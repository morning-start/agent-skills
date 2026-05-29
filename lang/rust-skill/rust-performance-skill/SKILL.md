---
name: rust-performance-skill
description: Rust Layer 2 技能 - 性能优化，核心问题：瓶颈在哪里？掌握 benchmark、profiling、热点分析等性能调优方法
version: 1.0.0
layer: 2
trigger: benchmark, profiling, performance, speed, optimize, flamegraph, cargo bench
---

# Rust Performance - Layer 2

## 核心问题

瓶颈在哪里？

## 元认知追溯

```
问题 → Layer 2: 性能分析
        ↓
识别热点 → Layer 1: 语言机制优化
        ↓
架构决策 → Layer 3: 领域需求权衡
```

## 性能测量

### Criterion - 基准测试

```rust
// Cargo.toml
[dev-dependencies]
criterion = { version = "0.5", features = ["html_reports"] }

[[bench]]
name = "my_benchmark"
harness = false
```

```rust
// benches/my_benchmark.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("fibonacci_20", |b| {
        b.iter(|| fibonacci(black_box(20)))
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
```

### Iai - 静态分析

```rust
// benches/my_benchmark.rs
use iai::black_box;

fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

iai::main!(func1, func2);
```

## Profiling 工具

### perf (Linux)

```bash
# 编译带调试信息
RUSTFLAGS="-g" cargo build --release

# 运行并记录
perf record -g -- ./target/release/my_app

# 生成火焰图
perf script | stackcollapse-perf.pl | flamegraph.pl > flamegraph.svg
```

### cargo-flamegraph

```bash
# 安装
cargo install flamegraph

# 生成火焰图
cargo flamegraph --bin my_app
```

### CPU 计数器

```bash
# Linux
perf stat -e cycles,instructions,cache-misses ./target/release/my_app

# macOS
 Instruments.app (Instruments → Time Profiler)
```

## 常见优化模式

### 避免不必要的克隆

```rust
// 优化前
fn process(data: Vec<u8>) -> usize {
    let data_clone = data.clone();
    do_work(&data_clone).len()
}

// 优化后
fn process(data: &Vec<u8>) -> usize {
    do_work(data).len()
}
```

### 使用合适的集合类型

```rust
// 小数据用栈
let arr: [i32; 3] = [1, 2, 3];

// 大数据用堆
let vec = vec![1, 2, 3];

// 固定大小用数组
let arr = [0u8; 1024];
```

### 减少动态分发

```rust
// 动态分发
fn process(items: &[&dyn Serializable]) { }

// 泛型静态分发
fn process<T: Serializable>(items: &[T]) { }
```

## 性能技巧

### 预分配容量

```rust
// 预分配减少重新分配
let mut vec = Vec::with_capacity(1000);
for i in 0..1000 {
    vec.push(i);
}
```

### 缓存友好访问

```rust
// 缓存行大小约 64 字节
struct Row {
    a: u64,
    b: u64,
    c: u64,
    d: u64,
}

// 访问模式影响缓存命中率
```

### 并行化

```rust
use rayon::prelude::*;

let result: Vec<u64> = (0..1000)
    .into_par_iter()
    .map(|x| expensive_computation(x))
    .collect();
```

## 资源索引

- [Criterion](https://bheisner.github.io/criterion.rs/)
- [cargo-flamegraph](https://github.com/flamegraph-rs/flamegraph)
- [perf-tools](https://github.com/brendangregg/perf-tools)

## 注意事项

- 先测量再优化，避免过早优化
- 用 benchmark 验证优化效果
- 权衡性能与可读性
