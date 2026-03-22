# Validation Cycle 1

**Date:** 2026-03-22
**Cycle Status:** PARTIAL PASS — ODE figures reproduced, PDE figures failed

## Results Summary

| Figure | Type | Status | Issue |
|--------|------|--------|-------|
| Fig 1 (Bjorken) | ODE | PASS | Fixed axis scaling (LogLogPlot → manual log transform) |
| Fig 2 (Shockwave ODE) | ODE | PASS | Fixed x-shift centering (transition was off-screen) |
| Fig 7 (Convergence ODE) | ODE | PASS | Q_N → 16 matching Table III |
| Fig 3 (Dynamic shock) | PDE | FAIL | Module::lvsym error — underscored variable names |
| Fig 4 (Acausality) | PDE | FAIL | Same as Fig 3 |
| Fig 5 (Heat stationary) | PDE | FAIL | Same as Fig 3 |
| Fig 6 (Telegrapher's) | PDE | FAIL | Same as Fig 3 |

## Derivation Verification
- 59/59 symbolic tests PASS

## Issues Found and Fixed

### Issue 1: Bjorken flow plot axis range (FIXED)
- `LogLogPlot` and `ListLogLogPlot` with `Show` auto-expanded x-axis to 10^8
- Fix: Use `ListLinePlot` with manual log10 transform + `ScalingFunctions`
- Result: Correct [1, 20] range with proper log-log scaling

### Issue 2: Shockwave ODE profile off-screen (FIXED)
- Initial delta=1e-6 at x=-5 caused transition at x≈-3.5, but plot range [-2,2] showed only right state
- Fix: Increase domain to [-8,8], find transition midpoint via FindRoot, shift x-coordinate
- Result: Smooth S-curve centered at x=0, matching paper Fig 2

### Issue 3: PDE solver Module::lvsym error (FIXED in code, not re-tested yet)
- Variable names like `dTtt_deps` invalid in Mathematica's `Module` — `_` is pattern syntax
- Fix: Rename to camelCase: `dTttDeps`, `dTtxDeps`, etc.
- Affected files: `shockwave_dynamic.wl`, `heat_flow.wl`
- Result: Code fixed, needs re-run in Cycle 2

## Actions for Cycle 2
1. Re-run `shockwave_dynamic.wl` with fixed variable names
2. Re-run `heat_flow.wl` with fixed variable names
3. Validate PDE solver is actually evolving the solution
4. Compare Figs 3-6 against paper
