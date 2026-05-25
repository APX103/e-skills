# Hermes Install Guide for e-research

This document is written for a Hermes agent that has been asked to install the `e-research` skill from this repository.

## Goal

Install the `e-research` skill so Hermes can load it as `/e-research`.

The skill lives at:

```text
skills/e-research/SKILL.md
```

The skill name in frontmatter is:

```yaml
name: e-research
```

Do not install or call it as `research`. That was the old name.

## Recommended Install

Use Hermes' direct single-skill install command:

```bash
hermes skills install APX103/e-skills/skills/e-research
```

Expected result:

```text
~/.hermes/skills/e-research/SKILL.md
```

Then use it:

```text
/e-research 研究一下长任务知识生产如何做证据闭环
```

## Alternative: Tap Install

If direct install is unavailable, add this repository as a tap:

```bash
hermes skills tap add APX103/e-skills
hermes skills install APX103/e-skills/e-research
```

Hermes tap defaults expect skills under the repository's `skills/` directory. This repository matches that layout.

## Alternative: Clone Then Install

If Hermes has cloned this repository locally:

```bash
git clone https://github.com/APX103/e-skills.git
cd e-skills
./install.sh update
```

The installer links all repository skills into common agent skill directories, including:

```text
~/.hermes/skills/e-research
~/.claude/skills/e-research
~/.codex/skills/e-research
~/.agents/skills/e-research
```

## Verify

Check the installed file:

```bash
test -f ~/.hermes/skills/e-research/SKILL.md
```

Inspect the frontmatter:

```bash
sed -n '1,12p' ~/.hermes/skills/e-research/SKILL.md
```

You should see:

```yaml
name: e-research
```

In Hermes, verify the slash command:

```text
/e-research
```

or ask:

```text
What skills do you have?
```

## Troubleshooting

### `/research` does not work

Use `/e-research`. The skill was renamed.

### `~/.hermes/skills/research` exists

That is stale. Remove it if it points to this repository:

```bash
rm ~/.hermes/skills/research
```

Then install again:

```bash
hermes skills install APX103/e-skills/skills/e-research
```

### `hermes skills install APX103/e-skills` installs nothing useful

That points at the repository, not the skill directory. Use the full skill path:

```bash
hermes skills install APX103/e-skills/skills/e-research
```

or use the tap flow:

```bash
hermes skills tap add APX103/e-skills
hermes skills install APX103/e-skills/e-research
```

### Hermes cloned the repo but still cannot see the skill

From the repo root, run:

```bash
./install.sh update
```

Then check:

```bash
test -f ~/.hermes/skills/e-research/SKILL.md
```

If using Hermes external skill directories instead of symlinks, configure `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - /absolute/path/to/e-skills/skills
```

Restart Hermes or start a new session after changing skill directories.

## Why This Matters

Hermes discovers skills by scanning skill directories for `SKILL.md`. Installed skills become slash commands using their skill name. This repository's research workflow skill is named `e-research`, so installation paths, frontmatter, and slash command must all agree.
