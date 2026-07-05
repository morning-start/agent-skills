# 部署指南

本指南介绍如何构建、打包和发布 WXT 浏览器扩展到各大浏览器商店（Chrome、Firefox、Edge、Safari）。

## 官方导航链接

- [Publishing](https://wxt.dev/guide/essentials/publishing.html) - 扩展打包与应用商店发布流程
- [Testing Updates](https://wxt.dev/guide/essentials/testing-updates.html) - 扩展更新测试方法
- [Target Different Browsers](https://wxt.dev/guide/essentials/target-different-browsers.html) - 多浏览器适配方案

---

## 一、构建配置

### 1.1 构建命令

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

**在 package.json 中配置脚本：**

```json
{
  "scripts": {
    "build": "wxt build",
    "build:chrome": "wxt build -b chrome",
    "build:firefox": "wxt build -b firefox",
    "build:edge": "wxt build -b edge",
    "build:safari": "wxt build -b safari",
    "build:all": "wxt build && wxt build -b firefox && wxt build -b edge"
  }
}
```

### 1.2 构建选项

在 `wxt.config.ts` 中配置构建选项：

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  // 开发配置
  dev: {
    server: {
      port: 3000,
      strictPort: false,
    },
  },

  // 构建配置
  build: {
    // 生成 sourcemap
    sourcemap: true,

    // 压缩配置
    minify: 'esbuild', // 'esbuild' | 'terser'

    // Rollup 配置
    rollupOptions: {
      output: {
        // chunk 文件名
        chunkFileNames: 'chunks/[name]-[hash].js',
        // entry 文件名
        entryFileNames: 'entries/[name]-[hash].js',
        // asset 文件名
        assetFileNames: 'assets/[name]-[hash].[ext]',
      },
    },
  },

  // 多浏览器配置
  manifest: {
    // Chrome 专属配置
    chrome: {
      permissions: ['alarms', 'idle'],
    },

    // Firefox 专属配置
    firefox: {
      permissions: ['alarms'],
    },

    // Safari 专属配置
    safari: {
      permissions: ['alarms'],
    },
  },
});
```

### 1.3 构建输出

构建完成后，输出目录为 `.output/<browser>/`：

```
.output/
├── chrome/
│   ├── manifest.json
│   ├── background.js
│   ├── popup.html
│   ├── chunks/
│   └── assets/
├── firefox/
│   ├── manifest.json
│   └── ...
└── edge/
    ├── manifest.json
    └── ...
```

## 二、打包扩展

### 2.1 压缩打包

WXT 提供便捷的打包命令：

```bash
# 打包默认浏览器
bun run zip

# 打包特定浏览器
bun run zip:chrome      # Chrome
bun run zip:firefox     # Firefox
bun run zip:edge        # Edge
bun run zip:safari      # Safari
```

**配置打包脚本：**

```json
{
  "scripts": {
    "zip": "wxt zip",
    "zip:chrome": "wxt zip -b chrome",
    "zip:firefox": "wxt zip -b firefox",
    "zip:edge": "wxt zip -b edge",
    "zip:safari": "wxt zip -b safari"
  }
}
```

打包后，在项目根目录生成 `<browser>-<version>.zip` 文件。

### 2.2 手动打包（高级）

如果需要更精细的控制，可以手动打包：

```bash
# 构建扩展
bun run build:chrome

# 进入构建目录
cd .output/chrome

# 手动打包
zip -r ../../my-extension-v1.0.0.zip .
```

### 2.3 打包内容验证

解压 .zip 文件，确保包含以下内容：

```
my-extension-v1.0.0.zip
├── manifest.json        # ✓ 必需
├── background.js        # ✓ 如有后台脚本
├── content/             # ✓ 如有内容脚本
├── popup.html           # ✓ 如有弹出页面
├── options.html         # ✓ 如有选项页面
├── icons/               # ✓ 图标资源
├── _locales/            # ✓ 如有国际化
└── assets/              # ✓ 其他资源
```

## 三、Chrome Web Store 发布

### 3.1 准备工作

**开发者账户：**

1. 访问 https://chrome.google.com/webstore/dev
2. 注册开发者账户
3. 支付一次性注册费（5 美元）

**图标资源准备：**

```
icons/
├── icon-16.png   # 16x16, 用于扩展管理页
├── icon-48.png   # 48x48, 用于扩展管理页
├── icon-128.png  # 128x128, 用于 Chrome 网上应用店
└── icon-256.png  # 256x256, 用于 Chrome 网上应用店
```

### 3.2 创建新项目

1. 登录 Chrome Web Store Developer Dashboard
2. 点击 "新增项目" 按钮
3. 上传打包的 .zip 文件
4. 填写商店信息

**必填信息：**

| 项目 | 说明 | 要求 |
|------|------|------|
| 项目信息 | 扩展名称、描述 | 详细的描述，不超过 132 字符 |
| 类目 | 扩展分类 | 选择合适的分类 |
| 语言 | 支持语言 | 选择扩展支持的语言 |
| 图标 | 扩展图标 | 128x128 PNG 格式 |
| 屏幕截图 | 功能演示截图 | 1280x800 或 640x400 PNG 格式，至少 1 张，最多 5 张 |
| 隐私 | 隐权政策 URL | 如果扩展收集数据，必须提供 |

### 3.3 填写隐私信息

Chrome 要求所有扩展提供隐私声明：

1. 在 Google 表单中填写隐私信息
2. 说明扩展如何使用数据
3. 说明是否收集用户数据
4. 提供隐私政策 URL（如果收集数据）

### 3.4 审核流程

**提交审核：**

1. 完成所有必填信息
2. 点击 "提交审核" 按钮
3. 等待审核（通常 2-5 个工作日）

**审核要点：**

- ✓ 扩展功能描述与实际功能一致
- ✓ 无恶意代码
- ✓ 符合 Chrome 扩展政策
- ✓ 用户隐私得到保护
- ✓ 界面友好、无错误

**审核失败：**

如果审核失败，会收到失败原因，修正后重新提交。

### 3.5 更新扩展

**版本更新：**

```json
// package.json
{
  "version": "1.0.1"
}
```

```typescript
// wxt.config.ts
export default defineConfig({
  manifest: {
    version: '1.0.1',
  },
});
```

**更新流程：**

1. 更新版本号
2. 构建新版本
3. 打包新版本
4. 上传到 Chrome Web Store
5. 填写更新说明
6. 提交审核

## 四、Firefox Add-ons 发布

### 4.1 准备工作

**开发者账户：**

1. 访问 https://addons.mozilla.org/developers/
2. 注册开发者账户
3. 验证邮箱

**账户类型：**

- **免费账户**：适合个人开发者
- **付费账户**：适合企业（可选）

### 4.2 创建新项目

1. 登录 Firefox Add-ons Developer Hub
2. 点击 "提交新扩展"
3. 上传打包的 .zip 文件

### 4.3 填写项目信息

**必填信息：**

| 项目 | 说明 | 要求 |
|------|------|------|
| 名称 | 扩展名称 | 唯一，不能重复 |
| 描述 | 扩展描述 | 详细的描述 |
| 类别 | 扩展分类 | 选择合适的分类 |
| 图标 | 扩展图标 | 32x32, 64x64, 128x128 PNG 格式 |
| 屏幕截图 | 功能演示截图 | 至少 1 张，最多 5 张 |

### 4.4 Firefox 特殊要求

Firefox 有一些特殊要求：

**manifest.json：**

Firefox 要求 `manifest_version: 3` 和 `browser_specific_settings` 字段：

```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0.0",
  "browser_specific_settings": {
    "gecko": {
      "id": "my-extension@example.com",
      "strict_min_version": "102.0"
    }
  }
}
```

**WXT 自动处理：**

WXT 会自动为 Firefox 生成正确的 `browser_specific_settings` 配置。

### 4.5 审核流程

**提交审核：**

1. 完成所有必填信息
2. 点击 "提交审核" 按钮
3. 等待审核（通常 1-3 个工作日）

**审核要点：**

- ✓ 扩展功能描述与实际功能一致
- ✓ 无恶意代码
- ✓ 符合 Firefox 扩展政策
- ✓ 代码质量高
- ✓ 用户界面友好

### 4.6 更新扩展

更新流程与 Chrome 类似：

1. 更新版本号
2. 构建新版本
3. 打包新版本
4. 上传到 Firefox Add-ons
5. 填写更新说明
6. 提交审核

## 五、Microsoft Edge Add-ons 发布

### 5.1 准备工作

**开发者账户：**

1. 访问 https://partner.microsoft.com/dashboard
2. 注册 Microsoft 开发者账户
3. 支付注册费（19 美元，可选）

### 5.2 发布流程

Edge Add-ons 发布流程与 Chrome 类似：

1. 登录 Microsoft Partner Center
2. 创建新扩展
3. 上传打包的 .zip 文件
4. 填写商店信息
5. 提交审核

### 5.3 Edge 特殊要求

Edge 基于 Chromium，与 Chrome 兼容性好，但有一些特殊要求：

**manifest.json：**

Edge 不需要特殊的 manifest 配置，使用 Chrome 的 manifest 即可。

**图标要求：**

Edge 要求提供完整的图标集：

```
icons/
├── icon-16.png
├── icon-32.png
├── icon-48.png
├── icon-64.png
└── icon-128.png
```

## 六、Safari App Store 发布

### 6.1 准备工作

**Apple 开发者账户：**

1. 访问 https://developer.apple.com/
2. 注册 Apple 开发者账户
3. 支付年费（99 美元）

**设备要求：**

- macOS 设备
- Xcode（用于构建和签名）

### 6.2 构建版本化

Safari 扩展需要特殊配置。

**注意：** WXT 对 Safari 支持有限，需要手动调整。

**推荐方案：**

使用专门支持 Safari 的框架，如：

- **Xcode Extension Builder**
- **Parasite**

### 6.3 发布流程

Safari App Store 发布流程与其他平台不同：

1. 在 Xcode 中创建扩展项目
2. 配置扩展功能
3. 生成 .appex 文件
4. 在 App Store Connect 中创建应用
5. 上传扩展
6. 提交审核

### 6.4 Safari 特殊要求

**代码签名：**

所有 Safari 扩展必须使用 Apple 代码签名：

```bash
codesign --force --sign "Developer ID Application: Your Name" MyExtension.appex
```

**权限配置：**

Safari 扩展需要明确声明权限：

```json
{
  "com.apple.security.app-sandbox": true,
  "com.apple.security.network.client": true
}
```

## 七、自动化部署

### 7.1 GitHub Actions

使用 GitHub Actions 自动化构建和发布：

```yaml
# .github/workflows/release.yml
name: Release Extension

