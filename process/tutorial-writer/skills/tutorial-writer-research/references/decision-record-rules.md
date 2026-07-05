# Research 阶段决策细则

## 本阶段涉及的决策项

| ID | 决策问题 | 为什么要现在确认 |
|----|---------|----------------|
| `content_target_audience` | 目标用户画像？ | 影响全书的语言风格和深度 |
| `content_depth_level` | 内容深度级别？ | 决定每章节的展开程度 |
| `content_text_image_ratio` | 图文比例偏好？ | 影响章节结构和素材准备 |
| `style_writing_tone` | 写作语气？ | 影响全书的表达风格 |
| `style_metaphor_usage` | 使用生活化比喻？ | 认知篇需要用比喻降低门槛 |

## 操作指引

1. PLAN 开始前，检查上述决策是否为 `confirmed` 状态
2. 如有缺失（`pending`），向用户发起讨论，给出选项和推荐值
3. 确认后写入 `decision-record.json` 并更新 Memory
4. 进入 WRITE 前必须确保所有 critical 级决策已确认
