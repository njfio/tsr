"""
lexical_rigidity.py — Part II.B: Chapter 16 Axiomatic MUC Audit & Cross-Platform Discrete-Sense Lexicon Audit
=============================================================================================================
Epistemic scope: Following *The Sovereign Mirror* (v57, A Note Before We Begin p. 9),
"the table borrows the shape of physics, not its authority." Z3 does not independently
know English, and the relation sets, `CANDIDATES` feature booleans, `SLOT_REQUIREMENTS`
rules, and per-slot keyword groups (`DUAL_SENSE_POLYSEMY_SPECS` / `SINGLE_SENSE_DOMAIN_SPECS`)
were all written by hand knowing the target Map terms (they are NOT "blind" to the
target words). What the Z3 result establishes is: no two terms in the Map, as encoded,
are interchangeable.

Contains THREE explicitly distinguished components:
  1. Axiomatic Formalization of Chapter 16's Synchronic Elimination Rules (Z3):
     Encodes the stated multi-row structural and semantic elimination criteria from
     *The Sovereign Mirror* (v57: Ch. 2 pp. 26-27, Ch. 6 pp. 46-51, Ch. 8 pp. 59-60,
     Ch. 16 pp. 122-126, Ch. 17 pp. 128-130, and The Map pp. 169-176) over the
     30-word candidate pool. Proves that the encoded Chapter 16 criteria are mutually
     consistent, admit a unique satisfying assignment across all P(30, 14) = 4.28e18
     injective assignments (with only `growth` surviving before the continuum tiebreak,
     matching p. 124), and yield 21 deletion-verified 1-minimal UNSAT cores.
  2. Cross-Platform Discrete WordNet 3.0 Synset-Gloss Audit (All Platforms, Zero Window Parameters):
     Evaluates all 14 nonphysical slots of Chapter 16 (7 explicit dual-sense polysemy slots
     + 7 single-sense lexical-domain slots) against genuine Princeton WordNet 3.0 discrete
     synset definitions (`wordnet_100_synsets.json`, SHA-256 verified) across all 100
     single-word candidates (`PRIMARY_30_POOL` U `CURRENT_CANDIDATES` U `ledger_80`).
     Distinction: the per-slot concept keyword groups were written by hand knowing the
     target words, while the dictionary intersection helper uses zero hand-coded per-word
     booleans, zero character-window tuning, and an automated stem check enforcing zero
     target-word stem self-matching. Runs deterministically on macOS, Linux, and Windows.
  3. Live macOS New Oxford American Dictionary Discrete-Sense & Uniform Window-Sweep Audit:
     When macOS `CoreServices` is available, queries New Oxford American Dictionary
     (`DCSCopyTextDefinition`), strips `ORIGIN` etymology blocks before lowercasing, splits
     entries strictly on discrete sense delimiters (`•`, `;`, POS headers, numbered senses)
     into whole-word definition token sets across all 14 slots with zero window parameters,
     and runs a uniform character-gap sensitivity sweep over `w in [40, 60, 80, 100]`.
     When `CoreServices` is unavailable (Linux/Windows), runs deterministically via the
     checked-in cross-platform Princeton WordNet 3.0 payload (`wordnet_100_synsets.json`).
"""
from __future__ import annotations

import ctypes
import ctypes.util
import hashlib
import importlib.util
import itertools
import json
import re
import sys
from pathlib import Path
from typing import Any

import z3

Z3_DIR = Path(__file__).resolve().parent
REPO_ROOT = Z3_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from arms.a3_shuffled import build_arm_a3_permutation, build_arm_a3_swap_sides  # noqa: E402
from rule.tsr_formal_port import CURRENT_CANDIDATES  # noqa: E402

WORDNET_SYNSETS_PATH = Z3_DIR / "wordnet_100_synsets.json"
EXPECTED_WORDNET_ARCHIVE_SHA256 = "cbda5ea6eef7f36a97a43d4a75f85e07fccbb4f23657d27b4ccbc93e2646ab59"
EXPECTED_WORDNET_PAYLOAD_SHA256 = "39bb1c50ec3438386138e05af49be80aa8407e16a7481ea93a8c66508e3b14cf"

# 14 core nonphysical slots tested across Ch. 2, Ch. 8, Ch. 16, and A3
SLOTS: list[str] = [
    "Current",
    "Movement",
    "Expansion",
    "Vibration",
    "Frequency",
    "Appreciation",
    "Tune",
    "Convergence",
    "Desire",
    "Vibrance",
    "Idle",
    "Reflected",
    "Future",
    "Intuition",
]

# Boolean lexical + structural predicates (hand-written knowing the target Map terms,
# cited to SM v57 pages and dictionary senses)
FEATURES: list[str] = [
    "not_physical_side_term",          # Not already a physical-side term (Belief, Focus, Now, Past, Space, etc.)
    "not_center_whole_entity",         # Not the two-sided center whole ('soul' = Eternal-Energetic-Entity, p. 123)
    "zero_travel_medium",              # Compatible with zero spatial travel/glass/compression (p. 122)
    "receptive_non_forcing",           # Receptive rather than willpower/effortful pushing (p. 124)
    "non_hierarchical",                # Does not posit a rank/being above the entity (p. 123)
    "unseparated_shared_medium",       # Does not enclose reality inside a private skull/mind (p. 123)
    "means_persistent_flow",           # Dictionary sense: a continuous flowing stream (p. 123, p. 125)
    "collects_rather_than_radiates",   # Gathers/runs together rather than pouring outward from a point (p. 123)
    "means_present_moment",            # Dictionary sense: happening now / the present time (p. 123, p. 125)
    "means_motion_receptivity",        # Dictionary sense: act/receptivity of changing motion (pp. 21, 123, Map p. 175)
    "means_self_contained_part",       # Dictionary sense: self-contained section of a larger whole, e.g. symphony (pp. 21, 31, Map p. 175)
    "irreversible_cumulative_growth",  # Dictionary sense: unfolding/enlarging irreversibly (p. 123)
    "continuum_unfolding_sense",       # Continuum/whole spreading-out (cosmic expansion) rather than bounded organismal lifecycle
    "oscillatory_difference_root",     # Dictionary sense: oscillatory state grounding Frequency & Vibrance (p. 123, p. 125)
    "change_is_felt_emotion",          # Experiential readout: felt frequency whose change is emotion (p. 124, p. 174)
    "means_rate_of_value_rise",        # Dictionary sense: rising in value / quickening of gain (p. 124, p. 125)
    "means_gratitude_alignment",       # Dictionary sense: gratitude / thankful recognition (p. 124, p. 125)
    "selects_receptivity_target",      # Dictionary sense: actively selecting a resonant frequency/station (p. 124)
    "means_coming_together",           # Dictionary sense: streams meeting/focusing without a physical lens (p. 122)
    "means_pure_wanting",              # Dictionary sense: what is wanted, outward pull (p. 125)
    "means_vibration_extent",          # Dictionary sense: fullness/resonance extent of vibration (p. 26, p. 175)
    "means_poised_at_rest",            # Dictionary sense: running while standing still (p. 27, p. 125)
    "means_returning_closed_loop",     # Dictionary sense: bent/turned back on itself (p. 27, p. 125)
    "flow_direction_out",              # Carries outward directional polarity ('Out For' / 'Future' / 'Desire', p. 124)
    "flow_direction_in",               # Carries inward receiving polarity ('In To' / 'Current' / 'Intuition', p. 124)
    "means_direct_unlived_knowing",    # Dictionary sense: immediate knowing received prior to action/reasoning (p. 48)
]

FEAT_IDX: dict[str, int] = {f: i for i, f in enumerate(FEATURES)}


def _make_vec(true_feats: list[str]) -> dict[str, bool]:
    unknown = set(true_feats) - set(FEATURES)
    assert not unknown, f"Unknown features: {unknown}"
    return {f: (f in true_feats) for f in FEATURES}


COMMON_NONPHYS = [
    "not_physical_side_term",
    "not_center_whole_entity",
    "zero_travel_medium",
    "receptive_non_forcing",
    "non_hierarchical",
    "unseparated_shared_medium",
]

