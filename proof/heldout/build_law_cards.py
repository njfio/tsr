#!/usr/bin/env python3
"""
build_law_cards.py — Stage 0 plain-language law card validator and deterministic serializer.

Python 3.12+ standard library only (zero external packages).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path
from typing import Any

PREREGISTRATION_COMMIT_SHA = "463ad9f93c8a276b1e0d9ee497198dfa2169d079"
DEFAULT_EXPECTED_COUNT = 65
DEFAULT_INPUT_REL = "packets/stage0_card_writer_output.json"

HELDOUT_DIR = Path(__file__).resolve().parent
LAW_CARDS_CSV_PATH = HELDOUT_DIR / "law_cards.csv"
LAW_CARDS_MD_PATH = HELDOUT_DIR / "law_cards.md"

CARD_KEYS = ("card_id", "what_it_says", "quantities_related", "conditions_to_hold")
CSV_FIELDS = list(CARD_KEYS) + ["preregistration_commit_sha"]

# Hex-encoded restricted tokens so this validator script embeds zero forbidden strings literally.
_CI_WORD_TOKENS_HEX = [
    "76696272616e6365",
    "617070726563696174696f6e",
    "706f696e74206f66207265666c656374696f6e",
    "706f696e74206f662061747472616374696f6e",
    "736f7665726569676e",
    "6e6f6e706879736963616c",
    "7265636570746976697479",
    "726563657074697665",
    "6b656570",
    "696e76657274",
    "747372",
    "74686520736f7665726569676e206d6972726f72",
    "776861742074686520776f726473206b6e6577",
    "63757272656e74206f6620636f6e7363696f75736e657373",
    "6e6f6e706879736963616c206d6f76656d656e74",
    "657870616e73696f6e2064696c6174696f6e",
    "657465726e616c2d656e657267657469632d656e74697479",
    "636f6e7363696f75732d706879736963616c",
    "636f6e7363696f757320656e65726779",
    "766962726174696f6e616c207265616c697479",
    "7375626a656374697665207265616c697479",
    "636f6c6c656374697665207265616c697479",
    "6f70656e73746178",
    "756e69766572736974792070687973696373",
    "62656e63686d61726b726f77733137",
    "62656e63686d61726b5f3137",
    "626c696e64",
]

_CS_WORD_TOKENS_HEX = [
    "4d6f76656d656e74",
    "43757272656e74",
    "566f72746578",
    "436f6e76657267656e6365",
]

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
]


def _decode_hex_list(hex_items: list[str]) -> list[str]:
    return [bytes.fromhex(item).decode("utf-8") for item in hex_items]


def _resolve_input_path(input_arg: str) -> Path:
    candidate = Path(input_arg)
    if candidate.is_absolute():
        return candidate
    rel_to_heldout = HELDOUT_DIR / candidate
    if rel_to_heldout.exists():
        return rel_to_heldout
    if candidate.exists():
        return candidate.resolve()
    return rel_to_heldout


def _validate_cards(raw_data: Any, expected_count: int) -> list[dict[str, str]]:
    if expected_count < 1:
        raise RuntimeError(f"expected_count must be >= 1, got {expected_count}")
    if not isinstance(raw_data, list):
        raise RuntimeError(f"Top-level JSON value must be a list, got {type(raw_data).__name__}")
    if len(raw_data) != expected_count:
        raise RuntimeError(f"Expected {expected_count} cards, got {len(raw_data)}")

    expected_keys = set(CARD_KEYS)
    validated: list[dict[str, str]] = []
    for idx, item in enumerate(raw_data, start=1):
        if not isinstance(item, dict):
            raise RuntimeError(f"Card index {idx} must be a JSON object, got {type(item).__name__}")
        actual_keys = set(item.keys())
        if actual_keys != expected_keys:
            raise RuntimeError(f"Card {idx} has keys {sorted(actual_keys)}, expected {sorted(expected_keys)}")
        for key in CARD_KEYS:
            val = item[key]
            if not isinstance(val, str) or val.strip() == "":
                raise RuntimeError(f"Card {idx} field {key!r} must be a non-empty string")
        expected_id = f"C{idx:03d}"
        if item["card_id"] != expected_id:
            raise RuntimeError(f"Card {idx} has card_id {item['card_id']!r}, expected {expected_id!r}")
        validated.append({key: item[key] for key in CARD_KEYS})
    return validated


def _render_csv_bytes(cards: list[dict[str, str]]) -> bytes:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=CSV_FIELDS, lineterminator="\n")
    writer.writeheader()
    for card in cards:
        row = {key: card[key] for key in CARD_KEYS}
        row["preregistration_commit_sha"] = PREREGISTRATION_COMMIT_SHA
        writer.writerow(row)
    return buf.getvalue().encode("utf-8")


def _render_md_bytes(cards: list[dict[str, str]]) -> bytes:
    lines: list[str] = [
        "# Stage 0 Plain-Language Law Cards",
        "",
        f"- **preregistration_commit_sha:** {PREREGISTRATION_COMMIT_SHA}",
        f"- **Card count:** {len(cards)}",
        "",
    ]
    for card in cards:
        lines.extend(
            [
                f"## {card['card_id']}",
                f"- **what_it_says:** {card['what_it_says']}",
                f"- **quantities_related:** {card['quantities_related']}",
                f"- **conditions_to_hold:** {card['conditions_to_hold']}",
                "",
            ]
        )
    if lines and lines[-1] == "":
        lines = lines[:-1]
    return ("\n".join(lines) + "\n").encode("utf-8")


def _check_hygiene(named_texts: list[tuple[str, str]]) -> None:
    ci_words = _decode_hex_list(_CI_WORD_TOKENS_HEX)
    cs_words = _decode_hex_list(_CS_WORD_TOKENS_HEX)
    forbidden_substrings = _decode_hex_list(_FORBIDDEN_SUBSTRINGS_HEX)

    for label, text in named_texts:
        for tok in ci_words:
            if re.search(r"\b" + re.escape(tok) + r"\b", text, flags=re.IGNORECASE):
                raise RuntimeError(f"Restricted case-insensitive token {tok!r} found in {label}")
        for tok in cs_words:
            if re.search(r"\b" + re.escape(tok) + r"\b", text):
                raise RuntimeError(f"Restricted case-sensitive token {tok!r} found in {label}")
        lowered = text.lower()
        for tok in forbidden_substrings:
            if tok.lower() in lowered:
                raise RuntimeError(f"Forbidden substring {tok!r} found in {label}")


def run(input_arg: str, expected_count: int, verify_offline: bool) -> dict[str, Any]:
    input_path = _resolve_input_path(input_arg)
    if not input_path.exists():
        raise RuntimeError(f"Input JSON file not found: {input_path}")

    input_text = input_path.read_text(encoding="utf-8")
    raw_data = json.loads(input_text)
    cards = _validate_cards(raw_data, expected_count)

    csv_bytes = _render_csv_bytes(cards)
    md_bytes = _render_md_bytes(cards)
    csv_text = csv_bytes.decode("utf-8")
    md_text = md_bytes.decode("utf-8")
    script_text = Path(__file__).read_text(encoding="utf-8")

    _check_hygiene(
        [
            (input_path.name, input_text),
            (LAW_CARDS_CSV_PATH.name, csv_text),
            (LAW_CARDS_MD_PATH.name, md_text),
            (Path(__file__).name, script_text),
        ]
    )

    if verify_offline:
        if not LAW_CARDS_CSV_PATH.exists():
            raise RuntimeError(f"Missing output file on disk: {LAW_CARDS_CSV_PATH}")
        if not LAW_CARDS_MD_PATH.exists():
            raise RuntimeError(f"Missing output file on disk: {LAW_CARDS_MD_PATH}")
        if LAW_CARDS_CSV_PATH.read_bytes() != csv_bytes:
            raise RuntimeError(f"Byte-for-byte mismatch on {LAW_CARDS_CSV_PATH.name}")
        if LAW_CARDS_MD_PATH.read_bytes() != md_bytes:
            raise RuntimeError(f"Byte-for-byte mismatch on {LAW_CARDS_MD_PATH.name}")
    else:
        LAW_CARDS_CSV_PATH.write_bytes(csv_bytes)
        LAW_CARDS_MD_PATH.write_bytes(md_bytes)

    return {
        "mode": "verify-offline" if verify_offline else "build",
        "card_count": len(cards),
        "first_card_id": cards[0]["card_id"],
        "last_card_id": cards[-1]["card_id"],
        "csv_bytes": len(csv_bytes),
        "md_bytes": len(md_bytes),
        "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
        "hygiene_passed": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Stage 0 law cards JSON and serialize law_cards.csv and law_cards.md."
    )
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT_REL,
        help="Path to Stage 0 JSON array (default: packets/stage0_card_writer_output.json relative to proof/heldout/).",
    )
    parser.add_argument(
        "--expected-count",
        type=int,
        default=DEFAULT_EXPECTED_COUNT,
        help="Expected number of sequential cards (default: 65).",
    )
    parser.add_argument(
        "--verify-offline",
        action="store_true",
        help="Re-render in memory and verify byte-for-byte parity and hygiene checks against files on disk.",
    )
    args = parser.parse_args()
    result = run(args.input, args.expected_count, args.verify_offline)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
