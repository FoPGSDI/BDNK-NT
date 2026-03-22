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
p0 = 1/3;

tInit[x_] := ampA*Exp[-x^2/wHeat^2] + delta;
epsFromTP[t_, p_] := p*(mass/t + 1/(gam - 1));
nFromTP[t_, p_] := p/t;

Print["\nInitial data parameters:"];
Print["  A=", ampA, ", delta=", delta, ", w=", wHeat, ", P0=", N[p0]];

(* ---- BDNK components computation (same as shockwave_dynamic) ---- *)
bdnkComponents[eps_, v_, n_, dxEps_, dxV_, dxN_, dtEps_, dtV_,
               gam_, mass_, vHat_, sigmaHat_, tauHat_] :=
Module[{pp, rr, cs2, ww, ww2, tc,
        tauEps, tauP, tauQ, vVisc, sig, betaE, betaN0, eta0,
        divU, udotEps, uDotUx, dxEpsProj, dxNProj,
        scrE, scrP, scrQx, sigXX,
        ttt, ttx, txx, jx},

  pp  = (gam - 1)*(eps - mass*n);
  rr  = eps + pp;
  cs2 = gam*pp/rr;
  ww  = 1.0/Sqrt[1.0 - v^2];
  ww2 = 1.0/(1.0 - v^2);

  tc = transportCoeffs[eps, n, gam, mass, vHat, sigmaHat, tauHat];
  tauEps = tc["tauEps"]; tauP = tc["tauP"]; tauQ = tc["tauQ"];
  vVisc = tc["V"]; sig = tc["sigma"]; betaE = tc["betaEps"];
  betaN0 = tc["betaN"]; eta0 = 3.0*vVisc/4.0;

  divU     = ww^3*(v*dtV + dxV);
  udotEps  = ww*(dtEps + v*dxEps);
  uDotUx   = ww^4*(dtV + v*dxV);
  dxEpsProj = ww2*(v*dtEps + dxEps);
  dxNProj   = ww2*dxN;

  scrE  = eps + tauEps*(udotEps + rr*divU);
  scrP  = pp + tauP*(udotEps + rr*divU);
  scrQx = tauQ*rr*uDotUx + betaE*dxEpsProj + betaN0*dxNProj;
  sigXX = (2.0/3.0)*ww2*divU;

  ttt = scrE*ww2 + scrP*ww2*v^2 + 2*v*scrQx*ww - 2*eta0*v^2*sigXX;
  ttx = (scrE + scrP)*ww2*v + scrQx*ww*(1 + v^2) - 2*eta0*v*sigXX;
  txx = scrE*ww2*v^2 + scrP*ww2 + 2*scrQx*ww*v - 2*eta0*sigXX;
  jx  = n*ww*v;

  {ttt, ttx, txx, jx}
];

(* ---- RHS computation ---- *)
computeRHS[epsArr_, vArr_, nArr_, dtEpsArr_, dtVArr_,
           dx_, gam_, mass_, vHat_, sigmaHat_, tauHat_] :=
