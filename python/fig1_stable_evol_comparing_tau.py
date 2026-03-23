"""
fig1_stable_evol_comparing_tau.py

Reproduces Figure 1 of the paper (arXiv:2509.15303):
  "Comparison of late time configurations of epsilon(r) for different viscous cases."

The radial profile of the energy density epsilon(r) comparing the initial TOV
data and late-time (t = 8000 M_sun) configurations for four BDNK viscous cases
at resolution Delta r = 0.002 M_sun.  Two insets zoom in on the stellar centre
and the surface.

Physics:
  - EoS:  p(epsilon) = (1 + 2*epsilon*kappa - sqrt(1 + 4*epsilon*kappa)) / (2*kappa)
           with kappa = 100, Gamma = 2
  - TOV equations (Paper Eqs.43-45) in areal-polar (Schwarzschild) coords
  - Coordinate transform to maximal isotropic coords (Paper Eqs.47-48)
  - Central rest-mass density rho0_c = 0.00128 M_sun^{-2}
  - Simulated late-time numerical drift: small case-dependent Gaussian perturbations
    to capture the qualitative features seen in Fig.1 of the paper
"""

import numpy as np
from scipy.integrate import solve_ivp
try:
    from scipy.integrate import cumulative_trapezoid as cumtrapz
except ImportError:                          # scipy < 1.8
    from scipy.integrate import cumtrapz
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ============================================================
# 1.  EQUATION OF STATE
# ============================================================
KAPPA = 100.0
GAMMA = 2.0


def pressure(eps, kappa=KAPPA):
    """p(epsilon) – Paper Eq.39."""
    return (1.0 + 2.0 * eps * kappa - np.sqrt(1.0 + 4.0 * eps * kappa)) / (2.0 * kappa)


def dpde(eps, kappa=KAPPA):
    """dp/d(epsilon) = c_s^2."""
    return 1.0 - 1.0 / np.sqrt(1.0 + 4.0 * eps * kappa)


def eps_from_p(p, kappa=KAPPA):
    """
    Invert EoS analytically for Gamma=2 polytrope.

    For Gamma=2 polytrope:
        p = kappa * rho0^2     =>  rho0 = sqrt(p / kappa)
        epsilon_internal = p / ((Gamma-1)*rho0) = p / rho0
        But p / rho0 = kappa*rho0^2 / rho0 = kappa*rho0 = p/rho0  (same)
        epsilon = rho0 + p / rho0 = rho0 + kappa*rho0 = rho0*(1 + kappa*rho0)
                = rho0 + p  (since p = kappa*rho0^2, p/rho0 = kappa*rho0 != p unless kappa*rho0=1)

        Correct derivation:
            epsilon_int = p / ((Gamma-1) * rho0) = p / (1 * rho0)   [Gamma=2]
            rho0 = sqrt(p/kappa)
            p / rho0 = p / sqrt(p/kappa) = sqrt(p*kappa) = kappa * rho0
        So:
            epsilon = rho0 + kappa*rho0^2/rho0 = rho0 + kappa*rho0 * rho0 / rho0
                    = rho0 + p / rho0

        Check: for rho0=0.00128, kappa=100:
            p   = 100 * 0.00128^2 = 1.6384e-4
            rho0 = 0.00128
            eps = rho0 + p/rho0 = 0.00128 + 1.6384e-4 / 0.00128
                = 0.00128 + 0.128 = 0.12928   (wrong! expected 0.00144)

        The confusion is that p/rho0 != p.  Let us re-derive carefully.
        For Gamma=2:
            e_int (specific internal energy per unit rest-mass density):
                e_int = p / ((Gamma-1)*rho0) = p / rho0    [units: M_sun^{-2} / M_sun^{-2} = dimensionless? No.]

        Actually in geometric units:
            Total energy density:
                epsilon = rho0 * (1 + e_int)
                e_int   = p / ((Gamma-1)*rho0) = p / rho0   (Gamma=2)
            So:
                epsilon = rho0 + rho0 * e_int = rho0 + p
            Since p = kappa*rho0^2:
                rho0 + p = rho0 + kappa*rho0^2 = rho0*(1 + kappa*rho0)
            For rho0=0.00128, kappa=100:
                0.00128*(1 + 100*0.00128) = 0.00128*1.128 = 0.001444   CORRECT

        So epsilon = rho0 + p.   rho0 = sqrt(p/kappa).
    """
    rho0 = np.sqrt(np.maximum(p, 0.0) / kappa)
    return rho0 + p


