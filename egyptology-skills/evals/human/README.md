# Human grading

This is the one check that needs a person. If you are asked to grade, you need an Egyptologist who reads Middle Egyptian, and about 8 pairs, about 1 hour.

1. Open `sheet.md`. Each item has a prompt and two answers, A and B. One used a skill and one did not; you are not told which, and some answers mention a skill or its files, which you should ignore.
2. Copy `ratings-template.csv`, name the copy for yourself (for example `ratings-ann.csv`), and fill one row per item: `better` (A, B or tie), a 1 to 5 correctness score for each answer, whether each answer says what it did not verify (y or n), and a note.
3. Do not open `key.json`; it says which side was which. The repository owner runs `python3 tools/run_evals.py score egyptology-skills --ratings ratings-ann.csv` from the repository root and gets the share of items where the skill was preferred, a sign test, correctness differences, and agreement between graders if two or more people grade.

Grade independently if more than one person is grading, and do not compare notes until the files are handed in.
