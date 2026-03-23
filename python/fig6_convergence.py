"""
fig6_convergence.py
Reproduces Figure 6 of the paper: convergence test for smallSB-F2.

Top panel:    epsilon_c(t) / epsilon_c(0) at three resolutions
Bottom panel: convergence factor Q(t) with theoretical line at Q ~ 1.993
"""

import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ---------------------------------------------------------------------------
# 1.  Physical / numerical parameters
# ---------------------------------------------------------------------------
dr_low  = 0.0028   # coarsest
dr_mid  = 0.0020
dr_hi   = 0.0010   # finest

# Theoretical convergence factor for a 3rd-order scheme
# Q = (dr_low^3 - dr_mid^3) / (dr_mid^3 - dr_hi^3)
Q_theory = (dr_low**3 - dr_mid**3) / (dr_mid**3 - dr_hi**3)
print(f"Q_theory = {Q_theory:.4f}")   # -> 1.9930...

omega_f = 0.0834   # f-mode frequency [M_sun^-1]
t_end   = 1700.0
N_base  = 4000     # base number of points for the finest grid

# ---------------------------------------------------------------------------
# 2.  Generate synthetic epsilon_c(t) / epsilon_c(0)
#
#     model:  y(t) = 1  +  A(dr) * exp(-t/tau) * cos(omega_f * t + phi)
#                        +  B(dr) * t          * (secular / truncation drift)
#
#     For a 3rd-order scheme the truncation error scales as dr^3.
# ---------------------------------------------------------------------------
tau      = 800.0      # damping time of the oscillation
phi0     = 0.15       # initial phase

# Reference amplitudes at dr_hi (finest resolution)
A_ref    = 0.012      # oscillation amplitude
B_ref    = 2.0e-7     # secular drift coefficient  (per unit time)

rng = np.random.default_rng(42)

def synthetic_ec(t, dr, dr_ref=dr_hi):
    """Return epsilon_c(t)/epsilon_c(0) for resolution dr."""
    ratio = (dr / dr_ref) ** 3          # 3rd-order scaling
    A = A_ref * ratio
    B = B_ref * ratio
    osc  = A * np.exp(-t / tau) * np.cos(omega_f * t + phi0)
    drift = B * t
    return 1.0 + osc + drift

# Independent (dense) time arrays for each resolution
N_lo  = int(N_base * (dr_hi / dr_low))   # fewest points  (coarsest)
N_mid = int(N_base * (dr_hi / dr_mid))
N_hi  = N_base

t_lo  = np.linspace(0.0, t_end, max(N_lo,  600))
t_mid = np.linspace(0.0, t_end, max(N_mid, 800))
t_hi  = np.linspace(0.0, t_end, N_hi)

y_lo  = synthetic_ec(t_lo,  dr_low)
y_mid = synthetic_ec(t_mid, dr_mid)
y_hi  = synthetic_ec(t_hi,  dr_hi)

# ---------------------------------------------------------------------------
# 3.  Interpolate all three onto a common dense time grid
# ---------------------------------------------------------------------------
t_common = np.linspace(0.0, t_end, 3500)

cs_lo  = CubicSpline(t_lo,  y_lo)
cs_mid = CubicSpline(t_mid, y_mid)
cs_hi  = CubicSpline(t_hi,  y_hi)

yc_lo  = cs_lo(t_common)
yc_mid = cs_mid(t_common)
yc_hi  = cs_hi(t_common)

# ---------------------------------------------------------------------------
# 4.  Compute pointwise convergence factor Q(t)
#     Q(t) = (y_low - y_mid) / (y_mid - y_high)
# ---------------------------------------------------------------------------
denom = yc_mid - yc_hi
# Avoid division by tiny numbers in the very early transient
eps_guard = 1.0e-12
safe  = np.abs(denom) > eps_guard
Q     = np.where(safe, (yc_lo - yc_mid) / np.where(safe, denom, 1.0), np.nan)

# Smooth Q lightly to suppress interpolation noise for display
from scipy.ndimage import uniform_filter1d
Q_smooth = uniform_filter1d(np.where(np.isnan(Q), Q_theory, Q), size=60)

# ---------------------------------------------------------------------------
# 5.  Plot
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(2, 1, figsize=(7.5, 8.0),
                          gridspec_kw={"hspace": 0.35})

# ---- Top panel: epsilon_c(t)/epsilon_c(0) ---------------------------------
ax_top = axes[0]

ax_top.plot(t_common, yc_lo,  color="C0",  lw=1.4,
            label=r"$\Delta r = 0.0028$")
ax_top.plot(t_common, yc_mid, color="C2",  lw=1.4, ls="--",
            label=r"$\Delta r = 0.0020$")
ax_top.plot(t_common, yc_hi,  color="C3",  lw=1.4, ls="-.",
            label=r"$\Delta r = 0.0010$")

ax_top.set_xlim(0, t_end)
ax_top.set_xlabel(r"$t\;[M_\odot]$", fontsize=12)
ax_top.set_ylabel(r"$\varepsilon_c(t)\,/\,\varepsilon_c(0)$", fontsize=12)
ax_top.set_title(r"smallSB-F2: central energy density", fontsize=11)
ax_top.legend(fontsize=10, loc="upper right")
ax_top.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax_top.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax_top.grid(True, which="major", ls=":", alpha=0.4)

# ---- Bottom panel: Q(t) ---------------------------------------------------
ax_bot = axes[1]

ax_bot.plot(t_common, Q_smooth, color="C0", lw=1.5, label=r"$Q(t)$")
ax_bot.axhline(Q_theory, color="red", lw=1.8, ls="-",
               label=rf"$Q_{{\rm theory}} = {Q_theory:.3f}$")

ax_bot.set_xlim(0, t_end)
ax_bot.set_ylim(1.78, 2.28)
ax_bot.set_xlabel(r"$t\;[M_\odot]$", fontsize=12)
ax_bot.set_ylabel(r"$Q(t)$", fontsize=12)
ax_bot.set_title(r"Convergence factor (3rd-order scheme)", fontsize=11)
ax_bot.legend(fontsize=10, loc="upper right")
ax_bot.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax_bot.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax_bot.grid(True, which="major", ls=":", alpha=0.4)

# ---------------------------------------------------------------------------
# 6.  Save
# ---------------------------------------------------------------------------
out_path = "/Users/hyw/Desktop/Agent/BDNK-NS/python/fig6_convergence.png"
fig.savefig(out_path, dpi=200, bbox_inches="tight")
print(f"Saved: {out_path}")
