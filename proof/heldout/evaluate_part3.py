#!/usr/bin/env python3
"""
evaluate_part3.py — Post-unmasking Part 3 etymology direction control evaluation.

Reads:
  - proof/heldout/etymology_codings.csv
  - proof/heldout/word_coding_key.csv
  - proof/etymology/ledger_80.json

Writes (unless --verify-offline):
  - proof/heldout/part3_item_table.csv
  - proof/heldout/part3_results.json

Python 3.12+ standard library only (exact fractions.Fraction, math.comb).
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
from typing import Any, Callable, Sequence

PREREGISTRATION_COMMIT_SHA = "463ad9f93c8a276b1e0d9ee497198dfa2169d079"
PART3_PRE_UNMASKING_COMMIT_SHA = "cf6f1352a36e798e65c28c6d77cd320180b3761c"
ATTRIBUTION = "Access for free at https://openstax.org — Licensed under CC BY 4.0."
EVALUATION_STATUS = "PROTOCOL_DEVIATED_PRE_UNMASKING"

EXPECTED_ITEM_COUNT = 78
VERIFIED_UTC_DATE = "2026-11-14"
UNVERIFIED_UTC = "unverified"
SOURCE_COVERAGE = "single-source"

TARGETS_10: tuple[str, ...] = (
    "acceleration",
    "density",
    "energy",
    "force",
    "mass",
    "space",
    "speed",
    "time",
    "velocity",
    "volume",
)
EXPECTED_TARGETS_OVERLAP_LEDGER_35: tuple[str, ...] = (
    "density",
    "energy",
    "force",
    "mass",
    "space",
    "time",
    "volume",
)
EXPECTED_TARGET_ONLY: tuple[str, ...] = ("acceleration", "speed", "velocity")

VALID_DIRECTION_CLASSES: tuple[str, ...] = (
    "person_first",
    "physics_first",
    "both_from_start",
    "no_person_sense",
)
VALID_DIRECTION_MAJ_CLASSES: tuple[str, ...] = (
    "person_first",
    "physics_first",
    "both_from_start",
    "no_person_sense",
    "tie_or_disagreement",
)
BINARY_PF_CATEGORIES: tuple[str, ...] = ("person_first", "not_person_first")
BINARY_BOOL_CATEGORIES: tuple[str, ...] = ("true", "false")

LEDGER_KINDS_35_ORDER: tuple[str, ...] = (
    "inward first",
    "either side",
    "outward first",
    "both ways",
    "family",
    "household",
    "nothing to add",
    "not used",
)

HELDOUT_DIR = Path(__file__).resolve().parent
PROOF_DIR = HELDOUT_DIR.parent
REPO_ROOT = PROOF_DIR.parent

ETYMOLOGY_CODINGS_CSV_PATH = HELDOUT_DIR / "etymology_codings.csv"
WORD_CODING_KEY_CSV_PATH = HELDOUT_DIR / "word_coding_key.csv"
LEDGER_80_JSON_PATH = PROOF_DIR / "etymology" / "ledger_80.json"

ITEM_TABLE_CSV_PATH = HELDOUT_DIR / "part3_item_table.csv"
RESULTS_JSON_PATH = HELDOUT_DIR / "part3_results.json"

EXPECTED_CODINGS_FIELDS = [
    "item_id",
    "word",
    "etymonline_url",
    "etymonline_retrieved_utc",
    "source_coverage",
    "s1_model",
    "s1_retrieved_utc",
    "s1_earliest_person_sense",
    "s1_earliest_physics_sense",
    "s1_direction_class",
    "s2_model",
    "s2_retrieved_utc",
    "s2_earliest_person_sense",
    "s2_earliest_physics_sense",
    "s2_direction_class",
    "s3_model",
    "s3_retrieved_utc",
    "s3_earliest_person_sense",
    "s3_earliest_physics_sense",
    "s3_direction_class",
    "direction_class_maj",
    "person_first_maj",
    "preregistration_commit_sha",
]

EXPECTED_KEY_FIELDS = [
    "item_id",
    "word",
    "in_targets_10",
    "in_controls_40",
    "in_ledger_physics_35",
    "ledger_stratum",
    "ledger_kind",
    "control_openstax_chapters",
    "preregistration_commit_sha",
]

PART3_ITEM_TABLE_FIELDS = [
    "item_id",
    "word",
    "in_targets_10",
    "in_controls_40",
    "in_ledger_physics_35",
    "ledger_stratum",
    "ledger_kind",
    "control_openstax_chapters",
    "s1_retrieved_utc",
    "s1_direction_class",
    "s2_retrieved_utc",
    "s2_direction_class",
    "s3_retrieved_utc",
    "s3_direction_class",
    "direction_class_maj",
    "person_first_maj",
    "preregistration_commit_sha",
    "part3_pre_unmasking_commit_sha",
]

PROTOCOL_DEVIATION_DISCLOSURE = (
    "Two protocol deviations occurred prior to unmasking and are disclosed upfront: "
    "(1) PREREGISTRATION.md Section 2.4 specified 3 distinct model families, whereas grok_4_7 "
    "refused the task, leaving 2 model families represented across 3 sessions: two Gemini runs "
    "(s1 = gemini_hydrogen, s3 = gemini_carbon; 78/78 retrieved live on 2026-11-14) and one "
    "Anthropic run (s2 = opus_5_5), giving Gemini 2/3 of the majority vote (direction_class_maj). "
    "(2) In s2 (opus_5_5), anti-bot blocking prevented live etymonline.com retrieval after W003, "
    "so only 3/78 items (W001 theory, W002 sound, W003 friction) were verified live on 2026-11-14 "
    "and 75/78 items (W004..W078) were coded from parametric memory marked 'unverified', including "
    "all 10/10 target words, 38/40 control words, and 34/35 ledger_physics_35 words. All session "
    "codings were committed at part3_pre_unmasking_commit_sha before joining with word_coding_key.csv."
)

# Hex-encoded hygiene tokens so restricted substrings never appear literally in repository files.
_FORBIDDEN_SUBSTRINGS_HEX: tuple[str, ...] = (
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
)
_GUARDED_SCAN_HEX = "626c696e64"


def frac_dict(value: Fraction) -> dict[str, Any]:
    """Serialize an exact Fraction with integer numerator/denominator, string, and float."""
    return {
        "num": value.numerator,
        "den": value.denominator,
        "fraction": f"{value.numerator}/{value.denominator}",
        "float": float(value),
    }


def _decode_hex_list(hex_items: Sequence[str]) -> list[str]:
    return [bytes.fromhex(item).decode("utf-8") for item in hex_items]


def _check_hygiene(named_texts: Sequence[tuple[str, str]]) -> None:
    """Verify generated/source texts and every text file under proof/heldout/ pass hygiene."""
    forbidden = _decode_hex_list(_FORBIDDEN_SUBSTRINGS_HEX)
    for label, text in named_texts:
        lowered = text.lower()
        for tok in forbidden:
            if tok.lower() in lowered:
                raise RuntimeError(
                    f"Hygiene check failed in {label}: forbidden token (hex {tok.encode('utf-8').hex()})"
                )

    guarded_token = bytes.fromhex(_GUARDED_SCAN_HEX).decode("utf-8")
    for path in sorted(HELDOUT_DIR.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() in (".pyc", ".png", ".jpg", ".gz"):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if guarded_token in content.lower():
            raise RuntimeError(
                f"Hygiene failure in {path.relative_to(REPO_ROOT)}: guarded hex token {_GUARDED_SCAN_HEX} found"
            )


def _binarize_pf(direction_class: str) -> str:
    return "person_first" if direction_class == "person_first" else "not_person_first"


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


def cohen_kappa_exact(
    xs: Sequence[str],
    ys: Sequence[str],
    categories: Sequence[str],
) -> dict[str, Any]:
    """Compute exact rational Cohen's kappa and agreement rate over categories."""
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
        "agreement_rate": frac_dict(p_o),
        "p_o": frac_dict(p_o),
        "p_e": frac_dict(p_e),
        "confusion_matrix": matrix,
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


