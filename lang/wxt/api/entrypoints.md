# 入口点 API 详解

本文档详细说明 WXT 的所有入口点 API，包括函数签名、参数说明和使用示例。

## 官方导航链接

- [Entrypoints](https://wxt.dev/guide/essentials/entrypoints.html) - 入口脚本类型配置规则
- [Content Scripts](https://wxt.dev/guide/essentials/content-scripts.html) - 内容脚本开发与注入规则

---

## 入口点概览

WXT 支持以下类型的入口点：

| 类型 | 函数 | 说明 |
|------|------|------|
| Background Script | `defineBackground` | 后台脚本，在扩展后台持续运行 |
| Content Script | `defineContentScript` | 内容脚本，注入到网页上下文中 |
| Popup | `definePopup` | 弹出页面，用户点击扩展图标时显示 |
| Options | `defineOptions` | 选项页面，扩展的设置页面 |
| DevTools | `defineDevTools` | 开发者工具页面 |
| Sidebar | `defineSidebar` | 侧边栏页面（仅 Firefox） |

## 一、Background Script

### 1.1 defineBackground

定义后台脚本入口点。

**函数签名：**

```typescript
function defineBackground(
  background: BackgroundDefinition
): BackgroundEntrypoint;

interface BackgroundDefinition {
  type?: BackgroundType;
  main?: BackgroundMain;
  persistent?: boolean;
}

type BackgroundType = 'module' | 'classic';

type BackgroundMain = () => void | (() => Promise<void>);
```

**参数说明：**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `type` | `'module' \| 'classic'` | 否 | 后台脚本类型，默认 `'module'` |
| `main` | `() => void` | 是 | 后台脚本主函数 |
| `persistent` | `boolean` | 否 | 是否持久化，默认 `false` |

**返回值：** `BackgroundEntrypoint`

**使用示例：**

```typescript
import { defineBackground } from 'wxt/sandbox';

export default defineBackground(() => {
  console.log('Background script started');

  browser.runtime.onInstalled.addListener(() => {
    console.log('Extension installed');
  });

  // 监听消息
  browser.runtime.onMessage.addListener((message, sender) => {
    console.log('Received message:', message);
    return Promise.resolve('Response from background');
  });

  // 设置警报
  browser.alarms.create('check-updates', {
    periodInMinutes: 60,
  });

  browser.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === 'check-updates') {
      console.log('Checking for updates...');
    }
  });
});
```

### 1.2 使用 TypeScript 类型

```typescript
import { defineBackground } from 'wxt/sandbox';

export default defineBackground(() => {
  // 类型安全的消息处理
  interface Message {
    type: 'GET_DATA' | 'SET_DATA';
    payload?: any;
  }

  browser.runtime.onMessage.addListener(
    (message: Message, sender) => {
      if (message.type === 'GET_DATA') {
        return Promise.resolve({ data: 'Hello' });
      }
      if (message.type === 'SET_DATA') {
        console.log('Setting data:', message.payload);
        return Promise.resolve({ success: true });
      }
    }
  );
});
```

### 1.3 使用 async/await

```typescript
import { defineBackground } from 'wxt/sandbox';

export default defineBackground(async () => {
  console.log('Background script started');

  // 等待扩展安装
  const onInstalled = new Promise<void>((resolve) => {
    browser.runtime.onInstalled.addListener(() => {
      console.log('Extension installed');
      resolve();
    });
  });

  await onInstalled;

  // 执行异步操作
  const data = await fetchData();
  console.log('Fetched data:', data);
});
```

---

## 二、Content Script

### 2.1 defineContentScript

定义内容脚本入口点。

**函数签名：**

```typescript
function defineContentScript(
  contentScript: ContentScriptDefinition
): ContentScriptEntrypoint;

interface ContentScriptDefinition {
  matches?: string[];
  excludeMatches?: string[];
  includeGlobs?: string[];
  excludeGlobs?: string[];
  css?: string[];
  js?: string[];
  runAt?: 'document_start' | 'document_end' | 'document_idle';
  allFrames?: boolean;
  matchAboutBlank?: boolean;
  matchOriginAsFallback?: boolean;
  world?: 'ISOLATED' | 'MAIN';
  main?: ContentScriptMain;
}

type ContentScriptMain = () => void | (() => Promise<void>);
```

**参数说明：**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `matches` | `string[]` | 是 | 匹配模式，如 `['<all_urls>']` |
| `excludeMatches` | `string[]` | 否 | 排除的匹配模式 |
| `includeGlobs` | `string[]` | 否 | 包含的 URL 模式 |
| `excludeGlobs` | `string[]` | 否 | 排除的 URL 模式 |
| `css` | `string[]` | 否 | 注入的 CSS 文件 |
| `js` | `string[]` | 否 | 注入的 JS 文件 |
| `runAt` | `RunAt` | 否 | 注入时机，默认 `'document_idle'` |
| `allFrames` | `boolean` | 否 | 是否注入所有框架，默认 `false` |
| `matchAboutBlank` | `boolean` | 否 | 是否匹配 about:blank，默认 `false` |
| `matchOriginAsFallback` | `boolean` | 否 | 是否匹配 origin as fallback，默认 `false` |
| `world` | `'ISOLATED' \| 'MAIN'` | 否 | 执行环境，默认 `'ISOLATED'` |
| `main` | `() => void` | 是 | 内容脚本主函数 |

**返回值：** `ContentScriptEntrypoint`

**使用示例：**

```typescript
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],
  runAt: 'document_idle',
  main() {
    console.log('Content script injected');

    // 操作 DOM
    const body = document.body;
    if (body) {
      body.style.backgroundColor = '#f0f0f0';
    }

    // 监听 DOM 变化
    const observer = new MutationObserver((mutations) => {
      console.log('DOM changed:', mutations);
    });

    observer.observe(document.body!, {
      childList: true,
      subtree: true,
    });

    // 监听来自后台脚本的消息
    browser.runtime.onMessage.addListener((message) => {
      console.log('Received message:', message);
      return Promise.resolve('Response from content');
    });
  },
});
```

### 2.2 匹配特定网站

```typescript
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  // 仅匹配特定网站
  matches: [
    'https://www.google.com/*',
    'https://github.com/*',
  ],

  // 排除某些页面
  excludeMatches: [
    'https://www.google.com/search*',
  ],

  main() {
    console.log('Content script injected to Google or GitHub');
  },
});
```

### 2.3 注入 CSS 和 JS

```typescript
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],

  // 注入 CSS 文件
  css: ['./content.css'],

  // 注入 JS 文件
  js: ['./content.js'],

  main() {
    console.log('Content script with CSS and JS');
  },
});
```

### 2.4 在所有框架中注入

```typescript
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],
  allFrames: true, // 注入所有框架，包括 iframe
  main() {
    console.log('Content script injected to all frames');
    console.log('Frame ID:', window.frameId);
  },
});
```

### 2.5 在 MAIN world 中执行

```typescript
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],
  world: 'MAIN', // 在 MAIN world 中执行，可以访问页面 JS
  main() {
    console.log('Content script running in MAIN world');
    console.log('Can access page JS:', window.somePageFunction);
  },
});
```

---

## 三、Popup

### 3.1 定义 Popup

Popup 由两个文件组成：HTML 文件和逻辑文件。

**HTML 文件（popup.html）：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Popup</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="./popup.ts"></script>
</body>
</html>
```

**逻辑文件（popup.ts）：**

```typescript
import { definePopup } from 'wxt/sandbox';

export default definePopup(() => {
  console.log('Popup loaded');

  // 获取 DOM 元素
  const button = document.getElementById('my-button')!;

  button.addEventListener('click', () => {
    console.log('Button clicked');

    // 发送消息到后台脚本
    browser.runtime.sendMessage({
      type: 'POPUP_ACTION',
    });
  });

  // 从后台脚本获取数据
  browser.runtime.sendMessage({ type: 'GET_DATA' }).then((response) => {
    console.log('Received data:', response);
  });
});
```

**使用 Svelte：**

```html
<!-- popup.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Popup</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="./popup.ts"></script>
</body>
</html>
```

```typescript
// popup.ts
import App from './App.svelte';

const app = new App({
  target: document.getElementById('app')!,
});

export default app;
```

```svelte
<!-- App.svelte -->
<script lang="ts">
  let count = 0;

  function increment() {
    count += 1;
    browser.runtime.sendMessage({ type: 'INCREMENT', count });
  }
</script>

<main>
  <h1>Popup</h1>
  <p>Count: {count}</p>
  <button on:click={increment}>Increment</button>
</main>
```

### 3.2 Popup 配置

在 `wxt.config.ts` 中配置 Popup：

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    action: {
      default_popup: 'popup.html',
      default_title: 'My Extension',
      default_icon: {
        16: 'icons/icon-16.png',
        32: 'icons/icon-32.png',
        48: 'icons/icon-48.png',
        128: 'icons/icon-128.png',
      },
    },
  },
});
```

---

## 四、Options

### 4.1 定义 Options

Options 与 Popup 类似，由 HTML 文件和逻辑文件组成。

**HTML 文件（options.html）：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Options</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="./options.ts"></script>
</body>
</html>
```

**逻辑文件（options.ts）：**

```typescript
import { defineOptions } from 'wxt/sandbox';

export default defineOptions(() => {
  console.log('Options loaded');

  // 保存设置
  function saveSettings() {
    const settings = {
      enabled: true,
      apiKey: 'your-api-key',
    };

    browser.storage.sync.set(settings);
  }

  // 加载设置
  browser.storage.sync.get().then((settings) => {
    console.log('Loaded settings:', settings);
  });
});
```

### 4.2 Options 配置

在 `wxt.config.ts` 中配置 Options：

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    options_page: 'options.html',
  },
});
```

---

## 五、DevTools

### 5.1 定义 DevTools

DevTools 由三个文件组成：DevTools 页面、Panel 页面和后台脚本。

**DevTools 页面（devtools.ts）：**

```typescript
import { defineDevTools } from 'wxt/sandbox';

export default defineDevTools(() => {
  console.log('DevTools panel created');

  // 创建 DevTools 面板
  browser.devtools.panels.create(
    'My Panel',
    'icons/icon-16.png',
    'devtools-panel.html'
  );
});
```

**Panel 页面（devtools-panel.html）：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>DevTools Panel</title>
</head>
<body>
  <h1>DevTools Panel</h1>
  <script type="module" src="./devtools-panel.ts"></script>
</body>
</html>
```

**Panel 逻辑（devtools-panel.ts）：**

```typescript
console.log('DevTools panel loaded');

// 获取当前标签页
browser.devtools.inspectedWindow.eval(
  'document.title',
  (result, isException) => {
    if (!isException) {
      console.log('Page title:', result);
    }
  }
);
```

### 5.2 DevTools 配置

在 `wxt.config.ts` 中配置 DevTools：

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    devtools_page: 'devtools.html',
  },
});
```

---

## 六、Sidebar

### 6.1 定义 Sidebar

Sidebar 仅在 Firefox 中支持。

**HTML 文件（sidebar.html）：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Sidebar</title>
</head>
<body>
  <h1>Sidebar</h1>
  <script type="module" src="./sidebar.ts"></script>
</body>
</html>
```

**逻辑文件（sidebar.ts）：**

```typescript
import { defineSidebar } from 'wxt/sandbox';

export default defineSidebar(() => {
  console.log('Sidebar loaded');

  // 显示侧边栏
  browser.sidebarAction.open();
});
```

### 6.2 Sidebar 配置

在 `wxt.config.ts` 中配置 Sidebar：

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    sidebar_action: {
      default_panel: 'sidebar.html',
      default_title: 'My Sidebar',
      default_icon: {
        16: 'icons/icon-16.png',
        32: 'icons/icon-32.png',
        48: 'icons/icon-48.png',
        128: 'icons/icon-128.png',
      },
    },
  },
});
```

---

## 七、消息传递

### 7.1 Background ↔ Content

**Content Script 发送消息：**

```typescript
browser.runtime.sendMessage({
  type: 'GET_DATA',
}).then((response) => {
  console.log('Response:', response);
});
```

**Background Script 接收消息：**

```typescript
browser.runtime.onMessage.addListener((message, sender) => {
  if (message.type === 'GET_DATA') {
    return Promise.resolve({ data: 'Hello' });
  }
});
```

### 7.2 Content ↔ Popup

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

### 7.3 跨上下文通信

使用 `browser.storage` 进行跨上下文通信：

```typescript
// 写入存储
browser.storage.local.set({
  key: 'value',
});

// 读取存储
browser.storage.local.get(['key']).then((data) => {
  console.log('Read from storage:', data.key);
});

// 监听存储变化
browser.storage.onChanged.addListener((changes, areaName) => {
  console.log('Storage changed:', changes);
});
```

---

## 八、存储 API

### 8.1 使用存储

```typescript
// 写入存储
browser.storage.sync.set({
  apiKey: 'your-api-key',
  enabled: true,
});

browser.storage.local.set({
  cache: 'data',
});

// 读取存储
browser.storage.sync.get(['apiKey', 'enabled']).then((data) => {
  console.log('API Key:', data.apiKey);
  console.log('Enabled:', data.enabled);
});

// 清除存储
browser.storage.sync.clear();

// 移除特定键
browser.storage.sync.remove(['apiKey']);
```

### 8.2 监听存储变化

```typescript
browser.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === 'sync') {
    console.log('Sync storage changed:', changes);
  }
  if (areaName === 'local') {
    console.log('Local storage changed:', changes);
  }
});
```

---

## 九、常见问题

### Q1: 如何在 Content Script 中访问页面变量？

**方法一：注入脚本到 MAIN world：**

```typescript
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],
  world: 'MAIN',
  main() {
    console.log('Can access page variables:', window.somePageVar);
  },
});
```

**方法二：使用 script 标签注入：**

```typescript
const script = document.createElement('script');
script.textContent = `
  window.someExtensionVar = 'Extension data';
`;
(document.head || document.documentElement).appendChild(script);
script.remove();
```

### Q2: 如何调试 Background Script？

**方法一：查看扩展页面：**

1. 打开 `chrome://extensions` 或 `about:debugging#/runtime/this-firefox`
2. 找到扩展
3. 点击 "Inspect views: background page"
4. 打开开发者工具

**方法二：使用 console.log：**

```typescript
export default defineBackground(() => {
  console.log('Background script started');

  // 所有 console.log 会显示在背景页控制台中
});
```

### Q3: 如何调试 Content Script？

**方法一：查看页面控制台：**

1. 打开匹配 Content Script 的网页
2. 打开开发者工具（F12）
3. 查看 Console 标签

**方法二：在 Sources 标签中查看：**

1. 打开开发者工具
2. 查看 Sources 标签
3. 找到 Content Scripts 文件夹

### Q4: 如何在 Popup 和 Background 之间传递数据？

**Popup 发送消息：**

```typescript
browser.runtime.sendMessage({
  type: 'GET_DATA',
}).then((response) => {
  console.log('Response:', response);
});
```

**Background 接收消息：**

```typescript
browser.runtime.onMessage.addListener((message) => {
  if (message.type === 'GET_DATA') {
    return Promise.resolve({ data: 'Hello' });
  }
});
```

### Q5: 如何在多个 Content Script 之间传递数据？

**方法一：使用 Storage：**

```typescript
// Content Script A 写入
browser.storage.local.set({
  sharedData: 'Hello from A',
});

// Content Script B 读取
browser.storage.local.get(['sharedData']).then((data) => {
  console.log('Received:', data.sharedData);
});
```

**方法二：使用消息传递：**

```typescript
// Content Script A 发送
browser.runtime.sendMessage({
  type: 'FROM_CONTENT_A',
  data: 'Hello from A',
});

// Content Script B 接收
browser.runtime.onMessage.addListener((message, sender) => {
  if (message.type === 'FROM_CONTENT_A') {
    console.log('Received:', message.data);
  }
});
```

---

## 十、最佳实践

### 10.1 模块化代码

```typescript
// utils.ts
export function fetchData() {
  return fetch('https://api.example.com/data').then((res) =>
    res.json()
  );
}

export function saveData(data: any) {
  return browser.storage.local.set(data);
}
```

```typescript
// background.ts
import { defineBackground } from 'wxt/sandbox';
import { fetchData, saveData } from './utils';

export default defineBackground(async () => {
  const data = await fetchData();
  await saveData(data);
  console.log('Data saved:', data);
});
```

### 10.2 使用 TypeScript 类型

```typescript
// types.ts
export interface ExtensionMessage {
  type: string;
  payload?: any;
}

export interface ExtensionData {
  apiKey: string;
  enabled: boolean;
}
```

```typescript
// background.ts
import { defineBackground } from 'wxt/sandbox';
import type { ExtensionMessage } from './types';

export default defineBackground(() => {
  browser.runtime.onMessage.addListener(
    (message: ExtensionMessage, sender) => {
      console.log('Received message:', message);
      return Promise.resolve({ success: true });
    }
  );
});
```

### 10.3 错误处理

```typescript
import { defineBackground } from 'wxt/sandbox';

export default defineBackground(() => {
  browser.runtime.onMessage.addListener(async (message, sender) => {
    try {
      const response = await handleMessage(message);
      return response;
    } catch (error) {
      console.error('Error handling message:', error);
      return { error: true, message: error.message };
    }
  });
});
```

## 下一步

- [配置 API](./config.md)：学习 WXT 配置 API
- [工具函数](./utilities.md)：学习存储、脚本注入等工具函数
- [构建阶段](../lifecycle/phases.md)：了解构建流程
- [示例代码](../examples/)：查看完整项目示例
