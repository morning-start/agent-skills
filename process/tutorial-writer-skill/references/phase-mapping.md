# 阶段→决策项映射

> 定义 5 个子技能对应 PRWRD+D 流程中的位置，以及每个阶段涉及的核心决策项。

## 整体映射

```
PRWRD+D 流程     → 负责子技能
─────────────────   ──────────────────
DECISION (贯穿)     decision (📐)
PLAN + RESEARCH      research (📚)
WRITE                writing (✍️)
REVIEW               review (✅)
DELIVER + WEB        publish (🌐)
```

## 各阶段决策项一览

### 📚 research 阶段决策

| 决策项 | 问题 | 影响 |
|--------|------|------|
| `content_target_audience` | 目标用户画像？ | 全书 |
| `content_depth_level` | 内容深度级别？ | 全书 |
| `content_text_image_ratio` | 图文比例偏好？ | 全书 |
| `style_writing_tone` | 写作语气？ | 全书 |
| `style_metaphor_usage` | 使用生活化比喻？ | 认知篇 |

### ✍️ writing 阶段决策

| 决策项 | 问题 | 影响 |
|--------|------|------|
| `tech_language` | 编程语言？ | Ch3-Ch11 |
| `tech_framework_preference` | 编排框架偏好？ | Ch5-Ch13 |
| `tech_vector_database` | 向量数据库选型？ | Ch4-Ch11 |
| `tech_llm_selection` | LLM 选型？ | 全书 |
| `content_example_style` | 代码示例风格？ | Ch3-Ch8 |
| `style_data_citation` | 数据引用严格度？ | 全书 |

### ✅ review 阶段决策

| 决策项 | 问题 | 影响 |
|--------|------|------|
| `project_quality_standard` | 质量标准？ | REVIEW |
| `style_data_citation` | 数据引用严格度（验证） | 全书 |
| (跨章规则) | R7-R10 一致性验证 | 全书 |

### 🌐 publish 阶段决策

| 决策项 | 问题 | 影响 |
|--------|------|------|
| `project_delivery_format` | 交付物格式？ | DELIVER |
| `project_web_ssg` | SSG 选型？ | WEB |
| `project_web_diagram` | 图解方案？ | WEB |
| `project_web_interactive` | 需要交互组件？ | WEB |
| `project_web_deploy` | 部署方式？ | WEB |

### 📐 decision 阶段决策

| 决策项 | 问题 | 影响 |
|--------|------|------|
| (所有决策的管理) | 创建/修改/冲突解决 | 全过程 |
| `project_version_control` | Git 策略？ | 协作流程 |
| `project_feedback_mechanism` | 反馈机制？ | 项目周期 |

## 决策项的三种状态

```
pending    → 待讨论（初始）
discussing → 讨论中
confirmed  → 已确认（可执行）
deferred   → 延后讨论
```

状态变更由 decision 子技能统一管理，各子技能仅读取 `confirmed` 状态的决策。
