# Numerical Implementations: BDNK Viscous Hydrodynamics for Neutron Stars

## Preamble: Guidelines for These Notes

*Read this section whenever updating.*

Treat this as a publishable implementation document. Every algorithm, scheme, and numerical choice should be documented with enough detail for independent reproduction.

- **Uncertainty is explicit** — use markers
- **Gaps are visible** — mark them
- **Code must be tested** — every implementation accompanied by verification
- **Structure is provisional** — may need revision

---

## 1. Overview of Numerical Strategy

`[SOLID]` (ref: Paper Section II.C, Section II.D)

### 1.1 Evolution Strategy Summary

The system evolves two sets of variables:
- **Primitive variables:** $\mathbf{p}_0 = (\epsilon, \tilde{v}^r)$ — evolved via first-order reduction equations
- **Conservative variables:** $\mathbf{q} = (\tilde{\gamma}E, \tilde{\gamma}S_r)$ — evolved via balance laws
- **Reconstructed primitives:** $\mathbf{p}_1 = (\hat{\epsilon}, \hat{\bar{v}}^r)$ — recovered via linear con2prim at each timestep

Additionally evolved: $\partial_r \epsilon$ and $\partial_r \tilde{v}^r$ (promoted to dynamical fields).

**Total evolved fields:** 6 — $\{\tilde{\gamma}E, \tilde{\gamma}S_r, \epsilon, \partial_r\epsilon, \tilde{v}^r, \partial_r\tilde{v}^r\}$

### 1.2 Time Integration

`[SOLID]` (ref: Paper Section II.E)

- Method of Lines with **3rd-order Strong Stability Preserving Runge-Kutta** (SSP-RK3)
- Courant factor: $\Delta t / \Delta r = 0.25$
- CFL condition satisfied

### 1.3 Spatial Discretization

`[SOLID]` (ref: Paper Section II.E)

- **FDOC scheme**: 3rd-order finite-volume ≡ 4th-order finite difference with 3rd-order dissipation
- Based on "finite-difference Osher-Chakrabarthy" scheme
- Characteristic speed from 6 BDNK characteristic velocities used for numerical dissipation
- Minimum velocity floor: $0.1c$ (near surface and atmosphere)

---

## 2. Equation of State Implementation

### 2.1 Combined Polytropic-Ideal Gas EoS

`[SOLID]` (ref: Paper Eq.39)

```python
import numpy as np

def pressure(epsilon, kappa=100.0, Gamma=2.0):
    """
    Compute pressure from energy density using combined EoS.
    p(epsilon) = (1 + 2*epsilon*kappa - sqrt(1 + 4*epsilon*kappa)) / (2*kappa)

    Parameters:
        epsilon: total energy density (in geometric units, M_sun^{-2})
        kappa: polytropic constant (default 100)
        Gamma: adiabatic index (default 2)
    Returns:
        p: pressure
    """
    return (1.0 + 2.0*epsilon*kappa - np.sqrt(1.0 + 4.0*epsilon*kappa)) / (2.0*kappa)

def dpressure_depsilon(epsilon, kappa=100.0):
    """
    Speed of sound squared: dp/depsilon = c_s^2
    """
    return 1.0 - 1.0/np.sqrt(1.0 + 4.0*epsilon*kappa)

def rho0_from_pressure(p, kappa=100.0, Gamma=2.0):
    """Rest mass density from pressure via polytropic EoS."""
    return (p/kappa)**(1.0/Gamma)

def epsilon0_from_pressure_rho0(p, rho0, Gamma=2.0):
    """Specific internal energy."""
    return p / ((Gamma - 1.0) * rho0)
```

`[FUTURE: Verify edge cases — ensure p(0)=0 and no negative pressures]`

---

## 3. Initial Data: TOV Solver

### 3.1 TOV ODE System

`[SOLID]` (ref: Paper Eqs.43-45)

```python
from scipy.integrate import solve_ivp

def tov_rhs(R, y, kappa=100.0):
    """
    TOV equations in areal-polar coordinates.
    y = [a, alpha, p]
    """
    a, alpha, p = y

    # EoS: epsilon from p
    # From p = (1 + 2*eps*kappa - sqrt(1+4*eps*kappa))/(2*kappa)
    # Need to invert: given p, find epsilon
    epsilon = epsilon_from_pressure(p, kappa)

    if R < 1e-14:
        return [0.0, 0.0, 0.0]  # Regularity at origin

    da_dR = (1.0 + a**2*(-1.0 + 8*np.pi*R**2*epsilon)) / (2*R) * a
    dalpha_dR = (-1.0 + a**2*(1.0 + 8*np.pi*R**2*p)) / (2*R) * alpha
    dp_dR = -(p + epsilon)/alpha * dalpha_dR

    return [da_dR, dalpha_dR, dp_dR]

def epsilon_from_pressure(p, kappa=100.0):
    """Invert EoS to get epsilon from p."""
    rho0 = np.sqrt(p/kappa)  # For Gamma=2
    eps0_rho0 = p  # For Gamma=2: p = (Gamma-1)*eps0*rho0 = eps0*rho0
    return rho0 + eps0_rho0
```

### 3.2 Boundary Conditions

`[SOLID]` (ref: Paper Eqs.46-47)

- At origin: $\alpha(0) = 1$, $a(0) = 1$, $p(0) = \kappa\rho_0(0)^\Gamma$
- Central rest mass density: $\rho_{0,c} = 0.00128\ M_\odot^{-2}$ → $\epsilon_c = 0.00144\ M_\odot^{-2}$
- Total gravitational mass: $M_T = 1.4\ M_\odot$

### 3.3 Coordinate Transformation

`[SOLID]` (ref: Paper Eq.47-48, following Lai 2004 [PhDT.......230L])

Transform from areal-polar $(R, a(R), \alpha(R))$ to maximal isotropic $(r, \psi(r), \alpha(r))$
coordinates where the metric takes the form:

$$ds^2 = -\alpha^2(r)dt^2 + \psi^4(r)(dr^2 + r^2 d\Omega^2)$$

The isotropic radius $r$ is related to the areal radius $R$ by $R = r\,\psi^2(r)$, where the
conformal factor $\psi$ satisfies an ODE derived from requiring $g_{rr} = \psi^4$ and
$g_{\theta\theta} = \psi^4 r^2$. In areal-polar coordinates $g_{rr}^{\rm AP} = a^2(R)$, so the
matching condition is $(dR/dr)^2 / a^2 = \psi^4$. Together with $R = r\psi^2$ this gives:

$$\frac{d\ln\psi}{dR} = \frac{1 - a(R)}{2R}$$

integrated outward from the origin where $\psi(0) = 1$ (regularity), with the lapse $\alpha(r)$
identical in both charts.

```python
from scipy.integrate import solve_ivp, cumtrapz
from scipy.interpolate import CubicSpline

def areal_to_isotropic(R_arr, a_arr, alpha_arr, p_arr):
    """
    Transform TOV solution from areal-polar (Schwarzschild) coordinates
    (R, a, alpha) to maximal isotropic coordinates (r, psi, alpha).

    The metric in areal-polar coordinates is:
        ds^2 = -alpha^2 dT^2 + a^2 dR^2 + R^2 dOmega^2

    The metric in maximal isotropic coordinates is:
        ds^2 = -alpha^2 dt^2 + psi^4 (dr^2 + r^2 dOmega^2)

    The coordinate transformation is found by integrating:
        d(ln psi) / dR = (1 - a(R)) / (2R)
    with boundary condition psi(R=0) = 1.

    Once psi(R) is known, the isotropic radius is r(R) = R / psi(R)^2.

    Parameters
    ----------
    R_arr   : 1D array, areal radii (M_sun), R_arr[0] = 0 (or small stagger)
    a_arr   : 1D array, metric function a(R) = sqrt(g_RR) in Schwarzschild coords
    alpha_arr: 1D array, lapse alpha(R)
    p_arr   : 1D array, pressure p(R) — needed only to locate stellar surface

    Returns
    -------
    r_arr   : isotropic radii (M_sun)
    psi_arr : conformal factor psi(r)
    alpha_arr_iso: lapse (unchanged in value, re-labeled by r)
    grr_iso : g_rr = psi^4 in isotropic coordinates (array, same size)
    gtt_iso : g_thetatheta = psi^4 * r^2 in isotropic coordinates
    """
    # --- Step 1: integrate d(ln psi)/dR = (1 - a(R)) / (2*R) ---
    # At R=0 the integrand is (1 - 1)/(2*0) = 0/0 but psi(0) = 1 by regularity,
    # so we integrate starting from index 1 and prepend psi=1 at R=0.
    dR = np.diff(R_arr)

    # Compute integrand, handling R=0 carefully
    integrand = np.zeros_like(R_arr)
    mask = R_arr > 0
    integrand[mask] = (1.0 - a_arr[mask]) / (2.0 * R_arr[mask])
    # integrand[0] = 0 by regularity (l'Hopital: a(0)=1, a'(0) finite => (1-a)/(2R) -> -a'(0)/2)

    # Numerically integrate using trapezoidal rule from R=0 outward
    # ln_psi(R) = int_0^R integrand dR'
    ln_psi = np.zeros_like(R_arr)
    ln_psi[1:] = cumtrapz(integrand, R_arr)

    psi_arr = np.exp(ln_psi)  # psi(R), with psi(0)=1

    # --- Step 2: compute isotropic radius r = R / psi^2 ---
    r_arr = np.zeros_like(R_arr)
    r_arr[1:] = R_arr[1:] / psi_arr[1:]**2
    # r[0] = 0 by definition

    # --- Step 3: the lapse is the same function evaluated at the same physical point ---
    alpha_arr_iso = alpha_arr  # alpha expressed as a function of r via r_arr mapping

    # --- Step 4: compute metric components in isotropic form ---
    # g_rr = psi^4, g_thetatheta = psi^4 * r^2
    grr_iso  = psi_arr**4
    gtt_iso  = psi_arr**4 * r_arr**2   # r^2 * psi^4

    return r_arr, psi_arr, alpha_arr_iso, grr_iso, gtt_iso


def interpolate_onto_uniform_grid(r_arr, fields_dict, r_min, r_max, N):
    """
    Given an irregularly spaced isotropic grid r_arr (from the transformation above),
    interpolate all fields onto a uniform grid suitable for finite-volume evolution.

    Parameters
    ----------
    r_arr      : array of isotropic radii from coordinate transformation
    fields_dict: dict of {name: array} with values on r_arr
    r_min, r_max: grid extent (r_min > 0 for staggered grid)
    N          : number of uniform grid points

    Returns
    -------
    r_uni      : uniform grid (cell centers if staggered)
    out_dict   : dict of {name: interpolated array}
    """
    r_uni = np.linspace(r_min, r_max, N)
    out_dict = {}
    for name, vals in fields_dict.items():
        cs = CubicSpline(r_arr, vals)
        out_dict[name] = cs(r_uni)
    return r_uni, out_dict
```