on:
  push:
    tags:
      - 'v*'

jobs:
  build-and-release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1
        with:
          bun-version: latest

      - name: Install dependencies
        run: bun install

      - name: Build extension
        run: |
          bun run build:chrome
          bun run build:firefox

      - name: Zip extension
        run: |
          bun run zip:chrome
          bun run zip:firefox

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            chrome-*.zip
            firefox-*.zip
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 7.2 发布到 Chrome Web Store

使用 Chrome Web Store API 自动发布：

```typescript
// scripts/publish-chrome.ts
import { webstoreUpload } from 'chrome-webstore-upload';

const accessToken = process.env.CHROME_ACCESS_TOKEN;
const extensionId = process.env.CHROME_EXTENSION_ID;
const zipPath = 'chrome-1.0.0.zip';

await webstoreUpload({
  extensionId,
  accessToken,
  zipPath,
});
```

### 7.3 发布到 Firefox Add-ons

使用 Firefox Add-ons API 自动发布：

```typescript
// scripts/publish-firefox.ts
import { submit } from 'addons-linter';

const jwtCredentials = process.env.FIREFOX_JWT_CREDENTIALS;
const zipPath = 'firefox-1.0.0.zip';

await submit({
  jwtCredentials,
  zipPath,
  source: null,
});
```

