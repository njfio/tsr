# Track (b) Independent Rule-Applier Evaluation Packet

- **preregistration_commit_sha:** `463ad9f93c8a276b1e0d9ee497198dfa2169d079`
- **amendment_1_commit_sha:** `b66f48efb76e0f8d17d7db32848ad95f0a5c8633`
- **Card count:** 65 (C001..C065)

## Instructions

1. You are working in a clean, standalone session with zero access to external files, repositories, or background sources.
2. Apply **ONLY** the two *The Sovereign Mirror* (v57) rule passages and the term definitions reproduced verbatim below. Do **not** rely on external sources, outside knowledge, or infer the origin of any card.
3. Evaluate all `65` law cards (`C001`..`C065`) independently in the exact order presented. Do **not** group, sort, or omit any card.
4. For each card, assign `ruling` in `{"Keep", "Invert", "the rule doesn't say"}` and a one-line `rationale` citing which phrase of the quoted rule applies.
5. Return **ONLY** a valid JSON array of `65` objects in exact order `C001`..`C065` with exact keys `"card_id"`, `"ruling"`, and `"rationale"`:

```json
[
  {
    "card_id": "<card_id>",
    "ruling": "<Keep | Invert | the rule doesn't say>",
    "rationale": "<one-line rationale citing which phrase of the quoted rule applies>"
  }
]
```

## Locked Rule Passages and Term Definitions (*The Sovereign Mirror*, v57)

### Rule Passages

- **Chapter 2 (*The One Rule*), p. 20:**
> The main difference between the physical and the nonphysical is resistance. That’s the rule, or the start of it. Physics already measures resistance to a change in motion. It calls it mass. So you take the world Einstein described and reflect it: keep each relationship, and flip the condition. Resistant becomes receptive, limited becomes limitless, radiating becomes collecting. What comes out the other side is the nonphysical version. Every term reflects; that part always happens. What you have to know is whether the relationship keeps its shape or turns around. If it depends on resistance, or on the distance resistance makes, so that more mass or more separation means more of something, flipping resistant to receptive turns it around: more Movement means less of that thing, or it gets easier instead of harder. If it’s an identity or a definition, two names for one thing, [...], there’s nothing to turn around, even with mass in it; the terms reflect and the relationship keeps its shape. That’s the one rule.

- **Chapter 16 (*Twelve Reflections*), p. 116:**
> The rule from Chapter 2 does, whoever is running it, because it asks one question of every row: does this relationship depend on resistance, or on the distance resistance makes, or is it an identity, a definition, or the work of the one energy both sides share?

### Term Definitions

- **Two Environments (Chapter 1, p. 16):**
> There are two environments, the physical and the nonphysical, and they’re mirror images of each other. The physical is limited, resistant, and it radiates. The nonphysical is limitless, receptive, and it collects. Those three pairs aren’t three separate rules—they’re one condition seen three ways. Resistance creates a boundary, which makes a thing limited, and bounded things can only reach each other by radiating across the space between them. Take resistance away and there’s no boundary, so the nonphysical is limitless, and with nothing held apart, it collects instead of radiating. Everything else in TSR comes from what happens where they meet.

- **Resistance and "Physical" (Chapter 2, p. 25):**
> Resistance is resistance to change.
>
> Physical, in this book, is the resistant condition wherever it occurs, not matter as opposed to mind.

- **Space, Time, and Distance (Chapter 2, p. 21):**
> Think about what space and time actually do. On the physical side, where resistance gives things edges, space is what keeps two things from sitting in the same place, and time is what keeps everything from happening at once. Take resistance away and there’s no distance. Two particulars in the same whole don’t sit in different places; they differ by how they vibrate, the way two notes share the same air in a room. So space reflects as Vibration. And where nothing decays or comes apart, before and after are separated only by the whole becoming more than it was.

- **Nonphysical Movement (*The Map*, p. 175):**
> Receptivity to change in motion; a self-contained part of the whole, like a movement in a symphony. The reflection of mass.

- **The One Energy Both Sides Share (Chapter 16, p. 117; Chapter 17, pp. 131–132; *The Map*, p. 174):**
  - Chapter 16, p. 117:
> TSR has three: the two sides and the continuum where they meet, with one energy in it.
  - Chapter 17, p. 131:
> There aren’t two energies, one spiritual and one physical, taking turns. There’s one energy transmuting. On the nonphysical side it’s conscious energy: the Collective and Vibrational realities are made of it.
  - Chapter 17, p. 132:
> Where your Vibrational Reality meets your Subjective Reality, the two blend. I call that conscious-physical energy.
  - *The Map*, p. 174 (*Conscious-physical energy* entry):
> The blend of conscious and physical energy at the hinge, the E.

---

## Law Cards

### C001
- **what_it_says:** For an incompressible fluid in steady flow through a confined channel or streamtube with no fluid added or removed, the volume flow rate is the same across every cross section, expressed as A_1 v_1 = A_2 v_2.
- **quantities_related:** Cross-sectional areas at two locations along the flow path (A_1, A_2) and fluid flow speeds perpendicular to those cross sections (v_1, v_2).
- **conditions_to_hold:** Steady fluid flow of constant mass density (incompressible fluid) within a continuous pipe, channel, or streamtube having impermeable walls and no sources or sinks between sections 1 and 2, with uniform or cross-section-averaged flow speed across each cross section.

### C002
- **what_it_says:** When a solid object undergoes a small uniform temperature change, its change in length is proportional to its initial length and the temperature change, expressed as \Delta L = \alpha L \Delta T.
- **quantities_related:** Change in length (\Delta L), initial length (L), change in temperature (\Delta T), and coefficient of linear thermal expansion (\alpha).
- **conditions_to_hold:** Solid material body of finite initial length L subjected to a uniform temperature change \Delta T small enough that the linear expansion coefficient \alpha stays approximately constant, free of external mechanical constraints that prevent expansion or contraction, and without a phase transition.

