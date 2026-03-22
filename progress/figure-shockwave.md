# Figure Analysis: Steady-State Shockwave Profiles (`shockwave_plot.pdf`)

**Figure label:** `fig:shockwave_profile`
**Source:** Paper Sec. III.C, line 1014--1028 (caption); discussion lines 992--1012.
**Parameters from Table I (line 555):** Gamma = 4/3, m = 0.1, V_hat = 2/15, sigma_hat = 0, tau_hat = 1.5.

---

## 1. Visual Description

The figure shows steady-state shockwave profiles for a BDNK (Bemfica--Disconzi--Noronha--Kovtun) viscous relativistic fluid. The profiles are obtained by solving the coupled system of ODEs (Eqs. shockwave_nprime, shockwave_epsP, shockwave_velP) that describe a planar shockwave in its rest frame, where all quantities depend only on the spatial coordinate x. Two distinct fluids are compared on the same axes: a non-conformal ideal gas BDNK fluid (black curves) and a conformal BDNK fluid (green curves), both sharing the same asymptotic left state and shear viscosity.

The plot displays three physical quantities---energy density epsilon, three-velocity v, and baryon number density n---as functions of the spatial coordinate x, each transitioning smoothly from their left asymptotic values (as x -> -infinity) to their right asymptotic values (as x -> +infinity). The smooth transition replaces the step-function discontinuity that would appear in the inviscid (perfect fluid) solution.

---

## 2. Axes and Labels

- **Horizontal axis:** Spatial coordinate x, ranging from -2 to +2. The shockwave is centered near x = 0.
- **Vertical axis:** f(x), a generic label for the plotted quantity, ranging from 0 to approximately 4.5.
- **Legend (top-left corner):**
  - Solid line: f = epsilon (energy density)
  - Dash-dot line: f = v (three-velocity in the x-direction)
  - Dotted line: f = n (baryon number density)

All three quantities share the same vertical axis; their scales are such that epsilon has the largest dynamic range (from ~1 on the left to ~4.5 on the right), while v and n have smaller ranges.

---

## 3. Line Styles and Color Coding

- **Black curves:** BDNK fluid with relativistic ideal gas ("gamma-law") equation of state (Eq. EOS: P = (Gamma - 1) m n e) and the hydrodynamic frame defined in Eq. hydro_frame. This is the primary model studied in the paper, featuring non-conformal microphysics with a finite particle mass m = 0.1.
- **Green curves:** Conformal BDNK fluid with the "sharply causal" hydrodynamic frame (equation 16, frame B of Pandya & Pretorius 2021). This serves as a benchmark comparison, reproducing the earlier conformal analysis in a context where the equation of state is P = epsilon/3.

For each color, three line styles are used:
  - **Solid:** energy density epsilon(x)
  - **Dash-dot:** velocity v(x)
  - **Dotted:** baryon number density n(x)

---

## 4. Key Observations

### 4.1 Shared Qualitative Structure
Both the ideal gas (black) and conformal (green) profiles exhibit the expected shockwave structure: a smooth monotonic transition from left-state values to right-state values. The energy density increases from left to right (compression), the velocity decreases from left to right (deceleration), and the baryon number density increases from left to right (compression of matter).

### 4.2 Differences in the Energy Density Profile
The most visually striking difference between the two fluids is in the energy density (solid lines). The black (ideal gas) profile is noticeably steeper and transitions more sharply than the green (conformal) profile, which has a broader, more gradual sigmoid shape. On the left side (x < 0), the conformal epsilon profile begins to rise earlier (further to the left) than the ideal gas profile. On the right side (x > 0), both profiles converge to similar asymptotic values near epsilon ~ 4.3--4.5, though the conformal profile reaches its plateau slightly sooner.

### 4.3 Differences in the Velocity Profile
The velocity profiles (dash-dot lines) start at v_L = 0.8 on the left for both cases, as stated in the caption (both share the same asymptotic left state {epsilon, v, n} = {1, 0.8, 0.1}). The conformal (green) dash-dot curve sits slightly above the ideal gas (black) one on the far left, though both asymptote to the same v_L = 0.8. Moving rightward, both decrease monotonically through the shock transition. The ideal gas velocity profile transitions more sharply than the conformal one, consistent with the steeper epsilon profile. On the right side, the two profiles converge to slightly different right-state velocities, reflecting the different Rankine-Hugoniot jump conditions arising from the distinct equations of state.

### 4.4 Differences in the Number Density Profile
The baryon number density profiles (dotted lines) both start at n_L = 0.1 on the left. The ideal gas n profile is nearly flat on the left side and rises slightly later and more steeply than the conformal profile. The green dotted curve begins rising somewhat earlier. The right-state values are comparable but not identical, reflecting the different Rankine-Hugoniot jump conditions arising from the distinct equations of state.

### 4.5 Shockwave Width
The conformal fluid shockwave appears slightly broader overall, with the transition spread over a wider region in x. This is consistent with the different transport coefficients and relaxation time structures in the two models, even though both share the same shear viscosity.

### 4.6 No Singular Behavior
Crucially, for both profiles the velocity v never attains a value equal to the characteristic speeds c_+ or c_-, meaning the denominators in the shockwave ODEs never vanish. This is a necessary condition for the steady-state solution to exist.

---

## 5. Numerical / Implementation Notes

