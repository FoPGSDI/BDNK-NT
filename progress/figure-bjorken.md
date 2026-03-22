# Figure Analysis: Bjorken Flow (bjorken_plot.pdf)

**Source:** Fig. 1 in paper.tex (label `fig:bjorken`), Section III.B (lines 773-940).

---

## 1. Visual Description

The figure contains two vertically stacked panels sharing a common horizontal axis (proper time tau).

### Top Panel
A log-log plot showing nine black curves (three families of three, each family sharing a line style) plus one thick red dashed reference line. The nine curves emerge from widely different initial values at tau = 1 and converge onto the red dashed reference line at late times. Within each family of three (corresponding to a single line style, i.e. a single value of tau-hat), the three members correspond to three different initial conditions for epsilon-dot. Several of the curves plunge steeply downward (sometimes below the plotted range) before recovering and joining the reference solution from below; this occurs when the plotted quantity passes through zero and becomes negative, which cannot be displayed on a log scale.

### Bottom Panel
A linear-log plot showing three black solid curves (BDNK frame temperature) and three blue dashed curves (Eckart frame temperature) for the three tau-hat = 2 solutions from the top panel. All three BDNK (black) curves originate from T ~ 0.5 at tau = 1 (since they share the same epsilon_0 = 0.25), but diverge rapidly due to different epsilon-dot_0 values. The three Eckart (blue) curves start at very different initial values because T_E depends on epsilon_dot through the frame correction. Importantly, the BDNK and Eckart curves for a single initial condition are NOT visually adjacent at early times; they cross other curves and only converge into identifiable pairs at late times.

Specifically:
- **epsilon-dot_0 = 0 solution:** Both BDNK and Eckart start near T ~ 0.5 and decay monotonically together. This pair remains close throughout and is the most visually "paired" at all times.
- **epsilon-dot_0 = 2 solution:** The BDNK curve starts at T ~ 0.5, rises to T ~ 1.6, then decays. Its Eckart partner starts at T ~ -0.8 (negative!) and rises. At late times both converge to the highest temperature of the three pairs.
- **epsilon-dot_0 = -2 solution:** The BDNK curve starts at T ~ 0.5, then plunges rapidly to negative values. Its Eckart partner starts at the highest value in the plot, T ~ 1.8-2.0, and decays steeply. At late times both converge to negative temperatures (T ~ -0.4 to -0.5), forming the bottom pair.

---

## 2. Axes and Labels

### Top Panel
- **Horizontal axis:** tau (proper time in Milne coordinates), logarithmic scale, ranging from 1 to approximately 20.
- **Vertical axis:** epsilon-dot + Gamma * epsilon / tau, logarithmic scale, ranging from roughly 10^{-4} to above 10^{-1}. This combination equals m * n_0 * (Gamma - 1) / tau^2 for the inviscid (ideal) Bjorken solution, independent of the integration constant e_0.

### Bottom Panel
- **Horizontal axis:** tau, logarithmic scale, same range as top panel (1 to ~20).
- **Vertical axis:** T (temperature), linear scale, ranging from approximately -0.6 to 2.2.

---

## 3. Line Styles and Legend

### Top Panel
| Line Style       | Meaning |
|------------------|---------|
| Thick red dashed | Inviscid (V-hat = 0) Bjorken solution: m * n_0 * (Gamma - 1) / tau^2, serving as the equilibrium attractor. |
| Solid black      | BDNK viscous solutions with tau-hat = 0.5 (always superluminal characteristics, c_+ ~ 1.3). |
| Dash-dot black   | BDNK viscous solutions with tau-hat = 1 (superluminal at early times c_+ ~ 1.05, subluminal at late times c_+ ~ 0.9). |
| Dotted black     | BDNK viscous solutions with tau-hat = 2 (always subluminal characteristics, c_+ ~ 0.7). |

Within each line-style group, the three individual curves correspond to three different initial values of epsilon-dot: {-2, 0, 2}, all starting from epsilon_0 = 0.25 at tau = 1.

### Bottom Panel
| Line Style       | Meaning |
|------------------|---------|
| Solid black      | Temperature T in the BDNK hydrodynamic frame, for the three tau-hat = 2 solutions. |
| Dashed blue      | Eckart-frame temperature T_E computed from the frame-invariant observable T^{tau tau} at each tau. |

