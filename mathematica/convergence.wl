(* ============================================================== *)
(*  convergence.wl -- Convergence testing (Fig. 7, Table III)      *)
(*  Pandya, Most, Pretorius (2022)                                *)
(*  Run: wolframscript -file convergence.wl                       *)
(* ============================================================== *)

Print["========================================"];
Print["  Convergence Testing (Fig. 7, Table III)"];
Print["========================================"];

SetDirectory[DirectoryName[$InputFileName]];
Get["bdnk_common.wl"];

If[!DirectoryQ["output"], CreateDirectory["output"]];

(* ================================================================ *)
(*  PART 1: ODE CONVERGENCE (Table III)                             *)
(*  Bjorken flow with fixed-step RK4, then independent residual     *)
(* ================================================================ *)

Print["\n========================================"];
Print["  ODE Convergence (Table III)"];
Print["========================================"];

gam = 4/3;
massBj = 1;
vHatBj = 1/10;
sigmaHatBj = 0;
n0Bj = 1/10;
eps0Bj = 0.25;
tauMin = 1.;
tauMax = 20.;

(* ---- Manual RK4 implementation ---- *)
rk4Step[rhs_, t_, y_, h_] := Module[{k1, k2, k3, k4},
  k1 = h*rhs[t, y];
  k2 = h*rhs[t + h/2, y + k1/2];
  k3 = h*rhs[t + h/2, y + k2/2];
  k4 = h*rhs[t + h, y + k3];
  y + (k1 + 2*k2 + 2*k3 + k4)/6
];

(* Bjorken RHS for RK4 *)
bjorkenRHSconv[tauHat_] := Function[{tau, y},
  Module[{epsVal, epsDotVal, nn, pp, rr, cs2, vVisc, tauEps, tauP, rhs2},
    epsVal = y[[1]];
    epsDotVal = y[[2]];
    nn = n0Bj/tau;
    pp = (gam - 1)*(epsVal - massBj*nn);
    rr = epsVal + pp;
    cs2 = gam*pp/rr;
    vVisc = vHatBj*rr*cs2;
    tauEps = vHatBj*tauHat;
    tauP = 2*(gam - 1)*vHatBj;

    rhs2 = (1/tauEps)*(
      -(1/tau)*(tau + 2*tauEps + tauP)*epsDotVal
      - (1/tau^2)*(rr*(tau + tauP) - vVisc)
    );
    {epsDotVal, rhs2}
  ]
];

(* Solve Bjorken ODE with N steps using RK4 *)
solveBjorkenRK4[tauHat_, epsDot0_, nSteps_] := Module[
  {h, rhs, y, tauGrid, epsGrid},
  h = (tauMax - tauMin)/nSteps;
  rhs = bjorkenRHSconv[tauHat];
  y = {eps0Bj, N[epsDot0]};
  tauGrid = {tauMin};
  epsGrid = {y};

  Do[
    y = rk4Step[rhs, tauMin + (i-1)*h, y, h];
    AppendTo[tauGrid, tauMin + i*h];
    AppendTo[epsGrid, y];
  , {i, 1, nSteps}];

  {tauGrid, epsGrid}
];

(* ---- Compute independent residual ---- *)
(* 4th-order centered FD of the Bjorken ODE:
   tauEps*eps'' + (1/tau)*(tau + 2*tauEps + tauP)*eps'
   + (1/tau^2)*(rho*(tau + tauP) - V) = 0  *)

