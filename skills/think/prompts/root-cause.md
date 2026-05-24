---
name: root-cause
title: 根因分析包
badge: 归因分析
trigger: 已确认成功或失败，需要解释原因
downstream:
  - condition: "原因复杂，多个系统条件交织"
    next: main-contradiction
  - condition: "原因明确，单一或少数根因"
    next: next-experiment
---

# 根因分析包

把"为什么"从情绪化解释，推进到可验证的因果链。

## 输入材料

- 要解释的结果：成功或失败的具体表现
- 过程记录：做了什么，按什么顺序
- 已知变量：关键的可控和不可控变量
- 对照案例：类似场景的不同结果（如果有）
- 异常现象：过程中的反常信号
- 上游分析：verify-success 或 verify-failure 的结论

## 核心问题

1. 所有可能的原因是什么？（不少于 5 个）
2. 每个原因追到哪一层了？（5 Whys 深挖）
3. 根因、近因、背景条件、触发因素分别是什么？
4. 有没有反例？（相同原因但不同结果，或不同原因但相同结果）
5. 哪些原因是可以改变并产生下一轮可验证行动的？

## 操作步骤

1. 列出所有候选原因，不急着选一个喜欢的解释
2. 用 5 Whys 深挖每个候选原因的上游条件
3. 按"可控性、影响力、证据强度"给原因排序
4. 寻找反例：相同原因是否也导致过不同结果
5. 区分根因、近因、背景条件和触发因素
6. 把最可能根因改写成可验证假设

参考框架：Toyota A3 / 5 Whys — 连续追问到可行动层面。

## 输出物

### Markdown 报告

写入 `{state_dir}/root-cause.md`：

```markdown
# 根因分析 — 分析报告

## 候选原因排序
[按影响力×可控性×证据强度排序]

## 5 Whys 分析
[对每个主要原因的追问链]

## 原因分类
- 根因：
- 近因：
- 背景条件：
- 触发因素：

## 反例检查
[相同原因但不同结果的案例，或不同原因但相同结果的案例]

## 最可能的 1-3 个根因
[带证据等级和评分]

## 可验证假设
[将根因改写为可检验假设]
```

### JSON 结构化数据

写入 `{state_dir}/root-cause.json`：

```json
{
  "pack": "root-cause",
  "timestamp": "<ISO 8601>",
  "candidate_causes": [
    {"cause": "...", "impact": "高|中|低", "controllability": "高|中|低", "evidence": "强|中|弱"}
  ],
  "root_causes": ["..."],
  "proximate_causes": ["..."],
  "background_conditions": ["..."],
  "triggers": ["..."],
  "counter_examples": ["..."],
  "testable_hypotheses": ["..."],
  "risks": ["..."],
  "next_action": "...",
  "downstream_pack": "main-contradiction | next-experiment"
}
```

## 下游接口

- 原因复杂（3+ 系统条件交织） → main-contradiction（找主要矛盾）
- 原因明确（单一或少数根因） → next-experiment（设计针对性实验）
