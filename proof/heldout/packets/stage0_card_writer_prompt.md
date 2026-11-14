# Stage 0 Plain-Physics Law Card Generation Packet

- **preregistration_commit_sha:** `463ad9f93c8a276b1e0d9ee497198dfa2169d079`
- **Card count:** `65` (`C001`..`C065`)

## Instructions for One Fresh External Session

You are assisting with a physics curriculum summarization task in a clean standalone session.
Write one plain-language physics summary card for each of the `65` physics laws/relations listed below (`C001` through `C065`).

### Strict Output Schema
Return **ONLY** one valid JSON array of `65` objects in exact order `C001`..`C065`, using these exact four keys per object:

```json
[
  {
    "card_id": "C001",
    "what_it_says": "...",
    "quantities_related": "...",
    "conditions_to_hold": "..."
  }
]
```

### Field Requirements
For every entry:
1. `what_it_says`: A concise, accurate, plain-language statement of the physical law or principle, plus its mathematical formula where a formula is given.
2. `quantities_related`: List all physical quantities and variables related by the law (e.g., mass, velocity, force, displacement, pressure, volume, temperature, time, energy, frequency, wavelength).
3. `conditions_to_hold`: State all physical conditions, domain assumptions, or structural requirements needed for the law to hold (for example: mass or rotational inertia, spatial distance or separation between bodies/events, physical contact/surfaces/walls or medium, gravitational field or spacetime curvature, relative speed/inertial or accelerating reference frame, or definitional equivalence/conservation/frame invariance).

### Style & Neutrality Constraints
- Use strictly standard textbook physics terminology.
- Do **not** group entries, sort entries, infer source origin, speculate about book/chapter provenance, or use philosophical or non-standard terminology.
- Every string value must be non-empty.

---

## Physics Laws to Summarize (`C001`..`C065`)

### C001
- **description:** Continuity equation (constant density)
- **formula:** `A_{1} v_{1} = A_{2} v_{2}`

### C002
- **description:** Linear thermal expansion
- **formula:** `\Delta L = \alpha L \Delta T`

### C003
- **description:** Wavelength for symmetric boundary conditions
- **formula:** `\lambda_{n} = \frac{2}{n} L, n = 1, 2, 3, 4, 5 \dots`

### C004
- **description:** Magnitude of kinetic friction
- **formula:** `f_{k} = \mu_{k} N`

### C005
- **description:** Time dilation between proper time and moving-observer coordinate time
- **formula:** `\Delta t = \gamma \Delta \tau = \frac{\Delta \tau}{\sqrt{1 - v^{2}/c^{2}}}`

### C006
- **description:** Newton's second law for harmonic motion
- **formula:** `m \frac{d^{2} x}{d t^{2}} + b \frac{d x}{d t} + k x = 0`

### C007
- **description:** Angular velocity
- **formula:** `\omega = \lim_{\Delta t \to 0} \frac{\Delta \theta}{\Delta t} = \frac{d \theta}{d t}`

### C008
- **description:** Orbital period
- **formula:** `T = 2 \pi \sqrt{\frac{r^{3}}{\text{GM}_{\text{E}}}}`

### C009
- **description:** Molar heat capacity at constant pressure
- **formula:** `C_{p} = C_{V} + R`

### C010
- **description:** For a system of particles, derivative of angular momentum equals torque
- **formula:** `\frac{d \vec{L}}{d t} = \sum \vec{\tau}`

### C011
- **description:** Relativistic kinetic energy and total energy of a moving particle
- **formula:** `K = (\gamma - 1) m c^{2}, \quad E = \gamma m c^{2}`

### C012
- **description:** Ideal gas law in terms of molecules
- **formula:** `p V = N k_{\text{B}} T`

### C013
- **description:** Inverse Lorentz transformation
- **formula:** `x'= \frac{x - v t}{\sqrt{1 - v^{2} / c^{2}}}`

### C014
- **description:** Boyle's law for an isothermal fixed quantity of ideal gas
- **formula:** `P_{1} V_{1} = P_{2} V_{2} \quad (\text{constant } T, n)`

