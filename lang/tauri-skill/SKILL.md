---
name: tauri-skills
version: v2.0.0
author: book-skills
description: Tauri v2 桌面应用开发指导技能 — 提供架构决策、IPC 设计、权限安全、性能优化等生产级开发指导，覆盖项目初始化到发布全流程的最佳实践与反模式避免
tags: [tauri, rust, desktop-app, cross-platform, ipc, security, webview, vue, react, svelte]
dependency:
  parent: none
---

# Tauri v2 开发指导

## 任务目标

指导开发者使用 Tauri v2 构建生产级桌面应用。聚焦**架构决策、模式选择和陷阱避免**，而非 API 教程或安装步骤。

核心价值：帮助开发者在每个关键决策点做出正确选择。

## 触发条件

用户需要以下任一场景时使用：
- 新建 Tauri 项目并进行架构设计
- 实现/重构前后端通信（IPC）
- 配置权限与安全策略
- 解决性能问题或内存占用过高
- 处理跨平台兼容性问题
- 准备应用发布与分发

## 核心架构

```
┌─────────────────────────────────────────────────────────────┐
│                      Tauri Application                       │
│                                                             │
│  ┌──────────────────────┐   IPC    ┌─────────────────────┐  │
│  │   WebView (Frontend)  │ <──────> │   Tauri Core (Rust) │  │
│  │                      │ JSON/    │                     │  │
│  │  · UI + Routing      │ Channel │  · Commands          │  │
│  │  · Local State       │         │  · Event Bus         │  │
│  │  · Data Fetching     │         │  · Channels<T>       │  │
│  │  · Typed invoke()    │         │  · Managed State     │  │
│  └──────────────────────┘         └──────────┬──────────┘  │
│                                             │              │
└─────────────────────────────────────────────┼──────────────┘
                                              │
                    ┌─────────────────────────┘
                    ▼
     ┌─────────────────────────────────────┐
     │  OS APIs / Filesystem / Network / DB  │
     └─────────────────────────────────────┘
```

### 三条铁律

1. **Commands = 请求/响应**：JS 调用 `invoke`，Rust 返回 `Result<T>`
2. **Events = 广播订阅**：fire-and-forget，任意端可 emit/listen
3. **Channels = 有序流**：Rust → JS 的类型化单向数据流（v2 新增）

> 所有跨越边界的数据都会被序列化（JSON）。**设计时必须考虑序列化成本**。

---

## 开发决策流程

### 阶段一：项目初始化

#### 技术栈选择

| 前端框架 | 适用场景 | 社区成熟度 |
|---------|---------|-----------|
| React | 复杂 UI、大型团队、生态需求 | ★★★★★ |
| Vue 3 | 快速开发、渐进式、中文社区强 | ★★★★☆ |
| Svelte | 极致性能、轻量级、编译时优化 | ★★★☆☆ |
| Solid | 高性能响应式、类 React 语法 | ★★★☆☆ |

**决策依据**：团队熟悉度 > 项目复杂度 > 性能要求 > 包体积敏感度

#### 必做初始化清单

```bash
# 1. 创建项目
npm create tauri-app@latest my-app

# 2. 立即修复的配置项（首次提交前）
# - tauri.conf.json: identifier 设为反向 DNS (com.mycompany.app)
# - tsconfig.json: 启用 strict + exactOptionalPropertyTypes + noUncheckedIndexedAccess
# - rust-toolchain.toml: 锁定 Rust 版本
# - 生成 updater 密钥: npx @tauri-apps/cli signer generate
```

> ⚠️ **反模式**：发布后才改 `identifier` 会破坏通知、自启动、用户数据目录。

### 阶段二：类型契约设计

#### IPC 类型共享策略（按优先级排序）

| 方案 | 工具 | 适用场景 |
|------|------|---------|
| **A: 从 Rust 生成 TS** | `specta` + `tauri-specta` 或 `ts-rs` | ✅ 首选，Rust 为单一真相源 |
| B: OpenAPI 层生成 | 自定义脚本 | 命令已封装 REST 风格服务 |
| C: 手动维护 | `src/bindings/` 目录 | 小项目，每次 PR 审计 |

**Serde 枚举映射建议**：

```rust
// 推荐：内部标签（与 TS discriminated union 对齐）
#[serde(tag = "type")]
enum CommandResult {
    Success { data: String },
    Error { code: u32, message: String },
}

// 或邻接标签（更紧凑）
#[serde(tag = "type", content = "data")]
enum CommandResult { ... }
```

