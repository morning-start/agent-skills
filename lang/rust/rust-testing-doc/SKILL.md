---
name: rust-testing-doc
version: 1.0.0
author: book-skills
description: Rust 测试与文档技能，掌握单元测试、集成测试、文档测试、文档注释和 rustdoc 使用
tags: [rust, testing, doctest, mock, proptest]
layer: Layer 2 - Design Choices
trigger: testing, doctest, unit test, integration test, mock, proptest
---

# Rust 测试与文档

## 任务目标

- 本 Skill 用于：编写高质量测试和文档
- 能力包含：单元测试、集成测试、文档测试、测试组织、文档注释、rustdoc
- 触发条件：需要测试代码、生成 API 文档、编写示例代码

## 前置准备

- 完成 rust-core 和 rust-generics
- 理解 Rust 的测试框架

## 测试基础

### #[test] 属性

```rust
#[test]
fn basic_test() {
    assert_eq!(2 + 2, 4);
}

#[test]
fn test_with_result() -> Result<(), String> {
    if 2 + 2 == 4 {
        Ok(())
    } else {
        Err(String::from("Math failed"))
    }
}
```

### 断言宏

```rust
#[test]
fn test_assertions() {
    // 基本断言
    assert!(true);
    assert!(1 == 1);

    // 相等断言
    assert_eq!(2 + 2, 4);
    assert_ne!(2 + 2, 5);

    // 带自定义消息
    assert_eq!(result, 42, "Expected 42 but got {}", result);

    // debug 格式比较（用于实现了 PartialEq 的类型）
    // assert_eq!(a, b);  // 编译错误
    // assert_eq!(a, b, "a and b should be equal");
}
```

## 单元测试

### 在源文件中编写测试

```rust
// src/lib.rs 或 src/main.rs

pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 2), 4);
    }

    #[test]
    fn test_add_negative() {
        assert_eq!(add(-1, -1), -2);
    }
}
```

### 测试私有权

```rust
#[cfg(test)]
mod tests {
    // 不需要 use super::*; 可以直接访问父模块的私有项
    fn private_helper() {}

    #[test]
    fn test_with_private() {
        // 可以调用私有函数
        private_helper();
    }
}
```

## 集成测试

### 创建集成测试

```rust
// tests/integration.rs

#[test]
fn test_integration() {
    // 使用库
    use my_crate::add;

    assert_eq!(add(2, 2), 4);
}
```

### tests 目录结构

```
my-project/
├── src/
│   └── lib.rs
├── tests/
│   ├── integration.rs
│   └── other/
│       └── another_integration.rs
└── Cargo.toml
```

### 运行集成测试

```bash
cargo test --test integration
cargo test --tests
```

## 文档测试

### 文档注释

```rust
/// Adds two numbers together.
///
/// # Examples
///
/// ```
/// assert_eq!(add(2, 2), 4);
/// ```
///
/// # Panics
///
/// Panics if the inputs are invalid.
///
/// # Safety
///
/// This function is safe to call with any inputs.
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

### 运行文档测试

```bash
# 运行文档测试
cargo test --doc

# 运行特定包的文档测试
cargo test --doc --package my-package
```

### 文档测试中的隐藏代码

````rust
/// ```
/// # fn hidden() {
/// // This code will be hidden in the documentation
/// # }
/// assert_eq!(visible_code(), expected);
/// ```
fn visible_code() -> i32 {
    1
}
````

### 常见错误

```rust
/// ```
/// let result = broken();
/// assert_eq!(result, 42);
/// ```
pub fn broken() -> i32 {
    0  // 这个测试会失败
}
```

### 期望失败的测试

```rust
/// Should panic
///
/// ```
/// # //假装代码会 panic，但这不是真的
/// # panic!("intentional panic");
/// ```
///
/// 上面的 # 表示这行不会显示在文档中
```

## 模块化测试

### 测试模块组织

```rust
// src/lib.rs

// 模块
pub mod calculator;

#[cfg(test)]
mod tests {
    #[test]
    fn test_module_public_api() {
        // 测试公共 API
    }
}

// src/calculator.rs
pub fn add(a: i32, b: i32) -> i32 { a + b }

#[cfg(test)]
mod calculator_tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 2), 4);
    }
}
```

### 测试夹具

```rust
// tests/fixtures.rs
pub fn test_fixture() -> Vec<i32> {
    vec![1, 2, 3]
}

// tests/integration.rs
mod fixtures;

#[test]
fn test_with_fixture() {
    let data = fixtures::test_fixture();
    assert_eq!(data.len(), 3);
}
```

## 测试配置

### Cargo.toml 测试配置

```toml
[package]
name = "my-crate"

[dev-dependencies]
mockall = "0.11"
proptest = "1.0"

[[test]]
name = "integration"
path = "tests/integration.rs"

