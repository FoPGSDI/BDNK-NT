# Verification Report: Mathematical Derivations (Sections 1--5)

**Scope:** Sections 1 (Foundations), 2 (Ideal Gas Microphysics), 3 (Microphysics Derivatives), 4 (BDNK Conserved Currents), 5 (Hydrodynamic Frame), plus Sections 6--7 which directly use results from 1--5.

**Reference documents:**
- `/Users/hyw/Desktop/Agent/BDNK/paper.tex` (original paper)
- `/Users/hyw/Desktop/Agent/BDNK/mathematical-derivations.md` (document under verification)
- `/Users/hyw/Desktop/Agent/BDNK/progress/conventions.md` (notation conventions)

---

## 1. Summary of Findings

Overall the derivations are mathematically rigorous and correct. Out of approximately 35 distinct derivations/verifications across Sections 1--7, all final results match the paper. Two errors were found and corrected directly in the file:

1. **A dimensional/algebraic typo** in the intermediate boxed equation for the first law expansion (Section 2.2, three occurrences).
2. **A notation convention violation** using $c_1$ instead of $c_{1,\text{MIS}}$ in the MIS context (Section 7.2--7.3).

---

## 2. Derivation-by-Derivation Checklist

### Section 1: Foundations

| # | Derivation | Lines | Status | Notes |
|---|-----------|-------|--------|-------|
| 1.1 | $\Delta^{ab}$ orthogonality | 19--35 | PASS | All steps explicit and correct |
| 1.2 | $\Delta^{ab}$ idempotence | 37--63 | PASS | Four-term expansion verified |
| 1.3 | $\Delta^{ab}$ trace = 3 | 65--69 | PASS | |
| 1.4 | $X^{\langle ab\rangle}$ symmetry | 79--87 | PASS | |
| 1.5 | $X^{\langle ab\rangle}$ tracelessness | 89--103 | PASS | Correct use of idempotence |
| 1.6 | $X^{\langle ab\rangle}$ transversality | 105--111 | PASS | |
| 1.7 | Decomposition of conserved currents | 113--141 | PASS | All six projections verified for ideal fluid |
| 1.8 | Scalar Euler equation | 152--222 | PASS | Matches paper Eq. 40 |
| 1.9 | Vector Euler equation | 224--244 | PASS | Matches paper Eq. 41 |

### Section 2: Ideal Gas Microphysics

| # | Derivation | Lines | Status | Notes |
|---|-----------|-------|--------|-------|
| 2.1 | $e(\epsilon,n)$ and $T(\epsilon,n)$ | 250--294 | PASS | Matches paper Eqs. 14--15 |
| 2.2 | Entropy density $s(\epsilon,n)$ | 296--730 | PASS (with correction) | Final result correct; intermediate boxed eq at line 347 had $Ts/n$ instead of $Ts$ -- **CORRECTED** |
| 2.3 | Chemical potential $\mu(\epsilon,n)$ | 732--808 | PASS | Matches paper Eq. 18 |
| 2.4 | Thermodynamic identity | 810--880 | PASS | Matches paper Eq. 53 |

### Section 3: Microphysics Derivatives

| # | Derivation | Lines | Status | Notes |
|---|-----------|-------|--------|-------|
| 3.1 | $p'_\epsilon = \Gamma - 1$ | 886--898 | PASS | Matches paper Eq. 19 |
| 3.2 | $p'_n = -(\Gamma-1)m$ | 900--908 | PASS | Matches paper Eq. 20 |
| 3.3 | $\kappa_\epsilon$ full derivation | 910--1012 | PASS | All intermediate steps shown; matches paper Eq. 21 |
| 3.4 | $\kappa_n$ full derivation | 1014--1096 | PASS | Matches paper Eq. 22 |
| 3.5 | $\kappa_s = -(\Gamma-1)m\rho/n$ | 1098--1144 | PASS | Algebraic simplification correct |
| 3.6 | $c_s^2 = \Gamma P/\rho$ | 1146--1236 | PASS | Identity $(\partial n/\partial\epsilon)_{\bar{s}} = n/\rho$ verified from first principles |
| 3.7 | $\omega$ and $\alpha$ | 1238--1278 | PASS | Matches paper Eqs. 29--30 |

