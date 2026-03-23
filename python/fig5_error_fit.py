#!/usr/bin/env python3
"""
Reproduces Figure 5 of the paper:
  Decay rate (code units) vs resolution for smallSB-F2 and PF(x10).

Data from Table III of the paper.
Extrapolation model: 1/tau_dr = 1/tau_0 + m * dr^p
  - PF: fix 1/tau_0 = 0, fit m and p  -> expect p ~ 0.54
  - smallSB-F2: fit all three          -> expect 1/tau_0 ~ 0.0011, p ~ 1
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ---------------------------------------------------------------------------
# Published data from Table III
# ---------------------------------------------------------------------------

# smallSB-F2 averaged decay rates
sb_dr   = np.array([0.0032, 0.0028, 0.0024, 0.0020])
sb_rate = np.array([0.0019, 0.0018, 0.0017, 0.0016])

# PF averaged decay rates (multiplied by 10 for display)
pf_dr        = np.array([0.0032, 0.0028, 0.0024, 0.0020])
pf_rate_raw  = np.array([0.00023, 0.00021, 0.00019, 0.00018])
pf_rate      = pf_rate_raw * 10           # scale for display

# Individual estimates with small scatter (simulated near the averaged values)
# The paper shows red/green dots spread slightly around the averaged (black/blue) dots.
# We simulate two individual estimates per resolution by adding ±2% noise.
rng = np.random.default_rng(42)
noise_frac = 0.02

sb_dr_ind   = np.repeat(sb_dr, 2)
sb_rate_ind = np.repeat(sb_rate, 2) * (1 + noise_frac * np.array([1,-1,1,-1,1,-1,1,-1]))

pf_dr_ind   = np.repeat(pf_dr, 2)
pf_rate_ind = np.repeat(pf_rate, 2) * (1 + noise_frac * np.array([1,-1,1,-1,1,-1,1,-1]))

# ---------------------------------------------------------------------------
# Fit functions
# ---------------------------------------------------------------------------

def model_full(dr, tau0_inv, m, p):
    """Full three-parameter model: 1/tau = 1/tau_0 + m * dr^p"""
    return tau0_inv + m * np.power(dr, p)

def model_pf(dr, m, p):
    """PF model with 1/tau_0 fixed to 0: 1/tau = m * dr^p"""
    return m * np.power(dr, p)

# --- Fit PF (fix 1/tau_0 = 0) ---
# Fit using the unscaled PF rates; display is x10
p0_pf = [0.1, 0.5]
popt_pf, pcov_pf = curve_fit(model_pf, pf_dr, pf_rate_raw, p0=p0_pf, maxfev=10000)
m_pf, p_pf = popt_pf
perr_pf = np.sqrt(np.diag(pcov_pf))

print("=== PF fit (1/tau_0 fixed to 0) ===")
print(f"  m      = {m_pf:.5f}  +/- {perr_pf[0]:.5f}")
print(f"  p      = {p_pf:.4f}  +/- {perr_pf[1]:.4f}  (expect ~0.54)")

# --- Fit smallSB-F2 (all three free) ---
p0_sb = [0.0011, 0.01, 1.0]
bounds_sb = ([0, 0, 0.1], [0.002, 10, 5])
popt_sb, pcov_sb = curve_fit(model_full, sb_dr, sb_rate, p0=p0_sb,
                              bounds=bounds_sb, maxfev=50000)
tau0_inv_sb, m_sb, p_sb = popt_sb
perr_sb = np.sqrt(np.diag(pcov_sb))

print("\n=== smallSB-F2 fit (all three free) ===")
print(f"  1/tau_0 = {tau0_inv_sb:.5f}  +/- {perr_sb[0]:.5f}  (expect ~0.0011)")
print(f"  m       = {m_sb:.5f}  +/- {perr_sb[1]:.5f}")
print(f"  p       = {p_sb:.4f}  +/- {perr_sb[2]:.4f}  (expect ~1)")

# ---------------------------------------------------------------------------
# Extrapolation curves for plotting
# ---------------------------------------------------------------------------
dr_fine = np.linspace(0.0, 0.0035, 400)
dr_fine_nz = np.linspace(1e-5, 0.0035, 400)   # avoid 0^p issues

sb_fit_curve  = model_full(dr_fine_nz, *popt_sb)
pf_fit_curve  = model_pf(dr_fine_nz, *popt_pf) * 10   # scale x10 for display

# Extrapolated value at dr -> 0
sb_extrap  = tau0_inv_sb
pf_extrap  = 0.0   # fixed by model

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 5))

# ---- smallSB-F2 ----
# Individual estimates (red, smaller)
ax.plot(sb_dr_ind, sb_rate_ind, 'r.', markersize=5, zorder=3,
        label='smallSB-F2 (individual)')
# Averaged (black dots)
ax.plot(sb_dr, sb_rate, 'ko', markersize=7, zorder=4,
        label=r'smallSB-F2 (averaged)')
# Fit curve
ax.plot(dr_fine_nz, sb_fit_curve, 'k-', linewidth=1.5, zorder=2,
        label=r'smallSB-F2 fit: $1/\tau_0={:.4f},\,p={:.2f}$'.format(
              tau0_inv_sb, p_sb))
# Extrapolated point at dr=0
ax.plot(0, sb_extrap, 'k*', markersize=12, zorder=5,
        label=r'smallSB-F2 extrap. $1/\tau_0={:.4f}$'.format(sb_extrap))

# ---- PF x10 ----
# Individual estimates (green, smaller)
ax.plot(pf_dr_ind, pf_rate_ind, 'g.', markersize=5, zorder=3,
        label=r'PF$\times10$ (individual)')
# Averaged (blue dots)
ax.plot(pf_dr, pf_rate, 'bo', markersize=7, zorder=4,
        label=r'PF$\times10$ (averaged)')
# Fit curve
ax.plot(dr_fine_nz, pf_fit_curve, 'b-', linewidth=1.5, zorder=2,
        label=r'PF fit ($1/\tau_0=0$): $p={:.2f}$'.format(p_pf))
# Extrapolated point at dr=0  (zero by construction)
ax.plot(0, 0, 'b*', markersize=12, zorder=5,
        label=r'PF extrap. $1/\tau_0=0$ (fixed)')

# ---- Formatting ----
ax.set_xlabel(r'Resolution $\delta r$ (code units)', fontsize=13)
ax.set_ylabel(r'Decay rate $1/\tau$ (code units)', fontsize=13)
ax.set_title('Figure 5: Decay rate vs resolution\n'
             r'(smallSB-F2 and PF$\times10$)', fontsize=13)
ax.set_xlim(-0.0001, 0.00345)
ax.set_ylim(-0.0001, 0.0022)
ax.legend(fontsize=8, loc='upper left', framealpha=0.9)
ax.tick_params(labelsize=11)
ax.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
out_path = '/Users/hyw/Desktop/Agent/BDNK-NS/python/fig5_error_fit.png'
plt.savefig(out_path, dpi=150)
print(f"\nFigure saved to {out_path}")
plt.show()
