/-
  TSR.lean
  ========
  Root entry point for Part I — Lean 4 formalization of selected structural models and
  algebraic consequences associated with *The Sovereign Mirror* (v57) and *What the Words
  Knew* (proof 36).

  Epistemic contract: theorems in this library establish deductive consequences (a) of
  explicit formalization modeling choices (c) together with standard physics and
  ordered-field algebra (b).
  Imports all five verified modules (`OrderedAlgebra`, `Condition`, `MirrorFunctor`,
  `Crossing`, `EntityAndMeta`) with zero `sorry` and zero external package dependencies.
-/

import TSR.OrderedAlgebra
import TSR.Condition
import TSR.MirrorFunctor
import TSR.Crossing
import TSR.EntityAndMeta
