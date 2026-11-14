# Machine-Checked Formalization and Consistency Check of the Theory of Sovereign Reflectivity

**Primary Sources Audited**:
1. Nicholas Ferguson, *The Sovereign Mirror* (**v57**; *The Map*, pp. 172–176)
2. Nicholas Ferguson, *What the Words Knew* (**proof 36**, November 2026; *Every Word, for the Record*, pp. 99–104)

**Verification Suite**: [run_all_proofs.py](run_all_proofs.py) → [verification_certificate.json](verification_certificate.json)  
**Toolchains**: Lean 4 (`v4.35.0`, `0 sorry`, `0 Classical.choice`, nominal `PhysDim` / `NonphysRank` separation), Z3 SMT Solver (`v5.4.1`), Princeton WordNet 3.0 ([wordnet_100_synsets.json](z3/wordnet_100_synsets.json), SHA-256 verified) + Apple `CoreServices` New Oxford American Dictionary (with cross-platform WordNet 3.0 fallback on Linux), Python 3.12 Exact Rational Arithmetic (`fractions.Fraction`, `0` LLM calls).

---

## 0. Epistemic Contract & Removed / Weakened Claims

Before stating any machine-checked result, this suite draws an explicit boundary around what deductive logic, finite SMT checking, and combinatorial word counts establish — and what they do **not** establish. As *The Sovereign Mirror* states upfront (*v57*, Note p. 9):

> **The table borrows the shape of physics, not its authority.**

### 0.1 What Is Scoped Out (Not Proved)
1. **External Physical or Ontological Truth**: Machine-checked theorems prove what follows *conditional on chosen Lean structures and definitions*, or that those definitions admit a constructive rational witness (`canonicalTSRModel`). They do **not** establish from zero premises that consciousness exists independently, that the Map describes external physical law, or that a nonphysical medium is empirically real (*SM v57*, Ch. 21, p. 153).
2. **Physics Authority or Dimensional Equivalence**: TSR does **not** equate physical joules across $C^2 \times M = E = m \times c^2$, assign SI meters/seconds/kilograms to nonphysical terms, or derive physical constants (*SM v57*, Note p. 9, Ch. 2 p. 28, Ch. 17 p. 128). Structural analogies share algebraic form only.
3. **Modeling Choices Introduced in Code (`(c)` Items)**: Several quantitative formulas, AST categories, and synthetic dynamical laws in Lean — including the specific dilation ansatz $C_{\text{rate}} \cdot \frac{T_0}{T_0 + h}$, quadratic update increments $(x - s)^2$, `"reversible equilibrium"` encoding for Boyle's law, and identifier strings such as `hinge`, `barrier`, `temporal momentum`, and `twoRegionNoSharedE`/`threeRegionSharedE` — are **(c) formalization choices not stated in *v57***, and are flagged explicitly in [Section 1](#1-part-i--machine-checked-formalization-in-lean-4).
4. **Open Empirical & Domain Questions**: Unforced empirical claims (fever/illness Ch. 19 pp. 144–146, post-mortem continuation Ch. 20 pp. 147–151, planetary/ecosystem entity boundaries Ch. 18 p. 141) remain outside deductive claims.

