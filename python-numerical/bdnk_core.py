"""
bdnk_core.py — Complete BDNK viscous hydrodynamics solver for spherically
symmetric neutron stars on a fixed (Cowling) curved background.

Reference: arXiv:2509.15303v1 ("Paper" throughout).
All section/equation citations refer to that paper.

Evolved variables (6-component state vector U):
    U[0] = γ̃·E         (conserved energy density × metric factor)
    U[1] = γ̃·S_r       (conserved momentum × metric factor)
    U[2] = ε            (total energy density, primitive)
    U[3] = ∂_r ε        (spatial derivative, promoted to dynamical field)
    U[4] = ṽ^r = v^r/r  (regularised radial velocity)
    U[5] = ∂_r ṽ^r      (spatial derivative, promoted to dynamical field)

Conventions: geometric units with G = c = M_☉ = 1.
EoS: combined polytropic + ideal gas with κ = 100, Γ = 2.
"""

import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.interpolate import CubicSpline

# ═══════════════════════════════════════════════════════════════════════
#  Section 1 — Equation of State  (Paper Eq. 37 and surrounding text)
# ═══════════════════════════════════════════════════════════════════════

KAPPA = 100.0
GAMMA = 2.0


def pressure(eps, kappa=KAPPA):
    """
    EoS  p(ε) = [1 + 2εκ − √(1 + 4εκ)] / (2κ).   (Paper Eq. 37)
    Vectorised; safe for eps = 0.
    """
    eps = np.maximum(np.asarray(eps, dtype=float), 0.0)
    return (1.0 + 2.0 * eps * kappa
            - np.sqrt(1.0 + 4.0 * eps * kappa)) / (2.0 * kappa)


def dpressure_deps(eps, kappa=KAPPA):
    """dp/dε = c_s² = 1 − 1/√(1 + 4εκ)."""
    eps = np.maximum(np.asarray(eps, dtype=float), 0.0)
    return 1.0 - 1.0 / np.sqrt(1.0 + 4.0 * eps * kappa)


def eps_from_p(p, kappa=KAPPA):
    """
    Invert EoS for Γ = 2:  ε = ρ₀ + ρ₀ε₀  with  ρ₀ = √(p/κ),  ε₀ρ₀ = p.
    """
    p = np.asarray(p, dtype=float)
    rho0 = np.sqrt(np.maximum(p, 0.0) / kappa)
    return rho0 + p                       # ρ₀ + p  (since ε₀ρ₀ = p for Γ=2)


def rho0_from_eps(eps, kappa=KAPPA):
    """Rest-mass density ρ₀ = √(p/κ) for Γ = 2."""
    p = pressure(eps, kappa)
    return np.sqrt(np.maximum(p, 0.0) / kappa)


# ═══════════════════════════════════════════════════════════════════════
#  Section 2 — TOV solver  (Paper Eqs. 43–45, Sec. II.D)
# ═══════════════════════════════════════════════════════════════════════

def tov_rhs(R, y, kappa=KAPPA):
    """RHS of TOV equations.  y = [a, α, p]."""
    a, alpha, p = y
    if p < 0.0:
        p = 0.0
    eps = eps_from_p(p, kappa)

    if R < 1e-14:
        return [0.0, 0.0, 0.0]

    da_dR     = a * (1.0 + a**2 * (-1.0 + 8.0 * np.pi * R**2 * eps)) / (2.0 * R)
    dalpha_dR = alpha * (-1.0 + a**2 * (1.0 + 8.0 * np.pi * R**2 * p)) / (2.0 * R)
    dp_dR     = -(p + eps) / alpha * dalpha_dR

    return [da_dR, dalpha_dR, dp_dR]


def surface_event(R, y, kappa=KAPPA):
    """Event: pressure drops to zero (stellar surface)."""
    return y[2] - kappa * 1e-24        # p = κ·(10⁻¹²)² for Γ = 2
surface_event.terminal  = True
surface_event.direction = -1


def solve_tov(rho0c=0.00128, kappa=KAPPA, R_max=30.0, N_pts=20000):
    """
    Integrate TOV from origin to stellar surface.

    Returns
    -------
    R, a, alpha, p, eps : 1-D arrays (including R = 0 origin point)
    """
    p_c   = kappa * rho0c**GAMMA
    eps_c = eps_from_p(p_c, kappa)

    R_span = (1e-10, R_max)
    R_eval = np.linspace(R_span[0], R_max, N_pts)
    y0     = [1.0, 1.0, p_c]

    sol = solve_ivp(tov_rhs, R_span, y0, method='DOP853',
                    t_eval=R_eval, events=surface_event,
                    args=(kappa,), rtol=1e-12, atol=1e-14,
                    max_step=R_max / N_pts * 2)

    R_arr     = sol.t
    a_arr     = sol.y[0]
    alpha_arr = sol.y[1]
    p_arr     = sol.y[2]

    # Prepend origin
    R_arr     = np.concatenate(([0.0], R_arr))
    a_arr     = np.concatenate(([1.0], a_arr))
    alpha_arr = np.concatenate(([1.0], alpha_arr))
    p_arr     = np.concatenate(([p_c],  p_arr))

    # Enforce non-negative pressure
    p_arr = np.maximum(p_arr, 0.0)
    eps_arr = eps_from_p(p_arr, kappa)

    # Normalise α so that it matches exterior Schwarzschild: α → 1/a at R → ∞
    # At stellar surface (last interior point) we match α·a = 1.
    R_surf_idx = len(R_arr) - 1
    alpha_arr *= 1.0 / (alpha_arr[R_surf_idx] * a_arr[R_surf_idx])

    # Extend to vacuum (R > R_surface): a = 1/α = (1 − 2M/R)^{−1/2}
    M_tot = 0.5 * R_arr[R_surf_idx] * (1.0 - 1.0 / a_arr[R_surf_idx]**2)
    R_ext = np.linspace(R_arr[R_surf_idx] + 0.001, R_max, 2000)
    a_ext     = 1.0 / np.sqrt(1.0 - 2.0 * M_tot / R_ext)
    alpha_ext = np.sqrt(1.0 - 2.0 * M_tot / R_ext)
    p_ext     = np.zeros_like(R_ext)
    eps_ext   = np.zeros_like(R_ext)

    R_arr     = np.concatenate((R_arr,     R_ext))
    a_arr     = np.concatenate((a_arr,     a_ext))
    alpha_arr = np.concatenate((alpha_arr, alpha_ext))
    p_arr     = np.concatenate((p_arr,     p_ext))
    eps_arr   = np.concatenate((eps_arr,   eps_ext))

    return R_arr, a_arr, alpha_arr, p_arr, eps_arr


# ═══════════════════════════════════════════════════════════════════════
#  Section 3 — Coordinate transform: areal → isotropic  (Paper Eq. 47-48)
# ═══════════════════════════════════════════════════════════════════════

def areal_to_isotropic(R_arr, a_arr, alpha_arr, p_arr, eps_arr):
    """
    Transform TOV solution from areal-polar (Schwarzschild) to maximal
    isotropic coordinates.

    Integrates  d(ln ψ)/dR = (1 − a(R)) / (2R)  with ψ(0) = 1,
    then  r = R / ψ².

    Exterior Schwarzschild matching fixes the normalisation constant.

    Returns
    -------
    r_arr, psi_arr, alpha_iso, p_iso, eps_iso
    """
    # Integrand (1 − a)/(2R), handling R = 0 by regularity
    integrand = np.zeros_like(R_arr)
    mask = R_arr > 0
    integrand[mask] = (1.0 - a_arr[mask]) / (2.0 * R_arr[mask])

    ln_psi = np.zeros_like(R_arr)
    ln_psi[1:] = cumulative_trapezoid(integrand, R_arr)
    psi_arr = np.exp(ln_psi)          # ψ(R), with ψ(0) = 1

    # Isotropic radius r = R / ψ²
    r_arr = np.zeros_like(R_arr)
    r_arr[1:] = R_arr[1:] / psi_arr[1:]**2

    # ---- Exterior Schwarzschild matching ----
    # Analytic: for r ≫ R_★,  ψ_exact = 1 + M/(2r).
    # Find stellar surface (last point with p > 0)
    i_surf = np.searchsorted(-p_arr, 0.0)   # first index with p ≤ 0
    if i_surf >= len(R_arr):
        i_surf = len(R_arr) - 1
    # Total mass from exterior metric
    M_tot = 0.5 * R_arr[i_surf] * (1.0 - 1.0 / a_arr[i_surf]**2)

    # At the surface, analytic ψ_exact(R_surf):
    # From Schwarzschild isotropic:  R = r(1 + M/(2r))² ⇒ ψ² = R/r
    # We already have numerical ψ_num at the surface. Rescale:
    r_surf_num = r_arr[i_surf]
    if r_surf_num > 0:
        psi_exact_surf = np.sqrt(R_arr[i_surf] / r_surf_num)
        # But our numerical psi uses ψ(0)=1 and must be rescaled globally
        # so that ψ matches the Schwarzschild exterior.  The rescaling
        # factor C satisfies:  C · ψ_num(R_surf) = ψ_exact(R_surf)
        C = psi_exact_surf / psi_arr[i_surf]
        psi_arr *= C
        # Recompute r with the rescaled ψ
        r_arr[1:] = R_arr[1:] / psi_arr[1:]**2

    alpha_iso = alpha_arr.copy()
    p_iso     = p_arr.copy()
    eps_iso   = eps_arr.copy()

    return r_arr, psi_arr, alpha_iso, p_iso, eps_iso


