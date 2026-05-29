# 模式匹配 — 完整参考手册

> **来源**: `moonbit-pattern-match/SKILL.md` v6.0.0 + `moonbit-functional/SKILL.md` v8.0.0 额外内容 | **迁移日期**: 2026-05-17
> **原始位置**:
> - `skills/layer1-foundation-path/moonbit-pattern-match/SKILL.md`
> - `skills/layer1-foundation-path/moonbit-functional/SKILL.md` (Part 1.6 + Part 3.5.1 整合)
> **本文件涵盖**: 模式匹配完整体系 + 生产项目实战经验 + 常见陷阱规避指南

---

## 基础匹配

### match 表达式

MoonBit 的 `match` 是表达式，有返回值：

```moonbit
fn classify_number(n: Int) -> String {
  match n {
    0 => "Zero"
    1 | 2 | 3 => "Small positive"
    x if x > 0 => "Positive"
    x if x < 0 => "Negative"
    _ => "Unknown"
  }
}

fn main {
  println(classify_number(0))    // Zero
  println(classify_number(2))    // Small positive
  println(classify_number(10))   // Positive
  println(classify_number(-5))   // Negative
}
```

### 匹配规则

| 模式 | 说明 | 示例 |
|------|------|------|
| 字面值 | 匹配具体值 | `0`, `"hello"` |
| 变量 | 绑定任意值 | `x` |
| 通配符 | 匹配任意值 | `_` |
| 或模式 | 匹配多个值 | `1 \| 2 \| 3` |
| 范围 | 匹配范围 | `1..=10` |
| 守卫条件 | 附加条件 | `x if x > 0` |

## 解构匹配

### 元组解构

```moonbit
fn get_coordinates() -> (Int, Int) {
  (10, 20)
}

fn main {
  let point = (10, 20)

  // match 解构
  match point {
    (0, 0) => println("Origin")
    (x, 0) => println("On x-axis at \(x)")
    (0, y) => println("On y-axis at \(y)")
    (x, y) => println("Point at (\(x), \(y))")
  }
}
```

### 结构体解构

```moonbit
struct User {
  name: String
  age: Int
}

fn greet_user(user: User) -> String {
  match user {
    { name: "Alice", age: _ } => "Hello, Alice!"
    { name, age: 0 } => "Welcome, baby \(name)!"
    { name, age } => "Hello \(name), you are \(age) years old."
  }
}
```

### 枚举解构

```moonbit
enum Shape {
  Circle(Double)
  Rectangle(Double, Double)
  Square(Double)
}

fn area(shape: Shape) -> Double {
  match shape {
    Circle(r) => 3.14159 * r * r
    Rectangle(w, h) => w * h
    Square(s) => s * s
  }
}
```

## 数组匹配

```moonbit
fn describe_list(arr: Array[Int]) -> String {
  match arr {
    [] => "Empty list"
    [single] => "Single element: \(single)"
    [first, ..] => "Starts with \(first)"
    _ => "Multiple elements"
  }
}
```

**更多数组模式变体**：

```moonbit
match arr {
  [] => "empty"
  [x] => "single: \(x)"
  [x, y] => "pair: \(x), \(y)"
  [head, ..rest] => "head: \(head), rest: ..."
}
```

## 守卫条件

```moonbit
fn grade(score: Int) -> String {
  match score {
    s if s >= 90 => "A"
    s if s >= 80 => "B"
    s if s >= 70 => "C"
    s if s >= 60 => "D"
    _ => "F"
  }
}
```

**Option 守卫示例**：

```moonbit
match option {
  Some(x) if x > 0 => "positive: \(x)"
  Some(x) => "non-positive: \(x)"
  None => "none"
}
```

## is 表达式

MoonBit 新增 `is` 表达式，用于检查值是否符合模式：

```moonbit
fn main {
  let x = Some(42)

  // is 表达式返回 Bool
  if x is Some(n) {
    println("Value is \(n)")  // Value is 42
  }

  let arr = [1, 2, 3]
  if arr is [first, ..] {
    println("First element: \(first)")  // First element: 1
  }
}
```

**is 表达式与结构体/枚举结合**：

```moonbit
if value is Some(x) {
  // x 已绑定到 Some 的内部值
  println(x.to_string())
}
```

## 穷尽检查

MoonBit 编译器会检查 match 是否穷尽所有可能：

```moonbit
enum Color {
  Red
  Green
  Blue
}

// 编译错误：未穷尽所有变体
fn bad_match(color: Color) -> String {
  match color {
    Red => "Red"
    Green => "Green"
    // 缺少 Blue 的处理
  }
}

// 正确：穷尽所有变体
fn good_match(color: Color) -> String {
  match color {
    Red => "Red"
    Green => "Green"
    Blue => "Blue"
  }
}
```

## 在 let 中使用模式

```moonbit
fn main {
  let (x, y) = (10, 20)
  let { name, age } = { name: "Alice", age: 30 }

  println("\(name) is \(age) years old")
}
```

## 循环中的模式匹配

```moonbit
fn main {
  let points = [(1, 2), (3, 4), (5, 6)]

  for (x, y) in points {
    println("Point: (\(x), \(y))")
  }
}
```

## 范围模式

```moonbit
match score {
  90..100 => "A"
  80..89 => "B"
  70..79 => "C"
  _ => "F"
}
```

