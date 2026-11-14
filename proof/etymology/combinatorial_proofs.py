"""
combinatorial_proofs.py — Part III: Exact Combinatorial Proofs of What the Words Knew
=====================================================================================
Deterministic, LLM-free, exact rational (`fractions.Fraction` / `math.comb`) audit
over the COMPLETE 80-word ledger (`proof/etymology/ledger_80.json`, verbatim from
*What the Words Knew*, proof 36, 'Every Word, for the Record', pp. 99-104 — all
misses, 'outward first', 'household', 'either side', 'nothing to add', 'no help',
'not used', 'a pun', and 'unknown' included; cross-checked against *The Sovereign
Mirror* v57).

Pre-Declared Single Primary Test (Confirmatory Lead):
  - Primary TSR graph: `g_tsr_oct22_cdba80d` (`66` orthographically unrelated pairs
    extracted directly from the Oct 22 commit `cdba80d` artifact `tests/tsr_formal.py`,
    after asserting its SHA-256 equals
    `075fd22b9e4a9b91fa76bc433e4a754ca5faf57009fa0c071158711fba918ae0`). Combines
    `MIRROR`, `DIAGONAL`, `('gravitational pull', 'Attraction')`, `PHYS`,
    `NONPHYS_STATED`, `EXTENSION`, and `ROWS`.
  - Primary etymology graph: `pie_roots_strict` (`16` orthographically unrelated pairs
    under modern laryngeal Indo-European reconstruction: de Vaan 2008 / LIV2 /
    Kroonen 2013 / Beekes 2010).
  - Background pair pool: `N_orth_unrelated = 3,152` pairs across all `C(80, 2) = 3,160`
    word pairs after removing 8 orthographically or transparently morphologically
    related pairs via the strict Latinate `-mentum`/`-entum`/`-tum` + `-ment` + 4-char
    filter (which excludes `momentum-movement` alongside 7 4-char stem overlaps).
  - Primary Test Result: **`1` overlapping pair (`("distance", "resist")`), exact
    hypergeometric upper-tail `p = 0.2878...` (NOT statistically significant; null
    result).** This script leads with that primary test result first in docstring,
    stdout, and top-level JSON `"primary_test"`.

Multiplicity Quarantine & Provenance Safeguards:
  1. Uncorrected Exploratory / Sensitivity Section (`exploratory_sensitivity_uncorrected`):
     ALL other ~60+ `p`-values, secondary graph/root pairings, alternative null
     controls, QAP permutations, and calque probabilities are quarantined under
     `"exploratory_sensitivity_uncorrected"` with explicit notice that NONE are
     corrected for multiple comparisons. This includes:
       - `g_tsr_oct22_pure_table` (54 pairs from `tests/tsr_formal.py` without `ROWS`),
       - secondary `vocab/mirror.py` + `rule/tsr_formal_port.py` graphs (`67` and
         `182` pairs), explicitly labeled `"author-attested, first committed Nov 13"`,
       - `pokorny_pie`, `strict_pie_plus_translation_calque`, `diachronic_strict_pie`,
         and `diachronic_pokorny_pie` sensitivity variants,
       - legacy 4-char morphological filter (`N_orth_unrelated = 3,153`, retaining
         `momentum-movement`),
       - uniform `S_80` QAP vertex-permutation moments, Cantelli bounds, and 100k
         `(pos, polysemy_tier)`-stratified permutations (`seed=20191007`),
       - `actual-energy` center-crossing translation-calque localization probabilities,
       - the post-hoc prose-augmented full-book concordance (`CANONICAL_TSR_EDGES_RAW`).

  2. Descriptive `core_law` vs `secondary_physics` Kind Split:
     Any `core_law` vs `secondary_physics` Fisher / binomial concentration breakdown is
     explicitly tagged `"DESCRIPTIVE_ONLY_POST_HOC_SPLIT_NOT_INFERENTIAL"`. Because
     the `kind` labels in `ledger_80.json` were assigned by the author while drafting
     *What the Words Knew* (not blind) and the `21` vs `14` split is post hoc, those
     tallies are strictly descriptive summaries and NOT confirmatory hypothesis tests.

  3. Explicit Surface-to-Ledger Inflected Wordform Map (`SURFACE_TO_LEDGER`):
     Replaces prefix-heuristic matching with an audited exact token-to-lemma map.
     Prevents false-friend stem leaks (`"real"`, `"reality"`, `"realities"` -/->
     `"realize"`; `"moment"` -/-> `"momentum"`; `"times"` -/-> `"time"`;
     `"forceable"` -/-> `"force"`; `"senses"` -/-> `"sense"`; `"limitless"` -/->
     `"limit"`; `"radius"` -/-> `"radiate"`; `"be"` -/-> `"being"`) while mapping
     genuine inflections (`"belief"` -> `"believe"`, `"expansion"` -> `"expand"`,
     `"receptive"` -> `"receive"`, `"vibrance"` -> `"vibration"`).

  4. Pre-Etymology Grounding of the 21 `core_law` Words (Updated for Proof 36 & SM v57):
     - `accelerate`: SM v57 Ch. 2 pp. 20, 23 (`F = ma`), Map pp. 171, 173; `MIRROR`, `PHYS`.
     - `attraction`: Notebook p. 1 (2019-10-07, WTWK proof 36 p. 97); SM v57 Ch. 8 pp. 59-60, Map pp. 169-172.
     - `charge`: SM v57 Ch. 2 p. 27 (electric field around charge at rest vs closed magnetic lines); `kind='both ways'`.
     - `current`: Table (2020-07-06); SM v57 Ch. 1-2, 17 (`E = C^2 M`, `c <-> C`); `MIRROR`, `NONPHYS_STATED`.
     - `density`: SM v57 Ch. 2 pp. 20, 22, 26 (`m = density * volume`), Map pp. 172-173; `MIRROR`, `PHYS`.
     - `distance`: SM v57 Ch. 2 pp. 21, 24, Ch. 16 pp. 116, 118-119 (`#2`); `ROWS` #2 (`tests/tsr_formal.py`).
     - `electric`: Table (2020-07-06); SM v57 Ch. 2 pp. 26-27, Map pp. 172-173; `MIRROR`.
     - `energy`: Notebook p. 1 (2019-10-07, central `E`); SM v57 Ch. 2, 16 (pp. 117, 120), 17 (pp. 127-133).
     - `force`: SM v57 Ch. 2 pp. 20, 23 (`F = ma`), Ch. 10 pp. 76-79, Map pp. 170-173; `MIRROR`, `DIAGONAL`, `PHYS`.
     - `gravity`: SM v57 Ch. 8 pp. 59-60, Ch. 16 pp. 117, 121 (`#11-12`), Map pp. 170, 174; `ROWS`.
     - `inertia`: SM v57 Ch. 1 p. 16, Ch. 10 pp. 75-76; `deep-read.md`.
     - `light`: Notebook p. 1 (2019-10-07, `c`); SM v57 Ch. 2, 16 (pp. 116, 120 `#7`, `#9`), Map pp. 170-171; WTWK proof 36 p. 81 (`kind='family'`).
     - `mass`: Notebook p. 1 (2019-10-07, `m`); SM v57 Ch. 1, 2, 16 (pp. 116, 120-121), 17, Map pp. 169-173.
     - `matter`: SM v57 Ch. 2 p. 25, Ch. 10 pp. 76, 79, Ch. 18, 21; `deep-read.md`.
     - `momentum`: Notebook p. 1 (2019-10-07); SM v57 Ch. 17 pp. 129-130, Map pp. 169-175; `EXTENSION`.
     - `power`: Extension Test (2026-10-22, `tests/tsr_formal.py` `EXTENSION`); secondary `vocab/mirror.py` (`author-attested, first committed Nov 13`).
     - `pressure`: SM v57 Ch. 16 p. 118 (Boyle's law); `tests/tsr_formal.py` `ROWS` Boyle row.
     - `space`: Notebook p. 1 (2019-10-07); SM v57 Ch. 2, 16 (p. 121 `#10`), Map pp. 169-173.
     - `time`: Notebook p. 1 (2019-10-07); SM v57 Ch. 2, 15, 16 (pp. 116, 120-121 `#5`, `#10`), Map pp. 169-173.
     - `volume`: SM v57 Ch. 2 pp. 20, 22, 26 (`m = density * volume`), Ch. 16 p. 118; `MIRROR`, `PHYS`, `ROWS`.
     - `work`: Extension Test (2026-10-22, `tests/tsr_formal.py` `EXTENSION`); secondary `vocab/mirror.py` (`author-attested, first committed Nov 13`).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from vocab.mirror import (  # noqa: E402
    AUTHOR_RULING_SOURCES as NOV13_AUTHOR_RULING_SOURCES,
    DIAGONAL as NOV13_DIAGONAL,
    EXTENDED_PARTNERS as NOV13_EXTENDED_PARTNERS,
    GLOSSARY_SENSES as NOV13_GLOSSARY_SENSES,
    MIRROR as NOV13_MIRROR,
)
from rule.tsr_formal_port import (  # noqa: E402
    EXTENSION as NOV13_EXTENSION,
    NONPHYS_STATED as NOV13_NONPHYS_STATED,
    PHYS as NOV13_PHYS,
    ROWS as NOV13_ROWS,
)

LEDGER_PATH = Path(__file__).resolve().parent / "ledger_80.json"
OCT22_TSR_FORMAL_RELPATH = Path("tests") / "tsr_formal.py"
OCT22_TSR_FORMAL_PATH = REPO_ROOT / OCT22_TSR_FORMAL_RELPATH
OCT22_TSR_FORMAL_SHA256 = (
    "075fd22b9e4a9b91fa76bc433e4a754ca5faf57009fa0c071158711fba918ae0"
)
NOV13_PROVENANCE_LABEL = "author-attested, first committed Nov 13"
CORE_LAW_FISHER_STATUS = "DESCRIPTIVE_ONLY_POST_HOC_SPLIT_NOT_INFERENTIAL"

# Explicit, audited surface-token -> 80-word-ledger lemma dictionary across ALL unique
# alphabetic tokens in `tests/tsr_formal.py`, `vocab/mirror.py`, and `rule/tsr_formal_port.py`.
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

# False-friend, meta-lexicographic, antonym, and homograph tokens that MUST NEVER
# alias to a ledger word:
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


def load_oct22_tsr_formal_module() -> Any:
    """
    Verify the SHA-256 digest of `tests/tsr_formal.py` (commit `cdba80d`, 2026-10-22)
    and import its data tables cleanly without running its `__main__` block or mutating globals.
    """
    assert OCT22_TSR_FORMAL_PATH.is_file(), f"Missing Oct 22 artifact: {OCT22_TSR_FORMAL_PATH}"
    digest = hashlib.sha256(OCT22_TSR_FORMAL_PATH.read_bytes()).hexdigest()
    assert digest == OCT22_TSR_FORMAL_SHA256, (
        f"SHA-256 mismatch on {OCT22_TSR_FORMAL_RELPATH}: expected {OCT22_TSR_FORMAL_SHA256}, got {digest}"
    )
    spec = importlib.util.spec_from_file_location("tsr_formal_oct22_cdba80d", OCT22_TSR_FORMAL_PATH)
    assert spec is not None and spec.loader is not None, f"Could not create spec for {OCT22_TSR_FORMAL_PATH}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    Map alphabetic tokens in `text` strictly through `SURFACE_TO_LEDGER`
    (zero 4-char `startswith` guessing).
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
    """Legacy 4-char orthographic filter (used for morphological sensitivity checks)."""
    a, b = _strip_productive_suffix_legacy(w1.lower()), _strip_productive_suffix_legacy(w2.lower())
    if len(a) < 4 or len(b) < 4:
        return a == b
    subs_a = {a[i : i + 4] for i in range(len(a) - 3)}
    subs_b = {b[i : i + 4] for i in range(len(b) - 3)}
    return bool(subs_a & subs_b)


def shares_4char_substring(w1: str, w2: str, *, strict_latinate: bool = True) -> bool:
    """
    Orthographic and transparent-morphology filter.
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


