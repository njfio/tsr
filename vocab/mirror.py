"""
mirror.py - The locked word map, typed by Map row, ported and extended from tsr_formal.py.

Vocabulary is frozen to tsr_formal.MIRROR plus the Map's reflected partnerships and
glossary senses (The Sovereign Mirror, pp. 167-171).
"""
from __future__ import annotations

from collections import defaultdict
from typing import Iterable

# 1. THE OLOG: types on each side, and the straight mirror between them
#    (role = the Map row the pairing comes from)
MIRROR: list[tuple[str, str, str]] = [
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

DIAGONAL: list[tuple[str, str]] = [
    ("strong force: Expectation", "strong frequency: Desire"),
    ("weak force: Belief", "weak frequency: Intuition"),
]

# Book-stated mappings (Chapter 8, Chapter 16, The Map pp. 167-171) plus ONLY
# the partners explicitly ruled by the author, with the ruling text as the source.
# Run 3 instruction: Revert every vocabulary mapping added in the v2 reconciliation to "no partner".
# Re-add only the ones the author has ruled, with the ruling text as the source.
# The harness may not add partners; it reports "no partner" and the author decides.
AUTHOR_RULING_SOURCES: dict[str, str] = {
    "gravitational pull": "gravity_call: closed, keeps. Energy curves space-time; that curvature is Attraction on the center continuum, seen as gravity with mass in Subjective Reality and as a Movement Vortex in Vibrational Reality. Rows 11 and 12 become forceable. Escape velocity: no reflection (Attraction is not a thing you escape); mark closed-no-partner, not open.",
    "gravity": "gravity_call: closed, keeps. Energy curves space-time; that curvature is Attraction on the center continuum, seen as gravity with mass in Subjective Reality and as a Movement Vortex in Vibrational Reality. Rows 11 and 12 become forceable. Escape velocity: no reflection (Attraction is not a thing you escape); mark closed-no-partner, not open.",
    "gravitational acceleration": "gravity_call: closed, keeps. Energy curves space-time; that curvature is Attraction on the center continuum, seen as gravity with mass in Subjective Reality and as a Movement Vortex in Vibrational Reality. Rows 11 and 12 become forceable.",
    "gravitational field": "gravity_call: closed, keeps. Energy curves space-time; that curvature is Attraction on the center continuum, seen as gravity with mass in Subjective Reality and as a Movement Vortex in Vibrational Reality. Rows 11 and 12 become forceable.",
    "gravity well": "gravity_call: closed, keeps. Energy curves space-time; that curvature is Attraction on the center continuum, seen as gravity with mass in Subjective Reality and as a Movement Vortex in Vibrational Reality. Rows 11 and 12 become forceable.",
    "gravitational lensing": "gravity_call: closed, keeps. The Map p. 169 ('Convergence: The reflection of gravitational lensing') + gravity_call: Rows 11 and 12 become forceable.",
    "rest energy": "rest_energy_call: row 7 (E = C²M) is the rest row; a Movement changing its Vibration adds that term, as physics does.",
    "distance": "separation_call: distance as a falloff or nearness carries across as difference in Vibration (Vortex); distance as a separation or location turns (row 2, interference).",
    "displacement": "separation_call: distance as a falloff or nearness carries across as difference in Vibration (Vortex); distance as a separation or location turns (row 2, interference).",
    "length": "separation_call: distance as a falloff or nearness carries across as difference in Vibration (Vortex); distance as a separation or location turns (row 2, interference).",
    "radius": "separation_call: distance as a falloff or nearness carries across as difference in Vibration (Vortex); distance as a separation or location turns (row 2, interference).",
    "work": "Author's ruling, October 2026 (tsr.wtf/answers, 'Kinetic energy, work, and force'): work formula reflects as Frequency × Vibration (or conscious energy); reading turns.",
    "power": "Author's ruling, October 2026 (tsr.wtf/answers, 'Kinetic energy, work, and force'): power formula reflects as Frequency × rise per Expansion (or conscious energy); reading turns.",
    "kinetic energy": "Author's ruling, October 2026 (tsr.wtf/answers, 'Kinetic energy, work, and force') + The Map p. 169 ('Conscious-kinetic energy').",
}

EXTENDED_PARTNERS: dict[str, str] = {
    "gravitational pull": "Attraction",
    "gravity": "Attraction",
    "gravitational acceleration": "Attraction",
    "gravitational field": "Attraction",
    "gravity well": "Vortex",
    "gravitational lensing": "Convergence",
    "time dilation": "Expansion Dilation",
    "length contraction": "Vibrational Contraction",
    "friction": "resonance",
    "speed of light": "Current",
    "c": "Current",
    "mass": "Movement",
    "m": "Movement M",
    "distance": "Vibration",
    "displacement": "Vibration",
    "length": "Vibration",
    "radius": "Vibration",
    "momentum": "momentum",
    "momentum through time": "Movement M × Current",
    "rest energy": "conscious energy",
    "kinetic energy": "conscious energy",
    "work": "conscious energy",
    "power": "conscious energy",
    "weight": "Frequency",
}

# Typing of extended/canonical physical quantities by their physical quantity type
# so check_mirror_twice() enforces the exact same strictness that produced Young's
# torque/work collision: any two distinct physical quantities of the same type
# mapping to one TSR word is a clash (do not type around them).
EXTENDED_TYPED_ENTRIES: list[tuple[str, str, str]] = [
    ("distance", "Vibration", "reflected partnership"),
    ("displacement", "Vibration", "reflected partnership"),
    ("length", "Vibration", "reflected partnership"),
    ("radius", "Vibration", "reflected partnership"),
    ("time interval", "Expansion", "reflected partnership"),
    ("rest energy", "conscious energy", "energy"),
    ("kinetic energy", "conscious energy", "energy"),
    ("work", "conscious energy", "energy"),
    ("power", "conscious energy", "energy"),
    ("gravity", "Attraction", "gravity"),
    ("gravitational pull", "Attraction", "gravity"),
    ("gravitational field", "Attraction", "gravity"),
    ("gravitational acceleration", "Attraction", "gravity"),
    ("weight", "Frequency", "reflected partnership"),
    ("buoyant force", "Frequency", "reflected partnership"),
    ("centripetal force", "Frequency", "reflected partnership"),
]

# Provisional book readings (cannot force a row on their own without rule closure)
PROVISIONAL_PARTNERS: dict[str, str] = {
    "entropy": "Culmination",
}

# Locked glossary senses from The Map (pp. 169-171)
GLOSSARY_SENSES: dict[str, str] = {
    "Appreciation": (
        "How a Movement's rising changes, its quickening or slowing, how much of "
        "the Current's pull a Movement is letting move it. The reflection of acceleration."
    ),
    "Attraction": (
        "The entity property made of receptive and resistant; how you draw from "
        "the whole what corresponds to you."
    ),
    "Awareness": (
        "Two senses: the whole where everything starts, and the entity property "
        "made of limitless and limited (the whole, aware from somewhere)."
    ),
    "Belief": (
        "What is taken to be true now; energy going Out Through you. The physical "
        "weak force, able to shift in the Now."
    ),
    "Conscious-kinetic energy": "The blend of conscious and kinetic energy at the hinge, the E.",
    "Convergence": (
        "The reflection of gravitational lensing. The Current coming together "
        "through a Vortex, which defines what can be focused and how much."
    ),
    "Current": (
        "The Current of Consciousness: the whole, flowing, always at the furthest "
        "point it has reached; also means the present moment. Idle and reflected; "
        "the reflection of the speed of light c and the Past."
    ),
    "Desire": (
        "What is wanted; how much wanting is packed into a Movement (reflection "
        "of density); the expansion that happens in the nonphysical; energy going Out For you."
    ),
    "Emotional evidence": (
        "Frequency, felt. The level is a feeling; a change in the level is an emotion."
    ),
    "Empirical evidence": "Force, measured: a steady push, or a change in it.",
    "Eternal-Energetic-Entity": "The soul: the continuum where vibrational and subjective realities meet.",
    "Expansion": "The reflection of time. What the Current does, and can't undo.",
    "Expansion Dilation": (
        "The gap between where the Current is and what you're living, widened by "
        "resistance. The reflection of time dilation."
    ),
    "Expectation": (
        "What was true; energy coming In From the world. The physical strong force, "
        "binding your lived history into a shape."
    ),
    "Focus": "Where physical attention and effort go. The reflection of Tune.",
    "Frequency": (
        "Movement times Appreciation; what you feel as a Movement's rising quickens "
        "or slows. Carries no units."
    ),
    "Idle": "The nonphysical partner of electric; with Reflected, makes the Current.",
    "Reflected": "The nonphysical partner of magnetic; with Idle, makes the Current.",
    "Intuition": (
        "What is received; energy coming In To you. The nonphysical weak frequency "
        "arriving at the Point of Reflection."
    ),
    "imagination": (
        "The reflection of manifestation; paired with intuition as the nonphysical "
        "weak frequency."
    ),
    "Momentum": (
        "On each side, what a thing carries through its continuum (mass × velocity "
        "physically, Movement × rise per Expansion nonphysically); at the crossing, "
        "the entity property made of collection and radiation (M × C and m × c)."
    ),
    "Movement": (
        "Receptivity to change in motion; a self-contained part of the whole, like "
        "a movement in a symphony. The reflection of mass."
    ),
    "Movement M": (
        "Symbolic reflection of mass m: receptivity to change in motion."
    ),
    "Point of Reflection": (
        "The crossing at the center where the two sides meet and energy changes form."
    ),
    "Resistance": (
        "Resistance to change; what makes the physical physical. Two kinds: shape "
        "and holding on."
    ),
    "resonance": (
        "Two Movements meeting don't lose to each other; they build each other up "
        "and culminate. Reflection of friction / damping."
    ),
    "rise per Expansion": (
        "Vibration over Expansion; how much a Movement's vibration rises per "
        "Expansion. The reflection of velocity."
    ),
    "Tune": "What you are receptive to. The reflection of Focus.",
    "Vibrance": (
        "A Movement's extent in Vibration: how much of it is vibrating, how ready "
        "it is to vibrate. The reflection of volume."
    ),
    "Vibration": (
        "How particulars differ when there is no distance. The reflection of space."
    ),
    "Vibrational Contraction": (
        "The shrinking of the felt distance between what you want and its arrival, "
        "as you align. The reflection of length contraction."
    ),
    "Vortex": (
        "The reflection of a gravity well. Desire and Vibrance, organized strongly "
        "enough, turning the Current around themselves."
    ),
    "limitless": "Nonphysical property paired with limited.",
    "receptive": "Nonphysical property paired with resistant.",
    "collection": "Nonphysical property paired with radiation.",
    "Vibrational Reality": "Nonphysical reality paired with Subjective Reality.",
    "Collective Reality": "Nonphysical reality paired with Objective Reality.",
    "Vibration-Expansion": "Nonphysical continuum paired with Space-Time.",
    "Future": "Nonphysical energy flow paired with Now.",
    "conscious energy": "Nonphysical energy paired with physical energy.",
    "realization": "Nonphysical transmutation paired with actualization.",
    "Out For": "Nonphysical entity transmutation paired with Out Through.",
    "In To": "Nonphysical entity transmutation paired with In From.",
}


def word_map(include_extended: bool = True) -> dict[str, str]:
    """Return physical -> nonphysical word map."""
    m: dict[str, str] = {}
    for phys, non, _role in MIRROR:
        m.setdefault(phys, non)
    if include_extended:
        for phys, non in EXTENDED_PARTNERS.items():
            m.setdefault(phys, non)
    return m


def typed_word_map() -> dict[tuple[str, str], str]:
    """Return (physical, role) -> nonphysical map."""
    return {(phys, role): non for phys, non, role in MIRROR}


def check_mirror_twice(
    extra_entries: Iterable[tuple[str, str, str]] | None = None,
) -> tuple[dict[str, list[tuple[str, str]]], dict[str, list[str]], dict[tuple[str, str], set[str]]]:
    """
    Check whether the word map is one-to-one with the exact strictness that produced
    Young's torque/work collision: any two distinct physical quantities of the same type
    mapping to one TSR word is a clash.
    Returns (many_to_one, one_to_many, typed_clash).
    """
    if extra_entries is None:
        extra_entries = EXTENDED_TYPED_ENTRIES
    entries = list(MIRROR) + list(extra_entries)
    back: dict[str, set[tuple[str, str]]] = defaultdict(set)
    fwd: dict[str, set[str]] = defaultdict(set)
    typed: dict[tuple[str, str], set[str]] = defaultdict(set)
    for phys, non, role in entries:
        back[non].add((phys, role))
        fwd[phys].add(non)
        typed[(non, role)].add(phys)
    many_to_one = {n: sorted(p) for n, p in back.items() if len(p) > 1}
    one_to_many = {p: sorted(n) for p, n in fwd.items() if len(n) > 1}
    typed_clash = {k: v for k, v in typed.items() if len(v) > 1}
    return many_to_one, one_to_many, typed_clash


def is_stripped_constant(physical_term: str) -> bool:
    """
    Criterion 5.3.5: Numeric/dimensional constants and dimensionless mode indices
    do not cross the mirror (they drop out of the reflected formula rather than
    requiring a new TSR vocabulary word). Note: speed of light c DOES cross as Current.
    """
    lower = physical_term.strip().lower()
    constant_markers = (
        "planck constant",
        "reduced planck constant",
        "boltzmann constant",
        "gravitational constant",
        "vacuum permittivity",
        "vacuum permeability",
        "lorentz factor",
        "principal quantum number",
        "mode integer",
        "infinitesimal contour regulator",
        "levi-civita symbol",
        "critical exponent",
    )
    return any(m in lower for m in constant_markers)


def translate_term(physical_term: str) -> tuple[str | None, bool]:
    """
    Translate a physical variable or term into its frozen TSR partner.
    Returns (partner_or_None, is_mapped).
    """
    w = word_map(include_extended=True)
    cleaned = physical_term.strip()
    if cleaned in w:
        return w[cleaned], True
    lower = cleaned.lower()
    for k, v in w.items():
        if k.lower() == lower:
            return v, True

    # Exclude terms that have no partner in the frozen vocabulary (including all
    # v2 reconciliation mappings reverted in Run 3: viscosity, damping, stiffness,
    # spring constant, impedance, inductance, electrical resistance, reynolds number,
    # yukawa coupling, vacuum expectation value, transmission probability, barrier height,
    # wave intensity, total intensity, phase difference, diffraction angle, plus
    # un-ruled rotational/atomic quantities moment of inertia, angular momentum,
    # angular velocity, angular acceleration, impulse, torque, poynting energy flux, wavelength).
    unmapped_blocklist = (
        "temperature",
        "entropy",
        "enthalpy",
        "free energy",
        "latent heat",
        "heat capacity",
        "thermal conductivity",
        "heat flux",
        "heat transfer",
        "heat q",
        "internal energy",
        "charge",
        "electric current",
        "induced current",
        "displacement current",
        "noether four-current",
        "voltage",
        "electromotive force",
        "capacitance",
        "pressure",
        "escape velocity",
        "schwarzschild radius",
        "wavefunction",
        "quantum state",
        "eigenstate",
        "subsystem state",
        "basis state",
        "ancilla state",
        "density matrix",
        "spin",
        "outcome probability",
        "channel capacity",
        "mutual information",
        "random variable",
        "frequency f",
        "angular frequency",
        "observed frequency",
        "source frequency",
        "emitted frequency",
        "frequency at infinity",
        "wavenumber",
        "wavelength",
        "index of refraction",
        "angle of incidence",
        "angle of refraction",
        "critical angle",
        "reflectance",
        "local phase",
        "phase difference",
        "diffraction angle",
        "fringe visibility",
        "path distinguishability",
        "unitary operator",
        "running coupling",
        "beta function",
        "gauge potential",
        "matter field",
        "quark flavor",
        "w gauge boson",
        "feynman propagator",
        "vacuum energy",
        "vacuum state",
        "vacuum expectation value",
        "yukawa coupling",
        "transmission probability",
        "barrier height",
        "wave intensity",
        "total intensity",
        "poynting energy flux",
        "viscosity",
        "reynolds number",
        "damping",
        "stiffness",
        "spring constant",
        "impedance",
        "inductance",
        "electrical resistance",
        "resonance width",
        "decoherence rate",
        "string tension",
        "moment of inertia",
        "angular momentum",
        "angular velocity",
        "angular acceleration",
        "impulse",
        "torque",
        "microstate multiplicity",
        "diffusion coefficient",
        "ensemble average",
        "time average",
        "carnot",
        "efficiency",
    )
    if any(b in lower for b in unmapped_blocklist):
        return None, False

    # Canonical phrase/token matches for book-stated and author-ruled partners ONLY.
    canonical_matches = [
        ("speed of light", "Current"),
        ("buoyant force", "Frequency"),
        ("centripetal force", "Frequency"),
        ("kinetic energy", "conscious energy"),
        ("rest energy", "conscious energy"),
        ("relativistic energy", "conscious energy"),
        ("energy", "conscious energy"),
        ("power", "conscious energy"),
        ("work", "conscious energy"),
        ("momentum", "momentum"),
        ("weight", "Frequency"),
        ("gravitational acceleration", "Attraction"),
        ("gravitational field", "Attraction"),
        ("gravitational pull", "Attraction"),
        ("gravity", "Attraction"),
        ("electric field", "Idle"),
        ("magnetic field", "Reflected"),
        ("magnetic flux", "Reflected"),
        ("mass", "Movement M"),
        ("density", "Desire"),
        ("volume", "Vibrance"),
        ("velocity", "rise per Expansion"),
        ("speed", "rise per Expansion"),
        ("acceleration", "Appreciation"),
        ("force", "Frequency"),
        ("spacetime interval", "Vibration-Expansion"),
        ("spacetime coordinate", "Vibration-Expansion"),
        ("spacetime derivative", "Vibration-Expansion"),
        ("spacetime metric", "Vibration-Expansion"),
        ("time interval", "Expansion"),
        ("evolution time", "Expansion"),
        ("time", "Expansion"),
        ("distance", "Vibration"),
        ("displacement", "Vibration"),
        ("separation", "Vibration"),
        ("length", "Vibration"),
        ("radius", "Vibration"),
        ("radial coordinate", "Vibration"),
        ("friction", "resonance"),
        ("radiation", "collection"),
        ("collection", "collection"),
        ("focus", "Tune"),
        ("manifestation", "imagination"),
    ]
    for phrase, target in canonical_matches:
        if phrase in lower:
            return target, True
    return None, False
