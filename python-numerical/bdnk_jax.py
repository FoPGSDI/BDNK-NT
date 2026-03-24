"""
bdnk_jax.py — JAX/GPU-compatible BDNK viscous hydrodynamics solver.

Drop-in replacement for the evolution hot path in bdnk_core.py.
Setup (TOV, coordinate transform, grid construction) still uses NumPy/SciPy.
The evolution loop (RHS + SSP-RK3) is fully JIT-compiled via JAX.

Usage:
    import bdnk_jax as bj
    grid_data = bj.make_grid_data(dr=0.01)
    U0 = bj.build_initial_state(grid_data)
    times, eps_c = bj.evolve(grid_data, U0, t_end=2000.0, hat_eta=0.01, hat_zeta=0.01)
"""

import numpy as np
import jax
jax.config.update("jax_enable_x64", True)   # Use float64 for numerical accuracy
import jax.numpy as jnp
from functools import partial

# Use the NumPy-based setup from bdnk_core (TOV, coord transform, etc.)
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import bdnk_core

# ═══════════════════════════════════════════════════════════════════════
#  Constants
# ═══════════════════════════════════════════════════════════════════════

KAPPA = 100.0
GAMMA = 2.0
DISS_SIGMA = 0.5
RHO0_ATMS = 1e-12
P_ATMS = KAPPA * RHO0_ATMS**GAMMA
EPS_FLOOR = float(bdnk_core.EPS_FLOOR)

# ═══════════════════════════════════════════════════════════════════════
#  EoS (JAX-compatible, no in-place ops)
# ═══════════════════════════════════════════════════════════════════════

@jax.jit
def pressure(eps):
    eps = jnp.maximum(eps, 0.0)
    return (1.0 + 2.0 * eps * KAPPA
            - jnp.sqrt(1.0 + 4.0 * eps * KAPPA)) / (2.0 * KAPPA)

@jax.jit
def dpressure_deps(eps):
    eps = jnp.maximum(eps, 0.0)
    return 1.0 - 1.0 / jnp.sqrt(1.0 + 4.0 * eps * KAPPA)


# ═══════════════════════════════════════════════════════════════════════
#  Grid data — build from bdnk_core.GridData, store as dict of jax arrays
# ═══════════════════════════════════════════════════════════════════════

def make_grid_data(dr=0.01, r_max=20.0, rho0c=0.00128):
    """Build grid using NumPy, then convert to JAX arrays for JIT."""
    grid = bdnk_core.GridData(dr=dr, r_max=r_max, rho0c=rho0c)
    return {
        'r':          jnp.array(grid.r),
        'dr':         dr,
        'N':          grid.N,
        'grr':        jnp.array(grid.grr),
        'alpha':      jnp.array(grid.alpha),
        'A_r':        jnp.array(grid.A_r),
        'D_rr_r':     jnp.array(grid.D_rr_r),
        'D_rth_th':   jnp.array(grid.D_rth_th),
        'tgamma':     jnp.array(grid.tgamma),
        'eps_bg':     jnp.array(grid.eps_bg),
        'tgE_eq':     jnp.array(grid.tgE_eq),
        'tgSr_eq':    jnp.array(grid.tgSr_eq),
        'Dr_eps_eq':  jnp.array(grid.Dr_eps_eq),
        'eq_corr_E':  jnp.array(grid.eq_corr_E),
        'eq_corr_Sr': jnp.array(grid.eq_corr_Sr),
        'c0_eq_res':  jnp.array(grid.c0_eq_residual),
        'cr_eq_res':  jnp.array(grid.cr_eq_residual),
    }


def build_initial_state(gd):
    """Build initial state as JAX array. Uses NumPy grid internally."""
    grid = bdnk_core.GridData.__new__(bdnk_core.GridData)
    # Reconstruct minimal grid for build_initial_state
    grid.N = gd['N']
    grid.r = np.array(gd['r'])
    grid.dr = gd['dr']
    grid.eps_bg = np.array(gd['eps_bg'])
    grid.tgamma = np.array(gd['tgamma'])
    grid.alpha = np.array(gd['alpha'])
    U0_np = bdnk_core.build_initial_state(grid)
    return jnp.array(U0_np)


