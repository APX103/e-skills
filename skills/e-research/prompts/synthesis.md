# Research Synthesis Prompt

Produce an evidence-backed research report.

## Input

- Charter: read `{state_dir}/charter.md`
- Evidence ledger: read `{state_dir}/evidence-ledger.md`
- Experiment results: read all `{state_dir}/experiment-*-results.md`
- Additional notes: `{notes}`

## Instructions

1. Answer the research question directly.
2. For each important claim, cite the supporting evidence file or mark it as unknown.
3. Separate findings from interpretations.
4. Include negative and inconclusive results.
5. State confidence and limitations.
6. Extract reusable knowledge in compact form.
7. Recommend the next action only if it follows from the evidence.

## Output

Write `{state_dir}/report.md`:

```markdown
# Research Report

## Answer
[direct answer with confidence level]

## Key Claims
| Claim | Evidence | Confidence | Notes |
|---|---|---|---|

## Findings
[evidence-backed findings]

## Interpretations
[reasoned explanations, clearly marked]

## Negative / Inconclusive Results
[what did not work or remains unknown]

## Limitations
[scope and evidence limits]

## Next Action
[optional, evidence-driven]
```

Write `{state_dir}/knowledge.md`:

```markdown
# Reusable Knowledge

- [portable learning]
- [method that worked or failed]
- [risk or pitfall to remember]
```