def compute_orth_unrelated_pair_universe(
    words: list[dict[str, Any]],
    *,
    strict_latinate: bool = True,
) -> tuple[set[tuple[str, str]], list[tuple[str, str]]]:
    """
    Return `(eligible_orth_unrelated_pairs, excluded_orth_related_pairs)` across all
    `C(80, 2) = 3,160` unordered word pairs in the 80-word ledger.
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
    kc = Counter(w["kind"] for w in words)
    assert kc["family"] == 36, f"Expected family==36 in proof 36 ledger, got {kc['family']}"
    assert kc["not used"] == 1, f"Expected not used==1 in proof 36 ledger, got {kc['not used']}"
    assert sum(kc.values()) == 80
    return words


def build_hidden_etymology_graphs(
    words: list[dict[str, Any]],
    *,
    strict_latinate: bool = True,
) -> dict[str, set[tuple[str, str]]]:
    """
    Construct diachronic root and classical-link graphs over the 80 words under the
    specified orthographic filter (`strict_latinate=True` -> N_orth_unrelated=3152;
    `strict_latinate=False` -> N_orth_unrelated=3153):
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
    eligible_pairs, _ = compute_orth_unrelated_pair_universe(
        words, strict_latinate=strict_latinate
    )

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
    orth_related = shares_4char_substring(u, v, strict_latinate=True)
    if orth_related:
        rel = "orth_related_shared_latinate_morphology"
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
            "united only under Pokorny IEW 1152 *wer-; both are Ch. 8 'outward first' misses in WTWK proof 36 (p. 86)."
        )
    elif {u, v} == {"momentum", "movement"}:
        out["note"] = (
            "Shared Latinate movere + -mentum/-ment morphology; excluded from primary strict orthographically "
            "unrelated universe (also subject to 2019-10-07 -> 2020-07-06 Momentum -> Movement M-slot swap, WTWK proof 36 pp. 41, 97)."
        )
    elif {u, v} == {"desire", "expect"}:
        out["note"] = (
            "Classical Latin dictionary polysemy overlap (desiderare / exspectare 'to long for, hope for', "
            "WTWK proof 36 Ch. 2 p. 28, Ch. 5 p. 52); classified as classical_sense_overlap (classical_polysemy_parallel), NOT a calque."
        )
    elif {u, v} == {"actual", "energy"}:
        out["note"] = (
            "Coined medieval Scholastic translation calque (actualitas coined to translate Aristotle's energeia); "
            "classified as coined_translation_calque (translation_calque)."
        )
    return out


# Post-hoc prose-augmented book concordance (quarantined in exploratory section):
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


def _extract_tsr_graph_from_components(
    words: list[dict[str, Any]],
    *,
    strict_latinate: bool,
    mirror_rows: Iterable[tuple[str, str, str]],
    diagonal_rows: Iterable[tuple[str, str]],
    extra_partner_items: Iterable[tuple[str, str]],
    equation_items: Iterable[tuple[str, tuple[str, tuple[str, ...]]]],
    calibration_rows: Iterable[tuple[Any, ...]] = (),
    glossary_items: Iterable[tuple[str, str]] = (),
    ruling_items: Iterable[tuple[str, str]] = (),
) -> set[tuple[str, str]]:
    """Shared deterministic graph extractor restricted to orthographically unrelated pairs."""
    smap = build_surface_to_ledger_map(words)
    eligible_pairs, _ = compute_orth_unrelated_pair_universe(
        words, strict_latinate=strict_latinate
    )
    edges: set[tuple[str, str]] = set()

    def connect_sets(s1: set[str], s2: set[str]) -> None:
        for u in s1:
            for v in s2:
                if u != v:
                    e = _u_edge(u, v)
                    if e in eligible_pairs:
                        edges.add(e)

    for phys, non, _role in mirror_rows:
        connect_sets(extract_ledger_words(phys, smap), extract_ledger_words(non, smap))
    for left, right in diagonal_rows:
        connect_sets(extract_ledger_words(left, smap), extract_ledger_words(right, smap))
    for phys, non in extra_partner_items:
        connect_sets(extract_ledger_words(phys, smap), extract_ledger_words(non, smap))
    for lhs, (_op, rhs_tup) in equation_items:
        connect_sets(
            extract_ledger_words(lhs, smap),
            extract_ledger_words(" ".join(rhs_tup), smap),
        )
    for row in calibration_rows:
        row_name, row_src = row[0], row[5]
        connect_sets(extract_ledger_words(row_name, smap), extract_ledger_words(row_src, smap))
    for head, text in glossary_items:
        connect_sets(extract_ledger_words(head, smap), extract_ledger_words(text, smap))
    for head, text in ruling_items:
        connect_sets(extract_ledger_words(head, smap), extract_ledger_words(text, smap))

    return edges


def build_canonical_tsr_graph(
    words: list[dict[str, Any]],
    *,
    strict_latinate: bool = True,
) -> set[tuple[str, str]]:
    """Post-hoc prose-augmented book concordance restricted to `eligible_orth_unrelated_pairs`."""
    word_set = {w["word"] for w in words}
    eligible_pairs, _ = compute_orth_unrelated_pair_universe(
        words, strict_latinate=strict_latinate
    )
    edges: set[tuple[str, str]] = set()
    for u, v in CANONICAL_TSR_EDGES_RAW:
        assert u in word_set and v in word_set, f"Edge ({u}, {v}) not in 80-word ledger!"
        e = _u_edge(u, v)
        if e in eligible_pairs:
            edges.add(e)
    return edges


def build_oct22_pure_table_graph(
    words: list[dict[str, Any]],
    oct22_mod: Any,
    *,
    strict_latinate: bool = True,
) -> set[tuple[str, str]]:
    """
    `g_tsr_oct22_pure_table` (54 strict pairs): Oct 22 commit `cdba80d` (`tests/tsr_formal.py`)
    tables and algebraic equations (`MIRROR`, `DIAGONAL`, `('gravitational pull', 'Attraction')`,
    `PHYS`, `NONPHYS_STATED`, `EXTENSION`), excluding `ROWS`.
    """
    return _extract_tsr_graph_from_components(
        words,
        strict_latinate=strict_latinate,
        mirror_rows=oct22_mod.MIRROR,
        diagonal_rows=oct22_mod.DIAGONAL,
        extra_partner_items=[("gravitational pull", "Attraction")],
        equation_items=(
            list(oct22_mod.PHYS.items())
            + list(oct22_mod.NONPHYS_STATED.items())
            + list(oct22_mod.EXTENSION.items())
        ),
    )


def build_oct22_cdba80d_graph(
    words: list[dict[str, Any]],
    oct22_mod: Any,
    *,
    strict_latinate: bool = True,
) -> set[tuple[str, str]]:
    """
    PRIMARY pre-declared TSR graph (`g_tsr_oct22_cdba80d`, 66 strict pairs): full Oct 22
    commit `cdba80d` (`tests/tsr_formal.py`) extraction (`MIRROR`, `DIAGONAL`,
    `('gravitational pull', 'Attraction')`, `PHYS`, `NONPHYS_STATED`, `EXTENSION`, and `ROWS`).
    """
    return _extract_tsr_graph_from_components(
        words,
        strict_latinate=strict_latinate,
        mirror_rows=oct22_mod.MIRROR,
        diagonal_rows=oct22_mod.DIAGONAL,
        extra_partner_items=[("gravitational pull", "Attraction")],
        equation_items=(
            list(oct22_mod.PHYS.items())
            + list(oct22_mod.NONPHYS_STATED.items())
            + list(oct22_mod.EXTENSION.items())
        ),
        calibration_rows=oct22_mod.ROWS,
    )


def build_nov13_pure_table_graph(
    words: list[dict[str, Any]],
    *,
    strict_latinate: bool = True,
) -> set[tuple[str, str]]:
    """
    Secondary `g_tsr_nov13_pure_table` (67 strict pairs; author-attested, first committed
    Nov 13): `vocab/mirror.py` (`MIRROR`, `DIAGONAL`, `EXTENDED_PARTNERS`) and
    `rule/tsr_formal_port.py` (`PHYS`, `NONPHYS_STATED`, `EXTENSION`).
    """
    return _extract_tsr_graph_from_components(
        words,
        strict_latinate=strict_latinate,
        mirror_rows=NOV13_MIRROR,
        diagonal_rows=NOV13_DIAGONAL,
        extra_partner_items=NOV13_EXTENDED_PARTNERS.items(),
        equation_items=(
            list(NOV13_PHYS.items())
            + list(NOV13_NONPHYS_STATED.items())
            + list(NOV13_EXTENSION.items())
        ),
    )


def build_nov13_frozen_mirror_graph(
    words: list[dict[str, Any]],
    *,
    strict_latinate: bool = True,
) -> set[tuple[str, str]]:
    """
    Secondary `g_tsr_nov13_frozen` (182 strict pairs; author-attested, first committed
    Nov 13): `g_tsr_nov13_pure_table` plus `GLOSSARY_SENSES`, `AUTHOR_RULING_SOURCES`,
    and `ROWS`.
    """
    return _extract_tsr_graph_from_components(
        words,
        strict_latinate=strict_latinate,
        mirror_rows=NOV13_MIRROR,
        diagonal_rows=NOV13_DIAGONAL,
        extra_partner_items=NOV13_EXTENDED_PARTNERS.items(),
        equation_items=(
            list(NOV13_PHYS.items())
            + list(NOV13_NONPHYS_STATED.items())
            + list(NOV13_EXTENSION.items())
        ),
        calibration_rows=NOV13_ROWS,
        glossary_items=NOV13_GLOSSARY_SENSES.items(),
        ruling_items=NOV13_AUTHOR_RULING_SOURCES.items(),
    )


