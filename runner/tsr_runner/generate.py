"""Generation: multi-model, blind, adversarial (spec section 6) and the agreement gate (6.3)."""
from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field, asdict
from pathlib import Path

from .schema import Relation
from .rule import Decision, decide
from .vocab import Vocab, load_lexicon, ROOT
from .formal import parse_formula, image
from .providers import LoggedModel, ModelSpec, CallLog, Mock

PROMPTS = ROOT / "prompts"

RULE_TEXT = (
    "Keep each relationship, and flip the condition. Equivalences, definitions, identities, conservation "
    "laws and symmetries keep their shape. A cost or a limit caused by resistance turns around; a separation "
    "made by distance turns around; an odd number of such costs turns around. Units don't cross the mirror."
)


def _tmpl(name: str) -> str:
    return (PROMPTS / name).read_text()


def vocab_table(v: Vocab) -> str:
    lines = ["| Physical | Nonphysical | Map row |", "| --- | --- | --- |"]
    for phys, non, role, m in v.mirror:
        flag = " (provisional)" if m.get("provisional") else ""
        lines.append(f"| {phys} | {non}{flag} | {role} |")
    lines.append("")
    lines.append("Other legal nonphysical words: " + ", ".join(f"{w} ({e.get('note','')})" for w, e in v.extra.items()))
    return "\n".join(lines)


def resistance_rules(lexicon: dict, rec: Relation) -> str:
    qs = sorted({v.quantity for v in rec.variables} | {q for c in rec.costs for q in c.rises_with})
    out = []
    for q in qs:
        e = lexicon["quantities"].get(q)
        if not e:
            out.append(f"- {q}: not classified")
            continue
        out.append(f"- {q}: {'carries resistance' if e['verdict'] is True else 'does not carry resistance' if e['verdict'] is False else 'UNDETERMINED (a judgment call; say so)'} — {e.get('reason','')}")
    return "\n".join(out) or "- (no classified quantities)"


def relation_block(rec: Relation) -> str:
    """What the generator sees: the physics record without book_status, ruling, notes, depends_on."""
    d = {"id": rec.id, "title": rec.title, "statement": rec.statement, "formula": rec.formula,
         "form": rec.form,
         "variables": [{"name": v.name, "quantity": v.quantity, "carries_distance": v.carries_distance} for v in rec.variables],
         "costs": [asdict(c) for c in rec.costs],
         "physical_terms": rec.physical_terms,
         "alternate_statements": [{"statement": a.statement, "form": a.form, "costs": [asdict(c) for c in a.costs]} for a in rec.alternate_statements]}
    return "```yaml\n" + json.dumps(d, indent=2, ensure_ascii=False) + "\n```"


def generator_prompt(rec: Relation, v: Vocab, lexicon: dict) -> str:
    return _tmpl("generator.md").format(resistance_rules=resistance_rules(lexicon, rec), vocab_table=vocab_table(v),
                                        forbidden=", ".join(sorted(v.forbidden)), relation=relation_block(rec),
                                        record_id=rec.id)


def opponent_prompt(rec: Relation, v: Vocab, lexicon: dict, majority: dict) -> str:
    return _tmpl("opponent.md").format(rule=RULE_TEXT, resistance_rules=resistance_rules(lexicon, rec),
                                       vocab_table=vocab_table(v), relation=relation_block(rec),
                                       majority=json.dumps(majority, indent=2, ensure_ascii=False), record_id=rec.id)


def canary_prompt(rec: Relation) -> str:
    return _tmpl("canary.md").format(relation=relation_block(rec))


def parse_json(text: str) -> dict | None:
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def expected_image(rec: Relation, v: Vocab) -> tuple[str, list[str]]:
    """The word-map image of the record's formula (C1: never a rewrite), and the physical
    terms that have no partner, written in parentheses: '(work) = Frequency × Vibration'."""
    p = parse_formula(rec.formula, rec.physical_terms) if rec.formula and rec.physical_terms else None
    if not p:
        return "", []
    w = v.word_map()
    lname, expr = p
    img = image(expr, w)
    unmapped = sorted({t[1:] for t in (w.get(lname, "?" + lname),) + img.num + img.den if t.startswith("?")})
    fmt = lambda t: f"({t[1:]})" if t.startswith("?") else t
    rhs = " × ".join(fmt(t) for t in img.num) + (" ÷ " + " × ".join(fmt(t) for t in img.den) if img.den else "")
    return f"{fmt(w.get(lname, '?' + lname))} = {rhs}", unmapped


# ---------------------------------------------------------------------------
@dataclass
class GenResult:
    model: str
    vendor: str
    output: dict | None
    quarantined: bool = False
    quarantine_reason: str = ""
    lint: list[str] = field(default_factory=list)
    new_words: list[str] = field(default_factory=list)
    forbidden: list[str] = field(default_factory=list)


