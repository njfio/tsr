"""Collision detection on forced rows (spec section 7).

Layer A: formal (mirror-twice, composition, sign graph, parity).
Layer B: claim-level, two blind judges on every pair of forced rows and every forced row against the book's rulings.
Layer C: book-text check by retrieval over a local text of the paperback.
Break report: surviving collisions with derivation chains and the minimal dissolving change.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from itertools import combinations
from pathlib import Path

from .schema import Relation
from .vocab import Vocab, ROOT
from .formal import composition_check, sign_graph_check, parity_check, mirror_twice_check
from .generate import vocab_table, parse_json, _tmpl
from .providers import LoggedModel


@dataclass
class Collision:
    layer: str                 # A1 | A2 | A3 | A4 | B
    rows: list[str]
    detail: dict
    status: str = "candidate"  # candidate | dissolved_by_judgment | book_resolves | stands
    book_ref: str = ""
    upstream_judgments: list[str] = field(default_factory=list)
    minimal_change: str = ""


# ---------------------------------------------------------------------------
def eligible(rows: list[dict]) -> list[dict]:
    """7.1: only forced rows collide."""
    return [r for r in rows if r.get("candidate_forced")]


def layer_a(forced: list[dict], records: dict[str, Relation], v: Vocab) -> list[Collision]:
    out: list[Collision] = []
    # A1 mirror twice: new (physical, nonphysical, role) pairings implied by forced rows
    new_rows = []
    for r in forced:
        c = r["consensus"]
        rec = records[r["record_id"]]
        if c.get("reflected_formula") and "=" in c["reflected_formula"] and rec.formula and c.get("formula_reflected", True):
            lhs_non = c["reflected_formula"].split("=")[0].strip()
            lhs_phys = rec.physical_terms.get(rec.formula.split("=")[0].strip(), rec.formula.split("=")[0].strip())
            if lhs_phys not in v.word_map():
                new_rows.append((lhs_phys, lhs_non, "reflected partnership"))
    m2 = mirror_twice_check(v, new_rows)
    for k, phys in m2["new_typed_clashes"].items():
        out.append(Collision("A1", [r["record_id"] for r in forced if any(p in r["consensus"].get("reflected_formula", "") for p in phys)],
                             {"nonphysical": k[0], "role": k[1], "physical": phys}))
    # A2 composition
    for r in forced:
        rec = records[r["record_id"]]
        c = r["consensus"]
        if rec.formula and rec.physical_terms and c.get("reflected_formula") and c.get("formula_reflected", True):
            res = composition_check(rec.formula, rec.physical_terms, c["reflected_formula"], v)
            if res.get("ok") is False:
                out.append(Collision("A2", [rec.id], res))
    # A3 sign graph: book claims + forced rows' monotone claims
    claims = list(BOOK_SIGN_CLAIMS)
    for r in forced:
        for mc in r["consensus"].get("monotone_claims", []):
            if {"rises", "with", "sign"} <= set(mc):
                claims.append({**mc, "source": r["record_id"]})
    sg = sign_graph_check(claims)
    for k, v_ in sg["opposite_sign_pairs"].items():
        out.append(Collision("A3", sorted({src for _, src in v_}), {"pair": k, "edges": v_}))
    seen = set()
    for u in sg["unbalanced"]:
        key = tuple(sorted(u["edge"]))
        if key in seen or key in sg["opposite_sign_pairs"]:
            continue
        seen.add(key)
        out.append(Collision("A3", [u["source"]], {"unbalanced_cycle_through": u["edge"], "sign": u["sign"]}))
    # A4 parity along derivation chains (formula level = collision; reading level = informational)
    shapes_formula = {r["record_id"]: "keeps" for r in forced}  # C1: formulas are never rewritten
    shapes_reading = {r["record_id"]: r["consensus"]["shape"] for r in forced}
    for rid, rec in records.items():
        if rec.ruling and rec.ruling.shape:
            shapes_reading.setdefault(rid, rec.ruling.shape)
            shapes_formula.setdefault(rid, "keeps")
    chains = {rid: rec.derived_from for rid, rec in records.items() if rec.derived_from}
    for f in parity_check(shapes_formula, chains, "formula"):
        out.append(Collision("A4", [f["child"], *f["parents"]], f))
    for f in parity_check(shapes_reading, chains, "reading"):
        out.append(Collision("A4-reading", [f["child"], *f["parents"]], {**f, "note": "informational: reading parity is not compositional by the book's own row 8"},
                             status="informational"))
    return out


# the book's own monotone claims (tests/tsr_formal.py section 4)
BOOK_SIGN_CLAIMS = [
    {"rises": "Movement M", "with": "alignment", "sign": 1, "source": "book: Ch 1/2 'the more receptive you become'"},
    {"rises": "Appreciation", "with": "alignment", "sign": 1, "source": "book: Ch 8 'full in free fall, low while you hold'"},
    {"rises": "Frequency", "with": "alignment", "sign": 1, "source": "book: Ch 16 #8 'you feel that in your frequency'"},
    {"rises": "the gap", "with": "alignment", "sign": -1, "source": "book: Ch 16 Expansion Dilation"},
]


# ---------------------------------------------------------------------------
def book_claim_sentences(records: dict[str, Relation]) -> list[dict]:
    out = []
    for rid, rec in records.items():
        if rec.ruling and rec.ruling.shape and rec.ruling.words:
            out.append({"record_id": rid, "sentence": rec.ruling.words, "shape": rec.ruling.shape, "book": True})
    return out


def layer_b(forced: list[dict], records: dict[str, Relation], judges: list[LoggedModel], v: Vocab,
            include_book: bool = True) -> list[Collision]:
    """Two judges, blind to which rows are new. A pair is a candidate collision when both return
    'contradiction' with the same situation (same up to case and punctuation)."""
    items = [{"record_id": r["record_id"], "sentence": r["consensus"]["reflected_sentence"], "book": False} for r in forced]
    if include_book:
        items += book_claim_sentences(records)
    vt = vocab_table(v)
    out = []
    for a, b in combinations(items, 2):
        if a["book"] and b["book"]:
            continue  # the book against itself is not this system's job
        verdicts = []
        for j in judges:
            # alternate order per judge so neither position is privileged
            x, y = (a, b) if len(verdicts) % 2 == 0 else (b, a)
            prompt = _tmpl("judge.md").format(vocab_table=vt, a=x["sentence"], b=y["sentence"])
            try:
                o = parse_json(j(prompt, role="judge", temperature=0.0)) or {}
            except RuntimeError as e:
                o = {"verdict": "error", "situation": str(e)}
            verdicts.append({"judge": j.spec.name, **o})
        if len(verdicts) >= 2 and all(vd.get("verdict") == "contradiction" for vd in verdicts):
            sits = {re.sub(r"[^a-z ]", "", (vd.get("situation") or "").lower()).strip() for vd in verdicts}
            same = len(sits) == 1
            out.append(Collision("B", [a["record_id"], b["record_id"]],
                                 {"verdicts": verdicts, "same_situation": same, "a": a["sentence"], "b": b["sentence"]},
                                 status="candidate" if same else "judges_disagree_on_situation"))
    return out


# ---------------------------------------------------------------------------
class BookIndex:
    """Minimal retrieval over a local plain-text copy of the paperback (not in the repo).

    Format: lines; a line matching '^## Chapter' or '^\\[p\\. ?\\d+\\]' sets the current chapter / page.
    """
    def __init__(self, path: Path | None):
        self.chunks: list[tuple[str, str, str]] = []  # (chapter, page, text)
        if path and Path(path).exists():
            ch, pg, buf = "", "", []
            for line in Path(path).read_text().splitlines():
                m = re.match(r"^\s*(?:##\s*)?(Chapter\s+\d+[^\n]*)", line)
                p = re.match(r"^\s*\[p\.?\s*(\d+)\]", line)
                if m or p:
                    if buf:
                        self.chunks.append((ch, pg, " ".join(buf)))
                        buf = []
                    if m:
                        ch = m.group(1).strip()
                    if p:
                        pg = p.group(1)
                    continue
                if line.strip():
                    buf.append(line.strip())
                if len(buf) >= 6:
                    self.chunks.append((ch, pg, " ".join(buf)))
                    buf = []
            if buf:
                self.chunks.append((ch, pg, " ".join(buf)))

    def search(self, query: str, k: int = 3) -> list[dict]:
        if not self.chunks:
            return []
        q = {w for w in re.findall(r"[a-z]{4,}", query.lower())}
        scored = []
        for ch, pg, text in self.chunks:
            t = set(re.findall(r"[a-z]{4,}", text.lower()))
            s = len(q & t) / (len(q) or 1)
            if s > 0:
                scored.append((s, ch, pg, text))
        scored.sort(reverse=True)
        return [{"score": round(s, 2), "chapter": ch, "page": pg, "text": t[:2000]} for s, ch, pg, t in scored[:k]]


def layer_c(cands: list[Collision], book: BookIndex, resolver: LoggedModel | None, v: Vocab) -> list[Collision]:
    """If the book already states the resolution, downgrade to a documentation gap."""
    for c in cands:
        if c.status != "candidate":
            continue
        q = " ".join(str(x) for x in c.detail.values())[:600]
        hits = book.search(q)
        c.detail["book_hits"] = hits
        if not hits:
            c.status = "stands (book text not available or silent)"
            continue
        if resolver is None:
            c.status = "stands (book hits recorded; no resolver run)"
            continue
        prompt = ("ROLE: judge\n\nTwo sentences read as a contradiction. Below are passages from a book. Does any passage state "
                  "a resolution that makes both sentences true at once, or is one of the sentences itself the book's own claim?\n\n"
                  f"A: {c.detail.get('a','')}\nB: {c.detail.get('b','')}\n\nPassages:\n" +
                  "\n".join(f"[{h['chapter']} p.{h['page']}] {h['text']}" for h in hits) +
                  '\n\nReturn JSON: {"verdict": "resolves | silent | one_side", "where": "chapter/page", "situation": ""}')
        try:
            o = parse_json(resolver(prompt, role="layer-c", temperature=0.0)) or {}
        except RuntimeError as e:
            o = {"verdict": "error", "where": str(e)}
        if o.get("verdict") == "resolves":
            c.status, c.book_ref = "book_resolves", o.get("where", "")
        else:
            c.status = "stands"
            c.book_ref = o.get("where", "")
    return cands


# ---------------------------------------------------------------------------
def break_report(cands: list[Collision], rows: dict[str, dict], records: dict[str, Relation]) -> list[dict]:
    """7.3: a break is a surviving collision between forced rows, with chains and the minimal dissolving change."""
    out = []
    for c in cands:
        if not c.status.startswith("stands"):
            continue
        chains = []
        for rid in c.rows:
            r = rows.get(rid)
            rec = records.get(rid)
            if not r or not rec:
                chains.append({"record": rid, "note": "book ruling" if rec and rec.ruling else "unknown"})
                continue
            d = r["decision"]
            chains.append({"record": rid, "statement": rec.statement, "form": rec.form,
                           "features": d["features"], "criteria": d["rule_trace"], "shape": r["consensus"]["shape"],
                           "words": r["consensus"]["reflected_sentence"]})
        upstream = sorted({j for rid in c.rows for j in (records[rid].depends_on if rid in records else [])})
        und = sorted({u for rid in c.rows if rid in rows for u in rows[rid]["decision"]["features"]["undetermined"]})
        minimal = _minimal_change(c, rows, records)
        out.append({"layer": c.layer, "rows": c.rows, "failing_check": c.detail, "chains": chains,
                    "upstream_judgment_calls": upstream + und,
                    "is_break": not (upstream or und),
                    "minimal_change_to_dissolve": minimal, "book_ref": c.book_ref})
    return out


def _minimal_change(c: Collision, rows: dict[str, dict], records: dict[str, Relation]) -> str:
    if c.layer == "A2":
        return "accept a rewritten formula for turned rows (gives up C1: 'the formula is never rewritten')"
    if c.layer == "A3":
        return "drop one of the two monotone claims, or make the relation between them non-monotone (gives up the qualitative model of section 4 of tsr_formal.py)"
    if c.layer == "A4":
        return "give up compositionality of formula shape along derivation chains"
    if c.layer == "A1":
        return "give the nonphysical word a second typed role (as the book does for Current and Desire)"
    if c.layer == "B":
        quantities = sorted({q for rid in c.rows if rid in rows for cd in rows[rid]["decision"]["features"]["cost_detail"] for q in cd["resistance_carriers"]})
        if quantities:
            return f"change the resistance verdict for one of {quantities} in R1 (reruns every domain that uses it)"
        return "reclassify one record's form (definition ↔ equation), which C6 would then log as a form_call"
    return ""
