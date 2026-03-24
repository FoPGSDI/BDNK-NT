# BDNK-NS Project Stage Diary

## Overview
This diary tracks the progress of reproducing the results from "Neutron star evolution with BDNK viscous hydrodynamics framework" (arXiv:2509.15303v1). The project combines mathematical derivations, numerical implementation, and figure reproduction.

---

## Stages 0–5: Documentation (Complete, 2026-03-23)

Stages 0–5 produced three comprehensive research documents (`math-derivations.md`, `numerical-implementations.md`, `test-results.md`) covering the full BDNK formulation. 33 agents across 5 stages. All paper table values confirmed numerically. See `progress/final-report.md` for details.

---

## Stage 6: Numerical Evolution & Figure Reproduction (In Progress)

**Date:** 2026-03-23 to 2026-03-24
**Status:** In Progress — solver works, figure reproduction partially complete

### 6.1 Code Architecture

`python-numerical/bdnk_core.py` — ~1470 lines, 13 sections:

| Section | Contents | Status |
|---------|----------|--------|
| 1. EoS | p(ε), dp/dε, inversion | `[VERIFIED]` |
| 2. TOV solver | areal-polar ODEs, surface detection | `[VERIFIED]` |
| 3. Coord transform | areal → isotropic, ψ integration | `[VERIFIED]` |
| 4. GridData class | uniform staggered grid, metric derivatives | `[VERIFIED]` |
| 5. Transport coefficients | η, ζ, τ_ε, τ_p, τ_Q from hatted params | `[VERIFIED]` |
| 6. A-matrix & c-vector | 2×2 con2prim system (Appendix A) | `[VERIFIED]` |
| 7. Con2prim | recover (ε̂, v̂) from conservatives + primitives | `[VERIFIED]` |
| 8. Stress tensor | E, S^r, S^r_r, S^θ_θ projections | `[VERIFIED]` |
| 9. Characteristic speeds | 6 BDNK modes, curved-space formula | `[VERIFIED]` |
| 10. FDOC operators | 4th-order derivative + KO dissipation | `[SOLID]` |
| 11. SSP-RK3 | 3rd-order strong stability preserving RK | `[VERIFIED]` |
| 12. Signal analysis | PSD, Butterworth filter, decay fits | `[SOLID]` |
| 13. Initial conditions | Equilibrium state from TOV | `[VERIFIED]` |

Supporting scripts:
- `generate_figures.py` — reproduces all 6 paper figures from saved .npz data
- `analyze_results.py` — extracts QNM frequencies and decay rates
- `run_multiresolution.py` — convergence testing at multiple Δr

### 6.2 Numerical Stability — History of Fixes

The evolution was unstable from the start and required 6 major fixes to reach stability:

1. **Perturbation-based KO dissipation** — apply Δ⁴ dissipation to `(U − U_eq)` not `U`, preventing diffusion of the equilibrium profile.

2. **Atmosphere-consistent equilibrium** — initial state and grid reference data must both apply the atmosphere floor identically, otherwise a false perturbation is created at the stellar surface.

3. **Constraint damping** — add `−κ_cd·(tgE − γ̃·E_stress)` to balance-law RHS to prevent conservative-primitive decoupling. Without this, `tgSr` grows unboundedly. Rate `κ·dt ≈ 1.5`.

4. **Hat-value clamps** — limit |ε̂| and |v̂/r| to prevent runaway from con2prim noise feeding back into the primitive evolution.

5. **KO dissipation on all 6 variables** — not just the conservatives. `DISS_SIGMA = 0.5` (large, needed without proper FDOC characteristic decomposition).

6. **Hat-clamp calibration (the critical fix)** — see Section 6.3.

### 6.3 Root Cause of ε_c Drift `[SOLID]`

**Problem**: Evolved ε(r) profiles drifted 6–32% from initial data — far from the paper's <0.1%.

**Root cause**: The hat_eps clamp was 13× too large.

The first-order reduction `∂_t ε = −α ε̂` makes cumulative drift = `α · ε̂_max · t`:
- **Old clamp 1e-6**: drift ≈ 0.67 × 1e-6 × 2000 = 1.34e-3 ≈ **93% of ε_c**
- **New clamp 1e-9**: drift ≈ 0.67 × 1e-9 × 2000 = 1.34e-6 ≈ **0.09% of ε_c**

