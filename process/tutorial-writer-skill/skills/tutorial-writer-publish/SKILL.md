---
name: tutorial-writer-publish
version: v4.1.0
author: skill-factory
description: Use when deploying technical tutorial content as a web site via GitHub Pages using Astro + Starlight — project planning, modular configuration, community plugins, content conventions, and deployment
tags: [tutorial, publishing, astro, github-pages, web, starlight, ssg, plugins]
---

# Tutorial Writer — 🌐 网页发布（Astro + Starlight）

## 技能定位

本子技能负责教程创作的 **交付与发布阶段**，基于 Astro 框架 + Starlight 文档主题将 Markdown 教程输出为 GitHub Pages 静态网站。提供从项目规划、模块化配置、社区生态到部署的完整指南。

**输入**: 已通过质量门禁的章节 .md 文件
**输出**: Astro + Starlight 项目的完整规划、配置方案、目录结构约定、部署配置

**为什么选择 Astro + Starlight**:
| 特性 | 说明 |
|------|------|
| 零 JS 默认输出 | 教程页面默认不加载 JS，Lighthouse 评分 97-100 |
| Islands 架构 | 仅在需要交互的地方加载框架组件（React/Vue/Svelte） |
| Content Collections | 类型安全的 Markdown 内容管理，Zod 检验 frontmatter |
| Starlight 主题 | 内置搜索 / 侧边栏导航 / 暗色模式 / 代码高亮 / i18n |
| 搜索 | 默认 Pagefind 构建时搜索，零外部依赖, 无额外成本 |
| 组件覆盖 | 可覆盖 Starlight 任意内置组件，深度定制 UI |
| 插件生态 | 官方 + 社区插件体系，功能可扩展 |
| 部署 | `withastro/action` 一键部署到 GitHub Pages |
| 社区案例 | Cloudflare 文档、Astro 官方文档、WP Engine 案例 |

## 启动流程

```
① 项目初始化 ──────────────────────────
   npm create astro@latest -- --template starlight

② 配置基础信息 ────────────────────────
   astro.config.mjs: title / description / logo / social / site / base

③ 配置侧边栏导航 ──────────────────────
   手动分组 / 自动生成 / 混合模式

④ 配置 Content Collections ───────────
   src/content.config.ts: docsSchema + 自定义 frontmatter 字段

⑤ 迁移章节内容 ────────────────────────
   book/ → src/content/docs/

⑥ 添加插件（按需）─────────────────────
   官方插件 / 社区插件

⑦ 添加交互组件（按需）─────────────────
   React/Vue/Svelte Islands

⑧ 部署 ────────────────────────────────
   GitHub Actions → GitHub Pages

⑨ 质量验证 ────────────────────────────
   构建检查 + Lighthouse + 链接验证 + 响应式
```

## 模块化配置

### 配置分层结构

```
astro.config.mjs（主配置）
├── site / base          # 部署 URL 配置
├── integrations         # Starlight 集成 + 其他 Astro 集成
│   └── starlight({...}) # Starlight 主题配置
│       ├── 基础: title / description / logo / favicon
│       ├── 社交: social（github / twitter / mastodon / discord / youtube）
│       ├── 导航: sidebar（手动 / 自动 / 混合）
│       ├── 搜索: 默认 Pagefind / 可替换 DocSearch
│       ├── 插件: plugins[]（官方 + 社区）
│       ├── 组件覆盖: components（覆盖内置组件）
│       ├── 页面元素: head / editLink / lastUpdated / pagination
│       └── 多语言: locales / defaultLocale
└── 其他 Astro 配置: output / adapter / vite / markdown / image
```

### Starlight 配置全景

| 配置项 | 类型 | 说明 | 必要性 |
|--------|------|------|--------|
| `title` | string | 站点标题（浏览器标签 + meta） | ✅ 必填 |
| `description` | string | 站点描述（SEO meta） | 推荐 |
| `logo` | object | Logo 图片（支持 light/dark 双版本） | 可选 |
| `favicon` | string | Favicon 路径 | 可选 |
| `social` | object | 社交链接（显示在导航栏） | 可选 |
| `sidebar` | array | 侧边栏导航配置 | ✅ 推荐 |
| `tableOfContents` | object/false | 目录层级（默认 h2-h3） | 可选 |
| `editLink` | object | "编辑此页"链接 | 推荐 |
| `lastUpdated` | boolean | 显示最后更新时间 | 推荐 |
| `pagination` | boolean | 上一页/下一页导航 | 可选 |
| `search` | object | 搜索配置 | 可选 |
| `plugins` | array | Starlight 插件列表 | 可选 |
| `components` | object | 覆盖内置组件 | 可选 |
| `head` | array | 自定义 <head> 标签 | 可选 |
| `locales` | object | 多语言配置 | 可选 |
| `defaultLocale` | string | 默认语言 | 可选 |

