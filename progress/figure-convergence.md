# Figure Analysis: Convergence Plot (conv_plot.pdf)

**Figure label:** `fig:conv_plot` (Appendix B, Fig. 8 in the paper)

---

## 1. Visual Description

The figure consists of two side-by-side panels, each displaying the convergence factor Q_N(t) as a function of time t. The left panel corresponds to the **shockwave problem** (Sec. V of the paper) and the right panel corresponds to the **heat flow problem** (Sec. VI). Both panels share the same vertical axis label, Q_N(t), and each has its own horizontal time axis.

A horizontal **red dotted line** at Q_N = 4 serves as a visual reference for the expected second-order convergence rate.

---

## 2. Axes and Labels

- **Vertical axis (both panels):** Q_N(t), ranging from approximately 2 to 8. Tick marks are shown at 2, 4, 6, and 8.
- **Horizontal axis (left panel, shockwave):** t, ranging from 0 to approximately 400, with labeled ticks at 0, 150, and 300.
- **Horizontal axis (right panel, heat flow):** t, ranging from 0 to approximately 450, with labeled ticks at 0, 200, and 400.

---

## 3. Line Styles and Resolutions

Three resolutions are shown, distinguished by shade/weight:

| Resolution | Line style |
|---|---|
| N = 2^{11} (2048 points) | Light gray, thinnest |
| N = 2^{12} (4096 points) | Medium gray (dark gray), intermediate weight |
| N = 2^{13} (8192 points) | Black, thickest |

The legend appears in the upper-right area of the right panel. The convergence factor Q_N at resolution N is defined as the ratio of discrete residual norms at consecutive resolutions:

Q_N = ||R_{N/2}|| / ||R_N||

so computing Q_N at resolution N = 2^{13} requires solutions at both N = 2^{13} and N = 2^{12}, and so on. Each curve thus involves a pair of resolutions.

---

## 4. Key Observations

### Near t = 0: Second-order convergence (Q_N -> 4)

In both panels, all three resolution curves cluster tightly around the red dotted reference line Q_N = 4 at early times (roughly t < 80 in the left panel and t < 150 in the right panel). This demonstrates that the numerical scheme converges at **second order** in the grid spacing, as expected from the Heun + WENO/CWENO method of lines discretization described in Appendix B.

The highest-resolution curve (N = 2^{13}, black) stays closest to Q_N = 4, while the lowest-resolution curve (N = 2^{11}, light gray) shows the largest deviations, consistent with the Richardson expansion prediction that Q_N -> 4 only in the limit N -> infinity.

### Degradation after boundary interaction

**Left panel (shockwave):** Starting around t ~ 80-100, the convergence factor begins to deviate significantly from 4. The curves dip below 4 (reaching as low as Q_N ~ 2 for the N = 2^{13} curve near t ~ 130) and then partially recover but with persistent oscillations. The lower-resolution curves (N = 2^{11}) actually overshoot to Q_N ~ 6-7, indicating super-convergence artifacts at coarse resolution. At late times (t > 300), the curves settle at values between roughly 3.5 and 4.5, indicating convergence between first and second order.

**Right panel (heat flow):** The picture is qualitatively similar but with a sharper disruption. Around t ~ 150-180, there is a dramatic feature: the convergence factor exhibits a sharp spike (particularly visible as a tall, narrow excursion near t ~ 160-180 for all resolutions). After this transient, the curves show oscillatory behavior with Q_N fluctuating between roughly 3 and 7 for the coarser resolutions, while the N = 2^{13} curve settles closer to Q_N ~ 3.5. The disruption in the right panel is more violent than in the left panel, with the spike reaching very large and/or very small values.

### Physical interpretation of the degradation

The degradation is attributed to **interaction of outgoing transients with the ghost cell boundaries** of the computational domain. The initial data in both problems produce propagating disturbances (in the shockwave case, a bump traveling at approximately the sound speed; in the heat flow case, a transient wave). When these disturbances reach the domain boundaries (implemented via ghost cells), they reflect or otherwise contaminate the solution, degrading the convergence rate. As stated in the paper: "the solution converges at a rate between first and second order" after significant boundary interaction.

---

## 5. Numerical/Implementation Notes

### Independent residual discretization

The convergence factor Q_N is **not** computed using the same discretization as the evolution scheme. Instead, the residual R_N is evaluated using an **independent second-order Crank-Nicolson discretization** of the t-component of the stress-energy conservation law, nabla_a T^{ab} = 0 (specifically the equation (T^{tt})_{,t} + (T^{tx})_{,x} = 0 in the planar-symmetric case). This is a critical methodological point: using an independent discretization for the residual avoids the possibility that the evolution scheme's own truncation errors cancel in the convergence test, thereby providing a more honest measure of solution accuracy.

