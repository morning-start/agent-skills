# window 命名空间

`window` 命名空间提供窗口管理功能，用于获取当前窗口并进行各种操作。

## 导入

```typescript
import { getCurrentWindow, Window } from '@tauri-apps/api/window';
```

## 函数

### getCurrentWindow(): Window

获取当前窗口实例。

```typescript
function getCurrentWindow(): Window
```

**示例：**
```typescript
import { getCurrentWindow } from '@tauri-apps/api/window';

const win = getCurrentWindow();
console.log(win.label);
```

## Window 类

### 窗口信息

```typescript
const win = getCurrentWindow();

// 窗口标签
const label = win.label;

// 创建 Promise 版本
const window = await win.asWindow();
```

### 标题操作

```typescript
// 获取标题
const title = await win.title();

// 设置标题
await win.setTitle('My App');
```

### 大小操作

```typescript
// 获取内部尺寸
const size = await win.innerSize();
console.log(size.width, size.height);

// 设置尺寸
await win.setSize({ width: 800, height: 600 });

// 获取外部尺寸
const outerSize = await win.outerSize();

// 设置最小尺寸
await win.setMinSize({ width: 400, height: 300 });

// 设置最大尺寸
await win.setMaxSize({ width: 1200, height: 900 });
```

### 位置操作

```typescript
// 获取内部位置
const position = await win.innerPosition();
console.log(position.x, position.y);

// 设置位置
await win.setPosition({ x: 100, y: 100 });

// 获取外部位置
const outerPosition = await win.outerPosition();

// 居中
await win.center();
```

### 窗口状态

```typescript
// 最小化
await win.minimize();

// 最大化
await win.maximize();

// 恢复（取消最大化）
await win.unmaximize();

// 切换最大化
await win.toggleMaximize();

// 是否最大化
const isMaximized = await win.isMaximized();

// 全屏
await win.setFullscreen(true);
await win.setFullscreen(false);

// 是否全屏
const isFullscreen = await win.isFullscreen();

// 显示/隐藏
await win.show();
await win.hide();

// 关闭
await win.close();
```

### 窗口属性

```typescript
// 设置始终置顶
await win.setAlwaysOnTop(true);

// 获取缩放因子
const scaleFactor = await win.scaleFactor();

// 是否获得焦点
const isFocused = await win.isFocused();

// 请求焦点
await win.setFocus();

// 设置焦点
await win.requestUserAttention(2); // 1: informational, 2: critical
```

### 事件监听

```typescript
const win = getCurrentWindow();

// 窗口移动
const unlistenMove = win.onMoved((event) => {
  console.log('Window moved to:', event.payload.x, event.payload.y);
});

// 窗口大小变化
const unlistenResize = win.onResized((event) => {
  console.log('Window resized to:', event.payload.width, event.payload.height);
});

// 关闭请求
const unlistenClose = win.onCloseRequested((event) => {
  console.log('Window close requested');
  // 阻止关闭
  event.preventDefault();
});

// 焦点变化
const unlistenFocus = win.onFocusChanged((event) => {
  console.log('Focus changed:', event.payload);
});

// 主题变化
const unlistenTheme = win.onThemeChanged((event) => {
  console.log('Theme changed:', event.payload);
});

// 取消监听
unlistenMove();
unlistenResize();
unlistenClose();
unlistenFocus();
unlistenTheme();
```

## WindowOptions

创建窗口时使用的选项：

```typescript
interface WindowOptions {
  label: string;
  title?: string;
  width?: number;
  height?: number;
  minWidth?: number;
  minHeight?: number;
  resizable?: boolean;
  fullscreen?: boolean;
  center?: boolean;
  x?: number;
  y?: number;
  decorations?: boolean;
  transparent?: boolean;
  alwaysOnTop?: boolean;
  focus?: boolean;
  visible?: boolean;
}
```
