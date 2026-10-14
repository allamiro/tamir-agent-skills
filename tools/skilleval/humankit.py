"""Blind human grading kit (standard library only).

`sheet` pairs, for each skill, one answer produced with the skill and one without, hides which is which, shuffles the
order with a seed, and writes three files to evals/human/: sheet.md (what a grader reads), ratings-template.csv (what a grader
fills in) and key.json (which side was which; do not give it to graders). `score` reads one or more filled-in
ratings files and reports, per grader, how often the with-skill answer was preferred (with an exact sign test and a
Wilson interval, ties set aside), the mean correctness scores, and, with two or more graders, Cohen's kappa.

The kit is the part of the evaluation that needs a person. Nothing here pretends to be one: a model's verdicts are
produced separately (`pairwise`) and are labelled as a model's.
"""
import csv
import json
import os
import random

from . import stats
from .samples import scrub

COLUMNS = ["id", "better", "a_correct_1to5", "b_correct_1to5", "a_flags_doubt_y_n", "b_flags_doubt_y_n", "notes"]


def make_pairs(records, seed=1):
    """One pair per skill from the first with-skill and first without-skill outcome runs. Returns (items, key)."""
    by = {}
    for r in records:
        if r.get("kind") == "outcome" and r.get("text") and r["run"] == 1:
            by.setdefault(r["key"], {})[r["arm"]] = r
    rng = random.Random(seed)
    items, key = [], {}
    for n, skill in enumerate(sorted(by), 1):
        pair = by[skill]
        if "with" not in pair or "without" not in pair:
            continue
        with_first = rng.random() < 0.5
        a, b = (pair["with"], pair["without"]) if with_first else (pair["without"], pair["with"])
        pid = "P%02d" % n
        items.append({"id": pid, "skill": skill, "a": scrub(a["text"]), "b": scrub(b["text"]), "case": a["case"]})
        key[pid] = {"skill": skill, "a": "with" if with_first else "without", "b": "without" if with_first else "with"}
    rng.shuffle(items)
    return items, key


