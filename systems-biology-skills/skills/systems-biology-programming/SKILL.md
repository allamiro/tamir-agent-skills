---
name: systems-biology-programming
description: Writes, tests and shares code and model files for systems biology, covering Python and other tools (NumPy, SciPy solve_ivp, COBRApy, libRoadRunner, Tellurium, COPASI, PySB), standard formats (SBML, SED-ML, CellML, the COMBINE archive), annotation (MIRIAM, identifiers.org, SBO), MIASE for simulations, BioModels deposition, MEMOTE tests for metabolic models, element and charge balance checks, unit tests for models, and reproducible environments. Use for "write Python code to simulate this model", "export my model to SBML", "annotate my model", "test my metabolic model", "check my reactions are balanced", "make my simulation reproducible", "which tool should I use for this model", "deposit my model in BioModels". Use the formalism skills (ode-dynamics, flux-balance-analysis) for the analysis itself and model-review to audit a model.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Systems biology programming

## Purpose and activation

A model that lives only in a script cannot be checked, reused or cited. Standard formats separate the
model (SBML or CellML) from the simulation experiment (SED-ML), annotations tie each element to a database
entry, and tests catch unbalanced reactions or growth from nothing before they reach a paper. Activate
when the user writes model code, converts between formats, annotates, tests or shares a model.

## Required inputs

The model (equations, reactions, or an existing file) and its formalism; the language and tools the user
prefers; what will be shared and with whom; and any journal or repository requirements.

## Workflow

1. **Pick the tool by formalism** with the table below; prefer tools that read and write standard formats.
2. **Write the model in a standard format** (SBML for reaction-based models; CellML for general equation-based
   models), not only as solver code. Keep units in the file.
3. **Annotate** each species and reaction with identifiers.org URIs to databases (ChEBI, UniProt, KEGG, Rhea,
   GO) and model terms (SBO), following MIRIAM; record the creator, dates and the reference publication.
4. **Check reaction balance** with `python3 scripts/balance.py check REACTIONS.txt FORMULAS.txt`; every reaction except
   exchange, demand and biomass should balance elements and charge.
5. **Test the model:** unit tests for known behaviour (a steady state, a conservation law, a known knockout),
   and for genome-scale metabolic models a MEMOTE report.
6. **Describe the simulation** in SED-ML (model, changes, simulation settings, outputs) and report what MIASE
   asks for: which model, which simulations, which outputs and how they were produced.
7. **Package** model, SED-ML, data and scripts in a COMBINE archive or a versioned repository with an
   environment file (`assets/templates/model-repo-readme.md`), and deposit in BioModels or a general
   archive with a DOI.
8. **Write code that can be checked:** fixed seeds, pinned versions, no hard-coded paths, tolerances stated;
   `references/code-practices.md` lists the details.

## Decision framework

| Need | Tool (examples) | Format |
|---|---|---|
| ODE simulation in Python | SciPy solve_ivp; libRoadRunner or Tellurium for SBML | SBML, Antimony for writing |
| GUI, parameter estimation, stochastic simulation | COPASI | SBML, SED-ML |
| Constraint-based metabolic models | COBRApy (Python), COBRA Toolbox (MATLAB) | SBML with the fbc package |
| Rule-based models (many complexes) | PySB, BioNetGen | BNGL, SBML export |
| Logical models | GINsim, CellNOpt, MaBoSS: VERIFY | SBML qual |
| Equation-based physiology | OpenCOR | CellML |
| Quick checks in this collection | The standard-library scripts | Plain text |

## Failure and edge cases

- **A model shared only as solver code** in one language.
- **Annotations missing or pointing to the wrong organism.**
- **SBML that validates but has no units,** so the simulator assumes defaults.
- **Unbalanced reactions** hiding mass or charge creation.
- **Results depending on solver tolerances** that are not reported.
- **Unpinned dependencies:** a library upgrade changes the default solver.
- **Exchange reactions open by default** in a metabolic model.

## Validation

- `python3 scripts/balance.py --selftest` passes.
- The SBML file passes the official validator (online or libSBML) with units checked.
- The model reproduces the paper's main figure from the deposited files alone.
- MEMOTE (metabolic models) shows no growth without substrates and no energy-generating cycles.
- Falsifier: a second simulator, given the same SBML and SED-ML, producing a different result.

## Expected output

Code or model files in a standard format; the annotation table; the balance report; tests and their
results; a SED-ML or equivalent simulation description; and a repository layout with environment and
deposition plan.

## Sources and confidence

- Hucka et al. 2003, doi:10.1093/bioinformatics/btg015 (SBML); Le Novère et al. 2005, doi:10.1038/nbt1156
  (MIRIAM); Waltemath et al. 2011, doi:10.1186/1752-0509-5-198 (SED-ML) and doi:10.1371/journal.pcbi.1001122
  (MIASE); Ebrahim et al. 2013, doi:10.1186/1752-0509-7-74 (COBRApy); Lieven et al. 2020,
  doi:10.1038/s41587-020-0446-y (MEMOTE); Malik-Sheriff et al., doi:10.1093/nar/gkz1055 (BioModels; Crossref
  dates it 2019 online, 2020 in print). Records checked on Crossref 2026-10-15; tool features from author
  knowledge, VERIFY current versions
- Sauter and Albrecht 2023, doi:10.11647/OBP.0291: the introduction notes that computational scientists look
  for existing software modules and libraries, and calls for reproducible workflows and benchmark datasets
  (supplied text)
