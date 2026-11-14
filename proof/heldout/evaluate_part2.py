#!/usr/bin/env python3
"""
evaluate_part2.py — Post-unmasking Part 2 evaluation on 48 held-out OpenStax laws
and 17-row benchmarkRows17 calibration (never pooled).

Reads:
  - proof/heldout/appliers.csv
  - proof/heldout/labels.csv
  - proof/heldout/packets/session_extra_gemini_hydrogen.json
  - proof/heldout/sample_manifest.csv
  - proof/heldout/eligible_laws_pool.csv
  - proof/heldout/law_cards.csv
  - proof/lean/TSR/MirrorFunctor.lean

Writes (unless --verify-offline):
  - proof/heldout/part2_results.json
  - proof/heldout/part2_disagreements.csv

Python 3.12+ standard library only (zero external packages).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any, Sequence

PREREGISTRATION_COMMIT_SHA = "463ad9f93c8a276b1e0d9ee497198dfa2169d079"
AMENDMENT_1_COMMIT_SHA = "b66f48efb76e0f8d17d7db32848ad95f0a5c8633"
AMENDMENT_2_COMMIT_SHA = "530a254a51789a9fd68e1889f713b86d829c1146"
PRE_UNMASKING_COMMIT_SHA = "5f5c828d2d8dc32b53de887b9faa6ad214faf8e6"
ATTRIBUTION = "Access for free at https://openstax.org — Licensed under CC BY 4.0."

PRIMARY_PANEL_MODELS = {
    "s1": "gemini_carbon",
    "s2": "grok_4_7",
    "s3": "kimi_k3",
}
EXTRA_MODEL = "gemini_hydrogen"

SHARED_SESSION_DISCLOSURE = (
    "Under Pre-Results Amendment 2, Track (b) rulings/rationales and Track (c) codebook "
    "answers q1..q4 were generated inside the same standalone session per model family "
    "(s1: gemini_carbon, s2: grok_4_7, s3: kimi_k3; plus extra sensitivity session "
    "gemini_hydrogen) on the withheld-origin 65-card packet. Accordingly, comparisons "
    "between Track (b) rulings and Track (c) induced formulas (pred_ch16, pred_ch2) "
    "measure within-session codebook-to-prose consistency rather than session-independent "
    "cross-validation, whereas independence holds across the three distinct model families "
    "and against the pre-committed benchmarkRows17 book rulings."
)

CLAIM_TESTED = (
    "The one rule as printed in The Sovereign Mirror v57 (pp. 20 and 116) is enough "
    "to rule on a law it was not built from, in hands other than the author's."
)
NOT_TESTED = "Whether a ruling is true."

Z_95 = 1.959963984540054
CONSTRUCTION_BENCHMARK_IDS = frozenset({7, 14, 15, 16})
VALID_RULINGS_3 = ("Keep", "Invert", "the rule doesn't say")
VALID_RULINGS_4 = ("Keep", "Invert", "the rule doesn't say", "no_majority")
VALID_RULINGS_2 = ("Keep", "Invert")
VALID_BINARY = ("Yes", "No")

HELDOUT_DIR = Path(__file__).resolve().parent
REPO_ROOT = HELDOUT_DIR.parents[1]
PACKETS_DIR = HELDOUT_DIR / "packets"
APPLIERS_CSV_PATH = HELDOUT_DIR / "appliers.csv"
LABELS_CSV_PATH = HELDOUT_DIR / "labels.csv"
EXTRA_JSON_PATH = PACKETS_DIR / "session_extra_gemini_hydrogen.json"
SAMPLE_MANIFEST_PATH = HELDOUT_DIR / "sample_manifest.csv"
ELIGIBLE_POOL_PATH = HELDOUT_DIR / "eligible_laws_pool.csv"
LAW_CARDS_PATH = HELDOUT_DIR / "law_cards.csv"
LEAN_MIRROR_PATH = REPO_ROOT / "proof" / "lean" / "TSR" / "MirrorFunctor.lean"

RESULTS_JSON_PATH = HELDOUT_DIR / "part2_results.json"
DISAGREEMENTS_CSV_PATH = HELDOUT_DIR / "part2_disagreements.csv"

DISAGREEMENTS_FIELDS = [
    "card_id",
    "law_id",
    "volume",
    "chapter",
    "eq_number",
    "description",
    "b1_ruling",
    "b2_ruling",
    "b3_ruling",
    "b_maj_ruling",
    "pred_ch2",
    "pred_ch16",
    "note",
]

# Exact 22 included OpenStax chapters per PREREGISTRATION.md Section 1.3.
INCLUDED_CHAPTERS: list[tuple[int, int, str]] = [
    (1, 1, "Units and Measurement"),
    (1, 2, "Vectors"),
    (1, 3, "Motion Along a Straight Line"),
    (1, 4, "Motion in Two and Three Dimensions"),
    (1, 5, "Newton's Laws of Motion"),
    (1, 6, "Applications of Newton's Laws"),
    (1, 7, "Work and Kinetic Energy"),
    (1, 8, "Potential Energy and Conservation of Energy"),
    (1, 9, "Linear Momentum and Collisions"),
    (1, 10, "Fixed-Axis Rotation"),
    (1, 11, "Angular Momentum"),
    (1, 12, "Static Equilibrium and Elasticity"),
    (1, 13, "Gravitation"),
    (1, 14, "Fluid Mechanics"),
    (1, 15, "Oscillations"),
    (1, 16, "Waves"),
    (1, 17, "Sound"),
    (2, 1, "Temperature and Heat"),
    (2, 2, "The Kinetic Theory of Gases"),
    (2, 3, "The First Law of Thermodynamics"),
    (2, 4, "The Second Law of Thermodynamics"),
    (3, 5, "Relativity"),
]

# Hex-encoded hygiene patterns (excludes sample_manifest since evaluate_part2.py runs post-unmasking).
_FORBIDDEN_SUBSTRINGS_HEX = [
    "2f55736572732f6e6a66",
    "66696c653a2f2f2f",
    "7473725f3031",
    "2e706466",
    "726973657265",
    "763535",
    "70726f6f66203236",
    "4e5f626c696e64",
    "6e5f626c696e645f7061697273",
    "2e67656d696e69",
    "626c696e64",
]

# Concise factual domain clauses for held-out disagreements grounded in the law cards and rationales.
_CARD_FACTUAL_REASON: dict[str, str] = {
    "C002": "linear thermal expansion (Delta L = alpha L Delta T) scales with initial length L but is temperature-driven rather than inertial mass resistance",
    "C003": "standing-wave wavelength lambda_n = (2/n)L depends on boundary separation L (boundary condition vs defining cavity relation vs distance resistance)",
    "C004": "kinetic friction f_k = mu_k N expresses surface resistance without explicit mass m or spatial separation terms in the equation",
    "C008": "orbital period T = 2 pi sqrt(r^3 / (G M_E)) couples gravitational mass M_E and separation r across shared gravitational attraction",
    "C012": "ideal-gas equation of state pV = N k_B T involves molecule count N without inertial mass m or spatial separation",
    "C020": "volume thermal expansion Delta V = beta V Delta T scales with volume V and temperature without mass m or spatial separation",
    "C026": "near-Earth gravitational work W_grav = -m g (y_B - y_A) involves gravitational potential coupling across mass m and height displacement",
    "C031": "ideal-gas sound speed v = sqrt(gamma R T / M) inversely depends on gas molar mass M (inertial opposition vs defining gas relation)",
    "C033": "moment of inertia I = sum m_j r_j^2 defines rotational inertia from particle masses m_j and axis distances r_j",
    "C041": "adiabatic state relation p V^gamma = constant constrains a fixed molar gas quantity without explicit spatial separation",
    "C044": "Carnot refrigerator performance K_R = T_c / (T_h - T_c) relates reservoir temperatures without mass or spatial separation",
    "C048": "horizontal normal force N = mg equates contact support force with gravitational weight (equilibrium identity vs mass/boundary scaling)",
    "C049": "Doppler observed frequency f_o = f_s ((v +- v_o)/v) depends on relative medium speed without mass, separation, or identity",
    "C051": "Kepler's third law T^2 = (4 pi^2 / (G M)) a^3 couples central mass M and semi-major axis a through Newtonian gravitation",
    "C059": "equipartition heat capacity C_V = (d/2) R relates degrees of freedom and gas constant without mass or spatial separation",
    "C061": "universal gravitation F_12 = G (m_1 m_2 / r^2) r_hat couples masses m_1, m_2 across separation r via gravitational attraction",
    "C062": "Hooke's law F = -k x links restoring spring force to displacement x from equilibrium (elastic resistance vs conservative potential relation)",
    "C064": "vertical free fall y = y_0 + v_0 t - (1/2) g t^2 describes motion under constant gravity across vertical position y",
    "C065": "bulk modulus B = -Delta p (V_0 / Delta V) measures resistance to hydrostatic compression without explicit mass m or spatial separation",
}


def frac_dict(value: Fraction) -> dict[str, Any]:
    """Serialize an exact Fraction with integer numerator/denominator, string, and float."""
    return {
        "num": value.numerator,
        "den": value.denominator,
        "fraction": f"{value.numerator}/{value.denominator}",
        "float": float(value),
    }


def _decode_hex_list(hex_items: list[str]) -> list[str]:
    return [bytes.fromhex(item).decode("utf-8") for item in hex_items]


def _check_hygiene(named_texts: list[tuple[str, str]]) -> None:
    forbidden = _decode_hex_list(_FORBIDDEN_SUBSTRINGS_HEX)
    for label, text in named_texts:
        lowered = text.lower()
        for tok in forbidden:
            if tok.lower() in lowered:
                raise RuntimeError(f"Forbidden hygiene token {tok!r} found in {label}")


def _majority_ruling(rulings: Sequence[str]) -> str:
    counts = Counter(rulings)
    for ruling, count in counts.items():
        if count >= 2:
            return ruling
    return "no_majority"


def _majority_binary(answers: Sequence[str]) -> str:
    return "Yes" if sum(1 for ans in answers if ans == "Yes") >= 2 else "No"


def _compute_predictions(q1: bool, q2: bool, q3: bool, q4: bool) -> dict[str, str]:
    """Mirror proof/lean/TSR/MirrorFunctor.lean reading rules identically."""
    pred_ch2 = "Keep" if (q1 or (not q2 and not q3)) else "Invert"
    pred_ch16 = "Keep" if (q1 or q4 or (not q2 and not q3)) else "Invert"
    pred_naive_mass = "Invert" if q2 else "Keep"
    return {
        "pred_ch2": pred_ch2,
        "pred_ch16": pred_ch16,
        "pred_naive_mass": pred_naive_mass,
        "R_read_always_keep": "Keep",
        "R_read_always_invert": "Invert",
    }


def fleiss_kappa_exact(
    ratings_rows: Sequence[Sequence[str]],
    categories: Sequence[str],
) -> dict[str, Any]:
    """Compute exact rational Fleiss' kappa across N items and n raters per item."""
    if not ratings_rows:
        raise ValueError("fleiss_kappa_exact requires at least one item row")
    n_items = len(ratings_rows)
    n_raters = len(ratings_rows[0])
    if n_raters < 2:
        raise ValueError("fleiss_kappa_exact requires at least 2 raters per item")
    cat_list = list(categories)
    cat_set = set(cat_list)

    counts_matrix: list[list[int]] = []
    for idx, row in enumerate(ratings_rows):
        if len(row) != n_raters:
            raise ValueError(f"Inconsistent rater count at row {idx}: {len(row)} != {n_raters}")
        for val in row:
            if val not in cat_set:
                raise ValueError(f"Unexpected rating category {val!r} not in {cat_list}")
        counts_matrix.append([sum(1 for val in row if val == cat) for cat in cat_list])

    total_assignments = n_items * n_raters
    cat_totals = [sum(row[j] for row in counts_matrix) for j in range(len(cat_list))]
    p_j = [Fraction(tot, total_assignments) for tot in cat_totals]

    denom_pairs = n_raters * (n_raters - 1)
    p_i = [
        Fraction(sum(c * (c - 1) for c in row), denom_pairs)
        for row in counts_matrix
    ]
    p_bar = sum(p_i, Fraction(0)) / n_items
    p_e = sum((p * p for p in p_j), Fraction(0))
    one_minus_pe = Fraction(1, 1) - p_e

    unanimous_count = sum(1 for row in counts_matrix if n_raters in row)
    unanimous_rate = Fraction(unanimous_count, n_items)

    base = {
        "n_items": n_items,
        "n_raters": n_raters,
        "categories": cat_list,
        "category_counts": {cat: cat_totals[j] for j, cat in enumerate(cat_list)},
        "category_proportions": {cat: frac_dict(p_j[j]) for j, cat in enumerate(cat_list)},
        "unanimous_count": unanimous_count,
        "unanimous_rate": frac_dict(unanimous_rate),
        "P_bar": frac_dict(p_bar),
        "P_e": frac_dict(p_e),
    }
    if one_minus_pe == 0:
        return {
            **base,
            "kappa": None,
            "kappa_fraction": None,
            "kappa_float": None,
            "degenerate_single_category": True,
        }

    kappa = (p_bar - p_e) / one_minus_pe
    return {
        **base,
        "kappa": frac_dict(kappa),
        "kappa_fraction": f"{kappa.numerator}/{kappa.denominator}",
        "kappa_float": float(kappa),
        "degenerate_single_category": False,
    }


