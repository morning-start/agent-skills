---
name: quality-scorer
version: 0.1.1
description: Use when the user needs a computed document quality score or a weighted scoring breakdown.
tags: [scoring, quality-metrics, documentation]
---

# Quality Scorer

## 职责

- 汇总一致性、完整性检查结果
- 按权重计算综合质量分数
- 判断是否通过质量门禁
- 输出详细评分报告

## 输入

- consistency_result
- completeness_result

## 输出

```yaml
quality_score:
  overall: 0.87
  breakdown:
    format: 1.00       # 格式规范（10%）
    consistency: 0.92  # 一致性（25%）
    completeness: 0.85 # 完整性（25%）
    traceability: 0.88 # 追溯完整性（20%）
    diagram: 0.80      # 图示覆盖（20%）
  status: pass
  threshold: 0.80
  details:
    total_issues: 3
    errors: 0
    warnings: 2
    info: 1
```

## 评分权重

| 维度 | 权重 | 说明 |
|------|------|------|
| 格式规范 | 10% | YAML front matter、标题层级 |
| 一致性 | 25% | 术语、格式、数据一致 |
| 完整性 | 25% | 章节、示例完整 |
| 追溯完整性 | 20% | depends_on/feeds_into 双向对应 |
| 图示覆盖 | 20% | 复杂文档有图示 |

## 评分计算

```
overall = format * 0.10 + consistency * 0.25 + completeness * 0.25 + traceability * 0.20 + diagram * 0.20
```

## 状态判定

| overall | status | 处理 |
|---------|--------|------|
| ≥ 0.90 | pass | 通过 |
| 0.80 - 0.89 | pass | 通过，有建议 |
| 0.70 - 0.79 | warning | 标注警告 |
| < 0.70 | fail | 不通过 |

## 注意事项

- 任何 error 级别问题自动将状态设为 fail
- 评分必须精确到两位小数
- 必须输出详细 breakdown 供改进参考
