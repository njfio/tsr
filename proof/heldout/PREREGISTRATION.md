# Preregistered Protocol for Held-Out Validation and Verification Hygiene (Parts 2–4)

**Status:** Locked initial preregistration at Commit 2 (`463ad9f93c8a276b1e0d9ee497198dfa2169d079`, branch `feat/heldout-preregistration`; pre-data decisions `A1`–`A4` confirmed before any OpenStax data was fetched) + Pre-Results Amendment 1 (Commit 6, prior to any Track `(b)` or Track `(c)` execution).  
**Epistemic Contract:** Governed by Section 0 of [`proof/PROOF.md`](../PROOF.md). All confirmatory hypotheses, sampling seeds, exclusion rules, boundary flags, and statistical tests below are fixed before any held-out dataset is retrieved.

---

## 0. Pre-Data Attestation, Reference Commits, and Execution Gate

### 0.1 Frozen Reference Commits
- **Prior theory & formal proof freeze:** `df6d8fbab8aec198ac4d6af58455a206f8bc6ebd`
- **Upstream `main` merge base:** `ec8a85b89f82c2c8a3f9a73492c9c2ac49a68809`
- **Part 0 constant-baseline & 17-row provenance commit (`COMMIT_1_SHA`):** `eb7cb044725beb2572cfe9c657e3309df2aca55c` (added `R_read_always_keep`, `R_read_always_invert`, and `constant_baselines_benchmark` in `proof/lean/TSR/MirrorFunctor.lean`, and locked the 17-row provenance in `proof/PROOF.md` Section 1.3)
- **Preregistration commit (`preregistration_commit_sha`):** The 40-character commit SHA of Commit 2 creating this locked file (`proof/heldout/PREREGISTRATION.md`).

### 0.2 Pre-Data Attestation
At the time this file is locked and committed (Commit 2):
1. Zero OpenStax *University Physics* `"Key Equations"` rows and zero OpenStax `"Key Terms"` headwords have been fetched, stored, or inspected. (Only the table-of-contents chapter list across Volumes 1–3 was checked to verify chapter numbers and titles.)
2. Zero `etymonline.com` or OED entries have been fetched or recorded for any Part 3 held-out target word or control word beyond the existing 80-word ledger already committed at `proof/etymology/ledger_80.json`.
3. Only already-committed repository files at `eb7cb044725beb2572cfe9c657e3309df2aca55c` and *The Sovereign Mirror* (v57, pp. 16, 20–21, 25, 116–117, 121, 131–132, and *The Map* pp. 170–175) were consulted to specify this protocol.

### 0.3 Locked Pre-Data Decisions (`A1`–`A4`) and SHA Recording
Before any OpenStax *University Physics* data was fetched or any held-out run began, Nicholas approved this `proof/heldout/PREREGISTRATION.md` protocol and confirmed all four pre-data decisions (`A1`–`A4`):
1. **`A1` — 17-Row Provenance (`proof/PROOF.md` Section 1.3, locked in Commit 1 `eb7cb044725beb2572cfe9c657e3309df2aca55c`):** `"construction"` (`4` rows): Row `7` (`7 E = mc^2`), Row `14` (`Newton's third law`), Row `15` (`m = density x volume`), and Row `16` (`F = ma`), all `Keep` (`4/4` `Keep`). `"applied later"` (`13` rows): Rows `1–6`, `8–13`, and `17` (`10` `Keep`, `3` `Invert` `[2, 8, 9]`).
2. **`A2` — Part 2 Track `(b)` Rule-Applier Packet (Section 1.6):** Approved the verbatim *SM v57* rule passages (pp. 20, 116) and half-page of verbatim term definitions (pp. 16, 21, 25, 117, 131–132, 174–175), locking **Option 2 (Redacted Inline Examples)**: inside the Ch. 2 p. 20 blockquote in `proof/heldout/applier_packet.md`, only `"the way mass is density times volume and force is mass times acceleration"` is replaced with `[...]`, leaving every other character verbatim.
3. **`A3` — Part 2 Track `(c)` Codebook `q4` Gravity Scope (Section 1.7):** Locked **Option B (All-Gravitation Scope)** — `q4 = Yes` for ALL gravitational laws, including Newtonian universal gravitation ($F = G m_1 m_2 / r^2$), gravitational field/potential/wells, relativistic spacetime curvature, and gravitational lensing (matching *SM v57* pp. 117 and 121). Frozen Lean predicates at `df6d8fbab8aec198ac4d6af58455a206f8bc6ebd` (`R_read_v57_ch2`, `R_read_v57_ch16`, etc.) remain unchanged.
4. **`A4` — Part 3 Target Word List (Section 2.2):** Confirmed the `10` physical-quantity words in the `Physical` column of *The Map* (*SM v57* pp. 170–173): `acceleration`, `density`, `energy`, `force`, `mass`, `space`, `speed`, `time`, `velocity`, `volume`. All `7` flagged borderline terms (`light`, `radiation`, `electric`/`electro`, `magnetic`, `kinetic`, `rest`, `momentum`) are excluded from Part 3 targets.

Every downstream Part 2, Part 3, and Part 4 data file, card/ruling/applier/labeling packet, evaluation script output JSON, and `proof/verification_certificate.json` MUST record the 40-character SHA of Commit 2 in the field `preregistration_commit_sha`.

### 0.4 Pre-Results Amendment 1 — Author Withdrawal From Track `(a)`
After Commit 5 (`c329a65fb8e833067686790096a105dd7f0fbf81`, which emitted the Track `(a)` worksheet) and with zero Track `(a)`, Track `(b)`, or Track `(c)` rulings or labels in existence, Nicholas declined to rule in Track `(a)` because he built *The Sovereign Mirror* table from $E = mc^2$ and Newton's mechanics only and is not qualified to rule on unfamiliar university physics equations.

Under this pre-results amendment (Commit 6, locked prior to any Track `(b)` or Track `(c)` execution):
1. **Track `(a)` retired pre-results:** `proof/heldout/build_ruling_packet.py`, `proof/heldout/ruling_packet.csv`, and `proof/heldout/packets/track_a_ruling_worksheet.md` are removed from the working tree via `git rm` in Commit 6 (Commit 5 remains in git history for audit), and no `proof/heldout/rulings.csv` is created.
2. **Fixed `48`-law held-out sample:** With no Track `(a)` rulings to trigger minority-class adaptive extension, the held-out evaluation sample size is fixed at the `48` `primary_48` laws already drawn at Commit 3 (`C001`–`C065` minus the `17` `calibration_17` rows; `proof/heldout/reserve_pool.csv` stays unused on disk, and no adaptive stopping applies to Track `(b)` or Track `(c)`).
3. **Two remaining evaluation tracks and single conjunctive primary test:** Part 2 proceeds exclusively with independent Track `(b)` (three fresh model-family rule-applier sessions on `proof/heldout/applier_packet.md`) and independent Track `(c)` (three separate fresh model-family physics-codebook sessions on `proof/heldout/labeling_packet.md`), evaluated under the single conjunctive primary test specified in Section 1.9.
4. **Amendment SHA provenance:** `preregistration_commit_sha = 463ad9f93c8a276b1e0d9ee497198dfa2169d079` remains untouched across all Commit 3–4 files (`fetch_and_sample_laws.py`, `openstax_*`, `exclusion_log.csv`, `eligible_laws_pool.csv`, `reserve_pool.csv`, `sample_manifest.csv`, `build_law_cards.py`, `law_cards.csv`, `law_cards.md`, and `packets/stage0_*`). Commit 6's 40-character commit SHA is recorded alongside `preregistration_commit_sha` as `amendment_1_commit_sha` in Part 2 evaluation packets (`proof/heldout/applier_packet.md`, `proof/heldout/labeling_packet.md`), Part 2 evaluation scripts and output JSONs, and `proof/PROOF.md`.

---

## 1. Part 2 Protocol — Held-Out Laws: Does the Rule Decide by Itself

### 1.1 Claim Tested, Scope Boundary, and Locked 17-Row Provenance (`A1`)
- **Claim tested:** The one rule as printed in *The Sovereign Mirror* v57 (pp. 20 and 116) is enough to rule on a law it was not built from, in hands other than the author's.
- **Not tested:** Whether a ruling is true.

Both sentences above MUST appear verbatim at the top of the Part 2 section in `proof/PROOF.md` before any results or interpretation.

**Locked 17-Row Provenance (`A1`, `proof/PROOF.md` Section 1.3):** Nicholas built the table in *The Sovereign Mirror* from $E = mc^2$ and Newton's mechanics, and confirmed provenance for all 17 benchmark rows before any held-out data was fetched:
- **`"construction"` (`4` rows):** Row `7` (`7 E = mc^2`), Row `14` (`Newton's third law`), Row `15` (`m = density x volume`), and Row `16` (`F = ma`) (`4/4` `Keep`; `always-Keep`, `R_read_v57_ch2`, and `R_read_v57_ch16` match `4/4`; `always-Invert`: `0/4`).
- **`"applied later"` (`13` rows):** Rows `1–6`, `8–13`, and `17` (`10` `Keep`, `3` `Invert` `[2, 8, 9]`; `always-Keep` matches `10/13`, `always-Invert` matches `3/13`, `R_read_v57_ch2` matches `10/13` missing Rows `11, 12, 17`, and `R_read_v57_ch16` matches `12/13` missing Row `17`).

