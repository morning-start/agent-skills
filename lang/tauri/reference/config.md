# 配置参考

本文档包含 Tauri `tauri.conf.json` 配置文件的详细说明。

## 基本结构

```json
{
  "productName": "My App",
  "version": "1.0.0",
  "identifier": "com.myapp.app",
  "build": {},
  "app": {},
  "bundle": {}
}
```

## 配置项说明

### productName

应用名称，将用于窗口标题和安装包名称。

```json
"productName": "My App"
```

### version

应用版本号。

```json
"version": "1.0.0"
```

### identifier

应用唯一标识符，格式：`com.domain.app`。

```json
"identifier": "com.myapp.app"
```

## build 配置

```json
"build": {
  "beforeDevCommand": "npm run dev",
  "beforeBuildCommand": "npm run build",
  "devUrl": "http://localhost:5173",
  "frontendDist": "../dist",
  "devtools": true
}
```

| 配置项 | 说明 |
|--------|------|
| beforeDevCommand | 开发模式前执行的命令 |
| beforeBuildCommand | 构建前执行的命令 |
| devUrl | 开发服务器 URL |
| frontendDist | 前端构建输出目录 |
| devtools | 开启开发者工具 |

## app 配置

```json
"app": {
  "withGlobalTauri": true,
  "windows": [
    {
      "title": "My App",
      "label": "main",
      "width": 800,
      "height": 600,
      "minWidth": 400,
      "minHeight": 300,
      "resizable": true,
      "fullscreen": false,
      "center": true,
      "decorations": true,
      "transparent": false,
      "alwaysOnTop": false
    }
  ],
  "security": {
    "csp": null
  }
}
```

### windows 配置

| 属性 | 说明 | 默认值 |
|------|------|--------|
| title | 窗口标题 | - |
| label | 窗口标签 | - |
| width | 窗口宽度 | 800 |
| height | 窗口高度 | 600 |
| minWidth | 最小宽度 | - |
| minHeight | 最小高度 | - |
| resizable | 是否可调整大小 | true |
| fullscreen | 是否全屏 | false |
| center | 是否居中 | false |
| decorations | 是否显示标题栏 | true |
| transparent | 是否透明 | false |
| alwaysOnTop | 是否置顶 | false |

### security 配置

| 属性 | 说明 |
|------|------|
| csp | 内容安全策略 |

## bundle 配置

```json
"bundle": {
  "active": true,
  "targets": "all",
  "icon": [
    "icons/32x32.png",
    "icons/128x128.png",
    "icons/128x128@2x.png",
    "icons/icon.icns",
    "icons/icon.ico"
  ],
  "resources": [],
  "copyright": "Copyright © 2024",
  "category": "Utility",
  "shortDescription": "My App Description",
  "longDescription": "Long description of my app",
  "windows": {
    "certificateThumbprint": null,
    "digestAlgorithm": "sha256",
    "timestampUrl": ""
  }
}
```

### targets

打包目标平台：
- `"all"` - 所有平台
- `["msi", "nsis"]` - 仅 Windows
- `["app", "dmg"]` - 仅 macOS
- `["deb", "rpm", "appimage"]` - 仅 Linux

## 环境变量

Tauri 支持多种环境变量：

| 变量 | 说明 |
|------|------|
| `TAURI_DEBUG` | 开启调试模式 |
| `TAURI_ENV_*` | 自定义环境变量 |
| `RUST_BACKTRACE` | Rust 堆栈跟踪 |
