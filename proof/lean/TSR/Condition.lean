/-
  TSR/Condition.lean
  ==================
  Part I, Section 1 — Lean 4 formalization of condition-triad, ripple-evolution,
  irreversibility, and wave-interference models from *The Sovereign Mirror* (v57):
    - Proposition 1.1: Condition Triad Equivalence on Partitioned Media (`condition_triad_equivalence`),
                       Receptive Triad (`receptive_triad_equivalence`), and Undivided Locus Triad (`undivided_locus_triad`)
                       (SM v57 Ch. 1, pp. 16–19; Ch. 2, p. 20; *The Map*, pp. 169–170)
    - Theorem 1.2: Damped Ripple Decay (`ρ > 0`), Zero-Resistance Laminar Culmination (`ρ = 0`),
                   and Multi-Mode Chord Signature Preservation (`zero_resistance_chord_preservation`,
                   SM v57 Ch. 1, p. 18; Ch. 2, p. 21; Ch. 20, pp. 148–149)
    - Theorem 1.3: "The Knife" — Irreversibility of Zero-Resistance Expansion (SM v57 Ch. 14, p. 106)
    - Theorem 1.4: Wave Interference Spatial-Separation Requirement (SM v57 Ch. 16, p. 118)

  Epistemic status: explicit algebraic/discrete definitions (`Medium`, `barrier`, `transferCost`,
  `PerturbationMedium`, `trajectory`, `chordTrajectory`, `listSum`) are `(c)` modeling choices;
  all propositions/theorems here are `(a)` deductive consequences (using `(b)` ordered-field algebra).
-/

import TSR.OrderedAlgebra

namespace TSR
open OrderedField

section ConditionModule
variable {F : Type} [OrderedField F]

/-! ### Helper Field Lemmas for Subtractive Decay -/

theorem sub_lt_self {x p : F} (hp : zero < p) : x - p < x := by
  have h1 : (x - p) + zero < (x - p) + p := add_lt_add_left zero p hp (x - p)
  rw [add_zero, sub_def, add_assoc, add_left_neg, add_zero, ← sub_def] at h1
  exact h1

theorem one_sub_mul_eq_self_sub (alpha b : F) : (one - alpha) * b = b - alpha * b := by
  rw [sub_def, right_distrib, one_mul, neg_mul_eq_mul_neg, ← sub_def]

theorem not_pos_iff_eq_zero_of_nonneg {r : F} (hnonneg : zero ≤ r) :
    (¬ (zero < r)) ↔ r = zero := by
  rw [le_def] at hnonneg
  constructor
  · intro hnot
    cases hnonneg with
    | inl hlt => exact False.elim (hnot hlt)
    | inr heq => exact heq.symm
  · intro heq hlt
    rw [heq] at hlt
    exact lt_irrefl zero hlt

theorem pos_of_mul_pos_left {a b : F} (ha : zero < a) (hab : zero < a * b) : zero < b := by
  have haNe : a ≠ zero := ne_of_gt ha
  have hInvPos : zero < a⁻¹ := inv_pos_of_pos ha
  have hp : zero < a⁻¹ * (a * b) := mul_pos a⁻¹ (a * b) hInvPos hab
  rw [← mul_assoc, inv_mul_cancel haNe, one_mul] at hp
  exact hp

/-!
  ## Proposition 1.1 — Bilinear Metric-Work Coupling of the Condition Triad
  (*The Sovereign Mirror* v57, Ch. 1, pp. 16–19; Ch. 2, p. 20; *The Map*, pp. 169–170)

  Modeling choice `(c)`: The base `Medium F` structure assumes a locus space `(Locus, dist)`
  obeying `dist x x = 0` and `0 ≤ dist x y`, resistance parameter `ρ ≥ 0`, and coupling `κ > 0`.
  Spatial partition into distinct positively separated particulars (`IsPartitionedMedium M`)
  is factored out as an explicit hypothesis:
    - Formalization metric-resistance term: `barrier M x y := ρ * dist x y` (`(c)` modeling choice).
    - Formalization transfer-loss term: `transferCost M x y := κ * barrier M x y` (`(c)` modeling choice).
    - Note: `"barrier"` and `"transferCost"` are formalization identifiers `(c)`, not book vocabulary.
  Deductive consequences `(a)`:
    - On a partitioned physical medium (`IsPartitionedMedium M`), `Resistant ↔ Limited ↔ Radiating`.
    - On **any** medium (partitioned or undivided `Unit`), `ρ = 0` implies zero `barrier`/`transferCost`
      (`Limitless ∧ Collecting`), AND an undivided locus (`∀ x y, x = y`) independently forces zero
      `barrier`/`transferCost` (`Limitless ∧ Collecting`) via `dist_self`.
