# Astro 6.x 深度开发指南

> **来源**: [../SKILL.md](../SKILL.md) → 高级开发参考
> **用途**: 深入理解 Astro 6.x 新特性、API、调试技巧和高级配置
> **何时读取**: 需要使用 Fonts API、CSP、Rust 编译器、实验性功能或排查构建问题时

---

## Astro 6.3 新特性速查

| 特性 | 状态 | 版本 | 说明 |
|------|------|------|------|
| **内置 Fonts API** | ✅ 稳定 | 6.0 | 自动优化字体加载，支持自托管 |
| **Content Security Policy** | ✅ 稳定 | 6.0 | 内置 CSP 支持 |
| **Live Content Collections** | ✅ 稳定 | 6.0 | 外部内容源统一层 |
| **Rust 编译器** | ⚠️ 实验 | 6.0 | 替代 Go 编译器，更可靠 |
| **Queued Rendering** | ⚠️ 实验 | 6.0 | 渲染速度提升最高 2 倍 |
| **Advanced Routing** | ⚠️ 实验 | 6.3 | 完全控制请求管道 |
| **Cloudflare 原生支持** | ✅ 增强 | 6.0 | dev server 使用 workerd |

---

## 1. 内置 Fonts API（Astro 6.0+）

### 配置方法

```javascript
// astro.config.mjs
import { defineConfig, fontProviders } from 'astro/config';

export default defineConfig({
  fonts: [
    {
      name: 'Inter',
      cssVariable: '--font-inter',
      provider: fontProviders.fontsource(),  // 自托管（推荐）
    },
    {
      name: 'Roboto',
      cssVariable: '--font-roboto',
      provider: fontProviders.google(),
    },
  ],
});
```

### 在组件中使用

```astro
---
import { Font } from 'astro:components';
---

<head>
  <Font family="Inter" />
  <Font family="Roboto" />
</head>
```

### 支持的字体源

- **Google Fonts**: `fontProviders.google()`
- **Fontsource**: `fontProviders.fontsource()` （自托管，隐私友好）
- **Adobe Fonts**: `fontProviders.adobe()`
- **Bunny Fonts**: `fontProviders.bunny()` （GDPR 合规）

### 自动优化行为

✅ 开发时缓存到 `.astro/fonts/`，生产时复制到 `_astro/fonts/` 并设置 1 年 HTTP 缓存
✅ 自动生成优化的 fallback 字体栈
✅ 添加 `<link rel="preload">`
✅ 与 Tailwind CSS 4 的 `@theme` 无缝集成

---

## 2. Content Security Policy API

### 基础配置

```javascript
csp: {
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'unsafe-inline'"],
    styleSrc: ["'self'", "'unsafe-inline'", 'fonts.googleapis.com'],
    fontSrc: ["'self'", 'fonts.gstatic.com', 'data:'],
    imgSrc: ["'self'", 'data:', 'https:'],
  },
},
```

### Report-Only 模式（先监控不阻止）

```javascript
csp: {
  reportOnly: {
    directives: { /* 同上 */ },
    reportUri: 'https://your-csp-report-endpoint.com/report',
  },
},
```

---

## 3. Live Content Collections

### 配置远程数据源

```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const products = defineCollection({
  type: 'data',  // 非文档类型
  loader: async () => {
    const response = await fetch('https://api.example.com/products');
    return response.json();
  },
});

export const collections = { products };
```

### 统一查询接口

```astro
---
import { getCollection } from 'astro:content';

// 本地和远程使用相同 API
const posts = await getCollection('blog');       // 本地 Markdown
const products = await getCollection('products');  // 远程 API
---
```

---

## 4. Rust 编译器（实验性）

### 启用方法

```bash
npm install @astrojs/compiler-rs
```

```javascript
experimental: {
  compiler: {
    rust: true,
  },
},
```

### 当前状态（Astro 6.3）

⚠️ 仍为实验性功能
- ✅ 基本编译功能可用
- ✅ 错误诊断已改进
- ⚠️ 部分边缘情况可能不如 Go 版稳定
- 🎯 计划 Astro 7.0 作为默认编译器

---

## 5. Queued Rendering（实验性）

### 性能提升数据

| 场景 | 提升幅度 |
|------|---------|
| 大型站点渲染速度 | 最高 **2 倍** |
| 组件树深度 > 5 层 | 显著提升 |
| 100+ 页面构建 | 20-50% 提升 |

### 启用方法

```javascript
experimental: {
  queuedRendering: {
    enabled: true,
  },
},
```

### 适用场景

✅ 推荐：内容密集型站点、页面数量 > 50、组件嵌套层级深
❌ 不推荐：简单的营销页面（< 10 页）、高度交互的应用（SSR）

---

## 6. Advanced Routing（Astro 6.3+）

### 与 Hono 集成示例

```typescript
// src/app.ts
import { Hono } from 'hono';
import { actions, middleware, pages } from 'astro/hono';

const app = new Hono();

app.use(actions());
app.use(middleware());
app.use(pages());

export default app;
```

### 可用的 Handlers

`astro`, `trailingSlash`, `redirects`, `sessions`, `actions`, `middleware`, `pages`, `cache`, `i18n`

---

## 调试技巧

### 构建产物分析

```bash
npm install -D rollup-plugin-visualizer
```

```javascript
vite: {
  plugins: [visualizer({ open: true, gzipSize: true })],
},
```

运行 `npm run build` 后自动打开可视化报告。

### 本地模拟 GitHub Pages 环境

```bash
GH_PAGES_BASE=/repo-name npm run build
npx serve dist -l 3000
# 访问 http://localhost:3000/repo-name/
```

### 常见构建错误排查

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `JavaScript heap out of memory` | 大型项目内存不足 | `NODE_OPTIONS=--max-old-space-size=4096` |
| `Type 'string' is not assignable to type 'number'` | TS 类型错误 | 修复类型或临时关闭 strict |
| `ERESOLVE unable to resolve dependency tree` | 依赖冲突 | 删除 node_modules 和 lock 文件重新安装 |

---

## 相关资源

- [Astro 6.0 发布博客](https://astro.build/blog/astro-6/)
- [Astro 6.3 发布博客](https://astro.build/blog/astro-630/)
- [官方文档 - 实验性功能](https://docs.astro.build/en/reference/experimental-flags/)
