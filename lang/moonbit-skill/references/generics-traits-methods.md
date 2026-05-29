# 泛型编程、Trait 系统、方法与派生宏 — 完整参考手册

> **来源**: `moonbit-functional/SKILL.md` v8.0.0 | **迁移日期**: 2026-05-17
> **原始位置**: `skills/layer1-foundation-path/moonbit-functional/SKILL.md`
> **本文件涵盖**: Part 1 ~ Part 7 全部内容，含 v6/v7/v8 增强部分

---

## Part 1: 核心语法基础 (来自官方 fundamentals 文档)

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

### 1.4 函数系统

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

### 1.5 控制结构

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

### 1.6 模式匹配

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

### 1.7 特殊语法

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

## Part 3: 泛型编程 ⚡ v6.0 库级增强

> 本部分是编写 MoonBit 语言库的核心能力。涵盖泛型类型参数、Trait 完整体系（可见性/继承/默认实现）、以及实用的库级设计模式。

### 3.1 泛型函数与泛型类型

#### 基本语法

```moonbit
// 泛型函数：类型参数在函数名前
fn[T] identity(x : T) -> T { x }

// 多个类型参数
fn[A, B] make_pair(a : A, b : B) -> (A, B) { (a, b) }

// 泛型结构体
struct Box[T] {
  value : T
}

// 泛型枚举
enum Option[T] {
  None
  Some(T)
}

// 泛型元组结构体
struct Pair[A, B](A, B)
```

#### 泛型函数调用

```moonbit
// 类型推断：编译器自动推导 T = Int
let x = identity(42)

// 显式指定类型参数
let y : String = identity[String]("hello")

// 部分应用返回新函数
let id_int : (Int) -> Int = identity[Int]
```

### 3.2 Trait 系统完整体系

> Trait 是 MoonBit 抽象能力的核心，也是设计高质量库 API 的关键工具。

#### 3.2.1 定义 Trait

```moonbit
// 基本 Trait 定义：使用 Self 指代实现该 trait 的类型
trait Show {
  to_string(Self) -> String
}

// 带超特征的 Trait（继承）
trait Compare : Eq {          // Compare 继承自 Eq
  compare(Self, Self) -> Int   // 返回 -1/0/1
}

// 公开 Trait：外部可见名称和方法签名
pub(open) trait Display {
  display(Self, &Logger) -> Unit
}

// 只读 Trait：外部可查看但不可实现
pub(readonly) trait Inspectable {
  inspect_fields(Self) -> Map[String, String]
}
```

**Trait 可见性等级**：

| 可见性 | 声明方式 | 外部可见 | 外部可实现 |
|--------|---------|---------|-----------|
| 私有 | `priv trait` | ❌ | ❌ |
| 抽象（默认）| `trait` | ✅ 仅名称 | ❌ |
| 只读 | `pub(readonly) trait` | ✅ 名称+方法 | ❌ |
| 完全公开 | `pub(open) trait` | ✅ 全部 | ✅ |

#### 3.2.2 Trait 超特征继承

```moonbit
// 单继承
trait Ord : Compare { ... }       // Ord 继承 Compare

// 多重继承（使用 + 号）
pub(open) trait Shape : Position + Draw + Debug {}

// 具体示例
pub(open) trait Position {
  pos(Self) -> (Int, Int)
}

pub(open) trait Draw {
  draw(Self, Canvas) -> Unit
}

pub(open) trait Movable : Position + Draw {
  move_to(Self, Int, Int) -> Self
}
```

#### 3.2.3 实现 Trait 的两种方式

**方式一：隐式实现（定义方法即可）**

MoonBit 是**结构性 Trait 系统**——只要类型提供了 Trait 要求的所有方法，就自动实现了该 Trait。

```moonbit
struct Point { x : Int, y : Int }

// 定义了 to_string 方法 → 自动实现 Show
fn Point::to_string(self : Point) -> String {
  "Point(\(self.x), \(self.y))"
}

// 定义了 op_equal 方法 → 自动实现 Eq
fn Point::op_equal(self : Point, other : Point) -> Bool {
  self.x == other.x && self.y == other.y
}

// 定义了 compare 方法 → 自动实现 Compare（因为已有 Eq）
fn Point::compare(self : Point, other : Point) -> Int {
  if self.x != other.x { self.x - other.x }
  else { self.y - other.y }
}
```

**方式二：显式实现（impl 语法）**

显式 `impl` 提供更清晰的签名信息，且支持为 Trait 提供**默认实现**：

```moonbit
// 为具体类型实现 Trait
impl Show for Point with to_string(self) {
  "Point(\(self.x), \(self.y))"
}

// 为泛型类型实现 Trait
impl[X : Show] Show for Array[X] with to_string(self) {
  "[" + self.map(fn(x) { X::to_string(x) }).join(", ") + "]"
}

// 为 Trait 提供默认实现
impl Show with to_string(self) {
  // 默认使用 debug 输出
  @debug.to_string(self)
}
```

**两种方式的对比**：

| 特性 | 隐式实现 (`fn Type::method`) | 显式实现 (`impl Trait for Type`) |
|------|---------------------------|-------------------------------|
| 位置要求 | 必须在 Type 所在包 | Type 或 Trait 所在包（孤立规则）|
| 编译器推断 | ✅ 自动识别 | ✅ 明确声明 |
| 默认实现 | ❌ 不支持 | ✅ 支持 |
| 泛型 impl | ❌ 不支持 | ✅ 支持 `impl[X]` |
| 推荐场景 | 简单类型 | 库 API、复杂抽象 |

#### 3.2.4 Trait 默认实现

```moonbit
pub(open) trait J {
  f(Self) -> Unit              // 必须由实现者提供
  f_twice(Self) -> Unit         // 有默认实现
}

// 为 Trait 自身提供默认实现
impl J with f_twice(self) {
  self.f()
  self.f()
}

// 实现 J 时只需提供 f()，f_twice 使用默认值
struct MyType(Int)
impl J for MyType with f(self) {
  println("f called: \(self.0)")
}

// 也可以覆盖默认实现
impl J for MyType with f_twice(self) {
  println("custom twice!")
  self.f()
  self.f()
}
```

**v0.9 新增**: Trait 方法支持可选参数

```moonbit
pub(open) trait Reader {
  async read(Self, buf : FixedArray[Byte], offset? : Int, len? : Int) -> Unit
}

// 不同 impl 可以定义不同的默认值或选择不提供
impl Reader for FileImpl with read(self, buf, offset?, len?) {
  let off = offset.unwrap_or(0)
  let ln = len.unwrap_or(buf.length())
  // ...
}
```

#### 3.2.5 孤立规则 (Orphan Rule)

MoonBit 遵循孤立规则：`impl Trait for Type` 必须在 **Type 或 Trait 所在的包中**。

```moonbit
// ✅ 合法：在 Point 所在包中
impl Show for Point with to_string(self) { ... }

// ✅ 合法：在 Show Trait 所在包中
impl Show for ExternalType with to_string(self) { ... }

// ❌ 非法：在第三方包中同时为外部 Type 和外部 Trait 做 impl
// （解决方案：使用 newtype 包装 或 本地私有方法扩展）
```

### 3.3 类型约束 (Trait Bounds)

> 类型约束是泛型编程的核心机制，用于限定类型参数必须满足的能力。

#### 基本约束语法

```moonbit
// 单一约束：T 必须实现 Show
fn[T : Show] print_value(value : T) -> Unit {
  println(value.to_string())
}

// 多约束：T 必须同时实现 Show 和 Eq
fn[T : Show + Eq] print_and_compare(a : T, b : T) -> Unit {
  println("\(a.to_string()) vs \(b.to_string())")
  if a == b { println("equal!") }
}

// 多类型参数各有约束
fn[A : Show, B : Eq] process(a : A, b : B) -> String {
  a.to_string()
}
```

#### 在约束内调用 Trait 方法

```moonbit
// 约束后可直接用 T::method_name 调用
fn[T : Compare] max_pair(a : T, b : T) -> T {
  if T::compare(a, b) >= 0 { a } else { b }
}

// 也可以用点语法（当 self 是第一个参数时）
fn[T : Show] show_all(values : Array[T]) -> String {
  values.map(fn(v) { v.to_string() }).join(", ")
}
```

