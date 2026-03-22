# Plan: Mathematica Implementation of BDNK Numerical Methods

## Execution Environment

- **Executable:** `/Applications/Wolfram.app/Contents/MacOS/wolframscript`
- **Output directory:** `/Users/hyw/Desktop/Agent/BDNK/mathematica/`
- **Plot export format:** PDF (matching paper figure names)
- **All scripts are `.wl` (Wolfram Language) files**, executed via `wolframscript -file <script>.wl`

---

## Shared Module: `mathematica/bdnk_common.wl`

All five scripts share the same equation of state, thermodynamics, and transport coefficient calculations. Factor these into a common module loaded by each script via ``Get["bdnk_common.wl"]``.

### Contents

**1. Equation of State (paper Eqs. 25-26, 31-38):**

```mathematica
(* Gamma-law EOS: P = (Gamma-1)(eps - m*n), rho = eps + P *)
pressure[eps_, n_, Gamma_, m_] := (Gamma - 1)*(eps - m*n)
enthalpy[eps_, n_, Gamma_, m_] := eps + pressure[eps, n, Gamma, m]
                                (* = Gamma*eps - (Gamma-1)*m*n *)
soundSpeedSq[eps_, n_, Gamma_, m_] := Module[{P, rho},
  P = pressure[eps, n, Gamma, m];
  rho = enthalpy[eps, n, Gamma, m];
  Gamma*P/rho
]
temperature[eps_, n_, Gamma_, m_] := (Gamma - 1)*(eps/n - m)
```

**2. Microphysics-derived quantities (paper Eqs. 31-38):**

```mathematica
(* Derivatives of P *)
pPrimeEps[Gamma_] := Gamma - 1
pPrimeN[Gamma_, m_] := -(Gamma - 1)*m

(* kappa quantities *)
kappaEps[eps_, n_, Gamma_, m_] := Module[{P, rho},
  P = pressure[eps, n, Gamma, m];
  rho = enthalpy[eps, n, Gamma, m];
  -(Gamma - 1)*eps*rho^2/(n^2*P)
]
kappaN[eps_, n_, Gamma_, m_] := Module[{P, rho},
  P = pressure[eps, n, Gamma, m];
  rho = enthalpy[eps, n, Gamma, m];
  rho/(n^2*P)*((Gamma - 1)*eps^2 + P^2)
]
kappaS[eps_, n_, Gamma_, m_] := -(Gamma - 1)*m*enthalpy[eps, n, Gamma, m]/n

(* Dimensionless ratios *)
alphaRatio[eps_, n_, Gamma_, m_] := (Gamma - 1)/soundSpeedSq[eps, n, Gamma, m]
omegaRatio[eps_, n_, Gamma_, m_] := Module[{P, rho},
  P = pressure[eps, n, Gamma, m];
  rho = enthalpy[eps, n, Gamma, m];
  m*n*P/(eps*rho)
]
```

**3. Transport coefficient computation (paper Eq. 41, with L=1):**

Recipe: given local state (eps, n) and dimensionless parameters (Gamma, m, Vhat, sigmaHat, tauHat):

```mathematica
transportCoeffs[eps_, n_, Gamma_, m_, Vhat_, sigmaHat_, tauHat_] := Module[
  {P, rho, cs2, V, tauEps, tauP, tauQ, sigma, kE, kN, kS, betaEps, betaN, kappa, gammaCoeff},

  P = (Gamma - 1)*(eps - m*n);
  rho = eps + P;
  cs2 = Gamma*P/rho;

  (* Transport coefficients, L = 1 *)
  V = Vhat*rho*cs2;                       (* combined viscosity *)
  tauEps = Vhat*tauHat;                   (* relaxation time epsilon *)
  tauQ = Vhat*tauHat;                     (* relaxation time Q = tauEps *)
  tauP = 2*(Gamma - 1)*Vhat;              (* relaxation time P *)

  (* Thermal conductivity *)
  kE = -(Gamma - 1)*eps*rho^2/(n^2*P);    (* kappaEpsilon *)
  sigma = Vhat*rho*cs2*sigmaHat/(-kE);    (* sigma *)

  (* kappa_n, kappa_s for beta computation *)
  kN = rho/(n^2*P)*((Gamma - 1)*eps^2 + P^2);
  kS = kE + kN;  (* = -(Gamma-1)*m*rho/n *)

  (* beta coefficients (paper Eqs. 18-19) *)
  betaEps = (Gamma - 1)*tauQ - (Gamma - 1)*sigma*eps*rho/(n^2*P);
  betaN = -(Gamma - 1)*m*tauQ + sigma*rho/(n^3*P)*((Gamma - 1)*eps^2 + P^2);

  (* Thermal conductivity kappa = sigma*rho^2/(n^2*T) *)
  kappa = If[sigmaHat == 0, 0, sigma*rho^2/(n^2*temperature[eps, n, Gamma, m])];

  (* gamma coefficient for heat flow: gamma = tauQ + sigma*rho/n^2 *)
  gammaCoeff = tauQ + sigma*rho/n^2;

  <|"P" -> P, "rho" -> rho, "cs2" -> cs2, "V" -> V,
    "tauEps" -> tauEps, "tauP" -> tauP, "tauQ" -> tauQ,
    "sigma" -> sigma, "betaEps" -> betaEps, "betaN" -> betaN,
    "kE" -> kE, "kN" -> kN, "kS" -> kS,
    "kappa" -> kappa, "gammaCoeff" -> gammaCoeff|>
]
```

**Important note:** `tauEps`, `tauP`, `tauQ` are **constants** (independent of local state) for this frame ansatz. The quantities `V`, `sigma`, `betaEps`, `betaN`, `kappa` depend on the local state (eps, n) and must be recomputed at each step.

**4. Characteristic speeds (paper Eqs. A15-A16):**