### C015
- **description:** Invariant speed of light as the upper speed limit for massive particles
- **formula:** `v < c \quad (\gamma \to \infty \text{ as } v \to c \text{ for } m > 0)`

### C016
- **description:** Condition for conservative force in two dimensions
- **formula:** `(\frac{d F_{x}}{d y}) = (\frac{d F_{y}}{d x})`

### C017
- **description:** Conservative force is the negative derivative of potential energy
- **formula:** `F_{l} = - \frac{d U}{d l}`

### C018
- **description:** Gravitational potential wells, gravitational redshift, and gravitational lensing of light
- **formula:** `None (qualitative physical principle)`

### C019
- **description:** Coefficient of performance of a heat pump
- **formula:** `K_{\text{P}} = \frac{Q_{\text{h}}}{W} = \frac{Q_{\text{h}}}{Q_{\text{h}} - Q_{\text{c}}}`

### C020
- **description:** Thermal expansion in three dimensions
- **formula:** `\Delta V = \beta V \Delta T`

### C021
- **description:** Stokes' law
- **formula:** `F_{\text{s}} = 6 \pi r \eta v`

### C022
- **description:** Conservation of total energy in an isolated system
- **formula:** `E_{\text{i}} = E_{\text{f}} \quad (\Delta E_{\text{sys}} = 0)`

### C023
- **description:** First postulate of special relativity (invariance of physical laws across inertial reference frames)
- **formula:** `None (qualitative physical principle)`

### C024
- **description:** Work-energy theorem
- **formula:** `W_{\text{net}} = K_{B} - K_{A}`

### C025
- **description:** Impulse
- **formula:** `\vec{J} \equiv \int_{t_{\text{i}}}^{t_{\text{f}}} \vec{F} (t) d t \text{or} \vec{J} = \vec{F}_{\text{ave}} \Delta t`

### C026
- **description:** Work done going from A to B by Earth's gravity, near its surface
- **formula:** `W_{\text{grav,} A B} = - m g (y_{B} - y_{A})`

### C027
- **description:** Newton's second law of motion
- **formula:** `\vec{F}_{\text{net}} = m \vec{a}`

### C028
- **description:** Lorentz transformation
- **formula:** `t = \frac{t'+ v x' / c^{2}}{\sqrt{1 - v^{2} / c^{2}}}`

### C029
- **description:** General velocity in SHM
- **formula:** `v (t) = - A \omega \sin (\omega t + \phi)`

### C030
- **description:** Total acceleration
- **formula:** `\vec{a} = \vec{a}_{\text{C}} + \vec{a}_{\text{T}}`

### C031
- **description:** Speed of sound in an ideal gas
- **formula:** `v = \sqrt{\frac{\gamma R T}{M}}`

### C032
- **description:** Mass density definition relating mass, density, and volume
- **formula:** `m = \rho V \quad (\rho = \frac{m}{V})`

### C033
- **description:** Moment of inertia
- **formula:** `I = \sum_{j} m_{j} r_{j}^{2}`

### C034
- **description:** Young's modulus
- **formula:** `Y = \frac{\text{tensile stress}}{\text{tensile strain}} = \frac{F_{\perp}}{A} \frac{L_{0}}{\Delta L}`

### C035
- **description:** Principle of relativity (absence of a preferred inertial rest frame)
- **formula:** `None (qualitative physical principle)`

### C036
- **description:** Ratio of molar heat capacities
- **formula:** `\gamma = C_{p} / C_{V}`

### C037
- **description:** Relativity of simultaneity for spatially separated events
- **formula:** `\Delta t = \frac{\gamma v \Delta x}{c^{2}} \quad (\text{for } \Delta t' = 0)`

### C038
- **description:** Acceleration of the center of mass
- **formula:** `\vec{a}_{\text{CM}} = \frac{d^{2}}{d t^{2}} (\frac{1}{M} \sum_{j = 1}^{N} m_{j} \vec{r}_{j}) = \frac{1}{M} \sum_{j = 1}^{N} m_{j} \vec{a}_{j}`

### C039
- **description:** Viscosity
- **formula:** `\eta = \frac{F L}{v A}`

### C040
- **description:** Rest mass-energy equivalence
- **formula:** `E_{0} = m c^{2}`

