"""Layer A: formal collision checks (spec 7.2 A), extending tests/tsr_formal.py.

1. mirror-twice (typed one-to-one) with new rows added
2. composition: w(q) = op(w(inputs)) for every reflected formula
3. sign consistency on a graph of monotone claims
4. parity along derivation chains
"""
from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field

from .vocab import Vocab

# ---------------------------------------------------------------------------
# tiny formula algebra: products and quotients of named terms
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Expr:
    num: tuple[str, ...]
    den: tuple[str, ...] = ()

    def canon(self) -> tuple[tuple[str, ...], tuple[str, ...]]:
        return tuple(sorted(self.num)), tuple(sorted(self.den))


# symbols the book itself uses on the nonphysical side
REFLECTED_ALIASES = {"C": "Current", "M": "Movement M", "E": "conscious energy"}

_TOKEN = re.compile(r"\s*(×|x(?=\s)|\*|÷|/|\^2|²|\(|\)|[^\s×*÷/()²]+(?:\s+[^\s×*÷/()²=]+)*?)(?=\s*(?:×|x\s|\*|÷|/|\^2|²|\(|\)|$))")


def _tokenize(side: str, names: dict[str, str] | None) -> list[str]:
    """Split one side of a formula into tokens, keeping multi-word names whole."""
    s = side.strip()
    toks: list[str] = []
    if names:
        for k in sorted(names, key=len, reverse=True):
            s = re.sub(rf"(?<![A-Za-z]){re.escape(k)}(?![A-Za-z])", f" «{k}» ", s)
    for part in re.split(r"(«[^»]*»|×|÷|\*|/|\^2|²|\(|\))", s):
        part = part.strip()
        if not part:
            continue
        if part.startswith("«"):
            toks.append(part[1:-1])
        elif part in {"x"}:
            toks.append("×")
        elif names is not None:
            # physical side with a names dict: anything not a declared name splits into symbols
            toks.extend(part.split())
        else:
            toks.append(part)
    return toks


def parse_side(side: str, names: dict[str, str] | None = None) -> Expr:
    """Parse 'a × b ÷ c²' into Expr(num=(a,b), den=(c,c)). Numerals are dropped (lint catches them)."""
    toks = _tokenize(side, names)
    num, den = [], []
    where = num
    last = None
    for t in toks:
        if t in {"×", "*"}:
            where = num if where is den and False else where  # products keep current side
            continue
        if t in {"÷", "/"}:
            where = den
            continue
        if t in {"^2", "²"}:
            if last is not None:
                where.append(last)
            continue
        if t in {"(", ")", "−", "-", "+"}:
            continue
        if re.fullmatch(r"[\d.,½¼¾√]+", t):
            continue
        name = names.get(t, t) if names else REFLECTED_ALIASES.get(t, t)
        where.append(name)
        last = name
    return Expr(tuple(num), tuple(den))


def parse_formula(formula: str, names: dict[str, str] | None = None) -> tuple[str, Expr] | None:
    if "=" not in formula:
        return None
    lhs, rhs = formula.split("=", 1)
    lhs_t = _tokenize(lhs, names)
    if len(lhs_t) != 1:
        # the book writes the nonphysical side first: C² × M = E
        lhs, rhs = rhs, lhs
        lhs_t = _tokenize(lhs, names)
        if len(lhs_t) != 1:
            return None
    lname = names.get(lhs_t[0], lhs_t[0]) if names else REFLECTED_ALIASES.get(lhs_t[0], lhs_t[0])
    return lname, parse_side(rhs, names)


def image(expr: Expr, w: dict[str, str]) -> Expr:
    return Expr(tuple(w.get(t, "?" + t) for t in expr.num), tuple(w.get(t, "?" + t) for t in expr.den))