[[test]]
name = "doctest"
doctest = false  # 禁用文档测试
```

### 条件测试

```rust
#[test]
#[ignore]  // 忽略此测试
fn expensive_test() {
    // 运行时间很长的测试
}

#[test]
#[cfg(target_os = "linux")]  // 仅在 Linux 运行
fn linux_only_test() {
    // Linux 特定测试
}
```

## 测试运行选项

### 命令行选项

```bash
# 运行特定测试
cargo test test_name

# 运行多个测试（匹配模式）
cargo test test_prefix

# 忽略被忽略的测试
cargo test -- --ignored

# 运行所有测试包括 ignored
cargo test -- --include-ignored

# 显示测试输出
cargo test -- --nocapture

# 并行运行测试
cargo test -- --test-threads=4

# 顺序运行
cargo test -- --test-threads=1
```

### 过滤测试

```bash
# 运行模块中的测试
cargo test module_name

# 运行特定包的测试
cargo test --package my-package

# 运行特定 binary 的测试
cargo test --bin my-binary
```

## 测试组织原则

### 测试金字塔

```
       ┌─────────────┐
       │ Integration │
       │   Tests     │
       ├─────────────┤
       │ Unit Tests  │
       │ (in source) │
       ├─────────────┤
       │ Doc Tests   │
       └─────────────┘
```

### 测试驱动开发（TDD）

```rust
// 1. 写一个失败的测试
#[test]
fn test_add() {
    assert_eq!(add(1, 1), 2);
}

// 2. 运行测试看到失败
// cargo test

// 3. 写最小实现让测试通过
pub fn add(a: i32, b: i32) -> i32 {
    2
}

// 4. 重构让实现正确
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

## 常用测试宏

| 宏 | 说明 |
|----|------|
| assert!(expr) | 断言为真 |
| assert!(expr, msg) | 带消息的断言 |
| assert_eq!(a, b) | 断言相等 |
| assert_ne!(a, b) | 断言不相等 |
| debug_assert!(expr) | Debug 断言 |
| panic!(msg) | 触发 panic |
| try_test | Result 测试 |

## 文档注释

### 文档注释类型

```rust
/// 外文档：注释之后的项
//! 内文档：注释所在的项（用于 crate 根或模块）
```

### 文档注释示例

```rust
//! # My Crate
//!
//! This is my awesome crate for doing things.
//!
//! ## Usage
//!
//! ```rust
//! let result = my_crate::do_something();
//! ```

/// Calculates the square of a number.
///
/// ## Arguments
///
/// * `x` - The number to square
///
/// ## Returns
///
/// The square of the input number
///
/// ## Examples
///
/// ```
/// assert_eq!(square(3), 9);
/// ```
///
/// ## Panics
///
/// Does not panic.
pub fn square(x: i32) -> i32 {
    x * x
}
```

### Markdown 支持

```rust
/// # Heading 1
/// ## Heading 2
///
/// - bullet
/// - points
///
/// 1. numbered
/// 2. list
///
/// `inline code`
///
/// ```rust
/// let code = "block";
/// ```
///
/// [link](https://example.com)
///
/// ## See Also
///
/// * [Other Function](other_function)
/// * [Module](module)
```

## rustdoc

### 生成文档

```bash
# 生成文档
cargo doc

# 打开文档
cargo doc --open

# 不打开浏览器
cargo doc --no-deps

# 仅生成库文档
cargo doc --lib

# 指定包
cargo doc --package my-package
```

### rustdoc 选项

```bash
# 私有项也生成文档
cargo doc --document-private-items

# 移除缓存重新生成
cargo doc --force

# 输出到指定目录
rustdoc src/lib.rs -o ./docs
```

### HTML 输出

```bash
rustdoc src/lib.rs --crate-name my-crate
```

## 文档测试配置

### Cargo.toml

```toml
[package]
name = "my-crate"

[package.metadata.docs.rs]
all-features = true
rustdoc-args = ["--cfg", "docsrs"]

[profile.dev.package."*"]
opt-level = 0
```

## 资源索引

- 测试：https://doc.rust-lang.org/book/ch11-00-testing.html
- 文档：https://doc.rust-lang.org/book/ch14-02-publishing-to-crates-io.html
- rustdoc：https://doc.rust-lang.org/rustdoc/index.html
- 已知测试宏：https://doc.rust-lang.org/std/prelude/macro.assert_eq.html

## 注意事项

- 使用 `#[cfg(test)]` 只在测试时编译
- 集成测试在 tests/ 目录中
- 文档测试使用 `///` 或 `//!`
- `cargo test` 运行所有测试包括文档测试
- 使用 `cargo doc --open` 查看生成的文档
- 测试私有项不需要特殊导入
- 长期运行的测试使用 `#[ignore]`
