# MoonBit Skills 架构说明

## 设计哲学

MoonBit Skills 采用分层技能架构，参考 Rust Skills 的元认知框架，但针对 MoonBit 的语言特性进行了调整：

- MoonBit 没有所有权/借用检查器（有 GC），因此不需要所有权相关的复杂技能分层
- MoonBit 强调多后端编译，因此增加后端领域技能
- MoonBit 有强大的模式匹配和函数式特性，需要专门的技能覆盖

## 技能分层

```mermaid
flowchart TB
    subgraph L1 ["Layer 1: 语言基础"]
        L1_1[变量、类型、控制流]
        L1_2[数据结构]
        L1_3[函数与表达式]
    end

    subgraph L2 ["Layer 2: 抽象与组织"]
        L2_1[泛型与 Trait]
        L2_2[模式匹配]
        L2_3[错误处理]
        L2_4[模块与包]
    end

    subgraph L3 ["Layer 3: 工程与部署"]
        L3_1[工具链与构建]
        L3_2[测试与调试]
        L3_3[包管理]
        L3_4[多后端编译]
    end

    L1 --> L2 --> L3

    style L1 fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    style L2 fill:#fff3e0,stroke:#ff9800,color:#e65100
    style L3 fill:#e3f2fd,stroke:#2196f3,color:#0d47a1
```

## 与 Rust Skills 的对比

| 维度 | Rust Skills | MoonBit Skills |
|------|------------|----------------|
| 内存管理 | 所有权系统（核心） | GC（无需所有权技能） |
| 编程范式 | 命令式为主 | 函数式+命令式融合 |
| 后端支持 | 单一原生后端 | wasm/js/native 多后端 |
| 错误处理 | Result + panic | Option + Result + raise |
| 模式匹配 | 支持 | 更强大，核心特性 |

## 技能触发规则

```mermaid
flowchart TD
    U[用户问题] --> Q{问题类型?}

    Q -->|语法基础| C1[moonbit-core-skill]
    Q -->|数据结构| C2[moonbit-data-structures-skill]
    Q -->|模式匹配| C3[moonbit-pattern-matching-skill]
    Q -->|构建/工具| C4[moonbit-toolchain-skill]
    Q -->|包管理| C5[moonbit-packages-skill]
    Q -->|WASM 开发| C6[moonbit-wasm-skill]

    style U fill:#f5f5f5,color:#424242
    style C1 fill:#c8e6c9,stroke:#388e3c,color:#1b5e20
    style C2 fill:#c8e6c9,stroke:#388e3c,color:#1b5e20
    style C3 fill:#ffe0b2,stroke:#fb8c00,color:#e65100
    style C4 fill:#bbdefb,stroke:#1976d2,color:#0d47a1
    style C5 fill:#bbdefb,stroke:#1976d2,color:#0d47a1
    style C6 fill:#f3e5f5,stroke:#9c27b0,color:#4a148c
```

| 用户信号 | 推荐技能 |
|---------|---------|
| "如何声明变量" | moonbit-core-skill |
| "模式匹配怎么用" | moonbit-pattern-matching-skill |
| "如何构建项目" | moonbit-toolchain-skill |
| "怎么发布包" | moonbit-packages-skill |
| "编译到 WASM" | moonbit-wasm-skill |
| "数组/Map 用法" | moonbit-data-structures-skill |
| "函数式编程" | moonbit-functions-skill |
| "泛型和 Trait" | moonbit-generics-skill |
| "错误处理" | moonbit-error-handling-skill |

## 四维分类

根据 skill-factory 分类体系，moonbit-skills 属于 **Type 4 (重+厚)**：

| 维度 | 类型 | 说明 |
|------|------|------|
| 功能维度 | **重** | 13 个子技能，覆盖完整语言生态 |
| 内容维度 | **厚** | 包含 references/ 目录、详细示例、图表 |
| 输出结构 | skills/ + references/ | 混合模式 |
| 复杂度评估 | 高 | 覆盖语法、工具链、多后端 |

## 子技能依赖关系

```mermaid
flowchart LR
    subgraph 入门
        TUT[tutorial] --> CORE[core]
        CORE --> DS[data-structures]
    end

    subgraph 进阶
        DS --> FN[functions]
        DS --> PM[pattern-matching]
        FN --> GEN[generics]
        PM --> EH[error-handling]
    end

    subgraph 工程
        TC[toolchain] --> PKG[packages]
        TC --> TEST[testing]
    end

    subgraph 后端
        TC --> WASM[wasm]
        TC --> JS[js]
        TC --> NAT[native]
    end

    style 入门 fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    style 进阶 fill:#fff3e0,stroke:#ff9800,color:#e65100
    style 工程 fill:#e3f2fd,stroke:#2196f3,color:#0d47a1
    style 后端 fill:#f3e5f5,stroke:#9c27b0,color:#4a148c
```