### C041
- **description:** Condition for an ideal gas in a quasi-static adiabatic process
- **formula:** `p V^{\gamma} = \text{constant}`

### C042
- **description:** Invariant spacetime interval unifying space and time
- **formula:** `s^{2} = c^{2} (\Delta t)^{2} - (\Delta x)^{2} - (\Delta y)^{2} - (\Delta z)^{2}`

### C043
- **description:** Wave number
- **formula:** `k \equiv \frac{2 \pi}{\lambda}`

### C044
- **description:** Performance coefficient of a reversible refrigerator
- **formula:** `K_{\text{R}} = \frac{T_{\text{c}}}{T_{\text{h}} - T_{\text{c}}}`

### C045
- **description:** Position from velocity and acceleration
- **formula:** `x = x_{0} + v_{0} t + \frac{1}{2} a t^{2} (\text{constant} a)`

### C046
- **description:** Acceleration of an object rolling without slipping
- **formula:** `a_{\text{CM}} = \frac{m g \sin \theta}{m + (I_{\text{CM}} / r^{2})}`

### C047
- **description:** Rate of conductive heat transfer
- **formula:** `P = \frac{k A (T_{h} - T_{c})}{d}`

### C048
- **description:** Normal force on an object resting on a horizontal surface, scalar form
- **formula:** `N = m g`

### C049
- **description:** Observed frequency for a moving observer and a stationary source
- **formula:** `f_{\text{o}} = f_{\text{s}} (\frac{v \pm v_{\text{o}}}{v})`

### C050
- **description:** Equivalence principle and scope of inertial versus accelerating or gravitating reference frames
- **formula:** `None (qualitative physical principle)`

### C051
- **description:** Kepler's third law
- **formula:** `T^{2} = \frac{4 \pi^{2}}{G M} a^{3}`

### C052
- **description:** Velocity in terms of components
- **formula:** `\vec{v} (t) = v_{x} (t) \hat{i} + v_{y} (t) \hat{j} + v_{z} (t) \hat{k}`

### C053
- **description:** Newton's first law
- **formula:** `\vec{v} = \text{constant when} \vec{F}_{\text{net}} = \vec{0} \text{N}`

### C054
- **description:** Newton's third law of motion (action-reaction force pair)
- **formula:** `\vec{F}_{AB} = -\vec{F}_{BA}`

### C055
- **description:** Wave speed
- **formula:** `v = \frac{\omega}{k}`

### C056
- **description:** Instantaneous acceleration as second derivatives of position
- **formula:** `\vec{a} (t) = \frac{d^{2} x (t)}{d t^{2}} \hat{i} + \frac{d^{2} y (t)}{d t^{2}} \hat{j} + \frac{d^{2} z (t)}{d t^{2}} \hat{k}`

### C057
- **description:** Maximum velocity of SHM
- **formula:** `| v_{\max} | = A \omega`

### C058
- **description:** Average velocity (for constant acceleration)
- **formula:** `\bar{v} = \frac{v_{0} + v}{2}`

### C059
- **description:** Molar heat capacity at constant volume for an ideal gas with d degrees of freedom
- **formula:** `C_{V} = \frac{d}{2} R`

### C060
- **description:** Curvature of spacetime geometry induced by mass-energy
- **formula:** `None (qualitative physical principle)`

### C061
- **description:** Newton's law of gravitation
- **formula:** `\vec{F}_{12} = G \frac{m_{1} m_{2}}{r^{2}} \hat{r}_{12}`

### C062
- **description:** Restoring force by a spring displaced by x from the relaxed position
- **formula:** `\vec{F} = - k \vec{x}`

### C063
- **description:** Length contraction along the direction of relative motion
- **formula:** `L = \frac{L_{0}}{\gamma} = L_{0} \sqrt{1 - \frac{v^{2}}{c^{2}}}`

### C064
- **description:** Height of free fall
- **formula:** `y = y_{0} + v_{0} t - \frac{1}{2} g t^{2}`

### C065
- **description:** Bulk modulus
- **formula:** `B = \frac{\text{bulk stress}}{\text{bulk strain}} = - \Delta p \frac{V_{0}}{\Delta V}`
