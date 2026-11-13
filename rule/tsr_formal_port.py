"""
tsr_formal_port.py - Direct port of tests/tsr_formal.py into rule/ (Phase 0).

Preserves the exact data structures and checks of tests/tsr_formal.py while
making them importable by the TSR Rule Runner pipeline and Layer A collision checks.
"""
from __future__ import annotations

from collections import defaultdict
from vocab.mirror import MIRROR, DIAGONAL, check_mirror_twice, word_map

ROWS: list[tuple[str, str, bool, bool, int, str]] = [
    # name, book ruling, has_mass, definition, costs, source
    ("1 laws same for every observer", "keep", False, True, 0, "Ch16 #1"),
    ("2 no shared now (distance)", "invert", False, False, 1, "Ch16 #2: distance is what resistance makes"),
    ("3 no fixed frame", "keep", False, True, 0, "Ch16 #3"),
    ("4 special vs general", "keep", False, True, 0, "Ch16 #4"),
    ("5 time dilation", "keep", False, False, 0, "Ch16 #5, #16 opening: no mass in it"),
    ("6 length contraction", "keep", False, False, 0, "Ch16 #6"),
    ("7 E = mc^2", "keep", True, True, 0, "Ch16 #7: an equivalence"),
    ("8 cost of more speed", "invert", True, False, 1, "Ch16 #8: a cost that rises with resistance"),
    ("9 mass can't reach c", "invert", True, False, 1, "Ch16 #9: inverted, because mass is in it"),
    ("10 space-time one continuum", "keep", False, True, 0, "Ch16 #10"),
    ("11 mass-energy warps space-time", "keep", True, False, 0, "Ch16 #11 + Ch16 gravity call (open)"),
    ("12 wells and lensing", "keep", True, False, 0, "Ch16 #12"),
    ("conservation", "keep", False, True, 0, "Ch16: an identity, so it keeps its shape"),
    ("Newton's third law", "keep", False, True, 0, "Ch16: an identity too"),
    ("m = density x volume", "keep", True, True, 0, "Ch2 / Map: Movement = Desire x Vibrance  [definition: JUDGMENT]"),
    ("F = ma", "keep", True, True, 0, "Ch2 / Map: Frequency = Movement x Appreciation  [definition: JUDGMENT]"),
    ("Boyle: squeeze volume, pressure climbs", "keep", True, False, 0, "Ch16 Boyle passage"),
]


def wording_ch2(r: tuple[str, str, bool, bool, int, str]) -> str:
    name, ruling, has_mass, definition, costs, src = r
    if definition:
        return "keep"
    return "invert" if has_mass else "keep"


def wording_ch2_literal(r: tuple[str, str, bool, bool, int, str]) -> str:
    name, ruling, has_mass, definition, costs, src = r
    return "invert" if has_mass else "keep"


def wording_ch16(r: tuple[str, str, bool, bool, int, str]) -> str:
    """
    Corrected Ch 16 rule (Step 2 parity resolution):
    The reading turns iff the relation contains at least one resistance-caused cost (costs >= 1);
    the formula always carries.
    Parity (costs % 2 == 1) was an over-specification in the formalization, exposed by tunneling,
    dispersion, virtual particles and work; the author's October ruling on work already decided it.
    """
    name, ruling, has_mass, definition, costs, src = r
    return "invert" if costs >= 1 else "keep"


def check_rule() -> dict[str, list[tuple[str, str, str]]]:
    out: dict[str, list[tuple[str, str, str]]] = {}
    for label, f in [
        ("Ch 2, first clause read literally", wording_ch2_literal),
        ("Ch 2, both clauses", wording_ch2),
        ("Ch 16, cost vs equivalence", wording_ch16),
    ]:
        misses = [(r[0], r[1], f(r)) for r in ROWS if f(r) != r[1]]
        out[label] = misses
    return out


PHYS: dict[str, tuple[str, tuple[str, ...]]] = {
    "velocity": ("quotient", ("space", "time")),
    "acceleration": ("rate", ("velocity", "time")),
    "mass m": ("product", ("density", "volume")),
    "force": ("product", ("mass m", "acceleration")),
    "physical energy": ("product", ("mass m", "speed of light c", "speed of light c")),
}

NONPHYS_STATED: dict[str, tuple[str, tuple[str, ...]]] = {
    "rise per Expansion": ("quotient", ("Vibration", "Expansion")),
    "Appreciation": ("rate", ("rise per Expansion", "Expansion")),
    "Movement M": ("product", ("Desire", "Vibrance")),
    "Frequency": ("product", ("Movement M", "Appreciation")),
    "conscious energy": ("product", ("Movement M", "Current", "Current")),
}

EXTENSION: dict[str, tuple[str, tuple[str, ...]]] = {
    "momentum": ("product", ("mass m", "velocity")),
    "work": ("product", ("force", "space")),
    "power": ("product", ("force", "velocity")),
    "kinetic energy": ("half product", ("mass m", "velocity", "velocity")),
    "impulse": ("product", ("force", "time")),
    "weight": ("product", ("mass m", "gravitational pull")),
}


def check_composition():
    w = word_map(include_extended=False)
    w["gravitational pull"] = "Attraction"
    results = []
    for q, (op, ins) in PHYS.items():
        image = (op, tuple(w[i] for i in ins))
        stated = NONPHYS_STATED.get(w[q])
        results.append((q, w[q], op, image, stated, stated == image))
    ext = []
    for q, (op, ins) in EXTENSION.items():
        ext.append((q, op, tuple(w.get(i, "?" + i) for i in ins)))
    return results, ext


def sign_mul(a, b):
    if "?" in (a, b):
        return "?"
    if 0 in (a, b):
        return 0
    return a * b


def sign_add(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    if a == b:
        return a
    return "?"


def qualitative_check():
    dM, dA = +1, +1
    prod = sign_add(sign_mul(+1, dM), sign_mul(+1, dA))
    ratio = sign_add(sign_mul(+1, dA), sign_mul(-1, dM))
    return {"product M x A": prod, "ratio A / M": ratio}


CURRENT_REQS = ["a flow", "collects", "means the present moment"]
CURRENT_CANDIDATES = {
    "Current": (1, 1, 1),
    "Source": (0, 0, 0),
    "God": (0, 0, 0),
    "field": (0, 0, 0),
    "flow": (1, 0, 0),
    "stream": (1, 1, 0),
    "tide": (1, 1, 0),
    "Now": (0, 0, 1),
    "present": (0, 0, 1),
    "Relation": (0, 0, 0),
    "Resonance": (0, 0, 0),
}


def constraint_count():
    full = [w for w, v in CURRENT_CANDIDATES.items() if all(v)]
    partial = {w: sum(v) for w, v in CURRENT_CANDIDATES.items()}
    return full, partial
