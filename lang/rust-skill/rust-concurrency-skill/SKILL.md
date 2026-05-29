---
name: rust-concurrency
description: Rust 并发编程技能，掌握线程创建、消息传递、共享状态、Send 和 Sync 等并发原语
version: 1.0.0
---

# Rust 并发编程

## 任务目标

- 本 Skill 用于：编写多线程 Rust 程序，实现线程间通信和共享数据
- 能力包含：线程管理、消息通道、Mutex、Arc、Send/Sync trait、死锁避免
- 触发条件：需要并行处理、共享数据、线程间通信

## 前置准备

- 完成 rust-core-skill 和 rust-smart-pointers-skill
- 理解 Rust 所有权的特殊性

## 线程创建

### 基础用法

```rust
use std::thread;
use std::time::Duration;

let handle = thread::spawn(|| {
    for i in 1..5 {
        println!("spawned thread: {}", i);
        thread::sleep(Duration::from_millis(100));
    }
});

// 主线程继续执行
for i in 1..3 {
    println!("main thread: {}", i);
    thread::sleep(Duration::from_millis(100));
}

// 等待线程完成
handle.join().unwrap();
```

### move 闭包

```rust
use std::thread;

let data = vec![1, 2, 3];

let handle = thread::spawn(move || {
    println!("data: {:?}", data);
});

// data 在这里不能再使用
// println!("{:?}", data);  // 错误：data 已移动

handle.join().unwrap();
```

### thread::sleep

```rust
use std::thread;
use std::time::Duration;

thread::sleep(Duration::from_secs(1));
thread::sleep(Duration::from_millis(500));
thread::sleep(Duration::from_nanos(1000));
```

### 获取线程信息

```rust
use std::thread;

let handle = thread::spawn(|| {
    println!("Thread ID: {:?}", thread::current().id());
    println!("Thread name: {:?}", thread::current().name());
});

handle.join().unwrap();

// 获取当前线程
let current = thread::current();
println!("{:?}", current.id());
```

### 构建多线程

```rust
use std::thread;

let handles: Vec<_> = (0..4).map(|i| {
    thread::spawn(move || {
        println!("Thread {}", i);
    })
}).collect();

for handle in handles {
    handle.join().unwrap();
}
```

## 消息传递

### mpsc::channel

```rust
use std::sync::mpsc;
use std::thread;

let (tx, rx) = mpsc::channel();

thread::spawn(move || {
    let msg = String::from("hello");
    tx.send(msg).unwrap();
    // msg 不能再使用
});

let received = rx.recv().unwrap();
println!("Got: {}", received);
```

### 发送多个消息

```rust
use std::sync::mpsc;
use std::thread;

let (tx, rx) = mpsc::channel();

for i in 0..5 {
    let tx = tx.clone();
    thread::spawn(move || {
        tx.send(i).unwrap();
    });
}

drop(tx);  // 关闭发送端

for msg in rx {
    println!("Received: {}", msg);
}
```

### 多发送者

```rust
use std::sync::mpsc;
use std::thread;

let (tx, rx) = mpsc::channel();

let tx1 = tx.clone();
let tx2 = tx.clone();

thread::spawn(move || {
    tx1.send(1).unwrap();
});

thread::spawn(move || {
    tx2.send(2).unwrap();
});

drop(tx);

let result = rx.recv().unwrap() + rx.recv().unwrap();
println!("Result: {}", result);  // 3
```

### 迭代器接收

```rust
use std::sync::mpsc;
use std::thread;

let (tx, rx) = mpsc::channel();

thread::spawn(move || {
    for i in 0..3 {
        tx.send(i).unwrap();
    }
});

for msg in rx {  // 自动等待
    println!("Received: {}", msg);
}
```

### 非阻塞接收

```rust
use std::sync::mpsc;

let (tx, rx) = mpsc::channel();

// try_recv 不阻塞
loop {
    match rx.try_recv() {
        Ok(msg) => println!("Got: {}", msg),
        Err(_) => {
            println!("No message yet");
            break;
        }
    }
}
```

## 共享状态

### Mutex<T>

```rust
use std::sync::Mutex;
use std::thread;

let counter = Mutex::new(0);

let mut handles: Vec<_> = (0..10).map(|_| {
    let counter = Mutex::new(counter.inner().clone());
    thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    })
}).collect();

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap());
```

### 多线程共享 Mutex

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles: Vec<_> = Vec::new();

for _ in 0..8 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap());
```

### RwLock<T>

```rust
use std::sync::{Arc, RwLock};
use std::thread;

let data = Arc::new(RwLock::new(vec![1, 2, 3]));

// 读锁
let r1 = data.read().unwrap();
let r2 = data.read().unwrap();
println!("{:?}", *r1);
drop(r1);
drop(r2);

// 写锁
let mut w = data.write().unwrap();
w.push(4);
```

### Atomic 类型

```rust
use std::sync::atomic::{AtomicUsize, Ordering};
use std::thread;

let counter = AtomicUsize::new(0);

let handles: Vec<_> = (0..8).map(|_| {
    thread::spawn(|| {
        counter.fetch_add(1, Ordering::SeqCst);
    })
}).collect();

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", counter.load(Ordering::SeqCst));
```

### 常用 Atomic 类型

```rust
use std::sync::atomic::*;