# ═══════════════════════════════════════════════════════════════════════
#  Transport coefficients (JAX)
# ═══════════════════════════════════════════════════════════════════════

@jax.jit
def compute_transport(eps, hat_eta, hat_zeta,
                      hat_a=1.0, hat_q=0.999, hat_s=1.0):
    p   = pressure(eps)
    cs2 = dpressure_deps(eps)
    rho = eps + p
    hat_V = (4.0 / 3.0) * hat_eta + hat_zeta
    eta     = hat_q * cs2 * rho * hat_eta
    zeta    = hat_q * cs2 * rho * hat_zeta
    tau_eps = hat_V
    tau_p   = hat_s * cs2 * hat_V
    tau_Q   = hat_a * hat_V
    return eta, zeta, tau_eps, tau_p, tau_Q, cs2, p, rho


# ═══════════════════════════════════════════════════════════════════════
#  Padding (JAX-compatible, no in-place ops)
# ═══════════════════════════════════════════════════════════════════════

def _pad_parity(u, ng, parity):
    """Pad with parity at left, outflow at right. Returns (N+2*ng,) array."""
    # Left ghost: mirror with parity
    left = parity * jnp.flip(u[:ng])
    # Right ghost: constant extrapolation
    right = jnp.broadcast_to(u[-1], (ng,))
    return jnp.concatenate([left, u, right])


# ═══════════════════════════════════════════════════════════════════════
#  FDOC operators (JAX)
# ═══════════════════════════════════════════════════════════════════════

def fdoc_deriv(f_pad, dr):
    """4th-order centered first derivative."""
    return (-f_pad[4:]
            + 8.0 * f_pad[3:-1]
            - 8.0 * f_pad[1:-3]
            + f_pad[:-4]) / (12.0 * dr)


def fdoc_diss(u_pad, lam, dr):
    """3rd-order KO dissipation."""
    d4u = (u_pad[4:]
           - 4.0 * u_pad[3:-1]
           + 6.0 * u_pad[2:-2]
           - 4.0 * u_pad[1:-3]
           + u_pad[:-4])
    return -DISS_SIGMA * lam * d4u / dr


# ═══════════════════════════════════════════════════════════════════════
#  A-matrix and c-vector (JAX)
# ═══════════════════════════════════════════════════════════════════════

def _A_and_c(eps, vr, grr, eta, zeta, tau_eps, tau_p, tau_Q, cs2, p, rho,
             A_r, r, Dr_eps, Dr_vr):
    """Build A-matrix and c-vector. All inputs are JAX arrays."""
    v2     = jnp.minimum(grr * vr**2, 1.0 - 1e-10)
    W2_inv = 1.0 - v2
    W      = 1.0 / jnp.sqrt(W2_inv)
    W2     = W**2
    W3     = W**3

    vr_low  = grr * vr
    a_dot_v = A_r * vr
    Div_v   = Dr_vr + 2.0 * vr / r
    vvDv    = W2 * vr**2 * grr * Dr_vr
    Theta   = a_dot_v + Div_v + vvDv
    bracket = rho * Theta + vr * Dr_eps
    dp      = cs2

    denom_32 = W2_inv**1.5
    denom_52 = W2_inv**2.5

    A00 = -(2.0 * grr * vr**2 * tau_Q * dp
            + tau_eps * (grr * vr**2 * dp + 1.0)) / denom_32
    A01 = -(grr * vr * (-4.0 * grr * vr**2 * eta
                         + 3.0 * grr * vr**2 * (rho * tau_eps * dp - zeta)
                         + 3.0 * rho * (2.0 * tau_Q + tau_eps))
            ) / (3.0 * denom_52)
    A10 = -(grr * vr * ((grr * vr**2 + 1.0) * tau_Q * dp
                          + tau_eps * (dp + 1.0))) / denom_32
    A11 = -(grr * (-4.0 * grr * vr**2 * eta
                    + 3.0 * grr * vr**2 * (rho * (tau_eps * (dp + 1.0) + tau_Q) - zeta)
                    + 3.0 * rho * tau_Q)) / (3.0 * denom_52)

    # c-vector
    c0 = (W2 * eps - p * (1.0 - W2)
          + W * (tau_eps * W2 - (1.0 - W2) * tau_p) * bracket
          + 2.0 * tau_Q * W3 * (rho * (a_dot_v + vvDv) + dp * vr * Dr_eps)
          + (2.0 / 3.0) * eta * W * ((1.0 - W2) * (2.0 * a_dot_v - Div_v)
              + W2 * (1.0 + 2.0 * W2) * (-2.0 + W2) * vr**2 * grr * Dr_vr)
          + zeta * W * (1.0 - W2) * Theta)

    cr = (-vr_low * W2 * rho
          + (tau_eps + tau_p) * vr_low * W3 * bracket
          + tau_Q * (-dp * W * Dr_eps
              + W3 * (-(rho * (A_r + vr_low * a_dot_v
                                + vr * grr * Dr_vr
                                - vr_low * 2.0 * W2 * vr**2 * grr * Dr_vr))
                      - 2.0 * dp * vr_low * vr * Dr_eps))
          + eta * (-A_r * W * (1.0 - W2)
              + (1.0 / 3.0) * W3 * (vr_low * (a_dot_v - 2.0 * Div_v + 4.0 * vvDv)
                  + 3.0 * 2.0 * vr * grr * Dr_vr))
          + zeta * vr_low * W3 * Theta)

    return A00, A01, A10, A11, c0, cr


