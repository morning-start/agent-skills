---
name: rust-error-handling
version: 1.0.0
author: book-skills
description: Rust 错误处理技能，掌握 Result 和 Option 类型、错误传播、自定义错误类型、panic 机制
tags: [rust, error-handling, result, option, panic]
layer: Layer 1 - Language Mechanics
trigger: result, option, panic, thiserror, anyhow
---

# Rust 错误处理

## 任务目标

- 本 Skill 用于：处理程序运行中的错误和异常情况
- 能力包含：Result 类型、Option 类型、错误传播、自定义错误、panic 处理、panic 恢复
- 触发条件：处理可恢复错误、处理可选值、遇到 panic 错误

## 前置准备

- 完成 rust-core 和 rust-generics
- 理解 Rust 没有异常的机制

## Option 枚举

```rust
// 标准库定义
enum Option<T> {
    Some(T),
    None,
}

fn find_user(name: &str) -> Option<&str> {
    if name == "Alice" {
        Some("user@example.com")
    } else {
        None
    }
}

// 使用 match
let result = find_user("Alice");
match result {
    Some(email) => println!("Email: {}", email),
    None => println!("User not found"),
}

// if let 简化
if let Some(email) = find_user("Alice") {
    println!("Email: {}", email);
}

// unwrap_or 提供默认值
let email = find_user("Bob").unwrap_or("no email");

// unwrap_or_else 延迟计算默认值
let email = find_user("Bob").unwrap_or_else(|| {
    println!("User not found, using default");
    "default@example.com"
});

// map 转换内部值
let email = find_user("Alice").map(|e| e.to_uppercase());

// and_then 链式调用
fn get_domain(email: &str) -> Option<&str> {
    email.split('@').nth(1)
}

let domain = find_user("Alice")
    .and_then(get_domain);

// is_some/is_none 检查
if find_user("Alice").is_some() {
    println!("User exists");
}

// expect 提供错误信息（调试用）
let email = find_user("Alice").expect("User should exist");
```

## Result 枚举

```rust
// 标准库定义
enum Result<T, E> {
    Ok(T),
    Err(E),
}

use std::num::ParseIntError;

fn parse_number(s: &str) -> Result<i32, ParseIntError> {
    s.parse::<i32>()
}

// 使用 match
match parse_number("42") {
    Ok(n) => println!("Number: {}", n),
    Err(e) => println!("Error: {}", e),
}

// unwrap 传播错误（不推荐）
let n = parse_number("42").unwrap();

// expect 提供错误信息
let n = parse_number("42").expect("Failed to parse number");

// unwrap_or 提供默认值
let n = parse_number("not a number").unwrap_or(0);

// unwrap_or_else 延迟计算
let n = parse_number("not a number").unwrap_or_else(|_| 0);

// is_ok/is_err 检查
if parse_number("42").is_ok() {
    println!("Valid number");
}
```

## 错误传播

### ? 运算符

```rust
use std::fs::File;
use std::io;
use std::io::Read;

fn read_username() -> Result<String, io::Error> {
    let mut file = File::open("username.txt")?;
    let mut content = String::new();
    file.read_to_string(&mut content)?;
    Ok(content)
}

// 等价的 match 版本
fn read_username_match() -> Result<String, io::Error> {
    let mut file = match File::open("username.txt") {
        Ok(f) => f,
        Err(e) => return Err(e),
    };
    let mut content = String::new();
    match file.read_to_string(&mut content) {
        Ok(_) => Ok(content),
        Err(e) => Err(e),
    }
}

// 链式调用
fn read_username_chained() -> Result<String, io::Error> {
    let mut content = String::new();
    File::open("username.txt")?.read_to_string(&mut content)?;
    Ok(content)
}
```

### ? 与 Option

```rust
fn last_char(s: &str) -> Option<char> {
    s.lines().last()?.chars().last()
}

// 等价于
fn last_char_match(s: &str) -> Option<char> {
    if let Some(line) = s.lines().last() {
        if let Some(c) = line.chars().last() {
            return Some(c);
        }
    }
    None
}
```

### ? 与 From

```rust
use std::fs::File;
use std::io;
use std::num::ParseIntError;

fn read_config() -> Result<i32, Box<dyn std::error::Error>> {
    let content = File::open("config.txt")?.read_to_string()?;
    let n = content.trim().parse::<i32>()?;
    Ok(n)
}
```

