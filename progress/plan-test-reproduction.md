# Test Reproduction and Validation Plan

## Reference

All tests reproduce figures from: Pandya, Most, Pretorius, "Causal, stable first-order viscous relativistic hydrodynamics with ideal gas microphysics."

PDF figures located at `/Users/hyw/Desktop/Agent/BDNK/`:
- `bjorken_plot.pdf` (Fig 1), `shockwave_plot.pdf` (Fig 2), `shock_instability.pdf` (Fig 3)
- `acaus_instab.pdf` (Fig 4), `heat_stationary.pdf` (Fig 5), `telegraphers_plot.pdf` (Fig 6)
- `conv_plot.pdf` (Fig 7)

---

## 1. Priority Ordering

| Priority | Figure | Type | Complexity | Rationale |
|----------|--------|------|------------|-----------|
| 1 | Fig 1 (Bjorken) | ODE (RK4) | Low | Single second-order ODE, analytic reference available, self-contained |
| 2 | Fig 2 (Shockwave profile) | ODE (RK4) | Low-Medium | Three coupled first-order ODEs, same RK4 solver, but requires initialization near asymptotic state |
| 3 | Fig 7 (Convergence) | PDE diagnostic | Medium | Validates PDE solver infrastructure; requires Figs 3 and 6 runs as inputs |
| 4 | Fig 3 (Shock instability) | PDE (FV) | Medium | Full PDE solver needed; two parameter cases; instability must be reproduced |
| 5 | Fig 4 (Acausal instability) | PDE (FV) | Medium-High | Four parameter cases; CFL variation; wildly superluminal case is stiff |
| 6 | Fig 5 (Heat stationary) | PDE (FV) | Medium | Same PDE solver, but different initial data (Gaussian temperature profile); unknown parameters A, delta, w, P0 |
| 7 | Fig 6 (Telegrapher's) | PDE (FV) | Medium | Same PDE solver and initial data as Fig 5; three parameter cases; late-time instability |

**Implementation phases:**
- Phase A: ODE infrastructure + Figs 1, 2 (validates EOS, transport coefficients, RK4)
- Phase B: PDE infrastructure + Figs 3, 5 (validates conservative FV, WENO, Heun)
- Phase C: Remaining figures + Fig 7 convergence (validates full pipeline)

---

## 2. Figure-by-Figure Reproduction Specifications

### 2.1 Figure 1: Bjorken Flow (`bjorken_plot.pdf`)

**Problem type:** (0+1)D ODE, second order, reduced to first-order system

**Parameters:**

| Parameter | Value |
|-----------|-------|
| Gamma | 4/3 |
| m | 1 |
| Vhat | 1/10 |
| sigma_hat | 0 |
| tau_hat | 0.5, 1, 2 |
| epsilon_0 | 0.25 |
| epsdot_0 | -2, 0, 2 |
| n_0 | 0.1 |
| Domain | tau in [1, 20] |

**ODE system (state vector y = {epsilon, epsdot}):**

```
dy1/dtau = y2
dy2/dtau = (1/tau_eps) * [ -(1/tau)*(tau + 2*tau_eps + tau_P)*y2
                            -(1/tau^2)*(rho*(tau + tau_P) - V) ]
```

where at each evaluation:
- n = n0/tau
- P = (Gamma-1)*(eps - m*n)
- rho = eps + P
- cs2 = Gamma*P/rho
- V = Vhat * rho * cs2 (since L=1)
- tau_eps = Vhat * tau_hat
- tau_P = 2*(Gamma-1)*Vhat

**Inviscid reference:** epsilon_dot + Gamma*epsilon/tau = m*n0*(Gamma-1)/tau^2

**Plot specifications:**

*Top panel (log-log):*
- X-axis: tau (log scale, range [1, 20])
- Y-axis: |epsdot + Gamma*epsilon/tau| (log scale, range ~[1e-4, 1])
- 9 black curves: 3 families of 3 (one per epsdot_0), families distinguished by line style
  - Solid: tau_hat = 0.5
  - Dash-dot: tau_hat = 1
  - Dotted: tau_hat = 2
- 1 red dashed thick line: inviscid solution m*n0*(Gamma-1)/tau^2
- Legend: "Vhat = 0", "tau_hat = 0.5", "tau_hat = 1", "tau_hat = 2"

*Bottom panel (linear-log):*
- X-axis: tau (log scale, range [1, 20])
- Y-axis: T (linear, range ~[-0.6, 2.2])
- 3 black solid curves: BDNK temperature T = (Gamma-1)*(epsilon/n - m) for tau_hat=2 solutions
- 3 blue dashed curves: Eckart temperature T_E computed from T^{tau tau}
  - T^{tau tau} = epsilon + tau_eps * epsdot (the frame correction delta_epsilon = -tau_eps * epsdot gives T^{tau tau} = epsilon - delta_epsilon)
  - Actually: T^{tau tau}_Eckart = epsilon_E, so epsilon_E = T^{tau tau} = epsilon + tau_eps*epsdot + (additional terms from stress tensor at u^a = (1,0,0,0))
  - More precisely: compute the full T^{tau tau} from the BDNK stress-energy tensor, set epsilon_E = T^{tau tau}, then T_E = (Gamma-1)*(epsilon_E/n - m)
- Legend: "tau_hat = 2", "BDNK", "Eckart"

**Acceptance criteria:**
1. All 9 curves in top panel must converge onto the inviscid reference at late tau
2. Solid (tau_hat=0.5) curves must converge fastest, dotted (tau_hat=2) slowest
3. Some curves must plunge steeply downward (the plotted quantity passes through zero) before recovering
4. Bottom panel: one solution must exhibit T < 0 (the epsdot_0 = -2 case)
5. BDNK and Eckart temperatures must converge at late tau
6. Quantitative: at tau=20, max relative deviation of |epsdot + Gamma*eps/tau| from inviscid reference < 10% for tau_hat=0.5 case

---

### 2.2 Figure 2: Steady-State Shockwave Profiles (`shockwave_plot.pdf`)

**Problem type:** (1+1)D ODE, three coupled first-order equations

**Parameters:**

| Parameter | Value |
|-----------|-------|
| Gamma | 4/3 |
| m | 0.1 |
| Vhat | 2/15 |
| sigma_hat | 0 |
| tau_hat | 1.5 |
| epsilon_L, v_L, n_L | 1, 0.8, 0.1 |

**Derived constants (computed from left state):**
- P_L = (Gamma-1)*(epsilon_L - m*n_L) = (1/3)*(1 - 0.01) = 0.33
- rho_L = epsilon_L + P_L = 1.33
- W_L = 1/sqrt(1 - 0.64) = 1/0.6 = 5/3
- T^{tx} = rho_L * W_L^2 * v_L
- T^{xx} = rho_L * W_L^2 * v_L^2 + P_L

**Right state:** Determined by Rankine-Hugoniot conditions (solve nonlinear system)

**ODE system:** See paper Eqs. 72-77. State vector y = {n, epsilon, v}.
- n' = -W^2 * n * v'/v
- epsilon' = (c4*v^4 + c3*v^3 + c2*v^2 + c1*v + c0) / [A*W*v*(v-cp)(v+cp)(v-cm)(v+cm)]
- v' = (d3*v^3 + d2*v^2 + d1*v + d0) / [A*W^3*(v-cp)(v+cp)(v-cm)(v+cm)]

**Initialization:** Start near left asymptotic state at large negative x with small perturbation. The paper does not specify the exact initialization procedure. Use a linearization of the ODE about the left equilibrium state to determine the perturbation direction (eigenvector of the linearized system with negative eigenvalue, i.e., the stable manifold direction).

**Also compute:** Conformal BDNK fluid (green curves) with same shear viscosity and sharply causal frame B of Pandya 2021. NOTE: reproducing the conformal comparison is optional for initial validation; the primary target is the black (ideal gas) curves.

**Plot specifications:**
- Single panel
- X-axis: x (range [-2, 2])
- Y-axis: f(x) (range [0, ~5])
- Three quantities plotted with different line styles:
  - Solid: f = epsilon
  - Dash-dot: f = v
  - Dotted: f = n
- Two colors:
  - Black: ideal gas BDNK fluid
  - Green: conformal BDNK fluid (optional for initial validation)
- Legend: "f = epsilon", "f = v", "f = n"

**Acceptance criteria:**
1. Smooth monotonic transitions from left to right state for all three quantities
2. epsilon transitions from 1 (left) to a higher right-state value (~4-5)
3. v transitions from 0.8 (left) to a lower right-state value
4. n transitions from 0.1 (left) to a higher right-state value (~0.5-0.8)
5. Profile is centered near x=0
6. Velocity never reaches c_+ or c_-
7. Quantitative: right-state values must satisfy Rankine-Hugoniot conditions to within 0.1%

---

### 2.3 Figure 3: Dynamic Shockwave Stability (`shock_instability.pdf`)

**Problem type:** (1+1)D PDE (full BDNK equations)

**Parameters:**

| Parameter | Value |
|-----------|-------|
| Gamma | 4/3 |
| m | 0.1 |
| Vhat | 4/3 |
| sigma_hat | 0 |
| tau_hat | 3 (unstable, top panel), 1.5 (stable, bottom panel) |
| epsilon_L, v_L, n_L | 1, 0.9, 1 |
| epsilon_R, v_R, n_R | 11.5174, 0.354727, 5.44212 |
| w (erf width) | 10 |
| CFL lambda | 0.1 |
| Resolutions | N = 2^9, 2^10, 2^11 |

**Initial data (error function interpolation):**
- epsilon(0,x) = (eps_R - eps_L)/2 * [erf(x/w) + 1] + eps_L
- v(0,x) = (v_L - v_R)/2 * [1 - erf(x/w)] + v_R
- n(0,x) = (n_L - n_R)/2 * [1 - erf(x/w)] + n_R
- Time derivatives: edot(0,x) = 0, vdot(0,x) = 0 (assumed, not explicitly stated)

**Plot specifications:**

*Top panel (unstable, tau_hat=3):*
- X-axis: x (range [-50, 50])
- Y-axis: v (range [0.5, 0.9])
- Snapshot at t = 27
- Three resolution levels shown (N = 2^9, 2^10, 2^11) in light gray to black
- Horizontal dotted line at c_+ ~ 0.75
- Inset: magnified view of shock transition region showing oscillatory instability
- Labels: "t = 27", "tau_hat = 3"

*Bottom panel (stable, tau_hat=1.5):*
- X-axis: x (range [-50, 50])
- Y-axis: v (range [0.4, 1.0])
- Snapshot at t = 372
- Three resolution levels (same gray scale)
- Horizontal dotted line at c_+ ~ 0.94
- Labels: "t = 372", "tau_hat = 1.5", resolution legend

**Acceptance criteria:**
1. Top panel: oscillatory instability visible in region where v > c_+ ~ 0.75
2. Top panel: instability persists and sharpens with increasing resolution
3. Bottom panel: smooth, monotonic transition with no oscillation
4. Bottom panel: all three resolutions indistinguishable (converged)
5. Both panels: upstream velocity v_L correct (0.9), downstream v_R correct (~0.35)
6. Smooth "bump" feature visible downstream of shock in top panel

---

### 2.4 Figure 4: Acausality/Instability Tests (`acaus_instab.pdf`)

**Problem type:** (1+1)D PDE (full BDNK equations)

**Parameters:**

| Parameter | Value |
|-----------|-------|
| Gamma | 4/3 |
| m | 0.1 |
| Vhat | 4/3 |
| sigma_hat | 0 |
| tau_hat | 0.25, 0.4, 0.5, 1.5 |
| epsilon_L, v_L, n_L | 1, 0.6, 1 |
| epsilon_R, v_R, n_R | 1.33795, 0.514414, 1.25027 |
| w (erf width) | 10 |
| CFL lambda | 0.1 (tau_hat=0.5, 1.5); 0.01 (tau_hat=0.25, 0.4) |

**Plot specifications:**

*Top panel (weakly superluminal, tau_hat = 0.4, 0.5, 1.5):*
- X-axis: x (range [-100, 100])
- Y-axis: v (range [0.5, 0.6])
- Dotted line: t = 0 (initial data)
- Solid line: t = 1582 (late time, all three frames overlapping)
- All three frames produce visually identical late-time solutions
- Labels: "tau_hat = 0.4, 0.5, 1.5", "t = 0", "t = 1582"

*Bottom panel (wildly superluminal, tau_hat = 0.25):*
- X-axis: x (range [-100, 100])
- Y-axis: v (range [0.5, 0.6])
- Three time snapshots: t = 0.27 (dotted), t = 0.31 (dash-dot), t = 0.36 (solid)
- Growing bump near x ~ 10-20, sharp dip near x ~ 40-50
- Inset: sharp feature at 5 resolutions (N = 2^7 through 2^11), light gray to black
- Labels: "tau_hat = 0.25", time values

**Acceptance criteria:**
1. Top panel: all three late-time solutions identical up to plot resolution
2. Top panel: no superluminal signal propagation
3. Bottom panel: unboundedly growing bump that does not propagate
4. Bottom panel: sharp dip feature that converges with resolution (shown in inset)
5. Quantitative: late-time velocity profile v transitions from ~0.6 to ~0.515

---

### 2.5 Figure 5: Heat Flow Stationary Test (`heat_stationary.pdf`)

**Problem type:** (1+1)D PDE (full BDNK equations)

**Parameters:**

| Parameter | Value |
|-----------|-------|
| Gamma | 4/3 |
| m | 0.1 |
| Vhat | 2/15 |
| sigma_hat | 0 (top panel), 1/3 (bottom panel) |
| tau_hat | 1.5 |
| CFL lambda | 0.1 |
| Resolutions | N = 2^7, 2^8, 2^9 |

**Initial data:**
- T(0,x) = A * exp(-x^2/w^2) + delta, P(0,x) = P0 = const
- Convert: epsilon = P*(m/T + 1/(Gamma-1)), n = P/T
- Time-symmetric: epsdot(0,x) = 0, udot^i(0,x) = 0

**UNKNOWN parameters (not in Table II):** A (Gaussian amplitude), delta (temperature offset), w (width), P0 (constant pressure). These must be inferred from the figure or code.

From the telegrapher's figure (Fig 6), T ranges from ~1.000 to ~1.100, suggesting:
- delta ~ 1.0 (background temperature)
- A ~ 0.1 (amplitude, giving peak T ~ 1.1)
- w ~ 10-20 (based on the spatial scale of the profiles in Fig 5, peaks at x ~ +/- 45)
- P0: from the EOS at equilibrium, with T ~ 1.0 and n ~ P/T, a reasonable choice might be P0 ~ 0.1 or similar

**ACTION REQUIRED:** Check the BDNK-NT code repository or Mathematica notebooks for exact values. If unavailable, calibrate by matching the spatial structure of Fig 5 bottom panel.

**Plot specifications:**

*Top panel (sigma_hat = 0):*
- X-axis: x (range [-100, 100])
- Y-axis: |epsdot| (range [0, ~3e-6], scale x10^{-6})
- Three curves at resolutions N = 2^7, 2^8, 2^9 (light gray to black)
- Noisy, oscillatory features near x = 0 that decrease with resolution
- Inset: magnified central region showing amplitude reduction
- Label: "sigma_hat = 0"

*Bottom panel (sigma_hat = 1/3):*
- X-axis: x (range [-100, 100])
- Y-axis: |epsdot| (range [0, ~1.5e-4], scale x10^{-4})
- Three curves at same resolutions, tightly overlapping
- Rich spatial structure with multiple symmetric peaks at x ~ +/- 45
- Inset: near x ~ 50 showing convergence
- Label: "sigma_hat = 1/3"

**Acceptance criteria:**
1. Top panel: |epsdot| decreases with resolution, converging to zero
2. Bottom panel: |epsdot| converges to a nonzero value with symmetric multi-peak structure
3. Scale difference: bottom panel ~ 100x larger than top panel (1e-4 vs 1e-6)
4. The spatial structure of the bottom panel must be qualitatively correct (peaks at roughly the right positions)

---

### 2.6 Figure 6: Telegrapher's Equation Behavior (`telegraphers_plot.pdf`)

**Problem type:** (1+1)D PDE (full BDNK equations)

**Parameters:**

| Parameter | Value |
|-----------|-------|
| Gamma | 4/3 |
| m | 0.1 |
| Vhat | 2/15 |
| sigma_hat | 0.15, 1.5, 7.5 |
| tau_hat | 1.5, 15, 75 |
| sigma_hat/tau_hat | 0.1 (constant across all cases) |
| CFL lambda | 0.1 |

**Initial data:** Same as Fig 5 (Gaussian temperature profile at constant pressure).

**Plot specifications:**

Three side-by-side panels (wide figure, textwidth):
- X-axis: x (range [-100, 100] in each panel, labeled with -75, 0, 75)
- Y-axis: T (range [1.000, 1.100], shared across panels)

*Left panel (t = 16, early time):*
- Three curves: sigma_hat = 0.15 (light gray), 1.5 (medium gray), 7.5 (black)
- All show a single central peak at x = 0, peak height T ~ 1.075-1.08
- Curves nearly overlap
- Label: "t = 16"

*Middle panel (t = 39, intermediate time):*
- sigma_hat = 0.15: smooth, single-peaked diffusive profile
- sigma_hat = 7.5: peak splitting into two counter-propagating peaks
- sigma_hat = 1.5: intermediate behavior
- Inset: zoomed view showing wavelike transient in all cases
- Label: "t = 39"

*Right panel (t = 312, late time):*
- sigma_hat = 0.15, 1.5: broad, smooth, decayed profiles
- sigma_hat = 7.5: oscillatory instability (high-frequency oscillations)
- Label: "t = 312"

*Legend (in left panel):* "sigma_hat = 0.15", "sigma_hat = 1.5", "sigma_hat = 7.5"

**Acceptance criteria:**
1. Left panel: all three curves nearly overlapping, single central peak
2. Middle panel: sigma_hat = 7.5 shows clear peak splitting (wavelike)
3. Middle panel: inset shows wavelike transient in all three cases
4. Right panel: sigma_hat = 7.5 shows oscillatory instability
5. Right panel: sigma_hat = 0.15 and 1.5 remain smooth and well-behaved
6. Quantitative: background temperature T ~ 1.0, peak heights match

---

### 2.7 Figure 7: Convergence Plot (`conv_plot.pdf`)

**Problem type:** Diagnostic (computed from PDE solutions)

**Input data:**
- Left panel: stable shockwave (bottom panel of Fig 3, tau_hat = 1.5)
- Right panel: heat flow (sigma_hat = 0.15 from Fig 6)

**Resolutions:** N = 2^11, 2^12, 2^13

**Convergence factor:**
Q_N(t) = ||R_{N/2}|| / ||R_N||
where R_N is an independent Crank-Nicolson residual of the t-component of nabla_a T^{ab} = 0.
Norm: 1-norm (sum of absolute values).

**Plot specifications:**

Two side-by-side panels:
- X-axis: t
- Y-axis: Q_N(t) (range [1, ~9])

*Left panel (shockwave):*
- X-axis range: t in [0, ~400]
- Three curves: N = 2^11 (light gray), 2^12 (medium gray), 2^13 (black)
- Red dotted horizontal line at Q_N = 4
- Q_N ~ 4 for t < 80, then degradation after boundary interaction

*Right panel (heat flow):*
- X-axis range: t in [0, ~450]
- Same three curves and red reference line
- Q_N ~ 4 for t < 150, sharp spike near t ~ 160-180, then settling

**Acceptance criteria:**
1. Both panels: Q_N ~ 4 at early times (within 10% of 4)
2. Left panel: degradation onset near t ~ 80
3. Right panel: sharp disruption near t ~ 150-180
4. Highest resolution (N = 2^13) stays closest to Q_N = 4
5. After boundary interaction: Q_N between ~2 and ~8

---

## 3. Validation Methodology

### 3.1 Quantitative Comparison Metrics

For each figure, validation uses a tiered approach:

**Tier 1 -- Qualitative match (REQUIRED for PASS):**
- Correct number of curves, correct topology (e.g., monotonic vs oscillatory)
- Correct axis scales and ranges (log vs linear, order of magnitude)
- Correct qualitative behavior (convergence to reference, instability onset, etc.)

**Tier 2 -- Semi-quantitative match (REQUIRED for PASS):**
- Key feature values within 5% (e.g., asymptotic states, peak heights, crossing points)
- Correct ordering of curves (which converges fastest, which is most unstable)
- Correct spatial/temporal locations of features (e.g., instability onset time, peak positions within 10%)

**Tier 3 -- Quantitative match (TARGET, not strictly required):**
- Pointwise relative error < 2% at selected sample points read from the paper figures
- Convergence factors within 0.5 of paper values (e.g., Q_N = 16 +/- 0.5 for ODE)
- Rankine-Hugoniot conditions satisfied to < 0.1%

### 3.2 Comparison Procedure

**Step 1: Visual overlay**
- Export our Mathematica plots as PDF
- Visually compare side-by-side with the paper's PDF figures
- Check axis labels, ranges, line styles, legend entries

**Step 2: Spot-check key values**
Read off specific numerical values from the paper figures and compare:

| Figure | Key values to check |
|--------|---------------------|
| Fig 1 top | Value of inviscid reference at tau=1 and tau=20; convergence time of each tau_hat family |
| Fig 1 bottom | Temperature at tau=1 for each epsdot_0; sign of T for bottom-most curve |
| Fig 2 | Left-state values (eps=1, v=0.8, n=0.1); right-state values; transition width |
| Fig 3 | c_+ values (dotted lines); instability location; snapshot times (t=27, t=372) |
| Fig 4 | Late-time velocity profile shape; instability growth times; v_L and v_R values |
| Fig 5 | Scale of |epsdot| (1e-6 top, 1e-4 bottom); peak positions; convergence behavior |
| Fig 6 | Background temperature (~1.0); peak heights (~1.075-1.10); instability onset time |
| Fig 7 | Q_N ~ 4 at early times; boundary interaction times (t~80, t~150) |

**Step 3: Convergence verification (ODE tests)**
- Compute Q_N at multiple resolutions and compare to Table III:
  - Bjorken tau_hat=0.5: Q at N=2^11 should be ~16.9
  - Bjorken tau_hat=1: Q at N=2^11 should be ~16.3
  - Bjorken tau_hat=2: Q at N=2^11 should be ~16.1
  - Shockwave: Q at N=2^13 should be ~15.9

### 3.3 PASS/FAIL Criteria

| Verdict | Criteria |
|---------|----------|
| **PASS** | Tier 1 and Tier 2 both satisfied; qualitative and semi-quantitative agreement |
| **CONDITIONAL PASS** | Tier 1 satisfied; Tier 2 has minor deviations (< 10%) attributable to known causes |
| **FAIL** | Tier 1 not satisfied (wrong qualitative behavior) OR Tier 2 deviations > 20% |

### 3.4 Known Sources of Discrepancy

The following discrepancies are expected and do NOT constitute failures:

1. **Heat flow initial data parameters (A, delta, w, P0):** Not fully specified in the paper. Figs 5 and 6 may require parameter tuning. Document the values used.

2. **Shockwave ODE initialization:** The linearization procedure at the asymptotic state is not documented. Small differences in initialization affect the profile's x-position but not its shape.

3. **Conformal comparison (Fig 2, green curves):** Reproducing the conformal BDNK fluid requires the frame B of Pandya 2021, which is outside the scope of the ideal gas implementation. Only the black (ideal gas) curves are required.

4. **PDE boundary effects:** Outflow boundary conditions are implementation-dependent. Late-time convergence degradation is expected and acceptable.

5. **CFL sensitivity for stiff cases:** The exact CFL values (0.1 vs 0.01) may need adjustment based on the specific PDE solver implementation.

---

## 4. Shared Infrastructure Requirements

Before any figure can be reproduced, the following Mathematica modules must be implemented and verified:

### 4.1 Equation of State Module

```
(* Required functions *)
ComputeP[eps, n, Gamma, m]        (* Pressure *)
ComputeRho[eps, n, Gamma, m]      (* Enthalpy density *)
ComputeCs2[eps, n, Gamma, m]      (* Sound speed squared *)
ComputeKappaEps[eps, n, Gamma, m] (* kappa_epsilon *)
ComputeKappaN[eps, n, Gamma, m]   (* kappa_n *)
ComputeKappaS[eps, n, Gamma, m]   (* kappa_s *)
ComputeAlpha[eps, n, Gamma, m]    (* alpha = p'_eps / cs2 *)
ComputeOmega[eps, n, Gamma, m]    (* omega = kappa_s / kappa_eps *)
```

**Verification:** Check algebraic identities:
- P = (Gamma-1)*(eps - m*n)
- rho = Gamma*eps - (Gamma-1)*m*n
- cs2 = Gamma*P/rho
- kappa_s = kappa_eps + kappa_n = -(Gamma-1)*m*rho/n

### 4.2 Transport Coefficient Module

```
(* Required functions, all take (eps, n, Gamma, m, Vhat, sigmahat, tauhat) *)
ComputeV[...]         (* Combined viscosity V = Vhat * rho * cs2 *)
ComputeTauEps[...]    (* tau_epsilon = Vhat * tauhat *)
ComputeTauP[...]      (* tau_P = 2*(Gamma-1)*Vhat *)
ComputeTauQ[...]      (* tau_Q = Vhat * tauhat *)
ComputeSigma[...]     (* sigma = Vhat * rho * cs2 * sigmahat / (-kappa_eps) *)
ComputeBetaEps[...]   (* beta_epsilon *)
ComputeBetaN[...]     (* beta_n *)
```

**Note:** tau_eps, tau_P, tau_Q are CONSTANTS (do not depend on state).
V, sigma, beta_eps, beta_n depend on state and must be recomputed at each step.

**Verification:** Check that for sigma_hat=0: sigma=0, and the beta coefficients reduce to simpler forms.

### 4.3 Characteristic Speed Module

```
ComputeCpm[eps, n, Gamma, m, Vhat, sigmahat, tauhat]  (* Returns {c_+, c_-} *)
ComputeC1[eps, n, Gamma, m, Vhat, sigmahat, tauhat]   (* Returns c_1 *)
```

**Verification:** Check values against Table in test-results.md:
- Fig 1 params, tau_hat=0.5: c_+ ~ 1.3
- Fig 1 params, tau_hat=2: c_+ ~ 0.7
- Fig 3 params, tau_hat=3: c_+ ~ 0.75
- Fig 3 params, tau_hat=1.5: c_+ ~ 0.94

### 4.4 Rankine-Hugoniot Solver

```
SolveRankineHugoniot[epsL, vL, nL, Gamma, m]  (* Returns {epsR, vR, nR} *)
```

**Verification:** Check against known values:
- {1, 0.9, 1}_L -> {11.5174, 0.354727, 5.44212}_R
- {1, 0.6, 1}_L -> {1.33795, 0.514414, 1.25027}_R

---

## 5. Cycle Documentation Template

Each validation attempt is documented in a cycle file named:
`/Users/hyw/Desktop/Agent/BDNK/progress/cycle-FIGNUM-ATTEMPT.md`

Example: `cycle-fig1-01.md`, `cycle-fig2-03.md`

### Template

```markdown
# Validation Cycle: Figure N, Attempt M

## Date
YYYY-MM-DD

## Target
Figure N: [description] from paper

## Parameters Used
| Parameter | Value |
|-----------|-------|
| ... | ... |

## Code Files Modified
- /path/to/file1.wl -- [description of changes]
- /path/to/file2.wl -- [description of changes]

## Execution
- Mathematica version: [version]
- Runtime: [duration]
- Any warnings/errors: [none / description]

## Results

### Visual Comparison
[Side-by-side description: what matches, what differs]

### Spot-Check Values
| Quantity | Paper Value | Our Value | Relative Error | Status |
|----------|-------------|-----------|----------------|--------|
| ... | ... | ... | ... | PASS/FAIL |

### Convergence Check (if applicable)
| N | Q_N (paper) | Q_N (ours) | Status |
|---|-------------|------------|--------|
| ... | ... | ... | PASS/FAIL |

## Verdict
[PASS / CONDITIONAL PASS / FAIL]

## Issues Found
1. [description]
2. [description]

## Actions for Next Cycle
1. [what to fix]
2. [what to investigate]
```

---

## 6. Implementation Roadmap

### Phase A: ODE Infrastructure (Target: Figs 1, 2)

**Step A1:** Implement EOS module. Verify all thermodynamic identities.

**Step A2:** Implement transport coefficient module. Verify tau_eps, tau_P, tau_Q are constants. Verify V, sigma, beta depend on state correctly.

**Step A3:** Implement characteristic speed module. Verify against known values from test-results.md.

**Step A4:** Implement RK4 solver (generic, reusable).

**Step A5:** Implement Bjorken flow RHS function. Integrate for all 9 parameter/IC combinations.

**Step A6:** Compute inviscid reference. Compute Eckart temperature. Generate Fig 1.

**Step A7:** Validate Fig 1 (cycle-fig1-01.md).

**Step A8:** Implement Rankine-Hugoniot solver. Verify against known right states.

**Step A9:** Implement shockwave ODE RHS function. Set up initialization near left asymptotic state.

**Step A10:** Integrate shockwave ODE. Generate Fig 2 (black curves only).

**Step A11:** Validate Fig 2 (cycle-fig2-01.md).

**Step A12:** Compute ODE convergence factors Q_N for Bjorken and shockwave. Compare to Table III.

### Phase B: PDE Infrastructure (Target: Figs 3, 5)

**Step B1:** Implement conservative formulation (conserved variables T^{tt}, T^{tx}, J^t and fluxes).

**Step B2:** Implement primitive variable recovery (conserved -> primitive).

**Step B3:** Implement spatial reconstruction (WENO or simpler alternative for initial testing).

**Step B4:** Implement Heun's method (TVD-RK2) time integrator.

**Step B5:** Implement ghost cell / outflow boundary conditions.

**Step B6:** Set up shockwave PDE initial data (error function profiles). Generate Fig 3.

**Step B7:** Validate Fig 3 (cycle-fig3-01.md).

**Step B8:** Set up heat flow initial data (Gaussian temperature). Generate Fig 5.

**Step B9:** Validate Fig 5 (cycle-fig5-01.md).

### Phase C: Remaining Figures (Target: Figs 4, 6, 7)

**Step C1:** Run shockwave PDE with four tau_hat values and different CFL numbers. Generate Fig 4.

**Step C2:** Validate Fig 4 (cycle-fig4-01.md).

**Step C3:** Run heat flow PDE with three sigma_hat/tau_hat combinations. Generate Fig 6.

**Step C4:** Validate Fig 6 (cycle-fig6-01.md).

**Step C5:** Compute PDE convergence factors Q_N(t) using Crank-Nicolson residual. Generate Fig 7.

**Step C6:** Validate Fig 7 (cycle-fig7-01.md).

---

## 7. Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Heat flow initial data parameters (A, delta, w, P0) unknown | Cannot reproduce Figs 5, 6 quantitatively | Inspect BDNK-NT code; if unavailable, calibrate from figure features |
| Shockwave ODE initialization procedure unknown | Profile may be shifted in x or fail to converge | Use linearized eigenvector approach; shift profile post-hoc if needed |
| PDE solver is complex (WENO + primitive recovery) | Large implementation effort; potential for subtle bugs | Start with simpler spatial reconstruction; validate against ODE steady-state |
| Conformal fluid comparison (Fig 2, green) requires separate model | Cannot reproduce green curves | Mark as optional; focus on black (ideal gas) curves |
| Stiff cases (small tau_hat) may require implicit methods | Explicit methods may be prohibitively slow or unstable | Use very small CFL; accept longer runtimes; focus on non-stiff cases first |
| Mathematica performance for large PDE grids | Slow execution at N = 2^13 | Use compiled functions; start with lower resolutions; profile and optimize |

---

## 8. Summary Checklist

- [ ] EOS module implemented and verified
- [ ] Transport coefficient module implemented and verified
- [ ] Characteristic speed module implemented and verified
- [ ] RK4 solver implemented
- [ ] Fig 1 reproduced and validated (cycle-fig1)
- [ ] Fig 2 reproduced and validated (cycle-fig2)
- [ ] ODE convergence (Table III) reproduced
- [ ] PDE solver implemented (conservative FV + WENO + Heun)
- [ ] Fig 3 reproduced and validated (cycle-fig3)
- [ ] Fig 5 reproduced and validated (cycle-fig5)
- [ ] Fig 4 reproduced and validated (cycle-fig4)
- [ ] Fig 6 reproduced and validated (cycle-fig6)
- [ ] Fig 7 reproduced and validated (cycle-fig7)
- [ ] All 7 figures PASS validation
