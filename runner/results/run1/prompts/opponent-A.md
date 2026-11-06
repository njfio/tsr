ROLE: opponent

You are the opponent in a test of a reflection rule. Below are the rule, a frozen vocabulary, one physics relation, and the reading that a majority of independent generators produced for it. Your task: produce the STRONGEST reading in which the shape is the other way (keeps instead of turns around, or the reverse), using the same rule and only the frozen vocabulary.

You win only if your alternative is rule-compliant: it must name an equivalence (to keep) or a resistance-caused cost or distance-made separation actually present in the physics statement (to turn), without inventing physics, without new words, and without rewriting the formula. If no rule-compliant alternative exists, say so; that is the honest result and it is what the test needs.

Use only this prompt. If you know anything else about TSR, set it aside and say so in `knew_tsr`.

## The rule

Keep each relationship, and flip the condition. Equivalences, definitions, identities, conservation laws and symmetries keep their shape. A cost or a limit caused by resistance turns around; a separation made by distance turns around; an odd number of such costs turns around. Units don't cross the mirror.

## Which quantities carry resistance (fixed before this run)

- amplitude: does not carry resistance — extent of oscillation
- angular momentum: does not carry resistance — a conserved quantity; rises with moment of inertia, recorded in rises_with
- angular velocity: does not carry resistance — a rate
- coefficient of friction: carries resistance — ratio defining opposition to sliding
- coefficient of restitution: does not carry resistance — a ratio of speeds
- damping coefficient: carries resistance — defined as the opposition to velocity that drains an oscillation
- density: carries resistance — mass per unit volume: mass redistributed by geometry
- force: does not carry resistance — not defined as opposition
- frequency (physical): does not carry resistance — a rate; NB: not TSR Frequency
- gravitational field g: does not carry resistance — an acceleration
- height: does not carry resistance — extent
- kinetic energy: does not carry resistance — energy
- length: does not carry resistance — extent (separation is a relation-level feature)
- mass m: carries resistance — inertial mass is defined as opposition to a change in motion
- moment of inertia: carries resistance — mass redistributed about an axis
- momentum: does not carry resistance — a conserved quantity, not an opposition
- normal force: does not carry resistance — a constraint force; rises with mass only through weight, which is recorded in rises_with
- potential energy: does not carry resistance — energy
- pressure: does not carry resistance — force per area; the book places it at the crossing, not as a resistance quantity
- radius: does not carry resistance — extent
- spring constant: carries resistance — stiffness: opposition to deformation
- time: does not carry resistance — a continuum coordinate
- velocity: does not carry resistance — a rate, not an opposition
- volume: does not carry resistance — extent

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

### mech.angular_momentum
```yaml
{
  "id": "mech.angular_momentum",
  "title": "Angular momentum",
  "statement": "Angular momentum is moment of inertia times angular velocity (the rotational definition), and is conserved when no external torque acts.",
  "formula": "L = I × ω",
  "form": "definition",
  "variables": [
    {
      "name": "angular momentum L",
      "quantity": "angular momentum",
      "carries_distance": false
    },
    {
      "name": "moment of inertia I",
      "quantity": "moment of inertia",
      "carries_distance": false
    },
    {
      "name": "angular velocity ω",
      "quantity": "angular velocity",
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
  "reflected_sentence": "Rotational momentum is the rotational distribution of Movement M times the rate of turning per Expansion, and is conserved when no turning Frequency acts.",
  "rule_trace": [
    "C1"
  ]
}
```

### mech.bernoulli
```yaml
{
  "id": "mech.bernoulli",
  "title": "Bernoulli's principle",
  "statement": "Along a streamline of steady, inviscid, incompressible flow, pressure plus kinetic energy per volume plus gravitational energy per volume is constant.",
  "formula": "P + ½ × ρ × v² + ρ × g × h = const",
  "form": "conservation",
  "variables": [
    {
      "name": "pressure P",
      "quantity": "pressure",
      "carries_distance": false
    },
    {
      "name": "density ρ",
      "quantity": "density",
      "carries_distance": false
    },
    {
      "name": "speed v",
      "quantity": "velocity",
      "carries_distance": false
    },
    {
      "name": "height h",
      "quantity": "height",
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
  "reflected_sentence": "Along a steady flow, Frequency per area plus Desire times rise per Expansion squared plus Desire times Attraction times Vibration is constant.",
  "rule_trace": [
    "C1"
  ]
}
```

