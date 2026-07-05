# 编译错误码速查表与常见陷阱

> **来源**: `moonbit-devtools` SKILL.md v7.0.0 | Part 6 (主) + Part 1/2 (附录)
> **实践经验来源**: mbtgraph（MoonBit 图算法库）400+ 行代码实践

---

## 一、错误码速查表

| 错误码 | 含义 | 常见原因 | 修复方式 |
|--------|------|---------|---------|
| **E0029** | `unused_package` | 存在其他编译错误导致 import 看似未使用 | 修复底层错误后自动消失 |
| **E0015** | `unused_mut` | 声明了 `let mut` 但未重新赋值绑定 | 改为 `let`（只需改字段时无需 mut）|
| **E3002** | Parse error | 语法错误（mut self、for 解构、逗号分支等）| 检查具体语法问题 |
| **E4021** | unbound variable | 变量名未定义（通常在 trait 方法中）| 用 `Trait::method(self, ...)` 调用 |
| **E4036** | read-only type | 外部包无法构造 `pub struct` 类型 | 改为 `pub(all) struct` |
| **E4051** | unused_mut (warning) | 同 E0015 | 改为 `let` |
| **E4087** | immutable field | 字段缺少 `mut` 声明 | 添加 `mut` 关键字 |
| **E4145** | sealed trait | 无法实现 `pub trait`（密封 trait）| 改为 `pub(open)trait` |
| **E4014** | type mismatch | 类型不匹配（如元组解构变量对应错误）| 检查解构变量名和类型 |

### 错误码优先级处理策略

```
高优先级（立即修复）
├── E3002: 语法错误 - 阻止编译
├── E4036/E4145: 可见性问题 - 影响跨包使用
└── E4014: 类型错误 - 运行时风险

中优先级（尽快修复）
├── E0015/E4051: unused_mut - 代码质量问题
├── E4087: immutable field - 功能性错误
└── E4021: unbound variable - 逻辑错误

低优先级（可延后）
└── E0029: unused_package - 级联伪错误
```

---

## 二、八大常见陷阱与修复

### 陷阱 1：mut self 参数 ⚠️

```moonbit
// ❌ MoonBit 不支持
impl Trait for Struct with method(mut self, x) -> T { ... }

// ✅ 内部按需绑定可变副本
impl Trait for Struct with method(self, x) -> T {
  let mut s = self
}
```

**触发场景**：从 Rust 迁移代码时常见，Rust 允许 `&mut self` 但 MoonBit 不支持。

---

### 陷阱 2：For 循环元组解构 ⚠️

```moonbit
// ❌ MoonBit 不支持
for (a, b) in array_of_pairs { ... }

// ✅ 先绑定再 match
for pair in array_of_pairs {
  match pair {
    (a, b) => ...
  }
}
```

**触发场景**：遍历元组数组时直接解构，Python/Rust 风格的写法在 MoonBit 中不支持。

---

### 陷阱 3：函数返回值上链式调用 ⚠️

```moonbit
// ❌ 可能触发解析问题
fn get_sorted() -> Array[Int] { ... }
get_sorted().iter()

// ✅ 分两步写
let sorted = get_sorted()
sorted.iter()
```

**触发场景**：复杂表达式链式调用时，编译器可能产生歧义。

---

### 陷阱 4：Match 分支内多条语句 ⚠️

```moonbit
// ❌ 单行多语句 + 逗号分隔
match x {
  Some(v) => do_a(v); do_b(v),
  None => ()
}

// ✅ 多语句用 {} 包裹，分支间无逗号
match x {
  Some(v) => {
    do_a(v)
    do_b(v)
  }
  None => ()
}
```

**触发场景**：match 分支需要执行多个操作时的语法问题。

---

### 陷阱 5：构造只读类型 🔴

```moonbit
// core 中定义为 pub struct Node { id: NodeId, data: Double }
// storage 中无法构造：

// ❌ Cannot create values of read-only type: Node
let n = { id: NodeId(0), data: 1.0 }

// ✅ core 中改为 pub(all) struct 即可解决
```

**规则**：如果外部包需要构造某个类型，必须用 `pub(all)`。

**适用场景**：
- 跨包数据传递
- 外部包需要创建实例
- 测试代码构造测试数据

**对比表**：

| 可见性修饰符 | 包内构造 | 外部包构造 | 适用场景 |
|------------|---------|-----------|---------|
| `pub struct` | ✅ | ❌ 只读 | 内部实现细节 |
| `pub(all) struct` | ✅ | ✅ | 公开 API 类型 |

---

### 陷阱 6：实现密封 Trait 🔴

```moonbit
// core 中: pub trait GraphWritable { fn add_node(...) }
// storage 中:

// ❌ cannot implement sealed trait 'GraphWritable'
impl @core.GraphWritable for MyGraph with add_node(...) { ... }

// ✅ core 中改为 pub(open)trait GraphWritable { ... }
```

**规则**：如果需要在外部包实现 trait，必须用 `pub(open)trait`。

**适用场景**：
- 插件系统
- 策略模式实现
- 跨包接口扩展

**对比表**：

