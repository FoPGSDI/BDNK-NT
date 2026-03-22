# Mathematical Expression Conventions for NT-Disk LaTeX Translation

## Status: DRAFT - To be refined by Stage 1 agents

## 1. Document Class and Packages

```latex
\documentclass[aps,prd,twocolumn,superscriptaddress,nofootinbib]{revtex4-2}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{bm}           % Bold math
\usepackage{mathrsfs}     % Script fonts
\usepackage{hyperref}
\usepackage{physics}      % For differential operators if needed
```

## 2. Equation Numbering

The paper uses hierarchical numbering: **(section.subsection.number)**
- Example: Eq. (2.1.1), Eq. (5.6.14a), Eq. (2.5.18b)
- Sub-equations use letters: (2.1.5a), (2.1.5b)
- Implementation: Use `\tag{}` for explicit numbering or custom counter

```latex
% Custom equation numbering
\renewcommand{\theequation}{\thesection.\thesubsection.\arabic{equation}}
% Or use \tag{} for each equation explicitly
```

## 3. Fundamental Constants and Notation

| Symbol | LaTeX | Description |
|--------|-------|-------------|
| h | `\hbar` or `h` | Planck's constant (paper uses h, not hbar) |
| m_e | `m_e` | Rest mass of electron |
| m_p | `m_p` | Rest mass of proton |
| e | `e` | Charge of electron |
| c | `c` | Speed of light |
| alpha | `\alpha` | Fine-structure constant |
| r_0 | `r_0` | Classical electron radius |
| R_y | `R_y` | Rydberg energy |
| Z | `Z` | Charge of ions in plasma |
| A | `\mathcal{A}` | Atomic weight of ions |
| k | `k` | Boltzmann's constant |
| xi | `\xi` | Euler constant (= 1.78...) |
| G | `G` | Gravitational constant |
| M | `M` | Mass of black hole |

## 4. Vector and Tensor Notation

### 4-vectors and 4-tensors
- **Bold sans-serif** for 4-vectors: `\mathbf{u}`, `\mathbf{p}`
- Bold extra-bold sans-serif for 4-tensors: e.g., **g**, **T**
- Greek indices alpha, beta = 0,1,2,3
- Latin indices a,b = 1,2,3 (spatial)

```latex
% 4-vectors: bold upright
\newcommand{\fvec}[1]{\mathbf{#1}}
% Example: \fvec{u} for 4-velocity u
```

### 3-vectors
- Bold face: `\mathbf{v}`, `\mathbf{B}`, `\mathbf{E}`
- Or arrow notation in some contexts

### Specific notation
- `\mathbf{u}` = 4-velocity of fluid
- `\mathbf{n}` = unit vector
- `\mathbf{e}_{\hat{r}}`, etc. = orthonormal basis vectors (with hats)
- Hat on indices for orthonormal frame: `e_{\hat{0}}`, `e_{\hat{r}}`

## 5. Differential Operators

| Operator | LaTeX | Usage |
|----------|-------|-------|
| Gradient | `\boldsymbol{\nabla}` or `\nabla` | 3-gradient |
| Divergence | `\nabla \cdot` | `\nabla \cdot \mathbf{v}` |
| Curl | `\nabla \times` | `\nabla \times \mathbf{B}` |
| Covariant derivative | `\nabla` (no bold) | 4-covariant derivative |
| d/dt | `\frac{d}{dt}` | Total derivative |
| partial | `\frac{\partial}{\partial t}` | Partial derivative |
| Lie derivative | `\mathscr{L}_{\xi}` | Along vector xi |

## 6. Special Symbols Used in the Paper

| Symbol | LaTeX | Meaning |
|--------|-------|---------|
| rho_0 | `\rho_0` | Rest-mass density |
| p | `p` | Isotropic pressure |
| rho | `\rho` | Total density of mass-energy |
| Pi | `\Pi` | Specific internal energy |
| T | `T` | Temperature |
| s | `s` | Entropy per baryon |
| s_0 | `s_0` | Entropy per unit mass |
| mu | `\mu` | Chemical potential |
| V | `\mathcal{V}` | Specific volume = 1/rho_0 |
| V_0 | `V_0` | = 1/rho_0 |
| n | `n` | Number density of baryons |
| m_B | `m_B` | Mean rest mass of a baryon |
| Gamma | `\Gamma` | Adiabatic index |
| c_s | `c_s` | Speed of sound |
| theta | `\theta` | Expansion scalar |
| sigma_ab | `\sigma_{\alpha\beta}` | Shear tensor |
| omega_ab | `\omega_{\alpha\beta}` | Rotation/vorticity tensor |

