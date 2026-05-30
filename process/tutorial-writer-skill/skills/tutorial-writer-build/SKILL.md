---
name: tutorial-writer-build
version: "1.0.0"
author: skill-factory
description: >
  Use when building Astro-based tutorial websites, creating Starlight documentation sites,
  configuring Astro projects, setting up Content Collections, developing components,
  or managing static site structure for tutorial content. Triggers on "构建网站",
  "创建 Astro 项目", "Starlight 配置", "Content Collections", "组件开发",
  "网站结构", or "Astro 构建". Covers Astro 6.x framework usage, Starlight theme integration,
  Islands Architecture, and content management specifically designed for tutorial websites.
  This is a high-frequency skill that may be called repeatedly during development iterations.
tags: [astro, starlight, build, static-site, content-collections, islands-architecture, web-development, tutorial]
dependency:
  parent: tutorial-writer
  structure: "Type 3 Sub-skill: self-contained with references"
  pattern: "Build Phase Coordinator"
meta:
  complexity: intermediate
  standalone: true
  can_invoke_directly: true
  astro_version: "6.3"
  focus: "build-phase"
  call_frequency: "high"  # 高频调用：预计每项目 10-20 次
---

# 🏗️ Tutorial Writer Build — Astro + Starlight 构建指南

> **父技能**: [tutorial-writer](../SKILL.md)
> **独立可用**: ✅ 可通过 `/build` 或 `/tutorial-writer/build` 直接触发（L1 直达）
> **架构**: L1 独立子技能 — 专注教程网站的**构建阶段**
> **基于版本**: Astro 6.3（2026年5月最新版）+ Starlight 最新版
> **使用频率**: 🔴 **高频** — 开发过程中反复迭代调用

---

## 🎯 职责范围

| ✅ 负责 | ❌ 不负责 |
|---------|----------|
| Astro 项目创建与初始化 | 部署配置 → `/publish` |
| Starlight 主题配置与定制 | GitHub Actions 工作流 → `/publish` |
| Content Collections 内容管理 | CI/CD 流水线 → `/publish` |
| 组件开发（Islands + 静态） | 域名/DNS 配置 → `/publish` |
| 项目结构与目录组织 | 生产环境监控 → `/publish` |
| 性能优化（构建时） | 发布后验证 → `/publish` |

**设计理念**: 本技能是 Tutorial Writer 流程中**调用频率最高**的子技能之一。Agent 在构建教程网站时会反复调用此技能进行配置、开发和调试。

---

## 🚀 快速启动：5 步构建教程网站

### Step 1: 项目初始化

```bash
# 使用 Starlight 模板创建（推荐）
npm create astro@latest -- --template starlight my-tutorial
cd my-tutorial

# 或交互式创建
npm create astro@latest my-tutorial
# 选择：Documentation Site → Starlight

# 启动开发服务器
npm run dev                    # http://localhost:4321
```

**输出目录结构**：

```
my-tutorial/
├── astro.config.mjs          # 核心配置文件
├── tsconfig.json             # TypeScript 配置
├── package.json              # 依赖管理
├── public/                   # 静态资源（直接复制）
│   └── favicon.svg
└── src/
    ├── content/
    │   ├── docs/             # 教程章节（Markdown）
    │   │   └── index.md      # 首页
    │   └── config.ts         # Content Collections 定义
    ├── components/           # 自定义组件
    └── styles/               # 全局样式
```

### Step 2: 核心基础配置

**astro.config.mjs**（最小可用配置）：