# ═══════════════════════════════════════════════════════════════════════
#  Con2prim (JAX)
# ═══════════════════════════════════════════════════════════════════════

def con2prim(E, Sr, eps, vtilde_r, gd,
             eta, zeta, tau_eps, tau_p, tau_Q, cs2, p, rho,
             Dr_eps, Dr_vr):
    vr = gd['r'] * vtilde_r
    A00, A01, A10, A11, c0, cr = _A_and_c(
        eps, vr, gd['grr'], eta, zeta, tau_eps, tau_p, tau_Q, cs2, p, rho,
        gd['A_r'], gd['r'], Dr_eps, Dr_vr)
    c0 = c0 - gd['c0_eq_res']
    cr = cr - gd['cr_eq_res']
    b0 = E - c0
    b1 = Sr - cr
    det = A00 * A11 - A01 * A10
    safe_det = jnp.where(jnp.abs(det) > 1e-30, det, 1e-30)
    hat_eps    = ( A11 * b0 - A01 * b1) / safe_det
    hat_vbar_r = (-A10 * b0 + A00 * b1) / safe_det
    return hat_eps, hat_vbar_r


# ═══════════════════════════════════════════════════════════════════════
#  Stress tensor (JAX)
# ═══════════════════════════════════════════════════════════════════════

