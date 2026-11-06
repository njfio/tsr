ROLE: opponent

You are the opponent in a test of a reflection rule. Below are the rule, a frozen vocabulary, one physics relation, and the reading that a majority of independent generators produced for it. Your task: produce the STRONGEST reading in which the shape is the other way (keeps instead of turns around, or the reverse), using the same rule and only the frozen vocabulary.

You win only if your alternative is rule-compliant: it must name an equivalence (to keep) or a resistance-caused cost or distance-made separation actually present in the physics statement (to turn), without inventing physics, without new words, and without rewriting the formula. If no rule-compliant alternative exists, say so; that is the honest result and it is what the test needs.

Use only this prompt. If you know anything else about TSR, set it aside and say so in `knew_tsr`.

## The rule

Keep each relationship, and flip the condition. Equivalences, definitions, identities, conservation laws and symmetries keep their shape. A cost or a limit caused by resistance turns around; a separation made by distance turns around; an odd number of such costs turns around. Units don't cross the mirror.

## Which quantities carry resistance (fixed before this run)

- amplitude: does not carry resistance — extent of oscillation
- angle: does not carry resistance — geometry
- dispersion: does not carry resistance — a dependence, not an opposition
- frequency (physical): does not carry resistance — a rate; NB: not TSR Frequency
- group velocity: does not carry resistance — a rate
- length: does not carry resistance — extent (separation is a relation-level feature)
- phase: does not carry resistance — an angle
- phase velocity: does not carry resistance — a rate
- quantum number: does not carry resistance — a count
- refractive index: UNDETERMINED — n = c/v: the factor by which a medium slows light. Physics defines it as a ratio of speeds, not as opposition; but the Ch 16 reading of diffraction ('where the Current meets resistance, it diffracts') treats the medium as resistance. R does not decide it.
- velocity: does not carry resistance — a rate, not an opposition
- wave speed: does not carry resistance — a rate
- wavelength: does not carry resistance — extent
- wavenumber: does not carry resistance — inverse extent

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

### waves.dispersion
```yaml
{
  "id": "waves.dispersion",
  "title": "Dispersion",
  "statement": "In a dispersive medium the phase velocity depends on wavelength, so a pulse made of many wavelengths spreads as it travels.",
  "formula": "v_p = v_p(λ)",
  "form": "equation",
  "variables": [
    {
      "name": "phase velocity v_p",
      "quantity": "phase velocity",
      "carries_distance": false
    },
    {
      "name": "wavelength λ",
      "quantity": "wavelength",
      "carries_distance": false
    },
    {
      "name": "dispersion",
      "quantity": "dispersion",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "a pulse keeping its shape",
      "rises_with": [
        "dispersion"
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
  "shape": "keeps",
  "reflected_formula": "rise per Expansion = rise per Expansion(Vibration)",
  "reflected_sentence": "Rise per Expansion varies with the extent of each Vibration, so a collection of many Vibrations spreads across Expansion.",
  "rule_trace": [
    "C0"
  ]
}
```

### waves.doppler
```yaml
{
  "id": "waves.doppler",
  "title": "Doppler effect (waves in a medium)",
  "statement": "A receiver moving toward a source, or a source moving toward a receiver, measures a higher frequency than the one emitted; moving apart, a lower one.",
  "formula": "f' = f × (v + v_r) ÷ (v − v_s)",
  "form": "equation",
  "variables": [
    {
      "name": "emitted frequency f",
      "quantity": "frequency (physical)",
      "carries_distance": false
    },
    {
      "name": "wave speed v",
      "quantity": "wave speed",
      "carries_distance": false
    },
    {
      "name": "receiver speed v_r",
      "quantity": "velocity",
      "carries_distance": false
    },
    {
      "name": "source speed v_s",
      "quantity": "velocity",
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
  "reflected_formula": "Frequency' = Frequency × (rise per Expansion + rise per Expansion_r) ÷ (rise per Expansion − rise per Expansion_s)",
  "reflected_sentence": "When receptive and collecting Movement come into alignment, the rate of Vibration per Expansion increases; when out of alignment, it decreases.",
  "rule_trace": [
    "C0"
  ]
}
```

### waves.group_velocity
```yaml
{
  "id": "waves.group_velocity",
  "title": "Group velocity",
  "statement": "The envelope of a wave packet travels at the group velocity, the derivative of angular frequency with respect to wavenumber; it is the speed at which energy and signal travel.",
  "formula": "v_g = dω ÷ dk",
  "form": "definition",
  "variables": [
    {
      "name": "group velocity v_g",
      "quantity": "group velocity",
      "carries_distance": false
    },
    {
      "name": "angular frequency ω",
      "quantity": "frequency (physical)",
      "carries_distance": false
    },
    {
      "name": "wavenumber k",
      "quantity": "wavenumber",
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
  "reflected_formula": "rise per Expansion = d(Expansion) ÷ d(Vibration)",
  "reflected_sentence": "The overall rise per Expansion of a packet of Vibration is the change of Expansion with inverse Vibration, which is how conscious energy E moves.",
  "rule_trace": [
    "C1"
  ]
}
```

