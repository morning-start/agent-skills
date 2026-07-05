---
name: rust-struct-enum
version: 1.0.0
author: book-skills
description: Rust 结构体与枚举技能，掌握定义、方法、关联函数、模式匹配和模块化编程
tags: [rust, struct, enum, modeling, pattern-matching]
layer: Layer 1 - Language Mechanics
trigger: struct, enum, pattern matching, modeling
---

# Rust 结构体与枚举

## 任务目标

- 本 Skill 用于：使用结构体和枚举组织数据，实现面向对象和函数式模式
- 能力包含：结构体定义、方法、关联函数、枚举定义、模式匹配、impl 块、模块系统
- 触发条件：需要定义复杂数据类型、处理可选值、实现多态

## 前置准备

- 完成 rust-core 基础语法
- 完成 rust-ownership 所有权系统

## 结构体

### 定义与实例化

```rust
// 普通结构体
struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}

let user = User {
    email: String::from("user@example.com"),
    username: String::from("alice"),
    active: true,
    sign_in_count: 1,
};

// 元组结构体
struct Color(i32, i32, i32);
let black = Color(0, 0, 0);

// 类单元结构体（无字段）
struct AlwaysEqual;
```

### 可变字段与字段简写

```rust
fn build_user(email: String, username: String) -> User {
    User {
        email,          // 字段简写，等同于 email: email
        username,
        active: true,
        sign_in_count: 1,
    }
}
```

### 结构体更新语法

```rust
let user1 = User {
    email: String::from("user1@example.com"),
    username: String::from("user1"),
    active: true,
    sign_in_count: 1,
};

let user2 = User {
    email: String::from("user2@example.com"),
    ..user1  // 其余字段从 user1 复制
};
```

## 结构体方法

### impl 块定义

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    // 方法
    fn area(&self) -> u32 {
        self.width * self.height
    }

    // 可变方法
    fn set_width(&mut self, width: u32) {
        self.width = width;
    }

    // 静态方法（关联函数）
    fn new(width: u32, height: u32) -> Rectangle {
        Rectangle { width, height }
    }

    // 可以有多个 impl 块
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}

fn main() {
    let rect = Rectangle::new(30, 50);  // 调用静态方法
    println!("面积: {}", rect.area());   // 调用实例方法
}
```

### 方法接收者

| 接收者 | 说明 |
|--------|------|
| `&self` | 不可变借用 |
| `&mut self` | 可变借用 |
| `self` | 获取所有权 |
| `&mut Self` | 返回可变引用 |

## 枚举

### 基础枚举

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },  // 元组变体
    Write(String),            // 元组变体
    ChangeColor(i32, i32, i32), // 元组变体
}

let m = Message::Move { x: 10, y: 20 };
```

### 枚举方法

```rust
impl Message {
    fn call(&self) {
        match self {
            Message::Quit => println!("Quit"),
            Message::Move { x, y } => println!("Move to ({}, {})", x, y),
            Message::Write(s) => println!("Write: {}", s),
            Message::ChangeColor(r, g, b) => println!("Color: {}, {}, {}", r, g, b),
        }
    }
}

let m = Message::Write(String::from("hello"));
m.call();
```

### Option 枚举

```rust
// 标准库定义
enum Option<T> {
    Some(T),
    None,
}

fn find_user(name: &str) -> Option<&str> {
    if name == "Alice" {
        Some("found")
    } else {
        None
    }
}

// 使用 Option
if let Some(result) = find_user("Alice") {
    println!("{}", result);
}

let result = find_user("Bob").unwrap_or("not found");
```

## 模式匹配

### match 表达式

```rust
enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter,
}

fn value_in_cents(coin: Coin) -> u32 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
    }
}

// 带值的匹配
fn value_in_cents(coin: Coin) -> u32 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter(state) => {
            println!("State quarter from {:?}", state);
            25
        }
    }
}

#[derive(Debug)]
enum UsState {
    Alabama,
    Alaska,
}

enum Coin2 {
    Quarter(UsState),
    Dime,
}

fn value(coin: Coin2) -> u32 {
    match coin {
        Coin2::Quarter(state) => {
            println!("{:?}", state);
            25
        }
        Coin2::Dime => 10,
    }
}
```

### if let 简洁匹配

```rust
let some_u8_value = Some(3u8);

// 传统 match
match some_u8_value {
    Some(3) => println!("three"),
    _ => (),
}

// if let 简化
if let Some(3) = some_u8_value {
    println!("three");
}

// if let else
if let Some(x) = some_u8_value {
    println!("{}", x);
} else {
    println!("not three");
}

// let...else
let Some(x) = some_u8_value else {
    println!("not three");
    return;
};
println!("{}", x);
```

### while let 循环

```rust
let mut stack = Vec::new();
stack.push(1);
stack.push(2);
stack.push(3);

while let Some(top) = stack.pop() {
    println!("{}", top);
}
```

### for 循环解构

```rust
let v = vec![(1, 2), (3, 4), (5, 6)];
for (index, value) in v.iter().enumerate() {
    println!("{}: {:?}", index, value);
}
```

### let 赋值

```rust
let (x, y, z) = (1, 2, 3);
let (a, b) = (1, 2, 3);  // 错误：模式不匹配
```

## 模块系统

### 模块定义

```rust
// lib.rs 或 main.rs
mod network {
    pub fn connect() {
        println!("Connecting...");
    }

    pub mod client {
        pub fn request() {
            println!("Making request...");
        }
    }
}

fn main() {
    network::connect();
    network::client::request();
}
```

### 路径与 use

```rust
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}

use crate::front_of_house::hosting;

pub fn eat_at_restaurant() {
    hosting::add_to_waitlist();
}
```

### 访问级别

| 关键字 | 访问范围 |
|--------|----------|
| `pub` | 公开 |
| (无) | 私有（默认） |
| `pub(crate)` | crate 内公开 |
| `pub(super)` | 父模块可见 |
| `pub(in path)` | 指定路径可见 |

### 分离到文件

```rust
// src/network/mod.rs
pub mod client;
pub mod server;

// src/network/client.rs
pub fn connect() {}

// src/network/server.rs
pub fn listen() {}

// src/main.rs
mod network;
```

## 资源索引

- 结构体：https://doc.rust-lang.org/book/ch05-00-structs.html
- 枚举：https://doc.rust-lang.org/book/ch06-00-enums.html
- 模块：https://doc.rust-lang.org/book/ch07-00-modules.html

## 注意事项

- 结构体字段默认私有，枚举变体默认公开
- 方法第一个参数必须是 `self`、`&self` 或 `&mut self`
- 模式匹配必须穷尽所有情况
- 模块路径区分大小写
