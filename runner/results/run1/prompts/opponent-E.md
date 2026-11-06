ROLE: opponent

You are the opponent in a test of a reflection rule. Below are the rule, a frozen vocabulary, one physics relation, and the reading that a majority of independent generators produced for it. Your task: produce the STRONGEST reading in which the shape is the other way (keeps instead of turns around, or the reverse), using the same rule and only the frozen vocabulary.

You win only if your alternative is rule-compliant: it must name an equivalence (to keep) or a resistance-caused cost or distance-made separation actually present in the physics statement (to turn), without inventing physics, without new words, and without rewriting the formula. If no rule-compliant alternative exists, say so; that is the honest result and it is what the test needs.

Use only this prompt. If you know anything else about TSR, set it aside and say so in `knew_tsr`.

## The rule

Keep each relationship, and flip the condition. Equivalences, definitions, identities, conservation laws and symmetries keep their shape. A cost or a limit caused by resistance turns around; a separation made by distance turns around; an odd number of such costs turns around. Units don't cross the mirror.

## Which quantities carry resistance (fixed before this run)

- Poynting vector: does not carry resistance — an energy flux
- charge: does not carry resistance — a source / coupling strength; not defined as opposition. The book pairs electric and magnetic as co-creating partners, not as resistance. Decided under R before electromagnetism ran.
- current (electric): does not carry resistance — a flow
- electric field: does not carry resistance — force per charge
- electric flux: does not carry resistance — a field integral
- electrical resistance: carries resistance — defined as opposition to current (V / I)
- impedance: carries resistance — generalized opposition to alternating current
- inductance: carries resistance — opposition to a change in current (Lenz / Faraday)
- magnetic field: does not carry resistance — a field
- magnetic flux: does not carry resistance — a field integral
- permeability: does not carry resistance — a medium constant
- permittivity: does not carry resistance — a medium constant
- reactance: carries resistance — opposition to change of current or voltage
- speed of light c: does not carry resistance — the limit, not an opposition
- time: does not carry resistance — a continuum coordinate
- voltage: does not carry resistance — energy per charge

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

### em.displacement_current
```yaml
{
  "id": "em.displacement_current",
  "title": "Maxwell's displacement current",
  "statement": "A changing electric field acts as a source of magnetic field just as a current does, which closes the symmetry between the two fields and makes electromagnetic waves possible.",
  "formula": "∇ × B = μ0 × J + μ0 × ε0 × dE ÷ dt",
  "form": "symmetry",
  "variables": [
    {
      "name": "electric field E",
      "quantity": "electric field",
      "carries_distance": false
    },
    {
      "name": "magnetic field B",
      "quantity": "magnetic field",
      "carries_distance": false
    },
    {
      "name": "time t",
      "quantity": "time",
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
  "reflected_formula": "? × ? = ? × ? + ? × ? × d? ÷ dExpansion",
  "reflected_sentence": "The symmetry involving Idle, Reflected and Expansion keeps its shape, with the remaining partners unnamed.",
  "rule_trace": [
    "C1"
  ]
}
```

### em.faraday
```yaml
{
  "id": "em.faraday",
  "title": "Faraday's law",
  "statement": "A changing magnetic flux through a loop induces an electromotive force equal to the rate of change of the flux.",
  "formula": "EMF = dΦ_B ÷ dt",
  "form": "equation",
  "variables": [
    {
      "name": "electromotive force",
      "quantity": "voltage",
      "carries_distance": false
    },
    {
      "name": "magnetic flux Φ_B",
      "quantity": "magnetic flux",
      "carries_distance": false
    },
    {
      "name": "time t",
      "quantity": "time",
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
  "reflected_formula": "EMF = dReflected_flux ÷ dExpansion",
  "reflected_sentence": "A changing Reflected collection through a loop induces conscious energy per source equal to the change of that Reflected collection across Expansion.",
  "rule_trace": [
    "C0"
  ]
}
```

