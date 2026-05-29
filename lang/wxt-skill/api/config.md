# 配置 API 详解

本文档详细说明 WXT 的所有配置 API，包括函数签名、参数说明和使用示例。

## 官方导航链接

- [Configuration](https://wxt.dev/guide/essentials/config/) - 配置相关完整指南
  - [Manifest](https://wxt.dev/guide/essentials/config/manifest.html) - Manifest 配置详解
  - [Browser Startup](https://wxt.dev/guide/essentials/config/browser-startup.html) - 浏览器启动相关配置
  - [Auto-imports](https://wxt.dev/guide/essentials/config/auto-imports.html) - 自动导入配置
  - [Environment Variables](https://wxt.dev/guide/essentials/config/environment-variables.html) - 环境变量配置
  - [Runtime Config](https://wxt.dev/guide/essentials/config/runtime.html) - 运行时配置
  - [Vite](https://wxt.dev/guide/essentials/config/vite.html) - Vite 构建工具集成配置
  - [Build Mode](https://wxt.dev/guide/essentials/config/build-mode.html) - 构建模式配置
  - [TypeScript](https://wxt.dev/guide/essentials/config/typescript.html) - TypeScript 类型配置
  - [Hooks](https://wxt.dev/guide/essentials/config/hooks.html) - 构建与运行时钩子函数
  - [Entrypoint Loaders](https://wxt.dev/guide/essentials/config/entrypoint-loaders.html) - 入口脚本加载器配置

---

## 配置概览

WXT 的配置主要通过 `wxt.config.ts` 文件定义。

| 配置函数 | 说明 |
|----------|------|
| `defineConfig` | 定义 WXT 配置 |
| `defineManifest` | 定义 manifest.json 配置 |
| `defineBackground` | 定义后台脚本配置 |
| `defineContentScript` | 定义内容脚本配置 |
| `definePopup` | 定义弹出页面配置 |
| `defineOptions` | 定义选项页面配置 |

## 一、defineConfig

### 1.1 函数签名

```typescript
function defineConfig(config: UserConfig): ResolvedConfig;

interface UserConfig {
  manifest?: ManifestConfig;
  build?: BuildConfig;
  dev?: DevConfig;
  modules?: ModuleOption[];
  hooks?: HooksConfig;
  plugins?: PluginOption[];
  publicDir?: string;
  outDir?: string;
  cacheDir?: string;
  root?: string;
  mode?: 'development' | 'production';
  envPrefix?: string | string[];
  envDir?: string;
}
```

### 1.2 基本配置

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  // 入口点目录
  root: process.cwd(),

  // 输出目录
  outDir: '.output',

  // 公共目录
  publicDir: 'public',

  // 缓存目录
  cacheDir: '.wxt',

  // 构建模式
  mode: 'production',

  // 环境变量前缀
  envPrefix: 'WXT_',
});
```

### 1.3 Manifest 配置

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    // 基本信息
    name: 'My Extension',
    version: '1.0.0',
    description: 'A browser extension built with WXT',

    // 权限
    permissions: ['storage', 'tabs'],
    host_permissions: ['<all_urls>'],

    // 浏览器特定配置
    chrome: {
      permissions: ['alarms'],
    },
    firefox: {
      permissions: ['alarms'],
    },
    edge: {
      permissions: ['alarms'],
    },
    safari: {
      permissions: ['alarms'],
    },

    // 覆盖配置
    overrides: {
      // 覆盖 manifest 字段
    },
  },
});
```

### 1.4 构建配置

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  build: {
    // 生成 sourcemap
    sourcemap: true,

    // 压缩配置
    minify: 'esbuild', // 'esbuild' | 'terser' | false

    // 目标浏览器
    target: 'es2020',

    // Rollup 配置
    rollupOptions: {
      output: {
        // chunk 文件名
        chunkFileNames: 'chunks/[name]-[hash].js',
        // entry 文件名
        entryFileNames: 'entries/[name]-[hash].js',
        // asset 文件名
        assetFileNames: 'assets/[name]-[hash].[ext]',
        // 启用哈希
        hash: true,
      },
      // 输入配置
      input: {},
      // 外部化依赖
      external: [],
      // 插件
      plugins: [],
      // 缓存
      cache: true,
    },

    // 代码分割配置
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks: (id) => {
          // 手动代码分割
          if (id.includes('node_modules')) {
            return 'vendor';
          }
        },
      },
    },
  },
});
```

### 1.5 开发配置

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  dev: {
    // 开发服务器配置
    server: {
      port: 3000,
      strictPort: false,
      host: 'localhost',
      open: true,
    },

    // HMR 配置
    hmr: {
      host: 'localhost',
      port: 3000,
      overlay: true,
    },

    // 浏览器配置
    browser: 'chrome', // 'chrome' | 'firefox' | 'edge' | 'safari'

    // 自动打开浏览器
    openBrowser: true,

    // 监听配置
    watch: {
      ignored: ['node_modules', '.output'],
    },
  },
});
```

### 1.6 模块配置

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  modules: [
    // Svelte 模块
    '@wxt-dev/module-svelte',

    // Solid 模块
    '@wxt-dev/module-solid',

    // Vue 模块
    '@wxt-dev/module-vue',

    // React 模块
    '@wxt-dev/module-react',
  ],
});
```

### 1.7 钩子配置

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  hooks: {
    // 构建钩子
    'prepare:build': async (ctx) => {
      console.log('准备构建');
    },
    'resolve:entrypoints': async (ctx) => {
      console.log('解析入口点');
    },
    'analyze:modules': async (ctx) => {
      console.log('分析模块');
    },
    'transform:code': async (ctx) => {
      console.log('转换代码');
    },
    'build:module': async (ctx) => {
      console.log('构建模块');
    },
    'generate:manifest': async (ctx) => {
      console.log('生成 manifest');
    },
    'optimize:output': async (ctx) => {
      console.log('优化输出');
    },
    'build:done': async (ctx) => {
      console.log('构建完成');
    },

    // 开发钩子
    'dev:server:start': async (ctx) => {
      console.log('开发服务器启动');
    },
    'dev:server:restart': async (ctx) => {
      console.log('开发服务器重启');
    },
    'dev:file:change': async (ctx) => {
      console.log('文件变化');
    },
    'dev:server:close': async (ctx) => {
      console.log('开发服务器关闭');
    },
  },
});
```

### 1.8 插件配置

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  plugins: [
    // 自定义插件
    {
      name: 'my-plugin',
      config(config) {
        // 修改配置
        return config;
      },
      configResolved(config) {
        // 配置解析后
      },
      transform(code, id) {
        // 转换代码
        return code;
      },
    },
  ],
});
```

---

## 二、defineManifest

### 2.1 函数签名

```typescript
function defineManifest(manifest: ManifestConfig): ManifestConfig;

interface ManifestConfig {
  name?: string;
  version?: string;
  description?: string;
  author?: string;
  homepage_url?: string;
  permissions?: string[];
  host_permissions?: string[];
  optional_permissions?: string[];
  background?: BackgroundConfig;
  content_scripts?: ContentScriptConfig[];
  action?: ActionConfig;
  options_page?: string;
  options_ui?: OptionsUIConfig;
  devtools_page?: string;
  sidebar_action?: SidebarActionConfig;
  icons?: IconsConfig;
  web_accessible_resources?: WebAccessibleResourcesConfig;
  chrome?: ChromeSpecificConfig;
  firefox?: FirefoxSpecificConfig;
  edge?: EdgeSpecificConfig;
  safari?: SafariSpecificConfig;
}
```

### 2.2 基本配置

```typescript
import { defineConfig, defineManifest } from 'wxt';

export default defineConfig({
  manifest: defineManifest({
    name: 'My Extension',
    version: '1.0.0',
    description: 'A browser extension built with WXT',
    author: 'Your Name',
    homepage_url: 'https://example.com',

    // 权限
    permissions: [
      'storage',
      'tabs',
      'activeTab',
      'scripting',
    ],

    // 主机权限
    host_permissions: [
      'https://api.example.com/*',
    ],

    // 可选权限
    optional_permissions: [
      'alarms',
      'bookmarks',
    ],

    // 图标
    icons: {
      16: 'icons/icon-16.png',
      32: 'icons/icon-32.png',
      48: 'icons/icon-48.png',
      128: 'icons/icon-128.png',
    },

    // 操作（浏览器按钮）
    action: {
      default_title: 'My Extension',
      default_popup: 'popup.html',
      default_icon: {
        16: 'icons/icon-16.png',
        32: 'icons/icon-32.png',
        48: 'icons/icon-48.png',
        128: 'icons/icon-128.png',
      },
    },

    // 选项页面
    options_page: 'options.html',

    // 选项 UI（Chrome）
    options_ui: {
      page: 'options.html',
      open_in_tab: true,
    },

    // 开发者工具
    devtools_page: 'devtools.html',

    // 可访问的资源
    web_accessible_resources: [
      {
        resources: ['icons/*'],
        matches: ['<all_urls>'],
      },
    ],

    // 浏览器特定配置
    chrome: {
      permissions: ['alarms', 'idle'],
    },

    firefox: {
      permissions: ['alarms'],
      browser_specific_settings: {
        gecko: {
          id: 'my-extension@example.com',
          strict_min_version: '102.0',
        },
      },
    },

    edge: {
      permissions: ['alarms'],
    },

    safari: {
      permissions: ['alarms'],
    },
  }),
});
```

### 2.3 后台脚本配置

```typescript
manifest: defineManifest({
  background: {
    service_worker: 'background.js',
    type: 'module',
  },
});
```

### 2.4 内容脚本配置

```typescript
manifest: defineManifest({
  content_scripts: [
    {
      matches: ['<all_urls>'],
      js: ['content.js'],
      css: ['content.css'],
      run_at: 'document_idle',
      all_frames: false,
    },
  ],
});
```

### 2.5 覆盖配置

```typescript
manifest: defineManifest({
  overrides: {
    // 覆盖 manifest 字段
    name: 'Custom Name',
    version: '2.0.0',
  },
});
```

---

## 三、高级配置

### 3.1 多环境配置

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  mode: process.env.NODE_ENV || 'development',

  manifest: {
    name: process.env.NODE_ENV === 'production'
      ? 'My Extension'
      : 'My Extension (Dev)',
  },
});
```

### 3.2 多浏览器配置

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: 'My Extension',

    chrome: {
      permissions: ['alarms'],
    },

    firefox: {
      permissions: ['alarms'],
      browser_specific_settings: {
        gecko: {
          id: 'my-extension@example.com',
        },
      },
    },

    edge: {
      permissions: ['alarms'],
    },

    safari: {
      permissions: ['alarms'],
    },
  },
});
```

### 3.3 条件配置

```typescript
import { defineConfig } from 'wxt';

