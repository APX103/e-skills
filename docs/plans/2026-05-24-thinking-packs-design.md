# Thinking Packs Design: 实践闭环思维框架

## Overview

将"Agent 思维包"系统整合到 engineer_skills 项目中，为 build 循环提供深度分析和实践闭环能力。采用**独立 /think skill + build 集成钩子**的方案。

## Architecture

```
skills/
  think/                         # 独立 /think skill
    SKILL.md                     # skill 定义 + 触发规则 + 闭环流程
    prompts/
      template.md                # 通用思维包模板
      verify-success.md          # 包1: 真成了吗
      verify-failure.md          # 包2: 真没成吗
      root-cause.md              # 包3: 根因分析
      main-contradiction.md      # 包4: 主要矛盾
      next-experiment.md         # 包5: 下一轮实验
  build/
    SKILL.md                     # 在 Phase 4/5 间增加 think 钩子
    prompts/
      think-hook-verify.md       # 验证后调用思维包的路由逻辑
      think-hook-iterate.md      # 迭代前调用思维包的路由逻辑
shared/
  thinking-frameworks.md         # 6 个思想工具的摘要引用
```

## 1. /think Skill

### 触发规则

- `/think` — 完整闭环模式，根据上下文自动选择入口
- `/think success` — 直接调用"真成了吗包"
- `/think failure` — 直接调用"真没成吗包"
- `/think cause` — 直接调用"根因分析包"
- `/think reflect` — 读取 .agent-log/ 最近状态，自动判断入口

### 闭环流程

**成功路径：**
真成了吗包 → (证据弱？复现实验) → (证据强？根因分析包) → (多系统条件？主要矛盾包) → 下一轮实验包

**失败路径：**
真没成吗包 → (假失败？重设指标) → (真失败？根因分析包) → (原因复杂？主要矛盾包) → 下一轮实验包

### 判断原则

- 先判定结果，再解释结果。不要在结果真假还没确认时急着讲故事
- 一个原因如果不能生成下一轮可验证行动，就还不是足够好的根因
- 下一轮实验要比上一轮更小、更清楚、更容易被证伪

### 文件输出

分析结果写入 `.agent-log/thinking/` 目录：

```
.agent-log/thinking/
  2026-05-24-verify-success.md     # 可读的分析报告
  2026-05-24-verify-success.json   # 结构化数据（跨包传递）
```

JSON 格式：
```json
{
  "pack": "verify-success",
  "timestamp": "2026-05-24T10:30:00Z",
  "conclusion": "真成功 | 假成功 | 不确定",
  "evidence_level": "强 | 中 | 弱",
  "key_reasons": ["..."],
  "risks": ["..."],
  "next_action": "...",
  "downstream_pack": "root-cause | next-experiment | ..."
}
```

## 2. Build 集成点

### 节点 1: Phase 4 Verify 后 (新增 Phase 4.5)

```
Phase 4: Verify → 产出验证报告
    ↓
Phase 4.5: Think
    ├─ 验证通过 → verify-success 包
    │   → 证据弱：回到 Phase 3（缩小范围）
    │   → 证据强：进入 Phase 6
    │   → 有隐藏风险：进入 Phase 5 Fix
    │
    └─ 验证失败 → verify-failure 包
        → 假失败：回到 Phase 4（换指标/放宽时间）
        → 真失败 → root-cause 包
            → 单一原因：Phase 5 Fix（针对性修复）
            → 多原因 → main-contradiction 包
                → 找到突破口 → Phase 5 Fix（聚焦修复）
```

### 节点 2: Phase 5 Fix 收敛后 / Phase 6 之前

Fix 循环收敛后，调用 next-experiment 包评估是否需要下一轮 build 循环。

### 与现有机制的关系

- Build 的 convergence detection（问题计数）不变，思维包是计数之外的深度分析层
- Phase 6 Extract Knowledge 的知识提取逻辑不变，思维包 JSON 输出作为额外输入
- Build 现有的 7 阶段编号不变，Phase 4.5 是隐式步骤

## 3. 思维包 Prompt 设计

### 统一格式

每个包的 prompt 文件遵循以下结构：

```markdown
---
name: verify-success
title: 真成了吗包
badge: 成功校验
trigger: 验证通过 / 行动看起来成功了
downstream:
  - condition: "证据强"
    next: root-cause
  - condition: "证据弱"
    next: "复现实验"
  - condition: "假成功"
    next: root-cause
---

## 输入材料
需要提供的信息列表（用自然语言描述，不用模板变量）

## 核心问题
这个包必须回答的关键问题

## 操作步骤
可执行的推理动作

## 输出物
结论、证据等级、风险、下一步动作

## 下游接口
什么条件下接哪个思维包
```

### 5 个核心包

| 包 | 触发 | 输出 | 下游 |
|---|---|---|---|
| 真成了吗 | 看起来成功 | 真成功/假成功/不确定 + 证据等级 | 真成功→根因分析；假成功→根因分析；不确定→复现 |
| 真没成吗 | 看起来失败 | 真失败/假失败/未到时点 + 保留价值 | 真失败→根因分析；假失败→下一轮实验；不确定→补全证据 |
| 根因分析 | 已确认成功/失败 | 候选原因排序 + 待验证根因 | 原因复杂→主要矛盾；原因明确→下一轮实验 |
| 主要矛盾 | 原因很多 | 主要矛盾 + 突破策略 | → 下一轮实验 |
| 下一轮实验 | 已有结论 | 实验设计 + 指标 + 停止条件 | → 执行后回到"真成了吗"或"真没成吗" |

### 思想工具引用

6 个思想工具不独立实现为 prompt，而是作为 `shared/thinking-frameworks.md` 供各包引用：

| 工具 | 引用它的包 |
|---|---|
| 实践论式闭环 | 所有包（整体框架） |
| 矛盾论式定位 | 主要矛盾包 |
| 科学方法 | 下一轮实验包 |
| Popper 证伪 | 真成了吗包（寻找反证） |
| Lean Startup | 下一轮实验包（MVP 思维） |
| Toyota A3 / 5 Whys | 根因分析包 |

## 4. 通用思维包模板

供未来扩展新包使用：

```markdown
【思维包名称】
触发条件：在什么场景下调用这个包
输入材料：目标、假设、行动/实验、观察到的结果、证据、约束
核心问题：
  1. 这个包要判断什么？
  2. 最容易误判的地方是什么？
  3. 怎样把判断落到证据和行动上？
操作步骤：
  1. 明确评价标准
  2. 检查证据质量
  3. 区分事实、解释、情绪、愿望
  4. 给出结论等级：成立 / 不成立 / 不确定
  5. 生成下一步行动
输出物：结论、证据等级、关键原因、主要风险、下一步
下游接口：成立→接X；不成立→接Y；不确定→接Z
```
