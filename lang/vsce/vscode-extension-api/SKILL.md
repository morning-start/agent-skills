---
name: vscode-extension-api
description: 掌握VSCode扩展API核心命名空间，包括commands、window、workspace、debug等常用API的使用方法和最佳实践
dependency:
  system:
    - npm install -g @vscode/vsce
---

# VSCode Extension API

## 任务目标
- 本 Skill 用于：掌握 VSCode 扩展开发的核心 API 使用
- 能力包含：命令注册、窗口管理、工作区操作、调试集成、通知与对话框
- 触发条件：当用户需要实现扩展功能或调用 VSCode API 时

## 前置准备
- 环境要求：已完成 vscode-extension-basics 学习
- 工具要求：VSCode API 类型定义（@types/vscode）

## 操作步骤

### 标准流程

#### 1. 命令操作 (commands)
```typescript
// 注册命令
const disposable = vscode.commands.registerCommand(
  'extension.command',
  (args: any) => {
    console.log('Command executed');
  }
);

// 执行命令
vscode.commands.executeCommand('editor.action.addCommentLine');

// 获取所有命令
const commands = await vscode.commands.getCommands();
```

#### 2. 窗口操作 (window)
```typescript
// 显示消息
vscode.window.showInformationMessage('Hello!', 'Option1', 'Option2');

// 显示输入框
const input = await vscode.window.showInputBox({
  prompt: 'Enter your name'
});

// 显示快速选择
const selected = await vscode.window.showQuickPick(
  ['Option A', 'Option B'],
  { canPickMany: false }
);

// 创建终端
const terminal = vscode.window.createTerminal({
  name: 'My Terminal',
  shellPath: 'bash'
});

// 创建输出通道
const outputChannel = vscode.window.createOutputChannel('My Extension');
outputChannel.appendLine('Log message');
```

#### 3. 工作区操作 (workspace)
```typescript
// 获取配置
const config = vscode.workspace.getConfiguration('myExtension');
const value = config.get('settingKey');

// 获取工作区文件夹
const folders = vscode.workspace.workspaceFolders;

// 读取文件
const document = await vscode.workspace.openTextDocument(uri);
const text = document.getText();

// 创建文件监视
const watcher = vscode.workspace.createFileSystemWatcher('**/*.ts');
```

#### 4. 调试操作 (debug)
```typescript
// 启动调试
await vscode.debug.startDebugging(
  workspaceFolder,
  { type: 'node', request: 'launch' }
);

// 获取活动调试会话
const session = vscode.debug.activeDebugSession;

// 输出到调试控制台
vscode.debug.activeDebugConsole.appendLine('Debug message');
```

### 可选分支

#### 当需要事件监听时
```typescript
// 监听文本编辑器变化
vscode.window.onDidChangeActiveTextEditor(editor => {
  console.log('Active editor changed');
});

// 监听配置变化
vscode.workspace.onDidChangeConfiguration(event => {
  if (event.affectsConfiguration('myExtension')) {
    console.log('Configuration changed');
  }
});
```

## 资源索引

### 领域参考
- [references/commands-api.md](references/commands-api.md)
  - 何时读取：需要深入使用命令 API 时
  - 内容：命令注册、执行、命令 URI

- [references/window-api.md](references/window-api.md)
  - 何时读取：需要管理窗口、对话框、QuickPick 时
  - 内容：所有 window API 详细说明

- [references/workspace-api.md](references/workspace-api.md)
  - 何时读取：需要文件操作、工作区配置时
  - 内容：工作区、文件系统、配置 API

- [references/debug-api.md](references/debug-api.md)
  - 何时读取：需要集成调试功能时
  - 内容：调试会话、断点、调试控制台

## 注意事项

### 资源清理
- 所有 register 返回的 Disposable 需加入 context.subscriptions
- 事件监听器需在适当时机释放

### 异步处理
- 大部分 API 返回 Promise/T Thenable
- 使用 async/await 正确处理异步流程

### 类型安全
- 使用 TypeScript 获取完整的类型提示
- @types/vscode 提供 API 类型定义
