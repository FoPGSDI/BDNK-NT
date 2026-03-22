# Figure Analysis: Telegrapher's Equation Transition (Fig. telegraphers_plot.pdf)

**Reference:** paper.tex, Sec. III.D (lines 1242--1275), Fig. \ref{fig:telegraphers}

---

## 1. Visual Description

The figure consists of **three side-by-side panels**, each showing the spatial temperature profile T(x) at a different evolution time. Together, the panels illustrate the time evolution of a Gaussian hot spot in a BDNK fluid and its transition from diffusive (heat-equation-like) to wavelike (telegrapher/wave-equation-like) behavior as the dimensionless thermal conductivity parameter sigma-hat is increased.

- **Left panel (t = 16):** Early time. All three solutions show a single central temperature peak at x = 0 that is beginning to decay and spread outward, qualitatively resembling diffusion governed by the heat equation. The three curves are nearly overlapping at this early stage; the peak heights are approximately T ~ 1.075--1.08 and the profiles are sharply localized within |x| < ~25.

- **Middle panel (t = 39):** Intermediate time. The transition from diffusive to wavelike behavior becomes apparent. The sigma-hat = 0.15 solution (light gray) retains a smooth, single-peaked, diffusion-like profile that has broadened and decayed. The sigma-hat = 1.5 solution (medium gray) shows a slightly flattened top. The sigma-hat = 7.5 solution (black) exhibits clear **peak splitting**: the central maximum has divided into two distinct peaks propagating outward in opposite directions from the origin, characteristic of wave-equation solutions. An **inset** (zoomed view) is provided in the upper-right area of this panel, showing that even the sigma-hat = 0.15 solution possesses a small wavelike **transient** -- a tiny bump propagating outward at the sound speed ahead of the main diffusive profile.

- **Right panel (t = 312):** Late time. The sigma-hat = 0.15 (light gray) and sigma-hat = 1.5 (medium gray) solutions show broad, smooth, decayed Gaussian-like profiles centered near x = 0. The sigma-hat = 7.5 solution (black), however, displays a dramatic **oscillatory instability**: high-frequency oscillations have developed and spread across the domain (visible as rapid wiggles with |x| extending out to ~75 or more), signaling that the numerical simulation is approaching a crash. The central region of the sigma-hat = 7.5 profile has a broad, lower-amplitude hump superimposed with these oscillations.

---

## 2. Axes and Labels

- **Horizontal axis (all panels):** Spatial coordinate x, ranging from approximately -100 to +100 (tick marks at -75, 0, 75). Shared label "x" at the bottom center.
- **Vertical axis (shared, labeled on the left panel):** Temperature T, ranging from 1.000 to 1.100 (tick marks at 1.000, 1.025, 1.050, 1.075, 1.100). The background equilibrium temperature is T = 1.0 (i.e., delta = 1 in the initial data), so the plotted range shows the perturbation above equilibrium.
- **Time labels:** Each panel is annotated with a boxed label: t = 16 (left), t = 39 (middle), t = 312 (right).
- **Legend (left panel):** Three entries identifying the line styles by sigma-hat value.

---

## 3. Line Styles

Three curves appear in each panel, distinguished by **shading (gray scale)**:

| Curve | sigma-hat | tau-hat | Line shade | Description |
|-------|-----------|---------|------------|-------------|
| 1 | 0.15 | 1.5 | **Light gray** | Smallest conductivity; predominantly diffusive behavior |
| 2 | 1.5 | 15 | **Medium/dark gray** | Intermediate conductivity; mild departure from diffusive |
| 3 | 7.5 | 75 | **Black (darkest)** | Largest conductivity; strongly wavelike, eventually unstable |

All curves are solid lines. The progression from light to dark corresponds to increasing sigma-hat (and proportionally increasing tau-hat), visually encoding the transition from diffusive to wavelike regimes.

---

## 4. Key Observations

### 4.1 Heat-equation-like to telegrapher/wave-like transition

At early times (left panel, t = 16), all three solutions are qualitatively similar: a localized Gaussian hot spot decays and spreads, resembling diffusion. This is consistent with the fact that for short times the damping term (1/tau_epsilon) * dT/dt in the modified telegrapher's equation (Eq. 57 / eq:heat_t_BDNK) dominates, making the equation behave like a parabolic heat equation.

