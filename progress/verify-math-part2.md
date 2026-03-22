# Verification Report: Mathematical Derivations (Sections 6--10)

**Verified by:** Verification Agent (Part 2)
**Date:** 2026-03-22
**Source files:**
- `/Users/hyw/Desktop/Agent/BDNK/mathematical-derivations.md` (lines 1861--3571)
- `/Users/hyw/Desktop/Agent/BDNK/paper.tex`
- `/Users/hyw/Desktop/Agent/BDNK/progress/conventions.md`

---

## Summary

Sections 6--10 of the mathematical derivations document cover constraint simplification, equilibrium state comparison, Bjorken flow, shockwave ODEs, and heat flow. The overall quality is high: the mathematics is correct in every derivation that is completed, the final boxed results match the paper, and the logical flow is sound. Two issues were found and fixed directly; several minor issues are documented below.

---

## Section-by-Section Verification Checklist

### Section 6: Constraint Simplification

| Subsection | Status | Notes |
|---|---|---|
| 6.1 Rescaled shorthand ($\hat{B}$) | PASS | Derivation correct; matches paper Eq. (rescaled_shorthand) line 1 |
| 6.1 Rescaled shorthand ($\hat{D}$) | PASS | Derivation correct; matches paper Eq. (rescaled_shorthand) line 3 |
| 6.1 Rescaled shorthand ($\hat{E}$) | PASS | First approach is messy but the second (using $\alpha\omega$) is clean and correct |
| 6.1 Rescaled shorthand ($\hat{C}$) | PASS | Stated without derivation ("follows the same pattern"); formula matches paper exactly |
| 6.2 Rescaled linear stability constraints | PASS | Rescaling algebra verified for STAB A1, A2, C; full system matches paper Eq. (rescaled_constraints) |
| 6.3 Simplification of "simple" constraints | PASS | $\lvert\hat{B}\rvert \geq \hat{D}$ and $\hat{D} - \hat{E} \geq 1 \Rightarrow \hat{D} \geq 1$ both verified |
| 6.4 The $\hat{\sigma} \leq 1/3$ bound | PASS | Algebraic derivation of $\hat{\sigma} \leq 1/(2-\alpha\omega)$ is correct; sharpening to $1/3$ deferred to computer algebra (appropriately marked PRELIMINARY) |
| 6.5 Causality constraints reduction | PASS (with fix) | CAUS A, first half of CAUS C, CAUS D all verified against paper Eq. (caus_const_simplified). See Fix #2 below. |
| 6.6 Single simplified causality inequality | PASS | Derivation of paper Eq. (fully_simplified_caus_const) from the $\sigma \to 0$ limit is correct; footnote 6 verification ($\Gamma \to 2$) is correct |

### Section 7: Equilibrium State Comparison

