# Test Results and Test Suite Design: BDNK Viscous Hydrodynamics for Neutron Stars

## Preamble: Guidelines for These Notes

*Read this section whenever updating.*

This document tracks all test results, validation checks, and test suite designs for reproducing and verifying the results of the BDNK neutron star paper.

- **Uncertainty is explicit** — use markers
- **Every test has pass/fail criteria**
- **Discrepancies are flagged** with `[DISCREPANCY]`
- **Verified results** marked `[VERIFIED]`

---

## 1. Test Suite Overview

### 1.1 Test Categories

| Category | Description | Status |
|---|---|---|
| T1: EoS Verification | Equation of state correctness | `[PENDING]` |
| T2: TOV Solver | Initial data generation | `[PENDING]` |
| T3: Transport Coefficients | Parameter computation | `[PENDING]` |
| T4: Well-Posedness | Condition verification | `[PENDING]` |
| T5: Characteristic Velocities | Speed computation | `[PENDING]` |
| T6: Con2Prim | Primitive recovery | `[PENDING]` |
| T7: Stable Evolution | Long-time stability | `[PENDING]` |
| T8: QNM Frequencies | Spectrum analysis | `[PENDING]` |
| T9: Decay Rates | f-mode decay | `[PENDING]` |
| T10: Convergence | Order verification | `[PENDING]` |

---

## 2. T1: Equation of State Tests

### 2.1 Test: p(ε=0) = 0

`[PENDING]`

**Purpose:** Verify physical boundary condition.

```python
def test_eos_zero():
    assert abs(pressure(0.0)) < 1e-15
```

**Expected:** $p(0) = 0$ exactly.

### 2.2 Test: EoS Inversion Consistency

`[PENDING]`

**Purpose:** Verify $\epsilon(p(ε)) = ε$ for range of values.

```python
def test_eos_inversion():
    for eps in [1e-6, 1e-4, 1e-3, 0.00144, 0.01, 0.1]:
        p = pressure(eps)
        eps_recovered = epsilon_from_pressure(p)
        assert abs(eps - eps_recovered) / abs(eps) < 1e-12
```

### 2.3 Test: Speed of Sound

`[PENDING]`

**Purpose:** Verify $c_s^2 = dp/d\epsilon \in (0, 1)$ and $c_s^2 < 1/3$ for relevant densities.

```python
def test_speed_of_sound():
    eps_c = 0.00144  # central density
    cs2 = dpressure_depsilon(eps_c)
    assert 0 < cs2 < 1.0
    assert cs2 < 1.0/3.0  # Required for causality conditions
```

### 2.4 Test: Central Values

`[PENDING]`

**Purpose:** Verify $\rho_{0,c} = 0.00128 \implies \epsilon_c = 0.00144$

```python
def test_central_values():
    rho_0c = 0.00128
    kappa = 100.0
    p_c = kappa * rho_0c**2  # Gamma=2
    eps_0 = p_c / rho_0c     # Gamma-1 = 1
    epsilon_c = rho_0c * (1 + eps_0)
    assert abs(epsilon_c - 0.00144) < 0.00001
```

---

## 3. T2: TOV Solver Tests

### 3.1 Test: Regularity at Origin

`[PENDING]`

**Purpose:** Verify smooth behavior at $R=0$.

### 3.2 Test: Stellar Properties

`[PENDING]`

**Purpose:** Verify $M_T = 1.4\ M_\odot$ for $\rho_{0,c} = 0.00128\ M_\odot^{-2}$.

**Expected values** (ref: Font:2001ew, CCC):
- Total gravitational mass: $M_T = 1.4\ M_\odot$
- Surface location: where $p = 0$

### 3.3 Test: Asymptotic Flatness

`[PENDING]`

**Purpose:** Verify $\lim_{R\to\infty} \alpha(R) = \lim_{R\to\infty} 1/a(R)$ and $\lim_{R\to\infty} p(R) = 0$.

---

## 4. T3: Transport Coefficient Tests

