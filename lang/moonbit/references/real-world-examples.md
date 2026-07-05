# MoonBit 真实项目案例集 🌟

> 基于生产级 MoonBit 开源项目提取的真实架构模式、关键代码片段和经验数据

## 项目概览

| 项目 | 地址 | 类型 | 核心技术 | 复杂度 |
|------|------|------|---------|--------|
| 🎬 **moon-lottie** | [GitHub](https://github.com/cg-zhou/moon-lottie) | 动画渲染引擎 | 多层架构 + 双运行时 + Trait 抽象 | ⭐⭐⭐⭐ |
| 🐚 **MoonBash** | [GitHub](https://github.com/Haoxincode/MoonBash) | Shell 解释器 | 编译器管道 + ADT + JS 优化 | ⭐⭐⭐ |
| 🗄️ **morm** | [GitHub](https://github.com/oboard/morm) | ORM 框架 | 属性驱动 DSL + 代码生成 + 方言抽象 | ⭐⭐⭐ |
| 🔢 **mbtgraph** | [GitHub](https://github.com/morning-start/mbtgraph) | 图算法库 | 有向/无向分离 + Trait 多态 + Builder 模式 | ⭐⭐⭐ |

---

## 一、🎬 moon-lottie — Lottie 动画渲染引擎

**项目地址**: https://github.com/cg-zhou/moon-lottie

### 1.1 架构设计模式（多层架构）

```
moon-lottie/
├── lib/                          # 🔧 Core Engine（核心引擎）
│   ├── core/
│   │   ├── animation.mbt        # 动画数据模型
│   │   ├── layer.mbt            # 图层数据结构
│   │   ├── transform.mbt        # 变换计算
│   │   └── easing.mbt           # 缓动函数
│   ├── renderer/
│   │   ├── canvas.mbt           # Canvas 渲染器
│   │   ├── svg.mbt              # SVG 渲染器
│   │   └── context.mbt          # 渲染上下文
│   └── parser/
│       ├── lottie_json.mbt      # Lottie JSON 解析器
│       └── validator.mbt        # 数据验证
│
├── cmd/                          # 🚀 运行时 & 工具
│   ├── player_runtime/          # Wasm-GC / JS 运行时
│   │   ├── bridge.mbt           # 平台桥接层
│   │   └── event_loop.mbt       # 事件循环
│   └── svg_cli/                 # SVG 导出 CLI 工具
│       └── main.mbt
│
├── packages/                     # 📦 Frontend SDKs（语言绑定）
│   ├── js-binding/               # JavaScript 绑定
│   │   ├── package.json
│   │   └── src/index.ts
│   ├── react-lottie/             # React 组件封装
│   │   ├── package.json
│   │   └── src/LottiePlayer.tsx
│   └── web-component/            # Web Component 封装
│       ├── package.json
│       └── src/LottieElement.ts
│
└── demo/                         # 🎮 Playground（演示/测试）
    └── playground/
        ├── moon.pkg
        └── main.mbt
```

**架构原则**：

| 层次 | 职责 | 发布形式 |
|------|------|---------|
| `lib/core` | 纯算法和数据结构，无平台依赖 | mooncakes 库 |
| `lib/renderer` | 平台抽象接口 | mooncakes 库 |
| `cmd/*` | 平台特定实现 | 可执行程序 |
| `packages/*` | 生态集成（npm 包） | npm publish |
| `demo` | 验证和演示 | 不发布 |

### 1.2 关键设计决策

#### 决策 1：核心零依赖

`lib/core` 不依赖任何平台 API，可跨后端编译：

```moonbit
// lib/core/easing.mbt — 纯算法实现，无任何外部依赖
pub fn ease_in_out_cubic(t : Float) -> Float {
  if t < 0.5 {
    4.0 * t * t * t
  } else {
    1.0 - (-2.0 * t + 2.0).powi(3) / 2.0
  }
}

pub fn lerp(a : Float, b : Float, t : Float) -> Float {
  a + (b - a) * t
}
```

**经验数据**：纯算法模块可同时编译到 wasm-gc 和 js 后端，无需任何修改。

#### 决策 2：渲染器抽象 Trait

定义 `Renderer` Trait，各平台自由实现：

```moonbit
// lib/renderer/context.mbt — 平台抽象接口
pub(open) trait Renderer {
  draw_rect(self : Self, x : Float, y : Float, w : Float, h : Float, color : Color) -> Unit
  draw_path(self : Self, points : Array[Point], stroke : StrokeStyle) -> Unit
  save(self : Self) -> Unit
  restore(self : Self) -> Unit
  set_transform(self : Self, matrix : Matrix) -> Unit
}
```

### 1.3 Wasm-GC + JS 双运行时模式 ⭐

来自 multi-backend Chapter 7 的生产级双后端架构：

#### 为什么需要双运行时？

| 场景 | Wasm-Gc 后端 | JS 后端 |
|------|-------------|---------|
| 浏览器核心引擎 | ✅ 最佳（性能+体积） | ❌ 不适合 |
| Node.js 工具链 | ❌ 无法访问 FS | ✅ 最佳 |
| 边缘计算 | ✅ V8 Isolate 支持 | ✅ 也支持 |
| 调试体验 | 🟡 中等（WAT 调试） | 🟢 优秀（Chrome DevTools） |
| 生态集成 | 🟡 需要 FFI 桥接 | 🟢🟢 原生 npm |

#### 架构设计图

```
┌─────────────────────────────────────────────┐
│              平台无关层 (lib/)                │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │ core    │ │ parser  │ │ algo    │       │
│  │ 纯算法   │ │ 数据解析 │ │ 通用逻辑 │       │
│  └────┬────┘ └────┬────┘ └────┬────┘       │
│       └──────────┼──────────┘              │
│                  ▼                           │
│        ┌──────────────────┐                 │
│        │ Platform Trait   │  ← 抽象接口     │
│        └────────┬─────────┘                 │
└─────────────────┼───────────────────────────┘
                  │ implements
        ┌─────────┴─────────┐
        ▼                   ▼
┌───────────────┐  ┌───────────────┐
│ Wasm-GC 运行时 │  │   JS 运行时    │
│ cmd/wasm_rt/  │  │ cmd/js_rt/    │
│               │  │               │
│ • Canvas API  │  │ • DOM API     │
│ • requestAnimationFrame│ • fetch   │
│ • Web Workers │  │ • fs/promises │
└───────────────┘  └───────────────┘
```

#### 平台抽象 Trait 设计示例

```moonbit
pub(open) trait PlatformRenderer {
  create_canvas(Self, Int, Int) -> CanvasHandle
  clear_canvas(Self, CanvasHandle, String) -> Unit
  draw_rect(Self, CanvasHandle, Rect, FillStyle) -> Unit
  draw_path(Self, CanvasHandle, PathData, StrokeStyle) -> Unit
  set_transform(Self, CanvasHandle, Transform) -> Unit
  
  request_animation_frame(Self, () -> Unit) -> Int
  add_event_listener(Self, String, EventHandler) -> Unit
  now_ms(Self) -> Int
  
  load_image(Self, String) -> Result[ImageHandle, String]
  log(Self, String) -> Unit
}

impl PlatformRenderer for WasmRuntime with create_canvas(self, w, h) {
  extern "js" fn js_create_canvas(w : Int, h : Int) -> CanvasHandle =
    "(w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }"
  js_create_canvas(w, h)
} with request_animation_frame(self, cb) {
  extern "js" fn js_raf(cb : () -> Unit) = "(cb) => requestAnimationFrame(cb)"
  js_raf(cb)
} with now_ms(self) {
  extern "js" fn js_now() -> Int = "() => performance.now()"
  js_now()
}

impl PlatformRenderer for JsRuntime with create_canvas(self, w, h) {
  if self.is_browser { create_dom_canvas(w, h) }
  else { create_offscreen_canvas(w, h) }
} with log(self, msg) {
  println("[JS Runtime] " + msg)
}
```

#### 双目标构建脚本

```bash
#!/bin/bash
set -e
PROJECT_NAME="my_project"
BUILD_DIR="_build"

echo "=== Building ${PROJECT_NAME} ==="

echo "[1/3] Building Wasm-Gc target..."
moon build --target wasm-gc --release
mkdir -p ${BUILD_DIR}/wasm
cp target/wasm-gc/release/*.wasm ${BUILD_DIR}/wasm/

echo "[2/3] Building JavaScript target..."
moon build --target js --release
mkdir -p ${BUILD_DIR}/js
cp -r target/js/release/* ${BUILD_DIR}/js/

echo "[3/3] Generating package metadata..."
cat > ${BUILD_DIR}/package.json << 'EOF'
{
  "name": "my-project",
  "version": "0.1.0",
  "type": "module",
  "main": "./js/index.mjs",
  "exports": {
    ".": { "import": "./js/index.mjs", "types": "./js/index.d.ts" },
    "./wasm": { "import": "./wasm/module.wasm", "types": "./wasm.d.ts" }
  },
  "files": ["wasm/", "js/"]
}
EOF

echo "✅ Build complete!"
```

---

## 二、🐚 MoonBash — POSIX Shell 解释器

**项目地址**: https://github.com/Haoxincode/MoonBash

### 2.1 解释器/编译器架构模式

```
MoonBash/
├── src/
│   ├── frontend/                  # 📖 前端（源码 → AST）
│   │   ├── lexer/
│   │   │   ├── token.mbt         # Token ADT 定义
│   │   │   └── lexer.mbt         # 词法分析器
│   │   ├── parser/
│   │   │   ├── ast.mbt           # AST 节点 ADT
│   │   │   └── parser.mbt        # 递归下降解析器
│   │   └── expand/
│   │       └── expander.mbt      # 变量/路径展开
│   │
│   ├── runtime/                   # ⚙️ 运行时（AST 执行）
│   │   ├── evaluator/
│   │   │   └── eval.mbt          # AST 求值器
│   │   ├── builtin/
│   │   │   ├── registry.mbt      # 命令注册表
│   │   │   ├── string_cmd.mbt    # 字符串命令
│   │   │   ├── file_cmd.mbt      # 文件操作命令
│   │   │   └── process_cmd.mbt   # 进程管理命令
│   │   └── filesystem/
│   │       ├── fs_trait.mbt      # 文件系统抽象 Trait
│   │       ├── memory_fs.mbt     # 内存文件系统
│   │       └── agent_fs.mbt      # Agent 文件系统
│   │
│   ├── vm/                        # 🤖 子组件虚拟机
│   │   ├── regex_vm.mbt          # ReDoS 免疫的正则 VM
│   │   ├── opcode.mbt            # 操作码定义
│   │   └── compiler.mbt          # 正则 → VM 编译器
│   │
│   └── api/                       # 🌐 公开 API 层
│       ├── types.mbt             # 公开类型导出
│       └── session.mbt           # 会话管理
│
├── cmd/
│   └── repl/                      # 交互式 REPL
│       └── main.mbt
│
├── bindings/                      # 🔗 语言绑定
│   └── typescript/
│       ├── index.ts              # TypeScript API
│       └── package.json
│
└── docs/
    ├── FFI.md                     # FFI 互操作指南
    └── commands.md                # 内置命令列表
```

### 2.2 ADT 驱动：Token 和 AST 定义

Token、AST Node 全部使用 enum + Pattern Matching：

```moonbit
enum Token {
  Word(String)
  Number(Int)
  StringLiteral(String)
  Pipe
  Semicolon
  AndIf
  OrIf
  RedirectIn
  RedirectOut
  AppendOut
  HereDoc
  EOF
}

enum Command {
  SimpleCommand {
    name : String
    args : Array[String]
    redirects : Array[Redirect]
  }
  Pipeline {
    commands : Array[Command]
    negated : Bool
  }
  AndOrList {
    left : Command
    operator : AndOrOperator
    right : Command
  }
}
```

### 2.3 命令注册表模式

87 个内置命令通过统一接口注册：

```moonbit
struct BuiltinRegistry {
  mut commands : Map[String, BuiltinCommand]
}

impl BuiltinRegistry {
  pub fn new() -> BuiltinRegistry {
    let mut registry = BuiltinRegistry { commands: map![] }
    registry.register("echo", builtin_echo)
    registry.register("cd", builtin_cd)
    registry.register("export", builtin_export)
    registry
  }

  pub fn register(mut self : BuiltinRegistry, name : String, handler : BuiltinCommand) -> Unit {
    self.commands.insert(name, handler)
  }

  pub fn get(self : BuiltinRegistry, name : String) -> Option[BuiltinCommand] {
    self.commands.get(name)
  }
}
```

### 2.4 VM 替代方案：正则 VM 避免 ReDoS 攻击

```moonbit
enum RegexOpCode {
  MatchChar(Char)
  MatchAny
  MatchRange(Char, Char)
  Jump(Int)
  Split(Int, Int)
  Save(Int)
  Accept
}

pub struct RegexVM {
  program : Array[RegexOpCode]
}

impl RegexVM {
  pub fn execute(self : RegexVM, input : String) -> Bool {
    let mut vm_state = VMState::new(input)
    self.run(&mut vm_state)
  }
}
```

### 2.5 文件系统 Trait 抽象

```moonbit
pub(open) trait FileSystem {
  read_file(self : Self, path : String) -> Result[String, FsError]
  write_file(self : Self, path : String, content : String) -> Result[Unit, FsError]
  exists(self : Self, path : String) -> Bool
  list_dir(self : Self, path : String) -> Result(Array[String], FsError)
}
```

### 2.6 JavaScript 后端深度优化成果 ⭐

来自 multi-backend Chapter 8 的 MoonBash 优化策略：

#### 体积优化成果

| 指标 | 数值 |
|------|------|
| 原始 .mjs 大小 | ~1.8 MB |
| gzip 压缩后 | **434 KB** |
| minify + gzip | **~380 KB** (预估) |
| tree-shaking 后 | **~300 KB** (预估) |

**对比参考**：
- Bash 源码（C语言）：~1.2 MB 编译后二进制
- Node.js 内置 parser：不可分离
- **MoonBash**: 单文件、零依赖、可 tree-shake ✅

#### 四大优化策略

**策略一：最小化导出**

```moonbit
// ❌ 错误：导出了所有内部实现细节
pub fn internal_helper_1() -> Unit { ... }
pub fn internal_helper_2() -> Unit { ... }
pub fn internal_helper_3() -> Unit { ... }

// ✅ 正确：只导出公开 API，内部函数标记为 priv
priv fn internal_helper_1() -> Unit { ... }  // priv → tree-shakeable
priv fn internal_helper_2() -> Unit { ... }
priv fn internal_helper_3() -> Unit { ... }

pub fn parse_and_run(input : String) -> Result[Output, Error] { ... }
pub fn version() -> String { "1.0.0" }
```

**策略二：惰性初始化**

```moonbit
// ❌ 错误：模块加载时立即初始化所有命令
let BUILTIN_COMMANDS : Map[String, Command] = init_all_commands()

// ✅ 正确：使用懒加载，只在首次使用时初始化
var lazy_commands : Option[Map[String, Command]] = None

fn get_builtin_commands() -> Map[String, Command] {
  match lazy_commands {
    Some(cmds) => cmds
    None => {
      let cmds = init_all_commands()
      lazy_commands = Some(cmds)
      cmds
    }
  }
}
```

**策略三：避免重复代码生成（泛型 vs 特化）**

```moonbit
// ❌ 错误：泛型实例化导致代码膨胀
fn process_int_array(arr : Array[Int]) -> Array[Int] { ... }
fn process_string_array(arr : Array[String]) -> Array[String] { ... }
fn process_bool_array(arr : Array[Bool]) -> Array[Bool] { ... }

// ✅ 正确：使用泛型 + 特化关键路径
fn[T] process_array(arr : Array[T]) -> Array[T] {
  // 通用逻辑
}

fn process_int_array_fast(arr : Array[Int]) -> Array[Int] {
  // 针对 Int 的优化实现
}
```

**策略四：利用内联优化**

```moonbit
#[inline]
fn hot_path_function(x : Int, y : Int) -> Int {
  x * y + x - y
}

fn clamp(value : Int, min : Int, max : Int) -> Int {
  if value < min { min }
  else if value > max { max }
  else { value }
}
```

#### npm 包发布流程

```bash
moon build --target js --release
mkdir -p dist
cp target/js/release/*.mjs dist/
cp target/js/release/*.d.ts dist/

cat > dist/package.json << 'EOF'
{
  "name": "@scope/my-moonbit-lib",
  "version": "0.1.0",
  "type": "module",
  "main": "./index.mjs",
  "exports": {
    ".": { "import": "./index.mjs", "types": "./index.d.ts" }
  },
  "files": ["*.mjs", "*.d.ts"],
  "sideEffects": false
}
EOF

cd dist && npm publish
```

#### TypeScript 类型声明生成

```typescript
export interface ParseResult {
  success: boolean;
  ast?: ASTNode;
  errors?: Array<Error>;
}

export function parse(source: string): ParseResult;
export function evaluate(ast: ASTNode, env?: Env): Result<Value, Error>;
export function version(): string;
export type { Command, Token, Value, Env };
```

---

## 三、🗄️ morm — ORM 框架

**项目地址**: https://github.com/oboard/morm

### 3.1 属性驱动 DSL 架构

```
morm/
├── src/
│   ├── attributes/                # 🏷️ 属性定义层
│   │   └── morm_attrs.mbt        # #morm.* 属性宏定义
│   │
│   ├── generator/                 # ⚙️ 代码生成器
│   │   ├── schema_gen.mbt        # Schema 生成
│   │   ├── crud_gen.mbt          # CRUD 代码生成
│   │   └── migration_gen.mbt     # 迁移脚本生成
│   │
│   ├── engine/                    # 🔧 查询引擎
│   │   ├── query_builder.mbt     # 查询构建器
│   │   ├── executor.mbt          # 查询执行器
│   │   └── connection_pool.mbt   # 连接池
│   │
│   ├── dialect/                   # 🗣️ SQL 方言层
│   │   ├── dialect_trait.mbt     # SqlDialect Trait 定义
│   │   ├── sqlite.mbt            # SQLite 方言实现
│   │   ├── mysql.mbt             # MySQL 方言实现
│   │   └── postgresql.mbt        # PostgreSQL 方言实现
│   │
│   └── main/                      # 📢 公开 API
│       ├── entity.mbt            # 实体基类/接口
│       ├── repo.mbt              # Repository 模式
│       ├── query.mbt             # 查询类型定义
│       └── transaction.mbt       # 事务管理
│
├── cmd/
│   └── generator/                 # 代码生成命令
│       └── main.mbt              # `moon run generator -- example`
│
├── lib/                           # 🔗 FFI 绑定
│   └── sqlite3/                   # SQLite3 C FFI
│       ├── sqlite3.mbt           # FFI 声明
│       └── native_stub.c         # Native 存根
│
├── test/
│   ├── entity_test.mbt
│   ├── query_test.mbt
│   └── e2e_test.mbt
│
└── example/
    ├── user.mbt                   # 用户实体定义
    └── user.g.mbt                 # ✨ 自动生成的代码
```

### 3.2 属性即配置：声明式 DSL

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

### 3.3 属性分类体系

```
实体级属性（放在 struct 上）
├── #morm.entity              — 标记为 ORM 实体
├── #morm.table_name("name")  — 自定义表名
├── #morm.schema("schema")   — 数据库 schema
└── #morm.index(fields...)   — 定义索引

字段级属性（放在字段上）
├── #morm.primary_key        — 主键
├── #morm.auto_increment      — 自增主键
├── #morm.foreign_key("ref") — 外键引用
├── #morm.unique              — 唯一约束
├── #morm.not_null            — 非空约束
├── #morm.default(value)      — 默认值
├── #morm.column("name")      — 自定义列名
├── #morm.type_override(type) — 类型覆盖
├── #morm.max_length(n)       — 最大长度
└── #morm.ignore              — 忽略此字段
```

### 3.4 代码生成器核心结构

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

### 3.5 CRUD 代码生成

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
```

### 3.6 方言抽象 Trait（多后端支持）

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
} with upsert(table, columns, values) {
  "INSERT INTO " + table + " (" + columns.join(", ") + ") VALUES (" + values.join(", ") + ") " +
  "ON DUPLICATE KEY UPDATE " + columns.map(fn(c) { c + "=VALUES(" + c + ")" }).join(", ")
}
```

### 3.7 C FFI 集成（SQLite3）

```moonbit
type OpaqueSqliteDb = Opaque
type OpaqueStmt = Opaque

extern "c" fn sqlite3_open(filename : CString, dbOut : Ptr[OpaqueSqliteDb]) -> Int
extern "c" fn sqlite3_close(db : OpaqueSqliteDb) -> Int
extern "c" fn sqlite3_exec(db : OpaqueSqliteDb, sql : CString, callback : Ptr[Unit], err_msg : Ptr[CString]) -> Int
extern "c" fn sqlite3_prepare_v2(db : OpaqueSqliteDb, sql : CString, nByte : Int, stmtOut : Ptr[OpaqueStmt], tail : Ptr[CString]) -> Int
extern "c" fn sqlite3_step(stmt : OpaqueStmt) -> Int
extern "c" fn sqlite3_finalize(stmt : OpaqueStmt) -> Int
extern "c" fn sqlite3_column_int(stmt : OpaqueStmt, idx : Int) -> Int
extern "c" fn sqlite3_column_text(stmt : OpaqueStmt, idx : Int) -> CString
extern "c" fn sqlite3_errmsg(db : OpaqueSqliteDb) -> CString

struct Database {
  handle : OpaqueSqliteDb
}

fn Database::open(path : String) -> Result[Database, String] {
  let cstr = path.to_cstring()
  let mut db_ptr : OpaqueSqliteDb = unsafe_zero()
  let rc = sqlite3_open(cstr, &mut db_ptr)
  if rc == 0 {
    Ok(Database::{ handle: db_ptr })
  } else {
    let errmsg = sqlite3_errmsg(db_ptr).to_string()
    sqlite3_close(db_ptr)
    Err("cannot open database: " + errmsg)
  }
}
```

---

## 四、🔢 mbtgraph — 图算法库

**项目地址**: https://github.com/morning-start/mbtgraph

### 4.1 生产级架构设计模式

#### 有向/无向分离原则（替代条件分支）

**❌ 旧方案：单一结构体 + 运行时标志**

```moonbit
impl GraphWritable for AdjListGraph with add_edge(self, from, to, data) {
  if self.directed {
    // 有向逻辑：adj[from] + rev_adj[to]
  } else {
    // 无向逻辑：半存储 adj[min(from,to)]
  }
}
```

**问题**：
- 代码臃肿（567 行），每个方法都有条件分支
- 语义不清晰：`is_directed()` 返回运行时值而非编译时保证
- 测试困难：需要同时覆盖有向和无向路径

**✅ 方案：独立双结构体 + Trait 多态**

```
src/storage/
├── directed_adj_list.mbt     ← DirectedAdjList (纯有向)
├── undirected_adj_list.mbt   ← UndirectedAdjList (纯无向)
├── directed_matrix.mbt        ← DirectedMatrix (纯有向)
├── undirected_matrix.mbt      ← UndirectedMatrix (纯无向)
├── edge_list.mbt              ← EdgeListGraph (纯有向)
└── csr.mbt                    ← CSRGraph (纯只读有向)
```

**Trait 实现对照**：

| 结构体 | GraphReadable | GraphWritable | GraphDirected | GraphEdgeIterable | GraphBatchReadable |
|--------|:---:|:---:|:---:|:---:|:---:|
| DirectedAdjList | ✅ | ✅ | ✅ | — | — |
| UndirectedAdjList | ✅ | ✅ | — | ✅ | — |
| DirectedMatrix | ✅ | ✅ | ✅ | — | — |
| UndirectedMatrix | ✅ | ✅ | — | — | — |
| EdgeListGraph | ✅ | ✅ | — | ✅ | — |
| CSRGraph | ✅ | — | — | — | ✅ |

**设计原则**：用**类型系统的力量**替代运行时条件分支，让编译器保证正确性。

#### 半存储优化（空间换时间的权衡）

**问题**：无向图的对称存储导致 ~50% 空间浪费

```
全存:  边 (0,1) 存在 adj[0] 和 adj[1] 各一次 → 2E 条边记录
半存:  边 (0,1) 只存在 adj[0]（因为 0 < 1）→ E 条边记录
```

**规则**：对于无向边 (u, v, w)，如果 u < v → 存入 adj[u] 为 (v, w)，否则存入 adj[v]

**数据结构差异**：

```moonbit
pub struct DirectedAdjList {
  adj : Array[Array[(NodeId, Double)]]      // 出边
  rev_adj : Array[Array[(NodeId, Double)]]   // 入边
}

pub struct UndirectedAdjList {
  adj : Array[Array[(NodeId, Double)]]      // 唯一邻接表，无 rev_adj
}
```

**复杂度权衡表**：

| 操作 | 全存（有向式） | 半存（优化后） |
|------|--------------|---------------|
| `add_edge(u,v)` | O(1) 双写 | O(1) 单写 |
| `contains_edge(u,v)` | O(deg(u)) | O(min(u,v)+deg) |
| `neighbors(u)` | **O(deg(u))** | O(u + deg(u)) |
| `degree(u)` | **O(1)** | O(u + deg(u)) |
| `remove_edge(u,v)` | 删两处 | 删一处 |
| **空间** | O(V + 2E) | **O(V + E)** |

#### 公共 Helper 消除重复

**问题**：多个存储实现的重复代码

```moonbit
// 每个 .mbt 文件都复制了一遍相同的辅助函数
fn dal_has_node(nodes, idx) -> Bool { ... }
fn ual_has_node(nodes, idx) -> Bool { ... }
fn el_has_node(nodes, idx) -> Bool { ... }
```

**方案**：同包内的 shared_helpers.mbt

```moonbit
pub fn has_node(nodes : Array[Node?], idx : Int) -> Bool { ... }
pub fn find_slot(nodes : Array[Node?], i : Int, n : Int) -> Int { ... }
pub fn remove_from_list(list, target) -> (Bool, Array[...]) { ... }
pub fn bubble_sort_by_weight(edges) -> Array[...] { ... }
```

**调用方式**：同包内直接调用，无需模块前缀。

```moonbit
has_node(self.nodes, idx)          // ✅ 直接调用
find_slot(self.nodes, 0, len)      // ✅ 直接调用
```

#### Builder 模式（不可变构建）

CSR 是**只读**格式（符合 LSP 原则，不实现 GraphWritable）。但构建 CSR 需要逐步添加节点和边：

```moonbit
pub struct CSRBuilder {
  nodes : Array[Node]
  edges : Array[(NodeId, NodeId, Double)]
}

pub fn CSRBuilder::new() -> CSRBuilder { ... }
pub fn CSRBuilder::add_node(self, id, data) -> CSRBuilder { ... }   // 返回新 builder
pub fn CSRBuilder::add_edge(self, from, to, w) -> CSRBuilder { ... }  // 返回新 builder
pub fn CSRBuilder::build(self) -> CSRGraph { ... }                    // 构建最终结果
```

**使用方式**：

```moonbit
let graph = CSRBuilder::new()
  .add_node(NodeId(0), 1.0)
  .add_node(NodeId(1), 2.0)
  .add_edge(NodeId(0), NodeId(1), 3.14)
  .build()
```

**关键设计决策**：
- Builder 方法返回 **新的 CSRBuilder**（函数式链式调用）
- `build()` 执行排序和 CSR 结构构建（一次性 O(E log E)）
- 最终的 `CSRGraph` 是不可变的纯数据结构

#### Converter 统一模式

所有转换函数遵循相同模板：

```moonbit
pub fn[G : GraphReadable] to_xxx(g : G) -> TargetType {
  let r = new_target_constructor()       // 1. 创建目标实例
  for nid in g.node_ids() {               // 2. 复制所有节点
    match g.get_node(nid) {
      Some(data) => GraphWritable::add_node(r, data) |> ignore
      None => ()
    }
  }
  for triple in g.edges() {                // 3. 复制所有边
    match triple {
      (f, t, w) => GraphWritable::add_edge(r, f, t, w) |> ignore
      _ => ()
    }
  }
  r                                       // 4. 返回目标实例
}
```

**转换函数清单**：

| 函数 | 源约束 | 目标类型 |
|------|--------|---------|
| `to_directed_adj_list[G]` | GraphReadable | DirectedAdjList |
| `to_undirected_adj_list[G]` | GraphReadable | UndirectedAdjList |
| `to_directed_matrix[G, cap]` | GraphReadable | DirectedMatrix |
| `to_undirected_matrix[G]` | GraphReadable | UndirectedMatrix |
| `to_csr[G]` | GraphReadable | CSRGraph |
| `to_edge_list[G]` | GraphReadable | EdgeListGraph |

#### SOLID 原则体现

**里氏替换原则 (LSP)**：
- `GraphReadable` 是基础 trait（所有存储都实现）
- `GraphWritable` 扩展了写入能力
- **CSR 是只读存储**，故意不实现 `GraphWritable`
  - 如果实现了 `add_node` 但抛出 "不支持" 异常，就违反了 LSP
  - **不实现 = 编译期保证，比运行时异常更安全**

**接口隔离原则 (ISP)**：
- `GraphEdgeIterable` 是独立的 trait（只有 `edges_sorted`）
- 只有需要排序功能的存储才实现它
- `GraphBatchReadable` 也是独立 trait（批量查询优化）
- 只有 CSR 这种适合批量的格式才实现它

### 4.2 可见性决策实战

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

### 4.3 Impl 可变性语义深度解析

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

### 4.4 元组解构注意事项

**For 循环不支持元组解构**：
```moonbit
for entry in self.adj[idx] {
  match entry {
    (nid, _) => {
      r.push(nid)
    }
  }
}
```

**Match 中元组解构变量要有意义**：
```moonbit
match entry {
  (node_id, weight) => {
    // node_id 明确表示 NodeId
    // weight 明确表示 Double
    process_node(node_id, weight)
  }
}
```

---

## 五、四种架构模式对比总结

| 维度 | 多层架构 (moon-lottie) | 解释器架构 (MoonBash) | DSL架构 (morm) | 图算法库 (mbtgraph) |
|------|----------------------|---------------------|---------------|------------------|
| **适用场景** | 复杂渲染/工具链 | 语言处理器 | 框架/ORM/DSL | 数据结构与算法库 |
| **核心抽象** | Renderer Trait | AST ADT | Attribute Macros | Trait 多态体系 |
| **扩展方式** | 实现 Trait 接口 | 注册内置命令 | 定义属性+方言 | 实现不同 Storage |
| **代码生成** | 无 | 无 | ✅ 核心 | 无 |
| **平台适配** | cmd/packages 分离 | FS Trait 抽象 | Dialect Trait | 类型系统分离 |
| **复杂度** | ⭐⭐⭐⭐ 高 | ⭐⭐⭐ 中高 | ⭐⭐⭐ 中高 | ⭐⭐⭐ 中高 |
| **学习曲线** | 陡峭 | 中等 | 中等 | 较陡峭 |

---

## 六、Monorepo 最佳实践清单

| # | 实践 | 说明 | 来源项目 |
|---|------|------|---------|
| 1 | **清晰分层** | lib(核心)/cmd(入口)/packages(绑定)/demo(示例) 四层分离 | moon-lottie |
| 2 | **workspace 声明** | 使用 `moon.workspace.json` 声明内部包 | 所有三个项目 |
| 3 | **独立 pkg** | 每个子目录是独立的 `moon.pkg` 单元 | 所有四个项目 |
| 4 | **双目标构建** | 同时支持 wasm-gc 和 js，各自有入口 | moon-lottie |
| 5 | **npm workspace** | 用 pnpm/yarn workspace 管理 JS 子包 | moon-lottie |
| 6 | **文档分离** | README.md(用户) + README.mbt.md(MoonBit开发者) | moon-lottie |
| 7 | **FFI 隔离** | C FFI 绑定放在 `lib/` 或 `ffi/` 独立目录 | morm |
| 8 | **生成代码管理** | `.g.mbt` 文件加入 `.gitignore` 或单独跟踪 | morm |
| 9 | **构建脚本化** | 复杂构建逻辑写入 `scripts/` 目录 | moon-lottie |
| 10 | **示例完整** | `example/` 提供可直接运行的示例 | morm |
| 11 | **类型系统利用** | 用 Trait 分离有向/无向，用 pub(all)/pub 区分可见性 | mbtgraph |
| 12 | **值传递设计** | impl 方法返回新状态，天然支持不可变接口和调试回溯 | mbtgraph |
| 13 | **属性驱动** | 用声明式属性替代 XML/JSON 配置，自动生成类型安全代码 | morm |
| 14 | **JS 体积优化** | priv 导出 + 懒加载 + 泛型合并 + 内联标注 | MoonBash |

---

*文档版本: v1.0.0 | 最后更新: 2026-05-17*
*来源: library-design Part 12/14/15 + functional Part 3.5 + multi-backend Ch7/Ch8 + project-layout Monorepo模板 + devtools 错误码 + data-types 可见性 + pattern-match 陷阱*