def confusion_matrix_dict(
    xs: Sequence[str],
    ys: Sequence[str],
    x_categories: Sequence[str],
    y_categories: Sequence[str],
) -> dict[str, dict[str, int]]:
    """Build nested confusion matrix counts[x_cat][y_cat]."""
    if len(xs) != len(ys):
        raise ValueError(f"Mismatched sequence lengths: {len(xs)} != {len(ys)}")
    x_set = set(x_categories)
    y_set = set(y_categories)
    matrix: dict[str, dict[str, int]] = {
        xc: {yc: 0 for yc in y_categories} for xc in x_categories
    }
    for x_val, y_val in zip(xs, ys):
        if x_val not in x_set:
            raise ValueError(f"Unexpected x category {x_val!r} not in {list(x_categories)}")
        if y_val not in y_set:
            raise ValueError(f"Unexpected y category {y_val!r} not in {list(y_categories)}")
        matrix[x_val][y_val] += 1
    return matrix


def cohen_kappa_exact(
    xs: Sequence[str],
    ys: Sequence[str],
    categories: Sequence[str],
) -> dict[str, Any]:
    """Compute exact rational Cohen's kappa over the given category set."""
    if not xs or len(xs) != len(ys):
        raise ValueError("cohen_kappa_exact requires non-empty equal-length sequences")
    n_items = len(xs)
    cat_list = list(categories)
    matrix = confusion_matrix_dict(xs, ys, cat_list, cat_list)

    agree = sum(matrix[c][c] for c in cat_list)
    p_o = Fraction(agree, n_items)
    row_totals = {c: sum(matrix[c][yc] for yc in cat_list) for c in cat_list}
    col_totals = {c: sum(matrix[xc][c] for xc in cat_list) for c in cat_list}
    p_e = Fraction(sum(row_totals[c] * col_totals[c] for c in cat_list), n_items * n_items)
    one_minus_pe = Fraction(1, 1) - p_e

    base = {
        "n_items": n_items,
        "categories": cat_list,
        "matches": agree,
        "p_o": frac_dict(p_o),
        "p_e": frac_dict(p_e),
    }
    if one_minus_pe == 0:
        return {
            **base,
            "kappa": None,
            "kappa_fraction": None,
            "kappa_float": None,
            "degenerate_single_category": True,
        }

    kappa = (p_o - p_e) / one_minus_pe
    return {
        **base,
        "kappa": frac_dict(kappa),
        "kappa_fraction": f"{kappa.numerator}/{kappa.denominator}",
        "kappa_float": float(kappa),
        "degenerate_single_category": False,
    }


def fisher_exact_one_sided_or_gt_1(tp: int, fp: int, fn: int, tn: int) -> Fraction:
    """Exact one-sided Fisher hypergeometric upper-tail p-value for OR > 1 on [[tp, fp], [fn, tn]]."""
    if min(tp, fp, fn, tn) < 0:
        raise ValueError(f"Negative cell count in 2x2 table: {(tp, fp, fn, tn)}")
    n1 = tp + fn
    n2 = fp + tn
    r1 = tp + fp
    r2 = fn + tn
    n_total = n1 + n2
    if n1 == 0 or n2 == 0 or r1 == 0 or r2 == 0:
        return Fraction(1, 1)

    denom = math.comb(n_total, r1)
    max_x = min(n1, r1)
    min_x = max(tp, r1 - n2)
    numer = sum(math.comb(n1, x) * math.comb(n2, r1 - x) for x in range(min_x, max_x + 1))
    return Fraction(numer, denom)


def _wilson_score_bounds(k: int, n: int, z: float) -> tuple[float, float]:
    p_hat = k / n
    z2 = z * z
    rad = z * math.sqrt(max(0.0, z2 + 4.0 * k * (n - k) / n))
    denom = 2.0 * (n + z2)
    lower = (2.0 * k + z2 - rad) / denom
    upper = (2.0 * k + z2 + rad) / denom
    return lower, upper


def wilson_mover_ba_ci(
    k1: int,
    n1: int,
    k2: int,
    n2: int,
    z: float = Z_95,
) -> dict[str, Any]:
    """
    Closed-form 95% Wilson-MOVER (Newcombe Method 10 square-and-add) confidence interval
    for balanced accuracy BA = (TPR + TNR) / 2 per PREREGISTRATION.md L307-314.
    """
    if min(k1, n1, k2, n2) < 0 or k1 > n1 or k2 > n2:
        raise ValueError(f"Invalid counts for wilson_mover_ba_ci: {(k1, n1, k2, n2)}")
    total = n1 + n2
    cond_acc = frac_dict(Fraction(k1 + k2, total)) if total > 0 else None

    if n1 == 0 or n2 == 0:
        return {
            "n1": n1,
            "k1": k1,
            "n2": n2,
            "k2": k2,
            "z": z,
            "TPR": frac_dict(Fraction(k1, n1)) if n1 > 0 else None,
            "TNR": frac_dict(Fraction(k2, n2)) if n2 > 0 else None,
            "conditional_acc": cond_acc,
            "BA": None,
            "wilson_class1": None,
            "wilson_class2": None,
            "L_BA": None,
            "U_BA": None,
            "degenerate_class": True,
        }

    tpr = Fraction(k1, n1)
    tnr = Fraction(k2, n2)
    ba = (tpr + tnr) / 2
    p1 = float(tpr)
    p2 = float(tnr)
    l1, u1 = _wilson_score_bounds(k1, n1, z)
    l2, u2 = _wilson_score_bounds(k2, n2, z)

    l_ba = 0.5 * (p1 + p2 - math.sqrt((p1 - l1) ** 2 + (p2 - l2) ** 2))
    u_ba = 0.5 * (p1 + p2 + math.sqrt((u1 - p1) ** 2 + (u2 - p2) ** 2))

    return {
        "n1": n1,
        "k1": k1,
        "n2": n2,
        "k2": k2,
        "z": z,
        "TPR": frac_dict(tpr),
        "TNR": frac_dict(tnr),
        "conditional_acc": cond_acc,
        "BA": frac_dict(ba),
        "wilson_class1": [l1, u1],
        "wilson_class2": [l2, u2],
        "L_BA": l_ba,
        "U_BA": u_ba,
        "degenerate_class": False,
    }


def _parse_lean_row_tuple(body: str) -> dict[str, Any]:
    """Parse a Lean ⟨id, "label", .Reading, bool, lawAST⟩ tuple."""
    pattern = re.compile(
        r'^\s*⟨\s*(\d+)\s*,\s*"([^"]+)"\s*,\s*\.(Keep|Invert)\s*,\s*(true|false)\s*,\s*(.+?)\s*⟩\s*$'
    )
    match = pattern.match(body.strip())
    if not match:
        raise RuntimeError(f"Could not parse Lean BenchmarkRow tuple: {body!r}")
    row_id = int(match.group(1))
    label = match.group(2)
    book_ruling = match.group(3)
    has_mass = match.group(4) == "true"
    law_ast = " ".join(match.group(5).split())
    lean_q1 = law_ast == ".IdentityOrEquiv"
    lean_q2 = has_mass
    lean_q3 = law_ast == ".SpatialSeparationDependence"
    lean_q4 = law_ast == ".SharedCenterCurvature"
    preds = _compute_predictions(lean_q1, lean_q2, lean_q3, lean_q4)
    return {
        "id": row_id,
        "label": label,
        "bookRuling": book_ruling,
        "hasMass": has_mass,
        "lawAST": law_ast,
        "lean_q1": lean_q1,
        "lean_q2": lean_q2,
        "lean_q3": lean_q3,
        "lean_q4": lean_q4,
        "lean_R_read_v57_ch2": preds["pred_ch2"],
        "lean_R_read_v57_ch16": preds["pred_ch16"],
        "lean_R_read_naive_mass": preds["pred_naive_mass"],
        "lean_R_read_always_keep": preds["R_read_always_keep"],
        "lean_R_read_always_invert": preds["R_read_always_invert"],
    }