| Trait 可见性 | 包内实现 | 外部包实现 | 设计意图 |
|------------|---------|-----------|---------|
| `pub trait` | ✅ | ❌ 密封 | 控制实现范围 |
| `pub(open) trait` | ✅ | ✅ 开放 | 允许扩展 |

---

### 陷阱 7：Trait 方法中的 unbound 标识符 🔴

```moonbit
impl GraphReadable for MyGraph with degree(self, id) -> Int {
  // 在 impl 内部不能直接调用同 trait 的其他方法：
  neighbors(self, id).length()   // ❌ neighbors 未绑定

  // ✅ 必须使用完全限定名
  @core.GraphReadable::neighbors(self, id).to_array().length()
  // 或者直接实现逻辑而不委托
}
```

**原因分析**：
- MoonBit 的 trait 实现块中，同 trait 的方法不会自动绑定到作用域
- 这与 Rust 的行为不同，Rust 可以直接调用 `self.method()`

**解决方案**：

| 方案 | 适用场景 | 示例 |
|------|---------|------|
| 完全限定名 | 调用同 trait 其他方法 | `@Trait::method(self, args)` |
| 直接内联 | 简单逻辑避免委托 | 直接写实现代码 |
| 辅助函数 | 复杂逻辑提取 | 在 impl 外定义 helper 函数 |

---

### 陷阱 8：元组解构变量对应错误 🟡

```moonbit
// adj 存储 (NodeId, Double)，即 (nid, weight)
for entry in self.adj[idx] {
  match entry {
    (_, w) => {
      // w 是 Double（权重），不是 NodeId！
      g = al_remove_rev(g, w.0, idx)  // ❌ Double 没有 .0
    }
  }
}

// ✅ 正确的变量命名
match entry {
  (nid, _) => {
    g = al_remove_rev(g, nid.0, idx)  // nid.0 是 Int（NodeId 的内部索引）
  }
}
```

**教训**：解构时变量名要有意义，避免用单字母导致混淆。

**最佳实践**：

```moonbit
// ✅ 有意义的变量名
match entry {
  (node_id, weight) => {
    // node_id 明确表示 NodeId
    // weight 明确表示 Double
    process_node(node_id, weight)
  }
}

// ❌ 容易混淆的单字母
match entry {
  (a, b) => {
    // a 和 b 的含义不明确
    process(a, b)
  }
}
```

---

## 三、诊断修复标准工作流

遇到编译错误时的标准流程：

```
┌─────────────────────────────────────────────────────────────┐
│  编译错误诊断修复流程                                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ① 格式化与信息收集                                           │
│     moon fmt && moon info                                    │
│           │                                                 │
│           ▼                                                 │
│  ② 定位第一个真正的错误                                       │
│     （排除级联产生的伪错误）                                   │
│           │                                                 │
│           ▼                                                 │
│  ③ 对照错误码速查表                                           │
│     找到对应的陷阱模式                                        │
│           │                                                 │
│           ▼                                                 │
│  ④ 应用修复方案                                              │
│     （参考第二节的具体示例）                                  │
│           │                                                 │
│           ▼                                                 │
│  ⑤ 验证修复结果                                              │
│     重新运行 moon info 确认 Exit code 0                      │
│           │                                                 │
│           ▼                                                 │
│  ⑥ IDE 确认                                                  │
│     GetDiagnostics 确认无警告                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 关键原则

**原则 1：总是从第一个真正的错误开始修复**

```bash
# ❌ 从最后一个错误开始修复
# 可能是级联产生的伪错误，修复后仍会报错

# ✅ 从第一个错误开始
moon info | head -20  # 查看前 20 行错误
```

**原则 2：区分真正的错误和级联错误**

| 特征 | 真正的错误 | 级联错误（伪错误） |
|------|----------|------------------|
| 位置 | 语法/类型问题的实际位置 | 受影响的下游位置 |
| 数量 | 通常 1-3 个核心错误 | 可能出现大量相关错误 |
| 修复效果 | 修复后错误消失 | 修复底层错误后自动消失 |
| 典型例子 | E3002、E4036、E4014 | E0029（unused_package）|

**原则 3：批量修复 vs 逐步修复**

```bash
# 场景 A：同一类错误批量出现（如多个 unused_mut）
# → 可以批量修复，统一将 let mut 改为 let

# 场景 B：不同类型错误交织
# → 必须逐步修复，每次只修一个错误再验证
```

### 常见错误组合模式

**模式 1：可见性连锁反应**
```
E4036 (read-only type)
  └→ E4021 (unbound variable) - 无法构造类型导致变量未定义
      └→ E0029 (unused_package) - 导入看似未使用
```
**修复顺序**：先修 E4036 → 后续自动消失

**模式 2：语法错误级联**
```
E3002 (parse error)
  └→ E4014 (type mismatch) - 解析失败导致类型推断错误
      └→ E0015 (unused_mut) - 类型错误影响 mut 分析
```
**修复顺序**：先修 E3002 → 重新编译检查

**模式 3：Trait 实现链**
```
E4145 (sealed trait)
  └→ E4021 (unbound variable) - 无法实现 trait 导致方法未绑定
      └→ E4014 (type mismatch) - 方法返回类型未知
