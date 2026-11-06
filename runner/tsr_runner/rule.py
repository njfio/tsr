"""The closed rule: feature extractor + decision procedure (spec section 5).

Nothing here reads an LLM's opinion and nothing here contains a hand-coded ruling.
Every decision is traceable to a record field, a lexicon entry and a criterion id.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path

import yaml

from .schema import Relation, Cost
from .vocab import load_lexicon, ROOT

CRITERIA_PATH = ROOT / "rule" / "criteria.yaml"


def load_criteria(path: Path = CRITERIA_PATH) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


@dataclass
class Features:
    is_identity: bool
    resistance_terms: int
    distance_terms: int
    cost_count: int
    undetermined: list[str]
    depends_on: list[str]
    cost_detail: list[dict]


@dataclass
class Decision:
    record_id: str
    shape: str                 # keeps | turns around | JUDGMENT
    formula_shape: str         # keeps (C1: the formula is never rewritten) | n/a
    forced: bool
    features: Features
    rule_trace: list[str]      # criterion ids that fired, in order
    reasons: list[str]
    alternates: list[dict] = field(default_factory=list)
    criteria_version: int | None = None
    lexicon_version: int | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        return d


def _count_costs(costs: list[Cost], lexicon_q: dict) -> tuple[int, int, list[str], list[dict]]:
    """Count resistance-caused costs and distance-made separations (C0, C3)."""
    resistance_terms = 0
    distance_terms = 0
    undetermined: list[str] = []
    detail = []
    for c in costs:
        carriers = []
        for q in c.rises_with:
            entry = lexicon_q.get(q)
            if entry is None:
                undetermined.append(f"{q}: not in lexicon")
                continue
            v = entry["verdict"]
            if v == "undetermined":
                undetermined.append(f"{q}: R1 undetermined ({entry.get('reason','')})")
            elif v is True:
                carriers.append(q)
        reverse = []
        for q in c.falls_with:
            entry = lexicon_q.get(q)
            if entry is None:
                undetermined.append(f"{q}: not in lexicon")
            elif entry["verdict"] == "undetermined":
                undetermined.append(f"{q}: R1 undetermined ({entry.get('reason','')})")
            elif entry["verdict"] is True:
                reverse.append(q)
        if reverse:
            # the rule speaks of costs that rise with resistance; one that falls with it is not covered (open joint reverse_cost)
            undetermined.append(f"difficulty falls with resistance-carrying {reverse}: reverse_cost joint")
        is_res_cost = bool(carriers)
        is_dist_cost = bool(c.separation_made_by_distance)
        # one cost block counts once, whichever way it is caused (the book counts claims, not variables)
        if is_res_cost:
            resistance_terms += 1
        elif is_dist_cost:
            distance_terms += 1
        detail.append({"what_gets_harder": c.what_gets_harder, "resistance_carriers": carriers, "reverse_carriers": reverse,
                       "separation": is_dist_cost, "counted": is_res_cost or is_dist_cost})
    return resistance_terms, distance_terms, undetermined, detail


def extract(rec: Relation, lexicon: dict, criteria: dict,
            form: str | None = None, costs: list[Cost] | None = None) -> Features:
    identity_forms = set(criteria["identity_forms"])
    form = form or rec.form
    costs = rec.costs if costs is None else costs
    is_identity = form in identity_forms
    r, d, und, detail = _count_costs(costs, lexicon["quantities"])
    return Features(is_identity=is_identity, resistance_terms=r, distance_terms=d,
                    cost_count=r + d, undetermined=und, depends_on=list(rec.depends_on),
                    cost_detail=detail)


def _decide_features(f: Features) -> tuple[str, list[str], list[str]]:
    trace, reasons = [], []
    if f.undetermined:
        trace.append("C3")
        reasons.extend(f.undetermined)
        return "JUDGMENT", trace, reasons
    if f.is_identity:
        trace.append("C1")
        reasons.append("equivalence / definition / conservation / symmetry: keeps (C1)")
        return "keeps", trace, reasons
    trace.append("C0")
    if f.cost_count % 2 == 1:
        reasons.append(f"{f.cost_count} resistance-caused cost(s) or separation(s): odd, turns around (C0)")
        return "turns around", trace, reasons
    if f.cost_count == 0:
        reasons.append("no resistance-caused cost and no separation: keeps (C0)")
    else:
        reasons.append(f"{f.cost_count} costs: even, keeps (C0)")
    return "keeps", trace, reasons


def decide(rec: Relation, lexicon: dict | None = None, criteria: dict | None = None) -> Decision:
    lexicon = lexicon or load_lexicon()
    criteria = criteria or load_criteria()
    f = extract(rec, lexicon, criteria)
    shape, trace, reasons = _decide_features(f)
    forced = shape != "JUDGMENT"

    # C2 and any other open joint named on the record
    if rec.depends_on:
        trace.append("C2" if "gravity_call" in rec.depends_on else "open_joint")
        reasons.append(f"depends on open joint(s) {rec.depends_on}: not forced")
        forced = False

    # C6: every standard form is run; disagreement -> not forced
    alts = []
    for a in rec.alternate_statements:
        fa = extract(rec, lexicon, criteria, form=a.form, costs=a.costs)
        sa, ta, ra = _decide_features(fa)
        alts.append({"statement": a.statement, "form": a.form, "shape": sa, "trace": ta, "note": a.note, "joint": a.joint})
        if sa != shape:
            trace.append("C6")
            reasons.append(f"alternate standard form ({a.form}) decides {sa!r} vs primary {shape!r}: {a.joint}, not forced")
            forced = False

    # C1: the formula is never rewritten
    formula_shape = "keeps" if rec.formula else "n/a"
    return Decision(record_id=rec.id, shape=shape, formula_shape=formula_shape, forced=forced,
                    features=f, rule_trace=trace, reasons=reasons, alternates=alts,
                    criteria_version=criteria.get("version"), lexicon_version=lexicon.get("version"))


def calibrate(records: list[Relation], lexicon=None, criteria=None) -> dict:
    """Run the procedure on every ruled record and compare to the book's ruling."""
    lexicon = lexicon or load_lexicon()
    criteria = criteria or load_criteria()
    rows, pending = [], []
    for r in records:
        if r.book_status != "ruled" or r.ruling is None:
            continue
        if r.ruling.shape is None:
            pending.append(r.id)
            continue
        d = decide(r, lexicon, criteria)
        rows.append({"id": r.id, "book": r.ruling.shape, "procedure": d.shape,
                     "match": d.shape == r.ruling.shape, "forced": d.forced,
                     "trace": d.rule_trace, "source": r.ruling.source})
    n = len(rows)
    ok = sum(1 for x in rows if x["match"])
    return {"matched": ok, "total": n, "rows": rows, "pending_author": pending,
            "criteria_version": criteria.get("version"), "lexicon_version": lexicon.get("version")}
