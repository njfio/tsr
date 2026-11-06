"""Staged orchestration for runs where the models are driven outside this process
(blind agent sessions, one per model per batch) and answer into files.

Stage files live under results/<run-id>/:
  prompts/generator-<batch>.md      one prompt per (batch); the same prompt goes to every generator model
  prompts/canary.md
  raw/<model>/<record_id>.json      per-record generator output (ingested from the model's batch answer)
  raw/<model>/canary.json
  raw/opponent/<record_id>.json
  raw/raters/<model>-<list>.json
  raw/judges/<model>-screen.json, raw/judges/<model>-pairs-<n>.json
  calls.jsonl                        every ingested answer, with the prompt hash it answers

The decision procedure, the agreement gate, the collision layers and the outputs are the
same code as the in-process pipeline; only the transport differs.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict
from itertools import combinations
from pathlib import Path

from .schema import Relation, load_corpus
from .rule import decide, load_criteria, calibrate
from .vocab import Vocab, load_lexicon, ROOT
from .providers import ModelSpec, CallLog, LoggedModel, sha
from . import generate, collide, decoy, ledger

CORPUS = ROOT / "corpus"
RESULTS = ROOT / "results"


class FileProvider:
    """Answers from raw/<model>/<key>.json; raises KeyError when the answer is not there yet."""
    def __init__(self, run_dir: Path, model_dir: str):
        self.dir = Path(run_dir) / "raw" / model_dir

    def complete(self, prompt, model, temperature, max_tokens=4000):
        key = _key_from_prompt(prompt)
        p = self.dir / f"{key}.json"
        if not p.exists():
            raise KeyError(f"no answer yet: {p}")
        return p.read_text()


def _key_from_prompt(prompt: str) -> str:
    m = re.search(r'"id":\s*"([^"]+)"', prompt)
    if m:
        return m.group(1)
    if "ROLE: rater" in prompt:
        m = re.search(r"LIST:\s*(\S+)", prompt)
        return "rater-" + (m.group(1) if m else "x")
    if "ROLE: judge" in prompt:
        return "judge-" + sha(prompt)[:10]
    return sha(prompt)[:12]


# ---------------------------------------------------------------------------
# batch prompts
# ---------------------------------------------------------------------------
BATCHES = {
    "A": ["mechanics"],
    "B": ["thermodynamics"],
    "C": ["statistical_mechanics", "information"],
    "D": ["waves_optics"],
    "E": ["electromagnetism"],
    "F": ["quantum"],
    "G": ["field_theory", "relativity"],
}
HIDDEN = {"A": ["mech.damping", "mech.friction"], "B": [], "C": [], "D": ["waves.interference_cancellation"], "E": [], "F": [], "G": []}


def batch_records(recs: list[Relation], batch: str) -> list[Relation]:
    by_id = {r.id: r for r in recs}
    out = [r for r in recs if r.domain in BATCHES[batch] and r.book_status != "ruled"]
    out += [by_id[h] for h in HIDDEN[batch]]
    return out


def generator_batch_prompt(records: list[Relation], v: Vocab, lexicon: dict, out_path: str) -> str:
    """The single-relation generator prompt, extended to a batch; one JSON object per relation."""
    head = generate._tmpl("generator.md")
    head = head.split("## The relation")[0].replace("to ONE physics relation", "to each of the physics relations below, one at a time")
    # resistance rules for every quantity in the batch
    qs = sorted({vv.quantity for r in records for vv in r.variables} | {q for r in records for c in r.costs for q in c.rises_with + c.falls_with})
    rr = []
    for q in qs:
        e = lexicon["quantities"].get(q)
        if e:
            rr.append(f"- {q}: {'carries resistance' if e['verdict'] is True else 'does not carry resistance' if e['verdict'] is False else 'UNDETERMINED (a judgment call; say so)'} — {e.get('reason','')}")
    head = head.format(resistance_rules="\n".join(rr), vocab_table=generate.vocab_table(v), forbidden=", ".join(sorted(v.forbidden)))
    body = ["## The relations", "", "Take each one on its own. Do not let one relation's reflection decide another's; the rule decides each.", ""]
    for r in records:
        body.append(f"### {r.id}")
        body.append(generate.relation_block(r))
        body.append("")
    schema = generate._tmpl("generator.md").split("## What to report")[1]
    schema = schema.replace('"id": "{record_id}"', '"id": "<the relation id>"').replace("{{", "{").replace("}}", "}")
    tail = ["## What to report", schema.strip(), "",
            f"Return a JSON ARRAY with one such object per relation, in the order given, and nothing else in the file. "
            f"Write it to the file `{out_path}` and then reply with the single word DONE. "
            "Do not read any other file, do not search the web, do not look at the repository."]
    return head + "\n".join(body + tail)


def opponent_batch_prompt(items: list[tuple[Relation, dict]], v: Vocab, lexicon: dict, out_path: str) -> str:
    head = generate._tmpl("opponent.md").split("## The relation")[0]
    qs = sorted({vv.quantity for r, _ in items for vv in r.variables} | {q for r, _ in items for c in r.costs for q in c.rises_with + c.falls_with})
    rr = []
    for q in qs:
        e = lexicon["quantities"].get(q)
        if e:
            rr.append(f"- {q}: {'carries resistance' if e['verdict'] is True else 'does not carry resistance' if e['verdict'] is False else 'UNDETERMINED'} — {e.get('reason','')}")
    head = head.format(rule=generate.RULE_TEXT, resistance_rules="\n".join(rr), vocab_table=generate.vocab_table(v))
    body = ["## The relations and their majority readings", ""]
    for r, maj in items:
        body.append(f"### {r.id}")
        body.append(generate.relation_block(r))
        body.append("Majority reading:")
        body.append("```json\n" + json.dumps({k: maj[k] for k in ("shape", "reflected_formula", "reflected_sentence", "rule_trace")}, indent=2, ensure_ascii=False) + "\n```")
        body.append("")
    tail = ["## Report", "", "For each relation return one JSON object:", "",
            '```json\n{"id": "<the relation id>", "alternative_shape": "keeps | turns around | null", "rule_compliant": false, '
            '"argument": "the equivalence, cost or separation you rest on, in one or two sentences, or why none exists", '
            '"reflected_sentence": "your alternative sentence in frozen words, or empty", "knew_tsr": false}\n```', "",
            f"Return a JSON ARRAY of these objects, one per relation, and nothing else. Write it to `{out_path}` and reply DONE. "
            "Do not read any other file, do not search the web, do not look at the repository."]
    return head + "\n".join(body + tail)


def canary_batch_prompt(rec: Relation, out_path: str) -> str:
    p = generate.canary_prompt(rec)
    return p + f"\n\nWrite the JSON object to `{out_path}` and reply DONE. Do not read any other file or search the web."


# ---------------------------------------------------------------------------
# stage 1: emit generator + canary prompts
# ---------------------------------------------------------------------------
def stage_gen_prompts(run_id: str) -> dict:
    lex, crit, recs, v = load_lexicon(), load_criteria(), load_corpus(CORPUS), Vocab()
    run_dir = RESULTS / run_id
    (run_dir / "prompts").mkdir(parents=True, exist_ok=True)
    (run_dir / "raw").mkdir(exist_ok=True)
    manifest = {"run_id": run_id, "batches": {}, "criteria_version": crit["version"], "lexicon_version": lex["version"]}
    for b in BATCHES:
        rs = batch_records(recs, b)
        out_rel = f"runner/results/{run_id}/raw/<MODEL>/batch-{b}.json"
        prompt = generator_batch_prompt(rs, v, lex, out_rel)
        (run_dir / "prompts" / f"generator-{b}.md").write_text(prompt)
        manifest["batches"][b] = {"records": [r.id for r in rs], "prompt_sha256": sha(prompt), "n": len(rs)}
    canary_rec = next(r for r in recs if r.id == "mech.hooke")
    cp = canary_batch_prompt(canary_rec, f"runner/results/{run_id}/raw/<MODEL>/canary.json")
    (run_dir / "prompts" / "canary.md").write_text(cp)
    manifest["canary"] = {"record": canary_rec.id, "prompt_sha256": sha(cp)}
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def _parse_array(text: str) -> list[dict]:
    text = text.strip()
    m = re.search(r"\[.*\]", text, flags=re.S)
    if not m:
        o = generate.parse_json(text)
        return [o] if o else []
    try:
        arr = json.loads(m.group(0))
    except json.JSONDecodeError:
        # tolerate trailing commas / fences
        cleaned = re.sub(r",\s*([\]}])", r"\1", m.group(0))
        arr = json.loads(cleaned)
    return [x for x in arr if isinstance(x, dict)]


def stage_ingest(run_id: str, model_dir: str, batch_file: Path, role: str, prompt_sha: str = "") -> dict:
    """Split a model's batch answer into per-record files and log each as a call."""
    run_dir = RESULTS / run_id
    log = CallLog(run_dir)
    arr = _parse_array(batch_file.read_text())
    out_dir = run_dir / "raw" / model_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    ids = []
    for o in arr:
        rid = o.get("id")
        if not rid:
            continue
        (out_dir / f"{rid}.json").write_text(json.dumps(o, ensure_ascii=False, indent=1))
        log.write(role=role, model=model_dir, provider="agent", vendor="", temperature=None,
                  prompt_sha256=prompt_sha, prompt_chars=0, response=json.dumps(o, ensure_ascii=False), error=None)
        ids.append(rid)
    return {"model": model_dir, "ingested": ids, "n": len(ids)}