This stands in contrast to the ODE convergence tests in Table I of the paper, where a fourth-order centered finite difference discretization is used as the independent residual, and Q_N -> 16 is expected and observed (consistent with the RK4 time integrator used for those problems).

### When boundary effects kick in

- **Shockwave (left panel):** Boundary effects become significant around t ~ 80. This is consistent with a sound-speed transient (propagating at c_s ~ 1/sqrt(3) for Gamma = 4/3) traversing a domain of half-width on the order of 50-80 spatial units.
- **Heat flow (right panel):** Boundary effects become significant around t ~ 150. The heat flow domain is presumably larger or the characteristic propagation speed is slower, giving a longer clean-convergence window.

### Evolution scheme details

The PDE evolution uses the conservative finite volume method of Pandya et al. (2022):
- **Time integration:** Method of lines with the TVD second-order Runge-Kutta scheme (Heun's method).
- **Spatial reconstruction:** WENO/CWENO, which is at most fourth-order convergent in grid spacing for smooth flows.
- **CFL number:** lambda = Delta t / Delta x = 0.1 for both the shockwave and heat flow problems shown here.
- **Overall order:** The scheme is **second-order overall** because the time integrator (Heun) is second-order, even though the spatial reconstruction can achieve up to fourth order. This is why Q_N -> 4 (not 16) is the target.

---

## 6. Connection to Theory

### Expected convergence rate

The Heun/WENO scheme is second-order in both time and space (the WENO reconstruction is formally higher order in space, but the overall scheme is limited by the second-order time integrator). A second-order scheme produces truncation errors proportional to (Delta x)^2. Under grid refinement by a factor of 2 (i.e., doubling N), the residual norm should decrease by a factor of 2^2 = 4. Hence Q_N -> 4 as N -> infinity, which is precisely what is observed at early times.

### Richardson expansion

The convergence factor is derived from the Richardson expansion of the discrete solution. If u_N = u_exact + C (Delta x)^p + O((Delta x)^{p+1}), where p is the order of the scheme, then the ratio of residuals at consecutive resolutions yields Q_N = 2^p. For p = 2, this gives Q_N = 4. The fact that Q_N exceeds 4 at some finite resolutions (particularly for the coarsest grid, N = 2^{11}) can be attributed to higher-order terms in the Richardson expansion that have not yet become negligible, or to the spatial WENO reconstruction contributing convergence at a rate faster than second order in regions where the solution is smooth and time derivatives are small.

### Degradation mechanism

The degradation from Q_N = 4 after boundary interaction is expected: the ghost cell boundary treatment is at best first-order accurate (simple extrapolation or copy), so once boundary-reflected signals contaminate the interior solution, the overall convergence rate is dragged down toward first order (Q_N -> 2). The observed values of Q_N between 2 and 4 at late times are consistent with a mixture of second-order interior accuracy and first-order boundary contamination.

---

## 7. Parameters

### Left panel: Shockwave problem

This panel shows convergence results for the **stable shockwave solution** displayed in the **bottom panel of Fig. 3** (labeled `fig:shock_instability` in the source). The key parameters are:

| Parameter | Value |
|---|---|
| Adiabatic index Gamma | 4/3 |
| Particle mass m | 0.1 |
| Dimensionless bulk viscosity V-hat | 4/3 |
| Dimensionless thermal conductivity sigma-hat | 0 |
| Dimensionless relaxation time tau-hat | **3** (bottom panel; the top panel uses tau-hat = 1.5 which is unstable) |
| Shockwave width parameter w | 10 |
| CFL number lambda | 0.1 |

The bottom panel of Fig. 3 corresponds to the case where the maximum characteristic speed c_+ exceeds the flow velocity v throughout the shockwave profile, so no instability occurs. This is the tau-hat = 3 case. The convergence test is performed on this stable solution.

### Right panel: Heat flow problem

This panel shows convergence results for the **sigma-hat = 0.15 case** of the heat flow problem displayed in **Fig. 6** (labeled `fig:telegraphers` in the source). The key parameters are:

| Parameter | Value |
|---|---|
| Adiabatic index Gamma | 4/3 |
| Particle mass m | 0.1 |
| Dimensionless bulk viscosity V-hat | 2/15 |
| Dimensionless thermal conductivity sigma-hat | **0.15** |
| Dimensionless relaxation time tau-hat | **1.5** (satisfying sigma-hat/tau-hat = 0.1) |
| CFL number lambda | 0.1 |

The sigma-hat = 0.15 case is the smallest value of sigma-hat tested in Fig. 6 and is the only one of the three cases (0.15, 1.5, 7.5) that satisfies the linear stability constraint. It exhibits predominantly heat-equation-like behavior with a small wavelike transient visible in the inset of Fig. 6. This is the natural choice for a convergence test, as the other two cases violate the linear stability bound and the sigma-hat = 7.5 case eventually crashes due to an oscillatory instability.