### 0.2 Explicit Removed or Weakened Claims (PR Revision Transparency)
Compared to earlier drafts of this document and verification scripts, the following claims were explicitly **removed or weakened**:
1. **Rescoped Overall Claim**: Removed maximalist phrasing claiming external certainty or proof of physical/ontological truth; the suite is framed plainly as a **machine-checked formalization and consistency check**.
2. **Removed Physics-Authority Metaphors in Part II**: Removed all classical electromagnetism field-line and divergence metaphors from Stage S3 and `SLOT_REQUIREMENTS`; Stage S3 (`S3_plus_ch2_stationary_vs_returning_polarity`) now relies solely on *SM v57* Ch. 2 pp. 26–27 stationary vs. returning polarity, and the side-swap MUC tag is `thm_3_2_bottom_holding_on_resistance_only_on_P`.
3. **Disclosure of Hand-Written Inputs in Part II**: Part II no longer characterizes Z3 relation graphs, feature flags, or dictionary concept-groups as target-blind; [structural_rigidity.py](z3/structural_rigidity.py#L375-L383) and [lexical_rigidity.py](z3/lexical_rigidity.py#L1319-L1334) disclose directly that relation sets, `CANDIDATES`/`SLOT_REQUIREMENTS` flags, and per-slot keyword groups were **written by hand knowing the target words**. What Z3 checks is strictly: **no two terms in the Map, as encoded, are interchangeable**.
4. **Replacement of Confirmatory Etymology Overclaims in Part III**: Under the single **pre-declared primary test** (`g_tsr_oct22_cdba80d`, `66` pairs from Oct 22 commit `cdba80d` [tests/tsr_formal.py](../tests/tsr_formal.py), SHA-256 `075fd22b9e4a9b91fa76bc433e4a754ca5faf57009fa0c071158711fba918ae0`, vs. `pie_roots_strict`, `16` pairs over `N_orth_unrelated = 3,152`), there is **`1` overlapping pair (`distance–resist`) with exact hypergeometric $p = 0.2878$ — not statistically significant (null result)**. Earlier headlines featuring uncorrected Nov 13 graphs and exploratory `p < 0.05` cells are quarantined in [Section 3.2](#32-uncorrected-exploratory-sensitivity-analyses).
5. **Reclassification of Core-Law Directionality Ratios as Descriptive Only**: In [ledger_80.json](etymology/ledger_80.json), the 80 `kind` classifications (`family: 36`, `not used: 1`, etc.) were assigned by the author while drafting *What the Words Knew* (*proof 36*, pp. 99–104), not blind, and the `21 core_law` vs. `14 secondary_physics` partition is post hoc. All Fisher / binomial ratios in [Section 3.3](#33-descriptive-core-law-directionality-summary-post-hoc-not-inferential) are marked `DESCRIPTIVE_ONLY_POST_HOC_SPLIT_NOT_INFERENTIAL`.
6. **Accurate Pair Filtering Label**: Replaced the misleading `"blind"` label for the orthographic exclusion filter (`N_orth_unrelated = 3,152` strict / `3,153` legacy) with **"orthographically unrelated"** (`N_orth_unrelated`, `n_orth_unrelated_pairs`).
7. **Book Edition & Ledger Reconciliation**: Updated all references to *The Sovereign Mirror* **v57** and *What the Words Knew* **proof 36** (`pp. 99–104`), incorporating the 3 *proof 36* ledger diffs (`light` moved from `not used` to `family`, changing `worst_case_nonfamily_core_law` from `5/15` to `5/14`; `reflection` and `wave` text updates; shifted page numbers).

```mermaid
flowchart LR
    subgraph P1["Part I: Lean 4.35.0 Kernel (35 Items)"]
        OA["OrderedAlgebra.lean (OrderedField + QRat)"]
        C1["Condition.lean (9 Items)"]
        C2["MirrorFunctor.lean (14 Items incl. v57 Benchmark)"]
        C3["Crossing.lean (6 Items)"]
        C4["EntityAndMeta.lean (6 Items)"]
        OA --> C1 & C2 & C3 --> C4
    end
    subgraph P2["Part II: Z3 5.4.1 + Dictionary Audits"]
        Z1["structural_rigidity.py (S_29: 12 -> 2 -> 1)"]
        Z2["lexical_rigidity.py (21 MUCs + WordNet 3.0 / Oxford)"]
    end
    subgraph P3["Part III: Exact Q-Combinatorics (WTWK Proof 36)"]
        L80["ledger_80.json (80 Words, Dual PIE)"]
        E1["combinatorial_proofs.py (Primary Null + Sensitivity + Descriptive)"]
        L80 --> E1
    end
    C4 & Z1 & Z2 & E1 --> CERT["verification_certificate.json"]
```

---

## 1. Part I — Machine-Checked Formalization in Lean 4

Source directory: [proof/lean/](lean) (`0 sorry`, `0 admit`, `0 custom axioms`, `0 Classical.choice`, `0 have _`; negative compile check rejects `def bad : TSR.PhysDim → TSR.NonphysRank := id`).

Every theorem below is quantified over `[OrderedField F]` ([OrderedAlgebra.lean](lean/TSR/OrderedAlgebra.lean#L21-L40), including `sub_nonneg_of_le` [#L195-L199](lean/TSR/OrderedAlgebra.lean#L195-L199) and `mul_left_cancel_pos` [#L254-L258](lean/TSR/OrderedAlgebra.lean#L254-L258)) and constructively inhabited on `QRat` ([#L499-L743](lean/TSR/OrderedAlgebra.lean#L499-L743)). Across all **35 verified items**: **15** use zero axioms (pure CIC), **13** depend only on `[propext]`, and **7** depend on `[propext, Quot.sound]`.

### 1.1 Explicit Classification Standard `(a)` / `(b)` / `(c)`

Every Lean theorem proves something exact, but for different reasons:
- **`(a)` Consequence of chosen definitions**: Deductively follows once the Lean structures/predicates are posited.
- **`(b)` Standard physics or algebra true regardless of TSR**: Ordinary ordered-field, group-theoretic, Newtonian, or relativistic algebra that holds independently of TSR.
- **`(c)` Modeling choice not in the book**: Quantitative equations, data encodings, or code labels added during Lean formalization that do not appear verbatim in *SM v57*. Hybrids such as **(a) over (c)** mean Lean proves `(a)` deductively about the chosen `(c)` model.

Specifically flagged as **`(c)` not in *SM v57***:
1. **Dilation formula $v_{\text{eff}} = C_{\text{rate}} \cdot \frac{T_0}{T_0 + h}$** ([cross_hinge_dilation_throttling](lean/TSR/MirrorFunctor.lean#L795-L844)) and the identifier word `hinge` (*v57* speaks of *The Present* / center rather than a `"hinge"` rate quotient).
2. **Squared-error state update rules $(x - s)^2$** in [predErrorSq](lean/TSR/EntityAndMeta.lean#L209-L210), [subgoalErrorSq](lean/TSR/EntityAndMeta.lean#L213-L214), [four_way_entity_separation](lean/TSR/EntityAndMeta.lean#L349-L498), [pairwiseContrast](lean/TSR/EntityAndMeta.lean#L703-L705), and [independence_of_first_partition](lean/TSR/EntityAndMeta.lean#L734-L760).
3. **`"reversible equilibrium"` encoding (`IsothermalEquilibriumBalance` / `reversibleStateEquilibrium`) for Row 17 (Boyle's law)** in [two_level_reading_theorem](lean/TSR/MirrorFunctor.lean#L626-L637). In *SM v57* Ch. 16, p. 118, Boyle's law stays `.Keep` for a different physical reason: **pressure exists only because walls hold something in; walls are resistance, so pressure can only exist where the two sides touch**, keeping the compressed pressure–volume relation unchanged when resistance is on.
4. **Formalization code labels not used as *v57* terms**: identifiers containing `hinge` (`cross_hinge_dilation_throttling`), `barrier` (`barrier`, `ResistanceWorkBarrier`, `countActiveBarriers`, `multiBarrierWorkRow`), `temporal momentum` (`physTemporalMomentum`, *cf. SM v57* Ch. 17 pp. 129–130), and `twoRegion` / `threeRegion` (`MirrorArchitecture.twoRegionNoSharedE` vs. `.threeRegionSharedE`; *SM v57* Ch. 16 p. 117 writes `"two sides"` vs. `"three: the two sides and the continuum where they meet, with one energy in it"`).

### 1.2 Complete 35-Item Classification Table

| # | Lean Identifier & Location | Kernel Axioms | Class | What Lean Actually Proves vs. What Is `(b)` or `(c)` |
|---:|:---|:---|:---|:---|
| 1 | [`condition_triad_equivalence`](lean/TSR/Condition.lean#L115-L129) | `none` | `(a) over (c)` | On a partitioned `(c)` `Medium` ([L75-L87](lean/TSR/Condition.lean#L75-L87)), modeled `Resistant ↔ Limited ↔ Radiating` via `rho > 0` / positive `barrier` & `transferCost`. |
| 2 | [`receptive_triad_equivalence`](lean/TSR/Condition.lean#L138-L169) | `[propext]` | `(a) over (c)` | `rho = 0` forces zero modeled `barrier`/`transferCost`, giving `Limitless ↔ Collecting` on partitioned `Medium`. |
| 3 | [`undivided_locus_triad`](lean/TSR/Condition.lean#L175-L196) | `none` | `(a) over (c)` | An undivided locus (`∀ x y, x = y`) forces zero `barrier`/`transferCost`, `Limitless`, and `Collecting` even when `rho > 0`. |
| 4 | [`damped_ripple_strict_decay`](lean/TSR/Condition.lean#L228-L252) | `none` | `(a)/(b) over (c)` | `(b)` Geometric-decay induction ($B_{n+1} = (1-\alpha)B_n < B_n$) over `(c)` discrete `PerturbationMedium` (`trajectory`). |
| 5 | [`zero_resistance_culmination`](lean/TSR/Condition.lean#L258-L285) | `none` | `(a)/(b) over (c)` | `(b)` Additive partial-sum accumulation $B_n = B_0 + \sum \xi_k$ when `rho = 0 → α = 0` in `(c)` `PerturbationMedium`. |
| 6 | [`zero_resistance_chord_preservation`](lean/TSR/Condition.lean#L308-L380) | `[propext]` | `(a)/(b) over (c)` | On `(c)` `chordTrajectory` under `singleModePulse`, `rho = 0` keeps target mode raised with zero cross-talk while `0 < α < 1` decays; finite ratio uses `(b)` `QRat` arithmetic. |
| 7 | [`the_knife_irreversibility`](lean/TSR/Condition.lean#L420-L437) | `[propext, Quot.sound]` | `(a)/(b) over (c)` | `(b)` Order monotonicity ($B_k < B_k + \Delta \implies B_k < B_m$ for $m \ge k+1$) on `(c)` `PerturbationMedium` at `α = 0` vs. signed restoration. |
| 8 | [`destructive_null_requires_spatial_separation`](lean/TSR/Condition.lean#L503-L516) | `[propext, Quot.sound]` | `(a)/(b) over (c)` | `(b)` Algebraic cancellation witness over `(c)` 2-locus wave sum (`E1 + E2 > 0`, null at 1 locus forces a distinct bright locus). |
| 9 | [`single_locus_cannot_cancel`](lean/TSR/Condition.lean#L521-L535) | `none` | `(a)/(b) over (c)` | `(b)` Positivity ($E_1 + E_2 \neq 0$) on `(c)` 1-locus `Unit` wave carrier. |
| 10 | [`density_volume_product_symmetric`](lean/TSR/MirrorFunctor.lean#L132-L141) | `[propext, Quot.sound]` | `(b)` | Pure `(b)` `OrderedField` commutativity/cancellation on $\rho \cdot V = M \iff D \cdot Vi = Mo$. |
| 11 | [`canonicalMirrorRankHom_isomorphism`](lean/TSR/MirrorFunctor.lean#L213-L231) | `none` | `(a) over (c)` | Constructive left/right-inverse bijection and additive homomorphism between `(c)` `PhysDim` ([L48-L52](lean/TSR/MirrorFunctor.lean#L48-L52)) and `NonphysRank` ([L55-L59](lean/TSR/MirrorFunctor.lean#L55-L59)). |
| 12 | [`elimination_theorem_desire_vibrance`](lean/TSR/MirrorFunctor.lean#L239-L280) | `[propext, Quot.sound]` | `(a)/(b) over (c)` | `(b)` `Int` linear arithmetic over `(c)` `IsMirrorRankHom`: anchoring Space↔Vibration and Mass↔Movement uniquely fixes Volume↔Vibrance and Density↔Desire. |
| 13 | [`R_form_involutive`](lean/TSR/MirrorFunctor.lean#L335-L342) | `[propext]` | `(a) over (c)` | `R_form (R_form t) = t` by structural induction on `(c)` `FormulaTerm` AST ([L316-L332](lean/TSR/MirrorFunctor.lean#L316-L332)). |
| 14 | [`R_form_compositional_mechanics`](lean/TSR/MirrorFunctor.lean#L389-L402) | `none` | `(a) over (c)` | Definitional evaluation showing `R_form` swaps modeled physical laws (`physForce`, `physRestEnergy`, `physTemporalMomentum`) with their nonphysical counterparts. |
| 15 | [`temporal_momentum_energy_factorization`](lean/TSR/MirrorFunctor.lean#L412-L421) | `none` | `(a)/(b) over (c)` | `(b)` Associative factoring $m \cdot c \cdot c = m \cdot (c \cdot c)$ over `(c)` code label `physTemporalMomentum` (`"temporal momentum"` is a code identifier, not a *v57* term). |
| 16 | [`two_level_reading_theorem`](lean/TSR/MirrorFunctor.lean#L626-L637) | `[propext]` | `(a) over (c)` | Finite `decide` check over `(c)` 17-row `LawAST` hand-classification `R_read` (`17/17`), narrow `R_read_ch2_clauses` (`4` misses), `(c)` `IsothermalEquilibriumBalance` Row 17, and `(c)` `multiBarrierWorkRow` (`2` active barriers). |
| 17 | [`v57_rule_wordings_benchmark`](lean/TSR/MirrorFunctor.lean#L682-L687) | `[propext]` | `(a) over (c)` | Finite `decide` evaluation of `(c)` AST encodings `R_read_v57_ch2` (`14/17`, fails `[11, 12, 17]`) and `R_read_v57_ch16` (`16/17`, fails `[17]`). See [Section 1.3](#13-v57-rule-wordings-benchmark). |
| 18 | [`constant_baselines_benchmark`](lean/TSR/MirrorFunctor.lean#L701-L710) | `[propext]` | `(a) over (c)` | Finite `decide` evaluation of `(c)` constant baselines `R_read_always_keep` (`14/17`, misses `[2, 8, 9]`) and `R_read_always_invert` (`3/17`, matches `[2, 8, 9]`); `R_read_v57_ch2` ties `always-Keep` (`14/17`) and `R_read_v57_ch16` (`16/17`) exceeds it by `2`. See [Section 1.3](#13-v57-rule-wordings-benchmark). |
| 19 | [`falling_man_equivalence`](lean/TSR/MirrorFunctor.lean#L726-L772) | `none` | `(b)` | Pure `(b)` ordered-field mechanics $m a = m g - R \iff R/m + a = g$ with boundary cases ($a = 0 \iff R = mg$; $R = 0 \iff a = g$). |
| 20 | [`frequency_product_strict_monotonicity`](lean/TSR/MirrorFunctor.lean#L778-L782) | `none` | `(b)` | Pure `(b)` `OrderedField` strict monotonicity ($0 < M_1 < M_2 \land 0 < A_1 < A_2 \implies M_1 A_1 < M_2 A_2$). |
| 21 | [`cross_hinge_dilation_throttling`](lean/TSR/MirrorFunctor.lean#L795-L844) | `[propext]` | `(a)/(b) over (c)` | **`(c)` Ansatz not in book**: formula $v_{\text{eff}} = C_{\text{rate}} \cdot \frac{T_0}{T_0 + h}$ and identifier word `"hinge"` are modeling choices; $v_{\text{eff}} = C_{\text{rate}} \iff h = 0$ and $0 < h \implies 0 < v_{\text{eff}} < C_{\text{rate}}$ follow by `(b)` algebra. |
| 22 | [`ratio_laws_fail_monotonicity`](lean/TSR/MirrorFunctor.lean#L852-L880) | `[propext, Quot.sound]` | `(b)/(a)` | `(b)` Explicit `QRat` arithmetic witnesses `(1, 4, 1, 2)` and `(1, 2, 1, 4)` refuting unconditional monotonicity of $A/M$ and $M/A$. |
| 23 | [`light_surface_of_mirror`](lean/TSR/MirrorFunctor.lean#L952-L1016) | `[propext]` | `(b) + (c)` | `(b)` Relativistic shell algebra ($m = 0 \iff pc = E \iff v = c$, $ds^2 = 0$, $E, p, v > 0$); calling $m = 0$ `"the surface of the mirror"` is `(c)` book reading (*v57* Ch. 2 p. 24, Ch. 21 p. 154). |
| 24 | [`v4_group_and_action`](lean/TSR/Crossing.lean#L111-L123) | `none` | `(b) over (c)` | `(b)` Klein-4 ($V_4$) group laws (`decide`) over `(c)` 4-pole `Quad` grid ([L46](lean/TSR/Crossing.lean#L46)). |
| 25 | [`derived_diagonal_symmetry`](lean/TSR/Crossing.lean#L131-L159) | `none` | `(a) over (c)` | Finite `decide` search over `24` bijections showing `(c)` Irreversible-Pole & side-swap axioms force `diag` (`Desire ↔ Expectation`, `Belief ↔ Intuition`). |
| 26 | [`resistance_contrast_filter_properties`](lean/TSR/Crossing.lean#L200-L223) | `[propext]` | `(a)/(b) over (c)` | `(b)` Idempotence and sign inequalities of `(c)` projection [`projectNP`](lean/TSR/Crossing.lean#L177). |
| 27 | [`self_refutation_of_wanting_nonwanting`](lean/TSR/Crossing.lean#L248-L283) | `[propext]` | `(a) over (c)` | Deductive contradiction and force-balance consequences on `(c)` `FallingManState` ([L228-L238](lean/TSR/Crossing.lean#L228-L238)) predicates. |
| 28 | [`direct_forcing_increases_confinement`](lean/TSR/Crossing.lean#L301-L308) | `none` | `(a)/(b) over (c)` | `(b)` Ordered-field addition monotonicity ($H < H + \beta u_{\text{force}}$) on `(c)` `confinementStep`. |
| 29 | [`unique_weak_diagonal_escape`](lean/TSR/Crossing.lean#L367-L434) | `[propext]` | `(a)/(b) over (c)` | Exhaustive induction over `(c)` finite `Quad` paths: when `tuned = true`, only `[Intuition, Belief, Expectation]` exits without cycle. |
| 30 | [`multiplicative_gate_characterization`](lean/TSR/EntityAndMeta.lean#L55-L81) | `none` | `(a)/(b) over (c)` | `(b)` Field algebra showing $u \cdot x$ satisfies `(c)` `IsZeroAnnihilatingGate` while $a u + b x$ ($a, b > 0$) leaks bilaterally. |
| 31 | [`coupled_entity_false_positive_ease`](lean/TSR/EntityAndMeta.lean#L113-L153) | `[propext]` | `(a)/(b) over (c)` | `(b)` Linear sum conservation $R_1' + R_2' = R_1 + R_2$ over `(c)` 2-entity `CoupledExchange` ([L91-L100](lean/TSR/EntityAndMeta.lean#L91-L100)). |
| 32 | [`four_way_entity_separation`](lean/TSR/EntityAndMeta.lean#L349-L498) | `[propext]` | `(a)/(b) over (c)` | **`(c)` Toy rules not in book**: synthetic `rockDyn`/`frozenAIDyn`/`persistentMemoryAIDyn`/`sovereignEntityDyn` using `(c)` quadratic updates `(x - s)^2` ([L209-L214](lean/TSR/EntityAndMeta.lean#L209-L214)); `(b)` induction separates all 6 pairs across arbitrary `xs : List F`. |
| 33 | [`tsr_axioms_consistent`](lean/TSR/EntityAndMeta.lean#L681-L682) | `[propext, Quot.sound]` | `(a) over (c)` | Relative consistency of `(c)` `TSRSystemModel` ([L517-L544](lean/TSR/EntityAndMeta.lean#L517-L544)) via constructive `QRat` witness `canonicalTSRModel` ([L648-L677](lean/TSR/EntityAndMeta.lean#L648-L677)). |
| 34 | [`independence_of_first_partition`](lean/TSR/EntityAndMeta.lean#L734-L760) | `[propext, Quot.sound]` | `(a)/(b) over (c)` | **`(c)` Toy formula not in book**: `QRat` counter-models (`undividedSingleLocusWorld`, `unresistedMultiLocusWorld`, `partitionedContrastWorld`) showing neither `|Locus| ≥ 2` nor `ρ > 0` alone yields positive `(c)` `pairwiseContrast = ρ * (state x - state y)^2`. |
| 35 | [`gravity_open_joint_two_vs_three_regions`](lean/TSR/EntityAndMeta.lean#L795-L812) | `none` | `(a) over (c)` | `decide` evaluation of `(c)` `R_readArch` / `countActiveBarriers` on `.twoRegionNoSharedE` (`15/17`) vs. `.threeRegionSharedE` (`17/17`). |

### 1.3 `v57` Rule-Wordings Benchmark

[v57_rule_wordings_benchmark](lean/TSR/MirrorFunctor.lean#L682-L687) tests exact prose reading rules from *SM v57* directly against the 17-row benchmark (`benchmarkRows17`, ported from [rule/tsr_formal_port.py](../rule/tsr_formal_port.py)):

| Rule / Model Encoding | Source Citation / Status | Match Count | Missed Rows | Structural Explanation |
| :--- | :--- | :---: | :--- | :--- |
| [`R_read_always_invert`](lean/TSR/MirrorFunctor.lean#L693) | `(c)` Constant baseline (`always-Invert`) | **3 / 17** | `1, 3–7, 10–17` | Matches only the 3 `.Invert` rows (`2, 8, 9`). |
| [`R_read_always_keep`](lean/TSR/MirrorFunctor.lean#L690) | `(c)` Constant baseline (`always-Keep`) | **14 / 17** | `2, 8, 9` | Matches all 14 `.Keep` rows; misses only the 3 `.Invert` rows (`2, 8, 9`). |
| [`R_read_ch2_clauses`](lean/TSR/MirrorFunctor.lean#L573-L574) | `(c)` Narrow `hasMass`-only proxy | **13 / 17** | `2, 11, 12, 17` | Misses Row 2 (`no shared now` / distance without mass), gravity rows `11–12`, and Boyle `17`. |
| [`R_read_v57_ch2`](lean/TSR/MirrorFunctor.lean#L656-L659) | *SM v57*, Ch. 2, p. 20 (`dependsOnResistanceOrSeparation`) | **14 / 17** | `11, 12, 17` | Adds `"or on the distance resistance makes"` (`SpatialSeparationDependence`), resolving Row 2; still lacks shared-energy work and boundary walls. |
| [`R_read_v57_ch16`](lean/TSR/MirrorFunctor.lean#L664-L667) | *SM v57*, Ch. 16, p. 116 (`+ isSharedEnergyWork`) | **16 / 17** | `17` | Adds `"or the work of the one energy both sides share"` (`.SharedCenterCurvature`), resolving Rows `11–12` and isolating Row 17 (`Boyle`). |
| [`R_read`](lean/TSR/MirrorFunctor.lean#L563-L564) (`two_level_reading_theorem`) | `(c)` 6-category `LawAST` + `IsothermalEquilibriumBalance` | **17 / 17** | None | **Note**: `17/17` requires hand-assigning laws to the six `LawAST` categories plus `(c)` `IsothermalEquilibriumBalance` for Row 17; in *SM v57* Ch. 16, p. 118, Boyle is instead explained because pressure requires walls, walls are resistance, and pressure exists only where the two sides touch. |

`benchmarkRows17` has 14 `Keep` rulings and 3 `Invert` rulings (`2, 8, 9`). As checked by [`constant_baselines_benchmark`](lean/TSR/MirrorFunctor.lean#L701-L710), `always-Keep` matches 14/17 and `always-Invert` matches 3/17. `R_read_v57_ch2` (14/17) ties `always-Keep`, and `R_read_v57_ch16` (16/17) beats it by two laws.

**17-Row Provenance (`"construction"` vs. `"applied later"`):** Nicholas built the table in *The Sovereign Mirror* from `E = mc^2` and Newton's mechanics, and confirmed provenance for the 17 benchmark rows before any held-out run:
- **`"construction"` (4 rows):** Row `7` (`7 E = mc^2`), Row `14` (`Newton's third law`), Row `15` (`m = density x volume`), and Row `16` (`F = ma`). All 4 have ruling `Keep` (`4/4` `Keep`); `always-Keep`, `R_read_v57_ch2`, and `R_read_v57_ch16` match `4/4` (`always-Invert`: `0/4`).
- **`"applied later"` (13 rows):** Rows `1–6`, `8–13`, and `17` (`1 laws same for every observer`, `2 no shared now (distance)`, `3 no fixed frame`, `4 special vs general`, `5 time dilation`, `6 length contraction`, `8 cost of more speed`, `9 mass can't reach c`, `10 space-time one continuum`, Row `11` gravity spacetime curvature, Row `12` gravity lensing, `13 conservation`, Row `17` Boyle's law). These 13 rows contain `10` `Keep` rulings and `3` `Invert` rulings (`2, 8, 9`). On these 13 applied-later rows, `always-Keep` matches `10/13`, `always-Invert` matches `3/13`, `R_read_v57_ch2` matches `10/13` (missing Rows `11, 12, 17`), and `R_read_v57_ch16` matches `12/13` (missing Row `17`).

Similarly, [gravity_open_joint_two_vs_three_regions](lean/TSR/EntityAndMeta.lean#L795-L812) shows via `decide` how adding shared-energy evaluation (code identifiers `.twoRegionNoSharedE` vs. `.threeRegionSharedE`, encoding *SM v57* Ch. 16 p. 117's `"two sides"` vs. `"three: the two sides and the continuum where they meet, with one energy in it"`) shifts Rows `11–12` from `.Invert` (`15/17`) to `.Keep` (`17/17`) while leaving the other 15 rows unchanged.

---

## 2. Part II — Structural & Lexical Uniqueness Checks in Z3 (Knowing-Targets Scope)

> [!IMPORTANT]
> **Disclosure on Hand-Written Inputs**: In both Part II.A ([structural_rigidity.py](z3/structural_rigidity.py#L375-L383)) and Part II.B ([lexical_rigidity.py](z3/lexical_rigidity.py#L1319-L1334)), all graph relations (`_build_stage_relations`), `CANDIDATES` feature flags, `SLOT_REQUIREMENTS` rules, and per-slot keyword concept groups (`DUAL_SENSE_POLYSEMY_SPECS` / `SINGLE_SENSE_DOMAIN_SPECS`) were **written by hand knowing the target words**. They are **not** target-blind derivations. What the Z3 solver establishes is: **no two terms in the Map, as encoded, are interchangeable**.

### 2.1 Part II.A — Unlabeled-Graph Automorphism Cascade (`S_29`)
Source: [structural_rigidity.py](z3/structural_rigidity.py#L95-L393)

Giving Z3 only integer node IDs `0..28` (representing the 29 Map slots without dictionary text or sort tags, across $29! = 8{,}841{,}761{,}993{,}739{,}701{,}954{,}543{,}616{,}000{,}000$ bijections), Z3 enumerates every graph automorphism across three cumulative relation layers:

| Stage | Encoded Structural Relations (*v57*) | $\|\mathrm{Aut}(\mathcal{S})\|$ | Fixed Nodes | Residual Orbit(s) |
| :--- | :--- | ---: | ---: | :--- |
| **Stage S1** (`S1_equations_crossing_containment`) | Algebraic equations + $V_4$ crossing topology + reality containment + 3 property pairs | **12** | **21 / 29** | `{limitless, receptive, collection}`, `{Awareness, Attraction, Momentum}`, `{Idle, Reflected}` |
| **Stage S2** (`S2_plus_map_cocreation_links`) | Stage S1 + *The Map* p. 172 cross-row links (`Tune → Attraction`, `Idle/Reflected → Momentum`) | **2** | **27 / 29** | `{Idle, Reflected}` |
| **Stage S3** (`S3_plus_ch2_stationary_vs_returning_polarity`) | Stage S2 + *SM v57* Ch. 2 pp. 26–27 stationary vs. returning polarity (`Idle` stationary vs. `Reflected` returning) | **1** | **29 / 29** | None (all 29 encoded slots uniquely fixed) |

Forcing a global sector swap (`A3-S`: $\sigma(\mathsf{NP}) = \mathsf{P}$) in [prove_two_sided_asymmetry_unsat](z3/structural_rigidity.py#L301-L359) returns **`UNSAT`** with minimal unsatisfiable core `["dynamical_structure_preservation", "hypothesis_swap_NP_and_P_sides", "thm_1_2_laminar_culmination_vs_damped_decay"]`.

### 2.2 Part II.B — Chapter 16 MUC Audit & Cross-Platform Dictionary Checks
Source: [lexical_rigidity.py](z3/lexical_rigidity.py) | WordNet payload: [wordnet_100_synsets.json](z3/wordnet_100_synsets.json) (`SHA-256: 9ae84ba4d9e8e0b2293862ed3e42bd86817b223220b549c8eb4c13511b765618`)

#### II.B.1 — Injective Map Uniqueness & 21 Deletion-Verified 1-Minimal MUCs
Across $P(30, 14) = 4{,}284{,}987{,}369{,}062{,}400{,}000$ injective assignments ([verify_tsr_sat_and_uniqueness](z3/lexical_rigidity.py#L490-L553)):
- **Cleaned Physical Control Flags** ([CANDIDATES](z3/lexical_rigidity.py#L135-L275)): `Focus` (`selects_receptivity_target = False`), `electric` (`means_poised_at_rest = False`), and `magnetic` (`means_returning_closed_loop = False`) carry physical-side features only, enforced at runtime (`physical_control_flags_cleaned`).
- **Pre-Continuum Tiebreak (`2`) & Unique Solution (`1`)**: Omitting `continuum_unfolding_sense` on `Expansion` leaves exact **2** assignments (`A0` and `A0[Expansion := growth]`, matching *SM v57* Ch. 16 p. 124); adding it leaves `A0` unique.
- **21 Deletion-Verified 1-Minimal `UNSAT` Cores**: All **17 book challengers** ([run_challenger_mucs](z3/lexical_rigidity.py#L576-L625)) and all **4 `A3` floor-control arms** ([run_a3_control_mucs](z3/lexical_rigidity.py#L647-L706) over [arms/a3_shuffled.py](../arms/a3_shuffled.py), breaking `14/14` slots each) return `UNSAT` with deletion-verified 1-minimal cores ([extract_verified_minimal_unsat_core](z3/lexical_rigidity.py#L445-L487)).

#### II.B.2 — 14-Slot Discrete-Sense Dictionary Checks (Princeton WordNet 3.0 & macOS Oxford)
While the per-slot keyword groups in [DUAL_SENSE_POLYSEMY_SPECS](z3/lexical_rigidity.py#L723-L776) and [SINGLE_SENSE_DOMAIN_SPECS](z3/lexical_rigidity.py#L778-L821) were written knowing targets, the lookup helpers use **zero per-word booleans**, **zero window-size parameters on discrete senses**, strip uppercase `ORIGIN` etymology before lowercasing on Oxford ([_split_oxford_discrete_senses](z3/lexical_rigidity.py#L1044-L1067)), and enforce zero target-stem circularity ([_validate_noncircular_slot_specs](z3/lexical_rigidity.py#L826-L848)) across the 100-word pool:
1. **Cross-Platform Princeton WordNet 3.0** ([verify_wordnet_synset_polysemy](z3/lexical_rigidity.py#L883-L1036)): Evaluates `776` synsets across `99/100` resolved words (`"vibrance": []` left unpatched because WordNet 3.0 indexes `-ancy` `vibrancy`) and matches all `14/14` slots (`7` dual-sense + `7` single-sense domain).
2. **macOS Oxford & Linux Cross-Platform Fallback** ([verify_blind_dictionary_polysemy](z3/lexical_rigidity.py#L1070-L1251) — key `"blind_oxford_dictionary_polysemy"` retained for schema compatibility; [verify_cross_platform_without_coreservices](z3/lexical_rigidity.py#L1254-L1301)): On macOS (`macos_coreservices_available = True`), New Oxford American Dictionary resolves `100/100` entries and is invariant across a uniform `[40, 60, 80, 100]` character-gap sweep (`all_slots_invariant_across_widths = True`; `6/7` match discrete-sense splits identically, while `Vibration` adds `'light'` under uniform char gaps). On Linux / non-macOS systems without `CoreServices`, `verify_blind_dictionary_polysemy()` deterministically executes against the checked-in Princeton WordNet 3.0 payload (`resolved_entries_count == 99`, `cross_platform_wordnet_status == "verified_cross_platform_princeton_wordnet_3_0"`, verified both via offline self-test and directly inside Linux Docker).

| Dual-Sense Slot (7) | WordNet 3.0 $(\|S_A\|,\|S_B\|)$ | WordNet 3.0 $S_A \cap S_B$ | Oxford $(\|S_A\|,\|S_B\|)$ | Oxford $S_A \cap S_B$ |
| :--- | :---: | :--- | :---: | :--- |
| `Current` | `(7, 5)` | `['current']` | `(10, 3)` | `['current']` |
| `Appreciation` | `(2, 2)` | `['appreciate', 'appreciation']` | `(4, 3)` | `['appreciate', 'appreciation']` |
| `Movement` | `(12, 2)` | `['movement']` | `(13, 1)` | `['movement']` |
| `Idle` | `(2, 1)` | `['idle']` | `(1, 1)` | `['idle']` |
| `Tune` | `(1, 1)` | `['tune']` | `(1, 1)` | `['tune']` |
| `Vibration` | `(7, 12)` | `['radiate', 'vibration']` | `(5, 12)` | `['vibration', 'wave']` |
| `Reflected` | `(2, 2)` | `['reflected', 'reflection']` | `(2, 4)` | `['reflected', 'reflection']` |

| Single-Sense Slot (7) | WordNet 3.0 Survivors (`99/100` resolved) | Oxford Survivors (`100/100` resolved) |
| :--- | :--- | :--- |
| `Expansion` | `['expand', 'expansion', 'field', 'growth']` | `['compression', 'expand', 'expansion', 'growth']` |
| `Frequency` | `['frequency']` | `['frequency']` |
| `Convergence` | `['converge', 'convergence']` | `['collect', 'converge', 'convergence']` |
| `Desire` | `['desire', 'want']` | `['desire']` |
| `Vibrance` | `['resonance']` (`"vibrance"` unindexed) | `['resonance', 'vibrance']` |
| `Future` | `['future', 'relation']` | `['future', 'now']` |
| `Intuition` | `['intuition']` | `['intuition']` |

---

## 3. Part III — Exact Rational Combinatorics of *What the Words Knew* (Proof 36)

Dataset: [ledger_80.json](etymology/ledger_80.json) (`80` words from *What the Words Knew*, **proof 36**, pp. 99–104: `36 family`, `19 outward first`, `7 household`, `5 inward first`, `4 either side`, `3 nothing to add`, `2 both ways`, `1 not used`, `1 a pun`, `1 no help`, `1 unknown`).  
Proof script: [combinatorial_proofs.py](etymology/combinatorial_proofs.py) (`fractions.Fraction` exact arithmetic throughout).

### 3.1 Pre-Declared Primary Confirmatory Test (Null Result)

To avoid multiple-testing distortion across post-hoc graph definitions, etymology conventions, and morphological filters, [combinatorial_proofs.py](etymology/combinatorial_proofs.py#L1537-L1591) isolates **strictly ONE pre-declared primary test** (`primary_test`):

- **TSR Graph**: `g_tsr_oct22_cdba80d` (`66` orthographically unrelated edges extracted mechanically from the pre-existing Oct 22 commit `cdba80d` file [tests/tsr_formal.py](../tests/tsr_formal.py), verified `SHA-256: 075fd22b9e4a9b91fa76bc433e4a754ca5faf57009fa0c071158711fba918ae0`).
- **Etymology Target**: `pie_roots_strict` (`16` orthographically unrelated PIE cognate pairs under strict modern laryngeal standards — de Vaan 2008 / *LIV²*, keeping `converge < *h₁uerg-` distinct from `vortex < *uert-`).
- **Orthographic Filter (`N_orth_unrelated = 3,152`)**: [shares_4char_substring](etymology/combinatorial_proofs.py#L289-L310) excludes all `8` pairs sharing a 4-character stem or productive Latinate `-mentum`/`-ment` root (`appreciate–radiate`, `collect–electric`, `expect–experience`, `express–present`, `express–pressure`, `momentum–movement`, `object–subject`, `present–pressure`), leaving **`3,152`** orthographically unrelated pairs out of $\binom{80}{2} = 3,160$.
- **Surface-Token Safeguard**: [SURFACE_TO_LEDGER](etymology/combinatorial_proofs.py#L220-L226) and [run_self_tests](etymology/combinatorial_proofs.py#L1594-L1778) audit `333` unique source tokens (`84` mapped) and block false friends (`real`, `reality`, `realities`, `moment`, `times`, `forceable`, `senses`, `limitless`).

**Primary Test Outcome (`PRIMARY_PRE_DECLARED_OCT22_CDBA80D_VS_STRICT_PIE`)**:

| Metric | Observed Value |
| :--- | :--- |
| Universe (`N_orth_unrelated`) | `3,152` |
| TSR Edges (`g_tsr_oct22_cdba80d`) | `66` |
| Strict PIE Cognate Edges (`pie_roots_strict`) | `16` |
| Expected Overlap (Hypergeometric Mean) | $\frac{66}{197} \approx 0.3350$ (`std ≈ 0.5714`, `z ≈ +1.1639`) |
| Observed Overlap | **`1 / 16`** — `["distance", "resist"]` (`< *stā-`) |
| Exact Hypergeometric Upper-Tail $p$ | $\frac{86446639322316364752811143688157099}{300368220274967343909714599772439787} \approx \mathbf{0.2878}$ |
| Verdict ($\alpha = 0.05$) | **NOT SIGNIFICANT (`NOT_STATISTICALLY_SIGNIFICANT_NULL_RESULT`)** |

**Plain reading**: Under the cleanest pre-existing graph (`cdba80d`) and strict modern PIE standard, cognate overlap is **`1` pair vs. `0.335` expected by chance ($p = 0.2878$)** — indistinguishable from chance overlap.

### 3.2 Uncorrected Exploratory Sensitivity Analyses

All remaining ~60+ `p`-values, alternative null controls, secondary graphs ([vocab/mirror.py](../vocab/mirror.py) and [rule/tsr_formal_port.py](../rule/tsr_formal_port.py), labeled **`"author-attested, first committed Nov 13"`**), Pokorny/diachronic root targets, legacy 4-char filtering (`N_orth_unrelated = 3,153`), center-crossing calque probabilities, and post-hoc book concordance numbers live exclusively inside `exploratory_sensitivity_uncorrected` ([combinatorial_proofs.py](etymology/combinatorial_proofs.py#L2205-L2321)). **None are corrected for multiple comparisons; they are sensitivity diagnostics, not confirmatory evidence.**

- **Alternative Null Controls on the Primary Pair (`g_tsr_oct22_cdba80d` vs. `pie_roots_strict`)**: Uniform $S_{80}$ vertex-pair QAP mean $\frac{132}{395} \approx 0.3342$ (`z = 1.1547`, Cantelli upper bound $0.4286$), exact polysemy-stratified mean $0.3154$ ($3.17\times$), exact `(POS, polysemy)`-stratified mean $0.2744$ ($3.64\times$), and `100,000`-trial stratified permutation (`seed=20191007`) `24,560 / 100,000` ($p_{\text{emp}} = 0.2456$, **not significant**).
- **Sensitivity Across Graphs, Root Standards, and Morphological Filters (Uncorrected)**:

| Graph (`Provenance`) | Etymology Target | Filter (`N_orth_unrelated`) | $\|E_{\text{TSR}}\|$ / $\|E_{\text{etym}}\|$ | Overlap | Overlapping Pairs | Uncorrected Hyper $p$ | Stratified Perm $p$ |
| :--- | :--- | :--- | :---: | :---: | :--- | :---: | :---: |
| `g_tsr_oct22_cdba80d` (Oct 22 commit) | `pokorny_pie` | Strict (`3,152`) | `66 / 17` | `1` | `distance–resist` | `0.3028` | `0.2456` |
| `g_tsr_oct22_cdba80d` (Oct 22 commit) | `diachronic_strict_pie` | Strict (`3,152`) | `66 / 18` | `2` | `desire–expect`, `distance–resist` | `0.0533` | `0.0331` |
| `g_tsr_oct22_cdba80d` (Oct 22 commit) | `diachronic_pokorny_pie` | Strict (`3,152`) | `66 / 19` | `2` | `desire–expect`, `distance–resist` | `0.0587` | `0.0331` |
| `g_tsr_oct22_pure_table` (Oct 22 commit) | `strict_pie` | Strict (`3,152`) | `54 / 16` | `0` | — | `1.0000` | `1.0000` |
| `g_tsr_oct22_pure_table` (Oct 22 commit) | `diachronic_pokorny_pie` | Strict (`3,152`) | `54 / 19` | `1` | `desire–expect` | `0.2806` | `0.2225` |
| `g_tsr_nov13_pure_table` (**author-attested, first committed Nov 13**) | `strict_pie` | Strict (`3,152`) | `67 / 16` | `1` | `energy–work` | `0.2915` | `0.2196` |
| `g_tsr_nov13_pure_table` (**author-attested, first committed Nov 13**) | `diachronic_pokorny_pie` | Strict (`3,152`) | `67 / 19` | `2` | `desire–expect`, `energy–work` | `0.0603` | `0.0294` |
| `g_tsr_nov13_frozen` (**author-attested, first committed Nov 13**) | `strict_pie` | Strict (`3,152`) | `182 / 16` | `2` | `distance–resist`, `energy–work` | `0.2352` | `0.1833` |
| `g_tsr_nov13_frozen` (**author-attested, first committed Nov 13**) | `pokorny_pie` | Strict (`3,152`) | `182 / 17` | `3` | `converge–vortex`, `distance–resist`, `energy–work` | `0.0708` | `0.0587` |
| `g_tsr_nov13_frozen` (**author-attested, first committed Nov 13**) | `diachronic_strict_pie` | Strict (`3,152`) | `182 / 18` | `3` | `desire–expect`, `distance–resist`, `energy–work` | `0.0815` | `0.0501` |
| `g_tsr_nov13_frozen` (**author-attested, first committed Nov 13**) | `diachronic_pokorny_pie` | Strict (`3,152`) | `182 / 19` | `4` | `+ desire–expect` | `0.0210` | `0.0137` |
| `g_tsr_oct22_cdba80d` (Legacy 4-char) | `diachronic_pokorny_pie` | Legacy (`3,153`) | `66 / 20` | `2` | `desire–expect`, `distance–resist` | `0.0644` | `0.0379` |
| `g_tsr_nov13_frozen` (Legacy 4-char, **first committed Nov 13**) | `diachronic_pokorny_pie` | Legacy (`3,153`) | `183 / 20` | `5` | `+ momentum–movement` | `0.00473` | `0.00311` |

- **Center-Crossing Coined Calque (`actual–energy`, Uncorrected)**: Greek *energeia* (`energy`) → Latin *actualitas* (`actualization`). Absent as an explicit string pair in both Oct 22 and Nov 13 programmatic graphs (`in_g_tsr_oct22_cdba80d = False`, `in_g_tsr_nov13_frozen = False`), its exact uniform pair fraction is $\frac{1}{3152} \approx 3.17 \times 10^{-4}$ ($\frac{1}{1576}$ either transmutation edge; $\frac{1}{17}$ conditioned on the `17` process words).
- **Quarantined Post-Hoc Concordance**: `g_tsr_canonical` ([CANONICAL_TSR_EDGES_RAW](etymology/combinatorial_proofs.py#L485-L597), `109` strict edges, `11/16` strict PIE, `14/19` diachronic Pokorny) was compiled *after* reading *WTWK* and includes thematic prose links (`actual–energy`, `being–future`, `exist–resist`, `tension–tune`, etc.); it is strictly post hoc and non-confirmatory.

### 3.3 Descriptive Core-Law Directionality Summary (Post-Hoc, Not Inferential)

Source function: [run_descriptive_core_law_directionality_audit](etymology/combinatorial_proofs.py#L1299-L1513) (`inferential_status = "DESCRIPTIVE_ONLY_POST_HOC_SPLIT_NOT_INFERENTIAL"`).

Two methodological limits prevent these numbers from acting as inferential $p$-values:
1. All `kind` labels in [ledger_80.json](etymology/ledger_80.json) (`36 family`, `19 outward first`, `7 household`, `5 inward first`, `4 either side`, `3 nothing to add`, `2 both ways`, `1 a pun`, `1 no help`, `1 not used`, `1 unknown`) were **assigned by the author while drafting *What the Words Knew* (*proof 36*, pp. 99–104), not blind**.
2. Splitting the `35` physics-eligible words into `21 core_law` vs. `14 secondary_physics` is **post hoc** (and all `45 not_physics_term` words are `0/45` by definition; *WTWK proof 36* p. 99 reads: *"Inward first is the rare kind: a word for a state of a person that was later handed to physics."*).

Reported purely as **descriptive ledger ratios**:
- **Directional `core_law` vs. `secondary_physics`**: `5` inward / `1` outward (`energy, force, inertia, power, work` vs. `attraction`) vs. `0` inward / `8` outward — exact contingency fraction $\frac{\binom{6}{5}\binom{8}{0}}{\binom{14}{5}} = \frac{3}{1001} \approx 0.00300$ (Haldane-Anscombe OR $= \frac{187}{3} \approx 62.33$).
- **All `35` eligible physics words (`inward` vs. all others)**: `5/21` in `core_law` vs. `0/14` in `secondary_physics` — contingency fraction $\frac{\binom{21}{5}\binom{14}{0}}{\binom{35}{5}} = \frac{171}{2728} \approx 0.06268$.
- **Book-only holdout (`work`, `power` held out to Oct 22 / Oct 2026 sources)**: `3/4` vs. `0/8` ($\frac{1}{55} \approx 0.0182$), `3/19` vs. `0/14` ($\frac{969}{5456} \approx 0.1776$), `3/4` vs. `2/10` ($\frac{95}{1001} \approx 0.0949$).
- **Descriptive binomial tails against reference base rates $q_0 \in \{0.05, 0.10, 0.15\}$**:
  - `directional_core_law_5_of_6`: `1.80e-6` ($5\%$), `5.50e-5` ($10\%$), `3.99e-4` ($15\%$).
  - `worst_case_nonfamily_core_law_5_of_14` (because *proof 36* p. 102 classifies `light` as `family`, leaving `14` non-family core words): `4.27e-4` ($5\%$), `9.23e-3` ($10\%$), `0.0467` ($15\%$).
  - `all_core_law_5_of_21`: `3.24e-3` ($5\%$), `0.0522` ($10\%$), `0.1975` ($15\%$).
- **Full 80-word tally**: `5/21` in `core_law`, `0/14` in `secondary_physics`, `0/45` structurally ineligible (`153/180752 ≈ 8.46e-4`).

The held-out control sampling and coding setup intended to address the post-hoc selection limit above (Part 3) is documented in [Section 5](#5-part-v--held-out-etymology-direction-control-proofheldout-part-3).

---

## 4. Part IV — Held-Out Law Evaluation (proof/heldout/, Part 2)

Claim tested: The one rule as printed in The Sovereign Mirror v57 (pp. 20 and 116) is enough to rule on a law it was not built from

- **Overall Primary Verdict**: **FAIL (`passes_all_three = false`)**. Across `3` standalone evaluation sessions on the `48` held-out OpenStax laws, Conditions 2 and 3 pass (`BA = 9/10 = 0.9000`, `L_BA = 0.7370 > 0.50`, Fisher $p = 45/177232627 \approx 2.5390 \times 10^{-7} < 0.05$), while **Condition 1 fails** (`3`-category Fleiss' $\kappa = 2447/5039 \approx 0.4856 < 0.60$). Under the shared-session protocol (`Amendments 1–2`), Conditions 2–3 measure **within-session codebook-to-prose consistency** rather than an independent cross-session check.

### 4.1 Corpus, Protocol & Disclosure Notes

- **Sources & Attribution**: External laws were extracted from all `22` chapters of the OpenStax *University Physics* frozen bundle (`bundle_commit_sha = 2300d5b8ca2571dacc6ec25ebef56ba8d49000a2`; [openstax_fetch_manifest.json](heldout/openstax_fetch_manifest.json), [openstax_key_equations_raw.csv](heldout/openstax_key_equations_raw.csv)) — *Access for free at https://openstax.org — Licensed under CC BY 4.0.* Deterministic exclusions ([exclusion_log.csv](heldout/exclusion_log.csv), [eligible_laws_pool.csv](heldout/eligible_laws_pool.csv)), sampling (`48` held-out laws, [sample_manifest.csv](heldout/sample_manifest.csv)), and redaction/interleaving with the `17` Lean benchmark rows (`65` total anonymized cards `C001..C065`, [law_cards.csv](heldout/law_cards.csv)) are generated by [fetch_and_sample_laws.py](heldout/fetch_and_sample_laws.py), [build_law_cards.py](heldout/build_law_cards.py), and [build_evaluation_packets.py](heldout/build_evaluation_packets.py) into [combined_evaluation_packet.md](heldout/combined_evaluation_packet.md).
- **Commit Provenance SHAs**:
  - `preregistration_commit_sha`: `463ad9f93c8a276b1e0d9ee497198dfa2169d079` ([PREREGISTRATION.md](heldout/PREREGISTRATION.md))
  - `amendment_1_commit_sha`: `b66f48efb76e0f8d17d7db32848ad95f0a5c8633` (disclosing `q4` Option 3 scope sentence)
  - `amendment_2_commit_sha`: `530a254a51789a9fd68e1889f713b86d829c1146` (authorizing combined single-session collection under `A1` Option 3, `A2` Option 2, and `A4` Option 2)
  - `pre_unmasking_commit_sha`: `5f5c828d2d8dc32b53de887b9faa6ad214faf8e6`
- **Model Panel & Artifacts**: Primary 3-session panel in [ingest_sessions.py](heldout/ingest_sessions.py), [appliers.csv](heldout/appliers.csv), and [labels.csv](heldout/labels.csv) consists of `s1 = gemini_carbon`, `s2 = grok_4_7`, and `s3 = kimi_k3`; a 4th archived run (`gemini_hydrogen`) is analyzed solely for descriptive sensitivity and excluded from primary inference. Full exact rational results live in [part2_results.json](heldout/part2_results.json) (computed by [evaluate_part2.py](heldout/evaluate_part2.py)).
- **Shared-Session & Audit Limitations**: Under Amendment 2 (`shared_session_disclosure`), Track `(b)` rulings (`b1..b3`) and Track `(c)` codebook flags (`q1..q4`) were produced in the same model session, so Condition 2/3 tests whether each session's rule application agrees with predictions from its own codebook readings. In `s3` (`kimi_k3`), the paste for `C065.rationale` truncated mid-sentence (`"Bulk modulus explicitly \"measures a material's resistance to uniform hydrostatic compression\"; since [truncated in paste]"`); its ruling (`"Invert"`) and `q1..q4` values are intact.

### 4.2 Held-Out 48 Primary Results (`never_pooled_with_calibration_17`)

#### Confirmatory Primary Gate Summary

| Check | Exact Quantity Tested | Result | Threshold / Criterion | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| Condition 1 (Across-family agreement) | 3-cat Fleiss' $\kappa$ across `b1, b2, b3` (`N = 48`) | `2447/5039` (`0.4856`, unanimous `31/48 = 64.58%`) | `>= 0.60` | **FAIL** |
| Condition 2 (95% CI lower bound) | `pred_ch16` vs definite `b_maj_ruling` (`N_def = 44`) | `BA = 9/10` (`0.9000`), Wilson-MOVER `CI = [0.7370, 0.9717]` | `L_BA > 0.50` | **PASS** (within-session) |
| Condition 3 (Fisher exact test) | `TP=8, FP=0, FN=2, TN=34` (`pred_ch16` vs `b_maj_ruling`) | One-sided $p = 45/177232627 \approx 2.5390 \times 10^{-7}$ | `p < 0.05` | **PASS** (within-session) |
| **Overall Primary Gate** | **`passes_all_three`** (`C1 AND C2 AND C3`) | **`false`** | All three pass | **FAIL** |

- **Inter-session Agreement Detail**: Across all `144` held-out Track `(b)` ratings (`48 × 3`), category counts are `Keep = 97`, `Invert = 32`, and `"the rule doesn't say" = 15` (`P_bar = 3/4 = 0.7500`, `P_e = 5329/10368 ≈ 0.5140`). Usage of `"the rule doesn't say"` is concentrated in `b1` (`gemini_carbon`: `12/48 = 25.0%`) versus `b2` (`grok_4_7`: `1/48`) and `b3` (`kimi_k3`: `2/48`). On the `35/48` subset where all three sessions gave a definite `Keep`/`Invert` ruling (`Keep = 75`, `Invert = 30`), 2-category Fleiss' $\kappa = 61/75 \approx 0.8133$ (`unanimous = 31/35`).
- **Track `(c)` Inter-session Agreement (`N = 48`)**: Two-category Fleiss' $\kappa$ on codebook flags is `q1 = 359/551 ≈ 0.6515` (`36/48` unanimous, `Yes=87, No=57`), `q2 = 935/1007 ≈ 0.9285` (`46/48` unanimous, `Yes=38, No=106`), `q3 = 251/323 ≈ 0.7771` (`40/48` unanimous, `Yes=68, No=76`), and `q4 = 119/155 ≈ 0.7677` (`44/48` unanimous, `Yes=20, No=124`).

#### Predictors vs. Majority Ruling `b_maj_ruling` (`N = 48` & `N_def = 44`)

| Rule / Baseline Predictor | Unconditional Matches (`48`) | Uncond. 4-cat Cohen's $\kappa$ | Definite `N_def = 44` Acc | `TPR` / `TNR` | Balanced Acc (`BA`) | 95% Wilson-MOVER CI | One-sided Fisher $p$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`pred_ch16`** (primary) | `42/48` (`0.8750`) | `13/19` (`0.6842`) | `21/22` (`0.9545`) | `4/5` (`0.8000`) / `1/1` (`1.0000`) | `9/10` (`0.9000`) | `[0.7370, 0.9717]` | `45/177232627` (`2.5390e-07`) |
| `pred_ch2` (no `q4` carve-out) | `37/48` (`0.7708`) | `21/43` (`0.4884`) | `37/44` (`0.8409`) | `4/5` (`0.8000`) / `29/34` (`0.8529`) | `281/340` (`0.8265`) | `[0.6534, 0.9092]` | `2171/8675723` (`2.5024e-04`) |
| `pred_naive_mass` (`q2 == Yes`) | `28/48` (`0.5833`) | `0/1` (`0.0000`) | `7/11` (`0.6364`) | `3/10` (`0.3000`) / `25/34` (`0.7353`) | `44/85` (`0.5176`) | `[0.3905, 0.6805]` | `4845983/8675723` (`0.5586`) |
| `R_read_always_keep` | `34/48` (`0.7083`) | — | `17/22` (`0.7727`) | `0/1` (`0.0000`) / `1/1` (`1.0000`) | `1/2` (`0.5000`) | `[0.4492, 0.6388]` | `1/1` (`1.0000`) |
| `R_read_always_invert` | `10/48` (`0.2083`) | — | `5/22` (`0.2273`) | `1/1` (`1.0000`) / `0/1` (`0.0000`) | `1/2` (`0.5000`) | `[0.3612, 0.5508]` | `1/1` (`1.0000`) |

- **Individual Appliers vs. `pred_ch16`**:
  - Across all `48` laws: `b1` (`gemini_carbon`) matches `2/3 = 32/48` (`0.6667`, `TPR=9/10`, `TNR=23/38`, `BA=143/190 = 0.7526`, CI `[0.5812, 0.8333]`); `b2` (`grok_4_7`) matches `7/8 = 42/48` (`0.8750`, `TPR=3/5`, `TNR=18/19`, `BA=147/190 = 0.7737`, CI `[0.6180, 0.8911]`); `b3` (`kimi_k3`) matches `43/48` (`0.8958`, `TPR=9/10`, `TNR=17/19`, `BA=341/380 = 0.8974`, CI `[0.7308, 0.9493]`).
  - Restricted to definite `b_maj` (`N_def = 44`): `b1` `31/44` (`0.7045`, `BA=59/72 = 0.8194`, CI `[0.6379, 0.8876]`); `b2` `10/11` (`40/44 = 0.9091`, `BA=61/72 = 0.8472`, CI `[0.6656, 0.9387]`); `b3` `21/22` (`42/44 = 0.9545`, `BA=35/36 = 0.9722`, CI `[0.7982, 0.9923]`).

#### Misses, Unanimous False Negatives & Non-Definite Cards (`part2_disagreements.csv`)

[part2_disagreements.csv](heldout/part2_disagreements.csv) records all `19` held-out laws (`C002, C003, C004, C008, C012, C020, C026, C031, C033, C041, C044, C048, C049, C051, C059, C061, C062, C064, C065`) where either `b1..b3` disagreed, `b_maj` was non-definite, or `b_maj`, `pred_ch2`, and `pred_ch16` diverged:

1. **Two Unanimous `Invert` Misses (`b_maj = Invert`, `pred_ch16 = Keep`)**:
   - `C004` (`H051`, Vol. 1 Ch. 6, *Magnitude of kinetic friction*, $f_k = \mu_k N$): all three sessions ruled `Invert`, and all three coded `q1..q4 = (No, No, No, No)` $\to$ `pred_ch16 = Keep` (surface resistance without an explicit mass or spatial separation variable).
   - `C065` (`H124`, Vol. 1 Ch. 12, *Bulk modulus*, $B = -\Delta p (V_0/\Delta V)$): all three sessions ruled `Invert` (`kimi_k3` rationale truncated in paste), and all three coded `q1..q4 = (No, No, No, No)` $\to$ `pred_ch16 = Keep` (hydrostatic compression resistance without an explicit mass or spatial separation term).
2. **Two Majority `"the rule doesn't say"` Cards**: `C020` (`H215`, *Thermal expansion in three dimensions*: `b1=doesn't say, b2=Keep, b3=doesn't say`) and `C049` (`H209`, *Observed frequency for a moving observer and a stationary source*: `b1=doesn't say, b2=Keep, b3=doesn't say`).
3. **Two `"no_majority"` 3-Way Splits**: `C002` (`H213`, *Linear thermal expansion*: `b1=doesn't say, b2=Keep, b3=Invert`) and `C003` (`H191`, *Wavelength for symmetric boundary conditions*: `b1=Invert, b2=doesn't say, b3=Keep`).
4. **Nine Additional `b1 = "the rule doesn't say"` Cards (`b2 = b3 = Keep` $\to$ `b_maj = Keep`)**: `C008` (*Orbital period*), `C012` (*Ideal gas law in terms of molecules*), `C026` (*Work done going from A to B by Earth's gravity, near its surface*), `C041` (*Condition for an ideal gas in a quasi-static adiabatic process*), `C044` (*Performance coefficient of a reversible refrigerator*), `C051` (*Kepler's third law*), `C059` (*Molar heat capacity at constant volume for an ideal gas with d degrees of freedom*), `C061` (*Newton's law of gravitation*), and `C064` (*Height of free fall*).

### 4.3 Separate Calibration Check on `benchmarkRows17` (`n = 17`, Never Pooled)

Static Lean benchmark checks on `benchmarkRows17` (`3`-predicate book wording rules): `lean_R_read_v57_ch2 = 14/17` (`missed = [11, 12, 17]`), `lean_R_read_v57_ch16 = 16/17` (`missed = [17]`), `always_keep = 14/17`, `always_invert = 3/17` (`matched = [2, 8, 9]`).

Running the redacted interleaved `benchmarkRows17` cards (`17` total: `4 construction` rows `[7, 14, 15, 16]` all `Keep`, and `13 applied later` rows `[1..6, 8..13, 17]`, `10 Keep / 3 Invert`) through the fresh sessions gives:

- **Inter-session Agreement on `17`**: 3-category Fleiss' $\kappa = 335/692 \approx 0.4841$ (`unanimous = 10/17`); on the `11/17` unanimously definite subset, 2-category Fleiss' $\kappa = 149/182 \approx 0.8187`.
- **Track `(b)` vs. `book_ruling` (`17`)**: `b_maj_ruling = 13/17` (`b1 = 11/17`, `b2 = 12/17`, `b3 = 13/17`), `pred_ch16 = 14/17`, `pred_ch2 = 12/17`, `pred_naive_mass = 9/17`, compared to `always-Keep = 14/17`.
  - **`construction` split (`4` rows)**: `b_maj_ruling = 3/4` (`b1 = 3/4, b2 = 3/4, b3 = 3/4`), `pred_ch16 = 3/4`, `pred_ch2 = 3/4`, `pred_naive_mass = 1/4`, vs. `always-Keep = 4/4`. On Row `16` (`C027`, $F = ma$), where the prose cue `"force is mass times acceleration"` was redacted under `A2` Option 2, **all three Track `(b)` sessions (`b1..b3`) and all three Track `(c)` codebooks (`q1_maj = No, q2_maj = Yes`) inverted $F = ma$**, opposite `book_ruling = Keep`.
  - **`applied later` split (`13` rows)**: `b_maj_ruling = 10/13` (`b1 = 8/13, b2 = 9/13, b3 = 10/13`), `pred_ch16 = 11/13`, `pred_ch2 = 9/13`, `pred_naive_mass = 8/13`, vs. `always-Keep = 10/13`.
  - **Four `b_maj_ruling` Misses on `17`**:
    - Row `5` (`C005`, `5 time dilation`, `book = Keep`): `b1=Invert, b2=doesn't say, b3=doesn't say` $\to$ `b_maj = "the rule doesn't say"` (`pred_ch16 = Keep`).
    - Row `6` (`C063`, `6 length contraction`, `book = Keep`): `b1=Invert, b2=doesn't say, b3=Invert` $\to$ `b_maj = Invert` (`q3_maj = Yes`, `pred_ch16 = Invert`).
    - Row `8` (`C011`, `8 cost of more speed`, `book = Invert`): `b1=Invert, b2=Keep, b3=Keep` $\to$ `b_maj = Keep` (`q1_maj = Yes`, `pred_ch16 = Keep`).
    - Row `16` (`C027`, `F = ma`, `book = Keep`): `b1=Invert, b2=Invert, b3=Invert` $\to$ `b_maj = Invert` (`q1_maj = No, q2_maj = Yes`, `pred_ch16 = Invert`).
  - Note also Row `17` (`C014`, Boyle's law, `book = Keep`, `lean_R_read_v57_ch16 = Invert`): sessions gave `b_maj = Keep` (`b1=doesn't say, b2=Keep, b3=Keep`) and `pred_ch16 = Keep`.
- **Track `(c)` vs. Lean Ground-Truth Predicates on `17`**: Fleiss' $\kappa$ on `q1..q4` is `271/322 ≈ 0.8416` (`q1`), `1/1` (`q2`), `1/1` (`q3`), `1/1` (`q4`); `q_maj` matches Lean predicates `14/17` on `q1` ($\kappa = 92/143 \approx 0.6434$, mismatch `[8, 16, 17]`), `16/17` on `q2` ($\kappa = 128/145 \approx 0.8828$, mismatch `[4]`), `13/17` on `q3` ($\kappa = 6/23 \approx 0.2609$, mismatch `[6, 10, 11, 12]`), `16/17` on `q4` ($\kappa = 56/73 \approx 0.7671$, mismatch `[4]`), yielding `pred_ch16` vs. `lean_R_read_v57_ch16` agreement `13/17` (mismatch `[6, 8, 16, 17]`). Within-session `b_maj_ruling` vs. `pred_ch16` on `17` is `16/17` (mismatch `[5]`, `16/16` on definite rows).

### 4.4 Descriptive Sensitivity Run (`gemini_hydrogen`)

Substituting `gemini_hydrogen` for `gemini_carbon` (`(gemini_hydrogen, grok_4_7, kimi_k3)`) does not change the confirmatory outcome (`would_pass_all_three_if_primary = false`): Condition 1 remains below threshold with 3-category Fleiss' $\kappa = 2051/3779 \approx 0.5427 < 0.60$ (`45/48` unanimously definite, 2-cat $\kappa = 17/27 \approx 0.6296$; `N_def = 45`, `pred_ch16` vs. definite `b_maj`: `TP=9, FP=0, FN=2, TN=34`, `acc = 43/45 = 0.9556`, `BA = 10/11 ≈ 0.9091`, CI `[0.7530, 0.9743]`, Fisher $p = 1/16112057 \approx 6.2065 \times 10^{-8}$). On `calibration_17`, swap-in agreement is `b_maj vs book = 13/17` (`3/4` construction, `10/13` applied later), `s1_extra vs book = 13/17`, and `b_maj vs pred_ch16 = 16/17` (3-cat $\kappa = 244/295 \approx 0.8271$). Across all `4` archived runs combined (`s1, s2, s3, extra`), 3-category Fleiss' $\kappa = 959/2111 \approx 0.4543$ on `48` and `177/296 ≈ 0.5980` on `17`.

---

## 5. Part V — Held-Out Etymology Direction Control (proof/heldout/, Part 3)

**Status**: **Corpus preparation, deterministic exclusions, `40`-word control draw, and anonymized `78`-word single-source coding packet complete; external `etymonline.com` session collection and statistical scoring are pending (not yet run).**

To replace the post-hoc core-law directionality split documented in [Section 3.3](#33-descriptive-core-law-directionality-summary-post-hoc-not-inferential), [prepare_part3_etymology.py](heldout/prepare_part3_etymology.py) builds the preregistered external control pool and anonymized coding packet following [PREREGISTRATION.md](heldout/PREREGISTRATION.md) Section 3:

1. **External Control Extraction (`openstax_key_terms_raw.csv`)**: Fetches all `153` CNXML modules across the same `22` chapters of the frozen OpenStax *University Physics* bundle (`bundle_commit_sha = 2300d5b8ca2571dacc6ec25ebef56ba8d49000a2`, SHA-256 verified per module URL in [openstax_fetch_manifest.json](heldout/openstax_fetch_manifest.json)) and extracts `<glossary><definition><term>` headwords verbatim without `<meaning>` prose, yielding `454` raw entries ([openstax_key_terms_raw.csv](heldout/openstax_key_terms_raw.csv)).
2. **Deterministic Filtering & Exclusions `C1`–`C3` ([control_exclusion_log.csv](heldout/control_exclusion_log.csv))**:
   - Retains `101` unique lowercase single-word (`^[a-z]+$`) candidates verbatim (no case-folding).
   - Applies preregistered exclusions against all `80` words in [ledger_80.json](etymology/ledger_80.json) and the `10` confirmed physical quantity targets (`acceleration, density, energy, force, mass, space, speed, time, velocity, volume`):
     - `C1_IN_LEDGER_80` (`11`): `density, force, friction, inertia, momentum, power, pressure, resonance, tension, wave, work`.
     - `C2_CONFIRMED_TARGET` (`0`): (`density` and `force` match `C1` first; `acceleration, speed, velocity` do not appear as standalone lowercase `<term>` entries).
     - `C3_MORPHOLOGICAL_VARIANT` (`1`): `radiation` (Latinate/affix root of `radiate`).
   - Leaves `89` eligible control candidates (`>= 40`). Two audited edge cases remain eligible under the `PREREGISTRATION.md` affix rule: `wavelength` (compound `wave` + `length`) and `compressibility` (`com-` prefix, not in `{un-, in-, im-, non-, re-}`).
3. **Sample Draw & Anonymized Coding Packet (`seed = 20261113`)**:
   - Draws `controls_40 = random.Random(20261113).sample(eligible_controls, 40)` (`100%` disjoint from both `ledger_80` and `targets_10`).
   - Forms the `78`-word unified coding pool: `35` physics-eligible words from `ledger_80.json` (`ledger_physics_35`) $+$ `3` remaining target nouns (`acceleration, speed, velocity`, since `7` overlap: `density, energy, force, mass, space, time, volume`) $+$ `40` OpenStax controls, shuffled with `seed = 20261113` as `W001..W078`.
   - Emits the withheld answer key [word_coding_key.csv](heldout/word_coding_key.csv), the ID/word packet [word_coding_packet.csv](heldout/word_coding_packet.csv), and the standalone coding prompt [etymology_coding_prompt.md](heldout/etymology_coding_prompt.md) (`source_coverage = "single-source"` on `https://www.etymonline.com` only, no quoted dictionary prose allowed, zero group/stratum/TSR identifiers).
4. **Offline Reproducibility & Confirmatory Analysis Spec (Pending Data)**: `prepare_part3_etymology.py --verify-offline` checks byte-for-byte parity from `openstax_key_terms_raw.csv` with zero network requests and enforces hex-encoded repo/leak hygiene checks. Once `3` standalone external `etymonline.com` sessions are collected and ingested, the preregistered primary check tests two-sided Fisher exact enrichment of `"person_first"` among `targets_10` versus `controls_40`.

---

## 6. Part VI — Cross-Platform CI & 15-Mutation Verification Audit (Part 4)

### 6.1 Automated GitHub Actions Workflow ([verify-proofs.yml](../.github/workflows/verify-proofs.yml))

Continuous integration runs on `ubuntu-latest` with Python `3.12`, `z3-solver==5.4.1`, and Lean `v4.35.0` (exact toolchain versions parity-checked against [run_all_proofs.py](run_all_proofs.py)), builds and runs `PYTHONDONTWRITEBYTECODE=1 python -B proof/run_all_proofs.py`, and verifies that the freshly generated [verification_certificate.json](verification_certificate.json) matches the committed certificate on all source hashes and proof checks, permitting differences only on `5` declared runtime/environment fields (`execution_os`, `execution_arch`, `python_version`, `lean_version`, `verification_runtime_seconds`).

### 6.2 Independent 15-Mutation Suite ([run_mutation_suite.py](heldout/run_mutation_suite.py) → [mutation_results.json](heldout/mutation_results.json))

In addition to positive theorem/solver runs, [run_mutation_suite.py](heldout/run_mutation_suite.py) applies `15` targeted adversarial mutations in isolated temporary repository copies (executed on Linux `aarch64`, Python `3.12.15`) to confirm each proof gate actually rejects broken definitions, dropped assumptions, weakened Z3 graphs, or altered combinatorial counts. **All `15/15` mutations were caught (`0` surviving, `all_caught = true`)**:

| ID | Target File | Mutated Symbol / Construct | Failing Verifier Check | Outcome |
| :--- | :--- | :--- | :--- | :--- |
| `M01` | `proof/lean/TSR/Condition.lean` | `barrier` (Lean definition) | `lake build` fails at `condition_triad_equivalence` / `destructive_null_requires_spatial_separation` | Caught (`exit 1`) |
| `M02` | `proof/lean/TSR/Condition.lean` | `condition_triad_equivalence` assumption | `lake build` fails at `condition_triad_equivalence` (missing partition assumption `hPart`) | Caught (`exit 1`) |
| `M03` | `proof/lean/TSR/Condition.lean` | `damped_ripple_strict_decay` assumption | `lake build` fails at `damped_ripple_strict_decay` (`M.alpha_bounds_of_pos hRes` type mismatch) | Caught (`exit 1`) |
| `M04` | `proof/lean/TSR/MirrorFunctor.lean` | `mirrorAtom` (Lean definition) | `lake build` fails at `mirrorAtom_involutive` / `R_form_involutive` | Caught (`exit 1`) |
| `M05` | `proof/lean/TSR/MirrorFunctor.lean` | `regionResistant` (Lean definition) | `lake build` fails at `two_level_reading_theorem` and `gravity_open_joint_two_vs_three_regions` | Caught (`exit 1`) |
| `M06` | `proof/lean/TSR/MirrorFunctor.lean` | `benchmarkRows17` Row 2 | `lake build` fails at `two_level_reading_theorem` and `v57_rule_wordings_benchmark` | Caught (`exit 1`) |
| `M07` | `proof/lean/TSR/MirrorFunctor.lean` | `benchmarkRows17` Row 7 | `lake build` fails at `two_level_reading_theorem` and `v57_rule_wordings_benchmark` | Caught (`exit 1`) |
| `M08` | `proof/lean/TSR/MirrorFunctor.lean` | `isSharedEnergyWork` (Lean definition) | `lake build` fails at `v57_rule_wordings_benchmark` (`R_read_v57_ch16` drops `16 -> 14`) | Caught (`exit 1`) |
| `M09` | `proof/lean/TSR/Crossing.lean` | `canStep` (Lean definition) | `lake build` fails at `step_from_intuition_false` and `unique_weak_diagonal_escape` | Caught (`exit 1`) |
| `M10` | `proof/lean/TSR/EntityAndMeta.lean` | `sovereignEntityDyn` (Lean definition) | `lake build` fails at `four_way_entity_separation` | Caught (`exit 1`) |
| `M11` | `proof/z3/structural_rigidity.py` | `_build_stage_relations` (Stage 2) | `run_structural_rigidity()` raises `AssertionError: Expected 2 at Stage 2, got 4` | Caught (`exit 1`) |
| `M12` | `proof/z3/structural_rigidity.py` | `_build_stage_relations` (Stage 3) | `run_structural_rigidity()` raises `AssertionError: Expected 1 at Stage 3, got 2` | Caught (`exit 1`) |
| `M13` | `proof/z3/lexical_rigidity.py` | `SLOT_REQUIREMENTS["Expansion"]` | `verify_tsr_sat_and_uniqueness()` raises `AssertionError` (uniqueness violated) | Caught (`exit 1`) |
| `M14` | `proof/etymology/combinatorial_proofs.py` | `shares_4char_substring` | `verify_part3_invariants()` fails (`N_orth_unrelated` shifts `3152 -> 3153`) and self-tests fail | Caught (`exit 1`) |
| `M15` | `proof/etymology/combinatorial_proofs.py` | `exact_hypergeometric_upper_tail` | `verify_part3_invariants()` fails (`p` shifts out of `0.287 < p < 0.289` to `0.0429`) | Caught (`exit 1`) |

---

## 7. Single-Command Reproduction

From the repository root on either macOS or Linux (requiring Lean `v4.35.0` via `elan` and Python `3.12` + `z3-solver`):

```bash
python proof/run_all_proofs.py
```

This single command compiles the Lean 4 suite (`0 sorry`, `0 warnings`, negative nominal-type check, 35-item `#print axioms` audit), runs Z3's $S_{29}$ automorphism solver, 21 1-minimal MUC extractors, and 14-slot WordNet 3.0 + live Oxford / Linux fallback dictionary checks, runs all exact rational 80-word combinatorial audits and self-tests, and writes [verification_certificate.json](verification_certificate.json) with runtime OS/architecture metadata and SHA-256 hashes of all verified source files.

To replay the offline held-out Part 2 scoring and Part 3 packet generation checks (zero network requests):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B proof/heldout/evaluate_part2.py --verify-offline
PYTHONDONTWRITEBYTECODE=1 python3 -B proof/heldout/prepare_part3_etymology.py --verify-offline
```
