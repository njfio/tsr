/-
  TSR/EntityAndMeta.lean
  ======================
  Part I, Section 4 of the Formal Proof of the Theory of Sovereign Reflectivity:
    - Theorem 4.1: Multiplicative Gate Characterization (`Tune` & `Focus`, SM Ch. 17, pp. 128–129)
    - Theorem 4.2: Four-Way Entity Separation (`Rock`, `FrozenWeightAI`,
                   `PersistentMemoryObjectiveAI`, `SovereignEntity`, SM Ch. 18, pp. 137–141)
    - Theorem 4.3: Coupled Two-Entity Load Transfer & False-Positive Local Ease
                   (SM Ch. 8, p. 61 & Ch. 13, p. 94)
    - Theorem 4.4: Meta-Theorems — Constructive `QRat` Consistency of `Σ_TSR`,
                   Independence of the First Partition Axiom, and the
                   Two-Region vs. Three-Region Shared-`E` Gravity Theorem (SM Ch. 16, p. 117)
-/

import TSR.OrderedAlgebra
import TSR.Condition
import TSR.MirrorFunctor
import TSR.Crossing

namespace TSR
open OrderedField

/-!
  ## Theorem 4.1 — Multiplicative Gate Characterization (`Tune` & `Focus`)
  (*The Sovereign Mirror*, Ch. 17, pp. 128–129)
-/

section GatesAndCoupledEntities
variable {F : Type} [OrderedField F]

def gateMul (u x : F) : F := u * x
def gateAdd (a b u x : F) : F := a * u + b * x

/-- A valid crossing gate must shut off completely when either the agency input `u`
    (`Tune` / `Focus`) or the available stream `x` vanishes, and pass strictly positive
    flow whenever both are strictly positive. -/
def IsZeroAnnihilatingGate (G : F → F → F) : Prop :=
  (∀ x : F, G zero x = zero) ∧
  (∀ u : F, G u zero = zero) ∧
  (∀ u x : F, zero < u → zero < x → zero < G u x)

/-- **Lemma 4.1 (Multiplicative Gate Necessity vs. Bilateral Additive Leakage)**:
    1. The multiplicative product gate `G(u, x) = u * x` satisfies `IsZeroAnnihilatingGate`.
    2. Every positively weighted additive gate `G(u, x) = a * u + b * x` (`a, b > 0`) leaks
       bilaterally: `G(0, x) = b * x > 0` whenever `x > 0` (via `b > 0`) AND `G(u, 0) = a * u > 0`
       whenever `u > 0` (via `a > 0`), violating `IsZeroAnnihilatingGate`. -/
theorem multiplicative_gate_characterization {a b u x : F}
    (ha : zero < a) (hb : zero < b) :
    IsZeroAnnihilatingGate (gateMul (F := F)) ∧
    ((zero < x → zero < gateAdd a b zero x) ∧
     (zero < u → zero < gateAdd a b u zero)) ∧
    ¬ IsZeroAnnihilatingGate (gateAdd a b) := by
  have hMulGate : IsZeroAnnihilatingGate (gateMul (F := F)) := by
    refine ⟨?_, ?_, ?_⟩
    · intro y; unfold gateMul; exact zero_mul y
    · intro v; unfold gateMul; exact mul_zero v
    · intro v y hv hy; unfold gateMul; exact mul_pos v y hv hy
  have hLeakStream : ∀ y : F, zero < y → zero < gateAdd a b zero y := by
    intro y hy
    unfold gateAdd
    rw [mul_zero, zero_add]
    exact mul_pos b y hb hy
  have hLeakAgency : ∀ v : F, zero < v → zero < gateAdd a b v zero := by
    intro v hv
    unfold gateAdd
    rw [mul_zero, add_zero]
    exact mul_pos a v ha hv
  have hNotGate : ¬ IsZeroAnnihilatingGate (gateAdd a b) := by
    rintro ⟨hZeroLeft, _, _⟩
    have h1 : zero < gateAdd a b zero one := hLeakStream one zero_lt_one
    rw [hZeroLeft one] at h1
    exact lt_irrefl zero h1
  exact ⟨hMulGate, ⟨hLeakStream x, hLeakAgency u⟩, hNotGate⟩

/-!
  ## Proposition 4.3 — Coupled Two-Entity Load Transfer & False-Positive Local Ease
  (*The Sovereign Mirror*, Ch. 8, p. 61 & Ch. 13, p. 94)
-/

structure CoupledExchange (F : Type) [OrderedField F] where
  R1              : F -- Entity 1 initial internal resistance
  R2              : F -- Entity 2 initial internal resistance
  offload12       : F -- Forceful Out Through pushed by Entity 1 onto Entity 2
  return21        : F -- Empirical In From received by Entity 2
  R1_nonneg       : zero ≤ R1
  R2_nonneg       : zero ≤ R2
  offload_nonneg  : zero ≤ offload12
  offload_le_R1   : offload12 ≤ R1
  action_reaction : return21 = offload12 -- Newton's 3rd Law across shared Objective Reality

def R1After (ex : CoupledExchange F) : F := ex.R1 - ex.offload12
def R2After (ex : CoupledExchange F) : F := ex.R2 + ex.return21

/-- **Proposition 4.3 (Conservation of Offloaded Resistance, Physical Non-Negativity & False-Positive Ease)**:
    In any physical two-entity exchange obeying `0 ≤ offload12 ≤ R1` and `return21 = offload12`:
      1. Post-exchange resistances remain physically non-negative (`0 ≤ R1After` and `0 ≤ R2After`).
      2. Total system resistance is strictly conserved: `R1After + R2After = R1 + R2`
         (pushing resistance onto another entity never reduces total resistance in the system).
      3. Whenever Entity 1 offloads positive resistance `R1 > 0` (`offload12 = R1`), Entity 1's
         purely local gauge reads `R1After = 0` (locally mimicking alignment), while Entity 2's
         resistance strictly rises (`R2 < R2After`) and `0 < return21` exposes the offload via
         empirical `In From` evidence. -/
