---
name: rust-domain-error-skill
description: Rust Layer 2 技能 - 领域错误处理，核心问题：谁来处理这个错误？掌握 retry、circuit breaker、错误传播等模式
version: 1.0.0
layer: 2
trigger: retry, circuit breaker, error handling, fault tolerance, backoff
---

# Rust Domain Error - Layer 2

## 核心问题

谁来处理这个错误？

## 元认知追溯

```
问题 → Layer 2: 错误处理模式
        ↓
重试策略 → Layer 3: 领域需求
        ↓
Rust Result 类型 → Layer 1: 语言机制
```

## 错误处理模式

### Retry - 重试机制

```rust
use std::time::Duration;

// 简单重试
async fn fetch_with_retry<F, Fut, T>(
    mut f: F,
    max_retries: u32,
) -> Result<T, Error>
where
    F: FnMut() -> Fut,
    Fut: std::future::Future<Output = Result<T, Error>>,
{
    let mut attempts = 0;
    loop {
        match f().await {
            Ok(v) => return Ok(v),
            Err(e) if attempts < max_retries => {
                attempts += 1;
                backoff(attempts).await;
            }
            Err(e) => return Err(e),
        }
    }
}

// 指数退避
async fn backoff(attempts: u32) {
    let delay = Duration::from_millis(100 * 2_u64.pow(attempts));
    tokio::time::sleep(delay).await;
}
```

### Circuit Breaker - 熔断器

```rust
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;

struct CircuitBreaker {
    failures: AtomicU64,
    threshold: u64,
    state: std::sync::Mutex<CircuitState>,
}

#[derive(Debug, Clone, Copy)]
enum CircuitState {
    Closed,
    Open,
    HalfOpen,
}

impl CircuitBreaker {
    fn new(threshold: u64) -> Self {
        CircuitBreaker {
            failures: AtomicU64::new(0),
            threshold,
            state: std::sync::Mutex::new(CircuitState::Closed),
        }
    }

    fn record_failure(&self) {
        let failures = self.failures.fetch_add(1, Ordering::SeqCst);
        if failures >= self.threshold {
            let mut state = self.state.lock().unwrap();
            *state = CircuitState::Open;
        }
    }

    fn is_available(&self) -> bool {
        let state = self.state.lock().unwrap();
        matches!(*state, CircuitState::Closed | CircuitState::HalfOpen)
    }
}
```

### Error 转换

```rust
use std::fmt;

// 领域错误
#[derive(Debug)]
enum DomainError {
    NotFound(String),
    ValidationError(String),
    Unauthorized,
}

impl fmt::Display for DomainError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            DomainError::NotFound(id) => write!(f, "Not found: {}", id),
            DomainError::ValidationError(msg) => write!(f, "Validation: {}", msg),
            DomainError::Unauthorized => write!(f, "Unauthorized"),
        }
    }
}

impl std::error::Error for DomainError {}

// 转换 trait
impl From<DatabaseError> for DomainError {
    fn from(err: DatabaseError) -> Self {
        DomainError::ValidationError(err.to_string())
    }
}
```

## 错误传播

```rust
// 使用 ? 运算符传播
async fn process_order(order_id: OrderId) -> Result<Order, DomainError> {
    let order = db::find_order(order_id)
        .await
        .map_err(|e| DomainError::NotFound(order_id.to_string()))?;

    validate_order(&order)?; // ? 自动转换

    save_order(order).await?;
    Ok(order)
}
```

## thiserror - 简化错误定义

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum OrderError {
    #[error("order not found: {0}")]
    NotFound(String),

    #[error("invalid order status: {status}")]
    InvalidStatus { status: String, expected: String },

    #[error("payment failed: {0}")]
    PaymentFailed(#[from] PaymentError),
}
```

## 与其他技能关联

- rust-error-handling-skill: 基础错误类型
- rust-async-skill: 异步错误处理
- rust-concurrency-skill: 多线程错误处理

## 资源索引

- [thiserror](https://github.com/dtolnay/thiserror)
- [anyhow](https://github.com/dtolnay/anyhow)
- [retry](https://crates.io/crates/retry)

## 注意事项

- 区分可恢复错误和不可恢复错误
- 选择合适的错误粒度
- 考虑错误日志和监控
