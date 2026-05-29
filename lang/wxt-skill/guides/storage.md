# 数据存储方案

本文档详细说明 WXT 的数据存储方案，包括浏览器存储 API、WXT 存储工具、迁移和最佳实践。

## 官方导航链接

- [Storage](https://wxt.dev/guide/essentials/storage.html) - 数据存储完整指南
- [Permissions](https://wxt.dev/guide/essentials/permissions.html) - 存储权限配置

---

## 一、存储类型

### 1.1 浏览器存储类型

| 类型 | 容量限制 | 同步 | 清理时机 | 用途 |
|------|----------|------|----------|------|
| `storage.local` | ~10MB | 不同步 | 手动删除 | 本地数据 |
| `storage.sync` | ~100KB | 同步 | 手动删除 | 同步设置 |
| `storage.session` | ~1MB | 不同步 | 会话结束 | 临时数据 |

### 1.2 存储选择指南

```typescript
// settings - 使用 sync（跨设备同步）
await browser.storage.sync.set({ theme: 'dark' });

// cache - 使用 local（大容量）
await browser.storage.local.set({ cacheData: largeObject });

// temp - 使用 session（临时数据）
await browser.storage.session.set({ tempData: '...' });
```

## 二、基础用法

### 2.1 写入数据

```typescript
// 写入单个值
await browser.storage.local.set({
  apiKey: 'your-api-key',
  enabled: true,
});

// 写入嵌套对象
await browser.storage.local.set({
  settings: {
    theme: 'dark',
    language: 'en',
  },
});

// 写入多个键值对
await browser.storage.local.set({
  name: 'John',
  age: 30,
  email: 'john@example.com',
});
```

### 2.2 读取数据

```typescript
// 读取单个值
const result = await browser.storage.local.get('apiKey');
console.log(result.apiKey); // 'your-api-key'

// 读取多个值
const data = await browser.storage.local.get(['apiKey', 'enabled']);
console.log(data.apiKey, data.enabled);

// 读取所有数据
const allData = await browser.storage.local.get();

// 带默认值
const result = await browser.storage.local.get({ theme: 'light' });
console.log(result.theme); // 'light' 或存储的值
```

### 2.3 删除数据

```typescript
// 删除单个键
await browser.storage.local.remove('apiKey');

// 删除多个键
await browser.storage.local.remove(['apiKey', 'enabled']);

// 清空所有数据
await browser.storage.local.clear();
```

## 三、监听变化

### 3.1 监听存储变化

```typescript
browser.storage.onChanged.addListener((changes, areaName) => {
  console.log('Storage changed:', areaName);

  for (const [key, { oldValue, newValue }] of Object.entries(changes)) {
    console.log(`${key}:`, oldValue, '->', newValue);
  }
});
```

### 3.2 响应式存储

```typescript
// Background Script
browser.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === 'sync' && changes.enabled?.newValue) {
    const enabled = changes.enabled.newValue;
    console.log('Extension enabled:', enabled);

    if (enabled) {
      startBackgroundTask();
    } else {
      stopBackgroundTask();
    }
  }
});
```

### 3.3 跨标签页同步

```typescript
// 标签页 A
await browser.storage.sync.set({ theme: 'dark' });

// 标签页 B（自动接收变化）
browser.storage.onChanged.addListener((changes) => {
  if (changes.theme) {
    applyTheme(changes.theme.newValue);
  }
});
```

## 四、WXT 存储工具

### 4.1 使用 storage 工具

```typescript
import { storage } from 'wxt/utils/storage';

// 定义存储项
const apiKey = storage.defineItem('local:apiKey', {
  defaultValue: '',
});

const theme = storage.defineItem('sync:theme', {
  defaultValue: 'light',
});

const tempData = storage.defineItem('session:tempData', {
  defaultValue: null,
});
```

### 4.2 读取存储项

```typescript
// 读取单个值
const key = await apiKey.getValue();
console.log(key); // 'your-api-key' 或 ''

// 读取多个值
const values = await Promise.all([
  apiKey.getValue(),
  theme.getValue(),
]);
```

### 4.3 写入存储项

```typescript
// 写入值
await apiKey.setValue('new-api-key');

// 删除值
await apiKey.remove();
```

### 4.4 监听变化

```typescript
const unwatch = apiKey.watch((newValue, oldValue) => {
  console.log('API key changed:', oldValue, '->', newValue);
});

// 停止监听
unwatch();
```

### 4.5 响应式集成（Vue）

```vue
<script setup>
import { storage } from 'wxt/utils/storage';

const theme = storage.defineItem('sync:theme', {
  defaultValue: 'light',
});

// 使用 Vue 的 ref
const currentTheme = ref(theme.defaultValue);

// 监听变化
theme.watch((value) => {
  currentTheme.value = value;
});
</script>

<template>
  <div :class="currentTheme">
    Content
  </div>
</template>
```

## 五、数据迁移

### 5.1 版本管理

```typescript
// 存储版本号
await browser.storage.local.set({
  storageVersion: 2,
});
```

### 5.2 迁移脚本

```typescript
// Background Script
export default defineBackground(async () => {
  const currentVersion = await browser.storage.local.get('storageVersion')
    .then((data) => data.storageVersion || 1);

  if (currentVersion < 2) {
    console.log('Migrating to version 2...');

    // 迁移数据
    const oldData = await browser.storage.local.get('oldKey');
    await browser.storage.local.set({
      newData: transform(oldData.oldKey),
    });
    await browser.storage.local.remove('oldKey');

    // 更新版本
    await browser.storage.local.set({ storageVersion: 2 });
  }
});

function transform(oldValue) {
  // 数据转换逻辑
  return { ...oldValue, version: 2 };
}
```

### 5.3 批量迁移

```typescript
async function migrateStorage() {
  const data = await browser.storage.local.get();

  for (const [key, value] of Object.entries(data)) {
    if (needsMigration(key)) {
      const newValue = transformValue(value);
      await browser.storage.local.set({ [key]: newValue });
    }
  }
}
```

## 六、错误处理

### 6.1 捕获错误

```typescript
try {
  await browser.storage.local.set({
    data: largeObject,
  });
} catch (error) {
  if (error.message.includes('QUOTA_BYTES')) {
    console.error('Storage quota exceeded');
    // 清理旧数据
    await cleanupOldData();
  }
}
```

### 6.2 验证数据

```typescript
function isValidData(data) {
  return typeof data === 'object' && data !== null;
}

async function saveData(data) {
  if (!isValidData(data)) {
    throw new Error('Invalid data format');
  }

  await browser.storage.local.set({ data });
}
```

## 七、最佳实践

### 7.1 数据结构设计

```typescript
// ✅ 好的数据结构
const settings = {
  user: {
    name: 'John',
    email: 'john@example.com',
  },
  app: {
    theme: 'dark',
    language: 'en',
  },
};

// ❌ 差的数据结构
const settings = {
  userName: 'John',
  userEmail: 'john@example.com',
  appTheme: 'dark',
  appLanguage: 'en',
};
```

### 7.2 性能优化

```typescript
// 批量读写
await browser.storage.local.set({
  key1: value1,
  key2: value2,
  key3: value3,
});

// 避免频繁读写
const cache = new Map();

async function getCachedData(key) {
  if (cache.has(key)) {
    return cache.get(key);
  }

  const data = await browser.storage.local.get(key);
  cache.set(key, data);
  return data;
}
```

### 7.3 数据安全

```typescript
// 加密敏感数据
async function saveSecureData(key, value) {
  const encrypted = encrypt(value);
  await browser.storage.local.set({ [key]: encrypted });
}

async function getSecureData(key) {
  const data = await browser.storage.local.get(key);
  return decrypt(data[key]);
}
```

### 7.4 清理策略

```typescript
// 定期清理过期数据
async function cleanupOldData() {
  const data = await browser.storage.local.get();

  for (const [key, value] of Object.entries(data)) {
    if (isExpired(value)) {
      await browser.storage.local.remove(key);
    }
  }
}

function isExpired(item) {
  return item.expiry < Date.now();
}
```

## 八、完整示例

```typescript
// utils/storage.ts
import { storage } from 'wxt/utils/storage';

// 定义存储项
export const apiKey = storage.defineItem('local:apiKey', {
  defaultValue: '',
});

export const settings = storage.defineItem('sync:settings', {
  defaultValue: {
    theme: 'light',
    language: 'en',
    notifications: true,
  },
});

export const cache = storage.defineItem('local:cache', {
  defaultValue: {},
});

// 辅助函数
export async function getApiKey() {
  return await apiKey.getValue();
}

export async function setApiKey(key) {
  await apiKey.setValue(key);
}

export async function getSettings() {
  return await settings.getValue();
}

export async function updateSettings(updates) {
  const current = await settings.getValue();
  await settings.setValue({ ...current, ...updates });
}

// 监听设置变化
export function watchSettings(callback) {
  return settings.watch((newValue, oldValue) => {
    callback(newValue, oldValue);
  });
}
```

```typescript
// entrypoints/popup/main.ts
import { getSettings, updateSettings, watchSettings } from '~/utils/storage';

// 读取设置
const settings = await getSettings();

// 更新设置
await updateSettings({ theme: 'dark' });

// 监听变化
const unwatch = watchSettings((newValue) => {
  console.log('Settings updated:', newValue);
});

// 组件销毁时停止监听
onCleanup(() => {
  unwatch();
});
```