The three pairs correspond to the three initial conditions epsilon-dot_0 in {-2, 0, 2} (top to bottom in the panel at late times: epsilon-dot_0 = 2 gives the highest temperature, epsilon-dot_0 = -2 gives the lowest/negative temperature).

---

## 4. Key Observations

### 4.1 Universal Late-Time Attractor
All nine viscous solutions in the top panel converge to the inviscid Bjorken solution (red dashed line) at late proper times, regardless of the value of tau-hat or the initial condition for epsilon-dot. This demonstrates that the viscous BDNK theory possesses the correct equilibrium attractor and that the non-equilibrium (frame-dependent) degrees of freedom decay away.

### 4.2 Relaxation Time Controls Equilibration Rate
Larger values of tau-hat (corresponding to larger relaxation time tau_epsilon) produce slower convergence to the inviscid attractor. The solid curves (tau-hat = 0.5) join the red dashed line earliest; the dotted curves (tau-hat = 2) take the longest. This is physically intuitive: longer relaxation times mean the system takes longer to equilibrate.

### 4.3 Superluminal Characteristics Cause No Qualitative Change
A central result of this figure is that the three families of curves (tau-hat = 0.5, 1, 2) exhibit the same qualitative behavior despite spanning the range from always-superluminal to always-subluminal characteristic speeds. There is no visible pathology, instability, or qualitative change in the solutions when the characteristics become superluminal. This supports the analogy between hydrodynamic frame modes and gauge modes in general relativity, where gauge modes are not confined to propagate at the speed of light.

### 4.4 Stiffness at Small tau-hat
Although not directly visible in the plot, the paper notes that decreasing tau-hat (and hence tau_epsilon) makes the ODE stiff, requiring very small time steps. This is a practical numerical consequence of reducing the relaxation time toward zero.

### 4.5 Negative Temperatures and Far-From-Equilibrium Initial Data
The bottom panel shows that one of the three solutions (the one with epsilon-dot_0 = -2) develops negative temperature at intermediate and late times in both the BDNK frame and the Eckart frame. The BDNK temperature starts positive (T = 0.5 at tau = 1, since all three solutions share the same epsilon_0) but plunges negative shortly after. The Eckart temperature for this solution actually starts at the highest value in the plot (T_E ~ 1.8, because the large negative epsilon-dot produces a large positive frame correction to epsilon_E) before decaying to negative values. This behavior arises because the initial data is sufficiently far from equilibrium that it violates the weak energy condition (u_a u_b T^{ab} < 0). The paper emphasizes that negative T is allowed by the BDNK causality/stability constraints (which only require rho > eta / tau_Q, leading to the weaker condition on P in Eq. (74)), but may cause practical problems when the equation of state is tabulated and not defined for T < 0.

### 4.6 Frame Dependence of Temperature
The difference between the solid black (BDNK frame) and dashed blue (Eckart frame) curves illustrates that the temperature is not a unique physical observable outside of equilibrium -- it depends on the choice of hydrodynamic frame. At early times, even the upper-most solution (which has T > 0 throughout) shows a significant discrepancy between BDNK and Eckart temperatures, indicating it is far from equilibrium. At late times, both frame temperatures converge, confirming equilibration.

### 4.7 Frame Mapping as a Diagnostic
The Eckart temperature is computed at each proper time tau by extracting the frame-invariant T^{tau tau}, identifying it as the Eckart-frame energy density epsilon_E, and then using the equation of state (with the same n) to compute T_E. The difference |T_BDNK - T_Eckart| can serve as a diagnostic for how far the solution is from equilibrium and thus from the domain of validity of first-order hydrodynamics.

---

## 5. Numerical / Implementation Notes

### 5.1 Equation of Motion
The Bjorken flow ODE for the BDNK theory is (Eq. 62 of the paper):

```
tau_epsilon * ddot(epsilon) = -(1/tau) * (tau + 2*tau_epsilon + tau_P) * dot(epsilon)
                              - (1/tau^2) * [rho * (tau + tau_P) - V]
```

where rho = epsilon + P is the enthalpy density, and V = (4/3)*eta + zeta is the combined viscosity. This is a second-order ODE in epsilon(tau) with tau as the independent variable.

### 5.2 Transport Coefficients for the Bjorken Problem
From the hydrodynamic frame ansatz (Eq. 25) with L = 1:

- tau_epsilon = tau_Q = V-hat * tau-hat   (with V-hat = 1/10)
- tau_P = 2*(Gamma - 1) * V-hat = 2*(1/3)*(1/10) = 1/15
- V = V-hat * rho * c_s^2  (since L = 1)
- sigma-hat = 0, so heat conductivity sigma = 0 (but this is irrelevant for Bjorken flow since Q^a = 0 by symmetry)

Because rho and c_s^2 depend on the hydrodynamic variables (epsilon, n), V and tau_epsilon are state-dependent. Specifically:

- P = (Gamma - 1) * (epsilon - m*n)
- rho = epsilon + P = Gamma*epsilon - (Gamma - 1)*m*n
- c_s^2 = Gamma * P / rho

### 5.3 Particle Number Density
The conservation law for J^a in Bjorken flow gives n(tau) = n_0 / tau analytically. This does not need to be integrated; it is an exact input to the ODE.

### 5.4 Integration Domain and Initial Data
- Integration range: tau in [1, 20].
- Initial data at tau = 1: epsilon(1) = epsilon_0 = 0.25, dot(epsilon)(1) in {-2, 0, 2}.
- Particle density: n_0 = 0.1, so n(tau) = 0.1/tau.

### 5.5 Inviscid Reference Solution
The inviscid Bjorken solution is:

```
epsilon(tau) = m * n_0 * tau^{-1} * [1 + e_0 * tau^{-(Gamma - 1)}]
```

For the plotted quantity, on the inviscid solution:

```
dot(epsilon) + Gamma * epsilon / tau = m * n_0 * (Gamma - 1) / tau^2
```

which is independent of e_0 and serves as the universal reference curve. With the given parameters (m = 1, n_0 = 0.1, Gamma = 4/3): this equals 0.1 * (1/3) / tau^2 = 1/(30 * tau^2).

### 5.6 Computing the Plotted Quantity
For each numerical solution epsilon(tau), compute dot(epsilon) (which is a dynamical variable in the second-order ODE, or obtained by finite differencing if using a first-order system reformulation), then evaluate:

```
y(tau) = dot(epsilon) + (4/3) * epsilon / tau
```

Note: since some solutions pass through y = 0 (the plotted quantity changes sign), the log-log plot only shows |y| when positive. The steep downward plunges in the plot correspond to y approaching zero before the solution overshoots and recovers.

### 5.7 Computing the Eckart Temperature (Bottom Panel)
1. From the BDNK solution, compute T^{tau tau} = epsilon + delta_epsilon, where delta_epsilon = -tau_epsilon * dot(epsilon) for Bjorken flow (since u^a = (1,0,0,0) in Milne coordinates).
2. Set epsilon_E = T^{tau tau} (Eckart frame definition).
3. Compute the Eckart temperature: T_E = (Gamma - 1)/n * (epsilon_E - m*n) = (epsilon_E - m*n) * (Gamma - 1) / n.

The BDNK-frame temperature is simply T = P/n = (Gamma - 1)*(epsilon - m*n)/n from the equation of state.

### 5.8 Stiffness and ODE Solver Considerations
For small tau-hat (e.g. 0.5), tau_epsilon = V-hat * tau-hat becomes small, making the coefficient of ddot(epsilon) small relative to other terms. This creates a stiff ODE. An implicit or adaptive ODE integrator (e.g., a BDF method or an implicit Runge-Kutta method) is recommended. The paper notes that "very small steps in tau" are needed to resolve the decay time tau_epsilon.

### 5.9 Reformulation as a First-Order System
For numerical integration, rewrite the second-order ODE as two first-order ODEs:

```
Let q1 = epsilon, q2 = dot(epsilon).

dq1/dtau = q2
dq2/dtau = (1/tau_epsilon) * [-(1/tau)*(tau + 2*tau_epsilon + tau_P)*q2 - (1/tau^2)*(rho*(tau + tau_P) - V)]
```

where rho and V depend on q1 and on n(tau) = n_0/tau (and hence also on tau).

---

## 6. Connection to Theory

### 6.1 Validation of the Inviscid Attractor
The convergence of all viscous solutions to the inviscid Bjorken solution confirms that BDNK theory, as a first-order viscous extension of relativistic hydrodynamics, correctly reduces to ideal hydrodynamics at late times when the system equilibrates. The specific quantity plotted (dot(epsilon) + Gamma*epsilon/tau) is chosen precisely because it collapses all inviscid solutions (regardless of integration constant e_0) onto a single curve, making the attractor universally identifiable.