#### 约束的实际应用：通用数据结构

```moonbit
// 泛型栈：需要 Default 来创建初始容量
struct Stack[T] {
  data : Array[T]
  top : Int
}

fn[T : Default] Stack::new(capacity : Int) -> Stack[T] {
  Stack::{ data: Array::make(capacity, T::default()), top: 0 }
}

fn[T] Stack::push(self : Stack[T], value : T) -> Stack[T] {
  self.data[self.top] = value
  { ..self, top: self.top + 1 }
}

fn[T] Stack::pop(self : Stack[T]) -> Option[(T, Stack[T])] {
  if self.top == 0 { None }
  else { Some((self.data[self.top - 1], { ..self, top: self.top - 1 })) }
}
```

#### 约束的实际应用：排序算法

```moonbit
// 通用快速排序：需要 Compare 约束
fn[T : Compare] quick_sort(arr : Array[T]) -> Array[T] {
  if arr.length <= 1 { return arr }
  let pivot = arr[arr.length / 2]
  let mut left : Array[T] = []
  let mut middle : Array[T] = []
  let mut right : Array[T] = []
  for elem in arr {
    let c = T::compare(elem, pivot)
    if c < 0 { left.push(elem) }
    else if c > 0 { right.push(elem) }
    else { middle.push(elem) }
  }
  quick_sort(left) + middle + quick_sort(right)
}

// 使用：任何实现了 Compare 的类型都能排序
test {
  let nums = [3, 1, 4, 1, 5, 9, 2, 6]
  assert_eq(quick_sort(nums), [1, 1, 2, 3, 4, 5, 6, 9])
}
```

### 3.4 库级设计模式

#### 模式一：Builder 模式（链式 API）

```moonbit
struct QueryConfig[T] {
  table : String
  filters : Array[(String, T)]
  limit : Int?
  offset : Int?
}

fn[T] QueryConfig::new(table : String) -> QueryConfig[T] {
  QueryConfig::{ table: table, filters: [], limit: None, offset: None }
}

fn[T] QueryConfig::where_eq(self : QueryConfig[T], column : String, value : T) -> QueryConfig[T] {
  { ..self, filters: self.filters.push((column, value)) }
}

fn[T] QueryConfig::with_limit(self : QueryConfig[T], limit : Int) -> QueryConfig[T] {
  { ..self, limit: Some(limit) }
}

// 使用
let query = QueryConfig[String]
  ::new("users")
  .where_eq("status", "active")
  .where_eq("role", "admin")
  .with_limit(100)
```

#### 模式二：策略模式（通过 Trait 约束）

```moonbit
// 定义策略接口
pub(open) trait SortStrategy[T] {
  sort(Array[T]) -> Array[T]
}

// 不同策略实现
struct AscendingOrder {}
impl[T : Compare] SortStrategy[T] for AscendingOrder with sort(arr) {
  quick_sort(arr)
}

struct DescendingOrder {}
impl[T : Compare] SortStrategy[T] for DescendingOrder with sort(arr) {
  reverse(quick_sort(arr))
}

// 使用策略的函数
fn[T : Compare, S : SortStrategy[T]] execute_sort(data : Array[T], strategy : S) -> Array[T] {
  S::sort(data)
}
```

#### 模式三：Newtype 模式（类型安全包装）

```moonbit
// 用 Newtype 包装基础类型以获得类型安全
struct UserId(Int)
struct OrderId(Int)
struct ProductId(Int)

// 防止混淆不同类型的 ID
fn find_user(id : UserId) -> User { ... }
fn find_order(id : OrderId) -> Order { ... }

// 通过派生自动获得能力
derive(UserId: Eq, Compare, Hash, Debug)
derive(OrderId: Eq, Compare, Hash, Debug)
derive(ProductId: Eq, Compare, Hash, Debug)
```

#### 模式四：Trait 组合（小型 Trait 组合大型能力）

```moonbit
// 小而聚焦的 Trait
pub(open) trait Cloneable {
  clone(Self) -> Self
}

pub(open) trait Serializable {
  serialize(Self) -> Bytes
  deserialize(Bytes) -> Self
}

// 组合 Trait
pub(open) trait Persistent : Cloneable + Serializable {
  save(Self, Path) -> Unit
  load(Path) -> Self
}
```

#### 模式五：using 导入（v0.6.29+ 统一导入语法）

```moonbit
// using 统一 fnalias、traitalias 和 typealias
using @my_lib {
  my_function,
  MY_CONSTANT,
  type MyType,
  trait MyTrait,
}

// pub using 用于重新导出
pub using @internal_utils {
  type InternalHelper,
}
```

### 3.5 内建 Trait 速查表

| Trait | 方法 | 说明 | 可派生 |
|-------|------|------|--------|
| `Eq` | `op_equal(Self, Self) -> Bool` | 相等性比较 | ✅ `derive(Eq)` |
| `Compare : Eq` | `compare(Self, Self) -> Int` | 排序比较 (-1/0/1) | ✅ `derive(Compare)` |
| `Hash` | `hash_combine(Self, Hasher)` / `hash(Self) -> Int` | 哈希支持 | ✅ `derive(Hash)` |
| `Show` | `output(Self, Logger)` / `to_string(Self) -> String` | 字符串化 | ✅ `derive(Show)` |
| `Debug` | 结构化调试输出 | 调试用途 | ✅ `derive(Debug)` |
| `Default` | `default() -> Self` | 默认值 | ✅ `derive(Default)` |
| `Add` | `add(Self, Self) -> Self` | 加法运算符 | ❌ 手动 |
| `Sub` | `sub(Self, Self) -> Self` | 减法运算符 | ❌ 手动 |
| `Mul` | `mul(Self, Self) -> Self` | 乘法运算符 | ❌ 手动 |
| `Div` | `div(Self, Self) -> Self` | 除法运算符 | ❌ 手动 |

**Trait 继承关系**：
```
Ord ──→ Compare ──→ Eq
                    ↓
               Hash (独立)
                    ↓
Show / Debug (独立)
Default (独立)
```

---

## Part 3.5: 高级应用模式 ⭐ v7.0 新增