```mathematica
charSpeeds[eps_, n_, Gamma_, m_, Vhat_, sigmaHat_, tauHat_] := Module[
  {cs2, alpha, omega, disc, cp2, cm2},
  cs2 = soundSpeedSq[eps, n, Gamma, m];
  alpha = alphaRatio[eps, n, Gamma, m];
  omega = omegaRatio[eps, n, Gamma, m];
  disc = Sqrt[omega*sigmaHat*(4*alpha + omega*sigmaHat) + (2*alpha + 1)^2
              - 2*(omega + 2)*sigmaHat + tauHat^2 + tauHat*(2 - 2*omega*sigmaHat)];
  cp2 = cs2/(2*tauHat)*(2*alpha - omega*sigmaHat + tauHat + 1 + disc);
  cm2 = cs2/(2*tauHat)*(2*alpha - omega*sigmaHat + tauHat + 1 - disc);
  {Sqrt[cp2], Sqrt[cm2]}
]
```

---

## Script 1: `mathematica/bjorken.wl` -- Bjorken Flow ODE

### Purpose
Reproduce Fig. 1 of the paper: Bjorken flow in Milne coordinates.

### Governing Equation (paper Eq. 66)

Second-order ODE for eps(tau):
```
tauEps * eps'' = -(1/tau)*(tau + 2*tauEps + tauP)*eps' - (1/tau^2)*(rho*(tau + tauP) - V)
```
where `n(tau) = n0/tau` is exact (paper Eq. 65), and transport coefficients depend on local (eps, n).

### First-Order Reduction

State vector: `y = {eps, epsDot}`. The system is:
```
y1' = y2
y2' = (1/tauEps)*[-(1/tau)*(tau + 2*tauEps + tauP)*y2 - (1/tau^2)*(rho*(tau + tauP) - V)]
```

### Parameters (Table II, Fig. 1 row)

| Parameter | Value |
|-----------|-------|
| Gamma | 4/3 |
| m | 1 |
| Vhat | 1/10 |
| sigmaHat | 0 |
| tauHat | {0.5, 1, 2} |
| eps0 | 0.25 |
| epsDot0 | {-2, 0, 2} |
| n0 | 0.1 |
| Domain | tau in [1, 20] |

### Implementation

**Step 1: Define the RHS function**

```mathematica
bjorkenRHS[tau_, {eps_, epsDot_}, Gamma_, m_, Vhat_, tauHat_, n0_] := Module[
  {n, P, rho, cs2, V, tauEps, tauP},
  n = n0/tau;
  P = (Gamma - 1)*(eps - m*n);
  rho = eps + P;
  cs2 = Gamma*P/rho;
  V = Vhat*rho*cs2;         (* L = 1 *)
  tauEps = Vhat*tauHat;     (* constant *)
  tauP = 2*(Gamma - 1)*Vhat; (* constant *)

  {epsDot,
   (1/tauEps)*(-(1/tau)*(tau + 2*tauEps + tauP)*epsDot
               - (1/tau^2)*(rho*(tau + tauP) - V))}
]
```

**Step 2: Solve using NDSolve**

Use `NDSolve` with `Method -> {"ExplicitRungeKutta", "DifferenceOrder" -> 4}` (this is the classical RK4 equivalent). Set `MaxStepSize` appropriately; for tauHat = 0.5 (stiff), use a smaller max step.

```mathematica
solveBjorken[tauHat_, epsDot0_] := NDSolve[
  {eps'[tau] == bjorkenRHS[tau, {eps[tau], epsDot[tau]}, ...][[1]],
   epsDot'[tau] == bjorkenRHS[tau, {eps[tau], epsDot[tau]}, ...][[2]],
   eps[1] == 0.25, epsDot[1] == epsDot0},
  {eps, epsDot},
  {tau, 1, 20},
  Method -> {"ExplicitRungeKutta", "DifferenceOrder" -> 4},
  MaxStepSize -> 19/2^11  (* ~0.0093, matching paper resolution *)
]
```

Alternative (cleaner): define as a system of two first-order ODEs directly.

```mathematica
sol = NDSolve[{
  y1'[t] == y2[t],
  y2'[t] == (1/tauEps)*(-(1/t)*(t + 2*tauEps + tauP)*y2[t]
            - (1/t^2)*(rhoFunc[y1[t], n0/t]*(t + tauP) - VFunc[y1[t], n0/t])),
  y1[1] == 0.25,
  y2[1] == epsDot0
}, {y1, y2}, {t, 1, 20},
  Method -> {"ExplicitRungeKutta", "DifferenceOrder" -> 4},
  MaxStepSize -> 19/2048
]
```

**Step 3: Inviscid reference solution (paper Eq. 67)**

```mathematica
epsInviscid[tau_, Gamma_, m_, n0_, e0_] := m*n0/tau*(1 + e0*tau^(-(Gamma - 1)))
```

The constant `e0` is determined from initial data: `eps0 = m*n0*(1 + e0)`, so `e0 = eps0/(m*n0) - 1`.

The diagnostic quantity `epsDot + Gamma*eps/tau` evaluates to `m*n0*(Gamma-1)/tau^2` on the inviscid solution, independent of `e0`.

**Step 4: Compute Eckart-frame temperature (for bottom panel)**

The stress-energy tensor component `T^{tau tau}` for BDNK is:
```
Ttt = eps + tauEps*(epsDot + rho/tau)
```
(using E = eps + tauEps * [u^c nabla_c eps + rho * nabla_c u^c] with nabla_c u^c = 1/tau in Milne).

Then Eckart-frame energy density `epsE = Ttt`, and Eckart temperature:
```
T_E = (Gamma - 1)*(epsE/n - m)
```

**Step 5: Plotting**

*Top panel (log-log):*
- x-axis: tau (log scale, 1 to 20)
- y-axis: |epsDot + Gamma*eps/tau| (log scale)
- 9 black curves: 3 tauHat values x 3 epsDot0 values
  - Solid lines for tauHat = 0.5
  - Dash-dot for tauHat = 1
  - Dotted for tauHat = 2
- 1 red dashed line: inviscid solution `m*n0*(Gamma-1)/tau^2`

```mathematica
LogLogPlot[..., PlotRange -> {{1, 20}, {1*^-4, 1}},
  AxesLabel -> {"\[Tau]", "..."},
  PlotStyle -> {... line styles ...}]
```

