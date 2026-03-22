# Verification: `figure-acaus-instab.md`

**Verified by:** Claude (verification agent)
**Date:** 2026-03-22
**Status:** PASS -- no corrections needed

---

## 1. Visual Description vs. PDF

The figure analysis accurately describes both panels.

- **Top panel:** Two line styles (dotted for t=0, solid for t=1582) with a smooth transition from v~0.6 to v~0.515. The solid line is steeper/narrower than the dotted initial data. All three tau-hat values (0.4, 0.5, 1.5) overlap completely. Confirmed against the PDF.
- **Bottom panel:** Three line styles (dotted t=0.27, dot-dash t=0.31, solid t=0.36) showing progressive instability growth. The growing bump near x~10-20 and the sharp dip near x~40-50 are both correctly described. The solid-line (t=0.36) bump overshoots v~0.6 and the dip drops below v~0.5, consistent with the analysis estimate of v~0.49.
- **Inset:** Correctly described as showing five resolutions (N = 2^7 through 2^11) in increasingly dark shades of gray, with convergence toward a well-defined sharp spike.
- **Axes:** x in [-100, 100], v ticks at 0.5 and 0.6. Both panels share the x-axis label. Confirmed.

## 2. Parameters vs. Paper

All parameters verified against the caption (lines 1140-1144) and body text (lines 1096-1138):

| Parameter | Analysis | Paper | Match? |
|-----------|----------|-------|--------|
| tau-hat values (top) | 0.4, 0.5, 1.5 | 0.4, 0.5, 1.5 | Yes |
| tau-hat (bottom) | 0.25 | 0.25 | Yes |
| c+ for tau-hat=1.5 | ~0.9 | ~0.9 | Yes |
| c+ for tau-hat=0.5 | ~1.5 | ~1.5 | Yes |
| c+ for tau-hat=0.4 | ~1.6 | ~1.6 | Yes |
| c+ for tau-hat=0.25 | ~2 | ~2 | Yes |
| CFL for tau-hat=0.4 | 0.01 | 0.01 (caption) | Yes |
| CFL for tau-hat>=0.5 | 0.1 | "order of magnitude" larger (caption) | Yes |
| Resolutions in inset | {2^7,...,2^11} | {2^7,...,2^11} (caption) | Yes |
| Left-state (eps,v,n) | (1, 0.6, 1) | (1, 0.6, 1) at line 1099 | Yes |

**Minor note:** The CFL value of 0.01 for tau-hat=0.25 (in the analysis table 5.1) is not explicitly stated in the paper. This is a reasonable inference but should be understood as such. The paper says only that "a very fast instability sets in at early times" for this case.

## 3. Physical Interpretation

All interpretations verified against the paper body text:

- **Weakly superluminal frames produce no issues:** Confirmed (lines 1100-1107). The analysis correctly notes that solutions are identical at plot resolution but converge to slightly different continuum solutions.
- **No superluminal signal propagation:** Confirmed (lines 1115-1118). The bump propagates downstream at the sound speed, not superluminally.
- **Wildly superluminal instability:** Confirmed (lines 1133-1134). Unbounded growth of the bump and finite-time divergence of time derivatives are both described in the paper.
- **No unphysical state variables:** Confirmed (line 1134). The paper explicitly lists c_s, c_pm, T^{ta}, epsilon, P, n as remaining physical.
- **Stiffness analogy to Bjorken flow:** Confirmed in the caption.
- **Connection to linear stability proof:** Confirmed (line 1137).
- **Recommendation for |c+|=1:** Confirmed (line 1123).

## 4. Numerical Notes

- **Convergence in inset:** The analysis correctly interprets the inset as showing convergence toward a continuum PDE feature. The paper states the same at line 1134: "behavior appear to be indicating convergence."
- **Scheme description:** Pandya et al. (2022) finite volume, Heun's method (TVD-RK2), WENO/CWENO -- consistent with the numerical methods described elsewhere in the paper.
- **Domain x in [-100, 100], width w=10:** Confirmed from paper line 1098.

## 5. Verdict

The figure analysis in `figure-acaus-instab.md` is accurate and thorough. No corrections are required. The only minor caveat is that the CFL number for the tau-hat=0.25 case (listed as 0.01 in table 5.1) is inferred rather than explicitly stated in the paper, but this does not constitute an error -- the analysis table correctly notes that the instability develops regardless of time step size.
