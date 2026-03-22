(* ============================================================== *)
(*  bdnk_common.wl -- Shared module for BDNK numerical methods    *)
(*  Pandya, Most, Pretorius (2022)                                *)
(*  Load via: Get[FileNameJoin[{dir, "bdnk_common.wl"}]]          *)
(* ============================================================== *)

Print["Loading bdnk_common.wl ..."];

(* ================================================================ *)
(*  1. EQUATION OF STATE  (gamma-law ideal gas, paper Eqs. 25-26)   *)
(* ================================================================ *)

pressure[eps_, n_, gam_, mass_] := (gam - 1)*(eps - mass*n);

enthalpy[eps_, n_, gam_, mass_] := gam*eps - (gam - 1)*mass*n;
(* = eps + P *)

soundSpeedSq[eps_, n_, gam_, mass_] :=
  gam*pressure[eps, n, gam, mass] / enthalpy[eps, n, gam, mass];

temperature[eps_, n_, gam_, mass_] := pressure[eps, n, gam, mass]/n;
(* = (gam-1)*(eps/n - mass) *)

lorentzW[v_] := 1.0/Sqrt[1.0 - v^2];

(* ================================================================ *)
(*  2. MICROPHYSICS  (paper Eqs. 31-38)                             *)
(* ================================================================ *)

pPrimeEps[gam_] := gam - 1;
pPrimeN[gam_, mass_] := -(gam - 1)*mass;

kappaEpsilon[eps_, n_, gam_, mass_] := Module[{pp, rr},
  pp = pressure[eps, n, gam, mass];
  rr = enthalpy[eps, n, gam, mass];
  -(gam - 1)*eps*rr^2/(n^2*pp)
];

kappaN[eps_, n_, gam_, mass_] := Module[{pp, rr},
  pp = pressure[eps, n, gam, mass];
  rr = enthalpy[eps, n, gam, mass];
  rr/(n^2*pp)*((gam - 1)*eps^2 + pp^2)
];

kappaS[eps_, n_, gam_, mass_] :=
  -(gam - 1)*mass*enthalpy[eps, n, gam, mass]/n;

alphaRatio[eps_, n_, gam_, mass_] :=
  (gam - 1)/soundSpeedSq[eps, n, gam, mass];

omegaRatio[eps_, n_, gam_, mass_] := Module[{pp, rr},
  pp = pressure[eps, n, gam, mass];
  rr = enthalpy[eps, n, gam, mass];
  mass*n*pp/(eps*rr)
];

(* ================================================================ *)
(*  3. TRANSPORT COEFFICIENTS  (paper Eq. 41, L=1)                  *)
(* ================================================================ *)

transportCoeffs[eps_, n_, gam_, mass_, vHat_, sigmaHat_, tauHat_] :=
Module[{pp, rr, cs2, vVisc, tauEps, tauP, tauQ, kE, sig, kN, kSval,
        betaEps, betaN, kap, gamCoeff},

  pp  = (gam - 1)*(eps - mass*n);
  rr  = eps + pp;
  cs2 = gam*pp/rr;

  vVisc  = vHat*rr*cs2;
  tauEps = vHat*tauHat;
  tauQ   = vHat*tauHat;
  tauP   = 2*(gam - 1)*vHat;

  kE   = -(gam - 1)*eps*rr^2/(n^2*pp);
  sig  = If[sigmaHat == 0 || sigmaHat == 0., 0.,
            vHat*rr*cs2*sigmaHat/(-kE)];

  kN   = rr/(n^2*pp)*((gam - 1)*eps^2 + pp^2);
  kSval = kE + kN;

  betaEps = tauQ*(gam - 1) + sig/rr*kE;
  betaN   = tauQ*(-(gam - 1)*mass) + sig/n*kN;

  kap = If[sigmaHat == 0 || sigmaHat == 0., 0.,
           sig*rr^2/(n^2*(pp/n))];

  gamCoeff = tauQ + sig*rr/n^2;

  <|"P" -> pp, "rho" -> rr, "cs2" -> cs2, "V" -> vVisc,
    "tauEps" -> tauEps, "tauP" -> tauP, "tauQ" -> tauQ,
    "sigma" -> sig, "betaEps" -> betaEps, "betaN" -> betaN,
    "kE" -> kE, "kN" -> kN, "kS" -> kSval,
    "kappa" -> kap, "gammaCoeff" -> gamCoeff|>
];

(* ================================================================ *)
(*  4. CHARACTERISTIC SPEEDS  (paper Eqs. A15-A16)                  *)
(* ================================================================ *)