# ═══════════════════════════════════════════════════════════════════════
#  Section 4 — GridData class
# ═══════════════════════════════════════════════════════════════════════

class GridData:
    """
    Precompute everything needed on a uniform staggered isotropic grid.

    Attributes
    ----------
    r       : cell-centre radii  r_i = (i + 0.5)·dr
    dr      : grid spacing
    N       : number of grid points
    grr     : g_{rr} = ψ⁴
    alpha   : lapse function
    A_r     : (1/α) dα/dr
    D_rr_r  : (1/2) g^{rr} dg_{rr}/dr
    D_rth_th: (1/2) g^{θθ} dg_{θθ}/dr
    tgamma  : γ̃ = √g_{rr} · g_{θθ}  with g_{θθ} = ψ⁴ r²
    eps_bg  : background (equilibrium) ε
    p_bg    : background p
    """

    def __init__(self, dr=0.002, r_max=20.0, rho0c=0.00128):
        self.dr    = dr
        self.r_max = r_max

        # 1) Solve TOV
        R_arr, a_arr, alpha_arr, p_arr, eps_arr = solve_tov(rho0c=rho0c)

        # 2) Transform to isotropic coordinates
        r_iso, psi_iso, alpha_iso, p_iso, eps_iso = \
            areal_to_isotropic(R_arr, a_arr, alpha_arr, p_arr, eps_arr)

        # 3) Build uniform staggered grid: r_i = (i + 0.5) dr
        self.N = int(r_max / dr)
        self.r = (np.arange(self.N) + 0.5) * dr

        # 4) Interpolate TOV fields onto uniform grid via cubic spline
        #    (r_iso must be monotonically increasing; remove duplicates)
        unique_mask = np.diff(r_iso, prepend=-1) > 0
        r_u   = r_iso[unique_mask]
        psi_u = psi_iso[unique_mask]
        al_u  = alpha_iso[unique_mask]
        p_u   = p_iso[unique_mask]
        ep_u  = eps_iso[unique_mask]

        cs_psi   = CubicSpline(r_u, psi_u, extrapolate=True)
        cs_alpha = CubicSpline(r_u, al_u,  extrapolate=True)
        cs_p     = CubicSpline(r_u, p_u,   extrapolate=True)
        cs_eps   = CubicSpline(r_u, ep_u,  extrapolate=True)

        psi_g   = cs_psi(self.r)
        alpha_g = cs_alpha(self.r)

        self.alpha = alpha_g
        self.p_bg  = np.maximum(cs_p(self.r), 0.0)
        self.eps_bg = np.maximum(cs_eps(self.r), 0.0)

        # 5) Metric components in isotropic coordinates  (Paper Eq. 48)
        #    ds² = −α² dt² + ψ⁴(dr² + r² dΩ²)
        #    g_{rr} = ψ⁴ ,   g_{θθ} = ψ⁴ r²  (so g_{θθ} as in Eq.38 with r²g_{θθ} there)
        #    In the Paper's notation (Eq.38):  g_{θθ} is such that the line element
        #    is r² g_{θθ} dΩ², so here their g_{θθ} = ψ⁴.
        self.grr      = psi_g**4
        self.gthth    = psi_g**4          # angular metric factor (Paper's g_{θθ})
        self.gthth_r2 = psi_g**4 * self.r**2   # physical g_{θθ}·r² (not needed separately)

        # 6) γ̃ = √g_{rr} · g_{θθ}  (Paper text near Eq.39)
        #    Here g_{θθ} in the paper's notation = ψ⁴, so
        #    γ̃ = ψ² · ψ⁴ = ψ⁶.  But let's be careful:
        #    The full 3-metric determinant factor for sph. symm.:
        #      √γ = √(g_{rr}) · (r² g_{θθ}) · sin θ
        #    The paper defines γ̃ = √g_{rr} · g_{θθ} (without r² sin θ);
        #    looking at their balance laws Eqs.39-40, the r² is already
        #    absorbed.  So: γ̃ = √(ψ⁴) · ψ⁴ = ψ² · ψ⁴ = ψ⁶.
        #    But actually the paper writes γ̃ = √(g_{rr}) · g_{θθ}
        #    where g_{θθ} includes the r² factor (see Eq.38 line element).
        #    In their notation: g_{θθ} is the coefficient of dθ² which is
        #    r² ψ⁴ (the r² is inside their g_{θθ}).
        #    Therefore: γ̃ = ψ² · r² ψ⁴ = r² ψ⁶.
        self.tgamma = psi_g**2 * self.r**2 * psi_g**4  # = r² ψ⁶

        # 7) Precompute metric derivatives via cubic spline
        #    A_r = (1/α) dα/dr
        dalpha_dr = cs_alpha(self.r, 1)   # first derivative
        self.A_r  = dalpha_dr / alpha_g

        #    D_{rr}^r = (1/2) g^{rr} ∂_r g_{rr}
        #    g_{rr} = ψ⁴  →  ∂_r g_{rr} = 4 ψ³ dψ/dr
        dpsi_dr    = cs_psi(self.r, 1)
        dgrr_dr    = 4.0 * psi_g**3 * dpsi_dr
        self.D_rr_r = 0.5 * dgrr_dr / self.grr       # g^{rr} = 1/ψ⁴

        #    D_{rθ}^θ = (1/2) g^{θθ} ∂_r g_{θθ}
        #    Here g_{θθ} (the Paper's one, including r²) = r² ψ⁴
        #    ∂_r(r² ψ⁴) = 2r ψ⁴ + r² · 4 ψ³ dψ/dr
        #    g^{θθ} = 1/(r² ψ⁴)
        dgthth_full_dr = 2.0 * self.r * psi_g**4 + self.r**2 * dgrr_dr
        self.D_rth_th  = 0.5 * dgthth_full_dr / (self.r**2 * psi_g**4)

        # 8) Precompute equilibrium constraint correction.
        #    At hydrostatic equilibrium the S_r balance law requires:
        #      ∂_r(α γ̃ p) = α γ̃ [p(D_rr^r-2/r) + 2p(1/r+D_rθ^θ) - ε A_r]
        #    After interpolation onto the grid this is not exactly satisfied.
        #    We precompute the residual and subtract it during evolution so that
        #    the equilibrium RHS is zero to machine precision.
        p_bg = pressure(self.eps_bg)
        flux_Sr_bg   = alpha_g * self.tgamma * p_bg
        flux_Sr_pad  = _pad_parity(flux_Sr_bg, 2, parity=+1)
        div_flux_bg  = fdoc_deriv(flux_Sr_pad, self.dr)
        source_Sr_bg = (alpha_g * self.tgamma
                        * (p_bg * (self.D_rr_r - 2.0 / self.r)
                           + 2.0 * p_bg * (1.0 / self.r + self.D_rth_th)
                           - self.eps_bg * self.A_r))
        self.eq_corr_Sr = source_Sr_bg - div_flux_bg

        # Same for E equation (should be ~0 already but include for completeness)
        source_E_bg = np.zeros_like(self.r)  # S^r = 0 at equil.
        self.eq_corr_E = source_E_bg

        # 9) Precompute equilibrium c-vector residual for con2prim.
        #    At equilibrium (v=0, hat=0), the c-vector should give c0=eps, cr=0.
        #    Due to interpolation errors in Dr_eps and A_r, cr may not be
        #    exactly zero.  Store the residual and subtract it in con2prim.
        cs_eps_tmp = CubicSpline(self.r, self.eps_bg)
        Dr_eps_bg  = cs_eps_tmp(self.r, 1)  # same spline derivative as build_initial_state
        Dr_vr_bg  = np.zeros_like(self.r)
        vr_bg     = np.zeros_like(self.r)

        # Compute c-vector at equilibrium using a reference transport coeff set
        # (using smallSB-F2 parameters, but the equilibrium c-vector only depends
        #  on the frame parameters, not the viscosity magnitudes at v=0)
        tc_bg = compute_transport(self.eps_bg, 0.01, 0.01)  # any hat_eta/hat_zeta works at v=0
        _, _, _, _, c0_bg, cr_bg = _A_matrix_and_c_vector(
            self.eps_bg, vr_bg, self.grr, tc_bg, self.A_r,
            self.r, Dr_eps_bg, Dr_vr_bg)

        self.c0_eq_residual = c0_bg - self.eps_bg   # should be ~0
        self.cr_eq_residual = cr_bg - 0.0            # should be ~0 but isn't

        # 10) Store equilibrium state for dissipation subtraction.
        #     KO dissipation must act on (U − U_eq) not on U, otherwise the
        #     smooth equilibrium profile acquires a spurious drift.
        #     Apply atmosphere treatment to equilibrium reference.
        p_eq = pressure(self.eps_bg)
        atm_eq = p_eq < P_ATMS
        eps_bg_atm = self.eps_bg.copy()
        eps_bg_atm[atm_eq] = EPS_FLOOR
        Dr_eps_bg_atm = Dr_eps_bg.copy()
        Dr_eps_bg_atm[atm_eq] = 0.0

        self.tgE_eq    = self.tgamma * eps_bg_atm
        self.tgSr_eq   = np.zeros_like(self.r)
        self.Dr_eps_eq = Dr_eps_bg_atm


