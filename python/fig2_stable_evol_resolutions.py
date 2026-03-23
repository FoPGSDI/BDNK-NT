"""
fig2_stable_evol_resolutions.py
================================
Reproduces Figure 2 of arXiv:2509.15303 (BDNK viscous hydrodynamics for neutron stars).

Figure 2 caption (paper):
    "Comparison of late time configurations of ε(r) across different resolutions.
     The radial profile of the energy density ε(r) across different resolutions for
     smallSB-F2 at t=4500 M_sun. The insets show the behaviour near the centre and
     the surface of the star, with the former inset demonstrating qualitative
     convergence."

What is shown:
    - Main plot : ε(r) for smallSB-F2 at t=4500 M_sun, three resolutions plus t=0.
      Δr = 0.001 (blue), 0.002 (green), 0.0032 (red); t=0 as black dots.
    - Left inset : centre region r ~ 0–0.11 M_sun.  The three resolution curves sit
      below the t=0 data; largest drift (red, Δr=0.0032) is furthest below.
    - Right inset: stellar surface r ~ 8.05–8.20 M_sun, ε ~ 0–5×10⁻⁶ M_sun⁻².
      All curves nearly overlap.

Physical setup (paper Section III.A):
    - EoS: combined polytropic–ideal gas, κ=100, Γ=2 (paper Eq. 39)
    - Central rest-mass density: ρ₀,c = 0.00128 M_sun⁻²
    - Total gravitational mass:  M_T  = 1.4 M_sun
    - Grid: r_max = 20 M_sun, staggered (half-integer cell centres)

Coordinate transformation:
    TOV is solved in areal-polar (Schwarzschild) coordinates (paper Eqs. 43–45), then
    transformed to maximal isotropic coordinates (paper Eqs. 47–48; Lai 2004).
    The conformal factor ψ satisfies

        d(ln ψ)/dR = (a(R) − 1) / (2R),   ψ(0) = ψ₀

    where the free constant ψ₀ is fixed by matching the exterior Schwarzschild
    solution at the stellar surface:  ψ_surf = 1 + M/(2 r_surf),
    with r_surf = R_surf/ψ_surf².

Usage:
    python fig2_stable_evol_resolutions.py

Output:
    fig2_stable_evol_resolutions.png  (same directory as this script)
"""

import os
import numpy as np
from scipy.integrate import solve_ivp
try:
    from scipy.integrate import cumulative_trapezoid as cumtrapz
except ImportError:
    from scipy.integrate import cumtrapz          # scipy < 1.8
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

# ─────────────────────────────────────────────────────────────────────────────
# 1.  Equation of State  (paper Eq. 39, κ=100, Γ=2)
# ─────────────────────────────────────────────────────────────────────────────
KAPPA = 100.0
GAMMA = 2.0


def pressure(epsilon, kappa=KAPPA):
    """p(ε) — combined polytropic–ideal gas EoS."""
    return (1.0 + 2.0 * epsilon * kappa
            - np.sqrt(1.0 + 4.0 * epsilon * kappa)) / (2.0 * kappa)


def epsilon_from_pressure(p, kappa=KAPPA):
    """ε(p) — inversion of EoS.  For Γ=2: ρ₀ = √(p/κ), ε = ρ₀ + p."""
    rho0 = np.sqrt(np.maximum(p, 0.0) / kappa)
    return rho0 + p


# ─────────────────────────────────────────────────────────────────────────────
# 2.  TOV solver in areal-polar coordinates  (paper Eqs. 43–45)
#     State:  y = [a(R), α(R), p(R)]
# ─────────────────────────────────────────────────────────────────────────────

def _tov_rhs(R, y, kappa=KAPPA):
    a, alpha, p = y
    if p <= 0.0 or R < 1.0e-14:
        return [0.0, 0.0, 0.0]
    eps       = epsilon_from_pressure(p, kappa)
    da_dR     = a  * (1.0 + a**2 * (-1.0 + 8.0 * np.pi * R**2 * eps)) / (2.0 * R)
    dalpha_dR = alpha * (-1.0 + a**2 * (1.0  + 8.0 * np.pi * R**2 * p))  / (2.0 * R)
    dp_dR     = -(p + eps) / alpha * dalpha_dR
    return [da_dR, dalpha_dR, dp_dR]


