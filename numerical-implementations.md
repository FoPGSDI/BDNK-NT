# Numerical Methods and Implementation Details

## Reference

All content derives from: Pandya, Most, Pretorius, "Causal, stable first-order viscous relativistic hydrodynamics with ideal gas microphysics" (paper.tex), with primary numerical details drawn from the paper's Appendix B (ref: paper Sec. B) and scattered throughout Secs. III.B--III.D. The PDE solver is described in detail in Pandya 2022 (Ref. [30], Pandya:2022pif).

**Software references:**
- Main numerical code: [BDNK-NT](https://github.com/FoPGSDI/BDNK-NT), branch `BDNK-hydro-sim`
- Frame constraint derivations: [BDNK_frame_constraints](https://github.com/aapandy2/BDNK_frame_constraints) (Mathematica notebook)

---

## 1. Overview

[SOLID] The paper employs two distinct classes of numerical methods:

1. **ODE integrations** (fourth-order explicit Runge-Kutta, RK4): used for (0+1)D Bjorken flow and steady-state shockwave profile computations. These are the simpler problems from a computational perspective, but stiffness can arise for small relaxation times.

2. **PDE solver** (conservative finite volume with WENO/CWENO reconstruction and Heun time integration): used for dynamical (1+1)D shockwave formation and heat flow problems. The scheme is second-order overall and is described in detail in Pandya:2022pif.

The two classes of problems serve complementary roles: ODE solutions provide reference solutions and steady-state profiles, while PDE evolutions capture the full dynamics including transient behavior, stability properties, and approach to equilibrium.

---

## 2. Equation of State and Thermodynamics

### 2.1 Gamma-Law EOS

[SOLID] The equation of state is the relativistic ideal gas (ref: paper Eq. 25):

<a id="eq:EOS"></a>
$$
P(\epsilon, n) = [\Gamma - 1]\, m n\, e(\epsilon, n) = n\, T(\epsilon, n)
$$

where $\Gamma \in (1,2)$ is the adiabatic index, and the specific internal energy $e$ is related to the total energy density by (ref: paper Eq. 26):

$$
\epsilon = m n (1 + e).
$$

From these, the key thermodynamic quantities needed by the numerical code are:

$$
\begin{aligned}
P &= (\Gamma - 1)(\epsilon - mn) \\
T &= P / n = (\Gamma - 1)(\epsilon/n - m) \\
\rho &\equiv \epsilon + P = \Gamma \epsilon - (\Gamma - 1) m n \\
c_s^2 &= \Gamma P / \rho
\end{aligned}
$$

and the microphysics-derived quantities (ref: paper Eqs. 31--38):

$$
\begin{aligned}
p'_\epsilon &= \Gamma - 1, \quad p'_n = -(\Gamma - 1) m \\
\kappa_\epsilon &= -(\Gamma - 1) \frac{\epsilon \rho^2}{n^2 P}, \quad \kappa_n = \frac{\rho}{n^2 P}\left[(\Gamma - 1)\epsilon^2 + P^2\right] \\
\kappa_s &= \kappa_\epsilon + \kappa_n = -(\Gamma - 1) m \frac{\rho}{n}
\end{aligned}
$$

with the dimensionless ratios:

$$
\alpha \equiv \frac{p'_\epsilon}{c_s^2} = \frac{\Gamma - 1}{c_s^2}, \quad \omega \equiv \frac{\kappa_s}{\kappa_\epsilon} = \frac{m n P}{\epsilon \rho}.
$$

### 2.2 Transport Coefficient Computation

[SOLID] The hydrodynamic frame (ref: paper Eq. 41) defines all six independent transport coefficients from five dimensionless parameters ($\hat{\eta}, \hat{\zeta}, \hat{\sigma}, \hat{\tau}$, and the lengthscale $L$):

<a id="eq:hydro_frame"></a>
$$
\begin{aligned}
&\eta = \rho c_s^2 L\, \hat{\eta}, \quad \zeta = \rho c_s^2 L\, \hat{\zeta}, \quad \sigma = \frac{\hat{V}\, L\, \rho c_s^2}{(-\kappa_\epsilon)}\, \hat{\sigma} \\
&\tau_\epsilon = \tau_Q = L \hat{V}\, \hat{\tau}, \quad \tau_P = 2(\Gamma - 1) L \hat{V}
\end{aligned}
$$

where the combined viscosity and its dimensionless counterpart are (ref: paper Eqs. 42--43):

$$
V \equiv \frac{4\eta}{3} + \zeta, \quad \hat{V} \equiv \frac{V}{\rho c_s^2 L} = \frac{4\hat{\eta}/3 + \hat{\zeta}}{1}.
$$

The derived coefficients $\beta_\epsilon, \beta_n$ are then computed from (ref: paper Eqs. 18--19):

$$
\begin{aligned}
\beta_\epsilon &= (\Gamma - 1)\tau_Q - (\Gamma - 1)\frac{\sigma \epsilon \rho}{n^2 P} \\
\beta_n &= -(\Gamma - 1) m\, \tau_Q + \frac{\sigma \rho}{n^3 P}\left[(\Gamma - 1)\epsilon^2 + P^2\right]
\end{aligned}
$$

**Implementation note:** $L = 1$ throughout the paper (ref: paper line 487). For this EOS/frame, $\tau_\epsilon = \hat{V}\hat{\tau}$, $\tau_P = 2(\Gamma-1)\hat{V}$, and $\tau_Q = \hat{V}\hat{\tau}$ are **constants** (they do not depend on the local state). The transport coefficients $V, \sigma, \beta_\epsilon, \beta_n$, however, depend on the local state $(\epsilon, n)$ through $\rho, c_s^2, \kappa_\epsilon$, etc., and must be recomputed at each step during integration.

### 2.3 Parameter Table

[SOLID] **Table II** (ref: paper Table II) summarizes all dimensionless parameters used in each numerical test. Note that $\hat{\eta}$ and $\hat{\zeta}$ do not appear individually in the table because only the combination $\hat{V} = 4\hat{\eta}/3 + \hat{\zeta}$ enters the equations of motion for the highly symmetric test problems considered.

| Figure | $\Gamma$ | $m$ | $\hat{V}$ | $\hat{\sigma}$ | $\hat{\tau}$ |
|--------|----------|-----|-----------|----------------|-------------|
| Fig. 1 (Bjorken) | $4/3$ | $1$ | $1/10$ | $0$ | $0.5,\; 1,\; 2$ |
| Fig. 2 (Shockwave profile) | $4/3$ | $0.1$ | $2/15$ | $0$ | $1.5$ |
| Fig. 3 (Shock instability) | $4/3$ | $0.1$ | $4/3$ | $0$ | $1.5,\; 3$ |
| Fig. 4 (Acausal instability) | $4/3$ | $0.1$ | $4/3$ | $0$ | $0.25,\; 0.4,\; 0.5,\; 1.5$ |
| Fig. 5 (Heat stationary) | $4/3$ | $0.1$ | $2/15$ | $0,\; 1/3$ | $1.5$ |
| Fig. 6 (Telegrapher's) | $4/3$ | $0.1$ | $2/15$ | $0.15,\; 1.5,\; 7.5$ | $1.5,\; 15,\; 75$ |

**Recipe to go from table parameters to transport coefficients:**

Given a local state $(\epsilon, n)$ and a row from the table:

1. Compute $P = (\Gamma - 1)(\epsilon - mn)$, $\rho = \epsilon + P$, $c_s^2 = \Gamma P / \rho$.
2. Compute $\kappa_\epsilon = -(\Gamma-1)\epsilon\rho^2/(n^2 P)$.
3. Set $V = \hat{V}\, \rho c_s^2$ (since $L = 1$).
4. Set $\tau_\epsilon = \tau_Q = \hat{V}\, \hat{\tau}$, $\tau_P = 2(\Gamma-1)\hat{V}$.
5. Set $\sigma = \hat{V}\, \rho c_s^2\, \hat{\sigma} / (-\kappa_\epsilon)$.
6. Compute $\beta_\epsilon, \beta_n$ from the formulas above.

Note that $\hat{\eta}, \hat{\zeta}$ are individually undetermined by the table; only their combination $\hat{V}$ is specified. For problems where shear and bulk viscosity appear only through $V$, this suffices. The characteristic speed $c_1^2 = c_s^2\, \eta/(V\hat{\tau})$ does require $\eta$ individually, but does not affect the dynamics in these test problems.

---

## 3. ODE Problems

### 3.1 Bjorken Flow

#### 3.1.1 Coordinate System

[SOLID] Bjorken flow is studied in Milne coordinates $x^a = (\tau, x, y, \xi)^T$ (ref: paper Sec. III.B), where:

$$
\tau \equiv \sqrt{t^2 - z^2}, \quad \xi \equiv \text{arctanh}(z/t).
$$

The metric is:

$$
g_{ab} = \text{diag}(-1, 1, 1, \tau^2),
$$

with nonzero Christoffel symbols:

$$
\Gamma^\xi_{\tau\xi} = \Gamma^\xi_{\xi\tau} = \frac{1}{\tau}, \quad \Gamma^\tau_{\xi\xi} = \tau,
$$

and metric determinant $\sqrt{|g|} = \tau$. Boost invariance requires $u^a = (1, 0, 0, 0)^T$ and all quantities depend only on $\tau$.

#### 3.1.2 Governing Equation

[SOLID] The particle current conservation law immediately gives (ref: paper Eq. 65):

$$
n(\tau) = \frac{n_0}{\tau},
$$

where $n_0$ is a constant. This is **analytic** and does not need to be evolved numerically.

The sole nontrivial equation of motion is the $\tau$-component of $\nabla_a T^{ab} = 0$ (ref: paper Eq. 66):

<a id="eq:Bjorken_EOM"></a>
$$
\tau_\epsilon\, \ddot{\epsilon} = -\frac{1}{\tau}(\tau + 2\tau_\epsilon + \tau_P)\, \dot{\epsilon} - \frac{1}{\tau^2}\left[\rho(\tau + \tau_P) - V\right]
$$

where $\dot{\epsilon} \equiv \partial_\tau \epsilon$, $\ddot{\epsilon} \equiv \partial_\tau^2 \epsilon$, and the transport coefficients $\{\tau_\epsilon, \tau_P, V\}$ are functions of $\epsilon$ and $n(\tau) = n_0/\tau$ through the frame definitions [Eq. (hydro_frame)](#eq:hydro_frame).

#### 3.1.3 Reduction to First-Order System

To apply RK4, Eq. 35 must be recast as a first-order system. Define the state vector:

$$
\mathbf{y} = \begin{pmatrix} y_1 \\ y_2 \end{pmatrix} = \begin{pmatrix} \epsilon \\ \dot{\epsilon} \end{pmatrix}.
$$

The first-order system is then:

$$
\frac{d\mathbf{y}}{d\tau} = \mathbf{f}(\tau, \mathbf{y}) = \begin{pmatrix} y_2 \\ \displaystyle\frac{1}{\tau_\epsilon}\left[-\frac{1}{\tau}(\tau + 2\tau_\epsilon + \tau_P)\, y_2 - \frac{1}{\tau^2}\left[\rho(\tau + \tau_P) - V\right]\right] \end{pmatrix}
$$

where at each evaluation of $\mathbf{f}$:
1. Set $n = n_0/\tau$.
2. Compute $P, \rho, c_s^2$ from the EOS using $\epsilon = y_1$ and $n$.
3. Compute $\tau_\epsilon, \tau_P, V$ from the frame definitions.
4. Evaluate the right-hand side.

**Pseudocode for the derivative function:**

```
function bjorken_rhs(tau, y):
    eps = y[0]
    eps_dot = y[1]

    n = n0 / tau
    P = (Gamma - 1) * (eps - m * n)
    rho = eps + P
    cs2 = Gamma * P / rho
    Vhat_local = Vhat   # constant dimensionless parameter
    V_local = Vhat_local * rho * cs2   # since L = 1
    tau_eps = Vhat_local * tau_hat
    tau_P = 2 * (Gamma - 1) * Vhat_local

    dy0 = eps_dot
    dy1 = (1/tau_eps) * ( -(1/tau) * (tau + 2*tau_eps + tau_P) * eps_dot
                          -(1/tau^2) * (rho * (tau + tau_P) - V_local) )
    return [dy0, dy1]
```

#### 3.1.4 Initial Conditions and Domain

[SOLID] (ref: paper lines 835--836):

- **Domain:** $\tau \in [1, 20]$
- **Initial energy density:** $\epsilon(\tau = 1) = \epsilon_0 = 0.25$
- **Initial energy density derivatives:** $\dot{\epsilon}(\tau = 1) \in \{-2, 0, 2\}$
- **Baryon number constant:** $n_0 = 0.1$

Three separate ODE integrations are performed for each value of $\hat{\tau}$, one per choice of $\dot{\epsilon}_0$.

#### 3.1.5 Inviscid Reference Solution

[SOLID] The inviscid (perfect fluid) solution (ref: paper Eq. 67) provides a reference for comparison:

$$
\epsilon(\tau) = m n_0 \tau^{-1}\left[1 + e_0\, \tau^{-(\Gamma - 1)}\right] \quad \text{(inviscid)},
$$

where $e_0$ is an integration constant determined by initial data.

### 3.2 Steady-State Shockwave

#### 3.2.1 Setup

[SOLID] For a planar shockwave in its rest frame in 4D Minkowski spacetime, the solution is time-independent and varies only in $x$. The four-velocity is parameterized by the three-velocity $v \in [0,1)$ as:

$$
u^a = (W, Wv, 0, 0)^T, \quad W \equiv (1 - v^2)^{-1/2}.
$$

#### 3.2.2 Governing Equations

[SOLID] The conservation laws reduce to three coupled first-order ODEs for $n(x), \epsilon(x), v(x)$.

**Baryon number conservation** (ref: paper Eq. 72):

<a id="eq:shockwave_nprime"></a>
$$
n' = -\frac{W^2 n\, v'}{v},
$$

which allows $n'$ to be eliminated in favor of $v'$.

**Energy-momentum conservation** (ref: paper Eqs. 76--77):

<a id="eq:shockwave_epsP"></a>
$$
\epsilon'(x) = \frac{c_4 v^4 + c_3 v^3 + c_2 v^2 + c_1 v + c_0}{A W v\, (v - c_+)(v + c_+)(v - c_-)(v + c_-)}
$$

<a id="eq:shockwave_velP"></a>
$$
v'(x) = \frac{d_3 v^3 + d_2 v^2 + d_1 v + d_0}{A W^3\, (v - c_+)(v + c_+)(v - c_-)(v + c_-)}
$$

where $c_\pm$ are the characteristic speeds (ref: paper Eq. 75):

$$
c_\pm^2 = \frac{-B \pm \sqrt{B^2 - 4AC}}{2A}
$$

with $A = \rho\, \tau_\epsilon\, \tau_Q$, $B$ and $C$ defined in (ref: paper Eqs. A2--A4).

#### 3.2.3 Numerator Coefficients

[SOLID] The coefficients in the numerator polynomials are (ref: paper Eq. 78):

$$
\begin{aligned}
c_0 &= \beta_n n\, (T^{xx} - P) \\
c_1 &= -T^{tx}(2\beta_n n - \rho\, \tau_P + V) \\
c_2 &= [\beta_n n - \rho(\tau_\epsilon + \tau_P + \tau_Q) + V](T^{xx} + \epsilon) + \rho^2(\tau_\epsilon + \tau_Q) \\
c_3 &= \rho\, T^{tx}(\tau_\epsilon + 2\tau_Q) \\
c_4 &= -\rho\, \tau_Q\, (T^{xx} + \epsilon)
\end{aligned}
$$

$$
\begin{aligned}
d_0 &= \beta_\epsilon\, (T^{xx} - P) \\
d_1 &= -T^{tx}(2\beta_\epsilon + \tau_P) \\
d_2 &= (T^{xx} + \epsilon)(\beta_\epsilon + \tau_\epsilon + \tau_P) - \rho\, \tau_\epsilon \\
d_3 &= -\tau_\epsilon\, T^{tx}
\end{aligned}
$$

#### 3.2.4 Conserved Quantities $T^{tx}, T^{xx}$

[SOLID] The quantities $T^{tx}$ and $T^{xx}$ are constants of the motion. They are computed from the asymptotic left state using the perfect fluid stress-energy tensor (ref: paper Eq. 3), since the asymptotic states are in thermodynamic equilibrium (ref: paper lines 1000--1005):

$$
T^{tx} = \rho_L W_L^2 v_L, \quad T^{xx} = \rho_L W_L^2 v_L^2 + P_L,
$$

where $\rho_L = \epsilon_L + P_L$ and $W_L = (1 - v_L^2)^{-1/2}$.

#### 3.2.5 State Vector and Integration

The state vector for the shockwave ODE is:

$$
\mathbf{y} = \begin{pmatrix} n \\ \epsilon \\ v \end{pmatrix}.
$$

The derivative function is:

```
function shockwave_rhs(x, y):
    n_loc, eps, v = y[0], y[1], y[2]
    W = 1 / sqrt(1 - v^2)

    # Compute thermodynamics and transport coefficients
    P = (Gamma - 1) * (eps - m * n_loc)
    rho = eps + P
    cs2 = Gamma * P / rho
    # ... compute tau_eps, tau_P, tau_Q, V, beta_eps, beta_n, sigma, kappa_eps ...

    # Compute characteristic speeds
    A = rho * tau_eps * tau_Q
    B = -tau_eps * (rho * cs2 * tau_Q + V + sigma * kappa_s) - rho * tau_P * tau_Q
    C = tau_P * (rho * cs2 * tau_Q + sigma * kappa_s) - beta_eps * V
    disc = sqrt(B^2 - 4*A*C)
    cp2 = (-B + disc) / (2*A)
    cm2 = (-B - disc) / (2*A)
    cp = sqrt(cp2)
    cm = sqrt(cm2)

    # Shared denominator
    denom_eps = A * W * v * (v - cp)*(v + cp)*(v - cm)*(v + cm)
    denom_v   = A * W^3 * (v - cp)*(v + cp)*(v - cm)*(v + cm)

    # Compute numerator coefficients c_i, d_i
    # ... (as given in Sec. 3.2.3) ...

    eps_prime = (c4*v^4 + c3*v^3 + c2*v^2 + c1*v + c0) / denom_eps
    v_prime   = (d3*v^3 + d2*v^2 + d1*v + d0) / denom_v
    n_prime   = -W^2 * n_loc * v_prime / v

    return [n_prime, eps_prime, v_prime]
```

#### 3.2.6 Asymptotic States and Parameters

[SOLID] (ref: paper lines 994--995):

- **Left asymptotic state** ($x \to -\infty$): $\{\epsilon_L, v_L, n_L\} = \{1, 0.8, 0.1\}$
- **Parameters:** $\Gamma = 4/3$, $m = 0.1$, $\hat{V} = 2/15$, $\hat{\sigma} = 0$, $\hat{\tau} = 1.5$ (Table II)

#### 3.2.7 Singularity Structure

[SOLID] The denominators in [Eqs. (39--40)](#eq:shockwave_epsP) vanish when $v = \pm c_\pm$ or $v = 0$. Solutions only exist when the velocity profile avoids these singular values, or when the numerators simultaneously vanish at those points. The paper verifies numerically that for the chosen parameters, $v$ never attains any of these singular values (ref: paper lines 1006--1012). When $v_L \geq c_+$, the solver finds only the trivial constant equilibrium state.

[PRELIMINARY] The paper does not specify precisely how the ODE integration is initialized at finite $x$ given that the left state is an asymptotic value at $x \to -\infty$. In practice, one starts at some large negative $x$ with a small perturbation away from the asymptotic state. The specific initialization procedure is not documented in the paper.

### 3.3 RK4 Integration

#### 3.3.1 Method Description

[SOLID] All ODE integrations use the classical fourth-order explicit Runge-Kutta method (ref: paper line 1434). For a system $\mathbf{y}' = \mathbf{f}(x, \mathbf{y})$ with step size $h$, the RK4 update is:

$$
\begin{aligned}
\mathbf{k}_1 &= h\, \mathbf{f}(x_n, \mathbf{y}_n) \\
\mathbf{k}_2 &= h\, \mathbf{f}(x_n + h/2, \mathbf{y}_n + \mathbf{k}_1/2) \\
\mathbf{k}_3 &= h\, \mathbf{f}(x_n + h/2, \mathbf{y}_n + \mathbf{k}_2/2) \\
\mathbf{k}_4 &= h\, \mathbf{f}(x_n + h, \mathbf{y}_n + \mathbf{k}_3) \\
\mathbf{y}_{n+1} &= \mathbf{y}_n + \frac{1}{6}(\mathbf{k}_1 + 2\mathbf{k}_2 + 2\mathbf{k}_3 + \mathbf{k}_4)
\end{aligned}
$$

This is a single-step, explicit method with local truncation error $O(h^5)$ and global error $O(h^4)$.

#### 3.3.2 Resolution and Step Size

[SOLID] Solutions are produced at resolutions ranging from $N = 2^9 = 512$ to $N = 2^{13} = 8192$ gridpoints (ref: paper line 1434). For Bjorken flow with domain $\tau \in [1, 20]$, the step size is:

$$
h = \frac{\tau_{\max} - \tau_{\min}}{N} = \frac{19}{N}.
$$

For the shockwave ODE, the step size is $h = (x_{\max} - x_{\min})/N$, though the domain extents are not explicitly stated.

---

## 4. PDE Solver

### 4.1 Overall Structure

[SOLID] The PDE solver employs a conservative finite volume method described in Pandya:2022pif (ref: paper line 1452). The approach uses the **method of lines**: spatial discretization produces a semi-discrete system of the form:

$$
\frac{d\mathbf{U}}{dt} = \mathbf{L}(\mathbf{U}),
$$

where $\mathbf{U}$ represents the cell-averaged conserved variables and $\mathbf{L}$ is the spatial discretization operator (including flux differences and source terms). This semi-discrete system is then integrated forward in time.

### 4.2 Conservative Formulation

[SOLID] The BDNK equations are written in conservative form via the conservation laws (ref: paper Eqs. 1--2):

$$
\nabla_a T^{ab} = 0, \quad \nabla_a J^a = 0.
$$

In flat (1+1)D Minkowski spacetime with Cartesian coordinates $(t, x)$, these become:

$$
\partial_t T^{tb} + \partial_x T^{xb} = 0, \quad \partial_t J^t + \partial_x J^x = 0.
$$

The conserved variables are the components $T^{tt}, T^{tx}$, and $J^t = nW$ (where $W = (1-v^2)^{-1/2}$ is the Lorentz factor). The corresponding fluxes are $T^{xt}, T^{xx}$, and $J^x = nWv$.

**Key distinction from ideal hydrodynamics:** The BDNK stress-energy tensor (ref: paper Eqs. 7--16) contains first derivatives of the primitive variables $(\epsilon, n, u^a)$. When inserted into the conservation laws, this produces **second-order** PDEs, unlike the first-order system of ideal hydrodynamics. This has two important consequences:

1. The system is second-order in time, so initial conditions for both the state variables and their time derivatives must be specified.
2. The primitive variable recovery procedure (going from conserved to primitive variables) is more involved than in standard ideal hydrodynamics, as it must account for gradient terms in the stress-energy tensor.

[PRELIMINARY] The paper does not provide explicit details on the primitive recovery procedure for the BDNK system. These details are contained in Pandya:2022pif.

### 4.3 Spatial Discretization: WENO/CWENO

[SOLID] The spatial reconstruction uses Weighted Essentially Non-Oscillatory (WENO) / Central WENO (CWENO) methods (ref: paper line 1452). Key properties:

- **Convergence order:** At most fourth-order convergent in the grid spacing for smooth flows.
- **Conservative:** Fluxes are computed at cell interfaces, ensuring discrete conservation.
- **Non-oscillatory:** The WENO methodology uses nonlinear weights that adapt to local solution smoothness, suppressing spurious oscillations near discontinuities while maintaining high-order accuracy in smooth regions.

[PRELIMINARY] The paper does not specify the WENO stencil width, polynomial order, smoothness indicators, or whether reconstruction is performed component-wise or characteristic-wise. All such details are contained in Pandya:2022pif. For reproducibility of the specific WENO variant, the reader must consult that reference.

### 4.4 Time Integration: Heun's Method (TVD-RK2)

[SOLID] Time integration uses Heun's method, also known as the total variation diminishing second-order Runge-Kutta scheme (TVD-RK2). This is a two-stage method (ref: paper line 1452):

<a id="eq:Heun"></a>
$$
\begin{aligned}
\mathbf{U}^* &= \mathbf{U}^n + \Delta t\, \mathbf{L}(\mathbf{U}^n) \\
\mathbf{U}^{n+1} &= \frac{1}{2}\mathbf{U}^n + \frac{1}{2}\left[\mathbf{U}^* + \Delta t\, \mathbf{L}(\mathbf{U}^*)\right]
\end{aligned}
$$

This is equivalent to:

$$
\mathbf{U}^{n+1} = \mathbf{U}^n + \frac{\Delta t}{2}\left[\mathbf{L}(\mathbf{U}^n) + \mathbf{L}(\mathbf{U}^*)\right],
$$

which is the standard trapezoidal-rule predictor-corrector form. The method is:

- **Second-order accurate** in time.
- **TVD (Total Variation Diminishing):** When combined with an appropriate spatial discretization, it does not increase the total variation of the solution, preventing the growth of spurious oscillations.
- **SSP (Strong Stability Preserving):** It preserves any convex stability property satisfied by forward Euler.

The **overall scheme is second-order** (ref: paper line 1452), limited by the time integrator. At finite resolution, convergence can be at higher rates when time derivatives are small, because the spatial discretization is up to fourth-order accurate.

### 4.5 CFL Condition and Stiffness

#### 4.5.1 CFL Numbers Used

[SOLID] The Courant-Friedrichs-Lewy (CFL) condition restricts the timestep:

$$
\Delta t = \lambda\, \Delta x
$$

where $\lambda$ is the CFL number. The values used in the paper are:

| Case | $\lambda$ | Reference |
|------|-----------|-----------|
| Default (all cases) | $0.1$ | ref: paper line 1452 |
| "Stiff superluminal" ($\hat{\tau} = 0.4$, $c_+ \sim 1.6$) | $0.01$ | ref: paper lines 1127--1129 |
| "Wildly superluminal" ($\hat{\tau} = 0.25$, $c_+ \sim 2$) | $0.01$ | ref: paper line 1452 |

The CFL condition requires $\lambda \leq \lambda_{\max}$ where $\lambda_{\max}$ depends on the maximum characteristic speed $c_{\max}$ of the system and the spatial discretization. The actual constraint is:

$$
\Delta t \leq \frac{C_{\text{CFL}}\, \Delta x}{c_{\max}},
$$

where $C_{\text{CFL}}$ is a scheme-dependent constant of order unity. Since the BDNK characteristic speeds $c_\pm$ can exceed unity for superluminal frames, the required timestep becomes correspondingly smaller.

#### 4.5.2 Stiffness

[SOLID] Stiffness arises when the relaxation times are small ($\hat{\tau} \to 0$, ref: paper lines 854--856, 1125--1131). The mechanism is:

1. Small $\hat{\tau}$ implies small $\tau_\epsilon$ (since $\tau_\epsilon = L \hat{V}\, \hat{\tau}$).
2. Small $\tau_\epsilon$ implies large characteristic speeds $c_\pm$ (from [Eq. (A8)](#eq:cpmsq); as $\hat{\tau} \to 0$, $c_\pm^2 \to \infty$).
3. Large $c_\pm$ tightens the CFL condition, requiring very small $\Delta t$.
4. Simultaneously, the relaxation timescale $\tau_\epsilon$ is very short, meaning the solution has fast-decaying "frame modes" that must be temporally resolved.

**Physical interpretation:** Decreasing $\hat{\tau}$ brings the BDNK equations closer to the Eckart (parabolic) limit, where information propagates infinitely fast. The explicit time integrator must resolve these fast modes, leading to prohibitively small timesteps.

**Practical consequence for Bjorken flow (ODE):** The equation of motion [Eq. (35)](#eq:Bjorken_EOM) becomes a "stiff" ODE, requiring very small steps in $\tau$ to resolve the decay time $\tau_\epsilon$ (ref: paper lines 855--856).

**Practical consequence for shockwave PDE:** The $\hat{\tau} = 0.4$ case ($c_+ \sim 1.6$) requires an order of magnitude smaller CFL number than $\hat{\tau} = 0.5$ ($c_+ \sim 1.5$) (ref: paper lines 1127--1129).

[HYPOTHESIS] For production-level simulations with very small $\hat{\tau}$, an implicit or IMEX (implicit-explicit) time integration scheme would likely be needed to avoid prohibitively small timesteps. The paper uses only explicit methods.

---

## 5. Initial and Boundary Conditions

### 5.1 Shockwave PDE Initial Data

[SOLID] The initial data for the dynamical shockwave PDE problem uses error function profiles (ref: paper Eq. 79):

<a id="eq:shockwave_ID"></a>
$$
\begin{aligned}
\epsilon(0, x) &= \frac{\epsilon_R - \epsilon_L}{2}\left[\text{erf}\!\left(\frac{x}{w}\right) + 1\right] + \epsilon_L \\
v(0, x) &= \frac{v_L - v_R}{2}\left[1 - \text{erf}\!\left(\frac{x}{w}\right)\right] + v_R \\
n(0, x) &= \frac{n_L - n_R}{2}\left[1 - \text{erf}\!\left(\frac{x}{w}\right)\right] + n_R
\end{aligned}
$$

where $\text{erf}(y) = \frac{2}{\sqrt{\pi}}\int_0^y e^{-s^2}\, ds$ is the Gaussian error function. Each profile smoothly interpolates between the asymptotic left state ($x \to -\infty$) and the right state ($x \to +\infty$).

**Width parameter:** $w = 10$ (ref: paper line 1056).

**Note on sign conventions:** The energy density profile is written so that $\epsilon \to \epsilon_L$ as $x \to -\infty$ and $\epsilon \to \epsilon_R$ as $x \to +\infty$ (since $\text{erf}(-\infty) = -1$, $\text{erf}(+\infty) = +1$). The velocity and density profiles have the opposite convention (using $1 - \text{erf}$) because $v_L > v_R$ and $n_L > n_R$ for these shockwaves.

[PRELIMINARY] **Time derivative initial data for the shockwave PDE:** The BDNK equations are second-order in time, so initial time derivatives $\dot{\epsilon}(0,x)$ and $\dot{v}(0,x)$ must be specified. The paper does not explicitly state how these are chosen for the shockwave problem. Since the initial data [Eq. (46)](#eq:shockwave_ID) approximates a steady-state shock profile, the time derivatives should be small (ideally zero, matching the steady-state solution), but the precise initialization is not documented. This is in contrast to the heat flow problem, where time-symmetric data ($\dot{\epsilon} = \dot{u}^i = 0$) is explicitly specified.

### 5.2 Rankine-Hugoniot Conditions

[SOLID] The right states $(\epsilon_R, v_R, n_R)$ are determined from the left states using the Rankine-Hugoniot jump conditions for a shockwave in its rest frame (ref: paper Eq. 80):

<a id="eq:Rankine_Hugoniot"></a>
$$
\begin{aligned}
n_L W_L v_L &= n_R W_R v_R \\
v_L W_L^2 \rho_L &= v_R W_R^2 \rho_R \\
v_L^2 W_L^2 \rho_L + P_L &= v_R^2 W_R^2 \rho_R + P_R
\end{aligned}
$$

where $W_i = (1 - v_i^2)^{-1/2}$ and $\rho_i = \epsilon_i + P_i$.

This is a **nonlinear system of 3 equations in 3 unknowns** ($\epsilon_R, v_R, n_R$), which must be solved numerically (e.g., via Newton's method). The equation of state is needed to evaluate $P$ and $\rho$ from $\epsilon$ and $n$.

**Numerical solutions** (ref: paper Eq. 81):

| Left state $\{\epsilon_L, v_L, n_L\}$ | Right state $\{\epsilon_R, v_R, n_R\}$ | Used in |
|----------------------------------------|----------------------------------------|---------|
| $\{1,\; 0.9,\; 1\}$ | $\{11.5174,\; 0.354727,\; 5.44212\}$ | Fig. 3 |
| $\{1,\; 0.6,\; 1\}$ | $\{1.33795,\; 0.514414,\; 1.25027\}$ | Fig. 4 |

### 5.3 Heat Flow Initial Data

[SOLID] The heat flow initial data specifies a Gaussian temperature profile at constant pressure (ref: paper Eq. 95):

<a id="eq:heat_flow_ID"></a>
$$
T(0, x) = A\, e^{-x^2/w^2} + \delta, \quad P(0, x) = P_0 = \text{const}.
$$

**Conversion to primitive variables:** Since the PDE solver evolves $\epsilon$ and $n$, the initial data must be converted using the EOS (ref: paper line 1220):

$$
\epsilon = P\left[\frac{m}{T} + \frac{1}{\Gamma - 1}\right], \quad n = \frac{P}{T}.
$$

These follow directly from $P = nT$ and $\epsilon = mn(1+e)$ with $P = (\Gamma-1)mne$.

**Time-symmetric initial data** (ref: paper line 1220):

$$
\dot{\epsilon}(0, x) = 0, \quad \dot{u}^i(0, x) = 0.
$$

This is the specification needed for the second-order-in-time BDNK system. At $t = 0$, the $x$-component of $\nabla_a T^{ab} = 0$ is trivially satisfied, and the $t$-component reduces to (ref: paper Eq. 96):

$$
\left.T^{at}_{,a}\right|_{t=0} = 0 = \tau_\epsilon\, \ddot{\epsilon} - (\kappa T')'.
$$

This equation determines $\ddot{\epsilon}$ at $t = 0$ from the initial spatial profile, and is used by the PDE solver to initiate the evolution.

**Key physics:** With $\hat{\sigma} = 0$ (hence $\sigma = \kappa = 0$), the initial data is a stationary solution ($\ddot{\epsilon} = 0$). Only when $\hat{\sigma} > 0$ does dynamical heat flow occur (ref: paper lines 1226--1234).

[PRELIMINARY] **Specific parameter values:** The parameters $A$ (Gaussian amplitude), $\delta$ (temperature offset), $w$ (width), and $P_0$ (constant pressure) in [Eq. (53)](#eq:heat_flow_ID) are not explicitly given in the paper text or Table II. They may only be available in the code repository. For the tests shown in Figs. 5--6, the parameters $\Gamma = 4/3$, $m = 0.1$, $\hat{V} = 2/15$ are used with $\hat{\sigma}$ and $\hat{\tau}$ as given in Table II.

### 5.4 Ghost Cells and Boundary Treatment

[SOLID] The finite volume method uses ghost cells to implement boundary conditions (ref: paper line 1452). For the shockwave and heat flow problems:

- **Boundary type:** Outflow (copy/extrapolation) boundary conditions, since the solutions have non-trivial asymptotic states.
- **Effect on convergence:** Interaction with ghost cell boundaries degrades the convergence rate from second order to between first and second order (ref: paper line 1452).
- **Timing of boundary interaction:** Transients from the initial data propagate away and interact with the boundaries at $t \sim 80$ for the shockwave problem and $t \sim 150$ for the heat flow problem (ref: paper `fig:conv_plot` caption, line 1457).

[PRELIMINARY] The number of ghost cells, the specific extrapolation method used, and the computational domain extents ($x_{\min}, x_{\max}$) are not stated in the paper. These details are in Pandya:2022pif.

---

## 6. Convergence Testing

### 6.1 Convergence Factor $Q_N$

[SOLID] The convergence factor is defined as (ref: paper Eq. B1, label `eq:convergence_factor`):

<a id="eq:convergence_factor"></a>
$$
Q_N = \frac{\|R_{N/2}\|}{\|R_N\|}
$$

where:
- $R_N$ is a **discrete residual** evaluated on the numerical solution at resolution $N$.
- $\|\cdot\|$ denotes the **1-norm** (sum of absolute values) (ref: paper line 1437).
- The residual $R_N$ is identically zero for exact solutions to the continuum equations; it measures the extent to which the discrete solution fails to satisfy the continuum equations.

### 6.2 Richardson Expansion and Expected Rates

[SOLID] The convergence factor $Q_N$ can be related to the order of the numerical scheme via the Richardson expansion (ref: paper line 1438). For a scheme of order $p$ with uniform grid spacing $h = (\text{domain size})/N$, the error at each gridpoint has the form:

$$
e_i = C_i h^p + O(h^{p+1}).
$$

Since the norm of the residual scales as $\|R_N\| \propto h^p \propto N^{-p}$, halving the grid spacing (doubling $N$) gives:

$$
Q_N = \frac{\|R_{N/2}\|}{\|R_N\|} \to 2^p \quad \text{as } N \to \infty.
$$

Therefore:
- **RK4 (fourth-order):** $Q_N \to 2^4 = 16$ as $N \to \infty$.
- **PDE solver (second-order overall):** $Q_N \to 2^2 = 4$ as $N \to \infty$.

### 6.3 Independent Residual Discretizations

[SOLID] A critical aspect of the convergence testing methodology is that the residual $R_N$ is computed using an **independent discretization**, distinct from the one used to evolve the equations. This avoids the trivial result that the evolution scheme's own discrete equations are satisfied by construction.

The independent discretizations used are:

| Problem | Residual equation | Independent discretization |
|---------|-------------------|---------------------------|
| Bjorken flow ODE | Eq. 35 | Fourth-order centered finite difference |
| Shockwave ODE | $T^{tx}_{,x} = 0$ | Fourth-order centered finite difference |
| Shockwave PDE | $t$-component of $\nabla_a T^{ab} = 0$ | Second-order Crank-Nicolson |
| Heat flow PDE | $t$-component of $\nabla_a T^{ab} = 0$ | Second-order Crank-Nicolson |

(ref: paper lines 1449, 1457)

### 6.4 ODE Convergence Results (Table III)

[SOLID] Reproduction of Table III from the paper (ref: paper Table III, lines 1441--1450):

| Test | $N$ | $Q_{N/4}$ | $Q_{N/2}$ | $Q_N$ |
|------|-----|-----------|-----------|-------|
| Bjorken flow, $\hat{\tau} = 0.5$ | $2^{11}$ | 34.8 | 18.7 | 16.9 |
| Bjorken flow, $\hat{\tau} = 1$ | $2^{11}$ | 18.4 | 16.9 | 16.3 |
| Bjorken flow, $\hat{\tau} = 2$ | $2^{11}$ | 16.9 | 16.3 | 16.1 |
| Shockwave | $2^{13}$ | 15.9 | 15.9 | 15.9 |

**Interpretation:**

- All cases converge toward $Q_N = 16$, consistent with the fourth-order RK4 method.
- The Bjorken flow results are for the $\dot{\epsilon}_0 = -2$ initial condition; convergence for $\dot{\epsilon}_0 = 0, 2$ is essentially identical (ref: paper Table III caption).
- **Stiffness effect:** For $\hat{\tau} = 0.5$ (the stiffest case), convergence is slowest, with $Q_{N/4} = 34.8$ significantly above 16. This is because the stiff modes require finer resolution to resolve. As $\hat{\tau}$ increases (and stiffness decreases), the convergence factor approaches 16 more rapidly.
- The shockwave ODE converges very cleanly with $Q_N \approx 15.9$ at all three resolutions, slightly below 16, indicating that the shockwave profile is well-resolved even at moderate resolution.

The column labels require clarification: for the row with $N = 2^{11}$, the three convergence factors are computed at resolutions $N/4 = 2^9$, $N/2 = 2^{10}$, $N = 2^{11}$. Specifically, $Q_{N/4}$ means $Q$ evaluated at resolution $N/4$, i.e., $Q_{N/4} = \|R_{N/8}\| / \|R_{N/4}\|$.

### 6.5 PDE Convergence Results

[SOLID] PDE convergence results are shown in the paper's convergence plot (ref: paper `fig:conv_plot`, line 1457). Key findings:

- **Near $t = 0$:** $Q_N \approx 4$ for both the shockwave and heat flow problems, consistent with the second-order scheme.
- **After boundary interaction:** The convergence rate degrades to between first and second order. Boundary interaction occurs at $t \sim 80$ for the shockwave (bottom panel of Fig. 3) and $t \sim 150$ for the heat flow ($\hat{\sigma} = 0.15$ case of Fig. 6).
- **Higher-order convergence at finite resolution:** Because the WENO/CWENO spatial discretization is up to fourth-order for smooth flows, $Q_N$ can transiently exceed 4 at finite resolution when spatial errors dominate over temporal errors.

The independent residual for the PDE convergence test is computed using a second-order Crank-Nicolson discretization of the $t$-component of $\nabla_a T^{ab} = 0$ (ref: paper line 1457).

### 6.6 Convergence Figure Analysis (Fig. 7, `conv_plot.pdf`)

The convergence figure consists of two side-by-side panels, each displaying $Q_N(t)$ at three resolutions ($N = 2^{11}, 2^{12}, 2^{13}$, light gray to black). A horizontal red dotted line at $Q_N = 4$ marks the expected second-order convergence rate.

**Left panel (shockwave):** Clean second-order convergence ($Q_N \approx 4$) up to $t \sim 80$, after which boundary interaction degrades the rate. The highest-resolution curve stays closest to 4. At late times, values settle between $\sim 3.5$ and $4.5$, consistent with a mixture of second-order interior accuracy and first-order boundary contamination.

**Right panel (heat flow, $\hat{\sigma} = 0.15$):** Similar behavior with $Q_N \approx 4$ up to $t \sim 150$, followed by a sharp spike near $t \sim 160\text{--}180$ when boundary-reflected signals reach the interior. The highest-resolution curve ($N = 2^{13}$) settles near $Q_N \sim 3.5$ at late times.

**Implementation note:** The convergence factor at resolution $N$ is computed from the Richardson expansion $Q_N = \|R_{N/2}\| / \|R_N\|$, where $R_N$ is an independent Crank-Nicolson residual. The degradation after boundary interaction arises because ghost cell boundary conditions are at best first-order accurate, reducing the effective convergence rate when boundary-reflected signals contaminate the interior solution.

---

## 7. Practical Considerations

### 7.1 Stiffness and CFL Restrictions

[SOLID] The relationship between $\hat{\tau}$ and numerical stiffness is a central practical concern:

**In Bjorken flow (ODE):** "Decreasing $\hat{\tau} \propto \tau_\epsilon$ makes the equation of motion (35) a 'stiff' ODE, requiring very small steps in $\tau$ to still resolve the decay time $\tau_\epsilon$" (ref: paper lines 854--856).

**In shockwave PDE:** The paper demonstrates a concrete example of stiffness scaling. The threshold appears to be around $\hat{\tau} \sim 0.5$:

| $\hat{\tau}$ | $c_+$ | Required CFL $\lambda$ | Behavior |
|-------------|--------|------------------------|----------|
| $1.5$ | $\sim 0.9$ | $0.1$ | Subluminal, no issues |
| $0.5$ | $\sim 1.5$ | $0.1$ | Weakly superluminal, no issues |
| $0.4$ | $\sim 1.6$ | $0.01$ | Stiff superluminal, requires 10x smaller timestep |
| $0.25$ | $\sim 2$ | $0.01$ | Wildly superluminal, fast instability onset |

The order-of-magnitude jump in required CFL number between $\hat{\tau} = 0.5$ and $\hat{\tau} = 0.4$ illustrates the rapid onset of stiffness as $\hat{\tau}$ decreases.

### 7.2 Characteristic Speed Monitoring

[SOLID] The characteristic speeds $c_\pm$ and $c_1$ are monitored during evolution as diagnostics. They are computed from (ref: paper Eqs. A15--A16):

<a id="eq:cpmsq"></a>
$$
c_\pm^2 = \frac{c_s^2}{2\hat{\tau}}\left(2\alpha - \omega\hat{\sigma} + \hat{\tau} + 1 \pm \left[\omega\hat{\sigma}(4\alpha + \omega\hat{\sigma}) + (2\alpha + 1)^2 - 2(\omega + 2)\hat{\sigma} + \hat{\tau}^2 + \hat{\tau}(2 - 2\omega\hat{\sigma})\right]^{1/2}\right)
$$

<a id="eq:c1sq"></a>
$$
c_1^2 = c_s^2\, \frac{\eta}{V\hat{\tau}}
$$

These speeds serve multiple purposes:
1. **Causality check:** $|c_+| < 1$ ensures causal propagation. The paper demonstrates that violations ($|c_+| > 1$) do not immediately cause problems for "weakly superluminal" cases but lead to instabilities for "wildly superluminal" cases.
2. **CFL constraint:** The maximum characteristic speed determines the maximum stable timestep.
3. **Shockwave stability:** If the flow velocity $v$ exceeds $c_+$ anywhere in the shockwave profile, a high-frequency numerical instability sets in (ref: paper Fig. 3, lines 1060--1070).

### 7.3 Coordinate Systems

[SOLID] Two coordinate systems are used:

| Coordinate system | Metric | Used for |
|-------------------|--------|----------|
| Cartesian $(t, x, y, z)$ | $\eta_{ab} = \text{diag}(-1, 1, 1, 1)$ | Shockwave and heat flow problems |
| Milne $(\tau, x, y, \xi)$ | $g_{ab} = \text{diag}(-1, 1, 1, \tau^2)$ | Bjorken flow |

**Why Milne for Bjorken:** Boost invariance implies that the solution depends only on $\tau$, reducing the PDEs to a single ODE. In Cartesian coordinates, Bjorken flow would require solving coupled PDEs.

**Milne coordinate details:**
- $\tau = \sqrt{t^2 - z^2}$ (proper time)
- $\xi = \text{arctanh}(z/t)$ (rapidity)
- Christoffel symbols: $\Gamma^\xi_{\tau\xi} = \Gamma^\xi_{\xi\tau} = 1/\tau$, $\Gamma^\tau_{\xi\xi} = \tau$
- Metric determinant: $\sqrt{|g|} = \tau$
- Flow velocity: $u^a = (1, 0, 0, 0)^T$ (fixed by boost invariance)

### 7.4 Ghost Cell and Boundary Effects on Late-Time Convergence

[SOLID] Ghost cell boundary interactions are identified as the primary cause of convergence degradation at late times (ref: paper line 1452, `fig:conv_plot` caption):

- **Before boundary interaction:** The convergence factor $Q_N$ is consistent with the expected second-order rate ($Q_N \approx 4$).
- **After boundary interaction:** Convergence degrades to between first and second order.
- **Mechanism:** Transients generated by the initial data (which deviate from a true steady-state solution) propagate outward and eventually reach the computational domain boundaries. The outflow boundary conditions do not perfectly absorb these transients, introducing boundary errors that pollute the interior solution.
- **Timing:** The time at which boundary effects become significant depends on the domain size and the propagation speed of the transients. For the paper's test problems, this occurs at $t \sim 80$ (shockwave) and $t \sim 150$ (heat flow).

### 7.5 Handling Second-Order-in-Time Terms

[SOLID] The BDNK stress-energy tensor contains terms proportional to $\dot{\epsilon} \equiv u^c \nabla_c \epsilon$ and $\nabla_c u^c$, which are first-order time derivatives of the primitive variables. When the conservation law $\nabla_a T^{ab} = 0$ is applied, this produces second-order time derivatives ($\ddot{\epsilon}$, etc.).

For the **ODE problems**, this is handled straightforwardly by reducing to a first-order system (introducing $\dot{\epsilon}$ as an additional variable, as in Sec. 3.1.3).

For the **PDE problems**, the method-of-lines approach naturally accommodates this: the spatial discretization operator $\mathbf{L}(\mathbf{U})$ computes spatial derivatives of all quantities (including those involving time derivatives of primitives), and the Heun time integrator advances the full state forward. The specific algorithmic details of how this is implemented in the conservative finite volume framework are contained in Pandya:2022pif.

### 7.6 Diagnostic Quantities

[SOLID] The following quantities are computed during the evolution for diagnostic purposes:

1. **$\dot{\epsilon} + \Gamma\epsilon/\tau$** (Bjorken flow): This quantity equals $mn_0(\Gamma-1)/\tau^2$ for the inviscid solution, independent of $e_0$, providing a clean measure of how close the viscous solution is to the inviscid one (ref: paper Fig. 1 caption).

2. **Temperature in different frames:** The BDNK frame temperature $T$ (from the EOS applied to the evolved $\epsilon, n$) is compared with an Eckart frame temperature $T_E$, computed by first evaluating $T^{\tau\tau} = \epsilon_E$ and then using the EOS to find $T_E(\epsilon_E, n)$ (ref: paper lines 915--921). The difference between $T$ and $T_E$ measures how far the solution is from equilibrium.

3. **Characteristic speeds $c_\pm, c_1$:** Monitored to check causality and stability, as described in Sec. 7.2.

4. **Convergence factor $Q_N(t)$:** Computed as a function of time for the PDE problems, revealing the time at which boundary effects degrade convergence (ref: paper `fig:conv_plot`).

---

## 8. Summary of Numerical Algorithms by Problem

For quick reference, the following table summarizes which numerical method applies to each test problem:

| Problem | Type | Method | State vector | Domain | Key parameters |
|---------|------|--------|-------------|--------|----------------|
| Bjorken flow | ODE (IVP) | RK4 | $(\epsilon, \dot{\epsilon})$ | $\tau \in [1, 20]$ | $\epsilon_0 = 0.25$, $\dot{\epsilon}_0 \in \{-2,0,2\}$, $n_0 = 0.1$ |
| Shockwave ODE | ODE (IVP) | RK4 | $(n, \epsilon, v)$ | $x$-domain | $\{\epsilon_L, v_L, n_L\} = \{1, 0.8, 0.1\}$ |
| Shockwave PDE | PDE (IVP) | FV + WENO + Heun | Conserved vars | $(t,x)$ domain | Erf profiles, $w = 10$, $\lambda = 0.1$ or $0.01$ |
| Heat flow PDE | PDE (IVP) | FV + WENO + Heun | Conserved vars | $(t,x)$ domain | Gaussian $T$, const $P$, $\dot{\epsilon}_0 = 0$ |

**Resolution ranges:**
- ODE problems: $N = 2^9$ to $2^{13}$ gridpoints
- PDE problems: Multiple resolutions for convergence testing; specific values include $N \in \{2^7, 2^8, 2^9, 2^{10}, 2^{11}\}$ for the acausal instability study (ref: paper Fig. 4 caption)

---

## Appendix: Open Questions

[BLOCKING] The following items are not fully specified in the paper and would require consulting Pandya:2022pif or the code repository for complete reproducibility:

1. **WENO/CWENO specifics:** Order, stencil width, smoothness indicators, component-wise vs. characteristic-wise reconstruction.
2. **Primitive variable recovery:** How primitive variables $(\epsilon, n, u^a)$ are recovered from conserved variables in the presence of gradient terms in the BDNK stress-energy tensor.
3. **Shockwave ODE initialization:** How integration is started at finite $x$ for the steady-state shockwave, given that the left state is an asymptotic condition at $x \to -\infty$.
4. **Heat flow parameters:** The specific values of $A$, $\delta$, $w$, and $P_0$ in Eq. 53 are not given in the paper.
5. **Shockwave PDE time-derivative initial data:** How $\dot{\epsilon}(0,x)$ and $\dot{v}(0,x)$ are specified for the shockwave PDE evolution.
6. **Computational domain extents:** The values of $x_{\min}$ and $x_{\max}$ for the PDE simulations are not stated.
7. **Number of ghost cells:** Not specified in the paper; contained in Pandya:2022pif.