```
**修复顺序**：先修 E4145 → 重新编译检查

---

## 附录 A：测试系统基础（Part 1）

> 来源：`moonbit-devtools` SKILL.md v7.0.0 Part 1

### 测试块基础

MoonBit 提供**内联测试代码块**，用于编写测试用例：

```moonbit
test "test_name" {
  assert_eq(1 + 1, 2)
  assert_eq(2 + 2, 4)
  inspect([1, 2, 3], content="[1, 2, 3]")
}
```

**关键特点**：
- 本质上是一个返回 `Unit` 抛出 `Error` 的函数
- 签名等价于 `Unit!Error`
- 在执行 `moon test` 期间被调用
- 字符串 `"test_name"` **可选**，用于标识测试用例
- `assert_eq` 来自标准库，失败时打印错误信息并终止测试

#### Panic 测试

如果测试名称以 `"panic"` 开头，表示**预期触发 panic**：

```moonbit
test "panic_test" {
  let _ : Int = Option::None.unwrap()
  // 只有触发 panic 时测试才会通过
}
```

#### 快照测试

检查实现了 `Show` 特征的任何内容：

```moonbit
struct X { x: Int }
derive(Debug)

test "show snapshot test" {
  debug_inspect({ x: 10 }, content="{ x: 10 }")
}
```

**使用 `moon test --update` 自动插入或更新预期值**

#### 快照 JSON

生成结构化的 JSON 输出：

```moonbit
enum Rec {
  End
  Really_long_name_that_is_difficult_to_read(Rec)
}
derive(Debug, ToJson)

test "json snapshot test" {
  let r = Really_long_name_that_is_difficult_to_read(
    Really_long_name_that_is_difficult_to_read(
      Really_long_name_that_is_difficult_to_read(End),
    ),
  )
  debug_inspect(r, content="...")
  json_inspect(r, content=[
    "Really_long_name_that_is_difficult_to_read",
    [
      "Really_long_name_that_is_difficult_to_read",
      ["Really_long_name_that_is_difficult_to_read", "End"],
    ],
  ])
}
```

#### 黑盒测试和白盒测试

| 类型 | 文件后缀 | 访问权限 | 用途 |
|------|---------|---------|------|
| **白盒测试** | `_wbtest.mbt` | 包中所有成员 | 内部实现验证 |
| **黑盒测试** | `_test.mbt` | 仅公开成员 | API 用户体验 |

**导入规则**：
- **WhiteBox** (`_wbtest.mbt`)：导入 `import` + `wbtest-import` 中的包
- **BlackBox** (`_test.mbt`)：导入当前包 + `import` + `test-import` 中的包

---

## 附录 B：基准测试（Part 2）

> 来源：`moonbit-devtools` SKILL.md v7.0.0 Part 2

### 基本基准测试

使用带有 `@bench.T` 参数的测试块进行性能测量：

```moonbit
fn fib(n : Int) -> Int {
  if n < 2 {
    return n
  }
  return fib(n - 1) + fib(n - 2)
}

test (b : @bench.T) {
  b.bench(fn() { b.keep(fib(20)) })
}
```

**输出示例**：
```
time (mean ± σ)   range (min … max)
  21.67 µs ± 0.54 µs   21.28 µs … 23.14 µs in 10 × 4619 runs
```

**关键点**：
- `@bench.T::bench` 自动确定合适的迭代次数
- `@bench.T::keep` **防止计算被优化掉**（纯函数必须使用）

### 批量基准测试

比较同一函数的多个实现：

```moonbit
fn fast_fib(n : Int) -> Int {
  if n < 2 { return n }
  else {
    let mut a = 0
    let mut b = 1
    for i = 2; i <= n; i = i + 1 {
      let t = a + b
      a = b
      b = t
    }
    b
  }
}

test (b : @bench.T) {
  b.bench(name="naive_fib", fn() { b.keep(fib(20)) })
  b.bench(name="fast_fib", fn() { b.keep(fast_fib(20)) })
}
```

### 原始统计数据导出

```moonbit
fn collect_bench() -> Unit {
  let mut saved = 0
  let summary : @bench.Summary = @bench.single_bench(name="fib", fn() {
    saved = fib(20)
  })
  println(saved)
  println(summary.to_json().stringify())
}
```

**输出字段**（JSON 格式）：
```json
{
  "name": "fib",
  "sum": 217.22,
  "min": 21.62,
  "max": 21.87,
  "mean": 21.72,
  "median": 21.70,
  "var": 0.0072,
  "std_dev": 0.085,
  "std_dev_pct": 0.39,
  "median_abs_dev": 0.082,
  "median_abs_dev_pct": 0.38,
  "quartiles": [21.67, 21.70, 21.76],
  "iqr": 0.092,
  "batch_size": 4594,
  "runs": 10
}
```

**注意**：时间单位为微秒（µs），`Summary` 类型的内部字段不保证稳定性。

---

*文档版本: v7.0.0 (from moonbit-devtools SKILL.md)*
*生成日期: 2026-05-17*