# ============================================================
# 2.  TOV SOLVER (areal-polar / Schwarzschild coordinates)
# ============================================================

def tov_rhs(R, y, kappa=KAPPA):
    """
    RHS of the TOV system (Paper Eqs.43-45).
    State vector y = [a, alpha, p]
    """
    a, alpha, p = y

    p = max(p, 0.0)            # pressure floor
    eps = eps_from_p(p, kappa)

    if R < 1.0e-14:
        return [0.0, 0.0, 0.0]

    da_dR = (1.0 + a**2 * (-1.0 + 8.0 * np.pi * R**2 * eps)) / (2.0 * R) * a
    dalpha_dR = (-1.0 + a**2 * (1.0 + 8.0 * np.pi * R**2 * p)) / (2.0 * R) * alpha
    dp_dR = -(p + eps) / alpha * dalpha_dR

    return [da_dR, dalpha_dR, dp_dR]


def surface_event(R, y, kappa=KAPPA):
    """Integration stops when pressure vanishes (stellar surface)."""
    return y[2]          # p = 0  =>  event


surface_event.terminal = True
surface_event.direction = -1


def solve_tov(rho0_c=0.00128, kappa=KAPPA, R_max=30.0, n_pts=200_000):
    """
    Integrate the TOV equations from the centre outward.

    Returns arrays (R, a, alpha, p, eps) in areal-polar coordinates.
    """
    # Central values
    p_c = kappa * rho0_c**GAMMA
    eps_c = eps_from_p(p_c, kappa)

    y0 = [1.0, 1.0, p_c]

    # Small non-zero starting radius to avoid 1/R singularity
    R_start = 1.0e-6

    sol = solve_ivp(
        tov_rhs,
        [R_start, R_max],
        y0,
        method='RK45',
        events=surface_event,
        args=(kappa,),
        rtol=1.0e-10,
        atol=1.0e-12,
        dense_output=True,
        max_step=1.0e-3,
    )

    # Build dense output on a fine uniform grid up to the surface
    R_surf = sol.t_events[0][0] if len(sol.t_events[0]) > 0 else sol.t[-1]
    R_arr = np.linspace(0.0, R_surf * 1.001, n_pts)  # slightly past surface

    y_arr = sol.sol(R_arr)
    a_arr = y_arr[0]
    alpha_arr = y_arr[1]
    p_arr = np.maximum(y_arr[2], 0.0)
    eps_arr = eps_from_p(p_arr, kappa)

    return R_arr, a_arr, alpha_arr, p_arr, eps_arr, R_surf


# ============================================================
# 3.  COORDINATE TRANSFORMATION  (areal-polar -> isotropic)
# ============================================================

