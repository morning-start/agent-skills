---
name: rust-anti-pattern
version: 1.0.0
author: book-skills
description: Rust Layer 2 技能 - 反模式识别，核心问题：这个模式是否隐藏了设计问题？掌握常见的 Rust 代码坏味道和问题模式
tags: [rust, anti-pattern, code-smell, pitfalls, best-practices]
layer: Layer 2 - Design Choices
trigger: anti-pattern, code smell, mistake, common errors, bad practice
---

# Rust Anti-Pattern - Layer 2

## 核心问题

这个模式是否隐藏了设计问题？

## 元认知追溯

```
问题 → Layer 2: 代码坏味道
        ↓
识别反模式 → Layer 3: 设计意图
        ↓
正确模式 → Layer 1: Rust 规则
```

## 常见反模式

### Clone 滥用

```rust
// 反模式：过度使用 clone
fn process(data: Vec<String>) -> usize {
    let clone = data.clone();
    do_work(&clone).len()
}

// 好模式：使用引用
fn process(data: &[String]) -> usize {
    do_work(data).len()
}
```

### .unwrap() 滥用

```rust
// 反模式：panic on None
fn get_config() -> Config {
    CONFIG.get().unwrap() // panic if None
}

// 好模式：传播错误
fn get_config() -> Result<&Config, Error> {
    CONFIG.get().ok_or(Error::NotInitialized)
}

// 好模式：提供默认值
fn get_config() -> &Config {
    CONFIG.get().unwrap_or(&DEFAULT_CONFIG)
}
```

### 错误隐藏

```rust
// 反模式：吞掉错误
if let Some(v) = result {
    println!("{}", v);
} // 错误被静默忽略

// 好模式：传播或记录
match result {
    Ok(v) => println!("{}", v),
    Err(e) => {
        tracing::error!("Failed: {}", e);
        return Err(e);
    }
}
```

### 多线程共享可变状态

```rust
// 反模式：Arc<Mutex> 滥用
let shared = Arc::new(Mutex::new(Vec::new()));

// 好模式：消息传递
let (tx, rx) = mpsc::channel();
```

## 设计反模式

### God Object

```rust
// 反模式：一个结构体做所有事
struct UserManager {
    db: Database,
    cache: Cache,
    email: EmailService,
    // ... 太多职责
}

// 好模式：职责分离
struct UserRepository {
    db: Database,
}
struct UserCache {
    cache: Cache,
}
```

### 鞭子效应

```rust
// 反模式：过度嵌套
if let Some(user) = get_user() {
    if let Some(order) = get_order(&user) {
        if let Some(items) = order.items() {
            // 太深，难以理解
        }
    }
}

// 好模式：早期返回
let Some(user) = get_user() else { return None; };
let Some(order) = get_order(&user) else { return None; };
let Some(items) = order.items() else { return None; };
```

### 链式 API 滥用

```rust
// 反模式：Builder 过度复杂
let user = User::build()
    .name("Alice")
    .email("alice@example.com")
    .age(30)
    .address(Address::build()
        .street("Main")
        .city("NYC")
        .build())
    .build()?;

// 好模式：简洁的必填参数
struct User {
    name: String,
    email: String,
}

impl User {
    fn new(name: String, email: String) -> Self {
        User { name, email }
    }
}
```

## 代码组织反模式

### 模块耦合

```rust
// 反模式：循环依赖
mod a {
    pub fn f() -> i32 { b::g() }
}
mod b {
    pub fn g() -> i32 { a::f() }
}

// 好模式：使用 trait 解耦
trait Greet {
    fn g(&self) -> i32;
}
```

### Trait 滥用

```rust
// 反模式：徒有其名的 trait
trait Serializable {
    fn serialize(&self) -> String;
}

impl Serializable for MyType {
    fn serialize(&self) -> String {
        serde_json::to_string(self).unwrap()
    }
}

// 好模式：直接使用 serde
use serde::Serialize;
```

## 检测工具

```bash
# clippy - Rust linter
cargo clippy

# 包括所有反模式检测
cargo clippy --all-targets -- -D warnings
```

## 资源索引

- [Clippy 规则](https://rust-lang.github.io/rust-clippy/)
- [Effective Rust](https://www.lurenzotorres.com.br/effective_rust/)

## 注意事项

- 遵循 "三次法则"：如果复制三次，考虑重构
- 使用 clippy 作为辅助工具
- 优先代码清晰度，其次性能优化
