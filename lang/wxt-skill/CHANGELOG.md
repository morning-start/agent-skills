# 更新日志

## [2.0.3] - 2025-02-01

### 新增

**CLI 命令文档**
- 重写 `cli/commands.md`，添加官方导航链接和详细命令说明
  - wxt build - 构建命令（参数、示例、配置）
  - wxt zip - 压缩打包命令
  - wxt prepare - 预处理命令
  - wxt clean - 清理命令
  - wxt init - 初始化命令
  - wxt submit - 扩展提交命令
  - wxt submit init - 提交初始化命令
  - 完整配置示例和最佳实践
  - 常见问题解答

**API 接口文档**
- 新增 `api/interfaces.md` - 核心接口文档
  - 入口点接口（BackgroundDefinition、ContentScriptEntrypoint、PopupEntrypoint 等）
  - 配置接口（UserConfig、ResolvedConfig、InlineConfig）
  - 构建接口（BuildOutput、WxtBuilder、WxtBuilderServer）
  - 开发服务器接口（WxtDevServer、ServerInfo）
  - 核心接口（Wxt、WxtHooks、WxtModule）
  - 输出接口（OutputAsset、OutputChunk、OutputFile）
  - 工具接口（Logger、FsCache、WxtPackageManager）
  - 类型引用接口（EntrypointInfo、Dependency、TargetBrowser）
  - 完整示例和类型使用示例

**API 类型文档**
- 新增 `api/types.md` - 类型别名文档
  - 配置类型（UserConfig、UserManifest、UserManifestFn）
  - 入口点类型（Entrypoint、EntrypointGroup、ContentScriptDefinition）
  - 浏览器类型（TargetBrowser、PerBrowserOption、ResolvedPerBrowserOptions）
  - 清单版本类型（TargetManifestVersion）
  - 构建类型（HookResult、OutputFile、WxtCommand）
  - 模块类型（WxtModuleOptions、WxtModuleSetup、WxtPlugin）
  - 目录类型（WxtDirEntry、WxtDirFileEntry、WxtDirTypeReferenceEntry）
  - 公共文件类型（ResolvedPublicFile、CopiedPublicFile、GeneratedPublicFile）
  - 其他类型（ExtensionRunnerConfig、EslintGlobalsPropValue 等）
  - 完整示例和类型使用示例

**官方文档覆盖**
- 完整覆盖 CLI Reference（8 个命令）
- 完整覆盖 API Reference - Interfaces（核心接口）
- 完整覆盖 API Reference - Type Aliases（核心类型）
- 所有文档包含官方导航链接和详细说明

### 改进

- 所有新增文档遵循统一的格式规范
- 每个文档包含官方导航链接、详细说明、使用示例
- 提供完整的代码示例和最佳实践
- 添加类型推断和类型守卫示例

## [2.0.2] - 2025-02-01

### 新增

**核心指南文档**
- 新增 `guides/assets.md` - 静态资源管理
  - 资源目录结构（public/、入口点资源）
  - 引用方式（TypeScript、HTML、CSS、Svelte）
  - 图标配置和优化策略
  - 环境变量使用
  - 最佳实践和常见问题
- 新增 `guides/content-scripts.md` - 内容脚本开发
  - 内容脚本定义和配置
  - 运行时机和样式注入
  - 与页面交互（读取/修改 DOM、监听事件）
  - 与 Background Script 通信（一次性消息、长连接）
  - 动态脚本注入
  - 权限配置和调试方法
  - 完整示例代码
- 新增 `guides/storage.md` - 数据存储方案
  - 存储类型（local、sync、session）
  - 基础用法（读写删除）
  - 监听变化和跨标签页同步
  - WXT 存储工具（defineItem、watch）
  - 数据迁移和错误处理
  - 最佳实践和完整示例
- 新增 `guides/messaging.md` - 扩展内通信
  - 通信类型和方式（sendMessage、connect、storage）
  - 一次性消息和长连接
  - 跨扩展通信和 Native Messaging
  - 通信模式（请求-响应、发布-订阅、事件总线）
  - 错误处理和性能优化
  - 消息格式规范和类型定义
  - 完整示例代码
- 新增 `guides/i18n.md` - 国际化配置
  - 语言文件格式和目录结构
  - 在 Manifest、JavaScript、HTML 中使用
  - 动态语言切换
  - 复数形式和变量插值
  - 日期和数字格式化
  - 最佳实践和完整示例

**官方文档覆盖**
- 新增 5 个核心主题的独立文档
- 每个文档包含官方导航链接、详细说明、配置方法、示例代码和最佳实践
- 补充官方导航中的关键主题：Assets、Content Scripts、Storage、Messaging、I18n