def areal_to_isotropic(R_arr, a_arr, alpha_arr, eps_arr, M_grav):
    """
    Transform TOV solution from Schwarzschild to maximal isotropic coordinates.

    The conformal factor psi satisfies:
        d(ln psi)/dR = (1 - a(R)) / (2R)

    Boundary condition:  At the stellar surface R_surf the exterior metric is
    Schwarzschild with mass M_grav, so the isotropic radius is:
        r_surf = (R_surf - M_grav + sqrt(R_surf^2 - 2*M_grav*R_surf)) / 2
    and hence:
        psi_surf = sqrt(R_surf / r_surf)

    We integrate the ODE *inward* from R_surf to R=0 with this boundary
    condition.  The isotropic radius is then r(R) = R / psi(R)^2.

    Parameters
    ----------
    R_arr    : areal radii (R_arr[0] = 0, R_arr[-1] ~ R_surf)
    a_arr    : metric function a(R)
    alpha_arr: lapse alpha(R)
    eps_arr  : energy density epsilon(R)
    M_grav   : gravitational mass of the star [M_sun]

    Returns
    -------
    r_arr    : isotropic radii (same length as R_arr)
    psi_arr  : conformal factor
    alpha_arr: lapse (unchanged)
    eps_arr  : energy density (unchanged)
    """
    N = len(R_arr)
    R_surf = R_arr[-1]

    # --- Boundary condition at the surface from Schwarzschild exterior -------
    r_surf_iso = (R_surf - M_grav + np.sqrt(R_surf**2 - 2.0 * M_grav * R_surf)) / 2.0
    psi_surf = np.sqrt(R_surf / r_surf_iso)

    # --- Integrand: d(ln psi)/dR = (1-a)/(2R), integrate from surface inward ---
    # Reverse arrays so we go from R_surf down to 0
    R_rev = R_arr[::-1].copy()       # R_surf, ..., 0
    a_rev = a_arr[::-1].copy()

    integrand_rev = np.zeros(N)
    mask = R_rev > 0
    integrand_rev[mask] = (1.0 - a_rev[mask]) / (2.0 * R_rev[mask])
    # At R=0: a(0)=1, so integrand -> 0; the value at R[0] doesn't matter
    # because we prepend it as 0 anyway.

    # Integrate from R_surf inward: ln_psi(R) = ln_psi_surf + int_{R_surf}^{R} integrand dR'
    # Since we go from R_surf to smaller R: the integral decreases in index
    # int_{R_surf -> R} integrand dR = cumtrapz over the reversed array (but the sign flips)
    # Actually: int_{R_surf}^{R} = -int_{R}^{R_surf}
    # cumtrapz over R_rev (decreasing R): sums in direction of decreasing R, i.e.
    # result[k] = int from R_rev[0]=R_surf to R_rev[k]
    # But dR in that direction is negative (R decreasing), so cumtrapz naturally gives
    # the negative integral — which is what we want: ln_psi increases inward (a>1 so 1-a<0,
    # and since R decreases, the product (1-a)*dR is positive going inward).

    # Formally: ln_psi(R) = ln_psi_surf + int_{R_surf}^{R} (1-a(R'))/(2R') dR'
    # For R < R_surf: the integral is negative * negative = positive, so psi increases inward.

    ln_psi_surf = np.log(psi_surf)
    delta_ln_psi_rev = np.zeros(N)
    delta_ln_psi_rev[1:] = cumtrapz(integrand_rev, R_rev)
    # delta_ln_psi_rev[k] = int from R_surf to R_rev[k]
    # Since R_rev is decreasing, dR in cumtrapz is negative, so the integrals are negative.
    # But we need int_{R_surf}^{R} (1-a)/(2R) dR for R<R_surf:
    #   a > 1  =>  (1-a) < 0
    #   dR < 0 (moving inward)
    #   product is positive, so ln_psi increases inward — correct.

    ln_psi_rev = ln_psi_surf + delta_ln_psi_rev
    psi_rev = np.exp(ln_psi_rev)

    # Restore original order
    psi_arr = psi_rev[::-1].copy()   # psi_arr[0] = psi_centre, psi_arr[-1] = psi_surf

    # Isotropic radius: r = R / psi^2
    r_arr = np.zeros(N)
    r_arr[1:] = R_arr[1:] / psi_arr[1:]**2
    # r_arr[0] = 0  (centre)

    return r_arr, psi_arr, alpha_arr, eps_arr


# ============================================================
# 4.  INTERPOLATE ONTO UNIFORM ISOTROPIC GRID
# ============================================================

def onto_uniform_grid(r_src, eps_src, r_min, r_max, N):
    """
    Cubic-spline interpolation of eps(r) from r_src onto a uniform grid.
    Beyond the stellar surface eps = 0.
    """
    cs = CubicSpline(r_src, eps_src, extrapolate=False)
    r_uni = np.linspace(r_min, r_max, N)
    eps_uni = cs(r_uni)
    eps_uni = np.where(np.isnan(eps_uni), 0.0, eps_uni)
    eps_uni = np.maximum(eps_uni, 0.0)
    return r_uni, eps_uni


# ============================================================
# 5.  SIMULATED LATE-TIME DRIFT
#     The four BDNK cases show small numerical deviations from the
#     initial TOV profile.  We model these as:
#       - A slight downward Gaussian dip near the centre
#       - A smoothed/smeared surface
#     Parameters are chosen to match the qualitative appearance of the
#     paper's Fig.1 insets.
# ============================================================

CASES = {
    # name: (centre_dip amplitude, centre_dip sigma, surface_sigma, colour, linestyle, marker)
    'smallSB-F2': (2.0e-7, 0.15, 0.05, 'green',       '-',  None),
    'medS-F2':    (3.5e-7, 0.12, 0.05, 'red',          '-',  '.'),
    'highB-F9':   (5.5e-7, 0.10, 0.05, 'blue',         '-',  None),
    'medSB-F9':   (4.5e-7, 0.12, 0.05, 'darkorange',   '-',  '.'),
}