> ⚠️ **反模式**：默认的外部标签 `{"Success": {...}}` 与 TS 联合类型不自然对齐。

### 阶段三：IPC 边界设计

#### Commands 设计原则

```rust
// ✅ 正确：薄命令层，委托给服务层
#[tauri::command]
async fn get_user(id: u32, state: State<'_, AppState>) -> Result<User, AppError> {
    validate_id(id)?;                          // 输入验证
    state.user_service().get_user(id).await     // 业务逻辑
}

// ❌ 错误：胖命令，包含业务逻辑
#[tauri::command]
async fn get_user_bad(id: u32) -> Result<User, String> {
    // 直接在这里写 SQL / 业务逻辑...
}
```

**前端调用封装规范**：

```typescript
// src/ipc/user.ts — 统一 IPC 调用层
import { invoke } from '@tauri-apps/api/core';
import type { User } from '@/bindings';

export async function getUser(id: number): Promise<User> {
  return invoke<User>('get_user', { id });
}

// ❌ 禁止：在组件中直接 invoke('get_user', ...)
```

#### Events 使用准则

| 场景 | 用 Events? | 替代方案 |
|------|-----------|---------|
| 全局配置变更通知 | ✅ | — |
| 窗口焦点变化 | ✅ | — |
| 后台任务进度 | ❌ 用 Channels | `Channel<Progress>` |
| 需要类型安全 | ❌ 用 Commands | request/response |
| 单向通知多窗口 | ✅ | `window.emit()` |

```typescript
// ✅ 正确：必须在 cleanup 中注销
useEffect(() => {
  const unlisten = listen('config-changed', () => {
    queryClient.invalidateQueries({ queryKey: ['config'] });
  });
  return () => { unlisten.then(fn => fn()); };
}, []);
```

#### Channels 使用场景

高频、有序、Rust → JS 的数据流：
- 文件下载进度
- 日志实时输出
- 长时间计算的状态更新

```rust
use tauri::ipc::Channel;

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Progress {
    pub bytes_done: u64,
    pub bytes_total: u64,
}

#[tauri::command]
async fn download_with_progress(url: String, channel: Channel<Progress>) -> Result<(), AppError> {
    channel.send(Progress { bytes_done: 0, bytes_total: 1000 })?;
    Ok(())
}
```

### 阶段四：权限与安全

#### Capability 设计模式

```json
{
  "identifier": "main-window",
  "description": "主窗口能力",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "dialog:allow-open",
    "fs:allow-read-text-file",
    {"identifier": "fs:scope", "allow": [{"path": "$APPDATA/**"}]}
  ]
}
```

**最小权限原则**：
1. 从 `core:default` 开始
2. 每添加一个功能，才添加对应权限
3. 使用 Scope 限制文件系统访问范围
4. 不同窗口可分配不同 capability

#### 输入验证清单

| 检查项 | 验证方式 | 风险 |
|--------|---------|------|
| 字符串长度 | 拒绝空串 / 限制上限 | DoS |
| 数值范围 | cap 合理值 | 资源耗尽 |
| 文件路径 | canonicalize + 检查根目录 | 路径遍历 (`../../etc/passwd`) |
| Shell 输入 | 禁止字符串插值，使用参数向量 | 命令注入 |

### 阶段五：错误处理

#### Rust 端错误模式

```rust
#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("IO 错误: {0}")]
    Io(#[from] std::io::Error),
    #[error("数据库错误: {0}")]
    Db(#[from] sqlx::Error),
    #[error("未授权")]
    Unauthorized,
    #[error("资源不存在: {0}")]
    NotFound(String),
}

impl serde::Serialize for AppError {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where S: serde::Serializer {
        serializer.serialize_str(&self.to_string())
    }
}
```

> ⚠️ **致命反模式**：**不要用 `anyhow::Error` 作为命令返回类型** —— 它不实现 `Serialize`，会导致编译失败。`anyhow` 仅用于 `main.rs` 和测试代码。

#### TypeScript 端异步状态模式

```typescript
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

function assertNever(x: never): never {
  throw new Error(`Unhandled case: ${x}`);
}
```

### 阶段六：性能优化

#### 优化优先级表

| 优化项 | 影响 | 成本 |
|--------|------|------|
| 减少 IPC 调用次数 | ★★★★★ | 低 |
| 批量/合并请求 | ★★★★☆ | 低 |
| 使用 Channels 替代轮询 | ★★★★☆ | 中 |
| 密集计算放 Rust 端 | ★★★★☆ | 中 |
| 控制序列化 payload 大小 | ★★★☆☆ | 低 |
| 避免阻塞主线程 | ★★★★★ | 中 |