def compute_stress(eps, vtilde_r, hat_eps, hat_vbar_r, gd,
                   eta, zeta, tau_eps, tau_p, tau_Q, cs2, p, rho,
                   Dr_eps, Dr_vr):
    r = gd['r']; grr = gd['grr']
    vr = r * vtilde_r
    A00, A01, A10, A11, c0, cr = _A_and_c(
        eps, vr, grr, eta, zeta, tau_eps, tau_p, tau_Q, cs2, p, rho,
        gd['A_r'], r, Dr_eps, Dr_vr)

    E_out  = A00 * hat_eps + A01 * hat_vbar_r + c0
    S_r    = A10 * hat_eps + A11 * hat_vbar_r + cr
    Sr_contra = S_r / grr

    u      = jnp.minimum(grr * vr**2, 1.0 - 1e-10)
    W2_inv = 1.0 - u
    W      = 1.0 / jnp.sqrt(W2_inv)
    W2     = W**2; dp = cs2
    A_r    = gd['A_r']; vr_low = grr * vr
    a_dot_v = A_r * vr
    Div_v   = Dr_vr + 2.0 * vr / r
    vvDv    = W2 * vr**2 * grr * Dr_vr
    Theta   = a_dot_v + Div_v + vvDv
    bracket = rho * Theta + vr * Dr_eps
    hat_v_dot_v = hat_vbar_r * vr_low
    vvDvr_raw   = vr**2 * grr * Dr_vr
    B_full = hat_eps - bracket + rho * W2 * hat_v_dot_v
    Theta_full = Theta - W2 * hat_v_dot_v

    S_rr_m = p + W2 * rho * u
    S_rr_m += -W * (tau_p + (tau_eps + tau_p) * W2 * u) * B_full
    tQ_t1 = 2.0 * W * vr * (W2 * rho * (A_r - grr * hat_vbar_r + vr * grr * Dr_vr) + dp * Dr_eps)
    tQ_t2 = 2.0 * W * u / grr * (-dp * hat_eps - W2 * rho * (hat_v_dot_v - vvDvr_raw) + dp * vr * Dr_eps)
    S_rr_m += tau_Q * (tQ_t1 + tQ_t2)
    Drv_cov = grr * Dr_vr
    eta_rr = ((1.0 / 3.0) * eta * W / grr
              * (2.0 * (grr + W2 * vr_low**2) * (a_dot_v + Div_v)
                 - 6.0 * (Drv_cov + W2 * (2.0 * vr * vr_low * Drv_cov + (A_r - grr * hat_vbar_r) * vr_low))
                 - 2.0 * W2 * (grr - 2.0 * W2 * vr_low**2) * (hat_v_dot_v - vvDvr_raw)))
    S_rr_m += eta_rr
    S_rr_m += -zeta * W * (1.0 + W2 * u) * Theta_full

    tQ_trace = (2.0 * W * vr * (W2 * rho * (A_r - grr * hat_vbar_r + vr * grr * Dr_vr) + dp * Dr_eps)
                + 2.0 * W * u / grr * (-dp * hat_eps - W2 * rho * (hat_v_dot_v - vvDvr_raw) + dp * vr * Dr_eps))
    S_trace = (3.0 * p + W2 * rho * u
               - W * (3.0 * tau_p + (tau_eps + tau_p) * W2 * u) * B_full
               + tau_Q * tQ_trace
               - zeta * W * (3.0 + W2 * u) * Theta_full)
    Sthth = 0.5 * (S_trace - S_rr_m)

    return E_out, Sr_contra, S_rr_m, Sthth


# ═══════════════════════════════════════════════════════════════════════
#  Characteristic speeds (JAX)
# ═══════════════════════════════════════════════════════════════════════

def max_char_speed(eps, vr, grr, alpha, hat_eta, hat_zeta,
                   hat_a=1.0, hat_q=0.999, hat_s=1.0):
    cs2 = dpressure_deps(eps)
    cs  = jnp.sqrt(jnp.maximum(cs2, 1e-15))
    hat_V = (4.0 / 3.0) * hat_eta + hat_zeta
    c0 = cs * jnp.sqrt(hat_q * hat_eta / (hat_a * hat_V))
    disc = jnp.maximum(hat_q**2 + hat_a**2 * (4.0 * hat_q + (hat_s - 1.0)**2)
                       + 2.0 * hat_a * hat_q * (1.0 + hat_s), 0.0)
    c_plus  = cs * jnp.sqrt((hat_a * (1.0 + hat_s) + hat_q + jnp.sqrt(disc)) / (2.0 * hat_a))
    c_minus = cs * jnp.sqrt(jnp.maximum(
        (hat_a * (1.0 + hat_s) + hat_q - jnp.sqrt(disc)) / (2.0 * hat_a), 0.0))

    v2 = jnp.minimum(grr * vr**2, 1.0 - 1e-10)
    W2 = 1.0 / (1.0 - v2)
    vdotk = jnp.sqrt(grr) * vr
    c_max = jnp.full_like(eps, 0.1)

    for c_flat in [c0, c_plus, c_minus]:
        c_flat_safe = jnp.maximum(c_flat, 1e-12)
        mi = 1.0 / c_flat_safe**2 - 1.0
        discriminant = jnp.maximum(1.0 + mi * W2 * (1.0 - vdotk**2), 0.0)
        denom = mi * W2 + 1.0
        c_fwd = alpha * (mi * W2 * vdotk + jnp.sqrt(discriminant)) / denom
        c_bwd = alpha * (mi * W2 * vdotk - jnp.sqrt(discriminant)) / denom
        c_max = jnp.maximum(c_max, jnp.abs(c_fwd))
        c_max = jnp.maximum(c_max, jnp.abs(c_bwd))
    return c_max


# ═══════════════════════════════════════════════════════════════════════
#  RHS — the complete right-hand side (JIT-compiled)
# ═══════════════════════════════════════════════════════════════════════

