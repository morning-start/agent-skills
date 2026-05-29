---
name: consistency-checker
version: 0.1.0
description: 检查文档间的术语、追溯关系、格式一致性
---

# Consistency Checker

## 职责

- 检查术语命名一致性
- 检查追溯关系完整性
- 检查格式一致性
- 检查数据参数一致性

## 输入

- 文档集

## 输出

```yaml
consistency_result:
  score: 0.92
  issues:
    - type: terminology
      severity: warning
      docs: ["REQ-001", "ARCH-001"]
      detail: "REQ-001使用'用户'，ARCH-001使用'User'"
      suggestion: "统一使用'用户'"
    - type: traceability
      severity: error
      docs: ["API-001"]
      detail: "API-001 depends_on 指向 ARCH-001，但 ARCH-001 feeds_into 不包含 API-001"
      suggestion: "修复追溯关系双向对应"
```

## 检查项

### 术语一致性

- 同一概念在各文档中使用相同术语
- 检查中英文术语混用
- 检查缩写使用一致性
- 输出术语对照表

### 追溯一致性

- `A feeds_into B` 必须等价于 `B depends_on A`
- 追溯链不能有断点
- 追溯链不能有循环

### 格式一致性

- YAML front matter 格式统一
- 标题层级统一
- 代码块语言标注统一
- 列表风格统一

### 数据一致性

- API 接口定义在架构和 API 文档中一致
- 数据模型在架构和数据文档中一致
- 版本号在各文档中一致

## 严重级别

| 级别 | 含义 | 处理 |
|------|------|------|
| error | 必须修复 | 阻断发布 |
| warning | 建议修复 | 标注 warning |
| info | 可选优化 | 记录建议 |

## 注意事项

- error 级别问题必须修复才能通过质量检查
- 术语检查需要参考术语对照表
- 追溯检查需要双向验证
