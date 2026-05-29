# MoonBit 常见陷阱与错误排查 ⚠️

> 整合自 devtools、functional、pattern-match、data-types、project-layout 等多个技能的生产经验

## 一、Top 10 错误码速查表 📋

| 错误码 | 含义 | 常见原因 | 快速修复 |
|--------|------|---------|---------|
| **E0001** | 语法错误 | 括号/分号不匹配 | 检查括号配对 |
| **E0015** | unused_mut 警告 | 声明了 mut 但未重新赋值 | 改为 `let x`（非mut）|
| **E0029** | unused_package | import 未被使用 | 修复其他编译错误后自动消失 |
| **E0030** | 循环依赖 | 包 A 引用 B，B 又引用 A | 重构为单向依赖 |
| **E3002** | Parse error | match 分支格式错误 | 分支独占行 + 多语句用 {} |
| **E3XXX** | 类型错误 | 类型不匹配 | 检查返回值和参数类型 |
| **E4XXX** | 模块错误 | 包路径/别名问题 | 检查 moon.pkg 配置 |
| **E5XXX** | FFI 错误 | 外部函数声明问题 | 检查 extern 声明语法 |
| **WXXXX** | Warning | 各种警告信息 | 根据具体警告处理 |
| **unreachable_code** | 不可达代码 | match 已穷尽但有多余分支 | 删除冗余 `_` 分支 |

---

## 二、8 大高频陷阱详解（含 ❌✅ 对比）⭐

### 陷阱 1：Match 分支格式错误 (E3002)

**❌ 错误：逗号分隔 + 单行多语句**

```moonbit
match self.matrix[i][idx] {
  Some(_) => ec = ec + 1; g.matrix[i][idx] = None,
  None => ()
}
// E3002: Parse error — 分支内多条语句需要块包裹
```

**✅ 正确：每个分支独占行，多语句用 {} 包裹**

```moonbit
match self.matrix[i][idx] {
  Some(_) => {
    ec = ec + 1
    g.matrix[i][idx] = None
  }
  None => ()
}
```

**核心规则**：
- 分支间**不需要逗号分隔**
- 多条语句必须用 `{}` 包裹
- 单行单语句可省略 `{}`
- 保持每个分支独占一行，提高可读性

---

### 陷阱 2：Unreachable Code 警告

当 match 的模式已经穷尽所有可能时，`_ => ()` 通配分支永远不可达：

```moonbit
// ❌ 有警告
match nodes[idx] {
  None => false
  Some(_) => true
  _ => ()   // ⚠️ Warning: unreachable_code — Option 只有 2 个变体
}

// ✅ 干净，无警告
match nodes[idx] {
  None => false
  Some(_) => true
}
```

**适用场景（不需要 `_` 通配分支的情况）**：
- `Option` 匹配（Some/None 穷尽）
- 固定变体的枚举匹配
- 元组解构（当编译器能推断穷尽性时）

---

### 陷阱 3：For 循环不支持元组解构

**⚠️ For 循环不支持元组解构**：

```moonbit
// ❌ 编译错误
for (a, b) in pair_array { ... }

// ✅ 正确做法：先绑定，再 match 解构
for pair in pair_array {
  match pair {
    (a, b) => do_work(a, b)
  }
}
```

这是 MoonBit 当前的语法限制，需要在 for 循环内额外写一层 match。

---

### 陷阱 4：可变性语义陷阱 (E0015)

#### ⚠️ 不支持 mut self 参数

```moonbit
// ❌ 错误：MoonBit 不支持 mut self
impl GraphWritable for MyGraph with add_node(mut self, data) -> NodeId {
  self.nodes.push(...)
}

// ✅ 正确：使用 (self)，内部绑定可变副本
impl GraphWritable for MyGraph with add_node(self, data) -> NodeId {
  let g = self
  g.nodes.push(...)
  result
}
```

#### 两层可变性机制

**层级 1：字段级 mut（声明时决定）**
```moonbit
pub struct MyGraph {
  mut node_cnt : Int       // 字段本身是可变的
  nodes : Array[Node?]     // 字段不可变（但数组内容可通过 API 变更）
}
```

**层级 2：绑定级 mut（let mut vs let）**
```moonbit
let g = self                    // 普通 binding
g.node_cnt = g.node_cnt + 1   // ✅ 因为字段声明了 mut

let mut g = self                // 可变 binding
g = some_other_value           // ✅ 因为绑定了 mut
g.node_cnt = g.node_cnt + 1    // ✅ 同时也支持字段修改
```

**核心规则**：
> **如果只需要修改结构体的字段（push、索引赋值等），不需要 `let mut`。只有需要重新赋值变量本身时才需要 `let mut`。**

#### E0015 unused_mut 警告处理

