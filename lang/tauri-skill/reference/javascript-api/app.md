# app 命名空间

`app` 命名空间提供应用生命周期管理和获取应用信息的功能。

## 导入

```typescript
import { app } from '@tauri-apps/api';
```

## 函数

### getName()

获取应用名称。

```typescript
function getName(): Promise<string>
```

**示例：**
```typescript
const name = await app.getName();
console.log(name); // "My App"
```

### getVersion()

获取应用版本号。

```typescript
function getVersion(): Promise<string>
```

**示例：**
```typescript
const version = await app.getVersion();
console.log(version); // "1.0.0"
```

### getTauriVersion()

获取 Tauri 框架版本。

```typescript
function getTauriVersion(): Promise<string>
```

**示例：**
```typescript
const tauriVersion = await app.getTauriVersion();
console.log(tauriVersion); // "2.10.2"
```

### getAppWindow()

获取当前应用窗口实例。

```typescript
function getAppWindow(): Promise<WebviewWindow>
```

**示例：**
```typescript
const win = await app.getAppWindow();
await win.setTitle('New Title');
```

### show()

显示应用窗口（如果隐藏）。

```typescript
function show(): Promise<void>
```

### hide()

隐藏应用窗口。

```typescript
function hide(): Promise<void>
```

### setAppTheme()

设置应用主题。

```typescript
function setAppTheme(theme: 'light' | 'dark' | 'system'): Promise<void>
```

**示例：**
```typescript
await app.setAppTheme('dark');
```

## 事件

### appReady

应用准备就绪时触发。

```typescript
import { onAppReady } from '@tauri-apps/api/app';

onAppReady(() => {
  console.log('App is ready!');
});
```

### windowResized

窗口大小改变时触发。

```typescript
import { onWindowResized } from '@tauri-apps/api/app';

onWindowResized(({ payload }) => {
  console.log('Window resized:', payload);
});
```
