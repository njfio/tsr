/-
  TSR/EntityAndMeta.lean
  ======================
  Part I, Section 4 — Formalization Notes & Theorems for Selected Claims
  (*The Sovereign Mirror* v57):
    - Theorem 4.1: Multiplicative Gate Characterization (`Tune` & `Focus`, SM v57 Ch. 17, pp. 128–129)
    - Theorem 4.2: Four-Way Separation Over a Modeled State System (`Rock`, `FrozenWeightAI`,
                   `PersistentMemoryObjectiveAI`, `SovereignEntity`, SM v57 Ch. 18, pp. 137–141)
    - Proposition 4.3: Coupled Two-Entity Load Transfer & False-Positive Local Ease
                       (SM v57 Ch. 8, p. 61 & Ch. 13, p. 94)
    - Theorem 4.4: Meta-Theorems — Constructive `QRat` Witness Model for Formalized Predicates,
                   Independence in a Pairwise-Contrast Toy Model (`v57` Ch. 21, p. 153), and
                   Benchmark Evaluation Across Two vs. Three Modeled Regions (`v57` Ch. 16, p. 117)

  Epistemic tags in docstrings:
    (a) Deductive consequence of the definitions in this repository.
    (b) Standard ordered-field algebra / arithmetic.
    (c) Formalization or modeling choice not uniquely determined by (or absent from) the book prose.
-/

import TSR.OrderedAlgebra
import TSR.Condition
import TSR.MirrorFunctor
import TSR.Crossing

namespace TSR
open OrderedField

/-!
  ## Theorem 4.1 — Multiplicative Gate Characterization (`Tune` & `Focus`)
  (*The Sovereign Mirror* v57, Ch. 17, pp. 128–129)
-/

section GatesAndCoupledEntities
variable {F : Type} [OrderedField F]

def gateMul (u x : F) : F := u * x
def gateAdd (a b u x : F) : F := a * u + b * x

/-- `(c)` Specification capturing *SM* v57 Ch. 17, pp. 128–129's two-factor constraint
    (`"In a product, neither factor does anything alone... if either factor is zero, the whole thing
    is zero"`): vanishes when either factor is zero, strictly positive when both are positive. -/
def IsZeroAnnihilatingGate (G : F → F → F) : Prop :=
  (∀ x : F, G zero x = zero) ∧
  (∀ u : F, G u zero = zero) ∧
  (∀ u x : F, zero < u → zero < x → zero < G u x)

/-- **Lemma 4.1 (Multiplicative Gate Necessity vs. Positively Weighted Additive Sums)**
    Classifications: **(c)** contrasting `u * x` against positively weighted linear combinations
    `a * u + b * x` (`a, b > 0`) as formal gate candidates; **(a)**/**(b)** ordered-field proof.
      1. `gateMul u x = u * x` satisfies `IsZeroAnnihilatingGate`.
      2. Every positively weighted additive sum `gateAdd a b u x = a * u + b * x` (`a, b > 0`)
         violates `IsZeroAnnihilatingGate`: `gateAdd a b 0 x > 0` for `x > 0` and
         `gateAdd a b u 0 > 0` for `u > 0`. -/
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
  (*The Sovereign Mirror* v57, Ch. 8, p. 61 & Ch. 13, p. 94)
-/

/-- `(c)` Minimal two-entity accounting model encoding *SM* v57 Ch. 8 p. 61 & Ch. 13 p. 94
    ("a path feels easy because somebody else is carrying the hard part" / Newton's 3rd Law):
    `return21 = offload12` enforces action-reaction balance between entities `1` and `2`. -/
structure CoupledExchange (F : Type) [OrderedField F] where
  R1              : F -- Entity 1 initial internal resistance
  R2              : F -- Entity 2 initial internal resistance
  offload12       : F -- Load transferred from Entity 1 onto Entity 2
  return21        : F -- Empirical return load received by Entity 2
  R1_nonneg       : zero ≤ R1
  R2_nonneg       : zero ≤ R2
  offload_nonneg  : zero ≤ offload12
  offload_le_R1   : offload12 ≤ R1
  action_reaction : return21 = offload12

def R1After (ex : CoupledExchange F) : F := ex.R1 - ex.offload12
def R2After (ex : CoupledExchange F) : F := ex.R2 + ex.return21

/-- **Proposition 4.3 (Conservation of Transferred Load & Local Ease Under Externalization)**
    Classifications: **(c)** scalar two-entity balance model `CoupledExchange`; **(b)**/**(a)**
    ordered-field arithmetic consequences.
      1. Post-exchange resistances remain non-negative (`0 ≤ R1After` and `0 ≤ R2After`).
      2. Total load is conserved: `R1After + R2After = R1 + R2`.
      3. When Entity 1 offloads all positive resistance (`R1 > 0`, `offload12 = R1`),
         Entity 1's local term becomes `R1After = 0`, while Entity 2's rises (`R2 < R2After`)
         and `0 < return21`. -/
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
  ## Theorem 4.2 — Four-Way Separation in a Toy State-Update Model of Entity Classes
  (*The Sovereign Mirror* v57, Ch. 18, pp. 137–141)

  **Modeling Disclosure (`(c)`):** *The Sovereign Mirror* v57 characterizes rocks, locked-state AIs,
  persistent-memory AIs, and sovereign entities qualitatively (`Ch. 18, pp. 137–141`). The concrete
  3-component record `EntityState F` (`shape`, `subgoal`, `outerObjective`) and the four explicit
  discrete update rules below—including the squared-error increments `(x - st.shape)²` (`predErrorSq`)
  and `(x - st.subgoal)²` (`subgoalErrorSq`)—are **`(c)` toy modeling choices NOT present in the book**,
  chosen to isolate the qualitative distinctions in a minimal algebraic setting:
    1. `rockDyn`: zero feedback action; invariant state across `xs`.
    2. `frozenAIDyn`: nonzero feedback action `(outerObjective + subgoal) - x`; invariant state across `xs`.
    3. `persistentMemoryAIDyn`: `(c)` updates `shape` and `subgoal` via squared errors, while
       `outerObjective` stays invariant across `xs` (modeling an externally fixed objective).
    4. `sovereignEntityDyn`: `(c)` updates `shape`, `subgoal`, and `outerObjective` from contrast
       `predErrorSq`, yielding **(a)** deductive trajectory separations over **(b)** `OrderedField F`.
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

