"""
tsr_formal.py - a first formal model of TSR's table, with checks.

Everything in DATA comes from the final text of The Sovereign Mirror (October 2026):
the Map's reference table and reflected partnerships, Chapter 2's rule,
Chapter 8's falling-man passage, and Chapter 16's twelve reflections.
Where a classification is a judgment rather than a quotation, it is marked
JUDGMENT so anyone can dispute that one cell.

Run:  python3 tsr_formal.py
"""
from collections import defaultdict
from itertools import product

# --------------------------------------------------------------------------
# 1. THE OLOG: types on each side, and the straight mirror between them
#    (role = the Map row the pairing comes from)
# --------------------------------------------------------------------------
MIRROR = [  # (physical, nonphysical, role)
    ("limited", "limitless", "property"),
    ("resistant", "receptive", "property"),
    ("radiation", "collection", "property"),
    ("Subjective Reality", "Vibrational Reality", "reality"),
    ("Objective Reality", "Collective Reality", "reality"),
    ("Space-Time", "Vibration-Expansion", "continuum"),
    ("empirical evidence", "emotional evidence", "evidence"),
    ("Now", "Future", "energy flow"),
    ("Past", "Current", "energy flow"),
    ("Belief", "Desire", "entity contrast"),
    ("Expectation", "Intuition", "entity contrast"),
    ("speed of light c", "Current", "symbol"),
    ("mass m", "Movement M", "symbol"),
    ("Focus", "Tune", "entity action"),
    ("electric", "Idle", "co-creating partner"),
    ("magnetic", "Reflected", "co-creating partner"),
    ("density", "Desire", "co-creating partner"),
    ("volume", "Vibrance", "co-creating partner"),
    ("physical energy", "conscious energy", "energy"),
    ("actualization", "realization", "transmutation"),
    ("Out Through", "Out For", "entity transmutation"),
    ("In From", "In To", "entity transmutation"),
    ("space", "Vibration", "reflected partnership"),
    ("time", "Expansion", "reflected partnership"),
    ("velocity", "rise per Expansion", "reflected partnership"),
    ("acceleration", "Appreciation", "reflected partnership"),
    ("manifestation", "imagination", "reflected partnership"),
    ("force", "Frequency", "reflected partnership"),
]
DIAGONAL = [  # the second symmetry, through the center (Map, Core interactions)
    ("strong force: Expectation", "strong frequency: Desire"),
    ("weak force: Belief", "weak frequency: Intuition"),
]


def check_mirror_twice():
    """A mirror applied twice should return the original: the word map must be one-to-one."""
    back = defaultdict(set)
    fwd = defaultdict(set)
    for phys, non, role in MIRROR:
        back[non].add((phys, role))
        fwd[phys].add(non)
    many_to_one = {n: sorted(p) for n, p in back.items() if len(p) > 1}
    one_to_many = {p: sorted(n) for p, n in fwd.items() if len(n) > 1}
    # typed by role, is it one-to-one?
    typed = defaultdict(set)
    for phys, non, role in MIRROR:
        typed[(non, role)].add(phys)
    typed_clash = {k: v for k, v in typed.items() if len(v) > 1}
    return many_to_one, one_to_many, typed_clash