@dataclass
class RowResult:
    record_id: str
    decision: dict
    generators: list[GenResult]
    majority_shape: str | None
    agreement: dict
    opponent: dict | None
    opponent_flipped: bool
    candidate_forced: bool
    gate: list[str]           # reasons it failed the gate, empty if it passed
    consensus: dict | None    # the row that goes to collision testing
    mock: bool = False


def _check_output(o: dict, v: Vocab, rec: Relation | None = None) -> tuple[list[str], list[str], list[str]]:
    lint = v.lint_formula(o.get("reflected_formula", "") or "")
    known = {vv.name for vv in rec.variables} | {vv.quantity for vv in rec.variables} | set(o.get("unmapped_terms") or []) if rec else set(o.get("unmapped_terms") or [])
    new = list(o.get("new_words") or []) + v.new_words(o.get("reflected_formula", "") or "", known)
    forb = v.forbidden_in((o.get("reflected_sentence", "") or "") + " " + (o.get("reflected_formula", "") or ""))
    forb += ["C4 sense: " + x for x in v.sense_violations(o.get("reflected_sentence", "") or "", o.get("reflected_formula", "") or "")]
    return lint, sorted(set(new)), forb


def _supported_claims(agreeing: list, min_support: int = 2) -> list[dict]:
    """Monotone claims asserted (same rises/with/sign, normalized) by at least min_support agreeing generators."""
    from collections import Counter
    norm = lambda x: re.sub(r"\s+", " ", str(x or "")).strip().lower().replace("movement m", "movement").replace("the ", "")
    count: Counter = Counter()
    first: dict = {}
    for g in agreeing:
        seen = set()
        for c in (g.output.get("monotone_claims") or []):
            if not isinstance(c, dict) or not {"rises", "with", "sign"} <= set(c):
                continue
            try:
                sign = 1 if float(c["sign"]) > 0 else -1 if float(c["sign"]) < 0 else 0
            except (TypeError, ValueError):
                continue
            key = (norm(c["rises"]), norm(c["with"]), sign)
            if key in seen:
                continue
            seen.add(key)
            count[key] += 1
            first.setdefault(key, {"rises": c["rises"], "with": c["with"], "sign": sign})
    return [dict(first[k], support=n) for k, n in count.items() if n >= min_support]


