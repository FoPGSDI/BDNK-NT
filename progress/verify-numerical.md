# Verification Report: Numerical Implementations Document

**File verified:** `/Users/hyw/Desktop/Agent/BDNK/numerical-implementations.md`
**Verified against:** `paper.tex` (Appendix B, lines 1433-1462; Secs. III.B-III.D; Appendix A)
**Notation cross-checked with:** `progress/conventions.md`

---

## Section-by-Section Verification Checklist

### 1. Overview (Sec. 1)
- **PASS** -- Correctly identifies two classes of numerical methods (ODE/RK4 and PDE/FV+WENO+Heun). Matches paper lines 1433-1434 and 1452.

### 2. Equation of State and Thermodynamics (Sec. 2)

#### 2.1 Gamma-Law EOS
- **PASS** -- All EOS formulas verified against paper Eqs. 8-9 and derived quantities (Eqs. 12-17). The expressions for $P, T, \rho, c_s^2, p'_\epsilon, p'_n, \kappa_\epsilon, \kappa_n, \kappa_s, \alpha, \omega$ all match the paper exactly.

#### 2.2 Transport Coefficient Computation
- **NEEDS_CORRECTION (fixed)** -- The frame definitions match paper Eq. 26 (`eq:hydro_frame`, line 464-468) exactly. The $\beta_\epsilon, \beta_n$ formulas match paper lines 430-431. **However**, the implementation note incorrectly stated that $\tau_\epsilon, \tau_P$ depend on local state. For this EOS/frame, $\tau_\epsilon = \hat{V}\hat{\tau}$, $\tau_P = 2(\Gamma-1)\hat{V}$, and $\tau_Q = \hat{V}\hat{\tau}$ are **constants** -- only $V, \sigma, \beta_\epsilon, \beta_n$ depend on local state. **Fixed in document.**

#### 2.3 Parameter Table (Table II)
- **PASS** -- All entries in the reproduced Table II match paper Table `table:parameters` (lines 550-562) exactly, including all six figure rows with their $\Gamma, m, \hat{V}, \hat{\sigma}, \hat{\tau}$ values.

#### 2.4 Recipe for Transport Coefficients
- **PASS** -- The 6-step recipe (lines 113-121) correctly translates from table parameters to transport coefficients with $L=1$.

### 3. ODE Problems (Sec. 3)

#### 3.1 Bjorken Flow
- **PASS** -- Coordinate system (Milne), metric, Christoffel symbols all match paper line 784-787.
- **PASS** -- Baryon conservation $n(\tau) = n_0/\tau$ matches paper Eq. 33 (line 791).
- **PASS** -- Bjorken EOM matches paper Eq. 35 (`eq:Bjorken_EOM`, line 795) exactly.
- **PASS** -- Reduction to first-order system is mathematically correct.
- **PASS** -- Pseudocode (lines 193-211) is logically correct and implements the EOM faithfully.
- **PASS** -- Initial conditions ($\epsilon_0 = 0.25$, $\dot{\epsilon}_0 \in \{-2,0,2\}$, $n_0 = 0.1$, $\tau \in [1,20]$) match paper lines 835-837.
- **PASS** -- Inviscid reference solution matches paper Eq. 34 (`eq:inviscid_bjorken`, line 801).

#### 3.2 Steady-State Shockwave
- **PASS** -- Four-velocity parameterization matches paper line 948.
- **PASS** -- Baryon conservation ODE $n' = -W^2 n v'/v$ matches paper Eq. 37 (`eq:shockwave_nprime`, line 954).
- **PASS** -- Shockwave ODE formulas (Eqs. 39-40) for $\epsilon'(x), v'(x)$ match paper `eq:shockwave_epsP` and `eq:shockwave_velP` (lines 974-975) exactly, including the denominators.
- **PASS** -- Characteristic speed formula $c_\pm^2 = (-B \pm \sqrt{B^2-4AC})/(2A)$ matches paper Eq. 38 (`cpmsq_general`, line 970).
- **PASS** -- Numerator coefficients $c_0, ..., c_4$ and $d_0, ..., d_3$ (Sec. 3.2.3) match paper Eq. 41 (lines 978-986) exactly.
- **PASS** -- Conserved quantities $T^{tx}, T^{xx}$ formula matches perfect fluid stress-energy.
- **PASS** -- Left asymptotic state $\{1, 0.8, 0.1\}$ matches paper lines 994-995.
- **PASS** -- Pseudocode (lines 321-353) is logically correct. The $A, B, C$ coefficients in lines 332-334 match paper Eqs. A3-A5 (`eq:A`, `eq:B`, `eq:C`, lines 1330-1332).

