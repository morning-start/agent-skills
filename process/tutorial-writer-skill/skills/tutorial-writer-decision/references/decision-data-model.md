# 决策数据模型

> 本文档定义了决策记录系统的数据模型，包括 5 大类 20 个预定义决策项、状态机和字段定义。

## 决策项分类体系（5 大类 20 个预定义项）

### 基础配置 (Basic Configuration)

影响全局的基础设定，优先级最高。

| ID | 决策问题 | 类型 | 默认值 | 影响范围 |
|----|---------|------|--------|---------|
| `basic_lang_primary` | 教程的主要写作语言？ | 单选 | zh-CN（简体中文） | 全书 |
| `basic_lang_term_handling` | 技术术语如何处理？ | 单选 | first_en_then_zh | 全书 |

**使用场景示例**：
```
用户说："开始写第一章"
→ Agent 检查 basic_lang_primary 状态
→ 若 pending → 发起讨论："请问教程主要用什么语言写？"
→ 若 confirmed(zh-CN) → 直接用中文开始规划
```

---

### 技术选型 (Technical Choices)

决定代码示例和技术栈，影响实操章节。

| ID | 决策问题 | 类型 | 默认值 | 影响范围 |
|----|---------|------|--------|---------|
| `tech_primary_language` | 代码示例主要语言？ | 单选 | python | Ch3-Ch11 |
| `tech_framework_preference` | RAG 框架偏好？ | 多选 | langchain+llamaindex | Ch4-Ch7 |
| `tech_vector_db` | 向量数据库选择？ | 多选 | chromadb+faiss | Ch4, Ch6 |
| `tech_llm_provider` | LLM API 提供商？ | 多选 | openai+local_models | Ch3-Ch7 |

**依赖关系图**：
```
tech_primary_language (Python)
    ↓ 影响
tech_framework_preference (LangChain)
    ↓ 影响
tech_vector_db (ChromaDB)
tech_llm_provider (OpenAI)

建议讨论顺序：language → framework → vector_db → llm
```

---

### 内容策略 (Content Strategy)

决定内容的深度、广度和呈现方式。

| ID | 决策问题 | 类型 | 默认值 | 影响范围 |
|----|---------|------|--------|---------|
| `content_target_audience` | 目标用户画像？ | 单选 | mixed（混合受众） | 全书 |
| `content_depth_level` | 内容深度级别？ | 量表(1-5) | 3（标准级） | 全书 |
| `content_text_image_ratio` | 图文比例偏好？ | 单选 | balanced（均衡） | 全书 |
| `content_example_style` | 代码示例风格？ | 单选 | complete（完整可运行） | Ch3-Ch8 |

**深度级别说明**：

| 级别 | 名称 | 特征 | 适用场景 |
|------|------|------|---------|
| 1 | 概念级 | 只讲是什么 | 快速入门概览 |
| 2 | 入门级 | 基本用法+简单示例 | 动手实验课 |
| 3 | **标准级** | **原理+实践+对比** | **正式教程（默认）** |
| 4 | 深入级 | 源码分析+性能优化 | 进阶专题 |
| 5 | 专家级 | 前沿研究+论文解读 | 学术研讨 |

---

### 风格偏好 (Style Preferences)

决定写作的语气、格式和表达习惯。

| ID | 决策问题 | 类型 | 默认值 | 影响范围 |
|----|---------|------|--------|---------|
| `style_writing_tone` | 写作语气？ | 单选 | professional_practical | 全书 |
| `style_metaphor_usage` | 使用生活化比喻？ | 布尔值 | true | 认知篇 |
| `style_data_citation` | 数据引用严格度？ | 单选 | strict | 全书 |

---

### 项目管理 (Project Management)

决定工作流程和交付标准。

| ID | 决策问题 | 类型 | 默认值 | 影响范围 |
|----|---------|------|--------|---------|
| `project_delivery_format` | 交付物格式？ | 多选 | markdown+web | DELIVER |
| `project_web_ssg` | 网页 SSG 选型？ | 单选 | mkdocs-material | WEB |
| `project_web_diagram` | 图解方案？ | 单选 | mermaid | WEB |
| `project_web_interactive` | 需要交互组件？ | 布尔值 | false | WEB |
| `project_web_deploy` | 部署方式？ | 单选 | github-actions | WEB |
| `project_chapter_order` | 编写顺序？ | 单选 | sequential | WRITE 调度 |
| `project_quality_standard` | 质量标准？ | 单选 | standard | REVIEW |
| `project_version_control` | Git 策略？ | 单选 | branch_per_chapter | 协作流程 |
| `project_feedback_mechanism` | 反馈机制？ | 单选 | milestone_based | 项目周期 |

