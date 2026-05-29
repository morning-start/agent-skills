# 软件设计与编码规范技能系统

> 全面的软件设计与编码规范指导，涵盖从基础术语到架构设计的完整知识体系

## 📚 技能架构

```
software-design (主技能)
│
├── terminology (术语概念)         - 编程术语与概念解析
├── state-management (状态管理)    - 状态管理方案设计
├── function-design (函数设计)     - 函数设计与拆分
├── modularization (模块化)        - 模块化与架构设计
├── error-handling (错误处理)      - 错误处理机制
├── performance (性能优化)         - 性能优化策略
├── code-quality (代码质量)        - 代码质量优化
└── naming (命名规范)              - 命名与注释规范
```

## 🎯 核心能力

### 主技能能力

- **术语概念解析**: 作用域、闭包、命名空间、变量生命周期等
- **状态管理设计**: 局部/全局/共享状态、不可变状态、单向数据流
- **函数设计原则**: 单一职责、纯函数、方法封装、高内聚低耦合
- **模块化架构**: 分层架构、目录规范、代码组织结构
- **错误处理机制**: 异常捕获、错误码设计、异常抛出策略
- **性能优化**: 内存管理、资源释放、性能瓶颈分析
- **代码质量**: 可读性、语义化命名、编码风格、可维护性
- **设计原则**: SOLID 原则、设计模式、重构技巧

### 支持网络搜索

- ✅ 获取最新设计模式和实践
- ✅ 验证技术选型和方案对比
- ✅ 查询特定框架的最佳实践
- ✅ 了解性能优化新技术

## 📖 使用方式

### 基础使用

```
调用 software-design 技能，根据具体问题自动选择子技能
```

### 场景示例

#### 1. 术语查询
```
用户：什么是闭包？
→ 调用 terminology 子技能
→ 提供定义、原理、示例、应用场景
```

#### 2. 代码重构
```
用户：这个函数太复杂了，怎么优化？
→ 调用 function-design 子技能
→ 分析问题、提供拆分方案、重构代码
```

#### 3. 架构设计
```
用户：我要开发电商系统，怎么设计架构？
→ 调用 modularization + state-management + error-handling
→ 必要时网络搜索最佳实践
→ 提供完整架构方案
```

#### 4. 性能优化
```
用户：应用加载很慢，怎么优化？
→ 调用 performance 子技能
→ 性能分析、瓶颈识别、优化方案
```

## 📚 子技能文档

| 子技能 | 文档 | 主要内容 |
|--------|------|----------|
| **terminology** | [terminology.md](references/terminology.md) | 作用域、闭包、变量生命周期、命名空间 |
| **state-management** | [state-management.md](references/state-management.md) | 状态分类、数据流、Redux、性能优化 |
| **function-design** | [function-design.md](references/function-design.md) | 单一职责、纯函数、函数拆分、组合 |
| **modularization** | [modularization.md](references/modularization.md) | 分层架构、目录结构、依赖管理 |
| **error-handling** | [error-handling.md](references/error-handling.md) | 异常捕获、错误码、降级策略 |
| **performance** | [performance.md](references/performance.md) | 性能分析、内存管理、渲染优化 |
| **code-quality** | [code-quality.md](references/code-quality.md) | 可读性、重构技巧、SOLID 原则 |
| **naming** | [naming.md](references/naming.md) | 命名规范、注释技巧、文档编写 |

## 🎓 学习路径

### 🌱 新手阶段（0-6 个月）

**推荐顺序**:
```
terminology → naming → function-design → code-quality
```

**重点内容**:
- 基础术语理解
- 命名和注释规范
- 简单函数设计
- 代码质量意识

---

### 🚀 进阶阶段（6 个月 -2 年）

**推荐顺序**:
```
function-design → state-management → modularization → error-handling → performance
```

**重点内容**:
- 高级函数设计
- 状态管理方案
- 模块化设计
- 错误处理机制
- 性能优化基础

---

### 🏗️ 架构师阶段（2 年以上）

**学习重点**:
```
架构设计 → 性能优化 → 代码质量 → 团队规范制定
```

**重点内容**:
- Clean Architecture
- 高级性能优化
- 设计模式应用
- 架构决策和权衡
- 团队规范制定

## 🔍 网络搜索配置

### 触发条件

- 用户明确要求搜索最新实践
- 需要了解技术趋势
- 验证设计模式使用情况
- 查询框架最佳实践
- 获取性能对比数据

### 搜索示例

```
- "React state management comparison 2025"
- "SOLID principles real-world examples"
- "code refactoring techniques 2025"
- "performance optimization patterns"
```

## 📋 工作流

详细的工作流和调用规则请参考：[WORKFLOW.md](WORKFLOW.md)

### 调用流程

```
用户问题
  ↓
问题分析和分类
  ↓
选择子技能（可多个）
  ↓
必要时网络搜索
  ↓
整合信息
  ↓
提供解答 + 示例 + 建议
```

## 🎯 核心概念体系

### 基础术语
- 作用域（Scope）
- 闭包（Closure）
- 变量生命周期
- 命名空间
- 执行上下文

### 设计原则（SOLID）
1. 单一职责（SRP）
2. 开放封闭（OCP）
3. 里氏替换（LSP）
4. 接口隔离（ISP）
5. 依赖倒置（DIP）

### 代码质量维度
- 可读性
- 可维护性
- 可扩展性
- 可测试性
- 解耦

### 架构模式
- MVC
- MVVM
- Clean Architecture
- 分层架构
- 微服务

## 📝 使用示例

### 示例 1: 术语查询

```
用户：什么是闭包？怎么用？

调用：software-design/terminology

输出:
✓ 闭包定义
✓ 工作原理图解
✓ 实际代码示例
✓ 应用场景
✓ 注意事项
```

### 示例 2: 状态管理

```
用户：这个组件的状态应该怎么管理？

调用：software-design/state-management

输出:
✓ 状态分析（局部/全局/共享）
✓ 管理方案推荐
✓ 代码实现示例
✓ 最佳实践建议
```

### 示例 3: 架构设计

```
用户：我要开发一个社交 App，怎么设计架构？

调用：
- software-design/modularization
- software-design/state-management
- software-design/error-handling
- （可选）网络搜索

输出:
✓ 分层架构设计
✓ 目录结构方案
✓ 技术选型建议
✓ 关键设计决策
```

## ⚠️ 注意事项

- **子技能选择**: 根据问题类型自动选择，无需手动指定
- **网络搜索**: 仅在需要最新信息时启用
- **学习路径**: 根据自身水平选择合适的内容
- **代码示例**: 所有示例都可运行，遵循最佳实践
- **原则应用**: 结合实际场景，避免教条主义

## 📦 文件结构

```
software-design/
├── SKILL.md                    # 主技能文档
├── WORKFLOW.md                 # 工作流和调用规则
├── README.md                   # 本文件
└── references/                 # 子技能文档
    ├── terminology.md
    ├── state-management.md
    ├── function-design.md
    ├── modularization.md
    ├── error-handling.md
    ├── performance.md
    ├── code-quality.md
    └── naming.md
```

## 📊 版本历史

### v1.0.0 (2025-01-XX)

**初始版本发布**

- ✅ 创建完整的技能系统架构
- ✅ 定义 8 个子技能
- ✅ 配置网络搜索能力
- ✅ 提供学习路线图
- ✅ 制定工作流规则
- ✅ 编写详细文档和示例

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License

## 📧 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 参与讨论

---

**最后更新**: 2025-01-XX

**维护者**: skill-manager
