# MoonBit 多后端开发 🌐

## 任务目标

- 本 Skill 用于：掌握 **MoonBit 三大后端（WASM/JS/Native）的开发与优化**
- 能力包含：**后端对比选择、各平台编译优化、互操作、性能调优**
- 触发条件：选择编译目标、跨平台开发、性能优化

## 后端对比总览

### 三大后端特性对比

| 特性 | **WASM** | **JavaScript** | **Native** |
|------|---------|---------------|------------|
| **执行环境** | 浏览器 / 边缘计算 | Node.js / 浏览器 | 操作系统 |
| **性能等级** | ⭐⭐⭐ 高 | ⭐⭐ 中 | ⭐⭐⭐⭐ 最高 |
| **二进制体积** | 🔵 极小（KB级） | 🟢 中等（MB级） | 🔴 小 |
| **启动速度** | ⚡ 快 | ⚡ 快 | ⚡⚡ 最快 |
| **安全性** | 🛡️ 沙箱隔离 | 🌐 Web 安全模型 | 🔓 系统级别 |
| **调试体验** | 🟡 中等 | 🟢 优秀（浏览器工具） | 🔴 优秀（GDB/LLDB） |
| **生态集成** | 🟡 WASI + JS FFI | 🟢🟢 完整 npm 生态 | 🔴 C FFI + 系统调用 |
| **适用场景** | 前端核心模块、边缘计算 | 全栈应用、前端集成 | 系统工具、高性能计算 |

### 选择决策树

```
你的目标场景是什么？
│
├─ 🌐 Web 前端 / 浏览器
│   ├─ 需要极致性能？ → WASM（主选）
│   └─ 需要快速集成？ → JS（备选）
│
├─ ⚙️ Node.js 后端
│   └─ → JavaScript（最佳选择）
│
└─ 💻 系统 / 高性能计算
    └─ → Native（唯一选择）
```

## 一、WebAssembly 后端（WASM）

### 核心优势

MoonBit 生成比现有解决方案**明显更小的 Wasm 文件**，同时保持**更高的运行时性能**。

### 编译选项

```bash
# 标准 WASM（默认）
moon build --target wasm

# 带 GC 的 WASM（更小体积，更好内存管理）
moon build --target wasm-gc

# Release 优化模式
moon build --target wasm --release

# 组件模型（实验性）
moon build --target wasm --component
```

### 输出文件结构

```
_build/
└── wasm/
    └── release/
        └── my-project.wasm      # WASM 二进制文件
```

### WASM vs WASM-GC 对比

| 特性 | `wasm` | `wasm-gc` |
|------|--------|-----------|
| 兼容性 | ✅ 广泛支持 | ⚠️ 需要较新浏览器 |
| 二进制大小 | 小 | **更小**（-20%~40%） |
| 内存管理 | 手动/线性内存 | **自动 GC** |
| 数据结构传递 | 复杂（需要序列化） | **简单**（直接传引用） |
| 适用场景 | 生产环境 | 实验/前沿项目 |

### 与 JavaScript 互操作

#### 导出函数给 JS 调用

```moonbit
// src/lib.mbt

/// 导出函数给 JavaScript 调用
pub fn add(a: Int, b: Int) -> Int {
  a + b
}

/// 导出字符串处理函数
pub fn greet(name: String) -> String {
  "Hello, \(name) from MoonBit!"
}
```

#### 在 JavaScript 中使用 WASM

```javascript
// 加载 WASM 模块
const wasmModule = await WebAssembly.instantiateStreaming(
  fetch("./my-project.wasm"),
  {
    // 导入 JS 函数给 WASM 使用
    env: {
      console_log: (ptr) => {
        console.log(/* 从 WASM 内存读取字符串 */);
      }
    }
  }
);

// 调用 MoonBit 导出的函数
const result = wasmModule.exports.add(5, 3);
console.log(result); // 8
```

#### 从 MoonBit 调用 JS 函数

```moonbit
// 声明外部 JS 函数
fn js_alert(message: String) -> Unit = "env" "alert"

fn main {
  js_alert("Hello from MoonBit!")
}
```

### 浏览器集成示例

#### HTML 中使用 WASM

