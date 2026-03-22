# Convention Convergence Report

## Documents Reviewed

1. `conventions.md` — Master notation and formatting conventions
2. `plan-mathematical-derivations.md` — Plan for detailed derivations
3. `plan-numerical-implementations.md` — Plan for numerical methods documentation
4. `plan-test-results.md` — Plan for test suite documentation

---

## Issues Found

### Issue 1: Conflicting Equation Numbering Systems (CRITICAL)

The three plan documents use **mutually inconsistent paper equation numbers** for the same equations. This is the most serious inconsistency found.

| Equation Content | `plan-numerical-implementations.md` | `plan-mathematical-derivations.md` | `plan-test-results.md` |
|---|---|---|---|
| Bjorken flow ODE | Eq 35 (line 795) | Eq. 47 | (not numbered) |
| Inviscid Bjorken solution | Eq 34 (line 800) | Eq. 48 | Eq. (39) |
| Large tau-hat limit | (not listed) | Eq. 49 | Eq. (40) |
| Equilibrium: Eckart/BDNK/MIS | (not listed) | Eqs. 36-45 | Eqs. (32)-(33) |
| Shockwave n'(x) | Eq 37 (line 953) | Eq. 43 | (not numbered) |
| Shockwave ODE system | Eqs 39-40 (lines 974-975) | Eqs. 47-48 | Eqs. (44)-(47) |
| Characteristic speeds c_pm | Eq 38 (line 969) | Eq. 44 | (not numbered) |
| Shockwave initial data (erf) | Eq 46 (lines 1031-1037) | (not numbered) | Eq. (50) |
| Rankine-Hugoniot conditions | Eq 47 (lines 1039-1045) | Eqs. 49-50 | (not numbered) |
| Heat flow initial data | Eq 53 (lines 1217-1220) | (below Eq. 64) | Eq. (59) |
| Thermodynamic identity | (not listed) | Eq. 53 | (not listed) |
| Telegrapher's equation | (not listed) | Eqs. 59-63 | Eqs. (53)-(55) |
| Convergence factor Q_N | Eq A1 (line 1436) | (not listed) | Eq. A6 |
| Characteristic speeds c_pm^2 | Eq A8 (lines 1424-1427) | Eq. 75 | Eqs. A12-A13 |
| Characteristic speed c_1^2 | Eq A9 (line 1429) | Eq. 76 | (not numbered) |

**Root cause:** The paper likely underwent revisions between drafts, and each plan agent may have been working from a different version of the equation numbering, or the paper.tex labels versus compiled numbering differ. The numerical-implementations plan includes paper.tex line numbers, making it the most verifiable.

**Resolution:** All documents must adopt a unified referencing scheme. The conventions.md already defines a label-based system (`eq:Bjorken_EOM`, `eq:inviscid_bjorken`, etc.) in Section 6.4. All plan documents and final outputs should use either:
- The label-based system from conventions.md (preferred), OR
- Paper equation numbers with explicit line number citations (as in plan-numerical-implementations.md) for unambiguous identification.

An equation number mapping table has been added to conventions.md (see Section 6.5 below) to resolve all ambiguity.

---

### Issue 2: Table Numbering Inconsistency (MODERATE)

The parameter table containing {Gamma, m, V_hat, sigma_hat, tau_hat} per figure is called:
- **"Table II"** in `plan-numerical-implementations.md` (e.g., line 30: "Table II, line 554")
- **"Table I"** in `plan-test-results.md` (e.g., line 31: "Parameters from Table I (Fig. 1)")
- **"Table II"** in `conventions.md` (line 501: "From paper Table II")

Similarly, the ODE convergence results table is called:
- **"Table III"** in `plan-numerical-implementations.md` (lines 177, 185, 302, 336)
- **"Table II"** in `plan-test-results.md` (lines 59, 221, 274, 306-307)

**Resolution:** Use the label-based convention to avoid ambiguity. Added to conventions.md: the parameter table is `Table:parameters` and the convergence table is `Table:ODE_convergence`. When citing by number, cite with the paper.tex line reference for disambiguation.

---

### Issue 3: Missing Symbols in conventions.md (MODERATE)

Several symbols used across the plan documents are not formally defined in conventions.md Section 1 (Notation Table):

| Symbol | Used in | Meaning | Status in conventions.md |
|---|---|---|---|
| `tau_pi` | test-results (line 20), math-derivations (Sec. 8.5), conventions Sec. 10 | MIS relaxation time | Used in equations (Sec. 10) but missing from notation table (Sec. 1) |
| `pi^{ab}_{NS}` | conventions Sec. 10 | Navier-Stokes viscous tensor | Used in MIS equation but never defined |
| `I^{ab}` | conventions Sec. 10 | MIS higher-order terms | Used in MIS equation but never defined |
| `e_0` | numerical-impl (line 96), math-derivations (Sec. 9.4), test-results (line 33) | Integration constant in inviscid Bjorken solution | Missing entirely |
| `c_1` (MIS context) | math-derivations (Sec. 8.5, line 339), conventions Sec. 10 (line 562) | MIS coefficient (NOT the BDNK characteristic speed) | Conflicts with `c_1` defined in Sec. 1.6 as BDNK characteristic speed |
| `tau_theta` | math-derivations (Sec. 11.7) | Pressure relaxation timescale | Missing from conventions |
| `alpha_E` | conventions Sec. 4.3, math-derivations (Sec. 11.4) | Eckart thermal diffusivity | In heat flow shorthands but not in main notation table |
| `n_0` | numerical-impl (lines 28, 93), math-derivations (Sec. 9.2) | Initial baryon density for Bjorken flow | Missing from notation table |
| `epsilon_0`, `dot{epsilon}_0` | numerical-impl (line 91-92) | Initial energy density and its derivative | Missing from notation table |

