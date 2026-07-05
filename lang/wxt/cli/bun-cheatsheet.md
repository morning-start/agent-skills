# Bun 速查表

Bun 是一个现代的 JavaScript 运行时、包管理器、测试运行器和打包器，专为速度和效率设计。

## 安装与更新

### 安装 Bun

**Windows（PowerShell）：**

```powershell
irm https://bun.sh/install.ps1 | iex
```

**macOS / Linux：**

```bash
curl -fsSL https://bun.sh/install | bash
```

**使用 Homebrew（macOS）：**

```bash
brew tap oven-sh/bun
brew install bun
```

**验证安装：**

```bash
bun --version
```

### 更新 Bun

```bash
# 更新 Bun 到最新版本
bun upgrade

# 更新到特定版本
bun upgrade@latest
bun upgrade@1.0.0
```

### 卸载 Bun

**macOS / Linux：**

```bash
rm -rf ~/.bun
```

**Windows：**

```powershell
Remove-Item -Recurse -Force $env:LOCALAPPDATA\bun
```

## 包管理

### 安装依赖

```bash
# 安装所有依赖
bun install

# 简写
bun i

# 安装特定包
bun install react
bun i react

# 安装开发依赖
bun install -D typescript
bun i -D typescript

# 安装特定版本
bun install react@18.2.0

# 安装多个包
bun install react react-dom
```

### 更新依赖

```bash
# 更新所有依赖
bun update

# 更新特定包
bun update react

# 更新到最新版本
bun update --latest
```

### 卸载依赖

```bash
# 卸载包
bun uninstall react
bun remove react

# 卸载开发依赖
bun uninstall -D typescript
```

### 查看依赖

```bash
# 列出所有依赖
bun pm ls

# 查看依赖树
bun pm ls --all

# 查看过时的包
bun pm outdated
```

## 运行脚本

### 运行 Node.js 脚本

```bash
# 运行 .js 文件
bun run index.js

# 运行 .ts 文件（无需编译）
bun run index.ts

# 运行 .mjs 文件
bun run index.mjs

# 运行 .cjs 文件
bun run index.cjs
```

### 运行 package.json 脚本

```bash
# 运行脚本
bun run dev
bun run build
bun run test

# 简写（省略 run）
bun dev
bun build
bun test
```

### 运行远程脚本

```bash
# 运行远程脚本
bun run https://example.com/script.ts

# 运行 NPM 包
bun run create-vite
```

## TypeScript

### 原生 TypeScript 支持

```bash
# 直接运行 TypeScript 文件
bun run index.ts

# 类型检查
bun --typecheck index.ts

# 类型检查并运行
bun --typecheck --run index.ts
```

### TypeScript 配置

```bash
# 使用特定 tsconfig.json
bun --tsconfig tsconfig.build.json run index.ts
```

## 性能优化

### 缓存

```bash
# 清理缓存
bun pm cache rm

# 查看缓存
bun pm cache ls
```

### 并发

```bash
# 并发运行多个命令
bun run dev & bun run test
```

### 监视模式

```bash
# 监视文件变化
bun --watch run index.ts
```

## 开发服务器

### 启动服务器

```bash
# 启动开发服务器
bun dev

# 指定端口
bun dev --port 3000

# 指定主机
bun dev --host 0.0.0.0
```

### HMR（热模块替换）

```bash
# 启用 HMR
bun --hot run index.ts
```

## 测试

### 运行测试

```bash
# 运行所有测试
bun test

# 运行特定测试文件
bun test index.test.ts

# 运行匹配模式的测试
bun test **/*.test.ts

# 监视模式
bun test --watch
```

### 覆盖率

```bash
# 生成覆盖率报告
bun test --coverage
```

## 打包

### 创建可执行文件

```bash
# 打包单个文件
bun build index.ts --outfile index.js

# 打包为可执行文件
bun build index.ts --compile --outfile index

# 打包为 Node.js 包
bun build index.ts --target node

# 打包为浏览器包
bun build index.ts --target browser
```

### 打包选项

```bash
# 压缩输出
bun build index.ts --minify

# 指定入口点
bun build --entrypoint ./src/index.ts

# 指定输出目录
bun build --outdir ./dist

# 外部化依赖
bun build index.ts --external react
```

## 环境变量

### 加载环境变量

```bash
# 从 .env 加载
bun run index.ts

# 从特定文件加载
bun run --env-file .env.production index.ts
```

### 设置环境变量

