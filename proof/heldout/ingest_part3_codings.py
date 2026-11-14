#!/usr/bin/env python3
"""
ingest_part3_codings.py — Validate Part 3 etymology session JSONs and emit etymology_codings.csv.

Reads ONLY proof/heldout/word_coding_packet.csv and proof/heldout/packets/part3_session_{1,2,3}.json.
Python 3.12+ standard library only (zero external packages).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PREREGISTRATION_COMMIT_SHA = "463ad9f93c8a276b1e0d9ee497198dfa2169d079"
EXPECTED_ITEM_COUNT = 78
SOURCE_COVERAGE = "single-source"
VERIFIED_UTC_DATE = "2026-11-14"
UNVERIFIED_UTC = "unverified"
MIXED_UTC_LABEL = "2026-11-14 (s1,s3); unverified (s2)"

HELDOUT_DIR = Path(__file__).resolve().parent
PACKETS_DIR = HELDOUT_DIR / "packets"
WORD_PACKET_CSV_PATH = HELDOUT_DIR / "word_coding_packet.csv"
ETYMOLOGY_CODINGS_CSV_PATH = HELDOUT_DIR / "etymology_codings.csv"

PACKET_FIELDS = ["item_id", "word"]

SESSION_SPECS = (
    ("s1", "gemini_hydrogen", PACKETS_DIR / "part3_session_1.json"),
    ("s2", "opus_5_5", PACKETS_DIR / "part3_session_2.json"),
    ("s3", "gemini_carbon", PACKETS_DIR / "part3_session_3.json"),
)

EXPECTED_JSON_KEYS = {
    "item_id",
    "word",
    "etymonline_url",
    "etymonline_retrieved_utc",
    "earliest_person_sense",
    "earliest_physics_sense",
    "direction_class",
}

VALID_DIRECTION_CLASSES = {
    "person_first",
    "physics_first",
    "both_from_start",
    "no_person_sense",
}

ETYMOLOGY_CODINGS_FIELDS = [
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

# Hex-encoded hygiene patterns so restricted/forbidden tokens never appear literally in this file.
_FORBIDDEN_SUBSTRINGS_HEX: tuple[str, ...] = (
    "776f72645f636f64696e675f6b6579",
    "6c65646765725f3830",
    "626c696e64",
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
)


def _decode_hex_list(hex_items: tuple[str, ...]) -> list[str]:
    return [bytes.fromhex(item).decode("utf-8") for item in hex_items]


def _load_packet_items() -> list[tuple[str, str]]:
    """Load and validate sequential items W001..W078 from proof/heldout/word_coding_packet.csv."""
    if not WORD_PACKET_CSV_PATH.is_file():
        raise RuntimeError(f"Missing word_coding_packet.csv at {WORD_PACKET_CSV_PATH}")
    items: list[tuple[str, str]] = []
    seen_words: set[str] = set()
    with WORD_PACKET_CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != PACKET_FIELDS:
            raise RuntimeError(
                f"Unexpected word_coding_packet.csv header: {reader.fieldnames} != {PACKET_FIELDS}"
            )
        for idx, row in enumerate(reader, start=1):
            expected_id = f"W{idx:03d}"
            item_id = row.get("item_id", "")
            word = row.get("word", "")
            if item_id != expected_id:
                raise RuntimeError(f"Expected item_id {expected_id!r} at index {idx}, got {item_id!r}")
            if not re.fullmatch(r"[a-z]+", word):
                raise RuntimeError(f"Unexpected non-lowercase ASCII word at {expected_id}: {word!r}")
            if word in seen_words:
                raise RuntimeError(f"Duplicate word in word_coding_packet.csv: {word!r}")
            seen_words.add(word)
            items.append((item_id, word))
    if len(items) != EXPECTED_ITEM_COUNT:
        raise RuntimeError(f"Expected {EXPECTED_ITEM_COUNT} items in word_coding_packet.csv, got {len(items)}")
    return items


def _validate_sense_tag(filename: str, item_id: str, field_name: str, value: object) -> str:
    """Enforce copyright/non-prose guard and length bounds on a coded sense tag."""
    if not isinstance(value, str):
        raise RuntimeError(f"{filename}: {item_id} {field_name} must be a string, got {type(value).__name__}")
    if '"' in value:
        raise RuntimeError(f"{filename}: {item_id} {field_name} contains forbidden double-quote character")
    if "\n" in value or "\r" in value:
        raise RuntimeError(f"{filename}: {item_id} {field_name} contains newline characters")
    stripped_len = len(value.strip())
    if not (1 <= stripped_len <= 80):
        raise RuntimeError(
            f"{filename}: {item_id} {field_name} stripped length {stripped_len} outside [1, 80]"
        )
    return " ".join(value.split())


def _load_and_validate_session(
    session_key: str,
    path: Path,
    packet_items: list[tuple[str, str]],
) -> tuple[str, list[dict[str, str]]]:
    """Read and validate one raw 78-item Part 3 session JSON array."""
    if not path.is_file():
        raise RuntimeError(f"Missing session JSON at {path}")
    raw_text = path.read_text(encoding="utf-8")
    data = json.loads(raw_text)
    if not isinstance(data, list):
        raise RuntimeError(f"{path.name}: top-level JSON must be a list, got {type(data).__name__}")
    if len(data) != len(packet_items):
        raise RuntimeError(f"{path.name}: expected {len(packet_items)} rows, got {len(data)}")

    validated: list[dict[str, str]] = []
    for idx, (row, (expected_id, expected_word)) in enumerate(zip(data, packet_items), start=1):
        if not isinstance(row, dict):
            raise RuntimeError(f"{path.name}: row {idx} must be a JSON object")
        actual_keys = set(row.keys())
        if actual_keys != EXPECTED_JSON_KEYS:
            raise RuntimeError(
                f"{path.name}: row {idx} keys {sorted(actual_keys)} != {sorted(EXPECTED_JSON_KEYS)}"
            )
        for key, val in row.items():
            if not isinstance(val, str):
                raise RuntimeError(f"{path.name}: {expected_id} field {key} must be str, got {type(val).__name__}")

        if row["item_id"] != expected_id:
            raise RuntimeError(f"{path.name}: row {idx} item_id {row['item_id']!r} != {expected_id!r}")
        if row["word"] != expected_word:
            raise RuntimeError(f"{path.name}: {expected_id} word {row['word']!r} != {expected_word!r}")

        expected_url = f"https://www.etymonline.com/word/{expected_word}"
        if row["etymonline_url"] != expected_url:
            raise RuntimeError(
                f"{path.name}: {expected_id} etymonline_url {row['etymonline_url']!r} != {expected_url!r}"
            )

        utc = row["etymonline_retrieved_utc"]
        if session_key in ("s1", "s3"):
            if utc != VERIFIED_UTC_DATE:
                raise RuntimeError(
                    f"{path.name}: {expected_id} expected etymonline_retrieved_utc={VERIFIED_UTC_DATE!r}, got {utc!r}"
                )
        elif session_key == "s2":
            expected_utc = VERIFIED_UTC_DATE if idx <= 3 else UNVERIFIED_UTC
            if utc != expected_utc:
                raise RuntimeError(
                    f"{path.name}: {expected_id} expected etymonline_retrieved_utc={expected_utc!r}, got {utc!r}"
                )
        else:
            raise RuntimeError(f"Unknown session_key {session_key!r}")

        direction_class = row["direction_class"]
        if direction_class not in VALID_DIRECTION_CLASSES:
            raise RuntimeError(f"{path.name}: {expected_id} invalid direction_class={direction_class!r}")

        person_sense = _validate_sense_tag(path.name, expected_id, "earliest_person_sense", row["earliest_person_sense"])
        physics_sense = _validate_sense_tag(
            path.name, expected_id, "earliest_physics_sense", row["earliest_physics_sense"]
        )

        validated.append(
            {
                "item_id": expected_id,
                "word": expected_word,
                "etymonline_url": expected_url,
                "etymonline_retrieved_utc": utc,
                "earliest_person_sense": person_sense,
                "earliest_physics_sense": physics_sense,
                "direction_class": direction_class,
            }
        )
    return raw_text, validated


def _compute_retrieved_utc(u1: str, u2: str, u3: str) -> str:
    if u1 != VERIFIED_UTC_DATE or u3 != VERIFIED_UTC_DATE or u2 not in (VERIFIED_UTC_DATE, UNVERIFIED_UTC):
        raise RuntimeError(f"Unexpected session retrieval dates: {(u1, u2, u3)!r}")
    if u1 == u2 == u3 == VERIFIED_UTC_DATE:
        return VERIFIED_UTC_DATE
    return MIXED_UTC_LABEL


def _compute_direction_majority(item_id: str, classes: tuple[str, str, str]) -> tuple[str, str]:
    counts = Counter(classes)
    top_label, top_count = counts.most_common(1)[0]
    direction_class_maj = top_label if top_count >= 2 else "tie_or_disagreement"
    person_first_maj = "true" if sum(1 for c in classes if c == "person_first") >= 2 else "false"
    if (person_first_maj == "true") != (direction_class_maj == "person_first"):
        raise RuntimeError(
            f"{item_id}: majority consistency failure for {classes!r}: "
            f"direction_class_maj={direction_class_maj!r}, person_first_maj={person_first_maj!r}"
        )
    return direction_class_maj, person_first_maj


def _render_codings_bytes(
    packet_items: list[tuple[str, str]],
    sessions: list[tuple[str, list[dict[str, str]]]],
) -> tuple[bytes, dict[str, Any]]:
    (m1, rows1), (m2, rows2), (m3, rows3) = sessions
    maj_counts: Counter[str] = Counter()
    pf_counts: Counter[str] = Counter()
    utc_counts: Counter[str] = Counter()
    s1_counts: Counter[str] = Counter()
    s2_counts: Counter[str] = Counter()
    s3_counts: Counter[str] = Counter()

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=ETYMOLOGY_CODINGS_FIELDS, lineterminator="\n")
    writer.writeheader()

    for (item_id, word), r1, r2, r3 in zip(packet_items, rows1, rows2, rows3):
        retrieved_utc = _compute_retrieved_utc(
            r1["etymonline_retrieved_utc"],
            r2["etymonline_retrieved_utc"],
            r3["etymonline_retrieved_utc"],
        )
        direction_maj, person_first_maj = _compute_direction_majority(
            item_id,
            (r1["direction_class"], r2["direction_class"], r3["direction_class"]),
        )

        maj_counts[direction_maj] += 1
        pf_counts[person_first_maj] += 1
        utc_counts[retrieved_utc] += 1
        s1_counts[r1["direction_class"]] += 1
        s2_counts[r2["direction_class"]] += 1
        s3_counts[r3["direction_class"]] += 1

        writer.writerow(
            {
                "item_id": item_id,
                "word": word,
                "etymonline_url": f"https://www.etymonline.com/word/{word}",
                "etymonline_retrieved_utc": retrieved_utc,
                "source_coverage": SOURCE_COVERAGE,
                "s1_model": m1,
                "s1_retrieved_utc": r1["etymonline_retrieved_utc"],
                "s1_earliest_person_sense": r1["earliest_person_sense"],
                "s1_earliest_physics_sense": r1["earliest_physics_sense"],
                "s1_direction_class": r1["direction_class"],
                "s2_model": m2,
                "s2_retrieved_utc": r2["etymonline_retrieved_utc"],
                "s2_earliest_person_sense": r2["earliest_person_sense"],
                "s2_earliest_physics_sense": r2["earliest_physics_sense"],
                "s2_direction_class": r2["direction_class"],
                "s3_model": m3,
                "s3_retrieved_utc": r3["etymonline_retrieved_utc"],
                "s3_earliest_person_sense": r3["earliest_person_sense"],
                "s3_earliest_physics_sense": r3["earliest_physics_sense"],
                "s3_direction_class": r3["direction_class"],
                "direction_class_maj": direction_maj,
                "person_first_maj": person_first_maj,
                "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
            }
        )

    summary = {
        "source_coverage": SOURCE_COVERAGE,
        "retrieved_utc_counts": dict(utc_counts),
        "direction_class_maj_counts": dict(maj_counts),
        "person_first_maj_counts": dict(pf_counts),
        "session_direction_counts": {
            m1: dict(s1_counts),
            m2: dict(s2_counts),
            m3: dict(s3_counts),
        },
    }
    return buf.getvalue().encode("utf-8"), summary


def _check_hygiene(named_texts: list[tuple[str, str]]) -> None:
    forbidden = _decode_hex_list(_FORBIDDEN_SUBSTRINGS_HEX)
    for label, text in named_texts:
        lowered = text.lower()
        for tok in forbidden:
            if tok.lower() in lowered:
                raise RuntimeError(
                    f"Hygiene check failed in {label}: forbidden token (hex {tok.encode('utf-8').hex()})"
                )


def run(verify_offline: bool) -> dict[str, Any]:
    packet_items = _load_packet_items()

    named_texts: list[tuple[str, str]] = [
        (Path(__file__).name, Path(__file__).read_text(encoding="utf-8")),
    ]
    sessions: list[tuple[str, list[dict[str, str]]]] = []
    for session_key, model_name, path in SESSION_SPECS:
        raw_text, rows = _load_and_validate_session(session_key, path, packet_items)
        named_texts.append((path.name, raw_text))
        sessions.append((model_name, rows))

    codings_bytes, summary = _render_codings_bytes(packet_items, sessions)
    codings_text = codings_bytes.decode("utf-8")
    named_texts.append((ETYMOLOGY_CODINGS_CSV_PATH.name, codings_text))
    _check_hygiene(named_texts)

    if verify_offline:
        if not ETYMOLOGY_CODINGS_CSV_PATH.is_file():
            raise RuntimeError(f"Missing output file on disk: {ETYMOLOGY_CODINGS_CSV_PATH}")
        disk_bytes = ETYMOLOGY_CODINGS_CSV_PATH.read_bytes()
        if disk_bytes != codings_bytes:
            raise RuntimeError(f"Byte-for-byte mismatch on {ETYMOLOGY_CODINGS_CSV_PATH.name}")
        _check_hygiene([(ETYMOLOGY_CODINGS_CSV_PATH.name, disk_bytes.decode("utf-8"))])
    else:
        ETYMOLOGY_CODINGS_CSV_PATH.write_bytes(codings_bytes)
        _check_hygiene(
            [(ETYMOLOGY_CODINGS_CSV_PATH.name, ETYMOLOGY_CODINGS_CSV_PATH.read_text(encoding="utf-8"))]
        )

    return {
        "mode": "verify-offline" if verify_offline else "build",
        "item_count": len(packet_items),
        "sessions": [m for _, m, _ in SESSION_SPECS],
        "etymology_codings_bytes": len(codings_bytes),
        "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
        "hygiene_passed": True,
        **summary,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Part 3 etymology session JSONs and generate/verify etymology_codings.csv."
    )
    parser.add_argument(
        "--verify-offline",
        action="store_true",
        help="Recompute etymology_codings.csv in memory and assert byte-for-byte parity and hygiene.",
    )
    args = parser.parse_args(argv)
    result = run(args.verify_offline)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
