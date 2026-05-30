# 网页发布指南 — Web Publishing (Astro + Starlight)

> **版本**: v5.0.0 — 模块化配置 + 插件生态 + 社区最佳实践
>
> **定位**: 🏗️ **构建阶段详细参考** — 本文档专注于 Astro + Starlight 的项目构建、配置、内容管理和插件生态。
>
> **所属阶段**: 主要服务于 `/website-build` 子技能（构建阶段）
>
> **发布阶段参考**: GitHub Pages 部署、CI/CD、Actions 工作流等详见 → [website-deploy 子技能](../skills/website-deploy/SKILL.md)
>
> **使用场景**: 当需要深入了解 Starlight 配置细节、插件用法、内容组织、组件开发等构建相关主题时读取本文档。

---

## 文档导航

| 章节 | 内容 | 所属子技能 |
|------|------|-----------|
| **§1-5** | 技术栈、模块化配置、内容管理、插件、项目初始化 | `/website-build` ✅ |
| **§6** | 部署基础配置（精简版） | `/website-deploy` (完整版) → [查看](../skills/website-deploy/SKILL.md) |
| **§7-8** | 社区经验、质量门禁 | `/website-build` + `/website-deploy` |

---

| 层 | 技术 | 作用 |
|----|------|------|
| 框架 | Astro 6.x | 静态站点生成，默认零 JS 输出 |
| 主题 | Starlight | 文档主题（搜索/导航/暗色模式/代码高亮/i18n） |
| 包管理 | npm / pnpm / yarn | 依赖管理 |
| 内容 | Markdown + Content Collections | 类型安全的内容管理 |
| 校验 | Zod (内置) | Frontmatter schema 校验 |
| 搜索 | Pagefind (内置) | 构建时全文搜索，零外部依赖 |
| 代码高亮 | Expressive Code (内置) | 语法高亮 + 行号 + 复制 + 差异对比 |
| 交互 | Islands 架构 (React/Vue/Svelte) | 按需加载交互组件 |
| 部署 | GitHub Actions + `withastro/action` | 自动化构建部署到 Pages |
| 链接验证 | `starlight-links-validator` | 构建时内部链接检查 |

## 2. 模块化配置参考

### 2.1 Astro + Starlight 配置全貌

```js
// astro.config.mjs — 完整配置结构
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://用户名.github.io',    // 部署后完整 URL
  base: '/仓库名',                      // 项目站点必填，用户站点省略

  integrations: [
    starlight({
      // ── 基础信息 ──
      title: '教程标题',                // 必填
      description: '教程描述',          // 推荐，SEO
      logo: { src: './src/assets/logo.svg' },
      favicon: '/favicon.svg',

      // ── 社交链接（显示在导航栏右侧）──
      social: {
        github: 'https://github.com/用户名/仓库名',
      },

      // ── 导航 ──
      sidebar: [
        { label: '首页', slug: 'index' },
        { label: '入门', autogenerate: { directory: 'getting-started' }},
        { label: '进阶', items: [
          { label: '配置', slug: 'advanced/config' },
          { label: '部署', slug: 'advanced/deploy' },
        ]},
      ],

      // ── 页面功能 ──
      editLink: { baseUrl: 'https://github.com/用户名/仓库名/edit/main/' },
      lastUpdated: true,
      pagination: true,

      // ── 目录 ──
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },

      // ── 搜索 ──
      search: { mode: 'auto' },         // 默认 Pagefind

      // ── 插件 ──
      plugins: [],

      // ── 自定义 <head> ──
      head: [
        { tag: 'meta', attrs: { property: 'og:image', content: '/og-default.png' }},
      ],
    }),
  ],
});
```

### 2.2 Content Collections (src/content.config.ts)

```ts
import { defineCollection } from 'astro:content';
import { docsLoader, docsSchema } from '@astrojs/starlight/loaders';
import { z } from 'astro/zod';

const docs = defineCollection({
  loader: docsLoader(),
  schema: docsSchema({
    schema: z.object({
      // Starlight 默认: title / description / slug / draft / sidebar
      // 额外自定义字段:
      tags: z.array(z.string()).optional(),
      difficulty: z.enum(['beginner', 'intermediate', 'advanced']).optional(),
      readingTime: z.number().optional(),
    }),
  }),
});

export const collections = { docs };
```

