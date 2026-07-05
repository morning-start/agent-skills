# MoonBit 决策支持矩阵集合

> 📅 创建: 2026-05-08 | 版本: v1.0.0
> 用途: 快速选择正确的方案、避免常见错误

---

## 目录

1. [错误处理方式选择](#1-错误处理方式选择)
2. [数据结构选择](#2-数据结构选择)
3. [函数签名标注选择](#3-函数签名标注选择)
4. [后端目标选择](#4-后端目标选择)
5. [测试策略选择](#5-测试策略选择)
6. [常见陷阱速查](#6-常见陷阱速查)

---

## 1. 错误处理方式选择

**问题**: 我应该如何处理这个可能失败的操作？

| 场景 | 推荐方案 | 关键考虑 | 示例 |
|------|---------|---------|------|
| 值可能不存在 | `Option[T]` | 轻量级，无错误信息需求 | 查找、可选配置 |
| 操作可能成功/失败 | `Result[T, E]` | 需要详细错误原因 | IO、解析、外部资源 |
| 多层调用链传播错误 | `raise + try/catch` | 需要错误传播和恢复 | 复杂业务逻辑 |
| 调试/快速失败 | `try! / fail!` | 确定不应出错 | 前置条件检查 |
| 转换为值处理 | `try? expr` | 将 raise 转为 Result | 测试中验证错误 |

**决策流程**:
```
需要错误信息?
├── 否 → Option[T]
├── 是 → 需要传播?
│   ├── 是 → raise + try/catch
│   └── 否 → Result[T, E] 或 try?
└── 调试阶段? → try! / fail!
```

---

## 2. 数据结构选择

**问题**: 我应该使用哪种数据结构？

| 使用场景 | 推荐类型 | 特点 |
|---------|---------|------|
| 固定大小、已知元素 | `Array[T]` | 连续内存，快速索引 |
| 键值对查找 | `Map[K, V]` | O(1) 查找和插入 |
| 唯一值集合 | `Set[T]` | 自动去重 |
| 两个值的组合 | `(T1, T2)` 元组 | 临时组合 |
| 复杂数据聚合 | `struct` | 命名字段，类型安全 |
| 有限状态/分类 | `enum` | 模式匹配友好 |
| 可选值 | `Option[T]` | 明确表达"有或无" |
| 可能失败的结果 | `Result[T, E]` | 成功/失败语义 |

**性能对比**:

| 操作 | Array | Map | Set |
|------|-------|-----|-----|
| 访问 | O(1) | O(1) avg | O(1) avg |
| 插入 | O(1)* | O(1) avg | O(1) avg |
| 查找 | O(n)** | O(1) avg | O(1) avg |
| 删除 | O(n) | O(1) avg | O(1) avg |

*末尾追加 O(1), 中间插入/删除 O(n)
**线性搜索 O(n)

---

## 3. 函数签名标注选择

**问题**: 我的函数应该用什么错误标注？

| 情况 | 标注 | 示例 |
|------|------|------|
| 保证不抛出错误 | `noraise` | `fn add(a, b) -> Int noraise` |
| 抛出特定错误类型 | `raise ErrorType` | `fn div(x, y) -> Int raise DivError` |
| 抛出通用错误（省略写法） | `raise` (或 `raise Error`) | `fn f() -> Unit raise` |
| 高阶函数（灵活） | `raise?` | `fn map(f: (T) -> U raise?) -> Array[U] raise?` |

**高阶函数场景详解**:

```moonbit
// 场景 1: 参数函数一定不抛出错误
fn map_no_error(arr, f: (T) -> U noraise) -> Array[U] noraise { ... }

// 场景 2: 参数函数一定抛出错误
fn map_with_error(arr, f: (T) -> U raise) -> Array[U] raise { ... }

// 场景 3: 参数函数可能抛出也可能不抛出（推荐）
fn map_polymorphic(arr, f: (T) -> U raise?) -> Array[U] raise? { ... }
```

---

## 4. 后端目标选择

**问题**: 我应该编译到哪个后端？

| 目标平台 | 推荐 | 特点 | 适用场景 |
|---------|------|------|---------|
| 浏览器/Wasm | **wasm** | 小体积、高性能 | WebAssembly 应用 |
| Wasm-GC 新特性 | **wasm-gc** | GC 支持、组件模型 | 边缘计算、新项目 |
| Node.js 后端 | **js** | 直接运行 JS | 服务端应用 |
| 前端集成 | **js** | 与 JS 互操作 | 前端库 |
| 高性能/系统级 | **native** | LLVM 编译 | 性能关键应用 |
| 本地开发测试 | **wasm** (默认) | 快速编译 | 日常开发 |

**多后端策略**:
```json
{
  "preferred-target": "wasm",  // 默认开发用 wasm
  // 生产环境根据需要切换:
  // moon build --target js      // 部署到 Node.js
  // moon build --target native  // 高性能部署
}
```

---

## 5. 测试策略选择

**问题**: 我应该使用什么类型的测试？

| 测试类型 | 适用场景 | 工具 | 优点 |
|---------|---------|------|------|
| 单元测试 | 函数/方法逻辑 | `test { ... }` | 快速、隔离 |
| 文档字符串测试 | 公共 API 示例 | `/// \`mbt check\` ... `` | 即文档即测试 |
| 快照测试 | 输出验证 | `inspect(value, content="...")` | 容易更新 |
| 黑盒测试 | 集成测试 | `@package.fn()` | 测试公共接口 |
| 白盒测试 | 私有成员测试 | 同包内直接访问 | 内部逻辑验证 |
| 覆盖率测试 | 质量门禁 | `moon coverage analyze` | 发现未覆盖分支 |

**TDD 流程推荐**:
```
1. 写失败的测试 (Red)
2. 写最小实现通过测试 (Green)
3. 重构优化 (Refactor)
4. 运行完整测试套件确认
```

---

## 6. 常见陷阱速查

### 🔥 致命陷阱（编译错误）

| # | 陷阱 | 正确做法 | 影响 |
|---|------|---------|------|
| 1 | **变量/函数大写开头** | 使用 snake_case | 编译错误 |
| 2 | **忘记 `mut`** | `let mut x = ...` | 编译错误 |
| 3 | **不处理错误** | 必须显式处理所有错误 | 编译错误 |
| 4 | **方法不用 `Type::` 前缀** | `fn Type::method(self)` | 编译错误 |
| 5 | **跨包调用忘记前缀** | `@package.function()` | 编译错误 |
| 6 | **使用 `++`/`--`** | `i += 1` 或 `i = i + 1` | 编译错误 |

### ⚠️ 逻辑陷阱（运行时错误）

| # | 陷阱 | 正确做法 | 影响 |
|---|------|---------|------|
| 7 | **数组越界访问** | 使用 `.get(i)` 安全访问 | Panic |
| 8 | **对 Error 类型穷尽匹配缺少 `_`** | 必须包含通配符 | 编译警告/错误 |
| 9 | **#borrow 用于存储指针的参数** | 使用 `#owned` 或检查生命周期 | 内存安全问题 |
| 10 | **忘记 `moonbit_decref` owned 参数** | C 端必须 decref | 内存泄漏 |
| 11 | **对 External Object 调用 free()** | GC 管理容器，只释放内部资源 | Double free |
| 12 | **使用 `moonbit_make_bytes` 包含内部指针的结构** | 使用 External Object | 内部指针泄漏 |

### 💡 性能陷阱

| # | 陷阱 | 正确做法 | 影响 |
|---|------|---------|------|
| 13 | **不必要的 clone/copy** | 使用引用或借用 | 性能下降 |
| 14 | **在循环中创建大量临时对象** | 对象池或复用 | GC 压力 |
| 15 | **过度使用 `String` 拼接** | 使用 `StringBuilder` 或预分配 | 性能下降 |
| 16 | **忽略 `--warn-list` 警告** | 启用并修复警告 | 潜在 bug |

### 🎯 惯用法陷阱

| # | 陷阱 | 正确做法 | 影响 |
|---|------|---------|------|
| 17 | **C-style for 循环** | 使用 range `for i in 0..<n` | 不地道 |
| 18 | **过长的函数 (>200行)** | 拆分为小函数 | 可读性差 |
| 19 | **巨大的 "util" 文件** | 按功能拆分文件 | 维护困难 |
| 20 | **不写文档字符串** | 公共 API 都应有文档 | 可发现性差 |
| 21 | **跳过 `moon fmt`** | 定期格式化 | 代码风格不一致 |
| 22 | **不提交 mbti 文件** | 加入版本控制 | 无法 review API 变更 |

---

## 快速命令参考

### 开发常用命令序列

```bash
# 编辑后的快速验证循环
moon check && moon test --filter "MyModule::*" && moon fmt

# 完整验证（提交前）
moon check --target all && moon test && moon fmt && moon info

# 只检查不构建（最快）
moon check

# 更新快照测试
moon test --update

# 查看某个符号的信息
moon ide doc "my_function"

# 重命名符号（语义化）
moon ide rename old_name new_name --loc src/file.mbt:10:5
```

### IDE 命令速查

| 命令 | 用途 | 示例 |
|------|------|------|
| `moon ide doc "<query>"` | 搜索 API 文档 | `"parse_int"` |
| `moon ide outline <dir>` | 查看文件结构 | `src/lib/` |
| `moon ide peek-def <sym>` | 跳转到定义 | `User::new` |
| `moon ide find-references <sym>` | 查找所有引用 | `process_data` |
| `moon ide rename <old> <new>` | 语义重命名 | `foo bar` |
| `moon ide analyze [path]` | 分析代码质量 | `src/main.mbt` |

---

## 相关资源

- [error-handling](../moonbit-error-handling/SKILL.md) - 错误处理详细指南
- [data-types](../moonbit-data-types/SKILL.md) - 数据结构深入讲解
- [testing](../moonbit-testing/SKILL.md) - 测试策略与技巧
- [toolchain](../moonbit-toolchain/SKILL.md) - 工具链完整文档
- [workflow](../moonbit-workflow/SKILL.md) - 标准化工作流
- [project-layout](../moonbit-project-layout/SKILL.md) - 项目布局规范

---

*版本: v1.0.0 | 类别: Decision Support | 维护: 随技能更新同步*
