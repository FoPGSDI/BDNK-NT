# Verification: figure-convergence.md (conv_plot.pdf)

**Verified by:** Verification agent
**Date:** 2026-03-22
**Status:** PASS (no corrections needed)

---

## Checklist

### 1. Visual description vs. PDF

- [x] Two side-by-side panels: confirmed.
- [x] Left panel = shockwave, right panel = heat flow: confirmed (matches caption at paper.tex:1457).
- [x] Horizontal red dotted reference line at Q_N = 4: confirmed from the figure.
- [x] Three curves in shades of gray/black (N = 2^{11}, 2^{12}, 2^{13}): confirmed. Legend appears in the upper portion of the right panel.
- [x] Y-axis range approximately 2--8 with ticks at 2, 4, 6, 8: confirmed.
- [x] Left panel t-axis: 0 to ~400, ticks at 0, 150, 300: confirmed.
- [x] Right panel t-axis: 0 to ~450, ticks at 0, 200, 400: confirmed.
- [x] Left panel shows post-boundary oscillations with the lightest curve (N=2^{11}) overshooting to ~6--7: confirmed.
- [x] Right panel shows a dramatic near-vertical spike around t ~ 150--180: confirmed.

### 2. Q_N definition and expected values

- [x] Q_N = ||R_{N/2}|| / ||R_N||: matches eq. (convergence_factor) in paper.tex:1435--1437.
- [x] R_N is a discrete residual evaluated using an independent second-order Crank-Nicolson discretization of the t-component of the stress-energy conservation law: confirmed from the caption (paper.tex:1457).
- [x] Q_N -> 4 expected for a second-order scheme: confirmed (paper.tex:1438, "a numerical scheme that is second order in the grid spacing will have Q_N -> 4").
- [x] PDE scheme is second-order overall (Heun + WENO/CWENO, limited by second-order time integrator): confirmed (paper.tex:1452).
- [x] Contrast with ODE convergence tests (RK4, Q_N -> 16): correctly noted; Table I in paper shows Q_N approaching 16 for Bjorken flow and shockwave ODE problems.

### 3. Test cases referenced

**Left panel (shockwave):**
- [x] "Stable shockwave solution shown in the bottom panel of Fig. 3 (fig:shock_instability)": matches caption exactly.
- [x] Parameters from Table I: Gamma = 4/3, m = 0.1, V-hat = 4/3, sigma-hat = 0, tau-hat = 1.5 and 3. Analysis correctly identifies tau-hat = 3 as the stable (bottom panel) case.
- [x] w = 10: confirmed (paper.tex:1056).

**Right panel (heat flow):**
- [x] "sigma-hat = 0.15 case of the heat flow problem shown in Fig. 6 (fig:telegraphers)": matches caption exactly.
- [x] Parameters from Table I: Gamma = 4/3, m = 0.1, V-hat = 2/15, sigma-hat = 0.15, tau-hat = 1.5.
- [x] Analysis correctly notes sigma-hat/tau-hat = 0.1 and that this is the only one of the three cases satisfying the linear stability constraint.

### 4. Boundary interaction timing

- [x] Left panel: t ~ 80. Matches the figure caption ("t ~ 80 in the left panel") and is visually consistent with the PDF (deviations begin around t ~ 60--80).
- [x] Right panel: t ~ 150. Matches the figure caption ("t ~ 150 in the right panel") and is visually consistent with the dramatic spike starting around t ~ 150.
- [x] Physical mechanism (ghost cell boundary interaction with outgoing transients): correctly described, consistent with paper.tex:1452 ("significant interaction with the ghost cell boundaries") and paper.tex:1457.

---

## Minor observations (not errors)

1. The analysis says "Starting around t ~ 80-100" for the left panel degradation onset; the paper caption says "t ~ 80." The range stated is not wrong but the upper bound of 100 is slightly generous. This is within acceptable imprecision for a visual reading.

2. The analysis describes "three resolutions" as being shown. More precisely, three *convergence factor curves* Q_N are shown (each labeled by its finer resolution N), but computing all three requires solutions at four underlying resolutions (2^{10} through 2^{13}). The analysis does correctly explain the pairing mechanism in its Section 3, so this is not misleading.

3. The CFL number lambda = 0.1 stated in the analysis is confirmed by paper.tex:1452.

---

## Conclusion

The analysis in `figure-convergence.md` is accurate on all substantive points. No corrections are required.