*Bottom panel (linear-log):*
- x-axis: tau (log scale)
- y-axis: T (linear, approx -0.6 to 2.2)
- 3 black solid curves: BDNK temperature T for tauHat = 2
- 3 blue dashed curves: Eckart temperature T_E for tauHat = 2

Use `Show[LogLinearPlot[...], ...]` or plot against `Log[tau]`.

**Export:**
```mathematica
Export["mathematica/bjorken_plot.pdf", combinedPlot]
```

### Key Implementation Choices

| Choice | Value | Rationale |
|--------|-------|-----------|
| NDSolve method | ExplicitRungeKutta, order 4 | Matches paper's RK4 |
| MaxStepSize | 19/2048 (~0.0093) | Matches paper's N=2^11 resolution |
| WorkingPrecision | MachinePrecision | Sufficient for these ODEs |
| Stiff case (tauHat=0.5) | May need MaxStepSize -> 19/8192 | Stiffness requires finer steps |

### Expected Outputs

1. `mathematica/bjorken_plot.pdf` -- two-panel figure matching Fig. 1
2. Console output: convergence of all solutions to inviscid attractor

---

## Script 2: `mathematica/shockwave_steady.wl` -- Steady-State Shockwave ODE

### Purpose
Reproduce Fig. 2: steady-state shockwave profiles for eps(x), v(x), n(x).

### Governing Equations (paper Eqs. 72, 76-77)

Three coupled first-order ODEs for {n(x), eps(x), v(x)}:

```
n'  = -W^2 * n * v' / v
eps' = (c4*v^4 + c3*v^3 + c2*v^2 + c1*v + c0) / (A*W*v*(v-cp)*(v+cp)*(v-cm)*(v+cm))
v'   = (d3*v^3 + d2*v^2 + d1*v + d0) / (A*W^3*(v-cp)*(v+cp)*(v-cm)*(v+cm))
```

### Parameters (Table II, Fig. 2 row)

| Parameter | Value |
|-----------|-------|
| Gamma | 4/3 |
| m | 0.1 |
| Vhat | 2/15 |
| sigmaHat | 0 |
| tauHat | 1.5 |
| Left state | {epsL, vL, nL} = {1, 0.8, 0.1} |
| Domain | x in [-xMax, xMax], xMax ~ 5-10 (estimated from Fig. 2 showing x in [-2, 2]) |

### Conserved Quantities

Computed from perfect-fluid stress-energy at the left asymptotic state:
```mathematica
PL = (Gamma - 1)*(epsL - m*nL);
rhoL = epsL + PL;
WL = 1/Sqrt[1 - vL^2];
Ttx = rhoL*WL^2*vL;
Txx = rhoL*WL^2*vL^2 + PL;
```

### Numerator Coefficients (paper Eq. 78)

At each evaluation point, compute the full transport coefficients and then:

```mathematica
c0 = betaN*n*(Txx - P);
c1 = -Ttx*(2*betaN*n - rho*tauP + V);
c2 = (betaN*n - rho*(tauEps + tauP + tauQ) + V)*(Txx + eps) + rho^2*(tauEps + tauQ);
c3 = rho*Ttx*(tauEps + 2*tauQ);
c4 = -rho*tauQ*(Txx + eps);

d0 = betaEps*(Txx - P);
d1 = -Ttx*(2*betaEps + tauP);
d2 = (Txx + eps)*(betaEps + tauEps + tauP) - rho*tauEps;
d3 = -tauEps*Ttx;
```

### Characteristic Speeds

Compute A, B, C (paper Eqs. A2-A4) for the denominator factorization:
```mathematica
A = rho*tauEps*tauQ;
B = -tauEps*(rho*cs2*tauQ + V + sigma*kS) - rho*tauP*tauQ;
C = tauP*(rho*cs2*tauQ + sigma*kS) - betaEps*V;
disc = Sqrt[B^2 - 4*A*C];
cp = Sqrt[(-B + disc)/(2*A)];
cm = Sqrt[(-B - disc)/(2*A)];
```

Note: with sigmaHat = 0, sigma = 0, so kS terms vanish and B, C simplify.

### Implementation

**Step 1: Define the RHS function**

```mathematica
shockwaveRHS[x_, {nVal_, epsVal_, vVal_}] := Module[
  {W, P, rho, cs2, tc, ...numerator coefficients..., denomEps, denomV, epsPrime, vPrime, nPrime},
  W = 1/Sqrt[1 - vVal^2];
  (* compute all transport coeffs *)
  tc = transportCoeffs[epsVal, nVal, Gamma, m, Vhat, sigmaHat, tauHat];
  (* compute A, B, C, cp, cm *)
  ...
  (* compute c0..c4, d0..d3 *)
  ...
  epsPrime = (c4*vVal^4 + c3*vVal^3 + c2*vVal^2 + c1*vVal + c0) / denomEps;
  vPrime = (d3*vVal^3 + d2*vVal^2 + d1*vVal + d0) / denomV;
  nPrime = -W^2*nVal*vPrime/vVal;
  {nPrime, epsPrime, vPrime}
]
```

**Step 2: Initialization strategy**

The left state is asymptotic (x -> -inf). In practice, start at a large negative x with a small perturbation away from equilibrium. The paper does not document the precise initialization, so use:

Option A: Start at `x = -xStart` (e.g., -5) with a small perturbation:
```mathematica
{n0, eps0, v0} = {nL, epsL, vL} + delta*{dnPerturb, depsPerturb, dvPerturb}
```
where `delta` is small (e.g., 1e-6) and the perturbation direction is along the unstable eigenvector of the ODE linearized about the left equilibrium.

Option B (simpler): Use NDSolve with `WhenEvent` to detect when v approaches the right state and stop. Start from a point slightly away from the left state.

Option C (recommended): Solve using NDSolve from x = -5 to x = 5, with initial conditions at x = -5 set to exactly {nL, epsL, vL} and apply a tiny kick to v or eps. The ODE has the left state as an unstable fixed point, so any perturbation will grow into the shockwave profile.

