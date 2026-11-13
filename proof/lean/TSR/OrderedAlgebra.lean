/-
  TSR/OrderedAlgebra.lean
  =======================
  Self-contained axiomatization of Linear Ordered Fields (`OrderedField F`)
  over Lean 4 core (`Init`), together with general ordered-field theorems and
  a fully constructive rational model `QRat` (`OrderedField QRat`).

  Epistemic classification: `(b)` standard ordered-field algebra.
  Having both:
    (1) Generic theorems quantified over an arbitrary `[OrderedField F]` (applicable
        to ℝ, ℚ, or any ordered commutative field), and
    (2) A constructive witness `OrderedField QRat` built from `Int` with zero
        `sorry` and zero `Classical.choice`,
  establishes that all ordered-field results hold in general `[OrderedField F]`
  and that the `OrderedField` axioms are constructively inhabited by `QRat`.
-/

namespace TSR

/-- Standard mathematical axioms of a Linear Ordered Commutative Field. -/
class OrderedField (F : Type) extends Add F, Sub F, Neg F, Mul F, Inv F, LT F, LE F where
  zero : F
  one : F
  sub_def : ∀ a b : F, a - b = a + (-b)
  le_def : ∀ a b : F, (a ≤ b) ↔ (a < b ∨ a = b)
  add_assoc : ∀ a b c : F, a + b + c = a + (b + c)
  add_comm : ∀ a b : F, a + b = b + a
  zero_add : ∀ a : F, zero + a = a
  add_left_neg : ∀ a : F, (-a) + a = zero
  mul_assoc : ∀ a b c : F, a * b * c = a * (b * c)
  mul_comm : ∀ a b : F, a * b = b * a
  one_mul : ∀ a : F, one * a = a
  left_distrib : ∀ a b c : F, a * (b + c) = a * b + a * c
  mul_inv_cancel : ∀ a : F, a ≠ zero → a * a⁻¹ = one
  zero_ne_one : zero ≠ one
  lt_irrefl : ∀ a : F, ¬ (a < a)
  lt_trans : ∀ a b c : F, a < b → b < c → a < c
  lt_trichotomy : ∀ a b : F, a < b ∨ a = b ∨ b < a
  add_lt_add_left : ∀ a b : F, a < b → ∀ c : F, c + a < c + b
  mul_pos : ∀ a b : F, zero < a → zero < b → zero < a * b

namespace OrderedField

section GeneralTheorems
variable {F : Type} [OrderedField F]

/-- Field division `a / b := a * b⁻¹`. -/
def fdiv (a b : F) : F := a * b⁻¹

infixl:70 " /ᶠ " => fdiv

theorem add_zero (a : F) : a + zero = a := by
  rw [add_comm, zero_add]

theorem add_right_neg (a : F) : a + (-a) = zero := by
  rw [add_comm, add_left_neg]

theorem mul_one (a : F) : a * one = a := by
  rw [mul_comm, one_mul]

theorem right_distrib (a b c : F) : (a + b) * c = a * c + b * c := by
  rw [mul_comm, left_distrib, mul_comm c a, mul_comm c b]

theorem inv_mul_cancel {a : F} (h : a ≠ zero) : a⁻¹ * a = one := by
  rw [mul_comm, mul_inv_cancel a h]

theorem add_left_cancel {a b c : F} (h : a + b = a + c) : b = c := by
  have h1 : (-a) + (a + b) = (-a) + (a + c) := congrArg (fun x => (-a) + x) h
  rw [← add_assoc, ← add_assoc, add_left_neg, zero_add, zero_add] at h1
  exact h1

theorem add_right_cancel {a b c : F} (h : a + c = b + c) : a = b := by
  apply add_left_cancel (a := c)
  rw [add_comm c a, add_comm c b]
  exact h

theorem zero_mul (a : F) : zero * a = zero := by
  apply add_left_cancel (a := zero * a)
  rw [← right_distrib, zero_add, add_zero]

theorem mul_zero (a : F) : a * zero = zero := by
  rw [mul_comm, zero_mul]

theorem neg_zero : (- (zero : F)) = zero := by
  apply add_right_cancel (c := zero)
  rw [add_left_neg, zero_add]

theorem neg_neg (a : F) : -(-a) = a := by
  apply add_left_cancel (a := -a)
  rw [add_right_neg, add_left_neg]

theorem neg_mul_eq_mul_neg (a b : F) : (-a) * b = -(a * b) := by
  apply add_left_cancel (a := a * b)
  rw [← right_distrib, add_right_neg, zero_mul, add_right_neg]

theorem mul_neg_eq_neg_mul_symm (a b : F) : a * (-b) = -(a * b) := by
  apply add_left_cancel (a := a * b)
  rw [← left_distrib, add_right_neg, mul_zero, add_right_neg]

theorem neg_mul_neg (a b : F) : (-a) * (-b) = a * b := by
  rw [neg_mul_eq_mul_neg, mul_neg_eq_neg_mul_symm, neg_neg]

theorem sub_self (a : F) : a - a = zero := by
  rw [sub_def, add_right_neg]