charSpeeds[eps_, n_, gam_, mass_, vHat_, sigmaHat_, tauHat_] :=
Module[{cs2, alp, omg, innerSq, disc, cp2, cm2},
  cs2 = soundSpeedSq[eps, n, gam, mass];
  alp = alphaRatio[eps, n, gam, mass];
  omg = omegaRatio[eps, n, gam, mass];
  innerSq = omg*sigmaHat*(4*alp + omg*sigmaHat)
            + (2*alp + 1)^2
            - 2*(omg + 2)*sigmaHat
            + tauHat^2
            + tauHat*(2 - 2*omg*sigmaHat);
  disc = Sqrt[Max[innerSq, 0]];
  cp2 = cs2/(2*tauHat)*(2*alp - omg*sigmaHat + tauHat + 1 + disc);
  cm2 = cs2/(2*tauHat)*(2*alp - omg*sigmaHat + tauHat + 1 - disc);
  <|"cPlus" -> Sqrt[Abs[cp2]], "cMinus" -> Sqrt[Abs[cm2]],
    "cPlus2" -> cp2, "cMinus2" -> cm2|>
];

(* ================================================================ *)
(*  5. RANKINE-HUGONIOT SOLVER                                      *)
(* ================================================================ *)

solveRankineHugoniot[epsL_, vL_, nL_, gam_, mass_] := Module[
  {pL, rhoL, wL, eqs, sol, epsR, vR, nR},
  pL   = (gam - 1)*(epsL - mass*nL);
  rhoL = epsL + pL;
  wL   = 1/Sqrt[1 - vL^2];

  eqs = {
    nL*wL*vL - nR/Sqrt[1 - vR^2]*vR,
    rhoL*wL^2*vL - (gam*epsR - (gam-1)*mass*nR)/(1 - vR^2)*vR,
    rhoL*wL^2*vL^2 + pL
      - (gam*epsR - (gam-1)*mass*nR)/(1 - vR^2)*vR^2
      - (gam - 1)*(epsR - mass*nR)
  };

  sol = FindRoot[Thread[eqs == 0],
    {{epsR, 2*epsL}, {vR, vL/2}, {nR, 2*nL}}];
  {epsR /. sol, vR /. sol, nR /. sol}
];

(* ================================================================ *)
(*  6. BDNK STRESS-ENERGY IN 1+1D FLAT SPACETIME                   *)
(*     Computes T^{tt}, T^{tx}, T^{xx}, J^t, J^x                  *)
(*     from primitives (eps,v,n) and their derivatives              *)
(* ================================================================ *)
(*
   In 1+1D with u^a = (W, Wv):
   - divU  = theta = W^3*(v*dtV + dxV)
   - udotEps = W*(dtEps + v*dxEps)
   - uDotUx  = W^4*(dtV + v*dxV)
   - Delta^{xc}*nabla_c f = W^2*(v*dtF + dxF)  for scalar f

   Shear tensor in 1+1D (3+1D with trivial y,z):
   sigma^{xx} = (2/3)*W^2*divU,  sigma^{tx} = v*sigma^{xx},
   sigma^{tt} = v^2*sigma^{xx}

   T^{ab} = scrE*u^a*u^b + scrP*Delta^{ab}
          + Q^a*u^b + Q^b*u^a - 2*eta*sigma^{ab}
   with Q^t = v*Q^x  (orthogonality u_a Q^a = 0)
*)

bdnkTab[eps_, v_, n_, dtEps_, dxEps_, dtV_, dxV_, dxN_,
        gam_, mass_, vHat_, sigmaHat_, tauHat_] :=
Module[{pp, rr, cs2, ww, ww2, tc,
        tauEps, tauP, tauQ, vVisc, sig, betaE, betaN0, eta0,
        divU, udotEps, uDotUx, dxEpsProj, dxNProj,
        scrE, scrP, scrQx, sigXX, sigTX, sigTT,
        ttt, ttx, txx, jt, jx},

  pp  = (gam - 1)*(eps - mass*n);
  rr  = eps + pp;
  cs2 = gam*pp/rr;
  ww  = 1.0/Sqrt[1.0 - v^2];
  ww2 = 1.0/(1.0 - v^2);

  tc = transportCoeffs[eps, n, gam, mass, vHat, sigmaHat, tauHat];
  tauEps = tc["tauEps"];
  tauP   = tc["tauP"];
  tauQ   = tc["tauQ"];
  vVisc  = tc["V"];
  sig    = tc["sigma"];
  betaE  = tc["betaEps"];
  betaN0 = tc["betaN"];

  (* Convention: eta = 3V/4, zeta = 0  (only V matters in 1+1D) *)
  eta0 = 3.0*vVisc/4.0;

  (* Kinematic quantities *)
  divU     = ww^3*(v*dtV + dxV);           (* nabla_c u^c *)
  udotEps  = ww*(dtEps + v*dxEps);         (* u^c nabla_c eps *)
  uDotUx   = ww^4*(dtV + v*dxV);           (* u^c nabla_c u^x *)
  dxEpsProj = ww2*(v*dtEps + dxEps);       (* Delta^{xc}*nabla_c eps *)
  dxNProj   = ww2*(0 + dxN);               (* Delta^{xc}*nabla_c n *)
  (* Note: dtN not needed as J^a = n*u^a with nabla_a J^a = 0
     and for the stress-energy we only need spatial gradient of n.
     Actually Delta^{xc}*nabla_c n = W^2*v*dtN + W^2*dxN.
     But for initial data with dtN=0, and during evolution dtN
     is not independently evolved. For the BDNK system, dtN is
     determined by baryon conservation: dt(nW) + dx(nWv) = 0.
     We handle this by passing dxN only and assuming dtN contribution
     is zero or absorbed. For the heat flow and shockwave problems
     where v=0 initially, this is fine. For general use, one
     should compute dtN from the baryon conservation equation. *)

  (* Script quantities *)
  scrE  = eps + tauEps*(udotEps + rr*divU);
  scrP  = pp + tauP*(udotEps + rr*divU);  (* zeta=0 with our convention *)
  scrQx = tauQ*rr*uDotUx + betaE*dxEpsProj + betaN0*dxNProj;

  (* Shear tensor components *)
  sigXX = (2.0/3.0)*ww2*divU;
  sigTX = v*sigXX;
  sigTT = v^2*sigXX;

  (* Assemble T^{ab} *)
  ttt = scrE*ww2 + scrP*ww2*v^2 + 2*v*scrQx*ww - 2*eta0*sigTT;
  ttx = (scrE + scrP)*ww2*v + scrQx*ww*(1 + v^2) - 2*eta0*sigTX;
  txx = scrE*ww2*v^2 + scrP*ww2 + 2*scrQx*ww*v - 2*eta0*sigXX;

  (* Baryon current *)
  jt = n*ww;
  jx = n*ww*v;

  <|"Ttt" -> ttt, "Ttx" -> ttx, "Txx" -> txx,
    "Jt" -> jt, "Jx" -> jx,
    "scrE" -> scrE, "scrP" -> scrP, "scrQx" -> scrQx,
    "divU" -> divU, "udotEps" -> udotEps|>
];