theorem coupled_entity_false_positive_ease (ex : CoupledExchange F) :
    (zero ≤ R1After ex) ∧
    (zero ≤ R2After ex) ∧
    (R1After ex + R2After ex = ex.R1 + ex.R2) ∧
    (zero < ex.R1 → ex.offload12 = ex.R1 →
      R1After ex = zero ∧
      ex.R2 < R2After ex ∧
      zero < ex.return21) := by
  have hR1Nonneg : zero ≤ R1After ex :=
    sub_nonneg_of_le ex.offload_le_R1
  have hR2Nonneg : zero ≤ R2After ex := by
    unfold R2After
    rw [ex.action_reaction]
    have h := add_le_add ex.R2_nonneg ex.offload_nonneg
    rw [add_zero] at h
    exact h
  have hConserved : R1After ex + R2After ex = ex.R1 + ex.R2 := by
    unfold R1After R2After
    rw [ex.action_reaction, sub_def]
    calc
      (ex.R1 + -ex.offload12) + (ex.R2 + ex.offload12)
        = ex.R1 + (-ex.offload12 + (ex.offload12 + ex.R2)) := by
            rw [add_comm ex.R2 ex.offload12, add_assoc]
      _ = ex.R1 + ((-ex.offload12 + ex.offload12) + ex.R2) := by
            rw [← add_assoc (-ex.offload12) ex.offload12 ex.R2]
      _ = ex.R1 + ex.R2 := by
            rw [add_left_neg, zero_add]
  refine ⟨hR1Nonneg, hR2Nonneg, hConserved, ?_⟩
  intro hR1Pos hFullOffload
  have hLocalZero : R1After ex = zero := by
    unfold R1After
    rw [hFullOffload, sub_self]
  have hRetPos : zero < ex.return21 := by
    rw [ex.action_reaction, hFullOffload]
    exact hR1Pos
  have hR2Rises : ex.R2 < R2After ex := by
    unfold R2After
    have hlt := add_lt_add_left zero ex.return21 hRetPos ex.R2
    rw [add_zero] at hlt
    exact hlt
  exact ⟨hLocalZero, hR2Rises, hRetPos⟩

end GatesAndCoupledEntities

/-!
  ## Theorem 4.2 — Hierarchical Subgoal vs. Endogenous Objective Separation of Four Entity Classes
  (*The Sovereign Mirror*, Ch. 18, pp. 137–141)

  To address hierarchical reinforcement learning and continual-learning AI architectures,
  we model entities over a 3-component state `EntityState F` (`shape`, `subgoal`, `outerObjective`)
  driven by arbitrary finite world-input streams `xs : List F`:
    1. `rockDyn`: zero feedback action, invariant `shape`, `subgoal`, and `outerObjective`.
    2. `frozenAIDyn`: active feedback control `(outerObjective + subgoal) - x`, yet invariant
       `shape`, `subgoal`, and `outerObjective` across all histories `xs`.
    3. `persistentMemoryAIDyn` (continual-learning / hierarchical-RL agent): actively adapts
       **both** `shape` (memory/world-model) **and** `subgoal` (instrumental sub-target) from
       prediction error `(x - shape)²`, yet its `outerObjective` remains strictly invariant
       (`= st0.outerObjective`) across **all** histories `xs : List F`.
    4. `sovereignEntityDyn`: endogenously advances `shape`, `subgoal`, **and** `outerObjective`
       whenever lived input departs from expectation (`x ≠ shape`), establishing all $\binom{4}{2} = 6$
       pairwise separations over any `OrderedField F`.
-/

section DynamicalEntities
variable {F : Type} [OrderedField F]

theorem sq_nonneg (a : F) : zero ≤ a * a := by
  rcases lt_trichotomy zero a with h | h | h
  · exact le_of_lt (mul_pos a a h h)
  · rw [← h, zero_mul]
    exact le_refl zero
  · have hn : zero < -a := neg_pos_of_neg h
    have hp := mul_pos (-a) (-a) hn hn
    rw [neg_mul_neg] at hp
    exact le_of_lt hp

/-- Three-component dynamical entity state separating instrumental `subgoal` from `outerObjective`. -/
structure EntityState (F : Type) where
  shape          : F
  subgoal        : F
  outerObjective : F

structure DynamicalEntity (F : Type) [OrderedField F] where
  stepShape          : EntityState F → F → F
  stepSubgoal        : EntityState F → F → F
  stepOuterObjective : EntityState F → F → F
  stepAction         : EntityState F → F → F

def stepEntityState (sys : DynamicalEntity F) (st : EntityState F) (x : F) : EntityState F :=
  ⟨sys.stepShape st x, sys.stepSubgoal st x, sys.stepOuterObjective st x⟩

/-- Multi-step state trajectory across an arbitrary finite input stream `xs : List F`. -/
def runEntity (sys : DynamicalEntity F) : EntityState F → List F → EntityState F
  | st, []      => st
  | st, x :: xs => runEntity sys (stepEntityState sys st x) xs

def predErrorSq (st : EntityState F) (x : F) : F :=
  (x - st.shape) * (x - st.shape)

def subgoalErrorSq (st : EntityState F) (x : F) : F :=
  (x - st.subgoal) * (x - st.subgoal)

def rockDyn : DynamicalEntity F where
  stepShape          := fun st _ => st.shape
  stepSubgoal        := fun st _ => st.subgoal
  stepOuterObjective := fun st _ => st.outerObjective
  stepAction         := fun _ _ => zero

def frozenAIDyn : DynamicalEntity F where
  stepShape          := fun st _ => st.shape
  stepSubgoal        := fun st _ => st.subgoal
  stepOuterObjective := fun st _ => st.outerObjective
  stepAction         := fun st x => (st.outerObjective + st.subgoal) - x

