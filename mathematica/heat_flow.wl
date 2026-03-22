(* ============================================================== *)
(*  heat_flow.wl -- Heat conduction PDE (Figs. 5, 6)              *)
(*  Pandya, Most, Pretorius (2022)                                *)
(*  Run: wolframscript -file heat_flow.wl                         *)
(* ============================================================== *)

Print["========================================"];
Print["  Heat Flow PDE Solver (Figs. 5, 6)"];
Print["========================================"];

SetDirectory[DirectoryName[$InputFileName]];
Get["bdnk_common.wl"];

If[!DirectoryQ["output"], CreateDirectory["output"]];

gam = 4/3;
mass = 0.1;
nGhost = 3;

(* ---- Heat flow initial data (paper Eq. 95) ---- *)
ampA = 0.1;
delta = 1.0;
wHeat = 10.0;
p0 = 1.0/3.0;  (* Use float to avoid exact-rational mixing *)

tInit[x_] := ampA*Exp[-x^2/wHeat^2] + delta;
epsFromTP[t_, p_] := p*(mass/t + 1/(gam - 1));
nFromTP[t_, p_] := p/t;

Print["\nInitial data parameters:"];
Print["  A=", ampA, ", delta=", delta, ", w=", wHeat, ", P0=", N[p0]];

(* ---- Diagnostic: verify initial data produces expected gradients ---- *)
Module[{tPeak, tBg, epsPeak, epsBg, nPeak, nBg},
  tPeak = tInit[0.]; tBg = tInit[100.];
  epsPeak = epsFromTP[tPeak, p0]; epsBg = epsFromTP[tBg, p0];
  nPeak = nFromTP[tPeak, p0]; nBg = nFromTP[tBg, p0];
  Print["  T(x=0) = ", tPeak, ", T(x=far) = ", tBg];
  Print["  eps(x=0) = ", epsPeak, ", eps(x=far) = ", epsBg,
        ", diff = ", epsPeak - epsBg];
  Print["  n(x=0) = ", nPeak, ", n(x=far) = ", nBg,
        ", diff = ", nPeak - nBg];
];

(* ---- Safe numeric check: clamp non-numeric values ---- *)
safeVal[x_] := If[NumberQ[x] && Abs[x] < 1.0*^15, x, 0.];

(* ---- BDNK components computation ---- *)
bdnkComponents[eps_, v_, n_, dxEps_, dxV_, dxN_, dtEps_, dtV_,
               gam_, mass_, vHat_, sigmaHat_, tauHat_] :=
Module[{pp, rr, cs2, vClamped, ww, ww2, tc,
        tauEps, tauP, tauQ, vVisc, sig, betaE, betaN0, eta0,
        divU, udotEps, uDotUx, dxEpsProj, dxNProj,
        scrE, scrP, scrQx, sigXX,
        ttt, ttx, txx, jx},

  (* Clamp velocity to safe range *)
  vClamped = Clip[v, {-0.9999, 0.9999}];

  pp  = (gam - 1)*(eps - mass*n);
  rr  = eps + pp;
  cs2 = If[Abs[rr] < 1.0*^-30, 0., gam*pp/rr];
  ww  = 1.0/Sqrt[1.0 - vClamped^2];
  ww2 = 1.0/(1.0 - vClamped^2);

  tc = transportCoeffs[eps, n, gam, mass, vHat, sigmaHat, tauHat];
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

  {safeVal[ttt], safeVal[ttx], safeVal[txx], safeVal[jx]}
];

