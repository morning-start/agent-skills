# webview 命名空间

`webview` 命名空间提供 WebView 控制功能，用于创建和管理 WebView 窗口。

## 导入

```typescript
import { Webview, WebviewWindow } from '@tauri-apps/api/webview';
```

## 函数

### createWebviewWindow(label: string, options?: WebviewWindowOptions): Promise<WebviewWindow>

创建新的 WebView 窗口。

```typescript
async function createWebviewWindow(label: string, options?: WebviewWindowOptions): Promise<WebviewWindow>
```

**示例：**
```typescript
import { createWebviewWindow } from '@tauri-apps/api/webview';

const webview = await createWebviewWindow('my-webview', {
  url: 'https://tauri.app',
  title: 'Tauri Website',
  width: 800,
  height: 600,
  center: true
});
```

### getWebviewWindow(label: string): WebviewWindow

根据标签获取 WebView 窗口。

```typescript
function getWebviewWindow(label: string): WebviewWindow
```

### getAllWebviewWindows(): WebviewWindow[]

获取所有 WebView 窗口。

```typescript
function getAllWebviewWindows(): WebviewWindow[]
```

## WebviewWindow 类

### 属性

```typescript
interface WebviewWindow {
  label: string;
  title: string;
  url: string;
}
```

### 方法

```typescript
const webview = getWebviewWindow('my-webview');

// 获取窗口标题
const title = await webview.title();

// 设置窗口标题
await webview.setTitle('New Title');

// 获取 URL
const url = await webview.url();

// 加载 URL
await webview.setUrl('https://new-url.com');

// 加载 HTML
await webview.setHtml('<html><body>Hello!</body></html>');

// 关闭窗口
await webview.close();

// 销毁窗口
await webview.destroy();
```

### 事件

```typescript
import { getWebviewWindow } from '@tauri-apps/api/webview';

const webview = getWebviewWindow('my-webview');

// 页面加载完成
await webview.onPageReady(() => {
  console.log('Page loaded!');
});

// DOM 内容加载完成
await webview.onDomContentLoaded(() => {
  console.log('DOM ready!');
});
```

## WebviewWindowOptions

```typescript
interface WebviewWindowOptions {
  url?: string;
  title?: string;
  width?: number;
  height?: number;
  x?: number;
  y?: number;
  center?: boolean;
  resizable?: boolean;
  fullscreen?: boolean;
  decorations?: boolean;
  transparent?: boolean;
  alwaysOnTop?: boolean;
  focus?: boolean;
  visible?: boolean;
  enabled?: boolean;
}
```

## 窗口间通信

```typescript
import { getWebviewWindow, emit } from '@tauri-apps/api/webview';

// 向其他窗口发送消息
await emitTo('other-webview', 'message', { text: 'Hello!' });

// 监听来自其他窗口的消息
await listen('message', (event) => {
  console.log('Received:', event.payload);
});
```
