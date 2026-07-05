# 浏览器适配指南

本指南详细介绍 WXT 如何适配不同浏览器（Chrome、Firefox、Edge、Safari），包括兼容性配置、特殊功能和最佳实践。

## 官方导航链接

- [Target Different Browsers](https://wxt.dev/guide/essentials/target-different-browsers.html) - 多浏览器适配方案
- [Browser Startup](https://wxt.dev/guide/essentials/config/browser-startup.html) - 浏览器启动相关配置
- [Content Scripts](https://wxt.dev/guide/essentials/content-scripts.html) - 内容脚本开发与注入规则
- [Extension APIs](https://wxt.dev/guide/essentials/extension-apis.html) - 浏览器扩展 API 调用与适配

---

## 一、浏览器支持概览

### 1.1 支持的浏览器

WXT 原生支持以下浏览器：

| 浏览器 | 支持状态 | 版本要求 | 特殊配置 |
|--------|----------|----------|----------|
| **Chrome** | ✅ 完全支持 | 88+ | 标准配置 |
| **Firefox** | ✅ 完全支持 | 102+ | 需要特定配置 |
| **Edge** | ✅ 完全支持 | 88+ | 标准配置 |
| **Safari** | ⚠️ 部分支持 | 16+ | 需要特殊工具 |

### 1.2 兼容性对比

| 功能 | Chrome | Firefox | Edge | Safari |
|------|--------|---------|------|--------|
| Manifest V3 | ✅ | ✅ | ✅ | ⚠️ |
| Service Worker | ✅ | ✅ | ✅ | ❌ |
| 内容脚本 | ✅ | ✅ | ✅ | ✅ |
| 存储API | ✅ | ✅ | ✅ | ✅ |
| 脚本注入 | ✅ | ✅ | ✅ | ✅ |
| 侧边栏 | ❌ | ✅ | ❌ | ✅ |
| 开发者工具 | ✅ | ✅ | ✅ | ❌ |

## 二、构建不同浏览器版本

### 2.1 构建命令

WXT 支持构建到不同浏览器：

```bash
# 构建默认浏览器（Chrome）
bun run build

# 构建特定浏览器
bun run build:chrome      # Chrome
bun run build:firefox     # Firefox
bun run build:edge        # Edge
bun run build:safari      # Safari

# 构建所有浏览器
bun run build:all         # 需要配置
```

**配置 package.json 脚本：**

```json
{
  "scripts": {
    "build": "wxt build",
    "build:chrome": "wxt build -b chrome",
    "build:firefox": "wxt build -b firefox",
    "build:edge": "wxt build -b edge",
    "build:safari": "wxt build -b safari"
  }
}
```

### 2.2 开发不同浏览器

```bash
# Chrome 开发
bun run dev

# Firefox 开发
bun run dev:firefox

# Edge 开发
bun run dev:edge

# Safari 开发
bun run dev:safari
```

### 2.3 打包不同浏览器

```bash
# 打包 Chrome
bun run zip:chrome

# 打包 Firefox
bun run zip:firefox

# 打包 Edge
bun run zip:edge

# 打包 Safari
bun run zip:safari
```

## 三、Chrome 适配

### 3.1 标准 Chrome 配置

Chrome 使用标准 Manifest V3 配置：

```typescript
// wxt.config.ts
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: 'My Extension',
    version: '1.0.0',

    // Chrome 标准权限
    permissions: [
      'storage',
      'tabs',
      'activeTab',
      'scripting',
    ],

    // Chrome 主机权限
    host_permissions: [
      'https://api.example.com/*',
    ],

    // Chrome 专属权限
    chrome: {
      permissions: ['alarms', 'idle'],
    },
  },
});
```

### 3.2 Chrome 特殊功能

#### Chrome API

```typescript
// 使用 Chrome 专属 API
import { defineBackground } from 'wxt/sandbox';

export default defineBackground(() => {
  // Chrome 空闲检测
  chrome.idle.setDetectionInterval(60);

  chrome.idle.onStateChanged.addListener((state) => {
    console.log('Idle state:', state);
  });

  // Chrome 警报
  chrome.alarms.create('check-updates', {
    periodInMinutes: 60,
  });

  chrome.alarms.onAlarm.addListener((alarm) => {
    console.log('Alarm:', alarm.name);
  });
});
```

#### Chrome 特定 manifest 字段

```typescript
export default defineConfig({
  manifest: {
    // Chrome 操作（浏览器按钮）
    action: {
      default_title: 'My Extension',
      default_popup: 'popup.html',
      default_icon: {
        16: 'icons/icon-16.png',
        32: 'icons/icon-32.png',
        48: 'icons/icon-48.png',
        128: 'icons/icon-128.png',
      },
    },

    // Chrome 特定权限
    permissions: ['alarms', 'idle'],
  },
});
```

### 3.3 Chrome 发布

**Chrome Web Store 发布流程：**

1. 注册开发者账户（5 美元）
2. 上传 .zip 文件
3. 填写商店信息
4. 提交审核（2-5 个工作日）

详细步骤：参见 [部署指南](../guides/deployment.md#chrome-web-store-发布)

## 四、Firefox 适配

### 4.1 Firefox 特定配置

Firefox 需要 `browser_specific_settings` 字段：

```typescript
// wxt.config.ts
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: 'My Extension',
    version: '1.0.0',

    // Firefox 特定配置
    firefox: {
      permissions: ['alarms'],
      browser_specific_settings: {
        gecko: {
          // 扩展 ID（必需）
          id: 'my-extension@example.com',

          // 最低 Firefox 版本
          strict_min_version: '102.0',

          // 推荐 Firefox 版本
          strict_max_version: '*',
        },
      },
    },
  },
});
```

### 4.2 Firefox 专属功能

#### Firefox 侧边栏

```typescript
// wxt.config.ts
export default defineConfig({
  manifest: {
    // Firefox 侧边栏（仅 Firefox 支持）
    sidebar_action: {
      default_panel: 'sidebar.html',
      default_title: 'My Sidebar',
      default_icon: {
        16: 'icons/icon-16.png',
        32: 'icons/icon-32.png',
        48: 'icons/icon-48.png',
      },
    },
  },
});
```

**侧边栏入口点（sidebar.html）：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Sidebar</title>
</head>
<body>
  <h1>Firefox Sidebar</h1>
  <script type="module" src="./sidebar.ts"></script>
</body>
</html>
```

**侧边栏逻辑（sidebar.ts）：**

```typescript
import { defineSidebar } from 'wxt/sandbox';

export default defineSidebar(() => {
  console.log('Sidebar loaded');

  // 监听当前标签页变化
  browser.tabs.onActivated.addListener((activeInfo) => {
    console.log('Tab activated:', activeInfo.tabId);
  });
});
```

#### Firefox 开发者工具

```typescript
// devtools.ts
import { defineDevTools } from 'wxt/sandbox';

export default defineDevTools(() => {
  console.log('DevTools panel created');

  // 创建 DevTools 面板
  browser.devtools.panels.create(
    'My Panel',
    'icons/icon-16.png',
    'devtools-panel.html'
  );
});
```

### 4.3 Firefox API 差异

Firefox 使用 `browser` API，而不是 `chrome` API：

```typescript
// ✅ 正确：使用 browser API（跨浏览器兼容）
browser.storage.local.set({ key: 'value' });

// ✅ 正确：使用 browser API（Firefox 推荐）
browser.runtime.sendMessage({ type: 'HELLO' });

// ❌ 错误：在 Firefox 中使用 chrome API（不兼容）
chrome.storage.local.set({ key: 'value' });
```

**WXT 自动处理：**

WXT 会自动将 `browser` API 转换为 `chrome` API（在 Chrome 中），因此推荐始终使用 `browser` API。

### 4.4 Firefox 发布

**Firefox Add-ons 发布流程：**

1. 注册开发者账户（免费）
2. 上传 .zip 文件
3. 填写商店信息
4. 提交审核（1-3 个工作日）

详细步骤：参见 [部署指南](../guides/deployment.md#firefox-add-ons-发布)

## 五、Edge 适配

### 5.1 Edge 配置

Edge 基于 Chromium，与 Chrome 高度兼容：

```typescript
// wxt.config.ts
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: 'My Extension',
    version: '1.0.0',

    // Edge 特定配置
    edge: {
      permissions: ['alarms'],
    },
  },
});
```

### 5.2 Edge 特殊功能

Edge 大部分功能与 Chrome 兼容，无需特殊处理。

**Edge 独有功能：**

```typescript
// Edge 集合（Edge Collections）
if (browser.edgeCollections) {
  browser.edgeCollections.create({
    name: 'My Collection',
  });
}
```

### 5.3 Edge 发布

**Microsoft Edge Add-ons 发布流程：**

1. 注册 Microsoft 开发者账户（19 美元，可选）
2. 上传 .zip 文件
3. 填写商店信息
4. 提交审核（1-3 个工作日）

详细步骤：参见 [部署指南](../guides/deployment.md#microsoft-edge-add-ons-发布)

## 六、Safari 适配

### 6.1 Safari 特殊性

Safari 扩展与其他浏览器有显著差异：

- **不支持 Manifest V3**：仅支持 Manifest V2
- **需要 Xcode**：必须使用 Xcode 构建
- **需要代码签名**：必须使用 Apple 开发者证书签名
- **不同的构建流程**：不能直接使用 WXT 构建

### 6.2 Safari 替代方案

**推荐使用 Safari Web Extension Converter：**

```bash
# 转换 Chrome 扩展为 Safari 扩展
xcrun safari-web-extension-converter /path/to/chrome-extension
```

**转换流程：**

1. 构建 Chrome 版本
2. 使用转换工具转换为 Xcode 项目
3. 在 Xcode 中配置和构建
4. 使用 Apple 开发者账户签名
5. 发布到 Safari App Store

### 6.3 Safari 专属功能

**Safari 侧边栏：**

```typescript
// Safari 侧边栏配置
export default defineConfig({
  manifest: {
    safari: {
      sidebar_action: {
        default_panel: 'sidebar.html',
      },
    },
  },
});
```

**Safari 开发者工具：**

Safari 不支持扩展开发者工具面板。

### 6.4 Safari 发布

**Safari App Store 发布流程：**

1. 注册 Apple 开发者账户（99 美元/年）
2. 使用 Xcode 构建 Safari 扩展
3. 代码签名
4. 上传到 App Store Connect
5. 提交审核（1-2 周）

详细步骤：参见 [部署指南](../guides/deployment.md#safari-app-store-发布)

## 七、跨浏览器配置

### 7.1 条件配置

根据浏览器动态配置：

```typescript
// wxt.config.ts
import { defineConfig } from 'wxt';

export default defineConfig(({ browser }) => ({
  manifest: {
    name: 'My Extension',
    version: '1.0.0',

    // 根据浏览器添加不同权限
    permissions: ['storage', 'tabs'],

    // Chrome 特定权限
    ...(browser === 'chrome' ? {
      chrome: {
        permissions: ['alarms', 'idle'],
      },
    } : {}),

    // Firefox 特定配置
    ...(browser === 'firefox' ? {
      firefox: {
        permissions: ['alarms'],
        browser_specific_settings: {
          gecko: {
            id: 'my-extension@example.com',
            strict_min_version: '102.0',
          },
        },
      },
    } : {}),
  },
}));
```

### 7.2 浏览器检测

**在运行时检测浏览器：**

```typescript
import { defineBackground } from 'wxt/sandbox';

export default defineBackground(() => {
  // 检测浏览器
  if (typeof browser !== 'undefined') {
    // 使用 browser API（Firefox、Edge、Safari）
    console.log('Using browser API');
  } else if (typeof chrome !== 'undefined') {
    // 使用 chrome API（Chrome）
    console.log('Using chrome API');
  }

  // 检测特定浏览器
  if (browser.runtime.getURL('').includes('moz-extension://')) {
    console.log('Firefox');
  } else if (browser.runtime.getURL('').includes('chrome-extension://')) {
    console.log('Chrome or Edge');
  }
});
```

### 7.3 API 兼容性封装

**创建浏览器兼容层：**

```typescript
// utils/browser.ts

export const browserAPI = typeof browser !== 'undefined' ? browser : chrome;

export function sendMessage(message: any): Promise<any> {
  return browserAPI.runtime.sendMessage(message);
}

export function storageGet(keys: string | string[] | null): Promise<any> {
  return browserAPI.storage.local.get(keys);
}

export function storageSet(data: object): Promise<void> {
  return browserAPI.storage.local.set(data);
}
```

**使用兼容层：**

```typescript
import { sendMessage, storageGet, storageSet } from './utils/browser';

export default defineBackground(() => {
  // 使用兼容层
  sendMessage({ type: 'HELLO' });
  storageGet(['key']).then((data) => console.log(data));
  storageSet({ key: 'value' });
});
```

## 八、浏览器特定 manifest 覆盖

### 8.1 使用覆盖配置

为不同浏览器提供不同的 manifest 配置：

```typescript
// wxt.config.ts
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: 'My Extension',
    version: '1.0.0',

    // 默认配置
    permissions: ['storage', 'tabs'],
  },

  // Chrome 覆盖配置
  manifest: {
    chrome: {
      name: 'My Extension (Chrome)',
      permissions: ['alarms', 'idle'],
    },
  },

  // Firefox 覆盖配置
  manifest: {
    firefox: {
      name: 'My Extension (Firefox)',
      permissions: ['alarms'],
      browser_specific_settings: {
        gecko: {
          id: 'my-extension@example.com',
        },
      },
    },
  },
});
```

### 8.2 使用公共配置文件

**使用 manifest-overrides 目录：**

```
public/manifest-overrides/
├── chrome.json
├── firefox.json
├── edge.json
└── safari.json
```

**chrome.json：**

```json
{
  "name": "My Extension (Chrome)",
  "permissions": ["alarms", "idle"]
}
```

**firefox.json：**

```json
{
  "name": "My Extension (Firefox)",
  "permissions": ["alarms"],
  "browser_specific_settings": {
    "gecko": {
      "id": "my-extension@example.com"
    }
  }
}
```

WXT 会自动合并这些配置文件。

## 九、常见浏览器兼容性问题

### 9.1 API 不一致

**问题：** 某些 API 在不同浏览器中表现不一致。

**解决方案：** 使用 polyfill 或条件检查。

```typescript
// 检查 API 是否存在
if (browserAPI.storage?.sync) {
  // 使用 sync storage
  browserAPI.storage.sync.set({ key: 'value' });
} else {
  // 回退到 local storage
  browserAPI.storage.local.set({ key: 'value' });
}
```

### 9.2 权限差异

**问题：** 不同浏览器支持的权限不同。

**解决方案：** 使用最小权限原则，并检查权限是否可用。

```typescript
// 检查权限
if (browserAPI.permissions?.contains) {
  browserAPI.permissions.contains({
    permissions: ['alarms'],
  }).then((result) => {
    if (result) {
      console.log('Alarms permission granted');
    } else {
      console.log('Alarms permission not granted');
    }
  });
}
```

### 9.3 Manifest 版本差异

**问题：** Chrome/Firefox 使用 Manifest V3，Safari 使用 Manifest V2。

**解决方案：** 构建不同版本，或使用 Safari Web Extension Converter。

### 9.4 Content Script 注入时机

**问题：** 不同浏览器中 Content Script 注入时机略有差异。

**解决方案：** 使用 `runAt: 'document_idle'`，这是最可靠的时机。

```typescript
export default defineContentScript({
  matches: ['<all_urls>'],
  runAt: 'document_idle', // 推荐使用
  main() {
    console.log('Content script injected');
  },
});
```

## 十、最佳实践

### 10.1 使用 browser API

始终使用 `browser` API，而不是 `chrome` API：

```typescript
// ✅ 正确
browser.runtime.sendMessage({ type: 'HELLO' });