/-- `(c)` Toy 3-component dynamical entity state separating instrumental `subgoal` from `outerObjective`. -/
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

/-- `(c)` Modeled squared prediction error `(x - shape)²` (not in *The Sovereign Mirror* v57). -/
def predErrorSq (st : EntityState F) (x : F) : F :=
  (x - st.shape) * (x - st.shape)

/-- `(c)` Modeled squared subgoal error `(x - subgoal)²` (not in *The Sovereign Mirror* v57). -/
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

/-- **Theorem 4.2 (Trajectory-Level & 6-Way Separation in the Modeled Entity System)**
    Classifications: **(c)** toy squared-error update rules (`predErrorSq`, `subgoalErrorSq`,
    `rockDyn`, `frozenAIDyn`, `persistentMemoryAIDyn`, `sovereignEntityDyn`, not in *SM* v57);
    **(a)**/**(b)** ordered-field consequences over any `OrderedField F` and stream `xs : List F`:
      1. `rockDyn` emits identically zero action, whereas `frozenAIDyn` emits non-zero action
         (`stepAction ⟨st0.shape, 0, 1⟩ 0 = 1 ≠ 0`), while both keep `EntityState` invariant across `xs`.
      2. Under `x ≠ st0.shape`, `persistentMemoryAIDyn` strictly increases `shape` and `subgoal`
         while `outerObjective` remains invariant (`= st0.outerObjective`) across all `xs`.
      3. Under `x ≠ st0.shape`, `sovereignEntityDyn` strictly increases `shape`, `subgoal`,
         and `outerObjective` across all `xs`.
      4. All $\binom{4}{2} = 6$ pairs among `{rockDyn, frozenAIDyn, persistentMemoryAIDyn, sovereignEntityDyn}`
         are explicitly separated. -/
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
  ## Theorem 4.4 — Meta-Theorems: Model Consistency, Toy Contrast Independence & Gravity Benchmark
  (*The Sovereign Mirror* v57, Ch. 1, Ch. 16 pp. 117–118, Ch. 21 p. 153)
-/

/-- Concrete two-point locus `{locA, locB}` for instantiating partitioned physical media. -/
inductive TwoLoci where
  | locA
  | locB
  deriving DecidableEq, Repr

/-- `(c)` Model bundle witnessing simultaneous satisfiability of the formalized structural
    predicates in `TSR.Condition`, `TSR.MirrorFunctor`, and `TSR.Crossing` over `OrderedField F`:
    `physMedium` partitioned (`IsPartitionedMedium`), `nonphysMedium` undivided (`∀ x y, x = y`),
    and `dimHom : PhysDim → NonphysRank` a multiplicative rank isomorphism. -/
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

/-- **Theorem 4.4a (Relative Consistency of the Formalized Predicate Bundle over `QRat`)**
    Classifications: **(a)** explicit construction witnessing **(c)** that the formalized predicates
    in `TSRSystemModel QRat` are mutually satisfiable (no empirical or metaphysical truth beyond
    the chosen mathematical structure is claimed). -/
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

/-- Witness theorem confirming `Nonempty (TSRSystemModel QRat)` via `canonicalTSRModel`
    (**(a)** consequence of constructive inhabitant for the **(c)** predicate bundle). -/
theorem tsr_axioms_consistent : Nonempty (TSRSystemModel QRat) :=
  ⟨canonicalTSRModel⟩

/-!
  ### Theorem 4.4b — Toy-Model Independence of Both Conditions for Pairwise Contrast
  (*The Sovereign Mirror* v57, Ch. 21, p. 153: `"the first partition is the one move in the book
  my own rule can't produce. It isn't a result. It's the axiom"`)

  **Modeling Disclosure (`(c)`):** Defining pairwise contrast as `ρ * (state(x) - state(y))²`
  (`pairwiseContrast`) inside `ContrastUniverse F` is a **`(c)` toy quadratic formula NOT in the
  book**. Given that formula, **(a)**/**(b)** ordered-field algebra and three `QRat` witness models
  show that neither multiplicity (`|Locus| ≥ 2`) nor positive resistance (`ρ > 0`) alone yields
  non-zero `pairwiseContrast`.
