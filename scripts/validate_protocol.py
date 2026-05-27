#!/usr/bin/env python3
"""Validate prompt-protocol invariants for engineer_skills."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAMES = ("e-build", "e-think", "e-research")
INSTALL_TARGETS = (
    ".claude/skills",
    ".codex/skills",
    ".hermes/skills",
    ".agents/skills",
)
E_THINK_PACKS = {
    "verify-success",
    "verify-failure",
    "root-cause",
    "main-contradiction",
    "next-experiment",
    "reproduce",
    "red-team",
    "second-order-effects",
    "investigation",
    "evidence-strength",
    "assumption-surfacing",
}
E_BUILD_RECOMMENDATIONS = {
    "continue-fixing",
    "narrow-scope",
    "re-verify",
    "proceed",
    "deep-analysis",
}
TERMINALS = {"done"}
RESIDUAL_PATTERNS = {
    "research template described as state target": r"Then fill `prompts/charter\.md`",
    "direct Phase 6 proceed recommendation": r"\*\*proceed\*\*: Success is genuine, proceed to Phase 6 Knowledge Extraction",
    "old iteration_number placeholder": r"\{iteration_number\}",
    "old verify-report-prev path": r"verify-report-prev\.md",
    "old iteration changes path": r"iteration-N/changes\.md",
    "machine-local path in public docs": r"/Users/lijialun/work/engineer_skills",
    "old thinking pack count": r"(all 5 (pack|prompt)|5 个核心包)",
    "old thinking state directory": r"\.agent-log/thinking/",
    "localized downstream label in JSON": r'"downstream_pack"\s*:\s*"[^"]*(复现实验|补全证据)',
    "stale e-build recommendation phrase": r"\[[^\]]*(continue fixing|narrow scope|proceed to Phase 6|redesign)[^\]]*\]",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def run_check(name: str, command: list[str], *, env: dict[str, str] | None = None) -> None:
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        output = result.stdout.strip()
        fail(f"{name} failed\n{output}")
    print(f"PASS: {name}")


def parse_frontmatter_fields(frontmatter: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" not in line or line.startswith(" ") or line.startswith("\t"):
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def frontmatter_check() -> None:
    errors: list[str] = []
    files = list((ROOT / "skills").glob("*/SKILL.md"))
    files += list((ROOT / "skills").glob("*/prompts/*.md"))

    for path in files:
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        if path.name == "SKILL.md":
            if not text.startswith("---\n"):
                errors.append(f"{rel}: missing frontmatter opener")
                continue
            end = text.find("\n---\n", 4)
            if end < 0:
                errors.append(f"{rel}: missing frontmatter closer")
                continue
            frontmatter = text[4:end]
            fields = parse_frontmatter_fields(frontmatter)
            for key in ("name:", "description:"):
                if key not in frontmatter:
                    errors.append(f"{rel}: missing {key}")
            if not fields.get("name"):
                errors.append(f"{rel}: empty name")
            elif fields["name"] != rel.parts[1]:
                errors.append(f"{rel}: name {fields['name']!r} does not match directory {rel.parts[1]!r}")
            if not fields.get("description"):
                errors.append(f"{rel}: empty description")
            continue

        if rel.parts[1] == "e-think":
            if not text.startswith("---\n"):
                errors.append(f"{rel}: e-think prompt missing frontmatter")
                continue
            end = text.find("\n---\n", 4)
            if end < 0:
                errors.append(f"{rel}: malformed prompt frontmatter")
                continue
            frontmatter = text[4:end]
            fields = parse_frontmatter_fields(frontmatter)
            for key in ("name:", "title:", "downstream:"):
                if key not in frontmatter:
                    errors.append(f"{rel}: missing {key}")
            if not fields.get("name"):
                errors.append(f"{rel}: empty prompt name")

    if errors:
        fail("frontmatter check failed\n" + "\n".join(errors))
    print("PASS: frontmatter check")


def html_parser_check() -> None:
    for path in (ROOT / "docs").rglob("*.html"):
        HTMLParser().feed(path.read_text(encoding="utf-8"))
    print("PASS: HTML parser")


def install_smoke_test() -> None:
    tmp_home = Path(tempfile.mkdtemp(prefix="engineer-skills-home-"))
    try:
        env = os.environ.copy()
        env["HOME"] = str(tmp_home)
        run_check("installation smoke command", ["./install.sh", "update"], env=env)

        expected = 0
        for target in INSTALL_TARGETS:
            for skill in SKILL_NAMES:
                expected += 1
                link = tmp_home / target / skill
                if not link.is_symlink():
                    fail(f"installation smoke missing symlink: {link}")
                if link.resolve() != (ROOT / "skills" / skill).resolve():
                    fail(f"installation smoke wrong target: {link} -> {link.resolve()}")
        print(f"PASS: installation smoke symlinks ({expected})")
    finally:
        shutil.rmtree(tmp_home, ignore_errors=True)


def protocol_residual_scan() -> None:
    active_files = list((ROOT / "skills").rglob("*.md"))
    active_files += [ROOT / "README.md"]
    active_files += list((ROOT / "docs").rglob("*.md"))
    active_files += list((ROOT / "docs").rglob("*.html"))
    errors: list[str] = []
    for path in active_files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for label, pattern in RESIDUAL_PATTERNS.items():
            if re.search(pattern, text):
                errors.append(f"{label}: {rel}")
    if errors:
        fail("protocol residual scan failed\n" + "\n".join(errors))
    print("PASS: protocol residual scan")


def e_think_downstream_invariant_check() -> None:
    allowed = E_THINK_PACKS | TERMINALS
    errors: list[str] = []
    for path in sorted((ROOT / "skills/e-think/prompts").glob("*.md")):
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        frontmatter_end = text.find("\n---\n", 4)
        frontmatter = text[4:frontmatter_end] if text.startswith("---\n") and frontmatter_end >= 0 else ""

        name_match = re.search(r"^name:\s*([^\n]+)", frontmatter, re.MULTILINE)
        if not name_match:
            errors.append(f"{rel}: missing pack name")
        elif name_match.group(1).strip() not in E_THINK_PACKS:
            errors.append(f"{rel}: unknown pack name {name_match.group(1).strip()}")

        frontmatter_next_values: set[str] = set()
        for next_match in re.finditer(r"^\s+next:\s*([^\n]+)", frontmatter, re.MULTILINE):
            next_value = next_match.group(1).strip().strip('"').strip("'")
            frontmatter_next_values.add(next_value)
            if next_value not in allowed:
                errors.append(f"{rel}: invalid frontmatter next {next_value!r}")

        json_downstream_values: set[str] = set()
        for json_match in re.finditer(r'"downstream_pack"\s*:\s*"([^"]+)"', text):
            for value in [part.strip() for part in json_match.group(1).split("|")]:
                json_downstream_values.add(value)
                if value not in allowed:
                    errors.append(f"{rel}: invalid JSON downstream_pack {value!r}")

        if frontmatter_next_values != json_downstream_values:
            errors.append(
                f"{rel}: frontmatter downstream {sorted(frontmatter_next_values)} "
                f"does not match JSON downstream_pack {sorted(json_downstream_values)}"
            )

        for key in ('"pack"', '"timestamp"', '"conclusion"', '"next_action"', '"downstream_pack"'):
            if key not in text:
                errors.append(f"{rel}: JSON schema missing {key}")

    if errors:
        fail("e-think downstream invariant check failed\n" + "\n".join(errors))
    print("PASS: e-think downstream invariant check")


def e_build_verify_prompt_check() -> None:
    path = ROOT / "skills/e-build/prompts/verify.md"
    text = path.read_text(encoding="utf-8")
    required_sections = ("## Commands Run", "## Evidence", "## Residual Risks / Gaps")
    missing = [section for section in required_sections if section not in text]
    if missing:
        fail("e-build verify prompt missing required sections: " + ", ".join(missing))
    print("PASS: e-build verify prompt check")


def research_state_check(state_dir: Path) -> None:
    if not state_dir.exists() or not state_dir.is_dir():
        fail(f"research state directory does not exist: {state_dir}")

    required = ("session.md", "charter.md", "evidence-ledger.md", "report.md", "knowledge.md")
    missing = [name for name in required if not (state_dir / name).is_file()]
    if missing:
        fail("research state missing required files: " + ", ".join(missing))

    errors: list[str] = []
    experiments: dict[str, Path] = {}
    results: dict[str, Path] = {}
    for path in state_dir.glob("experiment-*.md"):
        match = re.fullmatch(r"experiment-(\d+)(-results)?\.md", path.name)
        if not match:
            errors.append(f"unexpected experiment filename: {path.name}")
            continue
        number = match.group(1)
        if match.group(2):
            results[number] = path
        else:
            experiments[number] = path

    for number in sorted(experiments):
        if number not in results:
            errors.append(f"missing result file for experiment-{number}.md")
    for number in sorted(results):
        if number not in experiments:
            errors.append(f"missing design file for experiment-{number}-results.md")

    if not experiments:
        errors.append("no experiment-N.md files found")

    if errors:
        fail("research state check failed\n" + "\n".join(errors))
    print(f"PASS: research state check ({len(experiments)} experiments)")


def self_test() -> None:
    residual_fixtures = {
        "direct Phase 6 proceed recommendation": "- **proceed**: Success is genuine, proceed to Phase 6 Knowledge Extraction",
        "old iteration_number placeholder": "Current iteration: {iteration_number}",
        "old thinking state directory": "State passes through `.agent-log/thinking/` files.",
        "localized downstream label in JSON": '"downstream_pack": "root-cause | 复现实验"',
    }
    for label, fixture in residual_fixtures.items():
        pattern = RESIDUAL_PATTERNS[label]
        if not re.search(pattern, fixture):
            fail(f"self-test did not catch residual fixture: {label}")

    allowed = E_THINK_PACKS | TERMINALS
    bad_downstream_values = ["复现实验", "補全證據", "verify success", "phase-6"]
    for value in bad_downstream_values:
        if value in allowed:
            fail(f"self-test bad downstream unexpectedly allowed: {value}")

    good_downstream_values = ["root-cause", "next-experiment", "reproduce", "done"]
    for value in good_downstream_values:
        if value not in allowed:
            fail(f"self-test good downstream unexpectedly rejected: {value}")

    fields = parse_frontmatter_fields("name: wrong-name\ndescription: Use when testing.\n")
    if fields.get("name") != "wrong-name" or fields.get("description") != "Use when testing.":
        fail("self-test frontmatter parser failed")
    if fields["name"] == "e-build":
        fail("self-test frontmatter mismatch fixture unexpectedly matched")

    stale_recommendation = "**Recommendation**: [continue fixing | narrow scope | proceed to Phase 6 | redesign]"
    if not re.search(RESIDUAL_PATTERNS["stale e-build recommendation phrase"], stale_recommendation):
        fail("self-test did not catch stale recommendation phrase")
    for recommendation in E_BUILD_RECOMMENDATIONS:
        if " " in recommendation:
            fail(f"self-test allowed recommendation contains spaces: {recommendation}")

    print("PASS: validator self-test")


def main() -> None:
    if len(sys.argv) > 1:
        if sys.argv[1] == "--self-test":
            self_test()
            return
        if sys.argv[1] == "--research-state" and len(sys.argv) == 3:
            research_state_check((ROOT / sys.argv[2]).resolve())
            return
        fail(f"unknown argument: {sys.argv[1]}")

    run_check("bash syntax", ["bash", "-n", "install.sh"])
    run_check("git diff whitespace", ["git", "diff", "--check"])
    frontmatter_check()
    html_parser_check()
    install_smoke_test()
    protocol_residual_scan()
    e_think_downstream_invariant_check()
    e_build_verify_prompt_check()
    print("All protocol validation checks passed.")


if __name__ == "__main__":
    main()