### mech.buoyancy
```yaml
{
  "id": "mech.buoyancy",
  "title": "Buoyancy (Archimedes)",
  "statement": "A body immersed in a fluid is pushed up by a force equal to the weight of the fluid it displaces; it floats if it is less dense than the fluid.",
  "formula": "F_b = ρ_fluid × g × V",
  "form": "equation",
  "variables": [
    {
      "name": "buoyant force F_b",
      "quantity": "force",
      "carries_distance": false
    },
    {
      "name": "fluid density ρ_fluid",
      "quantity": "density",
      "carries_distance": false
    },
    {
      "name": "displaced volume V",
      "quantity": "volume",
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
  "reflected_formula": "Frequency = Desire × Attraction × Vibrance",
  "reflected_sentence": "A body in a medium is lifted by a Frequency equal to the Desire times Attraction times Vibrance it displaces, and rises when it has less Desire than the medium.",
  "rule_trace": [
    "C0"
  ]
}
```

### mech.collisions_elastic_inelastic
```yaml
{
  "id": "mech.collisions_elastic_inelastic",
  "title": "Elastic and inelastic collisions",
  "statement": "Momentum is conserved in every collision; kinetic energy is conserved in an elastic collision and partly converted to internal energy in an inelastic one, the fraction set by the coefficient of restitution.",
  "formula": "",
  "form": "conservation",
  "variables": [
    {
      "name": "momentum",
      "quantity": "momentum",
      "carries_distance": false
    },
    {
      "name": "kinetic energy",
      "quantity": "kinetic energy",
      "carries_distance": false
    },
    {
      "name": "coefficient of restitution e",
      "quantity": "coefficient of restitution",
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
  "reflected_sentence": "Momentum is conserved in every meeting; conscious energy of motion is conserved when fully preserved and partly converted when not, in proportion to the ratio of rise per Expansion.",
  "rule_trace": [
    "C1"
  ]
}
```

### mech.gravitational_potential_energy
```yaml
{
  "id": "mech.gravitational_potential_energy",
  "title": "Gravitational potential energy (cost reading)",
  "statement": "Lifting a body against gravity costs energy in proportion to its mass and the height gained.",
  "formula": "U = m × g × h",
  "form": "equation",
  "variables": [
    {
      "name": "potential energy U",
      "quantity": "potential energy",
      "carries_distance": false
    },
    {
      "name": "mass m",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "height h",
      "quantity": "height",
      "carries_distance": false
    },
    {
      "name": "gravitational field g",
      "quantity": "gravitational field g",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "lifting the body; the energy the lift costs",
      "rises_with": [
        "mass m"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {
    "U": "potential energy",
    "m": "mass m",
    "h": "space",
    "g": "gravitational pull"
  },
  "alternate_statements": []
}
```
Majority reading:
```json
{
  "shape": "turns around",
  "reflected_formula": "(potential energy) = Movement M × Attraction × Vibration",
  "reflected_sentence": "Rising in Vibration with Attraction becomes easier as alignment and receptivity rise, rather than costing conscious energy in proportion to Movement M and Vibration.",
  "rule_trace": [
    "C0"
  ]
}
```

### mech.hooke
```yaml
{
  "id": "mech.hooke",
  "title": "Hooke's law",
  "statement": "A spring pushes back in proportion to how far it is stretched; stretching it further takes more force, more so the stiffer the spring.",
  "formula": "F = k × x",
  "form": "equation",
  "variables": [
    {
      "name": "restoring force F",
      "quantity": "force",
      "carries_distance": false
    },
    {
      "name": "spring constant k",
      "quantity": "spring constant",
      "carries_distance": false
    },
    {
      "name": "stretch x",
      "quantity": "length",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "stretching the spring further",
      "rises_with": [
        "spring constant"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {
    "F": "force",
    "k": "spring constant",
    "x": "space"
  },
  "alternate_statements": []
}
```
Majority reading:
```json
{
  "shape": "turns around",
  "reflected_formula": "Frequency = (spring constant) × Vibration",
  "reflected_sentence": "Extending further in Vibration becomes easier and takes less Frequency as receptivity and alignment rise.",
  "rule_trace": [
    "C0"
  ]
}
```