#### 3.3 RK4 Integration
- **PASS** -- Standard RK4 method is correctly described with proper Butcher tableau form.
- **PASS** -- Resolution range $N = 2^9$ to $2^{13}$ matches paper line 1434.
- **PASS** -- Step size formula for Bjorken flow is correct.

### 4. PDE Solver (Sec. 4)

#### 4.1 Overall Structure
- **PASS** -- Method of lines approach correctly described, matches paper line 1452.

#### 4.2 Conservative Formulation
- **NEEDS_CORRECTION (fixed)** -- The statement "$J^t = n$" was incorrect. In the BDNK theory, $J^a = nu^a$ (paper Eqs. `eq:script_N`, `eq:script_J_a`), so $J^t = nW$ where $W = (1-v^2)^{-1/2}$ is the Lorentz factor. Only when the fluid is at rest ($W = 1$) does $J^t = n$. **Fixed in document** to read "$J^t = nW$" with corresponding flux "$J^x = nWv$".

#### 4.3 WENO/CWENO
- **PASS** -- Correctly states "at most fourth-order convergent" for smooth flows. Matches paper line 1452.
- **PASS** -- Correctly notes that specifics are deferred to Pandya:2022pif.

#### 4.4 Heun's Method (TVD-RK2)
- **PASS** -- Two-stage method correctly written. The predictor-corrector form and equivalent trapezoidal form are both standard and correct.
- **PASS** -- Correctly identified as second-order, TVD, and SSP.

#### 4.5 CFL Condition and Stiffness
- **PASS** -- CFL values ($\lambda = 0.1$ default, $\lambda = 0.01$ for stiff/wildly superluminal) match paper line 1452 and lines 1127-1129.
- **PASS** -- Characteristic speed values for each $\hat{\tau}$ match paper: $\hat{\tau} = 1.5 \to c_+ \sim 0.9$ (line 1105), $\hat{\tau} = 0.5 \to c_+ \sim 1.5$ (lines 1101-1102), $\hat{\tau} = 0.4 \to c_+ \sim 1.6$ (line 1127), $\hat{\tau} = 0.25 \to c_+ \sim 2$ (line 1143).
- **PASS** -- Stiffness discussion correctly captures the paper's explanation.

### 5. Initial and Boundary Conditions (Sec. 5)

#### 5.1 Shockwave PDE Initial Data
- **PASS** -- Error function profiles match paper Eq. 46 (`eq:shockwave_ID`, lines 1031-1037) exactly, including sign conventions.
- **PASS** -- Width parameter $w = 10$ matches paper line 1056.

#### 5.2 Rankine-Hugoniot Conditions
- **PASS** -- The three jump conditions match paper Eq. 47 (`eq:Rankine_Hugoniot`, lines 1039-1045).
- **PASS** -- The numerical solutions match paper Eq. 48 (`eq:shockwave_params`, lines 1047-1052) exactly: $\{1, 0.9, 1\}_L \to \{11.5174, 0.354727, 5.44212\}_R$ and $\{1, 0.6, 1\}_L \to \{1.33795, 0.514414, 1.25027\}_R$.
- **Note:** The document uses $W_i = (1 - v_i^2)^{-1/2}$ which is the standard Lorentz factor. The paper at line 1046 writes $W_i = (1 - v_i)^{-1/2}$ (missing the square on $v_i$) -- this is a **typo in the paper**, and the document correctly uses the standard form.

