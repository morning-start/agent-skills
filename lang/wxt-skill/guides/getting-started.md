# WXT 入门指南

本指南基于 WXT 官方文档整理，帮助您快速上手 WXT 框架。

## 官方导航链接

### Get Started（快速开始）
- [Introduction](https://wxt.dev/guide/introduction.html) - WXT 框架概述，核心优势与特性介绍
- [Installation](https://wxt.dev/guide/installation.html) - 环境要求、项目初始化步骤、模板选择

### Essentials（核心指南）
- [Project Structure](https://wxt.dev/guide/essentials/project-structure.html) - 项目目录结构规范，核心文件作用说明
- [Entrypoints](https://wxt.dev/guide/essentials/entrypoints.html) - 入口脚本类型（背景 / 内容 / 弹出层等）配置规则
- [Configuration](https://wxt.dev/guide/essentials/config/) - 配置相关子分类
  - [Manifest](https://wxt.dev/guide/essentials/config/manifest.html) - Manifest 配置详解，权限与基础信息设置
  - [Browser Startup](https://wxt.dev/guide/essentials/config/browser-startup.html) - 浏览器启动相关配置，调试与运行参数
  - [Auto-imports](https://wxt.dev/guide/essentials/config/auto-imports.html) - 自动导入配置，简化模块引用
  - [Environment Variables](https://wxt.dev/guide/essentials/config/environment-variables.html) - 环境变量配置与使用方法
  - [Runtime Config](https://wxt.dev/guide/essentials/config/runtime.html) - 运行时配置，动态参数调整
  - [Vite](https://wxt.dev/guide/essentials/config/vite.html) - Vite 构建工具集成配置
  - [Build Mode](https://wxt.dev/guide/essentials/config/build-mode.html) - 构建模式配置，开发 / 生产环境区分
  - [TypeScript](https://wxt.dev/guide/essentials/config/typescript.html) - TypeScript 类型配置与类型提示优化
  - [Hooks](https://wxt.dev/guide/essentials/config/hooks.html) - 构建与运行时钩子函数配置
  - [Entrypoint Loaders](https://wxt.dev/guide/essentials/config/entrypoint-loaders.html) - 入口脚本加载器配置
- [Extension APIs](https://wxt.dev/guide/essentials/extension-apis.html) - 浏览器扩展 API 调用与适配
- [Assets](https://wxt.dev/guide/essentials/assets.html) - 静态资源（图片、样式等）管理
- [Target Different Browsers](https://wxt.dev/guide/essentials/target-different-browsers.html) - 多浏览器（Chrome/Firefox 等）适配方案
- [Content Scripts](https://wxt.dev/guide/essentials/content-scripts.html) - 内容脚本开发与注入规则
- [Storage](https://wxt.dev/guide/essentials/storage.html) - 数据存储方案，WXT 存储 API 与浏览器 storage 适配
- [Messaging](https://wxt.dev/guide/essentials/messaging.html) - 扩展内脚本间通信方法（背景 / 内容 / 弹出层）
- [I18n](https://wxt.dev/guide/essentials/i18n.html) - 国际化与本地化配置，多语言支持
- [Scripting](https://wxt.dev/guide/essentials/scripting.html) - 动态脚本注入与执行
- [WXT Modules](https://wxt.dev/guide/essentials/wxt-modules.html) - WXT 模块开发与使用
- [Frontend Frameworks](https://wxt.dev/guide/essentials/frontend-frameworks.html) - React/Vue/Svelte 等前端框架集成
- [ES Modules](https://wxt.dev/guide/essentials/es-modules.html) - ES 模块在扩展中的使用规范
- [Remote Code](https://wxt.dev/guide/essentials/remote-code.html) - 远程代码加载与安全策略
- [Unit Testing](https://wxt.dev/guide/essentials/unit-testing.html) - 单元测试配置与编写方法
- [E2E Testing](https://wxt.dev/guide/essentials/e2e-testing.html) - 端到端测试，Playwright 集成
- [Publishing](https://wxt.dev/guide/essentials/publishing.html) - 扩展打包与应用商店发布流程
- [Testing Updates](https://wxt.dev/guide/essentials/testing-updates.html) - 扩展更新测试方法

---

## 框架概述

### WXT 是什么

WXT（Web eXtensions Tools）是一个基于 Vite 构建的现代化浏览器扩展开发框架，专为 Manifest V3 设计。

**核心特性：**
- 声明式入口点定义，自动生成 manifest 配置
- 基于 Vite 的极速构建速度
- 完整的 TypeScript 类型支持
- 多框架支持（Vanilla、Vue、React、Svelte、Solid）
- 多浏览器一键构建（Chrome、Firefox、Edge、Safari）
- 内置热重载和开发服务器

**官方资源：**
- 安装指南：https://wxt.dev/guide/installation.html
- 项目结构：https://wxt.dev/guide/essentials/project-structure.html
- 入口点：https://wxt.dev/guide/essentials/entrypoints.html

## 一、环境准备

### 1.1 安装 Bun（推荐）

Bun 是一个现代化的 JavaScript 运行时和包管理器，速度快且磁盘占用小。

**Windows（PowerShell）：**
```powershell
irm https://bun.sh/install.ps1 | iex
```

**macOS / Linux：**
```bash
curl -fsSL https://bun.sh/install | bash
```

**验证安装：**
```bash
bun --version
```

### 1.2 安装浏览器

开发 WXT 扩展需要安装目标浏览器：

| 浏览器 | 版本要求 | 下载地址 |
|--------|----------|----------|
| Chrome | 88+ | https://www.google.com/chrome/ |
| Firefox | 102+ | https://www.mozilla.org/firefox/ |
| Edge | 88+ | https://www.microsoft.com/edge |
| Safari | 16+ | macOS 系统自带 |

### 1.3 验证环境

```bash
# 检查 Bun
bun --version

# 检查 Node.js（Bun 内置）
bun --version

# 检查浏览器（macOS/Linux）
which google-chrome  # Chrome
which firefox       # Firefox
```

## 二、创建项目

### 2.1 使用 bunx wxt 创建项目（推荐）

这是 WXT 官方推荐的创建方式。

**创建命令：**
```bash
bunx wxt@latest init
```

**交互式创建流程：**

#### 第一步：选择项目模板

```
? Select a template: (Use arrow keys)
❯ Vanilla
  Vue
  React
  Svelte    # 推荐
  Solid     # 推荐
```

**模板说明：**
- **Svelte**：轻量、高性能、编译时优化，学习曲线平缓
- **Solid**：细粒度响应式、性能最佳
- **Vue**：生态成熟、中文文档丰富
- **React**：生态庞大、虚拟 DOM
- **Vanilla**：无框架、简单直接

#### 第二步：选择包管理器

```
? Select package manager: (Use arrow keys)
❯ bun       # 推荐
  npm
  pnpm
  yarn
```

#### 第三步：输入项目名称

```
? Project name: my-extension
```

#### 第四步：确认创建

```
? Confirm project creation? (Y/n) y
```

### 2.2 创建后的项目结构

创建完成后，项目结构如下：

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
- 项目结构详解：https://wxt.dev/guide/essentials/project-structure.html

### 2.3 启动开发服务器

```bash
cd my-extension
bun run dev
```

WXT 会自动：
1. 编译源代码
2. 启动本地服务器（默认端口 3000）
3. 打开浏览器窗口
4. 安装开发版本扩展
5. 监听文件变化并热重载

## 三、入口点详解

### 3.1 入口点类型

WXT 支持以下类型的入口点：

| 类型 | 函数 | 说明 |
|------|------|------|
| Background Script | `defineBackground` | 后台脚本，在扩展后台持续运行 |
| Content Script | `defineContentScript` | 内容脚本，注入到网页上下文中 |
| Popup | `definePopup` | 弹出页面，用户点击扩展图标时显示 |
| Options | `defineOptions` | 选项页面，扩展的设置页面 |
| DevTools | `defineDevTools` | 开发者工具页面 |
| Sidebar | `defineSidebar` | 侧边栏页面（仅 Firefox） |

**参考文档：**
- 入口点详解：https://wxt.dev/guide/essentials/entrypoints.html

### 3.2 Background Script（后台脚本）

后台脚本在扩展后台持续运行，用于处理浏览器事件、管理状态、协调通信。

```typescript
// entrypoints/background.ts
import { defineBackground } from 'wxt/sandbox';

export default defineBackground(() => {
  console.log('Background script started');

  // 监听扩展安装
  browser.runtime.onInstalled.addListener(() => {
    console.log('Extension installed');
  });

  // 监听消息
  browser.runtime.onMessage.addListener((message, sender) => {
    console.log('Received message:', message);
    return Promise.resolve('Response from background');
  });
});
```

### 3.3 Content Script（内容脚本）

内容脚本注入到网页上下文中，可以访问和操作页面 DOM。

```typescript
// entrypoints/content.ts
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],
  runAt: 'document_idle',
  main() {
    console.log('Content script injected');

    // 操作 DOM
    const button = document.createElement('button');
    button.textContent = 'Click me';
    button.addEventListener('click', () => {
      browser.runtime.sendMessage({ type: 'CONTENT_CLICK' });
    });
    document.body.appendChild(button);
  },
});
```

### 3.4 Popup（弹出页面）

弹出页面是用户点击扩展图标时显示的界面。

**HTML 文件（entrypoints/popup.html）：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Popup</title>
</head>
<body>
  <h1>Hello, WXT!</h1>
  <script type="module" src="./popup.ts"></script>
</body>
</html>
```

**逻辑文件（entrypoints/popup.ts）：**

```typescript
console.log('Popup loaded');

// 发送消息到后台脚本
browser.runtime.sendMessage({ type: 'POPUP_OPEN' }).then((response) => {
  console.log('Response:', response);
});
```

### 3.5 Options（选项页面）

选项页面是扩展的设置页面，用户可以在这里配置扩展。

**HTML 文件（entrypoints/options.html）：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Options</title>
</head>
<body>
  <h1>Options</h1>
  <button id="save">Save Settings</button>
  <script type="module" src="./options.ts"></script>
</body>
</html>
```

**逻辑文件（entrypoints/options.ts）：**

```typescript
// 保存设置
document.getElementById('save')!.addEventListener('click', async () => {
  await browser.storage.sync.set({ enabled: true });
  alert('Settings saved!');
});

// 加载设置
browser.storage.sync.get(['enabled']).then((data) => {
  console.log('Settings:', data);
});
```

## 四、静态资源管理

### 4.1 公共资源目录

`public/` 目录包含直接复制到构建输出的文件：

```
public/
├── _locales/                    # 国际化文件
│   └── en/
│       └── messages.json
├── images/                     # 图片资源
│   ├── icon-16.png
│   ├── icon-48.png
│   └── icon-128.png
└── manifest-overrides/          # Manifest 覆盖配置
    └── chrome.json
```

### 4.2 导入静态资源

在代码中导入静态资源：

```typescript
// 导入图片
import iconUrl from '~/images/icon-16.png';

// 使用图片
console.log(iconUrl);
browser.action.setIcon({ path: iconUrl });
```

### 4.3 路径处理

WXT 支持使用 `~` 别名引用项目根目录：

```typescript
// 使用 ~ 别名
import { helper } from '~/utils/helper';

// 相当于
import { helper } from '../../utils/helper';
```

**参考文档：**
- 静态资源：https://wxt.dev/guide/essentials/assets.html

## 五、前端框架集成

### 5.1 支持的框架

WXT 原生支持以下框架：

| 框架 | 推荐度 | 特点 |
|------|--------|------|
| **Svelte** | ⭐⭐⭐⭐⭐ | 轻量、高性能、编译时优化 |
| **Solid** | ⭐⭐⭐⭐⭐ | 细粒度响应式、性能最佳 |
| **Vue** | ⭐⭐⭐⭐ | 生态成熟、中文文档丰富 |
| **React** | ⭐⭐⭐⭐ | 生态庞大、虚拟 DOM |
| **Vanilla** | ⭐⭐⭐ | 无框架、简单直接 |

### 5.2 创建框架项目

使用 `bunx wxt@latest init` 创建项目时，选择对应的框架模板即可。

**参考文档：**
- 前端框架：https://wxt.dev/guide/essentials/frontend-frameworks.html
- 框架配置：[框架配置](./framework-setup.md)

## 六、基础配置

### 6.1 WXT 配置文件

`wxt.config.ts` 是 WXT 的核心配置文件：

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: 'My Extension',
    version: '1.0.0',
    description: 'A browser extension built with WXT',
    permissions: ['storage'],
    host_permissions: ['<all_urls>'],
  },
});
```

### 6.2 TypeScript 配置

`tsconfig.json` 配置 TypeScript：

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
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

**参考文档：**
- 配置详解：https://wxt.dev/guide/essentials/configuration.html

## 七、权限配置

### 7.1 权限类型

浏览器扩展需要声明所需的权限：

```typescript
export default defineConfig({
  manifest: {
    // 基础权限
    permissions: [
      'storage',        // 存储权限
      'tabs',           // 标签页权限
      'activeTab',      // 活动标签页权限
      'scripting',      // 脚本注入权限
    ],

    // 主机权限
    host_permissions: [
      '<all_urls>',     // 所有网站
      'https://api.example.com/*',  // 特定网站
    ],
  },
});
```

### 7.2 动态权限

可以在运行时申请额外权限：

```typescript
// 申请权限
browser.permissions.request({
  permissions: ['alarms'],
  origins: ['https://api.example.com/*'],
}).then((granted) => {
  if (granted) {
    console.log('Permissions granted');
  } else {
    console.log('Permissions denied');
  }
});
```

**参考文档：**
- 权限详解：https://wxt.dev/guide/essentials/permissions.html

## 八、消息传递

### 8.1 跨脚本通信

WXT 支持在 Background Script、Content Script、Popup 之间传递消息。

**Content Script 发送消息：**

```typescript
browser.runtime.sendMessage({
  type: 'GET_DATA',
  payload: { id: 123 },
}).then((response) => {
  console.log('Response:', response);
});
```

**Background Script 接收消息：**

```typescript
browser.runtime.onMessage.addListener((message, sender) => {
  console.log('Received message:', message);
  return Promise.resolve({ data: 'Hello from background' });
});
```

### 8.2 标签到 Popup 通信

**Popup 发送消息到 Content Script：**

```typescript
browser.tabs.query({ active: true, currentWindow: true }).then((tabs) => {
  const tabId = tabs[0].id;
  browser.tabs.sendMessage(tabId, {
    type: 'FROM_POPUP',
    data: 'Hello from popup',
  });
});
```

**Content Script 接收消息：**

```typescript
browser.runtime.onMessage.addListener((message, sender) => {
  if (message.type === 'FROM_POPUP') {
    console.log('Received from popup:', message.data);
    return Promise.resolve({ status: 'OK' });
  }
});
```

**参考文档：**
- 消息传递：https://wxt.dev/guide/essentials/messaging.html

## 九、数据存储

### 9.1 存储类型

WXT 支持三种存储类型：

| 存储类型 | 说明 | 限制 |
|----------|------|------|
| `storage.sync` | 同步存储，跨设备同步 | 102KB |
| `storage.local` | 本地存储 | 5MB |
| `storage.session` | 会话存储 | 1MB |

### 9.2 使用存储

**写入数据：**

```typescript
// 写入同步存储
await browser.storage.sync.set({
  apiKey: 'your-api-key',
  enabled: true,
});

// 写入本地存储
await browser.storage.local.set({
  cache: 'data',
});
```

**读取数据：**

```typescript
// 读取特定键
const data = await browser.storage.sync.get(['apiKey', 'enabled']);
console.log('API Key:', data.apiKey);

// 读取所有数据
const allData = await browser.storage.sync.get(null);
console.log('All data:', allData);
```

**监听存储变化：**

```typescript
browser.storage.onChanged.addListener((changes, areaName) => {
  console.log('Storage changed:', areaName, changes);
});
```

**参考文档：**
- 存储详解：https://wxt.dev/guide/essentials/storage.html

## 十、构建和发布

### 10.1 构建扩展

```bash
# 构建生产版本
bun run build

# 构建特定浏览器
bun run build:chrome      # Chrome
bun run build:firefox     # Firefox
bun run build:edge        # Edge
```

### 10.2 打包扩展

```bash
# 打包扩展
bun run zip

# 打包特定浏览器
bun run zip:chrome
bun run zip:firefox
```

### 10.3 发布扩展

发布到不同的浏览器商店：

| 浏览器 | 商店 | 账户费用 | 审核时间 |
|--------|------|----------|----------|
| Chrome | Chrome Web Store | $5 | 2-5 天 |
| Firefox | Firefox Add-ons | 免费 | 1-3 天 |
| Edge | Microsoft Edge Add-ons | $19 | 1-3 天 |
| Safari | Safari App Store | $99/年 | 1-2 周 |

**参考文档：**
- 发布详解：https://wxt.dev/guide/essentials/publishing.html
- 部署指南：[部署指南](./deployment.md)

## 下一步

- [框架配置](./framework-setup.md)：学习各框架的完整配置
- [浏览器适配](./browser-adapter.md)：学习不同浏览器的适配
- [命令参考](../cli/commands.md)：掌握开发和构建命令
- [入口点 API](../api/entrypoints.md)：学习入口点 API
- [示例代码](../examples/)：查看完整项目示例

## 官方文档链接

| 文档 | 链接 |
|------|------|
| Introduction | https://wxt.dev/guide/introduction.html |
| Installation | https://wxt.dev/guide/installation.html |
| Entrypoints | https://wxt.dev/guide/essentials/entrypoints.html |
| Assets | https://wxt.dev/guide/essentials/assets.html |
| Project Structure | https://wxt.dev/guide/essentials/project-structure.html |
| Frontend Frameworks | https://wxt.dev/guide/essentials/frontend-frameworks.html |
| Configuration | https://wxt.dev/guide/essentials/configuration.html |
| Permissions | https://wxt.dev/guide/essentials/permissions.html |
| Messaging | https://wxt.dev/guide/essentials/messaging.html |
| Storage | https://wxt.dev/guide/essentials/storage.html |
| Publishing | https://wxt.dev/guide/essentials/publishing.html |