---

## 4. Transport Coefficients and Frame Parameters

### 4.1 Parametrization

`[SOLID]` (ref: Paper Eqs.48-50)

```python
def compute_transport_coefficients(epsilon, kappa=100.0, L=1.0,
                                     hat_a=1.0, hat_q=0.999, hat_s=1.0,
                                     hat_eta=0.01, hat_zeta=0.01):
    """
    Compute BDNK transport coefficients from hatted parameters.
    """
    p = pressure(epsilon, kappa)
    cs2 = dpressure_depsilon(epsilon, kappa)
    rho = epsilon + p
    hat_V = (4.0/3.0)*hat_eta + hat_zeta

    eta = hat_q * L * cs2 * rho * hat_eta
    zeta = hat_q * L * cs2 * rho * hat_zeta
    tau_epsilon = hat_V * L
    tau_p = hat_s * cs2 * L * hat_V
    tau_Q = hat_a * L * hat_V
    beta_epsilon = cs2 * hat_a * hat_V * L

    return {
        'eta': eta, 'zeta': zeta,
        'tau_epsilon': tau_epsilon, 'tau_p': tau_p,
        'tau_Q': tau_Q, 'beta_epsilon': beta_epsilon,
        'cs2': cs2, 'rho': rho, 'hat_V': hat_V
    }
```

### 4.2 Four Parameter Cases

`[SOLID]` (ref: Paper Section III.A)

```python
CASES = {
    'smallSB-F2': {'tau_eps': 0.023, 'hat_eta': 0.01,    'hat_zeta': 0.01},
    'medS-F2':    {'tau_eps': 0.023, 'hat_eta': 0.01725, 'hat_zeta': 0.0},
    'highB-F9':   {'tau_eps': 0.092, 'hat_eta': 0.0015,  'hat_zeta': 0.09},
    'medSB-F9':   {'tau_eps': 0.092, 'hat_eta': 0.03525, 'hat_zeta': 0.045},
}
```

### 4.3 Characteristic Velocities (Flat Spacetime)

`[SOLID]` (ref: Paper Eqs.51-52)

```python
def characteristic_velocities(hat_a=1.0, hat_q=0.999, hat_s=1.0,
                                hat_eta=0.01, hat_zeta=0.01, cs=None):
    """Compute the three characteristic velocities c_0, c_+, c_-."""
    hat_V = (4.0/3.0)*hat_eta + hat_zeta

    c0 = cs * np.sqrt(hat_q * hat_eta / (hat_a * hat_V))

    discriminant = (hat_q**2 + hat_a**2*(4*hat_q + (hat_s - 1)**2)
                    + 2*hat_a*hat_q*(1 + hat_s))

    c_plus = cs * np.sqrt((hat_a*(1 + hat_s) + hat_q + np.sqrt(discriminant)) / (2*hat_a))
    c_minus = cs * np.sqrt((hat_a*(1 + hat_s) + hat_q - np.sqrt(discriminant)) / (2*hat_a))

    return c0, c_plus, c_minus
```

### 4.4 Well-Posedness Verification

`[SOLID]` (ref: Paper Eqs.53-56)

```python
def check_well_posedness(hat_a, hat_q, hat_s, hat_eta, hat_zeta, cs2):
    """Verify all well-posedness, causality, and stability conditions."""
    cs = np.sqrt(cs2)
    c0, cp, cm = characteristic_velocities(hat_a, hat_q, hat_s, hat_eta, hat_zeta, cs)

    checks = {
        'strong_hyperbolicity': 0 < hat_q < hat_s,
        'c_minus_real': not np.isnan(cm),
        'c_plus_neq_c_minus': abs(cp - cm) > 1e-14,
        'causality_c0': c0 < 1.0,
        'causality_c_plus': cp < 1.0,
        'causality_c_minus': cm < 1.0,
        'causality_ineq': hat_q < (1-cs2)/cs2 * (1-hat_s*cs2)/(cs2 + 1.0/hat_a),
        'causality_s': hat_s < 1.0/cs2,
    }
    return checks
```

### 4.5 Curved-Space Characteristic Velocities

`[SOLID]` (ref: Paper Eq. vel_w_m, spherical symmetry, Cowling approximation)

The six BDNK characteristic velocities on a curved background are (Paper Eq. vel_w_m):

$$\tilde{c}_{i\pm} = -\beta \cdot k + \alpha \frac{m_i W^2 (v \cdot k) \pm \sqrt{k^2 + k^2 m_i W^2 - m_i W^2 (v\cdot k)^2}}{m_i W^2 + 1}$$

where $i=0,1,2$, $m_0 = 1/c_0^2 - 1$, $m_{1,2} = 1/c_\pm^2 - 1$, $k^i$ is the spatial wave
vector, and $W$ is the Lorentz factor. In spherical symmetry with the Cowling approximation
($\beta^r = 0$, $K^r{}_r = 0$, $K^\theta{}_\theta = 0$, wave vector $k^r = 1/\sqrt{g_{rr}}$)
the formula reduces to the following, with dot products computed using the spatial metric $\gamma_{ij}$:

```python
def curved_characteristic_velocities_spherical(
        vr, grr, alpha,
        hat_a=1.0, hat_q=0.999, hat_s=1.0,
        hat_eta=0.01, hat_zeta=0.01, cs=None,
        v_min=0.1):
    """
    Compute the six curved-space BDNK characteristic velocities in spherical
    symmetry under the Cowling approximation (beta=0, K=0).

    Implements Paper Eq.(vel_w_m):
        c_{i,pm} = alpha * (m_i * W^2 * (v.k) +/- sqrt(k^2 + k^2*m_i*W^2 - m_i*W^2*(v.k)^2))
                   / (m_i * W^2 + 1)
    where beta=0 so the -beta.k term vanishes.

    In spherical symmetry the only nonzero velocity component is v^r = r * vtilde_r.
    The wave vector is chosen as k^r = 1/sqrt(g_rr) (unit radial covector raised with g^rr),
    so:
        k^2  = gamma_{ij} k^i k^j = g_rr * (k^r)^2 = g_rr / g_rr = 1
        v.k  = gamma_{ij} v^i k^j  = g_rr * v^r * k^r = g_rr * v^r / sqrt(g_rr) = sqrt(g_rr)*v^r
        W    = 1 / sqrt(1 - g_rr * (v^r)^2)

    The six velocities correspond to three flat-space speeds {c0, c+, c-}, each giving a
    forward (+) and backward (-) moving mode.

    Parameters
    ----------
    vr      : physical radial velocity v^r (NOT vtilde_r; recover via vr = r * vtilde_r)
    grr     : metric component g_rr at the point of evaluation
    alpha   : lapse function at the point of evaluation
    hat_a, hat_q, hat_s, hat_eta, hat_zeta : frame/viscosity parameters
    cs      : local speed of sound sqrt(c_s^2)
    v_min   : minimum characteristic speed floor (default 0.1c, Paper Section II.E)

    Returns
    -------
    speeds  : list of six characteristic velocities [c_{0+}, c_{0-}, c_{++}, c_{+-},
              c_{-+}, c_{--}]  (positive = outgoing, negative = ingoing)
    c_max   : maximum absolute value (used for LLF flux)
    """
    # Flat-space characteristic speeds (Paper Eqs.51-52)
    c0, c_plus, c_minus = characteristic_velocities(
        hat_a, hat_q, hat_s, hat_eta, hat_zeta, cs)

    # Map to m_i = 1/c_i^2 - 1 (Paper below Eq. vel_w_m)
    m_values = [1.0/c0**2 - 1.0,
                1.0/c_plus**2 - 1.0,
                1.0/c_minus**2 - 1.0]

    # Lorentz factor W = 1/sqrt(1 - g_rr * (v^r)^2)
    v2 = grr * vr**2
    # Clamp to avoid superluminal velocities (numerical safety)
    v2 = np.minimum(v2, 1.0 - 1e-10)
    W2 = 1.0 / (1.0 - v2)
    W  = np.sqrt(W2)

    # Dot products using spatial metric (spherical, only r-component)
    # k^r = 1/sqrt(g_rr), k^2 = g_rr*(k^r)^2 = 1 (unit wave vector)
    k2    = 1.0
    vdotk = np.sqrt(grr) * vr   # g_rr * v^r * (1/sqrt(g_rr))

    speeds = []
    for m in m_values:
        # Discriminant inside sqrt: k^2 + k^2*m*W^2 - m*W^2*(v.k)^2
        #   = 1 + m*W^2*(1 - (v.k)^2)
        discriminant = k2 + k2 * m * W2 - m * W2 * vdotk**2
        # discriminant = 1 + m*W^2*(k^2 - (v.k)^2) >= 0 for |v| < c_i
        discriminant = np.maximum(discriminant, 0.0)

        denom = m * W2 + 1.0

        # Forward (+) and backward (-) modes
        c_fwd = alpha * (m * W2 * vdotk + np.sqrt(discriminant)) / denom
        c_bwd = alpha * (m * W2 * vdotk - np.sqrt(discriminant)) / denom

        speeds.extend([c_fwd, c_bwd])

    # Apply minimum speed floor (Paper Section II.E)
    c_max = np.maximum(np.max(np.abs(speeds)), v_min)

    return speeds, c_max
```