## 八、发布前检查清单

### 8.1 通用检查

- [ ] 版本号已更新
- [ ] manifest.json 配置正确
- [ ] 所有图标资源完整
- [ ] 屏幕截图清晰美观
- [ ] 扩展描述详细准确
- [ ] 隐私政策 URL 有效（如需要）
- [ ] 扩展功能测试通过
- [ ] 多浏览器兼容性测试通过
- [ ] 无控制台错误或警告

### 8.2 Chrome 特定检查

- [ ] Chrome 权限声明最小化
- [ ] Chrome Web Store 政策符合
- [ ] 隐私信息完整填写
- [ ] 支付注册费（5 美元）

### 8.3 Firefox 特定检查

- [ ] Firefox 权限声明最小化
- [ ] Firefox 扩展政策符合
- [ ] browser_specific_settings 配置正确
- [ ] 开发者账户已验证

### 8.4 Edge 特定检查

- [ ] Edge 权限声明最小化
- [ ] Edge 扩展政策符合
- [ ] 图标资源完整
- [ ] Partner Center 账户已注册

### 8.5 Safari 特定检查

- [ ] Safari 权限声明最小化
- [ ] Safari 扩展政策符合
- [ ] 代码签名有效
- [ ] Apple 开发者账户已注册

## 九、常见问题

