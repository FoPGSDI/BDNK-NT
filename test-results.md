# Test Results: Comprehensive Documentation of All Numerical Tests

## Reference

All tests derive from: Pandya, Most, Pretorius, "Causal, stable first-order viscous relativistic hydrodynamics with ideal gas microphysics" (paper.tex), Section III (Results) and Appendix B (Numerical algorithms and convergence tests).

---

## 1. Physical Glossary and Parameter Definitions

### 1.1 Key Physical Quantities

| Quantity | Symbol | Definition | Role in Tests |
|----------|--------|------------|---------------|
| Adiabatic index | $\Gamma$ | EOS parameter, $\Gamma \in (1,2)$ | Set to $4/3$ in all tests |
| Particle rest mass | $m$ | Baryon mass | Controls rest-mass energy density $mn$ |
| Combined viscosity | $V$ | $V \equiv \frac{4\eta}{3} + \zeta$ | Determines dissipation strength |
| Inverse Reynolds number | $\hat{V}$ | $\hat{V} \equiv V/(\rho c_s^2 L)$ | Dimensionless viscosity |
| Dimensionless thermal conductivity | $\hat{\sigma}$ | $\sigma = \hat{V} L \rho c_s^2 / (-\kappa_\epsilon) \cdot \hat{\sigma}$ | Controls heat flow strength |
| Dimensionless relaxation time | $\hat{\tau}$ | $\tau_\epsilon = \tau_Q = L \hat{V} \hat{\tau}$ | Controls characteristic speeds |
| Sound speed squared | $c_s^2$ | $c_s^2 = \Gamma P / \rho$ | Propagation speed of inviscid modes |
| Relaxation times | $\tau_\epsilon, \tau_P, \tau_Q$ | (ref: paper Eq. 41) | Timescales over which dissipation acts |

### 1.2 Characteristic Speeds

The BDNK equations possess three families of characteristic speeds (ref: paper Eq. A15--A16):

| Speed | Symbol | Expression | Role |
|-------|--------|------------|------|
| Maximum BDNK speed | $c_+$ | Larger root of $c_\pm^2$ polynomial (ref: paper Eq. A15) | Determines causality; must satisfy $\|c_+\| < 1$ for causal propagation |
| Smaller nonzero speed | $c_-$ | Smaller root of $c_\pm^2$ polynomial (ref: paper Eq. A15) | Secondary characteristic; related to shockwave ODE singularity |
| Third characteristic speed | $c_1$ | $c_1^2 = c_s^2 \eta/(V \hat{\tau})$ (ref: paper Eq. A16) | Associated with shear mode |

Causality is guaranteed when all $|c_+|, |c_-|, |c_1| < 1$.

### 1.3 Constraint Summary

For the frame ansatz used in this paper (ref: paper Eq. 41), all BDNK constraints reduce to two simple conditions (ref: paper Eq. 44):

$$
\hat{\sigma} \leq \frac{1}{3}, \quad \hat{\tau} \geq \frac{(\Gamma-1)(2 - c_s^2) + c_s^2}{1 - c_s^2}
$$

- The $\hat{\sigma}$ constraint ensures **linear stability** about equilibrium.
- The $\hat{\tau}$ constraint ensures **causality** (subluminal characteristics).

---

## 2. Parameter Summary (Table II Reproduction)

[SOLID] The following table reproduces Table II from the paper with additional annotations on constraint satisfaction and characteristic speed behavior.

