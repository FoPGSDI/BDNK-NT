# Plan: test-results.md — Comprehensive Documentation of All Numerical Tests

This document outlines what needs to be documented in `test-results.md`, covering every numerical test in the paper, the validation strategy, figure descriptions, and test design principles.

---

## 1. Test Suite Inventory

The paper contains **seven distinct numerical tests** organized into four physical categories. Each test maps to one or more figures and entries in Table I. The documentation must enumerate all of them systematically.

### Test 1: Trivial Equilibrium States — Eckart vs BDNK vs MIS (Sec. III.A)

**What to document:**
- **Purpose:** Show that BDNK and MIS share the same relaxation-type dissipation mechanism, while Eckart applies dissipation instantaneously (acausally). Demonstrate "purely frame" dynamics — systems where T^{ab} is static but hydrodynamic variables evolve.
- **Initial conditions:** Spatially isotropic states (Eq. 23): epsilon, n nonzero and spatially uniform; no spatial gradients; dot{epsilon} != 0 for BDNK; pi^{tt} != 0 for MIS; dot{u}^i = 0 for all theories.
- **Parameters:** Not in Table I (this is an analytic comparison, not a numerical integration shown in a figure).
- **Expected analytical behavior:** All three theories reduce to Eq. (32):
  - Eckart: epsilon = T^{tt} (no dynamics, instantaneous equilibration)
  - BDNK: dot{epsilon} = (1/tau_epsilon)(T^{tt} - epsilon) — relaxation ODE
  - MIS: identical to BDNK with identification tau_epsilon = tau_pi + c_1
  - Analytic solution Eq. (33): epsilon(t) = T^{tt} + (epsilon_0 - T^{tt}) exp(-t/tau)
- **Key observables:** The relaxation timescale tau; the exponential decay of out-of-equilibrium epsilon toward T^{tt}.
- **Success criteria:** BDNK and MIS equations of motion are algebraically equivalent on this data. Eckart has no dynamics. Frame-dependent temperature Eq. (35) illustrates non-uniqueness outside equilibrium.
- **Connection to figures:** No dedicated figure; this is a purely analytic derivation used to motivate later tests.

### Test 2: Bjorken Flow (0+1D) — Fig. 1

**What to document:**
- **Purpose:** Investigate how relaxation times tau_epsilon, tau_P, tau_Q affect solutions in a dynamical setting. Two key questions: (1) Does the solution qualitatively change when characteristics are superluminal? (2) What happens when dissipation is applied too slowly (tau -> infinity)?
- **Initial conditions:** Milne coordinates. epsilon_0 = 0.25, dot{epsilon}_0 in {-2, 0, 2}, n_0 = 0.1, integrated from tau = 1 to tau = 20.
- **Parameters from Table I (Fig. 1):** Gamma = 4/3, m = 1, V_hat = 1/10, sigma_hat = 0, tau_hat in {0.5, 1, 2}.
- **Expected analytical behavior:**
  - Inviscid solution Eq. (39): epsilon(tau) = m n_0 tau^{-1} [1 + e_0 tau^{-(Gamma-1)}]
  - tau_hat -> infinity limit Eq. (40): epsilon(tau) = c_1 tau^{-1} + c_2
  - tau_hat -> 0 limit: characteristics diverge, equations become stiff, but no qualitative change
- **Key observables:**
  - Top panel: dot{epsilon} + Gamma epsilon/tau (equals m n_0 (Gamma-1)/tau^2 for inviscid solution, independent of e_0)
  - Bottom panel: Temperature T in BDNK frame vs Eckart frame temperature T_E
  - Maximum characteristic speed c_+ for each tau_hat value
- **Characteristic speed values to document:**
  - tau_hat = 0.5: c_+ ~ 1.3 (always superluminal)
  - tau_hat = 1: c_+ ~ 1.05 at early times, ~ 0.9 at late times
  - tau_hat = 2: c_+ ~ 0.7 (always subluminal)