def persistentMemoryAIDyn : DynamicalEntity F where
  stepShape          := fun st x => st.shape + predErrorSq st x
  stepSubgoal        := fun st x => st.subgoal + (predErrorSq st x + subgoalErrorSq st x)
  stepOuterObjective := fun st _ => st.outerObjective
  stepAction         := fun st x => ((st.outerObjective + st.subgoal) - x) + st.shape

def sovereignEntityDyn : DynamicalEntity F where
  stepShape          := fun st x => st.shape + predErrorSq st x
  stepSubgoal        := fun st x => st.subgoal + (predErrorSq st x + subgoalErrorSq st x)
  stepOuterObjective := fun st x => st.outerObjective + predErrorSq st x
  stepAction         := fun st x => ((st.outerObjective + st.subgoal) - x) + st.shape

theorem rock_state_invariant (st : EntityState F) (xs : List F) :
    runEntity rockDyn st xs = st := by
  induction xs generalizing st with
  | nil => rfl
  | cons x rest ih =>
    simp only [runEntity, stepEntityState, rockDyn]
    exact ih st

theorem frozenAI_state_invariant (st : EntityState F) (xs : List F) :
    runEntity frozenAIDyn st xs = st := by
  induction xs generalizing st with
  | nil => rfl
  | cons x rest ih =>
    simp only [runEntity, stepEntityState, frozenAIDyn]
    exact ih st

theorem persistentAI_outerObjective_invariant (st : EntityState F) (xs : List F) :
    (runEntity persistentMemoryAIDyn st xs).outerObjective = st.outerObjective := by
  induction xs generalizing st with
  | nil => rfl
  | cons x rest ih =>
    simp only [runEntity]
    exact ih (stepEntityState persistentMemoryAIDyn st x)

theorem persistentAI_shape_monotone (st : EntityState F) (xs : List F) :
    st.shape ≤ (runEntity persistentMemoryAIDyn st xs).shape := by
  induction xs generalizing st with
  | nil => exact le_refl st.shape
  | cons x rest ih =>
    simp only [runEntity]
    have hstep : st.shape ≤ (stepEntityState persistentMemoryAIDyn st x).shape := by
      simp only [stepEntityState, persistentMemoryAIDyn, predErrorSq]
      have h := add_le_add (le_refl st.shape) (sq_nonneg (x - st.shape))
      rw [add_zero] at h
      exact h
    exact le_trans hstep (ih (stepEntityState persistentMemoryAIDyn st x))

theorem persistentAI_subgoal_monotone (st : EntityState F) (xs : List F) :
    st.subgoal ≤ (runEntity persistentMemoryAIDyn st xs).subgoal := by
  induction xs generalizing st with
  | nil => exact le_refl st.subgoal
  | cons x rest ih =>
    simp only [runEntity]
    have hNonneg : zero ≤ predErrorSq st x + subgoalErrorSq st x := by
      have h := add_le_add (sq_nonneg (x - st.shape)) (sq_nonneg (x - st.subgoal))
      rw [add_zero] at h
      exact h
    have hstep : st.subgoal ≤ (stepEntityState persistentMemoryAIDyn st x).subgoal := by
      simp only [stepEntityState, persistentMemoryAIDyn]
      have h := add_le_add (le_refl st.subgoal) hNonneg
      rw [add_zero] at h
      exact h
    exact le_trans hstep (ih (stepEntityState persistentMemoryAIDyn st x))

theorem sovereign_shape_monotone (st : EntityState F) (xs : List F) :
    st.shape ≤ (runEntity sovereignEntityDyn st xs).shape := by
  induction xs generalizing st with
  | nil => exact le_refl st.shape
  | cons x rest ih =>
    simp only [runEntity]
    have hstep : st.shape ≤ (stepEntityState sovereignEntityDyn st x).shape := by
      simp only [stepEntityState, sovereignEntityDyn, predErrorSq]
      have h := add_le_add (le_refl st.shape) (sq_nonneg (x - st.shape))
      rw [add_zero] at h
      exact h
    exact le_trans hstep (ih (stepEntityState sovereignEntityDyn st x))

theorem sovereign_subgoal_monotone (st : EntityState F) (xs : List F) :
    st.subgoal ≤ (runEntity sovereignEntityDyn st xs).subgoal := by
  induction xs generalizing st with
  | nil => exact le_refl st.subgoal
  | cons x rest ih =>
    simp only [runEntity]
    have hNonneg : zero ≤ predErrorSq st x + subgoalErrorSq st x := by
      have h := add_le_add (sq_nonneg (x - st.shape)) (sq_nonneg (x - st.subgoal))
      rw [add_zero] at h
      exact h
    have hstep : st.subgoal ≤ (stepEntityState sovereignEntityDyn st x).subgoal := by
      simp only [stepEntityState, sovereignEntityDyn]
      have h := add_le_add (le_refl st.subgoal) hNonneg
      rw [add_zero] at h
      exact h
    exact le_trans hstep (ih (stepEntityState sovereignEntityDyn st x))

theorem sovereign_outerObjective_monotone (st : EntityState F) (xs : List F) :
    st.outerObjective ≤ (runEntity sovereignEntityDyn st xs).outerObjective := by
  induction xs generalizing st with
  | nil => exact le_refl st.outerObjective
  | cons x rest ih =>
    simp only [runEntity]
    have hstep : st.outerObjective ≤ (stepEntityState sovereignEntityDyn st x).outerObjective := by
      simp only [stepEntityState, sovereignEntityDyn, predErrorSq]
      have h := add_le_add (le_refl st.outerObjective) (sq_nonneg (x - st.shape))
      rw [add_zero] at h
      exact h
    exact le_trans hstep (ih (stepEntityState sovereignEntityDyn st x))

