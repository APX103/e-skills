---
name: next-experiment
title: 下一轮实验包
badge: 行动生成
trigger: 已有判断、根因或突破口，需要继续实践
downstream:
  - condition: "实验设计完成"
    next: done
---

# 下一轮实验包

把反思收束成更小、更准、更可验证的行动。

## 输入材料

- 上一轮结论：前面思维包的结论
- 待验证假设：需要检验的具体假设
- 主要矛盾/根因：当前最需要解决的问题
- 可用资源：时间、人力、技术限制
- 约束条件：不能改变的硬性限制
- 风险：已知的可能负面后果
- 上游分析：前面思维包的 JSON 输出

## 核心问题

1. 用一句话，本轮假设是什么？
2. 最小行动是什么？（尽量只改变一个关键变量）
3. 什么结果算成功？什么结果算失败？什么结果算信息不够？
4. 观察什么指标？结果指标、过程指标、反作用指标分别是什么？
5. 什么时候停止？（防止沉没成本）
6. 复盘时优先调用哪个思维包？

## 操作步骤

1. 把上一轮结论改写成一个可检验假设
2. 设计最小行动，只改变一个关键变量
3. 定义成功标准、失败标准和不确定标准
4. 提前写下停止条件，防止沉没成本
5. 设定观察指标：结果指标、过程指标、反作用指标
6. 安排复盘节点，明确下一次调用哪个思维包

参考框架：科学方法（可检验假设）+ Lean Startup（最小实验）。

## 输出物

### Markdown 报告

写入 `{state_dir}/next-experiment.md`：

```markdown
# 下一轮实验 — 设计报告

## 本轮假设
[一句话]

## 最小行动
[只改变一个关键变量的最小可执行方案]

## 成功/失败/不确定标准
- 成功：[什么结果算成]
- 失败：[什么结果算没成]
- 不确定：[什么情况说明信息不够]

## 观察指标
- 结果指标：
- 过程指标：
- 反作用指标：

## 停止条件
[什么情况下应该放弃这个方向]

## 复盘安排
[什么时候复盘，复盘时优先调用哪个思维包]
```

### JSON 结构化数据

写入 `{state_dir}/next-experiment.json`：

```json
{
  "pack": "next-experiment",
  "timestamp": "<ISO 8601>",
  "conclusion": "<实验设计结论>",
  "hypothesis": "...",
  "minimal_action": "...",
  "changed_variable": "...",
  "success_criteria": "...",
  "failure_criteria": "...",
  "uncertain_criteria": "...",
  "result_metrics": ["..."],
  "process_metrics": ["..."],
  "side_effect_metrics": ["..."],
  "stop_conditions": ["..."],
  "review_schedule": "...",
  "review_pack": "verify-success | verify-failure",
  "risks": ["..."],
  "next_action": "执行实验",
  "downstream_pack": "done"
}
```

## 下游接口

- 实验设计完成 → done。实验执行后，根据实际结果重新进入 verify-success 或 verify-failure。
