# Plan: Mathematical Derivations Document

## Overview

This document plans the structure and content for `mathematical-derivations.md`, which will provide **non-step-skipping derivations** of every mathematical result in the paper "Causal, stable first-order viscous relativistic hydrodynamics with ideal gas microphysics" by Pandya, Most, Pretorius.

The guiding principle: if the paper writes "one can show that X" or jumps from equation A to equation B, the derivations document fills in every intermediate algebraic step.

---

## I. Dependency Map (What Must Be Derived First)

The derivations form a directed acyclic graph. The ordering below respects all dependencies.

```
Layer 0 (Foundations — no dependencies):
  - Tensor decomposition of T^{ab}, J^a w.r.t. u^a
  - Definition of projection operator Delta^{ab}
  - Traceless-transverse projector <ab>
  - Gradient expansion philosophy

Layer 1 (Ideal fluid):
  - Ideal fluid constitutive relations (E_0=epsilon, P_0=P, etc.)
  - Relativistic Euler equations from ideal conserved currents

Layer 2 (Microphysics — depends on Layer 0):
  - EOS: P = (Gamma-1) m n e = n T
  - Specific internal energy e and epsilon = mn(1+e)
  - Entropy density s(epsilon, n) from first law
  - Chemical potential mu(epsilon, n) from Euler relation
  - Thermodynamic identity dP/rho = dT/T + (nT/rho) d(mu/T)

Layer 3 (Microphysics derivatives — depends on Layer 2):
  - p'_epsilon, p'_n
  - kappa_epsilon, kappa_n, kappa_s
  - Sound speed c_s^2
  - omega, alpha

Layer 4 (BDNK theory — depends on Layers 1, 2, 3):
  - BDNK constitutive relations (script E, P, Q^a, T^{ab}, N, J^a)
  - beta_epsilon, beta_n from microphysics
  - On-shell nature of regularizing terms (scalar and vector)
  - Connection between BDNK and Eckart heat flux

Layer 5 (Hydrodynamic frame — depends on Layer 4):
  - Frame ansatz: eta, zeta, sigma, tau_epsilon, tau_P, tau_Q
  - Combined viscosity V, inverse Reynolds number V-hat
  - Characteristic speeds c_pm, c_1

Layer 6 (Constraint simplification — depends on Layers 3, 4, 5):
  - Rescaled shorthand B-hat, C-hat, D-hat, E-hat
  - Linear stability constraint simplification
  - Causality constraint simplification
  - Derivation of the two simple constraints (sigma-hat <= 1/3, tau-hat bound)

Layer 7 (Applications — depends on all above):
  - Equilibrium state comparison (Eckart, MIS, BDNK)
  - Bjorken flow EOM
  - Shockwave ODE system
  - Heat flow equations (Eckart, hybrid, BDNK forms)
```

---

## II. Section-by-Section Plan

### Section 1: Tensor Decomposition and Gradient Expansion

**Derivations needed:**

1.1. **Projection operator properties**
   - Show Delta^{ab} = g^{ab} + u^a u^b projects orthogonal to u^a:
     verify u_a Delta^{ab} = 0, Delta^a_c Delta^{cb} = Delta^{ab}, Delta^a_a = 3.
   - *Status in paper:* Stated without proof (Sec. II.A, below Eq. 5).

1.2. **Traceless-transverse projector**
   - Show that X^{<ab>} as defined is (i) symmetric, (ii) traceless (g_{ab} X^{<ab>} = 0), and (iii) orthogonal to u^a in both indices.
   - *Status in paper:* Defined in Eq. 9 but properties stated without verification.

1.3. **Decomposition of T^{ab} and J^a**
   - Verify that inserting the projection definitions (Eq. 8) into the decomposition (Eqs. 6-7) recovers the identity T^{ab} = T^{ab}, J^a = J^a.
   - Verify the ideal fluid constitutive relations: E_0 = epsilon, P_0 = P, Q_0^a = 0, T_0^{ab} = 0, N_0 = n, J_0^a = 0.
   - *Status in paper:* Asserted in text below Eq. 8.

1.4. **Relativistic Euler equations**
   - Derive the explicit form of nabla_a T_0^{ab} = 0 and nabla_a J_0^a = 0 for the ideal fluid.
   - Decompose into scalar (u_b projection) and vector (Delta^a_b projection) parts:
     - Scalar: u^b nabla_b epsilon + rho nabla_b u^b = 0
     - Vector: rho u^b nabla_b u^a + Delta^{ab} nabla_b P = 0
   - *Status in paper:* These appear as Eqs. 40-41 but are stated without derivation; they are the "regularizing terms."

---

### Section 2: Ideal Gas Microphysics

**Derivations needed:**

2.1. **Equation of state and specific internal energy**
   - Start from P = (Gamma-1) m n e and epsilon = mn(1+e).
   - Derive e(epsilon, n) = epsilon/(mn) - 1.
   - Derive T(epsilon, n) = P/n = (Gamma-1)(epsilon/n - m).
   - Verify P = (Gamma-1)(epsilon - mn).
   - *Status in paper:* Eqs. 14-15 stated; the expression T = P/n is implicit.

