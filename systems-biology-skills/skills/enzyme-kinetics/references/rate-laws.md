# Rate laws (v = rate, S = substrate, P = product, I = inhibitor)

| Law | Formula | Parameters |
|---|---|---|
| Michaelis–Menten | v = Vmax S / (Km + S) | Vmax (concentration/time), Km (concentration) |
| Competitive inhibition | v = Vmax S / (Km (1 + I/Ki) + S) | Ki |
| Uncompetitive inhibition | v = Vmax S / (Km + S (1 + I/Kii)) | Kii |
| Mixed inhibition | v = Vmax S / (Km (1 + I/Ki) + S (1 + I/Kii)) | Ki, Kii |
| Substrate inhibition | v = Vmax S / (Km + S + S^2/Ksi) | Ksi |
| Hill | v = Vmax S^n / (K^n + S^n) | K (concentration), n (dimensionless) |
| Reversible Michaelis–Menten | v = (Vf S/Ks - Vr P/Kp) / (1 + S/Ks + P/Kp) | Vf, Vr, Ks, Kp; Haldane: Keq = Vf Kp / (Vr Ks) |

## Michaelis–Menten from mass action (sketch)

E + S ⇌ ES → E + P with constants k1, k-1, k2. Quasi-steady state of ES (d[ES]/dt ≈ 0) and enzyme conservation
E_total = E + ES give v = k2 E_total S / ((k-1 + k2)/k1 + S), so Vmax = k2 E_total and Km = (k-1 + k2)/k1.
Km equals the dissociation constant only when k2 is much smaller than k-1.

Formulas are standard (author knowledge, VERIFY against an enzymology text); they match the functions in
the skill's kinetics script.
