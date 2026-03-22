(* ============================================================== *)
(*  shockwave_steady.wl -- Steady-state shockwave ODE (Fig. 2)    *)
(*  Pandya, Most, Pretorius (2022)                                *)
(*  Run: wolframscript -file shockwave_steady.wl                  *)
(* ============================================================== *)

Print["========================================"];
Print["  Steady-State Shockwave ODE (Fig. 2)"];
Print["========================================"];

(* Load common module *)
SetDirectory[DirectoryName[$InputFileName]];
Get["bdnk_common.wl"];

If[!DirectoryQ["output"], CreateDirectory["output"]];

(* ---- Parameters (Table II, Fig. 2 row) ---- *)
gam = 4/3;
mass = 0.1;
vHat = 2/15;
sigmaHat = 0;
tauHat = 3/2;  (* 1.5 *)

(* Left asymptotic state *)
epsL = 1.0;
vL   = 0.8;
nL   = 0.1;

Print["\nParameters:"];
Print["  gam = ", gam, ", mass = ", mass, ", vHat = ", N[vHat]];
Print["  sigmaHat = ", sigmaHat, ", tauHat = ", N[tauHat]];
Print["  Left state: {eps, v, n} = {", epsL, ", ", vL, ", ", nL, "}"];

(* ---- Compute conserved quantities ---- *)
pL   = (gam - 1)*(epsL - mass*nL);
rhoL = epsL + pL;
wL   = 1/Sqrt[1 - vL^2];

Ttx = rhoL*wL^2*vL;
Txx = rhoL*wL^2*vL^2 + pL;

Print["\nConserved quantities:"];
Print["  P_L = ", N[pL], ", rho_L = ", N[rhoL], ", W_L = ", N[wL]];
Print["  T^{tx} = ", N[Ttx]];
Print["  T^{xx} = ", N[Txx]];

(* ---- Compute right state via Rankine-Hugoniot ---- *)
{epsR, vR, nR} = solveRankineHugoniot[epsL, vL, nL, gam, mass];
Print["\nRight state (Rankine-Hugoniot):"];
Print["  {eps_R, v_R, n_R} = {", epsR, ", ", vR, ", ", nR, "}"];

(* ---- Compute characteristic speeds at left state ---- *)
cs = charSpeeds[epsL, nL, gam, mass, vHat, sigmaHat, tauHat];
Print["\nCharacteristic speeds at left state:"];
Print["  c+ = ", N[cs["cPlus"]], ", c- = ", N[cs["cMinus"]]];
Print["  v_L = ", vL, " < c+ = ", N[cs["cPlus"]], ": ",
      If[vL < cs["cPlus"], "YES (smooth profile exists)", "NO"]];

(* ---- Constant transport coefficients ---- *)
tauEps = vHat*tauHat;
tauQ   = vHat*tauHat;
tauP   = 2*(gam - 1)*vHat;

Print["\nTransport constants:"];
Print["  tauEps = tauQ = ", N[tauEps]];
Print["  tauP = ", N[tauP]];

(* ---- Define RHS of shockwave ODE system ---- *)
(* State vector: y = {n, eps, v}
   Paper Eqs. 72, 76-77 *)

