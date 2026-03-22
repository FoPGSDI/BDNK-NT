# Plan: Numerical Implementations Documentation

## Purpose
Document every numerical method and implementation detail described in the paper (primarily Appendix B / Sec. "Numerical algorithms and convergence tests", lines 1433-1458 of paper.tex) and scattered throughout the results sections, so that a reader could reproduce all computations from the documentation alone.

---

## 1. ODE Integration Methods

### 1.1 General Method: Fourth-Order Explicit Runge-Kutta (RK4)
- State that ALL ODE integrations use the classical RK4 method (paper line 1434).
- Write out the standard RK4 tableau (Butcher tableau or the familiar k1,k2,k3,k4 form).
- Clarify what "resolution N" means for an ODE: N gridpoints in the independent variable (tau for Bjorken, x for shockwave), with uniform spacing h = (domain_end - domain_start) / N.
- Resolution range: N = 2^9 to 2^13 (line 1434).

### 1.2 Bjorken Flow ODE (Eq 35 / line 795)
- **Equation to document:** The second-order ODE for epsilon(tau):
  ```
  tau_epsilon * ddot{epsilon} = -(1/tau)(tau + 2*tau_epsilon + tau_P) * dot{epsilon}
                                 - (1/tau^2)[rho*(tau + tau_P) - V]
  ```
- **Reduction to first-order system:** Introduce y1 = epsilon, y2 = dot{epsilon}, then:
  - dy1/dtau = y2
  - dy2/dtau = RHS(tau, y1, y2) from Eq 35
- **State variables:** (epsilon, dot{epsilon}) -- two-component ODE system in proper time tau.
- **Derivative computation:** All transport coefficients {tau_epsilon, tau_P, V} are functions of epsilon and n(tau) = n_0/tau (particle conservation is analytic). Document how rho = epsilon + P(epsilon, n) is computed from EOS (Eq 8, line 394).
- **Domain:** tau in [1, 20] (line 835).
- **Initial conditions:** epsilon(tau=1) = 0.25, dot{epsilon}(tau=1) in {-2, 0, 2}, n_0 = 0.1 (line 835-836).
- **Coordinate system:** Milne coordinates (tau, x, y, xi). Document metric g_ab = diag(-1,1,1,tau^2), Christoffel symbols (line 781-786).
- **Parameters:** Gamma=4/3, m=1, V_hat=1/10, sigma_hat=0, tau_hat in {0.5, 1, 2} (Table II, line 554).

### 1.3 Steady-State Shockwave ODEs (Eqs 37, 39-40 / lines 953-976)
- **System of three coupled first-order ODEs:**
  1. n'(x) from baryon conservation (Eq 37, line 953): n' = -W^2 * n * v' / v
  2. epsilon'(x) from Eq 39 (line 974): ratio of 4th-order polynomial in v over product of characteristic speed factors
  3. v'(x) from Eq 40 (line 975): ratio of 3rd-order polynomial in v over product of characteristic speed factors
- **State variables:** (n(x), epsilon(x), v(x)) -- three-component ODE system in spatial coordinate x.
- **Derivative computation:**
  - Document the numerator coefficients c0..c4 and d0..d4 (line 979-985).
  - Document the shared denominator structure involving characteristic speeds c_pm (Eq 38, line 969).
  - Note that T^{tx}, T^{xx} are constants computed from the left asymptotic state using perfect-fluid stress-energy tensor (lines 1000-1005).
  - Document how W = (1-v^2)^{-1/2} enters.
- **Boundary conditions (asymptotic states):**
  - Left state {epsilon_L, v_L, n_L} = {1, 0.8, 0.1} as x -> -infinity (line 995).
  - Integration proceeds from left to right.
- **Parameters:** Gamma=4/3, m=0.1, V_hat=2/15, sigma_hat=0, tau_hat=1.5 (Table II, line 555).
- **Singularity structure:** Note the denominators vanish when v = +/- c_pm or v = 0. Document that solutions only exist when numerators simultaneously vanish at these points, or when v never reaches these values (lines 989-1012).

---

## 2. PDE Solver

### 2.1 Overall Structure
- **Reference:** Conservative finite volume method of Pandya 2022 (cite [30] = Pandya:2022pif), line 1452.
- **Method of lines:** Spatial discretization produces a semi-discrete system dU/dt = L(U), then integrate in time.