### 1.2 Frozen Rule Definitions and Exact Majority-Vote Boolean Formula
Part 2 evaluates the frozen reading rules defined in `proof/lean/TSR/MirrorFunctor.lean` at commit `df6d8fbab8aec198ac4d6af58455a206f8bc6ebd` and `eb7cb044725beb2572cfe9c657e3309df2aca55c`:
- `isIdentityOrEquiv` (`LawAST -> Bool`)
- `isSharedEnergyWork` (`LawAST -> Bool`)
- `dependsOnResistanceOrSeparation` (`r.hasMass || (r.lawAST == .SpatialSeparationDependence)`)
- `R_read_v57_ch2`
- `R_read_v57_ch16`
- `R_read_naive_mass`
- `R_read_always_keep`
- `R_read_always_invert`

In Track `(c)` (Section 1.5), each law card is scored across 3 fresh sessions of 3 distinct model families on 4 binary (`Yes = True`, `No = False`) physics codebook questions defined in Section 1.7:
- $q_1$: `q1_identity_or_definition` (maps to `isIdentityOrEquiv`)
- $q_2$: `q2_mass_or_inertia_term` (maps to `hasMass`)
- $q_3$: `q3_spatial_separation` (maps to `lawAST == .SpatialSeparationDependence`)
- $q_4$: `q4_shared_energy_curvature` (maps to `isSharedEnergyWork`)

For each question $k \in \{1, 2, 3, 4\}$, the strict 2/3 majority bit $q_k \in \{\text{True}, \text{False}\}$ equals `True` iff at least 2 of the 3 sessions answer `Yes` (`sum >= 2`). Because 3 binary votes admit no tie, $(q_1, q_2, q_3, q_4)$ is uniquely determined for every card.

The deterministic boolean mapping from $(q_1, q_2, q_3, q_4)$ to predicted readings $\in \{\text{Keep}, \text{Invert}\}$ mirrors `proof/lean/TSR/MirrorFunctor.lean` identically:

```python
depends_on_resistance_or_separation = q2 or q3

R_read_v57_ch2(q1, q2, q3, q4) = (
    "Keep" if (q1 or (not q2 and not q3)) else "Invert"
)
R_read_v57_ch16(q1, q2, q3, q4) = (
    "Keep" if (q1 or q4 or (not q2 and not q3)) else "Invert"
)
R_read_naive_mass(q1, q2, q3, q4) = "Invert" if q2 else "Keep"
R_read_always_keep(q1, q2, q3, q4) = "Keep"
R_read_always_invert(q1, q2, q3, q4) = "Invert"
```

Equivalently, `R_read_v57_ch16` returns `"Invert"` iff `(not q1) and (not q4) and (q2 or q3)`, and `R_read_v57_ch2` returns `"Invert"` iff `(not q1) and (q2 or q3)`.

### 1.3 Corpus Source, Attribution, Exact 22 Chapters, Exclusions (`E1`–`E4`), and Stratified Sample (`seed = 20261113`)

#### Corpus Source, License Attribution, and Fetch Mechanism
- **Text Source & License:** OpenStax *University Physics*, Volumes 1–3 (Samuel J. Ling, Jeff Sanny, William Moebs; Rice University / OpenStax), licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). Required attribution string carried into all derived corpus manifests and outputs:
  `"Access for free at https://openstax.org — Licensed under CC BY 4.0."`
- **Exact 22 Included Chapters:**
  - **Volume 1 (Chapters 1–17):**
    1. Ch. 1 — Units and Measurement
    2. Ch. 2 — Vectors
    3. Ch. 3 — Motion Along a Straight Line
    4. Ch. 4 — Motion in Two and Three Dimensions
    5. Ch. 5 — Newton's Laws of Motion
    6. Ch. 6 — Applications of Newton's Laws
    7. Ch. 7 — Work and Kinetic Energy
    8. Ch. 8 — Potential Energy and Conservation of Energy
    9. Ch. 9 — Linear Momentum and Collisions
    10. Ch. 10 — Fixed-Axis Rotation
    11. Ch. 11 — Angular Momentum
    12. Ch. 12 — Static Equilibrium and Elasticity
    13. Ch. 13 — Gravitation
    14. Ch. 14 — Fluid Mechanics
    15. Ch. 15 — Oscillations
    16. Ch. 16 — Waves
    17. Ch. 17 — Sound
  - **Volume 2, Unit 1 Thermodynamics (Chapters 1–4):**
    18. Vol. 2 Ch. 1 — Temperature and Heat
    19. Vol. 2 Ch. 2 — The Kinetic Theory of Gases
    20. Vol. 2 Ch. 3 — The First Law of Thermodynamics
    21. Vol. 2 Ch. 4 — The Second Law of Thermodynamics
  - **Volume 3 (Chapter 5):**
    22. Vol. 3 Ch. 5 — Relativity
- **Fetch Mechanism:** Retrieve verbatim `"Key Equations"` summary tables directly from `openstax.org` chapter pages or the official `openstax/osbooks-university-physics-bundle` repository, preserving `volume`, `chapter`, `chapter_title`, `row_idx` (0-based or 1-based table order within chapter), `eq_number`, `description`, `equation_latex`, `source_url`, and `retrieved_utc`.
- **Mandatory Stop Rule:** If the `"Key Equations"` sections across these 22 chapters cannot be retrieved from `openstax.org` or `openstax/osbooks-university-physics-bundle`, execution MUST halt immediately and report the retrieval failure. Equations MUST NOT be reconstructed from model memory.

#### Pre-Sampling Deterministic Exclusion Rules (`proof/heldout/exclusion_log.csv`)
Before sampling, every extracted row in canonical `(volume, chapter, row_idx)` order passes through 4 deterministic exclusion criteria. Every excluded row is recorded in `proof/heldout/exclusion_log.csv` with columns:
`volume, chapter, row_idx, eq_number, description, equation_latex, exclusion_code, matched_benchmark_id, rationale, preregistration_commit_sha`.

1. **`E1_PURE_MATH`:** Pure mathematical, algebraic, geometric, trigonometric, vector-calculus, or coordinate-transformation identities containing no physical quantity (for example, dot/cross product formulas, unit-vector calculus, Taylor approximations, or triangle/trig identities). Kinematics equations involving physical displacement, velocity, acceleration, time, frequency, or wavelength are **retained**.
2. **`E2_UNIT_OR_CONSTANT`:** Pure unit-conversion ratios or bare numerical values of physical constants without a functional physical relationship (for example, $1\text{ atm} = 1.013 \times 10^5\text{ Pa}$, $G = 6.67 \times 10^{-11}\text{ N}\cdot\text{m}^2/\text{kg}^2$ alone). Functional physical definitions (such as $\rho = m/V$, $v = \lambda f$) are retained unless matched by `E3` or `E4`.
3. **`E3_RESTATES_BENCHMARK_17`:** Any OpenStax equation or statement that directly restates one of the 17 existing laws in `benchmarkRows17` (`proof/lean/TSR/MirrorFunctor.lean` L579–607). Multi-variable thermodynamic gas equations not identical to fixed-temperature $P$-$V$ Boyle inverse scaling (specifically `pV = nRT`, ideal-gas kinetic/equipartition laws, adiabatic processes, and Carnot efficiency) are **retained**. The 17 existing rows excluded against `E3` are fixed as:

