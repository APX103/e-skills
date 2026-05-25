# Engineer Skills

`engineer_skills` 是一组面向 Agent 的工作流 skills，用来把软件工程、结构化思考和长任务知识生产变成可复用、可安装、可验证的流程。

这个仓库目前包含三类核心能力：

- `e-build`: 面向工程实现的自驱闭环，覆盖理解、计划、执行、验证、修复和知识提取。
- `e-think`: 面向结果复盘和结构化分析的思维包系统，覆盖成功/失败判断、根因、主要矛盾、证据强度、下一轮实验等。
- `e-research`: 面向长任务知识生产的研究闭环，覆盖 research charter、调查、实验、证据复盘和综合报告。

这些 skills 的目标不是让 Agent “多想一点”，而是让 Agent 在长任务中有稳定的状态文件、明确的证据标准、可复现的实验路径和可沉淀的经验。

## 目录

- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [核心 Skills](#核心-skills)
- [安装方式](#安装方式)
- [平台用法](#平台用法)
- [典型工作流](#典型工作流)
- [状态与知识沉淀](#状态与知识沉淀)
- [Hermes 安装说明](#hermes-安装说明)
- [开发与维护](#开发与维护)
- [排障](#排障)

## 快速开始

克隆仓库：

```bash
git clone https://github.com/APX103/e-skills.git
cd e-skills
```

安装或更新本仓库所有 skills：

```bash
./install.sh update
```

安装脚本会把 `skills/` 下的每个 skill 以 symlink 形式安装到常见 Agent skill 目录：

```text
~/.claude/skills
~/.codex/skills
~/.hermes/skills
~/.agents/skills
```

安装后，重启对应 Agent 或开启新会话，让它重新扫描 skill 列表。

## 项目结构

```text
.
├── install.sh
├── shared/
│   └── thinking-frameworks.md
├── skills/
│   ├── e-build/
│   │   ├── SKILL.md
│   │   └── prompts/
│   ├── e-think/
│   │   ├── SKILL.md
│   │   └── prompts/
│   └── e-research/
│       ├── SKILL.md
│       └── prompts/
└── docs/
    ├── hermes-e-research-install.md
    ├── research-skill-usage.html
    └── plans/
```

### 关键文件

| 路径 | 作用 |
|---|---|
| `install.sh` | 将仓库 skills 链接到 Claude Code、Codex、Hermes 和通用 Agent skill 目录 |
| `skills/e-build/SKILL.md` | 工程实现闭环的主说明 |
| `skills/e-think/SKILL.md` | 结构化思考和复盘系统的主说明 |
| `skills/e-research/SKILL.md` | 长任务研究和知识生产闭环的主说明 |
| `shared/thinking-frameworks.md` | 多个 thinking packs 共用的思想框架摘要 |
| `docs/hermes-e-research-install.md` | 给 Hermes Agent 自己读取的安装和排障指南 |
| `docs/research-skill-usage.html` | 面向人类阅读的平台使用指南 |

## 核心 Skills

### e-build

`e-build` 用于工程实现类任务，例如：

- 新建项目
- 复刻已有项目或页面
- 改进代码库
- 重构模块
- 多步骤实现并验证

调用示例：

```text
/e-build "实现一个日志分析 CLI，支持读取 JSONL、聚合错误类型并输出报告" --iterations 2 --verification "automated-testing,code-review"
```

核心流程：

```text
Understand -> Plan -> Execute -> Verify -> Think -> Fix -> Extract Knowledge -> Evolve Prompts
```

特点：

- 以 `.agent-log/<timestamp>-e-build/` 保存过程状态。
- 每个阶段通过文件传递上下文，减少长任务上下文压缩带来的信息丢失。
- 验证后接入 `e-think`，先判断成功/失败是否真实，再决定修复、缩小范围、重验或继续。
- 会将跨会话经验沉淀到 `$HOME/.claude/e-build-knowledge/`。

### e-think

`e-think` 用于结构化分析，不直接承担工程实现。它适合在以下场景使用：

- 结果看起来成功，但需要确认是否真成功。
- 结果失败，需要判断是真失败、假失败还是证据不足。
- 需要根因分析、主要矛盾定位、下一轮实验设计。
- 需要审视假设、证据强度、复现性和二阶影响。

调用示例：

```text
/e-think "这个 benchmark 结果显示方案 A 快 20%，但样本只有 3 次，证据够吗？" --pack evidence-strength
```

内置 packs：

```text
verify-success
verify-failure
root-cause
main-contradiction
next-experiment
reproduce
red-team
second-order-effects
investigation
evidence-strength
assumption-surfacing
```

特点：

- 每个 pack 输出 Markdown 和 JSON。
- JSON 中的 `downstream_pack` 决定后续分析链。
- 常见链路包括预调查、调试、稳健验证和深度失败分析。

### e-research

`e-research` 用于长任务知识生产，例如：

- 思维实验
- 计算机科学研究
- 算法比较
- 可复现实验
- 对陌生系统进行证据驱动调研
- 从代码、论文、数据、模拟和实验中生产结构化理解

调用示例：

```text
/e-research 研究一下长上下文 Agent 在多轮实验任务中如何降低假成功率，输出 Research Charter、实验计划和最终报告
```

核心流程：

```text
Research Charter -> Investigation -> Experiment -> Evidence Review -> Synthesis
```

特点：

- `brainstorming` 只用于入口澄清，不负责整个研究流程。
- 小实验可以直接执行，工程复杂实验可以交给 `e-build`。
- 实验后用 `e-think` 判断成功/失败、证据强度、复现性和下一步。
- 输出应区分事实、假设、解释、未知和可复用知识。

## 安装方式

### 安装全部 skills

```bash
./install.sh update
```

这个命令会遍历 `skills/*/`，把每个 skill 链接到以下目录：

```text
~/.claude/skills/<skill-name>
~/.codex/skills/<skill-name>
~/.hermes/skills/<skill-name>
~/.agents/skills/<skill-name>
```

当前会安装：

```text
e-build
e-think
e-research
```

### 卸载

```bash
./install.sh uninstall
```

脚本只会删除它创建的 symlink。如果目标位置是普通目录，会跳过并提示手动处理。

### 为什么使用 symlink

symlink 的好处是：

- `git pull` 后本地安装内容自动更新。
- 不需要复制多份 skill 文件。
- 多个平台可以共享同一份仓库内容。

## 平台用法

### Claude Code

个人级 skills 位于：

```text
~/.claude/skills/<skill-name>/SKILL.md
```

安装后可直接调用：

```text
/e-build "实现 X"
/e-think "分析 Y 为什么失败" --pack root-cause
/e-research 研究 Z
```

也可以自然语言触发，例如：

```text
帮我研究一下 Agent 长任务知识生产怎样做证据闭环
```

### Codex

Codex 可从用户级 skills 目录发现：

```text
~/.codex/skills/<skill-name>/SKILL.md
```

安装后建议重启 Codex 或开启新会话，让 skill 列表重新加载。

推荐说法：

```text
请使用 e-research skill 研究「X」，先写 Research Charter，再设计最小实验，最后输出 evidence-backed report。
```

### Hermes

Hermes 主目录：

```text
~/.hermes/skills/<skill-name>/SKILL.md
```

如果 Hermes 已经克隆本仓库，推荐：

```bash
./install.sh update
```

如果希望 Hermes 直接从 GitHub 安装单个 skill：

```bash
hermes skills install APX103/e-skills/skills/e-research
```

或使用 tap：

```bash
hermes skills tap add APX103/e-skills
hermes skills install APX103/e-skills/e-research
```

更完整的 Hermes 安装和排障说明见：

```text
docs/hermes-e-research-install.md
```

注意：当前 skill 名是 `e-research`，slash command 应为：

```text
/e-research
```

不要使用旧名 `/research`。

### OpenCode

OpenCode 支持多种兼容路径。本仓库安装脚本会写入：

```text
~/.agents/skills/<skill-name>
~/.claude/skills/<skill-name>
```

如果 OpenCode 读取这些路径，即可发现本仓库 skills。

### Kimi CLI

Kimi Code CLI 文档显示会扫描多个用户级 skill 目录，包括：

```text
~/.kimi/skills/
~/.claude/skills/
~/.codex/skills/
~/.agents/skills/
```

本仓库安装脚本会覆盖其中多个通用目录。安装后建议重启 Kimi CLI 或开启新会话。

## 典型工作流

### 工程实现

```text
/e-build "给现有项目增加 CSV 导入功能，要求有测试和错误处理" --iterations 2
```

适合目标明确、需要改代码、需要验证的任务。

### 失败复盘

```text
/e-think "测试通过但用户反馈功能仍不可用，帮我判断是假成功还是验证不足" --pack evidence-strength
```

适合判断证据质量、复现问题、定位根因。

### 长任务研究

```text
/e-research 研究一下为什么某类 Agent 在多轮实验中容易过早收敛，允许搭建小型模拟实验并输出报告
```

适合开放式问题、实验探索和知识生产。

### e-build 与 e-think 联动

`e-build` 在验证后会触发 `e-think` 分析：

```text
Verify -> Think -> Fix or Proceed
```

这能减少“测试过了就宣称完成”的假成功。

### e-research 与 e-build 联动

`e-research` 遇到需要实现、benchmark、模拟或环境搭建的实验时，可以把执行交给 `e-build`：

```text
Research Charter -> Experiment Design -> e-build executes experiment -> e-think reviews evidence -> Synthesis
```

## 状态与知识沉淀

### 临时任务状态

长任务状态默认写入 `.agent-log/`：

```text
.agent-log/<timestamp>-e-build/
.agent-log/<timestamp>-e-think/
.agent-log/<timestamp>-research/
```

`.agent-log/` 已被 `.gitignore` 忽略，不会进入版本库。

### e-build 跨会话知识

`e-build` 会把经验沉淀到：

```text
$HOME/.claude/e-build-knowledge/
```

主要包括：

```text
knowledge/
metrics/
prompt-versions/
```

当积累足够多会话后，`e-build` 可以用这些经验做 prompt evolution。

### research 输出建议

`e-research` 的研究任务至少应产生：

```text
session.md
charter.md
evidence-ledger.md
report.md
knowledge.md
```

多轮实验任务还应包含：

```text
experiment-N.md
experiment-N-results.md
```

## Hermes 安装说明

如果你要让 Hermes 自己安装本仓库的研究 skill，直接把这份文档交给它：

```text
docs/hermes-e-research-install.md
```

最短路径：

```bash
hermes skills install APX103/e-skills/skills/e-research
```

验证：

```bash
test -f ~/.hermes/skills/e-research/SKILL.md
```

使用：

```text
/e-research 研究一下长任务知识生产如何做证据闭环
```

常见错误：

- 错误：`/research`
- 正确：`/e-research`
- 错误：`hermes skills install APX103/e-skills`
- 正确：`hermes skills install APX103/e-skills/skills/e-research`

## 开发与维护

### 新增 skill

建议结构：

```text
skills/<skill-name>/
├── SKILL.md
└── prompts/
```

`SKILL.md` frontmatter 至少包含：

```yaml
---
name: skill-name
description: Use when ...
---
```

写 description 时，重点描述“什么时候触发”，不要把完整流程塞进 description。

### 修改 skill

修改后至少检查：

```bash
bash -n install.sh
rg -n "TBD|TODO|PLACEHOLDER|\\?\\?\\?" skills docs
```

如果修改 HTML：

```bash
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path
class P(HTMLParser):
    pass
P().feed(Path("docs/research-skill-usage.html").read_text())
print("html-ok")
PY
```

### 安装脚本验证

```bash
./install.sh update
test -f ~/.hermes/skills/e-research/SKILL.md
test -f ~/.claude/skills/e-research/SKILL.md
test -f ~/.codex/skills/e-research/SKILL.md
```

## 排障

### Agent 看不到新 skill

先确认文件存在：

```bash
test -f ~/.claude/skills/e-research/SKILL.md
test -f ~/.codex/skills/e-research/SKILL.md
test -f ~/.hermes/skills/e-research/SKILL.md
```

然后重启对应 Agent 或开启新会话。很多 Agent 在会话启动时缓存 skill 列表。

### Hermes 安装后没有 `/e-research`

检查：

```bash
test -f ~/.hermes/skills/e-research/SKILL.md
sed -n '1,12p' ~/.hermes/skills/e-research/SKILL.md
```

应该看到：

```yaml
name: e-research
```

如果存在旧路径：

```bash
rm ~/.hermes/skills/research
```

然后重新安装：

```bash
hermes skills install APX103/e-skills/skills/e-research
```

### `research` 和 `e-research` 名字混淆

本仓库当前正式 skill 名是：

```text
e-research
```

旧名 `research` 不再使用。路径、frontmatter、slash command 都应统一为 `e-research`。

### install.sh 提示目录已存在

如果目标位置是普通目录而不是 symlink，脚本不会覆盖它。先确认内容，再手动处理：

```bash
ls -la ~/.hermes/skills/e-research
```

如果确定可以替换：

```bash
rm -rf ~/.hermes/skills/e-research
./install.sh update
```

## 参考文档

- `docs/research-skill-usage.html`
- `docs/hermes-e-research-install.md`
- `docs/plans/2026-05-24-e-build-skill-design.md`
- `docs/plans/2026-05-24-thinking-packs-design.md`
- `docs/plans/2026-05-24-research-skill-design.md`

## 许可证

当前仓库未声明许可证。复用、分发或公开发布前，请先确认项目所有者希望采用的许可证。
