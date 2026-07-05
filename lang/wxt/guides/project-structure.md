# 项目结构详解

本文档详细说明 WXT 的项目结构，包括默认结构、源码模式和核心文件作用。

## 官方导航链接

- [Project Structure](https://wxt.dev/guide/essentials/project-structure.html) - 项目目录结构规范
- [Configuration](https://wxt.dev/guide/essentials/config/) - 配置相关子分类
  - [Manifest](https://wxt.dev/guide/essentials/config/manifest.html) - Manifest 配置详解
  - [Environment Variables](https://wxt.dev/guide/essentials/config/environment-variables.html) - 环境变量配置
  - [TypeScript](https://wxt.dev/guide/essentials/config/typescript.html) - TypeScript 类型配置
  - [Auto-imports](https://wxt.dev/guide/essentials/config/auto-imports.html) - 自动导入配置

---

## 一、标准项目结构

### 1.1 默认结构

使用 `bunx wxt@latest init` 创建项目后，默认结构如下：

```
my-extension/
├── .output/              # 构建输出目录（自动生成）
├── entrypoints/          # 入口点目录（核心）
│   ├── background.ts     # 后台脚本
│   ├── content.ts        # 内容脚本
│   ├── popup.html        # 弹出页面
│   └── options.html      # 选项页面（可选）
├── public/               # 公共资源目录
│   ├── _locales/         # 国际化文件
│   ├── images/           # 图片资源
│   └── manifest-overrides/  # Manifest 覆盖配置
├── wxt.config.ts         # WXT 配置文件
├── package.json          # 项目配置
└── tsconfig.json         # TypeScript 配置
```

**参考文档：**
- 项目结构：https://wxt.dev/guide/essentials/project-structure.html

### 1.2 源码模式结构

对于大型项目，建议使用源码模式结构：

```
src/
├── entrypoints/                 # 入口点
│   ├── background.ts
│   ├── content/
│   │   ├── index.ts
│   │   └── styles.css
│   ├── popup/
│   │   ├── main.ts
│   │   ├── App.svelte
│   │   └── App.css
│   └── options/
│       ├── main.ts
│       └── App.svelte
├── components/                 # 共享组件
│   ├── ui/
│   │   ├── Button.svelte
│   │   ├── Input.svelte
│   │   └── Card.svelte
│   └── features/
│       └── counter/
├── composables/                # 组合式函数
│   ├── useStorage.ts
│   └── useTheme.ts
├── lib/                        # 工具库
│   ├── api/
│   ├── utils/
│   ├── types/
│   └── constants/
├── stores/                     # 状态管理
├── styles/                     # 全局样式
├── assets/                     # 静态资源
└── utils/                      # 工具函数
```

## 二、目录说明

### 2.1 .output/（构建输出目录）

构建后生成的输出目录，包含编译后的文件。

```
.output/
├── chrome/                  # Chrome 输出
│   ├── manifest.json
│   ├── background.js
│   ├── popup.html
│   ├── chunks/
│   └── assets/
├── firefox/                 # Firefox 输出
│   ├── manifest.json
│   └── ...
└── edge/                    # Edge 输出
    ├── manifest.json
    └── ...
```

**注意：** 此目录在构建时自动生成，不应手动修改。

### 2.2 entrypoints/（入口点目录）

**核心目录**，包含所有入口点文件。

#### Background Script

```typescript
// entrypoints/background.ts
import { defineBackground } from 'wxt/sandbox';

export default defineBackground(() => {
  console.log('Background script started');
});
```

#### Content Script

```typescript
// entrypoints/content.ts
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],
  main() {
    console.log('Content script injected');
  },
});
```

#### Popup

```html
<!-- entrypoints/popup.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Popup</title>
</head>
<body>
  <script type="module" src="./popup.ts"></script>
</body>
</html>
```

```typescript
// entrypoints/popup.ts
console.log('Popup loaded');
```

#### Options

```html
<!-- entrypoints/options.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Options</title>
</head>
<body>
  <h1>Options</h1>
  <script type="module" src="./options.ts"></script>
</body>
</html>
```

```typescript
// entrypoints/options.ts
console.log('Options loaded');
```

### 2.3 public/（公共资源目录）

包含直接复制到构建输出的文件。

#### 国际化文件

```
public/_locales/
├── en/
│   └── messages.json
├── zh_CN/
│   └── messages.json
└── ja/
    └── messages.json
```

**messages.json：**

```json
{
  "extensionName": {
    "message": "My Extension",
    "description": "The name of the extension"
  },
  "extensionDescription": {
    "message": "A browser extension built with WXT",
    "description": "The description of the extension"
  }
}
```

#### 图片资源

```
public/images/
├── icon-16.png
├── icon-32.png
├── icon-48.png
└── icon-128.png
```

#### Manifest 覆盖配置

```
public/manifest-overrides/
├── chrome.json
├── firefox.json
├── edge.json
└── safari.json
```

**chrome.json：**

```json
{
  "name": "My Extension (Chrome)",
  "permissions": ["alarms", "idle"]
}
```

**firefox.json：**

```json
{
  "name": "My Extension (Firefox)",
  "browser_specific_settings": {
    "gecko": {
      "id": "my-extension@example.com"
    }
  }
}
```

### 2.4 wxt.config.ts（配置文件）

WXT 的核心配置文件。

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: 'My Extension',
    version: '1.0.0',
  },
});
```

### 2.5 package.json（项目配置）

项目依赖和脚本配置。

```json
{
  "name": "my-extension",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "wxt",
    "dev:firefox": "wxt -b firefox",
    "build": "wxt build",
    "build:firefox": "wxt build -b firefox",
    "zip": "wxt zip",
    "zip:firefox": "wxt zip -b firefox",
    "postinstall": "wxt prepare"
  },
  "devDependencies": {
    "wxt": "^0.17.0",
    "typescript": "^5.3.0"
  }
}
```

### 2.6 tsconfig.json（TypeScript 配置）

TypeScript 编译配置。

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "lib": ["ESNext", "DOM", "DOM.Iterable"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "types": ["wxt/client-types"]
  },
  "include": ["**/*.ts", "**/*.tsx", "**/*.svelte", "wxt.config.ts"]
}
```

## 三、路径别名

### 3.1 使用 ~ 别名

WXT 支持使用 `~` 别名引用项目根目录：

```typescript
// 使用 ~ 别名
import { helper } from '~/utils/helper';

// 相当于
import { helper } from '../../utils/helper';
```

### 3.2 配置路径别名

在 `wxt.config.ts` 中配置自定义路径别名：

```typescript
import { defineConfig } from 'wxt';
import path from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@components': path.resolve(__dirname, 'src/components'),
      '@utils': path.resolve(__dirname, 'src/utils'),
      '@types': path.resolve(__dirname, 'src/types'),
    },
  },
});
```

**使用自定义别名：**

```typescript
import { Button } from '@components/ui/Button';
import { fetchData } from '@utils/api';
import type { User } from '@types';
```

## 四、环境变量

### 4.1 环境变量文件

在项目根目录创建 `.env` 文件：

```bash
# .env
NODE_ENV=development
WXT_API_URL=https://api.example.com
WXT_API_KEY=your-api-key
```

**环境特定文件：**

```bash
# .env.development
NODE_ENV=development
WXT_API_URL=https://dev-api.example.com

# .env.production
NODE_ENV=production
WXT_API_URL=https://api.example.com
```

### 4.2 使用环境变量

在代码中使用环境变量：

```typescript
const apiUrl = import.meta.env.WXT_API_URL;
const apiKey = import.meta.env.WXT_API_KEY;

console.log('API URL:', apiUrl);
console.log('API Key:', apiKey);
```

### 4.3 配置环境变量前缀

在 `wxt.config.ts` 中配置环境变量前缀：

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  envPrefix: 'WXT_', // 仅加载 WXT_ 开头的环境变量
});
```

## 五、类型定义

### 5.1 自动类型生成

WXT 会自动生成类型定义文件：

- `.wxt/types/`：WXT 生成的类型
- `wxt/client-types`：浏览器 API 类型

### 5.2 自定义类型

创建 `src/types/` 目录：

```
src/types/
├── index.ts
├── message.ts
├── storage.ts
└── api.ts
```

**message.ts：**

```typescript
export interface Message {
  type: string;
  payload?: any;
}

