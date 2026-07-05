# MoonBit 类型系统参考手册 📖

> **来源**：[moonbit-functional/SKILL.md](../skills/layer1-foundation-path/moonbit-functional/SKILL.md) Part 1-2 (v8.0.0)
>
> **用途**：深入理解 MoonBit 类型系统、函数式编程特性和高阶函数
> **定位**：类型系统与函数式编程参考文档（进阶学习）

---

## Part 1: 核心语法基础 🆕 (来自官方 fundamentals 文档)

### 1.1 内置数据类型

#### 基本类型

| 类型 | 描述 | 示例 |
|------|------|------|
| `Int` | 32 位有符号整数 | `42` |
| `Int64` | 64 位有符号整数 | `1000L` |
| `UInt` | 32 位无符号整数 | `14U` |
| `UInt64` | 64 位无符号整数 | `14UL` |
| `Double` | 64 位浮点数 | `3.14` |
| `Float` | 32 位浮点数 | `(3.14 : Float)` |
| `Bool` | 布尔值 | `true`, `false` |
| `String` | UTF-16 字符串 | `"Hello"` |
| `Char` | Unicode 码点 | `'A'`, `'兔'` |
| `Byte` | ASCII 字节 | `b'a'` |
| `BigInt` | 大整数 | `10000000000000000000000N` |

#### 数字字面量格式

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

#### 重载字面量

当期望的类型已知时，MoonBit 可以**自动重载字面量**：

```moonbit
let int : Int = 42
let uint : UInt = 42
let int64 : Int64 = 42
let double : Double = 42
let float : Float = 42
let bigint : BigInt = 42
```

### 1.2 内置数据结构

#### Unit 类型

`Unit` 表示无意义的值，类似 `void` 但是一等类型：

```moonbit
fn print_hello() -> Unit {
  println("Hello, world!")
}
```

#### 元组 (Tuple)

```moonbit
fn pack(a: Bool, b: Int, c: String) -> (Bool, Int, String, Double) {
  (a, b, c, 3.14)
}

fn main {
  let quad = pack(false, 100, "text", 3.14)
  let (bool_val, int_val, str, float_val) = quad  // 解构

  // 通过索引访问
  let x2 = quad.0
  let y2 = quad.1
}
```

#### Ref (可变引用)

```moonbit
let a : Ref[Int] = { val: 100 }

test {
  a.val = 200
  assert_eq(a.val, 200)
  a.val += 1
  assert_eq(a.val, 201)
}
```

#### Option 和 Result

```moonbit
test {
  // Option[T] 表示可能缺失的值，可缩写为 T?
  let a : Int? = None
  let b : Option[Int] = Some(42)

  // Result[T, E] 表示成功(T)或错误(E)
  let c : Result[Int, String] = Ok(42)
  let d : Result[Int, String] = Err("error")

  match a {
    Some(_) => assert_true(false)
    None => assert_true(true)
  }
}
```

#### 数组 (Array)

```moonbit
let numbers = [1, 2, 3, 4]

test {
  let a = numbers[2]      // 索引访问（从 0 开始）
  numbers[3] = 5          // 修改元素
  let b = a + numbers[3]
  assert_eq(b, 8)
}

// Array[T]: 可增长数组
// FixedArray[T]: 固定大小数组
let fixed_array : FixedArray[Int] = [1, 2, 3]
```

#### ArrayView (切片)

类似于其他语言中的 `slice`：

```moonbit
test {
  let xs = [0, 1, 2, 3, 4, 5]
  let s1 : ArrayView[Int] = xs[2:]       // [2, 3, 4, 5]
  inspect(xs[:4], content="[0, 1, 2, 3]")  // [0, 1, 2, 3]
  inspect(xs[2:5], content="[2, 3, 4]")   // [2, 3, 4]
}
```

#### Map (有序哈希表)

```moonbit
let map : Map[String, Int] = {
  "x": 1,
  "y": 2,
  "z": 3
}
```

#### JSON 支持

通过重载字面量方便地处理 JSON：

```moonbit
let json_example : Json = {
  "import": ["moonbitlang/core/builtin"],
  "test-import": ["moonbitlang/core/random"],
}
```

