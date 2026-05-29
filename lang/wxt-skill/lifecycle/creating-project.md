# 创建项目指南

本指南详细介绍如何使用 WXT 创建新的浏览器扩展项目，包括命令行交互流程、配置选项和最佳实践。

## 一、创建方式

### 1.1 使用 bunx wxt（推荐）

使用 `bunx wxt` 命令可以快速创建 WXT 项目，无需全局安装。

```bash
# 创建新项目
bunx wxt@latest init
```

**优势：**
- 无需全局安装 WXT
- 始终使用最新版本
- 每个项目独立管理

### 1.2 交互式创建流程

运行 `bunx wxt@latest init` 后，会启动交互式创建流程：

#### 第一步：选择项目模板

```
? Select a template: (Use arrow keys)
❯ Vanilla
  Vue
  React
  Svelte
  Solid
```

**模板说明：**

| 模板 | 推荐度 | 特点 | 适用场景 |
|------|--------|------|----------|
| **Svelte** | ⭐⭐⭐⭐⭐ | 轻量、高性能、编译时优化 | 推荐首选 |
| **Solid** | ⭐⭐⭐⭐⭐ | 细粒度响应式、性能最佳 | 推荐首选 |
| **Vue** | ⭐⭐⭐⭐ | 生态成熟、中文文档丰富 | 熟悉 Vue 的开发者 |
| **React** | ⭐⭐⭐⭐ | 生态庞大、虚拟 DOM | 熟悉 React 的开发者 |
| **Vanilla** | ⭐⭐⭐ | 无框架、简单直接 | 简单扩展或无框架经验 |

**选择建议：**
- 新手或追求性能：选择 **Svelte** 或 **Solid**
- 已有 Vue 经验：选择 **Vue**
- 已有 React 经验：选择 **React**
- 简单项目：选择 **Vanilla**

#### 第二步：选择包管理器

```
? Select package manager: (Use arrow keys)
❯ bun       # 推荐
  npm
  pnpm
  yarn
```

**包管理器对比：**

| 特性 | Bun | npm | pnpm | Yarn |
|------|-----|-----|------|------|
| 速度 | 最快 | 慢 | 快 | 中等 |
| 磁盘占用 | 最小 | 最大 | 小 | 小 |
| 兼容性 | 好 | 标准 | 标准 | 标准 |
| 推荐度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**选择建议：** 优先选择 **Bun**，速度最快且磁盘占用最小。

#### 第三步：输入项目名称

```
? Project name: my-extension
```

**项目名称规范：**
- 使用小写字母、数字和连字符
- 不能包含空格或特殊字符
- 例如：`my-extension`、`weather-widget`、`url-shortener`

#### 第四步：确认创建项目

```
? Confirm project creation? (Y/n) y
```

输入 `y` 确认创建，或 `n` 取消。

### 1.3 自动化流程

WXT 会自动执行以下操作：

1. 创建项目目录结构
2. 生成配置文件（wxt.config.ts、tsconfig.json 等）
3. 生成示例代码（background.ts、popup.html 等）
4. 生成 package.json
5. 安装依赖
6. 提示启动开发服务器

## 二、创建后项目结构

### 2.1 标准项目结构

创建完成后，项目目录结构如下：

```
my-extension/
├── .output/              # 构建输出目录（自动生成）
├── entrypoints/          # 入口点目录（核心）
│   ├── background.ts     # 后台脚本
│   ├── content.ts        # 内容脚本
│   ├── popup.html        # 弹出页面
│   └── options.html      # 选项页面（可选）
├── public/               # 公共资源目录
│   ├── _locales/         # 国际化文件
│   ├── images/           # 图片资源
│   └── manifest-overrides/  # Manifest 覆盖配置
├── wxt.config.ts         # WXT 配置文件
├── package.json          # 项目配置
├── tsconfig.json         # TypeScript 配置
├── package-lock.json     # 依赖锁定文件
└── node_modules/         # 依赖包（自动生成）
```

### 2.2 不同框架的差异

**Svelte 项目结构：**

```
my-extension/
├── entrypoints/
│   ├── background.ts
│   ├── content.ts
│   ├── popup.html
│   ├── popup.ts          # Svelte 挂载脚本
│   ├── App.svelte        # Svelte 组件
│   ├── options.html
│   └── options.ts
├── wxt.config.ts
├── svelte.config.js      # Svelte 配置
└── package.json
```

**Solid 项目结构：**

```
my-extension/
├── entrypoints/
│   ├── background.ts
│   ├── content.ts
│   ├── popup.html
│   ├── popup.tsx         # Solid 挂载脚本
│   ├── App.tsx           # Solid 组件
│   ├── options.html
│   └── options.tsx
├── wxt.config.ts
└── package.json
```

**Vue 项目结构：**

```
my-extension/
├── entrypoints/
│   ├── background.ts
│   ├── content.ts
│   ├── popup.html
│   ├── popup.ts          # Vue 挂载脚本
│   ├── App.vue           # Vue 组件
│   ├── options.html
│   └── options.ts
├── wxt.config.ts
└── package.json
```