export default defineConfig(({ mode }) => ({
  mode,
  build: {
    sourcemap: mode === 'development',
    minify: mode === 'production',
  },
}));
```

### 3.4 自定义插件

```typescript
import { defineConfig } from 'wxt';

function myPlugin() {
  return {
    name: 'my-plugin',

    config(config) {
      // 修改配置
      config.manifest = {
        ...config.manifest,
        custom_field: 'custom_value',
      };
      return config;
    },

    configResolved(config) {
      // 配置解析后
      console.log('Config resolved:', config);
    },

    transform(code, id) {
      // 转换代码
      if (id.endsWith('.ts')) {
        return code.replace('FOO', 'BAR');
      }
      return code;
    },

    async buildStart() {
      // 构建开始
      console.log('Build start');
    },

    async buildEnd() {
      // 构建结束
      console.log('Build end');
    },
  };
}

export default defineConfig({
  plugins: [myPlugin()],
});
```

### 3.5 环境变量

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: process.env.WXT_NAME || 'My Extension',
    version: process.env.WXT_VERSION || '1.0.0',
  },
});
```

**.env 文件：**

```bash
WXT_NAME=My Extension
WXT_VERSION=1.0.0
WXT_API_URL=https://api.example.com
```

**.env.production 文件：**

```bash
WXT_NAME=My Extension (Production)
WXT_VERSION=1.0.0
WXT_API_URL=https://api.example.com
```

