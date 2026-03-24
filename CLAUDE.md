# BDNK Neutron Star Viscous Hydrodynamics — Derivation & Implementation Project

## Essentials

**Your role:** Take ownership of the project. Push it forward and maintain clear documentation. The human provides feedback and advice, but do not rely on them to keep track of the project—that's your job.

**Primary documents:** Three research note markdown files:
1. `math-derivations.md` — Mathematical non-step-skipping derivations
2. `numerical-implementations.md` — Numerical implementation details
3. `test-results.md` — Test results and test suite designs

All research knowledge flows into these documents. Follow the guidelines in the RESEARCH_NOTE template preamble when updating.

**Source paper:** `arXiv-2509.15303v1/Paper.tex` and `arXiv-2509.15303v1/fluids.bib` — "Neutron star evolution with BDNK viscous hydrodynamics framework" by Shum, Abalos, Bea, Bezares, Figueras, Palenzuela.

**Markers:**
- `[HYPOTHESIS]` / `[PRELIMINARY]` / `[SOLID]` — confidence levels
- `[BLOCKING: ...]` — needs human input to proceed
- `[FUTURE: ...]` — deferred, revisit later
- `(ref: source)` — evidence for claims
- `[VERIFIED]` — cross-checked against paper
- `[DISCREPANCY: ...]` — mismatch found with paper

**Session start:** Read research notes → Evaluate ("Any unmarked loose ends? Should we reframe?") → Plan next steps

**Session end** (when human says "let's end this session" or "let's wrap up"):
1. What have I done/learned in this session?
2. What existing information would I update or remove?
3. What new information would I add?
4. Would I restructure the content? If yes, how?
5. Would I revise the overall narrative? If yes, how?

Then:
- Update the research notes
- Flag [BLOCKING] items for human attention
- Commit and push changes

**When human says "memorize this":**
- Finding, decision, research knowledge → Add to research notes
- Workflow, code location, how-to → Add to Technical Notes below
- Behavior, style, preference → Add to Preferences section below

---

## Mathematical Expression Conventions

*(To be converged upon in Stage 1 — Plan Mode)*

[Convention document will be established by the convention agent and agreed upon by all agents]

---

## Preferences and Behavior

- Derivations must be **non-step-skipping**: every algebraic step must be shown explicitly
- Use LaTeX math notation in markdown ($$...$$ for display, $...$ for inline)
- All equations from the paper must be referenced by their equation numbers
- Numerical implementations should include Python code with clear comments
- Test results should compare against paper's published values
- Progress tracked in `progress/` folder

**When to seek human feedback:**
- When you are unsure about your choice
- If confident but choice involves subjectivity: proceed, mention for feedback

---

## Technical Notes

**Paper structure:**
- Section II: BDNK formulation (stress-energy tensor, 3+1 decomposition, spherical symmetry, EoS, initial data, frame choice, numerical methods)
- Section III: Numerical results (parameter choices, stable evolutions, QNM frequency, QNM decay rates)
- Appendix A: Primitive variable recovery (con2prim)
- Appendix B: Convergence tests

**Key figures (6 PDFs):**
1. `stable_evol_comparing_tau.pdf` — Fig 1: ε(r) profiles for different viscous cases at t=2000
2. `stable_evol_resolutions.pdf` — Fig 2: ε(r) across resolutions (convergence) at t=4500
3. `QNM_plot.pdf` — Fig 3: Central density oscillations + PSD spectrum (t=0–8000)
4. `casA_fitting.pdf` — Fig 4: Decay rate extraction procedure (3 panels, t=4000–5000)
5. `error_fit.pdf` — Fig 5: Decay rate vs resolution (Δr=0.002–0.0032)
6. `convergence.pdf` — Fig 6: Convergence factor Q(t) (Δr=0.001,0.002,0.0028)

**Four parameter cases:**
- `smallSB-F2`: (τ_ε, η̂, ζ̂) = (0.023, 0.01, 0.01)
- `medS-F2`: (τ_ε, η̂, ζ̂) = (0.023, 0.01725, 0)
- `highB-F9`: (τ_ε, η̂, ζ̂) = (0.092, 0.0015, 0.09)
- `medSB-F9`: (τ_ε, η̂, ζ̂) = (0.092, 0.03525, 0.045)

**Paper reference values (Tables I–III):**
- ε_c = 0.00144 M☉⁻², ρ₀c = 0.00128 M☉⁻², M_T = 1.4 M☉
- QNM frequencies: F = 2.69 kHz, H1 = 4.55 kHz, H2 = 6.36 kHz
- QNM decay rates at Δr=0.002: smallSB=0.00157, medS=0.00150, highB=0.00215, medSB=0.00182 (M☉⁻¹)
- Fitted ω_nl = 0.0834 M☉⁻¹ (all cases)
- Conversion: f_kHz = ω_code × 203.025 / (2π)

**Code files:**
- `python-numerical/bdnk_core.py` — Complete BDNK solver (~1470 lines, 13 sections)
- `python-numerical/generate_figures.py` — Figure reproduction pipeline
- `python-numerical/analyze_results.py` — QNM extraction and comparison
- `python-numerical/run_*.npz` — Saved evolution data (may be from old clamp; check timestamps)
- `figures/` — Generated figures (versions v2/v3 are latest)

**Critical numerical lesson (hat-clamp calibration):**
The first-order reduction `∂_t ε = −α ε̂` means that any CONSTANT bias in ε̂ causes LINEAR drift: Δε = α · ε̂_bias · t. The hat clamp directly controls maximum allowed bias. It must satisfy:
```
hat_eps_max × α × t_evolution ≪ ε_c
```
For t=2000, α=0.67, ε_c=0.00144: hat_eps_max ≤ 1e-9 gives drift < 0.1%.
The physical QNM ε̂ amplitude is ~7.5e-8 (from A·ω/α with A~6e-7, ω=0.084).

**Git repo:** https://github.com/FoPGSDI/BDNK-NT branch BDNK-NS