```bash
# 设置环境变量
NODE_ENV=production bun run index.ts

# 设置多个环境变量
NODE_ENV=production PORT=3000 bun run index.ts
```

## 调试

### 启用调试

```bash
# 启用调试
bun --debug run index.ts

# 使用 inspect
bun --inspect run index.ts

# 使用 inspect-brk
bun --inspect-brk run index.ts
```

### 查看日志

```bash
# 启用详细日志
bun --verbose run index.ts

# 启用调试日志
bun --debug run index.ts
```

## WXT 与 Bun 集成

### 初始化 WXT 项目

```bash
# 使用 Bun 创建 WXT 项目
bunx wxt@latest init

# 选择 Bun 作为包管理器
```

### 运行 WXT 命令

```bash
# 启动开发服务器
bun run dev

# 构建扩展
bun run build

# 打包扩展
bun run zip
```

### 使用 bunx 替代 npx

```bash
# 使用 bunx
bunx wxt@latest init

# 使用 npx
npx wxt@latest init
```

## 实用技巧

### 批量操作

```bash
# 批量安装包
bun i react react-dom typescript eslint

# 批量卸载包
bun remove react react-dom typescript eslint
```

### 脚本别名

```bash
# 在 .bashrc 或 .zshrc 中添加别名
alias b='bun'
alias bi='bun i'
alias bd='bun dev'
alias bb='bun build'
```

### 性能对比

| 操作 | Bun | npm | pnpm | Yarn |
|------|-----|-----|------|------|
| 安装依赖 | ⚡ | 🐢 | 🚀 | 🚗 |
| 更新依赖 | ⚡ | 🐢 | 🚀 | 🚗 |
| 卸载依赖 | ⚡ | 🐢 | 🚀 | 🚗 |
| 运行脚本 | ⚡ | 🐢 | 🚗 | 🚗 |
| 构建项目 | ⚡ | 🐢 | 🚗 | 🚗 |

**说明：**
- ⚡ 极快（毫秒级）
- 🚀 快（秒级）
- 🚗 中等（几十秒）
- 🐢 慢（分钟级）

## 常见问题

### Q1: Bun 与 Node.js 兼容性如何？

**兼容性：** Bun 与 Node.js 有高度兼容性，但不完全兼容。

**不兼容的情况：**
- 某些 Node.js 内置模块
- 特定的 npm 包
- C++ 原生模块

**解决方案：** 对于不兼容的情况，使用 Node.js 运行。

### Q2: Bun 可以替换 npm 吗？

**可以，但需要注意：**

- Bun 与 npm 完全兼容
- 可以使用所有 npm 命令
- 可以使用 package-lock.json
- 建议使用 bun.lockb

### Q3: Bun 适合生产环境吗？

**目前不适合：** Bun 仍在快速开发中，不建议用于生产环境。

**适用场景：**
- 开发环境
- 工具脚本
- 测试环境

### Q4: 如何切换回 npm？

```bash
# 删除 bun.lockb
rm bun.lockb

# 使用 npm 安装依赖
npm install

# 使用 npm 运行脚本
npm run dev
```

### Q5: Bun 的未来规划是什么？

**目标：**

- 完全兼容 Node.js
- 更快的运行速度
- 更小的包大小
- 更好的工具集成

## 更多资源

- 官方文档：https://bun.sh/docs
- GitHub 仓库：https://github.com/oven-sh/bun
- Discord 社区：https://bun.sh/discord
- 示例项目：https://bun.sh/examples

## 快速参考

### 常用命令

```bash
bun i                # 安装依赖
bun run dev          # 运行脚本
bun run build        # 构建项目
bun test             # 运行测试
bun upgrade          # 更新 Bun
bun --help           # 查看帮助
```

### 包管理

```bash
bun i react          # 安装包
bun i -D typescript  # 安装开发依赖
bun remove react     # 卸载包
bun update react     # 更新包
bun pm ls            # 查看依赖
```

### 运行脚本

```bash
bun run index.js     # 运行 .js 文件
bun run index.ts     # 运行 .ts 文件
bun dev              # 运行 package.json 脚本
bun --watch run index.ts  # 监视模式
```

### 打包

```bash
bun build index.ts --outfile index.js  # 打包文件
bun build index.ts --compile --outfile index  # 打包可执行文件
```

### WXT 专用

```bash
bunx wxt@latest init  # 创建 WXT 项目
bun run dev           # 开发 WXT 扩展
bun run build         # 构建 WXT 扩展
bun run zip           # 打包 WXT 扩展
```
