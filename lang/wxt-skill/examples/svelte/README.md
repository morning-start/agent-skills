# Svelte 示例项目

这是一个使用 Svelte 框架构建的完整 WXT 扩展示例。

## 官方导航链接

- [Svelte 框架集成](https://wxt.dev/guide/frontend-frameworks/svelte.html) - Svelte 集成完整指南
- [Frontend Frameworks](https://wxt.dev/guide/essentials/frontend-frameworks.html) - 前端框架集成总览

---

## 项目结构

```
examples/svelte/
├── package.json
├── tsconfig.json
├── wxt.config.ts
├── svelte.config.js
└── entrypoints/
    ├── background.ts
    ├── content.ts
    ├── popup.html
    ├── popup.ts
    ├── App.svelte
    ├── options.html
    └── options.ts
```

## 文件内容

### package.json

```json
{
  "name": "wxt-svelte-example",
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
  "dependencies": {
    "wxt": "^0.17.0",
    "svelte": "^4.0.0"
  },
  "devDependencies": {
    "@sveltejs/vite-plugin-svelte": "^3.0.0",
    "@tsconfig/svelte": "^5.0.0",
    "svelte-preprocess": "^5.0.0",
    "typescript": "^5.3.0"
  }
}
```

### tsconfig.json

```json
{
  "extends": "@tsconfig/svelte/tsconfig.json",
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
  "include": ["**/*.ts", "**/*.svelte", "wxt.config.ts"]
}
```

### wxt.config.ts

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  modules: ['@wxt-dev/module-svelte'],
});
```

### svelte.config.js

```javascript
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

export default {
  preprocess: vitePreprocess(),
};
```

### entrypoints/background.ts

```typescript
import { defineBackground } from 'wxt/sandbox';

