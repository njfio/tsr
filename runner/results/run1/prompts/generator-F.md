ROLE: generator

You're helping test a framework called the Theory of Sovereign Reflectivity (TSR). TSR reflects physics onto a "nonphysical" side using one rule. Your job is to apply the rule, exactly as written below, to each of the physics relations below, one at a time, and to report honestly where the result holds up and where it doesn't.

Ground rules:

- Use only the material in this prompt. Don't search the web. If you know anything else about TSR, set it aside, and say so in the `knew_tsr` field.
- Be strict, not generous. A reflection that reads as nonsense in TSR's own terms is a useful result. Don't rescue it with creative reinterpretation.
- The vocabulary below is frozen. If a physical term has no partner, say so in `unmapped_terms`. Any word you introduce goes in `new_words`, and a row with new words is recorded as "no partner".
- Apply the rule as stated, even where you think it's wrong. Put your disagreement in `closing`, never in the reflection.
- Do not rewrite the formula. A relation that turns around keeps its formula in the table's terms; what turns is its reading (harder becomes easier, unreachable becomes already there).

## The rule

> "Keep each relationship, and flip the condition. Resistant becomes receptive, limited becomes limitless, radiating becomes collecting. ... Every term reflects; that part always happens. What you have to know is whether the relationship keeps its shape or turns around."

The deciding question: "One is an equivalence. The other is a cost that rises with resistance."

- Equivalences, definitions, identities, conservation laws and symmetries keep their shape.
- A cost or a limit caused by resistance turns around: what gets harder with more resistance gets easier with more receptivity. Mass is resistance, and distance is "what resistance makes." A separation made by distance also turns around.
- A statement with an odd number of such costs turns around; with none or an even number it keeps.
- "Units don't cross the mirror, only relationships do." Nothing on the nonphysical side has a number, a unit or a distance.

## Which quantities carry resistance (fixed before this run)

- Planck constant: does not carry resistance — a constant
- barrier height: UNDETERMINED (a judgment call; say so) — a potential energy that opposes passage; physics defines it as energy, the tunneling relation treats it as what must be overcome. R does not decide it.
- barrier width: does not carry resistance — extent
- decoherence rate: does not carry resistance — a rate
- energy: does not carry resistance — shared by both sides of the mirror (one E)
- environment coupling: does not carry resistance — interaction strength
- frequency (physical): does not carry resistance — a rate; NB: not TSR Frequency
- interference visibility: does not carry resistance — a measure
- length: does not carry resistance — extent (separation is a relation-level feature)
- mass m: carries resistance — inertial mass is defined as opposition to a change in motion
- momentum: does not carry resistance — a conserved quantity, not an opposition
- probability: does not carry resistance — a measure
- quantum number: does not carry resistance — a count
- spin: does not carry resistance — intrinsic angular momentum
- time: does not carry resistance — a continuum coordinate
- wavefunction amplitude: does not carry resistance — an amplitude
- which-path information: does not carry resistance — a measure

## The frozen vocabulary

| Physical | Nonphysical | Map row |
| --- | --- | --- |
| limited | limitless | property |
| resistant | receptive | property |
| radiation | collection | property |
| Subjective Reality | Vibrational Reality | reality |
| Objective Reality | Collective Reality | reality |
| Space-Time | Vibration-Expansion | continuum |
| empirical evidence | emotional evidence | evidence |
| Now | Future | energy flow |
| Past | Current | energy flow |
| Belief | Desire | entity contrast |
| Expectation | Intuition | entity contrast |
| speed of light c | Current | symbol |
| mass m | Movement M | symbol |
| Focus | Tune | entity action |
| electric | Idle | co-creating partner |
| magnetic | Reflected | co-creating partner |
| density | Desire | co-creating partner |
| volume | Vibrance | co-creating partner |
| physical energy | conscious energy | energy |
| actualization | realization | transmutation |
| Out Through | Out For | entity transmutation |
| In From | In To | entity transmutation |
| space | Vibration | reflected partnership |
| time | Expansion | reflected partnership |
| velocity | rise per Expansion | reflected partnership |
| acceleration | Appreciation | reflected partnership |
| manifestation | imagination | reflected partnership |
| force | Frequency | reflected partnership |
| gravitational pull | Attraction | gravity |
| gravity well | Vortex | gravity |
| gravitational lensing | Convergence | gravity |
| time dilation | Expansion Dilation | named reflection |
| length contraction | Vibrational Contraction | named reflection |
| friction | resonance | named reflection |
| entropy | Culmination (provisional) | named reflection |
| momentum | momentum | momentum |

