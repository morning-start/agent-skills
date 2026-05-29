---
name: moonbit
version: v11.0.0
description: >
  Use when user asks about MoonBit programming, creating projects,
  writing code, debugging errors, testing, publishing, optimizing,
  FFI integration, or architecture decisions for MoonBit (.mbt/.pkg).
  Triggers on keywords: MoonBit, .mbt, .pkg, 月兔, moon new/build/test/check.
  Provides task-oriented routing to 8 sub-skills and 16 knowledge base references.
  Includes v0.9.x latest syntax quick reference and code templates for immediate use.
  Based on 4 real-world open-source projects (moon-lottie/MoonBash/morm/mbtgraph).
trigger:
  - user mentions "MoonBit", ".mbt", ".pkg"
  - user wants to create/build/debug/test/publish/optimize MoonBit artifacts
tags: [moonbit, action-guide, task-oriented, v11-agent-handbook]
category: language-skill
total_skills: 8
architecture: agent-handbook
meta:
  complexity: intermediate
  standalone: true
  tdd: validation-only
  tdd_waiver_reason: "行动指引技能本质是路由器/Agent手册，不包含可执行代码。质量保证通过审计脚本(audit.ps1)自动化验证+8个子技能独立测试覆盖"
  tdd_waiver_date: "2026-05-27"
  moonbit_version: "v0.9.2 (2026-05-13)"
  last_sync: "2026-05-27"
---

# 🌙 MoonBit Agent 行动手册 v11.0

> **定位**：这是 **Agent 行动手册**，不是教程也不是目录。
> 
> **核心目标**：让 AI Agent **读这一个文件就能完成 80% 的常见 MoonBit 任务**，无需频繁跳转其他文件。
>
> **适用版本**：MoonBit **v0.9.2+** (2026-05-13)
>
> **深度参考**：复杂场景请查阅 `skills/` 子技能或 `references/` 知识库。

---

## ⚡ 一、5 分钟快速开始

### 1.1 创建并运行项目

```bash
# 安装工具链（如未安装）
curl -fsSL https://www.moonbitlang.com/install.sh | bash  # Linux/macOS
# Windows: 从官网下载 .msi 安装包

# 验证安装
moon --version  # 输出: moon 0.9.2+xxxxx

# 创建项目
moon new my-app && cd my-app

# 运行（自动编译 + 执行）
moon run

# 类型检查
moon check

# 运行测试
moon test
```

### 1.2 最小可运行代码模板

```moonbit
// src/lib.mbt - 库代码
fn greet(name: String) -> String {
  "Hello, \{name}!"
}

// src/main.mbt - 主程序入口
fn main {
  println(greet("MoonBit"))
}
```

### 1.3 项目结构速览

```
my-app/
├── moon.mod.json        # 模块元数据（必需）
├── src/
│   ├── lib.mbt          # 库代码（自动导出）
│   └── main/
│       ├── main.mbt     # 主程序入口（含 fn main）
│       └── moon.pkg     # 包配置
└── tests/
    └── lib_test.mbt     # 测试文件
```

---

## 📝 二、核心语法速查 (v0.9.x 最新)

> ⚠️ **重要**：以下语法基于 **MoonBit v0.9.2** (2026-05-13)，与旧版本有重大差异！

### 2.1 基础类型与变量

```moonbit
// 类型注解（可选，推荐标注）
let x: Int = 42
let pi: Double = 3.14159
let name: String = "MoonBit"
let flag: Bool = true

// 可变绑定（需要 mut）
let mut counter: Int = 0
counter = counter + 1

// 字符串插值
let msg: String = "Count: \{counter}"
```

### 2.2 函数定义

```moonbit
// 基础函数
fn add(a: Int, b: Int) -> Int {
  a + b
}

// 泛型函数（v0.9.x 标准语法）
fn identity[T](x: T) -> T { x }

// 多参数泛型
fn pair[T, U](first: T, second: U) -> (T, U) { (first, second) }

// 箭头函数（v0.9.x 新特性）
let double = (x: Int) => x * 2
let add_curried = (a: Int, b: Int) => a + b

// 错误处理函数（raise 关键字，替代旧的 ! 语法）
fn divide(a: Int, b: Int) -> Int raise DivByZero {
  if b == 0 { raise DivByZero }
  a / b
}

// 自定义错误类型（suberror 替代旧的 type!）
suberror DivByZero

// 可选错误多态（raise?）
fn safe_divide(a: Int, b: Int) -> Int raise? {
  if b == 0 { raise DivByZero }
  a / b
}
```

### 2.3 数据类型定义

