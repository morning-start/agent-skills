---
name: rust-lifecycle-skill
description: Rust Layer 2 技能 - 生命周期管理，核心问题：何时创建、使用、清理？掌握 RAII、Drop、延迟初始化等资源管理模式
version: 1.0.0
layer: 2
trigger: RAII, Drop, lifetime, lazy, initialization, cleanup, resource management
---

# Rust Lifecycle - Layer 2

## 核心问题

何时创建、使用、清理？

## 元认知追溯

```
问题 → Layer 2: 生命周期模式
        ↓
资源获取即初始化 → Layer 1: 所有权
        ↓
确定性清理 vs 垃圾回收 → Layer 3: 领域需求
```

## RAII - 资源获取即初始化

```rust
// 文件句柄 - 自动关闭
struct File {
    handle: std::fs::File,
}

impl Drop for File {
    fn drop(&mut self) {
        // 析构时自动关闭
        println!("File closed");
    }
}

// 使用
{
    let file = File { handle: std::fs::File::open("data.txt")? };
    // 使用文件...
} // 文件自动关闭
```

## Drop Trait

```rust
struct CustomResource {
    id: u64,
}

impl Drop for CustomResource {
    fn drop(&mut self) {
        // 清理资源
        println!("Cleaning up resource {}", self.id);
    }
}

// 手动 drop
drop(resource); // 立即释放
```

## 延迟初始化

### 懒加载

```rust
use std::cell::LazyCell;

static CONFIG: LazyCell<Config> = LazyCell::new(|| {
    Config::load()
});

// 首次访问时才初始化
println!("{:?}", *CONFIG);
```

### OnceCell

```rust
use std::sync::OnceLock;

static mut DATA: OnceLock<Vec<u8>> = OnceLock::new();

// 线程安全单例
fn get_data() -> &'static Vec<u8> {
    unsafe {
        DATA.get_or_init(|| {
            vec![1, 2, 3]
        })
    }
}
```

### Builder 模式

```rust
struct QueryBuilder {
    table: String,
    conditions: Vec<String>,
    limit: Option<usize>,
}

impl QueryBuilder {
    fn new(table: &str) -> Self {
        QueryBuilder {
            table: table.to_string(),
            conditions: Vec::new(),
            limit: None,
        }
    }

    fn where_clause(mut self, cond: &str) -> Self {
        self.conditions.push(cond.to_string());
        self
    }

    fn limit(mut self, n: usize) -> Self {
        self.limit = Some(n);
        self
    }

    fn build(self) -> String {
        // 构建最终查询
        todo!()
    }
}

let query = QueryBuilder::new("users")
    .where_clause("active = true")
    .limit(10)
    .build();
```

## 生命周期标注

### 引用参数

```rust
// 生命周期 'a 表示参数和返回值的存活时间
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

### 结构体生命周期

```rust
// 结构体持有引用时需要标注
struct Excerpt<'a> {
    part: &'a str,
}

impl<'a> Excerpt<'a> {
    fn new(paragraph: &'a str) -> Self {
        Excerpt { part: paragraph }
    }
}
```

## 常见模式

### 有界生命周期

```rust
// 限制返回值的生命周期
fn first_word<'a>(s: &'a str) -> &'a str {
    s.split_whitespace().next().unwrap_or("")
}
```

### 静态生命周期

```rust
// 编译期常量
static APP_NAME: &str = "MyApp";
static VERSION: &str = "1.0.0";

// String 字面量实现
const APP_INFO: &str = concat!(env!("CARGO_PKG_NAME"), " v", env!("CARGO_PKG_VERSION"));
```

## 与其他技能关联

- rust-ownership-skill: 生命周期与所有权
- rust-resource-management-skill: RAII 资源模式
- rust-error-handling-skill: 构造失败处理

## 资源索引

- [Drop Trait](https://doc.rust-lang.org/std/ops/trait.Drop.html)
- [LazyCell](https://doc.rust-lang.org/std/cell/struct.LazyCell.html)
- [Lifetime 语法](https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html)

## 注意事项

- 优先使用 RAII 自动清理资源
- 生命周期标注是编译时检查，无运行时开销
- 延迟初始化避免不必要的计算
- 避免生命周期逃逸到运行时
