# ACL Capability 参考

Capability 定义了应用的能力边界，控制哪些窗口可以使用哪些权限。

## 概述

在 Tauri 2.0 中，权限系统使用 Capability 进行管理。每个 Capability 定义了：
- 应用的唯一标识符
- 适用的窗口
- 授予的权限列表

## Capability 文件位置

```
src-tauri/capabilities/
├── default.json
└── main.json
```

## 基本结构

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Main window capability",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "dialog:default",
    "fs:default"
  ]
}
```

## 属性说明

| 属性 | 类型 | 必需 | 说明 |
|------|------|------|------|
| identifier | string | 是 | 唯一标识符 |
| description | string | 否 | 描述信息 |
| windows | string[] | 是 | 适用的窗口标签 |
| permissions | string[] | 是 | 权限列表 |
| platform | string[] | 否 | 适用的平台 |

## 窗口匹配

```json
{
  "windows": ["main", "settings"]
}
```

使用通配符匹配所有窗口：

```json
{
  "windows": ["*"]
}
```

## 权限继承

```json
{
  "identifier": "admin-capability",
  "windows": ["admin"],
  "permissions": [
    "core:default",
    {
      "identifier": "fs:allow-write",
      "allow": [{ "path": "**" }]
    }
  ]
}
```

## 多个 Capability

可以创建多个 Capability 文件：

```json
// capabilities/main.json
{
  "identifier": "main-capability",
  "windows": ["main"],
  "permissions": ["core:default", "dialog:default"]
}

// capabilities/admin.json
{
  "identifier": "admin-capability",
  "windows": ["admin"],
  "permissions": ["core:default", "fs:default", "shell:default"]
}
```

## 权限引用格式

### 简单权限

```json
"permissions": [
  "dialog:default",
  "fs:default"
]
```

### 带配置的权限

```json
"permissions": [
  {
    "identifier": "fs:allow-read-text-file",
    "allow": [
      { "path": "$APPDATA/**" },
      { "path": "$HOME/documents/**" }
    ]
  }
]
```

## 完整示例

```json
{
  "identifier": "my-app-capability",
  "description": "Capability for main application window",
  "windows": ["main", "settings"],
  "permissions": [
    "core:default",
    "core:window:default",
    "core:window:allow-create",
    "core:window:allow-close",
    "dialog:default",
    "fs:default",
    "notification:default",
    "shell:allow-open",
    {
      "identifier": "fs:allow-read-text-file",
      "allow": [
        { "path": "$APPDATA/**" }
      ]
    },
    {
      "identifier": "http:default",
      "allow": [
        { "url": "https://api.example.com/**" }
      ]
    }
  ]
}
```