## 7. Accretion-Specific Notation

| Symbol | LaTeX | Meaning |
|--------|-------|---------|
| M_dot_0 | `\dot{M}_0` | Accretion rate |
| r_g | `r_g` | Gravitational radius = 2GM/c^2 |
| r_s | `r_s` | Sonic radius |
| L_crit | `L_{\text{crit}}` | Critical (Eddington) luminosity |
| sigma_T | `\sigma_T` | Thomson cross section |
| a_* | `a_*` | Dimensionless spin parameter |
| M_* | `M_*` | = M/M_sun |
| M_dot_* | `\dot{M}_*` | = M_dot/M_dot_crit |
| Sigma | `\Sigma` | Surface density of disk |
| W | `W` | Integrated stress |
| h | `h` | Disk half-thickness (context dependent) |

## 8. Kerr Metric Functions (Section 5.4)

```latex
\newcommand{\scripta}{\mathscr{A}}   % script A
\newcommand{\scriptb}{\mathscr{B}}   % script B
\newcommand{\scriptc}{\mathscr{C}}   % script C
\newcommand{\scriptd}{\mathscr{D}}   % script D
\newcommand{\scripte}{\mathscr{E}}   % script E
\newcommand{\scriptf}{\mathscr{F}}   % script F
\newcommand{\scriptg}{\mathscr{G}}   % script G
% Delta = r^2 - 2Mr + a^2
\newcommand{\KDelta}{\Delta}
```

## 9. Cross-Section and Emission Notation

| Symbol | LaTeX | Meaning |
|--------|-------|---------|
| d sigma/d Omega | `\frac{d\sigma}{d\Omega}` | Differential cross section |
| epsilon_nu | `\varepsilon_\nu` | Emissivity per unit frequency |
| kappa_nu | `\kappa_\nu` | Absorption coefficient |
| kappa_s | `\kappa_s` | Scattering coefficient |
| tau_nu | `\tau_\nu` | Optical depth |
| I_nu | `I_\nu` | Specific intensity |
| J_nu | `J_\nu` | Mean intensity |
| F_nu | `F_\nu` | Specific flux |
| B_nu | `B_\nu` | Planck function |
| G(v,u) | `G(\nu,u)` | Gaunt factor |
| G_bar | `\bar{G}` | Mean Gaunt factor |
| G_bf | `G_{bf}` | Bound-free Gaunt factor |

## 10. Figure Handling

Figures should be included as placeholders with descriptive captions:

```latex
\begin{figure}[htbp]
\centering
% \includegraphics[width=\columnwidth]{fig_2_1_1}
\fbox{\parbox{0.9\columnwidth}{\centering [Figure 2.1.1 placeholder]\\
Regions and Gaunt factors for bremsstrahlung...}}
\caption{...original caption text...}
\label{fig:2.1.1}
\end{figure}
```

## 11. Reference Style

References in the paper are cited by author-year in text. Use BibTeX with:

```latex
\bibliographystyle{apsrev4-2}
\bibliography{NT-Disk-translated}
```

BibTeX entries should use keys like `Shakura1973`, `Novikov1973`, etc.

## 12. Section/Subsection Formatting

```latex
\section{Introductory Remarks}
\label{sec:1}

\section{Thermal Bremsstrahlung...}
\label{sec:2}

\subsection{Thermal Bremsstrahlung}
\label{sec:2.1}
```

## 13. Units Convention

- CGS-Gaussian units throughout
- Geometrized units (c = G = 1) used explicitly in relativistic sections (S5.4 onward)
- When both are used, paper states which convention applies

## 14. Footnotes

Use `\footnote{}` for paper footnotes marked with daggers and double-daggers.

## 15. Italics Convention

- *Italics* for emphasis and defined terms (first occurrence)
- Section references: "see S2.1" -> `see \S\ref{sec:2.1}`
- "Basic references" and "Basic physics and formulas" headers in italics