def exact_orth_unrelated_hypergeometric_moments(
    n_orth_unrelated_pairs: int,
    draws: int,
    pop_successes: int,
) -> dict[str, Any]:
    """
    Exact rational first and second moments of the hypergeometric edge-overlap count
    over the eligible orthographically unrelated pair universe of size
    `n_orth_unrelated_pairs` (< 3,160).
    """
    mean_exact = Fraction(draws * pop_successes, n_orth_unrelated_pairs)
    var_exact = (
        Fraction(draws * pop_successes, n_orth_unrelated_pairs)
        * Fraction(n_orth_unrelated_pairs - pop_successes, n_orth_unrelated_pairs)
        * Fraction(n_orth_unrelated_pairs - draws, n_orth_unrelated_pairs - 1)
    )
    return {
        "n_orth_unrelated_pairs": n_orth_unrelated_pairs,
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
    (80! ≈ 7.16e118). Because orthographically related pairs are already absent from E_A
    and E_B, any edge mapped onto an excluded vertex pair contributes 0 to T(pi).
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
    eligible_orth_unrelated_pairs: set[tuple[str, str]] | None = None,
) -> Fraction:
    """
    Compute the EXACT rational stratified expectation E_strat[T]:
      - If `eligible_orth_unrelated_pairs is None`: exact expectation over vertex permutations
        pi in prod_s S_{V_s} preserving `stratum_fn(word)`.
      - If `eligible_orth_unrelated_pairs` is provided: exact expectation over stratum-matched
        orthographically unrelated edge draws where each unordered stratum pair `(s_u, s_v)`
        uses denominator `|Pairs(s_u, s_v) cap eligible_orth_unrelated_pairs|`.
    """
    word_to_stratum = {w["word"]: stratum_fn(w) for w in words}
    stratum_sizes = Counter(word_to_stratum.values())

    orth_stratum_denoms: Counter[tuple[Any, Any]] = Counter()
    if eligible_orth_unrelated_pairs is not None:
        for u, v in eligible_orth_unrelated_pairs:
            su, sv = word_to_stratum[u], word_to_stratum[v]
            key = (su, sv) if su <= sv else (sv, su)
            orth_stratum_denoms[key] += 1

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
        if eligible_orth_unrelated_pairs is not None:
            denom = orth_stratum_denoms[key]
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
    `draws` pairs without replacement from `total_pop = n_orth_unrelated_pairs`
    eligible pairs containing `pop_successes` hidden etymology edges.
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
    """Standalone deterministic seeded permutation cross-check preserving `stratum_fn(w)`."""
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
    provenance_status: str,
    words: list[dict[str, Any]],
    word_by_name: dict[str, dict[str, Any]],
    eligible_orth_unrelated_pairs: set[tuple[str, str]],
    edges_tsr: set[tuple[str, str]],
    edges_etym: set[tuple[str, str]],
    perm_check: dict[str, Any],
) -> dict[str, Any]:
    assert edges_tsr <= eligible_orth_unrelated_pairs, (
        f"{label}: TSR graph contains orthographically related pair!"
    )
    assert edges_etym <= eligible_orth_unrelated_pairs, (
        f"{label}: Etymology graph contains orthographically related pair!"
    )

    n_words = len(words)
    all_word_pairs = math.comb(n_words, 2)
    n_orth_unrelated_pairs = len(eligible_orth_unrelated_pairs)

    overlap_edges = sorted(edges_tsr & edges_etym)
    missed_etym_edges = sorted(edges_etym - edges_tsr)
    obs = len(overlap_edges)

    orth_hyper_moments = exact_orth_unrelated_hypergeometric_moments(
        n_orth_unrelated_pairs=n_orth_unrelated_pairs,
        draws=len(edges_tsr),
        pop_successes=len(edges_etym),
    )
    qap_uniform = exact_qap_moments_uniform(n_words, edges_tsr, edges_etym)

    z_score_orth = (
        (obs - orth_hyper_moments["mean_float"]) / orth_hyper_moments["std_float"]
        if orth_hyper_moments["std_float"] > 0
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

    hyper_p = exact_hypergeometric_upper_tail(
        total_pop=n_orth_unrelated_pairs,
        pop_successes=len(edges_etym),
        draws=len(edges_tsr),
        obs_k=obs,
    )

    exp_polysemy_orth = exact_stratified_expectation(
        words,
        edges_tsr,
        edges_etym,
        stratum_fn=lambda w: w["polysemy_tier"],
        eligible_orth_unrelated_pairs=eligible_orth_unrelated_pairs,
    )
    exp_pos_polysemy_orth = exact_stratified_expectation(
        words,
        edges_tsr,
        edges_etym,
        stratum_fn=lambda w: (w["pos"], w["polysemy_tier"]),
        eligible_orth_unrelated_pairs=eligible_orth_unrelated_pairs,
    )
    exp_pos_polysemy_vertex = exact_stratified_expectation(
        words,
        edges_tsr,
        edges_etym,
        stratum_fn=lambda w: (w["pos"], w["polysemy_tier"]),
        eligible_orth_unrelated_pairs=None,
    )

    return {
        "alignment_id": label,
        "provenance_status": provenance_status,
        "total_words": n_words,
        "total_unfiltered_word_pairs": all_word_pairs,
        "n_orth_unrelated_pairs": n_orth_unrelated_pairs,
        "hypergeometric_total_pop_used": n_orth_unrelated_pairs,
        "tsr_edge_count": len(edges_tsr),
        "etymology_edge_count": len(edges_etym),
        "observed_overlap_count": obs,
        "overlapping_pairs": [list(e) for e in overlap_edges],
        "overlapping_pair_classifications": [
            classify_etymology_pair(e, word_by_name) for e in overlap_edges
        ],
        "non_overlapping_etymology_pairs": [list(e) for e in missed_etym_edges],
        "exact_orth_unrelated_hypergeometric_moments": orth_hyper_moments,
        "exact_uniform_S80_moments": qap_uniform,
        "z_score_vs_orth_unrelated_hypergeometric": round(z_score_orth, 4),
        "z_score_vs_uniform_S80": round(z_score_s80, 4),
        "exact_cantelli_upper_bound_float": float(cantelli_bound),
        "exact_hypergeometric_p_fraction": f"{hyper_p.numerator}/{hyper_p.denominator}",
        "exact_hypergeometric_p_float": float(hyper_p),
        "exact_polysemy_stratified_mean": {
            "orth_unrelated_conditioned_fraction": f"{exp_polysemy_orth.numerator}/{exp_polysemy_orth.denominator}",
            "float": float(exp_polysemy_orth),
            "enrichment_ratio": round(obs / float(exp_polysemy_orth), 2)
            if exp_polysemy_orth > 0
            else None,
        },
        "exact_pos_and_polysemy_stratified_mean": {
            "orth_unrelated_conditioned_fraction": f"{exp_pos_polysemy_orth.numerator}/{exp_pos_polysemy_orth.denominator}",
            "orth_unrelated_conditioned_float": float(exp_pos_polysemy_orth),
            "vertex_permutation_fraction": f"{exp_pos_polysemy_vertex.numerator}/{exp_pos_polysemy_vertex.denominator}",
            "float": float(exp_pos_polysemy_vertex),
            "enrichment_ratio": round(obs / float(exp_pos_polysemy_orth), 2)
            if exp_pos_polysemy_orth > 0
            else None,
            "enrichment_ratio_vertex_perm": round(obs / float(exp_pos_polysemy_vertex), 2)
            if exp_pos_polysemy_vertex > 0
            else None,
        },
        "stratified_permutation_100k_crosscheck": perm_check,
    }


def run_test_iii_2_energeia_actualitas_center_crossing(
    words: list[dict[str, Any]],
    n_orth_unrelated_pairs_strict: int,
    g_oct22_pure_table: set[tuple[str, str]],
    g_oct22_cdba80d: set[tuple[str, str]],
    g_nov13_pure_table: set[tuple[str, str]],
    g_nov13_frozen: set[tuple[str, str]],
    g_tsr_canonical: set[tuple[str, str]],
) -> dict[str, Any]:
    """
    Exploratory / Uncorrected Center-Crossing Localization: exact rational probabilities
    for the coined translation calque (`energy` [*energeia*] <-> `actual` [*actualitas*])
    landing on the central E -> physical transmutation center_crossing edge of *The Sovereign Mirror*
    v57 (The Map pp. 169-171). Quarantined under `exploratory_sensitivity_uncorrected`.
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

    p_exact_right_orth = Fraction(1, n_orth_unrelated_pairs_strict)
    p_either_center_crossing_orth = Fraction(2, n_orth_unrelated_pairs_strict)
    p_exact_right_all = Fraction(1, total_pairs)
    p_either_center_crossing_all = Fraction(2, total_pairs)
    p_in_oct22_pure = Fraction(len(g_oct22_pure_table), n_orth_unrelated_pairs_strict)
    p_in_oct22_cdba = Fraction(len(g_oct22_cdba80d), n_orth_unrelated_pairs_strict)
    p_in_nov13_pure = Fraction(len(g_nov13_pure_table), n_orth_unrelated_pairs_strict)
    p_in_nov13_frozen = Fraction(len(g_nov13_frozen), n_orth_unrelated_pairs_strict)
    p_role_conditioned_right = Fraction(1, n_process)
    p_role_conditioned_either = Fraction(2, n_process)

    calque_edge = _u_edge("actual", "energy")

    return {
        "inferential_status": "UNCORRECTED_EXPLORATORY_LOCALIZATION",
        "calque_pair": ["actual", "energy"],
        "classical_link_type": "coined_translation_calque",
        "classical_link_category": "translation_calque",
        "historical_origin": (
            "Greek energeia (coined by Aristotle for being-at-work) -> Latin actualitas "
            "(coined by medieval Scholastics specifically to translate energeia)."
        ),
        "shares_4char_substring": shares_4char_substring("actual", "energy", strict_latinate=True),
        "graph_presence_audit": {
            "in_g_tsr_oct22_pure_table": calque_edge in g_oct22_pure_table,
            "in_g_tsr_oct22_cdba80d": calque_edge in g_oct22_cdba80d,
            "in_g_tsr_nov13_pure_table": calque_edge in g_nov13_pure_table,
            "in_g_tsr_nov13_frozen": calque_edge in g_nov13_frozen,
            "in_post_hoc_diagram_concordance": calque_edge in g_tsr_canonical,
            "candor_note": (
                "In both `tests/tsr_formal.py` (Oct 22 `cdba80d`) and secondary `vocab/mirror.py` "
                "(author-attested, first committed Nov 13), `actualization` is paired horizontally with "
                "`realization` (`role='transmutation'`) without an explicit string link to `'energy'`, "
                "so `('actual', 'energy')` is NOT counted as an overlap hit in either extracted graph."
            ),
        },
        "exact_probabilities_uncorrected": {
            "uniform_orth_unrelated_exact_physical_center_crossing_edge": {
                "n_orth_unrelated_pairs": n_orth_unrelated_pairs_strict,
                "fraction": f"{p_exact_right_orth.numerator}/{p_exact_right_orth.denominator}",
                "float": float(p_exact_right_orth),
            },
            "uniform_orth_unrelated_either_center_crossing_transmutation_edge": {
                "n_orth_unrelated_pairs": n_orth_unrelated_pairs_strict,
                "fraction": f"{p_either_center_crossing_orth.numerator}/{p_either_center_crossing_orth.denominator}",
                "float": float(p_either_center_crossing_orth),
            },
            "uniform_exact_physical_center_crossing_edge": {
                "total_word_pairs": total_pairs,
                "fraction": f"{p_exact_right_all.numerator}/{p_exact_right_all.denominator}",
                "float": float(p_exact_right_all),
            },
            "uniform_either_center_crossing_transmutation_edge": {
                "total_word_pairs": total_pairs,
                "fraction": f"{p_either_center_crossing_all.numerator}/{p_either_center_crossing_all.denominator}",
                "float": float(p_either_center_crossing_all),
            },
            "uniform_any_edge_of_g_tsr_oct22_pure_table": {
                "fraction": f"{p_in_oct22_pure.numerator}/{p_in_oct22_pure.denominator}",
                "float": float(p_in_oct22_pure),
            },
            "uniform_any_edge_of_g_tsr_oct22_cdba80d": {
                "fraction": f"{p_in_oct22_cdba.numerator}/{p_in_oct22_cdba.denominator}",
                "float": float(p_in_oct22_cdba),
            },
            "uniform_any_edge_of_g_tsr_nov13_pure_table": {
                "fraction": f"{p_in_nov13_pure.numerator}/{p_in_nov13_pure.denominator}",
                "float": float(p_in_nov13_pure),
            },
            "uniform_any_edge_of_g_tsr_nov13_frozen": {
                "fraction": f"{p_in_nov13_frozen.numerator}/{p_in_nov13_frozen.denominator}",
                "float": float(p_in_nov13_frozen),
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


def run_descriptive_core_law_directionality_audit(words: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Descriptive `core_law` vs `secondary_physics` Kind Tally & Pre-Etymology Grounding.

    Inferential status: `DESCRIPTIVE_ONLY_POST_HOC_SPLIT_NOT_INFERENTIAL`.
    The `kind` labels in `proof/etymology/ledger_80.json` were assigned by the author
    while drafting *What the Words Knew* (not blind), and the `21` `core_law` vs `14`
    `secondary_physics` partition is post hoc. All Fisher / binomial ratios below are
    reported purely as descriptive ledger summaries, NOT confirmatory inferential tests.
    """
    kind_counts = Counter(w["kind"] for w in words)
    assert sum(kind_counts.values()) == 80
    assert kind_counts["family"] == 36
    assert kind_counts["not used"] == 1

    core_law = [w for w in words if w["physics_stratum"] == "core_law"]
    sec_phys = [w for w in words if w["physics_stratum"] == "secondary_physics"]
    non_phys = [w for w in words if w["physics_stratum"] == "not_physics_term"]
    assert len(core_law) == 21 and len(sec_phys) == 14 and len(non_phys) == 45

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

    # Descriptive Fisher ratios within physics words (STRICTLY DESCRIPTIVE ONLY)
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

    # In proof 36, `light` has `kind='family'`, so non-family/non-both-ways core_law pool is 14
    worst_case_core_pool = sorted(
        w["word"] for w in core_law if w["kind"] not in ("family", "both ways")
    )
    n_worst_core = len(worst_case_core_pool)  # 14
    assert n_worst_core == 14, f"Expected 14 non-family/non-both-ways core_law words, got {n_worst_core}"

    binomial_reference_summaries: dict[str, Any] = {}
    for denom_key, n_trials, desc in (
        (
            "directional_core_law_5_of_6",
            n_dir_core,
            "Directional `kind` labels in core_law (5 inward vs 1 outward ['attraction'])",
        ),
        (
            "worst_case_nonfamily_core_law_5_of_14",
            n_worst_core,
            "Pools 'either side' (gravity, matter, pressure), 'household' (density, electric, mass, volume), "
            "'nothing to add' (accelerate), and 'outward first' (attraction) as non-inward; `light` is `family` in proof 36",
        ),
        (
            "all_core_law_5_of_21",
            len(core_law),
            "All 21 core_law words (including 'family' [6 words including light] and 'both ways' [charge])",
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
                "descriptive_tail_value": float(bt),
            }
        binomial_reference_summaries[denom_key] = {
            "k_of_n": f"5/{n_trials}",
            "denominator_description": desc,
            "reference_tails_by_base_rate": per_q,
        }

    # Sensitivity counts without Oct 22 work/power rulings (purely descriptive)
    p_sm_book_holdout_dir = exact_hypergeometric_upper_tail(
        total_pop=4 + 8, pop_successes=3, draws=4, obs_k=3
    )
    p_sm_book_holdout_all33 = exact_hypergeometric_upper_tail(
        total_pop=19 + 14, pop_successes=3, draws=19, obs_k=3
    )
    p_sm_book_reclass_dir = exact_hypergeometric_upper_tail(
        total_pop=4 + 10, pop_successes=5, draws=4, obs_k=3
    )
    p_descriptive_all80 = exact_hypergeometric_upper_tail(
        total_pop=80, pop_successes=5, draws=21, obs_k=5
    )

    return {
        "inferential_status": CORE_LAW_FISHER_STATUS,
        "author_assigned_kind_labels_disclosure": (
            "The `kind` labels in proof/etymology/ledger_80.json were assigned by the author while "
            "drafting What the Words Knew (proof 36, pp. 99-104), not blind. Furthermore, the "
            "21 `core_law` vs 14 `secondary_physics` split is post hoc, and WTWK proof 36 p. 99 reads: "
            '"Inward first is the rare kind: a word for a state of a person that was later handed to physics." '
            "(making all 45 `not_physics_term` words structurally ineligible, 0/45 by definition). Therefore "
            "EVERY Fisher enrichment ratio, odds ratio, and binomial bound below is strictly descriptive "
            "(`DESCRIPTIVE_ONLY_POST_HOC_SPLIT_NOT_INFERENTIAL`) and MUST NOT be reported as a confirmatory test."
        ),
        "ledger_total_words": 80,
        "eligible_physics_words_total": len(core_law) + len(sec_phys),
        "structurally_ineligible_not_physics_term_count": len(non_phys),
        "full_80_kind_distribution": dict(sorted(kind_counts.items())),
        "strata_sizes": {
            "core_law": len(core_law),
            "secondary_physics": len(sec_phys),
            "not_physics_term_ineligible": len(non_phys),
        },
        "inward_first_core_law_words": inward_core,
        "inward_first_secondary_physics_words": inward_sec,
        "outward_first_core_law_words": outward_core,
        "outward_first_secondary_physics_words": outward_sec,
        "either_side_physics_words": either_side_phys,
        "household_physics_words": household_phys,
        "descriptive_physics_stratum_ratios": {
            "inferential_status": CORE_LAW_FISHER_STATUS,
            "descriptive_fisher_directional_physics_core_vs_secondary": {
                "inferential_status": CORE_LAW_FISHER_STATUS,
                "contingency": (
                    f"{len(inward_core)} inward / {len(outward_core)} outward in core_law vs "
                    f"{len(inward_sec)} inward / {len(outward_sec)} outward in secondary_physics"
                ),
                "exact_fraction": f"{p_fisher_dir_phys.numerator}/{p_fisher_dir_phys.denominator}",
                "descriptive_hypergeometric_ratio_float": float(p_fisher_dir_phys),
                **or_dir_phys,
            },
            "descriptive_fisher_all_35_physics_words_core_vs_secondary": {
                "inferential_status": CORE_LAW_FISHER_STATUS,
                "contingency": "5/21 in core_law vs 0/14 in secondary_physics (non-inward kinds scored 0)",
                "exact_fraction": f"{p_fisher_all35_phys.numerator}/{p_fisher_all35_phys.denominator}",
                "descriptive_hypergeometric_ratio_float": float(p_fisher_all35_phys),
                "exceeds_0_05_threshold": float(p_fisher_all35_phys) > 0.05,
                **or_all35_phys,
            },
            "descriptive_binomial_reference_tails": {
                "inferential_status": CORE_LAW_FISHER_STATUS,
                "denominators": binomial_reference_summaries,
            },
            "descriptive_sovereign_mirror_book_only_holdout": {
                "inferential_status": CORE_LAW_FISHER_STATUS,
                "description": (
                    "Descriptive tally holding out `work` and `power` (introduced in Oct 22 "
                    "tests/tsr_formal.py EXTENSION and Oct 2026 author rulings rather than main chapters of "
                    "The Sovereign Mirror v57), leaving `energy`, `force`, `inertia` in core_law."
                ),
                "holdout_directional_3_of_4_vs_0_of_8": {
                    "exact_fraction": f"{p_sm_book_holdout_dir.numerator}/{p_sm_book_holdout_dir.denominator}",
                    "descriptive_ratio_float": float(p_sm_book_holdout_dir),
                },
                "holdout_all_physics_3_of_19_vs_0_of_14": {
                    "exact_fraction": f"{p_sm_book_holdout_all33.numerator}/{p_sm_book_holdout_all33.denominator}",
                    "descriptive_ratio_float": float(p_sm_book_holdout_all33),
                },
                "reclassified_to_secondary_directional_3_of_4_vs_2_of_10": {
                    "exact_fraction": f"{p_sm_book_reclass_dir.numerator}/{p_sm_book_reclass_dir.denominator}",
                    "descriptive_ratio_float": float(p_sm_book_reclass_dir),
                },
            },
        },
        "core_law_pre_etymology_citations": core_law_citations,
        "descriptive_80_word_ledger_concentration_summary": {
            "inferential_status": CORE_LAW_FISHER_STATUS,
            "structural_ineligibility_reason": (
                "45 of the 59 non-core_law words are `not_physics_term` and cannot be "
                "handed to physics (`inward first`, WTWK proof 36 p. 99) by definition; do NOT cite this ratio "
                "as an inferential hypothesis test."
            ),
            "ledger_tally": "5/21 in core_law vs 0/14 in secondary_physics and 0/45 in not_physics_term",
            "descriptive_hypergeometric_ratio_fraction": (
                f"{p_descriptive_all80.numerator}/{p_descriptive_all80.denominator}"
            ),
            "descriptive_hypergeometric_ratio_float": float(p_descriptive_all80),
        },
    }


def _compact_summary_row(al: dict[str, Any]) -> dict[str, Any]:
    return {
        "tsr_edges": al["tsr_edge_count"],
        "etymology_edges": al["etymology_edge_count"],
        "n_orth_unrelated_pairs": al["n_orth_unrelated_pairs"],
        "observed_overlap": al["observed_overlap_count"],
        "overlapping_pairs": al["overlapping_pairs"],
        "orth_unrelated_hypergeometric_mean": round(
            al["exact_orth_unrelated_hypergeometric_moments"]["mean_float"], 4
        ),
        "exact_hypergeometric_p_fraction": al["exact_hypergeometric_p_fraction"],
        "exact_hypergeometric_p_float": al["exact_hypergeometric_p_float"],
        "pos_polysemy_stratified_mean_orth_unrelated": round(
            al["exact_pos_and_polysemy_stratified_mean"]["orth_unrelated_conditioned_float"], 4
        ),
        "stratified_perm_100k_p_upper_bound": al["stratified_permutation_100k_crosscheck"][
            "empirical_p_upper_bound"
        ],
    }


def _build_primary_test_block(primary_alignment: dict[str, Any]) -> dict[str, Any]:
    """
    Build the single pre-declared primary confirmatory test block (`g_tsr_oct22_cdba80d` vs
    `pie_roots_strict` over `N_orth_unrelated = 3152`). Keeps alternative null controls and QAP
    runs inside `exploratory_sensitivity_uncorrected` so `"primary_test"` carries strictly
    ONE p-value (`p ≈ 0.2878`, null result).
    """
    p_val = primary_alignment["exact_hypergeometric_p_float"]
    assert primary_alignment["tsr_edge_count"] == 66
    assert primary_alignment["etymology_edge_count"] == 16
    assert primary_alignment["n_orth_unrelated_pairs"] == 3152
    assert primary_alignment["observed_overlap_count"] == 1
    assert primary_alignment["overlapping_pairs"] == [["distance", "resist"]]
    assert 0.2877 < p_val < 0.2879, f"Unexpected primary p-value: {p_val}"

    return {
        "test_id": "PRIMARY_PRE_DECLARED_OCT22_CDBA80D_VS_STRICT_PIE",
        "pre_declared_hypothesis": (
            "Single confirmatory edge-overlap test comparing the Oct 22 commit `cdba80d` TSR graph "
            "(`g_tsr_oct22_cdba80d`, 66 pairs from `tests/tsr_formal.py`) against strict laryngeal "
            "PIE cognates (`pie_roots_strict`, 16 pairs) within the `N_orth_unrelated = 3,152` "
            "orthographically unrelated word-pair universe."
        ),
        "primary_tsr_graph": "g_tsr_oct22_cdba80d",
        "primary_tsr_provenance": f"Git commit cdba80d (2026-10-22), {OCT22_TSR_FORMAL_RELPATH} (SHA-256 verified)",
        "primary_tsr_sha256": OCT22_TSR_FORMAL_SHA256,
        "primary_etymology_graph": "pie_roots_strict",
        "orthographic_filter": "strict_latinate_mentum_ment_4char",
        "total_words": primary_alignment["total_words"],
        "total_unfiltered_word_pairs": primary_alignment["total_unfiltered_word_pairs"],
        "N_orth_unrelated": primary_alignment["n_orth_unrelated_pairs"],
        "tsr_edge_count": primary_alignment["tsr_edge_count"],
        "etymology_edge_count": primary_alignment["etymology_edge_count"],
        "observed_overlap_count": primary_alignment["observed_overlap_count"],
        "overlapping_pairs": primary_alignment["overlapping_pairs"],
        "overlapping_pair_classifications": primary_alignment["overlapping_pair_classifications"],
        "non_overlapping_etymology_pairs": primary_alignment["non_overlapping_etymology_pairs"],
        "exact_orth_unrelated_hypergeometric_moments": primary_alignment[
            "exact_orth_unrelated_hypergeometric_moments"
        ],
        "z_score_vs_orth_unrelated_hypergeometric": primary_alignment[
            "z_score_vs_orth_unrelated_hypergeometric"
        ],
        "exact_hypergeometric_p_fraction": primary_alignment["exact_hypergeometric_p_fraction"],
        "exact_hypergeometric_p_float": p_val,
        "statistically_significant_at_0_05": p_val < 0.05,
        "verdict": "NOT_STATISTICALLY_SIGNIFICANT_NULL_RESULT",
        "candor_note": (
            "The single pre-declared primary test (`g_tsr_oct22_cdba80d`, 66 pairs from Oct 22 "
            "`tests/tsr_formal.py`, vs `pie_roots_strict`, 16 pairs over N_orth_unrelated = 3152) "
            "yields 1 overlapping pair (`distance` <-> `resist`), exact hypergeometric upper-tail "
            "p = 0.2878 (> 0.05). Under the strictest pre-committed graph and strict PIE standard, "
            "there is no statistically significant cognate enrichment."
        ),
    }


def run_self_tests(
    words: list[dict[str, Any]],
    word_by_name: dict[str, dict[str, Any]],
    oct22_mod: Any,
    orth_unrelated_strict: set[tuple[str, str]],
    excluded_strict: list[tuple[str, str]],
    orth_unrelated_legacy: set[tuple[str, str]],
    g_oct22_pure_strict: set[tuple[str, str]],
    g_oct22_cdba_strict: set[tuple[str, str]],
    g_nov13_pure_strict: set[tuple[str, str]],
    g_nov13_frozen_strict: set[tuple[str, str]],
    etym_strict_filter: dict[str, set[tuple[str, str]]],
    all_strict_alignments: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """
    Internal deterministic self-assertion suite verifying ledger integrity, SHA-256 verification,
    stem-leak guards, Oct 22 primary graph counts, Nov 13 secondary graph counts, and QAP moments.
    """
    smap = build_surface_to_ledger_map(words)

    # 1. Surface-to-ledger stem leak assertions
    assert extract_ledger_words(
        "Subjective Reality and Objective Reality; vibrational and subjective realities; make real",
        smap,
    ) == {"subject", "object", "vibration"}, "Leak failure: 'real'/'reality'/'realities' leaked!"
    assert "realize" not in extract_ledger_words("real reality realities", smap)
    assert extract_ledger_words(
        "present moment; Movement times Appreciation; Rows 11 and 12 become forceable; Two senses: limitless",
        smap,
    ) == {"present", "movement", "appreciate"}, "Leak failure: false-friend token leaked!"

    # Audit every token across Oct 22 `tests/tsr_formal.py` AND secondary Nov 13 files
    source_texts: list[str] = []
    for phys, non, _r in oct22_mod.MIRROR:
        source_texts.extend([phys, non])
    for l_str, r_str in oct22_mod.DIAGONAL:
        source_texts.extend([l_str, r_str])
    source_texts.extend(["gravitational pull", "Attraction"])
    for k, (_op, rhs) in (
        list(oct22_mod.PHYS.items())
        + list(oct22_mod.NONPHYS_STATED.items())
        + list(oct22_mod.EXTENSION.items())
    ):
        source_texts.extend([k, " ".join(rhs)])
    for r in oct22_mod.ROWS:
        source_texts.extend([r[0], r[5]])

    for phys, non, _r in NOV13_MIRROR:
        source_texts.extend([phys, non])
    for l_str, r_str in NOV13_DIAGONAL:
        source_texts.extend([l_str, r_str])
    for k, v in NOV13_EXTENDED_PARTNERS.items():
        source_texts.extend([k, v])
    for k, v in NOV13_GLOSSARY_SENSES.items():
        source_texts.extend([k, v])
    for k, v in NOV13_AUTHOR_RULING_SOURCES.items():
        source_texts.extend([k, v])
    for k, (_op, rhs) in (
        list(NOV13_PHYS.items())
        + list(NOV13_NONPHYS_STATED.items())
        + list(NOV13_EXTENSION.items())
    ):
        source_texts.extend([k, " ".join(rhs)])
    for r in NOV13_ROWS:
        source_texts.extend([r[0], r[5]])

    all_audited_tokens = {
        tok for txt in source_texts for tok in re.findall(r"[a-zA-Z]+", txt.lower())
    }
    mapped_tokens = sorted(tok for tok in all_audited_tokens if tok in smap)
    for tok in mapped_tokens:
        assert tok not in FORBIDDEN_SURFACE_TOKENS
        assert smap[tok] in word_by_name

    # 2. Proof 36 `light` update & kind_counts check
    kc = Counter(w["kind"] for w in words)
    assert word_by_name["light"]["kind"] == "family"
    assert word_by_name["light"]["check"] == ["E"]
    assert kc["family"] == 36
    assert kc["not used"] == 1
    assert sum(kc.values()) == 80

    # 3. Orthographic filter & graph subset assertions
    assert shares_4char_substring("momentum", "movement", strict_latinate=True) is True
    assert shares_4char_substring("momentum", "movement", strict_latinate=False) is False
    assert ("momentum", "movement") not in orth_unrelated_strict
    assert ("momentum", "movement") in excluded_strict
    assert ("momentum", "movement") in orth_unrelated_legacy
    assert len(orth_unrelated_strict) == 3152
    assert len(orth_unrelated_legacy) == 3153
    assert len(g_oct22_pure_strict) == 54
    assert len(g_oct22_cdba_strict) == 66
    assert g_oct22_pure_strict <= g_oct22_cdba_strict
    assert len(g_nov13_pure_strict) == 67
    assert len(g_nov13_frozen_strict) == 182
    assert g_nov13_pure_strict <= g_nov13_frozen_strict

    # 4. Dual PIE root standards & calque vs classical_sense_overlap labels
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

    # 5. Verify N_orth_unrelated=3152 denominator & QAP / stratified permutation consistency
    for al_key, al_val in all_strict_alignments.items():
        assert al_val["n_orth_unrelated_pairs"] == 3152, (
            f"{al_key} did not use N_orth_unrelated=3152!"
        )
        assert al_val["hypergeometric_total_pop_used"] == 3152
        emp_mu = al_val["stratified_permutation_100k_crosscheck"]["empirical_mean"]
        exact_mu = al_val["exact_pos_and_polysemy_stratified_mean"]["float"]
        assert abs(emp_mu - exact_mu) < 0.02, (
            f"Stratified permutation mean mismatch on {al_key}: {emp_mu} vs {exact_mu}"
        )
        assert (
            al_val["exact_pos_and_polysemy_stratified_mean"]["orth_unrelated_conditioned_float"]
            + 1e-12
            >= exact_mu
        )

    # Verify batched permutation runner matches standalone bit-for-bit on 500 trials
    sample_edges_etym = etym_strict_filter["strict_pie"]
    standalone_500 = run_stratified_permutation_crosscheck(
        words,
        g_oct22_cdba_strict,
        sample_edges_etym,
        obs_overlap=len(g_oct22_cdba_strict & sample_edges_etym),
        stratum_fn=lambda w: (w["pos"], w["polysemy_tier"]),
        n_trials=500,
        seed=20191007,
    )
    batched_500 = run_batched_stratified_permutation_crosscheck(
        words,
        [("check", g_oct22_cdba_strict, sample_edges_etym, len(g_oct22_cdba_strict & sample_edges_etym))],
        stratum_fn=lambda w: (w["pos"], w["polysemy_tier"]),
        n_trials=500,
        seed=20191007,
    )["check"]
    assert standalone_500 == batched_500

    # 6. Verify all 21 core_law words carry pre_etymology_citation & non_phys has 0 inward_first
    core_words = [w for w in words if w["physics_stratum"] == "core_law"]
    assert len(core_words) == 21
    for cw in core_words:
        assert cw.get("pre_etymology_citation") and len(cw["pre_etymology_citation"]) > 20
    assert [
        w["word"]
        for w in words
        if w["physics_stratum"] == "not_physics_term" and w["kind"] == "inward first"
    ] == []

    return {
        "all_passed": True,
        "oct22_tsr_formal_sha256_verified": True,
        "ledger_kind_counts_verified": dict(sorted(kc.items())),
        "audited_unique_source_tokens": len(all_audited_tokens),
        "audited_mapped_tokens_count": len(mapped_tokens),
        "forbidden_tokens_verified_unmapped": sorted(FORBIDDEN_SURFACE_TOKENS),
        "strict_n_orth_unrelated_pairs": len(orth_unrelated_strict),
        "legacy_n_orth_unrelated_pairs": len(orth_unrelated_legacy),
        "oct22_pure_table_edge_count": len(g_oct22_pure_strict),
        "oct22_cdba80d_edge_count": len(g_oct22_cdba_strict),
        "nov13_pure_table_edge_count": len(g_nov13_pure_strict),
        "nov13_frozen_edge_count": len(g_nov13_frozen_strict),
        "excluded_orth_related_pairs_strict": [list(e) for e in excluded_strict],
        "pokorny_minus_strict_pie_pairs": [["converge", "vortex"]],
        "core_law_pre_etymology_citations_verified": len(core_words),
        "subset_invariants_verified": True,
    }


def run_combinatorial_proofs() -> dict[str, Any]:
    words = load_ledger()
    word_by_name = {w["word"]: w for w in words}
    oct22_mod = load_oct22_tsr_formal_module()

    # Strict (-mentum/-ment, primary: N_orth_unrelated=3152) and legacy (4-char: N_orth_unrelated=3153) universes
    orth_strict, excluded_strict = compute_orth_unrelated_pair_universe(words, strict_latinate=True)
    orth_legacy, excluded_legacy = compute_orth_unrelated_pair_universe(words, strict_latinate=False)

    etym_strict = build_hidden_etymology_graphs(words, strict_latinate=True)
    etym_legacy = build_hidden_etymology_graphs(words, strict_latinate=False)

    # Primary Oct 22 commit cdba80d TSR graphs (tests/tsr_formal.py)
    g_oct22_cdba_strict = build_oct22_cdba80d_graph(words, oct22_mod, strict_latinate=True)
    g_oct22_pure_strict = build_oct22_pure_table_graph(words, oct22_mod, strict_latinate=True)
    g_oct22_cdba_legacy = build_oct22_cdba80d_graph(words, oct22_mod, strict_latinate=False)
    g_oct22_pure_legacy = build_oct22_pure_table_graph(words, oct22_mod, strict_latinate=False)

    # Secondary Nov 13 TSR graphs (author-attested, first committed Nov 13: vocab/mirror.py + rule/tsr_formal_port.py)
    g_nov13_pure_strict = build_nov13_pure_table_graph(words, strict_latinate=True)
    g_nov13_frozen_strict = build_nov13_frozen_mirror_graph(words, strict_latinate=True)
    g_nov13_pure_legacy = build_nov13_pure_table_graph(words, strict_latinate=False)
    g_nov13_frozen_legacy = build_nov13_frozen_mirror_graph(words, strict_latinate=False)

    # Post-hoc prose-augmented concordance (quarantined in exploratory)
    g_canon_strict = build_canonical_tsr_graph(words, strict_latinate=True)

    # Batch all 100,000-trial (pos, polysemy_tier)-stratified permutation checks in one pass
    etym_grid_keys = (
        ("strict_pie", "strict_pie"),
        ("pokorny_pie", "pokorny_pie"),
        ("strict_pie_plus_translation_calque", "strict_pie_calque_only"),
        ("diachronic_strict_pie", "diachronic_strict_pie"),
        ("diachronic_pokorny_pie", "diachronic_pokorny_pie"),
    )
    perm_tasks: list[tuple[str, set[tuple[str, str]], set[tuple[str, str]], int]] = []
    graph_specs = [
        ("oct22_cdba_strict", g_oct22_cdba_strict, etym_strict),
        ("oct22_pure_strict", g_oct22_pure_strict, etym_strict),
        ("nov13_pure_strict", g_nov13_pure_strict, etym_strict),
        ("nov13_frozen_strict", g_nov13_frozen_strict, etym_strict),
        ("oct22_cdba_legacy", g_oct22_cdba_legacy, etym_legacy),
        ("oct22_pure_legacy", g_oct22_pure_legacy, etym_legacy),
        ("nov13_pure_legacy", g_nov13_pure_legacy, etym_legacy),
        ("nov13_frozen_legacy", g_nov13_frozen_legacy, etym_legacy),
    ]
    for g_prefix, g_edges, e_dict in graph_specs:
        for e_key, t_suffix in etym_grid_keys:
            if "legacy" in g_prefix and e_key == "strict_pie_plus_translation_calque":
                continue
            eg = e_dict[e_key]
            perm_tasks.append((f"{g_prefix}__{t_suffix}", g_edges, eg, len(g_edges & eg)))

    perm_tasks.extend(
        [
            ("oct22_cdba_strict__calque_only", g_oct22_cdba_strict, etym_strict["coined_translation_calque_only"], len(g_oct22_cdba_strict & etym_strict["coined_translation_calque_only"])),
            ("oct22_cdba_strict__sense_overlap_only", g_oct22_cdba_strict, etym_strict["classical_sense_overlap_only"], len(g_oct22_cdba_strict & etym_strict["classical_sense_overlap_only"])),
            ("desc__canon__strict_pie", g_canon_strict, etym_strict["strict_pie"], len(g_canon_strict & etym_strict["strict_pie"])),
            ("desc__canon__diachronic_pokorny_pie", g_canon_strict, etym_strict["diachronic_pokorny_pie"], len(g_canon_strict & etym_strict["diachronic_pokorny_pie"])),
        ]
    )

    perm_results = run_batched_stratified_permutation_crosscheck(
        words=words,
        tasks=perm_tasks,
        stratum_fn=lambda w: (w["pos"], w["polysemy_tier"]),
        n_trials=100_000,
        seed=20191007,
    )

    def eval_strict(
        label: str, status: str, g_tsr: set[tuple[str, str]], g_etym: set[tuple[str, str]], pkey: str
    ) -> dict[str, Any]:
        return evaluate_graph_alignment(
            label, status, words, word_by_name, orth_strict, g_tsr, g_etym, perm_results[pkey]
        )

    def eval_legacy(
        label: str, status: str, g_tsr: set[tuple[str, str]], g_etym: set[tuple[str, str]], pkey: str
    ) -> dict[str, Any]:
        return evaluate_graph_alignment(
            label, status, words, word_by_name, orth_legacy, g_tsr, g_etym, perm_results[pkey]
        )

    # 1. Pre-declared primary alignment (single confirmatory test)
    oct22_cdba_vs_strict_pie_full = eval_strict(
        "PRIMARY_Oct22_cdba80d_vs_Strict_PIE",
        "PRIMARY_PRE_DECLARED_OCT22_CDBA80D",
        g_oct22_cdba_strict,
        etym_strict["strict_pie"],
        "oct22_cdba_strict__strict_pie",
    )
    primary_test_block = _build_primary_test_block(oct22_cdba_vs_strict_pie_full)

    # 2. Exploratory Oct 22 alignments (other etymology specs + pure_table without ROWS + null controls)
    oct22_cdba_exploratory = {
        "pokorny_pie": eval_strict(
            "Exploratory_Oct22_cdba80d_vs_Pokorny_PIE",
            "EXPLORATORY_SENSITIVITY_UNCORRECTED_OCT22_CDBA80D",
            g_oct22_cdba_strict,
            etym_strict["pokorny_pie"],
            "oct22_cdba_strict__pokorny_pie",
        ),
        "coined_translation_calque_only": eval_strict(
            "Exploratory_Oct22_cdba80d_vs_Coined_Calque_Only",
            "EXPLORATORY_SENSITIVITY_UNCORRECTED_OCT22_CDBA80D",
            g_oct22_cdba_strict,
            etym_strict["coined_translation_calque_only"],
            "oct22_cdba_strict__calque_only",
        ),
        "classical_sense_overlap_only": eval_strict(
            "Exploratory_Oct22_cdba80d_vs_Classical_Sense_Overlap_Only",
            "EXPLORATORY_SENSITIVITY_UNCORRECTED_OCT22_CDBA80D",
            g_oct22_cdba_strict,
            etym_strict["classical_sense_overlap_only"],
            "oct22_cdba_strict__sense_overlap_only",
        ),
        "strict_pie_plus_translation_calque_only": eval_strict(
            "Exploratory_Oct22_cdba80d_vs_Strict_PIE_Plus_Calque",
            "EXPLORATORY_SENSITIVITY_UNCORRECTED_OCT22_CDBA80D",
            g_oct22_cdba_strict,
            etym_strict["strict_pie_plus_translation_calque"],
            "oct22_cdba_strict__strict_pie_calque_only",
        ),
        "diachronic_strict_pie": eval_strict(
            "Exploratory_Oct22_cdba80d_vs_Diachronic_Strict_PIE",
            "EXPLORATORY_SENSITIVITY_UNCORRECTED_OCT22_CDBA80D",
            g_oct22_cdba_strict,
            etym_strict["diachronic_strict_pie"],
            "oct22_cdba_strict__diachronic_strict_pie",
        ),
        "diachronic_pokorny_pie": eval_strict(
            "Exploratory_Oct22_cdba80d_vs_Diachronic_Pokorny_PIE",
            "EXPLORATORY_SENSITIVITY_UNCORRECTED_OCT22_CDBA80D",
            g_oct22_cdba_strict,
            etym_strict["diachronic_pokorny_pie"],
            "oct22_cdba_strict__diachronic_pokorny_pie",
        ),
    }

    oct22_pure_exploratory = {
        "strict_pie": eval_strict(
            "Exploratory_Oct22_PureTable_vs_Strict_PIE",
            "EXPLORATORY_SENSITIVITY_UNCORRECTED_OCT22_PURE_TABLE",
            g_oct22_pure_strict,
            etym_strict["strict_pie"],
            "oct22_pure_strict__strict_pie",
        ),
        "pokorny_pie": eval_strict(
            "Exploratory_Oct22_PureTable_vs_Pokorny_PIE",
            "EXPLORATORY_SENSITIVITY_UNCORRECTED_OCT22_PURE_TABLE",
            g_oct22_pure_strict,
            etym_strict["pokorny_pie"],
            "oct22_pure_strict__pokorny_pie",
        ),
        "strict_pie_plus_translation_calque_only": eval_strict(
            "Exploratory_Oct22_PureTable_vs_Strict_PIE_Plus_Calque",
            "EXPLORATORY_SENSITIVITY_UNCORRECTED_OCT22_PURE_TABLE",
            g_oct22_pure_strict,
            etym_strict["strict_pie_plus_translation_calque"],
            "oct22_pure_strict__strict_pie_calque_only",
        ),
        "diachronic_strict_pie": eval_strict(
            "Exploratory_Oct22_PureTable_vs_Diachronic_Strict_PIE",
            "EXPLORATORY_SENSITIVITY_UNCORRECTED_OCT22_PURE_TABLE",
            g_oct22_pure_strict,
            etym_strict["diachronic_strict_pie"],
            "oct22_pure_strict__diachronic_strict_pie",
        ),
        "diachronic_pokorny_pie": eval_strict(
            "Exploratory_Oct22_PureTable_vs_Diachronic_Pokorny_PIE",
            "EXPLORATORY_SENSITIVITY_UNCORRECTED_OCT22_PURE_TABLE",
            g_oct22_pure_strict,
            etym_strict["diachronic_pokorny_pie"],
            "oct22_pure_strict__diachronic_pokorny_pie",
        ),
    }

    # 3. Secondary Nov 13 graphs (author-attested, first committed Nov 13)
    nov13_status_pure = f"SECONDARY_UNCORRECTED ({NOV13_PROVENANCE_LABEL})"
    nov13_status_frozen = f"SECONDARY_UNCORRECTED ({NOV13_PROVENANCE_LABEL})"
    nov13_strict_alignments = {
        "pure_table_vs_strict_pie": eval_strict(
            "Secondary_Nov13_PureTable_vs_Strict_PIE",
            nov13_status_pure,
            g_nov13_pure_strict,
            etym_strict["strict_pie"],
            "nov13_pure_strict__strict_pie",
        ),
        "pure_table_vs_pokorny_pie": eval_strict(
            "Secondary_Nov13_PureTable_vs_Pokorny_PIE",
            nov13_status_pure,
            g_nov13_pure_strict,
            etym_strict["pokorny_pie"],
            "nov13_pure_strict__pokorny_pie",
        ),
        "pure_table_vs_strict_pie_plus_translation_calque_only": eval_strict(
            "Secondary_Nov13_PureTable_vs_Strict_PIE_Plus_Calque",
            nov13_status_pure,
            g_nov13_pure_strict,
            etym_strict["strict_pie_plus_translation_calque"],
            "nov13_pure_strict__strict_pie_calque_only",
        ),
        "pure_table_vs_diachronic_strict_pie": eval_strict(
            "Secondary_Nov13_PureTable_vs_Diachronic_Strict_PIE",
            nov13_status_pure,
            g_nov13_pure_strict,
            etym_strict["diachronic_strict_pie"],
            "nov13_pure_strict__diachronic_strict_pie",
        ),
        "pure_table_vs_diachronic_pokorny_pie": eval_strict(
            "Secondary_Nov13_PureTable_vs_Diachronic_Pokorny_PIE",
            nov13_status_pure,
            g_nov13_pure_strict,
            etym_strict["diachronic_pokorny_pie"],
            "nov13_pure_strict__diachronic_pokorny_pie",
        ),
        "frozen_code_vs_strict_pie": eval_strict(
            "Secondary_Nov13_Frozen_vs_Strict_PIE",
            nov13_status_frozen,
            g_nov13_frozen_strict,
            etym_strict["strict_pie"],
            "nov13_frozen_strict__strict_pie",
        ),
        "frozen_code_vs_pokorny_pie": eval_strict(
            "Secondary_Nov13_Frozen_vs_Pokorny_PIE",
            nov13_status_frozen,
            g_nov13_frozen_strict,
            etym_strict["pokorny_pie"],
            "nov13_frozen_strict__pokorny_pie",
        ),
        "frozen_code_vs_strict_pie_plus_translation_calque_only": eval_strict(
            "Secondary_Nov13_Frozen_vs_Strict_PIE_Plus_Calque",
            nov13_status_frozen,
            g_nov13_frozen_strict,
            etym_strict["strict_pie_plus_translation_calque"],
            "nov13_frozen_strict__strict_pie_calque_only",
        ),
        "frozen_code_vs_diachronic_strict_pie": eval_strict(
            "Secondary_Nov13_Frozen_vs_Diachronic_Strict_PIE",
            nov13_status_frozen,
            g_nov13_frozen_strict,
            etym_strict["diachronic_strict_pie"],
            "nov13_frozen_strict__diachronic_strict_pie",
        ),
        "frozen_code_vs_diachronic_pokorny_pie": eval_strict(
            "Secondary_Nov13_Frozen_vs_Diachronic_Pokorny_PIE",
            nov13_status_frozen,
            g_nov13_frozen_strict,
            etym_strict["diachronic_pokorny_pie"],
            "nov13_frozen_strict__diachronic_pokorny_pie",
        ),
    }

    # 4. Legacy 4-char morphological filter sensitivity (N_orth_unrelated = 3153)
    legacy_oct22_alignments = {
        "oct22_cdba80d_vs_strict_pie": eval_legacy(
            "Legacy4Char_Oct22_cdba80d_vs_Strict_PIE",
            "SENSITIVITY_LEGACY_4CHAR_FILTER_INCLUDES_MOMENTUM_MOVEMENT",
            g_oct22_cdba_legacy,
            etym_legacy["strict_pie"],
            "oct22_cdba_legacy__strict_pie",
        ),
        "oct22_cdba80d_vs_pokorny_pie": eval_legacy(
            "Legacy4Char_Oct22_cdba80d_vs_Pokorny_PIE",
            "SENSITIVITY_LEGACY_4CHAR_FILTER_INCLUDES_MOMENTUM_MOVEMENT",
            g_oct22_cdba_legacy,
            etym_legacy["pokorny_pie"],
            "oct22_cdba_legacy__pokorny_pie",
        ),
        "oct22_cdba80d_vs_diachronic_strict_pie": eval_legacy(
            "Legacy4Char_Oct22_cdba80d_vs_Diachronic_Strict_PIE",
            "SENSITIVITY_LEGACY_4CHAR_FILTER_INCLUDES_MOMENTUM_MOVEMENT",
            g_oct22_cdba_legacy,
            etym_legacy["diachronic_strict_pie"],
            "oct22_cdba_legacy__diachronic_strict_pie",
        ),
        "oct22_cdba80d_vs_diachronic_pokorny_pie": eval_legacy(
            "Legacy4Char_Oct22_cdba80d_vs_Diachronic_Pokorny_PIE",
            "SENSITIVITY_LEGACY_4CHAR_FILTER_INCLUDES_MOMENTUM_MOVEMENT",
            g_oct22_cdba_legacy,
            etym_legacy["diachronic_pokorny_pie"],
            "oct22_cdba_legacy__diachronic_pokorny_pie",
        ),
        "oct22_pure_table_vs_strict_pie": eval_legacy(
            "Legacy4Char_Oct22_PureTable_vs_Strict_PIE",
            "SENSITIVITY_LEGACY_4CHAR_FILTER_INCLUDES_MOMENTUM_MOVEMENT",
            g_oct22_pure_legacy,
            etym_legacy["strict_pie"],
            "oct22_pure_legacy__strict_pie",
        ),
        "oct22_pure_table_vs_diachronic_pokorny_pie": eval_legacy(
            "Legacy4Char_Oct22_PureTable_vs_Diachronic_Pokorny_PIE",
            "SENSITIVITY_LEGACY_4CHAR_FILTER_INCLUDES_MOMENTUM_MOVEMENT",
            g_oct22_pure_legacy,
            etym_legacy["diachronic_pokorny_pie"],
            "oct22_pure_legacy__diachronic_pokorny_pie",
        ),
    }

    legacy_nov13_alignments = {
        "nov13_pure_table_vs_strict_pie": eval_legacy(
            "Legacy4Char_Nov13_PureTable_vs_Strict_PIE",
            f"SENSITIVITY_LEGACY_4CHAR ({NOV13_PROVENANCE_LABEL})",
            g_nov13_pure_legacy,
            etym_legacy["strict_pie"],
            "nov13_pure_legacy__strict_pie",
        ),
        "nov13_pure_table_vs_pokorny_pie": eval_legacy(
            "Legacy4Char_Nov13_PureTable_vs_Pokorny_PIE",
            f"SENSITIVITY_LEGACY_4CHAR ({NOV13_PROVENANCE_LABEL})",
            g_nov13_pure_legacy,
            etym_legacy["pokorny_pie"],
            "nov13_pure_legacy__pokorny_pie",
        ),
        "nov13_pure_table_vs_diachronic_strict_pie": eval_legacy(
            "Legacy4Char_Nov13_PureTable_vs_Diachronic_Strict_PIE",
            f"SENSITIVITY_LEGACY_4CHAR ({NOV13_PROVENANCE_LABEL})",
            g_nov13_pure_legacy,
            etym_legacy["diachronic_strict_pie"],
            "nov13_pure_legacy__diachronic_strict_pie",
        ),
        "nov13_pure_table_vs_diachronic_pokorny_pie": eval_legacy(
            "Legacy4Char_Nov13_PureTable_vs_Diachronic_Pokorny_PIE",
            f"SENSITIVITY_LEGACY_4CHAR ({NOV13_PROVENANCE_LABEL})",
            g_nov13_pure_legacy,
            etym_legacy["diachronic_pokorny_pie"],
            "nov13_pure_legacy__diachronic_pokorny_pie",
        ),
        "nov13_frozen_code_vs_strict_pie": eval_legacy(
            "Legacy4Char_Nov13_Frozen_vs_Strict_PIE",
            f"SENSITIVITY_LEGACY_4CHAR ({NOV13_PROVENANCE_LABEL})",
            g_nov13_frozen_legacy,
            etym_legacy["strict_pie"],
            "nov13_frozen_legacy__strict_pie",
        ),
        "nov13_frozen_code_vs_pokorny_pie": eval_legacy(
            "Legacy4Char_Nov13_Frozen_vs_Pokorny_PIE",
            f"SENSITIVITY_LEGACY_4CHAR ({NOV13_PROVENANCE_LABEL})",
            g_nov13_frozen_legacy,
            etym_legacy["pokorny_pie"],
            "nov13_frozen_legacy__pokorny_pie",
        ),
        "nov13_frozen_code_vs_diachronic_strict_pie": eval_legacy(
            "Legacy4Char_Nov13_Frozen_vs_Diachronic_Strict_PIE",
            f"SENSITIVITY_LEGACY_4CHAR ({NOV13_PROVENANCE_LABEL})",
            g_nov13_frozen_legacy,
            etym_legacy["diachronic_strict_pie"],
            "nov13_frozen_legacy__diachronic_strict_pie",
        ),
        "nov13_frozen_code_vs_diachronic_pokorny_pie": eval_legacy(
            "Legacy4Char_Nov13_Frozen_vs_Diachronic_Pokorny_PIE",
            f"SENSITIVITY_LEGACY_4CHAR ({NOV13_PROVENANCE_LABEL})",
            g_nov13_frozen_legacy,
            etym_legacy["diachronic_pokorny_pie"],
            "nov13_frozen_legacy__diachronic_pokorny_pie",
        ),
    }

    # 5. Post-hoc prose-augmented concordance
    t1_desc_strict_pie = eval_strict(
        "Exploratory_Canonical_Book_Concordance_vs_Strict_PIE",
        "POST_HOC_DESCRIPTIVE_CONCORDANCE_ONLY",
        g_canon_strict,
        etym_strict["strict_pie"],
        "desc__canon__strict_pie",
    )
    t1_desc_diachronic_pokorny = eval_strict(
        "Exploratory_Canonical_Book_Concordance_vs_Diachronic_Pokorny_PIE",
        "POST_HOC_DESCRIPTIVE_CONCORDANCE_ONLY",
        g_canon_strict,
        etym_strict["diachronic_pokorny_pie"],
        "desc__canon__diachronic_pokorny_pie",
    )
    post_hoc_extra_hits_vs_oct22 = [
        list(e)
        for e in sorted(
            (g_canon_strict & etym_strict["diachronic_pokorny_pie"]) - g_oct22_cdba_strict
        )
    ]

    all_strict_alignments_for_self_test = {
        "primary_oct22_cdba80d_vs_strict_pie": oct22_cdba_vs_strict_pie_full,
        **{f"oct22_cdba__{k}": v for k, v in oct22_cdba_exploratory.items()},
        **{f"oct22_pure__{k}": v for k, v in oct22_pure_exploratory.items()},
        **nov13_strict_alignments,
        "canon_vs_strict_pie": t1_desc_strict_pie,
        "canon_vs_diachronic_pokorny_pie": t1_desc_diachronic_pokorny,
    }

    self_test_report = run_self_tests(
        words=words,
        word_by_name=word_by_name,
        oct22_mod=oct22_mod,
        orth_unrelated_strict=orth_strict,
        excluded_strict=excluded_strict,
        orth_unrelated_legacy=orth_legacy,
        g_oct22_pure_strict=g_oct22_pure_strict,
        g_oct22_cdba_strict=g_oct22_cdba_strict,
        g_nov13_pure_strict=g_nov13_pure_strict,
        g_nov13_frozen_strict=g_nov13_frozen_strict,
        etym_strict_filter=etym_strict,
        all_strict_alignments=all_strict_alignments_for_self_test,
    )

    center_crossing_loc = run_test_iii_2_energeia_actualitas_center_crossing(
        words=words,
        n_orth_unrelated_pairs_strict=len(orth_strict),
        g_oct22_pure_table=g_oct22_pure_strict,
        g_oct22_cdba80d=g_oct22_cdba_strict,
        g_nov13_pure_table=g_nov13_pure_strict,
        g_nov13_frozen=g_nov13_frozen_strict,
        g_tsr_canonical=g_canon_strict,
    )
    descriptive_core_law = run_descriptive_core_law_directionality_audit(words)

    return {
        "proof_id": "Part_III_Exact_Combinatorial_Etymology_Proofs",
        "source_dataset": str(LEDGER_PATH.relative_to(REPO_ROOT)),
        "source_edition": "WTWK proof 36 (pp. 99-104); Sovereign Mirror v57",
        "oct22_tsr_formal_sha256": OCT22_TSR_FORMAL_SHA256,
        "primary_test": primary_test_block,
        "self_tests": self_test_report,
        "descriptive_core_law_directionality_summary": descriptive_core_law,
        "exploratory_sensitivity_uncorrected": {
            "multiple_comparisons_warning": (
                "UNCORRECTED EXPLORATORY & SENSITIVITY ANALYSES: None of the ~60+ p-values, "
                "alternative null controls (uniform S_80 QAP / Cantelli bounds / 100k stratified "
                "permutations), secondary Nov 13 graphs ('author-attested, first committed Nov 13'), "
                "diachronic/Pokorny etymology specifications, legacy 4-char morphological filters, "
                "center-crossing calque probabilities, or post-hoc concordance counts below are "
                "corrected for multiple comparisons. Treat exclusively as sensitivity diagnostics, "
                "NEVER as confirmatory hypothesis tests."
            ),
            "primary_alignment_alternative_null_controls": {
                "note": (
                    "Alternative null models and permutation diagnostics specifically for the "
                    "primary pair (`g_tsr_oct22_cdba80d` vs `pie_roots_strict`); placed here "
                    "so `primary_test` reports strictly ONE pre-declared confirmatory p-value."
                ),
                "exact_uniform_S80_moments": oct22_cdba_vs_strict_pie_full["exact_uniform_S80_moments"],
                "z_score_vs_uniform_S80": oct22_cdba_vs_strict_pie_full["z_score_vs_uniform_S80"],
                "exact_cantelli_upper_bound_float": oct22_cdba_vs_strict_pie_full[
                    "exact_cantelli_upper_bound_float"
                ],
                "exact_polysemy_stratified_mean": oct22_cdba_vs_strict_pie_full[
                    "exact_polysemy_stratified_mean"
                ],
                "exact_pos_and_polysemy_stratified_mean": oct22_cdba_vs_strict_pie_full[
                    "exact_pos_and_polysemy_stratified_mean"
                ],
                "stratified_permutation_100k_crosscheck": oct22_cdba_vs_strict_pie_full[
                    "stratified_permutation_100k_crosscheck"
                ],
            },
            "oct22_cdba80d_sensitivity_strict_filter": {
                "graph_provenance": f"Git commit cdba80d (2026-10-22), {OCT22_TSR_FORMAL_RELPATH}",
                "g_tsr_oct22_cdba80d_66_pairs": {
                    "summary": {k: _compact_summary_row(v) for k, v in oct22_cdba_exploratory.items()},
                    "full_alignments": oct22_cdba_exploratory,
                },
                "g_tsr_oct22_pure_table_54_pairs": {
                    "summary": {k: _compact_summary_row(v) for k, v in oct22_pure_exploratory.items()},
                    "full_alignments": oct22_pure_exploratory,
                },
            },
            "nov13_author_attested_secondary_graphs": {
                "graph_provenance": (
                    f"{NOV13_PROVENANCE_LABEL}: vocab/mirror.py & rule/tsr_formal_port.py "
                    "(g_tsr_nov13_pure_table=67 pairs; g_tsr_nov13_frozen=182 pairs)"
                ),
                "summary_grid_strict_filter": {
                    "g_tsr_nov13_pure_table": {
                        "strict_pie": _compact_summary_row(
                            nov13_strict_alignments["pure_table_vs_strict_pie"]
                        ),
                        "pokorny_pie": _compact_summary_row(
                            nov13_strict_alignments["pure_table_vs_pokorny_pie"]
                        ),
                        "diachronic_strict_pie": _compact_summary_row(
                            nov13_strict_alignments["pure_table_vs_diachronic_strict_pie"]
                        ),
                        "diachronic_pokorny_pie": _compact_summary_row(
                            nov13_strict_alignments["pure_table_vs_diachronic_pokorny_pie"]
                        ),
                        "strict_pie_plus_coined_calque_only": _compact_summary_row(
                            nov13_strict_alignments[
                                "pure_table_vs_strict_pie_plus_translation_calque_only"
                            ]
                        ),
                    },
                    "g_tsr_nov13_frozen": {
                        "strict_pie": _compact_summary_row(
                            nov13_strict_alignments["frozen_code_vs_strict_pie"]
                        ),
                        "pokorny_pie": _compact_summary_row(
                            nov13_strict_alignments["frozen_code_vs_pokorny_pie"]
                        ),
                        "diachronic_strict_pie": _compact_summary_row(
                            nov13_strict_alignments["frozen_code_vs_diachronic_strict_pie"]
                        ),
                        "diachronic_pokorny_pie": _compact_summary_row(
                            nov13_strict_alignments["frozen_code_vs_diachronic_pokorny_pie"]
                        ),
                        "strict_pie_plus_coined_calque_only": _compact_summary_row(
                            nov13_strict_alignments[
                                "frozen_code_vs_strict_pie_plus_translation_calque_only"
                            ]
                        ),
                    },
                },
                "full_alignments": nov13_strict_alignments,
            },
            "legacy_4char_morphological_filter_sensitivity": {
                "audit_note": (
                    "Compares strict Latinate `-mentum`/`-ment` filter (excluding `momentum-movement`, "
                    "`N_orth_unrelated = 3152`) against legacy 4-char filter (including `momentum-movement`, "
                    "`N_orth_unrelated = 3153`; WTWK proof 36 pp. 41, 97 M-slot swap)."
                ),
                "n_orth_unrelated_pairs": len(orth_legacy),
                "excluded_pairs": [list(e) for e in excluded_legacy],
                "oct22_graphs_summary": {
                    k: _compact_summary_row(v) for k, v in legacy_oct22_alignments.items()
                },
                "oct22_graphs_full_alignments": legacy_oct22_alignments,
                "nov13_author_attested_graphs_summary": {
                    k: _compact_summary_row(v) for k, v in legacy_nov13_alignments.items()
                },
                "nov13_author_attested_graphs_full_alignments": legacy_nov13_alignments,
            },
            "prose_augmented_book_concordance_post_hoc": {
                "warning": (
                    "Compiled after reading What the Words Knew; includes thematic prose links not in "
                    "Oct 22 tests/tsr_formal.py or Nov 13 vocab/mirror.py and MUST NOT be cited as confirmatory."
                ),
                "post_hoc_extra_overlapping_pairs_not_in_oct22": post_hoc_extra_hits_vs_oct22,
                "canonical_vs_strict_pie": t1_desc_strict_pie,
                "canonical_vs_diachronic_pokorny_pie": t1_desc_diachronic_pokorny,
            },
            "center_crossing_calque_localization_uncorrected": center_crossing_loc,
        },
    }


if __name__ == "__main__":
    report = run_combinatorial_proofs()
    print(json.dumps(report, indent=2))
