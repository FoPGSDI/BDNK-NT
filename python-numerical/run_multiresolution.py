"""
run_multiresolution.py — Run smallSB-F2 at multiple resolutions for convergence testing.

Produces data for Figs 2, 5, 6.
"""
import sys, time, warnings, os
sys.path.insert(0, os.path.dirname(__file__))
import bdnk_core as bc
import numpy as np
warnings.filterwarnings('ignore')

# Paper uses dr = [0.001, 0.002, 0.0024, 0.0028, 0.0032]
# We use coarser resolutions due to computational cost
RESOLUTIONS = [0.005, 0.008, 0.01]
T_END = 2000.0
HAT_ETA = 0.01
HAT_ZETA = 0.01

for dr in RESOLUTIONS:
    tag = f"dr{dr:.4f}".replace('.', 'p')
    fname = f"run_smallSB_F2_{tag}.npz"
    fpath = os.path.join(os.path.dirname(__file__), fname)

    if os.path.exists(fpath):
        print(f"[{tag}] Already exists, skipping.")
        continue

    print(f"[{tag}] Building grid dr={dr}, r_max=20...")
    t0 = time.time()
    grid = bc.GridData(dr=dr, r_max=20.0, rho0c=0.00128)
    U0 = bc.build_initial_state(grid)

    dt_save = max(1.0, dr * 100)  # save less frequently for fine grids
    print(f"[{tag}] N={grid.N}, evolving to t={T_END}, dt_save={dt_save}...")

    times, states = bc.evolve(grid, U0, t_end=T_END,
                               hat_eta=HAT_ETA, hat_zeta=HAT_ZETA,
                               dt_save=dt_save)

    times = np.array(times)
    eps_c = np.array([s[2, 0] for s in states])
    eps_final = states[-1][2]

    elapsed = time.time() - t0
    drift = abs(eps_c[-1] - eps_c[0]) / eps_c[0]
    print(f"[{tag}] Done in {elapsed:.0f}s. drift={drift:.3e}")

    np.savez(fpath,
             times=times, eps_c=eps_c,
             r=grid.r, eps_bg=grid.eps_bg,
             eps_final=eps_final,
             dr=dr)
    print(f"[{tag}] Saved {fname}")

print("\nAll resolutions complete.")
