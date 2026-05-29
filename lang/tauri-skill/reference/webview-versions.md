# WebView 版本参考

本文档列出各平台使用的 WebView 组件及其版本信息。

## Windows

### WebView2

Windows 10/11 使用 Microsoft Edge WebView2。

| 操作系统 | WebView2 版本 |
|----------|---------------|
| Windows 10 (21H2+) | 内置 |
| Windows 11 | 内置 |
| Windows 10 (旧版本) | 需要安装 |

### WebView2 最低版本

- **Evergreen**: 自动更新版本
- **Fixed Version**: 固定版本号

```json
{
  "app": {
    "windows": [
      {
        "webviewInstallMode": {
          "type": "downloadBootstrapper"
        }
      }
    ]
  }
}
```

### WebView2 安装模式

```json
{
  "app": {
    "windows": [
      {
        "webviewInstallMode": {
          "type": "embedBootstrapper",
          "silent": true
        }
      }
    ]
  }
}
```

**安装模式类型：**

| 类型 | 说明 |
|------|------|
| `downloadBootstrapper` | 下载引导程序 |
| `embedBootstrapper` | 内置引导程序 |
| `installWebview` | 安装 WebView2（需要管理员） |
| `none` | 不安装 |

## macOS

### WKWebView

macOS 使用 WebKit 的 WKWebView。

| macOS 版本 | WKWebView 版本 |
|------------|----------------|
| macOS 13+ | 最新 |
| macOS 12 | 旧版 |
| macOS 11 | 旧版 |

### 特性支持

- **Safari WebKit**: 自动使用系统版本
- **Privacy**: 隐私保护功能
- **Process Pool**: 共享进程池

## Linux

### WebKitGTK

Linux 使用 WebKitGTK。

| 发行版 | WebKitGTK 版本 |
|--------|----------------|
| Ubuntu 22.04+ | 4.1+ |
| Fedora | 4.1+ |
| Arch | 4.1+ |

### 安装依赖

```bash
# Ubuntu/Debian
sudo apt install libwebkit2gtk-4.1-dev

# Fedora
sudo dnf install webkit2gtk4.1-devel

# Arch
sudo pacman -S webkit2gtk-4.1
```

## iOS

### WKWebView

iOS 同样使用 WKWebView。

| iOS 版本 | WKWebView 版本 |
|----------|----------------|
| iOS 16+ | 最新 |
| iOS 15 | 旧版 |
| iOS 14 | 旧版 |

## Android

### Android WebView

Android 使用 Android System WebView。

| Android 版本 | WebView 版本 |
|--------------|--------------|
| Android 12+ | Chromium 90+ |
| Android 11 | Chromium 83+ |
| Android 10 | Chromium 79+ |

## 版本检测

### 前端检测

```javascript
// 检测 WebView 类型
const isWebView2 = navigator.userAgent.includes('Edg/');
const isWebKit = navigator.userAgent.includes('AppleWebKit');
const isGecko = navigator.userAgent.includes('Gecko');
```

### Rust 检测

```rust
use tauri::Manager;

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let webview = app.get_webview_window("main").unwrap();
            // 获取 WebView 信息
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## WebView 配置

### Windows WebView2 配置

```json
{
  "app": {
    "windows": [
      {
        "devtools": true
      }
    ]
  }
}
```

### macOS WKWebView 配置

```json
{
  "app": {
    "windows": [
      {
        "allowFileAccess": true,
        "allowUniversalAccessFromFileURLs": true
      }
    ]
  }
}
```

### Linux WebKitGTK 配置

无特殊配置要求。

## 常见问题

### WebView2 未安装

用户会看到安装提示，引导下载 WebView2。

### macOS 混合内容

确保使用 HTTPS 避免混合内容警告。

### Linux 依赖缺失

确保安装所有必需的 WebKitGTK 依赖。
