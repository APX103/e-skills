---
name: evidence-strength
title: 证据强度包
badge: 质量校验
trigger: 收集证据后、做出判断前，或证据感觉薄弱/不完整时
downstream:
  - condition: "证据充分"
    next: root-cause
  - condition: "证据不足，关键缺口已知"
    next: next-experiment
  - condition: "证据不足，缺口未知"
    next: investigation
---

# 证据强度包

系统性评估证据基础是否足以支撑结论，防止"测试通过就等于没问题"的假象。

## 输入材料

- 待支持的主张：需要被证据证明的结论
- 已收集的证据：测试结果、观察数据、日志、对比信息
- 证据来源：证据是如何产生的（自动化测试、手动验证、用户反馈等）
- 验证方法：证据收集的过程和方法
- 已知局限：证据收集过程中的限制条件
- 上游分析：verify-success 或 verify-failure 的初步结论
- 完整性预期：理想情况下应该有哪些证据

## 核心问题

1. 这组证据要支持什么主张？
2. 这是什么类型的证据（直接/间接/旁证/类比）？
3. 缺少了什么？完整的证据集应该是什么样的？
4. 这个证据能否用替代假说来解释？
5. 当前验证方法的假阳性率是多少？
6. 如果这个证据是错的，第一个信号会是什么？

## 操作步骤

1. 明确待支持主张：精确陈述证据需要证明什么
2. 分类证据类型：将每条证据标记为直接、间接、旁证或类比
3. 映射证据缺口：对比现有证据和理想证据集，找出缺失的关键证据
4. 生成替代解释：为每个主张提出至少一个不依赖当前结论的替代解释
5. 评估假阳性风险：分析当前验证方法可能产生误导性通过信号的概率
6. 设计证伪测试：为结论设计"如果错了会怎样"的具体检验

参考框架：科学方法（证据质量优先于逻辑美感）+ Popper 证伪（什么证据能推翻这个结论）。

## 输出物

### Markdown 报告

写入 `{state_dir}/evidence-strength.md`：

```markdown
# 证据强度 — 分析报告

## 结论
[证据充分 / 证据不足(缺口已知) / 证据不足(缺口未知)]

## 主张-证据映射
[每条主张对应的证据和证据类型]

## 证据类型分析
- 直接证据：
- 间接证据：
- 旁证：
- 类比：

## 完整性检查
[现有证据 vs 理想证据集的差距]

## 替代解释
[不依赖当前结论的其他可能解释]

## 假阳性风险
[验证方法可能产生误导信号的评估]

## 关键缺口
[缺失的最重要证据]

## 置信度评分
[基于以上分析的整体置信度]

## 建议
[继续归因 / 补充证据 / 重新调查]
```

### JSON 结构化数据

写入 `{state_dir}/evidence-strength.json`：

```json
{
  "pack": "evidence-strength",
  "timestamp": "<ISO 8601>",
  "conclusion": "证据充分 | 证据不足(缺口已知) | 证据不足(缺口未知)",
  "claims_supported": [
    {"claim": "...", "evidence": "...", "evidence_type": "直接|间接|旁证|类比"}
  ],
  "evidence_completeness": "高|中|低",
  "alternative_explanations": ["..."],
  "false_positive_risk": "高|中|低",
  "critical_gaps": ["..."],
  "confidence_score": "0-100",
  "risks": ["..."],
  "next_action": "...",
  "downstream_pack": "root-cause | next-experiment | investigation"
}
```

## 下游接口

- 证据充分 → root-cause（基于可靠证据进行归因分析）
- 证据不足，关键缺口已知 → next-experiment（设计针对性证据收集实验）
- 证据不足，缺口未知 → investigation（系统性地搜索缺失的证据）