### Section 4: BDNK Conserved Currents

| # | Derivation | Lines | Status | Notes |
|---|-----------|-------|--------|-------|
| 4.1 | BDNK constitutive relations stated | 1282--1302 | PASS | Matches paper Eqs. 10--15 |
| 4.2 | $\beta_\epsilon$, $\beta_n$ for ideal gas | 1304--1332 | PASS | Matches paper Eqs. 26--27 |
| 4.3 | On-shell nature of regularizing terms | 1334--1350 | PASS | Conceptually correct |
| 4.4 | Eckart theory as BDNK limit | 1352--1448 | PASS | Detailed cancellation verified |
| 4.5 | Alternative heat flux form $\mathcal{Q}^a$ | 1450--1552 | PASS | Matches paper Eq. 55; $\gamma$ definition correct |

### Section 5: Hydrodynamic Frame

| # | Derivation | Lines | Status | Notes |
|---|-----------|-------|--------|-------|
| 5.1 | Frame ansatz and $V$, $\hat{V}$ | 1556--1586 | PASS | Matches paper Eqs. 31--33 |
| 5.2 | $\delta = 0$ identity | 1587--1627 | PASS | Clean proof using $c_s^2$ definition and $\kappa_s$ definition |
| 5.3 | $c_\pm^2$ explicit formula | 1629--1835 | PASS | Discriminant expansion verified term by term; matches paper Eq. 75 |
| 5.4 | $c_1^2 = c_s^2\eta/(V\hat{\tau})$ | 1837--1857 | PASS | Matches paper Eq. 76 |

### Section 6: Constraint Simplification (uses Section 5 results)

| # | Derivation | Lines | Status | Notes |
|---|-----------|-------|--------|-------|
| 6.1 | $\hat{B}$ rescaled form | 1867--1899 | PASS | Matches paper Eq. 67 |
| 6.2 | $\hat{D}$ rescaled form | 1901--1925 | PASS | Matches paper Eq. 67 |
| 6.3 | $\hat{E}$ rescaled form | 1927--2001 | PASS | Uses $\alpha\omega$ shortcut correctly |
| 6.4 | $\hat{C}$ rescaled form | 2003--2009 | PASS | Result stated without full derivation; verified independently matches paper |
| 6.5 | Rescaled stability constraints | 2011--2058 | PASS | |
| 6.6 | $\hat{\sigma} \leq 1/3$ bound | 2100--2144 | PASS | Analytical bound $1/2$ derived; $1/3$ sharpening correctly noted as computer-algebra result |
| 6.7 | Causality $\hat{\tau}$ bound | 2146--2288 | PASS | Matches paper Eq. 74 |

### Section 7: Equilibrium State Comparison (uses Section 4--5 results)

| # | Derivation | Lines | Status | Notes |
|---|-----------|-------|--------|-------|
| 7.1 | Baryon and energy conservation | 2291--2320 | PASS | |
| 7.2 | Eckart/BDNK/MIS equations | 2322--2364 | PASS (with correction) | $c_1 \to c_{1,\text{MIS}}$ per conventions -- **CORRECTED** |
| 7.3 | BDNK-MIS equivalence | 2366--2374 | PASS (with correction) | Same notation fix -- **CORRECTED** |
| 7.4 | Temperature frame dependence | 2376--2402 | PASS | Matches paper Eq. 43 |

---

## 3. Errors Found and Corrections Applied

### Error 1: Incorrect intermediate expression in entropy derivation (COSMETIC -- does not affect final result)

**Location:** Lines 347, 394, 397, 406, 411 of `mathematical-derivations.md`

**Description:** In the first law expansion (Section 2.2, Step 2), the boxed equation and subsequent references wrote the coefficient of $dn$ as $\frac{P - Ts/n}{mn^2}$ when it should be $\frac{P - Ts}{mn^2}$.