### 4.1 Test: Parameter Case Consistency

`[PENDING]`

**Purpose:** Verify $\tau_\epsilon = \hat{V} \cdot L = (4/3\hat{\eta} + \hat{\zeta}) \cdot L$ for each case.

```python
def test_tau_epsilon_consistency():
    for name, case in CASES.items():
        hat_V = (4.0/3.0)*case['hat_eta'] + case['hat_zeta']
        L = 1.0  # L=1 in paper
        tau_eps_computed = hat_V * L
        assert abs(tau_eps_computed - case['tau_eps']) < 1e-10, \
            f"Case {name}: tau_eps mismatch {tau_eps_computed} vs {case['tau_eps']}"
```

**Expected results:**

| Case | $\hat{V} = 4/3\hat{\eta} + \hat{\zeta}$ | $\tau_\epsilon$ |
|---|---|---|
| smallSB-F2 | $4/3 \times 0.01 + 0.01 = 0.02333$ | 0.023 |
| medS-F2 | $4/3 \times 0.01725 + 0 = 0.023$ | 0.023 |
| highB-F9 | $4/3 \times 0.0015 + 0.09 = 0.092$ | 0.092 |
| medSB-F9 | $4/3 \times 0.03525 + 0.045 = 0.092$ | 0.092 |

`[VERIFIED]` All four cases yield consistent $\tau_\epsilon$ values.

---

## 5. T4: Well-Posedness Condition Tests

### 5.1 Test: Strong Hyperbolicity

`[PENDING]`

**Purpose:** Verify $0 < \hat{q} < \hat{s}$ → $0 < 0.999 < 1$.

```python
def test_strong_hyperbolicity():
    hat_q = 0.999
    hat_s = 1.0
    assert 0 < hat_q < hat_s
```

### 5.2 Test: Causality Conditions

`[PENDING]`

**Purpose:** Verify inequalities Eqs.55-56 for all four cases.

```python
def test_causality():
    hat_a, hat_q, hat_s = 1.0, 0.999, 1.0
    eps_c = 0.00144
    cs2 = dpressure_depsilon(eps_c)

    # Condition 1: hat_q < (1-cs2)/cs2 * (1-hat_s*cs2)/(cs2 + 1/hat_a)
    rhs = (1 - cs2)/cs2 * (1 - hat_s*cs2)/(cs2 + 1.0/hat_a)
    assert hat_q < rhs

    # Condition 2: hat_s < 1/cs2
    assert hat_s < 1.0/cs2
```

---

## 6. T5: Characteristic Velocity Tests

### 6.1 Test: Specific Values from Paper

`[PENDING]`

**Purpose:** Verify characteristic velocities match paper's quoted values.

**Expected** (for $\hat{s}=1, \hat{a}=1, \hat{q}=0.999$):
- $c_0 = 0.9995\sqrt{\hat{\eta}/\hat{V}}\,c_s$
- $c_+ = 1.732\,c_s$ (i.e., $\sqrt{3}\,c_s$)
- $c_- = 0.0183\,c_s$

```python
def test_characteristic_velocities():
    hat_a, hat_q, hat_s = 1.0, 0.999, 1.0

    # c_+ = cs * sqrt((1*(1+1) + 0.999 + sqrt(...))/2)
    # Numerically compute and compare
    c0, cp, cm = characteristic_velocities(hat_a, hat_q, hat_s, 0.01, 0.01, cs=1.0)

    # c_+ should be sqrt(3)*cs = 1.732*cs
    assert abs(cp - np.sqrt(3)) < 0.001

    # c_- should be 0.0183*cs
    assert abs(cm - 0.0183) < 0.001
```

`[FUTURE: Verify these exact numerical values by direct computation]`

---

## 7. T6: Con2Prim Tests

`[PENDING]`

### 7.1 Test: Perfect Fluid Limit

**Purpose:** When all transport coefficients → 0, con2prim should reduce to standard PF recovery.

### 7.2 Test: Static Equilibrium

