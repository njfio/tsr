"""
combinatorial_proofs.py — Part III: Exact Combinatorial Proofs of What the Words Knew
=====================================================================================
Deterministic, LLM-free, exact rational (`fractions.Fraction` / `math.comb`) proofs
over the COMPLETE 80-word audited ledger (`proof/etymology/ledger_80.json`, verbatim
from *What the Words Knew*, 'Every Word, for the Record', pp. 95-100 — all misses,
'outward first', 'household', 'either side', 'nothing to add', 'no help', 'not used',
'a pun', and 'unknown' included).

Methodological & Linguistic Safeguards (Adversarial Referee Audit Hardening):
  1. Explicit Surface-to-Ledger Inflected Wordform Map (`SURFACE_TO_LEDGER`):
     Replaces prefix-heuristic matching across `vocab/mirror.py` and
     `rule/tsr_formal_port.py` with an audited exact token-to-lemma dictionary over
     all 333 frozen-code tokens. Prevents false-friend stem leaks (`"real"`,
     `"reality"`, `"realities"` -/-> `"realize"`; `"moment"` -/-> `"momentum"`;
     `"times"` -/-> `"time"`; `"forceable"` -/-> `"force"`; `"senses"` -/-> `"sense"`;
     `"limitless"` -/-> `"limit"`) while recovering genuine inflected TSR table slots
     (`"belief"` -> `"believe"`, `"expansion"` -> `"expand"`, `"receptive"` ->
     `"receive"`, `"vibrance"` -> `"vibration"`).

  2. Strict Latinate `-mentum`/`-entum`/`-tum` + `-ment` Morphological Blindness Filter
     (Reported Side-by-Side with Legacy 4-Char Filter):
     Strips Latinate `-mentum`, `-entum`, `-tum` alongside English `-ment`, `-tion`,
     etc., catching `momentum` (< Lat. *momentum* < *movimentum*) <-> `movement`
     (< MLat. *movimentum*) as transparent shared *move-*/nominalizer morphology rather
     than counting it as an opaque PIE hit (also documenting the 2019-10-07 ->
     2020-07-06 `Momentum -> Movement` `M`-slot swap, WTWK pp. 39, 93). Reports
     both the primary strict filter (`n_blind_pairs = 3152`, excluding
     `momentum-movement`) and the legacy 4-char filter (`n_blind_pairs = 3153`,
     including `momentum-movement`) side-by-side.

  3. Exact Blind-Pair Hypergeometric Denominator (`total_pop = n_blind_pairs`):
     Because non-blind pairs are deleted from both TSR and etymology blind graphs,
     all exact hypergeometric upper-tail p-values draw from `total_pop = n_blind_pairs`
     (`3152` strict / `3153` legacy, NOT `C(80, 2) = 3160`), reported alongside exact
     blind-pair hypergeometric moments, exact `S_80` QAP vertex-permutation moments,
     exact `(pos, polysemy_tier)` stratified expectations (both blind-pair-conditioned
     and vertex-permutation), and 100,000-trial stratified permutations (`seed=20191007`).

  4. Complete Blind Graph Grid (`g_tsr_pure_table` First) + Dual PIE Root Standards +
     Calque vs. Classical Sense-Overlap Taxonomy:
     Evaluates BOTH zero-choice frozen graphs — prose-free `g_tsr_pure_table` (67 strict
     blind edges; primary headline family) and full frozen repo `g_tsr_frozen` (182
     strict blind edges, verified `g_tsr_pure_table <= g_tsr_frozen`) — across:
       * `pie_roots_strict` (Modern Laryngeal IE: de Vaan 2008 / LIV2 / Kroonen 2013 /
         Beekes 2010; separates `converge < *h1werg-` from `vortex < *wert-`),
       * `pie_roots_pokorny` (Broad Traditional IE: Pokorny IEW 1152 / Watkins /
         Etymonline; retains `*wer-turn` on `converge-vortex`, noting both are Ch. 8
         `outward first` misses in WTWK p. 82), and
       * Diachronic classical extensions distinguishing `coined_translation_calque`
         (`actual-energy`, category `translation_calque`: *energeia -> actualitas*)
         from `classical_sense_overlap` (`desire-expect`, category
         `classical_polysemy_parallel`: *desiderare / exspectare*).
     Explicitly outputs the 2x3 primary grid, the four named Checklist §3.4 cells
     (`III_1A_Pure_PIE`, `III_1A_Diachronic`, `III_1B_Pure_PIE`, `III_1C_Diachronic`),
     and the strict laryngeal-IE sensitivity cells.

  5. Within-Physics Test III.3 (`core_law` vs `secondary_physics`) & Pre-Etymology
     Grounding of All 21 `core_law` Words:
     In *What the Words Knew* (p. 95), `"inward first"` means a word that *"began in
     human life and was later handed to physics"*. Thus the 45 `not_physics_term` words
     are structurally ineligible (`0/45` by definition), making the old `5/21` vs `0/59`
     all-80 Fisher test circular. Test III.3 leads with valid within-physics tests
     (`5/6` vs `0/8` directional physics, p = 3/1001 ≈ 3.00e-3; `5/21` vs `0/14` all
     35 physics words, p = 171/2728 ≈ 0.0627 reported candidly; exact binomial bounds
     against q_0 in {0.05, 0.10, 0.15}; and *Sovereign Mirror* book-only sensitivity
     holding out Oct 2026 `EXTENSION` rulings `work` and `power`), while retaining the
     80-word figure strictly as a descriptive ledger concentration summary.

     Pre-etymology grounding of all 21 `core_law` words (fixed prior to Nov 2026 lookup):
       - `accelerate`: SM Ch. 2 pp. 20, 23 (`F = ma`), Map pp. 171, 173; `MIRROR`, `PHYS`.
       - `attraction`: Notebook p. 1 (2019-10-07); SM Ch. 8 pp. 59-60, Map pp. 169-172; `EXTENDED_PARTNERS`.
       - `charge`: SM Ch. 2 p. 27 (stationary electric charge vs magnetic loop); `kind='both ways'`.
       - `current`: Table (2020-07-06); SM Ch. 1-2, 17 (`E = C^2 M`, `c <-> C`); `MIRROR`, `NONPHYS_STATED`.
       - `density`: SM Ch. 2 pp. 20, 22, 26 (`m = density * volume`), Map pp. 172-173; `MIRROR`, `PHYS`.
       - `distance`: SM Ch. 2 pp. 21, 24, Ch. 16 pp. 116, 118 (#2); `EXTENDED_PARTNERS`, `ROWS` #2.
       - `electric`: Table (2020-07-06); SM Ch. 2 pp. 26-27, Map pp. 172-173; `MIRROR`.
       - `energy`: Notebook p. 1 (2019-10-07, central `E`); SM Ch. 2, 16, 17; `MIRROR`, `PHYS`, `ROWS` #7.
       - `force`: SM Ch. 2 pp. 20, 23 (`F = ma`), Ch. 10 pp. 76-79, Map pp. 170-173; `MIRROR`, `DIAGONAL`, `PHYS`.
       - `gravity`: SM Ch. 8 pp. 59-60, Ch. 16 pp. 117, 121 (#11-12), Map pp. 170, 174; `EXTENDED_PARTNERS`, `ROWS`.
       - `inertia`: SM Ch. 1 p. 16 (defining TSR physical resistance via Newton's inertia), Ch. 10 pp. 75-76; `deep-read.md` (Nov 5).
       - `light`: Notebook p. 1 (2019-10-07, `c`); SM Ch. 2, 16 (#7, #9), Map pp. 170-171; `MIRROR`, `PHYS`, `ROWS`.
       - `mass`: Notebook p. 1 (2019-10-07, `m`); SM Ch. 1, 2, 16, 17, Map pp. 169-173; `MIRROR`, `PHYS`, `ROWS`.
       - `matter`: SM Ch. 2 p. 25, Ch. 10 pp. 76, 79 (core of matter), Ch. 18, 21; `deep-read.md` §2 (Nov 5).
       - `momentum`: Notebook p. 1 (2019-10-07); SM Ch. 17 pp. 129-130, Map pp. 169-175; `EXTENDED_PARTNERS`, `EXTENSION`.
       - `power`: Extension Test (2026-10-22) & Oct 2026 Author Ruling (`tsr.wtf/answers`); `AUTHOR_RULING_SOURCES`, `EXTENDED_PARTNERS`, `EXTENSION` (Nov 5-6).
       - `pressure`: SM Ch. 16 p. 118 (Boyle's law); Extension Test Key #11 (Oct 22 / Nov 5); `ROWS` Boyle row.
       - `space`: Notebook p. 1 (2019-10-07); SM Ch. 2, 16 (#10), Map pp. 169-173; `MIRROR`, `PHYS`, `EXTENSION`, `ROWS`.
       - `time`: Notebook p. 1 (2019-10-07); SM Ch. 2, 15, 16 (#5, #10), Map pp. 169-173; `MIRROR`, `PHYS`, `EXTENSION`, `ROWS`.
       - `volume`: SM Ch. 2 pp. 20, 22, 26 (`m = density * volume`), Ch. 16 p. 118; `MIRROR`, `PHYS`, `ROWS`.
       - `work`: Extension Test (2026-10-22) & Oct 2026 Author Ruling (`tsr.wtf/answers`, `deep-read.md` Nov 5); `AUTHOR_RULING_SOURCES`, `EXTENDED_PARTNERS`, `EXTENSION` (Nov 5-6).
"""
from __future__ import annotations

import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from vocab.mirror import (  # noqa: E402
    AUTHOR_RULING_SOURCES,
    DIAGONAL,
    EXTENDED_PARTNERS,
    GLOSSARY_SENSES,
    MIRROR,
)
from rule.tsr_formal_port import EXTENSION, NONPHYS_STATED, PHYS, ROWS  # noqa: E402

LEDGER_PATH = Path(__file__).resolve().parent / "ledger_80.json"

# Explicit, audited surface-token -> 80-word-ledger lemma dictionary across ALL 333
# unique alphabetic tokens in `vocab/mirror.py` and `rule/tsr_formal_port.py`.
# Zero prefix guessing is permitted.
INFLECTED_SURFACE_TO_LEDGER: dict[str, str] = {
    "acceleration": "accelerate",
    "actualization": "actual",
    "actualized": "actual",
    "appreciation": "appreciate",
    "awareness": "aware",
    "belief": "believe",
    "collection": "collect",
    "collective": "collect",
    "consciousness": "conscious",
    "convergence": "converge",
    "emotional": "emotion",
    "energetic": "energy",
    "expansion": "expand",
    "expectation": "expect",
    "feeling": "feel",
    "felt": "feel",
    "focused": "focus",
    "gravitational": "gravity",
    "imagination": "imagine",
    "limited": "limit",
    "manifestation": "manifest",
    "move": "movement",
    "movements": "movement",
    "objective": "object",
    "radiation": "radiate",
    "realization": "realize",
    "realized": "realize",
    "received": "receive",
    "receptive": "receive",
    "receptivity": "receive",
    "reflected": "reflection",
    "reflects": "reflection",
    "resistance": "resist",
    "resistant": "resist",
    "subjective": "subject",
    "vibrance": "vibration",
    "vibrate": "vibration",
    "vibrating": "vibration",
    "vibrational": "vibration",
    "wanted": "want",
    "wanting": "want",
}

# False-friend, meta-lexicographic, antonym, and homograph tokens in frozen code
# that MUST NEVER alias to a ledger word:
FORBIDDEN_SURFACE_TOKENS: frozenset[str] = frozenset(
    {
        "real",
        "reality",
        "realities",   # Noun 'reality' (Subjective/Objective Reality), NOT transmutation 'realize'
        "moment",      # 'present moment', NOT mechanics 'momentum'
        "times",       # Multiplication ('Movement times Appreciation'), NOT 'time'
        "forceable",   # Rule-runner meta-predicate ('become forceable'), NOT 'force'
        "senses",      # Lexicographic meta-header ('Two senses:'), NOT 'sense'
        "limitless",   # Nonphysical antonym ('without limit'), NOT physical 'limit'/'limited'
        "radius",      # Circle radius (distance), NOT 'radiate'/'radiation'
        "be",          # Auxiliary copula ('taken to be true'), NOT ontological 'being'
    }
)


