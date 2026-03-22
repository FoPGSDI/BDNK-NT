# Research Diary: Analysis of "Causal, stable first-order viscous relativistic hydrodynamics with ideal gas microphysics"

**Paper:** Pandya, Most, Pretorius (2022)
**Analysis period:** 2026-03-22
**Methodology:** Multi-agent research analysis pipeline (4 stages)

---

## Stage 0: Setup and Initial Assessment

### What was done
The project began with a full reading of the paper (`paper.tex`, 1462 lines) and its bibliography (`paper.bbl`). The paper presents a first-order viscous relativistic hydrodynamics formulation (BDNK theory) applied to a relativistic ideal gas equation of state, including causality/stability constraint analysis, numerical implementation, and a comprehensive test suite. Seven PDF figures were identified for visual analysis.

A project structure was established: three main output documents (mathematical derivations, numerical implementations, test results), a progress tracking directory, and a four-stage workflow (planning, content generation, verification, finalization).

### Key decisions
- The paper's structure naturally decomposes into three complementary documents: mathematical derivations (theory), numerical implementations (methods), and test results (validation).
- A "non-step-skipping" policy was adopted for the mathematical derivations document, aiming to make every algebraic step explicit.
- A confidence tagging system ([SOLID], [PRELIMINARY], [BLOCKING]) was established for tracking the reliability of each result.

---

## Stage 1: Planning

### What was done
Four planning agents were deployed in parallel to establish conventions and create detailed outlines for each output document.

**Convention Agent:** Produced a comprehensive notation table (12 sections, ~600 lines) covering all symbols, sign conventions, coordinate systems, and equation referencing rules. A critical early decision was to adopt label-based equation references (e.g., `eq:Bjorken_EOM`) rather than equation numbers, because different agents working from different drafts of the paper produced inconsistent numbering.

**Math Derivations Plan:** Identified 35+ derivations across 10 sections, from foundational tensor algebra through Bjorken flow, shockwave ODEs, and heat flow equations.

**Numerical Implementations Plan:** Structured documentation around the two-class numerical approach (ODE/RK4 and PDE/FV+WENO+Heun), with sections for equation of state, transport coefficients, convergence testing, and practical considerations.

**Test Results Plan:** Organized 7 tests plus convergence analysis, with pass/fail criteria for each.

### Key decisions and rationale
- **Label-based equation referencing:** The convention convergence report revealed that the three plan documents used mutually inconsistent equation numbers for the same equations (e.g., the Bjorken ODE was "Eq. 35" in one, "Eq. 47" in another, and "Eq. 36" in a third). This was traced to differences in how RevTeX numbers multi-line align environments. The label-based system resolved this.
- **$c_1$ disambiguation:** The symbol $c_1$ was used for three different quantities (BDNK characteristic speed, MIS coefficient, integration constant). The convention $c_{1,\text{MIS}}$ for the MIS coefficient and $C_1, C_2$ for integration constants was established.
- **Table numbering:** The parameter table was called "Table I" by some agents and "Table II" by others (the paper has three tables, with Table I being a notation summary). Label-based references (`Table:parameters`, `Table:ODE_convergence`) were recommended.

### Issues encountered
- Significant inter-document equation numbering conflicts required the creation of a concordance table mapping labels to numbers in each document.
- Several symbols used across documents were missing from the initial conventions (e.g., $\tau_\pi$, $e_0$, $n_0$, $\tau_\theta$).
- The heat flow initial data parameters ($A, \delta, w, P_0$) were not specified anywhere in the paper, flagged as a permanent open question.

---

## Stage 2: Content Generation

### What was done
Eleven agents were deployed: four content agents (one per output document plus a convention convergence agent) and seven figure analysis agents (one per figure).