#### 异步陷阱

```rust
// ❌ 致命：std::sync::Mutex 跨 await 导致死锁
let guard = state.std_mutex.lock().unwrap();
some_async_call().await;  // 运行时被阻塞！

// ✅ 正确：使用 tokio::sync::Mutex
let guard = state.tokio_mutex.lock().await;
some_async_call().await;  // 异步感知
```

**禁止在 async 上下文中使用**：
- `std::fs::*` → 用 `tokio::fs::*`
- `ureq` / `reqwest::blocking` → 用 `reqwest`
- `std::thread::sleep` → 用 `tokio::time::sleep`
- `std::sync::Mutex` → 用 `tokio::sync::Mutex`

### 阶段七：构建与发布

#### 构建优化

```bash
# 开发环境：增量编译
cargo build          # 利用 sccache 进一步加速

# 发布构建
npm run tauri build  # 自动执行 cargo --release
```

#### 分发检查清单

- [ ] `tauri.conf.json` 的 `identifier` 已设置
- [ ] 应用图标已配置（32x32, 128x128, ico/icns/png）
- [ ] updater 公私钥已生成并安全存储
- [ ] CSP 已正确配置（非 null）
- [ ] Windows: 代码签名证书就绪
- [ ] macOS: Apple Developer ID 证书就绪
- [ ] 各平台测试通过

---

## 反模式速查

| 反模式 | 正确做法 | 后果 |
|--------|---------|------|
| anyhow::Error 作返回类型 | 自定义 AppError + Serialize | 编译失败 |
| std::sync::Mutex 跨 .await | tokio::sync::Mutex | 死锁 |
| 组件内直接 invoke() | 封装到 src/ipc/ | 无法统一处理错误/日志 |
| 宽开权限后收紧 | 最小权限逐步添加 | 安全漏洞 |
| 不检查 WebView 平台差异 | 各平台测试 | 渲染不一致 |
| 大 payload 频繁 IPC | 批量/流式/Channels | 性能下降 |
| .unwrap() / .expect() 在命令中 | ? 传播到 AppError | 前端收到模糊错误 |
| 手动维护 TS/Rust 双份类型 | specta 自动生成 | 类型不同步导致运行时崩溃 |

---

## API 参考

完整的 API 文档索引见 [reference/index.md](reference/index.md)。

### 常用模块快速定位

| 需求 | 模块文档 |
|------|---------|
| 文件对话框 | [dialog](reference/javascript-modules/dialog.md) |
| 文件系统操作 | [fs](reference/javascript-modules/fs.md) |
| Shell 命令 | [shell](reference/javascript-modules/shell.md) |
| HTTP 请求 | [http](reference/javascript-modules/http.md) |
| 系统通知 | [notification](reference/javascript-modules/notification.md) |
| 剪贴板 | [clipboard-manager](reference/javascript-modules/clipboard-manager.md) |
| 自动更新 | [updater](reference/javascript-modules/updater.md) |
| 本地存储 | [store](reference/javascript-modules/store.md) |
| 窗口管理 | [window](reference/javascript-api/window.md) |
| 多窗口 | [webview-window](reference/javascript-api/webview-window.md) |
| 系统托盘 | [tray](reference/javascript-api/tray.md) |
| 权限配置 | [capability](reference/acl/capability.md) |
| 全局配置 | [config](reference/config.md) |

---

## 注意事项

### Tauri v2 vs v1 关键变更

- **权限系统重写**：Allowlist → Capability + Permission + Scope
- **IPC 重写**：自定义协议，性能大幅提升
- **插件分离**：核心功能移至插件（fs, shell, http 等）
- **移动端支持**：iOS/Android（稳定中）

### WebView 平台差异

| 平台 | WebView 引擎 | 注意事项 |
|------|-------------|---------|
| macOS/iOS | WKWebView | CSS `-webkit-` 前缀 |
| Windows | WebView2 (Edge) | 最新 ES 特性支持最好 |
| Linux | WebKitGTK | 版本可能较旧，需测试 |

### Rust 编译优化

- 安装 `sccache` 缓存编译结果
- 在 `Cargo.toml` 中为 release 启用 LTO：`[profile.release].opt-level = "z"` （更小的二进制）
- 首次编译较慢，后续增量编译快

### 生产环境必做

1. **CSP 配置**：不要设为 `null`，定义明确的安全策略
2. **代码签名**：Windows (signtool), macOS (codesign)
3. **Updater 配置**：提前生成密钥对
4. **权限审计**：定期审查 capability 配置