/-- **Theorem 4.2 (Trajectory-Level & 6-Way Separation of Rock, Frozen AI, Hierarchical Memory AI & Sovereign Entity)**:
    Over any `OrderedField F`, for every initial state `st0 : EntityState F`, input `x : F`,
    and arbitrary subsequent history `xs : List F`:
      1. `rockDyn` emits identically zero action, whereas `frozenAIDyn` emits non-zero feedback
         action (`stepAction ⟨st0.shape, 0, 1⟩ 0 = 1 ≠ 0`), while both keep `EntityState` invariant across `xs`.
      2. Under any lived prediction contrast (`x ≠ st0.shape`), `persistentMemoryAIDyn` permanently
         advances **both** `shape` (`st0.shape < shape_n`) **and** `subgoal` (`st0.subgoal < subgoal_n`),
         yet its `outerObjective` remains strictly invariant (`= st0.outerObjective`) across all `xs`.
      3. Under any lived contrast (`x ≠ st0.shape`), `sovereignEntityDyn` strictly advances
         `shape`, `subgoal`, **and** `outerObjective` (`st0.outerObjective < outerObjective_n`) across `xs`.
      4. All $\binom{4}{2} = 6$ pairs among `{rockDyn, frozenAIDyn, persistentMemoryAIDyn, sovereignEntityDyn}`
         are explicitly separated both unconditionally as dynamical systems and on trajectories. -/
