---
name: rust-iot
version: 1.0.0
author: book-skills
description: 物联网领域Rust应用技能，涵盖嵌入式开发、实时系统、传感器通信与边缘计算
tags: [iot, embedded, real-time, sensors, edge-computing, no_std]
trigger: /rust-iot
layer: Layer 3 - Domain Extensions
---

# Rust 物联网开发

## 概述

本技能聚焦物联网领域，展示Rust在嵌入式、实时系统、边缘计算等场景下的优势。涵盖传感器通信、设备管理、边缘推理等核心场景。

## 任务目标

1. 构建嵌入式设备固件
2. 实现传感器驱动与通信
3. 开发边缘计算应用
4. 设计低功耗物联网设备

## 操作步骤

### 1. 嵌入式基础 (no_std)

```rust
#![no_std]
#![no_main]

use cortex_m_rt::entry;

#[entry]
fn main() -> ! {
    let peripherals = stm32f4::Peripherals::take().unwrap();
    let gpioa = peripherals.GPIOA;
    gpioa.odr.modify(|_, w| w.odr0().set_bit());
    loop {
        cortex_m::asm::wfi();
    }
}
```

### 2. 传感器驱动

```rust
use embedded_hal::i2c::I2c;

pub struct BME280<I2C> {
    i2c: I2C,
    address: u8,
}

impl<I2C, E> BME280<I2C>
where
    I2C: I2c<Error = E>,
{
    pub fn new(i2c: I2C) -> Self {
        BME280 {
            i2c,
            address: 0x76,
        }
    }

    pub fn read_temperature(&mut self) -> Result<f32, E> {
        let cmd = [0xFA];
        let mut buf = [0u8; 3];
        self.i2c.write_read(self.address, &cmd, &mut buf)?;
        let raw = (u16::from(buf[0]) << 8) | u16::from(buf[1]);
        let temp = raw as f32 / 5120.0 * 100.0;
        Ok(temp)
    }
}
```

### 3. MQTT客户端

```rust
use rumqttc::{AsyncClient, MqttOptions, QoS};

pub struct IoTDevice {
    client: AsyncClient,
    device_id: String,
}

impl IoTDevice {
    pub fn new(broker: &str, device_id: &str) -> Self {
        let mut options = MqttOptions::new(device_id, broker, 1883);
        options.set_keep_alive(60);

        let client = AsyncClient::new(options, 100);
        IoTDevice {
            client,
            device_id: device_id.to_string(),
        }
    }

    pub async fn publish(&self, topic: &str, payload: &[u8]) -> Result<(), rumqttc::Error> {
        self.client
            .publish(topic, QoS::AtLeastOnce, false, payload)
            .await
    }

    pub async fn subscribe(&self, topic: &str) -> Result<(), rumqttc::Error> {
        self.client.subscribe(topic, QoS::AtLeastOnce).await
    }
}
```

### 4. 边缘推理

```rust
use tract_onnx::prelude::*;

pub struct EdgeInference {
    model: SimpleTypedModel,
    input_shape: TensorShape,
}

impl EdgeInference {
    pub fn load_model(path: &str) -> TractResult<Self> {
        let model = std::fs::read(path)?;
        let proto = tract_onnx::parse_onnx(&model)?;
        let model = proto
            .with_input_fact(0, f32::fact(&[1, 3, 64, 64]).into())?
            .into_optimized()?
            .into_typed()?;

        Ok(EdgeInference {
            model,
            input_shape: tvec!(TensorFact::from(f32::fact(&[1, 3, 64, 64]))),
        })
    }

    pub fn infer(&self, input: &[f32]) -> TractResult<Vec<f32>> {
        let tensor = Tensor::from(input).into_shape(&[1, 3, 64, 64])?;
        let result = self.model.run(vec![tensor.into()])?;
        Ok(result[0].to_vec::<f32>()?)
    }
}
```

### 5. 低功耗设计

```rust
use embedded_hal::digital::v2::OutputPin;

pub struct PowerManager {
    wake_interval_secs: u32,
}

impl PowerManager {
    pub fn new(wake_interval_secs: u32) -> Self {
        PowerManager { wake_interval_secs }
    }

    pub fn enter_deep_sleep(&self) {
        #[cfg(target_arch = "arm")]
        {
            let scb = cortex_m::Peripherals::take().unwrap().SCB;
            unsafe {
                scb.sleep modeset();
            }
        }
    }

    pub fn schedule_wake(&self) {
        let ticks = self.wake_interval_secs * 32768;
        set_timer(ticks);
        enable_irq();
    }
}
```

## 资源索引

### 核心库

| 库 | 用途 | 链接 |
|---|------|------|
| embedded-hal | 嵌入式抽象 | https://github.com/rust-embedded/embedded-hal |
| esp-idf-sys | ESP32支持 | https://github.com/esp-rs/esp-idf-sys |
| cortex-m | ARM Cortex-M | https://github.com/rust-embedded/cortex-m |
| rumqttc | MQTT客户端 | https://github.com/bytebeamio/rumqttc |

### 关键依赖

```toml
[dependencies]
embedded-hal = "0.2"
cortex-m = "0.7"
cortex-m-rt = "0.7"
rumqttc = "0.21"
tract-onnx = "0.21"
esp-idf-sys = "0.33"
```

## 注意事项

1. **内存约束**：嵌入式设备内存有限，避免动态分配
2. **功耗优化**：不使用时进入睡眠模式
3. **实时性**：硬实时场景需使用RTOS或裸机
4. **通信协议**：根据场景选择MQTT/CoAP/HTTP
