---
name: wxt-skills
description: WXT 是现代化浏览器扩展开发框架，支持 Chrome、Firefox、Safari、Edge；提供 TypeScript 支持、HMR 热更新、多框架支持（Vanilla/Vue/React/Svelte/Solid）；适用于快速开发跨浏览器扩展。
version: 2.0.3
---
# WXT 浏览器扩展开发框架

WXT（Web eXtensions Tools）是一个基于 Vite 构建的现代化浏览器扩展开发框架，专为 Manifest V3 设计。

## 框架概述

**核心优势**：

- 声明式入口点定义，自动生成 manifest 配置
- 基于 Vite 的极速构建速度
- 完整的 TypeScript 类型支持
- 多框架支持（Vanilla、Vue、React、Svelte、Solid）
- 多浏览器一键构建（Chrome、Firefox、Edge、Safari）
- 内置热重载和开发服务器

## 官方资源

- **官网**：https://wxt.dev
- **GitHub**：https://github.com/wxt-dev/wxt
- **快速开始**：https://wxt.dev/guide/introduction.html
- **核心指南**：https://wxt.dev/guide/essentials/

## 模块导航

本技能按功能分为 5 个核心模块，建议按顺序学习：

### 1. 指引（guides/）

**[入门指南](guides/getting-started.md)**：基于官方文档的快速入门，包含环境准备、项目创建、入口点、静态资源、前端框架、权限、消息传递、数据存储和发布。

**[项目结构](guides/project-structure.md)**：项目结构详解，包含默认结构、源码模式和核心文件作用。

**[静态资源](guides/assets.md)**：静态资源管理，包含资源目录、引用方式、图标配置、优化策略和最佳实践。

**[内容脚本](guides/content-scripts.md)**：内容脚本开发，包含注入规则、与页面交互、调试方法和完整示例。

**[数据存储](guides/storage.md)**：数据存储方案，包含存储类型、监听变化、WXT 存储工具、数据迁移和最佳实践。

**[扩展内通信](guides/messaging.md)**：扩展内通信，包含一次性消息、长连接、跨扩展通信、通信模式和完整示例。

**[国际化](guides/i18n.md)**：国际化配置，包含语言文件、动态切换、复数形式、变量插值和完整示例。

**[框架配置](guides/framework-setup.md)**：Vanilla/Vue/React/Svelte/Solid 框架的完整配置。

**[权限配置](guides/permissions.md)**：权限声明方式、动态权限申请、最小权限原则和最佳实践。

**[浏览器适配](guides/browser-adapter.md)**：Chrome、Firefox、Edge、Safari 的适配和兼容性配置。

**[部署指南](guides/deployment.md)**：构建、打包、发布到各浏览器的完整流程。

### 2. 命令行（cli/）

**[命令参考](cli/commands.md)**：所有开发、构建、测试、打包命令（Bun 为主）。

**[Bun 速查表](cli/bun-cheatsheet.md)**：Bun 常用命令快速参考。

### 3. 生命周期（lifecycle/）

**[创建项目](lifecycle/creating-project.md)**：使用 bunx wxt 创建新项目的完整流程。

**[构建阶段](lifecycle/phases.md)**：8 个构建阶段的详细说明。

**[钩子函数](lifecycle/hooks.md)**：构建生命周期钩子的完整文档。

**[流程图](lifecycle/flow.md)**：完整的构建流程图示。

### 4. API（api/）

**[入口点 API](api/entrypoints.md)**：defineBackground、defineContentScript 等。

**[配置 API](api/config.md)**：defineConfig、defineManifest 等。

**[工具函数](api/utilities.md)**：存储、脚本注入、匹配模式等。

### 5. 示例（examples/）

**[Vanilla 示例](examples/vanilla/)**：原生 JavaScript/TypeScript 项目。

**[Vue 示例](examples/vue/)**：Vue 3 项目示例。

**[React 示例](examples/react/)**：React 项目示例。

**[Svelte 示例](examples/svelte/)**：Svelte 项目示例（推荐）。

**[Solid 示例](examples/solid/)**：SolidJS 项目示例（推荐）。

### 4. API（api/）