### em.gauss
```yaml
{
  "id": "em.gauss",
  "title": "Gauss's law",
  "statement": "The electric flux through any closed surface equals the enclosed charge divided by the permittivity of free space.",
  "formula": "Φ_E = Q ÷ ε0",
  "form": "identity",
  "variables": [
    {
      "name": "electric flux Φ_E",
      "quantity": "electric flux",
      "carries_distance": false
    },
    {
      "name": "enclosed charge Q",
      "quantity": "charge",
      "carries_distance": false
    },
    {
      "name": "permittivity ε0",
      "quantity": "permittivity",
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
  "reflected_formula": "[Idle flux: flux unmapped] = [charge: unmapped] ÷ [permittivity: unmapped]",
  "reflected_sentence": "The Idle gathered over any closed surface equals the enclosed source over the medium constant.",
  "rule_trace": [
    "C1"
  ]
}
```

### em.impedance
```yaml
{
  "id": "em.impedance",
  "title": "Impedance",
  "statement": "In an alternating-current circuit the ratio of voltage to current is the impedance, whose magnitude combines resistance with the inductive and capacitive reactances.",
  "formula": "|Z| = √(R² + (X_L − X_C)²)",
  "form": "definition",
  "variables": [
    {
      "name": "impedance Z",
      "quantity": "impedance",
      "carries_distance": false
    },
    {
      "name": "resistance R",
      "quantity": "electrical resistance",
      "carries_distance": false
    },
    {
      "name": "reactance X",
      "quantity": "reactance",
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
  "reflected_formula": "[impedance: unmapped] = √(the gap² + ([reactance_L: unmapped] − [reactance_C: unmapped])²)",
  "reflected_sentence": "The whole opposition met by an alternating flow combines the gap with the opposition to change, and, read receptively, the whole receptivity combines the same way.",
  "rule_trace": [
    "C1"
  ]
}
```

### em.lenz_inductance
```yaml
{
  "id": "em.lenz_inductance",
  "title": "Lenz's law and self-inductance",
  "statement": "An induced current flows so as to oppose the change that produced it; a coil opposes a change in its own current with a back-EMF proportional to its inductance.",
  "formula": "EMF = L × dI ÷ dt",
  "form": "equation",
  "variables": [
    {
      "name": "back-EMF",
      "quantity": "voltage",
      "carries_distance": false
    },
    {
      "name": "inductance L",
      "quantity": "inductance",
      "carries_distance": false
    },
    {
      "name": "current I",
      "quantity": "current (electric)",
      "carries_distance": false
    },
    {
      "name": "time t",
      "quantity": "time",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "changing the current",
      "rises_with": [
        "inductance"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
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
  "reflected_formula": "EMF = L × dI ÷ dExpansion",
  "reflected_sentence": "An induced flow moves to receive the change that produced it, so changing a flow across Expansion gets easier as receptivity and alignment rise.",
  "rule_trace": [
    "C0"
  ]
}
```

### em.mutual_induction
```yaml
{
  "id": "em.mutual_induction",
  "title": "Mutual induction",
  "statement": "A changing current in one coil induces an EMF in a nearby coil in proportion to their mutual inductance, which depends on their geometry and how much flux they share.",
  "formula": "EMF_2 = M × dI_1 ÷ dt",
  "form": "equation",
  "variables": [
    {
      "name": "induced EMF",
      "quantity": "voltage",
      "carries_distance": false
    },
    {
      "name": "mutual inductance M",
      "quantity": "inductance",
      "carries_distance": false
    },
    {
      "name": "current I_1",
      "quantity": "current (electric)",
      "carries_distance": false
    },
    {
      "name": "time t",
      "quantity": "time",
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
  "reflected_formula": "EMF_2 = M × dI_1 ÷ dExpansion",
  "reflected_sentence": "A changing flow across Expansion in one loop induces conscious energy per source in another loop in proportion to their shared coupling.",
  "rule_trace": [
    "C0"
  ]
}
```

### em.ohm_cost
```yaml
{
  "id": "em.ohm_cost",
  "title": "Ohm's law (the cost reading)",
  "statement": "For a given voltage, the current that flows falls as the resistance rises.",
  "formula": "I = V ÷ R",
  "form": "equation",
  "variables": [
    {
      "name": "resistance R",
      "quantity": "electrical resistance",
      "carries_distance": false
    },
    {
      "name": "voltage V",
      "quantity": "voltage",
      "carries_distance": false
    },
    {
      "name": "current I",
      "quantity": "current (electric)",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "current flowing for a given voltage",
      "rises_with": [
        "electrical resistance"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
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
  "reflected_formula": "I = V ÷ receptivity",
  "reflected_sentence": "For a given conscious energy per source, the flow that moves rises as receptivity and alignment rise (and as the gap narrows).",
  "rule_trace": [
    "C0"
  ]
}
```