### 3.6 路径别名

```typescript
import { defineConfig } from 'wxt';
import path from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@components': path.resolve(__dirname, 'src/components'),
      '@utils': path.resolve(__dirname, 'src/utils'),
    },
  },
});
```

**在代码中使用别名：**

```typescript
import { Button } from '@components/ui/Button';
import { fetchData } from '@utils/api';
```

---

## 四、配置验证

### 4.1 验证配置

WXT 会自动验证配置，但您也可以手动验证：

```typescript
import { defineConfig, validateConfig } from 'wxt';

const config = {
  manifest: {
    name: 'My Extension',
    version: '1.0.0',
  },
};

const result = validateConfig(config);

if (result.errors.length > 0) {
  console.error('Config errors:', result.errors);
}
```

### 4.2 配置提示

WXT 会自动检测常见配置错误并提示：

- 缺少必需字段
- 权限配置错误
- 路径错误
- 类型错误

---

## 五、常见问题

### Q1: 如何根据环境加载不同配置？

**方法一：使用 process.env**

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  mode: process.env.NODE_ENV || 'development',

  build: {
    sourcemap: process.env.NODE_ENV === 'development',
    minify: process.env.NODE_ENV === 'production',
  },
});
```

**方法二：使用条件配置**

```typescript
import { defineConfig } from 'wxt';