# ---------------------------------------------------------------------------
# stage 2: rows from generator files (+ opponent files when present)
# ---------------------------------------------------------------------------
def _models(run_dir: Path, gens: list[tuple[str, str]], opp: tuple[str, str] | None):
    log = CallLog(run_dir / "replay")
    G = [LoggedModel(ModelSpec(name, "agent", vendor), log, FileProvider(run_dir, name)) for name, vendor in gens]
    O = LoggedModel(ModelSpec(opp[0], "agent", opp[1]), log, FileProvider(run_dir, "opponent")) if opp else None
    return G, O


def stage_rows(run_id: str, gens: list[tuple[str, str]], opp: tuple[str, str] | None, with_opponent: bool) -> list[dict]:
    lex, crit, recs, v = load_lexicon(), load_criteria(), load_corpus(CORPUS), Vocab()
    run_dir = RESULTS / run_id
    G, O = _models(run_dir, gens, opp)
    rows = []
    for b in BATCHES:
        for rec in batch_records(recs, b):
            rr = generate.run_row(rec, G, O if with_opponent else None, v, lex, crit, wording_pass=False)
            d = asdict(rr)
            d["batch"] = b
            d["hidden_calibration"] = rec.book_status == "ruled"
            rows.append(d)
    (run_dir / ("rows.json" if with_opponent else "rows-pre-opponent.json")).write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    return rows


