"""
generate_figures.py — Reproduce all 6 figures from arXiv:2509.15303v1.

Usage:
    python generate_figures.py [--fig N] [--all] [--tov-only]

Figures:
    1: stable_evol_comparing_tau — ε(r) profiles for 4 parameter cases
    2: stable_evol_resolutions  — ε(r) at 3 resolutions (convergence)
    3: QNM_plot                 — Central density oscillations + PSD
    4: casA_fitting             — Decay rate extraction (3-panel)
    5: error_fit                — Decay rate vs resolution
    6: convergence              — ε_c(t)/ε_c(0) + Q(t)
"""

import sys
import os
import time
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

sys.path.insert(0, os.path.dirname(__file__))
import bdnk_core as bc

# ═══════════════════════════════════════════════════════════════════════
#  Paper parameters and constants
# ═══════════════════════════════════════════════════════════════════════

CASES = {
    'smallSB-F2': {'hat_eta': 0.01,    'hat_zeta': 0.01,  'color': 'green',  'marker': '-'},
    'medS-F2':    {'hat_eta': 0.01725, 'hat_zeta': 0.0,   'color': 'red',    'marker': '.'},
    'highB-F9':   {'hat_eta': 0.0015,  'hat_zeta': 0.09,  'color': 'blue',   'marker': '-'},
    'medSB-F9':   {'hat_eta': 0.03525, 'hat_zeta': 0.045, 'color': 'orange', 'marker': '.'},
}

# Convert code-unit frequency to kHz:  f_kHz = f_code / (2π) × 203.025
CODE_TO_KHZ = 203.025 / (2.0 * np.pi)

# Paper QNM frequencies (kHz, from Table II / Fig 3)
QNM_FREQS_KHZ = {'F': 2.696, 'H1': 4.586, 'H2': 6.392}

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'figures')
os.makedirs(OUT_DIR, exist_ok=True)