### C003
- **what_it_says:** A standing wave confined to a one-dimensional region of length L with identical boundary conditions at both ends supports discrete harmonic wavelengths given by \lambda_n = (2 / n) L for n = 1, 2, 3, 4, 5, ...
- **quantities_related:** Allowed standing-wave wavelengths (\lambda_n), spatial length between the two boundaries (L), and positive integer harmonic mode number (n).
- **conditions_to_hold:** Linear wave propagation in a uniform, non-dispersive one-dimensional medium or cavity of fixed spatial separation L bounded at both ends by symmetric boundary conditions (either nodes at both ends or antinodes at both ends).

### C004
- **what_it_says:** The magnitude of the kinetic friction force opposing relative sliding between two contacting surfaces is proportional to the magnitude of the normal force pressing the surfaces together, expressed as f_k = \mu_k N.
- **quantities_related:** Magnitude of kinetic frictional force (f_k), coefficient of kinetic friction (\mu_k), and magnitude of normal contact force (N).
- **conditions_to_hold:** Direct macroscopic physical contact and active sliding (nonzero relative tangential velocity) between two solid surfaces under dry Coulomb friction conditions where \mu_k is approximately independent of apparent contact area and sliding speed.

### C005
- **what_it_says:** The coordinate time interval \Delta t measured in an inertial frame between two events occurring at a single clock moving at constant speed v is longer than the proper time interval \Delta \tau recorded by that moving clock, given by \Delta t = \gamma \Delta \tau = \Delta \tau / \sqrt{1 - v^2 / c^2}.
- **quantities_related:** Coordinate time interval in the observer's inertial frame (\Delta t), proper time interval measured in the clock's rest frame (\Delta \tau), relative frame speed (v), speed of light in vacuum (c), and Lorentz factor (\gamma).
- **conditions_to_hold:** Flat spacetime without significant gravitational time dilation, two inertial reference frames in uniform relative motion at constant speed v < c, \Delta \tau measured by one clock present at both events, and \Delta t measured using synchronized clocks at rest in the second inertial frame.

### C006
- **what_it_says:** For an unforced, linearly damped one-dimensional harmonic oscillator, the product of mass and acceleration plus the velocity-proportional damping force and displacement-proportional restoring force equals zero, expressed as m (d^2 x / dt^2) + b (dx / dt) + k x = 0.
- **quantities_related:** Oscillator mass (m), displacement from equilibrium (x), time (t), velocity (dx / dt), acceleration (d^2 x / dt^2), viscous damping coefficient (b), and linear restoring force constant (k).
- **conditions_to_hold:** Object of constant nonzero mass m moving along one axis in an inertial reference frame at non-relativistic speeds under a linear Hookean restoring force (-k x), a resistive damping force linearly proportional to velocity (-b dx / dt), and zero external driving force.

### C007
- **what_it_says:** Instantaneous angular velocity is defined as the instantaneous time derivative of angular position, expressed as \omega = \lim_{\Delta t \to 0} (\Delta \theta / \Delta t) = d\theta / dt.
- **quantities_related:** Instantaneous angular velocity (\omega), angular displacement (\Delta \theta), angular coordinate (\theta), time interval (\Delta t), and time (t).
- **conditions_to_hold:** Rotational or angular motion measured relative to a specified reference axis and reference direction, with angular position \theta(t) being a differentiable function of time t.

### C008
- **what_it_says:** The time required for a small satellite to complete one circular orbit of radius r around Earth is given by T = 2 \pi \sqrt{r^3 / (G M_E)}.
- **quantities_related:** Orbital period (T), orbital radius from Earth's center (r), universal gravitational constant (G), and mass of Earth (M_E).
- **conditions_to_hold:** Circular orbit at center-to-center distance r exceeding Earth's radius, satellite mass negligible compared to Earth's mass (m \ll M_E), spherically symmetric Earth mass distribution, inertial reference frame, Newtonian gravitation (weak field and v \ll c), and negligible atmospheric drag, thrust, or third-body gravitational perturbations.

### C009
- **what_it_says:** For an ideal gas, the molar heat capacity at constant pressure exceeds the molar heat capacity at constant volume by the universal molar gas constant, expressed as C_p = C_V + R.
- **quantities_related:** Molar heat capacity at constant pressure (C_p), molar heat capacity at constant volume (C_V), and universal molar gas constant (R).
- **conditions_to_hold:** Fixed molar quantity of an ideal gas (negligible intermolecular forces and molecular volume, so internal energy depends only on temperature and pV = nRT holds) undergoing quasi-static heating in thermal equilibrium without chemical reaction or phase change.

### C010
- **what_it_says:** For a system of particles, the time derivative of the total angular momentum vector equals the vector sum of all external torques acting on the system, expressed as d\vec{L} / dt = \sum \vec{\tau}.
- **quantities_related:** Total system angular momentum vector (\vec{L}), time (t), and net external torque vector (\sum \vec{\tau}).
- **conditions_to_hold:** System of massive particles observed in an inertial reference frame, with both \vec{L} and \vec{\tau} evaluated about the same fixed point in that inertial frame or about the system's center of mass, and pairwise internal interaction forces directed along the lines connecting particles (equal and opposite central forces) so net internal torque vanishes.

### C011
- **what_it_says:** A particle of rest mass m moving at speed v has total relativistic energy E = \gamma m c^2 and relativistic kinetic energy K = (\gamma - 1) m c^2, where \gamma = 1 / \sqrt{1 - v^2 / c^2}.
- **quantities_related:** Relativistic kinetic energy (K), total relativistic energy (E), invariant rest mass (m), particle speed (v), speed of light in vacuum (c), and Lorentz factor (\gamma).
- **conditions_to_hold:** Free particle with nonzero invariant rest mass (m > 0) moving at speed v < c relative to an inertial reference frame in flat spacetime, with external potential energy excluded from E.

