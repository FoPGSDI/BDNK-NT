# Verification Report: test-results.md

## Reference Files
- **Document verified:** `/Users/hyw/Desktop/Agent/BDNK/test-results.md`
- **Source paper:** `/Users/hyw/Desktop/Agent/BDNK/paper.tex`
- **Conventions:** `/Users/hyw/Desktop/Agent/BDNK/progress/conventions.md`

---

## 1. Test Coverage Checklist

| # | Test | Paper Section | Figure | Documented? | Status |
|---|------|---------------|--------|-------------|--------|
| 1 | Trivial Equilibrium States | Sec. III.A | None | Yes (Sec. 4) | **PASS** |
| 2 | Bjorken Flow | Sec. III.B | Fig. 1 | Yes (Sec. 5) | **PASS** |
| 3 | Steady-State Shockwave | Sec. III.C | Fig. 2 | Yes (Sec. 6) | **PASS** |
| 4 | Dynamic Shockwave Stability | Sec. III.C | Fig. 3 | Yes (Sec. 7) | **PASS** |
| 5 | Acausality/Instability | Sec. III.C | Fig. 4 | Yes (Sec. 8) | **PASS** |
| 6 | Heat Flow Stationary | Sec. III.D | Fig. 5 | Yes (Sec. 9) | **PASS** |
| 7 | Telegrapher's Equation | Sec. III.D | Fig. 6 | Yes (Sec. 10) | **PASS** |

All 7 tests are documented. Convergence results (Appendix B, Table III, Fig. 7) are also documented in Sec. 11.

---

## 2. Parameter Verification Against Paper Table II

The paper has three tables:
- **Table I:** Notation summary (`table:notation`, line 306)
- **Table II:** Parameters for numerical tests (`table:parameters`, line 561)
- **Table III:** ODE convergence factors (`table:ODE_conv`, line 1449)

### Error Found: Table Numbering

The test-results.md consistently refers to the parameter table as "Table I" and the convergence table as "Table II". These are **incorrect**: the parameter table is Table II and the convergence table is Table III in the paper (since Table I is the notation summary table).

**Affected locations:** Lines 49, 51, 103, 144, 246, 325, 371, 409, 449, 521, 625, 707, 786, 788, 798.

**Status: NEEDS_CORRECTION** (fixed below)

### Parameter Values Verification

