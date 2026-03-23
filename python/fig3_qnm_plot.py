"""
fig3_qnm_plot.py
----------------
Reproduces Figure 3 of the BDNK viscous neutron-star paper.

Figure 3 has two panels:
  Top   : epsilon_c(t) oscillations for PF, smallSB-F2, highB-F9  (t = 0..8000 M_sun)
  Bottom: Power spectral density (Blackman window) showing F, H1, H2 QNM peaks

Signal model
------------
Each run is modelled as a superposition of three damped sinusoids (F, H1, H2)
plus a secular (linear) drift for the PF run:

  epsilon_c(t) = eps_c0
                + drift * t                           (PF only)
                + A * exp(-t/tau) * sum_k [ a_k * cos(omega_k * t + phi_k) ]

where the QNM frequencies (kHz) are converted to code units via:
  omega [1/M_sun] = 2*pi * f [kHz] * 1e3 [Hz/kHz] * 4.926e-6 [M_sun/s]
                  = 2*pi * f_kHz * 4.926e-3

QNM parameters (from paper Table / Fig. 3 annotations):
  PF      : F=2.69, H1=4.55, H2=6.36 kHz;  1/tau = 0.00018
  smallSB : F=2.69, H1=4.60, H2=6.36 kHz;  1/tau = 0.00157
  highB   : F=2.67, H1=4.60, H2=6.30 kHz;  1/tau = 0.00215

Baseline: eps_c0 = 0.00144  (equilibrium central energy density)
Perturbation amplitude: A = 1e-7
Secular drift for PF: ~4e-7 over 7500 M_sun  →  slope = 4e-7/7500
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal.windows import blackman
from scipy.fft import fft, fftfreq

# ---------------------------------------------------------------------------
# Constants / conversion
# ---------------------------------------------------------------------------
M_SUN_S = 4.926e-6          # seconds per solar mass (geometrised units)
KHZ_TO_CODE = 2.0 * np.pi * 1.0e3 * M_SUN_S   # [1/M_sun] per kHz

# ---------------------------------------------------------------------------
# Run parameters
# ---------------------------------------------------------------------------
runs = {
    "PF": {
        "freqs_kHz": [2.69, 4.55, 6.36],
        "inv_tau": 0.00018,
        "color": "#1f77b4",   # matplotlib blue
        "linestyle": "-",
        "label": "PF",
        "secular_drift": 4.0e-7 / 7500.0,   # linear ramp over 7500 M_sun
    },
    "smallSB-F2": {
        "freqs_kHz": [2.69, 4.60, 6.36],
        "inv_tau": 0.00157,
        "color": "#ff7f0e",   # orange
        "linestyle": "--",
        "label": "smallSB-F2",
        "secular_drift": 0.0,
    },
    "highB-F9": {
        "freqs_kHz": [2.67, 4.60, 6.30],
        "inv_tau": 0.00215,
        "color": "#2ca02c",   # green
        "linestyle": "-.",
        "label": "highB-F9",
        "secular_drift": 0.0,
    },
}

EPS_C0 = 0.00144          # baseline central energy density [M_sun^{-2}]
AMPLITUDE = 1.0e-7        # total perturbation amplitude
# Relative amplitudes of F, H1, H2 modes (F dominates, H modes are weaker)
MODE_WEIGHTS = np.array([0.70, 0.20, 0.10])
# Phase offsets (arbitrary, chosen to give a realistic-looking beat pattern)
PHASES = np.array([0.0, 0.4, 0.8])   # radians

# Time axis: 0 to 8000 M_sun, finely sampled for smooth PSD
T_END = 8000.0          # M_sun
N_POINTS = 80001        # ~10 pts per M_sun  →  dt = 0.1 M_sun
t = np.linspace(0.0, T_END, N_POINTS)
dt = t[1] - t[0]

# ---------------------------------------------------------------------------
# Synthetic signal generator
# ---------------------------------------------------------------------------
def make_signal(params: dict, t: np.ndarray) -> np.ndarray:
    """Return synthetic epsilon_c(t) for a given run."""
    inv_tau = params["inv_tau"]
    freqs_kHz = params["freqs_kHz"]
    drift = params["secular_drift"]

    envelope = AMPLITUDE * np.exp(-inv_tau * t)
    osc = np.zeros_like(t)
    for k, (f_kHz, w, phi) in enumerate(zip(freqs_kHz, MODE_WEIGHTS, PHASES)):
        omega = f_kHz * KHZ_TO_CODE
        osc += w * np.cos(omega * t + phi)

    return EPS_C0 + drift * t + envelope * osc

# ---------------------------------------------------------------------------
# Compute PSD  (from numerical-implementations.md §8.1)
# ---------------------------------------------------------------------------
def compute_psd(signal: np.ndarray, dt: float):
    """Power spectral density with Blackman window.

    Returns
    -------
    freqs_kHz : positive-frequency axis in kHz
    psd       : |FFT|^2 (arbitrary units, not normalised)
    """
    N = len(signal)
    w = blackman(N)
    windowed = signal * w
    spectrum = fft(windowed)
    freqs = fftfreq(N, d=dt)          # units: 1/M_sun

    psd = np.abs(spectrum[:N // 2]) ** 2
    freqs_pos = freqs[:N // 2]

    # Convert from 1/M_sun to kHz
    freqs_kHz = freqs_pos / KHZ_TO_CODE

    return freqs_kHz, psd

# ---------------------------------------------------------------------------
# Build signals and PSDs
# ---------------------------------------------------------------------------
signals = {}
psds = {}
for name, params in runs.items():
    sig = make_signal(params, t)
    signals[name] = sig
    freqs_kHz, psd = compute_psd(sig - sig.mean(), dt)   # remove DC before PSD
    psds[name] = (freqs_kHz, psd)

# ---------------------------------------------------------------------------
# Figure layout
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(
    2, 1,
    figsize=(8, 7),
    constrained_layout=True,
)

# ── Top panel: epsilon_c(t) ─────────────────────────────────────────────────
ax_top = axes[0]
for name, params in runs.items():
    ax_top.plot(
        t, signals[name],
        color=params["color"],
        linestyle=params["linestyle"],
        linewidth=0.8,
        label=params["label"],
    )

ax_top.set_xlabel(r"$t\ [M_\odot]$", fontsize=11)
ax_top.set_ylabel(r"$\varepsilon_c\ [M_\odot^{-2}]$", fontsize=11)
ax_top.set_xlim(0.0, T_END)
ax_top.set_ylim(0.0014428, 0.0014434)
ax_top.legend(loc="upper right", fontsize=9, framealpha=0.9)
ax_top.set_title(
    r"Central energy density $\varepsilon_c(t)$ — QNM oscillations",
    fontsize=11,
)
ax_top.tick_params(labelsize=9)

# ── Bottom panel: PSD ────────────────────────────────────────────────────────
ax_bot = axes[1]

# Frequency range of interest: 0 to ~8 kHz
F_MAX_KHZ = 8.0

# QNM peak positions for annotation (use PF values as reference)
qnm_labels = {
    "F":  2.69,
    "H1": 4.55,
    "H2": 6.36,
}

for name, params in runs.items():
    freqs_kHz, psd = psds[name]
    mask = freqs_kHz <= F_MAX_KHZ
    ax_bot.semilogy(
        freqs_kHz[mask], psd[mask],
        color=params["color"],
        linestyle=params["linestyle"],
        linewidth=0.9,
        label=params["label"],
    )

# Annotate QNM peaks with vertical dashed lines and labels
# Choose a representative y position in the middle of the plot y-range
ax_bot.set_xlim(0.0, F_MAX_KHZ)
ax_bot.set_xlabel(r"Frequency $[{\rm kHz}]$", fontsize=11)
ax_bot.set_ylabel(r"PSD (arbitrary units)", fontsize=11)
ax_bot.legend(loc="upper right", fontsize=9, framealpha=0.9)
ax_bot.set_title(
    "Power spectral density (Blackman window)",
    fontsize=11,
)
ax_bot.tick_params(labelsize=9)

# Annotate mode labels after setting axes limits so ylim is finalised
ax_bot.figure.canvas.draw()          # force layout so get_ylim() is reliable
y_lo, y_hi = ax_bot.get_ylim()
y_ann = 10 ** (0.85 * np.log10(y_hi) + 0.15 * np.log10(y_lo))  # 85% from top

for mode, f_kHz in qnm_labels.items():
    ax_bot.axvline(f_kHz, color="gray", linestyle=":", linewidth=0.8, alpha=0.7)
    ax_bot.text(
        f_kHz + 0.05, y_ann, mode,
        fontsize=10, color="dimgray",
        ha="left", va="center",
        fontstyle="italic",
    )

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out_path = "/Users/hyw/Desktop/Agent/BDNK-NS/python/fig3_qnm_plot.png"
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved: {out_path}")
plt.close(fig)
