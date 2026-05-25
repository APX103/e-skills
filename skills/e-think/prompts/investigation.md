---
name: investigation
title: 调查研究包
badge: 系统探查
trigger: 面对陌生代码、未知API、模糊需求或"我不理解X"
downstream:
  - condition: "理解清晰，可形成假设"
    next: next-experiment
  - condition: "发现关键未知"
    next: next-experiment
  - condition: "范围过大，需要缩小"
    next: investigation
---

# 调查研究包

在形成判断之前，系统地探索未知领域，建立基于证据的理解基础。

## 输入材料

- 调查目标：需要理解的主题、问题或现象
- 已知信息：已经确认为事实的内容
- 假设和猜测：认为可能为真但未验证的内容
- 可用线索：代码、文档、日志、错误信息、API 响应
- 约束条件：时间限制、访问权限、可用的工具
- 上下文：这个调查服务于什么更大的目标
- 上游分析：其他思维包提出的未解答问题

## 核心问题

1. 我实际知道什么 vs 我认为我知道什么？
2. 形成可验证假设所需的最小信息集是什么？
3. 信息密度最高的观察点在哪里？
4. 已知证据中存在什么模式？
5. 哪些关键未知阻塞了进展？

## 操作步骤

1. 区分已知事实和假设：列出所有"知道的内容"，逐个标记为已验证事实或未验证假设
2. 识别最小必要信息：确定形成可行动结论所需的最少信息
3. 按信息密度排序：对每个未知项评估"获取该信息的成本"vs"该信息的价值"，从高密度点开始
4. 提取模式：从已知事实中寻找规律、结构和关系
5. 编目关键未知：列出阻塞进展的未知项，按优先级排序
6. 设计定向探索：为每个关键未知设计最小调查动作（读代码、写测试、查文档、加日志）

参考框架：实践论式闭环（从证据出发）+ 结构化调查（按信息密度系统探索）。

## 输出物

### Markdown 报告

写入 `{state_dir}/investigation.md`：

```markdown
# 调查研究 — 分析报告

## 结论
[理解清晰 / 有关键未知 / 范围过大]

## 已知事实 vs 假设
- 已验证事实：
- 未验证假设：

## 关键未知清单
[按优先级排序的阻塞项]

## 信息密度排序
[成本-价值比分析，从哪里开始调查]

## 模式分析
[从已知证据中提取的规律和结构]

## 调查目标
[每个关键未知对应的定向探索动作]

## 建议
[继续调查 / 缩小范围 / 可形成假设，进入实验]
```

### JSON 结构化数据

写入 `{state_dir}/investigation.json`：

```json
{
  "pack": "investigation",
  "timestamp": "<ISO 8601>",
  "conclusion": "理解清晰 | 有关键未知 | 范围过大",
  "known_facts": ["..."],
  "assumptions": ["..."],
  "critical_unknowns": [
    {"unknown": "...", "priority": "高|中|低", "investigation_action": "..."}
  ],
  "information_density_priorities": [
    {"item": "...", "cost": "高|中|低", "value": "高|中|低"}
  ],
  "pattern_notes": ["..."],
  "investigation_targets": ["..."],
  "risks": ["..."],
  "next_action": "...",
  "downstream_pack": "next-experiment | investigation"
}
```

## 下游接口

- 理解清晰，可形成假设 → next-experiment（基于调查结果设计实验）
- 发现关键未知 → next-experiment（设计针对未知项的定向实验）
- 范围过大，需要缩小 → investigation（聚焦到更小的子范围继续调查）
