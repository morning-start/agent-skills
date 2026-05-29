---
name: tutorial-writer-writing
version: v3.2.0
author: skill-factory
description: Use when writing, editing, or completing technical tutorial chapter content
tags: [tutorial, writing, content-creation, code-examples, asset-management, self-check]
---

# Tutorial Writer — ✍️ 撰写执行

## 技能定位

本子技能负责教程创作的 **中期撰写执行阶段**（PRWRD+D 中的 WRITE），按已确认的规划产出高质量章节内容。

**核心理念切换**: 传统教程写作输出的是"静态文档"，网页优先写作输出的是**交互式学习体验的蓝本**。每写一段内容，都要思考它在网页上如何呈现、如何交互、如何引导读者探索。

**输入**: 已确认的章节执行计划 + 归档资料
**输出**: `book/` 中的完成初稿章节 .md 文件（包含交互组件占位标记）

## 核心流程

```
① 在 book/ 中按规划逐节撰写（先讲原理再给实践）
    │
    ├── ② 写作过程收集资料：
    │   ├── 截图 → web/assets/images/（统一 PNG/WebP，800-1200px）
    │   ├── 代码运行结果 → 内嵌在代码块后
    │   ├── 对比数据 → 内嵌表格或 reference/
    │   └── 架构图/Mermaid 代码 → 验证语法后写入章节
    │
    ├── ③ 遵循写作规范（references/writing-standards.md）
    │   ├── R1: 使用目标语言
    │   ├── R2: 无注释性文字
    │   ├── R3: 关键数据标注来源
    │   ├── R4: 代码块标注语言
    │   ├── R5: 内容对齐大纲
    │   └── R6: 资料归档到指定目录
    │
    ├── ④ 实时感知累计行数
    │   ├── 60% → 正常继续
    │   ├── 80% → 开始收尾
    │   └── 120% → 触发过长预警
    │
    ├── ⑤ **网页优先增强**：检查每个核心概念能否用交互组件增强
    │   ├── 概念能否用交互式图解替代静态截图？
    │   ├── 代码能否做成可运行沙盒？
    │   ├── 数据能否用动画图表呈现？
    │   ├── 知识检验能否插入快速测验？
    │   └── 步骤流程能否用滚动触发动画逐步揭示？
    │
    ├── ⑥ 每小节完成后的自检
    │   ├── 逻辑连贯性
    │   ├── 数据准确性
    │   └── 见 references/quality-self-check.md
    │
    └── ⑦ 整章完成后同步 book/ → web/chapters/
        └── cp book/chXX-*.md web/chapters/
```

## 写作过程收集资料

| 资料类型 | 来源 | 保存位置 | 命名规范 |
|---------|------|---------|---------|
| 截图/图示 | 自行截图、工具生成 | `web/assets/images/` | `ch{02}-{描述}.png` |
| 代码输出 | 终端运行结果 | 内嵌在代码块后 | 直接写 |
| Mermaid 图 | 在线工具验证语法后 | 内嵌在 Markdown 中 | mermaid 代码块 |
| 对比数据 | 运行基准测试 | 正文表格或 `reference/` | 按分类归档 |
| **交互组件数据** | **JSON 格式的结构化数据** | `web/js/*-data.json` | 与组件同名 |
| **沙盒代码示例** | **可独立运行的代码片段** | `web/js/` 或 inline | `playground-{序号}.js` |
| **3D 场景数据** | **Three.js 场景配置** | `web/js/3d/` | `{场景名}.js` |

## 参考文件

- [写作规范](references/writing-standards.md) — R1-R6 强制规则 + S1-S5 推荐惯例
- [写作中自检清单](references/quality-self-check.md) — 每小节完成后的即时检查
- [本阶段决策细则](references/decision-record-rules.md) — writing 阶段涉及的决策项