```html
<!DOCTYPE html>
<html>
<head>
  <title>MoonBit WASM Demo</title>
</head>
<body>
  <div id="app"></div>
  
  <script type="module">
    const wasm = await WebAssembly.instantiateStreaming(
      fetch("./my-project.wasm")
    );
    
    // 使用导出的函数
    const result = wasm.instance.exports.add(10, 20);
    document.getElementById('app').textContent = `Result: ${result}`;
  </script>
</body>
</html>
```

### 性能优化策略

#### 减少 WASM 体积

1. **使用 `wasm-gc` 目标**：自动 GC 减少手动管理代码
2. **移除未使用代码**：Tree-shaking 自动消除死代码
3. **优化数据结构**：
   ```moonbit
   // 使用 FixedArray 替代 Array（固定长度更高效）
   let data : FixedArray[Int] = [1, 2, 3, 4, 5]
   ```

#### 编译优化

```bash
# Release 模式（启用所有优化）
moon build --target wasm --release

# 查看生成的文件大小
ls -lh _build/wasm/release/
```

### WASM 组件模型（实验性）

```bash
# 编译为 WIT 组件
moon build --target wasm --component
```

特点：
- 基于 WIT（WebAssembly Interface Types）标准
- 更强的类型安全和边界
- 跨语言互操作性更好

---

## 二、JavaScript 后端（JS）

### 核心优势

- **完整 npm 生态**：可直接使用 JavaScript 库
- **优秀调试体验**：浏览器 DevTools + Node.js inspector
- **易于集成**：与现有前端/Node.js 项目无缝结合

### 编译与运行

```bash
# 编译到 JavaScript
moon build --target js

# 运行 JS 后端程序
moon run cmd/main --target js

# Release 模式
moon build --target js --release
```

### 输出文件结构

```
_build/
└── js/
    └── release/
        ├── main.js              # 主程序
        └── lib.js               # 库代码（如果有）
```

### Node.js 开发

#### 创建 Node.js 项目

```bash
moon new my-node-project
cd my-node-project
```

#### 编写代码

```moonbit
// cmd/main/main.mbt

fn main {
  println("Hello from MoonBit in Node.js!")

  // 使用 MoonBit 标准库
  let arr = [1, 2, 3, 4, 5]
  let sum = arr.fold(0, (a, b) => a + b)
  println("Sum: \(sum)")
}
```

#### 运行

```bash
# 方式一：通过 moon run
moon run cmd/main --target js

# 方式二：直接运行生成的 JS
node _build/js/release/main.js
```

### 前端集成

#### 操作 DOM（通过外部函数声明）

```moonbit
// 声明外部 JS 函数用于 DOM 操作
fn document_get_element_by_id(id: String) -> JsObject = "js" "document_getElementById"
fn element_set_inner_html(el: JsObject, html: String) = "js" "element_setInnerHTML"

fn update_page() -> Unit {
  let el = document_get_element_by_id("app")
  element_set_inner_html(el, "<h1>Hello from MoonBit!</h1>")
}
```

#### 生成前端库

```bash
# 编译为 JS 库
moon build --target js

# 在 HTML 或其他 JS 项目中引用
// <script src="./_build/js/release/my-lib.js"></script>
```

### JS 互操作详解

#### 调用 JS 函数

```moonbit
// 声明外部 JS 函数
fn js_console_log(msg: String) -> Unit = "js" "console_log"
fn js_set_timeout(callback: () -> Unit, ms: Int) -> Unit = "js" "setTimeout"

fn main {
  js_console_log("Hello from MoonBit!")
  
  // 使用 setTimeout
  js_set_timeout(fn() { 
    js_console_log("Delayed message!") 
  }, 1000)
}
```

#### 导出给 JS 调用

```moonbit
// 使用 pub 导出函数和类型
pub fn calculate(x: Int, y: Int) -> Int {
  x * x + y * y
}

pub fn process_data(data: Array[String]) -> String {
  data.fold("", (acc, s) => acc + s)
}

pub struct UserData {
  name: String
  age: Int
} reexport
```

在 JavaScript 中使用：

```javascript
const moonbit = require('./_build/js/release/my-lib.js');

// 调用导出的函数
const result = moonbit.calculate(3, 4);
console.log(result); // 25

// 处理数据
const processed = moonbit.process_data(["a", "b", "c"]);
console.log(processed); // "abc"
```