def save_fig(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    print(f"  Saved {path}")
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════
#  TOV / Initial Data (exact, no evolution needed)
# ═══════════════════════════════════════════════════════════════════════

def get_tov_profile(dr=0.01, r_max=20.0):
    """Build grid and return the equilibrium ε(r) profile."""
    grid = bc.GridData(dr=dr, r_max=r_max, rho0c=0.00128)
    return grid


def verify_tov():
    """Verify TOV solution against paper values."""
    grid = get_tov_profile(dr=0.005)
    eps_c = grid.eps_bg[0]
    # Paper: ρ₀c = 0.00128, εc ≈ 0.00144, M = 1.4 M☉
    print(f"  TOV verification:")
    print(f"    ε_c = {eps_c:.6e} (paper: ~0.00144)")
    print(f"    α_c = {grid.alpha[0]:.6f}")

    # Find stellar surface (where eps drops to ~0)
    i_surf = np.searchsorted(-grid.eps_bg, -1e-8)
    r_surf = grid.r[i_surf] if i_surf < grid.N else grid.r[-1]
    print(f"    R_star(iso) ≈ {r_surf:.2f} M☉")

    # Speed of sound at centre
    cs2_c = bc.dpressure_deps(eps_c)
    print(f"    c_s²(centre) = {cs2_c:.6f}")
    return grid


# ═══════════════════════════════════════════════════════════════════════
#  Evolution helper
# ═══════════════════════════════════════════════════════════════════════

def run_evolution(dr, r_max, t_end, hat_eta, hat_zeta, dt_save=1.0,
                  label="", verbose=True):
    """Run a full BDNK evolution and return (times, eps_central, grid, states)."""
    t0 = time.time()
    if verbose:
        print(f"  [{label}] Building grid dr={dr}, r_max={r_max}...")
    grid = bc.GridData(dr=dr, r_max=r_max, rho0c=0.00128)
    U0 = bc.build_initial_state(grid)

    if verbose:
        print(f"  [{label}] Evolving to t={t_end} (N={grid.N}, dt_save={dt_save})...")
    times, states = bc.evolve(grid, U0, t_end,
                               hat_eta=hat_eta, hat_zeta=hat_zeta,
                               dt_save=dt_save)

    times = np.array(times)
    eps_central = np.array([s[2, 0] for s in states])

    elapsed = time.time() - t0
    if verbose:
        rel = abs(eps_central[-1] - eps_central[0]) / eps_central[0]
        print(f"  [{label}] Done in {elapsed:.0f}s. "
              f"eps_c: {eps_central[0]:.6e} → {eps_central[-1]:.6e} "
              f"(Δ={rel:.2e})")

    return {
        'times': times,
        'eps_central': eps_central,
        'grid': grid,
        'states': states,
        'U0': states[0],
        'Uf': states[-1],
        'label': label,
    }


# ═══════════════════════════════════════════════════════════════════════
#  Figure 1: ε(r) profiles at t=t_end for 4 parameter cases
# ═══════════════════════════════════════════════════════════════════════

def figure_1(results_dict, grid_ref):
    """
    Reproduce Paper Fig 1: ε(r) at t=2000 for four parameter cases.
    results_dict: {case_name: run_result}
    grid_ref: reference grid for initial data
    """
    fig, ax_main = plt.subplots(figsize=(10, 7))

    r = grid_ref.r
    # Initial data
    ax_main.plot(r, grid_ref.eps_bg, 'ko', markersize=2, label='$t=0$', zorder=5)

    for name, params in CASES.items():
        if name in results_dict:
            res = results_dict[name]
            eps_final = res['Uf'][2]
            ax_main.plot(res['grid'].r, eps_final,
                        color=params['color'], linewidth=1.5, label=name)

    ax_main.set_xlabel(r'$r/M_\odot$', fontsize=14)
    ax_main.set_ylabel(r'$\epsilon\, M_\odot^2$', fontsize=14)
    ax_main.set_xlim(0, 19)
    ax_main.set_ylim(-5e-5, 0.0015)
    ax_main.legend(fontsize=11, loc='center left')

    # Inset 1: zoom on central region
    ax_in1 = fig.add_axes([0.22, 0.55, 0.32, 0.32])
    ax_in1.plot(r, grid_ref.eps_bg, 'ko', markersize=3)
    for name, params in CASES.items():
        if name in results_dict:
            res = results_dict[name]
            ax_in1.plot(res['grid'].r, res['Uf'][2],
                       color=params['color'], linewidth=1.2)
    ax_in1.set_xlim(0.02, 0.12)
    ax_in1.set_ylim(0.0014426, 0.0014436)
    ax_in1.ticklabel_format(axis='y', style='plain', useOffset=True)

    # Inset 2: zoom on surface
    ax_in2 = fig.add_axes([0.6, 0.25, 0.28, 0.25])
    ax_in2.plot(r, grid_ref.eps_bg, 'ko', markersize=3)
    for name, params in CASES.items():
        if name in results_dict:
            res = results_dict[name]
            ax_in2.plot(res['grid'].r, res['Uf'][2],
                       color=params['color'], linewidth=1.2)
    ax_in2.set_xlim(8.0, 8.25)
    ax_in2.set_ylim(-5e-7, 8e-6)

    save_fig(fig, 'fig1_eps_profiles.png')


# ═══════════════════════════════════════════════════════════════════════
#  Figure 2: ε(r) at multiple resolutions (convergence)
# ═══════════════════════════════════════════════════════════════════════

def figure_2(resolution_results, case_name='smallSB-F2'):
    """
    Reproduce Paper Fig 2: ε(r) at t_end for 3 resolutions.
    resolution_results: list of run results at different dr.
    """
    fig, ax_main = plt.subplots(figsize=(10, 7))
    colors = {0.001: 'blue', 0.002: 'green', 0.0032: 'red',
              0.004: 'blue', 0.008: 'green', 0.01: 'red'}

    # Plot initial data from finest resolution
    ref = resolution_results[0]
    r0 = ref['grid'].r
    ax_main.plot(r0, ref['grid'].eps_bg, 'k-', linewidth=2, label='$t=0$')

    for res in resolution_results:
        dr = res['grid'].dr
        c = colors.get(dr, 'purple')
        ax_main.plot(res['grid'].r, res['Uf'][2],
                    color=c, linewidth=1.5,
                    label=rf'$\Delta r = {dr}$')

    ax_main.set_xlabel(r'$r/M_\odot$', fontsize=14)
    ax_main.set_ylabel(r'$\epsilon\, M_\odot^2$', fontsize=14)
    ax_main.set_xlim(0, 19)
    ax_main.set_ylim(-5e-5, 0.0015)
    ax_main.legend(fontsize=11)
    ax_main.set_title(f'{case_name} — resolution comparison', fontsize=13)

    # Inset: central zoom
    ax_in = fig.add_axes([0.22, 0.55, 0.32, 0.32])
    ax_in.plot(r0, ref['grid'].eps_bg, 'k-', linewidth=2)
    for res in resolution_results:
        dr = res['grid'].dr
        c = colors.get(dr, 'purple')
        ax_in.plot(res['grid'].r, res['Uf'][2], color=c, linewidth=1.2)
    ax_in.set_xlim(0.02, 0.12)
    ax_in.set_ylim(0.0014426, 0.0014436)

    save_fig(fig, 'fig2_resolutions.png')


# ═══════════════════════════════════════════════════════════════════════
#  Figure 3: Central density + PSD
# ═══════════════════════════════════════════════════════════════════════

def figure_3(results_dict):
    """
    Reproduce Paper Fig 3: ε_c(t) and PSD.
    results_dict should contain at least 'smallSB-F2' and 'highB-F9'.
    """
    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(10, 8))

    for name, params in [('smallSB-F2', CASES['smallSB-F2']),
                          ('highB-F9', CASES['highB-F9'])]:
        if name not in results_dict:
            continue
        res = results_dict[name]
        t = res['times']
        ec = res['eps_central']

        ax_top.plot(t, ec, color=params['color'], linewidth=0.8, label=name)

        # PSD
        dt_save = t[1] - t[0] if len(t) > 1 else 1.0
        freqs, psd = bc.compute_psd(ec - np.mean(ec), dt_save)
        freq_khz = freqs * CODE_TO_KHZ
        mask = freq_khz > 0.5
        ax_bot.semilogy(freq_khz[mask], psd[mask],
                       color=params['color'], linewidth=0.8, label=name)

    ax_top.set_xlabel(r'$t/M_\odot$', fontsize=13)
    ax_top.set_ylabel(r'$\epsilon_c(t)\,M_\odot^2$', fontsize=13)
    ax_top.set_title('Central Density Evolution', fontsize=13)
    ax_top.legend(fontsize=11)

    # Mark known QNM frequencies
    for mode, f_khz in QNM_FREQS_KHZ.items():
        ax_bot.axvline(f_khz, color='gray', alpha=0.5, linewidth=2)
        ax_bot.text(f_khz, ax_bot.get_ylim()[1] * 0.5, mode,
                   ha='center', fontsize=11, color='gray')

    ax_bot.set_xlabel(r'$f$ [kHz]', fontsize=13)
    ax_bot.set_ylabel('PSD', fontsize=13)
    ax_bot.set_title('Power Spectral Density', fontsize=13)
    ax_bot.set_xlim(2, 7)
    ax_bot.legend(fontsize=11)

    fig.tight_layout()
    save_fig(fig, 'fig3_qnm_psd.png')