### 6.2 Confirmation of the tau-hat -> 0 and tau-hat -> infinity Limits
The paper analytically derives two limits:
- **tau-hat -> 0 limit:** The characteristics diverge (become infinitely superluminal), but inspection of the EOM shows no structural change. The figure confirms no qualitative difference for tau-hat = 0.5 (superluminal) vs. tau-hat = 2 (subluminal).
- **tau-hat -> infinity limit:** The EOM reduces to ddot(epsilon) = -2*dot(epsilon)/tau, solved by epsilon = c_1/tau + c_2. This solution agrees with the inviscid result only if c_2 = 0, and fails in the ultrarelativistic limit. The figure is consistent with this: larger tau-hat solutions take longer to equilibrate, and in the infinite limit one expects the system never to reach the correct attractor (except trivially).

### 6.3 Gauge/Frame Analogy
The insensitivity of solutions to superluminal characteristics supports the analogy between hydrodynamic frame dynamics and gauge dynamics in general relativity. Just as coordinate gauge modes can propagate superluminally without violating causality, the frame-dependent modes in BDNK theory can have superluminal characteristics without affecting the physical (frame-invariant) observables. The caveat, noted by the authors, is that this is a (0+1)D test with no spatial propagation by construction; the (1+1)D tests in the subsequent section provide a more stringent check.

### 6.4 Frame-Dependence of Hydrodynamic Variables
The bottom panel directly illustrates the theoretical result of Eq. (55) in the paper: the temperature (and hence other thermodynamic quantities derived from the equation of state) depends on the choice of hydrodynamic frame outside of equilibrium. This is not a deficiency of the theory but rather a feature of the general-frame formulation. The frame-invariant observable T^{tau tau} can be used to map between frames.

### 6.5 Negative Temperature and the Weak Energy Condition
The occurrence of T < 0 for the epsilon-dot_0 = -2 initial data illustrates the constraint analysis of Eq. (74)-(75). The BDNK causality constraints only require P > (Gamma - 1)/Gamma * (eta/tau_Q - m*n), which can be negative. The additional constraint tau_Q > eta/(m*n) (Eq. (76)) would guarantee P > 0 but is not enforced in this work. The figure shows that T < 0 arises from far-from-equilibrium initial data and is not a fundamental instability -- the solution still evolves smoothly and would eventually reach T > 0 at sufficiently late times.

---

## 7. Parameters

All parameters used for this figure, consolidated from Table I and the text:

| Parameter | Value | Description |
|-----------|-------|-------------|
| Gamma     | 4/3   | Adiabatic index |
| m         | 1     | Particle mass |
| V-hat     | 1/10  | Dimensionless combined viscosity (inverse Reynolds number) |
| sigma-hat | 0     | Dimensionless thermal conductivity parameter |
| tau-hat   | 0.5, 1, 2 | Dimensionless relaxation time parameter |
| L         | 1     | Characteristic length scale |
| epsilon_0 | 0.25  | Initial energy density at tau = 1 |
| dot(epsilon)_0 | -2, 0, 2 | Initial time derivative of energy density at tau = 1 |
| n_0       | 0.1   | Particle number density constant (n(tau) = n_0/tau) |
| tau range | [1, 20] | Integration domain in proper time |

### Derived Quantities at Initial Time (tau = 1)
- n(1) = n_0 = 0.1
- P(1) = (Gamma - 1)*(epsilon_0 - m*n(1)) = (1/3)*(0.25 - 0.1) = 0.05
- rho(1) = epsilon_0 + P(1) = 0.30
- c_s^2(1) = Gamma*P(1)/rho(1) = (4/3)*0.05/0.30 = 2/9
- tau_epsilon for tau-hat = 0.5: V-hat * tau-hat = 0.05
- tau_epsilon for tau-hat = 1: V-hat * tau-hat = 0.10
- tau_epsilon for tau-hat = 2: V-hat * tau-hat = 0.20
- tau_P = 2*(Gamma - 1)*V-hat = 2*(1/3)*(1/10) = 1/15
- V = V-hat * rho * c_s^2 = (1/10)*0.30*(2/9) = 1/150

Note: tau_epsilon, V, and other transport coefficients depend on the local state (epsilon, n) and therefore evolve with tau. The values above are only the initial values. During integration, they must be recomputed at each step from the current epsilon and n(tau) = n_0/tau.
