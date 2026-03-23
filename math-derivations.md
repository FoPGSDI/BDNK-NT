# Mathematical Derivations: BDNK Viscous Hydrodynamics for Neutron Stars

## Preamble: Guidelines for These Notes

*Read this section whenever updating.*

### What These Notes Should Be

Treat this as a publishable derivation document, except:

- **Uncertainty is explicit** — use markers (`[HYPOTHESIS]`, `[PRELIMINARY]`, `[SOLID]`), not hedging prose
- **Gaps are visible** — mark them (`[BLOCKING]`, `[FUTURE]`), don't smooth over
- **Every algebraic step is shown** — no step-skipping; reader should be able to follow line by line
- **Sections can be unbalanced** — developed where we have results, skeletal where we don't
- **Abandoned paths are documented** — in appendix, not omitted

### Bidirectional Criterion

- **Forward:** Every marker, if resolved, should advance the document
- **Backward:** Every loose end should be captured by a marker

---

## 1. Ideal Fluid Foundation

### 1.1 Stress-Energy Tensor of Ideal Fluid

`[SOLID]` (ref: Paper Eq.1)

The stress-energy tensor of an ideal (non-conformal) fluid:

$$T^{\mu\nu} = \epsilon \, u^\mu \, u^\nu + p(\epsilon) \, \Delta^{\mu\nu}$$

where:
- $\epsilon$: total energy density
- $u^\mu$: four-velocity ($u_\mu u^\mu = -1$)
- $p = p(\epsilon)$: pressure (determined by EoS)
- $\Delta^{\mu\nu} = g^{\mu\nu} + u^\mu u^\nu$: projector orthogonal to $u^\mu$

### 1.2 Equations of Motion from Conservation Laws

`[SOLID]` (ref: Paper Eqs.3-5)

From $\nabla_\mu T^{\mu\nu} = 0$, projecting along and orthogonal to $u^\mu$:

**Energy equation** (projection along $u^\mu$):

$$u^\mu \nabla_\mu \epsilon + (\epsilon + p)(\nabla_\mu u^\mu) = 0$$

**Momentum equation** (projection orthogonal to $u^\mu$):