### 类型映射表

| MoonBit 类型 | JavaScript 类型 | 说明 |
|-------------|----------------|------|
| `Int` | `number` | 整数 |
| `Double` | `number` | 浮点数 |
| `String` | `string` | 字符串 |
| `Bool` | `boolean` | 布尔值 |
| `Array[T]` | `Array` | 数组 |
| `Unit` | `undefined` | 无返回值 |
| `JsObject` | `object` | 通用 JS 对象 |

### 代码分割与打包

对于大型项目，建议分割为多个包：

```json
// src/core/moon.pkg.json
{
  "is-main": false,
  "import": []
}

// cmd/main/moon.pkg.json
{
  "is-main": true,
  "import": [
    { "path": "my-project/core", alias: "core" },
    { "path": "my-project/utils", alias: "utils" }
  ]
}
```

### 性能优化

```bash
# Release 模式（压缩和优化）
moon build --target js --release

# 检查输出大小
ls -lh _build/js/release/

# 可配合 webpack/rollup 进一步打包优化
```

---

## 三、Native 后端（原生代码）

### 核心优势

- **最高运行性能**：接近 C/C++ 级别（比 Java 快 15 倍）
- **LLVM 后端支持**：生成高质量机器码
- **系统级编程**：可直接调用操作系统 API 和 C 库
- **启动速度最快**：无虚拟机或解释器开销

### 编译与运行

```bash
# 编译到原生代码
moon build --target native

# 运行原生程序
moon run cmd/main --target native

# Release 模式（高度优化）
moon build --target native --release

# LLVM 后端（可选，通常已启用）
moon build --target native --llvm

# 查看生成的汇编代码（调试用）
moon build --target native --emit-asm
```

### 输出文件结构

```
_build/
└── native/
    └── release/
        ├── main          # Linux/macOS 可执行文件
        └── main.exe      # Windows 可执行文件
```

### 系统编程能力

#### 命令行参数处理

```moonbit
// cmd/main/main.mbt

fn main {
  // 原生后端支持完整的系统 I/O
  println("Hello from native MoonBit!")
  
  // 可以读取环境变量、命令行参数等
}
```

#### 文件操作（通过标准库或 FFI）

```moonbit
// 使用 MoonBit 标准库进行文件操作
fn read_file_content(path: String) -> Result[String, String] {
  // 标准库提供的文件读取接口
}

fn write_file_content(path: String, content: String) -> Result[Unit, String] {
  // 标准库提供的文件写入接口
}
```

### 性能调优技巧

#### 1. 使用合适的数据结构

```moonbit
// FixedArray 比 Array 更快（固定长度，无动态分配）
let arr : FixedArray[Int] = [1, 2, 3, 4, 5]

// IntMap 比 Map[String, Int] 在整数键时更快
let map : IntMap[String] = IntMap::empty()
```

#### 2. 避免不必要的堆分配

```moonbit
// ❌ 差：每次循环创建新数组
let result = []
arr.each(x => result.append(process(x)))

// ✅ 好：使用迭代器或预分配
let result = arr.map(x => process(x))
```

#### 3. 尾递归优化

```moonbit
// 尾递归形式（编译器会优化为循环，不会栈溢出）
fn factorial(n: Int, acc: Int) -> Int {
  if n <= 1 {
    acc
  } else {
    factorial(n - 1, n * acc)  // 尾调用
  }
}

// 使用
fn main {
  let result = factorial(10, 1)
  println("10! = \(result)")
}
```

#### 4. 内联 hint（如果编译器支持）

```moonbit
#[inline]
fn fast_add(a: Int, b: Int) -> Int {
  a + b
}
```

### Release 优化效果

```bash
# Debug 构建（默认，包含调试信息）
moon build --target native
# 输出：较大的二进制，包含符号信息

# Release 构建（生产环境）
moon build --target native --release
# 输出：优化的二进制，体积更小，性能更高
```

**预期提升**：
- 执行速度：+20% ~ +50%（取决于代码特征）
- 二进制体积：-30% ~ -50%
- 启动时间：显著加快

### 调试原生程序

#### 使用 GDB（Linux）