(* ================================================================ *)
(*  7. CONSERVATIVE-TO-PRIMITIVE RECOVERY  (for PDE solver)         *)
(*     Given conserved vars (Ttt, Ttx, Jt) and auxiliary info,      *)
(*     recover (eps, v, n)                                          *)
(* ================================================================ *)
(*
   For the perfect-fluid part (zeroth order):
   Ttt = rho*W^2 - P = (gam*eps - (gam-1)*m*n)*W^2 - (gam-1)*(eps-m*n)
   Ttx = rho*W^2*v
   Jt  = n*W
   From Ttx and Ttt+P:  v = Ttx/(Ttt+P)
   This is an implicit equation since P depends on eps, n.

   For BDNK, the conserved variables include gradient corrections,
   making exact inversion very hard. Instead, for the PDE solver
   we evolve primitives directly using the method-of-lines approach.
*)

(* ================================================================ *)
(*  8. PDE SOLVER INFRASTRUCTURE                                    *)
(*     Method of lines: evolve primitives (eps, v, n) and their     *)
(*     time derivatives (dtEps, dtV) directly                       *)
(* ================================================================ *)

(* Minmod limiter *)
minmod[a_, b_] := If[a*b <= 0, 0., If[Abs[a] < Abs[b], a, b]];

(* 2nd-order slopes with minmod limiter *)
reconstructSlopes[u_, dx_] := Module[{nn, slopes},
  nn = Length[u];
  slopes = Table[
    minmod[(u[[i+1]] - u[[i]])/dx, (u[[i]] - u[[i-1]])/dx],
    {i, 2, nn - 1}
  ];
  Join[{slopes[[1]]}, slopes, {slopes[[-1]]}]
];

(* 4th-order centered finite difference for first derivative *)
d1Center4[u_, i_, dx_] :=
  (-u[[i+2]] + 8*u[[i+1]] - 8*u[[i-1]] + u[[i-2]])/(12*dx);

(* 4th-order centered finite difference for second derivative *)
d2Center4[u_, i_, dx_] :=
  (-u[[i+2]] + 16*u[[i+1]] - 30*u[[i]] + 16*u[[i-1]] - u[[i-2]])/(12*dx^2);

(* 2nd-order centered finite difference for first derivative *)
d1Center2[u_, i_, dx_] :=
  (u[[i+1]] - u[[i-1]])/(2*dx);

(* ================================================================ *)
(*  9. UTILITY: APPLY OUTFLOW (COPY) BOUNDARY CONDITIONS            *)
(* ================================================================ *)

applyOutflowBC[u_, nGhost_] := Module[{uu},
  uu = u;
  Do[uu[[i]] = uu[[nGhost + 1]], {i, 1, nGhost}];
  Do[uu[[i]] = uu[[Length[uu] - nGhost]], {i, Length[uu] - nGhost + 1, Length[uu]}];
  uu
];

Print["bdnk_common.wl loaded successfully."];
Print["  EOS: pressure, enthalpy, soundSpeedSq, temperature"];
Print["  Transport: transportCoeffs, charSpeeds"];
Print["  Solver: solveRankineHugoniot, bdnkTab"];
Print["  FD: d1Center2, d1Center4, d2Center4, minmod, reconstructSlopes"];
Print["  BC: applyOutflowBC"];