### waves.phase_velocity
```yaml
{
  "id": "waves.phase_velocity",
  "title": "Phase and phase velocity",
  "statement": "A wave's phase advances by one cycle per wavelength; the phase velocity is wavelength times frequency, or angular frequency over wavenumber.",
  "formula": "v_p = ω ÷ k",
  "form": "definition",
  "variables": [
    {
      "name": "phase velocity v_p",
      "quantity": "phase velocity",
      "carries_distance": false
    },
    {
      "name": "angular frequency ω",
      "quantity": "frequency (physical)",
      "carries_distance": false
    },
    {
      "name": "wavenumber k",
      "quantity": "wavenumber",
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
  "reflected_formula": "rise per Expansion = Expansion ÷ Vibration",
  "reflected_sentence": "A Vibration advances by one cycle per extent of Vibration, and its rise per Expansion is the ratio of rate in Expansion to inverse extent of Vibration.",
  "rule_trace": [
    "C1"
  ]
}
```

### waves.snell_refraction
```yaml
{
  "id": "waves.snell_refraction",
  "title": "Refraction (Snell's law)",
  "statement": "Crossing into a medium with a different refractive index, a ray bends so that index times the sine of the angle is the same on both sides.",
  "formula": "n1 × sin θ1 = n2 × sin θ2",
  "form": "equation",
  "variables": [
    {
      "name": "refractive index n",
      "quantity": "refractive index",
      "carries_distance": false
    },
    {
      "name": "angle θ",
      "quantity": "angle",
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
  "reflected_formula": "the gap_1 × Vibration_1 = the gap_2 × Vibration_2",
  "reflected_sentence": "Crossing the Point of Reflection into a different gap, the product of the gap and the angle of Vibration remains the same on both sides.",
  "rule_trace": [
    "C0"
  ]
}
```

### waves.standing_waves
```yaml
{
  "id": "waves.standing_waves",
  "title": "Standing waves",
  "statement": "Between two fixed ends only wavelengths that fit a whole number of half-waves into the length persist; the ends force nodes and the allowed modes are set by the separation.",
  "formula": "λ_n = 2 × L ÷ n",
  "form": "limit",
  "variables": [
    {
      "name": "wavelength λ",
      "quantity": "wavelength",
      "carries_distance": false
    },
    {
      "name": "length L between the ends",
      "quantity": "length",
      "carries_distance": true
    },
    {
      "name": "mode number n",
      "quantity": "quantum number",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "which vibrations can persist: only those that fit between the two ends",
      "rises_with": [],
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
  "reflected_formula": "no partner",
  "reflected_sentence": "With receptivity, the limited becomes limitless in which vibrations can persist.",
  "rule_trace": [
    "C0"
  ]
}
```

### waves.superposition
```yaml
{
  "id": "waves.superposition",
  "title": "Superposition",
  "statement": "In a linear medium the net displacement at any point is the sum of the displacements each wave would produce alone.",
  "formula": "y = y1 + y2",
  "form": "identity",
  "variables": [
    {
      "name": "amplitude",
      "quantity": "amplitude",
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
  "reflected_formula": "Vibration = Vibration_1 + Vibration_2",
  "reflected_sentence": "Two Vibrations met in receptivity culminate together into the whole extent of Vibration.",
  "rule_trace": [
    "C1"
  ]
}
```

### waves.interference_cancellation
```yaml
{
  "id": "waves.interference_cancellation",
  "title": "Destructive interference at a point",
  "statement": "Two waves in opposite phase cancel at a point; the cancellation is located, and energy is conserved overall.",
  "formula": "",
  "form": "equation",
  "variables": [
    {
      "name": "phase difference",
      "quantity": "phase",
      "carries_distance": false
    },
    {
      "name": "location of the point",
      "quantity": "length",
      "carries_distance": true
    },
    {
      "name": "amplitude",
      "quantity": "amplitude",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "two vibrations coexisting at one location",
      "rises_with": [],
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
  "reflected_formula": "",
  "reflected_sentence": "Vibrations culminate, while conscious energy is conserved.",
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

Return a JSON ARRAY of these objects, one per relation, and nothing else. Write it to `runner/results/run1/raw/opponent/batch-D.json` and reply DONE. Do not read any other file, do not search the web, do not look at the repository.