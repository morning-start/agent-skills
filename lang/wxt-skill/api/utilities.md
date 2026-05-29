# 工具函数详解

本文档详细说明 WXT 的所有工具函数，包括存储、脚本注入、匹配模式等。

## 官方导航链接

- [Storage](https://wxt.dev/guide/essentials/storage.html) - 数据存储方案
- [Messaging](https://wxt.dev/guide/essentials/messaging.html) - 扩展内脚本间通信方法
- [I18n](https://wxt.dev/guide/essentials/i18n.html) - 国际化与本地化配置
- [Scripting](https://wxt.dev/guide/essentials/scripting.html) - 动态脚本注入与执行
- [ES Modules](https://wxt.dev/guide/essentials/es-modules.html) - ES 模块在扩展中的使用
- [Extension APIs](https://wxt.dev/guide/essentials/extension-apis.html) - 浏览器扩展 API 调用与适配

---

## 工具函数概览

WXT 提供以下工具函数：

| 分类 | 函数 | 说明 |
|------|------|------|
| 存储 | `storage` | 存储和读取数据 |
| 脚本注入 | `injectScript` | 注入脚本到页面 |
| 匹配模式 | `matchPattern` | 匹配 URL 模式 |
| 消息传递 | `sendMessage` | 发送消息 |
| 浏览器 API | `browser` | 浏览器 API |

---

## 一、存储工具

### 1.1 使用 browser.storage

WXT 提供完整的浏览器存储 API 支持。

#### 写入数据

```typescript
// 写入到 sync storage（跨设备同步）
await browser.storage.sync.set({
  apiKey: 'your-api-key',
  enabled: true,
  settings: {
    theme: 'dark',
    language: 'en',
  },
});

// 写入到 local storage（本地存储）
await browser.storage.local.set({
  cache: 'data',
  timestamp: Date.now(),
});

// 写入到 session storage（会话存储）
await browser.storage.session.set({
  sessionId: '12345',
});
```

#### 读取数据

```typescript
// 读取特定键
const data1 = await browser.storage.sync.get(['apiKey', 'enabled']);
console.log('API Key:', data1.apiKey);
console.log('Enabled:', data1.enabled);

// 读取所有数据
const data2 = await browser.storage.sync.get(null);
console.log('All data:', data2);

// 读取默认值
const data3 = await browser.storage.sync.get({
  apiKey: 'default-api-key',
  enabled: true,
});
console.log('API Key:', data3.apiKey);
console.log('Enabled:', data3.enabled);
```

#### 删除数据

```typescript
// 删除特定键
await browser.storage.sync.remove(['apiKey', 'enabled']);

// 清除所有数据
await browser.storage.sync.clear();
```

#### 监听存储变化

```typescript
browser.storage.onChanged.addListener((changes, areaName) => {
  console.log('Storage changed:', areaName, changes);

  for (const [key, { oldValue, newValue }] of Object.entries(changes)) {
    console.log(`${key} changed from ${oldValue} to ${newValue}`);
  }
});
```

### 1.2 封装存储工具

**创建存储工具类：**

```typescript
// utils/storage.ts

export class StorageHelper {
  private area: 'sync' | 'local' | 'session';

  constructor(area: 'sync' | 'local' | 'session' = 'sync') {
    this.area = area;
  }

  async get<T>(keys: string | string[] | null | object): Promise<T> {
    return await browser.storage[this.area].get(keys);
  }

  async set(data: object): Promise<void> {
    await browser.storage[this.area].set(data);
  }

  async remove(keys: string | string[]): Promise<void> {
    await browser.storage[this.area].remove(keys);
  }

  async clear(): Promise<void> {
    await browser.storage[this.area].clear();
  }

  onChanged(
    callback: (
      changes: Record<string, chrome.storage.StorageChange>,
      areaName: string
    ) => void
  ): void {
    browser.storage.onChanged.addListener((changes, areaName) => {
      if (areaName === this.area) {
        callback(changes, areaName);
      }
    });
  }
}

// 使用示例
const syncStorage = new StorageHelper('sync');
const localStorage = new StorageHelper('local');
```

**使用存储工具：**

```typescript
// background.ts
import { defineBackground } from 'wxt/sandbox';
import { StorageHelper } from './utils/storage';

export default defineBackground(() => {
  const storage = new StorageHelper('sync');

  // 保存设置
  storage.set({
    apiKey: 'your-api-key',
    enabled: true,
  });

  // 读取设置
  storage.get(['apiKey', 'enabled']).then((data) => {
    console.log('API Key:', data.apiKey);
    console.log('Enabled:', data.enabled);
  });

  // 监听变化
  storage.onChanged((changes, areaName) => {
    console.log('Storage changed:', changes);
  });
});
```

---

## 二、脚本注入工具

### 2.1 注入脚本到页面

**方法一：使用 content script 的 world 参数：**

```typescript
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],
  world: 'MAIN',
  main() {
    console.log('Running in MAIN world');
    console.log('Can access page variables:', window.somePageVar);
  },
});
```

**方法二：动态注入脚本：**

```typescript
import { defineContentScript } from 'wxt/sandbox';

function injectScript(code: string) {
  const script = document.createElement('script');
  script.textContent = code;
  (document.head || document.documentElement).appendChild(script);
  script.remove();
}

export default defineContentScript({
  matches: ['<all_urls>'],
  main() {
    // 注入脚本到 MAIN world
    injectScript(`
      window.extensionData = 'Hello from extension';
      console.log('Extension data:', window.extensionData);
    `);

    // 验证注入成功
    setTimeout(() => {
      console.log('Injected data:', window.extensionData);
    }, 100);
  },
});
```

**方法三：注入外部脚本：**

```typescript
import { defineContentScript } from 'wxt/sandbox';

function injectExternalScript(url: string) {
  const script = document.createElement('script');
  script.src = url;
  script.onload = () => {
    console.log('External script loaded:', url);
  };
  (document.head || document.documentElement).appendChild(script);
}

export default defineContentScript({
  matches: ['<all_urls>'],
  main() {
    injectExternalScript('https://example.com/script.js');
  },
});
```

### 2.2 注入 CSS

```typescript
import { defineContentScript } from 'wxt/sandbox';

function injectCSS(code: string) {
  const style = document.createElement('style');
  style.textContent = code;
  (document.head || document.documentElement).appendChild(style);
}

export default defineContentScript({
  matches: ['<all_urls>'],
  main() {
    injectCSS(`
      body {
        background-color: #f0f0f0 !important;
      }

      .extension-highlight {
        border: 2px solid red;
      }
    `);
  },
});
```

### 2.3 封装注入工具

```typescript
// utils/inject.ts

export function injectScript(code: string) {
  const script = document.createElement('script');
  script.textContent = code;
  (document.head || document.documentElement).appendChild(script);
  script.remove();
}

export function injectExternalScript(url: string) {
  return new Promise<void>((resolve, reject) => {
    const script = document.createElement('script');
    script.src = url;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error(`Failed to load script: ${url}`));
    (document.head || document.documentElement).appendChild(script);
  });
}

export function injectCSS(code: string) {
  const style = document.createElement('style');
  style.textContent = code;
  (document.head || document.documentElement).appendChild(style);
}

export function injectExternalCSS(url: string) {
  return new Promise<void>((resolve, reject) => {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = url;
    link.onload = () => resolve();
    link.onerror = () => reject(new Error(`Failed to load CSS: ${url}`));
    (document.head || document.documentElement).appendChild(link);
  });
}
```

---

## 三、匹配模式工具

### 3.1 匹配 URL 模式

**基本匹配：**

```typescript
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  // 匹配所有 URL
  matches: ['<all_urls>'],

  // 匹配特定域名
  // matches: ['https://www.google.com/*'],

  // 匹配多个域名
  // matches: ['https://www.google.com/*', 'https://github.com/*'],

  // 匹配特定路径
  // matches: ['https://example.com/path/*'],

  // 匹配特定文件
  // matches: ['https://example.com/file.html'],

  main() {
    console.log('Content script injected');
  },
});
```

**匹配模式语法：**

| 模式 | 说明 | 示例 |
|------|------|------|
| `*` | 匹配任意长度字符串 | `https://*/*` |
| `?` | 匹配单个字符 | `https://example.com/file?.html` |
| `*://*/*` | 匹配所有协议 | `*://*/*` |
| `<all_urls>` | 匹配所有 URL | `<all_urls>` |

**匹配模式示例：**

```typescript
// 匹配所有 HTTP 和 HTTPS URL
matches: ['<all_urls>']

// 匹配所有 HTTPS URL
matches: ['https://*/*']

// 匹配特定域名
matches: ['https://www.google.com/*']

// 匹配多个域名
matches: [
  'https://www.google.com/*',
  'https://github.com/*',
  'https://stackoverflow.com/*',
]

// 匹配特定路径
matches: ['https://example.com/docs/*']

// 匹配特定文件
matches: ['https://example.com/index.html']

// 匹配所有子域名
matches: ['https://*.example.com/*']
```

### 3.2 排除模式

```typescript
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  // 匹配所有 URL
  matches: ['<all_urls>'],

  // 排除特定 URL
  excludeMatches: [
    'https://www.google.com/search*',
    'https://example.com/admin/*',
  ],

  main() {
    console.log('Content script injected (excluding some URLs)');
  },
});
```

### 3.3 Glob 模式

```typescript
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  // 匹配所有 URL
  matches: ['<all_urls>'],

  // 包含特定 Glob 模式
  includeGlobs: [
    '*://*.example.com/*',
    '*://example.com/*.pdf',
  ],

  // 排除特定 Glob 模式
  excludeGlobs: [
    '*://*.example.com/admin/*',
    '*://example.com/*/*.pdf',
  ],

  main() {
    console.log('Content script injected (with glob patterns)');
  },
});
```

### 3.4 封装匹配工具

```typescript
// utils/match.ts

export function matchUrl(url: string, patterns: string[]): boolean {
  return patterns.some(pattern => {
    if (pattern === '<all_urls>') return true;

    const regex = patternToRegex(pattern);
    return regex.test(url);
  });
}

function patternToRegex(pattern: string): RegExp {
  // 转换匹配模式为正则表达式
  let regex = pattern
    .replace(/[.+?^${}()|[\]\\]/g, '\\$&')
    .replace(/\*/g, '.*')
    .replace(/\?/g, '.');

  return new RegExp(`^${regex}$`);
}

// 使用示例
const isMatched = matchUrl('https://example.com/page', [
  'https://example.com/*',
]);
console.log('Matched:', isMatched);
```

---

## 四、消息传递工具

### 4.1 发送消息

**发送消息到 Background：**

```typescript
// content.ts
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],
  main() {
    // 发送消息到后台脚本
    browser.runtime.sendMessage({
      type: 'GET_DATA',
      payload: { id: 123 },
    }).then((response) => {
      console.log('Response:', response);
    });
  },
});
```

**发送消息到 Content Script：**

```typescript
// background.ts
import { defineBackground } from 'wxt/sandbox';

export default defineBackground(() => {
  // 获取当前标签页
  browser.tabs.query({ active: true, currentWindow: true }).then((tabs) => {
    const tabId = tabs[0].id;

    // 发送消息到内容脚本
    browser.tabs.sendMessage(tabId, {
      type: 'FROM_BACKGROUND',
      data: 'Hello from background',
    }).then((response) => {
      console.log('Response:', response);
    });
  });
});
```

**发送消息到 Popup：**

```typescript
// popup.ts
browser.runtime.sendMessage({
  type: 'POPUP_ACTION',
  payload: { action: 'click' },
});
```

### 4.2 接收消息

**Background 接收消息：**

```typescript
// background.ts
import { defineBackground } from 'wxt/sandbox';

export default defineBackground(() => {
  browser.runtime.onMessage.addListener((message, sender) => {
    console.log('Received message:', message);
    console.log('Sender:', sender);

    // 处理不同类型的消息
    if (message.type === 'GET_DATA') {
      return Promise.resolve({
        data: 'Hello from background',
        timestamp: Date.now(),
      });
    }

    if (message.type === 'SET_DATA') {
      console.log('Setting data:', message.payload);
      return Promise.resolve({ success: true });
    }
  });
});
```

**Content Script 接收消息：**

```typescript
// content.ts
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],
  main() {
    browser.runtime.onMessage.addListener((message, sender) => {
      console.log('Received message:', message);
      console.log('Sender:', sender);

      if (message.type === 'FROM_BACKGROUND') {
        console.log('Data:', message.data);
        return Promise.resolve({ status: 'OK' });
      }
    });
  },
});
```

### 4.3 封装消息工具

```typescript
// utils/message.ts

export interface Message<T = any> {
  type: string;
  payload?: T;
}

export interface Response<T = any> {
  data?: T;
  error?: boolean;
  message?: string;
}

export async function sendMessage<T = any>(
  message: Message
): Promise<Response<T>> {
  return await browser.runtime.sendMessage(message);
}

export async function sendMessageToTab<T = any>(
  tabId: number,
  message: Message
): Promise<Response<T>> {
  return await browser.tabs.sendMessage(tabId, message);
}

export function onMessage<T = any>(
  callback: (message: Message<T>, sender: chrome.runtime.MessageSender) => Promise<Response>
): void {
  browser.runtime.onMessage.addListener(callback);
}
```

---

## 五、浏览器 API 工具

### 5.1 标签页操作

```typescript
// 获取当前标签页
const tabs = await browser.tabs.query({ active: true, currentWindow: true });
const currentTab = tabs[0];

// 创建新标签页
const newTab = await browser.tabs.create({
  url: 'https://example.com',
});

// 更新标签页
await browser.tabs.update(currentTab.id, {
  url: 'https://example.com/new-page',
});

// 关闭标签页
await browser.tabs.remove(currentTab.id);

// 获取所有标签页
const allTabs = await browser.tabs.query({});

// 监听标签页更新
browser.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  console.log('Tab updated:', tabId, changeInfo);
});
```

### 5.2 窗口操作

```typescript
// 获取当前窗口
const window = await browser.windows.getCurrent();

// 创建新窗口
const newWindow = await browser.windows.create({
  url: 'https://example.com',
  width: 800,
  height: 600,
});

// 更新窗口
await browser.windows.update(newWindow.id, {
  width: 1024,
  height: 768,
});

// 关闭窗口
await browser.windows.remove(newWindow.id);
```

### 5.3 通知操作

```typescript
// 创建通知
await browser.notifications.create('notification-id', {
  type: 'basic',
  iconUrl: 'icons/icon-48.png',
  title: 'Notification Title',
  message: 'Notification message',
});

// 监听通知点击
browser.notifications.onClicked.addListener((notificationId) => {
  console.log('Notification clicked:', notificationId);
});
```

### 5.4 下载操作

```typescript
// 开始下载
const downloadId = await browser.downloads.download({
  url: 'https://example.com/file.pdf',
  filename: 'file.pdf',
  saveAs: true,
});

// 监听下载完成
browser.downloads.onChanged.addListener((downloadDelta) => {
  if (downloadDelta.state && downloadDelta.state.current === 'complete') {
    console.log('Download complete:', downloadDelta.id);
  }
});
```

### 5.5 警报操作

```typescript
// 创建警报
await browser.alarms.create('alarm-name', {
  delayInMinutes: 10,
  periodInMinutes: 60,
});

// 监听警报
browser.alarms.onAlarm.addListener((alarm) => {
  console.log('Alarm triggered:', alarm.name);

  if (alarm.name === 'alarm-name') {
    // 执行任务
  }
});

// 清除警报
await browser.alarms.clear('alarm-name');
```

---

## 六、常见问题

### Q1: 如何在 Content Script 中访问页面变量？

**使用 world: 'MAIN'：**

```typescript
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],
  world: 'MAIN',
  main() {
    console.log('Page variables:', window.somePageVar);
  },
});
```

### Q2: 如何在多个 Content Script 之间传递数据？

**使用 Storage：**

```typescript
// Content Script A
browser.storage.local.set({
  sharedData: 'Hello from A',
});

// Content Script B
browser.storage.local.get(['sharedData']).then((data) => {
  console.log('Received:', data.sharedData);
});
```

### Q3: 如何处理消息传递错误？

**使用 try-catch：**

```typescript
try {
  const response = await browser.runtime.sendMessage({
    type: 'GET_DATA',
  });
  console.log('Response:', response);
} catch (error) {
  console.error('Failed to send message:', error);
}
```

### Q4: 如何监听所有存储变化？

```typescript
browser.storage.onChanged.addListener((changes, areaName) => {
  console.log('Storage changed:', areaName);
  console.log('Changes:', changes);
});
```

### Q5: 如何动态注入脚本？

**使用动态注入：**

```typescript
function injectScript(code: string) {
  const script = document.createElement('script');
  script.textContent = code;
  (document.head || document.documentElement).appendChild(script);
  script.remove();
}

injectScript(`
  console.log('Injected script executed');
`);
```

---

## 七、最佳实践

### 7.1 封装常用操作

```typescript
// utils/common.ts

export async function getCurrentTab() {
  const tabs = await browser.tabs.query({ active: true, currentWindow: true });
  return tabs[0];
}

export async function createNotification(title: string, message: string) {
  await browser.notifications.create({
    type: 'basic',
    iconUrl: 'icons/icon-48.png',
    title,
    message,
  });
}

export async function sendMessageToContentScript(
  tabId: number,
  message: any
) {
  return await browser.tabs.sendMessage(tabId, message);
}
```

### 7.2 错误处理

```typescript
async function safeSendMessage(message: any) {
  try {
    return await browser.runtime.sendMessage(message);
  } catch (error) {
    console.error('Failed to send message:', error);
    return { error: true, message: error.message };
  }
}
```

### 7.3 类型安全

```typescript
interface ExtensionMessage {
  type: string;
  payload?: any;
}

interface ExtensionResponse {
  data?: any;
  error?: boolean;
  message?: string;
}

async function sendMessage(
  message: ExtensionMessage
): Promise<ExtensionResponse> {
  return await browser.runtime.sendMessage(message);
}
```

## 下一步

- [入口点 API](./entrypoints.md)：学习入口点 API
- [配置 API](./config.md)：学习配置 API
- [构建阶段](../lifecycle/phases.md)：了解构建流程
- [示例代码](../examples/)：查看完整项目示例
