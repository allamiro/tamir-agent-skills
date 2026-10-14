# The modelling cycle

The cycle below follows the steps of the Blum and Leiß cycle named in the Sauter and Albrecht checklist,
described here in original words with what typically goes wrong at each step. VERIFY the exact step names
against the workbook chapter.

| Step | What happens | Typical failure |
|---|---|---|
| 1. Understand the real situation | Read the biology, talk to the experimenters, list what is known and how well | Modelling a textbook cartoon rather than the system measured |
| 2. Simplify and structure | Choose the boundary, the species, the processes, the assumptions | Leaving out the process the question depends on |
| 3. Mathematise | Write equations, choose the formalism | Rate laws chosen for convenience, units mixed |
| 4. Work mathematically | Solve, simulate, analyse (steady state, stability, sensitivity) | Numerical artefacts mistaken for biology |
| 5. Interpret | Translate the results back into biological statements | Claims stronger than the assumptions allow |
| 6. Validate | Compare with data not used so far | Comparing with the fitting data |
| 7. Report or revise | Communicate the model, or return to step 2 | Hiding failed versions instead of reporting what was learned |

## How the steps connect to the book's other topics

- Step 2 is where variables, parameters and coefficients are distinguished and assumptions written down.
- Step 3 is where dimension analysis catches errors.
- Step 4 includes sensitivity analysis: which parameters the conclusions depend on.
- Step 6 includes model selection, for example with the Akaike information criterion, when several
  structures fit (`parameter-estimation-model-selection`).
