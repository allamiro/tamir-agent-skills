# Unit pitfalls in biological models

| Trap | Example | Check |
|---|---|---|
| Molar is per litre | 1 mM = 1 mol/m^3 (not 0.001) | `units.py convert 1 mM --to mol/m^3` |
| Micro written as u | uM, µM and μM are the same unit | Normalise before parsing |
| Second-order constants | 1e6 1/(M s) = 1e3 1/(mM s) = 1 1/(µM s) | Unit carries concentration to the power -1 |
| Time units | 0.1 1/min = 6 1/h | Convert the parameter, not the axis |
| Molecules to concentration | 1 molecule in 1 fL (about an E. coli volume) is about 1.66 nM | n / (N_A V) |
| Specific versus volumetric | mmol/(gDW h) times biomass (gDW/L) gives mmol/(L h) | Units must cancel |
| Michaelis constant | Km has the unit of concentration, not of rate | Km/S is dimensionless |
| Hill coefficient | dimensionless; K in a Hill law has concentration units | K^n has concentration^n |
| Daltons | 1 Da = 1 g/mol; a 50 kDa protein is 50,000 g/mol | Mass to amount needs molar mass |
| Percentages | w/v percent is g per 100 mL | State which percent |

The fL to nM figure is illustrative: 1 / (6.022e23 /mol × 1e-15 L) ≈ 1.66e-9 M.