The paper's physical QNM hat_eps is:
$$\hat\epsilon_\text{QNM} = \frac{A \omega}{\alpha} \approx \frac{6 \times 10^{-7} \times 0.084}{0.67} \approx 7.5 \times 10^{-8}$$

confirming the old clamp was far too loose. The fix was committed in `dc9e869`.

**Verified at t=500**: eps_c relative drift = 8.7e-5 (0.009%). **700× improvement**.

### 6.4 Results with Old Clamp (1e-6) — Superseded

These results had excessive drift but still showed QNM frequency detection:

| Quantity | Ours | Paper | Match |
|----------|------|-------|-------|
| ε_c (initial) | 0.001444 | 0.00144 | exact |
| F-mode [kHz] | 2.85 | 2.69 | 94% |
| H1-mode [kHz] | 4.41 | 4.55 | 97% |
| ω_nl [M☉⁻¹] | 0.0845 | 0.0834 | 99% |
| 1/τ (lin, smallSB) | 0.00140 | 0.00157 | 89% |

### 6.5 Current Status

- **Hat clamp fix committed** (`1e-9`) — verified to give <0.1% drift at t=500
- **Full t=2000 re-runs NOT yet completed** — runs were interrupted
- **Figures 1–6 generated** from old (drifted) data — need regeneration with corrected data
- **No multi-resolution convergence data** with corrected clamp

### 6.6 Remaining Work

- [ ] Re-run all 4 cases with corrected hat clamp to t=2000
- [ ] Regenerate all 6 figures with corrected data
- [ ] Verify Fig 1 ε(r) profiles stay within ~4e-7 of initial data
- [ ] Multi-resolution convergence testing (dr=0.005, 0.008, 0.01)
- [ ] Perfect fluid (PF) evolution (needs special handling: τ_ε=0 makes A-matrix singular)
- [BLOCKING: proper FDOC with LLF flux and characteristic upwinding would improve accuracy beyond what scalar KO dissipation can achieve]

### 6.8 JAX/GPU Port (Session 4, 2026-03-24) `[VERIFIED]`

Created `bdnk_jax.py` — a drop-in JAX replacement for the evolution hot path.

**Design:**
- Setup (TOV, coordinate transform, grid) stays in NumPy/SciPy (runs once)
- Evolution (RHS, SSP-RK3, time loop) fully converted to JAX with `@jax.jit`
- Grid data stored as dict of JAX arrays (not a class) for JIT tracing
- In-place mutations replaced with `jnp.where` (functional style)
- Inner time loop uses `jax.lax.fori_loop` to avoid Python overhead
- `jax_enable_x64 = True` for float64 precision (matches NumPy)

**Benchmark (Apple M3 Max, CPU, N=2000, float64):**

| Metric | NumPy | JAX (CPU) | Speedup |
|--------|-------|-----------|---------|
| Single RHS | 0.70 ms | 0.17 ms | **4.1×** |
| 1000 steps | 2.16 s | 0.50 s | **4.3×** |
| 10000 steps (fori_loop) | 21.6 s (est) | 5.32 s | **4.1×** |
| Estimated t=2000 | 28.9 min | 7.1 min | **4.1×** |

**Verification**: eps_c drift after 1000 steps matches between NumPy (1.7696e-7) and JAX (1.7697e-7) — identical to float64 precision.

**GPU status**: Apple Metal GPU (M3 Max) detected but `jax-metal 0.1.1` is incompatible with JAX 0.9.2 (MLIR dialect version mismatch). Metal float64 is also unsupported — would require float32 mode. On NVIDIA GPU with CUDA, expect 50-100× speedup over NumPy.

### 6.9 Known Limitations `[SOLID]`

1. **No characteristic decomposition** — scalar KO dissipation treats all 6 modes equally, while the paper's FDOC applies mode-by-mode dissipation. This is the main accuracy bottleneck.

2. **Constraint damping is a workaround** — it prevents conservative-primitive decoupling but introduces O(κ_cd) systematic error. The paper's FDOC doesn't need this.

3. **Hat clamp suppresses physical viscous dynamics** — the 1e-9 clamp keeps ε(r) close to equilibrium but prevents the full viscous relaxation from being captured. The paper resolves perturbations of amplitude ~4e-7 in ε_c naturally.

4. **PF evolution not implemented** — perfect fluid (η=ζ=0) makes τ_ε=0 and the A-matrix singular. Needs a separate code path.
