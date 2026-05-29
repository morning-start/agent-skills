# 环境变量参考

本文档列出 Tauri 支持的环境变量。

## Tauri 环境变量

### TAURI_DEBUG

开启调试模式。

```bash
# Windows
set TAURI_DEBUG=1

# Linux/macOS
export TAURI_DEBUG=1
```

### TAURI_DEV_WATCHER

在开发模式下启用文件监视。

```bash
export TAURI_DEV_WATCHER=1
```

### TAURI_SIGNING_PRIVATE_KEY

用于应用签名的私钥路径。

```bash
export TAURI_SIGNING_PRIVATE_KEY=/path/to/private.key
```

### TAURI_SIGNING_PRIVATE_KEY_PASSWORD

签名私钥的密码。

```bash
export TAURI_SIGNING_PRIVATE_KEY_PASSWORD=password
```

### TAURI_BUILD_TARGET

指定构建目标平台。

```bash
# Windows x64
export TAURI_BUILD_TARGET=x86_64-pc-windows-msvc

# macOS ARM
export TAURI_BUILD_TARGET=aarch64-apple-darwin

# Linux
export TAURI_BUILD_TARGET=x86_64-unknown-linux-gnu
```

## Rust 环境变量

### RUST_BACKTRACE

启用 Rust 堆栈跟踪。

```bash
# 启用
export RUST_BACKTRACE=1

# 完整堆栈跟踪
export RUST_BACKTRACE=full
```

### RUST_LOG

设置日志级别。

```bash
# 级别: error, warn, info, debug, trace
export RUST_LOG=info
export RUST_LOG=tauri=debug
export RUST_LOG=my_app=trace,warn
```

### RUST_MIN_STACK

设置最小堆栈大小。

```bash
export RUST_MIN_STACK=16777216
```

### CARGO_HOME

指定 Cargo 目录。

```bash
export CARGO_HOME=/path/to/cargo
```

### RUSTUP_HOME

指定 Rustup 目录。

```bash
export RUSTUP_HOME=/path/to/rustup
```

## 窗口环境变量

### TAURI_WINDOW_WIDTH

设置窗口宽度。

```bash
export TAURI_WINDOW_WIDTH=800
```

### TAURI_WINDOW_HEIGHT

设置窗口高度。

```bash
export TAURI_WINDOW_HEIGHT=600
```

### TAURI_WINDOW_TITLE

设置窗口标题。

```bash
export TAURI_WINDOW_TITLE="My App"
```

### TAURI_WINDOW_FULLSCREEN

设置全屏模式。

```bash
export TAURI_WINDOW_FULLSCREEN=1
```

### TAURI_WINDOW_RESIZABLE

设置是否可调整大小。

```bash
export TAURI_WINDOW_RESIZABLE=1
```

## 开发环境变量

### TAURI_CLI_CONFIG

指定 Tauri CLI 配置文件路径。

```bash
export TAURI_CLI_CONFIG=/path/to/tauri.conf.json
```

### NODE_OPTIONS

Node.js 选项（用于 Vite 开发服务器）。

```bash
export NODE_OPTIONS="--max-old-space-size=4096"
```

## 生产环境变量

### TAURI_DISABLE_ANALYTICS

禁用分析数据收集。

```bash
export TAURI_DISABLE_ANALYTICS=1
```

### APPIMAGE_EXTRACT_AND_RUN

在 AppImage 中启用提取和运行模式。

```bash
export APPIMAGE_EXTRACT_AND_RUN=1
```

## 使用示例

### 在 package.json 中配置

```json
{
  "scripts": {
    "tauri:dev": "TAURI_DEBUG=1 RUST_LOG=info npm run tauri dev"
  }
}
```

### 在 .env 文件中配置

```
TAURI_DEBUG=1
RUST_LOG=info
RUST_BACKTRACE=1
```
