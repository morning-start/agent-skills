# Webview Basics

## 目录
- [概览](#概览)
- [createWebviewPanel](#createwebviewpanel)
- [webview.html](#webviewhtml)
- [生命周期](#生命周期)

## 概览
Webview 允许扩展创建完全自定义的 HTML/CSS/JS 界面。

## createWebviewPanel
创建 Webview 面板：
```typescript
const panel = vscode.window.createWebviewPanel(
  'viewType',           // 唯一标识符
  'Title',              // 显示标题
  vscode.ViewColumn.One, // 显示列
  {
    enableScripts: false,
    retainContextWhenHidden: false,
    localResourceRoots: []
  }
);
```

## webview.html
设置 HTML 内容：
```typescript
panel.webview.html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
</head>
<body>
  <h1>Hello Webview</h1>
</body>
</html>`;
```

## 生命周期
- onDidDispose: 面板关闭时
- onDidChangeViewState: 视图状态变化时
- dispose(): 编程方式关闭面板
