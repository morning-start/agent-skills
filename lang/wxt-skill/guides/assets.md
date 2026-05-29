# 静态资源管理

本文档详细说明如何在 WXT 项目中管理静态资源（图片、样式、字体等），包括资源目录、引用方式和优化策略。

## 官方导航链接

- [Assets](https://wxt.dev/guide/essentials/assets.html) - 静态资源完整指南

---

## 一、资源目录

### 1.1 public 目录

`public/` 目录是 WXT 的静态资源根目录，所有文件都会被复制到输出目录。

```
my-extension/
├── public/
│   ├── icons/              # 扩展图标
│   │   ├── icon-16.png
│   │   ├── icon-48.png
│   │   ├── icon-128.png
│   │   └── icon-512.png
│   ├── images/            # 图片资源
│   │   ├── logo.png
│   │   └── banner.jpg
│   ├── styles/            # 全局样式
│   │   └── global.css
│   ├── _locales/          # 国际化文件
│   │   ├── en/
│   │   │   └── messages.json
│   │   └── zh/
│   │       └── messages.json
│   └── manifest-overrides/ # Manifest 覆盖配置
│       └── chrome.json
```

### 1.2 入口点资源

每个入口点可以有自己的资源目录：

```
entrypoints/
├── popup/
│   ├── main.ts
│   ├── App.svelte
│   ├── App.css           # 入口点专用样式
│   └── assets/           # 入口点专用资源
│       └── logo.svg
├── options/
│   ├── main.ts
│   └── styles.css
└── content/
    ├── index.ts
    └── styles.css
```

## 二、引用方式

### 2.1 在 TypeScript 中引用

```typescript
// 导入图片
import logo from '~/public/icons/icon-128.png';

// 使用图片
browser.action.setIcon({ path: logo });

// 在 HTML 中使用
const html = `<img src="${logo}" alt="Logo" />`;
```

### 2.2 在 HTML 中引用

```html
<!-- popup.html -->
<!doctype html>
<html>
<head>
  <link rel="stylesheet" href="/styles/global.css">
</head>
<body>
  <img src="/images/logo.png" alt="Logo">
</body>
</html>
```

### 2.3 在 CSS 中引用

```css
/* App.css */
.logo {
  background-image: url('/images/logo.png');
  width: 100px;
  height: 100px;
}
```

### 2.4 在 Svelte 中引用

```svelte
<script>
  import logo from '~/public/icons/icon-128.png';
</script>

<img src={logo} alt="Logo" />
```

## 三、图标配置

### 3.1 扩展图标

扩展图标在 `public/icons/` 目录中，支持多种尺寸：

| 尺寸 | 用途 |
|------|------|
| 16x16 | 扩展管理页面小图标 |
| 48x48 | 扩展管理页面图标 |
| 128x128 | Chrome 商店图标 |
| 512x512 | Chrome 商店大图标 |

### 3.2 在 wxt.config.ts 中配置

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    icons: {
      16: '/icons/icon-16.png',
      48: '/icons/icon-48.png',
      128: '/icons/icon-128.png',
      512: '/icons/icon-512.png',
    },
    action: {
      default_icon: {
        16: '/icons/icon-16.png',
        48: '/icons/icon-48.png',
      },
    },
  },
});
```

## 四、资源优化

### 4.1 图片优化

**使用 SVG 图标（推荐）：**

SVG 图标体积小、可缩放，适合扩展图标。

```html
<!-- SVG 图标 -->
<svg width="128" height="128" viewBox="0 0 128 128">
  <!-- SVG 内容 -->
</svg>
```

**压缩图片：**

使用工具压缩图片：
- PNG: [TinyPNG](https://tinypng.com/)
- JPG: [Squoosh](https://squoosh.app/)

### 4.2 代码分割

WXT 自动进行代码分割，无需手动配置。

```typescript
// 动态导入大文件
const heavyLibrary = import('./heavy-library');
```

### 4.3 样式优化

```css
/* 使用 CSS 变量 */
:root {
  --primary-color: #3b82f6;
  --text-color: #1f2937;
}

/* 避免重复代码 */
.button {
  background-color: var(--primary-color);
  color: var(--text-color);
}
```

## 五、环境变量

### 5.1 使用环境变量

```typescript
// .env
VITE_API_URL=https://api.example.com

// main.ts
const apiUrl = import.meta.env.VITE_API_URL;
```

### 5.2 条件性引入资源

```typescript
// 仅在生产环境引入
if (import.meta.env.PROD) {
  import('./analytics');
}
```

## 六、最佳实践

### 6.1 资源组织

- **按类型分类**：images、icons、fonts、styles
- **按功能分类**：common、popup、options
- **命名规范**：使用 kebab-case

### 6.2 性能优化

- 使用 WebP 格式图片（Chrome 88+）
- 使用 CSS Sprites 合并小图标
- 使用字体子集化减少字体文件大小
- 启用 Gzip 压缩

### 6.3 安全考虑

- 验证用户上传的资源
- 限制资源大小
- 使用 CSP（Content Security Policy）
- 避免使用 eval() 和 innerHTML

## 七、常见问题

### 7.1 资源路径错误

```typescript
// ❌ 错误：相对路径
import logo from './icons/icon.png';

// ✅ 正确：使用 ~ 别名
import logo from '~/public/icons/icon.png';
```

### 7.2 资源未加载

检查 `public/` 目录结构是否正确，资源是否在正确的位置。

### 7.3 资源大小超限

Chrome 扩展限制：
- 单个文件：最大 4MB
- 总大小：最大 128MB

使用压缩和优化工具减小资源大小。
