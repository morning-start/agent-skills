# Window API

## 目录
- [概览](#概览)
- [showInformationMessage](#showinformationmessage)
- [showInputBox](#showinputbox)
- [showQuickPick](#showquickpick)
- [createTerminal](#createterminal)
- [createOutputChannel](#createoutputchannel)

## 概览
Window API 管理 VSCode 的 UI 交互，包括对话框、终端、编辑器等。

## showInformationMessage
显示信息消息：
```typescript
const result = await vscode.window.showInformationMessage(
  'Hello!',
  { modal: false },
  'Option1',
  'Option2'
);
```

## showInputBox
显示输入框：
```typescript
const input = await vscode.window.showInputBox({
  prompt: 'Enter name',
  value: 'default',
  validateInput: (value) => {
    return value.length > 0 ? null : 'Required';
  }
});
```

## showQuickPick
显示快速选择：
```typescript
const selected = await vscode.window.showQuickPick(
  items,
  {
    canPickMany: false,
    placeHolder: 'Select an option'
  }
);
```

## createTerminal
创建集成终端：
```typescript
const terminal = vscode.window.createTerminal({
  name: 'Build',
  shellPath: 'bash',
  shellArgs: ['-c', 'npm run build']
});
terminal.show();
terminal.sendText('npm install');
```

## createOutputChannel
创建输出通道：
```typescript
const channel = vscode.window.createOutputChannel('My Extension');
channel.appendLine('Log entry');
channel.show();
```