### 2.3 章节 Frontmatter 完整示例

```yaml
---
title: 环境准备
description: 本教程所需的工具安装和环境配置
slug: getting-started/setup
tags: [入门, 环境]
difficulty: beginner
readingTime: 10
draft: false
sidebar:
  label: 环境准备
  order: 1
---
```

### 2.4 Starlight 配置项速查

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `title` | string \| object | — | 站点标题（支持多语言 object） |
| `description` | string | — | 默认页面描述（SEO） |
| `logo` | object | — | `{ src }` 或 `{ light, dark }` + `alt` + `replacesTitle` |
| `favicon` | string | — | favicon 路径（相对于 public/） |
| `social` | object | — | 社交链接: github / twitter / mastodon / discord / youtube / bluesky |
| `sidebar` | array | — | 见下方侧边栏配置 |
| `tableOfContents` | object \| false | h2-h3 | 可设 min/maxHeadingLevel |
| `editLink` | object | — | `{ baseUrl }` 链接到源码 |
| `lastUpdated` | boolean | false | 显示最后更新时间（需 git） |
| `pagination` | boolean | true | 上一页/下一页 |
| `search` | object | — | `{ mode: 'auto' }`，可替换 DocSearch |
| `plugins` | array | [] | Starlight 插件 |
| `components` | object | — | 覆盖内置组件 |
| `head` | array | [] | 自定义 `<head>` 标签 |
| `locales` | object | — | 多语言配置 root / en / zh 等 |
| `defaultLocale` | string | — | 默认语言 locale 键 |
| `credits` | boolean | true | 是否显示 "Built with Starlight" |

## 3. 内容管理

### 3.1 Starlight 内置内容组件

Starlight 提供了开箱即用的内容组件，无需额外配置：

| 组件 | 功能 | Markdown 写法 |
|------|------|-------------- |
| 代码高亮 | 语法高亮 + 行号 + 复制按钮 | ` ```python ` |
| 代码分组 | Tab 切换多语言代码 | ` ```js ` / ` ```py ` 用 ` ``` ` 分隔 |
| 代码差异对比 | 展示代码变更 | ` ```diff ` |
| 提示框 | info / tip / caution / danger | `!!! tip "标题"` |
| 可折叠详情 | 折叠内容 | `??? note "标题"` |
| 表格 | 标准 Markdown 表格 | `\| 列1 \| 列2 \|` |
| 图片 | 响应式图片 | `![alt](path)` |
| TOC | 自动生成 | 默认开启 |
| 搜索 | 全文搜索 | 默认 Pagefind |
| 分页导航 | 上一页/下一页 | 默认开启 |
| 编辑链接 | 链接到源码 | 配置 editLink 后显示 |

### 3.2 内容组织结构

**小型教程（≤10 章）**: 扁平文件
```
src/content/docs/
├── index.md
├── 01-概述.md
├── 02-入门.md
└── ...
```

**中型教程（10-30 章）**: 按模块分组
```
src/content/docs/
├── index.md
├── 01-基础篇/
│   ├── index.md
│   ├── 01-安装.md
│   └── 02-配置.md
├── 02-进阶篇/
└── ...
```

**大型教程（30+ 章）**: 多层分组 + 自动生成侧边栏
```
src/content/docs/
├── index.md
├── quick-start/
│   ├── index.md
│   └── first-app.md
├── guides/
│   ├── installation.md
│   ├── configuration.md
│   └── deployment.md
├── tutorials/
│   ├── beginner/
│   ├── intermediate/
│   └── advanced/
└── reference/
    ├── api.md
    └── faq.md
```

### 3.3 图片处理

| 方式 | 路径 | 处理 | 适用 |
|------|------|------|------|
| `src/assets/images/` | 相对路径引用 | Astro 处理（优化/哈希） | 教程内嵌图片 |
| `public/images/` | 绝对路径引用 | 直接复制不处理 | OG 图片、全局资源 |
| 外部 CDN | 完整 URL | 无处理 | 已托管图片 |

> 推荐: 教程内嵌图片放 `src/assets/images/`，由 Astro 自动优化。

## 4. 插件使用指南

### 4.1 插件安装通用流程

```bash
# 1. 安装插件包
npm install starlight-links-validator

