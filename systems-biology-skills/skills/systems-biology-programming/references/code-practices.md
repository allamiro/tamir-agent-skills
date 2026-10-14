# Code practices for models

- One model file in a standard format is the source of truth; code reads it rather than re-typing equations.
- Pin versions (requirements file with exact versions, or a container); record the solver and its tolerances.
- Fix random seeds and record them with the output.
- Separate model, parameters, simulation settings and plotting, so each can be checked alone.
- Test: a known steady state, a conservation law that must hold, mass balance, a known knockout, and the
  behaviour at zero input.
- Make the main figures from a single command; never edit numbers by hand after the script.
- Keep raw data read-only; write derived data to a separate folder.
- Use relative paths and a README that says how to run everything.
- Follow FAIR principles for data (findable, accessible, interoperable, reusable) and the ten simple rules for
  reproducible computational research.

Sources: Wilkinson et al. 2016, doi:10.1038/sdata.2016.18; Sandve et al. 2013, doi:10.1371/journal.pcbi.1003285
(records checked on Crossref 2026-10-15; content from author knowledge, VERIFY).