### C012
- **what_it_says:** In thermodynamic equilibrium, the product of absolute pressure and volume of an ideal gas equals the number of molecules multiplied by Boltzmann's constant and absolute temperature, expressed as p V = N k_B T.
- **quantities_related:** Absolute gas pressure (p), container volume (V), number of gas molecules (N), Boltzmann constant (k_B), and absolute temperature (T).
- **conditions_to_hold:** Dilute gas enclosed within volume V in thermodynamic equilibrium at sufficiently low density and high temperature that molecular size, long-range intermolecular attractions, and quantum degeneracy effects are negligible, with interactions limited to brief elastic collisions.

### C013
- **what_it_says:** The spatial coordinate x' of an event in inertial frame S' moving at constant velocity v along the positive x-axis relative to inertial frame S is related to its coordinates (x, t) in S by x' = (x - v t) / \sqrt{1 - v^2 / c^2}.
- **quantities_related:** Spatial coordinate in frame S' (x'), spatial coordinate in frame S (x), coordinate time in frame S (t), relative velocity component along the x-axis (v), and speed of light in vacuum (c).
- **conditions_to_hold:** Flat spacetime, two inertial reference frames S and S' in standard configuration with parallel Cartesian axes, constant relative speed |v| < c along the shared x/x'-axis, and coinciding origins x = x' = 0 at t = t' = 0.

### C014
- **what_it_says:** For a fixed molar amount of an ideal gas held at constant temperature, the product of absolute pressure and volume remains constant between equilibrium states, expressed as P_1 V_1 = P_2 V_2 (constant T, n).
- **quantities_related:** Initial and final absolute pressures (P_1, P_2), initial and final gas volumes (V_1, V_2), constant absolute temperature (T), and constant molar amount of gas (n).
- **conditions_to_hold:** Closed system containing a constant amount n of dilute gas obeying ideal-gas behavior (negligible intermolecular forces and molecular volume), evaluated at two thermodynamic equilibrium states sharing the same uniform absolute temperature T.

### C015
- **what_it_says:** Every particle with nonzero rest mass moves at a speed strictly less than the vacuum speed of light c because the Lorentz factor \gamma and kinetic energy grow without bound as v approaches c, expressed as v < c (\gamma \to \infty as v \to c for m > 0).
- **quantities_related:** Particle speed relative to an inertial observer (v), speed of light in vacuum (c), invariant rest mass (m), and Lorentz factor (\gamma).
- **conditions_to_hold:** Particle or body with positive invariant rest mass (m > 0) moving locally through spacetime as measured in any inertial (or local inertial) reference frame under relativistic kinematics and the frame invariance of the vacuum speed of light c.

### C016
- **what_it_says:** A two-dimensional position-dependent force field has path-independent work (is conservative) when the spatial derivative of its x-component with respect to y equals the spatial derivative of its y-component with respect to x, expressed as (dF_x / dy) = (dF_y / dx).
- **quantities_related:** Cartesian force components (F_x, F_y) and planar spatial coordinates (x, y).
- **conditions_to_hold:** Two-dimensional force field \vec{F}(x, y) that depends solely on spatial position (independent of velocity, history, and explicit time) and has continuous first partial derivatives throughout a simply connected two-dimensional spatial domain.

### C017
- **what_it_says:** The component of a conservative force along a spatial coordinate direction l equals the negative derivative of the corresponding potential energy with respect to l, expressed as F_l = - dU / dl.
- **quantities_related:** Conservative force component along direction l (F_l), potential energy (U), and spatial position or displacement coordinate along that direction (l).
- **conditions_to_hold:** Force is conservative (work done depends only on initial and final positions and not on path), allowing a single-valued, differentiable potential energy function U(l) over the spatial region.

### C018
- **what_it_says:** Massive bodies create gravitational potential wells and curve surrounding spacetime, causing electromagnetic waves propagating outward from deeper gravitational potential to shift to lower frequency and longer wavelength (gravitational redshift) and bending light rays passing near a massive body (gravitational lensing).
- **quantities_related:** Mass-energy of the gravitating body, radial spatial distance from the mass, gravitational potential or spacetime metric, emitted and observed frequencies and wavelengths of light, and light deflection angle.
- **conditions_to_hold:** Non-uniform gravitational field or curved spacetime produced by localized mass-energy, with electromagnetic radiation propagating between locations of differing gravitational potential or past a massive gravitating object in accordance with general relativity and the equivalence principle.

### C019
- **what_it_says:** The coefficient of performance of a heat pump equals the ratio of heat delivered to the hot reservoir to the net work input per cycle, expressed as K_P = Q_h / W = Q_h / (Q_h - Q_c).
- **quantities_related:** Heat pump coefficient of performance (K_P), heat transferred to the hot reservoir per cycle (Q_h), heat absorbed from the cold reservoir per cycle (Q_c), and net work input per cycle (W).
- **conditions_to_hold:** Device operating in a closed thermodynamic cycle (\Delta U = 0 over a complete cycle so W = Q_h - Q_c by energy conservation) transferring heat between a cold reservoir and a hot reservoir with positive net work input W > 0.

### C020
- **what_it_says:** When a solid or liquid undergoes a small uniform change in temperature, its change in volume is proportional to its initial volume and the temperature change, expressed as \Delta V = \beta V \Delta T.
- **quantities_related:** Change in volume (\Delta V), initial volume (V), change in temperature (\Delta T), and coefficient of volume thermal expansion (\beta).
- **conditions_to_hold:** Continuous solid or liquid of finite initial volume V undergoing a uniform temperature change \Delta T at constant external pressure, over a small temperature interval in which \beta remains approximately constant and no phase transition occurs.