```mathematica
(* Small perturbation: decrease v slightly from left-state value *)
sol = NDSolve[{
  n'[x] == shockwaveRHS[x, {n[x], eps[x], v[x]}][[1]],
  eps'[x] == shockwaveRHS[x, {n[x], eps[x], v[x]}][[2]],
  v'[x] == shockwaveRHS[x, {n[x], eps[x], v[x]}][[3]],
  n[-5] == nL, eps[-5] == epsL, v[-5] == vL - 1*^-6
}, {n, eps, v}, {x, -5, 5},
  Method -> {"ExplicitRungeKutta", "DifferenceOrder" -> 4},
  MaxStepSize -> 10/2^13
]
```

**Step 3: Right-state computation (for reference)**

Solve Rankine-Hugoniot conditions to find (epsR, vR, nR) -- not needed for the ODE integration itself, but useful for verifying the asymptotic right state.

```mathematica
rhSolution = FindRoot[{
  nL*WL*vL == nR*WR*vR,
  vL*WL^2*rhoL == vR*WR^2*rhoR,
  vL^2*WL^2*rhoL + PL == vR^2*WR^2*rhoR + PR
} /. {WR -> 1/Sqrt[1 - vR^2], rhoR -> epsR + (Gamma-1)*(epsR - m*nR), ...},
  {{epsR, 2}, {vR, 0.5}, {nR, 0.2}}
]
```

**Step 4: Plotting**

Three-panel figure (or single panel with three quantities):
- x-axis: x in [-2, 2] (matching Fig. 2)
- Solid line: eps(x)
- Dash-dot: v(x)
- Dotted: n(x)
- Black curves: ideal gas BDNK fluid
- (Green curves for conformal fluid -- skip unless needed)

```mathematica
Plot[{eps[x] /. sol, v[x] /. sol, n[x] /. sol}, {x, -2, 2},
  PlotStyle -> {{Black, Thick}, {Black, DashDotted}, {Black, Dotted}},
  AxesLabel -> {"x", ""},
  PlotLegends -> {"\[Epsilon]", "v", "n"}]
```

**Export:**
```mathematica
Export["mathematica/shockwave_plot.pdf", plot]
```

### Key Implementation Choices

| Choice | Value | Rationale |
|--------|-------|-----------|
| NDSolve method | ExplicitRungeKutta, order 4 | Matches paper's RK4 |
| MaxStepSize | 10/8192 (~0.0012) | Fine enough for ODE |
| Integration domain | x in [-5, 5] | Wider than plot range [-2, 2] |
| Perturbation | v(-5) = vL - 1e-6 | Seed unstable eigenvector |
| WorkingPrecision | MachinePrecision or 20 | May need higher precision near singularities |

### Expected Outputs

1. `mathematica/shockwave_plot.pdf` -- three curves matching Fig. 2
2. Console output: right-state values from Rankine-Hugoniot for verification

---

## Script 3: `mathematica/shockwave_dynamic.wl` -- Dynamic Shockwave PDE

### Purpose
Reproduce Figs. 3 and 4: dynamic shockwave formation, stability/instability tests, and acausality tests.

### Governing Equations

The BDNK conservation laws in (1+1)D flat Minkowski:
```
d_t T^{tt} + d_x T^{xt} = 0
d_t T^{tx} + d_x T^{xx} = 0
d_t J^t + d_x J^x = 0
```

The conserved variables are `U = {T^{tt}, T^{tx}, J^t}` and the fluxes are `F = {T^{xt}, T^{xx}, J^x}`.

The stress-energy tensor components include first-derivative terms from the BDNK constitutive relations (paper Eqs. 7-16), making the system second-order in time.

### Approach: Method of Lines with Finite Volume

**Spatial discretization:** Since implementing full WENO/CWENO in Mathematica is very involved, use one of these approaches:

**Option A (Recommended for Mathematica):** Use NDSolve's built-in PDE capabilities with `MethodOfLines`. Mathematica's NDSolve can handle systems of hyperbolic PDEs.

**Option B:** Implement a simple finite volume scheme manually:
1. Discretize x into N cells with cell-averaged values
2. Compute fluxes at cell interfaces using a simple numerical flux (Lax-Friedrichs or Rusanov)
3. Time-step with Heun's method (TVD-RK2)

**Option C (Simplest, recommended first attempt):** Use NDSolve with MethodOfLines and a spatial discretization of 200-400 points. The second-order nature of the BDNK system means we need to evolve the primitive variables and their time derivatives.

### Implementation Strategy

Given the complexity of the BDNK PDE system (second-order in time, requiring primitive variable recovery), the most practical Mathematica approach is:

**Step 1: Formulate as a first-order-in-time system**

Introduce auxiliary variables for time derivatives. The state vector becomes:
```
{eps(t,x), v(t,x), n(t,x), epsDot(t,x), vDot(t,x)}
```
where `epsDot = d_t eps` and `vDot = d_t v`. The conservation laws then become evolution equations for these 5 fields.

However, this requires expressing the BDNK stress-energy tensor components explicitly in terms of the primitives and their spatial/temporal derivatives, then forming the conservation law system. This is the approach of Pandya:2022pif.

**Step 2: Alternative -- direct NDSolve approach**

Formulate the two conservation laws and baryon conservation as three coupled PDEs for eps(t,x), v(t,x), n(t,x). Since BDNK has terms involving d_t eps and d_t v, these appear as second-time-derivative terms in the conservation laws, which NDSolve can handle if properly set up.

The explicit PDE system:
```
d_t[E(eps, n, v, d_t eps, d_x eps, d_x n, d_x v, ...)] + d_x[Fx(...)] = 0
d_t[Mx(eps, n, v, ...)] + d_x[Fmx(...)] = 0
d_t[n*W] + d_x[n*W*v] = 0
```

**Step 3: Practical implementation**

Use manual finite-difference discretization in space, creating an ODE system for the cell values:

```mathematica
(* Discretize spatial domain into Nx cells *)
Nx = 256; (* or 512 for higher resolution *)
dx = (xMax - xMin)/Nx;
xGrid = Table[xMin + (i - 0.5)*dx, {i, 1, Nx}];

(* Initialize primitive variables on grid *)
(* Error function initial data (paper Eq. 46) *)
epsInit[x_] := (epsR - epsL)/2*(Erf[x/w] + 1) + epsL;
vInit[x_] := (vL - vR)/2*(1 - Erf[x/w]) + vR;
nInit[x_] := (nL - nR)/2*(1 - Erf[x/w]) + nR;
```

For time integration, use Heun's method (TVD-RK2) with CFL number lambda = 0.1:
```
dt = lambda * dx  (* where lambda = 0.1 or 0.01 for stiff cases *)
```

**NOTE:** Full implementation of the BDNK PDE solver in Mathematica is the most complex script. It requires:
1. Computing T^{ab} and J^a from primitives and their derivatives
2. Computing spatial derivatives via finite differences (or WENO reconstruction)
3. Recovering primitives from conserved variables (iterative procedure)
4. Time-stepping with Heun's method

This script should be structured as:
- `computeFluxes[U, dx]` -- compute T^{xt}, T^{xx}, J^x from cell data
- `spatialRHS[U, dx]` -- compute d_t U from flux differences
- `heunStep[U, dt, dx]` -- one step of Heun's method
- `evolve[U0, tFinal, dt, dx]` -- main evolution loop

### Initial Data

**Fig. 3 (dynamic shockwave stability):**

Left state: {epsL, vL, nL} = {1, 0.9, 1}
Right state (from Rankine-Hugoniot): {11.5174, 0.354727, 5.44212}
Width: w = 10
Parameters: Gamma = 4/3, m = 0.1, Vhat = 4/3, sigmaHat = 0
Two runs: tauHat = 1.5 (stable, evolve to t=372) and tauHat = 3 (unstable, evolve to t=27)

**Fig. 4 (acausality tests):**

Left state: {epsL, vL, nL} = {1, 0.6, 1}
Right state (from Rankine-Hugoniot): {1.33795, 0.514414, 1.25027}
Width: w = 10
Parameters: Gamma = 4/3, m = 0.1, Vhat = 4/3, sigmaHat = 0
Four runs: tauHat in {0.25, 0.4, 0.5, 1.5}
CFL: lambda = 0.1 for tauHat = {0.5, 1.5}; lambda = 0.01 for tauHat = {0.25, 0.4}

### Rankine-Hugoniot Solver

```mathematica
solveRankineHugoniot[epsL_, vL_, nL_, Gamma_, m_] := Module[
  {PL, rhoL, WL, eqs, sol},
  PL = (Gamma - 1)*(epsL - m*nL);
  rhoL = epsL + PL;
  WL = 1/Sqrt[1 - vL^2];

  eqs = {
    nL*WL*vL == nR*1/Sqrt[1 - vR^2]*vR,
    vL*WL^2*rhoL == vR*(1/(1 - vR^2))*((Gamma*epsR - (Gamma - 1)*m*nR)),
    vL^2*WL^2*rhoL + PL == vR^2*(1/(1 - vR^2))*(Gamma*epsR - (Gamma - 1)*m*nR)
                           + (Gamma - 1)*(epsR - m*nR)
  };

  sol = FindRoot[eqs, {{epsR, 5}, {vR, 0.4}, {nR, 2}}];
  {epsR, vR, nR} /. sol
]
```

### Boundary Conditions

Outflow (copy) boundary conditions: ghost cells copy the values from the nearest interior cell.

### Plotting

**Fig. 3:**
- Top panel: v(x) at t=27 for tauHat=3, multiple resolutions. Dotted line at c_+ ~ 0.75.
- Bottom panel: v(x) at t=372 for tauHat=1.5, multiple resolutions. Dotted line at c_+ ~ 0.94.

**Fig. 4:**
- Top panel: v(x) at t=0 (dotted) and t=1582 (solid) for tauHat = {0.4, 0.5, 1.5}.
- Bottom panel: v(x) at three early times for tauHat = 0.25.

Domain: x in [-50, 50] for Fig. 3; x in [-100, 100] for Fig. 4.

**Export:**
```mathematica
Export["mathematica/shock_instability.pdf", fig3]
Export["mathematica/acaus_instab.pdf", fig4]
```

### Key Implementation Choices

| Choice | Value | Rationale |
|--------|-------|-----------|
| Spatial discretization | 2nd-order central FD or simple WENO | Simplest that works |
| Time integration | Heun's method (TVD-RK2) | Matches paper |
| CFL number | 0.1 (default), 0.01 (stiff) | Matches paper |
| Nx (spatial points) | 256-512 for stable, 128-512 for resolution study | Multiple resolutions needed |
| Domain | [-100, 100] for Fig. 4; [-50, 50] for Fig. 3 | Large enough for long-time evolution |
| Ghost cells | 2-3 on each side | Standard for 2nd-order scheme |

### Expected Outputs

1. `mathematica/shock_instability.pdf` -- two-panel figure matching Fig. 3
2. `mathematica/acaus_instab.pdf` -- two-panel figure matching Fig. 4

---

## Script 4: `mathematica/heat_flow.wl` -- Heat Conduction PDE

### Purpose
Reproduce Figs. 5 and 6: heat flow stationary test and telegrapher's equation transition.

### Governing Equations

Same BDNK PDE system as Script 3, but with different initial data and zero initial velocity.

Key simplification: u^i = 0 at t=0, and the initial data is designed so that:
- Baryon conservation: n_dot = 0 (n is time-independent)
- At t=0, the x-component of conservation is trivially satisfied
- The t-component gives: `tauEps * eps_ddot = (kappa * T')' ` (paper Eq. 96)

When sigma = 0 (hence kappa = 0), eps_ddot = 0 and the solution is stationary.

### Initial Data (paper Eq. 53/95)

