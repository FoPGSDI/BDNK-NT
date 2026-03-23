# Mathematical Conventions Reference Document

## Paper: "Neutron Star Evolution with BDNK Viscous Hydrodynamics Framework"
### (arXiv:2509.15303v1, Shum, Abalos, Bea, Bezares, Figueras, Palenzuela)

---

## 1. Index Conventions and Notation Rules

### 1.1 Spacetime vs. Spatial Indices

- **Greek indices** $\mu, \nu, \rho, \alpha, \beta, \ldots$ run from $0$ to $3$ and label **spacetime** components.
- **Roman indices** $i, j, k, l, m, n, \ldots$ run from $1$ to $3$ and label **spatial** components.
- **Einstein summation convention** used throughout.

### 1.2 Index Placement

- Upstairs (contravariant): $u^\mu$, $v^i$, $\beta^i$
- Downstairs (covariant): $u_\mu$, $S_i$, $n_\mu$
- Mixed: $K^i{}_j$, $\gamma^\mu{}_\alpha$, $T^\mu{}_\nu$
- Symmetrization: $v_{(\mu} w_{\nu)} = \tfrac{1}{2}(v_\mu w_\nu + v_\nu w_\mu)$

### 1.3 Derivative Notation

- Covariant derivative: $\nabla_\mu$
- Spatial covariant derivative: $D_i$
- Partial time derivative: $\partial_t$
- Partial spatial derivative: $\partial_i$, $\partial_r$
- Lie derivative: $\mathcal{L}_n$

---

## 2. Metric Signature and Units

### 2.1 Metric Signature

$$(-,+,+,+) \quad \text{(mostly positive)}$$

### 2.2 Geometric Units

$$G = c = 1$$

- Length, time, mass in units of $M_\odot$
- Energy density $\epsilon$, pressure $p$ in $M_\odot^{-2}$
- Velocities dimensionless (units of $c = 1$)
- $L = 1$ in all numerical work
- Decay rates in $M_\odot^{-1}$

### 2.3 Conversion: 1 $M_\odot$(time) = $4.9255 \times 10^{-6}$ s; 1/$M_\odot$ = 203,025 $s^{-1}$

---

## 3. Spacetime and 3+1 Variables

| Symbol | Definition |
|---|---|
| $\alpha$ | Lapse function |
| $\beta^i$ | Shift vector (= 0 in our gauge) |
| $\gamma_{ij}$ | Induced spatial metric |
| $n_\mu = -\alpha(dt)_\mu$ | Unit normal to spatial slices |
| $n^\mu = \frac{1}{\alpha}(\partial_t^\mu - \beta^i\partial_i^\mu)$ | Normal vector |
| $K_{\mu\nu} = -\frac{1}{2}\mathcal{L}_n\gamma_{\mu\nu}$ | Extrinsic curvature |
| $a_\mu = n^\nu\nabla_\nu n_\mu$ | Normal acceleration (spatial) |
| $\tilde{\gamma} = \sqrt{g_{rr}}\,g_{\theta\theta}$ | Spherical combination |

---

## 4. Fluid Variables

| Symbol | Definition |
|---|---|
| $\epsilon$ | Total energy density |
| $p = p(\epsilon)$ | Pressure (via EoS) |
| $c_s^2 = p'(\epsilon)$ | Speed of sound squared |
| $\rho_0$ | Rest mass density |
| $\rho \equiv \epsilon + p$ | Enthalpy density |
| $u^\mu = W(n^\mu + v^\mu)$ | Four-velocity |
| $v^i$ | Spatial three-velocity ($v^t = 0$) |
| $W = (1-\gamma_{ij}v^iv^j)^{-1/2}$ | Lorentz factor |
| $\tilde{v}^r = v^r/r$ | Regularized radial velocity |

---

## 5. Bar and Hat Notation

### Bar $\bar{\phantom{v}}$: spatial (orthogonal to $n^\mu$)

- $\bar{v}^\mu$: spatial velocity ($n_\mu v^\mu = 0$)
- $\hat{\bar{v}}^\mu$: spatial time derivative reduction

### Hat $\hat{\phantom{f}}$ (first-order reduction): negative normal-derivative

| Symbol | Definition |
|---|---|
| $\hat{\epsilon} = -n^\mu\nabla_\mu\epsilon$ | Time derivative of energy density |
| $\hat{\bar{v}}^\mu = -\gamma^\mu{}_\alpha n^\nu\nabla_\nu v^\alpha$ | Spatial time derivative of velocity |

### Hat (dimensionless parameters): frame parameters