def load_and_verify_lean_benchmark(path: Path) -> list[dict[str, Any]]:
    """Parse row11GravityWarp, row12GravityLensing, row17Boyle, and benchmarkRows17 from Lean."""
    text = path.read_text(encoding="utf-8")

    named_rows: dict[str, dict[str, Any]] = {}
    for name in ("row11GravityWarp", "row12GravityLensing", "row17Boyle"):
        pat = re.compile(
            rf"def\s+{name}\s*:\s*BenchmarkRow\s*:=\s*(⟨[^\n⟩]+⟩)",
            re.MULTILINE,
        )
        m = pat.search(text)
        if not m:
            raise RuntimeError(f"Missing Lean definition {name} in {path}")
        named_rows[name] = _parse_lean_row_tuple(m.group(1))

    list_match = re.search(
        r"def\s+benchmarkRows17\s*:\s*List\s+BenchmarkRow\s*:=\s*\[(.*?)\n\]",
        text,
        re.DOTALL,
    )
    if not list_match:
        raise RuntimeError(f"Missing Lean benchmarkRows17 list in {path}")

    rows: list[dict[str, Any]] = []
    for raw_line in list_match.group(1).splitlines():
        line = raw_line.strip().rstrip(",").strip()
        if not line:
            continue
        if line in named_rows:
            rows.append(dict(named_rows[line]))
        else:
            rows.append(_parse_lean_row_tuple(line))

    if len(rows) != 17:
        raise RuntimeError(f"Expected 17 parsed Lean rows, got {len(rows)}")
    if [r["id"] for r in rows] != list(range(1, 18)):
        raise RuntimeError(f"Unexpected Lean benchmark row IDs: {[r['id'] for r in rows]}")

    ch2_misses = [r["id"] for r in rows if r["lean_R_read_v57_ch2"] != r["bookRuling"]]
    ch16_misses = [r["id"] for r in rows if r["lean_R_read_v57_ch16"] != r["bookRuling"]]
    keep_misses = [r["id"] for r in rows if r["lean_R_read_always_keep"] != r["bookRuling"]]
    invert_matches = [r["id"] for r in rows if r["lean_R_read_always_invert"] == r["bookRuling"]]

    assert len(rows) - len(ch2_misses) == 14 and ch2_misses == [11, 12, 17], (
        f"Lean R_read_v57_ch2 check failed: misses={ch2_misses}"
    )
    assert len(rows) - len(ch16_misses) == 16 and ch16_misses == [17], (
        f"Lean R_read_v57_ch16 check failed: misses={ch16_misses}"
    )
    assert len(rows) - len(keep_misses) == 14 and keep_misses == [2, 8, 9], (
        f"Lean R_read_always_keep check failed: misses={keep_misses}"
    )
    assert len(invert_matches) == 3 and invert_matches == [2, 8, 9], (
        f"Lean R_read_always_invert check failed: matches={invert_matches}"
    )
    return rows


def _load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_and_validate_inputs() -> dict[str, Any]:
    """Load all 7 required input files and verify internal integrity & SHA invariants."""
    lean_rows = load_and_verify_lean_benchmark(LEAN_MIRROR_PATH)
    lean_by_id = {r["id"]: r for r in lean_rows}

    cards_rows = _load_csv_rows(LAW_CARDS_PATH)
    manifest_rows = _load_csv_rows(SAMPLE_MANIFEST_PATH)
    pool_rows = _load_csv_rows(ELIGIBLE_POOL_PATH)
    appliers_rows = _load_csv_rows(APPLIERS_CSV_PATH)
    labels_rows = _load_csv_rows(LABELS_CSV_PATH)
    extra_rows = json.loads(EXTRA_JSON_PATH.read_text(encoding="utf-8"))

    expected_card_ids = [f"C{i:03d}" for i in range(1, 66)]
    for name, rows in (
        ("law_cards.csv", cards_rows),
        ("sample_manifest.csv", manifest_rows),
        ("appliers.csv", appliers_rows),
        ("labels.csv", labels_rows),
        ("session_extra_gemini_hydrogen.json", extra_rows),
    ):
        if [r["card_id"] for r in rows] != expected_card_ids:
            raise RuntimeError(f"{name}: unexpected card_id sequence")

    for r in cards_rows + manifest_rows + pool_rows:
        if r["preregistration_commit_sha"] != PREREGISTRATION_COMMIT_SHA:
            raise RuntimeError("preregistration_commit_sha mismatch in Stage 0/manifest/pool")

    pool_by_law_id = {r["law_id"]: r for r in pool_rows}
    if len(pool_by_law_id) != len(pool_rows):
        raise RuntimeError("Duplicate law_id in eligible_laws_pool.csv")

    chapter_title_map = {(v, c): title for v, c, title in INCLUDED_CHAPTERS}
    for r in pool_rows:
        key = (int(r["volume"]), int(r["chapter"]))
        if key not in chapter_title_map or r["chapter_title"] != chapter_title_map[key]:
            raise RuntimeError(f"Unexpected chapter in eligible_laws_pool.csv: {r}")

    cards_by_id = {r["card_id"]: r for r in cards_rows}
    manifest_by_id = {r["card_id"]: r for r in manifest_rows}
    appliers_by_id = {r["card_id"]: r for r in appliers_rows}
    labels_by_id = {r["card_id"]: r for r in labels_rows}
    extra_by_id = {r["card_id"]: r for r in extra_rows}

    heldout_ids: list[str] = []
    cal_ids: list[str] = []
    seen_benchmark_ids: set[int] = set()
    seen_law_ids: set[str] = set()

    for cid in expected_card_ids:
        m = manifest_by_id[cid]
        a = appliers_by_id[cid]
        l = labels_by_id[cid]
        e = extra_by_id[cid]

        if m["source_set"] == "heldout":
            assert m["draw_phase"] == "primary_48"
            law_id = m["law_id"]
            if law_id in seen_law_ids or law_id not in pool_by_law_id:
                raise RuntimeError(f"Invalid or duplicate held-out law_id {law_id!r}")
            seen_law_ids.add(law_id)
            p = pool_by_law_id[law_id]
            assert m["volume"] == p["volume"] and m["chapter"] == p["chapter"]
            heldout_ids.append(cid)
        elif m["source_set"] == "benchmark_17":
            assert m["draw_phase"] == "calibration_17"
            bid = int(m["benchmark_id"])
            if bid in seen_benchmark_ids or bid not in lean_by_id:
                raise RuntimeError(f"Invalid or duplicate benchmark_id {bid}")
            seen_benchmark_ids.add(bid)
            cal_ids.append(cid)
        else:
            raise RuntimeError(f"Unknown source_set {m['source_set']!r} on {cid}")

        # Validate appliers.csv consistency.
        assert (a["b1_model_family"], a["b2_model_family"], a["b3_model_family"]) == (
            "gemini_carbon",
            "grok_4_7",
            "kimi_k3",
        )
        assert a["preregistration_commit_sha"] == PREREGISTRATION_COMMIT_SHA
        assert a["amendment_1_commit_sha"] == AMENDMENT_1_COMMIT_SHA
        for col in ("b1_ruling", "b2_ruling", "b3_ruling"):
            assert a[col] in VALID_RULINGS_3
        assert a["b_maj_ruling"] == _majority_ruling(
            (a["b1_ruling"], a["b2_ruling"], a["b3_ruling"])
        )

        # Validate labels.csv consistency.
        assert (l["c1_model_family"], l["c2_model_family"], l["c3_model_family"]) == (
            "gemini_carbon",
            "grok_4_7",
            "kimi_k3",
        )
        assert l["preregistration_commit_sha"] == PREREGISTRATION_COMMIT_SHA
        assert l["amendment_1_commit_sha"] == AMENDMENT_1_COMMIT_SHA
        for q in ("q1", "q2", "q3", "q4"):
            votes = (l[f"c1_{q}"], l[f"c2_{q}"], l[f"c3_{q}"])
            for v in votes:
                assert v in VALID_BINARY
            assert l[f"{q}_maj"] == _majority_binary(votes)

        preds = _compute_predictions(
            l["q1_maj"] == "Yes",
            l["q2_maj"] == "Yes",
            l["q3_maj"] == "Yes",
            l["q4_maj"] == "Yes",
        )
        assert l["pred_ch2"] == preds["pred_ch2"]
        assert l["pred_ch16"] == preds["pred_ch16"]
        assert l["pred_naive_mass"] == preds["pred_naive_mass"]

        # Validate extra session JSON.
        assert set(e.keys()) == {"card_id", "q1", "q2", "q3", "q4", "ruling", "rationale"}
        for q in ("q1", "q2", "q3", "q4"):
            assert e[q] in VALID_BINARY
        assert e["ruling"] in VALID_RULINGS_3
        assert isinstance(e["rationale"], str) and e["rationale"].strip() != ""

    assert len(heldout_ids) == 48
    assert len(cal_ids) == 17
    assert seen_benchmark_ids == set(range(1, 18))
    assert set(heldout_ids).isdisjoint(set(cal_ids))

    return {
        "lean_rows": lean_rows,
        "lean_by_id": lean_by_id,
        "cards_by_id": cards_by_id,
        "manifest_by_id": manifest_by_id,
        "pool_rows": pool_rows,
        "pool_by_law_id": pool_by_law_id,
        "appliers_by_id": appliers_by_id,
        "labels_by_id": labels_by_id,
        "extra_by_id": extra_by_id,
        "heldout_ids": heldout_ids,
        "cal_ids": cal_ids,
    }


def _binary_agreement_block(
    xs: Sequence[str],
    ys: Sequence[str],
    x_cats: Sequence[str],
    y_cats: Sequence[str],
    kappa_cats: Sequence[str],
    row_ids: Sequence[Any] | None = None,
) -> dict[str, Any]:
    """Compute exact matches/n, confusion matrix, and Cohen's kappa for any paired series."""
    n = len(xs)
    matches = sum(1 for x, y in zip(xs, ys) if x == y)
    out: dict[str, Any] = {
        "n": n,
        "matches": matches,
        "agreement_rate": frac_dict(Fraction(matches, n)),
        "confusion_matrix": confusion_matrix_dict(xs, ys, x_cats, y_cats),
        "cohen_kappa": cohen_kappa_exact(xs, ys, kappa_cats),
    }
    if row_ids is not None:
        out["mismatch_ids"] = [rid for rid, x, y in zip(row_ids, xs, ys) if x != y]
    return out