- **Success criteria:**
  - All three tau_hat values produce same qualitative behavior (approach inviscid solution)
  - Larger tau_hat -> slower equilibration (as expected)
  - Superluminal characteristics do NOT qualitatively change solution
  - Negative temperatures allowed when initial data is far from equilibrium; BDNK frame T < 0 does not crash
- **Connection to figures:** Fig. 1 (bjorken_plot.pdf) — two panels (top: convergence to inviscid; bottom: temperature in two frames).

### Test 3: Steady-State Shockwave Profiles (1+1D ODE) — Fig. 2

**What to document:**
- **Purpose:** Generalize conformal shockwave analysis from Pandya (2021) to arbitrary BDNK fluids with ideal gas microphysics. Compare ideal gas vs conformal shockwave profiles.
- **Initial conditions:** Asymptotic left state {epsilon_L, v_L, n_L} = {1, 0.8, 0.1} as x -> -infinity. Right state determined by Rankine-Hugoniot conditions.
- **Parameters from Table I (Fig. 2):** Gamma = 4/3, m = 0.1, V_hat = 2/15, sigma_hat = 0, tau_hat = 1.5.
- **Expected analytical behavior:** System of coupled ODEs (Eqs. 44-47). Denominators vanish when v = +/- c_+/-, which means no smooth solution exists if velocity profile crosses characteristic speed. For v_L < c_+, a smooth shockwave profile connecting left and right states should exist. For v_L >= c_+, solver finds trivial constant state.
- **Key observables:** Profiles of epsilon(x), v(x), n(x) for both ideal gas (black) and conformal (green) fluids. Shape and width of shockwave transition region.
- **Success criteria:** Smooth profiles obtained. Velocity never reaches c_+ or c_-. Ideal gas and conformal profiles are qualitatively similar but quantitatively different. ODE convergence is fourth-order (Table II).
- **Connection to figures:** Fig. 2 (shockwave_plot.pdf) — three-panel plot showing epsilon, v, n profiles.

### Test 4: Dynamic Shockwaves — Stability and Frame Dependence (1+1D PDE) — Fig. 3

**What to document:**
- **Purpose:** Test what happens when a shockwave forms dynamically. Investigate whether instability occurs when flow velocity exceeds the maximum characteristic speed c_+.
- **Initial conditions:** Error-function interpolation Eq. (50) with width w = 10.
  - Left-right state pair (for Fig. 3): {1, 0.9, 1}_L -> {11.5174, 0.354727, 5.44212}_R
- **Parameters from Table I (Fig. 3):** Gamma = 4/3, m = 0.1, V_hat = 4/3, sigma_hat = 0, tau_hat in {1.5, 3}.
- **Expected behavior:**
  - Top panel (tau_hat = 1.5): High-frequency numerical instability onset where v > c_+
  - Bottom panel (tau_hat = 3): c_+ > v everywhere, stable evolution to late times, asymptotes to steady-state ODE solution
- **Key observables:**
  - Velocity profile v(x) vs characteristic speed c_+(x) (dotted line)
  - Onset of instability at the point where v crosses c_+
  - Multiple numerical resolutions shown (darker = finer)
- **Success criteria:**
  - Instability onset localized to region where v > c_+ (causal mechanism identified)
  - Stable frame (tau_hat = 3) runs to late times and matches steady-state solution
  - Consistent with rigorous result of Freistuhler (2021) for conformal case
- **Connection to figures:** Fig. 3 (shock_instability.pdf) — two panels (top: unstable; bottom: stable).

### Test 5: Acausality / Superluminal Frame Tests — Fig. 4

**What to document:**
- **Purpose:** Systematically test behavior across a range of superluminal frames, from weakly to wildly superluminal.
- **Initial conditions:** Same error-function interpolation Eq. (50) with w = 10.
  - Left-right state pair (for Fig. 4): {1, 0.6, 1}_L -> {1.33795, 0.514414, 1.25027}_R
