---
name: rust-generics
description: Rust 泛型与 Trait 技能，掌握泛型数据类型、Trait 定义与实现、Trait  bounds、默认实现
version: 1.0.0
---

# Rust 泛型与 Trait

## 任务目标

- 本 Skill 用于：使用泛型和 Trait 实现代码复用、抽象和多态
- 能力包含：泛型函数、泛型结构体、Trait 定义、Trait 实现、Trait bounds、默认实现、 Trait 继承
- 触发条件：需要编写通用代码、实现接口抽象、处理类型约束

## 前置准备

- 完成 rust-core-skill 和 rust-struct-enum-skill
- 理解 Rust 所有权的特殊性

## 泛型基础

### 泛型函数

```rust
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }
    largest
}

fn main() {
    let numbers = vec![34, 50, 25, 100, 65];
    println!("最大: {}", largest(&numbers));

    let chars = vec!['y', 'm', 'a', 'q'];
    println!("最大: {}", largest(&chars));
}
```

### 泛型结构体

```rust
struct Point<T> {
    x: T,
    y: T,
}

struct Point2<T, U> {
    x: T,
    y: U,
}

impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}

impl<T: Clone, U: Clone> Point2<T, U> {
    fn clone_fields(&self) -> Point2<T, U> {
        Point2 {
            x: self.x.clone(),
            y: self.y.clone(),
        }
    }
}

fn main() {
    let p1 = Point { x: 5, y: 10 };
    let p2 = Point { x: 1.0, y: 4.0 };
    let p3 = Point2 { x: 5, y: 10.5 };
}
```

### 泛型枚举

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}

enum Option<T> {
    Some(T),
    None,
}

enum Either<L, R> {
    Left(L),
    Right(R),
}
```

## Trait 系统

### 定义 Trait

```rust
pub trait Summary {
    fn summarize(&self) -> String;

    // 默认实现
    fn summarize_author(&self) -> String {
        String::from("(Unknown)")
    }
}

pub struct Tweet {
    pub username: String,
    pub content: String,
}

impl Summary for Tweet {
    fn summarize(&self) -> String {
        format!("@{}: {}", self.username, self.content)
    }

    // 可以覆盖默认实现
    fn summarize_author(&self) -> String {
        format!("@{}", self.username)
    }
}
```

### Trait 实现

```rust
pub struct NewsArticle {
    pub headline: String,
    pub location: String,
    pub author: String,
    pub content: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!("{}, by {} ({})", self.headline, self.author, self.location)
    }
}

pub struct BlogPost {
    pub title: String,
    pub content: String,
}

impl Summary for BlogPost {
    fn summarize(&self) -> String {
        format!("{}", self.title)
    }
}
```

### Trait 作为参数

```rust
// Trait bound 语法
pub fn notify(item: &impl Summary) {
    println!("速报: {}", item.summarize());
}

// Trait bound 完整语法
pub fn notify<T: Summary>(item: &T) {
    println!("速报: {}", item.summarize());
}

// 多个参数
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
    // ...
}

// 同一类型
pub fn notify<T: Summary>(item1: &T, item2: &T) {
    // ...
}
```

### Trait Bound 复杂约束

```rust
use std::fmt::{Debug, Display};

fn some_function<T, U>(t: &T, u: &U)
where
    T: Display + Clone,
    U: Clone + Debug,
{
    println!("T: {}", t);
    println!("U: {:?}", u);
}
```

### 返回 Trait 类型

```crate
fn returns_summarizable() -> impl Summary {
    Tweet {
        username: String::from("horse_ebooks"),
        content: String::from("of course, as you probably already know, people"),
    }
}
```

### 使用 Trait Bounds 有条件地实现方法

```rust
use std::fmt::Display;

struct Pair<T> {
    x: T,
    y: T,
}

impl<T> Pair<T> {
    fn new(x: T, y: T) -> Self {
        Self { x, y }
    }
}

// 仅当 T 实现 Display + PartialOrd 时实现此方法
impl<T: Display + PartialOrd> Pair<T> {
    fn cmp_display(&self) {
        if self.x >= self.y {
            println!("最大的成员是 x = {}", self.x);
        } else {
            println!("最大的成员是 y = {}", self.y);
        }
    }
}
```

## 常用标准库 Trait

### Display 和 Debug

```rust
use std::fmt;