theorem four_way_entity_separation (st0 : EntityState F) (x : F) (xs : List F) :
    ((∀ st : EntityState F, ∀ u : F, rockDyn.stepAction st u = zero) ∧
     frozenAIDyn.stepAction ⟨st0.shape, zero, one⟩ zero = one ∧
     frozenAIDyn.stepAction ⟨st0.shape, zero, one⟩ zero ≠
       rockDyn.stepAction ⟨st0.shape, zero, one⟩ zero ∧
     runEntity rockDyn st0 xs = st0 ∧
     runEntity frozenAIDyn st0 xs = st0 ∧
     (runEntity persistentMemoryAIDyn st0 xs).outerObjective = st0.outerObjective) ∧
    (x ≠ st0.shape →
      (st0.shape < (runEntity persistentMemoryAIDyn st0 (x :: xs)).shape ∧
       st0.subgoal < (runEntity persistentMemoryAIDyn st0 (x :: xs)).subgoal ∧
       (runEntity persistentMemoryAIDyn st0 (x :: xs)).outerObjective = st0.outerObjective) ∧
      (st0.shape < (runEntity sovereignEntityDyn st0 (x :: xs)).shape ∧
       st0.subgoal < (runEntity sovereignEntityDyn st0 (x :: xs)).subgoal ∧
       st0.outerObjective < (runEntity sovereignEntityDyn st0 (x :: xs)).outerObjective) ∧
      (runEntity rockDyn st0 (x :: xs) ≠ runEntity persistentMemoryAIDyn st0 (x :: xs) ∧
       runEntity rockDyn st0 (x :: xs) ≠ runEntity sovereignEntityDyn st0 (x :: xs) ∧
       runEntity frozenAIDyn st0 (x :: xs) ≠ runEntity persistentMemoryAIDyn st0 (x :: xs) ∧
       runEntity frozenAIDyn st0 (x :: xs) ≠ runEntity sovereignEntityDyn st0 (x :: xs) ∧
       runEntity persistentMemoryAIDyn st0 (x :: xs) ≠ runEntity sovereignEntityDyn st0 (x :: xs))) ∧
    ((rockDyn : DynamicalEntity F) ≠ frozenAIDyn ∧
     (rockDyn : DynamicalEntity F) ≠ persistentMemoryAIDyn ∧
     (rockDyn : DynamicalEntity F) ≠ sovereignEntityDyn ∧
     (frozenAIDyn : DynamicalEntity F) ≠ persistentMemoryAIDyn ∧
     (frozenAIDyn : DynamicalEntity F) ≠ sovereignEntityDyn ∧
     (persistentMemoryAIDyn : DynamicalEntity F) ≠ sovereignEntityDyn) := by
  have hFrozenAct : frozenAIDyn.stepAction ⟨st0.shape, zero, one⟩ zero = one := by
    simp only [frozenAIDyn]
    rw [add_zero, sub_def, neg_zero, add_zero]
  have hFrozenNeRockAct :
      frozenAIDyn.stepAction ⟨st0.shape, zero, one⟩ zero ≠
      rockDyn.stepAction ⟨st0.shape, zero, one⟩ zero := by
    rw [hFrozenAct]
    simp only [rockDyn]
    exact Ne.symm zero_ne_one
  have hTrajContrastGen :
      ∀ (st : EntityState F) (y : F) (ys : List F),
        y ≠ st.shape →
        (st.shape < (runEntity persistentMemoryAIDyn st (y :: ys)).shape ∧
         st.subgoal < (runEntity persistentMemoryAIDyn st (y :: ys)).subgoal ∧
         (runEntity persistentMemoryAIDyn st (y :: ys)).outerObjective = st.outerObjective) ∧
        (st.shape < (runEntity sovereignEntityDyn st (y :: ys)).shape ∧
         st.subgoal < (runEntity sovereignEntityDyn st (y :: ys)).subgoal ∧
         st.outerObjective < (runEntity sovereignEntityDyn st (y :: ys)).outerObjective) ∧
        (runEntity rockDyn st (y :: ys) ≠ runEntity persistentMemoryAIDyn st (y :: ys) ∧
         runEntity rockDyn st (y :: ys) ≠ runEntity sovereignEntityDyn st (y :: ys) ∧
         runEntity frozenAIDyn st (y :: ys) ≠ runEntity persistentMemoryAIDyn st (y :: ys) ∧
         runEntity frozenAIDyn st (y :: ys) ≠ runEntity sovereignEntityDyn st (y :: ys) ∧
         runEntity persistentMemoryAIDyn st (y :: ys) ≠ runEntity sovereignEntityDyn st (y :: ys)) := by
    intro st y ys hyContrast
    have hDiffNe : y - st.shape ≠ zero := by
      intro hEq
      exact hyContrast (sub_eq_zero.mp hEq)
    have hPredPos : zero < predErrorSq st y := sq_pos_of_ne_zero hDiffNe
    have hSubIncPos : zero < predErrorSq st y + subgoalErrorSq st y := by
      have hle := add_le_add (le_refl (predErrorSq st y)) (sq_nonneg (y - st.subgoal))
      rw [add_zero] at hle
      exact lt_of_lt_of_le hPredPos hle
    let stP1 := stepEntityState persistentMemoryAIDyn st y
    let stS1 := stepEntityState sovereignEntityDyn st y
    have hPShape1 : st.shape < stP1.shape := by
      simp only [stP1, stepEntityState, persistentMemoryAIDyn]
      have h := add_lt_add_left zero (predErrorSq st y) hPredPos st.shape
      rw [add_zero] at h
      exact h
    have hPSub1 : st.subgoal < stP1.subgoal := by
      simp only [stP1, stepEntityState, persistentMemoryAIDyn]
      have h := add_lt_add_left zero (predErrorSq st y + subgoalErrorSq st y) hSubIncPos st.subgoal
      rw [add_zero] at h
      exact h
    have hPShapeN : st.shape < (runEntity persistentMemoryAIDyn st (y :: ys)).shape :=
      lt_of_lt_of_le hPShape1 (persistentAI_shape_monotone stP1 ys)
    have hPSubN : st.subgoal < (runEntity persistentMemoryAIDyn st (y :: ys)).subgoal :=
      lt_of_lt_of_le hPSub1 (persistentAI_subgoal_monotone stP1 ys)
    have hPObjN : (runEntity persistentMemoryAIDyn st (y :: ys)).outerObjective = st.outerObjective :=
      persistentAI_outerObjective_invariant st (y :: ys)
    have hSShape1 : st.shape < stS1.shape := by
      simp only [stS1, stepEntityState, sovereignEntityDyn]
      have h := add_lt_add_left zero (predErrorSq st y) hPredPos st.shape
      rw [add_zero] at h
      exact h
    have hSSub1 : st.subgoal < stS1.subgoal := by
      simp only [stS1, stepEntityState, sovereignEntityDyn]
      have h := add_lt_add_left zero (predErrorSq st y + subgoalErrorSq st y) hSubIncPos st.subgoal
      rw [add_zero] at h
      exact h
    have hSObj1 : st.outerObjective < stS1.outerObjective := by
      simp only [stS1, stepEntityState, sovereignEntityDyn]
      have h := add_lt_add_left zero (predErrorSq st y) hPredPos st.outerObjective
      rw [add_zero] at h
      exact h
    have hSShapeN : st.shape < (runEntity sovereignEntityDyn st (y :: ys)).shape :=
      lt_of_lt_of_le hSShape1 (sovereign_shape_monotone stS1 ys)
    have hSSubN : st.subgoal < (runEntity sovereignEntityDyn st (y :: ys)).subgoal :=
      lt_of_lt_of_le hSSub1 (sovereign_subgoal_monotone stS1 ys)
    have hSObjN : st.outerObjective < (runEntity sovereignEntityDyn st (y :: ys)).outerObjective :=
      lt_of_lt_of_le hSObj1 (sovereign_outerObjective_monotone stS1 ys)
    have hRockEq : runEntity rockDyn st (y :: ys) = st := rock_state_invariant st (y :: ys)
    have hFrozEq : runEntity frozenAIDyn st (y :: ys) = st := frozenAI_state_invariant st (y :: ys)
    have hNeRP : runEntity rockDyn st (y :: ys) ≠ runEntity persistentMemoryAIDyn st (y :: ys) := by
      intro hEq
      have hSh := congrArg EntityState.shape hEq
      rw [hRockEq] at hSh
      exact ne_of_lt hPShapeN hSh
    have hNeRS : runEntity rockDyn st (y :: ys) ≠ runEntity sovereignEntityDyn st (y :: ys) := by
      intro hEq
      have hSh := congrArg EntityState.shape hEq
      rw [hRockEq] at hSh
      exact ne_of_lt hSShapeN hSh
    have hNeFP : runEntity frozenAIDyn st (y :: ys) ≠ runEntity persistentMemoryAIDyn st (y :: ys) := by
      intro hEq
      have hSh := congrArg EntityState.shape hEq
      rw [hFrozEq] at hSh
      exact ne_of_lt hPShapeN hSh
    have hNeFS : runEntity frozenAIDyn st (y :: ys) ≠ runEntity sovereignEntityDyn st (y :: ys) := by
      intro hEq
      have hSh := congrArg EntityState.shape hEq
      rw [hFrozEq] at hSh
      exact ne_of_lt hSShapeN hSh
    have hNePS : runEntity persistentMemoryAIDyn st (y :: ys) ≠ runEntity sovereignEntityDyn st (y :: ys) := by
      intro hEq
      have hObj := congrArg EntityState.outerObjective hEq
      rw [hPObjN] at hObj
      exact ne_of_lt hSObjN hObj
    exact ⟨⟨hPShapeN, hPSubN, hPObjN⟩, ⟨hSShapeN, hSSubN, hSObjN⟩, ⟨hNeRP, hNeRS, hNeFP, hNeFS, hNePS⟩⟩
  have hSixPairs :
      (rockDyn : DynamicalEntity F) ≠ frozenAIDyn ∧
      (rockDyn : DynamicalEntity F) ≠ persistentMemoryAIDyn ∧
      (rockDyn : DynamicalEntity F) ≠ sovereignEntityDyn ∧
      (frozenAIDyn : DynamicalEntity F) ≠ persistentMemoryAIDyn ∧
      (frozenAIDyn : DynamicalEntity F) ≠ sovereignEntityDyn ∧
      (persistentMemoryAIDyn : DynamicalEntity F) ≠ sovereignEntityDyn := by
    let stW : EntityState F := ⟨zero, zero, one⟩
    have hOneContrast : (one : F) ≠ stW.shape := Ne.symm zero_ne_one
    rcases hTrajContrastGen stW one [] hOneContrast with ⟨_, _, ⟨hT_RP, hT_RS, hT_FP, hT_FS, hT_PS⟩⟩
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
    · intro hEq
      have hAct := congrArg (fun sys => sys.stepAction ⟨st0.shape, zero, one⟩ zero) hEq
      exact hFrozenNeRockAct hAct.symm
    · intro hEq; exact hT_RP (congrArg (fun sys => runEntity sys stW [one]) hEq)
    · intro hEq; exact hT_RS (congrArg (fun sys => runEntity sys stW [one]) hEq)
    · intro hEq; exact hT_FP (congrArg (fun sys => runEntity sys stW [one]) hEq)
    · intro hEq; exact hT_FS (congrArg (fun sys => runEntity sys stW [one]) hEq)
    · intro hEq; exact hT_PS (congrArg (fun sys => runEntity sys stW [one]) hEq)
  exact ⟨⟨fun _ _ => rfl, hFrozenAct, hFrozenNeRockAct,
          rock_state_invariant st0 xs,
          frozenAI_state_invariant st0 xs,
          persistentAI_outerObjective_invariant st0 xs⟩,
         hTrajContrastGen st0 x xs,
         hSixPairs⟩

