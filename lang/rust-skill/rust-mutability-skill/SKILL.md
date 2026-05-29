---
name: rust-mutability-skill
description: Rust Layer 1 技能 - 可变性设计，核心问题：为什么这个数据需要变化？掌握 mut、Cell、UnsafeCell 的使用场景
version: 1.0.0
layer: 1
trigger: mut, Cell, UnsafeCell, E0596, interior mutability, mutation
---

# Rust Mutability - Layer 1

## 核心问题

为什么这个数据需要变化？

## 元认知追溯

```
问题 → Layer 1: mut 语法
        ↓
是否必须可变? → Layer 2: 设计选择
        ↓
为什么需要变化? → Layer 3: 领域约束
```

## 可变性模式

### 顶层可变性

```rust
let mut x = 5;
x += 1; // 直接修改

fn increment(x: &mut i32) {
    *x += 1;
}
```

### 内部可变性 - Cell<T>

```rust
use std::cell::Cell;

// T 必须实现 Copy
let cell = Cell::new(42);
cell.set(100); // 获取内部值并设置新值

println!("{}", cell.get()); // 100
```

### 内部可变性 - RefCell<T>

```rust
use std::cell::RefCell;

let cell = RefCell::new(vec![1, 2, 3]);

// 运行时借用检查
cell.borrow_mut().push(4);
println!("{:?}", cell.borrow());
```

### 内部可变性 - UnsafeCell<T>

```rust
use std::cell::UnsafeCell;

// 编译器信任的 unsafe 内部可变性
unsafe {
    let cell = UnsafeCell::new(42);
    *cell.get() = 100;
}
```

## 选择指南

| 场景 | 推荐 | 说明 |
|------|------|------|
| Copy 类型，局部变量 | Cell<T> | 无引用开销 |
| 需要引用，运行时检查 | RefCell<T> | 借用规则运行时检查 |
| unsafe 上下文 | UnsafeCell<T> | 信任开发者 |
| 跨线程可变 | Mutex<T> / RwLock<T> | 线程安全 |

## 常见错误

### E0596 - 可变借用错误

```rust
let x = 5;
let y = &x;
// *y = 10; // 错误：y 是不可变借用

// 解决
let mut x = 5;
let y = &mut x; // OK
```

### 借用冲突

```rust
let cell = RefCell::new(vec![1, 2, 3]);

let r1 = cell.borrow();
// let r2 = cell.borrow(); // 运行时 panic：同时借用
drop(r1);
let r2 = cell.borrow(); // OK
```

## 与其他技能关联

- 所有权：可变借用影响所有权转移
- 线程安全：多线程需要 `Mutex`/`RwLock`

## 资源索引

- [Cell 文档](https://doc.rust-lang.org/std/cell/struct.Cell.html)
- [RefCell 文档](https://doc.rust-lang.org/std/cell/struct.RefCell.html)
- [UnsafeCell 文档](https://doc.rust-lang.org/std/cell/struct.UnsafeCell.html)

## 注意事项

- 优先使用不可变设计，需要时才用可变
- `Cell<T>` 仅适用于 `Copy` 类型
- `RefCell` 有运行时开销，慎用
- 跨线程场景使用 `Mutex`/`RwLock`