```bash
# 编译 debug 版本
moon build --target native

# 启动 GDB
gdb ./_build/native/release/main

# GDB 常用命令
(gdb) break main           # 设置断点
(gdb) run                  # 运行程序
(gdb) next                 # 单步执行
(gdb) print variable_name  # 打印变量
(gdb) continue             # 继续
(gdb) quit                 # 退出
```

#### 使用 LLDB（macOS）

```bash
lldb ./_build/native/release/main

# LLDB 命令类似 GDB
(lldb) break set --name main
(lldb) run
(lldb) next
(lldb) frame variable
```

### 与 C 语言的互操作（FFI 基础）

Native 后端可以通过 FFI 直接调用 C 语言库：

```moonbit
// 声明外部 C 函数
extern "C" fn c_printf(fmt: CString) -> Int = "libc.printf"

fn main {
  c_printf("Hello from C!\n")
}
```

> 💡 **详细 FFI 内容请参考 [moonbit-ffi](../moonbit-ffi/SKILL.md)**

---

## 四、跨平台开发指南

### 条件编译

使用 `#[cfg]` 属性编写平台特定代码：

```moonbit
// 平台检测与条件编译

#[cfg(target = "wasm")]
pub fn get_platform() -> String {
  "WebAssembly"
}

#[cfg(target = "js")]
pub fn get_platform() -> String {
  "JavaScript"
}

#[cfg(target = "native")]
pub fn get_platform() -> String {
  "Native"
}

fn main {
  println("Running on: \(get_platform())")
}
```

### 平台抽象层设计

```moonbit
// 定义平台无关的 trait
trait PlatformIO {
  read_file(path: String) -> Result[String, String]
  write_file(path: String, content: String) -> Result[Unit, String]
}

// 为不同平台实现
struct WasmIO
struct NativeIO

impl PlatformIO for WasmIO {
  fn read_file(path: String) -> Result[String, String] {
    // WASM 实现（通过 JS FFI）
  }
  // ...
}

impl PlatformIO for NativeIO {
  fn read_file(path: String) -> Result[String, String] {
    // Native 实现（直接系统调用）
  }
  // ...
}
```

### 共享代码策略

```
my-cross-platform-app/
├── src/
│   ├── common/              # ✅ 平台共享代码
│   │   ├── types.mbt       # 数据类型定义
│   │   ├── logic.mbt       # 业务逻辑
│   │   └── algorithm.mbt   # 算法实现
│   ├── wasm/               # 🔵 WASM 特定代码
│   │   └── browser_io.mbt
│   ├── js/                 # 🟢 JS 特定代码
│   │   └── node_io.mbt
│   └── native/             # 🔴 Native 特定代码
│       └── sys_io.mbt
├── cmd/
│   └── main/
│       └── main.mbt        # 入口（根据 target 选择实现）
```

## 五、性能基准对比

### 基准测试场景

| 测试场景 | WASM | JS | Native | 备注 |
|---------|------|-----|--------|------|
| **计算密集型**（斐波那契） | 1.2x | 1.0x (基准) | **0.3x** | Native 最快 |
| **数组操作**（排序算法） | 1.1x | 1.0x | **0.4x** | Native 显著领先 |
| **字符串处理** | 1.0x | **0.8x** | 0.9x | JS 引擎优化好 |
| **内存分配/释放** | 1.3x | 1.0x | **0.2x** | Native 无 GC 开销 |
| **启动时间** | 5ms | 10ms | **<1ms** | Native 秒启 |
| **二进制大小** | 15KB | 200KB | 80KB | WASM 最小 |

> 注：数值为相对值，越小越好。基于典型硬件的粗略估算。

### 如何选择：决策矩阵

| 你的优先级 | 推荐后端 | 理由 |
|-----------|---------|------|
| 🎯 **最小体积** | WASM | KB 级二进制，适合边缘部署 |
| ⚡ **最高性能** | Native | LLVM 优化，接近 C/C++ 速度 |
| 🌐 **Web 集成** | JS/WASM | JS 易集成，WASM 适合核心模块 |
| 🔧 **调试便利** | JS | 浏览器 DevTools + Source Map 支持 |
| 🛡️ **安全隔离** | WASM | 沙箱执行，适合不可信代码 |
| 💾 **系统编程** | Native | 完整系统 API 访问权限 |

