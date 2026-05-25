# Research Charter Prompt

Create a research charter for a long-running knowledge production task.

## Input

- User request: `{request}`
- State directory: `{state_dir}`
- Known context: `{context}`

## Instructions

1. Restate the research question in one precise sentence.
2. List what is already known, separating verified facts from assumptions.
3. Define 1-5 hypotheses or subquestions.
4. Define acceptable research methods: reading, source search, code inspection, prototype, benchmark, simulation, proof sketch, interview, or other.
5. Define evidence standards:
   - what would support each hypothesis
   - what would falsify each hypothesis
   - what would remain inconclusive
6. Define autonomy boundaries and human gates.
7. Define stop conditions.
8. Define final outputs.

## Output

Write `{state_dir}/charter.md`:

```markdown
# Research Charter

## Research Question
[one precise question]

## Background
- Verified facts:
- Assumptions:

## Hypotheses / Subquestions
1. ...

## Methods
[allowed methods and why]

## Evidence Standards
| Hypothesis | Support | Falsification | Inconclusive |
|---|---|---|---|

## Autonomy Boundaries
[what the agent may do without asking; what requires approval]

## Stop Conditions
[when to stop, pivot, or ask the user]

## Final Outputs
[report, code, benchmark, notes, knowledge file, etc.]
```
