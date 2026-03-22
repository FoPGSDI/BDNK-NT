(* ============================================================== *)
(*  bjorken.wl -- Bjorken flow ODE solver (reproduces Fig. 1)      *)
(*  Pandya, Most, Pretorius (2022)                                 *)
(*  Run: wolframscript -file bjorken.wl                            *)
(* ============================================================== *)

Print["========================================"];
Print["  Bjorken Flow Solver (Fig. 1)"];
Print["========================================"];

SetDirectory[DirectoryName[$InputFileName]];
Get["bdnk_common.wl"];

If[!DirectoryQ["output"], CreateDirectory["output"]];

(* ---- Parameters (Table II, Fig. 1 row) ---- *)
gam = 4/3;
mass = 1;
vHat = 1/10;
sigmaHat = 0;
tauHatValues = {1/2, 1, 2};
eps0 = 1/4;
epsDot0Values = {-2, 0, 2};
n0 = 1/10;
tauMin = 1;
tauMax = 20;

Print["\nParameters:"];
Print["  gam = ", gam, ", mass = ", mass, ", vHat = ", vHat];
Print["  sigmaHat = ", sigmaHat];
Print["  tauHat values = ", tauHatValues];

(* ---- Compute characteristic speeds ---- *)
Do[
  tauEpsC = vHat*th;
  tauPC = 2*(gam - 1)*vHat;
  cs = charSpeeds[eps0, n0, gam, mass, vHat, sigmaHat, th];
  Print["tauHat = ", th, ": tauEps=", N[tauEpsC],
        ", c+=", N[cs["cPlus"]],
        If[cs["cPlus"] < 1, " (causal)", " (SUPERLUMINAL)"]];
, {th, tauHatValues}];

(* ---- Define RHS functions for NDSolve ---- *)
(* Two separate scalar functions to avoid list-indexing issues *)

bjorkenRHS1[tau_?NumericQ, epsVal_?NumericQ, epsDotVal_?NumericQ,
            gamL_, massL_, vHatL_, tauHatL_, n0L_] := epsDotVal;

bjorkenRHS2[tau_?NumericQ, epsVal_?NumericQ, epsDotVal_?NumericQ,
            gamL_, massL_, vHatL_, tauHatL_, n0L_] :=
Module[{nn, pp, rr, cs2, vVisc, tauEpsL, tauPL},
  nn = n0L/tau;
  pp = (gamL - 1)*(epsVal - massL*nn);
  rr = epsVal + pp;
  cs2 = gamL*pp/rr;
  vVisc = vHatL*rr*cs2;
  tauEpsL = vHatL*tauHatL;
  tauPL = 2*(gamL - 1)*vHatL;

  (1/tauEpsL)*(
    -(1/tau)*(tau + 2*tauEpsL + tauPL)*epsDotVal
    - (1/tau^2)*(rr*(tau + tauPL) - vVisc)
  )
];

(* ---- Solve using NDSolve ---- *)
Print["\n--- Solving Bjorken flow ODEs ---"];

allSolutions = {};

Do[
  Print["  tauHat = ", th, ", epsDot0 = ", ed0, " ..."];

  sol = NDSolve[{
    y1'[t] == bjorkenRHS1[t, y1[t], y2[t], gam, mass, vHat, th, n0],
    y2'[t] == bjorkenRHS2[t, y1[t], y2[t], gam, mass, vHat, th, n0],
    y1[tauMin] == N[eps0],
    y2[tauMin] == N[ed0]
  }, {y1, y2}, {t, tauMin, tauMax},
    Method -> {"ExplicitRungeKutta", "DifferenceOrder" -> 4},
    MaxStepSize -> N[(tauMax - tauMin)/2048],
    MaxSteps -> 100000
  ];

  AppendTo[allSolutions, <|"tauHat" -> th, "epsDot0" -> ed0,
    "eps" -> (y1 /. sol[[1]]), "epsDot" -> (y2 /. sol[[1]])|>];

  Print["    eps(20) = ", N[(y1 /. sol[[1]])[tauMax], 6]];
, {th, tauHatValues}, {ed0, epsDot0Values}];

(* ---- Inviscid reference ---- *)
inviscidDiag[tau_] := mass*n0*(gam - 1)/tau^2;

Print["\nInviscid ref: m*n0*(gam-1)/tau^2 = ", N[mass*n0*(gam-1)], "/tau^2"];

(* ---- Top panel: log-log plot ---- *)
Print["\n--- Generating Top Panel ---"];

lineStyles = {
  Directive[Black, AbsoluteThickness[1.5]],
  Directive[Black, AbsoluteThickness[1.5], Dashing[{0.02, 0.01, 0.005, 0.01}]],
  Directive[Black, AbsoluteThickness[1.5], Dotted]
};

(* Build data tables with log spacing *)
tauPts = Table[tauMin*Exp[Log[tauMax/tauMin]*i/500], {i, 1, 500}];