# Hand-written feature profiles (authored knowing the target words) for all 14 canonical
# TSR terms + 16 challengers + physical terms for A3-S
CANDIDATES: dict[str, dict[str, bool]] = {
    # --- 14 Canonical TSR Nonphysical Terms ---
    "Current": _make_vec(
        COMMON_NONPHYS
        + ["means_persistent_flow", "collects_rather_than_radiates", "means_present_moment", "flow_direction_in"]
    ),
    "Movement": _make_vec(
        COMMON_NONPHYS + ["means_motion_receptivity", "means_self_contained_part"]
    ),
    "Expansion": _make_vec(
        COMMON_NONPHYS + ["irreversible_cumulative_growth", "continuum_unfolding_sense"]
    ),
    "Vibration": _make_vec(
        COMMON_NONPHYS + ["oscillatory_difference_root"]
    ),
    "Frequency": _make_vec(
        COMMON_NONPHYS + ["oscillatory_difference_root", "change_is_felt_emotion"]
    ),
    "Appreciation": _make_vec(
        COMMON_NONPHYS + ["means_rate_of_value_rise", "means_gratitude_alignment"]
    ),
    "Tune": _make_vec(
        COMMON_NONPHYS + ["selects_receptivity_target"]
    ),
    "Convergence": _make_vec(
        COMMON_NONPHYS + ["means_coming_together", "collects_rather_than_radiates"]
    ),
    "Desire": _make_vec(
        COMMON_NONPHYS + ["means_pure_wanting", "flow_direction_out"]
    ),
    "Vibrance": _make_vec(
        COMMON_NONPHYS + ["means_vibration_extent", "oscillatory_difference_root"]
    ),
    "Idle": _make_vec(
        COMMON_NONPHYS + ["means_poised_at_rest"]
    ),
    "Reflected": _make_vec(
        COMMON_NONPHYS + ["means_returning_closed_loop"]
    ),
    "Future": _make_vec(
        COMMON_NONPHYS + ["irreversible_cumulative_growth", "continuum_unfolding_sense", "flow_direction_out"]
    ),
    "Intuition": _make_vec(
        COMMON_NONPHYS + ["means_direct_unlived_knowing", "flow_direction_in"]
    ),
    # --- 16 Explicit Challengers from The Sovereign Mirror & tsr_formal_port.py ---
    "belief lens": _make_vec(
        # Fails not_physical_side_term ('Belief' is physical Out Through) AND zero_travel_medium ('lens' requires travel, p. 122)
        ["not_center_whole_entity", "receptive_non_forcing", "non_hierarchical", "unseparated_shared_medium", "means_coming_together", "collects_rather_than_radiates"]
    ),
    "Vibrational Lens": _make_vec(
        # Fixes 'Belief', but still fails zero_travel_medium ('lens' is physical glass/mass traversed by traveling rays, p. 122)
        ["not_physical_side_term", "not_center_whole_entity", "receptive_non_forcing", "non_hierarchical", "unseparated_shared_medium", "means_coming_together", "collects_rather_than_radiates", "oscillatory_difference_root"]
    ),
    "soul": _make_vec(
        # Fails means_motion_receptivity AND not_center_whole_entity (soul = Eternal-Energetic-Entity joining both sides, p. 123)
        ["not_physical_side_term", "zero_travel_medium", "receptive_non_forcing", "non_hierarchical", "unseparated_shared_medium", "means_self_contained_part"]
    ),
    "Source": _make_vec(
        # Fails collects_rather_than_radiates (pours outward from a point = radiation) and means_present_moment (p. 123)
        ["not_physical_side_term", "not_center_whole_entity", "zero_travel_medium", "receptive_non_forcing", "non_hierarchical", "unseparated_shared_medium", "means_persistent_flow"]
    ),
    "God": _make_vec(
        # Fails non_hierarchical (posits a supreme ranked being above), collects_rather_than_radiates, means_present_moment (p. 123)
        ["not_physical_side_term", "not_center_whole_entity", "zero_travel_medium", "receptive_non_forcing", "unseparated_shared_medium"]
    ),
    "eternity": _make_vec(
        # Fails irreversible_cumulative_growth (static timelessness; nothing new can be added, breaking The Knife, p. 123)
        COMMON_NONPHYS
    ),
    "mind": _make_vec(
        # Fails oscillatory_difference_root (Frequency & Vibrance lose their root) and unseparated_shared_medium (private mental space, p. 123)
        ["not_physical_side_term", "not_center_whole_entity", "zero_travel_medium", "receptive_non_forcing", "non_hierarchical"]
    ),
    "will": _make_vec(
        # Fails receptive_non_forcing (willpower = physical Focus/effort) and change_is_felt_emotion (p. 124)
        ["not_center_whole_entity", "zero_travel_medium", "non_hierarchical", "unseparated_shared_medium"]
    ),
    "growth": _make_vec(
        # Closest challenger (p. 124): has irreversible_cumulative_growth, but fails means_rate_of_value_rise (2nd derivative/yield) & means_gratitude_alignment
        COMMON_NONPHYS + ["irreversible_cumulative_growth"]
    ),
    "surrender": _make_vec(
        # Receptive, but fails selects_receptivity_target (picks no station, erasing nonphysical agency, p. 124)
        COMMON_NONPHYS
    ),
    "responsiveness": _make_vec(
        # Has motion receptivity, but fails means_self_contained_part (not a discrete particular like a movement in a symphony)
        COMMON_NONPHYS + ["means_motion_receptivity"]
    ),
    "gratitude": _make_vec(
        # Has thankful alignment, but fails means_rate_of_value_rise (lacks acceleration/appreciation-in-value sense, p. 125)
        COMMON_NONPHYS + ["means_gratitude_alignment"]
    ),
    "field": _make_vec(
        # Fails means_persistent_flow, collects_rather_than_radiates, means_present_moment (tsr_formal_port.py l. 140)
        COMMON_NONPHYS
    ),
    "stream": _make_vec(
        # Flows and collects, but fails means_present_moment (tsr_formal_port.py l. 142)
        COMMON_NONPHYS + ["means_persistent_flow", "collects_rather_than_radiates"]
    ),
    "intention": _make_vec(
        # Executive/planned aim: fails receptive_non_forcing (carries Focus/planning strain) and means_pure_wanting
        ["not_center_whole_entity", "zero_travel_medium", "non_hierarchical", "unseparated_shared_medium", "flow_direction_out"]
    ),
    "compression": _make_vec(
        # Physical squeezing: fails not_physical_side_term, zero_travel_medium, receptive_non_forcing, means_pure_wanting
        ["not_center_whole_entity", "non_hierarchical", "unseparated_shared_medium"]
    ),
    # Additional TSR nonphysical pool words that A3 shuffles into our 14 core slots
    "rise per Expansion": _make_vec(COMMON_NONPHYS),
    "conscious energy": _make_vec(COMMON_NONPHYS),
    "imagination": _make_vec(COMMON_NONPHYS + ["flow_direction_in"]),
    "resonance": _make_vec(COMMON_NONPHYS + ["oscillatory_difference_root"]),
    "Attraction": _make_vec(
        ["not_physical_side_term", "zero_travel_medium", "receptive_non_forcing", "non_hierarchical", "unseparated_shared_medium"]
    ),
    "Vortex": _make_vec(COMMON_NONPHYS + ["collects_rather_than_radiates"]),
    "Out For": _make_vec(COMMON_NONPHYS + ["flow_direction_out"]),
    "In To": _make_vec(COMMON_NONPHYS + ["flow_direction_in"]),
    # Physical terms used when A3-S swaps physical words onto the nonphysical side
    "speed of light c": _make_vec(["non_hierarchical", "unseparated_shared_medium"]),
    "mass m": _make_vec(["non_hierarchical", "unseparated_shared_medium", "means_self_contained_part"]),
    "time": _make_vec(["non_hierarchical", "unseparated_shared_medium"]),
    "space": _make_vec(["non_hierarchical", "unseparated_shared_medium"]),
    "force": _make_vec(["non_hierarchical", "unseparated_shared_medium"]),
    "acceleration": _make_vec(["non_hierarchical", "unseparated_shared_medium"]),
    "Focus": _make_vec(["non_hierarchical", "unseparated_shared_medium"]),
    "gravitational lensing": _make_vec(["non_hierarchical", "unseparated_shared_medium"]),
    "density": _make_vec(["non_hierarchical", "unseparated_shared_medium"]),
    "volume": _make_vec(["non_hierarchical", "unseparated_shared_medium"]),
    "electric": _make_vec(["non_hierarchical", "unseparated_shared_medium"]),
    "magnetic": _make_vec(["non_hierarchical", "unseparated_shared_medium"]),
    "Now": _make_vec(["non_hierarchical", "unseparated_shared_medium", "means_present_moment", "flow_direction_out"]),
    "Expectation": _make_vec(["non_hierarchical", "unseparated_shared_medium", "flow_direction_in"]),
}

assert not CANDIDATES["Focus"]["selects_receptivity_target"]
assert not CANDIDATES["electric"]["means_poised_at_rest"]
assert not CANDIDATES["magnetic"]["means_returning_closed_loop"]

CAND_NAMES: list[str] = list(CANDIDATES.keys())
CAND_IDX: dict[str, int] = {w: i for i, w in enumerate(CAND_NAMES)}

