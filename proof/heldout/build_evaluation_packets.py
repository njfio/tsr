#!/usr/bin/env python3
"""
build_evaluation_packets.py — Emit and verify the combined withheld-origin evaluation packet.

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
AMENDMENT_2_COMMIT_SHA = "530a254a51789a9fd68e1889f713b86d829c1146"
EXPECTED_CARD_COUNT = 65

HELDOUT_DIR = Path(__file__).resolve().parent
LAW_CARDS_CSV_PATH = HELDOUT_DIR / "law_cards.csv"
COMBINED_PACKET_PATH = HELDOUT_DIR / "combined_evaluation_packet.md"

CARD_FIELDS = ["card_id", "what_it_says", "quantities_related", "conditions_to_hold"]
LAW_CARDS_FIELDS = CARD_FIELDS + ["preregistration_commit_sha"]
CARDS_SECTION_MARKER = "## Section 3: Law Cards (`C001`..`C065`)"

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

_HEADER_LEAKS_HEX = [
    "67726176697479",
    "776f726b65642072756c696e67",
    "7265646163746564",
    "6578636c75646564",
]

_FORMULA_LEAKS_HEX = [
    "725f726561645f",
    "725f72656164",
    "646570656e64735f6f6e5f726573697374616e63655f6f725f73657061726174696f6e",
    "6e6f7420713120616e64",
    "6e6f7420713220616e64",
    "6e6f7420713420616e64",
    "626f6f6b72756c696e67",
    "6d6972726f7266756e63746f72",
    "69736964656e746974796f726571756976",
    "6973736861726564656e65726779776f726b",
    "646570656e64736f6e726573697374616e63656f7273657061726174696f6e",
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


def _render_combined_packet_bytes(cards: list[dict[str, str]]) -> bytes:
    """Render combined_evaluation_packet.md deterministically."""
    lines: list[str] = [
        "# Combined Evaluation Packet (Physics Codebook and Rule Application)",
        "",
        f"- **preregistration_commit_sha:** `{PREREGISTRATION_COMMIT_SHA}`",
        f"- **amendment_1_commit_sha:** `{AMENDMENT_1_COMMIT_SHA}`",
        f"- **amendment_2_commit_sha:** `{AMENDMENT_2_COMMIT_SHA}`",
        f"- **Card count:** {len(cards)} ({cards[0]['card_id']}..{cards[-1]['card_id']})",
        "",
        "## Instructions",
        "",
        "1. You are working in a clean, standalone session with zero access to external files, repositories, or background sources.",
        f"2. Evaluate all `{len(cards)}` law cards (`{cards[0]['card_id']}`..`{cards[-1]['card_id']}`) independently in the exact order presented. Do **not** use external sources, infer card origin, group, sort, or skip cards.",
        "3. **Part 1 (`q1`–`q4`):** Answer the four binary (`\"Yes\"` / `\"No\"`) physics questions (`q1` = `q1_identity_or_definition`, `q2` = `q2_mass_or_inertia_term`, `q3` = `q3_spatial_separation`, `q4` = `q4_shared_energy_curvature`) strictly from the physical law on each card, standard physics definitions, and the Section 1 questions and `q4` scope rule below.",
        '4. **Part 2 (`ruling` & `rationale`):** Apply **only** the two *The Sovereign Mirror* (v57) rule passages and term definitions reproduced verbatim in Section 2 below to judge whether each card keeps its relationship (`"Keep"`), turns around (`"Invert"`), or is not decided by the quoted text (`"the rule doesn\'t say"`). Do **not** derive `"ruling"` mechanically from your `q1..q4` answers; judge it directly from the quoted passages, and write a one-line `"rationale"` citing which phrase of the quoted rule applies.',
        f"5. Return **ONLY** a valid JSON array of `{len(cards)}` objects in exact order `{cards[0]['card_id']}`..`{cards[-1]['card_id']}` with exact keys `\"card_id\"`, `\"q1\"`, `\"q2\"`, `\"q3\"`, `\"q4\"`, `\"ruling\"`, and `\"rationale\"`:",
        "",
        "```json",
        "[",
        "  {",
        '    "card_id": "<card_id>",',
        '    "q1": "<Yes | No>",',
        '    "q2": "<Yes | No>",',
        '    "q3": "<Yes | No>",',
        '    "q4": "<Yes | No>",',
        '    "ruling": "<Keep | Invert | the rule doesn\'t say>",',
        '    "rationale": "<one-line rationale citing which phrase of the quoted rule applies>"',
        "  }",
        "]",
        "```",
        "",
        "## Section 1: Four Binary Physics Codebook Questions",
        "",
        *_CODEBOOK_QUESTIONS,
        "",
        "### Scope Rule for `q4`",
        "",
        _Q4_SCOPE_RULE,
        "",
        "## Section 2: Locked Rule Passages and Term Definitions (*The Sovereign Mirror*, v57)",
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


def _check_hygiene(script_text: str, packet_text: str) -> None:
    forbidden = _decode_hex_list(_FORBIDDEN_SUBSTRINGS_HEX)
    origin_ci = _decode_hex_list(_ORIGIN_CI_SUBSTRINGS_HEX)
    origin_cs = bytes.fromhex(_ORIGIN_CS_TOKEN_HEX).decode("utf-8")
    redacted_leaks = _decode_hex_list(_REDACTED_AND_ROW_LEAKS_HEX)
    header_leaks = _decode_hex_list(_HEADER_LEAKS_HEX)
    formula_leaks = _decode_hex_list(_FORMULA_LEAKS_HEX)

    for label, text in (
        (Path(__file__).name, script_text),
        (COMBINED_PACKET_PATH.name, packet_text),
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
        for tok in formula_leaks:
            if tok.lower() in lowered:
                raise RuntimeError(f"Formula/code leak {tok!r} found in {label}")

    cards_idx = packet_text.find(CARDS_SECTION_MARKER)
    if cards_idx == -1:
        raise RuntimeError(f"Missing {CARDS_SECTION_MARKER!r} in {COMBINED_PACKET_PATH.name}")
    header_lower = packet_text[:cards_idx].lower()
    for tok in redacted_leaks:
        if tok.lower() in header_lower:
            raise RuntimeError(f"Redacted-clause or row leak {tok!r} found in {COMBINED_PACKET_PATH.name} header")
    for tok in header_leaks:
        if tok.lower() in header_lower:
            raise RuntimeError(f"Header/citation leak {tok!r} found in {COMBINED_PACKET_PATH.name} header")


def run(verify_offline: bool) -> dict[str, Any]:
    cards = _load_all_law_cards()
    packet_bytes = _render_combined_packet_bytes(cards)
    packet_text = packet_bytes.decode("utf-8")
    script_text = Path(__file__).read_text(encoding="utf-8")

    _check_hygiene(script_text, packet_text)

    if verify_offline:
        if not COMBINED_PACKET_PATH.exists():
            raise RuntimeError(f"Missing output file on disk: {COMBINED_PACKET_PATH}")
        if COMBINED_PACKET_PATH.read_bytes() != packet_bytes:
            raise RuntimeError(f"Byte-for-byte mismatch on {COMBINED_PACKET_PATH.name}")
    else:
        COMBINED_PACKET_PATH.write_bytes(packet_bytes)

    return {
        "mode": "verify-offline" if verify_offline else "build",
        "card_count": len(cards),
        "first_card_id": cards[0]["card_id"],
        "last_card_id": cards[-1]["card_id"],
        "combined_evaluation_packet_bytes": len(packet_bytes),
        "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
        "amendment_1_commit_sha": AMENDMENT_1_COMMIT_SHA,
        "amendment_2_commit_sha": AMENDMENT_2_COMMIT_SHA,
        "hygiene_passed": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Emit and verify combined_evaluation_packet.md for 65 cards."
    )
    parser.add_argument(
        "--verify-offline",
        action="store_true",
        help="Re-render combined_evaluation_packet.md in memory and assert byte-for-byte parity and hygiene against disk.",
    )
    args = parser.parse_args()
    result = run(args.verify_offline)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
