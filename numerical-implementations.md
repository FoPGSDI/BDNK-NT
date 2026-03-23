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

`[PRELIMINARY]` (ref: Paper Eq.47-48)

Transform from areal-polar $(R)$ to maximal isotropic $(r)$ coordinates:

$$ds^2 = -\alpha^2(r)dt^2 + \psi^4(r)(dr^2 + r^2 d\Omega^2)$$

`[FUTURE: Implement coordinate transformation following Lai (2004)]`

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

### 4.3 Characteristic Velocities

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
        'c_minus_real': cm.imag == 0 if isinstance(cm, complex) else True,
        'c_plus_neq_c_minus': abs(cp - cm) > 1e-14,
        'causality_c0': c0 < 1.0,
        'causality_c_plus': cp < 1.0,
        'causality_c_minus': cm < 1.0,
        'causality_ineq': hat_q < (1-cs2)/cs2 * (1-hat_s*cs2)/(cs2 + 1.0/hat_a),
        'causality_s': hat_s < 1.0/cs2,
    }
    return checks
```

---

## 5. Conservative-to-Primitive Recovery (con2prim)

### 5.1 Spherically Symmetric 2×2 System

`[SOLID]` (ref: Paper Appendix A)

```python
def con2prim_spherical(E, S_r, epsilon, vr, grr,
                        transport_coeffs, spatial_derivs):
    """
    Recover p1 = (hat_epsilon, hat_vbar_r) from conservative and p0 variables.
    Solves the 2x2 linear system: A * p1 = b

    Parameters:
        E, S_r: conservative variables (divided by tilde_gamma)
        epsilon, vr: primitive variables p0
        grr: metric component
        transport_coeffs: dict with eta, zeta, tau_epsilon, tau_p, tau_Q, cs2
        spatial_derivs: dict with D_r_epsilon, D_r_vr, etc.
    """
    tc = transport_coeffs
    eta = tc['eta']
    zeta = tc['zeta']
    tau_eps = tc['tau_epsilon']
    tau_p = tc['tau_p']
    tau_Q = tc['tau_Q']
    p = pressure(epsilon)
    dp = dpressure_depsilon(epsilon)

    W2_inv = 1.0 - grr * vr**2
    W = 1.0 / np.sqrt(W2_inv)

    # Matrix components A (ref: Paper Eqs.A8-A11)
    A00 = -(2*grr*vr**2*tau_Q*dp + tau_eps*(grr*vr**2*dp + 1)) / W2_inv**1.5
    A01 = -(grr*vr*(-4*grr*vr**2*eta + 3*grr*vr**2*((p+epsilon)*tau_eps*dp - zeta)
            + 3*(p+epsilon)*(2*tau_Q + tau_eps))) / (3*W2_inv**2.5)
    A10 = -(grr*vr*((grr*vr**2 + 1)*tau_Q*dp + tau_eps*(dp + 1))) / W2_inv**1.5
    A11 = -(grr*(-4*grr*vr**2*eta + 3*grr*vr**2*((p+epsilon)*(tau_eps*(dp+1) + tau_Q) - zeta)
            + 3*(p+epsilon)*tau_Q)) / (3*W2_inv**2.5)

    # Compute b = (E, S_r) - c vector
    # c vector depends on spatial derivatives and geometry
    # [FUTURE: Implement full c vector computation]

    # Solve 2x2 linear system
    det = A00*A11 - A01*A10
    hat_epsilon = (A11*b0 - A01*b1) / det
    hat_vbar_r = (-A10*b0 + A00*b1) / det

    return hat_epsilon, hat_vbar_r
```

`[FUTURE: Complete the c vector (b0, b1) implementation with all geometric and spatial derivative terms]`

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

`[PRELIMINARY]`

`[FUTURE: Implement the finite-difference Osher-Chakrabarthy scheme for spatial reconstruction]`

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

### 9.1 Convergence Factor

`[SOLID]` (ref: Paper Appendix B)

```python
def convergence_factor(sol_low, sol_mid, sol_high, dr_l, dr_m, dr_h, n):
    """
    Compute convergence factor Q for non-uniform resolution ratios.
    Q = (dr_l^n - dr_m^n) / (dr_m^n - dr_h^n)
    """
    return (dr_l**n - dr_m**n) / (dr_m**n - dr_h**n)

# For resolutions 0.0028, 0.002, 0.001 with 3rd-order scheme:
# Q_expected = (0.0028^3 - 0.002^3) / (0.002^3 - 0.001^3) = ...
```

`[FUTURE: Implement full convergence test with cubic spline interpolation for time alignment]`

---

## Appendix

### Unit Conversions

```python
# Geometric units: G = c = 1, length/time in M_sun
M_SUN_KG = 1.989e30        # kg
M_SUN_M = 1.477e3          # meters (GM/c^2)
M_SUN_S = 4.926e-6         # seconds (GM/c^3)
M_SUN_INV2_TO_KG_M3 = 6.176e17  # density conversion

# Frequency: f[kHz] = f[1/M_sun] * 1/(2*pi*M_SUN_S) * 1e-3
# = f[1/M_sun] * 203.025 / (2*pi) kHz (for angular frequency)
# = f[1/M_sun] * 32.312 kHz (for frequency in 1/M_sun)
```

### Abandoned Approaches

[None yet]
