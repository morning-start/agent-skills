# Solid 示例项目

这是一个使用 SolidJS 框架构建的完整 WXT 扩展示例。

## 官方导航链接

- [Solid 框架集成](https://wxt.dev/guide/frontend-frameworks/solid.html) - Solid 集成完整指南
- [Frontend Frameworks](https://wxt.dev/guide/essentials/frontend-frameworks.html) - 前端框架集成总览

---

## 项目结构

```
examples/solid/
├── package.json
├── tsconfig.json
├── wxt.config.ts
└── entrypoints/
    ├── background.ts
    ├── content.ts
    ├── popup.html
    ├── popup.tsx
    ├── App.tsx
    ├── options.html
    └── options.tsx
```

## 文件内容

### package.json

```json
{
  "name": "wxt-solid-example",
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
    "solid-js": "^1.8.0"
  },
  "devDependencies": {
    "solid-styled-jsx": "^0.4.0",
    "typescript": "^5.3.0",
    "vite-plugin-solid": "^2.10.0"
  }
}
```

### tsconfig.json

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
    "types": ["wxt/client-types"],
    "jsx": "preserve",
    "jsxImportSource": "solid-js"
  },
  "include": ["**/*.ts", "**/*.tsx", "wxt.config.ts"]
}
```

### wxt.config.ts

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  modules: ['@wxt-dev/module-solid'],
});
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
    button.style.backgroundColor = '#4f46e5';
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
  <script type="module" src="./popup.tsx"></script>
</body>
</html>
```

### entrypoints/popup.tsx

```typescript
import { render } from 'solid-js/web';
import App from './App';

render(() => <App />, document.getElementById('app')!);
```

### entrypoints/App.tsx

```typescript
import { createSignal } from 'solid-js';

export default function App() {
  const [count, setCount] = createSignal(0);
  const [message, setMessage] = createSignal('');
  const [timestamp, setTimestamp] = createSignal('');

  function increment() {
    setCount(c => c + 1);
  }

  function decrement() {
    setCount(c => c - 1);
  }

  async function sendMessage() {
    try {
      const response = await browser.runtime.sendMessage({
        type: 'GET_DATA',
        payload: { count: count() },
      });

      setMessage(response.data);
      setTimestamp(new Date(response.timestamp).toLocaleTimeString());
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  }

  return (
    <main>
      <h1>Solid Popup</h1>

      <div class="counter">
        <p>Count: {count()}</p>
        <div class="buttons">
          <button onClick={decrement}>-</button>
          <button onClick={increment}>+</button>
        </div>
      </div>

      <div class="message">
        <button onClick={sendMessage}>Send Message</button>
        {message() && (
          <>
            <p>Response: {message()}</p>
            <p>Timestamp: {timestamp()}</p>
          </>
        )}
      </div>

      <style jsx>{`
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
          background: #4f46e5;
          color: white;
          cursor: pointer;
          font-size: 16px;
        }

        button:hover {
          background: #4338ca;
        }

        button:active {
          background: #3730a3;
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
      `}</style>
    </main>
  );
}
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
  <script type="module" src="./options.tsx"></script>
</body>
</html>
```

### entrypoints/options.tsx

```typescript
import { render } from 'solid-js/web';
import App from './Options';

render(() => <App />, document.getElementById('app')!);
```

### entrypoints/Options.tsx

```typescript
import { createSignal, onMount } from 'solid-js';

export default function Options() {
  const [apiKey, setApiKey] = createSignal('');
  const [enabled, setEnabled] = createSignal(true);
  const [theme, setTheme] = createSignal('light');
  const [saveMessage, setSaveMessage] = createSignal('');

  onMount(async () => {
    const data = await browser.storage.sync.get(['apiKey', 'enabled', 'theme']);
    setApiKey(data.apiKey || '');
    setEnabled(data.enabled !== false);
    setTheme(data.theme || 'light');
  });

  async function saveSettings() {
    await browser.storage.sync.set({
      apiKey: apiKey(),
      enabled: enabled(),
      theme: theme(),
    });

    setSaveMessage('Settings saved successfully!');
    setTimeout(() => {
      setSaveMessage('');
    }, 2000);
  }

  return (
    <main>
      <h1>Options</h1>

      <div class="form">
        <div class="field">
          <label for="apiKey">API Key</label>
          <input
            type="text"
            id="apiKey"
            value={apiKey()}
            onInput={(e) => setApiKey(e.currentTarget.value)}
            placeholder="Enter your API key"
          />
        </div>

        <div class="field">
          <label>
            <input
              type="checkbox"
              checked={enabled()}
              onChange={(e) => setEnabled(e.currentTarget.checked)}
            />
            Enable Extension
          </label>
        </div>

        <div class="field">
          <label for="theme">Theme</label>
          <select
            id="theme"
            value={theme()}
            onChange={(e) => setTheme(e.currentTarget.value)}
          >
            <option value="light">Light</option>
            <option value="dark">Dark</option>
            <option value="auto">Auto</option>
          </select>
        </div>

        <button onClick={saveSettings}>Save Settings</button>

        {saveMessage() && <p class="success">{saveMessage()}</p>}
      </div>

      <style jsx>{`
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

        input[type='text'],
        select {
          padding: 8px 12px;
          border: 1px solid #e5e7eb;
          border-radius: 4px;
          font-size: 16px;
        }

        input[type='text']:focus,
        select:focus {
          outline: none;
          border-color: #4f46e5;
        }

        button {
          padding: 10px 20px;
          border: none;
          border-radius: 4px;
          background: #4f46e5;
          color: white;
          cursor: pointer;
          font-size: 16px;
          font-weight: 500;
        }

        button:hover {
          background: #4338ca;
        }

        button:active {
          background: #3730a3;
        }

        .success {
          color: #10b981;
          font-weight: 500;
          margin: 0;
        }
      `}</style>
    </main>
  );
}
```

## 使用说明

### 安装依赖

```bash
cd examples/solid
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

## Solid 特性

### 细粒度响应式

Solid 使用细粒度响应式系统，性能优异：

```typescript
const [count, setCount] = createSignal(0);
```

### 派生状态

```typescript
const doubled = createMemo(() => count() * 2);
```

### Store

```typescript
import { createStore } from 'solid-js/store';

const [state, setState] = createStore({
  count: 0,
  user: null,
});
```

## 扩展功能

### 添加更多组件

创建 `entrypoints/components/` 目录：

```
entrypoints/components/
├── Button.tsx
├── Input.tsx
└── Card.tsx
```

### 使用 Store

```typescript
import { createStore, produce } from 'solid-js/store';

const [state, setState] = createStore({
  count: 0,
});

function increment() {
  setState('count', c => c + 1);
}
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

- [Svelte 示例](../svelte/)
- [Vue 示例](../vue/)
- [React 示例](../react/)
- [Vanilla 示例](../vanilla/)

## 相关文档

- [框架配置](../../guides/framework-setup.md)
- [入口点 API](../../api/entrypoints.md)
- [配置 API](../../api/config.md)
- [工具函数](../../api/utilities.md)