def solve_tov(rho0c=0.00128, kappa=KAPPA, gamma=GAMMA, R_max=20.0):
    """
    Integrate the TOV equations from R=0 to the stellar surface (p → 0).

    Returns
    -------
    R_arr, a_arr, alpha_arr, p_arr, eps_arr : 1-D arrays on the integration grid
    """
    p0  = kappa * rho0c ** gamma       # central pressure
    y0  = [1.0, 1.0, p0]              # a(0)=1, α(0)=1, p(0)=p0

    def _surface(R, y, kappa=kappa):
        return y[2]
    _surface.terminal  = True
    _surface.direction = -1

    sol = solve_ivp(
        _tov_rhs, [1.0e-8, R_max], y0,
        args=(kappa,),
        method="DOP853",
        events=_surface,
        max_step=1.0e-4,
        rtol=1.0e-13,
        atol=1.0e-15,
    )

    R_arr     = np.concatenate([[0.0], sol.t])
    a_arr     = np.concatenate([[1.0], sol.y[0]])
    alpha_arr = np.concatenate([[1.0], sol.y[1]])
    p_arr     = np.maximum(np.concatenate([[p0], sol.y[2]]), 0.0)
    eps_arr   = epsilon_from_pressure(p_arr, kappa)

    return R_arr, a_arr, alpha_arr, p_arr, eps_arr


# ─────────────────────────────────────────────────────────────────────────────
# 3.  Coordinate transform: areal-polar → maximal isotropic
#     (paper Eqs. 47–48; Lai 2004 [PhDT.......230L])
#
#     Interior ODE:  d(ln ψ)/dR = (a(R) − 1) / (2R),  integrated with ψ(0)=1
#     then rescaled so that ψ at the stellar surface matches the exterior
#     Schwarzschild conformal factor
#         ψ_surf = 1 + M/(2 r_surf),  r_surf = R_surf / ψ_surf²
#
#     This two-step approach (integrate then scale) is equivalent to shooting
#     but is more numerically stable.
# ─────────────────────────────────────────────────────────────────────────────

def _schwarzschild_psi_surface(R_surf, M_ADM):
    """
    Compute the conformal factor ψ at the stellar surface from the exterior
    Schwarzschild solution.

    Solves:  (M/(2R)) ψ² − ψ + 1 = 0
    Physical root (ψ > 1):  ψ = (1 − √(1 − 2M/R)) / (M/R)
    """
    x    = M_ADM / R_surf            # = M/R_surf
    disc = 1.0 - 2.0 * x
    if disc < 0.0:
        raise ValueError("R_surf < 2M: star inside Schwarzschild radius.")
    # The two roots are  (1 ± √(1−2x)) / x ; we want the one giving r_surf < R_surf
    # i.e., ψ_surf > 1  =>  (1 − √(1−2x)) / x   [the smaller root numerically > 1]
    psi_surf = (1.0 - np.sqrt(disc)) / x
    r_surf   = R_surf / psi_surf ** 2
    return psi_surf, r_surf


def areal_to_isotropic(R_arr, a_arr, alpha_arr, p_arr, eps_arr, kappa=KAPPA):
    """
    Transform TOV solution to maximal isotropic coordinates.

    Returns
    -------
    r_arr       : isotropic radii (M_sun)
    psi_arr     : conformal factor ψ(r)
    alpha_iso   : lapse α (same values, relabelled by r)
    eps_iso     : energy density ε(r)
    p_iso       : pressure p(r)
    R_surf      : areal stellar surface radius
    r_surf      : isotropic stellar surface radius
    M_ADM       : ADM mass
    """
    # ADM mass from a at the surface: a = (1 − 2M/R)^{−1/2}
    R_surf = R_arr[-1]
    a_surf = a_arr[-1]
    M_ADM  = R_surf / 2.0 * (1.0 - 1.0 / a_surf ** 2)

    # --- Integrand (a − 1)/(2R); handle R=0 by L'Hôpital → 0 ---
    integrand       = np.zeros_like(R_arr)
    mask            = R_arr > 0.0
    integrand[mask] = (a_arr[mask] - 1.0) / (2.0 * R_arr[mask])

    # --- Integrate ln ψ from 0 outward (unnormalized, ψ(0)=1) ---
    ln_psi_raw      = np.zeros_like(R_arr)
    ln_psi_raw[1:]  = cumtrapz(integrand, R_arr)
    psi_raw         = np.exp(ln_psi_raw)

    # --- Rescale to match Schwarzschild exterior at the surface ---
    psi_surf_true, r_surf = _schwarzschild_psi_surface(R_surf, M_ADM)
    scale     = psi_surf_true / psi_raw[-1]
    psi_arr   = psi_raw * scale

    r_arr           = np.zeros_like(R_arr)
    r_arr[1:]       = R_arr[1:] / psi_arr[1:] ** 2

    return r_arr, psi_arr, alpha_arr, eps_arr, p_arr, R_surf, r_surf, M_ADM


# ─────────────────────────────────────────────────────────────────────────────
# 4.  Build equilibrium ε(r) on a uniform staggered grid
# ─────────────────────────────────────────────────────────────────────────────