-/

/-- `(c)` Toy contrast universe pairing a locus type, scalar resistance `rho`, and scalar `state`. -/
structure ContrastUniverse (F : Type) [OrderedField F] where
  Locus : Type
  rho   : F
  state : Locus → F

/-- `(c)` Modeled squared pairwise contrast `ρ * (state(x) - state(y))²` (not in *SM* v57). -/
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

/-- **Theorem 4.4b (Double Model-Theoretic Independence in the Pairwise-Contrast Toy Model)**
    Classifications: **(c)** quadratic `pairwiseContrast` model (not in *SM* v57); **(a)**/**(b)**
    field-algebraic proof and explicit `QRat` countermodels.
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
  ### Theorem 4.4c — Modeled Gravity Rulings Across Two- vs. Three-Part Mirror Architectures
  (*The Sovereign Mirror* v57, Ch. 16, p. 117 & `vocab/mirror.py`, lines 56–61)

  **Terminology Disclosure (`(c)`):** `"two-region"`, `"three-region"`, `"open-joint"`, and
  `"barrier"` (`countActiveBarriers`, `.twoRegionNoSharedE`, `.threeRegionSharedE`) are `(c)`
  formalization labels (not book terminology). They formalize *SM* v57 Ch. 16, p. 117:
  `"Given a mirror with only two sides, they turned it over. TSR has three: the two sides and
  the continuum where they meet, with one energy in it."`

  Evaluates the AST evaluator `countActiveBarriers` and `R_readArch` across `.twoRegionNoSharedE`
  vs. `.threeRegionSharedE` (`LawAST` representations of `benchmarkRows17`; note Row 17 uses `(c)`
  `IsothermalEquilibriumBalance` here, whereas *SM* v57 p. 118 uses walls/two-sides-touching):
    - Under `.twoRegionNoSharedE`, `energyAttractionHome` places `E` / `Attraction` in
      resistant `.physical`, so `countActiveBarriers` evaluates `.SharedCenterCurvature`
      on `row11GravityWarp` and `row12GravityLensing` to `1`, yielding `.Invert` (`15/17`).
    - Under `.threeRegionSharedE`, `energyAttractionHome` places `E` / `Attraction` in
      zero-resistance `.sharedOverlap`, so `countActiveBarriers` evaluates the identical
      `LawAST` to `0`, yielding `.Keep` (`17/17`).
-/

def nonGravityRows15 : List BenchmarkRow :=
  benchmarkRows17.filter (fun r => r.id != 11 && r.id != 12)

/-- **Theorem 4.4c (Modeled Benchmark Agreement Across `.twoRegionNoSharedE` vs. `.threeRegionSharedE`)**
    Classifications: **(a)** finite `decide` evaluation over **(c)** AST/architecture encoding
    (`countActiveBarriers`, `R_readArch`, `LawAST`, `benchmarkRows17`):
      1. The 15 non-gravity benchmark rows evaluate identically across both architectures and match
         `bookRuling` (`15/15`).
      2. Under `.twoRegionNoSharedE`, `energyAttractionHome = .physical` (`regionResistant = true`),
         so `countActiveBarriers` computes `1` on Rows 11–12 and `R_readArch` yields `.Invert` (`15/17`).
      3. Under `.threeRegionSharedE`, `energyAttractionHome = .sharedOverlap` (`regionResistant = false`),
         so `countActiveBarriers` computes `0` on Rows 11–12 and `R_readArch` yields `.Keep` (`17/17`). -/
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