theorem sub_eq_zero {a b : F} : a - b = zero ↔ a = b := by
  constructor
  · intro h
    rw [sub_def] at h
    have h2 : (a + -b) + b = zero + b := congrArg (fun x => x + b) h
    rw [add_assoc, add_left_neg, add_zero, zero_add] at h2
    exact h2
  · intro h
    rw [h, sub_self]

theorem add_lt_add_right {a b : F} (h : a < b) (c : F) : a + c < b + c := by
  rw [add_comm a c, add_comm b c]
  exact add_lt_add_left a b h c

theorem add_lt_add {a b c d : F} (h1 : a < b) (h2 : c < d) : a + c < b + d := by
  exact lt_trans (a + c) (b + c) (b + d) (add_lt_add_right h1 c) (add_lt_add_left c d h2 b)

theorem lt_asymm {a b : F} (h : a < b) : ¬ (b < a) := by
  intro hba
  exact lt_irrefl a (lt_trans a b a h hba)

theorem ne_of_lt {a b : F} (h : a < b) : a ≠ b := by
  intro hab
  rw [hab] at h
  exact lt_irrefl b h

theorem ne_of_gt {a b : F} (h : b < a) : a ≠ b := by
  intro hab
  rw [hab] at h
  exact lt_irrefl b h

theorem le_refl (a : F) : a ≤ a := by
  rw [le_def]
  exact Or.inr rfl

theorem le_of_lt {a b : F} (h : a < b) : a ≤ b := by
  rw [le_def]
  exact Or.inl h

theorem lt_of_le_of_lt {a b c : F} (h1 : a ≤ b) (h2 : b < c) : a < c := by
  rw [le_def] at h1
  cases h1 with
  | inl hlt => exact lt_trans a b c hlt h2
  | inr heq => rw [heq]; exact h2

theorem lt_of_lt_of_le {a b c : F} (h1 : a < b) (h2 : b ≤ c) : a < c := by
  rw [le_def] at h2
  cases h2 with
  | inl hlt => exact lt_trans a b c h1 hlt
  | inr heq => rw [← heq]; exact h1

