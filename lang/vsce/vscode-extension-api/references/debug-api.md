# Debug API

## 目录
- [概览](#概览)
- [startDebugging](#startdebugging)
- [activeDebugSession](#activedebugsession)
- [调试配置](#调试配置)

## 概览
Debug API 用于与 VSCode 调试功能集成。

## startDebugging
启动调试会话：
```typescript
const success = await vscode.debug.startDebugging(
  workspaceFolder,
  {
    type: 'node',
    request: 'launch',
    name: 'Launch Program',
    program: '${workspaceFolder}/index.js'
  }
);
```

## activeDebugSession
访问活动调试会话：
```typescript
const session = vscode.debug.activeDebugSession;
if (session) {
  session.customRequest('runInTerminal', { args: ['--debug'] });
}
```

## 调试配置
launch.json 配置示例：
```json
{
  "version": "0.2.0",
  "configurations": [{
    "type": "node",
    "request": "launch",
    "name": "Launch",
    "program": "${workspaceFolder}/index.js"
  }]
}
```
