"""
benchmark.py — Compare NumPy vs JAX solver performance.
"""
import sys, time, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np

print("=" * 70)
print("  BDNK Solver Benchmark: NumPy vs JAX (CPU)")
print("  Platform: Apple M3 Max, 48GB RAM")
print("=" * 70)

# ===== NumPy Benchmark =====
import bdnk_core as bc
print("\n--- NumPy (float64) ---")
grid_np = bc.GridData(dr=0.01, r_max=20.0, rho0c=0.00128)
U0_np = bc.build_initial_state(grid_np)
print(f"Grid: N={grid_np.N}, dr={grid_np.dr}")

_ = bc.bdnk_rhs(U0_np, grid_np, hat_eta=0.01, hat_zeta=0.01)

t0 = time.time()
for _ in range(20):
    dU = bc.bdnk_rhs(U0_np, grid_np, hat_eta=0.01, hat_zeta=0.01)
np_rhs_ms = (time.time() - t0) / 20 * 1000
print(f"Single RHS: {np_rhs_ms:.2f} ms")

t0 = time.time()
U = U0_np.copy()
dt = 0.25 * grid_np.dr
def rhs_np(state, grd):
    return bc.bdnk_rhs(state, grd, hat_eta=0.01, hat_zeta=0.01)
for _ in range(1000):
    U = bc.ssp_rk3_step(U, dt, rhs_np, grid_np)
np_1k_s = time.time() - t0
np_eps_c = U[2, 0]
np_drift = abs(np_eps_c - U0_np[2, 0]) / U0_np[2, 0]
print(f"1000 steps: {np_1k_s:.2f}s ({np_1k_s/1000*1000:.2f} ms/step)")
print(f"eps_c drift: {np_drift:.4e}")

# ===== JAX Benchmark =====
import bdnk_jax as bj
import jax
import jax.numpy as jnp
print(f"\n--- JAX (float64, CPU) ---")
print(f"JAX {jax.__version__}, backend: {jax.default_backend()}")

gd = bj.make_grid_data(dr=0.01, r_max=20.0)
U0_jax = bj.build_initial_state(gd)

# JIT warmup
dU = bj.bdnk_rhs(U0_jax, gd, hat_eta=0.01, hat_zeta=0.01)
dU.block_until_ready()

t0 = time.time()
for _ in range(100):
    dU = bj.bdnk_rhs(U0_jax, gd, hat_eta=0.01, hat_zeta=0.01)
    dU.block_until_ready()
jax_rhs_ms = (time.time() - t0) / 100 * 1000
print(f"Single RHS: {jax_rhs_ms:.3f} ms")

# SSP-RK3 warmup
dt_jax = 0.25 * 0.01
_ = bj.ssp_rk3_step(U0_jax, dt_jax, gd, hat_eta=0.01, hat_zeta=0.01)
_.block_until_ready()

# 1000 steps (Python loop)
t0 = time.time()
U = U0_jax
for _ in range(1000):
    U = bj.ssp_rk3_step(U, dt_jax, gd, hat_eta=0.01, hat_zeta=0.01)
U.block_until_ready()
jax_1k_s = time.time() - t0
jax_drift_1k = abs(float(U[2, 0]) - float(U0_jax[2, 0])) / float(U0_jax[2, 0])
print(f"1000 steps (python loop): {jax_1k_s:.2f}s ({jax_1k_s/1000*1000:.2f} ms/step)")
print(f"eps_c drift: {jax_drift_1k:.4e}")

# 10000 steps via fori_loop
from functools import partial
@partial(jax.jit, static_argnames=['n_steps', 'hat_eta', 'hat_zeta', 'hat_a', 'hat_q', 'hat_s'])
def evolve_block(U, n_steps, dt, gd, hat_eta=0.01, hat_zeta=0.01,
                 hat_a=1.0, hat_q=0.999, hat_s=1.0):
    def body(i, U):
        return bj.ssp_rk3_step(U, dt, gd, hat_eta, hat_zeta, hat_a, hat_q, hat_s)
    return jax.lax.fori_loop(0, n_steps, body, U)

_ = evolve_block(U0_jax, 100, dt_jax, gd)
_.block_until_ready()

t0 = time.time()
U = evolve_block(U0_jax, 10000, dt_jax, gd)
U.block_until_ready()
jax_10k_s = time.time() - t0
jax_drift_10k = abs(float(U[2, 0]) - float(U0_jax[2, 0])) / float(U0_jax[2, 0])
t_phys = 10000 * 0.0025
print(f"10000 steps (fori_loop): {jax_10k_s:.2f}s ({jax_10k_s/10000*1000:.3f} ms/step)")
print(f"eps_c drift: {jax_drift_10k:.4e}  (t={t_phys:.0f} M)")

# ===== Summary =====
rhs_speedup = np_rhs_ms / jax_rhs_ms
step_speedup = np_1k_s / jax_1k_s
np_10k_est = np_1k_s * 10
fori_speedup = np_10k_est / jax_10k_s
np_t2000 = np_1k_s * 800
jax_t2000 = jax_10k_s * 80

print()
print("=" * 70)
print("  SUMMARY")
print("=" * 70)
fmt = "  {:<35s} {:>12s} {:>12s} {:>10s}"
print(fmt.format("Metric", "NumPy", "JAX (CPU)", "Speedup"))
print("  " + "-" * 68)
print(fmt.format("Single RHS",
                 f"{np_rhs_ms:.2f} ms",
                 f"{jax_rhs_ms:.3f} ms",
                 f"{rhs_speedup:.1f}x"))
print(fmt.format("1000 steps",
                 f"{np_1k_s:.2f} s",
                 f"{jax_1k_s:.2f} s",
                 f"{step_speedup:.1f}x"))
print(fmt.format("10000 steps (fori_loop)",
                 f"{np_10k_est:.1f} s (est)",
                 f"{jax_10k_s:.2f} s",
                 f"{fori_speedup:.1f}x"))
print(fmt.format("Estimated t=2000",
                 f"{np_t2000/60:.1f} min",
                 f"{jax_t2000/60:.1f} min",
                 f"{np_t2000/jax_t2000:.1f}x"))
print()
print("  Note: Apple Metal GPU (M3 Max) not testable due to jax-metal")
print("  incompatibility with JAX 0.9.2. On NVIDIA GPU, expect 50-100x")
print("  speedup over NumPy.")
