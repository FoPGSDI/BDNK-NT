# PDF Figure Analyses — Stage 2

## Figure 1: stable_evol_comparing_tau.pdf

**Description:** Radial profile ε(r) comparing initial data with late-time (t=8000 M☉) configurations for all four viscous cases at Δr=0.002 M☉.

**Key quantitative findings:**
- Central ε(r=0) initial: ~0.001445 M☉⁻²
- Central ε(r=0) late time: ~0.0014432 M☉⁻² (all cases)
- Absolute drift at center: ~2–6 × 10⁻⁷ M☉⁻² (~0.01–0.04% of ε_c)
- Stellar radius: r* ~ 8.0–8.2 M☉
- Spread among four viscous cases: ~10⁻⁷ M☉⁻² (~0.007% of ε_c)

**Implementation notes:**
- Atmosphere threshold: p < κρ₀,atms^Γ (ρ₀,atms = 10⁻¹²)
- Minimum characteristic speed floor 0.1c stabilizes atmosphere
- Staggered grid avoids r=0 singularity
- Secular drift is numerical dissipation, not physical instability
- Frame-dependent deviations (F2 vs F9) are genuine physical effects

**Stability conclusion:** All four cases maintain equilibrium over t=8000 M☉ with only truncation-error-level deviations. Confirms stability of BDNK evolution in restricted parameter space.

---

## Figure 2: stable_evol_resolutions.pdf

**Description:** ε(r) for `smallSB-F2` at t=4500 M☉ across resolutions Δr = [0.001, 0.002, 0.0032] M☉.

**Key quantitative findings:**
- Total spread across resolutions at center: ~3 × 10⁻⁷ M☉⁻² (~0.02% of ε_c)
- Ordering: Δr=0.001 closest to initial data, Δr=0.0032 furthest
- Surface profile perfectly converged across all resolutions
- Gap between finest two resolutions < gap between coarsest two (convergent behavior)

**Implementation notes:**
- Non-uniform resolution ratios (1:2:3.2) require careful convergence analysis
- Surface inset shows resolution-independent atmosphere treatment
- End time t=4500 (shorter than 8000) reduces accumulated dissipation

**Convergence conclusion:** Qualitative convergence demonstrated — errors decrease monotonically with resolution at ~O(10⁻⁴) relative accuracy.

---

## Figure 3: QNM_plot.pdf

**Description:** Two panels — top: ε_c(t) for PF, smallSB-F2, highB-F9; bottom: PSD with Blackman window.

**Key quantitative findings (top panel):**
- PF shows secular drift ~4 × 10⁻⁷ M☉⁻² over 7500 M☉
- BDNK cases plateau by t~1500–3000 M☉ at ε_c ~ 0.0014432
- highB-F9 settles fastest (~1000–1500 M☉), smallSB-F2 by ~2000–3000 M☉
- Oscillations visible only for t ≲ 1000 M☉

**Key quantitative findings (bottom panel):**
- F-mode: ~2.65–2.70 kHz (consistent across all cases)
- H1: ~4.45–4.50 kHz; H2: ~6.35–6.40 kHz
- H1/H2 suppression in BDNK vs PF: ~10–30× in PSD
- FFT resolution: ~25 Hz (raw), ~76 Hz (with Blackman)
- Nyquist: ~101.5 kHz (no aliasing concern)

**Implementation notes:**
- Sampling: Δt = 1 M☉, N = 8000 points
- Blackman window essential to suppress spectral leakage from secular drift
- Negative troughs flanking peaks are Blackman sidelobe artifacts
- PF larger PSD may partly reflect secular-drift contamination

---

## Figure 4: casA_fitting.pdf

**Description:** Three-panel decay rate extraction for `smallSB-F2`.

**Key quantitative findings:**
- Fitting window: t ∈ [4000, 5000] M☉
- ~13 oscillation cycles in window (period ~75 M☉)
- Linear fit slope: 1/τ_l = 0.00157 M☉⁻¹
- Nonlinear fit: 1/τ_nl = 0.00157 M☉⁻¹, ω_nl = 0.0834 M☉⁻¹
- Fit-data agreement: visually indistinguishable

**Implementation notes:**
- Butterworth: order 4, bandpass [0.01, 0.1] M☉⁻¹
- Use `filtfilt` for zero-phase filtering
- Peak extraction: find peaks on |ε̃_c| first, then log
- Nonlinear fit: 5 parameters (A, τ, ω, φ₀, C); use Fourier ω as initial guess
- Window independence: vary start time by ±200 M☉, verify <5% change

---

## Figure 5: error_fit.pdf

**Description:** Decay rate vs resolution for `smallSB-F2` and PF (×10).

**Key quantitative findings:**
- smallSB-F2: monotone from 0.0016 (Δr=0.002) to 0.0019 (Δr=0.0032) M☉⁻¹
- PF×10: from 0.0018 to 0.0023 (steeper, sub-linear)
- Error bars: ±0.00001–0.00002 (BDNK), ±0.00003–0.00005 (PF)
- Extrapolated: 1/τ₀ = 0.0011 M☉⁻¹ = 220 s⁻¹ (smallSB-F2)
- Convergence order: p=1 (BDNK), p=0.54 (PF)
- highB-F9 uses only 3 highest resolutions

**Implementation notes:**
- Two-tier data: 3-sig-fig raw measurements → 2-sig-fig averaged for fit
- PF: 1/τ₀ = 0 fixed explicitly (no physical dissipation)
- Extrapolation curve NOT shown in figure
- PF p=0.54 reflects breakdown of single-mode assumption

---

## Figure 6: convergence.pdf

**Description:** Two panels — top: ε_c(t) at three resolutions; bottom: convergence factor Q(t).

**Key quantitative findings:**
- Resolutions: Δr = 0.0028, 0.002, 0.001 M☉ (case: smallSB-F2)
- Theoretical Q = (0.0028³ - 0.002³)/(0.002³ - 0.001³) = **1.993 ≈ 2.0**
- Transient duration: ~300–400 M☉
- Asymptotic Q: ~1.97–1.99 (slightly below theoretical)
- Top panel: monotone convergence with Δr=0.001 closest to initial data

**Implementation notes:**
- Non-commensurate time steps require cubic spline interpolation
- Cubic spline order 4 > scheme order 3 (required for valid convergence test)
- Early-time spikes in Q from near-zero denominator — skip first ~100 M☉
- y-axis clipped to [1.78, 2.28] to suppress early spikes
- Use exact resolution values (not approximations) in Q formula
