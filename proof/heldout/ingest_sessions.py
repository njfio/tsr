#!/usr/bin/env python3
"""
ingest_sessions.py — Validate raw session JSONs and emit appliers.csv and labels.csv.

Reads ONLY proof/heldout/law_cards.csv and proof/heldout/packets/session_*.json.
Python 3.12+ standard library only (zero external packages).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PREREGISTRATION_COMMIT_SHA = "463ad9f93c8a276b1e0d9ee497198dfa2169d079"
AMENDMENT_1_COMMIT_SHA = "b66f48efb76e0f8d17d7db32848ad95f0a5c8633"
EXPECTED_CARD_COUNT = 65

HELDOUT_DIR = Path(__file__).resolve().parent
PACKETS_DIR = HELDOUT_DIR / "packets"
LAW_CARDS_CSV_PATH = HELDOUT_DIR / "law_cards.csv"
APPLIERS_CSV_PATH = HELDOUT_DIR / "appliers.csv"
LABELS_CSV_PATH = HELDOUT_DIR / "labels.csv"

LAW_CARDS_FIELDS = [
    "card_id",
    "what_it_says",
    "quantities_related",
    "conditions_to_hold",
    "preregistration_commit_sha",
]

SESSION_SPECS = (
    ("s1", "gemini_carbon", PACKETS_DIR / "session_1.json"),
    ("s2", "grok_4_7", PACKETS_DIR / "session_2.json"),
    ("s3", "kimi_k3", PACKETS_DIR / "session_3.json"),
)
EXTRA_SESSION_SPEC = ("extra", "gemini_hydrogen", PACKETS_DIR / "session_extra_gemini_hydrogen.json")

EXPECTED_JSON_KEYS = {"card_id", "q1", "q2", "q3", "q4", "ruling", "rationale"}
VALID_BINARY_ANSWERS = {"Yes", "No"}
VALID_RULINGS = {"Keep", "Invert", "the rule doesn't say"}

APPLIERS_FIELDS = [
    "card_id",
    "b1_model_family",
    "b2_model_family",
    "b3_model_family",
    "b1_ruling",
    "b1_rationale",
    "b2_ruling",
    "b2_rationale",
    "b3_ruling",
    "b3_rationale",
    "b_maj_ruling",
    "preregistration_commit_sha",
    "amendment_1_commit_sha",
]

LABELS_FIELDS = [
    "card_id",
    "c1_model_family",
    "c2_model_family",
    "c3_model_family",
    "c1_q1",
    "c1_q2",
    "c1_q3",
    "c1_q4",
    "c2_q1",
    "c2_q2",
    "c2_q3",
    "c2_q4",
    "c3_q1",
    "c3_q2",
    "c3_q3",
    "c3_q4",
    "q1_maj",
    "q2_maj",
    "q3_maj",
    "q4_maj",
    "pred_ch2",
    "pred_ch16",
    "pred_naive_mass",
    "preregistration_commit_sha",
    "amendment_1_commit_sha",
]

# Hex-encoded hygiene patterns so restricted/forbidden tokens never appear literally in this file.
_FORBIDDEN_SUBSTRINGS_HEX = [
    "73616d706c655f6d616e6966657374",
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


def _decode_hex_list(hex_items: list[str]) -> list[str]:
    return [bytes.fromhex(item).decode("utf-8") for item in hex_items]


def _load_card_ids() -> list[str]:
    """Load and validate sequential card IDs C001..C065 from proof/heldout/law_cards.csv."""
    if not LAW_CARDS_CSV_PATH.exists():
        raise RuntimeError(f"Missing law_cards.csv at {LAW_CARDS_CSV_PATH}")
    card_ids: list[str] = []
    with LAW_CARDS_CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != LAW_CARDS_FIELDS:
            raise RuntimeError(f"Unexpected law_cards.csv header: {reader.fieldnames} != {LAW_CARDS_FIELDS}")
        for idx, row in enumerate(reader, start=1):
            if row["preregistration_commit_sha"] != PREREGISTRATION_COMMIT_SHA:
                raise RuntimeError(f"law_cards.csv SHA mismatch on row {idx}")
            expected_id = f"C{idx:03d}"
            if row["card_id"] != expected_id:
                raise RuntimeError(f"Expected card_id {expected_id!r} at index {idx}, got {row['card_id']!r}")
            card_ids.append(row["card_id"])
    if len(card_ids) != EXPECTED_CARD_COUNT:
        raise RuntimeError(f"Expected {EXPECTED_CARD_COUNT} cards in law_cards.csv, got {len(card_ids)}")
    return card_ids


def _load_and_validate_session(path: Path, expected_card_ids: list[str]) -> tuple[str, list[dict[str, str]]]:
    """Read and validate one raw 65-card session JSON array."""
    if not path.exists():
        raise RuntimeError(f"Missing session JSON at {path}")
    raw_text = path.read_text(encoding="utf-8")
    data = json.loads(raw_text)
    if not isinstance(data, list):
        raise RuntimeError(f"{path.name}: top-level JSON must be a list, got {type(data).__name__}")
    if len(data) != len(expected_card_ids):
        raise RuntimeError(f"{path.name}: expected {len(expected_card_ids)} rows, got {len(data)}")

    validated: list[dict[str, str]] = []
    for idx, (row, expected_id) in enumerate(zip(data, expected_card_ids), start=1):
        if not isinstance(row, dict):
            raise RuntimeError(f"{path.name}: row {idx} must be a JSON object")
        actual_keys = set(row.keys())
        if actual_keys != EXPECTED_JSON_KEYS:
            raise RuntimeError(
                f"{path.name}: row {idx} keys {sorted(actual_keys)} != {sorted(EXPECTED_JSON_KEYS)}"
            )
        if row["card_id"] != expected_id:
            raise RuntimeError(f"{path.name}: row {idx} card_id {row['card_id']!r} != {expected_id!r}")
        for q_key in ("q1", "q2", "q3", "q4"):
            if row[q_key] not in VALID_BINARY_ANSWERS:
                raise RuntimeError(f"{path.name}: {expected_id} invalid {q_key}={row[q_key]!r}")
        if row["ruling"] not in VALID_RULINGS:
            raise RuntimeError(f"{path.name}: {expected_id} invalid ruling={row['ruling']!r}")
        rationale = row["rationale"]
        if not isinstance(rationale, str) or " ".join(rationale.split()) == "":
            raise RuntimeError(f"{path.name}: {expected_id} rationale must be a non-empty string")
        validated.append(
            {
                "card_id": row["card_id"],
                "q1": row["q1"],
                "q2": row["q2"],
                "q3": row["q3"],
                "q4": row["q4"],
                "ruling": row["ruling"],
                "rationale": " ".join(rationale.split()),
            }
        )
    return raw_text, validated


def _compute_majority_ruling(rulings: tuple[str, str, str]) -> str:
    counts = Counter(rulings)
    for ruling, count in counts.items():
        if count >= 2:
            return ruling
    return "no_majority"


def _compute_majority_binary(answers: tuple[str, str, str]) -> str:
    return "Yes" if sum(1 for ans in answers if ans == "Yes") >= 2 else "No"


def _render_appliers_bytes(
    card_ids: list[str],
    sessions: list[tuple[str, list[dict[str, str]]]],
) -> tuple[bytes, Counter[str]]:
    (m1, rows1), (m2, rows2), (m3, rows3) = sessions
    maj_counts: Counter[str] = Counter()
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=APPLIERS_FIELDS, lineterminator="\n")
    writer.writeheader()
    for card_id, r1, r2, r3 in zip(card_ids, rows1, rows2, rows3):
        b_maj = _compute_majority_ruling((r1["ruling"], r2["ruling"], r3["ruling"]))
        maj_counts[b_maj] += 1
        writer.writerow(
            {
                "card_id": card_id,
                "b1_model_family": m1,
                "b2_model_family": m2,
                "b3_model_family": m3,
                "b1_ruling": r1["ruling"],
                "b1_rationale": r1["rationale"],
                "b2_ruling": r2["ruling"],
                "b2_rationale": r2["rationale"],
                "b3_ruling": r3["ruling"],
                "b3_rationale": r3["rationale"],
                "b_maj_ruling": b_maj,
                "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
                "amendment_1_commit_sha": AMENDMENT_1_COMMIT_SHA,
            }
        )
    return buf.getvalue().encode("utf-8"), maj_counts


def _render_labels_bytes(
    card_ids: list[str],
    sessions: list[tuple[str, list[dict[str, str]]]],
) -> tuple[bytes, dict[str, Any]]:
    (m1, rows1), (m2, rows2), (m3, rows3) = sessions
    q_yes_counts: Counter[str] = Counter()
    pred_ch2_counts: Counter[str] = Counter()
    pred_ch16_counts: Counter[str] = Counter()
    pred_naive_mass_counts: Counter[str] = Counter()

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=LABELS_FIELDS, lineterminator="\n")
    writer.writeheader()
    for card_id, r1, r2, r3 in zip(card_ids, rows1, rows2, rows3):
        q1_maj = _compute_majority_binary((r1["q1"], r2["q1"], r3["q1"]))
        q2_maj = _compute_majority_binary((r1["q2"], r2["q2"], r3["q2"]))
        q3_maj = _compute_majority_binary((r1["q3"], r2["q3"], r3["q3"]))
        q4_maj = _compute_majority_binary((r1["q4"], r2["q4"], r3["q4"]))

        for q_name, q_val in (("q1_maj", q1_maj), ("q2_maj", q2_maj), ("q3_maj", q3_maj), ("q4_maj", q4_maj)):
            if q_val == "Yes":
                q_yes_counts[q_name] += 1

        q1 = q1_maj == "Yes"
        q2 = q2_maj == "Yes"
        q3 = q3_maj == "Yes"
        q4 = q4_maj == "Yes"

        pred_ch2 = "Keep" if (q1 or (not q2 and not q3)) else "Invert"
        pred_ch16 = "Keep" if (q1 or q4 or (not q2 and not q3)) else "Invert"
        pred_naive_mass = "Invert" if q2 else "Keep"

        pred_ch2_counts[pred_ch2] += 1
        pred_ch16_counts[pred_ch16] += 1
        pred_naive_mass_counts[pred_naive_mass] += 1

        writer.writerow(
            {
                "card_id": card_id,
                "c1_model_family": m1,
                "c2_model_family": m2,
                "c3_model_family": m3,
                "c1_q1": r1["q1"],
                "c1_q2": r1["q2"],
                "c1_q3": r1["q3"],
                "c1_q4": r1["q4"],
                "c2_q1": r2["q1"],
                "c2_q2": r2["q2"],
                "c2_q3": r2["q3"],
                "c2_q4": r2["q4"],
                "c3_q1": r3["q1"],
                "c3_q2": r3["q2"],
                "c3_q3": r3["q3"],
                "c3_q4": r3["q4"],
                "q1_maj": q1_maj,
                "q2_maj": q2_maj,
                "q3_maj": q3_maj,
                "q4_maj": q4_maj,
                "pred_ch2": pred_ch2,
                "pred_ch16": pred_ch16,
                "pred_naive_mass": pred_naive_mass,
                "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
                "amendment_1_commit_sha": AMENDMENT_1_COMMIT_SHA,
            }
        )

    summary = {
        "q_maj_yes_counts": {k: q_yes_counts[k] for k in ("q1_maj", "q2_maj", "q3_maj", "q4_maj")},
        "pred_ch2_counts": dict(pred_ch2_counts),
        "pred_ch16_counts": dict(pred_ch16_counts),
        "pred_naive_mass_counts": dict(pred_naive_mass_counts),
    }
    return buf.getvalue().encode("utf-8"), summary


def _check_hygiene(named_texts: list[tuple[str, str]]) -> None:
    forbidden = _decode_hex_list(_FORBIDDEN_SUBSTRINGS_HEX)
    for label, text in named_texts:
        lowered = text.lower()
        for tok in forbidden:
            if tok.lower() in lowered:
                raise RuntimeError(f"Forbidden token {tok!r} found in {label}")


def run(verify_offline: bool) -> dict[str, Any]:
    card_ids = _load_card_ids()

    named_texts: list[tuple[str, str]] = [
        (Path(__file__).name, Path(__file__).read_text(encoding="utf-8")),
    ]
    primary_sessions: list[tuple[str, list[dict[str, str]]]] = []
    for _, model_family, path in SESSION_SPECS:
        raw_text, rows = _load_and_validate_session(path, card_ids)
        named_texts.append((path.name, raw_text))
        primary_sessions.append((model_family, rows))

    _, _, extra_path = EXTRA_SESSION_SPEC
    extra_raw_text, _ = _load_and_validate_session(extra_path, card_ids)
    named_texts.append((extra_path.name, extra_raw_text))

    appliers_bytes, maj_ruling_counts = _render_appliers_bytes(card_ids, primary_sessions)
    labels_bytes, labels_summary = _render_labels_bytes(card_ids, primary_sessions)

    named_texts.append((APPLIERS_CSV_PATH.name, appliers_bytes.decode("utf-8")))
    named_texts.append((LABELS_CSV_PATH.name, labels_bytes.decode("utf-8")))
    _check_hygiene(named_texts)

    if verify_offline:
        for path, expected_bytes in (
            (APPLIERS_CSV_PATH, appliers_bytes),
            (LABELS_CSV_PATH, labels_bytes),
        ):
            if not path.exists():
                raise RuntimeError(f"Missing output file on disk: {path}")
            if path.read_bytes() != expected_bytes:
                raise RuntimeError(f"Byte-for-byte mismatch on {path.name}")
    else:
        APPLIERS_CSV_PATH.write_bytes(appliers_bytes)
        LABELS_CSV_PATH.write_bytes(labels_bytes)

    return {
        "mode": "verify-offline" if verify_offline else "build",
        "card_count": len(card_ids),
        "primary_sessions": [m for _, m, _ in SESSION_SPECS],
        "extra_session_validated": EXTRA_SESSION_SPEC[1],
        "appliers_bytes": len(appliers_bytes),
        "labels_bytes": len(labels_bytes),
        "b_maj_ruling_counts": dict(maj_ruling_counts),
        **labels_summary,
        "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
        "amendment_1_commit_sha": AMENDMENT_1_COMMIT_SHA,
        "hygiene_passed": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate raw session JSONs and generate/verify appliers.csv and labels.csv."
    )
    parser.add_argument(
        "--verify-offline",
        action="store_true",
        help="Re-render appliers.csv and labels.csv in memory and assert byte-for-byte parity and hygiene.",
    )
    args = parser.parse_args()
    result = run(args.verify_offline)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
