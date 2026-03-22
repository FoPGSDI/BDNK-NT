(* ============================================================== *)
(*  shockwave_dynamic.wl -- Dynamic shockwave PDE (Figs. 3, 4)   *)
(*  Pandya, Most, Pretorius (2022)                                *)
(*  Run: wolframscript -file shockwave_dynamic.wl                 *)
(*                                                                *)
(*  Approach: First-order reduction with NDSolve time integration *)
(*  State vector: U = {eps, v, n, p, q} per grid point            *)
(*    where p = dt(eps), q = dt(v)                                *)
(*  Spatial discretization: 2nd-order centered FD                 *)
(*  Time integration: NDSolve with ExplicitRungeKutta (RK4)       *)
(* ============================================================== *)

Print["========================================"];
Print["  Dynamic Shockwave PDE (Figs. 3, 4)"];
Print["  NDSolve-based solver"];
Print["========================================"];

SetDirectory[DirectoryName[$InputFileName]];
Get["bdnk_common.wl"];

If[!DirectoryQ["output"], CreateDirectory["output"]];

(* ================================================================ *)
(*  GLOBAL PARAMETERS                                               *)
(* ================================================================ *)

gam = 4/3;
mass = 0.1;

(* ================================================================ *)
(*  INITIAL DATA: Error-function profiles (paper Eq. 46)            *)
(* ================================================================ *)

makeInitialData[epsL_, vL_, nL_, epsR_, vR_, nR_, w_, xGrid_] := {
  Table[(epsR - epsL)/2*(Erf[x/w] + 1) + epsL, {x, xGrid}],
  Table[(vL - vR)/2*(1 - Erf[x/w]) + vR, {x, xGrid}],
  Table[(nL - nR)/2*(1 - Erf[x/w]) + nR, {x, xGrid}]
};

(* ================================================================ *)
(*  bdnkComponents: wrapper around bdnkTab                          *)
(*  Includes dtN in the projected gradient of n.                    *)
(*  Returns: {Ttt, Ttx, Txx, Jx}                                   *)
(* ================================================================ *)

bdnkComponents[epsV_, vV_, nV_, dxEpsV_, dxVV_, dxNV_,
               dtEpsV_, dtVV_, dtNV_,
               gamV_, massV_, vHatV_, sigmaHatV_, tauHatV_] :=
Module[{vc, tab, ttt, ttx, txx, jx, ww, ww2, tc, betaN0, corr},
  vc = Clip[vV, {-0.9999, 0.9999}];
  tab = bdnkTab[epsV, vc, nV, dtEpsV, dxEpsV, dtVV, dxVV, dxNV,
                gamV, massV, vHatV, sigmaHatV, tauHatV];
  ttt = tab["Ttt"]; ttx = tab["Ttx"]; txx = tab["Txx"]; jx = tab["Jx"];

  (* Add dtN correction to projected gradient of n:
     bdnkTab uses dxNProj = W^2*dxN (missing v*dtN term)
     Full: Delta^{xc}*nabla_c n = W^2*(v*dtN + dxN)
     Correction enters through scrQx: delta_scrQx = betaN * W^2 * v * dtN
     Then Ttt += 2*v*W * delta_scrQx, Ttx += W*(1+v^2)*delta_scrQx,
          Txx += 2*v*W * delta_scrQx *)
  ww = 1.0/Sqrt[1.0 - vc^2]; ww2 = 1.0/(1.0 - vc^2);
  tc = transportCoeffs[epsV, nV, gamV, massV, vHatV, sigmaHatV, tauHatV];
  betaN0 = tc["betaN"];
  corr = betaN0 * ww2 * vc * dtNV;  (* delta_scrQx *)
  ttt += 2*vc*ww * corr;
  ttx += ww*(1 + vc^2) * corr;
  txx += 2*vc*ww * corr;
  {ttt, ttx, txx, jx}
];

(* ================================================================ *)
(*  RHS COMPUTATION                                                 *)
(*  Uses forward finite differences for the Jacobian (9 calls per  *)
(*  grid point instead of 15 for central differences).              *)
(* ================================================================ *)

