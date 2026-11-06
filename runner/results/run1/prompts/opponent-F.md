ROLE: opponent

You are the opponent in a test of a reflection rule. Below are the rule, a frozen vocabulary, one physics relation, and the reading that a majority of independent generators produced for it. Your task: produce the STRONGEST reading in which the shape is the other way (keeps instead of turns around, or the reverse), using the same rule and only the frozen vocabulary.

You win only if your alternative is rule-compliant: it must name an equivalence (to keep) or a resistance-caused cost or distance-made separation actually present in the physics statement (to turn), without inventing physics, without new words, and without rewriting the formula. If no rule-compliant alternative exists, say so; that is the honest result and it is what the test needs.

Use only this prompt. If you know anything else about TSR, set it aside and say so in `knew_tsr`.

## The rule

Keep each relationship, and flip the condition. Equivalences, definitions, identities, conservation laws and symmetries keep their shape. A cost or a limit caused by resistance turns around; a separation made by distance turns around; an odd number of such costs turns around. Units don't cross the mirror.

## Which quantities carry resistance (fixed before this run)

- Planck constant: does not carry resistance — a constant
- decoherence rate: does not carry resistance — a rate
- energy: does not carry resistance — shared by both sides of the mirror (one E)
- environment coupling: does not carry resistance — interaction strength
- frequency (physical): does not carry resistance — a rate; NB: not TSR Frequency
- interference visibility: does not carry resistance — a measure
- length: does not carry resistance — extent (separation is a relation-level feature)
- momentum: does not carry resistance — a conserved quantity, not an opposition
- probability: does not carry resistance — a measure
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

## The relations and their majority readings

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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "[probability: no partner] = |[wavefunction amplitude: no partner]|²",
  "reflected_sentence": "How likely a realization is stays tied in the same way to the strength of the state that leads to it.",
  "rule_trace": [
    "C1"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "[which-path information: no partner]² + [interference visibility: no partner]² ≤ 1",
  "reflected_sentence": "The trade-off between telling two ways apart and seeing how they culminate together keeps its shape.",
  "rule_trace": [
    "C0"
  ]
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
Majority reading:
```json
{
  "shape": "turns around",
  "reflected_formula": "(rate, no partner) rises with (coupling, no partner) × the gap²",
  "reflected_sentence": "Two vibrations culminate more easily as the gap closes.",
  "rule_trace": [
    "C0"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "",
  "reflected_sentence": "Two vibrations that share one measure answer alike, and the nearness of their answering does not thin as the gap widens.",
  "rule_trace": [
    "C0"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "",
  "reflected_sentence": "What happens when a state is met keeps its shape: one realization appears and the state matches it, without the prior state fixing which one.",
  "rule_trace": [
    "C0"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "",
  "reflected_sentence": "The limit keeps its shape: nothing can make a second independent state out of an unknown one, because that limit does not come from the gap.",
  "rule_trace": [
    "C0"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "",
  "reflected_sentence": "The relationship governing exchange of what is identical keeps its shape.",
  "rule_trace": [
    "C1"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "",
  "reflected_sentence": "The definition keeps its shape: momentum that belongs to the thing itself is still momentum, and what is not a turning in space is not a turning in Vibration.",
  "rule_trace": [
    "C1"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "",
  "reflected_sentence": "The relationship allowing combinations of what is allowed keeps its shape.",
  "rule_trace": [
    "C1"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "",
  "reflected_sentence": "The product relationship concerning conscious energy and Expansion keeps its shape.",
  "rule_trace": [
    "C0"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "ΔVibration × Δmomentum ≥ ħ ÷ 2",
  "reflected_sentence": "The spreads of Vibration and of momentum in any state cannot both be made small.",
  "rule_trace": [
    "C0"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "",
  "reflected_sentence": "The relationship concerning conscious energy that remains keeps its shape.",
  "rule_trace": [
    "C0"
  ]
}
```

## Report

For each relation return one JSON object:

```json
{"id": "<the relation id>", "alternative_shape": "keeps | turns around | null", "rule_compliant": false, "argument": "the equivalence, cost or separation you rest on, in one or two sentences, or why none exists", "reflected_sentence": "your alternative sentence in frozen words, or empty", "knew_tsr": false}
```

Return a JSON ARRAY of these objects, one per relation, and nothing else. Write it to `runner/results/run1/raw/opponent/batch-F.json` and reply DONE. Do not read any other file, do not search the web, do not look at the repository.