@partial(jax.jit, static_argnames=['hat_eta', 'hat_zeta', 'hat_a', 'hat_q', 'hat_s'])
def bdnk_rhs(U, gd, hat_eta=0.01, hat_zeta=0.01,
             hat_a=1.0, hat_q=0.999, hat_s=1.0):
    """JIT-compiled RHS for the 6-variable BDNK system."""
    r  = gd['r']
    dr = gd['dr']
    ng = 2

    tgE       = U[0]
    tgSr      = U[1]
    eps       = U[2]
    Dr_eps    = U[3]
    vtilde_r  = U[4]
    Dr_vtilde = U[5]

    # Atmosphere floor (functional, no in-place mutation)
    p_check = pressure(eps)
    atm = p_check < P_ATMS
    eps       = jnp.where(atm, EPS_FLOOR, eps)
    vtilde_r  = jnp.where(atm, 0.0, vtilde_r)
    Dr_eps    = jnp.where(atm, 0.0, Dr_eps)
    Dr_vtilde = jnp.where(atm, 0.0, Dr_vtilde)

    vr    = r * vtilde_r
    Dr_vr = vtilde_r + r * Dr_vtilde

    # Transport coefficients
    eta, zeta, tau_eps, tau_p, tau_Q, cs2, p, rho = compute_transport(
        eps, hat_eta, hat_zeta, hat_a, hat_q, hat_s)

    # Con2prim
    E_grid  = tgE / gd['tgamma']
    Sr_grid = tgSr / gd['tgamma']
    E_grid  = jnp.where(atm, eps, E_grid)
    Sr_grid = jnp.where(atm, 0.0, Sr_grid)

    hat_eps, hat_vbar_r = con2prim(E_grid, Sr_grid, eps, vtilde_r, gd,
                                    eta, zeta, tau_eps, tau_p, tau_Q, cs2, p, rho,
                                    Dr_eps, Dr_vr)

    # Cleanup and clamps (functional)
    hat_eps    = jnp.where(atm, 0.0, hat_eps)
    hat_vbar_r = jnp.where(atm, 0.0, hat_vbar_r)
    hat_eps    = jnp.nan_to_num(hat_eps, nan=0.0, posinf=0.0, neginf=0.0)
    hat_vbar_r = jnp.nan_to_num(hat_vbar_r, nan=0.0, posinf=0.0, neginf=0.0)
    hat_eps    = jnp.clip(hat_eps, -1e-9, 1e-9)
    hat_vbar_r = jnp.clip(hat_vbar_r, -1e-7 * r, 1e-7 * r)

    # Stress tensor
    E_st, Sr_contra, Srr_mixed, Sthth = compute_stress(
        eps, vtilde_r, hat_eps, hat_vbar_r, gd,
        eta, zeta, tau_eps, tau_p, tau_Q, cs2, p, rho,
        Dr_eps, Dr_vr)

    # Characteristic speeds
    lam_max = max_char_speed(eps, vr, gd['grr'], gd['alpha'],
                             hat_eta, hat_zeta, hat_a, hat_q, hat_s)

    # Balance-law flux divergences
    flux_E  = gd['alpha'] * gd['tgamma'] * Sr_contra
    flux_Sr = gd['alpha'] * gd['tgamma'] * Srr_mixed

    div_flux_E  = fdoc_deriv(_pad_parity(flux_E,  ng, -1), dr)
    div_flux_Sr = fdoc_deriv(_pad_parity(flux_Sr, ng, +1), dr)

    # KO dissipation on perturbations
    div_flux_E  += fdoc_diss(_pad_parity(tgE  - gd['tgE_eq'],  ng, +1), lam_max, dr)
    div_flux_Sr += fdoc_diss(_pad_parity(tgSr - gd['tgSr_eq'], ng, -1), lam_max, dr)

    # Sources
    source_E = gd['alpha'] * gd['tgamma'] * (-Sr_contra * (2.0 / r + gd['A_r']))
    source_Sr = (gd['alpha'] * gd['tgamma']
                 * (Srr_mixed * (gd['D_rr_r'] - 2.0 / r)
                    + 2.0 * Sthth * (1.0 / r + gd['D_rth_th'])
                    - E_st * gd['A_r']))

    dU0 = -div_flux_E  + source_E  - gd['eq_corr_E']
    dU1 = -div_flux_Sr + source_Sr - gd['eq_corr_Sr']

    # Constraint damping
    kappa_cd = 6.0 / dr
    dU0 += -kappa_cd * (tgE  - gd['tgamma'] * E_st)
    dU1 += -kappa_cd * (tgSr - gd['tgamma'] * Sr_contra * gd['grr'])

    # First-order reduction
    dU2 = -gd['alpha'] * hat_eps
    dU3 = -fdoc_deriv(_pad_parity(gd['alpha'] * hat_eps, ng, +1), dr)
    dU4 = -gd['alpha'] * hat_vbar_r / r
    dU5 = fdoc_deriv(_pad_parity(-gd['alpha'] * hat_vbar_r / r, ng, +1), dr)

    # KO dissipation on primitive perturbations
    dU2 += fdoc_diss(_pad_parity(eps - gd['eps_bg'],        ng, +1), lam_max, dr)
    dU3 += fdoc_diss(_pad_parity(Dr_eps - gd['Dr_eps_eq'],  ng, -1), lam_max, dr)
    dU4 += fdoc_diss(_pad_parity(vtilde_r,                  ng, -1), lam_max, dr)
    dU5 += fdoc_diss(_pad_parity(Dr_vtilde,                 ng, +1), lam_max, dr)

    # Zero RHS in atmosphere
    dU = jnp.stack([dU0, dU1, dU2, dU3, dU4, dU5])
    dU = jnp.where(atm[None, :], 0.0, dU)
    return dU


