---
name: vscode-extension-webview
description: 掌握VSCode Webview开发，创建自定义Web界面，实现扩展与Webview之间的消息传递和状态管理
---

# VSCode Extension Webview

## 任务目标
- 本 Skill 用于：创建自定义 Webview 界面，实现与 VSCode 深度集成的功能
- 能力包含：Webview Panel、消息传递、生命周期管理、本地资源加载、CSP 安全策略
- 触发条件：当用户需要创建自定义 UI 界面或实现复杂交互功能时

## 前置准备
- 环境要求：已完成 vscode-extension-basics 学习
- 前置知识：HTML/CSS/JavaScript 基础

## 操作步骤

### 标准流程

#### 1. 创建 Webview Panel
```typescript
const panel = vscode.window.createWebviewPanel(
  'catCoding',           // viewType 标识符
  'Cat Coding',          // 面板标题
  vscode.ViewColumn.One, // 显示位置
  {
    enableScripts: true,
    localResourceRoots: [vscode.Uri.joinPath(context.extensionUri, 'media')]
  }
);

panel.webview.html = getWebviewContent();
```

#### 2. 设置 Webview HTML 内容
```typescript
function getWebviewContent() {
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy"
    content="default-src 'none'; img-src https:; script-src 'self';">
  <title>My Webview</title>
</head>
<body>
  <h1>Hello from Webview</h1>
  <div id="content"></div>
</body>
</html>`;
}
```

#### 3. 扩展向 Webview 发送消息
```typescript
// 扩展端发送
panel.webview.postMessage({ command: 'refactor', text: 'Reduce lines' });

// Webview 端接收
window.addEventListener('message', event => {
  const message = event.data;
  if (message.command === 'refactor') {
    console.log(message.text);
  }
});
```

#### 4. Webview 向扩展发送消息
```typescript
// Webview 端发送
const vscode = acquireVsCodeApi();
vscode.postMessage({ command: 'alert', text: 'Bug found!' });

// 扩展端接收
panel.webview.onDidReceiveMessage(message => {
  switch (message.command) {
    case 'alert':
      vscode.window.showErrorMessage(message.text);
      break;
  }
}, undefined, context.subscriptions);
```

#### 5. 管理 Webview 生命周期
```typescript
panel.onDidDispose(() => {
  // 清理资源
  panel = undefined;
}, undefined, context.subscriptions);

panel.onDidChangeViewState(e => {
  if (e.webviewPanel.visible) {
    // 恢复状态
  }
});
```

### 可选分支

#### 当需要加载本地资源时
```typescript
const localPath = vscode.Uri.joinPath(context.extensionUri, 'media', 'cat.gif');
const imageSrc = panel.webview.asWebviewUri(localPath);
```

#### 当需要持久化状态时
```typescript
// 在 webview 中保存状态
const vscode = acquireVsCodeApi();
vscode.setState({ count: 10 });

// 恢复状态
const previousState = vscode.getState();
```

## 资源索引

### 领域参考
- [references/webview-basics.md](references/webview-basics.md)
  - 何时读取：需要了解 Webview 基本概念时
  - 内容：Panel 创建、HTML 设置、生命周期

- [references/webview-messaging.md](references/webview-messaging.md)
  - 何时读取：需要实现双向消息传递时
  - 内容：postMessage、onDidReceiveMessage、消息格式

- [references/webview-security.md](references/webview-security.md)
  - 何时读取：需要确保 Webview 安全时
  - 内容：Content Security Policy、本地资源限制、输入验证

## 注意事项

### 安全最佳实践
- 启用 Content Security Policy
- 使用 localResourceRoots 限制资源访问
- 验证和清理所有用户输入

### 性能考虑
- 使用 retainContextWhenHidden 要谨慎（高内存开销）
- 优先使用 getState/setState 进行状态持久化

### 主题适配
- 使用 CSS 变量响应 VSCode 主题变化
- 支持 vscode-light、vscode-dark、vscode-high-contrast