### C021
- **what_it_says:** A small rigid sphere of radius r moving slowly at speed v through a viscous fluid of dynamic viscosity \eta experiences a resistive drag force of magnitude F_s = 6 \pi r \eta v.
- **quantities_related:** Viscous drag force magnitude (F_s), sphere radius (r), fluid dynamic viscosity (\eta), and relative speed between the sphere and distant fluid (v).
- **conditions_to_hold:** Rigid spherical body moving steadily through a homogeneous, unbounded, incompressible Newtonian fluid with no-slip contact at the sphere's surface and very low Reynolds number (Re \ll 1, laminar creeping flow with negligible inertial forces, turbulence, or container-wall interference).

### C022
- **what_it_says:** In an isolated system with no energy crossing its boundary, the total energy of the system remains constant between any initial and final states, expressed as E_i = E_f (\Delta E_sys = 0).
- **quantities_related:** Initial total energy of the system (E_i), final total energy of the system (E_f), and net change in total system energy (\Delta E_sys).
- **conditions_to_hold:** Isolated physical system exchanging zero mechanical work, zero heat, zero radiation, and zero matter with its surroundings, evaluated within a single inertial reference frame under time-independent fundamental physical laws.

### C023
- **what_it_says:** The fundamental laws of physics—spanning mechanics, electromagnetism, optics, and thermodynamics—take the same mathematical form in all inertial reference frames.
- **quantities_related:** Physical observables, dynamical variables, fields, and spacetime coordinates measured in inertial reference frames moving at constant velocity relative to one another.
- **conditions_to_hold:** Observers occupy inertial (unaccelerated, non-rotating) reference frames in flat spacetime, or local freely falling inertial frames over small spacetime regions where gravitational tidal effects are negligible.

### C024
- **what_it_says:** The net work done by the resultant force acting on a particle moving from position A to position B equals the change in the particle's kinetic energy, expressed as W_net = K_B - K_A.
- **quantities_related:** Net work done by all forces (W_net), initial kinetic energy at A (K_A), and final kinetic energy at B (K_B), along with net force, displacement, mass, and speed.
- **conditions_to_hold:** Point particle (or rigid body in pure translation without rotation or internal deformation) of constant mass analyzed in an inertial reference frame.

### C025
- **what_it_says:** The impulse imparted by a force over the time interval from t_i to t_f is the time integral of the force vector, equivalently written in terms of time-averaged force as \vec{J} \equiv \int_{t_i}^{t_f} \vec{F}(t) dt or \vec{J} = \vec{F}_ave \Delta t.
- **quantities_related:** Impulse vector (\vec{J}), instantaneous force vector (\vec{F}(t)), time-averaged force vector (\vec{F}_ave), initial and final times (t_i, t_f), and elapsed time interval (\Delta t = t_f - t_i).
- **conditions_to_hold:** Force vector \vec{F}(t) is integrable with respect to time over the finite interval [t_i, t_f] in a chosen reference frame (equaling the change in linear momentum \Delta \vec{p} when \vec{F} is the net external force in an inertial frame).

### C026
- **what_it_says:** Near Earth's surface, the mechanical work done by Earth's gravitational force on an object of mass m moving from vertical height y_A to vertical height y_B is W_{grav, AB} = - m g (y_B - y_A).
- **quantities_related:** Work done by gravity from A to B (W_{grav, AB}), object mass (m), magnitude of gravitational acceleration near Earth's surface (g), initial vertical coordinate (y_A), and final vertical coordinate (y_B).
- **conditions_to_hold:** Object of constant mass m moving over vertical displacements small compared to Earth's radius so the gravitational field has constant magnitude g and uniform downward direction, with the vertical coordinate y measured positive upward.

### C027
- **what_it_says:** The vector sum of external forces acting on an object of constant mass equals the product of its mass and its acceleration vector, expressed as \vec{F}_net = m \vec{a}.
- **quantities_related:** Net external force vector (\vec{F}_net), inertial mass (m), and acceleration vector (\vec{a}).
- **conditions_to_hold:** Particle or system center of mass having constant mass m, measured in an inertial reference frame at speeds much smaller than the speed of light (v \ll c).

### C028
- **what_it_says:** The coordinate time t of an event in inertial frame S is related to its coordinate time t' and position x' in inertial frame S' moving at velocity v along the positive x-axis relative to S by t = (t' + v x' / c^2) / \sqrt{1 - v^2 / c^2}.
- **quantities_related:** Coordinate time in frame S (t), coordinate time in frame S' (t'), spatial coordinate along the motion axis in frame S' (x'), relative frame velocity along x (v), and speed of light in vacuum (c).
- **conditions_to_hold:** Flat spacetime, two inertial reference frames S and S' in standard configuration with parallel spatial axes, constant relative velocity v (|v| < c) of S' along the positive x-axis of S, synchronized clocks in each frame, and coinciding spacetime origins at x = x' = 0, t = t' = 0.

### C029
- **what_it_says:** For one-dimensional simple harmonic motion with displacement x(t) = A \cos(\omega t + \phi), the instantaneous velocity as a function of time is v(t) = - A \omega \sin(\omega t + \phi).
- **quantities_related:** Instantaneous velocity (v(t)), oscillation amplitude (A), angular frequency (\omega), time (t), and phase constant (\phi).
- **conditions_to_hold:** Undamped, unforced linear one-dimensional simple harmonic motion about x = 0 following the cosine displacement phase convention x(t) = A \cos(\omega t + \phi) with constant A and \omega.

