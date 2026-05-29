# rust-ml-skill

## 前言区

```
name: rust-ml-skill
version: v1.0.0
author: book-skills
description: 机器学习领域Rust应用技能，涵盖tch-rs、rustml、linfa等库的模型训练与部署
tags: [machine-learning, deep-learning, neural-networks, data-science, tch-rs]
trigger: /rust-ml
layer: Layer 3 - Domain Extensions
```

## 概述

本技能聚焦机器学习领域，展示Rust在ML场景下的高性能优势。涵盖深度学习、传统ML算法、模型部署与推理优化等核心场景。

## 任务目标

1. 使用tch-rs构建深度学习模型
2. 运用linfa进行传统机器学习
3. 实现模型量化与部署优化
4. 构建高性能推理服务

## 操作步骤

### 1. 深度学习 with tch-rs

tch-rs提供Rust绑定PyTorch的能力：

```rust
use tch::{nn, nn::Module, Device, Kind, Tensor};

pub struct SimpleNet {
    fc1: nn::Linear,
    fc2: nn::Linear,
}

impl SimpleNet {
    pub fn new(vs: &nn::Path) -> Self {
        SimpleNet {
            fc1: nn::linear(vs / "fc1", 784, 256, Default::default()),
            fc2: nn::linear(vs / "fc2", 256, 10, Default::default()),
        }
    }
}

impl Module for SimpleNet {
    fn forward(&self, xs: &Tensor) -> Tensor {
        xs.view([-1, 784])
            .apply(&self.fc1)
            .relu()
            .apply(&self.fc2)
    }
}

pub fn train_epoch(
    net: &mut SimpleNet,
    vs: &nn::Path,
    data: &Tensor,
    labels: &Tensor,
    optimizer: &mut nn::Optimizer,
) -> f64 {
    let logits = net.forward(&data);
    let loss = logits.cross_entropy_for_logits(&labels);
    optimizer.backward_step(&loss);
    loss.double_value(&[])
}
```

### 2. 传统机器学习 with linfa

linfa提供统一的ML算法接口：

```rust
use linfa::prelude::*;
use linfa_linear::LinearRegression;
use ndarray::Array2;

pub fn train_linear_model(
    features: Array2<f64>,
    targets: Array2<f64>,
) -> Result<LinearRegression, LinfaError> {
    let dataset = Dataset::new(features, targets);
    let (train, _) = dataset.split(0.8);

    let model = LinearRegression::new();
    let fitted = model.fit(&train)?;
    Ok(fitted)
}

pub fn predict(model: &LinearRegression, features: Array2<f64>) -> Array2<f64> {
    model.predict(&features)
}
```

### 3. 模型量化

```rust
use tract_onnx::prelude::*;

pub fn load_quantized_model(path: &str) -> TractResult<Runnable> {
    let model = std::fs::read(path)?;
    let proto = tract_onnx::parse_onnx(&model)?;

    let model = proto
        .with_input_fact(0, f32::fact(&[1, 3, 224, 224]).into())?
        .into_optimized()?
        .into_runnable()?;

    Ok(model)
}

pub fn run_inference(
    model: &Runnable,
    input_data: Tensor,
) -> TractResult<Vec<f32>> {
    let result = model.run(vec![input_data.into()])?;
    Ok(result[0].to_vec::<f32>().unwrap())
}
```

### 4. 特征工程

```rust
use ndarray::{Array, Array1, Axis};
use ndarray_stats::QuantileExt;

pub struct FeatureScaler {
    mean: Array1<f64>,
    std: Array1<f64>,
}

impl FeatureScaler {
    pub fn fit(data: &Array2<f64>) -> Self {
        let mean = data.mean_axis(Axis(0)).unwrap();
        let std = data.std_axis(Axis(0), 1.0);
        FeatureScaler { mean, std }
    }

    pub fn transform(&self, data: &Array2<f64>) -> Array2<f64> {
        (data - &self.mean) / &self.std
    }

    pub fn fit_transform(&mut self, data: &Array2<f64>) -> Array2<f64> {
        let transformed = self.transform(data);
        self.mean = data.mean_axis(Axis(0)).unwrap();
        self.std = data.std_axis(Axis(0), 1.0);
        transformed
    }
}
```

## 资源索引

### 核心库

| 库 | 用途 | 链接 |
|---|------|------|
| tch-rs | PyTorch Rust绑定 | https://github.com/LaurentMazare/tch-rs |
| linfa | 传统ML算法框架 | https://github.com/rust-ml/linfa |
| tract | ONNX模型推理 | https://github.com/sonos/tract |
| rustml | ML工具库 | https://github.com/mwitkow/rustml |

### 关键依赖

```toml
[dependencies]
tch = "0.12"
linfa = "0.7"
ndarray = "0.16"
ndarray-stats = "0.5"
tract-onnx = "0.21"
```

## 注意事项

1. **内存管理**：大数据集训练需注意内存分配，避免泄漏
2. **数值稳定性**：除法操作需检查分母是否接近零
3. **并行计算**：使用rayon进行数据并行处理
4. **模型序列化**：生产环境必须使用安全的序列化格式
