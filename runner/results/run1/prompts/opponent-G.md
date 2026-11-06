ROLE: opponent

You are the opponent in a test of a reflection rule. Below are the rule, a frozen vocabulary, one physics relation, and the reading that a majority of independent generators produced for it. Your task: produce the STRONGEST reading in which the shape is the other way (keeps instead of turns around, or the reverse), using the same rule and only the frozen vocabulary.

You win only if your alternative is rule-compliant: it must name an equivalence (to keep) or a resistance-caused cost or distance-made separation actually present in the physics statement (to turn), without inventing physics, without new words, and without rewriting the formula. If no rule-compliant alternative exists, say so; that is the honest result and it is what the test needs.

Use only this prompt. If you know anything else about TSR, set it aside and say so in `knew_tsr`.

## The rule

Keep each relationship, and flip the condition. Equivalences, definitions, identities, conservation laws and symmetries keep their shape. A cost or a limit caused by resistance turns around; a separation made by distance turns around; an odd number of such costs turns around. Units don't cross the mirror.

## Which quantities carry resistance (fixed before this run)

- Higgs coupling (Yukawa): UNDETERMINED — the coupling that gives a particle its mass; mass carries resistance (a), and the coupling is monotone in it, but it is a coupling, not a redistribution by geometry. R does not decide it.
- charge: does not carry resistance — a source / coupling strength; not defined as opposition. The book pairs electric and magnetic as co-creating partners, not as resistance. Decided under R before electromagnetism ran.
- coupling constant: does not carry resistance — interaction strength, not opposition
- energy: does not carry resistance — shared by both sides of the mirror (one E)
- frequency (physical): does not carry resistance — a rate; NB: not TSR Frequency
- gravitational field g: does not carry resistance — an acceleration
- mass m: carries resistance — inertial mass is defined as opposition to a change in motion
- momentum: does not carry resistance — a conserved quantity, not an opposition
- running coupling: does not carry resistance — interaction strength
- speed of light c: does not carry resistance — the limit, not an opposition
- vacuum energy density: does not carry resistance — energy
- vacuum expectation value: does not carry resistance — a field value
- velocity: does not carry resistance — a rate, not an opposition

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

### field.cp_violation
```yaml
{
  "id": "field.cp_violation",
  "title": "CP violation",
  "statement": "The weak interaction treats matter and antimatter slightly differently: the combined operation of charge conjugation and parity is not an exact symmetry.",
  "formula": "",
  "form": "equation",
  "variables": [],
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
  "reflected_sentence": "A weak Frequency treats two sides differently in Vibrational Reality: their combined reflection is not an exact equivalence.",
  "rule_trace": [
    "C0"
  ]
}
```

### field.gauge_invariance
```yaml
{
  "id": "field.gauge_invariance",
  "title": "Gauge invariance",
  "statement": "Requiring the laws to be unchanged under local phase changes of the matter fields forces the existence of the gauge fields that carry the forces.",
  "formula": "",
  "form": "symmetry",
  "variables": [],
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
  "reflected_sentence": "In Vibrational Reality, the Demand that Desire remain unchanged under every shift of imagination brings Frequency into being.",
  "rule_trace": [
    "C1"
  ]
}
```

### field.higgs_mechanism
```yaml
{
  "id": "field.higgs_mechanism",
  "title": "Higgs mechanism",
  "statement": "The masses of the W and Z bosons and of the fundamental fermions arise from their coupling to the Higgs field's nonzero vacuum value; a particle's mass is its coupling strength times that value.",
  "formula": "m_f = y_f × v ÷ √2",
  "form": "equation",
  "variables": [
    {
      "name": "fermion mass m_f",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "Yukawa coupling y_f",
      "quantity": "Higgs coupling (Yukawa)",
      "carries_distance": false
    },
    {
      "name": "vacuum expectation value v",
      "quantity": "vacuum expectation value",
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
  "reflected_formula": "Movement M = Yukawa coupling y_f × vacuum expectation value v ÷ √2",
  "reflected_sentence": "Movement M arises from how receptivity Tunes to the underlying Vibration; Movement M is that Tune times that Vibration.",
  "rule_trace": [
    "C0"
  ]
}
```

### field.noether
```yaml
{
  "id": "field.noether",
  "title": "Noether's theorem",
  "statement": "Every continuous symmetry of the action corresponds to a conserved quantity: time translation to energy, space translation to momentum, rotation to angular momentum, phase to charge.",
  "formula": "",
  "form": "identity",
  "variables": [
    {
      "name": "energy",
      "quantity": "energy",
      "carries_distance": false
    },
    {
      "name": "momentum",
      "quantity": "momentum",
      "carries_distance": false
    },
    {
      "name": "charge",
      "quantity": "charge",
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
  "reflected_sentence": "In Vibrational Reality, every symmetry corresponds to a quantity that stays: Expansion to conscious energy, Vibration to momentum, turning to angular momentum, and phase to charge.",
  "rule_trace": [
    "C1"
  ]
}
```

### field.running_couplings
```yaml
{
  "id": "field.running_couplings",
  "title": "Running couplings",
  "statement": "The strengths of the interactions depend on the energy scale at which they are probed: the electromagnetic coupling grows with energy, the strong coupling falls.",
  "formula": "",
  "form": "equation",
  "variables": [
    {
      "name": "running coupling",
      "quantity": "running coupling",
      "carries_distance": false
    },
    {
      "name": "energy scale",
      "quantity": "energy",
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
  "reflected_sentence": "Frequency depends on E: Idle and Reflected Frequency grows with E, while strong Frequency falls with E.",
  "rule_trace": [
    "C0"
  ]
}
```

