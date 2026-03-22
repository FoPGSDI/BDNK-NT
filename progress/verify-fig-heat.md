# Verification Report: Heat Flow Figures (Fig 5 & Fig 6)

**Verified by:** Verification agent
**Date:** 2026-03-22
**Files reviewed:**
- `heat_stationary.pdf` (Fig 5) against `progress/figure-heat-stationary.md`
- `telegraphers_plot.pdf` (Fig 6) against `progress/figure-telegraphers.md`
- `paper.tex` lines 505--514 (Eq. simple_constraints), 550--562 (Table I), 1210--1275 (Sec. III.D text and captions)

---

## Fig 5: `heat_stationary.pdf` -- PASS

### Visual description accuracy
- **Top panel (sigma_hat = 0):** Correctly describes two vertically stacked panels. The oscillatory features near x = 0, the grayscale convention (lighter = coarser), the inset showing convergence to zero, and the 10^{-6} vertical scale all match the PDF exactly.
- **Bottom panel (sigma_hat = 1/3):** The multi-peak structure symmetric about x = 0 with dominant peaks near x ~ +-45 is accurately described. The 10^{-4} vertical scale, the inset showing tight overlap of resolution curves near x ~ 50, and the convergence to a nonzero profile are all confirmed by visual inspection.

### Parameter verification (against Table I, line 558)
| Parameter | Table I value | Analysis value | Match? |
|-----------|--------------|----------------|--------|
| Gamma | 4/3 | 4/3 | Yes |
| m | 0.1 | 0.1 | Yes |
| V_hat | 2/15 | 2/15 | Yes |
| sigma_hat | 0, 1/3 | 0, 1/3 | Yes |
| tau_hat | 1.5 | 1.5 | Yes |
| Resolutions | N = 2^7, 2^8, 2^9 | N = 2^7, 2^8, 2^9 | Yes |

### Physical interpretation
- Correctly explains that sigma = 0 implies kappa = 0 (via kappa = sigma * rho^2 / (n^2 T)), so Eq. (heat_ID_EOM) gives ddot{epsilon} = 0 and the solution is static. Matches paper lines 1226--1234.
- Correctly explains that sigma = 1/3 gives nonzero kappa, yielding genuine heat flow dynamics. Matches paper caption (line 1239).
- The convergence interpretation (numerical artifact vs. physical solution) is correct.

### Connection to theory
- Reference to Eq. (heat_ID_EOM) / Eq. 54 is correct.
- The explanation of time-symmetric initial data and baryon conservation is accurate.
- The broader context placing this figure as a prerequisite for Fig 6 (telegraphers) is appropriate.

### Errors found: None

---

## Fig 6: `telegraphers_plot.pdf` -- PASS

### Visual description accuracy
- **Left panel (t = 16):** Correctly describes nearly overlapping curves with a single central peak at T ~ 1.075--1.08. Confirmed by PDF.
- **Middle panel (t = 39):** Peak splitting for sigma_hat = 7.5 (black curve) is accurately described. The inset in the upper-right region of this panel correctly shows a small wavelike transient visible in all solutions. The description of sigma_hat = 0.15 retaining a diffusive profile and sigma_hat = 1.5 showing a slightly flattened top is consistent with the PDF.
- **Right panel (t = 312):** The oscillatory instability in the sigma_hat = 7.5 solution is accurately described. The smooth, broad decayed profiles for sigma_hat = 0.15 and 1.5 are confirmed. The extent of oscillations in the black curve (out to |x| ~ 75) matches the PDF.

### Parameter verification (against Table I, line 559)
| Parameter | Table I value | Analysis value | Match? |
|-----------|--------------|----------------|--------|
| Gamma | 4/3 | 4/3 | Yes |
| m | 0.1 | 0.1 | Yes |
| V_hat | 2/15 | 2/15 | Yes |
| sigma_hat | 0.15, 1.5, 7.5 | 0.15, 1.5, 7.5 | Yes |
| tau_hat | 1.5, 15, 75 | 1.5, 15, 75 | Yes |
| sigma_hat/tau_hat | 0.1 (constant) | 0.1 (constant) | Yes |

### Line style / legend verification
- sigma_hat = 0.15 -> light gray: matches PDF legend
- sigma_hat = 1.5 -> medium gray: matches PDF legend
- sigma_hat = 7.5 -> black (darkest): matches PDF legend

### Physical interpretation
- **Diffusive-to-wavelike transition:** Correctly explained via the telegrapher's equation (Eq. 57 / eq:heat_t_BDNK). The damping term (1/tau_epsilon) * dT/dt dominates at early times (parabolic behavior), while the wave-like principal part becomes dominant as sigma_hat and tau_hat increase. This matches the paper text (lines 1242--1257).
- **Peak splitting:** Correctly identified as the hallmark of a wave equation solution (initial pulse splits into counter-propagating components). Matches paper lines 1252--1254.
- **Inset interpretation:** Correctly notes that all solutions, including sigma_hat = 0.15, possess some wavelike behavior (finite-speed transient). This matches the paper caption and lines 1254--1257.
- **Oscillatory instability:** Correctly attributed to violation of the linear stability constraint sigma_hat <= 1/3 (Eq. simple_constraints, line 505). The note about sigma_hat = 1.5 also violating the bound but not yet showing visible instability, with the two possible explanations (slow growth rate or nonlinear stabilization), accurately reflects the paper text (lines 1266--1269).

### Connection to telegrapher's equation theory
- The modified telegrapher's equation (Eq. 57) is correctly stated.
- The wave equation limit (sigma, tau_epsilon -> infinity with c_B^2 ~ sigma/tau_epsilon finite) is correctly described, matching the paper text (lines 1246--1249).
- The ratio sigma_hat/tau_hat = 0.1 held constant to keep c_B^2 approximately constant is correctly explained.
- The hierarchy of hydrodynamic frames (Eckart -> small sigma_hat -> large sigma_hat) is a valid synthesis.
- The instability mechanism via the pressure relaxation equation (Eq. heat_x_soln) and the condition theta >= 0 is correctly referenced from the paper (lines 1210--1211).

### Errors found: None

---

## Summary

Both figure analyses are **accurate and complete**. No corrections were needed in either `figure-heat-stationary.md` or `figure-telegraphers.md`. The visual descriptions faithfully represent the PDF contents, all parameters match Table I, the physical interpretations are correct, and the connections to telegrapher's equation theory are accurate and well-supported by the paper text.
