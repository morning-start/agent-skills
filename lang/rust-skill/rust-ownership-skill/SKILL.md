---
name: rust-ownership
description: Rust 所有权系统核心技能，掌握所有权、借用规则和生命周期，确保内存安全
version: 1.0.0
---

# Rust 所有权系统

## 任务目标

- 本 Skill 用于：理解 Rust 所有权规则、借用检查和生命周期
- 能力包含：所有权转移、借用规则、可变借用、生命周期注解、引用规则
- 触发条件：遇到 "borrowed value does not live long enough" 或所有权相关错误

## 前置准备

- 完成 rust-core-skill 基础语法学习
- 理解 Rust 所有权与 C/C++ 内存管理的区别

## 核心概念

### 所有权规则

```rust
fn main() {
    // 规则 1：每个值有一个所有者
    let s1 = String::from("hello");

    // 规则 2：值只能有一个所有者
    let s2 = s1;  // s1 被移动到 s2，s1 不再有效

    // 规则 3：当所有者离开作用域，值被丢弃
    println!("{}", s2);  // 正确：s2 是所有者
    // println!("{}", s1);  // 错误：s1 已无效
}
```

### 移动语义

```rust
// 堆分配类型（String, Vec, Box 等）会移动
let s1 = String::from("hello");
let s2 = s1;  // 移动
// s1 不再可用

// 栈分配类型（整数、浮点、bool 等）Copy
let x = 5;
let y = x;  // 复制
println!("{} {}", x, y);  // 两者都有效

// 自定义类型
struct Person {
    name: String,
    age: u32,
}

let p1 = Person {
    name: String::from("Alice"),
    age: 30,
};
let p2 = p1;  // 移动
// p1 不再可用
```

### 克隆

```rust
let s1 = String::from("hello");
let s2 = s1.clone();  // 深拷贝（显式）
println!("{} {}", s1, s2);  // 两者都有效
```

### 借用规则

```rust
fn main() {
    let s = String::from("hello");

    // 不可变借用（可同时有多个）
    let r1 = &s;
    let r2 = &s;
    println!("{} {}", r1, r2);  // OK

    // 可变借用（只能有一个，且期间原变量不可用）
    let r3 = &mut s;
    r3.push_str(" world");
    // println!("{}", r1);  // 错误：不可变引用在使用中
    println!("{}", r3);  // OK
}
```

### 借用规则总结

| 规则 | 说明 |
|------|------|
| 任意数量的不可变引用 | `&T` |
| 只能一个可变引用 | `&mut T` |
| 不可变引用和可变引用不能同时存在 | 二选一 |
| 引用必须总是有效的 | 不能悬垂引用 |

### 函数中的借用

```rust
fn calculate(s: &String) -> usize {
    s.len()
}  // s 离开作用域，但不丢弃所有权

fn modify(s: &mut String) {
    s.push_str(" world");
}

fn main() {
    let s = String::from("hello");
    let len = calculate(&s);
    println!("'{}' 的长度是 {}", s, len);  // s 仍然有效

    modify(&mut s);
    println!("{}", s);
}
```

### 返回值与所有权

```rust
fn take(s: String) {
    // s 进入作用域
}  // s 离开作用域，被丢弃

fn main() {
    let s1 = String::from("hello");
    take(s1);  // s1 移动到函数中
    // println!("{}", s1);  // 错误：s1 已无效
}
```

### 引用作为参数

```rust
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();
    for (i, &byte) in bytes.iter().enumerate() {
        if byte == b' ' {
            return &s[0..i];
        }
    }
    s
}

fn main() {
    let s = String::from("hello world");
    let word = first_word(&s);
    println!("第一个词: {}", word);
}
```

## 生命周期

### 生命周期注解

```rust
// 单生命周期
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// 结构体中的生命周期
struct Important<'a> {
    part: &'a str,
}

fn main() {
    let novel = String::from("Call me Ishmael...");
    let first = novel.split('.').next().unwrap();
    let i = Important { part: first };
}
```

### 生命周期省略规则

以下情况编译器自动推断生命周期：

1. 每个引用的参数获得自己的生命周期
2. 如果只有一个输入生命周期，它被赋给所有输出生命周期
3. 如果有 `&self` 或 `&mut self`，所有输出生命周期是 `self` 的生命周期

```rust
// 编译器自动推断生命周期
fn first_word(s: &str) -> &str { ... }
fn get_char(s: &str) -> char { s.chars().next().unwrap() }
```

### 静态生命周期

```rust
let s: &'static str = "我有很长的生命周期";
```

## 常见错误与解决

### 错误1：使用已移动的值

```rust
let s = String::from("hello");
let s2 = s;
// println!("{}", s);  // 错误

// 解决：使用克隆
let s2 = s.clone();
```

### 错误2：可变引用与不可变引用冲突

```rust
let mut s = String::from("hello");
let r1 = &s;
let r2 = &s;
let r3 = &mut s;  // 错误

// 解决：确保可变引用在不可变引用之后
let r1 = &s;
let r2 = &s;
println!("{} {}", r1, r2);
let r3 = &mut s;
r3.push_str(" world");
```

### 错误3：悬垂引用

```rust
fn dangle() -> &String {  // 错误
    let s = String::from("hello");
    &s  // s 在函数结束时被丢弃
}

// 解决：返回所有权
fn dangle() -> String {
    let s = String::from("hello");
    s
}
```

## 资源索引

- 官方文档：https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html
- 生命周期：https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html

## 注意事项

- 基本类型（i32, f64, bool, char）实现 Copy trait，直接复制
- 复杂类型默认移动语义，需要 Clone 才能复制
- 借用检查器在编译时防止所有内存错误
- 生命周期注解不改变引用的生命周期，只是描述关系