**Mathematical Derivations (~3500 lines):** Produced detailed, step-by-step derivations of all key mathematical results, organized into 10 sections: foundations (tensor algebra, projectors, Euler equations), ideal gas microphysics (EOS, entropy, chemical potential, thermodynamic identity), microphysics derivatives ($p'_\epsilon$, $p'_n$, $\kappa_\epsilon$, $\kappa_n$, $\kappa_s$, $c_s^2$, $\alpha$, $\omega$), BDNK constitutive relations, hydrodynamic frame analysis (characteristic speeds, $\delta=0$ identity), constraint simplification, equilibrium state comparison (Eckart/BDNK/MIS), Bjorken flow, shockwave ODEs, and heat flow.

**Numerical Implementations (~800 lines):** Documented all numerical methods, including EOS computation recipes, ODE integration (RK4 with pseudocode), PDE solver (conservative finite volume, WENO/CWENO, Heun time integration), initial and boundary conditions, convergence testing methodology, and practical considerations (stiffness, CFL restrictions, characteristic speed monitoring).

**Test Results (~920 lines):** Documented all 7 tests with setup, analytical expectations, key results, physical interpretations, pass/fail criteria, and associated figure descriptions. Included convergence analysis (ODE Table III reproduction and PDE convergence discussion) and a validation strategy section.

**Figure Analyses (7 files, ~200 lines each):** Each figure analysis included visual description, axes/labels, line styles, key observations, numerical/implementation notes, connection to theory, and parameter summary.

### Key decisions
- The entropy density derivation in the math document included a "false start" where the author encountered a dimensional inconsistency and restarted. This was retained rather than removed, as it pedagogically illustrates the subtlety.
- The Bjorken ODE derivation with state-dependent transport coefficients was marked [PRELIMINARY] because the full derivation with $\dot{\tau}_\epsilon$ and $\dot{\rho}$ chain-rule terms proved difficult to complete cleanly. The final boxed result was verified correct by matching the paper.
- The shockwave numerator coefficients ($c_0, \ldots, c_4$ and $d_0, \ldots, d_3$) were stated without derivation in the math document, as the algebra is "substantial but straightforward."

### Issues encountered
- The Bjorken ODE derivation with state-dependent coefficients required careful tracking of how transport coefficients change with the fluid state. Multiple false starts occurred before settling on stating the result and verifying its structure.
- The convergence figure was numbered "Fig. 7" in some documents and "Fig. 8" in others, requiring reconciliation.

---

## Stage 3: Verification

### What was done
Eleven verification agents were deployed to check every derivation, equation reference, parameter value, and cross-document consistency.

**Math verification (2 agents, covering Secs. 1--5 and 6--10):** Checked all ~55 derivations step by step. Found 2 errors in Part 1 (cosmetic entropy typo, MIS notation violation) and applied 3 fixes in Part 2 (convention violations for integration constants and equation references, confusing intermediate step). Identified 3 items needing further work (Bjorken ODE derivation, $\hat{C}$ derivation, shockwave numerator coefficients).

**Numerical implementations verification:** Found and corrected 4 errors: $J^t = n$ should be $J^t = nW$; imprecise statement about $\tau_\epsilon, \tau_P$ state dependence; wrong appendix reference; ambiguous figure numbering.

**Test results verification:** Found and corrected 2 errors: table numbering (Table I/II to Table II/III) and integration constant notation ($c_1, c_2$ to $C_1, C_2$).

**Reference verification:** Compiled the paper with pdflatex to extract definitive equation numbering from `paper.aux`. Found that 181 out of 190 equation references across all three documents were incorrect (due to the numbering discrepancy identified in Stage 1). All were corrected.

**Cross-consistency verification:** Identified 11 issues across documents, categorized by severity. The most significant were the table numbering conflict (E1) and inconsistent equation numbers (E2), both addressed by the reference verification agent. Minor issues included Greek vs. Latin index notation and missing symbol definitions.

**Figure verification (5 agents):** Verified figure analyses against the paper's actual figure captions and text descriptions.

### Corrections made
Total corrections applied: ~200 (181 equation references + 9 content fixes + assorted notation corrections).

### Issues resolved
- All equation references now use the definitive numbering from the compiled paper.
- Table numbering standardized (parameter table = Table II, convergence table = Table III).
- $c_1$ disambiguation applied throughout.
- Figure numbering reconciled (convergence plot = Fig. 7 = `fig:conv_plot`).

