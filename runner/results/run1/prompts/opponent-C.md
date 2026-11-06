ROLE: opponent

You are the opponent in a test of a reflection rule. Below are the rule, a frozen vocabulary, one physics relation, and the reading that a majority of independent generators produced for it. Your task: produce the STRONGEST reading in which the shape is the other way (keeps instead of turns around, or the reverse), using the same rule and only the frozen vocabulary.

You win only if your alternative is rule-compliant: it must name an equivalence (to keep) or a resistance-caused cost or distance-made separation actually present in the physics statement (to turn), without inventing physics, without new words, and without rewriting the formula. If no rule-compliant alternative exists, say so; that is the honest result and it is what the test needs.

Use only this prompt. If you know anything else about TSR, set it aside and say so in `knew_tsr`.

## The rule

Keep each relationship, and flip the condition. Equivalences, definitions, identities, conservation laws and symmetries keep their shape. A cost or a limit caused by resistance turns around; a separation made by distance turns around; an odd number of such costs turns around. Units don't cross the mirror.

## Which quantities carry resistance (fixed before this run)

- Boltzmann constant: does not carry resistance — a constant
- Shannon entropy: does not carry resistance — a measure of uncertainty
- bandwidth: does not carry resistance — extent in frequency
- channel capacity: does not carry resistance — a rate
- correlation length: does not carry resistance — extent
- damping coefficient: carries resistance — defined as the opposition to velocity that drains an oscillation
- degrees of freedom: does not carry resistance — a count
- energy: does not carry resistance — shared by both sides of the mirror (one E)
- entropy: does not carry resistance — a count of microstates / a state function; not defined as opposition. Decided under R before thermodynamics ran.
- mutual information: does not carry resistance — a measure
- noise power: does not carry resistance — power
- number of microstates: does not carry resistance — a count
- order parameter: does not carry resistance — a measure of order
- power: does not carry resistance — a rate of energy
- probability: does not carry resistance — a measure
- temperature: does not carry resistance — mean kinetic energy per degree of freedom (or dS/dU inverse); not defined as opposition to change. Decided under R before thermodynamics ran.

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

### info.channel_capacity
```yaml
{
  "id": "info.channel_capacity",
  "title": "Channel capacity",
  "statement": "The greatest rate at which information can be sent reliably through a noisy channel is the bandwidth times the log of one plus the signal-to-noise ratio.",
  "formula": "C = B × log(1 + S ÷ N)",
  "form": "definition",
  "variables": [
    {
      "name": "capacity C",
      "quantity": "channel capacity",
      "carries_distance": false
    },
    {
      "name": "bandwidth B",
      "quantity": "bandwidth",
      "carries_distance": false
    },
    {
      "name": "signal power S",
      "quantity": "power",
      "carries_distance": false
    },
    {
      "name": "noise power N",
      "quantity": "noise power",
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
  "reflected_formula": "[unmapped: capacity C] = [unmapped: bandwidth B] × log(1 + [unmapped: signal power S] ÷ [unmapped: noise power N])",
  "reflected_sentence": "The limitless collection of [unmapped: channel capacity C] equals [unmapped: bandwidth B] times the logarithm of one plus [unmapped: signal power S] divided by [unmapped: noise power N].",
  "rule_trace": [
    "C1"
  ]
}
```

### info.data_processing_inequality
```yaml
{
  "id": "info.data_processing_inequality",
  "title": "Data processing inequality",
  "statement": "Processing cannot increase information: if Z depends on X only through Y, then the information Z carries about X is at most what Y carries.",
  "formula": "I(X;Z) ≤ I(X;Y)",
  "form": "inequality",
  "variables": [
    {
      "name": "mutual information I",
      "quantity": "mutual information",
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
  "reflected_formula": "[unmapped: mutual information I](X;Z) ≤ [unmapped: mutual information I](X;Y)",
  "reflected_sentence": "If Z Tune-s to X only through Y, then the [unmapped: mutual information I] that Z holds with X is at most what Y holds with X.",
  "rule_trace": [
    "C0"
  ]
}
```

### info.landauer
```yaml
{
  "id": "info.landauer",
  "title": "Landauer's principle",
  "statement": "Erasing one bit of information dissipates at least k T ln 2 of energy as heat; logically irreversible operations have a thermodynamic cost that rises with temperature.",
  "formula": "E ≥ k × T × ln 2",
  "form": "inequality",
  "variables": [
    {
      "name": "energy E",
      "quantity": "energy",
      "carries_distance": false
    },
    {
      "name": "temperature T",
      "quantity": "temperature",
      "carries_distance": false
    },
    {
      "name": "Boltzmann constant k",
      "quantity": "Boltzmann constant",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "erasing; the heat it must dissipate",
      "rises_with": [
        "temperature"
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
  "reflected_formula": "",
  "reflected_sentence": "E has a partner, but the complete relation does not.",
  "rule_trace": [
    "C0"
  ]
}
```

