# event 命名空间

`event` 命名空间提供 Tauri 应用内的事件系统，用于前端与后端、前端与前端之间的通信。

## 导入

```typescript
import { listen, emit, once, UnlistenFn } from '@tauri-apps/api/event';
```

## 函数

### listen<T>(event: string, handler: EventHandler<T>): Promise<UnlistenFn>

监听事件。

**参数：**
- `event`: 事件名称
- `handler`: 事件处理函数

**返回：**
- `Promise<UnlistenFn>`: 取消监听函数

**示例：**
```typescript
import { listen } from '@tauri-apps/api/event';

const unlisten = await listen<string>('my-event', (event) => {
  console.log('Received:', event.payload);
});

// 取消监听
unlisten();
```

### once<T>(event: string, handler: EventHandler<T>): Promise<UnlistenFn>

只监听一次事件。

**示例：**
```typescript
import { once } from '@tauri-apps/api/event';

await once<{ message: string }>('init-data', (event) => {
  console.log('Init data:', event.payload);
});
```

### emit<T>(event: string, payload?: T): Promise<void>

发射事件（发送到前端）。

**示例：**
```typescript
import { emit } from '@tauri-apps/api/event';

// 发送数据
await emit('my-event', { message: 'Hello!' });

// 发送无数据事件
await emit('my-event');
```

### emitTo<T>(event: string, target: string, payload?: T): Promise<void>

向特定窗口发射事件。

**参数：**
- `event`: 事件名称
- `target`: 目标窗口标签
- `payload`: 事件数据

**示例：**
```typescript
import { emitTo } from '@tauri-apps/api/event';

await emitTo('main-window', 'data-update', { count: 42 });
await emitTo('secondary-window', 'close-dialog');
```

## 事件类型

### 前端到前端事件

```typescript
// 监听
await listen('from-other-window', (e) => console.log(e.payload));

// 发送
await emit('from-other-window', 'Hello from window 1!');
```

### 后端到前端事件

**Rust 后端：**
```rust
use tauri::{AppHandle, Emitter};

#[command]
fn send_to_frontend(app: AppHandle) {
    app.emit("backend-event", "Message from Rust!").unwrap();
}
```

### 窗口事件

监听窗口相关事件：

```typescript
import { getCurrentWindow } from '@tauri-apps/api/window';

const win = getCurrentWindow();

// 窗口移动事件
win.onMoved(({ payload }) => {
  console.log('Window moved to:', payload.x, payload.y);
});

// 窗口大小变化事件
win.onResized(({ payload }) => {
  console.log('Window resized:', payload.width, payload.height);
});

// 窗口关闭事件
win.onCloseRequested((event) => {
  console.log('Window close requested');
});
```

## 类型定义

```typescript
interface Event<T> {
  payload: T;
  windowLabel?: string;
}

type EventHandler<T> = (event: Event<T>) => void;

type UnlistenFn = () => void;
```