```javascript
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://username.github.io',     // 完整站点 URL（部署后）
  base: '/repo-name/',                     // 项目路径前缀（GitHub Pages 必填）

  integrations: [
    starlight({
      title: '教程标题',                    // 必填：浏览器标签 + SEO
      description: '教程描述',              // 推荐：SEO meta

      // 社交链接（显示在导航栏右侧）
      social: {
        github: 'https://github.com/username/repo',
      },

      // 侧边栏导航
      sidebar: [
        { label: '首页', slug: 'index' },
        { label: '入门', autogenerate: { directory: 'getting-started' }},
        { label: '进阶', items: [
          { label: '配置', slug: 'advanced/config' },
          { label: '部署', slug: 'advanced/deploy' },
        ]},
      ],

      // 页面功能开关
      editLink: {
        baseUrl: 'https://github.com/username/repo/edit/main/',
      },
      lastUpdated: true,                   // 显示最后更新时间
      pagination: true,                    // 上一页/下一页导航

      // 搜索配置（默认 Pagefind，零外部依赖）
      search: { mode: 'auto' },

      // 插件列表（按需添加）
      plugins: [],
    }),
  ],
});
```

### Step 3: Content Collections 配置

**src/content/config.ts**（定义教程内容的元数据 schema）：

```typescript
import { defineCollection, z } from 'astro:content';
import { docsLoader, docsSchema } from '@astrojs/starlight/loaders';

const docs = defineCollection({
  loader: docsLoader(),
  schema: docsSchema({
    // Starlight 自动处理：title / description / slug / draft / sidebar
    schema: z.object({
      // 扩展自定义字段（按需添加）
      tags: z.array(z.string()).optional(),           // 标签分类
      difficulty: z.enum(['beginner', 'intermediate', 'advanced']).optional(),  // 难度等级
      readingTime: z.number().optional(),              // 预估阅读时间（分钟）
      coverImage: z.string().optional(),               // 封面图片
    }),
  }),
});

export const collections = { docs };
```

**章节 Frontmatter 示例**（`src/content/docs/getting-started/setup.md`）：

```yaml
---
title: 环境准备
description: 安装所需的工具和依赖，配置开发环境
slug: getting-started/setup
tags: [入门, 环境]
difficulty: beginner
readingTime: 10
draft: false
sidebar:
  label: 环境准备
  order: 1
---

# 环境准备

本章节将指导你完成...
```

### Step 4: 目录结构组织

#### 小型教程（≤10 章）

```
src/content/docs/
├── index.md              # 教程首页/概览
├── 01-概述.md
├── 02-入门.md
└── 03-进阶.md
```

#### 中型教程（10-30 章）— **推荐**

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
│   └── 02-最佳实践.md
└── appendix/
    ├── faq.md
    └── changelog.md
```

**对应的侧边栏配置**：

```javascript
sidebar: [
  { label: '教程简介', slug: 'index' },
  { label: '基础篇', autogenerate: { directory: '01-基础篇' }},
  { label: '进阶篇', autogenerate: { directory: '02-进阶篇' }},
  { label: '附录', autogenerate: { directory: 'appendix' }},
],
```

#### 大型教程（30+ 章）— 多层分组

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

### Step 5: 开发与验证

```bash
# 启动开发服务器（热重载）
npm run dev                      # http://localhost:4321

# 构建生产版本（检查错误）
npm run build                    # 输出到 dist/

# 本地预览构建结果
npm run preview                  # http://localhost:4321

# 添加常用插件（推荐）
npm install starlight-links-validator  # 构建时链接验证
```

---

## 🏗️ 核心概念详解

### Islands Architecture（岛屿架构）

Astro 的核心优势：**默认零 JavaScript**，仅在需要交互的地方加载。

```astro
---
// src/pages/index.astro
// 示例：教程首页
import Header from '../components/Header.astro';
import Hero from '../components/Hero.astro';
import FeatureList from '../components/FeatureList.astro';
import InteractiveDemo from '../components/InteractiveDemo.jsx';  // React 组件
import Footer from '../components/Footer.astro';
---

<html>
  <head><title>教程标题</title></head>
  <body>
    <!-- 静态组件：零 JS 输出 -->
    <Header />
    <Hero />
    <FeatureList />

    <!-- 交互组件：仅此组件发送 JS -->
    <InteractiveDemo client:visible />  {/* 用户滚动到才加载 */}

    <Footer />
  </body>