### 改进

- 所有新增文档遵循统一的格式规范
- 每个文档包含完整的官方导航链接
- 提供实用的示例代码和最佳实践
- 添加常见问题和错误处理说明

## [2.0.1] - 2025-02-01

### 新增

**官方导航链接**
- 在所有核心文档中添加官方导航链接，方便用户快速查阅：
  - `getting-started.md`：Get Started（快速开始）、Essentials（核心指南）完整导航
  - `project-structure.md`：项目结构、Configuration 子页面导航
  - `permissions.md`：权限、Manifest、Storage 官方链接
  - `framework-setup.md`：Frontend Frameworks 完整导航
  - `deployment.md`：Publishing、Testing Updates 官方链接
  - `browser-adapter.md`：Target Different Browsers、Browser Startup 官方链接
  - `api/config.md`：Configuration 完整子页面导航
  - `api/utilities.md`：Storage、Messaging、I18n、Scripting 官方链接
  - `api/entrypoints.md`：Entrypoints、Content Scripts 官方链接
  - `lifecycle/flow.md`：Remote Code、WXT Modules、Hooks 官方链接
  - `lifecycle/hooks.md`：Hooks 完整指南链接
  - `lifecycle/phases.md`：Hooks、Vite、Build Mode 官方链接
  - `cli/commands.md`：Installation、Browser Startup 官方链接
  - `examples/svelte/README.md`：Svelte 集成链接
  - `examples/solid/README.md`：Solid 集成链接

**官方文档覆盖**
- Get Started（2 个链接）
  - Introduction
  - Installation
- Essentials（22 个链接）
  - Project Structure
  - Entrypoints
  - Configuration（10 个子链接）
  - Extension APIs
  - Assets
  - Target Different Browsers
  - Content Scripts
  - Storage
  - Messaging
  - I18n
  - Scripting
  - WXT Modules
  - Frontend Frameworks
  - ES Modules
  - Remote Code
  - Unit Testing
  - E2E Testing
  - Publishing
  - Testing Updates

### 改进

- 统一所有文档的官方导航链接格式
- 在每个文档顶部添加"官方导航链接"章节
- 提供完整的一级、二级、三级导航结构
- 便于用户快速跳转到官方文档查阅详细信息

## [2.0.0] - 2025-02-01

### 新增

**指引模块**
- 基于官方文档重写 `getting-started.md`，包含：
  - 框架概述和核心特性
  - 环境准备（Bun 安装、浏览器安装）
  - 项目创建（使用 bunx wxt）
  - 入口点详解（Background、Content、Popup、Options）
  - 静态资源管理
  - 前端框架集成
  - 基础配置（wxt.config.ts、tsconfig.json）
  - 权限配置
  - 消息传递
  - 数据存储
  - 构建和发布
- 新增 `project-structure.md`，详细说明：
  - 标准项目结构
  - 源码模式结构
  - 目录说明（entrypoints、public、.output）
  - 路径别名配置
  - 环境变量
  - 类型定义
  - 目录组织最佳实践
- 新增 `permissions.md`，详细说明：
  - 权限类型（基础权限、主机权限、可选权限）
  - 权限配置方法
  - 最小权限原则
  - 动态权限申请
  - 权限使用场景
  - 权限与隐私
  - 权限最佳实践

**生命周期模块**
- 新增 `creating-project.md`，详细说明：
  - 使用 bunx wxt 创建项目（推荐方式）
  - 交互式创建流程（5 步）
  - 创建后项目结构
  - 不同框架的差异
  - 启动开发服务器
  - 创建不同类型的项目
  - 手动创建项目

**其他更新**
- 删除 scripts 目录，使用 bunx wxt 替代初始化脚本
- 更新 SKILL.md，添加版本信息和新的文档链接
- 所有文档基于 WXT 官方文档（https://wxt.dev）整理

### 改进

- 更新所有文档，确保与 WXT 官方文档一致
- 添加官方文档链接，方便用户查阅
- 改进文档结构，提高可读性
- 添加更多示例和最佳实践

### 修复

- 修复文档中过时的命令和配置
- 修复链接错误

## [1.0.0] - 初始版本

### 功能

- 5 个核心模块：指引、命令行、生命周期、API、示例
- 支持 5 个框架：Vanilla、Vue、React、Svelte、Solid
- 完整的浏览器适配：Chrome、Firefox、Edge、Safari
- Bun 包管理器支持
- 详细的 API 文档和示例代码
