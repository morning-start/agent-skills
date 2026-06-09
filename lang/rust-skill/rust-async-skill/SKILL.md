---
name: rust-async
version: 1.0.0
author: book-skills
description: Rust 异步编程技能，掌握 Future、async/await、Tokio 运行时、Stream 处理和取消
tags: [rust, async, tokio, future, stream]
layer: Layer 1 - Language Mechanics
trigger: async, async/await, tokio, future, stream, cancellation
---

# Rust 异步编程

## 任务目标

- 本 Skill 用于：编写高效的异步 Rust 程序
- 能力包含：async/await 语法、Future trait、Tokio 运行时、Stream、取消和超时
- 触发条件：需要高性能 I/O、并发请求处理、异步网络编程

## 前置准备

- 完成 rust-core-skill 和 rust-concurrency-skill
- 理解 Rust 所有权的特殊性

## async/await 基础

### 基本语法

```rust
async fn fetch_data() -> String {
    String::from("data")
}

#[tokio::main]
async fn main() {
    let result = fetch_data().await;
    println!("{}", result);
}
```

### 阻塞 vs 异步

```rust
// 阻塞操作（同步）
use std::fs;
let content = fs::read_to_string("file.txt").unwrap();

// 异步操作（非阻塞）
use tokio::fs;
let content = tokio::fs::read_to_string("file.txt").await.unwrap();
```

### async 函数返回 Future

```rust
async fn example() -> i32 {
    42
}

// 等价于
fn example() -> impl Future<Output = i32> {
    std::future::ready(42)
}
```

## Tokio 运行时

### Cargo.toml

```toml
[dependencies]
tokio = { version = "1", features = ["full"] }
```

### 运行时配置

```rust
use tokio::runtime::Builder;

fn main() {
    // 多线程运行时
    let runtime = Builder::new_multi_thread()
        .worker_threads(4)
        .enable_all()
        .build()
        .unwrap();

    runtime.block_on(async {
        println!("Running on multi-threaded runtime");
    });
}
```

### #[tokio::main]

```rust
// 单线程运行时
#[tokio::main(flavor = "current_thread")]
async fn main() {
    println!("Single threaded");
}

// 多线程运行时（默认）
#[tokio::main]
async fn main() {
    println!("Multi threaded");
}

// 简化写法
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        42
    });
    let result = handle.await.unwrap();
    println!("{}", result);
}
```

## spawn 任务

### 基本用法

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        // 异步工作
        42
    });

    let result = handle.await.unwrap();
    println!("Result: {}", result);
}
```

### 在任务间共享数据

```rust
use tokio::sync::Mutex;

#[tokio::main]
async fn main() {
    let counter = Mutex::new(0);

    let handle = tokio::spawn(async {
        let mut c = counter.lock().await;
        *c += 1;
    });

    handle.await.unwrap();
    println!("{}", *counter.lock().await);
}
```

### Join 多个任务

```rust
#[tokio::main]
async fn main() {
    let handle1 = tokio::spawn(async {
        tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
        1
    });

    let handle2 = tokio::spawn(async {
        tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;
        2
    });

    let (r1, r2) = (handle1.await.unwrap(), handle2.await.unwrap());
    println!("{} {}", r1, r2);
}
```

## tokio::join!

```rust
#[tokio::main]
async fn main() {
    let (r1, r2, r3) = tokio::join!(
        async { 1 },
        async { 2 },
        async { 3 }
    );
    println!("{} {} {}", r1, r2, r3);
}
```

## select!

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx1, mut rx1) = mpsc::channel::<i32>(1);
    let (tx2, mut rx2) = mpsc::channel::<i32>(1);

    tokio::spawn(async move {
        tx1.send(1).await.unwrap();
    });

    tokio::spawn(async move {
        tx2.send(2).await.unwrap();
    });

    tokio::spawn(async move {
        tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
        tx2.send(3).await.unwrap();
    });

    loop {
        tokio::select! {
            Some(v) = rx1.recv() => {
                println!("Received from rx1: {}", v);
                break;
            }
            Some(v) = rx2.recv() => {
                println!("Received from rx2: {}", v);
                break;
            }
            () = tokio::time::sleep(tokio::time::Duration::from_secs(1)) => {
                println!("Timeout");
                break;
            }
        }
    }
}
```

## Channel

### mpsc::channel

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(32);  // 缓冲区大小

    tokio::spawn(async move {
        tx.send(1).await.unwrap();
        tx.send(2).await.unwrap();
        // tx 被 drop
    });

    while let Some(msg) = rx.recv().await {
        println!("Got: {}", msg);
    }
}
```

### broadcast

```rust
use tokio::sync::broadcast;

