---
name: rust
version: v2.1.0
author: book-skills
description: Use when the user asks about Rust project setup, architecture decisions, crate selection, ownership, lifetimes, concurrency, async, error handling, performance, deployment, or production patterns.
tags: [rust, systems-programming, cli, web, embedded, blockchain, game-dev, desktop, performance, concurrency, async]
dependency:
  parent: none
  children:
    - rust-ownership-skill
    - rust-concurrency-skill
    - rust-error-handling-skill
    - rust-async-skill
    - rust-cli-project-skill
---

# Rust 开发指导

## 任务目标

指导开发者使用 Rust 构建各领域生产级应用。聚焦**领域选择、架构决策、模式选择和陷阱避免**，而非语法教程或 API 文档。

核心价值：帮助开发者在每个关键决策点做出正确选择。

## 使用原则

- 先判断问题落在哪一层：语言机制、设计选择，还是领域约束
- 默认组合 `1` 个基础技能 + `1` 个领域或横切技能，避免一次加载过多技能
- 遇到错误、性能、并发和安全问题时，优先切到对应专门技能，而不是在总技能里硬讲
- 参考文档只承载补充信息，主技能负责路由和决策

## 触发条件

用户需要以下任一场景时使用：
- 新建 Rust 项目并确定技术方向/架构设计
- 选择框架或 crate（Web/CLI/嵌入式等）
- 处理所有权、生命周期、并发问题
- 设计错误处理策略
- 性能优化或内存调优
- 准备发布到 crates.io 或生产环境