| Subsection | Status | Notes |
|---|---|---|
| 7.1 Baryon and energy conservation | PASS | Straightforward; matches paper |
| 7.2 Eckart, BDNK, MIS equations | PASS | All three derivations correct; MIS derivation uses $c_1$ coefficient (paper's notation for the MIS context) |
| 7.3 Equivalence of BDNK and MIS | PASS | Identification $\tau_\epsilon = \tau_\pi + c_1$ correct |
| 7.4 Temperature frame dependence | PASS | Derivation of paper Eq. (eqn:temp_frame) correct |
| 7.5 General relaxation form | PASS | Derivation of paper Eq. (exp_relax) correct; projection $u_a u_b T^{ab} = \mathcal{E}$ uses orthogonality properties correctly |

### Section 8: Bjorken Flow

| Subsection | Status | Notes |
|---|---|---|
| 8.1 Milne coordinates | PASS | Metric, Christoffel symbols, divergence $\nabla_a u^a = 1/\tau$ all correct |
| 8.2 Baryon conservation | PASS | $n(\tau) = n_0/\tau$ derivation correct |
| 8.3 Bjorken ODE | NEEDS_CORRECTION | See Issue #1 below. The final boxed result matches the paper but the derivation is incomplete |
| 8.4 Inviscid Bjorken solution | PASS | All steps verified: integrating factor, integration, final form matches paper Eq. (inviscid_bjorken) |
| 8.5 Limiting cases ($\hat{\tau} \to \infty$) | PASS (with fix) | Correct derivation; notation fix applied (see Fix #1) |
| 8.6 Pressure positivity constraint | PASS | Derivation of paper Eqs. (Pmin) and (eqn:tau_phys) correct |

### Section 9: Shockwave ODE System

| Subsection | Status | Notes |
|---|---|---|
| 9.1 Reduction to ODEs | PASS | Setup and conservation law structure correct |
| 9.2 Baryon conservation $n'(x)$ | PASS | Derivation of $n' = -W^2 n v'/v$ fully verified; intermediate algebra ($W^2 v^2 + 1 = W^2$) correct |
| 9.3 Shared denominator and characteristic speeds | PASS | Structure described correctly; explicit numerator derivation deferred (appropriately noted) |
| 9.4 Full shockwave ODE system | PASS | Matches paper Eqs. (shockwave_nprime, shockwave_epsP, shockwave_velP) |
| 9.5 Rankine-Hugoniot conditions | PASS | Matches paper Eq. (Rankine_Hugoniot) |

### Section 10: Heat Flow

| Subsection | Status | Notes |
|---|---|---|
| 10.1 Heat flow EOMs | PASS | Both $t$- and $x$-components match paper Eqs. (heat_t_eqn, heat_x_eqn) |
| 10.2 Eckart heat equation | PASS | Reduction to $\dot{T} = \alpha_E T''$ correct; sign handling verified |
| 10.3 Telegrapher's equation | PASS | All steps verified; matches paper Eq. (heat_t_hybrid) |
| 10.4 BDNK generalized telegrapher's equation | PASS | Derivation correct; $c_B^2$ and l.o.t. terms match paper Eq. (heat_t_BDNK) |
| 10.5 Pressure relaxation and stability | PASS | $\theta$ definition matches paper Eq. (heat_theta_defn); stability analysis (Eckart $\tau_\theta < 0$) correct |
| 10.6 Initial data and initial EOM | PASS | Derivation of paper Eq. (heat_ID_EOM) correct |

---

## Fixes Applied

### Fix #1: Convention Violation -- Integration Constants in Section 8.5 (line 2915)

**Problem:** The derivation used $c_1, c_2$ as integration constants, violating the conventions document (Section 1.8) which mandates $C_1, C_2$ to avoid collision with the BDNK characteristic speed $c_1$.

**Fix:** Replaced $c_1 \to C_1$ and $c_2 \to C_2$ throughout Section 8.5.

**Location:** Lines 2915--2921 of `mathematical-derivations.md`.

### Fix #2: Incorrect Equation Reference in Section 6.5 (line 2150)

**Problem:** The causality constraints were referenced as "paper Eqs. 55--58", but the paper uses labeled tags (CAUS A)--(CAUS D), not equation numbers 55--58.

**Fix:** Changed reference to "paper Eqs. CAUS A--CAUS D".

**Location:** Line 2150 of `mathematical-derivations.md`.

### Fix #3: Confusing Intermediate Step in CAUS A Derivation (lines 2161--2163)

**Problem:** The intermediate expression $\hat{\tau} > c_s^2\frac{\eta}{V/(\rho c_s^2 L)\cdot\rho c_s^2 L}$ was unnecessarily convoluted and hard to follow.

**Fix:** Rewrote the step to show the dimensionless ratio first ($c_s^2\hat{\eta}/\hat{V}$), then convert to the dimensionful form ($c_s^2\eta/V = c_s^2\eta/(\frac{4\eta}{3} + \zeta)$) matching the paper.

**Location:** Lines 2159--2165 of `mathematical-derivations.md`.

---

## Issues Not Fixed (Requiring Further Work)

### Issue #1: Bjorken ODE Derivation Incomplete (Section 8.3)

**Description:** The derivation of the Bjorken ODE (paper Eq. Bjorken_EOM) is marked [PRELIMINARY]. The document correctly states the final result and verifies its structure, but does not complete the full derivation from the conservation law with state-dependent transport coefficients. The document includes several false starts and "wait, let me try differently" passages.

**Impact:** The boxed final equation is correct (matches the paper), but the "non-step-skipping" promise of the document is not fulfilled for this derivation.

**Recommendation:** Either (a) complete the derivation by carefully tracking all $\dot{\tau}_\epsilon$ and $\dot{\rho}$ terms with the chain rule, showing that the paper's ODE is exact when transport coefficients are functions of $\epsilon(\tau)$ and $n(\tau) = n_0/\tau$; or (b) clearly state that the derivation requires treating the transport coefficients as instantaneous (frozen) and cite the paper for verification.

### Issue #2: $\hat{C}$ Derivation Omitted (Section 6.1, line 2003)

**Description:** The derivation of $\hat{C}$ is stated to follow "the same pattern" as $\hat{B}, \hat{D}, \hat{E}$ but is not explicitly shown. The formula matches the paper.

**Impact:** Minor gap. The pattern is indeed clear from the other three derivations.

**Recommendation:** Add the explicit computation for completeness, starting from $C = \tau_P(\rho c_s^2\tau_Q + \sigma\kappa_s) - \beta_\epsilon V$.

### Issue #3: Shockwave Numerator Coefficients Not Derived (Section 9.3)

**Description:** The document states the shockwave ODE numerator coefficients $c_i, d_i$ without deriving them, noting it involves "substantial but straightforward algebra."

**Impact:** Minor. The coefficients are listed in the paper and the algebra, while tedious, is indeed straightforward.

**Recommendation:** Either derive explicitly or provide a clear outline of the key steps (compute $T^{tx}$ and $T^{xx}$ for $u^a = (W, Wv, 0, 0)$, take $x$-derivatives, eliminate $n'$, solve the $2\times 2$ system).

### Issue #4: Cross-Reference Table Overlap (Appendix)

**Description:** Section 10.5 is listed as referencing "Eqs. 59--63" in the appendix cross-reference table, but Eqs. 59--61 are already covered by Sections 10.2--10.4. Section 10.5 should reference approximately "Eqs. 62--63" (the $x$-equation ODE form and the pressure relaxation result).

**Impact:** Cosmetic only.

---

## Verification Methodology

For each derivation, I performed the following checks:

1. **Equation matching:** Compared every boxed/final result against the corresponding equation in `paper.tex`, using LaTeX labels for unambiguous identification.
2. **Step-by-step algebra:** Verified all intermediate algebraic manipulations by hand, checking sign conventions, index contractions, and use of identities ($u_c u^c = -1$, $\Delta^{ab} u_b = 0$, $c_s^2 = \Gamma P/\rho$, etc.).
3. **Notation compliance:** Checked all symbols against `conventions.md`, focusing on the disambiguation of $c_1$ (characteristic speed) vs. integration constants, the use of script quantities ($\mathcal{E}, \mathcal{P}$, etc.), and the sign convention for $\kappa_\epsilon < 0$.
4. **Logical completeness:** Identified skipped steps and marked them as needing attention.
5. **Cross-consistency:** Verified that results from earlier sections (e.g., $\nabla_a u^a = 1/\tau$ from Section 8.1) are used consistently in later sections (e.g., Section 8.3).

---

## Overall Assessment

**Sections 6--10 are mathematically sound.** All completed derivations are correct, all final results match the paper, and the notation is (after fixes) consistent with conventions.md. The main gap is the incomplete Bjorken ODE derivation (Section 8.3), which is appropriately flagged as [PRELIMINARY]. The document would benefit from filling in the three omitted derivations ($\hat{C}$, Bjorken ODE, shockwave numerators), but none of the omitted results are incorrect -- they are simply not derived from first principles.