Module[{nx, dxEps, dxV, dxN,
        ttxArr, txxArr, jxArr,
        dxTtx, dxTxx, dxJx,
        ddotEps, ddotV, dtNArr, i, eps, v, n, ww},

  nx = Length[epsArr];

  dxEps = Table[0., {nx}]; dxV = Table[0., {nx}]; dxN = Table[0., {nx}];
  Do[
    dxEps[[i]] = (epsArr[[i+1]] - epsArr[[i-1]])/(2*dx);
    dxV[[i]]   = (vArr[[i+1]] - vArr[[i-1]])/(2*dx);
    dxN[[i]]   = (nArr[[i+1]] - nArr[[i-1]])/(2*dx);
  , {i, 2, nx-1}];
  dxEps[[1]] = dxEps[[2]]; dxEps[[nx]] = dxEps[[nx-1]];
  dxV[[1]] = dxV[[2]]; dxV[[nx]] = dxV[[nx-1]];
  dxN[[1]] = dxN[[2]]; dxN[[nx]] = dxN[[nx-1]];

  ttxArr = Table[0., {nx}]; txxArr = Table[0., {nx}]; jxArr = Table[0., {nx}];
  Do[
    Module[{comp},
      comp = bdnkComponents[epsArr[[i]], vArr[[i]], nArr[[i]],
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
    eps = epsArr[[i]]; v = vArr[[i]]; n = nArr[[i]];
    ww = 1.0/Sqrt[1.0 - v^2];

    Module[{comp0, compE, compV, compN,
            ttt0, ttx0, a11, a12, a21, a22,
            he, hv, hn,
            dTttDeps, dTtxDeps, dTttDv, dTtxDv, dTttDn, dTtxDn,
            dtNi, rhsEn, rhsMom, det},

      comp0 = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]],
                              gam, mass, vHat, sigmaHat, tauHat];
      ttt0 = comp0[[1]]; ttx0 = comp0[[2]];

      compE = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]]+1, dtVArr[[i]],
                              gam, mass, vHat, sigmaHat, tauHat];
      a11 = compE[[1]] - ttt0; a21 = compE[[2]] - ttx0;

      compV = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]]+1,
                              gam, mass, vHat, sigmaHat, tauHat];
      a12 = compV[[1]] - ttt0; a22 = compV[[2]] - ttx0;

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

      dtNi = (-dxJx[[i]] - n*ww^3*v*dtVArr[[i]])/ww;

      rhsEn  = -dxTtx[[i]] - (dTttDeps*dtEpsArr[[i]] + dTttDv*dtVArr[[i]] + dTttDn*dtNi);
      rhsMom = -dxTxx[[i]] - (dTtxDeps*dtEpsArr[[i]] + dTtxDv*dtVArr[[i]] + dTtxDn*dtNi);

      det = a11*a22 - a12*a21;
      If[Abs[det] < 1.0*^-30,
        ddotEps[[i]] = 0.; ddotV[[i]] = 0.;,
        ddotEps[[i]] = (a22*rhsEn - a12*rhsMom)/det;
        ddotV[[i]]   = (a11*rhsMom - a21*rhsEn)/det;
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
  sStar[[2]] = Clip[sStar[[2]], {-0.9999, 0.9999}];
  sStar[[3]] = Map[Max[#, 1.0*^-10]&, sStar[[3]]];
  sStar = applyBCAll[sStar, ng];

  rhs2 = computeRHS[sStar[[1]], sStar[[2]], sStar[[3]], sStar[[4]], sStar[[5]],
                     dx, gam, mass, vHat, sigmaHat, tauHat];
  sNew = Table[0.5*s0[[k]] + 0.5*(sStar[[k]] + dt*rhs2[[k]]), {k, 5}];
  sNew[[2]] = Clip[sNew[[2]], {-0.9999, 0.9999}];
  sNew[[3]] = Map[Max[#, 1.0*^-10]&, sNew[[3]]];
  applyBCAll[sNew, ng]
];

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
  Print["  dt = ", dt, ", dx = ", dx];

  t = 0.; step = 0;
  While[t < tFinal,
    If[t + dt > tFinal, dt = tFinal - t];
    state = heunStepH[state, dt, dx, nGhost, gam, mass, vHat, sigmaHat, tauHat];
    t += dt; step++;
    If[Mod[step, printInterval] == 0,
      Print["    step ", step, ", t = ", NumberForm[t, {6,2}]];
    ];
    If[AnyTrue[Flatten[{state[[1]], state[[2]]}],
               (!NumberQ[#] || Abs[#] > 1.0*^10)&],
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
  epsI = Table[epsFromTP[tInit[x], p0], {x, xGridH}];
  vI   = Table[0., {nxVal}];
  nI   = Table[nFromTP[tInit[x], p0], {x, xGridH}];

  dtSmall = 0.01;
  stH = evolveHeat[epsI, vI, nI, dtSmall,
    dxH, 0.1, gam, mass, vHatF5, 0, tauHatF5, 10000];
  edArr = (stH[[1]] - epsI)/dtSmall;
  AppendTo[epsDotSigma0, {xGridH, Abs[edArr]}];
, {nxVal, nxValues}];

(* --- Bottom panel: sigmaHat = 1/3 --- *)
Print["\n--- sigmaHat = 1/3 (dynamical) ---"];

epsDotSigma13 = {};
Do[
  Print["  Nx = ", nxVal];
  dxH = (xMaxH - xMinH)/nxVal;
  xGridH = Table[xMinH + (i-0.5)*dxH, {i, 1, nxVal}];
  epsI = Table[epsFromTP[tInit[x], p0], {x, xGridH}];
  vI   = Table[0., {nxVal}];
  nI   = Table[nFromTP[tInit[x], p0], {x, xGridH}];

  dtSmall = 0.01;
  stH = evolveHeat[epsI, vI, nI, dtSmall,
    dxH, 0.1, gam, mass, vHatF5, 1/3, tauHatF5, 10000];
  edArr = (stH[[1]] - epsI)/dtSmall;
  AppendTo[epsDotSigma13, {xGridH, Abs[edArr]}];
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

sigmaHatVals = {0.15, 1.5, 7.5};
tauHatVals   = {1.5, 15., 75.};
tSnapshots   = {16., 39., 312.};

NxF6 = 256;
dxF6 = (xMaxH - xMinH)/NxF6;
xGridF6 = Table[xMinH + (i-0.5)*dxF6, {i, 1, NxF6}];
epsInitF6 = Table[epsFromTP[tInit[x], p0], {x, xGridF6}];
vInitF6   = Table[0., {NxF6}];
nInitF6   = Table[nFromTP[tInit[x], p0], {x, xGridF6}];

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
  Print["  dt = ", dt6];

  t6 = 0.; step6 = 0;

  Do[
    tTarget = tSnapshots[[j]];
    Print["  Evolving to t = ", tTarget, " ..."];
    While[t6 < tTarget - 1.0*^-10,
      dtStep = Min[dt6, tTarget - t6];
      state6 = heunStepH[state6, dtStep, dxF6, nGhost, gam, mass, vHatF5, sH, tH];
      t6 += dtStep; step6++;
      If[AnyTrue[Flatten[{state6[[1]], state6[[2]]}],
                 (!NumberQ[#] || Abs[#] > 1.0*^10)&],
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
  , {j, 1, 3}];

  Label[nextParam];
, {k, 1, 3}];

(* --- Generate Fig. 6 --- *)
Print["\n--- Generating Fig. 6 ---"];

grayLevels6 = {GrayLevel[0.6], GrayLevel[0.3], GrayLevel[0.0]};
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
          "\!\(\*OverscriptBox[\(\[Sigma]\), \(^\)]\)=0.15",
          "\!\(\*OverscriptBox[\(\[Sigma]\), \(^\)]\)=1.5",
          "\!\(\*OverscriptBox[\(\[Sigma]\), \(^\)]\)=7.5"}, LegendMarkerSize -> 15], {Right,Top}],
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
