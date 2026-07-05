# Extension Anatomy

## 目录
- [概览](#概览)
- [项目结构](#项目结构)
- [package.json 详解](#package-json-详解)
- [入口文件解析](#入口文件解析)
- [三个核心概念](#三个核心概念)

## 概览
VSCode 扩展通过 package.json 声明扩展能力，使用 TypeScript/JavaScript 实现功能逻辑。本文档详细说明扩展的内部结构和各部分作用。

## 项目结构

### 标准目录结构
```
extension-name/
├── .vscode/
│   ├── launch.json     # 调试启动配置
│   └── tasks.json      # 构建任务配置
├── src/
│   └── extension.ts    # 扩展入口源文件
├── package.json        # 扩展清单文件
├── tsconfig.json       # TypeScript 配置
├── README.md           # 扩展说明文档
└── CHANGELOG.md        # 变更日志
```

### 各文件作用
| 文件 | 用途 |
|------|------|
| package.json | 扩展元数据、激活事件、贡献点 |
| src/extension.ts | 扩展入口，导出 activate 和 deactivate |
| launch.json | F5 调试配置 |
| tasks.json | 编译任务定义 |

## package.json 详解

### VSCode 特定字段
```json
{
  "name": "extension-name",
  "displayName": "Display Name",
  "description": "Extension description",
  "version": "0.0.1",
  "publisher": "publisher-id",
  "engines": {
    "vscode": "^1.51.0"
  },
  "categories": ["Other"],
  "activationEvents": [],
  "main": "./out/extension.js",
  "contributes": {}
}
```

### 核心字段说明
| 字段 | 说明 | 示例 |
|------|------|------|
| name | 扩展唯一名称 | "helloworld-sample" |
| displayName | 显示名称 | "Hello World Sample" |
| publisher | 发布者 ID | "vscode-samples" |
| engines.vscode | 最低 VSCode 版本 | "^1.51.0" |
| main | 入口文件路径 | "./out/extension.js" |
| activationEvents | 激活事件数组 | ["onCommand:helloworld.helloWorld"] |
| contributes | 贡献点定义 | { "commands": [...] } |

## 入口文件解析

### 标准结构
```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  // 扩展被激活时执行
  console.log('Extension activated');

  // 注册命令
  let disposable = vscode.commands.registerCommand(
    'extension.command',
    () => {
      // 命令处理逻辑
    }
  );

  // 管理生命周期
  context.subscriptions.push(disposable);
}

export function deactivate() {
  // 清理资源
}
```

### ExtensionContext 属性
| 属性 | 说明 |
|------|------|
| subscriptions | 可释放资源的注册表 |
| workspaceState | 工作区级别存储 |
| globalState | 全局级别存储 |
| extensionPath | 扩展目录路径 |
| secrets | 安全存储 |

## 三个核心概念

### 1. Activation Events（激活事件）
触发扩展激活的事件类型：
- `onCommand:commandId` - 命令被执行时
- `onView:viewId` - 视图被打开时
- `onLanguage:languageId` - 文件被特定语言打开时
- `onStartupFinished` - VSCode 启动完成后

### 2. Contribution Points（贡献点）
package.json 中的静态声明：
```json
{
  "contributes": {
    "commands": [...],
    "menus": {...},
    "configuration": {...},
    "views": {...}
  }
}
```

### 3. VS Code API
代码中调用的 JavaScript API：
```typescript
vscode.commands.registerCommand()
vscode.window.showInformationMessage()
vscode.workspace.getConfiguration()
```
