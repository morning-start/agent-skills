# CLI 命令行参考

本文档包含 Tauri CLI 的命令行使用指南。

## 安装

```bash
# 使用 npm
npm install -D @tauri-apps/cli@latest

# 使用 cargo
cargo install tauri-cli
```

## 常用命令

### 开发

```bash
# 启动开发服务器
npm run tauri dev

# 指定端口
npm run tauri dev -- --port 5173

# 开启调试
npm run tauri dev -- --inspect-brk
```

### 构建

```bash
# 构建生产版本
npm run tauri build

# 指定目标平台
npm run tauri build -- --target x86_64-pc-windows-msvc
npm run tauri build -- --bundles msi
npm run tauri build -- --bundles nsis
```

### 项目管理

```bash
# 初始化新项目
npm create tauri-app@latest

# 添加插件
npm run tauri add dialog
npm run tauri add fs

# 查看版本
npm run tauri -- --version

# 查看帮助
npm run tauri -- --help
```

## Tauri CLI 子命令

| 命令 | 说明 |
|------|------|
| `init` | 初始化 Tauri 项目 |
| `dev` | 启动开发服务器 |
| `build` | 构建生产版本 |
| `bundle` | 生成安装包 |
| `icon` | 生成应用图标 |
| `sign` | 代码签名 |
| `info` | 查看项目信息 |

## 配置文件

Tauri CLI 使用 `tauri.conf.json` 配置文件：

```json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devUrl": "http://localhost:5173",
    "frontendDist": "../dist"
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": ["icons/32x32.png", "icons/128x128.png"]
  }
}
```