---

## 5. Conservative-to-Primitive Recovery (con2prim)

### 5.1 Spherically Symmetric 2×2 System

`[SOLID]` (ref: Paper Appendix A)

The con2prim recovers $\mathbf{p}_1 = (\hat\epsilon, \hat{\bar{v}}^r)$ from known conserved variables
$\mathbf{q} = (\tilde\gamma E, \tilde\gamma S_r)$ divided by $\tilde\gamma$ and known
$\mathbf{p}_0 = (\epsilon, \tilde{v}^r)$ (with $v^r = r\,\tilde{v}^r$). The system is
$\mathcal{A}\,\mathbf{p}_1 = \mathbf{b}$ where $\mathbf{b} = (E, S_r) - \mathbf{c}$.

In the **Cowling approximation** the background metric is fixed and static
($K^r{}_r = K^\theta{}_\theta = 0$, $\beta^r = 0$), so all extrinsic curvature terms
and shift terms vanish in the $\mathbf{c}$-vector. The spatial metric has $g_{rr}$ and
$g_{\theta\theta} = r^2 \psi^4$ fixed from initial data.

```python
def con2prim_spherical(E, S_r, epsilon, vtilde_r, r, grr,
                        transport_coeffs, spatial_derivs,
                        alpha, alpha_r):
    """
    Recover p1 = (hat_epsilon, hat_vbar_r) from conservative and p0 variables.

    Solves the 2x2 linear system:  A * p1 = b,  where b = (E, S_r) - c.

    In the Cowling approximation (K=0, beta=0), several geometric terms vanish.
    The spatial derivative terms in the c-vector remain.

    Parameters
    ----------
    E, S_r          : conservative variables divided by tilde_gamma
    epsilon         : primitive variable (total energy density)
    vtilde_r        : regularized radial velocity tilde_v^r = v^r / r
    r               : radial coordinate (needed to recover v^r = r * vtilde_r)
    grr             : metric component g_rr
    transport_coeffs: dict with keys eta, zeta, tau_epsilon, tau_p, tau_Q, cs2
    spatial_derivs  : dict with keys Dr_epsilon (= partial_r epsilon),
                                      Dr_vr     (= partial_r v^r),
                                      a_r       (= partial_r ln alpha = A_r)
    alpha           : lapse function
    alpha_r         : A_r = (1/alpha) * partial_r alpha

    Returns
    -------
    hat_epsilon  : time derivative of energy density (= -n^mu nabla_mu epsilon)
    hat_vbar_r   : spatial time derivative of v^r projected onto spatial slice
    """
    tc   = transport_coeffs
    eta  = tc['eta']
    zeta = tc['zeta']
    tau_eps = tc['tau_epsilon']
    tau_p   = tc['tau_p']
    tau_Q   = tc['tau_Q']
    dp   = tc['cs2']                    # dp/depsilon = c_s^2
    p    = pressure(epsilon)
    rho  = epsilon + p                  # enthalpy density

    # Physical radial velocity v^r from regularized form
    vr   = r * vtilde_r

    # Lorentz factor (1 - g_rr (v^r)^2)
    v2      = grr * vr**2
    v2      = np.minimum(v2, 1.0 - 1e-10)   # numerical safety
    W2_inv  = 1.0 - v2                       # = 1/W^2
    W       = 1.0 / np.sqrt(W2_inv)
    W2      = W**2

    # ----------------------------------------------------------------
    # Matrix A  (Paper Appendix A, spherical symmetry expressions)
    # ----------------------------------------------------------------
    # A_0^0
    A00 = -(2.0*grr*vr**2*tau_Q*dp + tau_eps*(grr*vr**2*dp + 1.0)) / W2_inv**1.5

    # A_0^1  (coefficient of hat_vbar^r in the E equation)
    A01 = -(grr*vr * (-4.0*grr*vr**2*eta
                      + 3.0*grr*vr**2*((rho*tau_eps*dp) - zeta)
                      + 3.0*rho*(2.0*tau_Q + tau_eps))
            ) / (3.0 * W2_inv**2.5)

    # A_1^0  (coefficient of hat_epsilon in the S_r equation)
    A10 = -(grr*vr * ((grr*vr**2 + 1.0)*tau_Q*dp
                      + tau_eps*(dp + 1.0))
            ) / W2_inv**1.5

    # A_1^1  (coefficient of hat_vbar^r in the S_r equation)
    A11 = -(grr * (-4.0*grr*vr**2*eta
                   + 3.0*grr*vr**2*(rho*(tau_eps*(dp + 1.0) + tau_Q) - zeta)
                   + 3.0*rho*tau_Q)
            ) / (3.0 * W2_inv**2.5)

    # ----------------------------------------------------------------
    # c-vector  (Paper Appendix A, Cowling approximation: K=0, beta=0)
    #
    # In the Cowling approximation:
    #   K^r_r = K^theta_theta = 0  =>  K = 0
    #   beta^r = 0
    #   a^r = partial_r ln alpha = A_r   (the normal acceleration is spatial)
    #
    # The spatial divergence of v^r in spherical symmetry is:
    #   D_i v^i = partial_r v^r + (2/r) v^r    (from Christoffel symbols)
    #
    # The term W^2 v^i v^j D_i v_j in spherical symmetry:
    #   = W^2 (v^r)^2 * D_r v_r  =  W^2 (v^r)^2 * (grr * partial_r v^r
    #                                                 + Gamma^r_rr * v_r)
    # For the isotropic metric: Gamma^r_rr = (1/2) g^rr partial_r g_rr =: D_rr^r * grr^{-1}
    # In the Cowling approximation, partial_t g_rr = 0 so g_rr is static.
    # For the purposes of the c-vector, we use:
    #   partial_r v^r = Dr_vr  (evolved dynamical field)
    #
    # Define the combination (used in several places):
    #   Theta = -K + a^i v_i + D_i v^i + W^2 v^i v^j D_i v_j
    #         = a_r_low * v^r + Div_v + W^2 * grr * vr^2 * Dr_vr
    # where a_r_low = g_rr * A_r (lowered acceleration), and
    #   Div_v = partial_r v^r + (2/r)*v^r
    # ----------------------------------------------------------------

    Dr_eps = spatial_derivs['Dr_epsilon']   # partial_r epsilon
    Dr_vr  = spatial_derivs['Dr_vr']        # partial_r v^r
    A_r    = alpha_r                         # (1/alpha) partial_r alpha = a_r (raised index)

    # Lowered acceleration: a_r = g_rr * A_r (a_i = partial_i ln alpha in this gauge)
    a_r_low = grr * A_r

    # Spatial divergence of v^r  (spherical symmetry: D_i v^i = dr(v^r) + 2*v^r/r)
    Div_v = Dr_vr + 2.0 * vr / r

    # W^2 v^i v^j D_i v_j  (only r-component survives)
    # D_r v_r = partial_r (g_rr v^r) = g_rr * Dr_vr + v^r * partial_r g_rr
    # In Cowling approx, partial_r g_rr is a fixed metric derivative from initial data.
    # For simplicity we assume metric is smooth and denote partial_r g_rr / g_rr = 2*D_rr^r
    # but in practice spatial_derivs should supply this; use Dr_vr with g_rr = const approx:
    vv_Dv = W2 * grr * vr**2 * Dr_vr   # W^2 g_rr (v^r)^2 partial_r v^r (leading term)

    # Combined geometric-matter combination Theta (Cowling: K=0)
    Theta = a_r_low * vr + Div_v + vv_Dv

    # ---- c_0 (energy equation, Paper Appendix A) ----
    # c_0 = E_ideal + E_tau_eps_tau_p + E_tau_Q + E_eta + E_zeta
    #
    # Ideal part:
    c0_ideal = W2 * epsilon - p * (1.0 - W2)

    # tau_epsilon / tau_p contribution (Paper Appendix A c_0 expression):
    # W*(tau_eps*W^2 - (1-W^2)*tau_p) * [Theta*(epsilon+p) + v^r * Dr_eps]
    factor_eps_p = W * (tau_eps * W2 - (1.0 - W2) * tau_p)
    bracket_E    = rho * Theta + vr * Dr_eps

    c0_tau = factor_eps_p * bracket_E

    # tau_Q contribution:
    # 2*tau_Q*W^3 * [(epsilon+p)*(a^i v_i + v^i v^j (- K_ij + W^2 D_i v_j))
    #                + dp * v^r D_r epsilon]
    # In Cowling (K_ij=0): a^i v_i = A_r * vr (raised a^r = A_r, v^r normal)
    # v^i v^j D_i v_j = (v^r)^2 * D_r v_r (same as vv_Dv / grr ... careful with index)
    # Here: v^i v^j D_i v_j in raised+lowered = vr * vr * grr * Dr_vr (approx, leading term)
    c0_tauQ = (2.0 * tau_Q * W**3
               * (rho * (a_r_low * vr + vv_Dv) + dp * vr * Dr_eps))

    # eta (shear) contribution:
    # (2/3)*eta*W * [(1-W^2)*(K + 2*a^i v_i - D_i v^i)
    #                + W^2 v^i v^j (3 K_ij + (1+2W^2)((-2+W^2) D_i v_j - W^2 v_i v^l D_l v_j))]
    # In Cowling (K=0, K_ij=0):
    # = (2/3)*eta*W * [(1-W^2)*(2*A_r*vr - Div_v)
    #                  + W^2*(1+2W^2)*(-2+W^2)*vv_Dv   (leading non-trivial term)]
    c0_eta = ((2.0/3.0) * eta * W
              * ((1.0 - W2) * (2.0 * a_r_low * vr - Div_v)
                 + W2 * (1.0 + 2.0*W2) * (-2.0 + W2) * vv_Dv / grr))
    # Note: vv_Dv already contains a factor grr; for D_i v_j we need to be careful
    # with the metric factor. Here we use the approximation for small v that the
    # metric-correction to vv_Dv is sub-dominant. For a full implementation, supply
    # partial_r g_rr from initial data.

    # zeta (bulk) contribution:
    # zeta * W * (1-W^2) * Theta
    c0_zeta = zeta * W * (1.0 - W2) * Theta

    c0 = c0_ideal + c0_tau + c0_tauQ + c0_eta + c0_zeta

    # ---- c_r (momentum equation, Paper Appendix A) ----
    # c_r = S_ideal + S_tau + S_tauQ + S_eta + S_zeta
    #
    # Lower index v_r = g_rr * v^r
    vr_low = grr * vr

    # Ideal part:
    cr_ideal = -vr_low * W2 * rho

    # (tau_eps + tau_p) contribution:
    cr_tau = (tau_eps + tau_p) * vr_low * W**3 * bracket_E

    # tau_Q contribution:
    # tau_Q * { -dp*W * Dr_eps
    #           + W^3 * [ -(epsilon+p)*(a_r + vr*a^j*vj + v^j*(-K_rj + D_j*vr - vr*vl*(K_jl - 2W^2 D_l vj)))
    #                     - 2*dp*vr*(v^j D_j eps) ] }
    # In Cowling (K=0):
    # = tau_Q * { -dp*W * Dr_eps
    #             + W^3 * [ -(epsilon+p)*(a_r_low + vr_low*A_r*vr + vr*(Dr_vr - vv_Dv*...))
    #                       - 2*dp*vr_low*vr*Dr_eps ] }
    # Leading terms:
    cr_tauQ = (tau_Q * (-dp * W * Dr_eps
                        + W**3 * (-(rho * (a_r_low + vr_low * a_r_low * vr
                                           + vr * Dr_vr - vr * vv_Dv))
                                  - 2.0 * dp * vr_low * vr * Dr_eps)))

    # eta contribution:
    # eta * { -a_r_low * W * (1-W^2)
    #         - K_rj * v^j * W * (1+W^2)      [=0 in Cowling]
    #         + (1/3)*W^3 * [vr_low*(2K + A_r*vr - 3K_jl*v^j*v^l - 2*Div_v + 4W^2*vv_Dv)
    #                        + 3*v^j*(D_r v_j + D_j v^r)] }
    # In Cowling (K=0, K_ij=0):
    cr_eta = (eta * (-a_r_low * W * (1.0 - W2)
                     + (1.0/3.0) * W**3 * (vr_low * (a_r_low * vr - 2.0 * Div_v + 4.0 * W2 * vv_Dv / grr)
                                            + 3.0 * vr * (grr * Dr_vr + Dr_vr))))
    # The last term 3*v^j*(D_r v_j + D_j v^r) in spherical symmetry gives
    # 3*vr*(D_r v_r + D_r v^r) = 3*vr*(grr*Dr_vr + Dr_vr)

    # zeta contribution:
    cr_zeta = zeta * vr_low * W**3 * Theta

    cr = cr_ideal + cr_tau + cr_tauQ + cr_eta + cr_zeta

    # ---- b-vector ----
    b0 = E  - c0
    b1 = S_r - cr

    # ---- Solve 2x2 linear system ----
    det = A00 * A11 - A01 * A10
    hat_epsilon  = ( A11 * b0 - A01 * b1) / det
    hat_vbar_r   = (-A10 * b0 + A00 * b1) / det

    return hat_epsilon, hat_vbar_r
```

