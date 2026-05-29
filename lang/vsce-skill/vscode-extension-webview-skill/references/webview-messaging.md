# Webview Messaging

## 目录
- [概览](#概览)
- [扩展到Webview](#扩展到webview)
- [Webview到扩展](#webview到扩展)
- [消息格式](#消息格式)

## 概览
消息传递允许扩展和 Webview 双向通信。

## 扩展到Webview
```typescript
// 扩展端
panel.webview.postMessage({ command: 'init', data: someData });

// Webview端
window.addEventListener('message', event => {
  const { command, data } = event.data;
  if (command === 'init') {
    // 处理消息
  }
});
```

## Webview到扩展
```typescript
// Webview端
const vscode = acquireVsCodeApi();
vscode.postMessage({ command: 'action', value: result });

// 扩展端
panel.webview.onDidReceiveMessage(msg => {
  switch (msg.command) {
    case 'action':
      // 处理消息
      break;
  }
}, undefined, context.subscriptions);
```

## 消息格式
```typescript
interface WebviewMessage {
  command: string;
  data?: any;
}
```