**Resolution:** Added missing symbols to conventions.md (see updates below).

---

### Issue 4: Symbol Collision for `c_1` (MODERATE)

The symbol `c_1` is used for three different quantities across the documents:

1. **BDNK characteristic speed**: `c_1^2 = c_s^2 eta/(V tau_hat)` (conventions.md Sec. 1.6, math-derivations Sec. 6.3)
2. **MIS coefficient**: appears in `tau_epsilon = tau_pi + c_1` (conventions.md Sec. 10, test-results line 20, math-derivations Sec. 8.5)
3. **Generic integration constant**: `epsilon = c_1 tau^{-1} + c_2` in the large-tau_hat Bjorken limit (math-derivations Sec. 9.5, test-results line 34)

**Resolution:** Added a disambiguation note to conventions.md. The BDNK characteristic speed remains `c_1`. The MIS coefficient should be written as `c_{1,\text{MIS}}` or kept in context with explicit reference to MIS. Integration constants should use `C_1, C_2` instead of `c_1, c_2` to avoid collision.

---

### Issue 5: Figure Numbering Inconsistency (MINOR)

The convergence plot figure is called:
- **"Fig 8"** in `plan-numerical-implementations.md` (lines 159, 180, 192, 303)
- **"Fig. 7"** in `plan-test-results.md` (lines 227, 255, 275)
- **"fig:conv_plot"** in `conventions.md` (line 477), listed as the 7th figure

Also, the superluminal shockwave figure:
- `plan-numerical-implementations.md` references "Fig 5" for CFL reduction (line 80) and for left states (lines 107-108)
- `plan-test-results.md` calls the same content "Fig. 4" (acaus_instab.pdf, line 82) and a different test "Fig. 5" (heat_stationary.pdf, line 108)

**Resolution:** Use the label-based figure references from conventions.md Section 8.1 (`fig:conv_plot`, `fig:acaus_instab`, etc.) to avoid ambiguity. The figure count in conventions.md lists 7 figures, matching plan-test-results.md.

---

### Issue 6: Structural Overlap Between Documents (MINOR)

**Overlapping coverage:**
- Convergence testing methodology appears in both `plan-numerical-implementations.md` (Sec. 5) and `plan-test-results.md` (Sec. 3.4, 5.2). Both describe Q_N, residual discretizations, and expected rates.
- Parameter tables appear in all three plan documents: conventions.md Sec. 8.3, numerical-implementations Sec. 6.3, and test-results Sec. 6.1-6.2.
- EOS and transport coefficient definitions appear in both conventions.md and numerical-implementations Sec. 2.

**Resolution:** This overlap is acceptable since each document serves a different purpose. However, all should cross-reference conventions.md as the single source of truth for notation and definitions. The conventions.md already contains the authoritative parameter table (Sec. 8.3). Final documents should reference it rather than duplicating.

---

### Issue 7: Structural Gap — Heat Flow Parameters (MINOR)

The numerical-implementations plan (Sec. 3.5, item 4 in Open Questions) notes that the heat flow initial data parameters (A, delta, w, P_0 in the Gaussian profile) are not specified anywhere in the planning documents or conventions.md. These values may only exist in the code.

**Resolution:** Flag as an open question. Added a note to conventions.md Section 8.3 acknowledging this gap.

---

## Summary of Changes Made to conventions.md

1. **Section 1.7 (Miscellaneous)**: Added missing symbols: `tau_pi`, `pi^{ab}_{NS}`, `I^{ab}`, `e_0`, `n_0`, `epsilon_0`, `tau_theta`, `C_1`/`C_2` (integration constants).

2. **Section 1.6 (Characteristic Speeds)**: Added disambiguation note for `c_1` vs the MIS coefficient and integration constants.

3. **Section 6.5 (NEW)**: Added an equation number concordance table mapping label-based references to the paper equation numbers used by each plan document, with paper.tex line numbers as the ground truth.

4. **Section 8.3**: Added a note about missing heat flow parameters.

---

## Recommendations for Content Generation Agents

1. **Always use label-based equation references** (e.g., `eq:Bjorken_EOM`) as the primary identifier. When citing a paper equation number, include the paper.tex line number for disambiguation.

2. **Never use `c_1` as an integration constant.** Use `C_1, C_2` instead.

3. **When referring to `c_1` in the MIS context**, write `c_{1,\text{MIS}}` or provide explicit context.

4. **Use `Table:parameters`** and **`Table:ODE_convergence`** labels rather than "Table I" or "Table II" to avoid the numbering conflict.

5. **For figure references**, always use the label from conventions.md Section 8.1 (e.g., `fig:bjorken`, `fig:conv_plot`).

6. **For convergence testing content**, treat `plan-numerical-implementations.md` as authoritative for method details and `plan-test-results.md` as authoritative for result interpretation and pass/fail criteria.
