---
name: rust-mental-model-skill
description: Rust Layer 2 技能 - 心智模型，核心问题：如何正确理解 Rust 的这些概念？掌握所有权、借用、生命周期等核心概念的心智模型
version: 1.0.0
layer: 2
trigger: learning, mental model, understanding, concept, beginner, why
---

# Rust Mental Model - Layer 2

## 核心问题

如何正确理解 Rust 的这些概念？

## 元认知追溯

```
问题 → Layer 2: 心智模型
        ↓
概念类比 → Layer 3: 已知领域
        ↓
形式化理解 → Layer 1: 语法规则
```

## 所有权心智模型

### 类比：书籍与借阅

```rust
// 你拥有一本书（值的所有权）
let book = String::from("The Rust Programming Language");

// 你把书借给朋友（借用）
fn read_book(book: &String) {
    println!("{}", book);
} // 朋友把书还给你（借用结束）

read_book(&book); // 借出
println!("{}", book); // 你仍然拥有这本书
```

### 所有权的三条规则

```
1. Rust 中每个值有一个所有者
2. 同时只能有一个所有者
3. 当所有者离开作用域，值被丢弃
```

## 借用心智模型

### 类比：图书馆的借书证

```rust
// 不可变借用 - 只能阅读
let library = vec![String::from("Book 1"), String::from("Book 2")];
let reader = &library; // 借阅证

// reader 和 library 都能访问
println!("{:?}", library);
println!("{:?}", reader);

// 可变借用 - 可以修改
let mut library = vec![String::from("Book 1")];
{
    let modifier = &mut library;
    modifier.push(String::from("Book 2"));
} // 修改完成，释放可变借用

println!("{:?}", library);
```

### 借用规则

```
1. 可以有任意数量的不可变借用
2. 只能有一个可变借用
3. 不可变借用和可变借用不能同时存在
```

## 生命周期心智模型

### 类比：合同的有效期

```rust
// 'a 是生命周期的名字
// 这个函数说：返回值的生命周期 = 输入借用的较短者
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// 合同：返回值的有效期 = 较短合同的有效期
```

### 生命周期省略

```rust
// 编译器自动推断
fn first_word(s: &str) -> &str {
    s.split_whitespace().next().unwrap_or("")
}

// 等价于
fn first_word<'a>(s: &'a str) -> &'a str {
    s.split_whitespace().next().unwrap_or("")
}
```

## Trait 心智模型

### 类比：接口契约

```rust
// 定义一个接口/契约
trait Drawable {
    fn draw(&self);
}

// 实现契约
struct Circle;
struct Square;

impl Drawable for Circle {
    fn draw(&self) { println!("Circle"); }
}

impl Drawable for Square {
    fn draw(&self) { println!("Square"); }
}
```

## 错误处理心智模型

### 类比：飞行计划

```rust
// Result = 成功(值) 或 失败(原因)
enum Result<T, E> {
    Ok(T),
    Err(E),
}

// Option = 有(值) 或 无
enum Option<T> {
    Some(T),
    None,
}

// 航班可能延误或取消
fn book_flight() -> Result<Ticket, FlightError> {
    if available() {
        Ok(Ticket::new())
    } else {
        Err(FlightError::FullyBooked)
    }
}
```

## 常见误解纠正

### 误解 vs 真相

| 误解 | 真相 |
|------|------|
| Rust 很难 | 规则少且一致 |
| 所有权限制太多 | 编译时检查，无运行时开销 |
| 必须手动管理内存 | 编译器自动插入 drop 代码 |
| 生命周期很复杂 | 只是借用的有效期标注 |

## 学习路径

```rust
1. 变量和所有权 - 赋值/移动
2. 引用和借用 - 只读/可变借用
3. 结构体和方法 - self 参数
4. 生命周期 - 借用有效期
5. Trait - 多态
6. 错误处理 - Result/Option
```

## 资源索引

- [The Rust Book](https://doc.rust-lang.org/book/)
- [Rust By Example](https://doc.rust-lang.org/rust-by-example/)
- [Rustlings](https://github.com/rust-lang/rustlings/)

## 注意事项

- 不要类比过度，形式化理解最终必要
- 多写代码，实践中内化规则
- 善用编译器错误学习