As time progresses, the wave-like principal part (d^2 T/dt^2 - c_B^2 d^2 T/dx^2) becomes increasingly important for larger sigma-hat and tau-hat. By t = 39 (middle panel), the sigma-hat = 7.5 solution has clearly transitioned to wave-like dynamics.

### 4.2 Peak splitting at large sigma-hat

The most visually striking feature is the **peak splitting** of the sigma-hat = 7.5 solution in the middle panel: the initially single Gaussian peak has separated into two counter-propagating peaks. This is the hallmark of a wave equation solution -- an initial pulse splits into left-moving and right-moving components. This behavior is expected from the modified telegrapher's equation in the limit tau_epsilon -> infinity with c_B^2 held finite, where it reduces to a pure 1D wave equation.

### 4.3 Inset showing transient at sound speed

The zoomed-in inset in the middle panel reveals that **all three** solutions, including the most diffusion-like sigma-hat = 0.15 case, possess *some* wavelike behavior. This manifests as a small transient (a tiny bump or wavefront) propagating outward ahead of the main diffusive profile at the sound speed. This demonstrates that BDNK theory is fundamentally hyperbolic even when the solution appears predominantly diffusive -- information propagates at finite speed, unlike in the parabolic Eckart/heat-equation formulation.

### 4.4 Oscillatory instability at sigma-hat = 7.5

In the right panel (t = 312), the sigma-hat = 7.5 solution develops an **oscillatory instability**: high-frequency spatial oscillations grow in amplitude across the domain. The paper states that this instability "eventually crashes the numerical simulation." This is a direct consequence of violating the linear stability constraint sigma-hat <= 1/3 (Eq. simple_constraints). Since sigma-hat = 7.5 >> 1/3, the solution is linearly unstable, and the instability has had sufficient time to grow to visible and eventually catastrophic amplitude.

Notably, the sigma-hat = 1.5 solution also violates the linear stability bound (1.5 > 1/3) but does **not** show visible instability at this time. The paper suggests two possible explanations: (a) the instability growth rate may be slow relative to the dynamical timescale, or (b) nonlinear mechanisms may stabilize the solution.

---

## 5. Numerical/Implementation Notes

### 5.1 Ratio sigma-hat / tau-hat = 0.1 held constant

Across all three simulations, the ratio sigma-hat / tau-hat = 0.1 is kept fixed:
- sigma-hat = 0.15, tau-hat = 1.5 => ratio = 0.1
- sigma-hat = 1.5, tau-hat = 15 => ratio = 0.1
- sigma-hat = 7.5, tau-hat = 75 => ratio = 0.1

This is done to keep the "thermal propagation speed" c_B^2 (which is proportional to sigma/tau_epsilon, equivalently sigma-hat/tau-hat) approximately constant across the three cases. The limit sigma, tau_epsilon -> infinity with c_B^2 finite then corresponds to increasing sigma-hat and tau-hat together -- which is exactly what the three cases represent in sequence.

### 5.2 Linear stability violation for sigma-hat > 1/3

The BDNK linear stability constraint (Eq. simple_constraints) requires:

    sigma-hat <= 1/3

Of the three cases:
- sigma-hat = 0.15: **satisfies** the constraint (0.15 < 1/3 ~ 0.333)
- sigma-hat = 1.5: **violates** the constraint (1.5 > 1/3)
- sigma-hat = 7.5: **violates** the constraint (7.5 >> 1/3)

All three cases possess **subluminal characteristic speeds** (i.e., the causality constraint on tau-hat is satisfied). It is only the stability constraint that is violated. The figure demonstrates that moderate violations (sigma-hat = 1.5) may be tolerable in practice, while large violations (sigma-hat = 7.5) lead to clear pathological behavior.

### 5.3 Initial data

The initial data are of the Gaussian heat-flow form (Eq. heat_flow_ID):

    T(0, x) = A * exp(-x^2 / w^2) + delta,  P(0, x) = P_0 = const.

with time-symmetric conditions: d(epsilon)/dt(0,x) = d(u^i)/dt(0,x) = 0. The constant pressure ensures that the dynamics are driven purely by the temperature gradient (pure heat flow), with no pressure-driven flow at t = 0. The implementation converts from (T, P) to the BDNK hydrodynamic variables (epsilon, n) using the ideal gas equation of state.

---

## 6. Connection to Theory

### 6.1 Modified telegrapher's equation (Eq. 57 / eq:heat_t_BDNK)