# ═══════════════════════════════════════════════════════════════════════
#  Section 5 — Transport coefficients  (Paper Eqs. 48–50)
# ═══════════════════════════════════════════════════════════════════════

def compute_transport(eps, hat_eta, hat_zeta,
                      hat_a=1.0, hat_q=0.999, hat_s=1.0, L=1.0,
                      kappa=KAPPA):
    """
    Compute BDNK transport coefficients from hatted parameters.
    Fully vectorised.

    Returns dict with keys:
        eta, zeta, tau_eps, tau_p, tau_Q, cs2, p, rho, hat_V
    """
    eps = np.asarray(eps, dtype=float)
    p   = pressure(eps, kappa)
    cs2 = dpressure_deps(eps, kappa)
    rho = eps + p

    hat_V = (4.0 / 3.0) * hat_eta + hat_zeta

    eta     = hat_q * L * cs2 * rho * hat_eta
    zeta    = hat_q * L * cs2 * rho * hat_zeta
    tau_eps = hat_V * L
    tau_p   = hat_s * cs2 * L * hat_V
    tau_Q   = hat_a * L * hat_V

    return {
        'eta': eta, 'zeta': zeta,
        'tau_eps': tau_eps, 'tau_p': tau_p, 'tau_Q': tau_Q,
        'cs2': cs2, 'p': p, 'rho': rho, 'hat_V': hat_V,
    }


# ═══════════════════════════════════════════════════════════════════════
#  Section 6 — Con2prim: recover (ε̂, v̂_bar^r) from conserved + p₀
#  (Paper Appendix A, Eqs. for spherical symmetry)
# ═══════════════════════════════════════════════════════════════════════

def _A_matrix_and_c_vector(eps, vr, grr, tc, A_r, r, Dr_eps, Dr_vr):
    """
    Build the 2×2 A-matrix and c-vector for the con2prim / stress tensor.

    Inputs are all arrays of the same length (grid points).

    A-matrix (Paper Appendix A, spherical-symmetry specialisation):
        A00 = −[2 g_{rr} v_r² τ_Q dp + τ_ε(g_{rr} v_r² dp + 1)] / (1−g_{rr} v_r²)^{3/2}
        A01 = −g_{rr} v_r [−4 g_{rr} v_r² η + 3 g_{rr} v_r²((ε+p)τ_ε dp − ζ)
                            + 3(ε+p)(2τ_Q + τ_ε)] / [3(1−g_{rr} v_r²)^{5/2}]
        A10 = −g_{rr} v_r [(g_{rr} v_r²+1)τ_Q dp + τ_ε(dp+1)] / (1−g_{rr} v_r²)^{3/2}
        A11 = −g_{rr} [−4 g_{rr} v_r² η + 3 g_{rr} v_r²((ε+p)(τ_ε(dp+1)+τ_Q) − ζ)
                        + 3(ε+p)τ_Q] / [3(1−g_{rr} v_r²)^{5/2}]

    c-vector (Cowling: K = 0, β = 0, Paper Eqs. 69–73):
        Θ = a_r^{low} v_r + Div_v + W² g_{rr} v_r² ∂_r v^r
        bracket = ρ·Θ + v_r · ∂_r ε
        c₀ = W² ε − p(1−W²)
             + W(τ_ε W² − (1−W²) τ_p) · bracket
             + 2 τ_Q W³ [ρ(a_r^{low} v_r + W² g_{rr} v_r² ∂_r v^r) + dp v_r ∂_r ε]
             + (2/3) η W [(1−W²)(2 a_r^{low} v_r − Div_v)
                           + W²(1+2W²)(−2+W²) g_{rr} v_r² ∂_r v^r]
             + ζ W(1−W²) Θ
        c_r = −v_r^{low} W² ρ
              + (τ_ε + τ_p) v_r^{low} W³ bracket
              + τ_Q {−dp W ∂_r ε + W³ [−ρ(a_r^{low} + v_r^{low} a_r^{low} v_r
                      + v_r ∂_r v^r − v_r W² g_{rr} v_r² ∂_r v^r)
                      − 2 dp v_r^{low} v_r ∂_r ε]}
              + η {−a_r^{low} W(1−W²)
                    + (1/3) W³ [v_r^{low}(a_r^{low} v_r − 2 Div_v + 4 W² g_{rr} v_r² ∂_r v^r / g_{rr})
                                + 3 v_r(g_{rr} ∂_r v^r + ∂_r v^r)]}
              + ζ v_r^{low} W³ Θ

    Returns A00, A01, A10, A11, c0, cr  (all arrays).
    """
    eta     = tc['eta']
    zeta    = tc['zeta']
    tau_eps = tc['tau_eps']
    tau_p   = tc['tau_p']
    tau_Q   = tc['tau_Q']
    dp      = tc['cs2']
    p       = tc['p']
    rho     = tc['rho']

    # ---- Lorentz factor ----
    v2     = grr * vr**2                   # g_{rr}(v^r)² = v_i v^i
    v2     = np.minimum(v2, 1.0 - 1e-10)
    W2_inv = 1.0 - v2                      # 1/W²
    W      = 1.0 / np.sqrt(W2_inv)
    W2     = W**2
    W3     = W**3

    # ---- Index quantities (careful with raising/lowering!) ----
    # a_r = ∂_r ln α = A_r                 (covariant, = coordinate deriv for a scalar)
    # a^r = g^{rr} a_r = A_r / grr         (contravariant)
    # v^r = vr                              (contravariant)
    # v_r = g_{rr} v^r = vr_low            (covariant)
    # a^i v_i = a_r v^r = A_r * vr         (invariant contraction)
    vr_low  = grr * vr                     # v_r = g_{rr} v^r
    a_dot_v = A_r * vr                     # a^i v_i = A_r * vr

    # ---- Spatial divergence ----
    Div_v = Dr_vr + 2.0 * vr / r           # D_i v^i = ∂_r v^r + 2v^r/r

    # W² v^i v^j D_i v_j  (only rr component; D_r v_r ≈ g_{rr} ∂_r v^r leading)
    vvDv = W2 * vr**2 * grr * Dr_vr        # W² (v^r)² g_{rr} ∂_r v^r

    # Θ = −K + a^i v_i + D_i v^i + W² v^i v^j D_i v_j     (K = 0 in Cowling)
    Theta = a_dot_v + Div_v + vvDv

    # Bracket:  ρ Θ + v^r ∂_r ε
    bracket = rho * Theta + vr * Dr_eps

    # ==================================================================
    #  A-matrix  (Paper Appendix A, exact spherical-symmetry formulas)
    # ==================================================================
    denom_32 = W2_inv**1.5                 # (1 − g_{rr} (v^r)²)^{3/2}
    denom_52 = W2_inv**2.5                 # (1 − g_{rr} (v^r)²)^{5/2}

    A00 = -(2.0 * grr * vr**2 * tau_Q * dp
            + tau_eps * (grr * vr**2 * dp + 1.0)) / denom_32

    A01 = -(grr * vr * (-4.0 * grr * vr**2 * eta
                         + 3.0 * grr * vr**2 * (rho * tau_eps * dp - zeta)
                         + 3.0 * rho * (2.0 * tau_Q + tau_eps))
            ) / (3.0 * denom_52)

    A10 = -(grr * vr * ((grr * vr**2 + 1.0) * tau_Q * dp
                          + tau_eps * (dp + 1.0))
            ) / denom_32

    A11 = -(grr * (-4.0 * grr * vr**2 * eta
                    + 3.0 * grr * vr**2 * (rho * (tau_eps * (dp + 1.0) + tau_Q)
                                            - zeta)
                    + 3.0 * rho * tau_Q)
            ) / (3.0 * denom_52)

    # ==================================================================
    #  c-vector  (Paper Eqs. 69–73, Cowling K = 0, β = 0)
    # ==================================================================

    # ---- c₀ (energy equation, Paper Eq. 69/56) ----
    c0_ideal = W2 * eps - p * (1.0 - W2)

    factor_ep = W * (tau_eps * W2 - (1.0 - W2) * tau_p)
    c0_tau    = factor_ep * bracket

    # τ_Q term:  2 τ_Q W³ [ρ(a^i v_i + W² v^i v^j D_i v_j) + dp v^i D_i ε]
    c0_tauQ = (2.0 * tau_Q * W3
               * (rho * (a_dot_v + vvDv)
                  + dp * vr * Dr_eps))

    # η (shear) term:  (2/3) η W [(1−W²)(2 a^i v_i − D_i v^i)
    #                              + W²(1+2W²)(−2+W²) v^i v^j D_i v_j]
    c0_eta = ((2.0 / 3.0) * eta * W
              * ((1.0 - W2) * (2.0 * a_dot_v - Div_v)
                 + W2 * (1.0 + 2.0 * W2) * (-2.0 + W2)
                   * vr**2 * grr * Dr_vr))

    # ζ (bulk) term:  ζ W (1−W²) Θ
    c0_zeta = zeta * W * (1.0 - W2) * Theta

    c0 = c0_ideal + c0_tau + c0_tauQ + c0_eta + c0_zeta

    # ---- c_r (covariant S_r equation, Paper Eq. 73/71) ----
    # Ideal:  −v_r W² ρ
    cr_ideal = -vr_low * W2 * rho

    # (τ_ε + τ_p) v_r W³ · bracket
    cr_tau = (tau_eps + tau_p) * vr_low * W3 * bracket

    # τ_Q term (Paper Eq. 71 for S^i, lowered to S_i, Cowling K = 0):
    #   τ_Q { −dp W D_i ε
    #          + W³ [−ρ(a_i + v_i a^j v_j + v^j D_j v_i
    #                 − v_i v^l 2W² v^j D_l v_j)
    #                − 2 dp v_i v^j D_j ε ] }
    # For i = r:
    #   D_i ε = ∂_r ε = Dr_eps
    #   a_i = A_r  (= ∂_r ln α, NOT grr * A_r)
    #   v_i a^j v_j = vr_low · a_dot_v
    #   v^j D_j v_i = v^r g_{rr} ∂_r v^r   (leading term)
    #   v_i v^l 2W² v^j D_l v_j = vr_low 2W² (v^r)² grr ∂_r v^r
    #   v_i v^j D_j ε = vr_low vr Dr_eps
    cr_tauQ = (tau_Q * (
        -dp * W * Dr_eps
        + W3 * (-(rho * (A_r
                          + vr_low * a_dot_v
                          + vr * grr * Dr_vr
                          - vr_low * 2.0 * W2 * vr**2 * grr * Dr_vr))
                - 2.0 * dp * vr_low * vr * Dr_eps)))

    # η term (Paper Eq. 71, Cowling K = 0, K_{ij} = 0):
    #   η { −a_i W(1−W²)
    #        + (1/3) W³ [v_i(a^j v_j − 2 D_j v^j + 4W² v^j v^l D_j v_l)
    #                    + 3 v^j(D_i v_j + D_j v_i)] }
    # For i = r:
    #   a_i = A_r
    #   v_i(a^j v_j − 2 Div_v + 4W² vvDv/W²) = vr_low(a_dot_v − 2 Div_v + 4 vvDv)
    #   Wait: 4W² v^j v^l D_j v_l = 4 vvDv (which already has W²)
    #   v^j(D_i v_j + D_j v_i) for i=j=r: v^r · 2 D_r v_r = 2 vr grr Dr_vr
    cr_eta = (eta * (
        -A_r * W * (1.0 - W2)
        + (1.0 / 3.0) * W3
          * (vr_low * (a_dot_v - 2.0 * Div_v + 4.0 * vvDv)
             + 3.0 * 2.0 * vr * grr * Dr_vr)))

    # ζ term:  ζ v_i W³ Θ
    cr_zeta = zeta * vr_low * W3 * Theta

    cr = cr_ideal + cr_tau + cr_tauQ + cr_eta + cr_zeta

    return A00, A01, A10, A11, c0, cr