```moonbit
fn bad_example(self : MyGraph) -> Int {
  let mut g = self
  g.node_cnt = g.node_cnt + 1   // 只改了字段，没重新赋值 g 本身
  // ⚠️ Warning: unused_mut — g 的 mut 从未使用
  g.node_cnt
}

fn fixed_example(self : MyGraph) -> Int {
  let g = self                  // 改为普通 binding
  g.node_cnt = g.node_cnt + 1   // ✅ 字段修改仍然有效
  g.node_cnt
}
```

**判断方法**：问自己：这个函数中是否有 `g = ...` 这样的**重新赋值语句**？
- 有 → 需要 `let mut g`
- 没有 → 用 `let g` 即可

#### 快速检查清单

| 操作类型 | 需要 `let mut`？ | 示例 |
|---------|-----------------|------|
| 字段赋值 | ❌ | `g.field = new_value` |
| 数组 push | ❌ | `g.arr.push(elem)` |
| 索引赋值 | ❌ | `g.arr[i] = value` |
| Map 插入 | ❌ | `g.map.set(key, val)` |
| 变量重新赋值 | ✅ | `g = some_function(g)` |
| 循环累加 | ✅ | `for ... { g = update(g) }` |

---

### 陷阱 5：可见性决策失误

来自 mbtgraph 生产项目的可见性决策记录：

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

**❌ 常见错误**：过度使用 `pub(all)` 导致内部实现暴露过多

```moonbit
// ❌ 错误：所有类型都 pub(all)
pub(all) struct InternalCache { ... }   // 不应该暴露
pub(all) fn _helper() -> Int { ... }     // 内部函数不应该公开

// ✅ 正确：按需选择可见性
struct InternalCache { ... }             // 默认 priv
pub(all) struct PublicAPI { ... }        // 真正需要公开的类型
pub(open) trait Extensible { ... }       // 需要外部实现的 trait
```

---

### 陷阱 6：Option 匹配遗漏

**❌ 错误：忘记处理 None 情况**

```moonbit
fn get_user_name(user : Option[User]) -> String {
  match user {
    Some(u) => u.name
    // ❌ 缺少 None 处理 → 编译错误
  }
}

// ✅ 正确：穷尽所有情况
fn get_user_name(user : Option[User]) -> String {
  match user {
    Some(u) => u.name
    None => "Unknown User"
  }
}
```

**最佳实践**：使用 `unwrap_or` / `map` / `and_then` 简化代码

```moonbit
// 更简洁的方式
fn get_user_name(user : Option[User]) -> String {
  user.map(u => u.name).unwrap_or("Unknown User")
}
```

---

### 陷阱 7：元组解构变量混淆

**❌ 错误：使用无意义的变量名**

```moonbit
match entry {
  (a, b) => process(a, b)      // a 和 b 是什么？
  _ => ()
}
```

**✅ 正确：使用有意义的变量名**

```moonbit
match entry {
  (node_id, weight) => process(node_id, weight)  // 明确语义
  _ => ()
}
```

**经验法则**：
- 元组第一个元素通常表示 ID 或 key
- 第二个元素通常表示关联数据或 value
- 使用下划线前缀忽略不需要的值：`(node_id, _)`

---

### 陷阱 8：E0029 unused_package 误报

```
Error: unused_package: @core is imported but unused
```

**原因**：不是真的未使用，而是文件中存在**其他编译错误**导致 import 看起来"未被消费"。

**修复方法**：
1. 先修复文件中的其他编译错误
2. E0029 会自动消失
3. 如果仍然存在，检查是否真的没有使用该包

```bash
# 排查步骤
moon check          # 1. 运行完整检查
moon info           # 2. 查看 .mbti 接口变更
git diff "*.mbti"   # 3. 检查接口是否真的变化
```

---

## 三、模式匹配专项陷阱 🔍

### 3.1 Match 分支格式速记

```
✅ 正确格式：
match expr {
  Pattern1 => single_statement
  Pattern2 => {
    statement_1
    statement_2
  }
  _ => default_case
}

❌ 错误格式：
match expr { P1 => s1; s2, P2 => s3 }    // 缺少 {}
match expr {                               // 逗号分隔错误
  P1 => s1,
  P2 => s2
}
```

### 3.2 范围遍历语法

```moonbit
for i in 0..<n { ... }      // [0, n)，半开区间
for i in 0..=n { ... }     // [0, n]，闭区间
```

**⚠️ 注意**：范围操作符是 `..<` 和 `..=`，不是 `::<` 或其他变体。

### 3.3 If 表达式作为返回值

```moonbit
let idx = if slot >= 0 { slot } else { self.nodes.length() }

let (lo, hi) = if fi < ti { (fi, ti) } else { (ti, fi) }
```

**注意**：if-else-if 链作为表达式时，每个分支返回值类型必须一致。

### 3.4 While 循环典型用途

当 for 的范围不够灵活时使用 while：