## 自定义错误类型

### 简单错误枚举

```rust
use std::fmt;

#[derive(Debug)]
enum AppError {
    NotFound(String),
    InvalidInput(String),
    ParseError(std::num::ParseIntError),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppError::NotFound(s) => write!(f, "Not found: {}", s),
            AppError::InvalidInput(s) => write!(f, "Invalid input: {}", s),
            AppError::ParseError(e) => write!(f, "Parse error: {}", e),
        }
    }
}

impl std::error::Error for AppError {}

fn find_user(name: &str) -> Result<String, AppError> {
    if name.is_empty() {
        return Err(AppError::InvalidInput("Name cannot be empty".to_string()));
    }
    if name == "Unknown" {
        return Err(AppError::NotFound(format!("User '{}' not found", name)));
    }
    Ok(format!("{}@example.com", name))
}
```

### 使用 thiserror

```rust
// Cargo.toml
// [dependencies]
// thiserror = "1.0"

use thiserror::Error;

#[derive(Error, Debug)]
pub enum ConfigError {
    #[error("File not found: {0}")]
    NotFound(String),

    #[error("Invalid format in {filename}: {message}")]
    InvalidFormat { filename: String, message: String },

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Parse error: {0}")]
    Parse(#[from] std::num::ParseIntError),
}
```

### 使用 anyhow

```rust
// Cargo.toml
// [dependencies]
// anyhow = "1.0"

use anyhow::{Context, Result};

fn read_config(path: &str) -> Result<i32> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read {}", path))?;
    let n = content.trim().parse::<i32>()
        .context("Failed to parse number")?;
    Ok(n)
}
```

## Panic 处理

### panic! 宏

```rust
fn main() {
    panic!("这是一个 panic");

    // 带回溯
    panic!("错误发生在: {:?}", std::env::current_dir());
}
```

### 数组越界

```rust
let v = vec![1, 2, 3];
// v[99];  // panic: index out of bounds

// 安全访问
if let Some(item) = v.get(99) {
    println!("{}", item);
}
```

### unwrap 和 expect

```rust
// 不安全的 unwrap
let n = parse_number("not a number").unwrap();  // panic

// 推荐：使用 expect 提供上下文
let n = parse_number("not a number").expect("应该是一个数字");
```

### 禁用 panic 处理

```rust
// Cargo.toml
[profile.release]
panic = 'abort'  // 减小二进制大小
```

## 错误处理策略

### 原则

| 场景 | 推荐方式 |
|------|----------|
| 可恢复错误 | Result |
| 可选值 | Option |
| 真正的异常情况 | panic |
| 库代码 | 自定义错误 |
| 应用代码 | anyhow |

### 组合使用

```rust
use std::num::ParseIntError;

fn parse_and_double(s: &str) -> Result<i32, ParseIntError> {
    Ok(s.parse::<i32>()? * 2)
}

fn parse_and_double_safe(s: &str) -> Option<i32> {
    Some(s.parse::<i32>().ok()? * 2)
}

fn main() {
    // 组合使用
    let result: Option<i32> = find_user("Alice")
        .and_then(|email| email.split('@').nth(1))
        .and_then(|domain| domain.parse::<i32>().ok());

    // or_else 处理复杂逻辑
    let n = parse_number("invalid")
        .unwrap_or_else(|_| {
            eprintln!("Using default value");
            0
        });
}
```

### 与迭代器组合

```rust
let numbers = vec!["1", "2", "three", "4", "5"];

let parsed: Vec<i32> = numbers
    .iter()
    .filter_map(|s| s.parse::<i32>().ok())
    .collect();

println!("{:?}", parsed);  // [1, 2, 4, 5]
```

## 资源索引

- 错误处理：https://doc.rust-lang.org/book/ch09-00-error-handling.html
- Result：https://doc.rust-lang.org/std/io/type.Result.html
- thiserror：https://github.com/dtolnay/thiserror
- anyhow：https://github.com/dtolnay/anyhow

## 注意事项

- Rust 没有异常，使用 Result 处理可恢复错误
- panic 用于真正的不可恢复错误
- ? 运算符只能用于 Result 和 Option
- 库应该返回具体错误类型，应用代码可用 anyhow
- 避免在库中使用 `unwrap()` 和 `expect()`