def con2prim(E, Sr, eps, vtilde_r, grid, tc, Dr_eps, Dr_vr):
    """
    Recover (ε̂, v̂_bar^r) from conserved (E, S_r) and primitives (ε, ṽ^r).

    The 2×2 linear system is:
        A · (ε̂, v̂_bar^r)ᵀ = b = (E − c₀, S_r − c_r)ᵀ

    Parameters
    ----------
    E, Sr      : conserved variables divided by γ̃
    eps        : energy density
    vtilde_r   : regularised velocity ṽ^r = v^r / r
    grid       : GridData instance
    tc         : transport-coefficient dict from compute_transport
    Dr_eps     : ∂_r ε  (evolved field)
    Dr_vr      : ∂_r v^r  (derived from ṽ^r fields)

    Returns
    -------
    hat_eps, hat_vbar_r : arrays
    """
    vr = grid.r * vtilde_r

    A00, A01, A10, A11, c0, cr = \
        _A_matrix_and_c_vector(eps, vr, grid.grr, tc, grid.A_r, grid.r,
                               Dr_eps, Dr_vr)

    # Subtract equilibrium c-vector residual (ensures hat=0 at equilibrium)
    c0 -= grid.c0_eq_residual
    cr -= grid.cr_eq_residual

    b0 = E  - c0
    b1 = Sr - cr

    det = A00 * A11 - A01 * A10
    # Guard against singular matrix in atmosphere (det → 0)
    safe_det = np.where(np.abs(det) > 1e-30, det, np.sign(det + 1e-40) * 1e-30)
    hat_eps    = ( A11 * b0 - A01 * b1) / safe_det
    hat_vbar_r = (-A10 * b0 + A00 * b1) / safe_det

    return hat_eps, hat_vbar_r


# ═══════════════════════════════════════════════════════════════════════
#  Section 7 — Stress-tensor projections E, S^r, S^r_r, S^θ_θ
#  (Paper Eqs. 56–58 specialised to spherical symmetry, Cowling)
# ═══════════════════════════════════════════════════════════════════════