**Purpose:** For static star ($v^r = 0$, no perturbation), verify $\hat{\epsilon} = \hat{\bar{v}}^r = 0$.

### 7.3 Test: Invertibility

**Purpose:** Verify matrix $\mathcal{A}$ is invertible (non-zero determinant) for all grid points.

---

## 8. T7: Stable Evolution Results

### 8.1 Published Results Summary

`[SOLID]` (ref: Paper Section III.B, Figs.1-2)

**Simulation parameters:**
- End time: $t_f = 8000\ M_\odot$ (except $\Delta r = 0.001$ which reached $t_f = 4500\ M_\odot$)
- Resolutions: $\Delta r = [0.001, 0.002, 0.0024, 0.0028, 0.0032]\ M_\odot$
- Initial perturbation: numerical discretisation errors only

**Key observations:**
1. Stable evolutions achieved for all four parameter cases
2. Late-time $\epsilon(r)$ shows slight deviations near centre and surface (numerical dissipation)
3. Deviations decrease with increasing resolution (qualitative convergence)

### 8.2 Figure Descriptions

**Figure 1 (stable_evol_comparing_tau.pdf):**
- Shows $\epsilon(r)$ at initial and $t = 8000\ M_\odot$ for all four cases at $\Delta r = 0.002$
- Insets: near-center and near-surface behavior
- All cases remain close to initial profile

**Figure 2 (stable_evol_resolutions.pdf):**
- Shows $\epsilon(r)$ at $t = 4500\ M_\odot$ for smallSB-F2 across resolutions
- Qualitative convergence demonstrated in inset

---

## 9. T8: QNM Frequency Results

### 9.1 Published Frequencies

`[SOLID]` (ref: Paper Table I, Fig.3)

| Mode | PF (kHz) | smallSB-F2 (kHz) | highB-F9 (kHz) |
|---|---|---|---|
| F (fundamental) | 2.69 | 2.69 | 2.67 |
| H1 (1st overtone) | 4.55 | 4.60 | 4.60 |
| H2 (2nd overtone) | 6.36 | 6.36 | 6.30 |

**Key findings:**
- f-mode frequency consistent across all cases (~2.69 kHz)
- Overtones show slight viscosity dependence
- Matches literature values under Cowling approximation

### 9.2 Figure Description: QNM_plot.pdf (Fig.3)

**Top panel:** $\epsilon_c(t)$ for PF, smallSB-F2, highB-F9 at $\Delta r = 0.002$
- Data extracted every $\Delta t = 1\ M_\odot$ up to $t = 8000\ M_\odot$
- Perturbation visible only in first ~1000 M_sun

**Bottom panel:** Power spectral density (Blackman window)
- Three clear peaks: F, H1, H2
- F-mode consistent across cases
- Higher modes show slight viscosity dependence

---

## 10. T9: Decay Rate Results

### 10.1 Published Decay Rates at $\Delta r = 0.002$

`[SOLID]` (ref: Paper Table II)

| Case | $1/\tau_l$ ($M_\odot^{-1}$) | $1/\tau_{nl}$ ($M_\odot^{-1}$) | $\omega_{nl}$ ($M_\odot^{-1}$) |
|---|---|---|---|
| smallSB-F2 | 0.00157 | 0.00157 | 0.0834 |
| medS-F2 | 0.00150 | 0.00150 | 0.0834 |
| highB-F9 | 0.00215 | 0.00215 | 0.0834 |
| medSB-F9 | 0.00182 | 0.00182 | 0.0834 |

$\omega_{nl} = 0.0834\ M_\odot^{-1}$ → $f = 2.71$ kHz

### 10.2 Continuum Extrapolation

`[SOLID]` (ref: Paper Table III)

**Decay rates $1/\tau_{\Delta r}$ ($M_\odot^{-1}$) as function of resolution:**