# ---------------------------------------------------------------------------
# A.2 composition
# ---------------------------------------------------------------------------
def composition_check(physical_formula: str, physical_terms: dict[str, str],
                      reflected_formula: str, vocab: Vocab,
                      extra_map: dict[str, str] | None = None) -> dict:
    """Does the reflected formula equal the word-map image of the physical one?"""
    w = vocab.word_map()
    if extra_map:
        w.update(extra_map)
    p = parse_formula(physical_formula, physical_terms)
    r = parse_formula(reflected_formula, None)
    if p is None or r is None:
        return {"ok": None, "reason": "unparsed", "physical": physical_formula, "reflected": reflected_formula}
    lname, pexpr = p
    rname, rexpr = r
    img = image(pexpr, w)
    lhs_img = w.get(lname, "?" + lname)
    ok = (img.canon() == rexpr.canon()) and (lhs_img == rname or lhs_img.startswith("?"))
    return {"ok": ok, "lhs_image": lhs_img, "lhs_reflected": rname,
            "rhs_image": img.canon(), "rhs_reflected": rexpr.canon(),
            "unmapped": [t[1:] for t in img.num + img.den if t.startswith("?")]}


# ---------------------------------------------------------------------------
# A.3 sign consistency
# ---------------------------------------------------------------------------
def sign_graph_check(claims: list[dict]) -> dict:
    """claims: [{rises: A, with: B, sign: +1|-1, source: id}]

    Collision if two edges of opposite sign join the same pair, or a cycle has an
    odd number of negative edges (an unbalanced signed graph).
    """
    edges = defaultdict(list)
    adj = defaultdict(list)
    for c in claims:
        a, b, s = c["rises"], c["with"], int(c["sign"])
        key = tuple(sorted((a, b)))
        edges[key].append((s, c.get("source", "?")))
        adj[a].append((b, s, c.get("source", "?")))
        adj[b].append((a, s, c.get("source", "?")))
    opposite = {k: v for k, v in edges.items() if len({s for s, _ in v}) > 1}
    # balance check: 2-color with parity; conflict = unbalanced cycle
    color: dict[str, int] = {}
    unbalanced = []
    for start in adj:
        if start in color:
            continue
        color[start] = 0
        stack = [start]
        while stack:
            u = stack.pop()
            for v, s, src in adj[u]:
                want = color[u] if s > 0 else 1 - color[u]
                if v not in color:
                    color[v] = want
                    stack.append(v)
                elif color[v] != want:
                    unbalanced.append({"edge": (u, v), "sign": s, "source": src})
    return {"opposite_sign_pairs": opposite, "unbalanced": unbalanced,
            "ok": not opposite and not unbalanced, "n_edges": sum(len(v) for v in edges.values())}


# ---------------------------------------------------------------------------
# A.4 parity along derivation chains
# ---------------------------------------------------------------------------
PARITY = {"keeps": 0, "turns around": 1}


def parity_check(shapes: dict[str, str], derived_from: dict[str, list[str]], level: str = "formula") -> list[dict]:
    """For each record derived from others, the parity of the parents must compose to the child's.

    keep∘keep = keep, turn∘turn = keep, keep∘turn = turn.
    Returns the list of chains that fail. At level='reading' a failure is informational:
    the book's own row 8 is built from kept rows and turns (tests/README.md), so reading
    parity is not compositional by the book's own precedent.
    """
    fails = []
    for child, parents in derived_from.items():
        if child not in shapes or any(p not in shapes for p in parents) or not parents:
            continue
        if shapes[child] not in PARITY or any(shapes[p] not in PARITY for p in parents):
            continue
        expect = sum(PARITY[shapes[p]] for p in parents) % 2
        got = PARITY[shapes[child]]
        if expect != got:
            fails.append({"child": child, "parents": parents, "expected": "turns around" if expect else "keeps",
                          "got": shapes[child], "level": level,
                          "collision": level == "formula"})
    return fails


# ---------------------------------------------------------------------------
# A.1 mirror twice with new rows
# ---------------------------------------------------------------------------
def mirror_twice_check(vocab: Vocab, new_rows: list[tuple[str, str, str]]) -> dict:
    base = vocab.typed_clashes()
    with_new = vocab.typed_clashes(new_rows)
    new_clashes = {k: v for k, v in with_new.items() if k not in base}
    return {"baseline_typed_clashes": base, "new_typed_clashes": new_clashes,
            "many_to_one": vocab.many_to_one(new_rows), "ok": not new_clashes}