```moonbit
// 结构体（默认引用语义）
struct Point {
  x: Double
  y: Double
}

// 值类型（v0.9.x 新特性，高性能）
#valtype
struct Complex {
  real: Double
  imag: Double
}

// 枚举（代数数据类型）
enum Color {
  Red
  Green
  Blue
  RGB(Int, Int, Int)
}

// 可扩展枚举（v0.9.x 新特性，允许跨包扩展）
pub(all) extenum LogEvent[T] {
  Info(T)
  Warning(T)
}

// 带方法的枚举
enum Option[T] {
  Some(T)
  None
  
  fn is_some(self) -> Bool {
    match self {
      Some(_) => true
      _ => false
    }
  }
  
  fn unwrap(self) -> T {
    match self {
      Some(value) => value
      None => panic("unwrap on None")
    }
  }
}

// 类型别名（新语法：typealias B as A）
typealias StringMap[V] as Map[String, V]

// Trait 别名
traitalias ShowAndEq as (Show + Eq)
```

### 2.4 Trait 与实现

```moonbit
// 定义 Trait（接口）
pub(open) trait Show {
  fn to_string(self) -> String
}

pub(open) trait Eq {
  fn eq(self, other: Self) -> Bool
}

// 实现 Trait（必须显式 impl，即使有默认方法）
impl Show for Int {
  fn to_string(self) -> String { introspect(self) }
}

impl Show for String {
  fn to_string(self) -> String { self }
}

// 自定义类型的 Trait 实现
impl Show for Point {
  fn to_string(self) -> String {
    "Point(\{self.x}, \{self.y})"
  }
}

// 泛型约束
fn display[T : Show](item: T) -> Unit {
  println(item.to_string())
}

// 多重约束
fn compare_and_show[T : Show + Eq](a: T, b: T) -> String {
  if (a.eq(b)) { "Equal: \{a.to_string()}" }
  else { "Different: \{a.to_string()} vs \{b.to_string()}" }
}
```

### 2.5 模式匹配（v0.9.x 增强）

```moonbit
// 基础模式匹配
fn describe(color: Color) -> String {
  match color {
    Red => "red"
    Green => "green"
    Blue => "blue"
    RGB(r, g, b) => "rgb(\{r}, \{g}, \{b})"
  }
}

// 类型分支匹配（:TypeName 语法）
fn process_option(opt: Option[Int]) -> Int {
  match opt {
    :Some(value) => value
    :None => 0
  }
}

// Guard 条件
fn classify(n: Int) -> String {
  match n {
    x if x < 0 => "negative"
    0 => "zero"
    x if x > 100 => "large"
    _ => "small"
  }
}

// 列表推导式（v0.9.x 新特性！）
let even_squares = [for i in 0..<10 if i % 2 == 0 => i * i]
// 结果: [0, 4, 16, 36, 64]

// 惰性序列（Iter 类型）
let fibs: Iter[Int] = [
  for p1 = 1, p2 = 0;; p1 = p1 + p2, p2 = p1 => p1
]

// 布尔取反（!expr，替代 not() 函数）
fn check(cond: Bool) -> Unit {
  if !cond {
    println("condition is false")
  }
}
```

### 2.6 自定义构造器（v0.9.x 简化语法）

```moonbit
struct Point {
  x: Double
  y: Double
}

// 新语法：简洁构造器（无需双重签名）
fn Point::Point(x: Double, y: Double) -> Point {
  { x, y }  // 直接返回结构体字面量
}

// 使用
let p = Point(1.0, 2.0)  // 调用自定义构造器

// 如需保留 new 方法作为别名（向后兼容）
#alias(new)
fn Point::Point(x: Double, y: Double) -> Point { ... }
```

### 2.7 控制流

```moonbit
// If 表达式
let abs_value = if x >= 0 { x } else { -x }

// For 循环（使用元组参数，v0.9.x 标准）
for (i, item) in array::enumerate(items) {
  println("[\{i}] \{item}")
}

// While 循环
let mut i = 0
while i < 10 {
  println(i)
  i = i + 1
}

// Loop + 元组参数（v0.9.x 新标准）
let mut sum = 0
let mut i = 0
loop (sum, i) {
  if i >= 10 { break(sum) }
  sum = sum + i
  i = i + 1
}

// Defer 资源清理（v0.9.x 新特性）
fn process_file(path: String) -> Unit {
  let file = open_file(path)
  defer { close(file) }  // 作用域结束时自动执行
  
  // 使用 file...
}  // close(file) 在此处自动调用
```

### 2.8 可见性与模块系统