def fisher_exact_proportions(
    a: int,
    n1: int,
    c: int,
    n2: int,
) -> tuple[Fraction, Fraction]:
    """
    Compute exact hypergeometric one-sided upper-tail p (target > control)
    and exact two-sided Fisher p (sum of hypergeometric probabilities <= P(X=a))
    using exact Fraction arithmetic.
    """
    if n1 <= 0 or n2 <= 0 or not (0 <= a <= n1) or not (0 <= c <= n2):
        raise ValueError(f"Invalid Fisher counts: a={a}, n1={n1}, c={c}, n2={n2}")

    total_pos = a + c
    total_n = n1 + n2
    denom = math.comb(total_n, total_pos)
    min_x = max(0, total_pos - n2)
    max_x = min(n1, total_pos)

    probs: list[tuple[int, Fraction]] = [
        (x, Fraction(math.comb(n1, x) * math.comb(n2, total_pos - x), denom))
        for x in range(min_x, max_x + 1)
    ]
    if sum((p for _, p in probs), Fraction(0)) != Fraction(1, 1):
        raise RuntimeError("Hypergeometric distribution failed unit-sum invariant")

    p_obs = next(p for x, p in probs if x == a)
    p_one_sided = sum((p for x, p in probs if x >= a), Fraction(0))
    p_two_sided = sum((p for _, p in probs if p <= p_obs), Fraction(0))
    return p_one_sided, p_two_sided


def _load_csv_checked(path: Path, expected_fields: list[str]) -> list[dict[str, str]]:
    if not path.is_file():
        raise RuntimeError(f"Missing required CSV file: {path}")
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != expected_fields:
            raise RuntimeError(f"{path.name}: header {reader.fieldnames} != {expected_fields}")
        return list(reader)


def _compute_majority(classes: tuple[str, str, str]) -> tuple[str, str]:
    counts = Counter(classes)
    top_label, top_count = counts.most_common(1)[0]
    maj = top_label if top_count >= 2 else "tie_or_disagreement"
    pf_maj = "true" if sum(1 for c in classes if c == "person_first") >= 2 else "false"
    if (pf_maj == "true") != (maj == "person_first"):
        raise RuntimeError(f"Majority consistency error for {classes!r}: maj={maj!r}, pf={pf_maj!r}")
    return maj, pf_maj


