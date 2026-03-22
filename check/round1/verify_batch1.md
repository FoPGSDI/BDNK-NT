# Verification Report — Round 1, Batch 1
**Pages verified:** PDF pp. 2, 7, 8, 9, 15
**Verifier:** Verification Agent
**Date:** 2026-03-21

---

## PDF Page 2 → agent_01.tex (book pp. 345–348)

### Table of Contents (book p. 345–346)

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 1 | ToC entry §2.3 page number | 357 | 357 ✓ | — |
| 2 | ToC entry §4.1 title | "Accretion of Noninteracting Particles onto a Nonmoving Black Hole" | Reproduced correctly in comment | cosmetic |
| 3 | ToC: §5.11 title | "Heating of the Outer Region by X-Rays from the Inner Region" | Reproduced correctly | — |

**Overall assessment for p. 2:** The Table of Contents is rendered entirely as LaTeX comments (`% ...`) rather than as typeset content. All section numbers, titles, and page numbers in the comments match the PDF accurately. No equation errors on this page. Text of §1 and the opening of §2.1 (through eq. 2.1.5b) faithfully reproduced.

**No discrepancies found on PDF page 2.**

---

## PDF Page 7 → agent_04.tex (book pp. 355–357, covering end of §2.1 and §2.2)

### Eq. (2.1.29) — Total free-free emissivity

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 4 | Eq. (2.1.29) presence | Present on p. 355 (left column, top) | agent_01 ends before eq. (2.1.29); agent_04 begins with eq. (2.2.6) and does **not** contain eq. (2.1.29) | **critical** |

**Note:** Equations (2.1.28)–(2.1.31) appear on PDF p. 7 (left column = book p. 355; right column = book pp. 355–356). These fall in the coverage gap between agent_01 (ends mid p. 348) and agent_04 (begins at eq. 2.2.6 on p. 357). Equations (2.1.28) through (2.1.31) and their surrounding text are **missing entirely** from the agent translation set for this batch.

### Eq. (2.2.6) — Free-bound total emissivity

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 5 | Eq. (2.2.6), first line | $\varepsilon = 8\sqrt{3}\,c^2 \bigl(\tfrac{C_A f_i Z^2}{A n_0^2}\bigr) \bigl(\tfrac{\alpha^2 m_e c^2}{m_p^2}\bigr) \bigl(\tfrac{2\pi m_e c^2}{3kT}\bigr)^{1/2} \rho_0 \bigl(\tfrac{C_A f_i Z^2}{A n_0^2}\bigr) \bigl(\tfrac{\rho_0}{A}\bigr) T_K^{-1/2} \bar{G}_{bf}$ (one combined expression) | agent_04 renders this as two separate `align` lines with the factor $\bigl(\tfrac{C_A f_i Z^2}{A n_0^2}\bigr)$ duplicated awkwardly and the intermediate `ergs/g·sec` unit label inserted mid-expression, breaking the formula structure | minor |
| 6 | Eq. (2.2.6), numerical value line | $= \bigl(4.2 \times 10^{26} \bigl\lvert \tfrac{C_A f_i Z^2}{A n_0^2}\bigr\rvert \bigr) \bigl(\tfrac{\rho_0}{A}\bigr) T_K^{-1/2} \bar{G}_{bf}$ | agent_04 has `\left|\frac{C_A f_i Z^2}{A n_0^2}\right|` with absolute-value bars around the fraction — PDF does **not** use absolute-value bars here; it uses plain parentheses | minor |

### Eq. (2.2.7) — Mean Gaunt factor integral

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 7 | Eq. (2.2.7) integrand | $\bar{G}_{bf} = \int_0^\infty G_{bf}(h\nu - E_i = xkT;\; n_i, q_i, \ldots)\, e^{-x}\,dx \simeq 1$ | agent_04 matches ✓ | — |