## Map 模式

```moonbit
match map {
  { "x": x, "y": y } => "point: (\(x), \(y))"
  _ => "other map"
}
```

## JSON 模式

```moonbit
match json_value {
  { "name": name, "age": age } => "user: \(name), \(age)"
  _ => "other json"
}
```

---

## 模式匹配常见陷阱与实战 ⭐v6.0新增

> 来自 mbtgraph（MoonBit 图算法库）生产项目中的模式匹配经验

### X.1 Match 分支格式规则（重要！）

**❌ 错误：逗号分隔 + 单行多分支**

```moonbit
match self.matrix[i][idx] { Some(_) => ec = ec + 1; g.matrix[i][idx] = None, None => () }
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

### X.2 Unreachable Code 警告处理

当 match 的模式已经穷尽所有可能时，`_ => ()` 通配分支永远不可达：

```moonbit
match nodes[idx] {
  None => false
  Some(_) => true
  _ => ()   // ⚠️ Warning: unreachable_code — Option 只有 2 个变体
}
```

**修复方法**：删除冗余的 `_` 分支

```moonbit
match nodes[idx] {
  None => false
  Some(_) => true
  // 干净，无警告
}
```

**适用场景（不需要 `_` 通配分支的情况）**：
- `Option` 匹配（Some/None 穷尽）
- 固定变体的枚举匹配
- 元组解构（当编译器能推断穷尽性时）

### X.3 For 循环限制（元组解构）

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

### X.4 范围遍历语法

```moonbit
for i in 0..<n { ... }      // [0, n)，半开区间
for i in 0..=n { ... }     // [0, n]，闭区间
```

**⚠️ 注意**：范围操作符是 `..<` 和 `..=`，不是 `::<` 或其他变体。

### X.5 If 表达式作为返回值

```moonbit
let idx = if slot >= 0 { slot } else { self.nodes.length() }

let (lo, hi) = if fi < ti { (fi, ti) } else { (ti, fi) }
```

**注意**：if-else-if 链作为表达式时，每个分支返回值类型必须一致。

### X.6 While 循环典型用途

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

## 高级应用：编译器管道中的模式匹配 ⭐来自 MoonBash 项目

> 本部分展示模式匹配在真实编译器/解释器项目中的高级应用场景

### 词法分析器中的模式匹配分派

**Token 类型定义（ADT）**

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
```

**核心 tokenize 方法：使用模式匹配分派字符**

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

**标识符 → 关键字映射（模式匹配）**

```moonbit
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
```

### AST 解析中的模式匹配

**表达式类型定义（ADT）**

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

**Parser 主表达式解析（模式匹配 Token 类型）**

```moonbit
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
```

**运算符解析（模式匹配进行 Pratt 解析）**

```moonbit
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
```

### 求值器中的模式匹配分发

**Value 类型和 Env 定义**

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
```

**核心求值函数：使用嵌套模式匹配分发**

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

**模式匹配辅助函数（嵌套元组模式 + 守卫条件）**

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
```

### 编译器管道中模式匹配的设计要点总结

| 阶段 | 数据结构 | 核心技术 | 模式匹配用途 |
|------|---------|---------|-------------|
| 词法分析 | `Token` (ADT) | 模式匹配分派 | 字符 → Token 分类 |
| 语法分析 | `Expr` (ADT) | 递归下降 + 模式匹配 | Token → AST 构建 |
| 语义求值 | `Value` (ADT) + `Env` | 模式匹配分发 | AST → 运行时值 |
| 错误处理 | `Result[T, String]` | 函数式错误传播 | 非穷尽情况捕获 |

---

## 注意事项

- match 必须穷尽所有可能性，否则编译器报错
- 使用 `_` 处理不需要关心的情况
- `is` 表达式是 Bool 类型，只能在条件中使用
- 守卫条件可以添加任意布尔表达式
- 分支间不需要逗号分隔，多语句必须用 `{}` 包裹
- For 循环不支持元组解构，需在内部使用 match
- 当模式已穷尽时，删除冗余的 `_` 通配分支以避免 unreachable_code 警告
- 范围操作符使用 `..<`（半开区间）和 `..=`（闭区间）
- 在生产项目中，模式匹配是构建解释器/编译器的核心技术

---

## 资源索引

- [MoonBit 模式匹配文档](https://docs.moonbitlang.cn/language/index.html)
- [MoonBit 更新日志 - is 表达式](https://www.moonbitlang.cn/updates/page/2)
- [MoonBash - POSIX Shell 解释器](https://github.com/Haoxincode/MoonBash) — 本文档高级应用部分的来源项目
- [mbtgraph - MoonBit 图算法库](https://github.com/...) — 本文档陷阱规避部分的来源项目

---

*文档版本: v6.0.0 (迁移自 moonbit-pattern-match/SKILL.md) + v8.0.0 整合内容*
*迁移完成时间: 2026-05-17*
*内容完整性保证: 全部原样保留 + functional SKILL.md Part 1.6/Part 3.5.1 额外模式匹配内容整合*
*v6.0 新增保留: Match 分支格式规则、Unreachable Code 警告处理、For 循环限制、范围遍历语法、While 循环典型用途*
*高级应用保留: 来自 MoonBash 项目的编译器/解释器管道完整模式匹配实现（Lexer/Parser/Evaluator）*
