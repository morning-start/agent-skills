# Webview Security

## 目录
- [概览](#概览)
- [Content Security Policy](#content-security-policy)
- [本地资源限制](#本地资源限制)
- [输入验证](#输入验证)

## 概览
Webview 安全最佳实践，防止恶意内容注入。

## Content Security Policy
```html
<meta http-equiv="Content-Security-Policy"
  content="default-src 'none';
           img-src https:;
           script-src 'self';
           style-src 'self';">
```

## 本地资源限制
```typescript
const panel = vscode.window.createWebviewPanel(
  'viewType', 'Title', vscode.ViewColumn.One,
  {
    localResourceRoots: [
      vscode.Uri.joinPath(context.extensionUri, 'media')
    ]
  }
);
```

## 输入验证
```typescript
// 清理用户输入
function sanitize(input: string): string {
  return input.replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
```

## 最佳实践
- 仅启用必要的功能（enableScripts）
- 尽可能使用 localResourceRoots = []
- 验证所有来自用户的输入
- 使用 HTTPS 加载外部资源