```moonbit
let mut i = 0
while i < idx {
  for entry in self.adj[i] {
    match entry {
      (nid, _) => if nid == id { d = d + 1 }
    }
  }
  i = i + 1
}
```

**典型用途**：
- 无向图 `neighbors()` / `degree()` 中扫描前置行
- 冒泡排序的多层循环
- 条件动态变化的迭代

---

## 四、项目配置陷阱 📁

### 4.1 moon.pkg 和 moon.pkg.json 不能共存

```
同一目录下不能同时存在 moon.pkg 和 moon.pkg.json
```

**解决方法**：
- 选择一种格式（推荐新格式 `moon.pkg`）
- 删除另一种格式的文件

### 4.2 supported-targets vs targets 混淆

| 特性 | `supported-targets` | `targets` |
|------|---------------------|-----------|
| **作用域** | 包级元数据 | 文件级条件编译规则 |
| **用途** | 声明该包**打算支持哪些后端** | 为不同后端**包含或排除单独文件** |
| **影响** | 影响包的发布和依赖解析 | 影响哪些文件参与编译 |

### 4.3 同包调用规则

同一 `moon.pkg` 目录下的 `.mbt` 文件属于**同一个包**，函数直接调用，**不需要模块前缀**：

```moonbit
// shared_helpers.mbt 中定义
pub fn has_node(nodes : Array[Node?], idx : Int) -> Bool { ... }

// directed_adj_list.mbt 中使用（同包，无需前缀）
has_node(self.nodes, idx)        // ✅ 正确
shared_helpers::has_node(...)     // ❌ 错误：同包不需要前缀
```

---

## 五、调试技巧速查 🛠️

### 5.1 常用调试命令

```bash
moon check              # 完整类型检查
moon test               # 运行测试
moon bench              # 性能基准测试
moon info               # 查看 .mbti 接口
moon fmt                # 格式化代码
moon build --target xxx # 指定后端构建
```

### 5.2 GDB/LLDB 调试 Native 后端

```bash
# Linux (GDB)
gdb ./_build/native/release/main
(gdb) break main
(gdb) run
(gdb) next
(gdb) print variable_name

# macOS (LLDB)
lldb ./_build/native/release/main
(lldb) break set --name main
(lldb) run
(lldb) next
(lldb) frame variable
```

### 5.3 .mbti 接口文件检查

```bash
moon info                          # 生成/更新 .mbti
git diff -- "*.mbti"               # 检查接口变更
```

**意义**：
- `.mbti` 不变 → 改动是内部实现细节
- `.mbti` 变更 → 公开 API 变化，需评估影响

---

## 六、陷阱预防清单 ✅

### 开发阶段

- [ ] 使用 `moon check` 进行持续类型检查
- [ ] Match 表达式确保穷尽所有情况
- [ ] 避免不必要的 `let mut`（减少 E0015）
- [ ] 合理选择可见性修饰符
- [ ] 同包内函数直接调用，不加前缀

### Code Review 阶段

- [ ] 检查是否有 unreachable code 警告
- [ ] 确认 Option/Enum 匹配完整性
- [ ] 验证元组解构变量命名有意义
- [ ] 审查 pub(all)/pub(open) 是否必要
- [ ] 确认 moon.pkg 配置正确

### 发布前

- [ ] 运行 `moon test` 确保测试通过
- [ ] 执行 `moon fmt` 格式化代码
- [ ] 检查 `.mbti` 接口变更影响
- [ ] 多后端构建测试（wasm/js/native）
- [ ] Release 模式性能验证

---

## 七、快速参考卡片 📝

### Match 格式速查卡

```
┌─────────────────────────────────────┐
│  MoonBit Match 表达式速查            │
├─────────────────────────────────────┤
│  ✅ 单语句: Pat => expr             │
│  ✅ 多语句: Pat => { stmt; stmt }  │
│  ❌ 错误: Pat => s1; s2, Pat => s3 │
│  💡 提示: 分支间无需逗号            │
└─────────────────────────────────────┘
```

### 可变性速查卡

```
┌─────────────────────────────────────┐
│  MoonBit 可变性速查                  │
├─────────────────────────────────────┤
│  字段修改: let g = self (无需mut)   │
│  变量重赋: let mut g = self         │
│  mut self: ❌ 不支持                 │
│  E0015: 删除无用 mut                │
└─────────────────────────────────────┘
```

### 可见性速查卡

```
┌─────────────────────────────────────┐
│  MoonBit 可见性速查                  │
├─────────────────────────────────────┤
│  pub(all): 外部构造类型             │
│  pub(open): 外部实现 trait           │
│  pub: 外部读取                      │
│  priv(默认): 仅包内访问             │
└─────────────────────────────────────┘
```

---

*文档版本: v1.0.0 | 最后更新: 2026-05-17*
*来源: devtools Part 6 + functional Part 4.5 + pattern-match 陷阱 + data-types 可见性 + project-layout E0029*