| ID | Existing `benchmarkRows17` label | Restated physics content excluded under `E3_RESTATES_BENCHMARK_17` |
|---:|---|---|
| 1 | `"1 laws same for every observer"` | First postulate of special relativity / invariance of physics across inertial frames |
| 2 | `"2 no shared now (distance)"` | Relativity of simultaneity for spatially separated events ($\Delta t = \gamma v \Delta x / c^2$ for $\Delta t'=0$) |
| 3 | `"3 no fixed frame"` | Absence of an absolute or preferred inertial rest frame |
| 4 | `"4 special vs general"` | Distinction / equivalence principle scope between inertial and accelerating/gravitating frames |
| 5 | `"5 time dilation"` | Proper time dilation ($\Delta t = \gamma \Delta \tau$ / $\gamma = 1/\sqrt{1-v^2/c^2}$) |
| 6 | `"6 length contraction"` | Proper length contraction ($L = L_0 / \gamma$) |
| 7 | `"7 E = mc^2"` | Rest mass-energy equivalence ($E_0 = mc^2$ / $E = mc^2$ at rest) |
| 8 | `"8 cost of more speed"` | Relativistic kinetic / total energy increase with speed ($K = (\gamma - 1)mc^2$, $E = \gamma mc^2$) |
| 9 | `"9 mass can't reach c"` | Invariance of $c$ as upper speed limit ($v < c$ / $\gamma \to \infty$ for $m > 0$) |
| 10 | `"10 space-time one continuum"` | Invariant spacetime interval unifying space and time ($s^2 = c^2\Delta t^2 - \Delta x^2 - \Delta y^2 - \Delta z^2$) |
| 11 | `"11 mass-energy warps space-time"` | Mass-energy curving spacetime geometry |
| 12 | `"12 wells and lensing"` | Gravitational wells, gravitational redshift, and gravitational deflection/lensing of light |
| 13 | `"conservation"` | Generic total energy conservation statement ($E_i = E_f$ / $\Delta E_{\text{sys}} = 0$ closed) |
| 14 | `"Newton's third law"` | Action-reaction force pair ($\vec{F}_{AB} = -\vec{F}_{BA}$) |
| 15 | `"m = density x volume"` | Mass density definition ($\rho = m/V$ or $m = \rho V$) |
| 16 | `"F = ma"` | Newton's second law ($\vec{F}_{\text{net}} = m\vec{a}$) |
| 17 | `"Boyle: squeeze volume, pressure climbs"` | Isothermal fixed-gas inverse pressure-volume scaling ($P_1 V_1 = P_2 V_2$) |

4. **`E4_EXACT_DUPLICATE`:** An exact repeat (same normalized formula/law statement) of an earlier retained entry within the 22-chapter corpus; the earliest occurrence in canonical `(volume, chapter, row_idx)` order is retained and later duplicates are logged under `E4_EXACT_DUPLICATE`.

#### Deterministic Stratified Sampling and Fixed Sample Size (Amendment 1)
All surviving eligible laws are sorted canonically by `(volume, chapter, row_idx)` and assigned canonical `law_id` values `H001, H002, ...`. Sampling uses `rng = random.Random(20261113)` exclusively:
1. Partition eligible rows into the 22 chapter buckets ordered canonically by `(volume, chapter)`. For each bucket in canonical chapter order, run `rng.shuffle(bucket)`.
2. **Capacity-aware round-robin allocation totaling `N_primary = 48`:**
   Maintain `avail` as the canonically ordered list of chapter keys that still hold unallocated rows. While `allocated < 48` and `avail` is non-empty:
   - If `48 - allocated >= len(avail)`, pop 1 row from each chapter in `avail` in canonical order (`allocated += len(avail)`), removing any chapter that becomes empty after its pop.
   - Otherwise (`remainder = 48 - allocated < len(avail)`), draw `chosen = rng.sample(avail, remainder)` (preserving canonical ordering of `avail` as input to `rng.sample`), pop 1 row from each chosen chapter, and finish primary allocation (`allocated == 48`).
3. **Sequential Reserve Permutation:** Gather all unallocated eligible rows across all chapters in canonical `(volume, chapter, row_idx)` order into `reserve_pool`, execute `rng.shuffle(reserve_pool)`, and assign `reserve_rank = 1, 2, ..., len(reserve_pool)`.
4. **Fixed Held-Out Sample Size (`48` `primary_48` Laws; Pre-Results Amendment 1):**
   With Track `(a)` withdrawn pre-results (Section 0.4), the held-out evaluation sample size is fixed at the `48` `primary_48` OpenStax laws already drawn at Commit 3 (`C001`–`C065` minus the `17` `calibration_17` rows). `proof/heldout/reserve_pool.csv` stays unused on disk, and no minority-class adaptive extension or adaptive stopping is applied to Track `(b)` or Track `(c)`.

### 1.4 Stage 0 — Plain-Language Law Cards (`proof/heldout/law_cards.csv` & `proof/heldout/law_cards.md`)
- **Card Writer & Isolation:** One fresh external model session (run by Nicholas; repository agents MUST NOT write law cards) with zero access to this repository, *The Sovereign Mirror*, *What the Words Knew*, or TSR writes a plain-language card for every drawn held-out law and for the 17 existing laws from `benchmarkRows17`.
- **Pooling, Shuffling, and Withheld Manifest:** The `48` primary held-out laws and the `17` existing laws are pooled (`65` laws) and shuffled with `random.Random(20261113)` under sequential neutral IDs `C001, C002, ..., C065`. The mapping between `card_id` (`C001..`), `source_set` (`"heldout"` vs. `"benchmark_17"`), `law_id`, `benchmark_id`, `volume`, `chapter`, `row_idx`, `eq_number`, `draw_phase`, and `reserve_rank` is stored solely in `proof/heldout/sample_manifest.csv` and stays withheld from the card writer, Track `(b)` sessions, and Track `(c)` sessions (and was withheld from Track `(a)` prior to its pre-results withdrawal in Amendment 1).
- **Structured JSON Output & Deterministic Serialization (`proof/heldout/build_law_cards.py`):** The single fresh external card-writer session outputs one structured JSON array of objects, each containing exact keys `card_id`, `what_it_says`, `quantities_related`, and `conditions_to_hold`, for `C001..C065` (fixed at `65` cards total under Amendment 1, with no `C066..` `reserve_extension` cards drawn). A deterministic repository serialization script (`proof/heldout/build_law_cards.py`) validates the JSON schema, exact sequential `card_id` coverage (`C001..C065`), non-empty string values, and zero TSR vocabulary, and writes `proof/heldout/law_cards.csv` (appending `preregistration_commit_sha`) and `proof/heldout/law_cards.md` verbatim without editing card wording.
- **Required Card Fields:** Each card in `proof/heldout/law_cards.csv` and `proof/heldout/law_cards.md` states:
  1. `what_it_says`: Plain-language statement of the physical law plus its standard mathematical formula where present.
  2. `quantities_related`: The physical quantities related by the law.
  3. `conditions_to_hold`: The physical conditions required for the law to hold (for example: mass or rotational inertia, spatial distance or separation, physical contact/surfaces or walls, gravitational curvature/field, or definition/equivalence/conservation/frame invariance).
- **Zero TSR Vocabulary Permitted:** Law cards MUST contain zero TSR vocabulary (`Movement` as a TSR term, `Current of Consciousness`, `Vibrance`, `Appreciation`, `Point of Reflection`, `Point of Attraction`, `Vortex`, `Convergence` as TSR terms, `Nonphysical Movement`, `Expansion Dilation`, `Eternal-Energetic-Entity`, `Conscious-physical`, `conscious energy`, `Keep`, `Invert`, `sovereign`, `nonphysical`, `receptivity`, `receptive`, `TSR`, `The Sovereign Mirror`, etc.). The deterministic serialization/filter script `proof/heldout/build_law_cards.py` MUST verify zero TSR vocabulary matches in the input JSON, `proof/heldout/law_cards.csv`, and `proof/heldout/law_cards.md` before commit (using case-insensitive matching for TSR-exclusive terms such as `vibrance`, `appreciation`, `point of reflection`, `point of attraction`, `sovereign`, `nonphysical`, `receptivity`, `receptive`, `keep`, `invert`, `tsr`, and capitalized/phrase matching for polysemous physics words such as `Movement`, `Current`, `Vortex`, `Convergence` so standard physics terms such as electric current remain unblocked).
- **Stage 0 Commit Gate:** `proof/heldout/law_cards.csv` and `proof/heldout/law_cards.md` (`C001..C065`) were committed to git in Commit 4 (`b19f5da7bb3f1516d568434d49febbf043416ae9`) BEFORE Track `(b)` or Track `(c)` begins. Under Amendment 1 (Section 0.4), no `C066..` `reserve_extension` laws are drawn.
- **Schemas:**
  - `proof/heldout/law_cards.csv`: `card_id, what_it_says, quantities_related, conditions_to_hold, preregistration_commit_sha`
  - `proof/heldout/sample_manifest.csv` (withheld until both Track `(b)` and Track `(c)` commit): `card_id, source_set, law_id, benchmark_id, volume, chapter, row_idx, eq_number, draw_phase, reserve_rank, preregistration_commit_sha`

### 1.5 Two Independent Evaluation Tracks — Each Committed Before Joining
Both remaining evaluation tracks (`(b)` and `(c)`) operate on the committed plain-language law cards (`C001..C065`) without sight of each other's outputs or `proof/heldout/sample_manifest.csv`. Repository agents MUST NOT produce or edit any ruling in Track `(b)` or any label in Track `(c)`. Both output files (`proof/heldout/appliers.csv` and `proof/heldout/labels.csv`), together with the six raw session JSON outputs, MUST be committed independently to git BEFORE any script reads `proof/heldout/sample_manifest.csv` to separate `"heldout"` (`48`) from `"benchmark_17"` (`17`) or join Track `(b)` with Track `(c)`:

1. **Track `(a)` — Author Rulings (`WITHDRAWN PRE-RESULTS` in Amendment 1):**
   - Withdrawn prior to any evaluation execution under Section 0.4 because Nicholas built *The Sovereign Mirror* table from $E = mc^2$ and Newton's mechanics only and declined to rule on unfamiliar university physics equations.
   - `proof/heldout/build_ruling_packet.py`, `proof/heldout/ruling_packet.csv`, and `proof/heldout/packets/track_a_ruling_worksheet.md` are retired via `git rm` in Commit 6 (Commit 5 `c329a65fb8e833067686790096a105dd7f0fbf81` is retained in git history for audit), and no `proof/heldout/rulings.csv` is created.

2. **Track `(b)` — Independent Rule Appliers (`proof/heldout/appliers.csv`):**
   - Nicholas runs **3 fresh sessions** (`b1`, `b2`, `b3`) of **three distinct model families** on `proof/heldout/applier_packet.md`, with zero access to this repository, *The Sovereign Mirror*, *What the Words Knew*, or any TSR material outside `proof/heldout/applier_packet.md`, and zero sight of Track `(c)` or each other's outputs.
   - Each Track `(b)` session receives ONLY `proof/heldout/applier_packet.md`, containing:
     1. The locked Track `(b)` text block in Section 1.6 (the two exact *SM v57* rule passages from pp. 20 and 116 with the Ch. 2 p. 20 inline example clause replaced by `[...]`, plus the half-page of exact *SM v57* term definitions — zero worked rulings and nothing else from TSR); and
     2. All `65` shuffled plain-language law cards (`C001..C065`, pooling the `48` `primary_48` held-out laws and the `17` existing laws from `benchmarkRows17`, presented in `random.Random(20261113)` order without origin labels).
   - Each session outputs JSON `[{"card_id": ..., "ruling": ..., "rationale": ...}]` in order `C001..C065`, assigning `ruling` $\in \{\text{"Keep"}, \text{"Invert"}, \text{"the rule doesn't say"}\}$ and a one-line `rationale` citing which phrase of the quoted rule applies. Raw session JSON outputs are committed alongside `proof/heldout/appliers.csv`.
   - **3-Category Majority (`b_maj_ruling`):** Across `(b1_ruling, b2_ruling, b3_ruling)`, if at least 2 of 3 sessions agree on one category in `{"Keep", "Invert", "the rule doesn't say"}`, `b_maj_ruling` equals that category; if all 3 sessions select distinct categories (a 1-1-1 three-way split), record `b_maj_ruling = "no_majority"` (counted as non-definite / non-match against `"Keep"` or `"Invert"` in unconditional metrics).
   - **Schema (`proof/heldout/appliers.csv`):**
     `card_id, b1_model_family, b2_model_family, b3_model_family, b1_ruling, b1_rationale, b2_ruling, b2_rationale, b3_ruling, b3_rationale, b_maj_ruling, preregistration_commit_sha, amendment_1_commit_sha`

3. **Track `(c)` — Physics Codebook & Mechanical Rule Evaluation (`proof/heldout/labels.csv`):**
   - Nicholas runs **3 separate fresh sessions** (`c1`, `c2`, `c3`) of **three distinct model families** (separate sessions from Track `(b)`) on `proof/heldout/labeling_packet.md`, with zero access to this repository, *The Sovereign Mirror*, *What the Words Knew*, Track `(b)`, or the Section 1.6 rule quotes.
   - Each Track `(c)` session receives ONLY `proof/heldout/labeling_packet.md`, containing:
     1. The verbatim 4-question yes/no pure-physics codebook and pure-physics `q4` scope paragraph (Section 1.7, with zero TSR vocabulary or `"Keep"`/`"Invert"` terms); and
     2. All `65` shuffled plain-language law cards (`C001..C065`, pooling the `48` `primary_48` held-out laws and the `17` existing laws from `benchmarkRows17`, presented in `random.Random(20261113)` order without origin labels).
   - Each session outputs JSON `[{"card_id": ..., "q1": ..., "q2": ..., "q3": ..., "q4": ...}]` in order `C001..C065`, answering `"Yes"` or `"No"` for each question on every card. Raw session JSON outputs are committed alongside `proof/heldout/labels.csv`.
   - Strict 2/3 majority vote per question (`q1_maj..q4_maj`) feeds the frozen formulas in Section 1.2 to emit `pred_ch2` (`R_read_v57_ch2`), `pred_ch16` (`R_read_v57_ch16`), and `pred_naive_mass` (`R_read_naive_mass`).
   - **Schema (`proof/heldout/labels.csv`):**
     `card_id, c1_model_family, c2_model_family, c3_model_family, c1_q1, c1_q2, c1_q3, c1_q4, c2_q1, c2_q2, c2_q3, c2_q4, c3_q1, c3_q2, c3_q3, c3_q4, q1_maj, q2_maj, q3_maj, q4_maj, pred_ch2, pred_ch16, pred_naive_mass, preregistration_commit_sha, amendment_1_commit_sha`

### 1.6 Locked Track `(b)` Rule-Applier Text Block (`proof/heldout/applier_packet.md`)
In Track `(b)`, `proof/heldout/applier_packet.md` provides only the prompt instructions (asking for `ruling ∈ {"Keep", "Invert", "the rule doesn't say"}` and a one-line `rationale` for each card `C001..`), the shuffled plain-language law cards, and the locked *The Sovereign Mirror* (v57) text block below (zero worked rulings from Ch. 16 or elsewhere):

#### 1.6.1 Rule Passages (*SM v57*, Ch. 2 p. 20 & Ch. 16 p. 116)
- **Chapter 2 (*The One Rule*), p. 20 (with Option 2 inline example redaction locked under `A2`):**
> The main difference between the physical and the nonphysical is resistance. That’s the rule, or the start of it. Physics already measures resistance to a change in motion. It calls it mass. So you take the world Einstein described and reflect it: keep each relationship, and flip the condition. Resistant becomes receptive, limited becomes limitless, radiating becomes collecting. What comes out the other side is the nonphysical version. Every term reflects; that part always happens. What you have to know is whether the relationship keeps its shape or turns around. If it depends on resistance, or on the distance resistance makes, so that more mass or more separation means more of something, flipping resistant to receptive turns it around: more Movement means less of that thing, or it gets easier instead of harder. If it’s an identity or a definition, two names for one thing, [...], there’s nothing to turn around, even with mass in it; the terms reflect and the relationship keeps its shape. That’s the one rule.

- **Locked Redaction (`A2`, Option 2):** Inside the verbatim *SM v57* Ch. 2 p. 20 passage above, only the inline clause `"the way mass is density times volume and force is mass times acceleration"` is replaced with `[...]` in `proof/heldout/applier_packet.md` so calibration Rows 15 and 16 are not exemplified; every other character of the p. 20 passage matches the printed book verbatim.

- **Chapter 16 (*Twelve Reflections*), p. 116** *(adjacent sentences on p. 116 discuss specific numbered benchmark rows `5`, `6`, `7`, and `8` and are excluded so zero worked rulings appear in the packet)*:
> The rule from Chapter 2 does, whoever is running it, because it asks one question of every row: does this relationship depend on resistance, or on the distance resistance makes, or is it an identity, a definition, or the work of the one energy both sides share?

#### 1.6.2 Half-Page of Term Definitions (*SM v57*, pp. 16, 21, 25, 117, 131–132, 174–175; Zero Worked Rulings)
- **Two Environments (*SM v57*, Ch. 1, p. 16):**
> There are two environments, the physical and the nonphysical, and they’re mirror images of each other. The physical is limited, resistant, and it radiates. The nonphysical is limitless, receptive, and it collects. Those three pairs aren’t three separate rules—they’re one condition seen three ways. Resistance creates a boundary, which makes a thing limited, and bounded things can only reach each other by radiating across the space between them. Take resistance away and there’s no boundary, so the nonphysical is limitless, and with nothing held apart, it collects instead of radiating. Everything else in TSR comes from what happens where they meet.

- **Resistance and "Physical" (*SM v57*, Ch. 2, p. 25):**
> Resistance is resistance to change.
>
> Physical, in this book, is the resistant condition wherever it occurs, not matter as opposed to mind.

- **Space, Time, and Distance (*SM v57*, Ch. 2, p. 21):**
> Think about what space and time actually do. On the physical side, where resistance gives things edges, space is what keeps two things from sitting in the same place, and time is what keeps everything from happening at once. Take resistance away and there’s no distance. Two particulars in the same whole don’t sit in different places; they differ by how they vibrate, the way two notes share the same air in a room. So space reflects as Vibration. And where nothing decays or comes apart, before and after are separated only by the whole becoming more than it was.

- **Nonphysical Movement (*SM v57*, *The Map*, p. 175):**
> Receptivity to change in motion; a self-contained part of the whole, like a movement in a symphony. The reflection of mass.

- **The One Energy Both Sides Share (*SM v57*, Ch. 16 p. 117; Ch. 17 pp. 131–132; *The Map* p. 174):**
  - *SM v57*, Ch. 16, p. 117 *(preceding and following lines discussing gravity and numbered rows are excluded so zero worked rulings appear)*:
> TSR has three: the two sides and the continuum where they meet, with one energy in it.
  - *SM v57*, Ch. 17, p. 131:
> There aren’t two energies, one spiritual and one physical, taking turns. There’s one energy transmuting. On the nonphysical side it’s conscious energy: the Collective and Vibrational realities are made of it.
  - *SM v57*, Ch. 17, p. 132:
> Where your Vibrational Reality meets your Subjective Reality, the two blend. I call that conscious-physical energy.
  - *SM v57*, *The Map*, p. 174 (*Conscious-physical energy* entry):
> The blend of conscious and physical energy at the hinge, the E.

### 1.7 Track `(c)` 4-Question Physics Codebook & Locked `q4` Gravity Scope (`A3`)

#### Exact 4 Yes/No Codebook Questions (Included Verbatim in `proof/heldout/labeling_packet.md`)
- **`q1_identity_or_definition` (`Yes` / `No`):** *Does this equation/statement primarily express a conservation law, equivalence or correspondence identity, defining physical relation, symmetry/frame-invariance principle, or reciprocal action-reaction pairing (as opposed to a dynamical resistance, inertial barrier, or spatial-separation effect)?*
- **`q2_mass_or_inertia_term` (`Yes` / `No`):** *Does the equation/statement explicitly include mass, gravitational mass, inertial mass, moment of inertia, linear/angular mass resistance, or a fixed quantity/mass of gas or matter ($m$, $M$, $I$, $n$)?*
- **`q3_spatial_separation` (`Yes` / `No`):** *Does the physical law or effect explicitly depend on spatial distance, displacement, separation between bodies or events, or path/length difference ($r$, $d$, $\Delta x$, $\Delta s$, $L$)?*
- **`q4_shared_energy_curvature` (`Yes` / `No`):** *Does the equation/statement govern shared gravitational/spacetime curvature, gravitational wells or lensing, or conservative potential-well / shared field energy coupling across space — including all Newtonian and relativistic gravitational laws (rather than non-gravitational inertial resistance to acceleration or point-to-point transport/dissipation)?*

#### Locked `q4` Scope Rule — Option B (All-Gravitation Scope, Frozen Verbatim into `proof/heldout/labeling_packet.md`)

**Pure-Physics `q4` Scope Text (placed verbatim in `proof/heldout/labeling_packet.md`):**

> Answer `q4 = Yes` for **all gravitational laws**, including Newtonian universal gravitation ($F = Gm_1 m_2 / r^2$) and closely related orbital/gravitational force laws, gravitational field/potential/wells ($U_g = -GMm/r$, escape/orbital balance), relativistic spacetime curvature / mass-energy warping, and gravitational lensing. Non-gravitational laws involving inertial resistance to acceleration or point-to-point transport/dissipation remain `q4 = No`.

**TSR / Lean Provenance Note (kept out of `proof/heldout/labeling_packet.md` so Track `(c)` sees zero TSR vocabulary or `"Keep"`/`"Invert"` words):**
Under confirmed pre-data decision `A3` (**Option B — All-Gravitation Scope**), the pure-physics `q4` scope rule above matches *SM v57* pp. 117 and 121 (where gravity reflects as Attraction — what receptive and resistant make together through the one shared energy). Under `R_read_v57_ch16`, `q4 = Yes` predicts `"Keep"` for all such gravitational laws, while non-gravitational laws involving inertial resistance to acceleration or point-to-point transport/dissipation remain `q4 = No`. The frozen Lean predicates and benchmark definitions at commit `df6d8fbab8aec198ac4d6af58455a206f8bc6ebd` (`isIdentityOrEquiv`, `isSharedEnergyWork`, `dependsOnResistanceOrSeparation`, `R_read_v57_ch2`, `R_read_v57_ch16`, `R_read_naive_mass`, `benchmarkRows17`, and `v57_rule_wordings_benchmark`) remain unchanged.

### 1.8 Calibration on Existing 17 (`benchmarkRows17`, Never Pooled with Held-Out)
Both Track `(b)` and Track `(c)` include the 17 existing laws from `benchmarkRows17` embedded as plain-language cards in the shuffled `C001..C065` packets (`proof/heldout/appliers.csv` and `proof/heldout/labels.csv`). Calibration on the 17 is analyzed separately and NEVER pooled with held-out laws:
1. **Track `(b)` on `benchmarkRows17`:**
   - Exact rational **3-category Fleiss' $\kappa$** (`{"Keep", "Invert", "the rule doesn't say"}`) among `(b1, b2, b3)`.
   - Agreement rate of each individual applier (`b1`, `b2`, `b3`) and of the majority (`b_maj_ruling`) against `benchmarkRows17.bookRuling`, reported **overall (`n = 17`)** AND **split by provenance (`"construction"` [4 rows: `7, 14, 15, 16`] vs. `"applied later"` [13 rows: `1–6, 8–13, 17`], as recorded in `proof/PROOF.md` Section 1.3)**.
   - Exact count and row-by-row listing of any `"the rule doesn't say"` rulings (and any `"no_majority"` 3-way split) on the 17 rows.
2. **Track `(c)` on `benchmarkRows17`:**
   - Per-question `%` agreement and exact rational **Fleiss' $\kappa$** among `(c1, c2, c3)` for each codebook question (`q1..q4`).
   - Per-question `%` agreement and exact Cohen's $\kappa$ between the 2/3 majority votes `(q1_maj, q2_maj, q3_maj, q4_maj)` and the existing Lean encodings in `proof/lean/TSR/MirrorFunctor.lean` (`isIdentityOrEquiv`, `hasMass`, `lawAST == .SpatialSeparationDependence`, `isSharedEnergyWork`).
   - Induced `R_read_v57_ch2` (`pred_ch2`) and `R_read_v57_ch16` (`pred_ch16`) agreement rates against `benchmarkRows17.bookRuling` (reported overall and split by `"construction"` vs. `"applied later"`).
3. **Direct Track `(b)` vs. Track `(c)` Agreement on `benchmarkRows17` (`n = 17`):**
   - Direct agreement rate (`matches / 17`), exact rational Cohen's $\kappa$, full confusion matrices, and row-by-row comparison between `b_maj_ruling` (and individual appliers `b1..b3`) and `pred_ch16` (`R_read_v57_ch16`) as well as `pred_ch2` (`R_read_v57_ch2`), reported **overall (`n = 17`)** AND **split by provenance (`"construction"` [4 rows] vs. `"applied later"` [13 rows])**.

### 1.9 Held-Out Evaluation Metrics and Single Confirmatory Primary Test (`48` OpenStax Laws)
All Part 2 held-out metrics below are computed **strictly on the `48` held-out cards** (`source_set == "heldout"` in `proof/heldout/sample_manifest.csv`, NEVER pooled with the `17` calibration rows), using exact rational arithmetic (`fractions.Fraction`) for all agreement statistics, rates, and Fisher's exact tests:

1. **Inter-Session Agreement (`Fleiss' kappa`):**
   - Exact rational **3-category Fleiss' $\kappa$ among `(b1, b2, b3)`** across all `48` held-out laws (`{"Keep", "Invert", "the rule doesn't say"}`).
   - Descriptive **2-category Fleiss' $\kappa$** (`{"Keep", "Invert"}`) restricted to held-out cards where all three Track `(b)` appliers gave definite rulings (`b1, b2, b3 ∈ {"Keep", "Invert"}`).
   - Exact rational **2-category Fleiss' $\kappa$ among `(c1, c2, c3)`** per codebook question (`q1..q4`) across all `48` held-out laws.

2. **`"the rule doesn't say"` & `"no_majority"` Inventory:**
   Exact counts across `b1`, `b2`, `b3`, and `b_maj_ruling` (`"the rule doesn't say"` and `"no_majority"` 3-way splits), definite-majority coverage $N_{\text{def}} / 48$ (where $N_{\text{def}}$ is the count of held-out laws with `b_maj_ruling ∈ {"Keep", "Invert"}`), and complete per-law listing (`card_id, law_id, volume, chapter, eq_number, description`) of every `"the rule doesn't say"` or `"no_majority"` held-out card.

3. **Unconditional Agreement (`matches / 48`) and Full $4 \times 2$ Confusion Matrices:**
   - Compare `b_maj_ruling` (`"Keep"`, `"Invert"`, `"the rule doesn't say"`, `"no_majority"`) against all 5 mechanical predictors (`R_read_v57_ch16` [`pred_ch16`], `R_read_v57_ch2` [`pred_ch2`], `R_read_naive_mass` [`pred_naive_mass`], `R_read_always_keep`, `R_read_always_invert`), reporting exact `matches / 48` and the full $4 \times 2$ confusion matrix for each predictor (where `"the rule doesn't say"` and `"no_majority"` count as non-matches).
   - Also report unconditional `matches / 48` and full $3 \times 2$ confusion matrices for each individual Track `(b)` applier (`b1`, `b2`, `b3`) against `R_read_v57_ch16` (`pred_ch16`) and `R_read_v57_ch2` (`pred_ch2`).

4. **Conditional Metrics on Definite `b_maj_ruling` (`"Keep"` / `"Invert"`, $N_{\text{def}} = n_1 + n_2$):**
   Restricted to held-out laws with definite `b_maj_ruling ∈ {"Keep", "Invert"}`, treating `"Invert"` as the positive class $i = 1$ ($n_1 = n_{\text{Invert}}$) and `"Keep"` as the negative class $i = 2$ ($n_2 = n_{\text{Keep}}$):
   - $\text{TPR} = k_1 / n_1$ (matches on positive-class laws)
   - $\text{TNR} = k_2 / n_2$ (matches on negative-class laws)
   - Conditional accuracy $= (k_1 + k_2) / (n_1 + n_2)$
   - Balanced accuracy $\text{BA} = (\text{TPR} + \text{TNR}) / 2$
   - Closed-form **95% Wilson-MOVER (Newcombe Method 10 square-and-add) confidence interval $[L_{\text{BA}}, U_{\text{BA}}]$** using $z = 1.959963984540054$ for $\hat{p}_1 = k_1 / n_1 = \text{TPR}$ and $\hat{p}_2 = k_2 / n_2 = \text{TNR}$:

$$l_i, u_i = \frac{2 k_i + z^2 \mp z\sqrt{z^2 + 4 k_i \left(1 - k_i/n_i\right)}}{2\left(n_i + z^2\right)}, \qquad i \in \{1, 2\},$$

$$L_{\text{BA}} = \frac{1}{2}\left(\hat{p}_1 + \hat{p}_2 - \sqrt{(\hat{p}_1 - l_1)^2 + (\hat{p}_2 - l_2)^2}\right),$$

$$U_{\text{BA}} = \frac{1}{2}\left(\hat{p}_1 + \hat{p}_2 + \sqrt{(u_1 - \hat{p}_1)^2 + (u_2 - \hat{p}_2)^2}\right).$$

   Report all five quantities (accuracy, $\text{TPR}$, $\text{TNR}$, $\text{BA}$, and $[L_{\text{BA}}, U_{\text{BA}}]$) on the definite-`b_maj_ruling` subset for: `R_read_v57_ch16`, `R_read_v57_ch2`, `b1..b3` vs `pred_ch16` (treating `pred_ch16 == "Invert"` as positive class $n_1$ and `pred_ch16 == "Keep"` as negative class $n_2$, with any `"the rule doesn't say"` by `b_j` counted in $n_1$ or $n_2$ and not in $k_1$ or $k_2$), `R_read_naive_mass`, `R_read_always_keep`, and `R_read_always_invert`.  
   **Degenerate-Class Rule:** If $n_1 == 0$ or $n_2 == 0$, $\text{TPR}$, $\text{TNR}$, $\text{BA}$, and $[L_{\text{BA}}, U_{\text{BA}}]$ are undefined (`null`), Fisher's exact $p = 1$ (`1/1`), and the confirmatory test does not pass.

5. **Complete Per-Law Disagreement Log:**
   List **every held-out disagreement by law** (`card_id, law_id, volume, chapter, eq_number, description, b1_ruling, b2_ruling, b3_ruling, b_maj_ruling, pred_ch2, pred_ch16, note`) covering all disagreements among Track `(b)` appliers (`b1`, `b2`, `b3`, `b_maj_ruling`) and Track `(c)` mechanical readings (`pred_ch2`, `pred_ch16`), with a one-line `note` explaining why the disagreement occurred.

#### Single Confirmatory Primary Test (Part 2)
Held-out validation on the `48` OpenStax laws passes iff **ALL THREE** conditions hold simultaneously:
1. Exact rational **3-category Fleiss' $\kappa \ge 0.60$** among `(b1, b2, b3)` across all `48` held-out laws (`{"Keep", "Invert", "the rule doesn't say"}`); **AND**
2. **One-sided Fisher's exact $p < 0.05$** (`fractions.Fraction`, hypergeometric upper tail for $\text{OR} > 1$ on the $2 \times 2$ contingency table `[[TP, FP], [FN, TN]]` with `"Invert"` as the positive class) comparing `R_read_v57_ch16` (`pred_ch16`) against definite `b_maj_ruling` (`"Keep"` / `"Invert"`) on the held-out laws; **AND**
3. **Closed-form 95% Wilson-MOVER lower bound $L_{\text{BA}} > 0.50$** for `R_read_v57_ch16` (`pred_ch16`) against definite `b_maj_ruling`.

If $n_1 == 0$ or $n_2 == 0$ on definite `b_maj_ruling`, Fisher's $p = 1$ (`1/1`), $\text{TPR}/\text{TNR}/\text{BA}/[L_{\text{BA}}, U_{\text{BA}}]$ are `null`, and the confirmatory test does not pass. All other Part 2 metrics (`R_read_v57_ch2`, `b1..b3` vs `pred_ch16`, `R_read_naive_mass`, `R_read_always_keep`, `R_read_always_invert`, unconditional $4 \times 2$ metrics, 2-category Fleiss' $\kappa$ on unanimously definite cards, per-chapter breakdowns, and calibration metrics on `benchmarkRows17`) are reported strictly as descriptive or secondary outputs.

