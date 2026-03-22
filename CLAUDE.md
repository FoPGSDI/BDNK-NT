# BDNK Viscous Relativistic Hydrodynamics — Research Analysis

## Essentials

**Your role:** Take ownership of the project. Push it forward and maintain clear documentation. The human provides feedback and advice, but do not rely on them to keep track of the project — that's your job.

**Primary documents:** Three research note files:
1. `mathematical-derivations.md` — Non-step-skipping mathematical derivations
2. `numerical-implementations.md` — Numerical methods, algorithms, and implementation details
3. `test-results.md` — Test results, test suite designs, and convergence analysis

All research knowledge flows into these documents. Follow the guidelines in the notes preamble when updating.

**Markers:**
- `[HYPOTHESIS]` / `[PRELIMINARY]` / `[SOLID]` — confidence levels
- `[BLOCKING: ...]` — needs human input to proceed
- `[FUTURE: ...]` — deferred, revisit later
- `(ref: paper Eq. XX)` — evidence for claims, referencing paper equations

**Session start:** Read research notes → Evaluate ("Any unmarked loose ends? Should we reframe?") → Plan next steps

**Session end** (when human says "let's end this session" or "let's wrap up"):

Answer these questions in order, then update the notes accordingly:
1. What have I done/learned in this session (or since last update)?
2. What existing information would I update or remove?
3. What new information would I add?
4. Would I restructure the content of the notes? If yes, how?
5. Would I revise the overall narrative of the notes? If yes, how?

Then:
- Update the research notes
- Flag [BLOCKING] items for human attention
- Commit and push changes

**When human says "memorize this":**
- Finding, decision, research knowledge → Add to research notes
- Workflow, code location, how-to → Add to Technical Notes below
- Behavior, style, preference → Add to Preferences section below

---

## Preferences and Behavior

- Mathematical notation: Follow conventions established in `progress/conventions.md`
- Use LaTeX-style math in markdown (dollar-sign delimiters)
- Paper reference: Pandya, Most, Pretorius (2022) — "Causal, stable first-order viscous relativistic hydrodynamics with ideal gas microphysics"
- GitHub repo: https://github.com/FoPGSDI/BDNK-NT (BDNK-hydro-sim branch)

**When to seek human feedback:**
- When you are unsure about your choice
- If you are confident but the choice involves subjectivity: proceed with your choice, but mention it to the human for feedback afterward

---

## Technical Notes

**Paper structure:**
- Sec I: Introduction — history of relativistic viscous hydro (Eckart → MIS → BDNK)
- Sec II: Model — gradient expansion, BDNK conserved currents, ideal gas microphysics, hydrodynamic frame
- Sec III: Results — equilibrium states, Bjorken flow, shockwaves, heat conduction
- Appendix A: Deriving suitable hydrodynamic frames (stability + causality constraints)
- Appendix B: Numerical algorithms and convergence tests

**Key equations to track:**
- EOS: Eq (14) — gamma-law P = (Γ-1)mn·e
- BDNK currents: Eqs (7)-(13)
- Transport coefficients: Eq (28)
- Constraints: Eq (29) — σ̂ ≤ 1/3, τ̂ bound
- Characteristic speeds: Eqs (A26)-(A27)

**Figures (7 PDFs):**
1. `bjorken_plot.pdf` — Bjorken flow results (Fig 1)
2. `shockwave_plot.pdf` — Steady-state shockwave profiles (Fig 2)
3. `shock_instability.pdf` — Shockwave instability onset (Fig 3)
4. `acaus_instab.pdf` — Acausality instability for various frames (Fig 4)
5. `heat_stationary.pdf` — Heat flow stationary test (Fig 5)
6. `telegraphers_plot.pdf` — Telegrapher's equation behavior (Fig 6)
7. `conv_plot.pdf` — Convergence plot (Fig 7)
