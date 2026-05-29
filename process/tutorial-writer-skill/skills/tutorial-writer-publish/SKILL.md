---
name: tutorial-writer-publish
version: v3.2.0
author: skill-factory
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
    ├── ④ 本地验证：uv run mkdocs build --strict（无 error/warning）
    ├── ⑤ 提交并打 tag
    │   ├── git add . && git commit -m "feat: 第X章"
    │   └── git tag v{major}.{minor}.{patch}
    └── ⑥ 发布
        ├── git push && git push --tags
        │   └── GitHub Actions 自动: validate → build → deploy
        └── 或手动触发: gh workflow run deploy.yml -f version=vX.Y.Z
```

## 能力速查

| 能力 | 技术方案 | 复杂度 |
|------|---------|--------|
| 多级导航 + 全文搜索 | MkDocs Material 内置 | 零配置 |
| 架构图 / 流程图 | Mermaid 代码块 | 内置支持 |
| 代码复制 + 行号 | `content.code.copy` 等特性 | 一行配置 |
| 暗色模式切换 | Material palette | 一行配置 |
| **可拖拽时间轴** | **自定义 JS + JSON 数据** | **需手动实现** |
| **滚动触发动效** | **Intersection Observer + CSS 过渡** | **轻量实现** |
| **交互代码沙盒** | **Monaco Editor + Pyodide** | **中等复杂度** |
| **3D 架构可视化** | **Three.js + OrbitControls** | **中等复杂度** |
| **交互测验卡片** | **Vanilla JS 选择题组件** | **轻量实现** |
| **动画数据仪表盘** | **Chart.js / D3.js** | **轻量实现** |
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
| W8 | 3D 场景渲染无白屏 | WebGL 初始化正常，fallback 图片备选 |
| W9 | 代码沙盒可运行 | Monaco 编辑器加载正常，Pyodide 可执行 |
| W10 | 动效无障碍 | `prefers-reduced-motion` 时动效关闭 |
| W11 | 交互测验功能完整 | 选项点击反馈、正确答案展示、解析文字显示 |
| W12 | 动画图表渲染正常 | Chart.js/D3.js 数据加载后图表正常展示 |
| W13 | 构建无警告 | `mkdocs build` 无 error/warning |

## 参考文件

- [网页发布完整指南](references/web-publishing.md) — MkDocs 配置 + 交互组件 + Tag 驱动部署 + GitHub Actions
- [本阶段决策细则](references/decision-record-rules.md) — publish 阶段涉及的决策项