let a = AtomicBool::new(false);
a.store(true, Ordering::SeqCst);

let b = AtomicI32::new(0);
b.fetch_add(5, Ordering::SeqCst);

let c = AtomicPtr::new(std::ptr::null_mut());
```

## Send 和 Sync

### Send - 可以在线程间转移所有权

```rust
use std::marker::Send;

// 基本类型默认 Send
struct MyStruct {
    data: i32,
}

// 手动实现
unsafe impl Send for MyStruct {}
```

### Sync - 可以在线程间共享引用

```rust
use std::marker::Sync;

// 基本类型默认 Sync
struct MyStruct {
    data: i32,
}

// 手动实现
unsafe impl Sync for MyStruct {}
```

### 常用类型的 Send/Sync

| 类型 | Send | Sync |
|------|------|------|
| i32 | Yes | Yes |
| &T | Yes (T: Sync) | Yes (T: Send) |
| Mutex<T> | Yes | Yes |
| Rc<T> | **No** | **No** |
| Arc<T> | Yes | Yes |
| RefCell<T> | **No** | **No** |
| Cell<T> | **No** | **No** |

## Condition Variables

```rust
use std::sync::{Arc, Mutex, Condvar};
use std::thread;

let pair = Arc::new((Mutex::new(false), Condvar::new()));
let pair2 = pair.clone();

thread::spawn(move || {
    let (lock, cvar) = &*pair2;
    let mut started = lock.lock().unwrap();
    *started = true;
    println!("Worker thread started");
    cvar.notify_one();
});

let (lock, cvar) = &*pair;
let mut started = lock.lock().unwrap();
while !*started {
    started = cvar.wait(started).unwrap();
}
println!("Main thread running");
```

## Barrier

```rust
use std::sync::{Arc, Barrier};
use std::thread;

let barrier = Arc::new(Barrier::new(3));
let mut handles = Vec::new();

for i in 0..3 {
    let barrier = barrier.clone();
    let handle = thread::spawn(move || {
        println!("Thread {} phase 1", i);
        barrier.wait();
        println!("Thread {} phase 2", i);
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}
```

## Once 和 OnceLock

```rust
use std::sync::{Arc, OnceLock};
use std::thread;

static INIT: OnceLock<i32> = OnceLock::new();

let handle = thread::spawn(|| {
    let result = INIT.get_or_init(|| {
        println!("Initializing");
        42
    });
    println!("Thread 1: {}", result);
});

let handle2 = thread::spawn(|| {
    let result = INIT.get_or_init(|| {
        println!("Initializing again");
        100
    });
    println!("Thread 2: {}", result);
});

handle.join().unwrap();
handle2.join().unwrap();
```

## 常见并发模式

### 生产者-消费者

```rust
use std::sync::mpsc;
use std::thread;

let (tx, rx) = mpsc::channel();

for i in 0..3 {
    let tx = tx.clone();
    thread::spawn(move || {
        tx.send(i * 2).unwrap();
    });
}

drop(tx);

let sum: i32 = rx.iter().sum();
println!("Sum: {}", sum);
```

### 工作池

```rust
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

struct Worker {
    id: usize,
}

impl Worker {
    fn process_job(&self, job: i32) {
        println!("Worker {} processing job {}", self.id, job);
        thread::sleep(Duration::from_millis(50));
    }
}

let num_jobs = 20;
let num_workers = 4;

let job_queue = Arc::new(Mutex::new((0..num_jobs).collect::<Vec<_>>()));
let completed = Arc::new(Mutex::new(0));

let mut handles = Vec::new();

for id in 0..num_workers {
    let job_queue = job_queue.clone();
    let completed = completed.clone();
    let handle = thread::spawn(move || {
        let worker = Worker { id };
        loop {
            let job = {
                let mut queue = job_queue.lock().unwrap();
                if queue.is_empty() {
                    None
                } else {
                    Some(queue.pop().unwrap())
                }
            };
            match job {
                Some(j) => worker.process_job(j),
                None => break,
            }
        }
        *completed.lock().unwrap() += 1;
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("All workers completed");
```

## 死锁避免

```rust
// 错误：可能导致死锁
// let mut m1 = mutex1.lock().unwrap();
// let mut m2 = mutex2.lock().unwrap();

// 正确：始终按相同顺序获取锁
use std::sync::Mutex;

fn lock_both(a: &Mutex<i32>, b: &Mutex<i32>) -> (i32, i32) {
    let _a = a.lock().unwrap();
    let _b = b.lock().unwrap();
    (*_a, *_b)
}

// 或者使用 std::sync::mpsc::Receiver
```

## 资源索引

- 并发：https://doc.rust-lang.org/book/ch16-00-concurrency.html
- Send/Sync：https://doc.rust-lang.org/nomicon/send-and-sync.html
- Mutex：https://doc.rust-lang.org/std/sync/struct.Mutex.html
- Arc：https://doc.rust-lang.org/std/sync/struct.Arc.html

## 注意事项

- 使用 Arc<Mutex<T>> 进行多线程共享可变状态
- Rc 不是线程安全的，使用 Arc
- RefCell 不是线程安全的，使用 Mutex/RwLock
- 避免死锁：始终按相同顺序获取多个锁
- 使用原子类型代替锁来提高性能
- 理解 Send/Sync 是编写安全并发代码的基础
