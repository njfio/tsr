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

- Reynolds number: does not carry resistance — a ratio of inertial to viscous effects; its viscosity factor is recorded in rises_with
- amplitude: does not carry resistance — extent of oscillation
- angular acceleration: does not carry resistance — a rate
- angular momentum: does not carry resistance — a conserved quantity; rises with moment of inertia, recorded in rises_with
- angular velocity: does not carry resistance — a rate
- area: does not carry resistance — extent
- coefficient of friction: carries resistance — ratio defining opposition to sliding
- coefficient of restitution: does not carry resistance — a ratio of speeds
- damping coefficient: carries resistance — defined as the opposition to velocity that drains an oscillation
- density: carries resistance — mass per unit volume: mass redistributed by geometry
- drag coefficient: carries resistance — defines opposition to motion through a fluid
- force: does not carry resistance — not defined as opposition
- frequency (physical): does not carry resistance — a rate; NB: not TSR Frequency
- gravitational constant G: does not carry resistance — a constant
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
- torque: does not carry resistance — not defined as opposition
- velocity: does not carry resistance — a rate, not an opposition
- viscosity: carries resistance — defined as resistance to shear flow
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

### mech.newton_gravitation
```yaml
{
  "id": "mech.newton_gravitation",
  "title": "Newton's law of gravitation",
  "statement": "Two masses attract with a force proportional to the product of the masses and inversely proportional to the square of their separation.",
  "formula": "F = G × M × m ÷ r²",
  "form": "equation",
  "variables": [
    {
      "name": "force F",
      "quantity": "force",
      "carries_distance": false
    },
    {
      "name": "mass M",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "mass m",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "separation r",
      "quantity": "length",
      "carries_distance": true
    },
    {
      "name": "gravitational constant G",
      "quantity": "gravitational constant G",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {
    "F": "force",
    "M": "mass m",
    "m": "mass m",
    "r": "space",
    "G": "gravitational constant G"
  },
  "alternate_statements": [
    {
      "statement": "Read as a separation cost: the pull between two bodies is weakened by their separation.",
      "form": "equation",
      "costs": [
        {
          "what_gets_harder": "the pull, weakened by separation",
          "rises_with": [],
          "falls_with": [],
          "separation_made_by_distance": true
        }
      ]
    }
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

### mech.reynolds_laminar_turbulent
```yaml
{
  "id": "mech.reynolds_laminar_turbulent",
  "title": "Reynolds number: laminar and turbulent flow",
  "statement": "Flow stays laminar while inertial effects are small relative to viscous ones (low Reynolds number); as density, speed or size rise, or viscosity falls, the flow becomes turbulent.",
  "formula": "Re = ρ × v × L ÷ μ",
  "form": "equation",
  "variables": [
    {
      "name": "Reynolds number Re",
      "quantity": "Reynolds number",
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
      "name": "length scale L",
      "quantity": "length",
      "carries_distance": false
    },
    {
      "name": "viscosity μ",
      "quantity": "viscosity",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "keeping the flow ordered (laminar)",
      "rises_with": [
        "density"
      ],
      "falls_with": [
        "viscosity"
      ],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### mech.terminal_velocity
```yaml
{
  "id": "mech.terminal_velocity",
  "title": "Terminal velocity",
  "statement": "A falling body stops accelerating when drag balances weight; that terminal speed rises with the body's mass and falls with the drag coefficient, the fluid's density and the cross-section.",
  "formula": "v_t = √(2 × m × g ÷ (ρ × C_d × A))",
  "form": "equation",
  "variables": [
    {
      "name": "terminal speed v_t",
      "quantity": "velocity",
      "carries_distance": false
    },
    {
      "name": "mass m",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "drag coefficient C_d",
      "quantity": "drag coefficient",
      "carries_distance": false
    },
    {
      "name": "fluid density ρ",
      "quantity": "density",
      "carries_distance": false
    },
    {
      "name": "cross-section A",
      "quantity": "area",
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
      "what_gets_harder": "stopping the fall: the speed the fall settles at",
      "rises_with": [
        "mass m"
      ],
      "falls_with": [
        "drag coefficient",
        "density"
      ],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### mech.torque
```yaml
{
  "id": "mech.torque",
  "title": "Torque and angular acceleration",
  "statement": "Torque equals moment of inertia times angular acceleration: the rotational form of Newton's second law, read as the definition of torque's effect.",
  "formula": "τ = I × α",
  "form": "definition",
  "variables": [
    {
      "name": "torque τ",
      "quantity": "torque",
      "carries_distance": false
    },
    {
      "name": "moment of inertia I",
      "quantity": "moment of inertia",
      "carries_distance": false
    },
    {
      "name": "angular acceleration α",
      "quantity": "angular acceleration",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": [
    {
      "statement": "Read as a law: for a given angular acceleration, the torque required rises with the moment of inertia.",
      "form": "equation",
      "costs": [
        {
          "what_gets_harder": "the torque required for a given angular acceleration",
          "rises_with": [
            "moment of inertia"
          ],
          "falls_with": [],
          "separation_made_by_distance": false
        }
      ]
    }
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

Return a JSON ARRAY with one such object per relation, in the order given, and nothing else in the file. Write it to the file `runner/results/run1/raw/<MODEL>/batch-A.json` and then reply with the single word DONE. Do not read any other file, do not search the web, do not look at the repository.