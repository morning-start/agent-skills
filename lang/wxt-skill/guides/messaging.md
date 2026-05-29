# 扩展内通信

本文档详细说明 WXT 扩展内的脚本间通信方法，包括 Background、Content、Popup 等不同上下文之间的消息传递。

## 官方导航链接

- [Messaging](https://wxt.dev/guide/essentials/messaging.html) - 消息传递完整指南
- [Content Scripts](https://wxt.dev/guide/essentials/content-scripts.html) - 内容脚本通信

---

## 一、通信类型

### 1.1 通信关系

WXT 扩展中的脚本间通信关系：

```
┌─────────────────┐
│  Background     │ ←→ Extension Storage
│  Script         │ ←→ Browser API
└────────┬────────┘
         │
         ├─→ Popup
         ├─→ Options
         └─→ Content Scripts (多个)
```

### 1.2 通信方式

| 方式 | 类型 | 用途 |
|------|------|------|
| `sendMessage` | 一次性消息 | 简单请求-响应 |
| `connect` | 长连接 | 持续通信 |
| `storage` | 共享存储 | 数据同步 |
| `browser.runtime` | 广播 | 通知所有脚本 |

## 二、一次性消息

### 2.1 发送消息

**从 Content Script 发送到 Background：**

```typescript
// entrypoints/content.ts
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],

  main() {
    browser.runtime.sendMessage({
      type: 'GET_USER',
      userId: 123,
    }).then((response) => {
      console.log('Response:', response);
    }).catch((error) => {
      console.error('Error:', error);
    });
  },
});
```

**从 Popup 发送到 Background：**

```typescript
// entrypoints/popup/main.ts
async function handleClick() {
  const response = await browser.runtime.sendMessage({
    type: 'GET_DATA',
    url: window.location.href,
  });

  console.log('Data:', response);
}
```

### 2.2 接收消息

**Background Script 接收消息：**

```typescript
// entrypoints/background.ts
import { defineBackground } from 'wxt/sandbox';

export default defineBackground(() => {
  browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('Received message:', message);
    console.log('Sender:', sender);

    switch (message.type) {
      case 'GET_USER':
        handleGetUser(message.userId).then(sendResponse);
        return true; // 异步响应

      case 'GET_DATA':
        const data = handleGetData(message.url);
        sendResponse(data);
        return false; // 同步响应

      default:
        sendResponse({ error: 'Unknown message type' });
        return false;
    }
  });
});

async function handleGetUser(userId) {
  // 模拟异步操作
  const user = await fetchUserFromAPI(userId);
  return user;
}

function handleGetData(url) {
  return { url, data: '...' };
}
```

### 2.3 Content Script 接收消息

```typescript
// entrypoints/content.ts
browser.runtime.onMessage.addListener((message, sender) => {
  console.log('Received:', message);

  if (message.type === 'HIGHLIGHT') {
    document.body.classList.add('highlighted');
  }

  return false;
});
```

### 2.4 发送到指定标签页

```typescript
// Background Script
async function sendToTab(tabId, message) {
  const response = await browser.tabs.sendMessage(tabId, {
    type: 'ACTION',
    data: message,
  });
  return response;
}

// 使用示例
const tabs = await browser.tabs.query({ active: true, currentWindow: true });
if (tabs[0]) {
  await sendToTab(tabs[0].id, { action: 'highlight' });
}
```

## 三、长连接

### 3.1 建立连接

**从 Content Script 连接到 Background：**

```typescript
// entrypoints/content.ts
const port = browser.runtime.connect({ name: 'content-port' });

// 监听消息
port.onMessage.addListener((message) => {
  console.log('Received:', message);
});

// 发送消息
port.postMessage({ type: 'HELLO', data: 'Hello from content' });

// 监听断开
port.onDisconnect.addListener(() => {
  console.log('Port disconnected');
});
```

### 3.2 Background 处理连接

```typescript
// entrypoints/background.ts
export default defineBackground(() => {
  browser.runtime.onConnect.addListener((port) => {
    console.log('Connected to:', port.name);

    // 监听消息
    port.onMessage.addListener((message) => {
      console.log('Received:', message);

      if (message.type === 'HELLO') {
        port.postMessage({
          type: 'ACK',
          data: 'Hello from background',
        });
      }
    });

    // 监听断开
    port.onDisconnect.addListener(() => {
      console.log('Port disconnected:', port.name);
    });
  });
});
```

### 3.3 多端口管理

```typescript
// entrypoints/background.ts
const ports = new Map();

browser.runtime.onConnect.addListener((port) => {
  const tabId = port.sender?.tab?.id;
  if (tabId) {
    ports.set(tabId, port);

    port.onDisconnect.addListener(() => {
      ports.delete(tabId);
    });
  }

  port.onMessage.addListener((message) => {
    broadcastToAll(message, port);
  });
});

function broadcastToAll(message, excludePort) {
  for (const [tabId, port] of ports.entries()) {
    if (port !== excludePort) {
      port.postMessage(message);
    }
  }
}
```

## 四、跨扩展通信

### 4.1 发送到其他扩展

```typescript
// Background Script
const otherExtensionId = 'abcdefghijklmno...';

const response = await browser.runtime.sendMessage(
  otherExtensionId,
  { type: 'PING' }
);

console.log('Response:', response);
```

### 4.2 接收来自其他扩展的消息

```typescript
// Background Script
export default defineBackground(() => {
  // 外部扩展必须知道你的扩展 ID
  browser.runtime.onMessageExternal.addListener(
    (message, sender, sendResponse) => {
      console.log('External message:', message);
      console.log('From:', sender.id);

      if (message.type === 'PING') {
        sendResponse({ type: 'PONG' });
      }

      return false;
    }
  );
});
```

## 五、与 Native Messaging 通信

### 5.1 声明权限

```typescript
// wxt.config.ts
export default defineConfig({
  manifest: {
    permissions: ['nativeMessaging'],
  },
});
```

### 5.2 发送消息到 Native 应用

```typescript
// Background Script
async function sendToNativeApp(message) {
  const port = browser.runtime.connectNative('com.example.app');
  port.postMessage(message);

  port.onMessage.addListener((response) => {
    console.log('Native response:', response);
  });

  port.onDisconnect.addListener(() => {
    console.log('Disconnected from native app');
  });
}

// 使用示例
await sendToNativeApp({ action: 'getData' });
```

### 5.3 接收 Native 消息

```typescript
const port = browser.runtime.connectNative('com.example.app');

port.onMessage.addListener((message) => {
  console.log('Message from native app:', message);
  // 处理消息
});
```

## 六、通信模式

### 6.1 请求-响应模式

```typescript
// Content Script
const response = await browser.runtime.sendMessage({
  type: 'FETCH_DATA',
  url: 'https://api.example.com/data',
});

console.log('Data:', response.data);

// Background Script
browser.runtime.onMessage.addListener((message) => {
  if (message.type === 'FETCH_DATA') {
    return fetch(message.url)
      .then(res => res.json())
      .then(data => ({ data }));
  }
});
```

### 6.2 发布-订阅模式

```typescript
// Background Script
const subscribers = new Set();

browser.runtime.onMessage.addListener((message, sender) => {
  if (message.type === 'SUBSCRIBE') {
    subscribers.add(sender.tab?.id);
  } else if (message.type === 'UNSUBSCRIBE') {
    subscribers.delete(sender.tab?.id);
  } else if (message.type === 'PUBLISH') {
    broadcast(message.event);
  }
});

function broadcast(event) {
  subscribers.forEach(tabId => {
    browser.tabs.sendMessage(tabId, {
      type: 'EVENT',
      event,
    });
  });
}
```

### 6.3 事件总线模式

```typescript
// utils/eventBus.ts
class EventBus {
  private listeners = new Map();

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  off(event, callback) {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      const index = callbacks.indexOf(callback);
      if (index !== -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  emit(event, data) {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.forEach(callback => callback(data));
    }
  }
}

export const eventBus = new EventBus();
```

## 七、错误处理

### 7.1 消息发送失败

```typescript
async function sendMessageSafely(message) {
  try {
    const response = await browser.runtime.sendMessage(message);
    return response;
  } catch (error) {
    if (error.message.includes('Receiving end does not exist')) {
      console.error('No listener for message');
    } else {
      console.error('Message send error:', error);
    }
    return null;
  }
}
```

### 7.2 超时处理

```typescript
async function sendMessageWithTimeout(message, timeout = 5000) {
  return Promise.race([
    browser.runtime.sendMessage(message),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Timeout')), timeout)
    ),
  ]);
}
```

### 7.3 验证消息

```typescript
function isValidMessage(message) {
  return message && typeof message === 'object' && message.type;
}

browser.runtime.onMessage.addListener((message) => {
  if (!isValidMessage(message)) {
    console.error('Invalid message:', message);
    return false;
  }

  // 处理消息
});
```

## 八、最佳实践

### 8.1 消息格式规范

```typescript
// ✅ 统一的消息格式
interface Message {
  type: string;
  payload?: any;
  id?: string;
  timestamp?: number;
}

// 发送消息
const message: Message = {
  type: 'FETCH_DATA',
  payload: { url: 'https://example.com' },
  id: generateId(),
  timestamp: Date.now(),
};

await browser.runtime.sendMessage(message);
```

### 8.2 类型定义

```typescript
// types/messages.ts
export type MessageType =
  | 'GET_USER'
  | 'UPDATE_SETTINGS'
  | 'TOGGLE_FEATURE'
  | 'NOTIFY';

export interface Message<T = any> {
  type: MessageType;
  payload: T;
}

export interface GetUserPayload {
  userId: number;
}

export interface UpdateSettingsPayload {
  theme: 'light' | 'dark';
  language: string;
}

// 使用示例
async function getUser(userId: number) {
  const message: Message<GetUserPayload> = {
    type: 'GET_USER',
    payload: { userId },
  };

  return await browser.runtime.sendMessage(message);
}
```

### 8.3 消息去重

```typescript
const pendingMessages = new Map();

async function sendMessageOnce(message) {
  const key = JSON.stringify(message);

  if (pendingMessages.has(key)) {
    return pendingMessages.get(key);
  }

  const promise = browser.runtime.sendMessage(message);
  pendingMessages.set(key, promise);

  try {
    return await promise;
  } finally {
    pendingMessages.delete(key);
  }
}
```

### 8.4 性能优化

```typescript
// 批量发送消息
async function sendBatch(messages) {
  const promises = messages.map(message =>
    browser.runtime.sendMessage(message)
  );
  return await Promise.all(promises);
}

// 防抖
function debounce(func, wait) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

const debouncedSend = debounce((message) => {
  browser.runtime.sendMessage(message);
}, 300);
```

## 九、完整示例

```typescript
// utils/messaging.ts
import { storage } from 'wxt/utils/storage';

// 类型定义
export interface Message<T = any> {
  type: string;
  payload: T;
  id?: string;
}

// 消息发送
export async function sendMessage<T = any>(message: Message<T>) {
  return await browser.runtime.sendMessage(message);
}

// 发送到当前标签页
export async function sendToActiveTab<T = any>(message: Message<T>) {
  const tabs = await browser.tabs.query({
    active: true,
    currentWindow: true,
  });

  if (tabs[0]) {
    return await browser.tabs.sendMessage(tabs[0].id, message);
  }

  throw new Error('No active tab');
}

// 消息监听器
export function createMessageHandler(handlers: Record<string, Function>) {
  return (message: Message, sender: any, sendResponse: Function) => {
    const handler = handlers[message.type];

    if (handler) {
      const result = handler(message.payload, sender);
      if (result instanceof Promise) {
        result.then(sendResponse);
        return true;
      } else {
        sendResponse(result);
        return false;
      }
    }

    console.warn('Unhandled message type:', message.type);
    return false;
  };
}

// 使用示例
// entrypoints/background.ts
export default defineBackground(() => {
  const handlers = {
    GET_USER: async (payload: { userId: number }) => {
      const user = await fetchUser(payload.userId);
      return { user };
    },

    UPDATE_SETTINGS: async (payload: any) => {
      await storage.defineItem('sync:settings').setValue(payload);
      return { success: true };
    },
  };

  browser.runtime.onMessage.addListener(createMessageHandler(handlers));
});
```
