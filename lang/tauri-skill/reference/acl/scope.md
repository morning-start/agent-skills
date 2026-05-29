# ACL Scope 参考

Scope 定义了更细粒度的权限控制，用于限制对特定资源（文件、URL 等）的访问。

## 概述

Scope 扩展了权限系统，允许定义具体的资源路径或 URL 模式。

## 文件系统 Scope

### 路径变量

Tauri 提供了内置的路径变量：

| 变量 | 说明 | 示例 |
|------|------|------|
| `$APPDATA` | 应用数据目录 | `C:\Users\...\AppData\Roaming\com.app` |
| `$APPCACHE` | 应用缓存目录 | `C:\Users\...\AppData\Local\com.app` |
| `$APPCONFIG` | 应用配置目录 | `C:\Users\...\AppData\Roaming\com.app` |
| `$APPLOG` | 应用日志目录 | `C:\Users\...\AppData\Roaming\com.app` |
| `$HOME` | 用户主目录 | `C:\Users\...` |
| `$DESKTOP` | 桌面目录 | `C:\Users\...\Desktop` |
| `$DOCUMENT` | 文档目录 | `C:\Users\...\Documents` |
| `$DOWNLOAD` | 下载目录 | `C:\Users\...\Downloads` |
| `$PICTURE` | 图片目录 | `C:\Users\...\Pictures` |
| `$VIDEO` | 视频目录 | `C:\Users\...\Videos` |
| `$AUDIO` | 音频目录 | `C:\Users\...\Music` |
| `$TEMP` | 临时目录 | `C:\Users\...\AppData\Local\Temp` |
| `$RESOURCE` | 资源目录 | 应用打包资源 |

### 路径模式

```json
{
  "identifier": "fs:allow-read-text-file",
  "allow": [
    { "path": "$APPDATA/**" },
    { "path": "$HOME/documents/*.txt" }
  ]
}
```

### 递归匹配

- `**` - 匹配所有文件和目录
- `*` - 匹配当前目录下的所有文件

### 示例

```json
{
  "permissions": [
    {
      "identifier": "fs:allow-read-text-file",
      "allow": [
        { "path": "$APPDATA/**" },
        { "path": "$HOME/documents/**" },
        { "path": "$DOWNLOAD/reports/*.pdf" }
      ]
    },
    {
      "identifier": "fs:allow-write-text-file",
      "allow": [
        { "path": "$APPDATA/*.json" }
      ]
    }
  ]
}
```

## HTTP Scope

### URL 模式

```json
{
  "identifier": "http:allow-fetch",
  "allow": [
    { "url": "https://api.example.com/**" },
    { "url": "https://*.github.com/**" }
  ]
}
```

### 通配符

- `**` - 匹配所有路径
- `*` - 匹配单个路径段

### 示例

```json
{
  "permissions": [
    {
      "identifier": "http:default",
      "allow": [
        { "url": "https://api.example.com/**" },
        { "url": "https://*.service.com/api/**" }
      ]
    }
  ]
}
```

## Shell Scope

### 命令白名单

```json
{
  "identifier": "shell:allow-execute",
  "allow": [
    {
      "name": "git",
      "cmd": "git",
      "args": true
    },
    {
      "name": "npm",
      "cmd": "npm",
      "args": [
        "run",
        "dev",
        "build"
      ]
    }
  ]
}
```

### 打开 URL

```json
{
  "identifier": "shell:allow-open",
  "allow": [
    { "url": "https://**" },
    { "url": "http://**" },
    { "url": "mailto:**" }
  ]
}
```

## 拒绝规则

```json
{
  "permissions": [
    {
      "identifier": "fs:allow-read",
      "allow": [
        { "path": "$HOME/**" }
      ],
      "deny": [
        { "path": "$HOME/.ssh/**" },
        { "path": "$HOME/.env" }
      ]
    }
  ]
}
```

## 完整示例

```json
{
  "identifier": "main-capability",
  "windows": ["main"],
  "permissions": [
    {
      "identifier": "fs:allow-read-text-file",
      "allow": [
        { "path": "$APPDATA/**" },
        { "path": "$HOME/documents/**" }
      ]
    },
    {
      "identifier": "fs:allow-write-text-file",
      "allow": [
        { "path": "$APPDATA/**" }
      ]
    },
    {
      "identifier": "http:allow-fetch",
      "allow": [
        { "url": "https://api.example.com/**" }
      ]
    },
    {
      "identifier": "shell:allow-open",
      "allow": [
        { "url": "https://**" },
        { "url": "mailto:**" }
      ]
    }
  ]
}
```
