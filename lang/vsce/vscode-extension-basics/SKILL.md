---
name: vscode-extension-basics
description: VSCode扩展开发入门技能，掌握扩展基础概念、项目结构、package.json配置和激活事件机制
---

# VSCode Extension Basics

## 任务目标
- 本 Skill 用于：掌握 VSCode 扩展开发的基础知识和入门实践
- 能力包含：项目搭建、package.json 配置、激活事件、贡献点、调试运行
- 触发条件：当用户需要创建 VSCode 扩展或学习扩展开发基础时

## 前置准备
- 环境要求：Node.js 18+、Git、VSCode 最新版
- 工具安装：
  ```bash
  npm install -g yo generator-code
  ```

## 操作步骤

### 标准流程

#### 1. 创建扩展项目
使用 Yeoman 脚手架创建新扩展：
```bash
npx yo code
```

选择选项：
- Extension Type: New Extension (TypeScript)
- Name: YourExtensionName
- Identifier: your-extension-name
- Description: 扩展描述
- Initialize git repository: Y
- Bundler: unbundled
- Package Manager: npm

#### 2. 理解项目结构
```
my-extension/
├── .vscode/
│   ├── launch.json     # 调试配置
│   └── tasks.json      # 构建任务
├── src/
│   └── extension.ts    # 扩展入口
├── package.json        # 扩展清单
├── tsconfig.json       # TypeScript 配置
└── README.md           # 扩展说明
```

#### 3. 配置 package.json
核心字段说明：
```json
{
  "name": "my-extension",
  "displayName": "My Extension",
  "version": "0.0.1",
  "publisher": "your-publisher-id",
  "engines": {
    "vscode": "^1.74.0"
  },
  "main": "./out/extension.js",
  "activationEvents": [],
  "contributes": {
    "commands": [{
      "command": "my-extension.helloWorld",
      "title": "Hello World"
    }]
  }
}
```

#### 4. 编写扩展代码
```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  console.log('Extension activated!');

  const disposable = vscode.commands.registerCommand(
    'my-extension.helloWorld',
    () => {
      vscode.window.showInformationMessage('Hello World!');
    }
  );

  context.subscriptions.push(disposable);
}

export function deactivate() {}
```

#### 5. 调试运行
1. 按 F5 或 Ctrl+Shift+P 运行 "Debug: Start Debugging"
2. 在扩展开发主机窗口中测试
3. 打开命令面板 (Ctrl+Shift+P) 执行扩展命令

### 可选分支

#### 当需要添加新命令时
1. 在 package.json 的 contributes.commands 中添加命令定义
2. 使用 vscode.commands.registerCommand 注册处理函数
3. 刷新扩展或重启调试

## 资源索引

### 必要脚本
无（基础技能以文档和实践为主）

### 领域参考
- [references/extension-anatomy.md](references/extension-anatomy.md)
  - 何时读取：需要深入理解扩展内部结构时
  - 内容：package.json 详解、入口文件解析、目录结构说明

- [references/activation-events.md](references/activation-events.md)
  - 何时读取：需要理解扩展激活机制时
  - 内容：激活事件类型、触发条件、生命周期

- [references/contribution-points.md](references/contribution-points.md)
  - 何时读取：需要声明式扩展 VSCode 功能时
  - 内容：贡献点分类、JSON Schema、配置参考

## 注意事项

### 版本兼容性
- engines.vscode 指定最低兼容版本
- 使用 ^1.74.0 表示兼容 1.74.0 及以上版本
- VSCode 1.74+ 自动为 commands 贡献生成激活事件

### 扩展标识
- 扩展 ID 格式：`<publisher>.<name>`
- publisher 来自 Marketplace 发布者账户
- ID 一经创建不可更改

### 清理资源
- 使用 context.subscriptions.push() 管理可释放资源
- 扩展停用时自动调用 deactivate() 函数

### TypeScript 支持
- 推荐使用 TypeScript 开发扩展
- 编译输出到 out/ 目录
- 使用 vscode:prepublish 脚本进行发布前编译