struct Point {
    x: i32,
    y: i32,
}

// 必须先实现 Debug 才能手动实现 Display
impl fmt::Debug for Point {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("Point")
            .field("x", &self.x)
            .field("y", &self.y)
            .finish()
    }
}

impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

println!("{:?}", point);  // Debug
println!("{}", point);   // Display
```

### Clone 和 Copy

```rust
#[derive(Debug, Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}

let p1 = Point { x: 1, y: 2 };
let p2 = p1;      // Copy（自动复制）
let p3 = p1.clone(); // Clone（显式深拷贝）
```

### Default

```rust
#[derive(Debug)]
struct Config {
    port: u16,
    host: String,
    max_connections: u32,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            port: 80,
            host: String::from("localhost"),
            max_connections: 100,
        }
    }
}

let config = Config::default();
let config2 = Config {
    port: 8080,
    ..Default::default()
};
```

### From 和 Into

```rust
use std::convert::From;

#[derive(Debug)]
struct Number {
    value: i32,
}

impl From<i32> for Number {
    fn from(item: i32) -> Self {
        Number { value: item }
    }
}

let num = Number::from(5);
let num: Number = 5.into();
```

### PartialEq 和 Eq

```rust
#[derive(Debug, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

let p1 = Point { x: 1, y: 2 };
let p2 = Point { x: 1, y: 2 };
let p3 = Point { x: 3, y: 4 };

println!("{}", p1 == p2);  // true
println!("{}", p1 == p3);  // false
```

### 运算符 Trait

```rust
use std::ops::Add;

#[derive(Debug, Copy, Clone)]
struct Point {
    x: i32,
    y: i32,
}

impl Add for Point {
    type Output = Point;

    fn add(self, other: Point) -> Point {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

impl Add<(i32, i32)> for Point {
    type Output = Point;

    fn add(self, (rx, ry): (i32, i32)) -> Point {
        Point {
            x: self.x + rx,
            y: self.y + ry,
        }
    }
}
```

## Trait 对象（动态分发）

```rust
pub trait Drawable {
    fn draw(&self);
}

pub struct Circle {
    pub radius: f64,
}

impl Drawable for Circle {
    fn draw(&self) {
        println!("Drawing circle with radius {}", self.radius);
    }
}

pub struct Square {
    pub side: f64,
}

impl Drawable for Square {
    fn draw(&self) {
        println!("Drawing square with side {}", self.side);
    }
}

// 存储不同类型的集合
pub struct Canvas {
    pub items: Vec<Box<dyn Drawable>>,
}

impl Canvas {
    pub fn add(&mut self, item: Box<dyn Drawable>) {
        self.items.push(item);
    }

    pub fn draw_all(&self) {
        for item in &self.items {
            item.draw();
        }
    }
}
```

## Trait 高级特性

###  trait 继承

```rust
trait Printable: Debug {
    fn print(&self);
}

impl Printable for Point {
    fn print(&self) {
        println!("{:?}", self);
    }
}
```

### 关联类型

```rust
pub trait Iterator {
    type Item;  // 关联类型

    fn next(&mut self) -> Option<Self::Item>;
}

struct Counter {
    count: u32,
}

impl Counter {
    fn new() -> Counter {
        Counter { count: 0 }
    }
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        if self.count < 5 {
            self.count += 1;
            Some(self.count)
        } else {
            None
        }
    }
}
```

## 资源索引

- 泛型：https://doc.rust-lang.org/book/ch10-01-syntax.html
- Trait：https://doc.rust-lang.org/book/ch10-02-traits.html
- 高级 Trait：https://doc.rust-lang.org/book/ch19-03-advanced-traits.html

## 注意事项

- 泛型在编译时单态化，无运行时开销
- Trait 对象有虚函数表（vtable）运行时开销
- 使用 `derive` 自动实现常用 Trait
- Trait bounds 可以使用 `where` 子句简化
- 关联类型 vs 泛型参数：关联类型每个实现只有一个，泛型参数可以有多个实现