# Slot-by-slot required features (hand-written knowing the target Map terms, with SM v57 justifications)
SLOT_REQUIREMENTS: dict[str, list[tuple[str, str]]] = {
    "Current": [
        ("not_physical_side_term", "Current_must_belong_to_nonphysical_side"),
        ("receptive_non_forcing", "Current_is_receptive_not_forcing"),
        ("non_hierarchical", "Current_has_no_rank_or_being_above (Ch.3, Ch.16 p.123)"),
        ("means_persistent_flow", "Current_must_mean_a_continuous_flow (Ch.16 p.123)"),
        ("collects_rather_than_radiates", "Current_collects_rather_than_radiating_from_a_source (Ch.16 p.123)"),
        ("means_present_moment", "Current_must_mean_the_present_moment (Ch.16 p.123, p.125)"),
        ("flow_direction_in", "Current_aligns_with_inward_returning_flow_across_from_Past (Ch.6 p.48, Ch.16 p.124)"),
    ],
    "Movement": [
        ("not_physical_side_term", "Movement_must_belong_to_nonphysical_side"),
        ("not_center_whole_entity", "Movement_cannot_consume_the_two_sided_soul_entity (Ch.16 p.123)"),
        ("means_motion_receptivity", "Movement_must_mean_receptivity_to_change_in_motion (Ch.16 p.123)"),
        ("means_self_contained_part", "Movement_must_mean_a_discrete_particular_part_of_a_whole (Map p.175)"),
    ],
    "Expansion": [
        ("not_physical_side_term", "Expansion_must_belong_to_nonphysical_side"),
        ("irreversible_cumulative_growth", "Expansion_must_grow_irreversibly_for_The_Knife_and_Dilation (Ch.14, Ch.16 p.123)"),
        ("continuum_unfolding_sense", "Expansion_names_unbounded_continuum_unfolding_rather_than_organismal_lifecycle"),
        ("!flow_direction_out", "Expansion_is_the_time_axis_not_purely_the_Future_rim_arrow"),
    ],
    "Vibration": [
        ("not_physical_side_term", "Vibration_must_belong_to_nonphysical_side"),
        ("zero_travel_medium", "Vibration_cannot_invoke_a_physical_lens_or_ray_travel (Ch.16 p.122)"),
        ("unseparated_shared_medium", "Vibration_cannot_enclose_private_mental_separation (Ch.16 p.123)"),
        ("oscillatory_difference_root", "Vibration_must_ground_Frequency_and_Vibrance (Ch.16 p.123, p.125)"),
        ("!change_is_felt_emotion", "Vibration_is_the_axis_not_the_felt_Frequency_product"),
        ("!means_vibration_extent", "Vibration_is_the_axis_not_3D_Vibrance_volume"),
    ],
    "Frequency": [
        ("not_physical_side_term", "Frequency_must_belong_to_nonphysical_side"),
        ("receptive_non_forcing", "Frequency_cannot_be_willpower_or_physical_forcing (Ch.16 p.124)"),
        ("oscillatory_difference_root", "Frequency_belongs_to_oscillatory_Vibration (Ch.16 p.123)"),
        ("change_is_felt_emotion", "Frequency_is_felt_emotional_evidence (Ch.8, Ch.16 p.124)"),
    ],
    "Appreciation": [
        ("not_physical_side_term", "Appreciation_must_belong_to_nonphysical_side"),
        ("means_rate_of_value_rise", "Appreciation_must_mean_acceleration_of_value_rise (Ch.8, Ch.16 p.124)"),
        ("means_gratitude_alignment", "Appreciation_must_carry_gratitude_sense_linking_yield_to_feeling (Ch.8, Ch.16 p.124)"),
    ],
    "Tune": [
        ("not_physical_side_term", "Tune_must_belong_to_nonphysical_side"),
        ("receptive_non_forcing", "Tune_is_receptive_agency_not_physical_Focus"),
        ("selects_receptivity_target", "Tune_must_select_a_station_preserving_free_will_at_product_gate (Ch.16 p.124)"),
    ],
    "Convergence": [
        ("not_physical_side_term", "Convergence_cannot_use_a_physical_side_term_like_Belief (Ch.16 p.122)"),
        ("zero_travel_medium", "Convergence_cannot_invoke_a_lens_traversed_by_traveling_rays (Ch.16 p.122)"),
        ("means_coming_together", "Convergence_must_mean_streams_coming_together (Ch.16 p.122)"),
        ("collects_rather_than_radiates", "Convergence_collects_through_a_Vortex"),
    ],
    "Desire": [
        ("not_physical_side_term", "Desire_must_belong_to_nonphysical_side"),
        ("zero_travel_medium", "Desire_has_no_spatial_squeezing_or_travel"),
        ("receptive_non_forcing", "Desire_is_wanting_stripped_of_physical_strain_and_forcing (Ch.6 p.46, Ch.10)"),
        ("means_pure_wanting", "Desire_must_mean_what_is_wanted_and_concentrated_wanting (Ch.16 p.125)"),
        ("flow_direction_out", "Desire_goes_Out_For_across_from_Belief (Ch.6 p.46, Ch.16 p.124)"),
    ],
    "Vibrance": [
        ("not_physical_side_term", "Vibrance_must_belong_to_nonphysical_side"),
        ("oscillatory_difference_root", "Vibrance_is_derived_from_Vibration_as_Volume_from_Space (Ch.2 p.26)"),
        ("means_vibration_extent", "Vibrance_must_mean_extent_fullness_of_vibration (Ch.2 p.26, Map p.176)"),
    ],
    "Idle": [
        ("not_physical_side_term", "Idle_must_belong_to_nonphysical_side"),
        ("means_poised_at_rest", "Idle_must_mean_poised_running_while_standing_still (Ch.2 p.27)"),
    ],
    "Reflected": [
        ("not_physical_side_term", "Reflected_must_belong_to_nonphysical_side"),
        ("means_returning_closed_loop", "Reflected_must_mean_bent_back_always_returning_closing_on_itself (Ch.2 p.27)"),
    ],
    "Future": [
        ("not_physical_side_term", "Future_must_belong_to_nonphysical_side"),
        ("irreversible_cumulative_growth", "Future_is_active_expansion_out_ahead (Ch.6 p.48, Ch.16 p.123)"),
        ("flow_direction_out", "Future_moves_outward_across_from_Now (Ch.16 p.124)"),
    ],
    "Intuition": [
        ("not_physical_side_term", "Intuition_must_belong_to_nonphysical_side"),
        ("means_direct_unlived_knowing", "Intuition_arrives_prior_to_lived_physical_experience (Ch.6 p.48)"),
        ("flow_direction_in", "Intuition_comes_In_To_across_from_Expectation (Ch.6 p.48, Ch.16 p.124)"),
    ],
}

# Only the 14 canonical + 16 explicit challengers form the primary 30-word candidate set
PRIMARY_30_POOL: list[str] = SLOTS + [
    "belief lens",
    "Vibrational Lens",
    "soul",
    "Source",
    "God",
    "eternity",
    "mind",
    "will",
    "growth",
    "surrender",
    "responsiveness",
    "gratitude",
    "field",
    "stream",
    "intention",
    "compression",
]
assert len(PRIMARY_30_POOL) == 30


def _build_single_word_pool() -> list[str]:
    ledger_path = REPO_ROOT / "proof" / "etymology" / "ledger_80.json"
    ledger_words = [
        w["word"] for w in json.loads(ledger_path.read_text(encoding="utf-8"))["words"]
    ]
    pool = sorted(
        {
            w.lower()
            for w in (list(PRIMARY_30_POOL) + list(CURRENT_CANDIDATES.keys()) + ledger_words)
            if " " not in w
        }
    )
    assert len(pool) == 100, f"Expected 100 single-word candidates, got {len(pool)}"
    return pool


def _build_base_constraints(
    allowed_pool: list[str],
) -> tuple[list[z3.IntNumRef | z3.ArithRef], list[tuple[str, z3.BoolRef]]]:
    """
    Build labeled Z3 constraints `(label, expr)` for assigning each of the 14 SLOTS
    to a distinct candidate word in `allowed_pool`.
    """
    slot_vars = [z3.Int(f"slot_{s}") for s in SLOTS]
    allowed_ids = [CAND_IDX[w] for w in allowed_pool]
    labeled: list[tuple[str, z3.BoolRef]] = []

    # Domain restriction + injectivity ("Two rows would end up saying the same thing.", SM v57 Ch. 16 p. 124)
    for s_idx, s_name in enumerate(SLOTS):
        labeled.append(
            (
                f"domain_{s_name}",
                z3.Or([slot_vars[s_idx] == cid for cid in allowed_ids]),
            )
        )
    labeled.append(("injective_distinct_words_across_slots", z3.Distinct(slot_vars)))

    # Feature tables via Z3 cases over candidate IDs
    for s_idx, s_name in enumerate(SLOTS):
        sv = slot_vars[s_idx]
        for feat_spec, rule_label in SLOT_REQUIREMENTS[s_name]:
            negated = feat_spec.startswith("!")
            feat_name = feat_spec[1:] if negated else feat_spec
            satisfying_cids = [
                cid
                for cid in allowed_ids
                if CANDIDATES[CAND_NAMES[cid]][feat_name] != negated
            ]
            expr = (
                z3.Or([sv == cid for cid in satisfying_cids])
                if satisfying_cids
                else z3.BoolVal(False)
            )
            labeled.append((f"{s_name}:{rule_label}", expr))

    return slot_vars, labeled


