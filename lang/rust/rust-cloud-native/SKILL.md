---
name: rust-cloud-native
version: 1.0.0
author: book-skills
description: 云原生领域Rust应用技能，涵盖Kubernetes、容器化、微服务、Wasm及服务网格
tags: [cloud-native, kubernetes, wasm, microservices, service-mesh, containers]
trigger: /rust-cloud-native
layer: Layer 3 - Domain Extensions
---

# Rust 云原生开发

## 概述

本技能聚焦云原生领域，展示Rust在容器化、微服务、Wasm等场景下的高性能与安全优势。

## 任务目标

1. 构建轻量级微服务
2. 开发Wasm组件
3. 实现云原生存储方案
4. 构建服务网格Sidecar

## 操作步骤

### 1. 微服务 with Axum

```rust
use axum::{
    extract::Path,
    http::StatusCode,
    response::Json,
    routing::get,
    Router,
};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct User {
    id: u64,
    name: String,
    email: String,
}

async fn get_user(Path(user_id): Path<u64>) -> Result<Json<User>, StatusCode> {
    let user = User {
        id: user_id,
        name: "Alice".to_string(),
        email: "alice@example.com".to_string(),
    };
    Ok(Json(user))
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/users/:id", get(get_user));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000")
        .await
        .unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

### 2. Wasm组件

使用wasm-bindgen构建Wasm组件：

```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn process_data(data: &[f64]) -> Vec<f64> {
    data.iter()
        .map(|x| x * 2.0 + 1.0)
        .collect()
}

#[wasm_bindgen]
pub struct Calculator {
    value: f64,
}

#[wasm_bindgen]
impl Calculator {
    #[wasm_bindgen(constructor)]
    pub fn new(initial: f64) -> Self {
        Calculator { value: initial }
    }

    #[wasm_bindgen]
    pub fn add(&mut self, v: f64) -> f64 {
        self.value += v;
        self.value
    }
}
```

### 3. 容器镜像优化

创建多阶段Dockerfile：

```dockerfile
# Stage 1: Build
FROM rust:1.75 as builder
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo build --release
RUN strip target/release/my-service

# Stage 2: Runtime
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/release/my-service /usr/local/bin/
EXPOSE 8080
CMD ["my-service"]
```

### 4. Kubernetes部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rust-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rust-service
  template:
    metadata:
      labels:
        app: rust-service
    spec:
      containers:
      - name: service
        image: myregistry/rust-service:v1.0
        ports:
        - containerPort: 8080
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
```

### 5. 服务网格Sidecar

```rust
use std::net::SocketAddr;

pub struct SidecarConfig {
    pub upstream: SocketAddr,
    pub port: u16,
}

impl SidecarConfig {
    pub fn new(upstream: SocketAddr, port: u16) -> Self {
        SidecarConfig { upstream, port }
    }

    pub async fn start(self) -> Result<(), Box<dyn std::error::Error>> {
        let listener = tokio::net::TcpListener::bind(format!("0.0.0.0:{}", self.port)).await?;
        loop {
            let (client, _) = listener.accept().await?;
            let upstream = self.upstream;
            tokio::spawn(async move {
                let upstream_conn = tokio::net::TcpStream::connect(upstream).await.ok();
                if let Some(mut u] = upstream_conn {
                    let (_, mut c) = tokio::io::copy_bidirectional(&mut client, &mut u).await.ok();
                }
            });
        }
    }
}
```

## 资源索引

### 核心框架

| 框架 | 用途 | 链接 |
|------|------|------|
| Axum | Web框架 | https://github.com/tokio-rs/axum |
| Actix-web | Web框架 | https://actix.rs/ |
| Poem | Web框架 | https://poem.rs/ |
| wasm-bindgen | Wasm绑定 | https://rustwasm.github.io/wasm-bindgen/ |

### 关键依赖

```toml
[dependencies]
axum = "0.7"
tokio = { version = "1.35", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
wasm-bindgen = "0.2"
```

## 注意事项

1. **镜像大小**：使用rust-slim或distroless镜像减小体积
2. **健康检查**：实现/probe端点供K8s探测
3. **资源限制**：生产环境必须设置CPU/内存限制
4. **Wasm兼容性**：使用wasm-bindgen时注意JS互操作类型限制