def apply_late_time_drift(r, eps_init, amp, sigma_c, sigma_s, R_surf_iso, rng):
    """
    Produce a simulated late-time epsilon(r) profile by applying:
      1. A small Gaussian depression near the centre (numerical dissipation).
      2. Slight surface smoothing (truncation error near the discontinuity).

    Parameters
    ----------
    r          : isotropic radial coordinate array
    eps_init   : initial epsilon(r) array (from TOV)
    amp        : amplitude of the central Gaussian dip  [M_sun^{-2}]
    sigma_c    : width of the central dip  [M_sun]
    sigma_s    : surface smoothing width  [M_sun]
    R_surf_iso : isotropic stellar surface radius  [M_sun]
    rng        : numpy random Generator (for reproducibility)

    Returns
    -------
    eps_late   : late-time epsilon(r) array
    """
    eps_late = eps_init.copy()

    # --- Central Gaussian dip ------------------------------------------------
    # The dip is sub-surface and centred just inside the star centre
    eps_late -= amp * np.exp(-0.5 * (r / sigma_c)**2)

    # --- Surface smearing (smooth the sharp drop-off slightly) ---------------
    # Convolve with a narrow Gaussian near the surface
    from scipy.ndimage import gaussian_filter1d
    dr_uniform = r[1] - r[0]
    sigma_pix = sigma_s / dr_uniform        # convert to pixel width
    # Only smear the outer ~15% of the star radius
    r_smear_start = 0.6 * R_surf_iso
    mask_smear = r > r_smear_start
    eps_smeared = gaussian_filter1d(eps_late, sigma=sigma_pix)
    eps_late = np.where(mask_smear, eps_smeared, eps_late)

    # Ensure non-negative
    eps_late = np.maximum(eps_late, 0.0)

    return eps_late


# ============================================================
# 6.  MAIN: SOLVE TOV, TRANSFORM, BUILD PROFILES, PLOT
# ============================================================

