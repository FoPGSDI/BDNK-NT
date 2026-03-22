# Figure Analysis: `acaus_instab.pdf` (Fig. `\ref{fig:acaus_instab}`)

**Source:** `/Users/hyw/Desktop/Agent/BDNK/acaus_instab.pdf`
**Paper reference:** Sec. III.C of `paper.tex`, lines 1096--1144; caption at lines 1140--1144.

---

## 1. Visual Description

The figure consists of two panels stacked vertically, sharing a common horizontal axis.

### Top Panel -- Weakly Superluminal and Subluminal Frames

The top panel shows the velocity profile $v(x)$ for three different hydrodynamic frames ($\hat{\tau} = 0.4, 0.5, 1.5$) at two times:

- **Dotted line ($t = 0$):** The initial data profile. It is a smooth error-function transition from $v \approx 0.6$ on the left ($x \to -\infty$) down to $v \approx 0.515$ on the right ($x \to +\infty$), centered near $x = 0$ with a transition width set by $w = 10$.
- **Solid line ($t = 1582$):** The late-time solution, after all transients have damped out. The profile has relaxed to a sharper, steeper transition compared to the initial data and now closely approximates the steady-state (ODE) shockwave solution. The transition region has shifted slightly and narrowed relative to the initial data.

Crucially, all three frames ($\hat{\tau} = 0.4, 0.5, 1.5$) produce solutions that are **identical up to the resolution of the plot** at both $t = 0$ and $t = 1582$. There is no visible distinction between the subluminal case ($\hat{\tau} = 1.5$, $c_+ \sim 0.9$) and the weakly superluminal cases ($\hat{\tau} = 0.5$, $c_+ \sim 1.5$; $\hat{\tau} = 0.4$, $c_+ \sim 1.6$). The three curves overlap completely.

### Bottom Panel -- Wildly Superluminal Frame ($\hat{\tau} = 0.25$)

The bottom panel shows the velocity profile $v(x)$ for a single wildly superluminal frame with $\hat{\tau} = 0.25$ ($c_+ \sim 2$) at three closely spaced early times:

- **Dotted line ($t = 0.27$):** A bump has begun to form near $x \sim 10$--$20$, to the right of the initial shockwave transition. The velocity dips below the right-state value near $x \sim 40$.
- **Dot-dash line ($t = 0.31$):** The bump has grown significantly in amplitude, now reaching $v \approx 0.63$, above the left-state value. The structure of oscillations becomes more pronounced, with a secondary dip visible near $x \sim 35$--$45$.
- **Solid line ($t = 0.36$):** The bump has grown further and the oscillatory structure has amplified dramatically. A very large overshoot appears near $x \sim 10$--$20$, and a very deep, narrow dip forms near $x \sim 40$--$50$, where $v$ drops sharply to approximately $v \approx 0.49$ or below.

**Inset (bottom-right corner):** A magnified view of the sharp downward feature near $x \sim 40$--$50$ at $t = 0.36$, rendered at five different numerical resolutions $N \in \{2^7, 2^8, 2^9, 2^{10}, 2^{11}\}$ shown in increasingly dark shades of gray (lightest = lowest resolution, darkest/black = highest resolution). The curves appear to be converging to a well-defined, very narrow and deep spike as resolution increases. This convergence behavior indicates the feature is present in the continuum PDE solution and is not a numerical artifact.

---

## 2. Axes and Labels

| Axis | Quantity | Range |
|------|----------|-------|
| Horizontal ($x$-axis) | Spatial coordinate $x$ | $[-100, 100]$ (both panels) |
| Vertical ($y$-axis) | Flow three-velocity $v$ | $[0.5, 0.6]$ approximately (both panels) |

Both panels share the same $x$-axis label printed once below the bottom panel. The $y$-axis is labeled $v$ on each panel individually. Tick marks on the $y$-axis show $0.5$ and $0.6$.

**Annotations in the panels:**
- Top panel: A text box in the upper right reads "$\hat{\tau} = 0.4, 0.5, 1.5$"; a legend at left identifies the dotted line as $t = 0$ and the solid line as $t = 1582$.
- Bottom panel: A text box reads "$\hat{\tau} = 0.25$"; a legend identifies the dotted line as $t = 0.27$, the dot-dash line as $t = 0.31$, and the solid line as $t = 0.36$.

---

## 3. Line Styles

### Top Panel
| Style | Meaning |
|-------|---------|
| **Dotted** | Initial data ($t = 0$). All three $\hat{\tau}$ values produce the same initial profile. |
| **Solid** | Late-time solution ($t = 1582$). Again, all three $\hat{\tau}$ values overlap. |