### 侧边栏导航模式

Starlight 支持三种侧边栏配置策略，可按章节混合使用：

**手动模式** — 精确控制章节顺序和结构：
```
sidebar: [
  { label: '第一章', slug: 'ch01-概述' },
  { label: '第二章', slug: 'ch02-入门' },
  { label: '进阶', items: [
    { label: '第三章', slug: 'ch03-进阶' },
    { label: '第四章', slug: 'ch04-深入' },
  ]},
]
```

**自动生成** — 基于文件系统自动生成：
```
sidebar: [
  { label: '入门', autogenerate: { directory: 'getting-started' }},
  { label: '进阶', autogenerate: { directory: 'advanced' }},
]
```

**混合模式** — 手动项与自动生成混合：
```
sidebar: [
  { label: '首页', slug: 'index' },
  { label: '教程', autogenerate: { directory: 'tutorial' }},
  { label: '附录', items: [
    { slug: 'appendix/faq' },
    { slug: 'appendix/changelog' },
  ]},
]
```

### Content Collections 方案

通过 `src/content.config.ts` 定义教程章节的 frontmatter schema：

**基础方案**（Starlight 默认）:
```
docsSchema() 自动处理: title / description / slug / draft / sidebar
```

**扩展方案**（添加自定义字段）:
```
docsSchema({ schema: z.object({
  tags: z.array(z.string()).optional(),
  difficulty: z.enum(['beginner', 'intermediate', 'advanced']).optional(),
  readingTime: z.number().optional(),
  coverImage: z.string().optional(),
})})
```

**适用场景**:
- 按标签分类检索 → 添加 `tags` 字段
- 按难度分级 → 添加 `difficulty` 字段
- 显示预估阅读时间 → 添加 `readingTime` 字段
- SEO 优化 → 利用 Starlight 内置的 `description` 和 `head` frontmatter

## 插件与组件生态

### 官方插件

| 插件 | 用途 | 适用场景 |
|------|------|---------|
| `@astrojs/starlight-docsearch` | 替换 Pagefind 为 Algolia DocSearch | 需要搜索分析/建议的站点 |
| `@astrojs/starlight-tailwind` | Tailwind CSS v4 兼容 | 使用 Tailwind 定制样式 |
| `@astrojs/starlight-markdoc` | 启用 Markdoc 格式 | 需要比 MDX 更灵活的内容格式 |

### 社区插件（按人气排序）

| 插件 | Stars | 用途 | 教程场景 |
|------|-------|------|---------|
| **starlight-blog** | ⭐264 | 在文档站点中添加博客 | 教程更新日志、发布公告 |
| **starlight-links-validator** | ⭐109 | 构建时验证内部链接 | 确保跨章链接不失效 |
| **starlight-openapi** | — | 从 OpenAPI/Swagger 生成文档 | API 教程自动生成 |
| **starlight-obsidian** | — | 发布 Obsidian 知识库 | 从 Obsidian 直接发布教程 |
| **starlight-versions** | — | 多版本文档管理 | 教程不同版本切换 |
| **starlight-sidebar-topics** | — | 多分区独立侧边栏 | 不同模块 / 不同课程的分区 |
| **starlight-image-zoom** | — | 图片点击缩放 | 架构图 / 截图放大查看 |
| **starlight-heading-badges** | — | 标题徽章 | 标注"新"、"已更新"、"实验性" |
| **starlight-site-graph** | — | 交互式站点图谱 | 教程知识图谱可视化 |
| **starlight-utils** | — | 通用工具集合 | 多页面共享工具函数 |
| **starlight-view-modes** | — | 不同视图模式切换 | 阅读/演示/全屏模式 |
| **starlight-spell-checker** | — | 拼写检查（多语言） | 文档质量保障 |
| **starlight-showcases** | — | 作品展示组件集 | 教程案例 / 学员作品展示 |
| **star-warp** | — | 搜索体验增强 | 更快的搜索导航体验 |
| **starlight-sidebar-swipe** | — | 移动端侧边栏滑动 | 移动端用户体验优化 |
| **starlight-contributor-list** | — | 贡献者列表组件 | 多人协作教程致谢 |
| **starlight-save-file-component** | — | 文件下载组件 | 提供示例代码下载 |
| **starlight-cooler-credit** | — | 美化 Starlight 版权声明 | 页脚美化 |
| **starlight-plugin-show-latest-version** | — | 显示最新版本号 | 教程配套项目的版本展示 |