theorem le_trans {a b c : F} (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by
  rw [le_def] at h1 h2 ⊢
  cases h1 with
  | inl hlt1 =>
    cases h2 with
    | inl hlt2 => exact Or.inl (lt_trans a b c hlt1 hlt2)
    | inr heq2 => rw [← heq2]; exact Or.inl hlt1
  | inr heq1 =>
    rw [heq1]
    exact h2

theorem le_antisymm {a b : F} (h1 : a ≤ b) (h2 : b ≤ a) : a = b := by
  rw [le_def] at h1 h2
  cases h1 with
  | inl hlt1 =>
    cases h2 with
    | inl hlt2 => exact False.elim (lt_irrefl a (lt_trans a b a hlt1 hlt2))
    | inr heq2 => exact heq2.symm
  | inr heq1 => exact heq1

theorem add_le_add {a b c d : F} (h1 : a ≤ b) (h2 : c ≤ d) : a + c ≤ b + d := by
  rw [le_def] at h1 h2 ⊢
  cases h1 with
  | inl hlt1 =>
    cases h2 with
    | inl hlt2 => exact Or.inl (add_lt_add hlt1 hlt2)
    | inr heq2 => rw [heq2]; exact Or.inl (add_lt_add_right hlt1 d)
  | inr heq1 =>
    rw [heq1]
    cases h2 with
    | inl hlt2 => exact Or.inl (add_lt_add_left c d hlt2 b)
    | inr heq2 => rw [heq2]; exact Or.inr rfl

theorem sub_pos_of_lt {a b : F} (h : a < b) : zero < b - a := by
  have h1 := add_lt_add_right h (-a)
  rw [add_right_neg, ← sub_def] at h1
  exact h1

theorem sub_nonneg_of_le {a b : F} (h : a ≤ b) : zero ≤ b - a := by
  rw [le_def] at h ⊢
  cases h with
  | inl hlt => exact Or.inl (sub_pos_of_lt hlt)
  | inr heq => rw [heq, sub_self]; exact Or.inr rfl

theorem lt_of_sub_pos {a b : F} (h : zero < b - a) : a < b := by
  have h1 := add_lt_add_right h a
  rw [zero_add, sub_def, add_assoc, add_left_neg, add_zero] at h1
  exact h1

theorem neg_pos_of_neg {a : F} (h : a < zero) : zero < -a := by
  have h1 := sub_pos_of_lt h
  rw [sub_def, zero_add] at h1
  exact h1

theorem zero_lt_one : (zero : F) < one := by
  rcases lt_trichotomy (zero : F) (one : F) with h | h | h
  · exact h
  · exact False.elim (zero_ne_one h)
  · have hn : (zero : F) < -(one : F) := neg_pos_of_neg h
    have hp : (zero : F) < (-(one : F)) * (-(one : F)) := mul_pos (-(one : F)) (-(one : F)) hn hn
    rw [neg_mul_neg, one_mul] at hp
    exact hp

theorem mul_lt_mul_of_pos_left {a b c : F} (h : a < b) (hc : zero < c) : c * a < c * b := by
  apply lt_of_sub_pos
  have hsub : c * b - c * a = c * (b - a) := by
    rw [sub_def, sub_def, left_distrib, mul_neg_eq_neg_mul_symm]
  rw [hsub]
  exact mul_pos c (b - a) hc (sub_pos_of_lt h)

theorem mul_lt_mul_of_pos_right {a b c : F} (h : a < b) (hc : zero < c) : a * c < b * c := by
  rw [mul_comm a c, mul_comm b c]
  exact mul_lt_mul_of_pos_left h hc

theorem mul_nonneg {a b : F} (ha : zero ≤ a) (hb : zero ≤ b) : zero ≤ a * b := by
  rw [le_def] at ha hb ⊢
  cases ha with
  | inl ha_pos =>
    cases hb with
    | inl hb_pos => exact Or.inl (mul_pos a b ha_pos hb_pos)
    | inr hb_zero => rw [← hb_zero, mul_zero]; exact Or.inr rfl
  | inr ha_zero =>
    rw [← ha_zero, zero_mul]
    exact Or.inr rfl

theorem mul_eq_zero {a b : F} (h : a * b = zero) : a = zero ∨ b = zero := by
  rcases lt_trichotomy a zero with ha | ha | ha
  · have hna : a ≠ zero := ne_of_lt ha
    have h1 : a⁻¹ * (a * b) = a⁻¹ * zero := congrArg (fun x => a⁻¹ * x) h
    rw [← mul_assoc, inv_mul_cancel hna, one_mul, mul_zero] at h1
    exact Or.inr h1
  · exact Or.inl ha
  · have hna : a ≠ zero := ne_of_gt ha
    have h1 : a⁻¹ * (a * b) = a⁻¹ * zero := congrArg (fun x => a⁻¹ * x) h
    rw [← mul_assoc, inv_mul_cancel hna, one_mul, mul_zero] at h1
    exact Or.inr h1

theorem mul_left_cancel_pos {m x y : F} (hm : zero < m) (h : m * x = m * y) : x = y := by
  have hmNe : m ≠ zero := ne_of_gt hm
  have hInv : m⁻¹ * (m * x) = m⁻¹ * (m * y) := congrArg (fun z => m⁻¹ * z) h
  rw [← mul_assoc, inv_mul_cancel hmNe, one_mul, ← mul_assoc, inv_mul_cancel hmNe, one_mul] at hInv
  exact hInv

theorem inv_pos_of_pos {a : F} (ha : zero < a) : zero < a⁻¹ := by
  have hna : a ≠ zero := ne_of_gt ha
  rcases lt_trichotomy zero (a⁻¹) with h | h | h
  · exact h
  · have h1 : a * a⁻¹ = one := mul_inv_cancel a hna
    rw [← h, mul_zero] at h1
    exact False.elim (zero_ne_one h1)
  · have hn : zero < -(a⁻¹) := neg_pos_of_neg h
    have hp : zero < a * (-(a⁻¹)) := mul_pos a (-(a⁻¹)) ha hn
    rw [mul_neg_eq_neg_mul_symm, mul_inv_cancel a hna] at hp
    have hadd := add_lt_add_right hp one
    rw [zero_add, add_left_neg] at hadd
    exact False.elim (lt_asymm zero_lt_one hadd)

theorem sq_pos_of_ne_zero {a : F} (ha : a ≠ zero) : zero < a * a := by
  rcases lt_trichotomy zero a with h | h | h
  · exact mul_pos a a h h
  · exact False.elim (ha h.symm)
  · have hn : zero < -a := neg_pos_of_neg h
    have hp := mul_pos (-a) (-a) hn hn
    rw [neg_mul_neg] at hp
    exact hp

theorem sq_eq_zero_iff {a : F} : a * a = zero ↔ a = zero := by
  constructor
  · intro h
    cases mul_eq_zero h with
    | inl h1 => exact h1
    | inr h2 => exact h2
  · intro h
    rw [h, zero_mul]

/-- If `0 < M1 < M2` and `0 < A1 < A2`, then `M1 * A1 < M2 * A2`. -/
theorem mul_lt_mul_of_pos_of_lt {M1 M2 A1 A2 : F}
    (hM1 : zero < M1) (hA1 : zero < A1)
    (hM : M1 < M2) (hA : A1 < A2) :
    M1 * A1 < M2 * A2 := by
  have hM2 : zero < M2 := lt_trans zero M1 M2 hM1 hM
  have step1 : M1 * A1 < M2 * A1 := mul_lt_mul_of_pos_right hM hA1
  have step2 : M2 * A1 < M2 * A2 := mul_lt_mul_of_pos_left hA hM2
  exact lt_trans (M1 * A1) (M2 * A1) (M2 * A2) step1 step2

end GeneralTheorems
end OrderedField

/-!
  ### Constructive Rational Field `QRat`
  Built directly on Lean 4's `Int` via positive-denominator pairs modulo cross-multiplication.
-/

structure RawRat where
  num : Int
  den : Int
  den_pos : 0 < den

namespace RawRat

def Equiv (a b : RawRat) : Prop :=
  a.num * b.den = b.num * a.den

theorem equiv_refl (a : RawRat) : Equiv a a := rfl

theorem equiv_symm {a b : RawRat} (h : Equiv a b) : Equiv b a := h.symm

theorem equiv_trans {a b c : RawRat} (hab : Equiv a b) (hbc : Equiv b c) : Equiv a c := by
  unfold Equiv at *
  have hb_ne : b.den ≠ 0 := by
    have hp := b.den_pos
    omega
  apply Int.eq_of_mul_eq_mul_right hb_ne
  calc
    a.num * c.den * b.den
      = (a.num * b.den) * c.den := by
          rw [Int.mul_assoc, Int.mul_comm c.den b.den, ← Int.mul_assoc]
    _ = (b.num * a.den) * c.den := by rw [hab]
    _ = (b.num * c.den) * a.den := by
          rw [Int.mul_assoc, Int.mul_comm a.den c.den, ← Int.mul_assoc]
    _ = (c.num * b.den) * a.den := by rw [hbc]
    _ = c.num * a.den * b.den := by
          rw [Int.mul_assoc, Int.mul_comm b.den a.den, ← Int.mul_assoc]

instance rawRatSetoid : Setoid RawRat where
  r := Equiv
  iseqv := ⟨equiv_refl, equiv_symm, equiv_trans⟩

def zero : RawRat := ⟨0, 1, by decide⟩
def one  : RawRat := ⟨1, 1, by decide⟩

def add (a b : RawRat) : RawRat :=
  ⟨a.num * b.den + b.num * a.den, a.den * b.den, Int.mul_pos a.den_pos b.den_pos⟩

def neg (a : RawRat) : RawRat :=
  ⟨-a.num, a.den, a.den_pos⟩

def mul (a b : RawRat) : RawRat :=
  ⟨a.num * b.num, a.den * b.den, Int.mul_pos a.den_pos b.den_pos⟩

def inv (a : RawRat) : RawRat :=
  if hpos : 0 < a.num then
    ⟨a.den, a.num, hpos⟩
  else if hneg : a.num < 0 then
    ⟨-a.den, -a.num, by omega⟩
  else
    ⟨0, 1, by decide⟩

def ltProp (a b : RawRat) : Prop :=
  a.num * b.den < b.num * a.den

private theorem ac_swap (x y z : Int) : x * y * z = x * z * y := by
  rw [Int.mul_assoc, Int.mul_comm y z, ← Int.mul_assoc]

private theorem four_prod (a b c d : Int) : (a * b) * (c * d) = (a * c) * (b * d) := by
  calc
    (a * b) * (c * d) = a * (b * (c * d)) := by rw [Int.mul_assoc]
    _ = a * ((b * c) * d) := by rw [← Int.mul_assoc b c d]
    _ = a * ((c * b) * d) := by rw [Int.mul_comm b c]
    _ = a * (c * (b * d)) := by rw [Int.mul_assoc c b d]
    _ = (a * c) * (b * d) := by rw [← Int.mul_assoc]

theorem add_resp {a1 a2 b1 b2 : RawRat} (ha : Equiv a1 a2) (hb : Equiv b1 b2) :
    Equiv (add a1 b1) (add a2 b2) := by
  unfold Equiv add at *
  dsimp
  rw [Int.add_mul, Int.add_mul]
  have t1 : a1.num * b1.den * (a2.den * b2.den) = a2.num * b2.den * (a1.den * b1.den) := by
    calc
      a1.num * b1.den * (a2.den * b2.den)
        = (a1.num * a2.den) * (b1.den * b2.den) := four_prod a1.num b1.den a2.den b2.den
      _ = (a2.num * a1.den) * (b2.den * b1.den) := by rw [ha, Int.mul_comm b1.den b2.den]
      _ = a2.num * b2.den * (a1.den * b1.den) := (four_prod a2.num b2.den a1.den b1.den).symm
  have t2 : b1.num * a1.den * (a2.den * b2.den) = b2.num * a2.den * (a1.den * b1.den) := by
    calc
      b1.num * a1.den * (a2.den * b2.den)
        = (b1.num * b2.den) * (a1.den * a2.den) := by
            rw [Int.mul_comm a2.den b2.den]
            exact four_prod b1.num a1.den b2.den a2.den
      _ = (b2.num * b1.den) * (a2.den * a1.den) := by rw [hb, Int.mul_comm a1.den a2.den]
      _ = b2.num * a2.den * (a1.den * b1.den) := by
            rw [Int.mul_comm a1.den b1.den]
            exact (four_prod b2.num a2.den b1.den a1.den).symm
  rw [t1, t2]

theorem neg_resp {a1 a2 : RawRat} (ha : Equiv a1 a2) : Equiv (neg a1) (neg a2) := by
  unfold Equiv neg at *
  dsimp
  rw [Int.neg_mul, Int.neg_mul, ha]

theorem mul_resp {a1 a2 b1 b2 : RawRat} (ha : Equiv a1 a2) (hb : Equiv b1 b2) :
    Equiv (mul a1 b1) (mul a2 b2) := by
  unfold Equiv mul at *
  dsimp
  calc
    (a1.num * b1.num) * (a2.den * b2.den)
      = (a1.num * a2.den) * (b1.num * b2.den) := four_prod a1.num b1.num a2.den b2.den
    _ = (a2.num * a1.den) * (b2.num * b1.den) := by rw [ha, hb]
    _ = (a2.num * b2.num) * (a1.den * b1.den) := (four_prod a2.num b2.num a1.den b1.den).symm

theorem inv_resp {a1 a2 : RawRat} (ha : Equiv a1 a2) : Equiv (inv a1) (inv a2) := by
  unfold Equiv inv at *
  have hd1 : 0 < a1.den := a1.den_pos
  have hd2 : 0 < a2.den := a2.den_pos
  by_cases hp1 : 0 < a1.num
  · have hp2 : 0 < a2.num := by
      have hprod : 0 < a1.num * a2.den := Int.mul_pos hp1 hd2
      rw [ha] at hprod
      rcases Int.lt_trichotomy 0 a2.num with h | h | h
      · exact h
      · rw [← h, Int.zero_mul] at hprod; omega
      · have hneg : a2.num * a1.den < 0 := Int.mul_neg_of_neg_of_pos h hd1
        omega
    simp only [hp1, hp2, ↓reduceDIte]
    calc
      a1.den * a2.num = a2.num * a1.den := Int.mul_comm a1.den a2.num
      _ = a1.num * a2.den := ha.symm
      _ = a2.den * a1.num := Int.mul_comm a1.num a2.den
  · by_cases hn1 : a1.num < 0
    · have hn2 : a2.num < 0 := by
        have hprod : a1.num * a2.den < 0 := Int.mul_neg_of_neg_of_pos hn1 hd2
        rw [ha] at hprod
        rcases Int.lt_trichotomy a2.num 0 with h | h | h
        · exact h
        · rw [h, Int.zero_mul] at hprod; omega
        · have hpos : 0 < a2.num * a1.den := Int.mul_pos h hd1
          omega
      have hnp2 : ¬ (0 < a2.num) := by omega
      simp only [hp1, hn1, hnp2, hn2, ↓reduceDIte]
      rw [Int.neg_mul_neg, Int.neg_mul_neg]
      calc
        a1.den * a2.num = a2.num * a1.den := Int.mul_comm a1.den a2.num
        _ = a1.num * a2.den := ha.symm
        _ = a2.den * a1.num := Int.mul_comm a1.num a2.den
    · have hz1 : a1.num = 0 := by omega
      rw [hz1, Int.zero_mul] at ha
      have hz2 : a2.num = 0 := by
        rcases Int.lt_trichotomy a2.num 0 with h | h | h
        · have hneg := Int.mul_neg_of_neg_of_pos h hd1; omega
        · exact h
        · have hpos := Int.mul_pos h hd1; omega
      have hnp2 : ¬ (0 < a2.num) := by omega
      have hnn2 : ¬ (a2.num < 0) := by omega
      simp only [hp1, hn1, hnp2, hnn2, ↓reduceDIte]

theorem lt_imp {a1 a2 b1 b2 : RawRat} (ha : Equiv a1 a2) (hb : Equiv b1 b2)
    (hlt : ltProp a1 b1) : ltProp a2 b2 := by
  unfold Equiv ltProp at *
  have hd : 0 < a1.den * b1.den := Int.mul_pos a1.den_pos b1.den_pos
  have hd2 : 0 < a2.den * b2.den := Int.mul_pos a2.den_pos b2.den_pos
  have hscaled : (a1.num * b1.den) * (a2.den * b2.den) < (b1.num * a1.den) * (a2.den * b2.den) :=
    Int.mul_lt_mul_of_pos_right hlt hd2
  have lhs_eq : (a1.num * b1.den) * (a2.den * b2.den) = (a2.num * b2.den) * (a1.den * b1.den) := by
    calc
      (a1.num * b1.den) * (a2.den * b2.den)
        = (a1.num * a2.den) * (b1.den * b2.den) := four_prod a1.num b1.den a2.den b2.den
      _ = (a2.num * a1.den) * (b2.den * b1.den) := by rw [ha, Int.mul_comm b1.den b2.den]
      _ = (a2.num * b2.den) * (a1.den * b1.den) := (four_prod a2.num b2.den a1.den b1.den).symm
  have rhs_eq : (b1.num * a1.den) * (a2.den * b2.den) = (b2.num * a2.den) * (a1.den * b1.den) := by
    calc
      (b1.num * a1.den) * (a2.den * b2.den)
        = (b1.num * b2.den) * (a1.den * a2.den) := by
            rw [Int.mul_comm a2.den b2.den]
            exact four_prod b1.num a1.den b2.den a2.den
      _ = (b2.num * b1.den) * (a2.den * a1.den) := by rw [hb, Int.mul_comm a1.den a2.den]
      _ = (b2.num * a2.den) * (a1.den * b1.den) := by
            rw [Int.mul_comm a1.den b1.den]
            exact (four_prod b2.num a2.den b1.den a1.den).symm
  rw [lhs_eq, rhs_eq] at hscaled
  rcases Int.lt_trichotomy (a2.num * b2.den) (b2.num * a2.den) with h | h | h
  · exact h
  · rw [h] at hscaled; omega
  · have hcontra := Int.mul_lt_mul_of_pos_right h hd
    omega

theorem lt_resp {a1 a2 b1 b2 : RawRat} (ha : Equiv a1 a2) (hb : Equiv b1 b2) :
    ltProp a1 b1 = ltProp a2 b2 :=
  propext ⟨lt_imp ha hb, lt_imp ha.symm hb.symm⟩

end RawRat

/-- Exact Rational Field `QRat := Quotient RawRat.rawRatSetoid`. -/
abbrev QRat := Quotient RawRat.rawRatSetoid

namespace QRat

def mkRat (n : Int) (d : Int) (hd : 0 < d) : QRat :=
  Quotient.mk _ ⟨n, d, hd⟩

def ofInt (n : Int) : QRat :=
  mkRat n 1 (by decide)

def zero : QRat := Quotient.mk _ RawRat.zero
def one  : QRat := Quotient.mk _ RawRat.one

def add : QRat → QRat → QRat :=
  Quotient.lift₂ (fun a b => Quotient.mk _ (RawRat.add a b))
    (fun _ _ _ _ ha hb => Quotient.sound (RawRat.add_resp ha hb))

def neg : QRat → QRat :=
  Quotient.lift (fun a => Quotient.mk _ (RawRat.neg a))
    (fun _ _ ha => Quotient.sound (RawRat.neg_resp ha))

def sub (a b : QRat) : QRat := add a (neg b)

def mul : QRat → QRat → QRat :=
  Quotient.lift₂ (fun a b => Quotient.mk _ (RawRat.mul a b))
    (fun _ _ _ _ ha hb => Quotient.sound (RawRat.mul_resp ha hb))

def inv : QRat → QRat :=
  Quotient.lift (fun a => Quotient.mk _ (RawRat.inv a))
    (fun _ _ ha => Quotient.sound (RawRat.inv_resp ha))

def lt : QRat → QRat → Prop :=
  Quotient.lift₂ RawRat.ltProp (fun _ _ _ _ ha hb => RawRat.lt_resp ha hb)

def le (a b : QRat) : Prop := lt a b ∨ a = b

instance : Add QRat := ⟨add⟩
instance : Sub QRat := ⟨sub⟩
instance : Neg QRat := ⟨neg⟩
instance : Mul QRat := ⟨mul⟩
instance : Inv QRat := ⟨inv⟩
instance : LT QRat  := ⟨lt⟩
instance : LE QRat  := ⟨le⟩

private theorem add_assoc_q (a b c : QRat) : a + b + c = a + (b + c) := by
  refine Quotient.inductionOn₃ a b c (fun x y z => Quotient.sound ?_)
  change RawRat.Equiv _ _
  unfold RawRat.Equiv RawRat.add
  dsimp
  have h1 : (x.num * y.den + y.num * x.den) * z.den + z.num * (x.den * y.den)
          = x.num * (y.den * z.den) + (y.num * z.den + z.num * y.den) * x.den := by
    rw [Int.add_mul, Int.add_mul, Int.mul_assoc x.num y.den z.den]
    rw [Int.mul_assoc y.num x.den z.den, Int.mul_comm x.den z.den, ← Int.mul_assoc y.num z.den x.den]
    rw [Int.mul_comm x.den y.den, ← Int.mul_assoc z.num y.den x.den]
    rw [Int.add_assoc]
  have h2 : x.den * y.den * z.den = x.den * (y.den * z.den) := Int.mul_assoc _ _ _
  rw [h1, h2]

private theorem add_comm_q (a b : QRat) : a + b = b + a := by
  refine Quotient.inductionOn₂ a b (fun x y => Quotient.sound ?_)
  change RawRat.Equiv _ _
  unfold RawRat.Equiv RawRat.add
  dsimp
  rw [Int.add_comm (x.num * y.den) (y.num * x.den), Int.mul_comm x.den y.den]

private theorem zero_add_q (a : QRat) : zero + a = a := by
  refine Quotient.inductionOn a (fun x => Quotient.sound ?_)
  change RawRat.Equiv _ _
  unfold RawRat.Equiv RawRat.add RawRat.zero
  dsimp
  rw [Int.zero_mul, Int.zero_add, Int.mul_one, Int.one_mul]

private theorem add_left_neg_q (a : QRat) : (-a) + a = zero := by
  refine Quotient.inductionOn a (fun x => Quotient.sound ?_)
  change RawRat.Equiv _ _
  unfold RawRat.Equiv RawRat.add RawRat.neg RawRat.zero
  dsimp
  rw [Int.neg_mul, Int.add_left_neg, Int.zero_mul, Int.zero_mul]

private theorem mul_assoc_q (a b c : QRat) : a * b * c = a * (b * c) := by
  refine Quotient.inductionOn₃ a b c (fun x y z => Quotient.sound ?_)
  change RawRat.Equiv _ _
  unfold RawRat.Equiv RawRat.mul
  dsimp
  rw [Int.mul_assoc x.num y.num z.num, Int.mul_assoc x.den y.den z.den]

private theorem mul_comm_q (a b : QRat) : a * b = b * a := by
  refine Quotient.inductionOn₂ a b (fun x y => Quotient.sound ?_)
  change RawRat.Equiv _ _
  unfold RawRat.Equiv RawRat.mul
  dsimp
  rw [Int.mul_comm x.num y.num, Int.mul_comm x.den y.den]

private theorem one_mul_q (a : QRat) : one * a = a := by
  refine Quotient.inductionOn a (fun x => Quotient.sound ?_)
  change RawRat.Equiv _ _
  unfold RawRat.Equiv RawRat.mul RawRat.one
  dsimp
  rw [Int.one_mul, Int.one_mul]

private theorem left_distrib_q (a b c : QRat) : a * (b + c) = a * b + a * c := by
  refine Quotient.inductionOn₃ a b c (fun x y z => Quotient.sound ?_)
  change RawRat.Equiv _ _
  unfold RawRat.Equiv RawRat.mul RawRat.add
  dsimp
  calc
    x.num * (y.num * z.den + z.num * y.den) * (x.den * y.den * (x.den * z.den))
      = (x.num * (y.num * z.den) + x.num * (z.num * y.den)) * ((x.den * x.den) * (y.den * z.den)) := by
          rw [Int.mul_add, RawRat.four_prod x.den y.den x.den z.den]
    _ = ((x.num * y.num) * (x.den * z.den) + (x.num * z.num) * (x.den * y.den)) * (x.den * (y.den * z.den)) := by
          have lhs1 : (x.num * (y.num * z.den) + x.num * (z.num * y.den)) * ((x.den * x.den) * (y.den * z.den))
                    = (x.num * (y.num * z.den) * x.den + x.num * (z.num * y.den) * x.den) * (x.den * (y.den * z.den)) := by
            rw [Int.mul_assoc x.den x.den (y.den * z.den), ← Int.mul_assoc _ x.den (x.den * (y.den * z.den)), Int.add_mul]
          rw [lhs1]
          have p1 : x.num * (y.num * z.den) * x.den = (x.num * y.num) * (x.den * z.den) := by
            rw [← Int.mul_assoc x.num y.num z.den, Int.mul_assoc (x.num * y.num) z.den x.den, Int.mul_comm z.den x.den]
          have p2 : x.num * (z.num * y.den) * x.den = (x.num * z.num) * (x.den * y.den) := by
            rw [← Int.mul_assoc x.num z.num y.den, Int.mul_assoc (x.num * z.num) y.den x.den, Int.mul_comm y.den x.den]
          rw [p1, p2]

private theorem mul_inv_cancel_q (a : QRat) (h : a ≠ zero) : a * a⁻¹ = one := by
  refine Quotient.inductionOn a (fun x => ?_) h
  intro hne
  apply Quotient.sound
  change RawRat.Equiv _ _
  unfold RawRat.Equiv RawRat.mul RawRat.inv RawRat.one
  have hx_ne : x.num ≠ 0 := by
    intro hz
    apply hne
    apply Quotient.sound
    change RawRat.Equiv _ _
    unfold RawRat.Equiv RawRat.zero
    dsimp
    omega
  by_cases hp : 0 < x.num
  · simp only [hp, ↓reduceDIte]
    rw [Int.mul_one, Int.one_mul, Int.mul_comm]
  · have hn : x.num < 0 := by omega
    simp only [hp, hn, ↓reduceDIte]
    rw [Int.mul_one, Int.one_mul, Int.mul_neg, Int.mul_neg, Int.mul_comm]

private theorem zero_ne_one_q : (zero : QRat) ≠ one := by
  intro h
  have heq : RawRat.Equiv RawRat.zero RawRat.one := Quotient.exact h
  unfold RawRat.Equiv RawRat.zero RawRat.one at heq
  dsimp at heq
  omega

private theorem lt_irrefl_q (a : QRat) : ¬ (a < a) := by
  refine Quotient.inductionOn a (fun x => ?_)
  change ¬ RawRat.ltProp x x
  unfold RawRat.ltProp
  omega

private theorem lt_trans_q (a b c : QRat) : a < b → b < c → a < c := by
  refine Quotient.inductionOn₃ a b c (fun x y z hxy hyz => ?_)
  change RawRat.ltProp x y at hxy
  change RawRat.ltProp y z at hyz
  change RawRat.ltProp x z
  unfold RawRat.ltProp at *
  have h1 : (x.num * y.den) * z.den < (y.num * x.den) * z.den :=
    Int.mul_lt_mul_of_pos_right hxy z.den_pos
  have h2 : (y.num * z.den) * x.den < (z.num * y.den) * x.den :=
    Int.mul_lt_mul_of_pos_right hyz x.den_pos
  have eq1 : (y.num * x.den) * z.den = (y.num * z.den) * x.den := by
    rw [Int.mul_assoc, Int.mul_comm x.den z.den, ← Int.mul_assoc]
  rw [eq1] at h1
  have h3 : (x.num * y.den) * z.den < (z.num * y.den) * x.den := Int.lt_trans h1 h2
  have lhs_eq : (x.num * y.den) * z.den = (x.num * z.den) * y.den := by
    rw [Int.mul_assoc, Int.mul_comm y.den z.den, ← Int.mul_assoc]
  have rhs_eq : (z.num * y.den) * x.den = (z.num * x.den) * y.den := by
    rw [Int.mul_assoc, Int.mul_comm y.den x.den, ← Int.mul_assoc]
  rw [lhs_eq, rhs_eq] at h3
  rcases Int.lt_trichotomy (x.num * z.den) (z.num * x.den) with h | h | h
  · exact h
  · rw [h] at h3; omega
  · have hc := Int.mul_lt_mul_of_pos_right h y.den_pos; omega

private theorem lt_trichotomy_q (a b : QRat) : a < b ∨ a = b ∨ b < a := by
  refine Quotient.inductionOn₂ a b (fun x y => ?_)
  rcases Int.lt_trichotomy (x.num * y.den) (y.num * x.den) with h | h | h
  · exact Or.inl h
  · exact Or.inr (Or.inl (Quotient.sound h))
  · exact Or.inr (Or.inr h)

private theorem add_lt_add_left_q (a b : QRat) (hab : a < b) (c : QRat) : c + a < c + b := by
  refine Quotient.inductionOn₃ a b c (fun x y z hxy => ?_) hab
  change RawRat.ltProp x y at hxy
  change RawRat.ltProp (RawRat.add z x) (RawRat.add z y)
  unfold RawRat.ltProp RawRat.add at *
  dsimp
  rw [Int.add_mul, Int.add_mul]
  have eqL : z.num * x.den * (z.den * y.den) = z.num * y.den * (z.den * x.den) := by
    calc
      z.num * x.den * (z.den * y.den)
        = (z.num * z.den) * (x.den * y.den) := RawRat.four_prod z.num x.den z.den y.den
      _ = (z.num * z.den) * (y.den * x.den) := by rw [Int.mul_comm x.den y.den]
      _ = z.num * y.den * (z.den * x.den) := (RawRat.four_prod z.num y.den z.den x.den).symm
  rw [eqL]
  have hzz : 0 < z.den * z.den := Int.mul_pos z.den_pos z.den_pos
  have hscaled : (x.num * y.den) * (z.den * z.den) < (y.num * x.den) * (z.den * z.den) :=
    Int.mul_lt_mul_of_pos_right hxy hzz
  have eqR1 : x.num * z.den * (z.den * y.den) = (x.num * y.den) * (z.den * z.den) := by
    rw [Int.mul_comm z.den y.den]
    exact RawRat.four_prod x.num z.den y.den z.den
  have eqR2 : y.num * z.den * (z.den * x.den) = (y.num * x.den) * (z.den * z.den) := by
    rw [Int.mul_comm z.den x.den]
    exact RawRat.four_prod y.num z.den x.den z.den
  rw [eqR1, eqR2]
  omega

private theorem mul_pos_q (a b : QRat) (ha : zero < a) (hb : zero < b) : zero < a * b := by
  refine Quotient.inductionOn₂ a b (fun x y hx hy => ?_) ha hb
  change RawRat.ltProp RawRat.zero x at hx
  change RawRat.ltProp RawRat.zero y at hy
  change RawRat.ltProp RawRat.zero (RawRat.mul x y)
  unfold RawRat.ltProp RawRat.zero RawRat.mul at *
  dsimp at *
  have hxpos : 0 < x.num := by omega
  have hypos : 0 < y.num := by omega
  have hprod : 0 < x.num * y.num := Int.mul_pos hxpos hypos
  omega

instance : OrderedField QRat where
  zero := zero
  one := one
  sub_def := fun _ _ => rfl
  le_def := fun _ _ => Iff.rfl
  add_assoc := add_assoc_q
  add_comm := add_comm_q
  zero_add := zero_add_q
  add_left_neg := add_left_neg_q
  mul_assoc := mul_assoc_q
  mul_comm := mul_comm_q
  one_mul := one_mul_q
  left_distrib := left_distrib_q
  mul_inv_cancel := mul_inv_cancel_q
  zero_ne_one := zero_ne_one_q
  lt_irrefl := lt_irrefl_q
  lt_trans := lt_trans_q
  lt_trichotomy := lt_trichotomy_q
  add_lt_add_left := add_lt_add_left_q
  mul_pos := mul_pos_q

end QRat
end TSR