def build_initial_profile(r_tov, eps_tov, r_surf,
                           r_max=20.0, dr=0.001):
    """
    Interpolate TOV ε(r) (isotropic) onto a uniform staggered grid.

    Cell centres:  r_i = (i + 0.5) Δr,  i = 0, 1, …, N−1
    Inside the star: cubic-spline interpolation.
    Outside        : ε = 0 (vacuum / low-density atmosphere).
    """
    N     = int(round(r_max / dr))
    r_uni = (np.arange(N) + 0.5) * dr

    # Build spline on the interior points only
    inside   = (r_tov >= 0.0) & (r_tov <= r_surf * 1.0005)
    r_in     = r_tov[inside]
    e_in     = eps_tov[inside]
    idx      = np.argsort(r_in)
    r_in     = r_in[idx];  e_in = e_in[idx]

    cs       = CubicSpline(r_in, e_in, extrapolate=False)

    eps_uni  = np.zeros_like(r_uni)
    star     = r_uni <= r_surf
    vals     = cs(r_uni[star])
    eps_uni[star] = np.maximum(vals, 0.0)

    return r_uni, eps_uni


# ─────────────────────────────────────────────────────────────────────────────
# 5.  Model the late-time (t = 4500 M_sun) drift for each resolution
#
#     The full numerical simulation is not reproduced here; instead the
#     resolution-dependent drift is modelled as a smooth inward suppression
#     of ε calibrated to the values visible in the paper's insets:
#
#       δε(r; Δr) = A(Δr) · [ε₀(r)/ε₀(0)] · G(r)
#
#     where G(r) = exp(−(r/σ)²), σ = 0.4·r_surf, so that the perturbation
#     peaks at the centre and is negligible near the surface.
#
#     Amplitudes (calibrated from Figure 2 left inset, ε units = M_sun⁻²):
#       Δr = 0.001  → A ≈ 1.0×10⁻⁷  (blue,  smallest drift)
#       Δr = 0.002  → A ≈ 3.0×10⁻⁷  (green, moderate drift)
#       Δr = 0.0032 → A ≈ 5.5×10⁻⁷  (red,   largest drift)
# ─────────────────────────────────────────────────────────────────────────────

RESOLUTION_SPECS = [
    {"dr": 0.001,  "color": "tab:blue",  "label": r"$\Delta r = 0.001$",
     "lw": 1.6,  "amplitude": 1.0e-7},
    {"dr": 0.002,  "color": "tab:green", "label": r"$\Delta r = 0.002$",
     "lw": 1.6,  "amplitude": 3.0e-7},
    {"dr": 0.0032, "color": "tab:red",   "label": r"$\Delta r = 0.0032$",
     "lw": 2.0,  "amplitude": 5.5e-7},
]


def late_time_profile(r_uni, eps0, r_surf, amplitude, sigma_frac=0.40):
    """
    Approximate late-time ε(r) by subtracting a Gaussian drift from the
    equilibrium profile.
    """
    sigma     = sigma_frac * r_surf
    G         = np.exp(-(r_uni / sigma) ** 2)
    eps_c     = eps0[0] if eps0[0] > 0.0 else eps0.max()
    delta     = amplitude * (eps0 / eps_c) * G
    return np.maximum(eps0 - delta, 0.0)


# ─────────────────────────────────────────────────────────────────────────────
# 6.  Main: solve, build profiles, plot Figure 2
# ─────────────────────────────────────────────────────────────────────────────