## 最佳实践

### 通用建议

1. **先选后端再设计架构**：不同后端的惯用法差异大
2. **抽象平台差异**：使用 trait/interface 隔离平台相关代码
3. **针对性优化**：根据目标平台的特性优化热点路径
4. **多后端测试**：确保所有目标平台的功能一致性

### WASM 最佳实践

- 优先使用 `wasm-gc` 目标（如果兼容性允许）
- 减少 WASM/JS 边界的调用次数（有开销）
- 批量处理数据，减少内存拷贝
- 利用 WASM 的沙箱特性做安全敏感计算

### JS 最佳实践

- 充分利用 npm 生态系统
- 合理使用 JS FFI 调用浏览器/Node.js API
- 注意类型映射（特别是 JsObject 的使用）
- 考虑配合 webpack/rollup 进行最终打包

### Native 最佳实践

- 使用 `--release` 模式进行生产构建
- 利用 FFI 调用成熟的 C 库（避免重复造轮子）
- 关注内存布局和缓存友好性
- 使用 GDB/LLDB 进行性能剖析

---

## 六、moon.pkg 多后端配置详解

> 本章节基于官方 `moon.pkg` 文档，详细说明如何在 `moon.pkg` 中配置多后端支持、链接选项和原生存根。

### 6.1 supported-targets 声明

使用 `supported-targets` 声明本包支持的编译目标后端集合：

```toml
# 声明本包支持的后端集合
options(
  "supported-targets": "js",
)
```

**语法变体：**

| 写法 | 含义 |
|------|------|
| `"js"` | 单个后端 |
| `"+js+wasm-gc"` | 显式指定一组（`+` 号前缀表示集合表达式） |
| `"+all-js"` | 除 js 外的所有后端 |
| `["js", "native"]` | 旧数组语法（已弃用但仍兼容） |

**注意事项：**

- `--target all` 展开为 `wasm/wasm-gc/js/native`（不含 llvm）
- 省略 `supported-targets` = 支持所有后端
- 模块和包都声明时取**交集**

### 6.2 Wasm 后端链接选项

配置 WASM/WASM-GC 后端的导出、内存和导入行为：

```toml
options(
  link: {
    "wasm": {
      "exports": [ "hello", "foo:bar" ],        # 导出函数
      "import-memory": { "module": "env", "name": "memory" },  # 导入内存
      "memory-limits": { "min": 1, "max": 65536 },           # 内存限制（页）
      "shared-memory": true,                               # 共享内存
      "export-memory-name": "memory",                       # 导出内存名
      "heap-start-address": 1024,                           # 线性内存起始地址（仅线性内存）
    },
    "wasm-gc": {
      "exports": [ "hello" ],
      "use-js-builtin-string": true,                        # 启用 JS String 提案
      "imported-string-constants": "_",                    # 字符串常量命名空间
    },
  },
)
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `exports` | `Array[String]` | 导出的函数名列表，支持 `"foo:bar"` 重命名语法 |
| `import-memory` | `{ module, name }` | 从外部模块导入 WebAssembly.Memory |
| `memory-limits` | `{ min, max }` | 内存页数限制（1 页 = 64KB） |
| `shared-memory` | `Bool` | 启用共享内存（用于多线程场景） |
| `export-memory-name` | `String` | 导出 Memory 实例的名称 |
| `heap-start-address` | `Int` | 线性内存中堆的起始地址偏移 |
| `use-js-builtin-string` | `Bool` | 启用 JS String Builtins 提案（wasm-gc） |
| `imported-string-constants` | `String` | 导入字符串常量的命名空间前缀 |

### 6.3 JS 后端链接选项

配置 JavaScript 后端的输出格式和导出函数：

```toml
options(
  link: {
    "js": {
      "exports": [ "hello", "init" ],   # 导出函数
      "format": "esm",                   # 输出格式: esm(默认)/cjs/iife
    },
  },
)
```

**JS 输出格式说明：**

| 格式 | 全称 | 适用场景 |
|------|------|---------|
| `esm` | ES Module | 默认格式，现代浏览器、打包工具、Node.js ESM |
| `cjs` | CommonJS | 传统 Node.js 项目、require() 加载 |
| `iife` | Immediately Invoked Function Expression | 浏览器 `<script>` 标签直接引入 |

### 6.4 Native 后端链接选项

配置 Native 后端的编译器和链接器参数：

```toml
options(
  link: {
    "native": {
      "cc": "/usr/bin/gcc13",            # C 编译器路径
      "cc-flags": "-DMOONBIT",          # 编译器标志
      "cc-link-flags": "-s",             # 链接器标志（剥离符号）
      "stub-cc": "/usr/bin/gcc13",       # 存根编译器（调试用）
      "stub-cc-flags": "-g",            # 存根编译标志
      "stub-cc-link-flags": "",         # 存根链接标志
    },
  },
)
```

**字段说明：**

| 字段 | 说明 |
|------|------|
| `cc` | C 编译器可执行文件路径 |
| `cc-flags` | 传递给 C 编译器的额外标志 |
| `cc-link-flags` | 传递给链接器的额外标志 |
| `stub-cc` | 编译 native-stub 文件使用的 C 编译器（可不同于主 cc） |
| `stub-cc-flags` | 存根编译器的额外标志 |
| `stub-cc-link-flags` | 存根链接器的额外标志 |

> ⚠️ **注意**：`link` 对 native 后端本身不起直接作用（不控制是否生成可执行文件），仅用于配置编译器和链接器参数。

### 6.5 原生存根文件 native-stub

列出需要与本包一起编译的 C 存根源文件：

```toml
# 列出需要与本包一起编译的 C 存根源文件
options(
  "native-stub": [ "stub.c", "helpers.c" ],
)
```

**用途说明：**

- 与 FFI 的 `extern "C"` 声明配合使用
- 提供 C 语言包装函数或适配代码
- 文件路径**相对于包目录**
- 这些 `.c` 文件会在 native 编译时与生成的 C 代码一同编译链接

**典型用法示例：**

```moonbit
// MoonBit 侧声明外部 C 函数
extern "C" fn my_wrapper_init() -> Unit = "my_wrapper_init"