Other legal nonphysical words: alignment (how little you resist; the nonphysical measure of nearness to the Current), receptivity (the flipped condition), the gap (resistance's only appearance on the nonphysical side: between the Current and what you're living), Point of Reflection (center of the crossing; where energy changes form), the Present (the whole equation C^2 x M = E = m x c^2), E (the one energy / the entity, shared by both sides), Awareness (limitless and limited met), Attraction (receptive and resistant met (entity property) and gravity's reflection), Momentum (collecting and radiating met), wanting (Desire in plain speech), culminate (verb of Culmination; what two vibrations do instead of cancel (Ch 16)), strong frequency (Desire), weak frequency (Intuition and imagination)

Words that must never appear on the nonphysical side: boundary, distance, edge, effort, inside, judgment, location, mental, mind, outside, place, radiate, radiates, radiating, rank, resistance, speed, time, travel, will.

## Traps (refuse each one)

- No distance, time, location, travel or quantities on the nonphysical side.
- No resistance on the nonphysical side; it appears only as the gap.
- No entity properties (Awareness, Momentum as a property) on things that are not entities.
- "Nonphysical" does not mean "mental".
- Frequency is not a rate and not cycles per second.
- No sums where the book has products.
- No physical words in disguise: belief, expectation, will, effort, judgment, rank belong to the physical side.

## The relations

Take each one on its own. Do not let one relation's reflection decide another's; the rule decides each.

### qm.born_rule
```yaml
{
  "id": "qm.born_rule",
  "title": "Born rule",
  "statement": "The probability of an outcome is the squared magnitude of its amplitude.",
  "formula": "P = |ψ|²",
  "form": "definition",
  "variables": [
    {
      "name": "probability P",
      "quantity": "probability",
      "carries_distance": false
    },
    {
      "name": "amplitude ψ",
      "quantity": "wavefunction amplitude",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### qm.bound_state_quantization
```yaml
{
  "id": "qm.bound_state_quantization",
  "title": "Quantization of bound states",
  "statement": "A particle confined to a region has only discrete allowed energies; the spacing grows as the region shrinks and falls as the particle's mass rises.",
  "formula": "E_n = n² × π² × ħ² ÷ (2 × m × L²)",
  "form": "equation",
  "variables": [
    {
      "name": "energy level E_n",
      "quantity": "energy",
      "carries_distance": false
    },
    {
      "name": "quantum number n",
      "quantity": "quantum number",
      "carries_distance": false
    },
    {
      "name": "mass m",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "confinement length L",
      "quantity": "length",
      "carries_distance": true
    },
    {
      "name": "Planck constant ħ",
      "quantity": "Planck constant",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "which energies are allowed: only those that fit the confinement",
      "rises_with": [],
      "falls_with": [
        "mass m"
      ],
      "separation_made_by_distance": true
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### qm.complementarity
```yaml
{
  "id": "qm.complementarity",
  "title": "Wave-particle complementarity",
  "statement": "The more which-path information an interferometer records, the less visible its interference fringes; the two trade off so that distinguishability squared plus visibility squared is at most one.",
  "formula": "D² + V² ≤ 1",
  "form": "inequality",
  "variables": [
    {
      "name": "which-path distinguishability D",
      "quantity": "which-path information",
      "carries_distance": false
    },
    {
      "name": "fringe visibility V",
      "quantity": "interference visibility",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### qm.decoherence
```yaml
{
  "id": "qm.decoherence",
  "title": "Decoherence",
  "statement": "Interaction with an environment spreads a system's phase relations into degrees of freedom no one can recover, suppressing interference; two branches of a superposition lose coherence faster the more strongly they couple to the environment and the farther apart in position they are.",
  "formula": "Γ ∝ Λ × (Δx)²",
  "form": "equation",
  "variables": [
    {
      "name": "decoherence rate Γ",
      "quantity": "decoherence rate",
      "carries_distance": false
    },
    {
      "name": "environment coupling Λ",
      "quantity": "environment coupling",
      "carries_distance": false
    },
    {
      "name": "branch separation Δx",
      "quantity": "length",
      "carries_distance": true
    }
  ],
  "costs": [
    {
      "what_gets_harder": "keeping two branches coherent",
      "rises_with": [
        "environment coupling"
      ],
      "falls_with": [],
      "separation_made_by_distance": true
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### qm.entanglement
```yaml
{
  "id": "qm.entanglement",
  "title": "Entanglement",
  "statement": "Measurements on two entangled particles are correlated more strongly than any local account allows (Bell), and the correlation does not weaken with their separation.",
  "formula": "",
  "form": "statistical",
  "variables": [
    {
      "name": "probability",
      "quantity": "probability",
      "carries_distance": false
    },
    {
      "name": "separation",
      "quantity": "length",
      "carries_distance": true
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### qm.measurement_collapse
```yaml
{
  "id": "qm.measurement_collapse",
  "title": "Measurement",
  "statement": "A measurement yields one of the observable's eigenvalues, and afterwards the system is in the corresponding eigenstate; which value appears is not determined by the prior state.",
  "formula": "",
  "form": "statistical",
  "variables": [
    {
      "name": "probability",
      "quantity": "probability",
      "carries_distance": false
    },
    {
      "name": "wavefunction amplitude",
      "quantity": "wavefunction amplitude",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### qm.no_cloning
```yaml
{
  "id": "qm.no_cloning",
  "title": "No-cloning",
  "statement": "No physical operation can make an independent copy of an arbitrary unknown quantum state.",
  "formula": "",
  "form": "limit",
  "variables": [
    {
      "name": "wavefunction amplitude",
      "quantity": "wavefunction amplitude",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### qm.pauli_exclusion
```yaml
{
  "id": "qm.pauli_exclusion",
  "title": "Pauli exclusion",
  "statement": "No two identical fermions can occupy the same quantum state; the many-body state is antisymmetric under exchange.",
  "formula": "",
  "form": "symmetry",
  "variables": [
    {
      "name": "spin",
      "quantity": "spin",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### qm.spin
```yaml
{
  "id": "qm.spin",
  "title": "Spin",
  "statement": "Particles carry an intrinsic angular momentum that is quantized in half-integer or integer multiples of the reduced Planck constant and is not a rotation in space.",
  "formula": "",
  "form": "definition",
  "variables": [
    {
      "name": "spin",
      "quantity": "spin",
      "carries_distance": false
    },
    {
      "name": "Planck constant ħ",
      "quantity": "Planck constant",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### qm.superposition
```yaml
{
  "id": "qm.superposition",
  "title": "Quantum superposition",
  "statement": "Any linear combination of allowed states is an allowed state; the state space is linear.",
  "formula": "",
  "form": "identity",
  "variables": [
    {
      "name": "wavefunction amplitude",
      "quantity": "wavefunction amplitude",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### qm.tunneling
```yaml
{
  "id": "qm.tunneling",
  "title": "Tunneling",
  "statement": "A particle can cross a barrier higher than its energy; the chance falls exponentially with the barrier's width, with the square root of its height above the particle's energy, and with the square root of the particle's mass.",
  "formula": "T ≈ exp(−2 × κ × d), κ = √(2 × m × (V − E)) ÷ ħ",
  "form": "equation",
  "variables": [
    {
      "name": "transmission T",
      "quantity": "probability",
      "carries_distance": false
    },
    {
      "name": "mass m",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "barrier height V",
      "quantity": "barrier height",
      "carries_distance": false
    },
    {
      "name": "barrier width d",
      "quantity": "barrier width",
      "carries_distance": false
    },
    {
      "name": "Planck constant ħ",
      "quantity": "Planck constant",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "getting through the barrier",
      "rises_with": [
        "mass m",
        "barrier height"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### qm.uncertainty_energy_time
```yaml
{
  "id": "qm.uncertainty_energy_time",
  "title": "Energy-time uncertainty",
  "statement": "A state that lasts only a short time has a correspondingly broad energy; the product of the energy spread and the lifetime is at least half the reduced Planck constant.",
  "formula": "ΔE × Δt ≥ ħ ÷ 2",
  "form": "inequality",
  "variables": [
    {
      "name": "energy spread ΔE",
      "quantity": "energy",
      "carries_distance": false
    },
    {
      "name": "lifetime Δt",
      "quantity": "time",
      "carries_distance": false
    },
    {
      "name": "Planck constant ħ",
      "quantity": "Planck constant",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### qm.uncertainty_position_momentum
```yaml
{
  "id": "qm.uncertainty_position_momentum",
  "title": "Position-momentum uncertainty",
  "statement": "The spreads of position and momentum in any state cannot both be made small: their product is at least half the reduced Planck constant.",
  "formula": "Δx × Δp ≥ ħ ÷ 2",
  "form": "inequality",
  "variables": [
    {
      "name": "position spread Δx",
      "quantity": "length",
      "carries_distance": false
    },
    {
      "name": "momentum spread Δp",
      "quantity": "momentum",
      "carries_distance": false
    },
    {
      "name": "Planck constant ħ",
      "quantity": "Planck constant",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### qm.zero_point_energy
```yaml
{
  "id": "qm.zero_point_energy",
  "title": "Zero-point energy",
  "statement": "The lowest energy of a bound system is not zero; an oscillator's ground state keeps half a quantum of energy.",
  "formula": "E0 = ½ × ħ × ω",
  "form": "limit",
  "variables": [
    {
      "name": "ground-state energy E0",
      "quantity": "energy",
      "carries_distance": false
    },
    {
      "name": "angular frequency ω",
      "quantity": "frequency (physical)",
      "carries_distance": false
    },
    {
      "name": "Planck constant ħ",
      "quantity": "Planck constant",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

## What to report
Return ONE JSON object with exactly these keys:

```json
{
  "id": "<the relation id>",
  "physical": "the relation as given",
  "reflected_formula": "the word-map image of the formula, in frozen words, with × ÷ and so on (empty if the relation has no formula)",
  "reflected_sentence": "one plain sentence",
  "shape": "keeps | turns around | no partner",
  "rule_reason": "equivalence or definition, or which cost or limit caused by resistance, or which separation",
  "rule_trace": ["which of these fired: identity, resistance-cost, separation, none"],
  "forced": true,
  "unmapped_terms": [],
  "new_words": [],
  "monotone_claims": [{"rises": "a frozen word", "with": "a frozen word or 'alignment'", "sign": 1}],
  "interpretation": "2 or 3 sentences, frozen words only",
  "conflicts": "any claim in the vocabulary table it contradicts, quoted, or \"none\"",
  "sense": 1,
  "confidence": 1,
  "closing": "one short paragraph: did the rule decide on its own, or did you need a judgment call? where was it ambiguous?",
  "knew_tsr": false
}
```

`forced` is true only if the rule decided without a judgment call. `sense` 1–7 (1 = nonsense in TSR's terms; 7 = coherent and says something the table doesn't). `confidence` 1–7 on the keeps-or-turns call.

Return a JSON ARRAY with one such object per relation, in the order given, and nothing else in the file. Write it to the file `runner/results/run1/raw/<MODEL>/batch-F.json` and then reply with the single word DONE. Do not read any other file, do not search the web, do not look at the repository.