$$u^\nu \nabla_\nu u^\mu + \frac{p'(\epsilon)}{\epsilon + p} \Delta^{\mu\nu} \nabla_\nu \epsilon = 0$$

`[FUTURE: Provide explicit derivation of these projections step by step]`

---

## 2. BDNK Viscous Stress-Energy Tensor

### 2.1 First-Order Derivative Expansion

`[SOLID]` (ref: Paper Eq.6)

The BDNK viscous stress-energy tensor up to first order in derivatives:

$$T^{\mu\nu} = (\epsilon + \mathcal{A}) u^\mu u^\nu + (p + \Pi) \Delta^{\mu\nu} + \mathcal{Q}^\mu u^\nu + u^\mu \mathcal{Q}^\nu - 2\eta \sigma^{\mu\nu}$$

### 2.2 Viscous Correction Terms

`[SOLID]` (ref: Paper unnumbered eqs after Eq.6)

$$\mathcal{A} = \tau_\epsilon \left[ u^\mu \nabla_\mu \epsilon + (\epsilon + p)(\nabla_\mu u^\mu) \right]$$

$$\Pi = -\zeta \nabla_\mu u^\mu + \tau_p \left[ u^\mu \nabla_\mu \epsilon + (\epsilon + p)(\nabla_\mu u^\mu) \right]$$

$$\mathcal{Q}^\mu = \tau_Q (\epsilon + p) u^\nu \nabla_\nu u^\mu + \beta_\epsilon \Delta^{\mu\nu} \nabla_\nu \epsilon$$

### 2.3 Shear Tensor

`[SOLID]` (ref: Paper Eq.7)

$$\sigma^{\mu\nu} = \frac{1}{2}\left[\Delta^{\mu\alpha}\Delta^{\nu\beta}(\nabla_\alpha u_\beta + \nabla_\beta u_\alpha) - \frac{2}{3}\Delta^{\mu\nu}\Delta^{\alpha\beta}\nabla_\alpha u_\beta\right]$$

### 2.4 Special Frame Choice: $\beta_\epsilon = \tau_Q p'(\epsilon)$

`[SOLID]` (ref: Paper Eq.8)

Choosing $\beta_\epsilon = \tau_Q p'(\epsilon)$ makes $\mathcal{Q}^\mu$ proportional to the ideal EoM:

$$\mathcal{Q}^\mu = \tau_Q \left[(\epsilon + p) u^\nu \nabla_\nu u^\mu + p'(\epsilon) \Delta^{\mu\nu} \nabla_\nu \epsilon \right]$$

`[FUTURE: Show explicitly why this is proportional to the zeroth-order EoM Eq.5]`

### 2.5 Transport Coefficients

`[SOLID]` (ref: Paper discussion after Eq.8)

| Coefficient | Name | Role | Frame-dependent? |
|---|---|---|---|
| $\eta$ | Shear viscosity | Physical dissipation | No (at this order) |
| $\zeta$ | Bulk viscosity | Physical dissipation | No (at this order) |
| $\tau_\epsilon$ | Relaxation time | Dissipation timescale | Yes |
| $\tau_p$ | Relaxation time | Dissipation timescale | Yes |
| $\tau_Q$ | Relaxation time | Heat flux timescale | Yes |
| $\beta_\epsilon$ | Heat flux coeff. | Energy density contribution to heat flux | Yes |

---

## 3. 3+1 Decomposition

### 3.1 Metric Decomposition

`[SOLID]` (ref: Paper Eq.9)

$$ds^2 = -\alpha^2 dt^2 + \gamma_{ij}(dx^i + \beta^i dt)(dx^j + \beta^j dt)$$

where $\alpha$ is the lapse, $\beta^i$ the shift, $\gamma_{ij}$ the induced spatial metric.

Normal vector: $n_\mu = -\alpha (dt)_\mu$, with $n^\mu = \frac{1}{\alpha}(\partial_t^\mu - \beta^i \partial_i^\mu)$.

Induced metric: $\gamma_{\mu\nu} = g_{\mu\nu} + n_\mu n_\nu$

Extrinsic curvature: $K_{\mu\nu} = -\frac{1}{2}\mathcal{L}_n \gamma_{\mu\nu} = -(\nabla_\mu n_\nu + n_\mu a_\nu)$

where $a_\mu = n^\nu \nabla_\nu n_\mu$ (acceleration, spatial: $n^\mu a_\mu = 0$).

### 3.2 Fluid Velocity Decomposition

`[SOLID]` (ref: Paper Eqs.10-12)

$$u^\mu = W(n^\mu + v^\mu), \quad W = \frac{1}{\sqrt{1 - \gamma_{ij} v^i v^j}}$$

with $v^t = 0$, $v^i = \frac{1}{\alpha}\left(\frac{u^i}{u^t} + \beta^i\right)$.

### 3.3 Stress-Energy Projections

`[SOLID]` (ref: Paper Eqs.13-14)

$$T^{\mu\nu} = E n^\mu n^\nu + S^\mu n^\nu + n^\mu S^\nu + S^{\mu\nu}$$

where:
- $E = n_\mu n_\nu T^{\mu\nu}$ — energy density
- $S^\mu = -\gamma^\mu_{\ \alpha} n_\beta T^{\alpha\beta}$ — momentum density
- $S^{\mu\nu} = \gamma^\mu_{\ \alpha} \gamma^\nu_{\ \beta} T^{\alpha\beta}$ — stress tensor

### 3.4 Balance Laws

`[SOLID]` (ref: Paper Eqs.15-16)

$$\partial_t(\sqrt{\gamma} E) + \partial_i[\sqrt{\gamma}(\alpha S^i - \beta^i E)] = \alpha\sqrt{\gamma}(S^{ij} K_{ij} - S^i \partial_i \ln\alpha)$$

$$\partial_t(\sqrt{\gamma} S_j) + \partial_i[\sqrt{\gamma}(\alpha S^i_{\ j} - \beta^i S_j)] = \alpha\sqrt{\gamma}\left(\frac{1}{2} S^{ik}\partial_j \gamma_{ik} + \frac{1}{\alpha} S_i \partial_j \beta^i - E \partial_j \ln\alpha\right)$$

Conservative variables: $\mathbf{q} = (\sqrt{\gamma} E, \sqrt{\gamma} S_i)$

### 3.5 First-Order Reduction in Time

`[SOLID]` (ref: Paper Eqs.17-21)

Define:
$$\hat{\epsilon} = -n^\mu \nabla_\mu \epsilon$$

$$\hat{\bar{v}}^\mu = \gamma^\mu_{\ \alpha}(-n^\nu \nabla_\nu v^\alpha)$$

Evolution equations in 3+1 form:
$$(\partial_t - \beta^j \partial_j)\epsilon = -\alpha \hat{\epsilon}$$

$$(\partial_t - \beta^j \partial_j)v^i = \alpha(-\hat{\bar{v}}^i + K^i_{\ j} v^j) - v^j \partial_j \beta^i$$

Primitive variables: $\mathbf{p}_0 = (\epsilon, v^i)$ and $\mathbf{p}_1 = (\hat{\epsilon}, \hat{\bar{v}}^i)$.

### 3.6 Full 3+1 Decomposition of E, S^i, S_{ij}

`[PRELIMINARY]` (ref: Paper Eqs.22-28)

`[FUTURE: Write out full step-by-step derivation of Eqs.22-28 from the viscous stress-energy tensor and the 3+1 projections. This is the most algebraically intensive part of the paper.]`

**Energy density E** (Eq.22):

$$E = W^2\epsilon - p(1 - W^2) + \text{[viscous terms involving } \tau_\epsilon, \tau_p, \tau_Q, \eta, \zeta\text{]}$$

`[FUTURE: Full explicit expression with all viscous terms expanded]`

**Momentum density S^i** (Eq.23):

$$S^i = -v^i W^2(\epsilon + p) + \text{[viscous correction terms]}$$

`[FUTURE: Full explicit expression]`

**Stress tensor S_{ij}** (Eq.24):

$$S_{ij} = p\gamma_{ij} + W^2(\epsilon + p)v_i v_j + \text{[viscous correction terms]}$$

`[FUTURE: Full explicit expression]`

---

## 4. Spherical Symmetry Reduction

### 4.1 Metric Ansatz

`[SOLID]` (ref: Paper Eq.25)

$$ds^2 = -\alpha(t,r)^2 dt^2 + g_{rr}(t,r)dr^2 + r^2 g_{\theta\theta}(t,r)(d\theta^2 + \sin^2\theta\, d\varphi^2)$$

### 4.2 First-Order Reduction Variables

`[SOLID]` (ref: Paper Eq.26)

$$A_r = \frac{1}{\alpha}\partial_r \alpha, \quad D_{rr}^{\ r} = \frac{1}{2}g^{rr}\partial_r g_{rr}, \quad D_{r\theta}^{\ \theta} = \frac{1}{2}g^{\theta\theta}\partial_r g_{\theta\theta}$$

### 4.3 Evolution Equations in Spherical Symmetry

`[SOLID]` (ref: Paper Eqs.27-30)

$$\partial_t(\tilde{\gamma} E) + \partial_r(\alpha \tilde{\gamma} S^r) = \alpha\tilde{\gamma}\left[S^r_{\ r} K^r_{\ r} + 2S^\theta_{\ \theta} K^\theta_{\ \theta} - S^r\left(\frac{2}{r} + A_r\right)\right]$$

$$\partial_t(\tilde{\gamma} S_r) + \partial_r(\alpha \tilde{\gamma} S^r_{\ r}) = \alpha\tilde{\gamma}\left[S^r_{\ r}(D_{rr}^r - \frac{2}{r}) + 2S^\theta_{\ \theta}\left(\frac{1}{r} + D_{r\theta}^\theta\right) - E A_r\right]$$

$$\partial_t \epsilon = -\alpha \hat{\epsilon}$$

$$\partial_t v^r = \alpha(-\hat{\bar{v}}^r + K^r_{\ r} v^r)$$

where $\tilde{\gamma} = \sqrt{g_{rr}} g_{\theta\theta}$.

### 4.4 Regularized Velocity and Promoted Derivatives

`[SOLID]` (ref: Paper Eqs.31-34)

Regularized velocity: $\tilde{v}^r = \frac{1}{r}v^r$

$$\partial_t \tilde{v}^r = \alpha\left(-\frac{\hat{\bar{v}}^r}{r} + K^r_{\ r} \tilde{v}^r\right)$$

Promoted spatial derivatives (evolved as dynamical fields):
$$\partial_t(\partial_r \epsilon) = -\partial_r(\alpha \hat{\epsilon})$$

$$\partial_t(\partial_r \tilde{v}^r) = \partial_r\left[\alpha\left(-\frac{\hat{\bar{v}}^r}{r} + K^r_{\ r} \tilde{v}^r\right)\right]$$

**Final evolved variables:** $\{\tilde{\gamma} E, \tilde{\gamma} S_r, \epsilon, \partial_r \epsilon, \tilde{v}^r, \partial_r \tilde{v}^r\}$

---

## 5. Equation of State

### 5.1 Definitions

`[SOLID]` (ref: Paper Eqs.35-38)

Total energy density: $\epsilon = \rho_0(1 + \epsilon_0)$

Polytropic EoS: $p = \kappa \rho_0^\Gamma$ with $\kappa = 100$, $\Gamma = 2$

Ideal gas EoS: $p = (\Gamma - 1)\epsilon_0 \rho_0$

### 5.2 Derivation of Combined EoS

`[SOLID]` (ref: Paper Eq.39)

**Step 1:** From polytropic EoS: $\rho_0 = (p/\kappa)^{1/\Gamma}$

**Step 2:** From ideal gas EoS: $\epsilon_0 \rho_0 = p/(\Gamma - 1)$

**Step 3:** Substitute into $\epsilon = \rho_0 + \epsilon_0 \rho_0$:

$$\epsilon = \left(\frac{p}{\kappa}\right)^{1/\Gamma} + \frac{p}{\Gamma - 1}$$

**Step 4:** For $\Gamma = 2$:

$$\epsilon = \left(\frac{p}{\kappa}\right)^{1/2} + p = \frac{\sqrt{p}}{\sqrt{\kappa}} + p$$

**Step 5:** Let $x = \sqrt{p}$, then $\epsilon = x/\sqrt{\kappa} + x^2$, giving quadratic:

$$x^2 + \frac{x}{\sqrt{\kappa}} - \epsilon = 0$$

**Step 6:** Solve: $x = \frac{-1/\sqrt{\kappa} \pm \sqrt{1/\kappa + 4\epsilon}}{2}$

**Step 7:** Since $p = x^2$ and requiring $p(\epsilon = 0) = 0$, take the appropriate root:

$$p(\epsilon) = \frac{1 + 2\epsilon\kappa - \sqrt{1 + 4\epsilon\kappa}}{2\kappa}$$

`[VERIFIED]` matches Paper Eq.39.

---

## 6. Initial Data: TOV Equations

### 6.1 Static Metric

`[SOLID]` (ref: Paper Eq.40)

$$ds^2 = -\alpha^2(R) dt^2 + a^2(R) dR^2 + R^2 d\Omega^2$$

### 6.2 TOV System

`[SOLID]` (ref: Paper Eqs.43-45)

$$\frac{da}{dR} = \frac{1 + a^2(-1 + 8\pi R^2 \epsilon)}{2R}a$$

$$\frac{d\alpha}{dR} = \frac{-1 + a^2(1 + 8\pi R^2 p)}{2R}\alpha$$

$$\frac{dp}{dR} = -\frac{(p + \epsilon)}{\alpha}\frac{d\alpha}{dR}$$

Boundary conditions: $\alpha(0) = 1$, $a(0) = 1$, $p(0) = \kappa\rho_0(0)^\Gamma$

### 6.3 Coordinate Transformation to Maximal Isotropic

`[SOLID]` (ref: Paper Eq.47)

$$ds^2 = -\alpha^2(r)dt^2 + \psi^4(r)(dr^2 + r^2 d\Omega^2)$$

`[FUTURE: Detail the coordinate transformation procedure from areal-polar to maximal isotropic coordinates]`

---

## 7. Frame Choice and Well-Posedness Conditions

### 7.1 Parametrization

`[SOLID]` (ref: Paper Eqs.48-50)

Define $\rho \equiv \epsilon + p$, $V \equiv \frac{4}{3}\eta + \zeta$, and:

| Parameter | Definition |
|---|---|
| $\eta$ | $\hat{q} L c_s^2 \rho \hat{\eta}$ |
| $\zeta$ | $\hat{q} L c_s^2 \rho \hat{\zeta}$ |
| $\tau_p$ | $\hat{s} c_s^2 L \hat{V}$ |
| $\tau_Q$ | $\hat{a} L \hat{V}$ |
| $\tau_\epsilon$ | $\hat{V} L$ |
| $\beta_\epsilon$ | $c_s^2 \hat{a} \hat{V} L$ |

with $\hat{\zeta} \geq 0$ and $\hat{a}, \hat{q}, \hat{s}, L, c_s, \hat{\eta}, \hat{V} > 0$.

### 7.2 Characteristic Velocities

`[SOLID]` (ref: Paper Eqs.51-52)

$$c_0 = c_s \sqrt{\frac{\hat{q}\hat{\eta}}{\hat{a}\hat{V}}}$$

$$c_\pm = c_s \sqrt{\frac{\hat{a}(1 + \hat{s}) + \hat{q} \pm \sqrt{\hat{q}^2 + \hat{a}^2(4\hat{q} + (\hat{s}-1)^2) + 2\hat{a}\hat{q}(1+\hat{s})}}{2\hat{a}}}$$

### 7.3 Well-Posedness Conditions

`[SOLID]` (ref: Paper Eqs.53-56)

1. **Strong hyperbolicity:** $0 < \hat{q} < \hat{s}$ (ensures $c_-$ is real and $c_+ \neq c_-$)
2. **Causality:** $\hat{q} < \frac{(1-c_s^2)}{c_s^2}\frac{(1-\hat{s}c_s^2)}{(c_s^2 + \hat{a}^{-1})}$ and $\hat{s} < \frac{1}{c_s^2}$
3. **Linear stability:** Same as condition 1 (verified analytically via Mathematica)

### 7.4 Characteristic Velocities on Curved Background

`[SOLID]` (ref: Paper Eq.57)

$$\tilde{c}_{i_\pm} = -\beta \cdot k + \alpha \frac{m_i W^2(v \cdot k) \pm \sqrt{k^2 + k^2 m_i W^2 - m_i W^2(v \cdot k)^2}}{m_i W^2 + 1}$$

where $m_0 = (1/c_0^2 - 1)$, $m_{1,2} = (1/c_\pm^2 - 1)$.

---

## 8. Primitive Variable Recovery (con2prim)

### 8.1 Linear System Formulation

`[SOLID]` (ref: Paper Appendix A, Eq.A1)

The conservative variables can be written as linear in $\mathbf{p}_1$:

$$\begin{pmatrix} E \\ S_i \end{pmatrix} = \begin{pmatrix} \mathcal{A}_0^{\ 0} & \mathcal{A}_0^{\ j} \\ \mathcal{A}_i^{\ 0} & \mathcal{A}_i^{\ j} \end{pmatrix} \begin{pmatrix} \hat{\epsilon} \\ \hat{\bar{v}}_j \end{pmatrix} + \begin{pmatrix} c_0 \\ c_i \end{pmatrix}$$

### 8.2 Matrix Components

`[SOLID]` (ref: Paper Appendix A, Eqs.A2-A5)

`[FUTURE: Write out full expressions for A matrix components with step-by-step derivation]`

### 8.3 Spherically Symmetric Case

`[SOLID]` (ref: Paper Appendix A, Eqs.A8-A11)

The 2×2 system with explicit matrix components.

`[FUTURE: Show full derivation of the spherically symmetric con2prim]`

---

## Appendix

### Abandoned Approaches

[None yet]

### Notation Index

| Symbol | Meaning |
|---|---|
| $\epsilon$ | Total energy density |
| $p$ | Pressure |
| $u^\mu$ | Four-velocity |
| $\Delta^{\mu\nu}$ | Projector $g^{\mu\nu} + u^\mu u^\nu$ |
| $\alpha$ | Lapse function |
| $\beta^i$ | Shift vector |
| $\gamma_{ij}$ | Spatial metric |
| $n^\mu$ | Unit normal to spatial hypersurface |
| $W$ | Lorentz factor |
| $v^i$ | Spatial velocity |
| $E$ | Projected energy density |
| $S^i$ | Projected momentum density |
| $S^{ij}$ | Projected stress tensor |
| $K_{ij}$ | Extrinsic curvature |
| $\hat{\epsilon}$ | Time derivative reduction of $\epsilon$ |
| $\hat{\bar{v}}^i$ | Spatial time derivative reduction of $v^i$ |
| $\tilde{v}^r$ | Regularized radial velocity $v^r/r$ |
| $\tilde{\gamma}$ | $\sqrt{g_{rr}} g_{\theta\theta}$ |
