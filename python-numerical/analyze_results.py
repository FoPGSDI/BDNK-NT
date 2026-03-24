"""
analyze_results.py — Analyze evolution results and compare with paper values.

Run after evolutions complete:
    python analyze_results.py
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import bdnk_core as bc

# Paper reference values (Table II, Table III)
PAPER_QNM_FREQ_KHZ = {'F': 2.69, 'H1': 4.55, 'H2': 6.36}  # kHz
PAPER_DECAY_RATES = {  # 1/τ at dr=0.002 (code units M☉⁻¹)
    'smallSB-F2': 0.00157,
    'medS-F2':    0.00150,
    'highB-F9':   0.00215,
    'medSB-F9':   0.00182,
}
PAPER_OMEGA_NL = 0.0834  # M☉⁻¹ (all cases)
CODE_TO_KHZ = 203.025 / (2.0 * np.pi)


def analyze_case(npz_path, case_name):
    """Full analysis of a single case."""
    d = np.load(npz_path)
    t = d['times']
    ec = d['eps_c']
    dr = float(d['dr'])
    dt = t[1] - t[0] if len(t) > 1 else 1.0

    print(f"\n{'='*60}")
    print(f"  {case_name}  (dr={dr}, t_max={t[-1]:.0f})")
    print(f"{'='*60}")

    # Basic stability
    drift = abs(ec[-1] - ec[0]) / ec[0]
    print(f"  eps_c[0] = {ec[0]:.8e}")
    print(f"  eps_c[-1] = {ec[-1]:.8e}")
    print(f"  Relative drift: {drift:.4e}")

    # PSD analysis
    ec_mean = np.mean(ec)
    ec_pert = ec - ec_mean
    freqs, psd = bc.compute_psd(ec_pert, dt)
    freq_khz = freqs * CODE_TO_KHZ

    # Find peaks in PSD
    from scipy.signal import find_peaks
    mask = freq_khz > 1.5
    if np.any(mask):
        psd_masked = psd[mask]
        freq_masked = freq_khz[mask]
        if len(psd_masked) > 5:
            peak_idx, props = find_peaks(psd_masked, height=np.max(psd_masked) * 0.01,
                                          distance=max(1, len(psd_masked) // 20))
            if len(peak_idx) > 0:
                # Sort by height
                heights = psd_masked[peak_idx]
                order = np.argsort(-heights)
                print(f"\n  PSD peaks:")
                for i, idx in enumerate(order[:5]):
                    f = freq_masked[peak_idx[idx]]
                    h = heights[idx]
                    # Match to known modes
                    mode = ""
                    for m, fref in PAPER_QNM_FREQ_KHZ.items():
                        if abs(f - fref) < 0.3:
                            mode = f" ← {m} (paper: {fref} kHz)"
                    print(f"    f = {f:.2f} kHz  (PSD = {h:.2e}){mode}")

    # Decay rate extraction (if signal long enough)
    if t[-1] >= 500:
        t_start = max(t[-1] * 0.3, 200)
        t_end = t[-1] * 0.8
        try:
            ec_filt = bc.butterworth_filter(ec_pert, dt,
                                             f_low=0.005, f_high_factor=0.05)
            rate_lin = bc.extract_decay_rate_linear(ec_filt, t, t_start, t_end)
            print(f"\n  Decay rate (linear):  1/τ = {rate_lin:.6f} M☉⁻¹")
            if case_name in PAPER_DECAY_RATES:
                ref = PAPER_DECAY_RATES[case_name]
                print(f"    Paper value (dr=0.002): {ref:.5f}")
                print(f"    Our/Paper ratio: {rate_lin/ref:.2f}")
        except Exception as e:
            print(f"  Decay rate extraction failed: {e}")

        try:
            fit = bc.extract_decay_rate_nonlinear(ec_filt, t, t_start, t_end)
            print(f"  Decay rate (nonlinear): 1/τ = {fit['decay_rate']:.6f}")
            print(f"    ω = {fit['omega']:.6f} → f = {fit['frequency_kHz']:.2f} kHz")
            print(f"    Paper ω_nl = {PAPER_OMEGA_NL:.4f} → f = {PAPER_OMEGA_NL*CODE_TO_KHZ:.2f} kHz")
        except Exception as e:
            print(f"  Nonlinear fit failed: {e}")


if __name__ == '__main__':
    data_dir = os.path.dirname(__file__)
    files = {
        'smallSB-F2': 'run_smallSB_F2.npz',
        'medS-F2':    'run_medS_F2.npz',
        'highB-F9':   'run_highB_F9.npz',
        'medSB-F9':   'run_medSB_F9.npz',
    }

    found = False
    for case_name, fname in files.items():
        fpath = os.path.join(data_dir, fname)
        if os.path.exists(fpath):
            found = True
            analyze_case(fpath, case_name)

    if not found:
        print("No evolution data found. Run the evolutions first.")

    # Multi-resolution analysis
    print(f"\n{'='*60}")
    print(f"  Multi-resolution summary")
    print(f"{'='*60}")
    for tag in ['dr0p0050', 'dr0p0080', 'dr0p0100']:
        fpath = os.path.join(data_dir, f'run_smallSB_F2_{tag}.npz')
        if os.path.exists(fpath):
            d = np.load(fpath)
            dr = float(d['dr'])
            ec = d['eps_c']
            drift = abs(ec[-1] - ec[0]) / ec[0]
            print(f"  dr={dr:.4f}: drift={drift:.4e}, t_max={d['times'][-1]:.0f}")