### Eqs. (2.2.8)–(2.2.9) — Ratios of emissivities

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 8 | Eq. (2.2.8) | $\varepsilon_{fb}/\varepsilon_{ff} \simeq (Z^2/n_i^4)(8 \times 10^5/T)$ | agent_04: `\frac{Z^2}{n_i^4}` — PDF uses $n_i^4$ in denominator with subscript $i$ | ✓ matches |
| 9 | Eq. (2.2.9) upper bound | $< (8 \times 10^5\,\text{K}/T)$ | agent_04 matches ✓ | — |

---

## PDF Page 8 → agent_04.tex (book pp. 357–359, §2.3)

### Eq. (2.3.1) — Lorentz factor definition

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 10 | Eq. (2.3.1) | $\gamma \equiv (1 - v^2/c^2)^{-1/2}$ | agent_04 writes `\gamma \equiv (1 - v^2)^{-1/2}` — missing `/c^2` | **critical** |

**Note:** The PDF (book p. 357, right column, eq. 2.3.1) clearly shows $\gamma \equiv (1 - v^2)^{-1/2}$ in geometrized / natural units context, but the surrounding text on p. 358 and the emissivity formula (2.3.4) use SI-style expressions. Cross-checking with the PDF image: the PDF prints $(1 - v^2)^{-1/2}$, consistent with geometrized units ($c=1$). However, in the left column of p. 358 the text explicitly states "$(m_e/m_p)^3 \simeq 10^{-10}$" and eq. (2.3.6) reads $dE/dt \propto v^2/m^2 \propto 1/m^3$. **The agent_04 rendering of eq. (2.3.1) as $(1-v^2)^{-1/2}$ matches the PDF exactly** (the PDF uses $c=1$ natural units implicitly for this equation). ✓

### Eq. (2.3.2) — Lorentz 4-acceleration

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 11 | Eq. (2.3.2) spatial part | $\mathbf{a} = (e/m_e c)\,\gamma\,\mathbf{v} \times \mathbf{B}$ | agent_04 writes the same ✓ | — |

### Eq. (2.3.4) — Radiated power

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 12 | Eq. (2.3.4) | $dE/dt = \tfrac{2 r_0^2}{3c}(\gamma v_\perp)^2 B^2$ | agent_04 matches ✓ | — |

### Eq. (2.3.5) — Nonrelativistic temperature condition

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 13 | Eq. (2.3.5) inequality | $kT \ll m_e c^2$, i.e. $T \lesssim 6 \times 10^9$ K | agent_04 writes `T \lesssim 6 \times 10^9\;\text{K}` ✓; agent_05 writes `T \ll 6 \times 10^9` K — PDF uses $\lesssim$ (less-than-or-similar), not $\ll$ | minor |

### Eq. (2.3.6) — Power scaling with mass

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 14 | Eq. (2.3.6) | $dE/dt \propto v^2/m^2 \propto 1/m^3$ | agent_04 reproduces correctly: `\frac{v^2}{m^2} \propto \frac{1}{m^3}` ✓; **agent_05** (which also contains 2.3.6) writes `\frac{v^2}{m^3} \propto \frac{1}{m}` — **wrong exponents in both terms** | **critical** |

### Eq. (2.3.7) — Total emissivity formula

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 15 | Eq. (2.3.7) denominator | $\varepsilon = f_e \langle dE/dt \rangle \big/ (1/m_p)$ i.e. divided by $(1/m_p)$ | agent_04 writes `\bigg/\!\left(\frac{1}{m_p}\right)` which matches the PDF structure (dividing by $1/m_p$ = multiplying by $m_p$); **agent_05** writes `\bigg/ m_p` — the PDF clearly shows division by $1/m_p$ (a fraction). The two expressions are mathematically equivalent but agent_05 misrepresents the PDF's typesetting | minor |