```moonbit
// 公开类型（跨包可见）
pub struct PublicStruct { ... }
pub enum PublicEnum { ... }

// 完全公开（包括字段/构造器）
pub(all) struct FullyPublic { ... }

// 私有（仅包内可见）
struct PrivateType { ... }

// 函数可见性
pub fn public_function() { ... }        // 跨包可调用
fn private_function() { ... }            // 仅包内

// 跨包引用（使用 @alias 完全限定名）
let value: @other_crate::SomeType = ...

// 导入外部包（在 moon.mod.json 中声明依赖后）
use @package_name::{Type, function}
```

---

## 🔧 三、常见任务 → 代码模板

### 3.1 任务：创建 CLI 工具

```bash
moon new my-cli && cd my-cli
```

```moonbit
// src/main.mbt
fn main {
  let args = args::collect_args()
  if (args.length() == 1) {
    print_usage()
  } else {
    match args[1] {
      "hello" => handle_hello(args)
      "version" => print_version()
      _ => print_usage()
    }
  }
}

fn print_usage() -> Unit {
  println("Usage: my-cli <command> [args]")
  println("Commands:")
  println("  hello   - Print greeting")
  println("  version - Print version")
}

fn handle_hello(args: Array[String]) -> Unit {
  let name = if (args.length() > 2) { args[2] } else { "World" }
  println("Hello, \{name}!")
}

fn print_version() -> Unit {
  println("my-cli v1.0.0")
}
```

### 3.2 任务：定义数据模型

```moonbit
// 用户模型
pub(all) struct User {
  id: Int
  name: String
  email: String
  role: Role
  created_at: Int  // Unix timestamp
}

pub(all) enum Role {
  Admin
  Editor
  Viewer
}

impl User {
  pub fn is_admin(self) -> Bool {
    match self.role {
      :Admin => true
      _ => false
    }
  }
  
  pub fn display_name(self) -> String {
    "\{self.name} (\{self.email})"
  }
}

// 可选用户（使用 Option）
fn find_user(id: Int) -> Option[User] {
  // 模拟数据库查询
  if (id > 0) {
    Some(User { id, name: "Test", email: "test@test.com", role: :Viewer, created_at: 0 })
  } else {
    None
  }
}
```

### 3.3 任务：错误处理最佳实践

```moonbit
// 定义领域错误
suberror NotFound(String)
suberror InvalidInput(String)
suberror PermissionDenied

// Result 类型别名
typealias Result[T] as Result[T, NotFound | InvalidInput | PermissionDenied]

// 示例：带完整错误处理的函数
fn get_user_safe(id: Int) -> Result[User] raise {
  if (id <= 0) {
    raise InvalidInput("ID must be positive")
  }
  // 模拟查找...
  match find_user(id) {
    Some(user) => user
    None => raise NotFound("User not found")
  }
}

// 调用端处理错误
fn main {
  match get_user_safe(1) {
    Ok(user) => println(user.display_name())
    Err(:NotFound(msg)) => println("Error: \{msg}")
    Err(:InvalidInput(msg)) => println("Invalid input: \{msg}")
    Err(:PermissionDenied) => println("Access denied")
  }
}
```

### 3.4 任务：编写测试

```moonbit
// tests/lib_test.mbt
test "greet returns correct message" {
  let result = greet("World")
  assert_eq(result, "Hello, World!")
}

test "add works for positive numbers" {
  assert_eq(add(2, 3), 5)
}

test "add works for negative numbers" {
  assert_eq(add(-1, -1), -2)
}

test "option is_some works" {
  assert(Some(42).is_some())
  assert!(not(None.is_some()))
}

test "option unwrap returns value" {
  assert_eq(Some(42).unwrap(), 42)
}

test "option unwrap panics on None" {
  assert_panic({ None.unwrap() })
}
```

运行测试：
```bash
moon test                    # 运行所有测试
moon test --filter "greet"   # 只运行匹配的测试
```

### 3.5 任务：发布库到 mooncakes

```bash
# 1. 确保 moon.mod.json 配置正确
cat moon.mod.json

# 2. 本地构建验证
moon check
moon test
moon build --target wasm-gc
moon build --target js

# 3. 发布（需要先登录）
moon login
moon publish
```

---

## 🚨 四、错误码快速修复指南

> 当用户报告编译错误时，**立即查阅此章节**。

### 4.1 常见错误速查表