def load_and_verify_inputs() -> dict[str, Any]:
    """Load and assert all input schemas, alignment, SHA, and partition invariants."""
    codings_rows = _load_csv_checked(ETYMOLOGY_CODINGS_CSV_PATH, EXPECTED_CODINGS_FIELDS)
    key_rows = _load_csv_checked(WORD_CODING_KEY_CSV_PATH, EXPECTED_KEY_FIELDS)
    if not LEDGER_80_JSON_PATH.is_file():
        raise RuntimeError(f"Missing ledger_80.json at {LEDGER_80_JSON_PATH}")
    ledger = json.loads(LEDGER_80_JSON_PATH.read_text(encoding="utf-8"))

    if len(codings_rows) != EXPECTED_ITEM_COUNT or len(key_rows) != EXPECTED_ITEM_COUNT:
        raise RuntimeError(
            f"Expected {EXPECTED_ITEM_COUNT} rows in codings/key, got {len(codings_rows)} and {len(key_rows)}"
        )

    ledger_words = ledger.get("words")
    if not isinstance(ledger_words, list) or len(ledger_words) != 80:
        raise RuntimeError("ledger_80.json must contain exactly 80 words")
    ledger_by_word = {row["word"].strip(): row for row in ledger_words}
    if len(ledger_by_word) != 80:
        raise RuntimeError("Duplicate word in ledger_80.json")
    ledger_physics_expected = {
        w: row for w, row in ledger_by_word.items() if row["physics_stratum"] in ("core_law", "secondary_physics")
    }
    if len(ledger_physics_expected) != 35:
        raise RuntimeError(f"Expected 35 physics-eligible ledger words, got {len(ledger_physics_expected)}")

    joined_rows: list[dict[str, str]] = []
    seen_words: set[str] = set()
    for idx, (c_row, k_row) in enumerate(zip(codings_rows, key_rows), start=1):
        expected_id = f"W{idx:03d}"
        if c_row["item_id"] != expected_id or k_row["item_id"] != expected_id:
            raise RuntimeError(
                f"Row {idx} item_id mismatch: codings={c_row['item_id']!r}, key={k_row['item_id']!r}"
            )
        word = c_row["word"]
        if word != k_row["word"]:
            raise RuntimeError(f"{expected_id} word mismatch: {word!r} != {k_row['word']!r}")
        if not re.fullmatch(r"[a-z]+", word) or word in seen_words:
            raise RuntimeError(f"{expected_id} invalid or duplicate word: {word!r}")
        seen_words.add(word)

        if c_row["preregistration_commit_sha"] != PREREGISTRATION_COMMIT_SHA:
            raise RuntimeError(f"{expected_id}: codings preregistration_commit_sha mismatch")
        if k_row["preregistration_commit_sha"] != PREREGISTRATION_COMMIT_SHA:
            raise RuntimeError(f"{expected_id}: key preregistration_commit_sha mismatch")
        if c_row["source_coverage"] != SOURCE_COVERAGE:
            raise RuntimeError(f"{expected_id}: unexpected source_coverage={c_row['source_coverage']!r}")
        if (c_row["s1_model"], c_row["s2_model"], c_row["s3_model"]) != (
            "gemini_hydrogen",
            "opus_5_5",
            "gemini_carbon",
        ):
            raise RuntimeError(f"{expected_id}: unexpected session models")

        expected_s2_utc = VERIFIED_UTC_DATE if idx <= 3 else UNVERIFIED_UTC
        if c_row["s1_retrieved_utc"] != VERIFIED_UTC_DATE or c_row["s3_retrieved_utc"] != VERIFIED_UTC_DATE:
            raise RuntimeError(f"{expected_id}: unexpected s1/s3 UTC date")
        if c_row["s2_retrieved_utc"] != expected_s2_utc:
            raise RuntimeError(f"{expected_id}: s2_retrieved_utc {c_row['s2_retrieved_utc']!r} != {expected_s2_utc!r}")

        for col in ("s1_direction_class", "s2_direction_class", "s3_direction_class"):
            if c_row[col] not in VALID_DIRECTION_CLASSES:
                raise RuntimeError(f"{expected_id}: invalid {col}={c_row[col]!r}")
        maj, pf_maj = _compute_majority(
            (c_row["s1_direction_class"], c_row["s2_direction_class"], c_row["s3_direction_class"])
        )
        if c_row["direction_class_maj"] != maj or c_row["person_first_maj"] != pf_maj:
            raise RuntimeError(f"{expected_id}: majority mismatch on disk")

        for bool_col in ("in_targets_10", "in_controls_40", "in_ledger_physics_35"):
            if k_row[bool_col] not in ("true", "false"):
                raise RuntimeError(f"{expected_id}: invalid bool {bool_col}={k_row[bool_col]!r}")

        if k_row["in_ledger_physics_35"] == "true":
            l_row = ledger_physics_expected.get(word)
            if l_row is None:
                raise RuntimeError(f"{expected_id} ({word}) marked in_ledger_physics_35 but absent from ledger")
            if k_row["ledger_stratum"] != l_row["physics_stratum"] or k_row["ledger_kind"] != l_row["kind"]:
                raise RuntimeError(f"{expected_id} ({word}): key stratum/kind disagrees with ledger_80.json")
        else:
            if k_row["ledger_stratum"] or k_row["ledger_kind"]:
                raise RuntimeError(f"{expected_id} ({word}): unexpected non-empty ledger fields")

        if k_row["in_controls_40"] == "true" and not k_row["control_openstax_chapters"]:
            raise RuntimeError(f"{expected_id} ({word}): missing control_openstax_chapters")
        if k_row["in_controls_40"] == "false" and k_row["control_openstax_chapters"]:
            raise RuntimeError(f"{expected_id} ({word}): non-control has control_openstax_chapters")

        joined_rows.append(
            {
                "item_id": expected_id,
                "word": word,
                "in_targets_10": k_row["in_targets_10"],
                "in_controls_40": k_row["in_controls_40"],
                "in_ledger_physics_35": k_row["in_ledger_physics_35"],
                "ledger_stratum": k_row["ledger_stratum"],
                "ledger_kind": k_row["ledger_kind"],
                "control_openstax_chapters": k_row["control_openstax_chapters"],
                "s1_retrieved_utc": c_row["s1_retrieved_utc"],
                "s1_direction_class": c_row["s1_direction_class"],
                "s2_retrieved_utc": c_row["s2_retrieved_utc"],
                "s2_direction_class": c_row["s2_direction_class"],
                "s3_retrieved_utc": c_row["s3_retrieved_utc"],
                "s3_direction_class": c_row["s3_direction_class"],
                "direction_class_maj": c_row["direction_class_maj"],
                "person_first_maj": c_row["person_first_maj"],
                "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
                "part3_pre_unmasking_commit_sha": PART3_PRE_UNMASKING_COMMIT_SHA,
            }
        )

    targets_10_set = {r["word"] for r in joined_rows if r["in_targets_10"] == "true"}
    controls_40_set = {r["word"] for r in joined_rows if r["in_controls_40"] == "true"}
    ledger_35_set = {r["word"] for r in joined_rows if r["in_ledger_physics_35"] == "true"}

    if targets_10_set != set(TARGETS_10):
        raise RuntimeError(f"targets_10 mismatch: {sorted(targets_10_set)}")
    if len(controls_40_set) != 40:
        raise RuntimeError(f"Expected 40 controls, got {len(controls_40_set)}")
    if targets_10_set & controls_40_set:
        raise RuntimeError(f"targets_10 & controls_40 non-empty: {sorted(targets_10_set & controls_40_set)}")
    if ledger_35_set != set(ledger_physics_expected.keys()):
        raise RuntimeError("ledger_physics_35 set mismatch with ledger_80.json")
    if ledger_35_set & controls_40_set:
        raise RuntimeError(f"ledger_physics_35 & controls_40 non-empty: {sorted(ledger_35_set & controls_40_set)}")
    if set(ledger_by_word.keys()) & controls_40_set:
        raise RuntimeError("controls_40 overlaps ledger_80.json")
    if targets_10_set & ledger_35_set != set(EXPECTED_TARGETS_OVERLAP_LEDGER_35):
        raise RuntimeError("targets_10 & ledger_physics_35 overlap mismatch")
    if targets_10_set - ledger_35_set != set(EXPECTED_TARGET_ONLY):
        raise RuntimeError("target-only set mismatch")
    if (targets_10_set | controls_40_set | ledger_35_set) != seen_words:
        raise RuntimeError("Union of subsets does not equal 78 items")

    core_law_count = sum(1 for r in joined_rows if r["ledger_stratum"] == "core_law")
    sec_phys_count = sum(1 for r in joined_rows if r["ledger_stratum"] == "secondary_physics")
    if core_law_count != 21 or sec_phys_count != 14:
        raise RuntimeError(f"Expected 21 core_law + 14 secondary_physics, got {core_law_count} + {sec_phys_count}")

    return {
        "rows": joined_rows,
        "targets_10_words": sorted(targets_10_set),
        "controls_40_words": sorted(controls_40_set),
        "ledger_35_words": sorted(ledger_35_set),
    }


