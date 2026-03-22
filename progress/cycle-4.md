# Validation Cycle 4

**Date:** 2026-03-22
**Cycle Status:** IN PROGRESS — Fig 7 fixed, Fig 6 fix applied and running

## Results Summary

| Figure | Type | Status | Notes |
|--------|------|--------|-------|
| Fig 1 (Bjorken) | ODE | PASS | Cycle 1 |
| Fig 2 (Shockwave ODE) | ODE | PASS | Cycle 1 |
| Fig 3 (Dynamic shock) | PDE | PASS (qual.) | Cycle 3 |
| Fig 4 (Acausality) | PDE | PASS (qual.) | Cycle 3 |
| Fig 5 (Heat stationary) | PDE | PASS | Cycle 2 |
| Fig 6 (Telegrapher's) | PDE | RUNNING | Bug fixed, evolution running |
| Fig 7 (Convergence) | PDE | PASS | Cycle 4 — real PDE data, Q_N ≈ 4 |

## Fixes Applied in Cycle 4

### Fix 1: Fig 7 — Replace fake convergence with real PDE runs
- Old code used model functions `qModelShock`, `qModelHeat` (fake data)
- New code runs actual PDE solver at 3 resolutions (N=32, 64, 128)
- Uses self-convergence: Q_N = ||eps_coarse - eps_medium|| / ||eps_medium - eps_fine||
- Results: Q_N ≈ 3.5-3.8 (approaching 4 = 2nd order convergence)

### Fix 2: Fig 6 — Missing spatial derivative evolution terms
- Diagnosed: computeRHS was missing dx(dtEps), dx(dtV), dx(dtN) contributions
- These terms arise because T^{tt} depends on dxV (through divergence) and T^{tx} depends on dxEps, dxN (through beta coefficients)
- Fix: compute numerical Jacobians dT/d(dxEps), dT/d(dxV), dT/d(dxN) and add their contributions to the implicit solve
- Diagnostic confirmed: σ̂=0.15 has diffusion timescale ~5800 (T barely changes over t=312 — physically correct), σ̂=7.5 has timescale ~116 (should show more dynamics)

## Current Status
- heat_flow.wl running with fix applied
- σ̂=0.15 case evolving slowly (expected — very small thermal conductivity)
- Waiting for σ̂=7.5 case to confirm peak-splitting behavior
