# ACL Permission 参考

Permission 定义了具体的安全权限，控制对特定 API 的访问。

## 概述

Permission 是 Tauri 2.0 权限系统的基本单元。每个插件提供一组预定义的权限。

## 权限格式

### 默认权限

```json
"dialog:default"
```

### 允许权限

```json
"dialog:allow-open"
```

### 拒绝权限

```json
"dialog:deny-open"
```

## 常用权限列表

### Core 权限

```json
"core:default"
"core:event:default"
"core:event:allow-emit"
"core:event:allow-listen"
"core:window:default"
"core:window:allow-create"
"core:window:allow-close"
"core:window:allow-set-title"
"core:window:allow-minimize"
"core:window:allow-maximize"
"core:window:allow-unmaximize"
"core:window:allow-show"
"core:window:allow-hide"
"core:window:allow-set-focus"
```

### Dialog 权限

```json
"dialog:default"
"dialog:allow-open"
"dialog:allow-save"
"dialog:allow-message"
"dialog:allow-ask"
"dialog:allow-confirm"
```

### File System 权限

```json
"fs:default"
"fs:allow-read"
"fs:allow-write"
"fs:allow-read-dir"
"fs:allow-create-dir"
"fs:allow-remove-dir"
"fs:allow-remove-file"
"fs:allow-rename"
"fs:allow-copy-file"
"fs:allow-exists"
"fs:allow-stat"
```

### HTTP 权限

```json
"http:default"
"http:allow-fetch"
"http:allow-fetch-cancel"
"http:allow-fetch-read-body"
"http:allow-fetch-send"
```

### Notification 权限

```json
"notification:default"
"notification:allow-is-permission-granted"
"notification:allow-request-permission"
"notification:allow-notify"
```

### Shell 权限

```json
"shell:default"
"shell:allow-open"
"shell:allow-execute"
"shell:allow-spawn"
"shell:allow-stdin-write"
"shell:allow-kill"
```

### Clipboard 权限

```json
"clipboard-manager:default"
"clipboard-manager:allow-read-text"
"clipboard-manager:allow-write-text"
```

## 自定义权限

可以在 Capability 中定义自定义权限：

```json
{
  "permissions": [
    {
      "identifier": "my-custom-permission",
      "description": "Custom permission for my feature",
      "allow": [
        { "path": "$APPDATA/**" }
      ]
    }
  ]
}
```

## 权限检查

权限在运行时自动检查。如果未授予相应权限，API 调用将失败。