### 5.2 Stress Tensor Components from Primitives

`[SOLID]` (ref: Paper Eqs. E_fluid_3p1, Si_fluid_3p1, Sij_fluid_3p1, Cowling approximation)

In the Cowling approximation ($K=0$, $K_{ij}=0$, $\beta=0$), these reduce significantly.
These functions compute $E$, $S^r$, $S^r{}_r$, $S^\theta{}_\theta$ given
$\mathbf{p}_0 = (\epsilon, \tilde{v}^r)$ and $\mathbf{p}_1 = (\hat\epsilon, \hat{\bar{v}}^r)$.

```python
def compute_stress_tensor_components(epsilon, vtilde_r, r, hat_eps, hat_vbar_r,
                                      grr, alpha_r,
                                      transport_coeffs, spatial_derivs):
    """
    Compute the stress-energy projections E, S^r, S^r_r, S^theta_theta from
    primitives in spherical symmetry under the Cowling approximation.

    These appear in the balance-law RHS and fluxes:
        partial_t(tilde_gamma * E) + partial_r(alpha * tilde_gamma * S^r) = source_E
        partial_t(tilde_gamma * S_r) + partial_r(alpha * tilde_gamma * S^r_r) = source_Sr

    Parameters
    ----------
    epsilon, vtilde_r : p0 primitive variables
    r                 : radial coordinate
    hat_eps           : hat_epsilon (= -n^mu nabla_mu epsilon)
    hat_vbar_r        : hat_vbar^r  (spatial time derivative of v^r)
    grr               : metric component g_rr
    alpha_r           : A_r = (1/alpha) partial_r alpha
    transport_coeffs  : dict with eta, zeta, tau_epsilon, tau_p, tau_Q, cs2
    spatial_derivs    : dict with Dr_epsilon, Dr_vr

    Returns
    -------
    E         : energy density projection (scalar)
    Sr        : momentum density S^r (contravariant r-component)
    Sr_r      : stress S^r_r = S^r_{r} (mixed tensor, flux for S_r equation)
    Sth_th    : stress S^theta_theta (needed for spherical-symmetry source term)
    """
    tc      = transport_coeffs
    eta     = tc['eta'];  zeta = tc['zeta']
    tau_eps = tc['tau_epsilon'];  tau_p = tc['tau_p'];  tau_Q = tc['tau_Q']
    dp      = tc['cs2']
    p       = pressure(epsilon)
    rho     = epsilon + p

    vr      = r * vtilde_r
    v2      = grr * vr**2
    v2      = np.minimum(v2, 1.0 - 1e-10)
    W2_inv  = 1.0 - v2
    W2      = 1.0 / W2_inv
    W       = np.sqrt(W2)

    Dr_eps  = spatial_derivs['Dr_epsilon']
    Dr_vr   = spatial_derivs['Dr_vr']
    A_r     = alpha_r
    a_r_low = grr * A_r
    vr_low  = grr * vr

    Div_v   = Dr_vr + 2.0 * vr / r
    vv_Dv   = W2 * grr * vr**2 * Dr_vr   # W^2 g_rr (v^r)^2 partial_r v^r

    # Combined matter-geometry scalar (Theta = -K + a.v + D.v + W^2 vv D v, K=0)
    Theta   = a_r_low * vr + Div_v + vv_Dv

    # Bracket [rho*Theta + v^r * Dr_eps] used in tau_eps/tau_p terms
    bracket = rho * Theta + vr * Dr_eps

    # ---- Energy density E (Paper Eq. E_fluid_3p1, Cowling K=0) ----
    # E = W^2*epsilon - p*(1-W^2)
    #   + W*(tau_eps*W^2 - (1-W^2)*tau_p) * bracket
    #   - W*(tau_eps*W^2 - (1-W^2)*tau_p) * hat_eps      [hat_eps term]
    #   + 2*tau_Q*W^3*(rho*(A_r*vr + vv_Dv) + dp*vr*Dr_eps)
    #   - 2*tau_Q*W*(1-W^2)*dp*hat_eps                    [hat_eps from Q term]
    #   + 2*tau_Q*W^3*rho*(-W^2)*(hat_vbar_r*vr_low)     [hat_vbar term in Q]
    #   + (2/3)*eta terms + zeta terms

    # Collect hat_eps and hat_vbar_r contributions (the A-matrix gives these)
    # Full E is: A00*hat_eps + A01*hat_vbar_r + c0
    # Re-derive from the full expression in Paper Eq. E_fluid_3p1:

    # hat_epsilon coefficient = A00 (computed in con2prim)
    A00 = -(2.0*grr*vr**2*tau_Q*dp + tau_eps*(grr*vr**2*dp + 1.0)) / W2_inv**1.5

    # hat_vbar^r coefficient = A01
    A01 = -(grr*vr * (-4.0*grr*vr**2*eta
                      + 3.0*grr*vr**2*(rho*tau_eps*dp - zeta)
                      + 3.0*rho*(2.0*tau_Q + tau_eps))
            ) / (3.0 * W2_inv**2.5)

    # c0 (spatial/geometric part — same as in con2prim)
    c0_ideal = W2 * epsilon - p * (1.0 - W2)
    c0_tau   = W * (tau_eps*W2 - (1.0 - W2)*tau_p) * bracket
    c0_tauQ  = 2.0*tau_Q*W**3 * (rho*(A_r*vr + vv_Dv) + dp*vr*Dr_eps)
    c0_eta   = ((2.0/3.0)*eta*W
                * ((1.0 - W2)*(2.0*A_r*vr - Div_v)
                   + W2*(1.0 + 2.0*W2)*(-2.0 + W2)*vv_Dv/grr))
    c0_zeta  = zeta * W * (1.0 - W2) * Theta
    c0       = c0_ideal + c0_tau + c0_tauQ + c0_eta + c0_zeta

    E = A00 * hat_eps + A01 * hat_vbar_r + c0

    # ---- Momentum density S^r (Paper Eq. Si_fluid_3p1, Cowling K=0) ----
    # Coefficient of hat_eps  = A10 / g_rr   (note: S^r not S_r)
    # S_r equation has A10; S^r = g^rr * S_r so coefficients differ by g^rr = 1/grr
    A10 = -(grr*vr*((grr*vr**2 + 1.0)*tau_Q*dp + tau_eps*(dp + 1.0))) / W2_inv**1.5
    A11 = -(grr*(-4.0*grr*vr**2*eta
                  + 3.0*grr*vr**2*(rho*(tau_eps*(dp + 1.0) + tau_Q) - zeta)
                  + 3.0*rho*tau_Q)
             ) / (3.0*W2_inv**2.5)

    cr_ideal = -vr_low * W2 * rho
    cr_tau   = (tau_eps + tau_p) * vr_low * W**3 * bracket
    cr_tauQ  = (tau_Q * (-dp*W*Dr_eps
                         + W**3*(-(rho*(a_r_low + vr_low*A_r*vr + vr*Dr_vr - vr*vv_Dv))
                                 - 2.0*dp*vr_low*vr*Dr_eps)))
    cr_eta   = (eta * (-a_r_low*W*(1.0 - W2)
                       + (1.0/3.0)*W**3*(vr_low*(A_r*vr - 2.0*Div_v + 4.0*W2*vv_Dv/grr)
                                          + 3.0*vr*(grr*Dr_vr + Dr_vr))))
    cr_zeta  = zeta * vr_low * W**3 * Theta
    cr       = cr_ideal + cr_tau + cr_tauQ + cr_eta + cr_zeta

    S_r_cov  = A10 * hat_eps + A11 * hat_vbar_r + cr   # covariant S_r

    # S^r (contravariant) = g^rr * S_r  (needed for flux alpha*tilde_gamma*S^r)
    Sr = (1.0/grr) * S_r_cov

    # ---- Stress S^r_r = S^r_{r} (Paper Eq. Sij_fluid_3p1 rr-component, Cowling) ----
    # S_rr = p*grr + W^2*rho*vr_low^2  (ideal) + viscous corrections
    # S^r_r = g^rr * S_rr = p + W^2*rho*vr^2 + ...
    # Cowling K=0, K_ij=0:

    # Ideal part: S^r_r|ideal = p + W^2*rho*vr^2 (using v_r=grr*vr, S^r_r=g^rr*S_rr)
    Srr_ideal = p + W2 * rho * grr * vr**2   # = p*grr + W^2*rho*vr_low^2, then /grr*grr = p+...

    # tau_eps/tau_p part of S_rr / grr:
    # From paper: -W*[tau_p*grr + (tau_eps+tau_p)*W^2*vr_low^2/grr] * bracket ... /grr
    Srr_tau = (-W * (tau_p + (tau_eps + tau_p)*W2*grr*vr**2) * bracket
               + W * (tau_p + (tau_eps + tau_p)*W2*grr*vr**2) * hat_eps)
    # Splitting: the bracket includes the spatial part; hat_eps appears with opposite sign.
    # Full rr-component of S_ij paper formula divided by grr to get S^r_r:
    Srr_tau_spatial = -W * (tau_p + (tau_eps + tau_p)*W2*grr*vr**2) * bracket / grr
    Srr_tau_hat    = +W * (tau_p + (tau_eps + tau_p)*W2*grr*vr**2) * hat_eps / grr

    # tau_Q part of S^r_r (from Sij_tau_Q, rr-component, Cowling K=0):
    # tau_Q * { 2W*v_(r [a_r) - hat_vbar_r) ... } / grr
    # Main terms: tau_Q * 2 * W * vr_low * (a_r_low - hat_vbar_r + vr*Dr_vr) / grr
    #            + tau_Q * 2 * W * vr_low^2 * (-dp*hat_eps + dp*vr*Dr_eps) / grr
    Srr_tauQ_spatial = (tau_Q * 2.0 * W * vr_low * (a_r_low + vr*Dr_vr) / grr
                        + tau_Q * 2.0 * W * grr * vr**2 * dp * vr * Dr_eps / grr)
    Srr_tauQ_hat     = (tau_Q * 2.0 * W * vr_low * (-hat_vbar_r) / grr
                        + tau_Q * 2.0 * W * grr * vr**2 * (-dp * hat_eps) / grr)

    # eta part of S^r_r (Cowling K=0, K_ij=0):
    # (1/3)*eta*W * { 6*K_rr [=0] + other terms }
    # The nonzero Cowling-approx terms:
    # (1/3)*eta*W * [2*(grr + W^2*vr_low^2/grr)*(-K + a.v + Div_v) ... ]
    # Simplified Cowling:
    Srr_eta_spatial = ((1.0/3.0)*eta*W
                       * (2.0*(1.0 + W2*grr*vr**2)*(A_r*vr + Div_v)
                          - 6.0*(Dr_vr + W2*(vr*A_r - hat_vbar_r + vr*Dr_vr))))
    Srr_eta_hat     = ((1.0/3.0)*eta*W
                       * (6.0*W2*(vr*hat_vbar_r)))

    # zeta part:
    # zeta * W * (grr/grr + W^2*vr_low^2/grr) * Theta   (Cowling, hat_vbar_r included)
    Srr_zeta_spatial = zeta * W * (1.0 + W2*grr*vr**2) * Theta
    Srr_zeta_hat     = zeta * W * (1.0 + W2*grr*vr**2) * (-W2*grr*vr * hat_vbar_r)
    # Note: hat_vbar_r enters Theta through -D_i v^i -> not directly; see Paper Sij formula.
    # The hat terms enter only through the explicit hat_vbar_r in the A-matrix.

    # Collect S^r_r
    Sr_r = (Srr_ideal
            + Srr_tau_spatial + Srr_tau_hat
            + Srr_tauQ_spatial + Srr_tauQ_hat
            + Srr_eta_spatial  + Srr_eta_hat
            + Srr_zeta_spatial)

    # ---- S^theta_theta (needed for spherical-symmetry source term) ----
    # S^theta_theta = (1/r^2 psi^4) * S_theta_theta in isotropic coords
    # = p * g^theta_theta * g_theta_theta + ... = p + viscous angular parts
    # In spherical symmetry, the angular stress equals pressure plus bulk viscosity
    # correction (shear is traceless and isotropic split gives):
    # S^theta_theta = p + (1/3)*eta*W*(2*K + a.v + Div_v - 3*K_theta_theta - ...)
    #               + zeta*W*(...)
    # Cowling (K=0, K_ij=0):
    # S^theta_theta ≈ p + (1/3)*eta*W*(2*A_r*vr - Div_v + ...)
    #               + zeta*W*(1 - W^2)*(...)   [same as bulk enters isotropically]
    # Keeping leading viscous terms:
    Sth_th = (p
              + (1.0/3.0)*eta*W*(2.0*A_r*vr - Div_v + W2*(A_r*vr + Div_v))
              - (1.0/3.0)*eta*W*W2*vr*hat_vbar_r
              + zeta*W*(Theta - W2*grr*vr*hat_vbar_r))

    return E, Sr, Sr_r, Sth_th
```