### 2.2 Time Integration: Heun's Method (TVD-RK2)
- Document Heun's method as a two-stage total-variation-diminishing Runge-Kutta scheme:
  ```
  U* = U^n + dt * L(U^n)
  U^{n+1} = (1/2) U^n + (1/2)[U* + dt * L(U*)]
  ```
- This is second-order accurate in time.
- State that the overall scheme is second-order (line 1452: "second-order overall").

### 2.3 Spatial Discretization: WENO/CWENO
- Document that spatial reconstruction uses WENO (Weighted Essentially Non-Oscillatory) / CWENO (Central WENO) methods (line 1452).
- Note: "at most fourth-order convergent in grid spacing for smooth flows" (line 1452).
- The scheme is conservative: fluxes are computed at cell interfaces.
- Reference Pandya:2022pif for full algorithmic details.
- Note: the paper does not give the specific WENO stencil width or weights; refer reader to [30].

### 2.4 Conservative Formulation
- The BDNK equations are written in conservative form: nabla_a T^{ab} = 0, nabla_a J^a = 0.
- Document what the conserved variables are (components of T^{ab} and J^a) vs. the primitive variables (epsilon, n, u^a).
- Note: the BDNK stress-energy tensor contains second derivatives of primitives, making this a second-order PDE system, which is different from standard ideal hydro.

### 2.5 CFL Condition
- **Default CFL number:** lambda = Delta_t / Delta_x = 0.1 (line 1452).
- **Reduced CFL for stiff cases:** lambda = 0.01 for "stiff superluminal" and "wildly superluminal" solutions in Fig 5 (line 1452, also line 1127-1129).
- Document why stiffness arises: small tau_hat -> large characteristic speeds -> small tau_epsilon -> fast-decaying frame modes that must be resolved temporally.
- Explain the connection: the CFL condition requires Delta_t < lambda * Delta_x / c_max, so larger c_max (from smaller tau_hat) demands smaller timesteps.

---

## 3. Initial Conditions

### 3.1 Bjorken Flow
- **Coordinate system:** Milne (tau, x, y, xi).
- **Initial data (line 835-836):**
  - epsilon_0 = epsilon(tau=1) = 0.25
  - dot{epsilon}_0 = dot{epsilon}(tau=1) in {-2, 0, 2}
  - n_0 = 0.1 (so n(tau) = n_0/tau = 0.1/tau)
- **Velocity:** u^a = (1,0,0,0)^T everywhere, fixed by boost invariance (line 787).
- Document the inviscid solution (Eq 34, line 800) for comparison:
  epsilon(tau) = m*n_0*tau^{-1}[1 + e_0*tau^{-(Gamma-1)}]

### 3.2 Shockwave PDE Initial Data (Eq 46 / lines 1031-1037)
- **Error function interpolation:**
  ```
  epsilon(0,x) = (epsilon_R - epsilon_L)/2 * [erf(x/w) + 1] + epsilon_L
  v(0,x) = (v_L - v_R)/2 * [1 - erf(x/w)] + v_R
  n(0,x) = (n_L - n_R)/2 * [1 - erf(x/w)] + n_R
  ```
- **Width parameter:** w = 10 (line 1056).
- **Left states (freely specifiable):** Document the two cases:
  - Fig 4: {epsilon_L, v_L, n_L} = {1, 0.9, 1} (line 1049)
  - Fig 5: {epsilon_L, v_L, n_L} = {1, 0.6, 1} (line 1053)

### 3.3 Rankine-Hugoniot Conditions (Eq 47 / lines 1039-1045)
- **Three equations** determining right states from left states for a shockwave in its rest frame:
  ```
  n_L W_L v_L = n_R W_R v_R
  v_L W_L^2 rho_L = v_R W_R^2 rho_R
  v_L^2 W_L^2 rho_L + P_L = v_R^2 W_R^2 rho_R + P_R
  ```
- **Numerical solutions** (Eq 48, line 1049-1053):
  - {1, 0.9, 1}_L -> {11.5174, 0.354727, 5.44212}_R
  - {1, 0.6, 1}_L -> {1.33795, 0.514414, 1.25027}_R
- Document that these are solved numerically (nonlinear system of 3 equations in 3 unknowns: epsilon_R, v_R, n_R).
- Note: need EOS to evaluate P and rho from epsilon and n.

### 3.4 Shockwave Time Derivatives
- The BDNK PDEs are second-order in time, so initial time derivatives are needed.
- Document how dot{epsilon}(0,x) and dot{v}(0,x) are specified (or computed from the spatial profile via the constraint equations).
- Note: the paper uses the spatial profile Eq 46 which approximates a steady-state shock, so initial time derivatives should be small.