(* ---- Diagnostic: verify transport coefficients and heat flux ---- *)
Module[{tcTest, betaETest, betaNTest, epsTest, nTest, dxEpsTest, dxNTest, qxTest},
  epsTest = epsFromTP[delta, p0]; nTest = nFromTP[delta, p0];
  tcTest = transportCoeffs[epsTest, nTest, gam, mass, 2/15, 7.5, 75.];
  betaETest = tcTest["betaEps"]; betaNTest = tcTest["betaN"];
  (* Estimate dxEps and dxN at center of Gaussian *)
  dxEpsTest = (epsFromTP[tInit[1.], p0] - epsFromTP[tInit[-1.], p0])/2.0;
  dxNTest = (nFromTP[tInit[1.], p0] - nFromTP[tInit[-1.], p0])/2.0;
  qxTest = betaETest*dxEpsTest + betaNTest*dxNTest;
  Print["\nDiagnostic (sigmaHat=7.5, tauHat=75):"];
  Print["  sigma = ", tcTest["sigma"]];
  Print["  betaEps = ", betaETest, ", betaN = ", betaNTest];
  Print["  dxEps(center) ~ ", dxEpsTest, ", dxN(center) ~ ", dxNTest];
  Print["  Q^x(center) ~ ", qxTest];
  Print["  tauQ = ", tcTest["tauQ"], ", kappa = ", tcTest["kappa"]];
];

(* ---- RHS computation ---- *)
(* The conservation law is d_t(T^{tt}) + d_x(T^{tx}) = 0 and
   d_t(T^{tx}) + d_x(T^{xx}) = 0.  Since T^{ab} depends on the
   primitives (eps,v,n), their time derivatives (dtEps,dtV), AND
   their spatial derivatives (dxEps,dxV,dxN), the full time derivative
   d_t(T^{tt}) includes contributions from all of these evolving:

     d_t(T^{tt}) = dT^{tt}/deps * dtEps + dT^{tt}/dv * dtV + dT^{tt}/dn * dtN
                 + dT^{tt}/d(dxEps) * dx(dtEps) + dT^{tt}/d(dxV) * dx(dtV)
                 + dT^{tt}/d(dxN) * dx(dtN)
                 + dT^{tt}/d(dtEps) * ddotEps + dT^{tt}/d(dtV) * ddotV

   The last two terms are the implicit part (a11*ddotEps + a12*ddotV).
   The middle three terms involve time evolution of spatial derivatives
   and were previously MISSING -- they are essential because T^{tt}
   depends on dxV through the theta = W^3(v*dtV+dxV) expansion term,
   and T^{tx} depends on dxEps, dxN through betaEps, betaN gradients. *)

computeRHS[epsArr_, vArr_, nArr_, dtEpsArr_, dtVArr_,
           dx_, gam_, mass_, vHat_, sigmaHat_, tauHat_] :=