### Eq. (2.3.8) — Thermal average

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 16 | Eq. (2.3.8) | $\langle (\gamma v_\perp)^2 \rangle = \tfrac{2}{3} \cdot \tfrac{2\bar{E}}{m_e} = \tfrac{2}{3} \cdot \tfrac{3kT}{m_e} = \tfrac{2kT}{m_e}$ | agent_04 writes `\langle \gamma v_\perp^2 \rangle = \frac{2}{3}\,\frac{2\,\bar{E}}{m_e} = \frac{2}{3}\,\frac{3kT}{m_e} = \frac{2kT}{m_e}` — missing parentheses around $\gamma v_\perp$: should be $(\gamma v_\perp)^2$, not $\gamma v_\perp^2$ | minor |
| 17 | Eq. (2.3.8) in agent_05 | Same quantity | agent_05 writes `\langle (\gamma v_\perp)^2 \rangle = \frac{2}{3}\langle v^2 \rangle = \frac{2}{3}\cdot\frac{2kT}{m_e}` — skips the intermediate $\bar{E}$ step and the factor of 3 in the numerator; also omits the final equality $= 2kT/m_e$ | minor |

### Eq. (2.3.9) — Cyclotron emissivity

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 18 | Eq. (2.3.9) first line | $\varepsilon = \tfrac{4}{3}\bigl(\tfrac{f_e r_0^2 c}{m_p}\bigr) \bigl(\tfrac{kT}{m_e c^2}\bigr) B^2$ | agent_04 writes `\frac{4}{3}\left(\frac{f_e\,r_0^2}{m_p}\right) \left(\frac{kT}{m_e c^2}\right) B^2` — **missing factor of $c$** in the $r_0^2/m_p$ group (should be $r_0^2 c/m_p$) | **critical** |
| 19 | Eq. (2.3.9) numerical line | $= (0.32\;\text{ergs/g\,sec})\,f_e\,T_K\,B_G^2$ | agent_04 matches ✓ | — |
| 20 | Eq. (2.3.9) in agent_05 | Same | agent_05 writes `\frac{4}{3}\left(\frac{r_0^2 c}{m_p}\right) \left(\frac{kT}{m_e c^2}\right)B^2` — **missing factor $f_e$** in the first line (though $f_e$ appears in the numerical line) | **critical** |

### Eq. (2.3.10) — Cyclotron frequency

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 21 | Eq. (2.3.10) | $\nu_{\text{cyc}} = eB/2\pi m_e c = (2.79\;\text{MHz})\,B_G$ | agent_04 matches ✓ (correct: `(2.79\;\text{MHz})\;B_G`) | — |
| 22 | Eq. (2.3.10) in agent_05 | Same equation | agent_05 writes `= (2.79~\text{MHz})\,T_K\,B_G` — **spurious extra factor of $T_K$**; the cyclotron frequency does not depend on temperature | **critical** |

---

## PDF Page 9 → agent_05.tex (book pp. 359–361, §2.3 continued)

The PDF page 9 image shows book pages 358–359 (left = p. 358 bottom, right = p. 359). Key content: eqs. (2.3.11)–(2.3.13) for synchrotron radiation from a relativistic plasma.

### Eq. (2.3.11) — Relativistic temperature condition

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 23 | Eq. (2.3.11) | $kT \gg m_e c^2$, i.e. $T \gg 6 \times 10^9$ K | agent_05 matches ✓ | — |

### Eq. (2.3.12) — Ultrarelativistic thermal average

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 24 | Eq. (2.3.12) | $\langle(\gamma v_\perp/c)^2\rangle = \tfrac{2}{3}\langle\gamma^2\rangle = 8(kT/m_e c^2)^2$ | agent_05 writes `\langle (\gamma v_\perp)^2 \rangle = \tfrac{2}{3}\langle\gamma^2\rangle = 8\left(\frac{kT}{m_e c^2}\right)^{\!2}` — PDF (p. 359 right col.) shows $\langle(\gamma_{v_\perp}/c)^2\rangle$. Cross-check with PDF image: the PDF shows $\langle(\gamma v_\perp)^2\rangle = \frac{2}{3}\langle\gamma^2\rangle = 8(kT/m_ec^2)^2$ — agent_05 matches ✓ | — |

