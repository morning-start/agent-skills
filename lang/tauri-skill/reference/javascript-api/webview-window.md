# webviewWindow 命名空间

`webviewWindow` 命名空间提供 WebView 窗口的创建和管理功能，是 WebView 相关的核心 API。

## 导入

```typescript
import { WebviewWindow } from '@tauri-apps/api/webviewWindow';
```

## 函数

### newWebviewWindow(label: string, options?: WebviewWindowOptions): Promise<WebviewWindow>

创建新的 WebView 窗口。

```typescript
async function newWebviewWindow(label: string, options?: WebviewWindowOptions): Promise<WebviewWindow>
```

**示例：**
```typescript
import { newWebviewWindow } from '@tauri-apps/api/webviewWindow';

const webview = await newWebviewWindow('my-view', {
  url: 'https://tauri.app',
  title: 'Tauri',
  width: 800,
  height: 600
});
```

### getWebviewWindow(label: string): WebviewWindow

获取现有 WebView 窗口。

```typescript
function getWebviewWindow(label: string): WebviewWindow
```

## WebviewWindow 类

### 创建窗口

```typescript
import { newWebviewWindow } from '@tauri-apps/api/webviewWindow';

const win = await newWebviewWindow('child', {
  url: 'child.html',
  title: 'Child Window',
  width: 400,
  height: 300,
  center: true
});
```

### 窗口操作

```typescript
const win = getWebviewWindow('main');

// 获取/设置标题
const title = await win.title();
await win.setTitle('New Title');

// 获取/设置大小
const size = await win.innerSize();
await win.setSize({ width: 800, height: 600 });

// 获取/设置位置
const pos = await win.innerPosition();
await win.setPosition({ x: 100, y: 100 });

// 最小化/最大化/恢复
await win.minimize();
await win.maximize();
await win.unmaximize();

// 关闭
await win.close();

// 显示/隐藏
await win.show();
await win.hide();

// 设置焦点
await win.setFocus();

// 全屏
await win.setFullscreen(true);
await win.setFullscreen(false);
```

### 事件监听

```typescript
const win = getWebviewWindow('main');

// 窗口移动
win.onMoved(({ payload }) => {
  console.log('Moved to:', payload.x, payload.y);
});

// 窗口大小变化
win.onResized(({ payload }) => {
  console.log('Resized to:', payload.width, payload.height);
});

// 窗口关闭请求
win.onCloseRequested((event) => {
  event.preventDefault();
  console.log('Close requested');
});

// 焦点变化
win.onFocusChanged(({ payload: focused }) => {
  console.log('Focus:', focused);
});

// 主题变化
win.onThemeChanged(({ payload }) => {
  console.log('Theme:', payload);
});
```

## WebviewWindowOptions

```typescript
interface WebviewWindowOptions {
  url?: string;
  title?: string;
  width?: number;
  height?: number;
  minWidth?: number;
  minHeight?: number;
  maxWidth?: number;
  maxHeight?: number;
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
}
```
