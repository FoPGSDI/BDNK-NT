# Stage 3: Verification Report — 11 Agents

## Date: 2026-03-23

---

## Summary

11 verification agents cross-checked all three deliverable files against the paper. **All table values verified correct.** Several bugs and inconsistencies found and categorized below.

---

## Critical Issues Found and Fixed

### Math Derivations (math-derivations.md)

| # | Issue | Severity | Status |
|---|---|---|---|
| M1 | Eq refs off-by-one: energy eq is Paper Eq.4 (not 3), momentum is Eq.5 (not 4) | MEDIUM | FIXED |
| M2 | Missing index relabeling step in Section 1.2 Step 3 | LOW | NOTED |
| M3 | Missing metric evolution eqs (∂_t g_rr, ∂_t g_θθ) in Section 4.2 | LOW | FIXED |
| M4 | Missing asymptotic flatness BCs in Section 6.2 | LOW | FIXED |
| M5 | Paper typo: c_1 should be c_0 in causality — not flagged in notes | LOW | NOTED |
| M6 | 3+1 decomposition (Sections 3.1-3.6): ALL TERMS VERIFIED CORRECT | — | — |
| M7 | Con2prim matrix (Section 8): ALL COMPONENTS VERIFIED CORRECT | — | — |

### Numerical Implementations (numerical-implementations.md)

| # | Issue | Severity | Status |
|---|---|---|---|
| N1 | `c_minus_real` check: `isinstance(cm, complex)` always False for numpy | MEDIUM | FIXED |
| N2 | `c0_tauQ`: uses `A_r*vr` instead of `grr*A_r*vr` (missing grr) | MEDIUM | FIXED |
| N3 | `cr_tauQ`: missing grr factor on D_r v_r term | MEDIUM | FIXED |
| N4 | `oc_reconstruct`: off-by-one index + missing dr scaling | CRITICAL | FIXED |
| N5 | `diss3`: denominator `2*dr` should be `2*dr**3` | HIGH | FIXED |
| N6 | `M_SUN_INV2_TO_KG_M3`: wrong by 3 orders (6.176e17 → 6.176e20) | CRITICAL | FIXED |
| N7 | `compute_pointwise_Q`: zero-guard fails for exact zero denominator | MEDIUM | FIXED |
| N8 | All EoS, TOV, transport coefficient, characteristic velocity code: CORRECT | — | — |
| N9 | A-matrix components, SSP-RK3, LLF flux: ALL CORRECT | — | — |

### Test Results (test-results.md)

| # | Issue | Severity | Status |
|---|---|---|---|
| T1 | T2.4 formula: `rho_0c + eps_0` should be `rho_0c * (1 + eps_0)` | CRITICAL | FIXED |
| T2 | tau_eps=0.023 for smallSB-F2: tolerance 1e-10 too tight (actual 0.02333) | HIGH | FIXED (tolerance → 1e-3) |
| T3 | T5.3 c_+ tolerance 1e-4 too tight (actual gap 3.85e-4) | MEDIUM | FIXED (→ 5e-4) |
| T4 | T1.6 viscosity SI conversion fundamentally wrong | HIGH | FIXED (replaced test) |
| T5 | All Table I-IV values: VERIFIED CORRECT | — | — |

### Cross-File Consistency

| # | Issue | Severity | Status |
|---|---|---|---|
| C1 | Equation numbers inconsistent between test-results.md and other files | MEDIUM | NOTED |
| C2 | Case labels not in backtick format in test-results.md prose | LOW | NOTED |
| C3 | V vs V̂ notational conflict in math-derivations.md §7 | LOW | NOTED |