---

## 2. Part 3 Protocol — Etymology Direction With Held-Out Control Pool

### 2.1 Relation to `PROOF.md` Section 3.3
Part 3 replaces the post-hoc `core_law` split in `proof/PROOF.md` Section 3.3 as the confirmatory inferential test of semantic directionality (`person_first` prevalence). Section 3.3 of `proof/PROOF.md` remains preserved in place and marked `DESCRIPTIVE_ONLY_POST_HOC_SPLIT_NOT_INFERENTIAL`.

### 2.2 Verbatim Audit of *SM v57* pp. 170–173 and Locked Target List (`A4`)
Below is the complete verbatim audit of the `Physical` column of **"The reference table"** (*SM v57*, pp. 170–172) and **"Reflected partnerships"** (*SM v57*, p. 173), contrasted where relevant with the `"Co-created result"` column:

#### Verbatim Entries in `Physical` Column (*SM v57*, pp. 170–172 — "The reference table")
- **Properties:** `Limited`; `Resistant`; `Radiation` (corresponding Co-created result on row 3: `Momentum`)
- **Realities:** `Subjective Reality`; `Objective Reality`
- **Continuums:** `Space-Time`
- **Evidence:** `Empirical`
- **Evidence formula:** `Force = Mass × Acceleration`
- **Relational formula:** `E = m × c²`
- **Energy flow:** `Now: active resistance`; `Past: most resistant`
- **Entity contrast:** `Belief: what is true`; `Expectation: what was true`
- **Core interactions:** `Strong force: Expectation`; `Weak force: Belief`
- **Symbols:** `c: the speed of light`; `m: mass` (Co-created result: `Conscious-physical energy (E)`, `Energetic entity`)
- **Entity action:** `Focus`
- **Co-creating partners:** `Electro-Magnetic` (Co-created result: `Momentum`); `Density × Volume`
- **Energy:** `Physical energy (rest and kinetic)`
- **Energy transmutation:** `Actualization`
- **Entity transmutation:** `Out Through`; `In From`