export default defineConfig(({ mode }) => ({
  mode,
  build: {
    sourcemap: mode === 'development',
    minify: mode === 'production',
  },
}));
```

### Q2: 如何添加自定义 manifest 字段？

**方法一：使用 overrides**

```typescript
manifest: defineManifest({
  overrides: {
    custom_field: 'custom_value',
  },
});
```

**方法二：使用钩子**

```typescript
hooks: {
  'generate:manifest': async (ctx) => {
    ctx.manifest.custom_field = 'custom_value';
  },
}
```

### Q3: 如何处理多浏览器配置差异？

**使用浏览器特定配置：**

```typescript
manifest: defineManifest({
  chrome: {
    permissions: ['alarms'],
  },
  firefox: {
    permissions: ['alarms'],
    browser_specific_settings: {
      gecko: {
        id: 'my-extension@example.com',
      },
    },
  },
});
```

### Q4: 如何配置多个入口点？

**在 `entrypoints/` 目录中创建多个入口点：**

```
entrypoints/
├── background.ts
├── content.ts
├── popup.html
├── popup.ts
├── options.html
└── options.ts
```

**WXT 会自动检测并包含所有入口点。**

### Q5: 如何配置路径别名？

**使用 resolve.alias：**

```typescript
import { defineConfig } from 'wxt';
import path from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
});
```

**在代码中使用：**

```typescript
import { Button } from '@/components/Button';
```

---

## 六、最佳实践

### 6.1 配置文件组织

**推荐结构：**

```
wxt.config.ts
config/
├── base.ts       # 基础配置
├── manifest.ts   # Manifest 配置
├── build.ts      # 构建配置
└── hooks.ts      # 钩子配置
```

**wxt.config.ts：**

```typescript
import { defineConfig } from 'wxt';
import baseConfig from './config/base';
import manifestConfig from './config/manifest';
import buildConfig from './config/build';
import hooksConfig from './config/hooks';

export default defineConfig({
  ...baseConfig,
  manifest: manifestConfig,
  build: buildConfig,
  hooks: hooksConfig,
});
```

### 6.2 环境配置

**.env：**

```bash
# 基础配置
NODE_ENV=development
WXT_NAME=My Extension
```

**.env.development：**

```bash
NODE_ENV=development
WXT_NAME=My Extension (Dev)
```

**.env.production：**

```bash
NODE_ENV=production
WXT_NAME=My Extension (Production)
```

### 6.3 类型安全

**使用 TypeScript 类型：**

```typescript
import type { UserConfig, ManifestConfig } from 'wxt';

const manifest: ManifestConfig = {
  name: 'My Extension',
  version: '1.0.0',
};

const config: UserConfig = {
  manifest,
};
```

### 6.4 配置注释

**添加详细注释：**

```typescript
export default defineConfig({
  /**
   * 入口点目录
   */
  root: process.cwd(),

  /**
   * 输出目录
   */
  outDir: '.output',

  /**
   * 公共目录
   */
  publicDir: 'public',
});
```

---

## 七、配置参考

### 7.1 完整配置示例

```typescript
import { defineConfig } from 'wxt';
import path from 'path';

export default defineConfig({
  // 入口点目录
  root: process.cwd(),

  // 输出目录
  outDir: '.output',

  // 公共目录
  publicDir: 'public',

  // 缓存目录
  cacheDir: '.wxt',

  // 构建模式
  mode: 'production',

  // 环境变量前缀
  envPrefix: 'WXT_',

  // 模块
  modules: ['@wxt-dev/module-svelte'],

  // 插件
  plugins: [],

  // 路径别名
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },

  // Manifest 配置
  manifest: {
    name: 'My Extension',
    version: '1.0.0',
    description: 'A browser extension built with WXT',
    permissions: ['storage', 'tabs'],
    host_permissions: ['<all_urls>'],
  },

  // 构建配置
  build: {
    sourcemap: true,
    minify: 'esbuild',
    target: 'es2020',
    rollupOptions: {
      output: {
        chunkFileNames: 'chunks/[name]-[hash].js',
        entryFileNames: 'entries/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]',
      },
    },
  },

  // 开发配置
  dev: {
    server: {
      port: 3000,
      strictPort: false,
      host: 'localhost',
    },
  },

  // 钩子
  hooks: {
    'build:done': async (ctx) => {
      console.log('构建完成');
    },
  },
});
```

## 下一步

- [入口点 API](./entrypoints.md)：学习入口点 API
- [工具函数](./utilities.md)：学习存储、脚本注入等工具函数
- [构建阶段](../lifecycle/phases.md)：了解构建流程
- [示例代码](../examples/)：查看完整项目示例