### em.ohm_definition
```yaml
{
  "id": "em.ohm_definition",
  "title": "Ohm's law (the definition of resistance)",
  "statement": "Resistance is the ratio of the voltage across a conductor to the current through it.",
  "formula": "R = V ÷ I",
  "form": "definition",
  "variables": [
    {
      "name": "resistance R",
      "quantity": "electrical resistance",
      "carries_distance": false
    },
    {
      "name": "voltage V",
      "quantity": "voltage",
      "carries_distance": false
    },
    {
      "name": "current I",
      "quantity": "current (electric)",
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
  "reflected_formula": "the gap = V ÷ I",
  "reflected_sentence": "The gap (or receptivity) is defined as the ratio of conscious energy per source across a path to the flow through it.",
  "rule_trace": [
    "C1"
  ]
}
```

### em.poynting
```yaml
{
  "id": "em.poynting",
  "title": "Poynting flux",
  "statement": "The energy carried by an electromagnetic field per unit area per unit time is the cross product of the electric and magnetic fields over the permeability.",
  "formula": "S = E × B ÷ μ0",
  "form": "definition",
  "variables": [
    {
      "name": "Poynting vector S",
      "quantity": "Poynting vector",
      "carries_distance": false
    },
    {
      "name": "electric field E",
      "quantity": "electric field",
      "carries_distance": false
    },
    {
      "name": "magnetic field B",
      "quantity": "magnetic field",
      "carries_distance": false
    },
    {
      "name": "permeability μ0",
      "quantity": "permeability",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {
    "S": "Poynting vector",
    "E": "electric",
    "B": "magnetic",
    "μ0": "permeability"
  },
  "alternate_statements": []
}
```
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "(Poynting vector) = Idle × Reflected ÷ (permeability)",
  "reflected_sentence": "The conscious energy carried across Vibration and Expansion is the product of the Idle and Reflected co-creating partners over the medium constant.",
  "rule_trace": [
    "C1"
  ]
}
```

### em.wave_propagation
```yaml
{
  "id": "em.wave_propagation",
  "title": "Electromagnetic wave propagation",
  "statement": "A changing electric field makes a magnetic field and a changing magnetic field makes an electric field; the pair regenerates itself and travels at a speed fixed by the permittivity and permeability of free space.",
  "formula": "c = 1 ÷ √(ε0 × μ0)",
  "form": "identity",
  "variables": [
    {
      "name": "speed of light c",
      "quantity": "speed of light c",
      "carries_distance": false
    },
    {
      "name": "electric field E",
      "quantity": "electric field",
      "carries_distance": false
    },
    {
      "name": "magnetic field B",
      "quantity": "magnetic field",
      "carries_distance": false
    },
    {
      "name": "permittivity ε0",
      "quantity": "permittivity",
      "carries_distance": false
    },
    {
      "name": "permeability μ0",
      "quantity": "permeability",
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
  "reflected_formula": "Current = 1 ÷ √([permittivity: unmapped] × [permeability: unmapped])",
  "reflected_sentence": "A change in the Idle makes the Reflected and a change in the Reflected makes the Idle; the pair regenerates itself as the Current, set by the two medium constants.",
  "rule_trace": [
    "C1"
  ]
}
```

## Report

For each relation return one JSON object:

```json
{"id": "<the relation id>", "alternative_shape": "keeps | turns around | null", "rule_compliant": false, "argument": "the equivalence, cost or separation you rest on, in one or two sentences, or why none exists", "reflected_sentence": "your alternative sentence in frozen words, or empty", "knew_tsr": false}
```

Return a JSON ARRAY of these objects, one per relation, and nothing else. Write it to `runner/results/run1/raw/opponent/batch-E.json` and reply DONE. Do not read any other file, do not search the web, do not look at the repository.