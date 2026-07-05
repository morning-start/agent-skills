---
name: rust-zero-cost
version: 1.0.0
author: book-skills
description: Rust Layer 1 技能 - 零成本抽象，核心问题：编译时多态还是运行时多态？掌握泛型、Trait、trait object 的性能特点
tags: [rust, zero-cost, generics, monomorphization, inline]
layer: Layer 1 - Language Mechanics
trigger: generic, trait, trait object, dyn, monomorphization, E0277
---

# Rust Zero-Cost Abstraction - Layer 1

## 核心问题

编译时多态还是运行时多态？

## 元认知追溯

```
问题 → Layer 1: trait/泛型语法
        ↓
静态分发 vs 动态分发 → Layer 2: 设计选择
        ↓
性能需求 vs 灵活性 → Layer 3: 领域约束
```

## 泛型 - 编译时多态

```rust
// 泛型函数
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];
    for item in list.iter() {
        if item > largest {
            largest = item;
        }
    }
    largest
}

// 泛型结构体
struct Point<T> {
    x: T,
    y: T,
}

let p1 = Point { x: 1, y: 2 };
let p2 = Point { x: 1.0, y: 2.0 };
```

### 单态化 (Monomorphization)

```rust
// 编译器为每个类型实例生成具体代码
let i = largest(&[1, 2, 3]);     // i32 版本
let f = largest(&[1.0, 2.0]);    // f64 版本
```

## Trait - 静态分发

```rust
trait Drawable {
    fn draw(&self);
}

struct Circle { radius: f64 }
struct Square { side: f64 }

impl Drawable for Circle {
    fn draw(&self) {
        println!("Circle: {}", self.radius);
    }
}

impl Drawable for Square {
    fn draw(&self) {
        println!("Square: {}", self.side);
    }
}

// 泛型约束 - 静态分发
fn render<T: Drawable>(shape: &T) {
    shape.draw();
}

render(&circle); // 编译时确定调用
```

## Trait Object - 运行时多态

```rust
trait Drawable {
    fn draw(&self);
}

// 动态分发
fn render_dynamic(shape: &dyn Drawable) {
    shape.draw();
}

// 运行时查表调用
render_dynamic(&circle);
render_dynamic(&square);
```

## 性能对比

| 分发方式 | 优点 | 缺点 | 适用场景 |
|---------|------|------|---------|
| 泛型 | 零成本，无虚表 | 代码膨胀 | 类型已知，静态调用 |
| trait object | 灵活，减小二进制 | 虚表查找开销 | 类型未知，需要存储异构集合 |

## 常用 Trait

```rust
// 标准库常用 trait
impl Clone for MyType { }           // 克隆
impl Copy for MyType { }            // 位拷贝
impl Debug for MyType { }           // 格式化调试
impl Display for MyType { }         // 用户显示
impl Default for MyType { }         // 默认值
impl serde::Serialize for MyType { } // 序列化
```

## 常见错误

### E0277 - Trait 未实现

```rust
trait Serializable {
    fn serialize(&self);
}

// fn save(s: &impl Serializable) { } // Error

// 解决：添加 trait bound
fn save<S: Serializable>(s: &S) {
    s.serialize();
}
```

## 选择指南

| 场景 | 推荐 |
|------|------|
| 性能关键代码 | 泛型静态分发 |
| 需要存储不同类型 | trait object |
| 需要返回不同类型 | trait object |
| 泛型约束不足 | trait object |

## 资源索引

- [Trait 对象](https://doc.rust-lang.org/book/ch17-02-trait-objects.html)
- [泛型](https://doc.rust-lang.org/book/ch10-01-syntax.html)
- [Trait Bound](https://doc.rust-lang.org/book/ch10-02-traits.html)

## 注意事项

- "零成本" 意味着：你不为你不用的东西付费
- 泛型在编译时单态化，无运行时开销
- trait object 有虚表查找开销
- 优先使用泛型，性能不够时再用 trait object
