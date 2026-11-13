/-
  TSR/Crossing.lean
  =================
  Part I, Section 3 — Lean 4 formalization of crossing symmetry, contrast-filter, and
  escape-walk models from *The Sovereign Mirror* (v57):
    - Theorem 3.1: Klein Four-Group `V_4` & Derived Diagonal Symmetry from the
                   Irreversible-Pole Assignment (SM v57 Ch. 10, pp. 78–79 & *The Map*, pp. 172–173)
    - Theorem 3.2: Resistance Contrast Filter, `Shape` vs. `HoldingOn`, and
                   Self-Refutation of Wanting Non-Wanting (SM v57 Ch. 10, pp. 69–75; Ch. 8, pp. 59–60)
    - Theorem 3.3: Confinement Scaling vs. Unique Weak-Diagonal Escape Path
                   (SM v57 Ch. 10, pp. 76–79 & Ch. 12, pp. 86–90)

  Epistemic status: explicit finite-group, linear-step, and directed-graph definitions (`Quad`,
  `poleStrength`, `V4Op`, `ContrastPair`, `FallingManState`, `confinementStep`, `canStep`) are `(c)`
  modeling choices; all theorems here are `(a)` deductive consequences (with `(b)` field algebra
  and Newton's force balance in `self_refutation_of_wanting_nonwanting`).
-/

import TSR.OrderedAlgebra
import TSR.MirrorFunctor

namespace TSR
open OrderedField

/-!
  ## Theorem 3.1 — Klein Four-Group `V_4` & Derived Diagonal Symmetry
  (*The Sovereign Mirror* v57, Ch. 10, pp. 78–79; *The Map*, pp. 172–173)

  Modeling choice `(c)`: `Quad := Side × FlowDir`, `poleStrength`, `V4Op`, `mulV4`, and `actV4`
  encode the four crossing corners and the two symmetries described on *The Map*, pp. 172–173.
  The group laws (`v4_group_and_action`) and uniqueness of `.diag` (`derived_diagonal_symmetry`)
  are `(a)` deductive consequences of these definitions.
-/

inductive Side where
  | P
  | NP
  deriving DecidableEq, Repr

inductive FlowDir where
  | Out
  | In
  deriving DecidableEq, Repr

/-- The four crossing quadrants of *The Present*. -/
abbrev Quad := Side × FlowDir

def qDesire      : Quad := (.NP, .Out) -- Out For / Desire / Future (Strong Frequency)
def qIntuition   : Quad := (.NP, .In)  -- In To / Intuition / Current (Weak Frequency)
def qBelief      : Quad := (.P,  .Out) -- Out Through / Belief / Now (Weak Force)
def qExpectation : Quad := (.P,  .In)  -- In From / Expectation / Past (Strong Force)

inductive Strength where
  | Strong
  | Weak
  deriving DecidableEq, Repr

def flipSide : Side → Side
  | .P  => .NP
  | .NP => .P

def flipDir : FlowDir → FlowDir
  | .Out => .In
  | .In  => .Out

def flipStrength : Strength → Strength
  | .Strong => .Weak
  | .Weak   => .Strong

/-- **Irreversible-Pole Assignment (`(c)` formalization of *SM* v57 Ch. 10, pp. 78–79)**:
    - On the Resistant side (`.P`), what has arrived (`.In`, `Past`) holds the mark (`.Strong`)
      while what goes out now (`.Out`, `Now`) is shiftable (`.Weak`).
    - On the Receptive side (`.NP`), what is launched (`.Out`, `Future` / `Desire`) irreversibly
      expands the front edge (`.Strong`) while what returns (`.In`, `Intuition`) offers without forcing (`.Weak`). -/
def poleStrength : Quad → Strength
  | (.P,  .In)  => .Strong
  | (.P,  .Out) => .Weak
  | (.NP, .Out) => .Strong
  | (.NP, .In)  => .Weak

/-- Elements of the Klein four-group `V_4 ≅ ℤ_2 × ℤ_2` acting on `Quad`. -/
inductive V4Op where
  | idOp
  | horiz
  | vert
  | diag
  deriving DecidableEq, Repr

def mulV4 : V4Op → V4Op → V4Op
  | .idOp,  g      => g
  | g,      .idOp  => g
  | .horiz, .horiz => .idOp
  | .vert,  .vert  => .idOp
  | .diag,  .diag  => .idOp
  | .horiz, .vert  => .diag
  | .vert,  .horiz => .diag
  | .horiz, .diag  => .vert
  | .diag,  .horiz => .vert
  | .vert,  .diag  => .horiz
  | .diag,  .vert  => .horiz

def actV4 : V4Op → Quad → Quad
  | .idOp,  (s, d) => (s, d)
  | .horiz, (s, d) => (flipSide s, d)
  | .vert,  (s, d) => (s, flipDir d)
  | .diag,  (s, d) => (flipSide s, flipDir d)

/-- **Theorem 3.1a (`V_4` Group Laws & Faithful Action)**:
    `V4Op` forms an abelian group of exponent 2 (`g * g = idOp`) with `horiz * vert = diag`,
    acting faithfully on the four quadrants of *The Present*. -/
theorem v4_group_and_action :
    (∀ a b c : V4Op, mulV4 (mulV4 a b) c = mulV4 a (mulV4 b c)) ∧
    (∀ a b : V4Op, mulV4 a b = mulV4 b a) ∧
    (∀ a : V4Op, mulV4 a a = .idOp) ∧
    (mulV4 .horiz .vert = .diag) ∧
    (∀ a b : V4Op, ∀ q : Quad, actV4 (mulV4 a b) q = actV4 a (actV4 b q)) := by
  refine ⟨?_, ?_, ?_, rfl, ?_⟩
  · intro a b c; cases a <;> cases b <;> cases c <;> rfl
  · intro a b; cases a <;> cases b <;> rfl
  · intro a; cases a <;> rfl
  · intro a b q
    rcases q with ⟨s, d⟩
    cases a <;> cases b <;> cases s <;> cases d <;> rfl

/-- **Theorem 3.1b (Derived Diagonal Symmetry & Strong-vs-Weak Horizontal Crossing)**:
    From the single `poleStrength` axiom alone:
      1. Horizontal reflection `.horiz` preserves flow direction (`Out ↔ Out`, `In ↔ In`).
      2. Central point-inversion `.diag` preserves binding strength (`Expectation ↔ Desire` Strong;
         `Belief ↔ Intuition` Weak), and is the **unique** side-swapping operator in `V_4` that does so.
      3. Every horizontal crossing `.horiz` necessarily pits `Strong` against `Weak`. -/
theorem derived_diagonal_symmetry :
    (∀ q : Quad, (actV4 .horiz q).2 = q.2) ∧
    (∀ q : Quad, poleStrength (actV4 .diag q) = poleStrength q) ∧
    (∀ g : V4Op,
      ((∀ q : Quad, (actV4 g q).1 = flipSide q.1) ∧
       (∀ q : Quad, poleStrength (actV4 g q) = poleStrength q)) ↔ g = .diag) ∧
    (∀ q : Quad, poleStrength (actV4 .horiz q) = flipStrength (poleStrength q)) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro q; rcases q with ⟨s, d⟩; rfl
  · intro q; rcases q with ⟨s, d⟩; cases s <;> cases d <;> rfl
  · intro g
    constructor
    · rintro ⟨hSide, hStr⟩
      cases g with
      | idOp =>
        have h := hSide (.P, .Out)
        cases h
      | horiz =>
        have h := hStr (.P, .In)
        cases h
      | vert =>
        have h := hSide (.P, .Out)
        cases h
      | diag => rfl
    · intro hg
      rw [hg]
      exact ⟨fun q => by rcases q with ⟨s, d⟩; rfl,
             fun q => by rcases q with ⟨s, d⟩; cases s <;> cases d <;> rfl⟩
  · intro q; rcases q with ⟨s, d⟩; cases s <;> cases d <;> rfl

/-!
  ## Theorem 3.2 — Resistance Contrast Filter & Buddhist Resolution
  (*The Sovereign Mirror* v57, Ch. 10, pp. 69–75; Ch. 8, pp. 59–60)

  Modeling choice `(c)`: `ContrastPair`, `projectNP (w, h) := (w, 0)`, `stepTopCrossing`,
  `stepBottomRefusal`, `IsShape`, `IsHoldingOn`, and `FallingManState` are algebraic models
  encoding the filter asymmetry and `tanha`/`chanda`/`upadana` distinction in Ch. 10, pp. 69–75.
-/

section ContrastFilterAndBuddhism
variable {F : Type} [OrderedField F]

/-- Lived physical contrast state `(wanting, holdingOn)`. -/
abbrev ContrastPair (F : Type) := F × F

/-- Nonphysical projection `Π_NP(w, h) = (w, 0)`: resistance cannot cross into a `ρ = 0` medium. -/
def projectNP (p : ContrastPair F) : ContrastPair F := (p.1, zero)

def stepTopCrossing (C_edge wanting : F) : F := C_edge + wanting

def stepBottomRefusal (C_edge newContrast : F) : F := C_edge + newContrast

structure ExpectationContext (F : Type) [OrderedField F] where
  expectation    : F
  opposingDesire : F

/-- `Shape`: physical expectation with nothing wanted against it (`opposingDesire = 0`). -/
def IsShape (ctx : ExpectationContext F) : Prop :=
  zero < ctx.expectation ∧ ctx.opposingDesire = zero

/-- `HoldingOn`: physical expectation with an active desire pushing against it (`opposingDesire > 0`). -/
def IsHoldingOn (ctx : ExpectationContext F) : Prop :=
  zero < ctx.expectation ∧ zero < ctx.opposingDesire

/-- **Theorem 3.2a (Contrast Filter Idempotence, Unconditional Top Expansion & Non-Shrinking Refusal)**:
    1. `projectNP` is idempotent and strips `holdingOn` to `0`.
    2. Every `wanting > 0` strictly expands `C_edge` at the top crossing.
    3. Refusal at the bottom crossing (`newContrast ≥ 0`) never shrinks `C_edge`.
    4. `IsShape` and `IsHoldingOn` are mutually exclusive relational modes of `Expectation > 0`. -/
theorem resistance_contrast_filter_properties
    (p : ContrastPair F) (C_edge wanting newContrast : F)
    (hWantPos : zero < wanting) (hNewNonneg : zero ≤ newContrast)
    (ctx : ExpectationContext F) :
    projectNP (projectNP p) = projectNP p ∧
    (projectNP p).2 = zero ∧
    C_edge < stepTopCrossing C_edge wanting ∧
    C_edge ≤ stepBottomRefusal C_edge newContrast ∧
    ¬ (IsShape ctx ∧ IsHoldingOn ctx) := by
  have hTop : C_edge < stepTopCrossing C_edge wanting := by
    unfold stepTopCrossing
    have hlt := add_lt_add_left zero wanting hWantPos C_edge
    rw [add_zero] at hlt
    exact hlt
  have hBot : C_edge ≤ stepBottomRefusal C_edge newContrast := by
    unfold stepBottomRefusal
    have hle := add_le_add (le_refl C_edge) hNewNonneg
    rw [add_zero] at hle
    exact hle
  have hDisj : ¬ (IsShape ctx ∧ IsHoldingOn ctx) := by
    rintro ⟨⟨_, hZero⟩, ⟨_, hPos⟩⟩
    rw [hZero] at hPos
    exact lt_irrefl zero hPos
  exact ⟨rfl, rfl, hTop, hBot, hDisj⟩

/-- Physical-nonphysical state model (`(c)` modeling choice) under gravitational pull `pull_g`
    and support reaction `support_N`, governed by Newton's multiplicative force balance
    `mass_m * accel = mass_m * pull_g - support_N` (`(b)` standard mechanics). -/
structure FallingManState (F : Type) [OrderedField F] where
  otherDesire    : F
  wantCessation  : F
  wanting        : F
  shape          : F
  vibrance       : F
  mass_m         : F
  pull_g         : F
  support_N      : F
  accel          : F
  newton_balance : mass_m * accel = mass_m * pull_g - support_N

/-- **Proposition 3.2b (Self-Refutation of Wanting Non-Wanting vs. Dropping `HoldingOn`)**:
    1. Any attempt to extinguish desire by *wanting* its cessation (`0 < s.wantCessation`)
       forces total `Desire = s.otherDesire + s.wantCessation > 0` and `Movement = Desire * s.vibrance > 0`.
    2. By `falling_man_equivalence` (`0 < s.mass_m`), `(s.support_N / m) + s.accel = s.pull_g`;
       dropping `HoldingOn` (`s.support_N = 0` on `s.shape > 0`) preserves `IsShape`, keeps
       `Movement = s.wanting * s.vibrance > 0`, cancels `s.mass_m > 0` from Newton's balance to
       yield `s.accel = s.pull_g`, and reduces the partition identity to `(0 / m) + g = g`.
    Epistemic status: `(a)`/`(b)` consequence under the `(c)` `FallingManState` identification. -/
theorem self_refutation_of_wanting_nonwanting
    (s : FallingManState F)
    (hOtherNonneg : zero ≤ s.otherDesire)
    (hWantStopPos : zero < s.wantCessation)
    (hWantPos     : zero < s.wanting)
    (hShapePos    : zero < s.shape)
    (hVibPos      : zero < s.vibrance)
    (hMassPos     : zero < s.mass_m) :
    let totalDesire := s.otherDesire + s.wantCessation
    (zero < totalDesire ∧ zero < totalDesire * s.vibrance) ∧
    ((s.support_N /ᶠ s.mass_m) + s.accel = s.pull_g) ∧
    (s.support_N = zero →
      IsShape ⟨s.shape, s.support_N⟩ ∧
      zero < s.wanting * s.vibrance ∧
      s.accel = s.pull_g ∧
      ((zero : F) /ᶠ s.mass_m) + s.pull_g = s.pull_g) := by
  dsimp only
  have hTotPos : zero < s.otherDesire + s.wantCessation := by
    have hle : zero + s.wantCessation ≤ s.otherDesire + s.wantCessation :=
      add_le_add hOtherNonneg (le_refl s.wantCessation)
    rw [zero_add] at hle
    exact lt_of_lt_of_le hWantStopPos hle
  have hMovStopPos : zero < (s.otherDesire + s.wantCessation) * s.vibrance :=
    mul_pos _ _ hTotPos hVibPos
  rcases falling_man_equivalence hMassPos s.newton_balance with ⟨hPart, _, _⟩
  refine ⟨⟨hTotPos, hMovStopPos⟩, hPart, ?_⟩
  intro hSupZero
  have hAccelEq : s.accel = s.pull_g := by
    have hBal := s.newton_balance
    rw [hSupZero, sub_def, neg_zero, add_zero] at hBal
    exact OrderedField.mul_left_cancel_pos hMassPos hBal
  have hFreeFall : ((zero : F) /ᶠ s.mass_m) + s.pull_g = s.pull_g := by
    have hPart0 := hPart
    rw [hSupZero, hAccelEq] at hPart0
    exact hPart0
  exact ⟨⟨hShapePos, hSupZero⟩, mul_pos _ _ hWantPos hVibPos, hAccelEq, hFreeFall⟩

/-!
  ## Theorem 3.3 — Confinement Scaling vs. Unique Weak-Diagonal Escape
  (*The Sovereign Mirror* v57, Ch. 10, pp. 76–79 & Ch. 12, pp. 86–90)

  Modeling choice `(c)`: `confinementStep H beta u_force := H + beta * u_force` is a linear
  formalization proxy (not an equation in the book) for Ch. 10 p. 77's qualitative quark-bond
  analogy, and `canStep` encodes the allowed quadrant transitions of Ch. 10 pp. 78–79.
-/

def confinementStep (H beta u_force : F) : F :=
  H + beta * u_force

/-- **Theorem 3.3a (Direct Forcing Strengthens Confinement)**:
    For positive coupling `β > 0`, any forceful push `u_force > 0` directly against an entrenched
    expectation strictly increases the modeled binding strength `H < H + β * u_force`.
    Epistemic status: `(a)`/`(b)` ordered-field inequality on the `(c)` function `confinementStep`. -/
theorem direct_forcing_increases_confinement {H beta u_force : F}
    (hBeta : zero < beta) (hForce : zero < u_force) :
    H < confinementStep H beta u_force := by
  unfold confinementStep
  have hProd : zero < beta * u_force := mul_pos beta u_force hBeta hForce
  have hlt := add_lt_add_left zero (beta * u_force) hProd H
  rw [add_zero] at hlt
  exact hlt

end ContrastFilterAndBuddhism

/-- Causal transition graph of *The Present* (`tuned` controls whether `Tune` has lowered
    effective `HoldingOn` enough for `Intuition` to shift `Belief` across the Weak Diagonal). -/
def canStep (tuned : Bool) : Quad → Quad → Bool
  | (.NP, .Out), (.NP, .In)  => true   -- Current collects Desire into Intuition
  | (.NP, .In),  (.P,  .Out) => tuned  -- Weak Diagonal: Intuition shifts Belief iff tuned
  | (.P,  .Out), (.P,  .In)  => true   -- Physical action returns In From evidence to Expectation
  | (.P,  .In),  (.NP, .Out) => true   -- Lived contrast launches new Desire
  | _,           _           => false  -- No direct Strong-to-Strong or world-bypassing jump

def isValidWalk (tuned : Bool) : List Quad → Bool
  | []           => false
  | [_]          => true
  | u :: v :: ws => canStep tuned u v && isValidWalk tuned (v :: ws)

def memQuad : Quad → List Quad → Bool
  | _, []      => false
  | x, y :: ys => (x == y) || memQuad x ys

def nodupQuad : List Quad → Bool
  | []      => true
  | x :: xs => !(memQuad x xs) && nodupQuad xs

private theorem step_from_intuition_false (q : Quad) :
    canStep false qIntuition q = false := by
  rcases q with ⟨s, d⟩
  cases s <;> cases d <;> rfl

private theorem step_from_intuition_true {q : Quad}
    (h : canStep true qIntuition q = true) : q = qBelief := by
  rcases q with ⟨s, d⟩
  cases s <;> cases d <;> simp [canStep, qIntuition, qBelief] at h ⊢

private theorem step_from_belief_true {q : Quad}
    (h : canStep true qBelief q = true) : q = qExpectation := by
  rcases q with ⟨s, d⟩
  cases s <;> cases d <;> simp [canStep, qBelief, qExpectation] at h ⊢

private theorem step_from_expectation_true {q : Quad}
    (h : canStep true qExpectation q = true) : q = qDesire := by
  rcases q with ⟨s, d⟩
  cases s <;> cases d <;> simp [canStep, qExpectation, qDesire] at h ⊢

private theorem step_from_desire_true {q : Quad}
    (h : canStep true qDesire q = true) : q = qIntuition := by
  rcases q with ⟨s, d⟩
  cases s <;> cases d <;> simp [canStep, qDesire, qIntuition] at h ⊢

/-- **Theorem 3.3b (Blocked Untuned Crossing & Unique Weak-Diagonal Escape Path)**:
    Over **all** walks `path : List Quad` of arbitrary finite length starting at `qIntuition`
    and ending at `qExpectation` under the `(c)` transition graph `canStep`:
      1. When `tuned = false`, **no** valid walk exists (`isValidWalk false path = false`).
      2. When `tuned = true`, a cycle-free (`nodupQuad`) walk is valid **if and only if**
         `path = [qIntuition, qBelief, qExpectation]`—uniquely traversing the Weak Diagonal
         `Intuition → Belief` followed by physical action `Belief → Expectation`.
    Epistemic status: `(a)` deductive consequence of the `(c)` transition graph `canStep`. -/
theorem unique_weak_diagonal_escape :
    (∀ path : List Quad,
      path.head? = some qIntuition →
      path.getLast? = some qExpectation →
      isValidWalk false path = false) ∧
    (∀ path : List Quad,
      (path.head? = some qIntuition ∧
       path.getLast? = some qExpectation ∧
       isValidWalk true path = true ∧
       nodupQuad path = true) ↔
      path = [qIntuition, qBelief, qExpectation]) := by
  constructor
  · intro path hHead hLast
    cases path with
    | nil => cases hHead
    | cons u rest =>
      simp only [List.head?_cons, Option.some.injEq] at hHead
      subst hHead
      cases rest with
      | nil =>
        simp [List.getLast?, qIntuition, qExpectation] at hLast
      | cons v ws =>
        simp only [isValidWalk, step_from_intuition_false v, Bool.false_and]
  · intro path
    constructor
    · rintro ⟨hHead, hLast, hValid, hNodup⟩
      cases path with
      | nil => cases hHead
      | cons q0 rest0 =>
        simp only [List.head?_cons, Option.some.injEq] at hHead
        subst hHead
        cases rest0 with
        | nil => simp [List.getLast?, qIntuition, qExpectation] at hLast
        | cons q1 rest1 =>
          simp only [isValidWalk, Bool.and_eq_true] at hValid
          rcases hValid with ⟨hStep01, hValid1⟩
          have hq1 : q1 = qBelief := step_from_intuition_true hStep01
          subst hq1
          cases rest1 with
          | nil => simp [List.getLast?, qBelief, qExpectation] at hLast
          | cons q2 rest2 =>
            simp only [isValidWalk, Bool.and_eq_true] at hValid1
            rcases hValid1 with ⟨hStep12, hValid2⟩
            have hq2 : q2 = qExpectation := step_from_belief_true hStep12
            subst hq2
            cases rest2 with
            | nil => rfl
            | cons q3 rest3 =>
              simp only [isValidWalk, Bool.and_eq_true] at hValid2
              rcases hValid2 with ⟨hStep23, hValid3⟩
              have hq3 : q3 = qDesire := step_from_expectation_true hStep23
              subst hq3
              cases rest3 with
              | nil => simp [List.getLast?, qDesire, qExpectation] at hLast
              | cons q4 rest4 =>
                simp only [isValidWalk, Bool.and_eq_true] at hValid3
                rcases hValid3 with ⟨hStep34, _⟩
                have hq4 : q4 = qIntuition := step_from_desire_true hStep34
                subst hq4
                simp only [nodupQuad, Bool.and_eq_true] at hNodup
                rcases hNodup with ⟨hNotContains, _⟩
                have hMem : memQuad qIntuition (qBelief :: qExpectation :: qDesire :: qIntuition :: rest4) = true := by
                  simp [memQuad, qIntuition, qBelief, qExpectation, qDesire]
                rw [hMem] at hNotContains
                cases hNotContains
    · intro hEq
      rw [hEq]
      decide

end TSR