**React 项目结构：**

```
my-extension/
├── entrypoints/
│   ├── background.ts
│   ├── content.ts
│   ├── popup.html
│   ├── popup.tsx         # React 挂载脚本
│   ├── App.tsx           # React 组件
│   ├── options.html
│   └── options.tsx
├── wxt.config.ts
└── package.json
```

**Vanilla 项目结构：**

```
my-extension/
├── entrypoints/
│   ├── background.ts
│   ├── content.ts
│   ├── popup.html
│   ├── popup.ts          # 原生 JS
│   ├── options.html
│   └── options.ts
├── wxt.config.ts
└── package.json
```

## 三、创建后的配置文件

### 3.1 package.json

WXT 会自动生成 package.json 文件，包含以下脚本：

```json
{
  "name": "my-extension",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "wxt",
    "dev:firefox": "wxt -b firefox",
    "build": "wxt build",
    "build:firefox": "wxt build -b firefox",
    "zip": "wxt zip",
    "zip:firefox": "wxt zip -b firefox",
    "postinstall": "wxt prepare"
  },
  "devDependencies": {
    "wxt": "^0.17.0",
    "typescript": "^5.3.0"
  }
}
```

### 3.2 wxt.config.ts

WXT 会自动生成 wxt.config.ts 文件：

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: 'My Extension',
    description: 'A browser extension built with WXT',
    permissions: [],
  },
});
```

### 3.3 tsconfig.json

WXT 会自动生成 tsconfig.json 文件：

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "lib": ["ESNext", "DOM", "DOM.Iterable"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "types": ["wxt/client-types"]
  },
  "include": ["**/*.ts", "**/*.tsx", "**/*.svelte", "wxt.config.ts"]
}
```

## 四、启动开发服务器

### 4.1 启动命令

```bash
# 进入项目目录
cd my-extension

# 启动开发服务器（默认浏览器：Chrome）
bun run dev

# 启动 Firefox 开发
bun run dev:firefox
```

### 4.2 开发服务器行为

启动开发服务器后，WXT 会自动执行以下操作：

1. **编译源代码**
   - 编译 TypeScript 代码
   - 编译框架组件（Svelte、Vue、React、Solid）
   - 处理 CSS 和静态资源

2. **启动本地服务器**
   - 默认端口：3000
   - 自动打开浏览器
   - 安装开发版本扩展

3. **监听文件变化**
   - 文件修改后自动重新编译
   - 自动刷新扩展（HMR 热更新）
   - 无需手动重启

### 4.3 开发服务器选项

修改 `wxt.config.ts` 可以自定义开发服务器：

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  dev: {
    server: {
      // 指定端口
      port: 3000,

      // 严格模式（端口被占用时失败）
      strictPort: false,

      // 指定主机
      host: 'localhost',

      // 自动打开浏览器
      open: true,
    },

    // 浏览器类型
    browser: 'chrome', // 'chrome' | 'firefox' | 'edge' | 'safari'
  },
});
```

## 五、创建不同类型的项目

### 5.1 创建 Svelte 项目

```bash
bunx wxt@latest init
```

在交互式流程中选择：
1. 模板：**Svelte**
2. 包管理器：**bun**
3. 项目名称：`my-svelte-extension`

**生成的额外文件：**
- `svelte.config.js`：Svelte 配置
- `entrypoints/App.svelte`：Svelte 组件

### 5.2 创建 Solid 项目

```bash
bunx wxt@latest init
```

在交互式流程中选择：
1. 模板：**Solid**
2. 包管理器：**bun**
3. 项目名称：`my-solid-extension`

**生成的额外文件：**
- 无额外配置文件
- `entrypoints/App.tsx`：Solid 组件

### 5.3 创建 Vue 项目

```bash
bunx wxt@latest init
```

在交互式流程中选择：
1. 模板：**Vue**
2. 包管理器：**bun**
3. 项目名称：`my-vue-extension`

**生成的额外文件：**
- 无额外配置文件
- `entrypoints/App.vue`：Vue 组件

### 5.4 创建 React 项目

```bash
bunx wxt@latest init
```

在交互式流程中选择：
1. 模板：**React**
2. 包管理器：**bun**
3. 项目名称：`my-react-extension`

**生成的额外文件：**
- 无额外配置文件
- `entrypoints/App.tsx`：React 组件

### 5.5 创建 Vanilla 项目

```bash
bunx wxt@latest init
```

在交互式流程中选择：
1. 模板：**Vanilla**
2. 包管理器：**bun**
3. 项目名称：`my-vanilla-extension`

**生成的额外文件：**
- 无额外配置文件
- 无框架组件

## 六、手动创建项目（高级）

如果需要更多控制权，可以手动创建项目：

### 6.1 创建项目目录

```bash
mkdir my-extension
cd my-extension
```

### 6.2 初始化 package.json

```bash
bun init
```

或手动创建 `package.json`：

```json
{
  "name": "my-extension",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "wxt",
    "build": "wxt build",
    "zip": "wxt zip"
  }
}
```

### 6.3 安装 WXT

```bash
bun i -D wxt typescript
```

### 6.4 创建目录结构

```bash
mkdir -p entrypoints public
```

### 6.5 创建配置文件

**wxt.config.ts：**

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: 'My Extension',
    version: '1.0.0',
  },
});
```