**Dimensional analysis:** $P$ has dimensions of [energy/volume], $Ts$ also has dimensions of [energy/volume] (since $s$ is entropy density), but $Ts/n$ has dimensions of [energy] -- dimensionally inconsistent with $P$.

**Impact:** None on the final result. The author noticed the dimensional inconsistency in the original text (see lines 420--424) and restarted the derivation at line 426 using the correct expanded form. All downstream results ($s(\epsilon,n)$, $\mu(\epsilon,n)$, etc.) are unaffected.

**Fix applied:** Changed $Ts/n$ to $Ts$ at lines 347, 394, 397, 406, 411.

### Error 2: Notation convention violation for MIS coefficient $c_1$

**Location:** Lines 2342, 2344, 2349, 2353, 2357, 2361, 2371, 2374 of `mathematical-derivations.md`

**Description:** The MIS coefficient was written as $c_1$ rather than $c_{1,\text{MIS}}$, violating the disambiguation rule in `conventions.md` (line 85): "To avoid confusion, write $c_{1,\text{MIS}}$ when referring to the MIS coefficient."

**Impact:** Potential confusion with the BDNK shear-mode characteristic speed $c_1$ defined in Section 5.3.

**Fix applied:** All occurrences of $c_1$ in the MIS context (Sections 7.2--7.3) changed to $c_{1,\text{MIS}}$.

---

## 4. Missing Steps / Recommendations

### 4.1 $\hat{C}$ Derivation (Section 6.1, line 2003)

The $\hat{C}$ rescaled shorthand is stated but its derivation is described as "follows the same pattern as above." Since this is a "no-step-skipping" document, the full derivation should be included. The intermediate computation was partially done in Section 5.3 (lines 1704--1751) where $C/A$ was computed; the remaining step to express in terms of $\tau_P, \tau_\epsilon, \tau_Q, L\hat{V}, \hat{\sigma}, \omega, \alpha$ is straightforward but should be written out.

### 4.2 Entropy derivation narrative (Section 2.2, lines 350--424)

The derivation contains a "false start" at lines 350--424 where the author attempts the computation with the (originally incorrect) boxed equation, encounters dimensional difficulties, and restarts. While the restart produces the correct result, the false start adds ~75 lines of potentially confusing material. Consider either:
- Removing the false start entirely and going directly from the corrected boxed equation to the ODE, or
- Adding a brief note explaining that the false start is retained for pedagogical reasons.

### 4.3 Reconciliation with paper's entropy form (Section 2.2, lines 592--728)

The reconciliation between the derived form $s = n[\frac{1}{\Gamma-1}\ln e + \ln(1+e) + C]$ and the paper's form $s = mn[\frac{1}{(\Gamma-1)m}\ln(e/n^{\Gamma-1}) + \text{const}]$ is somewhat lengthy and involves absorbing $n\ln\epsilon$ into the integration constant "at constant $\epsilon$." This is correct but could be streamlined.

---

## 5. Verification Method

Each derivation was verified by:
1. Checking each algebraic step follows from the previous one.
2. Cross-referencing final results against the corresponding equations in `paper.tex`.
3. Verifying dimensional consistency of intermediate expressions.
4. Checking that notation matches `conventions.md`.
5. Verifying sign conventions are consistent with the $(-+++)$ metric signature and $u_c u^c = -1$.

All paper equation references were checked against `paper.tex` using the LaTeX labels.

---

## 6. Overall Assessment

**Sections 1--5 (core scope): PASS** -- All derivations are mathematically correct. The two errors found were (1) a cosmetic typo in an intermediate expression that did not affect the final result, and (2) a notation convention violation. Both have been corrected.

The document fulfills its stated goal of providing "non-step-skipping derivations" for Sections 1--5, with the minor exception of the $\hat{C}$ rescaled shorthand in Section 6.1 where the derivation is stated rather than shown.
