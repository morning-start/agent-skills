# Tauri v2 API 参考

本目录包含 Tauri v2 桌面应用框架的完整 API 参考文档。**这些是 API 索引，用于查阅具体用法**。开发决策和最佳实践请参见 [SKILL.md](../SKILL.md)。

## 目录结构

```
reference/
├── javascript-api/      # 核心 JavaScript API
│   ├── app.md           # 应用生命周期
│   ├── core.md          # 核心 invoke/事件
│   ├── window.md        # 窗口管理
│   ├── webview-window.md # 多窗口管理
│   ├── webview.md       # WebView 控制
│   ├── tray.md          # 系统托盘
│   ├── menu.md          # 菜单系统
│   ├── event.md         # 事件系统
│   ├── path.md          # 路径解析
│   ├── image.md         # 图像处理
│   ├── dpi.md           # DPI 感知
│   └── mocks.md         # 测试 Mock
├── javascript-modules/  # 插件模块（按需启用）
│   ├── fs.md            # 文件系统
│   ├── dialog.md        # 文件对话框
│   ├── shell.md         # Shell 命令
│   ├── http.md          # HTTP 客户端
│   ├── notification.md  # 系统通知
│   ├── store.md         # 键值存储
│   ├── updater.md       # 自动更新
│   ├── clipboard-manager.md # 剪贴板
│   ├── sql.md           # 数据库
│   ├── stronghold.md     # 加密存储
│   ├── os.md            # 操作系统信息
│   └── ...              # (共 26 个模块)
├── acl/                # 权限与安全
│   ├── capability.md    # 能力配置
│   ├── permission.md    # 权限定义
│   ├── scope.md         # 作用域限制
│   └── core-permissions.md # 核心权限列表
├── config.md           # tauri.conf.json 配置详解
├── cli.md              # CLI 命令行工具
├── environment-variables.md # 环境变量参考
└── webview-versions.md # WebView 版本兼容性
```

## 快速定位

### IPC 通信

| 需求 | 文档 |
|------|------|
| invoke 调用 | [core](javascript-api/core.md) |
| 事件监听/发射 | [event](javascript-api/event.md) |
| Channels 流式数据 | [core](javascript-api/core.md) |

### 系统集成

| 需求 | 文档 |
|------|------|
| 文件读写 | [fs](javascript-modules/fs.md) |
| 文件选择对话框 | [dialog](javascript-modules/dialog.md) |
| 执行外部命令 | [shell](javascript-modules/shell.md) |
| HTTP 请求 | [http](javascript-modules/http.md) |
| 系统通知 | [notification](javascript-modules/notification.md) |
| 剪贴板操作 | [clipboard-manager](javascript-modules/clipboard-manager.md) |

### UI 与窗口

| 需求 | 文档 |
|------|------|
| 窗口控制 | [window](javascript-api/window.md) |
| 多窗口管理 | [webview-window](javascript-api/webview-window.md) |
| WebView 控制 | [webview](javascript-api/webview.md) |
| 系统托盘 | [tray](javascript-api/tray.md) |
| 菜单 | [menu](javascript-api/menu.md) |

### 数据持久化

| 需求 | 文档 |
|------|------|
| 键值存储 | [store](javascript-modules/store.md) |
| SQL 数据库 | [sql](javascript-modules/sql.md) |
| 加密存储 | [stronghold](javascript-modules/stronghold.md) |

### 权限安全

| 需求 | 文档 |
|------|------|
| Capability 配置 | [capability](acl/capability.md) |
| 权限列表 | [permission](acl/permission.md) |
| Scope 作用域 | [scope](acl/scope.md) |
| 核心权限 | [core-permissions](acl/core-permissions.md) |

### 发布与运维

| 需求 | 文档 |
|------|------|
| 自动更新 | [updater](javascript-modules/updater.md) |
| 全局配置 | [config](config.md) |
| CLI 工具 | [cli](cli.md) |
| 环境变量 | [environment-variables](environment-variables.md) |
