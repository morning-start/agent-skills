# rust-web-skill

## 前言区

```
name: rust-web-skill
version: v1.0.0
author: book-skills
description: Web开发领域Rust应用技能，涵盖Axum、Actix-web、Rocket等框架的API设计与性能优化
tags: [web, api, rest, graphql, axum, actix-web, rocket]
trigger: /rust-web
layer: Layer 3 - Domain Extensions
```

## 概述

本技能聚焦Web开发领域，展示Rust在高性能Web服务、API设计、微服务架构等场景下的优势。

## 任务目标

1. 构建高性能REST API
2. 实现GraphQL服务
3. 设计中间件与认证
4. 优化Web性能

## 操作步骤

### 1. REST API with Axum

```rust
use axum::{
    extract::{Path, Query, State},
    http::{HeaderMap, StatusCode},
    response::Json,
    routing::{delete, get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

#[derive(Clone)]
struct AppState {
    items: Arc<RwLock<HashMap<String, Item>>>,
}

#[derive(Debug, Serialize, Deserialize)]
struct Item {
    id: String,
    name: String,
    price: f64,
}

async fn create_item(
    State(state): State<AppState>,
    Json(payload): Json<Item>,
) -> StatusCode {
    let mut items = state.items.write().await;
    items.insert(payload.id.clone(), payload);
    StatusCode::CREATED
}

async fn get_item(
    State(state): State<AppState>,
    Path(id): Path<String>,
) -> Result<Json<Item>, StatusCode> {
    let items = state.items.read().await;
    items.get(&id)
        .map(|i| Json(i.clone()))
        .ok_or(StatusCode::NOT_FOUND)
}

async fn list_items(State(state): State<AppState>) -> Json<Vec<Item>> {
    let items = state.items.read().await;
    Json(items.values().cloned().collect())
}

#[tokio::main]
async fn main() {
    let state = AppState {
        items: Arc::new(RwLock::new(HashMap::new())),
    };

    let app = Router::new()
        .route("/items", post(create_item))
        .route("/items", get(list_items))
        .route("/items/:id", get(get_item))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080")
        .await
        .unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

### 2. GraphQL with async-graphql

```rust
use async_graphql::{Context, EmptySubscription, Object, Schema};

pub struct QueryRoot;

#[Object]
impl QueryRoot {
    async fn user(&self, ctx: &Context<'_>, id: ID) -> Option<User> {
        ctx.data::<DbPool>()?.get_user(id.parse()?).await.ok()
    }

    async fn users(&self, ctx: &Context<'_>) -> Vec<User> {
        ctx.data::<DbPool>()?.get_users().await.unwrap_or_default()
    }
}

pub struct MutationRoot;

#[Object]
impl MutationRoot {
    async fn create_user(&self, ctx: &Context<'_>, input: NewUser) -> User {
        ctx.data::<DbPool>()?.create_user(input).await
    }
}

type MySchema = Schema<QueryRoot, MutationRoot, EmptySubscription>;

async fn graphql_handler(schema: MySchema, req: Request) -> Response {
    graphql(schema, req).await
}
```

### 3. 中间件与认证

```rust
use axum::{
    extract::Request,
    http::{header::AUTHORIZATION, StatusCode},
    middleware::Next,
    response::Response,
};

pub async fn auth_middleware(
    mut req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let auth_header = req
        .headers()
        .get(AUTHORIZATION)
        .and_then(|h| h.to_str().ok());

    if let Some(token) = auth_header {
        if validate_token(token) {
            req.extensions_mut().insert(UserId(get_user_id(token)));
            return Ok(next.run(req).await);
        }
    }

    Err(StatusCode::UNAUTHORIZED)
}

fn validate_token(token: &str) -> bool {
    token.starts_with("Bearer ") && token.len() > 7
}
```

### 4. 数据库集成

```rust
use sqlx::{postgres::PgPoolOptions, PgPool, FromRow};

#[derive(Debug, FromRow)]
pub struct Product {
    pub id: i32,
    pub name: String,
    pub price: Decimal,
}

pub async fn get_products(pool: &PgPool) -> Result<Vec<Product>, sqlx::Error> {
    sqlx::query_as::<_, Product>("SELECT id, name, price FROM products")
        .fetch_all(pool)
        .await
}

pub async fn create_product(
    pool: &PgPool,
    name: &str,
    price: Decimal,
) -> Result<Product, sqlx::Error> {
    sqlx::query_as::<_, Product>(
        "INSERT INTO products (name, price) VALUES ($1, $2) RETURNING id, name, price"
    )
    .bind(name)
    .bind(price)
    .fetch_one(pool)
    .await
}
```

### 5. WebSocket

```rust
use axum::{
    extract::ws::{Message, WebSocket, WebSocketUpgrade},
    response::Response,
    routing::get,
    Router,
};
use std::sync::Arc;
use tokio::sync::broadcast;

pub async fn ws_handler(ws: WebSocketUpgrade) -> Response {
    ws.on_upgrade(|socket| handle_socket(socket))
}

async fn handle_socket(socket: WebSocket) {
    let (sender, mut receiver) = socket.split();
    let msg: broadcast::Receiver<String> = subscribe().await;

    tokio::spawn(async move {
        while let Ok(msg) = receiver.recv().await {
            if sender.send(Message::Text(msg)).await.is_err() {
                break;
            }
        }
    });
}
```

## 资源索引

### 核心框架

| 框架 | 特点 | 链接 |
|------|------|------|
| Axum | 轻量、类型安全 | https://github.com/tokio-rs/axum |
| Actix-web | 性能最高 | https://actix.rs/ |
| Rocket | 友好API | https://rocket.rs/ |
| Poem | 简洁优雅 | https://poem.rs/ |

### 关键依赖

```toml
[dependencies]
axum = "0.7"
tokio = { version = "1.35", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
sqlx = { version = "0.7", features = ["runtime-tokio", "postgres"] }
async-graphql = "7.0"
tower = "0.4"
tower-http = { version = "0.5", features = ["cors", "trace"] }
```

## 注意事项

1. **错误处理**：使用Result类型传播错误，避免panic
2. **连接池**：数据库连接池大小需合理配置
3. **中间件顺序**：注意中间件的注册顺序
4. **异步runtime**：选择一个runtime( tokio/compat)并一致使用
