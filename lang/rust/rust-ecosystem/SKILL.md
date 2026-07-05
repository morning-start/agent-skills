---
name: rust-ecosystem
version: 1.0.0
author: book-skills
description: Rust Layer 2 技能 - 生态选择，核心问题：哪个 crate 适合这个任务？掌握常用生态库的选择和使用
tags: [rust, ecosystem, crates, dependencies, versioning]
layer: Layer 2 - Design Choices
trigger: crate, library, ecosystem, dependency, selection, web, async, serialization
---

# Rust Ecosystem - Layer 2

## 核心问题

哪个 crate 适合这个任务？

## 元认知追溯

```
问题 → Layer 2: 生态知识
        ↓
评估 crate 质量 → Layer 3: 项目需求
        ↓
安全与维护 → Layer 1: Rust 规则
```

## Web 开发

### Web 框架

| Crate | 场景 | 特点 |
|-------|------|------|
| actix-web | 高性能 REST | actor 模型，快速 |
| axum | 现代异步 | Tokio 生态，类型安全 |
| rocket | 开发者体验 | 简单直观，类型路由 |
| poem | OpenAPI 集成 | 自动生成 OpenAPI |

### HTTP 客户端

```rust
// reqwest - 同步/异步 HTTP
use reqwest;

let resp = reqwest::get("https://api.example.com/data")
    .await?
    .json::<Data>()
    .await?;
```

## 异步生态

### 运行时

| Crate | 场景 | 特点 |
|-------|------|------|
| tokio | 生产环境 | 成熟，功能全面 |
| async-std | 简单场景 | 接近 std API |

### 异步生态库

```rust
// 数据库
use sqlx::PgPool;           // PostgreSQL
use redis::AsyncCommands;    // Redis

// HTTP
use reqwest::Client;         // HTTP 客户端

// WebSocket
use tokio_tungstenite;       // WebSocket
```

## 序列化

### JSON

```rust
// serde - 序列化框架
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct User {
    id: u64,
    name: String,
    email: String,
}

// serde_json - JSON 实现
use serde_json;

let json = serde_json::to_string(&user)?;
let user: User = serde_json::from_str(&json)?;
```

### 其他格式

```rust
// TOML
use toml;

// YAML
use serde_yaml;

// MessagePack
use rmp_serde;
```

## 数据库

### ORM

```rust
// Diesel - 静态查询
// SQLx - 异步、动态查询
use sqlx::PgPool;

let pool = PgPool::connect(&std::env::var("DATABASE_URL")?).await?;

let users: Vec<User> = sqlx::query_as!(
    User,
    "SELECT id, name, email FROM users WHERE active = true"
)
.fetch_all(&pool)
.await?;
```

### NoSQL

```rust
// Redis
use redis::aio::MultiplexedConnection;

let client = redis::Client::open("redis://127.0.0.1")?;
let mut con = client.get_multiplexed_async_connection().await?;
```

## 日志与追踪

```rust
// 日志
use tracing;
use tracing_subscriber;

tracing_subscriber::fmt::init();

tracing::info!("Starting application");
tracing::error!("Failed to connect: {}", err);

// 结构化日志
tracing::info!(
    user_id = %user.id,
    action = "login",
    "User logged in"
);
```

## 配置管理

```rust
// config
use config::{Config, File};

let settings = Config::builder()
    .add_source(File::with_name("settings"))
    .add_source(Environment::with_prefix("APP"))
    .build()?;
```

## 命令行

```rust
// clap - 参数解析
use clap::{Parser, Subcommand};

#[derive(Parser)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Start,
    Stop,
    Restart,
}
```

## 资源索引

- [crates.io](https://crates.io/) - Crate 注册表
- [lib.rs](https://lib.rs/) - 分类生态库
- [Are we web yet?](https://www.arewewebyet.org/)
- [Are we async yet?](https://areweasyncyet.rs/)

## 选择指南

| 需求 | 推荐 |
|------|------|
| REST API | axum / actix-web |
| 异步运行时 | tokio |
| 序列化 | serde |
| 数据库 | sqlx |
| CLI | clap |
| 日志 | tracing |

## 注意事项

- 优先选择活跃维护的 crate
- 检查依赖传递，避免依赖过多
- 考虑安全性：审计依赖漏洞