| Figure | $\Gamma$ | $m$ | $\hat{V}$ | $\hat{\sigma}$ | $\hat{\tau}$ | Stability ($\hat{\sigma} \leq 1/3$) | Causality status | Max $c_+$ |
|--------|----------|-----|-----------|----------------|-------------|--------------------------------------|------------------|-----------|
| Fig. 1 (Bjorken) | $4/3$ | $1$ | $1/10$ | $0$ | $0.5, 1, 2$ | Satisfied | $\hat{\tau}=0.5$: violated; $\hat{\tau}=1$: marginal; $\hat{\tau}=2$: satisfied | $\approx 1.3, 1.05, 0.7$ |
| Fig. 2 (Shockwave profile) | $4/3$ | $0.1$ | $2/15$ | $0$ | $1.5$ | Satisfied | Satisfied | Subluminal |
| Fig. 3 (Dynamic shock) | $4/3$ | $0.1$ | $4/3$ | $0$ | $1.5, 3$ | Satisfied | $\hat{\tau}=1.5$: $c_+ \approx 0.94 > v_L$ (stable); $\hat{\tau}=3$: $c_+ \approx 0.75 < v_L$ (unstable) | $\approx 0.94, 0.75$ |
| Fig. 4 (Acausality) | $4/3$ | $0.1$ | $4/3$ | $0$ | $0.25, 0.4, 0.5, 1.5$ | Satisfied | $\hat{\tau}=1.5$: satisfied; others: violated | $\approx 2.0, 1.6, 1.5, 0.9$ |
| Fig. 5 (Heat stationary) | $4/3$ | $0.1$ | $2/15$ | $0, 1/3$ | $1.5$ | Satisfied (boundary) | Satisfied | Subluminal |
| Fig. 6 (Telegrapher's) | $4/3$ | $0.1$ | $2/15$ | $0.15, 1.5, 7.5$ | $1.5, 15, 75$ | $\hat{\sigma}=0.15$: satisfied; $1.5, 7.5$: **violated** | Satisfied (all subluminal) | Subluminal |

---

## 3. Test Design Principles

### 3.1 Causality Validation Strategy

[SOLID] Causality in BDNK theory is ensured by requiring all characteristic speeds $c_+, c_-, c_1$ to be subluminal ($|c| < 1$). For the frame ansatz (ref: paper Eq. 41), this reduces to the single constraint on $\hat{\tau}$ in (ref: paper Eq. 44).

**How the test suite probes causality:**
- **Test 2 (Bjorken flow):** Varies $\hat{\tau} \in \{0.5, 1, 2\}$, systematically crossing the causality boundary. The case $\hat{\tau} = 0.5$ is always superluminal ($c_+ \approx 1.3$), $\hat{\tau} = 1$ is marginally superluminal at early times, and $\hat{\tau} = 2$ is always subluminal.
- **Test 5 (Acausality/instability):** Varies $\hat{\tau} \in \{0.25, 0.4, 0.5, 1.5\}$ to map the transition from subluminal to weakly superluminal to wildly superluminal.
- **Test 4 (Dynamic shockwave):** Tests whether $v > c_+$ triggers instability.

**Key finding:** [SOLID] Weakly superluminal characteristics do NOT produce acausal propagation or qualitative solution changes. Physical features (e.g., the "bump" in shockwave initial data) propagate at the sound speed, not at the characteristic speed. This is analogous to gauge dynamics in general relativity, where gauge modes can be superluminal without causing causality violation.

### 3.2 Linear Stability Validation Strategy

[SOLID] Linear stability about equilibrium requires $\hat{\sigma} \leq 1/3$ for the chosen frame (ref: paper Eq. 44). The full constraints are (ref: paper Eq. STAB A1--E).

**How the test suite probes stability:**
- **Test 7 (Telegrapher's equation):** Systematically violates $\hat{\sigma} \leq 1/3$ with $\hat{\sigma} = 1.5$ (mild violation) and $\hat{\sigma} = 7.5$ (severe violation).

**Key finding:** [SOLID] Mild violations ($\hat{\sigma} = 1.5$) appear benign---either the instability is slow relative to the dynamical timescale, or nonlinear effects provide stabilization. Severe violations ($\hat{\sigma} = 7.5$) trigger clear oscillatory instability. The bound $\hat{\sigma} \leq 1/3$ is sufficient but may not be necessary in all cases.

### 3.3 Constraint Violation Boundary Probing

The test suite is deliberately designed to explore behavior **both within and outside** the proven bounds:

| Boundary | Tests Probing It | Transition Mapped |
|----------|------------------|-------------------|
| Causality ($c_+ < 1$) | Tests 2, 4, 5 | Subluminal $\to$ weakly superluminal $\to$ wildly superluminal |
| Stability ($\hat{\sigma} \leq 1/3$) | Test 7 | Within bounds $\to$ mild violation $\to$ severe violation |
| Shockwave existence ($v < c_+$) | Tests 3, 4 | Smooth profile exists $\to$ ODE singularity encountered |

### 3.4 Convergence Testing Methodology

**ODE tests (Bjorken flow, steady-state shockwave):**
- Method: RK4 (fourth-order explicit Runge-Kutta)
- Convergence measure: $Q_N = \|R_{N/2}\| / \|R_N\|$ (ref: paper Eq. B1)
- Expected: $Q_N \to 16$ as $N \to \infty$ (fourth-order)
- Residual $R_N$: independent fourth-order centered finite difference discretization, evaluated on the numerical solution
- Results: Table III (reproduced below)

**PDE tests (dynamic shockwave, heat flow):**
- Method: Conservative finite volume (Pandya 2022), Heun's method (TVD RK2), WENO/CWENO spatial discretization
- CFL number: $\lambda = \Delta t / \Delta x = 0.1$ (default), $\lambda = 0.01$ for stiff/wildly superluminal cases
- Convergence measure: same $Q_N$, but using second-order Crank-Nicolson residual
- Expected: $Q_N \to 4$ as $N \to \infty$ (second-order)
- Results: Fig. 7

---

## 4. Test 1: Trivial Equilibrium States (Sec. III.A)

### Purpose

[SOLID] Compare the structure of Eckart, MIS, and BDNK theories by examining the simplest possible initial data---spatially isotropic states with no spatial gradients. The goal is to:

1. Show that BDNK and MIS share the same relaxation-type dissipation mechanism
2. Show that Eckart theory applies dissipation instantaneously (acausally)
3. Demonstrate "purely frame" dynamics---situations where $T^{ab}$ is static but hydrodynamic variables evolve
4. Illustrate that temperature outside equilibrium is frame-dependent

### Setup

**Spatial symmetry:** (0+0)D (no spatial variation, purely temporal ODE)

**Coordinate system:** Flat Minkowski, Cartesian

**Governing equations:** The conservation law $T^{tt}_{,t} = 0$ combined with the respective theory's constitutive relations.

**Initial data** (ref: paper Eq. 50):

$$
\begin{aligned}
&\epsilon, n \neq 0, \quad \epsilon_{,i} = n_{,i} = u^i = 0 \quad \text{(all three theories)} \\
&\dot{u}^i = 0 \quad \text{(Eckart)} \\
&\dot{\epsilon} \neq 0, \quad \dot{u}^i = 0 \quad \text{(BDNK)} \\
&\pi^{tt} \neq 0, \quad \pi^{ab}_{,i} = \pi^{ai} = 0 \quad \text{(MIS)}
\end{aligned}
$$

**Parameters:** Not listed in Table II (this is a purely analytic comparison, not a numerical integration depicted in a figure).

### Derivation of Simplified Equations of Motion

[SOLID] Starting from the conservation law $\nabla_a T^{ab} = 0$ with the spatially isotropic initial data (ref: paper Eq. 50), the only nontrivial component is the $t$-component:

$$
T^{tt}_{,t} = 0 \implies T^{tt} = \text{const}
$$

(ref: paper Eq. 52), because all off-diagonal components and spatial derivatives vanish by symmetry ($T^{ti} = T^{ij}_{,i} = 0$).

Baryon conservation gives $\dot{n} = 0$, so $n$ is constant in space and time.

Applying each theory's constitutive relations yields the simplified equations of motion (ref: paper Eq. 56):

$$
\begin{aligned}
\epsilon &= T^{tt} && \text{(Eckart)} \\
\dot{\epsilon} &= \frac{1}{\tau_\epsilon}(T^{tt} - \epsilon) && \text{(BDNK)} \\
\dot{\epsilon} &= \frac{1}{\tau_\pi + c_{1,\text{MIS}}}(T^{tt} - \epsilon) && \text{(MIS)}
\end{aligned}
$$

**Key structural observation:** [SOLID] The BDNK and MIS equations are algebraically equivalent under the identification $\tau_\epsilon = \tau_\pi + c_{1,\text{MIS}} \equiv \tau$.

### Exponential Relaxation Solution

[SOLID] For the special case where $\tau$ is independent of $t$, the BDNK/MIS ODE integrates directly to (ref: paper Eq. 59):

$$
\epsilon(t) = T^{tt} + (\epsilon_0 - T^{tt}) e^{-t/\tau}
$$

where $\epsilon_0 \equiv \epsilon(t=0)$ and $T^{tt}$ are freely specifiable initial data. The energy density relaxes exponentially toward the equilibrium value $T^{tt}$ with timescale $\tau$.

### Frame-Dependent Temperature

[SOLID] The BDNK stress-energy tensor admits the decomposition $u_a u_b T^{ab} = T^{tt} = \epsilon + \delta\epsilon$ (ref: paper Eq. 57). Using the EOS, the temperature can be expressed as (ref: paper Eq. 58):

$$
T = \frac{\Gamma - 1}{n}(T^{tt} - mn) - \tau_\epsilon \dot{T}
$$

This explicitly shows that different hydrodynamic frames (different values of $\tau_\epsilon$) yield different temperatures outside equilibrium (when $\dot{T} \neq 0$). Temperature is intrinsically frame-dependent, whereas the total energy content $T^{tt}$ is frame-independent.

### Key Results

1. **Eckart theory:** No dynamics---$\epsilon$ is pinned to $T^{tt}$ at all times. Dissipation is applied instantaneously.
2. **BDNK theory:** Relaxation-type dynamics with timescale $\tau_\epsilon$. The out-of-equilibrium correction $\delta\epsilon$ decays exponentially.
3. **MIS theory:** Identical relaxation dynamics under identification $\tau = \tau_\pi + c_{1,\text{MIS}}$.
4. **Origin of relaxation structure:** The BDNK relaxation form arises from terms proportional to projections of the relativistic Euler equations (ref: paper Eq. 60--61), which are $\mathcal{O}(\nabla^2)$ on-shell and thus do not alter the physical content at first order in gradients.
5. **Purely frame dynamics:** Even when $T^{ab}, J^a$ are static, the hydrodynamic variables $\epsilon, T$ can evolve nontrivially---these dynamics are "purely frame."

### Success Criteria

| Criterion | Status |
|-----------|--------|
| BDNK and MIS EOMs algebraically equivalent on this data | [SOLID] Verified analytically |
| Eckart theory has no dynamics | [SOLID] Verified analytically |
| Exponential relaxation to equilibrium | [SOLID] Exact analytic solution obtained |
| Temperature is frame-dependent outside equilibrium | [SOLID] Demonstrated via (ref: paper Eq. 58) |

### Associated Figures

No dedicated figure. This is a purely analytic derivation serving as foundation for all subsequent tests.

---

## 5. Test 2: Bjorken Flow (Sec. III.B, Fig. 1)

### Purpose

[SOLID] Investigate how relaxation times $\tau_\epsilon, \tau_P, \tau_Q$ affect solutions in a dynamical setting. Two primary questions:

1. Does the solution **qualitatively** change when characteristics are superluminal (dissipation applied "too quickly")?
2. What happens in the opposite limit, when dissipation is applied "too slowly" ($\hat{\tau} \to \infty$)?

### Setup

**Spatial symmetry:** (0+1)D (boost-invariant uniform expansion; no variation in $x, y, \xi$)

**Coordinate system:** Milne coordinates $x^a = (\tau, x, y, \xi)^T$ with metric $g_{ab} = \text{diag}(-1, 1, 1, \tau^2)$

**Flow profile:** $u^a = (1, 0, 0, 0)^T$ (Bjorken flow)

**Governing equation:** Single second-order ODE (ref: paper Eq. 66):

$$
\tau_\epsilon \ddot{\epsilon} = -\frac{1}{\tau}(\tau + 2\tau_\epsilon + \tau_P)\dot{\epsilon} - \frac{1}{\tau^2}[\rho(\tau + \tau_P) - V]
$$

where $\ddot{\epsilon} \equiv \partial_\tau^2 \epsilon$.

**Baryon conservation:** $n(\tau) = n_0/\tau$ (exact).

**Initial conditions:**
- $\epsilon_0 = 0.25$
- $\dot{\epsilon}_0 \in \{-2, 0, 2\}$ (three initial conditions per $\hat{\tau}$ value)
- $n_0 = 0.1$
- Integration domain: $\tau \in [1, 20]$

**Parameters** (from Table II):

| Parameter | Value |
|-----------|-------|
| $\Gamma$ | $4/3$ |
| $m$ | $1$ |
| $\hat{V}$ | $1/10$ |
| $\hat{\sigma}$ | $0$ |
| $\hat{\tau}$ | $0.5, 1, 2$ |

**Numerical method:** RK4 (fourth-order explicit Runge-Kutta)

### Analytical Expectations

**Inviscid solution** (ref: paper Eq. 67): obtained by setting $\tau_\epsilon, \tau_P, V \to 0$:

$$
\epsilon(\tau) = mn_0 \tau^{-1}[1 + e_0 \tau^{-(\Gamma-1)}] \quad \text{(inviscid)}
$$

where $e_0$ is an integration constant. The energy density separates into a rest-mass density term $\sim mn_0/\tau$ and an internal energy term that decays faster since $1 < \Gamma < 2$.

**Observable:** The quantity $\dot{\epsilon} + \Gamma\epsilon/\tau$ evaluates to $mn_0(\Gamma-1)/\tau^2$ on the inviscid solution, **independent of $e_0$**. This makes it an ideal diagnostic for measuring how quickly viscous solutions approach the inviscid one.

**$\hat{\tau} \to \infty$ limit** (ref: paper Eq. 68): the ODE reduces to $\ddot{\epsilon} = -2\dot{\epsilon}/\tau$, which has solution:

$$
\lim_{\tau_\epsilon \to \infty} \epsilon(\tau) = C_1 \tau^{-1} + C_2
$$

This solution does not agree with the inviscid solution in the ultrarelativistic limit ($m \to 0$ keeping $mn_0 e_0$ finite), confirming that infinite relaxation times prevent equilibration.

### Characteristic Speed Values

[SOLID] For each value of $\hat{\tau}$, the maximum characteristic speed $c_+$ is:

| $\hat{\tau}$ | $c_+$ (approximate) | Causality status |
|-------------|---------------------|------------------|
| $0.5$ | $\approx 1.3$ | **Always superluminal** |
| $1$ | $\approx 1.05$ (early), $\approx 0.9$ (late) | **Superluminal at early times only** |
| $2$ | $\approx 0.7$ | **Always subluminal** |

### Key Results

**Top panel of Fig. 1:** [SOLID] Plot of $\dot{\epsilon} + \Gamma\epsilon/\tau$ vs $\tau$. Three line styles (solid, dot-dash, dotted) for $\hat{\tau} = 0.5, 1, 2$ respectively, with three curves per $\hat{\tau}$ value (one per initial condition $\dot{\epsilon}_0 \in \{-2, 0, 2\}$). The red dashed line shows the inviscid solution $mn_0(\Gamma-1)/\tau^2$.

Key observations:
1. All three $\hat{\tau}$ values produce the same qualitative behavior---solutions approach the inviscid solution (red dashed line).
2. Larger $\hat{\tau}$ leads to slower equilibration, as expected from the relaxation picture.
3. **Superluminal characteristics do NOT qualitatively change the solution.** The $\hat{\tau} = 0.5$ case (always superluminal) behaves identically to the $\hat{\tau} = 2$ case (always subluminal), aside from equilibrating more rapidly.
4. Decreasing $\hat{\tau}$ makes the ODE "stiff" numerically, requiring very small steps to resolve the decay time $\tau_\epsilon$.

**Bottom panel of Fig. 1:** [SOLID] Temperature evolution for the $\hat{\tau} = 2$ solutions. Black solid lines show the BDNK-frame temperature $T$; blue dashed lines show the Eckart-frame temperature $T_E$ computed from the frame-independent observable $T^{\tau\tau}$.

Key observations:
1. One of the three solutions has **negative temperature** $T < 0$, corresponding to far-from-equilibrium initial data ($\dot{\epsilon}_0 = -2$).
2. The negative-temperature solution eventually reaches $T > 0$ at late times (beyond what is shown in the plot).
3. The BDNK-frame and Eckart-frame temperatures differ at early times, quantifying how far the system is from equilibrium.

### Discussion: $P < 0$ and Negative Temperatures

[SOLID] The causality and stability constraints of BDNK theory only require $\rho > \eta/\tau_Q$, which translates to (ref: paper Eq. 69):

$$
P > \frac{\Gamma - 1}{\Gamma}\left(\frac{\eta}{\tau_Q} - mn\right)
$$

This can become negative for small $\eta$, large $\tau_Q$, or large rest-mass energy density $mn$. An additional (optional) constraint $\tau_Q > \eta/(mn)$ (ref: paper Eq. 70) would ensure $P > 0$, but this is **not required** for causality and is not enforced in the paper.

The paper notes that negative temperatures arise because hydrodynamic variables are not unique outside equilibrium---they are only constrained to agree with thermodynamic observables upon equilibration. One can map between the BDNK evolution frame and the Eckart frame (where the EOS is naturally defined) to partially address this issue.

### Success Criteria

| Criterion | Status |
|-----------|--------|
| All $\hat{\tau}$ values approach inviscid solution | [SOLID] Confirmed in Fig. 1 |
| Larger $\hat{\tau}$ = slower equilibration | [SOLID] Confirmed |
| Superluminal characteristics cause no qualitative change | [SOLID] Confirmed |
| $T < 0$ allowed for far-from-equilibrium initial data | [SOLID] Observed; does not crash evolution |
| ODE convergence $Q_N \to 16$ | [SOLID] Confirmed in Table III |

### Associated Figures

**Fig. 1 (bjorken_plot.pdf):**
- **Top panel:** $\tau$ vs $\dot{\epsilon} + \Gamma\epsilon/\tau$. Three line styles for $\hat{\tau} = \{0.5, 1, 2\}$, three curves per $\hat{\tau}$ (one per $\dot{\epsilon}_0$). Red dashed = inviscid solution.
- **Bottom panel:** $\tau$ vs temperature for $\hat{\tau} = 2$. Black solid = BDNK frame $T$. Blue dashed = Eckart frame $T_E$. Bottom-most pair of lines: $T < 0$.

### Figure Analysis: Bjorken Flow (Fig. 1, `bjorken_plot.pdf`)

**Top Panel (log-log plot):** Nine black curves (three families of three, each family sharing a line style corresponding to a single $\hat{\tau}$ value) plus one thick red dashed reference line. The nine curves emerge from widely different initial values at $\tau = 1$ and converge onto the red dashed reference line (inviscid solution $mn_0(\Gamma-1)/\tau^2$) at late times. Within each family, the three members correspond to the three initial conditions $\dot{\epsilon}_0 \in \{-2, 0, 2\}$. Several curves plunge steeply downward before recovering, corresponding to the plotted quantity passing through zero. Line styles: solid ($\hat{\tau} = 0.5$, always superluminal $c_+ \approx 1.3$), dash-dot ($\hat{\tau} = 1$, superluminal at early times), dotted ($\hat{\tau} = 2$, always subluminal $c_+ \approx 0.7$). Axes: horizontal is $\tau$ (log scale, 1 to 20), vertical is $\dot{\epsilon} + \Gamma\epsilon/\tau$ (log scale, $\sim 10^{-4}$ to $> 10^{-1}$).

**Bottom Panel (linear-log plot):** Three black solid curves (BDNK-frame temperature $T$) and three blue dashed curves (Eckart-frame temperature $T_E$) for the three $\hat{\tau} = 2$ solutions. All BDNK curves start at $T \approx 0.5$ (from shared $\epsilon_0 = 0.25$) but diverge due to different $\dot{\epsilon}_0$ values. The Eckart curves start at very different values because $T_E$ depends on $\dot{\epsilon}$ through the frame correction $\delta\epsilon = -\tau_\epsilon \dot{\epsilon}$. For $\dot{\epsilon}_0 = -2$: BDNK temperature plunges negative shortly after $\tau = 1$, while its Eckart partner starts at $T_E \approx 1.8$ before also decaying to negative values. For $\dot{\epsilon}_0 = 0$: both frames start near $T \approx 0.5$ and decay together. At late times, BDNK and Eckart temperatures converge for each solution, confirming equilibration. Axes: horizontal is $\tau$ (log scale), vertical is $T$ (linear, $\approx -0.6$ to $2.2$).

**Key visual features:** (1) Universal convergence of all viscous solutions to the inviscid attractor regardless of $\hat{\tau}$ or initial conditions. (2) Larger $\hat{\tau}$ produces slower convergence. (3) No qualitative change when characteristics become superluminal. (4) Frame dependence of temperature is visually striking at early times but vanishes at late times.

---

## 6. Test 3: Steady-State Shockwave Profiles (Sec. III.C, Fig. 2)

### Purpose

[SOLID] Generalize the conformal shockwave analysis of Pandya (2021) to arbitrary BDNK fluids with ideal gas microphysics. Demonstrate that smooth, steady-state shockwave profiles exist when the flow velocity never reaches a characteristic speed, and compare the ideal gas and conformal shockwave structures.

### Setup

**Spatial symmetry:** (1+1)D (time-independent, one spatial dimension)

**Coordinate system:** Cartesian, boosted into the rest frame of the shock

**Governing equations:** System of coupled ODEs (ref: paper Eqs. 72--77):

$$
n' = -\frac{W^2 n v'}{v}
$$

$$
\epsilon'(x) = \frac{c_4 v^4 + c_3 v^3 + c_2 v^2 + c_1 v + c_0}{A W v (v - c_+)(v + c_+)(v - c_-)(v + c_-)}
$$

$$
v'(x) = \frac{d_3 v^3 + d_2 v^2 + d_1 v + d_0}{A W^3 (v - c_+)(v + c_+)(v - c_-)(v + c_-)}
$$

where the coefficients $c_i, d_i$ are given in (ref: paper Eq. 78) and the constants $T^{tx}, T^{xx}$ are computed from the perfect fluid stress-energy tensor at the asymptotic left state.

**Left state (asymptotic, $x \to -\infty$):**

$$
\{\epsilon_L, v_L, n_L\} = \{1, 0.8, 0.1\}
$$

**Right state:** Determined by Rankine-Hugoniot conditions (ref: paper Eq. 80).

**Parameters** (from Table II):

| Parameter | Value |
|-----------|-------|
| $\Gamma$ | $4/3$ |
| $m$ | $0.1$ |
| $\hat{V}$ | $2/15$ |
| $\hat{\sigma}$ | $0$ |
| $\hat{\tau}$ | $1.5$ |

**Numerical method:** RK4

### ODE Singularity Structure

[SOLID] The denominators of the ODEs (ref: paper Eqs. 76--77) vanish when $v = \pm c_\pm$ or $v = 0$. These are singularities of the ODE system. A smooth shockwave profile can only exist if the velocity profile **never attains** these singular values. If $v_L \geq c_+$, the numerator and denominator do not simultaneously vanish and the solver finds the trivial constant state $\epsilon, v, n = \epsilon_L, v_L, n_L$ for all $x$.

### Key Results

[SOLID] Fig. 2 shows a three-panel comparison of shockwave profiles:
- **Black curves:** Ideal gas BDNK fluid with the parameters listed above
- **Green curves:** Conformal BDNK fluid with the same shear viscosity and the sharply causal frame (equation 16, frame B of Pandya 2021)

Both shockwaves use the same asymptotic left state $\{\epsilon_L, v_L, n_L\} = \{1, 0.8, 0.1\}$.

**Panels:**
1. **$\epsilon(x)$:** Smooth transition from $\epsilon_L = 1$ (left) to a higher right-state value. Ideal gas and conformal profiles are qualitatively similar but quantitatively different.
2. **$v(x)$:** Smooth transition from $v_L = 0.8$ (left) to a lower right-state velocity. The velocity profile never reaches $c_+$ or $c_-$.
3. **$n(x)$:** Smooth transition in baryon density. The conformal case (green) has $n = 0$ since conformal fluids have zero baryon chemical potential; the ideal gas case (black) shows nontrivial baryon density structure.

The inviscid solution in each case would have the same asymptotic left and right states, but with the smooth transition replaced by a step function discontinuity at $x \approx 0$.

### Success Criteria

| Criterion | Status |
|-----------|--------|
| Smooth shockwave profile obtained | [SOLID] Confirmed |
| Velocity never reaches $c_+$ or $c_-$ | [SOLID] Confirmed |
| Ideal gas and conformal profiles qualitatively similar | [SOLID] Confirmed |
| ODE convergence $Q_N \to 16$ | [SOLID] Confirmed in Table III |

### Associated Figures

**Fig. 2 (shockwave_plot.pdf):** Three-panel plot showing $\epsilon(x)$, $v(x)$, $n(x)$ profiles. Black = ideal gas BDNK fluid. Green = conformal BDNK fluid.

### Figure Analysis: Steady-State Shockwave Profiles (Fig. 2, `shockwave_plot.pdf`)

**Visual description:** The figure shows steady-state shockwave profiles for two BDNK fluids plotted on common axes. Three physical quantities -- energy density $\epsilon$ (solid lines), three-velocity $v$ (dash-dot lines), and baryon number density $n$ (dotted lines) -- are plotted as functions of the spatial coordinate $x \in [-2, 2]$, each transitioning smoothly from left asymptotic values to right asymptotic values. Black curves show the non-conformal ideal gas BDNK fluid; green curves show the conformal BDNK fluid (sharply causal frame B of Pandya 2021). Both share the same asymptotic left state $\{\epsilon, v, n\}_L = \{1, 0.8, 0.1\}$.

**Key visual differences:** (1) The ideal gas (black) $\epsilon$ profile transitions more sharply than the conformal (green) profile, which has a broader sigmoid shape. (2) The velocity profiles are qualitatively similar but the conformal profile transitions slightly more gradually. (3) The right-state values differ between the two fluids due to different Rankine-Hugoniot jump conditions arising from the distinct equations of state. (4) No singular behavior is observed -- the velocity $v$ never reaches $c_+$ or $c_-$.

**Significance:** The smooth profiles confirm that steady-state shockwave solutions exist when $v < c_+$ everywhere. The comparison between ideal gas and conformal fluids demonstrates that the BDNK framework generalizes successfully beyond the conformal setting, and that the non-conformal microphysics produces quantitatively (but not qualitatively) different shockwave structures.

---

## 7. Test 4: Dynamic Shockwave Stability (Sec. III.C, Fig. 3)

### Purpose

[SOLID] Test what happens when a shockwave forms **dynamically** (from PDE initial data, rather than solving the steady-state ODE). Specifically, investigate whether instability occurs when the flow velocity $v$ exceeds the maximum characteristic speed $c_+$---the precise condition under which the steady-state ODE has no smooth solution.

### Setup

**Spatial symmetry:** (1+1)D PDE (one spatial dimension plus time)

**Coordinate system:** Cartesian

**Governing equations:** Full BDNK PDEs (ref: paper Eqs. 1--2)

**Initial data:** Error-function interpolation (ref: paper Eq. 79) with width $w = 10$:

$$
\begin{aligned}
\epsilon(0,x) &= \frac{\epsilon_R - \epsilon_L}{2}\left[\text{erf}\left(\frac{x}{w}\right) + 1\right] + \epsilon_L \\
v(0,x) &= \frac{v_L - v_R}{2}\left[1 - \text{erf}\left(\frac{x}{w}\right)\right] + v_R \\
n(0,x) &= \frac{n_L - n_R}{2}\left[1 - \text{erf}\left(\frac{x}{w}\right)\right] + n_R
\end{aligned}
$$

**Left-right state pair** (ref: paper Eq. 81):

$$
\{1, 0.9, 1\}_L \implies \{11.5174, 0.354727, 5.44212\}_R
$$

The right state is determined by the Rankine-Hugoniot conditions (ref: paper Eq. 80).

**Parameters** (from Table II):

| Parameter | Value |
|-----------|-------|
| $\Gamma$ | $4/3$ |
| $m$ | $0.1$ |
| $\hat{V}$ | $4/3$ |
| $\hat{\sigma}$ | $0$ |
| $\hat{\tau}$ | $3$ (unstable), $1.5$ (stable) |

**Numerical method:** Conservative finite volume (Pandya 2022), Heun's method, WENO/CWENO, CFL $\lambda = 0.1$

### Key Results

**Top panel of Fig. 3 ($\hat{\tau} = 3$, unstable):** [SOLID]

- The velocity profile $v(x)$ is shown at time $t = 27$ at multiple numerical resolutions (darker = finer grid).
- The dotted line shows $c_+(x) \approx 0.75$.
- With $\hat{\tau} = 3$, the maximum characteristic speed $c_+ \approx 0.75$ is below the upstream velocity $v_L = 0.9$, so the velocity profile must cross $c_+$ somewhere in the shock transition.
- **Instability onset:** A high-frequency numerical instability sets in precisely in the region where $v > c_+$. This is the same condition under which the steady-state ODE (ref: paper Eqs. 72--77) has no smooth solution.
- The instability is localized to the region where $v$ exceeds $c_+$ and grows more sharply with increasing resolution, confirming it is a genuine feature of the continuum equations in the sense that no smooth steady-state solution exists.

**Bottom panel of Fig. 3 ($\hat{\tau} = 1.5$, stable):** [SOLID]

- With $\hat{\tau} = 1.5$, the characteristic speed $c_+ \approx 0.94$ exceeds the upstream velocity $v_L = 0.9$, so $c_+ > v$ everywhere in the shockwave profile.
- The evolution is stable to very late times ($t = 372$; note the much later timestamp in the figure compared to the top panel).
- At late times, the solution asymptotes to the steady-state ODE solution.

### Connection to Rigorous Results

[SOLID] The observed instability for $v > c_+$ is consistent with a mathematically rigorous result by Freistuhler (2021) for conformal BDNK fluids, which proved that a given hydrodynamic frame will always possess shockwave solutions that break down unless the maximum local characteristic speed is greater than or equal to the speed of light.

One may also ask whether $v$ crossing $c_-$ causes issues. The paper notes that this requires severely violating both causality and stability constraints, making it difficult to isolate the instability mechanism.

### Success Criteria

| Criterion | Status |
|-----------|--------|
| Instability onset localized to $v > c_+$ region | [SOLID] Confirmed |
| Stable frame ($\hat{\tau} = 1.5$) evolves to late times | [SOLID] Confirmed |
| Stable frame approaches steady-state ODE solution | [SOLID] Confirmed |
| Consistent with Freistuhler (2021) rigorous result | [SOLID] Consistent |

### Associated Figures

**Fig. 3 (shock_instability.pdf):**
- **Top panel:** Unstable case ($\hat{\tau} = 3$, $c_+ \approx 0.75$). Snapshot at $t = 27$. Multiple resolutions (darker = finer). Dotted line = $c_+(x)$. Instability where $v > c_+$.
- **Bottom panel:** Stable case ($\hat{\tau} = 1.5$, $c_+ \approx 0.94$). Late-time snapshot at $t = 372$. $c_+ > v$ everywhere, stable evolution.

### Figure Analysis: Dynamic Shockwave Stability (Fig. 3, `shock_instability.pdf`)

**Top panel ($\hat{\tau} = 3$, unstable):** Velocity profile $v(t, x)$ at $t = 27$ over the spatial domain $x \in [-50, 50]$. The upstream velocity $v_L = 0.9$ sits above the horizontal dotted line marking $c_+ \approx 0.75$. A violent, high-frequency oscillatory instability is visible at the shock transition region near $x = 0$. An inset magnifies this region at three resolutions ($N = 2^9, 2^{10}, 2^{11}$, shown in progressively darker shading): the oscillations persist and sharpen with increasing resolution, confirming a genuine instability rather than a transient numerical artifact. A smooth "bump" feature propagates downstream at roughly the sound speed, sourced by the deviation of the initial data from the exact stationary shockwave profile.

**Bottom panel ($\hat{\tau} = 1.5$, stable):** Velocity profile at $t = 372$ (more than an order of magnitude later). The profile smoothly transitions from $v_L = 0.9$ to $v_R \approx 0.35$ through a well-resolved, monotonic shock front, with no oscillation or instability. The dotted line marks $c_+ \approx 0.94 > v_L = 0.9$. Three resolution levels ($N = 2^9, 2^{10}, 2^{11}$) are indistinguishable, indicating clean convergence to the steady-state shockwave solution.

**Central message:** The sharp dichotomy between the two panels demonstrates that the instability criterion is precisely $v > c_+$. When the flow velocity exceeds the maximum characteristic speed (top panel), the steady-state shockwave ODEs become singular and the dynamical evolution develops a non-convergent instability. When $c_+ > v$ everywhere (bottom panel), the evolution is stable and converges to the steady-state profile. The choice of hydrodynamic frame (via $\hat{\tau}$) directly controls $c_+$ and therefore determines stability.

---

## 8. Test 5: Acausality/Instability Tests (Sec. III.C, Fig. 4)

### Purpose

[SOLID] Systematically test the behavior of shockwave solutions across a range of superluminal frames, from weakly to wildly superluminal, to understand the practical consequences of violating the causality constraint.

### Setup

**Spatial symmetry:** (1+1)D PDE

**Coordinate system:** Cartesian

**Governing equations:** Full BDNK PDEs

**Initial data:** Same error-function interpolation (ref: paper Eq. 79) with $w = 10$.

**Left-right state pair** (ref: paper Eq. 81):

$$
\{1, 0.6, 1\}_L \implies \{1.33795, 0.514414, 1.25027\}_R
$$

**Parameters** (from Table II):

| Parameter | Value |
|-----------|-------|
| $\Gamma$ | $4/3$ |
| $m$ | $0.1$ |
| $\hat{V}$ | $4/3$ |
| $\hat{\sigma}$ | $0$ |
| $\hat{\tau}$ | $0.25, 0.4, 0.5, 1.5$ |

**Numerical method:** Conservative finite volume, Heun's method, WENO/CWENO
- CFL $\lambda = 0.1$ for $\hat{\tau} = 0.5, 1.5$
- CFL $\lambda = 0.01$ for $\hat{\tau} = 0.4$ (stiff superluminal)
- CFL $\lambda = 0.01$ for $\hat{\tau} = 0.25$ (wildly superluminal)

### Characteristic Speed Values

| $\hat{\tau}$ | $c_+$ (approx.) | Category |
|-------------|-----------------|----------|
| $1.5$ | $\sim 0.9$ | **Subluminal** (reference case) |
| $0.5$ | $\sim 1.5$ | **Weakly superluminal** |
| $0.4$ | $\sim 1.6$ | **Stiff superluminal** |
| $0.25$ | $\sim 2.0$ | **Wildly superluminal** |

### Key Results

**Top panel of Fig. 4 (weakly and stiffly superluminal):** [SOLID]

Solutions for $\hat{\tau} = 0.4, 0.5, 1.5$ are shown at $t = 0$ (dotted line) and at a very late time $t = 1582$ (solid line) when dynamics have damped out and the shockwave closely approximates the steady-state solution.

Key observations:
1. **At $t = 1582$, all three frames produce solutions identical up to the resolution of the plot.** The superluminal characteristics have no noticeable impact on the late-time solution.
2. The solutions are not exactly identical---they converge to slightly different continuum limits---but the differences are invisible at the plot resolution.
3. **No superluminal propagation is observed.** The "bump" sourced by the non-stationary part of the initial data propagates downstream at essentially the sound speed, not at the characteristic speed.
4. The $\hat{\tau} = 0.4$ case requires CFL number $\lambda = 0.01$ (an order of magnitude smaller than the others) due to numerical stiffness, but still recovers the same late-time solution.

**Bottom panel of Fig. 4 (wildly superluminal, $\hat{\tau} = 0.25$):** [SOLID]

A very fast instability sets in at early times:

1. The initial transient "bump" near $x \sim 20$ grows unboundedly **without propagating**, rather than reaching a fixed size and moving away.
2. The growth is shown at three successive times via dotted, dot-dash, and solid lines.
3. Shortly after, the quantities $\dot{\epsilon}, \dot{v}$ appear to **diverge in finite time** at a point to the right of the bump ($x \sim 40$).
4. This divergence forms a **very sharp feature** in essentially all state variables, though none of them---including $c_s, c_\pm, T^{ta}, \epsilon, P, n$---appear to obtain unphysical values.
5. **Inset:** The sharp feature in the $v$ profile is shown at multiple numerical resolutions $N \in \{2^7, 2^8, 2^9, 2^{10}, 2^{11}\}$ (increasingly dark shades of gray). The behavior appears to indicate **convergence**, meaning the rapid growth is present in the continuum PDE solution and is not numerical in origin.
6. Shortly beyond the time shown, the sharp feature sources an oscillatory numerical instability that crashes the simulation.

### Physical Interpretation

[SOLID] The paper offers the following interpretation:
- **Weakly superluminal:** No issues. Characteristics being superluminal does not imply acausal propagation. Physical features propagate at the sound speed. Analogy to gauge dynamics in GR---gauge modes need not be confined to the speed of light.
- **Stiff superluminal:** Same solution recovered, but numerical stiffness requires very small CFL numbers.
- **Wildly superluminal:** The instability is likely related to the failure of the linear stability proof, which requires subluminal characteristics. The instability converges with resolution (physical, not numerical).

The paper concludes: requiring $|c_+| = 1$ (or $|c_+| = 1 - \delta$ for infinitesimal $\delta > 0$) would guarantee causality **and** ensure fast shockwave solutions do not exhibit instability.

### Success Criteria

| Criterion | Status |
|-----------|--------|
| Weakly superluminal: identical late-time solutions | [SOLID] Confirmed at $t = 1582$ |
| No superluminal propagation observed | [SOLID] Confirmed |
| Stiff superluminal: same solution, smaller CFL required | [SOLID] Confirmed ($\lambda = 0.01$) |
| Wildly superluminal: instability converges with resolution | [SOLID] Confirmed (inset) |
| Instability is physical, not numerical | [SOLID] Supported by convergence behavior |

### Associated Figures

**Fig. 4 (acaus_instab.pdf):**
- **Top panel:** Late-time ($t = 1582$) comparison of $\hat{\tau} = 0.4, 0.5, 1.5$. All solutions agree up to plot resolution. No superluminal propagation.
- **Bottom panel:** Wildly superluminal $\hat{\tau} = 0.25$. Three time snapshots showing growth of bump ($x \sim 20$) and sharp feature ($x \sim 40$). **Inset:** sharp feature at $N \in \{2^7, \ldots, 2^{11}\}$ showing convergence.

### Figure Analysis: Acausality/Instability Tests (Fig. 4, `acaus_instab.pdf`)

**Top panel (weakly superluminal and subluminal frames):** Velocity profile $v(x)$ over the spatial domain $x \in [-100, 100]$ for three frames ($\hat{\tau} = 0.4, 0.5, 1.5$) at two times: dotted line at $t = 0$ (initial data, smooth error-function transition from $v \approx 0.6$ to $v \approx 0.515$) and solid line at $t = 1582$ (late time, relaxed to a steeper transition approximating the steady-state ODE solution). All three frames produce solutions that are identical up to the resolution of the plot at both times, despite spanning from subluminal ($\hat{\tau} = 1.5$, $c_+ \approx 0.9$) to weakly superluminal ($\hat{\tau} = 0.5$, $c_+ \approx 1.5$; $\hat{\tau} = 0.4$, $c_+ \approx 1.6$). No superluminal signal propagation is observed; the transient "bump" propagates downstream at the sound speed.

**Bottom panel (wildly superluminal, $\hat{\tau} = 0.25$, $c_+ \approx 2$):** Three closely spaced early-time snapshots ($t = 0.27$, $0.31$, $0.36$) show a rapidly growing instability. Two pathological features develop: (1) an unboundedly growing bump near $x \sim 10\text{--}20$ that does not propagate, and (2) a very sharp, narrow dip near $x \sim 40\text{--}50$ where the time derivatives $\dot{\epsilon}$ and $\dot{v}$ appear to diverge in finite time. The inset shows this sharp feature at five resolutions ($N = 2^7$ through $2^{11}$, light gray to black): the curves converge to a well-defined, very narrow spike, providing strong evidence that the rapid growth is a property of the continuum PDE solution, not a numerical artifact. Shortly beyond $t = 0.36$, the sharp feature sources an oscillatory numerical instability that crashes the simulation.

**Key conclusions:** (1) Weakly superluminal characteristics cause no qualitative change in the physical solution. (2) Physical features propagate at the sound speed, not at the characteristic speed. (3) Wildly superluminal frames trigger a genuine instability that converges with resolution. (4) The $\hat{\tau} = 0.4$ case requires an order-of-magnitude smaller CFL number ($\lambda = 0.01$) due to stiffness, but recovers the same late-time solution.

---

## 9. Test 6: Heat Flow Stationary Test (Sec. III.D, Fig. 5)

### Purpose

[SOLID] Confirm that nonzero thermal conductivity ($\sigma \neq 0$) is required for dynamical heat flow solutions. This test is unique to the ideal gas model---conformal fluids cannot have "pure" heat flow because temperature gradients necessarily imply pressure gradients ($P \propto T^4$).

### Setup

**Spatial symmetry:** (1+1)D PDE (one spatial dimension plus time)

**Coordinate system:** Cartesian

**Governing equations:** Full BDNK PDEs, restricted to zero-velocity ($u^i = 0$) initial data. The baryon conservation gives $\dot{n} = 0$ and the stress-energy conservation at $t = 0$ reduces to (ref: paper Eq. 96):

$$
T^{at}_{,a}\Big|_{t=0} = 0 = \tau_\epsilon \ddot{\epsilon} - (\kappa T')'
$$

This shows that the system has dynamics **only if** $\kappa \neq 0$, which requires $\sigma \neq 0$ by $\kappa \equiv \sigma\rho^2/(n^2 T)$ (ref: paper Eq. 46).

**Initial data** (ref: paper Eq. 95):

$$
T(0,x) = A \exp\left(-\frac{x^2}{w^2}\right) + \delta, \quad P(0,x) = P_0 = \text{const}
$$

The initial temperature profile is a Gaussian perturbation superimposed on a constant background, with spatially uniform pressure. Time-symmetric initial data: $\dot{\epsilon}(0,x) = \dot{u}^i(0,x) = 0$.

The hydrodynamic variables $\epsilon, n$ are computed from $T, P$ via the EOS relations $\epsilon = P[mT^{-1} + (\Gamma-1)^{-1}]$, $n = PT^{-1}$.

**Parameters** (from Table II):

| Parameter | Value |
|-----------|-------|
| $\Gamma$ | $4/3$ |
| $m$ | $0.1$ |
| $\hat{V}$ | $2/15$ |
| $\hat{\sigma}$ | $0$ (top panel), $1/3$ (bottom panel) |
| $\hat{\tau}$ | $1.5$ |

**Numerical method:** Conservative finite volume, Heun's method, WENO/CWENO, CFL $\lambda = 0.1$

### Key Results

**Top panel of Fig. 5 ($\hat{\sigma} = 0$):** [SOLID]

Snapshots of $\dot{\epsilon}(x)$ at a time shortly after $t = 0$, shown at multiple numerical resolutions (darker = higher resolution).

- $\dot{\epsilon}$ **converges to zero** as the grid is refined.
- There are no dynamics: $\sigma = 0 \implies \kappa = 0 \implies \ddot{\epsilon} = 0$ in (ref: paper Eq. 96).
- The nonzero values of $\dot{\epsilon}$ visible in the figure are purely numerical error, which diminishes with resolution.

**Bottom panel of Fig. 5 ($\hat{\sigma} = 1/3$):** [SOLID]

Same setup, but with nonzero thermal conductivity.

- $\dot{\epsilon}$ **converges to a nonzero value** as the grid is refined.
- The system has genuine heat flow dynamics: energy redistributes due to the thermal gradient.
- The converged profile of $\dot{\epsilon}(x)$ represents the continuum solution.

### Physical Interpretation

[SOLID] This test confirms the analytical result from (ref: paper Eq. 96): $\ddot{\epsilon} = 0$ when $\kappa = 0$. The ideal gas EOS allows the temperature to vary while keeping pressure constant (by adjusting $n$ appropriately through $P = nT$), which is impossible for a conformal fluid where $P \propto T^4$. This is why "pure" heat flow is a novel feature of the ideal gas model.

### Success Criteria

| Criterion | Status |
|-----------|--------|
| $\hat{\sigma} = 0$: $\dot{\epsilon} \to 0$ with resolution | [SOLID] Confirmed |
| $\hat{\sigma} = 1/3$: $\dot{\epsilon} \to$ nonzero with resolution | [SOLID] Confirmed |
| Confirms $\ddot{\epsilon} = 0$ when $\kappa = 0$ (ref: paper Eq. 96) | [SOLID] Confirmed |

### Associated Figures

**Fig. 5 (heat_stationary.pdf):**
- **Top panel:** $\hat{\sigma} = 0$, multiple resolutions (darker = higher $N$). $\dot{\epsilon}$ converges to zero.
- **Bottom panel:** $\hat{\sigma} = 1/3$, multiple resolutions. $\dot{\epsilon}$ converges to a nonzero continuum solution.

### Figure Analysis: Heat Flow Stationary Test (Fig. 5, `heat_stationary.pdf`)

**Top panel ($\hat{\sigma} = 0$):** Three curves at resolutions $N = 2^7, 2^8, 2^9$ (light gray to black) show $|\dot{\epsilon}|$ at a time shortly after $t = 0$. The vertical scale is $O(10^{-6})$. Noisy, oscillatory features near $x = 0$ (center of the Gaussian temperature bump) decrease systematically with resolution. The inset magnifies the central region, clearly revealing amplitude reduction from coarsest (lightest) to finest (darkest) resolution. The nonzero signal is purely numerical truncation error converging to zero.

**Bottom panel ($\hat{\sigma} = 1/3$):** Same resolution convention. The vertical scale is $O(10^{-4})$, two orders of magnitude larger than the top panel. The $|\dot{\epsilon}|$ profile has a rich spatial structure with multiple peaks symmetric about $x \approx \pm 45$, reflecting the second spatial derivative of the Gaussian temperature profile filtered through the spatially varying thermal conductivity $\kappa(x)$. The inset near $x \approx 50$ shows tight overlap of the three resolution curves, demonstrating clean convergence to a physical (non-artifact) solution.

**Significance:** The juxtaposition provides a clean numerical demonstration that (1) thermal conductivity ($\sigma \neq 0$) is a necessary condition for dynamical heat flow, (2) the code correctly produces a stationary solution when $\sigma = 0$, and (3) the numerical scheme converges in both cases. This test is unique to the ideal gas model -- conformal fluids cannot have pure heat flow because temperature gradients necessarily imply pressure gradients.

---

## 10. Test 7: Telegrapher's Equation Behavior (Sec. III.D, Fig. 6)

### Purpose

[SOLID] Demonstrate the transition from heat-equation-like (parabolic) to wave-like (hyperbolic) behavior as $\hat{\sigma}$ increases, consistent with the constant-coefficient analysis showing that the BDNK heat flow equation has the structure of a telegrapher's equation (ref: paper Eqs. 89--91). Additionally, test the consequences of violating the linear stability constraint $\hat{\sigma} \leq 1/3$.

### Background: Constant-Coefficient Analysis

[SOLID] For constant transport coefficients, the BDNK heat flow equation takes three forms depending on the frame choice (ref: paper Eqs. 89--91):

$$
\begin{aligned}
0 &= \dot{T} - \alpha_E T'' && \text{(Eckart: heat equation)} \\
0 &= \ddot{T} - c_h^2 T'' + \frac{1}{\tau_\epsilon}\dot{T} && \text{(hybrid: telegrapher's equation)} \\
0 &= \ddot{T} - c_B^2 T'' + \frac{1}{\tau_\epsilon}\dot{T} + l.o.t. && \text{(BDNK: generalized telegrapher's equation)}
\end{aligned}
$$

where $\alpha_E \equiv \kappa(\Gamma-1)/n$ is the Eckart thermal diffusivity, $c_h^2 \equiv \kappa(\Gamma-1)/(n\tau_\epsilon)$ is the hybrid thermal propagation speed, and $c_B^2 \equiv c_h^2(1 - \gamma n/\kappa)$ is the BDNK thermal propagation speed. The lower-order terms are $l.o.t. \equiv \frac{(\Gamma-1)}{n\tau_\epsilon}\gamma(n'' T + 2n'T')$.

In the limit $\sigma, \tau_\epsilon \to \infty$ with $c_B^2 \propto \sigma/\tau_\epsilon$ kept finite, (ref: paper Eq. 91) reduces to the simple 1D wave equation.

### Setup

**Spatial symmetry:** (1+1)D PDE

**Coordinate system:** Cartesian

**Governing equations:** Full BDNK PDEs

**Initial data:** Same as Test 6---Gaussian temperature perturbation at constant pressure (ref: paper Eq. 95).

**Parameters** (from Table II):

| Parameter | Value |
|-----------|-------|
| $\Gamma$ | $4/3$ |
| $m$ | $0.1$ |
| $\hat{V}$ | $2/15$ |
| $\hat{\sigma}$ | $0.15, 1.5, 7.5$ |
| $\hat{\tau}$ | $1.5, 15, 75$ |

**Critical design choice:** The ratio $\hat{\sigma}/\hat{\tau} = 0.1$ is held constant across all three cases. This ensures $c_B^2 \propto \hat{\sigma}/\hat{\tau}$ remains finite, allowing the systematic exploration of the transition from diffusive to wavelike behavior.

**Linear stability status:**

| $\hat{\sigma}$ | $\hat{\tau}$ | $\hat{\sigma} \leq 1/3$? | Status |
|----------------|-------------|--------------------------|--------|
| $0.15$ | $1.5$ | **Yes** | Within bounds |
| $1.5$ | $15$ | **No** ($\hat{\sigma} = 1.5 > 1/3$) | **Mild violation** |
| $7.5$ | $75$ | **No** ($\hat{\sigma} = 7.5 \gg 1/3$) | **Severe violation** |

All three cases have **subluminal** characteristic speeds.

**Numerical method:** Conservative finite volume, Heun's method, WENO/CWENO, CFL $\lambda = 0.1$

### Key Results

**Left panel (early time):** [SOLID]

All three solutions are shown at an early time. The central hot spot at $x = 0$ decays and spreads, similar to heat equation behavior. At this stage, the three cases ($\hat{\sigma} = 0.15$ in light gray, $1.5$ in medium gray, $7.5$ in black) are qualitatively similar.

**Middle panel (intermediate time):** [SOLID]

The solutions begin to diverge:
- $\hat{\sigma} = 0.15$ (light gray): Continues to exhibit heat-equation-like diffusive decay of the central peak.
- $\hat{\sigma} = 1.5$ (medium gray): Intermediate behavior; no apparent instability despite violating $\hat{\sigma} \leq 1/3$.
- $\hat{\sigma} = 7.5$ (black): The central peak **splits into two propagating waves**, characteristic of telegrapher's equation/wave equation behavior in the large-$\hat{\sigma}$ limit.

**Inset (zoomed in):** Shows that **all** three solutions possess some wavelike behavior in the form of a small transient that propagates away at the sound speed. The wavelike character becomes dominant only for large $\hat{\sigma}$.

**Right panel (late time):** [SOLID]

- $\hat{\sigma} = 0.15$ (light gray): Continues to evolve stably. The diffusive decay proceeds smoothly.
- $\hat{\sigma} = 1.5$ (medium gray): Still no apparent instability despite violating the stability bound.
- $\hat{\sigma} = 7.5$ (black): **Oscillatory instability** sets in, eventually crashing the numerical simulation.

### Physical Interpretation

[SOLID] The test confirms three key points:

1. **Smooth transition from parabolic to hyperbolic:** As $\hat{\sigma}$ (and correspondingly $\hat{\tau}$) increase while keeping $\hat{\sigma}/\hat{\tau}$ constant, the BDNK equations transition from heat-equation-like behavior to wave-like behavior, consistent with the constant-coefficient telegrapher's equation analysis.

2. **Mild stability violations can be benign:** The $\hat{\sigma} = 1.5$ case violates $\hat{\sigma} \leq 1/3$ by a factor of $\sim 4.5$ but shows no apparent instability. This may be because:
   - The instability growth rate is slow relative to the dynamical timescale, or
   - Nonlinear effects stabilize the system, or
   - The linear stability bound is sufficient but not necessary.

3. **Severe stability violations trigger oscillatory instability:** The $\hat{\sigma} = 7.5$ case (violation by a factor of $\sim 22.5$) exhibits clear oscillatory instability at late times. This is consistent with the constant-coefficient analysis showing that the stability constraint $\hat{\sigma} \leq 1/3$ ensures positive relaxation time $\tau_\theta$ in the pressure relaxation equation (ref: paper Eq. 94).

### Success Criteria

| Criterion | Status |
|-----------|--------|
| Smooth transition from diffusive to wavelike behavior | [SOLID] Confirmed |
| $\hat{\sigma} = 0.15$: stable throughout | [SOLID] Confirmed |
| $\hat{\sigma} = 1.5$: no apparent instability (mild violation) | [SOLID] Confirmed |
| $\hat{\sigma} = 7.5$: oscillatory instability onset (severe violation) | [SOLID] Confirmed |
| Peak splitting for large $\hat{\sigma}$ (wavelike behavior) | [SOLID] Confirmed |
| All solutions show some wavelike transient | [SOLID] Confirmed (inset) |
| Consistent with telegrapher's equation limit | [SOLID] Confirmed |

### Associated Figures

**Fig. 6 (telegraphers_plot.pdf):** Three-panel wide figure.
- **Left panel (early time):** All three cases ($\hat{\sigma} = 0.15, 1.5, 7.5$) shown in light gray to black. Central peak begins to decay and spread.
- **Middle panel (intermediate time):** $\hat{\sigma} = 7.5$ shows peak splitting (wavelike). Inset shows wavelike transient present in all cases.
- **Right panel (late time):** $\hat{\sigma} = 7.5$ exhibits oscillatory instability. $\hat{\sigma} = 0.15, 1.5$ remain well-behaved.

### Figure Analysis: Telegrapher's Equation Transition (Fig. 6, `telegraphers_plot.pdf`)

**Three side-by-side panels** showing the spatial temperature profile $T(x)$ at different evolution times ($t = 16$, $39$, $312$). Three curves in each panel: $\hat{\sigma} = 0.15$ (light gray), $\hat{\sigma} = 1.5$ (medium gray), $\hat{\sigma} = 7.5$ (black). Vertical axis: $T$ ranging from $1.000$ to $1.100$ (the background equilibrium is $T = 1.0$). Horizontal axis: $x \in [-100, 100]$.

**Left panel ($t = 16$, early time):** All three solutions show a single central temperature peak at $x = 0$ that is beginning to decay and spread, resembling diffusion. The curves nearly overlap, with peak heights $T \approx 1.075\text{--}1.08$.

**Middle panel ($t = 39$, intermediate time):** The transition becomes apparent. The $\hat{\sigma} = 0.15$ solution retains a smooth, single-peaked diffusive profile. The $\hat{\sigma} = 7.5$ solution exhibits clear **peak splitting**: the central maximum has divided into two counter-propagating peaks, the hallmark of wave-equation solutions. An inset shows that even the $\hat{\sigma} = 0.15$ solution possesses a small wavelike transient propagating outward at the sound speed, demonstrating that BDNK theory is fundamentally hyperbolic even when the solution appears predominantly diffusive.

**Right panel ($t = 312$, late time):** The $\hat{\sigma} = 0.15$ and $1.5$ solutions show broad, smooth, decayed profiles. The $\hat{\sigma} = 7.5$ solution displays a dramatic **oscillatory instability**: high-frequency oscillations have developed and spread across the domain. This is a direct consequence of violating the linear stability constraint $\hat{\sigma} \leq 1/3$ (since $7.5 \gg 1/3$). The $\hat{\sigma} = 1.5$ case also violates this bound ($1.5 > 1/3$) but does not show visible instability, suggesting the bound is sufficient but may not be necessary.

**Physical picture:** The figure numerically demonstrates the transition from the parabolic heat equation to the hyperbolic wave equation as $\hat{\sigma}$ and $\hat{\tau}$ increase while holding $\hat{\sigma}/\hat{\tau} = 0.1$ constant (keeping the thermal propagation speed $c_B^2$ approximately fixed).

---

## 11. Convergence Results (Appendix B, Fig. 7, Table III)

### 11.1 ODE Convergence (Table III)

[SOLID] All ODE tests use the fourth-order explicit Runge-Kutta method (RK4). Convergence is measured using the convergence factor (ref: paper Eq. B1):

$$
Q_N = \frac{\|R_{N/2}\|}{\|R_N\|}
$$

where $R_N$ is a discrete residual computed using an **independent** fourth-order centered finite difference discretization. This independence is crucial: the residual is not computed from the same numerical scheme used to solve the ODE, but from a separate discretization of the governing equations.

**Table III reproduction** (ref: paper Table III):

| Test | $N$ | $Q_{N/4}$ | $Q_{N/2}$ | $Q_N$ |
|------|-----|-----------|-----------|-------|
| Bjorken flow, $\hat{\tau} = 0.5$ | $2^{11}$ | $34.8$ | $18.7$ | $16.9$ |
| Bjorken flow, $\hat{\tau} = 1$ | $2^{11}$ | $18.4$ | $16.9$ | $16.3$ |
| Bjorken flow, $\hat{\tau} = 2$ | $2^{11}$ | $16.9$ | $16.3$ | $16.1$ |
| Shockwave ODE | $2^{13}$ | $15.9$ | $15.9$ | $15.9$ |

All cases demonstrate $Q_N \to 16$ as $N$ increases, confirming fourth-order convergence consistent with the RK4 method.

**Note on Bjorken residual:** The residual for Bjorken flow is an independent fourth-order centered finite difference discretization of the Bjorken ODE (ref: paper Eq. 66). For the shockwave case, a fourth-order centered finite difference discretization of the $t$-component of (ref: paper Eq. 1), namely $T^{tx}_{,x} = 0$, is used.

**Note on stiff cases:** The $\hat{\tau} = 0.5$ case (stiffest, always superluminal) shows the slowest convergence toward $Q_N = 16$, with $Q_{N/4} = 34.8$ indicating pre-asymptotic behavior at coarser resolutions. The $\hat{\tau} = 2$ case (least stiff, always subluminal) converges most rapidly.

### 11.2 PDE Convergence (Fig. 7)

[SOLID] PDE solutions use the conservative finite volume method of Pandya (2022) with Heun's method (TVD RK2) and WENO/CWENO spatial discretization. The scheme is second-order overall, so we expect $Q_N \to 4$ as $N \to \infty$.

**Convergence measure:** Same $Q_N$ formula, but the residual $R_N$ is computed using an **independent** second-order Crank-Nicolson discretization of the $t$-component of (ref: paper Eq. 1).

**Fig. 7 shows $Q_N(t)$ for two cases:**

**Left panel (stable shockwave, bottom panel of Fig. 3):**
- At early times near $t = 0$: $Q_N \approx 4$, confirming second-order convergence.
- At $t \sim 80$: significant interaction with the ghost cell boundary occurs (transients from initial data propagate to the boundary).
- After boundary interaction: $Q_N$ degrades, converging at a rate between first and second order.

**Right panel (heat flow, $\hat{\sigma} = 0.15$ from Fig. 6):**
- At early times near $t = 0$: $Q_N \approx 4$, confirming second-order convergence.
- At $t \sim 150$: boundary interaction occurs.
- After boundary interaction: $Q_N$ degrades to between first and second order.

### 11.3 Convergence Degradation Mechanism

[SOLID] The degradation of convergence from second order ($Q_N \to 4$) to between first and second order at late times is attributed to **boundary interaction**: transients from the initial data propagate outward and eventually reach the ghost cell boundaries. The ghost cell boundary conditions introduce errors that are not consistent with the interior scheme's convergence order, reducing the effective convergence rate.

This is a well-understood numerical phenomenon and does not indicate any problem with the BDNK equations or the numerical scheme itself. The key result is that the solutions converge at the expected rate prior to boundary interaction.

### Associated Figures

**Fig. 7 (conv_plot.pdf):**
- **Left panel:** $Q_N(t)$ for the stable shockwave (bottom panel of Fig. 3). Second-order convergence ($Q_N \approx 4$) up to $t \sim 80$, then degradation.
- **Right panel:** $Q_N(t)$ for the $\hat{\sigma} = 0.15$ heat flow (Fig. 6). Second-order convergence ($Q_N \approx 4$) up to $t \sim 150$, then degradation.

### Figure Analysis: Convergence Plot (Fig. 7, `conv_plot.pdf`)

**Two side-by-side panels** showing the convergence factor $Q_N(t)$ as a function of time. Three resolutions are shown in each panel ($N = 2^{11}, 2^{12}, 2^{13}$, light gray to black). A horizontal red dotted line at $Q_N = 4$ marks the expected second-order convergence rate.

**Left panel (shockwave problem):** At early times ($t < 80$), all three curves cluster tightly around $Q_N = 4$, confirming second-order convergence. The highest-resolution curve ($N = 2^{13}$, black) stays closest to 4. Starting around $t \sim 80\text{--}100$, the convergence factor deviates as outgoing transients interact with ghost cell boundaries: curves dip below 4 (reaching $Q_N \sim 2$ for $N = 2^{13}$) and partially recover with persistent oscillations. At late times ($t > 300$), values settle between $\sim 3.5$ and $4.5$.

**Right panel (heat flow problem, $\hat{\sigma} = 0.15$):** Qualitatively similar but with a sharper disruption. $Q_N \approx 4$ up to $t \sim 150$. Around $t \sim 160\text{--}180$, a dramatic spike occurs as boundary-reflected signals contaminate the interior. After this transient, $Q_N$ fluctuates but the $N = 2^{13}$ curve settles near $Q_N \sim 3.5$.

**Physical interpretation:** The degradation from $Q_N = 4$ to values between 2 and 4 at late times is attributed to ghost cell boundary interaction. The boundary treatment is at best first-order accurate, so boundary-reflected signals drag the overall convergence rate toward first order. The key result is that the scheme achieves the expected second-order rate prior to boundary interaction.

---

## 12. Validation Strategy

### 12.1 Independent Checks Performed

[SOLID] The validation strategy employs multiple levels of independent verification:

1. **ODE convergence:** The residual used to compute $Q_N$ is discretized using an independent fourth-order centered finite difference scheme, separate from the RK4 solution method. This ensures convergence is measured against an independent standard.

2. **PDE convergence:** The residual is computed using an independent second-order Crank-Nicolson discretization, separate from the Heun/WENO solution method.

3. **Analytic cross-checks:**
   - Inviscid Bjorken solution (ref: paper Eq. 67) serves as a known reference for the viscous solutions.
   - Equilibrium state comparison (ref: paper Eqs. 56--59) is verified analytically.
   - Constant-coefficient heat flow reduces to known equations (heat, telegrapher's, wave), providing independent validation of the numerical heat flow results.
   - Rankine-Hugoniot conditions (ref: paper Eq. 80) are used to fix shockwave asymptotic states, providing a consistency check.

4. **Multi-frame comparison:** The same physical problem is solved in multiple hydrodynamic frames. Frame-independent observables (e.g., $T^{ab}$) should agree between frames. This is verified in the Bjorken flow test (Fig. 1, bottom panel) where the BDNK-frame and Eckart-frame temperatures agree at late times (equilibrium).

5. **Resolution studies:** All PDE tests are shown at multiple numerical resolutions. Instabilities are distinguished from numerical artifacts by convergence behavior:
   - Features that grow and sharpen with resolution are physical.
   - Features that diminish with resolution are numerical artifacts.

### 12.2 Summary of Pass/Fail Criteria

[SOLID]

| Test | Pass Criteria | Result |
|------|---------------|--------|
| Equilibrium states | BDNK and MIS equations algebraically equivalent | **Pass** |
| Bjorken flow | All $\hat{\tau}$ values approach inviscid solution; $Q_N \sim 16$ | **Pass** |
| Steady-state shockwave | Smooth profile obtained; $Q_N \sim 16$ | **Pass** |
| Dynamic shockwave (stable, $\hat{\tau}=1.5$) | Evolves to late times, approaches steady-state ODE solution | **Pass** |
| Dynamic shockwave (unstable, $\hat{\tau}=3$) | Instability localized to $v > c_+$ region | **Pass** |
| Acausality (weak, $\hat{\tau}=0.5$) | Solution agrees with subluminal case | **Pass** |
| Acausality (stiff, $\hat{\tau}=0.4$) | Same solution, requires small CFL | **Pass** |
| Acausality (wild, $\hat{\tau}=0.25$) | Instability converges with resolution (physical) | **Pass** |
| Heat stationary ($\hat{\sigma}=0$) | $\dot{\epsilon} \to 0$ with resolution | **Pass** |
| Heat stationary ($\hat{\sigma}=1/3$) | $\dot{\epsilon} \to$ nonzero with resolution | **Pass** |
| Telegrapher ($\hat{\sigma}=0.15$) | Stable, diffusive behavior | **Pass** |
| Telegrapher ($\hat{\sigma}=1.5$) | No instability despite mild constraint violation | **Pass** |
| Telegrapher ($\hat{\sigma}=7.5$) | Oscillatory instability onset (expected) | **Pass** |
| ODE convergence | $Q_N \to 16$ | **Pass** |
| PDE convergence | $Q_N \to 4$ pre-boundary interaction | **Pass** |

All tests pass their respective success criteria. [SOLID]

---

## 13. Summary of Key Physical Insights from the Test Suite

### 13.1 On Causality

[SOLID] The test suite provides strong evidence that superluminal characteristics do not necessarily imply acausal propagation. Physical features (shockwave transients) propagate at the sound speed, regardless of the characteristic speed. This is analogous to gauge dynamics in general relativity. However, requiring subluminal characteristics **guarantees** causality and is essential for constructing a sensible relativistic fluid theory.

### 13.2 On Stability

[SOLID] The relationship between the linear stability constraint ($\hat{\sigma} \leq 1/3$) and actual stability is nuanced:
- Mild violations appear benign (possibly stabilized by nonlinear effects or slow instability growth).
- Severe violations trigger clear oscillatory instability.
- The shockwave instability mechanism ($v > c_+$) is distinct from the heat flow instability mechanism (negative relaxation time $\tau_\theta$).

### 13.3 On the BDNK Relaxation Structure

[SOLID] The test suite confirms that BDNK theory applies dissipation through a relaxation mechanism that is structurally identical to MIS theory (on the restricted class of spatially isotropic initial data). This relaxation arises from the addition of on-shell higher-order terms to the Eckart stress-energy tensor, and is responsible for causality.

### 13.4 On Frame Dependence

[SOLID] The temperature $T$ and other hydrodynamic variables are frame-dependent outside equilibrium. This has concrete consequences:
- $T < 0$ is allowed in far-from-equilibrium states
- Different frames yield different relaxation timescales
- Frame-independent observables ($T^{ab}$) agree across frames upon equilibration
- The choice of frame determines whether a given shockwave is stable ($c_+ > v$) or unstable ($v > c_+$)

### 13.5 On Heat Flow

[SOLID] The ideal gas model uniquely enables "pure" heat flow solutions (temperature gradient at constant pressure), impossible for conformal fluids. The BDNK heat flow equation has telegrapher's equation structure, providing a causal generalization of the acausal heat equation obtained in Eckart theory.
