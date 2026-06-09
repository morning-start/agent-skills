# Rust Skills 架构总览

## 整体架构

```
rust-skills (母技能)
├── references/           # 框架文档
│   ├── meta-cognition.md  # 元认知框架
│   ├── architecture.md    # 本文档
│   └── commands.md        # 命令系统
├── Layer 1: 语言机制      # m01-m07
├── Layer 2: 设计选择      # m09-m15
├── Layer 3: 领域扩展      # domain-*
└── 基础技能/              # rust-core, rust-cargo 等
```

## 技能分层

### Layer 1: 语言机制 (m01-m07)

| 技能 | 核心问题 | 触发条件 |
|------|---------|---------|
| m01-ownership | 谁应该拥有这个数据? | E0382, E0597, move, borrow |
| m02-resource | 什么所有权模式适合? | Box, Rc, Arc, RefCell |
| m03-mutability | 为什么这个数据需要变化? | mut, Cell, E0596, E0499 |
| m04-zero-cost | 编译时还是运行时多态? | generic, trait, E0277 |
| m05-type-driven | 如何用类型防止无效状态? | newtype, PhantomData |
| m06-error-handling | 预期失败还是 bug? | Result, Error, panic, ? |
| m07-concurrency | CPU 密集还是 I/O 密集? | async, Send, Sync, thread |

### Layer 2: 设计选择 (m09-m15)

| 技能 | 核心问题 | 触发条件 |
|------|---------|---------|
| m09-domain | 这个概念扮演什么角色? | DDD, entity, value object |
| m10-performance | 瓶颈在哪里? | benchmark, profiling |
| m11-ecosystem | 哪个 crate 适合这个任务? | crate selection, dependencies |
| m12-lifecycle | 何时创建、使用、清理? | RAII, Drop, lazy init |
| m13-domain-error | 谁来处理这个错误? | retry, circuit breaker |
| m14-mental-model | 如何正确理解这个? | learning Rust, why |
| m15-anti-pattern | 这个模式是否隐藏设计问题? | code smell, common mistakes |

### Layer 3: 领域扩展 (domain-*)

| 技能 | 领域 | 核心约束 |
|------|------|---------|
| domain-fintech | 金融科技 | 审计跟踪、精度、一致性 |
| domain-ml | 机器学习 | 内存效率、GPU 加速 |
| domain-cloud-native | 云原生 | 12-Factor、可观测性、优雅关闭 |
| domain-iot | 物联网 | 离线优先、功耗管理、安全 |
| domain-web | Web 服务 | 无状态、延迟 SLA、并发 |
| domain-cli | CLI | UX、配置优先级、退出码 |
| domain-embedded | 嵌入式 | 无堆分配、no_std、实时 |

## 技能路由

### 入口点

1. **rust-router**: 主路由器，所有 Rust 问题的入口
2. **rust-learner**: 获取最新 Rust/crate 版本信息
3. **coding-guidelines**: 编码规范查询

### 工作流程

```
用户问题
     │
     ▼
┌─────────────────────────────────────────┐
│           Hook Layer                     │
│  关键词触发元认知与路由                   │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│           rust-router                    │
│  识别入口层 + 领域                        │
│  决策: 双技能加载                        │
└─────────────────────────────────────────┘
     │
     ├──────────────┬──────────────┐
     ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Layer 1  │  │ Layer 2  │  │ Layer 3  │
│ m01-m07  │  │ m09-m15  │  │ domain-* │
└──────────┘  └──────────┘  └──────────┘
     │
     ▼
领域正确的架构解决方案
```

## 基础技能映射

| 基础技能 | 覆盖的 Layer 1 技能 |
|---------|-------------------|
| rust-ownership | m01-ownership |
| rust-smart-pointers | m02-resource |
| rust-generics | m04-zero-cost |
| rust-error-handling | m06-error-handling |
| rust-concurrency | m07-concurrency |

| 基础技能 | 覆盖的 Layer 2 技能 |
|---------|-------------------|
| rust-core | m14-mental-model |

## 版本要求

- Rust Skills: 2.1.0
- 支持 Rust 1.70+