extern "C" fn my_wrapper_process(data: Int) -> Int = "my_wrapper_process"
```

```c
// stub.c — 提供 C 语言实现
#include <stdio.h>

void my_wrapper_init(void) {
  printf("Stub initialized\n");
}

int my_wrapper_process(int data) {
  return data * 2;
}
```

### 6.6 link 布尔值快捷方式

当不需要指定详细的链接选项，只需标记某个包需要参与链接时，可以使用布尔值简写：

```toml
# 简单地标记需要链接（不指定详细选项）
options(
  link: true,
)
```

**适用场景：**

- 非主包也需要被链接到最终输出
- 库包中包含需要在运行时初始化的代码
- 确保 package 的副作用（如全局注册）在程序启动时执行

---

## 七、Wasm-GC + JS 双运行时模式 ⭐v6.0新增

> 来自 [moon-lottie](https://github.com/cg-zhou/moon-lottie) 的生产级双后端架构经验

### 7.1 为什么需要双运行时？

| 场景 | Wasm-Gc 后端 | JS 后端 |
|------|-------------|---------|
| 浏览器核心引擎 | ✅ 最佳（性能+体积） | ❌ 不适合 |
| Node.js 工具链 | ❌ 无法访问 FS | ✅ 最佳 |
| 边缘计算 | ✅ V8 Isolate 支持 | ✅ 也支持 |
| 调试体验 | 🟡 中等（WAT 调试） | 🟢 优秀（Chrome DevTools） |
| 生态集成 | 🟡 需要 FFI 桥接 | 🟢🟢 原生 npm |

### 7.2 架构设计模式

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

### 7.3 moon.pkg 双目标配置

```toml
# lib/core/moon.pkg — 平台无关的核心库
# 无需 target 限制，可被所有后端引用

# cmd/wasm_runtime/moon.pkg — Wasm-Gc 特定入口
import {
  "my_project/core" @lib,
}

options(
  "is-main": true,
)

# 使用条件编译引入 Wasm 特定代码
target("wasm-gc")

# cmd/js_runtime/moon.pkg — JS 特定入口
import {
  "my_project/core" @lib,
}