For constant transport coefficients, the BDNK heat flow equation reduces to a **modified telegrapher's equation**:

    0 = d^2 T/dt^2 - c_B^2 * d^2 T/dx^2 + (1/tau_epsilon) * dT/dt + l.o.t.

where:
- c_B^2 = c_h^2 * (1 - gamma * n / kappa), with c_h^2 = kappa * (Gamma - 1) / (n * tau_epsilon)
- The "l.o.t." (lower-order terms) involve spatial derivatives of n and T coupled through gamma.

This is a **damped wave equation** (telegrapher's equation) with:
- Wave speed: c_B (the "BDNK thermal propagation speed")
- Damping coefficient: 1/tau_epsilon
- Additional lower-order coupling terms from the BDNK frame

### 6.2 Wave equation limit: sigma, tau_epsilon -> infinity with c_B^2 finite

Since c_B^2 ~ kappa / (n * tau_epsilon) ~ sigma / tau_epsilon (using kappa = sigma * rho^2 / (n^2 * T)), holding sigma-hat / tau-hat constant ensures c_B^2 remains finite. In the limit sigma, tau_epsilon -> infinity:
- The damping term (1/tau_epsilon) * dT/dt -> 0 (damping vanishes)
- The lower-order terms -> 0 (they scale as 1/tau_epsilon)
- The equation reduces to: d^2 T/dt^2 = c_B^2 * d^2 T/dx^2

This is a simple **1D wave equation**, whose solutions are non-dispersive traveling waves. The figure numerically approximates this limit: as sigma-hat increases from 0.15 to 7.5 (with tau-hat increasing proportionally), the damping weakens and the solution transitions from diffusion-dominated to wave-dominated.

### 6.3 Hierarchy of hydrodynamic frames

The figure provides a numerical illustration of the theoretical hierarchy established in the constant-coefficient analysis:
- **Eckart frame** (tau_epsilon = 0): Heat equation (parabolic, acausal, unstable) -- not shown but provides the baseline intuition.
- **Small sigma-hat (0.15):** Telegrapher's equation with strong damping -- appears nearly diffusive but with finite-speed transients (visible in inset).
- **Large sigma-hat (7.5):** Telegrapher's equation approaching the wave equation limit -- peak splitting, minimal damping, but linear stability is violated.

### 6.4 Instability mechanism

The oscillatory instability at sigma-hat = 7.5 is related to the pressure relaxation equation (Eq. heat_x_soln):

    dP/dt = (1/tau_theta) * (P_0(t) - P)

where tau_theta = theta/n. In the BDNK frame, theta = -kappa + gamma*n + tau_P * n/(Gamma - 1). The stability condition theta >= 0 (equivalently, sigma-hat <= 1/3 for the chosen frame) ensures that the pressure relaxes *toward* equilibrium. When violated, the pressure deviates exponentially, producing the observed oscillatory instability.

---

## 7. Parameters

From Table I of the paper (line 559), the parameters for Fig. telegraphers are:

| Parameter | Value | Notes |
|-----------|-------|-------|
| Gamma | 4/3 | Adiabatic index (relativistic gas) |
| m | 0.1 | Particle rest mass parameter |
| V-hat | 2/15 | Combined viscosity parameter |
| sigma-hat | 0.15, 1.5, 7.5 | Dimensionless thermal conductivity |
| tau-hat | 1.5, 15, 75 | Dimensionless relaxation time |
| sigma-hat / tau-hat | 0.1 (constant) | Ensures c_B^2 is approximately constant |

**Derived quantities:**
- Sound speed squared: c_s^2 = (Gamma - 1)(1 + (Gamma - 1)/m) for the ideal gas (depends on local thermodynamic state)
- Linear stability bound: sigma-hat <= 1/3 ~ 0.333 (satisfied only by sigma-hat = 0.15)
- Causality bound on tau-hat: tau-hat >= (Gamma - 1)(2 - c_s^2) + c_s^2) / (1 - c_s^2) (satisfied by all three cases, as all have subluminal characteristics)

**Initial data parameters** (from Eq. heat_flow_ID): Gaussian temperature perturbation T(0,x) = A*exp(-x^2/w^2) + delta at constant pressure P_0. The peak temperature at t = 0 is approximately T ~ 1.1 (reading from the vertical axis), consistent with A ~ 0.1 and delta = 1.
