"""
a3_shuffled.py - Arm A3: Shuffled TSR Floor Controls (`A3-1`, `A3-2`, `A3-3`, and `A3-S`).

Standalone public module providing the exact deterministic A3 floor-control vocabulary
permutations (`seed=101`, `seed=202`, `seed=303`) and global side-swap (`A3-S`) audited
by `proof/z3/lexical_rigidity.py`, depending solely on `vocab.mirror`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import random
import re
from typing import Any

from vocab.mirror import EXTENDED_PARTNERS, MIRROR


@dataclass
class ArmSpec:
    arm_id: str
    blind_label: str
    mirror: list[tuple[str, str, str]]
    extended_partners: dict[str, str]
    synonyms: dict[str, list[str]] = field(default_factory=dict)
    word_swaps: list[tuple[str, str]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


def _seeded_derangement(items: list[str], seed: int) -> dict[str, str]:
    rng = random.Random(seed)
    n = len(items)
    if n <= 1:
        return {x: x for x in items}
    for _ in range(500):
        perm = list(items)
        rng.shuffle(perm)
        if all(a != b for a, b in zip(items, perm)):
            return dict(zip(items, perm))
    return {items[i]: items[(i + 1) % n] for i in range(n)}


def _apply_word_perm(text: str, mapping: dict[str, str]) -> str:
    keys = sorted(mapping.keys(), key=len, reverse=True)
    out = text
    placeholders: dict[str, str] = {}
    for idx, k in enumerate(keys):
        ph = f"__PERM_{idx}__"
        placeholders[ph] = mapping[k]
        out = re.sub(rf"\b{re.escape(k)}\b", ph, out)
    for ph, val in placeholders.items():
        out = out.replace(ph, val)
    return out


def build_arm_a3_permutation(arm_id: str, seed: int) -> ArmSpec:
    quantity_pool = [
        "Movement M",
        "Vibrance",
        "Desire",
        "Vibration",
        "Expansion",
        "rise per Expansion",
        "Appreciation",
        "Frequency",
        "Current",
        "Idle",
        "Reflected",
        "conscious energy",
        "imagination",
    ]
    q_map = _seeded_derangement(quantity_pool, seed=seed)
    q_map["Movement"] = q_map["Movement M"].replace(" M", "")

    phenom_pool = ["resonance", "Attraction", "Vortex", "Convergence", "Tune", "Intuition"]
    p_map = _seeded_derangement(phenom_pool, seed=seed + 17)

    dir_pool = ["Out For", "In To", "Future"]
    d_map = _seeded_derangement(dir_pool, seed=seed + 31)

    prop_pool = ["limitless", "receptive", "collection"]
    pr_map = _seeded_derangement(prop_pool, seed=seed + 47)

    full_perm: dict[str, str] = {}
    for m in (q_map, p_map, d_map, pr_map):
        full_perm.update(m)

    perm_mirror = [
        (phys, _apply_word_perm(non, full_perm), role)
        for phys, non, role in MIRROR
    ]
    perm_ext = {
        phys: _apply_word_perm(non, full_perm)
        for phys, non in EXTENDED_PARTNERS.items()
    }
    perm_synonyms = {new_word: [new_word.lower()] for new_word in full_perm.values()}

    return ArmSpec(
        arm_id=arm_id,
        blind_label=f"Rule R, Vocabulary V, Calibration K (Arm {arm_id})",
        mirror=perm_mirror,
        extended_partners=perm_ext,
        synonyms=perm_synonyms,
        word_swaps=[(new_w, orig_w) for orig_w, new_w in full_perm.items()],
        metadata={
            "control_type": "shuffled_tsr_permutation",
            "seed": seed,
            "permutation_map": full_perm,
        },
    )


def build_arm_a3_swap_sides() -> ArmSpec:
    swapped_mirror = [(phys, phys, role) for phys, _non, role in MIRROR]
    swapped_ext = {phys: phys for phys in EXTENDED_PARTNERS.keys()}
    return ArmSpec(
        arm_id="A3-S",
        blind_label="Rule R, Vocabulary V, Calibration K (Arm A3-S)",
        mirror=swapped_mirror,
        extended_partners=swapped_ext,
        synonyms={phys: [phys.lower()] for phys, _, _ in swapped_mirror},
        metadata={"control_type": "swapped_sides_outright"},
    )
