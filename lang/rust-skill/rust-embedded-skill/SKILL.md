# rust-embedded-skill

## 前言区

```
name: rust-embedded-skill
version: v1.0.0
author: book-skills
description: 嵌入式领域Rust应用技能，涵盖no_std开发、Cortex-M、ESP32、外设驱动与实时系统
tags: [embedded, no_std, cortex-m, esp32, real-time, bare-metal, drivers]
trigger: /rust-embedded
layer: Layer 3 - Domain Extensions
```

## 概述

本技能聚焦嵌入式开发领域，展示Rust在裸机开发、外设驱动、实时系统等场景下的内存安全与性能优势。

## 任务目标

1. 构建no_std固件
2. 开发Cortex-M外设驱动
3. ESP32物联网应用
4. 实时系统开发

## 操作步骤

### 1. no_std基础

```rust
#![no_std]
#![no_main]

extern crate panic_halt;

use cortex_m_rt::entry;

static MESSAGE: &str = "Hello, Embedded Rust!";

#[entry]
fn main() -> ! {
    let _ = cortex_m::asm::nop();
    loop {
        cortex_m::asm::wfi();
    }
}
```

### 2. GPIO控制

```rust
use embedded_hal::digital::v2::OutputPin;

pub struct Led<GPIO> {
    pin: GPIO,
}

impl<GPIO, E> Led<GPIO>
where
    GPIO: OutputPin<Error = E>,
{
    pub fn new(pin: GPIO) -> Self {
        Led { pin }
    }

    pub fn on(&mut self) -> Result<(), E> {
        self.pin.set_low()
    }

    pub fn off(&mut self) -> Result<(), E> {
        self.pin.set_high()
    }

    pub fn toggle(&mut self) -> Result<(), E> {
        if self.pin.is_set_low().unwrap_or(true) {
            self.pin.set_high()
        } else {
            self.pin.set_low()
        }
    }
}
```

### 3. PWM控制舵机

```rust
use embedded_hal::pwm::Pwm;

pub struct Servo<PWM> {
    pwm: PWM,
    min_duty: u16,
    max_duty: u16,
}

impl<PWM, E> Servo<PWM>
where
    PWM: Pwm<Error = E>,
{
    pub fn new(pwm: PWM, min_duty: u16, max_duty: u16) -> Self {
        Servo { pwm, min_duty, max_duty }
    }

    pub fn set_angle(&mut self, angle: f32) -> Result<(), E>
    where
        E: PartialEq,
    {
        let angle = angle.max(0.0).min(180.0);
        let duty = self.min_duty
            + ((self.max_duty - self.min_duty) as f32 * angle / 180.0) as u16;
        self.pwm.set_duty(self.pwm.get_max_duty() / 2, duty)
    }
}
```

### 4. 串口通信

```rust
use embedded_hal::serial::{Read, Write};
use nb::block;

pub struct Serial<UART> {
    uart: UART,
}

impl<UART, E> Serial<UART>
where
    UART: Read<Error = E> + Write<Error = E>,
    E: core::fmt::Debug,
{
    pub fn new(uart: UART) -> Self {
        Serial { uart }
    }

    pub fn write_string(&mut self, s: &str) -> Result<(), E> {
        for byte in s.bytes() {
            block!(self.uart.write(byte))?;
        }
        Ok(())
    }

    pub fn read_byte(&mut self) -> Result<u8, E> {
        block!(self.uart.read())
    }
}
```

### 5. ESP32 WiFi应用

```rust
use esp_idf_sys::{esp, wifi, nvs, esp_err};

pub fn connect_wifi(ssid: &str, password: &str) -> Result<(), esp_err> {
    unsafe {
        let wifi_config = wifi::config_t {
            sta: wifi::sta_config_t {
                ssid: [0u8; 32],
                password: [0u8; 64],
                ..Default::default()
            },
            ..Default::default()
        };

        let ssid_bytes = ssid.as_bytes();
        let pass_bytes = password.as_bytes();

        wifi_config.sta.ssid[..ssid_bytes.len()]
            .copy_from_slice(ssid_bytes);
        wifi_config.sta.password[..pass_bytes.len()]
            .copy_from_slice(pass_bytes);

        esp!(wifi::esp_wifi_set_config(
            wifi::ESP_IF_WIFI_STA,
            &wifi_config
        ))?;

        esp!(wifi::esp_wifi_start())
    }
}
```

### 6. 定时器中断

```rust
use cortex_m::interrupt::CriticalSection;
use stm32f4::TIM2;

pub trait TimerInterrupt {
    fn on_tick(&self);
}

pub struct SystickTimer {
    tim: TIM2,
}

impl SystickTimer {
    pub fn new(tim: TIM2) -> Self {
        SystickTimer { tim }
    }

    pub fn start(&mut self, period_hz: u32) {
        self.tim.arr.write(|w| w.arr().bits(period_hz));
        self.tim.dier.write(|w| w.uie().enabled());
        self.tim.cr1.write(|w| w.cen().enabled());
    }
}
```

## 资源索引

### 核心库

| 库 | 用途 | 链接 |
|---|------|------|
| embedded-hal | 嵌入式抽象 | https://github.com/rust-embedded/embedded-hal |
| cortex-m | ARM Cortex-M | https://github.com/rust-embedded/cortex-m |
| esp-idf-sys | ESP32支持 | https://github.com/esp-rs/esp-idf-sys |
| nb | 非阻塞抽象 | https://github.com/rust-embedded/nb |

### 关键依赖

```toml
[dependencies]
embedded-hal = "0.2"
cortex-m = "0.7"
cortex-m-rt = "0.7"
esp-idf-sys = "0.33"
nb = "1.1"
panic-halt = "0.2"
```

## 注意事项

1. **no_std环境**：避免使用std库，使用core替代
2. **内存分配**：静态分配为主，避免堆分配
3. **中断处理**：注意中断优先级和资源共享
4. **外设访问**：使用volatile访问外设寄存器
