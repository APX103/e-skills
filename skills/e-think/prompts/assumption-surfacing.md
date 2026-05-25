---
name: assumption-surfacing
title: 假设挖掘包
badge: 盲点检测
trigger: 任务开始前或计划屡屡失败原因不明时
downstream:
  - condition: "发现关键假设被违反"
    next: root-cause
  - condition: "假设未验证，需要测试"
    next: next-experiment
  - condition: "假设成立，方向正确"
    next: next-experiment
  - condition: "假设不明确"
    next: investigation
---

# 假设挖掘包

系统性地挖掘和检验隐含假设，防止在错误的前提下构建解决方案。

## 输入材料

- 方案/计划：待检验的方案或当前执行计划
- 前提条件：方案成立所需的显式条件
- 执行上下文：环境、依赖、配置、运行时状态
- 历史经验：类似方案过去成功/失败的模式
- 失败模式：如果当前方案正在失败，失败的具体表现
- 领域知识：相关领域的关键约束和常见陷阱
- 上游分析：root-cause 或其他思维包提出的问题

## 核心问题

1. 这个方案要成功，什么条件必须成立？
2. 这些条件中哪些已验证，哪些是假设？
3. 最危险的假设是哪个（如果错了影响最大）？
4. 什么证据能证明每个假设是错误的？
5. 是否有从外部导入的领域/文化假设可能不成立？
6. 如果最基本假设（如"代码能编译"、"测试环境匹配生产"）错了，会怎样？

## 操作步骤

1. 列出所有必要条件：从方案出发，反推它成立的全部前提
2. 分类已验证和未验证：将每个条件标记为"有证据支持"或"仅凭假设"
3. 按危险度排序：评估每个假设被推翻时的影响程度和概率
4. 设计证伪测试：为每个高危假设设计最小验证动作
5. 检查领域假设：识别从 prompt 或上下文中导入的可能不成立的领域假设
6. 压力测试基础假设：质疑最底层的前提（环境一致性、依赖可用性、数据正确性）

参考框架：Popper 证伪（主动挑战自己的前提）+ 科学方法（让隐含假设变得显式且可检验）。

## 输出物

### Markdown 报告

写入 `{state_dir}/assumption-surfacing.md`：

```markdown
# 假设挖掘 — 分析报告

## 结论
[关键假设被违反 / 假设未验证 / 假设成立 / 假设不明确]

## 隐含假设清单
[方案成立所依赖的全部前提]

## 已验证 vs 未验证
- 已验证条件：
- 未验证假设：

## 危险度排序
[按影响×概率排序的假设]

## 证伪测试设计
[每个高危假设的验证方法]

## 领域假设检查
[从外部导入的可能不成立的假设]

## 建议
[调整方案 / 验证假设 / 继续执行 / 补充调查]
```

### JSON 结构化数据

写入 `{state_dir}/assumption-surfacing.json`：

```json
{
  "pack": "assumption-surfacing",
  "timestamp": "<ISO 8601>",
  "conclusion": "关键假设被违反 | 假设未验证 | 假设成立 | 假设不明确",
  "implicit_assumptions": ["..."],
  "verified_assumptions": ["..."],
  "unverified_assumptions": [
    {"assumption": "...", "impact": "高|中|低", "probability_wrong": "高|中|低"}
  ],
  "most_dangerous_assumptions": ["..."],
  "falsification_tests": [
    {"assumption": "...", "test": "...", "effort": "高|中|低"}
  ],
  "domain_assumptions": ["..."],
  "risks": ["..."],
  "next_action": "...",
  "downstream_pack": "root-cause | next-experiment | investigation"
}
```

## 下游接口

- 发现关键假设被违反 → root-cause（被违反的假设就是根因）
- 假设未验证，需要测试 → next-experiment（设计假设验证实验）
- 假设成立，方向正确 → next-experiment（继续执行，信心更高）
- 假设不明确 → investigation（澄清真正的需求和约束）