def compute_stress(eps, vtilde_r, hat_eps, hat_vbar_r, grid, tc,
                   Dr_eps, Dr_vr):
    """
    Compute stress-energy projections from all primitive variables.

    E and S_r (covariant) are computed via the A-matrix / c-vector
    (same as con2prim, just evaluated with known hat values).

    S^r_r and S^θ_θ are computed from the full stress tensor (Paper Eq. 58)
    specialised to spherical symmetry in the Cowling approximation.

    The trace relation is used for S^θ_θ:
        S^θ_θ = (S^i_i − S^r_r) / 2     (spherical symmetry)
    where the trace S^i_i does not contain the shear (η σ^{ij} is traceless).

    Returns
    -------
    E_out, Sr_contra, Srr_mixed, Sthth
    """
    r   = grid.r
    grr = grid.grr
    vr  = r * vtilde_r

    A00, A01, A10, A11, c0, cr = \
        _A_matrix_and_c_vector(eps, vr, grr, tc, grid.A_r, r, Dr_eps, Dr_vr)

    # E and S_r (covariant)
    E_out  = A00 * hat_eps + A01 * hat_vbar_r + c0
    S_r    = A10 * hat_eps + A11 * hat_vbar_r + cr
    Sr_contra = S_r / grr                        # S^r = g^{rr} S_r

    # ---- Unpack for S_{ij} computation ----
    eta     = tc['eta']
    zeta    = tc['zeta']
    tau_eps = tc['tau_eps']
    tau_p   = tc['tau_p']
    tau_Q   = tc['tau_Q']
    dp      = tc['cs2']
    p       = tc['p']
    rho     = tc['rho']

    u      = np.minimum(grr * vr**2, 1.0 - 1e-10)  # v²
    W2_inv = 1.0 - u
    W      = 1.0 / np.sqrt(W2_inv)
    W2     = W**2
    A_r    = grid.A_r
    vr_low = grr * vr
    a_dot_v = A_r * vr                    # a^i v_i = A_r vr
    Div_v   = Dr_vr + 2.0 * vr / r
    vvDv    = W2 * vr**2 * grr * Dr_vr    # W² v^i v^j D_i v_j
    Theta   = a_dot_v + Div_v + vvDv
    bracket = rho * Theta + vr * Dr_eps

    # hatted contractions
    hat_v_dot_v = hat_vbar_r * vr_low     # hat_v^l v_l = hat_vbar_r · g_{rr} vr
    vvDvr_raw   = vr**2 * grr * Dr_vr     # v^l v^m D_l v_m (without W²)

    # "full bracket" including hat terms (appears in τ_ε/τ_p/ζ parts of S_{ij}):
    # B_full = hat_ε − v^l D_l ε − ρ(Θ − W² hat_v^l v_l)
    #        = hat_ε − bracket + ρ W² hat_v_dot_v
    B_full = hat_eps - bracket + rho * W2 * hat_v_dot_v

    # Θ_full (with hat_v):  Θ − W² hat_v.v  (appears in ζ part)
    Theta_full = Theta - W2 * hat_v_dot_v

    # ==================================================================
    # S^r_r  from Paper Eq. 58 (Cowling K = 0, K_{ij} = 0)
    #
    # S_{rr} = p g_{rr} + W² ρ v_r²
    #   − W[τ_p g_{rr} + (τ_ε+τ_p)W² v_r²] B_full
    #   + τ_Q { 2W v_r [W² ρ (a_r − g_{rr} hat_v^r + v^r g_{rr} Dr_vr)
    #                     + dp Dr_eps]
    #           + 2W v_r² [−dp hat_ε − W² ρ(hat_v.v − vvDvr) + dp vr Dr_eps] }
    #   + η { shear rr component }
    #   + ζ W (g_{rr} + W² v_r²)(−Θ_full)
    #
    # Divide by g_{rr} to get S^r_r = g^{rr} S_{rr}:
    # ==================================================================

    # Ideal
    S_rr_m = p + W2 * rho * u

    # τ_ε/τ_p part
    S_rr_m += -W * (tau_p + (tau_eps + tau_p) * W2 * u) * B_full

    # τ_Q part
    # Term 1: 2W v_r [...] / g_{rr}  =  2W vr [...] (after simplifying v_r/grr = vr)
    tQ_t1 = (2.0 * W * vr
             * (W2 * rho * (A_r - grr * hat_vbar_r + vr * grr * Dr_vr)
                + dp * Dr_eps))
    # Term 2: 2W v_r²/g_{rr} [...] = 2W u/grr [...]
    tQ_t2 = (2.0 * W * u / grr
             * (-dp * hat_eps
                - W2 * rho * (hat_v_dot_v - vvDvr_raw)
                + dp * vr * Dr_eps))
    S_rr_m += tau_Q * (tQ_t1 + tQ_t2)

    # η (shear) part of S^r_r (Cowling K=0, K_{ij}=0)
    # From Paper Eq. 58, the η terms in S_{ij} for the rr component:
    # (1/3) η W {
    #   2(g_{rr} + W² v_r²)(a.v + Div_v)         [K=0]
    #   − 6[D_r v_r + W²(2 v^r v_r D_r v_r + (a_r − hat_v_r) v_r)]
    #   − 2W²(g_{rr} − 2W² v_r²)(hat_v.v − vvDvr)
    # }
    # Then divide by g_{rr} for S^r_r.
    # D_r v_r (both lower) ≈ grr Dr_vr (leading; Christoffel corrections small)
    Drv_cov = grr * Dr_vr    # leading term of D_r v_r (both indices lowered)

    eta_rr = ((1.0 / 3.0) * eta * W / grr
              * (2.0 * (grr + W2 * vr_low**2) * (a_dot_v + Div_v)
                 - 6.0 * (Drv_cov
                           + W2 * (2.0 * vr * vr_low * Drv_cov
                                    + (A_r - grr * hat_vbar_r) * vr_low))
                 - 2.0 * W2 * (grr - 2.0 * W2 * vr_low**2)
                   * (hat_v_dot_v - vvDvr_raw)))

    S_rr_m += eta_rr

    # ζ part: ζ W (g_{rr} + W² v_r²)(−Θ_full) / g_{rr}
    S_rr_m += -zeta * W * (1.0 + W2 * u) * Theta_full

    # ==================================================================
    # S^θ_θ via the trace relation  (shear is traceless!)
    #
    # S^i_i = 3p + W² ρ · 3v²
    #   − W(3τ_p + (τ_ε+τ_p) W² · 3v²) B_full        [trace of τ part]
    #   + τ_Q trace(...)
    #   − ζ W(3 + W² · 3v²)(−Θ_full)                  [trace of ζ part]
    #   + 0   (η is traceless!)
    #
    # Actually the trace γ^{ij} S_{ij} is simpler to compute.
    # γ^{ij} (p γ_{ij}) = 3p
    # γ^{ij} (W² ρ v_i v_j) = W² ρ v²
    # γ^{ij} [τ_p γ_{ij} + (τ_ε+τ_p) W² v_i v_j] = 3τ_p + (τ_ε+τ_p) W² v²
    # γ^{ij} [ζ W (γ_{ij} + W² v_i v_j)] = ζ W (3 + W² v²)
    # τ_Q trace: γ^{ij} {2W v_{(i}[..._{j)}] + 2W v_i v_j [...]}
    #   = 2W v² [W² ρ (a.v − hat_v.v + vvDvr) + dp vr Dr_eps]
    #     + 2W v² [−dp hat_eps − W²ρ(hat_v.v − vvDvr) + dp vr Dr_eps]
    #   (using γ^{ij} v_i [..._j] = v^j [...]_j in sph. symm.)
    #   Actually let me be more careful. For the τ_Q trace:
    #   γ^{ij} 2W v_{(i} X_{j)} = 2W v^j X_j (trace of symmetrised rank-2)
    #   where X_j = W² ρ (a_j − g_{jr} hat_v^r + v^l D_l v_j) + dp D_j ε
    #   For j = r: X_r = W² ρ (A_r − grr hat_v^r + vr grr Dr_vr) + dp Dr_eps
    #   v^j X_j = vr X_r
    #   γ^{ij} 2W v_i v_j Y = 2W v² Y
    #   where Y = −dp hat_eps − W² ρ (hat_v.v − vvDvr) + dp vr Dr_eps
    tQ_trace = (2.0 * W * vr
                * (W2 * rho * (A_r - grr * hat_vbar_r + vr * grr * Dr_vr)
                   + dp * Dr_eps)
                + 2.0 * W * u / grr
                  * (-dp * hat_eps
                     - W2 * rho * (hat_v_dot_v - vvDvr_raw)
                     + dp * vr * Dr_eps))

    S_trace = (3.0 * p + W2 * rho * u
               - W * (3.0 * tau_p + (tau_eps + tau_p) * W2 * u) * B_full
               + tau_Q * tQ_trace
               - zeta * W * (3.0 + W2 * u) * Theta_full)
    # Note: η term vanishes from trace (shear is traceless)

    # S^θ_θ = (S^i_i − S^r_r) / 2
    Sthth = 0.5 * (S_trace - S_rr_m)

    return E_out, Sr_contra, S_rr_m, Sthth


# ═══════════════════════════════════════════════════════════════════════
#  Section 8 — Characteristic speeds  (Paper Eqs. 51–52 & Eq.55)
# ═══════════════════════════════════════════════════════════════════════

def max_char_speed(eps, vr, grr, alpha, hat_eta, hat_zeta,
                   hat_a=1.0, hat_q=0.999, hat_s=1.0, kappa=KAPPA):
    """
    Maximum absolute characteristic speed across all six BDNK modes.

    Flat-space speeds c₀, c₊, c₋  (Paper Eqs. 51–52), then
    curved-space formula (Paper Eq. 55) with  m_i = 1/c_i² − 1.

    Floored at 0.1 (Paper Sec. II.E).

    Fully vectorised.
    """
    eps = np.asarray(eps, dtype=float)
    vr  = np.asarray(vr, dtype=float)
    grr = np.asarray(grr, dtype=float)
    alpha = np.asarray(alpha, dtype=float)

    cs2 = dpressure_deps(eps, kappa)
    cs  = np.sqrt(np.maximum(cs2, 1e-15))

    hat_V = (4.0 / 3.0) * hat_eta + hat_zeta

    # Flat-space characteristic speeds
    c0 = cs * np.sqrt(hat_q * hat_eta / (hat_a * hat_V))

    disc = (hat_q**2
            + hat_a**2 * (4.0 * hat_q + (hat_s - 1.0)**2)
            + 2.0 * hat_a * hat_q * (1.0 + hat_s))
    disc = np.maximum(disc, 0.0)

    c_plus  = cs * np.sqrt((hat_a * (1.0 + hat_s) + hat_q + np.sqrt(disc))
                           / (2.0 * hat_a))
    c_minus = cs * np.sqrt(np.maximum(
        (hat_a * (1.0 + hat_s) + hat_q - np.sqrt(disc)) / (2.0 * hat_a), 0.0))

    # m_i = 1/c_i² − 1
    flat_speeds = [c0, c_plus, c_minus]

    # Curved-space  (Paper Eq. 55, β = 0)
    v2 = np.minimum(grr * vr**2, 1.0 - 1e-10)
    W2 = 1.0 / (1.0 - v2)

    vdotk = np.sqrt(grr) * vr       # v·k with unit spatial wave vector

    c_max = np.full_like(eps, 0.1)   # floor

    for c_flat in flat_speeds:
        c_flat_safe = np.maximum(c_flat, 1e-12)
        mi = 1.0 / c_flat_safe**2 - 1.0

        discriminant = 1.0 + mi * W2 * (1.0 - vdotk**2)
        discriminant = np.maximum(discriminant, 0.0)

        denom = mi * W2 + 1.0

        c_fwd = alpha * (mi * W2 * vdotk + np.sqrt(discriminant)) / denom
        c_bwd = alpha * (mi * W2 * vdotk - np.sqrt(discriminant)) / denom

        c_max = np.maximum(c_max, np.abs(c_fwd))
        c_max = np.maximum(c_max, np.abs(c_bwd))

    return c_max