# ═══════════════════════════════════════════════════════════════════════
#  Figure 4: Decay rate extraction (3-panel)
# ═══════════════════════════════════════════════════════════════════════

def figure_4(result, t_start=4000, t_end=5000, case_name='smallSB-F2'):
    """
    Reproduce Paper Fig 4: 3-panel decay rate extraction.
    Top: |ε̃_c(t)| on log scale
    Middle: log of envelope maxima + linear fit
    Bottom: filtered signal + damped sinusoid fit
    """
    from scipy.signal import argrelmax

    t = result['times']
    ec = result['eps_central']
    dt = t[1] - t[0]

    # Filter to isolate F-mode
    try:
        ec_filt = bc.butterworth_filter(ec - np.mean(ec), dt,
                                         f_low=0.005, f_high_factor=0.05)
    except Exception:
        print("  [Fig4] Butterworth filter failed — signal too short or flat")
        return

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10), sharex=True)

    mask = (t >= t_start) & (t <= t_end)
    t_w = t[mask]
    sig = ec_filt[mask]

    # Panel 1: |ε̃_c|
    ax1.semilogy(t_w, np.abs(sig), 'b-', linewidth=0.5)
    ax1.set_ylabel(r'$|\tilde{\epsilon}_c(t)|$', fontsize=12)

    # Panel 2: log of envelope maxima
    abs_sig = np.abs(sig)
    max_idx = argrelmax(abs_sig, order=5)[0]
    if len(max_idx) > 2:
        t_max = t_w[max_idx]
        log_max = np.log(np.maximum(abs_sig[max_idx], 1e-30))
        coeffs = np.polyfit(t_max, log_max, 1)
        ax2.plot(t_max, log_max, 'bo', markersize=4, label='data')
        ax2.plot(t_max, np.polyval(coeffs, t_max), 'r-', label='best fit')
        ax2.set_ylabel(r'$\log(|\tilde{\epsilon}_c(t)|)$', fontsize=12)
        ax2.legend()
        decay_rate = -coeffs[0]
        print(f"  [{case_name}] Linear decay rate: 1/τ = {decay_rate:.6f}")

    # Panel 3: signal + fit
    ax3.plot(t_w, sig * 1e12, 'b.', markersize=3, label='data')
    try:
        fit = bc.extract_decay_rate_nonlinear(ec_filt, t, t_start, t_end)
        from scipy.optimize import curve_fit
        def damped_sin(tt, A, tau, omega, phi, C):
            return A * np.exp(-tt / tau) * np.cos(omega * tt + phi) + C
        fitted = damped_sin(t_w, fit['amplitude'], fit['tau'],
                           fit['omega'], fit['phase'], fit['offset'])
        ax3.plot(t_w, fitted * 1e12, 'r-', linewidth=0.8, label='best fit')
        print(f"  [{case_name}] Nonlinear fit: f={fit['frequency_kHz']:.3f} kHz, "
              f"1/τ={fit['decay_rate']:.6f}")
    except Exception as e:
        print(f"  [{case_name}] Nonlinear fit failed: {e}")
    ax3.set_ylabel(r'$\tilde{\epsilon}_c(t) \times 10^{12}$', fontsize=12)
    ax3.set_xlabel(r'$t/M_\odot$', fontsize=12)
    ax3.legend()

    fig.suptitle(f'{case_name} — Decay rate extraction', fontsize=13)
    fig.tight_layout()
    save_fig(fig, 'fig4_decay_fitting.png')


