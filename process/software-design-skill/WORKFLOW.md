# 软件设计技能系统 - 使用工作流

## 技能架构

```
software-design (主技能)
├── terminology (术语概念)
├── state-management (状态管理)
├── function-design (函数设计)
├── modularization (模块化与架构)
├── error-handling (错误处理)
├── performance (性能优化)
├── code-quality (代码质量)
└── naming (命名与注释)
```

## 调用流程

### 场景 1: 新手学习

```
用户提问 → 判断为学习类问题
  ↓
调用 software-design
  ↓
根据问题类型选择子技能:
  - 术语问题 → terminology
  - 概念理解 → terminology + 相关子技能
  - 最佳实践 → 对应子技能
  ↓
提供解释 + 示例 + 学习建议
```

### 场景 2: 代码重构

```
用户提供代码 → 分析代码问题
  ↓
识别问题类型:
  - 函数过大 → function-design
  - 结构混乱 → modularization
  - 命名不清 → naming
  - 性能问题 → performance
  - 错误处理 → error-handling
  ↓
调用对应子技能
  ↓
提供重构方案 + 代码示例
```

### 场景 3: 架构设计

```
用户描述需求 → 分析项目规模
  ↓
判断项目类型:
  - 小型项目 → modularization (简单方案)
  - 中型项目 → modularization + state-management
  - 大型项目 → modularization + 所有相关子技能
  ↓
必要时网络搜索最佳实践
  ↓
提供架构方案 + 目录结构 + 技术选型
```

### 场景 4: 性能优化

```
用户描述性能问题 → 分析问题类型
  ↓
调用 performance 子技能
  ↓
性能分析方法:
  1. 性能测试
  2. 瓶颈识别
  3. 优化方案
  ↓
必要时结合:
  - state-management (状态优化)
  - function-design (算法优化)
  - modularization (架构优化)
  ↓
提供优化方案 + 代码示例
```

## 网络搜索配置

### 触发条件

满足以下任一条件时启用网络搜索：

1. 用户明确要求"搜索最新实践"
2. 需要了解技术趋势
3. 验证设计模式的当前使用情况
4. 查询特定框架的最佳实践
5. 获取性能对比数据

### 搜索关键词模板

```
- "{技术} {主题} best practices {年份}"
- "{设计模式} real-world examples"
- "{框架} {问题} solutions"
- "{技术} vs {技术} comparison"
- "{主题} performance optimization"
```

### 搜索示例

**用户**: "现在 React 状态管理用什么最好？"

**工作流**:
```
1. 识别问题：技术选型
2. 启用网络搜索
3. 搜索关键词："React state management comparison 2025"
4. 整合搜索结果
5. 调用 state-management 子技能
6. 提供对比分析和推荐
```

## 子技能调用规则

### 单一子技能

适用于简单、明确的问题：

- "什么是闭包？" → terminology
- "这个函数怎么优化？" → function-design
- "状态应该怎么管理？" → state-management

### 多子技能协作

适用于复杂、综合性问题：

**示例**: "帮我设计一个电商系统的架构"

```
调用流程:
1. modularization - 架构设计
2. state-management - 状态管理方案
3. error-handling - 错误处理策略
4. performance - 性能优化建议
5. code-quality - 代码质量标准
6. naming - 命名规范建议
```

## 学习路径推荐

### 🌱 新手阶段（0-6 个月）

**推荐子技能**:
1. terminology - 基础术语
2. naming - 命名规范
3. function-design - 基础函数设计

**学习顺序**:
```
terminology → naming → function-design → code-quality
```

---

### 🚀 进阶阶段（6 个月 -2 年）

**推荐子技能**:
1. function-design - 高级函数设计
2. state-management - 状态管理
3. modularization - 模块化
4. error-handling - 错误处理

**学习顺序**:
```
function-design → state-management → modularization → error-handling → performance
```

---

### 🏗️ 架构师阶段（2 年以上）

**推荐子技能**:
- 所有子技能综合运用
- 重点关注：modularization、performance、code-quality

**学习重点**:
```
架构设计 → 性能优化 → 代码质量 → 团队规范制定
```

---

## 使用示例

### 示例 1: 术语查询

**用户**: "什么是作用域？"

**工作流**:
```
1. 识别问题类型：术语查询
2. 调用 terminology 子技能
3. 提供：
   - 定义和解释
   - 工作原理
   - 代码示例
   - 常见误区
   - 相关概念
```

---

### 示例 2: 代码重构

**用户**: "这个函数太复杂了，帮我重构"

**工作流**:
```
1. 分析代码问题
2. 调用 function-design 子技能
3. 应用原则:
   - 单一职责
   - 函数拆分
   - 提取公共逻辑
4. 提供重构后代码
5. 解释改进点
```

---

### 示例 3: 架构设计

**用户**: "我要开发一个社交 App，怎么设计架构？"

**工作流**:
```
1. 分析需求：中型项目
2. 启用网络搜索（可选）：社交 App 架构最佳实践
3. 调用 modularization - 设计架构
4. 调用 state-management - 状态方案
5. 调用 error-handling - 错误处理
6. 调用 performance - 性能优化
7. 整合输出:
   - 架构图
   - 目录结构
   - 技术选型
   - 关键设计决策
```

---

### 示例 4: 性能优化

**用户**: "我的应用加载很慢，怎么优化？"

**工作流**:
```
1. 调用 performance 子技能
2. 性能分析方法:
   - 性能测试工具
   - 瓶颈识别
3. 优化方向:
   - 网络优化
   - 渲染优化
   - 代码优化
4. 必要时结合:
   - modularization (代码分割)
   - state-management (状态优化)
5. 提供优化清单和实施步骤
```

---

## 质量保障

### 代码示例标准

所有代码示例必须：
- ✅ 可运行
- ✅ 符合最佳实践
- ✅ 有清晰注释
- ✅ 包含正反对比
- ✅ 说明适用场景

### 解释标准

所有解释必须：
- ✅ 准确无误
- ✅ 通俗易懂
- ✅ 有实际示例
- ✅ 说明优缺点
- ✅ 提供学习建议

### 验证流程

每次回答后检查：
- [ ] 是否解决了用户问题？
- [ ] 代码示例是否正确？
- [ ] 解释是否清晰？
- [ ] 是否有更好的方案？
- [ ] 是否需要网络搜索验证？

---

## 版本历史

- **v1.0.0** (2025-01-XX): 初始版本
  - 定义技能调用流程
  - 制定学习路径
  - 提供使用示例
  - 配置网络搜索