#### Verbatim Entries in `Physical` Column (*SM v57*, p. 173 — "Reflected partnerships")
`Space`; `Time`; `Velocity (Space over Time)`; `Density`; `Volume`; `Focus`; `Acceleration`; `Manifestation`; `Force`; `Strong force (Expectation)`; `Weak force (Belief)`; `Electro`; `Magnetic`.

#### Locked Physical-Quantity Target Word List (`10` Words, Confirmed Under `A4`)
From the `Physical` column entries across *SM v57* pp. 170–173, the locked Part 3 physical-quantity target list (all `10` distinct single lowercase words naming classical/relativistic physical quantities) is:
1. `acceleration` (pp. 171, 173)
2. `density` (pp. 172, 173)
3. `energy` (pp. 171, 172)
4. `force` (pp. 171, 173)
5. `mass` (pp. 171, 172)
6. `space` (pp. 171, 173)
7. `speed` (p. 171 `c: the speed of light`)
8. `time` (pp. 171, 173)
9. `velocity` (p. 173 `Velocity (Space over Time)`)
10. `volume` (pp. 172, 173)

*(Non-quantity relational, temporal, or epistemic labels in the `Physical` column — `actualization`, `belief`, `empirical`, `expectation`, `focus`, `in`/`from`/`out`/`through`, `limited`, `manifestation`, `now`, `objective`, `past`, `resistant`, `subjective` — are excluded from the physical-quantity target set.)*