### Issues remaining after verification
- Bjorken ODE derivation incomplete (Sec. 8.3, [PRELIMINARY]) -- final result correct, derivation has gaps
- $\hat{C}$ derivation omitted (stated without proof, formula correct)
- Shockwave numerator coefficients not derived from first principles
- Heat flow initial data parameters unspecified in paper (permanent gap)
- Greek index notation in test-results.md line 182 (flagged but not fixed by verification agents)

---

## Stage 4: Finalization

### What was done
The final consolidation agent read all 18 source files and performed the following:

**Remaining issue fixes:**
1. Fixed the Greek index notation issue ($u_\mu u_\nu T^{\mu\nu} \to u_a u_b T^{ab}$) in test-results.md.
2. Fixed remaining $c_1 \to c_{1,\text{MIS}}$ instances in the MIS comparison equations of test-results.md (3 occurrences that the verification agents flagged but did not fix).
3. **Critical discovery and fix:** The $\hat{\tau}$ assignments for Fig. 3 (dynamic shockwave stability) were swapped in test-results.md. The document stated $\hat{\tau} = 1.5$ was the unstable case (top panel) and $\hat{\tau} = 3$ was stable (bottom panel), when in fact the reverse is true: $\hat{\tau} = 3$ gives $c_+ \approx 0.75 < v_L = 0.9$ (unstable, top panel) and $\hat{\tau} = 1.5$ gives $c_+ \approx 0.94 > v_L = 0.9$ (stable, bottom panel). This was verified against the paper's figure caption and the physics: larger $\hat{\tau}$ produces smaller $c_+$ for the $\hat{V} = 4/3$ parameter set. The error propagated to the parameter summary table and the pass/fail summary table, both of which were corrected.

**Figure analysis integration:**
All 7 figure analyses were integrated into the main documents as dedicated subsections:
- Figs. 1--6 added to their corresponding test sections in test-results.md
- Fig. 7 (convergence) added to both test-results.md Sec. 11 and numerical-implementations.md Sec. 6.6

Each integration condensed the detailed figure analysis (visual description, key observations, numerical notes) into a focused subsection within the existing test documentation, preserving the key quantitative details and physical interpretations.

**Output files created:**
- `progress/stage-progress.md` -- updated with complete status of all stages
- `progress/research-diary.md` -- this file
- `progress/final-report.md` -- executive summary for human readers

### Key decisions
- Figure analyses were condensed rather than copied verbatim, to maintain the flow of the main documents while preserving essential detail.
- The convergence figure analysis was added to both test-results.md (where it belongs as a test result) and numerical-implementations.md (where it provides critical information about the PDE solver's convergence properties).
- The swapped $\hat{\tau}$ assignments in Fig. 3 were treated as a critical fix because they affected the physical interpretation of the shockwave stability criterion (the central result of that test).

---

## Summary of the Research Analysis

### Scope
The analysis produced three comprehensive documents totaling approximately 5000 lines, covering all mathematical derivations, numerical methods, and test results from the paper. Seven figure analyses were produced and integrated. A total of ~200 corrections were applied during verification.

### Confidence assessment
- **Mathematical derivations:** All completed derivations are correct. Three derivations are incomplete (flagged as [PRELIMINARY] or omitted) but their final results are verified correct against the paper.
- **Numerical implementations:** All methods, parameters, and convergence results are accurately documented. No outstanding issues.
- **Test results:** All 7 tests are comprehensively documented with correct parameters, initial conditions, and physical interpretations. One critical error (swapped $\hat{\tau}$ assignments for Fig. 3) was found and corrected during finalization.

### Open questions
1. Heat flow initial data parameters ($A, \delta, w, P_0$) -- not specified in the paper; would require consulting the code repository.
2. Full derivation of the Bjorken ODE with state-dependent transport coefficients -- incomplete but final result verified.
3. Several implementation details deferred to Pandya (2022) reference [30] -- documented as open questions in the numerical implementations appendix.
