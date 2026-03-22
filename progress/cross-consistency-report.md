# Cross-Consistency Verification Report

**Documents reviewed:**
1. `mathematical-derivations.md` (math)
2. `numerical-implementations.md` (numerics)
3. `test-results.md` (tests)
4. `progress/conventions.md` (conventions)

---

## 1. Notation Consistency

### 1.1 Consistent usage (no issues found)

The following notation is used consistently across all four documents:

- $\epsilon$: energy density
- $P$: pressure
- $\rho \equiv \epsilon + P$: enthalpy density
- $n$: baryon number density
- $\Gamma$: adiabatic index
- $u^a$: flow four-velocity with $u_c u^c = -1$
- $\Delta^{ab} = g^{ab} + u^a u^b$: spatial projector
- $c_s^2 = \Gamma P / \rho$: sound speed squared
- $V = 4\eta/3 + \zeta$: combined viscosity
- $\hat{V}$, $\hat{\eta}$, $\hat{\zeta}$, $\hat{\sigma}$, $\hat{\tau}$: dimensionless transport coefficients
- $\alpha = (\Gamma - 1)/c_s^2$ and $\omega = mnP/(\epsilon\rho)$: dimensionless ratios
- $\kappa_\epsilon$, $\kappa_n$, $\kappa_s$: chemical potential derivative quantities
- $\beta_\epsilon$, $\beta_n$: heat flux coefficients
- Script quantities $\mathcal{E}$, $\mathcal{P}$, $\mathcal{Q}^a$, $\mathcal{T}^{ab}$, $\mathcal{N}$, $\mathcal{J}^a$
- Metric signature $(-+++)$
- Milne coordinates $(\tau, x, y, \xi)$ with $g_{ab} = \text{diag}(-1,1,1,\tau^2)$
- Frame ansatz: $\tau_\epsilon = \tau_Q = L\hat{V}\hat{\tau}$, $\tau_P = 2(\Gamma-1)L\hat{V}$

### 1.2 Issues found

**ISSUE N1 (minor): $c_1$ symbol collision in test-results.md.**
In `test-results.md` line 164, the MIS comparison uses $c_1$ without the disambiguating subscript:

```
\dot{\epsilon} = \frac{1}{\tau_\pi + c_1}(T^{tt} - \epsilon) \quad \text{(MIS)}
```

The conventions document (Sec. 1.6, line 85) explicitly states: "To avoid confusion, write $c_{1,\text{MIS}}$ when referring to the MIS coefficient." The conventions document's own Sec. 10 (line 608) correctly uses $c_{1,\text{MIS}}$, but `test-results.md` line 164 does not follow this convention.

Additionally, in `test-results.md` line 273, the $\hat{\tau} \to \infty$ limit uses $c_1, c_2$ as integration constants:

```
\lim_{\tau_\epsilon \to \infty} \epsilon(\tau) = c_1 \tau^{-1} + c_2
```

The conventions document (Sec. 1.8, line 113) states: "do NOT use $c_1, c_2$ to avoid collision with characteristic speed $c_1$." The mathematical derivations document (Sec. 8.5, line 2917) correctly uses $c_1, c_2$ but then does not follow the convention either. Both should use $C_1, C_2$.

**Recommendation:** In `test-results.md`, replace $c_1$ with $c_{1,\text{MIS}}$ in the MIS equation (line 164, 168, 194). Replace $c_1, c_2$ with $C_1, C_2$ in the $\hat{\tau}\to\infty$ limit (line 273). Make the same fix in `mathematical-derivations.md` line 2917.

**ISSUE N2 (minor): Mixed index notation in test-results.md line 182.**
The test-results document uses $u_\mu u_\nu T^{\mu\nu}$ with Greek indices, while the conventions document specifies Latin indices $\{a,b,c,d,e\}$ for spacetime. This should be $u_a u_b T^{ab}$.

**Recommendation:** Replace $u_\mu u_\nu T^{\mu\nu}$ with $u_a u_b T^{ab}$ in `test-results.md`.

---

## 2. Equation Numbering Consistency

### 2.1 Known table numbering conflict

The conventions document (Sec. 6.5, lines 438--462) explicitly documents that the three output documents use **different equation numbering** for the same paper equations, due to derivation from different draft versions. The concordance table provides the ground-truth mapping:

| Our Label | numerics Eq # | math Eq # | tests Eq # |
|-----------|--------------|-----------|------------|
| `eq:EOS` | Eq 8 | Eqs. 14--15 | -- |
| `eq:hydro_frame` | Eq 26 | Eq. 31 | -- |
| `eq:Bjorken_EOM` | Eq 35 | Eq. 47 | Eq. 36 |
| `eq:inviscid_bjorken` | Eq 34 | Eq. 48 | Eq. 39 |
| `Table:parameters` | Table II | -- | Table I |
| `Table:ODE_convergence` | Table III | -- | Table II |

### 2.2 Issues found

**ISSUE E1 (significant): Table numbering conflict between numerics and tests documents.**
The parameter table and convergence table are referred to by different numbers:

- `numerical-implementations.md` calls the parameter table "Table II" (line 100) and the convergence table "Table III" (line 657).
- `test-results.md` calls the parameter table "Table I" (line 49) and the convergence table "Table II" (line 786).

The conventions document acknowledges this conflict (lines 460--461) and recommends using label-based references (`Table:parameters`, `Table:ODE_convergence`) rather than numbered references. Neither output document follows this recommendation.

**Recommendation:** Adopt the label-based system or standardize on a single numbering scheme across all documents. At minimum, add a clarifying footnote in each document noting the cross-document numbering difference.

**ISSUE E2 (moderate): Inconsistent paper equation numbers for the same content.**
Cross-references between documents will confuse readers:

- The Bjorken ODE is "Eq. 35" in numerics, "Eq. 47" in math, and "Eq. 36" in tests.
- The inviscid Bjorken solution is "Eq. 34" in numerics, "Eq. 48" in math, and "Eq. 39" in tests.
- The shockwave initial data is "Eq. 46" in numerics and "Eq. 50" in tests.
- The Rankine-Hugoniot conditions are "Eq. 47" in numerics and "Eq. 49" in tests.
- The heat flow equation is "Eq. 53" in numerics and "Eq. 59" in tests.
- The heat flow governing equation is referenced as "Eq. 54" in numerics and "Eq. 61" in tests.
- The telegrapher's equations are "Eq. 55--57" in tests vs. no explicit numbering in numerics.

These are not contradictions (each document likely uses a different draft numbering), but they will be confusing for anyone reading across documents.

**Recommendation:** Adopt the conventions document's recommendation to use label-based references (e.g., `eq:Bjorken_EOM`) throughout, supplemented by the concordance table for anyone needing numeric references.

**ISSUE E3 (minor): The relaxation times reference.**
`test-results.md` line 22 references "$\tau_\epsilon, \tau_P, \tau_Q$ (ref: paper Eq. 14)" while `numerical-implementations.md` references the frame definitions as "(ref: paper Eq. 26)". These refer to different equations (constitutive relations vs. frame ansatz) and are actually distinct -- not a true inconsistency, but the test-results reference is misleading as Eq. 14 in the numerics document is the EOS, not the relaxation times.

**Recommendation:** Clarify in test-results.md that the relaxation times are defined through the frame ansatz, not directly as paper Eq. 14. Use the label `eq:hydro_frame` or `eq:frame_ansatz`.

---

## 3. Parameter Value Consistency

### 3.1 Consistent values (verified)

All three documents agree on the parameter values for each test:

| Figure | $\Gamma$ | $m$ | $\hat{V}$ | $\hat{\sigma}$ | $\hat{\tau}$ |
|--------|----------|-----|-----------|----------------|-------------|
| Fig. 1 (Bjorken) | $4/3$ | $1$ | $1/10$ | $0$ | $0.5, 1, 2$ |
| Fig. 2 (Shockwave) | $4/3$ | $0.1$ | $2/15$ | $0$ | $1.5$ |
| Fig. 3 (Shock instab.) | $4/3$ | $0.1$ | $4/3$ | $0$ | $1.5, 3$ |
| Fig. 4 (Acausal instab.) | $4/3$ | $0.1$ | $4/3$ | $0$ | $0.25, 0.4, 0.5, 1.5$ |
| Fig. 5 (Heat stationary) | $4/3$ | $0.1$ | $2/15$ | $0, 1/3$ | $1.5$ |
| Fig. 6 (Telegrapher's) | $4/3$ | $0.1$ | $2/15$ | $0.15, 1.5, 7.5$ | $1.5, 15, 75$ |

Verified consistent across `conventions.md` Sec. 8.3, `numerical-implementations.md` Sec. 2.3, and `test-results.md` Sec. 2.

### 3.2 Initial conditions consistency (verified)

- Bjorken flow: $\epsilon_0 = 0.25$, $\dot{\epsilon}_0 \in \{-2, 0, 2\}$, $n_0 = 0.1$, domain $\tau \in [1, 20]$ -- consistent across numerics (Sec. 3.1.4) and tests (Sec. 5).
- Shockwave ODE left state: $\{\epsilon_L, v_L, n_L\} = \{1, 0.8, 0.1\}$ -- consistent across numerics (Sec. 3.2.6) and tests (Sec. 6).
- Shockwave PDE left states and Rankine-Hugoniot right states: consistent across numerics (Sec. 5.2) and tests (Secs. 7--8).
- CFL numbers: consistent ($\lambda = 0.1$ default, $\lambda = 0.01$ for stiff/superluminal cases).
- Width parameter $w = 10$ for erf profiles: consistent.

### 3.3 Convergence results consistency (verified)

ODE convergence table values are identical across `numerical-implementations.md` (Sec. 6.4) and `test-results.md` (Sec. 11.1):

| Test | $N$ | $Q_{N/4}$ | $Q_{N/2}$ | $Q_N$ |
|------|-----|-----------|-----------|-------|
| Bjorken, $\hat{\tau} = 0.5$ | $2^{11}$ | $34.8$ | $18.7$ | $16.9$ |
| Bjorken, $\hat{\tau} = 1$ | $2^{11}$ | $18.4$ | $16.9$ | $16.3$ |
| Bjorken, $\hat{\tau} = 2$ | $2^{11}$ | $16.9$ | $16.3$ | $16.1$ |
| Shockwave | $2^{13}$ | $15.9$ | $15.9$ | $15.9$ |

No discrepancies found.

### 3.4 Issues found

**ISSUE P1 (minor): Characteristic speed approximate values differ slightly.**
`test-results.md` Sec. 5 gives $c_+ \approx 1.3$ for $\hat{\tau}=0.5$, $\approx 1.05$ for $\hat{\tau}=1$, and $\approx 0.7$ for $\hat{\tau}=2$ (Bjorken flow). The parameter table in Sec. 2 repeats these. `numerical-implementations.md` does not provide these values for Bjorken flow specifically (only for the shockwave PDE). No contradiction, but the approximate values in the test-results document are not cross-validated against the numerics document.

**ISSUE P2 (informational): Left-state pair for Fig. 3 and Fig. 4.**
Both documents use different left states for the two shockwave PDE tests:
- Fig. 3: $\{1, 0.9, 1\}$ (high velocity)
- Fig. 4: $\{1, 0.6, 1\}$ (lower velocity)

These are correctly reported in both documents. No issue.

---

## 4. Contradictions Check

### 4.1 No contradictions found in physics claims

All three documents agree on:

- BDNK and MIS are structurally equivalent on spatially isotropic data
- Eckart theory applies dissipation instantaneously
- Temperature is frame-dependent outside equilibrium
- Superluminal characteristics do NOT cause acausal propagation for weakly superluminal frames
- The stability bound $\hat{\sigma} \leq 1/3$ is sufficient but not necessary
- The causality bound on $\hat{\tau}$ ensures subluminal characteristics
- ODE convergence rate is fourth-order ($Q_N \to 16$)
- PDE convergence is second-order ($Q_N \to 4$), degrading after boundary interaction
- Shockwave instability is localized to $v > c_+$ region
- Heat flow requires $\sigma \neq 0$ for dynamics

### 4.2 Potential contradiction found

**ISSUE C1 (moderate): $c_1^2$ expression.**

The conventions document (Sec. 5.7, line 341) and `test-results.md` (line 32) both give:

$$c_1^2 = c_s^2 \frac{\eta}{V\hat{\tau}}$$

The `mathematical-derivations.md` (Sec. 5.3, line 1842) gives:

$$c_1^2 = \frac{\eta}{\rho\tau_Q}$$

and then derives:

$$c_1^2 = \frac{c_s^2\hat{\eta}}{\hat{V}\hat{\tau}}$$

These are equivalent: $\eta/(\rho\tau_Q) = (\rho c_s^2 L\hat{\eta})/(\rho L\hat{V}\hat{\tau}) = c_s^2\hat{\eta}/(\hat{V}\hat{\tau})$. And $\eta/(V\hat{\tau}) = (\rho c_s^2 L\hat{\eta})/(\rho c_s^2 L\hat{V}\hat{\tau}) = \hat{\eta}/(\hat{V}\hat{\tau})$. So $c_s^2\eta/(V\hat{\tau}) = c_s^2\hat{\eta}/(\hat{V}\hat{\tau})$.

This is consistent. However, the derivations document uses the more fundamental form $c_1^2 = \eta/(\rho\tau_Q)$ as the starting point, while the other documents quote $c_1^2 = c_s^2\eta/(V\hat{\tau})$. Both are correct. No contradiction.

**ISSUE C2 (minor): Discrepancy in "Fig. 7" vs "Fig. 8" for PDE convergence.**
`test-results.md` Sec. 11.2 header says "Fig. 7" (line 786: "Appendix B, Fig. 7, Table II"), while the body text at line 819 says "Fig. 7 shows $Q_N(t)$...". However, `numerical-implementations.md` Sec. 6.5 (line 679) says "PDE convergence results are shown in Fig. 8 of the paper (ref: paper Fig. 8, line 1457)."

Both cannot be correct. The conventions document (Sec. 8.1) lists 7 figures total (Fig. 1--Fig. 7), with "fig:conv_plot" as the 7th. The `test-results.md` reference to "Fig. 7" appears to match the conventions document's 7-figure numbering. The `numerical-implementations.md` reference to "Fig. 8" suggests a different draft numbering.

**Recommendation:** Standardize to "Fig. 7" in accordance with the conventions document, or use the label `fig:conv_plot` throughout.

---

## 5. Completeness Check

### 5.1 Coverage by topic

| Paper Section / Result | math | numerics | tests |
|------------------------|------|----------|-------|
| Tensor decomposition ($\Delta^{ab}$, projections) | Yes (Sec. 1) | -- | -- |
| Ideal fluid constitutive relations | Yes (Sec. 1.4) | Yes (Sec. 2.1) | -- |
| Relativistic Euler equations | Yes (Sec. 1.5) | -- | -- |
| EOS: $P$, $T$, $e$ | Yes (Sec. 2.1) | Yes (Sec. 2.1) | Yes (Sec. 1.1) |
| Entropy density $s(\epsilon,n)$ | Yes (Sec. 2.2) | -- | -- |
| Chemical potential $\mu(\epsilon,n)$ | Yes (Sec. 2.3) | -- | -- |
| Thermodynamic identity | Yes (Sec. 2.4) | -- | -- |
| Pressure derivatives $p'_\epsilon$, $p'_n$ | Yes (Sec. 3.1) | Yes (Sec. 2.1) | -- |
| $\kappa_\epsilon$, $\kappa_n$, $\kappa_s$ | Yes (Sec. 3.2--3.3) | Yes (Sec. 2.1) | -- |
| Sound speed derivation | Yes (Sec. 3.4) | Yes (Sec. 2.1) | -- |
| $\alpha$, $\omega$ | Yes (Sec. 3.5) | Yes (Sec. 2.1) | -- |
| BDNK constitutive relations | Yes (Sec. 4.1) | -- | -- |
| $\beta_\epsilon$, $\beta_n$ | Yes (Sec. 4.2) | Yes (Sec. 2.2) | -- |
| On-shell nature of regularizing terms | Yes (Sec. 4.3) | -- | -- |
| Eckart as limit of BDNK | Yes (Sec. 4.4) | -- | -- |
| Alternative heat flux form | Yes (Sec. 4.5) | -- | -- |
| Hydrodynamic frame ansatz | Yes (Sec. 5.1) | Yes (Sec. 2.2) | Yes (Sec. 1.1) |
| $\delta = 0$ identity | Yes (Sec. 5.2) | -- | -- |
| Characteristic speeds $c_\pm^2$, $c_1^2$ | Yes (Sec. 5.3) | Yes (Sec. 7.2) | Yes (Sec. 1.2) |
| Constraint simplification (CAUS, STAB) | Yes (Sec. 6) | -- | Yes (Sec. 1.3) |
| $\hat{\sigma} \leq 1/3$ derivation | Yes (Sec. 6.4) | -- | -- |
| $\hat{\tau}$ causality bound derivation | Yes (Sec. 6.5--6.6) | -- | -- |
| Equilibrium state comparison | Yes (Sec. 7) | -- | Yes (Sec. 4) |
| Bjorken: baryon conservation | Yes (Sec. 8.2) | Yes (Sec. 3.1.2) | -- |
| Bjorken: ODE derivation | Yes (Sec. 8.3) | Yes (Sec. 3.1.2) | -- |
| Bjorken: inviscid solution | Yes (Sec. 8.4) | Yes (Sec. 3.1.5) | Yes (Sec. 5) |
| Bjorken: $\hat{\tau}\to\infty$ limit | Yes (Sec. 8.5) | -- | Yes (Sec. 5) |
| Bjorken: pressure positivity | Yes (Sec. 8.6) | -- | Yes (Sec. 5) |
| Shockwave: ODE system | Yes (Sec. 9) | Yes (Sec. 3.2) | Yes (Sec. 6) |
| Shockwave: numerator coefficients | -- | Yes (Sec. 3.2.3) | Yes (Sec. 6) |
| Shockwave: conserved quantities | -- | Yes (Sec. 3.2.4) | -- |
| Shockwave: RK4 | -- | Yes (Sec. 3.3) | -- |
| Shockwave: PDE initial data | -- | Yes (Sec. 5.1) | Yes (Secs. 7--8) |
| Shockwave: Rankine-Hugoniot | -- | Yes (Sec. 5.2) | Yes (Sec. 6) |
| Heat flow: initial data | -- | Yes (Sec. 5.3) | Yes (Secs. 9--10) |
| Heat flow: telegrapher's eq. analysis | -- | -- | Yes (Sec. 10) |
| PDE solver: FV + WENO + Heun | -- | Yes (Sec. 4) | -- |
| CFL and stiffness | -- | Yes (Sec. 4.5) | Yes (Sec. 3) |
| Convergence testing | -- | Yes (Sec. 6) | Yes (Sec. 11) |
| Ghost cells / boundary effects | -- | Yes (Sec. 5.4, 7.4) | Yes (Sec. 11.3) |

### 5.2 Gaps identified

**ISSUE G1 (moderate): Shockwave numerator coefficient derivation missing from math document.**
The mathematical derivations document (Sec. 9) begins the shockwave ODE system derivation but the numerator coefficients $c_0, \ldots, c_4$ and $d_0, \ldots, d_3$ are stated in the numerics document (Sec. 3.2.3) without a step-by-step derivation appearing in the math document. Given the math document's stated goal of providing "non-step-skipping derivations of all mathematical results," this is a gap.

**Recommendation:** Add derivation of shockwave numerator coefficients to mathematical-derivations.md, or mark this as a known gap.

**ISSUE G2 (minor): Heat flow equation derivation (telegrapher's).**
The constant-coefficient heat flow analysis (Eckart, hybrid, BDNK telegrapher's equations) is described in `test-results.md` (Sec. 10 background) but the derivation showing how the full BDNK equations reduce to the telegrapher's equation form is not present in `mathematical-derivations.md`. The alternative heat flux form is derived (Sec. 4.5), but the reduction to the 1D heat equation, hybrid, and BDNK forms is not.

**Recommendation:** Add derivation of the constant-coefficient telegrapher's equation form to mathematical-derivations.md.

**ISSUE G3 (minor): Missing coverage of the Bjorken ODE derivation with state-dependent coefficients.**
The mathematical derivations document (Sec. 8.3) presents the Bjorken ODE but marks the full derivation with state-dependent transport coefficients as [PRELIMINARY]. The verification of the paper's Eq. 47 with proper accounting of $\dot{\tau}_\epsilon$, $\dot{\rho}$ terms is incomplete. The document states the final result is [SOLID] but the derivation itself has gaps.

**Recommendation:** Either complete the full derivation or add a note that the result is verified by numerical consistency (matching the RK4 integration results).

**ISSUE G4 (informational): Heat flow parameters remain unspecified.**
All three output documents and the conventions document acknowledge that the specific parameter values $(A, \delta, w, P_0)$ for the heat flow initial data (Gaussian temperature profile) are not given in the paper. Both `numerical-implementations.md` (Sec. 5.3, marked [PRELIMINARY]) and `test-results.md` (Sec. 9) note this gap. The conventions document (Sec. 8.3, line 557) also flags this as an open question. This is a gap in the paper itself, not in the documentation.

---

## 6. Additional Issues

**ISSUE A1 (minor): Left state for shockwave ODE vs. PDE.**
The steady-state shockwave ODE (Fig. 2) uses left state $\{1, 0.8, 0.1\}$, while the dynamic shockwave PDE (Fig. 3) uses $\{1, 0.9, 1\}$ and Fig. 4 uses $\{1, 0.6, 1\}$. These are correctly reported in all documents, but readers may be confused by the different left states and especially different $n_L$ values (0.1 vs 1). All documents handle this correctly; no action needed.

**ISSUE A2 (minor): Figure numbering for convergence plot.**
As noted in ISSUE C2, the convergence figure is called "Fig. 7" in `test-results.md` and `conventions.md`, but "Fig. 8" in `numerical-implementations.md`. This should be reconciled.

**ISSUE A3 (cosmetic): Inconsistent use of "ref: paper Eq." format.**
The conventions document specifies the format `(ref: paper Eq. XX)`. Most references follow this, but some in `test-results.md` use slightly different forms like `(ref: paper Eq. A12--A13)` for appendix equations. This is acceptable but should be noted as a minor style variation.

---

## 7. Summary of Issues by Severity

### Significant (should fix)
1. **E1**: Table numbering conflict ("Table I" vs "Table II" for parameters, "Table II" vs "Table III" for convergence) between numerics and tests documents.
2. **E2**: Inconsistent paper equation numbers across all three documents (different draft numbering).

### Moderate (recommended fix)
3. **C2/A2**: Convergence figure called "Fig. 7" in tests/conventions but "Fig. 8" in numerics.
4. **G1**: Shockwave numerator coefficient derivation missing from mathematical-derivations.md.
5. **E3**: Misleading equation reference for relaxation times in test-results.md.

### Minor (optional fix)
6. **N1**: $c_1$ symbol collision -- test-results.md uses $c_1$ where conventions require $c_{1,\text{MIS}}$, and both test-results and math-derivations use $c_1, c_2$ as integration constants where conventions require $C_1, C_2$.
7. **N2**: Greek indices $u_\mu u_\nu T^{\mu\nu}$ in test-results.md instead of Latin indices.
8. **G2**: Telegrapher's equation derivation not in mathematical-derivations.md.
9. **G3**: Bjorken ODE derivation with state-dependent coefficients incomplete.

### Informational (no action needed)
10. **G4**: Heat flow initial data parameters $(A, \delta, w, P_0)$ not specified in paper.
11. **P1**: Characteristic speed approximate values not cross-validated.

---

## 8. Recommendations

1. **Adopt label-based equation referencing** (`eq:Bjorken_EOM`, `Table:parameters`, etc.) across all three output documents, as recommended by the conventions document. This would resolve issues E1, E2, and E3 in one sweep.

2. **Reconcile the convergence figure number** to either "Fig. 7" (matching conventions.md) or "Fig. 8" (matching some paper draft), and use the label `fig:conv_plot` for unambiguous reference.

3. **Fix the $c_1$ / $c_{1,\text{MIS}}$ / $C_1, C_2$ notation** in test-results.md and mathematical-derivations.md to match the conventions document.

4. **Add the shockwave numerator coefficient derivation** (or at minimum a forward reference) to mathematical-derivations.md.

5. **Standardize Greek/Latin index usage** (replace $u_\mu u_\nu$ with $u_a u_b$ in test-results.md).

---

*Report generated by the cross-consistency verification agent.*
