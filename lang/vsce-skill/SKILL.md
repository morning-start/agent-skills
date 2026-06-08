---
name: vsce
version: 1.0.0
description: Use when the user asks about VSCode extension development, API usage, TreeView, Webview, packaging, or Marketplace publishing.
tags: [vscode, extension, vsce, typescript, vscode-api]
---

# VSCode Extension Development Skills

## 任务目标
- 本 Skill 用于：系统化掌握 VSCode 扩展开发技能
- 能力包含：扩展基础、API使用、TreeView、Webview、扩展发布
- 触发条件：当用户需要完整学习 VSCode 扩展开发或需要特定模块参考时

## 前置准备
- 环境要求：Node.js 18+、Git、VSCode 最新版
- 工具安装：
  ```bash
  npm install -g yo generator-code @vscode/vsce
  ```

## 技能模块

### 基础模块（入门必学）

#### 1. [vscode-extension-basics](vscode-extension-basics-skill/)
- **何时使用**：初次接触 VSCode 扩展开发
- **核心能力**：项目搭建、package.json 配置、激活事件、调试运行
- **前置要求**：Node.js 基础

#### 2. [vscode-extension-api](vscode-extension-api-skill/)
- **何时使用**：需要调用 VSCode API 实现功能
- **核心能力**：commands、window、workspace、debug API
- **前置要求**：已完成 basics 模块

### 功能模块（按需学习）

#### 3. [vscode-extension-treeview](vscode-extension-treeview-skill/)
- **何时使用**：需要创建自定义树形视图展示数据
- **核心能力**：TreeDataProvider、View Container、视图操作
- **前置要求**：已完成 basics 模块

#### 4. [vscode-extension-webview](vscode-extension-webview-skill/)
- **何时使用**：需要创建自定义 Web 界面
- **核心能力**：Webview Panel、消息传递、状态管理、CSP
- **前置要求**：已完成 basics 模块

### 发布模块

#### 5. [vscode-extension-publishing](vscode-extension-publishing-skill/)
- **何时使用**：需要发布扩展到 Marketplace
- **核心能力**：vsce 工具、发布流程、平台特定扩展
- **前置要求**：已完成 basics 模块

## 学习路径

```
┌─────────────────────────────────────────────────────────────┐
│                    VSCode 扩展开发学习路径                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐                                       │
│  │ vscode-extension │                                       │
│  │    -basics       │ ← 入门起点                            │
│  └────────┬─────────┘                                       │
│           │                                                  │
│     ┌─────┴─────┐                                           │
│     ▼           ▼                                           │
│  ┌──────┐  ┌─────────┐                                      │
│  │ api  │  │ treeview│                                      │
│  └──────┘  └─────────┘                                      │
│     │           │                                            │
│     │     ┌─────┴─────┐                                     │
│     │     ▼           ▼                                     │
│     │  ┌──────┐  ┌─────────┐                                │
│     └─►│webview│  │publishing│ ← 发布终点                   │
│        └──────┘  └─────────┘                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| 阶段 | 模块 | 建议时长 |
|------|------|----------|
| 入门 | basics | 1-2 天 |
| 进阶 | api | 2-3 天 |
| 功能 | treeview / webview | 各 2-3 天 |
| 发布 | publishing | 1 天 |

## 资源索引

| 模块 | 参考文档 | 何时使用 |
|------|----------|----------|
| basics | [extension-anatomy.md](vscode-extension-basics-skill/references/extension-anatomy.md) | 深入理解项目结构 |
| basics | [activation-events.md](vscode-extension-basics-skill/references/activation-events.md) | 理解激活机制 |
| basics | [contribution-points.md](vscode-extension-basics-skill/references/contribution-points.md) | 声明式扩展功能 |
| api | [commands-api.md](vscode-extension-api-skill/references/commands-api.md) | 命令操作 |
| api | [window-api.md](vscode-extension-api-skill/references/window-api.md) | 窗口管理 |
| api | [workspace-api.md](vscode-extension-api-skill/references/workspace-api.md) | 文件和配置 |
| api | [debug-api.md](vscode-extension-api-skill/references/debug-api.md) | 调试集成 |
| treeview | [treeview-basics.md](vscode-extension-treeview-skill/references/treeview-basics.md) | 基本树视图 |
| treeview | [treeview-advanced.md](vscode-extension-treeview-skill/references/treeview-advanced.md) | 高级视图功能 |
| webview | [webview-basics.md](vscode-extension-webview-skill/references/webview-basics.md) | Webview 基础 |
| webview | [webview-messaging.md](vscode-extension-webview-skill/references/webview-messaging.md) | 双向消息传递 |
| webview | [webview-security.md](vscode-extension-webview-skill/references/webview-security.md) | 安全策略 |
| publishing | [vsce-cli.md](vscode-extension-publishing-skill/references/vsce-cli.md) | vsce 工具 |
| publishing | [publisher-setup.md](vscode-extension-publishing-skill/references/publisher-setup.md) | 发布者账号 |
| publishing | [platform-extensions.md](vscode-extension-publishing-skill/references/platform-extensions.md) | 多平台支持 |

## 常见场景

| 场景 | 推荐模块 | 关键操作 |
|------|----------|----------|
| 创建第一个扩展 | basics | npx yo code → 调试运行 |
| 实现命令面板 | api | registerCommand + contributes |
| 显示文件树 | treeview | TreeDataProvider |
| 嵌入网页界面 | webview | createWebviewPanel |
| 发布到 Marketplace | publishing | vsce publish |

## 注意事项

### 版本兼容性
- 使用 `engines.vscode` 指定最低兼容版本
- 推荐 `^1.74.0` 及以上版本

### 资源管理
- 所有 Disposable 需加入 context.subscriptions
- Webview 面板需正确处理 onDidDispose

### 安全性
- Webview 必须配置 Content Security Policy
- 使用 localResourceRoots 限制资源访问
- 验证和清理所有用户输入

### 发布规范
- 扩展名称全局唯一
- 遵循 SemVer 版本管理
- 预发布版本使用奇数 patch