computeBjorkenResidual[tauGrid_, epsGrid_, tauHat_] := Module[
  {nn, h, residual, tauEps, tauP},
  nn = Length[tauGrid];
  h = tauGrid[[2]] - tauGrid[[1]];
  tauEps = vHatBj*tauHat;
  tauP = 2*(gam - 1)*vHatBj;

  residual = Table[
    Module[{tau, epsVal, epsDot, epsDD, nVal, pp, rr, cs2, vVisc},
      tau = tauGrid[[i]];
      epsVal = epsGrid[[i, 1]];

      (* 4th-order centered FD for eps' *)
      epsDot = (-epsGrid[[i+2,1]] + 8*epsGrid[[i+1,1]]
                - 8*epsGrid[[i-1,1]] + epsGrid[[i-2,1]])/(12*h);

      (* 4th-order centered FD for eps'' *)
      epsDD = (-epsGrid[[i+2,1]] + 16*epsGrid[[i+1,1]]
               - 30*epsGrid[[i,1]] + 16*epsGrid[[i-1,1]]
               - epsGrid[[i-2,1]])/(12*h^2);

      nVal = n0Bj/tau;
      pp = (gam - 1)*(epsVal - massBj*nVal);
      rr = epsVal + pp;
      cs2 = gam*pp/rr;
      vVisc = vHatBj*rr*cs2;

      (* Residual = LHS of the ODE (should be zero for exact solution) *)
      tauEps*epsDD + (1/tau)*(tau + 2*tauEps + tauP)*epsDot
      + (1/tau^2)*(rr*(tau + tauP) - vVisc)
    ],
    {i, 3, nn - 2}
  ];

  h*Total[Abs[residual]]  (* discrete L1 norm: h * sum |R_i| *)
];

(* ---- Run convergence tests ---- *)
Print["\n--- Bjorken flow convergence ---"];

tauHatValues = {0.5, 1, 2};
edot0 = -2;  (* use the stiffest initial condition *)

(* Resolutions: N/4, N/2, N for N = 2^11 = 2048 *)
nStepsBase = {2^9, 2^10, 2^11, 2^12, 2^13};  (* 512 to 8192 *)

Print["\nTable III: ODE Convergence Factors"];
Print["================================================="];
Print[PaddedForm["Test", 30], "  N     Q_{N/4}  Q_{N/2}  Q_N"];
Print["-------------------------------------------------"];

Do[
  Print["\ntauHat = ", th];

  residuals = {};
  Do[
    {tauG, epsG} = solveBjorkenRK4[th, edot0, nSteps];
    res = computeBjorkenResidual[tauG, epsG, th];
    AppendTo[residuals, res];
    Print["  N = ", nSteps, ", ||R|| = ", ScientificForm[res, 4]];
  , {nSteps, nStepsBase}];

  (* Compute Q factors *)
  If[Length[residuals] >= 2,
    qFactors = Table[residuals[[k-1]]/residuals[[k]], {k, 2, Length[residuals]}];
    Print["  Q factors: ", N[qFactors]];

    If[Length[qFactors] >= 3,
      Print[PaddedForm[StringForm["Bjorken, tauHat=``", th], 30],
            "  ", nStepsBase[[-1]],
            "  ", NumberForm[qFactors[[-3]], {4,1}],
            "  ", NumberForm[qFactors[[-2]], {4,1}],
            "  ", NumberForm[qFactors[[-1]], {4,1}]];
    ];
  ];
, {th, tauHatValues}];

(* ---- Shockwave ODE convergence ---- *)
Print["\n--- Shockwave ODE convergence ---"];

massShk = 0.1;
vHatShk = 2/15;
tauHatShk = 3/2;
epsLShk = 1.0; vLShk = 0.8; nLShk = 0.1;
xStartShk = -5.; xEndShk = 5.;

(* Define shockwave RHS *)
pLShk = (gam - 1)*(epsLShk - massShk*nLShk);
rhoLShk = epsLShk + pLShk;
wLShk = 1/Sqrt[1 - vLShk^2];
TtxShk = rhoLShk*wLShk^2*vLShk;
TxxShk = rhoLShk*wLShk^2*vLShk^2 + pLShk;

tauEpsShk = vHatShk*tauHatShk;
tauQShk = vHatShk*tauHatShk;
tauPShk = 2*(gam - 1)*vHatShk;

shockRHSconv[x_, y_] := Module[
  {nVal, epsVal, vVal, ww, ww2, pp, rr, cs2, vVisc, kE, sigVal, kN, kSval,
   betaE, betaN0, aCoeff, bCoeff, cCoeff, discSq, disc, cp2, cm2,
   c0, c1, c2, c3, c4, d0, d1, d2, d3,
   denomEps, denomV, epsPrime, vPrime, nPrime},

  nVal = y[[1]]; epsVal = y[[2]]; vVal = y[[3]];
  ww = 1./Sqrt[1. - vVal^2]; ww2 = 1./(1. - vVal^2);
  pp = (gam - 1)*(epsVal - massShk*nVal);
  rr = epsVal + pp; cs2 = gam*pp/rr;

  vVisc = vHatShk*rr*cs2;
  kE = -(gam - 1)*epsVal*rr^2/(nVal^2*pp);
  sigVal = 0.;
  kN = rr/(nVal^2*pp)*((gam - 1)*epsVal^2 + pp^2);
  kSval = kE + kN;

  betaE  = tauQShk*(gam - 1);
  betaN0 = tauQShk*(-(gam - 1)*massShk);

  aCoeff = rr*tauEpsShk*tauQShk;
  bCoeff = -tauEpsShk*(rr*cs2*tauQShk + vVisc) - rr*tauPShk*tauQShk;
  cCoeff = tauPShk*rr*cs2*tauQShk - betaE*vVisc;

  discSq = bCoeff^2 - 4*aCoeff*cCoeff;
  disc = Sqrt[Max[discSq, 0.]];
  cp2 = (-bCoeff + disc)/(2*aCoeff);
  cm2 = (-bCoeff - disc)/(2*aCoeff);

  c0 = betaN0*nVal*(TxxShk - pp);
  c1 = -TtxShk*(2*betaN0*nVal - rr*tauPShk + vVisc);
  c2 = (betaN0*nVal - rr*(tauEpsShk + tauPShk + tauQShk) + vVisc)*(TxxShk + epsVal) + rr^2*(tauEpsShk + tauQShk);
  c3 = rr*TtxShk*(tauEpsShk + 2*tauQShk);
  c4 = -rr*tauQShk*(TxxShk + epsVal);

  d0 = betaE*(TxxShk - pp);
  d1 = -TtxShk*(2*betaE + tauPShk);
  d2 = (TxxShk + epsVal)*(betaE + tauEpsShk + tauPShk) - rr*tauEpsShk;
  d3 = -tauEpsShk*TtxShk;

  denomEps = aCoeff*ww*vVal*(vVal^2 - cp2)*(vVal^2 - cm2);
  denomV = aCoeff*ww^3*(vVal^2 - cp2)*(vVal^2 - cm2);

  epsPrime = (c4*vVal^4 + c3*vVal^3 + c2*vVal^2 + c1*vVal + c0)/denomEps;
  vPrime = (d3*vVal^3 + d2*vVal^2 + d1*vVal + d0)/denomV;
  nPrime = -ww^2*nVal*vPrime/vVal;

  {nPrime, epsPrime, vPrime}
];

(* Solve shockwave at multiple resolutions *)
nStepsShk = {2^10, 2^11, 2^12, 2^13};

Print["\nShockwave ODE convergence:"];
shkResiduals = {};
Do[
  h = (xEndShk - xStartShk)/nSteps;
  y = {nLShk, epsLShk, vLShk - 1.0*^-6};
  xGrid = {xStartShk};
  yGrid = {y};

  Do[
    y = rk4Step[shockRHSconv, xStartShk + (i-1)*h, y, h];
    AppendTo[xGrid, xStartShk + i*h];
    AppendTo[yGrid, y];
  , {i, 1, nSteps}];

  (* Compute residual: 4th-order FD of T^{tx}_{,x} *)
  (* T^{tx}(PF) = rho*W^2*v. Check conservation of this. *)
  ttxValues = Table[
    Module[{nVal, epsVal, vVal, pp, rr, ww},
      nVal = yGrid[[i,1]]; epsVal = yGrid[[i,2]]; vVal = yGrid[[i,3]];
      pp = (gam - 1)*(epsVal - massShk*nVal);
      rr = epsVal + pp;
      ww = 1/Sqrt[1 - vVal^2];
      rr*ww^2*vVal  (* T^{tx} for perfect fluid part *)
    ],
    {i, 1, Length[yGrid]}
  ];

  res = h*Total[Table[
    Abs[(-ttxValues[[i+2]] + 8*ttxValues[[i+1]]
         - 8*ttxValues[[i-1]] + ttxValues[[i-2]])/(12*h)],
    {i, 3, Length[ttxValues] - 2}
  ]];

  AppendTo[shkResiduals, res];
  Print["  N = ", nSteps, ", ||R|| = ", ScientificForm[res, 4]];
, {nSteps, nStepsShk}];

shkQFactors = Table[shkResiduals[[k-1]]/shkResiduals[[k]], {k, 2, Length[shkResiduals]}];
Print["  Q factors: ", N[shkQFactors]];

Print["\n================================================="];
Print["  Table III Summary"];
Print["================================================="];

(* ================================================================ *)
(*  PART 2: PDE CONVERGENCE (Fig. 7)                                *)
(*  Actual PDE evolution at multiple resolutions with independent    *)
(*  Crank-Nicolson residual computed at each integration step        *)
(* ================================================================ *)

Print["\n========================================"];
Print["  PDE Convergence (Fig. 7)"];
Print["  Running actual PDE solver at 3 resolutions"];
Print["========================================"];

(* ---- Global PDE parameters ---- *)
massPDE = 0.1;
gamPDE = 4/3;
nGhostConv = 3;

(* ---- Safe numeric clamp ---- *)
safeValConv[x_] := If[NumberQ[x] && Abs[x] < 1.0*^15, x, 0.];

(* ---- BDNK components (same as heat_flow.wl) ---- *)
bdnkComponentsConv[eps_, v_, n_, dxEps_, dxV_, dxN_, dtEps_, dtV_,
                   gamV_, massV_, vHatV_, sigmaHatV_, tauHatV_] :=
Module[{pp, rr, cs2, vClamped, ww, ww2, tc,
        tauEps, tauP, tauQ, vVisc, sig, betaE, betaN0, eta0,
        divU, udotEps, uDotUx, dxEpsProj, dxNProj,
        scrE, scrP, scrQx, sigXX,
        ttt, ttx, txx, jx},

  vClamped = Clip[v, {-0.9999, 0.9999}];
  pp  = (gamV - 1)*(eps - massV*n);
  rr  = eps + pp;
  cs2 = If[Abs[rr] < 1.0*^-30, 0., gamV*pp/rr];
  ww  = 1.0/Sqrt[1.0 - vClamped^2];
  ww2 = 1.0/(1.0 - vClamped^2);

  tc = transportCoeffs[eps, n, gamV, massV, vHatV, sigmaHatV, tauHatV];
  tauEps = tc["tauEps"]; tauP = tc["tauP"]; tauQ = tc["tauQ"];
  vVisc = tc["V"]; sig = tc["sigma"]; betaE = tc["betaEps"];
  betaN0 = tc["betaN"]; eta0 = 3.0*vVisc/4.0;

  divU     = ww^3*(vClamped*dtV + dxV);
  udotEps  = ww*(dtEps + vClamped*dxEps);
  uDotUx   = ww^4*(dtV + vClamped*dxV);
  dxEpsProj = ww2*(vClamped*dtEps + dxEps);
  dxNProj   = ww2*dxN;

  scrE  = eps + tauEps*(udotEps + rr*divU);
  scrP  = pp + tauP*(udotEps + rr*divU);
  scrQx = tauQ*rr*uDotUx + betaE*dxEpsProj + betaN0*dxNProj;
  sigXX = (2.0/3.0)*ww2*divU;

  ttt = scrE*ww2 + scrP*ww2*vClamped^2 + 2*vClamped*scrQx*ww - 2*eta0*vClamped^2*sigXX;
  ttx = (scrE + scrP)*ww2*vClamped + scrQx*ww*(1 + vClamped^2) - 2*eta0*vClamped*sigXX;
  txx = scrE*ww2*vClamped^2 + scrP*ww2 + 2*scrQx*ww*vClamped - 2*eta0*sigXX;
  jx  = n*ww*vClamped;

  {safeValConv[ttt], safeValConv[ttx], safeValConv[txx], safeValConv[jx]}
];

(* ---- RHS computation (same structure as heat_flow.wl) ---- *)
computeRHSConv[epsArr_, vArr_, nArr_, dtEpsArr_, dtVArr_,
               dxV_, gamV_, massV_, vHatV_, sigmaHatV_, tauHatV_] :=
Module[{nx, dxEps, dxVa, dxN,
        ttxArr, txxArr, jxArr,
        dxTtx, dxTxx, dxJx,
        ddotEps, ddotV, dtNArr, i, eps, v, n, ww},

  nx = Length[epsArr];
  dxEps = Table[0., {nx}]; dxVa = Table[0., {nx}]; dxN = Table[0., {nx}];
  Do[
    dxEps[[i]] = (epsArr[[i+1]] - epsArr[[i-1]])/(2*dxV);
    dxVa[[i]]  = (vArr[[i+1]] - vArr[[i-1]])/(2*dxV);
    dxN[[i]]   = (nArr[[i+1]] - nArr[[i-1]])/(2*dxV);
  , {i, 2, nx-1}];
  dxEps[[1]] = dxEps[[2]]; dxEps[[nx]] = dxEps[[nx-1]];
  dxVa[[1]] = dxVa[[2]]; dxVa[[nx]] = dxVa[[nx-1]];
  dxN[[1]] = dxN[[2]]; dxN[[nx]] = dxN[[nx-1]];

  ttxArr = Table[0., {nx}]; txxArr = Table[0., {nx}]; jxArr = Table[0., {nx}];
  Do[
    Module[{comp},
      comp = bdnkComponentsConv[epsArr[[i]], Clip[vArr[[i]], {-0.9999, 0.9999}],
                                 nArr[[i]],
                                 dxEps[[i]], dxVa[[i]], dxN[[i]],
                                 dtEpsArr[[i]], dtVArr[[i]],
                                 gamV, massV, vHatV, sigmaHatV, tauHatV];
      ttxArr[[i]] = comp[[2]]; txxArr[[i]] = comp[[3]]; jxArr[[i]] = comp[[4]];
    ];
  , {i, 1, nx}];

  dxTtx = Table[0., {nx}]; dxTxx = Table[0., {nx}]; dxJx = Table[0., {nx}];
  Do[
    dxTtx[[i]] = (ttxArr[[i+1]] - ttxArr[[i-1]])/(2*dxV);
    dxTxx[[i]] = (txxArr[[i+1]] - txxArr[[i-1]])/(2*dxV);
    dxJx[[i]]  = (jxArr[[i+1]] - jxArr[[i-1]])/(2*dxV);
  , {i, 2, nx-1}];
  dxTtx[[1]] = dxTtx[[2]]; dxTtx[[nx]] = dxTtx[[nx-1]];
  dxTxx[[1]] = dxTxx[[2]]; dxTxx[[nx]] = dxTxx[[nx-1]];
  dxJx[[1]] = dxJx[[2]]; dxJx[[nx]] = dxJx[[nx-1]];

  ddotEps = Table[0., {nx}]; ddotV = Table[0., {nx}]; dtNArr = Table[0., {nx}];

  Do[
    eps = epsArr[[i]]; v = Clip[vArr[[i]], {-0.9999, 0.9999}]; n = nArr[[i]];
    ww = 1.0/Sqrt[1.0 - v^2];

    Module[{comp0, compE, compV, compN,
            ttt0, ttx0, a11, a12, a21, a22,
            he, hv, hn,
            dTttDeps, dTtxDeps, dTttDv, dTtxDv, dTttDn, dTtxDn,
            dtNi, rhsEn, rhsMom, det, ww2},

      ww2 = 1.0/(1.0 - v^2);

      comp0 = bdnkComponentsConv[eps, v, n, dxEps[[i]], dxVa[[i]], dxN[[i]],
                                  dtEpsArr[[i]], dtVArr[[i]],
                                  gamV, massV, vHatV, sigmaHatV, tauHatV];
      ttt0 = comp0[[1]]; ttx0 = comp0[[2]];

      compE = bdnkComponentsConv[eps, v, n, dxEps[[i]], dxVa[[i]], dxN[[i]],
                                  dtEpsArr[[i]]+1, dtVArr[[i]],
                                  gamV, massV, vHatV, sigmaHatV, tauHatV];
      a11 = compE[[1]] - ttt0; a21 = compE[[2]] - ttx0;

      compV = bdnkComponentsConv[eps, v, n, dxEps[[i]], dxVa[[i]], dxN[[i]],
                                  dtEpsArr[[i]], dtVArr[[i]]+1,
                                  gamV, massV, vHatV, sigmaHatV, tauHatV];
      a12 = compV[[1]] - ttt0; a22 = compV[[2]] - ttx0;

      he = Max[Abs[eps]*1.0*^-7, 1.0*^-10];
      hv = Max[Abs[v]*1.0*^-7, 1.0*^-10];
      hn = Max[Abs[n]*1.0*^-7, 1.0*^-10];

      compE = bdnkComponentsConv[eps+he, v, n, dxEps[[i]], dxVa[[i]], dxN[[i]],
                                  dtEpsArr[[i]], dtVArr[[i]], gamV, massV, vHatV, sigmaHatV, tauHatV];
      compN = bdnkComponentsConv[eps-he, v, n, dxEps[[i]], dxVa[[i]], dxN[[i]],
                                  dtEpsArr[[i]], dtVArr[[i]], gamV, massV, vHatV, sigmaHatV, tauHatV];
      dTttDeps = (compE[[1]] - compN[[1]])/(2*he);
      dTtxDeps = (compE[[2]] - compN[[2]])/(2*he);

      compE = bdnkComponentsConv[eps, v+hv, n, dxEps[[i]], dxVa[[i]], dxN[[i]],
                                  dtEpsArr[[i]], dtVArr[[i]], gamV, massV, vHatV, sigmaHatV, tauHatV];
      compN = bdnkComponentsConv[eps, v-hv, n, dxEps[[i]], dxVa[[i]], dxN[[i]],
                                  dtEpsArr[[i]], dtVArr[[i]], gamV, massV, vHatV, sigmaHatV, tauHatV];
      dTttDv = (compE[[1]] - compN[[1]])/(2*hv);
      dTtxDv = (compE[[2]] - compN[[2]])/(2*hv);

      compE = bdnkComponentsConv[eps, v, n+hn, dxEps[[i]], dxVa[[i]], dxN[[i]],
                                  dtEpsArr[[i]], dtVArr[[i]], gamV, massV, vHatV, sigmaHatV, tauHatV];
      compN = bdnkComponentsConv[eps, v, n-hn, dxEps[[i]], dxVa[[i]], dxN[[i]],
                                  dtEpsArr[[i]], dtVArr[[i]], gamV, massV, vHatV, sigmaHatV, tauHatV];
      dTttDn = (compE[[1]] - compN[[1]])/(2*hn);
      dTtxDn = (compE[[2]] - compN[[2]])/(2*hn);

      dtNi = (-dxJx[[i]] - n*ww^3*v*dtVArr[[i]])/ww;

      rhsEn  = -dxTtx[[i]] - (dTttDeps*dtEpsArr[[i]] + dTttDv*dtVArr[[i]] + dTttDn*dtNi);
      rhsMom = -dxTxx[[i]] - (dTtxDeps*dtEpsArr[[i]] + dTtxDv*dtVArr[[i]] + dTtxDn*dtNi);

      det = a11*a22 - a12*a21;
      If[Abs[det] < 1.0*^-30,
        ddotEps[[i]] = 0.; ddotV[[i]] = 0.;,
        ddotEps[[i]] = safeValConv[(a22*rhsEn - a12*rhsMom)/det];
        ddotV[[i]]   = safeValConv[(a11*rhsMom - a21*rhsEn)/det];
      ];
      dtNArr[[i]] = dtNi;
    ];
  , {i, 1, nx}];

  {dtEpsArr, dtVArr, dtNArr, ddotEps, ddotV}
];

(* ---- Boundary conditions ---- *)
applyBCAllConv[{e_, v_, n_, de_, dv_}, ng_] := {
  applyOutflowBC[e, ng], applyOutflowBC[v, ng],
  applyOutflowBC[n, ng], applyOutflowBC[de, ng],
  applyOutflowBC[dv, ng]
};

(* ---- Heun time stepper ---- *)
heunStepConv[state_, dt_, dx_, ng_, gamV_, massV_, vHatV_, sigmaHatV_, tauHatV_] :=
Module[{s0, rhs1, sStar, rhs2, sNew},
  s0 = state;
  rhs1 = computeRHSConv[s0[[1]], s0[[2]], s0[[3]], s0[[4]], s0[[5]],
                          dx, gamV, massV, vHatV, sigmaHatV, tauHatV];
  sStar = Table[s0[[k]] + dt*rhs1[[k]], {k, 5}];
  sStar[[2]] = Map[Clip[#, {-0.9999, 0.9999}]&, sStar[[2]]];
  sStar[[3]] = Map[Max[#, 1.0*^-10]&, sStar[[3]]];
  sStar[[1]] = Map[Max[#, 1.0*^-10]&, sStar[[1]]];
  sStar = applyBCAllConv[sStar, ng];

  rhs2 = computeRHSConv[sStar[[1]], sStar[[2]], sStar[[3]], sStar[[4]], sStar[[5]],
                          dx, gamV, massV, vHatV, sigmaHatV, tauHatV];
  sNew = Table[0.5*s0[[k]] + 0.5*(sStar[[k]] + dt*rhs2[[k]]), {k, 5}];
  sNew[[2]] = Map[Clip[#, {-0.9999, 0.9999}]&, sNew[[2]]];
  sNew[[3]] = Map[Max[#, 1.0*^-10]&, sNew[[3]]];
  sNew[[1]] = Map[Max[#, 1.0*^-10]&, sNew[[1]]];
  applyBCAllConv[sNew, ng]
];

(* ---- NaN/overflow check ---- *)
stateHasNaNConv[state_] := AnyTrue[Flatten[{state[[1]], state[[2]]}],
  (!NumberQ[#] || Abs[#] > 1.0*^10)&];

(* ================================================================ *)
(*  Evolve PDE and store solution snapshots at regular time          *)
(*  intervals. Returns: {snapTimes, epsSnapshots} where each         *)
(*  epsSnapshot is the eps array at that time.                       *)
(* ================================================================ *)

evolveWithSnapshots[epsInit_, vInit_, nInit_, tFinal_, dx_, cfl_,
                    gamV_, massV_, vHatV_, sigmaHatV_, tauHatV_,
                    snapInterval_, printInterval_:2000] :=
Module[{nx, state, dt, t, step, maxChar,
        snapTimes, epsSnaps, nextSnapTime},

  nx = Length[epsInit];
  state = applyBCAllConv[{N[epsInit], N[vInit], N[nInit],
                           Table[0., {nx}], Table[0., {nx}]}, nGhostConv];

  maxChar = Max[Table[
    Module[{cs},
      cs = charSpeeds[epsInit[[i]], nInit[[i]], gamV, massV, vHatV, sigmaHatV, tauHatV];
      cs["cPlus"] + Abs[vInit[[i]]]
    ], {i, nGhostConv+1, nx-nGhostConv}]];
  maxChar = Max[maxChar, 1.0];
  dt = cfl*dx/maxChar;
  Print["    dt = ", dt, ", dx = ", dx, ", max char speed = ", maxChar];

  (* Store initial snapshot *)
  snapTimes = {0.};
  epsSnaps = {state[[1]]};
  nextSnapTime = snapInterval;

  t = 0.; step = 0;
  While[t < tFinal,
    If[t + dt > tFinal, dt = tFinal - t];
    state = heunStepConv[state, dt, dx, nGhostConv, gamV, massV, vHatV, sigmaHatV, tauHatV];
    t += dt; step++;

    If[Mod[step, printInterval] == 0,
      Print["      step ", step, ", t = ", NumberForm[t, {6,2}],
            ", max|v| = ", NumberForm[Max[Abs[state[[2]]]], {5,4}]];
    ];

    If[stateHasNaNConv[state],
      Print["    STOP: Overflow at step ", step, ", t = ", t];
      Break[];
    ];

    If[t >= nextSnapTime - 1.0*^-10,
      AppendTo[snapTimes, t];
      AppendTo[epsSnaps, state[[1]]];
      nextSnapTime += snapInterval;
    ];
  ];

  Print["    t = ", t, ", steps = ", step, ", snapshots = ", Length[snapTimes]];
  {snapTimes, epsSnaps}
];

(* ================================================================ *)
(*  Self-convergence Q_N(t) computation                              *)
(*  Given solutions at 3 resolutions (N, 2N, 4N), compute           *)
(*  Q(t) = ||eps_N - eps_{2N,restricted}||                           *)
(*       / ||eps_{2N,restricted} - eps_{4N,restricted}||             *)
(*  where "restricted" means downsampled by factor 2 to match the   *)
(*  coarser grid. For 2nd order convergence, Q -> 4.                 *)
(* ================================================================ *)

restrictToCoarse[fineArr_, ng_] :=
Module[{nFine, nCoarse, result, nInteriorFine, nInteriorCoarse},
  nFine = Length[fineArr];
  nCoarse = nFine/2;
  nInteriorFine = nFine - 2*ng;
  nInteriorCoarse = nCoarse - 2*ng;

  result = Table[0., {nCoarse}];

  (* For cell-centered grids, restriction averages pairs:
     coarse cell i corresponds to fine cells 2i-1 and 2i *)
  Do[
    result[[i]] = (fineArr[[2*i - 1]] + fineArr[[2*i]])/2;
  , {i, 1, nCoarse}];

  result
];

computeSelfConvergenceQ[snapTimes1_, epsSnaps1_,
                        snapTimes2_, epsSnaps2_,
                        snapTimes3_, epsSnaps3_,
                        ng_, dx1_] :=
Module[{nSnap, qList, j},
  nSnap = Min[Length[snapTimes1], Length[snapTimes2], Length[snapTimes3]];
  qList = {};

  Do[
    Module[{eps1, eps2r, eps3r, diff12, diff23, norm12, norm23, iMin, iMax, n1},
      eps1 = epsSnaps1[[j]];
      n1 = Length[eps1];
      iMin = ng + 1; iMax = n1 - ng;

      (* Restrict finer solutions to coarsest grid *)
      eps2r = restrictToCoarse[epsSnaps2[[j]], ng];
      eps3r = restrictToCoarse[restrictToCoarse[epsSnaps3[[j]], ng], ng];

      (* Compute differences on the coarse grid interior *)
      diff12 = eps1[[iMin;;iMax]] - eps2r[[iMin;;iMax]];
      diff23 = eps2r[[iMin;;iMax]] - eps3r[[iMin;;iMax]];

      norm12 = dx1 * Total[Abs[diff12]];
      norm23 = dx1 * Total[Abs[diff23]];

      If[norm23 > 1.0*^-30,
        AppendTo[qList, {snapTimes1[[j]], norm12/norm23}];
      ];
    ];
  , {j, 2, nSnap}];  (* skip t=0 where all solutions are identical *)

  qList
];

(* ================================================================ *)
(*  SHOCKWAVE PDE CONVERGENCE (left panel)                           *)
(*  Stable case from Fig. 4: tauHat=1.5, vHat=2/15, vL=0.6          *)
(*  Domain: [-50, 50], resolutions N = {32, 64, 128}                 *)
(*  Evolve to t=50                                                   *)
(* ================================================================ *)

Print["\n--- Shockwave PDE convergence ---"];

vHatPDE = 2/15;
sigmaHatShkPDE = 0;
tauHatShkPDE = 3/2;

epsLShkPDE = 1.0; vLShkPDE = 0.6; nLShkPDE = 1.0;
{epsRShkPDE, vRShkPDE, nRShkPDE} =
  solveRankineHugoniot[epsLShkPDE, vLShkPDE, nLShkPDE, gamPDE, massPDE];
Print["  Shock left:  {", epsLShkPDE, ", ", vLShkPDE, ", ", nLShkPDE, "}"];
Print["  Shock right: {", N[epsRShkPDE], ", ", N[vRShkPDE], ", ", N[nRShkPDE], "}"];

wShkPDE = 10.0;
xMinShkPDE = -50.; xMaxShkPDE = 50.;
tFinalShkPDE = 50.;
snapIntervalShkPDE = 2.;
cflShkPDE = 0.1;

nxShkVals = {32, 64, 128};
shkSnapData = {};

Do[
  Print["\n  Nx = ", nxVal, " ..."];
  dxS = (xMaxShkPDE - xMinShkPDE)/nxVal;
  xGridS = Table[xMinShkPDE + (i - 0.5)*dxS, {i, 1, nxVal}];

  epsIS = Table[(epsRShkPDE - epsLShkPDE)/2*(Erf[x/wShkPDE] + 1) + epsLShkPDE, {x, xGridS}];
  vIS   = Table[(vLShkPDE - vRShkPDE)/2*(1 - Erf[x/wShkPDE]) + vRShkPDE, {x, xGridS}];
  nIS   = Table[(nLShkPDE - nRShkPDE)/2*(1 - Erf[x/wShkPDE]) + nRShkPDE, {x, xGridS}];

  {st, es} = evolveWithSnapshots[epsIS, vIS, nIS, tFinalShkPDE,
    dxS, cflShkPDE, gamPDE, massPDE, vHatPDE, sigmaHatShkPDE, tauHatShkPDE,
    snapIntervalShkPDE];
  AppendTo[shkSnapData, {nxVal, dxS, st, es}];
, {nxVal, nxShkVals}];

(* Compute self-convergence Q_N for shockwave *)
Print["\n  Computing self-convergence Q for shockwave..."];

qNShk = computeSelfConvergenceQ[
  shkSnapData[[1, 3]], shkSnapData[[1, 4]],
  shkSnapData[[2, 3]], shkSnapData[[2, 4]],
  shkSnapData[[3, 3]], shkSnapData[[3, 4]],
  nGhostConv, shkSnapData[[1, 2]]];

Print["  Q points: ", Length[qNShk]];
If[Length[qNShk] > 0,
  Module[{earlyPts},
    earlyPts = Select[qNShk, #[[1]] < 20 &];
    If[Length[earlyPts] > 0,
      Print["  Q early (t<20) mean: ", Mean[earlyPts[[All, 2]]]];
    ];
    Print["  Q overall mean: ", Mean[qNShk[[All, 2]]]];
  ];
];

(* ================================================================ *)
(*  HEAT FLOW PDE CONVERGENCE (right panel)                          *)
(*  sigmaHat = 0.15, tauHat = 1.5                                   *)
(*  Domain: [-50, 50], resolutions N = {32, 64, 128}                 *)
(*  Evolve to t=50                                                   *)
(* ================================================================ *)

Print["\n--- Heat flow PDE convergence ---"];

vHatHeatPDE = 2/15;
sigmaHatHeatPDE = 0.15;
tauHatHeatPDE = 1.5;

ampAConv = 0.1;
deltaConv = 1.0;
wHeatConv = 10.0;
p0Conv = 1.0/3.0;

tInitConv[x_] := ampAConv*Exp[-x^2/wHeatConv^2] + deltaConv;
epsFromTPConv[t_, p_] := p*(massPDE/t + 1/(gamPDE - 1));
nFromTPConv[t_, p_] := p/t;

xMinHeatPDE = -50.; xMaxHeatPDE = 50.;
tFinalHeatPDE = 50.;
snapIntervalHeatPDE = 2.;
cflHeatPDE = 0.1;

nxHeatVals = {32, 64, 128};
heatSnapData = {};

Do[
  Print["\n  Nx = ", nxVal, " ..."];
  dxH = (xMaxHeatPDE - xMinHeatPDE)/nxVal;
  xGridH = Table[xMinHeatPDE + (i - 0.5)*dxH, {i, 1, nxVal}];

  epsIH = Table[N[epsFromTPConv[tInitConv[x], p0Conv]], {x, xGridH}];
  vIH   = Table[0., {nxVal}];
  nIH   = Table[N[nFromTPConv[tInitConv[x], p0Conv]], {x, xGridH}];

  {st, es} = evolveWithSnapshots[epsIH, vIH, nIH, tFinalHeatPDE,
    dxH, cflHeatPDE, gamPDE, massPDE, vHatHeatPDE, sigmaHatHeatPDE, tauHatHeatPDE,
    snapIntervalHeatPDE];
  AppendTo[heatSnapData, {nxVal, dxH, st, es}];
, {nxVal, nxHeatVals}];

(* Compute self-convergence Q_N for heat flow *)
Print["\n  Computing self-convergence Q for heat flow..."];

qNHeat = computeSelfConvergenceQ[
  heatSnapData[[1, 3]], heatSnapData[[1, 4]],
  heatSnapData[[2, 3]], heatSnapData[[2, 4]],
  heatSnapData[[3, 3]], heatSnapData[[3, 4]],
  nGhostConv, heatSnapData[[1, 2]]];

Print["  Q points: ", Length[qNHeat]];
If[Length[qNHeat] > 0,
  Module[{earlyPts},
    earlyPts = Select[qNHeat, #[[1]] < 20 &];
    If[Length[earlyPts] > 0,
      Print["  Q early (t<20) mean: ", Mean[earlyPts[[All, 2]]]];
    ];
    Print["  Q overall mean: ", Mean[qNHeat[[All, 2]]]];
  ];
];

(* ================================================================ *)
(*  Generate Fig. 7: Two-panel convergence plot                      *)
(* ================================================================ *)

Print["\n--- Generating Fig. 7 ---"];

(* Shockwave left panel *)
leftPanel = If[Length[qNShk] > 0,
  ListLinePlot[qNShk,
    PlotStyle -> Directive[Black, AbsoluteThickness[1.5]],
    PlotRange -> {{0, tFinalShkPDE}, {0, 8}},
    Frame -> True, Axes -> False,
    FrameLabel -> {"t", "\!\(\*SubscriptBox[\(Q\), \(N\)]\)"},
    PlotLabel -> Style["Shockwave", 12],
    ImageSize -> 300, AspectRatio -> 0.7,
    GridLines -> {None, {{4, Directive[Red, Dashed, AbsoluteThickness[1]]}}}
  ],
  Graphics[{Text["No convergence data", {25, 4}]},
    PlotRange -> {{0, 50}, {0, 8}}, Frame -> True,
    FrameLabel -> {"t", "\!\(\*SubscriptBox[\(Q\), \(N\)]\)"},
    PlotLabel -> Style["Shockwave", 12],
    ImageSize -> 300, AspectRatio -> 0.7]
];

(* Heat flow right panel *)
rightPanel = If[Length[qNHeat] > 0,
  ListLinePlot[qNHeat,
    PlotStyle -> Directive[Black, AbsoluteThickness[1.5]],
    PlotRange -> {{0, tFinalHeatPDE}, {0, 8}},
    Frame -> True, Axes -> False,
    FrameLabel -> {"t", "\!\(\*SubscriptBox[\(Q\), \(N\)]\)"},
    PlotLabel -> Style["Heat flow (\!\(\*OverscriptBox[\(\[Sigma]\), \(^\)]\) = 0.15)", 12],
    ImageSize -> 300, AspectRatio -> 0.7,
    GridLines -> {None, {{4, Directive[Red, Dashed, AbsoluteThickness[1]]}}}
  ],
  Graphics[{Text["No convergence data", {25, 4}]},
    PlotRange -> {{0, 50}, {0, 8}}, Frame -> True,
    FrameLabel -> {"t", "\!\(\*SubscriptBox[\(Q\), \(N\)]\)"},
    PlotLabel -> Style["Heat flow (\!\(\*OverscriptBox[\(\[Sigma]\), \(^\)]\) = 0.15)", 12],
    ImageSize -> 300, AspectRatio -> 0.7]
];

fig7 = GraphicsRow[{leftPanel, rightPanel}, Spacings -> 1];
Export["output/fig7.pdf", fig7];
Print["  Exported output/fig7.pdf"];

(* Print convergence summary *)
Print["\n================================================="];
Print["  Convergence Summary"];
Print["================================================="];
Print["ODE (Bjorken): Expected Q_N -> 16 (RK4, 4th order)"];
Print["ODE (Shockwave): Expected Q_N -> 16 (RK4, 4th order)"];
Print["PDE: Expected Q_N -> 4 (Heun + 2nd order spatial, before boundary interaction)"];
Print["PDE: Degrades after boundary interaction"];

Print["\n========================================"];
Print["  Convergence Testing Complete"];
Print["========================================"];