// ❌ 错误（不兼容 Firefox）
chrome.runtime.sendMessage({ type: 'HELLO' });
```

### 10.2 最小权限原则

仅请求必要的权限：

```typescript
export default defineConfig({
  manifest: {
    // ✅ 正确：仅请求必要的权限
    permissions: ['storage'],

    // ❌ 错误：请求过多权限
    permissions: ['<all_urls>'],
  },
});
```

### 10.3 测试所有浏览器

确保在所有目标浏览器中测试：

```bash
# 测试 Chrome
bun run dev

# 测试 Firefox
bun run dev:firefox

# 测试 Edge
bun run dev:edge
```

### 10.4 使用浏览器前缀 API

对于实验性功能，使用浏览器前缀 API：

```typescript
// 检查 API 是否存在
if (browserAPI.experimental?.someFeature) {
  browserAPI.experimental.someFeature();
}
```

### 10.5 处理 API 不可用

使用 try-catch 处理 API 不可用的情况：

```typescript
try {
  const result = await browserAPI.someAPI();
  console.log('Result:', result);
} catch (error) {
  console.error('API not supported:', error);
  // 回退方案
}
```

## 十一、常见问题

### Q1: 如何同时支持 Chrome 和 Firefox？

**方法：**

1. 使用 `browser` API（跨浏览器兼容）
2. 使用条件配置（`wxt.config.ts`）
3. 测试两个浏览器

```typescript
export default defineConfig(({ browser }) => ({
  manifest: {
    name: 'My Extension',
    version: '1.0.0',
    permissions: ['storage'],

    // Firefox 特定配置
    ...(browser === 'firefox' ? {
      firefox: {
        browser_specific_settings: {
          gecko: {
            id: 'my-extension@example.com',
          },
        },
      },
    } : {}),
  },
}));
```

### Q2: Safari 扩展如何构建？

**方法：**

1. 构建 Chrome 版本
2. 使用 `xcrun safari-web-extension-converter` 转换
3. 在 Xcode 中构建和签名

**详细步骤：**

```bash
# 1. 构建 Chrome 版本
bun run build:chrome