- **Parameters from Table I (Fig. 4):** Gamma = 4/3, m = 0.1, V_hat = 4/3, sigma_hat = 0, tau_hat in {0.25, 0.4, 0.5, 1.5}.
- **Characteristic speed values:**
  - tau_hat = 1.5: c_+ ~ 0.9 (subluminal, reference)
  - tau_hat = 0.5: c_+ ~ 1.5 (weakly superluminal)
  - tau_hat = 0.4: c_+ ~ 1.6 (stiff superluminal)
  - tau_hat = 0.25: c_+ ~ 2.0 (wildly superluminal)
- **Expected behavior:**
  - Top panel: tau_hat = 0.4, 0.5, 1.5 all produce solutions identical up to plot resolution at late times (t = 1582). No features propagate superluminally.
  - Bottom panel: tau_hat = 0.25 triggers very fast instability — unbounded growth of bump near x ~ 20, sharp feature at x ~ 40 that appears to diverge in finite time.
- **Key observables:**
  - Late-time solutions for different frames (top panel)
  - Onset and growth of instability (bottom panel)
  - Convergence of sharp feature with resolution (inset, N in {2^7, ..., 2^11})
  - CFL requirements: tau_hat = 0.4 requires lambda = 0.01 (10x smaller than others)
- **Success criteria:**
  - Weakly superluminal: identical solutions, no acausal propagation
  - Stiff superluminal: same solution but requires very small CFL
  - Wildly superluminal: instability is physical (converges with resolution), likely related to failure of linear stability proof
- **Connection to figures:** Fig. 4 (acaus_instab.pdf) — two panels (top: late-time agreement; bottom: instability growth with inset).

### Test 6: Heat Flow — Stationary Test (sigma_hat = 0 vs sigma_hat = 1/3) — Fig. 5

**What to document:**
- **Purpose:** Confirm that nonzero thermal conductivity (sigma != 0) is required for dynamical heat flow solutions. This is unique to the ideal gas model — conformal fluids cannot have "pure" heat flow since P propto T^4.
- **Initial conditions:** Eq. (59): T(0,x) = A exp(-x^2/w^2) + delta with P(0,x) = P_0 = const. Time-symmetric: dot{epsilon}(0,x) = dot{u}^i(0,x) = 0.
- **Parameters from Table I (Fig. 5):** Gamma = 4/3, m = 0.1, V_hat = 2/15, sigma_hat in {0, 1/3}, tau_hat = 1.5.
- **Expected behavior:**
  - sigma_hat = 0: dot{epsilon} converges to zero with resolution (no dynamics; purely numerical error)
  - sigma_hat = 1/3: dot{epsilon} converges to nonzero value (genuine heat flow dynamics)
- **Key observables:** Snapshots of dot{epsilon}(x) at t shortly after 0, at multiple resolutions (darker = higher resolution).
- **Success criteria:**
  - sigma_hat = 0: dot{epsilon} -> 0 as resolution increases (convergence to zero)
  - sigma_hat = 1/3: dot{epsilon} -> nonzero function (convergence to continuum solution)
  - Confirms Eq. (61): ddot{epsilon} = 0 when kappa = 0
- **Connection to figures:** Fig. 5 (heat_stationary.pdf) — two panels (top: sigma=0; bottom: sigma=1/3).

### Test 7: Telegrapher's Equation Behavior — Fig. 6

**What to document:**
- **Purpose:** Demonstrate transition from heat-equation-like (parabolic) to wave-like (hyperbolic) behavior as sigma_hat increases, consistent with the constant-coefficient analysis showing telegrapher's equation structure. Also test linear stability constraint violation.
- **Initial conditions:** Same as Test 6 — Gaussian temperature perturbation at constant pressure.
- **Parameters from Table I (Fig. 6):** Gamma = 4/3, m = 0.1, V_hat = 2/15, sigma_hat in {0.15, 1.5, 7.5}, tau_hat in {1.5, 15, 75}. Note: sigma_hat/tau_hat = 0.1 held constant to keep c_B^2 finite.
- **Linear stability status:**
  - sigma_hat = 0.15: satisfies sigma_hat <= 1/3 (stable)
  - sigma_hat = 1.5: VIOLATES sigma_hat <= 1/3 (mildly unstable)
  - sigma_hat = 7.5: VIOLATES sigma_hat <= 1/3 (strongly unstable)
