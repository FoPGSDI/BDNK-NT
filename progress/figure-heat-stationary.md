# Figure Analysis: `heat_stationary.pdf`

**Figure label:** `fig:heat_stationary`
**Section:** III.D — "Heat flow problem with non-constant coefficients"
**Paper lines:** ~1213--1240 of `paper.tex`

---

## 1. Visual Description

The figure consists of two vertically stacked panels sharing the same horizontal axis (spatial coordinate x), each displaying a resolution study of the quantity |edot| (the absolute value of the time derivative of the energy density) at a time shortly after t = 0.

- **Top panel (sigma_hat = 0):** Three curves are plotted in progressively darker shades of gray corresponding to increasing numerical resolution (N = 2^7, 2^8, 2^9). The curves show noisy, oscillatory features concentrated near x = 0 (the center of the initial Gaussian temperature bump). An inset magnifies the central region, clearly revealing that the amplitude of the oscillations decreases systematically as the resolution is increased. At the coarsest resolution (N = 2^7, lightest gray) the signal is largest; at the finest resolution (N = 2^9, darkest/black) the signal is smallest and nearly flat. The vertical scale is on the order of 10^{-6}, indicating that these are tiny numerical artifacts.

- **Bottom panel (sigma_hat = 1/3):** Three curves are again plotted with the same gray-shade convention. Unlike the top panel, the curves here converge to a well-defined, nonzero profile as resolution increases. The |edot| signal has a rich spatial structure with multiple peaks concentrated symmetrically around x ~ +-40 to +-50, with smaller features near the center and edges. The vertical scale is on the order of 10^{-4}, two orders of magnitude larger than in the top panel. An inset magnifies a region near x ~ 50, showing that the three resolution curves overlap tightly---the solution has converged. A small amount of residual numerical noise is visible only at the base of the peaks in the lowest-resolution curve.

---

## 2. Axes and Labels

- **Horizontal axis (both panels):** x, the spatial coordinate, ranging from approximately -100 to +100.
- **Vertical axis (both panels):** |edot| (i.e., |epsilon_dot|), the absolute value of the time derivative of the energy density.
  - Top panel: scaled by 10^{-6}.
  - Bottom panel: scaled by 10^{-4}.
- **Annotations:** Each panel carries a label in the lower-left indicating the value of sigma_hat (sigma_hat = 0 in the top, sigma_hat = 1/3 in the bottom). The legend in the top panel identifies the three resolutions N = 2^7, 2^8, 2^9 by line shade.

The quantity plotted is epsilon_dot evaluated at a time shortly after t = 0. Because the initial data is time-symmetric (epsilon_dot(0,x) = 0), any nonzero epsilon_dot at early times must arise from the second time derivative ddot{epsilon} evaluated at t = 0, which is governed by Eq. (heat_ID_EOM).

---

## 3. Line Styles

Three curves appear in each panel, distinguished by gray shade:

| Resolution | Shade      | Meaning                                    |
|-----------|------------|---------------------------------------------|
| N = 2^7   | Light gray | Coarsest grid (128 points)                  |
| N = 2^8   | Medium gray| Intermediate grid (256 points)              |
| N = 2^9   | Black      | Finest grid (512 points)                    |

The convention is: darker lines correspond to higher resolution. This is a standard convergence-test presentation. No dashing or color is used; only the gray level distinguishes curves.

---

## 4. Key Observations

### Top panel (sigma_hat = 0): epsilon_dot converges to zero