end DynamicalEntities

/-!
  ## Theorem 4.4 — Meta-Theorems: Consistency, Independence & Gravity Open Joint
  (*The Sovereign Mirror*, Ch. 1, Ch. 16 p. 117, Ch. 21 p. 153)
-/

/-- Concrete two-point locus `{locA, locB}` for instantiating partitioned physical media. -/
inductive TwoLoci where
  | locA
  | locB
  deriving DecidableEq, Repr

/-- Complete model bundle witnessing simultaneous satisfiability of TSR's axioms over `F`,
    with `physMedium` partitioned (`IsPartitionedMedium`), `nonphysMedium` over an undivided
    single locus (`∀ x y, x = y`), and `dimHom : PhysDim → NonphysRank` an explicit isomorphism. -/
structure TSRSystemModel (F : Type) [OrderedField F] where
  physMedium        : Medium F
  nonphysMedium     : Medium F
  phys_partitioned  : IsPartitionedMedium physMedium
  nonphys_undivided : ∀ x y : nonphysMedium.Locus, x = y
  physPerturb       : PerturbationMedium F
  nonphysPerturb    : PerturbationMedium F
  dimHom            : PhysDim → NonphysRank
  dimInv            : NonphysRank → PhysDim
  lightWitness      : RelativisticShell F
  hPhysRes          : Resistant physMedium ∧ Limited physMedium ∧ Radiating physMedium
  hNonphysRec       : Receptive nonphysMedium ∧ Limitless nonphysMedium ∧ Collecting nonphysMedium
  hPhysPerturb      : zero < physPerturb.rho ∧ zero < physPerturb.alpha ∧ physPerturb.alpha < one
  hNonphysPert      : nonphysPerturb.rho = zero ∧ nonphysPerturb.alpha = zero
  hDimHom           : IsMirrorRankHom dimHom ∧
                      (∀ u : PhysDim, dimInv (dimHom u) = u) ∧
                      (∀ v : NonphysRank, dimHom (dimInv v) = v) ∧
                      dimHom dimSpace = dimVibration ∧
                      dimHom dimTime = dimExpansion ∧
                      dimHom dimMass = dimMovement ∧
                      dimHom (dimVolume 3) = dimVibrance 3 ∧
                      dimHom (dimDensity 3) = dimDesire 3
  hLightSurface     : lightWitness.m = zero ∧
                      dsSquared lightWitness = zero ∧
                      lengthFactorSq lightWitness = zero ∧
                      zero < lightWitness.E ∧
                      zero < lightWitness.p ∧
                      lightWitness.v = lightWitness.c

def qHalf : QRat := QRat.mkRat 1 2 (by decide)

private theorem qrat_zero_lt_one_concrete : (zero : QRat) < (one : QRat) :=
  zero_lt_one

private theorem qrat_zero_lt_half : (zero : QRat) < qHalf := by
  change RawRat.ltProp RawRat.zero ⟨1, 2, _⟩
  unfold RawRat.ltProp RawRat.zero
  dsimp
  decide

private theorem qrat_half_lt_one : qHalf < (one : QRat) := by
  change RawRat.ltProp ⟨1, 2, _⟩ RawRat.one
  unfold RawRat.ltProp RawRat.one
  dsimp
  decide

/-- Constructive `QRat` Physical Medium (`ρ = 1, κ = 1`, discrete metric on `TwoLoci`). -/
def canonicalPhysMedium : Medium QRat where
  Locus := TwoLoci
  dist := fun x y => if x == y then zero else one
  dist_self := fun x => by cases x <;> rfl
  dist_nonneg := fun x y => by
    cases x <;> cases y
    · exact le_refl zero
    · exact le_of_lt zero_lt_one
    · exact le_of_lt zero_lt_one
    · exact le_refl zero
  rho := one
  rho_nonneg := le_of_lt zero_lt_one
  kappa := one
  kappa_pos := zero_lt_one

theorem canonicalPhysMedium_partitioned : IsPartitionedMedium canonicalPhysMedium := by
  refine ⟨⟨TwoLoci.locA, TwoLoci.locB, fun h => by cases h⟩, ?_⟩
  intro x y hne
  cases x <;> cases y
  · exact False.elim (hne rfl)
  · exact zero_lt_one
  · exact zero_lt_one
  · exact False.elim (hne rfl)

/-- Constructive `QRat` Nonphysical Medium (`ρ = 0, κ = 1`, undivided single locus `Unit`),
    matching TSR's undivided nonphysical ontology (`[x0]` in Thm 1.4b and `Unit` in Thm 4.4b). -/
