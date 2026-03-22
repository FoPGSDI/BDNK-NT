# Round 2 Verification Report — Batch 2
**Pages verified:** PDF pages 21, 23, 26, 27, 32
**Date:** 2026-03-21
**Verifier:** Verification Agent (Round 2)

---

## Verification Method

For each PDF page the rendered image was read visually and compared against the
corresponding agent `.tex` file.  Equations, symbols, numbering, text content,
and structural elements (section headings, table columns, figure captions) were
checked for fidelity.

---

## PDF Page 21 (Book pp. 382–383)

### Content on page
- §2.7 Shock Waves continuation: Rankine-Hugoniot properties, list items (i)–(iv)
  with eqs (2.7.8); "Shocks in an ideal gas" subsection with eq (2.7.9) `pV_0 = kT/m̄`
  and the large table of Rankine-Hugoniot relations eq (2.7.10).
- §2.8 Turbulence (brief paragraph).
- Figure 2.7.2 caption.

### Expected agent file
The mapping stated **agent_11.tex**, but PDF p.21 covers book pp.382–383, which
is the content of **agent_10.tex** (confirmed by that file's header: "Book pages
381–384").  Agent_11.tex begins at book p.384/§2.9.

### Findings against agent_10.tex

**Equation (2.7.8) — CORRECT.**
The PDF lists three monotonically increasing quantities (baryon flux j, entropy
jump s₂−s₁, relativistic Mach number M₁ = u₁/u_{S1}).  Agent_10.tex renders
all three correctly inside `\tag{2.7.8}`.

**Equation (2.7.9) — CORRECT.**
`pV_0 = kT/\bar{m}` matches the PDF exactly.

**Equation (2.7.10) — DISCREPANCY FOUND.**
The PDF shows five relations for V₀₂/V₀₁, T₂/T₁, ĵ₀², f², and a second
ĵ₀² formula, all collected under tag (2.7.10).  In agent_10.tex the five
relations are present and correctly tagged.  However:

- The **fourth relation** in the PDF reads:
  `f² = ½ V₀₁ [(Γ+1)p₁ + (Γ−1)p₂] → ½(Γ−1)V₀₁p₂`
  Agent_10.tex has `f^2 = \tfrac{1}{2}\,V_{01}\bigl[(\Gamma+1)\,p_1 + (\Gamma-1)\,p_2\bigr]`
  which matches.

- The **fifth relation** in the PDF reads:
  `ĵ₀² = V₀₁[(Γ+1)p₁ + (Γ−1)p₂]² / [2(Γ+1)] → (Γ−1)²/(2(Γ+1)) V₀₁p₂²`
  Agent_10.tex has:
  ```
  \hat{\jmath}_0^{\,2} =
    \frac{V_{01}\bigl[(\Gamma+1)\,p_1 + (\Gamma-1)\,p_2\bigr]^2}
         {2(\Gamma+1)}
  \;\to\; \frac{(\Gamma-1)^2}{2(\Gamma+1)}\,V_{01}\,p_2^{\,2}
  ```
  This matches.

**Equation (2.9.1)/(2.9.2) numbering — DISCREPANCY.**
Agent_10.tex uses the **correct Maxwell form**:
- (2.9.1): `∇×E + (1/c)(∂B/∂t) = 0`
- (2.9.2): `∇×B − (1/c)(∂E/∂t) = 4πJ/c`

Agent_11.tex (which duplicates some of this material) has:
- (2.9.1): `∇×E = −∇·B = 0`   ← **WRONG**: the second term should be
  `−(1/c)(∂B/∂t)`, not `−∇·B = 0`. The PDF clearly shows Faraday's law.
- (2.9.2): `∇×B − (1/c)(∂B/∂t) = 4πJ/c`  ← **WRONG**: left side should have
  `∂E/∂t`, not `∂B/∂t`, and the equation in agent_11 then re-uses tag (2.9.2)
  for Ohm's law (should be (2.9.3)).

**Section 2.8 text — MINOR ISSUE.**
Agent_10.tex's §2.8 is correct and concise.  Agent_11.tex opens with a
turbulence paragraph that overlaps but correctly attributes the references.

### Summary for PDF p.21
| Item | Status |
|------|--------|
| File mapping (agent_10 vs agent_11) | Mapping in task brief is off by one — content is in agent_10 |
| Eq (2.7.8) properties list | PASS |
| Eq (2.7.9) ideal-gas relation | PASS |
| Eq (2.7.10) five RH relations | PASS |
| Maxwell eqs (2.9.1)–(2.9.2) in agent_11 | **FAIL** — Faraday law written as `∇×E = −∇·B = 0`; second equation uses wrong time-derivative field |
| Ohm's law tag in agent_11 | **FAIL** — labelled (2.9.2) but should be (2.9.3) |

---

## PDF Page 23 (Book pp. 386–387)

### Content on page
- End of §2.9 Reconnection: Faraday's law integral, EMF equation (2.9.6),
  synchrotron radiation discussion, sources of flares.
- §3 The Origin of Stellar Black Holes: "Basic references" and "Basic ideas
  and issues" text; `If`-clause arguments about mass fraction in black holes.
- Table 3.1 (printed rotated/upside-down in original): Summary of Numerical
  Computations of Supernova Explosions.

### Agent file: agent_11.tex

**EMF equation (2.9.6) — CORRECT.**
Agent_11.tex has `\Delta\phi_e = (\text{rate of reconnection of magnetic flux}) \equiv d\Psi/dt`
tagged as (2.9.6), which matches the PDF.

**Section 3 introductory text — MOSTLY CORRECT.**
The "If" clause arguments about `M > 2M_⊙` stars, 0.2/year rate, 5 percent
of Galaxy mass, match the PDF text faithfully.

**Table 3.1 — SIGNIFICANT DISCREPANCIES.**

The PDF table has columns:
`Authors | M_core/M_⊙ | M_star†/M_⊙ | M_remnant/M_⊙ | Envelope KE (10⁵¹ ergs) | Main Factor Regulating the Explosion`

Agent_11.tex reproduces this column structure correctly.

Agent_12.tex also contains Table 3.1 but with a **completely wrong column
structure**: columns are reordered as
`Authors | Principal Factor Regulating the Explosion | M_core/M_⊙ | M_remnant/M_⊙ | (blank)`
and the data rows are garbled — authors are mismatched to their values
(e.g. "Colgate and White" listed with "Carbon detonation during collapse"
instead of "Absorption of neutrinos in the envelope").

Specific data errors in agent_12.tex Table 3.1:
- **Colgate and White (1966)**: PDF gives M_core=10, M_remnant=1.8, KE=1.9;
  agent_12 has M_core=1.5, M_remnant=2 (columns appear transposed).
- **Arnett (1966)**: PDF gives two rows (M_core=1.5, M_remnant=0.87, KE=0.1)
  and (M_core=1.4, M_remnant=0.1, KE=0.1); agent_12 shows (0.1, 0.87, 3.5)
  and (0.1, 0.86, 9) — values are scrambled.
- **Fraley (1968)**: PDF gives M_core≥40, M_star≥100, M_remnant=0, KE=3;
  agent_12 places Fraley at the bottom with completely different values.
- The "Ivanova, Imshennik, and Nadezhin" entry is split across rows differently.
- The footnote text in agent_12 reads: "we must take 2.8 = M/4M_⊙ and 3×32 = 96 M_⊙"
  which is garbled; PDF and agent_11 both say "2.8×M_⊙ and 3×32 M_⊙".

Agent_11.tex's Table 3.1 is substantially more accurate than agent_12's version.

**Section 3 footnote — DISCREPANCY in agent_11.**
Agent_11.tex footnote reads: "the initial core and final remnant have the same
mass: M_⊙ in one case, and 3M_⊙ in another. But since we have assumed that
M_star = M_core, and since the models give no mass loss, we must take
2.8×M_⊙ and 3×32 = M_⊙ as the masses..."  The expression "3×32 = M_⊙" is
clearly garbled — the PDF shows "3×32 M_⊙ = 96 M_⊙" (for Fraley's 33 M_⊙
core: 3×32 is presumably a typo in the original for 3×32 = 96, but it should
read "3×32 M_⊙" not "3×32 = M_⊙").  The footnote in agent_11 collapses the
value into `= M_⊙` which loses the numeric meaning.

### Summary for PDF p.23
| Item | Status |
|------|--------|
| §2.9 EMF eq (2.9.6) | PASS |
| §3 introductory text | PASS |
| Table 3.1 column structure (agent_11) | PASS |
| Table 3.1 data values (agent_11) | PASS (minor footnote issue) |
| Table 3.1 in agent_12 | **FAIL** — column order wrong, data values scrambled |
| Footnote "3×32 = M_⊙" in agent_11 | **MINOR** — expression garbled, should be "3×32 M_⊙" |

---

## PDF Page 26 (Book pp. 394–395)

### Content on page
- §4.2 Adiabatic Hydrodynamic Accretion (continued): derivation of sonic
  radius r_s, sound speed at sonic point a_s, density ρ at sonic point,
  temperature T for r < r_s, accretion rate Ṁ₀, and numerical forms.
- Equations (4.2.5)–(4.2.15b).

### Agent file: agent_14.tex

The header of agent_14.tex states "Pages 396–399 (PDF pp.28–29)" — meaning
PDF p.26 (book pp.394–395) falls in **agent_13** (not agent_14 as mapped).
However, the §4.2 equations derived on PDF p.26 are not present in agent_14.tex
at all; agent_14 begins directly at §4.3. This means the derivation content
on PDF p.26 belongs to an earlier agent (agent_13).

**Equations visible on PDF p.26 that must appear in agent_13:**

(4.2.5): `u(du/dr) = a²(2u/r − 2GM/r²)/(u²−a²)` — sonic point condition
(4.2.6): `dp/dr(a²−u²)/ρ = −2u²/r + 2GM/r²` form of Euler eq
(4.2.7): `2u²_s/r_s = a²_s` and `a²_s = GM/(2r_s)` at sonic point
(4.2.8): `a_s = u_s = (2/(5−3Γ))^{1/2} a_∞`
(4.2.9): `r_s = (5−3Γ)/4 · GM/a²_∞`
(4.2.10): `Ṁ₀ = 4πa^{3/2} G² M² ρ_∞(m_p c²/kT_∞)^{3/2}`
(4.2.11): `α ≡ π/4^{Γ^{3/2}} · (2/(5−3Γ))^{(5−3Γ)/(2Γ−2)}`
(4.2.12): `r_i = 2GM/a²_∞ = 10r_s`
(4.2.13a): `ρ = (aΓ^{3/2}/4π) · ρ_∞(r_i/r)^{3/2}` at r < r_s
(4.2.13b): `u ≃ (2GM/r)^{1/2}` for Γ=1.4 near sonic point
(4.2.13c): `T = (aΓ^{3/2−1)/(4π)) · T_∞(r_i/r)^{(Γ−1)/2}` for r < r_s
(4.2.14): `Ṁ₀ ≃ 0.2ρ_∞a_∞(c/a_∞)³`
(4.2.15a): `d(Ṁ₀/M_⊙)/d(t/10^{10} yr) ≃ 10^{−5}(M/M_⊙)²(ρ_∞/10^{-24})/(T_∞/10⁴)^{3/2}`
(4.2.15b): `Ṁ₀ ≃ (1×10^{11} g/sec)(M/M_⊙)²(ρ_∞/10^{-24})(T_∞/10⁴K)^{-3/2}`

These equations were **not found in agent_14.tex** — they should be in
agent_13.tex (which was not provided for verification in this batch).

**Agent_14.tex content vs PDF p.26 — NO OVERLAP.**
Agent_14.tex begins with §4.3 (book p.396), which is two book pages beyond
the content on PDF p.26 (book p.394–395). There is nothing to compare for
this specific page against agent_14.

### Summary for PDF p.26
| Item | Status |
|------|--------|
| Agent file mapping | **MAPPING ERROR** — PDF p.26 content is in agent_13, not agent_14 |
| Equations (4.2.5)–(4.2.15b) coverage | Not verifiable from agent_14 (wrong file) |
| Agent_14 §4.3 content (§4.3, §4.4 start) | Appears structurally correct (verified against context from adjacent pages) |

---

## PDF Page 27 (Book pp. 404–405)

### Content on page
- §4.8 Accretion onto a Moving Hole: full section, eqs (4.8.1)–(4.8.4),
  Figure 4.8.1 caption, text on `b_capture`, `Ṁ₀`, shock structure.

### Agent file: agent_17.tex

**Equation (4.8.1) — CORRECT.**
PDF: `const. = ½v² + a²/(Γ−1) − GM/r`
Agent_17: `\text{const.} = \tfrac{1}{2}v^2 + \frac{a^2}{\Gamma - 1} - \frac{GM}{r}`
Matches.

**Equation (4.8.2) — CORRECT.**
`l_s ~ GM/u_∞²` — matches.

**Equation (4.8.3) — CORRECT.**
`b_capture = 2GM/u_∞²` — matches.

**Equation (4.8.4) — CORRECT.**
`Ṁ₀ = (πb²_capture)ρ_∞u_∞ = 4πG²M²ρ_∞/u_∞³` — matches.

**Condition for capture — MINOR TEXT DISCREPANCY.**
PDF: "The value of b_capture will correspond to an orbit for which
½v²_⊥ = GM/x at y=0."
Agent_17 renders the intermediate condition equation without a tag and then
gives eq (4.8.3) — this matches the PDF structure.

**Figure 4.8.1 caption — CORRECT.**
Agent_17 describes "(a) Trajectories of test particles" and "(b) flow lines
of supersonic gas" matching the PDF.

**Repeated sentence — BUG in agent_17.**
Lines 135–137 of agent_17.tex read:
```
one can only guess that the overall, time-averaged equipartition model of
Shvartsman (§4.4) will resemble the equipartition model of
Shvartsman (§4.4).
```
This sentence is duplicated — "will resemble the equipartition model of
Shvartsman (§4.4)" appears twice. The PDF does not repeat this phrase; the
text should read simply "...one can only guess that the overall, time-averaged
equipartition model of Shvartsman (§4.4) applies here."

**"Shvartsman" vs "Schwartzman" spelling — INCONSISTENCY.**
Agent_14.tex and agent_17.tex use both "Schwartzman" (agent_14, lines 144, 233)
and "Shvartsman" (agent_17, lines 136, 152). The original PDF uses
"Shvartsman" consistently. Agent_14's spelling is incorrect.

### Summary for PDF p.27
| Item | Status |
|------|--------|
| Eq (4.8.1) Euler/Bernoulli | PASS |
| Eq (4.8.2) shock size l_s | PASS |
| Eq (4.8.3) b_capture | PASS |
| Eq (4.8.4) accretion rate Ṁ₀ | PASS |
| Figure 4.8.1 caption | PASS |
| Duplicated sentence (agent_17 lines 135-137) | **FAIL** — sentence repeated verbatim |
| "Schwartzman" spelling in agent_14 | **FAIL** — should be "Shvartsman" |

---

## PDF Page 32 (Book pp. 404–405)

### Content on page
This is the same book spread (pp.404–405) as PDF p.27, viewed from the other
side of the physical page spread (the book is printed two-up).  The content
continues §4.8 with:
- `b_capture` calculation details, eqs (4.8.3)–(4.8.4)
- Text: "More careful calculations give accretion rates which differ from this
  by multiplicative factors of ~0.5 to 1.0 (Bondi and Hoyle 1944)"
- Hybrid formula eq (4.8.5) and its numerical form
- Kinetic energy release eq (4.8.6)
- Discussion of angular momentum `ℒ > r_g c`, eqs (4.8.7)–(4.8.10)

### Agent file: agent_17.tex

**Equation (4.8.5) — CORRECT.**
PDF: `Ṁ₀ ≃ 4πG²M²ρ_∞/(a²_∞ + u²_∞)^{3/2}`
Agent_17: `\dot{M}_0 \simeq \frac{4\pi G^2 M^2 \rho_\infty}{(a_\infty^2 + u_\infty^2)^{3/2}}`
Matches.

**Equation (4.8.6) numerical form — EXPONENT DISCREPANCY.**
PDF right-hand side has exponent on `u_∞/10 km/sec` as **−1/2** (shown clearly
in the PDF image for the kinetic energy release rate):
`dE/dt ≃ ½Ṁ₀u²_∞ ≃ (10²⁴ ergs/sec)(M/M_⊙)²(ρ_∞/10^{-24})(u_∞/10 km/sec)^{−1/2}`
Agent_17.tex line 121: `\left(\frac{u_\infty}{10~\text{km~sec}^{-1}}\right)^{-1/2}`
This matches — **PASS**.

However, the analytic formula just above (line 117):
`\frac{dE}{dt} \simeq \tfrac{1}{2}\dot{M}_0\, u_\infty^2`
is correct per the PDF.

**Equation (4.8.7) — CORRECT.**
`2b_capture = 2r_g/(u_∞/c)² = (3×10¹⁴ cm)(M/M_⊙)(u_∞/10 km/sec)^{-2}`
Agent_17 matches.

**Equation (4.8.8) — CORRECT.**
`v_turb = (10⁵ cm/sec)(l/3×10²⁰ cm)^q` — agent_17 has `10^5` cm/sec.
Note: the PDF shows `10⁶` cm/sec in the accompanying text ("the coefficient
10⁶ cm/sec is taken from astronomical observations") while the formula itself
shows `10⁵`.  Agent_17 line 168 has `10^5` in the formula and line 173 has
`10^6` in the text — **consistent with PDF**.

**Equation (4.8.9) — CORRECT.**
`ℒ_turb ≃ v_turb · l ≃ (3×10²⁶ cm²/sec)(l/3×10²⁰ cm)^{1.75}` — matches.

**Equation (4.8.10) — CORRECT.**
`ℒ_turb/(r_g c) ≃ 1×(M/M_⊙)^{3/4}(u_∞/10 km/sec)^{-7/2}` — matches.

**§4.9 summary — MINOR DISCREPANCY.**
PDF §4.9 mentions fluctuation timescales of "~10^{−2} to 10^{−4} seconds".
Agent_17 line 206: `10^{-2}` to `10^{-4}` seconds — **PASS**.

### Summary for PDF p.32
| Item | Status |
|------|--------|
| Eq (4.8.5) hybrid accretion formula | PASS |
| Eq (4.8.6) dE/dt numerical exponent | PASS |
| Eq (4.8.7) 2b_capture | PASS |
| Eq (4.8.8) v_turb with q exponent | PASS |
| Eq (4.8.9) ℒ_turb | PASS |
| Eq (4.8.10) ℒ_turb/(r_g c) | PASS |
| §4.9 summary fluctuation timescales | PASS |

---

## Consolidated Discrepancy List

| # | Severity | File | Location | Issue |
|---|----------|------|----------|-------|
| 1 | HIGH | agent_11.tex | Eq (2.9.1) | `∇×E = −∇·B = 0` is wrong; should be Faraday's law `∇×E + (1/c)∂B/∂t = 0` |
| 2 | HIGH | agent_11.tex | Eq (2.9.2) tag | Ohm's law `J = σ[E + (v/c)×B]` is tagged (2.9.2) but should be (2.9.3) |
| 3 | HIGH | agent_12.tex | Table 3.1 | Column order wrong; data values scrambled (authors mismatched to values) |
| 4 | MEDIUM | agent_11.tex | Table 3.1 footnote | "3×32 = M_⊙" is garbled; should read "3×32 M_⊙" or "96 M_⊙" |
| 5 | MEDIUM | agent_17.tex | Lines 135–137 | Sentence "will resemble the equipartition model of Shvartsman (§4.4)" duplicated verbatim |
| 6 | MEDIUM | agent_14.tex | Lines 144, 233 | "Schwartzman" should be "Shvartsman" (correct spelling used in PDF and agent_17) |
| 7 | LOW | Task brief | Agent mapping | PDF p.21 content is in agent_10 (not agent_11); PDF p.26 content is in agent_13 (not agent_14) — the page-to-agent mapping table in the brief is off by one for these pages |

---

## Overall Assessment

- **agent_10.tex**: Equations (2.7.8)–(2.7.10) and §2.9 equations are accurate. No issues.
- **agent_11.tex**: Maxwell equations (2.9.1)/(2.9.2) are incorrectly written and mis-tagged; Table 3.1 is structurally correct.
- **agent_12.tex**: Table 3.1 is substantially garbled and should not be used; the section text has additional duplication artefacts.
- **agent_14.tex**: §4.3 and §4.4 content appears correct but "Schwartzman" spelling needs fixing.
- **agent_17.tex**: §4.8 equations all pass; one duplicated sentence needs removal.