### 社区主题

| 主题 | 说明 |
|------|------|
| **starlight-nextjs-theme** | 类 Next.js 文档风格的 Starlight 主题 |

### 插件选择策略

```
教程需要...
├── 链接质量保障             → starlight-links-validator
├── 多版本文档               → starlight-versions
├── 模块化分区               → starlight-sidebar-topics
├── 发布日志 / 新闻          → starlight-blog
├── API 自动生成             → starlight-openapi
├── 从 Obsidian 发布         → starlight-obsidian
├── 图片放大查看             → starlight-image-zoom
├── 标题标注状态             → starlight-heading-badges
├── 知识图谱可视化           → starlight-site-graph
├── 多视图模式               → starlight-view-modes
├── 拼写检查                 → starlight-spell-checker
├── 展示案例                 → starlight-showcases
├── 贡献者列表               → starlight-contributor-list
├── 下载按钮                 → starlight-save-file-component
├── 自定义搜索               → @astrojs/starlight-docsearch
└── Tailwind 样式            → @astrojs/starlight-tailwind
```

### 交互组件框架选择

需要交互功能时，选择 Islands 组件框架：

| 框架 | 熟悉度 | 包体积 | 适用场景 |
|------|--------|--------|---------|
| **React** | 最广泛 | ~130KB | 通用交互，生态最丰富 |
| **Vue** | 较广 | ~100KB | Vue 技术栈教程 |
| **Svelte** | 新兴 | ~30KB | 极致性能，最小包体积 |
| **Solid** | 小众 | ~20KB | 极致性能，响应式粒度最细 |
| **Preact** | 中等 | ~10KB | React 兼容，超轻量 |

> 交互组件的具体实现 → 调用对应 UI 框架技能。

## 项目结构规范

### 推荐目录组织

```
tutorial-site/
│
├── astro.config.mjs          # Astro + Starlight 核心配置
├── tsconfig.json             # TypeScript 配置
├── package.json              # 依赖管理
│
├── src/
│   ├── content/
│   │   ├── docs/             # 教程章节 (Markdown/MDX)
│   │   │   ├── index.md      # 首页 / 概览
│   │   │   ├── ch01-概述.md
│   │   │   ├── ch02-入门/
│   │   │   │   ├── index.md
│   │   │   │   ├── 01-安装.md
│   │   │   │   └── 02-配置.md
│   │   │   └── ...
│   │   └── config.ts         # Content Collections 配置
│   │
│   ├── components/           # 自定义组件
│   │   ├── react/            # React Islands 组件
│   │   │   ├── Quiz.tsx
│   │   │   └── CodeSandbox.tsx
│   │   ├── ui/               # 通用 UI 组件
│   │   │   └── Badge.astro
│   │   └── overrides/        # Starlight 内置组件覆盖
│   │       └── Header.astro
│   │
│   ├── layouts/              # 布局覆盖
│   ├── assets/               # 图片等资源
│   │   └── images/
│   └── styles/               # 自定义 CSS
│       └── custom.css
│
├── public/                   # 直接复制的资源
│   ├── favicon.svg
│   └── og-default.png        # 默认 OG 图片 (1200×630)
│
├── book/                     # （可选）原始编辑源
│
└── .github/workflows/
    └── deploy.yml            # GitHub Actions 部署
```

### 大型教程的模块化组织

超过 20 章的教程推荐按模块拆分目录：

```
src/content/docs/
├── index.md                          # 教程首页
├── 01-基础篇/
│   ├── index.md                      # 模块概览
│   ├── 01-环境准备.md
│   ├── 02-核心概念.md
│   └── 03-快速上手.md
├── 02-进阶篇/
│   ├── index.md
│   ├── 01-性能优化.md
│   └── ...
├── 03-实战篇/
│   ├── index.md
│   ├── 01-项目一.md
│   └── ...
└── appendix/
    ├── faq.md
    ├── changelog.md
    └── references.md
```

