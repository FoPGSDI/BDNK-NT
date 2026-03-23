# The Novikov-Thorne Accretion Disk Model

## A Comprehensive Mathematical Reference

Based on: I. D. Novikov & K. S. Thorne, *Astrophysics of Black Holes*, in **Black Holes** (Les Houches 1972), eds. C. DeWitt & B. S. DeWitt (Gordon and Breach, New York, 1973), pp. 345–450.

---

## Table of Contents

1. [Historical Foundations](#1-historical-foundations)
2. [Notation and Conventions](#2-notation-and-conventions)
3. [Kerr Spacetime Geometry](#3-kerr-spacetime-geometry)
4. [Circular Geodesics in the Equatorial Plane](#4-circular-geodesics-in-the-equatorial-plane)
5. [Model Assumptions and Idealizations](#5-model-assumptions-and-idealizations)
6. [Equations of Radial Structure](#6-equations-of-radial-structure)
7. [The Zero-Torque Boundary and the Page-Thorne Flux](#7-the-zero-torque-boundary-and-the-page-thorne-flux)
8. [Equations of Vertical Structure](#8-equations-of-vertical-structure)
9. [The Alpha-Viscosity Prescription](#9-the-alpha-viscosity-prescription)
10. [Approximate Vertical Structure (Vertically-Averaged)](#10-approximate-vertical-structure-vertically-averaged)
11. [Three-Zone Disk Solutions](#11-three-zone-disk-solutions)
12. [Radiation Spectrum](#12-radiation-spectrum)
13. [Radiative Efficiency and the Eddington Limit](#13-radiative-efficiency-and-the-eddington-limit)
14. [Validity, Limitations, and Modern Extensions](#14-validity-limitations-and-modern-extensions)

---

## 1. Historical Foundations

The Novikov-Thorne (NT) disk model is the general-relativistic theory of geometrically thin, optically thick accretion disks around black holes. It rests on a chain of four foundational works:

| Year | Authors | Contribution |
|------|---------|-------------|
| 1972 | Bardeen, Press & Teukolsky | Complete geodesic toolkit for Kerr spacetime: $\Omega$, $\tilde{E}$, $\tilde{L}$, $r_{\rm ms}$ |
| 1973 | Shakura & Sunyaev | $\alpha$-viscosity prescription; Newtonian three-zone disk solutions |
| 1973 | Novikov & Thorne | GR extension of disk structure via three conservation laws; relativistic correction factors $\mathscr{A}$–$\mathscr{G}$; vertical structure framework |
| 1974 | Page & Thorne | Cleanest algebraic form of the time-averaged flux $F(r)$ as an explicit integral |

The logical chain: Keplerian disk + viscous angular momentum transport (Prendergast, Lynden-Bell) → $\alpha$-viscosity parameterization (Shakura & Sunyaev) → Newtonian radial + vertical structure → extension to Kerr spacetime using BPT geodesic quantities (Novikov & Thorne) → closed-form flux integral with zero-torque ISCO boundary condition (Page & Thorne).

---

## 2. Notation and Conventions

### 2.1 Fundamental Constants

| Symbol | Meaning |
|--------|---------|
| $G$ | Gravitational constant |
| $c$ | Speed of light |
| $k$ | Boltzmann constant |
| $h$ | Planck constant |
| $m_e$ | Electron rest mass |
| $m_p$ | Proton rest mass |
| $e$ | Electron charge |
| $\sigma_T$ | Thomson cross section |
| $\alpha_{\rm fs}$ | Fine-structure constant |
| $r_0$ | Classical electron radius |
| $R_y$ | Rydberg energy |
| $b$ | Radiation constant ($= 4\sigma_{\rm SB}/c$) |

### 2.2 Unit Systems

The paper employs two unit conventions:

- **CGS-Gaussian units** in Sections 2–4 (plasma physics, spherical accretion): all factors of $G$, $c$, $k$ retained explicitly.
- **Geometrized units** ($G = c = k = 1$) in Section 5 onward (disk structure in Kerr spacetime): mass, length, and time all measured in centimeters.

In geometrized units: $[M] = {\rm cm}$, $[r] = {\rm cm}$, $[t] = {\rm cm}$, $[\dot{M}_0] = {\rm cm}$ (i.e., ${\rm g\cdot cm/g} = {\rm cm}$).

### 2.3 Dimensionless Variables

$$
r_* \equiv \frac{r}{M}, \qquad a_* \equiv \frac{a}{M} \quad (0 \le a_* \le 1)
$$

For explicit disk models (Section 11), the following astrophysical scalings are used:

$$
M_* \equiv \frac{M}{10\,M_\odot}, \qquad \dot{M}_{0*} \equiv \frac{\dot{M}_0}{10^{17}\;{\rm g\;s^{-1}}}
$$

so that $M_* \sim \dot{M}_{0*} \sim 1$ for typical galactic X-ray binaries.

### 2.4 Tensor and Vector Notation

| Notation | Meaning |
|----------|---------|
| $\mathbf{u}$ (bold) | 4-vectors |
| $\mathbf{v}$ (bold) | 3-vectors |
| Greek indices $\alpha, \beta = 0,1,2,3$ | Spacetime indices |
| Latin indices $a, b = 1,2,3$ | Spatial indices |
| Hatted indices $\hat{r}, \hat{\phi}, \hat{z}$ | Orthonormal frame components |
| $\tilde{E}$, $\tilde{L}$ (tilde) | Per-unit-mass quantities (specific energy, specific angular momentum) |
| $\langle \Psi \rangle$ | Time-azimuth-radial average of $\Psi$ (eq. 5.5.2) |

### 2.5 Key Symbols for Disk Structure

| Symbol | Definition |
|--------|-----------|
| $M$, $a$ | Black hole mass and specific angular momentum |
| $\dot{M}_0$ | Steady-state rest-mass accretion rate |
| $\Sigma$ | Surface density (g cm$^{-2}$) |
| $W$ | Vertically integrated shear stress |
| $F$ | Radiative flux from one face of disk (erg cm$^{-2}$ s$^{-1}$) |
| $h$ | Disk half-thickness |
| $\bar{v}^{\hat{r}}$ | Mass-averaged radial velocity |
| $\rho_0$ | Rest-mass density |
| $p$ | Total pressure |
| $T$ | Temperature |
| $\alpha$ | Shakura-Sunyaev viscosity parameter |
| $\kappa$ | Rosseland mean opacity |
| $\tau$ | Optical depth |
| $r_{\rm ms}$ | Radius of marginally stable (ISCO) orbit |

---

## 3. Kerr Spacetime Geometry

### 3.1 Boyer-Lindquist Metric

The Kerr metric in standard Boyer-Lindquist coordinates $(t, r, \theta, \phi)$:

$$
ds^2 = -\left(1 - \frac{2Mr}{\Sigma_{\rm BL}}\right)dt^2 - \frac{4Mar\sin^2\theta}{\Sigma_{\rm BL}}\,dt\,d\phi + \frac{\Sigma_{\rm BL}}{\Delta}\,dr^2 + \Sigma_{\rm BL}\,d\theta^2 + \left(r^2 + a^2 + \frac{2Ma^2 r\sin^2\theta}{\Sigma_{\rm BL}}\right)\sin^2\theta\,d\phi^2
$$

where $\Sigma_{\rm BL} = r^2 + a^2\cos^2\theta$ and $\Delta = r^2 - 2Mr + a^2$.

### 3.2 Equatorial-Plane Metric

For the thin disk ($|\theta - \pi/2| \ll 1$), introduce $z = r\cos\theta \simeq r(\pi/2 - \theta)$. In the equatorial plane ($\theta = \pi/2$, $\Sigma_{\rm BL} = r^2$), the metric simplifies to [NT eq. 5.4.2]:

$$
ds^2 = -\frac{r^2\Delta}{\mathcal{A}}\,dt^2 + \frac{\mathcal{A}}{r^2}\bigl(d\phi - \omega\,dt\bigr)^2 + \frac{r^2}{\Delta}\,dr^2 + r^2\,d\theta^2
$$

where the key metric functions are:

$$
\Delta \equiv r^2 - 2Mr + a^2 = r^2\,\mathscr{D}
$$

$$
\mathcal{A} \equiv r^4 + r^2 a^2 + 2Mra^2 = r^4\,\mathscr{A}
$$

$$
\omega \equiv \frac{2Mar}{\mathcal{A}} = \frac{2Ma}{r^3}\,\mathscr{A}^{-1}
$$

The metric determinant satisfies $\sqrt{-g} = r$.

### 3.3 Relativistic Correction Factors

NT define seven dimensionless functions of $r_* = r/M$ and $a_* = a/M$, each approaching unity as $r_* \to \infty$ [NT eqs. 5.4.1a–g]:

$$
\boxed{
\begin{aligned}
\mathscr{A} &\equiv 1 + \frac{a_*^2}{r_*^2} + \frac{2a_*^2}{r_*^3} \\[6pt]
\mathscr{B} &\equiv 1 + \frac{a_*}{r_*^{3/2}} \\[6pt]
\mathscr{C} &\equiv 1 - \frac{3}{r_*} + \frac{2a_*}{r_*^{3/2}} \\[6pt]
\mathscr{D} &\equiv 1 - \frac{2}{r_*} + \frac{a_*^2}{r_*^2} \\[6pt]
\mathscr{E} &\equiv 1 + \frac{4a_*^2}{r_*^2} - \frac{4a_*^2}{r_*^3} + \frac{3a_*^4}{r_*^4} \\[6pt]
\mathscr{F} &\equiv 1 - \frac{2a_*}{r_*^{3/2}} + \frac{a_*^2}{r_*^2} \\[6pt]
\mathscr{G} &\equiv 1 - \frac{2}{r_*} + \frac{a_*}{r_*^{3/2}}
\end{aligned}
}
$$

**Physical roles:**

| Factor | Physical meaning | Vanishes at |
|--------|-----------------|-------------|
| $\mathscr{A}$ | Metric function $g_{\phi\phi}/r^4$; frame-dragging geometry | — |
| $\mathscr{B}$ | Angular velocity correction; $\Omega = M^{1/2}/(r^{3/2}\mathscr{B})$ | — |
| $\mathscr{C}$ | Orbital stability; $\mathscr{C} = 0$ defines the ISCO | $r = r_{\rm ms}$ |
| $\mathscr{D}$ | Horizon function; $\Delta/r^2$; $\mathscr{D} = 0$ at horizon | $r = r_+$ |
| $\mathscr{E}$ | Higher-order metric correction | — |
| $\mathscr{F}$ | Angular momentum correction | — |
| $\mathscr{G}$ | Combined gravitational-rotational factor; appears in $\tilde{E}$, $\tilde{L}$, flux | — |

**Newtonian limit** ($r_* \to \infty$): All factors $\to 1$.

**Schwarzschild limit** ($a_* = 0$):

$$
\mathscr{A} = 1, \quad \mathscr{B} = 1, \quad \mathscr{C} = 1 - 3/r_*, \quad \mathscr{D} = 1 - 2/r_*, \quad \mathscr{F} = 1, \quad \mathscr{G} = 1 - 2/r_*
$$

---

## 4. Circular Geodesics in the Equatorial Plane

All formulas in this section derive from Bardeen, Press & Teukolsky (1972), as presented in NT Section 5.4. These describe **direct** (prograde) circular orbits in the equatorial plane of the Kerr metric.

### 4.1 Angular Velocity

$$
\Omega \equiv \frac{d\phi}{dt} = \frac{M^{1/2}}{r^{3/2} + aM^{1/2}} = \frac{M^{1/2}}{r^{3/2}\,\mathscr{B}}
\tag{5.4.3}
$$

Newtonian limit: $\Omega \to (M/r^3)^{1/2}$ (Kepler's law).

### 4.2 Linear Velocity Relative to LNRF

The velocity of the orbiting gas measured by a locally non-rotating frame (LNRF) observer:

$$
V^{(\phi)} = r^{-1}\mathscr{A}^{1/2}(\Omega - \omega) = \frac{M^{1/2}}{r^{1/2}}\;\frac{\mathscr{F}}{\mathscr{G}^{1/2}\,\mathscr{B}}
\tag{5.4.4}
$$

### 4.3 Lorentz Factor

$$
\gamma = \bigl(1 - V^{(\phi)2}\bigr)^{-1/2} = \frac{\mathscr{B}}{r_*^{1/2}\,\mathscr{C}^{1/2}\,\mathscr{G}}
\tag{5.4.4b}
$$

### 4.4 Specific Energy (Energy per Unit Mass)

$$
\boxed{\tilde{E} = |u_0| = \frac{\mathscr{G}}{\mathscr{C}^{1/2}}}
\tag{5.4.7b}
$$

Newtonian limit: $\tilde{E} \to 1 - M/(2r)$ (i.e., binding energy $\to M/(2r)$).

### 4.5 Specific Angular Momentum

$$
\boxed{\tilde{L} = u_\phi = M^{1/2}\,r^{1/2}\;\frac{\mathscr{F}}{\mathscr{C}^{1/2}}}
\tag{5.4.7a}
$$

Newtonian limit: $\tilde{L} \to (Mr)^{1/2}$.

### 4.6 Shear of Equatorial Geodesic Congruence

The only nonvanishing component of the shear tensor of the congruence of circular equatorial geodesics:

$$
\sigma_{\hat{r}\hat{\phi}}^{(\rm EG)} = \sigma_{\hat{\phi}\hat{r}}^{(\rm EG)} = -\frac{3\,M^{1/2}\,\mathscr{G}}{4\,r^{3/2}\,\mathscr{C}\,\mathscr{B}}
\tag{5.4.6}
$$

Newtonian limit: $\sigma_{\hat{r}\hat{\phi}} \to -\tfrac{3}{4}(M/r^3)^{1/2}$.

### 4.7 Innermost Stable Circular Orbit (ISCO)

The ISCO radius $r_{\rm ms}$ is determined by $\mathscr{C}(r_{\rm ms}) = 0$, equivalently by:

$$
r_{\rm ms}^2 - 6Mr_{\rm ms} + 8aM^{1/2}\,r_{\rm ms}^{1/2} - 3a^2 = 0
$$

The explicit solution [NT eq. 5.4.8]:

$$
\boxed{r_{\rm ms} = M\Bigl\{3 + Z_2 - \bigl[(3 - Z_1)(3 + Z_1 + 2Z_2)\bigr]^{1/2}\Bigr\}}
\tag{5.4.8a}
$$

where

$$
Z_1 = 1 + (1 - a_*^2)^{1/3}\bigl[(1 + a_*)^{1/3} + (1 - a_*)^{1/3}\bigr]
\tag{5.4.8b}
$$

$$
Z_2 = (3a_*^2 + Z_1^2)^{1/2}
$$

The angular momentum at the ISCO:

$$
\tilde{L}_{\rm ms} = \frac{2M}{3^{1/2}\,r_{\rm ms}^{1/2}}(3r_{\rm ms}^{1/2} - 2a)
\tag{5.4.9}
$$

### 4.8 Key Values

| Quantity | Schwarzschild ($a_* = 0$) | Extreme Kerr ($a_* = 1$) |
|----------|--------------------------|-------------------------|
| $r_{\rm ms}/M$ | $6$ | $1$ |
| $\tilde{E}_{\rm ms}$ | $\sqrt{8/9} \approx 0.9428$ | $1/\sqrt{3} \approx 0.5774$ |
| $\tilde{L}_{\rm ms}/M$ | $2\sqrt{3} \approx 3.464$ | $2/\sqrt{3} \approx 1.155$ |
| Binding energy $1 - \tilde{E}_{\rm ms}$ | $5.72\%$ | $42.3\%$ |
| $r_+/M$ (horizon) | $2$ | $1$ |
| $r_{\rm mb}/M$ (marginally bound) | $4$ | $1$ |

---

## 5. Model Assumptions and Idealizations

The NT disk model rests on seven assumptions [NT §5.5]:

**(i) Equatorial plane.** The central plane of the disk coincides with the equatorial plane of the Kerr black hole.

**(ii) Negligible companion gravity.** The companion star's tidal field is ignored (valid in the inner disk, not at the outer edge).

**(iii) Thin disk.** The proper thickness $2h$, measured in the orbiting frame, satisfies

$$
h(r) \ll r
\tag{5.5.1}
$$

**(iv) Quasi-steady state.** All macroscopic quantities, when averaged over azimuth, a radial interval $\sim 2h$, and a time interval $\sim 2h/|\bar{v}^{\hat{r}}|$, are time-independent:

$$
\frac{\partial\langle\Psi\rangle}{\partial t} = 0 \quad (\text{scalars}), \qquad \mathscr{L}_{\partial/\partial t}\langle\Psi\rangle = 0 \quad (\text{vectors/tensors})
\tag{5.5.3}
$$

Local fluctuations (turbulence, magnetic reconnection, flares) on scales $\lesssim h$ are permitted.

**(v) Nearly geodesic orbits.** The macroscopic gas motion is dominated by circular geodesic orbits, with a small superimposed radial drift:

$$
|v^{\hat{r}}| \ll V^{(\phi)} \simeq (M/r)^{1/2}
\tag{5.5.5}
$$

This requires that pressure gradients and stresses are small compared to gravitational acceleration:

$$
\frac{T^{\hat{r}\hat{k}}}{\rho_0} \ll 1 - \tilde{E}(r) \approx \frac{1}{2}\frac{M}{r} \quad (\text{Newtonian limit})
\tag{5.5.6}
$$

**(vi) Negligible specific heat.** The specific internal energy (thermal + turbulent + magnetic) is much smaller than the gravitational binding energy:

$$
\Pi(r,z) \ll 1 - \tilde{E}(r)
\tag{5.5.7}
$$

Combined with (v), this yields the critical simplification:

$$
\Pi \ll 1, \qquad T^{\hat{r}\hat{k}}/\rho_0 \ll 1
\tag{5.5.8}
$$

**Key consequence:** Although spacetime curvature is fully relativistic near the hole, the *local* thermodynamic, hydrodynamic, and radiative properties of the gas can be treated with Newtonian physics everywhere. General relativity enters only through the geodesic structure (orbital quantities and tidal gravity).

**(vii) $\alpha$-viscosity.** The shear stress is parameterized as $t_{\hat{\phi}\hat{r}} = \alpha\,p$ with $\alpha \le 1$ (see Section 9).

---

## 6. Equations of Radial Structure

### 6.1 Defined Quantities

The radial structure is described by four functions of $r$ [NT eqs. 5.6.1]:

$$
\Sigma(r) \equiv \int_{-h}^{+h}\langle\rho_0\rangle\,dz \qquad \text{(surface density)}
\tag{5.6.1a}
$$

$$
W(r) \equiv \int_{-h}^{+h}\langle T_{\hat{r}\hat{\phi}}\rangle\,dz \qquad \text{(integrated shear stress)}
\tag{5.6.1b}
$$

$$
\bar{v}^{\hat{r}}(r) \equiv \frac{1}{\Sigma}\int_{-h}^{+h}\langle v^{\hat{r}}\,\rho_0\rangle\,dz \qquad \text{(mass-averaged radial velocity)}
\tag{5.6.1c}
$$

$$
F(r) \equiv \langle q^{\hat{z}}(z=h)\rangle = \langle -q^{\hat{z}}(z=-h)\rangle \qquad \text{(radiative flux per face)}
\tag{5.6.1d}
$$

### 6.2 Three Conservation Laws

**Conservation of rest mass.** The accretion rate across any cylinder of radius $r$ is constant:

$$
\dot{M}_0 = -2\pi r\,\Sigma\,\bar{v}^{\hat{r}}\,\mathscr{D}^{1/2}
\tag{5.6.14c}
$$

(Here $\mathscr{D}^{1/2}$ is the metric factor $\sqrt{g_{rr}}^{-1}$, sometimes written $\mathscr{G}^{1/2}$ in certain formulations.)

**Conservation of angular momentum.** Balancing angular momentum carried by mass inflow, viscous transport, and photon emission:

$$
-\frac{\dot{M}_0\,\tilde{L}}{2\pi} + \bigl(r^2\,\mathscr{D}^{-1/2}\,2\mathscr{D}^{1/2}\,W\bigr)_{,r} + 2\tilde{L}\,F = 0
\tag{5.6.6}
$$

**Conservation of energy.** Balancing viscous dissipation against radiative losses (dropping negligible specific-heat and compressional terms):

$$
2F = -2\,\sigma_{\hat{r}\hat{\phi}}^{(\rm EG)}\,W = \frac{3\,M^{1/2}}{2\,r^{3/2}}\;\frac{\mathscr{G}}{\mathscr{C}\,\mathscr{B}}\;W
\tag{5.6.12}
$$

### 6.3 Combined Differential Equation

Combining angular momentum and energy conservation yields a first-order ODE for $W(r)$:

$$
\Bigl(-\frac{\dot{M}_0\,\tilde{L}}{2\pi} + r^{3/2}\,\mathscr{D}^{-1/2}\,2\mathscr{D}^{1/2}\,W\Bigr)_{,r} + \frac{\tilde{L}}{2}\,(Mr)^{-1}\,\mathscr{D}^{-1/2}\,\mathscr{D}^{1/2}\,W = 0
\tag{5.6.13}
$$

All coefficients are known algebraic functions of $r$ from the Kerr geodesic quantities (Section 4). The only unknowns are $\dot{M}_0$ (a constant) and $W(r)$.

### 6.4 Solutions with Zero-Torque Boundary Condition

The boundary condition $W(r_{\rm ms}) = 0$ (Section 7) uniquely fixes the solution:

$$
\boxed{W(r) = \frac{\dot{M}_0}{2\pi}\left(\frac{M}{r^3}\right)^{1/2}\frac{\mathscr{Q}^{1/2}}{\mathscr{B}\,\mathscr{G}}}
\tag{5.6.14a}
$$

$$
\boxed{F(r) = \frac{3\dot{M}_0}{8\pi r^2}\;\frac{M}{r}\;\frac{\mathscr{Q}}{\mathscr{C}^{1/2}\,\mathscr{B}}}
\tag{5.6.14b}
$$

where $\mathscr{Q}$ is the **zero-torque integral factor** (see Section 7).

**Newtonian limits** (all correction factors $\to 1$, $\mathscr{Q} \to 1 - \sqrt{r_I/r}$):

$$
W_{\rm Newt} = \frac{\dot{M}_0}{2\pi}\left(\frac{M}{r^3}\right)^{1/2}\left[1 - \left(\frac{r_I}{r}\right)^{1/2}\right]
$$

$$
F_{\rm Newt} = \frac{3\dot{M}_0}{8\pi r^2}\;\frac{M}{r}\;\left[1 - \left(\frac{r_I}{r}\right)^{1/2}\right]
$$

**Important structural property:** The equations of radial structure determine $W(r)$ and $F(r)$ explicitly from $\dot{M}_0$, $M$, $a$ alone. They determine only the *product* $\Sigma\,\bar{v}^{\hat{r}}$, not the individual functions — separating these requires the vertical structure.

---

## 7. The Zero-Torque Boundary and the Page-Thorne Flux

### 7.1 Physical Motivation

At the ISCO ($r = r_{\rm ms}$), circular orbits become unstable. Gas reaching $r_{\rm ms}$ "falls out" of the disk and spirals rapidly into the black hole. Consequently:

- The gas density at $r < r_{\rm ms}$ is negligible compared to $r > r_{\rm ms}$.
- No viscous stresses can act across the surface $r = r_{\rm ms}$.
- Therefore: $W(r_{\rm ms}) = 0$.

This boundary condition uniquely determines the integration constant in the radial structure equations.

### 7.2 The $\mathscr{Q}$ Factor

The factor $\mathscr{Q}(r)$ encodes the zero-torque boundary condition. It satisfies:

$$
\mathscr{Q}(r_{\rm ms}) = 0, \qquad \mathscr{Q} \to 1 \text{ as } r \to \infty
$$

In the Newtonian limit, $\mathscr{Q} = 1 - (r_I/r)^{1/2}$.

In the full GR treatment, $\mathscr{Q}$ is determined by the integral structure of the ODE (6.3) and involves ratios of the geodesic quantities $\tilde{E}$, $\tilde{L}$, $\Omega$ evaluated between $r_{\rm ms}$ and $r$.

### 7.3 Page-Thorne Integral Form

Page & Thorne (1974) express the flux in the most transparent closed form:

$$
\boxed{F(r) = -\frac{\dot{M}_0}{4\pi\sqrt{-g}}\;\frac{\Omega_{,r}}{(\tilde{E} - \Omega\,\tilde{L})^2}\;\int_{r_{\rm ms}}^{r}(\tilde{E} - \Omega\,\tilde{L})\,\tilde{L}_{,r'}\;dr'}
$$

where all quantities ($\Omega$, $\tilde{E}$, $\tilde{L}$, $\sqrt{-g}$) are the known algebraic functions of $r$ from the Kerr geodesic structure (Section 4).

**Properties:**
- The integral vanishes at $r = r_{\rm ms}$, automatically enforcing zero torque.
- $\Omega_{,r} < 0$ and $\tilde{L}_{,r} > 0$ outside the ISCO, so $F > 0$.
- All geodesic quantities are known in closed form, so $F(r)$ can be evaluated as a single quadrature.

### 7.4 Total Luminosity

The total luminosity of the disk:

$$
L = \int_{r_{\rm ms}}^{\infty} 2F \cdot 2\pi r\,dr = \dot{M}_0\,(1 - \tilde{E}_{\rm ms})
$$

confirming that the radiative efficiency equals the binding energy at the ISCO (see Section 13).

---

## 8. Equations of Vertical Structure

### 8.1 Local Physics in the Orbiting Frame

A key insight of the NT model: in the orbiting orthonormal frame $\{\mathbf{e}_{\hat{0}}, \mathbf{e}_{\hat{r}}, \mathbf{e}_{\hat{\phi}}, \mathbf{e}_{\hat{z}}\}$, the local physics is Newtonian (because $\Pi \ll 1$). The only GR input is the correct tidal acceleration from the Kerr Riemann tensor:

$$
g(z) = R^{\hat{z}}{}_{\hat{0}\hat{z}\hat{0}}\;z
\tag{5.7.1}
$$

The Newtonian limit gives $g = (M/r^3)\,z$, but the full Kerr expression involves additional $a_*$-dependent corrections from the Riemann component $R^{\hat{z}}{}_{\hat{0}\hat{z}\hat{0}}$ [computed from the BPT Riemann tensor components, NT eq. 5.7.2].

### 8.2 Six Equations of Vertical Structure

The vertical structure at each radius $r$ is described by six functions of height $z$: density $\rho_0(z)$, pressure $p(z)$, shear stress $t_{\hat{\phi}\hat{r}}(z)$, temperature $T(z)$, energy flux $q^z(z)$, and opacity $\kappa(z)$. They are governed by [NT eqs. 5.7.4]:

**(a) Vertical pressure balance:**

$$
\frac{dp}{dz} = \rho_0\;R^{\hat{z}}{}_{\hat{0}\hat{z}\hat{0}}\;z
\tag{5.7.4a}
$$

**(b) Viscosity prescription:**

$$
t_{\hat{\phi}\hat{r}} = \text{(model-dependent expression)}
\tag{5.7.4b}
$$

**(c) Energy generation** (viscous dissipation):

$$
\frac{dq^z}{dz} = -2\,\sigma_{\hat{r}\hat{\phi}}^{(\rm EG)}\;t_{\hat{\phi}\hat{r}} = \frac{3}{2}\left(\frac{M}{r^3}\right)^{1/2}\frac{\mathscr{G}}{\mathscr{C}\,\mathscr{B}}\;t_{\hat{\phi}\hat{r}}
\tag{5.7.4c}
$$

**(d) Energy transport** (radiative diffusion for optically thick disks):

$$
q^z = -\frac{1}{\kappa\,\rho_0}\;\frac{d}{dz}\left(\frac{1}{3}\,b\,T^4\right)
\tag{5.7.4d'}
$$

**(e) Equation of state:**

$$
p = \text{(model-dependent; e.g., } p = p_{\rm gas} + p_{\rm rad}\text{)}
\tag{5.7.4e}
$$

**(f) Opacity:**

$$
\kappa = \text{(model-dependent; e.g., } \kappa = \kappa_{\rm ff} + \kappa_{\rm es}\text{)}
\tag{5.7.4f}
$$

### 8.3 Boundary Conditions

The three differential equations (a), (c), (d) require boundary conditions [NT eqs. 5.7.5]:

$$
\rho_0 = 0 \quad \text{at } z = h \tag{5.7.5a}
$$

$$
T = 0 \quad \text{at } z = h \tag{5.7.5b}
$$

$$
q^z = 0 \quad \text{at } z = 0 \quad (\text{symmetry}) \tag{5.7.5c}
$$

$$
2\int_0^h t_{\hat{\phi}\hat{r}}\,dz = W(r) \quad (\text{matching to radial structure}) \tag{5.7.5d}
$$

### 8.4 Coupling to Radial Structure

The vertical structure equations, together with their boundary conditions, automatically satisfy the radial structure equations (5.6.14a,b). The vertical structure additionally provides $\Sigma = 2\int_0^h \rho_0\,dz$, which inserted into eq. (5.6.14c) yields $\bar{v}^{\hat{r}}$, completing the full solution.

---

## 9. The Alpha-Viscosity Prescription

### 9.1 Physical Origins of Viscosity

Two dominant sources of viscosity in the disk:

**Chaotic magnetic fields.** The normal star's surface field ($B_s \sim 100$ G) is dragged into the disk. Shearing amplifies $B_\phi$ by $\sim B_r$ per orbit. Reconnection and magnetic bubble escape limit the growth. The magnetic stress satisfies:

$$
t_{\hat{\phi}\hat{r}}^{(\rm mag)} \lesssim \frac{B^2}{8\pi} \lesssim p
\tag{5.2.29}
$$

**Turbulence.** The turbulent viscosity $\eta \sim \rho_0\,v_{\rm turb}\,l_{\rm turb}$, with $v_{\rm turb} \le c_s$ (supersonic turbulence would shock-dissipate) and $l_{\rm turb} \le h$, gives:

$$
t_{\hat{\phi}\hat{r}}^{(\rm turb)} \lesssim \rho_0\,c_s\,h\,\Omega \simeq \rho_0\,c_s^2 \simeq p
\tag{5.2.31}
$$

### 9.2 The $\alpha$-Parameterization

Both bounds are identical: $t_{\hat{\phi}\hat{r}} \lesssim p$. This motivates the **Shakura-Sunyaev ansatz**:

$$
\boxed{t_{\hat{\phi}\hat{r}} = \alpha\,p, \qquad \alpha \le 1}
\tag{5.2.32}
$$

The parameter $\alpha$ absorbs all ignorance about the true magnitude of the viscosity. Its value determines the disk morphology:
- $\alpha \sim 1$: mottled structure on scales $\sim h$.
- $\alpha \ll 1$: smooth disk on scales $\sim h$.

### 9.3 Modern Perspective: The Magnetorotational Instability

The physical origin of $\alpha$ was identified by Balbus & Hawley (1991) as the **magnetorotational instability** (MRI). A weak magnetic field threading a differentially rotating disk is linearly unstable, generating MHD turbulence that transports angular momentum outward. GRMHD simulations typically find $\alpha \sim 0.01$–$0.1$ for sustained MRI turbulence, consistent with the NT requirement $\alpha \le 1$.

---

## 10. Approximate Vertical Structure (Vertically-Averaged)

Given the large uncertainties in turbulence and magnetic fields, NT replace the six differential equations (Section 8) with algebraic, vertically-averaged approximations [NT eqs. 5.8.1]:

### 10.1 Averaged Equations

**(a) Vertical pressure balance** → disk half-thickness:

$$
h = \left(\frac{p}{\rho_0}\right)^{1/2}\left(\frac{r^3}{M}\right)^{1/2}\frac{1}{R^{\hat{z}}{}_{\hat{0}\hat{z}\hat{0}}{}^{1/2}} = \frac{c_s}{\Omega_{\rm eff}}
\tag{5.8.1a}
$$

where $\Omega_{\rm eff}$ is the effective vertical oscillation frequency (= Keplerian $\Omega$ in the Newtonian limit).

**(b) Viscosity prescription:**

$$
t_{\hat{\phi}\hat{r}} = \alpha\,p
\tag{5.8.1b}
$$

**(c) Energy transport** (radiative diffusion):

$$
b\,T^4 = \kappa\,\Sigma\,F
\tag{5.8.1c}
$$

**(d) Equation of state:**

$$
p = p^{(\rm gas)} + p^{(\rm rad)} = \frac{\rho_0\,T}{\mu_{\rm mm}\,m_p} + \frac{1}{3}\,b\,T^4
\tag{5.8.1d}
$$

where $\mu_{\rm mm}$ is the mean molecular weight ($\approx 0.5$ for ionized hydrogen).

**(e) Opacity:**

$$
\kappa = \kappa_{\rm ff} + \kappa_{\rm es}
\tag{5.8.1e}
$$

$$
\kappa_{\rm ff} = 0.64 \times 10^{23}\;\left(\frac{\rho_0}{\rm g\,cm^{-3}}\right)\left(\frac{T}{\rm K}\right)^{-7/2}\;\frac{\rm cm^2}{\rm g}
$$

$$
\kappa_{\rm es} = 0.40\;\frac{\rm cm^2}{\rm g}
$$

---

## 11. Three-Zone Disk Solutions

Combining the approximate vertical structure (Section 10) with the exact radial structure (Section 6) yields explicit power-law solutions for the disk. The disk divides naturally into three zones based on the dominant pressure and opacity [Shakura & Sunyaev 1973; NT eqs. 5.9.6, 5.9.8, 5.9.10].

### 11.1 Zone Classification

| Zone | Pressure | Opacity | Radial range |
|------|----------|---------|-------------|
| **Outer** | Gas pressure ($p = p_{\rm gas}$) | Free-free ($\kappa = \kappa_{\rm ff}$) | $r > r_{\rm om}$ |
| **Middle** | Gas pressure ($p = p_{\rm gas}$) | Electron scattering ($\kappa = \kappa_{\rm es}$) | $r_{\rm mi} < r < r_{\rm om}$ |
| **Inner** | Radiation pressure ($p = p_{\rm rad}$) | Electron scattering ($\kappa = \kappa_{\rm es}$) | $r_{\rm ms} < r < r_{\rm mi}$ |

### 11.2 Transition Radii

**Outer-to-middle** ($\tau_{\rm ff}/\tau_{\rm es} \sim 1$):

$$
r_{{\rm om}*} \simeq 2 \times 10^3\;M_*^{-2/3}\,\dot{M}_{0*}^{2/3}\;\times (\text{relativistic corrections})
\tag{5.9.7}
$$

**Middle-to-inner** ($p_{\rm gas}/p_{\rm rad} \sim 1$):

$$
r_{{\rm mi}*} \simeq 40\;\alpha^{2/21}\,M_*^{2/3}\,\dot{M}_{0*}^{16/21}\;\times (\text{relativistic corrections})
\tag{5.9.9}
$$

For the supermassive case ($M_* \sim 10^7$, $\dot{M}_{0*} \sim 10^5$): $r_{{\rm om}*} \sim 100$, $r_{{\rm mi}*} \sim 4$ (middle region extends nearly to the ISCO).

### 11.3 Outer Region: $p = p_{\rm gas}$, $\kappa = \kappa_{\rm ff}$

All quantities expressed as (numerical coefficient) $\times$ (parameter dependence) $\times$ (radial power law) $\times$ (relativistic corrections) [NT eq. 5.9.6]:

$$
F = 0.6 \times 10^{26}\;{\rm erg\,cm^{-2}\,s^{-1}} \times M_*^{-2}\,\dot{M}_{0*} \times r_*^{-3} \times \mathscr{B}^{-1}\,\mathscr{C}^{-1/2}\,\mathscr{Q}
$$

$$
\Sigma = 9 \times 10^{5}\;{\rm g\,cm^{-2}} \times \alpha^{-4/5}\,M_*^{1/4}\,\dot{M}_{0*}^{7/10} \times r_*^{3/4} \times \mathscr{B}^{-4/5}\,\mathscr{Q}^{14/5}\,(\ldots)
$$

$$
h = 9 \times 10^{2}\;{\rm cm} \times \alpha^{-1/10}\,M_*^{3/4}\,\dot{M}_{0*}^{3/20} \times r_*^{9/8} \times (\ldots)
$$

$$
\rho_0 = 8 \times 10^{-1}\;{\rm g\,cm^{-3}} \times \alpha^{-7/10}\,M_*^{-7/10}\,\dot{M}_{0*}^{11/20} \times r_*^{-15/8} \times (\ldots)
$$

$$
T = 8 \times 10^{7}\;{\rm K} \times \alpha^{-1/5}\,M_*^{-1/5}\,\dot{M}_{0*}^{3/10} \times r_*^{-3/4} \times (\ldots)
$$

$$
\tau_{\rm ff} = 2 \times 10^{3} \times \alpha^{-4/5}\,M_*^{-7/8}\,\dot{M}_{0*}^{-2/5} \times r_*^{-21/16} \times (\ldots)
$$

### 11.4 Middle Region: $p = p_{\rm gas}$, $\kappa = \kappa_{\rm es}$

[NT eq. 5.9.8]:

$$
F = 0.6 \times 10^{26}\;{\rm erg\,cm^{-2}\,s^{-1}} \times M_*^{-2}\,\dot{M}_{0*} \times r_*^{-3} \times (\ldots)
$$

$$
\Sigma = 5 \times 10^{3}\;{\rm g\,cm^{-2}} \times \alpha^{-4/5}\,M_*^{2/5}\,\dot{M}_{0*}^{3/5} \times r_*^{-3/5} \times (\ldots)
$$

$$
h = 3 \times 10^{3}\;{\rm cm} \times \alpha^{-1/10}\,M_*^{-7/10}\,\dot{M}_{0*}^{1/5} \times r_*^{21/20} \times (\ldots)
$$

$$
\rho_0 = 10\;{\rm g\,cm^{-3}} \times \alpha^{-7/10}\,M_*^{-7/10}\,\dot{M}_{0*}^{2/5} \times r_*^{-33/20} \times (\ldots)
$$

$$
T = 3 \times 10^{8}\;{\rm K} \times \alpha^{-1/5}\,M_*^{-1/5}\,\dot{M}_{0*}^{2/5} \times r_*^{-9/10} \times (\ldots)
$$

$$
\tau_{\rm es} = 2 \times 10^{3} \times \alpha^{-4/5}\,M_*^{1/5}\,\dot{M}_{0*}^{3/5} \times r_*^{-3/5} \times (\ldots)
$$

### 11.5 Inner Region: $p = p_{\rm rad}$, $\kappa = \kappa_{\rm es}$

[NT eq. 5.9.10]:

$$
F = 0.6 \times 10^{26}\;{\rm erg\,cm^{-2}\,s^{-1}} \times M_*^{-2}\,\dot{M}_{0*} \times r_*^{-3} \times \mathscr{B}^{-1}\,\mathscr{C}^{-1/2}\,\mathscr{Q}
$$

$$
\Sigma = 20\;{\rm g\,cm^{-2}} \times \alpha^{-1}\,M_*\,\dot{M}_{0*} \times r_*^{3/2} \times (\ldots)\,\mathscr{Q}^{-1}
$$

$$
h = 1 \times 10^5\;{\rm cm} \times \dot{M}_{0*} \times (\ldots)\,\mathscr{Q}
$$

$$
\rho_0 = 1 \times 10^{-4}\;{\rm g\,cm^{-3}} \times \alpha^{-1}\,M_*\,\dot{M}_{0*} \times r_*^{3/2} \times (\ldots)\,\mathscr{Q}^{-2}
$$

$$
T = 4 \times 10^7\;{\rm K} \times \alpha^{-1/4}\,M_*^{-1/4} \times r_*^{-9/8} \times (\ldots)\,\mathscr{Q}^{1/4}
$$

Note: As $r \to r_{\rm ms}$, $\mathscr{Q} \to 0$, so $\Sigma \to \infty$ and $\rho_0 \to \infty$ in the inner region — signaling breakdown of the thin-disk approximation near the ISCO for the radiation-pressure-dominated zone.

### 11.6 Summary of Power-Law Exponents

| Quantity | Outer ($r_*$ exp) | Middle ($r_*$ exp) | Inner ($r_*$ exp) |
|----------|-------------------|--------------------|--------------------|
| $F$ | $-3$ | $-3$ | $-3$ |
| $\Sigma$ | $+3/4$ | $-3/5$ | $+3/2$ |
| $h$ | $+9/8$ | $+21/20$ | $\sim 0$ (const.) |
| $\rho_0$ | $-15/8$ | $-33/20$ | $+3/2$ |
| $T$ | $-3/4$ | $-9/10$ | $-9/8$ |

| Quantity | $\alpha$ exp (Outer) | $\alpha$ exp (Middle) | $\alpha$ exp (Inner) |
|----------|---------------------|-----------------------|----------------------|
| $\Sigma$ | $-4/5$ | $-4/5$ | $-1$ |
| $h$ | $-1/10$ | $-1/10$ | $0$ |
| $\rho_0$ | $-7/10$ | $-7/10$ | $-1$ |
| $T$ | $-1/5$ | $-1/5$ | $-1/4$ |

### 11.7 Auxiliary Quantities

**Inflow timescale:**

$$
\Delta t(r) = -r/\bar{v}^{\hat{r}}
\tag{5.9.5}
$$

**Magnetic field upper bound:**

$$
B \lesssim (8\pi\,p)^{1/2}
\tag{5.9.4}
$$

**Optical depth:**

$$
\tau = \kappa\,\Sigma
\tag{5.9.3}
$$

---

## 12. Radiation Spectrum

### 12.1 Outer Region: Blackbody

In the outer region ($\kappa_{\rm ff} \gg \kappa_{\rm es}$), the disk is optically thick to absorption. The surface radiates a blackbody spectrum with temperature:

$$
T_s = \left(\frac{4F}{b}\right)^{1/4} \simeq 3 \times 10^5\;{\rm K} \times M_*^{-1/2}\,\dot{M}_{0*}^{1/4} \times r_*^{-3/4}\;\mathscr{B}^{-1/4}\,\mathscr{C}^{-1/8}\,\mathscr{Q}^{1/4}
\tag{5.10.1}
$$

### 12.2 Middle and Inner Regions: Modified Spectrum

When electron scattering dominates the opacity, photons must random-walk through the scattering atmosphere. Photons of frequency $\nu$ escape from a depth where the *effective* optical depth equals unity [Zel'dovich & Shakura 1969]:

$$
\tau_{*}(\text{emission pt.}) \equiv \bigl(\kappa_{\rm ff}^{\nu}\,\kappa_{\rm es}\bigr)^{1/2}\;y_\nu = 1
\tag{5.10.2}
$$

The resulting modified spectrum:

$$
F_\nu = 2\pi\,B_\nu\;\bigl[\tau_{\rm es}(\text{at } \tau_* = 1)\bigr]^{-1}
\tag{5.10.4}
$$

For a homogeneous atmosphere, the spectrum modification factor is:

$$
F_\nu \propto \frac{x^{3/2}\,e^{-x/2}}{(e^x - 1)^{1/2}}, \qquad x \equiv \frac{h\nu}{kT}
\tag{5.10.5}
$$

This is harder (peaks at higher energies) than a pure blackbody.

### 12.3 Optically Thin Regions

If $\tau_* < 1$ at the disk midplane (possible in the innermost region for certain parameters), the spectrum becomes free-free:

$$
F_\nu \propto \kappa_{\rm ff}^{\nu}\;e^{-h\nu/kT}
\tag{5.10.9}
$$

At high temperatures ($T \sim 10^9$ K), **Comptonization** boosts low-energy photons by a fractional energy:

$$
\frac{\Delta(h\nu)}{h\nu} \simeq \frac{4kT}{m_e c^2} \simeq \frac{T}{2 \times 10^8\;{\rm K}}
\tag{5.10.10}
$$

This depletes the low-energy spectrum and augments the high-energy tail.

### 12.4 Peak Frequency Estimates

For an optically thick blackbody disk ($h\nu_{\rm max} \simeq 2.44 \times 10^{-4}\;{\rm eV} \times T_s/{\rm K}$):

| System | $h\nu_{\rm max}$ |
|--------|-------------------|
| Neutron star / BH X-ray binary | $\sim 1$ keV |
| White dwarf | $\sim 0.01$ keV |
| Supermassive BH ($M \sim 10^8\,M_\odot$) | $\sim 10$ eV (UV/optical) |

For the supermassive case [NT eq. 5.3.1]:

$$
\nu_{\rm max} \simeq 10^{15}\;{\rm Hz}\;\left(\frac{\dot{M}_0}{10^{-3}\,M_\odot/{\rm yr}}\right)^{1/4}\left(\frac{M}{10^8\,M_\odot}\right)^{-1/2}
\tag{5.3.1}
$$

---

## 13. Radiative Efficiency and the Eddington Limit

### 13.1 Radiative Efficiency

The total energy radiated per unit accreted rest mass equals the binding energy at the ISCO:

$$
\boxed{\eta = 1 - \tilde{E}_{\rm ms} = 1 - \frac{\mathscr{G}(r_{\rm ms})}{\mathscr{C}^{1/2}(r_{\rm ms})}}
$$

Since $\mathscr{C}(r_{\rm ms}) = 0$, the efficiency is evaluated via L'Hôpital or from the explicit ISCO energy formula.

| $a_*$ | $r_{\rm ms}/M$ | $\tilde{E}_{\rm ms}$ | $\eta$ |
|--------|-----------------|----------------------|--------|
| $0$ | $6$ | $0.9428$ | $5.72\%$ |
| $0.5$ | $4.233$ | $0.9179$ | $8.21\%$ |
| $0.9$ | $2.321$ | $0.8547$ | $15.5\%$ |
| $0.95$ | $1.937$ | $0.8274$ | $17.3\%$ |
| $0.998$ | $1.237$ | $0.7415$ | $25.9\%$ |
| $1$ | $1$ | $0.5774$ | $42.3\%$ |

For comparison: nuclear burning efficiency $\sim 0.7\%$, matter-antimatter annihilation $= 100\%$.

### 13.2 Eddington Luminosity

The maximum luminosity at which radiation pressure balances gravity for spherical accretion:

$$
L_{\rm crit} = \frac{4\pi G M m_p c}{\sigma_T} \simeq 1.3 \times 10^{38}\;{\rm erg\,s^{-1}}\;\left(\frac{M}{M_\odot}\right)
\tag{5.2.11a}
$$

### 13.3 Critical Accretion Rate

Setting $L = \eta\,\dot{M}_0\,c^2 = L_{\rm crit}$:

$$
\dot{M}_{\rm crit} = \frac{L_{\rm crit}}{\eta\,c^2} \sim 10^{-8}\;M_\odot\,{\rm yr^{-1}}\;\left(\frac{M}{M_\odot}\right)\left(\frac{0.1}{\eta}\right)
\tag{5.2.11b}
$$

The NT thin-disk model is valid for $\dot{M}_0 \ll \dot{M}_{\rm crit}$. At $\dot{M}_0 \gtrsim \dot{M}_{\rm crit}$, radiation pressure inflates the disk, violating the thin-disk assumption $h \ll r$, and the disk transitions to a geometrically thick ("slim disk" or "Polish doughnut") configuration.

### 13.4 Gravitational Binding Energy at the Inner Edge

| Compact object | $\tilde{E}_{\rm bind}$ | Inner edge |
|---------------|------------------------|-----------|
| White dwarf | $\sim 10^{-4}$ | Stellar surface |
| Neutron star | $\sim 0.05$ | Stellar surface |
| Schwarzschild BH | $0.0572$ | $r_{\rm ms} = 6M$ |
| Extreme Kerr BH | $0.423$ | $r_{\rm ms} = M$ |

---

## 14. Validity, Limitations, and Modern Extensions

### 14.1 GRMHD Validation

Penna, McKinney, et al. (2010) performed 3D GRMHD simulations of thin accretion disks and compared against the NT model. Key findings:

- For thin disks ($h/r \lesssim 0.1$) around non-spinning holes, the angular momentum profile deviates from NT by only $\sim 2.9\%$, and the luminosity by $\sim 3.5\%$.
- Deviations decrease with decreasing $h/r$.
- Conclusion: *"Magnetized thin accretion disks in X-ray binaries in the thermal/high-soft spectral state ought to be well-described by the NT model."*

### 14.2 Where the NT Model Breaks Down

| Regime | Failure mode | Alternative model |
|--------|-------------|-------------------|
| $\dot{M}_0 \gtrsim \dot{M}_{\rm crit}$ | Disk becomes geometrically thick; $h \sim r$ | Slim disk (Abramowicz et al. 1988) |
| Magnetically arrested disk (MAD) | Magnetic flux saturates; jet launching | MAD models (Narayan et al. 2003) |
| Low-$\dot{M}_0$ ($\dot{M}_0 \ll 0.01\,\dot{M}_{\rm crit}$) | Disk becomes optically thin, radiatively inefficient | ADAF/RIAF (Narayan & Yi 1994) |
| Strong jets (Blandford-Znajek) | Energy extraction from BH spin | Force-free electrodynamics |
| Inner region ($p = p_{\rm rad}$) | Thermal and viscous instability | Time-dependent models |
| Non-zero torque at ISCO | Magnetic stresses can thread $r_{\rm ms}$ | Extended NT with ISCO stress |

### 14.3 The Inner Region Instability

The radiation-pressure-dominated inner zone is both thermally and viscously unstable (Shakura & Sunyaev 1976; Lightman & Eardley 1974). A local increase in temperature raises radiation pressure, increasing the viscous stress ($t_{\hat{\phi}\hat{r}} = \alpha\,p_{\rm rad}$), generating more heat — a runaway. This instability may produce limit-cycle behavior in some X-ray binaries.

### 14.4 The Continuum Fitting Method

The NT model is the theoretical foundation for measuring black hole spins via X-ray continuum fitting (Zhang, Cui & Chen 1997; Li et al. 2005; McClintock et al. 2006). The method:

1. Observe the thermal X-ray spectrum of an accreting BH in the thermal/high-soft state.
2. Fit the observed spectrum to the NT model flux $F(r; M, a_*, \dot{M}_0)$ integrated over the disk and projected to the observer.
3. Extract $a_*$ from the best fit.

This method has yielded spin measurements for $\gtrsim 20$ stellar-mass black holes, with the NT model providing the theoretical $F(r)$ at its core.

---

## Summary of the Central Equations

The complete NT disk model, at its mathematical core, reduces to:

| Equation | Content | NT ref. |
|----------|---------|---------|
| $\Omega = M^{1/2}/(r^{3/2}\mathscr{B})$ | Orbital angular velocity | (5.4.3) |
| $\tilde{E} = \mathscr{G}/\mathscr{C}^{1/2}$ | Specific energy | (5.4.7b) |
| $\tilde{L} = M^{1/2}r^{1/2}\mathscr{F}/\mathscr{C}^{1/2}$ | Specific angular momentum | (5.4.7a) |
| $W = (\dot{M}_0/2\pi)(M/r^3)^{1/2}\mathscr{Q}^{1/2}/(\mathscr{B}\mathscr{G})$ | Integrated stress | (5.6.14a) |
| $F = (3\dot{M}_0/8\pi r^2)(M/r)\,\mathscr{Q}/(\mathscr{C}^{1/2}\mathscr{B})$ | Radiative flux | (5.6.14b) |
| $\dot{M}_0 = -2\pi r\Sigma\bar{v}^{\hat{r}}\mathscr{D}^{1/2}$ | Mass conservation | (5.6.14c) |
| $t_{\hat{\phi}\hat{r}} = \alpha\,p$ | Viscosity prescription | (5.2.32) |
| $\eta = 1 - \tilde{E}_{\rm ms}$ | Radiative efficiency | — |

Given only three inputs — $M$, $a$, $\dot{M}_0$ — these equations determine the complete radial and (approximate) vertical structure of a thin accretion disk around a Kerr black hole.