shockwaveRHS[x_?NumericQ, {nVal_?NumericQ, epsVal_?NumericQ, vVal_?NumericQ}] :=
Module[{ww, ww2, pp, rr, cs2Local, vVisc, sig, kE, kN, kSval,
        betaE, betaN0,
        aCoeff, bCoeff, cCoeff, discSq, disc, cp2, cm2, cp, cm,
        c0, c1, c2, c3, c4, d0, d1, d2, d3,
        denomEps, denomV, epsPrime, vPrime, nPrime},

  ww  = 1.0/Sqrt[1.0 - vVal^2];
  ww2 = 1.0/(1.0 - vVal^2);

  pp  = (gam - 1)*(epsVal - mass*nVal);
  rr  = epsVal + pp;
  cs2Local = gam*pp/rr;

  (* Transport coefficients *)
  vVisc = vHat*rr*cs2Local;
  kE    = -(gam - 1)*epsVal*rr^2/(nVal^2*pp);
  sig   = If[sigmaHat == 0, 0., vHat*rr*cs2Local*sigmaHat/(-kE)];
  kN    = rr/(nVal^2*pp)*((gam - 1)*epsVal^2 + pp^2);
  kSval = kE + kN;

  betaE  = tauQ*(gam - 1) + sig/rr*kE;
  betaN0 = tauQ*(-(gam - 1)*mass) + sig/nVal*kN;

  (* Characteristic speeds: A, B, C from paper Eqs. A2-A4 *)
  aCoeff = rr*tauEps*tauQ;
  bCoeff = -tauEps*(rr*cs2Local*tauQ + vVisc + sig*kSval) - rr*tauP*tauQ;
  cCoeff = tauP*(rr*cs2Local*tauQ + sig*kSval) - betaE*vVisc;

  discSq = bCoeff^2 - 4*aCoeff*cCoeff;
  disc   = Sqrt[Max[discSq, 0.]];
  cp2    = (-bCoeff + disc)/(2*aCoeff);
  cm2    = (-bCoeff - disc)/(2*aCoeff);
  cp     = Sqrt[Abs[cp2]];
  cm     = Sqrt[Abs[cm2]];

  (* Numerator coefficients (paper Eq. 78) *)
  c0 = betaN0*nVal*(Txx - pp);
  c1 = -Ttx*(2*betaN0*nVal - rr*tauP + vVisc);
  c2 = (betaN0*nVal - rr*(tauEps + tauP + tauQ) + vVisc)*(Txx + epsVal)
       + rr^2*(tauEps + tauQ);
  c3 = rr*Ttx*(tauEps + 2*tauQ);
  c4 = -rr*tauQ*(Txx + epsVal);

  d0 = betaE*(Txx - pp);
  d1 = -Ttx*(2*betaE + tauP);
  d2 = (Txx + epsVal)*(betaE + tauEps + tauP) - rr*tauEps;
  d3 = -tauEps*Ttx;

  (* Denominators *)
  denomEps = aCoeff*ww*vVal*(vVal^2 - cp2)*(vVal^2 - cm2);
  denomV   = aCoeff*ww^3*(vVal^2 - cp2)*(vVal^2 - cm2);

  (* Derivatives *)
  epsPrime = (c4*vVal^4 + c3*vVal^3 + c2*vVal^2 + c1*vVal + c0)/denomEps;
  vPrime   = (d3*vVal^3 + d2*vVal^2 + d1*vVal + d0)/denomV;
  nPrime   = -ww^2*nVal*vPrime/vVal;

  {nPrime, epsPrime, vPrime}
];

(* ---- Define separate scalar RHS functions for NDSolve ---- *)

shockwaveRHS1[x_?NumericQ, nVal_?NumericQ, epsVal_?NumericQ, vVal_?NumericQ] :=
  shockwaveRHS[x, {nVal, epsVal, vVal}][[1]];

shockwaveRHS2[x_?NumericQ, nVal_?NumericQ, epsVal_?NumericQ, vVal_?NumericQ] :=
  shockwaveRHS[x, {nVal, epsVal, vVal}][[2]];

shockwaveRHS3[x_?NumericQ, nVal_?NumericQ, epsVal_?NumericQ, vVal_?NumericQ] :=
  shockwaveRHS[x, {nVal, epsVal, vVal}][[3]];

(* ---- Solve the ODE system ---- *)
Print["\n--- Solving shockwave ODE ---"];

(* Strategy: integrate from left state with small perturbation.
   The perturbation grows exponentially, causing the transition.
   Then shift x so transition is centered at x=0. *)
xStart = -8.0;
xEnd   = 8.0;
delta  = 1.0*^-6;  (* Perturbation from left state *)

sol = NDSolve[{
  nn'[x] == shockwaveRHS1[x, nn[x], ee[x], vv[x]],
  ee'[x] == shockwaveRHS2[x, nn[x], ee[x], vv[x]],
  vv'[x] == shockwaveRHS3[x, nn[x], ee[x], vv[x]],
  nn[xStart] == N[nL],
  ee[xStart] == N[epsL],
  vv[xStart] == N[vL - delta]
}, {nn, ee, vv}, {x, xStart, xEnd},
  Method -> {"StiffnessSwitching",
    Method -> {{"ExplicitRungeKutta", "DifferenceOrder" -> 4},
               {"ImplicitRungeKutta"}}},
  MaxStepSize -> N[(xEnd - xStart)/16384],
  MaxSteps -> 2000000
];

nnF0 = nn /. sol[[1]];
eeF0 = ee /. sol[[1]];
vvF0 = vv /. sol[[1]];

Print["  Solution obtained (raw)."];
Print["  eps(xStart) = ", N[eeF0[xStart]], ", eps(xEnd) = ", N[eeF0[xEnd]]];