def extract_verified_minimal_unsat_core(
    labeled_constraints: list[tuple[str, z3.BoolRef]],
) -> list[str]:
    """
    Extract an UNSAT core with Z3 and deterministically reduce it by deletion
    until it is provably 1-minimal (removing ANY single constraint yields SAT).
    """
    solver = z3.Solver()
    solver.set(unsat_core=True)
    by_label: dict[str, z3.BoolRef] = {}
    for label, expr in labeled_constraints:
        assert label not in by_label, f"Duplicate constraint label: {label}"
        by_label[label] = expr
        solver.assert_and_track(expr, label)

    assert solver.check() == z3.unsat, "Expected constraint set to be UNSAT!"
    active = sorted(str(t) for t in solver.unsat_core())

    # Deletion-based exact irreducibility pass
    idx = 0
    while idx < len(active):
        trial = active[:idx] + active[idx + 1 :]
        s_check = z3.Solver()
        for lbl in trial:
            s_check.add(by_label[lbl])
        if s_check.check() == z3.unsat:
            active = trial
        else:
            idx += 1

    # Final verification: core itself is UNSAT, and every (|core| - 1) subset is SAT
    s_full = z3.Solver()
    for lbl in active:
        s_full.add(by_label[lbl])
    assert s_full.check() == z3.unsat
    for drop_i in range(len(active)):
        sub = active[:drop_i] + active[drop_i + 1 :]
        s_sub = z3.Solver()
        for lbl in sub:
            s_sub.add(by_label[lbl])
        assert s_sub.check() == z3.sat, f"Core was not minimal at {active[drop_i]}"

    return active


def verify_tsr_sat_and_uniqueness() -> dict[str, Any]:
    # 1. Pre-continuum-tiebreak check: verifies SM Ch. 16 p. 124 ("growth is what Expansion already means")
    slot_vars_pre, labeled_pre = _build_base_constraints(PRIMARY_30_POOL)
    s_pre = z3.Solver()
    for lbl, expr in labeled_pre:
        if "continuum_unfolding" not in lbl:
            s_pre.add(expr)
    pre_solutions: list[dict[str, str]] = []
    while s_pre.check() == z3.sat:
        m_pre = s_pre.model()
        sol = {SLOTS[i]: CAND_NAMES[m_pre.eval(slot_vars_pre[i]).as_long()] for i in range(len(SLOTS))}
        pre_solutions.append(sol)
        s_pre.add(z3.Or([slot_vars_pre[i] != m_pre.eval(slot_vars_pre[i]) for i in range(len(SLOTS))]))
    assert len(pre_solutions) == 2, f"Expected exactly 2 pre-tiebreak solutions, got {len(pre_solutions)}"
    expected_canonical = {s: s for s in SLOTS}
    expected_growth = dict(expected_canonical, Expansion="growth")
    assert expected_canonical in pre_solutions and expected_growth in pre_solutions, (
        f"Expected pre-tiebreak solutions {{A0, A0[Expansion:=growth]}}, got {pre_solutions}"
    )

    # 2. Full constraint check including continuum-unfolding sense
    slot_vars, labeled = _build_base_constraints(PRIMARY_30_POOL)
    solver = z3.Solver()
    for _lbl, expr in labeled:
        solver.add(expr)

    assert solver.check() == z3.sat, "Canonical TSR vocabulary must be SAT!"
    m = solver.model()
    found = {
        SLOTS[i]: CAND_NAMES[m.eval(slot_vars[i]).as_long()]
        for i in range(len(SLOTS))
    }
    assert found == expected_canonical, f"Expected canonical TSR {expected_canonical}, got {found}"

    # Block ONLY this solution to test global uniqueness across all P(30, 14) = 4.28e18 injective assignments!
    solver.add(
        z3.Or(
            [
                slot_vars[i] != CAND_IDX[SLOTS[i]]
                for i in range(len(SLOTS))
            ]
        )
    )
    second_status = solver.check()
    assert second_status == z3.unsat, "Canonical TSR assignment must be globally unique!"

    return {
        "candidate_pool_size": len(PRIMARY_30_POOL),
        "slot_count": len(SLOTS),
        "injective_search_space": "4284987369062400000",  # 30! / 16!
        "physical_control_flags_cleaned": {
            "Focus_selects_receptivity_target": CANDIDATES["Focus"]["selects_receptivity_target"],
            "electric_means_poised_at_rest": CANDIDATES["electric"]["means_poised_at_rest"],
            "magnetic_means_returning_closed_loop": CANDIDATES["magnetic"]["means_returning_closed_loop"],
        },
        "pre_continuum_tiebreak_solutions_count": len(pre_solutions),
        "pre_continuum_tiebreak_note": (
            "Without continuum_unfolding_sense on Expansion, exactly 2 of 4.28e18 assignments survive: "
            "A0 and A0[Expansion := growth], matching SM v57 Ch.16 p.124 ('growth is what Expansion already means')."
        ),
        "canonical_tsr_sat": True,
        "unique_solution": True,
        "recovered_assignment": found,
    }


CHALLENGER_SWAPS: list[tuple[str, str, str, str]] = [
    ("C01_belief_lens", "Convergence", "belief lens", "SM Ch.16 p.122 (2020 draft error #1)"),
    ("C02_vibrational_lens", "Convergence", "Vibrational Lens", "SM Ch.16 p.122 (draft error #2)"),
    ("C03_soul_for_Movement", "Movement", "soul", "SM Ch.16 p.123"),
    ("C04_Source_for_Current", "Current", "Source", "SM Ch.16 p.123"),
    ("C05_God_for_Current", "Current", "God", "SM Ch.16 p.123"),
    ("C06_eternity_for_Expansion", "Expansion", "eternity", "SM Ch.16 p.123"),
    ("C07_mind_for_Vibration", "Vibration", "mind", "SM Ch.16 p.123"),
    ("C08_will_for_Frequency", "Frequency", "will", "SM Ch.16 p.124"),
    ("C09_growth_for_Appreciation", "Appreciation", "growth", "SM Ch.16 p.124"),
    ("C10_surrender_for_Tune", "Tune", "surrender", "SM Ch.16 p.124"),
    ("C11_responsiveness_for_Movement", "Movement", "responsiveness", "SM Ch.2 / Map p.175"),
    ("C12_gratitude_for_Appreciation", "Appreciation", "gratitude", "SM Ch.8 & Ch.16 p.125"),
    ("C13_field_for_Current", "Current", "field", "tsr_formal_port.py l.140"),
    ("C14_stream_for_Current", "Current", "stream", "tsr_formal_port.py l.142"),
    ("C15_intention_for_Desire", "Desire", "intention", "SM Ch.6 p.46 & Ch.10"),
    ("C16_compression_for_Desire", "Desire", "compression", "SM Ch.2 p.26"),
]


def run_challenger_mucs() -> list[dict[str, Any]]:
    slot_vars, base_labeled = _build_base_constraints(PRIMARY_30_POOL)
    slot_to_idx = {s: i for i, s in enumerate(SLOTS)}
    results: list[dict[str, Any]] = []

    for test_id, slot_name, word, citation in CHALLENGER_SWAPS:
        s_i = slot_to_idx[slot_name]
        forced = (
            f"force_swap:{slot_name}:={word}",
            slot_vars[s_i] == CAND_IDX[word],
        )
        muc = extract_verified_minimal_unsat_core(base_labeled + [forced])
        all_violated = [
            f"{slot_name}:{rule_lbl}"
            for feat_spec, rule_lbl in SLOT_REQUIREMENTS[slot_name]
            if CANDIDATES[word][feat_spec[1:] if feat_spec.startswith("!") else feat_spec]
            == feat_spec.startswith("!")
        ]
        results.append(
            {
                "test_id": test_id,
                "slot": slot_name,
                "challenger_word": word,
                "citation": citation,
                "result": "unsat",
                "minimal_unsatisfiable_core": muc,
                "core_size": len(muc),
                "all_violated_slot_axioms": all_violated,
            }
        )

    # Also test Ch. 16 p. 124 time-pair swap (Future <-> Current across Now / Past)
    time_swap = [
        ("force_swap:Future:=Current", slot_vars[slot_to_idx["Future"]] == CAND_IDX["Current"]),
        ("force_swap:Current:=Future", slot_vars[slot_to_idx["Current"]] == CAND_IDX["Future"]),
    ]
    muc_time = extract_verified_minimal_unsat_core(base_labeled + time_swap)
    results.append(
        {
            "test_id": "C17_time_pair_swap_Future_Current",
            "slot": "Future <-> Current",
            "challenger_word": "Current / Future swapped",
            "citation": "SM Ch.16 p.124 ('Put the Future across from the Past')",
            "result": "unsat",
            "minimal_unsatisfiable_core": muc_time,
            "core_size": len(muc_time),
        }
    )

    return results