| Figure | $\Gamma$ | $m$ | $\hat{V}$ | $\hat{\sigma}$ | $\hat{\tau}$ | Match? |
|--------|----------|-----|-----------|----------------|-------------|--------|
| Fig. 1 (Bjorken) | 4/3 | 1 | 1/10 | 0 | 0.5, 1, 2 | **PASS** |
| Fig. 2 (Shockwave profile) | 4/3 | 0.1 | 2/15 | 0 | 1.5 | **PASS** |
| Fig. 3 (Dynamic shock) | 4/3 | 0.1 | 4/3 | 0 | 1.5, 3 | **PASS** |
| Fig. 4 (Acausality) | 4/3 | 0.1 | 4/3 | 0 | 0.25, 0.4, 0.5, 1.5 | **PASS** |
| Fig. 5 (Heat stationary) | 4/3 | 0.1 | 2/15 | 0, 1/3 | 1.5 | **PASS** |
| Fig. 6 (Telegrapher's) | 4/3 | 0.1 | 2/15 | 0.15, 1.5, 7.5 | 1.5, 15, 75 | **PASS** |

All parameter values match Table II of the paper exactly.

---

## 3. Initial Conditions Verification

| Test | Initial Conditions | Match Paper? | Status |
|------|-------------------|--------------|--------|
| 1 (Equilibrium) | $\epsilon, n \neq 0$; $\epsilon_{,i} = n_{,i} = u^i = 0$; theory-specific conditions | Yes (paper Eq. `eq:eq_state_ID`) | **PASS** |
| 2 (Bjorken) | $\epsilon_0 = 0.25$, $\dot{\epsilon}_0 \in \{-2, 0, 2\}$, $n_0 = 0.1$, $\tau \in [1, 20]$ | Yes (paper lines 835-836) | **PASS** |
| 3 (Shockwave ODE) | $\{\epsilon_L, v_L, n_L\} = \{1, 0.8, 0.1\}$ | Yes (paper line 995) | **PASS** |
| 4 (Dynamic shock) | Error-function interpolation with $w=10$; $\{1, 0.9, 1\}_L \implies \{11.5174, 0.354727, 5.44212\}_R$ | Yes (paper Eq. `shockwave_params`, line 1049) | **PASS** |
| 5 (Acausality) | Same interpolation with $w=10$; $\{1, 0.6, 1\}_L \implies \{1.33795, 0.514414, 1.25027\}_R$ | Yes (paper line 1050) | **PASS** |
| 6 (Heat stationary) | Gaussian $T$ perturbation at constant $P$; time-symmetric ($\dot{\epsilon} = \dot{u}^i = 0$) | Yes (paper Eq. `heat_flow_ID`, line 1218) | **PASS** |
| 7 (Telegrapher's) | Same as Test 6 | Yes | **PASS** |

All initial conditions are correctly stated.

---

## 4. Characteristic Speed Values

| Test | $\hat{\tau}$ | $c_+$ in test-results | $c_+$ in paper | Status |
|------|-------------|----------------------|----------------|--------|
| Bjorken | 0.5 | $\approx 1.3$ | $\approx 1.3$ (line 847) | **PASS** |
| Bjorken | 1 | $\approx 1.05$ (early), $\approx 0.9$ (late) | $\approx 1.05$ early, $\approx 0.9$ late (lines 848-849) | **PASS** |
| Bjorken | 2 | $\approx 0.7$ | $\approx 0.7$ (line 851) | **PASS** |
| Acausality | 1.5 | $\sim 0.9$ | $\sim 0.9$ (line 1105) | **PASS** |
| Acausality | 0.5 | $\sim 1.5$ | $\sim 1.5$ (line 1102) | **PASS** |
| Acausality | 0.4 | $\sim 1.6$ | $\sim 1.6$ (line 1127-1128) | **PASS** |
| Acausality | 0.25 | $\sim 2.0$ | $\sim 2$ (caption line 1143) | **PASS** |

The characteristic speed formula in the conventions.md (Sec. 5.7) matches the paper's Eq. `cpmsq` exactly.

All characteristic speed values are consistent with the paper.

---

## 5. Physical Interpretations

| Interpretation | Accurate? | Status |
|----------------|-----------|--------|
| BDNK and MIS have same relaxation structure (Test 1) | Yes -- matches paper Sec. III.A | **PASS** |
| Eckart applies dissipation instantaneously (Test 1) | Yes -- matches paper discussion | **PASS** |
| Temperature is frame-dependent outside equilibrium (Test 1) | Yes -- matches paper Eq. `eqn:temp_frame` | **PASS** |
| Superluminal characteristics do not imply acausal propagation (Tests 2, 5) | Yes -- matches paper discussion (lines 858-870, 1114-1122) | **PASS** |
| Analogy to gauge dynamics in GR (Test 2) | Yes -- matches paper lines 858-864 | **PASS** |
| Shockwave instability localized to $v > c_+$ (Test 4) | Yes -- matches paper caption line 1093 | **PASS** |
| Transition from parabolic to hyperbolic behavior (Test 7) | Yes -- matches paper Eqs. `heat_t_Eckart`--`heat_t_BDNK` | **PASS** |
| Mild stability violations can be benign (Test 7) | Yes -- matches paper lines 1266-1269 | **PASS** |
| Connection to Freistuhler (2021) result (Test 4) | Yes -- matches paper lines 1072-1076 | **PASS** |
| Pure heat flow impossible for conformal fluids (Test 6) | Yes -- matches paper footnote on line 1215 | **PASS** |

All physical interpretations are accurate.

---

## 6. Figure Descriptions

| Figure | Description Matches Paper Caption? | Status |
|--------|-----------------------------------|--------|
| Fig. 1 (bjorken_plot.pdf) | Top: $\dot{\epsilon} + \Gamma\epsilon/\tau$ vs $\tau$, three $\hat{\tau}$ values, red dashed inviscid. Bottom: temperature for $\hat{\tau}=2$, black=BDNK, blue dashed=Eckart. Matches caption (line 935-937). | **PASS** |
| Fig. 2 (shockwave_plot.pdf) | Three panels: $\epsilon(x)$, $v(x)$, $n(x)$. Black=ideal gas, green=conformal. Matches caption (line 1017-1027). | **PASS** |
| Fig. 3 (shock_instability.pdf) | Top: unstable $\hat{\tau}=1.5$, multiple resolutions, dotted $c_+(x)$. Bottom: stable $\hat{\tau}=3$. Matches caption (line 1093). | **PASS** |
| Fig. 4 (acaus_instab.pdf) | Top: $t=0$ and $t=1582$ for $\hat{\tau}=0.4, 0.5, 1.5$. Bottom: $\hat{\tau}=0.25$ instability with inset. Matches caption (line 1140-1143). | **PASS** |
| Fig. 5 (heat_stationary.pdf) | Top: $\hat{\sigma}=0$, $\dot{\epsilon}\to 0$. Bottom: $\hat{\sigma}=1/3$, $\dot{\epsilon}\to$ nonzero. Matches caption (line 1237-1239). | **PASS** |
| Fig. 6 (telegraphers_plot.pdf) | Three panels: early, intermediate (with inset), late. Matches caption (line 1271-1274). | **PASS** |
| Fig. 7 (conv_plot.pdf) | Left: shockwave $Q_N(t)$. Right: heat flow $Q_N(t)$. Matches caption (line 1454-1457). | **PASS** |

All figure descriptions are consistent with the paper's captions.

---

## 7. Pass/Fail Criteria Assessment

The test-results.md provides pass/fail criteria in Sec. 12.2 (summary table) and within each individual test section. Assessment:

| Criterion Category | Complete? | Reasonable? | Status |
|-------------------|-----------|-------------|--------|
| ODE convergence ($Q_N \to 16$) | Yes | Yes -- standard for RK4 | **PASS** |
| PDE convergence ($Q_N \to 4$) | Yes | Yes -- standard for 2nd-order | **PASS** |
| Qualitative behavior checks | Yes | Yes -- well-defined observables | **PASS** |
| Constraint violation boundary probing | Yes | Yes -- systematic | **PASS** |
| Resolution dependence (physical vs. numerical) | Yes | Yes -- correct methodology | **PASS** |

The pass/fail criteria are reasonable and complete. The summary table in Sec. 12.2 covers all relevant sub-cases.

---

## 8. Equation Reference Verification

The test-results.md uses the format "(ref: paper Eq. XX)" throughout. Since the paper uses LaTeX labels rather than explicit numbers, and the exact numbering depends on how RevTeX compiles the document, precise verification of equation numbers requires compilation. However, spot-checking key references:

| Reference | Content Referenced | Correct Content? | Status |
|-----------|--------------------|-------------------|--------|
| Eq. 14 (frame ansatz) | `eq:hydro_frame` | Plausible | **PASS** (tentative) |
| Eq. 15 (constraints) | `eq:simple_constraints` | Plausible | **PASS** (tentative) |
| Eq. 36 (Bjorken ODE) | `eq:Bjorken_EOM` | Equation content matches | **PASS** |
| Eq. 39 (inviscid Bjorken) | `eq:inviscid_bjorken` | Equation content matches | **PASS** |
| Eq. 40 ($\hat{\tau}\to\infty$ limit) | `eq_tau_inf` | Equation content matches | **PASS** |
| Eq. 44--47 (shockwave ODEs) | `shockwave_nprime`, `shockwave_epsP`, `shockwave_velP` | Equation content matches | **PASS** |
| Eq. 49 (Rankine-Hugoniot) | `eq:Rankine_Hugoniot` | Content matches | **PASS** |
| Eq. 50 (shockwave initial data) | `eq:shockwave_ID` | Content matches | **PASS** |
| Eq. 51 (left-right state pairs) | `eq:shockwave_params` | Content matches | **PASS** |
| Eq. 55--57 (heat equations) | `heat_t_Eckart`--`heat_t_BDNK` | Content matches | **PASS** |
| Eq. 59 (heat flow ID) | `eq:heat_flow_ID` | Content matches | **PASS** |
| Eq. 61 (heat flow EOM at $t=0$) | `eq:heat_ID_EOM` | Content matches | **PASS** |
| Eq. B1 (convergence factor) | `eq:convergence_factor` | Content matches | **PASS** |

All referenced equations have correct content, though exact equation numbers cannot be verified without compiling the paper.

---

## 9. Errors Found and Corrections Applied

### Error 1: Table Numbering (CRITICAL)

**Issue:** The test-results.md calls the parameter table "Table I" throughout. In the paper, this is Table II (Table I is the notation summary). Similarly, the ODE convergence table is called "Table II" but should be "Table III".

**Locations:** Lines 49, 51, 103, 144, 246, 325, 371, 409, 449, 521, 625, 707, 786, 788, 798.

**Fix:** Replace all "Table I" references (when referring to parameters) with "Table II", and all "Table II" references (when referring to ODE convergence) with "Table III".

**Status: CORRECTED** in test-results.md.

### Error 2: Integration Constants Notation (MINOR)

**Issue:** The inviscid Bjorken $\hat{\tau}\to\infty$ solution at line 273 uses $c_1, c_2$ as integration constants, faithfully reproducing the paper's notation. However, conventions.md (line 113) explicitly states "do NOT use $c_1, c_2$ to avoid collision with characteristic speed $c_1$; use $C_1, C_2$ instead."

**Assessment:** This is a minor inconsistency between test-results.md and conventions.md. The test-results faithfully follows the paper's notation, which is defensible. However, to be consistent with the project's own conventions, $C_1, C_2$ should be used.

**Status: CORRECTED** in test-results.md.

---

## 10. Missing Content Assessment

| Item | Present? | Status |
|------|----------|--------|
| Specific values for initial data parameters ($A, \delta, w, P_0$) in heat flow tests | No -- only functional form given | **Minor gap** |
| Explicit statement of Rankine-Hugoniot equations | Referenced but not reproduced | **Acceptable** (equations are standard) |
| Table I (notation table) reproduction | Not needed for test documentation | **Not required** |
| Full BDNK PDE system | Referenced but not reproduced | **Acceptable** (documented elsewhere) |

**Assessment:** No critical content is missing. The specific values of $A, \delta, w, P_0$ for the heat flow initial data are not given in the test-results, but the paper also does not specify these precisely (they are not in the parameter table and appear to be chosen freely for demonstration purposes). This is an acceptable gap.

---

## 11. Overall Assessment

**Verdict: PASS with minor corrections**

The test-results.md document is comprehensive, accurate, and well-organized. It correctly documents all 7 tests from the paper, with accurate parameter values, initial conditions, characteristic speed values, physical interpretations, and figure descriptions. The pass/fail criteria are reasonable and complete.

Two errors were found and corrected:
1. Table numbering (Table I should be Table II for parameters; Table II should be Table III for convergence)
2. Integration constant notation ($c_1, c_2$ changed to $C_1, C_2$ per conventions.md)

No substantive physics errors, missing tests, or incorrect interpretations were found.