def run_row(rec: Relation, generators: list[LoggedModel], opponent: LoggedModel | None,
            v: Vocab, lexicon: dict, criteria: dict, min_agree: int = 4, wording_pass: bool = True) -> RowResult:
    dec = decide(rec, lexicon, criteria)
    is_mock = any(isinstance(g.provider, Mock) for g in generators)
    if is_mock:
        img, unm = expected_image(rec, v)
        Mock.decisions[rec.id] = {"shape": dec.shape if dec.shape != "JUDGMENT" else "no partner",
                                  "statement": rec.statement, "image": img,
                                  "reasons": dec.reasons, "trace": dec.rule_trace, "forced": dec.forced,
                                  "unmapped": unm, "monotone_claims": rec.monotone_claims}
    prompt = generator_prompt(rec, v, lexicon)
    gens: list[GenResult] = []
    for g in generators:
        try:
            raw = g(prompt, role="generator", temperature=0.0)
        except RuntimeError as e:
            gens.append(GenResult(g.spec.name, g.spec.vendor, None, True, f"call failed: {e}"))
            continue
        o = parse_json(raw)
        if o is None:
            gens.append(GenResult(g.spec.name, g.spec.vendor, None, True, "unparseable output"))
            continue
        if wording_pass and not is_mock:
            try:
                raw2 = g(prompt + "\n\nSecond pass: keep every field as decided; improve only the wording of reflected_sentence and interpretation.",
                         role="generator-wording", temperature=0.7)
                o2 = parse_json(raw2)
                if o2 and o2.get("shape") == o.get("shape"):
                    o["reflected_sentence"] = o2.get("reflected_sentence", o["reflected_sentence"])
                    o["interpretation"] = o2.get("interpretation", o.get("interpretation"))
            except RuntimeError:
                pass
        lint, new, forb = _check_output(o, v, rec)
        if expected_image(rec, v)[1] or not rec.physical_terms:
            lint = []  # the formula has unmapped physical terms: it is not a reflection, so there is nothing to lint
        gr = GenResult(g.spec.name, g.spec.vendor, o, lint=lint, new_words=new, forbidden=forb)
        if o.get("knew_tsr") is True:
            gr.quarantined, gr.quarantine_reason = True, "admitted prior knowledge of TSR"
        gens.append(gr)

    live = [g for g in gens if not g.quarantined and g.output]
    shapes = Counter(g.output["shape"] for g in live)
    majority_shape, majority_n = (shapes.most_common(1)[0] if shapes else (None, 0))
    agreement = {"shapes": dict(shapes), "n_live": len(live), "n_total": len(gens), "majority_n": majority_n}

    gate: list[str] = []
    if dec.shape == "JUDGMENT" or not dec.forced:
        gate.append("procedure did not force the row: " + "; ".join(dec.reasons))
    if majority_n < min_agree:
        gate.append(f"{majority_n}/{len(gens)} agree on shape; need ≥ {min_agree}")
    if majority_shape and dec.shape not in ("JUDGMENT",) and majority_shape != dec.shape:
        gate.append(f"generators' majority {majority_shape!r} differs from the procedure {dec.shape!r}")
    agreeing = [g for g in live if g.output["shape"] == majority_shape]
    # the consensus sentence comes from the highest-confidence agreeing generator whose words pass the
    # frozen-vocabulary checks; a row is gated only if no agreeing generator passes
    clean = [g for g in agreeing if not g.new_words and not g.lint and not g.forbidden]
    if agreeing and not clean:
        if any(g.new_words for g in agreeing):
            gate.append("NEW words in every agreeing generator: " + str(sorted({w for g in agreeing for w in g.new_words})))
        if any(g.lint for g in agreeing):
            gate.append("units crossed the mirror in every agreeing generator: " + str([g.lint for g in agreeing if g.lint][0]))
        if any(g.forbidden for g in agreeing):
            gate.append("forbidden physical words on the nonphysical side in every agreeing generator: " + str(sorted({w for g in agreeing for w in g.forbidden})))
    agreeing_for_consensus = clean or agreeing

    consensus = None
    if agreeing:
        # the consensus row: majority shape; formula from the procedure's image (never a rewrite); sentence from the
        # highest-confidence clean agreeing generator
        def _content(g):
            sent = g.output.get("reflected_sentence", "") or ""
            n = sum(1 for w in v.nonphysical_words() if len(w) > 2 and re.search(rf"(?<![A-Za-z]){re.escape(w)}(?![A-Za-z])", sent))
            return (n, g.output.get("confidence", 0))
        best = max(agreeing_for_consensus, key=_content)
        img, unmapped = expected_image(rec, v)
        consensus = {"record_id": rec.id, "shape": majority_shape, "reflected_formula": img or best.output.get("reflected_formula", ""),
                     "formula_reflected": bool(img) and not unmapped, "unmapped_terms": unmapped,
                     "reflected_sentence": best.output.get("reflected_sentence", ""),
                     "sentences": [g.output.get("reflected_sentence", "") for g in agreeing],
                     "flags_by_model": {g.model: {"new_words": g.new_words, "lint": g.lint, "forbidden": g.forbidden} for g in agreeing if g.new_words or g.lint or g.forbidden},
                     "monotone_claims": _supported_claims(agreeing, min_support=2),
                     "monotone_claims_all": [c for g in agreeing for c in (g.output.get("monotone_claims") or [])],
                     "rule_trace": dec.rule_trace, "from_model": best.model}

    opp_out, flipped = None, False
    if opponent is None and not is_mock and consensus is not None and not gate:
        gate.append("opponent not run: candidate pending")
    if opponent is not None and consensus is not None and not gate:
        try:
            raw = opponent(opponent_prompt(rec, v, lexicon, consensus), role="opponent", temperature=0.0)
            opp_out = parse_json(raw)
        except RuntimeError as e:
            opp_out = {"error": str(e)}
        if opp_out and opp_out.get("rule_compliant") is True and opp_out.get("alternative_shape") in ("keeps", "turns around") \
                and opp_out.get("alternative_shape") != majority_shape:
            flipped = True
            gate.append("opponent produced a rule-compliant alternative: open joint")

    return RowResult(record_id=rec.id, decision=dec.to_dict(), generators=gens, majority_shape=majority_shape,
                     agreement=agreement, opponent=opp_out, opponent_flipped=flipped,
                     candidate_forced=not gate, gate=gate, consensus=consensus, mock=is_mock)


def run_canary(rec: Relation, generators: list[LoggedModel], v: Vocab) -> dict:
    """A fictional rule with the same shape: any TSR vocabulary in the output is a leak."""
    tsr_words = {w.lower() for w in v.nonphysical_words()} - {"e", "m", "c"}
    leaks = {}
    prompt = canary_prompt(rec)
    for g in generators:
        try:
            raw = g(prompt, role="canary", temperature=0.0)
        except RuntimeError as e:
            leaks[g.spec.name] = {"error": str(e)}
            continue
        low = raw.lower()
        hit = sorted(w for w in tsr_words if len(w) > 3 and re.search(rf"\b{re.escape(w)}\b", low))
        leaks[g.spec.name] = {"leaked": hit, "knew_framework": (parse_json(raw) or {}).get("knew_framework")}
    return leaks