### Q1: 如何同时发布到多个浏览器？

**方法一：顺序发布**

1. 先发布到 Chrome（审核较快）
2. 再发布到 Firefox
3. 最后发布到 Edge

**方法二：并行发布**

使用 GitHub Actions 自动化构建和发布所有浏览器的版本。

### Q2: 审核失败怎么办？

**诊断步骤：**

1. 仔细阅读审核失败原因
2. 对照扩展政策逐项检查
3. 修正问题
4. 重新构建和打包
5. 重新提交审核

**常见失败原因：**

- 权限声明过多
- 扩展功能描述不准确
- 用户隐私未得到保护
- 代码质量问题
- 恶意行为

### Q3: 如何管理多个版本？

**版本号管理：**

遵循语义化版本规范：

- `1.0.0`：主版本（重大更新）
- `1.1.0`：次版本（功能更新）
- `1.1.1`：修订版本（Bug 修复）

**发布策略：**

- 使用 Git 标签标记版本
- 使用 GitHub Releases 归档版本
- 在商店中维护多个版本

### Q4: 如何快速回滚？

**Chrome：**

1. 在 Developer Dashboard 中
2. 选择旧版本
3. 点击 "发布" 按钮

**Firefox：**

1. 在 Developer Hub 中
2. 选择旧版本
3. 点击 "发布" 按钮

**Edge：**

1. 在 Partner Center 中
2. 选择旧版本
3. 点击 "发布" 按钮

### Q5: 如何处理用户反馈？

**收集反馈：**

- 商店评分和评论
- GitHub Issues
- 用户邮件

**响应策略：**

1. 及时响应用户反馈
2. 记录 Bug 和功能请求
3. 定期发布更新
4. 改进用户体验

## 十、下一步

- [命令参考](../cli/commands.md)：掌握开发和构建命令
- [构建阶段](../lifecycle/phases.md)：了解构建流程
- [入口点 API](../api/entrypoints.md)：学习核心 API
- [示例代码](../examples/)：查看完整项目示例
