# `reproducible-research-code`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Set up a project layout for an analysis of public sequencing data in Python. Keep raw data read-only, record accessions and checksums, pin the environment, and say where seeds are recorded.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 10,376 | 12,519 |
| Input tokens read across all turns (including cached context) | 253,698 | 495,992 |
| Extra input tokens when the skill is installed | | +242,295 |
| Cost, US dollars at list price | 0.400 | 0.577 |
| Skills invoked in the sample run | none | `reproducible-research-code` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 230 tokens for its name and description, which are in every session where the skill is installed, and about 1,900 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I've set up the project layout in the working directory. **None of it has been run or tested**: running Python needed approval, and that didn't come through.

```
config/config.yaml        all settings: master seed, genome build + annotation release, paths
data/accessions.tsv       one row per input file: accession, study, source, URL, build, licence
data/checksums.sha256     SHA-256 per raw file, in the same format `sha256sum -c` reads
data/download_log.tsv     date, accession and URL of each download
data/raw/  reference/     downloaded files, read-only, kept out of git
data/interim/ processed/  files made from the raw data, can always be rebuilt
src/seqproject/           provenance.py, seeds.py, runrecord.py
scripts/                  fetch_data.py, run_analysis.py
tests/                    test_provenance.py, test_seeds.py
results/<run_id>/         outputs + run_record.json
docs/methods-record.md    methods record template
environment.yml, pyproject.toml, Makefile, .gitignore, README.md
```

**How each requirement is handled:**

- **Raw data is read-only.**
  - `scripts/fetch_data.py` downloads each file listed in `accessions.tsv`, records its checksum and removes write permission.
  - `make verify` fails if any raw file is writable, missing or changed.
  - `run_analysis.py` won't start unless the checksums match.
  - Anything made from the raw data goes to `interim/`, `processed/` or `results/`.
- **Accessions and checksums.**
  - `data/accessions.tsv` holds the accessions and `data/checksums.sha256` holds the checksums. Both are committed to git; the raw files are not.
  - A checksum is recorded once. If a file later doesn't match, that's treated as an error, not a reason to update the record.
- **Pinned environment.**
  - `environment.yml` gives an exact version for every package (Python 3.11.9, numpy, pandas, pysam, biopython, sra-tools, samtools, pytest).
  - `make lock` writes `conda-lock.txt`, the full resolved set with checksums; commit it after the first install.
  - Each run record also lists the installed package versions.
- **Where seeds are recorded.**
  - **Set:** in `seed:` in `config/config.yaml`. `--seed N` overrides it, for checking that results hold across seeds.
  - **Derived:** each random step gets its own named seed from `src/seqproject/seeds.py`, worked out from the master seed and the step's name. Adding a step doesn't change the other steps' seeds, and parallel workers get separate seeds.
  - **Recorded:** `results/<run_id>/run_record.json` stores `master_seed` and `seeds_used`, along with the git commit, config and input checksums. The run folder name also ends in `-seed<N>`. You then copy the seeds into the Steps table in `docs/methods-record.md`.

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
I've set up the project layout in the working directory. I haven't run any of it: my attempt to run the tests was blocked at a permission prompt, and I didn't try downloading real data.

**Layout**
```
config/config.yaml        list of accessions to fetch, plus the master seed
data/raw/                 downloaded data, read-only, not committed to git
data/raw/MANIFEST.tsv     one row per file: accession, URL, size, md5, sha256, download time (committed)
data/{external,interim,processed}/
src/seqproject/           checksums.py, seeds.py
scripts/                  fetch_raw.py, verify_raw.py
runs/<run_id>/run.json    a record of each run (committed)
notebooks/  results/  logs/  tests/
environment.yml  pyproject.toml  Makefile  .gitignore  README.md
```

**Read-only raw data:** only `scripts/fetch_raw.py` writes to `data/raw/`. It downloads FASTQ files from ENA and checks each one's size and MD5 against the values ENA publishes. It then removes write permission from the file. Analysis outputs go to `data/interim/` and `data/processed/`. `make protect` puts the read-only permissions back if they get changed.

**Accessions and checksums:** each downloaded file gets one new row in `data/raw/MANIFEST.tsv`. Rows are only ever added, never changed. Each row has the accession, source URL, size, MD5 (checked against ENA's value), SHA-256 (computed locally) and download time. If a file fails the check, it is deleted and no row is written. `make verify` re-checks every row: the file exists, both checksums still match, and it's still read-only.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