</html>
```

**客户端指令选择指南**：

| 指令 | 加载时机 | 适用场景 | 教程场景示例 |
|------|---------|---------|------------|
| `client:load` | 页面立即 | 关键交互 | 导航搜索框、折叠目录 |
| `client:idle` | 页面空闲后 | 非关键小部件 | 代码复制按钮、反馈表单 |
| `client:visible` | 元素可见时 | 懒加载内容 | 代码沙盒演示、图片画廊 |
| `client:media`(查询) | 媒体匹配时 | 响应式组件 | 移动端特定 UI |

**性能原则**：
- ✅ 90% 的页面内容应为静态组件（`.astro` 文件）
- ⚠️ 仅在必要时使用 Islands 组件（React/Vue/Svelte）
- 🎯 教程站点的交互应聚焦于**学习体验增强**（代码演示、交互式图表）

### Content Collections（内容集合）

类型安全的 Markdown/MDX 内容管理系统。

**查询内容**：

```astro
---
// src/pages/index.ts (或 .astro)
import { getCollection } from 'astro:content';

// 获取所有已发布的教程章节
const allDocs = await getCollection('docs');

// 过滤：排除草稿
const publishedDocs = allDocs.filter(doc => !doc.data.draft);

// 排序：按侧边栏 order 字段
const sortedDocs = publishedDocs.sort((a, b) => {
  const orderA = a.data.sidebar?.order ?? 999;
  const orderB = b.data.sidebar?.order ?? 999;
  return orderA - orderB;
});

// 按标签分组
const tagsGrouped = Object.entries(
  publishedDocs.reduce((acc, doc) => {
    const tags = doc.data.tags || [];
    tags.forEach(tag => {
      if (!acc[tag]) acc[tag] = [];
      acc[tag].push(doc);
    });
    return acc;
  }, {})
);
---

<h2>所有章节 ({publishedDocs.length})</h2>
{sortedDocs.map(doc => (
  <article>
    <h3><a href={doc.slug}>{doc.data.title}</a></h3>
    <p>{doc.data.description}</p>
    {doc.data.tags?.map(tag => (
      <span class="tag">{tag}</span>
    ))}
  </article>
))}
```

### 组件开发

#### 静态组件（`.astro`）— **优先使用**

```astro
---
// src/components/Card.astro
interface Props {
  title: string;
  description: string;
  icon?: string;
  href?: string;
  difficulty?: 'beginner' | 'intermediate' | 'advanced';
}

const { title, description, icon, href, difficulty } = Astro.props;
---

<div class:list={['card', { [`card--${difficulty}`]: difficulty }]}>
  {icon && <span class="card__icon">{icon}</span>}
  <h3 class="card__title">
    {href ? <a href={href}>{title}</a> : title}
  </h3>
  <p class="card__description">{description}</p>
  <slot name="footer" />
</div>

<style>
  .card {
    border: 1px solid var(--starlight-color-border);
    border-radius: 8px;
    padding: 1.25rem;
    transition: box-shadow 0.2s ease;
  }
  .card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  .card--beginner { border-left: 4px solid green; }
  .card--intermediate { border-left: 4px solid orange; }
  .card--advanced { border-left: 4px solid red; }
  .card__title { margin: 0.5rem 0; font-size: 1.125rem; }
  .card__description { color: var(--starlight-color-text); margin: 0; }
</style>
```

**使用方式**：

```astro
---
import Card from '../components/Card.astro';
---

<Card
  title="环境准备"
  description="安装 Node.js 和包管理器"
  difficulty="beginner"
  href="/getting-started/setup"
/>
```

#### Islands 交互组件（React/Vue/Svelte）

**React 示例**（代码运行沙盒）：

```tsx
// src/components/react/CodeSandbox.tsx
import { useState } from 'react';

interface Props {
  code: string;
  language?: string;
}

