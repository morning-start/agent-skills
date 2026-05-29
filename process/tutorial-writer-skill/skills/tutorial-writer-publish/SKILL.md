---
name: tutorial-writer-publish
version: v3.0.0
author: RAG 教程项目组
description: Use when deploying technical tutorial content as a web site via MkDocs, GitHub Pages, or managing interactive components like timelines
tags: [tutorial, publishing, mkdocs, github-pages, web, mermaid, interactive]
---

# Tutorial Writer — 🌐 网页发布

## 技能定位

本子技能负责教程创作的 **交付与网页发布阶段**（PRWRD+D 中的 DELIVER + WEB），将 Markdown 章节转换为交互式网页并部署。

**输入**: 已通过质量门禁的章节 .md 文件
**输出**: 部署到 GitHub Pages 的静态网站

## 核心流程

```
章节内容已通过 REVIEW
    │
    ├── ① 将 .md 文件放入 docs/chapters/
    ├── ② 更新 mkdocs.yml 的 nav 配置
    ├── ③ 如需交互组件 → 添加 JS/CSS 文件
    ├── ④ 本地验证：uv run mkdocs build（无报错）
    └── ⑤ 部署
        ├── 推送 main 分支 → GitHub Actions 自动构建
        └── 或手动：uv run mkdocs gh-deploy --force
```

## 能力速查

| 能力 | 技术方案 | 复杂度 |
|------|---------|--------|
| 多级导航 + 全文搜索 | MkDocs Material 内置 | 零配置 |
| 架构图 / 流程图 | Mermaid 代码块 | 内置支持 |
| 代码复制 + 行号 | `content.code.copy` 等特性 | 一行配置 |
| 暗色模式切换 | Material palette | 一行配置 |
| **可拖拽时间轴** | **自定义 JS + JSON 数据** | **需手动实现** |
| 响应式移动端适配 | Material 主题自带 | 自动 |
| 自动化构建部署 | GitHub Actions workflow | 一次配置 |

## 质量检查（发布前）

| # | 检查项 | 标准 |
|---|--------|------|
| W1 | 所有图片可访问 | 路径在构建后有效 |
| W2 | Mermaid 图正常渲染 | 所有 mermaid 代码块可见 |
| W3 | 导航结构完整 | 所有章节可达 |
| W4 | 跨章链接有效 | 不指向不存在的页面 |
| W5 | 交互组件功能正常 | 拖拽/点击/切换无障碍 |
| W6 | 响应式布局 | 375px / 768px / 1280px 可用 |
| W7 | 暗色模式兼容 | 对比度达标 |
| W8 | 构建无警告 | `mkdocs build` 无 error/warning |

## 参考文件

- [网页发布完整指南](references/web-publishing.md) — MkDocs 配置 + Mermaid + 时间轴组件 + GitHub Actions
- [本阶段决策细则](references/decision-record-rules.md) — publish 阶段涉及的决策项