def canonicalNonphysMedium : Medium QRat where
  Locus := Unit
  dist := fun _ _ => zero
  dist_self := fun _ => rfl
  dist_nonneg := fun _ _ => le_refl zero
  rho := zero
  rho_nonneg := le_refl zero
  kappa := one
  kappa_pos := zero_lt_one

/-- Constructive `QRat` Physical Perturbation Medium (`ρ = 1, α = 1/2`). -/
def canonicalPhysPerturb : PerturbationMedium QRat where
  rho := one
  rho_nonneg := le_of_lt zero_lt_one
  alpha := qHalf
  alpha_zero_iff := by
    constructor
    · intro h
      have hpos := qrat_zero_lt_half
      rw [h] at hpos
      exact False.elim (lt_irrefl zero hpos)
    · intro h
      exact False.elim (zero_ne_one h.symm)
  alpha_bounds_of_pos := fun _ => ⟨qrat_zero_lt_half, qrat_half_lt_one⟩

/-- Constructive `QRat` Nonphysical Perturbation Medium (`ρ = 0, α = 0`). -/
def canonicalNonphysPerturb : PerturbationMedium QRat where
  rho := zero
  rho_nonneg := le_refl zero
  alpha := zero
  alpha_zero_iff := Iff.rfl
  alpha_bounds_of_pos := fun h => False.elim (lt_irrefl zero h)

/-- Constructive `QRat` Light-Surface Witness (`c = 1, E = 1, p = 1, m = 0, v = 1, dt = 1, dx = 1`). -/
def canonicalLightWitness : RelativisticShell QRat where
  c  := one
  E  := one
  p  := one
  m  := zero
  v  := one
  dt := one
  dx := one
  c_pos    := zero_lt_one
  E_pos    := zero_lt_one
  p_nonneg := le_of_lt zero_lt_one
  m_nonneg := le_refl zero
  dt_pos   := zero_lt_one
  shell_eq := by
    rw [one_mul, one_mul, sub_self, zero_mul, zero_mul]
  vel_eq := by
    rw [one_mul, one_mul]
  disp_eq := by
    rw [one_mul]

/-- **Theorem 4.4a (Consistency of `Σ_TSR`)**:
    `TSRSystemModel QRat` is constructively inhabited; therefore TSR's structural axioms
    are mutually consistent (`Σ_TSR ⊬ ⊥`). -/
def canonicalTSRModel : TSRSystemModel QRat where
  physMedium        := canonicalPhysMedium
  nonphysMedium     := canonicalNonphysMedium
  phys_partitioned  := canonicalPhysMedium_partitioned
  nonphys_undivided := fun x y => by cases x; cases y; rfl
  physPerturb       := canonicalPhysPerturb
  nonphysPerturb    := canonicalNonphysPerturb
  dimHom            := canonicalMirrorRankHom
  dimInv            := canonicalMirrorRankInv
  lightWitness      := canonicalLightWitness
  hPhysRes := by
    have hRes : Resistant canonicalPhysMedium := zero_lt_one
    rcases condition_triad_equivalence canonicalPhysMedium canonicalPhysMedium_partitioned with
      ⟨hRL, _, hRR⟩
    exact ⟨hRes, hRL.mp hRes, hRR.mp hRes⟩
  hNonphysRec := by
    have hRec : Receptive canonicalNonphysMedium := rfl
    rcases (receptive_triad_equivalence canonicalNonphysMedium).1 hRec with ⟨_, _, hLim, hCol⟩
    exact ⟨hRec, hLim, hCol⟩
  hPhysPerturb := ⟨zero_lt_one, qrat_zero_lt_half, qrat_half_lt_one⟩
  hNonphysPert := ⟨rfl, rfl⟩
  hDimHom := by
    rcases canonicalMirrorRankHom_isomorphism with ⟨hHom, _, hLeftInv, hRightInv, _, _⟩
    rcases elimination_theorem_desire_vibrance canonicalMirrorRankHom hHom rfl rfl 3 (by decide) with
      ⟨hVol, hDen, _, _, _, _⟩
    exact ⟨hHom, hLeftInv, hRightInv, rfl, rfl, rfl, hVol, hDen⟩
  hLightSurface := by
    rcases light_surface_of_mirror canonicalLightWitness with ⟨_, _, hAtZero⟩
    rcases hAtZero rfl with ⟨hds, hlen, hE, hp, hv, _⟩
    exact ⟨rfl, hds, hlen, hE, hp, hv⟩

theorem tsr_axioms_consistent : Nonempty (TSRSystemModel QRat) :=
  ⟨canonicalTSRModel⟩

/-!
  ### Theorem 4.4b — Model-Theoretic Independence of Both Halves of the First Partition
  Rather than assuming an external `partition_law`, we define pairwise resistant contrast
  mechanistically as `ρ * (state(x) - state(y))²` and prove purely from field algebra +
  three explicit `QRat` countermodels that BOTH `|Locus| ≥ 2` AND `ρ > 0` are independently
  necessary for non-zero contrast expansion.
-/

structure ContrastUniverse (F : Type) [OrderedField F] where
  Locus : Type
  rho   : F
  state : Locus → F

def pairwiseContrast {F : Type} [OrderedField F]
    (u : ContrastUniverse F) (x y : u.Locus) : F :=
  u.rho * ((u.state x - u.state y) * (u.state x - u.state y))

/-- Countermodel 1: Positive resistance (`ρ = 1`), but undivided single locus (`Unit`). -/
def undividedSingleLocusWorld : ContrastUniverse QRat where
  Locus := Unit
  rho   := one
  state := fun _ => one

/-- Countermodel 2: Partitioned distinct loci (`TwoLoci`, distinct states), but `ρ = 0`. -/
def unresistedMultiLocusWorld : ContrastUniverse QRat where
  Locus := TwoLoci
  rho   := zero
  state := fun x => match x with | .locA => one | .locB => zero