(No color or shade differentiation is needed in the top panel because all three frames are indistinguishable at the resolution of the plot.)

### Bottom Panel
| Style | Meaning |
|-------|---------|
| **Dotted** | $t = 0.27$ -- early stage of instability growth |
| **Dot-dash** | $t = 0.31$ -- intermediate growth |
| **Solid** | $t = 0.36$ -- well-developed instability, just before simulation crash |

### Inset (Resolution Study)
| Shade | Resolution |
|-------|------------|
| Lightest gray | $N = 2^7 = 128$ |
| Light gray | $N = 2^8 = 256$ |
| Medium gray | $N = 2^9 = 512$ |
| Dark gray | $N = 2^{10} = 1024$ |
| Black | $N = 2^{11} = 2048$ |

The progressively darker lines converge toward a definite sharp spike profile, indicating a well-resolved feature in the continuum limit rather than a numerical artifact.

---

## 4. Key Observations

### 4.1 Weakly Superluminal Frames Produce No Issues

The top panel demonstrates that choosing a hydrodynamic frame with weakly superluminal characteristics ($\hat{\tau} = 0.5$ giving $c_+ \sim 1.5$) does **not** cause any qualitative change in the solution compared to the strictly subluminal frame ($\hat{\tau} = 1.5$ giving $c_+ \sim 0.9$). The three solutions are identical at plot resolution at both $t = 0$ and $t = 1582$, though the text notes they converge to slightly different solutions in the continuum limit. No superluminal propagation is observed: the "bump" feature sourced by the deviation of initial data from the exact shockwave profile propagates downstream at roughly the sound speed, not at or above the speed of light.

### 4.2 Wildly Superluminal Frame Triggers Fast Instability

For $\hat{\tau} = 0.25$ ($c_+ \sim 2$), the instability develops on a timescale of $O(0.1)$, compared to the $O(10^3)$ timescale needed for the stable solutions to relax. Two distinct pathological features develop:

1. **Unboundedly growing bump ($x \sim 10$--$20$):** Rather than growing to a fixed amplitude and propagating away (as occurs for stable frames), the bump grows without bound and does not propagate. At $t = 0.36$ it overshoots the left-state velocity.

2. **Sharp feature / spike ($x \sim 40$--$50$):** A very narrow, deep dip in $v$ develops, shown in the inset. The time derivatives $\dot{\epsilon}$ and $\dot{v}$ appear to diverge in finite time at this location. Despite this, the text reports that no state variables ($c_s, c_\pm, T^{ta}, \epsilon, P, n$) obtain unphysical values at this point.

### 4.3 Convergence of the Sharp Feature

The inset's resolution study (five resolutions spanning a factor of 16 in grid spacing) shows the sharp feature converging as resolution increases. This is strong evidence that the rapid growth and potential finite-time singularity are properties of the continuum PDE solution, not numerical artifacts. Shortly beyond $t = 0.36$, the sharp feature sources an oscillatory numerical instability that crashes the simulation -- but the growth leading up to it is physical.

### 4.4 No Superluminal Signal Propagation

Even for the weakly superluminal cases, no features are observed to propagate superluminally or even upstream. The bump propagates downstream at approximately the sound speed. This provides evidence that superluminal characteristics are not *a priori* related to physical propagation speeds.

---

## 5. Numerical / Implementation Notes

### 5.1 CFL Requirements

The numerical method is the conservative finite volume scheme of Pandya et al. (2022), using Heun's method (TVD-RK2) for time integration and WENO/CWENO spatial discretization.

| Frame | $\hat{\tau}$ | $c_+$ | CFL number $\lambda$ | Note |
|-------|-------------|--------|----------------------|------|
| Subluminal | 1.5 | $\sim 0.9$ | 0.1 | Standard |
| Weakly superluminal | 0.5 | $\sim 1.5$ | 0.1 | No issues |
| Stiff superluminal | 0.4 | $\sim 1.6$ | **0.01** | Order of magnitude smaller; equations become "stiff" |
| Wildly superluminal | 0.25 | $\sim 2$ | **0.01** | Instability develops regardless of time step |

The stiffness arises as the relaxation time $\hat{\tau}$ decreases, requiring a significantly reduced CFL number for stable time integration. The $\hat{\tau} = 0.4$ case requires $\lambda = 0.01$, an order of magnitude smaller than the $\lambda = 0.1$ used for $\hat{\tau} \geq 0.5$. This stiffness behavior is analogous to what occurs in Bjorken flow for small relaxation times.

### 5.2 Convergence in the Inset