export default function CodeSandbox({ code, language = 'javascript' }: Props) {
  const [output, setOutput] = useState('');
  const [isRunning, setIsRunning] = useState(false);

  const handleRun = async () => {
    setIsRunning(true);
    try {
      // 模拟代码执行（实际项目中可接入安全执行环境）
      const result = eval(code);  // 注意：生产环境需使用安全的沙盒
      setOutput(String(result));
    } catch (error) {
      setOutput(`Error: ${error.message}`);
    }
    setIsRunning(false);
  };

  return (
    <div className="sandbox">
      <pre><code className={`language-${language}`}>{code}</code></pre>
      <button onClick={handleRun} disabled={isRunning}>
        {isRunning ? '运行中...' : ▶ 运行代码'}
      </button>
      {output && <div className="output">{output}</div>}
    </div>
  );
}
```

**在页面中使用**：

```astro
---
import CodeSandbox from '../components/react/CodeSandbox.tsx';
---

<CodeSandbox client:visible
  code={`console.log('Hello, Tutorial!');`}
  language="javascript"
/>
```

---

## ⚙️ 高级配置

### Starlight 插件集成

**安装插件流程**：

```bash
# 1. 安装插件包
npm install starlight-links-validator

# 2. 在 astro.config.mjs 的 starlight.plugins 中注册
starlight({
  plugins: [
    starlightLinksValidator({  // 构建时验证所有内部链接
      errorOnInternalLink: true,
    }),
  ],
})
```

**推荐插件组合**（教程场景）：

| 类别 | 插件 | 用途 |
|------|------|------|
| **质量保障** | `starlight-links-validator` | 防止死链和失效锚点 |
| **内容管理** | `starlight-blog` | 更新日志 / 发布公告 |
| **展示增强** | `starlight-image-zoom` | 截图 / 架构图放大查看 |
| **状态标注** | `starlight-heading-badges` | 标注"新"、"已更新"、"实验性" |
| **模块化** | `starlight-sidebar-topics` | 多分区独立侧边栏 |

### 性能优化配置

**astro.config.mjs**：

```javascript
export default defineConfig({
  // 构建优化
  build: {
    inlineStylesheets: 'auto',       // 内联小 CSS（减少请求）
    compressHTML: true,              // 压缩 HTML
  },

  // 图片优化（Astro 内置）
  image: {
    domains: [],                     // 允许的远程图片域名
  },

  // Vite 优化
  vite: {
    cssMinify: true,                // CSS 压缩
    build: {
      minify: 'esbuild',            // JS 压缩器（比 terser 快）
    },
  },

  // 实验性功能（Astro 6.0+）
  experimental: {
    // queuedRendering: { enabled: true },  // 渲染速度提升最高 2x（实验性）
    // compiler: { rust: true },            // Rust 编译器（实验性）
  },
});
```

**字体优化**（Astro 6.0+ Fonts API）：

```javascript
import { defineConfig, fontProviders } from 'astro/config';

export default defineConfig({
  fonts: [
    {
      name: 'Inter',
      cssVariable: '--font-inter',
      provider: fontProviders.fontsource(),  // 自托管（最快、最隐私）
    },
  ],
});

// 在布局中使用
---
import { Font } from 'astro:components';
---

<head>
  <Font family="Inter" />
</head>
```

### i18n 多语言配置

**astro.config.mjs**：

```javascript
starlight({
  locales: {
    root: {
      label: '简体中文',
      lang: 'zh-CN',
    },
    en: {
      label: 'English',
      lang: 'en',
    },
  },
  defaultLocale: 'root',
}),
```

**目录结构**：

```
src/content/docs/
├── index.md                # 中文默认首页
├── guide/
│   └── introduction.md
└── en/
    ├── index.md            # 英文首页
    └── guide/
        └── introduction.md
```

---

## 📂 项目最佳实践

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 内容文件 | 数字前缀 + kebab-case | `01-环境准备.md` |
| 组件文件 | PascalCase | `CodeSandbox.tsx`, `Card.astro` |
| 样式文件 | kebab-case | `custom.css` |
| 目录名 | kebab-case | `01-基础篇/` |

### 图片处理策略

| 存放位置 | 引用方式 | 处理方式 | 适用场景 |
|---------|---------|---------|---------|
| `src/assets/images/` | 相对路径 | Astro 优化（WebP/哈希） | 教程内嵌截图 |
| `public/images/` | 绝对路径 | 直接复制 | OG 图片、favicon |
| 外部 CDN | 完整 URL | 无处理 | 已托管资源 |

**推荐**：教程内嵌图片统一放 `src/assets/images/`，由 Astro 自动优化格式和尺寸。

### 社区经验总结

✅ **项目启动建议**：
- 从 `--template starlight` 开始（比从零配置快 3 倍）
- 先规划 `sidebar` 导航结构（决定读者浏览路径）
- 小步验证：每写 2-3 章就 `npm run build`，避免积累错误

⚠️ **常见陷阱**：
- `base` 配置错误导致静态资源 404（GitHub Pages 必须设置）
- Frontmatter 字段类型不匹配（Zod 严格校验）
- 交互组件全局加载（应在具体页面按需引入）
- 侧边栏重复项（`autogenerate` 的目录不能同时出现在手动项中）

🎯 **性能原则**：
- 保持 Astro 默认零 JS 优势（不向全局 layout 添加 JS）
- 交互组件使用 `client:visible` 懒加载策略
- 图片优先 WebP 格式，配合 `astro:assets` 自动优化
- 利用 Starlight 内置 CSS 变量，减少自定义 CSS 覆盖

---

## 🔗 与发布阶段的衔接

构建完成后，进入 **发布阶段** → 调用 `/publish`

**构建阶段交付物**：

| 交付物 | 说明 | 验证方式 |
|--------|------|---------|
| ✅ `dist/` 目录 | 构建产物（HTML/CSS/JS） | `npm run build` 成功 |
| ✅ 无构建错误 | 终端返回 exit 0 | CI 自动检查 |
| ✅ 无内部死链 | 所有页面可互相访问 | `starlight-links-validator` |
| ✅ 响应式布局 | 375px / 768px / 1280px 可用 | 浏览器 DevTools |
| ✅ Lighthouse 评分 | Perf ≥ 90, A11y ≥ 90 | Chrome DevTools |

**触发发布的条件**：

```bash
# 本地验证通过后
npm run build           # ✅ 成功
npm run preview         # ✅ 预览正常

# 准备就绪，调用发布技能
→ /publish               # 进入 GitHub Pages 部署流程
```

---

## 📂 本子技能结构

```
skills/tutorial-writer-build/
├── SKILL.md                              ← 本文件（~400行）
└── references/
    └── astro-development.md              ← Astro 6.x 深度开发指南
```

---

## 📚 参考文档索引

| 文档 | 内容 | 何时读取 |
|------|------|---------|
| [astro-development.md](references/astro-development.md) | Astro 6.x 新特性、API 参考、调试技巧 | 需要高级功能或排查问题时 |

> 💡 **加载时机**: 仅在需要深度技术细节时读取，常规构建流程本文件已覆盖

---

## 🔗 相关资源

| 资源 | 路径/链接 | 用途 |
|------|----------|------|
| 父技能 | [../SKILL.md](../SKILL.md) | Tutorial Writer 主路由器 |
| 发布子技能 | [../skills/tutorial-writer-publish/SKILL.md](../skills/tutorial-writer-publish/SKILL.md) | GitHub Pages 发布流程 |
| Astro 官方文档 | https://docs.astro.build/ | 框架权威指南 |
| Starlight 文档 | https://starlight.astro.build/ | 主题完整参考 |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **1.0.0** | 2026-05-30 | **初始版本**: 从 publish/skills/website-build 提升为 L1 独立子技能；专注 Astro 6.3 + Starlight；5 步快速启动流程；Islands Architecture 详解；Content Collections 完整指南；组件开发示例（静态 + Islands）；高级配置（插件/性能/i18n）；项目最佳实践和命名规范；与发布阶段的衔接说明；标记为高频调用子技能 |
