"""Sample outputs and token counts for a collection's README (standard library only).

Reads the saved outcome runs, writes one examples/<skill>.md per skill (the starter prompt, the token numbers with and
without the skill, and excerpts of a real answer from each arm), and rewrites the block between the
<!-- samples:start --> and <!-- samples:end --> markers in the collection README. Skill sizes come from
`claude plugin details`, which is Claude Code's own estimate of what a skill adds to a session.
"""
import json
import os
import re
import subprocess
import tempfile
from statistics import mean

from . import cases as cases_mod

START, END = "<!-- samples:start -->", "<!-- samples:end -->"


def _num(tok):
    tok = tok.strip().lstrip("~").replace(",", "")
    if tok.lower().endswith("k"):
        return int(round(float(tok[:-1]) * 1000))
    return int(float(tok))


def parse_details(text):
    """{'skills': {name: (always_on, on_invoke)}, 'always_on_total': int} from `claude plugin details` output."""
    out = {"skills": {}, "always_on_total": None}
    m = re.search(r"Always-on:\s*~?([\d,.]+k?)", text)
    if m:
        out["always_on_total"] = _num(m.group(1))
    in_table = False
    for line in text.splitlines():
        if re.match(r"\s*component\s+always-on\s+on-invoke", line):
            in_table = True
            continue
        if in_table:
            m = re.match(r"\s*([a-z0-9-]+)\s+~?([\d,.]+k?)\s+~?([\d,.]+k?)\s*$", line)
            if m:
                out["skills"][m.group(1)] = (_num(m.group(2)), _num(m.group(3)))
            elif line.strip() == "":
                if out["skills"]:
                    break
    return out


def skill_sizes(collection):
    collection = os.path.abspath(collection)
    name = os.path.basename(collection)
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, ".claude-plugin"))
        json.dump({"name": name, "version": "0.0.0", "description": "size probe"}, open(os.path.join(tmp, ".claude-plugin", "plugin.json"), "w"))
        os.symlink(os.path.join(collection, "skills"), os.path.join(tmp, "skills"))
        r = subprocess.run(["claude", "--plugin-dir", tmp, "plugin", "details", name], capture_output=True, text=True, timeout=120)
    return parse_details(r.stdout)


TEMP_PATH = re.compile(r"/(?:private/)?(?:tmp|var/folders)/[^\s`'\"<>)\]]+")


def scrub(text):
    """Replace the throwaway folders the test runs used (they mean nothing to a reader) with a placeholder."""
    text = TEMP_PATH.sub("<temporary path>", text).replace("\t", "    ")
    return re.sub(r"\n{3,}", "\n\n", text)


def _version(meta):
    return str(meta.get("claudeVersion", "?")).replace(" (Claude Code)", "")


