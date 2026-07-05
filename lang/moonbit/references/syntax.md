# MoonBit 语法参考手册 📖

> **来源整合**：
> - [moonbit-quickstart/SKILL.md](../skills/layer1-foundation-path/moonbit-quickstart/SKILL.md) (v5.0.0)
> - [moonbit-data-types/SKILL.md](../skills/layer1-foundation-path/moonbit-data-types/SKILL.md) (v6.0.0)
>
> **用途**：快速查阅 MoonBit 核心语法、数据类型和项目结构
> **定位**：语法速查参考文档（非学习教程）

---

## Part 1: 环境搭建与项目初始化

### 系统要求

- CPU：双核 64 位处理器
- 内存：4GB RAM
- 磁盘空间：至少 200MB

### 安装工具链

#### Linux / macOS

```bash
curl -fsSL https://www.moonbitlang.com/install.sh | bash
source ~/.bashrc
```

#### Windows

1. 访问 [MoonBit 官网](https://www.moonbitlang.com) 下载 Windows 安装程序（.msi）
2. 双击安装文件，按照向导完成安装
3. 打开 PowerShell，执行验证

### 验证安装

```bash
moon --version
```

预期输出：
```
moon 0.1.20250606+a3f4966ca
```

### 可选配置

```bash
# 配置国内源（中国大陆用户推荐）
moon config --set registry https://mooncakes.cnpmjs.org
```

### 创建项目

```bash
moon new hello-moonbit && cd hello-moonbit
```

### 项目结构解析

```
hello-moonbit/
├── moon.mod.json          # 模块元数据（必需）
├── src/
│   └── lib.mbt            # 库代码
├── cmd/
│   └── main/
│       ├── main.mbt       # 主程序入口
│       └── moon.pkg.json  # 主包配置
└── tests/
    └── lib_test.mbt       # 测试文件
```

### 核心配置文件说明

#### moon.mod.json（模块根）

```json
{
  "name": "your_username/hello-moonbit",
  "version": "0.1.0",
  "license": "Apache-2.0",
  "description": "My first MoonBit project"
}
```

**作用**：
- 定义模块名称和版本
- 管理依赖关系
- 所有 `moon` 命令在此目录执行

#### moon.pkg.json（包定义）

```json
{
  "is-main": true,
  "import": [
    {
      "path": "your_username/hello-moonbit",
      "alias": "lib"
    }
  ]
}
```

**关键点**：
- **每个目录**都是一个 Package
- `is-main: true` 表示这是可执行入口包

### 构建与运行

```bash
# 检查代码
moon check

# 运行程序
moon run cmd/main
```

---

## Part 2: 基本类型速查表

### 标量类型

| 类型 | 说明 | 示例 | 值范围 |
|------|------|------|--------|
| Int | 32 位有符号整数（默认） | `42` | -2³¹ ~ 2³¹-1 |
| Int64 | 64 位有符号整数 | `1000L` | -2⁶³ ~ 2⁶³-1 |
| UInt / UInt64 | 无符号整数 | `14U` / `14UL` | - |
| Double | 64 位浮点数（默认） | `3.14` | ~15-17 位有效数字 |
| Float | 32 位浮点数 | `(3.14 : Float)` | - |
| Bool | 布尔值 | `true`, `false` | true / false |
| Char | Unicode 字符 | `'A'`, `'兔'` | 单个字符 |
| String | UTF-16 字符串 | `"Hello"` | UTF-16 文本 |
| Byte | ASCII 字节 | `b'a'` | - |
| BigInt | 任意精度整数 | `9876543210N` | 无限制 |

### 特殊类型

| 类型 | 说明 | 示例 |
|------|------|------|
| Unit | 无有意义值的类型（类似 void） | `()` |

### 数字字面量格式

```moonbit
// 十进制（支持下划线分隔）
let a = 1_000_000

// 二进制
let bin = 0b110010

// 八进制
let octal = 0o1234

// 十六进制
let hex = 0XA_B_C

// 浮点数
let double = 3.14
let hex_double = 0x1.2P3  // (1.0 + 2/16) * 2^3 = 9
```

### 重载字面量

当期望的类型已知时，MoonBit 可以**自动重载字面量**：

```moonbit
let int : Int = 42        // 默认 Int
let uint : UInt = 42       // 可重载为 UInt
let double : Double = 42   // 或 Double
```

---

## Part 3: 自定义数据结构

### 结构体 (Struct)

```moonbit
struct Point {
  x: Int
  y: Int
}

// 构造
let p = Point::{ x: 1, y: 2 }

// 更新（复制并修改）
let p2 = { ..p, x: 10 }
```

### 枚举 (Enum)

```moonbit
enum Color {
  Red
  Green
  Blue
  RGB(Int, Int, Int)
  Hex(String~)  // 带标签参数
}

let c1 = Red
let c2 = RGB(255, 0, 0)
let c3 = Hex(hex="#FF0000")
```

### 元组 (Tuple)

```moonbit
let tuple = (1, "hello", true)
let (a, b, c) = tuple  // 解构
let x = tuple.0         // 索引访问
```

### 元组结构体

```moonbit
struct Pair(Int, String)

let pair = Pair(42, "answer")
let (num, str) = pair  // 解构
```

### 类型别名与本地类型

```moonbit
type UserId = Int           // 类型别名

fn local_types() {
  type LocalState = { count: Int }  // 本地类型（仅在函数内可见）
}
```

---

## Part 4: Option/Result 类型

### Option[T] — 可能缺失的值

```moonbit
// Option[T] 表示可能缺失的值（可缩写为 T?）
let a : Int? = None
let b : Option[Int] = Some(42)

match a {
  Some(x) => println(x.to_string())
  None => println("None")
}
```

### Result[T, E] — 成功或错误

```moonbit
// Result[T, E] 表示成功(T)或错误(E)
let c : Result[Int, String] = Ok(42)
let d : Result[Int, String] = Err("error")

match may_fail() {
  Ok(v) => println(v.to_string())
  Err(e) => handle_error(e)
}
```

---

## Part 5: 集合类型

### 数组 (Array)

```moonbit
let arr = [1, 2, 3, 4]          // Array[T]: 可增长
let fixed : FixedArray[Int] = [1, 2, 3]  // FixedArray[T]: 固定大小

arr[0]                           // 索引访问
arr[2:]                          // ArrayView 切片
arr[3] = 5                       // 修改元素
```

### ArrayView (切片)

类似于其他语言中的 `slice`：

```moonbit
test {
  let xs = [0, 1, 2, 3, 4, 5]
  let s1 : ArrayView[Int] = xs[2:]       // [2, 3, 4, 5]
  inspect(xs[:4], content="[0, 1, 2, 3]")  // [0, 1, 2, 3]
  inspect(xs[2:5], content="[2, 3, 4]")   // [2, 3, 4]
}
```

### Map (有序哈希表)

```moonbit
let map : Map[String, Int] = {
  "x": 1,
  "y": 2,
  "z": 3
}
```

### Ref (可变引用)

```moonbit
let a : Ref[Int] = { val: 100 }

test {
  a.val = 200
  assert_eq(a.val, 200)
  a.val += 1
  assert_eq(a.val, 201)
}
```

### JSON 支持

通过重载字面量方便地处理 JSON：

```moonbit
let json_example : Json = {
  "import": ["moonbitlang/core/builtin"],
  "test-import": ["moonbitlang/core/random"],
}
```

### 字符串操作

```moonbit
fn main {
  let s = "Hello, MoonBit!"

  // 字符串长度
  println(s.length().to_string())

  // 字符串插值
  let name = "World"
  let greeting = "Hello, \(name)!"

  // 字符串拼接
  let combined = "Hello" + " " + "World"
}
```

---

## Part 6: 核心语法速查

### 6.1 变量与可变性

MoonBit 采用静态类型系统，支持类型推断，变量默认不可变：

```moonbit
fn main {
  // 不可变变量（默认）
  let message = "Hello MoonBit"  // 自动推断为 String
  let answer: Int = 42           // 显式类型标注

  // 可变变量
  let mut counter = 0
  counter += 1
}
```

| 特性 | 语法 | 说明 |
|------|------|------|
| 不可变 | `let x = 5` | 默认，不可重新赋值 |
| 可变 | `let mut x = 5` | 使用 `mut` 关键字 |
| 类型标注 | `let x: Int = 5` | 显式指定类型 |

### 6.2 函数定义

```moonbit
// 基本函数
fn add(a: Int, b: Int) -> Int {
  a + b
}

// 多参数函数
fn greet(name: String, age: Int) -> String {
  "Hello, \(name)! You are \(age) years old."
}

// 无返回值函数（返回 Unit）
fn print_hello() -> Unit {
  println("Hello, world!")
}

// 带类型参数的函数（泛型）
fn[T] identity(x: T) -> T {
  x
}
```

### 6.3 控制流

#### if 表达式

MoonBit 的 `if` 是表达式，有返回值：

```moonbit
fn abs(x: Int) -> Int {
  if x >= 0 { x } else { -x }
}

// if 作为表达式赋值
let value = if x > 10 { 1 } else { 0 }
```

#### while 循环

```moonbit
fn sum_to(n: Int) -> Int {
  let mut sum = 0
  let mut i = 1
  while i <= n {
    sum += i
    i += 1
  }
  sum
}
```

#### for 循环

```moonbit
fn main {
  // 范围遍历
  for i in 0..5 {
    println(i.to_string())
  }

  // 数组遍历
  let arr = [1, 2, 3]
  for x in arr {
    println(x.to_string())
  }
}
```

### 6.4 运算符

| 类别 | 运算符 |
|------|--------|
| 算术 | `+`, `-`, `*`, `/`, `%` |
| 比较 | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| 逻辑 | `&&`, `\|\|`, `not()` |
| 位运算 | `&`, `\|`, `^`, `<<`, `>>` |
| 字符串插值 | `\(expr)` |

### 6.5 注释

```moonbit
// 单行注释

/// 文档注释（用于函数/类型文档）
/// 计算两个数的和
fn add(a: Int, b: Int) -> Int { a + b }
```

### 6.6 模式匹配速查

#### 基本模式

```moonbit
match value {
  0 => "zero"
  1 => "one"
  n => "other: \(n)"
}
```

#### 数组/范围/Map/JSON 模式

```moonbit
match arr {
  [] => "empty"
  [x] => "single"
  [head, ..rest] => "head + rest"
}

match score {
  90..100 => "A"
  70..89 => "B"
  _ => "F"
}
```

#### 守卫条件

```moonbit
match option {
  Some(x) if x > 0 => "positive: \(x)"
  Some(x) => "non-positive: \(x)"
  None => "none"
}
```

---

## Part 6.5: 可见性实战 ⭐v6.0新增

> 来自 mbtgraph（MoonBit 图算法库）生产项目的可见性决策经验

### 可见性层级速查

MoonBit 有 **3 级可见性**（结构体/枚举）和 **2 级可见性**（Trait）：

```
priv（默认） < pub（只读） < pub(all)（完全公开）

pub trait（密封） < pub(open) trait（开放）
```

**结构体/枚举可见性**：

```moonbit
// 私有：仅本包可访问
struct InternalType { ... }

// 公开但只读：外部可读字段，不能构造
pub struct ReadOnly { x : Int }

// 完全公开：外部可以构造和修改
pub(all) struct FullyPublic { x : Int }
```

**Trait 可见性**：

```moonbit
// 密封 trait：仅本包内可实现
pub trait SealedTrait { fn method(self) -> Int }

// 开放 trait：任何包都可以实现
pub(open)trait OpenTrait { fn method(self) -> Int }
```

### 生产项目可见性决策表

来自 mbtgraph 图算法库的真实决策记录：

| 场景 | 选择 | 原因 |
|------|------|------|
| 核心类型 (NodeId, Node, Edge) | `pub(all) struct` | 存储实现需要构造这些类型 |
| 错误类型 (GraphError) | `pub(all) enum` | 外部包需要构造 Error 变体返回 |
| 图 trait (GraphReadable 等) | `pub(open)trait` | 存储包需要在外部实现这些 trait |
| 内部辅助结构 | `priv struct` / `pub struct` | 不需要外部访问 |

**关键规则**：
- 外部包需要**构造**某个类型 → 必须用 `pub(all)`
- 外部包需要**实现**某个 trait → 必须用 `pub(open)trait`
- 只需外部**读取** → 用 `pub` 即可

### Option 与 Result 实战技巧

**Option 匹配不需要通配分支**：
```moonbit
let value : Int? = Some(42)
match value {
  Some(x) => println(x)
  None => println("empty")
  // ✅ Option 只有 Some/None 两个变体，不需要 _ => ()
}
```

**Result 处理与忽略 Unit 值**：
```moonbit
fn may_fail() -> Result[Int, GraphError] {
  Ok(42)
}

match may_fail() {
  Ok(v) => println(v)
  Err(e) => handle_error(e)
}

// 丢弃 Ok(()) 的 Unit 值
@core.GraphWritable::add_node(g, data) |> ignore   // 丢弃成功结果
```

### Tuple 解构注意事项

**基本解构**：
```moonbit
let pair = (1, "hello")
let (a, b) = pair   // a = 1, b = "hello"
```

**⚠️ For 循环不支持元组解构**：
```moonbit
// ❌ 错误：MoonBit 不支持这种写法
for (f, t, w) in g.edges() { ... }

// ✅ 正确：先绑定，再 match 解构
for triple in g.edges() {
  match triple {
    (f, t, w) => do_something(f, t, w)
    _ => ()    // 注意：元组类型可能需要通配分支
  }
}
```

**Match 中的元组解构**：
```moonbit
for entry in self.adj[idx] {
  match entry {
    (nid, w) => {
      // nid: NodeId, w: Double
      r.push(nid)
    }
    // 如果编译器能推断穷尽性，则不需要 _
  }
}
```

### 泛型函数语法注意

```moonbit
// 泛型函数定义：[T] 放在函数名前
pub fn[G : GraphReadable] to_adjacency_list(g : G) -> AdjacencyList { ... }

// 调用时自动推断类型参数
to_directed_adj_list(my_graph)   // G 自动推断
```

**⚠️ 注意**：旧语法 `fn to_xxx[T](...)` 已废弃，新语法为 `fn[T] to_xxx(...)` 或 `fn to_xxx[T](...)`。

---

## 附录：快速示例

### 库函数示例

```moonbit
/// 计算斐波那契数列第 n 项
/// 采用迭代算法，时间复杂度 O(n)，空间复杂度 O(1)
pub fn fib(n: Int) -> Int {
  if n <= 0 {
    return 0
  }
  let mut a = 0
  let mut b = 1
  for _ in 1..n {
    let c = a + b
    a = b
    b = c
  }
  b
}

/// 问候函数
pub fn greet(name: String) -> String {
  "Hello, \(name)!"
}
```

### 主程序入口

```moonbit
fn main {
  println("Hello, MoonBit!")
  println("Fibonacci(10) = \{@lib.fib(10)}")
  println(@lib.greet("World"))
}
```

### 运行结果预期

```
Hello, MoonBit!
Fibonacci(10) = 55
Hello, World!
```

---

*文档版本: v1.0.0 | 整合自: moonbit-quickstart v5.0.0 + moonbit-data-types v6.0.0*
*最后更新: 2026-05-17*