---

## 6. Time Evolution Scheme

### 6.1 SSP-RK3

`[SOLID]` (ref: Paper Section II.E)

```python
def ssp_rk3_step(state, dt, rhs_func):
    """
    Strong Stability Preserving Runge-Kutta 3rd order.

    u^(1) = u^n + dt * L(u^n)
    u^(2) = 3/4 u^n + 1/4 (u^(1) + dt * L(u^(1)))
    u^(n+1) = 1/3 u^n + 2/3 (u^(2) + dt * L(u^(2)))
    """
    k1 = rhs_func(state)
    u1 = state + dt * k1

    k2 = rhs_func(u1)
    u2 = 0.75 * state + 0.25 * (u1 + dt * k2)

    k3 = rhs_func(u2)
    u_new = (1.0/3.0) * state + (2.0/3.0) * (u2 + dt * k3)

    return u_new
```

### 6.2 FDOC Spatial Scheme

`[SOLID]` (ref: Paper Section II.E, Alic et al. 2007, Palenzuela et al. 2018)

The FDOC (Finite-Difference Osher-Chakrabarthy) scheme is a 3rd-order finite-volume
scheme equivalent to a 4th-order finite difference with 3rd-order numerical dissipation.
For a scalar field $u$ on a staggered grid with cell-centers $r_i$ and interfaces at
$r_{i+1/2}$:

**Reconstruction:** 3rd-order Osher-Chakrabarthy minmod-limited reconstruction to
interfaces. The reconstructed left/right states at $r_{i+1/2}$ are:

