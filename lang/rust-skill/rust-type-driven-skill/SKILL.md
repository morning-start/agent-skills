---
name: rust-type-driven-skill
description: Rust Layer 1 技能 - 类型驱动设计，核心问题：如何用类型系统防止无效状态？掌握 newtype、PhantomData、类型状态模式
version: 1.0.0
layer: 1
trigger: newtype, PhantomData, type state, marker type, branding, self-referential
---

# Rust Type-Driven Design - Layer 1

## 核心问题

如何用类型系统防止无效状态？

## 元认知追溯

```
问题 → Layer 1: 类型语法
        ↓
类型如何编码业务规则 → Layer 2: 设计模式
        ↓
防止领域错误状态 → Layer 3: 领域约束
```

## 类型状态模式

### 防止无效值

```rust
// 普通类型
struct UserId(u64);

// 使用类型区分
struct Meters(f64);
struct Seconds(f64);

fn speed(d: Meters, t: Seconds) -> f64 {
    d.0 / t.0
}

let d = Meters(100.0);
let t = Seconds(10.0);
let s = speed(d, t);

// speed(Meters(100), Seconds(10)) // 编译错误
```

### 标记类型

```rust
// 标记类型
trait Marker {}
struct DebugOnly {}
struct ReleaseOnly {}

struct Config<M: Marker> {
    value: String,
    _marker: std::marker::PhantomData<M>,
}

impl Config<DebugOnly> {
    fn new(value: &str) -> Self {
        Config {
            value: value.to_string(),
            _marker: Default::default(),
        }
    }
}

// 不同配置类型
type DebugConfig = Config<DebugOnly>;
type ReleaseConfig = Config<ReleaseOnly>;
```

### Phase Type

```rust
// 编译阶段标记
struct BeforeInit;
struct AfterInit;

struct State<Phase> {
    data: Vec<u8>,
    _phase: PhantomData<Phase>,
}

impl State<BeforeInit> {
    fn new() -> Self {
        State {
            data: Vec::new(),
            _phase: PhantomData,
        }
    }

    fn init(self) -> State<AfterInit> {
        State {
            data: self.data,
            _phase: PhantomData,
        }
    }
}

impl State<AfterInit> {
    fn process(&self) {
        // 安全访问
        println!("{:?}", self.data);
    }
}

// let state = State::<BeforeInit>::new();
// state.process(); // 编译错误：未初始化不能处理
```

## Newtype 模式

```rust
// 防止类型混淆
struct Meters(f64);
struct Feet(f64);

struct UserId(u64);
struct SessionId(u64);

// 编译时类型安全
fn UserId::from_str(s: &str) -> Option<UserId> {
    s.parse().ok().map(UserId)
}
```

## PhantomData

```rust
use std::marker::PhantomData;

// 拥有泛型但不使用
struct Cache<K, V> {
    data: HashMap<K, V>,
    _key: PhantomData<K>,
    _value: PhantomData<V>,
}

// Send + Sync 约束
struct AsyncFn<F, T> {
    f: F,
    _marker: PhantomData<T>,
}

unsafe impl<F: Send, T: Send> Send for AsyncFn<F, T> {}
unsafe impl<F: Sync, T: Sync> Sync for AsyncFn<F, T> {}
```

## 常用模式

### 非空向量

```rust
struct NonEmptyVec<T> {
    first: T,
    rest: Vec<T>,
}

impl<T> NonEmptyVec<T> {
    fn new(first: T) -> Self {
        NonEmptyVec {
            first,
            rest: Vec::new(),
        }
    }

    fn push(&mut self, elem: T) {
        self.rest.push(elem);
    }
}
```

### 验证字符串

```rust
struct Username(String);
struct Password(String);

trait Validate {
    fn validate(s: &str) -> bool;
}

impl Validate for Username {
    fn validate(s: &str) -> bool {
        s.len() >= 3 && s.len() <= 20
    }
}

impl Validate for Password {
    fn validate(s: &str) -> bool {
        s.len() >= 8
    }
}
```

## 资源索引

- [类型状态模式](https://hoverbear.org/blog/rust-state-machines/)
- [PhantomData](https://doc.rust-lang.org/std/marker/struct.PhantomData.html)
- [Newtype Idiom](https://rust-unofficial.github.io/patterns/patterns/behavioural/newtype.html)

## 注意事项

- 让编译器捕获错误，而非运行时
- 类型是零成本的，不会增加运行时开销
- 过度使用类型标记可能增加复杂度
- 选择平衡点：安全性 vs 可读性