- **Expected behavior:**
  - sigma_hat = 0.15: Heat-equation-like decay of central peak; small wavelike transient visible in inset
  - sigma_hat = 1.5: Intermediate behavior; no apparent instability despite violating stability bound
  - sigma_hat = 7.5: Central peak splits into two propagating waves (telegrapher's regime); oscillatory instability at late times crashes simulation
- **Key observables:**
  - Left panel: early-time snapshots showing initial decay/spreading
  - Middle panel: intermediate time — sigma_hat = 7.5 shows peak splitting
  - Right panel: late time — sigma_hat = 7.5 shows oscillatory instability
  - Inset: zoom showing small wavelike transient present in ALL cases
- **Success criteria:**
  - Smooth transition from parabolic to hyperbolic behavior
  - sigma_hat = 0.15 (within bounds): stable throughout
  - sigma_hat = 1.5 (mild violation): no apparent instability — either stabilized by nonlinear effects or instability timescale >> dynamical timescale
  - sigma_hat = 7.5 (large violation): clear oscillatory instability onset
  - Consistent with telegrapher's equation limit (Eqs. 53-55)
- **Connection to figures:** Fig. 6 (telegraphers_plot.pdf) — three-panel wide figure (left: early; middle: intermediate; right: late).

---

## 2. Per-Test Documentation Template

For each of the seven tests above, `test-results.md` should contain a section structured as follows:

```
### Test N: [Name]

#### Purpose
- Physical question addressed
- Why this test matters for BDNK theory validation

#### Setup
- Spatial symmetry (0+1D, 1+1D)
- Coordinate system (Milne, Cartesian)
- Governing equation (ODE vs PDE; equation number reference)
- Initial conditions (with equation references)
- Parameters (from Table I)
- Boundary conditions (where applicable)

#### Analytical Expectations
- Known exact/asymptotic solutions
- Limiting behaviors (tau -> 0, tau -> infinity, sigma -> 0, etc.)
- Connection to known equations (heat equation, telegrapher's, wave equation)

#### Key Results
- Description of numerical findings
- Frame-dependent vs frame-independent observables
- Comparison across parameter values

#### Success Criteria
- Quantitative convergence metrics (where applicable)
- Qualitative behavior matching expectations
- Stability/instability onset conditions

#### Associated Figures
- Figure number and filename
- What each panel shows
- How to read the figure
```

---

## 3. Test Design Principles

The documentation must include a section explaining the overall design philosophy behind the test suite. Topics to cover:

### 3.1 Causality Validation
- **Mechanism:** Causality is ensured by requiring ALL characteristic speeds c_+, c_-, c_1 (Eqs. A12-A13) to be subluminal (|c| < 1).
- **How tests probe it:** Tests 2, 4, 5 systematically vary tau_hat to cross the causality boundary. The key constraint is tau_hat >= [(Gamma-1)(2 - c_s^2) + c_s^2] / (1 - c_s^2).
- **Key finding to document:** Weakly superluminal characteristics do NOT produce acausal propagation or qualitative solution changes. Physical features propagate at sound speed, not at characteristic speed. Analogy to gauge dynamics in GR.

### 3.2 Linear Stability Validation
- **Mechanism:** Linear stability about equilibrium requires sigma_hat <= 1/3 (for the chosen frame). This is a simplified bound; full constraints are Eqs. STAB A1-E.
- **How tests probe it:** Test 7 systematically violates the sigma_hat <= 1/3 bound with sigma_hat = 1.5 and 7.5.
- **Key finding to document:** Mild violations appear benign; severe violations trigger oscillatory instability. The bound is sufficient but may not be necessary (nonlinear stabilization possible).

### 3.3 Constraint Violation Boundary Probing
- **Causality boundary:** Tests 2 and 5 map out the transition from subluminal -> weakly superluminal -> wildly superluminal.
- **Stability boundary:** Test 7 maps out the transition from within-bounds -> mild violation -> severe violation.
- **Shockwave existence boundary:** Tests 3 and 4 probe when v crosses c_+ (steady-state solution ceases to exist).
- **Key design insight:** The test suite is designed to explore behavior BOTH within and outside the proven bounds, to understand how robust the bounds are and what failure modes look like.

### 3.4 Convergence Testing Methodology
- **ODE tests (Bjorken, steady-state shockwave):**
  - Method: RK4 (fourth-order explicit Runge-Kutta)
  - Convergence measure: Q_N = ||R_{N/2}|| / ||R_N|| (Eq. A6)
  - Expected: Q_N -> 16 (fourth-order)
  - Residual R_N: independent fourth-order centered finite difference discretization
  - Results: Table II — all ODE tests demonstrate Q_N ~ 16
- **PDE tests (dynamic shockwave, heat flow):**
  - Method: Conservative finite volume (Pandya 2022), Heun's method (TVD RK2), WENO/CWENO spatial discretization
  - CFL number: lambda = 0.1 (default), 0.01 for stiff/wildly superluminal cases
  - Convergence measure: Same Q_N, but using second-order Crank-Nicolson residual
  - Expected: Q_N -> 4 (second-order)
  - Results: Fig. 7 — second-order convergence until boundary interaction, then between first and second order

---

## 4. Figure Descriptions Plan

### Fig. 1 (bjorken_plot.pdf) — Bjorken Flow
- **Top panel:** tau vs (dot{epsilon} + Gamma epsilon/tau). Three line styles for tau_hat = {0.5, 1, 2}, three initial conditions each. Red dashed = inviscid solution. Document: convergence rate depends on tau_hat; superluminal cases indistinguishable qualitatively.
- **Bottom panel:** tau vs Temperature for tau_hat = 2. Black solid = BDNK frame T. Blue dashed = Eckart frame T_E. Document: one solution has T < 0 (far-from-equilibrium initial data).

### Fig. 2 (shockwave_plot.pdf) — Steady-State Shockwave Profile
- **Three panels:** epsilon(x), v(x), n(x) profiles. Black = ideal gas. Green = conformal. Document: smooth transition between asymptotic states; ideal gas has additional structure from nonzero mass and baryon current.

### Fig. 3 (shock_instability.pdf) — Dynamic Shockwave Stability
- **Top panel:** Unstable case (tau_hat = 1.5). Multiple resolutions (dark = fine). Dotted line = c_+. Document: instability where v > c_+.
- **Bottom panel:** Stable case (tau_hat = 3). Late-time snapshot. Document: c_+ > v everywhere, stable evolution.

### Fig. 4 (acaus_instab.pdf) — Acausality Instability
- **Top panel:** Late-time comparison of tau_hat = {0.4, 0.5, 1.5}. Document: all solutions agree at t = 1582 despite different causality properties. No superluminal propagation observed.
- **Bottom panel:** Wildly superluminal (tau_hat = 0.25). Dotted/dot-dash/solid = time progression. Inset: sharp feature at multiple resolutions. Document: instability converges with resolution (physical, not numerical).

### Fig. 5 (heat_stationary.pdf) — Heat Flow Stationarity
- **Top panel:** sigma_hat = 0, multiple resolutions. Document: dot{epsilon} -> 0 (no dynamics).
- **Bottom panel:** sigma_hat = 1/3, multiple resolutions. Document: dot{epsilon} -> nonzero (genuine heat flow).

### Fig. 6 (telegraphers_plot.pdf) — Telegrapher's Equation Behavior
- **Three panels (left, middle, right):** Time progression for sigma_hat = {0.15, 1.5, 7.5}. Document: transition from diffusive to wave-like. Peak splitting for sigma_hat = 7.5. Inset in middle panel showing wavelike transient in all cases. Oscillatory instability in right panel for sigma_hat = 7.5.

### Fig. 7 (conv_plot.pdf) — Convergence Plots
- **Two panels:** Q_N(t) for stable shockwave (left) and sigma_hat = 0.15 heat flow (right). Document: second-order convergence (Q -> 4) at early times, degrading to 1-2 order after boundary interaction.

---

## 5. Validation Strategy

### 5.1 Independent Checks Performed
- **ODE convergence:** Independent finite-difference residual discretization (4th-order centered) used to compute Q_N, separate from the RK4 solution method.
- **PDE convergence:** Independent Crank-Nicolson residual used to compute Q_N, separate from the Heun/WENO solution method.
- **Analytic cross-checks:**
  - Inviscid Bjorken solution (Eq. 39) used as reference
  - Equilibrium state comparison (Eq. 32-33) verified analytically
  - Constant-coefficient heat flow reduces to known equations (heat, telegrapher's, wave)
  - Rankine-Hugoniot conditions used to fix shockwave asymptotic states
- **Multi-frame comparison:** Same physical problem solved in multiple frames; frame-independent observables (T^{ab}) should agree.
- **Resolution studies:** All PDE tests shown at multiple resolutions; instabilities distinguished from numerical artifacts by convergence behavior.

### 5.2 Convergence Criteria
- **Fourth-order (ODE):** Q_N -> 16 as N -> infinity. Table II shows values 15.9-18.7 for N = 2^{11}-2^{13}.
- **Second-order (PDE):** Q_N -> 4 as N -> infinity. Fig. 7 shows Q_N ~ 4 at early times.
- **Degradation mechanism:** Boundary interaction from propagating transients reduces convergence to ~1st-2nd order at late times.

### 5.3 What Constitutes a "Passing" Test

| Test | Pass Criteria |
|------|---------------|
| Equilibrium states | BDNK and MIS equations algebraically equivalent |
| Bjorken flow | All tau_hat values approach inviscid solution; Q_N ~ 16 |
| Steady-state shockwave | Smooth profile obtained; Q_N ~ 16 |
| Dynamic shockwave (stable) | Evolves to late times, approaches steady-state ODE solution |
| Dynamic shockwave (unstable) | Instability localized to v > c_+ region |
| Acausality (weak) | Solution agrees with subluminal case |
| Acausality (wild) | Instability converges with resolution (physical) |
| Heat stationary (sigma=0) | dot{epsilon} -> 0 with resolution |
| Heat stationary (sigma=1/3) | dot{epsilon} -> nonzero with resolution |
| Telegrapher (sigma=0.15) | Stable, diffusive behavior |
| Telegrapher (sigma=1.5) | No instability despite mild constraint violation |
| Telegrapher (sigma=7.5) | Oscillatory instability onset (expected) |
| PDE convergence | Q_N ~ 4 pre-boundary interaction |

---

## 6. Additional Sections to Include

### 6.1 Table I Reproduction
Reproduce Table I (parameter summary) in the documentation with additional columns for:
- Which constraint equations are satisfied/violated
- Maximum characteristic speed c_+ for each case
- Whether the case is expected to be stable/unstable

### 6.2 Table II Reproduction
Reproduce Table II (ODE convergence results) verbatim.

### 6.3 Physical Glossary
Brief definitions of key quantities that appear throughout:
- Relaxation times (tau_epsilon, tau_P, tau_Q) and what they control
- Dimensionless parameters (hat quantities) and their physical meaning
- V_hat as inverse Reynolds number
- sigma_hat as dimensionless thermal conductivity
- tau_hat as dimensionless relaxation time controlling characteristic speeds
- c_+, c_-, c_1 characteristic speeds and their roles

### 6.4 Cross-References to Other Progress Documents
- Link to analysis of theoretical framework
- Link to figure reproduction methodology
- Link to code implementation notes (if applicable)

---

## 7. Writing Order

Suggested order for writing `test-results.md`:

1. Physical glossary / parameter definitions (Section 6.3)
2. Table I with annotations (Section 6.1)
3. Test design principles (Section 3) — gives context for reading individual tests
4. Individual test sections in paper order (Tests 1-7, Section 1)
5. Figure descriptions integrated into each test section (Section 4)
6. Validation strategy and convergence (Section 5)
7. Summary table of pass/fail criteria (Section 5.3)