# ═══════════════════════════════════════════════════════════════════════
#  Figure 5: Decay rate vs resolution
# ═══════════════════════════════════════════════════════════════════════

def figure_5(decay_data):
    """
    Reproduce Paper Fig 5: 1/τ vs Δr.
    decay_data: list of dicts with 'dr', 'decay_rate', 'case', 'error'.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    for case_name in ['smallSB-F2']:
        subset = [d for d in decay_data if d['case'] == case_name]
        if not subset:
            continue
        drs = [d['dr'] for d in subset]
        rates = [d['decay_rate'] for d in subset]
        errs = [d.get('error', 0) for d in subset]
        c = CASES[case_name]['color'] if case_name in CASES else 'black'
        ax.errorbar(drs, rates, yerr=errs, fmt='o-', color=c,
                   label=case_name, capsize=3)

    ax.set_xlabel(r'$\Delta r$', fontsize=14)
    ax.set_ylabel(r'$1/\tau_{\Delta r}$', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=12)

    save_fig(fig, 'fig5_decay_vs_dr.png')


# ═══════════════════════════════════════════════════════════════════════
#  Figure 6: Convergence (ε_c(t)/ε_c(0) + Q(t))
# ═══════════════════════════════════════════════════════════════════════

def figure_6(resolution_results):
    """
    Reproduce Paper Fig 6: convergence factor.
    resolution_results: list of 3 run results sorted finest→coarsest.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    colors_res = ['red', 'blue', 'green']

    for i, res in enumerate(resolution_results):
        t = res['times']
        ec = res['eps_central']
        dr = res['grid'].dr
        ax1.plot(t, ec / ec[0], color=colors_res[i], linewidth=1,
                label=rf'$\Delta r = {dr}$')

    ax1.set_ylabel(r'$\epsilon_c(t)/\epsilon_c(0)$', fontsize=13)
    ax1.legend(fontsize=11)

    # Q(t) if we have 3 resolutions
    if len(resolution_results) >= 3:
        r0, r1, r2 = resolution_results[0], resolution_results[1], resolution_results[2]
        tc, Qt, Qt_theory = bc.compute_pointwise_Q(
            r2['times'], r2['eps_central'],
            r1['times'], r1['eps_central'],
            r0['times'], r0['eps_central'],
            r2['grid'].dr, r1['grid'].dr, r0['grid'].dr, n=3)
        ax2.plot(tc, Qt, 'b-', linewidth=0.8)
        ax2.axhline(Qt_theory, color='red', linestyle='--', linewidth=2,
                    label=f'$Q_{{theory}} = {Qt_theory:.2f}$')
        ax2.set_ylim(1.5, 2.5)
        ax2.legend(fontsize=11)

    ax2.set_xlabel(r'$t/M_\odot$', fontsize=13)
    ax2.set_ylabel(r'$\mathcal{Q}(t)$', fontsize=13)

    fig.tight_layout()
    save_fig(fig, 'fig6_convergence.png')


# ═══════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════