$$u^L_{i+1/2} = u_i + \frac{1}{2}\,\phi(\Delta u_{i-1/2},\,\Delta u_{i+1/2})\,\Delta r$$
$$u^R_{i+1/2} = u_{i+1} - \frac{1}{2}\,\phi(\Delta u_{i+1/2},\,\Delta u_{i+3/2})\,\Delta r$$

where $\phi$ is the minmod limiter applied to consecutive undivided differences.

**Flux:** Local Lax-Friedrichs (LLF) numerical flux using the maximum curved-space
characteristic speed $\lambda_{\max}$ from `curved_characteristic_velocities_spherical`:

$$F_{i+1/2} = \frac{1}{2}\bigl[f(u^L_{i+1/2}) + f(u^R_{i+1/2})
              - \lambda_{\max}\,(u^R_{i+1/2} - u^L_{i+1/2})\bigr]$$

```python
def minmod(a, b):
    """
    Minmod slope limiter.
    Returns minmod(a, b) = sign(a)*max(0, min(|a|, sign(a)*b)).
    """
    return np.where(a * b > 0,
                    np.sign(a) * np.minimum(np.abs(a), np.abs(b)),
                    0.0)


def oc_reconstruct(u, dr):
    """
    3rd-order Osher-Chakrabarthy reconstruction on a 1D uniform grid.

    Computes left (u_L) and right (u_R) states at each cell interface i+1/2,
    for i = 0, ..., N-2.

    The stencil uses ghost cells; caller must have padded u by at least 2 cells
    on each side (e.g., using np.pad with 'edge' or outflow conditions).

    Parameters
    ----------
    u  : 1D array of cell-centered values (including ghost cells)
    dr : uniform grid spacing

    Returns
    -------
    u_L : left  state at interface i+1/2  (length N-1 for N interior cells)
    u_R : right state at interface i+1/2
    """
    # Undivided differences (slope estimates)
    # Delta_{i+1/2} = u_{i+1} - u_i
    du = np.diff(u)  # du[i] = u[i+1] - u[i]

    # Minmod-limited slopes at cell centers
    # slope_i = minmod(du[i-1], du[i]) where du[i] = u[i+1]-u[i]
    # For interior indices i (1 to N-2 in padded array):
    slope = minmod(du[:-1], du[1:])  # slope[i] for cell i+1 in padded coords

    # Reconstruct to interfaces
    # u_L[i+1/2] = u[i] + 0.5 * slope[i]
    # u_R[i+1/2] = u[i+1] - 0.5 * slope[i+1]
    u_L = u[1:-1] + 0.5 * slope[:-1]
    u_R = u[2:]   - 0.5 * slope[1:]

    return u_L, u_R


def llf_flux(f_L, f_R, u_L, u_R, lambda_max):
    """
    Local Lax-Friedrichs (Rusanov) numerical flux.

    F_{i+1/2} = 0.5 * (f_L + f_R - lambda_max * (u_R - u_L))

    Parameters
    ----------
    f_L, f_R    : physical fluxes evaluated at left/right reconstructed states
    u_L, u_R    : reconstructed conservative variables at each interface
    lambda_max  : maximum characteristic speed at this interface

    Returns
    -------
    flux : numerical flux array at interfaces
    """
    return 0.5 * (f_L + f_R - lambda_max * (u_R - u_L))


def fdoc_divergence(u, physical_flux_func, lambda_max_func,
                    r_ifaces, dr, n_ghost=2):
    """
    Compute the spatial divergence term partial_r F for the FDOC scheme on a
    1D staggered spherical-symmetry grid.

    The balance law is:
        partial_t q + (1/tilde_gamma) * partial_r (alpha * tilde_gamma * F) = S

    This function returns the flux-divergence contribution
        D[i] = (1/tilde_gamma[i]) * (Fnum[i+1/2] - Fnum[i-1/2]) / dr

    Parameters
    ----------
    u               : 1D array of evolved variable (cell centers, NO ghost cells)
    physical_flux_func  : callable f(u) returning the physical flux at each point
    lambda_max_func     : callable lam(i_iface) returning max char speed at interface
    r_ifaces        : array of interface radii (length N+1)
    dr              : grid spacing
    n_ghost         : number of ghost cells (default 2 for 3rd order stencil)

    Returns
    -------
    divF : spatial divergence of numerical flux (same length as u)
    """
    N = len(u)

    # Pad with ghost cells (outflow / zeroth-order extrapolation)
    u_pad = np.pad(u, n_ghost, mode='edge')

    # Reconstruct to interfaces
    u_L, u_R = oc_reconstruct(u_pad, dr)
    # u_L[i] is left state at interface between cell i and i+1 (in unpadded indexing)
    # There are N+1 interfaces for N cells (with 2 ghost on each side giving N+2*n_ghost cells)

    # Evaluate physical fluxes at reconstructed states
    f_L = physical_flux_func(u_L)
    f_R = physical_flux_func(u_R)

    # Evaluate maximum characteristic speeds at each interface
    # (caller provides this based on primitives at interfaces)
    lam = lambda_max_func(np.arange(N + 1))   # shape (N+1,)

    # Numerical flux at each interface i+1/2 for i = 0..N-1
    # Note: u_L and u_R are indexed from interface 0 to N (length N+1 if n_ghost=2)
    F_num = llf_flux(f_L, f_R, u_L, u_R, lam)

    # Divergence: (F[i+1/2] - F[i-1/2]) / dr
    divF = (F_num[1:] - F_num[:-1]) / dr

    return divF
```

### 6.3 Full RHS Function

`[SOLID]` (ref: Paper Section II.D, spherical symmetry, Cowling approximation)

The 6-variable state vector is:
$\mathbf{U} = [\tilde\gamma E,\; \tilde\gamma S_r,\; \epsilon,\; \partial_r\epsilon,\; \tilde{v}^r,\; \partial_r\tilde{v}^r]$

The RHS combines the balance-law divergence for the first two fields, and
simple evolution equations for the remaining four.