The inset shows resolutions $N = 2^7$ through $N = 2^{11}$ (128 to 2048 grid points on the domain $x \in [-100, 100]$). The behavior of the sharp feature appears to converge with increasing resolution, supporting the conclusion that this is a continuum phenomenon. The overall numerical scheme is second-order convergent in smooth regions.

### 5.3 Domain and Grid

The spatial domain spans $x \in [-100, 100]$. The initial data width parameter is $w = 10$. The left-state values are $\epsilon_L = 1$, $v_L = 0.6$, $n_L = 1$, and the right-state values are determined by the Rankine-Hugoniot conditions: $\epsilon_R \approx 1.338$, $v_R \approx 0.514$, $n_R \approx 1.250$.

---

## 6. Connection to Theory

### 6.1 Superluminal Characteristics and Causality

The BDNK formalism requires subluminal characteristics ($|c_+| < 1$) as part of its proof of well-posedness and linear stability. The causality constraint (Eq. (30) in the paper) requires:

$$\hat{\tau} \geq \frac{(\Gamma - 1)(2 - c_s^2) + c_s^2}{1 - c_s^2}$$

for the characteristics to remain subluminal. When $\hat{\tau}$ is taken below this threshold, the maximum characteristic speed $c_+$ exceeds the speed of light.

### 6.2 Physical vs. Characteristic Speeds

This figure provides direct numerical evidence that superluminal characteristics do not necessarily imply superluminal signal propagation. The weakly superluminal case ($c_+ \sim 1.5$) produces no observable superluminal features. This supports the interpretation that characteristic speeds in viscous relativistic hydrodynamics are mathematical artifacts of the PDE system rather than physical propagation speeds. Nevertheless, subluminal characteristics *guarantee* causal behavior, so the paper argues such a restriction should be an essential component of a sensible relativistic fluid theory.

### 6.3 Connection to Linear Stability

The instability observed for wildly superluminal frames ($\hat{\tau} = 0.25$) is likely related to the fact that subluminal characteristics are required in BDNK theory's proof of linear stability. Violating the causality constraints sufficiently strongly (i.e., going "wildly" superluminal) appears to trigger a genuine instability in the continuum solution, potentially involving finite-time blow-up of time derivatives.

### 6.4 Connection to Shockwave Existence

The paper draws a connection to the steady-state shockwave ODEs: when the flow velocity $v$ exceeds the maximum characteristic speed $c_+$ somewhere in the profile, the ODEs for the stationary shockwave solution have no solution. For the wildly superluminal case, $c_+ \sim 2$ is well above the flow velocity ($v \sim 0.5$--$0.6$), so the instability here is of a different nature than the $v > c_+$ instability shown in the companion figure (`shock_instability.pdf`). Instead, it appears to be a consequence of the severe violation of the linear stability constraints.

### 6.5 Recommendation

The authors suggest requiring all characteristics to be subluminal, and potentially even requiring $|c_+| = 1$ (or $|c_+| = 1 - \delta$ for infinitesimal $\delta > 0$), to ensure both causality and stability of fast shockwave solutions.

---

## 7. Parameters

All parameters for this figure are taken from Table I of the paper (line 557):

| Parameter | Value | Description |
|-----------|-------|-------------|
| $\Gamma$ | $4/3$ | Adiabatic index (ultrarelativistic ideal gas) |
| $m$ | $0.1$ | Particle mass |
| $\hat{V}$ | $4/3$ | Inverse Reynolds number (combined viscosity parameter) |
| $\hat{\sigma}$ | $0$ | Thermal conductivity parameter (zero -- pure viscous case) |
| $\hat{\tau}$ | $0.25, 0.4, 0.5, 1.5$ | Relaxation time parameter (controls characteristic speeds) |
| $L$ | $1$ | Lengthscale parameter (set to unity throughout) |
| $w$ | $10$ | Width of initial error-function transition |

### Characteristic speeds for each $\hat{\tau}$

| $\hat{\tau}$ | $c_+$ (approx.) | Classification | Panel |
|-------------|-----------------|----------------|-------|
| $1.5$ | $\sim 0.9$ | Subluminal (causal) | Top |
| $0.5$ | $\sim 1.5$ | Weakly superluminal | Top |
| $0.4$ | $\sim 1.6$ | Stiff superluminal | Top |
| $0.25$ | $\sim 2.0$ | Wildly superluminal | Bottom |

### Initial data (shockwave rest frame, Eq. (64)--(65))

| Side | $\epsilon$ | $v$ | $n$ |
|------|-----------|-----|-----|
| Left ($x \to -\infty$) | 1 | 0.6 | 1 |
| Right ($x \to +\infty$) | 1.33795 | 0.514414 | 1.25027 |

The right-state values are fixed by the Rankine-Hugoniot jump conditions for a shockwave in its rest frame.
