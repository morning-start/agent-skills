---
name: current-state-scanner
version: 0.1.0
description: 扫描项目中现有文档和代码，评估文档完整性和质量现状
---

# Current State Scanner

## 职责

- 扫描项目中的现有文档
- 评估文档完整性和质量
- 识别文档间的追溯关系
- 输出文档现状报告

## 输入

- 项目根目录路径
- 可选：指定文档目录

## 输出

```yaml
current_state_report:
  existing_docs:
    - type: requirement
      path: docs/srs.md
      format: markdown
      has_frontmatter: false
      quality_score: 0.7
      issues:
        - "缺少非功能需求章节"
        - "未标注版本号"
    - type: api
      path: docs/api.md
      format: markdown
      has_frontmatter: true
      quality_score: 0.85
      issues: []
  traceability_matrix:
    req_to_arch: partial
    arch_to_api: complete
    api_to_test: missing
  coverage:
    requirement: 0.7
    architecture: 0.5
    api: 0.85
    test: 0.0
    overall: 0.51
```

## 扫描规则

### 文档识别

| 文件名模式 | 文档类型 |
|-----------|---------|
| README.md | 基础文档 |
| CHANGELOG.md | 变更记录 |
| *requirement*, *srs*, *prd* | 需求文档 |
| *architecture*, *design*, *sad*, *tdd* | 架构文档 |
| *api*, *interface*, *endpoint* | API 文档 |
| *database*, *schema*, *data* | 数据文档 |
| *test*, *quality*, *qa* | 质量文档 |

### 质量评估维度

1. **格式规范**（20%）：是否有 YAML front matter、标题层级是否正确
2. **内容完整**（30%）：是否包含必需章节
3. **术语一致**（20%）：术语使用是否统一
4. **追溯完整**（15%）：是否有追溯关系标注
5. **时效性**（15%）：最后更新时间是否在合理范围内

## 注意事项

- 扫描结果仅作为参考，不替代用户判断
- 对现有文档保持只读，不修改原文件
- 质量评分低于 0.6 时需列出具体问题
- 识别到的追溯关系输出为矩阵形式
