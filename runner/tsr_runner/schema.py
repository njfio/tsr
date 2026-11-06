"""Relation records: the corpus schema (spec section 4), loading and validation.

A record is one physics statement. A relation that is both a definition and a
cost claim is two records linked by ``derived_from`` (criterion C1).
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable

import yaml

FORMS = {"equation", "definition", "identity", "conservation", "inequality",
         "limit", "symmetry", "statistical"}
BOOK_STATUS = {"unreflected", "reflected", "ruled"}
SHAPES = {"keeps", "turns around", "no partner"}
DOMAINS = {"mechanics", "thermodynamics", "statistical_mechanics", "waves_optics",
           "electromagnetism", "quantum", "field_theory", "relativity", "information",
           "calibration"}


@dataclass
class Variable:
    name: str
    quantity: str                      # key into vocab/resistance_lexicon.yaml
    carries_distance: bool = False     # the variable is a separation between two locations
    dimensionless: bool = False


@dataclass
class Cost:
    """One cost or limit claim, counted the way the book counts (C0)."""
    what_gets_harder: str
    rises_with: list[str] = field(default_factory=list)   # quantity keys
    falls_with: list[str] = field(default_factory=list)   # quantity keys the difficulty falls with
    separation_made_by_distance: bool = False


@dataclass
class Ruling:
    shape: str | None                  # None = pending author
    words: str = ""
    source: str = ""
    reading_note: str = ""


@dataclass
class Alternate:
    statement: str
    form: str
    formula: str = ""
    costs: list[Cost] = field(default_factory=list)
    note: str = ""
    joint: str = "form_call"     # the open joint a disagreement between forms is logged under


@dataclass
class Relation:
    id: str
    domain: str
    title: str
    statement: str
    form: str
    formula: str = ""
    variables: list[Variable] = field(default_factory=list)
    costs: list[Cost] = field(default_factory=list)
    distance_dependence: bool = False
    derived_from: list[str] = field(default_factory=list)
    derivation: str = ""
    alternate_statements: list[Alternate] = field(default_factory=list)
    standard_sources: list[str] = field(default_factory=list)
    book_status: str = "unreflected"
    ruling: Ruling | None = None
    depends_on: list[str] = field(default_factory=list)
    monotone_claims: list[dict] = field(default_factory=list)
    physical_terms: dict[str, str] = field(default_factory=dict)  # formula token -> frozen physical word
    review: str = "pending"            # pending | reviewed:<who>
    notes: str = ""
    path: str = ""

    # ---- helpers -------------------------------------------------------
    def to_dict(self) -> dict:
        d = asdict(self)
        d.pop("path", None)
        return d

    def digest(self) -> str:
        return hashlib.sha256(json.dumps(self.to_dict(), sort_keys=True).encode()).hexdigest()[:12]


def _cost(d: dict) -> Cost:
    return Cost(what_gets_harder=d["what_gets_harder"],
                rises_with=list(d.get("rises_with", []) or []),
                falls_with=list(d.get("falls_with", []) or []),
                separation_made_by_distance=bool(d.get("separation_made_by_distance", False)))


def from_dict(d: dict, path: str = "") -> Relation:
    ruling = None
    if d.get("ruling") is not None:
        r = d["ruling"]
        ruling = Ruling(shape=r.get("shape"), words=r.get("words", ""),
                        source=r.get("source", ""), reading_note=r.get("reading_note", ""))
    return Relation(
        id=d["id"], domain=d["domain"], title=d.get("title", d["id"]),
        statement=d["statement"], form=d["form"], formula=d.get("formula", "") or "",
        variables=[Variable(name=v["name"], quantity=v.get("quantity", v["name"]),
                            carries_distance=bool(v.get("carries_distance", False)),
                            dimensionless=bool(v.get("dimensionless", False)))
                   for v in d.get("variables", []) or []],
        costs=[_cost(c) for c in (d.get("costs") or [])],
        distance_dependence=bool(d.get("distance_dependence", False)),
        derived_from=list(d.get("derived_from", []) or []),
        derivation=d.get("derivation", "") or "",
        alternate_statements=[Alternate(statement=a["statement"], form=a["form"],
                                        formula=a.get("formula", "") or "",
                                        costs=[_cost(c) for c in (a.get("costs") or [])],
                                        note=a.get("note", "") or "", joint=a.get("joint", "form_call") or "form_call")
                              for a in d.get("alternate_statements", []) or []],
        standard_sources=list(d.get("standard_sources", []) or []),
        book_status=d.get("book_status", "unreflected"),
        ruling=ruling,
        depends_on=list(d.get("depends_on", []) or []),
        monotone_claims=list(d.get("monotone_claims", []) or []),
        physical_terms=dict(d.get("physical_terms", {}) or {}),
        review=d.get("review", "pending") or "pending",
        notes=d.get("notes", "") or "",
        path=path,
    )


def load_record(path: Path) -> Relation:
    with open(path) as f:
        d = yaml.safe_load(f)
    return from_dict(d, str(path))


def load_corpus(root: Path, domains: Iterable[str] | None = None) -> list[Relation]:
    recs = []
    for p in sorted(root.rglob("*.yaml")):
        r = load_record(p)
        if domains and r.domain not in domains and p.parent.name not in domains:
            continue
        recs.append(r)
    ids = [r.id for r in recs]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"duplicate record ids: {sorted(dupes)}")
    return recs


def validate(rec: Relation, lexicon: dict[str, Any], identity_forms: set[str]) -> list[str]:
    """Return a list of schema problems. Empty list = valid."""
    errs = []
    if rec.form not in FORMS:
        errs.append(f"{rec.id}: unknown form {rec.form!r}")
    if rec.book_status not in BOOK_STATUS:
        errs.append(f"{rec.id}: unknown book_status {rec.book_status!r}")
    if rec.domain not in DOMAINS:
        errs.append(f"{rec.id}: unknown domain {rec.domain!r}")
    if rec.book_status == "ruled" and rec.ruling is None:
        errs.append(f"{rec.id}: ruled but no ruling block")
    if rec.ruling and rec.ruling.shape is not None and rec.ruling.shape not in SHAPES:
        errs.append(f"{rec.id}: ruling.shape {rec.ruling.shape!r} not in {sorted(SHAPES)}")
    if rec.form in identity_forms and rec.costs:
        errs.append(f"{rec.id}: identity form {rec.form!r} with a cost block; split into two records (C1)")
    qkeys = {v.quantity for v in rec.variables}
    for c in rec.costs:
        for q in c.rises_with + c.falls_with:
            if q not in lexicon:
                errs.append(f"{rec.id}: cost quantity {q!r} not in resistance lexicon")
            if q not in qkeys:
                errs.append(f"{rec.id}: cost quantity {q!r} is not a declared variable")
        if not c.rises_with and not c.falls_with and not c.separation_made_by_distance:
            errs.append(f"{rec.id}: cost block with neither rises_with nor separation")
    for v in rec.variables:
        if v.quantity not in lexicon:
            errs.append(f"{rec.id}: variable quantity {v.quantity!r} not in resistance lexicon")
    for a in rec.alternate_statements:
        if a.form not in FORMS:
            errs.append(f"{rec.id}: alternate form {a.form!r} unknown")
        if a.form in identity_forms and a.costs:
            errs.append(f"{rec.id}: alternate identity form with cost block")
    return errs
