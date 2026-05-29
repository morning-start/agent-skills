# rust-fintech-skill

## 前言区

```
name: rust-fintech-skill
version: v1.0.0
author: book-skills
description: 金融科技领域Rust应用技能，涵盖安全计算、高性能交易系统、量化分析与风险管理
tags: [fintech, trading, quantitative-analysis, risk-management, high-performance]
trigger: /rust-fintech
layer: Layer 3 - Domain Extensions
```

## 概述

本技能聚焦金融科技领域，展示Rust在高性能、安全敏感场景下的应用优势。涵盖量化交易系统、风险管理平台、支付网关等核心场景。

## 任务目标

1. 构建高性能量化交易系统
2. 实现安全可靠的支付网关
3. 开发实时风险管理平台
4. 运用Rust安全计算特性保护敏感数据

## 操作步骤

### 1. 高性能交易系统

Rust在交易系统中的核心优势：
- 微秒级延迟（相比Python/JVM有10-100x优势）
- 内存安全保证（避免交易事故）
- 并行计算支持（多策略同时运行）

```rust
use std::sync::Arc;
use tokio::sync::RwLock;

pub struct OrderBook {
    bids: Arc<RwLock<Vec<Order>>>,
    asks: Arc<RwLock<Vec<Order>>>,
}

#[derive(Clone)]
pub struct Order {
    pub price: f64,
    pub quantity: f64,
    pub side: OrderSide,
    pub timestamp: u64,
}

pub fn calculate_spread(book: &OrderBook) -> f64 {
    let best_bid = book.bids.read().unwrap().first()
        .map(|o| o.price).unwrap_or(0.0);
    let best_ask = book.asks.read().unwrap().first()
        .map(|o| o.price).unwrap_or(f64::MAX);
    best_ask - best_bid
}
```

### 2. 安全计算与数据保护

Rust的类型系统确保敏感数据处理安全：

```rust
use subtle::{Choice, ConstantTimeEq};

pub struct SecretKey([u8; 32]);

impl SecretKey {
    pub fn new(key: [u8; 32]) -> Self {
        SecretKey(key)
    }

    pub fn compare(&self, other: &SecretKey) -> Choice {
        self.0.ct_eq(&other.0)
    }
}

pub struct EncryptedData {
    ciphertext: Vec<u8>,
    nonce: [u8; 12],
}

impl EncryptedData {
    pub fn encrypt(plaintext: &[u8], key: &SecretKey) -> Self {
        use chacha20poly1305::{
            ChaCha20Poly1305, Nonce,
            aead::{Aead, KeyInit}
        };
        let cipher = ChaCha20Poly1305::new(key.0.as_slice().into());
        let nonce = Nonce::from_slice(b"unique nonce");
        let ciphertext = cipher.encrypt(nonce, plaintext)
            .expect("encryption failed");
        EncryptedData {
            ciphertext,
            nonce: *b"unique nonce",
        }
    }
}
```

### 3. 量化分析核心库

```rust
use std::collections::VecDeque;

pub struct TimeSeries {
    data: VecDeque<f64>,
    window: usize,
}

impl TimeSeries {
    pub fn new(window: usize) -> Self {
        TimeSeries {
            data: VecDeque::with_capacity(window),
            window,
        }
    }

    pub fn push(&mut self, value: f64) {
        if self.data.len() >= self.window {
            self.data.pop_front();
        }
        self.data.push_back(value);
    }

    pub fn sma(&self) -> Option<f64> {
        if self.data.is_empty() {
            return None;
        }
        Some(self.data.iter().sum::<f64>() / self.data.len() as f64)
    }

    pub fn volatility(&self) -> Option<f64> {
        let mean = self.sma()?;
        let variance = self.data.iter()
            .map(|x| (x - mean).powi(2))
            .sum::<f64>() / self.data.len() as f64;
        Some(variance.sqrt())
    }
}
```

### 4. 风险管理框架

```rust
pub struct RiskMetrics {
    pub var_95: f64,
    pub cvar_95: f64,
    pub max_drawdown: f64,
}

pub fn calculate_var(returns: &[f64], confidence: f64) -> f64 {
    let sorted = {
        let mut s = returns.to_vec();
        s.sort_by(|a, b| a.partial_cmp(b).unwrap());
        s
    };
    let index = ((1.0 - confidence) * returns.len() as f64) as usize;
    sorted[index]
}

pub fn validate_position(
    position_value: f64,
    account_equity: f64,
    max_position_pct: f64,
) -> Result<(), RiskError> {
    let position_ratio = position_value / account_equity;
    if position_ratio > max_position_pct {
        return Err(RiskError::PositionLimitExceeded {
            requested: position_ratio,
            limit: max_position_pct,
        });
    }
    Ok(())
}
```

## 资源索引

### 核心库

| 库 | 用途 | 链接 |
|---|------|------|
| rust_decimal | 精确小数计算 | https://docs.rs/rust_decimal |
| orderbook-aggregator | 订单簿聚合 | https://github.com/yourgithub/orderbook |
| ta | 技术分析 | https://docs.rs/ta |

### 关键依赖

```toml
[dependencies]
tokio = { version = "1.35", features = ["full"] }
rust_decimal = "1.33"
chacha20poly1305 = "0.10"
subtle = "2.5"
ta = "0.6"
```

## 注意事项

1. **精度处理**：金融计算必须使用rust_decimal避免浮点误差
2. **并发安全**：交易系统多线程访问需使用Arc<RwLock<>>
3. **错误处理**：交易操作失败必须传播错误，不可panic
4. **审计日志**：所有关键操作需记录不可篡改的日志