Module[{nx, dxEps, dxV, dxN,
        dxDtEps, dxDtV,
        ttxArr, txxArr, jxArr,
        dxTtx, dxTxx, dxJx,
        ddotEps, ddotV, dtNArr, i, eps, v, n, ww},

  nx = Length[epsArr];

  (* Spatial derivatives of primitives *)
  dxEps = Table[0., {nx}]; dxV = Table[0., {nx}]; dxN = Table[0., {nx}];
  Do[
    dxEps[[i]] = (epsArr[[i+1]] - epsArr[[i-1]])/(2*dx);
    dxV[[i]]   = (vArr[[i+1]] - vArr[[i-1]])/(2*dx);
    dxN[[i]]   = (nArr[[i+1]] - nArr[[i-1]])/(2*dx);
  , {i, 2, nx-1}];
  dxEps[[1]] = dxEps[[2]]; dxEps[[nx]] = dxEps[[nx-1]];
  dxV[[1]] = dxV[[2]]; dxV[[nx]] = dxV[[nx-1]];
  dxN[[1]] = dxN[[2]]; dxN[[nx]] = dxN[[nx-1]];

  (* Spatial derivatives of TIME derivatives (needed for the missing terms) *)
  dxDtEps = Table[0., {nx}]; dxDtV = Table[0., {nx}];
  Do[
    dxDtEps[[i]] = (dtEpsArr[[i+1]] - dtEpsArr[[i-1]])/(2*dx);
    dxDtV[[i]]   = (dtVArr[[i+1]] - dtVArr[[i-1]])/(2*dx);
  , {i, 2, nx-1}];
  dxDtEps[[1]] = dxDtEps[[2]]; dxDtEps[[nx]] = dxDtEps[[nx-1]];
  dxDtV[[1]] = dxDtV[[2]]; dxDtV[[nx]] = dxDtV[[nx-1]];

  ttxArr = Table[0., {nx}]; txxArr = Table[0., {nx}]; jxArr = Table[0., {nx}];
  Do[
    Module[{comp},
      comp = bdnkComponents[epsArr[[i]], Clip[vArr[[i]], {-0.9999, 0.9999}],
                             nArr[[i]],
                             dxEps[[i]], dxV[[i]], dxN[[i]],
                             dtEpsArr[[i]], dtVArr[[i]],
                             gam, mass, vHat, sigmaHat, tauHat];
      ttxArr[[i]] = comp[[2]]; txxArr[[i]] = comp[[3]]; jxArr[[i]] = comp[[4]];
    ];
  , {i, 1, nx}];

  dxTtx = Table[0., {nx}]; dxTxx = Table[0., {nx}]; dxJx = Table[0., {nx}];
  Do[
    dxTtx[[i]] = (ttxArr[[i+1]] - ttxArr[[i-1]])/(2*dx);
    dxTxx[[i]] = (txxArr[[i+1]] - txxArr[[i-1]])/(2*dx);
    dxJx[[i]]  = (jxArr[[i+1]] - jxArr[[i-1]])/(2*dx);
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
            he, hv, hn, hdxE, hdxV, hdxN,
            dTttDeps, dTtxDeps, dTttDv, dTtxDv, dTttDn, dTtxDn,
            dTttDdxE, dTtxDdxE, dTttDdxV, dTtxDdxV, dTttDdxN, dTtxDdxN,
            dtNi, dxDtNi, rhsEn, rhsMom, spatialTermEn, spatialTermMom,
            det, ww2},

      ww2 = 1.0/(1.0 - v^2);

      comp0 = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]],
                              gam, mass, vHat, sigmaHat, tauHat];
      ttt0 = comp0[[1]]; ttx0 = comp0[[2]];

      (* Implicit matrix: derivatives w.r.t. dtEps, dtV *)
      compE = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]]+1, dtVArr[[i]],
                              gam, mass, vHat, sigmaHat, tauHat];
      a11 = compE[[1]] - ttt0; a21 = compE[[2]] - ttx0;

      compV = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]]+1,
                              gam, mass, vHat, sigmaHat, tauHat];
      a12 = compV[[1]] - ttt0; a22 = compV[[2]] - ttx0;

      (* Derivatives w.r.t. primitive variables (eps, v, n) *)
      he = Max[Abs[eps]*1.0*^-7, 1.0*^-10];
      hv = Max[Abs[v]*1.0*^-7, 1.0*^-10];
      hn = Max[Abs[n]*1.0*^-7, 1.0*^-10];

      compE = bdnkComponents[eps+he, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]], gam, mass, vHat, sigmaHat, tauHat];
      compN = bdnkComponents[eps-he, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]], gam, mass, vHat, sigmaHat, tauHat];
      dTttDeps = (compE[[1]] - compN[[1]])/(2*he);
      dTtxDeps = (compE[[2]] - compN[[2]])/(2*he);

      compE = bdnkComponents[eps, v+hv, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]], gam, mass, vHat, sigmaHat, tauHat];
      compN = bdnkComponents[eps, v-hv, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]], gam, mass, vHat, sigmaHat, tauHat];
      dTttDv = (compE[[1]] - compN[[1]])/(2*hv);
      dTtxDv = (compE[[2]] - compN[[2]])/(2*hv);

      compE = bdnkComponents[eps, v, n+hn, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]], gam, mass, vHat, sigmaHat, tauHat];
      compN = bdnkComponents[eps, v, n-hn, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]], gam, mass, vHat, sigmaHat, tauHat];
      dTttDn = (compE[[1]] - compN[[1]])/(2*hn);
      dTtxDn = (compE[[2]] - compN[[2]])/(2*hn);

      (* Derivatives w.r.t. spatial gradients (dxEps, dxV, dxN) *)
      hdxE = Max[Abs[dxEps[[i]]]*1.0*^-5, 1.0*^-8];
      hdxV = Max[Abs[dxV[[i]]]*1.0*^-5, 1.0*^-8];
      hdxN = Max[Abs[dxN[[i]]]*1.0*^-5, 1.0*^-8];

      compE = bdnkComponents[eps, v, n, dxEps[[i]]+hdxE, dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]], gam, mass, vHat, sigmaHat, tauHat];
      compN = bdnkComponents[eps, v, n, dxEps[[i]]-hdxE, dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]], gam, mass, vHat, sigmaHat, tauHat];
      dTttDdxE = (compE[[1]] - compN[[1]])/(2*hdxE);
      dTtxDdxE = (compE[[2]] - compN[[2]])/(2*hdxE);

      compE = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]]+hdxV, dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]], gam, mass, vHat, sigmaHat, tauHat];
      compN = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]]-hdxV, dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]], gam, mass, vHat, sigmaHat, tauHat];
      dTttDdxV = (compE[[1]] - compN[[1]])/(2*hdxV);
      dTtxDdxV = (compE[[2]] - compN[[2]])/(2*hdxV);

      compE = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]]+hdxN,
                              dtEpsArr[[i]], dtVArr[[i]], gam, mass, vHat, sigmaHat, tauHat];
      compN = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]]-hdxN,
                              dtEpsArr[[i]], dtVArr[[i]], gam, mass, vHat, sigmaHat, tauHat];
      dTttDdxN = (compE[[1]] - compN[[1]])/(2*hdxN);
      dTtxDdxN = (compE[[2]] - compN[[2]])/(2*hdxN);

      (* Time derivative of n from baryon conservation *)
      dtNi = (-dxJx[[i]] - n*ww^3*v*dtVArr[[i]])/ww;

      (* Spatial derivative of dtN: dx(dtN) = dx(-dxJx/ww - n*ww^2*v*dtV) *)
      (* For simplicity, approximate dx(dtN) from baryon conservation:
         dt(n) = -d_x(n*W*v)/W.  Since W~1 and v~0 initially,
         dtN ~ -n*dx(dtV) - dtV*dxN approximately *)
      dxDtNi = -n*dxDtV[[i]] - dtVArr[[i]]*dxN[[i]];

      (* Spatial-derivative evolution contributions to d_t(T^{tt}) and d_t(T^{tx}):
         d_t(dxEps) = dx(dtEps), d_t(dxV) = dx(dtV), d_t(dxN) = dx(dtN) *)
      spatialTermEn  = dTttDdxE*dxDtEps[[i]] + dTttDdxV*dxDtV[[i]] + dTttDdxN*dxDtNi;
      spatialTermMom = dTtxDdxE*dxDtEps[[i]] + dTtxDdxV*dxDtV[[i]] + dTtxDdxN*dxDtNi;

      rhsEn  = -dxTtx[[i]] - (dTttDeps*dtEpsArr[[i]] + dTttDv*dtVArr[[i]] + dTttDn*dtNi)
               - spatialTermEn;
      rhsMom = -dxTxx[[i]] - (dTtxDeps*dtEpsArr[[i]] + dTtxDv*dtVArr[[i]] + dTtxDn*dtNi)
               - spatialTermMom;

      det = a11*a22 - a12*a21;
      If[Abs[det] < 1.0*^-30,
        ddotEps[[i]] = 0.; ddotV[[i]] = 0.;,
        ddotEps[[i]] = safeVal[(a22*rhsEn - a12*rhsMom)/det];
        ddotV[[i]]   = safeVal[(a11*rhsMom - a21*rhsEn)/det];
      ];
      dtNArr[[i]] = dtNi;
    ];
  , {i, 1, nx}];

  {dtEpsArr, dtVArr, dtNArr, ddotEps, ddotV}
];

