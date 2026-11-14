"""
structural_rigidity.py — Part II.A: Unlabeled Graph Automorphism Group of TSR
=============================================================================
Uses Z3 (SMT solver) to compute the exact automorphism group Aut(S_TSR) of the
29 integer-indexed nonphysical + center nodes of The Present and The Map across
the full symmetric group S_29 (29! = 8,841,761,993,739,701,954,543,616,000,000),
passing zero English dictionary definitions to the solver.

Epistemic scope: Following The Sovereign Mirror (v57, A Note Before We Begin p. 9),
"the table borrows the shape of physics, not its authority." The 29-node graph
relations (both multi-node equations/links and unary directional/polarity
predicates in `_build_stage_relations`) were written by hand knowing the Map
terms. What the Z3 result establishes is: no two terms in the Map, as encoded,
are interchangeable (|Aut(S3)| = 1; all 29/29 nodes lie in singleton orbits).

Demonstrates a 3-stage symmetry-breaking cascade from the equations and diagram
geometry of The Sovereign Mirror (v57):
  - Stage S1 (Algebraic equations + Crossing V4 topology + Reality containment):
      |Aut(S1)| = 12  (≅ S_3 × Z_2; 21/29 nodes already have |orbit| = 1)
  - Stage S2 (+ Map p. 172 cross-row co-creation links: Tune->Attraction,
              Idle/Reflected->Momentum):
      |Aut(S2)| = 2   (≅ Z_2; 27/29 nodes have |orbit| = 1; only
                       Idle <-> Reflected duality remains)
  - Stage S3 (+ Ch. 2 pp. 26-27 stationary/poised Idle vs. returning/closed-loop
              Reflected polarity):
      |Aut(S3)| = 1   (Trivial group {id}; all 29/29 nodes have |orbit| = 1)

Also checks Global Two-Sided Asymmetry (UNSAT + Minimal Unsatisfiable Core):
no structure-preserving bijection of the encoded two-sided system can swap the
Physical and Nonphysical sectors because ρ_NP = 0 vs. ρ_P > 0 breaks mirror parity.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import z3

# 29 distinct unlabeled nodes (26 unique nonphysical concepts across the 28 MIRROR rows
# — recalling that 'Current' pairs with both 'Past' and 'speed of light c', and 'Desire'
# pairs with both 'Belief' and 'density' — plus the 3 co-created center properties).
NODES: list[str] = [
    # 0..2: Environmental properties
    "limitless",
    "receptive",
    "collection",
    # 3..5: Center co-created entity properties
    "Awareness",
    "Attraction",
    "Momentum",
    # 6..7: Realities
    "Collective Reality",
    "Vibrational Reality",
    # 8: Continuum
    "Vibration-Expansion",
    # 9: Evidence readout
    "emotional evidence",
    # 10..11: Outer rim energy flows
    "Future",
    "Current",
    # 12..13: Entity contrasts at the crossing
    "Desire",
    "Intuition",
    # 14: Particular symbol
    "Movement M",
    # 15: Crossing product gate
    "Tune",
    # 16..18: Co-creating partners (with Desire at index 12)
    "Idle",
    "Reflected",
    "Vibrance",
    # 19: Side energy
    "conscious energy",
    # 20: Side-wide transmutation
    "realization",
    # 21..22: Directional entity transmutations
    "Out For",
    "In To",
    # 23..28: Reflected mechanical & experiential partnerships
    "Vibration",
    "Expansion",
    "rise per Expansion",
    "Appreciation",
    "imagination",
    "Frequency",
]

IDX: dict[str, int] = {name: i for i, name in enumerate(NODES)}
N_NODES: int = len(NODES)
assert N_NODES == 29


def _build_stage_relations(stage: int) -> dict[str, Any]:
    """
    Build ground structural tuples for Stages 1, 2, 3 using integer node IDs only.
    Commutative binary products include both (b, c) and (c, b) so the solver is
    never handed factor ordering by fiat!
    """
    assert stage in (1, 2, 3)

    # Non-commutative quotient: x = num / den  (rise per Expansion = Vibration / Expansion)
    quotient3 = {(IDX["rise per Expansion"], IDX["Vibration"], IDX["Expansion"])}

    # Non-commutative rate of change: y = d(x)/d(t)  (Appreciation = rate(rise per Expansion, Expansion))
    rate3 = {(IDX["Appreciation"], IDX["rise per Expansion"], IDX["Expansion"])}

    # Commutative 2-factor products: z = x * y  (symmetric in the last two slots!)
    comm_prod3 = {
        (IDX["Movement M"], IDX["Desire"], IDX["Vibrance"]),
        (IDX["Movement M"], IDX["Vibrance"], IDX["Desire"]),
        (IDX["Frequency"], IDX["Movement M"], IDX["Appreciation"]),
        (IDX["Frequency"], IDX["Appreciation"], IDX["Movement M"]),
    }

    # Asymmetric rest-equivalence product: E = M * C^2 (linear factor M, squared factor C)
    energy_sq3 = {(IDX["conscious energy"], IDX["Movement M"], IDX["Current"])}

    # Dimensional power relation (Theorem 2.1): Vibrance = Vibration^d (pure Vibration extent)
    dim_power2 = {(IDX["Vibrance"], IDX["Vibration"])}

    # Continuum formed by (space-axis, time-axis) — symmetric in its 2 axes unless equations break it
    continuum_axes3 = {
        (IDX["Vibration-Expansion"], IDX["Vibration"], IDX["Expansion"]),
        (IDX["Vibration-Expansion"], IDX["Expansion"], IDX["Vibration"]),
    }

    # Evidence block reads Frequency
    evidence_reads2 = {(IDX["emotional evidence"], IDX["Frequency"])}

    # Crossing & Flow topology of The Present:
    #   Rim flows: Future (Out, Strong) -> Current (In, Weak)
    rim_out1 = {IDX["Future"]}
    rim_in1 = {IDX["Current"]}  # Structural join #1 with C in E = M * C^2!

    #   Crossing contrasts: Desire (Out, Strong) and Intuition (In, Weak)
    contrast_out_strong1 = {IDX["Desire"]}  # Structural join #2 with M = Desire * Vibrance!
    contrast_in_weak1 = {IDX["Intuition"]}

    #   Directional transmutation arrows carrying contrasts across E
    arrow_carries2 = {
        (IDX["Out For"], IDX["Desire"]),
        (IDX["In To"], IDX["Intuition"]),
    }

    #   Side transmutation spanning the outward + inward entity transmutations (unordered pair)
    transmutation_span3 = {
        (IDX["realization"], IDX["Out For"], IDX["In To"]),
        (IDX["realization"], IDX["In To"], IDX["Out For"]),
    }

    #   Weak-frequency experiential companion (Intuition and imagination, Map p. 171)
    weak_companion2 = {(IDX["imagination"], IDX["Intuition"])}

    #   Agency gate sitting on the crossing product of conscious energy (Ch. 17 p. 128)
    product_gate2 = {(IDX["Tune"], IDX["conscious energy"])}

    #   Reality containment (Collective outer whole -> Vibrational individual share, Ch. 6 p. 50)
    reality_contains2 = {(IDX["Collective Reality"], IDX["Vibrational Reality"])}

    #   Particular sits in the overlap of Collective and Vibrational Realities (Map p. 169, p. 171)
    particular_in_realities3 = {
        (IDX["Movement M"], IDX["Collective Reality"], IDX["Vibrational Reality"]),
        (IDX["Movement M"], IDX["Vibrational Reality"], IDX["Collective Reality"]),
    }

    #   Environmental properties co-creating center entity properties (Map p. 170)
    env_cocreates2 = {
        (IDX["limitless"], IDX["Awareness"]),
        (IDX["receptive"], IDX["Attraction"]),
        (IDX["collection"], IDX["Momentum"]),
    }

    #   Field-component partnership of Current (unordered pair {Idle, Reflected} -> Current, Ch. 2 p. 26)
    field_pair_of_current3 = {
        (IDX["Current"], IDX["Idle"], IDX["Reflected"]),
        (IDX["Current"], IDX["Reflected"], IDX["Idle"]),
    }

    rels: dict[str, Any] = {
        "quotient3": (3, quotient3),
        "rate3": (3, rate3),
        "comm_prod3": (3, comm_prod3),
        "energy_sq3": (3, energy_sq3),
        "dim_power2": (2, dim_power2),
        "continuum_axes3": (3, continuum_axes3),
        "evidence_reads2": (2, evidence_reads2),
        "rim_out1": (1, rim_out1),
        "rim_in1": (1, rim_in1),
        "contrast_out_strong1": (1, contrast_out_strong1),
        "contrast_in_weak1": (1, contrast_in_weak1),
        "arrow_carries2": (2, arrow_carries2),
        "transmutation_span3": (3, transmutation_span3),
        "weak_companion2": (2, weak_companion2),
        "product_gate2": (2, product_gate2),
        "reality_contains2": (2, reality_contains2),
        "particular_in_realities3": (3, particular_in_realities3),
        "env_cocreates2": (2, env_cocreates2),
        "field_pair_of_current3": (3, field_pair_of_current3),
    }

    if stage >= 2:
        # Map p. 172 cross-row co-creation links:
        #   Entity action: Tune (with Focus) -> Attraction
        #   Co-creating partners: Idle-Reflected (with Electro-Magnetic) -> Momentum
        rels["gate_cocreates_center2"] = (2, {(IDX["Tune"], IDX["Attraction"])})
        rels["field_pair_cocreates_center3"] = (
            3,
            {
                (IDX["Momentum"], IDX["Idle"], IDX["Reflected"]),
                (IDX["Momentum"], IDX["Reflected"], IDX["Idle"]),
            },
        )

    if stage >= 3:
        # The Sovereign Mirror (v57), Note p. 9: "the table borrows the shape of physics, not its authority"
        # Ch. 2 pp. 26-27 stationary/poised vs. returning polarity of the two Current partners:
        #   Idle (across from Electro): poised, running while standing still (present at rest without traveling)
        #   Reflected (across from Magnetic): bent back, closing on itself (always returning rather than pouring out)
        rels["poised_stationary_component1"] = (1, {IDX["Idle"]})
        rels["closed_loop_returning_component1"] = (1, {IDX["Reflected"]})

    return rels


def enumerate_automorphisms(stage: int) -> dict[str, Any]:
    """
    Use Z3 to enumerate ALL permutations pi in S_29 that preserve every structural
    relation in `_build_stage_relations(stage)` (both forward and backward, since pi
    is a bijection on finite ground relations).
    """
    solver = z3.Solver()
    pi = [z3.Int(f"pi_{i}") for i in range(N_NODES)]

    # Bijection on {0, ..., 28}
    for v in pi:
        solver.add(v >= 0, v < N_NODES)
    solver.add(z3.Distinct(pi))

    rels = _build_stage_relations(stage)

    for _rname, (arity, tuples) in rels.items():
        tuple_list = sorted(tuples)
        for tup in tuple_list:
            if arity == 1:
                a = tup
                solver.add(z3.Or([pi[a] == b for b in tuple_list]))
            elif arity == 2:
                a, b = tup
                solver.add(
                    z3.Or([z3.And(pi[a] == c, pi[b] == d) for (c, d) in tuple_list])
                )
            elif arity == 3:
                a, b, c = tup
                solver.add(
                    z3.Or(
                        [
                            z3.And(pi[a] == d, pi[b] == e, pi[c] == f)
                            for (d, e, f) in tuple_list
                        ]
                    )
                )

    automorphisms: list[list[int]] = []
    while solver.check() == z3.sat:
        m = solver.model()
        perm = [m.eval(pi[i]).as_long() for i in range(N_NODES)]
        automorphisms.append(perm)
        # Block this exact permutation to find all solutions exhaustively
        solver.add(z3.Or([pi[i] != perm[i] for i in range(N_NODES)]))

    # Compute exact orbits for every node
    orbits: dict[str, list[str]] = {}
    fixed_nodes: list[str] = []
    non_fixed_nodes: dict[str, list[str]] = {}
    for i, name in enumerate(NODES):
        orb_indices = sorted({perm[i] for perm in automorphisms})
        orb_names = [NODES[j] for j in orb_indices]
        orbits[name] = orb_names
        if len(orb_names) == 1:
            fixed_nodes.append(name)
        else:
            non_fixed_nodes[name] = orb_names

    # Verify identity permutation is always in Aut
    identity_perm = list(range(N_NODES))
    assert identity_perm in automorphisms, "Identity must be a valid automorphism!"

    return {
        "stage": stage,
        "search_space_factorial": str(math.factorial(N_NODES)),
        "automorphism_count": len(automorphisms),
        "fixed_node_count": len(fixed_nodes),
        "total_nodes": N_NODES,
        "fixed_nodes": fixed_nodes,
        "non_trivial_orbits": non_fixed_nodes,
    }


def prove_two_sided_asymmetry_unsat() -> dict[str, Any]:
    """
    Prove via Z3 + Minimal Unsatisfiable Core (unsat_core) that no dynamical
    automorphism of the two-sided system {NP=0, P=1} can swap the two sides.
    """
    solver = z3.Solver()
    solver.set(unsat_core=True)

    # Sector 0 = Nonphysical, Sector 1 = Physical
    sigma = [z3.Int("sigma_NP"), z3.Int("sigma_P")]
    solver.assert_and_track(
        z3.And(sigma[0] >= 0, sigma[0] <= 1, sigma[1] >= 0, sigma[1] <= 1, sigma[0] != sigma[1]),
        "bijection_on_two_sectors",
    )

    # Dynamical predicates established in Part I (Condition.lean & Crossing.lean)
    zero_damping = z3.Function("zero_damping", z3.IntSort(), z3.BoolSort())
    unconditional_out_crossing = z3.Function("unconditional_out_crossing", z3.IntSort(), z3.BoolSort())
    blockable_in_crossing = z3.Function("blockable_in_crossing", z3.IntSort(), z3.BoolSort())

    solver.assert_and_track(
        z3.And(zero_damping(0) == True, zero_damping(1) == False),
        "thm_1_2_laminar_culmination_vs_damped_decay",
    )
    solver.assert_and_track(
        z3.And(unconditional_out_crossing(0) == True, unconditional_out_crossing(1) == False),
        "thm_3_2_top_crossing_unconditional_only_from_NP",
    )
    solver.assert_and_track(
        z3.And(blockable_in_crossing(0) == False, blockable_in_crossing(1) == True),
        "thm_3_2_bottom_holding_on_resistance_only_on_P",
    )

    # Automorphism preservation of dynamical laws
    solver.assert_and_track(
        z3.And(
            zero_damping(0) == zero_damping(sigma[0]),
            zero_damping(1) == zero_damping(sigma[1]),
            unconditional_out_crossing(0) == unconditional_out_crossing(sigma[0]),
            blockable_in_crossing(1) == blockable_in_crossing(sigma[1]),
        ),
        "dynamical_structure_preservation",
    )

    # Challenger hypothesis (A3-S): swap Nonphysical and Physical sectors
    solver.assert_and_track(
        z3.And(sigma[0] == 1, sigma[1] == 0),
        "hypothesis_swap_NP_and_P_sides",
    )

    status = solver.check()
    assert status == z3.unsat, "Global side swap must be UNSAT!"
    core = sorted(str(c) for c in solver.unsat_core())

    return {
        "hypothesis": "Swap Nonphysical and Physical sectors globally (Arm A3-S structural test)",
        "solver_result": str(status),
        "minimal_unsatisfiable_core": core,
    }


def run_structural_rigidity() -> dict[str, Any]:
    s1 = enumerate_automorphisms(stage=1)
    s2 = enumerate_automorphisms(stage=2)
    s3 = enumerate_automorphisms(stage=3)
    side_swap = prove_two_sided_asymmetry_unsat()

    assert s1["automorphism_count"] == 12, f"Expected 12 at Stage 1, got {s1['automorphism_count']}"
    assert s2["automorphism_count"] == 2, f"Expected 2 at Stage 2, got {s2['automorphism_count']}"
    assert s3["automorphism_count"] == 1, f"Expected 1 at Stage 3, got {s3['automorphism_count']}"
    assert s3["fixed_node_count"] == 29

    return {
        "proof_id": "Part_II_A_Unlabeled_Graph_Structural_Rigidity",
        "epistemic_scope": (
            "Following The Sovereign Mirror (v57, Note p. 9), 'the table borrows the shape of physics, "
            "not its authority'. Although the Z3 solver receives only unlabeled integer node IDs 0..28 "
            "with zero English dictionary definitions, the 29-node graph relations in `_build_stage_relations` "
            "were written by hand knowing the Map terms. What this Z3 automorphism proof establishes is: "
            "no two terms in the Map, as encoded, are interchangeable (12 -> 2 -> 1 automorphism collapse, "
            "all 29/29 nodes fixed at Stage 3), and no encoded bijection swaps the Nonphysical and Physical sectors."
        ),
        "relations_hand_written_knowing_targets": True,
        "z3_version": z3.get_version_string(),
        "total_unlabeled_nodes": N_NODES,
        "symmetric_group_size": str(math.factorial(N_NODES)),
        "stages": {
            "S1_equations_crossing_containment": s1,
            "S2_plus_map_cocreation_links": s2,
            "S3_plus_ch2_stationary_vs_returning_polarity": s3,
        },
        "two_sided_swap_no_go": side_swap,
    }


if __name__ == "__main__":
    report = run_structural_rigidity()
    print(json.dumps(report, indent=2))