(* Transform data to log-log space and use plain ListLinePlot *)
topPlots = {};
Do[
  Do[
    idx = (ith - 1)*3 + ied;
    s = allSolutions[[idx]];
    epsF = s["eps"];
    edF  = s["epsDot"];
    data = Table[{tau, Abs[edF[tau] + gam*epsF[tau]/tau]}, {tau, tauPts}];
    data = Select[data, #[[2]] > 0 &];
    (* Transform to log10 space *)
    logData = {Log10[#[[1]]], Log10[#[[2]]]} & /@ data;
    AppendTo[topPlots,
      ListLinePlot[logData, PlotStyle -> lineStyles[[ith]]]
    ];
  , {ied, 1, 3}];
, {ith, 1, 3}];

inviscidData = Table[{tau, inviscidDiag[tau]}, {tau, tauPts}];
inviscidLogData = {Log10[#[[1]]], Log10[#[[2]]]} & /@ inviscidData;
inviscidPlot = ListLinePlot[inviscidLogData,
  PlotStyle -> Directive[Red, AbsoluteThickness[2.5], Dashed]];

topPanel = Show[topPlots, inviscidPlot,
  PlotRange -> {{Log10[tauMin], Log10[tauMax]}, {Log10[5*^-5], Log10[2]}},
  Frame -> True,
  FrameLabel -> {"Log\[ThinSpace]\[Tau]",
    "Log |\!\(\*OverscriptBox[\(\[Epsilon]\), \(.\)]\) + \[CapitalGamma]\[Epsilon]/\[Tau]|"},
  FrameTicks -> {
    {Table[{Log10[t], ToString[t]}, {t, {1, 2, 5, 10, 20}}], None},
    {Table[{Log10[v], Superscript["10", ToString[Round[Log10[v]]]]},
       {v, {10^-4, 10^-3, 10^-2, 10^-1, 1}}], None}
  },
  FrameStyle -> Directive[Black, 12],
  ImageSize -> 500, AspectRatio -> 0.7,
  PlotLabel -> Style["Bjorken Flow: Top Panel (Fig. 1)", 14]
];

(* ---- Bottom panel: T_BDNK and T_Eckart for tauHat=2 using explicit data ---- *)
Print["--- Generating Bottom Panel ---"];

bottomPlots = {};
Do[
  s = allSolutions[[6 + ied]];  (* tauHat=2 solutions: indices 7,8,9 *)
  epsF = s["eps"];
  edF  = s["epsDot"];

  (* BDNK temperature: T = P/n *)
  dataBDNK = Table[
    {tau, (gam - 1)*(epsF[tau]/(n0/tau) - mass)},
    {tau, tauPts}];
  AppendTo[bottomPlots,
    ListPlot[dataBDNK,
      PlotStyle -> Directive[Black, AbsoluteThickness[1.5]],
      Joined -> True
    ]
  ];

  (* Eckart temperature:
     T^{tau tau} = eps + tauEps*(epsDot + rho/tau)
     epsEckart = T^{tau tau}
     T_Eckart = (gam-1)*(epsEckart/n - mass) *)
  dataEckart = Table[
    Module[{nn, epsVal, edotVal, pp, rr, tauEpsL, ttt, epsE},
      nn = n0/tau;
      epsVal = epsF[tau]; edotVal = edF[tau];
      pp = (gam - 1)*(epsVal - mass*nn);
      rr = epsVal + pp;
      tauEpsL = vHat*2;  (* tauHat = 2 *)
      ttt = epsVal + tauEpsL*(edotVal + rr/tau);
      epsE = ttt;
      {tau, (gam - 1)*(epsE/nn - mass)}
    ],
    {tau, tauPts}];
  AppendTo[bottomPlots,
    ListPlot[dataEckart,
      PlotStyle -> Directive[Blue, AbsoluteThickness[1.5], Dashed],
      Joined -> True
    ]
  ];
, {ied, 1, 3}];

bottomPanel = Show[bottomPlots,
  PlotRange -> {{tauMin, tauMax}, {-0.8, 2.5}},
  ScalingFunctions -> {"Log", None},
  Frame -> True,
  FrameLabel -> {"\[Tau]", "T"},
  FrameStyle -> Directive[Black, 12],
  ImageSize -> 500, AspectRatio -> 0.7,
  PlotLabel -> Style["T (black=BDNK, blue dashed=Eckart), \!\(\*OverscriptBox[\(\[Tau]\), \(^\)]\)=2", 14]
];

(* ---- Export ---- *)
Print["\n--- Exporting ---"];
Export["output/fig1_top.pdf", topPanel];
Print["  output/fig1_top.pdf"];
Export["output/fig1_bottom.pdf", bottomPanel];
Print["  output/fig1_bottom.pdf"];
Export["output/fig1_combined.pdf", Column[{topPanel, bottomPanel}, Spacings -> 1]];
Print["  output/fig1_combined.pdf"];

(* ---- Diagnostics ---- *)
Print["\n--- Diagnostics ---"];
Do[
  s = allSolutions[[idx]];
  epsF = s["eps"]; edF = s["epsDot"];
  Print["tauHat=", s["tauHat"], ", edot0=", s["epsDot0"],
    ":  diag(20)=", N[Abs[edF[20] + gam*epsF[20]/20]],
    "  (inviscid=", N[inviscidDiag[20]], ")"];
, {idx, 1, Length[allSolutions]}];

Print["\n========================================"];
Print["  Bjorken Flow Complete"];
Print["========================================"];
