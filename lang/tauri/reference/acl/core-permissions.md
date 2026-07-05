# ACL Core Permissions 参考

Core Permissions 是 Tauri 核心功能的权限定义。

## 概述

Core Permissions 控制对 Tauri 核心 API 的访问，包括窗口管理、事件系统、应用控制等。

## 权限列表

### 默认权限

```json
"core:default"
```

包含所有核心功能的默认权限。

### Window 权限

```json
"core:window:default"
"core:window:allow-create"
"core:window:allow-close"
"core:window:allow-set-title"
"core:window:allow-set-size"
"core:window:allow-set-position"
"core:window:allow-set-fullscreen"
"core:window:allow-minimize"
"core:window:allow-maximize"
"core:window:allow-unmaximize"
"core:window:allow-show"
"core:window:allow-hide"
"core:window:allow-set-focus"
"core:window:allow-set-always-on-top"
"core:window:allow-set-decorations"
"core:window:allow-set-resizable"
"core:window:allow-set-min-size"
"core:window:allow-set-max-size"
"core:window:allow-set-size-constraints"
"core:window:allow-center"
"core:window:allow-request-user-attention"
"core:window:allow-available-monitors"
"core:window:allow-primary-monitor"
"core:window:allow-current-monitor"
"core:window:allow-scale-factor"
"core:window:allow-inner-position"
"core:window:allow-outer-position"
"core:window:allow-inner-size"
"core:window:allow-outer-size"
"core:window:allow-is-maximized"
"core:window:allow-is-minimized"
"core:window:allow-is-fullscreen"
"core:window:allow-is-focused"
"core:window:allow-is-visible"
"core:window:allow-is-decorations"
"core:window:allow-is-resizable"
"core:window:allow-is-always-on-top"
```

### Webview 权限

```json
"core:webview:default"
"core:webview:allow-create-webview-window"
"core:webview:allow-get-all-webviews"
"core:webview:allow-get-webview-window"
```

### Event 权限

```json
"core:event:default"
"core:event:allow-emit"
"core:event:allow-emit-to"
"core:event:allow-listen"
"core:event:allow-once"
"core:event:allow-unlisten"
```

### App 权限

```json
"core:app:default"
"core:app:allow-app-show"
"core:app:allow-app-hide"
"core:app:allow-app-set-theme"
"core:app:allow-app-theme"
```

### Path 权限

```json
"core:path:default"
"core:path:allow-app-data-dir"
"core:path:allow-app-config-dir"
"core:path:allow-app-local-data-dir"
"core:path:allow-app-cache-dir"
"core:path:allow-app-log-dir"
"core:path:allow-home-dir"
"core:path:allow-desktop-dir"
"core:path:allow-document-dir"
"core:path:allow-download-dir"
"core:path:allow-picture-dir"
"core:path:allow-video-dir"
"core:path:allow-audio-dir"
"core:path:allow-temp-dir"
"core:path:allow-resource-dir"
```

### Resources 权限

```json
"core:resources:default"
"core:resources:allow-load"
"core:resources:allow-set"
"core:resources:allow-monitor"
```

### Menu 权限

```json
"core:menu:default"
"core:menu:allow-new"
"core:menu:allow-popup"
"core:menu:allow-set-as-app-menu"
"core:menu:allow-set-as-window-menu"
```

### Tray 权限

```json
"core:tray:default"
"core:tray:allow-new"
"core:tray:allow-set-icon"
"core:tray:allow-set-menu"
"core:tray:allow-set-tooltip"
```

### Image 权限

```json
"core:image:default"
"core:image:allow-from-bytes"
"core:image:allow-from-path"
"core:image:allow-new"
```

### Window Label

```json
"core:window:allow-label"
```

## 使用示例

### 最小权限

```json
{
  "identifier": "minimal-capability",
  "windows": ["main"],
  "permissions": [
    "core:default"
  ]
}
```

### 完整权限

```json
{
  "identifier": "full-capability",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:window:allow-create",
    "core:event:allow-emit",
    "core:event:allow-listen"
  ]
}
```

### 自定义窗口权限

```json
{
  "identifier": "window-capability",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:window:default",
    "core:window:allow-create",
    "core:window:allow-close",
    "core:window:allow-set-title",
    "core:window:allow-show",
    "core:window:allow-hide"
  ]
}
```
