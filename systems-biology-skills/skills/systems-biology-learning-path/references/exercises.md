# Worked exercises with checkable answers

Try each by hand first, then run the command (from the skill that owns the script) to check. The expected
text is what the script prints; the collection's answer checker (check_answers.py in its scripts folder)
runs every row. Numbers are
illustrative teaching values, not measurements.

| # | Part | Exercise | Command | Expected output contains |
|---|---|---|---|---|
| 1 | 1 | Rank of the matrix with rows (1, 2) and (2, 4); why is it not 2? | `linalg.py rank "1,2;2,4"` | `rank 1 of a 2 x 2 matrix` |
| 2 | 1 | Determinant of rows (2, 1) and (1, 3), the area spanned by the two column vectors | `linalg.py det "2,1;1,3"` | `determinant 5` |
| 3 | 1 | Inverse of the same matrix | `linalg.py inv "2,1;1,3"` | `[3/5, -1/5]` |
| 4 | 1 | Solve x + y = 3, x - y = 1 and classify with Rouché–Capelli | `linalg.py solve "1,1;1,-1" --b "3,1"` | `one solution` |
| 5 | 1 | Classify x + y = 3, 2x + 2y = 7 | `linalg.py solve "1,1;2,2" --b "3,7"` | `no solution` |
| 6 | 1 | Eigenvalues of rows (2, 1) and (1, 2) from the characteristic polynomial | `linalg.py eig "2,1;1,2"` | `eigenvalues: 1, 3` |
| 7 | 1 | Reduced row-echelon form of rows (1, 2, 3) and (4, 5, 6) | `linalg.py rref "1,2,3;4,5,6"` | `[0, 1, 2]` |
| 8 | 2 | Null space of the chain A → B → C written as the matrix with rows (1, -1, 0) and (0, 1, -1) | `linalg.py null "1,-1,0;0,1,-1"` | `[1, 1, 1]` |
| 9 | 3 | Eigenvalues of the system matrix with rows (0, 1) and (-2, -3); is the system stable? | `linalg.py eig "0,1;-2,-3"` | `eigenvalues: -2, -1` |
| 10 | 3 | Routh–Hurwitz for s^3 + s^2 + 2s + 8 | `control.py routh "1,1,2,8"` | `2 root(s) with positive real part` |
| 11 | 3 | Is the pair A = rows (0, 1), (-2, -3), B = (0, 1) controllable? | `control.py ctrb "0,1;-2,-3" "0;1"` | `controllable` |
| 12 | 3 | Poles and steady-state gain of 1 / (s^2 + 3s + 2) | `control.py tf "1" "1,3,2"` | `steady-state gain (s = 0): 0.5` |
| 13 | 3 | Overshoot of a second-order system with natural frequency 2 and damping ratio 0.3 | `control.py second --wn 2 --zeta 0.3` | `overshoot_percent    37.2326` |
| 14 | 3 | Close a unity negative feedback loop around 4 / (10 s + 1) | `control.py loop --K 4 --tau 10` | `closed-loop gain 0.8, time constant 2` |
| 15 | 3 | Fixed points of the logistic map at r = 2.8 and their stability | `discrete.py map --r 2.8` | `fixed point 0.642857: stable` |
| 16 | 4 | Convert 5 mM to mol/m^3 | `units.py convert 5 mM --to mol/m^3` | `5 mM = 5 mol/m^3` |
| 17 | 4 | Convert a rate constant of 0.1 per minute to per hour | `units.py convert 0.1 1/min --to 1/h` | `6 1/h` |
| 18 | 4 | Convert a second-order constant of 1e6 per molar per second to per micromolar per second | `units.py convert 1e6 "1/(M*s)" --to "1/(uM*s)"` | `= 1 1/(uM*s)` |
| 19 | 4 | Chemostat at D = 0.2 per hour, mumax 0.5 per hour, Ks 0.1 g/L, S0 10 g/L, yield 0.5 | `units.py chemostat --D 0.2 --mumax 0.5 --Ks 0.1 --S0 10 --Y 0.5` | `X* = 4.96667` |
| 20 | 4 | Michaelis–Menten rate at S = 2, Vmax = 10, Km = 1 | `kinetics.py rate mm --S 2 --Vmax 10 --Km 1` | `v = 6.66667` |
| 21 | 4 | The same with a competitive inhibitor, I = 1, Ki = 0.5 | `kinetics.py rate competitive --S 2 --Vmax 10 --Km 1 --I 1 --Ki 0.5` | `v = 4` |
| 22 | 4 | Hill rate at S = 2, K = 1, n = 2, Vmax = 10 | `kinetics.py rate hill --S 2 --Vmax 10 --K 1 --n 2` | `v = 8` |
| 23 | 4 | AIC, AICc and BIC for RSS 1.2, n = 20, k = 3 | `fitstats.py ic --rss 1.2 --n 20 --k 3` | `AICc -48.7682` |
| 24 | 4 | Nested models: RSS 4 with 2 parameters against RSS 2.5 with 3, n = 20 | `fitstats.py ftest --rss1 4 --k1 2 --rss2 2.5 --k2 3 --n 20` | `F = 10.2000 on (1, 17)` |
| 25 | PK | Half-life and AUC of an IV bolus of 100 mg, V = 20 L, CL = 5 L/h | `pk.py iv --dose 100 --V 20 --CL 5 --t 2` | `AUC_inf                      20` |
| 26 | PK | Accumulation when dosing every 8 h | `pk.py repeat --dose 100 --F 1 --V 20 --CL 5 --tau 8` | `accumulation_ratio           1.15652` |
| 27 | Methods | Reliability of a scale with reliability 0.7 when doubled in length (Spearman–Brown) | `measure.py sb --r 0.7 --factor 2` | `0.8235` |
| 28 | Programming | Element counts of Ca(OH)2 | `balance.py formula "Ca(OH)2"` | `Ca 1, O 2, H 2` |

## Hand-working hints

- 1: the second row is twice the first. 2: 2·3 − 1·1. 4: add the equations. 5: the left sides are proportional,
  the right sides are not. 6: λ^2 − 4λ + 3 = 0. 9: λ^2 + 3λ + 2 = 0; both roots negative.
- 10: the third entry of the first column is (1·2 − 1·8)/1 = −6.
- 13: overshoot = exp(−πζ/√(1−ζ²)). 14: gain K/(1+K), time constant τ/(1+K).
- 15: fixed points x = 0 and x = 1 − 1/r; stable if |r(1 − 2x)| < 1.
- 19: S\* = Ks D/(mumax − D), X\* = Y (S0 − S\*).
- 21: the apparent Km is Km (1 + I/Ki) = 3.
- 23: AIC = n ln(RSS/n) + 2k; AICc adds 2k(k+1)/(n − k − 1).
- 26: R = 1/(1 − e^(−kτ)) with k = CL/V.
- 27: ρ' = 2ρ/(1 + ρ).
