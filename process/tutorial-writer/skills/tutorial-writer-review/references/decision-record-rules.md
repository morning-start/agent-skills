# Review 阶段决策细则

## 本阶段涉及的决策项

| ID | 决策问题 | 如何验证 |
|----|---------|---------|
| `project_quality_standard` | 质量标准？ | 按对应级别执行门禁检查 |
| `style_data_citation` | 数据引用严格度？ | 验证所有数据点有对应来源标注 |

## 跨章验证

Review 阶段需要验证 writing 阶段遵循的决策是否正确执行：

| 决策 | 验证方式 |
|------|---------|
| `tech_language` | 代码语言是否统一 |
| `tech_framework_preference` | 所有章节框架引用一致 |
| `content_example_style` | 代码示例风格一致 |

## 操作指引

1. 加载 `decision-record.json` 读取相关决策值
2. 在 Q10-Q11 检查中使用决策值作为判断基准
3. 如发现内容与决策不一致，标记为不通过并说明原因