### 1.3 自定义数据类型

#### 结构体 (Struct)

```moonbit
struct Point {
  x: Int
  y: Int
}

// 简写构造
let p = Point::{ x: 1, y: 2 }

// 更新语法
let p2 = { ..p, x: 10 }  // 复制 p 并修改 x
```

#### 枚举 (Enum)

```moonbit
enum Color {
  Red
  Green
  Blue
  RGB(Int, Int, Int)     // 带参数的构造器
  Hex(String~)           // 带标签参数
}

let c1 = Red
let c2 = RGB(255, 0, 0)
let c3 = Hex(hex="#FF0000")
```

#### 元组结构体

```moonbit
struct Pair(Int, String)

let pair = Pair(42, "answer")
let (num, str) = pair  // 解构
```

#### 类型别名与本地类型

```moonbit
type UserId = Int  // 类型别名

fn local_types() {
  type LocalState = { count: Int }  // 本地类型（仅在函数内可见）
}
```

### 1.4 函数系统 🆕

#### 顶层函数

```moonbit
fn add3(x: Int, y: Int, z: Int) -> Int {
  x + y + z
}
// 注意：顶层函数需要显式类型注释
```

#### 局部函数（命名和匿名）

```moonbit
fn local_demo() -> Int {
  // 命名局部函数（可省略类型注释）
  fn inc(x) {
    x + 1
  }

  // 匿名函数立即应用
  (fn(x) { x + inc(2) })(6)
}
```

#### 箭头函数

```moonbit
fn main {
  [1, 2, 3].eachi((i, x) => println("\(i) => \(x)"))
  [1, 2, 3].each(x => println(x * x))  // 单参数省略括号
}
```

#### 闭包（词法闭包）

```moonbit
let global_y = 3

fn demo_closure(x: Int) -> (Int, Int) {
  fn inc() { x + 1 }         // 捕获外部变量 x
  fn four() { global_y + 1 } // 捕获全局变量
  (inc(), four())
}
```

#### 互递归局部函数

```moonbit
letrec even = x => x == 0 || odd(x - 1)
and odd = x => x != 0 && even(x - 1)
```

#### 函数应用与部分应用

```moonbit
// 普通应用
add3(1, 2, 7)

// 部分应用：使用 _ 占位符
fn add(x: Int, y: Int) -> Int { x + y }
let add10 : (Int) -> Int = add(10, _)  // 返回新函数
```

#### 带标签参数与可选参数

```moonbit
fn labeled_example(
  required: Int,
  optional~: Int = 10,          // 可选参数（带默认值）
  no_default?: Int,             // 无默认值的可选参数
) -> Int {
  required + optional + no_default.unwrap_or(0)
}

// 调用时可以使用标签
labeled_example(1, optional=20, no_default=Some(30))
```

#### 自动填充参数

```moonbit
#callsite(autofill(loc))
pub fn[T] fail(msg: String, loc~: SourceLoc) -> T raise Failure {
  raise Failure("FAILED: \(loc) \(msg)")
}
```

#### 函数别名

```moonbit
type FnAlias = (Int) -> Int  // 函数类型别名
```

### 1.5 控制结构 🆕

#### 条件表达式

```moonbit
let abs_x = if x >= 0 { x } else { -x }
```

#### 匹配表达式 (Match)

```moonbit
match value {
  Some(x) => println(x.to_string())
  None => println("None")
}
```

#### 卫语句 (Guard)

```guard
guard condition else {
  // 条件不满足时执行
  return error_value
}
// 继续执行...
```

#### 循环

```moonbit
// While 循环
while condition { ... }

// For 循环
for i = 0; i < n; i = i + 1 { ... }

// for..in 循环（迭代器）
for x in array { ... }

// 函数式循环
array.map(fn(x) { ... })

// 带标记的 Continue/Break
'outer: for i in 0..10 {
  for j in 0..10 {
    if some_condition { continue 'outer }
    if other_condition { break 'outer }
  }
}
```

#### defer 表达式

```moonbit
fn process_file() {
  let file = open_file("test.txt")
  defer file.close()  // 函数返回前自动执行
  // ... 使用 file ...
}
```

