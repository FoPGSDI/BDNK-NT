# Plan: Mathematica Derivation Verification Script

## File: `mathematica/derivations.wl`

This document specifies the plan for a Mathematica script that symbolically verifies every derivation chain from the BDNK paper (Pandya, Most, Pretorius) using the ideal gas gamma-law equation of state.

---

## 0. Script Architecture

The script should:
- Be a plain `.wl` (Wolfram Language) file, runnable from the command line via `wolframscript -file derivations.wl`
- Print a header, then run each verification block in order
- For each verification, print `[PASS]` or `[FAIL]` with a descriptive label
- At the end, print a summary: total tests, passes, failures
- Use `FullSimplify` with explicit `Assumptions` throughout (e.g., `Gamma > 1, Gamma < 2, eps > 0, n > 0, m > 0, P > 0`)
- Define a helper function `TestResult[label_String, expr_, expected_] := ...` that compares `FullSimplify[expr - expected, assumptions]` to zero and prints PASS/FAIL

### Global assumptions block

```mathematica
$Assumptions = {
  Gamma > 1, Gamma < 2,
  eps > 0, n > 0, m > 0, P > 0,
  rho > 0, T > 0, s > 0,
  cs2 > 0, cs2 < 1,
  etaV > 0, zetaV >= 0, sigmaV >= 0,
  tauEps > 0, tauP > 0, tauQ > 0,
  hatEta > 0, hatZeta >= 0, hatSigma >= 0, hatSigma <= 1/3,
  hatTau > 0, hatV > 0,
  L > 0,
  alpha >= 1, omega > 0, omega < 1
};
```

---

## 1. Variable Naming Conventions

Map paper symbols to Mathematica variable names as follows:

| Paper Symbol | Mathematica Name | Description |
|---|---|---|
| $\epsilon$ | `eps` | Energy density |
| $n$ | `n` | Baryon number density |
| $m$ | `m` | Particle rest mass |
| $e$ | `e` | Specific internal energy |
| $P$ | `P` | Pressure |
| $T$ | `T` | Temperature |
| $\rho$ | `rho` | $\epsilon + P$ |
| $s$ | `s` | Entropy density |
| $\bar{s}$ | `sbar` | Entropy per particle $s/n$ |
| $\mu$ | `mu` | Relativistic chemical potential |
| $\Gamma$ | `Gamma` (or `gam` to avoid conflict with Mathematica's `Gamma` function) | Adiabatic index |
| $c_s^2$ | `cs2` | Sound speed squared |
| $p'_\epsilon$ | `pPeps` | $(\partial P/\partial\epsilon)_n$ |
| $p'_n$ | `pPn` | $(\partial P/\partial n)_\epsilon$ |
| $\kappa_\epsilon$ | `kappaEps` | Chemical potential derivative quantity |
| $\kappa_n$ | `kappaN` | Chemical potential derivative quantity |
| $\kappa_s$ | `kappaS` | $\kappa_\epsilon + \kappa_n$ |
| $\alpha$ | `alpha` | $p'_\epsilon / c_s^2$ |
| $\omega$ | `omega` | $\kappa_s / \kappa_\epsilon$ |
| $\eta$ | `etaV` | Shear viscosity (suffix V to avoid clash with Mathematica's `Eta`) |
| $\zeta$ | `zetaV` | Bulk viscosity |
| $\sigma$ | `sigmaV` | Thermal conductivity |
| $\tau_\epsilon$ | `tauEps` | Relaxation time for energy density |
| $\tau_P$ | `tauP` | Relaxation time for pressure |
| $\tau_Q$ | `tauQ` | Relaxation time for heat flux |
| $\beta_\epsilon$ | `betaEps` | Heat flux coefficient |
| $\beta_n$ | `betaN` | Heat flux coefficient |
| $V$ | `Vcomb` | Combined viscosity $4\eta/3 + \zeta$ |
| $\hat{V}$ | `hatV` | $V/(\rho c_s^2 L)$ |
| $\hat{\eta}$ | `hatEta` | Dimensionless shear viscosity |
| $\hat{\zeta}$ | `hatZeta` | Dimensionless bulk viscosity |
| $\hat{\sigma}$ | `hatSigma` | Dimensionless thermal conductivity |
| $\hat{\tau}$ | `hatTau` | Dimensionless relaxation time |
| $L$ | `L` | Characteristic lengthscale |
| $A, B, C, D, E$ | `AA, BB, CC, DD, EE` | Constraint shorthand (doubled to avoid Mathematica clashes) |
| $\hat{B}, \hat{C}, \hat{D}, \hat{E}$ | `hatB, hatC, hatD, hatE` | Rescaled constraint shorthand |
| $c_+^2, c_-^2, c_1^2$ | `cPlus2, cMinus2, c12` | Characteristic speeds squared |
| $\kappa$ (thermal conductivity) | `kappaTherm` | $\sigma\rho^2/(n^2 T)$ |
| $\gamma$ (heat flux) | `gammaHF` | $\tau_Q + \sigma\rho/n^2$ |
| $\delta$ | `delta` | $\beta_\epsilon\rho + \beta_n n - \rho c_s^2 \tau_Q - \sigma\kappa_s$ |

**IMPORTANT**: Use `gam` instead of `Gamma` for the adiabatic index to avoid collision with Mathematica's built-in `Gamma` function (the Euler gamma function). All code blocks below use `gam`.

---

## 2. Ordered Verification Steps

### Block 1: Equation of State (EOS) Fundamentals

**Test 1.1: Specific internal energy**
- Define: `e[eps_, n_] := eps/(m*n) - 1`
- Verify: `eps == m*n*(1 + e[eps, n])` (paper Eq. 15)
- Method: `FullSimplify[m*n*(1 + e[eps, n]) - eps]` should be 0

**Test 1.2: Pressure from EOS**
- Define: `Pfunc[eps_, n_] := (gam - 1)*m*n*e[eps, n]`
- Verify: `Pfunc[eps, n] == (gam - 1)*(eps - m*n)` (paper Eq. 14)
- Method: `FullSimplify[Pfunc[eps, n] - (gam-1)*(eps - m*n)]` should be 0

**Test 1.3: Temperature from EOS**
- Define: `Tfunc[eps_, n_] := (gam - 1)*(eps/n - m)`
- Verify: `Pfunc[eps, n] == n*Tfunc[eps, n]` (paper Eq. 14, second equality)
- Method: `FullSimplify[Pfunc[eps, n] - n*Tfunc[eps, n]]` should be 0

**Test 1.4: $\rho$ definition**
- Define: `rhoFunc[eps_, n_] := eps + Pfunc[eps, n]`
- Verify: `rhoFunc[eps, n] == gam*eps - (gam-1)*m*n` (simplification)
- Method: `FullSimplify[rhoFunc[eps, n] - (gam*eps - (gam-1)*m*n)]` should be 0

### Block 2: Microphysics Derivatives

**Test 2.1: $p'_\epsilon$**
- Compute: `D[Pfunc[eps, n], eps]` holding `n` constant
- Verify equals `gam - 1` (paper Eq. 31)

**Test 2.2: $p'_n$**
- Compute: `D[Pfunc[eps, n], n]` holding `eps` constant
- Verify equals `-(gam - 1)*m` (paper Eq. 32)

**Test 2.3: $\mu/T$ and its $\epsilon$-derivative for $\kappa_\epsilon$**
- Define `muOverT[eps_, n_]` from the chemical potential and temperature
- Compute: `D[muOverT[eps, n], eps]` at constant `n`
- Define: `kappaEpsFunc[eps_, n_] := rhoFunc[eps,n]^2 * Tfunc[eps,n] / n * D[muOverT[eps, n], eps]`
- Verify: `kappaEpsFunc` simplifies to `-(gam-1)*eps*rhoFunc[eps,n]^2 / (n^2 * Pfunc[eps,n])` (paper Eq. 33)
- Method: `FullSimplify[kappaEpsFunc[eps, n] - (-(gam-1)*eps*rhoFunc[eps,n]^2/(n^2*Pfunc[eps,n]))]` should be 0

**Test 2.4: $\kappa_n$**
- Compute: `D[muOverT[eps, n], n]` at constant `eps`
- Define: `kappaNFunc[eps_, n_] := rhoFunc[eps,n] * Tfunc[eps,n] * D[muOverT[eps, n], n]`
- Verify: simplifies to `rhoFunc[eps,n]/(n^2*Pfunc[eps,n]) * ((gam-1)*eps^2 + Pfunc[eps,n]^2)` (paper Eq. 34)

**Test 2.5: $\kappa_s = \kappa_\epsilon + \kappa_n$**
- Compute: `kappaEpsFunc + kappaNFunc`
- Verify: simplifies to `-(gam-1)*m*rhoFunc[eps,n]/n` (paper Eq. 38)

### Block 3: Sound Speed and Auxiliary Quantities

**Test 3.1: Sound speed $c_s^2 = p'_\epsilon + (n/\rho) p'_n$**
- Compute the general formula: `pPeps + n/rho * pPn`
- Verify equals `gam*P/rho` (paper Eq. 37)
- Method: Substitute the ideal gas values and simplify

**Test 3.2: $\omega = \kappa_s/\kappa_\epsilon$**
- Compute: `kappaSFunc / kappaEpsFunc`
- Verify equals `m*n*P/(eps*rho)` (paper Eq. 39)

**Test 3.3: $\alpha = p'_\epsilon / c_s^2$**
- Compute: `(gam - 1) / (gam*P/rho)`
- Verify equals `(gam-1)*rho/(gam*P)` (paper Eq. 40)

**Test 3.4: $\alpha\omega$ simplification**
- Compute: `alpha * omega`
- Verify equals `(gam-1)*m*n/(gam*eps)` (derivation in Sec. 3.5 of mathematical-derivations.md)

**Test 3.5: Verify $\alpha \geq 1$ for the ideal gas**
- Compute `alpha - 1` and show it simplifies to `(gam-1)*m*n / (gam*P)`, which is manifestly positive
- Method: `Simplify[alpha - 1 /. {alpha -> (gam-1)*rho/(gam*P), rho -> eps + P, P -> (gam-1)*(eps - m*n)}]`

### Block 4: Transport Coefficients from Frame Ansatz

**Test 4.1: Frame definitions**
- Define all transport coefficients from the frame ansatz (paper Eq. 41):
  ```
  etaV = rho*cs2*L*hatEta
  zetaV = rho*cs2*L*hatZeta
  sigmaV = hatV*L*rho*cs2/(-kappaEps) * hatSigma
  tauEps = L*hatV*hatTau
  tauQ = L*hatV*hatTau
  tauP = 2*(gam-1)*L*hatV
  ```
- Verify: `Vcomb == rho*cs2*L*hatV` where `Vcomb = 4*etaV/3 + zetaV` (paper Eq. 42)
- Verify: `hatV == 4*hatEta/3 + hatZeta` (paper Eq. 43)
- Verify: `tauP == 2*alpha*cs2*L*hatV` (paper Eq. A11, using $\alpha c_s^2 = \Gamma - 1$)

**Test 4.2: $\beta_\epsilon$ for the ideal gas frame**
- Compute `betaEps = tauQ * pPeps + sigmaV/rho * kappaEps`
- Verify equals `(gam-1)*tauQ - (gam-1)*sigmaV*eps*rho/(n^2*P)` (paper Eq. 35)
- Then substitute frame ansatz and verify:
  `betaEps == L*hatV*cs2*(alpha*hatTau - hatSigma)` (derived in Sec. 5.3 of derivations)

**Test 4.3: $\beta_n$ for the ideal gas frame**
- Compute `betaN = tauQ * pPn + sigmaV/n * kappaN`
- Verify equals `-(gam-1)*m*tauQ + sigmaV*rho/(n^3*P)*((gam-1)*eps^2 + P^2)` (paper Eq. 36)

### Block 5: The $\delta = 0$ Identity

**Test 5.1: $\delta = 0$ (general EOS)**
- Compute: `delta = betaEps*rho + betaN*n - rho*cs2*tauQ - sigmaV*kappaS`
- Substitute definitions of `betaEps`, `betaN` from Eqs. 18-19
- Factor into $\tau_Q$-terms and $\sigma$-terms
- Verify each group is zero independently:
  - $\tau_Q$-group: `pPeps*rho + pPn*n - rho*cs2` should be 0 (from definition of $c_s^2$)
  - $\sigma$-group: `kappaEps + kappaN - kappaS` should be 0 (by definition)
- Final: `FullSimplify[delta]` should be 0
- Method: This is an algebraic identity that holds for any EOS. Use `FullSimplify` with general symbolic `pPeps, pPn, cs2, kappaEps, kappaN, kappaS` and the identities `cs2 == pPeps + n/rho*pPn` and `kappaS == kappaEps + kappaN`.

**Test 5.2: $\delta = 0$ (ideal gas, explicit)**
- Substitute all ideal gas microphysics values into `delta`
- `FullSimplify` should give 0

### Block 6: Characteristic Speeds

**Test 6.1: Define $A, B, C$ (paper Eqs. A2-A4)**
- `AA = rho*tauEps*tauQ`
- `BB = -tauEps*(rho*cs2*tauQ + Vcomb + sigmaV*kappaS) - rho*tauP*tauQ`
- `CC = tauP*(rho*cs2*tauQ + sigmaV*kappaS) - betaEps*Vcomb`

**Test 6.2: $c_\pm^2$ from the quadratic formula**
- Compute `cPlus2` and `cMinus2` from $(-B \pm \sqrt{B^2 - 4AC})/(2A)$
- Substitute the frame ansatz values for all transport coefficients
- Verify the result matches the paper's formula (paper Eq. A15):
  ```
  cpm2 = cs2/(2*hatTau) * (2*alpha - omega*hatSigma + hatTau + 1
         +/- Sqrt[omega*hatSigma*(4*alpha + omega*hatSigma) + (2*alpha+1)^2
                  - 2*(omega+2)*hatSigma + hatTau^2 + hatTau*(2-2*omega*hatSigma)])
  ```
- Method: Substitute frame ansatz into $A, B, C$, compute $B/A$ and $C/A$, then compute $(B/A)^2 - 4C/A$ and simplify. Compare with the paper's discriminant.

**Test 6.3: $c_1^2$ (shear-mode speed)**
- Compute: `c12 = etaV/(rho*tauQ)`
- Substitute frame ansatz: verify equals `cs2*hatEta/(hatV*hatTau)` (paper Eq. A16)
- Alternate form: `c12 == cs2*etaV/(Vcomb*hatTau)` -- verify

**Test 6.4: Verify $c_\pm^2 > 0$ numerically**
- For a sample state (e.g., `gam = 4/3, eps = 1, n = 0.5, m = 0.1, hatEta = 1, hatZeta = 0, hatSigma = 0, hatTau = 5, L = 1`), compute `cPlus2` and `cMinus2` and verify both are positive and less than 1.

### Block 7: Rescaled Constraint Shorthand

**Test 7.1: $\hat{B}$ derivation**
- Define `hatB = BB/(rho*cs2*tauEps*tauQ)`
- Substitute frame ansatz
- Verify equals `-(1 + L*hatV/tauQ*(1 - omega*hatSigma) + tauP/(cs2*tauEps))` (paper Eq. A7)
- With the frame ansatz $\tau_\epsilon = \tau_Q = L\hat{V}\hat{\tau}$: verify `hatB == -(1 + 1/hatTau*(1 - omega*hatSigma) + 2*alpha/hatTau)`

**Test 7.2: $\hat{C}$ derivation**
- Define `hatC = CC/(rho*cs2^2*tauEps*tauQ)`
- Substitute frame ansatz
- Verify matches paper Eq. A7, second line

**Test 7.3: $\hat{D}$ derivation**
- Define `DD = rho*cs2*(tauEps + tauQ) + Vcomb + sigmaV*kappaEps`
- Define `hatD = DD/(rho*cs2*(tauEps + tauQ))`
- Substitute frame ansatz (with `tauEps = tauQ`)
- Verify equals `1 + L*hatV/(2*tauEps)*(1 - hatSigma)` (paper Eq. A7)
- With the frame ansatz: verify `hatD == 1 + (1 - hatSigma)/(2*hatTau)`

**Test 7.4: $\hat{E}$ derivation**
- Define `EE = sigmaV*(pPeps*kappaS - cs2*kappaEps)`
- Define `hatE = EE/(rho*cs2^2*(tauEps + tauQ))`
- Substitute frame ansatz
- Verify equals `hatSigma*L*hatV/(tauEps + tauQ)*(1 - alpha*omega)` (paper Eq. A7)
- With the frame ansatz: verify `hatE == hatSigma*(1 - alpha*omega)/(2*hatTau)`

### Block 8: Stability Constraint Verification

**Test 8.1: STAB line 1 ($|\hat{B}| \geq \hat{D}$) is automatic**
- Compute `|hatB| - hatD` with the frame ansatz
- Verify it simplifies to a manifestly nonneg expression: `1/(2*hatTau)*(1 + hatSigma*(1-2*omega)) + 2*alpha/hatTau` (or similar)
- Method: `FullSimplify[Abs[hatB] - hatD /. frameAnsatz, assumptions]` and check sign

**Test 8.2: STAB line 4 ($\hat{D} - \hat{E} \geq 1$) reduces to $\hat{\sigma} \leq 1/(2-\alpha\omega)$**
- Compute `hatD - hatE - 1` with the frame ansatz
- Verify equals `(1 - (2 - alpha*omega)*hatSigma)/(2*hatTau)`
- Since `2*hatTau > 0`, the constraint is `1 - (2 - alpha*omega)*hatSigma >= 0`
- Verify: `FullSimplify[(hatD - hatE - 1)*2*hatTau]` should give `1 - (2-alpha*omega)*hatSigma`

**Test 8.3: STAB line 4 implies STAB line 2**
- Show `hatE >= 0` (since `1 - alpha*omega > 0` and `hatSigma >= 0`)
- Then `hatD >= 1 + hatE >= 1`

**Test 8.4: Verify all 6 STAB constraints numerically**
- For a concrete parameter set (`gam = 4/3, hatEta = 1, hatZeta = 0, hatSigma = 1/4, hatTau = 5, alpha = 2, omega = 0.1`), numerically evaluate all 6 lines of the rescaled constraints and check they hold.

### Block 9: Causality Constraint Verification

**Test 9.1: CAUS A reduces to $\hat{\tau} > c_s^2 \eta/V$**
- From `rho*tauQ > etaV`: substitute frame ansatz
- `rho*L*hatV*hatTau > rho*cs2*L*hatEta`
- Simplifies to `hatV*hatTau > cs2*hatEta`, i.e., `hatTau > cs2*hatEta/hatV`
- Verify: `FullSimplify[rho*tauQ - etaV /. frameAnsatz]` and check it equals `rho*L*hatV*(hatTau - cs2*hatEta/hatV)`

**Test 9.2: First half of CAUS C ($2A > -B$) gives the second line of Eq. A13**
- Compute `2*AA + BB` with frame ansatz
- Verify the condition `2*hatTau > cs2*(2*alpha - omega*hatSigma + hatTau + 1)` (paper Eq. A13, line 2)

**Test 9.3: CAUS D ($A + B + C > 0$) gives the third line of Eq. A13**
- Compute `AA + BB + CC` with frame ansatz
- Verify the condition matches `cs2^2*(-2*alpha*omega*hatSigma + hatSigma + alpha*hatTau) + hatTau^2 >= cs2*hatTau*(2*alpha - omega*hatSigma + hatTau + 1)` (paper Eq. A13, line 3)

**Test 9.4: Simplified causality bound (paper Eq. A14)**
- Take the third line of Eq. A13, set `hatSigma = 0`, and solve for `hatTau`
- Verify the bound: `hatTau >= ((gam-1)*(2-cs2) + cs2)/(1-cs2)` (paper Eq. A14)
- Method: `Reduce[cs2^2*alpha*hatTau + hatTau^2 >= cs2*hatTau*(2*alpha + hatTau + 1), hatTau, Reals]` with substitution `alpha = (gam-1)/cs2`

**Test 9.5: Footnote 6 check ($\Gamma \to 2$)**
- Substitute `gam = 2` into the simplified causality bound
- Verify `hatTau >= 2/(1 - cs2)`

### Block 10: Entropy and Chemical Potential

**Test 10.1: Entropy density ODE**
- Define the entropy density from paper Eq. 29:
  `sFull[eps_, n_] := m*n*(1/((gam-1)*m)*Log[e[eps,n]/n^(gam-1)] + C0)`
- Verify the first law relation: `D[eps, s, n fixed] == T` (check $(\partial\epsilon/\partial s)_n = T$)
- Method: Compute $\partial s/\partial\epsilon|_n$ and verify it equals $1/T$

**Test 10.2: Chemical potential from Euler relation**
- Compute `mu = (rho - T*s)/n`
- Substitute the ideal gas expressions for `rho`, `T`, `s`
- Verify matches paper Eq. 30: `mu == m + m*e*(gam - Log[e/n^(gam-1)] + const)`

**Test 10.3: Thermodynamic identity (Gibbs-Duhem based)**
- Verify: `dP/rho == dT/T + n*T/rho * d(mu/T)` (paper Eq. 82)
- Method: Compute both sides for infinitesimal changes `deps`, `dn` and verify equality
- In Mathematica: compute `(D[Pfunc, eps]*deps + D[Pfunc, n]*dn) / rhoFunc` and compare with `(D[Tfunc, eps]*deps + D[Tfunc, n]*dn)/Tfunc + n*Tfunc/rhoFunc * (D[muOverT, eps]*deps + D[muOverT, n]*dn)`

### Block 11: Eckart Limit Verification

**Test 11.1: BDNK reduces to Eckart heat flux**
- Set `tauQ = -kappaTherm*T/rho` in the BDNK `Q^a` formula
- Compute `betaEps*nabla_eps + betaN*nabla_n` symbolically
- Verify it reduces to `-kappaTherm*nabla_T` (paper Footnote 5, Sec. 4.4 of derivations)
- Method: Define symbolic gradient components, substitute, and verify cancellation

**Test 11.2: Alternative heat flux form**
- Verify: `betaEps*nabla_eps + betaN*nabla_n == gammaHF*nabla_P - kappaTherm*nabla_T` (paper Eq. 83)
- Where `gammaHF = tauQ + sigmaV*rho/n^2` (paper Eq. 84)

### Block 12: Bjorken Flow Verification

**Test 12.1: Inviscid Bjorken solution**
- Solve the ODE `eps'[tau] + gam*eps[tau]/tau - (gam-1)*m*n0/tau^2 == 0`
- Verify solution: `eps[tau] == m*n0/tau*(1 + e0*tau^(-(gam-1)))` (paper Eq. 67)
- Method: `DSolve[{eps'[tau] + gam*eps[tau]/tau == (gam-1)*m*n0/tau^2}, eps[tau], tau]`

**Test 12.2: $\hat{\tau} \to \infty$ limit**
- Solve `eps''[tau] + 2/tau*eps'[tau] == 0`
- Verify solution: `eps[tau] == C1/tau + C2` (paper Eq. 68)
- Method: `DSolve[{eps''[tau] + 2/tau*eps'[tau] == 0}, eps[tau], tau]`

**Test 12.3: Pressure positivity constraint**
- From `rho > etaV/tauQ` and the ideal gas EOS
- Verify: `P > (gam-1)/gam * (etaV/tauQ - m*n)` (paper Eq. 69)

### Block 13: Heat Flow Equations

**Test 13.1: Eckart heat equation**
- From the BDNK PDEs with `tauEps = tauP = 0, gammaHF = 0, kappa = const`:
- Verify the result is `dotT == alphaE * T''` where `alphaE = kappaTherm*(gam-1)/n` (paper Eq. 89)

**Test 13.2: Telegrapher's equation (hybrid frame)**
- With `tauEps > 0, tauP = 0, gammaHF = 0`:
- Verify: `tauEps*ddotT + dotT - alphaE*T'' == 0` (paper Eq. 90)
- Define `ch2 = kappaTherm*(gam-1)/(n*tauEps)` and verify `ch2 == alphaE/tauEps`

**Test 13.3: BDNK generalized telegrapher's equation**
- With all BDNK coefficients nonzero:
- Define `cB2 = ch2*(1 - gammaHF*n/kappaTherm)` (paper Eq. 91)
- Verify the PDE structure: `ddotT - cB2*T'' + (1/tauEps)*dotT + l.o.t. == 0`

**Test 13.4: Pressure relaxation stability**
- Define `thetaHF = (-kappaTherm + gammaHF*n + tauP*n/(gam-1))/1` (paper Eq. 92 denominator)
- Define `tauTheta = thetaHF/n`
- Verify: for Eckart (`gammaHF=0, tauP=0`), `tauTheta = -kappaTherm/n < 0` (unstable)
- Verify: for BDNK with the frame ansatz, `tauTheta > 0` (stable) when `hatSigma <= 1/3`

### Block 14: Shockwave Structure

**Test 14.1: Baryon conservation ODE**
- From `(n*W*v)' = 0` where `W = 1/Sqrt[1-v^2]`:
- Derive `n' = -W^2*n/v * v'` (paper Eq. 72)
- Method: Use implicit differentiation and verify algebraically

**Test 14.2: Rankine-Hugoniot conditions**
- Write `T0^{tx} = rho*W^2*v`, `T0^{xx} = rho*W^2*v^2 + P`, `J^x = n*W*v`
- Verify the structure of the jump conditions (paper Eq. 80)

---

## 3. Key Mathematica Functions to Use

| Function | Usage |
|---|---|
| `FullSimplify[expr, Assumptions -> ...]` | Primary symbolic simplification with domain assumptions |
| `Simplify[expr]` | Lighter-weight simplification |
| `Reduce[ineq, var, Reals]` | Reduce inequalities symbolically (for constraint analysis) |
| `Solve[expr == 0, var]` | Solve equations |
| `DSolve[ode, y[x], x]` | Solve ODEs symbolically (Bjorken inviscid, telegrapher's) |
| `D[expr, var]` | Partial derivatives (for microphysics derivatives) |
| `ReplaceAll` (/.`) | Substitute frame ansatz, ideal gas values |
| `Together` | Combine rational expressions over common denominator |
| `Factor` | Factor polynomial expressions |
| `Expand` | Expand products |
| `PowerExpand` | Expand `Log[a*b]` etc. |
| `Positive[expr]` or `TrueQ[Simplify[expr > 0]]` | Check positivity of expressions |
| `$Assumptions` | Global assumption variable |
| `Assuming[assns, expr]` | Local assumption wrapper |
| `Refine[expr, assns]` | Simplify under assumptions (for `Abs`, `Sign`, etc.) |
| `Print[...]` | Output test results |

---

## 4. Expected Outputs

The script should produce output of the form:

```
==========================================
 BDNK Derivation Verification Script
 Paper: Pandya, Most, Pretorius (2023)
==========================================

--- Block 1: EOS Fundamentals ---
[PASS] Test 1.1: eps = m*n*(1+e) identity
[PASS] Test 1.2: P = (Gamma-1)*(eps - m*n)
[PASS] Test 1.3: P = n*T
[PASS] Test 1.4: rho = Gamma*eps - (Gamma-1)*m*n

--- Block 2: Microphysics Derivatives ---
[PASS] Test 2.1: p'_eps = Gamma - 1
[PASS] Test 2.2: p'_n = -(Gamma - 1)*m
[PASS] Test 2.3: kappa_eps formula
[PASS] Test 2.4: kappa_n formula
[PASS] Test 2.5: kappa_s = -(Gamma-1)*m*rho/n

--- Block 3: Sound Speed and Auxiliary ---
[PASS] Test 3.1: cs2 = Gamma*P/rho
[PASS] Test 3.2: omega = m*n*P/(eps*rho)
[PASS] Test 3.3: alpha = (Gamma-1)*rho/(Gamma*P)
[PASS] Test 3.4: alpha*omega = (Gamma-1)*m*n/(Gamma*eps)
[PASS] Test 3.5: alpha >= 1

... (etc. for all blocks)

==========================================
 SUMMARY: 45/45 tests passed
==========================================
```

If any test fails, the script should print the residual expression so the user can debug.

---

## 5. Implementation Notes

### 5.1 Handling $\mu/T$

The quantity $\mu/T$ requires the entropy density $s$, which involves an integration constant. The key insight is that the derivatives $\partial(\mu/T)/\partial\epsilon$ and $\partial(\mu/T)/\partial n$ do not depend on the integration constant. The script should:

1. Define `muOverT[eps_, n_]` with `Module[{eLocal, logArg}, ...]`
2. Use `e[eps, n] = eps/(m*n) - 1`
3. Write `muOverT = 1/((gam-1)*e) + (gam - Log[e/n^(gam-1)] + C0)/(gam-1)`
4. Verify that derivatives of `muOverT` w.r.t. `eps` and `n` are independent of `C0`

### 5.2 Avoiding Mathematica pitfalls

- **`Gamma` collision**: Always use `gam` for the adiabatic index
- **`Abs` in constraints**: Since `hatB < 0` for our parameter range, use `Refine[Abs[hatB], hatB < 0]` which gives `-hatB`
- **Branching in `Sqrt`**: For the discriminant in $c_\pm^2$, verify it is nonneg before taking the square root
- **Timeout**: Some `FullSimplify` calls on the "complicated" stability constraints (STAB B, D, E) may be slow. Set `TimeConstrained[FullSimplify[...], 120]` and report timeout as `[SKIP]` rather than hanging.
- **Substitution order**: Always substitute the ideal gas microphysics first, then the frame ansatz, then simplify. This order minimizes expression complexity.

### 5.3 Script structure

```mathematica
(* derivations.wl *)
(* BDNK Derivation Verification Script *)
(* Verifies all derivations from Pandya, Most, Pretorius *)

(* ---------- SETUP ---------- *)
$Assumptions = { ... };
passCount = 0; failCount = 0; skipCount = 0;
TestResult[label_, expr_, expected_:0] := Module[{res},
  res = TimeConstrained[FullSimplify[expr - expected, $Assumptions], 120, $Failed];
  If[res === $Failed,
    Print["[SKIP] ", label, " (timeout)"];
    skipCount++,
  If[res === 0,
    Print["[PASS] ", label];
    passCount++,
    Print["[FAIL] ", label, " -- residual: ", res];
    failCount++
  ]]
];

(* ---------- DEFINITIONS ---------- *)
e[eps_, n_] := eps/(m*n) - 1;
Pfunc[eps_, n_] := (gam - 1)*m*n*e[eps, n];
(* ... etc. *)

(* ---------- BLOCK 1: EOS ---------- *)
Print["--- Block 1: EOS Fundamentals ---"];
TestResult["Test 1.1: eps = m*n*(1+e)", m*n*(1 + e[eps, n]) - eps];
(* ... etc. *)

(* ---------- SUMMARY ---------- *)
Print["=========================================="];
Print[" SUMMARY: ", passCount, "/", passCount + failCount + skipCount, " passed"];
If[failCount > 0, Print[" FAILURES: ", failCount]];
If[skipCount > 0, Print[" SKIPPED: ", skipCount]];
Print["=========================================="];
```

---

## 6. Verification Dependency Graph

The tests should be run in order because later tests depend on earlier definitions:

```
Block 1 (EOS)
    |
    v
Block 2 (Microphysics derivatives)
    |
    v
Block 3 (Sound speed, alpha, omega)
    |
    v
Block 4 (Frame ansatz, transport coefficients, beta_eps, beta_n)
    |
    v
Block 5 (delta = 0 identity)
    |
    v
Block 6 (Characteristic speeds c_pm, c_1)
    |
    v
Block 7 (Rescaled shorthand hatB, hatC, hatD, hatE)
    |
    v
Block 8 (Stability constraints)  +  Block 9 (Causality constraints)
    |                                  |
    +----------------------------------+
    |
    v
Block 10 (Entropy, chemical potential, thermodynamic identity)
    |
    v
Block 11 (Eckart limit)
    |
    v
Block 12 (Bjorken flow)  +  Block 13 (Heat flow)  +  Block 14 (Shockwave)
```

---

## 7. Total Test Count

| Block | Tests | Description |
|---|---|---|
| 1 | 4 | EOS fundamentals |
| 2 | 5 | Microphysics derivatives |
| 3 | 5 | Sound speed, alpha, omega |
| 4 | 3 | Frame ansatz, beta coefficients |
| 5 | 2 | delta = 0 identity |
| 6 | 4 | Characteristic speeds |
| 7 | 4 | Rescaled shorthand |
| 8 | 4 | Stability constraints |
| 9 | 5 | Causality constraints |
| 10 | 3 | Entropy, chemical potential, thermo identity |
| 11 | 2 | Eckart limit |
| 12 | 3 | Bjorken flow |
| 13 | 4 | Heat flow |
| 14 | 2 | Shockwave structure |
| **Total** | **50** | |