# 2. 转换为 Safari 扩展
xcrun safari-web-extension-converter .output/chrome

# 3. 在 Xcode 中构建和签名
# 打开生成的 Xcode 项目并构建
```

### Q3: 如何检测当前浏览器？

**方法：**

```typescript
// 检测浏览器类型
const userAgent = navigator.userAgent;

if (userAgent.includes('Firefox')) {
  console.log('Firefox');
} else if (userAgent.includes('Edg')) {
  console.log('Edge');
} else if (userAgent.includes('Chrome')) {
  console.log('Chrome');
} else if (userAgent.includes('Safari')) {
  console.log('Safari');
}
```

**在扩展中检测：**

```typescript
// 检测扩展 URL
const extensionURL = browser.runtime.getURL('');

if (extensionURL.includes('moz-extension://')) {
  console.log('Firefox');
} else if (extensionURL.includes('chrome-extension://')) {
  console.log('Chrome or Edge');
} else if (extensionURL.includes('safari-web-extension://')) {
  console.log('Safari');
}
```

### Q4: 如何处理浏览器 API 差异？

**方法：**

使用 polyfill 或条件检查：

```typescript
// 创建浏览器兼容层
export const browserAPI = typeof browser !== 'undefined' ? browser : chrome;

// 使用兼容层
export function sendMessage(message: any) {
  return browserAPI.runtime.sendMessage(message);
}
```

### Q5: 如何构建所有浏览器版本？

**方法：**

使用脚本批量构建：

```bash
# 构建 Chrome
bun run build:chrome

# 构建 Firefox
bun run build:firefox

# 构建 Edge
bun run build:edge

# 打包所有版本
bun run zip:chrome
bun run zip:firefox
bun run zip:edge
```

**或使用 npm-run-all：**

```bash
# 安装 npm-run-all
bun i -D npm-run-all

# 并行构建所有浏览器
bun run build:all

# 在 package.json 中配置
{
  "scripts": {
    "build:all": "npm-run-all build:chrome build:firefox build:edge"
  }
}
```

## 十二、下一步

- [框架配置](../guides/framework-setup.md)：学习各框架的配置方法
- [部署指南](../guides/deployment.md)：学习如何发布到各浏览器商店
- [命令参考](../cli/commands.md)：掌握开发和构建命令
- [示例代码](../../examples/)：查看完整项目示例
- [入口点 API](../../api/entrypoints.md)：学习入口点 API
