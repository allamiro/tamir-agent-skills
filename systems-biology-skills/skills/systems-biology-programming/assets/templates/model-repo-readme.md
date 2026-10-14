# <Model name>

Reference publication: <citation with DOI, or "in preparation">
Model file: `model/model.xml` (SBML Level <L> Version <V>, packages: <fbc, qual, ...>)
Simulation description: `simulation/experiment.sedml`
Archive: <BioModels identifier or DOI>
Licence: <licence>

## What the model represents

Organism, cell type, compartments, conditions; the question it was built for; main assumptions (link to the
assumption register).

## How to run

```bash
<create environment from environment file>
<one command that regenerates the main figures>
```

Environment: `<environment file>` with pinned versions. Solver: <name, version, tolerances>. Seeds: <list>.

## Tests

`<test command>` checks: element and charge balance, conservation laws, known steady state, known knockout.

## Data

| File | Content | Source and version | Licence |
|---|---|---|---|

## Annotation

Species and reactions are annotated with identifiers.org URIs (ChEBI, UniProt, Rhea, GO, SBO), following MIRIAM.
