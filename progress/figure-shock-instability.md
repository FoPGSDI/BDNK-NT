# Figure Analysis: shock_instability.pdf

**Figure reference:** Fig. 3 (`\ref{fig:shock_instability}`) in the paper, Sec. III.C (lines 1055--1094 of `paper.tex`).

---

## 1. Visual Description

The figure consists of two vertically stacked panels, each showing the spatial profile of the fluid three-velocity v(t, x) at a single time snapshot for a dynamically evolving BDNK shockwave.

### Top panel (unstable case, tau_hat = 3)

- The velocity profile is plotted at time t = 27.
- On the far left (x << 0), v sits at the upstream asymptotic value v_L = 0.9. Moving rightward, the profile transitions downward through the shock front near x = 0, where a violent, high-frequency oscillatory instability is visible. The instability manifests as rapid, grid-scale oscillations in v around the shock transition region.
- A horizontal dotted line marks the maximum characteristic speed c_+ of the BDNK system. In this panel c_+ is approximately 0.75, well below the upstream velocity v_L = 0.9. The entire upstream plateau (v ~ 0.9) therefore lies above c_+, satisfying the condition v > c_+ that triggers the instability.
- An inset (zoom box) is provided, magnifying the region of the velocity profile where the instability is most pronounced. The inset shows three overlapping curves at different resolutions (N = 2^9, 2^10, 2^11), displayed with progressively darker shading. The oscillations do not converge away with increasing resolution; instead they persist and sharpen, confirming that this is a genuine instability rather than a transient numerical artifact.
- To the right of the shock front (x > 0), a smooth "bump" feature propagates downstream at roughly the sound speed. This bump is sourced by the portion of the initial data that deviates from the exact stationary shockwave profile.

### Bottom panel (stable case, tau_hat = 1.5)

- The velocity profile is plotted at a much later time, t = 372, demonstrating long-term stability.
- The profile smoothly transitions from v_L = 0.9 on the left to v_R ~ 0.35 on the right through a well-resolved, monotonic shock front near x = 0, with no sign of oscillation or instability.
- The horizontal dotted line marks c_+, which in this case is approximately 0.94 -- above the upstream velocity v_L = 0.9. Since v < c_+ everywhere in the domain, the condition for instability is never met.
- Three resolution levels (N = 2^9, 2^10, 2^11) are again shown but are indistinguishable from one another, indicating clean convergence to the steady-state shockwave solution.
- The legend in this panel labels the three resolutions: N = 2^9 (lightest gray), N = 2^10 (medium gray), N = 2^11 (darkest/black).

---

## 2. Axes and Labels

| Axis | Quantity | Range (approx.) |
|------|----------|-----------------|
| Horizontal (both panels) | Spatial coordinate x | [-50, 50] |
| Vertical (top panel) | Fluid three-velocity v | [0.5, 0.9] approximately |
| Vertical (bottom panel) | Fluid three-velocity v | [0.3, 1.0] approximately |

- The top-right corner of each panel displays the time stamp: "t = 27" (top) and "t = 372" (bottom).
- Each panel also displays the frame parameter: "tau_hat = 3" (top) and "tau_hat = 1.5" (bottom).

---

## 3. Line Styles

- **Solid lines with varying darkness (gray to black):** The flow velocity v(t, x) at three different numerical resolutions. Lighter gray corresponds to coarser resolution (N = 2^9 = 512 grid points), medium gray to intermediate resolution (N = 2^10 = 1024), and darkest/black to the finest resolution (N = 2^11 = 2048). The use of increasing darkness with resolution makes it easy to see whether solutions converge (bottom panel) or diverge (top panel inset).

- **Dotted line (thick, horizontal):** The maximum characteristic speed c_+ of the BDNK system. This is a single horizontal line because c_+ depends on the local thermodynamic state, and for these flow conditions it is approximately constant across the domain. Its value changes between panels because changing tau_hat alters the characteristic speeds:
  - Top panel (tau_hat = 3): c_+ ~ 0.75
  - Bottom panel (tau_hat = 1.5): c_+ ~ 0.94

---

## 4. Key Observations

### The instability criterion: v > c_+

The central message of the figure is the sharp dichotomy between the two panels:

1. **When v > c_+ (top panel):** The upstream flow velocity (v_L = 0.9) exceeds the maximum characteristic speed of the BDNK system (c_+ ~ 0.75 for tau_hat = 3). In this regime, a high-frequency numerical instability develops at the shock front. The instability:
   - Grows rapidly (already visible at t = 27).
   - Does not converge away with increasing resolution -- the inset shows all three resolutions exhibiting comparable-amplitude oscillations, with the oscillation frequency increasing with resolution (grid-scale behavior).
   - Is localized to the region where v crosses or exceeds c_+.

2. **When v < c_+ everywhere (bottom panel):** With tau_hat = 1.5, the maximum characteristic speed c_+ ~ 0.94 exceeds v_L = 0.9 everywhere. The evolution remains stable to very late times (t = 372, more than an order of magnitude later than the unstable case). The solution converges cleanly across all three resolutions to what appears to be the steady-state shockwave profile obtained from the ODEs.

### Downstream propagating feature

In the top panel, a smooth bump is visible to the right of the shock front (near x ~ 10-20). This feature arises from the part of the error-function initial data that does not exactly match the true stationary shockwave profile. It propagates downstream at approximately the sound speed. This same feature forms in the stable case as well but has propagated out of the domain by t = 372.

---

## 5. Numerical and Implementation Notes

### Initial data (Eq. 46 / shockwave_ID)

The initial conditions are smooth error-function profiles that interpolate between asymptotic left and right states:

- epsilon(0, x) = (epsilon_R - epsilon_L)/2 * [erf(x/w) + 1] + epsilon_L
- v(0, x) = (v_L - v_R)/2 * [1 - erf(x/w)] + v_R
- n(0, x) = (n_L - n_R)/2 * [1 - erf(x/w)] + n_R

The transition width is w = 10.

### Rankine-Hugoniot pairs (Eq. 47 / shockwave_params)

The left and right states are connected by the relativistic Rankine-Hugoniot jump conditions for a stationary shockwave:

- n_L W_L v_L = n_R W_R v_R (baryon flux conservation)
- v_L W_L^2 rho_L = v_R W_R^2 rho_R (energy flux conservation)
- v_L^2 W_L^2 rho_L + P_L = v_R^2 W_R^2 rho_R + P_R (momentum flux conservation)

where W_i = (1 - v_i^2)^{-1/2} and rho_i = epsilon_i + P_i.

For this figure, the left state {epsilon, v, n}_L = {1, 0.9, 1} yields the right state {epsilon, v, n}_R = {11.5174, 0.354727, 5.44212}. This is a strong shock with a large velocity jump (from 0.9 down to ~0.35).

### Transition width

w = 10 sets the spatial scale over which the initial error-function profiles transition between left and right states.

### Numerical method

The BDNK PDEs are integrated using fourth-order explicit Runge-Kutta (RK4). The resolutions shown are N = 2^9 (512), 2^10 (1024), and 2^11 (2048) grid points across the computational domain.

---

## 6. Connection to Theory

### Steady-state shockwave ODEs and their solvability

The key theoretical connection is between the *existence of steady-state shockwave solutions* (governed by the coupled ODEs for epsilon'(x) and v'(x)) and the *dynamical stability of time-dependent shockwave evolution*.

The steady-state shockwave ODEs have denominators proportional to (v - c_+)(v + c_+)(v - c_-)(v + c_-). When the velocity profile of the shockwave must pass through v = c_+ to connect the left and right asymptotic states, the ODE system becomes singular -- the denominators vanish, and no smooth steady-state solution exists.

- **tau_hat = 3 (top panel):** c_+ ~ 0.75 < v_L = 0.9, so the velocity profile must cross c_+ somewhere in the transition region. The steady-state ODEs have no solution. Correspondingly, the dynamical evolution develops a high-frequency instability.

- **tau_hat = 1.5 (bottom panel):** c_+ ~ 0.94 > v_L = 0.9, so the velocity profile remains below c_+ throughout the entire shock transition. The steady-state ODEs admit a smooth solution. Correspondingly, the dynamical evolution is stable and asymptotes to this steady-state solution at late times.

### Rigorous mathematical support

This intuition -- that the existence of the corresponding steady-state solution is necessary for dynamical stability -- is consistent with a rigorous result by Freistuhler (2021) for conformal BDNK fluids. That work showed that a hydrodynamic frame will always produce shockwave solutions that break down unless the maximum local characteristic speed is greater than or equal to the speed of light. The present figure extends this observation beyond the conformal case to BDNK fluids with ideal gas microphysics, demonstrating that the same mechanism (v crossing c_+) triggers the same type of instability.

### Role of c_- crossings

The paper also notes (lines 1078--1088) that one could ask whether crossing the other characteristic speed c_- causes similar problems. For the hydrodynamic frame used here, the authors find empirically that crossing c_- requires severely violating both the causality and linear stability constraints, making it difficult to disentangle the source of instability in those cases. This is left to future work.

---

## 7. Parameters

All parameters for this figure are taken from Table I of the paper (line 556):

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Adiabatic index | Gamma | 4/3 |
| Particle mass | m | 0.1 |
| Frame viscosity parameter | V_hat | 4/3 |
| Thermal conductivity parameter | sigma_hat | 0 |
| Frame relaxation parameter (top panel) | tau_hat | 3 |
| Frame relaxation parameter (bottom panel) | tau_hat | 1.5 |

### Derived quantities

- **Equation of state:** Relativistic ideal gas (gamma-law), P = (Gamma - 1) * m * n * e, with specific internal energy e = epsilon/(m*n) - 1.
- **Hydrodynamic frame:** The one-parameter family defined in Eq. (21) of the paper, where tau_epsilon = tau_Q = L * V_hat * tau_hat and tau_P = 2*(Gamma - 1)*L*V_hat. Here tau_hat is the single free parameter controlling the characteristic speeds.
- **Characteristic speeds:** Given by Eq. (A9) in the Appendix. For sigma_hat = 0 and the thermodynamic states in this problem:
  - tau_hat = 1.5 yields c_+ ~ 0.94 (subluminal, above v_L = 0.9)
  - tau_hat = 3 yields c_+ ~ 0.75 (subluminal, below v_L = 0.9)
- **Rankine-Hugoniot data:** Left state {epsilon, v, n} = {1, 0.9, 1}, right state = {11.5174, 0.354727, 5.44212}.
- **Transition width:** w = 10.
- **Resolutions:** N = 2^9, 2^10, 2^11 grid points.

---

## Summary

This figure provides the clearest demonstration in the paper of the connection between the choice of hydrodynamic frame (via tau_hat) and the dynamical stability of shockwave solutions in BDNK theory. The critical condition is whether the flow velocity anywhere exceeds c_+, the maximum characteristic speed of the system. When it does, the steady-state shockwave ODEs become singular (no smooth solution exists), and the time-dependent evolution develops a non-convergent, high-frequency instability. When c_+ > v everywhere, the evolution is stable and converges to the steady-state profile. The choice of hydrodynamic frame -- specifically the relaxation parameter tau_hat -- directly controls c_+ and therefore determines whether a given shockwave configuration is stable or unstable.