options(
  "is-main": true,

target("js")
```

### 7.4 平台抽象 Trait 设计

```moonbit
// ===== 平台抽象接口定义 =====
pub(open) trait PlatformRenderer {
  // 渲染相关
  create_canvas(Self, Int, Int) -> CanvasHandle
  clear_canvas(Self, CanvasHandle, String) -> Unit
  draw_rect(Self, CanvasHandle, Rect, FillStyle) -> Unit
  draw_path(Self, CanvasHandle, PathData, StrokeStyle) -> Unit
  set_transform(Self, CanvasHandle, Transform) -> Unit
  
  // 事件相关
  request_animation_frame(Self, () -> Unit) -> Int
  add_event_listener(Self, String, EventHandler) -> Unit
  now_ms(Self) -> Int
  
  // I/O 相关
  load_image(Self, String) -> Result[ImageHandle, String]
  log(Self, String) -> Unit
}

// ===== Wasm-Gc 实现 =====
impl PlatformRenderer for WasmRuntime with create_canvas(self, w, h) {
  // 通过 extern "js" 或 Wasm 导入调用浏览器 API
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
// ... 其他方法实现

// ===== JS 实现（Node.js 或 Browser）=====
impl PlatformRenderer for JsRuntime with create_canvas(self, w, h) {
  if self.is_browser { create_dom_canvas(w, h) }
  else { create_offscreen_canvas(w, h) }
} with log(self, msg) {
  // 在 JS 后端可以直接使用 console
  println("[JS Runtime] " + msg)
}
```

### 7.5 双目标构建脚本

```bash
#!/bin/bash
# build.sh — 双目标构建脚本

set -e

PROJECT_NAME="my_project"
BUILD_DIR="_build"

echo "=== Building ${PROJECT_NAME} ==="

# 1. 构建 Wasm-Gc 目标
echo "[1/3] Building Wasm-Gc target..."
moon build --target wasm-gc --release
mkdir -p ${BUILD_DIR}/wasm
cp target/wasm-gc/release/*.wasm ${BUILD_DIR}/wasm/

# 2. 构建 JS 目标
echo "[2/3] Building JavaScript target..."
moon build --target js --release
mkdir -p ${BUILD_DIR}/js
cp -r target/js/release/* ${BUILD_DIR}/js/

# 3. 生成包元数据
echo "[3/3] Generating package metadata..."
cat > ${BUILD_DIR}/package.json << 'EOF'
{
  "name": "my-project",
  "version": "0.1.0",
  "type": "module",
  "main": "./js/index.mjs",
  "exports": {
    ".": {
      "import": "./js/index.mjs",
      "types": "./js/index.d.ts"
    },
    "./wasm": {
      "import": "./wasm/module.wasm",
      "types": "./wasm.d.ts"
    }
  },
  "files": ["wasm/", "js/"]
}
EOF

echo ""
echo "✅ Build complete!"
echo "  Wasm-Gc: ${BUILD_DIR}/wasm/"
echo "  JS:      ${BUILD_DIR}/js/"
```

---

## 八、JavaScript 后端深度优化 ⭐v6.0新增

> 来自 [MoonBash](https://github.com/Haoxincode/MoonBash) 的 434KB gzip 成果和 moon-lottie 的 JS 集成经验

### 8.1 MoonBash 的体积优化成果

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

### 8.2 JS 后端优化策略

#### 策略一：最小化导出

```moonbit
// ❌ 错误：导出了所有内部实现细节
pub fn internal_helper_1() -> Unit { ... }
pub fn internal_helper_2() -> Unit { ... }
pub fn internal_helper_3() -> Unit { ... }

// ✅ 正确：只导出公开 API，内部函数标记为 priv
priv fn internal_helper_1() -> Unit { ... }  // priv → tree-shakeable
priv fn internal_helper_2() -> Unit { ... }
priv fn internal_helper_3() -> Unit { ... }

// 只有真正的公开 API
pub fn parse_and_run(input : String) -> Result[Output, Error] { ... }
pub fn version() -> String { "1.0.0" }
```

#### 策略二：惰性初始化

```moonbit
// ❌ 错误：模块加载时立即初始化所有命令
let BUILTIN_COMMANDS : Map[String, Command] = init_all_commands()  // 启动时执行

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

#### 策略三：避免重复代码生成

```moonbit
// ❌ 错误：泛型实例化导致代码膨胀
fn process_int_array(arr : Array[Int]) -> Array[Int] { ... }
fn process_string_array(arr : Array[String]) -> Array[String] { ... }
fn process_bool_array(arr : Array[Bool]) -> Array[Bool] { ... }

// ✅ 正确：使用泛型 + 特化关键路径
fn[T] process_array(arr : Array[T]) -> Array[T] {
  // 通用逻辑
}

// 仅对性能关键路径特化
fn process_int_array_fast(arr : Array[Int]) -> Array[Int] {
  针对 Int 的优化实现
}
```

#### 策略四：利用 MoonBit 的内联优化

```moonbit
// 标记热点函数为内联候选
#[inline]
fn hot_path_function(x : Int, y : Int) -> Int {
  x * y + x - y
}

// 小函数自动内联
fn clamp(value : Int, min : Int, max : Int) -> Int {
  if value < min { min }
  else if value > max { max }
  else { value }
}
```

### 8.3 JS 后端 npm 包发布流程

```bash
# 1. 构建 JS 目标
moon build --target js --release

# 2. 创建 npm 包结构
mkdir -p dist
cp target/js/release/*.mjs dist/
cp target/js/release/*.d.ts dist/  # 如果有类型声明

# 3. 创建 package.json
cat > dist/package.json << 'EOF'
{
  "name": "@scope/my-moonbit-lib",
  "version": "0.1.0",
  "type": "module",
  "main": "./index.mjs",
  "exports": {
    ".": {
      "import": "./index.mjs",
      "types": "./index.d.ts"
    }
  },
  "files": ["*.mjs", "*.d.ts"],
  "sideEffects": false,
  "description": "A MoonBit library compiled to JavaScript"
}
EOF

# 4. 发布到 npm
cd dist && npm publish
```

### 8.4 TypeScript 类型声明生成

```typescript
// index.d.ts — 从 MoonBit 自动生成的类型声明

// 核心类型
export interface ParseResult {
  success: boolean;
  ast?: ASTNode;
  errors?: Array<Error>;
}

export interface ASTNode {
  type: string;
  value?: any;
  children?: Array<ASTNode>;
}

// 公开 API 函数
export function parse(source: string): ParseResult;
export function evaluate(ast: ASTNode, env?: Env): Result<Value, Error>;
export function version(): string;

// 导出类型
export type { Command, Token, Value, Env };
```

## 资源索引

- [MoonBit WASM 文档](https://docs.moonbitlang.com/zh-cn/stable/toolchain/wasm/index.html)
- [WebAssembly 组件模型教程](https://docs.moonbitlang.com/zh-cn/stable/toolchain/wasm/component-model-tutorial.html)
- [JS 后端文档](https://docs.moonbitlang.com/zh-cn/stable/toolchain/js/index.html)
- [Native 后端文档](https://docs.moonbitlang.com/zh-cn/stable/toolchain/native/index.html)
- [LLVM 后端说明](https://docs.moonbitlang.com/zh-cn/stable/toolchain/native/llvm.html)
- [moon-lottie - 双运行时示例项目](https://github.com/cg-zhou/moon-lottie)
- [MoonBash - JS 优化示例项目](https://github.com/Haoxincode/MoonBash)

## 注意事项

- **WASM**：适合浏览器和边缘计算，注意与 JS 交互的内存管理
- **JS**：适合全栈开发和前端集成，充分利用 npm 生态
- **Native**：适合系统级和高性能场景，可通过 FFI 调用 C 库
- **跨平台代码**：使用 `#[cfg]` 属性进行条件编译
- **双运行时模式**：通过 Platform Trait 实现平台抽象，同一套 core 代码编译到多目标
- **JS 体积优化**：使用 priv 标记内部函数、惰性初始化、避免泛型膨胀、利用内联优化
- **性能测试**：使用 `moon bench` 在各后端上进行基准测试
- **Release 构建**：生产环境务必使用 `--release` 模式

---

*文档版本：v6.0.0 | 最后更新：2026-05-17 | 基于 moon.pkg 官方文档补充多后端配置详解*
*⭐v6.0 新增：Chapter 7 双运行时模式、Chapter 8 JS 深度优化（来自 moon-lottie & MoonBash 生产经验）*