**[接口文档](api/interfaces.md)**：WXT 核心接口详细说明，包括入口点接口、配置接口、构建接口、开发服务器接口等。

**[类型文档](api/types.md)**：WXT 类型别名文档，包括配置类型、入口点类型、浏览器类型、模块类型等。

**[入口点 API](api/entrypoints.md)**：defineBackground、defineContentScript 等入口点定义函数。

**[配置 API](api/config.md)**：defineConfig、defineManifest 等配置函数。

**[工具函数](api/utilities.md)**：存储、脚本注入、匹配模式等工具函数。

### 5. 示例（examples/）

**[Vanilla 示例](examples/vanilla/)**：原生 JavaScript/TypeScript 项目。

**[Vue 示例](examples/vue/)**：Vue 3 项目示例。

**[React 示例](examples/react/)**：React 项目示例。

**[Svelte 示例](examples/svelte/)**：Svelte 项目示例（推荐）。

**[Solid 示例](examples/solid/)**：SolidJS 项目示例（推荐）。

## 快速开始

### 环境准备

```bash
# 安装 Bun（推荐）
curl -fsSL https://bun.sh/install | bash

# 验证安装
bun --version
```

### 创建项目

```bash
# 创建项目
bunx wxt@latest init

# 选择框架：Svelte（推荐）或 Solid
```

### 启动开发

```bash
cd my-extension
bun run dev
```

## 学习路径

**初学者路径**：指引（入门→框架）→ 示例（Svelte）→ 命令行（开发）

**进阶路径**：生命周期（阶段→钩子）→ API（入口点→配置→工具）→ 部署

**快速上手**：快速开始 → 选择框架示例 → 命令速查

## 包管理器支持

本技能以 Bun 为主，同时支持其他包管理器：

| 操作     | Bun               | npm               | pnpm           | Yarn           |
| -------- | ----------------- | ----------------- | -------------- | -------------- |
| 安装依赖 | `bun i`         | `npm i`         | `pnpm i`     | `yarn`       |
| 开发     | `bun run dev`   | `npm run dev`   | `pnpm dev`   | `yarn dev`   |
| 构建     | `bun run build` | `npm run build` | `pnpm build` | `yarn build` |

## 框架选择建议

| 框架              | 推荐度     | 特点                       | 适用场景                 |
| ----------------- | ---------- | -------------------------- | ------------------------ |
| **Svelte**  | ⭐⭐⭐⭐⭐ | 轻量、高性能、学习曲线平缓 | 推荐首选                 |
| **Solid**   | ⭐⭐⭐⭐⭐ | 响应式、高性能、细粒度更新 | 推荐首选                 |
| **Vue**     | ⭐⭐⭐⭐   | 生态成熟、中文文档丰富     | 熟悉 Vue 的开发者        |
| **React**   | ⭐⭐⭐⭐   | 生态庞大、就业机会多       | 熟悉 React 的开发者      |
| **Vanilla** | ⭐⭐⭐     | 无框架依赖、简单直接       | 简单扩展或团队无框架经验 |

## 官方资源

| 资源        | 链接                                    |
| ----------- | --------------------------------------- |
| 安装指南    | https://wxt.dev/guide/installation.html |
| 示例项目    | https://wxt.dev/examples.html           |
| API 参考    | https://wxt.dev/api/reference/wxt/      |
| GitHub 仓库 | https://github.com/wxt-dev/wxt          |

## 调用时机

当您遇到以下情况时，可以调用本技能获取帮助：

- 创建新的浏览器扩展项目
- 配置 WXT 项目选项
- 使用 Svelte/Solid 等框架开发扩展
- 定义各种类型的入口点（后台脚本、内容脚本、弹出页面等）
- 使用存储、脚本注入等功能
- 构建和打包扩展
- 解决开发过程中遇到的问题

## 技能结构说明

本技能采用模块化设计，每个模块独立完整：

1. **指引模块**：理论学习和概念理解
2. **命令行模块**：实际操作和工具使用
3. **生命周期模块**：深入理解构建流程
4. **API 模块**：查阅函数和配置
5. **示例模块**：参考完整代码

建议按模块顺序学习，但也可根据需求直接跳转到对应模块。