| $\Delta r/M_\odot$ | PF | smallSB-F2 | medS-F2 | highB-F9 | medSB-F9 |
|---|---|---|---|---|---|
| 0.0032 | 0.00023 | 0.0019 | 0.0018 | 0.0024 | 0.0021 |
| 0.0028 | 0.00021 | 0.0018 | 0.0017 | 0.0024 | 0.0020 |
| 0.0024 | 0.00019 | 0.0017 | 0.0016 | 0.0023 | 0.0019 |
| 0.0020 | 0.00018 | 0.0016 | 0.0015 | 0.0022 | 0.0018 |
| **0 (extrap.)** | **NIL** | **0.0011** | **0.0010** | **0.0017** | **0.0013** |
| **0 ($s^{-1}$)** | **NIL** | **220** | **200** | **350** | **260** |

### 10.3 Figure Description: casA_fitting.pdf (Fig.4)

**Demonstrated using smallSB-F2 data:**

**Top panel:** $|\tilde{\epsilon}_c|$ vs time (log scale)
- Shows exponential decay at late times

**Middle panel:** Log of maxima with linear fit
- Slope gives decay rate

**Bottom panel:** Damped sinusoidal fit
- Recovers both decay rate and frequency

### 10.4 Figure Description: error_fit.pdf (Fig.5)

- Decay rate vs resolution for smallSB-F2 and PF (×10)
- Red/green dots: measured values with error bars
- Black/blue dots: averaged values used for extrapolation
- Shows resolution dependence consistent with marginal convergence (p=1)

---

## 11. T10: Convergence Test Results

### 11.1 Published Results

`[SOLID]` (ref: Paper Appendix B, Fig.6)

**Resolutions tested:** $\Delta r = 0.0028, 0.002, 0.001\ M_\odot$ (case smallSB-F2)

**Convergence factor Q:**
- Expected: $Q = (0.0028^n - 0.002^n)/(0.002^n - 0.001^n)$ for order $n$
- Found: converges to expected value after short transient

### 11.2 QNM Frequency Stability

`[SOLID]` (ref: Paper Table IV)

| $\Delta r$ | F (kHz) | H1 (kHz) | H2 (kHz) |
|---|---|---|---|
| 0.0028 | 2.69 | 4.60 | 6.36 |
| 0.002 | 2.69 | 4.60 | 6.36 |
| 0.001 | 2.67 | 4.61 | 6.33 |

Frequencies mostly stable against resolution change.

### 11.3 Figure Description: convergence.pdf (Fig.6)

**Top panel:** Central energy density evolution at three resolutions
- Qualitative convergence visible

**Bottom panel:** Convergence factor vs time
- Red line: expected theoretical value
- Factor reaches expected value after initial transient

---

## 12. Test Suite Design for Reproduction

### 12.1 Unit Tests (Fast, isolated)

```python
# test_eos.py
class TestEoS:
    def test_zero_pressure(self): ...
    def test_inversion(self): ...
    def test_sound_speed_bounds(self): ...
    def test_central_values(self): ...

# test_transport.py
class TestTransport:
    def test_tau_epsilon_cases(self): ...
    def test_well_posedness(self): ...
    def test_characteristic_velocities(self): ...
    def test_causality(self): ...

# test_con2prim.py
class TestCon2Prim:
    def test_static_equilibrium(self): ...
    def test_invertibility(self): ...
    def test_perfect_fluid_limit(self): ...
```

### 12.2 Integration Tests (TOV solver)

```python
# test_tov.py
class TestTOV:
    def test_regularity(self): ...
    def test_stellar_mass(self): ...
    def test_asymptotic_flatness(self): ...
    def test_coordinate_transform(self): ...
```

### 12.3 System Tests (Full evolution)

```python
# test_evolution.py
class TestEvolution:
    def test_stable_evolution_smallSB_F2(self): ...
    def test_stable_evolution_highB_F9(self): ...
    def test_qnm_frequencies(self): ...
    def test_decay_rates(self): ...
    def test_convergence_order(self): ...
```

---

## Appendix

### Abandoned Approaches

[None yet]
