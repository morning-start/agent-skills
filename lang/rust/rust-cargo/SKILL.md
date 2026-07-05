---
name: rust-cargo
version: 1.0.0
author: book-skills
description: Rust Cargo 包管理技能，掌握项目创建、依赖管理、工作区、构建配置、发布到 crates.io
tags: [rust, cargo, workspace, build, publish]
layer: Layer 2 - Design Choices
trigger: cargo, workspace, dependency, feature flags, publish
---

# Rust Cargo 包管理

## 任务目标

- 本 Skill 用于：使用 Cargo 管理 Rust 项目的依赖、构建和发布
- 能力包含：项目创建、依赖管理、工作区、构建配置、发布、cargo 子命令
- 触发条件：创建新项目、添加依赖、配置构建、管理多包工作区

## 前置准备

- 安装 Rust 工具链：`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
- 验证安装：`cargo --version`

## 项目创建

### cargo new

```bash
# 创建二进制项目
cargo new my-project
cd my-project

# 创建库项目
cargo new --lib my-library

# 使用 vcs 指定版本控制系统
cargo new --vcs git my-project
```

### 项目结构

```
my-project/
├── Cargo.toml      # 清单文件
├── src/
│   └── main.rs     # 主程序入口
└── Cargo.lock      # 依赖锁定文件（自动生成）
```

### 库项目结构

```
my-library/
├── Cargo.toml
└── src/
    └── lib.rs      # 库入口
```

## Cargo.toml 清单文件

### 基本配置

```toml
[package]
name = "my-project"
version = "0.1.0"
edition = "2021"      # Rust 版本
authors = ["Name <email@example.com>"]
description = "A short description"
license = "MIT OR Apache-2.0"
repository = "https://github.com/user/my-project"
documentation = "https://docs.rs/my-project"
homepage = "https://my-project.example.com"
readme = "README.md"
keywords = ["example", "tutorial"]
categories = ["command-line-utilities"]

[dependencies]
```

### edition 版本

| Edition | 说明 |
|---------|------|
| 2015 | 原始版本 |
| 2018 | 异步支持、模块系统改进 |
| 2021 | 最新版本，推荐使用 |

## 依赖管理

### 添加依赖

```bash
# 添加最新版本
cargo add serde

# 添加指定版本
cargo add serde@1.0

# 添加多个
cargo add serde@1.0 serde_json@1.0
```

### 依赖版本规范

```toml
[dependencies]
# 精确版本
crate = "1.2.3"

# 范围版本
crate = "1.0"
crate = ">=1.0"
crate = ">1.0,<2.0"

# 通配符
crate = "1.0.*"

# 使用版本标记
crate = "=1.2.3"  # 精确匹配

# git 依赖
crate = { git = "https://github.com/example/crate" }
crate = { git = "https://github.com/example/crate", branch = "next" }
crate = { git = "https://github.com/example/crate", tag = "v1.0.0" }

# 路径依赖
crate = { path = "../my-other-crate" }
```

### 依赖特性

```toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["full"] }

# 可选依赖
optional-crate = { version = "1.0", optional = true }

[features]
default = ["optional-crate"]
custom_feature = []
```

### Cargo.lock

- 自动生成，不要手动编辑
- 提交到版本控制
- 保证可重现构建

```bash
# 更新依赖
cargo update

# 更新特定依赖
cargo update -p serde

# 升级到新版本
cargo update -p serde --precise 1.0.100
```

## 构建命令

### 基本构建

```bash
# Debug 构建
cargo build

# Release 构建
cargo build --release

# 指定包构建
cargo build --package my-package

# 构建并运行
cargo run

# 带参数运行
cargo run -- arg1 arg2

# 指定示例
cargo run --example my-example
```

### 检查和诊断

```bash
# 类型检查（快速）
cargo check

# 格式化检查
cargo fmt --check

# 代码检查
cargo clippy

# 警告即错误
cargo build -- -D warnings
```

### 构建输出

```bash
# 紧凑输出
cargo build --quiet

# 详细输出
cargo build -v

# 显示 timings
cargo build --timings
```

## 测试

### 运行测试

```bash
# 运行所有测试
cargo test