#### 5.3 Heat Flow Initial Data
- **PASS** -- Gaussian temperature profile at constant pressure matches paper Eq. 53 (`eq:heat_flow_ID`, lines 1217-1218).
- **PASS** -- Conversion formulas $\epsilon = P[mT^{-1} + (\Gamma-1)^{-1}]$ and $n = PT^{-1}$ match paper line 1220.
- **PASS** -- Time-symmetric initial data $\dot{\epsilon} = \dot{u}^i = 0$ matches paper line 1220.
- **PASS** -- Initial constraint equation $\tau_\epsilon \ddot{\epsilon} - (\kappa T')' = 0$ matches paper Eq. 54 (`eq:heat_ID_EOM`, line 1224).

#### 5.4 Ghost Cells and Boundary Treatment
- **PASS** -- Correctly identifies outflow boundary conditions and convergence degradation effects. References are accurate.

### 6. Convergence Testing (Sec. 6)

#### 6.1 Convergence Factor $Q_N$
- **NEEDS_CORRECTION (fixed)** -- The convergence factor definition matches paper Eq. `eq:convergence_factor` (line 1435-1437) exactly. However, the reference was "(ref: paper Eq. A1)" which is incorrect -- the equation is in Appendix B (section `sec:numerics`), not Appendix A. **Fixed to** "(ref: paper Eq. B1, label `eq:convergence_factor`)".

#### 6.2 Richardson Expansion and Expected Rates
- **PASS** -- Correctly derives $Q_N \to 2^p$ for a $p$-th order scheme. The expected rates ($16$ for RK4, $4$ for PDE solver) are correct.

#### 6.3 Independent Residual Discretizations
- **PASS** -- The table of independent residual discretizations matches paper lines 1449 and 1457 (fourth-order centered FD for ODEs, second-order Crank-Nicolson for PDEs).

#### 6.4 ODE Convergence Results (Table III)
- **PASS** -- All numerical values in the reproduced Table III match paper `table:ODE_conv` (lines 1441-1450) exactly.
- **PASS** -- Interpretation is correct.

#### 6.5 PDE Convergence Results
- **NEEDS_CORRECTION (fixed)** -- References to "Fig. 8" were used throughout but the paper has only 7 figures (based on source counting: `fig:bjorken` through `fig:conv_plot`). The convergence figure is `fig:conv_plot`. **Fixed** all four occurrences to reference by label (`fig:conv_plot`) instead of ambiguous number.

### 7. Practical Considerations (Sec. 7)

#### 7.1 Stiffness and CFL Restrictions
- **PASS** -- Correctly reproduces the paper's stiffness discussion and CFL scaling.

#### 7.2 Characteristic Speed Monitoring
- **PASS** -- The $c_\pm^2$ formula matches paper Eq. `eq:cpmsq` (lines 1424-1427) exactly, term by term. The $c_1^2$ formula matches Eq. `eq:c1sq` (line 1429).

#### 7.3 Coordinate Systems
- **PASS** -- Correctly summarizes Cartesian and Milne usage.

#### 7.4 Ghost Cell and Boundary Effects
- **PASS** -- Correctly describes boundary interaction timing and mechanism.

#### 7.5 Second-Order-in-Time Terms
- **PASS** -- Correctly describes the handling of second-order terms for both ODE and PDE problems.

#### 7.6 Diagnostic Quantities
- **PASS** -- Correctly lists all four diagnostic quantities used in the paper.

### 8. Summary Table (Sec. 8)
- **PASS** -- All entries are consistent with the paper.

### Appendix: Open Questions
- **PASS** -- All seven items are genuine open questions that require consulting Pandya:2022pif or the code repository.

---

## Summary of Errors Found and Fixed

| # | Location | Error | Correction |
|---|----------|-------|------------|
| 1 | Line 424 (Sec. 4.2) | "$J^t = n$" is incorrect; should be $J^t = nW$ | Fixed to "$J^t = nW$" with flux "$J^x = nWv$" |
| 2 | Line 96 (Sec. 2.2) | Stated $\tau_\epsilon, \tau_P$ depend on local state | Fixed: clarified these are constants for this EOS/frame |
| 3 | Line 612 (Sec. 6.1) | "(ref: paper Eq. A1)" -- wrong appendix | Fixed to "(ref: paper Eq. B1, label `eq:convergence_factor`)" |
| 4 | Lines 602, 679, 747, 772 | "Fig. 8" references -- paper has only 7 figures | Fixed to reference by label `fig:conv_plot` |

## Missing Content

No critical content is missing. The document comprehensively covers all numerical methods, parameters, initial conditions, and convergence testing described in the paper. The items listed in the "Appendix: Open Questions" section are genuinely not available in the paper and would require external references.

One optional addition that could strengthen the document:
- The paper has a typo at line 1046 where $W_i = (1 - v_i)^{-1/2}$ is missing the square on $v_i$. The document correctly uses $W_i = (1 - v_i^2)^{-1/2}$, but could note this paper typo explicitly to prevent future confusion.

## Overall Assessment

**PASS with minor corrections (all applied).** The document is thorough, well-organized, and accurately reproduces the paper's numerical methodology. All formulas, parameters, initial conditions, convergence results, and CFL conditions have been verified against the source paper. The four errors found were all minor (incorrect conserved variable expression, imprecise implementation note, wrong appendix reference, and ambiguous figure numbering) and have been corrected directly in the document.