def build_surface_to_ledger_map(words: list[dict[str, Any]]) -> dict[str, str]:
    ledger_set = {w["word"] for w in words}
    mapping = {w: w for w in ledger_set}
    for surf, lemma in INFLECTED_SURFACE_TO_LEDGER.items():
        assert lemma in ledger_set, f"Inflected target {lemma!r} not in 80-word ledger!"
        mapping[surf] = lemma
    for bad in FORBIDDEN_SURFACE_TOKENS:
        assert bad not in mapping, f"Forbidden false-friend token {bad!r} present in SURFACE_TO_LEDGER!"
    return mapping


SURFACE_TO_LEDGER: dict[str, str] = {
    **{
        w["word"]: w["word"]
        for w in json.loads(LEDGER_PATH.read_text(encoding="utf-8"))["words"]
    },
    **INFLECTED_SURFACE_TO_LEDGER,
}


def extract_ledger_words(
    text: str,
    surface_map: dict[str, str] | None = None,
) -> set[str]:
    """
    Map alphabetic tokens in `text` strictly through the explicit `SURFACE_TO_LEDGER`
    dictionary (zero 4-char `startswith` guessing).
    """
    smap = SURFACE_TO_LEDGER if surface_map is None else surface_map
    tokens = re.findall(r"[a-zA-Z]+", text.lower())
    return {smap[tok] for tok in tokens if tok in smap}


def _u_edge(a: str, b: str) -> tuple[str, str]:
    assert a != b, f"Self-loop not allowed: {a}"
    return (a, b) if a < b else (b, a)


def _strip_productive_suffix_legacy(w: str) -> str:
    """Legacy English-only suffix stripper (misses Latinate `-mentum` on `momentum`)."""
    for suf in ("ation", "ition", "tion", "sion", "ment", "ness", "ance", "ence"):
        if len(w) >= len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def _strip_productive_suffix(w: str) -> tuple[str, str | None]:
    """
    Strict morphological suffix stripper handling Latinate `-mentum` / `-entum` / `-tum`
    alongside productive English nominalizers (`-ment`, `-ation`, `-ition`, `-tion`,
    `-sion`, `-ness`, `-ance`, `-ence`). Returns `(stripped_stem, suffix_family)`.
    """
    for suf, fam, min_stem in (
        ("mentum", "ment", 2),
        ("entum", "ment", 3),
        ("tum", "tum", 3),
        ("ation", "tion", 3),
        ("ition", "tion", 3),
        ("tion", "tion", 3),
        ("sion", "tion", 3),
        ("ment", "ment", 3),
        ("ness", "ness", 3),
        ("ance", "ance", 3),
        ("ence", "ence", 3),
    ):
        if len(w) >= len(suf) + min_stem and w.endswith(suf):
            return w[: -len(suf)], fam
    return w, None


def shares_4char_substring_legacy(w1: str, w2: str) -> bool:
    """Legacy 4-char substring filter (for Checklist §3.2 side-by-side sensitivity)."""
    a, b = _strip_productive_suffix_legacy(w1.lower()), _strip_productive_suffix_legacy(w2.lower())
    if len(a) < 4 or len(b) < 4:
        return a == b
    subs_a = {a[i : i + 4] for i in range(len(a) - 3)}
    subs_b = {b[i : i + 4] for i in range(len(b) - 3)}
    return bool(subs_a & subs_b)


def shares_4char_substring(w1: str, w2: str, *, strict_latinate: bool = True) -> bool:
    """
    Orthographic and transparent-morphology blindness filter.
    When `strict_latinate=True` (default / primary):
      1. Strips Latinate `-mentum` / `-entum` / `-tum` alongside `-ment`, `-tion`, etc.
      2. Flags cognate `-ment` / `-mentum` nominalizations sharing a >=2-character root
         onset (`mo-mentum` < *movimentum* and `move-ment` < *movimentum*, both from
         Latin *movere* + *-mentum*).
      3. Flags any shared >=4-char substring on stripped stems (or exact stem match when
         either stripped stem has <4 characters).
    """
    if not strict_latinate:
        return shares_4char_substring_legacy(w1, w2)
    a, fam_a = _strip_productive_suffix(w1.lower())
    b, fam_b = _strip_productive_suffix(w2.lower())
    if fam_a == "ment" and fam_b == "ment" and a[:2] == b[:2]:
        return True
    if len(a) < 4 or len(b) < 4:
        return a == b
    subs_a = {a[i : i + 4] for i in range(len(a) - 3)}
    subs_b = {b[i : i + 4] for i in range(len(b) - 3)}
    return bool(subs_a & subs_b)


def compute_blind_pair_universe(
    words: list[dict[str, Any]],
    *,
    strict_latinate: bool = True,
) -> tuple[set[tuple[str, str]], list[tuple[str, str]]]:
    """
    Return `(eligible_blind_pairs, excluded_nonblind_pairs)` across all C(80, 2) = 3,160
    unordered word pairs in the 80-word ledger.
    """
    eligible: set[tuple[str, str]] = set()
    excluded: list[tuple[str, str]] = []
    n = len(words)
    for i in range(n):
        for j in range(i + 1, n):
            wi, wj = words[i], words[j]
            u, v = wi["word"], wj["word"]
            e = _u_edge(u, v)
            if (
                wi["orthographic_stem"] == wj["orthographic_stem"]
                or shares_4char_substring(u, v, strict_latinate=strict_latinate)
            ):
                excluded.append(e)
            else:
                eligible.add(e)
    excluded.sort()
    assert len(eligible) + len(excluded) == math.comb(n, 2)
    return eligible, excluded


def load_ledger() -> list[dict[str, Any]]:
    data = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    words = data["words"]
    assert len(words) == 80, f"Expected all 80 words, got {len(words)}"
    seen = [w["word"] for w in words]
    assert len(set(seen)) == 80, "Duplicate words in ledger!"
    return words


def build_hidden_etymology_graphs(
    words: list[dict[str, Any]],
    *,
    strict_latinate: bool = True,
) -> dict[str, set[tuple[str, str]]]:
    """
    Construct hidden diachronic root and classical-link graphs over the 80 words under
    the specified blindness filter (`strict_latinate=True` -> N_blind=3152;
    `strict_latinate=False` -> N_blind=3153):
      - `strict_pie`: shared `pie_roots_strict` (de Vaan 2008 / LIV2 / Kroonen / Beekes;
        separates `converge < *h1werg-` from `vortex < *wert-`).
      - `pokorny_pie`: shared `pie_roots_pokorny` (Pokorny IEW / Watkins / Etymonline;
        retains `*wer-turn` grouping on `converge-vortex`).
      - `strict_pie_plus_translation_calque`: `strict_pie` + `coined_translation_calque`
        (`actual-energy` ONLY; excludes `desire-expect` `classical_sense_overlap`).
      - `diachronic_strict_pie`: `strict_pie` + `coined_translation_calque`
        (`actual-energy`) + `classical_sense_overlap` (`desire-expect`).
      - `diachronic_pokorny_pie`: `pokorny_pie` + `coined_translation_calque`
        (`actual-energy`) + `classical_sense_overlap` (`desire-expect`).
    """
    eligible_pairs, _ = compute_blind_pair_universe(words, strict_latinate=strict_latinate)

    strict_pie: set[tuple[str, str]] = set()
    pokorny_pie: set[tuple[str, str]] = set()
    coined_calque_edges: set[tuple[str, str]] = set()
    sense_overlap_edges: set[tuple[str, str]] = set()

    n = len(words)
    for i in range(n):
        for j in range(i + 1, n):
            wi, wj = words[i], words[j]
            e = _u_edge(wi["word"], wj["word"])
            if e not in eligible_pairs:
                continue

            if set(wi["pie_roots_strict"]) & set(wj["pie_roots_strict"]):
                strict_pie.add(e)
            if set(wi["pie_roots_pokorny"]) & set(wj["pie_roots_pokorny"]):
                pokorny_pie.add(e)

            if (
                wi.get("classical_link_type") == "coined_translation_calque"
                and wi.get("classical_link_group") is not None
                and wi.get("classical_link_group") == wj.get("classical_link_group")
            ):
                coined_calque_edges.add(e)
            elif (
                wi.get("classical_link_type") == "classical_sense_overlap"
                and wi.get("classical_link_group") is not None
                and wi.get("classical_link_group") == wj.get("classical_link_group")
            ):
                sense_overlap_edges.add(e)

    return {
        "strict_pie": strict_pie,
        "pokorny_pie": pokorny_pie,
        "coined_translation_calque_only": coined_calque_edges,
        "classical_sense_overlap_only": sense_overlap_edges,
        "strict_pie_plus_translation_calque": strict_pie | coined_calque_edges,
        "diachronic_strict_pie": strict_pie | coined_calque_edges | sense_overlap_edges,
        "diachronic_pokorny_pie": pokorny_pie | coined_calque_edges | sense_overlap_edges,
    }