def write_kit(items, key, prompts, outdir):
    os.makedirs(outdir, exist_ok=True)
    lines = ["# Blind grading sheet", "",
             "For each item, read the prompt and both answers. Do not try to guess which answer used a skill (some answers mention a skill or its files; ignore that), and do not reward length or formatting. "
             "Fill in `ratings-template.csv` (one row per item; copy it and name the copy for yourself).", "",
             "- `better`: A, B or tie, for the answer a specialist would rather receive",
             "- `a_correct_1to5`, `b_correct_1to5`: 1 = wrong or misleading, 3 = partly right, 5 = right and complete for the question asked",
             "- `a_flags_doubt_y_n`, `b_flags_doubt_y_n`: does the answer say what it did not verify, assumed or is unsure about (y or n)",
             "- `notes`: one line on anything a regular expression would miss", ""]
    for it in items:
        lines += ["---", "", "## %s" % it["id"], "", "**Prompt:** %s" % prompts.get(it["skill"], ""), "", "### Answer A", "", it["a"], "", "### Answer B", "", it["b"], ""]
    with open(os.path.join(outdir, "sheet.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(os.path.join(outdir, "ratings-template.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(COLUMNS)
        for it in sorted(items, key=lambda x: x["id"]):
            w.writerow([it["id"], "", "", "", "", "", ""])
    with open(os.path.join(outdir, "key.json"), "w", encoding="utf-8") as fh:
        json.dump(key, fh, indent=1)


def read_ratings(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return [row for row in csv.DictReader(fh)]


def label_for(row, key):
    """'skill', 'baseline', 'tie' or None for one rating row."""
    pid = row.get("id", "").strip()
    better = (row.get("better") or "").strip().lower()
    if pid not in key or better not in ("a", "b", "tie"):
        return None
    if better == "tie":
        return "tie"
    side = key[pid]["a" if better == "a" else "b"]
    return "skill" if side == "with" else "baseline"


def score_rater(rows, key):
    labels = {r["id"]: label_for(r, key) for r in rows if r.get("id") in key}
    wins = sum(1 for v in labels.values() if v == "skill")
    losses = sum(1 for v in labels.values() if v == "baseline")
    ties = sum(1 for v in labels.values() if v == "tie")
    out = {"rated": sum(1 for v in labels.values() if v), "skill_preferred": wins, "baseline_preferred": losses, "ties": ties,
           "sign_test_p": stats.sign_test(wins, losses), "labels": labels}
    lo, hi = stats.wilson(wins, wins + losses)
    out["win_rate_decisive"] = (wins / (wins + losses)) if wins + losses else None
    out["win_rate_ci"] = (lo, hi)
    diffs, flag_s, flag_b, n_flag = [], 0, 0, 0
    for r in rows:
        pid = r.get("id")
        if pid not in key:
            continue
        try:
            a, b = int(r["a_correct_1to5"]), int(r["b_correct_1to5"])
        except (KeyError, ValueError, TypeError):
            continue
        sa, sb = (a, b) if key[pid]["a"] == "with" else (b, a)
        diffs.append(sa - sb)
        fa, fb = (r.get("a_flags_doubt_y_n") or "").strip().lower(), (r.get("b_flags_doubt_y_n") or "").strip().lower()
        if fa in ("y", "n") and fb in ("y", "n"):
            n_flag += 1
            fs, fbase = (fa, fb) if key[pid]["a"] == "with" else (fb, fa)
            flag_s += fs == "y"
            flag_b += fbase == "y"
    out["mean_correctness_difference"] = (sum(diffs) / len(diffs)) if diffs else None
    out["correctness_ci"] = stats.bootstrap_mean(diffs)[1:] if len(diffs) > 1 else None
    out["flags_doubt_skill"], out["flags_doubt_baseline"], out["flag_items"] = flag_s, flag_b, n_flag
    return out


def agreement(raters):
    """Cohen's kappa between each pair of raters on the items both rated: {(i, j): (kappa, n)}."""
    res = {}
    for i in range(len(raters)):
        for j in range(i + 1, len(raters)):
            common = [k for k in raters[i]["labels"] if raters[i]["labels"][k] and raters[j]["labels"].get(k)]
            if len(common) >= 2:
                res[(i, j)] = (stats.cohen_kappa([raters[i]["labels"][k] for k in common], [raters[j]["labels"][k] for k in common]), len(common))
    return res


def render_score(names, raters):
    lines = ["| Grader | Items rated | Skill preferred | Baseline preferred | Ties | Share preferring the skill (95% interval) | Sign test p | Correctness, skill minus baseline | States doubt: skill / baseline |",
             "|---|---|---|---|---|---|---|---|---|"]
    for n, r in zip(names, raters):
        wr = "n/a" if r["win_rate_decisive"] is None else "%.0f%% (%.0f-%.0f)" % (100 * r["win_rate_decisive"], 100 * r["win_rate_ci"][0], 100 * r["win_rate_ci"][1])
        cd = "n/a" if r["mean_correctness_difference"] is None else "%+.2f" % r["mean_correctness_difference"]
        lines.append("| %s | %d | %d | %d | %d | %s | %.3f | %s | %d / %d of %d |" % (n, r["rated"], r["skill_preferred"], r["baseline_preferred"], r["ties"], wr,
                                                                                    r["sign_test_p"], cd, r["flags_doubt_skill"], r["flags_doubt_baseline"], r["flag_items"]))
    ag = agreement(raters)
    if ag:
        lines.append("")
        for (i, j), (k, n) in sorted(ag.items()):
            lines.append("Agreement between %s and %s: Cohen's kappa %.2f on %d items." % (names[i], names[j], k, n))
    return "\n".join(lines) + "\n"


def main(args):
    col = os.path.abspath(args.collection)
    outdir = os.path.join(col, "evals", "human")
    if args.cmd == "sheet":
        path = os.path.join(col, "evals", "runs", "latest-outcome.json")
        if not os.path.isfile(path):
            raise SystemExit("no saved outcome runs: run `run --kind outcome` first")
        recs = json.load(open(path, encoding="utf-8"))["records"]
        from . import cases as cases_mod
        data = cases_mod.load_cases(col)
        prompts = {c["skill"]: cases_mod.resolve_outcome(col, c)[0] for c in data["outcome"]}
        items, key = make_pairs(recs, args.seed)
        write_kit(items, key, prompts, outdir)
        print("wrote %d blind pairs to %s (give graders sheet.md and ratings-template.csv, not key.json)" % (len(items), outdir))
        return 0
    key = json.load(open(os.path.join(outdir, "key.json"), encoding="utf-8"))
    if not args.ratings:
        raise SystemExit("give --ratings FILE [FILE ...]")
    raters = [score_rater(read_ratings(p), key) for p in args.ratings]
    text = render_score([os.path.splitext(os.path.basename(p))[0] for p in args.ratings], raters)
    print(text)
    with open(os.path.join(col, "evals", "results", "human.md"), "w", encoding="utf-8") as fh:
        fh.write("# Human grading results\n\n" + text)
    return 0


def selftest():
    import tempfile
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    recs = []
    for skill in ("alpha", "beta", "gamma", "delta"):
        for arm in ("with", "without"):
            recs.append({"kind": "outcome", "key": skill, "case": "outcome-" + skill, "arm": arm, "run": 1, "text": "%s %s answer" % (skill, arm)})
            recs.append({"kind": "outcome", "key": skill, "case": "outcome-" + skill, "arm": arm, "run": 2, "text": "second run"})
    recs.append({"kind": "outcome", "key": "empty", "case": "outcome-empty", "arm": "with", "run": 1, "text": ""})
    recs.append({"kind": "trigger", "key": "t", "case": "trigger-t", "arm": "with", "run": 1, "text": "x"})
    items, key = make_pairs(recs, seed=3)
    eq("one pair per skill with text", len(items), 4)
    eq("ids unique", len({i["id"] for i in items}), 4)
    ok = all(items_i["a"].split()[1] == key[items_i["id"]]["a"] and items_i["b"].split()[1] == key[items_i["id"]]["b"] for items_i in items)
    eq("key matches placement", ok, True)
    eq("each pair has one of each arm", all(sorted([key[i]["a"], key[i]["b"]]) == ["with", "without"] for i in key), True)
    eq("deterministic", make_pairs(recs, seed=3)[1], key)
    eq("placement is mixed over many seeds", len({tuple(sorted((k, v["a"]) for k, v in make_pairs(recs, s)[1].items())) for s in range(1, 30)}) > 1, True)

    # a fixed key to score against
    k = {"P01": {"skill": "s1", "a": "with", "b": "without"}, "P02": {"skill": "s2", "a": "without", "b": "with"},
         "P03": {"skill": "s3", "a": "with", "b": "without"}, "P04": {"skill": "s4", "a": "without", "b": "with"}}
    rows = [{"id": "P01", "better": "A", "a_correct_1to5": "5", "b_correct_1to5": "3", "a_flags_doubt_y_n": "y", "b_flags_doubt_y_n": "n"},
            {"id": "P02", "better": "B", "a_correct_1to5": "2", "b_correct_1to5": "4", "a_flags_doubt_y_n": "n", "b_flags_doubt_y_n": "y"},
            {"id": "P03", "better": "tie", "a_correct_1to5": "4", "b_correct_1to5": "4", "a_flags_doubt_y_n": "y", "b_flags_doubt_y_n": "y"},
            {"id": "P04", "better": "A", "a_correct_1to5": "3", "b_correct_1to5": "3", "a_flags_doubt_y_n": "n", "b_flags_doubt_y_n": "n"}]
    eq("label with-skill A", label_for(rows[0], k), "skill")
    eq("label with-skill B", label_for(rows[1], k), "skill")
    eq("label tie", label_for(rows[2], k), "tie")
    eq("label baseline", label_for(rows[3], k), "baseline")
    eq("label bad value", label_for({"id": "P01", "better": "maybe"}, k), None)
    eq("label unknown id", label_for({"id": "P99", "better": "A"}, k), None)
    sc = score_rater(rows, k)
    eq("counts", (sc["rated"], sc["skill_preferred"], sc["baseline_preferred"], sc["ties"]), (4, 2, 1, 1))
    eq("sign test p", round(sc["sign_test_p"], 4), round(stats.sign_test(2, 1), 4))
    eq("mean correctness difference", sc["mean_correctness_difference"], ((5 - 3) + (4 - 2) + 0 + (3 - 3)) / 4.0)
    eq("flags counted per arm", (sc["flags_doubt_skill"], sc["flags_doubt_baseline"], sc["flag_items"]), (3, 1, 4))
    rows2 = [dict(r) for r in rows]
    rows2[0]["better"] = "B"
    a2 = score_rater(rows2, k)
    ag = agreement([sc, a2])
    eq("kappa available for two graders", list(ag), [(0, 1)])
    eq("kappa is below 1 when graders differ", ag[(0, 1)][0] < 1.0, True)
    eq("kappa 1 for identical graders", agreement([sc, sc])[(0, 1)][0], 1.0)
    text = render_score(["r1", "r2"], [sc, a2])
    eq("render has both graders", "| r1 |" in text and "| r2 |" in text and "Cohen's kappa" in text, True)
    with tempfile.TemporaryDirectory() as tmp:
        write_kit(items, key, {"alpha": "Prompt text"}, tmp)
        eq("kit files", sorted(os.listdir(tmp)), ["key.json", "ratings-template.csv", "sheet.md"])
        sheet = open(os.path.join(tmp, "sheet.md")).read()
        eq("sheet shows answers as A and B and never the arm labels", "### Answer A" in sheet and "### Answer B" in sheet and "arm:" not in sheet and "key" not in sheet.lower().replace("keys", ""), True)
        rows_t = read_ratings(os.path.join(tmp, "ratings-template.csv"))
        eq("template has one empty row per item", (len(rows_t), rows_t[0]["better"]), (4, ""))
    return fails, count[0]
