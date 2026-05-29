---
name: rust-resource-management-skill
description: Rust Layer 1 技能 - 资源管理模式，核心问题：什么所有权模式适合？掌握 Box、Rc、Arc、RefCell 等智能指针的选择
version: 1.0.0
layer: 1
trigger: Box, Rc, Arc, RefCell, Cow, ownership pattern, shared ownership
---

# Rust Resource Management - Layer 1

## 核心问题

什么所有权模式适合这个场景？

## 元认知追溯

```
问题 → Layer 1: 语言机制
        ↓
为什么需要共享? → Layer 3: 领域约束
        ↓
选择合适的所有权模式 → Layer 2: 设计选择
```

## 资源管理模式

### Box<T> - 堆分配

```rust
// 单所有权，堆分配
let b = Box::new(42);

// 模式匹配
match boxed_value {
    Box::new(x) => println!("{}", x),
}

// 递归类型
enum List<T> {
    Cons(T, Box<List<T>>),
    Nil,
}
```

### Rc<T> - 单线程引用计数

```rust
use std::rc::Rc;

// 共享所有权，不可变引用
let rc1 = Rc::new(42);
let rc2 = rc1.clone(); // 引用计数 +1

println!("{}", Rc::strong_count(&rc1)); // 2

// 不可变访问
println!("{}", *rc1);
```

### Arc<T> - 多线程引用计数

```rust
use std::sync::Arc;

// 跨线程共享所有权
let arc = Arc::new(42);
let arc2 = arc.clone(); // 原子操作，线程安全

std::thread::spawn({
    let arc = arc.clone();
    move || println!("{}", *arc)
});
```

### RefCell<T> - 内部可变性

```rust
use std::cell::RefCell;

// 单线程内部可变性
let cell = RefCell::new(42);

// 运行时借用检查
let r = cell.borrow();  // Ref<T>
let mut r = cell.borrow_mut(); // RefMut<T>
```

### 组合模式

```rust
use std::rc::Rc;
use std::cell::RefCell;

// Rc<RefCell<T>> - 共享可变状态（单线程）
let shared = Rc::new(RefCell::new(42));

// Arc<Mutex<T>> - 跨线程共享可变状态
use std::sync::{Arc, Mutex};
let shared = Arc::new(Mutex::new(42));
```

## 选择指南

| 场景 | 推荐 | 原因 |
|------|------|------|
| 堆分配，单所有权 | Box<T> | 最小开销 |
| 单线程共享不可变 | Rc<T> | 轻量级引用计数 |
| 多线程共享不可变 | Arc<T> | 原子引用计数 |
| 单线程共享可变 | Rc<RefCell<T>> | 运行时借用检查 |
| 多线程共享可变 | Arc<Mutex<T>> | 互斥锁保护 |
| 多线程共享可变 | Arc<RwLock<T>> | 读写锁优化 |

## 常见错误

### E0506 - 所有权已移动

```rust
let s1 = String::from("hello");
let s2 = s1;
// s1 已移动，s2 拥有所有权

// 解决：使用克隆
let s2 = s1.clone();

// 或使用共享所有权
let s1 = Rc::new(String::from("hello"));
let s2 = s1.clone();
```

### E0596 - 不可变绑定不能可变借用

```rust
let x = 5;
// x += 1; // 错误：x 是不可变的

let mut x = 5;
x += 1; // OK
```

## 资源索引

- [Box 文档](https://doc.rust-lang.org/std/boxed/struct.Box.html)
- [Rc 文档](https://doc.rust-lang.org/std/rc/struct.Rc.html)
- [Arc 文档](https://doc.rust-lang.org/std/sync/struct.Arc.html)
- [RefCell 文档](https://doc.rust-lang.org/std/cell/struct.RefCell.html)

## 注意事项

- 优先使用 `Box<T>`，只有在需要共享时才考虑 `Rc`/`Arc`
- `Rc` 不能跨线程使用，`Arc` 有额外原子操作开销
- `RefCell` 提供运行时借用检查，适合需要可变访问的场景