# 运行特定测试
cargo test my_test

# 运行集成测试
cargo test --test integration

# 显示测试输出
cargo test -- --nocapture

# 运行文档测试
cargo test --doc

# 运行带指定特征的测试
cargo test --features "feature1,feature2"
```

### 测试配置

```toml
[dev-dependencies]
mockall = "0.11"

[[test]]
name = "integration"
path = "tests/integration.rs"
```

## 文档

### 生成文档

```bash
# 生成文档
cargo doc

# 生成并打开
cargo doc --open

# 不包含私有项
cargo doc --no-deps

# 生成文档到指定目录
cargo doc --open --package my-package
```

## 安装和发布

### 安装二进制

```bash
# 从 crates.io 安装
cargo install ripgrep

# 从 git 安装
cargo install --git https://github.com/user/crate

# 卸载
cargo uninstall ripgrep

# 列出已安装
cargo install --list
```

### 发布到 crates.io

```bash
# 登录
cargo login <token>

# 检查包
cargo package --list

# 发布
cargo publish

# 发布到指定 registry
cargo publish --registry my-registry
```

## 工作区

### 工作区结构

```toml
# 根 Cargo.toml
[workspace]
members = [
    "crates/package-a",
    "crates/package-b",
]
resolver = "2"  # 推荐

# 或
[workspace]
members = ["crates/*"]
```

### 根包配置

```toml
[package]
name = "my-workspace"
version = "0.1.0"
edition = "2021"

# 不包含源代码
[[bin]]
name = "my-workspace"
path = "not-found"

# 实际二进制在 member 中
```

### member 配置

```toml
# crates/package-a/Cargo.toml
[package]
name = "package-a"
version = "0.1.0"
edition = "2021"

[dependencies]
package-b = { path = "../package-b" }
```

## 构建配置

### Profile 配置

```toml
[profile.dev]
opt-level = 0
debug = true

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true

[profile.dev.package.my-crate]
opt-level = 3
```

### 环境变量

| 变量 | 说明 |
|------|------|
| CARGO_HOME | Cargo 目录 |
| CARGO_TARGET_DIR | 目标目录 |
| RUSTUP_HOME | Rustup 目录 |
| RUSTFLAGS | 额外 Rustc 标志 |

### 构建脚本

```rust
// build.rs
fn main() {
    println!("cargo:rerun-if-changed=src/bindings.txt");
    println!("cargo:rustc-env=VERSION=1.0");
}
```

## Cargo 子命令

| 命令 | 说明 |
|------|------|
| cargo new | 创建项目 |
| cargo build | 构建 |
| cargo run | 运行 |
| cargo test | 测试 |
| cargo bench | 基准测试 |
| cargo doc | 文档 |
| cargo check | 检查 |
| cargo update | 更新依赖 |
| cargo clean | 清理 |
| cargo fmt | 格式化 |
| cargo clippy | 代码检查 |
| cargo tree | 显示依赖树 |
| cargo search | 搜索 crates.io |
| cargo publish | 发布 |
| cargo add | 添加依赖 |
| cargo remove | 移除依赖 |

## 常用操作

### 依赖树

```bash
# 显示依赖树
cargo tree

# 过滤依赖
cargo tree -p serde

# 反转依赖
cargo tree --invert
```

### 清理和重新构建

```bash
# 清理构建产物
cargo clean

# 清理并重新构建
cargo clean && cargo build

# 强制重新编译
cargo build --force
```

## .cargo/config.toml

```toml
[build]
target-dir = "target"

[target.x86_64-pc-windows-gnu]
linker = "x86_64-w64-mingw32-gcc"

[alias]
b = "build"
t = "test"
r = "run"
c = "check"
```

## 资源索引

- Cargo 文档：https://doc.rust-lang.org/cargo/index.html
- crates.io：https://crates.io/
- crates.io API：https://crates.io/api

## 注意事项

- 使用 `cargo new` 创建项目而非手动创建目录
- 始终提交 Cargo.lock 到版本控制
- 使用 `cargo add` 管理依赖而非手动编辑
- 优先使用发布版本而非 git 依赖
- release 构建使用 `--release` 标志
- 使用 `cargo clippy` 捕获常见错误