## Rust 能做什么：应用领域全景

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Rust 应用领域全景图                            │
├─────────────┬─────────────┬─────────────┬───────────────────────────┤
│   系统工具   │   Web 服务   │   数据系统   │      桌面/客户端          │
├─────────────┼─────────────┼─────────────┼───────────────────────────┤
│ · ripgrep   │ · axum      │ · Databend  │ · Tauri                  │
│ · fd        │ · actix-web │ · GreptimeDB│ · Slint UI               │
│ · bat       │ · rocket    │ · Qdrant    │ · Alacritty              │
│ · eza       │ · poem      │ · SurrealDB │ · cosmic-text            │
│ · zoxide    │ · warp      │ · Redpanda  │                         │
│ · just      │             │ · sled      │                         │
│ · starship  │             │             │                         │
├─────────────┼─────────────┼─────────────┼───────────────────────────┤
│   区块链     │   嵌入式/IoT  │   游戏开发   │   AI/ML                 │
├─────────────┼─────────────┼─────────────┼───────────────────────────┤
│ · Solana    │ · RTIC      │ · Bevy      │ · candle (HF)            │
│ · Polkadot  │ · embassy   │ · Fyrox     │ · burn                   │
│ · Zcash     │ · no_std    │ · ggez      │ · tch-rs                 │
│ · sui       │ · STM32     │ · macroquad │                         │
│ · Starknet  │ · RISC-V    │ · Embark    │                         │
└─────────────┴─────────────┴─────────────┴───────────────────────────┘
```

### 领域选择决策矩阵

| 你的需求 | 推荐方向 | 核心框架/crate |
|---------|---------|---------------|
| 高性能命令行工具 | **CLI 开发** | clap, tokio, anyhow, ratatui |
| HTTP API / 微服务 | **Web 服务** | axum / actix-web + sqlx + tower |
| 桌面跨平台应用 | **桌面应用** | Tauri (WebView) / Slint (原生) |
| 实时游戏 | **游戏开发** | Bevy (ECS) / macroquad (简单) |
| MCU 固件 / IoT | **嵌入式** | embassy / RTIC + PAC/HAL |
| 分布式账本 | **区块链** | Substrate / Anchor / sui-framework |
| 向量搜索 / 时序数据 | **数据库** | Qdrant / GreptimeDB (使用) 或从头构建 |
| 编译器 / 语言工具 | **编译器基础设施** | chumsky / rowan / codespan |

---

## 项目架构决策

### 模块 vs Crate：当前共识

> **"Module First, Crate Last"** — 过度拆分 crate 会带来"编译税"

```toml
# ✅ 正确：大多数项目用模块即可
my-app/
├── src/
│   ├── main.rs          # 入口
│   ├── lib.rs           # pub use 重导出
│   ├── config.rs        # 配置管理
│   ├── error.rs         # 错误类型定义
│   ├── domain/          # 领域模型
│   │   ├── mod.rs
│   │   └── user.rs
│   ├── infrastructure/  # 基础设施
│   │   ├── mod.rs
│   │   └── database.rs
│   └── handlers/        # 处理层 (Web)
│       └── mod.rs
```

**何时必须拆分 crate**：
1. 需要**过程宏**（Procedural Macro）—— 语言强制要求独立 crate
2. 需要**编译器级别的边界隔离** —— 确保 Module A 无法看到 Module B 的私有内部
3. 需要**编译并行加速** —— 两个大型独立模块可以同时编译

### 标准项目模板结构

```
project-name/
├── Cargo.toml              # workspace 根（如需要）
├── rust-toolchain.toml     # 锁定 Rust 版本！
├── crates/                 # 仅在需要时
│   ├── core/
│   └── cli/
├── src/
│   ├── main.rs / lib.rs
│   ├── error.rs            # 统一错误类型（必做）
│   ├── config.rs           # 配置加载
│   └── ...
├── tests/                  # 集成测试
├── benches/                # 基准测试
├── migrations/             # 数据库迁移（如适用）
└── configuration/          # 环境配置文件
```

### 错误处理架构（生产级）

```rust
// ✅ 正确：统一 AppError + thiserror + 结构化错误码
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("IO 错误: {0}")]
    Io(#[from] std::io::Error),

    #[error("数据库错误: {0}")]
    Database(#[from] sqlx::Error),

    #[error("配置错误: {0}")]
    Config(String),

    #[error("未授权访问")]
    Unauthorized,

    #[error("资源不存在: {0}")]
    NotFound(String),

    #[error("上游服务不可用: {source}, service={service}")]
    Upstream {
        source: reqwest::Error,
        service: String,
    },
}

// 为序列化场景实现 Serialize（如 IPC/Web）
impl serde::Serialize for AppError {
    fn serialize<S>(&self, s: S) -> Result<S::Ok, S::Error>
    where S: serde::Serializer {
        s.serialize_str(&self.to_string())
    }
}
```

> ⚠️ **致命反模式**：不要在库代码中使用 `anyhow` —— 它不实现 `Serialize`。`anyhow` 仅用于 `main.rs` 和二进制入口。

---

## 并发与异步模式

### 异步运行时选择

| 运行时 | 适用场景 | 特点 |
|--------|---------|------|
| **tokio** | 90% 的异步项目 | 全功能、最成熟、行业标准 |
| **async-std** | 简单异步 I/O | API 更接近 std，但生态较小 |
| **smol** | 嵌入式/资源受限 | 极简、可组合 |

### 生产环境反模式速查

| 反模式 | 后果 | 正确做法 |
|--------|------|---------|
| `std::sync::Mutex` 跨 `.await` | **死锁**（无声无息） | 使用 `tokio::sync::Mutex` |
| 无界 channel 缓冲区 | **OOM**（Rust 不防内存泄漏） | 小缓冲区 + 显式背压处理 |
| `.unwrap()` / `.expect()` 在库中 | 生产 panic = 进程崩溃 | 用 `?` 传播到 `AppError` |
| `Box<dyn Trait>` 在热路径 | **性能悬崖**（vtable 间接调用） | 泛型单态化或内联缓存 |
| `clone()` 大型数据 | 不必要的堆分配 | 引用 / `Cow<T>` / `Arc` |
| 阻塞操作在 async 中 | **阻塞整个线程池** | `spawn_blocking` / 异步替代品 |
| 不设置 channel 边界 | 内存无限增长 | 有界 channel + 背压策略 |

### 死锁实战案例

```rust
// ❌ 致命反模式：看起来正确，但会在生产中死锁
use std::sync::Mutex;

pub struct OrderService {
    cache: Mutex<HashMap<OrderId, Order>>,
    repo: Arc<dyn OrderRepository>,
}

impl OrderService {
    pub async fn get_or_fetch(&self, id: OrderId) -> Result<Order, Error> {
        let mut cache = self.cache.lock().unwrap(); // 获取锁
        if let Some(order) = cache.get(&id) {
            return Ok(order.clone());
        }
        let order = self.repo.fetch(id).await?; // ← 跨 .await 持有锁！
        cache.insert(id, order.clone());
        Ok(order)
    }
}

// ✅ 正确：先释放锁，再 await
pub async fn get_or_fetch(&self, id: OrderId) -> Result<Order, Error> {
    if let Some(order) = self.cache.lock().unwrap().get(&id).cloned() {
        return Ok(order);
    }
    let order = self.repo.fetch(id).await?; // 无锁持有
    self.cache.lock().unwrap().insert(id, order.clone());
    Ok(order)
}
```

> 💡 **Clippy 保护**：在 `clippy.toml` 中启用 `await-holding-lock` lint：
> ```toml
> await-holding-lock-timeout = 0
> ```

---

## 领域特定开发指导

### A. CLI 工具开发

**代表项目**：ripgrep, fd, bat, eza, zoxide, just, starship, broot, zellij

**技术栈模板**：

```toml
[dependencies]
clap = { version = "4", features = ["derive"] }  # 参数解析
anyhow = "1"                                       # 错误处理（仅 binary）
tracing = "0.1"                                    # 结构化日志
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
tokio = { version = "1", features = ["full"] }     # 异步运行时
serde = { version = "1", features = ["derive"] }   # 序列化
```

**架构要点**：
- 使用 `clap` derive 模式定义命令行接口
- TUI 应用使用 `ratatui`（终端 UI 框架）
- 并行文件搜索参考 ripgrep 的 `ignore` crate + `grep-searcher`
- 使用 `human-panic` 设置友好的 panic 处理

### B. Web 服务开发

**框架选型**：

| 框架 | 性能 | 生态 | 学习曲线 | 适用场景 |
|------|------|------|---------|---------|
| **axum** | ★★★★★ | ★★★★☆ | 低 | ✅ 首选，现代、类型安全 |
| **actix-web** | ★★★★★ | ★★★★☆ | 中 | 高并发、已有大量用户 |
| **rocket** | ★★★★☆ | ★★★☆☆ | 低 | 快速原型、全功能 |
| **poem** | ★★★★☆ | ★★★☆☆ | 中 | OpenAPI 集成、可扩展 |
| **salvo** | ★★★★☆ | ★★★☆☆ | 低 | 类似 Axum 的现代设计 |

**axum 标准分层架构**：

```
src/
├── main.rs              # 启动 + 路由注册
├── config.rs            # 配置（database_url, port...）
├── error.rs             # AppError 类型
├── state.rs             # AppState (共享状态)
├── routes/
│   ├── mod.rs
│   ├── health.rs        # GET /health
│   └── users.rs         # CRUD /users
├── handlers/            # 请求处理器（薄层）
│   └── mod.rs
├── services/            # 业务逻辑
│   └── mod.rs
└── repository/          # 数据访问
    └── mod.rs
```

**中间件链最佳实践**：

```rust
let app = Router::new()
    .route("/api/users", post(create_user))
    .layer(TraceLayer::new_for_http())                    // 请求追踪
    .layer(CompressionLayer::new())                       // 压缩
    .layer(CorsLayer::permissive())                       // CORS
    .layer(Extension(reqwest::Client::new()))             # 注入 HTTP 客户端
    .with_state(state);                                   // 共享状态
```

### C. 桌面应用开发

| 方案 | 渲染方式 | 包大小 | 适用场景 |
|------|---------|-------|---------|
| **Tauri v2** | WebView (系统) | 2-10 MB | ✅ 业务应用、跨平台首选 |
| **Slint** | 原生渲染 | <1 MB | 嵌入式 GUI、资源受限 |
| **iced** | GPU 渲染 (wgpu) | 中等 | Elm 架构风格、自定义 UI |
| **egui** | 即时模式 GPU | 小 | 工具窗口、调试面板 |
| **Dioxus** | WebView/Desktop | 中等 | React 风格跨平台 |

**Tauri v2 关键决策点**：
- IPC 边界设计（见 tauri-skills）
- 权限最小原则（Capability → Permission → Scope）
- 前端框架自由选择（React/Vue/Svelte/Solid）

### D. 嵌入式开发

**核心技术栈**：

| 层级 | 技术 | 说明 |
|------|------|------|
| HAL (硬件抽象层) | `stm32f4xx-hal`, `esp-hal` | 寄存器安全封装 |
| RTOS | **embassy** (推荐), RTIC | 异步/中断驱动调度 |
| no_std alloc | `heapless`, `arrayvec` | 无堆分配容器 |
| 串口/调试 | `defmt`, `log+panic-probe` | 日志输出 |

**embassy vs RTIC 选择**：

| 维度 | embassy | RTIC |
|------|---------|------|
| 编程模型 | async/await | 资源属性宏 |
| Future 支持 | ✅ 原生 | ❌ 有限 |
| 学习曲线 | 中（需理解 async） | 低（声明式） |
| 社区趋势 | 📈 上升中 | 📉 维护模式 |
| 适用场景 | 复杂异步逻辑 | 简单实时任务 |

**no_std 黄金规则**：
1. 没有 `Box`/`Vec`/`String`（除非启用 `alloc`）
2. panic = 死机（必须定义 `#[panic_handler]`）
3. 没有标准库 → 使用 `core` + `alloc` crate
4. 所有错误必须可 Sized（不能用 `dyn Error`）

### E. 游戏开发

**引擎选型**：

| 引擎 | 架构 | 2D | 3D | 成熟度 |
|------|------|----|----|-------|
| **Bevy** | ECS (Data-oriented) | ✅ | ✅ | ★★★★☆ (快速迭代) |
| Fyrox | OOP/场景树 | ✅ | ✅ | ★★★☆☆ |
| macroquad | 即时模式 | ✅ | 基础 | ★★★☆☆ |
| ggez | 简易 2D | ✅ | ❌ | ★★★☆☆ |

**Bevy ECS 核心模式**：

```rust
// Component: 纯数据标记
#[derive(Component)]
struct Player;

#[derive(Component)]
struct Velocity(Vec3);

// System: 纯函数 + 查询
fn movement_system(
    mut query: Query<(&mut Transform, &Velocity), With<Player>>,
    time: Res<Time>,
) {
    for (mut transform, velocity) in &mut query {
        transform.translation += velocity.0 * time.delta_seconds();
    }
}

// Schedule: 系统执行顺序
app.add_systems(Update, (
    input_system,
    movement_system.after(input_system),
    collision_system.after(movement_system),
));
```

### F. 区块链开发

| 链/框架 | 语言 | 方向 |
|---------|------|------|
| **Solana** | Rust + Anchor | 高吞吐 DeFi/NFT |
| **Polkadot/Substrate** | Rust | 自定义链/平行链 |
| **sui** | Move + Rust SDK | 对象模型链 |
| **Starknet** | Cairo (Rust 编译目标) | ZK Rollup |
| **Near** | Rust (WASM) | sharded 链 |

**Substrate pallet 模式**：

```rust
#[pallet::config]
pub trait Config: frame_system::Config {
    type RuntimeEvent: From<Event<Self>> = Into<<Self as frame_system::Config>::RuntimeEvent>;
    type WeightInfo: WeightInfo;
}

#[pallet::pallet]
pub struct Pallet<T>(_);

#[pallet::call]
impl<T: Config> Pallet<T> {
    #[pallet::weight(<T as Config>::WeightInfo::do_something())]
    pub fn do_something(origin: OriginFor<T>) -> DispatchResult {
        let _who = ensure_signed(origin)?;
        Self::deposit_event(Event::SomethingStored(who));
        Ok(())
    }
}
```

---

## 性能优化优先级表

| 优化项 | 影响 | 成本 | 工具 |
|--------|------|------|------|
| **算法/数据结构选择** | ★★★★★ | 低 | 分析 > 盲目优化 |
| **减少分配** | ★★★★★ | 中 | `cargo bench` + criterion |
| **零拷贝解析** | ★★★★☆ | 中 | `bytes`, `zerocopy` |
| **并行化 (rayon)** | ★★★★☆ | 中 | `rayon::iter` |
| **SIMD 自动向量化** | ★★★☆☆ | 低 | 确保对齐 + 简单循环 |
| **Profile-guided optimization** | ★★★☆☆ | 高 | `-C profile-generate/use` |
| **内存布局优化** | ★★★☆☆ | 高 | `#[repr(C)]`, `packed`, `Vec` 预分配 |

### 性能分析工具链

```bash
# 1. 基准测试
cargo bench --bench my_benchmark

# 2. CPU 性能分析
cargo instrument --release -g -- bench my_benchmark

# 3. 内存分析 (heap)
cargo install heaptrack
heaptrack target/release/my_binary

# 4. PGO (Profile-Guided Optimization)
RUSTFLAGS="-C profile-generate=/tmp/pgo-data" cargo build --release
./target/release/my-binary  # 运行典型工作负载
RUSTFLAGS="-C profile-use=/tmp/pgo-data" cargo build --release
```

---

## 发布与分发

### Crates.io 发布清单

- [ ] `Cargo.toml` 元信息完整（description, license, keywords, categories）
- [ ] 文档示例通过 `cargo doc` 无警告
- [ ] `cargo test` + `cargo clippy -- -D warnings` 全部通过
- [ ] `cargo audit` 无已知安全漏洞
- [ ] 版本号遵循语义化规范
- [ ] `CHANGELOG.md` 记录变更

### 二进制分发

| 平台 | 打包工具 |
|------|---------|
| Windows MSI | `msi-packager` / WiX |
| macOS DMG | `create-dmg` / `apple-dmg` |
| Linux deb/rpm | `cargo-deb` / `cargo-rpm` |
| 通用 | `cargo-binstall` / Homebrew / Scoop |

### CI/CD 必要检查

```yaml
# GitHub Actions 示例
- run: cargo fmt --check
- run: cargo clippy -- -D warnings
- run: cargo test
- run: cargo test --all-features
- run: cargo audit
- run: cargo deny check
```

---

## 反模式速查表（完整版）

| 类别 | 反模式 | 正确做法 | 严重度 |
|------|--------|---------|--------|
| **内存** | 无界 channel / HashMap 无限增长 | 有界 + TTL / LRU 淘汰 | 🔴 致命 |
| **并发** | `std::sync::Mutex` 跨 `.await` | `tokio::sync::Mutex` | 🔴 致命 |
| **错误** | 库中用 `anyhow` | 自定义 `AppError` + `thiserror` | 🔴 致命 |
| **错误** | `.unwrap()` 在库代码中 | `?` 传播到顶层 | 🟠 严重 |
| **性能** | `Box<dyn Trait>` 在热路径 | 泛型单态化 | 🟠 严重 |
| **性能** | 循环内不必要的 `clone()` | 借用 / `Cow` / `Arc` | 🟡 中等 |
| **架构** | 过早拆分 crate | Module First, Crate Last | 🟡 中等 |
| **架构** | `main.rs` 4000 行 | 分层：routes/handlers/services | 🟠 严重 |
| **异步** | 阻塞 I/O 在 async 中 | `spawn_blocking` | 🟠 严重 |
| **安全** | `unsafe` 无注释 | `// SAFETY:` + 最小作用域 | 🔴 致命 |
| **依赖** | 不审计依赖漏洞 | `cargo audit` + `cargo deny` | 🟠 严重 |
| **测试** | 只写单元测试 | 单元 + 集成 + 属性测试 | 🟡 中等 |
| **日志** | 生产环境 `println!` / `dbg!` | `tracing` + 结构化日志 | 🟡 中等 |

---

## 子技能索引

以下子技能提供各主题的深度指导：

| 子技能 | 覆盖范围 | 触发关键词 |
|--------|---------|-----------|
| [rust-ownership-skill](rust-ownership-skill/SKILL.md) | 所有权、借用、生命周期 | "借用检查"、"move"、"lifetime" |
| [rust-concurrency-skill](rust-concurrency-skill/SKILL.md) | 多线程、Sync/Send、原子操作 | "线程安全"、"竞态条件"、"Mutex" |
| [rust-error-handling-skill](rust-error-handling-skill/SKILL.md) | 错误类型设计、thiserror/anyhow | "Result"、"错误传播"、"AppError" |
| [rust-async-skill](rust-async-skill/SKILL.md) | async/await、Pin/Future、流 | "async"、"tokio"、"Stream" |
| [rust-cli-project-skill](rust-cli-project-skill/SKILL.md) | CLI 参数解析、TUI、发布 | "命令行"、"clap"、"终端应用" |
| [rust-performance-skill](rust-performance-skill/SKILL.md) | 基准测试、 profiling、优化 | "性能"、"benchmark"、"criterion" |
| [rust-testing-doc-skill](rust-testing-doc-skill/SKILL.md) | 测试策略、mock、属性测试 | "测试"、"mockall"、"proptest" |
| [rust-smart-pointers-skill](rust-smart-pointers-skill/SKILL.md) | Rc/Arc/Weak/Cow/Cell | "智能指针"、"引用计数" |
| [rust-collections-skill](rust-collections-skill/SKILL.md) | Vec/HashMap/BTreeSet 选择 | "集合"、"数据结构选择" |
| [rust-generics-skill](rust-generics-skill/SKILL.md) | 泛型、trait bound、关联类型 | "泛型"、"trait"、"monomorphization" |
| [rust-type-driven-skill](rust-type-driven-skill/SKILL.md) | 类型状态编程、newtype 模式 | "类型安全"、"type-state"、"phantom" |
| [rust-domain-design-skill](rust-domain-design-skill/SKILL.md) | DDD 领域建模 | "领域驱动"、"实体"、"值对象" |
| [rust-domain-error-skill](rust-domain-error-skill/SKILL.md) | 领域错误建模 | "领域错误"、"业务规则验证" |
| [rust-resource-management-skill](rust-resource-management-skill/SKILL.md) | RAII、Drop、守卫模式 | "资源管理"、"RAII"、"cleanup" |
| [rust-zero-cost-skill](rust-zero-cost-skill/SKILL.md) | 零成本抽象原理 | "零成本"、"monomorphization"、"inline" |
| [rust-mental-model-skill](rust-mental-model-skill/SKILL.md) | Rust 心智模型 | "心智模型"、"栈vs堆"、"所有权直觉" |
| [rust-mutability-skill](rust-mutability-skill/SKILL.md) | 可变性模式、Interior Mutability | "可变性"、"Cell"、"RefCell" |
| [rust-lifecycle-skill](rust-lifecycle-skill/SKILL.md) | 生命周期高级用法 | "生命周期省略"、"HRTB"、"covariance" |
| [rust-iterators-skill](rust-iterators-skill/SKILL.md) | 迭代器适配器、消费器 | "iterator"、"map/filter/collect" |
| [rust-struct-enum-skill](rust-struct-enum-skill/SKILL.md) | 结构体/枚举设计模式 | "enum dispatch"、"newtype pattern" |
| [rust-core-skill](rust-core-skill/SKILL.md) | 核心trait (From/TryInto/Deref) | "From"、"TryFrom"、"Operator overload" |
| [rust-cargo-skill](rust-cargo-skill/SKILL.md) | Cargo 高级用法、workspace | "workspace"、"feature flag"、"profile" |
| [rust-ecosystem-skill](rust-ecosystem-skill/SKILL.md) | 生态系统导航、crate 选择 | "用什么crate"、"crates.io" |
| [rust-web-skill](rust-web-skill/SKILL.md) | Web 开发完整指南 | "HTTP API"、"REST"、"WebSocket" |
| [rust-cloud-native-skill](rust-cloud-native-skill/SKILL.md) | 云原生/K8s/微服务 | "云原生"、"kubernetes"、"gRPC" |
| [rust-fintech-skill](rust-fintech-skill/SKILL.md) | 金融科技/量化交易 | "金融"、"交易系统"、"高精度" |
| [rust-embedded-skill](rust-embedded-skill/SKILL.md) | 嵌入式/no_std 开发 | "MCU"、"STM32"、"embassy" |
| [rust-iot-skill](rust-iot-skill/SKILL.md) | IoT 设备开发 | "IoT"、"传感器"、"MQTT" |
| [rust-ml-skill](rust-ml-skill/SKILL.md) | 机器学习/AI | "ML"、"神经网络"、"推理" |
| [rust-anti-pattern-skill](rust-anti-pattern-skill/SKILL.md) | 反模式大全 | "反模式"、"常见错误"、"pitfall" |
## 参考文档

- [architecture.md](references/architecture.md) — Rust 项目架构模式详解
- [commands.md](references/commands.md) — Cargo/Rust 常用命令速查
- [meta-cognition.md](references/meta-cognition.md) — Rust 学习元认知框架

## 注意事项

### Edition / Toolchain 注意事项

- 以当前 stable 与项目 MSRV 为准，不要把临时特性写成默认前提
- 升级 edition 或 toolchain 前，先验证 `cargo check`、`cargo clippy` 和测试套件
- 若需要新语法或新 trait 行为，先确认 crate 的兼容边界，再决定是否采用

### MSRV (最低支持版本)

- 始终在 `Cargo.toml` 中声明 `rust-version`
- 使用 `cargo msrv` 验证
- 不要盲目升级 MSRV，考虑下游兼容性

### unsafe 使用准则

1. **最小作用域**：将 unsafe 封装为安全的公开 API
2. **必须注释**：每处 `unsafe` 块必须有 `// SAFETY:` 解释为何安全
3. **审查机制**：unsafe 代码应经过额外 code review
4. **Miri 检测**：对含 unsafe 的代码运行 `cargo miri test` 发现 UB

### 依赖安全

```bash
# 定期审计
cargo audit          # 安全漏洞检测
cargo deny check     # 许可证合规 + 禁止列表
cargo tree -d        # 查看依赖树深度
cargo outdated       # 检查过时依赖
```