2.2. **Entropy density from the first law** (CRITICAL — steps skipped in paper)
   - Start from first law: dU = T dS - P dV + mu_N dN.
   - Rewrite as de = T d(s/(nm)) - P d(1/(nm)).
   - Expand the differentials on the RHS:
     d(s/(nm)) = ds/(nm) - s dn/(n^2 m)
     d(1/(nm)) = -dn/(n^2 m)
   - Substitute and collect terms.
   - "Divide by dn" (hold epsilon constant), substitute P = (Gamma-1)mne and T = (Gamma-1)mne/n... but this requires careful handling since e = e(epsilon,n).
   - Integrate the resulting ODE to obtain s(epsilon,n) = mn[1/((Gamma-1)m) ln(e/n^{Gamma-1}) + const].
   - *Status in paper:* Major steps skipped between Eq. 16 and Eq. 17. The paper says "expand, divide by dn, substitute, and integrate" — we must show every step.

2.3. **Chemical potential from Euler relation**
   - Start from rho = Ts + n mu (Eq. 16).
   - Solve for mu = (rho - Ts)/n.
   - Substitute rho = epsilon + P, the expression for s from 2.2, and T = P/n.
   - Simplify to obtain mu(epsilon,n) = m + me[Gamma - ln(e/n^{Gamma-1}) + const].
   - *Status in paper:* Jump from Eq. 17 to Eq. 18 with just "inserting."

2.4. **Thermodynamic identity derivation**
   - Derive dP/rho = dT/T + (nT/rho) d(mu/T) (Eq. 53).
   - Start from the Gibbs-Duhem relation: dP = s dT + n d mu_N = s dT + n d(mu - m) = s dT + n dmu.
   - Divide by rho and manipulate to obtain the stated form.
   - *Status in paper:* Eq. 53 stated without derivation; needed for the heat flow section.
   - *External reference needed:* Standard thermodynamics, but derivation should be self-contained.

---

### Section 3: Derivatives of Microphysics Quantities

**Derivations needed:**

3.1. **p'_epsilon = (dP/d epsilon)_n = Gamma - 1**
   - From P = (Gamma-1)(epsilon - mn), differentiate w.r.t. epsilon at constant n.
   - *Status in paper:* Result stated (Eq. 19); derivation is one line but should be shown.

3.2. **p'_n = (dP/d n)_epsilon = -(Gamma-1)m**
   - From P = (Gamma-1)(epsilon - mn), differentiate w.r.t. n at constant epsilon.
   - *Status in paper:* Result stated (Eq. 20).

3.3. **kappa_epsilon derivation** (CRITICAL — nontrivial)
   - Need to compute (d(mu/T)/d epsilon)_n.
   - First compute mu/T as a function of epsilon, n using results from Sec. 2.
   - mu/T = [m + me(Gamma - ln(e/n^{Gamma-1}) + const)] / [(Gamma-1)me]
   - Simplify.
   - Differentiate w.r.t. epsilon at constant n.
   - Multiply by rho^2 T / n.
   - Show result: kappa_epsilon = -(Gamma-1) epsilon rho^2 / (n^2 P).
   - *Status in paper:* Result stated (Eq. 21); intermediate steps entirely skipped.

3.4. **kappa_n derivation** (CRITICAL — nontrivial)
   - Compute (d(mu/T)/d n)_epsilon.
   - Differentiate mu/T w.r.t. n at constant epsilon.
   - Multiply by rho T.
   - Show result: kappa_n = rho/(n^2 P) [(Gamma-1)epsilon^2 + P^2].
   - *Status in paper:* Result stated (Eq. 22); intermediate steps entirely skipped.

3.5. **kappa_s = kappa_epsilon + kappa_n**
   - Direct addition; verify simplification to -(Gamma-1) m rho/n.
   - *Status in paper:* Eq. 23 defines it; Eq. 28 gives the result. Show the algebra.

3.6. **beta_epsilon derivation**
   - Substitute p'_epsilon, kappa_epsilon, and sigma/(rho) into beta_epsilon = tau_Q p'_epsilon + (sigma/rho) kappa_epsilon.
   - Note: the factor is sigma/rho, not sigma/n — verify from Eq. 11.
   - Show result: beta_epsilon = (Gamma-1)tau_Q - (Gamma-1) sigma epsilon rho/(n^2 P).
   - *Status in paper:* Result stated (Eq. 26); substitution steps skipped.

3.7. **beta_n derivation**
   - Substitute p'_n, kappa_n into beta_n = tau_Q p'_n + (sigma/n) kappa_n.
   - Show result: beta_n = -(Gamma-1)m tau_Q + sigma rho/(n^3 P)[(Gamma-1)epsilon^2 + P^2].
   - *Status in paper:* Result stated (Eq. 27).