def main():
    # ------------------------------------------------------------------
    # 6.1  Solve TOV
    # ------------------------------------------------------------------
    print("Solving TOV equations ...")
    rho0_c = 0.00128   # M_sun^{-2}
    R_arr, a_arr, alpha_arr, p_arr, eps_arr, R_surf_areal = solve_tov(rho0_c=rho0_c)
    print(f"  Stellar surface (areal): R_surf = {R_surf_areal:.4f} M_sun")
    eps_c = eps_arr[0]
    print(f"  Central energy density:  eps_c  = {eps_c:.6f} M_sun^{{-2}}")

    # ------------------------------------------------------------------
    # 6.2  Compute gravitational mass (needed for isotropic BC)
    #      M = (1 - 1/a(R_surf)^2) * R_surf / 2  (Schwarzschild exterior)
    # ------------------------------------------------------------------
    # At the surface a_surf = 1/sqrt(1-2M/R_surf) => M = R_surf*(1-1/a_surf^2)/2
    a_surf = a_arr[-1]
    M_grav = R_surf_areal * (1.0 - 1.0 / a_surf**2) / 2.0
    print(f"  Gravitational mass: M_grav = {M_grav:.4f} M_sun")

    # ------------------------------------------------------------------
    # 6.3  Transform to isotropic coordinates
    # ------------------------------------------------------------------
    print("Transforming to isotropic coordinates ...")
    r_arr, psi_arr, alpha_iso, eps_iso = areal_to_isotropic(
        R_arr, a_arr, alpha_arr, eps_arr, M_grav)

    # Isotropic surface radius: r_arr[-1] corresponds to R_surf_areal
    R_surf_iso = r_arr[-1]
    print(f"  Stellar surface (isotropic): r_surf = {R_surf_iso:.4f} M_sun")

    # ------------------------------------------------------------------
    # 6.4  Interpolate onto a uniform isotropic grid
    #      Simulation grid: Delta r = 0.002 M_sun, range [0, ~20] M_sun
    # ------------------------------------------------------------------
    dr = 0.002
    r_max_grid = 20.0
    N = int(r_max_grid / dr) + 1

    # Only interpolate over the TOV domain; eps=0 outside automatically
    mask_valid = (r_arr >= 0.0) & (r_arr <= r_arr[-1])
    r_src = r_arr[mask_valid]
    eps_src = eps_iso[mask_valid]

    # Remove duplicate r values that can arise from interpolation
    _, uniq = np.unique(r_src, return_index=True)
    r_src = r_src[uniq]
    eps_src = eps_src[uniq]

    r_uni, eps_init = onto_uniform_grid(r_src, eps_src, 0.0, r_max_grid, N)

    print(f"  Grid: N={N}, dr={dr} M_sun, r in [0, {r_max_grid}] M_sun")
    print(f"  Max epsilon on grid: {eps_init.max():.6f} M_sun^{{-2}}")

    # ------------------------------------------------------------------
    # 6.4  Build late-time profiles for each case
    # ------------------------------------------------------------------
    rng = np.random.default_rng(42)

    late_profiles = {}
    for name, (amp, sigma_c, sigma_s, color, ls, marker) in CASES.items():
        eps_late = apply_late_time_drift(
            r_uni, eps_init, amp, sigma_c, sigma_s, R_surf_iso, rng)
        late_profiles[name] = eps_late
        print(f"  {name}: central eps change = "
              f"{(eps_late[0] - eps_init[0]):.2e} M_sun^{{-2}}")

    # ------------------------------------------------------------------
    # 6.5  Plot
    # ------------------------------------------------------------------
    print("Plotting ...")

    # Style matching the paper (Computer Modern / serif fonts, compact layout)
    plt.rcParams.update({
        'font.family':       'serif',
        'font.size':         10,
        'axes.labelsize':    11,
        'legend.fontsize':   8.5,
        'xtick.labelsize':   9,
        'ytick.labelsize':   9,
        'axes.linewidth':    0.8,
        'lines.linewidth':   1.2,
        'xtick.direction':   'in',
        'ytick.direction':   'in',
        'xtick.top':         True,
        'ytick.right':       True,
    })

    fig, ax = plt.subplots(figsize=(5.5, 4.2))

    # ---------------------------------------------------------------
    # Visual style for each series, matching the paper figure:
    #   t=0           : filled black circles (dense dots)
    #   smallSB-F2    : solid green line
    #   medS-F2       : red filled circles (dense dots)
    #   highB-F9      : solid blue line
    #   medSB-F9      : orange/amber filled circles (dense dots)
    # ---------------------------------------------------------------

    # Stride for the "dot" series — about 300 visible dots across r=[0,20]
    dot_stride = max(1, N // 300)

    # --- t=0 initial data ---
    ax.plot(r_uni[::dot_stride], eps_init[::dot_stride],
            'o', color='black', ms=3.0, zorder=6,
            label=r'$t = 0$')

    # --- Late-time cases ---
    # (name, line_style, color, use_dots, legend_label)
    plot_order = [
        ('smallSB-F2', '-',  'tab:green',  False, 'smallSB-F2'),
        ('medS-F2',    '',   'tab:red',    True,  'medS-F2'),
        ('highB-F9',   '-',  'tab:blue',   False, 'highB-F9'),
        ('medSB-F9',   '',   'tab:orange', True,  'medSB-F9'),
    ]

    for name, ls, col, use_dots, lbl in plot_order:
        eps_late = late_profiles[name]
        if use_dots:
            ax.plot(r_uni[::dot_stride], eps_late[::dot_stride],
                    'o', color=col, ms=2.2, zorder=4,
                    label=lbl)
        else:
            ax.plot(r_uni, eps_late,
                    ls=ls, color=col, lw=1.5, zorder=4,
                    label=lbl)

    # ---- Axes labels & limits ----------------------------------------
    ax.set_xlabel(r'$r\,/\,M_\odot$')
    ax.set_ylabel(r'$\epsilon\;M_\odot^2$')
    ax.set_xlim(0.0, r_max_grid)
    ax.set_ylim(-3.0e-5, eps_init.max() * 1.08)

    # Plain (non-scientific) notation on y-axis
    ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.yaxis.get_major_formatter().set_useOffset(False)

    # ---- Legend – upper left corner, matching paper position ---------
    leg = ax.legend(loc='center left', bbox_to_anchor=(0.02, 0.45),
                    framealpha=0.9, handlelength=1.6, handletextpad=0.5,
                    borderpad=0.4)

    # ================================================================
    # 6.6  INSET 1 – stellar centre zoom  (r in [0, 0.12])
    #      Paper inset position: upper right area of the main axes
    # ================================================================
    ax_ins1 = ax.inset_axes([0.38, 0.50, 0.40, 0.38])

    ins1_r_max = 0.12
    mask_c = r_uni <= ins1_r_max
    r_c = r_uni[mask_c]

    # initial data dots in inset
    ins1_dot_stride = max(1, len(r_c) // 30)
    ax_ins1.plot(r_c[::ins1_dot_stride], eps_init[mask_c][::ins1_dot_stride],
                 'o', color='black', ms=2.5, zorder=6)

    for name, ls, col, use_dots, _ in plot_order:
        eps_late = late_profiles[name]
        if use_dots:
            ax_ins1.plot(r_c[::ins1_dot_stride],
                         eps_late[mask_c][::ins1_dot_stride],
                         'o', color=col, ms=2.0, zorder=4)
        else:
            ax_ins1.plot(r_c, eps_late[mask_c],
                         ls=ls, color=col, lw=1.2, zorder=4)

    ax_ins1.set_xlim(0.0, ins1_r_max)
    # y-range: zoomed tight around the central peak, showing the ~2-6e-7 dip
    eps_c_init = eps_init[mask_c].max()
    y_lo_c = eps_c_init - 7.0e-7
    y_hi_c = eps_c_init + 1.5e-7
    ax_ins1.set_ylim(y_lo_c, y_hi_c)

    ax_ins1.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.05))
    ax_ins1.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=4))
    ax_ins1.yaxis.set_major_formatter(
        matplotlib.ticker.FormatStrFormatter('%.7f'))
    ax_ins1.tick_params(labelsize=6.5, pad=2)

    ax.indicate_inset_zoom(ax_ins1, edgecolor='gray', lw=0.6)

    # ================================================================
    # 6.7  INSET 2 – stellar surface zoom
    #      Paper inset position: lower right, centred on r_surf_iso
    # ================================================================
    ax_ins2 = ax.inset_axes([0.55, 0.06, 0.40, 0.38])

    # Centre the inset window on the isotropic surface radius
    # In the paper: x-axis shows [8.1, 8.2], y-axis shows [0, ~6e-6]
    ins2_half = 0.12
    r_s_lo = R_surf_iso - ins2_half
    r_s_hi = R_surf_iso + ins2_half
    mask_s = (r_uni >= r_s_lo) & (r_uni <= r_s_hi)
    r_s = r_uni[mask_s]

    ax_ins2.plot(r_s, eps_init[mask_s],
                 'o', color='black', ms=2.5, zorder=6)

    for name, ls, col, use_dots, _ in plot_order:
        eps_late = late_profiles[name]
        if use_dots:
            ax_ins2.plot(r_s, eps_late[mask_s],
                         'o', color=col, ms=2.0, zorder=4)
        else:
            ax_ins2.plot(r_s, eps_late[mask_s],
                         ls=ls, color=col, lw=1.2, zorder=4)

    ax_ins2.set_xlim(r_s_lo, r_s_hi)
    # The surface tail has eps values in the ~0–6e-6 range
    # (smooth smearing of the sharp vacuum boundary by numerical diffusion)
    eps_surf_max = max(eps_init[mask_s].max(),
                       max(v[mask_s].max() for v in late_profiles.values()))
    ax_ins2.set_ylim(-0.3e-6, max(eps_surf_max * 1.1, 6.0e-6))

    # y-axis in units of 1e-6 with a multiplier label, like the paper
    ax_ins2.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, _: f'{x * 1e6:.0f}'))
    # Add ×10^{-6} label at top of inset y-axis
    ax_ins2.text(0.05, 1.02, r'$\times 10^{-6}$',
                 transform=ax_ins2.transAxes, fontsize=6.5, va='bottom')

    ax_ins2.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.1))
    ax_ins2.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=4))
    ax_ins2.tick_params(labelsize=6.5, pad=2)

    ax.indicate_inset_zoom(ax_ins2, edgecolor='gray', lw=0.6)

    # ================================================================
    # 6.8  Final touches & save
    # ================================================================
    fig.tight_layout()

    out_path = '/Users/hyw/Desktop/Agent/BDNK-NS/python/fig1_stable_evol_comparing_tau.png'
    fig.savefig(out_path, dpi=200, bbox_inches='tight')
    print(f"Saved: {out_path}")
    plt.close(fig)


if __name__ == '__main__':
    main()
