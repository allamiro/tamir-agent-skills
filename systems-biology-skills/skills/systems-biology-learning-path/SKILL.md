---
name: systems-biology-learning-path
description: Plans and supports learning systems biology, for students, self-learners and teachers, following the Sauter and Albrecht workbook's four parts (network matrices and linear algebra, metabolic modelling, dynamics and control, physical modelling and enzyme kinetics) and its prioritised checklist, with evidence-based study advice (self-efficacy, deliberate practice, elaboration, learning from mistakes, study groups of three to five), the four kinds of knowledge (declarative, procedural, contextual, conceptual), flipped-classroom teaching, and bridging biology and mathematics backgrounds. Use for "I want to learn systems biology", "make me a study plan", "explain eigenvalues to a biologist", "quiz me on stoichiometric matrices", "how should I study the maths", "design a flipped-classroom course", "what should I learn first". Use the topic skills for the content itself and quantitative-research-methods to evaluate a course.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Systems biology learning path

## Purpose and activation

Systems biology draws people from biology, mathematics, physics, engineering and computing, and each
group finds a different half of it hard. The workbook this collection draws on organises the subject in
four parts with prioritised topics and pairs them with study advice grounded in educational research.
This skill turns that into a personal plan, practice and feedback. Activate when the user wants to learn
or teach the subject, asks for a study plan, an explanation pitched to their background, or practice.

## Required inputs

The learner's background (biology, mathematics, physics, engineering, computing, medicine) and current
level; the goal (course exam, research project, reading papers, teaching); the time available; and which
topics are already known.

## Workflow

1. **Place the learner** with a short diagnostic of a few items per part (for example rank of a matrix,
   writing a balance, reading a phase portrait, Michaelis–Menten parameters).
2. **Build the plan** from the checklist in `references/checklist-map.md`: priority 1 topics first in each
   part, in the order Part 1 to Part 4, then priority 2 and 3 as the goal requires. Use
   `assets/templates/study-plan.md`.
3. **For each topic, aim at four kinds of knowledge:** what it is (declarative), how to do it (procedural),
   when to use it (contextual), and why it works (conceptual). Ask the matching questions from the checklist.
4. **Practise more than you read:** the workbook estimates that concepts take about a fifth to a third of the
   time and solving problems the rest. Set problems, have the learner try first, then give feedback; reveal
   worked solutions only after a real attempt.
5. **Use the scripts as answer checkers,** not as replacements for working by hand: for example
   `linear-algebra-networks` for a rank or eigenvalue, `stoichiometric-networks` for a null space. The 28
   worked exercises in `references/exercises.md` each have a command and the expected output.
6. **Target weaknesses** with deliberate practice on the hardest subtask, and connect each new idea to what the
   learner already knows (elaboration) rather than repeating it.
7. **Treat mistakes as information:** analyse sign errors and misconceptions, and revisit them later.
8. **Bridge backgrounds** with `references/study-strategies.md`: biologists build mathematical fluency by
   practice; mathematicians and engineers need the biological detail that decides which model is sensible.
9. **For teachers,** design flipped-classroom sessions: preparation before class (reading, short videos with
   stated objectives), class time for problem solving and discussion, and clear objectives and priorities.

## Decision framework

| Learner | Start with | Watch for |
|---|---|---|
| Biologist new to maths | Part 1 priority 1 (matrix operations, rank, eigenvalues), with biological examples | Giving up during the slow early phase of practice |
| Mathematician or engineer | Biology of the pathway, then Part 2 and Part 3 | Models that ignore biological detail |
| Computer scientist | Parts 3 and 4 concepts (balances, kinetics), with code | Running tools without checking units or assumptions |
| Medical student | Systems medicine framing, Part 2 and PK | Time pressure; prioritise the checklist |
| Teacher | Flipped-classroom design, objectives, priorities | Covering everything instead of practice time |

## Failure and edge cases

- **Reading solutions before trying,** which builds familiarity, not skill.
- **Repeating easy problems,** which feels productive but does not improve performance.
- **Skipping the conceptual question** (why a method works), so the method cannot be adapted.
- **Mistaking the slow early phase for inability;** performance often rises suddenly after enough practice.
- **Group work where the fastest member solves everything.** Each member should try first and explain at the end.
- **Effect sizes from educational research quoted as guarantees** for an individual learner.

## Validation

- The plan covers every priority 1 topic needed for the goal.
- Each topic has at least one problem solved by hand and checked with a script or worked solution.
- The diagnostic repeated after the plan shows progress on the topics practised.
- Falsifier: the learner can execute a procedure but cannot say when to use it or why it works.

## Expected output

The placement result; a study plan by part, priority and week; problems with feedback; explanations pitched
to the learner's background; and, for teachers, a session plan with objectives.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291 (supplied text): the four parts and prioritised checklist;
  the four kinds of knowledge with the determinant example; study advice (try problems before solutions,
  iterate between theory and problems, study groups of three to five of similar level, deliberate practice,
  elaboration, learning from mistakes, Cornell notes, Grow's stages of self-directed learning); and effect
  sizes quoted from Schneider and Mustafić (2015) and Freeman et al. 2014, doi:10.1073/pnas.1319030111
  (record checked on Crossref 2026-10-15)
- Effect sizes are as the workbook reports them; the primary sources were not read, VERIFY before quoting
