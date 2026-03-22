# Verification: Figure Analysis for Bjorken Flow (figure-bjorken.md)

**Status: PASS WITH CORRECTIONS**

**Verified against:** bjorken_plot.pdf (visual inspection), paper.tex (lines 460-940, especially caption at 932-938 and discussion at 835-930)

---

## Summary

The analysis is thorough, well-structured, and largely accurate. The physical interpretation, parameter values, numerical notes, and connection to theory are all correct and well-supported by the paper. However, several factual inaccuracies were found in the visual description of the bottom panel and in the figure numbering. These have been corrected in the analysis file.

---

## Verification Checklist

### 1. Figure Number
- **CORRECTED.** The analysis stated "Fig. 5" but `fig:bjorken` is the first `\begin{figure}` environment in paper.tex (line 932). It is Fig. 1, not Fig. 5.

### 2. Top Panel Visual Description
- **PASS.** The description of nine black curves (three families of three, solid/dash-dot/dotted) plus one thick red dashed reference line is accurate. The steep downward plunges and convergence behavior are correctly described. The legend items (V-hat=0, tau-hat=0.5/1/2) match the figure exactly.

### 3. Top Panel Axes
- **PASS (minor note).** The x-axis extends slightly beyond tau=20 (to about 30), not "approximately 20" as stated, but the integration domain is [1,20] per the paper. This is a minor visual detail.

### 4. Line Styles and Legend
- **PASS.** All line styles (solid, dash-dot, dotted for tau-hat = 0.5, 1, 2) and colors (red dashed for inviscid, black for viscous, blue dashed for Eckart) match the figure exactly.

### 5. Characteristic Speed Values
- **PASS.** The values c_+ ~ 1.3 (tau-hat=0.5), c_+ ~ 1.05/0.9 (tau-hat=1), c_+ ~ 0.7 (tau-hat=2) are verbatim from the paper (lines 847-851).

### 6. Bottom Panel Visual Description
- **CORRECTED.** Multiple inaccuracies were found:
  - (a) The y-axis range was stated as "approximately -0.3 to 2" but the figure shows a range from about -0.6 to about 2.2.
  - (b) The BDNK and Eckart curves for a single initial condition are NOT visually adjacent "pairs" at early times. For epsilon_dot_0 = -2, the BDNK curve starts at T=0.5 and drops to negative, while its Eckart partner starts at T ~ 1.8 (the highest blue curve). For epsilon_dot_0 = 2, the BDNK curve starts at T=0.5 and rises to ~1.6, while its Eckart partner starts at T ~ -0.8. The curves for a single IC cross other curves extensively.
  - (c) The statement "The bottom pair shows negative temperatures throughout the displayed domain" is incorrect. For the epsilon_dot_0 = -2 solution, the BDNK temperature starts positive (T=0.5) before plunging negative, and the Eckart temperature starts at ~1.8 before decaying.
  - (d) "The upper pair of curves starts near T ~ 0.6" is only accurate for the epsilon_dot_0 = 0 pair where both BDNK and Eckart give T ~ 0.5 initially.

### 7. Parameter Values
- **PASS.** All parameter values (Gamma=4/3, m=1, V-hat=1/10, sigma-hat=0, tau-hat in {0.5,1,2}, L=1, epsilon_0=0.25, epsilon_dot_0 in {-2,0,2}, n_0=0.1) match Table I and the text of the paper exactly.

### 8. Derived Quantities
- **PASS.** All derived quantities at initial time are correctly computed:
  - P(1) = (1/3)(0.25-0.1) = 0.05
  - rho(1) = 0.30
  - c_s^2(1) = 2/9
  - tau_epsilon values for each tau-hat: 0.05, 0.10, 0.20
  - tau_P = 1/15
  - V(1) = 1/150

### 9. Equations of Motion
- **PASS.** The Bjorken ODE (Eq. 62), inviscid solution, transport coefficient definitions, and first-order system reformulation are all correctly transcribed from the paper.

### 10. Physical Interpretation
- **CORRECTED (Section 4.5).** The claim that the epsilon_dot_0 = -2 solution "has negative temperature throughout the displayed domain in both the BDNK frame and the Eckart frame" was incorrect. The BDNK curve starts at T = 0.5 (positive) before plunging negative, and the Eckart curve starts at T ~ 1.8 (the highest value in the plot) before decaying to negative. This was corrected to state that the solution "develops negative temperature at intermediate and late times." All other key observations (universal attractor, relaxation time effect, superluminal characteristics, stiffness, frame dependence) and theory connections are correct.

### 11. Inviscid Reference Curve
- **PASS.** The computation m*n_0*(Gamma-1)/tau^2 = 1/(30*tau^2) is correct.

### 12. Eckart Temperature Computation
- **PASS.** The procedure (compute T^{tau tau}, identify as epsilon_E, use EOS) matches the paper's description at lines 915-921.

---

## Corrections Applied

The following corrections were made to figure-bjorken.md:
1. Figure number changed from "Fig. 5" to "Fig. 1"
2. Bottom panel y-axis range corrected from "-0.3 to 2" to "-0.6 to 2.2"
3. Bottom panel visual description (Section 1) rewritten to accurately reflect the non-trivial BDNK/Eckart curve pairing and crossing behavior, with per-IC breakdown
4. Section 4.5 corrected: the epsilon_dot_0 = -2 solution does NOT have negative T "throughout" -- both BDNK and Eckart start positive before going negative