### info.shannon_entropy
```yaml
{
  "id": "info.shannon_entropy",
  "title": "Shannon entropy",
  "statement": "The uncertainty of a source is minus the sum over outcomes of probability times log probability; it is the least average number of bits needed to encode it.",
  "formula": "H = −Σ p × log p",
  "form": "definition",
  "variables": [
    {
      "name": "Shannon entropy H",
      "quantity": "Shannon entropy",
      "carries_distance": false
    },
    {
      "name": "probability p",
      "quantity": "probability",
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
  "reflected_sentence": "No complete reflected sentence is available from the frozen vocabulary.",
  "rule_trace": [
    "C1"
  ]
}
```

### statmech.boltzmann_entropy
```yaml
{
  "id": "statmech.boltzmann_entropy",
  "title": "Boltzmann entropy",
  "statement": "The entropy of a macrostate is Boltzmann's constant times the logarithm of the number of microstates that realize it.",
  "formula": "S = k × ln W",
  "form": "definition",
  "variables": [
    {
      "name": "entropy S",
      "quantity": "entropy",
      "carries_distance": false
    },
    {
      "name": "number of microstates W",
      "quantity": "number of microstates",
      "carries_distance": false
    },
    {
      "name": "Boltzmann constant k",
      "quantity": "Boltzmann constant",
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
  "reflected_formula": "Culmination (provisional) = [unmapped: Boltzmann constant k] × ln [unmapped: number of microstates W]",
  "reflected_sentence": "The Culmination (provisional) of a [unmapped: macrostate] is [unmapped: Boltzmann constant k] times the logarithm of the [unmapped: number of microstates W] in its realization.",
  "rule_trace": [
    "C1"
  ]
}
```

### statmech.equipartition
```yaml
{
  "id": "statmech.equipartition",
  "title": "Equipartition",
  "statement": "In thermal equilibrium every quadratic degree of freedom carries an average energy of half k times the temperature.",
  "formula": "⟨E⟩ = ½ × k × T per degree of freedom",
  "form": "identity",
  "variables": [
    {
      "name": "energy E",
      "quantity": "energy",
      "carries_distance": false
    },
    {
      "name": "temperature T",
      "quantity": "temperature",
      "carries_distance": false
    },
    {
      "name": "degrees of freedom",
      "quantity": "degrees of freedom",
      "carries_distance": false
    },
    {
      "name": "Boltzmann constant k",
      "quantity": "Boltzmann constant",
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
  "reflected_sentence": "E has a partner, but the complete relation does not.",
  "rule_trace": [
    "C1"
  ]
}
```

### statmech.ergodicity
```yaml
{
  "id": "statmech.ergodicity",
  "title": "Ergodic hypothesis",
  "statement": "For an ergodic system the long-time average of an observable equals its average over the ensemble of accessible states.",
  "formula": "",
  "form": "identity",
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
  "reflected_sentence": "The relationship keeps: the average over long Expansion of a measurable quantity equals its average over the collection of reachable states, and only Expansion has a frozen partner.",
  "rule_trace": [
    "C1"
  ]
}
```

### statmech.fluctuation_dissipation
```yaml
{
  "id": "statmech.fluctuation_dissipation",
  "title": "Fluctuation-dissipation theorem",
  "statement": "The way a system in equilibrium dissipates a small push is fixed by the spectrum of its own spontaneous fluctuations: friction and thermal noise are two faces of one quantity.",
  "formula": "",
  "form": "identity",
  "variables": [
    {
      "name": "damping coefficient",
      "quantity": "damping coefficient",
      "carries_distance": false
    },
    {
      "name": "temperature T",
      "quantity": "temperature",
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
  "reflected_sentence": "The way a system in [unmapped: equilibrium] meets a small Frequency is fixed by the [unmapped: spectrum] of its own [unmapped: spontaneous fluctuations]: resonance and [unmapped: thermal noise] are two faces of one quantity.",
  "rule_trace": [
    "C1"
  ]
}
```

### statmech.phase_transition_critical_point
```yaml
{
  "id": "statmech.phase_transition_critical_point",
  "title": "Phase transition and critical point",
  "statement": "At a continuous phase transition the order parameter vanishes and the correlation length diverges: fluctuations at every scale, and no characteristic size.",
  "formula": "ξ → ∞ as T → T_c",
  "form": "limit",
  "variables": [
    {
      "name": "order parameter",
      "quantity": "order parameter",
      "carries_distance": false
    },
    {
      "name": "correlation length ξ",
      "quantity": "correlation length",
      "carries_distance": false
    },
    {
      "name": "temperature T",
      "quantity": "temperature",
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
  "reflected_formula": "[unmapped: correlation length ξ] → limitless as [unmapped: temperature T] → [unmapped: critical temperature T_c]",
  "reflected_sentence": "At a [unmapped: continuous phase transition] the [unmapped: order parameter] vanishes and the [unmapped: correlation length ξ] becomes limitless as [unmapped: temperature T] approaches [unmapped: critical temperature T_c].",
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

Return a JSON ARRAY of these objects, one per relation, and nothing else. Write it to `runner/results/run1/raw/opponent/batch-C.json` and reply DONE. Do not read any other file, do not search the web, do not look at the repository.