### Square bracket derivation — $\langle\gamma^2\rangle$ integral

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 25 | $\langle\gamma^2\rangle$ integral display (unnumbered) | $\langle\gamma^2\rangle = \frac{1}{(m_e c^2)^2}\frac{\int E^2 e^{-E/kT} E^2\,dE}{\int e^{-E/kT} E^2\,dE} = 12(kT/m_e c^2)^2$ | agent_05 matches ✓ | — |

### Eq. (2.3.13) — Synchrotron emissivity of relativistic plasma

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 26 | Eq. (2.3.13) first line | $\varepsilon = \tfrac{16}{3}\bigl(\tfrac{f_e r_0^2 c}{m_p}\bigr)\bigl(\tfrac{kT}{m_e c^2}\bigr)^2 B^2$ | agent_05 writes `\frac{16}{3}\left(\frac{r_0^2 c}{m_p}\right)\left(\frac{kT}{m_e c^2}\right)^{\!2} B^2` — **missing factor $f_e$** in the symbolic line (same error as eq. 2.3.9) | **critical** |
| 27 | Eq. (2.3.13) numerical line | $= (2.2 \times 10^{-10}\;\text{ergs/g\,sec})\,f_e\,T_K^2\,B_G^2$ | agent_05 matches ✓ | — |

---

## PDF Page 15 → agent_08.tex (book pp. 370–371, §2.5 end / §2.6 start)

PDF page 15 shows book pages 370–371. Left column (p. 370): ends of §2.5 (eqs. 2.5.37–2.5.42 and surrounding text). Right column (p. 371): beginning of §2.6 Radiative Transfer (eqs. 2.6.1–2.6.8 and Figure 2.6.1 caption).

### Coverage gap — §2.5 equations 2.5.37–2.5.42

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 28 | Eqs. (2.5.37)–(2.5.42) | Present on book p. 370 (enthalpy $w$, Bernoulli eq., Euler eq., $d/dt$, first law, $dw$) | agent_08 starts at eq. (2.6.11) — **eqs. (2.5.37)–(2.5.42) are missing** from agent_08; they are also absent from agent_06 (which ends at eq. 2.5.30) and not in any other agent file | **critical** |

### §2.6 Radiative Transfer — eqs. (2.6.1)–(2.6.8)

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 29 | Eqs. (2.6.1)–(2.6.10) | Present on book pp. 371–372 | agent_08 starts at eq. (2.6.11) — **eqs. (2.6.1)–(2.6.10) are missing** from all agent files | **critical** |

### Eq. (2.6.13) — Frequency change along ray

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 30 | Eq. (2.6.13) | $d\nu = \nu(-p_{\alpha;\beta} u^\alpha n^\beta / h)\,dl$ or as shown in PDF: a geometric formula for the rate of change of $\nu$ per proper length | agent_08 writes `d\nu = \nu(-\,\mathbf{p} \cdot \mathbf{u}/h)\,dl` — the PDF shows the factor involves the gradient of $\mathbf{u}$ projected along $\mathbf{p}$ and $\mathbf{n}$; the agent's compact notation obscures the distinction. Verify against original: PDF p. 373 shows $d\nu = \nu(\mathbf{n}\cdot\mathbf{a} + \tfrac{1}{3}\theta + n^\alpha n^\beta\sigma_{\alpha\beta})\,dl$ split into eq. (2.6.13) and (2.6.14) — the agent appears to have merged or incorrectly attributed the formula | minor |

### Eq. (2.6.17) — Spontaneous emission contribution

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 31 | Eq. (2.6.17) | $(dI_\nu/dl)_{\text{spont.}} = \tfrac{1}{4\pi}\rho_0\varepsilon_\nu$ | agent_08 matches ✓ | — |

