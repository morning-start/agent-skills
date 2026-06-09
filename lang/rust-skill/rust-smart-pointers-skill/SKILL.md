---
name: rust-smart-pointers
version: 1.0.0
author: book-skills
description: Rust 智能指针技能，掌握 Box<T>、Rc<T>、Arc<T>、RefCell<T>、Cell<T> 等指针类型的使用场景
tags: [rust, smart-pointers, rc, arc, refcell]
layer: Layer 1 - Language Mechanics
trigger: box, rc, arc, refcell, cow
---

# Rust 智能指针

## 任务目标

- 本 Skill 用于：管理堆分配内存、处理共享所有权、实现内部可变性
- 能力包含：Box 堆分配、Rc 引用计数、Arc 原子引用计数、RefCell 内部可变性、Cell
- 触发条件：需要堆分配、共享数据、可变数据、多线程共享

## 前置准备

- 完成 rust-ownership-skill 所有权系统
- 理解借用规则

## Box<T> 堆分配

### 基础用法

```rust
let b = Box::new(5);
println!("{}", b);  // 5

// 解引用
let b = Box::new(5);
assert_eq!(*b, 5);

// 修改
let mut b = Box::new(5);
*b = 10;
```

### 递归类型

```rust
// 列表类型
enum List {
    Cons(i32, Box<List>),
    Nil,
}

use crate::List::{Cons, Nil};

let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));
```

### trait 对象

```rust
trait Drawable {
    fn draw(&self);
}

struct Circle {
    radius: f64,
}

impl Drawable for Circle {
    fn draw(&self) {
        println!("Drawing circle with radius {}", self.radius);
    }
}

let drawable: Box<dyn Drawable> = Box::new(Circle { radius: 1.0 });
drawable.draw();
```

### 函数返回指针

```rust
fn create_box() -> Box<i32> {
    let b = Box::new(5);
    b  // 自动解构，堆上的值被返回
}

let b = create_box();
```

## Rc<T> 引用计数（单线程）

### 基本用法

```rust
use std::rc::Rc;

let rc1 = Rc::new(5);
println!("count after creating: {}", Rc::strong_count(&rc1));  // 1

let rc2 = rc1.clone();
println!("count after clone: {}", Rc::strong_count(&rc1));  // 2

{
    let rc3 = rc1.clone();
    println!("count in inner scope: {}", Rc::strong_count(&rc1));  // 3
}
println!("count after inner scope: {}", Rc::strong_count(&rc1));  // 2

// 读取值
println!("value: {}", *rc1);  // 5
```

### 不可变共享

```rust
use std::rc::Rc;

let shared = Rc::new(vec![1, 2, 3]);

let share1 = shared.clone();
let share2 = shared.clone();

// 只能不可变借用
println!("{:?}", *share1);  // OK
// share1.push(4);  // 错误：不能可变借用

// 如果需要可变，使用 RefCell
```

### 与 RefCell 组合

```rust
use std::rc::Rc;
use std::cell::RefCell;

let shared = Rc::new(RefCell::new(vec![1, 2, 3]));

let share1 = shared.clone();
let share2 = shared.clone();

// 可变借用
share1.borrow_mut().push(4);

println!("{:?}", *share2.borrow());  // [1, 2, 3, 4]
```

## RefCell<T> 内部可变性

### 基础用法

```rust
use std::cell::RefCell;

let data = RefCell::new(5);

// 不可变借用
let r = data.borrow();
println!("{}", *r);

// 可变借用
let mut w = data.borrow_mut();
*w = 10;

// 借用检查在运行时
// let r2 = data.borrow();  // panic: already borrowed
```

### 运行时借用检查

```rust
use std::cell::RefCell;

let data = RefCell::new(vec![1, 2, 3]);

// 安全的可变访问
data.borrow_mut().push(4);

// 借用规则在运行时检查
// let r1 = data.borrow();
// let r2 = data.borrow();  // panic
```

### 常见模式

```rust
use std::cell::RefCell;

struct Logger {
    messages: RefCell<Vec<String>>,
}

impl Logger {
    fn new() -> Self {
        Logger { messages: RefCell::new(Vec::new()) }
    }

    fn log(&self, msg: &str) {
        self.messages.borrow_mut().push(msg.to_string());
    }

    fn get_messages(&self) -> Vec<String> {
        self.messages.borrow().clone()
    }
}

let logger = Logger::new();
logger.log("message 1");
logger.log("message 2");
println!("{:?}", logger.get_messages());
```

## Cell<T> vs RefCell<T>

| 类型 | 复制值 | 借用 | 适用场景 |
|------|--------|------|----------|
| Cell<T> | Copy T | 通过 get/set | 单值，Copy 类型 |
| RefCell<T> | Clone T | borrow/borrow_mut | 需要引用语义 |

