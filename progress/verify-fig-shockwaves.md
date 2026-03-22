# Verification: Shockwave Figure Analyses

**Verified by:** Verification agent
**Date:** 2026-03-22
**Files checked:**
- `/Users/hyw/Desktop/Agent/BDNK/progress/figure-shockwave.md` (Fig 2, `shockwave_plot.pdf`)
- `/Users/hyw/Desktop/Agent/BDNK/progress/figure-shock-instability.md` (Fig 3, `shock_instability.pdf`)
- `/Users/hyw/Desktop/Agent/BDNK/paper.tex` (lines 550--562 Table I, 992--1012 discussion, 1014--1094 captions)

---

## Figure 2: Steady-State Shockwave Profiles (`shockwave_plot.pdf`)

### Visual description vs. PDF
- **PASS.** Axes (x from -2 to 2, f(x) from 0 to ~4.5), line styles (solid = epsilon, dash-dot = v, dotted = n), and colors (black = ideal gas, green = conformal) all match the PDF.
- **PASS.** The qualitative descriptions of monotonic transitions (epsilon and n increasing, v decreasing left-to-right) match the PDF.
- **CORRECTED (Sec. 4.3).** The original analysis claimed the conformal (green) velocity curve "starts at a somewhat lower left-state value for v compared to the ideal gas." This contradicts the paper caption (line 1022--1024), which explicitly states both use the same asymptotic left state {epsilon, v, n} = {1, 0.8, 0.1}. The PDF confirms both v curves asymptote to v_L = 0.8 on the left. The green dash-dot curve in fact sits very slightly above the black one on the far left. The analysis has been corrected.

### Parameters vs. paper Table I (line 555)
- **PASS.** Gamma = 4/3, m = 0.1, V_hat = 2/15, sigma_hat = 0, tau_hat = 1.5 all match Table I row for `fig:shockwave_profile`.
- **PASS.** Left state {epsilon_L, v_L, n_L} = {1, 0.8, 0.1} matches the caption (line 1023--1024) and discussion (line 994--995).

### Physical interpretations
- **PASS.** The connection between shockwave existence and the condition v_L < c_+ is correctly described and matches the paper discussion (lines 1006--1012).
- **PASS.** The comparison with the conformal (green) sharply causal frame is correctly attributed to Pandya & Pretorius 2021.
- **PASS.** The explanation that viscous corrections vanish at asymptotic states (where constants of integration T^{tx}, T^{xx} are evaluated) is correct.

### Numerical notes
- **PASS.** ODE system description, RK4 solver, convergence factor Q_N -> 15.9 (close to 16 for fourth-order), and residual check via T^{tx}_{,x} = 0 are all consistent with the paper's Appendix.
- **Minor note.** The analysis states "resolutions up to N = 2^13 gridpoints." This refers to the convergence test (Table ODE_conv), not necessarily the resolution used for the plot itself. Not an error, but worth noting.

### Verdict: PASS (after correction to Sec. 4.3)

---

## Figure 3: Shock Instability (`shock_instability.pdf`)

### Visual description vs. PDF
- **CORRECTED (figure number).** The original analysis stated "Fig. 8." The correct figure number is Fig. 3 (third `\begin{figure}` in the paper). Fixed.
- **CORRECTED (top panel y-axis).** The original analysis stated the vertical range as "[0.4, 1.0] approximately." The PDF tick marks read 0.5, 0.7, 0.9, giving a range of approximately [0.5, 0.9]. Fixed.
- **PASS.** Top panel: velocity plateau at v_L = 0.9 on the left, violent oscillatory instability at the shock front near x = 0, dotted c_+ line at ~0.75, inset with three resolutions showing non-convergent oscillations, smooth downstream bump near x ~ 10--20. All match the PDF.
- **PASS.** Bottom panel: smooth monotonic shock profile, v_L = 0.9 to v_R ~ 0.35, dotted c_+ line at ~0.94, three resolutions indistinguishable, t = 372, tau_hat = 1.5. All match the PDF.
- **PASS.** Horizontal axis range [-50, 50] with ticks at -40, -20, 0, 20, 40 matches the PDF.
- **PASS.** Legend placement and labeling (N = 2^9, 2^10, 2^11 with light-to-dark shading) correctly described, appearing in the bottom panel.

### Parameters vs. paper Table I (line 556)
- **PASS.** Gamma = 4/3, m = 0.1, V_hat = 4/3, sigma_hat = 0, tau_hat = 1.5 and 3 all match Table I row for `fig:shock_instability`.
- **PASS.** Left state {1, 0.9, 1}_L -> right state {11.5174, 0.354727, 5.44212}_R matches Eq. shockwave_params (line 1049).
- **PASS.** Transition width w = 10 matches the text (line 1056).

### Physical interpretations
- **PASS.** The instability criterion (v > c_+) is correctly identified as the central message. The connection between ODE singularity (denominators vanishing when v crosses c_+) and dynamical instability is correctly stated and matches the paper discussion (lines 1060--1076).
- **PASS.** The attribution to Freistuhler (2021) for the rigorous conformal result is correct.
- **PASS.** The discussion of c_- crossings (Sec. 6.3 of the analysis) correctly reflects the paper's cautious treatment (lines 1078--1088), noting that c_- crossings require violating causality/stability constraints and are left to future work.

### Numerical notes
- **PASS.** Initial data formulas (Eq. 46 / shockwave_ID) match the paper (lines 1031--1037).
- **PASS.** Rankine-Hugoniot conditions match the paper (lines 1039--1044). Note: the analysis writes W_i = (1 - v_i^2)^{-1/2}, which is the standard Lorentz factor. The paper text at line 1046 has W_i = (1 - v_i)^{-1/2} (missing the square on v_i), which appears to be a typo in the paper itself. The analysis has the physically correct formula.
- **PASS.** RK4 solver and resolution values (N = 512, 1024, 2048) are correctly stated.

### Verdict: PASS (after corrections to figure number and top-panel y-axis range)

---

## Summary of Corrections Made

| File | Section | Issue | Fix Applied |
|------|---------|-------|-------------|
| `figure-shockwave.md` | 4.3 | Incorrectly claimed green v curve starts lower than black; both share the same v_L = 0.8 | Rewritten to state both share the same left-state velocity |
| `figure-shock-instability.md` | Header | Figure labeled "Fig. 8" instead of "Fig. 3" | Changed to "Fig. 3" |
| `figure-shock-instability.md` | Sec. 2 table | Top panel y-axis range listed as [0.4, 1.0] | Corrected to [0.5, 0.9] |

## Additional Note

The paper itself appears to have a minor typo at line 1046: `W_i = (1 - v_i)^{-1/2}` should be `W_i = (1 - v_i^2)^{-1/2}`. Both analysis files correctly use the physically correct Lorentz factor formula with v_i^2.

**Overall status: Both analyses VERIFIED with minor corrections applied.**
