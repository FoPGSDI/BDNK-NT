# Mathematical Conventions Document

## Reference

All conventions derive from: Pandya, Most, Pretorius, "Causal, stable first-order viscous relativistic hydrodynamics with ideal gas microphysics" (paper.tex).

---

## 1. Notation Table

### 1.1 Thermodynamic / Fluid Variables

| Symbol | LaTeX | Meaning | Notes |
|--------|-------|---------|-------|
| $\epsilon$ | `\epsilon` | Energy density | Literature alternative: $e$ |
| $e$ | `e` | Specific internal energy, $e \equiv U/(mN)$ | Literature alternative: $\epsilon$ |
| $P$ | `P` | Isotropic (equilibrium) pressure | Literature alternative: $p$; $P = P(\epsilon, n)$ defines EOS |
| $\rho$ | `\rho` | Energy density + pressure, $\rho \equiv \epsilon + P$ | Literature alternative: sometimes used for rest mass density |
| $n$ | `n` | Baryon number density | |
| $m$ | `m` | Particle rest mass | |
| $mn$ | `mn` | Rest mass density | Literature alternative: $\rho$ |
| $T$ | `T` | Temperature | $T(\epsilon, n)$ |
| $\mu$ | `\mu` | Relativistic chemical potential, $\mu \equiv \mu_N + m$ | |
| $\mu_N$ | `\mu_N` | Newtonian chemical potential | |
| $s$ | `s` | Entropy density, $s \equiv S/V$ | Literature alternatives: $\tilde{s}, \bar{s}$ |
| $\bar{s}$ | `\bar{s}` | Entropy per particle, $\bar{s} \equiv S/N$ | Literature alternatives: $s, \tilde{s}$ |
| $\Gamma$ | `\Gamma` | Adiabatic index, $\Gamma \in (1,2)$ | Literature alternative: $\gamma$ |
| $u^a$ | `u^a` | Timelike flow four-velocity, $u_c u^c = -1$ | |
| $v$ | `v` | Three-velocity (in the $x$-direction for shockwaves) | $v \in [0,1)$ |
| $W$ | `W` | Lorentz factor, $W \equiv (1 - v^2)^{-1/2}$ | |

### 1.2 Tensors and Projectors

| Symbol | LaTeX | Meaning |
|--------|-------|---------|
| $g_{ab}$ | `g_{ab}` | Spacetime metric, signature $(-+++)$ |
| $\Delta^{ab}$ | `\Delta^{ab}` | Spatial projector, $\Delta^{ab} \equiv g^{ab} + u^a u^b$ |
| $T^{ab}$ | `T^{ab}` | Stress-energy tensor (full, including dissipative corrections) |
| $T^{ab}_0$ | `T^{ab}_0` | Perfect fluid (ideal) stress-energy tensor |
| $J^a$ | `J^a` | Baryon current |
| $J^a_0$ | `J^a_0` | Perfect fluid baryon current, $J^a_0 = n u^a$ |
| $\sigma^{ab}$ | `\sigma^{ab}` | Shear tensor, $\sigma^{ab} \equiv \nabla^{\langle a} u^{b \rangle}$ |
| $X^{\langle ab \rangle}$ | `X^{<ab>}` | Traceless transverse-to-$u^a$ projection of rank-2 tensor |

### 1.3 Script Quantities (Projections of Conserved Currents)

| Symbol | LaTeX | Meaning | Definition |
|--------|-------|---------|------------|
| $\mathcal{E}$ | `\mathcal{E}` | Energy density projection | $\mathcal{E} = u_a u_b T^{ab}$ |
| $\mathcal{P}$ | `\mathcal{P}` | Pressure projection | $\mathcal{P} = \frac{1}{3}\Delta_{ab} T^{ab}$ |
| $\mathcal{Q}^a$ | `\mathcal{Q}^a` | Heat flux vector | $\mathcal{Q}^a = -\Delta^{ab} u^c T_{bc}$ |
| $\mathcal{T}^{ab}$ | `\mathcal{T}^{ab}` | Traceless symmetric stress | $\mathcal{T}^{ab} = T^{\langle ab \rangle}$ |
| $\mathcal{N}$ | `\mathcal{N}` | Baryon density projection | $\mathcal{N} = -u_a J^a$ |
| $\mathcal{J}^a$ | `\mathcal{J}^a` | Baryon diffusion current | $\mathcal{J}^a = \Delta^{ab} J_b$ |

### 1.4 Differential Operators and Coordinates