| Symbol | Definition | Constraint |
|---|---|---|
| $\hat{a}$ | Frame parameter | $> 0$ |
| $\hat{q}$ | Frame/viscosity parameter | $0 < \hat{q} < \hat{s}$ |
| $\hat{s}$ | Frame parameter | $< 1/c_s^2$ |
| $\hat{\eta}$ | Dimensionless shear viscosity | $> 0$ |
| $\hat{\zeta}$ | Dimensionless bulk viscosity | $\geq 0$ |
| $\hat{V} = \frac{4}{3}\hat{\eta} + \hat{\zeta}$ | Combined viscosity | $> 0$ |

**IMPORTANT**: Distinguish $\hat{\epsilon}$ (dynamical field) from $\hat{\eta}$, $\hat{\zeta}$ etc. (parameters) by context.

---

## 6. Transport Coefficients

| Symbol | Name | Definition |
|---|---|---|
| $\eta = \hat{q}Lc_s^2\rho\hat{\eta}$ | Shear viscosity | Frame-independent |
| $\zeta = \hat{q}Lc_s^2\rho\hat{\zeta}$ | Bulk viscosity | Frame-independent |
| $\tau_\epsilon = \hat{V}L$ | Energy relaxation time | Frame-dependent |
| $\tau_p = \hat{s}c_s^2L\hat{V}$ | Pressure relaxation time | Frame-dependent |
| $\tau_Q = \hat{a}L\hat{V}$ | Heat flux relaxation time | Frame-dependent |
| $\beta_\epsilon = c_s^2\hat{a}\hat{V}L = c_s^2\tau_Q$ | Heat flux coefficient | Frame-dependent |

---

## 7. BDNK Stress-Energy Components

| Symbol | Definition |
|---|---|
| $\mathcal{A}$ | Energy correction (scalar) |
| $\Pi$ | Bulk pressure correction (scalar) |
| $\mathcal{Q}^\mu$ | Heat flux (4-vector) |
| $\sigma^{\mu\nu}$ | Shear tensor (traceless symmetric) |
| $\Delta^{\mu\nu} = g^{\mu\nu} + u^\mu u^\nu$ | Projector orthogonal to $u^\mu$ |

---

## 8. Conservative/Primitive Variable Sets

| Set | Symbol | Contents |
|---|---|---|
| $\mathbf{p}_0$ | Primitive (type 0) | $(\epsilon, v^i)$ or $(\epsilon, \tilde{v}^r)$ |
| $\mathbf{p}_1$ | Primitive (type 1) | $(\hat{\epsilon}, \hat{\bar{v}}^i)$ — recovered via con2prim |
| $\mathbf{q}$ | Conservative | $(\sqrt{\gamma}E, \sqrt{\gamma}S_i)$ or $(\tilde{\gamma}E, \tilde{\gamma}S_r)$ |

Evolved fields in spherical symmetry: $\{\tilde{\gamma}E, \tilde{\gamma}S_r, \epsilon, \partial_r\epsilon, \tilde{v}^r, \partial_r\tilde{v}^r\}$

---

## 9. Notation Conflicts (Disambiguation)

| Symbol | Context 1 | Context 2 | Rule |
|---|---|---|---|
| $a$ | $a(R)$: TOV metric function | $a_\mu$: normal acceleration | Always include index for acceleration |
| $\rho$ | $\epsilon + p$ (enthalpy) | $\rho_0$ (rest mass) | Use subscript 0 for rest mass |
| $\mathcal{A}$ | Scalar BDNK correction | $\mathcal{A}_i{}^j$ con2prim matrix | Matrix always has indices |
| $p$ | Pressure $p(\epsilon)$ | Convergence order | Specify in words for convergence |
| $\tau$ | QNM decay time | Transport relaxation times | Transport always has subscript |

---

## 10. Simulation Case Labels

| Label | $(\tau_\epsilon, \hat{\eta}, \hat{\zeta})$ |
|---|---|
| `smallSB-F2` | $(0.023, 0.01, 0.01)$ |
| `medS-F2` | $(0.023, 0.01725, 0)$ |
| `highB-F9` | $(0.092, 0.0015, 0.09)$ |
| `medSB-F9` | $(0.092, 0.03525, 0.045)$ |

---

## 11. Markdown Formatting Rules

- Inline math: `$...$` for variables in text
- Display equations: `$$...$$` on own line
- Thin spaces `\,` in products: $2\,\eta\,\sigma^{\mu\nu}$
- Fractions: `\frac{}{}` in display, `\tfrac{}{}` or `/` inline
- Case labels in backtick code: `` `smallSB-F2` ``