# 2. astro.config.mjs 的 starlight.plugins 中添加
starlight({
  plugins: [
    // 无需配置
    starlightLinksValidator(),

    // 或带配置
    starlightBlog({
      title: '更新日志',
      description: '教程更新记录',
    }),
  ],
})
```

### 4.2 常用插件配置示例

**starlight-links-validator** — 构建时验证所有内部链接：
```js
starlightLinksValidator({
  errorOnInternalLink: true,       // 死链报错（默认 warn）
  errorOnLocalLinks: true,         // 锚点失效报错
})
```

**starlight-blog** — 添加博客/更新日志：
```js
starlightBlog({
  title: '更新日志',
  description: '教程更新与发布记录',
  authors: {
    authorId: {
      name: '作者名',
      url: 'https://github.com/xxx',
    },
  },
})
```

**starlight-obsidian** — 从 Obsidian 直接发布：
```js
starlightObsidian({
  vaultDir: './obsidian-vault',
})
```

**starlight-versions** — 多版本切换：
```js
starlightVersions({
  versions: [
    { slug: 'v2', label: 'v2.0' },
    { slug: 'v1', label: 'v1.0 (旧版)' },
  ],
})
```

**starlight-sidebar-topics** — 多分区独立侧边栏：
```js
starlightSidebarTopics([
  { label: '教程', link: '/tutorial/', items: 'tutorial' },
  { label: 'API 参考', link: '/api/', items: 'api' },
])
```

### 4.3 插件选择速查

```
必需（推荐所有教程使用）
  └── starlight-links-validator     # 链接质量保障

内容管理
  ├── starlight-blog                 # 更新日志
  ├── starlight-versions             # 版本文档
  ├── starlight-sidebar-topics       # 分区侧边栏
  └── starlight-obsidian             # Obsidian 集成

展示增强
  ├── starlight-image-zoom           # 图片放大
  ├── starlight-heading-badges       # 标题徽章
  ├── starlight-site-graph           # 站点图谱
  ├── starlight-view-modes           # 视图模式
  └── starlight-showcases            # 作品展示

质量保障
  ├── starlight-spell-checker        # 拼写检查
  └── starlight-links-validator      # 链接验证

用户体验
  ├── starlight-utils                # 工具集
  ├── star-warp                      # 搜索增强
  └── starlight-sidebar-swipe        # 移动端滑动

官方扩展
  ├── @astrojs/starlight-docsearch   # Algolia 搜索
  ├── @astrojs/starlight-tailwind    # Tailwind CSS
  └── @astrojs/starlight-markdoc     # Markdoc 格式
```

### 4.4 交互组件框架选择

选择 Islands 框架时考虑以下因素：

| 因素 | React | Vue | Svelte | Solid | Preact |
|------|-------|-----|--------|-------|--------|
| 社区生态 | ★★★★★ | ★★★★ | ★★★ | ★★ | ★★★ |
| 包体积 | ~130KB | ~100KB | ~30KB | ~20KB | ~10KB |
| 学习成本 | 中 | 低 | 低 | 中 | 低 |
| Astro 集成 | 官方 | 官方 | 官方 | 官方 | 官方 |
| 教程适用 | 最通用 | Vue 栈适用 | 轻量交互 | 高性能 | React 替代 |

> 交互组件的具体实现 → 调用对应 UI 框架子技能。

## 5. 项目初始化

### 5.1 创建项目

```bash
# 创建
npm create astro@latest -- --template starlight my-tutorial
cd my-tutorial

# 启动开发
npm run dev                    # http://localhost:4321

# 添加额外依赖
npm install starlight-links-validator    # 链接验证（推荐）

# 构建
npm run build                  # 输出到 dist/
```

### 5.2 目录初始化

```bash
# 创建内容目录结构
mkdir -p src/content/docs/01-基础篇
mkdir -p src/content/docs/02-进阶篇
mkdir -p src/content/docs/appendix
mkdir -p src/assets/images
mkdir -p src/components/react
mkdir -p src/components/overrides
mkdir -p .github/workflows

# 创建首页
cat > src/content/docs/index.md << 'EOF'
---
title: 教程首页
description: 教程概述
---

# 教程标题

> 教程简介...
EOF
```

## 6. 部署

### 6.1 GitHub Actions 配置

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: withastro/action@v3
```

### 6.2 GitHub Pages 设置

