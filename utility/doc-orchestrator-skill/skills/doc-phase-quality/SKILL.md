---
name: doc-phase-quality
version: 0.1.0
description: 质量阶段协调器，负责文档的一致性检查、完整性检查和质量评分
---

# Quality Phase Coordinator

## 职责

- 对生成的文档进行一致性校验
- 检查文档完整性
- 计算质量评分
- 输出质量报告

## 子技能

| 执行者 | 职责 | 路径 |
|--------|------|------|
| consistency-checker | 术语、追溯、格式一致性 | [查看](consistency-checker/SKILL.md) |
| completeness-checker | 章节完整性、示例完整性 | [查看](completeness-checker/SKILL.md) |
| quality-scorer | 综合质量评分 | [查看](quality-scorer/SKILL.md) |

## 输入

- 文档集（来自 production 阶段）

## 输出

```yaml
quality_report:
  overall_score: 0.87
  consistency:
    score: 0.92
    issues:
      - type: terminology
        doc: "API-001"
        detail: "使用了'用户'，其他文档使用'User'"
  completeness:
    score: 0.85
    missing_sections:
      - doc: "TEST-001"
        section: "多端兼容测试矩阵"
  scoring_breakdown:
    format: 1.0
    consistency: 0.92
    completeness: 0.85
    traceability: 0.88
    diagram: 0.80
  status: pass  # pass | warning | fail
  threshold: 0.80
```

## 质量阈值

| 评分范围 | 状态 | 处理 |
|---------|------|------|
| ≥ 0.90 | pass | 通过，无问题 |
| 0.80 - 0.89 | pass | 通过，有改进建议 |
| 0.70 - 0.79 | warning | 标注 warning，列出问题 |
| < 0.70 | fail | 不通过，必须修复 |

## 工作流程

1. 读取所有文档
2. 调用 consistency-checker 检查一致性
3. 调用 completeness-checker 检查完整性
4. 调用 quality-scorer 综合评分
5. 输出 quality-report.yaml

## 注意事项

- 评分低于阈值时必须在文档中标注 warning
- 一致性问题是必须修复的（术语、追溯）
- 完整性问题可按优先级分批修复
- 质量报告必须包含详细的问题列表和修复建议