3.8. **Sound speed derivation** (CRITICAL — nontrivial)
   - Start from c_s^2 = (dP/d epsilon)_{s-bar} where s-bar = S/N = entropy per particle.
   - Show the identity: (dP/d epsilon)_{s-bar} = (dP/d epsilon)_n + (n/rho)(dP/dn)_epsilon.
   - This requires using the chain rule and the relation between holding s-bar constant vs. holding n constant.
   - Specifically: need to derive ds-bar = 0 implies a relation between depsilon and dn, then use it.
   - Substitute p'_epsilon = Gamma-1 and p'_n = -(Gamma-1)m.
   - Show c_s^2 = (Gamma-1)[1 - mn/rho] = (Gamma-1)(epsilon+P-mn)/(epsilon+P) ... but this doesn't immediately simplify to Gamma P/rho.
   - Key step: epsilon + P - mn = P + (epsilon - mn) = P + P/(Gamma-1) = Gamma P/(Gamma-1).
   - So c_s^2 = (Gamma-1) * Gamma P/((Gamma-1) rho) = Gamma P/rho.
   - *Status in paper:* The identity and final result are stated in Eq. 24 but the intermediate steps are skipped.

3.9. **omega and alpha**
   - omega = kappa_s/kappa_epsilon = mnP/(epsilon rho) — derive by direct division.
   - alpha = p'_epsilon/c_s^2 = (Gamma-1)/(Gamma P/rho) = rho/Gamma P ... wait, paper says alpha = (Gamma-1)/c_s^2. Verify.
   - Check: alpha = (Gamma-1)/c_s^2 = (Gamma-1) rho/(Gamma P). Show this equals rho/(Gamma P) * (Gamma-1). Verify range alpha >= 1.
   - *Status in paper:* Eqs. 29-30 state results.

---

### Section 4: BDNK Conserved Currents

**Derivations needed:**

4.1. **BDNK stress-energy tensor: explicit form**
   - Insert the constitutive relations (Eqs. 10-15) into the decomposition (Eq. 6).
   - Write out T^{ab} explicitly in terms of epsilon, n, u^a, and gradients.
   - *Status in paper:* Left in component form.

4.2. **On-shell equivalence of regularizing terms** (IMPORTANT)
   - Show that the terms added to Eckart theory to get BDNK theory are proportional to projections of the relativistic Euler equations (Eqs. 40-41).
   - The scalar term u^a nabla_b T_0^{ab} = u^b nabla_b epsilon + rho nabla_b u^b appears in script-E and script-P.
   - The vector term Delta^a_c nabla_b T_0^{bc} = rho u^b nabla_b u^a + Delta^{ab} nabla_b P appears in Q^a.
   - Show these are O(nabla^2) on-shell (i.e., when evaluated on solutions to the Euler equations, they vanish, so adding them to the conserved currents only changes T^{ab} at O(nabla^2)).
   - *Status in paper:* Discussed in text around Eqs. 40-41 but proof is sketched, not derived.

4.3. **Eckart theory as a special case of BDNK**
   - Show that setting tau_epsilon = tau_P = 0 and tau_Q = -kappa T/rho in the BDNK Q^a reproduces the Eckart heat flux.
   - The Eckart heat flux: Q^a_E = -kappa T(u^c nabla_c u^a + Delta^{ac}/T nabla_c T).
   - Start from BDNK Q^a (Eq. 12), substitute Eckart tau_Q, and use the thermodynamic identity to convert beta_epsilon nabla_c epsilon + beta_n nabla_c n to the form involving nabla_c T.
   - *Status in paper:* Stated in Footnote 4 and Eq. 32-33; details of the conversion are not shown.
   - *External reference:* Footnote references thermodynamic identity Eq. 53.

4.4. **Connection Q^a_BDNK = Q^a_Eckart + tau_Q * (transverse Euler eq)**
   - Show explicitly that the BDNK heat flux differs from Eckart by Eq. 41 times tau_Q (plus corrections).
   - *Status in paper:* Stated in Footnote 4.

---

### Section 5: Hydrodynamic Frame Ansatz

**Derivations needed:**

5.1. **Frame ansatz substitution**
   - Substitute the frame ansatz (Eq. 31) into the definitions of A, B, C, D, E (Eqs. 56-60).
   - Show the resulting expressions in terms of hatted quantities.
   - *Status in paper:* The ansatz is stated; the substitution results appear in the rescaled forms (Eq. 67) in the appendix.

5.2. **tau_P = 2(Gamma-1) L V-hat = 2 alpha c_s^2 L V-hat**
   - Verify that 2(Gamma-1) = 2 alpha c_s^2 using alpha = (Gamma-1)/c_s^2.
   - This confirms consistency between Eq. 31 and Eq. 72.
   - *Status in paper:* Both forms stated but equivalence not shown.

5.3. **delta = 0 identity**
   - Compute delta = beta_epsilon rho + beta_n n - rho c_s^2 tau_Q - sigma kappa_s.
   - Substitute the definitions of beta_epsilon, beta_n (Eqs. 11-12) and show cancellation.
   - This is crucial for simplifying the shockwave ODE denominator.
   - *Status in paper:* Stated to "vanish identically" below Eq. 46 with no proof.

---

### Section 6: Characteristic Speeds

**Derivations needed:**