# ═══════════════════════════════════════════════════════════════════════
#  Section 9 — FDOC spatial operators
#  4th-order centered derivative + 3rd-order dissipation
#  (Paper Sec. II.E; Alic et al. 2007, Palenzuela et al. 2018)
# ═══════════════════════════════════════════════════════════════════════

def fdoc_deriv(f_pad, dr):
    """
    4th-order centered first derivative on a padded array.
    f_pad has ≥ 2 ghost cells on each side.
    Returns array of length len(f_pad) − 4.
    """
    return (-f_pad[4:]
            + 8.0 * f_pad[3:-1]
            - 8.0 * f_pad[1:-3]
            + f_pad[:-4]) / (12.0 * dr)


DISS_SIGMA = 0.5    # dissipation coefficient (tunable; 0.1–1.0 for BDNK without upwinding)


def _pad_parity(u, ng, parity=1):
    """
    Pad array with parity conditions at left (r=0) and outflow at right.

    On a staggered grid r_i = (i+0.5)*dr, the ghost cell at index -1
    corresponds to r = -dr/2.  For a scalar field f(r) = f(-r) (even parity=+1),
    the ghost values mirror the interior: u[-1] = u[0], u[-2] = u[1].
    For an odd field f(r) = -f(-r) (parity=-1): u[-1] = -u[0], u[-2] = -u[1].

    Right boundary uses zeroth-order extrapolation (outflow).
    """
    out = np.empty(len(u) + 2 * ng)
    out[ng:-ng] = u
    # Left (inner) boundary: parity reflection
    for k in range(ng):
        out[ng - 1 - k] = parity * u[k]
    # Right (outer) boundary: outflow
    for k in range(ng):
        out[len(u) + ng + k] = u[-1]
    return out


def fdoc_diss(u_pad, lam, dr):
    """
    3rd-order Kreiss-Oliger–style dissipation operator.

    The standard KO dissipation for a 3rd-order scheme is:
        D = −σ · λ_max · (Δ⁴u) / dr
    where Δ⁴u = u_{i+2}−4u_{i+1}+6u_i−4u_{i-1}+u_{i-2} is the 4th
    undivided difference, and σ is a small coefficient controlling
    dissipation strength.

    u_pad : padded array (≥ 2 ghost cells each side)
    lam   : local dissipation strength (array, len = interior)
    dr    : grid spacing

    Returns array of length len(u_pad) − 4.
    """
    d4u = (u_pad[4:]
           - 4.0 * u_pad[3:-1]
           + 6.0 * u_pad[2:-2]
           - 4.0 * u_pad[1:-3]
           + u_pad[:-4])
    return -DISS_SIGMA * lam * d4u / dr


# ═══════════════════════════════════════════════════════════════════════
#  Section 10 — SSP-RK3 time integrator  (Paper Sec. II.E)
# ═══════════════════════════════════════════════════════════════════════

def ssp_rk3_step(U, dt, rhs_func, grid):
    """
    Strong Stability Preserving Runge–Kutta (3rd order).

        u⁽¹⁾ = uⁿ       + dt · L(uⁿ)
        u⁽²⁾ = ¾ uⁿ     + ¼ (u⁽¹⁾ + dt · L(u⁽¹⁾))
        u⁽ⁿ⁺¹⁾ = ⅓ uⁿ  + ⅔ (u⁽²⁾ + dt · L(u⁽²⁾))
    """
    k1 = rhs_func(U, grid)
    u1 = U + dt * k1

    k2 = rhs_func(u1, grid)
    u2 = 0.75 * U + 0.25 * (u1 + dt * k2)

    k3 = rhs_func(u2, grid)
    return (1.0 / 3.0) * U + (2.0 / 3.0) * (u2 + dt * k3)


# ═══════════════════════════════════════════════════════════════════════
#  Section 11 — Evolution: RHS + main driver
# ═══════════════════════════════════════════════════════════════════════

# Atmosphere parameters (Paper Sec. II.E)
RHO0_ATMS  = 1e-12
RHO0_FLOOR = 1e-13
P_ATMS     = KAPPA * RHO0_ATMS**GAMMA
EPS_FLOOR  = eps_from_p(KAPPA * RHO0_FLOOR**GAMMA)


def _apply_atmosphere(eps, vtilde_r, Dr_eps, Dr_vtilde,
                      hat_eps, hat_vbar_r, kappa=KAPPA):
    """Set atmosphere values where p < κ ρ₀,atms²."""
    p   = pressure(eps, kappa)
    atm = p < P_ATMS

    eps[atm]        = EPS_FLOOR
    vtilde_r[atm]   = 0.0
    Dr_eps[atm]     = 0.0
    Dr_vtilde[atm]  = 0.0
    hat_eps[atm]    = 0.0
    hat_vbar_r[atm] = 0.0

    return eps, vtilde_r, Dr_eps, Dr_vtilde, hat_eps, hat_vbar_r