> 本部分展示如何将函数式编程特性应用于真实世界的高级场景。基于 [MoonBash](https://github.com/Haoxincode/MoonBash)（POSIX Shell 解释器）和 [morm](https://github.com/oboard/morm)（ORM 库）两个开源项目的实践经验。

### 3.5.1 编译器/解释器管道模式（来自 MoonBash）

**核心思想**：使用 ADT（代数数据类型）+ 模式匹配实现标准的编译器前端：`Lexer → Parser → AST → Evaluator`

#### Token 类型定义（ADT）

```moonbit
enum Token {
  // 关键字
  KwIf
  KwElse
  KwFn
  KwLet
  KwMatch
  // 字面量
  LitInt(Int)
  LitString(String~)
  LitBool(Bool)
  // 标识符
  Ident(String~)
  // 运算符
  Plus
  Minus
  Star
  Slash
  EqEq
  Bang
  // 分隔符
  LParen
  RParen
  LBrace
  RBrace
  Arrow
  // 特殊
  Newline
  EOF
}

derive(Token: Eq, Show, Debug)
```

#### Lexer 结构体与核心方法

```moonbit
struct Lexer {
  source : String
  pos : Int
  line : Int
  col : Int
}

fn Lexer::new(source : String) -> Lexer {
  Lexer::{ source: source, pos: 0, line: 1, col: 1 }
}

fn Lexer::peek(self : Lexer) -> Char {
  if self.pos < self.source.byte_length() {
    self.source[self.pos]
  } else { '\x00' }
}

fn Lexer::advance(self : Ref[Lexer]) -> Char {
  let ch = self.peek()
  if ch != '\x00' {
    if ch == '\n' { self.line += 1; self.col = 1 }
    else { self.col += 1 }
    self.pos += 1
  }
  ch
}
```

**核心 tokenize 方法：使用模式匹配分派**

```moonbit
fn Lexer::tokenize(self : Lexer) -> Array[Token] {
  let mut tokens : Array[Token] = []
  let mut lexer = self
  
  while lexer.pos < lexer.source.byte_length() {
    let ch = lexer.peek()
    
    match ch {
      ' ' | '\t' | '\r' => { lexer.advance() }
      '\n' => { tokens.push(Newline); lexer.advance() }
      '(' => { tokens.push(LParen); lexer.advance() }
      ')' => { tokens.push(RParen); lexer.advance() }
      '{' => { tokens.push(LBrace); lexer.advance() }
      '}' => { tokens.push(RBrace); lexer.advance() }
      '+' => { tokens.push(Plus); lexer.advance() }
      '-' => {
        lexer.advance()
        if lexer.peek() == '>' { tokens.push(Arrow); lexer.advance() }
        else { tokens.push(Minus) }
      }
      '*' => { tokens.push(Star); lexer.advance() }
      '/' => { tokens.push(Slash); lexer.advance() }
      '=' => {
        lexer.advance()
        if lexer.peek() == '=' { tokens.push(EqEq); lexer.advance() }
        else { /* error */ }
      }
      '!' => { tokens.push(Bang); lexer.advance() }
      '"' => { tokens.push(lex_string(&mut lexer)) }
      '0'..'9' => { tokens.push(lex_number(&mut lexer)) }
      'a'..'z' | 'A'..'Z' | '_' => { tokens.push(lex_ident(&mut lexer)) }
      _ => { lexer.advance() }
    }
  }
  
  tokens.push(EOF)
  tokens
}
```

**辅助词法分析函数**

```moonbit
fn lex_string(lexer : Ref[Lexer]) -> Token {
  lexer.advance()
  let mut chars : Array[Char] = []
  
  while lexer.peek() != '"' && lexer.peek() != '\x00' {
    chars.push(lexer.advance())
  }
  lexer.advance()
  
  LitString(chars.iter().map(fn(c) { c.to_string() }).join(""))
}

fn lex_number(lexer : Ref[Lexer]) -> Token {
  let mut digits : Array[Char] = []
  while is_digit(lexer.peek()) {
    digits.push(lexer.advance())
  }
  LitInt(digits.iter().map(fn(c) { c.to_string() }).join("").to_int().unwrap_or(0))
}

fn lex_ident(lexer : Ref[Lexer]) -> Token {
  let mut chars : Array[Char] = []
  while is_ident_char(lexer.peek()) {
    chars.push(lexer.advance())
  }
  let ident = chars.iter().map(fn(c) { c.to_string() }).join("")
  
  match ident {
    "if" => KwIf
    "else" => KwElse
    "fn" => KwFn
    "let" => KwLet
    "match" => KwMatch
    _ => Ident(ident~)
  }
}

fn is_digit(ch : Char) -> Bool { ch >= '0' && ch <= '9' }

fn is_ident_char(ch : Char) -> Bool {
  (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z') || ch == '_'
}
```

#### AST 节点定义（ADT）

```moonbit
enum Expr {
  EInt(Int)
  EBool(Bool)
  EString(String~)
  EVar(String~)
  EBinOp(BinOp, Expr, Expr)
  EIf(Expr, Expr, Expr)
  ECall(String~, Array[Expr])
  ELet(String~, Expr, Expr)
  EMatch(Expr, Array[(Pattern, Expr)])
}

derive(Expr: Show, Debug)

enum BinOp {
  Add
  Sub
  Mul
  Div
  Eq
  Ne
  Lt
  Gt
}

enum Pattern {
  PInt(Int)
  PBool(Bool)
  PString(String~)
  PVar(String~)
  PWildcard
}
```

#### Parser（递归下降解析器）

```moonbit
struct Parser {
  tokens : Array[Token]
  pos : Int
}

fn Parser::new(tokens : Array[Token]) -> Parser {
  Parser::{ tokens: tokens, pos: 0 }
}

fn Parser::peek(self : Parser) -> Token {
  if self.pos < self.tokens.length { self.tokens[self.pos] }
  else { EOF }
}

fn Parser::advance(self : Ref[Parser]) -> Token {
  let token = self.peek()
  self.pos += 1
  token
}

fn Parser::expect(self : Ref[Parser], expected : Token) -> Result[Unit, String] {
  let token = self.advance()
  if token == expected { Ok(()) }
  else { Err("unexpected token: " + debug_show(token)) }
}
```

**表达式解析（Pratt 解析器 / 递归下降）**

```moonbit
fn Parser::parse_expr(self : Ref[Parser]) -> Result[Expr, String] {
  self.parse_additive()
}

fn Parser::parse_additive(self : Ref[Parser]) -> Result[Expr, String] {
  let mut left = self.parse_primary()?
  
  loop {
    match self.peek() {
      Plus => {
        self.advance()
        let right = self.parse_primary()?
        left = EBinOp(Add, left, right)
      }
      Minus => {
        self.advance()
        let right = self.parse_primary()?
        left = EBinOp(Sub, left, right)
      }
      _ => break
    }
  }
  
  Ok(left)
}

fn Parser::parse_primary(self : Ref[Parser]) -> Result[Expr, String] {
  match self.peek() {
    LitInt(n) => { self.advance(); Ok(EInt(n)) }
    LitBool(b) => { self.advance(); Ok(EBool(b)) }
    LitString(s) => { self.advance(); Ok(EString(s)) }
    Ident(name) => { self.advance(); Ok(EVar(name)) }
    KwIf => self.parse_if_expr()
    LParen => {
      self.advance()
      let expr = self.parse_expr()?
      self.expect(RParen)?;
      Ok(expr)
    }
    token => Err("unexpected token in primary: " + debug_show(token))
  }
}

fn Parser::parse_if_expr(self : Ref[Parser]) -> Result[Expr, String] {
  self.advance()
  let cond = self.parse_expr()?;
  Ok(EIf(cond, EInt(0), EInt(0)))
}
```

#### Evaluator（模式匹配求值器）

```moonbit
struct Env {
  bindings : Map[String, Value]
}

enum Value {
  VInt(Int)
  VBool(Bool)
  VString(String~)
  VClosure(String~, Expr, Env)
  VBuiltin((Array[Value]) -> Value)
}

fn Env::new() -> Env { Env::{ bindings: Map::empty() } }

fn Env::get(self : Env, name : String) -> Option[Value] {
  self.bindings.get(name)
}

fn Env::set(self : Env, name : String, value : Value) -> Env {
  { ..self, bindings: self.bindings.set(name, value) }
}
```

**核心求值函数：使用模式匹配分发**

```moonbit
fn eval(expr : Expr, env : Env) -> Result[Value, String] {
  match expr {
    EInt(n) => Ok(VInt(n))
    EBool(b) => Ok(VBool(b))
    EString(s) => Ok(VString(s))
    
    EVar(name) => match env.get(name) {
      Some(v) => Ok(v)
      None => Err("unbound variable: " + name)
    }
    
    EBinOp(op, left, right) => {
      let l = eval(left, env)?
      let r = eval(right, env)?
      
      match (op, l, r) {
        (Add, VInt(a), VInt(b)) => Ok(VInt(a + b))
        (Sub, VInt(a), VInt(b)) => Ok(VInt(a - b))
        (Mul, VInt(a), VInt(b)) => Ok(VInt(a * b))
        (Div, VInt(a), VInt(b)) =>
          if b == 0 { Err("division by zero") }
          else { Ok(VInt(a / b)) }
        (Eq, a, b) => Ok(VBool(values_equal(a, b)))
        (Ne, a, b) => Ok(VBool(!values_equal(a, b)))
        (Lt, VInt(a), VInt(b)) => Ok(VBool(a < b))
        (Gt, VInt(a), VInt(b)) => Ok(VBool(a > b))
        _ => Err("type error in binary operation")
      }
    }
    
    EIf(cond, then_branch, else_branch) => {
      match eval(cond, env)? {
        VBool(true) => eval(then_branch, env)
        VBool(false) => eval(else_branch, env)
        _ => Err("if condition must be boolean")
      }
    }
    
    ELet(name, value_expr, body) => {
      let value = eval(value_expr, env)?
      let new_env = env.set(name, value)
      eval(body, new_env)
    }
    
    ECall(func_name, args) => {
      match env.get(func_name) {
        Some(VBuiltIn(fn)) => {
          let evaluated_args : Array[Value] = []
          for arg in args {
            evaluated_args.push(eval(arg, env)?)
          }
          Ok(fn(evaluated_args))
        }
        Some(_) => Err(func_name + " is not a function")
        None => Err("undefined function: " + func_name)
      }
    }
    
    EMatch(scrutinee, cases) => {
      let value = eval(scrutinee, env)?
      
      for (pattern, body) in cases {
        match try_match(pattern, value) {
          Some(new_env) => return eval(body, merge_envs(env, new_env))
          None => {}
        }
      }
      
      Err("non-exhaustive match")
    }
  }
}
```

**模式匹配辅助函数**

```moonbit
fn try_match(pattern : Pattern, value : Value) -> Option[Env] {
  match (pattern, value) {
    (PWildcard, _) => Some(Env::new())
    (PInt(n), VInt(m)) if n == m => Some(Env::new())
    (PBool(b), VBool(c)) if b == c => Some(Env::new())
    (PString(s), VString(t)) if s == t => Some(Env::new())
    (PVar(name), v) => Some(Env::new().set(name, v))
    (_, _) => None
  }
}

fn values_equal(a : Value, b : Value) -> Bool {
  match (a, b) {
    (VInt(x), VInt(y)) => x == y
    (VBool(x), VBool(y)) => x == y
    (VString(x), VString(y)) => x == y
    (_, _) => false
  }
}

fn merge_envs(env1 : Env, env2 : Env) -> Env {
  { ..env1, bindings: env1.bindings.merge(env2.bindings) }
}
```

**设计要点总结**：

| 阶段 | 数据结构 | 核心技术 |
|------|---------|---------|
| 词法分析 | `Token` (ADT) | 模式匹配分派 |
| 语法分析 | `Expr` (ADT) | 递归下降 + 模式匹配 |
| 语义求值 | `Value` (ADT) + `Env` | 模式匹配分发 |
| 错误处理 | `Result[T, String]` | 函数式错误传播 |

### 3.5.2 属性驱动代码生成模式（来自 morm）

**核心思想**：利用 MoonBit 的属性系统实现 DSL 式 API，通过元数据驱动代码自动生成。

#### 自定义属性定义

```moonbit
attr MormEntityAttr : EntityDecl -> Unit = "#morm.entity"
attr MormPrimaryKeyAttr : FieldDecl -> Unit = "#morm.primary_key"
attr MormForeignKeyAttr : FieldDecl -> Unit = "#morm.foreign_key"
attr MormUniqueAttr : FieldDecl -> Unit = "#morm.unique"
attr MormIndexAttr : EntityDecl -> Unit = "#morm.index"
attr MormIgnoreAttr : FieldDecl -> Unit = "#morm.ignore"
```

#### 实体定义示例

```moonbit
#[morm.entity]
#[morm.table_name("users")]
struct User {
  #[morm.primary_key]
  #[morm.auto_increment]
  id : Int
  
  #[morm.unique]
  username : String~
  
  email : String~
  
  #[morm.column("created_at")]
  createdAt : DateTime
  
  #[morm.foreign_key("roles.id")]
  roleId : Int?
  
  #[morm.ignore]
  tempCache : String?
}
```

#### 代码生成器核心结构

```moonbit
struct CodeGenerator {
  entities : Array[EntityInfo]
}

struct EntityInfo {
  name : String
  table_name : String
  fields : Array[FieldInfo]
  primary_key : Option[String]
  foreign_keys : Array[ForeignKeyInfo]
  unique_fields : Array[String]
}

struct FieldInfo {
  name : String
  column_name : String
  type_name : String
  is_optional : Bool
  has_default : Bool
  attributes : Array[String]
}

struct ForeignKeyInfo {
  field_name : String
  reference : String~
}
```

#### CRUD 代码生成

```moonbit
fn CodeGenerator::generate_crud(self : CodeGenerator, entity : EntityInfo) -> String {
  let mut code : Array[String] = []
  
  for field in entity.fields {
    if field.attributes.contains("unique") || field.name == entity.primary_key.unwrap_or("") {
      code.push(generate_find_by(entity, field))
    }
  }
  
  code.push(generate_insert(entity))
  code.push(generate_update(entity))
  code.push(generate_delete(entity))
  code.push(generate_select(entity))
  
  code.join("\n\n")
}

fn generate_find_by(entity : EntityInfo, field : FieldInfo) -> String {
  let method_name = "find_by_" + snake_case(field.name)
  let param_type = if field.is_optional { field.type_name + "?" } else { field.type_name }
  
  "  pub fn " + method_name + "(self : " + entity.name + "Repo, value : " + param_type + ") -> Option[" + entity.name + "] {\n" +
  "    // Generated: SELECT * FROM " + entity.table_name + " WHERE " + field.column_name + " = ?\n" +
  "    TODO()\n" +
  "  }\n"
}

fn generate_insert(entity : EntityInfo) -> String {
  let columns = entity.fields
    .filter(fn(f) { !f.attributes.contains("ignore") })
    .map(fn(f) { f.column_name })
    .join(", ")
  
  "  pub fn insert(self : " + entity.name + "Repo, entity : " + entity.name + ") -> Result[" + entity.name + ", String] {\n" +
  "    // Generated: INSERT INTO " + entity.table_name + " (" + columns + ") VALUES (...)\n" +
  "    TODO()\n" +
  "  }\n"
}

fn generate_update(entity : EntityInfo) -> String {
  "  pub fn update(self : " + entity.name + "Repo, entity : " + entity.name + ") -> Result[" + entity.name + ", String] {\n" +
  "    // Generated: UPDATE " + entity.table_name + " SET ... WHERE id = ?\n" +
  "    TODO()\n" +
  "  }\n"
}

fn generate_delete(entity : EntityInfo) -> String {
  "  pub fn delete(self : " + entity.name + "Repo, id : Int) -> Result[Unit, String] {\n" +
  "    // Generated: DELETE FROM " + entity.table_name + " WHERE id = ?\n" +
  "    TODO()\n" +
  "  }\n"
}

fn generate_select(entity : EntityInfo) -> String {
  "  pub fn select_all(self : " + entity.name + "Repo) -> Array[" + entity.name + "] {\n" +
  "    // Generated: SELECT * FROM " + entity.table_name + "\n" +
  "    TODO()\n" +
  "  }\n"
}

fn snake_case(name : String) -> String {
  let mut result : Array[Char] = []
  for (i, ch) in name.char_iter().enumerate() {
    if i > 0 && ch >= 'A' && ch <= 'Z' {
      result.push('_')
      result.push((ch.to_int() + 32).to_char())
    } else {
      result.push(ch)
    }
  }
  result.iter().map(fn(c) { c.to_string() }).join("")
}
```

#### 方言抽象 Trait（多后端支持）

```moonbit
pub(open) trait SqlDialect {
  quote_identifier(Self, String) -> String
  placeholder(Self, Int) -> String
  limit_clause(Self, Int) -> String
  offset_clause(Self, Int) -> String
  upsert_syntax(Self, String, Array[String], Array[String]) -> String
}

impl SqlDialect for SQLiteDialect with quote_identifier(name) {
  "\"" + name + "\""
} with placeholder(_index) {
  "?"
} with limit(limit) {
  " LIMIT " + limit.to_string()
} with offset(offset) {
  " OFFSET " + offset.to_string()
} with upsert(table, columns, values) {
  "INSERT OR REPLACE INTO " + table + " (" + columns.join(", ") + ") VALUES (" + values.join(", ") + ")"
}

impl SqlDialect for MySQLDialect with quote_identifier(name) {
  "`" + name + "`"
} with placeholder(index) {
  "$" + index.to_string()
} with limit(limit) {
  " LIMIT " + limit.to_string()
} with offset(offset) {
  " OFFSET " + offset.to_string()
} with upsert(table, columns, values) {
  "INSERT INTO " + table + " (" + columns.join(", ") + ") VALUES (" + values.join(", ") + ") " +
  "ON DUPLICATE KEY UPDATE " + columns.map(fn(c) { c + "=VALUES(" + c + ")" }).join(", ")
}
```

**模式对比总结**：

| 模式 | 来源项目 | 核心技术 | 应用场景 |
|------|---------|---------|---------|
| 编译器管道 | MoonBash | ADT + 模式匹配 | 解释器、编译器、DSL 实现 |
| 属性驱动生成 | morm | 属性系统 + Trait 抽象 | ORM、代码生成、框架开发 |

---

## Part 4: 方法系统与运算符重载 ⚡ v6.0 增强

> MoonBit 的方法是与类型关联的顶层函数，支持重载、别名、运算符重载。这是构建直观 API 的核心能力。

### 4.1 方法定义语法

MoonBit 的方法是**与类型关联的顶层函数**（非 OOP 风格）：

```moonbit
// 推荐语法：TypeName::method_name
fn Point::new(x : Int, y : Int) -> Point {
  Point::{ x: x, y: y }
}

fn Point::distance_to(self : Point, other : Point) -> Double {
  let dx = (self.x - other.x).to_double()
  let dy = (self.y - other.y).to_double()
  sqrt(dx * dx + dy * dy)
}

// 调用方式
let p1 = Point::new(0, 0)
let p2 = Point::new(3, 4)
println(p1.distance_to(p2))     // 点语法
println(Point::distance_to(p1, p2))  // 完整语法
```

**⚠️ 已废弃语法提醒**：
```moonbit
// ❌ 不推荐：self 形式（未来可能废弃）
fn method_name(self : SelfType) -> Unit { ... }

// ✅ 推荐：TypeName::method_name 形式
fn SelfType::method_name(self : SelfType) -> Unit { ... }
```

### 4.2 方法重载

不同类型可以定义**同名方法**——每个类型的方法在各自命名空间中：

```moonbit
struct Vec2 { x : Double, y : Double }
struct Vec3 { x : Double, y : Double, z : Double }

fn Vec2::length(self : Vec2) -> Double {
  sqrt(self.x * self.x + self.y * self.y)
}

fn Vec3::length(self : Vec3) -> Double {
  sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
}

test {
  let v2 = Vec2::{ x: 3.0, y: 4.0 }
  let v3 = Vec3::{ x: 1.0, y: 2.0, z: 2.0 }
  assert_eq(v2.length(), 5.0)
  assert_eq(v3.length(), 3.0)
}
```

### 4.3 本地方法扩展

可以为**外部类型定义私有方法**，用于扩展上游 API：

```moonbit
// 为 Int 添加本地方法（仅当前包可见）
priv fn Int::is_even(self : Int) -> Bool {
  self % 2 == 0
}

test {
  assert_true((42).is_even())
  assert_false((7).is_even())
}
```

**规则**：
- 只能是 `priv`（私有）的
- 可以覆盖类型自身包中的方法（会发出警告）
- 用途：为外部库的类型提供补充 API

### 4.4 方法别名系统

#### #alias — 运算符重载（v0.6.29+ 推荐）

```moonbit
// 重载下标获取 [] 运算符
#alias("_[_]")
fn[X] Array::get(self : Array[X], index : Int) -> X {
  self[index]
}

// 重载下标设置 []= 运算符
#alias("_[_]=_")
fn[X] Array::set(self : Array[X], index : Int, elem : X) -> Unit {
  self[index] = elem
}

// 重载切片视图 [_:_] 运算符
#alias("_[_:_]")
fn[X] Array::view(
  self : Array[X],
  start? : Int = 0,
  end? : Int = self.length(),
) -> ArrayView[X] {
  self[start:end]
}
```

**v0.6.29+ 支持的所有 #alias 运算符**：

| #alias 值 | 运算符 | 说明 |
|-----------|--------|------|
| `"_[_]"` | `a[i]` | 下标获取 |
| `"_[_]=_"` | `a[i] = v` | 下标设置 |
| `"_[_:_]"` | `a[i:j]` | 视图切片 |

#### #alias / #as_free_fn — 方法/函数别名

```moonbit
#alias(m)                              // 创建同名方法别名
#alias(n, visibility="priv")            // 私有别名
#as_free_fn(m)                         // 转换为自由函数
#as_free_fn(n, visibility="pub")        // 公有自由函数

fn List::f() -> Bool { true }

test {
  assert_eq(List::f(), List::m())       // m 是 f 的方法别名
  assert_eq(List::m(), m())             // m() 作为自由函数调用
}
```

### 4.5 通过 Trait 重载算术/比较运算符

```moonbit
struct Complex {
  re : Double
  im : Double
}
derive(Debug)

impl Add for Complex with add(self : Complex, other : Complex) -> Complex {
  Complex::{ re: self.re + other.re, im: self.im + other.im }
}

impl Sub for Complex with sub(self : Complex, other : Complex) -> Complex {
  Complex::{ re: self.re - other.re, im: self.im - other.im }
}

impl Mul for Complex with mul(self : Complex, other : Complex) -> Complex {
  Complex::{
    re: self.re * other.re - self.im * other.im,
    im: self.re * other.im + self.im * other.re,
  }
}

impl Eq for Complex with op_equal(self : Complex, other : Complex) -> Bool {
  self.re == other.re && self.im == other.im
}

test {
  let a = Complex::{ re: 1.0, im: 2.0 }
  let b = Complex::{ re: 3.0, im: 4.0 }
  let sum = a + b       // 使用重载的 +
  let diff = a - b      // 使用重载的 -
  let prod = a * b      // 使用重载的 *
  assert_eq(sum, Complex::{ re: 4.0, im: 6.0 })
}
```

**完整可重载运算符表**：

| 运算符 | 重载机制 | Trait / 方法 |
|--------|---------|-------------|
| `+` | Trait | `Add` |
| `-` | Trait | `Sub` |
| `*` | Trait | `Mul` |
| `/` | Trait | `Div` |
| `%` | Trait | `Mod` |
| `==` / `!=` | Trait | `Eq` (`op_equal`) |
| `<` `>` `<=` `>=` | Trait | `Compare` (`compare`) |
| `<<` | Trait | `Shl` |
| `>>` | Trait | `Shr` |
| `-x` (一元负) | Trait | `Neg` |
| `&` | Trait | `BitAnd` |
| `\|` | Trait | `BitOr` |
| `^` | Trait | `BitXor` |
| `a[i]` | Method + #alias | `#[alias("_[_]")]` |
| `a[i]=v` | Method + #alias | `#[alias("_[_]=_")]` |
| `a[i:j]` | Method + #alias | `#[alias("_[_:_]")]` |

### 4.6 库级方法设计最佳实践

#### 原则一：构造器使用 ::new / ::make

```moonbit
struct Buffer[T] { data : Array[T]; capacity : Int; length : Int }

fn[T : Default] Buffer::new(capacity : Int) -> Buffer[T] {
  Buffer::{ data: Array::make(capacity, T::default()), capacity: capacity, length: 0 }
}

fn[T] Buffer::with_values(values : Array[T]) -> Buffer[T] {
  Buffer::{ data: values, capacity: values.length, length: values.length }
}
```

#### 原则二：不可变操作返回新值，可变操作修改 self

```moonbit
// 不可变：返回新实例
fn[T] Buffer::push(self : Buffer[T], value : T) -> Buffer[T] {
  // ...
}

// 可变：直接修改（使用 Ref 或 mut 字段）
fn[T] Buffer::push_mut(self : Ref[Buffer[T]], value : T) -> Unit {
  // ...
}
```

#### 原则三：转换方法用 ::to_xxx / ::from_xxx / ::into_xxx

```moonbit
fn Point::to_vec2(self : Point) -> Vec2 { ... }
fn Vec2::from_point(p : Point) -> Vec2 { ... }
fn Point::into_tuple(self : Point) -> (Int, Int) { (self.x, self.y) }
```

---

## Part 4.5: Impl 可变性语义深度解析 ⭐ v8.0 新增

> 来自 mbtgraph（MoonBit 图算法库）的核心概念——理解 MoonBit 的可变性两层机制

### 4.5.1 ⚠️ 不支持 mut self 参数

这是 MoonBit 新手最容易踩的坑之一：

```moonbit
// ❌ 错误：MoonBit 不支持 mut self
impl GraphWritable for MyGraph with add_node(mut self, data) -> NodeId {
  self.nodes.push(...)
}

// ✅ 正确：使用 (self)，内部绑定可变副本
impl GraphWritable for MyGraph with add_node(self, data) -> NodeId {
  let g = self          // 绑定到局部变量
  g.nodes.push(...)     // 通过字段修改
  result
}
```

**关键点**：
- `self` 参数始终是**不可变的绑定**
- 需要修改时，在方法体内部重新绑定为可变变量
- 这是 MoonBit 值传递语义的自然结果

### 4.5.2 可变性的两层机制（核心概念！）

MoonBit 的可变性有 **两个独立层级**，理解这一点至关重要：

#### 层级 1：字段级 mut（声明时决定）

```moonbit
pub struct MyGraph {
  mut node_cnt : Int       // 字段本身是可变的
  nodes : Array[Node?]     // 字段不可变（但数组内容可通过 API 变更）
}
```

- **`mut` 字段**：可以在不声明 `let mut` 的情况下被修改
- **非 mut 字段**：只能通过特定的可变 API（如 Array 的 push、索引赋值）变更

#### 层级 2：绑定级 mut（let mut vs let）

```moonbit
// 方式 A：普通绑定 + 字段 mut → 可以修改字段
let g = self
g.node_cnt = g.node_cnt + 1   // ✅ 因为字段声明了 mut

// 方式 B：可变绑定 → 可以重新赋值整个变量
let mut g = self
g = some_other_value           // ✅ 因为绑定了 mut
g.node_cnt = g.node_cnt + 1    // ✅ 同时也支持字段修改
```

**核心规则（背诵！）**：

> **如果只需要修改结构体的字段（push、索引赋值等），不需要 `let mut`。**
> **只有需要重新赋值变量本身时才需要 `let mut`。**

### 4.5.3 实际示例对比

#### 场景 1：只修改字段 — 不需要 mut

```moonbit
impl GraphWritable for MyGraph with add_node(self, data) -> NodeId {
  let g = self                    // 普通 binding
  if idx == g.nodes.length() {
    g.nodes.push(None)            // ✅ 字段 mut 允许
    g.adj.push([])                // ✅ 字段 mut 允许
  }
  g.nodes[idx] = Some(...)        // ✅ 字段 mut 允许
  g.node_cnt = g.node_cnt + 1     // ✅ 字段 mut 允许
  @core.NodeId(idx)
}
```

**适用场景**：
- push/pop 操作
- 索引赋值
- 字段计数器更新
- 数组/Map 内容修改

#### 场景 2：循环中重新赋值变量 — 需要 mut

```moonbit
impl ... with remove_node(self, id) -> Bool {
  let mut g = self                // 可变 binding
  for entry in g.adj[idx] {
    match entry {
      (nid, _) => {
        g = remove_rev(g, nid.0, idx)   // ✅ 重新赋值 g
        g.edge_cnt = g.edge_cnt - 1      // ✅ 字段修改
      }
    }
  }
  true
}
```

**适用场景**：
- 循环中累积状态变化
- 递归调用后更新变量
- 条件分支后合并不同状态

### 4.5.4 E0015 unused_mut 警告处理

当声明了 `let mut` 但从未对绑定进行重新赋值时触发：

```moonbit
fn bad_example(self : MyGraph) -> Int {
  let mut g = self
  g.node_cnt = g.node_cnt + 1   // 只改了字段，没重新赋值 g 本身
  // ⚠️ Warning: unused_mut — g 的 mut 从未使用
  g.node_cnt
}
```

**修复方案**：

```moonbit
fn fixed_example(self : MyGraph) -> Int {
  let g = self                  // 改为普通 binding
  g.node_cnt = g.node_cnt + 1   // ✅ 字段修改仍然有效
  g.node_cnt
}
```

**判断方法**：问自己：这个函数中是否有 `g = ...` 这样的**重新赋值语句**？
- 有 → 需要 `let mut g`
- 没有 → 用 `let g` 即可

**快速检查清单**：

| 操作类型 | 需要 `let mut`？ | 示例 |
|---------|-----------------|------|
| 字段赋值 | ❌ | `g.field = new_value` |
| 数组 push | ❌ | `g.arr.push(elem)` |
| 索引赋值 | ❌ | `g.arr[i] = value` |
| Map 插入 | ❌ | `g.map.set(key, val)` |
| 变量重新赋值 | ✅ | `g = some_function(g)` |
| 循环累加 | ✅ | `for ... { g = update(g) }` |

### 4.5.5 值传递语义的影响

由于 `self` 是按值传递的，这带来了重要的设计影响：

```moonbit
impl GraphWritable for MyGraph with add_node(self, data) -> NodeId {
  let g = self
  g.node_cnt = 100    // 修改的是副本 g，不是原始 self
  // 原始 self 不受影响（值语义）
  @core.NodeId(idx)
}

// 调用方示例
fn main {
  let graph = create_graph()
  let node_id = graph.add_node(1.0)   // graph 未改变
  // 如果需要更新后的图：
  let updated_graph = graph.with_added_node(1.0)  // 返回新状态
}
```

**这意味着**：

1. **天然不可变接口**：impl 方法天然支持**不可变接口 + 内部可变实现**
   ```moonbit
   // 外部看是不可变的
   let graph2 = graph.add_edge(u, v)
   // 内部实现可以修改字段
   ```

2. **调用方责任**：调用方需要接收返回值来获取更新后的状态
   ```moonbit
   // 模式 A：接收返回值
   let new_graph = old_graph.add_node(data)

   // 模式 B：调用方管理可变绑定
   let mut graph = initial_graph
   graph = graph.add_node(data)
   ```

3. **时间旅行调试优势**：旧状态仍可用，方便回溯和对比
   ```moonbit
   let graph_v1 = initial_graph
   let graph_v2 = graph_v1.add_node(node1)
   let graph_v3 = graph_v2.add_node(node2)
   // graph_v1, graph_v2, graph_v3 同时存在且各自独立
   ```

### 4.5.6 设计模式启示

基于值传递语义 + 两层可变性，MoonBit 天然适合以下模式：

#### 模式速查表

| 模式 | 描述 | 适用场景 |
|------|------|---------|
| **不可变接口** | 所有方法返回新状态 | 数据结构、状态机、配置对象 |
| **命令查询分离** | 修改方法返回新状态，查询方法无副作用 | API 设计、领域模型 |
| **链式调用** | 每步返回新对象 | Builder、DSL、管道操作 |
| **时间旅行调试** | 旧状态仍可用，方便回溯 | 算法可视化、撤销/重做 |

#### 实战示例：不可变图 API

```moonbit
pub struct Graph {
  mut nodes : Array[NodeData]
  mut edges : Array[Edge]
  mut node_count : Int
  mut edge_count : Int
}

impl Graph with add_node(self, data : NodeData) -> Graph {
  let g = self
  g.nodes.push(data)
  g.node_count = g.node_count + 1
  g                                    // 返回新状态
}

impl Graph with add_edge(self, u : NodeId, v : NodeId) -> Graph {
  let g = self
  g.edges.push(Edge::{ from: u, to: v })
  g.edge_count = g.edge_count + 1
  g                                    // 返回新状态
}

impl Graph with has_edge(self, u : NodeId, v : NodeId) -> Bool {
  // 查询方法：无副作用
  self.edges.any(fn(e) { e.from == u && e.to == v })
}

// 使用示例
fn build_sample_graph() -> Graph {
  let empty = Graph::new()
  empty
    .add_node(NodeData::{ id: 0, label: "A"~ })
    .add_node(NodeData::{ id: 1, label: "B"~ })
    .add_edge(@core.NodeId(0), @core.NodeId(1))
}
```

#### 实战示例：Builder 模式增强

```moonbit
struct QueryBuilder {
  mut table : String
  mut filters : Array[String]
  mut limit : Int?
}

impl QueryBuilder with new(table : String) -> QueryBuilder {
  QueryBuilder::{
    table: table,
    filters: [],
    limit: None,
  }
}

impl QueryBuilder with where_clause(self, condition : String) -> QueryBuilder {
  let b = self
  b.filters.push(condition)
  b
}

impl QueryBuilder with set_limit(self, n : Int) -> QueryBuilder {
  let b = self
  b.limit = Some(n)
  b
}

impl QueryBuilder with build(self) -> String {
  let base = "SELECT * FROM " + self.table
  let filter_part = if self.filters.length() > 0 {
    " WHERE " + self.filters.join(" AND ")
  } else { "" }
  let limit_part = match self.limit {
    Some(n) => " LIMIT " + n.to_string()
    None => ""
  }
  base + filter_part + limit_part
}

// 使用
fn example_query() -> String {
  QueryBuilder::new("users")
    .where_clause("age > 18")
    .where_clause("status = 'active'~")
    .set_limit(100)
    .build()
}
```

### 4.5.7 性能优化建议

虽然值传递语义带来代码清晰度，但在性能敏感场景需要注意：

#### 优化策略一：大结构体使用 Ref

```moonbit
// 对于大型数据结构，考虑使用 Ref 包装
fn process_large_graph(self : Ref[LargeGraph]) -> Unit {
  // 直接修改，无需复制
  self.node_count += 1
}
```

#### 优化策略二：批量操作减少中间状态

```moonbit
// ❌ 低效：多次创建中间状态
let g1 = graph.add_node(n1)
let g2 = g1.add_node(n2)
let g3 = g2.add_node(n3)

// ✅ 高效：批量添加
let g = graph.add_nodes([n1, n2, n3])
```

#### 优化策略三：惰性求值

```moonbit
// 对于可能不需要的结果，延迟计算
impl Graph with lazy_traversal(self) -> LazyTraversal {
  LazyTraversal::{ source: self }  // 不立即计算
}
```

### 4.5.8 常见错误与解决方案

#### 错误 1：误用 mut self

```moonbit
// ❌ 编译错误
impl Graph with broken_method(mut self) -> Graph {
  self.node_count += 1
  self
}

// ✅ 正确实现
impl Graph with correct_method(self) -> Graph {
  let g = self
  g.node_count += 1
  g
}
```

#### 错误 2：忘记返回新状态

```moonbit
// ❌ 丢失更新
let graph = create_graph()
graph.add_node(data)      // 返回值被忽略！

// ✅ 正确接收
let graph = graph.add_node(data)
```

#### 错误 3：过度使用 let mut

```moonbit
// ⚠️ 不必要的 mut（会触发 E0015 警告）
impl Graph with count_nodes(self) -> Int {
  let mut g = self           // 不必要的 mut
  return g.node_count        // 只读取，未修改
}

// ✅ 简洁版本
impl Graph with count_nodes(self) -> Int {
  self.node_count            // 直接访问即可
}
```

---

## Part 5: 特征对象

### 5.1 运行时多态

使用 `as &Trait` 将具体类型打包为**特征对象**：

```moonbit
pub(open) trait Animal {
  speak(Self) -> String
}

struct Duck(String)
fn Duck::make(name: String) -> Duck { Duck(name) }
impl Animal for Duck with speak(self) {
  "\(self.0): quack!"
}

struct Fox(String)
fn Fox::make(name: String) => Fox(name)
impl Animal for Fox with speak(_self) {
  "What does the fox say?"
}

test {
  let duck1 = Duck::make("duck1")
  let duck2 = Duck::make("duck2")
  let fox1 = Fox::make("fox1")

  // 不同类型可以放入同一数组！
  let animals: Array[&Animal] = [duck1, duck2, fox1]

  inspect(
    animals.map(fn(animal) { animal.speak() }),
    content=(
      #|["duck1: quack!", "duck2: quack!", "What does the fox say?"]
    ),
  )
}
```

### 5.2 对象安全规则

**并非所有 Trait 都能创建特征对象**。必须满足：

1. ✅ `Self` 必须是方法的**第一个参数**
2. ✅ 方法的类型中只能出现**一个** `Self`（即第一个参数）

```moonbit
// ✅ 对象安全
pub(open) trait Logger {
  write_string(Self, String) -> Unit
}

// ❌ 非对象安全（Self 出现两次）
pub(open) trait BadExample {
  merge(Self, Self) -> Self  // 错误！
}
```

### 5.3 为特征对象定义新方法

特征对象也可以像普通类型一样定义新方法：

```moonbit
pub(open) trait CanLog {
  log(Self, &Logger) -> Unit
}

// 为 &Logger 定义新方法
fn[Obj : CanLog] &Logger::write_object(self: &Logger, obj: Obj) -> Unit {
  obj.log(self)
}

// 使用新方法简化代码
pub impl[A : CanLog, B : CanLog] CanLog for (A, B) with log(self, logger) {
  let (a, b) = self
  logger
    ..write_string("(")
    ..write_object(a)
    ..write_string(", ")
    ..write_object(b)
    ..write_string(")")
}
```

---

## Part 6: 派生宏系统

### 6.1 自动派生概览

MoonBit 支持从类型定义中**自动派生内建特征的实现**：

```moonbit
struct T {
  a: Int
  b: Int
}
derive(Eq, Compare, Show, Default, Hash)  // 一行代码生成所有实现
```

**前提条件**：类型中使用的所有字段都必须实现了对应的 Trait。

### 6.2 相等与比较 (Eq / Compare)

```moonbit
struct DeriveEqCompare {
  x: Int
  y: Int
}
derive(Eq, Compare)

test "derive eq_compare struct" {
  let p1 = DeriveEqCompare::{ x: 1, y: 2 }
  let p2 = DeriveEqCompare::{ x: 2, y: 1 }
  let p3 = DeriveEqCompare::{ x: 1, y: 2 }

  // Eq 测试
  assert_eq(p1 == p2, false)
  assert_eq(p1 == p3, true)
  assert_eq(p1 != p2, true)

  // Compare 测试
  assert_true(p1 < p2)
  assert_false(p1 < p3)
  assert_true(p1 <= p2)
}

// 枚举也支持派生
enum DeriveEqCompareEnum {
  Case1(Int)
  Case2(label~: String)
  Case3
}
derive(Eq, Compare)
```

**比较规则**：
- 结构体：按字段定义顺序逐一比较
- 枚举：先按构造器顺序，再按构造器参数比较

### 6.3 Debug 特征

用于生成**结构化的调试输出**：

```moonbit
struct DebugPoint {
  x: Int
  y: Int
}
derive(Debug)

test "derive debug struct" {
  let point = DebugPoint::{ x: 1, y: 2 }
  debug_inspect(point, content="{ x: 1, y: 2 }")
}

enum DebugShape {
  Circle(radius~: Int)
  Rect(width~: Int, height~: Int)
}
derive(Debug)

test "derive debug enum" {
  let shape = DebugShape::Rect(width=3, height=4)
  debug_inspect(shape, content="Rect(width=3, height=4)")
}
```

**用途**：
- 测试中的 `debug_inspect`
- 配合 `@debug.to_string` 格式化诊断信息

### 6.4 Default 特征

生成类型的**默认值**：

```moonbit
// 结构体：所有字段设为默认值
struct DeriveDefault {
  x: Int
  y: String?
}
derive(Default, Eq)

test "derive default struct" {
  let p = DeriveDefault::default()
  assert_true(p == DeriveDefault::{ x: 0, y: None })
}

// 枚举：唯一无参构造器作为默认值
enum DeriveDefaultEnum {
  Case1(Int)
  Case2(label~: String)
  Case3  // ← 这个会成为默认值
}
derive(Default, Eq)

test "derive default enum" {
  assert_true(DeriveDefaultEnum::default() == DeriveDefaultEnum::Case3)
}
```

**限制**：
- ❌ 所有构造器都有参数 → 无法派生
- ❌ 多个无参构造器 → 歧义错误

### 6.5 Hash 特征

使类型可用于 `HashMap` 和 `HashSet`：

```moonbit
struct DeriveHash {
  x: Int
  y: String?
}
derive(Hash, Eq)

test "derive hash" {
  let hs = @hashset.new()
  hs.add(DeriveHash::{ x: 123, y: None })
  hs.add(DeriveHash::{ x: 123, y: None })  // 重复，不会添加
  assert_eq(hs.length(), 1)

  hs.add(DeriveHash::{ x: 123, y: Some("456") })
  assert_eq(hs.length(), 2)
}
```

### 6.6 Arbitrary 特征（测试用）

生成类型的**随机值**，用于属性测试：

```moonbit
struct TestStruct {
  data: Int
}
derive(Arbitrary)

// 可在测试中自动生成随机实例
```

### 6.7 JSON 序列化 (FromJson / ToJson)

自动派生 JSON 序列化和反序列化：

```moonbit
struct JsonTest1 {
  x: Int
  y: Int
}
derive(FromJson, ToJson, Eq)

enum JsonTest2 {
  A(x~: Int)
  B(x~: Int, y~: Int)
}
derive(FromJson(style="legacy"), ToJson(style="legacy"), Eq)

test "json basic" {
  let input = JsonTest1::{ x: 123, y: 456 }
  let expected : Json = { "x": 123, "y": 456 }
  assert_eq(input.to_json(), expected)
  assert_true(@json.from_json(expected) == input)
}
```

#### 枚举序列化样式

有两种枚举序列化样式可选：

**Legacy 样式** (`style="legacy"`):
```json
E::One              => { "$tag": "One" }
E::Uniform(2)       => { "$tag": "Uniform", "0": 2 }
E::Axes(x=-1, y=1)  => { "$tag": "Axes", "x": -1, "y": 1 }
```

**Flat 样式** (`style="flat"`):
```json
E::One              => "One"
E::Uniform(2)       => ["Uniform", 2]
E::Axes(x=-1, y=1)  => ["Axes", -1, 1]
```

#### 高级配置选项

```moonbit
struct JsonAdvanced {
  original_field_name: Int
  another_field: String
}
derive(
  FromJson(fields(original_field_name(rename="renamed"))),
  ToJson(fields(original_field_name(rename="renamed"))),
  Eq,
)
```

**可用的配置参数**：

| 参数 | 作用域 | 说明 |
|------|-------|------|
| `rename` | 字段/构造器 | 重命名 |
| `rename_fields` | 结构体/枚举 | 批量重命名字段 |
| `rename_cases` | 枚举 | 批量重命名构造器 |
| `style` | 枚举 | `"legacy"` 或 `"flat"` |
| `fields(...)` | 结构体 | 控制字段布局 |
| `cases(...)` | 枚举 | 控制构造器布局 |

**批量重命名格式选项**：`lowercase`, `UPPERCASE`, `camelCase`, `PascalCase`, `snake_case`, `SCREAMING_SNAKE_CASE`, `kebab-case`, `SCREAMING-KEBAB-CASE`

#### Option[T] 的特殊处理

```moonbit
struct A {
  x: Int?       // 直接字段 → T | undefined
  y: Int??      // 嵌套 Option → [T] | null
  z: (Int?, Int??)
}
derive(ToJson)
```

---

## Part 7: 库级实践模式（整合自 Part 3.4）

> 以下是编写高质量 MoonBit 库 API 时最常用的 5 种设计模式。

### 模式总览

| 模式 | 核心技术 | 适用场景 |
|------|---------|---------|
| Builder 模式 | 链式 API + 不可变返回 | 复杂对象构建 |
| 策略模式 | Trait 约束 + 泛型 | 可替换算法 |
| Newtype 模式 | 类型包装 + derive | 类型安全 ID |
| Trait 组合 | 小 Trait 继承 | 大型能力抽象 |
| using 导入 | 统一导入语法 | 库接口暴露 |

### 最佳实践要点

✅ **推荐做法**：

1. **优先使用 TypeName::method 语法**：推荐 `fn Point::new(...)` 而非 `fn new(self: Point)`
2. **善用迭代器方法**：`map/filter/fold` 表达意图更清晰
3. **合理使用泛型**：提高复用性，但不过度抽象（YAGNI 原则）
4. **Trait 设计原则**：保持小而聚焦，单一职责，使用 Trait 组合替代大 Trait
5. **善用派生宏**：减少样板代码，`derive(Eq, Compare, Debug, Default, Hash)` 一行搞定
6. **方法 vs 函数**：
   - 属于类型的操作 → **方法** (`Type::method`)
   - 跨类型操作 → **函数** (`operate(a, b)`)
7. **运算符重载**：保持语义一致性（`+` 应该是加法，`==` 应该是相等性）
8. **特征对象**：用于需要**运行时多态**的场景（如插件系统、回调注册）
9. **JSON 派生**：用于调试和人类可读格式；精确控制需手动实现 `FromJson` / `ToJson`
10. **库 API 设计**：
    - 使用 `pub(open) trait` 让外部可实现你的接口
    - 使用 `pub(readonly) trait` 保护内部实现细节
    - 提供 Builder 模式简化复杂对象的构造
    - 使用 Newtype 包装基础类型以获得类型安全

⚠️ **常见陷阱**：

1. **闭包共享可变状态**
   ```moonbit
   let mut count = 0
   let f1 = fn() { count += 1; count }
   let f2 = fn() { count += 1; count }
   // f1() 和 f2() 会互相影响！
   ```

2. **Trait 孤立规则**
   - 不能为外部类型实现外部 Trait
   - 解决方案：使用本地方法扩展 或 新建包装类型 (Newtype)

3. **运算符重载滥用**
   - ❌ 让 `+` 做减法
   - ✅ 保持运算符语义符合直觉

4. **FixedArray 初始化陷阱**
   ```moonbit
   // ⚠️ 错误：所有单元格引用同一对象
   let arr = FixedArray::make(10, FixedArray::make(10, 0))

   // ✅ 正确：每个索引创建独立对象
   let arr = FixedArray::makei(10, fn(_i) {
     FixedArray::make(10, 0)
   })
   ```

5. **泛型约束遗漏**
   ```moonbit
   // ⚠️ 编译错误：T 没有 default 方法
   fn[T] make_array(n : Int) -> Array[T] {
     Array::make(n, T::default())  // ❌
   }

   // ✅ 添加约束
   fn[T : Default] make_array(n : Int) -> Array[T] {
     Array::make(n, T::default())  // ✅
   }
   ```

6. **派生宏的限制**
   - JSON 派生参数可能在未来变更
   - 需要精确控制布局时，应手动实现 `FromJson` / `ToJson`

---

## 决策指南：何时使用？

| 场景 | 推荐技术 | 示例 |
|------|---------|------|
| 简单操作 | 普通函数 | `fn add(a, b)` |
| 一次性逻辑 | 箭头函数 | `arr.map(x => x * 2)` |
| 需要复用 | 闭包 | `make_counter()` |
| 数据转换 | 迭代器方法 | `arr.map/filter/fold` |
| 代码复用 | 泛型函数 | `fn[T] identity(x: T)` |
| 行为抽象 | Trait | `trait Show { ... }` |
| 快速实现 Trait | 派生宏 | `derive(Eq, Show, Debug)` |
| 类型专属操作 | 方法 | `fn Point::distance(self)` |
| 自定义数学类型 | 运算符重载 | `impl Add for Vector` |
| 插件/回调系统 | 特征对象 | `Array[&Handler]` |
| 调试输出 | Debug 派生 | `derive(Debug)` |
| JSON 处理 | JSON 派生 | `derive(FromJson, ToJson)` |
| 库 API 设计 | pub(open) trait + impl | 可扩展的接口设计 |
| 类型安全 ID | Newtype + derive | `struct UserId(Int); derive(Eq, Hash)` |
| 复杂对象构建 | Builder 模式 | `.new().with_x().with_y().build()` |

---

*文档版本: v8.0.0 (迁移自 moonbit-functional/SKILL.md)*
*迁移完成时间: 2026-05-17*
*内容完整性保证: Part 1 ~ Part 7 全部保留，含所有代码示例、表格、v6/v7/v8 增强内容*