### 5.1 ODE System
The steady-state shockwave is governed by three coupled first-order ODEs:
- **Baryon conservation (Eq. shockwave_nprime):** n' = -W^2 n v' / v
- **Energy density (Eq. shockwave_epsP):** epsilon'(x) = [quartic polynomial in v] / [A W v (v^2 - c_+^2)(v^2 - c_-^2)]
- **Velocity (Eq. shockwave_velP):** v'(x) = [cubic polynomial in v] / [A W^3 (v^2 - c_+^2)(v^2 - c_-^2)]

The numerator coefficients c_i, d_i (given in Eq. on lines 979--986) depend on the stress-energy tensor components T^{tx}, T^{xx} (which are constants of integration), the transport coefficients, and thermodynamic quantities.

### 5.2 Constants of Integration
The two constant stress-energy components T^{tx} and T^{xx} are computed from the asymptotic left state using the perfect-fluid stress-energy tensor:
- T^{tx} = rho W^2 v, evaluated at {epsilon_L, v_L, n_L} = {1, 0.8, 0.1}
- T^{xx} = rho W^2 v^2 + P, evaluated at the same left state

This is valid because the asymptotic states (x -> +/- infinity) should be in thermodynamic equilibrium where the viscous corrections vanish.

### 5.3 Left State
Both the ideal gas and conformal shockwaves use:
- epsilon_L = 1 (energy density)
- v_L = 0.8 (three-velocity)
- n_L = 0.1 (baryon number density)

### 5.4 Solver
All ODEs in the paper are integrated using the **fourth-order explicit Runge-Kutta method (RK4)** (Appendix, line 1434). For the shockwave ODE, resolutions up to N = 2^13 gridpoints are used. The convergence factor Q_N approaches 15.9 (close to the theoretical value of 16 for a fourth-order scheme), confirming fourth-order convergence (Table ODE_conv, line 1447).

### 5.5 Residual Check
Convergence is verified by computing a discrete residual using a fourth-order centered finite difference discretization of the t-component of the stress-energy conservation law, T^{tx}_{,x} = 0, which should be identically zero for exact solutions.

---

## 6. Connection to Theory: Characteristic Speeds and Shockwave Existence

### 6.1 Characteristic Speed Constraint
The denominators of the shockwave ODEs (Eqs. shockwave_epsP, shockwave_velP) are proportional to (v^2 - c_+^2)(v^2 - c_-^2), where c_+/- are two of the three characteristic speeds of the BDNK system (Eq. cpmsq_general, line 969--971). If the velocity profile v(x) ever attains the value v = c_+ or v = c_-, the ODEs become singular unless the numerators simultaneously vanish (which is difficult to verify analytically due to the high polynomial order of the numerators).

### 6.2 Existence Criterion
Empirically, the paper finds:
- When v_L < c_+: a nontrivial shockwave solution exists, as shown in this figure.
- When v_L >= c_+: the solver finds only the trivial equilibrium state where all quantities remain constant (equal to their left-state values) for all x.

This means that the maximum characteristic speed c_+ sets an upper bound on the flow velocities that can be accommodated by steady-state shockwave solutions.

### 6.3 Link to Dynamical Stability
The paper (lines 1060--1076) further demonstrates that when a shockwave forms dynamically (via time-dependent PDE evolution from smooth initial data), the evolution is stable only when c_+ > |v| across the entire shockwave profile---precisely the case where the steady-state ODE solution exists. When v exceeds c_+, a high-frequency numerical instability develops. This is consistent with the rigorous result of Freistuhler (2021) for conformal BDNK fluids, which proved that shockwave solutions break down unless the maximum characteristic speed is >= 1 (the speed of light).

### 6.4 Implication for Frame Choice
This motivates choosing hydrodynamic frames where c_+ is at least as large as the fastest flow velocity in the problem, or even requiring c_+ = 1 (the "sharply causal" limit). The conformal fluid shown in green uses exactly such a sharply causal frame (frame B of Pandya & Pretorius 2021), ensuring c_+ = 1 and thus guaranteeing both causality and shockwave existence for all subluminal flows.

---

## 7. Parameter Summary

| Parameter | Symbol | Value | Description |
|-----------|--------|-------|-------------|
| Adiabatic index | Gamma | 4/3 | Gamma-law EOS exponent |
| Particle mass | m | 0.1 | Rest mass per particle |
| Inverse Reynolds number | V_hat | 2/15 | Dimensionless combined viscosity |
| Thermal conductivity parameter | sigma_hat | 0 | No thermal conductivity |
| Relaxation time parameter | tau_hat | 1.5 | Controls characteristic speeds |
| Lengthscale | L | 1 | Set to unity for simplicity |
| Left-state energy density | epsilon_L | 1 | Asymptotic value as x -> -infinity |
| Left-state velocity | v_L | 0.8 | Asymptotic value as x -> -infinity |
| Left-state number density | n_L | 0.1 | Asymptotic value as x -> -infinity |

The hydrodynamic frame sets tau_epsilon = tau_Q = L * V_hat * tau_hat and tau_P = 2(Gamma - 1) L * V_hat. With sigma_hat = 0, there is no thermal conductivity contribution (sigma = 0). The relaxation time parameter tau_hat = 1.5 is chosen to satisfy the causality constraint tau_hat >= [(Gamma - 1)(2 - c_s^2) + c_s^2] / (1 - c_s^2), ensuring subluminal characteristic speeds for the ideal gas case.
