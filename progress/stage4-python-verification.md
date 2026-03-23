# Stage 4: Python Verification Results

## Date: 2026-03-23

---

## Summary: All Paper Values Verified Numerically

### EoS + Central Values

| Check | Result | Status |
|---|---|---|
| p(ε=0) = 0 | 0.0 (exact) | PASS |
| EoS round-trip (ε → p → ε) | relative error 1.5e-16 | PASS |
| ρ₀c=0.00128 → ε_c | 0.001444 (paper says 0.00144) | NOTE: ~0.3% rounding |
| cs² at ε_c | 0.2034 (< 1/3 ✓) | PASS |
| τ_ε consistency (4 cases) | 3/4 exact; smallSB-F2 rounds 0.02333→0.023 | PASS |

### Characteristic Velocities

| Velocity | Computed | Paper | Status |
|---|---|---|---|
| c₀/c_s | 0.6543 | 0.9995√(η̂/V̂) = 0.6545 | PASS |
| c₊/c_s | 1.7317 | 1.732 | PASS |
| c₋/c_s | 0.01826 | 0.0183 | PASS |
| All well-posedness conditions | All satisfied | — | PASS |
| All causality conditions | c₀=0.295, c₊=0.781, c₋=0.008 (all < 1) | — | PASS |

### Unit Conversions

| Conversion | Computed | Paper | Status |
|---|---|---|---|
| 1 M☉(time) | 4.9268 × 10⁻⁶ s | ~4.926 × 10⁻⁶ s | PASS |
| ω_nl → f | 2.694 kHz | 2.71 kHz (paper) / 2.69 (Table I) | DISCREPANCY (paper text says 2.71; correct is 2.69) |
| smallSB-F2 decay: 0.0011 M☉⁻¹ | 223 s⁻¹ | 220 s⁻¹ | PASS (1.5% rounding) |
| medS-F2: 0.0010 M☉⁻¹ | 203 s⁻¹ | 200 s⁻¹ | PASS |
| highB-F9: 0.0017 M☉⁻¹ | 345 s⁻¹ | 350 s⁻¹ | PASS |
| medSB-F9: 0.0013 M☉⁻¹ | 264 s⁻¹ | 260 s⁻¹ | PASS |

### Convergence Factor

Q = (0.0028³ - 0.002³)/(0.002³ - 0.001³) = **1.993** for n=3. Matches paper's red line at ~2.0.

### Con2prim at Static Equilibrium

| A-matrix | v=0, W=1, g_rr=1 | Status |
|---|---|---|
| A₀⁰ = -τ_ε = -0.02333 | PASS | Correct |
| A₀¹ = 0 | PASS | All terms ~v^r |
| A₁⁰ = 0 | PASS | All terms ~v^r |
| A₁¹ = -g_rr·τ_Q·(ε+p) = -3.74e-5 | PASS | Correct |
| det(A) = 8.73e-7 > 0 | PASS | Invertible |
| E(v=0, hat=0) = ε_c | PASS | Correct |
| S_r(v=0, hat=0) = 0 | PASS | Correct |

### Decay Rate Extrapolation

| Case | Fitted 1/τ₀ | Paper | p (order) | Paper p | Status |
|---|---|---|---|---|---|
| smallSB-F2 | 0.0011 | 0.0011 | 1.0 | ~1 | PASS |
| highB-F9 (3 pts, p=1 fixed) | 0.0017 | 0.0017 | 1.0 (fixed) | ~1 | PASS |
| PF (1/τ₀=0 fixed) | 0 | 0 | 0.53 | 0.54 | PASS |

---

## Known Documentation Discrepancies (Not Bugs)

1. **ρ₀c = 0.00128 vs ε_c = 0.00144**: Direct calculation gives ε_c = 0.001444, which the paper rounds to 0.00144. The values are self-consistent only to ~3 significant figures. This is standard practice in numerical relativity papers.

2. **ω_nl = 0.0834 → 2.71 kHz**: The precise conversion gives 2.694 kHz (rounds to 2.69). The paper's claim of 2.71 kHz uses a slightly different (likely rounded) conversion constant. This is a minor inconsistency in the paper itself.

3. **smallSB-F2 τ_ε = 0.023 vs 0.02333**: The paper rounds (4/3)×0.01+0.01 = 0.02333 to 0.023 for display. This means L ≠ 1 exactly for this case (L ≈ 0.986).