| Symbol | LaTeX | Meaning |
|--------|-------|---------|
| $\nabla_a$ | `\nabla_a` | Covariant derivative |
| $\dot{X}$ | `\dot{X}` | Time derivative, $\dot{X} \equiv \partial_t X$ |
| $X'$ | `X'` | Spatial derivative, $X' \equiv \partial_x X$ |
| $X_{,i}$ | `X_{,i}` | Partial spatial derivative, $X_{,i} \equiv \partial_i X$ |
| $\tau$ (Milne) | `\tau` | Milne proper time, $\tau \equiv \sqrt{t^2 - z^2}$ |
| $\xi$ | `\xi` | Milne rapidity, $\xi \equiv \mathrm{arctanh}(z/t)$ |

### 1.5 Dimensionless Ratios and Derived Quantities

| Symbol | LaTeX | Definition | Meaning |
|--------|-------|------------|---------|
| $c_s^2$ | `c_s^2` | $c_s^2 \equiv \left(\frac{\partial P}{\partial \epsilon}\right)_{\bar{s}} = \frac{\Gamma P}{\rho}$ | Sound speed squared |
| $\mathrm{Kn}$ | `\Kn` or `\mathrm{Kn}` | $\mathrm{Kn} \equiv \ell / L$ | Knudsen number |
| $\mathrm{Re}$ | `\Ren` or `\mathrm{Re}` | $\mathrm{Re} \equiv \hat{V}^{-1}$ | Effective Reynolds number |
| $\alpha$ | `\alpha` | $\alpha \equiv \frac{p'_\epsilon}{c_s^2} = \frac{\Gamma - 1}{c_s^2}$ | Dimensionless ratio |
| $\omega$ | `\omega` | $\omega \equiv \frac{\kappa_s}{\kappa_\epsilon} = \frac{m n P}{\epsilon \rho}$ | Dimensionless ratio |

### 1.6 Characteristic Speeds

| Symbol | LaTeX | Meaning |
|--------|-------|---------|
| $c_+$ | `c_+` | Largest BDNK characteristic speed |
| $c_-$ | `c_-` | Smaller nonzero BDNK characteristic speed |
| $c_1$ | `c_1` | Third BDNK characteristic speed, $c_1^2 = c_s^2 \frac{\eta}{V \hat{\tau}}$ |

**Disambiguation note on $c_1$:** The symbol $c_1$ denotes the BDNK shear-mode characteristic speed throughout our documentation. In the paper's MIS comparison (Sec. 10 below), a coefficient also called $c_1$ appears in the MIS relaxation equation $\dot{\epsilon} = (T^{tt} - \epsilon)/(\tau_\pi + c_1)$; in that context the paper inherits the notation from the MIS literature. To avoid confusion, write $c_{1,\text{MIS}}$ when referring to the MIS coefficient. Additionally, do **not** use $c_1, c_2$ as generic integration constants; use $C_1, C_2$ instead.

### 1.7 MIS-Specific Symbols (for Comparison Only)

| Symbol | LaTeX | Meaning |
|--------|-------|---------|
| $\tau_\pi$ | `\tau_\pi` | MIS shear relaxation time |
| $\pi^{ab}$ | `\pi^{ab}` | MIS dissipative tensor |
| $\pi^{ab}_{\text{NS}}$ | `\pi^{ab}_{\text{NS}}` | Navier-Stokes (first-order) viscous tensor target for MIS relaxation |
| $I^{ab}$ | `I^{ab}` | MIS higher-order transport terms (second-order gradient contributions) |
| $c_{1,\text{MIS}}$ | `c_{1,\text{MIS}}` | MIS coefficient appearing in $\tau_\epsilon^{\text{MIS}} = \tau_\pi + c_{1,\text{MIS}}$ |

### 1.8 Miscellaneous

| Symbol | LaTeX | Meaning |
|--------|-------|---------|
| $\delta\epsilon$ | `\delta\epsilon` | Out-of-equilibrium energy density correction |
| $\mathrm{erf}(y)$ | `\mathrm{erf}(y)` | Gaussian error function |
| $Q_N$ | `Q_N` | Convergence factor, $Q_N = \|R_{N/2}\| / \|R_N\|$ |
| $R_N$ | `R_N` | Discrete residual at resolution $N$ |
| $\lambda$ | `\lambda` | CFL number, $\lambda \equiv \Delta t / \Delta x$ |
| $w$ | `w` | Width parameter for initial data profiles |
| $L$ | `L` | Characteristic lengthscale (set to $L=1$ in the paper) |
| $n_0$ | `n_0` | Initial baryon density at $\tau = 1$ for Bjorken flow ($n_0 = 0.1$ in the paper) |
| $\epsilon_0$ | `\epsilon_0` | Initial energy density at $\tau = 1$ for Bjorken flow ($\epsilon_0 = 0.25$ in the paper) |
| $\dot{\epsilon}_0$ | `\dot{\epsilon}_0` | Initial $\dot{\epsilon}$ at $\tau = 1$ for Bjorken flow |
| $e_0$ | `e_0` | Integration constant in the inviscid Bjorken solution, determined by initial data |
| $\tau_\theta$ | `\tau_\theta` | Pressure relaxation timescale in heat flow, $\tau_\theta \equiv \theta / n$ |
| $C_1, C_2$ | `C_1, C_2` | Generic integration constants (do NOT use $c_1, c_2$ to avoid collision with characteristic speed $c_1$) |

---

## 2. Markdown Math Formatting Rules

### 2.1 Inline vs. Display Math

- **Inline math**: Use single dollar signs `$...$` for symbols, short expressions, and variable references within prose.
  - Example: `The energy density $\epsilon$ satisfies $\epsilon > 0$.`
- **Display math**: Use double dollar signs `$$...$$` for standalone equations, multi-line derivations, and any expression that should be visually prominent.
  - Example:
    ```
    $$
    T^{ab}_0 = \epsilon u^a u^b + P \Delta^{ab}
    $$
    ```
- **Multi-line display math**: Use `$$\begin{aligned}...\end{aligned}$$` for aligned multi-line equations.
  - Example:
    ```
    $$
    \begin{aligned}
    \nabla_a T^{ab} &= 0 \\
    \nabla_a J^a &= 0
    \end{aligned}
    $$
    ```

### 2.2 Equation Labeling

Label important equations with an HTML anchor immediately before the display math block:

```
<a id="eq:EOS"></a>
$$
P(\epsilon, n) = [\Gamma - 1]\, m n\, e(\epsilon, n) = n\, T(\epsilon, n)
$$
```

When labeling, use the **same label name as the paper** whenever the equation comes directly from the paper (e.g., `eq:EOS`, `eq:Tab_0`, `eq:hydro_frame`). For new equations not in the paper, use descriptive names with underscores (e.g., `eq:discrete_flux`).

### 2.3 Cross-Referencing Equations

- **Within the same markdown file**: Use markdown anchor links: `[Eq. (EOS)](#eq:EOS)`
- **Across markdown files**: Use relative links: `[Eq. (EOS)](derivations.md#eq:EOS)`
- **Referencing the paper**: Use the format `(ref: paper Eq. XX)` where XX is the equation number from the published paper or the `\label` tag. Example: `(ref: paper Eq. 14)` or `(ref: paper \ref{eq:EOS})`.

---

## 3. Index Conventions

### 3.1 Spacetime Indices

- **Letters used**: $\{a, b, c, d, e\}$
- **Range**: 0, 1, 2, 3 (or equivalently $t, x, y, z$)
- **Einstein summation convention**: Repeated upper-lower index pairs are summed over.

### 3.2 Spatial Indices

- **Letters used**: $\{i, j, k\}$
- **Range**: 1, 2, 3 (or equivalently $x, y, z$)

### 3.3 Metric Signature

$$
\text{Signature:} \quad (-+++)
$$

- Minkowski metric: $\eta_{ab} = \mathrm{diag}(-1, +1, +1, +1)$
- Flow velocity normalization: $u_c u^c = -1$ (timelike)
- Spatial projector: $\Delta^{ab} = g^{ab} + u^a u^b$ satisfies $\Delta^{ab} u_b = 0$

### 3.4 Milne Coordinates (for Bjorken flow)

- Coordinates: $x^a = (\tau, x, y, \xi)$
- Metric: $g_{ab} = \mathrm{diag}(-1, 1, 1, \tau^2)$
- Nonzero Christoffel symbols: $\Gamma^\xi_{\tau\xi} = \Gamma^\xi_{\xi\tau} = 1/\tau$, $\Gamma^\tau_{\xi\xi} = \tau$
- Metric determinant: $\sqrt{|g|} = \tau$
- Flow velocity (Bjorken): $u^a = (1, 0, 0, 0)^T$

---

## 4. Shorthand Definitions

### 4.1 Core Shorthands

| Shorthand | Definition | Where Defined |
|-----------|------------|---------------|
| $\rho$ | $\rho \equiv \epsilon + P$ | paper Eq. (rho) |
| $V$ | $V \equiv \frac{4\eta}{3} + \zeta$ | paper Eq. (V) |
| $\hat{V}$ | $\hat{V} \equiv \frac{V}{\rho c_s^2 L} \equiv \mathrm{Re}^{-1}$ | paper Eq. (Vhat_defn) |

### 4.2 EOS-Derived Shorthands

| Shorthand | Definition | For Ideal Gas |
|-----------|------------|---------------|
| $p'_\epsilon$ | $p'_\epsilon \equiv \left(\frac{\partial P}{\partial \epsilon}\right)_n$ | $\Gamma - 1$ |
| $p'_n$ | $p'_n \equiv \left(\frac{\partial P}{\partial n}\right)_\epsilon$ | $-(\Gamma - 1) m$ |
| $\kappa_\epsilon$ | $\kappa_\epsilon \equiv \frac{\rho^2 T}{n}\left(\frac{\partial(\mu/T)}{\partial \epsilon}\right)_n$ | $-(\Gamma-1)\frac{\epsilon \rho^2}{n^2 P}$ |
| $\kappa_n$ | $\kappa_n \equiv \rho T \left(\frac{\partial(\mu/T)}{\partial n}\right)_\epsilon$ | $\frac{\rho}{n^2 P}[(\Gamma-1)\epsilon^2 + P^2]$ |
| $\kappa_s$ | $\kappa_s \equiv \kappa_\epsilon + \kappa_n$ | $-(\Gamma-1)m\frac{\rho}{n}$ |
| $\alpha$ | $\alpha \equiv p'_\epsilon / c_s^2$ | $(\Gamma-1)/c_s^2$ |
| $\omega$ | $\omega \equiv \kappa_s / \kappa_\epsilon$ | $mnP/(\epsilon\rho)$ |

### 4.3 Heat Flow Shorthands

| Shorthand | Definition |
|-----------|------------|
| $\kappa$ | $\kappa \equiv \frac{\sigma \rho^2}{n^2 T}$ (thermal conductivity coefficient) |
| $\gamma$ | $\gamma \equiv \tau_Q + \frac{\sigma \rho}{n^2}$ |
| $\alpha_E$ | $\alpha_E \equiv \frac{\kappa(\Gamma-1)}{n}$ (Eckart thermal diffusivity) |
| $c_h^2$ | $c_h^2 \equiv \frac{\kappa(\Gamma-1)}{n\tau_\epsilon}$ (hybrid thermal propagation speed) |
| $c_B^2$ | $c_B^2 \equiv c_h^2\left(1 - \frac{\gamma n}{\kappa}\right)$ (BDNK thermal propagation speed) |
| $\theta$ | See Eq. (heat_theta_defn): frame-dependent constant in heat flow |

### 4.4 Causality/Stability Constraint Shorthands

| Shorthand | Definition |
|-----------|------------|
| $A$ | $A = \rho\,\tau_\epsilon\,\tau_Q$ |
| $B$ | $B = -\tau_\epsilon\left(\rho c_s^2 \tau_Q + V + \sigma\kappa_s\right) - \rho\,\tau_P\,\tau_Q$ |
| $C$ | $C = \tau_P(\rho c_s^2 \tau_Q + \sigma\kappa_s) - \beta_\epsilon V$ |
| $D$ | $D = \rho c_s^2(\tau_\epsilon + \tau_Q) + V + \sigma\kappa_\epsilon$ |
| $E$ | $E = \sigma(p'_\epsilon \kappa_s - c_s^2 \kappa_\epsilon)$ |
| $\hat{B}$ | $\hat{B} \equiv B / (\rho c_s^2 \tau_\epsilon \tau_Q)$ |
| $\hat{C}$ | $\hat{C} \equiv C / (\rho c_s^4 \tau_\epsilon \tau_Q)$ |
| $\hat{D}$ | $\hat{D} \equiv D / [\rho c_s^2 (\tau_\epsilon + \tau_Q)]$ |
| $\hat{E}$ | $\hat{E} \equiv E / [\rho c_s^4 (\tau_\epsilon + \tau_Q)]$ |

---

## 5. Transport Coefficient Conventions

### 5.1 The 8 Transport Coefficients

The BDNK conserved currents contain 8 transport coefficients, naturally grouped into three categories:

| Category | Coefficients | Role |
|----------|-------------|------|
| Relaxation times | $\tau_\epsilon,\; \tau_P,\; \tau_Q$ | Timescales over which dissipation impacts the solution |
| Physical dissipative coefficients | $\eta,\; \zeta,\; \sigma$ | Strength of dissipative effects (shear viscosity, bulk viscosity, thermal conductivity) |
| Heat flux coefficients | $\beta_\epsilon,\; \beta_n$ | Control contributions of $\nabla\epsilon$, $\nabla n$ to heat flux |

### 5.2 Physical Dissipative Coefficients

| Symbol | Name | Sign Constraint |
|--------|------|-----------------|
| $\eta$ | Shear viscosity | $\eta > 0$ |
| $\zeta$ | Bulk viscosity | $\zeta \geq 0$ |
| $\sigma$ | Thermal conductivity | $\sigma \geq 0$ |

### 5.3 Beta Coefficients (Derived)

$$
\begin{aligned}
\beta_\epsilon &= \tau_Q\, p'_\epsilon + \frac{\sigma}{\rho}\,\kappa_\epsilon \\
\beta_n &= \tau_Q\, p'_n + \frac{\sigma}{n}\,\kappa_n
\end{aligned}
$$

For the ideal gas:

$$
\begin{aligned}
\beta_\epsilon &= (\Gamma-1)\tau_Q - (\Gamma-1)\frac{\sigma\epsilon\rho}{n^2 P} \\
\beta_n &= -(\Gamma-1)m\,\tau_Q + \frac{\sigma\rho}{n^3 P}\left[(\Gamma-1)\epsilon^2 + P^2\right]
\end{aligned}
$$

### 5.4 Hydrodynamic Frame (Dimensionful Form)

The paper's chosen class of frames is defined by:

$$
\begin{aligned}
&\eta = \rho c_s^2 L\,\hat{\eta}, \quad \zeta = \rho c_s^2 L\,\hat{\zeta}, \quad \sigma = \frac{\hat{V}\,L\,\rho c_s^2}{(-\kappa_\epsilon)}\,\hat{\sigma} \\
&\tau_\epsilon = \tau_Q = L\hat{V}\,\hat{\tau}, \quad \tau_P = 2(\Gamma-1)L\hat{V}
\end{aligned}
$$

where all hatted quantities are dimensionless and $L > 0$ is a characteristic lengthscale (set to $L = 1$ in the paper).

### 5.5 Dimensionless (Hatted) Transport Coefficients

| Symbol | LaTeX | Meaning | Constraint |
|--------|-------|---------|------------|
| $\hat{\eta}$ | `\hat{\eta}` | Dimensionless shear viscosity | $\hat{\eta} > 0$ |
| $\hat{\zeta}$ | `\hat{\zeta}` | Dimensionless bulk viscosity | $\hat{\zeta} \geq 0$ |
| $\hat{\sigma}$ | `\hat{\sigma}` | Dimensionless thermal conductivity | $0 \leq \hat{\sigma} \leq 1/3$ (stability) |
| $\hat{\tau}$ | `\hat{\tau}` | Dimensionless relaxation time | $\hat{\tau} \geq \frac{(\Gamma-1)(2-c_s^2)+c_s^2}{1-c_s^2}$ (causality) |
| $\hat{V}$ | `\hat{V}` | Inverse Reynolds number | $\hat{V} = \frac{4\hat{\eta}/3 + \hat{\zeta}}{1}$ (from definition) |

### 5.6 BDNK Constraint Summary

**Causality** (simplified):

$$
\hat{\tau} \geq \frac{(\Gamma - 1)(2 - c_s^2) + c_s^2}{1 - c_s^2}
$$

**Linear stability** (simplified):

$$
\hat{\sigma} \leq \frac{1}{3}
$$

**Second law of thermodynamics**: $\eta, \zeta, \sigma \geq 0$.

**Full causality constraints** (CAUS A--D):

$$
\begin{aligned}
&\rho\,\tau_Q > \eta \tag{CAUS A} \\
&B^2 \geq 4AC \geq 0 \tag{CAUS B} \\
&2A > -B \geq 0 \tag{CAUS C} \\
&A > -B - C \tag{CAUS D}
\end{aligned}
$$

**Full linear stability constraints** (STAB A1--E): See paper Appendix A, Eqs. (STAB A1)--(STAB E).

### 5.7 Characteristic Speeds

$$
c_{\pm}^2 = \frac{c_s^2}{2\hat{\tau}}\left(2\alpha - \omega\hat{\sigma} + \hat{\tau} + 1 \pm \left[\omega\hat{\sigma}(4\alpha + \omega\hat{\sigma}) + (2\alpha+1)^2 - 2(\omega+2)\hat{\sigma} + \hat{\tau}^2 + \hat{\tau}(2 - 2\omega\hat{\sigma})\right]^{1/2}\right)
$$

$$
c_1^2 = c_s^2 \frac{\eta}{V\hat{\tau}}
$$

---

## 6. Equation Referencing Convention

### 6.1 Referencing Paper Equations

Use the format:

```
(ref: paper Eq. XX)
```

where `XX` is the equation number in the published paper. If the equation has a LaTeX label but no explicit number, use the label:

```
(ref: paper \eqref{eq:EOS})
```

Examples:
- `The equation of state (ref: paper Eq. 14)...`
- `The BDNK constitutive relations (ref: paper Eqs. 7--12)...`
- `The causality constraint (ref: paper Eq. 26)...`

### 6.2 Referencing Within Our Markdown Documents

Use HTML anchors for labeling and markdown links for referencing, as described in Section 2.

### 6.3 Referencing Paper Sections and Appendices

- `(ref: paper Sec. II)` for the Model section
- `(ref: paper Sec. III)` for the Results section
- `(ref: paper Sec. III.A)` for Trivial equilibrium states subsection
- `(ref: paper Sec. III.B)` for Bjorken flow subsection
- `(ref: paper Sec. III.C)` for Shockwaves subsection
- `(ref: paper Sec. III.D)` for Heat conduction subsection
- `(ref: paper Sec. IV)` for Conclusion
- `(ref: paper Appendix A)` for Deriving suitable hydrodynamic frames
- `(ref: paper Appendix B)` for Numerical algorithms and convergence tests

### 6.4 Key Equation Label Map

The following maps paper LaTeX labels to their content for convenient reference:

| Label | Content |
|-------|---------|
| `eq:Tab_cons_law` | $\nabla_a T^{ab} = 0$ |
| `eq:Ja_cons_law` | $\nabla_a J^a = 0$ |
| `eq:Tab_0` | Perfect fluid $T^{ab}_0 = \epsilon u^a u^b + P\Delta^{ab}$ |
| `eq:Ja_0` | Perfect fluid $J^a_0 = n u^a$ |
| `eq:gradient_exp` | Gradient expansion of $T^{ab}, J^a$ |
| `eq:Tab` | Decomposition of $T^{ab}$ w.r.t. $u^a$ |
| `eq:Ja` | Decomposition of $J^a$ w.r.t. $u^a$ |
| `eq:projections` | Definitions of $\mathcal{E}, \mathcal{P}, \mathcal{Q}^a, \mathcal{T}^{ab}, \mathcal{N}, \mathcal{J}^a$ |
| `eq:script_E` | BDNK $\mathcal{E}$ |
| `eq:script_P` | BDNK $\mathcal{P}$ |
| `eq:Q_a` | BDNK $\mathcal{Q}^a$ |
| `eq:script_T_ab` | BDNK $\mathcal{T}^{ab} = -2\eta\sigma^{ab}$ |
| `eq:script_N` | BDNK $\mathcal{N} = n$ |
| `eq:script_J_a` | BDNK $\mathcal{J}^a = 0$ |
| `eq:rho` | $\rho \equiv \epsilon + P$ |
| `eq:beta_eps`--`eq:kappa_s` | Definitions of $\beta_\epsilon, \beta_n, p'_\epsilon, p'_n, \kappa_\epsilon, \kappa_n, \kappa_s$ |
| `eq:EOS` | Gamma-law EOS: $P = [\Gamma-1]mne = nT$ |
| `eq:e_defn` | $\epsilon = mn(1+e)$ |
| `eq:Euler_relation` | Euler relation: $\rho = Ts + n\mu$ |
| `eq:S_over_V` | Entropy density $s(\epsilon, n)$ |
| `eq:mu` | Chemical potential $\mu(\epsilon, n)$ |
| `eq:cs_sq` | Sound speed: $c_s^2 = \Gamma P / \rho$ |
| `eq:omega` | $\omega = mnP/(\epsilon\rho)$ |
| `eq:alpha` | $\alpha = (\Gamma-1)/c_s^2$ |
| `eq:hydro_frame` | Hydrodynamic frame ansatz |
| `eq:V` | $V = 4\eta/3 + \zeta$ |
| `eq:Vhat_defn` | $\hat{V} = V/(\rho c_s^2 L) = \mathrm{Re}^{-1}$ |
| `eq:simple_constraints` | Simplified constraints: $\hat{\sigma} \leq 1/3$, $\hat{\tau} \geq ...$ |
| `eq:Bjorken_EOM` | Bjorken flow equation of motion |
| `eq:inviscid_bjorken` | Inviscid Bjorken solution |
| `eq:shockwave_nprime` | Shockwave baryon conservation |
| `eq:shockwave_epsP` | Shockwave $\epsilon'(x)$ equation |
| `eq:shockwave_velP` | Shockwave $v'(x)$ equation |
| `eq:shockwave_ID` | Shockwave initial data (erf profiles) |
| `eq:Rankine_Hugoniot` | Rankine-Hugoniot jump conditions |
| `eq:thermo_identity` | Thermodynamic identity for $dP/\rho$ |
| `eq:alt_heat_vector` | Alternative form of heat flux |
| `eq:heat_t_Eckart` | Heat equation (Eckart frame) |
| `eq:heat_t_hybrid` | Telegrapher's equation (hybrid frame) |
| `eq:heat_t_BDNK` | Generalized telegrapher's equation (BDNK frame) |
| `eq:heat_flow_ID` | Heat flow initial data |
| `eq:cpmsq` | Characteristic speeds $c_\pm^2$ |
| `eq:c1sq` | Characteristic speed $c_1^2$ |
| `eq:convergence_factor` | Convergence factor $Q_N$ |
| `eq:A`--`eq:C` | Shorthand $A, B, C$ for causality constraints |
| `eq:frame_ansatz` | $\tau_\epsilon = \tau_Q = L\hat{V}\hat{\tau}$, $\tau_P = 2\alpha c_s^2 L\hat{V}$ |
| `eq:sigma_bound` | $\hat{\sigma} \leq 1/3$ |
| `eq:fully_simplified_caus_const` | Fully simplified causality constraint |

### 6.5 Equation Number Concordance (Ground Truth)

The planning documents use inconsistent paper equation numbers due to different draft versions. The table below provides the **canonical mapping** from our label-based system to the paper.tex line numbers (ground truth). When citing paper equations by number, always include the line reference to avoid ambiguity.

| Our Label | Content | paper.tex Line(s) | plan-numerical-impl Eq # | plan-math-derivations Eq # | plan-test-results Eq # |
|---|---|---|---|---|---|
| `eq:EOS` | Gamma-law EOS | 394 | Eq 8 | Eqs. 14-15 | -- |
| `eq:hydro_frame` | Hydrodynamic frame definitions | 464-468 | Eq 26 | Eq. 31 | -- |
| `eq:V` / `eq:Vhat_defn` | Combined viscosity V and V_hat | 473-474 | Eqs 27-28 | -- | -- |
| `eq:inviscid_bjorken` | Inviscid Bjorken solution | 800 | Eq 34 | Eq. 48 | Eq. (39) |
| `eq:Bjorken_EOM` | Bjorken flow ODE | 795 | Eq 35 | Eq. 47 | -- |
| `eq:shockwave_nprime` | Shockwave n'(x) | 953 | Eq 37 | Eq. 43 | -- |
| `eq:cpmsq` (general) | Characteristic speeds c_pm (general) | 969 | Eq 38 | Eq. 44 | -- |
| `eq:shockwave_epsP` | Shockwave epsilon'(x) | 974 | Eq 39 | Eqs. 47-48 | Eqs. (44)-(47) |
| `eq:shockwave_velP` | Shockwave v'(x) | 975 | Eq 40 | Eqs. 47-48 | Eqs. (44)-(47) |
| `eq:shockwave_ID` | Shockwave initial data (erf) | 1031-1037 | Eq 46 | -- | Eq. (50) |
| `eq:Rankine_Hugoniot` | Rankine-Hugoniot conditions | 1039-1045 | Eq 47 | Eqs. 49-50 | -- |
| `eq:thermo_identity` | Thermodynamic identity | (Sec. III.D) | -- | Eq. 53 | -- |
| `eq:heat_flow_ID` | Heat flow initial data | 1217-1218 | Eq 53 | below Eq. 64 | Eq. (59) |
| `eq:convergence_factor` | Convergence factor Q_N | 1436 | Eq A1 | -- | Eq. A6 |
| `eq:cpmsq` (frame-specific) | Characteristic speeds c_pm^2 | 1424-1427 | Eq A8 | Eq. 75 | Eqs. A12-A13 |
| `eq:c1sq` | Characteristic speed c_1^2 | 1429 | Eq A9 | Eq. 76 | -- |
| `Table:parameters` | Parameter values per figure | 550-562 | Table II | -- | Table I |
| `Table:ODE_convergence` | ODE convergence results | 1441-1450 | Table III | -- | Table II |

**Rule:** In all final documentation, prefer the label from the "Our Label" column. If a numeric paper equation reference is needed, use the `plan-numerical-implementations.md` column (which includes paper.tex line citations) as the canonical source.

---

## 7. Unit Conventions

### 7.1 Natural Units

Throughout the paper, natural units are used:

$$
c = 1, \quad k_B = 1
$$

- The speed of light $c = 1$ means velocities are dimensionless fractions of the speed of light.
- Causality requires characteristic speeds $|c_\pm| \leq 1$.
- Energy density, pressure, and $\rho$ all have dimensions of energy/volume.
- Temperature has dimensions of energy (since $k_B = 1$).

### 7.2 Dimensionful vs. Dimensionless Quantities

- The lengthscale $L$ carries dimensions of length and is set to $L = 1$ in the paper.
- All hatted quantities ($\hat{\eta}, \hat{\zeta}, \hat{\sigma}, \hat{\tau}, \hat{V}$) are **dimensionless**.
- The unhatted transport coefficients ($\eta, \zeta, \sigma, \tau_\epsilon, \tau_P, \tau_Q$) carry dimensions determined by the factors $\rho c_s^2 L$ or $L\hat{V}$.
- The viscosity $V$ has the same dimensions as $\eta$ and $\zeta$.

### 7.3 Key Dimensional Relations

| Quantity | Dimensions (in $c = k_B = 1$) |
|----------|-------------------------------|
| $\epsilon, P, \rho$ | energy / volume |
| $n$ | 1 / volume |
| $m$ | energy (rest mass energy) |
| $T$ | energy |
| $\mu$ | energy |
| $s$ | 1 / volume |
| $\eta, \zeta, V$ | energy / (volume $\cdot$ length) $=$ energy / volume (when $L=1$) |
| $\sigma$ | 1 / (length $\cdot$ energy) (when combined with $\kappa_\epsilon$) |
| $\tau_\epsilon, \tau_P, \tau_Q$ | length (equivalently time, since $c=1$) |
| $u^a$ | dimensionless |
| $v, c_s, c_\pm, c_1$ | dimensionless |

---

## 8. Figure Naming Convention

### 8.1 Paper Figures

The paper contains 7 figures. Reference them using the following convention:

| Reference Tag | File Name | Content | Paper Section |
|---------------|-----------|---------|---------------|
| `fig:bjorken` | `bjorken_plot.pdf` | Bjorken flow: $\dot{\epsilon} + \Gamma\epsilon/\tau$ vs. $\tau$ (top); Temperature evolution (bottom) | Sec. III.B |
| `fig:shockwave_profile` | `shockwave_plot.pdf` | Steady-state shockwave profiles (ideal gas vs. conformal) | Sec. III.C |
| `fig:shock_instability` | `shock_instability.pdf` | Shockwave instability: $v > c_+$ causes breakdown (top); stable frame (bottom) | Sec. III.C |
| `fig:acaus_instab` | `acaus_instab.pdf` | Acausal instability: weakly superluminal frames OK (top); wildly superluminal breakdown (bottom) | Sec. III.C |
| `fig:heat_stationary` | `heat_stationary.pdf` | Heat flow: $\hat{\sigma}=0$ stationary (top) vs. $\hat{\sigma}=1/3$ dynamical (bottom) | Sec. III.D |
| `fig:telegraphers` | `telegraphers_plot.pdf` | Telegrapher's equation behavior: heat-like to wave-like transition; instability for $\hat{\sigma} = 7.5$ | Sec. III.D |
| `fig:conv_plot` | `conv_plot.pdf` | Convergence factor $Q_N(t)$ for shockwave and heat flow problems | Appendix B |

### 8.2 Figure Referencing Format

When referencing figures from the paper in our markdown files, use:

```
(ref: paper Fig. X)
```

Examples:
- `The Bjorken flow results are shown in (ref: paper Fig. 1).`
- `The shockwave instability is illustrated in (ref: paper Fig. 3).`

When creating our own figures, use descriptive filenames with the section prefix:

```
fig_bjorken_convergence.png
fig_shock_profile_comparison.png
fig_heat_temperature_evolution.png
```

### 8.3 Parameters Used Per Figure

(From paper Table II)

| Figure | $\Gamma$ | $m$ | $\hat{V}$ | $\hat{\sigma}$ | $\hat{\tau}$ |
|--------|----------|-----|-----------|----------------|-------------|
| `fig:bjorken` | $4/3$ | $1$ | $1/10$ | $0$ | $0.5, 1, 2$ |
| `fig:shockwave_profile` | $4/3$ | $0.1$ | $2/15$ | $0$ | $1.5$ |
| `fig:shock_instability` | $4/3$ | $0.1$ | $4/3$ | $0$ | $1.5, 3$ |
| `fig:acaus_instab` | $4/3$ | $0.1$ | $4/3$ | $0$ | $0.25, 0.4, 0.5, 1.5$ |
| `fig:heat_stationary` | $4/3$ | $0.1$ | $2/15$ | $0, 1/3$ | $1.5$ |
| `fig:telegraphers` | $4/3$ | $0.1$ | $2/15$ | $0.15, 1.5, 7.5$ | $1.5, 15, 75$ |
| `fig:conv_plot` | (same as respective tests) | | | | |

**Note (open question):** The heat flow initial data parameters ($A$, $\delta$, $w$, $P_0$ in the Gaussian temperature profile, `eq:heat_flow_ID`) are not explicitly stated in the paper text or in this parameter table. They may only be available in the code repository. This gap affects both `plan-numerical-implementations.md` (Sec. 3.5) and `plan-test-results.md` (Tests 6-7).

---

## 9. BDNK Constitutive Relations (Quick Reference)

For convenience, the full BDNK conserved currents are:

$$
T^{ab} = \mathcal{E}\,u^a u^b + \mathcal{P}\,\Delta^{ab} + \mathcal{Q}^a u^b + \mathcal{Q}^b u^a + \mathcal{T}^{ab}
$$

$$
J^a = n\,u^a
$$

with:

$$
\begin{aligned}
\mathcal{E} &= \epsilon + \tau_\epsilon\left[u^c \nabla_c \epsilon + \rho\,\nabla_c u^c\right] \\
\mathcal{P} &= P - \zeta\,\nabla_c u^c + \tau_P\left[u^c \nabla_c \epsilon + \rho\,\nabla_c u^c\right] \\
\mathcal{Q}^a &= \tau_Q\,\rho\,u^c \nabla_c u^a + \beta_\epsilon\,\Delta^{ac}\nabla_c \epsilon + \beta_n\,\Delta^{ac}\nabla_c n \\
\mathcal{T}^{ab} &= -2\eta\,\sigma^{ab} \equiv -2\eta\,\nabla^{\langle a} u^{b\rangle} \\
\mathcal{N} &= n \\
\mathcal{J}^a &= 0
\end{aligned}
$$

---

## 10. Eckart and MIS Conventions (for Comparison)

### Eckart Frame

$$
\tau_\epsilon = \tau_P = 0, \quad \tau_Q = -\frac{\kappa T}{\rho}
$$

### MIS Relaxation Equation

$$
u^c \nabla_c \pi^{ab} = \frac{1}{\tau_\pi}\left(\pi^{ab}_{NS} - \pi^{ab}\right) + I^{ab}
$$

### Theory Comparison (Trivial Equilibrium)

$$
\begin{aligned}
\epsilon &= T^{tt} &&\text{(Eckart)} \\
\dot{\epsilon} &= \frac{1}{\tau_\epsilon}(T^{tt} - \epsilon) &&\text{(BDNK)} \\
\dot{\epsilon} &= \frac{1}{\tau_\pi + c_{1,\text{MIS}}}(T^{tt} - \epsilon) &&\text{(MIS)}
\end{aligned}
$$

**Note:** The $c_{1,\text{MIS}}$ here is the MIS coefficient (see Sec. 1.7), NOT the BDNK characteristic speed $c_1$ defined in Sec. 1.6.

---

## 11. Equation of State Quick Reference

### Gamma-Law EOS

$$
P(\epsilon, n) = [\Gamma - 1]\,m\,n\,e(\epsilon, n) = n\,T(\epsilon, n)
$$

### Derived Relations

$$
\epsilon = m\,n\,(1 + e)
$$

$$
c_s^2 = \frac{\Gamma P}{\rho} = \frac{\Gamma P}{\epsilon + P}
$$

### Entropy and Chemical Potential

$$
s(\epsilon, n) = m\,n\left(\frac{1}{(\Gamma-1)m}\ln\left[\frac{e(\epsilon,n)}{n^{\Gamma-1}}\right] + \text{const}\right)
$$

$$
\mu(\epsilon, n) = m + m\,e(\epsilon,n)\left(\Gamma - \ln\left[\frac{e(\epsilon,n)}{n^{\Gamma-1}}\right] + \text{const}\right)
$$

### Euler Relation

$$
\rho = T\,s + n\,\mu
$$

### Thermodynamic Identity

$$
\frac{dP}{\rho} = \frac{dT}{T} + \frac{nT}{\rho}\,d(\mu/T)
$$
