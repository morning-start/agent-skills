# Workspace API

## 目录
- [概览](#概览)
- [getConfiguration](#getconfiguration)
- [workspaceFolders](#workspacefolders)
- [openTextDocument](#opentextdocument)
- [createFileSystemWatcher](#createfilesystemwatcher)

## 概览
Workspace API 提供对工作区文件、配置和资源的访问。

## getConfiguration
获取配置：
```typescript
const config = vscode.workspace.getConfiguration('myExtension');
const enabled = config.get('enabled', true);
await config.update('enabled', false, vscode.ConfigurationTarget.Global);
```

## workspaceFolders
访问工作区文件夹：
```typescript
if (vscode.workspace.workspaceFolders) {
  const root = vscode.workspace.workspaceFolders[0];
  console.log(root.uri.fsPath);
}
```

## openTextDocument
打开或创建文档：
```typescript
// 打开已有文件
const doc = await vscode.workspace.openTextDocument(uri);

// 创建新文档
const newDoc = await vscode.workspace.openTextDocument({
  content: 'console.log("Hello");',
  language: 'javascript'
});
```

## createFileSystemWatcher
创建文件监视器：
```typescript
const watcher = vscode.workspace.createFileSystemWatcher(
  '**/*.ts',
  false,  // ignoreCreateEvents
  true,   // ignoreChangeEvents
  false   // ignoreDeleteEvents
);

watcher.onDidCreate(uri => console.log('Created:', uri));
watcher.onDidChange(uri => console.log('Changed:', uri));
watcher.onDidDelete(uri => console.log('Deleted:', uri));
```