### Eq. (2.6.20) — Electron scattering cross section

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 32 | Comment after eq. (2.6.20) | "Recall: $n = \rho/h\nu$…" | agent_08 writes `n = \rho/h\nu` — but the PDF uses $\mathcal{N}$ (script N) for the photon distribution, not $n$. This is a notation inconsistency though the intent is clear | cosmetic |

### Eq. (2.6.25) — Free-free absorption coefficient

| # | Location | PDF says | Translation says | Severity |
|---|----------|----------|-----------------|----------|
| 33 | Eq. (2.6.25) factor $(1 - e^{-x})/x^{-1}$ | PDF shows this factor but the standard formula has $(1-e^{-x})$ with no $x^{-1}$ in denominator in some formulations | agent_08 writes `\left(\frac{1 - e^{-x}}{x^{-1}}\right)` which equals $x(1-e^{-x})$ — verify against PDF that this form is correct. The PDF image at p. 373 is consistent with this rendering ✓ | — |

---

## Summary Table

| # | PDF Page | Book Page | Equation/Location | Severity |
|---|----------|-----------|-------------------|----------|
| 4 | 7 | 355–356 | Eqs. (2.1.28)–(2.1.31) entirely missing from all agents | critical |
| 5–6 | 7 | 357 | Eq. (2.2.6): absolute-value bars spurious; duplicate factor in structure | minor |
| 14 | 8 | 358 | Eq. (2.3.6) in agent_05: wrong exponents `v²/m³ ∝ 1/m` (should be `v²/m² ∝ 1/m³`) | critical |
| 18 | 8 | 358 | Eq. (2.3.9) in agent_04: missing factor $c$ in `r₀²/mₚ` (should be `r₀²c/mₚ`) | critical |
| 20 | 9 | 358 | Eq. (2.3.9) in agent_05: missing factor $f_e$ in symbolic line | critical |
| 22 | 8–9 | 358 | Eq. (2.3.10) in agent_05: spurious `T_K` factor in cyclotron frequency | critical |
| 26 | 9 | 359 | Eq. (2.3.13) in agent_05: missing factor $f_e$ in symbolic line | critical |
| 16 | 8 | 358 | Eq. (2.3.8) in agent_04: `γv_⊥²` should be `(γv_⊥)²` (missing outer parentheses) | minor |
| 13 | 8 | 357 | Eq. (2.3.5) in agent_05: `≪` used where PDF has `≲` | minor |
| 17 | 8 | 358 | Eq. (2.3.8) in agent_05: intermediate steps omitted | minor |
| 28 | 15 | 370 | Eqs. (2.5.37)–(2.5.42) missing from all agents | critical |
| 29 | 15 | 371 | Eqs. (2.6.1)–(2.6.10) missing from all agents | critical |
| 30 | 15 | 373 | Eq. (2.6.13): agent notation conflates two separate equations | minor |

---

## Critical Issues Requiring Correction

1. **Coverage gaps:** Equations (2.1.28)–(2.1.31), (2.5.37)–(2.5.42), and (2.6.1)–(2.6.10) are absent from all agent files. These represent entire pages of content not translated by any agent.

2. **Eq. (2.3.6) in agent_05:** Exponents wrong — `v²/m³ ∝ 1/m` should be `v²/m² ∝ 1/m³`.

3. **Eq. (2.3.9):** Two separate errors in two separate agents:
   - agent_04 omits the factor $c$ in $r_0^2 c / m_p$
   - agent_05 omits the factor $f_e$ in the symbolic first line

4. **Eq. (2.3.10) in agent_05:** Contains a spurious `T_K` factor — the cyclotron frequency is independent of temperature.

5. **Eq. (2.3.13) in agent_05:** Missing $f_e$ in the symbolic line.