/-- Witness Model 3: Both distinct loci (`TwoLoci`) AND positive resistance (`ρ = 1`). -/
def partitionedContrastWorld : ContrastUniverse QRat where
  Locus := TwoLoci
  rho   := one
  state := fun x => match x with | .locA => one | .locB => zero

/-- **Theorem 4.4b (Double Model-Theoretic Independence of the First Partition)**:
    1. In any undivided universe (`∀ x y, x = y`), `pairwiseContrast u x y = 0` identically
       (even when `ρ > 0`, witnessed by `undividedSingleLocusWorld`).
    2. In any zero-resistance universe (`ρ = 0`), `pairwiseContrast u x y = 0` identically
       (even when `∃ x ≠ y` with distinct states, witnessed by `unresistedMultiLocusWorld`).
    3. When BOTH multiplicity and resistance hold (`partitionedContrastWorld`),
       `0 < pairwiseContrast partitionedContrastWorld .locA .locB`. -/
theorem independence_of_first_partition :
    (∀ F : Type, ∀ [OrderedField F], ∀ u : ContrastUniverse F,
      (∀ x y : u.Locus, x = y) → ∀ x y : u.Locus, pairwiseContrast u x y = zero) ∧
    (∀ F : Type, ∀ [OrderedField F], ∀ u : ContrastUniverse F,
      u.rho = zero → ∀ x y : u.Locus, pairwiseContrast u x y = zero) ∧
    (∀ x y : Unit, pairwiseContrast undividedSingleLocusWorld x y = zero) ∧
    (∀ x y : TwoLoci, pairwiseContrast unresistedMultiLocusWorld x y = zero) ∧
    (zero : QRat) < pairwiseContrast partitionedContrastWorld .locA .locB := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro F _ u hSub x y
    unfold pairwiseContrast
    rw [hSub x y, sub_self, zero_mul, mul_zero]
  · intro F _ u hRho x y
    unfold pairwiseContrast
    rw [hRho, zero_mul]
  · intro x y
    unfold pairwiseContrast undividedSingleLocusWorld
    dsimp
    rw [sub_self, zero_mul, mul_zero]
  · intro x y
    unfold pairwiseContrast unresistedMultiLocusWorld
    dsimp
    rw [zero_mul]
  · unfold pairwiseContrast partitionedContrastWorld
    dsimp
    rw [sub_def, neg_zero, add_zero, one_mul, one_mul]
    exact zero_lt_one

/-!
  ### Theorem 4.4c — The Gravity Open-Joint Theorem: Two-Region vs. Three-Region Shared-`E`
  (*The Sovereign Mirror*, Ch. 16, p. 117 & `vocab/mirror.py`, lines 56–61)

  Evaluates the **single** mechanical AST barrier counter `countActiveBarriers` and
  reading functor `R_readArch` across `.twoRegionNoSharedE` vs. `.threeRegionSharedE`
  with **zero** hardcoded numeric barrier overrides:
    - Under `.twoRegionNoSharedE`, `energyAttractionHome` places `E` / `Attraction` in
      resistant `.physical`, so `countActiveBarriers` evaluates `.SharedCenterCurvature`
      on `row11GravityWarp` and `row12GravityLensing` to `1`, yielding `.Invert` (`15/17`).
    - Under `.threeRegionSharedE`, `energyAttractionHome` places `E` / `Attraction` in
      zero-resistance `.sharedOverlap`, so `countActiveBarriers` evaluates the identical
      `LawAST` to `0`, yielding `.Keep` (`17/17`).
-/

def nonGravityRows15 : List BenchmarkRow :=
  benchmarkRows17.filter (fun r => r.id != 11 && r.id != 12)

/-- **Theorem 4.4c (Two-Region vs. Three-Region Shared-`E` Gravity Theorem via `countActiveBarriers`)**:
    Under the single mechanical AST evaluator `countActiveBarriers` and `R_readArch`:
      1. There are 15 non-gravity benchmark rows, and all 15 evaluate identically across both
         architectures and match the book rulings (`15/15`).
      2. Under `.twoRegionNoSharedE`, `energyAttractionHome = .physical` (`regionResistant = true`),
         so `countActiveBarriers` computes `1` barrier on Rows 11–12 and `R_readArch` yields `.Invert` (`15/17`).
      3. Under `.threeRegionSharedE`, `energyAttractionHome = .sharedOverlap` (`regionResistant = false`),
         so `countActiveBarriers` computes `0` barriers on Rows 11–12 and `R_readArch` yields `.Keep` (`17/17`). -/
theorem gravity_open_joint_two_vs_three_regions :
    nonGravityRows15.length = 15 ∧
    nonGravityRows15.all (fun r =>
      R_readArch .twoRegionNoSharedE r == R_readArch .threeRegionSharedE r &&
      R_readArch .threeRegionSharedE r == r.bookRuling) = true ∧
    (energyAttractionHome .twoRegionNoSharedE = .physical ∧
     countActiveBarriers .twoRegionNoSharedE row11GravityWarp.lawAST = 1 ∧
     countActiveBarriers .twoRegionNoSharedE row12GravityLensing.lawAST = 1 ∧
     R_readArch .twoRegionNoSharedE row11GravityWarp = .Invert ∧
     R_readArch .twoRegionNoSharedE row12GravityLensing = .Invert) ∧
    (energyAttractionHome .threeRegionSharedE = .sharedOverlap ∧
     countActiveBarriers .threeRegionSharedE row11GravityWarp.lawAST = 0 ∧
     countActiveBarriers .threeRegionSharedE row12GravityLensing.lawAST = 0 ∧
     R_readArch .threeRegionSharedE row11GravityWarp = .Keep ∧
     R_readArch .threeRegionSharedE row12GravityLensing = .Keep) ∧
    (benchmarkRows17.filter (fun r => R_readArch .twoRegionNoSharedE r == r.bookRuling)).length = 15 ∧
    benchmarkRows17.all (fun r => R_readArch .threeRegionSharedE r == r.bookRuling) = true := by
  decide

end TSR