| 错误码 | 含义 | 常见原因 | 快速修复 |
|--------|------|---------|---------|
| **E0015** | unused_mut | 定义了 `mut` 但未修改 | 删除 `mut` 或确保有赋值操作 |
| **E3002** | parse error | 语法错误 | 检查括号/花括号/引号是否配对 |
| **E4021** | unbound variable | 使用了未定义的变量 | 检查拼写或添加定义 |
| **E4046** | 循环依赖 | 包之间循环导入 | 重构以打破循环依赖 |
| **E4047-E4095** | 类型错误 | 类型不匹配 | 检查类型注解或添加显式转换 |

### 4.2 典型错误示例与修复

#### ❌ E0015: unused_mut
```moonbit
// 错误代码
fn bad_example() -> Int {
  let mut x = 42  // 警告: x 从未被重新赋值
  x
}

// 修复方案 A：删除 mut
fn fixed_a() -> Int {
  let x = 42
  x
}

// 修复方案 B：确实需要修改
fn fixed_b() -> Int {
  let mut x = 42
  x = x + 1  // 现在 mut 是必要的
  x
}
```

#### ❌ E4021: unbound variable
```moonbit
// 错误代码
fn bad_example() -> Int {
  y + 1  // 错误: y 未定义
}

// 修复：定义变量或检查拼写
fn fixed() -> Int {
  let y = 41
  y + 1
}
```

#### ❌ 旧语法迁移问题（v0.9.x）

如果你看到以下警告/错误，说明使用了**已废弃的旧语法**：

| 旧语法（废弃） | 新语法（v0.9.x） | 说明 |
|---------------|-----------------|------|
| `(..) -> T ! Err` | `(..) -> T raise Err` | 错误声明 |
| `type! MyErr` | `suberror MyErr` | 错误类型定义 |
| `f!(..)` / `f?(..)` | `try f(..)` / `try? f(..)` | 错误传播 |
| `fn f[T](..)` | `fn[T] f(..)` | 泛型函数 |
| `typealias A = B` | `typealias B as A` | 类型别名 |
| `loop { a; b }` | `loop (a, b) { .. }` | 多参数循环 |
| `not(x)` | `!x` | 布尔取反 |

**自动修复命令**：
```bash
moon fmt  # 自动格式化并迁移部分旧语法
```

---

## 🗺️ 五、意图路由表（何时查阅子技能）

对于**复杂场景**，请路由到对应子技能获取详细指导：

| 用户意图 | 关键词 | → 子技能 | → 核心知识库 |
|---------|--------|----------|-------------|
| **从零创建项目** | 新建/new/init/脚手架 | `skills/1-create-project/` | `references/app-templates.md`, `references/project-layout.md` |
| **编写/改造代码** | 写/实现/改/泛型/Trait/match | `skills/2-write-code/` | `references/syntax.md`, `references/generics-traits-methods.md`, `references/pattern-matching.md` |
| **调试/排错** | 报错/Error/Exxxx/编译失败 | `skills/3-debug-errors/` | `references/error-codes.md`, `references/pitfalls.md` |
| **编写测试** | 测试/test/assert/覆盖 | `skills/4-write-tests/` | （内嵌在本文件 §3.4） |
| **性能优化** | 慢/大/优化/performance | `skills/5-optimize/` | `references/multi-backend.md`, `references/pitfalls.md` |
| **发布库** | 发布/mooncakes/publish/npm | `skills/6-publish-lib/` | `references/library-design.md` |
| **FFI 集成** | C/JS/extern/interop/wasm-import | `skills/7-ffi-integration/` | `references/multi-backend.md` |
| **架构决策** | 设计/选型/SOLID/模式 | `skills/8-architecture-decisions/` | `references/library-design.md`, `references/decision-matrices.md`, `references/architecture.md` |

---

## 📚 六、知识库索引 (references/)