# Physical anchor for each of the 14 slots so we can read the exact A3-1..3 and A3-S mappings
SLOT_PHYS_ANCHOR: dict[str, str] = {
    "Current": "speed of light c",
    "Movement": "mass m",
    "Expansion": "time",
    "Vibration": "space",
    "Frequency": "force",
    "Appreciation": "acceleration",
    "Tune": "Focus",
    "Convergence": "gravitational lensing",
    "Desire": "density",
    "Vibrance": "volume",
    "Idle": "electric",
    "Reflected": "magnetic",
    "Future": "Now",
    "Intuition": "Expectation",
}


def run_a3_control_mucs() -> list[dict[str, Any]]:
    slot_vars, base_labeled = _build_base_constraints(CAND_NAMES)
    slot_to_idx = {s: i for i, s in enumerate(SLOTS)}

    arms = [
        build_arm_a3_permutation("A3-1", seed=101),
        build_arm_a3_permutation("A3-2", seed=202),
        build_arm_a3_permutation("A3-3", seed=303),
        build_arm_a3_swap_sides(),
    ]

    out: list[dict[str, Any]] = []
    for arm in arms:
        # Build physical -> mapped word lookup from arm.mirror + arm.extended_partners
        phys_map: dict[str, str] = {}
        for phys, non, _role in arm.mirror:
            phys_map.setdefault(phys, non)
        for phys, non in arm.extended_partners.items():
            phys_map.setdefault(phys, non)

        arm_assignments: dict[str, str] = {}
        forced_constraints: list[tuple[str, z3.BoolRef]] = []
        broken_slots_count = 0

        for s_name in SLOTS:
            phys_key = SLOT_PHYS_ANCHOR[s_name]
            mapped_word = phys_map[phys_key]
            if mapped_word == "Movement M":
                mapped_word = "Movement"
            assert mapped_word in CAND_IDX, f"Unregistered A3 word '{mapped_word}' in {arm.arm_id}"
            arm_assignments[s_name] = mapped_word
            forced_constraints.append(
                (
                    f"{arm.arm_id}_assign:{s_name}:={mapped_word}",
                    slot_vars[slot_to_idx[s_name]] == CAND_IDX[mapped_word],
                )
            )
            # Check individual slot compatibility against SLOT_REQUIREMENTS
            reqs_ok = all(
                CANDIDATES[mapped_word][fs[1:] if fs.startswith("!") else fs]
                != fs.startswith("!")
                for fs, _lbl in SLOT_REQUIREMENTS[s_name]
            )
            if not reqs_ok:
                broken_slots_count += 1

        muc = extract_verified_minimal_unsat_core(base_labeled + forced_constraints)
        out.append(
            {
                "arm_id": arm.arm_id,
                "seed": arm.metadata.get("seed"),
                "result": "unsat",
                "broken_slots_out_of_14": broken_slots_count,
                "sample_minimal_unsatisfiable_core": muc,
                "core_size": len(muc),
                "slot_assignments": arm_assignments,
            }
        )

    return out


# =============================================================================================
# Stem-Stripped Discrete-Sense Lexicon Specifications Covering ALL 14 Slots of Chapter 16
# =============================================================================================
# Epistemic clarification: The per-slot concept keyword groups below were written by hand
# knowing the 14 target words in The Sovereign Mirror (v57); they are NOT "blind" to the
# targets. What is automated and non-circular in the dictionary intersection helpers is:
# (1) zero hand-coded per-word booleans are used during lookup, (2) zero character-window
# parameters are tuned on discrete senses, (3) ORIGIN etymology is stripped before lowercasing
# in Oxford, and (4) `_validate_noncircular_slot_specs` asserts zero target-word stem
# self-matching across all 14 slots.
# Every concept group is a set of whole lowercase words. A discrete dictionary sense matches a
# query `groups: list[set[str]]` iff EVERY set in `groups` intersects that discrete sense's
# whole-word token set.

DUAL_SENSE_POLYSEMY_SPECS: list[tuple[str, str, str, list[set[str]], list[set[str]]]] = [
    (
        "Current",
        "current",
        "SM Ch.16 pp.123, 125 ('Current already meant both a flow and the present moment')",
        [{"flow", "flowing", "stream", "river", "water", "electricity"}],
        [{"present", "now"}, {"time", "moment", "occurring", "happening", "belonging"}],
    ),
    (
        "Appreciation",
        "appreciat",
        "SM Ch.8 & Ch.16 pp.124-125 ('Appreciation already meant both an increase in value and gratitude')",
        [{"gratitude", "grateful", "thankful"}],
        [{"increase", "increasing", "rise", "rising", "gain"}, {"value", "worth", "price", "monetary"}],
    ),
    (
        "Movement",
        "move",
        "SM v57 pp. 21, 31, Ch. 16 p. 123 & Map p. 175 ('Receptivity to change in motion; a self-contained part of the whole, like a movement in a symphony.')",
        [{"motion", "location", "position"}],
        [{"part", "division", "section"}, {"symphony", "sonata", "musical", "music", "concerto"}],
    ),
    (
        "Idle",
        "idl",
        "SM Ch.2 p.27 & Ch.16 p.125 ('Idle already meant running while standing still': inactive + engine running disconnected)",
        [
            {"inactive", "inaction", "unemployed", "unused", "lazy", "not"},
            {"inactive", "inaction", "unemployed", "unused", "lazy", "active", "action", "working", "work", "use"},
        ],
        [{"engine", "motor", "mechanism", "disconnected"}, {"run", "running", "disconnected", "gear", "state"}],
    ),
    (
        "Tune",
        "tun",
        "SM Ch.16 p.124 ('tuning selects. It picks the station': musical melody/pitch + radio receiver frequency adjustment)",
        [{"melody", "pitch", "pitches", "harmony", "notes"}],
        [{"adjust", "adjustment"}, {"radio", "receiver", "frequency", "signal", "circuit"}],
    ),
    (
        "Vibration",
        "vibrat",
        "SM Ch.8 & Ch.16 pp.123-124 (physical oscillation/periodic wave + felt emotional aura/state)",
        [{"oscillation", "oscillations", "periodic", "wave", "waves", "equilibrium"}],
        [{"emotional", "emotion", "aura", "atmosphere", "feelings"}],
    ),
    (
        "Reflected",
        "reflect",
        "SM Ch.2 p.27, Ch.16 p.125 & Book Title (wave/ray thrown or bent back from a surface + image seen in a mirror)",
        [{"throw", "thrown", "throwing", "bend", "bent", "cast", "sent"}, {"back", "surface", "light", "sound", "heat"}],
        [{"image", "likeness"}, {"show", "seen", "mirror", "mirrored", "surface", "reversed"}],
    ),
]

SINGLE_SENSE_DOMAIN_SPECS: list[tuple[str, str, str, list[set[str]]]] = [
    (
        "Expansion",
        "expan",
        "SM Ch.14 & Ch.16 pp.123-124 (increasing/becoming larger in size, volume, or scope; growth survives prior to continuum tiebreak)",
        [{"increase", "increasing", "larger", "bigger", "extensive"}, {"size", "volume", "scope", "quantity", "larger", "extensive"}],
    ),
    (
        "Frequency",
        "frequen",
        "SM Ch.8 & Ch.16 p.123 (rate/number of repeated occurrences or cycles per period of time)",
        [{"rate", "number"}, {"occurrences", "occurs", "repeated", "cycles"}, {"time", "period", "second"}],
    ),
    (
        "Convergence",
        "converg",
        "SM Ch.16 p.122 & Map p.174 (streams/lines coming together or meeting)",
        [{"come", "coming", "move", "draw", "meet", "tend"}, {"together", "closer", "currents", "airflows", "lines"}],
    ),
    (
        "Desire",
        "desir",
        "SM Ch.6 p.46 & Ch.16 p.125 (strong feeling or inclination of wanting/wishing)",
        [{"want", "wanting", "wish", "wishing"}, {"feeling", "inclination", "strongly", "strong"}],
    ),
    (
        "Vibrance",
        "vibran",
        "SM Ch.2 p.26 & Map p.176 (fullness of energy/life or resonant strength/sonority of sound)",
        [{"resonance", "resonant", "sonority", "full", "richness"}, {"sound", "energy", "life", "loud", "voice"}],
    ),
    (
        "Future",
        "futur",
        "SM Ch.6 p.48 & Ch.16 pp.123-124 (time yet to come / following the present)",
        [{"time"}, {"come", "coming", "following", "later", "ahead", "yet"}],
    ),
    (
        "Intuition",
        "intuit",
        "SM Ch.6 p.48 & Map p.175 (immediate/instinctive knowing or understanding without conscious/rational reasoning)",
        [{"instinctive", "immediately"}, {"knowing", "understand", "knows"}, {"without", "rather"}, {"rational", "reasoning"}],
    ),
]