### Cell<T>

```rust
use std::cell::Cell;

let cell = Cell::new(5);

// 获取值（Copy）
let n = cell.get();
println!("{}", n);  // 5

// 设置值
cell.set(10);

// 通过引用设置
let mut value = 5;
let cell = Cell::new(&mut value);
cell.get_mut();
```

### RefCell<T>

```rust
use std::cell::RefCell;

let cell = RefCell::new(vec![1, 2, 3]);

// borrow - 返回 Ref<T>
// borrow_mut - 返回 RefMut<T>

let mut borrowed = cell.borrow_mut();
borrowed.push(4);
drop(borrowed);

println!("{:?}", *cell.borrow());
```

## Rc<RefCell<T>> 组合

```rust
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
enum List {
    Cons(Rc<RefCell<i32>>, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};

let value = Rc::new(RefCell::new(5));

let list = Cons(
    value.clone(),
    Rc::new(Cons(
        value.clone(),
        Rc::new(Nil),
    )),
);

// 修改值
*value.borrow_mut() = 10;

println!("{:?}", list);
```

## Arc<T> 原子引用计数（多线程）

### 基本用法

```rust
use std::sync::Arc;
use std::thread;

let shared = Arc::new(5);

let handle = thread::spawn({
    let shared = shared.clone();
    move || {
        println!("thread value: {}", *shared);
    }
});

println!("main value: {}", *shared);
handle.join().unwrap();

println!("count: {}", Arc::strong_count(&shared));  // 2
```

### Arc 与 Mutex

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));

let handles: Vec<_> = (0..10).map(|_| {
    let counter = counter.clone();
    thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    })
}).collect();

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap());  // 10
```

### Arc 与 RwLock

```rust
use std::sync::{Arc, RwLock};
use std::thread;

let data = Arc::new(RwLock::new(vec![1, 2, 3]));

let handles: Vec<_> = (0..3).map(|i| {
    let data = data.clone();
    thread::spawn(move || {
        let mut writer = data.write().unwrap();
        writer.push(i * 10);
    })
}).collect();

for handle in handles {
    handle.join().unwrap();
}

println!("{:?}", *data.read().unwrap());  // [1, 2, 3, 0, 10, 20]
```

## 指针类型选择指南

| 场景 | 推荐类型 |
|------|----------|
| 堆分配单所有权 | Box<T> |
| 不可变共享（单线程） | Rc<T> |
| 可变共享（单线程） | Rc<RefCell<T>> |
| 不可变共享（多线程） | Arc<T> |
| 可变共享（多线程） | Arc<Mutex<T>> 或 Arc<RwLock<T>> |
| 简单可变性（Copy） | Cell<T> |
| 运行时借用检查 | RefCell<T> |

## Rc vs Arc 对比

```rust
// Rc - 非原子引用计数（快，单线程）
use std::rc::Rc;
let rc = Rc::new(5);
let rc2 = rc.clone();

// Arc - 原子引用计数（稍慢，多线程安全）
use std::sync::Arc;
let arc = Arc::new(5);
let arc2 = arc.clone();
```

## Weak<T>

```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Node {
    value: i32,
    parent: RefCell<Weak<Node>>,
    children: RefCell<Vec<Rc<Node>>>,
}

let leaf = Rc::new(Node {
    value: 3,
    parent: RefCell::new(Weak::new()),
    children: RefCell::new(Vec::new()),
});

let branch = Rc::new(Node {
    value: 5,
    parent: RefCell::new(Weak::new()),
    children: RefCell::new(vec![leaf.clone()]),
});

// 避免循环引用
*leaf.parent.borrow_mut() = Rc::downgrade(&branch);

println!("leaf parent strong: {}", leaf.parent.borrow().upgrade().is_some());
```

## 资源索引

- 智能指针：https://doc.rust-lang.org/book/ch15-00-smart-pointers.html
- Box：https://doc.rust-lang.org/std/boxed/struct.Box.html
- Rc：https://doc.rust-lang.org/std/rc/struct.Rc.html
- Arc：https://doc.rust-lang.org/std/sync/struct.Arc.html
- RefCell：https://doc.rust-lang.org/std/cell/struct.RefCell.html

## 注意事项

- Box<T> 始终是单所有权，无额外开销
- Rc<T> 有引用计数开销，不支持多线程
- RefCell<T> 运行时检查借用，可能 panic
- Arc<T> 使用原子操作，有一定性能成本
- 避免 Rc<RefCell<T>> 循环引用
- 多线程场景使用 Arc<Mutex<T>> 或 Arc<RwLock<T>>