(* Find the x-coordinate where eps crosses the midpoint *)
epsMid = (epsL + epsR)/2;
Print["  epsMid = ", N[epsMid]];

(* Search for midpoint crossing within the integration domain *)
xSearch = Table[{x0, eeF0[x0]}, {x0, xStart, xEnd, 0.01}];
crossings = Select[Partition[xSearch, 2, 1],
  (#[[1, 2]] - epsMid)*(#[[2, 2]] - epsMid) <= 0 &];

If[Length[crossings] > 0,
  xGuess = (crossings[[1, 1, 1]] + crossings[[1, 2, 1]])/2;
  xShift = x /. FindRoot[eeF0[x] == epsMid, {x, xGuess}];
  Print["  Transition center at x = ", N[xShift], " (shifting to x=0)"];,
  (* Fallback: estimate shift from where eps starts changing *)
  Print["  WARNING: midpoint crossing not found in domain. Using manual shift."];
  xShift = -3.5;  (* Approximate from first run *)
];

(* Create shifted interpolating functions *)
nnF[x_?NumericQ] := nnF0[x + xShift];
eeF[x_?NumericQ] := eeF0[x + xShift];
vvF[x_?NumericQ] := vvF0[x + xShift];

Print["  After shift:"];
Print["  eps(-2) = ", N[eeF[-2.0]], ", eps(2) = ", N[eeF[2.0]]];
Print["  v(-2)   = ", N[vvF[-2.0]], ", v(2)   = ", N[vvF[2.0]]];
Print["  n(-2)   = ", N[nnF[-2.0]], ", n(2)   = ", N[nnF[2.0]]];

(* ---- Verify right-state approach ---- *)
xFarRight = Min[xEnd - xShift, 5.0];
Print["\nRight-state verification at shifted x = ", N[xFarRight], ":"];
Print["  eps = ", N[eeF[xFarRight]], " (expected: ", epsR, ")"];
Print["  v   = ", N[vvF[xFarRight]], " (expected: ", vR, ")"];
Print["  n   = ", N[nnF[xFarRight]], " (expected: ", nR, ")"];

(* ---- Plotting ---- *)
Print["\n--- Generating Fig. 2 ---"];

xPlotMin = -2;
xPlotMax = 2;

fig2 = Plot[{eeF[x], vvF[x], nnF[x]}, {x, xPlotMin, xPlotMax},
  Exclusions -> None,
  PlotStyle -> {
    Directive[Black, AbsoluteThickness[2]],             (* eps: solid *)
    Directive[Black, AbsoluteThickness[2],
      Dashing[{0.02, 0.01, 0.005, 0.01}]],             (* v: dash-dot *)
    Directive[Black, AbsoluteThickness[2], Dotted]      (* n: dotted *)
  },
  PlotRange -> All,
  Frame -> True,
  FrameLabel -> {"x", ""},
  FrameStyle -> Directive[Black, 12],
  PlotLegends -> Placed[
    LineLegend[{
      Directive[Black, AbsoluteThickness[2]],
      Directive[Black, AbsoluteThickness[2], Dashing[{0.02, 0.01, 0.005, 0.01}]],
      Directive[Black, AbsoluteThickness[2], Dotted]},
      {"\[Epsilon]", "v", "n"}],
    {Right, Top}],
  ImageSize -> 500,
  AspectRatio -> 0.7,
  PlotLabel -> Style["Steady-State Shockwave Profile (Fig. 2)", 14],
  PlotPoints -> 300
];

Export["output/fig2.pdf", fig2];
Print["  Exported output/fig2.pdf"];

(* ---- Additional diagnostics: verify conservation ---- *)
Print["\n--- Conservation check (shifted coordinates) ---"];
Do[
  Module[{epsX, vX, nX, pX, rhoX, wX, ttxX, txxX},
    epsX = eeF[N[xp]];
    vX = vvF[N[xp]];
    nX = nnF[N[xp]];
    pX = (gam - 1)*(epsX - mass*nX);
    rhoX = epsX + pX;
    wX = 1/Sqrt[1 - vX^2];
    (* Perfect fluid part of conserved quantities *)
    ttxX = rhoX*wX^2*vX;
    txxX = rhoX*wX^2*vX^2 + pX;
    Print["x = ", xp, ":  T^{tx}(PF) = ", N[ttxX],
          " (ref: ", N[Ttx], "),  delta = ", N[ttxX - Ttx]];
  ];
, {xp, {-2, -1, 0, 1, 2}}];

Print["\n========================================"];
Print["  Steady-State Shockwave Complete"];
Print["========================================"];