def _evaluate_binary_classifier(
    pred_series: Sequence[str],
    actual_series: Sequence[str],
) -> dict[str, Any]:
    """Compute 2x2 table, Fisher upper-tail p, Wilson-MOVER BA CI, and Cohen's kappa."""
    tp = sum(1 for p, a in zip(pred_series, actual_series) if p == "Invert" and a == "Invert")
    fp = sum(1 for p, a in zip(pred_series, actual_series) if p == "Invert" and a == "Keep")
    fn = sum(1 for p, a in zip(pred_series, actual_series) if p == "Keep" and a == "Invert")
    tn = sum(1 for p, a in zip(pred_series, actual_series) if p == "Keep" and a == "Keep")
    fisher_p = fisher_exact_one_sided_or_gt_1(tp, fp, fn, tn)
    ci = wilson_mover_ba_ci(k1=tp, n1=tp + fn, k2=tn, n2=fp + tn)
    kappa = cohen_kappa_exact(pred_series, actual_series, VALID_RULINGS_2)
    return {
        "N": len(actual_series),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "confusion_matrix_2x2": {"rows_pred_cols_actual": [[tp, fp], [fn, tn]]},
        "fisher_p_one_sided": frac_dict(fisher_p),
        "cohen_kappa": kappa,
        **ci,
    }


def _evaluate_applier_vs_pred_l313(
    applier_series: Sequence[str],
    pred_series: Sequence[str],
) -> dict[str, Any]:
    """
    Evaluate individual applier b_j vs pred_ch16 per PREREGISTRATION.md L313:
    pred_ch16 == 'Invert' is n1, pred_ch16 == 'Keep' is n2, and 'the rule doesn't say'
    by b_j is counted in n1/n2 and NOT in k1/k2.
    """
    n1 = sum(1 for p in pred_series if p == "Invert")
    k1 = sum(1 for b, p in zip(applier_series, pred_series) if p == "Invert" and b == "Invert")
    n2 = sum(1 for p in pred_series if p == "Keep")
    k2 = sum(1 for b, p in zip(applier_series, pred_series) if p == "Keep" and b == "Keep")
    ci = wilson_mover_ba_ci(k1=k1, n1=n1, k2=k2, n2=n2)
    return {
        "confusion_matrix_3x2": confusion_matrix_dict(
            applier_series, pred_series, VALID_RULINGS_3, VALID_RULINGS_2
        ),
        **ci,
    }


def build_calibration_17_section(data: dict[str, Any]) -> dict[str, Any]:
    """Build Section 1 (calibration_17) strictly on the 17 benchmarkRows17 cards."""
    manifest = data["manifest_by_id"]
    appliers = data["appliers_by_id"]
    labels = data["labels_by_id"]
    extra = data["extra_by_id"]
    lean_by_id = data["lean_by_id"]

    cal_cards_sorted = sorted(
        data["cal_ids"],
        key=lambda cid: int(manifest[cid]["benchmark_id"]),
    )
    cal_items: list[dict[str, Any]] = []
    for cid in cal_cards_sorted:
        bid = int(manifest[cid]["benchmark_id"])
        lean_r = lean_by_id[bid]
        a = appliers[cid]
        l = labels[cid]
        e = extra[cid]
        provenance = "construction" if bid in CONSTRUCTION_BENCHMARK_IDS else "applied_later"
        cal_items.append(
            {
                "benchmark_id": bid,
                "card_id": cid,
                "label": lean_r["label"],
                "provenance": provenance,
                "book_ruling": lean_r["bookRuling"],
                "lean": lean_r,
                "applier": a,
                "label_row": l,
                "extra": e,
            }
        )

    assert len(cal_items) == 17
    assert sum(1 for x in cal_items if x["provenance"] == "construction") == 4
    assert sum(1 for x in cal_items if x["provenance"] == "applied_later") == 13

    # 1. Track (b) inter-session Fleiss' kappa across 17 rows.
    b_rows_17 = [
        (x["applier"]["b1_ruling"], x["applier"]["b2_ruling"], x["applier"]["b3_ruling"])
        for x in cal_items
    ]
    fleiss_b_3cat = fleiss_kappa_exact(b_rows_17, VALID_RULINGS_3)
    unanimously_def_rows = [
        row for row in b_rows_17 if all(r in VALID_RULINGS_2 for r in row)
    ]
    fleiss_b_2cat_unanimous = fleiss_kappa_exact(unanimously_def_rows, VALID_RULINGS_2)

    # 2. Agreement vs bookRuling overall (17), construction (4), applied_later (13).
    scopes = {
        "overall": cal_items,
        "construction": [x for x in cal_items if x["provenance"] == "construction"],
        "applied_later": [x for x in cal_items if x["provenance"] == "applied_later"],
    }

    def extract_rater(items: list[dict[str, Any]], key: str) -> list[str]:
        if key in ("b1", "b2", "b3"):
            return [x["applier"][f"{key}_ruling"] for x in items]
        if key == "b_maj_ruling":
            return [x["applier"]["b_maj_ruling"] for x in items]
        if key in ("pred_ch2", "pred_ch16", "pred_naive_mass"):
            return [x["label_row"][key] for x in items]
        if key == "R_read_always_keep":
            return ["Keep" for _ in items]
        if key == "R_read_always_invert":
            return ["Invert" for _ in items]
        if key in ("lean_R_read_v57_ch2", "lean_R_read_v57_ch16", "lean_R_read_naive_mass"):
            return [x["lean"][key] for x in items]
        raise ValueError(f"Unknown rater key {key}")

    rater_specs = [
        ("b1", VALID_RULINGS_3, VALID_RULINGS_3),
        ("b2", VALID_RULINGS_3, VALID_RULINGS_3),
        ("b3", VALID_RULINGS_3, VALID_RULINGS_3),
        ("b_maj_ruling", VALID_RULINGS_4, VALID_RULINGS_4),
        ("pred_ch2", VALID_RULINGS_2, VALID_RULINGS_2),
        ("pred_ch16", VALID_RULINGS_2, VALID_RULINGS_2),
        ("pred_naive_mass", VALID_RULINGS_2, VALID_RULINGS_2),
        ("R_read_always_keep", VALID_RULINGS_2, VALID_RULINGS_2),
        ("R_read_always_invert", VALID_RULINGS_2, VALID_RULINGS_2),
        ("lean_R_read_v57_ch2", VALID_RULINGS_2, VALID_RULINGS_2),
        ("lean_R_read_v57_ch16", VALID_RULINGS_2, VALID_RULINGS_2),
        ("lean_R_read_naive_mass", VALID_RULINGS_2, VALID_RULINGS_2),
    ]

    vs_book_ruling: dict[str, dict[str, Any]] = {}
    for scope_name, items in scopes.items():
        book = [x["book_ruling"] for x in items]
        bids = [x["benchmark_id"] for x in items]
        scope_res: dict[str, Any] = {"n": len(items), "benchmark_ids": bids, "raters": {}}
        for rater_key, x_cats, kappa_cats in rater_specs:
            xs = extract_rater(items, rater_key)
            scope_res["raters"][rater_key] = _binary_agreement_block(
                xs, book, x_cats, VALID_RULINGS_2, kappa_cats, row_ids=bids
            )
        vs_book_ruling[scope_name] = scope_res

    # 3. Non-ruling inventory on 17.
    non_ruling_counts = {
        "b1_rule_does_not_say": sum(1 for x in cal_items if x["applier"]["b1_ruling"] == "the rule doesn't say"),
        "b2_rule_does_not_say": sum(1 for x in cal_items if x["applier"]["b2_ruling"] == "the rule doesn't say"),
        "b3_rule_does_not_say": sum(1 for x in cal_items if x["applier"]["b3_ruling"] == "the rule doesn't say"),
        "b_maj_rule_does_not_say": sum(1 for x in cal_items if x["applier"]["b_maj_ruling"] == "the rule doesn't say"),
        "b_maj_no_majority": sum(1 for x in cal_items if x["applier"]["b_maj_ruling"] == "no_majority"),
        "b_maj_Keep": sum(1 for x in cal_items if x["applier"]["b_maj_ruling"] == "Keep"),
        "b_maj_Invert": sum(1 for x in cal_items if x["applier"]["b_maj_ruling"] == "Invert"),
    }
    n_def_17 = non_ruling_counts["b_maj_Keep"] + non_ruling_counts["b_maj_Invert"]
    non_ruling_rows_17 = [
        {
            "benchmark_id": x["benchmark_id"],
            "card_id": x["card_id"],
            "label": x["label"],
            "provenance": x["provenance"],
            "book_ruling": x["book_ruling"],
            "b1_ruling": x["applier"]["b1_ruling"],
            "b2_ruling": x["applier"]["b2_ruling"],
            "b3_ruling": x["applier"]["b3_ruling"],
            "b_maj_ruling": x["applier"]["b_maj_ruling"],
        }
        for x in cal_items
        if x["applier"]["b_maj_ruling"] in ("the rule doesn't say", "no_majority")
        or any(x["applier"][f"b{j}_ruling"] == "the rule doesn't say" for j in (1, 2, 3))
    ]

    # 4. Track (c) on 17: inter-session Fleiss, q_maj vs Lean predicates, induced vs Lean static.
    q_lean_map = {
        "q1": ("isIdentityOrEquiv", "lean_q1"),
        "q2": ("hasMass", "lean_q2"),
        "q3": ("lawAST == .SpatialSeparationDependence", "lean_q3"),
        "q4": ("isSharedEnergyWork", "lean_q4"),
    }
    track_c_inter_session: dict[str, Any] = {}
    majority_vs_lean_predicates: dict[str, Any] = {}
    for q_key, (lean_pred_name, lean_col) in q_lean_map.items():
        q_rows = [
            (x["label_row"][f"c1_{q_key}"], x["label_row"][f"c2_{q_key}"], x["label_row"][f"c3_{q_key}"])
            for x in cal_items
        ]
        fk = fleiss_kappa_exact(q_rows, VALID_BINARY)
        track_c_inter_session[q_key] = {
            "pairwise_agreement_rate": fk["P_bar"],
            "unanimous_agreement_rate": fk["unanimous_rate"],
            "fleiss_kappa_2cat": fk,
        }

        q_maj_vals = [x["label_row"][f"{q_key}_maj"] for x in cal_items]
        lean_vals = ["Yes" if x["lean"][lean_col] else "No" for x in cal_items]
        blk = _binary_agreement_block(
            q_maj_vals,
            lean_vals,
            VALID_BINARY,
            VALID_BINARY,
            VALID_BINARY,
            row_ids=[x["benchmark_id"] for x in cal_items],
        )
        mismatches = [
            {
                "benchmark_id": x["benchmark_id"],
                "card_id": x["card_id"],
                "label": x["label"],
                f"{q_key}_maj": qm,
                lean_pred_name: lv,
            }
            for x, qm, lv in zip(cal_items, q_maj_vals, lean_vals)
            if qm != lv
        ]
        majority_vs_lean_predicates[q_key] = {
            "lean_predicate": lean_pred_name,
            **blk,
            "mismatch_rows": mismatches,
        }

    induced_vs_lean_static: dict[str, Any] = {}
    for pred_key, lean_key in (
        ("pred_ch2", "lean_R_read_v57_ch2"),
        ("pred_ch16", "lean_R_read_v57_ch16"),
        ("pred_naive_mass", "lean_R_read_naive_mass"),
    ):
        ind_vals = [x["label_row"][pred_key] for x in cal_items]
        lean_vals = [x["lean"][lean_key] for x in cal_items]
        blk = _binary_agreement_block(
            ind_vals,
            lean_vals,
            VALID_RULINGS_2,
            VALID_RULINGS_2,
            VALID_RULINGS_2,
            row_ids=[x["benchmark_id"] for x in cal_items],
        )
        mismatches = [
            {
                "benchmark_id": x["benchmark_id"],
                "card_id": x["card_id"],
                "label": x["label"],
                pred_key: iv,
                lean_key: lv,
            }
            for x, iv, lv in zip(cal_items, ind_vals, lean_vals)
            if iv != lv
        ]
        induced_vs_lean_static[pred_key] = {
            "lean_static_rule": lean_key,
            **blk,
            "mismatch_rows": mismatches,
        }

    # 5. Within-session consistency Track (b) vs Track (c) on 17 (overall + 4 vs 13 split).
    within_session_b_vs_c: dict[str, Any] = {}
    for scope_name, items in scopes.items():
        scope_ws: dict[str, Any] = {
            "n": len(items),
            "within_session_note": "Within-session codebook-to-prose consistency (q1..q4 and ruling share each session).",
            "comparisons": {},
        }
        for pred_key in ("pred_ch16", "pred_ch2"):
            ys = [x["label_row"][pred_key] for x in items]
            for rater_key, x_cats, kappa_cats in (
                ("b_maj_ruling", VALID_RULINGS_4, VALID_RULINGS_4),
                ("b1", VALID_RULINGS_3, VALID_RULINGS_3),
                ("b2", VALID_RULINGS_3, VALID_RULINGS_3),
                ("b3", VALID_RULINGS_3, VALID_RULINGS_3),
            ):
                xs = extract_rater(items, rater_key)
                comp_name = f"{rater_key}_vs_{pred_key}"
                blk = _binary_agreement_block(
                    xs, ys, x_cats, VALID_RULINGS_2, kappa_cats,
                    row_ids=[x["benchmark_id"] for x in items],
                )
                def_pairs = [(xv, yv) for xv, yv in zip(xs, ys) if xv in VALID_RULINGS_2]
                def_block = None
                if def_pairs:
                    d_xs, d_ys = zip(*def_pairs)
                    def_block = _binary_agreement_block(
                        d_xs, d_ys, VALID_RULINGS_2, VALID_RULINGS_2, VALID_RULINGS_2
                    )
                scope_ws["comparisons"][comp_name] = {
                    "unconditional": blk,
                    "conditional_on_definite_b": def_block,
                }
        within_session_b_vs_c[scope_name] = scope_ws

    # 6. Complete 17-row breakdown table.
    row_by_row_table_17: list[dict[str, Any]] = []
    for x in cal_items:
        ep = _compute_predictions(
            x["extra"]["q1"] == "Yes",
            x["extra"]["q2"] == "Yes",
            x["extra"]["q3"] == "Yes",
            x["extra"]["q4"] == "Yes",
        )
        row_by_row_table_17.append(
            {
                "benchmark_id": x["benchmark_id"],
                "card_id": x["card_id"],
                "label": x["label"],
                "provenance": x["provenance"],
                "book_ruling": x["book_ruling"],
                "lean_predicates": {
                    "isIdentityOrEquiv": x["lean"]["lean_q1"],
                    "hasMass": x["lean"]["lean_q2"],
                    "SpatialSeparationDependence": x["lean"]["lean_q3"],
                    "isSharedEnergyWork": x["lean"]["lean_q4"],
                },
                "lean_R_read_v57_ch2": x["lean"]["lean_R_read_v57_ch2"],
                "lean_R_read_v57_ch16": x["lean"]["lean_R_read_v57_ch16"],
                "b1_ruling": x["applier"]["b1_ruling"],
                "b2_ruling": x["applier"]["b2_ruling"],
                "b3_ruling": x["applier"]["b3_ruling"],
                "b_maj_ruling": x["applier"]["b_maj_ruling"],
                "q1_maj": x["label_row"]["q1_maj"],
                "q2_maj": x["label_row"]["q2_maj"],
                "q3_maj": x["label_row"]["q3_maj"],
                "q4_maj": x["label_row"]["q4_maj"],
                "pred_ch2": x["label_row"]["pred_ch2"],
                "pred_ch16": x["label_row"]["pred_ch16"],
                "pred_naive_mass": x["label_row"]["pred_naive_mass"],
                "extra_gemini_hydrogen_ruling": x["extra"]["ruling"],
                "extra_gemini_hydrogen_pred_ch16": ep["pred_ch16"],
            }
        )

    return {
        "n": 17,
        "never_pooled_with_heldout": True,
        "provenance_counts": {"construction": 4, "applied_later": 13},
        "track_b_inter_session_agreement": {
            "fleiss_kappa_3cat_17": fleiss_b_3cat,
            "unanimously_definite_subset": {
                "count": len(unanimously_def_rows),
                "total": 17,
                "coverage": frac_dict(Fraction(len(unanimously_def_rows), 17)),
                "fleiss_kappa_2cat": fleiss_b_2cat_unanimous,
            },
        },
        "vs_book_ruling": vs_book_ruling,
        "non_ruling_inventory": {
            "counts": non_ruling_counts,
            "N_def": n_def_17,
            "definite_coverage": frac_dict(Fraction(n_def_17, 17)),
            "rows": non_ruling_rows_17,
        },
        "track_c_codebook_on_17": {
            "inter_session_fleiss_kappa": track_c_inter_session,
            "majority_vs_lean_predicates": majority_vs_lean_predicates,
            "induced_vs_lean_static_readings": induced_vs_lean_static,
            "induced_vs_book_ruling": {
                scope_name: {
                    "n": vs_book_ruling[scope_name]["n"],
                    "pred_ch2": vs_book_ruling[scope_name]["raters"]["pred_ch2"],
                    "pred_ch16": vs_book_ruling[scope_name]["raters"]["pred_ch16"],
                }
                for scope_name in ("overall", "construction", "applied_later")
            },
        },
        "within_session_consistency_b_vs_c": within_session_b_vs_c,
        "row_by_row_table_17": row_by_row_table_17,
    }