-/

structure Medium (F : Type) [OrderedField F] where
  Locus : Type
  dist : Locus → Locus → F
  dist_self : ∀ x : Locus, dist x x = zero
  dist_nonneg : ∀ x y : Locus, zero ≤ dist x y
  rho : F
  rho_nonneg : zero ≤ rho
  kappa : F
  kappa_pos : zero < kappa

/-- Explicit spatial-partition predicate: at least two distinct particulars separated by positive distance. -/
def IsPartitionedMedium (M : Medium F) : Prop :=
  (∃ x y : M.Locus, x ≠ y) ∧ (∀ x y : M.Locus, x ≠ y → zero < M.dist x y)

def barrier (M : Medium F) (x y : M.Locus) : F := M.rho * M.dist x y
def transferCost (M : Medium F) (x y : M.Locus) : F := M.kappa * barrier M x y

def Resistant (M : Medium F) : Prop := zero < M.rho
def Receptive (M : Medium F) : Prop := M.rho = zero
def Limited (M : Medium F) : Prop := ∃ x y : M.Locus, x ≠ y ∧ zero < barrier M x y
def Limitless (M : Medium F) : Prop := ¬ Limited M
def Radiating (M : Medium F) : Prop := ∃ x y : M.Locus, x ≠ y ∧ zero < transferCost M x y
def Collecting (M : Medium F) : Prop := ¬ Radiating M

theorem barrier_nonneg (M : Medium F) (x y : M.Locus) : zero ≤ barrier M x y :=
  mul_nonneg M.rho_nonneg (M.dist_nonneg x y)

theorem transferCost_nonneg (M : Medium F) (x y : M.Locus) : zero ≤ transferCost M x y :=
  mul_nonneg (le_of_lt M.kappa_pos) (barrier_nonneg M x y)

theorem limited_iff_radiating (M : Medium F) : Limited M ↔ Radiating M := by
  constructor
  · rintro ⟨x, y, hne, hbar⟩
    exact ⟨x, y, hne, mul_pos M.kappa (barrier M x y) M.kappa_pos hbar⟩
  · rintro ⟨x, y, hne, hrad⟩
    exact ⟨x, y, hne, pos_of_mul_pos_left M.kappa_pos hrad⟩

/-- **Proposition 1.1a (Physical Condition Triad on Partitioned Media)**:
    Under explicit spatial partition `(hPart : IsPartitionedMedium M)`,
    `Resistant M ↔ Limited M`, `Limited M ↔ Radiating M`, and `Resistant M ↔ Radiating M`. -/
theorem condition_triad_equivalence (M : Medium F) (hPart : IsPartitionedMedium M) :
    (Resistant M ↔ Limited M) ∧ (Limited M ↔ Radiating M) ∧ (Resistant M ↔ Radiating M) := by
  have hRL : Resistant M ↔ Limited M := by
    constructor
    · intro hRes
      rcases hPart.1 with ⟨x, y, hne⟩
      have hd : zero < M.dist x y := hPart.2 x y hne
      exact ⟨x, y, hne, mul_pos M.rho (M.dist x y) hRes hd⟩
    · rintro ⟨x, y, hne, hbar⟩
      have hd : zero < M.dist x y := hPart.2 x y hne
      unfold barrier at hbar
      rw [mul_comm] at hbar
      exact pos_of_mul_pos_left hd hbar
  have hLR : Limited M ↔ Radiating M := limited_iff_radiating M
  exact ⟨hRL, hLR, Iff.trans hRL hLR⟩

