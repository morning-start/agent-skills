---
name: rust-core
version: 1.0.0
author: book-skills
description: Rust 核心语法技能，涵盖变量、数据类型、函数定义、控制流和注释，是 Rust 编程的基础
tags: [rust, core, trait, conversion, deref]
layer: Layer 1 - Language Mechanics
trigger: core traits, from, into, tryfrom, deref, asref
---

# Rust 核心语法

## 任务目标

- 本 Skill 用于：掌握 Rust 基础语法和核心概念
- 能力包含：变量声明、可变性、数据类型、函数定义、控制流、模式匹配、注释
- 触发条件：需要编写 Rust 程序、解决语法错误、理解 Rust 基础语法

## 前置准备

- 安装 Rust 工具链：`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
- 验证安装：`rustc --version` 和 `cargo --version`

## 核心概念

### 变量与可变性

```rust
fn main() {
    // 不可变变量
    let x = 5;
    // 可变变量
    let mut y = 10;
    y = y + 1;

    // 类型注解
    let z: i32 = 20;

    // 常量（必须标注类型）
    const MAX_SCORE: i32 = 100;

    // 解构
    let (a, b) = (1, 2);
}
```

### 基本数据类型

#### 标量类型

| 类型 | 说明 | 示例 |
|------|------|------|
| 整数 | i8, i16, i32, i64, i128, isize | `let n: i32 = 42;` |
| 无符号整数 | u8, u16, u32, u64, u128, usize | `let n: u32 = 100;` |
| 浮点数 | f32, f64 | `let f: f64 = 3.14;` |
| 布尔 | bool | `let b: bool = true;` |
| 字符 | char (Unicode) | `let c: char = 'A';` |

#### 复合类型

```rust
// 元组（固定长度，类型可不同）
let tup: (i32, f64, u8) = (500, 6.4, 1);
let (x, y, z) = tup;
let first = tup.0;

// 数组（固定长度，类型相同）
let arr: [i32; 5] = [1, 2, 3, 4, 5];
let first = arr[0];
```

### 函数定义

```rust
// 基本函数
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

// 多返回值
fn swap(a: i32, b: i32) -> (i32, i32) {
    (b, a)
}

// 早期返回
fn absolute(x: i32) -> i32 {
    if x < 0 {
        return -x;
    }
    x
}

// 发散函数（永不返回）
fn dead_loop() -> ! {
    loop {
        // 处理中
    }
}
```

### 控制流

#### if 表达式

```rust
fn classify(n: i32) -> &'static str {
    if n < 0 {
        "negative"
    } else if n == 0 {
        "zero"
    } else {
        "positive"
    }
}

// if 是表达式，可返回值
let value = if x > 10 { 1 } else { 0 };
```

#### 循环

```rust
// loop 循环（可返回值）
let result = loop {
    counter += 1;
    if counter == 10 {
        break counter * 2;
    }
};

// while 循环
while n > 0 {
    n -= 1;
}

// for 循环（遍历迭代器）
for i in 0..5 {
    println!("{}", i);
}

// for 遍历集合（获取所有权）
for item in vec![1, 2, 3] {
    println!("{}", item);
}

// for 遍历引用
for item in &collection {
    println!("{}", item);
}
```

#### match 匹配

```rust
fn classify(n: i32) -> &'static str {
    match n {
        0 => "zero",
        1 | 2 => "one or two",
        3..=10 => "between three and ten",
        _ if n < 0 => "negative",
        _ => "large positive",
    }
}

// match 解构
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
}

fn handle(msg: &Message) {
    match msg {
        Message::Quit => println!("Quit"),
        Message::Move { x, y } => println!("Move to ({}, {})", x, y),
        Message::Write(s) => println!("Write: {}", s),
    }
}
```

### 注释

```rust
// 单行注释

/// 文档注释（支持 Markdown）
/// # Examples
/// ```
/// let x = 5;
/// ```

//! 内部文档注释（注释包含它的项）
//! # Notes
//! This module contains utilities.
```

## 运算符

| 类别 | 运算符 |
|------|--------|
| 算术 | `+`, `-`, `*`, `/`, `%` |
| 位运算 | `&`, `\|`, `^`, `!`, `<<`, `>>` |
| 比较 | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| 逻辑 | `&&`, `\|\|`, `!` |
| 类型转换 | `as` |

```rust
let n = 10 as f64;  // 类型转换
let a = 5;
let b = 2;
let c = a / b;  // 整数除法
let d = a as f64 / b as f64;  // 浮点除法
```

## 类型推断

Rust 编译器自动推断变量类型：

```rust
let x = 5;        // 推断为 i32
let y = 3.14;     // 推断为 f64
let name = "Alice"; // 推断为 &str
```

## 作用域与遮蔽

```rust
fn main() {
    let x = 5;
    {
        let x = x + 1;  // 遮蔽外部 x
        println!("{}", x);  // 6
    }
    println!("{}", x);  // 5
}
```

## 资源索引

- 官方文档：https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html
- 标准库：https://doc.rust-lang.org/std/index.html

## 注意事项

- Rust 默认变量不可变，使用 `mut` 使变量可变
- 整数除法向下取整
- 数组索引越界在运行时 panic（调试模式会触发 panic）
- match 必须穷尽所有可能性，使用 `_` 处理剩余情况
