# CLI 命令参考

本文档详细说明 WXT 支持的所有 CLI 命令，包括命令参数、使用示例和最佳实践。

## 官方导航链接

- [wxt](https://wxt.dev/api/cli/wxt.html) - WXT 核心CLI命令入口
- [wxt build](https://wxt.dev/api/cli/wxt-build.html) - 构建命令
- [wxt zip](https://wxt.dev/api/cli/wxt-zip.html) - 压缩打包命令
- [wxt prepare](https://wxt.dev/api/cli/wxt-prepare.html) - 预处理命令
- [wxt clean](https://wxt.dev/api/cli/wxt-clean.html) - 清理命令
- [wxt init](https://wxt.dev/api/cli/wxt-init.html) - 初始化命令
- [wxt submit](https://wxt.dev/api/cli/wxt-submit.html) - 扩展提交命令
- [wxt submit init](https://wxt.dev/api/cli/wxt-submit-init.html) - 提交初始化命令

---

## 命令概览

| 命令 | 说明 | 常用参数 |
|------|------|----------|
| `wxt` | 核心CLI命令入口 | `--help`, `--version` |
| `wxt build` | 构建项目 | `-b`, `--mode`, `--watch` |
| `wxt zip` | 压缩打包 | `-b`, `--browser` |
| `wxt prepare` | 预处理项目 | `--force` |
| `wxt clean` | 清理构建产物 | `--all` |
| `wxt init` | 初始化新项目 | `-t`, `--package-manager` |
| `wxt submit` | 提交到应用商店 | `--target` |
| `wxt submit init` | 初始化提交配置 | `--target` |

---

## 一、wxt build

### 1.1 命令说明

`wxt build` 命令用于构建 WXT 扩展项目，生成可运行的扩展产物。

### 1.2 基本用法

```bash
# 构建默认浏览器（Chrome）
wxt build

# 构建指定浏览器
wxt build -b chrome
wxt build -b firefox
wxt build -b edge
wxt build -b safari

# 构建所有配置的浏览器
wxt build --all-browsers

# 使用包管理器
bun run build
npm run build
pnpm build
yarn build
```

### 1.3 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-b, --browser` | 指定浏览器 | `-b chrome` |
| `--mode` | 构建模式 | `--mode production` |
| `--watch` | 监听文件变化 | `--watch` |
| `-m, --minify` | 压缩代码 | `-m` |
| `--sourcemap` | 生成 source map | `--sourcemap` |
| `--analyze` | 分析构建产物 | `--analyze` |

### 1.4 使用示例

```bash
# 开发模式构建（不压缩）
wxt build --mode development

# 生产模式构建（压缩）
wxt build --mode production

# 监听模式（文件变化自动重新构建）
wxt build --watch

# 生成 source map
wxt build --sourcemap

# 分析构建产物
wxt build --analyze
```

### 1.5 配置示例

在 `package.json` 中配置脚本：

```json
{
  "scripts": {
    "build": "wxt build",
    "build:chrome": "wxt build -b chrome",
    "build:firefox": "wxt build -b firefox",
    "build:all": "wxt build --all-browsers",
    "build:watch": "wxt build --watch",
    "build:dev": "wxt build --mode development",
    "build:prod": "wxt build --mode production"
  }
}
```

---

## 二、wxt zip

### 2.1 命令说明

`wxt zip` 命令用于将构建后的扩展项目压缩打包，适配浏览器应用商店发布要求。

### 2.2 基本用法

```bash
# 压缩默认浏览器
wxt zip

# 压缩指定浏览器
wxt zip -b chrome
wxt zip -b firefox

# 使用包管理器
bun run zip
npm run zip
```

### 2.3 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-b, --browser` | 指定浏览器 | `-b chrome` |
| `--filename` | 指定输出文件名 | `--filename extension.zip` |
| `--outDir` | 指定输出目录 | `--outDir dist` |

### 2.4 使用示例

```bash
# 压缩 Chrome 版本
wxt zip -b chrome

# 压缩所有浏览器版本
wxt zip --all-browsers

# 自定义输出文件名
wxt zip --filename my-extension-v1.0.0.zip

# 指定输出目录
wxt zip --outDir releases
```

### 2.5 配置示例

```json
{
  "scripts": {
    "zip": "wxt zip",
    "zip:chrome": "wxt zip -b chrome",
    "zip:firefox": "wxt zip -b firefox",
    "zip:all": "wxt zip --all-browsers",
    "zip:release": "wxt zip --filename my-extension-$npm_package_version.zip"
  }
}
```

---

## 三、wxt prepare

### 3.1 命令说明

`wxt prepare` 命令用于预处理项目，准备构建环境，包括初始化配置、安装依赖等。

### 3.2 基本用法

```bash
# 预处理项目
wxt prepare

# 强制重新预处理
wxt prepare --force

# 使用包管理器
bun run prepare
npm run prepare
```

### 3.3 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--force` | 强制重新预处理 | `--force` |

### 3.4 使用示例

```bash
# 标准预处理
wxt prepare

# 清理缓存后重新预处理
wxt clean && wxt prepare --force
```

### 3.5 自动执行

通常在 `package.json` 中配置为 postinstall 钩子：

```json
{
  "scripts": {
    "postinstall": "wxt prepare"
  }
}
```

---

## 四、wxt clean

### 4.1 命令说明

`wxt clean` 命令用于清理构建产物和临时文件，重置项目构建环境。

### 4.2 基本用法

```bash
# 清理构建产物
wxt clean

# 清理所有缓存和临时文件
wxt clean --all

# 使用包管理器
bun run clean
npm run clean
```

### 4.3 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--all` | 清理所有缓存和临时文件 | `--all` |

### 4.4 使用示例

```bash
# 仅清理构建产物
wxt clean

# 清理所有内容（包括缓存）
wxt clean --all

# 清理后重新构建
wxt clean --all && wxt build
```

### 4.5 配置示例

```json
{
  "scripts": {
    "clean": "wxt clean",
    "clean:all": "wxt clean --all",
    "rebuild": "wxt clean --all && wxt build"
  }
}
```

---

## 五、wxt init

### 5.1 命令说明

`wxt init` 命令用于快速创建新的 WXT 扩展项目，自动生成基础目录结构和配置文件。

### 5.2 基本用法

```bash
# 使用交互式创建
wxt init

# 直接指定项目名称
wxt init my-extension

# 使用模板创建
wxt init -t svelte my-extension
wxt init -t solid my-extension
```

### 5.3 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-t, --template` | 指定模板 | `-t svelte` |
| `--package-manager` | 指定包管理器 | `--package-manager bun` |
| `--no-install` | 跳过依赖安装 | `--no-install` |

### 5.4 使用示例

```bash
# 交互式创建（推荐）
wxt init

# 使用 Svelte 模板创建
wxt init -t svelte

# 使用 Solid 模板创建
wxt init -t solid

# 使用 Bun 作为包管理器
wxt init --package-manager bun

# 不安装依赖（手动安装）
wxt init --no-install
```

### 5.5 可用模板

| 模板 | 说明 | 推荐度 |
|------|------|--------|
| `vanilla` | 原生 JavaScript/TypeScript | ⭐⭐⭐ |
| `vue` | Vue 3 | ⭐⭐⭐⭐ |
| `react` | React | ⭐⭐⭐⭐ |
| `svelte` | Svelte | ⭐⭐⭐⭐⭐ |
| `solid` | SolidJS | ⭐⭐⭐⭐⭐ |

---

## 六、wxt submit

### 6.1 命令说明

`wxt submit` 命令用于将打包后的扩展提交到浏览器应用商店。

### 6.2 基本用法

```bash
# 提交到 Chrome Web Store
wxt submit --target chrome

# 提交到 Firefox Add-ons
wxt submit --target firefox

# 使用包管理器
bun run submit
npm run submit
```

### 6.3 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--target` | 指定目标商店 | `--target chrome` |
| `--zip` | 指定 zip 文件 | `--filename extension.zip` |

### 6.4 使用示例

```bash
# 提交到 Chrome Web Store
wxt submit --target chrome

# 提交到 Firefox Add-ons
wxt submit --target firefox

# 提交指定 zip 文件
wxt submit --target chrome --file my-extension.zip
```

### 6.5 配置示例

```json
{
  "scripts": {
    "submit": "wxt submit",
    "submit:chrome": "wxt submit --target chrome",
    "submit:firefox": "wxt submit --target firefox"
  }
}
```

---

## 七、wxt submit init

### 7.1 命令说明

`wxt submit init` 命令用于初始化扩展提交到应用商店所需的配置。

### 7.2 基本用法

```bash
# 初始化 Chrome Web Store 提交配置
wxt submit init --target chrome

# 初始化 Firefox Add-ons 提交配置
wxt submit init --target firefox
```

### 7.3 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--target` | 指定目标商店 | `--target chrome` |
| `--api-key` | API 密钥 | `--api-key YOUR_KEY` |
| `--client-id` | 客户端 ID | `--client-id YOUR_ID` |
| `--client-secret` | 客户端密钥 | `--client-secret YOUR_SECRET` |

### 7.4 使用示例

```bash
# 交互式初始化
wxt submit init

# 初始化 Chrome Web Store
wxt submit init --target chrome

# 初始化 Firefox Add-ons
wxt submit init --target firefox
```

---

## 八、完整配置示例

### 8.1 package.json 配置

```json
{
  "name": "my-extension",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "wxt",
    "dev:firefox": "wxt -b firefox",
    "build": "wxt build",
    "build:chrome": "wxt build -b chrome",
    "build:firefox": "wxt build -b firefox",
    "build:all": "wxt build --all-browsers",
    "build:watch": "wxt build --watch",
    "zip": "wxt zip",
    "zip:chrome": "wxt zip -b chrome",
    "zip:firefox": "wxt zip -b firefox",
    "zip:all": "wxt zip --all-browsers",
    "prepare": "wxt prepare",
    "clean": "wxt clean",
    "clean:all": "wxt clean --all",
    "rebuild": "wxt clean --all && wxt build",
    "postinstall": "wxt prepare"
  },
  "dependencies": {
    "wxt": "^0.20.0"
  }
}
```

### 8.2 开发流程

```bash
# 1. 创建新项目
wxt init -t svelte my-extension
cd my-extension

# 2. 启动开发服务器
bun run dev

# 3. 构建项目
bun run build

# 4. 压缩打包
bun run zip

# 5. 提交到应用商店（需要先配置）
bun run submit --target chrome
```

---

## 九、最佳实践

### 9.1 使用 Bun 作为包管理器

Bun 是 WXT 推荐的包管理器，速度更快。

```bash
# 安装 Bun（如果未安装）
curl -fsSL https://bun.sh/install | bash

# 使用 Bun 创建项目
bunx wxt init -t svelte

# 使用 Bun 运行命令
bun run dev
bun run build
bun run zip
```

### 9.2 环境变量配置

```bash
# .env.development
VITE_API_URL=https://dev.api.example.com

# .env.production
VITE_API_URL=https://api.example.com
```

```bash
# 构建不同环境
wxt build --mode development
wxt build --mode production
```

### 9.3 多浏览器构建

```bash
# 构建所有浏览器
wxt build --all-browsers

# 压缩所有浏览器版本
wxt zip --all-browsers
```

### 9.4 持续集成

```yaml
# .github/workflows/build.yml
name: Build Extension

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: oven-sh/setup-bun@v1
      - run: bun install
      - run: bun run build:all
      - run: bun run zip:all
```

---

## 十、常见问题

### 10.1 构建失败

```bash
# 清理缓存后重新构建
wxt clean --all
bun install
wxt build
```

### 10.2 端口占用

```bash
# 指定端口启动开发服务器
wxt --port 3001
```

### 10.3 浏览器未找到

```bash
# 确保目标浏览器已安装
# Windows: chrome --version
# macOS: /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
# Linux: google-chrome --version
```

### 10.4 权限错误

```bash
# Linux/Mac: 使用 sudo（不推荐）
sudo wxt build

# 推荐: 修复文件权限
chmod +x node_modules/.bin/wxt
```
