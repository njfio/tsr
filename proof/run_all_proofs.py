"""
run_all_proofs.py — Unified End-to-End Formal Verification Suite for TSR
========================================================================
Executes all three independent, deterministic, zero-LLM formal proof pillars:
  - Part I  (`proof/lean/`):      Lean 4 (v4.35.0) machine-checked deductive proofs,
                                  source scan for zero `sorry`/`admit`/`axiom`/`have _`,
                                  negative typecheck on nominal `PhysDim` vs `NonphysRank`,
                                  and `#print axioms` audit across all 33 headline items.
  - Part II (`proof/z3/`):        Z3 (SMT) structural automorphism cascade on S_29
                                  (8.84e30 -> 12 -> 2 -> 1) + Ch. 16 axiomatic MUC
                                  audit (21 deletion-verified 1-minimal cores, cleaned
                                  physical control flags) + 14-slot Princeton WordNet 3.0
                                  synset audit + macOS Oxford discrete-sense & uniform
                                  [40, 60, 80, 100] window-sweep audit + offline self-test.
  - Part III (`proof/etymology/`): Exact rational (`fractions.Fraction`) combinatorial
                                  proofs over all 80 audited words of *What the Words Knew*,
                                  headlined by zero-choice pre-existing repo code graphs
                                  across the full symmetric blind grid (`N_blind = 3152`)
                                  and non-circular within-physics directionality tests.

Writes deterministic output certificate to `proof/verification_certificate.json`.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

PROOF_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROOF_DIR.parent
LEAN_DIR = PROOF_DIR / "lean"
Z3_DIR = PROOF_DIR / "z3"
ETYM_DIR = PROOF_DIR / "etymology"
CERT_PATH = PROOF_DIR / "verification_certificate.json"

for p in (REPO_ROOT, Z3_DIR, ETYM_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import combinatorial_proofs  # noqa: E402
import lexical_rigidity  # noqa: E402
import structural_rigidity  # noqa: E402

LEAN_THEOREMS: list[str] = [
    # Condition.lean (Props/Thms 1.1 - 1.4, 9 items)
    "TSR.condition_triad_equivalence",
    "TSR.receptive_triad_equivalence",
    "TSR.undivided_locus_triad",
    "TSR.damped_ripple_strict_decay",
    "TSR.zero_resistance_culmination",
    "TSR.zero_resistance_chord_preservation",
    "TSR.the_knife_irreversibility",
    "TSR.destructive_null_requires_spatial_separation",
    "TSR.single_locus_cannot_cancel",
    # MirrorFunctor.lean (Thms/Props 2.1 - 2.4, 12 items)
    "TSR.density_volume_product_symmetric",
    "TSR.canonicalMirrorRankHom_isomorphism",
    "TSR.elimination_theorem_desire_vibrance",
    "TSR.R_form_involutive",
    "TSR.R_form_compositional_mechanics",
    "TSR.temporal_momentum_energy_factorization",
    "TSR.two_level_reading_theorem",
    "TSR.falling_man_equivalence",
    "TSR.frequency_product_strict_monotonicity",
    "TSR.cross_hinge_dilation_throttling",
    "TSR.ratio_laws_fail_monotonicity",
    "TSR.light_surface_of_mirror",
    # Crossing.lean (Thms/Lemmas 3.1 - 3.3, 6 items)
    "TSR.v4_group_and_action",
    "TSR.derived_diagonal_symmetry",
    "TSR.resistance_contrast_filter_properties",
    "TSR.self_refutation_of_wanting_nonwanting",
    "TSR.direct_forcing_increases_confinement",
    "TSR.unique_weak_diagonal_escape",
    # EntityAndMeta.lean (Lemmas/Props/Thms 4.1 - 4.4, 6 items)
    "TSR.multiplicative_gate_characterization",
    "TSR.four_way_entity_separation",
    "TSR.coupled_entity_false_positive_ease",
    "TSR.tsr_axioms_consistent",
    "TSR.independence_of_first_partition",
    "TSR.gravity_open_joint_two_vs_three_regions",
]


def _strip_lean_comments(src: str) -> str:
    # Strip block `/- ... -/` comments and `-- ...` line comments
    out = re.sub(r"/-.*?-/", " ", src, flags=re.DOTALL)
    out = re.sub(r"--[^\n]*", " ", out)
    return out


def verify_lean_suite() -> dict[str, Any]:
    env = os.environ.copy()
    elan_bin = Path.home() / ".elan" / "bin"
    if elan_bin.exists():
        env["PATH"] = f"{elan_bin}:{env.get('PATH', '')}"

    lean_files = sorted(LEAN_DIR.rglob("*.lean"))
    lean_files = [f for f in lean_files if ".lake" not in f.parts]
    assert len(lean_files) >= 7, f"Expected >= 7 Lean files, found {len(lean_files)}"
    assert len(LEAN_THEOREMS) == 33, f"Expected 33 headline Lean theorems, found {len(LEAN_THEOREMS)}"

    # 1. Source hygiene scan: zero `sorry`, `admit`, custom `axiom`, or unused `have _`
    for lf in lean_files:
        cleaned = _strip_lean_comments(lf.read_text(encoding="utf-8"))
        for forbidden in ("sorry", "admit", "axiom"):
            matches = re.findall(rf"\b{forbidden}\b", cleaned)
            assert not matches, f"Forbidden token `{forbidden}` found in {lf}!"
        unused_have = re.findall(r"\bhave\s+_\b", cleaned)
        assert not unused_have, f"Unused hypothesis suppressor `have _` found in {lf}!"

    # 2. Query Lean version
    ver_proc = subprocess.run(
        ["lean", "--version"],
        cwd=LEAN_DIR,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    lean_version = ver_proc.stdout.strip().splitlines()[0]

    # 3. Compile full Lean 4 library via `lake build`
    build_proc = subprocess.run(
        ["lake", "build"],
        cwd=LEAN_DIR,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    combined_build_out = (build_proc.stdout + "\n" + build_proc.stderr).strip()
    assert "warning:" not in combined_build_out, f"Lean build emitted warnings:\n{combined_build_out}"

    # 4. Kernel axiom audit on all 33 headline theorems via `#print axioms`
    stdin_script = "import TSR\n" + "\n".join(f"#print axioms {t}" for t in LEAN_THEOREMS) + "\n"
    ax_proc = subprocess.run(
        ["lake", "env", "lean", "--stdin"],
        cwd=LEAN_DIR,
        env=env,
        input=stdin_script,
        capture_output=True,
        text=True,
        check=True,
    )
    assert not ax_proc.stderr.strip(), f"Unexpected Lean stderr: {ax_proc.stderr}"

    theorem_axioms: dict[str, list[str]] = {}
    for line in ax_proc.stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        m_none = re.match(r"^'([^']+)' does not depend on any axioms$", line)
        m_some = re.match(r"^'([^']+)' depends on axioms: \[([^\]]+)\]$", line)
        if m_none:
            theorem_axioms[m_none.group(1)] = []
        elif m_some:
            axs = [a.strip() for a in m_some.group(2).split(",")]
            for a in axs:
                assert a in ("propext", "Quot.sound"), (
                    f"Unexpected non-constructive or sorry axiom `{a}` in {m_some.group(1)}!"
                )
            theorem_axioms[m_some.group(1)] = axs
        else:
            raise AssertionError(f"Unparsed #print axioms line: {line}")

    assert set(theorem_axioms.keys()) == set(LEAN_THEOREMS), (
        f"Theorem audit mismatch: {set(LEAN_THEOREMS) ^ set(theorem_axioms.keys())}"
    )

    # 5. Negative typecheck: verify nominal separation of `TSR.PhysDim` and `TSR.NonphysRank`
    neg_script = "import TSR\ndef bad : TSR.PhysDim → TSR.NonphysRank := id\n"
    neg_proc = subprocess.run(
        ["lake", "env", "lean", "--stdin"],
        cwd=LEAN_DIR,
        env=env,
        input=neg_script,
        capture_output=True,
        text=True,
        check=False,
    )
    neg_out = (neg_proc.stdout + "\n" + neg_proc.stderr).lower()
    assert neg_proc.returncode != 0 and "type mismatch" in neg_out, (
        "Negative typecheck failed: `def bad : TSR.PhysDim → TSR.NonphysRank := id` was not rejected!"
    )

    pure_cic_count = sum(1 for v in theorem_axioms.values() if len(v) == 0)

    return {
        "lean_version": lean_version,
        "modules_verified": [str(f.relative_to(REPO_ROOT)) for f in lean_files],
        "zero_sorry_verified": True,
        "zero_custom_axioms_verified": True,
        "zero_classical_choice_verified": True,
        "zero_unused_have_underscore_verified": True,
        "nominal_dim_rank_separation_verified": True,
        "total_theorems_audited": len(LEAN_THEOREMS),
        "pure_axiom_free_cic_theorems": pure_cic_count,
        "constructive_quotient_propext_theorems": len(LEAN_THEOREMS) - pure_cic_count,
        "theorem_kernel_axioms": theorem_axioms,
    }


def verify_part2_invariants(part2a_struct: dict[str, Any], part2b_lex: dict[str, Any]) -> None:
    # Part II.A: S_29 automorphism cascade 12 -> 2 -> 1 + A3-S UNSAT
    assert part2a_struct["total_unlabeled_nodes"] == 29
    stages = part2a_struct["stages"]
    assert stages["S1_equations_crossing_containment"]["automorphism_count"] == 12
    assert stages["S1_equations_crossing_containment"]["fixed_node_count"] == 21
    assert stages["S2_plus_map_cocreation_links"]["automorphism_count"] == 2
    assert stages["S2_plus_map_cocreation_links"]["fixed_node_count"] == 27
    assert stages["S3_plus_gauss_maxwell_field_polarity"]["automorphism_count"] == 1
    assert stages["S3_plus_gauss_maxwell_field_polarity"]["fixed_node_count"] == 29
    assert part2a_struct["two_sided_swap_no_go"]["solver_result"] == "unsat"
    assert len(part2a_struct["two_sided_swap_no_go"]["minimal_unsatisfiable_core"]) >= 2

    # Part II.B.1: Cleaned physical control flags, pre-tiebreak = 2, unique A0, 21 1-minimal MUCs
    uniq = part2b_lex["uniqueness_theorem"]
    assert uniq["physical_control_flags_cleaned"] == {
        "Focus_selects_receptivity_target": False,
        "electric_means_poised_at_rest": False,
        "magnetic_means_returning_closed_loop": False,
    }
    assert uniq["pre_continuum_tiebreak_solutions_count"] == 2
    assert uniq["canonical_tsr_sat"] is True
    assert uniq["unique_solution"] is True

    challengers = part2b_lex["challenger_swap_certificates"]
    a3_controls = part2b_lex["a3_floor_control_certificates"]
    assert len(challengers) == 17
    assert len(a3_controls) == 4
    assert all(c["result"] == "unsat" and c["core_size"] >= 1 for c in challengers)
    assert all(
        c["result"] == "unsat" and c["broken_slots_out_of_14"] == 14 and c["core_size"] >= 1
        for c in a3_controls
    )

    # Part II.B.2: Cross-platform Princeton WordNet 3.0 discrete synset audit + SHA-256 verification
    wn = part2b_lex["wordnet_synset_polysemy"]
    assert wn["status"] == "verified_cross_platform_princeton_wordnet_3_0"
    assert wn["zero_window_size_parameters"] is True
    assert wn["zero_hand_coded_word_booleans"] is True
    assert wn["zero_target_stem_circularity_verified"] is True
    assert wn["single_word_pool_size"] == 100
    assert wn["resolved_words_count"] == 99
    assert wn["unresolved_words"] == ["vibrance"]
    assert wn["total_synsets_evaluated"] == 776
    assert wn["slots_evaluated_total"] == 14
    assert wn["dual_sense_polysemy_slots_count"] == 7
    assert wn["single_sense_domain_slots_count"] == 7
    wn_path = REPO_ROOT / wn["artifact_path"]
    assert wn_path.exists(), f"Missing WordNet artifact at {wn_path}"
    assert hashlib.sha256(wn_path.read_bytes()).hexdigest() == wn["artifact_file_sha256"]

    # macOS New Oxford American Dictionary discrete-sense + uniform [40, 60, 80, 100] sweep
    ox = part2b_lex["blind_oxford_dictionary_polysemy"]
    assert ox["zero_hand_coded_word_booleans"] is True
    assert ox["zero_target_stem_circularity_verified"] is True
    assert ox["slots_evaluated_total"] == 14
    if ox.get("macos_coreservices_available"):
        assert ox["resolved_entries_count"] == 100
        assert ox["origin_etymology_stripped_before_lowercase"] is True
        assert ox["zero_window_size_parameters_in_discrete_audit"] is True
        sweep = ox["window_sensitivity_sweep"]
        assert sweep["uniform_widths_tested"] == [40, 60, 80, 100]
        assert sweep["all_slots_invariant_across_widths"] is True

    # Offline CoreServices -> None non-skipping self-test
    selftest = part2b_lex["cross_platform_offline_selftest"]
    assert selftest["simulated_linux_ci_coreservices_disabled"] is True
    assert selftest["did_silently_skip"] is False
    assert selftest["deterministic_match_with_wordnet_3_0_audit"] is True
    assert selftest["slots_verified_offline"] == 14


def verify_part3_invariants(part3_etym: dict[str, Any]) -> None:
    st = part3_etym["self_tests"]
    assert st["all_passed"] is True
    assert st["frozen_unique_tokens_audited"] == 333
    assert st["frozen_mapped_tokens_count"] == 84
    for tok in ("real", "reality", "realities"):
        assert tok in st["forbidden_tokens_verified_unmapped"]
    assert st["strict_n_blind_pairs"] == 3152
    assert st["legacy_n_blind_pairs"] == 3153
    assert st["core_law_pre_etymology_citations_verified"] == 21
    assert st["pure_table_subset_of_frozen_verified"] is True

    t1 = part3_etym["test_III_1_hidden_root_homomorphism"]
    for cell_key in ("III_1A_Pure_PIE", "III_1A_Diachronic", "III_1B_Pure_PIE", "III_1C_Diachronic"):
        cell = t1[cell_key]
        assert cell["n_blind_pairs"] == 3152
        assert cell["hypergeometric_total_pop_used"] == 3152

    sl = t1["strict_laryngeal_pie_sensitivity"]
    for sl_key in (
        "III_1A_Pure_PIE_Strict_Laryngeal",
        "III_1A_Diachronic_Strict_Laryngeal",
        "III_1B_Pure_PIE_Strict_Laryngeal",
        "III_1C_Diachronic_Strict_Laryngeal",
        "III_1A_Strict_PIE_Plus_Coined_Calque_Only",
        "III_1C_Strict_PIE_Plus_Coined_Calque_Only",
    ):
        assert sl[sl_key]["hypergeometric_total_pop_used"] == 3152

    mm = t1["momentum_movement_filter_sensitivity_side_by_side"]
    assert mm["strict_mentum_filter_excluding_momentum_movement"]["n_blind_pairs"] == 3152
    assert mm["legacy_4char_filter_including_momentum_movement"]["n_blind_pairs"] == 3153
    assert "exploratory_unblinded_descriptive_concordance" in t1

    t2 = part3_etym["test_III_2_energeia_actualitas_hinge_localization"]
    assert t2["calque_pair"] == ["actual", "energy"]
    assert t2["classical_link_type"] == "coined_translation_calque"
    assert t2["exact_probabilities"]["uniform_blind_exact_physical_hinge_edge"]["fraction"] == "1/3152"

    t3 = part3_etym["test_III_3_directional_asymmetry_within_physics"]
    hl = t3["headline_within_physics_inferential_tests"]
    assert hl["fisher_directional_physics_core_vs_secondary"]["exact_fraction"] == "3/1001"
    assert hl["fisher_all_35_physics_words_core_vs_secondary"]["exact_fraction"] == "171/2728"
    assert "binomial_reverse_metaphor_upper_tail_bounds" in hl
    assert "sovereign_mirror_book_only_sensitivity" in hl
    assert len(t3["core_law_pre_etymology_citations"]) == 21
    assert "descriptive_80_word_ledger_concentration_summary" in t3


def compute_file_hashes() -> dict[str, str]:
    tracked: list[Path] = []
    for sub in (LEAN_DIR, Z3_DIR, ETYM_DIR):
        for f in sorted(sub.rglob("*")):
            if f.is_file() and ".lake" not in f.parts and "__pycache__" not in f.parts and not f.name.startswith("."):
                tracked.append(f)
    hashes: dict[str, str] = {}
    for f in tracked:
        rel = str(f.relative_to(REPO_ROOT))
        hashes[rel] = hashlib.sha256(f.read_bytes()).hexdigest()
    return hashes


def main() -> None:
    t0 = time.perf_counter()

    print("[1/3] Verifying Part I — Lean 4 Deductive & Meta-Theoretical Suite...")
    part1_lean = verify_lean_suite()
    print(
        f"      PASS: {part1_lean['total_theorems_audited']} theorems kernel-verified "
        f"(0 sorry, 0 custom axioms, 0 Classical.choice, nominal PhysDim/NonphysRank separation verified; "
        f"{part1_lean['pure_axiom_free_cic_theorems']} pure CIC)."
    )

    print("[2/3] Verifying Part II — Z3 Structural, Ch. 16 MUC & WordNet 3.0 / Oxford Suite...")
    part2a_struct = structural_rigidity.run_structural_rigidity()
    part2b_lex = lexical_rigidity.run_lexical_rigidity()
    verify_part2_invariants(part2a_struct, part2b_lex)
    dict_status = part2b_lex["blind_oxford_dictionary_polysemy"]["status"]
    wn_status = part2b_lex["wordnet_synset_polysemy"]["status"]
    print(
        f"      PASS: S_29 cascade 12 -> 2 -> 1 + A3-S UNSAT; "
        f"Ch. 16 uniqueness (pre-tiebreak = 2) + 21 1-minimal MUCs; "
        f"14-slot WordNet ({wn_status}) + Oxford ({dict_status}) + offline self-test."
    )

    print("[3/3] Verifying Part III — Exact 80-Word Combinatorial Etymology Suite...")
    part3_etym = combinatorial_proofs.run_combinatorial_proofs()
    verify_part3_invariants(part3_etym)
    t1 = part3_etym["test_III_1_hidden_root_homomorphism"]
    c1a_pie = t1["III_1A_Pure_PIE"]
    c1c_dia = t1["III_1C_Diachronic"]
    t3_hl = part3_etym["test_III_3_directional_asymmetry_within_physics"]["headline_within_physics_inferential_tests"]
    f_dir = t3_hl["fisher_directional_physics_core_vs_secondary"]
    f_35 = t3_hl["fisher_all_35_physics_words_core_vs_secondary"]
    print(
        f"      PASS: 80/80 words + self-tests passed (N_blind = 3152 strict / 3153 legacy); "
        f"III.1A pure PIE = {c1a_pie['observed_overlap_count']}/{c1a_pie['etymology_edge_count']} "
        f"(p = {c1a_pie['exact_hypergeometric_p_float']:.4f}), "
        f"III.1C diachronic = {c1c_dia['observed_overlap_count']}/{c1c_dia['etymology_edge_count']} "
        f"(hyper p = {c1c_dia['exact_hypergeometric_p_float']:.4f}, "
        f"strat-perm p = {c1c_dia['stratified_permutation_100k_crosscheck']['empirical_p_upper_bound']:.4f}); "
        f"within-physics Fisher 5/6 vs 0/8 p = {f_dir['p_value']:.4e} "
        f"(all-35 5/21 vs 0/14 p = {f_35['p_value']:.4f})."
    )

    elapsed = round(time.perf_counter() - t0, 3)

    certificate = {
        "suite": "Theory of Sovereign Reflectivity (TSR) — Unified Formal Proof Certificate",
        "all_checks_passed": True,
        "zero_llm_calls": True,
        "verification_runtime_seconds": elapsed,
        "part_I_lean4_deductive": part1_lean,
        "part_II_A_z3_structural_rigidity": part2a_struct,
        "part_II_B_z3_lexical_rigidity": part2b_lex,
        "part_III_exact_combinatorial_etymology": part3_etym,
        "source_sha256_manifest": compute_file_hashes(),
    }

    CERT_PATH.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    print(f"\nALL PROOFS VERIFIED IN {elapsed:.2f}s -> {CERT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
