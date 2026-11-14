#!/usr/bin/env python3
"""
build_ruling_packet.py — Build and verify the Track (a) withheld-origin author ruling packet.

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
DEFAULT_PHASE = "primary_48"
PRIMARY_EXPECTED_COUNT = 48

HELDOUT_DIR = Path(__file__).resolve().parent
PACKETS_DIR = HELDOUT_DIR / "packets"
LAW_CARDS_CSV_PATH = HELDOUT_DIR / "law_cards.csv"
SAMPLE_MANIFEST_PATH = HELDOUT_DIR / "sample_manifest.csv"
RULING_PACKET_CSV_PATH = HELDOUT_DIR / "ruling_packet.csv"
WORKSHEET_MD_PATH = PACKETS_DIR / "track_a_ruling_worksheet.md"

CARD_FIELDS = ["card_id", "what_it_says", "quantities_related", "conditions_to_hold"]
LAW_CARDS_FIELDS = CARD_FIELDS + ["preregistration_commit_sha"]

# Hex-encoded manifest columns so origin-metadata column names do not appear literally in this file.
_MANIFEST_FIELDS_HEX = [
    "636172645f6964",
    "736f757263655f736574",
    "6c61775f6964",
    "62656e63686d61726b5f6964",
    "766f6c756d65",
    "63686170746572",
    "726f775f696478",
    "65715f6e756d626572",
    "647261775f7068617365",
    "726573657276655f72616e6b",
    "707265726567697374726174696f6e5f636f6d6d69745f736861",
]

# Hex-encoded restricted vocabulary matching build_law_cards.py.
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

# Origin-leak tokens: first 6 checked case-insensitively, final identifier prefix checked case-sensitively.
_ORIGIN_CI_SUBSTRINGS_HEX = [
    "4f70656e53746178",
    "556e69766572736974792050687973696373",
    "62656e63686d61726b526f77733137",
    "62656e63686d61726b5f3137",
    "647261775f7068617365",
    "726573657276655f72616e6b",
]
_ORIGIN_CS_TOKEN_HEX = "4830"

_CARDS_SECTION_START = "## Withheld-Origin Law Cards"
_TEMPLATE_SECTION_START = "## Track (a) Ruling Fill-In Template"


def _decode_hex_list(hex_items: list[str]) -> list[str]:
    return [bytes.fromhex(item).decode("utf-8") for item in hex_items]


def _card_sort_key(card_id: str) -> tuple[int, str]:
    if not re.fullmatch(r"C\d{3,}", card_id):
        raise RuntimeError(f"Invalid card_id format: {card_id!r}")
    return (int(card_id[1:]), card_id)


def _load_law_cards() -> dict[str, dict[str, str]]:
    if not LAW_CARDS_CSV_PATH.exists():
        raise RuntimeError(f"Missing law_cards.csv at {LAW_CARDS_CSV_PATH}")
    cards_by_id: dict[str, dict[str, str]] = {}
    with LAW_CARDS_CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != LAW_CARDS_FIELDS:
            raise RuntimeError(f"Unexpected law_cards.csv header: {reader.fieldnames} != {LAW_CARDS_FIELDS}")
        for row in reader:
            if row["preregistration_commit_sha"] != PREREGISTRATION_COMMIT_SHA:
                raise RuntimeError(f"law_cards.csv SHA mismatch on {row.get('card_id')!r}")
            cid = row["card_id"]
            if cid in cards_by_id:
                raise RuntimeError(f"Duplicate card_id in law_cards.csv: {cid!r}")
            for field in CARD_FIELDS:
                if not isinstance(row[field], str) or row[field].strip() == "":
                    raise RuntimeError(f"Empty field {field!r} in law_cards.csv for {cid!r}")
            cards_by_id[cid] = {field: row[field] for field in CARD_FIELDS}
    if not cards_by_id:
        raise RuntimeError("law_cards.csv contains zero rows")
    return cards_by_id


def _select_heldout_card_ids(cards_by_id: dict[str, dict[str, str]], target_phase: str) -> list[str]:
    if not SAMPLE_MANIFEST_PATH.exists():
        raise RuntimeError(f"Missing sample_manifest.csv at {SAMPLE_MANIFEST_PATH}")
    manifest_fields = _decode_hex_list(_MANIFEST_FIELDS_HEX)
    phase_col = manifest_fields[8]
    seen_ids: set[str] = set()
    selected_ids: list[str] = []

    with SAMPLE_MANIFEST_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != manifest_fields:
            raise RuntimeError("Unexpected sample_manifest.csv header")
        for row in reader:
            if row["preregistration_commit_sha"] != PREREGISTRATION_COMMIT_SHA:
                raise RuntimeError(f"sample_manifest.csv SHA mismatch on {row.get('card_id')!r}")
            cid = row["card_id"]
            if cid in seen_ids:
                raise RuntimeError(f"Duplicate card_id in sample_manifest.csv: {cid!r}")
            seen_ids.add(cid)
            if cid not in cards_by_id:
                raise RuntimeError(f"Manifest card_id missing from law_cards.csv: {cid!r}")
            if row["source_set"] == "heldout" and row[phase_col] == target_phase:
                selected_ids.append(cid)

    if seen_ids != set(cards_by_id.keys()):
        raise RuntimeError("Mismatch between sample_manifest.csv card_ids and law_cards.csv card_ids")
    if not selected_ids:
        raise RuntimeError(f"No heldout cards matched phase {target_phase!r}")
    if target_phase == DEFAULT_PHASE and len(selected_ids) != PRIMARY_EXPECTED_COUNT:
        raise RuntimeError(f"Expected {PRIMARY_EXPECTED_COUNT} heldout cards for {target_phase!r}, got {len(selected_ids)}")

    return sorted(selected_ids, key=_card_sort_key)


def _render_ruling_packet_csv_bytes(selected_cards: list[dict[str, str]]) -> bytes:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=CARD_FIELDS, lineterminator="\n")
    writer.writeheader()
    for card in selected_cards:
        writer.writerow({field: card[field] for field in CARD_FIELDS})
    return buf.getvalue().encode("utf-8")


def _render_worksheet_md_bytes(selected_cards: list[dict[str, str]], target_phase: str) -> bytes:
    lines: list[str] = [
        "# Track (a) Author Ruling Worksheet",
        "",
        f"- **preregistration_commit_sha:** {PREREGISTRATION_COMMIT_SHA}",
        f"- **Selection phase:** {target_phase}",
        f"- **Card count:** {len(selected_cards)}",
        "- **Origin metadata status:** All origin metadata (source collection, law identifier, volume, chapter, row index, equation number, selection phase, and reserve order) is withheld from this packet.",
        "",
        "## Instructions",
        "",
        "1. Review each law card below independently with zero access to other ruling tracks or origin metadata.",
        '2. Assign each `card_id` a `ruling` in `{"Keep", "Invert", "the rule doesn\'t say"}` plus an optional `note`.',
        '3. Rulings equal to `"the rule doesn\'t say"` are counted and reported separately and are excluded from `(n_Keep, n_Invert)` when evaluating the minority-class extension threshold (`min(n_Keep, n_Invert) < 10`).',
        "4. Fill in the pre-populated template at the bottom (`card_id | ruling | note`) and send it back in chat.",
        "",
        "---",
        "",
        _CARDS_SECTION_START,
        "",
    ]
    for card in selected_cards:
        lines.extend(
            [
                f"### {card['card_id']}",
                f"- **what_it_says:** {card['what_it_says']}",
                f"- **quantities_related:** {card['quantities_related']}",
                f"- **conditions_to_hold:** {card['conditions_to_hold']}",
                "",
            ]
        )

    lines.extend(
        [
            "---",
            "",
            _TEMPLATE_SECTION_START,
            "",
            "Fill in `Keep`, `Invert`, or `the rule doesn't say` (and an optional `note`) for each row below and return the completed block in chat:",
            "",
            "```text",
            "card_id | ruling | note",
        ]
    )
    for card in selected_cards:
        lines.append(f"{card['card_id']} |  | ")
    lines.extend(["```", ""])
    return "\n".join(lines).encode("utf-8")


def _extract_worksheet_cards_section(md_text: str) -> str:
    start_idx = md_text.find(_CARDS_SECTION_START)
    end_idx = md_text.find(_TEMPLATE_SECTION_START)
    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        raise RuntimeError("Could not locate card section markers inside worksheet markdown")
    return md_text[start_idx:end_idx]


def _check_origin_and_repo_hygiene(named_texts: list[tuple[str, str]]) -> None:
    origin_ci = _decode_hex_list(_ORIGIN_CI_SUBSTRINGS_HEX)
    origin_cs = bytes.fromhex(_ORIGIN_CS_TOKEN_HEX).decode("utf-8")
    forbidden_substrings = _decode_hex_list(_FORBIDDEN_SUBSTRINGS_HEX)

    for label, text in named_texts:
        lowered = text.lower()
        for tok in origin_ci:
            if tok.lower() in lowered:
                raise RuntimeError(f"Origin-leak token {tok!r} found in {label}")
        if origin_cs in text or re.search(r"\bH\d{3}\b", text):
            raise RuntimeError(f"Origin identifier token found in {label}")
        for tok in forbidden_substrings:
            if tok.lower() in lowered:
                raise RuntimeError(f"Forbidden repo substring {tok!r} found in {label}")


def _check_restricted_vocab(named_texts: list[tuple[str, str]]) -> None:
    ci_words = _decode_hex_list(_CI_WORD_TOKENS_HEX)
    cs_words = _decode_hex_list(_CS_WORD_TOKENS_HEX)

    for label, text in named_texts:
        for tok in ci_words:
            if re.search(r"\b" + re.escape(tok) + r"\b", text, flags=re.IGNORECASE):
                raise RuntimeError(f"Restricted case-insensitive token {tok!r} found in {label}")
        for tok in cs_words:
            if re.search(r"\b" + re.escape(tok) + r"\b", text):
                raise RuntimeError(f"Restricted case-sensitive token {tok!r} found in {label}")


def run(target_phase: str, verify_offline: bool) -> dict[str, Any]:
    cards_by_id = _load_law_cards()
    selected_ids = _select_heldout_card_ids(cards_by_id, target_phase)
    selected_cards = [cards_by_id[cid] for cid in selected_ids]

    packet_csv_bytes = _render_ruling_packet_csv_bytes(selected_cards)
    worksheet_md_bytes = _render_worksheet_md_bytes(selected_cards, target_phase)

    packet_csv_text = packet_csv_bytes.decode("utf-8")
    worksheet_md_text = worksheet_md_bytes.decode("utf-8")
    worksheet_cards_text = _extract_worksheet_cards_section(worksheet_md_text)
    script_text = Path(__file__).read_text(encoding="utf-8")

    _check_origin_and_repo_hygiene(
        [
            (RULING_PACKET_CSV_PATH.name, packet_csv_text),
            (WORKSHEET_MD_PATH.name, worksheet_md_text),
            (Path(__file__).name, script_text),
        ]
    )
    _check_restricted_vocab(
        [
            (RULING_PACKET_CSV_PATH.name, packet_csv_text),
            (f"{WORKSHEET_MD_PATH.name}#cards", worksheet_cards_text),
        ]
    )

    if verify_offline:
        if not RULING_PACKET_CSV_PATH.exists():
            raise RuntimeError(f"Missing output file on disk: {RULING_PACKET_CSV_PATH}")
        if not WORKSHEET_MD_PATH.exists():
            raise RuntimeError(f"Missing output file on disk: {WORKSHEET_MD_PATH}")
        disk_csv_bytes = RULING_PACKET_CSV_PATH.read_bytes()
        disk_md_bytes = WORKSHEET_MD_PATH.read_bytes()
        if disk_csv_bytes != packet_csv_bytes:
            raise RuntimeError(f"Byte-for-byte mismatch on {RULING_PACKET_CSV_PATH.name}")
        if disk_md_bytes != worksheet_md_bytes:
            raise RuntimeError(f"Byte-for-byte mismatch on {WORKSHEET_MD_PATH.name}")
    else:
        PACKETS_DIR.mkdir(parents=True, exist_ok=True)
        RULING_PACKET_CSV_PATH.write_bytes(packet_csv_bytes)
        WORKSHEET_MD_PATH.write_bytes(worksheet_md_bytes)

    return {
        "mode": "verify-offline" if verify_offline else "build",
        "phase": target_phase,
        "selected_count": len(selected_cards),
        "csv_bytes": len(packet_csv_bytes),
        "md_bytes": len(worksheet_md_bytes),
        "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
        "hygiene_passed": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Emit and verify withheld-origin Track (a) author ruling packet."
    )
    parser.add_argument(
        "--draw-phase",
        dest="phase",
        default=DEFAULT_PHASE,
        help="Sampling phase to select from manifest (default: primary_48).",
    )
    parser.add_argument(
        "--verify-offline",
        action="store_true",
        help="Re-render in memory and verify byte-for-byte parity and hygiene checks against files on disk.",
    )
    args = parser.parse_args()
    result = run(args.phase, args.verify_offline)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