def load_npz(path):
    """Load evolution data from a .npz file into a result dict."""
    d = np.load(path)
    class SimpleGrid:
        pass
    g = SimpleGrid()
    g.r = d['r']
    g.eps_bg = d['eps_bg']
    g.dr = float(d['dr'])
    g.N = len(g.r)
    return {
        'times': d['times'],
        'eps_central': d['eps_c'],
        'grid': g,
        'Uf': np.zeros((6, g.N)),  # placeholder
        'U0': np.zeros((6, g.N)),
        'eps_final': d['eps_final'] if 'eps_final' in d else None,
    }


def load_all_runs(data_dir):
    """Load all available .npz run files from data_dir."""
    results = {}
    name_map = {
        'run_smallSB_F2.npz': 'smallSB-F2',
        'run_medS_F2.npz': 'medS-F2',
        'run_highB_F9.npz': 'highB-F9',
        'run_medSB_F9.npz': 'medSB-F9',
    }
    for fname, case_name in name_map.items():
        fpath = os.path.join(data_dir, fname)
        if os.path.exists(fpath):
            r = load_npz(fpath)
            r['label'] = case_name
            # Fix: set eps_final in the Uf placeholder
            if r['eps_final'] is not None:
                r['Uf'] = np.zeros((6, r['grid'].N))
                r['Uf'][2] = r['eps_final']
            results[case_name] = r
            print(f"  Loaded {case_name} from {fname}")
    return results


def generate_all_figures(data_dir):
    """Generate all available figures from saved .npz data."""
    print("\n" + "=" * 60)
    print("  Generating figures from saved evolution data")
    print("=" * 60)

    # Load main case runs
    results = load_all_runs(data_dir)
    if not results:
        print("  No evolution data found! Run the evolutions first.")
        return

    # Reference grid for initial data
    grid_ref = get_tov_profile(dr=0.005)

    # --- Figure 1 ---
    available = [k for k in results if results[k]['eps_final'] is not None]
    if available:
        print(f"\n--- Figure 1: ε(r) profiles ({len(available)} cases) ---")
        figure_1(results, grid_ref)

    # --- Figure 3 ---
    fig3_cases = [k for k in ['smallSB-F2', 'highB-F9'] if k in results]
    if fig3_cases:
        print(f"\n--- Figure 3: Central density + PSD ({fig3_cases}) ---")
        figure_3(results)

    # --- Figure 4 ---
    if 'smallSB-F2' in results:
        r = results['smallSB-F2']
        t_max = r['times'][-1]
        if t_max >= 1000:
            # Use last quarter of data for fitting
            t_start = t_max * 0.5
            t_end = t_max * 0.9
            print(f"\n--- Figure 4: Decay fitting (t={t_start:.0f}-{t_end:.0f}) ---")
            figure_4(r, t_start=t_start, t_end=t_end, case_name='smallSB-F2')

    # --- Figures 2, 6: multi-resolution ---
    res_runs = []
    for tag in ['dr0p0050', 'dr0p0080', 'dr0p0100']:
        fpath = os.path.join(data_dir, f'run_smallSB_F2_{tag}.npz')
        if os.path.exists(fpath):
            res_runs.append(load_npz(fpath))
            print(f"  Loaded multi-res: {tag}")

    if len(res_runs) >= 2:
        print(f"\n--- Figure 2: Resolution comparison ({len(res_runs)} resolutions) ---")
        figure_2(res_runs)

    if len(res_runs) >= 3:
        print(f"\n--- Figure 6: Convergence factor ---")
        figure_6(res_runs)

    # Also load the standard dr=0.01 run as a resolution data point
    if 'smallSB-F2' in results and not res_runs:
        print(f"\n--- Figure 2: Using single resolution (dr=0.01) ---")
        figure_2([results['smallSB-F2']])

    print("\n" + "=" * 60)
    print("  Figure generation complete!")
    print(f"  Output directory: {OUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fig', type=int, default=0, help='Generate specific figure')
    parser.add_argument('--all', action='store_true', help='Generate all figures')
    parser.add_argument('--tov-only', action='store_true', help='Only verify TOV')
    parser.add_argument('--from-npz', action='store_true',
                        help='Generate figures from saved .npz data')
    args = parser.parse_args()

    if args.tov_only:
        verify_tov()
        sys.exit(0)

    print("BDNK Figure Generation")
    print("=" * 60)
    verify_tov()

    data_dir = os.path.dirname(__file__)

    if args.from_npz or args.all:
        generate_all_figures(data_dir)