computeRHS[epsArr_List, vArr_List, nArr_List,
           pArr_List, qArr_List,
           dxVal_?NumericQ, nxVal_Integer,
           gamV_?NumericQ, massV_?NumericQ,
           vHatV_?NumericQ, sigmaHatV_?NumericQ,
           tauHatV_?NumericQ] :=
Module[{
  dxEps, dxV, dxN, dxP, dxQ,
  jxArr, dxJx, dtNArr, dxDtN,
  ttxArr, txxArr, dxTtx, dxTxx,
  rhsEps, rhsV, rhsN, rhsP, rhsQ,
  i, eps, v, n, pi, qi, vc, ww, dtNi,
  comp0, compA1, compA2,
  a11, a12, a21, a22,
  he, hv, hn, hdx,
  compP, dTttDeps, dTttDv, dTttDn, dTttDdxE, dTttDdxV, dTttDdxN,
  dTtxDeps, dTtxDv, dTtxDn, dTtxDdxE, dTtxDdxV, dTtxDdxN,
  rhsEn, rhsMom, det
},

  (* ---- 1. Spatial first derivatives ---- *)
  dxEps = Table[0., {nxVal}]; dxV = Table[0., {nxVal}]; dxN = Table[0., {nxVal}];
  dxP = Table[0., {nxVal}]; dxQ = Table[0., {nxVal}];
  Do[
    dxEps[[i]] = (epsArr[[i+1]] - epsArr[[i-1]])/(2.*dxVal);
    dxV[[i]]   = (vArr[[i+1]] - vArr[[i-1]])/(2.*dxVal);
    dxN[[i]]   = (nArr[[i+1]] - nArr[[i-1]])/(2.*dxVal);
    dxP[[i]]   = (pArr[[i+1]] - pArr[[i-1]])/(2.*dxVal);
    dxQ[[i]]   = (qArr[[i+1]] - qArr[[i-1]])/(2.*dxVal);
  , {i, 2, nxVal-1}];
  dxEps[[1]]=dxEps[[2]]; dxEps[[nxVal]]=dxEps[[nxVal-1]];
  dxV[[1]]=dxV[[2]]; dxV[[nxVal]]=dxV[[nxVal-1]];
  dxN[[1]]=dxN[[2]]; dxN[[nxVal]]=dxN[[nxVal-1]];
  dxP[[1]]=dxP[[2]]; dxP[[nxVal]]=dxP[[nxVal-1]];
  dxQ[[1]]=dxQ[[2]]; dxQ[[nxVal]]=dxQ[[nxVal-1]];

  (* ---- 2. dtN from baryon conservation ---- *)
  jxArr = Table[Module[{vc2, ww2},
    vc2 = Clip[vArr[[i]], {-0.9999, 0.9999}];
    ww2 = 1./Sqrt[1. - vc2^2]; nArr[[i]]*ww2*vc2], {i, nxVal}];
  dxJx = Table[0., {nxVal}];
  Do[dxJx[[i]] = (jxArr[[i+1]] - jxArr[[i-1]])/(2.*dxVal), {i, 2, nxVal-1}];
  dxJx[[1]]=dxJx[[2]]; dxJx[[nxVal]]=dxJx[[nxVal-1]];

  dtNArr = Table[Module[{vc2, ww2},
    vc2 = Clip[vArr[[i]], {-0.9999, 0.9999}];
    ww2 = 1./Sqrt[1. - vc2^2];
    (-dxJx[[i]] - nArr[[i]]*ww2^3*vc2*qArr[[i]])/ww2], {i, nxVal}];
  dxDtN = Table[0., {nxVal}];
  Do[dxDtN[[i]] = (dtNArr[[i+1]] - dtNArr[[i-1]])/(2.*dxVal), {i, 2, nxVal-1}];
  dxDtN[[1]]=dxDtN[[2]]; dxDtN[[nxVal]]=dxDtN[[nxVal-1]];

  (* ---- 3. Compute Ttx, Txx at each point ---- *)
  ttxArr = Table[0., {nxVal}]; txxArr = Table[0., {nxVal}];
  Do[Module[{comp},
    comp = bdnkComponents[epsArr[[i]], vArr[[i]], nArr[[i]],
             dxEps[[i]], dxV[[i]], dxN[[i]],
             pArr[[i]], qArr[[i]], dtNArr[[i]],
             gamV, massV, vHatV, sigmaHatV, tauHatV];
    ttxArr[[i]] = comp[[2]]; txxArr[[i]] = comp[[3]];
  ], {i, 1, nxVal}];

  (* ---- 4. Flux spatial derivatives ---- *)
  dxTtx = Table[0., {nxVal}]; dxTxx = Table[0., {nxVal}];
  Do[dxTtx[[i]] = (ttxArr[[i+1]] - ttxArr[[i-1]])/(2.*dxVal);
     dxTxx[[i]] = (txxArr[[i+1]] - txxArr[[i-1]])/(2.*dxVal);
  , {i, 2, nxVal-1}];
  dxTtx[[1]]=dxTtx[[2]]; dxTtx[[nxVal]]=dxTtx[[nxVal-1]];
  dxTxx[[1]]=dxTxx[[2]]; dxTxx[[nxVal]]=dxTxx[[nxVal-1]];

  (* ---- 5. Solve 2x2 system at each grid point ---- *)
  rhsEps = Table[0., {nxVal}]; rhsV = Table[0., {nxVal}]; rhsN = Table[0., {nxVal}];
  rhsP = Table[0., {nxVal}]; rhsQ = Table[0., {nxVal}];

  Do[
    eps = epsArr[[i]]; v = Clip[vArr[[i]], {-0.9999, 0.9999}]; n = nArr[[i]];
    pi = pArr[[i]]; qi = qArr[[i]]; dtNi = dtNArr[[i]];

    rhsEps[[i]] = pi; rhsV[[i]] = qi; rhsN[[i]] = dtNi;

    (* A-matrix from linearity in p, q *)
    comp0 = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                            0., 0., dtNi, gamV, massV, vHatV, sigmaHatV, tauHatV];
    compA1 = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                             1., 0., dtNi, gamV, massV, vHatV, sigmaHatV, tauHatV];
    compA2 = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                             0., 1., dtNi, gamV, massV, vHatV, sigmaHatV, tauHatV];
    a11 = compA1[[1]]-comp0[[1]]; a12 = compA2[[1]]-comp0[[1]];
    a21 = compA1[[2]]-comp0[[2]]; a22 = compA2[[2]]-comp0[[2]];

    (* Forward-difference Jacobian (using comp0 as base for p=q=0 case *)
    (* But comp0 is at (p=0,q=0), while we need derivatives at (p=pi,q=qi).
       Since Ttt is nonlinear in eps,v,n but linear in p,q,
       the derivatives w.r.t. eps,v,n etc. may depend on p,q.
       We use the current-state evaluation as base. *)
    he = Max[Abs[eps]*1.0*^-6, 1.0*^-9];
    compP = bdnkComponents[eps+he, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                            pi, qi, dtNi, gamV, massV, vHatV, sigmaHatV, tauHatV];
    (* We need the base at current p,q too *)
    Module[{compBase},
      compBase = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                                 pi, qi, dtNi, gamV, massV, vHatV, sigmaHatV, tauHatV];
      dTttDeps = (compP[[1]] - compBase[[1]])/he;
      dTtxDeps = (compP[[2]] - compBase[[2]])/he;

      hv = Max[Abs[v]*1.0*^-6, 1.0*^-9];
      compP = bdnkComponents[eps, Clip[v+hv,{-0.9999,0.9999}], n, dxEps[[i]], dxV[[i]], dxN[[i]],
                               pi, qi, dtNi, gamV, massV, vHatV, sigmaHatV, tauHatV];
      dTttDv = (compP[[1]] - compBase[[1]])/hv;
      dTtxDv = (compP[[2]] - compBase[[2]])/hv;

      hn = Max[Abs[n]*1.0*^-6, 1.0*^-9];
      compP = bdnkComponents[eps, v, n+hn, dxEps[[i]], dxV[[i]], dxN[[i]],
                               pi, qi, dtNi, gamV, massV, vHatV, sigmaHatV, tauHatV];
      dTttDn = (compP[[1]] - compBase[[1]])/hn;
      dTtxDn = (compP[[2]] - compBase[[2]])/hn;

      hdx = Max[Abs[dxEps[[i]]]*1.0*^-6, 1.0*^-9];
      compP = bdnkComponents[eps, v, n, dxEps[[i]]+hdx, dxV[[i]], dxN[[i]],
                               pi, qi, dtNi, gamV, massV, vHatV, sigmaHatV, tauHatV];
      dTttDdxE = (compP[[1]] - compBase[[1]])/hdx;
      dTtxDdxE = (compP[[2]] - compBase[[2]])/hdx;

      hdx = Max[Abs[dxV[[i]]]*1.0*^-6, 1.0*^-9];
      compP = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]]+hdx, dxN[[i]],
                               pi, qi, dtNi, gamV, massV, vHatV, sigmaHatV, tauHatV];
      dTttDdxV = (compP[[1]] - compBase[[1]])/hdx;
      dTtxDdxV = (compP[[2]] - compBase[[2]])/hdx;

      hdx = Max[Abs[dxN[[i]]]*1.0*^-6, 1.0*^-9];
      compP = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]]+hdx,
                               pi, qi, dtNi, gamV, massV, vHatV, sigmaHatV, tauHatV];
      dTttDdxN = (compP[[1]] - compBase[[1]])/hdx;
      dTtxDdxN = (compP[[2]] - compBase[[2]])/hdx;
    ];

    rhsEn = -dxTtx[[i]]
            - (dTttDeps*pi + dTttDv*qi + dTttDn*dtNi
               + dTttDdxE*dxP[[i]] + dTttDdxV*dxQ[[i]] + dTttDdxN*dxDtN[[i]]);
    rhsMom = -dxTxx[[i]]
             - (dTtxDeps*pi + dTtxDv*qi + dTtxDn*dtNi
                + dTtxDdxE*dxP[[i]] + dTtxDdxV*dxQ[[i]] + dTtxDdxN*dxDtN[[i]]);

    det = a11*a22 - a12*a21;
    If[Abs[det] < 1.0*^-30,
      rhsP[[i]] = 0.; rhsQ[[i]] = 0.;,
      rhsP[[i]] = (a22*rhsEn - a12*rhsMom)/det;
      rhsQ[[i]] = (a11*rhsMom - a21*rhsEn)/det;
    ];
  , {i, 1, nxVal}];

  {rhsEps, rhsV, rhsN, rhsP, rhsQ}
];