### 3.5 Heat Flow Initial Data (Eq 53 / lines 1217-1220)
- **Gaussian temperature profile at constant pressure:**
  ```
  T(0,x) = A * exp(-x^2/w^2) + delta
  P(0,x) = P_0 = const
  ```
- **Conversion to primitive variables:** epsilon and n are computed from T, P via:
  - epsilon = P[m/T + 1/(Gamma-1)]
  - n = P/T
  (derived from EOS, Eq 8)
- **Time-symmetric initial data (line 1220):**
  - dot{epsilon}(0,x) = 0
  - dot{u}^i(0,x) = 0
- **Parameters:** Document A, delta, w, P_0 values (need to extract from Table II or figure captions).
- **Key physics:** Document that sigma_hat = 0 gives no dynamics (stationary solution), while sigma_hat > 0 gives dynamical heat flow (lines 1226-1234).

---

## 4. Boundary Conditions

### 4.1 Ghost Cell Treatment
- Document the ghost cell approach (mentioned at line 1452: "significant interaction with the ghost cell boundaries").
- Standard finite volume: extend the computational domain by a few ghost cells on each side.
- Ghost cell values are filled according to the boundary condition type.

### 4.2 Outflow Boundary Conditions
- For shockwave problems: outflow (copy/extrapolate) boundary conditions, since the solution has non-trivial asymptotic states at x -> +/- infinity.
- Document that boundary interaction degrades convergence from 2nd to between 1st and 2nd order (line 1452: "afterward, the solution converges at a rate between first and second order").

### 4.3 Boundary Condition for Heat Flow
- For heat flow problems: document the boundary type (likely outflow or periodic).
- Note from convergence plot description (Fig 8, line 1457): transients propagate away and interact with boundaries at t ~ 80 (shockwave) and t ~ 150 (heat flow).

### 4.4 ODE "Boundary Conditions"
- Bjorken: initial value problem in tau, so "boundary condition" is the initial state at tau = 1.
- Shockwave ODE: boundary value problem with asymptotic states at x -> -infinity; integration starts from left state.

---

## 5. Convergence Testing

### 5.1 Convergence Factor Definition (Eq A1 / line 1436)
- **Q_N = ||R_{N/2}|| / ||R_N||** where:
  - R_N is a discrete residual evaluated on the numerical solution at resolution N.
  - ||.|| is the 1-norm (explicitly stated, line 1437).
  - The residual should be identically zero for exact solutions to the continuum equations.

### 5.2 Independent Residual Computation
- **Key point:** The residual R_N is computed using an INDEPENDENT discretization, not the same one used to evolve the equations. This avoids the trivial result that the evolution scheme's own residual is always zero by construction.
- **ODE residuals (Table III):**
  - Bjorken: fourth-order centered finite difference discretization of Eq 35 (line 1449).
  - Shockwave ODE: fourth-order centered finite difference discretization of T^{tx}_{,x} = 0 (line 1449).
- **PDE residuals (Fig 8):**
  - Second-order Crank-Nicolson discretization of the t-component of nabla_a T^{ab} = 0 (line 1457).

### 5.3 Expected Convergence Rates
- **ODE (RK4):** Q_N -> 16 as N -> infinity (fourth-order, since 2^4 = 16 for halving the grid spacing).
  - Document the convergence results from Table III (line 1441-1450):
    - Bjorken tau_hat=0.5: Q = 34.8, 18.7, 16.9
    - Bjorken tau_hat=1: Q = 18.4, 16.9, 16.3
    - Bjorken tau_hat=2: Q = 16.9, 16.3, 16.1
    - Shockwave: Q = 15.9, 15.9, 15.9
  - Note: stiff cases (small tau_hat) converge more slowly but still approach 16.
- **PDE (Heun + WENO/CWENO):** Q_N -> 4 as N -> infinity (second-order, since 2^2 = 4).
  - Document from Fig 8 caption: Q_N ~ 4 near t=0, degrades to between 1st and 2nd order after boundary interaction.
  - Note: spatial discretization is up to 4th order for smooth flows, but time integration limits to 2nd order overall.

### 5.4 Richardson Expansion Connection
- Briefly explain how Q_N -> 2^p follows from the Richardson expansion for a p-th order scheme with grid spacing halved between successive resolutions (line 1438).

---

## 6. Practical Considerations

