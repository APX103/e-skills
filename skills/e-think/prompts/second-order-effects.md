---
name: second-order-effects
title: 二阶后果包
badge: 连锁分析
trigger: 方案确认前或修复设计后，需要评估连锁后果
downstream:
  - condition: "发现高风险连锁"
    next: main-contradiction
  - condition: "后果可控"
    next: next-experiment
  - condition: "需要更多信息"
    next: investigation
---

# 二阶后果包

追踪变更在系统中的连锁影响，防止"修了一个问题，引入了三个新问题"。

## 输入材料

- 变更内容：具体的代码变更、配置变更或架构变更
- 直接影响：已知的受影响的模块和功能
- 系统架构：模块间的依赖关系图
- 已有不变量：系统必须维持的行为保证
- 部署上下文：运行环境、依赖版本、配置状态
- 上游分析：root-cause 的结论和 next-experiment 的设计方案
- 历史教训：类似变更曾经导致的连锁问题

## 核心问题

1. 如果变更完全按预期生效，还有什么会随之改变？
2. 哪些系统、模块或依赖会直接受到影响？
3. 变更的两跳外、三跳外分别是什么？
4. 这可能违反哪些现有模式或不变量？
5. 最现实的最坏连锁失败模式是什么？
6. 负面后果能否在同一变更中一并缓解？

## 操作步骤

1. 映射一阶影响：列出变更直接触及的所有模块、接口和数据流
2. 追踪二阶影响：从一阶影响出发，找出被间接影响的下游模块
3. 追踪三阶影响：继续向外扩展，找出更远层的连锁效应
4. 检查不变量违反：对比变更前后的行为保证，识别可能被打破的契约
5. 识别最坏连锁失败：从每个影响点出发，推演最现实的灾难路径
6. 设计缓解措施：对高风险连锁设计预防措施，合并到同一变更中

参考框架：矛盾论式定位（系统级思维）+ 系统连锁分析（层层追踪变更传播）。

## 输出物

### Markdown 报告

写入 `{state_dir}/second-order-effects.md`：

```markdown
# 二阶后果 — 分析报告

## 结论
[高风险连锁 / 后果可控 / 需要更多信息]

## 一阶影响
[变更直接触及的模块和接口]

## 二阶影响
[被间接影响的下游模块]

## 三阶影响
[更远层的连锁效应]

## 不变量检查
[可能被打破的行为契约和模式]

## 风险链分析
[最现实的灾难路径和传播链]

## 缓解措施
[预防高风险连锁的具体措施]

## 建议
[继续执行 / 调整范围 / 补充调查]
```

### JSON 结构化数据

写入 `{state_dir}/second-order-effects.json`：

```json
{
  "pack": "second-order-effects",
  "timestamp": "<ISO 8601>",
  "conclusion": "高风险连锁 | 后果可控 | 需要更多信息",
  "first_order_effects": ["..."],
  "second_order_effects": ["..."],
  "third_order_effects": ["..."],
  "affected_systems": ["..."],
  "risk_chain": [
    {"chain": ["..."], "probability": "高|中|低", "severity": "高|中|低"}
  ],
  "violation_check": [
    {"invariant": "...", "risk": "高|中|低", "mitigation": "..."}
  ],
  "mitigations": ["..."],
  "risks": ["..."],
  "next_action": "...",
  "downstream_pack": "main-contradiction | next-experiment | investigation"
}
```

## 下游接口

- 发现高风险连锁 → main-contradiction（重新评估优先级，可能需要调整方案）
- 后果可控 → next-experiment（继续执行，将缓解措施纳入设计）
- 需要更多信息 → investigation（调查受影响的系统模块）