(* ================================================================ *)
(*  NDSolve EVOLUTION WRAPPER                                       *)
(* ================================================================ *)

evolveNDSolve[epsInit_, vInit_, nInit_, tFinal_,
              dxVal_, nxVal_, xGrid_,
              gamV_, massV_, vHatV_, sigmaHatV_, tauHatV_,
              maxStepFrac_:1/50] :=
Module[{y0, sol, gN, mN, vhN, shN, thN, dxN},

  gN  = N[gamV]; mN = N[massV]; vhN = N[vHatV];
  shN = N[sigmaHatV]; thN = N[tauHatV]; dxN = N[dxVal];

  Print["  Setting up NDSolve: ", nxVal, " grid pts x 5 vars = ", 5*nxVal, " ODEs"];
  Print["  Time domain: [0, ", tFinal, "], dx = ", dxN];

  rhsFnLocal[tVal_?NumericQ, sv_?(VectorQ[#, NumericQ]&)] :=
  Module[{ev, vv, nv, pv, qv, rhs},
    ev = Map[Max[#, 1.0*^-10]&, sv[[1 ;; nxVal]]];
    vv = Map[Clip[#, {-0.9999, 0.9999}]&, sv[[nxVal+1 ;; 2*nxVal]]];
    nv = Map[Max[#, 1.0*^-10]&, sv[[2*nxVal+1 ;; 3*nxVal]]];
    pv = sv[[3*nxVal+1 ;; 4*nxVal]];
    qv = sv[[4*nxVal+1 ;; 5*nxVal]];
    rhs = computeRHS[ev, vv, nv, pv, qv,
                      dxN, nxVal, gN, mN, vhN, shN, thN];
    Join[rhs[[1]], rhs[[2]], rhs[[3]], rhs[[4]], rhs[[5]]]
  ];

  y0 = Join[N[epsInit], N[vInit], N[nInit],
            Table[0., {nxVal}], Table[0., {nxVal}]];

  Print["  Calling NDSolve (ExplicitRungeKutta, order 4)..."];

  sol = Quiet[
    NDSolve[
      {y'[t] == rhsFnLocal[t, y[t]], y[0] == y0},
      y,
      {t, 0, tFinal},
      Method -> {"ExplicitRungeKutta", "DifferenceOrder" -> 4},
      MaxSteps -> Infinity,
      AccuracyGoal -> 4,
      PrecisionGoal -> 4,
      MaxStepFraction -> maxStepFrac,
      InterpolationOrder -> All
    ],
    {NDSolve::mxst, NDSolve::ndsz, NDSolve::ndtol, NDSolve::berr,
     NDSolve::nderr, Power::infy, Infinity::indet}
  ];

  Print["  NDSolve completed."];
  y /. First[sol]
];

(* ================================================================ *)
(*  Extract state at a given time from NDSolve solution             *)
(* ================================================================ *)

extractState[solFn_, tVal_, nxVal_] := Module[{sv, tUse, dom},
  dom = solFn["Domain"][[1]];
  tUse = Clip[tVal, {dom[[1]], dom[[2]]}];
  If[tUse < tVal - 0.01,
    Print["  WARNING: requested t=", tVal, " but solution ends at t=", dom[[2]]]];
  sv = solFn[tUse];
  {sv[[1 ;; nxVal]],
   sv[[nxVal+1 ;; 2*nxVal]],
   sv[[2*nxVal+1 ;; 3*nxVal]],
   sv[[3*nxVal+1 ;; 4*nxVal]],
   sv[[4*nxVal+1 ;; 5*nxVal]]}
];

(* ================================================================ *)
(*  FIG. 3: Dynamic shockwave stability                             *)
(* ================================================================ *)

Print["\n========================================"];
Print["  Fig. 3: Dynamic Shockwave Stability"];
Print["========================================"];

vHatF3 = 4/3;
sigmaHatF3 = 0;

epsLF3 = 1.0; vLF3 = 0.9; nLF3 = 1.0;
{epsRF3, vRF3, nRF3} = solveRankineHugoniot[epsLF3, vLF3, nLF3, gam, mass];
Print["Left state:  {", epsLF3, ", ", vLF3, ", ", nLF3, "}"];
Print["Right state: {", N[epsRF3], ", ", N[vRF3], ", ", N[nRF3], "}"];

w = 10.0;
xMinF3 = -50.; xMaxF3 = 50.;
NxF3 = 256;
dxF3 = (xMaxF3 - xMinF3)/NxF3;
xGridF3 = Table[xMinF3 + (i - 0.5)*dxF3, {i, 1, NxF3}];
{epsInitF3, vInitF3, nInitF3} = makeInitialData[epsLF3, vLF3, nLF3,
  epsRF3, vRF3, nRF3, w, xGridF3];

(* --- Top panel: tauHat = 3 (unstable, c+ < vL) --- *)
Print["\n--- tauHat = 3 (unstable, evolve to t=27) ---"];
csU = charSpeeds[epsLF3, nLF3, gam, mass, vHatF3, sigmaHatF3, 3];
Print["  c+ = ", N[csU["cPlus"]], " (vL=0.9 > c+: unstable)"];

solUnstable = evolveNDSolve[epsInitF3, vInitF3, nInitF3, 27.,
  dxF3, NxF3, xGridF3, gam, mass, vHatF3, sigmaHatF3, 3];

unstableSnapTimes = {0., 5., 10., 15., 20., 27.};
unstableSnaps = Table[
  {tSnap, Quiet[extractState[solUnstable, tSnap, NxF3]]},
  {tSnap, unstableSnapTimes}
];

(* --- Bottom panel: tauHat = 1.5 (stable, c+ > vL) --- *)
Print["\n--- tauHat = 1.5 (stable, evolve to t=372) ---"];
csS = charSpeeds[epsLF3, nLF3, gam, mass, vHatF3, sigmaHatF3, 1.5];
Print["  c+ = ", N[csS["cPlus"]], " (vL=0.9 < c+: stable)"];

solStable = evolveNDSolve[epsInitF3, vInitF3, nInitF3, 372.,
  dxF3, NxF3, xGridF3, gam, mass, vHatF3, sigmaHatF3, 1.5];

stateS = extractState[solStable, 372., NxF3];

(* --- Generate Fig. 3 --- *)
Print["\n--- Generating Fig. 3 ---"];

Module[{snapPlots, nSnaps, grayVals},
  nSnaps = Length[unstableSnaps];
  grayVals = Table[GrayLevel[0.7*(1 - (k-1)/Max[nSnaps-1, 1])], {k, nSnaps}];
  snapPlots = Table[
    ListLinePlot[Transpose[{xGridF3, unstableSnaps[[k, 2, 2]]}],
      PlotStyle -> Directive[grayVals[[k]], AbsoluteThickness[1.5]]],
    {k, nSnaps}];
  topPlotF3 = Show[
    snapPlots,
    PlotRange -> {{xMinF3, xMaxF3}, {0, 1.0}},
    Frame -> True, FrameLabel -> {"x", "v"},
    PlotLabel -> Style[Row[{"\!\(\*OverscriptBox[\(\[Tau]\), \(^\)]\) = 3 (unstable, v > ",
      Subscript["c","+"], ")"}], 12],
    ImageSize -> 500, AspectRatio -> 0.5,
    Epilog -> {Red, Dashed, AbsoluteThickness[1.5],
      Line[{{xMinF3, N[csU["cPlus"]]}, {xMaxF3, N[csU["cPlus"]]}}]}
  ];
];

bottomPlotF3 = ListLinePlot[
  Transpose[{xGridF3, stateS[[2]]}],
  PlotRange -> {{xMinF3, xMaxF3}, {0, 1.0}},
  PlotStyle -> Directive[Black, AbsoluteThickness[1.5]],
  Frame -> True, FrameLabel -> {"x", "v"},
  PlotLabel -> Style[Row[{"\!\(\*OverscriptBox[\(\[Tau]\), \(^\)]\) = 1.5, t = 372 (stable, v < ",
    Subscript["c","+"], ")"}], 12],
  ImageSize -> 500, AspectRatio -> 0.5,
  Epilog -> {Red, Dashed, AbsoluteThickness[1.5],
    Line[{{xMinF3, N[csS["cPlus"]]}, {xMaxF3, N[csS["cPlus"]]}}]}
];

fig3 = Column[{topPlotF3, bottomPlotF3}, Spacings -> 1];
Export["output/fig3.pdf", fig3];
Print["  Exported output/fig3.pdf"];

(* ================================================================ *)
(*  FIG. 4: Acausality / instability tests                          *)
(* ================================================================ *)

Print["\n========================================"];
Print["  Fig. 4: Acausality Tests"];
Print["========================================"];

epsLF4 = 1.0; vLF4 = 0.6; nLF4 = 1.0;
{epsRF4, vRF4, nRF4} = solveRankineHugoniot[epsLF4, vLF4, nLF4, gam, mass];
Print["Left state:  {", epsLF4, ", ", vLF4, ", ", nLF4, "}"];
Print["Right state: {", N[epsRF4], ", ", N[vRF4], ", ", N[nRF4], "}"];

xMinF4 = -100.; xMaxF4 = 100.;
NxF4 = 128;
dxF4 = (xMaxF4 - xMinF4)/NxF4;
xGridF4 = Table[xMinF4 + (i - 0.5)*dxF4, {i, 1, NxF4}];
{epsInitF4, vInitF4, nInitF4} = makeInitialData[epsLF4, vLF4, nLF4,
  epsRF4, vRF4, nRF4, w, xGridF4];

(* --- tauHat = 1.5 (stable reference) --- *)
Print["\n--- tauHat = 1.5, evolve to t=1582 ---"];
cs15 = charSpeeds[epsLF4, nLF4, gam, mass, vHatF3, sigmaHatF3, 1.5];
Print["  tauHat = 1.5: c+ = ", N[cs15["cPlus"]]];

solF4stable = evolveNDSolve[epsInitF4, vInitF4, nInitF4, 1582.,
  dxF4, NxF4, xGridF4, gam, mass, vHatF3, sigmaHatF3, 1.5];

(* --- tauHat = 0.5 (weakly superluminal) --- *)
Print["\n--- tauHat = 0.5, evolve to t=1582 ---"];
cs05 = charSpeeds[epsLF4, nLF4, gam, mass, vHatF3, sigmaHatF3, 0.5];
Print["  tauHat = 0.5: c+ = ", N[cs05["cPlus"]]];

solF4superlum = evolveNDSolve[epsInitF4, vInitF4, nInitF4, 1582.,
  dxF4, NxF4, xGridF4, gam, mass, vHatF3, sigmaHatF3, 0.5];

(* --- tauHat = 0.25 (wildly superluminal) --- *)
Print["\n--- tauHat = 0.25 ---"];
cs025 = charSpeeds[epsLF4, nLF4, gam, mass, vHatF3, sigmaHatF3, 0.25];
Print["  tauHat = 0.25: c+ = ", N[cs025["cPlus"]], " (wildly superluminal)"];

solF4wild = evolveNDSolve[epsInitF4, vInitF4, nInitF4, 0.36,
  dxF4, NxF4, xGridF4, gam, mass, vHatF3, sigmaHatF3, 0.25, 1/200];

(* --- Generate Fig. 4 --- *)
Print["\n--- Generating Fig. 4 ---"];

stateF4stable   = extractState[solF4stable, 1582., NxF4];
stateF4superlum = extractState[solF4superlum, 1582., NxF4];

topPlotF4 = Show[
  ListLinePlot[Transpose[{xGridF4, vInitF4}],
    PlotStyle -> Directive[Gray, Dotted, AbsoluteThickness[1]]],
  ListLinePlot[Transpose[{xGridF4, stateF4stable[[2]]}],
    PlotStyle -> Directive[Black, AbsoluteThickness[1.5]]],
  ListLinePlot[Transpose[{xGridF4, stateF4superlum[[2]]}],
    PlotStyle -> Directive[GrayLevel[0.4], Dashed, AbsoluteThickness[1.5]]],
  PlotRange -> {{xMinF4, xMaxF4}, {0.45, 0.65}},
  Frame -> True, FrameLabel -> {"x", "v"},
  PlotLabel -> Style["t = 0 (dotted), t = 1582 (solid)", 12],
  ImageSize -> 500, AspectRatio -> 0.5
];

earlyTimes = {0.27, 0.31, 0.36};
bottomStyles = {
  Directive[GrayLevel[0.4], Dotted, AbsoluteThickness[1.5]],
  Directive[GrayLevel[0.2], Dashing[{0.02,0.01,0.005,0.01}], AbsoluteThickness[1.5]],
  Directive[Black, AbsoluteThickness[1.5]]
};

bottomSnaps025 = Table[
  Quiet[extractState[solF4wild, tSnap, NxF4]],
  {tSnap, earlyTimes}
];

nBottom = Length[bottomSnaps025];
bottomPlotF4 = Show[
  Table[ListLinePlot[Transpose[{xGridF4, bottomSnaps025[[k, 2]]}],
    PlotStyle -> bottomStyles[[k]]], {k, 1, nBottom}],
  PlotRange -> {{xMinF4, xMaxF4}, All},
  Frame -> True, FrameLabel -> {"x", "v"},
  PlotLabel -> Style[Row[{"\!\(\*OverscriptBox[\(\[Tau]\), \(^\)]\) = 0.25 (wildly superluminal)"}], 12],
  ImageSize -> 500, AspectRatio -> 0.5
];

fig4 = Column[{topPlotF4, bottomPlotF4}, Spacings -> 1];
Export["output/fig4.pdf", fig4];
Print["  Exported output/fig4.pdf"];

Print["\n========================================"];
Print["  Dynamic Shockwave Complete"];
Print["========================================"];