侧边栏配置对应：
```
sidebar: [
  { label: '教程简介', slug: 'index' },
  { label: '基础篇', autogenerate: { directory: '01-基础篇' }},
  { label: '进阶篇', autogenerate: { directory: '02-进阶篇' }},
  { label: '实战篇', autogenerate: { directory: '03-实战篇' }},
  { label: '附录', autogenerate: { directory: 'appendix' }},
]
```

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 内容文件 | 数字前缀排序 + kebab-case | `01-环境准备.md` |
| 组件文件 | PascalCase | `CodeSandbox.tsx`, `QuizCard.astro` |
| 样式文件 | kebab-case | `custom.css` |
| 资源文件 | 语义化命名 | `rag-architecture.png` |
| 目录名 | kebab-case | `01-基础篇/` |

## 社区构建经验

### 内容组织最佳实践

- **每章一个文件**：章节内容 ≤ 2000 行，超长则拆分子章节
- **Frontmatter 完整**：每页必填 `title` + `description`（SEO + 搜索）
- **图片统一管理**：`src/assets/images/`，WebP 格式，宽度 800-1200px
- **代码块有语言标注**：` ```python ` 而非 ` ``` `，启用行号
- **跨章节链接使用相对路径**：`../02-进阶/01-配置.md`
- **将 frontmatter schema 作为合同**：Zod schema 定义所有页面必须遵守的字段契约

### 性能优化

- 图片使用 WebP / AVIF 格式，利用 Astro 内置的 `astro:assets` 处理
- 避免在每页加载全局 JS，交互组件仅在需要页面加载
- 使用 Starlight 内置的分页代替自定义导航组件
- 合理设置 `tableOfContents` 层级，避免过深目录（默认 h2-h3 足够）
- 构建时链接验证防止 404 → `starlight-links-validator`

### i18n 多语言策略

需要多语言教程时，利用 Starlight 内置多语言支持：
- `locales` 配置定义支持的语言
- `src/content/docs/` 下按语言分区（en/ zh/ ja/ 等）
- 配置 `defaultLocale` 指定默认语言
- 参考 [Starlight i18n 文档](https://starlight.astro.build/guides/i18n/)

### 版本化文档

教程有多个版本（如 v1/v2）时：
- **推荐方案**: 每个大版本独立仓库 + 独立部署
- **备选方案**: 使用 `starlight-versions` 插件
- **文档内标注**: 使用 `starlight-heading-badges` 标注"新"、"已弃用"

## 部署

### GitHub Actions（withastro/action）

```yaml
# .github/workflows/deploy.yml
# 官方推荐方式：使用 withastro/action
# push 到 main 分支自动部署
# 也可手动触发 workflow_dispatch
# 配置前提: astro.config.mjs 中 site + base 正确
# GitHub Pages 设置 Source → GitHub Actions
```

### 部署前检查清单

| # | 检查项 | 方式 |
|---|--------|------|
| 1 | `npm run build` 无错误 | 终端执行 |
| 2 | `astro.config.mjs` 中 `site` 和 `base` 正确 | 检查配置 |
| 3 | GitHub Pages 源设为 GitHub Actions | 仓库 Settings |
| 4 | 自定义域名 DNS 配置（如有） | DNS 验证 |
| 5 | 构建后 `dist/` 文件结构正确 | `npm run preview` 预览 |

## 质量门禁

| # | 检查项 | 标准 | 工具/方式 |
|---|--------|------|----------|
| W1 | 构建无错误 | `npm run build` 返回 0 | CI |
| W2 | 资源可访问 | 无 404 图片/CSS/JS | `starlight-links-validator` |
| W3 | 跨章链接有效 | 无内部死链 | `starlight-links-validator` |
| W4 | 导航结构完整 | 所有章节在侧边栏可达 | 人工巡查 |
| W5 | 交互组件可运行 | 浏览器控制台 error = 0 | 手动测试 |
| W6 | 响应式布局 | 375px / 768px / 1280px 可用 | 浏览器 DevTools |
| W7 | 暗色模式兼容 | 文字/背景对比度 ≥ 4.5:1 | 手动切换验证 |
| W8 | 搜索可用 | 关键词可搜索到对应页面 | 手动测试 |
| W9 | Lighthouse | Performance ≥ 90, Accessibility ≥ 90 | Chrome DevTools |
| W10 | SEO | 每页有 title + description meta | 构建后检查 HTML |
| W11 | 无敏感信息 | API Key / 密码 / 内网地址已脱敏 | 代码审查 |
| W12 | 无障碍 | 键盘导航 + 屏幕阅读器 | NVDA / VoiceOver |

## 参考文件

- [网页发布完整指南](references/web-publishing.md) — Astro + Starlight 配置详解 + 插件使用 + 内容管理 + 部署
- [本阶段决策细则](references/decision-record-rules.md) — publish 阶段涉及的决策项