export interface Response {
  data?: any;
  error?: boolean;
  message?: string;
}
```

**storage.ts：**

```typescript
export interface Storage {
  apiKey: string;
  enabled: boolean;
  theme: 'light' | 'dark' | 'auto';
}
```

## 六、目录组织最佳实践

### 6.1 小型项目

```
my-extension/
├── entrypoints/
├── public/
├── wxt.config.ts
├── package.json
└── tsconfig.json
```

### 6.2 中型项目

```
my-extension/
├── src/
│   ├── entrypoints/
│   ├── components/
│   ├── lib/
│   └── styles/
├── public/
├── wxt.config.ts
├── package.json
└── tsconfig.json
```

### 6.3 大型项目

```
my-extension/
├── src/
│   ├── entrypoints/
│   ├── components/
│   │   ├── ui/
│   │   └── features/
│   ├── composables/
│   ├── lib/
│   │   ├── api/
│   │   ├── utils/
│   │   ├── types/
│   │   └── constants/
│   ├── stores/
│   ├── styles/
│   └── assets/
├── public/
├── wxt.config.ts
├── package.json
└── tsconfig.json
```

## 七、常见问题

### Q1: 如何修改入口点目录位置？

**方法：** 在 `wxt.config.ts` 中配置 `entrypointsDir`：

```typescript
export default defineConfig({
  entrypointsDir: 'src/entrypoints',
});
```

### Q2: 如何修改公共资源目录位置？

**方法：** 在 `wxt.config.ts` 中配置 `publicDir`：

```typescript
export default defineConfig({
  publicDir: 'assets',
});
```

### Q3: 如何忽略某些文件？

**方法：** 在 `.gitignore` 中添加：

```
.output/
.wxt/
node_modules/
.env
*.log
```

### Q4: 如何共享代码？

**方法：** 创建 `lib/` 或 `utils/` 目录：

```
src/
├── entrypoints/
└── lib/
    ├── api.ts
    ├── storage.ts
    └── utils.ts
```

**在入口点中导入：**

```typescript
import { fetchData } from '~/lib/api';
import { storage } from '~/lib/storage';
```

### Q5: 如何管理不同环境的配置？

**方法：** 使用环境变量和条件配置：

```typescript
export default defineConfig(({ mode }) => ({
  manifest: {
    name: mode === 'development'
      ? 'My Extension (Dev)'
      : 'My Extension',
  },
}));
```

## 八、下一步

- [入口点详解](https://wxt.dev/guide/essentials/entrypoints.html)：学习入口点配置
- [配置详解](https://wxt.dev/guide/essentials/configuration.html)：学习 WXT 配置
- [前端框架](https://wxt.dev/guide/essentials/frontend-frameworks.html)：学习框架集成
- [静态资源](https://wxt.dev/guide/essentials/assets.html)：学习资源管理