> **用途**：深度学习、完整 API 参考、真实项目案例研究。

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `syntax.md` | 完整语法手册（含所有细节） | 遇到罕见语法问题时 |
| `type-system.md` | 类型系统深度解析（可见性/Option/Result/元组） | 设计复杂类型系统时 |
| `generics-traits-methods.md` | 泛型/Trait/方法/可变性/派生宏完全指南 | 设计抽象接口时 |
| `pattern-matching.md` | 模式匹配完整指南与高级陷阱 | 复杂 match 逻辑时 |
| `error-codes.md` | 全部错误码详解（50+ 个）+ 诊断工作流 | 遇到不常见错误时 |
| `project-layout.md` | 项目结构/Monorepo/配置字段完整说明 | 大型项目架构时 |
| `app-templates.md` | **10 种应用模板**完整源代码 | 需要完整项目脚手架时 |
| `library-design.md` | **15 Parts 库设计体系** + Builder/SOLID/反模式 | 设计公开 API 时 |
| `multi-backend.md` | Wasm/JS/Native 对比 + 双运行时 + FFI | 跨平台/性能优化时 |
| `real-world-examples.md` | **4 个真实项目**架构深度解析 | 学习最佳实践时 |
| `pitfalls.md` | **8 大常见陷阱** + 规避策略 | 排查疑难杂症时 |
| `async.md` ⚡ | 异步编程（实验性） | 使用 async/await 时 |
| `verification.md` 🔬 | 形式化验证（实验性） | 需要数学证明正确性时 |
| `decision-matrices.md` 📊 | **6 个决策矩阵**（错误处理/数据结构/...） | 技术选型犹豫不决时 |
| `architecture.md` 🏗️ | 技能体系设计哲学与分层逻辑 | 理解本技能的设计思路时 |

---

## ✅ 七、质量门禁（交付前必检）

### 必跑命令

```bash
moon check          # 类型检查（必须零错误零警告）
moon test           # 运行测试（必须全部通过）
moon build --target wasm-gc   # Wasm 构建
moon build --target js        # JS 构建
moon fmt && git diff --check  # 格式化检查（无未提交的格式变更）
```

### 交付 Checklist

- [ ] `moon check` 零错误零警告
- [ ] `moon test` 全部通过
- [ ] 目标后端构建成功（wasm/js/native）
- [ ] 无废弃语法警告（无 `!` 语法、无 `type!`、无旧泛型写法）
- [ ] 公开 API 符合库设计规范（如适用）
- [ ] 无实验性 API 泄漏到稳定接口
- [ ] 代码已格式化 (`moon fmt`)

---

## 🏆 八、数据来源与致谢

本技能基于以下 **4 个真实开源项目** 的最佳实践提取：

| 项目 | 定位 | 关键贡献 |
|------|------|---------|
| 🎬 [moon-lottie](https://github.com/cg-zhou/moon-lottie) | Lottie 动画引擎 | 多层架构 / Wasm-GC+JS 双目标 / Monorepo |
| 🐚 [MoonBash](https://github.com/Haoxincode/MoonBash) | POSIX Shell 解释器 | 编译器管道 / 434KB gzip 优化 / 属性驱动 DSL |
| 🗄️ [morm](https://github.com/oboard/morm) | ORM 库 | 属性驱动 DSL / 代码生成 / FFI 互操作实战 |
| 🔢 [mbtgraph](https://github.com/morning-start/mbtgraph) | 图算法库 | 可见性决策 / 可变性语义 / SOLID 设计 |

**从这些项目中提取的核心资产**：
- ✅ 10 种应用程序模板（含 Monorepo/解释器/属性驱动）
- ✅ 15 Parts 库设计体系（含 Part 15 架构设计模式）
- ✅ 50+ 编译器错误码诊断 + 8 大常见陷阱
- ✅ 13 个官方文档 URL 深度整合至各子技能

---

## ⚠️ 九、注意事项

1. **版本兼容性**：本手册基于 **MoonBit v0.9.2**。实验性 API 可能变更。
2. **子技能优先级**：简单任务直接使用本手册；复杂任务再查阅子技能。
3. **实验性标记**：`async.md` 和 `verification.md` 为实验性特性，生产环境慎用。
4. **自动迁移**：遇到旧语法警告时，优先运行 `moon fmt` 自动迁移。
5. **值类型**：`#valtype` 在 Native/Wasm 后端有显著性能提升，但语义不同（拷贝语义 vs 引用语义）。
6. **defer 作用域**：defer 注册的清理函数在当前作用域结束时执行，非函数结束时。

---

## 📖 版本历史

| 版本 | 日期 | 变更类型 | 主要内容 |
|------|------|---------|---------|
| **v11.0.0** | 2026-05-27 | **🔄 重构为 Agent 手册** | 从「目录索引」重构为「行动手册」；内嵌 v0.9.x 最新语法速查和代码模板；新增错误码快速修复指南；补充列表推导式/箭头函数/值类型/defer/extenum 等新特性 |
| v10.0.0 | 2026-05-17 | 架构重组 | 从教程式（15个子技能）重组为任务导向（8个子技能）；知识库分离至 references/ |
| v9.0 及之前 | 2026-05 前 | 历史版本 | 详细变更见 git log |

---

*最后更新: 2026-05-27 | 版本: v11.0.0 | MoonBit: v0.9.2 | 定位: Agent Action Handbook | 子技能: 8 | 知识库: 15 files*