WINDOW_SWEEP_WIDTHS: list[int] = [40, 60, 80, 100]


def _validate_noncircular_slot_specs() -> None:
    dual_names = [s[0] for s in DUAL_SENSE_POLYSEMY_SPECS]
    single_names = [s[0] for s in SINGLE_SENSE_DOMAIN_SPECS]
    assert len(dual_names) == 7 and len(single_names) == 7
    assert set(dual_names).isdisjoint(set(single_names))
    assert set(dual_names) | set(single_names) == set(SLOTS), (
        "Lexicon audit specifications must partition all 14 Chapter 16 nonphysical slots!"
    )
    for slot_name, forbidden_stem, _cite, sa, sb in DUAL_SENSE_POLYSEMY_SPECS:
        for grp in sa + sb:
            for tok in grp:
                assert not tok.startswith(forbidden_stem), (
                    f"Circular target-stem token '{tok}' forbidden in {slot_name}!"
                )
    for slot_name, forbidden_stem, _cite, sa in SINGLE_SENSE_DOMAIN_SPECS:
        for grp in sa:
            for tok in grp:
                assert not tok.startswith(forbidden_stem), (
                    f"Circular target-stem token '{tok}' forbidden in {slot_name}!"
                )


_validate_noncircular_slot_specs()


def _tokenize_whole_words(text: str) -> set[str]:
    return set(re.findall(r"[a-z]+", text.lower()))


def _sense_matches_groups(sense_tokens: set[str], groups: list[set[str]]) -> bool:
    return all(bool(sense_tokens & g) for g in groups)


def _format_groups(groups: list[set[str]]) -> list[list[str]]:
    return [sorted(g) for g in groups]


def _match_uniform_char_gap_window(text: str, groups: list[set[str]], max_char_gap: int) -> bool:
    """
    Evaluate whether whole-word tokens from every concept group in `groups` co-occur within
    uniform character gap `max_char_gap` (`max_token_start - min_token_end <= max_char_gap`),
    used solely for the uniform `[40, 60, 80, 100]` sensitivity sweep on unsplit Oxford text.
    """
    tokens = [(m.group(0), m.start(), m.end()) for m in re.finditer(r"[a-z]+", text)]
    if len(groups) == 1:
        g0 = groups[0]
        return any(tok in g0 for tok, _, _ in tokens)
    per_group = [[(s, e) for tok, s, e in tokens if tok in g] for g in groups]
    if any(not g_hits for g_hits in per_group):
        return False
    for combo in itertools.product(*per_group):
        char_gap = max(s for s, _ in combo) - min(e for _, e in combo)
        if char_gap <= max_char_gap:
            return True
    return False


def verify_wordnet_synset_polysemy() -> dict[str, Any]:
    """
    Cross-platform, OS-independent discrete-synset lexicon audit over genuine Princeton
    WordNet 3.0 synset definitions (`proof/z3/wordnet_100_synsets.json`, SHA-256 verified)
    across all 100 single-word candidates and all 14 nonphysical slots of Chapter 16.
    Per-slot keyword groups were written by hand knowing the target words; the lookup
    helper uses zero character-window parameters, zero hand-coded per-word booleans, and
    enforces zero target-stem circularity.
    """
    assert WORDNET_SYNSETS_PATH.exists(), f"Missing WordNet synset artifact: {WORDNET_SYNSETS_PATH}"
    raw_bytes = WORDNET_SYNSETS_PATH.read_bytes()
    artifact_file_sha256 = hashlib.sha256(raw_bytes).hexdigest()
    artifact = json.loads(raw_bytes.decode("utf-8"))

    meta = artifact["metadata"]
    words_map: dict[str, list[dict[str, Any]]] = artifact["words"]

    # Verify cryptographic provenance of the committed Princeton WordNet 3.0 payload
    canonical_payload = json.dumps(words_map, sort_keys=True, separators=(",", ":")).encode("utf-8")
    computed_payload_sha256 = hashlib.sha256(canonical_payload).hexdigest()
    assert computed_payload_sha256 == meta["synsets_payload_sha256"] == EXPECTED_WORDNET_PAYLOAD_SHA256, (
        "WordNet synset payload SHA-256 mismatch!"
    )
    assert meta["upstream_archive_sha256"] == EXPECTED_WORDNET_ARCHIVE_SHA256

    pool = _build_single_word_pool()
    assert sorted(words_map.keys()) == pool, "WordNet artifact word keys must match the 100-word pool!"

    # Optional live cross-check if nltk + WordNet 3.0 corpus happens to be installed on the runner
    live_nltk_crosscheck = "not_installed_using_sha256_verified_wordnet_3_0_artifact"
    if importlib.util.find_spec("nltk") is not None:
        try:
            from nltk.corpus import wordnet as nltk_wn  # type: ignore[import-not-found]

            sample_ids = sorted(
                f"{ss.offset():08d}-{ss.pos()}" for ss in nltk_wn.synsets("current")
            )
            artifact_ids = sorted(s["synset_id"] for s in words_map["current"])
            if sample_ids == artifact_ids:
                live_nltk_crosscheck = "verified_identical_against_live_nltk_wordnet"
            else:
                live_nltk_crosscheck = "live_nltk_wordnet_version_differs_using_pinned_3_0_artifact"
        except LookupError:
            live_nltk_crosscheck = "nltk_present_corpus_not_downloaded_using_sha256_verified_artifact"

    synset_tokens: dict[str, list[tuple[str, str, set[str]]]] = {
        w: [
            (s["synset_id"], s["nltk_name"], _tokenize_whole_words(s["definition"]))
            for s in words_map[w]
        ]
        for w in pool
    }
    resolved_count = sum(1 for w in pool if synset_tokens[w])
    assert resolved_count == 99, f"Expected 99/100 resolved WordNet words, got {resolved_count}"

    dual_results: dict[str, Any] = {}
    for slot_name, _stem, citation, sa, sb in DUAL_SENSE_POLYSEMY_SPECS:
        hits_a: list[str] = []
        hits_b: list[str] = []
        witness_synsets: dict[str, dict[str, list[str]]] = {}
        for w in pool:
            matched_a = [
                f"{sid} ({nname})"
                for sid, nname, toks in synset_tokens[w]
                if _sense_matches_groups(toks, sa)
            ]
            matched_b = [
                f"{sid} ({nname})"
                for sid, nname, toks in synset_tokens[w]
                if _sense_matches_groups(toks, sb)
            ]
            if matched_a:
                hits_a.append(w)
            if matched_b:
                hits_b.append(w)
            if matched_a and matched_b:
                witness_synsets[w] = {
                    "sense_A_synsets": matched_a,
                    "sense_B_synsets": matched_b,
                }
        inter = [w for w in pool if w in hits_a and w in hits_b]
        assert slot_name.lower() in inter, (
            f"Canonical word '{slot_name.lower()}' missing from WordNet intersection on {slot_name}: {inter}"
        )
        assert 1 <= len(inter) <= 4, (
            f"Unexpected WordNet survivor count on {slot_name}: {inter}"
        )
        dual_results[slot_name] = {
            "citation": citation,
            "sense_A_concept_groups": _format_groups(sa),
            "sense_B_concept_groups": _format_groups(sb),
            "sense_A_hit_count": len(hits_a),
            "sense_B_hit_count": len(hits_b),
            "intersection_words": inter,
            "matching_synset_witnesses": witness_synsets,
        }

    single_results: dict[str, Any] = {}
    for slot_name, _stem, citation, sa in SINGLE_SENSE_DOMAIN_SPECS:
        hits: list[str] = []
        witness_synsets_single: dict[str, list[str]] = {}
        for w in pool:
            matched = [
                f"{sid} ({nname})"
                for sid, nname, toks in synset_tokens[w]
                if _sense_matches_groups(toks, sa)
            ]
            if matched:
                hits.append(w)
                witness_synsets_single[w] = matched
        if slot_name != "Vibrance":
            assert slot_name.lower() in hits, (
                f"Canonical word '{slot_name.lower()}' missing from WordNet domain hits on {slot_name}: {hits}"
            )
        assert 1 <= len(hits) <= 5, (
            f"Unexpected WordNet single-sense survivor count on {slot_name}: {hits}"
        )
        entry: dict[str, Any] = {
            "citation": citation,
            "concept_groups": _format_groups(sa),
            "survivor_count": len(hits),
            "survivor_words": hits,
            "matching_synset_witnesses": witness_synsets_single,
        }
        if slot_name == "Vibrance":
            entry["orthographic_headword_note"] = meta["unresolved_orthographic_note"]
        if slot_name == "Expansion":
            assert "growth" in hits and "expansion" in hits, (
                "WordNet Expansion domain check must candidly recover 'growth' alongside 'expansion'!"
            )
        single_results[slot_name] = entry

    return {
        "status": "verified_cross_platform_princeton_wordnet_3_0",
        "cross_platform_os_independent": True,
        "zero_window_size_parameters": True,
        "zero_hand_coded_word_booleans": True,
        "zero_target_stem_circularity_verified": True,
        "per_slot_keyword_groups_hand_written_knowing_targets": True,
        "artifact_path": str(WORDNET_SYNSETS_PATH.relative_to(REPO_ROOT)),
        "artifact_file_sha256": artifact_file_sha256,
        "synsets_payload_sha256": computed_payload_sha256,
        "upstream_wordnet_3_0_archive_sha256": meta["upstream_archive_sha256"],
        "live_nltk_crosscheck": live_nltk_crosscheck,
        "single_word_pool_size": len(pool),
        "resolved_words_count": resolved_count,
        "unresolved_words": meta["unresolved_words"],
        "total_synsets_evaluated": meta["total_synsets_extracted"],
        "slots_evaluated_total": len(SLOTS),
        "dual_sense_polysemy_slots_count": len(DUAL_SENSE_POLYSEMY_SPECS),
        "single_sense_domain_slots_count": len(SINGLE_SENSE_DOMAIN_SPECS),
        "polysemy_intersections": dual_results,
        "single_sense_domain_survivors": single_results,
    }