### mech.moment_of_inertia
```yaml
{
  "id": "mech.moment_of_inertia",
  "title": "Moment of inertia",
  "statement": "A body's moment of inertia about an axis is the sum of each mass element times the square of its distance from the axis.",
  "formula": "I = Σ m × r²",
  "form": "definition",
  "variables": [
    {
      "name": "moment of inertia I",
      "quantity": "moment of inertia",
      "carries_distance": false
    },
    {
      "name": "mass element m",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "distance from axis r",
      "quantity": "radius",
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
  "reflected_sentence": "A body's rotational distribution of Movement M about an axis is the product of each Movement M element and the square of its Vibration from the axis.",
  "rule_trace": [
    "C1"
  ]
}
```

### mech.resonance_width
```yaml
{
  "id": "mech.resonance_width",
  "title": "Resonance width",
  "statement": "A driven oscillator responds most strongly near its natural frequency; the width of that response grows with the damping, and the peak height falls with it (Q = ω0/Δω).",
  "formula": "Δω = b ÷ m",
  "form": "equation",
  "variables": [
    {
      "name": "resonance width Δω",
      "quantity": "frequency (physical)",
      "carries_distance": false
    },
    {
      "name": "damping coefficient b",
      "quantity": "damping coefficient",
      "carries_distance": false
    },
    {
      "name": "mass m",
      "quantity": "mass m",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "a sharp, strong response at the natural frequency; the peak broadens and lowers as damping rises",
      "rises_with": [
        "damping coefficient"
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
  "reflected_formula": "",
  "reflected_sentence": "An oscillator responds most strongly at resonance, and as receptivity and alignment rise instead of draining the oscillation, the response sharpens and its peak rises.",
  "rule_trace": [
    "C0"
  ]
}
```

### mech.damping
```yaml
{
  "id": "mech.damping",
  "title": "Damped oscillation",
  "statement": "A damping force opposing velocity drains an oscillation: the amplitude decays exponentially, faster the larger the damping coefficient.",
  "formula": "A(t) = A0 × exp(−b t ÷ 2m)",
  "form": "equation",
  "variables": [
    {
      "name": "damping coefficient b",
      "quantity": "damping coefficient",
      "carries_distance": false
    },
    {
      "name": "mass m",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "amplitude A",
      "quantity": "amplitude",
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
      "what_gets_harder": "the oscillation surviving; amplitude lost per cycle rises with the damping",
      "rises_with": [
        "damping coefficient"
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
  "reflected_formula": "",
  "reflected_sentence": "Instead of an opposing Frequency draining the extent of oscillation over Expansion, the oscillation is sustained more easily as receptivity and alignment rise.",
  "rule_trace": [
    "C0"
  ]
}
```

### mech.friction
```yaml
{
  "id": "mech.friction",
  "title": "Friction",
  "statement": "Resistance between two surfaces sliding past each other: the frictional force rises with the coefficient of friction and the normal force, and turns motion into heat.",
  "formula": "F = μ × N",
  "form": "equation",
  "variables": [
    {
      "name": "coefficient of friction μ",
      "quantity": "coefficient of friction",
      "carries_distance": false
    },
    {
      "name": "normal force N",
      "quantity": "normal force",
      "carries_distance": false
    },
    {
      "name": "frictional force F",
      "quantity": "force",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "keeping the surfaces moving past each other",
      "rises_with": [
        "coefficient of friction"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {
    "F": "force",
    "μ": "coefficient of friction",
    "N": "normal force"
  },
  "alternate_statements": []
}
```
Majority reading:
```json
{
  "shape": "turns around",
  "reflected_formula": "Frequency = (coefficient of friction) × (normal force)",
  "reflected_sentence": "Where two surfaces meet in resonance, keeping going becomes easier rather than harder as receptivity and alignment rise, with Frequency rising with resonance.",
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

Return a JSON ARRAY of these objects, one per relation, and nothing else. Write it to `runner/results/run1/raw/opponent/batch-A.json` and reply DONE. Do not read any other file, do not search the web, do not look at the repository.