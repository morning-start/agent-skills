# 权限配置详解

本文档详细说明 WXT 的权限配置，包括权限声明方式、动态权限申请和最佳实践。

## 官方导航链接

- [Permissions](https://wxt.dev/guide/essentials/permissions.html) - 权限配置完整指南
- [Manifest](https://wxt.dev/guide/essentials/config/manifest.html) - Manifest 配置中的权限设置
- [Storage](https://wxt.dev/guide/essentials/storage.html) - 存储权限与 API

---

## 一、权限类型

### 1.1 基础权限（permissions）

基础权限是扩展运行所需的权限，必须在 manifest 中声明。

| 权限 | 说明 | 用途 |
|------|------|------|
| `storage` | 存储权限 | 读写扩展存储 |
| `tabs` | 标签页权限 | 读写标签页 |
| `activeTab` | 活动标签页权限 | 访问当前活动标签页 |
| `scripting` | 脚本注入权限 | 动态注入脚本 |
| `alarms` | 警报权限 | 设置定时任务 |
| `notifications` | 通知权限 | 显示系统通知 |
| `cookies` | Cookie 权限 | 读写 Cookie |
| `history` | 历史记录权限 | 访问浏览历史 |
| `bookmarks` | 书签权限 | 读写书签 |
| `downloads` | 下载权限 | 管理下载 |
| `geolocation` | 地理位置权限 | 获取地理位置 |
| `identity` | 身份权限 | OAuth 认证 |
| `idle` | 空闲检测权限 | 检测用户空闲状态 |

### 1.2 主机权限（host_permissions）

主机权限是扩展访问特定网站的权限。

```typescript
host_permissions: [
  '<all_urls>',              // 所有网站
  'https://*/*',              // 所有 HTTPS 网站
  'http://localhost:*',       // 本地服务器
  'https://api.example.com/*', // 特定网站
]
```

**主机权限模式：**

| 模式 | 说明 | 示例 |
|------|------|------|
| `*://*/*` | 所有协议 | 访问所有网站 |
| `https://*/*` | 仅 HTTPS | 访问所有 HTTPS 网站 |
| `https://*.example.com/*` | 所有子域名 | 访问 example.com 的所有子域名 |
| `https://example.com/*` | 特定域名 | 访问特定网站 |
| `file:///*` | 本地文件 | 访问本地文件 |

### 1.3 可选权限（optional_permissions）

可选权限是可以在运行时申请的权限。

```typescript
optional_permissions: [
  'alarms',
  'notifications',
  'geolocation',
]
```

**参考文档：**
- 权限详解：https://wxt.dev/guide/essentials/permissions.html

## 二、配置权限

### 2.1 在 wxt.config.ts 中配置

```typescript
// wxt.config.ts
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    // 基础权限
    permissions: [
      'storage',
      'tabs',
      'activeTab',
      'scripting',
      'alarms',
    ],

    // 主机权限
    host_permissions: [
      'https://api.example.com/*',
    ],

    // 可选权限
    optional_permissions: [
      'notifications',
      'geolocation',
    ],
  },
});
```

### 2.2 使用覆盖配置

为不同浏览器配置不同权限：

```typescript
export default defineConfig({
  manifest: {
    permissions: ['storage', 'tabs'],

    // Chrome 特定权限
    chrome: {
      permissions: ['alarms', 'idle'],
    },

    // Firefox 特定权限
    firefox: {
      permissions: ['alarms'],
    },
  },
});
```

## 三、最小权限原则

### 3.1 仅请求必要的权限

**✅ 正确：** 仅请求必要的权限

```typescript
export default defineConfig({
  manifest: {
    permissions: ['storage'],
  },
});
```

**❌ 错误：** 请求过多权限

```typescript
export default defineConfig({
  manifest: {
    permissions: [
      'storage',
      'tabs',
      'activeTab',
      'scripting',
      'alarms',
      'notifications',
      'geolocation',
      'bookmarks',
      'history',
      'downloads',
    ],
  },
});
```

### 3.2 使用特定主机权限

**✅ 正确：** 使用特定主机权限

```typescript
host_permissions: [
  'https://api.example.com/*',
]
```

**❌ 错误：** 使用过于宽泛的主机权限

```typescript
host_permissions: [
  '<all_urls>',
]
```

### 3.3 使用可选权限

对于不立即需要的权限，使用可选权限：

```typescript
export default defineConfig({
  manifest: {
    permissions: ['storage', 'tabs'],

    optional_permissions: [
      'notifications',
      'geolocation',
    ],
  },
});
```

## 四、动态权限申请

### 4.1 请求权限

在运行时请求权限：

```typescript
// 请求权限
async function requestPermissions() {
  const result = await browser.permissions.request({
    permissions: ['notifications'],
    origins: ['https://api.example.com/*'],
  });

  if (result) {
    console.log('Permissions granted');
  } else {
    console.log('Permissions denied');
  }
}
```

### 4.2 检查权限

检查是否已拥有权限：

```typescript
// 检查权限
async function checkPermissions() {
  const result = await browser.permissions.contains({
    permissions: ['notifications'],
  });

  console.log('Has notifications permission:', result);
}
```

### 4.3 移除权限

移除已授予的权限：

```typescript
// 移除权限
async function removePermissions() {
  const result = await browser.permissions.remove({
    permissions: ['notifications'],
  });

  console.log('Permissions removed:', result);
}
```

### 4.4 监听权限变化

监听权限变化事件：

```typescript
// 监听权限变化
browser.permissions.onAdded.addListener((permissions) => {
  console.log('Permissions added:', permissions);
});

browser.permissions.onRemoved.addListener((permissions) => {
  console.log('Permissions removed:', permissions);
});
```

## 五、权限使用场景

### 5.1 Storage 权限

**用途：** 存储扩展配置和用户数据。

```typescript
// 配置权限
export default defineConfig({
  manifest: {
    permissions: ['storage'],
  },
});

// 使用存储
await browser.storage.sync.set({
  apiKey: 'your-api-key',
  enabled: true,
});

const data = await browser.storage.sync.get(['apiKey']);
console.log('API Key:', data.apiKey);
```

### 5.2 Tabs 权限

**用途：** 读写标签页。

```typescript
// 配置权限
export default defineConfig({
  manifest: {
    permissions: ['tabs'],
  },
});

// 获取当前标签页
const tabs = await browser.tabs.query({
  active: true,
  currentWindow: true,
});
console.log('Current tab:', tabs[0]);

// 创建新标签页
await browser.tabs.create({
  url: 'https://example.com',
});
```

### 5.3 ActiveTab 权限

**用途：** 仅访问当前活动标签页，更安全。

```typescript
// 配置权限
export default defineConfig({
  manifest: {
    permissions: ['activeTab'],
  },
});

// 访问当前活动标签页
const tabs = await browser.tabs.query({
  active: true,
  currentWindow: true,
});

// 注入脚本到当前标签页
await browser.scripting.executeScript({
  target: { tabId: tabs[0].id },
  func: () => {
    console.log('Script injected');
  },
});
```

### 5.4 Scripting 权限

**用途：** 动态注入脚本和样式。

```typescript
// 配置权限
export default defineConfig({
  manifest: {
    permissions: ['activeTab', 'scripting'],
  },
});

// 注入脚本
const tabs = await browser.tabs.query({
  active: true,
  currentWindow: true,
});

await browser.scripting.executeScript({
  target: { tabId: tabs[0].id },
  func: () => {
    console.log('Script injected');
  },
});
```

### 5.5 Alarms 权限

**用途：** 设置定时任务。

```typescript
// 配置权限
export default defineConfig({
  manifest: {
    permissions: ['alarms'],
  },
});

// 创建警报
await browser.alarms.create('check-updates', {
  periodInMinutes: 60,
});

// 监听警报
browser.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'check-updates') {
    console.log('Checking for updates...');
  }
});
```

## 六、权限与隐私

### 6.1 Chrome Web Store 审核要求

Chrome Web Store 对权限有严格要求：

1. **最小权限原则**：仅请求必要的权限
2. **清晰的描述**：解释为什么需要这些权限
3. **不收集不必要的数据**：不收集用户不相关的数据
4. **透明的数据使用**：清楚说明如何使用收集的数据

### 6.2 Firefox Add-ons 审核要求

Firefox Add-ons 对权限的审核要求：

1. **用户同意**：请求权限时必须获得用户同意
2. **数据保护**：保护用户隐私
3. **代码审查**：代码会被审查，确保不包含恶意代码

### 6.3 隐私政策

如果扩展收集用户数据，必须提供隐私政策。

**隐私政策应包含：**
- 收集哪些数据
- 如何使用数据
- 数据如何存储
- 是否与第三方共享
- 用户如何删除数据

**添加隐私政策链接：**

```typescript
export default defineConfig({
  manifest: {
    homepage_url: 'https://example.com/privacy',
  },
});
```

## 七、常见问题

### Q1: 如何选择权限？

**原则：** 最小权限原则。

1. 列出扩展需要的功能
2. 确定每个功能需要哪些权限
3. 仅请求必要的权限
4. 对于可选功能，使用可选权限

### Q2: 权限过多会影响审核吗？

**会影响。**

- Chrome Web Store 和 Firefox Add-ons 都会审核权限
- 权限过多会导致审核延迟或拒绝
- 用户也会对权限过多的扩展产生不信任

### Q3: 如何减少权限？

**方法：**

1. 使用 `activeTab` 代替 `tabs`
2. 使用特定主机权限代替 `<all_urls>`
3. 将可选功能改为可选权限
4. 使用 Content Script 代替 Background Script 处理某些功能

### Q4: 如何处理权限被拒绝？

**方法：**

1. 检查权限是否被拒绝
2. 提供友好的提示
3. 提供替代方案

```typescript
// 检查权限
const hasPermission = await browser.permissions.contains({
  permissions: ['notifications'],
});

if (!hasPermission) {
  // 显示提示
  alert('需要通知权限才能显示通知');
  // 请求权限
  await browser.permissions.request({
    permissions: ['notifications'],
  });
}
```

### Q5: 不同浏览器的权限有差异吗？

**有差异。**

不同浏览器支持的权限不同：

- Chrome 支持 `idle` 权限
- Firefox 支持 `alarms` 权限
- Safari 的权限支持较少

**解决方案：** 使用条件配置

```typescript
export default defineConfig(({ browser }) => ({
  manifest: {
    permissions: ['storage', 'tabs'],

    // Chrome 特定权限
    ...(browser === 'chrome' ? {
      chrome: {
        permissions: ['idle'],
      },
    } : {}),

    // Firefox 特定权限
    ...(browser === 'firefox' ? {
      firefox: {
        permissions: ['alarms'],
      },
    } : {}),
  },
}));
```

## 八、最佳实践

### 8.1 最小权限原则

始终使用最小权限原则：

```typescript
// ✅ 正确
permissions: ['activeTab']

// ❌ 错误
permissions: ['tabs']
```

### 8.2 使用可选权限

对于可选功能，使用可选权限：

```typescript
export default defineConfig({
  manifest: {
    permissions: ['storage', 'tabs'],
    optional_permissions: [
      'notifications',
      'geolocation',
    ],
  },
});
```

### 8.3 清晰的描述

在扩展描述中说明为什么需要这些权限：

```typescript
export default defineConfig({
  manifest: {
    description: '需要访问活动标签页以提供页面分析功能',
  },
});
```

### 8.4 动态请求权限

在需要时请求权限：

```typescript
// 在用户点击按钮时请求权限
document.getElementById('enable-notifications')!.addEventListener(
  'click',
  async () => {
    const result = await browser.permissions.request({
      permissions: ['notifications'],
    });

    if (result) {
      alert('通知权限已授予');
    } else {
      alert('通知权限被拒绝');
    }
  }
);
```

### 8.5 检查权限

在使用 API 前检查权限：

```typescript
// 检查权限
const hasPermission = await browser.permissions.contains({
  permissions: ['notifications'],
});

if (hasPermission) {
  // 使用通知 API
  browser.notifications.create({
    type: 'basic',
    iconUrl: 'icons/icon-48.png',
    title: 'Notification',
    message: 'Hello, World!',
  });
} else {
  // 显示提示
  alert('需要通知权限');
}
```

## 九、下一步

- [配置详解](https://wxt.dev/guide/essentials/configuration.html)：学习 WXT 配置
- [消息传递](https://wxt.dev/guide/essentials/messaging.html)：学习跨脚本通信
- [数据存储](https://wxt.dev/guide/essentials/storage.html)：学习数据存储
- [发布指南](https://wxt.dev/guide/essentials/publishing.html)：学习如何发布扩展
