import Lake
open Lake DSL

package «tsr_proof» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]

@[default_target]
lean_lib «TSR» where
  globs := #[.submodules `TSR, .one `TSR]