export default defineBackground(() => {
  console.log('Background script started');

  browser.runtime.onInstalled.addListener(() => {
    console.log('Extension installed');
  });

  browser.runtime.onMessage.addListener((message, sender) => {
    console.log('Received message:', message);
    return Promise.resolve({
      data: 'Hello from background',
      timestamp: Date.now(),
    });
  });

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

### entrypoints/content.ts

```typescript
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],
  runAt: 'document_idle',
  main() {
    console.log('Content script injected');

    const button = document.createElement('button');
    button.textContent = 'Click me';
    button.style.position = 'fixed';
    button.style.top = '10px';
    button.style.right = '10px';
    button.style.zIndex = '9999';
    button.style.padding = '10px 20px';
    button.style.backgroundColor = '#3b82f6';
    button.style.color = 'white';
    button.style.border = 'none';
    button.style.borderRadius = '4px';
    button.style.cursor = 'pointer';

    button.addEventListener('click', () => {
      browser.runtime.sendMessage({
        type: 'CONTENT_CLICK',
        url: window.location.href,
      });
    });

    document.body.appendChild(button);

    browser.runtime.onMessage.addListener((message, sender) => {
      if (message.type === 'FROM_BACKGROUND') {
        console.log('Received from background:', message.data);
        return Promise.resolve({ status: 'OK' });
      }
    });
  },
});
```

### entrypoints/popup.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Popup</title>
  <style>
    body {
      width: 300px;
      padding: 16px;
      font-family: system-ui, -apple-system, sans-serif;
      margin: 0;
    }
  </style>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="./popup.ts"></script>
</body>
</html>
```

### entrypoints/popup.ts

```typescript
import App from './App.svelte';

const app = new App({
  target: document.getElementById('app')!,
});

export default app;
```

### entrypoints/App.svelte

```svelte
<script lang="ts">
  let count = 0;
  let message = '';
  let timestamp = '';

  function increment() {
    count += 1;
  }

  function decrement() {
    count -= 1;
  }

  async function sendMessage() {
    try {
      const response = await browser.runtime.sendMessage({
        type: 'GET_DATA',
        payload: { count },
      });

      message = response.data;
      timestamp = new Date(response.timestamp).toLocaleTimeString();
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  }
</script>

<main>
  <h1>Svelte Popup</h1>

  <div class="counter">
    <p>Count: {count}</p>
    <div class="buttons">
      <button on:click={decrement}>-</button>
      <button on:click={increment}>+</button>
    </div>
  </div>

  <div class="message">
    <button on:click={sendMessage}>Send Message</button>
    {#if message}
      <p>Response: {message}</p>
      <p>Timestamp: {timestamp}</p>
    {/if}
  </div>
</main>

<style>
  main {
    font-family: system-ui, -apple-system, sans-serif;
  }

  h1 {
    margin: 0 0 16px 0;
    font-size: 24px;
    text-align: center;
  }

  .counter {
    margin-bottom: 16px;
    text-align: center;
  }

  .counter p {
    margin: 0 0 8px 0;
    font-size: 18px;
  }

  .buttons {
    display: flex;
    gap: 8px;
    justify-content: center;
  }

  button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    background: #3b82f6;
    color: white;
    cursor: pointer;
    font-size: 16px;
  }

  button:hover {
    background: #2563eb;
  }

  button:active {
    background: #1d4ed8;
  }

  .message {
    margin-top: 16px;
    text-align: center;
  }

  .message button {
    margin-bottom: 8px;
  }

  .message p {
    margin: 4px 0;
    font-size: 14px;
  }
</style>
```

### entrypoints/options.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Options</title>
  <style>
    body {
      width: 600px;
      padding: 24px;
      font-family: system-ui, -apple-system, sans-serif;
      margin: 0;
    }
  </style>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="./options.ts"></script>
</body>
</html>
```

### entrypoints/options.ts

```typescript
import App from './Options.svelte';

const app = new App({
  target: document.getElementById('app')!,
});

export default app;
```

### entrypoints/Options.svelte

```svelte
<script lang="ts">
  let apiKey = '';
  let enabled = true;
  let theme = 'light';
  let saveMessage = '';

  async function loadSettings() {
    const data = await browser.storage.sync.get(['apiKey', 'enabled', 'theme']);
    apiKey = data.apiKey || '';
    enabled = data.enabled !== false;
    theme = data.theme || 'light';
  }

  async function saveSettings() {
    await browser.storage.sync.set({
      apiKey,
      enabled,
      theme,
    });

    saveMessage = 'Settings saved successfully!';
    setTimeout(() => {
      saveMessage = '';
    }, 2000);
  }

  loadSettings();
</script>

<main>
  <h1>Options</h1>

  <div class="form">
    <div class="field">
      <label for="apiKey">API Key</label>
      <input
        type="text"
        id="apiKey"
        bind:value={apiKey}
        placeholder="Enter your API key"
      />
    </div>

    <div class="field">
      <label>
        <input type="checkbox" bind:checked={enabled} />
        Enable Extension
      </label>
    </div>

    <div class="field">
      <label for="theme">Theme</label>
      <select id="theme" bind:value={theme}>
        <option value="light">Light</option>
        <option value="dark">Dark</option>
        <option value="auto">Auto</option>
      </select>
    </div>

    <button on:click={saveSettings}>Save Settings</button>

    {#if saveMessage}
      <p class="success">{saveMessage}</p>
    {/if}
  </div>
</main>

<style>
  h1 {
    margin: 0 0 24px 0;
    font-size: 32px;
  }

  .form {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  label {
    font-weight: 500;
    font-size: 14px;
  }

  input[type="text"],
  select {
    padding: 8px 12px;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
    font-size: 16px;
  }

  input[type="text"]:focus,
  select:focus {
    outline: none;
    border-color: #3b82f6;
  }

  button {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    background: #3b82f6;
    color: white;
    cursor: pointer;
    font-size: 16px;
    font-weight: 500;
  }

  button:hover {
    background: #2563eb;
  }

  button:active {
    background: #1d4ed8;
  }

  .success {
    color: #10b981;
    font-weight: 500;
    margin: 0;
  }
</style>
```

## 使用说明

### 安装依赖

```bash
cd examples/svelte
bun install
```

### 开发模式

```bash
# Chrome
bun run dev

# Firefox
bun run dev:firefox
```

### 构建生产版本

```bash
# Chrome
bun run build

# Firefox
bun run build:firefox
```

### 打包扩展

```bash
# Chrome
bun run zip

# Firefox
bun run zip:firefox
```

## 功能说明

- **Background Script**: 后台服务，处理消息和警报
- **Content Script**: 注入到所有网页，添加交互按钮
- **Popup**: 弹出页面，计数器和消息传递
- **Options**: 选项页面，保存设置

## 扩展功能

### 添加更多组件

创建 `entrypoints/components/` 目录：

```
entrypoints/components/
├── Button.svelte
├── Input.svelte
└── Card.svelte
```

### 使用 Store

创建 `entrypoints/store.ts`：

```typescript
import { writable } from 'svelte/store';

export const count = writable(0);
```

在组件中使用：

```svelte
<script>
  import { count } from './store';
</script>

<p>Count: {$count}</p>
```

### 添加类型

创建 `entrypoints/types.ts`：

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

## 更多示例

- [Vue 示例](../vue/)
- [React 示例](../react/)
- [Solid 示例](../solid/)
- [Vanilla 示例](../vanilla/)

## 相关文档

- [框架配置](../../guides/framework-setup.md)
- [入口点 API](../../api/entrypoints.md)
- [配置 API](../../api/config.md)
- [工具函数](../../api/utilities.md)