/-- **Proposition 1.1b (Receptive Triad on Arbitrary Media)**:
    On **any** `Medium F` (whether undivided `Unit` or partitioned):
      1. Zero resistance (`Receptive M`, i.e., `M.rho = 0`) annihilates all barriers and
         transfer costs identically and guarantees `Limitless M ∧ Collecting M`.
      2. `Limitless M ↔ Collecting M` holds unconditionally.
      3. When `IsPartitionedMedium M` holds, the full biconditionals
         `(Receptive M ↔ Limitless M) ∧ (Receptive M ↔ Collecting M)` hold as well. -/
theorem receptive_triad_equivalence (M : Medium F) :
    (Receptive M →
      (∀ x y : M.Locus, barrier M x y = zero) ∧
      (∀ x y : M.Locus, transferCost M x y = zero) ∧
      Limitless M ∧
      Collecting M) ∧
    (Limitless M ↔ Collecting M) ∧
    (IsPartitionedMedium M → (Receptive M ↔ Limitless M) ∧ (Receptive M ↔ Collecting M)) := by
  have hLR : Limited M ↔ Radiating M := limited_iff_radiating M
  have hLC : Limitless M ↔ Collecting M := not_congr hLR
  refine ⟨?_, hLC, ?_⟩
  · intro hRec
    have hBarZero : ∀ x y : M.Locus, barrier M x y = zero := by
      intro x y
      unfold barrier
      rw [hRec, zero_mul]
    have hTransZero : ∀ x y : M.Locus, transferCost M x y = zero := by
      intro x y
      unfold transferCost
      rw [hBarZero x y, mul_zero]
    have hLim : Limitless M := by
      rintro ⟨x, y, _, hPos⟩
      rw [hBarZero x y] at hPos
      exact lt_irrefl zero hPos
    have hCol : Collecting M := hLC.mp hLim
    exact ⟨hBarZero, hTransZero, hLim, hCol⟩
  · intro hPart
    rcases condition_triad_equivalence M hPart with ⟨hRL, _, _⟩
    have hRecNotRes : Receptive M ↔ ¬ Resistant M :=
      (not_pos_iff_eq_zero_of_nonneg M.rho_nonneg).symm
    have hRecLim : Receptive M ↔ Limitless M := Iff.trans hRecNotRes (not_congr hRL)
    exact ⟨hRecLim, Iff.trans hRecLim hLC⟩

/-- **Proposition 1.1c (Undivided Locus Triad)**:
    On any `Medium F` whose locus is undivided (`∀ x y : M.Locus, x = y`), `dist_self`
    forces `barrier M x y = 0` and `transferCost M x y = 0` for all `x, y`, directly
    establishing `Limitless M ∧ Collecting M` without positive-separation assumptions. -/
theorem undivided_locus_triad (M : Medium F) (hUndiv : ∀ x y : M.Locus, x = y) :
    (∀ x y : M.Locus, barrier M x y = zero) ∧
    (∀ x y : M.Locus, transferCost M x y = zero) ∧
    Limitless M ∧
    Collecting M := by
  have hBarZero : ∀ x y : M.Locus, barrier M x y = zero := by
    intro x y
    unfold barrier
    rw [hUndiv x y, M.dist_self y, mul_zero]
  have hTransZero : ∀ x y : M.Locus, transferCost M x y = zero := by
    intro x y
    unfold transferCost
    rw [hBarZero x y, mul_zero]
  have hLim : Limitless M := by
    rintro ⟨x, y, _, hPos⟩
    rw [hBarZero x y] at hPos
    exact lt_irrefl zero hPos
  have hCol : Collecting M := by
    rintro ⟨x, y, _, hPos⟩
    rw [hTransZero x y] at hPos
    exact lt_irrefl zero hPos
  exact ⟨hBarZero, hTransZero, hLim, hCol⟩

/-!
  ## Theorem 1.2 — Ripple Decay (`ρ > 0`) vs. Laminar Culmination (`ρ = 0`)
  (*The Sovereign Mirror* v57, Ch. 1, p. 18; Ch. 2, p. 21; Ch. 20, pp. 148–149)

  Modeling choice `(c)`: `PerturbationMedium`, `trajectory` (`B_{n+1} = (1 - α) B_n + ξ_n`),
  `singleModePulse`, and `chordTrajectory` (`C_{n+1}(m) = (1 - ρ) C_n(m) + pulse_n(m)`) are
  discrete linear-update models encoding the qualitative contrast between damped water ripples
  and undamped laminar/chord culmination in the book (which states no explicit recurrence formula).