- When sigma_hat = 0, the thermal conductivity kappa = sigma * rho^2 / (n^2 T) vanishes identically.
- The equation of motion at t = 0, namely tau_epsilon * ddot{epsilon} = (kappa T')', reduces to ddot{epsilon} = 0. Combined with the time-symmetric initial data (epsilon_dot(0,x) = 0), this means the energy density should remain constant: the solution has no dynamics.
- The nonzero values of |epsilon_dot| visible in the plot are purely numerical truncation error. The inset clearly demonstrates that this error decreases systematically with resolution (the lightest curve has the largest amplitude, the darkest curve the smallest), consistent with convergence to the exact (zero) solution.
- The magnitude is O(10^{-6}), confirming that the observed signal is a small numerical artifact.

### Bottom panel (sigma_hat = 1/3): epsilon_dot converges to a nonzero value

- When sigma_hat = 1/3, the thermal conductivity kappa is nonzero, so the right-hand side of the equation of motion (kappa T')' is a genuine nonzero source term.
- The time derivative epsilon_dot therefore develops a nonzero profile, representing genuine heat flow driven by the initial temperature gradient.
- The three resolution curves overlap almost perfectly, demonstrating clean numerical convergence to a physical (non-artifact) solution.
- The converged |epsilon_dot| has a characteristic multi-peak structure symmetric about x = 0, with the dominant peaks located near x ~ +-45. The spatial structure reflects the second spatial derivative of the initial Gaussian temperature profile filtered through the spatially varying kappa(x).
- The magnitude is O(10^{-4}), two orders of magnitude larger than the numerical noise in the top panel.

### Contrast between panels

The juxtaposition of the two panels provides a clean numerical demonstration that:
1. Thermal conductivity (sigma != 0) is a necessary condition for dynamical heat flow.
2. The code correctly produces a stationary (non-evolving) solution when sigma = 0.
3. The numerical scheme converges in both cases (to zero and to a nonzero profile, respectively).

---

## 5. Numerical / Implementation Notes

### Initial data (Eq. heat_flow_ID, paper Eq. 53)

The initial data is designed to represent a localized temperature perturbation atop a uniform-pressure background:

```
T(0, x) = A * exp(-x^2 / w^2) + delta,    P(0, x) = P_0 = const.
```

This ensures there is an initial temperature gradient but no pressure gradient, isolating the heat conduction mechanism from pressure-driven flow. (The paper notes in a footnote that this is impossible for a conformal fluid where P ~ T^4, making the ideal gas equation of state essential.)

### Conversion from (T, P) to (epsilon, n)

Because the BDNK PDEs are formulated in terms of hydrodynamic variables (epsilon, n) rather than (T, P), the initial data must be converted using the equation of state relations derived from the gamma-law EOS (Eq. EOS):

```
epsilon = P * [m / T + 1 / (Gamma - 1)]
n       = P / T
```

These follow directly from P = n T and epsilon = m n (1 + e) with P = (Gamma - 1) m n e.

### Time-symmetric initial data

To close the initial-value problem for the second-order-in-time BDNK system, first time derivatives must be specified. The choice is time-symmetric data:

```
epsilon_dot(0, x) = 0,    u^i_dot(0, x) = 0.
```

This has two consequences:
1. It ensures that at t = 0, the baryon conservation law reduces to n_dot = 0 (n remains constant for all time).
2. It means any early-time dynamics must come from ddot{epsilon}, which is determined by the t-component of stress-energy conservation (Eq. heat_ID_EOM).

### Resolution study

Three grid resolutions are used: N = 2^7 = 128, N = 2^8 = 256, N = 2^9 = 512 grid points. The convergence pattern (signal decreasing to zero in the top panel, signal stabilizing to a fixed profile in the bottom panel) validates both the theoretical prediction and the numerical implementation.

---

## 6. Connection to Theory

### Eq. (heat_ID_EOM) — the key diagnostic equation (paper Eq. 54)

At t = 0, stress-energy conservation reduces to:

```
T^{at}_{,a} |_{t=0} = 0 = tau_epsilon * ddot{epsilon} - (kappa T')'
```

This is the central equation connecting the figure to the theory:

- **When sigma = 0:** kappa = sigma * rho^2 / (n^2 T) = 0, so (kappa T')' = 0, hence ddot{epsilon} = 0. Combined with epsilon_dot(0,x) = 0 (time-symmetric data), the solution is static: epsilon_dot = 0 for all time. This is confirmed by the top panel.

- **When sigma != 0:** kappa != 0 and (kappa T')' != 0 wherever T has nonzero spatial curvature (which it does, due to the Gaussian initial profile). Therefore ddot{epsilon} != 0, and epsilon_dot develops a nonzero profile at early times. This is confirmed by the bottom panel.

### Physical interpretation

The thermal conductivity kappa (Eq. kappa in the paper) is the coefficient relating heat flux to temperature gradients in the Eckart decomposition. Setting sigma = 0 eliminates the heat conduction channel entirely. Even though a temperature gradient exists in the initial data, no energy can flow along it without a nonzero thermal conductivity. The figure provides a direct numerical verification of this fundamental physical requirement.

### Broader context in Sec. III.D

This figure is the first of two in the subsection on heat flow with non-constant transport coefficients. It establishes the baseline behavior: sigma controls whether heat flow occurs at all. The subsequent figure (fig:telegraphers) then explores the character of the heat flow (diffusive vs. wavelike) as sigma and tau are varied, connecting to the telegrapher's equation analysis from the constant-coefficient case in the preceding subsection (Sec. III.D's first part).

---

## 7. Parameters

From Table I (table:parameters) in the paper, the parameters for fig:heat_stationary are:

| Parameter     | Value         | Description                                       |
|---------------|---------------|---------------------------------------------------|
| Gamma         | 4/3           | Adiabatic index (gamma-law EOS)                   |
| m             | 0.1           | Particle rest mass                                |
| V_hat         | 2/15          | Dimensionless viscosity parameter                 |
| tau_hat        | 1.5           | Dimensionless relaxation time                     |
| sigma_hat     | 0 (top), 1/3 (bottom) | Dimensionless thermal conductivity parameter |

The initial data parameters (A, w, delta, P_0) for the Gaussian temperature profile in Eq. (heat_flow_ID) are not explicitly listed in the table; they are defined implicitly by the general form T(0,x) = A exp(-x^2/w^2) + delta with P(0,x) = P_0 = const.

The dimensionless sigma_hat is related to the physical thermal conductivity via kappa = sigma * rho^2 / (n^2 T), where sigma itself is determined by sigma_hat through the frame parametrization described in the paper's model section. Setting sigma_hat = 0 zeroes out sigma and hence kappa, while sigma_hat = 1/3 gives a finite, nonzero thermal conductivity.