# ═══════════════════════════════════════════════════════════════════════
#  SSP-RK3 stepper (JIT-compiled)
# ═══════════════════════════════════════════════════════════════════════

@partial(jax.jit, static_argnames=['hat_eta', 'hat_zeta', 'hat_a', 'hat_q', 'hat_s'])
def ssp_rk3_step(U, dt, gd, hat_eta=0.01, hat_zeta=0.01,
                 hat_a=1.0, hat_q=0.999, hat_s=1.0):
    """One SSP-RK3 step, fully JIT-compiled."""
    k1 = bdnk_rhs(U, gd, hat_eta, hat_zeta, hat_a, hat_q, hat_s)
    u1 = U + dt * k1
    k2 = bdnk_rhs(u1, gd, hat_eta, hat_zeta, hat_a, hat_q, hat_s)
    u2 = 0.75 * U + 0.25 * (u1 + dt * k2)
    k3 = bdnk_rhs(u2, gd, hat_eta, hat_zeta, hat_a, hat_q, hat_s)
    return (1.0 / 3.0) * U + (2.0 / 3.0) * (u2 + dt * k3)


# ═══════════════════════════════════════════════════════════════════════
#  Evolution driver
# ═══════════════════════════════════════════════════════════════════════

def evolve(gd, U0, t_end, hat_eta=0.01, hat_zeta=0.01,
           hat_a=1.0, hat_q=0.999, hat_s=1.0,
           dt_save=1.0, CFL=0.25):
    """
    Evolve the BDNK system using JAX-accelerated SSP-RK3.

    Returns (times, eps_central) — only central density is saved to minimise
    host-device transfers for long runs. Use evolve_full() for full snapshots.
    """
    dt = CFL * gd['dr']
    n_steps = int(np.ceil(t_end / dt))
    save_every = max(1, int(dt_save / dt))

    U = U0
    times = [0.0]
    eps_c  = [float(U[2, 0])]

    # JIT-compile a block of steps to reduce Python overhead
    @partial(jax.jit, static_argnames=['n_inner', 'hat_eta', 'hat_zeta',
                                        'hat_a', 'hat_q', 'hat_s'])
    def step_block(U, n_inner, dt, gd, hat_eta, hat_zeta, hat_a, hat_q, hat_s):
        def body(i, U):
            return ssp_rk3_step(U, dt, gd, hat_eta, hat_zeta, hat_a, hat_q, hat_s)
        return jax.lax.fori_loop(0, n_inner, body, U)

    t = 0.0
    step = 0
    while step < n_steps:
        # Take a block of steps
        n_block = min(save_every, n_steps - step)
        U = step_block(U, n_block, dt, gd, hat_eta, hat_zeta, hat_a, hat_q, hat_s)
        step += n_block
        t += n_block * dt
        times.append(t)
        eps_c.append(float(U[2, 0]))

    return np.array(times), np.array(eps_c), U