OXFORD_DISCRETE_SENSE_SPLIT_RE = re.compile(
    r"•|;|(?:\b(?:noun|verb|adjective|adverb)\b)|(?:(?<=[\.\s])(?:[1-9]|1[0-9])\s+)"
)


def _split_oxford_discrete_senses(pre_origin_text: str) -> list[set[str]]:
    """
    Split an ORIGIN-stripped macOS New Oxford American Dictionary entry strictly on
    discrete dictionary sense boundaries (`•`, `;`, POS headers, numbered senses)
    and extract whole-word tokens from each sense's definition clause (before any
    unparenthesized `: usage example`), with ZERO character-window parameters.
    """
    body = pre_origin_text
    for trailing_sec in ("DERIVATIVES", "PHRASAL VERBS", "PHRASES"):
        body = body.split(trailing_sec)[0]
    m_pos = re.search(r"\b(?:noun|verb|adjective|adverb)\b", body)
    if m_pos:
        body = body[m_pos.start() :]

    senses: list[set[str]] = []
    for raw_sense in OXFORD_DISCRETE_SENSE_SPLIT_RE.split(body):
        no_paren_colon = re.sub(
            r"\([^)]*\)", lambda m: m.group(0).replace(":", " "), raw_sense
        )
        defn_clause = no_paren_colon.split(":")[0]
        toks = _tokenize_whole_words(defn_clause)
        if toks:
            senses.append(toks)
    return senses


def verify_blind_dictionary_polysemy(allow_coreservices: bool = True) -> dict[str, Any]:
    """
    Stem-stripped discrete-sense lexicon audit against macOS's local New Oxford American
    Dictionary (`CoreServices.DCSCopyTextDefinition`), stripping `ORIGIN` blocks BEFORE
    lowercasing so etymology cannot leak in, splitting strictly into discrete senses
    with ZERO window-size parameters across all 14 nonphysical slots, AND running an
    explicit uniform `[40, 60, 80, 100]` character-gap sensitivity sweep.
    Note: The historical identifier `verify_blind_dictionary_polysemy` is retained for
    caller compatibility; the per-slot keyword groups were written by hand knowing the
    target words, while the lookup helper uses zero per-word booleans and enforces zero
    target-stem self-matching.
    When `CoreServices` is unavailable (e.g. Linux/Windows CI), the polysemy intersection
    check executes deterministically against the checked-in cross-platform Princeton
    WordNet 3.0 payload (`wordnet_100_synsets.json`) with compatible schema keys.
    """
    cs_path = ctypes.util.find_library("CoreServices") if allow_coreservices else None
    cf_path = ctypes.util.find_library("CoreFoundation") if allow_coreservices else None
    if not cs_path or not cf_path:
        wn_fallback = verify_wordnet_synset_polysemy()
        return {
            "status": "macos_coreservices_unavailable_verified_via_cross_platform_wordnet_3_0",
            "macos_coreservices_available": False,
            "lexicon_source_used": "checked_in_princeton_wordnet_3_0_payload",
            "cross_platform_fallback_note": (
                "macOS CoreServices / New Oxford American Dictionary is unavailable on this OS; "
                "all 14-slot polysemy and domain-intersection checks ran deterministically against "
                "the checked-in cross-platform Princeton WordNet 3.0 payload (wordnet_100_synsets.json)."
            ),
            "cross_platform_wordnet_status": wn_fallback["status"],
            "cross_platform_wordnet_payload_sha256": wn_fallback["synsets_payload_sha256"],
            "zero_window_size_parameters_in_discrete_audit": wn_fallback["zero_window_size_parameters"],
            "zero_hand_coded_word_booleans": wn_fallback["zero_hand_coded_word_booleans"],
            "zero_target_stem_circularity_verified": wn_fallback["zero_target_stem_circularity_verified"],
            "per_slot_keyword_groups_hand_written_knowing_targets": True,
            "single_word_pool_size": wn_fallback["single_word_pool_size"],
            "resolved_entries_count": wn_fallback["resolved_words_count"],
            "unresolved_words": wn_fallback["unresolved_words"],
            "slots_evaluated_total": wn_fallback["slots_evaluated_total"],
            "dual_sense_polysemy_slots_count": wn_fallback["dual_sense_polysemy_slots_count"],
            "single_sense_domain_slots_count": wn_fallback["single_sense_domain_slots_count"],
            "polysemy_intersections": wn_fallback["polysemy_intersections"],
            "single_sense_domain_survivors": wn_fallback["single_sense_domain_survivors"],
        }

    cs = ctypes.CDLL(cs_path)
    cf = ctypes.CDLL(cf_path)

    class CFRange(ctypes.Structure):
        _fields_ = [("location", ctypes.c_long), ("length", ctypes.c_long)]

    cf.CFStringCreateWithCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32]
    cf.CFStringCreateWithCString.restype = ctypes.c_void_p
    cf.CFStringGetLength.argtypes = [ctypes.c_void_p]
    cf.CFStringGetLength.restype = ctypes.c_long
    cf.CFStringGetMaximumSizeForEncoding.argtypes = [ctypes.c_long, ctypes.c_uint32]
    cf.CFStringGetMaximumSizeForEncoding.restype = ctypes.c_long
    cf.CFStringGetCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long, ctypes.c_uint32]
    cf.CFStringGetCString.restype = ctypes.c_bool
    cs.DCSCopyTextDefinition.argtypes = [ctypes.c_void_p, ctypes.c_void_p, CFRange]
    cs.DCSCopyTextDefinition.restype = ctypes.c_void_p
    k_utf8 = 0x08000100

    def lookup_synchronic_pre_origin(word: str) -> str:
        cf_word = cf.CFStringCreateWithCString(None, word.encode("utf-8"), k_utf8)
        res = cs.DCSCopyTextDefinition(None, cf_word, CFRange(0, len(word)))
        if not res:
            return ""
        length = cf.CFStringGetLength(res)
        buf = ctypes.create_string_buffer(cf.CFStringGetMaximumSizeForEncoding(length, k_utf8) + 1)
        cf.CFStringGetCString(res, buf, len(buf), k_utf8)
        txt = buf.value.decode("utf-8", errors="replace")
        # Strip uppercase ORIGIN section BEFORE any lowercasing so etymology cannot leak in
        return txt.split("ORIGIN")[0]

    pool = _build_single_word_pool()
    raw_entries = {w: lookup_synchronic_pre_origin(w) for w in pool}
    non_empty = sum(1 for d in raw_entries.values() if d)
    assert non_empty >= 95, f"Expected >= 95 Oxford dictionary entries, got {non_empty}"

    discrete_senses = {w: _split_oxford_discrete_senses(raw_entries[w]) for w in pool}
    lowered_pre_origin = {
        w: raw_entries[w]
        .split("DERIVATIVES")[0]
        .split("PHRASAL VERBS")[0]
        .split("PHRASES")[0]
        .lower()
        for w in pool
    }

    dual_results: dict[str, Any] = {}
    window_sweep: dict[str, Any] = {}

    for slot_name, _stem, citation, sa, sb in DUAL_SENSE_POLYSEMY_SPECS:
        hits_a = [
            w for w in pool if any(_sense_matches_groups(s, sa) for s in discrete_senses[w])
        ]
        hits_b = [
            w for w in pool if any(_sense_matches_groups(s, sb) for s in discrete_senses[w])
        ]
        inter = [w for w in pool if w in hits_a and w in hits_b]
        assert slot_name.lower() in inter, (
            f"Canonical word '{slot_name.lower()}' missing from discrete Oxford intersection on {slot_name}: {inter}"
        )
        assert 1 <= len(inter) <= 4, (
            f"Unexpected discrete Oxford survivor count on {slot_name}: {inter}"
        )
        dual_results[slot_name] = {
            "citation": citation,
            "sense_A_concept_groups": _format_groups(sa),
            "sense_B_concept_groups": _format_groups(sb),
            "sense_A_hit_count": len(hits_a),
            "sense_B_hit_count": len(hits_b),
            "intersection_words": inter,
        }

        by_width: dict[str, list[str]] = {}
        for width in WINDOW_SWEEP_WIDTHS:
            w_inter = [
                w
                for w in pool
                if _match_uniform_char_gap_window(lowered_pre_origin[w], sa, width)
                and _match_uniform_char_gap_window(lowered_pre_origin[w], sb, width)
            ]
            assert slot_name.lower() in w_inter, (
                f"Canonical word '{slot_name.lower()}' missing at uniform window w={width} on {slot_name}"
            )
            by_width[str(width)] = w_inter
        is_invariant = len({tuple(v) for v in by_width.values()}) == 1
        assert is_invariant, f"Uniform window sweep was not invariant on {slot_name}: {by_width}"
        window_sweep[slot_name] = {
            "intersections_by_uniform_width": by_width,
            "invariant_across_40_60_80_100": is_invariant,
            "matches_discrete_sense_intersection": by_width["40"] == inter,
        }

    single_results: dict[str, Any] = {}
    for slot_name, _stem, citation, sa in SINGLE_SENSE_DOMAIN_SPECS:
        hits = [
            w for w in pool if any(_sense_matches_groups(s, sa) for s in discrete_senses[w])
        ]
        assert slot_name.lower() in hits, (
            f"Canonical word '{slot_name.lower()}' missing from discrete Oxford domain hits on {slot_name}: {hits}"
        )
        assert 1 <= len(hits) <= 5, (
            f"Unexpected discrete Oxford single-sense survivor count on {slot_name}: {hits}"
        )
        if slot_name == "Expansion":
            assert "growth" in hits and "expansion" in hits, (
                "Discrete Oxford Expansion check must candidly recover 'growth' alongside 'expansion'!"
            )
        single_results[slot_name] = {
            "citation": citation,
            "concept_groups": _format_groups(sa),
            "survivor_count": len(hits),
            "survivor_words": hits,
        }

    return {
        "status": "verified_live_macos_new_oxford_american_dictionary_discrete_senses",
        "macos_coreservices_available": True,
        "lexicon_source_used": "live_macos_new_oxford_american_dictionary",
        "origin_etymology_stripped_before_lowercase": True,
        "discrete_sense_delimiters": ["•", ";", "POS_header", "numbered_senses"],
        "zero_window_size_parameters_in_discrete_audit": True,
        "zero_hand_coded_word_booleans": True,
        "zero_target_stem_circularity_verified": True,
        "per_slot_keyword_groups_hand_written_knowing_targets": True,
        "single_word_pool_size": len(pool),
        "resolved_entries_count": non_empty,
        "slots_evaluated_total": len(SLOTS),
        "dual_sense_polysemy_slots_count": len(DUAL_SENSE_POLYSEMY_SPECS),
        "single_sense_domain_slots_count": len(SINGLE_SENSE_DOMAIN_SPECS),
        "polysemy_intersections": dual_results,
        "single_sense_domain_survivors": single_results,
        "window_sensitivity_sweep": {
            "uniform_widths_tested": WINDOW_SWEEP_WIDTHS,
            "all_slots_invariant_across_widths": all(
                v["invariant_across_40_60_80_100"] for v in window_sweep.values()
            ),
            "slots": window_sweep,
        },
    }


