---
name: red-team
title: 红队攻击包
badge: 对抗验证
trigger: 方案设计完成后或验证通过后，需要对抗性验证
downstream:
  - condition: "发现严重缺陷"
    next: root-cause
  - condition: "发现可修复问题"
    next: next-experiment
  - condition: "方案经受住攻击"
    next: verify-success
  - condition: "需要更多信息"
    next: investigation
---

# 红队攻击包

系统性地攻击方案或实现，找出在正常验证流程中被遗漏的缺陷。

## 输入材料

- 方案/实现：待攻击的目标（代码、设计、计划）
- 预期行为：方案应该达到的效果
- 已有测试：已覆盖的测试场景和结果
- 攻击面：输入接口、依赖关系、外部交互点
- 上下文：部署环境、用户画像、使用场景
- 上游分析：verify-success 的结论和证据等级
- 约束：性能要求、安全要求、兼容性要求

## 核心问题

1. 这个方案在生产中最可能怎样失败？
2. 哪些输入/条件没有被测试覆盖？
3. 哪个假设如果错误会导致方案彻底崩溃？
4. 对抗性用户或外部系统会如何利用这个方案？
5. 在负载、边界和故障模式下会发生什么？
6. "显然的修复"是否在修症状而非修原因？

## 操作步骤

1. 枚举失败模式：从输入层、逻辑层、状态层、输出层逐层寻找可被攻击的点
2. 找出未覆盖场景：对比预期行为和已有测试，列出测试盲区
3. 识别关键假设：列出方案成立所依赖的隐含前提，逐个检查脆弱性
4. 模拟对抗行为：站在恶意用户或故障环境的视角，设计攻击路径
5. 测试边界和压力条件：空输入、超大输入、并发竞争、资源耗尽、超时
6. 区分症状修复和根因修复：检查每个"修复"是否真正消除了问题源头

参考框架：Popper 证伪（主动攻击自己的判断）+ 对抗性分析（系统性枚举失败模式）。

## 输出物

### Markdown 报告

写入 `{state_dir}/red-team.md`：

```markdown
# 红队攻击 — 分析报告

## 结论
[严重缺陷 / 可修复问题 / 经受住攻击]

## 攻击向量
[按严重程度排序的攻击路径]

## 严重程度评级
- 严重：
- 高：
- 中：
- 低：

## 未覆盖场景
[测试盲区清单]

## 关键假设风险
[每个隐含假设及其脆弱性评估]

## 最薄弱环节
[防御最弱的 1-3 个点]

## 修复建议
[针对发现的问题，给出修复方向]
```

### JSON 结构化数据

写入 `{state_dir}/red-team.json`：

```json
{
  "pack": "red-team",
  "timestamp": "<ISO 8601>",
  "conclusion": "严重缺陷 | 可修复问题 | 经受住攻击",
  "attack_vectors": [
    {"vector": "...", "severity": "严重|高|中|低", "scenario": "..."}
  ],
  "untested_scenarios": ["..."],
  "critical_assumptions": [
    {"assumption": "...", "fragility": "高|中|低"}
  ],
  "weakest_points": ["..."],
  "tested_scenarios": ["..."],
  "risks": ["..."],
  "next_action": "...",
  "downstream_pack": "root-cause | next-experiment | verify-success | investigation"
}
```

## 下游接口

- 发现严重缺陷 → root-cause（缺陷作为新的失败进行分析）
- 发现可修复问题 → next-experiment（设计针对性修复）
- 方案经受住攻击 → verify-success（以更高置信度确认成功）
- 需要更多信息 → investigation（调查攻击面涉及的未知领域）