6.1. **Derivation of c_pm^2 from the shockwave ODE shared denominator**
   - Start from the shared denominator Av^4 + v^2(B - tau_epsilon delta) + (C + tau_P delta).
   - Use delta = 0 to get Av^4 + Bv^2 + C.
   - Solve quadratic in v^2: c_pm^2 = (-B +/- sqrt(B^2 - 4AC))/(2A).
   - *Status in paper:* Eq. 44 stated; derivation follows from Eq. 45 but intermediate steps of setting up the quadratic should be shown.

6.2. **Explicit c_pm^2 for the ideal gas frame** (CRITICAL)
   - Substitute A, B, C (Eqs. 56-58) with the frame ansatz (Eq. 31/72) into the general formula (Eq. 44).
   - Simplify using ideal gas microphysics to arrive at Eq. 75.
   - This is a substantial algebraic computation.
   - *Status in paper:* Result stated (Eq. 75); all intermediate steps skipped.

6.3. **c_1^2 for the ideal gas frame**
   - Show c_1^2 = c_s^2 eta/(V tau-hat) from the definition.
   - Need to identify what c_1 represents (the shear characteristic speed).
   - *Status in paper:* Eq. 76 stated.
   - *External reference:* The origin of c_1 as a characteristic speed comes from [Bemfica:2020zjp] Eq. (20).

---

### Section 7: Constraint Simplification (Appendix A)

**Derivations needed:**

7.1. **Rescaling of B, C, D, E to hatted forms** (DETAILED)
   - Show every step of converting B, C, D, E (Eqs. 56-60) to B-hat, C-hat, D-hat, E-hat (Eq. 67).
   - Substitute the frame ansatz tau_epsilon = tau_Q = L V-hat tau-hat, tau_P = 2 alpha c_s^2 L V-hat.
   - Factor out appropriate powers of rho, c_s^2, tau_epsilon, tau_Q, (tau_epsilon + tau_Q).
   - *Status in paper:* Results stated (Eq. 67); derivation skipped.

7.2. **Rescaling of stability constraints** (DETAILED)
   - Show every step converting STAB A1-E (Eqs. 63-66) into the rescaled form (Eq. 68).
   - This involves substituting B-hat etc. and cancelling common factors.
   - *Status in paper:* Results stated (Eq. 68); derivation skipped.

7.3. **Simplification: first line of (68) is automatic**
   - Show |B-hat| >= D-hat is automatically satisfied given the parameter ranges.
   - Substitute B-hat and D-hat, show |B-hat| - D-hat >= 0.
   - *Status in paper:* Stated in text; proof not given.

7.4. **Simplification: fourth line implies second line**
   - Show D-hat - E-hat >= 1 implies D-hat >= 1 when E-hat >= 0.
   - *Status in paper:* Stated in text.

7.5. **Simple stability constraint derivation** (IMPORTANT)
   - From D-hat - E-hat >= 1, substitute definitions to get 1 - (2 - alpha omega) sigma-hat >= 0.
   - Show this is implied by sigma-hat <= 1/2 (using 0 < alpha omega < 0.2).
   - Show the stronger bound sigma-hat <= 1/3 from Mathematica analysis of the complicated constraints.
   - *Status in paper:* Result (Eq. 69) stated; derivation of the simplified form shown but the step from 1/2 to 1/3 is attributed to Mathematica.
   - *External reference:* Mathematica notebook at GitHub for the three complicated constraints.

7.6. **Causality constraint simplification** (IMPORTANT)
   - Start from CAUS A-D (Eqs. 55-58).
   - Show CAUS B and second half of CAUS C are automatic given the frame ansatz and sigma-hat <= 1/3.
   - Derive the three remaining constraints (Eq. 73).
   - Show all three are implied by the single inequality tau-hat >= [(Gamma-1)(2-c_s^2)+c_s^2]/(1-c_s^2).
   - *Status in paper:* Eq. 73 stated; then Eq. 74 stated as implying all three. Only the claim about the sigma -> 0 limit is mentioned.

7.7. **Simpler causal bound by taking Gamma -> 2**
   - Show the footnote result: Gamma -> 2 in Eq. 74 gives tau-hat >= 2/(1-c_s^2).
   - *Status in paper:* Footnote 6; one-line derivation needed.

---

### Section 8: Equilibrium State Comparison (Eckart / MIS / BDNK)

**Derivations needed:**

8.1. **Baryon conservation for spatially isotropic states**
   - From J^a = n u^a with u^i = 0, spatial isotropy, show nabla_a J^a = 0 implies n-dot = 0.
   - *Status in paper:* Result stated (Eq. 36).

8.2. **Stress-energy conservation for spatially isotropic states**
   - Show only the t-component is nontrivial: T^{tt}_{,t} = 0.
   - Verify that T^{ti} = 0 and T^{ij}_{,i} = 0 by the assumed symmetry.
   - *Status in paper:* Eq. 37 stated.

8.3. **Eckart equation from T^{tt} = epsilon**
   - Show that for Eckart (tau_epsilon = 0), T^{tt} = epsilon directly.
   - *Status in paper:* Eq. 38, one line.