```mathematica
(* Gaussian temperature profile at constant pressure *)
(* PRELIMINARY: A, delta, w, P0 not explicitly given in paper *)
(* Reasonable defaults based on figure analysis: *)
A = 0.1;        (* Gaussian amplitude -- T ranges from ~1.0 to ~1.1 in Fig. 6 *)
delta = 1.0;    (* background temperature *)
w = 10;         (* Gaussian width -- similar to shockwave width *)
P0 = 1/3;       (* constant pressure -- chosen for convenience *)

Tinit[x_] := A*Exp[-x^2/w^2] + delta;
Pinit = P0;

(* Convert to primitive variables using EOS *)
epsInit[x_] := Pinit*(m/Tinit[x] + 1/(Gamma - 1));
nInit[x_] := Pinit/Tinit[x];

(* Time-symmetric initial data *)
epsDotInit[x_] := 0;
vInit[x_] := 0;
```

**NOTE:** The parameters A, delta, w, P0 are marked [PRELIMINARY] in the documentation -- they are not explicitly stated in the paper. The values above are estimates from the figure analysis (Fig. 6 shows T ranging from ~1.0 to ~1.1 with background at ~1.0). These may need to be adjusted to match the paper figures.

### Parameters

**Fig. 5 (heat stationary test):**

| Parameter | Value |
|-----------|-------|
| Gamma | 4/3 |
| m | 0.1 |
| Vhat | 2/15 |
| sigmaHat | 0 (top panel), 1/3 (bottom panel) |
| tauHat | 1.5 |