### C030
- **what_it_says:** Along a curved trajectory, a particle's total instantaneous acceleration vector equals the vector sum of its centripetal (normal) acceleration and its tangential acceleration, expressed as \vec{a} = \vec{a}_C + \vec{a}_T.
- **quantities_related:** Total acceleration vector (\vec{a}), centripetal acceleration vector perpendicular to velocity toward the center of curvature (\vec{a}_C), and tangential acceleration vector parallel to velocity (\vec{a}_T).
- **conditions_to_hold:** Smooth, twice-differentiable particle trajectory in two or three spatial dimensions having well-defined instantaneous tangent and normal directions.

### C031
- **what_it_says:** Small-amplitude sound waves propagate through an ideal gas at speed v = \sqrt{\gamma R T / M}.
- **quantities_related:** Speed of sound (v), adiabatic heat-capacity ratio (\gamma = C_p / C_V), universal molar gas constant (R), absolute equilibrium temperature (T), and molar mass of the gas (M).
- **conditions_to_hold:** Homogeneous, stationary ideal gas in local thermodynamic equilibrium transmitting small-amplitude (linear acoustic) longitudinal waves whose compressions and rarefactions occur rapidly enough to be adiabatic (negligible thermal conduction and viscous dissipation) while remaining quasi-static at the molecular collision scale.

### C032
- **what_it_says:** For a body of uniform mass density, mass equals the product of density and volume, equivalently defining density as mass per unit volume: m = \rho V (\rho = m / V).
- **quantities_related:** Mass (m), mass density (\rho), and occupied three-dimensional volume (V).
- **conditions_to_hold:** Material body or continuum sample occupying nonzero volume V > 0 with spatially uniform density \rho (or with \rho representing the volume-averaged mass density over V).

### C033
- **what_it_says:** The moment of inertia of a collection of discrete particles about a given rotation axis equals the sum over all particles of each particle's mass multiplied by the square of its perpendicular distance from the axis, expressed as I = \sum_j m_j r_j^2.
- **quantities_related:** Moment of inertia about the specified axis (I), individual particle masses (m_j), and perpendicular distances of the particles from the rotation axis (r_j).
- **conditions_to_hold:** Discrete system of point masses evaluated relative to a well-defined axis in classical mechanics (with fixed perpendicular distances r_j required for I to remain constant during rigid-body rotation).

### C034
- **what_it_says:** Young's modulus characterizes the axial stiffness of an elastic solid as the ratio of tensile stress to tensile strain, expressed as Y = (tensile stress) / (tensile strain) = (F_\perp / A)(L_0 / \Delta L).
- **quantities_related:** Young's modulus (Y), axial force perpendicular to the cross section (F_\perp), cross-sectional area (A), initial unstrained length (L_0), length change (\Delta L), tensile stress (F_\perp / A), and tensile strain (\Delta L / L_0).
- **conditions_to_hold:** Homogeneous, isotropic solid bar or rod of uniform cross-sectional area A and nonzero initial length L_0 subjected to small uniaxial tension or compression within the linear Hookean elastic limit at constant temperature, without buckling or plastic yield.

### C035
- **what_it_says:** There is no preferred inertial rest frame in nature; only relative velocity between inertial frames is physically observable, and all inertial frames are completely equivalent for describing physical phenomena.
- **quantities_related:** Relative velocity between inertial frames, spacetime coordinates, and mechanical, electromagnetic, and optical observables measured within inertial frames.
- **conditions_to_hold:** Reference frames are inertial (free of linear acceleration and rotation) in flat spacetime, or locally inertial over small spacetime regions where gravitational curvature and tidal forces are negligible.

### C036
- **what_it_says:** The adiabatic index \gamma is the dimensionless ratio of molar heat capacity at constant pressure to molar heat capacity at constant volume, expressed as \gamma = C_p / C_V.
- **quantities_related:** Heat-capacity ratio or adiabatic index (\gamma), molar heat capacity at constant pressure (C_p), and molar heat capacity at constant volume (C_V).
- **conditions_to_hold:** Thermodynamic substance in equilibrium having well-defined, finite, nonzero molar heat capacities C_p and C_V > 0 at the state of interest (away from first-order phase transitions).