#[tokio::main]
async fn main() {
    let (tx, _rx) = broadcast::channel(16);

    let mut rx1 = tx.subscribe();
    let mut rx2 = tx.subscribe();

    tokio::spawn(async move {
        let msg = rx1.recv().await.unwrap();
        println!("rx1: {}", msg);
    });

    tokio::spawn(async move {
        let msg = rx2.recv().await.unwrap();
        println!("rx2: {}", msg);
    });

    tx.send("hello").unwrap();
}
```

### oneshot

```rust
use tokio::sync::oneshot;

#[tokio::main]
async fn main() {
    let (tx, rx) = oneshot::channel();

    tokio::spawn(async move {
        tx.send("done").unwrap();
    });

    let result = rx.await.unwrap();
    println!("Got: {}", result);
}
```

## I/O 操作

### TCP

```rust
use tokio::net::TcpListener;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:8080").await?;

    loop {
        let (mut socket, _) = listener.accept().await?;

        tokio::spawn(async move {
            let mut buf = vec![0u8; 1024];
            loop {
                let n = match socket.read(&mut buf).await {
                    Ok(n) if n == 0 => return,
                    Ok(n) => n,
                    Err(e) => {
                        eprintln!("Error: {}", e);
                        return;
                    }
                };
                if socket.write_all(&buf[..n]).await.is_err() {
                    return;
                }
            }
        });
    }
}
```

### HTTP 客户端

```rust
// Cargo.toml
// [dependencies]
// reqwest = { version = "0.11", features = ["json"] }

use reqwest;

#[tokio::main]
async fn main() -> Result<(), reqwest::Error> {
    let body = reqwest::get("https://www.rust-lang.org")
        .await?
        .text()
        .await?;
    println!("Body: {} bytes", body.len());
    Ok(())
}
```

### HTTP 服务器

```rust
// Cargo.toml
// [dependencies]
// axum = "0.7"

use axum::{routing::get, Router};

async fn handler() -> &'static str {
    "Hello, World!"
}

#[tokio::main]
async fn main() {
    let app = Router::new().route("/", get(handler));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000")
        .await
        .unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

## Timer 和超时

### sleep

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    println!("Starting...");
    sleep(Duration::from_secs(2)).await;
    println!("After 2 seconds");
}
```

### timeout

```rust
use tokio::time::{timeout, Duration};

async fn slowOperation() {
    tokio::time::sleep(Duration::from_secs(10)).await;
}

#[tokio::main]
async fn main() {
    let result = timeout(Duration::from_secs(1), slowOperation()).await;

    match result {
        Ok(_) => println!("Completed"),
        Err(_) => println!("Timed out"),
    }
}
```

### interval

```rust
use tokio::time::{interval, Duration};

#[tokio::main]
async fn main() {
    let mut tick = interval(Duration::from_millis(500));

    for _ in 0..5 {
        tick.tick().await;
        println!("Tick");
    }
}
```

## Stream

### 基本用法

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(10);

    tokio::spawn(async move {
        for i in 0..5 {
            if tx.send(i).await.is_err() {
                break;
            }
        }
    });

    while let Some(v) = rx.recv().await {
        println!("Got: {}", v);
    }
}
```

### StreamExt

```rust
use tokio_stream::StreamExt;

#[tokio::main]
async fn main() {
    let stream = tokio_stream::iter(1..10);

    stream
        .filter(|x| future::ready(x % 2 == 0))
        .map(|x| x * x)
        .for_each(|x| async move {
            println!("{}", x);
        })
        .await;
}
```

## Cancellation 取消

### 取消检测点

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        loop {
            // .await 是取消检测点
            tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
            println!("Working...");
        }
    });

    tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
    drop(handle);
    println!("Cancelled");
}
```

### graceful shutdown

```rust
use tokio::signal;

#[tokio::main]
async fn main() {
    let (tx, rx) = tokio::sync::broadcast::channel(1);

    tokio::spawn(async move {
        loop {
            tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
            println!("Working...");
        }
    });

    signal::ctrl_c().await.unwrap();
    println!("Shutting down...");
}
```

## 常用异步库

| 库 | 用途 |
|----|------|
| tokio | 异步运行时 |
| async-trait | async fn in trait |
| futures | Future/Stream 工具 |
| reqwest | HTTP 客户端 |
| axum | HTTP 服务器 |
| sqlx | 异步数据库 |
| redis | 异步 Redis |
| telegram-bot | Telegram Bot |

## 资源索引

- 异步：https://doc.rust-lang.org/book/ch17-00-async.html
- tokio：https://tokio.rs/
- async trait：https://docs.rs/async-trait

## 注意事项

- async 函数是惰性的，需要 .await 触发执行
- .await 是取消检测点，任务可能被取消
- 使用 Arc<Mutex<T>> 或 Channel 在任务间共享状态
- 阻塞操作应该使用 tokio::task::spawn_blocking
- async/await 没有运行时开销，比线程更轻量
- Tokio 运行时需要配置合理的 worker 数量