applyBCAll[{e_, v_, n_, de_, dv_}, ng_] := {
  applyOutflowBC[e, ng], applyOutflowBC[v, ng],
  applyOutflowBC[n, ng], applyOutflowBC[de, ng],
  applyOutflowBC[dv, ng]
};

heunStepH[state_, dt_, dx_, ng_, gam_, mass_, vHat_, sigmaHat_, tauHat_] :=
Module[{s0, rhs1, sStar, rhs2, sNew},
  s0 = state;
  rhs1 = computeRHS[s0[[1]], s0[[2]], s0[[3]], s0[[4]], s0[[5]],
                     dx, gam, mass, vHat, sigmaHat, tauHat];
  sStar = Table[s0[[k]] + dt*rhs1[[k]], {k, 5}];
  (* Clip velocity element-wise *)
  sStar[[2]] = Map[Clip[#, {-0.9999, 0.9999}]&, sStar[[2]]];
  sStar[[3]] = Map[Max[#, 1.0*^-10]&, sStar[[3]]];
  sStar[[1]] = Map[Max[#, 1.0*^-10]&, sStar[[1]]];
  sStar = applyBCAll[sStar, ng];

  rhs2 = computeRHS[sStar[[1]], sStar[[2]], sStar[[3]], sStar[[4]], sStar[[5]],
                     dx, gam, mass, vHat, sigmaHat, tauHat];
  sNew = Table[0.5*s0[[k]] + 0.5*(sStar[[k]] + dt*rhs2[[k]]), {k, 5}];
  sNew[[2]] = Map[Clip[#, {-0.9999, 0.9999}]&, sNew[[2]]];
  sNew[[3]] = Map[Max[#, 1.0*^-10]&, sNew[[3]]];
  sNew[[1]] = Map[Max[#, 1.0*^-10]&, sNew[[1]]];
  applyBCAll[sNew, ng]
];

(* ---- Check for NaN/Infinity in state ---- *)
stateHasNaN[state_] := AnyTrue[Flatten[{state[[1]], state[[2]]}],
  (!NumberQ[#] || Abs[#] > 1.0*^10)&];

evolveHeat[epsInit_, vInit_, nInit_, tFinal_, dx_, cfl_,
           gam_, mass_, vHat_, sigmaHat_, tauHat_,
           printInterval_:100] :=
Module[{nx, state, dt, t, step, maxChar},
  nx = Length[epsInit];
  state = applyBCAll[{N[epsInit], N[vInit], N[nInit],
                       Table[0., {nx}], Table[0., {nx}]}, nGhost];

  maxChar = Max[Table[
    Module[{cs},
      cs = charSpeeds[epsInit[[i]], nInit[[i]], gam, mass, vHat, sigmaHat, tauHat];
      cs["cPlus"] + Abs[vInit[[i]]]
    ], {i, nGhost+1, nx-nGhost}]];
  maxChar = Max[maxChar, 1.0];
  dt = cfl*dx/maxChar;
  Print["  dt = ", dt, ", dx = ", dx, ", max char speed = ", maxChar];

  t = 0.; step = 0;
  While[t < tFinal,
    If[t + dt > tFinal, dt = tFinal - t];
    state = heunStepH[state, dt, dx, nGhost, gam, mass, vHat, sigmaHat, tauHat];
    t += dt; step++;
    If[Mod[step, printInterval] == 0,
      Print["    step ", step, ", t = ", NumberForm[t, {6,2}],
            ", max|v| = ", NumberForm[Max[Abs[state[[2]]]], {5,4}],
            ", max|dtV| = ", NumberForm[Max[Abs[state[[5]]]], {5,4}]];
    ];
    If[stateHasNaN[state],
      Print["  STOP: Overflow at step ", step, ", t = ", t];
      Break[];
    ];
  ];
  Print["  t = ", t, ", steps = ", step];
  state
];

(* ================================================================ *)
(*  FIG. 5: Heat flow stationary test                               *)
(* ================================================================ *)

Print["\n========================================"];
Print["  Fig. 5: Heat Flow Stationary Test"];
Print["========================================"];

vHatF5 = 2/15;
tauHatF5 = 3/2;
xMinH = -100.; xMaxH = 100.;
nxValues = {128, 256, 512};

(* --- Top panel: sigmaHat = 0 --- *)
Print["\n--- sigmaHat = 0 (stationary) ---"];

epsDotSigma0 = {};
Do[
  Print["  Nx = ", nxVal];
  dxH = (xMaxH - xMinH)/nxVal;
  xGridH = Table[xMinH + (i-0.5)*dxH, {i, 1, nxVal}];
  epsI = Table[N[epsFromTP[tInit[x], p0]], {x, xGridH}];
  vI   = Table[0., {nxVal}];
  nI   = Table[N[nFromTP[tInit[x], p0]], {x, xGridH}];

  dtSmall = 0.01;
  stH = evolveHeat[epsI, vI, nI, dtSmall,
    dxH, 0.1, gam, mass, vHatF5, 0, tauHatF5, 10000];
  edArr = (stH[[1]] - epsI)/dtSmall;
  AppendTo[epsDotSigma0, {xGridH, Abs[edArr]}];
  Print["    max|edot| = ", Max[Abs[edArr[[nGhost+1;;nxVal-nGhost]]]]];
, {nxVal, nxValues}];

(* --- Bottom panel: sigmaHat = 1/3 --- *)
Print["\n--- sigmaHat = 1/3 (dynamical) ---"];

epsDotSigma13 = {};
Do[
  Print["  Nx = ", nxVal];
  dxH = (xMaxH - xMinH)/nxVal;
  xGridH = Table[xMinH + (i-0.5)*dxH, {i, 1, nxVal}];
  epsI = Table[N[epsFromTP[tInit[x], p0]], {x, xGridH}];
  vI   = Table[0., {nxVal}];
  nI   = Table[N[nFromTP[tInit[x], p0]], {x, xGridH}];

  dtSmall = 0.01;
  stH = evolveHeat[epsI, vI, nI, dtSmall,
    dxH, 0.1, gam, mass, vHatF5, 1/3, tauHatF5, 10000];
  edArr = (stH[[1]] - epsI)/dtSmall;
  AppendTo[epsDotSigma13, {xGridH, Abs[edArr]}];
  Print["    max|edot| = ", Max[Abs[edArr[[nGhost+1;;nxVal-nGhost]]]]];
, {nxVal, nxValues}];

(* --- Generate Fig. 5 --- *)
Print["\n--- Generating Fig. 5 ---"];

grayStyles = Table[
  Directive[GrayLevel[0.7 - 0.3*k], AbsoluteThickness[1.5]], {k, 1, 3}];

topPlotF5 = ListLinePlot[
  Table[Transpose[{epsDotSigma0[[k,1]], epsDotSigma0[[k,2]]}], {k, 1, 3}],
  PlotStyle -> grayStyles,
  PlotRange -> {{xMinH, xMaxH}, All},
  Frame -> True,
  FrameLabel -> {"x", "|\!\(\*OverscriptBox[\(\[Epsilon]\), \(.\)]\)|"},
  PlotLabel -> Style["\!\(\*OverscriptBox[\(\[Sigma]\), \(^\)]\) = 0 (converges to zero)", 12],
  ImageSize -> 500, AspectRatio -> 0.5,
  PlotLegends -> Placed[LineLegend[{"N=128","N=256","N=512"}], {Right,Top}]
];

bottomPlotF5 = ListLinePlot[
  Table[Transpose[{epsDotSigma13[[k,1]], epsDotSigma13[[k,2]]}], {k, 1, 3}],
  PlotStyle -> grayStyles,
  PlotRange -> {{xMinH, xMaxH}, All},
  Frame -> True,
  FrameLabel -> {"x", "|\!\(\*OverscriptBox[\(\[Epsilon]\), \(.\)]\)|"},
  PlotLabel -> Style["\!\(\*OverscriptBox[\(\[Sigma]\), \(^\)]\) = 1/3 (converges to nonzero)", 12],
  ImageSize -> 500, AspectRatio -> 0.5,
  PlotLegends -> Placed[LineLegend[{"N=128","N=256","N=512"}], {Right,Top}]
];

fig5 = Column[{topPlotF5, bottomPlotF5}, Spacings -> 1];
Export["output/fig5.pdf", fig5];
Print["  Exported output/fig5.pdf"];

(* ================================================================ *)
(*  FIG. 6: Telegrapher's equation transition                       *)
(* ================================================================ *)

Print["\n========================================"];
Print["  Fig. 6: Telegrapher's Equation"];
Print["========================================"];

(* Run sigma_hat=7.5 FIRST (fastest dynamics, most interesting) *)
sigmaHatVals = {7.5, 1.5, 0.15};
tauHatVals   = {75., 15., 1.5};
tSnapshots   = {16., 39., 312.};
(* Max evolution time per case to avoid hours-long runs *)
tMaxPerCase  = {312., 312., 50.};  (* sigma=0.15 barely changes, cap at t=50 *)

NxF6 = 256;
dxF6 = (xMaxH - xMinH)/NxF6;
xGridF6 = Table[xMinH + (i-0.5)*dxF6, {i, 1, NxF6}];
epsInitF6 = Table[N[epsFromTP[tInit[x], p0]], {x, xGridF6}];
vInitF6   = Table[0., {NxF6}];
nInitF6   = Table[N[nFromTP[tInit[x], p0]], {x, xGridF6}];

(* Diagnostic: print initial T range *)
Module[{tArr},
  tArr = Table[temperature[epsInitF6[[i]], nInitF6[[i]], gam, mass], {i, NxF6}];
  Print["  Initial T range: [", Min[tArr[[nGhost+1;;NxF6-nGhost]]],
        ", ", Max[tArr[[nGhost+1;;NxF6-nGhost]]], "]"];
];

(* Diagnostic: verify transport coefficients for each parameter set *)
Do[
  Module[{sH, tH, tcDiag, epsMid, nMid},
    sH = sigmaHatVals[[k]]; tH = tauHatVals[[k]];
    epsMid = epsInitF6[[NxF6/2]]; nMid = nInitF6[[NxF6/2]];
    tcDiag = transportCoeffs[epsMid, nMid, gam, mass, vHatF5, sH, tH];
    Print["  sigmaHat=", sH, ", tauHat=", tH,
          ": sigma=", tcDiag["sigma"],
          ", betaEps=", tcDiag["betaEps"],
          ", betaN=", tcDiag["betaN"],
          ", tauQ=", tcDiag["tauQ"]];
  ];
, {k, 1, 3}];

(* Store snapshots: allSnaps[[paramIdx, timeIdx]] = T(x) array *)
allSnaps = Table[{}, {3}, {3}];

Do[
  sH = sigmaHatVals[[k]]; tH = tauHatVals[[k]];
  Print["\n--- sigmaHat = ", sH, ", tauHat = ", tH, " ---"];

  state6 = applyBCAll[{N[epsInitF6], N[vInitF6], N[nInitF6],
                        Table[0., {NxF6}], Table[0., {NxF6}]}, nGhost];
  maxC6 = Max[Table[
    Module[{cs6},
      cs6 = charSpeeds[epsInitF6[[i]], nInitF6[[i]], gam, mass, vHatF5, sH, tH];
      cs6["cPlus"]
    ], {i, nGhost+1, NxF6-nGhost}]];
  maxC6 = Max[maxC6, 1.0];
  dt6 = 0.1*dxF6/maxC6;
  Print["  dt = ", dt6, ", max char speed = ", maxC6];

  t6 = 0.; step6 = 0;

  Do[
    tTarget = tSnapshots[[j]];
    (* Skip snapshots beyond the max time for this case *)
    If[tTarget > tMaxPerCase[[k]],
      Print["  Skipping t = ", tTarget, " (beyond tMax=", tMaxPerCase[[k]], ")"];
      (* Use the last available snapshot *)
      If[j > 1 && Length[allSnaps[[k, j-1]]] > 0,
        allSnaps[[k, j]] = allSnaps[[k, j-1]];
      ];
      Continue[];
    ];
    Print["  Evolving to t = ", tTarget, " ..."];
    While[t6 < tTarget - 1.0*^-10,
      dtStep = Min[dt6, tTarget - t6];
      state6 = heunStepH[state6, dtStep, dxF6, nGhost, gam, mass, vHatF5, sH, tH];
      t6 += dtStep; step6++;

      (* Print progress every 2000 steps *)
      If[Mod[step6, 2000] == 0,
        Print["    step ", step6, ", t = ", NumberForm[t6, {6,2}],
              ", max|v| = ", NumberForm[Max[Abs[state6[[2]]]], {5,4}]];
      ];

      If[stateHasNaN[state6],
        Print["    STOP: Overflow at t = ", t6];
        Goto[nextParam];
      ];
    ];

    tempArr = Table[
      temperature[state6[[1,i]], state6[[3,i]], gam, mass],
      {i, 1, NxF6}];
    allSnaps[[k, j]] = tempArr;
    Print["    T range: [",
      Min[tempArr[[nGhost+1;;NxF6-nGhost]]],
      ", ", Max[tempArr[[nGhost+1;;NxF6-nGhost]]], "]"];
    Print["    max|v| = ", Max[Abs[state6[[2, nGhost+1;;NxF6-nGhost]]]]];
    Print["    max|dtEps| = ", Max[Abs[state6[[4, nGhost+1;;NxF6-nGhost]]]]];
  , {j, 1, 3}];

  Label[nextParam];
, {k, 1, 3}];

(* --- Generate Fig. 6 --- *)
Print["\n--- Generating Fig. 6 ---"];

(* k=1: sigma=7.5 (darkest), k=2: sigma=1.5 (medium), k=3: sigma=0.15 (lightest) *)
grayLevels6 = {GrayLevel[0.0], GrayLevel[0.3], GrayLevel[0.6]};
panelLabels = {"t = 16", "t = 39", "t = 312"};

panels = Table[
  Module[{plotData},
    plotData = Table[
      If[Length[allSnaps[[k, j]]] > 0,
        Transpose[{xGridF6, allSnaps[[k, j]]}],
        {{0, delta}}
      ], {k, 1, 3}];
    ListLinePlot[plotData,
      PlotStyle -> Table[Directive[grayLevels6[[k]], AbsoluteThickness[1.5]], {k, 1, 3}],
      PlotRange -> {{xMinH, xMaxH}, {delta - 0.01, delta + ampA + 0.02}},
      Frame -> True, FrameLabel -> {"x", "T"},
      PlotLabel -> Style[panelLabels[[j]], 12],
      ImageSize -> 280, AspectRatio -> 0.7,
      PlotLegends -> If[j == 1,
        Placed[LineLegend[{
          "\!\(\*OverscriptBox[\(\[Sigma]\), \(^\)]\)=7.5",
          "\!\(\*OverscriptBox[\(\[Sigma]\), \(^\)]\)=1.5",
          "\!\(\*OverscriptBox[\(\[Sigma]\), \(^\)]\)=0.15"}, LegendMarkerSize -> 15], {Right,Top}],
        None]
    ]
  ],
  {j, 1, 3}
];

fig6 = GraphicsRow[panels, Spacings -> 0];
Export["output/fig6.pdf", fig6];
Print["  Exported output/fig6.pdf"];

Print["\n========================================"];
Print["  Heat Flow Complete"];
Print["========================================"];