#### Excluded Borderline Terms From pp. 170–173 (Confirmed Excluded Under `A4`)
Before any OpenStax Key Terms were fetched or Part 3 extraction or coding began, Nicholas confirmed that all `7` borderline terms below are excluded from the Part 3 target set:
1. **`light`** — appears inside `c: the speed of light` (p. 171 `Symbols` row); already in `proof/etymology/ledger_80.json` (`core_law`, `kind: "family"`).
2. **`radiation`** — appears in `Properties` row 3 (p. 170 `Physical` column: `Radiation`); verbal root `radiate` is in `ledger_80.json` (`secondary_physics`).
3. **`electric` / `electro`** — appears as `Electro-Magnetic` (p. 172) and `Electro` (p. 173); `electric` is in `ledger_80.json` (`core_law`, `kind: "household"`).
4. **`magnetic`** — appears as `Electro-Magnetic` (p. 172) and `Magnetic` (p. 173); absent from `ledger_80.json`.
5. **`kinetic`** — appears as `Physical energy (rest and kinetic)` (p. 172); absent from `ledger_80.json`.
6. **`rest`** — appears as `Physical energy (rest and kinetic)` (p. 172); absent from `ledger_80.json`.
7. **`momentum`** — present in `ledger_80.json` (`core_law`, `kind: "family"`), **but appears in the `Co-created result` column (pp. 170, 172), NOT the `Physical` column**.

