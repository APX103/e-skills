---
name: reproduce
title: 复现实验包
badge: 确认验证
trigger: 验证通过/失败后需要确认可复现，或调试间歇性问题
downstream:
  - condition: "稳定复现"
    next: verify-failure
  - condition: "无法复现"
    next: investigation
  - condition: "间歇性复现"
    next: next-experiment
---

# 复现实验包

设计受控复现实验，确认结果是可重复的，而非偶然或环境特定的。

## 输入材料

- 目标：需要复现的结果（成功或失败）
- 原始条件：首次观察时的环境、状态、输入
- 当前环境：与原始条件的差异
- 可变因素：已识别的可能影响结果的变量
- 时间窗口：原始结果发生的时间上下文
- 已有尝试：之前的复现尝试及结果
- 上游分析：verify-success 或 verify-failure 的结论

## 核心问题

1. 复现所需的最小步骤是什么？
2. 哪些环境因素可能影响结果（OS、运行时、状态、时序、并发）？
3. 结果能否在隔离环境中复现，还是依赖特定状态？
4. 哪些变量可控，哪些是随机的？
5. 需要连续成功多少次才能确认可靠性？
6. 如果无法复现，自上次观察以来什么发生了变化？

## 操作步骤

1. 提取最小复现步骤：从原始操作中剥离非必要步骤，逐步简化直到无法进一步减少
2. 识别环境因素：列出所有可能影响结果的系统级、进程级、数据级因素
3. 测试隔离级别：从完整环境逐步隔离到最小环境，找到复现所需的最少条件
4. 区分可控变量和随机变量：对每个变量进行可控性分类，识别噪声源
5. 建立可靠性基线：多次运行最小复现，记录成功率
6. 设计非复现场景：如果无法复现，列出可能的差异因素并设计排查实验

参考框架：科学方法（受控实验与变量隔离）+ Lean Startup（最小化复现）。

## 输出物

### Markdown 报告

写入 `{state_dir}/reproduce.md`：

```markdown
# 复现实验 — 分析报告

## 结论
[稳定复现 / 间歇性复现 / 无法复现]

## 最小复现步骤
[逐步简化的复现流程]

## 环境因素分析
- 系统级：
- 进程级：
- 数据级：
- 时序/并发：

## 隔离级别
[复现所需的最小环境条件]

## 可靠性评估
- 运行次数：
- 成功次数：
- 可靠性比率：

## 变量分析
- 可控变量：
- 随机变量/噪声源：

## 阻塞因素
[如果无法复现，可能的差异因素]

## 建议
[确认因果 / 排查差异 / 设计进一步实验]
```

### JSON 结构化数据

写入 `{state_dir}/reproduce.json`：

```json
{
  "pack": "reproduce",
  "timestamp": "<ISO 8601>",
  "conclusion": "稳定复现 | 间歇性复现 | 无法复现",
  "reproduction_steps": ["..."],
  "controlled_variables": ["..."],
  "stochastic_variables": ["..."],
  "environment_conditions": ["..."],
  "reliability_rate": "N/M",
  "isolation_level": "...",
  "blocking_factors": ["..."],
  "risks": ["..."],
  "next_action": "...",
  "downstream_pack": "verify-failure | investigation | next-experiment"
}
```

## 下游接口

- 稳定复现 → verify-failure（确认问题真实存在）或 verify-success（确认修复有效）
- 间歇性复现 → next-experiment（设计实验识别变化因素）
- 无法复现 → investigation（排查缺失的条件或环境差异）