**tsconfig.json：**

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "lib": ["ESNext", "DOM"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "types": ["wxt/client-types"]
  },
  "include": ["**/*.ts", "wxt.config.ts"]
}
```

### 6.6 创建入口点

**background.ts：**

```typescript
import { defineBackground } from 'wxt/sandbox';

export default defineBackground(() => {
  console.log('Background script started');
});
```

**popup.html：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Popup</title>
</head>
<body>
  <h1>Hello, WXT!</h1>
  <script type="module" src="./popup.ts"></script>
</body>
</html>
```

**popup.ts：**

```typescript
console.log('Popup loaded');
```

## 七、常见问题

### Q1: 如何创建指定框架的项目？

**方法一：交互式选择**

```bash
bunx wxt@latest init
```

在交互式流程中选择对应的框架模板。

**方法二：手动安装框架依赖**

```bash
# 创建 Vanilla 项目
bunx wxt@latest init

# 安装框架依赖
bun i -D svelte @sveltejs/vite-plugin-svelte  # Svelte
bun i -D solid-js vite-plugin-solid           # Solid
bun i -D vue @vitejs/plugin-vue               # Vue
bun i -D react react-dom @vitejs/plugin-react # React
```

### Q2: 可以在创建后切换框架吗？

**可以，但建议重新创建项目。**

切换框架需要：
1. 卸载旧框架依赖
2. 安装新框架依赖
3. 更新配置文件
4. 重写组件代码

建议：直接创建新项目，然后复制业务逻辑。

### Q3: 如何使用非 Bun 包管理器？

**使用 npm：**

```bash
npx wxt@latest init
npm run dev
```

**使用 pnpm：**

```bash
pnpm dlx wxt@latest init
pnpm dev
```

**使用 Yarn：**

```bash
yarn dlx wxt@latest init
yarn dev
```

### Q4: 创建项目失败怎么办？

**常见原因和解决方案：**

1. **网络问题**
   - 检查网络连接
   - 使用代理
   - 重新运行命令

2. **权限问题**
   - 检查目录权限
   - 使用 sudo（Linux/macOS）
   - 以管理员身份运行（Windows）

3. **Bun 未安装**
   - 安装 Bun：`curl -fsSL https://bun.sh/install | bash`
   - 验证安装：`bun --version`

4. **端口被占用**
   - 修改 `wxt.config.ts` 中的端口
   - 关闭占用端口的程序

### Q5: 如何在已有项目中添加 WXT？

**方法：**

```bash
# 进入已有项目目录
cd existing-project

# 安装 WXT
bun i -D wxt typescript

# 创建 WXT 配置文件
# 创建 wxt.config.ts

# 创建入口点目录
mkdir -p entrypoints

# 添加脚本到 package.json
```

## 八、最佳实践

### 8.1 命名规范

**项目名称：**
- 使用小写字母、数字和连字符
- 例如：`my-extension`、`weather-widget`

**目录名称：**
- 使用小写字母
- 例如：`entrypoints`、`public`

**文件名称：**
- 使用小写字母和连字符
- 例如：`background.ts`、`popup.html`

### 8.2 版本管理

**使用 Git：**

```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"
```

**使用 .gitignore：**

```
# 依赖
node_modules/
package-lock.json
yarn.lock
pnpm-lock.yaml
bun.lockb

# 构建输出
.output/
.wxt/
dist/

# 编辑器
.vscode/
.idea/
*.swp
*.swo

# 系统文件
.DS_Store
Thumbs.db
```

### 8.3 配置管理

**环境变量：**

创建 `.env` 文件：

```bash
# 开发环境
NODE_ENV=development
WXT_API_URL=https://api.example.com
```

创建 `.env.production` 文件：

```bash
# 生产环境
NODE_ENV=production
WXT_API_URL=https://api.example.com
```

### 8.4 依赖管理

**定期更新依赖：**

```bash
# 检查过时的包
bunx npm-check-updates

# 更新依赖
bun i -D wxt@latest typescript@latest
```

**清理无用依赖：**

```bash
# 检查未使用的包
bunx depcheck
```

## 九、下一步

- [框架配置](../framework-setup.md)：学习各框架的配置方法
- [命令参考](../cli/commands.md)：掌握开发和构建命令
- [构建阶段](../lifecycle/phases.md)：了解构建流程
- [示例代码](../../examples/)：查看完整项目示例
- [入口点 API](../../api/entrypoints.md)：学习入口点 API
