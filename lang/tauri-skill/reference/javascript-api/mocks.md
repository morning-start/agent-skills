# mocks 命名空间

`mocks` 命名空间提供测试模拟功能，用于在测试环境中模拟 Tauri API。

## 导入

```typescript
import { mock, Mock } from '@tauri-apps/api/mocks';
```

## 函数

### mock<T>(key: string, value: T): void

模拟 Tauri API。

**示例：**
```typescript
import { mock } from '@tauri-apps/api/mocks';

mock('greet', (args) => {
  return `Hello, ${args.name}!`;
});
```

### mockConsole()

模拟 console 对象。

```typescript
mockConsole();
```

### mockLogger()

模拟日志输出。

```typescript
mockLogger();
```

## Mock 类

### 创建模拟实例

```typescript
import { Mock } from '@tauri-apps/api/mocks';

const mock = new Mock();
```

## 测试示例

```typescript
import { mock, invoke } from '@tauri-apps/api';

// 模拟 invoke 函数
mock('my_command', async (args) => {
  return { success: true, data: args.value };
});

// 在测试中使用
const result = await invoke('my_command', { value: 42 });
console.log(result); // { success: true, data: 42 }
```

## 常用模拟场景

### 模拟文件对话框

```typescript
mock('dialog:open', () => {
  return '/path/to/file.txt';
});

mock('dialog:save', () => {
  return '/path/to/save.txt';
});
```

### 模拟通知

```typescript
mock('notification:send', (args) => {
  console.log('Notification:', args.title, args.body);
  return true;
});
```

### 模拟文件系统

```typescript
mock('fs:readTextFile', () => {
  return 'File content';
});

mock('fs:writeTextFile', () => {
  return true;
});
```