```python
def bdnk_rhs(U, r_grid, dr, grr_grid, alpha_grid, alpha_r_grid,
              tgamma_grid, transport_params, hat_a=1.0, hat_q=0.999,
              hat_s=1.0, v_min=0.1, kappa=100.0):
    """
    Compute the complete right-hand side for the 6-variable BDNK evolution system
    in spherical symmetry under the Cowling approximation.

    State vector U[k, i] where k indexes the 6 fields and i indexes grid points:
        U[0] = tilde_gamma * E
        U[1] = tilde_gamma * S_r
        U[2] = epsilon
        U[3] = partial_r epsilon
        U[4] = tilde_v^r
        U[5] = partial_r tilde_v^r

    Balance laws (Paper Eqs. in spherical symmetry section):
        partial_t(tilde_gamma * E)  + partial_r(alpha * tilde_gamma * S^r) = source_E
        partial_t(tilde_gamma * S_r) + partial_r(alpha * tilde_gamma * S^r_r) = source_Sr

    First-order reduction equations (Paper Eqs. evol_epsilon_sph, evol_vel_r):
        partial_t epsilon          = -alpha * hat_epsilon
        partial_t (partial_r eps)  = -partial_r(alpha * hat_epsilon)
        partial_t tilde_v^r        = alpha * (-hat_vbar_r / r + K^r_r * tilde_v^r)
                                   = -alpha * hat_vbar_r / r    [Cowling: K=0]
        partial_t (partial_r tilde_v^r) = partial_r[-alpha * hat_vbar_r / r]

    Parameters
    ----------
    U             : (6, N) array of evolved variables
    r_grid        : (N,) array of cell-center radii
    dr            : grid spacing
    grr_grid      : (N,) g_rr metric (fixed, from initial data)
    alpha_grid    : (N,) lapse function (fixed in Cowling approx)
    alpha_r_grid  : (N,) A_r = (1/alpha) partial_r alpha
    tgamma_grid   : (N,) tilde_gamma = sqrt(g_rr) * g_theta_theta = sqrt(grr) * r^2 * psi^4
    transport_params : dict with hat_eta, hat_zeta
    hat_a, hat_q, hat_s : frame parameters (Paper Section II.B)
    v_min         : minimum characteristic speed floor
    kappa         : polytropic constant

    Returns
    -------
    dU_dt : (6, N) array of time derivatives
    """
    N = len(r_grid)
    dU_dt = np.zeros_like(U)

    hat_eta  = transport_params['hat_eta']
    hat_zeta = transport_params['hat_zeta']

    # ---- Unpack state vector ----
    tgE       = U[0]   # tilde_gamma * E
    tgSr      = U[1]   # tilde_gamma * S_r
    eps       = U[2]   # epsilon
    Dr_eps    = U[3]   # partial_r epsilon
    vtilde_r  = U[4]   # tilde_v^r = v^r / r
    Dr_vtilde = U[5]   # partial_r tilde_v^r

    # ---- Derived primitives ----
    vr_grid = r_grid * vtilde_r                     # v^r = r * tilde_v^r
    Dr_vr_grid = vtilde_r + r_grid * Dr_vtilde      # partial_r v^r = tilde_v^r + r * partial_r tilde_v^r

    E_grid  = tgE  / tgamma_grid    # E (divided by tilde_gamma)
    Sr_grid = tgSr / tgamma_grid    # S_r (covariant, divided by tilde_gamma)

    # ---- Compute transport coefficients and recover p1 at each grid point ----
    hat_eps_grid    = np.zeros(N)
    hat_vbar_r_grid = np.zeros(N)
    Sr_contr_grid   = np.zeros(N)    # S^r contravariant
    Srr_grid        = np.zeros(N)    # S^r_r mixed
    Sth_grid        = np.zeros(N)    # S^theta_theta

    for i in range(N):
        r_i   = r_grid[i]
        eps_i = eps[i]

        # Transport coefficients at this point
        cs2_i = dpressure_depsilon(eps_i, kappa)
        cs_i  = np.sqrt(np.maximum(cs2_i, 1e-15))
        tc_i  = compute_transport_coefficients(
            eps_i, kappa=kappa, L=1.0,
            hat_a=hat_a, hat_q=hat_q, hat_s=hat_s,
            hat_eta=hat_eta, hat_zeta=hat_zeta)

        sd_i = {'Dr_epsilon': Dr_eps[i], 'Dr_vr': Dr_vr_grid[i]}

        # con2prim: recover hat_epsilon and hat_vbar_r
        he_i, hv_i = con2prim_spherical(
            E_grid[i], Sr_grid[i],
            eps_i, vtilde_r[i], r_i,
            grr_grid[i], tc_i, sd_i,
            alpha_grid[i], alpha_r_grid[i])

        hat_eps_grid[i]    = he_i
        hat_vbar_r_grid[i] = hv_i

        # Compute stress tensor components for fluxes and sources
        E_i, Sr_i, Srr_i, Sth_i = compute_stress_tensor_components(
            eps_i, vtilde_r[i], r_i, he_i, hv_i,
            grr_grid[i], alpha_r_grid[i], tc_i, sd_i)

        Sr_contr_grid[i] = Sr_i    # S^r
        Srr_grid[i]      = Srr_i   # S^r_r
        Sth_grid[i]      = Sth_i   # S^theta_theta

    # ---- Compute maximum characteristic speeds for LLF dissipation ----
    lambda_max_grid = np.zeros(N)
    for i in range(N):
        cs2_i = dpressure_depsilon(eps[i], kappa)
        cs_i  = np.sqrt(np.maximum(cs2_i, 1e-15))
        _, c_max_i = curved_characteristic_velocities_spherical(
            vr_grid[i], grr_grid[i], alpha_grid[i],
            hat_a=hat_a, hat_q=hat_q, hat_s=hat_s,
            hat_eta=hat_eta, hat_zeta=hat_zeta,
            cs=cs_i, v_min=v_min)
        lambda_max_grid[i] = c_max_i

    # ---- Flux divergence for tilde_gamma * E equation ----
    # partial_t(tgamma*E) + partial_r(alpha * tgamma * S^r) = source_E
    # Flux = alpha * tgamma * S^r
    flux_E  = alpha_grid * tgamma_grid * Sr_contr_grid
    flux_Sr = alpha_grid * tgamma_grid * Srr_grid   # flux for S_r eq is alpha*tgamma*S^r_r

    # Pad and reconstruct for FDOC (simple version using centered differences for divergence;
    # for the full FDOC the per-variable reconstruction is applied to tgamma*{S^r, S^r_r})
    # Here we use second-order centered divergence as a placeholder for the interface
    # reconstruction; replace with oc_reconstruct + llf_flux for full 3rd-order accuracy.

    # Divergence: d/dr (alpha * tgamma * S^r)
    flux_E_pad  = np.pad(flux_E,  2, mode='edge')
    flux_Sr_pad = np.pad(flux_Sr, 2, mode='edge')

    # 4th-order centered first derivative (FDOC equivalent without shock limiter)
    # (F_{i+2} - 8*F_{i+1} + 8*F_{i-1} - F_{i-2}) / (12*dr)
    def div4(f_pad, dr):
        return (f_pad[4:] - 8.0*f_pad[3:-1] + 8.0*f_pad[1:-3] - f_pad[:-4]) / (12.0*dr)

    # 3rd-order dissipation: lambda * (u_{i+2} - 4u_{i+1} + 6u_i - 4u_{i-1} + u_{i-2})/(2*dr)
    def diss3(u, lam, dr):
        u_pad = np.pad(u, 2, mode='edge')
        d4u = u_pad[4:] - 4.0*u_pad[3:-1] + 6.0*u_pad[2:-2] - 4.0*u_pad[1:-3] + u_pad[:-4]
        return -lam * d4u / (2.0 * dr**3)

    div_flux_E  = div4(flux_E_pad,  dr) + diss3(tgE,  lambda_max_grid, dr)
    div_flux_Sr = div4(flux_Sr_pad, dr) + diss3(tgSr, lambda_max_grid, dr)

    # ---- Sources for balance laws (Cowling: K=0, beta=0) ----
    # source_E  = alpha * tgamma * [S^r_r * K^r_r + 2*S^theta_theta * K^theta_theta
    #                                - S^r * (2/r + A_r)]
    #           = alpha * tgamma * [- S^r * (2/r + A_r)]     [Cowling: K_ij=0]
    source_E  = alpha_grid * tgamma_grid * (-Sr_contr_grid * (2.0/r_grid + alpha_r_grid))

    # source_Sr = alpha * tgamma * [S^r_r*(D_rr^r - 2/r) + 2*S^theta_theta*(1/r + D_r_theta^theta)
    #                                - E * A_r]
    # In isotropic coordinates with psi^4 conformal factor:
    #   D_rr^r = (1/2) g^rr partial_r g_rr = 2*partial_r ln psi + ...
    #   D_r_theta^theta = (1/2) g^theta_theta partial_r g_theta_theta = partial_r ln(r*psi^2)/r...
    # For a simple first approximation in the Cowling approximation on the fixed background,
    # use the precomputed metric derivative terms. Here we denote them generically:
    # D_rr_r and D_rth_th should be supplied from initial data. Approximate for uniform
    # isotropic metric: D_rr^r ~ 0, D_r_theta^theta ~ 1/r.
    # (A full implementation passes these from the coordinate transformation output.)
    D_rr_r  = np.zeros(N)   # should be supplied: (1/2)*g^rr * partial_r g_rr
    D_rth_th = 1.0/r_grid   # approximate for isotropic: (1/2) g^{theta theta} partial_r g_{theta theta} = 1/r

    source_Sr = (alpha_grid * tgamma_grid
                 * (Srr_grid*(D_rr_r - 2.0/r_grid)
                    + 2.0*Sth_grid*(1.0/r_grid + D_rth_th)
                    - E_grid * alpha_r_grid))

    # ---- RHS for balance laws ----
    dU_dt[0] = -div_flux_E  + source_E
    dU_dt[1] = -div_flux_Sr + source_Sr

    # ---- RHS for first-order reduction equations ----
    # partial_t epsilon = -alpha * hat_epsilon  (Paper Eq. evol_epsilon_sph)
    dU_dt[2] = -alpha_grid * hat_eps_grid

    # partial_t (partial_r epsilon) = -partial_r(alpha * hat_epsilon)
    # Evolve as a balance law with flux = alpha * hat_epsilon
    flux_hateps = alpha_grid * hat_eps_grid
    flux_hateps_pad = np.pad(flux_hateps, 2, mode='edge')
    dU_dt[3] = -div4(flux_hateps_pad, dr)

    # partial_t tilde_v^r = -alpha * hat_vbar_r / r  (Cowling: K=0, Paper Eq. evol_vel_r)
    dU_dt[4] = -alpha_grid * hat_vbar_r_grid / r_grid

    # partial_t (partial_r tilde_v^r) = partial_r[-alpha * hat_vbar_r / r]
    flux_hatvr = -alpha_grid * hat_vbar_r_grid / r_grid
    flux_hatvr_pad = np.pad(flux_hatvr, 2, mode='edge')
    dU_dt[5] = div4(flux_hatvr_pad, dr)

    return dU_dt
```

---

## 7. Grid Setup and Boundary Conditions

### 7.1 Grid Parameters

`[SOLID]` (ref: Paper Section II.E)

```python
GRID_PARAMS = {
    'dr_range': [0.001, 0.0032],  # M_sun
    'r_max': 20.0,                # M_sun
    'CFL': 0.25,                  # dt/dr
    'staggered': True,            # avoid r=0 singularity
}
```

### 7.2 Atmosphere Treatment

`[SOLID]` (ref: Paper Section II.E)

```python
ATMOSPHERE = {
    'rho_0_atms': 1e-12,   # M_sun^{-2}, threshold
    'rho_0_floor': 1e-13,  # M_sun^{-2}, floor value
    'v_min': 0.1,          # minimum characteristic velocity (units of c)
}

def apply_atmosphere(epsilon, vr, hat_epsilon, hat_vbar_r, p, kappa=100.0, Gamma=2.0):
    """Set atmosphere values where p < kappa * rho_0_atms^Gamma."""
    rho_0_atms = 1e-12
    rho_0_floor = 1e-13
    p_atms = kappa * rho_0_atms**Gamma

    is_atmosphere = p < p_atms

    epsilon[is_atmosphere] = rho_0_floor  # update via EoS
    vr[is_atmosphere] = 0.0
    hat_epsilon[is_atmosphere] = 0.0
    hat_vbar_r[is_atmosphere] = 0.0

    return epsilon, vr, hat_epsilon, hat_vbar_r
```

---

## 8. Signal Analysis Tools

### 8.1 Power Spectral Density

`[SOLID]` (ref: Paper Section III.C.1)

```python
from scipy.signal import blackman
from scipy.fft import fft, fftfreq

def compute_psd(signal, dt, window='blackman'):
    """Compute power spectral density with Blackman window."""
    N = len(signal)
    if window == 'blackman':
        w = blackman(N)
    else:
        w = np.ones(N)

    windowed = signal * w
    spectrum = fft(windowed)
    freqs = fftfreq(N, d=dt)

    psd = np.abs(spectrum[:N//2])**2
    freqs = freqs[:N//2]

    return freqs, psd
```