8.4. **BDNK relaxation equation**
   - From T^{tt} = epsilon + tau_epsilon epsilon-dot, derive epsilon-dot = (T^{tt} - epsilon)/tau_epsilon.
   - *Status in paper:* Eq. 39.

8.5. **MIS relaxation equation** (IMPORTANT — multiple steps)
   - Start from T^{ab}_{MIS} = T^{ab}_0 + pi^{ab} and the relaxation eq u^c nabla_c pi^{ab} = (pi^{ab}_{NS} - pi^{ab})/tau_pi.
   - For isotropic states: show Delta^{tt} = 0, C^t = 0, D^{tt} = 0.
   - Show nabla_c u^c = 0 by spatial isotropy.
   - Show the MIS equations reduce to: epsilon + pi^{tt} = T^{tt} and pi-dot^{tt} = (c_1 epsilon-dot - pi^{tt})/tau_pi.
   - Eliminate pi^{tt}: pi^{tt} = T^{tt} - epsilon, so pi-dot^{tt} = -epsilon-dot.
   - Substitute to get epsilon-dot = (T^{tt} - epsilon)/(tau_pi + c_1).
   - *Status in paper:* Eq. 39 through Eq. 42; several steps are compressed.

8.6. **Temperature frame dependence**
   - From T^{tt} = epsilon + delta_epsilon and EOS, derive T = (Gamma-1)/n (T^{tt} - mn) - tau_epsilon T-dot.
   - *Status in paper:* Eq. 43; derivation involves using chain rule on T(epsilon) and rearranging.

8.7. **Exponential relaxation solution**
   - Integrate epsilon-dot = (T^{tt} - epsilon)/tau when tau is constant.
   - Show epsilon(t) = T^{tt} + (epsilon_0 - T^{tt}) e^{-t/tau}.
   - *Status in paper:* Eq. 44; standard ODE solution.

8.8. **General relaxation equation derivation**
   - Compute u_a u_b T^{ab} from the BDNK stress-energy tensor.
   - Rearrange to get u^c nabla_c epsilon = (1/tau_epsilon)(u_a u_b T^{ab} - epsilon) - rho nabla_c u^c.
   - Show this equals (1/tau_epsilon) delta_epsilon - rho nabla_c u^c, which is the Euler eq + correction.
   - *Status in paper:* Eq. 45.

---

### Section 9: Bjorken Flow

**Derivations needed:**

9.1. **Milne coordinate setup**
   - State the metric, Christoffel symbols, and covariant derivatives in Milne coordinates.
   - *Status in paper:* Stated (around Eq. 46). Christoffel symbols should be derived from the metric.

9.2. **Baryon conservation in Milne coordinates**
   - Compute nabla_a J^a = nabla_a (n u^a) in Milne coordinates with u^a = (1,0,0,0).
   - Show this gives n-dot + n/tau = 0, hence n = n_0/tau.
   - *Status in paper:* Result stated; derivation requires explicit Christoffel symbol computation.

9.3. **Bjorken EOM derivation** (CRITICAL — many steps skipped)
   - Compute nabla_a T^{ab} = 0 in Milne coordinates.
   - The stress-energy tensor includes BDNK gradient corrections.
   - Need to compute all Christoffel-symbol contributions.
   - Must compute nabla_c u^c = 1/tau (from Christoffel symbols).
   - Must compute u^c nabla_c epsilon = epsilon-dot (since u^a = (1,0,0,0)).
   - Substitute the constitutive relations and simplify.
   - Show the only nontrivial component gives Eq. 47: tau_epsilon epsilon-ddot = -(1/tau)(tau + 2 tau_epsilon + tau_P) epsilon-dot - (1/tau^2)[rho(tau + tau_P) - V].
   - *Status in paper:* Eq. 47 stated with no derivation. This is one of the most important derivations to fill in.

9.4. **Inviscid Bjorken solution**
   - Take tau_epsilon, tau_P, V -> 0 in Eq. 47, getting epsilon-dot + rho/tau = 0.
   - Using rho = epsilon + P = epsilon + (Gamma-1)(epsilon - mn) = Gamma epsilon - (Gamma-1)mn, and n = n_0/tau:
     epsilon-dot + [Gamma epsilon - (Gamma-1)m n_0/tau]/tau = 0.
   - This is a first-order linear ODE. Solve by integrating factor.
   - Show the solution is epsilon(tau) = m n_0 tau^{-1} [1 + e_0 tau^{-(Gamma-1)}].
   - *Status in paper:* Eq. 48 stated; solution method not shown.

9.5. **Large tau-hat limit**
   - Take tau_epsilon -> infinity (keeping tau_P, V finite) in Eq. 47.
   - Show the equation reduces to epsilon-ddot = -2 epsilon-dot/tau.
   - Integrate: epsilon-dot = C/tau^2, then epsilon = -C/tau + c_2 = c_1 tau^{-1} + c_2.
   - *Status in paper:* Eq. 49 stated.