# --------------------------------------------------------------------------
# 2. THE RULE: which rows keep their shape and which turn around
#    Each row: the book's ruling + features used by the candidate wordings.
#    has_mass: mass (resistance) appears in the physical statement
#    definition: an equivalence, definition, identity or conservation law
#    costs: number of resistance-caused costs or limits in the statement
#           (difficulty that rises with mass, or separation made by distance)
# --------------------------------------------------------------------------
ROWS = [
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


def wording_ch2(r):
    # "If it depends on resistance, so that more mass means more of something,
    #  ... turns it around. If it's an identity, ... keeps its shape."
    name, ruling, has_mass, definition, costs, src = r
    if definition:
        return "keep"
    return "invert" if has_mass else "keep"


def wording_ch2_literal(r):
    # the first clause alone, read literally: any row with mass in it turns around
    name, ruling, has_mass, definition, costs, src = r
    return "invert" if has_mass else "keep"


def wording_ch16(r):
    # "One is an equivalence. The other is a cost that rises with resistance."
    # sharpened: turn around iff an odd number of resistance-caused costs/limits
    name, ruling, has_mass, definition, costs, src = r
    return "invert" if costs % 2 == 1 else "keep"


def check_rule():
    out = {}
    for label, f in [("Ch 2, first clause read literally", wording_ch2_literal),
                     ("Ch 2, both clauses", wording_ch2),
                     ("Ch 16, cost vs equivalence", wording_ch16)]:
        misses = [(r[0], r[1], f(r)) for r in ROWS if f(r) != r[1]]
        out[label] = misses
    return out


# --------------------------------------------------------------------------
# 3. COMPOSITION: reflected relations must compose the way physical ones do
#    (a functor preserves composites). Products kept on both sides.
# --------------------------------------------------------------------------
PHYS = {  # quantity: (operation, inputs)
    "velocity": ("quotient", ("space", "time")),
    "acceleration": ("rate", ("velocity", "time")),
    "mass m": ("product", ("density", "volume")),
    "force": ("product", ("mass m", "acceleration")),
    "physical energy": ("product", ("mass m", "speed of light c", "speed of light c")),
}
NONPHYS_STATED = {
    "rise per Expansion": ("quotient", ("Vibration", "Expansion")),
    "Appreciation": ("rate", ("rise per Expansion", "Expansion")),
    "Movement M": ("product", ("Desire", "Vibrance")),
    "Frequency": ("product", ("Movement M", "Appreciation")),
    "conscious energy": ("product", ("Movement M", "Current", "Current")),
}
# unstated physical relations to push through the map (the extension test)
EXTENSION = {
    "momentum": ("product", ("mass m", "velocity")),
    "work": ("product", ("force", "space")),
    "power": ("product", ("force", "velocity")),
    "kinetic energy": ("half product", ("mass m", "velocity", "velocity")),
    "impulse": ("product", ("force", "time")),
    "weight": ("product", ("mass m", "gravitational pull")),
}


def word_map():
    m = {}
    for phys, non, role in MIRROR:
        m.setdefault(phys, non)  # first (straight-mirror) partner
    m["gravitational pull"] = "Attraction"    # Ch 8: gravity reflects as Attraction
    return m


def check_composition():
    w = word_map()
    results = []
    for q, (op, ins) in PHYS.items():
        image = (op, tuple(w[i] for i in ins))
        stated = NONPHYS_STATED.get(w[q])
        results.append((q, w[q], op, image, stated, stated == image))
    ext = []
    for q, (op, ins) in EXTENSION.items():
        ext.append((q, op, tuple(w.get(i, "?" + i) for i in ins)))
    return results, ext


# --------------------------------------------------------------------------
# 4. QUALITATIVE MODEL: signs instead of numbers
#    Book claims about the falling man and alignment (Ch 1, 2, 8, Ch16 #8):
#      Movement rises with alignment ("the more receptive you become")
#      Appreciation rises with alignment ("full in free fall, low while you hold")
#      Claim O1: Frequency rises with alignment ("you feel that in your frequency")
#      Claim O2: holding on (low alignment) reads low and heavy; free fall reads ease
#    Compare the book's product form with the critic's ratio form.
# --------------------------------------------------------------------------
def sign_mul(a, b):
    if "?" in (a, b): return "?"
    if 0 in (a, b): return 0
    return a * b


def sign_add(a, b):
    if a == 0: return b
    if b == 0: return a
    if a == b: return a
    return "?"  # opposite signs: ambiguous without magnitudes


def qualitative_check():
    dM, dA = +1, +1          # d/d(alignment) of Movement and Appreciation
    # product F = M*A: dF = A dM + M dA, with A, M > 0
    prod = sign_add(sign_mul(+1, dM), sign_mul(+1, dA))
    # ratio F = A/M: dF = dA/M - A dM/M^2
    ratio = sign_add(sign_mul(+1, dA), sign_mul(-1, dM))
    return {"product M x A": prod, "ratio A / M": ratio}


# --------------------------------------------------------------------------
# 5. CONSTRAINT COUNT (harness): how many words satisfy a slot's requirements?
#    Requirements are the book's own words (Ch16): "A replacement has to be
#    the flow, the collecting and the present moment, all at once."
#    The yes/no cells are JUDGMENTS from ordinary dictionary senses, there to
#    be disputed. The count is only as good as these cells.
# --------------------------------------------------------------------------
CURRENT_REQS = ["a flow", "collects", "means the present moment"]
CURRENT_CANDIDATES = {
    # word: (flow, collects, present moment)
    "Current": (1, 1, 1),   # current of a river; a current carries and gathers; "current" = now
    "Source":  (0, 0, 0),   # Ch16: pours outward from a point, the radiating property
    "God":     (0, 0, 0),   # Ch16: brings in a being above you
    "field":   (0, 0, 0),   # Ch16: loses the flow and the present moment
    "flow":    (1, 0, 0),
    "stream":  (1, 1, 0),   # a stream gathers its tributaries; no sense of "now"
    "tide":    (1, 1, 0),
    "Now":     (0, 0, 1),   # taken: the physical present in the four directions
    "present": (0, 0, 1),
    "Relation":  (0, 0, 0), # critic's alternative, offered for space; listed for the harness
    "Resonance": (0, 0, 0),
}


def constraint_count():
    full = [w for w, v in CURRENT_CANDIDATES.items() if all(v)]
    partial = {w: sum(v) for w, v in CURRENT_CANDIDATES.items()}
    return full, partial


if __name__ == "__main__":
    print("== 1. Mirror twice (one-to-one?) ==")
    m2o, o2m, typed = check_mirror_twice()
    for k, v in m2o.items():
        print(f"  {k!r} has {len(v)} physical partners: {v}")
    print("  physical words with more than one reflection:", o2m or "none")
    print("  clashes once each pairing is typed by its Map row:", typed or "none")

    print("\n== 2. The rule against the book's own rulings ==")
    for label, misses in check_rule().items():
        print(f"  {label}: {len(ROWS) - len(misses)}/{len(ROWS)} rows match")
        for name, book, pred in misses:
            print(f"     miss: {name}: book says {book}, wording predicts {pred}")

    print("\n== 3. Composition ==")
    res, ext = check_composition()
    for q, img, op, image, stated, ok in res:
        print(f"  {q} -> {img}: {'commutes' if ok else 'MISMATCH'}  {image}")
    print("  extension test (relations the book does not reflect):")
    for q, op, ins in ext:
        print(f"     {q} = {op} of {ins}")

    print("\n== 4. Qualitative check: does Frequency rise with alignment? ==")
    for form, s in qualitative_check().items():
        print(f"  {form}: sign = {s}")

    print("\n== 5. Constraint count for the Current's slot ==")
    full, partial = constraint_count()
    print(f"  words meeting all {len(CURRENT_REQS)} requirements: {full}")
    print(f"  requirements met by each candidate: {partial}")
