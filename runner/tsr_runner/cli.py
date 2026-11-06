"""CLI: tsr-validate, tsr-calibrate, tsr-run, tsr-collide, tsr-ledger (spec section 3).

    python -m tsr_runner.cli validate
    python -m tsr_runner.cli calibrate
    python -m tsr_runner.cli run --domain mechanics --models models.yaml [--mock] [--no-decoys]
    python -m tsr_runner.cli collide --runs results/<id> [results/<id2> ...] --book path/to/book.txt
    python -m tsr_runner.cli ledger --run results/<id>
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path

from .schema import load_corpus, validate
from .rule import decide, calibrate, load_criteria
from .vocab import Vocab, load_lexicon, ROOT
from .providers import ModelSpec, CallLog, LoggedModel, load_models, check_roster
from . import generate, collide, decoy, ledger

CORPUS = ROOT / "corpus"
RESULTS = ROOT / "results"
LEDGER = ROOT / "ledger"
PATCHES = ROOT / "patches"

MOCK_ROSTER = [ModelSpec(f"mock-{i}", "mock", v, open_weights=(i == 5)) for i, v in
               enumerate(["openai", "anthropic", "google", "mistral", "open-weights"], 1)]


def _load_all():
    lex = load_lexicon()
    crit = load_criteria()
    recs = load_corpus(CORPUS)
    return lex, crit, recs


def cmd_validate(args):
    lex, crit, recs = _load_all()
    errs = []
    for r in recs:
        errs += validate(r, lex["quantities"], set(crit["identity_forms"]))
    nulls = [(r.id, "review pending") for r in recs if r.review == "pending"]
    print(f"{len(recs)} records; {len(errs)} schema problems; {len(nulls)} awaiting second-pass physics review")
    for e in errs:
        print("  ", e)
    by_domain = {}
    for r in recs:
        by_domain.setdefault(r.domain, []).append(r)
    for d, rs in sorted(by_domain.items()):
        print(f"  {d}: {len(rs)} ({sum(1 for r in rs if r.book_status == 'unreflected')} unreflected)")
    return 1 if errs else 0


def cmd_calibrate(args):
    lex, crit, recs = _load_all()
    cal = calibrate(recs, lex, crit)
    print(f"criteria v{crit['version']}, lexicon v{lex['version']}: {cal['matched']}/{cal['total']} rulings reproduced from records alone")
    for row in cal["rows"]:
        print(f"  {'ok  ' if row['match'] else 'MISS'} {row['id']:45s} book={row['book']:12s} procedure={row['procedure']:12s} {row['trace']}{'' if row['forced'] else '  (not forced)'}")
    if cal["pending_author"]:
        print("  pending author rulings:", ", ".join(cal["pending_author"]))
    print("open joints:", ", ".join(j["id"] for j in crit.get("open_joints", [])))
    return 0 if cal["matched"] == cal["total"] else 1


def cmd_preview(args):
    """What the procedure alone decides, before any model is consulted (no generators, no opponent)."""
    lex, crit, recs = _load_all()
    from collections import Counter
    by_domain = {}
    for r in recs:
        if args.domain and r.domain != args.domain:
            continue
        by_domain.setdefault(r.domain, []).append(r)
    totals = Counter()
    for d, rs in sorted(by_domain.items()):
        print(f"\n== {d} ==")
        for r in rs:
            dec = decide(r, lex, crit)
            status = "forced" if dec.forced else ("JUDGMENT" if dec.shape == "JUDGMENT" else "open")
            joint = ""
            if not dec.forced:
                joint = " <- " + "; ".join(x for x in dec.reasons if "not forced" in x or "undetermined" in x or "reverse_cost" in x)[:110]
            print(f"  {r.id:42s} {dec.shape:12s} {status:9s} {','.join(dec.rule_trace):10s}{joint}")
            totals[(d, status)] += 1
    print("\n== totals ==")
    for d in sorted(by_domain):
        n = len(by_domain[d])
        print(f"  {d:22s} {n:3d} records: forced {totals[(d,'forced')]:3d}, judgment {totals[(d,'JUDGMENT')]:3d}, open {totals[(d,'open')]:3d}")
    return 0


def _roster(args):
    if args.mock:
        gens = MOCK_ROSTER
        opp = ModelSpec("mock-opponent", "mock", "anthropic")
        judges = [ModelSpec("mock-judge-1", "mock", "google"), ModelSpec("mock-judge-2", "mock", "mistral")]
        raters = [ModelSpec(f"mock-rater-{i}", "mock", "x") for i in range(1, 5)]
        return gens, opp, judges, raters
    models = load_models(Path(args.models))
    roles = {}
    for m in models:
        roles.setdefault(getattr(m, "role", "generator"), []).append(m)
    import yaml
    d = yaml.safe_load(Path(args.models).read_text())
    gens = [ModelSpec(**m) for m in d["generators"]]
    opp = ModelSpec(**d["opponent"])
    judges = [ModelSpec(**m) for m in d["judges"]]
    raters = [ModelSpec(**m) for m in d.get("raters", d["judges"])]
    return gens, opp, judges, raters


def cmd_run(args):
    lex, crit, recs = _load_all()
    v = Vocab()
    domain_recs = [r for r in recs if r.domain == args.domain and (args.include_ruled or r.book_status != "ruled")]
    if args.hidden_calibration:
        # Phase 3: hidden calibration items are run blind alongside the domain (e.g. damping for mechanics)
        domain_recs += [r for r in recs if r.id in args.hidden_calibration]
    if not domain_recs:
        print(f"no records for domain {args.domain!r}")
        return 1
    run_id = args.run_id or f"{args.domain}-{time.strftime('%Y%m%d-%H%M%S')}" + ("-MOCK" if args.mock else "")
    run_dir = RESULTS / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    log = CallLog(run_dir)
    gens_spec, opp_spec, judges_spec, raters_spec = _roster(args)
    roster_problems = check_roster(gens_spec)
    gens = [LoggedModel(m, log) for m in gens_spec]
    opp = LoggedModel(opp_spec, log)
    judges = [LoggedModel(m, log) for m in judges_spec]
    raters = [LoggedModel(m, log) for m in raters_spec]
    # vendor rule: opponent must differ from the majority vendor of the generators
    cal = calibrate(recs, lex, crit)
    config = {"run_id": run_id, "domain": args.domain, "mock": args.mock, "criteria_version": crit["version"],
              "lexicon_version": lex["version"], "records": [r.id for r in domain_recs],
              "record_digests": {r.id: r.digest() for r in domain_recs},
              "generators": [asdict(m) for m in gens_spec], "opponent": asdict(opp_spec),
              "judges": [asdict(m) for m in judges_spec], "roster_problems": roster_problems,
              "calibration": {"matched": cal["matched"], "total": cal["total"], "pending": cal["pending_author"]}}
    (run_dir / "config.json").write_text(json.dumps(config, indent=2))

    rows = []
    for rec in domain_recs:
        rr = generate.run_row(rec, gens, opp, v, lex, crit, min_agree=args.min_agree, wording_pass=not args.mock)
        d = asdict(rr)
        rows.append(d)
        print(f"  {rec.id:45s} procedure={rr.decision['shape']:12s} majority={str(rr.majority_shape):12s} {'FORCED' if rr.candidate_forced else 'open: ' + rr.gate[0][:70]}")
    (run_dir / "rows.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    canary = None
    if not args.no_canary:
        canary = generate.run_canary(domain_recs[0], gens, v)
        (run_dir / "canary.json").write_text(json.dumps(canary, indent=2))
        for m, c in canary.items():
            if c.get("leaked"):
                print(f"  CANARY LEAK {m}: {c['leaked']}")

    dec = None
    forced = collide.eligible(rows)
    if forced and not args.no_decoys:
        statements, key = decoy.build_list(forced, seed=args.seed)
        if args.mock:
            from .providers import Mock
            Mock.decoy_key = key
        ratings = decoy.rate(statements, raters, v)
        dec = decoy.score(ratings, key)
        (run_dir / "decoys.json").write_text(json.dumps({"statements": statements, "key": key, "ratings": ratings, "score": dec}, indent=2, ensure_ascii=False))
        if dec["curated"]:
            for r in rows:
                if r["candidate_forced"]:
                    r["candidate_forced"] = False
                    r["gate"].append("decoy margin failed: domain marked curated")
            (run_dir / "rows.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    # collisions within the domain
    records = {r.id: r for r in recs}
    forced = collide.eligible(rows)
    cols = collide.layer_a(forced, records, v)
    if not args.no_layer_b:
        cols += collide.layer_b(forced, records, judges, v)
    book = collide.BookIndex(Path(args.book) if args.book else None)
    cols = collide.layer_c(cols, book, None, v)
    cols_d = [asdict(c) for c in cols]
    (run_dir / "collisions.json").write_text(json.dumps(cols_d, indent=2, ensure_ascii=False))
    breaks = collide.break_report(cols, {r["record_id"]: r for r in rows}, records)
    (run_dir / "breaks.json").write_text(json.dumps(breaks, indent=2, ensure_ascii=False))

    _write_outputs(run_id, args.domain, rows, cols_d, breaks, dec, cal, crit, lex, canary, roster_problems, args.mock, records)
    print(f"run {run_id}: {len(forced)} forced of {len(rows)}; {len([c for c in cols if c.status != 'informational'])} collisions; {len([b for b in breaks if b['is_break']])} breaks")
    return 0


def _write_outputs(run_id, domain, rows, cols, breaks, dec, cal, crit, lex, canary, roster_problems, mock, records):
    run_dir = RESULTS / run_id
    LEDGER.mkdir(exist_ok=True)
    PATCHES.mkdir(exist_ok=True)
    md = ledger.ledger_md(domain, run_id, rows, cols, breaks, dec, records, mock)
    (run_dir / f"ledger-{domain}.md").write_text(md)
    if not mock:
        (LEDGER / f"{domain}.md").write_text(md)
        (PATCHES / "tsr_formal_rows.py").write_text(ledger.patch_rows(rows, records, run_id))
    (run_dir / "report.md").write_text(ledger.report_md(run_id, domain, rows, cols, breaks, dec, cal, crit, lex, canary, roster_problems, mock))


def cmd_collide(args):
    """Phase 5: cross-domain collisions over the forced rows of several runs."""
    lex, crit, recs = _load_all()
    v = Vocab()
    records = {r.id: r for r in recs}
    rows = []
    mock = False
    for rd in args.runs:
        rd = Path(rd)
        rows += json.loads((rd / "rows.json").read_text())
        mock = mock or json.loads((rd / "config.json").read_text()).get("mock", False)
    forced = collide.eligible(rows)
    out_dir = RESULTS / (args.run_id or ("cross-" + time.strftime('%Y%m%d-%H%M%S') + ("-MOCK" if mock else "")))
    out_dir.mkdir(parents=True, exist_ok=True)
    log = CallLog(out_dir)
    cols = collide.layer_a(forced, records, v)
    if args.models or args.mock:
        if args.mock:
            judges = [LoggedModel(ModelSpec("mock-judge-1", "mock", "a"), log), LoggedModel(ModelSpec("mock-judge-2", "mock", "b"), log)]
        else:
            import yaml
            d = yaml.safe_load(Path(args.models).read_text())
            judges = [LoggedModel(ModelSpec(**m), log) for m in d["judges"]]
        cols += collide.layer_b(forced, records, judges, v)
    book = collide.BookIndex(Path(args.book) if args.book else None)
    cols = collide.layer_c(cols, book, None, v)
    cols_d = [asdict(c) for c in cols]
    (out_dir / "collisions.json").write_text(json.dumps(cols_d, indent=2, ensure_ascii=False))
    breaks = collide.break_report(cols, {r["record_id"]: r for r in rows}, records)
    (out_dir / "breaks.json").write_text(json.dumps(breaks, indent=2, ensure_ascii=False))
    cal = calibrate(recs, lex, crit)
    (out_dir / "report.md").write_text(ledger.report_md(out_dir.name, "cross-domain", rows, cols_d, breaks, None, cal, crit, lex, None, [], mock))
    print(f"{len(forced)} forced rows across {len(args.runs)} runs; {len(cols)} collisions; {len([b for b in breaks if b['is_break']])} breaks -> {out_dir}")
    return 0


def cmd_ledger(args):
    rd = Path(args.run)
    cfg = json.loads((rd / "config.json").read_text())
    lex, crit, recs = _load_all()
    records = {r.id: r for r in recs}
    rows = json.loads((rd / "rows.json").read_text())
    cols = json.loads((rd / "collisions.json").read_text())
    breaks = json.loads((rd / "breaks.json").read_text())
    dec = json.loads((rd / "decoys.json").read_text())["score"] if (rd / "decoys.json").exists() else None
    canary = json.loads((rd / "canary.json").read_text()) if (rd / "canary.json").exists() else None
    cal = calibrate(recs, lex, crit)
    _write_outputs(cfg["run_id"], cfg["domain"], rows, cols, breaks, dec, cal, crit, lex, canary, cfg.get("roster_problems", []), cfg.get("mock", False), records)
    print((rd / "report.md").read_text())
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="tsr-runner")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate").set_defaults(fn=cmd_validate)
    sub.add_parser("calibrate").set_defaults(fn=cmd_calibrate)
    pv = sub.add_parser("preview")
    pv.add_argument("--domain")
    pv.set_defaults(fn=cmd_preview)
    r = sub.add_parser("run")
    r.add_argument("--domain", required=True)
    r.add_argument("--models", help="models.yaml with generators / opponent / judges / raters")
    r.add_argument("--mock", action="store_true", help="plumbing only; no model is consulted")
    r.add_argument("--run-id")
    r.add_argument("--min-agree", type=int, default=4)
    r.add_argument("--seed", type=int, default=0)
    r.add_argument("--book", help="plain text of the paperback for Layer C")
    r.add_argument("--include-ruled", action="store_true")
    r.add_argument("--hidden-calibration", nargs="*", default=[])
    r.add_argument("--no-decoys", action="store_true")
    r.add_argument("--no-canary", action="store_true")
    r.add_argument("--no-layer-b", action="store_true")
    r.set_defaults(fn=cmd_run)
    c = sub.add_parser("collide")
    c.add_argument("--runs", nargs="+", required=True)
    c.add_argument("--models")
    c.add_argument("--mock", action="store_true")
    c.add_argument("--book")
    c.add_argument("--run-id")
    c.set_defaults(fn=cmd_collide)
    l = sub.add_parser("ledger")
    l.add_argument("--run", required=True)
    l.set_defaults(fn=cmd_ledger)
    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