9.6. **Pressure positivity constraint**
   - Derive P > (Gamma-1)/Gamma (eta/tau_Q - mn) from rho > eta/tau_Q.
   - Show the additional constraint tau_Q > eta/(mn) ensures P > 0.
   - *Status in paper:* Eqs. 50-51 stated.

---

### Section 10: Shockwave ODE System

**Derivations needed:**

10.1. **Reduction to ODEs**
   - Start from nabla_a T^{ab} = 0 and nabla_a J^a = 0 in Minkowski spacetime with t-independence and only x-variation.
   - Show (T^{tx})' = 0, (T^{xx})' = 0, and (J^x)' = 0.
   - *Status in paper:* Stated; straightforward.

10.2. **Baryon conservation -> n'(x)**
   - From (J^x)' = (nWv)' = 0, derive n' = -W^2 n v'/v.
   - *Status in paper:* Eq. 43 stated; need to show the chain rule step.

10.3. **Shockwave ODE system derivation** (CRITICAL — most complex derivation)
   - From (T^{tx})' = 0 and (T^{xx})' = 0, with T^{ab} the full BDNK stress-energy tensor:
     - Compute T^{tx} and T^{xx} explicitly for u^a = (W, Wv, 0, 0).
     - These will involve epsilon, v, n and their x-derivatives.
     - Set (T^{tx})' = 0 and (T^{xx})' = 0.
     - Eliminate n' using the baryon conservation result.
     - Solve the resulting 2x2 linear system for epsilon'(x) and v'(x).
   - Show the shared denominator structure (Eq. 45).
   - Verify delta = 0 (cross-reference with Section 5.3).
   - Factor the denominator as A(v^2 - c_+^2)(v^2 - c_-^2).
   - Derive the numerator coefficients c_i, d_i (Eq. 48).
   - *Status in paper:* The final ODEs are stated (Eqs. 47-48) with coefficients listed. The derivation from the conservation laws is completely skipped.
   - *External reference:* [Pandya_2021] for the conformal case.

10.4. **Rankine-Hugoniot conditions**
   - Derive the jump conditions from conservation of T^{tx}, T^{xx}, J^x across the shock.
   - Using the perfect fluid stress-energy tensor for the asymptotic states.
   - *Status in paper:* Eqs. 49-50 stated.

---

### Section 11: Heat Flow Equations

**Derivations needed:**

11.1. **Alternative form of heat flux vector** (IMPORTANT)
   - Start from Q^a = tau_Q rho u^c nabla_c u^a + beta_epsilon Delta^{ac} nabla_c epsilon + beta_n Delta^{ac} nabla_c n.
   - Apply the thermodynamic identity (Eq. 53) to convert gradients of epsilon, n to gradients of T, P.
   - Specifically: nabla_c P = p'_epsilon nabla_c epsilon + p'_n nabla_c n, and use the identity to express nabla_c T in terms of nabla_c epsilon, nabla_c n.
   - Show Q^a = -kappa Delta^{ab} nabla_b T + tau_Q rho u^b nabla_b u^a + gamma Delta^{ab} nabla_b P.
   - Identify kappa = sigma rho^2/(n^2 T) and gamma = tau_Q + sigma rho/n^2.
   - *Status in paper:* Eq. 54-55 stated; the conversion using the thermodynamic identity is not shown.

11.2. **Baryon conservation for heat flow**
   - With u^i = 0: nabla_a J^a = n-dot = 0.
   - *Status in paper:* Eq. 56.

11.3. **Heat flow equations of motion** (IMPORTANT)
   - From nabla_a T^{ab} = 0 with u^i = 0 and variation only in t, x:
   - t-component: (epsilon + tau_epsilon epsilon-dot)_{,t} + (-kappa T' + gamma P')_{,x} = 0.
   - x-component: (-kappa T' + gamma P')_{,t} + (P + tau_P epsilon-dot)_{,x} = 0.
   - Show every step of deriving these from the full BDNK T^{ab}.
   - *Status in paper:* Eqs. 57-58 stated without derivation.

11.4. **Eckart heat equation** (IMPORTANT)
   - Set tau_epsilon = tau_P = 0, gamma = 0 in Eqs. 57-58.
   - t-equation becomes: epsilon-dot - kappa T'' = 0 (since n is constant, T'' is related to epsilon'').
   - Convert to an equation for T using T = (Gamma-1)(epsilon/n - m), so epsilon = nT/(Gamma-1) + mn.
   - Show: T-dot = alpha_E T'' where alpha_E = kappa(Gamma-1)/n.
   - *Status in paper:* Eq. 59 stated; conversion steps from epsilon to T not shown.

11.5. **Hybrid frame telegrapher's equation**
   - Set tau_P = 0, gamma = 0, tau_epsilon > 0.
   - From the t-equation: (epsilon + tau_epsilon epsilon-dot)_{,t} - kappa T'' = 0.
   - Convert to T: this gives tau_epsilon T-ddot + T-dot = alpha_E T''.
   - Rearrange to T-ddot - c_h^2 T'' + (1/tau_epsilon) T-dot = 0 where c_h^2 = kappa(Gamma-1)/(n tau_epsilon).
   - *Status in paper:* Eq. 60 stated; conversion steps not shown.