def _build_panel_metrics(
    heldout_ids: list[str],
    cal_ids: list[str],
    panel_records: dict[str, dict[str, dict[str, str]]],
    manifest: dict[str, dict[str, str]],
    lean_by_id: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    """
    Compute confirmatory/descriptive metrics for any 3-session panel on heldout_48 and calibration_17.
    panel_records[cid] holds {"s1": {...}, "s2": {...}, "s3": {...}} with keys q1..q4, ruling.
    """
    b_rows_48: list[tuple[str, str, str]] = []
    b_maj_48: list[str] = []
    pred_ch16_48: list[str] = []
    pred_ch2_48: list[str] = []
    pred_naive_48: list[str] = []
    q_rows_48: dict[str, list[tuple[str, str, str]]] = {f"q{i}": [] for i in range(1, 5)}

    for cid in heldout_ids:
        recs = panel_records[cid]
        r_tuple = (recs["s1"]["ruling"], recs["s2"]["ruling"], recs["s3"]["ruling"])
        b_rows_48.append(r_tuple)
        b_maj_48.append(_majority_ruling(r_tuple))
        q_bools: list[bool] = []
        for q_key in ("q1", "q2", "q3", "q4"):
            qt = (recs["s1"][q_key], recs["s2"][q_key], recs["s3"][q_key])
            q_rows_48[q_key].append(qt)
            q_bools.append(_majority_binary(qt) == "Yes")
        preds = _compute_predictions(*q_bools)
        pred_ch16_48.append(preds["pred_ch16"])
        pred_ch2_48.append(preds["pred_ch2"])
        pred_naive_48.append(preds["pred_naive_mass"])

    fleiss_3cat_48 = fleiss_kappa_exact(b_rows_48, VALID_RULINGS_3)
    unan_def_48 = [r for r in b_rows_48 if all(x in VALID_RULINGS_2 for x in r)]
    fleiss_2cat_unan_48 = fleiss_kappa_exact(unan_def_48, VALID_RULINGS_2)
    q_fleiss_48 = {q_key: fleiss_kappa_exact(q_rows_48[q_key], VALID_BINARY) for q_key in ("q1", "q2", "q3", "q4")}

    def_indices = [i for i, b in enumerate(b_maj_48) if b in VALID_RULINGS_2]
    b_def = [b_maj_48[i] for i in def_indices]
    p16_def = [pred_ch16_48[i] for i in def_indices]
    p2_def = [pred_ch2_48[i] for i in def_indices]
    pn_def = [pred_naive_48[i] for i in def_indices]
    keep_def = ["Keep" for _ in def_indices]
    inv_def = ["Invert" for _ in def_indices]

    ch16_cond = _evaluate_binary_classifier(p16_def, b_def)
    cond1_pass = (not fleiss_3cat_48["degenerate_single_category"]) and (
        Fraction(fleiss_3cat_48["kappa"]["num"], fleiss_3cat_48["kappa"]["den"]) >= Fraction(3, 5)
    )
    p_val_16 = Fraction(ch16_cond["fisher_p_one_sided"]["num"], ch16_cond["fisher_p_one_sided"]["den"])
    cond2_pass = (not ch16_cond["degenerate_class"]) and (p_val_16 < Fraction(1, 20))
    cond3_pass = (not ch16_cond["degenerate_class"]) and (ch16_cond["L_BA"] is not None) and (ch16_cond["L_BA"] > 0.50)

    # Unconditional 48 counts.
    b_maj_counts = Counter(b_maj_48)
    n_def = len(def_indices)

    def uncond_block(preds: Sequence[str]) -> dict[str, Any]:
        matches = sum(1 for b, p in zip(b_maj_48, preds) if b == p)
        return {
            "matches": matches,
            "total": 48,
            "agreement_rate": frac_dict(Fraction(matches, 48)),
            "confusion_matrix_4x2": confusion_matrix_dict(b_maj_48, preds, VALID_RULINGS_4, VALID_RULINGS_2),
            "cohen_kappa_4cat": cohen_kappa_exact(b_maj_48, preds, VALID_RULINGS_4),
        }

    uncond_all = {
        "pred_ch16": uncond_block(pred_ch16_48),
        "pred_ch2": uncond_block(pred_ch2_48),
        "pred_naive_mass": uncond_block(pred_naive_48),
        "R_read_always_keep": uncond_block(["Keep" for _ in heldout_ids]),
        "R_read_always_invert": uncond_block(["Invert" for _ in heldout_ids]),
    }

    cond_all = {
        "pred_ch16": ch16_cond,
        "pred_ch2": _evaluate_binary_classifier(p2_def, b_def),
        "pred_naive_mass": _evaluate_binary_classifier(pn_def, b_def),
        "R_read_always_keep": _evaluate_binary_classifier(keep_def, b_def),
        "R_read_always_invert": _evaluate_binary_classifier(inv_def, b_def),
    }

    # Calibration 17 summary for this panel.
    cal_sorted = sorted(cal_ids, key=lambda cid: int(manifest[cid]["benchmark_id"]))
    cal_b_rows: list[tuple[str, str, str]] = []
    cal_b_maj: list[str] = []
    cal_pred_ch2: list[str] = []
    cal_pred_ch16: list[str] = []
    cal_book: list[str] = []
    cal_prov: list[str] = []
    cal_s1_ruling: list[str] = []

    for cid in cal_sorted:
        bid = int(manifest[cid]["benchmark_id"])
        recs = panel_records[cid]
        rt = (recs["s1"]["ruling"], recs["s2"]["ruling"], recs["s3"]["ruling"])
        cal_b_rows.append(rt)
        cal_b_maj.append(_majority_ruling(rt))
        cal_s1_ruling.append(recs["s1"]["ruling"])
        q_bools = [
            _majority_binary((recs["s1"][qk], recs["s2"][qk], recs["s3"][qk])) == "Yes"
            for qk in ("q1", "q2", "q3", "q4")
        ]
        preds = _compute_predictions(*q_bools)
        cal_pred_ch2.append(preds["pred_ch2"])
        cal_pred_ch16.append(preds["pred_ch16"])
        cal_book.append(lean_by_id[bid]["bookRuling"])
        cal_prov.append("construction" if bid in CONSTRUCTION_BENCHMARK_IDS else "applied_later")

    cal_fleiss_3cat = fleiss_kappa_exact(cal_b_rows, VALID_RULINGS_3)
    cal_n_def = sum(1 for b in cal_b_maj if b in VALID_RULINGS_2)

    def cal_scope_vs_book(series: Sequence[str], x_cats: Sequence[str]) -> dict[str, Any]:
        res: dict[str, Any] = {}
        for scope_name, pred_fn in (
            ("overall", lambda _: True),
            ("construction", lambda p: p == "construction"),
            ("applied_later", lambda p: p == "applied_later"),
        ):
            idx = [i for i, pv in enumerate(cal_prov) if pred_fn(pv)]
            sub_x = [series[i] for i in idx]
            sub_y = [cal_book[i] for i in idx]
            matches = sum(1 for x, y in zip(sub_x, sub_y) if x == y)
            res[scope_name] = {
                "n": len(idx),
                "matches": matches,
                "agreement_rate": frac_dict(Fraction(matches, len(idx))),
                "confusion_matrix": confusion_matrix_dict(sub_x, sub_y, x_cats, VALID_RULINGS_2),
            }
        return res

    cal_summary = {
        "n": 17,
        "fleiss_kappa_3cat_17": cal_fleiss_3cat,
        "N_def": cal_n_def,
        "definite_coverage": frac_dict(Fraction(cal_n_def, 17)),
        "b_maj_counts": {k: sum(1 for b in cal_b_maj if b == k) for k in VALID_RULINGS_4},
        "vs_book_ruling": {
            "s1_extra": cal_scope_vs_book(cal_s1_ruling, VALID_RULINGS_3),
            "b_maj_ruling": cal_scope_vs_book(cal_b_maj, VALID_RULINGS_4),
            "pred_ch2": cal_scope_vs_book(cal_pred_ch2, VALID_RULINGS_2),
            "pred_ch16": cal_scope_vs_book(cal_pred_ch16, VALID_RULINGS_2),
        },
        "within_session_b_maj_vs_pred_ch16": _binary_agreement_block(
            cal_b_maj, cal_pred_ch16, VALID_RULINGS_4, VALID_RULINGS_2, VALID_RULINGS_4
        ),
    }

    return {
        "b_rows_48": b_rows_48,
        "b_maj_48": b_maj_48,
        "pred_ch16_48": pred_ch16_48,
        "pred_ch2_48": pred_ch2_48,
        "pred_naive_48": pred_naive_48,
        "q_rows_48": q_rows_48,
        "fleiss_3cat_48": fleiss_3cat_48,
        "fleiss_2cat_unan_48": fleiss_2cat_unan_48,
        "unan_def_count_48": len(unan_def_48),
        "q_fleiss_48": q_fleiss_48,
        "b_maj_counts_48": {k: b_maj_counts.get(k, 0) for k in VALID_RULINGS_4},
        "N_def": n_def,
        "ch16_cond": ch16_cond,
        "cond1_pass": cond1_pass,
        "cond2_pass": cond2_pass,
        "cond3_pass": cond3_pass,
        "passes_all_three": cond1_pass and cond2_pass and cond3_pass,
        "uncond_all": uncond_all,
        "cond_all": cond_all,
        "cal_summary": cal_summary,
    }


def build_heldout_48_section(data: dict[str, Any]) -> dict[str, Any]:
    """Build Section 2 (heldout_48) strictly on the 48 primary held-out cards."""
    manifest = data["manifest_by_id"]
    pool_by_law_id = data["pool_by_law_id"]
    appliers = data["appliers_by_id"]
    labels = data["labels_by_id"]
    extra = data["extra_by_id"]
    lean_by_id = data["lean_by_id"]

    heldout_ids = sorted(data["heldout_ids"])
    cal_ids = sorted(data["cal_ids"])
    assert len(heldout_ids) == 48 and len(cal_ids) == 17

    # Construct panel records for primary panel (s1=gemini_carbon, s2=grok_4_7, s3=kimi_k3).
    primary_records: dict[str, dict[str, dict[str, str]]] = {}
    swap_records: dict[str, dict[str, dict[str, str]]] = {}
    for cid in heldout_ids + cal_ids:
        a = appliers[cid]
        l = labels[cid]
        e = extra[cid]
        s1_rec = {"ruling": a["b1_ruling"], "q1": l["c1_q1"], "q2": l["c1_q2"], "q3": l["c1_q3"], "q4": l["c1_q4"]}
        s2_rec = {"ruling": a["b2_ruling"], "q1": l["c2_q1"], "q2": l["c2_q2"], "q3": l["c2_q3"], "q4": l["c2_q4"]}
        s3_rec = {"ruling": a["b3_ruling"], "q1": l["c3_q1"], "q2": l["c3_q2"], "q3": l["c3_q3"], "q4": l["c3_q4"]}
        extra_rec = {"ruling": e["ruling"], "q1": e["q1"], "q2": e["q2"], "q3": e["q3"], "q4": e["q4"]}
        primary_records[cid] = {"s1": s1_rec, "s2": s2_rec, "s3": s3_rec}
        swap_records[cid] = {"s1": extra_rec, "s2": s2_rec, "s3": s3_rec}

    pm = _build_panel_metrics(heldout_ids, cal_ids, primary_records, manifest, lean_by_id)
    sw = _build_panel_metrics(heldout_ids, cal_ids, swap_records, manifest, lean_by_id)

    ch16_c = pm["ch16_cond"]
    confirmatory_primary_test = {
        "passes_all_three": pm["passes_all_three"],
        "condition_1_across_family_independence": {
            "description": "3-category Fleiss' kappa among (b1, b2, b3) across all 48 held-out laws >= 3/5 (0.60)",
            "threshold": frac_dict(Fraction(3, 5)),
            "fleiss_kappa_3cat_48": pm["fleiss_3cat_48"]["kappa"],
            "P_bar": pm["fleiss_3cat_48"]["P_bar"],
            "P_e": pm["fleiss_3cat_48"]["P_e"],
            "passes": pm["cond1_pass"],
        },
        "condition_2_within_session_association": {
            "description": "One-sided Fisher's exact p < 1/20 (0.05) for pred_ch16 vs definite b_maj_ruling (Invert as positive class)",
            "within_session_disclosure": "Tests within-session codebook-to-prose consistency under Amendment 2.",
            "threshold": frac_dict(Fraction(1, 20)),
            "N_def": ch16_c["N"],
            "tp": ch16_c["tp"],
            "fp": ch16_c["fp"],
            "fn": ch16_c["fn"],
            "tn": ch16_c["tn"],
            "confusion_matrix_2x2": ch16_c["confusion_matrix_2x2"],
            "fisher_p_one_sided": ch16_c["fisher_p_one_sided"],
            "passes": pm["cond2_pass"],
        },
        "condition_3_within_session_balanced_accuracy_ci": {
            "description": "Closed-form 95% Wilson-MOVER lower bound L_BA > 0.50 for pred_ch16 vs definite b_maj_ruling",
            "within_session_disclosure": "Tests within-session codebook-to-prose consistency under Amendment 2.",
            "threshold_L_BA": 0.5,
            "z": ch16_c["z"],
            "n1_actual_invert": ch16_c["n1"],
            "k1_matched_invert": ch16_c["k1"],
            "n2_actual_keep": ch16_c["n2"],
            "k2_matched_keep": ch16_c["k2"],
            "TPR": ch16_c["TPR"],
            "TNR": ch16_c["TNR"],
            "conditional_acc": ch16_c["conditional_acc"],
            "BA": ch16_c["BA"],
            "wilson_class1_invert": ch16_c["wilson_class1"],
            "wilson_class2_keep": ch16_c["wilson_class2"],
            "L_BA": ch16_c["L_BA"],
            "U_BA": ch16_c["U_BA"],
            "degenerate_class": ch16_c["degenerate_class"],
            "passes": pm["cond3_pass"],
        },
    }

    # Non-ruling inventory.
    non_ruling_counts = {
        "b1_counts": dict(Counter(appliers[c]["b1_ruling"] for c in heldout_ids)),
        "b2_counts": dict(Counter(appliers[c]["b2_ruling"] for c in heldout_ids)),
        "b3_counts": dict(Counter(appliers[c]["b3_ruling"] for c in heldout_ids)),
        "b_maj_counts": pm["b_maj_counts_48"],
        "b1_rule_does_not_say": sum(1 for c in heldout_ids if appliers[c]["b1_ruling"] == "the rule doesn't say"),
        "b2_rule_does_not_say": sum(1 for c in heldout_ids if appliers[c]["b2_ruling"] == "the rule doesn't say"),
        "b3_rule_does_not_say": sum(1 for c in heldout_ids if appliers[c]["b3_ruling"] == "the rule doesn't say"),
        "b_maj_rule_does_not_say": pm["b_maj_counts_48"]["the rule doesn't say"],
        "b_maj_no_majority": pm["b_maj_counts_48"]["no_majority"],
    }
    non_ruling_laws: list[dict[str, Any]] = []
    for cid in heldout_ids:
        a = appliers[cid]
        m = manifest[cid]
        p = pool_by_law_id[m["law_id"]]
        if a["b_maj_ruling"] in ("the rule doesn't say", "no_majority") or any(
            a[f"b{j}_ruling"] == "the rule doesn't say" for j in (1, 2, 3)
        ):
            non_ruling_laws.append(
                {
                    "card_id": cid,
                    "law_id": m["law_id"],
                    "volume": int(m["volume"]),
                    "chapter": int(m["chapter"]),
                    "eq_number": m["eq_number"],
                    "description": p["description"],
                    "b1_ruling": a["b1_ruling"],
                    "b2_ruling": a["b2_ruling"],
                    "b3_ruling": a["b3_ruling"],
                    "b_maj_ruling": a["b_maj_ruling"],
                }
            )

    # Individual appliers vs pred_ch16 & pred_ch2 unconditionally across 48.
    indiv_uncond: dict[str, Any] = {}
    for b_key, m_name in (("b1", "gemini_carbon"), ("b2", "grok_4_7"), ("b3", "kimi_k3")):
        b_vals = [appliers[c][f"{b_key}_ruling"] for c in heldout_ids]
        indiv_uncond[b_key] = {"model_family": m_name}
        for pred_key in ("pred_ch16", "pred_ch2"):
            p_vals = [labels[c][pred_key] for c in heldout_ids]
            matches = sum(1 for bv, pv in zip(b_vals, p_vals) if bv == pv)
            indiv_uncond[b_key][f"vs_{pred_key}"] = {
                "matches": matches,
                "total": 48,
                "agreement_rate": frac_dict(Fraction(matches, 48)),
                "confusion_matrix_3x2": confusion_matrix_dict(
                    b_vals, p_vals, VALID_RULINGS_3, VALID_RULINGS_2
                ),
            }

    # Conditional L313: b1..b3 vs pred_ch16 across all 48 AND restricted to N_def.
    def_ids = [c for c in heldout_ids if appliers[c]["b_maj_ruling"] in VALID_RULINGS_2]
    indiv_l313: dict[str, Any] = {"across_all_48": {}, "restricted_to_N_def": {}}
    for scope_label, id_list in (("across_all_48", heldout_ids), ("restricted_to_N_def", def_ids)):
        p16_sub = [labels[c]["pred_ch16"] for c in id_list]
        for b_key, m_name in (("b1", "gemini_carbon"), ("b2", "grok_4_7"), ("b3", "kimi_k3")):
            b_sub = [appliers[c][f"{b_key}_ruling"] for c in id_list]
            indiv_l313[scope_label][b_key] = {
                "model_family": m_name,
                **_evaluate_applier_vs_pred_l313(b_sub, p16_sub),
            }

    # Per-chapter breakdown across all 22 chapters.
    pool_counts_by_ch = Counter((int(r["volume"]), int(r["chapter"])) for r in data["pool_rows"])
    per_chapter_breakdown: list[dict[str, Any]] = []
    for vol, ch, ch_title in INCLUDED_CHAPTERS:
        ch_cids = [
            c for c in heldout_ids
            if int(manifest[c]["volume"]) == vol and int(manifest[c]["chapter"]) == ch
        ]
        ch_bmaj = Counter(appliers[c]["b_maj_ruling"] for c in ch_cids)
        ch_p16 = Counter(labels[c]["pred_ch16"] for c in ch_cids)
        ch_p2 = Counter(labels[c]["pred_ch2"] for c in ch_cids)
        ch_n_def = ch_bmaj["Keep"] + ch_bmaj["Invert"]
        per_chapter_breakdown.append(
            {
                "volume": vol,
                "chapter": ch,
                "chapter_title": ch_title,
                "eligible_pool_count": pool_counts_by_ch.get((vol, ch), 0),
                "heldout_count": len(ch_cids),
                "N_def": ch_n_def,
                "b_maj_counts": {k: ch_bmaj.get(k, 0) for k in VALID_RULINGS_4},
                "pred_ch16_counts": {k: ch_p16.get(k, 0) for k in VALID_RULINGS_2},
                "pred_ch2_counts": {k: ch_p2.get(k, 0) for k in VALID_RULINGS_2},
                "unanimous_b_agree_count": sum(
                    1
                    for c in ch_cids
                    if appliers[c]["b1_ruling"] == appliers[c]["b2_ruling"] == appliers[c]["b3_ruling"]
                ),
                "b_maj_eq_pred_ch16_count": sum(
                    1 for c in ch_cids if appliers[c]["b_maj_ruling"] == labels[c]["pred_ch16"]
                ),
                "b_maj_eq_pred_ch2_count": sum(
                    1 for c in ch_cids if appliers[c]["b_maj_ruling"] == labels[c]["pred_ch2"]
                ),
                "laws": [
                    {
                        "card_id": c,
                        "law_id": manifest[c]["law_id"],
                        "description": pool_by_law_id[manifest[c]["law_id"]]["description"],
                        "b1_ruling": appliers[c]["b1_ruling"],
                        "b2_ruling": appliers[c]["b2_ruling"],
                        "b3_ruling": appliers[c]["b3_ruling"],
                        "b_maj_ruling": appliers[c]["b_maj_ruling"],
                        "pred_ch2": labels[c]["pred_ch2"],
                        "pred_ch16": labels[c]["pred_ch16"],
                    }
                    for c in ch_cids
                ],
            }
        )

    # All-4-runs descriptive statistics.
    all4_b_48 = [
        (appliers[c]["b1_ruling"], appliers[c]["b2_ruling"], appliers[c]["b3_ruling"], extra[c]["ruling"])
        for c in heldout_ids
    ]
    all4_b_unan_def_48 = [r for r in all4_b_48 if all(x in VALID_RULINGS_2 for x in r)]
    all4_q_48 = {
        qk: fleiss_kappa_exact(
            [(labels[c][f"c1_{qk}"], labels[c][f"c2_{qk}"], labels[c][f"c3_{qk}"], extra[c][qk]) for c in heldout_ids],
            VALID_BINARY,
        )
        for qk in ("q1", "q2", "q3", "q4")
    }

    cal_sorted = sorted(cal_ids, key=lambda c: int(manifest[c]["benchmark_id"]))
    all4_b_17 = [
        (appliers[c]["b1_ruling"], appliers[c]["b2_ruling"], appliers[c]["b3_ruling"], extra[c]["ruling"])
        for c in cal_sorted
    ]
    all4_q_17 = {
        qk: fleiss_kappa_exact(
            [(labels[c][f"c1_{qk}"], labels[c][f"c2_{qk}"], labels[c][f"c3_{qk}"], extra[c][qk]) for c in cal_sorted],
            VALID_BINARY,
        )
        for qk in ("q1", "q2", "q3", "q4")
    }

    gemini_run_comparison_48 = {
        "ruling": _binary_agreement_block(
            [appliers[c]["b1_ruling"] for c in heldout_ids],
            [extra[c]["ruling"] for c in heldout_ids],
            VALID_RULINGS_3,
            VALID_RULINGS_3,
            VALID_RULINGS_3,
        ),
        **{
            qk: _binary_agreement_block(
                [labels[c][f"c1_{qk}"] for c in heldout_ids],
                [extra[c][qk] for c in heldout_ids],
                VALID_BINARY,
                VALID_BINARY,
                VALID_BINARY,
            )
            for qk in ("q1", "q2", "q3", "q4")
        },
    }

    descriptive_sensitivity = {
        "status": "DESCRIPTIVE_SENSITIVITY_ONLY",
        "swap_in_gemini_hydrogen_panel": {
            "models": {"s1_extra": EXTRA_MODEL, "s2": "grok_4_7", "s3": "kimi_k3"},
            "heldout_48": {
                "fleiss_kappa_3cat_48": sw["fleiss_3cat_48"],
                "unanimously_definite_subset": {
                    "count": sw["unan_def_count_48"],
                    "total": 48,
                    "coverage": frac_dict(Fraction(sw["unan_def_count_48"], 48)),
                    "fleiss_kappa_2cat": sw["fleiss_2cat_unan_48"],
                },
                "codebook_fleiss_kappa_2cat_48": sw["q_fleiss_48"],
                "N_def": sw["N_def"],
                "definite_coverage": frac_dict(Fraction(sw["N_def"], 48)),
                "b_maj_counts": sw["b_maj_counts_48"],
                "confirmatory_components_descriptive": {
                    "would_pass_all_three_if_primary": sw["passes_all_three"],
                    "cond1_fleiss_ge_0_60": sw["cond1_pass"],
                    "cond2_fisher_lt_0_05": sw["cond2_pass"],
                    "cond3_L_BA_gt_0_50": sw["cond3_pass"],
                    **sw["ch16_cond"],
                },
                "unconditional_48": sw["uncond_all"],
                "conditional_definite": sw["cond_all"],
            },
            "calibration_17_summary": sw["cal_summary"],
        },
        "all_4_runs_descriptive": {
            "models": ["gemini_carbon", "grok_4_7", "kimi_k3", EXTRA_MODEL],
            "heldout_48": {
                "fleiss_kappa_3cat_48": fleiss_kappa_exact(all4_b_48, VALID_RULINGS_3),
                "unanimously_definite_subset": {
                    "count": len(all4_b_unan_def_48),
                    "total": 48,
                    "coverage": frac_dict(Fraction(len(all4_b_unan_def_48), 48)),
                    "fleiss_kappa_2cat": fleiss_kappa_exact(all4_b_unan_def_48, VALID_RULINGS_2),
                },
                "codebook_fleiss_kappa_2cat_48": all4_q_48,
                "gemini_carbon_vs_gemini_hydrogen_48": gemini_run_comparison_48,
            },
            "calibration_17": {
                "fleiss_kappa_3cat_17": fleiss_kappa_exact(all4_b_17, VALID_RULINGS_3),
                "codebook_fleiss_kappa_2cat_17": all4_q_17,
            },
        },
    }

    return {
        "n": 48,
        "never_pooled_with_calibration_17": True,
        "confirmatory_primary_test": confirmatory_primary_test,
        "inter_session_agreement": {
            "track_b_fleiss_kappa_3cat_48": pm["fleiss_3cat_48"],
            "track_b_unanimously_definite_subset": {
                "count": pm["unan_def_count_48"],
                "total": 48,
                "coverage": frac_dict(Fraction(pm["unan_def_count_48"], 48)),
                "fleiss_kappa_2cat": pm["fleiss_2cat_unan_48"],
            },
            "track_c_codebook_fleiss_kappa_2cat_48": pm["q_fleiss_48"],
        },
        "non_ruling_inventory": {
            "counts": non_ruling_counts,
            "N_def": pm["N_def"],
            "definite_coverage": frac_dict(Fraction(pm["N_def"], 48)),
            "laws": non_ruling_laws,
        },
        "unconditional_48": {
            "b_maj_ruling_vs_predictors": pm["uncond_all"],
            "individual_appliers_vs_predictors": indiv_uncond,
        },
        "conditional_definite": {
            "N_def": pm["N_def"],
            "predictors_vs_definite_b_maj": pm["cond_all"],
            "individual_appliers_vs_pred_ch16_per_L313": indiv_l313,
        },
        "per_chapter_breakdown": per_chapter_breakdown,
        "descriptive_sensitivity": descriptive_sensitivity,
    }


def _format_disagreement_note(
    cid: str,
    applier_row: dict[str, str],
    label_row: dict[str, str],
) -> str:
    """Build a concise, factual one-line note describing every observed divergence for cid."""
    b1 = applier_row["b1_ruling"]
    b2 = applier_row["b2_ruling"]
    b3 = applier_row["b3_ruling"]
    bmaj = applier_row["b_maj_ruling"]
    ch2 = label_row["pred_ch2"]
    ch16 = label_row["pred_ch16"]

    if b1 == b2 == b3:
        b_part = f"Unanimous Track (b) {bmaj}"
    elif bmaj == "no_majority":
        b_part = f"3-way Track (b) split (b1={b1}, b2={b2}, b3={b3} -> no_majority)"
    else:
        b_part = f"Track (b) split (b1={b1}, b2={b2}, b3={b3} -> b_maj={bmaj})"

    q_vec = ",".join(label_row[f"q{i}_maj"] for i in range(1, 5))
    q_splits: list[str] = []
    for i in range(1, 5):
        votes = [label_row[f"c{j}_q{i}"] for j in (1, 2, 3)]
        if len(set(votes)) > 1:
            q_splits.append(f"q{i} 2-1 ({'/'.join(votes)})")
    split_txt = f"; splits: {', '.join(q_splits)}" if q_splits else "; unanimous q1..q4"

    if ch2 != ch16:
        c_part = f"pred_ch2={ch2} vs pred_ch16={ch16} (q4_maj=Yes)"
    elif bmaj != ch16:
        c_part = f"b_maj={bmaj} vs pred_ch2=pred_ch16={ch16}"
    else:
        c_part = f"pred_ch2=pred_ch16={ch16}"

    reason = _CARD_FACTUAL_REASON[cid]
    note = f"{b_part}; {c_part}; q_maj=({q_vec}){split_txt}; {reason}."
    return " ".join(note.split())


def render_disagreements_bytes(data: dict[str, Any]) -> tuple[bytes, list[dict[str, str]]]:
    """Render deterministic CSV bytes for all held-out disagreement/non-ruling cards."""
    manifest = data["manifest_by_id"]
    pool = data["pool_by_law_id"]
    appliers = data["appliers_by_id"]
    labels = data["labels_by_id"]

    rows: list[dict[str, str]] = []
    for cid in sorted(data["heldout_ids"]):
        a = appliers[cid]
        l = labels[cid]
        vals = {
            a["b1_ruling"],
            a["b2_ruling"],
            a["b3_ruling"],
            a["b_maj_ruling"],
            l["pred_ch2"],
            l["pred_ch16"],
        }
        if len(vals) > 1 or "the rule doesn't say" in vals:
            m = manifest[cid]
            p = pool[m["law_id"]]
            rows.append(
                {
                    "card_id": cid,
                    "law_id": m["law_id"],
                    "volume": m["volume"],
                    "chapter": m["chapter"],
                    "eq_number": m["eq_number"],
                    "description": p["description"],
                    "b1_ruling": a["b1_ruling"],
                    "b2_ruling": a["b2_ruling"],
                    "b3_ruling": a["b3_ruling"],
                    "b_maj_ruling": a["b_maj_ruling"],
                    "pred_ch2": l["pred_ch2"],
                    "pred_ch16": l["pred_ch16"],
                    "note": _format_disagreement_note(cid, a, l),
                }
            )

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=DISAGREEMENTS_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue().encode("utf-8"), rows


def build_results_payload(
    data: dict[str, Any],
    disagreement_rows: list[dict[str, str]],
) -> dict[str, Any]:
    """Assemble the complete part2_results.json payload."""
    cal_17 = build_calibration_17_section(data)
    held_48 = build_heldout_48_section(data)
    held_48["disagreements_csv_summary"] = {
        "row_count": len(disagreement_rows),
        "card_ids": [r["card_id"] for r in disagreement_rows],
    }
    lean_rows = data["lean_rows"]

    return {
        "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
        "amendment_1_commit_sha": AMENDMENT_1_COMMIT_SHA,
        "amendment_2_commit_sha": AMENDMENT_2_COMMIT_SHA,
        "pre_unmasking_commit_sha": PRE_UNMASKING_COMMIT_SHA,
        "attribution": ATTRIBUTION,
        "primary_panel_models": PRIMARY_PANEL_MODELS,
        "extra_sensitivity_model": EXTRA_MODEL,
        "shared_session_disclosure": SHARED_SESSION_DISCLOSURE,
        "claim_scope": {
            "claim_tested": CLAIM_TESTED,
            "not_tested": NOT_TESTED,
        },
        "dataset_partition_invariant": {
            "total_cards": 65,
            "heldout_count": 48,
            "calibration_17_count": 17,
            "overlap_count": 0,
            "never_pooled": True,
        },
        "lean_static_benchmark_verification": {
            "n_rows": len(lean_rows),
            "R_read_v57_ch2": {
                "matches": 14,
                "total": 17,
                "fraction": "14/17",
                "missed_ids": [11, 12, 17],
            },
            "R_read_v57_ch16": {
                "matches": 16,
                "total": 17,
                "fraction": "16/17",
                "missed_ids": [17],
            },
            "R_read_always_keep": {
                "matches": 14,
                "total": 17,
                "fraction": "14/17",
                "missed_ids": [2, 8, 9],
            },
            "R_read_always_invert": {
                "matches": 3,
                "total": 17,
                "fraction": "3/17",
                "matched_ids": [2, 8, 9],
            },
        },
        "calibration_17": cal_17,
        "heldout_48": held_48,
    }


def run(verify_offline: bool) -> dict[str, Any]:
    """Run Part 2 evaluation and write or offline-verify outputs and hygiene."""
    data = load_and_validate_inputs()
    disagreements_bytes, disagreement_rows = render_disagreements_bytes(data)
    results_payload = build_results_payload(data, disagreement_rows)

    results_text = json.dumps(results_payload, indent=2, ensure_ascii=False) + "\n"
    results_bytes = results_text.encode("utf-8")
    disagreements_text = disagreements_bytes.decode("utf-8")

    _check_hygiene(
        [
            (Path(__file__).name, Path(__file__).read_text(encoding="utf-8")),
            (RESULTS_JSON_PATH.name, results_text),
            (DISAGREEMENTS_CSV_PATH.name, disagreements_text),
        ]
    )

    if verify_offline:
        for path, expected_bytes in (
            (RESULTS_JSON_PATH, results_bytes),
            (DISAGREEMENTS_CSV_PATH, disagreements_bytes),
        ):
            if not path.exists():
                raise RuntimeError(f"Missing committed output file: {path}")
            if path.read_bytes() != expected_bytes:
                raise RuntimeError(f"Byte-for-byte mismatch on {path.name}")
    else:
        RESULTS_JSON_PATH.write_bytes(results_bytes)
        DISAGREEMENTS_CSV_PATH.write_bytes(disagreements_bytes)

    prim = results_payload["heldout_48"]["confirmatory_primary_test"]
    return {
        "mode": "verify-offline" if verify_offline else "evaluate",
        "hygiene_passed": True,
        "disagreement_rows": len(disagreement_rows),
        "passes_all_three": prim["passes_all_three"],
        "cond1_fleiss_kappa_3cat_48": prim["condition_1_across_family_independence"]["fleiss_kappa_3cat_48"],
        "cond1_passes": prim["condition_1_across_family_independence"]["passes"],
        "cond2_fisher_p_one_sided": prim["condition_2_within_session_association"]["fisher_p_one_sided"],
        "cond2_passes": prim["condition_2_within_session_association"]["passes"],
        "cond3_BA": prim["condition_3_within_session_balanced_accuracy_ci"]["BA"],
        "cond3_L_BA": prim["condition_3_within_session_balanced_accuracy_ci"]["L_BA"],
        "cond3_U_BA": prim["condition_3_within_session_balanced_accuracy_ci"]["U_BA"],
        "cond3_passes": prim["condition_3_within_session_balanced_accuracy_ci"]["passes"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate Part 2 held-out OpenStax laws and 17-row calibration post-unmasking."
    )
    parser.add_argument(
        "--verify-offline",
        action="store_true",
        help="Recompute part2_results.json and part2_disagreements.csv and verify exact match & hygiene.",
    )
    args = parser.parse_args()
    summary = run(args.verify_offline)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