-/

structure PerturbationMedium (F : Type) [OrderedField F] where
  rho : F
  rho_nonneg : zero ≤ rho
  alpha : F
  alpha_zero_iff : alpha = zero ↔ rho = zero
  alpha_bounds_of_pos : zero < rho → zero < alpha ∧ alpha < one

/-- Discrete state trajectory `B_{n+1} = (1 - α) B_n + ξ_n`. -/
def trajectory (alpha B0 : F) (xi : Nat → F) : Nat → F
  | 0 => B0
  | n + 1 => (one - alpha) * trajectory alpha B0 xi n + xi n

/-- Cumulative disturbance sum `∑_{k < n} ξ_k`. -/
def partialSum (xi : Nat → F) : Nat → F
  | 0 => zero
  | n + 1 => partialSum xi n + xi n

/-- **Theorem 1.2a (Damped Ripple Strict Decay)**:
    In any resistant medium (`0 < ρ`), an unforced ripple (`ξ_n = 0`) launched from
    `B_0 > 0` remains positive while strictly decaying at every step: `B_{n+1} < B_n`. -/
theorem damped_ripple_strict_decay (M : PerturbationMedium F)
    (hRes : zero < M.rho) (B0 : F) (hB0 : zero < B0)
    (xi : Nat → F) (hUnforced : ∀ n : Nat, xi n = zero) :
    ∀ n : Nat,
      zero < trajectory M.alpha B0 xi (n + 1) ∧
      trajectory M.alpha B0 xi (n + 1) < trajectory M.alpha B0 xi n := by
  rcases M.alpha_bounds_of_pos hRes with ⟨hAlphaPos, hAlphaLtOne⟩
  have hOneSubPos : zero < one - M.alpha := sub_pos_of_lt hAlphaLtOne
  have hPosAll : ∀ k : Nat, zero < trajectory M.alpha B0 xi k := by
    intro k
    induction k with
    | zero => exact hB0
    | succ k ih =>
      simp only [trajectory]
      rw [hUnforced k, add_zero]
      exact mul_pos (one - M.alpha) (trajectory M.alpha B0 xi k) hOneSubPos ih
  intro n
  refine ⟨hPosAll (n + 1), ?_⟩
  have hBnPos : zero < trajectory M.alpha B0 xi n := hPosAll n
  have hStep : trajectory M.alpha B0 xi (n + 1)
             = trajectory M.alpha B0 xi n - M.alpha * trajectory M.alpha B0 xi n := by
    simp only [trajectory]
    rw [hUnforced n, add_zero, one_sub_mul_eq_self_sub]
  rw [hStep]
  exact sub_lt_self (mul_pos M.alpha (trajectory M.alpha B0 xi n) hAlphaPos hBnPos)

/-- **Theorem 1.2b (Zero-Resistance Laminar Culmination)**:
    When `ρ = 0`, damping vanishes (`α = 0`), every disturbance accumulates exactly into
    the new permanent baseline `B_n = B_0 + ∑_{k < n} ξ_k`, and every positive pulse
    strictly raises the whole (`B_n < B_{n+1}`). -/