11.6. **BDNK frame generalized telegrapher's equation**
   - Full BDNK with tau_epsilon, tau_P, tau_Q > 0.
   - Derive T-ddot - c_B^2 T'' + (1/tau_epsilon) T-dot + l.o.t. = 0.
   - c_B^2 = c_h^2 (1 - gamma n/kappa).
   - l.o.t. = (Gamma-1)/(n tau_epsilon) gamma(n'' T + 2n'T').
   - *Status in paper:* Eq. 61 stated.

11.7. **x-component: pressure relaxation equation**
   - Integrate Eq. 58 once in x to get theta T-dot + P = P_0(t).
   - Show theta for each frame (Eq. 62).
   - Multiply by n, rearrange to get P-dot = (P_0 - P)/tau_theta.
   - Show tau_theta = theta/n.
   - Explain why Eckart is unstable (tau_theta < 0) and how BDNK avoids this (theta can be >= 0).
   - *Status in paper:* Eqs. 59-63 stated; some steps of integration and rearrangement skipped.

11.8. **Initial data conversion**
   - From T(0,x) and P(0,x) = P_0 = const, derive epsilon(0,x) and n(0,x) using:
     epsilon = P[mT^{-1} + (Gamma-1)^{-1}] and n = P T^{-1}.
   - *Status in paper:* Stated below Eq. 64.