def verify_cross_platform_without_coreservices(
    baseline_wordnet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Self-test mocking `ctypes.util.find_library` -> `None` (simulating a Linux/Windows CI
    runner without macOS `CoreServices`) to guarantee that offline discrete-synset verification
    executes deterministically with full schema compatibility and never silently skips.
    """
    if baseline_wordnet is None:
        baseline_wordnet = verify_wordnet_synset_polysemy()

    orig_find_library = ctypes.util.find_library
    try:
        ctypes.util.find_library = lambda _name: None  # type: ignore[assignment]
        mocked_dict = verify_blind_dictionary_polysemy(allow_coreservices=True)
        mocked_wn = verify_wordnet_synset_polysemy()
    finally:
        ctypes.util.find_library = orig_find_library

    assert mocked_dict["macos_coreservices_available"] is False
    assert (
        mocked_dict["status"]
        == "macos_coreservices_unavailable_verified_via_cross_platform_wordnet_3_0"
    )
    assert mocked_dict["lexicon_source_used"] == "checked_in_princeton_wordnet_3_0_payload"
    assert mocked_dict["zero_window_size_parameters_in_discrete_audit"] is True
    assert mocked_dict["zero_hand_coded_word_booleans"] is True
    assert mocked_dict["zero_target_stem_circularity_verified"] is True
    assert mocked_dict["per_slot_keyword_groups_hand_written_knowing_targets"] is True
    assert mocked_dict["single_word_pool_size"] == baseline_wordnet["single_word_pool_size"] == 100
    assert mocked_dict["resolved_entries_count"] == baseline_wordnet["resolved_words_count"] == 99
    assert mocked_dict["slots_evaluated_total"] == len(SLOTS) == 14
    assert mocked_dict["dual_sense_polysemy_slots_count"] == 7
    assert mocked_dict["single_sense_domain_slots_count"] == 7
    assert mocked_dict["polysemy_intersections"] == baseline_wordnet["polysemy_intersections"]
    assert mocked_dict["single_sense_domain_survivors"] == baseline_wordnet["single_sense_domain_survivors"]
    assert mocked_wn == baseline_wordnet

    return {
        "simulated_linux_ci_coreservices_disabled": True,
        "did_silently_skip": False,
        "fallback_status": mocked_dict["status"],
        "lexicon_source_used": mocked_dict["lexicon_source_used"],
        "zero_hand_coded_word_booleans": mocked_dict["zero_hand_coded_word_booleans"],
        "zero_target_stem_circularity_verified": mocked_dict["zero_target_stem_circularity_verified"],
        "deterministic_match_with_wordnet_3_0_audit": True,
        "slots_verified_offline": mocked_dict["slots_evaluated_total"],
    }


def run_lexical_rigidity() -> dict[str, Any]:
    uniqueness = verify_tsr_sat_and_uniqueness()
    challengers = run_challenger_mucs()
    a3_controls = run_a3_control_mucs()
    wordnet_audit = verify_wordnet_synset_polysemy()
    blind_dict = verify_blind_dictionary_polysemy()
    offline_selftest = verify_cross_platform_without_coreservices(wordnet_audit)

    assert len(challengers) == 17
    assert all(c["result"] == "unsat" for c in challengers)
    assert len(a3_controls) == 4
    assert all(a["result"] == "unsat" and a["broken_slots_out_of_14"] >= 10 for a in a3_controls)

    return {
        "proof_id": "Part_II_B_Chapter16_Axiomatic_MUC_Audit_and_Discrete_Sense_Lexicon_Audit",
        "epistemic_scope": (
            "Following The Sovereign Mirror (v57, Note p. 9), 'the table borrows the shape of physics, "
            "not its authority.' All relation sets, CANDIDATES feature flags, SLOT_REQUIREMENTS rules, "
            "and per-slot keyword groups (DUAL_SENSE_POLYSEMY_SPECS / SINGLE_SENSE_DOMAIN_SPECS) were "
            "written by hand knowing the target words (they are NOT blind to the targets). What the Z3 "
            "proof establishes is: no two terms in the Map, as encoded, are interchangeable (unique "
            "assignment across 4.28e18 injective mappings and 21 deletion-verified 1-minimal UNSAT cores). "
            "In the dictionary-intersection helpers (`wordnet_synset_polysemy` and `blind_oxford_dictionary_polysemy` "
            "— key retained for schema compatibility), zero hand-coded per-word booleans are used in the "
            "lookup, zero window parameters are tuned on discrete senses, ORIGIN etymology is stripped "
            "before lowercasing in Oxford, and an automated stem check enforces zero target-word stem "
            "self-matching across all 14 slots; on non-macOS systems without CoreServices, the dictionary "
            "audit executes deterministically via the checked-in cross-platform WordNet 3.0 payload."
        ),
        "candidate_feature_flags_hand_written_knowing_targets": True,
        "per_slot_keyword_groups_hand_written_knowing_targets": True,
        "z3_version": z3.get_version_string(),
        "uniqueness_theorem": uniqueness,
        "wordnet_synset_polysemy": wordnet_audit,
        "blind_oxford_dictionary_polysemy": blind_dict,
        "cross_platform_offline_selftest": offline_selftest,
        "challenger_swap_certificates": challengers,
        "a3_floor_control_certificates": a3_controls,
    }


if __name__ == "__main__":
    report = run_lexical_rigidity()
    print(json.dumps(report, indent=2))
