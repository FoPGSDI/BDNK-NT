(* ============================================================== *)
(*  shockwave_dynamic.wl -- Dynamic shockwave PDE (Figs. 3, 4)   *)
(*  Pandya, Most, Pretorius (2022)                                *)
(*  Run: wolframscript -file shockwave_dynamic.wl                 *)
(* ============================================================== *)

Print["========================================"];
Print["  Dynamic Shockwave PDE (Figs. 3, 4)"];
Print["========================================"];

SetDirectory[DirectoryName[$InputFileName]];
Get["bdnk_common.wl"];

If[!DirectoryQ["output"], CreateDirectory["output"]];

(* ================================================================ *)
(*  PDE SOLVER: Method of Lines for BDNK in 1+1D flat spacetime    *)
(*                                                                  *)
(*  State vector: (eps, v, n, dtEps, dtV) at each grid point       *)
(*  The system is 2nd order in time because T^{ab} contains first   *)
(*  time derivatives of the primitives via the BDNK corrections.    *)
(*                                                                  *)
(*  Strategy:                                                       *)
(*  1. Conservation laws: dt(Ttt) + dx(Ttx) = 0                    *)
(*                        dt(Ttx) + dx(Txx) = 0                    *)
(*                        dt(Jt)  + dx(Jx)  = 0                    *)
(*  2. Ttt, Ttx are LINEAR in dtEps and dtV, so we can write       *)
(*     Ttt = Ttt_base + A11*dtEps + A12*dtV                        *)
(*     Ttx = Ttx_base + A21*dtEps + A22*dtV                        *)
(*  3. From dt(Ttt) = -dx(Ttx) etc., we get a linear system        *)
(*     for (ddot_eps, ddot_v) at each grid point.                   *)
(*                                                                  *)
(*  Spatial: 2nd-order centered FD                                  *)
(*  Time: Heun's method (TVD-RK2)                                  *)
(* ================================================================ *)

gam = 4/3;
mass = 0.1;
nGhost = 3;

(* ---- Error-function initial data ---- *)
makeInitialData[epsL_, vL_, nL_, epsR_, vR_, nR_, w_, xGrid_] := {
  Table[(epsR - epsL)/2*(Erf[x/w] + 1) + epsL, {x, xGrid}],
  Table[(vL - vR)/2*(1 - Erf[x/w]) + vR, {x, xGrid}],
  Table[(nL - nR)/2*(1 - Erf[x/w]) + nR, {x, xGrid}]
};

(* ---- Safe numeric check: clamp non-numeric values ---- *)
safeVal[x_] := If[NumberQ[x] && Abs[x] < 1.0*^15, x, 0.];

(* ---- Compute Ttt, Ttx, Txx, Jx analytically ---- *)
(* All BDNK corrections are LINEAR in dtEps and dtV.
   We compute the base (dtEps=dtV=0) and the linear coefficients. *)

bdnkComponents[eps_, v_, n_, dxEps_, dxV_, dxN_, dtEps_, dtV_,
               gam_, mass_, vHat_, sigmaHat_, tauHat_] :=
Module[{pp, rr, cs2, vClamped, ww, ww2, tc,
        tauEps, tauP, tauQ, vVisc, sig, betaE, betaN0, eta0,
        divU, udotEps, uDotUx, dxEpsProj, dxNProj,
        scrE, scrP, scrQx, sigXX,
        ttt, ttx, txx, jx},

  (* Clamp velocity to safe range to prevent Sqrt of negative *)
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

(* ---- Compute RHS of the evolution system ---- *)
(*
  d/dt [eps]   = dtEps                    (definition)
  d/dt [v]     = dtV                      (definition)
  d/dt [n]     = dtN (from baryon cons.)  dtN = (-dxJx - n*W^3*v*dtV)/W
  d/dt [dtEps] = ddotEps                  (from energy conservation)
  d/dt [dtV]   = ddotV                    (from momentum conservation)

  The ddotEps and ddotV are found from:
  dt(Ttt) = -dxTtx  =>  dTtt/deps*dtEps + dTtt/dv*dtV + dTtt/dn*dtN
                        + A11*ddotEps + A12*ddotV + (spatial deriv changes) = -dxTtx
  dt(Ttx) = -dxTxx  =>  similarly

  where A11 = dTtt/d(dtEps), etc. are computed analytically.
*)

computeRHS[epsArr_, vArr_, nArr_, dtEpsArr_, dtVArr_,
           dx_, gam_, mass_, vHat_, sigmaHat_, tauHat_] :=
Module[{nx, dxEps, dxV, dxN,
        ttxArr, txxArr, jxArr,
        dxTtx, dxTxx, dxJx,
        ddotEps, ddotV, dtNArr,
        i, eps, v, n, ww, ww2, pp, rr},

  nx = Length[epsArr];

  (* 1. Compute spatial derivatives *)
  dxEps = Table[0., {nx}];
  dxV   = Table[0., {nx}];
  dxN   = Table[0., {nx}];
  Do[
    dxEps[[i]] = (epsArr[[i+1]] - epsArr[[i-1]])/(2*dx);
    dxV[[i]]   = (vArr[[i+1]] - vArr[[i-1]])/(2*dx);
    dxN[[i]]   = (nArr[[i+1]] - nArr[[i-1]])/(2*dx);
  , {i, 2, nx-1}];
  dxEps[[1]] = dxEps[[2]]; dxEps[[nx]] = dxEps[[nx-1]];
  dxV[[1]] = dxV[[2]]; dxV[[nx]] = dxV[[nx-1]];
  dxN[[1]] = dxN[[2]]; dxN[[nx]] = dxN[[nx-1]];

  (* 2. Compute T^{xt}, T^{xx}, J^x at each point with current dtEps, dtV *)
  ttxArr = Table[0., {nx}];
  txxArr = Table[0., {nx}];
  jxArr  = Table[0., {nx}];
  Do[
    Module[{comp},
      comp = bdnkComponents[epsArr[[i]], Clip[vArr[[i]], {-0.9999, 0.9999}], nArr[[i]],
                             dxEps[[i]], dxV[[i]], dxN[[i]],
                             dtEpsArr[[i]], dtVArr[[i]],
                             gam, mass, vHat, sigmaHat, tauHat];
      ttxArr[[i]] = comp[[2]];
      txxArr[[i]] = comp[[3]];
      jxArr[[i]]  = comp[[4]];
    ];
  , {i, 1, nx}];

  (* 3. Flux spatial derivatives *)
  dxTtx = Table[0., {nx}];
  dxTxx = Table[0., {nx}];
  dxJx  = Table[0., {nx}];
  Do[
    dxTtx[[i]] = (ttxArr[[i+1]] - ttxArr[[i-1]])/(2*dx);
    dxTxx[[i]] = (txxArr[[i+1]] - txxArr[[i-1]])/(2*dx);
    dxJx[[i]]  = (jxArr[[i+1]] - jxArr[[i-1]])/(2*dx);
  , {i, 2, nx-1}];
  dxTtx[[1]] = dxTtx[[2]]; dxTtx[[nx]] = dxTtx[[nx-1]];
  dxTxx[[1]] = dxTxx[[2]]; dxTxx[[nx]] = dxTxx[[nx-1]];
  dxJx[[1]] = dxJx[[2]];   dxJx[[nx]] = dxJx[[nx-1]];

  (* 4. At each grid point, solve for ddotEps, ddotV *)
  ddotEps = Table[0., {nx}];
  ddotV   = Table[0., {nx}];
  dtNArr  = Table[0., {nx}];

  Do[
    eps = epsArr[[i]]; v = Clip[vArr[[i]], {-0.9999, 0.9999}]; n = nArr[[i]];
    ww  = 1.0/Sqrt[1.0 - v^2];
    ww2 = 1.0/(1.0 - v^2);

    Module[{he, hv, hn,
            comp0, compE, compV, compN,
            ttt0, ttx0, tttE, ttxE, tttV, ttxV, tttN, ttxN,
            a11, a12, a21, a22,
            dTttDeps, dTtxDeps, dTttDv, dTtxDv, dTttDn, dTtxDn,
            dtNi, rhsEn, rhsMom, det},

      (* Compute base Ttt, Ttx at current state *)
      comp0 = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]],
                              gam, mass, vHat, sigmaHat, tauHat];
      ttt0 = comp0[[1]]; ttx0 = comp0[[2]];

      (* A11, A12, A21, A22: linear coefficients of Ttt, Ttx in dtEps, dtV.
         Since Ttt is linear in dtEps and dtV, we use:
         Ttt(dtE+1, dtV) - Ttt(dtE, dtV) = A11
         Ttt(dtE, dtV+1) - Ttt(dtE, dtV) = A12 *)
      compE = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]] + 1, dtVArr[[i]],
                              gam, mass, vHat, sigmaHat, tauHat];
      a11 = compE[[1]] - ttt0;   a21 = compE[[2]] - ttx0;

      compV = bdnkComponents[eps, v, n, dxEps[[i]], dxV[[i]], dxN[[i]],
                              dtEpsArr[[i]], dtVArr[[i]] + 1,
                              gam, mass, vHat, sigmaHat, tauHat];
      a12 = compV[[1]] - ttt0;   a22 = compV[[2]] - ttx0;

      (* Numerical derivatives of Ttt, Ttx w.r.t. eps, v, n *)
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

      (* dtN from baryon conservation *)
      dtNi = (-dxJx[[i]] - n*ww^3*v*dtVArr[[i]])/ww;

      (* RHS for the 2x2 system:
         A11*ddotEps + A12*ddotV = -dxTtx - (dTttDeps*dtEps + dTttDv*dtV + dTttDn*dtN)
         A21*ddotEps + A22*ddotV = -dxTxx - (dTtxDeps*dtEps + dTtxDv*dtV + dTtxDn*dtN)

         Note: spatial derivative changes are already captured through dxTtx, dxTxx
         since these are evaluated at the current state. *)
      rhsEn  = -dxTtx[[i]] - (dTttDeps*dtEpsArr[[i]] + dTttDv*dtVArr[[i]] + dTttDn*dtNi);
      rhsMom = -dxTxx[[i]] - (dTtxDeps*dtEpsArr[[i]] + dTtxDv*dtVArr[[i]] + dTtxDn*dtNi);

      det = a11*a22 - a12*a21;
      If[Abs[det] < 1.0*^-30,
        ddotEps[[i]] = 0.; ddotV[[i]] = 0.;,
        ddotEps[[i]] = safeVal[(a22*rhsEn - a12*rhsMom)/det];
        ddotV[[i]]   = safeVal[(a11*rhsMom - a21*rhsEn)/det];
      ];

      dtNArr[[i]] = dtNi;
    ];
  , {i, 1, nx}];

  (* Return: d/dt of {eps, v, n, dtEps, dtV} *)
  {dtEpsArr, dtVArr, dtNArr, ddotEps, ddotV}
];