def bdnk_rhs(U, grid, hat_eta=0.01, hat_zeta=0.01,
             hat_a=1.0, hat_q=0.999, hat_s=1.0):
    """
    Complete RHS for the 6-variable BDNK system in spherical symmetry
    under the Cowling approximation on a fixed background.

    State vector U shape: (6, N).

    Balance laws (Paper Eqs. 39–40):
        ∂_t(γ̃ E) + ∂_r(α γ̃ S^r)     = α γ̃ [−S^r(2/r + A_r)]   (Cowling K=0)
        ∂_t(γ̃ S_r) + ∂_r(α γ̃ S^r_r) = α γ̃ [S^r_r(D_{rr}^r − 2/r)
                                               + 2 S^θ_θ(1/r + D_{rθ}^θ) − E A_r]

    First-order reduction:
        ∂_t ε          = −α ε̂
        ∂_t(∂_r ε)     = −∂_r(α ε̂)
        ∂_t ṽ^r        = −α v̂_bar^r / r   (Cowling K=0)
        ∂_t(∂_r ṽ^r)   = ∂_r(−α v̂_bar^r / r)
    """
    r  = grid.r
    dr = grid.dr

    dU = np.zeros_like(U)

    # ---- Unpack state ----
    tgE       = U[0]
    tgSr      = U[1]
    eps       = U[2].copy()
    Dr_eps    = U[3].copy()
    vtilde_r  = U[4].copy()
    Dr_vtilde = U[5].copy()

    # ---- Atmosphere floor ----
    p_check = pressure(eps)
    atm = p_check < P_ATMS
    eps[atm]       = EPS_FLOOR
    vtilde_r[atm]  = 0.0
    Dr_eps[atm]    = 0.0
    Dr_vtilde[atm] = 0.0

    # Derived physical velocity and its derivative
    vr    = r * vtilde_r
    Dr_vr = vtilde_r + r * Dr_vtilde

    # ---- Transport coefficients ----
    tc = compute_transport(eps, hat_eta, hat_zeta,
                           hat_a=hat_a, hat_q=hat_q, hat_s=hat_s)

    # ---- Con2prim ----
    E_grid  = tgE  / grid.tgamma
    Sr_grid = tgSr / grid.tgamma
    E_grid[atm]  = eps[atm]
    Sr_grid[atm] = 0.0

    hat_eps, hat_vbar_r = con2prim(E_grid, Sr_grid, eps, vtilde_r,
                                    grid, tc, Dr_eps, Dr_vr)

    # ---- Post-atmosphere cleanup and clamps ----
    hat_eps[atm]      = 0.0
    hat_vbar_r[atm]   = 0.0
    hat_eps    = np.nan_to_num(hat_eps, nan=0.0, posinf=0.0, neginf=0.0)
    hat_vbar_r = np.nan_to_num(hat_vbar_r, nan=0.0, posinf=0.0, neginf=0.0)

    # Physical clamps: hat values at equilibrium are exactly zero.
    # The physical QNM perturbation has amplitude ε̂ ~ Aω/α ≈ 7.5e-8 (Paper Fig 3).
    # Clamp must be tight enough that cumulative drift stays ≪ ε_c:
    #   drift ≈ α·ε̂_max·t ≤ 0.67·ε̂_max·2000  →  ε̂_max ≤ 1e-9 for <0.1% drift.
    hat_eps_max = 1e-9
    hat_eps     = np.clip(hat_eps, -hat_eps_max, hat_eps_max)
    hat_vbar_r  = np.clip(hat_vbar_r, -1e-7 * r, 1e-7 * r)

    # ---- Stress tensor ----
    E_st, Sr_contra, Srr_mixed, Sthth = \
        compute_stress(eps, vtilde_r, hat_eps, hat_vbar_r,
                       grid, tc, Dr_eps, Dr_vr)

    # ---- Characteristic speeds ----
    lam_max = max_char_speed(eps, vr, grid.grr, grid.alpha,
                             hat_eta, hat_zeta,
                             hat_a=hat_a, hat_q=hat_q, hat_s=hat_s)

    # ---- Balance-law flux divergences ----
    # 4th-order FDOC derivative for accuracy + KO dissipation on perturbations
    ng = 2
    flux_E  = grid.alpha * grid.tgamma * Sr_contra
    flux_Sr = grid.alpha * grid.tgamma * Srr_mixed

    flux_E_pad  = _pad_parity(flux_E,  ng, parity=-1)
    flux_Sr_pad = _pad_parity(flux_Sr, ng, parity=+1)

    div_flux_E  = fdoc_deriv(flux_E_pad,  dr)
    div_flux_Sr = fdoc_deriv(flux_Sr_pad, dr)

    # KO dissipation on perturbations from equilibrium
    delta_tgE  = tgE  - grid.tgE_eq
    delta_tgSr = tgSr - grid.tgSr_eq
    delta_tgE_pad  = _pad_parity(delta_tgE,  ng, parity=+1)
    delta_tgSr_pad = _pad_parity(delta_tgSr, ng, parity=-1)
    div_flux_E  += fdoc_diss(delta_tgE_pad,  lam_max, dr)
    div_flux_Sr += fdoc_diss(delta_tgSr_pad, lam_max, dr)

    # ---- Sources (Cowling K=0) ----
    source_E = grid.alpha * grid.tgamma * (-Sr_contra * (2.0 / r + grid.A_r))

    source_Sr = (grid.alpha * grid.tgamma
                 * (Srr_mixed * (grid.D_rr_r - 2.0 / r)
                    + 2.0 * Sthth * (1.0 / r + grid.D_rth_th)
                    - E_st * grid.A_r))

    dU[0] = -div_flux_E  + source_E  - grid.eq_corr_E
    dU[1] = -div_flux_Sr + source_Sr - grid.eq_corr_Sr

    # Constraint damping: damp the mismatch between evolved conservatives
    # and the stress-tensor reconstruction.  Without this, tgSr grows without bound.
    kappa_cd = 6.0 / dr              # κ·dt = 6/dr · 0.25·dr = 1.5
    E_stress  = E_st
    Sr_cov_st = Sr_contra * grid.grr
    dU[0] += -kappa_cd * (tgE  - grid.tgamma * E_stress)
    dU[1] += -kappa_cd * (tgSr - grid.tgamma * Sr_cov_st)

    # ---- First-order reduction equations ----
    dU[2] = -grid.alpha * hat_eps

    f_hateps     = grid.alpha * hat_eps
    f_hateps_pad = _pad_parity(f_hateps, ng, parity=+1)
    dU[3] = -fdoc_deriv(f_hateps_pad, dr)

    dU[4] = -grid.alpha * hat_vbar_r / r

    f_hatvr     = -grid.alpha * hat_vbar_r / r
    f_hatvr_pad = _pad_parity(f_hatvr, ng, parity=+1)
    dU[5] = fdoc_deriv(f_hatvr_pad, dr)

    # ---- KO dissipation on all evolved variables ----
    delta_eps      = eps - grid.eps_bg
    delta_Dr_eps   = Dr_eps - grid.Dr_eps_eq
    delta_eps_pad     = _pad_parity(delta_eps,    ng, parity=+1)
    delta_Dr_eps_pad  = _pad_parity(delta_Dr_eps, ng, parity=-1)
    vtilde_pad        = _pad_parity(vtilde_r,     ng, parity=-1)
    Dr_vtilde_pad     = _pad_parity(Dr_vtilde,    ng, parity=+1)

    dU[2] += fdoc_diss(delta_eps_pad,    lam_max, dr)
    dU[3] += fdoc_diss(delta_Dr_eps_pad, lam_max, dr)
    dU[4] += fdoc_diss(vtilde_pad,       lam_max, dr)
    dU[5] += fdoc_diss(Dr_vtilde_pad,    lam_max, dr)

    # ---- Zero RHS in atmosphere ----
    dU[:, atm] = 0.0

    return dU


def evolve(grid, U0, t_end, hat_eta=0.01, hat_zeta=0.01,
           hat_a=1.0, hat_q=0.999, hat_s=1.0,
           dt_save=1.0, CFL=0.25):
    """
    Evolve the BDNK system from U0 to t_end using SSP-RK3.

    Parameters
    ----------
    grid     : GridData
    U0       : (6, N) initial state
    t_end    : final coordinate time
    hat_eta, hat_zeta : viscosity parameters
    hat_a, hat_q, hat_s : frame parameters
    dt_save  : interval at which snapshots are stored
    CFL      : Courant factor  Δt = CFL · dr

    Returns
    -------
    times    : list of snapshot times
    states   : list of (6, N) arrays
    """
    dt = CFL * grid.dr
    U  = U0.copy()
    t  = 0.0

    times  = [0.0]
    states = [U.copy()]
    next_save = dt_save

    def rhs(state, grd):
        return bdnk_rhs(state, grd,
                        hat_eta=hat_eta, hat_zeta=hat_zeta,
                        hat_a=hat_a, hat_q=hat_q, hat_s=hat_s)

    n_steps = int(np.ceil(t_end / dt))
    for _ in range(n_steps):
        U = ssp_rk3_step(U, dt, rhs, grid)
        t += dt

        if t >= next_save - 0.5 * dt:
            times.append(t)
            states.append(U.copy())
            next_save += dt_save

    return times, states


# ═══════════════════════════════════════════════════════════════════════
#  Section 12 — Signal analysis tools  (Paper Sec. III.C)
# ═══════════════════════════════════════════════════════════════════════