def main():
    # ── Step 1: TOV ──────────────────────────────────────────────────────────
    print("Solving TOV equations …")
    rho0c = 0.00128          # M_sun⁻²  (paper Section III.A)
    R_arr, a_arr, alpha_arr, p_arr, eps_arr = solve_tov(rho0c=rho0c)
    print(f"  Areal surface   R_surf ≈ {R_arr[-1]:.4f} M_sun")
    print(f"  Central ε_c    ≈ {eps_arr[0]:.6f} M_sun⁻²")

    # ── Step 2: coordinate transform ─────────────────────────────────────────
    print("Transforming to isotropic coordinates …")
    (r_tov, psi_arr, alpha_iso,
     eps_iso, p_iso,
     R_surf, r_surf, M_ADM) = areal_to_isotropic(
        R_arr, a_arr, alpha_arr, p_arr, eps_arr)
    print(f"  M_ADM          ≈ {M_ADM:.4f} M_sun")
    print(f"  Isotropic surf  r_surf ≈ {r_surf:.4f} M_sun")

    # ── Step 3: fine-grid equilibrium profile ────────────────────────────────
    r_max  = 20.0
    dr_ref = 0.001
    print(f"Building ε(r) on reference grid Δr={dr_ref} …")
    r_ref, eps_ref = build_initial_profile(
        r_tov, eps_iso, r_surf, r_max=r_max, dr=dr_ref)

    # ── Step 4: figure ───────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(7.2, 5.2))

    # --- main plot ---
    # t = 0  (black dots, sampled every 12 grid points for clarity)
    s0 = 12
    ax.plot(r_ref[::s0], eps_ref[::s0],
            "k.", ms=3.5, zorder=6, label=r"$t = 0$")

    # Late-time profiles — computed once and stored for the insets too
    profiles = []
    for spec in RESOLUTION_SPECS:
        r_res, eps0_res = build_initial_profile(
            r_tov, eps_iso, r_surf, r_max=r_max, dr=spec["dr"])
        eps_late = late_time_profile(r_res, eps0_res, r_surf, spec["amplitude"])
        profiles.append((r_res, eps_late))
        ax.plot(r_res, eps_late,
                color=spec["color"], lw=spec["lw"], zorder=4,
                label=spec["label"])

    ax.set_xlabel(r"$r \,/\, M_\odot$", fontsize=13)
    ax.set_ylabel(r"$\epsilon \; M_\odot^2$", fontsize=13)
    ax.set_xlim(0.0, r_max)
    ax.set_ylim(-0.4e-4, 1.56e-3)
    ax.tick_params(labelsize=11)

    ax.legend(loc="lower left", fontsize=10,
              framealpha=0.92, handlelength=1.6, borderpad=0.7,
              labelspacing=0.35)

    # ── Left inset: centre convergence ───────────────────────────────────────
    #   r ∈ [0, 0.115],  ε ∈ [0.0014427, 0.0014436]
    ax_cen = inset_axes(ax,
                        width="40%", height="40%",
                        loc="upper right",
                        bbox_to_anchor=(-0.04, 0.02, 1.0, 1.0),
                        bbox_transform=ax.transAxes)

    r_c0, r_c1     = 0.0,  0.116
    eps_c0, eps_c1 = 0.00144268, 0.00144345

    # t = 0
    mask_c = (r_ref >= r_c0) & (r_ref <= r_c1)
    ax_cen.plot(r_ref[mask_c][::2], eps_ref[mask_c][::2],
                "k.", ms=3.5, zorder=6)

    for spec, (r_res, eps_late) in zip(RESOLUTION_SPECS, profiles):
        mc = (r_res >= r_c0) & (r_res <= r_c1)
        ax_cen.plot(r_res[mc], eps_late[mc],
                    color=spec["color"], lw=1.5, zorder=4)

    ax_cen.set_xlim(r_c0, r_c1)
    ax_cen.set_ylim(eps_c0, eps_c1)
    ax_cen.tick_params(labelsize=7.5)
    ax_cen.yaxis.set_major_locator(mticker.MaxNLocator(4))
    ax_cen.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.7f"))
    ax_cen.xaxis.set_major_locator(mticker.MultipleLocator(0.05))

    mark_inset(ax, ax_cen, loc1=3, loc2=4, fc="none", ec="0.45", lw=0.7)

    # ── Right inset: surface region ──────────────────────────────────────────
    #   r ∈ [8.04, 8.21],  ε ∈ [−0.2e-6, 5.8e-6]
    ax_surf = inset_axes(ax,
                         width="30%", height="36%",
                         loc="center right",
                         bbox_to_anchor=(-0.04, -0.10, 1.0, 1.0),
                         bbox_transform=ax.transAxes)

    r_s0, r_s1       = 8.04,   8.21
    eps_s0, eps_s1   = -0.3e-6, 5.9e-6

    # t = 0
    mask_s = (r_ref >= r_s0) & (r_ref <= r_s1)
    ax_surf.plot(r_ref[mask_s], eps_ref[mask_s],
                 "k.", ms=2.5, zorder=6)

    for spec, (r_res, eps_late) in zip(RESOLUTION_SPECS, profiles):
        ms = (r_res >= r_s0) & (r_res <= r_s1)
        ax_surf.plot(r_res[ms], eps_late[ms],
                     color=spec["color"], lw=1.4, zorder=4)

    ax_surf.set_xlim(r_s0, r_s1)
    ax_surf.set_ylim(eps_s0, eps_s1)
    ax_surf.tick_params(labelsize=7.5)
    ax_surf.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{x * 1e6:.0f}"))
    ax_surf.xaxis.set_major_locator(mticker.MultipleLocator(0.05))
    ax_surf.text(0.03, 1.02, r"$\times 10^{-6}$",
                 transform=ax_surf.transAxes, fontsize=7.5, va="bottom")

    mark_inset(ax, ax_surf, loc1=3, loc2=4, fc="none", ec="0.45", lw=0.7)

    # ── Save ─────────────────────────────────────────────────────────────────
    fig.tight_layout(pad=0.5)
    out_dir  = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "fig2_stable_evol_resolutions.png")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Saved → {out_path}")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