**Fig. 6 (telegrapher's equation):**

| Parameter | Value |
|-----------|-------|
| Gamma | 4/3 |
| m | 0.1 |
| Vhat | 2/15 |
| sigmaHat | 0.15, 1.5, 7.5 |
| tauHat | 1.5, 15, 75 |

Design choice: sigmaHat/tauHat = 0.1 is held constant across all three cases.

### Implementation

The PDE solver is the same finite volume code as Script 3. The main differences are:

1. **Initial data:** Gaussian temperature profile instead of error function shockwave
2. **Initial velocity:** v = 0 everywhere
3. **Diagnostics:** Plot eps_dot (Fig. 5) or T (Fig. 6) instead of v

**Step 1: Set up initial data on grid**

```mathematica
Nx = 256;
xMin = -100; xMax = 100;  (* domain from Fig. 6 *)
dx = (xMax - xMin)/Nx;
```

**Step 2: Evolve using same PDE solver as Script 3**

For Fig. 5: evolve a short time (just after t=0) and plot eps_dot at multiple resolutions.
For Fig. 6: evolve to t = {16, 39, 312} and plot T(x) at each time.

**Step 3: Compute eps_dot diagnostic**

After one or a few time steps, compute `epsDot = (eps^{n+1} - eps^n)/dt` on the grid. For Fig. 5, this should be ~0 when sigma=0 and nonzero when sigma>0.

**Step 4: Plotting**

*Fig. 5 (heat stationary):*
- Top panel: |eps_dot(x)| at early time for sigmaHat = 0, multiple resolutions (light to dark gray)
- Bottom panel: |eps_dot(x)| at early time for sigmaHat = 1/3, multiple resolutions

```mathematica
ListLinePlot[Table[epsDotData[Nx], {Nx, {128, 256, 512}}],
  PlotStyle -> Table[GrayLevel[1 - i/3], {i, 1, 3}],
  AxesLabel -> {"x", "|\!\(\*OverscriptBox[\(\[Epsilon]\), \(.\)]\)|"}]
```

*Fig. 6 (telegrapher's):*
Three side-by-side panels showing T(x) at t = 16, 39, 312:
- Light gray: sigmaHat = 0.15, tauHat = 1.5
- Medium gray: sigmaHat = 1.5, tauHat = 15
- Black: sigmaHat = 7.5, tauHat = 75

```mathematica
GraphicsRow[{plot1, plot2, plot3}]
```

**Export:**
```mathematica
Export["mathematica/heat_stationary.pdf", fig5]
Export["mathematica/telegraphers_plot.pdf", fig6]
```

### Key Implementation Choices

| Choice | Value | Rationale |
|--------|-------|-----------|
| Spatial domain | [-100, 100] | Matches Fig. 6 axis range |
| Nx | {128, 256, 512} for resolution study | Three resolutions for convergence |
| CFL | 0.1 | Default from paper |
| Evolution times (Fig. 5) | Small dt after t=0 | Just need eps_dot shortly after initialization |
| Evolution times (Fig. 6) | t = {16, 39, 312} | From figure analysis |
| Boundary conditions | Outflow (copy) | Same as shockwave PDE |

### Expected Outputs

1. `mathematica/heat_stationary.pdf` -- two-panel figure matching Fig. 5
2. `mathematica/telegraphers_plot.pdf` -- three-panel figure matching Fig. 6

---

## Script 5: `mathematica/convergence.wl` -- Convergence Testing

### Purpose
Reproduce Table III (ODE convergence) and Fig. 7 (PDE convergence).

### ODE Convergence (Table III)

**Method:** Compute independent residuals using 4th-order centered finite differences, then compute convergence factor Q_N.

**Step 1: Solve Bjorken ODE at multiple resolutions**

```mathematica
resolutions = {2^9, 2^10, 2^11};  (* 512, 1024, 2048 *)

(* For each resolution N, solve with step size h = 19/N *)
bjorkenSolutions = Table[
  solveBjorkenFixedStep[tauHat, epsDot0, N],
  {N, resolutions}
];
```

To get fixed-step RK4 output, either:
- Use `NDSolve` with `StartingStepSize -> h`, `MaxStepSize -> h`, and `Method -> {"FixedStep", Method -> {"ExplicitRungeKutta", "DifferenceOrder" -> 4}}`
- Or implement RK4 manually with `Fold`/`NestList`

**Step 2: Compute independent residual**

The residual for Bjorken flow is an independent 4th-order centered finite difference discretization of Eq. 66:

```mathematica
(* 4th-order centered FD for second derivative: *)
(* f''(x) ~ (-f[x-2h] + 16*f[x-h] - 30*f[x] + 16*f[x+h] - f[x+2h]) / (12*h^2) *)
(* 4th-order centered FD for first derivative: *)
(* f'(x) ~ (-f[x+2h] + 8*f[x+h] - 8*f[x-h] + f[x-2h]) / (12*h) *)

computeResidual[epsSol_, tauGrid_, h_, Gamma_, m_, Vhat_, tauHat_, n0_] := Module[
  {Npts, residual, tau, eps, epsDot, epsDD, n, P, rho, cs2, V, tauEps, tauP},
  Npts = Length[tauGrid];
  residual = Table[
    tau = tauGrid[[i]];
    eps = epsSol[[i]];
    (* 4th-order centered FD for eps' and eps'' *)
    epsDot = (-epsSol[[i+2]] + 8*epsSol[[i+1]] - 8*epsSol[[i-1]] + epsSol[[i-2]])/(12*h);
    epsDD = (-epsSol[[i+2]] + 16*epsSol[[i+1]] - 30*epsSol[[i]] + 16*epsSol[[i-1]] - epsSol[[i-2]])/(12*h^2);

    n = n0/tau;
    P = (Gamma - 1)*(eps - m*n);
    rho = eps + P;
    cs2 = Gamma*P/rho;
    V = Vhat*rho*cs2;
    tauEps = Vhat*tauHat;
    tauP = 2*(Gamma - 1)*Vhat;

    (* Residual: LHS - RHS of Eq. 66 *)
    tauEps*epsDD + (1/tau)*(tau + 2*tauEps + tauP)*epsDot + (1/tau^2)*(rho*(tau + tauP) - V),
    {i, 3, Npts - 2}  (* skip boundary points *)
  ];
  Total[Abs[residual]]  (* 1-norm *)
]
```

**Step 3: Compute convergence factor**

```mathematica
QN = residualNorm[N/2] / residualNorm[N]
```

Expected: Q_N -> 16 for RK4.

**Step 4: Shockwave ODE convergence**

Same approach, but the residual is the 4th-order FD discretization of `T^{tx}_{,x} = 0`:
```
T^{tx} = rho*W^2*v + (BDNK correction terms involving derivatives)
```
The residual is `d_x T^{tx}` evaluated with 4th-order centered FD on the numerical solution.

Resolutions: N = {2^11, 2^12, 2^13} (paper Table III shows N = 2^13 for shockwave).

### PDE Convergence (Fig. 7)

**Method:** Compute Q_N(t) using independent Crank-Nicolson residual.

**Step 1: Evolve PDE at three resolutions**

```mathematica
resolutions = {2^11, 2^12, 2^13};
```

Store the full solution history (or at least the solution at each time step) for all resolutions.

**Step 2: Compute Crank-Nicolson residual**

The independent Crank-Nicolson discretization of `d_t T^{tt} + d_x T^{xt} = 0`:

```mathematica
(* At time level n+1/2, using average of levels n and n+1: *)
RN[i, n] = (Ttt[i, n+1] - Ttt[i, n])/dt
           + (Txt[i+1/2, (n+n+1)/2] - Txt[i-1/2, (n+n+1)/2])/dx
```

This requires interpolating the solution in time to evaluate at half-steps, and computing T^{xt} from the interpolated solution.

**Step 3: Compute Q_N(t) and plot**

```mathematica
QN[t_] := Norm[residual[N/2, t], 1] / Norm[residual[N, t], 1]
```

Plot Q_N(t) vs t for each resolution pair.

### Plotting

**Table III output:** Print to console as formatted table.

**Fig. 7:**
Two side-by-side panels:
- Left: Q_N(t) for stable shockwave (bottom panel of Fig. 3)
- Right: Q_N(t) for heat flow (sigma_hat = 0.15 case of Fig. 6)
- Three curves per panel: N = {2^11, 2^12, 2^13} in light gray to black
- Horizontal red dotted line at Q_N = 4

```mathematica
GraphicsRow[{
  ListLinePlot[{QN2048, QN4096, QN8192}, PlotRange -> {0, 8},
    Epilog -> {Red, Dashed, Line[{{0, 4}, {tMax, 4}}]}],
  (* similar for heat flow *)
}]
```

**Export:**
```mathematica
Export["mathematica/conv_plot.pdf", fig7]
```

### Key Implementation Choices

| Choice | Value | Rationale |
|--------|-------|-----------|
| ODE resolutions | N = {2^9, 2^10, 2^11} for Bjorken; {2^11, 2^12, 2^13} for shockwave | Match paper Table III |
| PDE resolutions | N = {2^11, 2^12, 2^13} | Match paper Fig. 7 |
| Independent residual (ODE) | 4th-order centered FD | Paper specification |
| Independent residual (PDE) | 2nd-order Crank-Nicolson | Paper specification |
| Norm | 1-norm (Total[Abs[...]]) | Paper specification |
| Bjorken initial condition for convergence | epsDot0 = -2 | Paper Table III caption |

### Expected Outputs

1. Console output: Table III reproduction with Q_N values
2. `mathematica/conv_plot.pdf` -- two-panel figure matching Fig. 7

---

## Implementation Order and Dependencies

### Recommended execution order:

1. **`bdnk_common.wl`** -- shared module (no dependencies)
2. **`bjorken.wl`** -- simplest ODE problem, validates EOS and transport coefficients
3. **`shockwave_steady.wl`** -- more complex ODE, validates full transport coefficient machinery
4. **`convergence.wl` (ODE part only)** -- validates numerical accuracy of scripts 2 and 3
5. **`heat_flow.wl`** -- PDE problem, requires PDE solver infrastructure
6. **`shockwave_dynamic.wl`** -- PDE problem, same infrastructure as heat_flow
7. **`convergence.wl` (PDE part)** -- validates PDE solver accuracy

### Shared infrastructure needed for PDE scripts (3, 4):

The PDE solver is the most complex component. Before writing Scripts 3 and 4, implement:

1. **BDNK stress-energy tensor computation:** Given (eps, n, v) and their spatial and temporal derivatives, compute all components of T^{ab} and J^a using the BDNK constitutive relations (paper Eqs. 7-16).

2. **Conserved-to-primitive variable recovery:** Given (T^{tt}, T^{tx}, J^t), recover (eps, n, v). This is an iterative procedure (Newton's method) because the BDNK T^{ab} depends on derivatives of the primitives.

3. **Spatial discretization:** Either simple 2nd-order central differences or a basic WENO implementation.

4. **Time integrator:** Heun's method (TVD-RK2).

5. **Boundary conditions:** Ghost cell copy (outflow).

### Complexity Assessment

| Script | Complexity | Estimated Lines | Key Challenge |
|--------|-----------|-----------------|---------------|
| bdnk_common.wl | Low | 80-120 | Getting all coefficients correct |
| bjorken.wl | Low | 150-200 | Plotting format, stiff case step size |
| shockwave_steady.wl | Medium | 200-300 | ODE initialization near asymptotic state |
| shockwave_dynamic.wl | High | 500-800 | Full PDE solver implementation |
| heat_flow.wl | High | 400-600 | Same PDE solver, different IC |
| convergence.wl | Medium | 300-400 | Independent residual computation |

---

## Verification Checklist

After implementation, verify each script against the paper:

### Script 1 (Bjorken)
- [ ] All 9 curves converge to inviscid attractor (red dashed line)
- [ ] Larger tauHat = slower equilibration
- [ ] No qualitative change for superluminal case (tauHat = 0.5)
- [ ] Bottom panel: one solution has T < 0 (epsDot0 = -2)
- [ ] BDNK and Eckart temperatures converge at late times

### Script 2 (Shockwave steady)
- [ ] Smooth transition from left to right asymptotic states
- [ ] Velocity never reaches c_+ or c_- (no singularity)
- [ ] Right-state values match paper Eq. 81 (if computed via RH)

### Script 3 (Shockwave dynamic)
- [ ] tauHat = 3: instability where v > c_+ at t = 27
- [ ] tauHat = 1.5: stable evolution to t = 372
- [ ] Fig. 4 top: all three frames agree at t = 1582
- [ ] Fig. 4 bottom: instability for tauHat = 0.25 at early times

### Script 4 (Heat flow)
- [ ] Fig. 5 top: epsDot -> 0 with resolution when sigma = 0
- [ ] Fig. 5 bottom: epsDot -> nonzero with resolution when sigma = 1/3
- [ ] Fig. 6: transition from diffusive to wavelike behavior
- [ ] Fig. 6 right panel: oscillatory instability for sigmaHat = 7.5

### Script 5 (Convergence)
- [ ] Table III: Q_N -> 16 for all ODE cases
- [ ] Fig. 7: Q_N ~ 4 at early times for PDE cases
- [ ] Convergence degradation after boundary interaction

---

## Risk Assessment and Fallback Strategies

### Risk 1: PDE solver complexity
The full BDNK PDE solver (Scripts 3 and 4) is significantly more complex than the ODE problems. If the finite-volume approach proves too difficult in Mathematica:

**Fallback A:** Use NDSolve's built-in PDE solver with `MethodOfLines` and `"SpatialDiscretization" -> {"TensorProductGrid", "MinPoints" -> Nx}`. This may work for the smooth/stable cases but could fail for the instability tests.

**Fallback B:** Simplify to a second-order centered-difference spatial discretization with artificial viscosity, creating a large ODE system that NDSolve evolves in time.

**Fallback C:** For the unstable cases (Fig. 3 top, Fig. 4 bottom), qualitative reproduction may be acceptable -- showing that instability occurs without exactly matching the paper's WENO resolution.

### Risk 2: Heat flow initial data parameters
The parameters A, delta, w, P0 in Eq. 53 are not given in the paper. Strategy:
1. Start with reasonable guesses from figure analysis (A=0.1, delta=1.0, w=10, P0=1/3)
2. Adjust to match the temperature range shown in Fig. 6 (T from ~1.0 to ~1.1)
3. If needed, consult the code repository at https://github.com/FoPGSDI/BDNK-NT

### Risk 3: Shockwave ODE initialization
The paper does not specify how the ODE integration is initialized near the asymptotic left state. Strategy:
1. Try small perturbation approach (decrease v by 1e-6)
2. If that fails, compute the linearized eigenvector at the left equilibrium and perturb along it
3. Try shooting from the right state backward (since right state is a stable fixed point)

### Risk 4: Primitive variable recovery for PDE solver
The BDNK T^{ab} contains derivative terms, so recovering primitives from conserved variables is non-trivial. Strategy:
1. Use the ideal-fluid recovery as initial guess for Newton iteration
2. At each time step, use the previous time step's primitives as initial guess
3. If Newton fails, reduce time step

---

## Summary of Output Files

| File | Description | Paper Figure |
|------|-------------|-------------|
| `mathematica/bdnk_common.wl` | Shared EOS and transport module | -- |
| `mathematica/bjorken.wl` | Bjorken flow ODE solver | Fig. 1 |
| `mathematica/bjorken_plot.pdf` | Bjorken flow plots | Fig. 1 |
| `mathematica/shockwave_steady.wl` | Steady-state shockwave ODE | Fig. 2 |
| `mathematica/shockwave_plot.pdf` | Shockwave profiles | Fig. 2 |
| `mathematica/shockwave_dynamic.wl` | Dynamic shockwave PDE | Figs. 3, 4 |
| `mathematica/shock_instability.pdf` | Shockwave stability test | Fig. 3 |
| `mathematica/acaus_instab.pdf` | Acausality test | Fig. 4 |
| `mathematica/heat_flow.wl` | Heat conduction PDE | Figs. 5, 6 |
| `mathematica/heat_stationary.pdf` | Heat stationary test | Fig. 5 |
| `mathematica/telegraphers_plot.pdf` | Telegrapher's equation test | Fig. 6 |
| `mathematica/convergence.wl` | Convergence testing | Table III, Fig. 7 |
| `mathematica/conv_plot.pdf` | Convergence plots | Fig. 7 |