theorem zero_resistance_culmination (M : PerturbationMedium F)
    (hRec : M.rho = zero) (B0 : F) (xi : Nat → F) :
    (∀ n : Nat, trajectory M.alpha B0 xi (n + 1) = trajectory M.alpha B0 xi n + xi n) ∧
    (∀ n : Nat, trajectory M.alpha B0 xi n = B0 + partialSum xi n) ∧
    (∀ n : Nat, zero < xi n → trajectory M.alpha B0 xi n < trajectory M.alpha B0 xi (n + 1)) := by
  have hAlphaZero : M.alpha = zero := M.alpha_zero_iff.mpr hRec
  have hStep : ∀ n : Nat, trajectory M.alpha B0 xi (n + 1) = trajectory M.alpha B0 xi n + xi n := by
    intro n
    simp only [trajectory]
    rw [hAlphaZero, sub_def, neg_zero, add_zero, one_mul]
  have hClosed : ∀ n : Nat, trajectory M.alpha B0 xi n = B0 + partialSum xi n := by
    intro n
    induction n with
    | zero =>
      simp only [trajectory, partialSum]
      rw [add_zero]
    | succ n ih =>
      rw [hStep n, ih]
      simp only [partialSum]
      rw [add_assoc]
  have hStrict : ∀ n : Nat, zero < xi n →
      trajectory M.alpha B0 xi n < trajectory M.alpha B0 xi (n + 1) := by
    intro n hXiPos
    rw [hStep n]
    have hlt := add_lt_add_left zero (xi n) hXiPos (trajectory M.alpha B0 xi n)
    rw [add_zero] at hlt
    exact hlt
  exact ⟨hStep, hClosed, hStrict⟩

/-- Single-mode pulse injecting `xi` onto mode `m0` at step `0` and `zero` elsewhere / thereafter. -/
def singleModePulse {Mode : Type} [DecidableEq Mode]
    (m0 : Mode) (xi : F) : Nat → Mode → F
  | 0,     m => if m = m0 then xi else zero
  | _ + 1, _ => zero

/-- Mode-indexed ("chord") state trajectory `C_{n+1}(m) = (1 - ρ) C_n(m) + pulse_n(m)`
    (*The Sovereign Mirror*, Ch. 20, pp. 148–149: distinct vibrational signatures coexisting
    without spatial walls like notes in a chord). -/
def chordTrajectory {Mode : Type}
    (rho : F) (C0 : Mode → F) (pulse : Nat → Mode → F) : Nat → Mode → F
  | 0,     m => C0 m
  | n + 1, m => (one - rho) * chordTrajectory rho C0 pulse n m + pulse n m

/-- **Theorem 1.2c (Zero-Resistance Chord Signature Preservation vs. Positive-Resistance Decay)**:
    Over any mode-indexed state space `Mode → F` (`[DecidableEq Mode]`):
      1. When `ρ = 0`, injecting a pulse `ξ > 0` on mode `m0` permanently raises and preserves
         `m0`'s amplitude (`C_{n+1}(m0) = C_0(m0) + ξ > C_0(m0)`) across all future steps `n`
         while leaving every distinct mode `m1 ≠ m0` completely untouched (`C_n(m1) = C_0(m1)`).
      2. Conversely, when `0 < ρ < 1`, every unforced mode starting at `C_0(m) > 0` remains
         positive while strictly decaying at every step (`C_{n+1}(m) < C_n(m)`). -/