def stage_opp_prompts(run_id: str, rows: list[dict]) -> dict:
    lex, recs, v = load_lexicon(), load_corpus(CORPUS), Vocab()
    by_id = {r.id: r for r in recs}
    run_dir = RESULTS / run_id
    out = {}
    for b in BATCHES:
        items = [(by_id[r["record_id"]], r["consensus"]) for r in rows
                 if r["batch"] == b and r["consensus"] and not r["gate"]]
        if not items:
            continue
        p = opponent_batch_prompt(items, v, lex, f"runner/results/{run_id}/raw/opponent/batch-{b}.json")
        (run_dir / "prompts" / f"opponent-{b}.md").write_text(p)
        out[b] = {"n": len(items), "records": [r.id for r, _ in items], "prompt_sha256": sha(p)}
    return out


# ---------------------------------------------------------------------------
# stage 3: decoys
# ---------------------------------------------------------------------------
def stage_decoy_prompts(run_id: str, rows: list[dict], n_lists: int = 3, seed: int = 0) -> dict:
    v = Vocab()
    run_dir = RESULTS / run_id
    forced = collide.eligible(rows)
    # controls: hidden calibration rows that were forced (the book's own reflections)
    statements, key = decoy.build_list(forced, seed=seed)
    # split into lists so each rater prompt stays the size of round 2's
    size = -(-len(statements) // n_lists)
    lists = {}
    for i in range(n_lists):
        chunk = statements[i * size:(i + 1) * size]
        name = f"L{i+1}"
        block = "\n".join(f"{s['id']}: {s['text']}" for s in chunk)
        prompt = generate._tmpl("rater.md").format(vocab_table=generate.vocab_table(v), statements=block)
        prompt = prompt.replace("## Statements", f"LIST: {name}\n\n## Statements")
        prompt += (f"\n\nWrite the JSON object to `runner/results/{run_id}/raw/raters/<MODEL>-{name}.json` and reply DONE. "
                   "Do not read any other file, do not search the web, do not look at the repository.")
        (run_dir / "prompts" / f"rater-{name}.md").write_text(prompt)
        lists[name] = {"ids": [s["id"] for s in chunk], "prompt_sha256": sha(prompt)}
    (run_dir / "decoys.json").write_text(json.dumps({"statements": statements, "key": key, "lists": lists}, indent=2, ensure_ascii=False))
    return {"n_statements": len(statements), "lists": {k: len(x["ids"]) for k, x in lists.items()}}


def stage_decoy_score(run_id: str, rows: list[dict], margin_fraction: float = 0.5) -> dict:
    run_dir = RESULTS / run_id
    d = json.loads((run_dir / "decoys.json").read_text())
    ratings: dict[str, dict[str, int]] = {}
    for p in sorted((run_dir / "raw" / "raters").glob("*.json")):
        model = p.stem.rsplit("-", 1)[0]
        o = generate.parse_json(p.read_text()) or {}
        ratings.setdefault(model, {}).update({k: int(x) for k, x in (o.get("ratings") or {}).items() if str(x).strip().isdigit()})
    controls = {r["record_id"] for r in rows if r.get("hidden_calibration") and r["candidate_forced"]}
    score = decoy.score(ratings, d["key"], controls=controls, margin_fraction=margin_fraction)
    score["controls"] = sorted(controls)
    d["ratings"] = ratings
    d["score"] = score
    (run_dir / "decoys.json").write_text(json.dumps(d, indent=2, ensure_ascii=False))
    return score


# ---------------------------------------------------------------------------
# stage 4: Layer B as set-level screening, then pairwise confirmation
# ---------------------------------------------------------------------------
def _sentences(rows: list[dict], records: dict[str, Relation]) -> list[dict]:
    forced = collide.eligible(rows)
    items = [{"key": f"N{i+1:02d}", "record_id": r["record_id"], "sentence": r["consensus"]["reflected_sentence"], "book": False}
             for i, r in enumerate(forced)]
    for j, b in enumerate(collide.book_claim_sentences(records)):
        items.append({"key": f"K{j+1:02d}", **b})
    return items


def stage_judge_screen_prompts(run_id: str, rows: list[dict]) -> dict:
    v, recs = Vocab(), load_corpus(CORPUS)
    records = {r.id: r for r in recs}
    run_dir = RESULTS / run_id
    items = _sentences(rows, records)
    # shuffle so new and book sentences are interleaved and unlabelled
    import random
    rng = random.Random(1)
    order = items[:]
    rng.shuffle(order)
    blind = [{"key": f"S{i+1:03d}", "sentence": it["sentence"]} for i, it in enumerate(order)]
    keymap = {f"S{i+1:03d}": {"record_id": it["record_id"], "book": it["book"]} for i, it in enumerate(order)}
    block = "\n".join(f"{b['key']}: {b['sentence']}" for b in blind)
    prompt = ("ROLE: judge\n\nBelow is a framework's vocabulary and a list of sentences written in it. Taking every sentence as true in the "
              "framework's meanings, find every PAIR of sentences for which there is a situation the two describe differently. "
              "You are not judging whether the framework is true, deep or sensible; only whether two of its sentences can both hold. "
              "Be strict: a pair is a contradiction only if you can state the one situation in a sentence. Do not report pairs that are merely "
              "about different things. Use only this prompt; if you know anything else about TSR, set it aside and say so.\n\n"
              f"## The vocabulary and its meanings\n\n{generate.vocab_table(v)}\n\n## Sentences\n\n{block}\n\n## Report\n\n"
              'Return ONE JSON object: {"contradictions": [{"a": "S001", "b": "S002", "situation": "one sentence"}], '
              '"underdetermined": [{"a": "S003", "b": "S004", "meaning_not_fixed": "which meaning"}], "knew_tsr": false}\n\n'
              f"Write it to `runner/results/{run_id}/raw/judges/<MODEL>-screen.json` and reply DONE. "
              "Do not read any other file, do not search the web, do not look at the repository.")
    (run_dir / "prompts" / "judge-screen.md").write_text(prompt)
    (run_dir / "judge-screen-key.json").write_text(json.dumps({"keymap": keymap, "n": len(blind), "prompt_sha256": sha(prompt)}, indent=2))
    return {"n_sentences": len(blind), "n_new": sum(1 for it in items if not it["book"]), "n_book": sum(1 for it in items if it["book"])}


def stage_judge_pair_prompts(run_id: str) -> dict:
    """Pairs flagged by either screening judge go to both judges for isolated confirmation."""
    v = Vocab()
    run_dir = RESULTS / run_id
    key = json.loads((run_dir / "judge-screen-key.json").read_text())["keymap"]
    screen = json.loads((run_dir / "prompts" / "judge-screen.md").read_text().split("## Sentences\n\n")[1].split("\n\n## Report")[0].__repr__()) if False else None
    # recover sentences from the prompt
    txt = (run_dir / "prompts" / "judge-screen.md").read_text()
    block = txt.split("## Sentences\n\n")[1].split("\n\n## Report")[0]
    sent = dict(line.split(": ", 1) for line in block.splitlines() if ": " in line)
    flagged = {}
    for p in sorted((run_dir / "raw" / "judges").glob("*-screen.json")):
        o = generate.parse_json(p.read_text()) or {}
        for c in o.get("contradictions", []) or []:
            a, b = sorted((c.get("a", ""), c.get("b", "")))
            if a in sent and b in sent and a != b:
                flagged.setdefault((a, b), []).append({"judge": p.stem, "situation": c.get("situation", "")})
    pairs = sorted(flagged)
    # drop book-vs-book pairs (not this system's job)
    pairs = [(a, b) for a, b in pairs if not (key[a]["book"] and key[b]["book"])]
    lines = []
    for i, (a, b) in enumerate(pairs, 1):
        lines.append(f"P{i:03d}\nA: {sent[a]}\nB: {sent[b]}\n")
    prompt = ("ROLE: judge\n\nFor each pair below, taking both sentences as true in the framework's meanings, is there a situation they describe "
              "differently? Judge each pair on its own. Use only this prompt; if you know anything else about TSR, set it aside and say so.\n\n"
              f"## The vocabulary and its meanings\n\n{generate.vocab_table(v)}\n\n## Pairs\n\n" + "\n".join(lines) +
              '\n\n## Report\n\nReturn ONE JSON object: {"verdicts": [{"pair": "P001", "verdict": "consistent | contradiction | underdetermined", '
              '"situation": "if contradiction, the one situation, in one sentence; if underdetermined, the meaning not fixed; else empty"}], "knew_tsr": false}\n\n'
              f"Write it to `runner/results/{run_id}/raw/judges/<MODEL>-pairs.json` and reply DONE. Do not read any other file, do not search the web, do not look at the repository.")
    (run_dir / "prompts" / "judge-pairs.md").write_text(prompt)
    (run_dir / "judge-pairs-key.json").write_text(json.dumps({"pairs": {f"P{i:03d}": {"a": a, "b": b, "flagged_by": flagged[(a, b)]} for i, (a, b) in enumerate(pairs, 1)}}, indent=2))
    return {"n_flagged_pairs": len(pairs), "flagged_by_judge": {p.stem: sum(1 for v_ in flagged.values() for x in v_ if x["judge"] == p.stem) for p in (run_dir / "raw" / "judges").glob("*-screen.json")}}


def stage_layer_b_collect(run_id: str) -> list[collide.Collision]:
    run_dir = RESULTS / run_id
    pk = json.loads((run_dir / "judge-pairs-key.json").read_text())["pairs"]
    sk = json.loads((run_dir / "judge-screen-key.json").read_text())["keymap"]
    txt = (run_dir / "prompts" / "judge-screen.md").read_text()
    block = txt.split("## Sentences\n\n")[1].split("\n\n## Report")[0]
    sent = dict(line.split(": ", 1) for line in block.splitlines() if ": " in line)
    verdicts: dict[str, list[dict]] = {}
    for p in sorted((run_dir / "raw" / "judges").glob("*-pairs.json")):
        o = generate.parse_json(p.read_text()) or {}
        for vd in o.get("verdicts", []) or []:
            verdicts.setdefault(vd.get("pair", ""), []).append({"judge": p.stem, **vd})
    out = []
    for pid, info in pk.items():
        vs = verdicts.get(pid, [])
        a, b = info["a"], info["b"]
        rows_ = [sk[a]["record_id"], sk[b]["record_id"]]
        detail = {"pair": pid, "a": sent[a], "b": sent[b], "a_book": sk[a]["book"], "b_book": sk[b]["book"],
                  "screen": info["flagged_by"], "verdicts": vs}
        if len(vs) >= 2 and all(x.get("verdict") == "contradiction" for x in vs):
            sits = {re.sub(r"[^a-z ]", "", (x.get("situation") or "").lower()).strip() for x in vs}
            status = "candidate"
            detail["same_situation"] = len(sits) == 1
        elif any(x.get("verdict") == "contradiction" for x in vs):
            status = "judges_split"
        elif any(x.get("verdict") == "underdetermined" for x in vs):
            status = "underdetermined"
        else:
            status = "consistent_on_confirmation"
        out.append(collide.Collision("B", rows_, detail, status=status))
    return out


# ---------------------------------------------------------------------------
# stage 5: Layer A + C, breaks, outputs
# ---------------------------------------------------------------------------
def stage_finalize(run_id: str, rows: list[dict], layer_b: list[collide.Collision], book_path: Path | None,
                   canary: dict | None, roster_problems: list[str], deviations: list[str]) -> dict:
    lex, crit, recs, v = load_lexicon(), load_criteria(), load_corpus(CORPUS), Vocab()
    records = {r.id: r for r in recs}
    run_dir = RESULTS / run_id
    forced = collide.eligible(rows)
    cols = collide.layer_a(forced, records, v) + layer_b
    book = collide.BookIndex(book_path)
    cols = collide.layer_c(cols, book, None, v)
    cols_d = [asdict(c) for c in cols]
    (run_dir / "collisions.json").write_text(json.dumps(cols_d, indent=2, ensure_ascii=False))
    breaks = collide.break_report(cols, {r["record_id"]: r for r in rows}, records)
    (run_dir / "breaks.json").write_text(json.dumps(breaks, indent=2, ensure_ascii=False))
    cal = calibrate(recs, lex, crit)
    dec = json.loads((run_dir / "decoys.json").read_text()).get("score") if (run_dir / "decoys.json").exists() else None
    # per-domain ledgers
    (ROOT / "ledger").mkdir(exist_ok=True)
    for dom in sorted({records[r["record_id"]].domain for r in rows}):
        drows = [r for r in rows if records[r["record_id"]].domain == dom]
        dids = {r["record_id"] for r in drows}
        dcols = [c for c in cols_d if set(c["rows"]) & dids]
        dbreaks = [b for b in breaks if set(b["rows"]) & dids]
        md = ledger.ledger_md(dom, run_id, drows, dcols, dbreaks, dec, records, False)
        (ROOT / "ledger" / f"{dom}.md").write_text(md)
    (ROOT / "patches").mkdir(exist_ok=True)
    (ROOT / "patches" / "tsr_formal_rows.py").write_text(ledger.patch_rows([r for r in rows if not r.get("hidden_calibration")], records, run_id))
    rep = ledger.report_md(run_id, "all domains", rows, cols_d, breaks, dec, cal, crit, lex, canary, roster_problems, False)
    if deviations:
        rep += "\n\n## Deviations from the spec in this run\n\n" + "\n".join(f"- {d}" for d in deviations)
    (run_dir / "report.md").write_text(rep)
    return {"forced": len(forced), "collisions": len([c for c in cols if c.status not in ("informational",)]),
            "breaks": len([b for b in breaks if b["is_break"]]), "report": str(run_dir / "report.md")}


# ---------------------------------------------------------------------------
# Layer C, agent-driven: one prompt listing every candidate with its book passages
# ---------------------------------------------------------------------------
def stage_layer_c_prompt(run_id: str, cands: list[collide.Collision], book_path: Path) -> dict:
    run_dir = RESULTS / run_id
    book = collide.BookIndex(book_path)
    items = []
    for i, c in enumerate([c for c in cands if c.status == "candidate"], 1):
        q = (c.detail.get("a", "") + " " + c.detail.get("b", "") + " " + " ".join(v.get("situation", "") for v in c.detail.get("verdicts", [])))[:800]
        hits = book.search(q, k=5)
        c.detail["book_hits"] = hits
        c.detail["layer_c_id"] = f"X{i:02d}"
        items.append((c, hits))
    lines = ["ROLE: judge", "",
             "Each item below is a pair of sentences in a framework's vocabulary that two independent judges found contradictory, "
             "with the situation they named, followed by passages from the framework's book. For each item decide: does any passage "
             "state a resolution that makes both sentences true at once (`resolves`), is one of the sentences itself the book's own claim "
             "with the other contradicting it (`one_side`), or is the book silent (`silent`)? Quote the resolving passage if there is one. "
             "Use only this prompt.", ""]
    for c, hits in items:
        lines.append(f"### {c.detail['layer_c_id']}")
        lines.append(f"A: {c.detail.get('a','')}")
        lines.append(f"B: {c.detail.get('b','')}")
        lines.append("Situation named by the judges: " + " / ".join(v.get("situation", "") for v in c.detail.get("verdicts", [])))
        lines.append("Passages:")
        for h in hits:
            lines.append(f"- [{h['chapter']}] {h['text']}")
        lines.append("")
    lines.append('## Report\n\nReturn ONE JSON object: {"items": [{"id": "X01", "verdict": "resolves | one_side | silent", "where": "chapter", "quote": "the resolving sentence or empty", "note": ""}]}')
    lines.append(f"\nWrite it to `runner/results/{run_id}/raw/judges/<MODEL>-layer-c.json` and reply DONE. Do not read any other file, do not search the web, do not look at the repository.")
    (run_dir / "prompts" / "layer-c.md").write_text("\n".join(lines))
    return {"n_candidates": len(items)}


def stage_layer_c_collect(run_id: str, cands: list[collide.Collision]) -> list[collide.Collision]:
    run_dir = RESULTS / run_id
    verdicts = {}
    for p in sorted((run_dir / "raw" / "judges").glob("*-layer-c.json")):
        o = generate.parse_json(p.read_text()) or {}
        for it in o.get("items", []) or []:
            verdicts.setdefault(it.get("id"), []).append({"judge": p.stem, **it})
    for c in cands:
        cid = c.detail.get("layer_c_id")
        if not cid or c.status != "candidate":
            continue
        vs = verdicts.get(cid, [])
        c.detail["layer_c"] = vs
        if vs and all(v.get("verdict") == "resolves" for v in vs):
            c.status = "book_resolves"
            c.book_ref = "; ".join(f"{v.get('where','')}: {v.get('quote','')[:160]}" for v in vs)
        elif not vs:
            c.status = "stands (book text not available or silent)"
        else:
            c.status = "stands"
            c.book_ref = "; ".join(f"{v['judge']}: {v.get('verdict')} {v.get('where','')}" for v in vs)
    return cands