def render_item_table_bytes(rows: Sequence[dict[str, str]]) -> bytes:
    """Render deterministic 78-row part3_item_table.csv bytes in W001..W078 order."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=PART3_ITEM_TABLE_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue().encode("utf-8")


def _build_reliability_block(subset_rows: Sequence[dict[str, str]]) -> dict[str, Any]:
    """Compute 4-cat and binary Fleiss' kappa, ties, and all 3 pairwise Cohen's kappas."""
    ratings_4cat = [
        (r["s1_direction_class"], r["s2_direction_class"], r["s3_direction_class"])
        for r in subset_rows
    ]
    ratings_2cat = [
        tuple(_binarize_pf(v) for v in triple)
        for triple in ratings_4cat
    ]
    ties = [
        {
            "item_id": r["item_id"],
            "word": r["word"],
            "in_targets_10": r["in_targets_10"] == "true",
            "in_controls_40": r["in_controls_40"] == "true",
            "in_ledger_physics_35": r["in_ledger_physics_35"] == "true",
            "s1": r["s1_direction_class"],
            "s2": r["s2_direction_class"],
            "s3": r["s3_direction_class"],
        }
        for r in subset_rows
        if r["direction_class_maj"] == "tie_or_disagreement"
    ]

    pairwise_specs = (
        ("s1_vs_s3", "within_gemini_family", "s1_direction_class", "s3_direction_class"),
        ("s1_vs_s2", "cross_family_gemini_vs_anthropic", "s1_direction_class", "s2_direction_class"),
        ("s3_vs_s2", "cross_family_gemini_vs_anthropic", "s3_direction_class", "s2_direction_class"),
    )
    pairwise: dict[str, Any] = {}
    for key, relation, col_a, col_b in pairwise_specs:
        xs = [r[col_a] for r in subset_rows]
        ys = [r[col_b] for r in subset_rows]
        pairwise[key] = {
            "relation": relation,
            "four_category": cohen_kappa_exact(xs, ys, VALID_DIRECTION_CLASSES),
            "binary_person_first": cohen_kappa_exact(
                [_binarize_pf(x) for x in xs],
                [_binarize_pf(y) for y in ys],
                BINARY_PF_CATEGORIES,
            ),
        }

    return {
        "n_items": len(subset_rows),
        "fleiss_kappa_4cat": fleiss_kappa_exact(ratings_4cat, VALID_DIRECTION_CLASSES),
        "fleiss_kappa_binary_person_first": fleiss_kappa_exact(ratings_2cat, BINARY_PF_CATEGORIES),
        "tie_or_disagreement_count": len(ties),
        "tie_or_disagreement_items": ties,
        "pairwise_cohen_kappa": pairwise,
    }


def _evaluate_fisher_rule(
    rule_key: str,
    description: str,
    predicate: Callable[[dict[str, str]], bool],
    targets_rows: Sequence[dict[str, str]],
    controls_rows: Sequence[dict[str, str]],
) -> dict[str, Any]:
    """Compute exact 2x2 counts, risk difference, one-sided and two-sided Fisher p."""
    t_words = sorted(r["word"] for r in targets_rows if predicate(r))
    c_words = sorted(r["word"] for r in controls_rows if predicate(r))
    a = len(t_words)
    b = len(targets_rows) - a
    c = len(c_words)
    d = len(controls_rows) - c

    p_one, p_two = fisher_exact_proportions(a, len(targets_rows), c, len(controls_rows))
    t_rate = Fraction(a, len(targets_rows))
    c_rate = Fraction(c, len(controls_rows))
    risk_diff = t_rate - c_rate

    return {
        "rule_name": rule_key,
        "description": description,
        "contingency_2x2": {
            "target_person_first": a,
            "target_not_person_first": b,
            "control_person_first": c,
            "control_not_person_first": d,
        },
        "target_person_first_count": a,
        "target_total": len(targets_rows),
        "target_person_first": frac_dict(t_rate),
        "control_person_first_count": c,
        "control_total": len(controls_rows),
        "control_person_first": frac_dict(c_rate),
        "risk_difference": frac_dict(risk_diff),
        "fisher_p_one_sided_upper": frac_dict(p_one),
        "fisher_p_two_sided_secondary": frac_dict(p_two),
        "p_lt_0_05": bool(p_one < Fraction(1, 20)),
        "target_person_first_words": t_words,
        "control_person_first_words": c_words,
    }


def _direction_distribution(subset_rows: Sequence[dict[str, str]]) -> dict[str, Any]:
    maj_counts = Counter(r["direction_class_maj"] for r in subset_rows)
    s1_counts = Counter(r["s1_direction_class"] for r in subset_rows)
    s2_counts = Counter(r["s2_direction_class"] for r in subset_rows)
    s3_counts = Counter(r["s3_direction_class"] for r in subset_rows)
    return {
        "n_items": len(subset_rows),
        "maj_3run": {cat: maj_counts.get(cat, 0) for cat in VALID_DIRECTION_MAJ_CLASSES},
        "s1_gemini_hydrogen": {cat: s1_counts.get(cat, 0) for cat in VALID_DIRECTION_CLASSES},
        "s2_opus_5_5": {cat: s2_counts.get(cat, 0) for cat in VALID_DIRECTION_CLASSES},
        "s3_gemini_carbon": {cat: s3_counts.get(cat, 0) for cat in VALID_DIRECTION_CLASSES},
    }


def build_target_vs_control_section(rows: Sequence[dict[str, str]]) -> dict[str, Any]:
    """Compute all 9 Fisher rules, 4-cat distributions, and complete target/control arrays."""
    targets_rows = [r for r in rows if r["in_targets_10"] == "true"]
    controls_rows = [r for r in rows if r["in_controls_40"] == "true"]
    if len(targets_rows) != 10 or len(controls_rows) != 40:
        raise RuntimeError("Unexpected target/control counts")

    rule_specs: tuple[tuple[str, str, Callable[[dict[str, str]], bool]], ...] = (
        (
            "maj_3run",
            "3-run strict majority (direction_class_maj == 'person_first'; Gemini holds 2/3 votes)",
            lambda r: r["direction_class_maj"] == "person_first",
        ),
        (
            "s1_gemini_hydrogen",
            "Session 1 only (gemini_hydrogen, 78/78 retrieved 2026-11-14)",
            lambda r: r["s1_direction_class"] == "person_first",
        ),
        (
            "s2_opus_5_5_memory_75_of_78",
            "Session 2 only (opus_5_5; W001..W003 live, W004..W078 memory unverified)",
            lambda r: r["s2_direction_class"] == "person_first",
        ),
        (
            "s3_gemini_carbon",
            "Session 3 only (gemini_carbon, 78/78 retrieved 2026-11-14)",
            lambda r: r["s3_direction_class"] == "person_first",
        ),
        (
            "cross_family_strict_s1_and_s2",
            "Cross-family strict conjunction: s1 (gemini_hydrogen) == 'person_first' AND s2 (opus_5_5) == 'person_first'",
            lambda r: r["s1_direction_class"] == "person_first" and r["s2_direction_class"] == "person_first",
        ),
        (
            "cross_family_strict_s3_and_s2",
            "Cross-family strict conjunction: s3 (gemini_carbon) == 'person_first' AND s2 (opus_5_5) == 'person_first'",
            lambda r: r["s3_direction_class"] == "person_first" and r["s2_direction_class"] == "person_first",
        ),
        (
            "cross_family_lenient_s1_or_s2",
            "Cross-family lenient disjunction: s1 (gemini_hydrogen) == 'person_first' OR s2 (opus_5_5) == 'person_first'",
            lambda r: r["s1_direction_class"] == "person_first" or r["s2_direction_class"] == "person_first",
        ),
        (
            "cross_family_lenient_s3_or_s2",
            "Cross-family lenient disjunction: s3 (gemini_carbon) == 'person_first' OR s2 (opus_5_5) == 'person_first'",
            lambda r: r["s3_direction_class"] == "person_first" or r["s2_direction_class"] == "person_first",
        ),
        (
            "unanimous_all_3",
            "Unanimous all 3 sessions (s1 == s2 == s3 == 'person_first')",
            lambda r: (
                r["s1_direction_class"]
                == r["s2_direction_class"]
                == r["s3_direction_class"]
                == "person_first"
            ),
        ),
    )

    fisher_9_rules = {
        key: _evaluate_fisher_rule(key, desc, pred, targets_rows, controls_rows)
        for key, desc, pred in rule_specs
    }

    targets_per_word = [
        {
            "item_id": r["item_id"],
            "word": r["word"],
            "s1_direction_class": r["s1_direction_class"],
            "s2_direction_class": r["s2_direction_class"],
            "s3_direction_class": r["s3_direction_class"],
            "direction_class_maj": r["direction_class_maj"],
            "person_first_maj": r["person_first_maj"] == "true",
            "s1_retrieved_utc": r["s1_retrieved_utc"],
            "s2_retrieved_utc": r["s2_retrieved_utc"],
            "s3_retrieved_utc": r["s3_retrieved_utc"],
            "in_ledger_physics_35": r["in_ledger_physics_35"] == "true",
            "ledger_stratum": r["ledger_stratum"] or None,
            "ledger_kind": r["ledger_kind"] or None,
        }
        for r in targets_rows
    ]

    controls_per_word = [
        {
            "item_id": r["item_id"],
            "word": r["word"],
            "control_openstax_chapters": r["control_openstax_chapters"].split(";"),
            "s1_direction_class": r["s1_direction_class"],
            "s2_direction_class": r["s2_direction_class"],
            "s3_direction_class": r["s3_direction_class"],
            "direction_class_maj": r["direction_class_maj"],
            "person_first_maj": r["person_first_maj"] == "true",
            "s1_retrieved_utc": r["s1_retrieved_utc"],
            "s2_retrieved_utc": r["s2_retrieved_utc"],
            "s3_retrieved_utc": r["s3_retrieved_utc"],
        }
        for r in controls_rows
    ]

    return {
        "primary_rule": "maj_3run",
        "preregistered_alpha": frac_dict(Fraction(1, 20)),
        "any_rule_p_lt_0_05": any(v["p_lt_0_05"] for v in fisher_9_rules.values()),
        "fisher_exact_tests_9_rules": fisher_9_rules,
        "direction_class_distributions": {
            "targets_10": _direction_distribution(targets_rows),
            "controls_40": _direction_distribution(controls_rows),
        },
        "targets_10_per_word": targets_per_word,
        "controls_40_per_word": controls_per_word,
    }


def _binary_ledger_comparison(
    sub_rows: Sequence[dict[str, str]],
    positive_kinds: frozenset[str],
) -> dict[str, Any]:
    """Compare coded person_first (maj_3run and s1..s3) vs binary ledger_kind target."""
    ref_bools = ["true" if r["ledger_kind"] in positive_kinds else "false" for r in sub_rows]
    ref_words = sorted(r["word"] for r in sub_rows if r["ledger_kind"] in positive_kinds)

    raters: tuple[tuple[str, Callable[[dict[str, str]], str]], ...] = (
        ("maj_3run", lambda r: r["person_first_maj"]),
        ("s1_gemini_hydrogen", lambda r: "true" if r["s1_direction_class"] == "person_first" else "false"),
        ("s2_opus_5_5", lambda r: "true" if r["s2_direction_class"] == "person_first" else "false"),
        ("s3_gemini_carbon", lambda r: "true" if r["s3_direction_class"] == "person_first" else "false"),
    )

    by_rater: dict[str, Any] = {}
    for rater_key, pred_fn in raters:
        coded_bools = [pred_fn(r) for r in sub_rows]
        ck = cohen_kappa_exact(coded_bools, ref_bools, BINARY_BOOL_CATEGORIES)
        tp_words = sorted(
            r["word"] for r, c_val, l_val in zip(sub_rows, coded_bools, ref_bools) if c_val == "true" and l_val == "true"
        )
        fp_words = sorted(
            r["word"] for r, c_val, l_val in zip(sub_rows, coded_bools, ref_bools) if c_val == "true" and l_val == "false"
        )
        fn_words = sorted(
            r["word"] for r, c_val, l_val in zip(sub_rows, coded_bools, ref_bools) if c_val == "false" and l_val == "true"
        )
        tn_count = sum(1 for c_val, l_val in zip(coded_bools, ref_bools) if c_val == "false" and l_val == "false")
        by_rater[rater_key] = {
            "coded_positive_count": len(tp_words) + len(fp_words),
            "coded_positive_words": sorted(tp_words + fp_words),
            "tp": len(tp_words),
            "fp": len(fp_words),
            "fn": len(fn_words),
            "tn": tn_count,
            "tp_words": tp_words,
            "fp_words": fp_words,
            "fn_words": fn_words,
            **ck,
        }

    return {
        "n_items": len(sub_rows),
        "ledger_positive_count": len(ref_words),
        "ledger_positive_words": ref_words,
        "by_rater": by_rater,
    }


def _crosstab_maj_vs_ledger(sub_rows: Sequence[dict[str, str]]) -> dict[str, Any]:
    """Compute 4x8 matrix, tie_or_disagreement row, and combined 5x8 cross-tabulation."""
    full_5x8 = confusion_matrix_dict(
        [r["direction_class_maj"] for r in sub_rows],
        [r["ledger_kind"] for r in sub_rows],
        VALID_DIRECTION_MAJ_CLASSES,
        LEDGER_KINDS_35_ORDER,
    )
    matrix_4x8 = {cat: full_5x8[cat] for cat in VALID_DIRECTION_CLASSES}
    tie_row = full_5x8["tie_or_disagreement"]
    row_totals = {cat: sum(full_5x8[cat].values()) for cat in VALID_DIRECTION_MAJ_CLASSES}
    col_totals = {
        kind: sum(full_5x8[cat][kind] for cat in VALID_DIRECTION_MAJ_CLASSES)
        for kind in LEDGER_KINDS_35_ORDER
    }
    words_by_cell: dict[str, dict[str, list[str]]] = {
        cat: {kind: [] for kind in LEDGER_KINDS_35_ORDER}
        for cat in VALID_DIRECTION_MAJ_CLASSES
    }
    for r in sub_rows:
        words_by_cell[r["direction_class_maj"]][r["ledger_kind"]].append(r["word"])
    for cat in VALID_DIRECTION_MAJ_CLASSES:
        for kind in LEDGER_KINDS_35_ORDER:
            words_by_cell[cat][kind].sort()

    return {
        "n_items": len(sub_rows),
        "row_categories_4": list(VALID_DIRECTION_CLASSES),
        "tie_row_category": "tie_or_disagreement",
        "col_categories_8": list(LEDGER_KINDS_35_ORDER),
        "matrix_4x8": matrix_4x8,
        "tie_or_disagreement_row": tie_row,
        "matrix_5x8_with_tie_row": full_5x8,
        "row_totals": row_totals,
        "col_totals": col_totals,
        "words_by_cell": words_by_cell,
    }


def build_ledger_agreement_section(rows: Sequence[dict[str, str]]) -> dict[str, Any]:
    """Compute descriptive agreement on n = 35 ledger_physics_35 (overall + stratum split)."""
    l35_rows = [r for r in rows if r["in_ledger_physics_35"] == "true"]
    core_rows = [r for r in l35_rows if r["ledger_stratum"] == "core_law"]
    sec_rows = [r for r in l35_rows if r["ledger_stratum"] == "secondary_physics"]
    if len(l35_rows) != 35 or len(core_rows) != 21 or len(sec_rows) != 14:
        raise RuntimeError("Unexpected ledger_physics_35 counts")

    splits = (
        ("all_35", l35_rows),
        ("core_law_21", core_rows),
        ("secondary_physics_14", sec_rows),
    )

    inward_only = {
        name: _binary_ledger_comparison(sub, frozenset({"inward first"}))
        for name, sub in splits
    }
    inward_or_either = {
        name: _binary_ledger_comparison(sub, frozenset({"inward first", "either side"}))
        for name, sub in splits
    }

    per_word = [
        {
            "item_id": r["item_id"],
            "word": r["word"],
            "ledger_stratum": r["ledger_stratum"],
            "ledger_kind": r["ledger_kind"],
            "in_targets_10": r["in_targets_10"] == "true",
            "s1_direction_class": r["s1_direction_class"],
            "s2_direction_class": r["s2_direction_class"],
            "s3_direction_class": r["s3_direction_class"],
            "direction_class_maj": r["direction_class_maj"],
            "person_first_maj": r["person_first_maj"] == "true",
            "s2_retrieved_utc": r["s2_retrieved_utc"],
            "ledger_is_inward_first": r["ledger_kind"] == "inward first",
            "ledger_is_inward_or_either_side": r["ledger_kind"] in ("inward first", "either side"),
        }
        for r in l35_rows
    ]

    return {
        "inferential_status": "DESCRIPTIVE_LEDGER_AGREEMENT_NOT_CONFIRMATORY",
        "n_items": 35,
        "core_law_count": 21,
        "secondary_physics_count": 14,
        "vs_inward_first": inward_only,
        "vs_inward_first_or_either_side": inward_or_either,
        "cross_tabulation_maj_3run_vs_ledger_kind": {
            "all_35": _crosstab_maj_vs_ledger(l35_rows),
            "core_law_21": _crosstab_maj_vs_ledger(core_rows),
            "secondary_physics_14": _crosstab_maj_vs_ledger(sec_rows),
        },
        "ledger_physics_35_per_word": per_word,
    }


def build_results_payload(data: dict[str, Any]) -> dict[str, Any]:
    """Assemble the complete part3_results.json payload."""
    rows: list[dict[str, str]] = data["rows"]
    primary_50_rows = [r for r in rows if r["in_targets_10"] == "true" or r["in_controls_40"] == "true"]
    ledger_35_rows = [r for r in rows if r["in_ledger_physics_35"] == "true"]

    return {
        "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
        "part3_pre_unmasking_commit_sha": PART3_PRE_UNMASKING_COMMIT_SHA,
        "attribution": ATTRIBUTION,
        "evaluation_status": EVALUATION_STATUS,
        "source_coverage": SOURCE_COVERAGE,
        "session_panel": {
            "preregistered_model_families_required": 3,
            "actual_model_families_represented": 2,
            "model_families": ["Gemini", "Anthropic"],
            "refused_models": ["grok_4_7"],
            "sessions": {
                "s1": {
                    "model": "gemini_hydrogen",
                    "family": "Gemini",
                    "items_coded": 78,
                    "live_verified_count": 78,
                    "unverified_memory_count": 0,
                    "retrieved_utc": VERIFIED_UTC_DATE,
                    "live_verified_items": "W001..W078",
                },
                "s2": {
                    "model": "opus_5_5",
                    "family": "Anthropic",
                    "items_coded": 78,
                    "live_verified_count": 3,
                    "live_verified_items": ["W001", "W002", "W003"],
                    "unverified_memory_count": 75,
                    "unverified_memory_items": "W004..W078",
                    "unverified_in_targets_10_count": sum(
                        1 for r in rows if r["in_targets_10"] == "true" and r["s2_retrieved_utc"] == UNVERIFIED_UTC
                    ),
                    "unverified_in_controls_40_count": sum(
                        1 for r in rows if r["in_controls_40"] == "true" and r["s2_retrieved_utc"] == UNVERIFIED_UTC
                    ),
                    "unverified_in_ledger_physics_35_count": sum(
                        1
                        for r in rows
                        if r["in_ledger_physics_35"] == "true" and r["s2_retrieved_utc"] == UNVERIFIED_UTC
                    ),
                    "retrieved_utc_summary": "2026-11-14 (W001..W003); unverified (W004..W078)",
                    "note": "Anti-bot blocking stopped live etymonline.com retrieval after W003; W004..W078 coded from parametric memory.",
                },
                "s3": {
                    "model": "gemini_carbon",
                    "family": "Gemini",
                    "items_coded": 78,
                    "live_verified_count": 78,
                    "unverified_memory_count": 0,
                    "retrieved_utc": VERIFIED_UTC_DATE,
                    "live_verified_items": "W001..W078",
                },
            },
        },
        "protocol_deviation_disclosure": PROTOCOL_DEVIATION_DISCLOSURE,
        "dataset_partition_invariants": {
            "total_items": EXPECTED_ITEM_COUNT,
            "targets_10_count": 10,
            "controls_40_count": 40,
            "primary_50_count": 50,
            "ledger_physics_35_count": 35,
            "ledger_core_law_count": 21,
            "ledger_secondary_physics_count": 14,
            "targets_and_ledger_physics_overlap_count": len(EXPECTED_TARGETS_OVERLAP_LEDGER_35),
            "targets_and_ledger_physics_overlap_words": list(EXPECTED_TARGETS_OVERLAP_LEDGER_35),
            "target_only_count": len(EXPECTED_TARGET_ONLY),
            "target_only_words": list(EXPECTED_TARGET_ONLY),
            "targets_and_controls_overlap_count": 0,
            "ledger_physics_and_controls_overlap_count": 0,
            "ledger_80_and_controls_overlap_count": 0,
            "targets_10_words": data["targets_10_words"],
            "controls_40_words": data["controls_40_words"],
        },
        "inter_session_reliability": {
            "all_78": _build_reliability_block(rows),
            "primary_50": _build_reliability_block(primary_50_rows),
            "ledger_physics_35": _build_reliability_block(ledger_35_rows),
        },
        "target_vs_control_primary_and_sensitivity": build_target_vs_control_section(rows),
        "descriptive_ledger_80_agreement": build_ledger_agreement_section(rows),
    }


def run(verify_offline: bool) -> dict[str, Any]:
    """Execute Part 3 evaluation and write or offline-verify CSV/JSON outputs and hygiene."""
    data = load_and_verify_inputs()
    item_table_bytes = render_item_table_bytes(data["rows"])
    results_payload = build_results_payload(data)
    results_text = json.dumps(results_payload, indent=2, ensure_ascii=False) + "\n"
    results_bytes = results_text.encode("utf-8")
    item_table_text = item_table_bytes.decode("utf-8")

    if verify_offline:
        for path, expected_bytes in (
            (ITEM_TABLE_CSV_PATH, item_table_bytes),
            (RESULTS_JSON_PATH, results_bytes),
        ):
            if not path.is_file():
                raise RuntimeError(f"Missing committed output file: {path}")
            if path.read_bytes() != expected_bytes:
                raise RuntimeError(f"Byte-for-byte mismatch on {path.name}")
    else:
        ITEM_TABLE_CSV_PATH.write_bytes(item_table_bytes)
        RESULTS_JSON_PATH.write_bytes(results_bytes)

    _check_hygiene(
        [
            (Path(__file__).name, Path(__file__).read_text(encoding="utf-8")),
            (ITEM_TABLE_CSV_PATH.name, item_table_text),
            (RESULTS_JSON_PATH.name, results_text),
        ]
    )

    fisher = results_payload["target_vs_control_primary_and_sensitivity"]["fisher_exact_tests_9_rules"]
    rel78 = results_payload["inter_session_reliability"]["all_78"]
    l35_inward = results_payload["descriptive_ledger_80_agreement"]["vs_inward_first"]["all_35"]["by_rater"]["maj_3run"]
    l35_either = results_payload["descriptive_ledger_80_agreement"]["vs_inward_first_or_either_side"]["all_35"]["by_rater"]["maj_3run"]

    return {
        "mode": "verify-offline" if verify_offline else "evaluate",
        "evaluation_status": EVALUATION_STATUS,
        "hygiene_passed": True,
        "item_table_bytes": len(item_table_bytes),
        "results_json_bytes": len(results_bytes),
        "maj_3run_target_person_first": fisher["maj_3run"]["target_person_first"]["fraction"],
        "maj_3run_control_person_first": fisher["maj_3run"]["control_person_first"]["fraction"],
        "maj_3run_fisher_p_one_sided": fisher["maj_3run"]["fisher_p_one_sided_upper"],
        "any_rule_p_lt_0_05": results_payload["target_vs_control_primary_and_sensitivity"]["any_rule_p_lt_0_05"],
        "all_78_fleiss_4cat": rel78["fleiss_kappa_4cat"]["kappa"],
        "all_78_fleiss_2cat": rel78["fleiss_kappa_binary_person_first"]["kappa"],
        "ledger_35_vs_inward_first_maj_acc": l35_inward["agreement_rate"],
        "ledger_35_vs_inward_first_maj_kappa": l35_inward["kappa"],
        "ledger_35_vs_inward_or_either_maj_acc": l35_either["agreement_rate"],
        "ledger_35_vs_inward_or_either_maj_kappa": l35_either["kappa"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate Part 3 etymology direction control post-unmasking."
    )
    parser.add_argument(
        "--verify-offline",
        action="store_true",
        help="Recompute part3_item_table.csv and part3_results.json in memory and assert byte-for-byte parity & hygiene.",
    )
    args = parser.parse_args(argv)
    summary = run(args.verify_offline)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