11.9. **Initial EOM simplification**
   - Show the x-component of conservation law is trivially satisfied at t=0.
   - Show the t-component reduces to tau_epsilon epsilon-ddot = (kappa T')'.
   - *Status in paper:* Eq. 65 stated.

---

### Section 12: Characteristic Speed Formulas (Appendix A)

**Derivations needed:**

12.1. **Derivation of c_pm^2 for the specific frame** (CRITICAL)
   - This is the same as 6.2 but with full detail.
   - Substitute the frame ansatz into A, B, C.
   - Factor and simplify.
   - Arrive at Eq. 75.
   - *Status in paper:* Formula stated (Eq. 75); derivation completely skipped.

12.2. **Derivation of c_1^2**
   - From the general definition of c_1 (in [Bemfica:2020zjp]), substitute the frame ansatz.
   - *Status in paper:* Eq. 76 stated.
   - *External reference:* The definition of c_1 is in [Bemfica:2020zjp].

---

## III. Derivations Requiring External References

The following derivations rely on results from cited papers that are not derived in this paper:

| Derivation | External Source | What's Needed |
|-----------|----------------|---------------|
| BDNK constitutive relations (Eqs. 10-15) | [Bemfica:2020zjp] | Why these specific gradient terms are the most general at O(nabla) |
| Causality constraints CAUS A-D | [Bemfica:2020zjp] Eq. (20) | How these constraints are derived from requiring subluminal characteristics |
| Stability constraints STAB A1-E | [Bemfica:2020zjp] Eq. (48) | How these are derived from linearized perturbation analysis |
| c_1 characteristic speed | [Bemfica:2020zjp] | Origin as a shear-mode characteristic speed |
| Three "complicated" stability constraints | Mathematica notebook (GitHub) | Verification that sigma-hat <= 1/3 suffices with the frame ansatz |
| Entropy production non-negativity | [Bemfica:2020zjp] | Proof that eta, zeta, sigma >= 0 ensures non-negative entropy production |
| Conformal limit and conformal BDNK | [Pandya_2021] | Comparison shockwave solutions |
| Boltzmann equation derivation of BDNK | [Rocha:2022ind] | Kinetic theory foundations |

**Note:** For items marked as from [Bemfica:2020zjp], the derivations document should clearly state what is being imported and why, even if we do not re-derive those results.

---

## IV. Prioritization

### Tier 1 — Must derive with full detail (steps are skipped and results are nontrivial):
1. Entropy density s(epsilon, n) from the first law (Sec. 2.2)
2. kappa_epsilon and kappa_n (Secs. 3.3-3.4)
3. Sound speed c_s^2 identity and evaluation (Sec. 3.8)
4. delta = 0 identity (Sec. 5.3)
5. Bjorken flow EOM (Sec. 9.3)
6. Shockwave ODE system (Sec. 10.3)
7. Heat flux vector alternative form (Sec. 11.1)
8. Heat flow EOMs: Eckart/hybrid/BDNK forms (Secs. 11.4-11.6)
9. Characteristic speed c_pm^2 explicit formula (Sec. 12.1)
10. Rescaled stability constraints (Secs. 7.1-7.2)
11. Causality constraint simplification (Sec. 7.6)
12. Thermodynamic identity (Sec. 2.4)

### Tier 2 — Should derive (steps are skipped but results are straightforward):
1. Projection operator properties (Sec. 1.1-1.2)
2. p'_epsilon, p'_n (Secs. 3.1-3.2)
3. beta_epsilon, beta_n (Secs. 3.6-3.7)
4. kappa_s, omega, alpha (Secs. 3.5, 3.9)
5. Chemical potential mu (Sec. 2.3)
6. Eckart as special case (Sec. 4.3)
7. MIS comparison derivation (Sec. 8.5)
8. Inviscid Bjorken solution (Sec. 9.4)
9. Baryon conservation in Milne coordinates (Sec. 9.2)
10. Pressure relaxation and instability explanation (Sec. 11.7)

### Tier 3 — Include for completeness (straightforward or follow from definitions):
1. Ideal fluid constitutive relations (Sec. 1.3)
2. Euler equations (Sec. 1.4)
3. On-shell equivalence (Sec. 4.2)
4. Relaxation solutions (Secs. 8.4, 8.6-8.8)
5. Rankine-Hugoniot conditions (Sec. 10.4)
6. Large/small tau-hat limits (Secs. 9.5-9.6)

---

## V. Proposed Document Structure

```
mathematical-derivations.md

# Mathematical Derivations: BDNK Hydrodynamics with Ideal Gas Microphysics

## 1. Foundations: Tensor Decomposition and Gradient Expansion
   1.1 Projection operator Delta^{ab}: properties
   1.2 Traceless-transverse projector X^{<ab>}
   1.3 Decomposition of conserved currents
   1.4 Ideal fluid constitutive relations
   1.5 Relativistic Euler equations (scalar and vector projections)

## 2. Relativistic Ideal Gas Microphysics
   2.1 Equation of state, specific internal energy, and temperature
   2.2 Entropy density from the first law of thermodynamics
   2.3 Chemical potential from the Euler relation
   2.4 The thermodynamic identity

## 3. Derivatives of Microphysics Quantities
   3.1 Pressure derivatives: p'_epsilon and p'_n
   3.2 Chemical potential derivatives: kappa_epsilon and kappa_n
   3.3 Combined quantity kappa_s
   3.4 Sound speed c_s^2
   3.5 Auxiliary quantities: omega and alpha

## 4. BDNK Conserved Currents
   4.1 BDNK constitutive relations and stress-energy tensor
   4.2 Heat flux coefficients: beta_epsilon and beta_n
   4.3 On-shell nature of regularizing terms
   4.4 Eckart theory as a limit of BDNK
   4.5 Alternative form of the heat flux vector

## 5. Hydrodynamic Frame
   5.1 Frame ansatz and definitions (V, V-hat, Reynolds number)
   5.2 delta = 0 identity
   5.3 Characteristic speeds: c_pm^2 and c_1^2

## 6. Constraint Simplification
   6.1 Rescaled shorthand: B-hat, C-hat, D-hat, E-hat
   6.2 Rescaled linear stability constraints
   6.3 Simplification of "simple" stability constraints
   6.4 The sigma-hat <= 1/3 bound
   6.5 Causality constraints: reduction to the tau-hat bound
   6.6 The single simplified causality inequality

## 7. Equilibrium State Comparison
   7.1 Spatially isotropic states: baryon and energy conservation
   7.2 Eckart, BDNK, and MIS equations for isotropic states
   7.3 Equivalence of BDNK and MIS relaxation structure
   7.4 Temperature frame dependence
   7.5 General relaxation form of BDNK equations

## 8. Bjorken Flow
   8.1 Milne coordinates: metric, Christoffel symbols, covariant derivatives
   8.2 Baryon conservation: n(tau) = n_0/tau
   8.3 Stress-energy conservation: the Bjorken ODE (Eq. 47)
   8.4 Inviscid Bjorken solution
   8.5 Limiting cases: tau-hat -> 0 and tau-hat -> infinity
   8.6 Pressure positivity constraint

## 9. Shockwave ODE System
   9.1 Reduction to ODEs in the shock rest frame
   9.2 Baryon conservation: n'(x) equation
   9.3 Stress-energy conservation: shared denominator and characteristic speeds
   9.4 Full shockwave ODE system: epsilon'(x) and v'(x)
   9.5 Rankine-Hugoniot jump conditions

## 10. Heat Flow
   10.1 Heat flow equations of motion (t and x components)
   10.2 Eckart frame: the heat equation
   10.3 Hybrid frame: the telegrapher's equation
   10.4 BDNK frame: the generalized telegrapher's equation
   10.5 Pressure relaxation and stability analysis
   10.6 Initial data and initial EOM

## Appendix: Cross-Reference to Paper Equations
   [Table mapping each derived result to the paper's equation number]
```

---

## VI. Estimated Complexity

| Section | Estimated Length | Difficulty |
|---------|-----------------|------------|
| 1. Foundations | Medium | Low |
| 2. Microphysics | Long | Medium-High (entropy derivation) |
| 3. Derivatives | Long | High (kappa_epsilon, kappa_n, c_s^2) |
| 4. BDNK Currents | Medium | Medium |
| 5. Frame | Medium | Medium-High (delta=0, c_pm^2) |
| 6. Constraints | Long | High (many inequality manipulations) |
| 7. Equilibrium | Medium | Low-Medium |
| 8. Bjorken | Long | High (ODE derivation in Milne coords) |
| 9. Shockwave | Very Long | Very High (full ODE derivation) |
| 10. Heat Flow | Long | Medium-High |

Total estimated: ~15,000-20,000 words of mathematical derivations.
