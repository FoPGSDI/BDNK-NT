# Stage 1: Plan Mode — Summary of Agent Outputs

## Date: 2026-03-23

---

## Agent 1: Convention Agent — COMPLETE

Output saved to: `progress/conventions.md`

Key deliverables:
- 19-section comprehensive convention document
- All ~60 mathematical symbols cataloged with definitions
- 6 notation conflicts identified and disambiguated
- Markdown formatting rules established
- Bar notation, hat notation (two distinct uses), index conventions all clarified

---

## Agent 2: Math Derivation Planning Agent — COMPLETE

### Missing Derivations Identified (total ~158 intermediate steps):

1. **Section 1.2** — Ideal fluid projections (8 steps, no dependencies)
2. **Section 2.4** — Q^mu proportional to zeroth-order EoM (4 steps, depends on 1.2)
3. **NEW Section 3.5.5** — Bridge: pre-projection of T^{mu nu} (18 steps)
4. **Section 3.6 Sub-stage A** — nabla_mu v_nu lemma (10 steps, KEYSTONE)
5. **Section 3.6 Sub-stage B** — sigma^{mu nu} in 3+1 (12 steps, depends on A)
6. **Section 3.6 Sub-stage C** — A, Pi, Q^mu in 3+1 (8 steps, depends on A)
7. **Section 3.6 Sub-stage D** — Final E, S^i, S_{ij} (~45 steps, depends on B+C)
8. **Section 6.3** — Coordinate transformation (10 steps, independent)
9. **NEW Section 7.3** — Well-posedness derivation (18 steps, independent)
10. **Section 8.2** — General con2prim A matrix (15 steps, depends on 3.6D)
11. **Section 8.3** — Spherical con2prim A matrix (10 steps, depends on 8.2)

### Recommended Writing Order:
- Phase 1: Sections 1.2, 2.4, 3.5.5 (foundational)
- Phase 2: Sub-stage A (keystone lemma)
- Phase 3: Sub-stages B and C (parallelizable)
- Phase 4: Sub-stage D (main derivation)
- Phase 5: Section 6.3 (independent)
- Phase 6: Sections 8.2, 8.3 (con2prim)
- Phase 7: Section 7.3 (well-posedness)

---

## Agent 3: Numerical Implementation Planning Agent — COMPLETE

### Correctness Issues Found (5):
1. con2prim uses wrong variable (vr vs vtilde_r)
2. b-vector entirely missing in con2prim
3. Only flat-space characteristic velocities implemented
4. convergence_factor ignores solution arrays
5. hat_V vs tau_epsilon naming confusion

### New Implementations Needed (7):
1. **Coordinate transformation** (areal-polar → isotropic) — HIGH priority
2. **FDOC spatial discretization** — HIGH priority
3. **Full c-vector for con2prim** — HIGH priority
4. **Curved-space characteristic velocities** — HIGH priority
5. **Full 6-variable RHS function** — HIGH priority
6. **Stress tensor components** — HIGH priority
7. **Convergence testing with cubic spline** — MEDIUM priority

### Implementation Order:
- Phase 1: Coord. transform, char. speeds, c-vector
- Phase 2: FDOC, stress tensor, con2prim fix
- Phase 3: Full RHS function + evolution loop
- Phase 4: Convergence testing

---

## Agent 4: Test Results Planning Agent — COMPLETE

### Gap Analysis:
- All 4 tables reproduced but missing precision specifications
- All 6 figures described but lacking quantitative pass/fail criteria
- ~25 new tests identified

### Critical Missing Items:
1. QNM frequency tolerance: ±0.025 kHz
2. Decay rate tolerance: ±0.00001 M_sun^-1
3. Expected convergence factor Q = 1.993
4. highB-F9 3-point extrapolation restriction
5. Unit conversion section
6. omega_nl conversion discrepancy (0.0834 → 2.692 kHz vs paper's 2.71 kHz)

### c- velocity VERIFIED: c- = 0.0183*cs is correct (was flagged as potential discrepancy, resolved by precise calculation with hat_q=0.999)

### New Test Categories Needed:
- EoS positivity/monotonicity, unit conversion
- TOV stellar radius, coordinate transform correctness
- tau_p/tau_Q/beta_epsilon consistency
- Con2prim determinant, static equilibrium recovery
- Energy conservation, atmosphere treatment
- Peak finding accuracy, Blackman window validation
- Butterworth filter parameters, fitting method agreement
- Convergence order p extraction
- Full pipeline integration tests
- Regression test architecture

### Pytest Structure: 10 test files, 3 execution marks (unit/integration/slow), 4 table marks