### C037
- **what_it_says:** Two spatially separated events that occur simultaneously in one inertial frame (\Delta t' = 0) are not simultaneous in another inertial frame moving at relative speed v along their separation axis, differing in coordinate time by \Delta t = (\gamma v \Delta x) / c^2 (for \Delta t' = 0).
- **quantities_related:** Coordinate time separation in the second inertial frame (\Delta t), zero time separation in the simultaneity frame (\Delta t' = 0), spatial separation along the direction of relative motion (\Delta x), relative frame speed (v), speed of light in vacuum (c), and Lorentz factor (\gamma).
- **conditions_to_hold:** Flat spacetime, two inertial reference frames in uniform relative motion at constant speed v < c, nonzero spatial separation between the two events along the axis of relative motion, synchronized coordinate clocks in each frame, and \Delta x denoting the rest-frame separation in the frame where \Delta t' = 0.

### C038
- **what_it_says:** The acceleration of the center of mass of an N-particle system of total mass M equals the mass-weighted sum of the individual particle accelerations divided by M, expressed as \vec{a}_CM = (d^2 / dt^2)((1 / M) \sum_{j=1}^N m_j \vec{r}_j) = (1 / M) \sum_{j=1}^N m_j \vec{a}_j.
- **quantities_related:** Center-of-mass acceleration vector (\vec{a}_CM), total mass (M), individual particle masses (m_j), particle position vectors (\vec{r}_j), particle acceleration vectors (\vec{a}_j), particle count (N), and time (t).
- **conditions_to_hold:** System of N particles with constant individual masses m_j, nonzero total mass M = \sum_{j=1}^N m_j > 0, and twice-differentiable position vectors \vec{r}_j(t) in classical non-relativistic kinematics.

### C039
- **what_it_says:** For laminar shear flow of a fluid layer of thickness L between two parallel plates of area A where tangential force F keeps one plate moving at constant speed v relative to the other, the fluid's dynamic viscosity is \eta = F L / (v A).
- **quantities_related:** Dynamic viscosity (\eta), tangential shear force (F), perpendicular separation between plates (L), relative tangential plate speed (v), and plate area in contact with the fluid (A).
- **conditions_to_hold:** Steady, laminar planar Couette flow of a homogeneous Newtonian fluid at constant temperature between parallel plates separated by small gap L, with no-slip boundary conditions at both solid surfaces, a uniform linear velocity profile across L, and zero pressure gradient.

### C040
- **what_it_says:** A body or particle with invariant rest mass m possesses an intrinsic rest energy equal to its mass multiplied by the square of the speed of light in vacuum, expressed as E_0 = m c^2.
- **quantities_related:** Rest energy (E_0), invariant rest mass (m), and speed of light in vacuum (c).
- **conditions_to_hold:** Particle or closed physical system evaluated in its center-of-momentum rest frame (zero net momentum, v = 0) in relativistic physics (flat spacetime or a local inertial frame).

### C041
- **what_it_says:** When a fixed quantity of an ideal gas undergoes a quasi-static adiabatic process with constant heat capacities, its pressure and volume satisfy p V^\gamma = constant.
- **quantities_related:** Absolute gas pressure (p), gas volume (V), and adiabatic index / ratio of molar heat capacities (\gamma = C_p / C_V).
- **conditions_to_hold:** Closed system of fixed molar amount of an ideal gas in a thermally insulated container (zero heat transfer, Q = 0) undergoing a reversible, quasi-static expansion or compression over a temperature range in which \gamma = C_p / C_V remains constant.

### C042
- **what_it_says:** In flat spacetime, the squared spacetime interval between any two events, defined by s^2 = c^2 (\Delta t)^2 - (\Delta x)^2 - (\Delta y)^2 - (\Delta z)^2, takes the exact same value in every inertial reference frame.
- **quantities_related:** Squared spacetime interval (s^2), speed of light in vacuum (c), coordinate time difference between two events (\Delta t), and Cartesian spatial coordinate differences (\Delta x, \Delta y, \Delta z).
- **conditions_to_hold:** Flat Minkowski spacetime free of gravitational curvature, with time and space separations measured using synchronized clocks and orthogonal Cartesian axes in inertial reference frames under the (+, -, -, -) sign convention.

### C043
- **what_it_says:** Angular wave number k is defined as 2\pi radians divided by the spatial wavelength of a periodic wave, expressed as k \equiv 2 \pi / \lambda.
- **quantities_related:** Angular wave number (k) and wavelength (\lambda).
- **conditions_to_hold:** Spatially periodic sinusoidal wave having a well-defined nonzero wavelength \lambda > 0.

### C044
- **what_it_says:** The coefficient of performance of a reversible (Carnot) refrigerator operating between a cold reservoir at absolute temperature T_c and a hot reservoir at absolute temperature T_h is K_R = T_c / (T_h - T_c).
- **quantities_related:** Reversible refrigerator coefficient of performance (K_R), cold-reservoir absolute temperature (T_c), and hot-reservoir absolute temperature (T_h).
- **conditions_to_hold:** Thermodynamic refrigeration cycle operating fully reversibly (zero entropy generation per cycle) between two isothermal thermal reservoirs whose temperatures T_c and T_h are measured on an absolute (Kelvin) scale with 0 < T_c < T_h.

### C045
- **what_it_says:** For one-dimensional motion with constant acceleration a starting from initial position x_0 and initial velocity v_0 at t = 0, position as a function of time is x = x_0 + v_0 t + (1/2) a t^2.
- **quantities_related:** Position at time t (x), initial position at t = 0 (x_0), initial velocity at t = 0 (v_0), constant acceleration (a), and elapsed time (t).
- **conditions_to_hold:** Motion constrained to one spatial axis in which acceleration a remains constant in both magnitude and sign throughout the elapsed time interval from 0 to t.

### C046
- **what_it_says:** A rigid, circularly symmetric object of mass m, outer radius r, and center-of-mass moment of inertia I_CM rolling without slipping down a plane inclined at angle \theta to the horizontal accelerates down the incline with magnitude a_CM = (m g \sin \theta) / (m + (I_CM / r^2)).
- **quantities_related:** Center-of-mass linear acceleration magnitude (a_CM), object mass (m), gravitational acceleration magnitude (g), incline angle (\theta), moment of inertia about the symmetry axis through the center of mass (I_CM), and outer rolling radius (r).
- **conditions_to_hold:** Rigid, axially symmetric body rolling without slipping (v_CM = \omega r, static friction acts without sliding dissipation) down a stationary planar incline in a uniform gravitational field g, observed in an inertial frame with negligible air drag and rolling resistance.

### C047
- **what_it_says:** In steady-state one-dimensional thermal conduction across a slab of area A and thickness d between boundary temperatures T_h and T_c, the rate of heat flow is P = k A (T_h - T_c) / d.
- **quantities_related:** Rate of conductive heat transfer (P), material thermal conductivity (k), cross-sectional area perpendicular to heat flow (A), hot-boundary temperature (T_h), cold-boundary temperature (T_c), and slab thickness (d).
- **conditions_to_hold:** Steady-state, one-dimensional conductive heat flow through a homogeneous, isotropic solid or stationary medium of uniform cross section A and nonzero thickness d > 0, constant uniform face temperatures T_h and T_c, constant thermal conductivity k, no lateral heat loss, and no internal heat sources or convection.

### C048
- **what_it_says:** For an object of mass m resting in vertical equilibrium on a horizontal surface with no other vertical forces present, the magnitude of the upward normal contact force equals the object's weight, expressed as N = m g.
- **quantities_related:** Normal force magnitude (N), object mass (m), and magnitude of local gravitational acceleration (g).
- **conditions_to_hold:** Object in contact with a flat, stationary horizontal surface (zero incline angle), zero vertical acceleration in an inertial reference frame, uniform downward gravitational acceleration g, and no additional vertical forces (such as tension, applied vertical loads, or buoyancy).

### C049
- **what_it_says:** When a stationary wave source emits waves of frequency f_s that travel at speed v through a stationary medium, an observer moving along the line to the source at speed v_o toward (+) or away from (-) the source measures frequency f_o = f_s ((v \pm v_o) / v).
- **quantities_related:** Observed frequency (f_o), emitted source frequency (f_s), wave speed relative to the medium (v), and observer speed relative to the medium (v_o).
- **conditions_to_hold:** Non-relativistic periodic mechanical wave (such as sound, with v, v_o \ll c) propagating through a homogeneous, stationary medium, source at rest relative to the medium, and observer moving collinearly toward (+) or away from (-) the source (with v_o \le v when receding).

### C050
- **what_it_says:** Within a sufficiently small spacetime region, all local physical effects in a uniform gravitational field are indistinguishable from those in a uniformly accelerating reference frame in gravity-free space, whereas a freely falling non-rotating frame forms a local inertial frame in which gravitational acceleration vanishes locally.
- **quantities_related:** Gravitational acceleration, reference-frame acceleration, inertial mass, gravitational mass, and local trajectories of test bodies and light rays.
- **conditions_to_hold:** Exact proportionality (equality) of inertial mass and gravitational mass, and restriction to a local spatial volume and time interval small enough that spatial variations and time derivatives of the gravitational field (tidal forces and curvature effects) are negligible.

### C051
- **what_it_says:** For a small body in a bound elliptical or circular orbit of semi-major axis a around a central body of much larger mass M, the square of the orbital period is proportional to the cube of the semi-major axis, expressed as T^2 = (4 \pi^2 / (G M)) a^3.
- **quantities_related:** Orbital period (T), universal gravitational constant (G), central body mass (M), and orbital semi-major axis (a).
- **conditions_to_hold:** Closed two-body orbit governed by Newtonian inverse-square gravitation in an inertial frame, orbiting body's mass m negligible compared to central mass M (m \ll M), spherically symmetric or point-like bodies separated beyond contact, and negligible drag, relativistic precession, or third-body perturbations.

### C052
- **what_it_says:** In three-dimensional Cartesian coordinates, a particle's instantaneous velocity vector at time t is written in terms of its orthogonal velocity components as \vec{v}(t) = v_x(t) \hat{i} + v_y(t) \hat{j} + v_z(t) \hat{k}.
- **quantities_related:** Instantaneous velocity vector (\vec{v}(t)), scalar Cartesian velocity components (v_x(t), v_y(t), v_z(t)), fixed orthogonal unit vectors (\hat{i}, \hat{j}, \hat{k}), and time (t).
- **conditions_to_hold:** Three-dimensional Euclidean coordinate system using a stationary, non-rotating orthonormal Cartesian basis (\hat{i}, \hat{j}, \hat{k}) and differentiable particle coordinates as functions of time.

### C053
- **what_it_says:** An object maintains a constant velocity vector (remaining at rest or moving in a straight line at constant speed) whenever the net external force acting on it is zero, expressed as \vec{v} = constant when \vec{F}_net = \vec{0} N.
- **quantities_related:** Object velocity vector (\vec{v}) and net external force vector acting on the object (\vec{F}_net).
- **conditions_to_hold:** Motion observed in an inertial (unaccelerated, non-rotating) reference frame for a particle or the center of mass of a body subject to zero resultant external force.

### C054
- **what_it_says:** Whenever body A exerts a force \vec{F}_{AB} on body B, body B simultaneously exerts an equal in magnitude and oppositely directed force \vec{F}_{BA} on body A, expressed as \vec{F}_{AB} = - \vec{F}_{BA}.
- **quantities_related:** Force vector exerted by body A on body B (\vec{F}_{AB}) and force vector exerted by body B on body A (\vec{F}_{BA}).
- **conditions_to_hold:** Mutual pairwise interaction between two distinct bodies A and B in classical Newtonian mechanics where interaction propagation delays and momentum carried by radiation or time-varying fields are negligible.

### C055
- **what_it_says:** The phase speed of a sinusoidal traveling wave equals its angular frequency divided by its angular wave number, expressed as v = \omega / k.
- **quantities_related:** Wave phase speed (v), angular frequency (\omega), and angular wave number (k).
- **conditions_to_hold:** Harmonic (monochromatic sinusoidal) traveling wave with well-defined angular frequency \omega and nonzero angular wave number k > 0 measured in a given reference frame.

### C056
- **what_it_says:** In fixed three-dimensional Cartesian coordinates, a particle's instantaneous acceleration vector equals the sum of the second time derivatives of its Cartesian position coordinates along the unit basis vectors: \vec{a}(t) = (d^2 x(t) / dt^2) \hat{i} + (d^2 y(t) / dt^2) \hat{j} + (d^2 z(t) / dt^2) \hat{k}.
- **quantities_related:** Instantaneous acceleration vector (\vec{a}(t)), Cartesian coordinates (x(t), y(t), z(t)), time (t), second time derivatives (d^2 x / dt^2, d^2 y / dt^2, d^2 z / dt^2), and Cartesian unit vectors (\hat{i}, \hat{j}, \hat{k}).
- **conditions_to_hold:** Three-dimensional Euclidean space parameterized by a fixed (time-independent, non-rotating) orthonormal Cartesian basis (\hat{i}, \hat{j}, \hat{k}), with x(t), y(t), and z(t) twice differentiable with respect to time t.

### C057
- **what_it_says:** In simple harmonic motion, the maximum speed of the oscillating object equals the product of its displacement amplitude and its angular frequency, expressed as |v_max| = A \omega.
- **quantities_related:** Maximum speed (|v_max|), displacement amplitude (A), and angular frequency (\omega).
- **conditions_to_hold:** Undamped, unforced sinusoidal simple harmonic motion along one coordinate with constant amplitude A \ge 0 and constant angular frequency \omega \ge 0.

### C058
- **what_it_says:** For one-dimensional motion with constant acceleration, the average velocity over any time interval equals half the sum of the initial and final velocities, expressed as \bar{v} = (v_0 + v) / 2.
- **quantities_related:** Time-averaged velocity (\bar{v}), initial velocity (v_0), and final velocity (v).
- **conditions_to_hold:** One-dimensional kinematics in which instantaneous acceleration remains constant throughout the entire time interval so velocity changes linearly with time.

### C059
- **what_it_says:** For a classical ideal gas whose molecules possess d active quadratic degrees of freedom, the molar heat capacity at constant volume is C_V = (d / 2) R.
- **quantities_related:** Molar heat capacity at constant volume (C_V), number of active quadratic degrees of freedom per molecule (d), and universal molar gas constant (R).
- **conditions_to_hold:** Ideal gas in thermal equilibrium at temperatures where classical equipartition of energy holds across the d active translational, rotational, and vibrational quadratic modes (k_B T much greater than quantum spacing of the active modes, much smaller than spacing of unexcited higher modes, and constant d).

### C060
- **what_it_says:** Mass, energy, and momentum curve the four-dimensional geometry of spacetime, and freely moving matter and radiation follow geodesics of that curved spacetime geometry, producing gravitational attraction and orbital motion.
- **quantities_related:** Mass-energy-momentum distribution, four-dimensional spacetime metric and curvature, and geodesic worldlines of particles and light.
- **conditions_to_hold:** Classical relativistic gravitation in four-dimensional Lorentzian spacetime (valid across weak and strong gravitational fields outside quantum-gravity scales), reducing to flat Minkowski spacetime when mass-energy vanishes and to Newtonian gravity for weak fields and speeds v \ll c.

### C061
- **what_it_says:** Every pair of point masses m_1 and m_2 separated by distance r attracts one another with a gravitational force proportional to m_1 m_2 and inversely proportional to r^2 along the line joining them, expressed as \vec{F}_{12} = G (m_1 m_2 / r^2) \hat{r}_{12}.
- **quantities_related:** Gravitational force vector on mass 1 due to mass 2 (\vec{F}_{12}), universal gravitational constant (G), interacting masses (m_1, m_2), separation distance between centers (r), and unit vector along the line between the masses (\hat{r}_{12}, directed from mass 1 toward mass 2 in the given attractive form).
- **conditions_to_hold:** Point particles or non-overlapping spherically symmetric bodies separated by distance r > 0, evaluated in the classical weak-field, slow-motion Newtonian limit (v \ll c and gravitational potential magnitude \ll c^2).

### C062
- **what_it_says:** An ideal linear spring displaced by \vec{x} from its relaxed equilibrium configuration exerts a restoring force proportional to the displacement and opposite in direction, expressed as \vec{F} = - k \vec{x}.
- **quantities_related:** Restoring spring force vector (\vec{F}), spring stiffness constant (k), and displacement vector from the relaxed equilibrium position (\vec{x}).
- **conditions_to_hold:** Elastic spring or Hookean element deformed within its proportional linear elastic limit (small displacements without plastic yielding, buckling, or coil contact) and negligible spring inertia when transmitting static or slowly varying forces.

### C063
- **what_it_says:** An object having proper length L_0 in its rest frame is measured by an inertial observer moving at relative speed v parallel to that length to have a contracted length L = L_0 / \gamma = L_0 \sqrt{1 - v^2 / c^2}.
- **quantities_related:** Contracted length measured in the observer's frame (L), proper length in the object's rest frame (L_0), relative speed between inertial frames (v), speed of light in vacuum (c), and Lorentz factor (\gamma).
- **conditions_to_hold:** Flat spacetime, two inertial reference frames in uniform relative motion at constant speed v < c, length oriented parallel to the direction of relative velocity, and both endpoints of the moving object located simultaneously in the observer's inertial frame.

### C064
- **what_it_says:** An object in vertical free fall from initial height y_0 with initial vertical velocity v_0 at t = 0 under constant downward gravitational acceleration g has vertical height y = y_0 + v_0 t - (1/2) g t^2.
- **quantities_related:** Vertical height at time t (y), initial height at t = 0 (y_0), initial vertical velocity component at t = 0 (v_0), downward gravitational acceleration magnitude (g), and elapsed time (t).
- **conditions_to_hold:** Motion governed solely by gravity (negligible air drag, buoyancy, and propulsion) over vertical displacements small enough that gravitational acceleration g remains uniform in magnitude and downward direction, measured in an inertial frame with the positive y-axis directed upward.

### C065
- **what_it_says:** Bulk modulus measures a material's resistance to uniform hydrostatic compression as the ratio of bulk stress to bulk strain, expressed as B = (bulk stress) / (bulk strain) = - \Delta p (V_0 / \Delta V).
- **quantities_related:** Bulk modulus (B), change in uniform pressure (\Delta p), initial volume (V_0), volume change (\Delta V), bulk stress (- \Delta p or \Delta p), and volumetric strain (\Delta V / V_0).
- **conditions_to_hold:** Homogeneous isotropic solid, liquid, or gas of nonzero initial volume V_0 > 0 subjected to a small, spatially uniform change in hydrostatic pressure \Delta p within the linear reversible compression range under specified thermal conditions (isothermal or adiabatic) and away from phase transitions.