def excerpt(text, limit):
    """Cut at a paragraph or line boundary at or before `limit` characters and mark the cut."""
    text = scrub(text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    for sep in ("\n\n", "\n", ". "):
        i = cut.rfind(sep)
        if i > limit * 0.5:
            cut = cut[:i]
            break
    return cut.rstrip() + "\n\n[... excerpt ends; the full answer is longer]"


def _fence(text):
    fence = "````"
    return "%stext\n%s\n%s" % (fence, text, fence)


def pick(runs):
    """The run whose output tokens are closest to the mean, preferring runs that passed the rubric."""
    good = [r for r in runs if r["graders"].get("rubric", {}).get("passed")] or runs
    target = mean(r["out_tokens"] for r in runs)
    return min(good, key=lambda r: abs(r["out_tokens"] - target))


def collect(records):
    by = {}
    for r in records:
        if r.get("kind") == "outcome":
            by.setdefault(r["key"], {"with": [], "without": []})[r["arm"]].append(r)
    rows = {}
    for skill, arms in by.items():
        if not arms["with"] or not arms["without"]:
            continue
        m = lambda rs, f: mean(x[f] for x in rs)
        rows[skill] = {
            "n_with": len(arms["with"]), "n_without": len(arms["without"]),
            "out_with": m(arms["with"], "out_tokens"), "out_without": m(arms["without"], "out_tokens"),
            "in_with": m(arms["with"], "in_tokens"), "in_without": m(arms["without"], "in_tokens"),
            "cost_with": m(arms["with"], "cost"), "cost_without": m(arms["without"], "cost"),
            "pick_with": pick(arms["with"]), "pick_without": pick(arms["without"]),
        }
    return rows


def example_md(skill, prompt, row, size, meta):
    a, b = row["pick_with"], row["pick_without"]
    lines = ["# `%s`: a sample answer" % skill, "",
             "A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). "
             "The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over %d runs with the skill and %d without." % (row["n_with"], row["n_without"]), "",
             "## Prompt", "", "> " + scrub(prompt).replace("\n", "\n> "), "", "## Tokens", "",
             "| | Without the skill | With the skill |", "|---|---|---|",
             "| Output tokens (what the model wrote, including its reasoning) | {:,.0f} | {:,.0f} |".format(row["out_without"], row["out_with"]),
             "| Input tokens read across all turns (including cached context) | {:,.0f} | {:,.0f} |".format(row["in_without"], row["in_with"]),
             "| Extra input tokens when the skill is installed | | {:+,.0f} |".format(row["in_with"] - row["in_without"]),
             "| Cost, US dollars at list price | %.3f | %.3f |" % (row["cost_without"], row["cost_with"]),
             "| Skills invoked in the sample run | %s | %s |" % (", ".join(sorted(set(b["skills"]))) or "none", ", ".join("`%s`" % s for s in sorted(set(a["skills"]))) or "none"), ""]
    if size:
        lines += ["Size of the skill by Claude Code's own estimate (`claude plugin details`): about {:,} tokens for its name and description, which are in every session where the skill is installed, "
                  "and about {:,} tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.".format(size[0], size[1]), ""]
    lines += ["## Answer with the skill (excerpt)", "", _fence(excerpt(a["text"], 3200)), "",
              "## Answer without the skill (excerpt)", "", _fence(excerpt(b["text"], 1600)), "",
              "Agent model %s, Claude Code %s. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md)." % (
                  meta.get("agent_model", "?"), _version(meta)), ""]
    return "\n".join(lines)


def readme_block(rows, sizes, feature, prompts, meta, examples_dir="examples"):
    n_with = max(r["n_with"] for r in rows.values())
    n_without = max(r["n_without"] for r in rows.values())
    lines = [START, "", "## Sample outputs and token cost", "",
             "Every skill has one real answer in [`%s/`](%s/), with the prompt that produced it. The table has the numbers behind those answers: means over "
             "%d runs with the skills installed and %d without (Claude Code %s, model %s). **Output tokens** is what the model wrote, including its reasoning. "
             "**Extra input tokens** is how many more tokens the model read across all turns when the skills were installed (the skill text it loaded, reference files, "
             "script output and extra turns); the large base context is the same in both arms and is left out. **Skill size** is Claude Code's own projected cost from "
             "`claude plugin details`: the first figure is in every session for every installed skill (its name and description), the second only when the skill is used. "
             "When the skill was not invoked in a run, the extra is only the descriptions of the installed skills, so the smallest figure in the table is the cost of having the collection installed. "
             "More tokens is not a defect by itself; what the tokens buy is in [`evals/`](evals/)." % (
                 examples_dir, examples_dir, n_with, n_without, _version(meta), meta.get("agent_model", "?")), "",
             "| Skill | Output tokens, no skill to skill | Extra input tokens | Cost, no skill to skill (US dollars) | Skill size, always / when used | Sample |",
             "|---|---|---|---|---|---|"]
    for skill in sorted(rows):
        r = rows[skill]
        size = sizes.get(skill)
        lines.append("| `%s` | {:,.0f} to {:,.0f} | {:+,.0f} | %.2f to %.2f | %s | [answer](%s/%s.md) |".format(
            r["out_without"], r["out_with"], r["in_with"] - r["in_without"]) % (
            skill, r["cost_without"], r["cost_with"], ("~{:,} / ~{:,}".format(*size) if size else "n/a"), examples_dir, skill))
    if feature in rows:
        a = rows[feature]["pick_with"]
        lines += ["", "### One answer in full: `%s`" % feature, "", "Prompt:", "", "> " + scrub(prompts[feature]).replace("\n", "\n> "), "",
                  "Answer with the skill (excerpt of a single run; the same prompt without the skill is on the [sample page](%s/%s.md)):" % (examples_dir, feature), "",
                  _fence(excerpt(a["text"], 2600)), ""]
    lines += [END]
    return "\n".join(lines)


def splice(readme, block):
    if START in readme and END in readme:
        a = readme.index(START)
        b = readme.index(END) + len(END)
        return readme[:a] + block + readme[b:]
    marker = "\n## Check it"
    if marker not in readme:
        raise ValueError("README has no '## Check it' heading to insert before")
    i = readme.index(marker)
    return readme[:i].rstrip("\n") + "\n\n" + block + "\n" + readme[i:]


def main(args):
    col = os.path.abspath(args.collection)
    path = os.path.join(col, "evals", "runs", "latest-outcome.json")
    if not os.path.isfile(path):
        raise SystemExit("no saved outcome runs: run `run --kind outcome` first")
    saved = json.load(open(path, encoding="utf-8"))
    rows = collect(saved["records"])
    data = cases_mod.load_cases(col)
    prompts = {c["skill"]: cases_mod.resolve_outcome(col, c)[0] for c in data["outcome"]}
    sizes = skill_sizes(col)["skills"]
    exdir = os.path.join(col, "examples")
    os.makedirs(exdir, exist_ok=True)
    for skill, row in rows.items():
        with open(os.path.join(exdir, skill + ".md"), "w", encoding="utf-8") as fh:
            fh.write(example_md(skill, prompts[skill], row, sizes.get(skill), saved["meta"]))
    readme_path = os.path.join(col, "README.md")
    readme = open(readme_path, encoding="utf-8").read()
    feature = args.feature or sorted(rows)[0]
    block = readme_block(rows, sizes, feature, prompts, saved["meta"])
    open(readme_path, "w", encoding="utf-8").write(splice(readme, block))
    print("wrote %d example pages and the README sample section (featured: %s)" % (len(rows), feature))
    return 0


DETAILS_SAMPLE = """egyptology-skills 0.1.0

Projected token cost
  Always-on:   ~1,021 tok   added to every session

Per-component (rounded)
  component               always-on  on-invoke
  hieroglyph-app-builder       ~220      ~1.8k
  transliteration              ~220        ~2k
  gardiner-sign-lookup         ~190      ~1.8k

  On-invoke cost is paid each time a skill or agent fires.
"""


def selftest():
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    d = parse_details(DETAILS_SAMPLE)
    eq("always-on total", d["always_on_total"], 1021)
    eq("component rows", d["skills"], {"hieroglyph-app-builder": (220, 1800), "transliteration": (220, 2000), "gardiner-sign-lookup": (190, 1800)})
    eq("num k", (_num("~1.8k"), _num("~2k"), _num("~220"), _num("1,021")), (1800, 2000, 220, 1021))
    eq("excerpt short text untouched", excerpt("short", 100), "short")
    eq("temporary paths are scrubbed", scrub("saved to `/private/tmp/claude-501/-x/scratchpad/a.json` and /var/folders/nk/z8/T/skilleval-ab/f.py)"),
       "saved to `<temporary path>` and <temporary path>)")
    eq("tabs and runs of blank lines are tidied", scrub("a\tb\n\n\n\nc"), "a    b\n\nc")
    eq("ordinary paths are kept", scrub("see scratchpad/record.json and /usr/bin/python3"), "see scratchpad/record.json and /usr/bin/python3")
    long = "para one is here.\n\npara two is here and longer.\n\npara three"
    e = excerpt(long, 45)
    eq("excerpt cuts at a paragraph", e.startswith("para one is here.\n\npara two is here and longer.") or e.startswith("para one is here."), True)
    eq("excerpt marks the cut", e.endswith("[... excerpt ends; the full answer is longer]"), True)

    def rec(arm, run, out, inp, cost, text, rubric=True, skills=()):
        return {"kind": "outcome", "key": "alpha", "arm": arm, "run": run, "out_tokens": out, "in_tokens": inp, "cost": cost, "text": text,
                "skills": list(skills), "graders": {"rubric": {"passed": rubric}}}
    recs = [rec("with", 1, 100, 5000, 0.2, "w1", True, ["alpha"]), rec("with", 2, 300, 7000, 0.4, "w2", True, ["alpha"]), rec("with", 3, 200, 6000, 0.3, "w3", False, ["alpha"]),
            rec("without", 1, 50, 1000, 0.1, "b1", False), rec("without", 2, 70, 1200, 0.12, "b2", False)]
    rows = collect(recs)
    r = rows["alpha"]
    eq("means", (r["out_with"], r["out_without"], r["in_with"], r["in_without"]), (200, 60, 6000, 1100))
    eq("pick prefers a rubric pass near the mean", r["pick_with"]["text"] in ("w1", "w2"), True)
    eq("pick baseline closest to mean", r["pick_without"]["text"] in ("b1", "b2"), True)
    md = example_md("alpha", "Do the thing.", r, (190, 1800), {"agent_model": "m", "claudeVersion": "1"})
    eq("example has token rows", "| Output tokens" in md and "+4,900" in md, True)
    eq("example quotes the prompt", "> Do the thing." in md, True)
    eq("example mentions skill size", "about 190 tokens" in md and "1,800" in md, True)
    block = readme_block(rows, {"alpha": (190, 1800)}, "alpha", {"alpha": "Do the thing."}, {"agent_model": "m", "claudeVersion": "1"})
    eq("block row", "| `alpha` | 60 to 200 | +4,900 | 0.11 to 0.30 | ~190 / ~1,800 | [answer](examples/alpha.md) |" in block, True)
    eq("block has markers", block.startswith(START) and block.endswith(END), True)
    readme = "# T\n\nintro\n\n## Check it\n\ncommands\n"
    s1 = splice(readme, block)
    eq("splice inserts before Check it", s1.index(START) < s1.index("## Check it"), True)
    block2 = block.replace("60 to 200", "61 to 201")
    s2 = splice(s1, block2)
    eq("splice replaces in place", (s2.count(START), "61 to 201" in s2, "60 to 200" in s2), (1, True, False))
    try:
        splice("# no heading", block)
        fails.append("splice without a heading should raise")
    except ValueError:
        pass
    count[0] += 1
    return fails, count[0]