theorem zero_resistance_chord_preservation {Mode : Type} [DecidableEq Mode]
    (C0 : Mode → F) (m0 : Mode) (xi : F) (hXiPos : zero < xi) :
    ((∀ n : Nat,
        chordTrajectory zero C0 (singleModePulse m0 xi) (n + 1) m0 = C0 m0 + xi ∧
        C0 m0 < chordTrajectory zero C0 (singleModePulse m0 xi) (n + 1) m0) ∧
     (∀ m1 : Mode, m1 ≠ m0 → ∀ n : Nat,
        chordTrajectory zero C0 (singleModePulse m0 xi) n m1 = C0 m1)) ∧
    (∀ rho : F, zero < rho → rho < one →
      ∀ m : Mode, zero < C0 m → ∀ n : Nat,
        zero < chordTrajectory rho C0 (fun _ _ => zero) (n + 1) m ∧
        chordTrajectory rho C0 (fun _ _ => zero) (n + 1) m <
          chordTrajectory rho C0 (fun _ _ => zero) n m) := by
  have hOneSubZero : (one : F) - zero = one := by
    rw [sub_def, neg_zero, add_zero]
  have hTarget : ∀ n : Nat,
      chordTrajectory zero C0 (singleModePulse m0 xi) (n + 1) m0 = C0 m0 + xi := by
    intro n
    induction n with
    | zero =>
      change (one - zero) * C0 m0 + (if m0 = m0 then xi else zero) = C0 m0 + xi
      simp only [↓reduceIte]
      rw [hOneSubZero, one_mul]
    | succ n ih =>
      change (one - zero) * chordTrajectory zero C0 (singleModePulse m0 xi) (n + 1) m0 + zero = C0 m0 + xi
      rw [hOneSubZero, one_mul, add_zero, ih]
  have hTargetRaises : ∀ n : Nat,
      chordTrajectory zero C0 (singleModePulse m0 xi) (n + 1) m0 = C0 m0 + xi ∧
      C0 m0 < chordTrajectory zero C0 (singleModePulse m0 xi) (n + 1) m0 := by
    intro n
    refine ⟨hTarget n, ?_⟩
    rw [hTarget n]
    have hlt := add_lt_add_left zero xi hXiPos (C0 m0)
    rw [add_zero] at hlt
    exact hlt
  have hOtherPreserved : ∀ m1 : Mode, m1 ≠ m0 → ∀ n : Nat,
      chordTrajectory zero C0 (singleModePulse m0 xi) n m1 = C0 m1 := by
    intro m1 hNe n
    induction n with
    | zero => rfl
    | succ k ih =>
      cases k with
      | zero =>
        change (one - zero) * C0 m1 + (if m1 = m0 then xi else zero) = C0 m1
        simp only [hNe, ↓reduceIte]
        rw [hOneSubZero, one_mul, add_zero]
      | succ k' =>
        change (one - zero) * chordTrajectory zero C0 (singleModePulse m0 xi) (k' + 1) m1 + zero = C0 m1
        rw [hOneSubZero, one_mul, add_zero, ih]
  have hResDecay : ∀ rho : F, zero < rho → rho < one →
      ∀ m : Mode, zero < C0 m → ∀ n : Nat,
        zero < chordTrajectory rho C0 (fun _ _ => zero) (n + 1) m ∧
        chordTrajectory rho C0 (fun _ _ => zero) (n + 1) m <
          chordTrajectory rho C0 (fun _ _ => zero) n m := by
    intro rho hRhoPos hRhoLtOne m hCmPos
    have hFactorPos : zero < one - rho := sub_pos_of_lt hRhoLtOne
    have hModePos : ∀ k : Nat, zero < chordTrajectory rho C0 (fun _ _ => zero) k m := by
      intro k
      induction k with
      | zero => exact hCmPos
      | succ k ih =>
        simp only [chordTrajectory]
        rw [add_zero]
        exact mul_pos (one - rho) (chordTrajectory rho C0 (fun _ _ => zero) k m) hFactorPos ih
    intro n
    refine ⟨hModePos (n + 1), ?_⟩
    have hStep : chordTrajectory rho C0 (fun _ _ => zero) (n + 1) m
               = chordTrajectory rho C0 (fun _ _ => zero) n m -
                 rho * chordTrajectory rho C0 (fun _ _ => zero) n m := by
      simp only [chordTrajectory]
      rw [add_zero, one_sub_mul_eq_self_sub]
    rw [hStep]
    exact sub_lt_self (mul_pos rho (chordTrajectory rho C0 (fun _ _ => zero) n m) hRhoPos (hModePos n))
  exact ⟨⟨hTargetRaises, hOtherPreserved⟩, hResDecay⟩

/-!
  ## Theorem 1.3 — "The Knife": Irreversibility of Zero-Resistance Expansion
  (*The Sovereign Mirror* v57, Ch. 14, p. 106: *"You can cover a cut. You can't uncut it."*)

  Epistemic status: `(b)` ordered-field additive cancellation `(P0 + δ) - δ = P0` paired with
  `(a)` monotonicity/strictness of `trajectory` under the `(c)` `PerturbationMedium` model.
-/

theorem zero_resistance_monotone (M : PerturbationMedium F)
    (hRec : M.rho = zero) (B0 : F) (xi : Nat → F)
    (hNonneg : ∀ n : Nat, zero ≤ xi n) :
    ∀ {k m : Nat}, k ≤ m → trajectory M.alpha B0 xi k ≤ trajectory M.alpha B0 xi m := by
  rcases zero_resistance_culmination M hRec B0 xi with ⟨hStep, _, _⟩
  intro k m hkm
  induction m with
  | zero =>
    have hk0 : k = 0 := by omega
    rw [hk0]
    exact le_refl _
  | succ m ih =>
    by_cases hkm' : k ≤ m
    · have hprev : trajectory M.alpha B0 xi k ≤ trajectory M.alpha B0 xi m := ih hkm'
      have hnext : trajectory M.alpha B0 xi m ≤ trajectory M.alpha B0 xi (m + 1) := by
        rw [hStep m]
        have hle := add_le_add (le_refl (trajectory M.alpha B0 xi m)) (hNonneg m)
        rw [add_zero] at hle
        exact hle
      exact le_trans hprev hnext
    · have hkeq : k = m + 1 := by omega
      rw [hkeq]
      exact le_refl _

/-- **Theorem 1.3 ("The Knife" — Physical Covering vs. Zero-Resistance Irreversibility)**:
    1. *Physical covering*: A physical state `P0` displaced by `δ > 0` (`P1 = P0 + δ`) and
       pushed back by `-δ` (`P2 = P1 - δ`) returns identically to `P2 = P0` (*"You can cover a cut."*, *SM* v57 Ch. 14 p. 106).
    2. *Nonphysical non-uncutting*: In a zero-resistance cumulative medium (`ρ = 0`) receiving
       contrast energy `ξ_n ≥ 0`, once step `k` strictly expands the baseline (`B_k < B_{k+1}`),
       no future state `B_m` (`m ≥ k + 1`) ever returns to `B_k` (*"You can't uncut it."*, *SM* v57 Ch. 14 p. 106). -/
theorem the_knife_irreversibility (M : PerturbationMedium F)
    (hRec : M.rho = zero) (P0 delta B0 : F) (hDelta : zero < delta)
    (xi : Nat → F) (hNonneg : ∀ n : Nat, zero ≤ xi n)
    {k m : Nat} (hCut : trajectory M.alpha B0 xi k < trajectory M.alpha B0 xi (k + 1))
    (hFuture : k + 1 ≤ m) :
    ((P0 < P0 + delta ∧ (P0 + delta) - delta = P0) ∧
     (trajectory M.alpha B0 xi k < trajectory M.alpha B0 xi m ∧
      trajectory M.alpha B0 xi m ≠ trajectory M.alpha B0 xi k)) := by
  have hPhysCut : P0 < P0 + delta := by
    have hlt := add_lt_add_left zero delta hDelta P0
    rw [add_zero] at hlt
    exact hlt
  have hPhysCover : (P0 + delta) - delta = P0 := by
    rw [sub_def, add_assoc, add_right_neg, add_zero]
  have hMono := zero_resistance_monotone M hRec B0 xi hNonneg hFuture
  have hStrict : trajectory M.alpha B0 xi k < trajectory M.alpha B0 xi m :=
    lt_of_lt_of_le hCut hMono
  exact ⟨⟨hPhysCut, hPhysCover⟩, ⟨hStrict, ne_of_gt hStrict⟩⟩

/-!
  ## Theorem 1.4 — Wave Interference Requires Spatial Separation
  (*The Sovereign Mirror* v57, Ch. 16, p. 118: why waves cancel in Space-Time via separated
  dark/bright fringes, whereas in the undivided Current two Movements cannot cancel.)

  Epistemic status: modeling intensity conservation as a finite list sum `listSum X I = E_tot > 0`
  is `(c)`/`(b)`; `destructive_null_requires_spatial_separation` and `single_locus_cannot_cancel`
  are `(a)` deductive consequences.
-/

/-- Total energy summed over a finite list of spatial loci. -/
def listSum {Locus : Type} : List Locus → (Locus → F) → F
  | [], _ => zero
  | x :: xs, I => I x + listSum xs I

theorem exists_bright_locus_of_pos_total {Locus : Type}
    (X : List Locus) (I : Locus → F)
    (hPosTotal : zero < listSum X I) :
    ∃ x1 : Locus, x1 ∈ X ∧ zero < I x1 := by
  induction X with
  | nil =>
    unfold listSum at hPosTotal
    exact False.elim (lt_irrefl zero hPosTotal)
  | cons x xs ih =>
    unfold listSum at hPosTotal
    rcases lt_trichotomy zero (I x) with hxPos | hxZero | hxNeg
    · exact ⟨x, List.Mem.head xs, hxPos⟩
    · rw [← hxZero, zero_add] at hPosTotal
      rcases ih hPosTotal with ⟨x1, hx1Mem, hx1Pos⟩
      exact ⟨x1, List.Mem.tail x hx1Mem, hx1Pos⟩
    · have hRestPos : zero < listSum xs I := by
        rcases lt_trichotomy zero (listSum xs I) with hr | hr | hr
        · exact hr
        · rw [← hr, add_zero] at hPosTotal
          exact False.elim (lt_asymm hPosTotal hxNeg)
        · have hNegSum : I x + listSum xs I < zero + zero := add_lt_add hxNeg hr
          rw [add_zero] at hNegSum
          exact False.elim (lt_asymm hPosTotal hNegSum)
      rcases ih hRestPos with ⟨x1, hx1Mem, hx1Pos⟩
      exact ⟨x1, List.Mem.tail x hx1Mem, hx1Pos⟩

theorem length_ge_two_of_two_distinct_mem {Locus : Type}
    {X : List Locus} {x0 x1 : Locus}
    (h0 : x0 ∈ X) (h1 : x1 ∈ X) (hne : x1 ≠ x0) :
    2 ≤ X.length := by
  cases X with
  | nil => cases h0
  | cons a xs =>
    cases xs with
    | nil =>
      cases h0 with
      | head =>
        cases h1 with
        | head => exact False.elim (hne rfl)
        | tail _ hm => cases hm
      | tail _ hm => cases hm
    | cons b ys =>
      simp only [List.length_cons]
      omega

/-- **Theorem 1.4a (Destructive Null Requires Separated Bright Fringe & `|X| ≥ 2`)**:
    Under conserved positive total energy (`listSum X I = E_tot > 0`), if any locus `x0 ∈ X`
    exhibits destructive cancellation (`I x0 = 0`), then `2 ≤ X.length` and there exists a
    **distinct** spatially separated locus `x1 ∈ X` (`x1 ≠ x0`) carrying positive energy (`0 < I x1`). -/
theorem destructive_null_requires_spatial_separation {Locus : Type}
    (X : List Locus) (I : Locus → F) (E_tot : F)
    (hConserved : listSum X I = E_tot) (hPosEnergy : zero < E_tot)
    {x0 : Locus} (hx0Mem : x0 ∈ X) (hDarkNull : I x0 = zero) :
    2 ≤ X.length ∧ ∃ x1 : Locus, x1 ∈ X ∧ x1 ≠ x0 ∧ zero < I x1 := by
  have hSumPos : zero < listSum X I := by
    rw [hConserved]
    exact hPosEnergy
  rcases exists_bright_locus_of_pos_total X I hSumPos with ⟨x1, hx1Mem, hx1Pos⟩
  have hDistinct : x1 ≠ x0 := by
    intro heq
    rw [heq, hDarkNull] at hx1Pos
    exact lt_irrefl zero hx1Pos
  exact ⟨length_ge_two_of_two_distinct_mem hx0Mem hx1Mem hDistinct, x1, hx1Mem, hDistinct, hx1Pos⟩

/-- **Theorem 1.4b (Undivided Single Locus Cannot Cancel)**:
    When separation collapses to a single undivided locus `X = [x0]` (`ρ = 0`),
    conservation forces `I x0 = E1 + E2 > 0`; destructive cancellation `I x0 = 0` is impossible. -/
theorem single_locus_cannot_cancel {Locus : Type}
    (x0 : Locus) (I : Locus → F) (E1 E2 : F)
    (hConserved : listSum [x0] I = E1 + E2)
    (hE1 : zero < E1) (hE2 : zero < E2) :
    I x0 = E1 + E2 ∧ zero < I x0 ∧ I x0 ≠ zero := by
  simp only [listSum] at hConserved
  rw [add_zero] at hConserved
  have hSumPos : zero < E1 + E2 := by
    have hlt := add_lt_add hE1 hE2
    rw [add_zero] at hlt
    exact hlt
  have hPos : zero < I x0 := by
    rw [hConserved]
    exact hSumPos
  exact ⟨hConserved, hPos, ne_of_gt hPos⟩

end ConditionModule
end TSR
