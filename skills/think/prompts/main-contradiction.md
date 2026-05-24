---
name: main-contradiction
title: 主要矛盾包
badge: 突破口选择
trigger: 原因很多、约束很多，不知道先解决哪个
downstream:
  - condition: "找到突破口"
    next: next-experiment
---

# 主要矛盾包

从一堆问题里找当前阶段最值得抓的突破口。

## 输入材料

- 当前目标：我们最终要达到什么
- 当前阶段：在整体进程中的位置
- 已知问题/矛盾：所有已识别的问题和约束
- 可用资源：时间、人力、技术、资金
- 关键约束：不能改变的硬性限制
- 时间压力：紧迫程度
- 上游分析：root-cause 的候选原因排序

## 核心问题

1. 哪个矛盾一旦改变，会带动最多其他问题变化？
2. 当前阶段的主要方面是什么？（供给不足 / 需求不清 / 能力不够 / 信任不足）
3. 这个矛盾在什么条件下会转化？
4. 最可撬动的关键点在哪里？（不是最大最难最显眼的，是最能四两拨千斤的）

## 操作步骤

1. 列出所有阻碍目标实现的矛盾：需求、资源、能力、时间、组织、环境
2. 判断哪个矛盾一旦改变，会带动最多其他问题变化
3. 判断当前阶段的主要方面：是供给不足、需求不清、能力不够，还是信任不足
4. 检查矛盾是否会随阶段转化，避免拿旧突破口解决新问题
5. 选择一个可撬动的关键点，而不是选择最大、最难、最显眼的问题
6. 把突破策略写成一个具体实验

参考框架：矛盾论 — 找主要矛盾和矛盾的主要方面，注意阶段转化。

## 输出物

### Markdown 报告

写入 `{state_dir}/main-contradiction.md`：

```markdown
# 主要矛盾 — 分析报告

## 矛盾全景
[所有矛盾的列表和影响范围]

## 影响力分析
[每个矛盾影响哪些其他问题]

## 可撬动性分析
[哪个矛盾用较小行动能产生明显变化]

## 主要矛盾判定
[当前阶段的主要矛盾]

## 矛盾的主要方面
[哪一边正在主导局面]

## 阶段转化预警
[这个主要矛盾在什么条件下会转化]

## 突破策略
[具体、可执行的突破方案]
```

### JSON 结构化数据

写入 `{state_dir}/main-contradiction.json`：

```json
{
  "pack": "main-contradiction",
  "timestamp": "<ISO 8601>",
  "conclusion": "<主要矛盾判定>",
  "all_contradictions": [
    {"contradiction": "...", "impact_scope": ["..."], "leverage": "高|中|低"}
  ],
  "main_contradiction": "...",
  "main_aspect": "...",
  "transformation_conditions": ["..."],
  "breakthrough_strategy": "...",
  "risks": ["..."],
  "next_action": "...",
  "downstream_pack": "next-experiment"
}
```

## 下游接口

- 找到突破口 → next-experiment（把突破策略转化为实验）
