#!/usr/bin/env python3
"""
build_evaluation_packets.py — Emit and verify Track (b) and Track (c) withheld-origin packets.

Reads ONLY proof/heldout/law_cards.csv (65 cards C001..C065).
Python 3.12+ standard library only (zero external packages).
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

PREREGISTRATION_COMMIT_SHA = "463ad9f93c8a276b1e0d9ee497198dfa2169d079"
AMENDMENT_1_COMMIT_SHA = "b66f48efb76e0f8d17d7db32848ad95f0a5c8633"
EXPECTED_CARD_COUNT = 65

HELDOUT_DIR = Path(__file__).resolve().parent
LAW_CARDS_CSV_PATH = HELDOUT_DIR / "law_cards.csv"
APPLIER_PACKET_PATH = HELDOUT_DIR / "applier_packet.md"
LABELING_PACKET_PATH = HELDOUT_DIR / "labeling_packet.md"

CARD_FIELDS = ["card_id", "what_it_says", "quantities_related", "conditions_to_hold"]
LAW_CARDS_FIELDS = CARD_FIELDS + ["preregistration_commit_sha"]
CARDS_SECTION_MARKER = "## Law Cards"

# Hex-encoded hygiene patterns so restricted/forbidden tokens never appear literally in this file.
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
    "73616d706c655f6d616e6966657374",
]

_ORIGIN_CI_SUBSTRINGS_HEX = [
    "4f70656e53746178",
    "556e69766572736974792050687973696373",
    "62656e63686d61726b526f77733137",
    "62656e63686d61726b5f3137",
    "647261775f7068617365",
    "726573657276655f72616e6b",
    "63616c6962726174696f6e",
]
_ORIGIN_CS_TOKEN_HEX = "4830"

_REDACTED_AND_ROW_LEAKS_HEX = [
    "64656e736974792074696d657320766f6c756d65",
    "6d6173732074696d657320616363656c65726174696f6e",
    "726f77732035",
    "726f7773203135",
    "726f77732036",
    "726f77732037",
    "726f77732038",
    "726f7773203136",
]

_APPLIER_HEADER_LEAKS_HEX = [
    "67726176697479",
    "776f726b65642072756c696e67",
    "7265646163746564",
    "6578636c75646564",
]

_TSR_CI_WORD_TOKENS_HEX = [
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
    "6d6972726f72",
    "763537",
    "746865206d6170",
    "6c696d69746c657373",
]

_TSR_CI_SUBSTRINGS_HEX = [
    "725f72656164",
    "626f6f6b72756c696e67",
    "6d6972726f7266756e63746f72",
]

_TSR_CS_WORD_TOKENS_HEX = [
    "4d6f76656d656e74",
    "43757272656e74",
    "566f72746578",
    "436f6e76657267656e6365",
    "41747472616374696f6e",
    "566962726174696f6e",
    "457870616e73696f6e",
    "4d6972726f72",
    "4d6170",
    "534d",
]

# Verbatim rule passages and term definitions from PREREGISTRATION.md Section 1.6.
_RULE_PASSAGE_CH2_P20 = (
    "> The main difference between the physical and the nonphysical is resistance. "
    "That’s the rule, or the start of it. Physics already measures resistance to a change in motion. "
    "It calls it mass. So you take the world Einstein described and reflect it: keep each relationship, "
    "and flip the condition. Resistant becomes receptive, limited becomes limitless, radiating becomes collecting. "
    "What comes out the other side is the nonphysical version. Every term reflects; that part always happens. "
    "What you have to know is whether the relationship keeps its shape or turns around. "
    "If it depends on resistance, or on the distance resistance makes, so that more mass or more separation "
    "means more of something, flipping resistant to receptive turns it around: more Movement means less of that thing, "
    "or it gets easier instead of harder. If it’s an identity or a definition, two names for one thing, [...], "
    "there’s nothing to turn around, even with mass in it; the terms reflect and the relationship keeps its shape. "
    "That’s the one rule."
)

_RULE_PASSAGE_CH16_P116 = (
    "> The rule from Chapter 2 does, whoever is running it, because it asks one question of every row: "
    "does this relationship depend on resistance, or on the distance resistance makes, or is it an identity, "
    "a definition, or the work of the one energy both sides share?"
)

_TERM_DEF_CH1_P16 = (
    "> There are two environments, the physical and the nonphysical, and they’re mirror images of each other. "
    "The physical is limited, resistant, and it radiates. The nonphysical is limitless, receptive, and it collects. "
    "Those three pairs aren’t three separate rules—they’re one condition seen three ways. Resistance creates a boundary, "
    "which makes a thing limited, and bounded things can only reach each other by radiating across the space between them. "
    "Take resistance away and there’s no boundary, so the nonphysical is limitless, and with nothing held apart, "
    "it collects instead of radiating. Everything else in TSR comes from what happens where they meet."
)

_TERM_DEF_CH2_P25 = (
    "> Resistance is resistance to change.\n"
    ">\n"
    "> Physical, in this book, is the resistant condition wherever it occurs, not matter as opposed to mind."
)

_TERM_DEF_CH2_P21 = (
    "> Think about what space and time actually do. On the physical side, where resistance gives things edges, "
    "space is what keeps two things from sitting in the same place, and time is what keeps everything from happening at once. "
    "Take resistance away and there’s no distance. Two particulars in the same whole don’t sit in different places; "
    "they differ by how they vibrate, the way two notes share the same air in a room. So space reflects as Vibration. "
    "And where nothing decays or comes apart, before and after are separated only by the whole becoming more than it was."
)

_TERM_DEF_MAP_P175 = (
    "> Receptivity to change in motion; a self-contained part of the whole, like a movement in a symphony. "
    "The reflection of mass."
)

_TERM_DEF_CH16_P117 = (
    "> TSR has three: the two sides and the continuum where they meet, with one energy in it."
)

_TERM_DEF_CH17_P131 = (
    "> There aren’t two energies, one spiritual and one physical, taking turns. There’s one energy transmuting. "
    "On the nonphysical side it’s conscious energy: the Collective and Vibrational realities are made of it."
)

_TERM_DEF_CH17_P132 = (
    "> Where your Vibrational Reality meets your Subjective Reality, the two blend. "
    "I call that conscious-physical energy."
)

_TERM_DEF_MAP_P174 = (
    "> The blend of conscious and physical energy at the hinge, the E."
)

# Verbatim codebook questions and pure-physics q4 scope rule from PREREGISTRATION.md Section 1.7.
_CODEBOOK_QUESTIONS = [
    (
        "- **`q1_identity_or_definition` (`Yes` / `No`):** "
        "*Does this equation/statement primarily express a conservation law, equivalence or correspondence identity, "
        "defining physical relation, symmetry/frame-invariance principle, or reciprocal action-reaction pairing "
        "(as opposed to a dynamical resistance, inertial barrier, or spatial-separation effect)?*"
    ),
    (
        "- **`q2_mass_or_inertia_term` (`Yes` / `No`):** "
        "*Does the equation/statement explicitly include mass, gravitational mass, inertial mass, moment of inertia, "
        "linear/angular mass resistance, or a fixed quantity/mass of gas or matter ($m$, $M$, $I$, $n$)?*"
    ),
    (
        "- **`q3_spatial_separation` (`Yes` / `No`):** "
        "*Does the physical law or effect explicitly depend on spatial distance, displacement, separation between "
        "bodies or events, or path/length difference ($r$, $d$, $\\Delta x$, $\\Delta s$, $L$)?*"
    ),
    (
        "- **`q4_shared_energy_curvature` (`Yes` / `No`):** "
        "*Does the equation/statement govern shared gravitational/spacetime curvature, gravitational wells or lensing, "
        "or conservative potential-well / shared field energy coupling across space — including all Newtonian and "
        "relativistic gravitational laws (rather than non-gravitational inertial resistance to acceleration or "
        "point-to-point transport/dissipation)?*"
    ),
]

_Q4_SCOPE_RULE = (
    "> Answer `q4 = Yes` for **all gravitational laws**, including Newtonian universal gravitation "
    "($F = Gm_1 m_2 / r^2$) and closely related orbital/gravitational force laws, gravitational "
    "field/potential/wells ($U_g = -GMm/r$, escape/orbital balance), relativistic spacetime curvature / "
    "mass-energy warping, and gravitational lensing. Non-gravitational laws involving inertial resistance "
    "to acceleration or point-to-point transport/dissipation remain `q4 = No`."
)


def _decode_hex_list(hex_items: list[str]) -> list[str]:
    return [bytes.fromhex(item).decode("utf-8") for item in hex_items]


def _load_all_law_cards() -> list[dict[str, str]]:
    """Load and validate all 65 sequential law cards from proof/heldout/law_cards.csv."""
    if not LAW_CARDS_CSV_PATH.exists():
        raise RuntimeError(f"Missing law_cards.csv at {LAW_CARDS_CSV_PATH}")
    cards: list[dict[str, str]] = []
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
            for field in CARD_FIELDS:
                if not isinstance(row[field], str) or row[field].strip() == "":
                    raise RuntimeError(f"Empty field {field!r} in law_cards.csv for {expected_id!r}")
            cards.append({field: row[field] for field in CARD_FIELDS})
    if len(cards) != EXPECTED_CARD_COUNT:
        raise RuntimeError(f"Expected {EXPECTED_CARD_COUNT} cards in law_cards.csv, got {len(cards)}")
    return cards


def _render_cards_lines(cards: list[dict[str, str]]) -> list[str]:
    lines: list[str] = [CARDS_SECTION_MARKER, ""]
    for card in cards:
        lines.extend(
            [
                f"### {card['card_id']}",
                f"- **what_it_says:** {card['what_it_says']}",
                f"- **quantities_related:** {card['quantities_related']}",
                f"- **conditions_to_hold:** {card['conditions_to_hold']}",
                "",
            ]
        )
    if lines and lines[-1] == "":
        lines = lines[:-1]
    return lines


def _render_applier_packet_bytes(cards: list[dict[str, str]]) -> bytes:
    """Render Track (b) applier_packet.md deterministically."""
    lines: list[str] = [
        "# Track (b) Independent Rule-Applier Evaluation Packet",
        "",
        f"- **preregistration_commit_sha:** `{PREREGISTRATION_COMMIT_SHA}`",
        f"- **amendment_1_commit_sha:** `{AMENDMENT_1_COMMIT_SHA}`",
        f"- **Card count:** {len(cards)} ({cards[0]['card_id']}..{cards[-1]['card_id']})",
        "",
        "## Instructions",
        "",
        "1. You are working in a clean, standalone session with zero access to external files, repositories, or background sources.",
        "2. Apply **ONLY** the two *The Sovereign Mirror* (v57) rule passages and the term definitions reproduced verbatim below. Do **not** rely on external sources, outside knowledge, or infer the origin of any card.",
        f"3. Evaluate all `{len(cards)}` law cards (`{cards[0]['card_id']}`..`{cards[-1]['card_id']}`) independently in the exact order presented. Do **not** group, sort, or omit any card.",
        '4. For each card, assign `ruling` in `{"Keep", "Invert", "the rule doesn\'t say"}` and a one-line `rationale` citing which phrase of the quoted rule applies.',
        f"5. Return **ONLY** a valid JSON array of `{len(cards)}` objects in exact order `{cards[0]['card_id']}`..`{cards[-1]['card_id']}` with exact keys `\"card_id\"`, `\"ruling\"`, and `\"rationale\"`:",
        "",
        "```json",
        "[",
        "  {",
        '    "card_id": "<card_id>",',
        '    "ruling": "<Keep | Invert | the rule doesn\'t say>",',
        '    "rationale": "<one-line rationale citing which phrase of the quoted rule applies>"',
        "  }",
        "]",
        "```",
        "",
        "## Locked Rule Passages and Term Definitions (*The Sovereign Mirror*, v57)",
        "",
        "### Rule Passages",
        "",
        "- **Chapter 2 (*The One Rule*), p. 20:**",
        _RULE_PASSAGE_CH2_P20,
        "",
        "- **Chapter 16 (*Twelve Reflections*), p. 116:**",
        _RULE_PASSAGE_CH16_P116,
        "",
        "### Term Definitions",
        "",
        "- **Two Environments (Chapter 1, p. 16):**",
        _TERM_DEF_CH1_P16,
        "",
        '- **Resistance and "Physical" (Chapter 2, p. 25):**',
        _TERM_DEF_CH2_P25,
        "",
        "- **Space, Time, and Distance (Chapter 2, p. 21):**",
        _TERM_DEF_CH2_P21,
        "",
        "- **Nonphysical Movement (*The Map*, p. 175):**",
        _TERM_DEF_MAP_P175,
        "",
        "- **The One Energy Both Sides Share (Chapter 16, p. 117; Chapter 17, pp. 131–132; *The Map*, p. 174):**",
        "  - Chapter 16, p. 117:",
        _TERM_DEF_CH16_P117,
        "  - Chapter 17, p. 131:",
        _TERM_DEF_CH17_P131,
        "  - Chapter 17, p. 132:",
        _TERM_DEF_CH17_P132,
        "  - *The Map*, p. 174 (*Conscious-physical energy* entry):",
        _TERM_DEF_MAP_P174,
        "",
        "---",
        "",
    ]
    lines.extend(_render_cards_lines(cards))
    return ("\n".join(lines) + "\n").encode("utf-8")


def _render_labeling_packet_bytes(cards: list[dict[str, str]]) -> bytes:
    """Render Track (c) labeling_packet.md deterministically."""
    lines: list[str] = [
        "# Track (c) Physics Codebook Evaluation Packet",
        "",
        f"- **preregistration_commit_sha:** `{PREREGISTRATION_COMMIT_SHA}`",
        f"- **amendment_1_commit_sha:** `{AMENDMENT_1_COMMIT_SHA}`",
        f"- **Card count:** {len(cards)} ({cards[0]['card_id']}..{cards[-1]['card_id']})",
        "",
        "## Instructions",
        "",
        "1. You are working in a clean, standalone physics classification session with zero access to external files, repositories, or background sources.",
        f"2. Read each of the `{len(cards)}` physics law cards (`{cards[0]['card_id']}`..`{cards[-1]['card_id']}`) independently in the exact order presented, using standard physics definitions and the four binary (`\"Yes\"` / `\"No\"`) questions and scope rule below. Do **not** group, sort, or omit cards, and do **not** infer the origin of any card.",
        '3. For each card, answer `q1` (`q1_identity_or_definition`), `q2` (`q2_mass_or_inertia_term`), `q3` (`q3_spatial_separation`), and `q4` (`q4_shared_energy_curvature`) with exact string `"Yes"` or `"No"`.',
        f"4. Return **ONLY** a valid JSON array of `{len(cards)}` objects in exact order `{cards[0]['card_id']}`..`{cards[-1]['card_id']}` with exact keys `\"card_id\"`, `\"q1\"`, `\"q2\"`, `\"q3\"`, and `\"q4\"`:",
        "",
        "```json",
        "[",
        "  {",
        '    "card_id": "<card_id>",',
        '    "q1": "<Yes | No>",',
        '    "q2": "<Yes | No>",',
        '    "q3": "<Yes | No>",',
        '    "q4": "<Yes | No>"',
        "  }",
        "]",
        "```",
        "",
        "## Four Binary Physics Codebook Questions",
        "",
        *_CODEBOOK_QUESTIONS,
        "",
        "### Scope Rule for `q4`",
        "",
        _Q4_SCOPE_RULE,
        "",
        "---",
        "",
    ]
    lines.extend(_render_cards_lines(cards))
    return ("\n".join(lines) + "\n").encode("utf-8")


def _check_hygiene(script_text: str, applier_text: str, labeling_text: str) -> None:
    forbidden = _decode_hex_list(_FORBIDDEN_SUBSTRINGS_HEX)
    origin_ci = _decode_hex_list(_ORIGIN_CI_SUBSTRINGS_HEX)
    origin_cs = bytes.fromhex(_ORIGIN_CS_TOKEN_HEX).decode("utf-8")
    redacted_leaks = _decode_hex_list(_REDACTED_AND_ROW_LEAKS_HEX)
    applier_header_leaks = _decode_hex_list(_APPLIER_HEADER_LEAKS_HEX)
    tsr_ci_words = _decode_hex_list(_TSR_CI_WORD_TOKENS_HEX)
    tsr_ci_substrings = _decode_hex_list(_TSR_CI_SUBSTRINGS_HEX)
    tsr_cs_words = _decode_hex_list(_TSR_CS_WORD_TOKENS_HEX)

    for label, text in (
        (Path(__file__).name, script_text),
        (APPLIER_PACKET_PATH.name, applier_text),
        (LABELING_PACKET_PATH.name, labeling_text),
    ):
        lowered = text.lower()
        for tok in forbidden:
            if tok.lower() in lowered:
                raise RuntimeError(f"Forbidden repo token {tok!r} found in {label}")
        for tok in origin_ci:
            if tok.lower() in lowered:
                raise RuntimeError(f"Origin-leak token {tok!r} found in {label}")
        if origin_cs in text or re.search(r"\bH\d{3}\b", text):
            raise RuntimeError(f"Origin identifier token found in {label}")

    applier_lower = applier_text.lower()
    for tok in redacted_leaks:
        if tok.lower() in applier_lower:
            raise RuntimeError(f"Redacted-clause or row leak {tok!r} found in {APPLIER_PACKET_PATH.name}")

    applier_cards_idx = applier_text.find(CARDS_SECTION_MARKER)
    if applier_cards_idx == -1:
        raise RuntimeError(f"Missing {CARDS_SECTION_MARKER!r} in {APPLIER_PACKET_PATH.name}")
    applier_header_lower = applier_text[:applier_cards_idx].lower()
    for tok in applier_header_leaks:
        if tok.lower() in applier_header_lower:
            raise RuntimeError(f"Header/citation leak {tok!r} found in {APPLIER_PACKET_PATH.name}")

    labeling_lower = labeling_text.lower()
    for tok in tsr_ci_words:
        if re.search(r"\b" + re.escape(tok) + r"\b", labeling_text, flags=re.IGNORECASE):
            raise RuntimeError(f"TSR case-insensitive word {tok!r} found in {LABELING_PACKET_PATH.name}")
    for tok in tsr_ci_substrings:
        if tok.lower() in labeling_lower:
            raise RuntimeError(f"TSR identifier substring {tok!r} found in {LABELING_PACKET_PATH.name}")
    for tok in tsr_cs_words:
        if re.search(r"\b" + re.escape(tok) + r"\b", labeling_text):
            raise RuntimeError(f"TSR case-sensitive word {tok!r} found in {LABELING_PACKET_PATH.name}")


def run(verify_offline: bool) -> dict[str, Any]:
    cards = _load_all_law_cards()
    applier_bytes = _render_applier_packet_bytes(cards)
    labeling_bytes = _render_labeling_packet_bytes(cards)

    applier_text = applier_bytes.decode("utf-8")
    labeling_text = labeling_bytes.decode("utf-8")
    script_text = Path(__file__).read_text(encoding="utf-8")

    _check_hygiene(script_text, applier_text, labeling_text)

    if verify_offline:
        if not APPLIER_PACKET_PATH.exists():
            raise RuntimeError(f"Missing output file on disk: {APPLIER_PACKET_PATH}")
        if not LABELING_PACKET_PATH.exists():
            raise RuntimeError(f"Missing output file on disk: {LABELING_PACKET_PATH}")
        if APPLIER_PACKET_PATH.read_bytes() != applier_bytes:
            raise RuntimeError(f"Byte-for-byte mismatch on {APPLIER_PACKET_PATH.name}")
        if LABELING_PACKET_PATH.read_bytes() != labeling_bytes:
            raise RuntimeError(f"Byte-for-byte mismatch on {LABELING_PACKET_PATH.name}")
    else:
        APPLIER_PACKET_PATH.write_bytes(applier_bytes)
        LABELING_PACKET_PATH.write_bytes(labeling_bytes)

    return {
        "mode": "verify-offline" if verify_offline else "build",
        "card_count": len(cards),
        "first_card_id": cards[0]["card_id"],
        "last_card_id": cards[-1]["card_id"],
        "applier_packet_bytes": len(applier_bytes),
        "labeling_packet_bytes": len(labeling_bytes),
        "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
        "amendment_1_commit_sha": AMENDMENT_1_COMMIT_SHA,
        "hygiene_passed": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Emit and verify Track (b) applier_packet.md and Track (c) labeling_packet.md for 65 cards."
    )
    parser.add_argument(
        "--verify-offline",
        action="store_true",
        help="Re-render both packets in memory and assert byte-for-byte parity and hygiene against disk.",
    )
    args = parser.parse_args()
    result = run(args.verify_offline)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