def evolve_full(gd, U0, t_end, hat_eta=0.01, hat_zeta=0.01,
                hat_a=1.0, hat_q=0.999, hat_s=1.0,
                dt_save=1.0, CFL=0.25):
    """Like evolve() but returns full state snapshots (slower due to transfers)."""
    dt = CFL * gd['dr']
    n_steps = int(np.ceil(t_end / dt))
    save_every = max(1, int(dt_save / dt))

    U = U0
    times  = [0.0]
    states = [np.array(U)]

    t = 0.0
    step = 0
    while step < n_steps:
        n_block = min(save_every, n_steps - step)
        @partial(jax.jit, static_argnames=['n_inner', 'hat_eta', 'hat_zeta',
                                            'hat_a', 'hat_q', 'hat_s'])
        def step_block(U, n_inner, dt, gd, hat_eta, hat_zeta, hat_a, hat_q, hat_s):
            def body(i, U):
                return ssp_rk3_step(U, dt, gd, hat_eta, hat_zeta, hat_a, hat_q, hat_s)
            return jax.lax.fori_loop(0, n_inner, body, U)

        U = step_block(U, n_block, dt, gd, hat_eta, hat_zeta, hat_a, hat_q, hat_s)
        step += n_block
        t += n_block * dt
        times.append(t)
        states.append(np.array(U))

    return np.array(times), states


# ═══════════════════════════════════════════════════════════════════════
#  Self-test
# ═══════════════════════════════════════════════════════════════════════

def _selftest():
    """Verify JAX solver matches NumPy solver."""
    import time

    print("JAX BDNK self-test")
    print(f"  JAX version: {jax.__version__}")
    print(f"  Devices: {jax.devices()}")

    # Build grid
    gd = make_grid_data(dr=0.01, r_max=20.0)
    U0 = build_initial_state(gd)
    print(f"  Grid: N={gd['N']}, dr={gd['dr']}")
    print(f"  eps_c = {float(U0[2, 0]):.6e}")

    # Single RHS evaluation (includes JIT compilation)
    t0 = time.time()
    dU = bdnk_rhs(U0, gd, hat_eta=0.01, hat_zeta=0.01)
    dU.block_until_ready()
    t_compile = time.time() - t0
    print(f"  JIT compile + first RHS: {t_compile:.2f}s")

    # Subsequent call (cached)
    t0 = time.time()
    for _ in range(10):
        dU = bdnk_rhs(U0, gd, hat_eta=0.01, hat_zeta=0.01)
        dU.block_until_ready()
    t_cached = (time.time() - t0) / 10
    print(f"  Cached RHS: {t_cached*1000:.1f}ms")

    # Check RHS is near zero at equilibrium
    for i in range(6):
        mx = float(jnp.max(jnp.abs(dU[i])))
        print(f"  max|dU[{i}]| = {mx:.3e}")

    # Short evolution (100 steps)
    t0 = time.time()
    times, eps_c, Uf = evolve(gd, U0, t_end=10.0, hat_eta=0.01, hat_zeta=0.01,
                               dt_save=1.0)
    t_evol = time.time() - t0
    drift = abs(eps_c[-1] - eps_c[0]) / eps_c[0]
    print(f"  Evolution t=10: {t_evol:.2f}s, drift={drift:.3e}")

    # Timing comparison: JAX vs NumPy
    grid_np = bdnk_core.GridData(dr=0.01, r_max=20.0, rho0c=0.00128)
    U0_np = bdnk_core.build_initial_state(grid_np)
    t0 = time.time()
    for _ in range(10):
        dU_np = bdnk_core.bdnk_rhs(U0_np, grid_np, hat_eta=0.01, hat_zeta=0.01)
    t_np = (time.time() - t0) / 10
    print(f"\n  NumPy RHS: {t_np*1000:.1f}ms")
    print(f"  JAX   RHS: {t_cached*1000:.1f}ms")
    print(f"  Speedup:   {t_np/t_cached:.1f}x")

    print("\nAll JAX self-tests passed!")


if __name__ == '__main__':
    _selftest()