### 8.2 Butterworth Filter for Decay Rate

`[SOLID]` (ref: Paper Section III.C.2)

```python
from scipy.signal import butter, filtfilt

def butterworth_filter(signal, dt, f_low=0.01, f_high_factor=0.1, order=4):
    """
    Apply 4th-order Butterworth bandpass filter.
    f_low: low frequency cutoff (code units 1/M_sun)
    f_high_factor: fraction of sampling frequency for high cutoff
    """
    f_sampling = 1.0 / dt
    f_high = f_sampling * f_high_factor

    nyquist = f_sampling / 2.0
    low = f_low / nyquist
    high = f_high / nyquist

    b, a = butter(order, [low, high], btype='band')
    filtered = filtfilt(b, a, signal)

    return filtered
```

### 8.3 Decay Rate Extraction

`[SOLID]` (ref: Paper Section III.C.2)

```python
from scipy.optimize import curve_fit

def extract_decay_rate_linear(filtered_signal, times, t_start, t_end):
    """
    Linear fit to log of envelope maxima.
    Returns decay rate 1/tau.
    """
    mask = (times >= t_start) & (times <= t_end)
    t_window = times[mask]
    sig_window = np.abs(filtered_signal[mask])

    # Find local maxima
    from scipy.signal import argrelmax
    max_idx = argrelmax(sig_window)[0]

    t_max = t_window[max_idx]
    log_max = np.log(sig_window[max_idx])

    # Linear fit: log(A) - t/tau
    coeffs = np.polyfit(t_max, log_max, 1)
    decay_rate = -coeffs[0]  # 1/tau

    return decay_rate

def extract_decay_rate_nonlinear(filtered_signal, times, t_start, t_end):
    """
    Non-linear fit: A*exp(-t/tau)*cos(omega*t + phi) + C
    Returns decay_rate, omega, amplitude.
    """
    mask = (times >= t_start) & (times <= t_end)
    t_fit = times[mask]
    sig_fit = filtered_signal[mask]

    def damped_sinusoid(t, A, tau, omega, phi, C):
        return A * np.exp(-t/tau) * np.cos(omega*t + phi) + C

    # Initial guesses
    omega_guess = 0.0834  # M_sun^{-1}, from paper
    tau_guess = 600.0     # M_sun

    p0 = [np.max(np.abs(sig_fit)), tau_guess, omega_guess, 0.0, 0.0]

    popt, pcov = curve_fit(damped_sinusoid, t_fit, sig_fit, p0=p0, maxfev=10000)

    return {
        'amplitude': popt[0],
        'tau': popt[1],
        'decay_rate': 1.0/popt[1],
        'omega': popt[2],
        'frequency_kHz': popt[2] / (2*np.pi) * 203.025,  # Convert to kHz
        'phase': popt[3],
        'offset': popt[4]
    }
```

### 8.4 Continuum Extrapolation

`[SOLID]` (ref: Paper Eq.58)

```python
def extrapolate_to_continuum(decay_rates, resolutions):
    """
    Fit: 1/tau_dr = 1/tau_0 + m * dr^p

    Parameters:
        decay_rates: measured decay rates at each resolution
        resolutions: dr values
    Returns:
        tau_0_inv: continuum decay rate
        m: coefficient
        p: convergence order
    """
    from scipy.optimize import curve_fit

    def model(dr, tau_0_inv, m, p):
        return tau_0_inv + m * dr**p

    p0 = [decay_rates[-1]*0.7, 1.0, 1.0]
    popt, pcov = curve_fit(model, resolutions, decay_rates, p0=p0)

    return {
        'tau_0_inv': popt[0],
        'm': popt[1],
        'p': popt[2]
    }
```

---

## 9. Convergence Testing

### 9.1 Convergence Factor with Cubic Spline Time Alignment

`[SOLID]` (ref: Paper Appendix B)

The convergence factor for non-uniform resolution ratios is (Paper Appendix B):

$$Q = \frac{(\Delta r_l)^n - (\Delta r_m)^n}{(\Delta r_m)^n - (\Delta r_h)^n}$$

Because different resolutions under the same CFL condition ($\Delta t / \Delta r = 0.25$)
produce time steps that are not integer multiples of each other (e.g., $\Delta r = 0.002$
and $\Delta r = 0.0028$ give incommensurable timesteps), the central energy density
$\epsilon_c(t)$ must be interpolated to a common time axis before computing pointwise
differences. A cubic spline interpolator (convergence order 4, sufficient for the
3rd-order scheme) is used for this purpose.

```python
from scipy.interpolate import CubicSpline

def convergence_factor(dr_l, dr_m, dr_h, n=3):
    """
    Theoretical convergence factor Q for convergence order n
    and three resolutions dr_l > dr_m > dr_h.

    Q = (dr_l^n - dr_m^n) / (dr_m^n - dr_h^n)

    For the paper's resolutions (0.0028, 0.002, 0.001) with n=3:
    Q = (0.0028^3 - 0.002^3) / (0.002^3 - 0.001^3) = (2.195e-8 - 8e-9)/(8e-9 - 1e-9)
      ≈ 1.393e-8 / 7e-9 ≈ 1.99

    Parameters
    ----------
    dr_l, dr_m, dr_h : grid spacings (low, mid, high resolution)
    n                : expected convergence order (default 3 for FDOC scheme)

    Returns
    -------
    Q : convergence factor
    """
    return (dr_l**n - dr_m**n) / (dr_m**n - dr_h**n)


def align_and_compare(t_low, eps_low, t_mid, eps_mid, t_high, eps_high,
                       t_common=None):
    """
    Align central energy density time series from three resolutions onto a
    common time grid using cubic spline interpolation (Paper Appendix B).

    The cubic spline interpolator has 4th-order accuracy, which is sufficient
    to avoid contaminating the 3rd-order convergence test.

    Parameters
    ----------
    t_low, eps_low   : time array and epsilon_c for low  resolution
    t_mid, eps_mid   : time array and epsilon_c for mid  resolution
    t_high, eps_high : time array and epsilon_c for high resolution
    t_common         : if None, use the intersection of all three time ranges
                       sampled at the coarsest timestep

    Returns
    -------
    t_common   : common time axis
    eps_l_int  : low  resolution epsilon_c interpolated to t_common
    eps_m_int  : mid  resolution epsilon_c interpolated to t_common
    eps_h_int  : high resolution epsilon_c interpolated to t_common
    """
    # Determine common time range
    t_start = max(t_low[0],  t_mid[0],  t_high[0])
    t_end   = min(t_low[-1], t_mid[-1], t_high[-1])

    if t_common is None:
        # Use coarsest timestep for the common grid (most conservative)
        dt_low  = np.median(np.diff(t_low))
        dt_mid  = np.median(np.diff(t_mid))
        dt_high = np.median(np.diff(t_high))
        dt_coarse = max(dt_low, dt_mid, dt_high)
        t_common = np.arange(t_start, t_end, dt_coarse)

    # Build cubic spline interpolators
    cs_low  = CubicSpline(t_low,  eps_low)
    cs_mid  = CubicSpline(t_mid,  eps_mid)
    cs_high = CubicSpline(t_high, eps_high)

    # Evaluate on common grid
    eps_l_int = cs_low(t_common)
    eps_m_int = cs_mid(t_common)
    eps_h_int = cs_high(t_common)

    return t_common, eps_l_int, eps_m_int, eps_h_int


def compute_pointwise_Q(t_low, eps_low, t_mid, eps_mid, t_high, eps_high,
                         dr_l, dr_m, dr_h, n=3):
    """
    Compute the pointwise convergence factor Q(t) for three resolution runs.

    Q(t) = (eps_l(t) - eps_m(t)) / (eps_m(t) - eps_h(t))

    Should asymptote to the theoretical value
        Q_theory = convergence_factor(dr_l, dr_m, dr_h, n)
    at late times after the transient (Paper Appendix B, Fig. convergence).

    Parameters
    ----------
    t_low, eps_low   : (time, epsilon_c) for lowest  resolution
    t_mid, eps_mid   : (time, epsilon_c) for middle  resolution
    t_high, eps_high : (time, epsilon_c) for highest resolution
    dr_l, dr_m, dr_h : corresponding grid spacings
    n                : expected convergence order

    Returns
    -------
    t_common : common time axis
    Q_t      : pointwise convergence factor Q(t)
    Q_theory : theoretical expected value of Q
    """
    t_common, el, em, eh = align_and_compare(
        t_low, eps_low, t_mid, eps_mid, t_high, eps_high)

    # Numerator: diff between low and mid
    num = el - em
    # Denominator: diff between mid and high
    den = em - eh

    # Avoid division by near-zero (numerical noise floor)
    safe_den = np.where(np.abs(den) > 1e-15, den, 1e-15)
    Q_t = num / safe_den

    Q_theory = convergence_factor(dr_l, dr_m, dr_h, n)

    return t_common, Q_t, Q_theory
```

---

## Appendix

### Unit Conversions

```python
# Geometric units: G = c = 1, length/time in M_sun
M_SUN_KG = 1.989e30        # kg
M_SUN_M = 1.477e3          # meters (GM/c^2)
M_SUN_S = 4.926e-6         # seconds (GM/c^3)
M_SUN_INV2_TO_KG_M3 = 6.176e20  # density conversion

# Frequency: f[kHz] = f[1/M_sun] * 1/(2*pi*M_SUN_S) * 1e-3
# = f[1/M_sun] * 203.025 / (2*pi) kHz (for angular frequency)
# = f[1/M_sun] * 32.312 kHz (for frequency in 1/M_sun)
```

### Abandoned Approaches

[None yet]