```
仓库 Settings → Pages → Source: GitHub Actions
```

### 6.3 部署前提

- `astro.config.mjs` 中 `site` 必须为完整 URL（如 `https://user.github.io/repo/`）
- 项目站点（非用户站点）必须设置 `base: '/仓库名/'`
- GitHub Actions 有 `pages: write` 和 `id-token: write` 权限

## 7. 社区经验总结

### 7.1 项目启动建议

- **从模板开始**：`--template starlight` 已配置好默认内容，改配置比从零开始快 3 倍
- **先配导航**：`sidebar` 决定读者浏览路径，应在写内容前规划好
- **小步验证**：每添加 1-2 章就 `npm run build`，避免积累大量错误
- **尽早部署**：第一天就配置好 CI/CD，每次 push 自动验证构建

### 7.2 内容管理经验

- **Frontmatter 是元数据合同**：Zod schema 定义后所有页面必须遵守，避免遗漏字段
- **description 必填**：每页 description 用于搜索摘要和 SEO，不可省略
- **侧边栏与文件名解耦**：使用 `autogenerate` 按文件系统组织，`sidebar` 中 `label` 自定义显示名
- **草稿机制利用**：未完成的章节设置 `draft: true`，构建时自动跳过

### 7.3 性能经验

- Astro 默认零 JS，保持此优势：不向全局 layout 添加 JS 引用
- 交互组件使用 client:visible 加载策略，仅在进入视口时加载
- 图片优先使用 WebP 格式，配合 `astro:assets` 自动优化
- 避免过多自定义 CSS 覆盖，尽量利用 Starlight 内置的 CSS 变量

### 7.4 常见陷阱

- `base` 配置错误导致 404：项目站点（`user.github.io/repo`）必须设置 `base: '/repo/'`
- 图片路径错误：`src/assets/` 中的图片用相对路径，`public/` 中图片用绝对路径
- 交互组件全局加载：不要在 `src/components/` 中创建会被自动全局引入的组件
- Frontmatter 字段类型不匹配：Zod schema 严格要求类型，日期用 `z.coerce.date()`
- 侧边栏重复：`autogenerate` 的目录不能包含在其他手动项中

### 7.5 社区资源

| 资源 | 链接 |
|------|------|
| Astro 官方文档 | https://docs.astro.build/ |
| Starlight 官方文档 | https://starlight.astro.build/ |
| Starlight 配置参考 | https://starlight.astro.build/reference/configuration/ |
| Starlight 插件列表 | https://starlight.astro.build/resources/plugins/ |
| 社区内容列表 | https://starlight.astro.build/resources/community-content/ |
| Astro Discord | https://astro.build/chat |
| Awesome Starlight | https://github.com/trueberryless-org/awesome-starlight |
| Astro GitHub Pages 部署 | https://docs.astro.build/en/guides/deploy/github/ |
| withastro/action | https://github.com/withastro/action |
| 案例: Cloudflare 文档 | https://blog.cloudflare.com/open-source-all-the-way-down/ |
| 案例: WP Engine | https://astro.build/case-studies/wp-engine/ |

## 8. 质量门禁

| # | 检查项 | 标准 | 验证方式 |
|---|--------|------|---------|
| W1 | 构建无错误 | `npm run build` 返回 0 | CI |
| W2 | 内部链接有效 | `starlight-links-validator` 无 error | CI |
| W3 | 资源可访问 | 图片/CSS/JS 路径不 404 | CI + 人工 |
| W4 | 导航结构完整 | 所有章节在侧边栏可达 | 人工巡查 |
| W5 | 搜索可用 | Pagefind 索引正常生成 | `npm run build` 后检查 |
| W6 | 响应式布局 | 375px / 768px / 1280px 可用 | DevTools |
| W7 | 暗色模式 | 对比度达标 | 手动切换 |
| W8 | Lighthouse 评分 | Perf ≥ 90, A11y ≥ 90 | Chrome DevTools |
| W9 | SEO | 每页有 title + description | 构建后检查 HTML |
| W10 | 无障碍 | 键盘可导航全部内容 | Tab 键走查 |
| W11 | 无敏感信息 | 无密钥/密码泄露 | 代码审查 |
| W12 | 构建产物大小 | dist/ 大小合理（检查 JS chunk） | 构建后检查 |