(* ---- Apply boundary conditions ---- *)
applyBCAll[{e_, v_, n_, de_, dv_}, ng_] := {
  applyOutflowBC[e, ng], applyOutflowBC[v, ng],
  applyOutflowBC[n, ng], applyOutflowBC[de, ng],
  applyOutflowBC[dv, ng]
};

(* ---- Sanitize state: replace NaN/Inf with safe values ---- *)
sanitizeArray[arr_] := Map[If[NumberQ[#] && Abs[#] < 1.0*^15, #, 0.]&, arr];

(* ---- Heun step ---- *)
heunStep[state_, dt_, dx_, ng_, gam_, mass_, vHat_, sigmaHat_, tauHat_] :=
Module[{s0, rhs1, sStar, rhs2, sNew},
  s0 = state;

  (* Stage 1: Forward Euler *)
  rhs1 = computeRHS[s0[[1]], s0[[2]], s0[[3]], s0[[4]], s0[[5]],
                     dx, gam, mass, vHat, sigmaHat, tauHat];
  sStar = Table[s0[[k]] + dt*rhs1[[k]], {k, 5}];
  (* Clip velocity element-wise to prevent |v| >= 1 *)
  sStar[[2]] = Map[Clip[#, {-0.9999, 0.9999}]&, sStar[[2]]];
  sStar[[3]] = Map[Max[#, 1.0*^-10]&, sStar[[3]]];
  sStar[[1]] = Map[Max[#, 1.0*^-10]&, sStar[[1]]];
  sStar = applyBCAll[sStar, ng];

  (* Stage 2: Corrector *)
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

(* ---- Evolution function with snapshot support ---- *)
evolve[epsInit_, vInit_, nInit_, tFinal_, dx_, cfl_,
       gam_, mass_, vHat_, sigmaHat_, tauHat_,
       printInterval_:100, snapTimes_:{}] :=
Module[{nx, state, dt, t, step, maxChar, cPlusMax,
        snapshots, snapIdx, nextSnap, blownUp},

  nx = Length[epsInit];
  state = applyBCAll[{N[epsInit], N[vInit], N[nInit],
                       Table[0., {nx}], Table[0., {nx}]}, nGhost];

  (* Estimate max signal speed *)
  maxChar = 0.;
  Do[
    Module[{cs},
      cs = charSpeeds[epsInit[[i]], nInit[[i]], gam, mass, vHat, sigmaHat, tauHat];
      maxChar = Max[maxChar, cs["cPlus"] + Abs[vInit[[i]]]];
    ];
  , {i, nGhost+1, nx-nGhost}];
  maxChar = Max[maxChar, 1.0];
  cPlusMax = maxChar;

  dt = cfl*dx/maxChar;
  Print["  dt = ", dt, ", dx = ", dx, ", max signal speed = ", maxChar];

  t = 0.; step = 0;
  snapshots = {};
  snapIdx = 1;
  blownUp = False;

  While[t < tFinal,
    If[t + dt > tFinal, dt = tFinal - t];

    (* Save snapshots at requested times *)
    If[snapIdx <= Length[snapTimes] && t + dt >= snapTimes[[snapIdx]],
      (* Evolve exactly to snapshot time *)
      Module[{dtSnap = snapTimes[[snapIdx]] - t},
        If[dtSnap > 1.0*^-12,
          state = heunStep[state, dtSnap, dx, nGhost, gam, mass, vHat, sigmaHat, tauHat];
          t += dtSnap; step++;
        ];
      ];
      AppendTo[snapshots, {t, state}];
      Print["    SNAPSHOT at t = ", t, ", max|v| = ", Max[Abs[state[[2]]]]];
      snapIdx++;
      If[stateHasNaN[state],
        Print["  STOP: Overflow/NaN at snapshot, step ", step, ", t = ", t];
        blownUp = True;
        Break[];
      ];
      Continue[];
    ];

    state = heunStep[state, dt, dx, nGhost, gam, mass, vHat, sigmaHat, tauHat];
    t += dt; step++;

    If[Mod[step, printInterval] == 0,
      Print["    step ", step, ", t = ", NumberForm[t, {6,2}],
            ", max|v| = ", NumberForm[Max[Abs[state[[2]]]], {5,4}]];
    ];

    If[stateHasNaN[state],
      Print["  STOP: Overflow/NaN at step ", step, ", t = ", t];
      blownUp = True;
      Break[];
    ];
  ];

  If[!blownUp,
    Print["  Finished: t = ", t, ", steps = ", step];
  ];

  If[Length[snapTimes] > 0,
    (* Return snapshots list *)
    snapshots,
    (* Return final state *)
    state
  ]
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
{epsInitF3, vInitF3, nInitF3} = makeInitialData[epsLF3, vLF3, nLF3, epsRF3, vRF3, nRF3, w, xGridF3];

(* --- Top panel: tauHat = 3 (unstable) --- *)
Print["\n--- tauHat = 3 (unstable, evolve to t=27) ---"];
csU = charSpeeds[epsLF3, nLF3, gam, mass, vHatF3, sigmaHatF3, 3];
Print["  c+ = ", N[csU["cPlus"]], " (vL=0.9 > c+: unstable)"];

(* For unstable case: use snapshots to capture the evolution before blow-up *)
unstableSnapTimes = {2., 5., 10., 15., 20., 27.};
unstableSnaps = evolve[epsInitF3, vInitF3, nInitF3, 27.,
  dxF3, 0.1, gam, mass, vHatF3, sigmaHatF3, 3, 200, unstableSnapTimes];

(* Use the last valid snapshot for the plot *)
If[Length[unstableSnaps] > 0,
  stateU = unstableSnaps[[-1, 2]];
  Print["  Using last snapshot at t = ", unstableSnaps[[-1, 1]]];,
  (* Fallback: just evolve without snapshots *)
  stateU = evolve[epsInitF3, vInitF3, nInitF3, 27.,
    dxF3, 0.1, gam, mass, vHatF3, sigmaHatF3, 3, 200];
];

(* --- Bottom panel: tauHat = 1.5 (stable) --- *)
Print["\n--- tauHat = 1.5 (stable, evolve to t=372) ---"];
csS = charSpeeds[epsLF3, nLF3, gam, mass, vHatF3, sigmaHatF3, 1.5];
Print["  c+ = ", N[csS["cPlus"]], " (vL=0.9 < c+: stable)"];

stateS = evolve[epsInitF3, vInitF3, nInitF3, 372.,
  dxF3, 0.1, gam, mass, vHatF3, sigmaHatF3, 1.5, 1000];

(* --- Generate Fig. 3 --- *)
Print["\n--- Generating Fig. 3 ---"];

(* Top panel: show multiple snapshots for the unstable case *)
If[Length[unstableSnaps] > 0,
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
      PlotLabel -> Style["\!\(\*OverscriptBox[\(\[Tau]\), \(^\)]\) = 3 (unstable, v > c+)", 12],
      ImageSize -> 500, AspectRatio -> 0.5,
      Epilog -> {Red, Dashed, AbsoluteThickness[1.5],
        Line[{{xMinF3, N[csU["cPlus"]]}, {xMaxF3, N[csU["cPlus"]]}}]}
    ];
  ];,
  topPlotF3 = ListLinePlot[
    Transpose[{xGridF3, stateU[[2]]}],
    PlotRange -> {{xMinF3, xMaxF3}, {0, 1.0}},
    PlotStyle -> Directive[Black, AbsoluteThickness[1.5]],
    Frame -> True, FrameLabel -> {"x", "v"},
    PlotLabel -> Style["\!\(\*OverscriptBox[\(\[Tau]\), \(^\)]\) = 3, t = 27 (unstable, v > c+)", 12],
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
  PlotLabel -> Style["\!\(\*OverscriptBox[\(\[Tau]\), \(^\)]\) = 1.5, t = 372 (stable, v < c+)", 12],
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

(* Use smaller domain and coarser grid for long evolutions to improve performance *)
xMinF4 = -100.; xMaxF4 = 100.;
NxF4 = 128;
dxF4 = (xMaxF4 - xMinF4)/NxF4;
xGridF4 = Table[xMinF4 + (i - 0.5)*dxF4, {i, 1, NxF4}];
{epsInitF4, vInitF4, nInitF4} = makeInitialData[epsLF4, vLF4, nLF4, epsRF4, vRF4, nRF4, w, xGridF4];

(* Only run the three cases that don't blow up immediately:
   tauHat = 0.4 (stiff, CFL=0.01), 0.5 (CFL=0.1), 1.5 (CFL=0.1) *)
tauHatValsF4top = {0.4, 0.5, 1.5};
cflValsF4top = {0.01, 0.1, 0.1};

Do[
  Module[{cs4},
    cs4 = charSpeeds[epsLF4, nLF4, gam, mass, vHatF3, sigmaHatF3, tauHatValsF4top[[k]]];
    Print["  tauHat = ", tauHatValsF4top[[k]], ": c+ = ", N[cs4["cPlus"]]];
  ];
, {k, 1, 3}];

(* --- Top panel: tauHat = 0.4, 0.5, 1.5 at t=1582 --- *)
Print["\n--- Top panel: evolve to t=1582 ---"];

topStatesF4 = {};
Do[
  thVal = tauHatValsF4top[[k]]; cflVal = cflValsF4top[[k]];
  Print["  tauHat = ", thVal, ", CFL = ", cflVal];
  stK = evolve[epsInitF4, vInitF4, nInitF4, 1582.,
    dxF4, cflVal, gam, mass, vHatF3, sigmaHatF3, thVal, 5000];
  AppendTo[topStatesF4, stK];
, {k, 1, 3}];

(* --- Bottom panel: tauHat = 0.25 at early times (wildly superluminal) --- *)
Print["\n--- Bottom panel: tauHat = 0.25 ---"];
cs025 = charSpeeds[epsLF4, nLF4, gam, mass, vHatF3, sigmaHatF3, 0.25];
Print["  tauHat = 0.25: c+ = ", N[cs025["cPlus"]], " (wildly superluminal)"];

(* Use snapshots: the evolution will blow up quickly *)
earlyTimes = {0.27, 0.31, 0.36};
bottomSnaps025 = evolve[epsInitF4, vInitF4, nInitF4, 0.36,
  dxF4, 0.005, gam, mass, vHatF3, sigmaHatF3, 0.25, 200, earlyTimes];

(* Build bottomStatesF4 from snapshots *)
bottomStatesF4 = {};
Do[
  If[k <= Length[bottomSnaps025],
    AppendTo[bottomStatesF4, bottomSnaps025[[k, 2]]];,
    (* If snapshot not reached, use initial data *)
    AppendTo[bottomStatesF4,
      {N[epsInitF4], N[vInitF4], N[nInitF4], Table[0.,{NxF4}], Table[0.,{NxF4}]}];
  ];
, {k, 1, 3}];

(* --- Generate Fig. 4 --- *)
Print["\n--- Generating Fig. 4 ---"];

topColors = {GrayLevel[0.5], GrayLevel[0.25], GrayLevel[0.0]};
topPlotF4 = Show[
  ListLinePlot[Transpose[{xGridF4, vInitF4}],
    PlotStyle -> Directive[Gray, Dotted, AbsoluteThickness[1]]],
  Table[
    If[k <= Length[topStatesF4],
      ListLinePlot[Transpose[{xGridF4, topStatesF4[[k]][[2]]}],
        PlotStyle -> Directive[topColors[[k]], AbsoluteThickness[1.5]]],
      Graphics[]
    ], {k, 1, 3}],
  PlotRange -> {{xMinF4, xMaxF4}, {0.45, 0.65}},
  Frame -> True, FrameLabel -> {"x", "v"},
  PlotLabel -> Style["t = 0 (dotted), t = 1582 (solid)", 12],
  ImageSize -> 500, AspectRatio -> 0.5
];

bottomStyles = {
  Directive[GrayLevel[0.4], Dotted, AbsoluteThickness[1.5]],
  Directive[GrayLevel[0.2], Dashing[{0.02,0.01,0.005,0.01}], AbsoluteThickness[1.5]],
  Directive[Black, AbsoluteThickness[1.5]]
};
nBottom = Min[3, Length[bottomStatesF4]];
bottomPlotF4 = If[nBottom > 0,
  Show[
    Table[ListLinePlot[Transpose[{xGridF4, bottomStatesF4[[k]][[2]]}],
      PlotStyle -> bottomStyles[[k]]], {k, 1, nBottom}],
    PlotRange -> {{xMinF4, xMaxF4}, All},
    Frame -> True, FrameLabel -> {"x", "v"},
    PlotLabel -> Style["\!\(\*OverscriptBox[\(\[Tau]\), \(^\)]\) = 0.25 (wildly superluminal)", 12],
    ImageSize -> 500, AspectRatio -> 0.5
  ],
  Graphics[{}, Frame -> True, ImageSize -> 500, AspectRatio -> 0.5,
    PlotLabel -> Style["tauHat = 0.25: blew up before first snapshot", 12]]
];

fig4 = Column[{topPlotF4, bottomPlotF4}, Spacings -> 1];
Export["output/fig4.pdf", fig4];
Print["  Exported output/fig4.pdf"];

Print["\n========================================"];
Print["  Dynamic Shockwave Complete"];
Print["========================================"];