### field.vacuum_energy
```yaml
{
  "id": "field.vacuum_energy",
  "title": "Vacuum energy",
  "statement": "The quantum vacuum has an energy density; the value field theory estimates and the value cosmology measures differ by many orders of magnitude.",
  "formula": "",
  "form": "definition",
  "variables": [
    {
      "name": "vacuum energy density",
      "quantity": "vacuum energy density",
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
  "reflected_sentence": "Vibration has conscious energy and Desire; what imagination Tunes to and what emotional evidence shows differ across the gap.",
  "rule_trace": [
    "C1"
  ]
}
```

### field.weak_flavor_change
```yaml
{
  "id": "field.weak_flavor_change",
  "title": "Flavor change via the weak interaction",
  "statement": "Only the weak interaction changes one kind of quark or lepton into another (through the charged W boson); the strong and electromagnetic interactions never do.",
  "formula": "",
  "form": "identity",
  "variables": [
    {
      "name": "coupling constant",
      "quantity": "coupling constant",
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
  "reflected_sentence": "Only weak Frequency gives realization from one form into another; strong Frequency and Idle and Reflected Frequency never do.",
  "rule_trace": [
    "C1"
  ]
}
```

### rel.energy_momentum_relation
```yaml
{
  "id": "rel.energy_momentum_relation",
  "title": "Energy-momentum relation",
  "statement": "A body's energy squared equals its momentum times c squared plus its rest energy squared; for a massless particle the energy is momentum times c.",
  "formula": "E² = (p × c)² + (m × c²)²",
  "form": "identity",
  "variables": [
    {
      "name": "energy E",
      "quantity": "energy",
      "carries_distance": false
    },
    {
      "name": "momentum p",
      "quantity": "momentum",
      "carries_distance": false
    },
    {
      "name": "mass m",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "speed of light c",
      "quantity": "speed of light c",
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
  "reflected_formula": "E² = (momentum × Current)² + (Movement M × Current²)²",
  "reflected_sentence": "E squared equals momentum times Current squared plus Movement M times Current squared squared.",
  "rule_trace": [
    "C1"
  ]
}
```

### rel.equivalence_principle
```yaml
{
  "id": "rel.equivalence_principle",
  "title": "Equivalence principle",
  "statement": "Gravitational mass equals inertial mass, so a freely falling observer feels no gravity: locally, free fall is indistinguishable from the absence of gravitation.",
  "formula": "",
  "form": "identity",
  "variables": [
    {
      "name": "mass m",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "gravitational field g",
      "quantity": "gravitational field g",
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
  "reflected_sentence": "Movement M in Attraction equals Movement M, so in receptive alignment there is no gap from Attraction.",
  "rule_trace": [
    "C1"
  ]
}
```

### rel.null_interval
```yaml
{
  "id": "rel.null_interval",
  "title": "Null interval",
  "statement": "Along a light ray the space-time interval is zero: no proper time passes for light, and its energy depends on who measures it.",
  "formula": "ds² = 0",
  "form": "identity",
  "variables": [
    {
      "name": "speed of light c",
      "quantity": "speed of light c",
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
  "reflected_formula": "ds² = 0, with s the Vibration-Expansion interval",
  "reflected_sentence": "Along the Current the Vibration-Expansion interval vanishes: no Expansion of its own passes for the Current, and its E depends on whose emotional evidence meets it.",
  "rule_trace": [
    "C1"
  ]
}
```

### rel.relativistic_doppler
```yaml
{
  "id": "rel.relativistic_doppler",
  "title": "Relativistic Doppler effect",
  "statement": "Light from a source receding at speed v is received at a lower frequency by the factor square root of (1 − β) over (1 + β); approaching, higher. No medium is involved and only the relative velocity matters.",
  "formula": "f' = f × √((1 − β) ÷ (1 + β))",
  "form": "equation",
  "variables": [
    {
      "name": "emitted frequency f",
      "quantity": "frequency (physical)",
      "carries_distance": false
    },
    {
      "name": "relative velocity v",
      "quantity": "velocity",
      "carries_distance": false
    },
    {
      "name": "speed of light c",
      "quantity": "speed of light c",
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
  "reflected_sentence": "A received rate keeps changed with rise per Expansion against the Current, and that rate is not Frequency.",
  "rule_trace": [
    "C0"
  ]
}
```

### rel.velocity_addition
```yaml
{
  "id": "rel.velocity_addition",
  "title": "Relativistic velocity addition",
  "statement": "Velocities compose so that the result never exceeds c: the combined speed is the sum divided by one plus the product over c squared.",
  "formula": "u' = (u + v) ÷ (1 + u × v ÷ c²)",
  "form": "identity",
  "variables": [
    {
      "name": "velocity u",
      "quantity": "velocity",
      "carries_distance": false
    },
    {
      "name": "velocity v",
      "quantity": "velocity",
      "carries_distance": false
    },
    {
      "name": "speed of light c",
      "quantity": "speed of light c",
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
  "reflected_formula": "(rise per Expansion)' = (rise per Expansion + rise per Expansion) ÷ (1 + rise per Expansion × rise per Expansion ÷ Current²)",
  "reflected_sentence": "In Vibrational Reality, rise per Expansion adds so that it never passes Current: the sum is tempered by one plus the product over Current squared.",
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

Return a JSON ARRAY of these objects, one per relation, and nothing else. Write it to `runner/results/run1/raw/opponent/batch-G.json` and reply DONE. Do not read any other file, do not search the web, do not look at the repository.