### 1.6 模式匹配 🆕

#### 简单模式

```moonbit
match value {
  0 => "zero"
  1 => "one"
  n => "other: \(n)"
}
```

#### 数组模式

```moonbit
match arr {
  [] => "empty"
  [x] => "single: \(x)"
  [x, y] => "pair: \(x), \(y)"
  [head, ..rest] => "head: \(x), rest: ..."
}
```

#### 范围模式

```moonbit
match score {
  90..100 => "A"
  80..89 => "B"
  70..79 => "C"
  _ => "F"
}
```

#### Map 模式

```moonbit
match map {
  { "x": x, "y": y } => "point: (\(x), \(y))"
  _ => "other map"
}
```

#### JSON 模式

```moonbit
match json_value {
  { "name": name, "age": age } => "user: \(name), \(age)"
  _ => "other json"
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

### 1.7 特殊语法 🆕

#### 管道操作符

```moonbit
let result = value
  |> transform1
  |> transform2
  |> final_transform
```

#### 级联运算符

```moonbit
logger
  ..write_string("(")
  ..write_object(a)
  ..write_string(", ")
  ..write_object(b)
  ..write_string(")")
```

#### is 表达式

```moonbit
if value is Some(x) {
  // x 已绑定到 Some 的内部值
  println(x.to_string())
}
```

#### 展开运算符

```moonbit
let base = { x: 1, y: 2 }
let extended = { ..base, z: 3 }  // 展开并扩展
```

#### TODO 语法

```moonbit
fn incomplete_function() -> Int {
  TODO()  // 编译通过但运行时报错
}
```

---

## Part 2: 高阶函数

### 2.1 数组迭代方法速查表

| 方法 | 签名 | 说明 |
|------|------|------|
| `map` | `map(f) -> Array[U]` | 映射转换 |
| `filter` | `filter(f) -> Array[T]` | 过滤筛选 |
| `fold` | `fold(init, f) -> U` | 折叠聚合 |
| `each` | `each(f) -> Unit` | 遍历执行 |
| `find` | `find(f) -> Option[T]` | 查找元素 |
| `find_index` | `find_index(f) -> Option[Int]` | 查找索引 |
| `all` | `all(f) -> Bool` | 全部满足 |
| `any` | `any(f) -> Bool` | 任一满足 |

### 2.2 使用示例

```moonbit
fn main {
  let numbers = [1, 2, 3, 4, 5]

  // 链式调用
  let result = numbers
    .filter(x => x % 2 == 0)     // [2, 4]
    .map(x => x * x)             // [4, 16]
    .fold(0, (acc, x) => acc + x) // 20

  println(result.to_string())  // 20
}
```

### 2.3 函数组合与偏应用

```moonbit
// 函数组合
fn compose[A, B, C](f: (B) -> C, g: (A) -> B) -> (A) -> C {
  fn(x) { f(g(x)) }
}

// 偏应用
fn add(a: Int, b: Int) -> Int { a + b }
let add5 = fn(x) { add(5, x) }  // 偏应用
```

---

## 附录：类型系统核心概念总结

### MoonBit 类型系统特点

1. **静态类型**：编译时类型检查，支持类型推断
2. **强类型**：严格的类型安全，避免隐式转换
3. **代数数据类型 (ADT)**：struct 和 enum 支持复杂的类型组合
4. **泛型编程**：支持泛型函数和泛型类型
5. **Trait 系统**：结构性 Trait，支持隐式实现
6. **模式匹配**：强大的解构和模式匹配能力
7. **不可变默认**：变量默认不可变，鼓励函数式风格

### 函数式编程特性

1. **一等函数**：函数可以作为值传递和返回
2. **闭包**：词法作用域的闭包支持
3. **高阶函数**：map/filter/fold 等标准迭代器方法
4. **部分应用**：使用 `_` 占位符创建偏应用函数
5. **管道操作符**：`|>` 支持链式函数调用
6. **纯函数鼓励**：不可变性和表达式导向的设计

---

*文档版本: v1.0.0 | 来源: moonbit-functional SKILL.md Part 1-2 (v8.0.0)*
*最后更新: 2026-05-17*
