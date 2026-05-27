# Protocol Validation

`scripts/validate_protocol.py` is the local oracle for prompt-protocol maintenance. Run it after editing `SKILL.md`, prompt files, installation behavior, or protocol-facing docs.

## Commands

```bash
python3 scripts/validate_protocol.py
python3 scripts/validate_protocol.py --self-test
python3 scripts/validate_protocol.py --research-state .agent-log/<timestamp>-research
```

The normal mode validates the current repository. The self-test mode checks that known bad protocol snippets are still rejected. The research-state mode validates a final e-research state directory before handoff.

## What It Checks

- `install.sh` shell syntax.
- `git diff --check` whitespace errors.
- Skill and prompt frontmatter shape.
- `SKILL.md` `name` values matching their skill directory names.
- HTML parser smoke checks for docs.
- Installation smoke test in a temporary `HOME`.
- Known protocol residuals, including stale state paths, old placeholders, and old recommendation labels.
- `e-think` downstream pack names and agreement between frontmatter `next:` values and JSON `downstream_pack` examples.
- `e-build` verification report template sections for commands, evidence, and residual risks.
- Final e-research artifact completeness when `--research-state` is provided, including `experiment-N.md` / `experiment-N-results.md` pairs.

## What It Does Not Prove

- It does not prove that a prompt's reasoning strategy is correct.
- It does not benchmark downstream agent behavior.
- It does not catch every possible natural-language contradiction.
- It does not replace e-think evidence review after a real build or research run.
- `--research-state` is final-stage oriented; it will fail while a new experiment design exists but its result file has not been written yet.

## Extending The Oracle

Add a check when a protocol failure is:

- repeated across files,
- easy to recognize structurally,
- likely to cause false success, broken routing, or installation drift,
- and cheap to verify locally.

Prefer narrow checks with self-test fixtures. If a rule causes false failures on valid prose, narrow the pattern instead of weakening the whole validator.