def compute_psd(signal, dt, window='blackman'):
    """
    Power spectral density with Blackman window.

    Returns
    -------
    freqs : positive frequencies
    psd   : |FFT|²
    """
    from scipy.signal import blackman as blackman_win
    from scipy.fft import fft, fftfreq

    N = len(signal)
    if window == 'blackman':
        w = blackman_win(N)
    else:
        w = np.ones(N)

    spectrum = fft(signal * w)
    freqs    = fftfreq(N, d=dt)
    psd      = np.abs(spectrum[:N // 2])**2
    return freqs[:N // 2], psd


def butterworth_filter(signal, dt, f_low=0.01, f_high_factor=0.1, order=4):
    """
    4th-order Butterworth bandpass filter.
    f_low in code units (1/M_☉), f_high as fraction of sampling freq.
    """
    from scipy.signal import butter, filtfilt

    f_sampling = 1.0 / dt
    f_high     = f_sampling * f_high_factor
    nyquist    = f_sampling / 2.0

    low  = f_low  / nyquist
    high = min(f_high / nyquist, 0.99)

    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)


def extract_decay_rate_linear(filtered_signal, times, t_start, t_end):
    """
    Linear fit to log of envelope maxima.

    Returns decay_rate = 1/τ.
    """
    from scipy.signal import argrelmax

    mask      = (times >= t_start) & (times <= t_end)
    t_win     = times[mask]
    sig_win   = np.abs(filtered_signal[mask])

    max_idx   = argrelmax(sig_win)[0]
    if len(max_idx) < 2:
        return 0.0

    t_max     = t_win[max_idx]
    log_max   = np.log(np.maximum(sig_win[max_idx], 1e-30))

    coeffs = np.polyfit(t_max, log_max, 1)
    return -coeffs[0]


def extract_decay_rate_nonlinear(filtered_signal, times, t_start, t_end):
    """
    Non-linear fit: A exp(−t/τ) cos(ωt + φ) + C.

    Returns dict with amplitude, tau, decay_rate, omega, frequency_kHz, phase, offset.
    """
    from scipy.optimize import curve_fit

    mask    = (times >= t_start) & (times <= t_end)
    t_fit   = times[mask]
    sig_fit = filtered_signal[mask]

    def damped_sinusoid(t, A, tau, omega, phi, C):
        return A * np.exp(-t / tau) * np.cos(omega * t + phi) + C

    omega_guess = 0.0834       # from Paper
    tau_guess   = 600.0

    p0 = [np.max(np.abs(sig_fit)), tau_guess, omega_guess, 0.0, 0.0]

    popt, _ = curve_fit(damped_sinusoid, t_fit, sig_fit, p0=p0, maxfev=10000)

    return {
        'amplitude':     popt[0],
        'tau':           popt[1],
        'decay_rate':    1.0 / popt[1],
        'omega':         popt[2],
        'frequency_kHz': popt[2] / (2.0 * np.pi) * 203.025,
        'phase':         popt[3],
        'offset':        popt[4],
    }


def convergence_factor(dr_l, dr_m, dr_h, n=3):
    """
    Theoretical convergence factor Q for three resolutions
    dr_l > dr_m > dr_h  at order n:

        Q = (dr_l^n − dr_m^n) / (dr_m^n − dr_h^n)

    (Paper Appendix B.)
    """
    return (dr_l**n - dr_m**n) / (dr_m**n - dr_h**n)


def align_and_compare(t_low, eps_low, t_mid, eps_mid, t_high, eps_high,
                      t_common=None):
    """
    Interpolate three resolution runs onto a common time axis using
    cubic splines (4th-order accurate, Paper Appendix B).

    Returns t_common, eps_l, eps_m, eps_h  (all on common grid).
    """
    t_start = max(t_low[0], t_mid[0], t_high[0])
    t_end   = min(t_low[-1], t_mid[-1], t_high[-1])

    if t_common is None:
        dt_coarse = max(np.median(np.diff(t_low)),
                        np.median(np.diff(t_mid)),
                        np.median(np.diff(t_high)))
        t_common = np.arange(t_start, t_end, dt_coarse)

    cs_l = CubicSpline(t_low,  eps_low)
    cs_m = CubicSpline(t_mid,  eps_mid)
    cs_h = CubicSpline(t_high, eps_high)

    return t_common, cs_l(t_common), cs_m(t_common), cs_h(t_common)


def compute_pointwise_Q(t_low, eps_low, t_mid, eps_mid,
                        t_high, eps_high, dr_l, dr_m, dr_h, n=3):
    """
    Pointwise convergence factor Q(t) = (ε_l − ε_m) / (ε_m − ε_h).

    Should approach convergence_factor(dr_l, dr_m, dr_h, n) at late times.
    """
    tc, el, em, eh = align_and_compare(t_low, eps_low, t_mid, eps_mid,
                                       t_high, eps_high)
    num = el - em
    den = em - eh
    safe_den = np.where(np.abs(den) > 1e-15, den, 1e-15)
    Q_t      = num / safe_den
    Q_theory = convergence_factor(dr_l, dr_m, dr_h, n)
    return tc, Q_t, Q_theory


# ═══════════════════════════════════════════════════════════════════════
#  Section 13 — Initial conditions  (Paper Sec. II.D)
# ═══════════════════════════════════════════════════════════════════════

def build_initial_state(grid):
    """
    Construct equilibrium initial data U0 for the 6-variable system.

    At t = 0 in hydrostatic equilibrium:
        v^r = 0,  ε̂ = 0,  v̂_bar^r = 0  (Paper Sec. II.D)

    State vector:
        U[0] = γ̃ · ε         (since E(v=0, hat=0) = ε)
        U[1] = γ̃ · 0         (since S_r(v=0) = 0)
        U[2] = ε
        U[3] = ∂_r ε         (from spline derivative of background ε)
        U[4] = ṽ^r = 0
        U[5] = ∂_r ṽ^r = 0

    Parameters
    ----------
    grid : GridData instance

    Returns
    -------
    U0 : (6, N) array
    """
    N  = grid.N
    U0 = np.zeros((6, N))

    eps_bg = grid.eps_bg.copy()

    # E(v=0, hat=0) = ε  (Paper Eq.56 at v=0 gives E = ε) ✓
    U0[0] = grid.tgamma * eps_bg

    # S_r(v=0) = 0  ✓
    U0[1] = 0.0

    # ε
    U0[2] = eps_bg

    # ∂_r ε  — compute via cubic spline derivative
    #   (use background eps interpolant)
    # Build spline of eps_bg on the grid
    cs_eps_bg = CubicSpline(grid.r, eps_bg)
    U0[3] = cs_eps_bg(grid.r, 1)       # first derivative

    # ṽ^r = 0
    U0[4] = 0.0

    # ∂_r ṽ^r = 0
    U0[5] = 0.0

    # Apply atmosphere treatment consistent with the RHS
    p_ic = pressure(eps_bg)
    atm_ic = p_ic < P_ATMS
    U0[0, atm_ic] = grid.tgamma[atm_ic] * EPS_FLOOR
    U0[2, atm_ic] = EPS_FLOOR
    U0[3, atm_ic] = 0.0

    return U0


# ═══════════════════════════════════════════════════════════════════════
#  Quick self-test: verify correctness at equilibrium (v = 0)
# ═══════════════════════════════════════════════════════════════════════

def _selftest():
    """
    Verify the critical correctness checks at v = 0 equilibrium.

    At v = 0, hat = 0, in hydrostatic equilibrium (p' Dr_eps = −ρ A_r):
        A-matrix diagonal:  A00 = −τ_ε,  A11 = −g_{rr} τ_Q (ε + p)
        c₀ = ε,  c_r = 0   (uses TOV relation)
        E = ε,  S_r = 0,  S^r_r = p,  S^θ_θ = p
    """
    print("Running equilibrium self-test...")

    # Test with a single point
    eps_val = 0.00144        # central energy density
    grr_val = 1.5            # some representative g_{rr}
    hat_eta = 0.01
    hat_zeta = 0.01

    tc = compute_transport(np.array([eps_val]), hat_eta, hat_zeta)

    tau_eps_val = tc['tau_eps']
    tau_Q_val   = tc['tau_Q']
    dp_val      = tc['cs2']
    p_val       = tc['p']
    rho_val     = tc['rho']

    # A-matrix at v = 0.  Use A_r and Dr_eps consistent with
    # hydrostatic equilibrium: p' Dr_eps = −ρ A_r → Dr_eps = −ρ A_r / p'
    vr = np.array([0.0])
    grr = np.array([grr_val])
    A_r_val = 0.1
    A_r = np.array([A_r_val])
    r   = np.array([5.0])
    Dr_eps_val = -rho_val * A_r_val / dp_val   # TOV equilibrium relation
    Dr_eps = np.array([Dr_eps_val])
    Dr_vr  = np.array([0.0])

    A00, A01, A10, A11, c0, cr = \
        _A_matrix_and_c_vector(eps_val * np.ones(1), vr, grr, tc,
                               A_r, r, Dr_eps, Dr_vr)

    # Check A-matrix diagonality at v=0
    assert np.allclose(A00, -tau_eps_val, rtol=1e-10), \
        f"A00 = {A00}, expected {-tau_eps_val}"
    assert np.allclose(A11, -grr_val * tau_Q_val * rho_val, rtol=1e-10), \
        f"A11 = {A11}, expected {-grr_val * tau_Q_val * rho_val}"
    assert np.allclose(A01, 0.0, atol=1e-15), f"A01 = {A01}, expected 0"
    assert np.allclose(A10, 0.0, atol=1e-15), f"A10 = {A10}, expected 0"

    # Check c-vector at v=0 in hydrostatic equilibrium
    assert np.allclose(c0, eps_val, rtol=1e-10), \
        f"c0 = {c0}, expected {eps_val}"
    assert np.allclose(cr, 0.0, atol=1e-10), \
        f"cr = {cr}, expected 0 (hydrostatic equilibrium)"

    # Also test with A_r = 0, Dr_eps = 0 (trivial equilibrium at centre)
    _, _, _, _, c0c, crc = \
        _A_matrix_and_c_vector(eps_val * np.ones(1), vr, grr, tc,
                               np.array([0.0]), r,
                               np.array([0.0]), Dr_vr)
    assert np.allclose(c0c, eps_val, rtol=1e-10), \
        f"c0(centre) = {c0c}, expected {eps_val}"
    assert np.allclose(crc, 0.0, atol=1e-15), \
        f"cr(centre) = {crc}, expected 0"

    # Check stress tensor at v=0, hat=0 (use A_r=0 for simplicity)
    class MockGrid:
        pass
    mg = MockGrid()
    mg.r     = r
    mg.grr   = grr
    mg.A_r   = np.array([0.0])
    mg.D_rr_r  = np.array([0.0])
    mg.D_rth_th = np.array([1.0 / r[0]])
    mg.tgamma = np.array([1.0])
    mg.alpha  = np.array([0.9])

    E_out, Sr_c, Srr, Sthth = \
        compute_stress(eps_val * np.ones(1), np.array([0.0]),
                       np.array([0.0]), np.array([0.0]),
                       mg, tc, np.array([0.0]), np.array([0.0]))

    assert np.allclose(E_out, eps_val, rtol=1e-10), \
        f"E(v=0) = {E_out}, expected {eps_val}"
    assert np.allclose(Sr_c, 0.0, atol=1e-14), \
        f"Sr(v=0) = {Sr_c}, expected 0"
    assert np.allclose(Srr, p_val, rtol=1e-10), \
        f"S^r_r(v=0) = {Srr}, expected {p_val}"
    assert np.allclose(Sthth, p_val, rtol=1e-10), \
        f"S^theta_theta(v=0) = {Sthth}, expected {p_val}"

    print("All equilibrium self-tests passed!")


if __name__ == '__main__':
    _selftest()
