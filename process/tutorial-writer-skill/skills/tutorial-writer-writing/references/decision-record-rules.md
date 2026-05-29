# Writing 阶段决策细则

## 本阶段涉及的决策项

| ID | 决策问题 | 为什么要现在确认 |
|----|---------|----------------|
| `tech_language` | 编程语言？ | 决定代码示例的语言和运行环境 |
| `tech_framework_preference` | 编排框架偏好？ | 决定 Ch5-Ch13 的代码架构 |
| `tech_vector_database` | 向量数据库选型？ | 决定 Ch4-Ch11 的存储代码 |
| `tech_llm_selection` | LLM 选型？ | 决定 API 调用方式和 prompt 设计 |
| `content_example_style` | 代码示例风格？ | 决定代码的完整性和注释方式 |
| `style_data_citation` | 数据引用严格度？ | 决定引用格式和验证要求 |

## 操作指引

1. 进入 WRITE 前，检查技术选型类决策是否已确认
2. 撰写过程中随时通过 Memory 读取决策值
3. 如遇到"需要决策但未定义"的情况，暂停并调用 decision 子技能
4. 每节完成后检查代码示例是否与决策一致
