# 内容脚本开发

本文档详细说明如何在 WXT 中开发内容脚本（Content Scripts），包括注入规则、与页面交互、调试和最佳实践。

## 官方导航链接

- [Content Scripts](https://wxt.dev/guide/essentials/content-scripts.html) - 内容脚本完整指南
- [Messaging](https://wxt.dev/guide/essentials/messaging.html) - 脚本间通信方法
- [Scripting](https://wxt.dev/guide/essentials/scripting.html) - 动态脚本注入

---

## 一、内容脚本概述

### 1.1 什么是内容脚本

内容脚本是运行在网页上下文中的脚本，可以：
- 读取和修改 DOM
- 监听网页事件
- 与网页的 JavaScript 交互
- 与扩展的 background script 通信

### 1.2 内容脚本的限制

- 无法访问大多数扩展 API
- 无法访问扩展的变量
- 运行在独立的 JavaScript 环境中
- 每个 match 都会创建新的实例

## 二、定义内容脚本

### 2.1 基本定义

```typescript
// entrypoints/content.ts
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['*://*.example.com/*'],

  main() {
    console.log('Content script loaded');

    // 读取和修改 DOM
    const title = document.querySelector('h1');
    if (title) {
      title.textContent = 'Modified by WXT Extension';
    }
  },
});
```

### 2.2 多个匹配规则

```typescript
export default defineContentScript({
  matches: [
    '*://*.example.com/*',
    '*://*.test.com/*',
    '<all_urls>',  // 匹配所有网站
  ],

  main() {
    console.log('Content script loaded on:', window.location.href);
  },
});
```

### 2.3 排除规则

```typescript
export default defineContentScript({
  matches: ['*://*.example.com/*'],
  excludeMatches: [
    '*://*.example.com/admin/*',
    '*://*.example.com/login/*',
  ],

  main() {
    console.log('Content script loaded');
  },
});
```

## 三、高级配置

### 3.1 运行时机

```typescript
export default defineContentScript({
  matches: ['*://*.example.com/*'],

  // 'document_idle'（默认）、'document_start'、'document_end'
  run_at: 'document_idle',

  main() {
    console.log('Content script loaded');
  },
});
```

| 时机 | 说明 |
|------|------|
| `document_start` | 在 CSS 加载后，DOM 加载前 |
| `document_end` | 在 DOM 加载完成后 |
| `document_idle` | 浏览器选择最佳时机（推荐） |

### 3.2 注入样式

```typescript
export default defineContentScript({
  matches: ['*://*.example.com/*'],

  css: ['./content.css'],

  main() {
    console.log('Content script loaded');
  },
});
```

**content.css**

```css
.wxt-highlight {
  background-color: yellow;
  border: 2px solid red;
}
```

### 3.3 隐藏匹配

```typescript
export default defineContentScript({
  matches: ['*://*.example.com/*'],

  // 隐藏内容脚本的执行（对用户不可见）
  // 适用于后台任务
  hidden: false,

  main() {
    console.log('Content script loaded');
  },
});
```

## 四、与页面交互

### 4.1 读取 DOM

```typescript
main() {
  const title = document.querySelector('h1')?.textContent;
  const links = document.querySelectorAll('a');

  console.log('Page title:', title);
  console.log('Links count:', links.length);
}
```

### 4.2 修改 DOM

```typescript
main() {
  // 创建新元素
  const button = document.createElement('button');
  button.textContent = 'Click Me';
  button.className = 'wxt-button';

  // 添加到页面
  document.body.appendChild(button);

  // 添加事件监听
  button.addEventListener('click', () => {
    console.log('Button clicked');
  });
}
```

### 4.3 监听页面事件

```typescript
main() {
  // 监听 DOM 变化
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      console.log('DOM changed:', mutation);
    });
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });

  // 监听 URL 变化（SPA 应用）
  window.addEventListener('popstate', () => {
    console.log('URL changed:', window.location.href);
  });
}
```

## 五、与 Background Script 通信

### 5.1 发送消息到 Background

```typescript
// content.ts
main() {
  browser.runtime.sendMessage({
    type: 'GET_DATA',
    url: window.location.href,
  }).then((response) => {
    console.log('Response:', response);
  });
}
```

```typescript
// background.ts
export default defineBackground(() => {
  browser.runtime.onMessage.addListener((message, sender) => {
    console.log('Received:', message);

    if (message.type === 'GET_DATA') {
      return Promise.resolve({
        data: 'Data from background',
      });
    }
  });
});
```

### 5.2 长连接

```typescript
// content.ts
main() {
  const port = browser.runtime.connect();

  port.onMessage.addListener((message) => {
    console.log('Received:', message);
  });

  port.postMessage({ type: 'HELLO' });
}
```

```typescript
// background.ts
export default defineBackground(() => {
  browser.runtime.onConnect.addListener((port) => {
    console.log('Connected to content script');

    port.onMessage.addListener((message) => {
      console.log('Received:', message);
      port.postMessage({ type: 'ACK' });
    });
  });
});
```

## 六、动态注入

### 6.1 使用 browser.scripting

```typescript
// background.ts
browser.action.onClicked.addListener(async (tab) => {
  await browser.scripting.executeScript({
    target: { tabId: tab.id },
    files: ['content.js'],
  });
});
```

### 6.2 注入代码字符串

```typescript
// background.ts
browser.action.onClicked.addListener(async (tab) => {
  await browser.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      alert('Hello from WXT!');
    },
  });
});
```

### 6.3 传递参数

```typescript
// background.ts
browser.action.onClicked.addListener(async (tab) => {
  await browser.scripting.executeScript({
    target: { tabId: tab.id },
    args: ['Hello from WXT!', 42],
    func: (message, number) => {
      alert(message);
      console.log('Number:', number);
    },
  });
});
```

## 七、权限配置

### 7.1 权限声明

```typescript
// wxt.config.ts
export default defineConfig({
  manifest: {
    permissions: ['scripting', 'activeTab'],
  },
});
```

### 7.2 Host Permissions

```typescript
export default defineConfig({
  manifest: {
    host_permissions: ['<all_urls>'],
  },
});
```

## 八、调试

### 8.1 调试内容脚本

1. 打开目标网页
2. 按 F12 打开开发者工具
3. 在 Console 中查看 `console.log` 输出
4. 在 Sources 中找到 content script 文件

### 8.2 调试 Background Script

1. 访问 `chrome://extensions`
2. 找到你的扩展
3. 点击"Service Worker"或"Background page"
4. 打开开发者工具

### 8.3 常见问题

**问题：内容脚本没有加载**
- 检查 `matches` 规则是否正确
- 检查扩展是否已启用
- 刷新页面

**问题：无法访问扩展 API**
- 内容脚本无法访问大部分扩展 API
- 需要通过 Background Script 中转

**问题：DOM 操作失败**
- 确认 DOM 已加载
- 使用 `DOMContentLoaded` 事件
- 检查元素是否存在

## 九、最佳实践

### 9.1 性能优化

```typescript
// 使用事件委托
main() {
  document.body.addEventListener('click', (e) => {
    if (e.target.matches('.wxt-button')) {
      console.log('Button clicked');
    }
  });
}
```

### 9.2 内存管理

```typescript
main() {
  // 及时清理监听器
  const observer = new MutationObserver(callback);

  // 当不需要时
  observer.disconnect();
}
```

### 9.3 隔离样式

```css
/* 使用 Shadow DOM */
.wxt-widget {
  all: initial;
  /* 样式重置 */
}
```

### 9.4 安全考虑

```typescript
main() {
  // 避免直接使用 innerHTML（XSS 风险）
  // ❌ 错误
  element.innerHTML = userInput;

  // ✅ 正确
  element.textContent = userInput;
}
```

## 十、示例：完整的内容脚本

```typescript
// entrypoints/content.ts
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['*://*.example.com/*'],
  run_at: 'document_idle',
  css: ['./content.css'],

  main() {
    console.log('WXT Content Script loaded');

    // 创建工具栏
    const toolbar = document.createElement('div');
    toolbar.className = 'wxt-toolbar';
    toolbar.innerHTML = `
      <button id="highlight">Highlight</button>
      <button id="copy">Copy</button>
    `;

    document.body.appendChild(toolbar);

    // 添加事件监听
    document.getElementById('highlight')?.addEventListener('click', () => {
      document.body.classList.toggle('wxt-highlight');
    });

    document.getElementById('copy')?.addEventListener('click', async () => {
      const text = window.getSelection()?.toString();
      if (text) {
        await browser.runtime.sendMessage({ type: 'COPY', text });
      }
    });

    // 监听 Background 消息
    browser.runtime.onMessage.addListener((message) => {
      if (message.type === 'TOGGLE') {
        document.body.classList.toggle('wxt-highlight');
      }
    });
  },
});
```