### 6.1 Stiffness Issues with Small tau_hat
- **Source of stiffness:** Small tau_hat (proportional to tau_epsilon) makes the relaxation timescale tau_epsilon very short compared to the dynamical timescale. The ODE/PDE then has widely separated timescales (line 854-856, 1125-1131).
- **Manifestation in Bjorken flow:** "stiff ODE, requiring very small steps in tau to still resolve the decay time tau_epsilon" (line 855-856).
- **Manifestation in shockwaves:** tau_hat = 0.4 (c+ ~ 1.6) requires CFL = 0.01, an order of magnitude smaller than tau_hat = 0.5 (c+ ~ 1.5) which uses CFL = 0.1 (line 1127-1129).
- **Physical origin:** Decreasing tau_hat increases characteristic speeds c_pm, which increases the maximum signal speed and tightens the CFL constraint.
- **Recommendation:** Document that explicit time integrators become impractical for very small tau_hat; an implicit or IMEX scheme might be needed for production use.

### 6.2 Coordinate Systems
- **Cartesian (t, x, y, z):** Used for shockwave and heat flow problems. Minkowski metric eta_ab = diag(-1,1,1,1).
- **Milne (tau, x, y, xi):** Used for Bjorken flow. Metric g_ab = diag(-1,1,1,tau^2). Document Christoffel symbols (line 784-786).
- **Relationship:** tau = sqrt(t^2 - z^2), xi = arctanh(z/t) (line 779).
- **Why Milne for Bjorken:** PDEs reduce to a single ODE in Milne coordinates due to boost invariance (line 779).

### 6.3 Parameter Tables
- **Table II (line 550-562):** Maps figure numbers to parameter values {Gamma, m, V_hat, sigma_hat, tau_hat}.
- Document every entry and how these dimensionless parameters map to the actual transport coefficients via Eq 26 (line 464-468):
  - eta = rho * c_s^2 * L * eta_hat
  - zeta = rho * c_s^2 * L * zeta_hat
  - sigma = (V_hat * L * rho * c_s^2 / (-kappa_epsilon)) * sigma_hat
  - tau_epsilon = tau_Q = L * V_hat * tau_hat
  - tau_P = 2*(Gamma-1)*L*V_hat
- Note: L = 1 throughout (line 487).
- Document how V_hat acts as an inverse Reynolds number (Eq 28, line 474).

### 6.4 Computed Quantities for Diagnostics
- **Characteristic speeds c_pm, c_1:** Eqs A8-A9 (lines 1424-1431). These are monitored to check causality.
- **Inviscid Bjorken solution:** Eq 34 (line 800) for comparison.
- **Temperature in different frames:** BDNK frame T vs. Eckart frame T_E (lines 915-921).
- **Convergence factor Q_N:** Eq A1 (line 1436).

---

## 7. Connection to GitHub Repository

### 7.1 Repository Information
- **URL:** https://github.com/FoPGSDI/BDNK-NT
- **Branch:** BDNK-hydro-sim
- **Also referenced:** Mathematica notebook for frame constraints at https://github.com/aapandy2/BDNK_frame_constraints (line 1360).

### 7.2 Expected Code Structure
- Document the expected mapping between paper sections and code modules:
  - **EOS module:** Implements Eq 8 (gamma-law EOS), including P(epsilon,n), T(epsilon,n), mu(epsilon,n), c_s^2, and all thermodynamic derivatives (kappa_epsilon, kappa_n, etc.).
  - **Transport coefficients module:** Implements the hydrodynamic frame (Eq 26), computing {tau_epsilon, tau_P, tau_Q, eta, zeta, sigma, beta_epsilon, beta_n} from the dimensionless parameters and local state.
  - **Flux computation:** Computes T^{ab} and J^a from primitives and their gradients (Eqs 4-10).
  - **ODE solver:** RK4 integrator for Bjorken (Eq 35) and shockwave (Eqs 37, 39-40) problems.
  - **PDE solver:** Conservative finite volume with WENO/CWENO reconstruction and Heun time integration.
  - **Initial data module:** Implements Eqs 46, 47, 53 for shockwave and heat flow initial conditions.
  - **Diagnostics:** Convergence factor Q_N, independent residual computation, characteristic speed monitoring.

### 7.3 Pandya 2022 Reference
- The PDE solver is described in detail in Pandya:2022pif (Ref [30]).
- Document that the full algorithmic details (WENO stencil, flux splitting, primitive recovery, etc.) are in that reference, not repeated in this paper.

---

## 8. Documentation Structure Plan

The final numerical-implementations.md should be organized as follows:

```
# Numerical Methods and Implementation Details

## 1. Overview
   - Summary of two classes of problems: ODEs and PDEs
   - Software references (GitHub repos)

## 2. Equation of State and Thermodynamics
   - Gamma-law EOS and all derived quantities
   - Transport coefficient computation from dimensionless parameters
   - Parameter table (reproduction of Table II)

## 3. ODE Problems
   ### 3.1 Bjorken Flow
   - Governing equation (Eq 35)
   - Reduction to first-order system
   - Initial conditions and domain
   - Milne coordinate details
   ### 3.2 Steady-State Shockwave
   - Governing equations (Eqs 37, 39-40)
   - Numerator/denominator coefficients
   - Asymptotic states and singularity structure
   ### 3.3 RK4 Integration
   - Method description
   - Resolution and convergence

## 4. PDE Solver
   ### 4.1 Conservative Formulation
   ### 4.2 Spatial Discretization (WENO/CWENO)
   ### 4.3 Time Integration (Heun's Method / TVD-RK2)
   ### 4.4 CFL Condition and Stiffness

## 5. Initial and Boundary Conditions
   ### 5.1 Shockwave Initial Data (Eq 46)
   ### 5.2 Rankine-Hugoniot Conditions (Eq 47)
   ### 5.3 Heat Flow Initial Data (Eq 53)
   ### 5.4 Ghost Cells and Boundary Treatment

## 6. Convergence Testing
   ### 6.1 Convergence Factor Q_N (Eq A1)
   ### 6.2 Independent Residual Discretizations
   ### 6.3 ODE Convergence Results (Table III)
   ### 6.4 PDE Convergence Results (Fig 8)

## 7. Practical Considerations
   ### 7.1 Stiffness and CFL Restrictions
   ### 7.2 Coordinate Systems
   ### 7.3 Diagnostic Quantities
```

---

## 9. Key Equations to Reproduce Verbatim

The following equations from the paper must be reproduced exactly (with full notation) in the documentation:

| Paper Ref | Content | Line(s) |
|-----------|---------|---------|
| Eq 8 | Gamma-law EOS | 394 |
| Eq 26 | Hydrodynamic frame definitions | 464-468 |
| Eq 27-28 | Combined viscosity V and V_hat | 473-474 |
| Eq 34 | Inviscid Bjorken solution | 800 |
| Eq 35 | Bjorken flow ODE | 795 |
| Eq 37 | Shockwave n'(x) | 953 |
| Eq 38 | Characteristic speeds c_pm (general) | 969 |
| Eq 39 | Shockwave epsilon'(x) | 974 |
| Eq 40 | Shockwave v'(x) | 975 |
| Eq 46 | Shockwave initial data (erf) | 1031-1037 |
| Eq 47 | Rankine-Hugoniot conditions | 1039-1045 |
| Eq 48 | Numerical R-H solutions | 1049-1053 |
| Eq 53 | Heat flow initial data | 1217-1218 |
| Eq A1 | Convergence factor Q_N | 1436 |
| Eq A8 | Characteristic speeds c_pm^2 | 1424-1427 |
| Eq A9 | Characteristic speed c_1^2 | 1429 |
| Table II | Parameter values | 550-562 |
| Table III | ODE convergence results | 1441-1450 |

---

## 10. Open Questions / Items Requiring Clarification

1. **WENO/CWENO details:** The paper does not specify the WENO order, stencil width, smoothness indicators, or whether it is component-wise or characteristic-wise. All of this is in Pandya:2022pif -- do we summarize or just cite?
2. **Primitive recovery:** For the conservative finite volume method, how are primitive variables (epsilon, n, u^a) recovered from conserved variables? This is non-trivial for BDNK since T^{ab} contains gradients of primitives.
3. **Shockwave ODE initial guess:** How is the ODE integration for the steady-state shockwave started? The left state is at x -> -infinity; in practice one must start at some finite x and perturb slightly off the asymptotic state.
4. **Heat flow parameters A, delta, w, P_0:** The specific values of the Gaussian amplitude, offset, width, and constant pressure in Eq 53 are not given in the text or Table II -- they may only be in the code.
5. **Time derivative initial data for PDE:** The BDNK system is second-order in time. For shockwave PDE initial data, how are initial time derivatives specified? The paper says time-symmetric for heat flow (dot{epsilon}=0, dot{u}^i=0) but is less explicit for shockwaves.
6. **Domain size and grid:** The computational domain extents (x_min, x_max) and number of grid points for PDE runs are not always explicitly stated.
