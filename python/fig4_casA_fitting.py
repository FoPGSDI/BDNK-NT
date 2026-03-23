"""
fig4_casA_fitting.py
--------------------
Reproduces Figure 4 of the BDNK-NS paper: decay rate extraction for smallSB-F2.

Three-panel figure:
  Top    : |ε̃_c(t)| on log scale showing exponential decay
  Middle : log of local maxima with linear fit (slope = decay rate)
  Bottom : damped sinusoidal fit overlaid on filtered data

Usage
-----
    python fig4_casA_fitting.py

Output
------
    fig4_casA_fitting.png  (saved in the current working directory)

Physical parameters (code units M_sun = 1)
-------------------------------------------
    1/τ  = 0.00157  M_sun^{-1}
    ω    = 0.0834   M_sun^{-1}
    A    = 5e-12
    t    ∈ [0, 8000] M_sun,  dt = 1 M_sun
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")          # non-interactive backend
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, argrelmax
from scipy.optimize import curve_fit

# ---------------------------------------------------------------------------
# 0.  Reproducibility
# ---------------------------------------------------------------------------
rng = np.random.default_rng(42)

# ---------------------------------------------------------------------------
# 1.  Generate synthetic damped sinusoidal signal
# ---------------------------------------------------------------------------
dt       = 1.0          # M_sun
t        = np.arange(0.0, 8001.0, dt)   # 0 … 8000 M_sun

# Physical parameters
inv_tau  = 0.00157      # 1/tau  [M_sun^{-1}]
tau      = 1.0 / inv_tau
omega    = 0.0834       # [M_sun^{-1}]
A        = 5.0e-12
phi0     = 0.0          # initial phase

# Clean signal + small white-noise perturbation (SNR ~ 100)
signal_clean = A * np.exp(-t / tau) * np.cos(omega * t + phi0)
noise        = rng.normal(0.0, A * 1e-2 * np.exp(-t / tau), size=t.size)
signal       = signal_clean + noise

# ---------------------------------------------------------------------------
# 2.  Butterworth bandpass filter  (order 4, [0.01, 0.1] M_sun^{-1})
#     Following numerical-implementations.md §8.2
# ---------------------------------------------------------------------------
def butterworth_filter(sig, dt, f_low=0.01, f_high_factor=0.1, order=4):
    """4th-order Butterworth bandpass filter."""
    f_sampling = 1.0 / dt
    f_high     = f_sampling * f_high_factor   # = 0.1 M_sun^{-1} for dt=1

    nyquist    = f_sampling / 2.0
    low        = f_low  / nyquist
    high       = f_high / nyquist

    b, a       = butter(order, [low, high], btype="band")
    return filtfilt(b, a, sig)

filtered = butterworth_filter(signal, dt)

# ---------------------------------------------------------------------------
# 3.  Window for the three panels  [4000, 5000] M_sun
# ---------------------------------------------------------------------------
T_START, T_END = 4000.0, 5000.0
mask_win       = (t >= T_START) & (t <= T_END)
t_win          = t[mask_win]
filt_win       = filtered[mask_win]

# ---------------------------------------------------------------------------
# 4.  Middle-panel: linear fit to log of envelope maxima
#     Following numerical-implementations.md §8.3
# ---------------------------------------------------------------------------
abs_win  = np.abs(filt_win)
max_idx  = argrelmax(abs_win, order=3)[0]   # local maxima of |filtered|

t_max    = t_win[max_idx]
amp_max  = abs_win[max_idx]

# Guard against zero or negative amplitudes before log
valid        = amp_max > 0
t_max        = t_max[valid]
amp_max      = amp_max[valid]
log_max      = np.log(amp_max)

# Linear fit:  log|ε̃_c| ≈ log(A') - t/τ
coeffs       = np.polyfit(t_max, log_max, 1)
decay_rate_linear = -coeffs[0]              # 1/τ

t_fit_line   = np.linspace(t_max[0], t_max[-1], 200)
log_fit_line = np.polyval(coeffs, t_fit_line)

# ---------------------------------------------------------------------------
# 5.  Bottom-panel: non-linear damped-sinusoid fit
#     Following numerical-implementations.md §8.3
# ---------------------------------------------------------------------------
def damped_sinusoid(t, A_fit, tau_fit, omega_fit, phi_fit, C):
    return A_fit * np.exp(-t / tau_fit) * np.cos(omega_fit * t + phi_fit) + C

# Shift time to near zero for numerical stability of the fitter
t0           = T_START
t_shifted    = t_win - t0

A_guess      = np.max(np.abs(filt_win))
tau_guess    = 600.0
omega_guess  = omega
phi_guess    = 0.0
C_guess      = 0.0
p0           = [A_guess, tau_guess, omega_guess, phi_guess, C_guess]

popt, pcov   = curve_fit(
    damped_sinusoid, t_shifted, filt_win,
    p0=p0, maxfev=20000,
    bounds=(
        [0,      50,   0.05, -np.pi, -np.inf],
        [np.inf, 5000, 0.15,  np.pi,  np.inf],
    ),
)

A_fit, tau_fit, omega_fit, phi_fit, C_fit = popt
decay_rate_nl = 1.0 / tau_fit

filt_model   = damped_sinusoid(t_shifted, *popt)

# ---------------------------------------------------------------------------
# 6.  Print results
# ---------------------------------------------------------------------------
print("=" * 55)
print("  Decay rate extraction – smallSB-F2 (synthetic data)")
print("=" * 55)
print(f"  True values :  1/τ = {inv_tau:.5f}  M_sun^{{-1}},  "
      f"ω = {omega:.4f} M_sun^{{-1}}")
print(f"  Linear fit  :  1/τ = {decay_rate_linear:.5f}  M_sun^{{-1}}")
print(f"  Nonlin. fit :  1/τ = {decay_rate_nl:.5f}  M_sun^{{-1}},  "
      f"ω = {omega_fit:.4f} M_sun^{{-1}}")
print("=" * 55)

# ---------------------------------------------------------------------------
# 7.  Figure: three-panel layout  (reproducing Fig. 4)
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(3, 1, figsize=(8, 10),
                         gridspec_kw={"hspace": 0.45})

col_data  = "#1f77b4"   # blue
col_fit   = "#d62728"   # red
col_max   = "orange"
lw        = 1.2

# ------ Top panel: |ε̃_c(t)| on log scale --------------------------------
ax0 = axes[0]
ax0.semilogy(t_win, np.abs(filt_win), color=col_data, lw=lw,
             label=r"$|\tilde{\varepsilon}_c(t)|$")
ax0.set_xlim(T_START, T_END)
ax0.set_xlabel(r"$t \; [M_\odot]$", fontsize=11)
ax0.set_ylabel(r"$|\tilde{\varepsilon}_c|$", fontsize=11)
ax0.set_title(r"$|\tilde{\varepsilon}_c(t)|$ – log scale (smallSB-F2)",
              fontsize=11)
ax0.legend(fontsize=9)
ax0.grid(True, which="both", alpha=0.3)

# ------ Middle panel: log(maxima) + linear fit ----------------------------
ax1 = axes[1]
ax1.scatter(t_max, log_max, s=25, color=col_max, zorder=5,
            label="Local maxima")
ax1.plot(t_fit_line, log_fit_line, color=col_fit, lw=lw,
         label=(rf"Linear fit: $1/\tau={decay_rate_linear:.5f}\,M_\odot^{{-1}}$"))
ax1.set_xlim(T_START, T_END)
ax1.set_xlabel(r"$t \; [M_\odot]$", fontsize=11)
ax1.set_ylabel(r"$\ln|\tilde{\varepsilon}_c^{\rm max}|$", fontsize=11)
ax1.set_title("Log-envelope maxima with linear fit", fontsize=11)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)

# ------ Bottom panel: damped sinusoid fit ---------------------------------
ax2 = axes[2]
ax2.plot(t_win, filt_win, color=col_data, lw=lw, alpha=0.8,
         label=r"Filtered $\tilde{\varepsilon}_c$")
ax2.plot(t_win, filt_model, color=col_fit, lw=lw + 0.4, ls="--",
         label=(rf"Damped sinusoid fit"
                rf"  $1/\tau={decay_rate_nl:.5f}$,"
                rf"  $\omega={omega_fit:.4f}\,M_\odot^{{-1}}$"))
ax2.set_xlim(T_START, T_END)
ax2.set_xlabel(r"$t \; [M_\odot]$", fontsize=11)
ax2.set_ylabel(r"$\tilde{\varepsilon}_c$", fontsize=11)
ax2.set_title("Damped sinusoidal fit", fontsize=11)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

fig.suptitle("Figure 4 – Decay rate extraction (smallSB-F2)", fontsize=13,
             fontweight="bold", y=1.01)

out_path = "fig4_casA_fitting.png"
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"\n  Figure saved to: {out_path}")
plt.close(fig)