def classify_etymology_pair(
    edge: tuple[str, str],
    word_by_name: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    u, v = edge
    wu, wv = word_by_name[u], word_by_name[v]
    shared_strict = sorted(set(wu["pie_roots_strict"]) & set(wv["pie_roots_strict"]))
    shared_pokorny = sorted(set(wu["pie_roots_pokorny"]) & set(wv["pie_roots_pokorny"]))
    nonblind_strict = shares_4char_substring(u, v, strict_latinate=True)
    if nonblind_strict:
        rel = "non_blind_shared_latinate_morphology"
    elif shared_strict:
        rel = "strict_pie_cognate"
    elif shared_pokorny:
        rel = "pokorny_root_extension_only"
    elif (
        wu.get("classical_link_type") == "coined_translation_calque"
        and wu.get("classical_link_group") == wv.get("classical_link_group")
    ):
        rel = "coined_translation_calque"
    elif (
        wu.get("classical_link_type") == "classical_sense_overlap"
        and wu.get("classical_link_group") == wv.get("classical_link_group")
    ):
        rel = "classical_sense_overlap"
    else:
        rel = "unclassified"
    out: dict[str, Any] = {
        "pair": [u, v],
        "relation_type": rel,
        "pie_roots_strict_shared": shared_strict,
        "pie_roots_pokorny_shared": shared_pokorny,
        "classical_link_type": wu.get("classical_link_type")
        if wu.get("classical_link_group") and wu.get("classical_link_group") == wv.get("classical_link_group")
        else None,
        "classical_link_category": wu.get("classical_link_category")
        if wu.get("classical_link_group") and wu.get("classical_link_group") == wv.get("classical_link_group")
        else None,
        "wtwk_kinds": [wu["kind"], wv["kind"]],
    }
    if {u, v} == {"converge", "vortex"}:
        out["note"] = (
            "Separated in strict laryngeal IE (converge < *h1werg- vs vortex < *wert-, de Vaan 2008: 665, 667); "
            "united only under Pokorny IEW 1152 *wer-; both are Ch. 8 'outward first' misses in WTWK (p. 82)."
        )
    elif {u, v} == {"momentum", "movement"}:
        out["note"] = (
            "Shared Latinate movere + -mentum/-ment morphology; excluded from primary strict blind universe "
            "(also subject to 2019-10-07 -> 2020-07-06 Momentum -> Movement M-slot swap, WTWK pp. 39, 93)."
        )
    elif {u, v} == {"desire", "expect"}:
        out["note"] = (
            "Classical Latin dictionary polysemy overlap (desiderare / exspectare 'to long for, hope for', "
            "WTWK Ch. 5 p. 52); classified as classical_sense_overlap (classical_polysemy_parallel), NOT a calque."
        )
    elif {u, v} == {"actual", "energy"}:
        out["note"] = (
            "Coined medieval Scholastic translation calque (actualitas coined to translate Aristotle's energeia); "
            "classified as coined_translation_calque (translation_calque)."
        )
    return out


# Exploratory unblinded book concordance (quarantined from blind inferential p-values):
CANONICAL_TSR_EDGES_RAW: list[tuple[str, str]] = [
    ("limit", "aware"),
    ("resist", "receive"),
    ("radiate", "collect"),
    ("subject", "vibration"),
    ("object", "collect"),
    ("empirical", "emotion"),
    ("now", "future"),
    ("past", "current"),
    ("believe", "desire"),
    ("expect", "intuition"),
    ("light", "current"),
    ("mass", "movement"),
    ("inertia", "movement"),
    ("focus", "tune"),
    ("electric", "idle"),
    ("density", "desire"),
    ("volume", "vibration"),
    ("actual", "realize"),
    ("express", "want"),
    ("express", "wish"),
    ("sense", "inspire"),
    ("space", "vibration"),
    ("time", "expand"),
    ("accelerate", "appreciate"),
    ("manifest", "imagine"),
    ("force", "frequency"),
    ("gravity", "attraction"),
    ("friction", "resonance"),
    ("distance", "vibration"),
    ("desire", "expect"),
    ("believe", "intuition"),
    ("future", "past"),
    ("now", "current"),
    ("resist", "attraction"),
    ("receive", "attraction"),
    ("collect", "momentum"),
    ("radiate", "momentum"),
    ("subject", "object"),
    ("subject", "experience"),
    ("object", "empirical"),
    ("empirical", "experience"),
    ("space", "time"),
    ("vibration", "expand"),
    ("time", "past"),
    ("time", "now"),
    ("time", "future"),
    ("expand", "past"),
    ("expand", "future"),
    ("future", "being"),
    ("entity", "being"),
    ("entity", "present"),
    ("entity", "soul"),
    ("entity", "eternal"),
    ("entity", "sovereign"),
    ("entity", "aware"),
    ("entity", "exist"),
    ("present", "eternal"),
    ("mirror", "reflection"),
    ("reflection", "present"),
    ("human", "being"),
    ("conscious", "aware"),
    ("conscious", "energy"),
    ("conscious", "current"),
    ("energy", "actual"),
    ("energy", "realize"),
    ("energy", "mass"),
    ("energy", "movement"),
    ("energy", "light"),
    ("energy", "current"),
    ("energy", "work"),
    ("energy", "power"),
    ("work", "force"),
    ("power", "force"),
    ("force", "mass"),
    ("force", "accelerate"),
    ("force", "empirical"),
    ("mass", "density"),
    ("mass", "volume"),
    ("mass", "inertia"),
    ("mass", "matter"),
    ("mass", "gravity"),
    ("movement", "desire"),
    ("movement", "appreciate"),
    ("movement", "frequency"),
    ("movement", "momentum"),
    ("movement", "emotion"),
    ("frequency", "appreciate"),
    ("frequency", "emotion"),
    ("emotion", "feel"),
    ("evidence", "empirical"),
    ("evidence", "emotion"),
    ("evidence", "sense"),
    ("intuition", "idea"),
    ("intuition", "imagine"),
    ("converge", "vortex"),
    ("converge", "focus"),
    ("vortex", "attraction"),
    ("culminate", "expand"),
    ("culminate", "collect"),
    ("culminate", "resonance"),
    ("resist", "distance"),
    ("resist", "contrast"),
    ("resist", "exist"),
    ("resist", "tension"),
    ("distance", "contrast"),
    ("contrast", "desire"),
    ("tension", "tune"),
    ("charge", "electric"),
    ("charge", "field"),
    ("electric", "field"),
    ("pressure", "volume"),
]


def build_canonical_tsr_graph(
    words: list[dict[str, Any]],
    *,
    strict_latinate: bool = True,
) -> set[tuple[str, str]]:
    """
    Build the unblinded exploratory concordance graph restricted to `eligible_blind_pairs`
    so its descriptive comparisons operate over the identical `n_blind_pairs` universe.
    """
    word_set = {w["word"] for w in words}
    eligible_pairs, _ = compute_blind_pair_universe(words, strict_latinate=strict_latinate)
    edges: set[tuple[str, str]] = set()
    for u, v in CANONICAL_TSR_EDGES_RAW:
        assert u in word_set and v in word_set, f"Edge ({u}, {v}) not in 80-word ledger!"
        e = _u_edge(u, v)
        if e in eligible_pairs:
            edges.add(e)
    return edges


def build_programmatic_pure_table_graph(
    words: list[dict[str, Any]],
    *,
    strict_latinate: bool = True,
) -> set[tuple[str, str]]:
    """
    Primary zero-researcher-choice blind graph (`g_tsr_pure_table`): extracted ONLY
    from prose-free table pairings and algebraic formulas in `vocab/mirror.py`
    (`MIRROR`, `DIAGONAL`, `EXTENDED_PARTNERS`) and `rule/tsr_formal_port.py`
    (`PHYS`, `NONPHYS_STATED`, `EXTENSION`), mapped via `SURFACE_TO_LEDGER` and
    restricted to `eligible_blind_pairs`.
    """
    smap = build_surface_to_ledger_map(words)
    eligible_pairs, _ = compute_blind_pair_universe(words, strict_latinate=strict_latinate)
    edges: set[tuple[str, str]] = set()

    def connect_sets(s1: set[str], s2: set[str]) -> None:
        for u in s1:
            for v in s2:
                if u != v:
                    e = _u_edge(u, v)
                    if e in eligible_pairs:
                        edges.add(e)

    for phys, non, _role in MIRROR:
        connect_sets(extract_ledger_words(phys, smap), extract_ledger_words(non, smap))
    for left, right in DIAGONAL:
        connect_sets(extract_ledger_words(left, smap), extract_ledger_words(right, smap))
    for phys, non in EXTENDED_PARTNERS.items():
        connect_sets(extract_ledger_words(phys, smap), extract_ledger_words(non, smap))
    for lhs, (_op, rhs_tup) in (
        list(PHYS.items()) + list(NONPHYS_STATED.items()) + list(EXTENSION.items())
    ):
        connect_sets(
            extract_ledger_words(lhs, smap),
            extract_ledger_words(" ".join(rhs_tup), smap),
        )

    return edges


def build_programmatic_frozen_mirror_graph(
    words: list[dict[str, Any]],
    *,
    strict_latinate: bool = True,
) -> set[tuple[str, str]]:
    """
    Full zero-researcher-choice frozen repository code graph (`g_tsr_frozen`):
    superset of `g_tsr_pure_table` adding frozen glossary and calibration-row structures
    in `vocab/mirror.py` (`GLOSSARY_SENSES`, `AUTHOR_RULING_SOURCES`) and
    `rule/tsr_formal_port.py` (`ROWS`), mapped via `SURFACE_TO_LEDGER` and restricted
    to `eligible_blind_pairs`.
    """
    smap = build_surface_to_ledger_map(words)
    eligible_pairs, _ = compute_blind_pair_universe(words, strict_latinate=strict_latinate)
    edges: set[tuple[str, str]] = set(
        build_programmatic_pure_table_graph(words, strict_latinate=strict_latinate)
    )

    def connect_sets(s1: set[str], s2: set[str]) -> None:
        for u in s1:
            for v in s2:
                if u != v:
                    e = _u_edge(u, v)
                    if e in eligible_pairs:
                        edges.add(e)

    for head, gloss in GLOSSARY_SENSES.items():
        connect_sets(extract_ledger_words(head, smap), extract_ledger_words(gloss, smap))
    for head, ruling_src in AUTHOR_RULING_SOURCES.items():
        connect_sets(extract_ledger_words(head, smap), extract_ledger_words(ruling_src, smap))
    for row_name, _ruling, _hm, _defn, _costs, row_src in ROWS:
        connect_sets(extract_ledger_words(row_name, smap), extract_ledger_words(row_src, smap))

    return edges


def exact_blind_hypergeometric_moments(
    n_blind_pairs: int,
    draws: int,
    pop_successes: int,
) -> dict[str, Any]:
    """
    Exact rational first and second moments of the hypergeometric edge-overlap count
    over the eligible blind-pair universe of size `n_blind_pairs` (< 3,160).
    """
    mean_exact = Fraction(draws * pop_successes, n_blind_pairs)
    var_exact = (
        Fraction(draws * pop_successes, n_blind_pairs)
        * Fraction(n_blind_pairs - pop_successes, n_blind_pairs)
        * Fraction(n_blind_pairs - draws, n_blind_pairs - 1)
    )
    return {
        "n_blind_pairs": n_blind_pairs,
        "mean_fraction": f"{mean_exact.numerator}/{mean_exact.denominator}",
        "mean_float": float(mean_exact),
        "variance_fraction": f"{var_exact.numerator}/{var_exact.denominator}",
        "variance_float": float(var_exact),
        "std_float": math.sqrt(float(var_exact)),
    }


def exact_qap_moments_uniform(
    n_vertices: int,
    edges_a: set[tuple[str, str]],
    edges_b: set[tuple[str, str]],
) -> dict[str, Any]:
    """
    Exact rational expectation E[T] and variance Var(T) of the vertex-permutation
    edge-overlap statistic T(pi) = |E_A cap pi(E_B)| over ALL n! bijections pi in S_n
    (80! ≈ 7.16e118). Because non-blind pairs are already absent from E_A and E_B,
    any edge mapped onto a non-blind vertex pair automatically contributes 0 to T(pi).
    """
    m_pairs = math.comb(n_vertices, 2)
    a_size = len(edges_a)
    b_size = len(edges_b)
    mean_exact = Fraction(a_size * b_size, m_pairs)

    def edge_pair_type_counts(edges: set[tuple[str, str]]) -> tuple[int, int, int]:
        deg: Counter[str] = Counter()
        for u, v in edges:
            deg[u] += 1
            deg[v] += 1
        same = len(edges)
        adj = sum(d * (d - 1) for d in deg.values())
        total_ord = len(edges) * len(edges)
        disj = total_ord - same - adj
        return same, adj, disj

    a0, a1, a2 = edge_pair_type_counts(edges_a)
    b0, b1, b2 = edge_pair_type_counts(edges_b)

    n0 = m_pairs
    n1 = n_vertices * (n_vertices - 1) * (n_vertices - 2)
    n2 = m_pairs * math.comb(n_vertices - 2, 2)

    e_t_sq = (
        Fraction(a0 * b0, n0)
        + Fraction(a1 * b1, n1)
        + Fraction(a2 * b2, n2)
    )
    var_exact = e_t_sq - mean_exact * mean_exact
    return {
        "vertex_pair_space": m_pairs,
        "mean_fraction": f"{mean_exact.numerator}/{mean_exact.denominator}",
        "mean_float": float(mean_exact),
        "variance_fraction": f"{var_exact.numerator}/{var_exact.denominator}",
        "variance_float": float(var_exact),
        "std_float": math.sqrt(float(var_exact)),
    }


def exact_stratified_expectation(
    words: list[dict[str, Any]],
    edges_tsr: set[tuple[str, str]],
    edges_etym: set[tuple[str, str]],
    stratum_fn: Callable[[dict[str, Any]], Any],
    eligible_blind_pairs: set[tuple[str, str]] | None = None,
) -> Fraction:
    """
    Compute the EXACT rational stratified expectation E_strat[T]:
      - If `eligible_blind_pairs is None`: exact expectation over vertex permutations
        pi in prod_s S_{V_s} preserving `stratum_fn(word)` (matches the exact mean of
        `run_stratified_permutation_crosscheck`).
      - If `eligible_blind_pairs` is provided: exact expectation over stratum-matched
        blind edge draws where each unordered stratum pair `(s_u, s_v)` uses denominator
        `|Pairs(s_u, s_v) cap eligible_blind_pairs|`.
    """
    word_to_stratum = {w["word"]: stratum_fn(w) for w in words}
    stratum_sizes = Counter(word_to_stratum.values())

    blind_stratum_denoms: Counter[tuple[Any, Any]] = Counter()
    if eligible_blind_pairs is not None:
        for u, v in eligible_blind_pairs:
            su, sv = word_to_stratum[u], word_to_stratum[v]
            key = (su, sv) if su <= sv else (sv, su)
            blind_stratum_denoms[key] += 1

    etym_counts: Counter[tuple[Any, Any]] = Counter()
    for u, v in edges_etym:
        su, sv = word_to_stratum[u], word_to_stratum[v]
        key = (su, sv) if su <= sv else (sv, su)
        etym_counts[key] += 1

    expected = Fraction(0, 1)
    for u, v in edges_tsr:
        su, sv = word_to_stratum[u], word_to_stratum[v]
        key = (su, sv) if su <= sv else (sv, su)
        k_hits = etym_counts[key]
        if k_hits == 0:
            continue
        if eligible_blind_pairs is not None:
            denom = blind_stratum_denoms[key]
        elif su == sv:
            denom = math.comb(stratum_sizes[su], 2)
        else:
            denom = stratum_sizes[su] * stratum_sizes[sv]
        assert denom > 0, f"Zero denominator in stratum {key}"
        expected += Fraction(k_hits, denom)
    return expected


def exact_hypergeometric_upper_tail(
    total_pop: int,
    pop_successes: int,
    draws: int,
    obs_k: int,
) -> Fraction:
    """
    Exact rational hypergeometric upper-tail probability P(X >= obs_k) when drawing
    `draws` blind pairs without replacement from `total_pop = n_blind_pairs` eligible
    blind pairs containing `pop_successes` hidden etymology edges.
    """
    assert 0 <= draws <= total_pop, f"Invalid draws={draws} for total_pop={total_pop}"
    assert 0 <= pop_successes <= total_pop, (
        f"Invalid pop_successes={pop_successes} for total_pop={total_pop}"
    )
    if obs_k <= 0:
        return Fraction(1, 1)
    denom = math.comb(total_pop, draws)
    num = 0
    max_k = min(pop_successes, draws)
    for k in range(obs_k, max_k + 1):
        if draws - k <= total_pop - pop_successes:
            num += math.comb(pop_successes, k) * math.comb(total_pop - pop_successes, draws - k)
    return Fraction(num, denom)


def exact_binomial_upper_tail(n_trials: int, k_obs: int, p0: Fraction) -> Fraction:
    """Exact rational binomial upper tail sum_{k=k_obs}^{n_trials} C(n, k) p0^k (1 - p0)^{n-k}."""
    q0 = Fraction(1, 1) - p0
    total = Fraction(0, 1)
    for k in range(k_obs, n_trials + 1):
        total += Fraction(math.comb(n_trials, k), 1) * (p0**k) * (q0 ** (n_trials - k))
    return total


def exact_odds_ratio_and_haldane(a: int, b: int, c: int, d: int) -> dict[str, Any]:
    """
    Compute exact MLE odds ratio `(a*d)/(b*c)` (`"infinity"` when `b*c == 0` and `a*d > 0`)
    and Haldane-Anscombe (+0.5) continuity-corrected odds ratio `((a+0.5)(d+0.5))/((b+0.5)(c+0.5))`
    for a 2x2 table `[[a, b], [c, d]]`.
    """
    exact_or: str | float
    exact_or_frac: str | None
    if b * c == 0:
        exact_or = "infinity" if a * d > 0 else "undefined"
        exact_or_frac = None
    else:
        f_or = Fraction(a * d, b * c)
        exact_or = float(f_or)
        exact_or_frac = f"{f_or.numerator}/{f_or.denominator}"

    ha = (Fraction(2 * a + 1, 2) * Fraction(2 * d + 1, 2)) / (
        Fraction(2 * b + 1, 2) * Fraction(2 * c + 1, 2)
    )
    return {
        "contingency_2x2": [[a, b], [c, d]],
        "exact_odds_ratio": exact_or,
        "exact_odds_ratio_fraction": exact_or_frac,
        "haldane_anscombe_cc_odds_ratio_fraction": f"{ha.numerator}/{ha.denominator}",
        "haldane_anscombe_cc_odds_ratio_float": round(float(ha), 4),
    }


def run_stratified_permutation_crosscheck(
    words: list[dict[str, Any]],
    edges_tsr: set[tuple[str, str]],
    edges_etym: set[tuple[str, str]],
    obs_overlap: int,
    stratum_fn: Callable[[dict[str, Any]], Any],
    n_trials: int = 100_000,
    seed: int = 20191007,
) -> dict[str, Any]:
    """
    Standalone deterministic seeded permutation cross-check preserving `stratum_fn(w)`.
    """
    return run_batched_stratified_permutation_crosscheck(
        words=words,
        tasks=[("single", edges_tsr, edges_etym, obs_overlap)],
        stratum_fn=stratum_fn,
        n_trials=n_trials,
        seed=seed,
    )["single"]


def run_batched_stratified_permutation_crosscheck(
    words: list[dict[str, Any]],
    tasks: list[tuple[str, set[tuple[str, str]], set[tuple[str, str]], int]],
    stratum_fn: Callable[[dict[str, Any]], Any],
    n_trials: int = 100_000,
    seed: int = 20191007,
) -> dict[str, dict[str, Any]]:
    """
    Evaluate one or more `(task_id, edges_tsr, edges_etym, obs_overlap)` alignments over
    the IDENTICAL sequence of `n_trials` stratified permutations (`seed=20191007`) using
    integer vertex indexing for speed (bit-for-bit identical to standalone execution).
    """
    sorted_words = sorted(w["word"] for w in words)
    w2i = {w: idx for idx, w in enumerate(sorted_words)}
    n_v = len(sorted_words)

    groups: dict[Any, list[str]] = defaultdict(list)
    for w in words:
        groups[stratum_fn(w)].append(w["word"])
    group_idx_lists = [[w2i[s] for s in sorted(vs)] for _k, vs in sorted(groups.items())]

    def pack_pair(i: int, j: int) -> int:
        return i * n_v + j if i < j else j * n_v + i

    compiled = []
    for task_id, edges_tsr, edges_etym, obs_overlap in tasks:
        tsr_packed = {pack_pair(w2i[u], w2i[v]) for u, v in edges_tsr}
        etym_idx = [(w2i[u], w2i[v]) for u, v in edges_etym]
        compiled.append([task_id, tsr_packed, etym_idx, obs_overlap, 0, 0, 0])

    rng = random.Random(seed)
    perm = [0] * n_v

    for _ in range(n_trials):
        for orig_indices in group_idx_lists:
            shuffled = list(orig_indices)
            rng.shuffle(shuffled)
            for a, b in zip(orig_indices, shuffled):
                perm[a] = b

        for entry in compiled:
            tsr_packed = entry[1]
            etym_idx = entry[2]
            obs_ov = entry[3]
            hits = 0
            for iu, iv in etym_idx:
                pu, pv = perm[iu], perm[iv]
                key = pu * n_v + pv if pu < pv else pv * n_v + pu
                if key in tsr_packed:
                    hits += 1
            entry[4] += hits
            if hits > entry[5]:
                entry[5] = hits
            if hits >= obs_ov:
                entry[6] += 1

    results: dict[str, dict[str, Any]] = {}
    for task_id, _tsr_p, _etym_i, _obs_ov, sum_hits, max_seen, exceed_count in compiled:
        results[task_id] = {
            "n_trials": n_trials,
            "seed": seed,
            "exceed_or_equal_count": exceed_count,
            "empirical_p_upper_bound": (exceed_count + 1) / (n_trials + 1),
            "empirical_mean": sum_hits / n_trials,
            "max_overlap_in_null": max_seen,
        }
    return results


def evaluate_graph_alignment(
    label: str,
    blind_status: str,
    words: list[dict[str, Any]],
    word_by_name: dict[str, dict[str, Any]],
    eligible_blind_pairs: set[tuple[str, str]],
    edges_tsr: set[tuple[str, str]],
    edges_etym: set[tuple[str, str]],
    perm_check: dict[str, Any],
) -> dict[str, Any]:
    assert edges_tsr <= eligible_blind_pairs, f"{label}: TSR graph contains non-blind pair!"
    assert edges_etym <= eligible_blind_pairs, f"{label}: Etymology graph contains non-blind pair!"

    n_words = len(words)
    all_word_pairs = math.comb(n_words, 2)
    n_blind_pairs = len(eligible_blind_pairs)

    overlap_edges = sorted(edges_tsr & edges_etym)
    missed_etym_edges = sorted(edges_etym - edges_tsr)
    obs = len(overlap_edges)

    blind_hyper_moments = exact_blind_hypergeometric_moments(
        n_blind_pairs=n_blind_pairs,
        draws=len(edges_tsr),
        pop_successes=len(edges_etym),
    )
    qap_uniform = exact_qap_moments_uniform(n_words, edges_tsr, edges_etym)

    z_score_blind = (
        (obs - blind_hyper_moments["mean_float"]) / blind_hyper_moments["std_float"]
        if blind_hyper_moments["std_float"] > 0
        else 0.0
    )
    z_score_s80 = (
        (obs - qap_uniform["mean_float"]) / qap_uniform["std_float"]
        if qap_uniform["std_float"] > 0
        else 0.0
    )

    mu_q = Fraction(qap_uniform["mean_fraction"])
    var_q = Fraction(qap_uniform["variance_fraction"])
    t_q = Fraction(obs, 1) - mu_q
    cantelli_bound = var_q / (var_q + t_q * t_q) if t_q > 0 else Fraction(1, 1)

    # Exact hypergeometric edge-draw upper tail over N_blind eligible blind pairs (< 3,160)
    hyper_p = exact_hypergeometric_upper_tail(
        total_pop=n_blind_pairs,
        pop_successes=len(edges_etym),
        draws=len(edges_tsr),
        obs_k=obs,
    )

    exp_polysemy_blind = exact_stratified_expectation(
        words,
        edges_tsr,
        edges_etym,
        stratum_fn=lambda w: w["polysemy_tier"],
        eligible_blind_pairs=eligible_blind_pairs,
    )
    exp_pos_polysemy_blind = exact_stratified_expectation(
        words,
        edges_tsr,
        edges_etym,
        stratum_fn=lambda w: (w["pos"], w["polysemy_tier"]),
        eligible_blind_pairs=eligible_blind_pairs,
    )
    exp_pos_polysemy_vertex = exact_stratified_expectation(
        words,
        edges_tsr,
        edges_etym,
        stratum_fn=lambda w: (w["pos"], w["polysemy_tier"]),
        eligible_blind_pairs=None,
    )

    return {
        "alignment_id": label,
        "blind_status": blind_status,
        "total_words": n_words,
        "total_unfiltered_word_pairs": all_word_pairs,
        "n_blind_pairs": n_blind_pairs,
        "hypergeometric_total_pop_used": n_blind_pairs,
        "tsr_edge_count": len(edges_tsr),
        "etymology_edge_count": len(edges_etym),
        "observed_overlap_count": obs,
        "overlapping_pairs": [list(e) for e in overlap_edges],
        "overlapping_pair_classifications": [
            classify_etymology_pair(e, word_by_name) for e in overlap_edges
        ],
        "non_overlapping_etymology_pairs": [list(e) for e in missed_etym_edges],
        "exact_blind_pair_hypergeometric_moments": blind_hyper_moments,
        "exact_uniform_S80_moments": qap_uniform,
        "z_score_vs_blind_hypergeometric": round(z_score_blind, 4),
        "z_score_vs_uniform_S80": round(z_score_s80, 4),
        "exact_cantelli_upper_bound_float": float(cantelli_bound),
        "exact_hypergeometric_p_fraction": f"{hyper_p.numerator}/{hyper_p.denominator}",
        "exact_hypergeometric_p_float": float(hyper_p),
        "exact_polysemy_stratified_mean": {
            "blind_pair_conditioned_fraction": f"{exp_polysemy_blind.numerator}/{exp_polysemy_blind.denominator}",
            "float": float(exp_polysemy_blind),
            "enrichment_ratio": round(obs / float(exp_polysemy_blind), 2)
            if exp_polysemy_blind > 0
            else None,
        },
        "exact_pos_and_polysemy_stratified_mean": {
            "blind_pair_conditioned_fraction": f"{exp_pos_polysemy_blind.numerator}/{exp_pos_polysemy_blind.denominator}",
            "blind_pair_conditioned_float": float(exp_pos_polysemy_blind),
            "vertex_permutation_fraction": f"{exp_pos_polysemy_vertex.numerator}/{exp_pos_polysemy_vertex.denominator}",
            "float": float(exp_pos_polysemy_vertex),
            "enrichment_ratio": round(obs / float(exp_pos_polysemy_blind), 2)
            if exp_pos_polysemy_blind > 0
            else None,
            "enrichment_ratio_vertex_perm": round(obs / float(exp_pos_polysemy_vertex), 2)
            if exp_pos_polysemy_vertex > 0
            else None,
        },
        "stratified_permutation_100k_crosscheck": perm_check,
    }


def run_test_iii_2_energeia_actualitas_hinge(
    words: list[dict[str, Any]],
    n_blind_pairs_strict: int,
    g_tsr_pure_table: set[tuple[str, str]],
    g_tsr_frozen: set[tuple[str, str]],
    g_tsr_canonical: set[tuple[str, str]],
) -> dict[str, Any]:
    """
    Test III.2: Exact rational probabilities for the unique coined translation calque
    (`energy` [*energeia*] <-> `actual` [*actualitas*]; category `translation_calque`,
    type `coined_translation_calque`) landing on the central E -> physical transmutation
    hinge of *The Sovereign Mirror* (The Map pp. 169-171).
    """
    n_words = len(words)
    total_pairs = math.comb(n_words, 2)  # 3,160

    process_words = [
        w["word"]
        for w in words
        if w["word"]
        in {
            "accelerate",
            "actual",
            "appreciate",
            "collect",
            "converge",
            "culminate",
            "expand",
            "express",
            "focus",
            "imagine",
            "inspire",
            "manifest",
            "radiate",
            "realize",
            "receive",
            "resist",
            "tune",
        }
    ]
    n_process = len(process_words)  # 17

    p_exact_right_blind = Fraction(1, n_blind_pairs_strict)
    p_either_hinge_blind = Fraction(2, n_blind_pairs_strict)
    p_exact_right_all = Fraction(1, total_pairs)
    p_either_hinge_all = Fraction(2, total_pairs)
    p_in_pure_table = Fraction(len(g_tsr_pure_table), n_blind_pairs_strict)
    p_in_frozen_repo = Fraction(len(g_tsr_frozen), n_blind_pairs_strict)
    p_role_conditioned_right = Fraction(1, n_process)
    p_role_conditioned_either = Fraction(2, n_process)

    calque_edge = _u_edge("actual", "energy")

    return {
        "calque_pair": ["actual", "energy"],
        "classical_link_type": "coined_translation_calque",
        "classical_link_category": "translation_calque",
        "historical_origin": (
            "Greek energeia (coined by Aristotle for being-at-work) -> Latin actualitas "
            "(coined by medieval Scholastics specifically to translate energeia)."
        ),
        "shares_4char_substring": shares_4char_substring("actual", "energy", strict_latinate=True),
        "graph_presence_audit": {
            "in_g_tsr_pure_table": calque_edge in g_tsr_pure_table,
            "in_g_tsr_frozen": calque_edge in g_tsr_frozen,
            "in_unblinded_diagram_concordance": calque_edge in g_tsr_canonical,
            "candor_note": (
                "In `vocab/mirror.py`, `actualization` is paired horizontally with `realization` "
                "(`role='transmutation'`) without an explicit string link to `'energy'`, so "
                "`('actual', 'energy')` is NOT counted as an overlap hit in either `g_tsr_pure_table` "
                "or `g_tsr_frozen`; Test III.2 evaluates the diagram-hinge localization directly."
            ),
        },
        "exact_probabilities": {
            "uniform_blind_exact_physical_hinge_edge": {
                "n_blind_pairs": n_blind_pairs_strict,
                "fraction": f"{p_exact_right_blind.numerator}/{p_exact_right_blind.denominator}",
                "float": float(p_exact_right_blind),
            },
            "uniform_blind_either_hinge_transmutation_edge": {
                "n_blind_pairs": n_blind_pairs_strict,
                "fraction": f"{p_either_hinge_blind.numerator}/{p_either_hinge_blind.denominator}",
                "float": float(p_either_hinge_blind),
            },
            "uniform_exact_physical_hinge_edge": {
                "total_word_pairs": total_pairs,
                "fraction": f"{p_exact_right_all.numerator}/{p_exact_right_all.denominator}",
                "float": float(p_exact_right_all),
            },
            "uniform_either_hinge_transmutation_edge": {
                "total_word_pairs": total_pairs,
                "fraction": f"{p_either_hinge_all.numerator}/{p_either_hinge_all.denominator}",
                "float": float(p_either_hinge_all),
            },
            "uniform_any_edge_of_g_tsr_pure_table": {
                "fraction": f"{p_in_pure_table.numerator}/{p_in_pure_table.denominator}",
                "float": float(p_in_pure_table),
            },
            "uniform_any_edge_of_g_tsr_frozen": {
                "fraction": f"{p_in_frozen_repo.numerator}/{p_in_frozen_repo.denominator}",
                "float": float(p_in_frozen_repo),
            },
            "process_stratum_conditioned_right_transmutation": {
                "process_pool_size": n_process,
                "fraction": f"{p_role_conditioned_right.numerator}/{p_role_conditioned_right.denominator}",
                "float": float(p_role_conditioned_right),
            },
            "process_stratum_conditioned_either_transmutation": {
                "process_pool_size": n_process,
                "fraction": f"{p_role_conditioned_either.numerator}/{p_role_conditioned_either.denominator}",
                "float": float(p_role_conditioned_either),
            },
        },
    }


def run_test_iii_3_directionality_audit(words: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Test III.3: Within-Physics Directional Asymmetry ('Mr. Newton Goes Shopping')
    & Pre-Etymology `core_law` Grounding Audit.

    Removes the circular all-80 Fisher test from headline inferential status:
    in *What the Words Knew* (p. 95), `"inward first"` means a word that *"began in
    human life and was later handed to physics"*, making the 45 `not_physics_term`
    words structurally ineligible (`0/45` by definition). Leads strictly with valid
    within-physics comparisons (`core_law` vs `secondary_physics`).
    """
    kind_counts = Counter(w["kind"] for w in words)
    assert sum(kind_counts.values()) == 80

    core_law = [w for w in words if w["physics_stratum"] == "core_law"]
    sec_phys = [w for w in words if w["physics_stratum"] == "secondary_physics"]
    non_phys = [w for w in words if w["physics_stratum"] == "not_physics_term"]
    assert len(core_law) == 21 and len(sec_phys) == 14 and len(non_phys) == 45

    # Verify every core_law word has a non-empty pre_etymology_citation in ledger_80.json
    core_law_citations: dict[str, str] = {}
    for w in sorted(core_law, key=lambda x: x["word"]):
        cit = w.get("pre_etymology_citation")
        assert isinstance(cit, str) and len(cit.strip()) > 20, (
            f"core_law word {w['word']!r} lacks pre_etymology_citation!"
        )
        core_law_citations[w["word"]] = cit

    inward_core = sorted(w["word"] for w in core_law if w["kind"] == "inward first")
    inward_sec = sorted(w["word"] for w in sec_phys if w["kind"] == "inward first")
    inward_nonphys = sorted(w["word"] for w in non_phys if w["kind"] == "inward first")
    outward_core = sorted(w["word"] for w in core_law if w["kind"] == "outward first")
    outward_sec = sorted(w["word"] for w in sec_phys if w["kind"] == "outward first")
    either_side_phys = sorted(w["word"] for w in core_law + sec_phys if w["kind"] == "either side")
    household_phys = sorted(w["word"] for w in core_law + sec_phys if w["kind"] == "household")

    assert inward_core == ["energy", "force", "inertia", "power", "work"]
    assert inward_sec == []
    assert inward_nonphys == []
    assert outward_core == ["attraction"]
    assert len(outward_sec) == 8

    # HEADLINE 1: Exact Fisher one-sided test on unambiguous directional physics metaphors
    # core_law: 5 inward ('energy, force, inertia, power, work') vs 1 outward ('attraction')
    # secondary_physics: 0 inward vs 8 outward ('converge, culminate, friction, limit, reflection, resonance, tension, vortex')
    n_dir_core = len(inward_core) + len(outward_core)  # 6
    n_dir_sec = len(inward_sec) + len(outward_sec)     # 8
    p_fisher_dir_phys = exact_hypergeometric_upper_tail(
        total_pop=n_dir_core + n_dir_sec,
        pop_successes=len(inward_core) + len(inward_sec),
        draws=n_dir_core,
        obs_k=len(inward_core),
    )
    or_dir_phys = exact_odds_ratio_and_haldane(
        a=len(inward_core),
        b=len(outward_core),
        c=len(inward_sec),
        d=len(outward_sec),
    )

    # HEADLINE 2: Exact Fisher one-sided test across ALL 35 physics words
    # (scoring all mixed/neutral/ambiguous kinds — 'household', 'either side', 'family',
    # 'both ways', 'nothing to add', 'not used' — conservatively as 0 / non-inward)
    p_fisher_all35_phys = exact_hypergeometric_upper_tail(
        total_pop=len(core_law) + len(sec_phys),  # 35
        pop_successes=len(inward_core),           # 5
        draws=len(core_law),                      # 21
        obs_k=len(inward_core),                   # 5
    )
    or_all35_phys = exact_odds_ratio_and_haldane(
        a=len(inward_core),
        b=len(core_law) - len(inward_core),
        c=len(inward_sec),
        d=len(sec_phys) - len(inward_sec),
    )

    # HEADLINE 3: Exact rational binomial upper-tail bounds against historical
    # reverse-metaphor base rates q_0 in {0.05, 0.10, 0.15}
    worst_case_core_pool = sorted(
        w["word"] for w in core_law if w["kind"] not in ("family", "both ways")
    )
    n_worst_core = len(worst_case_core_pool)  # 15

    binomial_bounds: dict[str, Any] = {}
    for denom_key, n_trials, desc in (
        (
            "directional_core_law_5_of_6",
            n_dir_core,
            "Unambiguous directional metaphors in core_law (5 inward vs 1 outward ['attraction'])",
        ),
        (
            "worst_case_nonfamily_core_law_5_of_15",
            n_worst_core,
            "Scores ALL 'either side' (gravity, matter, pressure), 'household' (density, electric, mass, volume), "
            "'nothing to add' (accelerate), and 'not used' (light) in core_law against TSR",
        ),
        (
            "all_core_law_5_of_21",
            len(core_law),
            "Ultra-conservative denominator across all 21 core_law words (including 'family' and 'both ways')",
        ),
    ):
        per_q: dict[str, Any] = {}
        for q_str, q_frac in (
            ("q0_0.05", Fraction(1, 20)),
            ("q0_0.10", Fraction(1, 10)),
            ("q0_0.15", Fraction(3, 20)),
        ):
            bt = exact_binomial_upper_tail(n_trials=n_trials, k_obs=5, p0=q_frac)
            per_q[q_str] = {
                "base_rate_fraction": f"{q_frac.numerator}/{q_frac.denominator}",
                "exact_fraction": f"{bt.numerator}/{bt.denominator}",
                "p_value": float(bt),
            }
        binomial_bounds[denom_key] = {
            "k_of_n": f"5/{n_trials}",
            "denominator_description": desc,
            "bounds_by_base_rate": per_q,
        }

    # SENSITIVITY: Sovereign Mirror manuscript-only core_law (holding out Oct 2026
    # Extension Test / Author Ruling words `work` and `power`)
    p_sm_book_holdout_dir = exact_hypergeometric_upper_tail(
        total_pop=4 + 8, pop_successes=3, draws=4, obs_k=3
    )
    p_sm_book_holdout_all33 = exact_hypergeometric_upper_tail(
        total_pop=19 + 14, pop_successes=3, draws=19, obs_k=3
    )
    p_sm_book_reclass_dir = exact_hypergeometric_upper_tail(
        total_pop=4 + 10, pop_successes=5, draws=4, obs_k=3
    )

    # DESCRIPTIVE ONLY (demoted from headline inferential reporting):
    p_descriptive_all80 = exact_hypergeometric_upper_tail(
        total_pop=80, pop_successes=5, draws=21, obs_k=5
    )

    return {
        "methodological_correction_note": (
            "In What the Words Knew ('Every Word, for the Record', p. 95), 'inward first' is defined as "
            "a word that 'began in human life and was later handed to physics'. Consequently, the 45 "
            "`not_physics_term` words in the 80-word ledger are structurally ineligible to be 'inward first' "
            "(0/45 is guaranteed by definition), making an all-80 Fisher test circular. All headline "
            "inferential tests below are restricted strictly to the 35 physics words (`core_law` vs "
            "`secondary_physics`), with the 80-word tally retained solely as a descriptive ledger summary."
        ),
        "ledger_total_words": 80,
        "eligible_physics_words_total": len(core_law) + len(sec_phys),
        "structurally_ineligible_not_physics_term_count": len(non_phys),
        "full_80_kind_distribution": dict(sorted(kind_counts.items())),
        "strata_sizes": {
            "core_law": len(core_law),
            "secondary_physics": len(sec_phys),
            "not_physics_term_excluded_from_inference": len(non_phys),
        },
        "inward_first_core_law_words": inward_core,
        "inward_first_secondary_physics_words": inward_sec,
        "outward_first_core_law_words": outward_core,
        "outward_first_secondary_physics_words": outward_sec,
        "either_side_physics_words_scored_zero": either_side_phys,
        "household_physics_words_scored_zero": household_phys,
        "headline_within_physics_inferential_tests": {
            "fisher_directional_physics_core_vs_secondary": {
                "contingency": (
                    f"{len(inward_core)} inward / {len(outward_core)} outward in core_law vs "
                    f"{len(inward_sec)} inward / {len(outward_sec)} outward in secondary_physics"
                ),
                "exact_fraction": f"{p_fisher_dir_phys.numerator}/{p_fisher_dir_phys.denominator}",
                "p_value": float(p_fisher_dir_phys),
                **or_dir_phys,
            },
            "fisher_all_35_physics_words_core_vs_secondary": {
                "contingency": "5/21 in core_law vs 0/14 in secondary_physics (all mixed/neutral physics words scored 0)",
                "exact_fraction": f"{p_fisher_all35_phys.numerator}/{p_fisher_all35_phys.denominator}",
                "p_value": float(p_fisher_all35_phys),
                "exceeds_0_05_alpha": float(p_fisher_all35_phys) > 0.05,
                "candor_note": (
                    "When all 15 non-directional core_law words and 6 non-directional secondary_physics "
                    "words are pooled as non-hits, the one-sided 35-word Fisher exact p-value is "
                    "171/2728 ≈ 0.0627 (> 0.05)."
                ),
                **or_all35_phys,
            },
            "binomial_reverse_metaphor_upper_tail_bounds": binomial_bounds,
            "sovereign_mirror_book_only_sensitivity": {
                "description": (
                    "Sensitivity check holding out `work` and `power` (whose pre-etymology grounding comes "
                    "from the 2026-10-22 Extension Test and October 2026 Author Ruling rather than the "
                    "main chapters of The Sovereign Mirror), leaving `energy`, `force`, `inertia` in core_law."
                ),
                "holdout_directional_3_of_4_vs_0_of_8": {
                    "exact_fraction": f"{p_sm_book_holdout_dir.numerator}/{p_sm_book_holdout_dir.denominator}",
                    "p_value": float(p_sm_book_holdout_dir),
                },
                "holdout_all_physics_3_of_19_vs_0_of_14": {
                    "exact_fraction": f"{p_sm_book_holdout_all33.numerator}/{p_sm_book_holdout_all33.denominator}",
                    "p_value": float(p_sm_book_holdout_all33),
                },
                "reclassified_to_secondary_directional_3_of_4_vs_2_of_10": {
                    "exact_fraction": f"{p_sm_book_reclass_dir.numerator}/{p_sm_book_reclass_dir.denominator}",
                    "p_value": float(p_sm_book_reclass_dir),
                },
            },
        },
        "core_law_pre_etymology_citations": core_law_citations,
        "descriptive_80_word_ledger_concentration_summary": {
            "inferential_status": "DESCRIPTIVE_CONCENTRATION_SUMMARY_ONLY_NOT_INFERENTIAL",
            "structural_ineligibility_reason": (
                "45 of the 59 non-core_law words are `not_physics_term` and therefore cannot be "
                "'handed to physics' (`inward first`) by definition; do NOT cite this hypergeometric "
                "ratio as an inferential hypothesis test."
            ),
            "ledger_tally": "5/21 in core_law vs 0/14 in secondary_physics and 0/45 in not_physics_term",
            "descriptive_hypergeometric_ratio_fraction": (
                f"{p_descriptive_all80.numerator}/{p_descriptive_all80.denominator}"
            ),
            "descriptive_hypergeometric_ratio_float": float(p_descriptive_all80),
        },
    }


def run_self_tests(
    words: list[dict[str, Any]],
    word_by_name: dict[str, dict[str, Any]],
    blind_pairs_strict: set[tuple[str, str]],
    excluded_strict: list[tuple[str, str]],
    blind_pairs_legacy: set[tuple[str, str]],
    g_pure_strict: set[tuple[str, str]],
    g_frozen_strict: set[tuple[str, str]],
    etym_strict_filter: dict[str, set[tuple[str, str]]],
    strict_alignments: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """
    Internal deterministic self-assertion suite verifying all four Leak fixes (1-4)
    and Checklist items (3.1-3.4) on every run.
    """
    smap = build_surface_to_ledger_map(words)

    # 1. Leak #3A: Surface-to-ledger stem leak assertions
    assert extract_ledger_words(
        "Subjective Reality and Objective Reality; vibrational and subjective realities; make real",
        smap,
    ) == {"subject", "object", "vibration"}, "Leak #3A failure: 'real'/'reality'/'realities' leaked!"
    assert "realize" not in extract_ledger_words("real reality realities", smap)
    assert extract_ledger_words(
        "present moment; Movement times Appreciation; Rows 11 and 12 become forceable; Two senses: limitless",
        smap,
    ) == {"present", "movement", "appreciate"}, "Leak #3A failure: false-friend token leaked!"

    # Scan every token across all frozen code structures
    frozen_texts: list[str] = []
    for phys, non, _r in MIRROR:
        frozen_texts.extend([phys, non])
    for l_str, r_str in DIAGONAL:
        frozen_texts.extend([l_str, r_str])
    for k, v in EXTENDED_PARTNERS.items():
        frozen_texts.extend([k, v])
    for k, v in GLOSSARY_SENSES.items():
        frozen_texts.extend([k, v])
    for k, v in AUTHOR_RULING_SOURCES.items():
        frozen_texts.extend([k, v])
    for k, (_op, rhs) in list(PHYS.items()) + list(NONPHYS_STATED.items()) + list(EXTENSION.items()):
        frozen_texts.extend([k, " ".join(rhs)])
    for r in ROWS:
        frozen_texts.extend([r[0], r[5]])

    all_frozen_tokens = {
        tok for txt in frozen_texts for tok in re.findall(r"[a-zA-Z]+", txt.lower())
    }
    mapped_frozen_tokens = sorted(tok for tok in all_frozen_tokens if tok in smap)
    for tok in mapped_frozen_tokens:
        assert tok not in FORBIDDEN_SURFACE_TOKENS
        assert smap[tok] in word_by_name

    # 2. Leak #3B: momentum-movement Latinate -mentum/-ment filter & full K_80 morphology check
    assert shares_4char_substring("momentum", "movement", strict_latinate=True) is True
    assert shares_4char_substring("momentum", "movement", strict_latinate=False) is False
    assert ("momentum", "movement") not in blind_pairs_strict
    assert ("momentum", "movement") in excluded_strict
    assert ("momentum", "movement") in blind_pairs_legacy
    assert len(blind_pairs_strict) == 3152
    assert len(blind_pairs_legacy) == 3153
    assert g_pure_strict <= g_frozen_strict, "g_tsr_pure_table must be a subset of g_tsr_frozen!"

    # 3. Leak #3C & #3D: Dual PIE root standards & calque vs classical_sense_overlap labels
    assert word_by_name["converge"]["pie_roots_strict"] == ["PIE:*h1werg-"]
    assert word_by_name["vortex"]["pie_roots_strict"] == ["PIE:*wert-"]
    assert set(word_by_name["converge"]["pie_roots_strict"]).isdisjoint(
        word_by_name["vortex"]["pie_roots_strict"]
    )
    assert word_by_name["converge"]["pie_roots_pokorny"] == ["PIE:*wer-turn"]
    assert word_by_name["vortex"]["pie_roots_pokorny"] == ["PIE:*wer-turn"]
    assert ("converge", "vortex") not in etym_strict_filter["strict_pie"]
    assert ("converge", "vortex") in etym_strict_filter["pokorny_pie"]
    assert etym_strict_filter["pokorny_pie"] - etym_strict_filter["strict_pie"] == {
        ("converge", "vortex")
    }

    for w_calq in ("actual", "energy"):
        assert word_by_name[w_calq]["classical_link_type"] == "coined_translation_calque"
        assert word_by_name[w_calq]["classical_link_category"] == "translation_calque"
    for w_sense in ("desire", "expect"):
        assert word_by_name[w_sense]["classical_link_type"] == "classical_sense_overlap"
        assert word_by_name[w_sense]["classical_link_category"] == "classical_polysemy_parallel"
        assert word_by_name[w_sense]["calque_group"] is None

    # 4. Leak #4: Verify N_blind denominator & consistency with QAP / stratified permutations
    for al_key, al_val in strict_alignments.items():
        assert al_val["n_blind_pairs"] == 3152, f"{al_key} did not use N_blind=3152!"
        assert al_val["hypergeometric_total_pop_used"] == 3152
        # Verify 100k stratified permutation empirical mean matches exact analytical vertex-perm mean
        emp_mu = al_val["stratified_permutation_100k_crosscheck"]["empirical_mean"]
        exact_mu = al_val["exact_pos_and_polysemy_stratified_mean"]["float"]
        assert abs(emp_mu - exact_mu) < 0.02, (
            f"Stratified permutation mean mismatch on {al_key}: {emp_mu} vs {exact_mu}"
        )
        # Blind-pair-conditioned stratified mean must be >= vertex-perm mean (since N_blind <= 3160)
        assert (
            al_val["exact_pos_and_polysemy_stratified_mean"]["blind_pair_conditioned_float"]
            + 1e-12
            >= exact_mu
        )

    # Verify batched permutation runner matches standalone bit-for-bit on 500 trials
    sample_edges_etym = etym_strict_filter["diachronic_strict_pie"]
    standalone_500 = run_stratified_permutation_crosscheck(
        words,
        g_pure_strict,
        sample_edges_etym,
        obs_overlap=len(g_pure_strict & sample_edges_etym),
        stratum_fn=lambda w: (w["pos"], w["polysemy_tier"]),
        n_trials=500,
        seed=20191007,
    )
    batched_500 = run_batched_stratified_permutation_crosscheck(
        words,
        [("check", g_pure_strict, sample_edges_etym, len(g_pure_strict & sample_edges_etym))],
        stratum_fn=lambda w: (w["pos"], w["polysemy_tier"]),
        n_trials=500,
        seed=20191007,
    )["check"]
    assert standalone_500 == batched_500

    # 5. Leak #1: Verify all 21 core_law words carry pre_etymology_citation & non_phys has 0 inward_first
    core_words = [w for w in words if w["physics_stratum"] == "core_law"]
    assert len(core_words) == 21
    for cw in core_words:
        assert cw.get("pre_etymology_citation") and len(cw["pre_etymology_citation"]) > 20
    assert [w["word"] for w in words if w["physics_stratum"] == "not_physics_term" and w["kind"] == "inward first"] == []

    return {
        "all_passed": True,
        "frozen_unique_tokens_audited": len(all_frozen_tokens),
        "frozen_mapped_tokens_count": len(mapped_frozen_tokens),
        "forbidden_tokens_verified_unmapped": sorted(FORBIDDEN_SURFACE_TOKENS),
        "strict_n_blind_pairs": len(blind_pairs_strict),
        "legacy_n_blind_pairs": len(blind_pairs_legacy),
        "excluded_nonblind_pairs_strict": [list(e) for e in excluded_strict],
        "pokorny_minus_strict_pie_pairs": [["converge", "vortex"]],
        "core_law_pre_etymology_citations_verified": len(core_words),
        "pure_table_subset_of_frozen_verified": True,
    }


def _compact_summary_row(al: dict[str, Any]) -> dict[str, Any]:
    return {
        "tsr_edges": al["tsr_edge_count"],
        "etymology_edges": al["etymology_edge_count"],
        "n_blind_pairs": al["n_blind_pairs"],
        "observed_overlap": al["observed_overlap_count"],
        "overlapping_pairs": al["overlapping_pairs"],
        "blind_hypergeometric_mean": round(
            al["exact_blind_pair_hypergeometric_moments"]["mean_float"], 4
        ),
        "exact_hypergeometric_p_fraction": al["exact_hypergeometric_p_fraction"],
        "exact_hypergeometric_p_float": al["exact_hypergeometric_p_float"],
        "pos_polysemy_stratified_mean_blind": round(
            al["exact_pos_and_polysemy_stratified_mean"]["blind_pair_conditioned_float"], 4
        ),
        "stratified_perm_100k_p_upper_bound": al["stratified_permutation_100k_crosscheck"][
            "empirical_p_upper_bound"
        ],
    }


def run_combinatorial_proofs() -> dict[str, Any]:
    words = load_ledger()
    word_by_name = {w["word"]: w for w in words}

    # Build strict (-mentum/-ment, primary: N_blind=3152) and legacy (4-char: N_blind=3153) universes
    blind_pairs_strict, excluded_strict = compute_blind_pair_universe(words, strict_latinate=True)
    blind_pairs_legacy, excluded_legacy = compute_blind_pair_universe(words, strict_latinate=False)

    etym_strict = build_hidden_etymology_graphs(words, strict_latinate=True)
    etym_legacy = build_hidden_etymology_graphs(words, strict_latinate=False)

    g_pure_strict = build_programmatic_pure_table_graph(words, strict_latinate=True)
    g_frozen_strict = build_programmatic_frozen_mirror_graph(words, strict_latinate=True)
    g_canon_strict = build_canonical_tsr_graph(words, strict_latinate=True)

    g_pure_legacy = build_programmatic_pure_table_graph(words, strict_latinate=False)
    g_frozen_legacy = build_programmatic_frozen_mirror_graph(words, strict_latinate=False)

    # Batch all 100,000-trial (pos, polysemy_tier)-stratified permutation checks in one pass
    perm_tasks: list[tuple[str, set[tuple[str, str]], set[tuple[str, str]], int]] = [
        # Primary strict filter (N_blind = 3,152)
        ("strict__pure__strict_pie", g_pure_strict, etym_strict["strict_pie"], len(g_pure_strict & etym_strict["strict_pie"])),
        ("strict__pure__pokorny_pie", g_pure_strict, etym_strict["pokorny_pie"], len(g_pure_strict & etym_strict["pokorny_pie"])),
        ("strict__pure__strict_pie_calque_only", g_pure_strict, etym_strict["strict_pie_plus_translation_calque"], len(g_pure_strict & etym_strict["strict_pie_plus_translation_calque"])),
        ("strict__pure__diachronic_strict_pie", g_pure_strict, etym_strict["diachronic_strict_pie"], len(g_pure_strict & etym_strict["diachronic_strict_pie"])),
        ("strict__pure__diachronic_pokorny_pie", g_pure_strict, etym_strict["diachronic_pokorny_pie"], len(g_pure_strict & etym_strict["diachronic_pokorny_pie"])),
        ("strict__frozen__strict_pie", g_frozen_strict, etym_strict["strict_pie"], len(g_frozen_strict & etym_strict["strict_pie"])),
        ("strict__frozen__pokorny_pie", g_frozen_strict, etym_strict["pokorny_pie"], len(g_frozen_strict & etym_strict["pokorny_pie"])),
        ("strict__frozen__strict_pie_calque_only", g_frozen_strict, etym_strict["strict_pie_plus_translation_calque"], len(g_frozen_strict & etym_strict["strict_pie_plus_translation_calque"])),
        ("strict__frozen__diachronic_strict_pie", g_frozen_strict, etym_strict["diachronic_strict_pie"], len(g_frozen_strict & etym_strict["diachronic_strict_pie"])),
        ("strict__frozen__diachronic_pokorny_pie", g_frozen_strict, etym_strict["diachronic_pokorny_pie"], len(g_frozen_strict & etym_strict["diachronic_pokorny_pie"])),
        # Legacy 4-char filter side-by-side (N_blind = 3,153, includes momentum-movement)
        ("legacy__pure__strict_pie", g_pure_legacy, etym_legacy["strict_pie"], len(g_pure_legacy & etym_legacy["strict_pie"])),
        ("legacy__pure__pokorny_pie", g_pure_legacy, etym_legacy["pokorny_pie"], len(g_pure_legacy & etym_legacy["pokorny_pie"])),
        ("legacy__pure__diachronic_strict_pie", g_pure_legacy, etym_legacy["diachronic_strict_pie"], len(g_pure_legacy & etym_legacy["diachronic_strict_pie"])),
        ("legacy__pure__diachronic_pokorny_pie", g_pure_legacy, etym_legacy["diachronic_pokorny_pie"], len(g_pure_legacy & etym_legacy["diachronic_pokorny_pie"])),
        ("legacy__frozen__strict_pie", g_frozen_legacy, etym_legacy["strict_pie"], len(g_frozen_legacy & etym_legacy["strict_pie"])),
        ("legacy__frozen__pokorny_pie", g_frozen_legacy, etym_legacy["pokorny_pie"], len(g_frozen_legacy & etym_legacy["pokorny_pie"])),
        ("legacy__frozen__diachronic_strict_pie", g_frozen_legacy, etym_legacy["diachronic_strict_pie"], len(g_frozen_legacy & etym_legacy["diachronic_strict_pie"])),
        ("legacy__frozen__diachronic_pokorny_pie", g_frozen_legacy, etym_legacy["diachronic_pokorny_pie"], len(g_frozen_legacy & etym_legacy["diachronic_pokorny_pie"])),
        # Unblinded descriptive concordance (quarantined)
        ("desc__canon__strict_pie", g_canon_strict, etym_strict["strict_pie"], len(g_canon_strict & etym_strict["strict_pie"])),
        ("desc__canon__diachronic_pokorny_pie", g_canon_strict, etym_strict["diachronic_pokorny_pie"], len(g_canon_strict & etym_strict["diachronic_pokorny_pie"])),
    ]
    perm_results = run_batched_stratified_permutation_crosscheck(
        words=words,
        tasks=perm_tasks,
        stratum_fn=lambda w: (w["pos"], w["polysemy_tier"]),
        n_trials=100_000,
        seed=20191007,
    )

    def eval_strict(label: str, status: str, g_tsr: set[tuple[str, str]], g_etym: set[tuple[str, str]], pkey: str) -> dict[str, Any]:
        return evaluate_graph_alignment(
            label, status, words, word_by_name, blind_pairs_strict, g_tsr, g_etym, perm_results[pkey]
        )

    def eval_legacy(label: str, status: str, g_tsr: set[tuple[str, str]], g_etym: set[tuple[str, str]], pkey: str) -> dict[str, Any]:
        return evaluate_graph_alignment(
            label, status, words, word_by_name, blind_pairs_legacy, g_tsr, g_etym, perm_results[pkey]
        )

    # Primary strict-filter alignments (g_tsr_pure_table FIRST, then g_tsr_frozen)
    strict_alignments = {
        "pure_table_vs_strict_pie": eval_strict(
            "III_1A_Pure_PIE_Strict_Laryngeal",
            "PRIMARY_BLIND_PURE_TABLE_STRICT_MENTUM_FILTER",
            g_pure_strict,
            etym_strict["strict_pie"],
            "strict__pure__strict_pie",
        ),
        "pure_table_vs_pokorny_pie": eval_strict(
            "III_1A_Pure_PIE",
            "PRIMARY_BLIND_PURE_TABLE_STRICT_MENTUM_FILTER",
            g_pure_strict,
            etym_strict["pokorny_pie"],
            "strict__pure__pokorny_pie",
        ),
        "pure_table_vs_strict_pie_plus_translation_calque_only": eval_strict(
            "III_1A_Strict_PIE_Plus_Coined_Translation_Calque_Only",
            "PRIMARY_BLIND_PURE_TABLE_STRICT_MENTUM_FILTER",
            g_pure_strict,
            etym_strict["strict_pie_plus_translation_calque"],
            "strict__pure__strict_pie_calque_only",
        ),
        "pure_table_vs_diachronic_strict_pie": eval_strict(
            "III_1A_Diachronic_Strict_Laryngeal",
            "PRIMARY_BLIND_PURE_TABLE_STRICT_MENTUM_FILTER",
            g_pure_strict,
            etym_strict["diachronic_strict_pie"],
            "strict__pure__diachronic_strict_pie",
        ),
        "pure_table_vs_diachronic_pokorny_pie": eval_strict(
            "III_1A_Diachronic",
            "PRIMARY_BLIND_PURE_TABLE_STRICT_MENTUM_FILTER",
            g_pure_strict,
            etym_strict["diachronic_pokorny_pie"],
            "strict__pure__diachronic_pokorny_pie",
        ),
        "frozen_code_vs_strict_pie": eval_strict(
            "III_1B_Pure_PIE_Strict_Laryngeal",
            "BLIND_FROZEN_REPO_CODE_STRICT_MENTUM_FILTER",
            g_frozen_strict,
            etym_strict["strict_pie"],
            "strict__frozen__strict_pie",
        ),
        "frozen_code_vs_pokorny_pie": eval_strict(
            "III_1B_Pure_PIE",
            "BLIND_FROZEN_REPO_CODE_STRICT_MENTUM_FILTER",
            g_frozen_strict,
            etym_strict["pokorny_pie"],
            "strict__frozen__pokorny_pie",
        ),
        "frozen_code_vs_strict_pie_plus_translation_calque_only": eval_strict(
            "III_1C_Strict_PIE_Plus_Coined_Translation_Calque_Only",
            "BLIND_FROZEN_REPO_CODE_STRICT_MENTUM_FILTER",
            g_frozen_strict,
            etym_strict["strict_pie_plus_translation_calque"],
            "strict__frozen__strict_pie_calque_only",
        ),
        "frozen_code_vs_diachronic_strict_pie": eval_strict(
            "III_1C_Diachronic_Strict_Laryngeal",
            "BLIND_FROZEN_REPO_CODE_STRICT_MENTUM_FILTER",
            g_frozen_strict,
            etym_strict["diachronic_strict_pie"],
            "strict__frozen__diachronic_strict_pie",
        ),
        "frozen_code_vs_diachronic_pokorny_pie": eval_strict(
            "III_1C_Diachronic",
            "BLIND_FROZEN_REPO_CODE_STRICT_MENTUM_FILTER",
            g_frozen_strict,
            etym_strict["diachronic_pokorny_pie"],
            "strict__frozen__diachronic_pokorny_pie",
        ),
    }

    # Legacy 4-char filter side-by-side alignments (Checklist §3.2)
    legacy_alignments = {
        "pure_table_vs_strict_pie": eval_legacy(
            "Legacy4Char_III_1A_Pure_PIE_Strict_Laryngeal",
            "SENSITIVITY_LEGACY_4CHAR_FILTER_INCLUDES_MOMENTUM_MOVEMENT",
            g_pure_legacy,
            etym_legacy["strict_pie"],
            "legacy__pure__strict_pie",
        ),
        "pure_table_vs_pokorny_pie": eval_legacy(
            "Legacy4Char_III_1A_Pure_PIE",
            "SENSITIVITY_LEGACY_4CHAR_FILTER_INCLUDES_MOMENTUM_MOVEMENT",
            g_pure_legacy,
            etym_legacy["pokorny_pie"],
            "legacy__pure__pokorny_pie",
        ),
        "pure_table_vs_diachronic_strict_pie": eval_legacy(
            "Legacy4Char_III_1A_Diachronic_Strict_Laryngeal",
            "SENSITIVITY_LEGACY_4CHAR_FILTER_INCLUDES_MOMENTUM_MOVEMENT",
            g_pure_legacy,
            etym_legacy["diachronic_strict_pie"],
            "legacy__pure__diachronic_strict_pie",
        ),
        "pure_table_vs_diachronic_pokorny_pie": eval_legacy(
            "Legacy4Char_III_1A_Diachronic",
            "SENSITIVITY_LEGACY_4CHAR_FILTER_INCLUDES_MOMENTUM_MOVEMENT",
            g_pure_legacy,
            etym_legacy["diachronic_pokorny_pie"],
            "legacy__pure__diachronic_pokorny_pie",
        ),
        "frozen_code_vs_strict_pie": eval_legacy(
            "Legacy4Char_III_1B_Pure_PIE_Strict_Laryngeal",
            "SENSITIVITY_LEGACY_4CHAR_FILTER_INCLUDES_MOMENTUM_MOVEMENT",
            g_frozen_legacy,
            etym_legacy["strict_pie"],
            "legacy__frozen__strict_pie",
        ),
        "frozen_code_vs_pokorny_pie": eval_legacy(
            "Legacy4Char_III_1B_Pure_PIE",
            "SENSITIVITY_LEGACY_4CHAR_FILTER_INCLUDES_MOMENTUM_MOVEMENT",
            g_frozen_legacy,
            etym_legacy["pokorny_pie"],
            "legacy__frozen__pokorny_pie",
        ),
        "frozen_code_vs_diachronic_strict_pie": eval_legacy(
            "Legacy4Char_III_1C_Diachronic_Strict_Laryngeal",
            "SENSITIVITY_LEGACY_4CHAR_FILTER_INCLUDES_MOMENTUM_MOVEMENT",
            g_frozen_legacy,
            etym_legacy["diachronic_strict_pie"],
            "legacy__frozen__diachronic_strict_pie",
        ),
        "frozen_code_vs_diachronic_pokorny_pie": eval_legacy(
            "Legacy4Char_III_1C_Diachronic",
            "SENSITIVITY_LEGACY_4CHAR_FILTER_INCLUDES_MOMENTUM_MOVEMENT",
            g_frozen_legacy,
            etym_legacy["diachronic_pokorny_pie"],
            "legacy__frozen__diachronic_pokorny_pie",
        ),
    }

    # Unblinded descriptive concordance
    t1_desc_strict_pie = eval_strict(
        "III_1_Descriptive_Full_Book_Concordance_vs_Strict_PIE",
        "UNBLINDED_POST_HOC_DESCRIPTIVE_CONCORDANCE_ONLY",
        g_canon_strict,
        etym_strict["strict_pie"],
        "desc__canon__strict_pie",
    )
    t1_desc_diachronic_pokorny = eval_strict(
        "III_1_Descriptive_Full_Book_Concordance_vs_Diachronic_Pokorny_PIE",
        "UNBLINDED_POST_HOC_DESCRIPTIVE_CONCORDANCE_ONLY",
        g_canon_strict,
        etym_strict["diachronic_pokorny_pie"],
        "desc__canon__diachronic_pokorny_pie",
    )
    unblinded_extra_hits = [
        list(e)
        for e in sorted(
            (g_canon_strict & etym_strict["diachronic_pokorny_pie"]) - g_frozen_strict
        )
    ]

    self_test_report = run_self_tests(
        words=words,
        word_by_name=word_by_name,
        blind_pairs_strict=blind_pairs_strict,
        excluded_strict=excluded_strict,
        blind_pairs_legacy=blind_pairs_legacy,
        g_pure_strict=g_pure_strict,
        g_frozen_strict=g_frozen_strict,
        etym_strict_filter=etym_strict,
        strict_alignments=strict_alignments,
    )

    t2_hinge = run_test_iii_2_energeia_actualitas_hinge(
        words=words,
        n_blind_pairs_strict=len(blind_pairs_strict),
        g_tsr_pure_table=g_pure_strict,
        g_tsr_frozen=g_frozen_strict,
        g_tsr_canonical=g_canon_strict,
    )
    t3_directionality = run_test_iii_3_directionality_audit(words)

    return {
        "proof_id": "Part_III_Exact_Combinatorial_Etymology_Proofs",
        "source_dataset": str(LEDGER_PATH.relative_to(REPO_ROOT)),
        "self_tests": self_test_report,
        "test_III_1_hidden_root_homomorphism": {
            "methodological_note": (
                "Headline benchmarks lead with prose-free `g_tsr_pure_table` (67 strict blind edges "
                "scraped solely from `MIRROR`, `DIAGONAL`, `EXTENDED_PARTNERS`, `PHYS`, `NONPHYS_STATED`, "
                "`EXTENSION`), followed by full frozen code `g_tsr_frozen` (182 strict blind edges). "
                "All tokens are resolved via the explicit `SURFACE_TO_LEDGER` map; transparent Latinate "
                "`-mentum`/`-ment` morphology (`momentum-movement`, also subject to the Oct 2019 -> July 2020 "
                "M-slot swap, WTWK pp. 39, 93) is excluded in the primary strict filter (`N_blind = 3152`) "
                "and reported side-by-side under the legacy 4-char filter (`N_blind = 3153`); exact "
                "hypergeometric tails use `total_pop = n_blind_pairs`; and both strict laryngeal PIE "
                "(de Vaan 2008 / LIV2, splitting `converge` < *h1werg- from `vortex` < *wert-) and "
                "Pokorny PIE (`*wer-turn`) are evaluated side-by-side."
            ),
            "blind_grid_2x3_summary_strict_filter": {
                "g_tsr_pure_table": {
                    "strict_pie": _compact_summary_row(strict_alignments["pure_table_vs_strict_pie"]),
                    "pokorny_pie": _compact_summary_row(strict_alignments["pure_table_vs_pokorny_pie"]),
                    "diachronic_strict_pie": _compact_summary_row(
                        strict_alignments["pure_table_vs_diachronic_strict_pie"]
                    ),
                    "diachronic_pokorny_pie": _compact_summary_row(
                        strict_alignments["pure_table_vs_diachronic_pokorny_pie"]
                    ),
                    "strict_pie_plus_coined_calque_only": _compact_summary_row(
                        strict_alignments["pure_table_vs_strict_pie_plus_translation_calque_only"]
                    ),
                },
                "g_tsr_frozen": {
                    "strict_pie": _compact_summary_row(strict_alignments["frozen_code_vs_strict_pie"]),
                    "pokorny_pie": _compact_summary_row(strict_alignments["frozen_code_vs_pokorny_pie"]),
                    "diachronic_strict_pie": _compact_summary_row(
                        strict_alignments["frozen_code_vs_diachronic_strict_pie"]
                    ),
                    "diachronic_pokorny_pie": _compact_summary_row(
                        strict_alignments["frozen_code_vs_diachronic_pokorny_pie"]
                    ),
                    "strict_pie_plus_coined_calque_only": _compact_summary_row(
                        strict_alignments["frozen_code_vs_strict_pie_plus_translation_calque_only"]
                    ),
                },
            },
            "III_1A_Pure_PIE": strict_alignments["pure_table_vs_pokorny_pie"],
            "III_1A_Diachronic": strict_alignments["pure_table_vs_diachronic_pokorny_pie"],
            "III_1B_Pure_PIE": strict_alignments["frozen_code_vs_pokorny_pie"],
            "III_1C_Diachronic": strict_alignments["frozen_code_vs_diachronic_pokorny_pie"],
            "strict_laryngeal_pie_sensitivity": {
                "note": (
                    "Strict modern laryngeal IE (de Vaan 2008: 665, 667; LIV2 290, 691) separates "
                    "`converge` (< Lat. vergere < PIE *h1werg-) from `vortex` (< Lat. vertere < PIE *wert-); "
                    "moreover, both `converge` and `vortex` are Ch. 8 'outward first' misses in WTWK (p. 82)."
                ),
                "III_1A_Pure_PIE_Strict_Laryngeal": strict_alignments["pure_table_vs_strict_pie"],
                "III_1A_Diachronic_Strict_Laryngeal": strict_alignments[
                    "pure_table_vs_diachronic_strict_pie"
                ],
                "III_1B_Pure_PIE_Strict_Laryngeal": strict_alignments["frozen_code_vs_strict_pie"],
                "III_1C_Diachronic_Strict_Laryngeal": strict_alignments[
                    "frozen_code_vs_diachronic_strict_pie"
                ],
                "III_1A_Strict_PIE_Plus_Coined_Calque_Only": strict_alignments[
                    "pure_table_vs_strict_pie_plus_translation_calque_only"
                ],
                "III_1C_Strict_PIE_Plus_Coined_Calque_Only": strict_alignments[
                    "frozen_code_vs_strict_pie_plus_translation_calque_only"
                ],
            },
            "momentum_movement_filter_sensitivity_side_by_side": {
                "audit_note": (
                    "Side-by-side comparison of the primary strict Latinate `-mentum`/`-ment` filter "
                    "(excluding `momentum-movement`, `n_blind_pairs = 3152`) vs. the legacy 4-char filter "
                    "(including `momentum-movement`, `n_blind_pairs = 3153`; Checklist §3.2). Also notes "
                    "that `Momentum` occupied the M slot on 2019-10-07 before being replaced by `Movement` "
                    "on 2020-07-06 while `Momentum` moved to the center continuum (WTWK pp. 39, 93)."
                ),
                "strict_mentum_filter_excluding_momentum_movement": {
                    "n_blind_pairs": len(blind_pairs_strict),
                    "excluded_pairs": [list(e) for e in excluded_strict],
                    "summary": {k: _compact_summary_row(v) for k, v in strict_alignments.items()},
                },
                "legacy_4char_filter_including_momentum_movement": {
                    "n_blind_pairs": len(blind_pairs_legacy),
                    "excluded_pairs": [list(e) for e in excluded_legacy],
                    "summary": {k: _compact_summary_row(v) for k, v in legacy_alignments.items()},
                    "full_alignments": legacy_alignments,
                },
            },
            "exploratory_unblinded_descriptive_concordance": {
                "warning": (
                    "Compiled after reading What the Words Knew; includes thematic prose links "
                    "not present in `vocab/mirror.py` and must NOT be cited as a blind p-value."
                ),
                "post_hoc_extra_overlapping_pairs_not_in_frozen_code": unblinded_extra_hits,
                "canonical_vs_strict_pie": t1_desc_strict_pie,
                "canonical_vs_diachronic_pokorny_pie": t1_desc_diachronic_pokorny,
            },
        },
        "test_III_2_energeia_actualitas_hinge_localization": t2_hinge,
        "test_III_3_directional_asymmetry_within_physics": t3_directionality,
    }


if __name__ == "__main__":
    report = run_combinatorial_proofs()
    print(json.dumps(report, indent=2))