### 2.3 Control Pool Sampling (`40` Single-Word OpenStax Key Terms, Seed `20261113`)
1. Retrieve verbatim `"Key Terms"` glossary headwords across the exact same 22 OpenStax *University Physics* chapters listed in Section 1.3 (same CC BY 4.0 attribution and same stop rule: halt and report if unfetchable).
2. Retain ONLY raw headword strings matching lowercase ASCII `^[a-z]+$` verbatim (without lowercasing capitalized proper-noun eponyms; this automatically drops multi-word phrases, hyphenated compounds, symbols, and proper-noun eponyms).
3. Deduplicate unique candidate words and apply deterministic exclusions (logging every removed candidate in `proof/heldout/control_exclusion_log.csv`):
   - `C1_IN_LEDGER_80`: exact match to any of the `80` words in `proof/etymology/ledger_80.json`.
   - `C2_CONFIRMED_TARGET`: exact match to any confirmed Part 3 target word.
   - `C3_MORPHOLOGICAL_VARIANT`: fixed inflectional or transparent derivational lemma variant of any word in `ledger_80.json` or any confirmed target word. Specifically, strip standard English suffixes (`-s`, `-es`, `-ed`, `-d`, `-ing`, `-er`, `-est`, `-ly`, `-ness`, `-ment`, `-tion`, `-ation`, `-ion`, `-ity`, `-ance`, `-ence`, `-al`, `-ical`, `-ive`, `-ic`, `-or`, `-y`) and common negating prefixes (`un-`, `in-`, `im-`, `non-`, `re-`), plus compare normalized stems against the explicit list of irregular/Latinate base pairs already represented in `ledger_80.json` (`accelerate/acceleration`, `radiate/radiation`, `expand/expansion`, `vibrate/vibration`, `resist/resistance`, `reflect/reflection`, `resonate/resonance`, `converge/convergence`, `culminate/culmination`, `appreciate/appreciation`, `collect/collection`, `create/creation`, `direct/direction`, `distort/distortion`, `dense/density`, `gravitate/gravity`, `press/pressure`, `real/realize`, `sense/sensation`, `move/movement`). Any Key Term reducing to the same base lemma/stem as a `ledger_80.json` or confirmed target word is logged as `C3_MORPHOLOGICAL_VARIANT` and excluded.
4. Sort remaining eligible control candidates lexicographically (`sorted(eligible_controls)`) and draw `40` control words via:
   `controls_40 = random.Random(20261113).sample(eligible_controls_sorted, 40)` (aborting and reporting if `< 40` eligible terms remain).

### 2.4 Unified Coding Packet, Independent Model Sessions, and Copyright Rule
- **Coding Pool:** Union of:
  1. All confirmed Part 3 target words;
  2. The `40` sampled OpenStax control words; and
  3. Any remaining words from the `35` physics-eligible strata of `proof/etymology/ledger_80.json` (`21 core_law` + `14 secondary_physics`) not already in (1).
- **Deterministic Anonymization:** Deduplicate and sort the combined pool lexicographically, shuffle with `random.Random(20261113)`, assign sequential neutral IDs `W001, W002, ...`, and emit `proof/heldout/word_coding_packet.csv` containing ONLY `(item_id, word)` (zero group labels: target / control / ledger strata are stored separately in `proof/heldout/word_coding_key.csv` and never exposed to coding sessions).
- **3 Independent Model-Family Sessions:** Nicholas submits `word_coding_packet.csv` (with `etymonline.com` entry URLs/records; OED entries added only where supplied by Nicholas) to **3 fresh sessions of 3 distinct model families** with zero access to the repository, `ledger_80.json`, or *The Sovereign Mirror*. Repository agents MUST NOT code `direction_class` or earliest dates.
- **Required Fields per Entry (`proof/heldout/etymology_codings.csv`):**
  - `item_id`, `word`, `etymonline_url`, `etymonline_retrieved_utc`
  - `source_coverage`: `"dual-source-oed"` when Nicholas supplies an OED record, otherwise `"single-source"` (`etymonline.com` only)
  - Per-session fields (`s1..s3`): `earliest_person_sense`, `earliest_physics_sense`, and `direction_class` $\in \{\text{"person\_first"}, \text{"physics\_first"}, \text{"both\_from\_start"}, \text{"no\_person\_sense"}\}$
  - Strict 2/3 majority `direction_class_maj` (if 3 sessions return 3 distinct categories, record `"tie_or_disagreement"` and preserve all 3 session labels; for the primary binary contrast `"person_first"` vs not-`"person_first"`, 3 binary votes admit no tie).
- **Commit Order:** `proof/heldout/etymology_codings.csv` MUST be committed to git BEFORE any script joins it with `proof/heldout/word_coding_key.csv`.
- **Copyright Restriction:** Zero prose definitions, glosses, or excerpted dictionary sentences from `etymonline.com` or OED may be committed anywhere in the repository. Only entry URLs, UTC retrieval dates, `source_coverage`, brief attestation dates/sense category tags (`earliest_person_sense`, `earliest_physics_sense`), and coded `direction_class` values may be committed.

### 2.5 Agreement Check (`35` Physics-Eligible Ledger Words) and Confirmatory Primary Test
- **Descriptive Ledger Agreement (`n = 35`):** Across the `35` physics-eligible words (`21 core_law + 14 secondary_physics`) of `proof/etymology/ledger_80.json`, compute `%` agreement and Cohen's $\kappa$ between newly coded binary `(direction_class_maj == "person_first")` and `ledger_80.json` `(kind == "inward first")` (as well as reporting against `kind in {"inward first", "either side"}`), alongside the full $4 \times 8$ cross-tabulation against `ledger_80.json` `kind` values.
- **Single Confirmatory Primary Test (Part 3):**
  Compare the proportion of `person_first` (`direction_class_maj == "person_first"`) among **confirmed Part 3 target words** vs. the **`40` OpenStax control words** on the `etymonline` dataset using the one-sided Fisher's exact test (`fractions.Fraction`, upper tail for target `person_first` proportion $>$ control `person_first` proportion).
  - **Confirmatory Support Criterion:** Exact Fisher $p < 0.05$.
  - All other statistics (OED sensitivity subset where supplied, 35-word ledger comparison, target-subset breakdowns) are explicitly descriptive.

---

## 3. Part 4 Protocol — Verification CI Workflow and Break-It Mutation Suite

### 3.1 Continuous Integration Workflow (`.github/workflows/verify-proofs.yml`)
- **Runner & Toolchain Pins:** Runs on `ubuntu-latest`, installs Lean `v4.35.0` (matching `proof/lean/lean-toolchain` `leanprover/lean4:v4.35.0`) and Python package `z3-solver==5.4.1` (matching `proof/verification_certificate.json`), builds/runs `python proof/run_all_proofs.py` from repository root.
- **Certificate Reproducibility Gate:** Diffs the freshly generated `proof/verification_certificate.json` against the committed `proof/verification_certificate.json` and **fails the CI job** if ANY field or nested value differs outside the exact 5 permitted platform/runtime metadata keys:
  1. `execution_os`
  2. `execution_arch`
  3. `python_version`
  4. `lean_version`
  5. `verification_runtime_seconds`

### 3.2 Break-It Mutation Suite (`M01`–`M15`)
- **Temp-Copy Isolation:** The Part 4 mutation runner copies the repository (excluding `.git`/transient caches or into an isolated temporary workspace) for each mutation `M01`–`M15` independently, applies the single-point edit, runs the relevant verifier (`lake build` for Lean mutations, `run_all_proofs.py` / module verifier for Z3 and Python mutations), checks that the verification fails with non-zero exit status, and deletes the temporary directory. The live working tree is NEVER mutated.
- **Reporting & Existing Audits:** Reports `caught / 15` and explicitly names every surviving mutation (`0` survivors required for pass). The existing kernel axiom audit (`proof_axiom_checks` / `#print axioms`) and negative typecheck suite in `proof/run_all_proofs.py` remain unchanged and active.