---

## 决策项状态机

```
                    ┌─────────────┐
                    │   pending   │ ← 初始状态（待讨论）
                    └──────┬──────┘
                           │
              Agent主动发起 / 用户触发
                           ↓
                    ┌─────────────┐
                    │  discussing │ ← 正在讨论中
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ↓            ↓            ↓
       ┌──────────┐  ┌──────────┐  ┌──────────┐
       │ confirmed│  │  deferred│  │ cancelled│
       │  (已确认) │  │  (推迟)  │  │  (取消)  │
       └────┬─────┘  └────┬─────┘  └──────────┘
            │              │
            │ 后续变更请求 │ 到期重新讨论
            ↓              ↓
       ┌──────────┐  ┌──────────┐
       │  changed │  │discussing│
       │  (已变更) │  └──────────┘
       └──────────┘
```

## 字段定义速查

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `id` | string | ✅ | 唯一标识，格式: `{category}_{name}` |
| `category` | enum | ✅ | 分类：基础配置/技术选型/内容策略/风格偏好/项目管理 |
| `question` | string | ✅ | 向用户提问的原话 |
| `type` | enum | ✅ | 值类型：single_choice/multiple_choice/text_input/number/boolean/scale |
| `options` | array | 条件必填 | 可选项列表（choice 类型必须） |
| `default_value` | any | ✅ | 未明确选择时的回退值 |
| `current_value` | any | - | 用户确认后的当前值（null 表示未确认） |
| `status` | enum | ✅ | pending/discussing/confirmed/changed/deferred/cancelled |
| `priority` | enum | ✅ | critical/high/medium/low |
| `dependencies` | array | - | 依赖的其他决策 ID 列表 |
| `impact_scope` | array | - | 影响的章节/模块列表 |
| `reasoning` | string | - | 决策原因/依据 |
| `created_at` | datetime | ✅ | 创建时间 |
| `confirmed_at` | datetime | - | 确认时间 |
| `change_history` | array | - | 变更记录数组 |

---

## 附录：决策项完整清单

| # | ID | 分类 | 问题 | 类型 | 优先级 | 默认值 |
|---|-----|------|------|------|--------|--------|
| 1 | basic_lang_primary | 基础配置 | 教程的主要写作语言？ | single_choice | critical | zh-CN |
| 2 | basic_lang_term_handling | 基础配置 | 技术术语如何处理？ | single_choice | high | first_en_then_zh |
| 3 | tech_primary_language | 技术选型 | 代码示例主要语言？ | single_choice | critical | python |
| 4 | tech_framework_preference | 技术选型 | RAG 实现框架偏好？ | multiple_choice | high | langchain+llamaindex |
| 5 | tech_vector_db | 技术选型 | 向量数据库选择？ | multiple_choice | high | chromadb+faiss |
| 6 | tech_llm_provider | 技术选型 | 大模型 API 提供商？ | multiple_choice | high | openai+local_models |
| 7 | content_target_audience | 内容策略 | 目标用户画像？ | single_choice | critical | mixed |
| 8 | content_depth_level | 内容策略 | 技术内容深度级别？ | scale(1-5) | high | 3 |
| 9 | content_text_image_ratio | 内容策略 | 图文内容比例？ | single_choice | medium | balanced |
| 10 | content_example_style | 内容策略 | 代码示例风格？ | single_choice | medium | complete |
| 11 | style_writing_tone | 风格偏好 | 写作语气/语调？ | single_choice | medium | professional_practical |
| 12 | style_metaphor_usage | 风格偏好 | 使用生活化比喻？ | boolean | low | true |
| 13 | style_data_citation | 风格偏好 | 数据引用严格程度？ | single_choice | high | strict |
| 14 | project_delivery_format | 项目管理 | 最终交付物格式？ | multiple_choice | medium | markdown+pdf |
| 15 | project_chapter_order | 项目管理 | 章节编写顺序？ | single_choice | medium | sequential |
| 16 | project_quality_standard | 项目管理 | 质量标准严格程度？ | single_choice | high | standard |
| 17 | project_version_control | 项目管理 | 版本控制策略？ | single_choice | low | branch_per_chapter |
| 18 | project_feedback_mechanism | 项目管理 | 反馈和迭代机制？ | single_choice | low | milestone_based |

---

**最后更新**: 2026-05-25
**版本**: v1.0.0
**作者**: RAG 教程项目组 + Skill Factory 优化
