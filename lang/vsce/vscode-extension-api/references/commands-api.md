# Commands API

## 目录
- [概览](#概览)
- [registerCommand](#registercommand)
- [executeCommand](#executecommand)
- [getCommands](#getcommands)
- [Command URI](#command-uri)

## 概览
Commands API 用于注册和执行命令，是扩展与 VSCode 交互的核心方式。

## registerCommand
注册命令处理函数：
```typescript
vscode.commands.registerCommand(
  'myExtension.command',
  (args: any) => {
    // 处理逻辑
  },
  thisArg
) → Disposable
```

## executeCommand
执行内置或扩展命令：
```typescript
const result = await vscode.commands.executeCommand<T>(
  'editor.action.addCommentLine'
);
```

常用命令：
- `editor.action.addCommentLine` - 添加注释
- `vscode.executeDefinitionProvider` - 获取定义
- `workbench.action.openSettings` - 打开设置

## getCommands
获取所有可用命令：
```typescript
const commands = await vscode.commands.getCommands(filterInternal?: boolean);
```

## Command URI
命令 URI 允许在hover、completion中使用可点击链接：
```typescript
const commandUri = vscode.Uri.parse('command:editor.action.addCommentLine');
const markdown = new vscode.MarkdownString(`[Add comment](${commandUri})`);
```
