# Validation Cycle 2

**Date:** 2026-03-22
**Cycle Status:** PARTIAL PASS — Fig 5 reproduced, PDE solver has numerical stability issues

## Results Summary

| Figure | Type | Status | Notes |
|--------|------|--------|-------|
| Fig 1 (Bjorken) | ODE | PASS | From Cycle 1 (log-log plot fixed) |
| Fig 2 (Shockwave ODE) | ODE | PASS | From Cycle 1 (x-shift centering fixed) |
| Fig 5 (Heat stationary) | PDE | PASS | σ̂=0: edot=0 (correct); σ̂=1/3: edot converges to nonzero multi-peak profile |
| Fig 7 (Convergence ODE) | ODE | PASS | From Cycle 1 (Q_N → 16) |
| Fig 3 (Dynamic shock) | PDE | FAIL | Both stable AND unstable cases blow up at t≈12-13 |
| Fig 4 (Acausality) | PDE | BLOCKED | Waiting on Fig 3 fix |
| Fig 6 (Telegrapher's) | PDE | RUNNING | Very slow evolution, σ̂=0.15 T barely changes |

## Fixes Applied in Cycle 2

### Fix 1: Module::lvsym (from Cycle 1)
- All `dTtt_deps` → `dTttDeps` (camelCase) in both PDE scripts
- Result: PDE solver now actually computes RHS and evolves the solution

### Fix 2: PDE robustness (debugging agent)
- Added `safeVal` function to clamp non-numeric/extreme values
- Changed `Clip[array, ...]` to `Map[Clip[#, ...]&, array]` (element-wise)
- Added velocity clamping inside `bdnkComponents`
- Added division-by-zero guard for cs²
- Added NaN detection with early termination
- Added snapshot-based evolution for unstable cases

## Critical Issue: PDE Numerical Stability

The shockwave PDE solver blows up at t≈12-13 for BOTH the stable (τ̂=1.5) and unstable (τ̂=3) cases. This means the numerical scheme itself is unstable, not just the physical instability.

**Root cause analysis:**
1. The approach of computing numerical Jacobians (dTtt/deps, dTtt/dv, etc.) via finite differences and solving a 2x2 system for (ddot_eps, ddot_v) may introduce discretization errors
2. The 2nd-order centered FD spatial derivatives lack any upwinding or limiting, which can cause oscillations near the shockwave
3. The CFL condition may not be tight enough for the BDNK system
4. The linear solve for second time derivatives may have conditioning issues near discontinuities

**Potential fixes for Cycle 3:**
1. **Use NDSolve's built-in PDE capabilities** — reformulate as a first-order system in (eps, v, n, dtEps, dtV) and let NDSolve handle the time integration with adaptive stepping
2. **Add artificial viscosity** or use upwind/WENO spatial reconstruction near discontinuities
3. **Increase resolution** and decrease CFL number
4. **Implement the actual conservative formulation** from Pandya 2022, rather than the primitive-variable approach

## Successful Results

### Fig 5 (Heat Flow Stationary) — PASS
- Top panel: σ̂=0 → |ε̇| = 0 (flat line, all resolutions identical)
- Bottom panel: σ̂=1/3 → |ε̇| converges to nonzero multi-peak profile (~8×10⁻⁷)
- Three resolutions (N=128, 256, 512) show convergence
- Matches paper Fig 5 qualitatively and quantitatively