#### Exact 15-Mutation Specification Table (`M01`–`M15`)

| ID | File Path | Symbol & Mutation Kind | Expected Failing Check |
|---|---|---|---|
| `M01` | `proof/lean/TSR/Condition.lean` | `barrier` (Lean definition) | `lake build` fails at `condition_triad_equivalence` / `destructive_null_requires_spatial_separation` |
| `M02` | `proof/lean/TSR/Condition.lean` | `condition_triad_equivalence` (Lean theorem assumption) | `lake build` fails at `condition_triad_equivalence` (missing partition assumption `hPart`) |
| `M03` | `proof/lean/TSR/Condition.lean` | `damped_ripple_strict_decay` (Lean theorem assumption) | `lake build` fails at `damped_ripple_strict_decay` (`M.alpha_bounds_of_pos hRes` type mismatch) |
| `M04` | `proof/lean/TSR/MirrorFunctor.lean` | `mirrorAtom` (Lean definition) | `lake build` fails at `mirrorAtom_involutive` / `R_form_involutive` |
| `M05` | `proof/lean/TSR/MirrorFunctor.lean` | `regionResistant` (Lean definition) | `lake build` fails at `two_level_reading_theorem` (`decide`) and `gravity_open_joint_two_vs_three_regions` |
| `M06` | `proof/lean/TSR/MirrorFunctor.lean` | `benchmarkRows17` Row 2 (Lean benchmark row) | `lake build` fails at `two_level_reading_theorem` and `v57_rule_wordings_benchmark` (`decide`) |
| `M07` | `proof/lean/TSR/MirrorFunctor.lean` | `benchmarkRows17` Row 7 (Lean benchmark row) | `lake build` fails at `two_level_reading_theorem` and `v57_rule_wordings_benchmark` (`decide`) |
| `M08` | `proof/lean/TSR/MirrorFunctor.lean` | `isSharedEnergyWork` (Lean definition) | `lake build` fails at `v57_rule_wordings_benchmark` (`decide`: `R_read_v57_ch16` match count drops from 16 to 14) |
| `M09` | `proof/lean/TSR/Crossing.lean` | `canStep` (Lean definition) | `lake build` fails at `step_from_intuition_false` and `unique_weak_diagonal_escape` |
| `M10` | `proof/lean/TSR/EntityAndMeta.lean` | `sovereignEntityDyn` (Lean definition) | `lake build` fails at `four_way_entity_separation` |
| `M11` | `proof/z3/structural_rigidity.py` | `_build_stage_relations` (Z3 Stage 2 relation graph) | `run_structural_rigidity()` raises `AssertionError: Expected 2 at Stage 2, got 4` |
| `M12` | `proof/z3/structural_rigidity.py` | `_build_stage_relations` (Z3 Stage 3 relation graph) | `run_structural_rigidity()` raises `AssertionError: Expected 1 at Stage 3, got 2` |
| `M13` | `proof/z3/lexical_rigidity.py` | `SLOT_REQUIREMENTS["Expansion"]` (Z3 lexical slot) | `verify_tsr_sat_and_uniqueness()` raises `AssertionError: Canonical TSR assignment must be globally unique!` |
| `M14` | `proof/etymology/combinatorial_proofs.py` | `shares_4char_substring` (Python combinatorics) | `verify_part3_invariants()` fails `N_orth_unrelated == 3152` (becomes `3153`) and `run_self_tests()` fails |
| `M15` | `proof/etymology/combinatorial_proofs.py` | `exact_hypergeometric_upper_tail` (Python `fractions` primary test) | `verify_part3_invariants()` fails `0.287 < exact_hypergeometric_p_float < 0.289` (`p` drops to `0.0429`) |

#### Exact Verbatim Single-Point Snippets (`M01`–`M15`)

- **`M01`** — `proof/lean/TSR/Condition.lean` (`barrier`)
  - Original:
```lean
def barrier (M : Medium F) (x y : M.Locus) : F := M.rho * M.dist x y
```
  - Mutated:
```lean
def barrier (M : Medium F) (_x _y : M.Locus) : F := zero
```

- **`M02`** — `proof/lean/TSR/Condition.lean` (`condition_triad_equivalence`)
  - Original:
```lean
theorem condition_triad_equivalence (M : Medium F) (hPart : IsPartitionedMedium M) :
```
  - Mutated:
```lean
theorem condition_triad_equivalence (M : Medium F) :
```

- **`M03`** — `proof/lean/TSR/Condition.lean` (`damped_ripple_strict_decay`)
  - Original:
```lean
theorem damped_ripple_strict_decay (M : PerturbationMedium F)
    (hRes : zero < M.rho) (B0 : F) (hB0 : zero < B0)
```
  - Mutated:
```lean
theorem damped_ripple_strict_decay (M : PerturbationMedium F)
    (hRes : zero ≤ M.rho) (B0 : F) (hB0 : zero < B0)
```

- **`M04`** — `proof/lean/TSR/MirrorFunctor.lean` (`mirrorAtom`)
  - Original:
```lean
  | .lightSpeed => .current
```
  - Mutated:
```lean
  | .lightSpeed => .attraction
```

- **`M05`** — `proof/lean/TSR/MirrorFunctor.lean` (`regionResistant`)
  - Original:
```lean
def regionResistant : MirrorRegion → Bool
  | .physical      => true
  | .nonphysical   => false
  | .sharedOverlap => false
```
  - Mutated:
```lean
def regionResistant : MirrorRegion → Bool
  | .physical      => true
  | .nonphysical   => false
  | .sharedOverlap => true
```

- **`M06`** — `proof/lean/TSR/MirrorFunctor.lean` (`benchmarkRows17` Row 2)
  - Original:
```lean
  ⟨2,  "2 no shared now (distance)",      .Invert, false, .SpatialSeparationDependence⟩,
```
  - Mutated:
```lean
  ⟨2,  "2 no shared now (distance)",      .Keep, false, .SpatialSeparationDependence⟩,
```

- **`M07`** — `proof/lean/TSR/MirrorFunctor.lean` (`benchmarkRows17` Row 7)
  - Original:
```lean
  ⟨7,  "7 E = mc^2",                      .Keep,   true,  .IdentityOrEquiv⟩,
```
  - Mutated:
```lean
  ⟨7,  "7 E = mc^2",                      .Invert,   true,  .IdentityOrEquiv⟩,
```

- **`M08`** — `proof/lean/TSR/MirrorFunctor.lean` (`isSharedEnergyWork`)
  - Original:
```lean
def isSharedEnergyWork : LawAST → Bool
  | .SharedCenterCurvature => true
  | _                      => false
```
  - Mutated:
```lean
def isSharedEnergyWork : LawAST → Bool
  | .SharedCenterCurvature => false
  | _                      => false
```

- **`M09`** — `proof/lean/TSR/Crossing.lean` (`canStep`)
  - Original:
```lean
  | (.NP, .In),  (.P,  .Out) => tuned  -- Weak Diagonal: Intuition shifts Belief iff tuned
```
  - Mutated:
```lean
  | (.NP, .In),  (.P,  .Out) => true
```

- **`M10`** — `proof/lean/TSR/EntityAndMeta.lean` (`sovereignEntityDyn`)
  - Original:
```lean
  stepOuterObjective := fun st x => st.outerObjective + predErrorSq st x
```
  - Mutated:
```lean
  stepOuterObjective := fun st _ => st.outerObjective
```

- **`M11`** — `proof/z3/structural_rigidity.py` (`_build_stage_relations`, Stage 2)
  - Original:
```python
        rels["gate_cocreates_center2"] = (2, {(IDX["Tune"], IDX["Attraction"])})
```
  - Mutated:
```python
        # disabled gate_cocreates_center2
```

- **`M12`** — `proof/z3/structural_rigidity.py` (`_build_stage_relations`, Stage 3)
  - Original:
```python
    if stage >= 3:
```
  - Mutated:
```python
    if stage >= 99:
```

- **`M13`** — `proof/z3/lexical_rigidity.py` (`SLOT_REQUIREMENTS["Expansion"]`)
  - Original:
```python
        ("continuum_unfolding_sense", "Expansion_names_unbounded_continuum_unfolding_rather_than_organismal_lifecycle"),
```
  - Mutated:
```python
        # removed continuum_unfolding_sense
```

- **`M14`** — `proof/etymology/combinatorial_proofs.py` (`shares_4char_substring`)
  - Original:
```python
    if fam_a == "ment" and fam_b == "ment" and a[:2] == b[:2]:
        return True
```
  - Mutated:
```python
    if fam_a == "ment" and fam_b == "ment" and a[:2] == b[:2]:
        return False
```

- **`M15`** — `proof/etymology/combinatorial_proofs.py` (`exact_hypergeometric_upper_tail`)
  - Original:
```python
    for k in range(obs_k, max_k + 1):
```
  - Mutated:
```python
    for k in range(obs_k + 1, max_k + 1):
```
