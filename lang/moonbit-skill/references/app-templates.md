# MoonBit 应用程序模板参考文档

> **来源版本**: moonbit-app-templates v2.0.0
> **源文件**: skills/layer3-domain-expertise/moonbit-app-templates/SKILL.md
> **迁移日期**: 2026-05-17

---

## 一、项目初始化

### 基础命令

```bash
# 安装 MoonBit（Windows）
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser; irm https://cli.moonbitlang.com/install/powershell.ps1 | iex

# 创建新项目
moon new my_project && cd my_project

# 运行程序
moon run cmd/main

# 构建到不同后端
moon build --target wasm     # WebAssembly
moon build --target js       # JavaScript
moon build --target native   # 原生代码 (C/LLVM)

# 测试
moon test

# 检查类型
moon check
```

### 项目结构说明

```
my_project/
├── moon.mod.json           # 模块元数据
├── moon.pkg                # 根包描述符
├── my_project.mbt          # 库代码
├── my_project_test.mbt     # 库测试
├── cmd/
│   └── main/
│       ├── main.mbt        # 程序入口 (fn main)
│       └── moon.pkg        # 入口包配置
├── README.md
└── LICENSE
```

### moon.mod.json 配置

```json
{
  "name": "username/my_project",
  "version": "0.1.0",
  "readme": "README.md",
  "repository": "",
  "license": "Apache-2.0",
  "keywords": [],
  "description": ""
}
```

### 添加第三方依赖

```bash
# 从 mooncakes.io 添加依赖
moon add FrozenLemonTee/LunarTUI
moon add WilliamZ1008/qtgui
moon add justjavac/moonbit-webview

# moon.mod.json 会自动更新 deps 字段
```

---

## 二、CLI 应用程序模板

### 基础 CLI 结构

```
cli_tool/
├── moon.mod.json
├── moon.pkg
├── cli_tool.mbt            # 核心逻辑
├── cli_tool_test.mbt
└── cmd/
    └── main/
        ├── main.mbt       # CLI 入口
        └── moon.pkg
```

### cmd/main/main.mbt - CLI 入口

```moonbit
///| CLI Application Entry Point

fn main {
  // 解析命令行参数
  let args = Sys::args()
  
  match args.length {
    0 | 1 => print_usage()
    _ => {
      let command = args[1]
      match command {
        "help" | "-h" | "--help" => print_usage()
        "version" | "-v" | "--version" => print_version()
        "run" => handle_run(args)
        "init" => handle_init(args)
        _ => {
          println("未知命令: " + command)
          print_usage()
        }
      }
    }
  }
}

fn print_usage() {
  println("Usage: cli-tool <command> [options]")
  println()
  println("Commands:")
  println("  help, -h, --help     显示帮助信息")
  println("  version, -v, --version 显示版本号")
  println("  run                 运行主功能")
  println("  init                初始化项目")
}

fn print_version() {
  println("cli-tool v0.1.0 (MoonBit)")
}
```

### cmd/main/moon.pkg - 入口包配置

```toml
import {
  "username/cli_tool" @lib,
}

options(
  "is-main": true,
)
```

### cli_tool.mbt - 核心逻辑

```moonbit
///| Core CLI Logic

// 数据结构定义
struct Config {
  input_path : String
  output_path : String
  verbose : Bool
  format : OutputFormat
}

enum OutputFormat {
  Json
  Csv
  Text
}

// 配置解析
fn parse_config(args : Array[String]) -> Result[Config, String] {
  // 实现参数解析逻辑
  Ok(Config::{
    input_path: "input.txt",
    output_path: "output.txt",
    verbose: false,
    format: Text,
  })
}

// 主处理函数
pub fn process(config : Config) -> Result[Unit, String] {
  if config.verbose {
    println("处理文件: " + config.input_path)
  }
  
  // 业务逻辑
  Ok(())
}
```

---

## 三、算法库模板

### 项目结构

```
algo_lib/
├── moon.mod.json
├── moon.pkg
├── src/
│   ├── sorting.mbt         # 排序算法
│   ├── searching.mbt       # 搜索算法
│   ├── data_structures.mbt # 数据结构
│   └── math.mbt            # 数学工具
├── src_test/
│   ├── sorting_test.mbt
│   └── searching_test.mbt
└── examples/
    └── demo.mbt
```

### 排序算法示例 (src/sorting.mbt)

```moonbit
///| Sorting Algorithms

// 快速排序
pub fn quick_sort[T](arr : Array[T], cmp : (T, T) -> Int) -> Array[T] {
  if arr.length <= 1 { return arr }
  
  let pivot = arr[arr.length / 2]
  let mut left : Array[T] = []
  let mut middle : Array[T] = []
  let mut right : Array[T] = []
  
  for elem in arr {
    let c = cmp(elem, pivot)
    if c < 0 { left.push(elem) }
    else if c > 0 { right.push(elem) }
    else { middle.push(elem) }
  }
  
  let sorted_left = quick_sort(left, cmp)
  let sorted_right = quick_sort(right, cmp)
  
  sorted_left + middle + sorted_right
}

// 归并排序
pub fn merge_sort[T](arr : Array[T], cmp : (T, T) -> Int) -> Array[T] {
  if arr.length <= 1 { return arr }
  
  let mid = arr.length / 2
  let left = merge_sort(arr[..mid], cmp)
  let right = merge_sort(arr[mid:], cmp)
  
  merge(left, right, cmp)
}

fn merge[T](left : Array[T], right : Array[T], cmp : (T, T) -> Int) -> Array[T] {
  let mut result : Array[T] = []
  let mut i = 0
  let mut j = 0
  
  while i < left.length && j < right.length {
    if cmp(left[i], right[j]) <= 0 {
      result.push(left[i])
      i += 1
    } else {
      result.push(right[j])
      j += 1
    }
  }
  
  while i < left.length {
    result.push(left[i])
    i += 1
  }
  
  while j < right.length {
    result.push(right[j])
    j += 1
  }
  
  result
}
```

### 数据结构示例 (src/data_structures.mbt)

```moonbit
///| Data Structures

// 链表节点
struct Node[T] {
  value : T
  next : Option[Node[T]]
}

// 链表操作
pub fn new_list[T]() -> Option[Node[T]] { None }

pub fn push[T](head : Option[Node[T]], value : T) -> Node[T] {
  Node::{ value: value, next: head }
}

pub fn to_array[T](head : Option[Node[T]]) -> Array[T] {
  let mut result : Array[T] = []
  let mut current = head
  
  match current {
    Some(node) => {
      result.push(node.value)
      current = node.next
    }
    None => {}
  }
  
  result
}

// 二叉树节点
struct TreeNode[T] {
  value : T
  left : Option[TreeNode[T]]
  right : Option[TreeNode[T]]
}

// 树的遍历
pub fn pre_order[T](node : Option[TreeNode[T]]) -> Array[T] {
  match node {
    None => []
    Some(n) => {
      let left_result = pre_order(n.left)
      let right_result = pre_order(n.right)
      [n.value] + left_result + right_result
    }
  }
}

pub fn in_order[T](node : Option[TreeNode[T]]) -> Array[T] {
  match node {
    None => []
    Some(n) => {
      let left_result = in_order(n.left)
      let right_result = in_order(n.right)
      left_result + [n.value] + right_result
    }
  }
}
```

---

## 四、计算库模板

### 数学工具库 (src/math.mbt)

```moonbit
///| Mathematical Computation Library

// 数值常量
const PI : Double = 3.14159265358979323846
const E : Double = 2.71828182845904523536
const PHI : Double = 1.61803398874989484820

// 基础数学函数
pub fn abs(x : Double) -> Double {
  if x >= 0.0 { x } else { -x.0 }
}

pub fn max(a : Double, b : Double) -> Double {
  if a >= b { a } else { b }
}

pub fn min(a : Double, b : Double) -> Double {
  if a <= b { a } else { b }
}

pub fn clamp(value : Double, min_val : Double, max_val : Double) -> Double {
  max(min_val, min(max_val, value))
}

pub fn pow(base : Double, exp : Int) -> Double {
  let mut result = 1.0
  let mut b = base
  let mut e = exp
  
  while e > 0 {
    if e & 1 == 1 { result *= b }
    b *= b
    e >>= 1
  }
  
  result
}

// 统计函数
pub fn mean(values : Array[Double]) -> Double {
  if values.length == 0 { return 0.0 }
  
  let mut sum = 0.0
  for v in values { sum += v }
  sum / values.length.to_double()
}

pub fn variance(values : Array[Double]) -> Double {
  if values.length <= 1 { return 0.0 }
  
  let m = mean(values)
  let mut sum_sq = 0.0
  for v in values {
    let diff = v - m
    sum_sq += diff * diff
  }
  sum_sq / (values.length - 1).to_double()
}

pub fn std_dev(values : Array[Double]) -> Double {
  sqrt(variance(values))
}

// 向量运算
pub struct Vec3 {
  x : Double
  y : Double
  z : Double
}

impl Vec3 with {
  pub fn new(x : Double, y : Double, z : Double) -> Vec3 {
    Vec3::{ x: x, y: y, z: z }
  }
  
  pub fn zero() -> Vec3 { Vec3::new(0.0, 0.0, 0.0) }
  
  pub fn add(self : Vec3, other : Vec3) -> Vec3 {
    Vec3::new(self.x + other.x, self.y + other.y, self.z + other.z)
  }
  
  pub fn sub(self : Vec3, other : Vec3) -> Vec3 {
    Vec3::new(self.x - other.x, self.y - other.y, self.z - other.z)
  }
  
  pub fn scale(self : Vec3, s : Double) -> Vec3 {
    Vec3::new(self.x * s, self.y * s, self.z * s)
  }
  
  pub fn dot(self : Vec3, other : Vec3) -> Double {
    self.x * other.x + self.y * other.y + self.z * other.z
  }
  
  pub fn length(self : Vec3) -> Double {
    sqrt(self.dot(self))
  }
  
  pub fn normalize(self : Vec3) -> Vec3 {
    let len = self.length
    if len > 0.0 { self.scale(1.0 / len) } else { self }
  }
}

// 矩阵运算
pub struct Mat2x2 {
  a : Double, b : Double,
  c : Double, d : Double,
}

impl Mat2x2 with {
  pub fn identity() -> Mat2x2 {
    Mat2x2::{ a: 1.0, b: 0.0, c: 0.0, d: 1.0 }
  }
  
  pub fn mul(self : Mat2x2, other : Mat2x2) -> Mat2x2 {
    Mat2x2::{
      a: self.a * other.a + self.b * other.c,
      b: self.a * other.b + self.b * other.d,
      c: self.c * other.a + self.d * other.c,
      d: self.c * other.b + self.d * other.d,
    }
  }
  
  pub fn determinant(self : Mat2x2) -> Double {
    self.a * self.d - self.b * self.c
  }
  
  pub fn transform(self : Mat2x2, x : Double, y : Double) -> (Double, Double) {
    (self.a * x + self.b * y, self.c * x + self.d * y)
  }
}
```

---

## 五、TUI 应用程序模板（LunarTUI）

### 安装依赖

```bash
moon add FrozenLemonTee/LunarTUI@0.0.1
```

### TUI 应用示例

```moonbit
///| Terminal UI Application using LunarTUI

typealias @widgets.Label as Label
typealias @widgets.ProgressBar as ProgressBar
typealias @widgets.Container as Container
typealias @layouts.VLayout as VLayout
typealias @layouts.HLayout as HLayout
typealias @terminal.Terminal as Terminal
typealias @base.Area as Area

fn main {
  // 初始化终端
  let terminal = Terminal::new(Area::new(80, 24))
  Terminal::clear()
  
  // 创建标题
  let title = Label::new(
    "🌙 MoonBit TUI Application",
    left=2, top=1,
  )
  
  // 创建进度条
  let progress = ProgressBar::new(
    100,
    value=0.65,
    left=2, top=5,
    prefix="Progress:",
    suffix="65%",
  )
  
  // 创建信息标签
  let info = Label::new(
    "Status: Running | Memory: 42MB | CPU: 12%",
    left=2, top=8,
  )
  
  // 使用垂直布局组织组件
  let layout = VLayout::new()
  let container = Container::new(
    0, 0, 80, 24,
    layout~,
    children=[title, progress, info],
  )
  
  // 渲染界面
  terminal.draw(container)
  Terminal::newline()
}
```

---

## 六、GUI 应用程序模板（WebView）

### 安装依赖

```bash
moon add justjavac/moonbit-webview
```

### WebView 应用示例

```moonbit
///| Desktop GUI Application using moonbit-webview

typealias @webview.WebView as WebView
typealias @webview.Size as Size
typealias @webview.Rect as Rect

fn main {
  // 创建 WebView 窗口
  let webview = WebView::new(
    title="MoonBit GUI App",
    url="https://www.moonbitlang.com",
    size=Size::new(1024, 768),
    resizable=true,
    debug=true,
  )
  
  // 设置窗口位置
  webview.set_position(Rect::new(100, 100))
  
  // 绑定 JavaScript 桥接函数
  webview.bind("greet", fn(name : String) -> String {
    "Hello from MoonBit, " + name + "!"
  })
  
  // 运行事件循环
  webview.run()
}
```

---

## 七、Qt GUI 应用程序模板

### 安装依赖

```bash
moon add WilliamZ1008/qtgui
```

### Qt GUI 示例

```moonbit
///| Qt GUI Application using moonbit-qt-gui

typealias @qtgui.Sys as Sys
typealias @qtgui.QApplication as QApplication
typealias @qtgui.QMainWindow as QMainWindow
typealias @qtgui.QLabel as QLabel
typealias @qtgui.QPushButton as QPushButton
typealias @qtgui.QWidget as QWidget
typealias @qtgui.QVBoxLayout as QVBoxLayout
typealias @qtgui.PyOS as PyOS

fn main {
  // 初始化系统
  let os = PyOS::new()
  let sys = Sys::new()
  let app = QApplication::new(sys.argv())
  app.setApplicationName("MoonBit Qt Demo")
  app.setApplicationVersion("1.0.0")
  
  // 创建主窗口
  let window = QMainWindow::new()
  window.setWindowTitle("🌙 MoonBit Qt Application")
  window.setMinimumSize(800, 600)
  window.set_geometry(100, 100, 1000, 700)
  
  // 创建中央控件
  let central_widget = QWidget::new(window)
  window.setCentralWidget(central_widget)
  
  // 创建布局
  let main_layout = QVBoxLayout::new(central_widget)
  
  // 添加标题标签
  let title_label = QLabel::new("Welcome to MoonBit Qt GUI!")
  main_layout.add_widget(title_label)
  
  // 添加按钮
  let button = QPushButton::new("Click Me!")
  main_layout.add_widget(button)
  
  // 显示窗口
  window.show()
  sys.exit(app.exec())
}
```

---

## 八、Web 应用程序模板（JS 后端）

### 配置 JS 后端

```json
// moon.mod.json 中添加
{
  "name": "username/my_web_app",
  "preferred-target": "js"
}
```

### JavaScript FFI 示例

```moonbit
///| Web Application with JavaScript FFI

extern "js" fn console_log(msg : String) -> Unit = "(msg) => console.log(msg)"

extern "js" fn fetch(url : String) -> JsPromise = "(url) => fetch(url)"

extern "js" fn json_parse(text : String) -> Dynamic = "(text) => JSON.parse(text)"

// 类型安全的 HTTP 请求
pub async fn get_json(url : String) -> Result[Dynamic, String] {
  try {
    let response = await fetch(url)
    let text = await response.text()
    Ok(json_parse(text))
  } catch e : Error {
    Err(e.message())
  }
}

fn main {
  console_log("Hello from MoonBit Web App!")
  
  // 异步获取数据
  async {
    match await get_json("https://api.example.com/data") {
      Ok(data) => console_log("Data received: " + data.to_string())
      Err(msg) => console_log("Error: " + msg)
    }
  }
}
```

---

## 九、Monorepo 多包项目模板（参考 moon-lottie） ⭐v2新增

### 适用场景
- 需要同时支持 Wasm-GC 和 JS 双目标构建的项目
- 核心库 + 多个可执行程序（运行时、CLI 工具等）
- 需要 JS/React/WebComponent 等语言绑定的跨平台库
- 包含示例/Playground 的开源项目

### 项目结构

```
monorepo-project/
├── moon.mod.json
├── pnpm-workspace.yaml          # npm workspace 配置
├── package.json                 # 根 package.json
├── lib/                         # 核心库代码
│   ├── core/
│   │   ├── moon.pkg
│   │   └── core.mbt            # 核心逻辑
│   └── utils/
│       ├── moon.pkg
│       └── utils.mbt           # 工具函数
├── cmd/                         # 可执行命令
│   ├── main_runtime/
│   │   ├── moon.pkg
│   │   └── main.mbt           # Wasm-GC 运行时入口
│   └── cli_tool/
│       ├── moon.pkg
│       └── main.mbt           # CLI 工具入口
├── packages/                    # 语言绑定/包装层
│   ├── js-binding/
│   │   ├── package.json
│   │   └── index.js           # JS 包装
│   └── react-component/
│       ├── package.json
│       └── index.tsx          # React 组件
├── demo/                        # 示例和 playground
│   └── playground/
│       ├── moon.pkg
│       └── main.mbt
└── README.md
```

### moon.mod.json 配置

```json
{
  "name": "username/monorepo-project",
  "version": "0.1.0",
  "readme": "README.md",
  "repository": "https://github.com/username/monorepo-project",
  "license": "MIT",
  "keywords": ["moonbit", "wasm", "monorepo"],
  "description": "MoonBit Monorepo 多包项目模板"
}
```

### lib/core/moon.pkg - 核心库配置

```toml
import {
  "username/monorepo-project/lib/utils" @lib,
}
```

### lib/core/core.mbt - 核心逻辑示例

```moonbit
///| Core Library - 核心引擎逻辑

// 数据结构定义
pub struct EngineConfig {
  debug_mode : Bool
  max_iterations : Int
}

// 核心处理函数
pub fn process_data(input : String, config : EngineConfig) -> String {
  if config.debug_mode {
    println("Debug: 处理输入数据")
  }
  
  let processed = transform(input)
  
  for i in 0..config.max_iterations {
    if i % 100 == 0 && config.debug_mode {
      println("迭代进度: " + i.to_string() + "/" + config.max_iterations.to_string())
    }
  }
  
  processed
}

fn transform(input : String) -> String {
  // 核心转换逻辑
  input.to_upper_case()
}

// 导出给 JS/Wasm 使用的关键函数
#[export]
pub fn version() -> String {
  "2.0.0"
}
```

### lib/utils/utils.mbt - 工具函数

```moonbit
///| Utility Functions - 通用工具函数

pub fn clamp(value : Int, min_val : Int, max_val : Int) -> Int {
  if value < min_val { min_val }
  else if value > max_val { max_val }
  else { value }
}

pub fn safe_div(a : Int, b : Int) -> Option[Int] {
  if b == 0 { None }
  else { Some(a / b) }
}

pub fn format_bytes(bytes : Int) -> String {
  let units = ["B", "KB", "MB", "GB"]
  let mut size = bytes.to_double()
  let mut unit_index = 0
  
  while size >= 1024.0 && unit_index < units.length - 1 {
    size /= 1024.0
    unit_index += 1
  }
  
  size.to_string() + " " + units[unit_index]
}
```

### cmd/main_runtime/main.mbt - Wasm-GC 运行时入口

```moonbit
///| Wasm-GC Runtime Entry Point

fn main {
  println("=== MoonBit Wasm-GC Runtime ===")
  println("版本: " + core::version())
  println()
  
  // 初始化引擎配置
  let config = core::EngineConfig::{
    debug_mode: true,
    max_iterations: 1000,
  }
  
  // 处理数据
  let result = core::process_data("Hello from Wasm!", config)
  println("结果: " + result)
}
```

### cmd/main_runtime/moon.pkg - 运行时入口配置

```toml
import {
  "username/monorepo-project/lib/core" @lib,
  "username/monorepo-project/lib/utils" @lib,
}

options(
  "is-main": true,
  "target": "wasm-gc",
)
```

### cmd/cli_tool/main.mbt - CLI 工具入口

```moonbit
///| CLI Tool Entry Point

fn main {
  let args = Sys::args()
  
  match args.length {
    0 | 1 => print_usage()
    _ => {
      match args[1] {
        "build-wasm" => build_wasm(args)
        "build-js" => build_js(args)
        "run" => run_project(args)
        _ => print_usage()
      }
    }
  }
}

fn print_usage() {
  println("Usage: monorepo-tool <command> [options]")
  println()
  println("Commands:")
  println("  build-wasm     构建 Wasm-GC 目标")
  println("  build-js        构建 JavaScript 目标")
  println("  run             运行项目")
  println("  help            显示帮助信息")
}

fn build_wasm(_args : Array[String]) {
  println("正在构建 Wasm-GC 目标...")
  // 构建逻辑
  println("✓ Wasm-Gc 构建完成")
}

fn build_js(_args : Array[String]) {
  println("正在构建 JavaScript 目标...")
  // 构建逻辑
  println("✓ JavaScript 构建完成")
}

fn run_project(_args : Array[String]) {
  println("运行项目...")
  // 运行逻辑
}
```

### npm workspace 配置

**pnpm-workspace.yaml**

```yaml
packages:
  - 'packages/*'
```

**根 package.json**

```json
{
  "name": "monorepo-project",
  "version": "0.1.0",
  "private": true,
  "description": "MoonBit Monorepo Project",
  "scripts": {
    "build:wasm": "moon build --target wasm-gc",
    "build:js": "moon build --target js",
    "build:all": "pnpm run build:wasm && pnpm run build:js",
    "test": "moon test",
    "dev": "moon watch"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/node": "^20.10.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

**packages/js-binding/package.json**

```json
{
  "name": "@username/js-binding",
  "version": "0.1.0",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  },
  "scripts": {
    "build": "tsc",
    "prepublishOnly": "npm run build"
  },
  "dependencies": {},
  "peerDependencies": {}
}
```

**packages/js-binding/index.js - JS 包装示例**

```javascript
/**
 * MoonBit JS Binding
 * 提供类型安全的 JavaScript API
 */

import init, { version, process_data } from '../target/lib/core.js';

let initialized = false;

async function initialize() {
  if (!initialized) {
    await init();
    initialized = true;
  }
}

export async function createEngine(options = {}) {
  await initialize();
  
  const config = {
    debugMode: options.debugMode ?? false,
    maxIterations: options.maxIterations ?? 1000,
  };
  
  return {
    version: version(),
    process: (input) => process_data(input, config),
  };
}

export default { createEngine };
```

### 双目标构建脚本

**build-wasm.sh**

```bash
#!/bin/bash
# 构建 Wasm-GC 目标

set -e

echo "🌙 构建 Wasm-GC 目标..."
moon build --target wasm-gc

# 检查输出
if [ -f "target/wasm-gc/build/main_runtime/main.wasm" ]; then
  echo "✓ Wasm 文件生成成功"
else
  echo "✗ Wasm 构建失败"
  exit 1
fi
```

**build-js.sh**

```bash
#!/bin/bash
# 构建 JavaScript 目标

set -e

echo "🌙 构建 JavaScript 目标..."
moon build --target js

# 检查输出
if [ -d "target/js/build/" ]; then
  echo "✓ JS 文件生成成功"
else
  echo "✗ JS 构建失败"
  exit 1
fi
```

---

## 十、解释器/编译器项目模板（参考 MoonBash） ⭐v2新增

### 适用场景
- 编程语言解释器或编译器
- DSL（领域特定语言）实现
- 配置文件解析器
- 表达式求值器
- 模板引擎

### 项目结构

```
interpreter-project/
├── moon.mod.json
├── src/
│   ├── lexer/
│   │   ├── moon.pkg
│   │   ├── token.mbt          # Token 类型定义（ADT）
│   │   └── lexer.mbt          # 词法分析器
│   ├── parser/
│   │   ├── moon.pkg
│   │   ├── ast.mbt            # AST 节点定义（ADT + Pattern Matching）
│   │   └── parser.mbt         # 语法分析器
│   ├── evaluator/
│   │   ├── moon.pkg
│   │   └── eval.mbt           # AST 求值器
│   ├── builtin/
│   │   ├── moon.pkg
│   │   └── commands.mbt       # 内置命令/函数
│   └── vm/
│       ├── moon.pkg
│       └── regex_vm.mbt       # VM-based 正则引擎
├── cmd/
│   └── repl/
│       ├── moon.pkg
│       └── main.mbt           # REPL 入口
└── tests/
    ├── lexer_test.mbt
    ├── parser_test.mbt
    └── integration_test.mbt
```

### src/lexer/token.mbt - Token 类型定义

```moonbit
///| Token Types - 使用 ADT 定义词法单元

enum TokenType {
  // 字面量
  NumberLit
  StringLit
  BoolLit
  Identifier
  
  // 运算符
  Plus        // +
  Minus       // -
  Star        // *
  Slash       // /
  Percent     // %
  Caret       // ^ (幂运算)
  
  // 比较运算符
  EqEq        // ==
  NotEq       // !=
  Lt          // <
  Gt          // >
  Le          // <=
  Ge          // >=
  
  // 逻辑运算符
  And         // &&
  Or          // ||
  Not         // !
  
  // 赋值
  Assign      // =
  PlusAssign  // +=
  MinusAssign // -=
  
  // 分隔符
  LParen      // (
  RParen      // )
  LBrace      // {
  RBrace      // }
  LBracket    // [
  RBracket    // ]
  Comma       // ,
  Semicolon   // ;
  Colon       // :
  Dot         // .
  Arrow       // ->
  
  // 关键字
  Fn          // fn
  Let         // let
  Mut         // mut
  If          // if
  Else        // else
  While       // while
  For         // for
  Return      // return
  Struct      // struct
  Enum        // enum
  Match       // match
  True        // true
  False       // false
  
  // 特殊
  EOF
  Error(String)
}

struct Token {
  token_type : TokenType
  lexeme : String
  line : Int
  column : Int
}

impl Token with {
  pub fn new(token_type : TokenType, lexeme : String, line : Int, column : Int) -> Token {
    Token::{ token_type: token_type, lexeme: lexeme, line: line, column: column }
  }
  
  pub fn to_string(self : Token) -> String {
    match self.token_type {
      Error(msg) => "Error(" + msg + ")"
      tt => tt.to_string()
    }
  }
}
```

### src/lexer/lexer.mbt - 词法分析器实现

```moonbit
///| Lexer Implementation - 将字符流转换为 Token 流

struct Lexer {
  source : String
  tokens : Array[Token]
  start : Int
  current : Int
  line : Int
  column : Int
}

impl Lexer with {
  pub fn new(source : String) -> Lexer {
    Lexer::{
      source: source,
      tokens: [],
      start: 0,
      current: 0,
      line: 1,
      column: 1,
    }
  }
  
  pub fn scan_tokens(self : Lexer) -> Array[Token] {
    while !self.is_at_end() {
      self.start = self.current
      self.scan_token()
    }
    
    self.tokens.push(Token::new(EOF, "", self.line, self.column))
    self.tokens
  }
  
  fn is_at_end(self : Lexer) -> Bool {
    self.current >= self.source.length
  }
  
  fn advance(self : Lexer) -> Char {
    let ch = self.source[self.current]
    self.current += 1
    self.column += 1
    ch
  }
  
  fn peek(self : Lexer) -> Char {
    if self.is_at_end() { '\0' }
    else { self.source[self.current] }
  }
  
  fn peek_next(self : Lexer) -> Char {
    if self.current + 1 >= self.source.length { '\0' }
    else { self.source[self.current + 1] }
  }
  
  fn match_char(self : Lexer, expected : Char) -> Bool {
    if self.is_at_end() || self.source[self.current] != expected {
      false
    } else {
      self.current += 1
      true
    }
  }
  
  fn add_token(self : Lexer, token_type : TokenType) {
    let text = self.source[self.start..self.current]
    self.tokens.push(Token::new(token_type, text, self.line, self.column))
  }
  
  fn add_token_error(self : Lexer, message : String) {
    self.tokens.push(Token::new(Error(message), "", self.line, self.column))
  }
  
  fn scan_token(self : Lexer) {
    let c = self.advance()
    
    match c {
      '(' => self.add_token(LParen)
      ')' => self.add_token(RParen)
      '{' => self.add_token(LBrace)
      '}' => self.add_token(RBrace)
      '[' => self.add_token(LBracket)
      ']' => self.add_token(RBracket)
      ',' => self.add_token(Comma)
      ';' => self.add_token(Semicolon)
      ':' => self.add_token(Colon)
      '.' => self.add_token(Dot)
      
      '-' => {
        if self.match_char('>') { self.add_token(Arrow) }
        else if self.match_char('=') { self.add_token(MinusAssign) }
        else { self.add_token(Minus) }
      }
      
      '+' => {
        if self.match_char('=') { self.add_token(PlusAssign) }
        else { self.add_token(Plus) }
      }
      
      '*' => self.add_token(Star)
      '/' => self.add_token(Slash)
      '%' => self.add_token(Percent)
      '^' => self.add_token(Caret)
      '!' => {
        if self.match_char('=') { self.add_token(NotEq) }
        else { self.add_token(Not) }
      }
      
      '=' => {
        if self.match_char('=') { self.add_token(EqEq) }
        else { self.add_token(Assign) }
      }
      
      '<' => {
        if self.match_char('=') { self.add_token(Le) }
        else { self.add_token(Lt) }
      }
      
      '>' => {
        if self.match_char('=') { self.add_token(Ge) }
        else { self.add_token(Gt) }
      }
      
      '&' => {
        if self.match_char('&') { self.add_token(And) }
        else { self.add_token_error("Unexpected character: &") }
      }
      
      '|' => {
        if self.match_char('|') { self.add_token(Or) }
        else { self.add_token_error("Unexpected character: |") }
      }
      
      '"' => self.string()
      
      ' ' | '\r' | '\t' => {} // 忽略空白字符
      
      '\n' => {
        self.line += 1
        self.column = 1
      }
      
      _ => {
        if c.is_digit() { self.number() }
        else if c.is_alpha() || c == '_' { self.identifier() }
        else { self.add_token_error("Unexpected character: " + c.to_string()) }
      }
    }
  }
  
  fn string(self : Lexer) {
    while self.peek() != '"' && !self.is_at_end() {
      if self.peek() == '\n' {
        self.line += 1
        self.column = 1
      }
      self.advance()
    }
    
    if self.is_at_end() {
      self.add_token_error("Unterminated string")
      return
    }
    
    // 闭合引号
    self.advance()
    
    // 提取字符串值（不包含引号）
    let value = self.source[(self.start + 1)..(self.current - 1)]
    self.add_token(StringLit)
  }
  
  fn number(self : Lexer) {
    while self.peek().is_digit() { self.advance() }
    
    // 支持小数点
    if self.peek() == '.' && self.peek_next().is_digit() {
      self.advance() // 消费小数点
      while self.peek().is_digit() { self.advance() }
    }
    
    self.add_token(NumberLit)
  }
  
  fn identifier(self : Lexer) {
    while self.peek().is_alphanumeric() || self.peek() == '_' { self.advance() }
    
    let text = self.source[self.start..self.current]
    
    // 检查是否是关键字
    match text {
      "fn" => self.add_token(Fn)
      "let" => self.add_token(Let)
      "mut" => self.add_token(Mut)
      "if" => self.add_token(If)
      "else" => self.add_token(Else)
      "while" => self.add_token(While)
      "for" => self.add_token(For)
      "return" => self.add_token(Return)
      "struct" => self.add_token(Struct)
      "enum" => self.add_token(Enum)
      "match" => self.add_token(Match)
      "true" => self.add_token(True)
      "false" => self.add_token(False)
      _ => self.add_token(Identifier)
    }
  }
}
```

### src/parser/ast.mbt - AST 节点定义

```moonbit
///| Abstract Syntax Tree - 抽象语法树节点定义

// 表达式节点
enum Expr {
  // 字面量
  Literal(LiteralExpr)
  
  // 变量引用
  Variable(String)
  
  // 一元运算
  Unary(UnaryOp, Expr)
  
  // 二元运算
  Binary(Expr, BinaryOp, Expr)
  
  // 函数调用
  Call(Expr, Array[Expr])
  
  // 成员访问
  Get(Expr, String)
  
  // 成员设置
  Set(Expr, String, Expr)
  
  // 分组表达式
  Grouping(Expr)
  
  // 赋值
  Assign(String, Expr)
  
  // Lambda/闭包
  Lambda(Array[String], Expr)
  
  // If 表达式
  IfExpr(Expr, Expr, Option[Expr])
  
  // 数组字面量
  ArrayLiteral(Array[Expr])
  
  // 结构体字面量
  StructLiteral(String, Array[(String, Expr)])
}

enum LiteralExpr {
  Num(Double)
  Str(String)
  Bool(bool)
  Nil
}

enum UnaryOp {
  Neg  // -
  Not  // !
  BitNot  // ~
}

enum BinaryOp {
  Add      // +
  Sub      // -
  Mul      // *
  Div      // /
  Mod      // %
  Pow      // ^
  Eq       // ==
  Neq      // !=
  Lt       // <
  Gt       // >
  Le       // <=
  Ge       // >=
  And      // &&
  Or       // ||
}

// 语句节点
enum Stmt {
  Expression(Expr)
  VarDecl(String, Option[Expr], Bool)  // 名称, 初始值, 是否可变
  FunctionDecl(String, Array[String], Array[Stmt])
  ReturnStmt(Option[Expr])
  Block(Array[Stmt])
  IfStmt(Stmt, Stmt, Option[Stmt])
  WhileStmt(Expr, Stmt)
  ForStmt(String, Expr, Expr, Stmt)
  BreakStmt
  ContinueStmt
}

// 程序（顶层声明）
struct Program {
  statements : Array[Stmt]
}

impl Program with {
  pub fn new(statements : Array[Stmt]) -> Program {
    Program::{ statements: statements }
  }
}
```

### src/parser/parser.mbt - 递归下降解析器

```moonbit
///| Parser Implementation - 递归下降语法分析器

struct Parser {
  tokens : Array[Token]
  current : Int
}

impl Parser with {
  pub fn new(tokens : Array[Token]) -> Parser {
    Parser::{ tokens: tokens, current: 0 }
  }
  
  pub fn parse(self : Parser) -> Result[Program, String] {
    let mut statements : Array[Stmt] = []
    
    while !self.is_at_end() {
      match self.declaration() {
        Ok(stmt) => statements.push(stmt),
        Err(e) => return Err(e),
      }
    }
    
    Ok(Program::new(statements))
  }
  
  fn is_at_end(self : Parser) -> Bool {
    self.peek_type() == EOF
  }
  
  fn peek_type(self : Parser) -> TokenType {
    self.tokens[self.current].token_type
  }
  
  fn previous(self : Parser) -> Token {
    self.tokens[self.current - 1]
  }
  
  fn advance(self : Parser) -> Token {
    if !self.is_at_end() { self.current += 1 }
    self.previous()
  }
  
  fn check(self : Parser, token_type : TokenType) -> Bool {
    if self.is_at_end() { false }
    else { self.peek_type() == token_type }
  }
  
  fn match_tokens(self : Parser, types : Array[TokenType]) -> Bool {
    for t in types {
      if self.check(t) {
        self.advance()
        return true
      }
    }
    false
  }
  
  fn consume(self : Parser, token_type : TokenType, message : String) -> Result[Token, String] {
    if self.check(token_type) { Ok(self.advance()) }
    else { Err(message) }
  }
  
  fn error(token : Token, message : String) -> String {
    "[第 " + token.line.to_string() + " 行] 错误: " + message
  }
  
  // 声明解析
  fn declaration(self : Parser) -> Result[Stmt, String] {
    match self.peek_type() {
      Fn => self.function_declaration(),
      Let => self.var_declaration(),
      _ => self.statement(),
    }
  }
  
  fn function_declaration(self : Parser) -> Result[Stmt, String] {
    self.consume(Fn, "期望 'fn'")
    let name = self.consume(Identifier, "期望函数名称")?
    self.consume(LParen, "期望 '('")
    
    let mut params : Array[String] = []
    if !self.check(RParen) {
      loop {
        let param = self.consume(Identifier, "期望参数名称")?
        params.push(param.lexeme)
        
        if !self.match_tokens([Comma]) { break }
      }
    }
    
    self.consume(RParen, "期望 ')'")
    let body = self.block_statement()?
    
    Ok(FunctionDecl(name.lexeme, params, body))
  }
  
  fn var_declaration(self : Parser) -> Result[Stmt, String] {
    self.consume(Let, "期望 'let'")
    let mut mutable = false
    
    if self.match_tokens([Mut]) {
      mutable = true
    }
    
    let name = self.consume(Identifier, "期望变量名称")?
    let mut initializer = None
    
    if self.match_tokens([Assign]) {
      initializer = Some(self.expression()?)
    }
    
    self.consume(Semicolon, "期望 ';' 在变量声明后")
    Ok(VarDecl(name.lexeme, initializer, mutable))
  }
  
  // 语句解析
  fn statement(self : Parser) -> Result[Stmt, String] {
    match self.peek_type() {
      If => self.if_statement(),
      While => self.while_statement(),
      For => self.for_statement(),
      Return => self.return_statement(),
      LBrace => self.block_statement(),
      _ => self.expression_statement(),
    }
  }
  
  fn if_statement(self : Parser) -> Result[Stmt, String] {
    self.consume(If, "期望 'if'")
    self.consume(LParen, "期望 '(' 在条件后")
    let condition = self.expression()?
    self.consume(RParen, "期望 ')' 在条件后")
    
    let then_branch = self.statement()?
    let mut else_branch = None
    
    if self.match_tokens([Else]) {
      else_branch = Some(self.statement()?)
    }
    
    Ok(IfStmt(then_branch, else_branch))
  }
  
  fn while_statement(self : Parser) -> Result[Stmt, String] {
    self.consume(While, "期望 'while'")
    self.consume(LParen, "期望 '(' 在条件后")
    let condition = self.expression()?
    self.consume(RParen, "期望 ')' 在条件后")
    let body = self.statement()?
    
    Ok(WhileStmt(condition, body))
  }
  
  fn block_statement(self : Parser) -> Result[Stmt, String> {
    self.consume(LBrace, "期望 '{'")
    
    let mut statements : Array[Stmt] = []
    while !self.check(RBrace) && !self.is_at_end() {
      statements.push(self.declaration()?)
    }
    
    self.consume(RBrace, "期望 '}'")
    Ok(Block(statements))
  }
  
  fn expression_statement(self : Parser) -> Result[Stmt, String] {
    let expr = self.expression()?
    self.consume(Semicolon, "期望 ';' 在表达式后")
    Ok(Expression(expr))
  }
  
  fn return_statement(self : Parser) -> Result[Stmt, String] {
    self.consume(Return, "期望 'return'")
    let mut value = None
    
    if !self.check(Semicolon) {
      value = Some(self.expression()?)
    }
    
    self.consume(Semicolon, "期望 ';' 在 return 后")
    Ok(ReturnStmt(value))
  }
  
  fn for_statement(self : Parser) -> Result[Stmt, String] {
    self.consume(For, "期望 'for'")
    let name = self.consume(Identifier, "期望循环变量")?
    self.consume(In, "期望 'in'")
    let iterable = self.expression()?
    let body = self.statement()?
    
    Ok(ForStmt(name.lexeme, iterable, body))
  }
  
  // 表达式解析（使用 Pratt 解析法）
  fn expression(self : Parser) -> Result[Expr, String] {
    self.assignment()
  }
  
  fn assignment(self : Parser) -> Result[Expr, String] {
    let expr = self.or_expr()?
    
    if self.match_tokens([Assign, PlusAssign, MinusAssign]) {
      let op = self.previous()
      let value = self.assignment()?
      
      match expr {
        Variable(name) => Ok(Assign(name, value)),
        _ => Err(self.error(op, "无效的赋值目标")),
      }
    } else {
      Ok(expr)
    }
  }
  
  fn or_expr(self : Parser) -> Result[Expr, String] {
    let mut expr = self.and_expr()?
    
    while self.match_tokens([Or]) {
      let right = self.and_expr()?
      expr = Binary(expr, Or, right)
    }
    
    Ok(expr)
  }
  
  fn and_expr(self : Parser) -> Result[Expr, String] {
    let mut expr = self.equality()?
    
    while self.match_tokens([And]) {
      let right = self.equality()?
      expr = Binary(expr, And, right)
    }
    
    Ok(expr)
  }
  
  fn equality(self : Parser) -> Result[Expr, String] {
    let mut expr = self.comparison()?
    
    while self.match_tokens([EqEq, NotEq]) {
      let op = self.previous()
      let right = self.comparison()?
      
      let bin_op = match op.token_type {
        EqEq => Eq
        NotEq => Neq
        _ => return Err(self.error(op, "无效的相等运算符")),
      }
      
      expr = Binary(expr, bin_op, right)
    }
    
    Ok(expr)
  }
  
  fn comparison(self : Parser) -> Result[Expr, String] {
    let mut expr = self.term()?
    
    while self.match_tokens([Lt, Gt, Le, Ge]) {
      let op = self.previous()
      let right = self.term()?
      
      let bin_op = match op.token_type {
        Lt => Lt
        Gt => Gt
        Le => Le
        Ge => Ge
        _ => return Err(self.error(op, "无效的比较运算符")),
      }
      
      expr = Binary(expr, bin_op, right)
    }
    
    Ok(expr)
  }
  
  fn term(self : Parser) -> Result[Expr, String] {
    let mut expr = self.factor()?
    
    while self.match_tokens([Minus, Plus]) {
      let op = self.previous()
      let right = self.factor()?
      
      let bin_op = match op.token_type {
        Minus => Sub
        Plus => Add
        _ => return Err(self.error(op, "无效的项运算符")),
      }
      
      expr = Binary(expr, bin_op, right)
    }
    
    Ok(expr)
  }
  
  fn factor(self : Parser) -> Result[Expr, String] {
    let mut expr = self.unary()?
    
    while self.match_tokens([Slash, Star, Percent]) {
      let op = self.previous()
      let right = self.unary()?
      
      let bin_op = match op.token_type {
        Slash => Div
        Star => Mul
        Percent => Mod
        _ => return Err(self.error(op, "无效的因子运算符")),
      }
      
      expr = Binary(expr, bin_op, right)
    }
    
    Ok(expr)
  }
  
  fn unary(self : Parser) -> Result[Expr, String] {
    if self.match_tokens([Not, Minus]) {
      let op = self.previous()
      let right = self.unary()?
      
      let un_op = match op.token_type {
        Not => Not
        Minus => Neg
        _ => return Err(self.error(op, "无效的一元运算符")),
      }
      
      Ok(Unary(un_op, right))
    } else {
      self.call()
    }
  }
  
  fn call(self : Parser) -> Result[Expr, String] {
    let mut expr = self.primary()?
    
    loop {
      if self.match_tokens([LParen]) {
        expr = self.finish_call(expr)?
      } else if self.match_tokens([Dot]) {
        let name = self.consume(Identifier, "期望属性名")?
        expr = Get(expr, name.lexeme)
      } else {
        break
      }
    }
    
    Ok(expr)
  }
  
  fn finish_call(self : Parser, callee : Expr) -> Result[Expr, String] {
    let mut arguments : Array[Expr] = []
    
    if !self.check(RParen) {
      loop {
        if arguments.length >= 255 {
          return Err(self.error(self.peek(), "参数数量不能超过 255"))
        }
        arguments.push(self.expression()?)
        if !self.match_tokens([Comma]) { break }
      }
    }
    
    self.consume(RParen, "期望 ')' 在参数列表后")
    Ok(Call(callee, arguments))
  }
  
  fn primary(self : Parser) -> Result[Expr, String] {
    match self.peek_type() {
      NumberLit => {
        let literal = self.advance()
        let value = literal.lexeme.to_double()
        Ok(Literal(Num(value)))
      }
      
      StringLit => {
        let literal = self.advance()
        // 移除引号
        let value = literal.lexeme[1..literal.lexeme.length - 1]
        Ok(Literal(Str(value)))
      }
      
      True => {
        self.advance()
        Ok(Literal(Bool(true)))
      }
      
      False => {
        self.advance()
        Ok(Literal(Bool(false)))
      }
      
      Identifier => {
        let name = self.advance()
        Ok(Variable(name.lexeme))
      }
      
      LParen => {
        self.advance()
        let expr = self.expression()?
        self.consume(RParen, "期望 ')' 在表达式后")
        Ok(Grouping(expr))
      }
      
      LBracket => {
        self.advance()
        let mut elements : Array[Expr] = []
        
        if !self.check(RBracket) {
          loop {
            elements.push(self.expression()?)
            if !self.match_tokens([Comma]) { break }
          }
        }
        
        self.consume(RBracket, "期望 ']' 在数组后")
        Ok(ArrayLiteral(elements))
      }
      
      _ => Err(self.error(self.peek(), "期望表达式")),
    }
  }
  
  fn peek(self : Parser) -> Token {
    self.tokens[self.current]
  }
}
```

### src/evaluator/eval.mbt - AST 求值器

```moonbit
///| Evaluator - AST 求值器，使用模式匹配进行表达式求值

enum Value {
  NumVal(Double)
  StrVal(String)
  BoolVal(bool)
  NilVal
  FuncVal(Array[String], Array[Stmt], Environment)
  BuiltInFunc((Array[Value]) -> Value)
}

struct Environment {
  values : Map[String, Value]
  parent : Option[Environment]
}

impl Environment with {
  pub fn new() -> Environment {
    Environment::{ 
      values: Map::new(), 
      parent: None 
    }
  }
  
  pub fn with_parent(parent : Environment) -> Environment {
    Environment::{ 
      values: Map::new(), 
      parent: Some(parent) 
    }
  }
  
  pub fn define(self : Environment, name : String, value : Value) {
    self.values.insert(name, value)
  }
  
  pub fn get(self : Environment, name : String) -> Result[Value, String] {
    match self.values.get(name) {
      Some(value) => Ok(value),
      None => {
        match self.parent {
          Some(parent_env) => parent_env.get(name),
          None => Err("未定义的变量: " + name),
        }
      }
    }
  }
  
  pub fn assign(self : Environment, name : String, value : Value) -> Result[Unit, String] {
    if self.values.contains_key(name) {
      self.values.insert(name, value)
      Ok(())
    } else {
      match self.parent {
        Some(parent_env) => parent_env.assign(name, value),
        None => Err("未定义的变量: " + name),
      }
    }
  }
}

struct Evaluator {
  environment : Environment
  globals : Environment
}

impl Evaluator with {
  pub fn new() -> Evaluator {
    let globals = Environment::new()
    builtin::register_builtins(globals)
    
    Evaluator::{
      environment: globals,
      globals: globals,
    }
  }
  
  pub fn interpret(self : Evaluator, program : Program) -> Result[Value, String] {
    let mut result : Value = NilVal
    
    for stmt in program.statements {
      result = self.execute_stmt(stmt)?
    }
    
    Ok(result)
  }
  
  fn execute_stmt(self : Evaluator, stmt : Stmt) -> Result[Value, String] {
    match stmt {
      Expression(expr) => self.evaluate(expr),
      
      VarDecl(name, initializer, _mutable) => {
        let value = match initializer {
          Some(init_expr) => self.evaluate(init_expr)?,
          None => NilVal,
        }
        self.environment.define(name, value)
        Ok(NilVal)
      }
      
      FunctionDecl(name, params, body) => {
        let func_value = FuncVal(params, body, self.environment)
        self.environment.define(name, func_value)
        Ok(NilVal)
      }
      
      ReturnStmt(value) => {
        let return_value = match value {
          Some(expr) => self.evaluate(expr)?,
          None => NilVal,
        }
        // 实际实现中需要异常机制来传播返回值
        Ok(return_value)
      }
      
      Block(statements) => {
        let previous = self.environment
        self.environment = Environment::with_parent(previous)
        
        let mut result : Value = NilVal
        for stmt in statements {
          result = self.execute_stmt(stmt)?
        }
        
        self.environment = previous
        Ok(result)
      }
      
      IfStmt(then_branch, else_branch) => {
        // 简化实现：实际需要先求值条件
        Ok(NilVal)
      }
      
      WhileStmt(condition, body) => {
        let mut result : Value = NilVal
        
        loop {
          let cond_value = self.evaluate(condition)?
          
          match cond_value {
            BoolVal(true) => {
              result = self.execute_stmt(body)?
              // 检查是否遇到 break/return
            }
            BoolVal(false) => break,
            _ => return Err("While 条件必须是布尔值"),
          }
        }
        
        Ok(result)
      }
      
      ForStmt(_, _, _) => Err("For 循环尚未实现"),
      BreakStmt => Err("Break 语句需要异常机制"),
      ContinueStmt => Err("Continue 语句需要异常机制"),
    }
  }
  
  fn evaluate(self : Evaluator, expr : Expr) -> Result[Value, String] {
    match expr {
      // 字面量
      Literal(literal) => {
        match literal {
          Num(n) => Ok(NumVal(n)),
          Str(s) => Ok(StrVal(s)),
          Bool(b) => Ok(BoolVal(b)),
          Nil => Ok(NilVal),
        }
      }
      
      // 变量引用
      Variable(name) => {
        self.environment.get(name)
      }
      
      // 一元运算
      Unary(op, operand) => {
        let right = self.evaluate(operand)?
        
        match (op, right) {
          (Neg, NumVal(n)) => Ok(NumVal(-n)),
          (Not, BoolVal(b)) => Ok(BoolVal(!b)),
          (_, v) => Err("一元运算符类型错误: " + v.to_string()),
        }
      }
      
      // 二元运算
      Binary(left_expr, op, right_expr) => {
        let left = self.evaluate(left_expr)?
        let right = self.evaluate(right_expr)?
        
        self.binary_operation(left, op, right)
      }
      
      // 函数调用
      Call(callee_expr, arguments) => {
        let callee = self.evaluate(callee_expr)?
        
        let mut arg_values : Array[Value] = []
        for arg in arguments {
          arg_values.push(self.evaluate(arg)?)
        }
        
        match callee {
          FuncVal(params, body, closure_env) => {
            if params.length != arg_values.length {
              return Err("参数数量错误: 期望 " + params.length.to_string() + 
                         ", 得到 " + arg_values.length.to_string())
            }
            
            let previous = self.environment
            self.environment = Environment::with_parent(closure_env)
            
            for i in 0..params.length {
              self.environment.define(params[i], arg_values[i])
            }
            
            let mut result : Value = NilVal
            for stmt in body {
              result = self.execute_stmt(stmt)?
            }
            
            self.environment = previous
            Ok(result)
          }
          
          BuiltInFunc(func) => {
            Ok(func(arg_values))
          }
          
          _ => Err("只能调用函数"),
        }
      }
      
      // 成员访问
      Get(_, _) => Err("成员访问尚未实现"),
      
      // 成员设置
      Set(_, _, _) => Err("成员设置尚未实现"),
      
      // 分组表达式
      Grouping(inner_expr) => {
        self.evaluate(inner_expr)
      }
      
      // 赋值
      Assign(name, value_expr) => {
        let value = self.evaluate(value_expr)?
        self.environment.assign(name, value)?;
        Ok(value)
      }
      
      // Lambda
      Lambda(params, body) => {
        Ok(FuncVal(params, [ReturnStmt(Some(body))], self.environment))
      }
      
      // If 表达式
      IfExpr(_, _, _) => Err("If 表达式尚未实现"),
      
      // 数组字面量
      ArrayLiteral(elements) => {
        let mut values : Array[Value] = []
        for elem in elements {
          values.push(self.evaluate(elem)?)
        }
        // 简化：实际应该使用数组类型的 Value
        Ok(NilVal)
      }
      
      // 结构体字面量
      StructLiteral(_, _) => Err("结构体字面量尚未实现"),
    }
  }
  
  fn binary_operation(self : Evaluator, left : Value, op : BinaryOp, right : Value) -> Result[Value, String] {
    match (op, left, right) {
      // 算术运算
      (Add, NumVal(l), NumVal(r)) => Ok(NumVal(l + r)),
      (Sub, NumVal(l), NumVal(r)) => Ok(NumVal(l - r)),
      (Mul, NumVal(l), NumVal(r)) => Ok(NumVal(l * r)),
      (Div, NumVal(l), NumVal(r)) => {
        if r == 0.0 { Err("除零错误") }
        else { Ok(NumVal(l / r)) }
      }
      (Mod, NumVal(l), NumVal(r)) => {
        if r == 0.0 { Err("模零错误") }
        else { Ok(NumVal(l % r)) }
      }
      
      // 比较运算
      (Eq, l, r) => Ok(BoolVal(self.is_equal(l, r))),
      (Neq, l, r) => Ok(BoolVal(!self.is_equal(l, r))),
      (Lt, NumVal(l), NumVal(r)) => Ok(BoolVal(l < r)),
      (Gt, NumVal(l), NumVal(r)) => Ok(BoolVal(l > r)),
      (Le, NumVal(l), NumVal(r)) => Ok(BoolVal(l <= r)),
      (Ge, NumVal(l), NumVal(r)) => Ok(BoolVal(l >= r)),
      
      // 逻辑运算
      (And, BoolVal(l), BoolVal(r)) => Ok(BoolVal(l && r)),
      (Or, BoolVal(l), BoolVal(r)) => Ok(BoolVal(l || r)),
      
      // 字符串连接
      (Add, StrVal(l), StrVal(r)) => Ok(StrVal(l + r)),
      
      _ => Err("二元运算类型错误"),
    }
  }
  
  fn is_equal(self : Evaluator, a : Value, b : Value) -> Bool {
    match (a, b) {
      (NumVal(x), NumVal(y)) => x == y,
      (StrVal(x), StrVal(y)) => x == y,
      (BoolVal(x), BoolVal(y)) => x == y,
      (NilVal, NilVal) => true,
      _ => false,
    }
  }
}
```

### src/builtin/commands.mbt - 内置命令注册表

```moonbit
///| Builtin Commands - 内置命令和函数注册表

pub fn register_builtins(env : Environment) {
  // 输入/输出函数
  env.define("print", BuiltInFunc(builtin_print))
  env.define("println", BuiltInFunc(builtin_println))
  env.define("input", BuiltInFunc(builtin_input))
  
  // 类型转换函数
  env.define("to_int", BuiltInFunc(builtin_to_int))
  env.define("to_string", BuiltInFunc(builtin_to_string))
  env.define("to_double", BuiltInFunc(builtin_to_double))
  env.define("type_of", BuiltInFunc(builtin_type_of))
  
  // 数学函数
  env.define("abs", BuiltInFunc(builtin_abs))
  env.define("min", BuiltInFunc(builtin_min))
  env.define("max", BuiltInFunc(builtin_max))
  env.define("sqrt", BuiltInFunc(builtin_sqrt))
  env.define("pow", BuiltInFunc(builtin_pow))
  env.define("floor", BuiltInFunc(builtin_floor))
  env.define("ceil", BuiltInFunc(builtin_ceil))
  env.define("round", BuiltInFunc(builtin_round))
  
  // 字符串函数
  env.define("length", BuiltInFunc(builtin_length))
  env.define("substring", BuiltInFunc(builtin_substring))
  env.define("contains", BuiltInFunc(builtin_contains))
  env.define("replace", BuiltInFunc(builtin_replace))
  env.define("trim", BuiltInFunc(builtin_trim))
  env.define("split", BuiltInFunc(builtin_split))
  env.define("upper", BuiltInFunc(builtin_upper))
  env.define("lower", BuiltInFunc(builtin_lower))
  
  // 数组函数
  env.define("push", BuiltInFunc(builtin_push))
  env.define("pop", BuiltInFunc(builtin_pop))
  env.define("array_length", BuiltInFunc(builtin_array_length))
  
  // 断言函数
  env.define("assert", BuiltInFunc(builtin_assert))
  env.define("assert_eq", BuiltInFunc(builtin_assert_eq))
  
  // 其他实用函数
  env.define("random", BuiltInFunc(builtin_random))
  env.define("time", BuiltInFunc(builtin_time))
  env.define("exit", BuiltInFunc(builtin_exit))
}

// I/O 函数实现
fn builtin_print(args : Array[Value]) -> Value {
  let output = args.map(fn(v) { value_to_string(v) }).join("")
  print(output)
  NilVal
}

fn builtin_println(args : Array[Value]) -> Value {
  let output = args.map(fn(v) { value_to_string(v) }).join(" ")
  println(output)
  NilVal
}

fn builtin_input(_args : Array[Value]) -> Value {
  let line = read_line()
  StrVal(line)
}

// 类型转换函数
fn builtin_to_int(args : Array[Value]) -> Value {
  match args[0] {
    NumVal(n) => NumVal(n.to_int().to_double()),
    StrVal(s) => {
      match s.parse_int() {
        Some(n) => NumVal(n.to_double()),
        None => NilVal,
      }
    }
    _ => NilVal,
  }
}

fn builtin_to_string(args : Array[Value]) -> Value {
  StrVal(value_to_string(args[0]))
}

fn builtin_to_double(args : Array[Value]) -> Value {
  match args[0] {
    NumVal(_) => args[0],
    StrVal(s) => {
      match s.parse_double() {
        Some(d) => NumVal(d),
        None => NilVal,
      }
    }
    _ => NilVal,
  }
}

fn builtin_type_of(args : Array[Value]) -> Value {
  StrVal(type_name(args[0]))
}

// 数学函数
fn builtin_abs(args : Array[Value]) -> Value {
  match args[0] {
    NumVal(n) => NumVal(if n < 0.0 { -n } else { n }),
    _ => NilVal,
  }
}

fn builtin_min(args : Array[Value]) -> Value {
  match (args[0], args[1]) {
    (NumVal(a), NumVal(b)) => NumVal(if a < b { a } else { b }),
    _ => NilVal,
  }
}

fn builtin_max(args : Array[Value]) -> Value {
  match (args[0], args[1]) {
    (NumVal(a), NumVal(b)) => NumVal(if a > b { a } else { b }),
    _ => NilVal,
  }
}

fn builtin_sqrt(args : Array[Value]) -> Value {
  match args[0] {
    NumVal(n) => NumVal(sqrt(n)),
    _ => NilVal,
  }
}

fn builtin_pow(args : Array[Value]) -> Value {
  match (args[0], args[1]) {
    (NumVal(base), NumVal(exp)) => NumVal(pow(base, exp.to_int())),
    _ => NilVal,
  }
}

fn builtin_floor(args : Array[Value]) -> Value {
  match args[0] {
    NumVal(n) => NumVal(floor(n).to_double()),
    _ => NilVal,
  }
}

fn builtin_ceil(args : Array[Value]) -> Value {
  match args[0] {
    NumVal(n) => NumVal(ceil(n).to_double()),
    _ => NilVal,
  }
}

fn builtin_round(args : Array[Value]) -> Value {
  match args[0] {
    NumVal(n) => NumVal(round(n).to_double()),
    _ => NilVal,
  }
}

// 字符串函数
fn builtin_length(args : Array[Value]) -> Value {
  match args[0] {
    StrVal(s) => NumVal(s.length.to_double()),
    _ => NilVal,
  }
}

fn builtin_substring(args : Array[Value]) -> Value {
  match (args[0], args[1], args[2]) {
    (StrVal(s), NumVal(start), NumVal(end)) => {
      StrVal(s[start.to_int()..end.to_int()])
    }
    _ => NilVal,
  }
}

fn builtin_contains(args : Array[Value]) -> Value {
  match (args[0], args[1]) {
    (StrVal(s), StrVal(sub)) => BoolVal(s.contains(sub)),
    _ => BoolVal(false),
  }
}

fn builtin_replace(args : Array[Value]) -> Value {
  match (args[0], args[1], args[2]) {
    (StrVal(s), StrVal(old), StrVal(new_str)) => {
      StrVal(s.replace(old, new_str))
    }
    _ => NilVal,
  }
}

fn builtin_trim(args : Array[Value]) -> Value {
  match args[0] {
    StrVal(s) => StrVal(s.trim()),
    _ => NilVal,
  }
}

fn builtin_split(args : Array[Value]) -> Value {
  match (args[0], args[1]) {
    (StrVal(s), StrVal(delimiter)) => {
      let parts = s.split(delimiter)
      // 简化：实际应返回数组
      NilVal
    }
    _ => NilVal,
  }
}

fn builtin_upper(args : Array[Value]) -> Value {
  match args[0] {
    StrVal(s) => StrVal(s.to_upper_case()),
    _ => NilVal,
  }
}

fn builtin_lower(args : Array[Value]) -> Value {
  match args[0] {
    StrVal(s) => StrVal(s.to_lower_case()),
    _ => NilVal,
  }
}

// 数组函数（简化实现）
fn builtin_push(_args : Array[Value]) -> Value {
  // 实际实现需要修改数组
  NilVal
}

fn builtin_pop(_args : Array[Value]) -> Value {
  // 实现需要修改数组
  NilVal
}

fn builtin_array_length(_args : Array[Value]) -> Value {
  NilVal
}

// 断言函数
fn builtin_assert(args : Array[Value]) -> Value {
  match args[0] {
    BoolVal(true) => NilVal,
    BoolVal(false) => {
      println("断言失败!")
      exit(1)
      NilVal
    }
    _ => NilVal,
  }
}

fn builtin_assert_eq(args : Array[Value]) -> Value {
  if is_equal(args[0], args[1]) {
    NilVal
  } else {
    println("断言失败: " + value_to_string(args[0]) + " != " + value_to_string(args[1]))
    exit(1)
    NilVal
  }
}

// 实用函数
fn builtin_random(_args : Array[Value]) -> Value {
  NumVal(random_double())
}

fn builtin_time(_args : Array[Value]) -> Value {
  NumVal(current_time_millis().to_double())
}

fn builtin_exit(args : Array[Value]) -> Value {
  match args[0] {
    NumVal(code) => exit(code.to_int()),
    _ => exit(0),
  }
  NilVal
}

// 辅助函数
fn value_to_string(value : Value) -> String {
  match value {
    NumVal(n) => n.to_string()
    StrVal(s) => s
    BoolVal(b) => if b { "true" } else { "false" }
    NilVal => "nil"
    FuncVal(_, _, _) => "<function>"
    BuiltInFunc(_) => "<builtin>"
  }
}

fn type_name(value : Value) -> String {
  match value {
    NumVal(_) => "number"
    StrVal(_) => "string"
    BoolVal(_) => "boolean"
    NilVal => "nil"
    FuncVal(_, _, _) => "function"
    BuiltInFunc(_) => "builtin"
  }
}

fn is_equal(a : Value, b : Value) -> Bool {
  match (a, b) {
    (NumVal(x), NumVal(y)) => x == y
    (StrVal(x), StrVal(y)) => x == y
    (BoolVal(x), BoolVal(y)) => x == y
    (NilVal, NilVal) => true
    _ => false
  }
}
```

### src/vm/regex_vm.mbt - VM-based 正则引擎

```moonbit
///| Regex VM - 基于 VM 的正则表达式引擎（ReDoS 免疫）

// 正则表达式指令集
enum RegexInstr {
  Match(Char)           // 匹配单个字符
  MatchAny              // 匹配任意字符
  MatchRange(Char, Char) // 匹配字符范围
  MatchClass(String)    // 匹配字符类
  Jump(Int)             // 无条件跳转
  Split(Int, Int)       // 分支跳转（回溯点）
  Save(Int)             // 保存当前位置到捕获组
  Accept                // 接受匹配
}

// 编译后的正则表达式
struct CompiledRegex {
  instructions : Array[RegexInstr]
  num_groups : Int
}

impl CompiledRegex with {
  pub fn new(instructions : Array[RegexInstr], num_groups : Int) -> CompiledRegex {
    CompiledRegex::{ 
      instructions: instructions, 
      num_groups: num_groups 
    }
  }
}

// VM 执行状态
struct Thread {
  pc : Int               // 程序计数器
  captures : Array[Int]  // 捕获组位置
}

impl Thread with {
  pub fn new(pc : Int, num_groups : Int) -> Thread {
    Thread::{ 
      pc: pc, 
      captures: Array::new(num_groups * 2, 0) 
    }
  }
}

// 匹配结果
struct MatchResult {
  matched : Bool
  captures : Array[Option[(Int, Int)]]
}

impl MatchResult with {
  pub fn success(captures : Array[Option[(Int, Int)]]) -> MatchResult {
    MatchResult::{ 
      matched: true, 
      captures: captures 
    }
  }
  
  pub fn failure() -> MatchResult {
    MatchResult::{ 
      matched: false, 
      captures: [] 
    }
  }
}

// 正则表达式编译器
struct RegexCompiler {
  pattern : String
  position : Int
  group_count : Int
  instructions : Array[RegexInstr]
}

impl RegexCompiler with {
  pub fn new(pattern : String) -> RegexCompiler {
    RegexCompiler::{
      pattern: pattern,
      position: 0,
      group_count: 0,
      instructions: [],
    }
  }
  
  pub fn compile(self : RegexCompiler) -> CompiledRegex {
    self.expr()
    
    self.instructions.push(Accept)
    
    CompiledRegex::new(self.instructions, self.group_count)
  }
  
  fn expr(self : RegexCompiler) {
    self.alternative()
    
    while self.position < self.pattern.length && self.pattern[self.position] == '|' {
      self.position += 1
      let fork_pos = self.instructions.length
      self.instructions.push(Split(0, 0)) // 占位
      let alt_start = self.instructions.length
      self.alternative()
      let jump_pos = self.instructions.length
      self.instructions.push(Jump(0)) // 占位
      self.instructions[fork_pos] = Split(alt_start, jump_pos + 1)
    }
  }
  
  fn alternative(self : RegexCompiler) {
    while self.position < self.pattern.length && 
          self.pattern[self.position] != ')' && 
          self.pattern[self.position] != '|' {
      self.term()
    }
  }
  
  fn term(self : RegexCompiler) {
    self.atom()
    
    // 处理量词
    if self.position < self.pattern.length {
      match self.pattern[self.position] {
        '*' => {
          self.position += 1
          self.quantifier_star()
        }
        '+' => {
          self.position += 1
          self.quantifier_plus()
        }
        '?' => {
          self.position += 1
          self.quantifier_question()
        }
        '{' => {
          // 支持 {n}, {n,m} 形式
          self.quantifier_range()
        }
        _ => {}
      }
    }
  }
  
  fn atom(self : RegexCompiler) {
    if self.position >= self.pattern.length { return }
    
    let c = self.pattern[self.position]
    
    match c {
      '(' => {
        self.position += 1
        let group_num = self.group_count
        self.group_count += 1
        self.instructions.push(Save(group_num * 2))
        self.expr()
        self.expect(')')
        self.instructions.push(Save(group_num * 2 + 1))
      }
      
      '[' => {
        self.char_class()
      }
      
      '.' => {
        self.position += 1
        self.instructions.push(MatchAny)
      }
      
      '\\' => {
        self.position += 1
        if self.position < self.pattern.length {
          let escaped = self.pattern[self.position]
          self.position += 1
          self.instructions.push(Match(escaped))
        }
      }
      
      '^' => {
        self.position += 1
        // 行首锚点（简化实现）
      }
      
      '$' => {
        self.position += 1
        // 行尾锚点（简化实现）
      }
      
      _ => {
        if c != '*' && c != '+' && c != '?' && c != '{' && c != '}' {
          self.position += 1
          self.instructions.push(Match(c))
        }
      }
    }
  }
  
  fn char_class(self : RegexCompiler) {
    self.position += 1 // 跳过 '['
    let negated = false
    
    if self.position < self.pattern.length && self.pattern[self.position] == '^' {
      negated = true
      self.position += 1
    }
    
    // 简化实现：实际应收集所有字符范围
    let class_content = ""
    while self.position < self.pattern.length && self.pattern[self.position] != ']' {
      class_content += self.pattern[self.position].to_string()
      self.position += 1
    }
    
    self.expect(']')
    self.instructions.push(MatchClass(class_content))
  }
  
  fn quantifier_star(self : RegexCompiler) {
    let split_pos = self.instructions.length
    self.instructions.push(Split(0, 0)) // 回退到循环开始 或 向前推进
    // split_pos 的指令将在编译完成后修正
  }
  
  fn quantifier_plus(self : RegexCompiler) {
    // + 至少匹配一次，然后变成 *
    let split_pos = self.instructions.length
    self.instructions.push(Split(0, 0))
  }
  
  fn quantifier_question(self : RegexCompiler) {
    let split_pos = self.instructions.length
    self.instructions.push(Split(0, 0))
  }
  
  fn quantifier_range(self : RegexCompiler) {
    self.position += 1 // 跳过 '{'
    
    // 解析最小次数
    let mut min_count = 0
    while self.position < self.pattern.length && 
          self.pattern[self.position].is_digit() {
      min_count = min_count * 10 + (self.pattern[self.position] - '0').to_int()
      self.position += 1
    }
    
    let mut max_count = min_count
    if self.position < self.pattern.length && self.pattern[self.position] == ',' {
      self.position += 1
      max_count = 0 // 无上限
      if self.position < self.pattern.length && 
         self.pattern[self.position].is_digit() {
        while self.position < self.pattern.length && 
              self.pattern[self.position].is_digit() {
          max_count = max_count * 10 + (self.pattern[self.position] - '0').to_int()
          self.position += 1
        }
      }
    }
    
    self.expect('}')
    
    // 展开为重复模式（简化实现）
    for _i in 0..min_count {
      // 复制前一个指令
    }
  }
  
  fn expect(self : RegexCompiler, expected : Char) {
    if self.position < self.pattern.length && 
       self.pattern[self.position] == expected {
      self.position += 1
    } else {
      // 编译错误
    }
  }
}

// VM 执行器
struct RegexVM {
  program : CompiledRegex
  input : String
}

impl RegexVM with {
  pub fn new(program : CompiledRegex, input : String) -> RegexVM {
    RegexVM::{ program: program, input: input }
  }
  
  /// 使用 NFA 模拟（基于线程的 VM）避免 ReDoS
  pub fn execute(self : RegexVM) -> MatchResult {
    if self.program.instructions.length == 0 {
      return MatchResult::failure()
    }
    
    // 当前活跃线程列表和下一轮线程列表
    let mut current_threads : Set[Thread] = Set::new()
    let mut next_threads : Set[Thread] = Set::new()
    
    // 初始化：从位置 0 开始
    current_threads.insert(Thread::new(0, self.program.num_groups))
    
    // 对每个输入位置执行一步
    for string_pos in 0..=self.input.length {
      // 执行当前所有线程
      for thread in current_threads {
        self.step(thread, string_pos, next_threads)
      }
      
      // 检查是否匹配成功
      for thread in next_threads {
        if thread.pc < self.program.instructions.length {
          match self.program.instructions[thread.pc] {
            Accept => {
              return MatchResult::success(
                self.extract_captures(thread.captures)
              )
            }
            _ => {}
          }
        }
      }
      
      // 准备下一轮
      current_threads = next_threads
      next_threads = Set::new()
    }
    
    MatchResult::failure()
  }
  
  fn step(self : RegexVM, thread : Thread, string_pos : Int, next_threads : Set[Thread]) {
    if thread.pc >= self.program.instructions.length { return }
    
    let instr = self.program.instructions[thread.pc]
    
    match instr {
      Match(expected_char) => {
        if string_pos < self.input.length && 
           self.input[string_pos] == expected_char {
          let mut new_thread = thread
          new_thread.pc += 1
          next_threads.insert(new_thread)
        }
      }
      
      MatchAny => {
        if string_pos < self.input.length {
          let mut new_thread = thread
          new_thread.pc += 1
          next_threads.insert(new_thread)
        }
      }
      
      MatchRange(start, end) => {
        if string_pos < self.input.length {
          let c = self.input[string_pos]
          if c >= start && c <= end {
            let mut new_thread = thread
            new_thread.pc += 1
            next_threads.insert(new_thread)
          }
        }
      }
      
      MatchClass(class_str) => {
        if string_pos < self.input.length {
          let c = self.input[string_pos]
          if class_str.contains(c.to_string()) {
            let mut new_thread = thread
            new_thread.pc += 1
            next_threads.insert(new_thread)
          }
        }
      }
      
      Jump(target) => {
        let mut new_thread = thread
        new_thread.pc = target
        // 不加入 next_threads，继续在当前步骤执行
        self.step(new_thread, string_pos, next_threads)
      }
      
      Split(target1, target2) => {
        // 创建两个分支
        let mut branch1 = thread
        branch1.pc = target1
        next_threads.insert(branch1)
        
        let mut branch2 = thread
        branch2.pc = target2
        next_threads.insert(branch2)
      }
      
      Save(group_idx) => {
        let mut new_thread = thread
        new_thread.captures[group_idx] = string_pos
        new_thread.pc += 1
        self.step(new_thread, string_pos, next_threads)
      }
      
      Accept => {
        // 已经在主循环中检查
        next_threads.insert(thread)
      }
    }
  }
  
  fn extract_captures(self : RegexVM, captures : Array[Int]) -> Array[Option[(Int, Int)]] {
    let mut result : Array[Option[(Int, Int)]] = []
    
    for i in 0..(self.program.num_groups * 2) step 2 {
      if captures[i] >= 0 && captures[i + 1] >= 0 {
        result.push(Some((captures[i], captures[i + 1])))
      } else {
        result.push(None)
      }
    }
    
    result
  }
}

// 公开 API
pub fn compile(pattern : String) -> CompiledRegex {
  let compiler = RegexCompiler::new(pattern)
  compiler.compile()
}

pub fn matches(regex : CompiledRegex, input : String) -> Bool {
  let vm = RegexVM::new(regex, input)
  vm.execute().matched
}

pub fn find_match(regex : CompiledRegex, input : String) -> Option[MatchResult] {
  let vm = RegexVM::new(regex, input)
  let result = vm.execute()
  if result.matched { Some(result) }
  else { None }
}
```

### cmd/repl/main.mbt - REPL 入口

```moonbit
///| REPL (Read-Eval-Print Loop)

fn main {
  println("╔══════════════════════════════════════╗")
  println("║     🌙 MoonBit Interpreter REPL      ║")
  println("║   输入表达式或语句，输入退出        ║")
  println("╚══════════════════════════════════════╝")
  println()
  
  let evaluator = Evaluator::new()
  let mut running = true
  
  while running {
    print(">>> ")
    let input = read_line()
    
    // 去除空白
    let trimmed = input.trim()
    
    if trimmed.length == 0 { continue }
    
    match trimmed {
      "quit" | "exit" | ":q" => {
        println("再见! 👋")
        running = false
      }
      
      ":help" | ":h" => {
        print_help()
      }
      
      ":clear" | ":c" => {
        // 清屏（平台相关）
        println("\x1b[2J\x1b[H")
      }
      
      _ => {
        // 词法分析
        let lexer = Lexer::new(input)
        let tokens = lexer.scan_tokens()
        
        // 检查是否有错误
        let has_error = tokens.any(fn(t) { 
          match t.token_type {
            Error(_) => true
            _ => false
          }
        })
        
        if has_error {
          println("❌ 词法错误:")
          for token in tokens {
            match token.token_type {
              Error(msg) => {
                println("  第 " + token.line.to_string() + " 行: " + msg)
              }
              _ => {}
            }
          }
        } else {
          // 语法分析
          let parser = Parser::new(tokens)
          match parser.parse() {
            Ok(program) => {
              // 执行
              match evaluator.interpret(program) {
                Ok(value) => {
                  println("=> " + eval::value_to_string(value))
                }
                Err(error_msg) => {
                  println("❌ 运行时错误: " + error_msg)
                }
              }
            }
            Err(parse_error) => {
              println("❌ 语法错误: " + parse_error)
            }
          }
        }
      }
    }
    
    println()
  }
}

fn print_help() {
  println("可用命令:")
  println("  :help, :h     显示帮助信息")
  println("  :clear, :c    清屏")
  println("  quit, exit    退出 REPL")
  println()
  println("语言特性:")
  println("  - 变量声明: let x = 42")
  println("  - 可变变量: let mut x = 10")
  println("  - 函数定义: fn add(a, b) { a + b }")
  println("  - 条件语句: if x > 0 { ... } else { ... }")
  println("  - 循环: while condition { ... }")
  println("  - 打印: println(\"Hello\")")
  println()
  println("内置函数:")
  println("  - print, println, input")
  println("  - abs, min, max, sqrt, pow")
  println("  - length, substring, contains, replace")
  println("  - to_int, to_string, to_double")
  println("  - type_of, assert, assert_eq")
}
```

---

## 十一、属性驱动代码生成项目模板（参考 morm） ⭐v2新增

### 适用场景
- ORM（对象关系映射）框架
- API 代码生成器
- 序列化/反序列化库
- 数据验证框架
- 依赖注入容器
- 任何需要元编程的场景

### 项目结构

```
attribute-driven-project/
├── moon.mod.json
├── src/
│   ├── attributes/
│   │   ├── moon.pkg
│   │   └── attrs.mbt          # 自定义属性定义
│   ├── generator/
│   │   ├── moon.pkg
│   │   └── gen.mbt            # 代码生成器
│   ├── engine/
│   │   ├── moon.pkg
│   │   └── engine.mbt         # 核心引擎
│   ├── dialect/
│   │   ├── moon.pkg
│   │   └── dialect.mbt        # 方言适配
│   └── main/
│       ├── moon.pkg
│       └── api.mbt            # 公开 API
├── cmd/
│   └── generator/
│       ├── moon.pkg
│       └── main.mbt           # 代码生成命令入口
└── example/
    ├── entity.mbt             # 用户定义的实体
    └── entity.g.mbt           # 自动生成的代码
```

### src/attributes/attrs.mbt - 自定义属性定义

```moonbit
///| Custom Attributes - 自定义属性系统

// 属性基础类型
struct Attribute {
  name : String
  parameters : Array[AttributeParam]
}

struct AttributeParam {
  key : String
  value : AttributeValue
}

enum AttributeValue {
  StringVal(String)
  IntVal(Int)
  BoolVal(bool)
  ArrayVal(Array[AttributeValue])
}

// 预定义属性常量

// 实体属性
pub const ATTR_ENTITY : String = "entity"

// 主键属性
pub const ATTR_PRIMARY_KEY : String = "primary_key"

// 外键属性
pub const ATTR_FOREIGN_KEY : String = "foreign_key"

// 唯一约束属性
pub const ATTR_UNIQUE : String = "unique"

// 索引属性
pub const ATTR_INDEX : String = "index"

// 列属性（映射到数据库列）
pub const ATTR_COLUMN : String = "column"

// 默认值属性
pub const ATTR_DEFAULT : String = "default"

// 非空约束属性
pub const ATTR_NOT_NULL : String = "not_null"

// 最大长度属性
pub const ATTR_MAX_LENGTH : String = "max_length"

// 最小值属性
pub const ATTR_MIN : String = "min"

// 最大值属性
pub const ATTR_MAX : String = "max"

// 正则验证属性
pub const ATTR_PATTERN : String = "pattern"

// 自动增长属性
pub const ATTR_AUTO_INCREMENT : String = "auto_increment"

// 忽略属性（不映射到数据库）
pub const ATTR_IGNORE : String = "ignore"

// 嵌套实体属性
pub const ATTR_EMBEDDED : String = "embedded"

// 多对多关联属性
pub const ATTR_MANY_TO_MANY : String = "many_to_many"

// 一对多关联属性
pub const ATTR_ONE_TO_MANY : String = "one_to_many"

// 多对一关联属性
pub const ATTR_MANY_TO_ONE : String = "many_to_one"

// 级联操作属性
pub const ATTR_CASCADE : String = "cascade"

// 延迟加载属性
pub const ATTR_LAZY : String = "lazy"

// 表名属性
pub const ATTR_TABLE_NAME : String = "table_name"

// Schema 属性
pub const ATTR_SCHEMA : String = "schema"

// 注释属性
pub const ATTR_COMMENT : String = "comment"

// 属性解析工具
pub struct ParsedAttribute {
  attribute_name : String
  params : Map[String, AttributeValue]
}

impl ParsedAttribute with {
  pub fn new(attribute_name : String) -> ParsedAttribute {
    ParsedAttribute::{
      attribute_name: attribute_name,
      params: Map::new(),
    }
  }
  
  pub fn set_param(self : ParsedAttribute, key : String, value : AttributeValue) {
    self.params.insert(key, value)
  }
  
  pub fn get_param(self : ParsedAttribute, key : String) -> Option[AttributeValue] {
    self.params.get(key)
  }
  
  pub fn get_string_param(self : ParsedAttribute, key : String, default : String) -> String {
    match self.params.get(key) {
      Some(StringVal(v)) => v,
      _ => default,
    }
  }
  
  pub fn get_int_param(self : ParsedAttribute, key : String, default : Int) -> Int {
    match self.params.get(key) {
      Some(IntVal(v)) => v,
      _ => default,
    }
  }
  
  pub fn get_bool_param(self : ParsedAttribute, key : String, default : bool) -> bool {
    match self.params.get(key) {
      Some(BoolVal(v)) => v,
      _ => default,
    }
  }
}

// 属性注解接口（伪代码，展示设计意图）
/*
// 用户使用方式示例：
//
// #[entity(table_name="users")]
// struct User {
// #[
column(name="post_content"), not_null]
  content : String
  
  #[default("draft")]
  status : String
  
  #[column(name="view_count"), default(0), min(0)]
  view_count : Int
  
  #[not_null]
  published_at : DateTime
  
  #[column(name="updated_at")]
  updated_at : DateTime
  
  #[many_to_one("users.id"), cascade(delete=Cascade, update=Restrict)]
  updater_id : Int
  
  #[ignore]
  computed_field : String
}

// ============================================
// 评论实体（演示关联）
// ============================================
#[entity(table_name="comments")]
struct Comment {
  #[primary_key(auto_increment=true)]
  id : Int
  
  #[foreign_key("posts.id"), not_null]
  post_id : Int
  
  #[foreign_key("users.id"), not_null]
  user_id : Int
  
  #[not_null, max_length(2000)]
  content : String
  
  #[default(false)]
  is_approved : Bool
  
  #[not_null]
  created_at : DateTime
}

// ============================================
// 标签实体（演示多对多关联）
// ============================================
#[entity(table_name="tags")]
struct Tag {
  #[primary_key(auto_increment=true)]
  id : Int
  
  #[not_null, max_length(50), unique]
  name : String
  
  #[column(name="slug"), max_length(50), unique]
  slug : String
}

// ============================================
// 文章-标签关联表（中间表）
// ============================================
#[entity(table_name="post_tags")]
struct PostTag {
  #[primary_key]
  id : Int
  
  #[foreign_key("posts.id"), not_null, primary_key]
  post_id : Int
  
  #[foreign_key("tags.id"), not_null, primary_key]
  tag_id : Int
  
  #[column(name="sort_order"), default(0)]
  sort_order : Int
}
```

#### example/entity.g.mbt - 自动生成的代码示例

```moonbit
///| Generated Code - 由属性驱动代码生成器自动生成
///
/// ⚠️ 警告: 此文件由代码生成器自动生成
/// ❌ 请勿手动编辑 - 所有更改将被覆盖!
///
/// 生成时间: 2026-05-17 10:30:00
/// 生成器版本: v2.0.0
/// 源文件: example/entity.mbt

// ============================================
// User 实体生成代码
// ============================================

// 表信息
pub struct UserTableInfo {
  table_name : String,
  schema : String,
  fields : Array[FieldInfo],
}

pub fn user_table_info() -> UserTableInfo {
  UserTableInfo::{
    table_name: "users",
    schema: "public",
    fields: [
      FieldInfo::{
        name: "id",
        column: "id",
        type: "Int",
        is_primary_key: true,
        is_nullable: false,
        is_auto_increment: true,
      },
      FieldInfo::{
        name: "username",
        column: "username",
        type: "String",
        is_primary_key: false,
        is_nullable: false,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "email",
        column: "email_address",
        type: "String",
        is_primary_key: false,
        is_nullable: false,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "password_hash",
        column: "password_hash",
        type: "String",
        is_primary_key: false,
        is_nullable: false,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "display_name",
        column: "display_name",
        type: "String",
        is_primary_key: false,
        is_nullable: true,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "is_active",
        column: "is_active",
        type: "Bool",
        is_primary_key: false,
        is_nullable: true,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "created_at",
        column: "created_at",
        type: "DateTime",
        is_primary_key: false,
        is_nullable: false,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "updated_at",
        column: "updated_at",
        type: "DateTime",
        is_primary_key: false,
        is_nullable: true,
        is_auto_increment: false,
      },
    ],
  }
}

// 字段访问器
pub fn get_id(user : User) -> Int {
  user.id
}

pub fn get_id_column() -> String {
  "id"
}

pub fn get_username(user : User) -> String {
  user.username
}

pub fn get_username_column() -> String {
  "username"
}

pub fn get_email(user : User) -> String {
  user.email
}

pub fn get_email_column() -> String {
  "email_address"
}

// ... 其他字段访问器 ...

// CRUD 操作
pub fn insert_user(user : User) -> String {
  let columns = ["id", "username", "email_address", "password_hash", "display_name", "is_active", "created_at", "updated_at"]
  let placeholders = columns.map(fn(_) { "?" }).join(", ")
  "INSERT INTO users (" + columns.join(", ") + ") VALUES (" + placeholders + ")"
}

pub fn select_user_by_id(id : Int) -> String {
  "SELECT * FROM users WHERE id = ?"
}

pub fn update_user(user : User) -> String {
  let sets = ["username = ?", "email_address = ?", "password_hash = ?", "display_name = ?", "is_active = ?", "updated_at = ?"]
  "UPDATE users SET " + sets.join(", ") + " WHERE id = ?"
}

pub fn delete_user(id : Int) -> String {
  "DELETE FROM users WHERE id = ?"
}

// 查询方法
pub fn find_all_users() -> String {
  "SELECT * FROM users"
}

pub fn find_user_by_username(username : String) -> String {
  "SELECT * FROM users WHERE username = ?"
}

pub fn find_user_by_email(email : String) -> String {
  "SELECT * FROM users WHERE email_address = ?"
}

pub fn count_users() -> String {
  "SELECT COUNT(*) FROM users"
}

pub fn exists_user(id : Int) -> String {
  "SELECT EXISTS(SELECT 1 FROM users WHERE id = ?)"
}

// 验证方法
pub fn validate_user(user : User) -> Array[String] {
  let mut errors : Array[String] = []
  
  // 验证 username 非空
  match user.username {
    "" => errors.push("username 不能为空"),
    _ => {}
  }
  
  // 验证 username 最大长度
  if user.username.length > 50 {
    errors.push("username 长度不能超过 50")
  }
  
  // 验证 email 非空
  match user.email {
    "" => errors.push("email 不能为空"),
    _ => {}
  }
  
  // 验证 email 格式
  if !(user.email =~ re"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$") {
    errors.push("email 格式不正确")
  }
  
  // 验证 password_hash 非空
  match user.password_hash {
    "" => errors.push("password_hash 不能为空"),
    _ => {}
  }
  
  // 验证 password_hash 最大长度
  if user.password_hash.length > 255 {
    errors.push("password_hash 长度不能超过 255")
  }
  
  // 验证 display_name 最大长度
  if user.display_name.length > 100 {
    errors.push("display_name 长度不能超过 100")
  }
  
  errors
}

// ============================================
// Role 实体生成代码
// ============================================

pub struct RoleTableInfo {
  table_name : String,
  schema : String,
  fields : Array[FieldInfo],
}

pub fn role_table_info() -> RoleTableInfo {
  RoleTableInfo::{
    table_name: "roles",
    schema: "public",
    fields: [
      FieldInfo::{
        name: "id",
        column: "id",
        type: "Int",
        is_primary_key: true,
        is_nullable: false,
        is_auto_increment: true,
      },
      FieldInfo::{
        name: "name",
        column: "name",
        type: "String",
        is_primary_key: false,
        is_nullable: false,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "description",
        column: "description",
        type: "String",
        is_primary_key: false,
        is_nullable: true,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "is_system",
        column: "is_system",
        type: "Bool",
        is_primary_key: false,
        is_nullable: true,
        is_auto_increment: false,
      },
    ],
  }
}

pub fn insert_role(role : Role) -> String {
  "INSERT INTO roles (id, name, description, is_system) VALUES (?, ?, ?, ?)"
}

pub fn select_role_by_id(id : Int) -> String {
  "SELECT * FROM roles WHERE id = ?"
}

pub fn update_role(role : Role) -> String {
  "UPDATE roles SET name = ?, description = ?, is_system = ? WHERE id = ?"
}

pub fn delete_role(id : Int) -> String {
  "DELETE FROM roles WHERE id = ?"
}

pub fn find_all_roles() -> String {
  "SELECT * FROM roles"
}

pub fn find_role_by_name(name : String) -> String {
  "SELECT * FROM roles WHERE name = ?"
}

pub fn count_roles() -> String {
  "SELECT COUNT(*) FROM roles"
}

pub fn validate_role(role : Role) -> Array[String] {
  let mut errors : Array[String] = []
  
  // 验证 name 非空
  match role.name {
    "" => errors.push("name 不能为空"),
    _ => {}
  }
  
  // 验证 name 最大长度
  if role.name.length > 50 {
    errors.push("name 长度不能超过 50")
  }
  
  // 验证 description 最大长度
  if role.description.length > 200 {
    errors.push("description 长度不能超过 200")
  }
  
  errors
}

// ============================================
// Post 实体生成代码（包含关联）
// ============================================

pub struct PostTableInfo {
  table_name : String,
  schema : String,
  fields : Array[FieldInfo],
  relations : Array[RelationInfo],
}

pub fn post_table_info() -> PostTableInfo {
  PostTableInfo::{
    table_name: "posts",
    schema: "content",
    fields: [
      FieldInfo::{
        name: "id",
        column: "id",
        type: "Int",
        is_primary_key: true,
        is_nullable: false,
        is_auto_increment: true,
      },
      FieldInfo::{
        name: "author_id",
        column: "author_id",
        type: "Int",
        is_primary_key: false,
        is_nullable: false,
        is_auto_increment: false,
      },
      // ... 其他字段 ...
    ],
    relations: [
      RelationInfo::{
        relation_type: ManyToOne,
        field_name: "author",
        target_entity: "User",
        target_field: "id",
        foreign_key_column: "author_id",
      },
      RelationInfo::{
        relation_type: ManyToOne,
        field_name: "updater",
        target_entity: "User",
        target_field: "id",
        foreign_key_column: "updater_id",
      },
    ],
  }
}

// 关联查询方法
pub fn find_post_with_author(post_id : Int) -> String {
  "SELECT p.*, u.username as author_username, u.display_name as author_display_name " +
  "FROM posts p LEFT JOIN users u ON p.author_id = u.id WHERE p.id = ?"
}

pub fn find_posts_by_author(author_id : Int) -> String {
  "SELECT * FROM posts WHERE author_id = ? ORDER BY created_at DESC"
}

// ... 其他 Post 相关方法 ...

// ============================================
// 辅助函数
// ============================================

struct FieldInfo {
  name : String,
  column : String,
  type : String,
  is_primary_key : Bool,
  is_nullable : Bool,
  is_auto_increment : Bool,
}

struct RelationInfo {
  relation_type : RelationType,
  field_name : String,
  target_entity : String,
  target_field : String,
  foreign_key_column : String,
}

enum RelationType {
  OneToOne
  OneToMany
  ManyToOne
  ManyToMany
}

pub fn get_all_tables() -> Array[String] {
  ["users", "roles", "posts", "comments", "tags", "post_tags"]
}

pub fn get_table_entities() -> Array[String] {
  ["User", "Role", "Post", "Comment", "Tag", "PostTag"]
}
```

---

## 资源索引

### 官方资源
- MoonBit 文档：https://docs.moonbitlang.com/zh-cn/stable/
- MoonBit 教程：https://docs.moonbitlang.com/zh-cn/latest/tutorial/tour.html
- Mooncakes 包仓库：https://mooncakes.io
- MoonBit 更新日志：https://www.moonbitlang.com/weekly-updates

### 第三方库
- **LunarTUI** (TUI 框架)：`moon add FrozenLemonTee/LunarTUI`
- **moonbit-qt-gui** (Qt GUI)：`moon add WilliamZ1008/qtgui`
- **moonbit-webview** (WebView GUI)：`moon add justjavac/moonbit-webview`

### v0.9 新特性参考
- Debug trait 替代 derive(Show)
- 正则表达式匹配 `s =~ re"..."`
- 反向管道语法 `<|`
- 形式化验证支持 `proof_ensure`
- Int64/UInt64 在 JS 后端编译为 BigInt

## 注意事项
- MoonBit 当前处于 beta-preview 阶段，API 可能变动
- 不同后端（wasm/js/native）支持的功能有差异
- FFI 调用需要了解目标平台的类型映射
- 使用 `moon mod tidy` 自动整理依赖
- 生产环境建议锁定依赖版本primary_key(auto_increment=true)]
//   id : Int
//   
//   #[column(name="user_name"), not_null, max_length(50)]
//   username : String
//   
//   #[unique]
//   email : String
//   
//   #[default=false)]
//   is_active : Bool
//   
//   #[foreign_key("roles.id")]
//   role_id : Int
//   
//   #[ignore]
//   temp_field : String
// }
*/
```

### src/generator/gen.mbt - 代码生成器

```moonbit
///| Code Generator - 从带属性的源码生成目标代码

struct CodeGenerator {
  source_code : String
  generated_code : String
  indent_level : Int
}

impl CodeGenerator with {
  pub fn new(source_code : String) -> CodeGenerator {
    CodeGenerator::{
      source_code: source_code,
      generated_code: "",
      indent_level: 0,
    }
  }
  
  /// 主入口：生成代码
  pub fn generate(self : CodeGenerator) -> String {
    // 1. 解析源文件，提取实体和属性
    let entities = self.parse_entities()
    
    // 2. 为每个实体生成代码
    self.generated_code = self.generate_header()
    
    for entity in entities {
      self.generated_code += self.generate_entity(entity)
    }
    
    // 3. 生成辅助函数
    self.generated_code += self.generate_helpers()
    
    self.generated_code
  }
  
  /// 解析实体定义
  fn parse_entities(self : CodeGenerator) -> Array[EntityDef] {
    let mut entities : Array[EntityDef] = []
    let lines = self.source_code.split("\n")
    let mut current_entity : Option[EntityDef] = None
    let mut in_struct = false
    
    for line in lines {
      let trimmed = line.trim()
      
      // 检测实体属性
      if trimmed.starts_with("#[") && trimmed.contains("entity") {
        let entity_attr = self.parse_entity_attribute(trimmed)
        current_entity = Some(EntityDef::new(
          entity_attr.get_string_param("table_name", ""),
          entity_attr.get_string_param("schema", "public"),
          entity_attr.get_string_param("comment", ""),
        ))
      }
      
      // 检测结构体定义
      if trimmed.starts_with("struct ") && current_entity.is_some() {
        in_struct = true
        let name = trimmed.split(" ")[1].split("{")[0]
        current_entity.unwrap().name = name
      }
      
      // 解析字段
      if in_struct && trimmed.contains(":") && !trimmed.starts_with("}") {
        let field_def = self.parse_field_definition(trimmed)
        match current_entity {
          Some(ref mut entity) => entity.fields.push(field_def),
          None => {}
        }
      }
      
      // 结束结构体
      if trimmed.starts_with("}") && in_struct {
        in_struct = false
        match current_entity {
          Some(entity) => entities.push(entity),
          None => {}
        }
        current_entity = None
      }
    }
    
    entities
  }
  
  /// 解析实体级别的属性
  fn parse_entity_attribute(self : CodeGenerator, attr_str : String) -> ParsedAttribute {
    let attr = ParsedAttribute::new(ATTR_ENTITY)
    
    // 提取括号内的内容
    if attr_str.contains("(") {
      let content = attr_str.between("(", ")")
      let params = self.parse_params(content)
      
      for (key, value) in params {
        attr.set_param(key, value)
      }
    }
    
    attr
  }
  
  /// 解析字段定义
  fn parse_field_definition(self : CodeGenerator, field_str : String) -> FieldDef {
    // 分离属性和字段声明
    let mut attrs : Array[ParsedAttribute] = []
    let mut decl = field_str
    
    // 提取所有 #[...] 属性
    while decl.starts_with("#[") {
      let end = decl.index_of("]") + 1
      let attr_str = decl[..end]
      attrs.push(self.parse_field_attribute(attr_str))
      decl = decl[end..].trim()
    }
    
    // 解析字段名和类型
    let parts = decl.split(":")
    let field_name = parts[0].trim()
    let field_type = parts[1].trim().replace(",", "")
    
    FieldDef::new(field_name, field_type, attrs)
  }
  
  /// 解析字段属性
  fn parse_field_attribute(self : CodeGenerator, attr_str : String) -> ParsedAttribute {
    // 提取属性名
    let attr_name = attr_str.between("#[", "(").or(attr_str.between("#[", "]"))
    let attr = ParsedAttribute::new(attr_name.trim())
    
    // 如果有参数
    if attr_str.contains("(") {
      let content = attr_str.between("(", ")")
      let params = self.parse_params(content)
      
      for (key, value) in params {
        attr.set_param(key, value)
      }
    }
    
    attr
  }
  
  /// 解析参数列表
  fn parse_params(self : CodeGenerator, params_str : String) -> Array[(String, AttributeValue)] {
    let mut params : Array[(String, AttributeValue)] = []
    
    // 简单解析：支持 key=value 和 value 两种形式
    let pairs = params_str.split(",")
    for pair in pairs {
      let trimmed = pair.trim()
      
      if trimmed.contains("=") {
        let kv = trimmed.split("=")
        let key = kv[0].trim()
        let value_str = kv[1].trim().replace("\"", "")
        
        // 尝试推断类型
        let value = if value_str == "true" || value_str == "false" {
          BoolVal(value_str == "true")
        } else if value_str.chars().all(fn(c) { c.is_digit() }) {
          IntVal(value_str.to_int())
        } else {
          StringVal(value_str)
        }
        
        params.push((key, value))
      } else {
        // 布尔标志
        params.push((trimmed, BoolVal(true)))
      }
    }
    
    params
  }
  
  /// 生成文件头
  fn generate_header(self : CodeGenerator) -> String {
    "// Auto-generated code by attribute-driven generator\n" +
    "// DO NOT EDIT MANUALLY - Changes will be overwritten\n\n" +
    "///| Generated Entity Implementations\n\n"
  }
  
  /// 为单个实体生成代码
  fn generate_entity(self : CodeGenerator, entity : EntityDef) -> String {
    let mut code : String = ""
    
    code += "// ============================================\n"
    code += "// Entity: " + entity.name + "\n"
    code += "// Table: " + entity.table_name + "\n"
    code += "// ============================================\n\n"
    
    // 1. 生成表信息
    code += self.generate_table_info(entity)
    
    // 2. 生成字段访问器
    code += self.generate_field_accessors(entity)
    
    // 3. 生成 CRUD 操作
    code += self.generate_crud_operations(entity)
    
    // 4. 生成查询方法
    code += self.generate_query_methods(entity)
    
    // 5. 生成验证方法
    code += self.generate_validation_methods(entity)
    
    code += "\n"
  }
  
  /// 生成表信息
  fn generate_table_info(self : CodeGenerator, entity : EntityDef) -> String {
    "pub struct " + entity.name + "TableInfo {\n" +
    "  table_name : String,\n" +
    "  schema : String,\n" +
    "  fields : Array[FieldInfo],\n" +
    "}\n\n" +
    "pub fn " + entity.name.lower_case() + "_table_info() -> " + entity.name + "TableInfo {\n" +
    "  " + entity.name + "TableInfo::{\n" +
    "    table_name: \"" + entity.table_name + "\",\n" +
    "    schema: \"" + entity.schema + "\",\n" +
    "    fields: [\n" +
    self.generate_field_info_list(entity) +
    "    ],\n" +
    "  }\n" +
    "}\n\n"
  }
  
  /// 生成字段信息列表
  fn generate_field_info_list(self : CodeGenerator, entity : EntityDef) -> String {
    let mut list : String = ""
    
    for field in entity.fields {
      let col_name = self.get_column_name(field)
      let nullable = !field.has_attr(ATTR_NOT_NULL)
      
      list += "      FieldInfo::{\n"
      list += "        name: \"" + field.name + "\",\n"
      list += "        column: \"" + col_name + "\",\n"
      list += "        type: \"" + field.field_type + "\",\n"
      list += "        is_primary_key: " + (field.has_attr(ATTR_PRIMARY_KEY)).to_string() + ",\n"
      list += "        is_nullable: " + nullable.to_string() + ",\n"
      list += "        is_auto_increment: " + (field.get_bool_attr(ATTR_AUTO_INCREMENT, false)).to_string() + ",\n"
      list += "      },\n"
    }
    
    list
  }
  
  /// 生成字段访问器
  fn generate_field_accessors(self : CodeGenerator, entity : EntityDef) -> String {
    let mut code : String = ""
    
    for field in entity.fields {
      let method_name = "get_" + field.name
      let col_name = self.get_column_name(field)
      
      code += "pub fn " + method_name + "(entity : " + entity.name + ") -> " + field.field_type + " {\n"
      code += "  entity." + field.name + "\n"
      code += "}\n\n"
      
      code += "pub fn " + method_name + "_column() -> String {\n"
      code += "  \"" + col_name + "\"\n"
      code += "}\n\n"
    }
    
    code
  }
  
  /// 生成 CRUD 操作
  fn generate_crud_operations(self : CodeGenerator, entity : EntityDef) -> String {
    let lower_name = entity.name.lower_case()
    let pk_field = self.find_primary_key(entity)
    
    // Insert
    let insert_code =
      "pub fn insert_" + lower_name + "(entity : " + entity.name + ") -> String {\n" +
      "  let columns = [" + self.generate_column_list(entity) + "]\n" +
      "  let placeholders = columns.map(fn(_) { \"?\" }).join(\", \")\n" +
      "  \"INSERT INTO " + entity.table_name + " (\" + columns.join(\", \") + \") VALUES (\" + placeholders + \")\"\n" +
      "}\n\n"
    
    // Select by ID
    let select_by_id_code =
      "pub fn select_" + lower_name + "_by_id(id : " + pk_field.field_type + ") -> String {\n" +
      "  \"SELECT * FROM " + entity.table_name + " WHERE " + self.get_column_name(pk_field) + " = ?\"\n" +
      "}\n\n"
    
    // Update
    let update_code =
      "pub fn update_" + lower_name + "(entity : " + entity.name + ") -> String {\n" +
      "  let sets = [" + this.generate_set_list(entity) + "]\n" +
      "  \"UPDATE " + entity.table_name + " SET \" + sets.join(\", \") + \" WHERE " + this.get_column_name(pk_field) + " = ?\"\n" +
      "}\n\n"
    
    // Delete
    let delete_code =
      "pub fn delete_" + lower_name + "(id : " + pk_field.field_type + ") -> String {\n" +
      "  \"DELETE FROM " + entity.table_name + " WHERE " + this.get_column_name(pk_field) + " = ?\"\n" +
      "}\n\n"
    
    insert_code + select_by_id_code + update_code + delete_code
  }
  
  /// 生成查询方法
  fn generate_query_methods(self : CodeGenerator, entity : EntityDef) -> String {
    let lower_name = entity.name.lower_case()
    let mut code : String = ""
    
    // Find all
    code += "pub fn find_all_" + lower_name + "() -> String {\n"
    code += "  \"SELECT * FROM " + entity.table_name + "\"\n"
    code += "}\n\n"
    
    // Find by unique fields
    for field in entity.fields {
      if field.has_attr(ATTR_UNIQUE) || field.has_attr(ATTR_PRIMARY_KEY) {
        let method_name = "find_" + lower_name + "_by_" + field.name
        
        code += "pub fn " + method_name + "(value : " + field.field_type + ") -> String {\n"
        code += "  \"SELECT * FROM " + entity.table_name + " WHERE " + this.get_column_name(field) + " = ?\"\n"
        code += "}\n\n"
      }
    }
    
    // Count
    code += "pub fn count_" + lower_name + "() -> String {\n"
    code += "  \"SELECT COUNT(*) FROM " + entity.table_name + "\"\n"
    code += "}\n\n"
    
    // Exists
    code += "pub fn exists_" + lower_name + "(id : Int) -> String {\n"
    code += "  \"SELECT EXISTS(SELECT 1 FROM " + entity.table_name + " WHERE id = ?)\"\n"
    code += "}\n\n"
    
    code
  }
  
  /// 生成验证方法
  fn generate_validation_methods(self : CodeGenerator, entity : EntityDef) -> String {
    let mut code : String = ""
    
    code += "pub fn validate_" + entity.name.lower_case() + "(entity : " + entity.name + ") -> Array[String] {\n"
    code += "  let mut errors : Array[String] = []\n\n"
    
    for field in entity.fields {
      // 非空验证
      if field.has_attr(ATTR_NOT_NULL) {
        code += "  // 验证 " + field.name + " 非空\n"
        code += "  match entity." + field.name + " {\n"
        
        match field.field_type {
          "String" => {
            code += "    \"\" => errors.push(\"" + field.name + " 不能为空\"),\n"
          }
          _ => {
            code += "    null => errors.push(\"" + field.name + " 不能为空\"),\n"
          }
        }
        
        code += "    _ => {}\n"
        code += "  }\n\n"
      }
      
      // 最大长度验证
      if field.has_attr(ATTR_MAX_LENGTH) {
        let max_len = field.get_int_attr(ATTR_MAX_LENGTH, 0)
        if field.field_type == "String" {
          code += "  // 验证 " + field.name + " 最大长度\n"
          code += "  if entity." + field.name + ".length > " + max_len.to_string() + " {\n"
          code += "    errors.push(\"" + field.name + " 长度不能超过 " + max_len.to_string() + "\")\n"
          code += "  }\n\n"
        }
      }
      
      // 范围验证
      if field.has_attr(ATTR_MIN) || field.has_attr(ATTR_MAX) {
        let min_val = field.get_int_attr(ATTR_MIN, 0)
        let max_val = field.get_int_attr(ATTR_MAX, 0)
        
        code += "  // 验证 " + field.name + " 范围\n"
        code += "  if entity." + field.name + " < " + min_val.to_string() + " || "
        code += "entity." + field.name + " > " + max_val.to_string() + " {\n"
        code += "    errors.push(\"" + field.name + " 必须在 " + min_val.to_string() + " 到 " + max_val.to_string() + " 之间\")\n"
        code += "  }\n\n"
      }
      
      // 正则验证
      if field.has_attr(ATTR_PATTERN) {
        let pattern = field.get_string_attr(ATTR_PATTERN, "")
        code += "  // 验证 " + field.name + " 格式\n"
        code += "  if !(entity." + field.name + " =~ re\"" + pattern + "\") {\n"
        code += "    errors.push(\"" + field.name + " 格式不正确\")\n"
        code += "  }\n\n"
      }
    }
    
    code += "  errors\n"
    code += "}\n\n"
    
    code
  }
  
  /// 生成辅助函数
  fn generate_helpers(self : CodeGenerator) -> String {
    "// ============================================\n" +
    "// Helper Functions\n" +
    "// ============================================\n\n" +
    "struct FieldInfo {\n" +
    "  name : String,\n" +
    "  column : String,\n" +
    "  type : String,\n" +
    "  is_primary_key : Bool,\n" +
    "  is_nullable : Bool,\n" +
    "  is_auto_increment : Bool,\n" +
    "}\n\n" +
    "pub fn get_all_tables() -> Array[String] {\n" +
    "  // 返回所有实体的表名\n" +
    "  []\n" +
    "}\n"
  }
  
  /// 辅助方法：获取列名
  fn get_column_name(self : CodeGenerator, field : FieldDef) -> String {
    match field.get_attr(ATTR_COLUMN) {
      Some(attr) => attr.get_string_param("name", field.name),
      None => field.name.to_snake_case(),
    }
  }
  
  /// 辅助方法：查找主键字段
  fn find_primary_key(self : CodeGenerator, entity : EntityDef) -> FieldDef {
    for field in entity.fields {
      if field.has_attr(ATTR_PRIMARY_KEY) {
        return field
      }
    }
    // 默认使用第一个字段
    entity.fields[0]
  }
  
  /// 辅助方法：生成列列表
  fn generate_column_list(self : CodeGenerator, entity : EntityDef) -> String {
    entity.fields
      .filter(fn(f) { !f.has_attr(ATTR_IGNORE) })
      .map(fn(f) { "\"" + this.get_column_name(f) + "\"" })
      .join(", ")
  }
  
  /// 辅助方法：生成 SET 子句
  fn generate_set_list(self : CodeGenerator, entity : EntityDef) -> String {
    entity.fields
      .filter(fn(f) { !f.has_attr(ATTR_IGNORE) && !f.has_attr(ATTR_PRIMARY_KEY) })
      .map(fn(f) { this.get_column_name(f) + " = ?" })
      .join(", ")
  }
}

// 数据结构定义

struct EntityDef {
  mut name : String
  table_name : String
  schema : String
  comment : String
  mut fields : Array[FieldDef]
}

impl EntityDef with {
  pub fn new(table_name : String, schema : String, comment : String) -> EntityDef {
    EntityDef::{
      name: "",
      table_name: table_name,
      schema: schema,
      comment: comment,
      fields: [],
    }
  }
}

struct FieldDef {
  name : String
  field_type : String
  attributes : Array[ParsedAttribute]
}

impl FieldDef with {
  pub fn new(name : String, field_type : String, attributes : Array[ParsedAttribute]) -> FieldDef {
    FieldDef::{
      name: name,
      field_type: field_type,
      attributes: attributes,
    }
  }
  
  pub fn has_attr(self : FieldDef, attr_name : String) -> Bool {
    self.attributes.any(fn(a) { a.attribute_name == attr_name })
  }
  
  pub fn get_attr(self : FieldDef, attr_name : String) -> Option[ParsedAttribute] {
    self.attributes.find(fn(a) { a.attribute_name == attr_name })
  }
  
  pub fn get_bool_attr(self : FieldDef, attr_name : String, default : bool) -> bool {
    match self.get_attr(attr_name) {
      Some(attr) => attr.get_bool_param("", default),
      None => default,
    }
  }
  
  pub fn get_int_attr(self : FieldDef, attr_name : String, default : Int) -> Int {
    match self.get_attr(attr_name) {
      Some(attr) => attr.get_int_param("", default),
      None => default,
    }
  }
  
  pub fn get_string_attr(self : FieldDef, attr_name : String, default : String) -> String {
    match self.get_attr(attr_name) {
      Some(attr) => attr.get_string_param("", default),
      None => default,
    }
  }
}

// 字符串扩展方法（伪代码，展示设计意图）
/*
impl String with {
  pub fn between(self : String, start : String, end : String) -> String { ... }
  pub fn lower_case(self : String) -> String { ... }
  pub fn to_snake_case(self : String) -> String { ... }
}
*/
```

### src/engine/engine.mbt - 核心引擎

```moonbit
///| Core Engine - 属性驱动框架核心引擎

struct Engine {
  entities : Map[String, EntityMetadata]
  generators : Map[String, CodeGeneratorFn]
  validators : Map[String, ValidatorFn]
}

typealias CodeGeneratorFn = (EntityMetadata) -> String
typealias ValidatorFn = (Dynamic) -> Result[Unit, String]

struct EntityMetadata {
  name : String
  table_name : String
  schema : String
  fields : Array[FieldMetadata]
  relations : Array[RelationMetadata]
  indexes : Array[IndexMetadata]
}

struct FieldMetadata {
  name : String
  column_name : String
  field_type : String
  is_primary_key : Bool
  is_nullable : Bool
  is_unique : Bool
  has_default : Bool
  default_value : Option[String]
  constraints : Array[ConstraintMetadata]
}

struct RelationMetadata {
  relation_type : RelationType
  field_name : String
  target_entity : String
  target_field : String
  cascade_options : CascadeOptions
  lazy_loading : Bool
}

enum RelationType {
  OneToOne
  OneToMany
  ManyToOne
  ManyToMany
}

struct CascadeOptions {
  on_delete : CascadeAction
  on_update : CascadeAction
}

enum CascadeAction {
  NoAction
  Restrict
  Cascade
  SetNull
  SetDefault
}

struct IndexMetadata {
  index_name : String
  columns : Array[String]
  is_unique : Bool
  index_type : IndexType
}

enum IndexType {
  BTree
  Hash
  Gin
  Gist
}

struct ConstraintMetadata {
  constraint_type : ConstraintType
  value : String
}

enum ConstraintType {
  MaxLength(Int)
  Min(Int)
  Max(Int)
  Pattern(String)
  NotNull
  Custom(String)
}

impl Engine with {
  pub fn new() -> Engine {
    Engine::{
      entities: Map::new(),
      generators: Map::new(),
      validators: Map::new(),
    }
  }
  
  /// 注册实体
  pub fn register_entity(self : Engine, metadata : EntityMetadata) {
    self.entities.insert(metadata.name, metadata)
  }
  
  /// 注册代码生成器
  pub fn register_generator(self : Engine, entity_type : String, generator : CodeGeneratorFn) {
    self.generators.insert(entity_type, generator)
  }
  
  /// 注册验证器
  pub fn register_validator(self : Engine, entity_type : String, validator : ValidatorFn) {
    self.validators.insert(entity_type, validator)
  }
  
  /// 生成所有实体的代码
  pub fn generate_all(self : Engine) -> Map[String, String] {
    let mut results : Map[String, String] = Map::new()
    
    for (entity_name, metadata) in self.entities {
      match self.generators.get(entity_name) {
        Some(generator) => {
          let code = generator(metadata)
          results.insert(entity_name, code)
        }
        None => {
          // 使用默认生成器
          let code = self.default_generate(metadata)
          results.insert(entity_name, code)
        }
      }
    }
    
    results
  }
  
  /// 验证实体实例
  pub fn validate(self : Engine, entity_name : String, instance : Dynamic) -> Result[Unit, String] {
    match self.validators.get(entity_name) {
      Some(validator) => validator(instance),
      None => Ok(()),
    }
  }
  
  /// 生成 CREATE TABLE SQL
  pub fn generate_create_table_sql(self : Engine, entity_name : String) -> Result[String, String] {
    match self.entities.get(entity_name) {
      Some(metadata) => Ok(self.build_create_table_sql(metadata)),
      None => Err("未找到实体: " + entity_name),
    }
  }
  
  /// 默认代码生成
  fn default_generate(self : Engine, metadata : EntityMetadata) -> String {
    let mut code : String = ""
    
    // 生成结构体实现
    code += "impl " + metadata.name + " with {\n"
    
    // 生成 to_map 方法
    code += "  pub fn to_map(self : " + metadata.name + ") -> Map[String, Dynamic] {\n"
    code += "    let mut map : Map[String, Dynamic] = Map::new()\n"
    
    for field in metadata.fields {
      code += "    map.insert(\"" + field.column_name + "\", self." + field.name + ")\n"
    }
    
    code += "    map\n"
    code += "  }\n\n"
    
    // 生成 from_map 方法
    code += "  pub fn from_map(map : Map[String, Dynamic]) -> " + metadata.name + " {\n"
    code += "    " + metadata.name + "::{\n"
    
    for field in metadata.fields {
      code += "      " + field.name + ": "
      code += match field.field_type {
        "String" => "map.get(\"" + field.column_name + "\").unwrap_or(\"\").to_string()",
        "Int" => "map.get(\"" + field.column_name + "\").unwrap_or(0).to_int()",
        "Bool" => "map.get(\"" + field.column_name + "\").unwrap_or(false)",
        "Double" => "map.get(\"" + field.column_name + "\").unwrap_or(0.0).to_double()",
        _ => "map.get(\"" + field.column_name + "\")",
      }
      code += ",\n"
    }
    
    code += "    }\n"
    code += "  }\n"
    code += "}\n"
    
    code
  }
  
  /// 构建 CREATE TABLE SQL
  fn build_create_table_sql(self : Engine, metadata : EntityMetadata) -> String {
    let mut sql : String = "CREATE TABLE IF NOT EXISTS "
    sql += metadata.schema + "." + metadata.table_name + " (\n"
    
    let mut columns : Array[String] = []
    
    for field in metadata.fields {
      let mut col_def : String = "  " + field.column_name + " "
      col_def += self.map_type_to_sql(field.field_type)
      
      if field.is_primary_key {
        col_def += " PRIMARY KEY"
        if field.has_default {
          col_def += " AUTOINCREMENT"
        }
      }
      
      if !field.is_nullable {
        col_def += " NOT NULL"
      }
      
      if field.is_unique {
        col_def += " UNIQUE"
      }
      
      if field.has_default {
        match field.default_value {
          Some(default) => col_def += " DEFAULT " + default,
          None => {}
        }
      }
      
      columns.push(col_def)
    }
    
    sql += columns.join(",\n")
    sql += "\n);\n"
    
    // 添加索引
    for index in metadata.indexes {
      sql += self.create_index_sql(metadata, index)
    }
    
    sql
  }
  
  /// 类型映射到 SQL
  fn map_type_to_sql(self : Engine, moonbit_type : String) -> String {
    match moonbit_type {
      "Int" => "INTEGER",
      "Int64" => "BIGINT",
      "Double" => "DOUBLE PRECISION",
      "String" => "TEXT",
      "Bool" => "BOOLEAN",
      "DateTime" => "TIMESTAMP",
      "Bytes" => "BLOB",
      _ => "TEXT",
    }
  }
  
  /// 创建索引 SQL
  fn create_index_sql(self : Engine, metadata : EntityMetadata, index : IndexMetadata) -> String {
    let mut sql : String = "CREATE "
    
    if index.is_unique { sql += "UNIQUE " }
    
    sql += "INDEX " + index.index_name + " ON "
    sql += metadata.schema + "." + metadata.table_name + " ("
    sql += index.columns.join(", ")
    sql += ");\n"
    
    sql
  }
}
```

### src/dialect/dialect.mbt - 方言适配

```moonbit
///| SQL Dialect Adapter - SQL 方言适配层

enum DialectType {
  SQLite
  PostgreSQL
  MySQL
  SQLServer
  Oracle
}

trait Dialect {
  quote_identifier(identifier : String) -> String
  quote_value(value : Dynamic) -> String
  limit_offset(limit : Int, offset : Int) -> String
  upsert_sql(table : String, columns : Array[String], conflict_columns : Array[String]) -> String
  auto_increment() -> String
  boolean_type() -> String
  supports_returning() -> Bool
}

struct SQLiteDialect {}

impl SQLiteDialect with Dialect {
  pub fn quote_identifier(self : SQLiteDialect, identifier : String) -> String {
    "\"" + identifier + "\""
  }
  
  pub fn quote_value(self : SQLiteDialect, value : Dynamic) -> String {
    match value {
      String(s) => "'" + s.replace("'", "''") + "'"
      Int(i) => i.to_string()
      Bool(b) => if b { "1" } else { "0" }
      Double(d) => d.to_string()
      Null => "NULL"
      _ => "''",
    }
  }
  
  pub fn limit_offset(self : SQLiteDialect, limit : Int, offset : Int) -> String {
    " LIMIT " + limit.to_string() + " OFFSET " + offset.to_string()
  }
  
  pub fn upsert_sql(self : SQLiteDialect, table : String, columns : Array[String], conflict_columns : Array[String]) -> String {
    let quoted_cols = columns.map(fn(c) { "\"" + c + "\"" })
    let placeholders = columns.map(fn(_) { "?" })
    let updates = columns.filter(fn(c) { !conflict_columns.contains(c) })
                          .map(fn(c) { "\"" + c + "\" = excluded.\"" + c + "\"" })
    
    "INSERT OR REPLACE INTO \"" + table + "\" (" + quoted_cols.join(", ") + 
    ") VALUES (" + placeholders.join(", ") + ")"
  }
  
  pub fn auto_increment(self : SQLiteDialect) -> String {
    "INTEGER PRIMARY KEY AUTOINCREMENT"
  }
  
  pub fn boolean_type(self : SQLiteDialect) -> String {
    "INTEGER"
  }
  
  pub fn supports_returning(self : SQLiteDialect) -> Bool {
    false
  }
}

struct PostgreSQLDialect {}

impl PostgreSQLDialect with Dialect {
  pub fn quote_identifier(self : PostgreSQLDialect, identifier : String) -> String {
    "\"" + identifier + "\""
  }
  
  pub fn quote_value(self : PostgreSQLDialect, value : Dynamic) -> String {
    match value {
      String(s) => "'" + s.replace("'", "''") + "'"
      Int(i) => i.to_string()
      Bool(b) => if b { "TRUE" } else { "FALSE" }
      Double(d) => d.to_string()
      Null => "NULL"
      _ => "''",
    }
  }
  
  pub fn limit_offset(self : PostgreSQLDialect, limit : Int, offset : Int) -> String {
    " LIMIT " + limit.to_string() + " OFFSET " + offset.to_string()
  }
  
  pub fn upsert_sql(self : PostgreSQLDialect, table : String, columns : Array[String], conflict_columns : Array[String]) -> String {
    let quoted_cols = columns.map(fn(c) { "\"" + c + "\"" })
    let placeholders = columns.map(fn(_) { "$" + (_index + 1).to_string() })
    let updates = columns.filter(fn(c) { !conflict_columns.contains(c) })
                          .map(fn(c) { "\"" + c + "\" = EXCLUDED.\"" + c + "\"" })
    
    "INSERT INTO \"" + table + "\" (" + quoted_cols.join(", ") + 
    ") VALUES (" + placeholders.join(", ") + ")" +
    " ON CONFLICT (" + conflict_columns.map(fn(c) { "\"" + c + "\"" }).join(", ") + ") DO UPDATE SET " + 
    updates.join(", ")
  }
  
  pub fn auto_increment(self : PostgreSQLDialect) -> String {
    "SERIAL"
  }
  
  pub fn boolean_type(self : PostgreSQLDialect) -> String {
    "BOOLEAN"
  }
  
  pub fn supports_returning(self : PostgreSQLDialect) -> Bool {
    true
  }
}

struct MySQLDialect {}

impl MySQLDialect with Dialect {
  pub fn quote_identifier(self : MySQLDialect, identifier : String) -> String {
    "`" + identifier + "`"
  }
  
  pub fn quote_value(self : MySQLDialect, value : Dynamic) -> String {
    match value {
      String(s) => "'" + s.replace("'", "\\'") + "'"
      Int(i) => i.to_string()
      Bool(b) => if b { "TRUE" } else { "FALSE" }
      Double(d) => d.to_string()
      Null => "NULL"
      _ => "''",
    }
  }
  
  pub fn limit_offset(self : MySQLDialect, limit : Int, offset : Int) -> String {
    " LIMIT " + offset.to_string() + ", " + limit.to_string()
  }
  
  pub fn upsert_sql(self : MySQLDialect, table : String, columns : Array[String], conflict_columns : Array[String]) -> String {
    let quoted_cols = columns.map(fn(c) { "`" + c + "`" })
    let placeholders = columns.map(fn(_) { "?" })
    let updates = columns.filter(fn(c) { !conflict_columns.contains(c) })
                          .map(fn(c) { "`" + c + "` = VALUES(`" + c + "`)" })
    
    "INSERT INTO `" + table + "` (" + quoted_cols.join(", ") + 
    ") VALUES (" + placeholders.join(", ") + ")" +
    " ON DUPLICATE KEY UPDATE " + updates.join(", ")
  }
  
  pub fn auto_increment(self : MySQLDialect) -> String {
    "INT AUTO_INCREMENT"
  }
  
  pub fn boolean_type(self : MySQLDialect) -> String {
    "TINYINT(1)"
  }
  
  pub fn supports_returning(self : MySQLDialect) -> Bool {
    false
  }
}

/// 方言工厂
pub fn create_dialect(dialect_type : DialectType) -> Dialect {
  match dialect_type {
    SQLite => SQLiteDialect::{} as Dialect,
    PostgreSQL => PostgreSQLDialect::{} as Dialect,
    MySQL => MySQLDialect::{} as Dialect,
    _ => SQLiteDialect::{} as Dialect,
  }
}
```

### src/main/api.mbt - 公开 API

```moonbit
///| Public API - 属性驱动框架公开接口

// 便捷宏（伪代码，展示设计意图）
/*
macro_rules! entity {
  ($($tt:tt)*) => {
    // 解析属性并注册实体
  }
}
*/

/// 初始化引擎
pub fn init_engine() -> Engine {
  let engine = Engine::new()
  
  // 注册默认生成器
  engine.register_generator("default", default_generator)
  
  // 注册默认验证器
  engine.register_validator("default", default_validator)
  
  engine
}

/// 从源文件生成代码
pub fn generate_from_file(file_path : String) -> Result[String, String] {
  // 读取源文件
  let source_code = read_file(file_path)
  
  // 创建生成器
  let generator = CodeGenerator::new(source_code)
  
  // 生成代码
  Ok(generator.generate())
}

/// 生成到文件
pub fn generate_to_file(source_path : String, output_path : String) -> Result[Unit, String] {
  let code = generate_from_file(source_path)?
  write_file(output_path, code)
  Ok(())
}

/// 批量生成
pub fn generate_batch(source_dir : String, output_dir : String) -> Result[Unit, String] {
  let files = list_files(source_dir, "*.mbt")
  
  for file in files {
    let file_name = file.file_name_stem()
    let output_path = output_dir + "/" + file_name + ".g.mbt"
    
    match generate_to_file(file, output_path) {
      Ok(_) => println("✓ 已生成: " + output_path),
      Err(e) => println("✗ 生成失败 " + file + ": " + e),
    }
  }
  
  Ok(())
}

/// 获取实体元数据
pub fn get_entity_metadata(engine : Engine, entity_name : String) -> Option[EntityMetadata] {
  engine.entities.get(entity_name)
}

/// 生成迁移 SQL
pub fn generate_migration_sql(engine : Engine, dialect_type : DialectType) -> Result[String, String] {
  let dialect = create_dialect(dialect_type)
  let mut sql : String = "-- Auto-generated migration\n\n"
  
  for (entity_name, metadata) in engine.entities {
    sql += "-- Table: " + metadata.table_name + "\n"
    sql += engine.generate_create_table_sql(entity_name)? + "\n"
  }
  
  Ok(sql)
}

/// 验证实体
pub fn validate_entity(engine : Engine, entity_name : String, instance : Dynamic) -> Result[Unit, String] {
  engine.validate(entity_name, instance)
}

// 默认生成器实现
fn default_generator(metadata : EntityMetadata) -> String {
  let mut code : String = ""
  
  code += "// Generated implementation for " + metadata.name + "\n"
  code += "\n"
  
  // 生成 CRUD trait 实现
  code += "impl " + metadata.name + " with Repository {\n"
  
  // Save 方法
  code += "  pub fn save(self : " + metadata.name + ") -> Result[" + metadata.name + ", String] {\n"
  code += "    // 根据 ID 存在决定 INSERT 或 UPDATE\n"
  code += "    repository::save(self)\n"
  code += "  }\n\n"
  
  // Delete 方法
  code += "  pub fn delete(self : " + metadata.name + ") -> Result[Unit, String] {\n"
  code += "    repository::delete(self.id)\n"
  code += "  }\n\n"
  
  // Find by ID
  code += "  pub fn find_by_id(id : Int) -> Option[" + metadata.name + "] {\n"
  code += "    repository::find_by_id::<" + metadata.name + ">(id)\n"
  code += "  }\n"
  
  code += "}\n"
  
  code
}

// 默认验证器实现
fn default_validator(instance : Dynamic) -> Result[Unit, String] {
  // 通用验证逻辑
  Ok(())
}
```

### cmd/generator/main.mbt - 代码生成命令入口

```moonbit
///| Code Generator CLI - 代码生成命令行工具

fn main {
  let args = Sys::args()
  
  match args.length {
    0 | 1 => print_usage()
    _ => {
      let command = args[1]
      match command {
        "generate" | "gen" => handle_generate(args)
        "watch" => handle_watch(args)
        "init" => handle_init(args)
        "validate" => handle_validate(args)
        "migrate" => handle_migrate(args)
        "help" | "-h" | "--help" => print_usage()
        "version" | "-v" | "--version" => print_version()
        _ => {
          println("未知命令: " + command)
          print_usage()
        }
      }
    }
  }
}

fn print_usage() {
  println("╔═════════════════════════════════════════════╗")
  println("║   🌙 Attribute-Driven Code Generator CLI    ║")
  println("╚═════════════════════════════════════════════╝")
  println()
  println("用法: gen-tool <command> [options]")
  println()
  println("命令:")
  println("  generate, gen   生成代码")
  println("  watch           监视文件变化并自动重新生成")
  println("  init            初始化项目配置")
  println("  validate        验证实体定义")
  println("  migrate         生成数据库迁移 SQL")
  println("  help, -h        显示帮助信息")
  println("  version, -v     显示版本号")
  println()
  println("选项:")
  println("  --source, -s    源文件或目录路径")
  println("  --output, -o    输出目录路径")
  println("  --dialect, -d   SQL 方言 (sqlite/postgresql/mysql)")
  println("  --watch, -w     监视模式")
  println("  --verbose, -v   详细输出")
  println()
  println("示例:")
  println("  gen-tool generate -s ./entities -o ./generated")
  println("  gen-tool watch -s ./src -o ./gen --dialect postgresql")
  println("  gen-tool migrate --dialect sqlite > migration.sql")
}

fn print_version() {
  println("attribute-driven-generator v2.0.0 (MoonBit)")
}

fn handle_generate(args : Array[String]) {
  let source = get_option(args, "--source", "-s", "./src")
  let output = get_option(args, "--output", "-o", "./generated")
  let verbose = has_flag(args, "--verbose", "-v")
  
  if verbose {
    println("📂 源目录: " + source)
    println("📁 输出目录: " + output)
    println()
  }
  
  match api::generate_batch(source, output) {
    Ok(_) => {
      println("✅ 代码生成完成!")
      println("   输出目录: " + output)
    }
    Err(e) => {
      println("❌ 生成失败: " + e)
      exit(1)
    }
  }
}

fn handle_watch(args : Array[String]) {
  let source = get_option(args, "--source", "-s", "./src")
  let output = get_option(args, "--output", "-o", "./generated")
  
  println("👁️  监视模式启动...")
  println("   监视目录: " + source)
  println("   输出目录: " + output)
  println("   按 Ctrl+C 停止")
  println()
  
  // 简化的监视循环（实际应使用文件系统监视 API）
  let mut running = true
  
  while running {
    // 首次生成
    match api::generate_batch(source, output) {
      Ok(_) => println("🔄 " + current_time() + " - 代码已更新"),
      Err(e) => println("⚠️  " + e),
    }
    
    // 等待一段时间再检查（简化实现）
    sleep_ms(2000)
  }
}

fn handle_init(_args : Array[String]) {
  println("🚀 初始化项目配置...")
  
  // 创建目录结构
  ensure_dir("./src/entities")
  ensure_dir("./src/generated")
  ensure_dir("./migrations")
  
  // 创建配置文件
  write_file("gen-config.toml", """# Generator Configuration
[source]
path = "./src/entities"
pattern = "*.mbt"

[output]
path = "./src/generated"
suffix = ".g.mbt"

[database]
dialect = "sqlite"
migration_path = "./migrations"

[options]
verbose = false
watch = false
""")
  
  println("✅ 项目初始化完成!")
  println("   已创建:")
  println("   - ./src/entities/     (放置实体定义)")
  println("   - ./src/generated/    (生成的代码)")
  println("   - ./migrations/       (数据库迁移)")
  println("   - gen-config.toml     (配置文件)")
}

fn handle_validate(args : Array[String]) {
  let source = get_option(args, "--source", "-s", "./src")
  
  println("🔍 验证实体定义...")
  println()
  
  let files = list_files(source, "*.mbt")
  let mut total_errors = 0
  
  for file in files {
    println("📄 检查: " + file)
    
    // 读取并解析文件
    let source_code = read_file(file)
    let generator = CodeGenerator::new(source_code)
    let entities = generator.parse_entities()
    
    for entity in entities {
      // 验证实体
      let errors = validate_entity_structure(entity)
      
      if errors.length > 0 {
        total_errors += errors.length
        for error in errors {
          println("  ❌ " + error)
        }
      } else {
        println("  ✅ 实体 " + entity.name + " 验证通过")
      }
    }
  }
  
  println()
  if total_errors == 0 {
    println("✅ 所有实体验证通过!")
  } else {
    println("❌ 发现 " + total_errors.to_string() + " 个错误")
    exit(1)
  }
}

fn handle_migrate(args : Array[String]) {
  let dialect_str = get_option(args, "--dialect", "-d", "sqlite")
  
  let dialect_type = match dialect_str {
    "postgresql" => PostgreSQL,
    "mysql" => MySQL,
    "sqlite" | _ => SQLite,
  }
  
  println("🗃️  生成迁移 SQL (" + dialect_str + ")...")
  println()
  
  let engine = init_engine()
  
  match generate_migration_sql(engine, dialect_type) {
    Ok(sql) => {
      println(sql)
    }
    Err(e) => {
      println("❌ 生成失败: " + e)
      exit(1)
    }
  }
}

// 命令行参数解析辅助函数
fn get_option(args : Array[String], long : String, short : String, default : String) -> String {
  for i in 1..args.length {
    if args[i] == long || args[i] == short {
      if i + 1 < args.length {
        return args[i + 1]
      }
    }
  }
  default
}

fn has_flag(args : Array[String], long : String, short : String) -> Bool {
  args.any(fn(arg) { arg == long || arg == short })
}

fn validate_entity_structure(entity : EntityDef) -> Array[String] {
  let mut errors : Array[String] = []
  
  // 检查实体名称
  if entity.name.length == 0 {
    errors.push("实体缺少名称")
  }
  
  // 检查表名
  if entity.table_name.length == 0 {
    errors.push("实体 " + entity.name + " 缺少表名 (使用 #[entity(table_name=\"...\")] 指定)")
  }
  
  // 检查字段
  if entity.fields.length == 0 {
    errors.push("实体 " + entity.name + " 没有字段定义")
  }
  
  // 检查主键
  let has_pk = entity.fields.any(fn(f) { f.has_attr(ATTR_PRIMARY_KEY) })
  if !has_pk {
    errors.push("实体 " + entity.name + " 缺少主键 (使用 #[primary_key] 指定)")
  }
  
  // 检查外键引用
  for field in entity.fields {
    if field.has_attr(ATTR_FOREIGN_KEY) {
      let ref_table = field.get_string_attr(ATTR_FOREIGN_KEY, "")
      if ref_table.length == 0 {
        errors.push("字段 " + field.name + " 的外键缺少目标表")
      }
    }
  }
  
  errors
}
```

### example/entity.mbt - 用户定义的实体示例

```moonbit
///| Example Entity Definitions - 用户实体定义示例

// ============================================
// 用户实体
// ============================================
#[entity(table_name="users", comment="用户表")]
struct User {
  #[primary_key(auto_increment=true)]
  id : Int
  
  #[column(name="username"), not_null, max_length(50), unique]
  username : String
  
  #[column(name="email_address"), not_null, pattern("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")]
  email : String
  
  #[column(name="password_hash"), not_null, max_length(255)]
  password_hash : String
  
  #[column(name="display_name"), max_length(100)]
  display_name : String
  
  #[default(false)]
  is_active : Bool
  
  #[column(name="created_at"), not_null]
  created_at : DateTime
  
  #[column(name="updated_at")]
  updated_at : DateTime
}

// ============================================
// 角色实体
// ============================================
#[entity(table_name="roles")]
struct Role {
  #[primary_key(auto_increment=true)]
  id : Int
  
  #[not_null, max_length(50), unique]
  name : String
  
  #[max_length(200)]
  description : String
  
  #[default(true)]
  is_system : Bool
}

// ============================================
// 文章实体
// ============================================
#[entity(table_name="posts", schema="content")]
struct Post {
  #[primary_key(auto_increment=true)]
  id : Int
  
  #[foreign_key("users.id"), not_null]
  author_id : Int
  
  #[not_null, max_length(200)]
  #[column(name="post_content"), not_null]
  content : String
  
  #[default("draft")]
  status : String
  
  #[column(name="view_count"), default(0), min(0)]
  view_count : Int
  
  #[not_null]
  published_at : DateTime
  
  #[column(name="updated_at")]
  updated_at : DateTime
  
  #[many_to_one("users.id"), cascade(delete=Cascade, update=Restrict)]
  updater_id : Int
  
  #[ignore]
  computed_field : String
}

// ============================================
// 评论实体（演示关联）
// ============================================
#[entity(table_name="comments")]
struct Comment {
  #[primary_key(auto_increment=true)]
  id : Int
  
  #[foreign_key("posts.id"), not_null]
  post_id : Int
  
  #[foreign_key("users.id"), not_null]
  user_id : Int
  
  #[not_null, max_length(2000)]
  content : String
  
  #[default(false)]
  is_approved : Bool
  
  #[not_null]
  created_at : DateTime
}

// ============================================
// 标签实体（演示多对多关联）
// ============================================
#[entity(table_name="tags")]
struct Tag {
  #[primary_key(auto_increment=true)]
  id : Int
  
  #[not_null, max_length(50), unique]
  name : String
  
  #[column(name="slug"), max_length(50), unique]
  slug : String
}

// ============================================
// 文章-标签关联表（中间表）
// ============================================
#[entity(table_name="post_tags")]
struct PostTag {
  #[primary_key]
  id : Int
  
  #[foreign_key("posts.id"), not_null, primary_key]
  post_id : Int
  
  #[foreign_key("tags.id"), not_null, primary_key]
  tag_id : Int
  
  #[column(name="sort_order"), default(0)]
  sort_order : Int
}
```

#### example/entity.g.mbt - 自动生成的代码示例

```moonbit
///| Generated Code - 由属性驱动代码生成器自动生成
///
/// ⚠️ 警告: 此文件由代码生成器自动生成
/// ❌ 请勿手动编辑 - 所有更改将被覆盖!
///
/// 生成时间: 2026-05-17 10:30:00
/// 生成器版本: v2.0.0
/// 源文件: example/entity.mbt

// ============================================
// User 实体生成代码
// ============================================

// 表信息
pub struct UserTableInfo {
  table_name : String,
  schema : String,
  fields : Array[FieldInfo],
}

pub fn user_table_info() -> UserTableInfo {
  UserTableInfo::{
    table_name: "users",
    schema: "public",
    fields: [
      FieldInfo::{
        name: "id",
        column: "id",
        type: "Int",
        is_primary_key: true,
        is_nullable: false,
        is_auto_increment: true,
      },
      FieldInfo::{
        name: "username",
        column: "username",
        type: "String",
        is_primary_key: false,
        is_nullable: false,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "email",
        column: "email_address",
        type: "String",
        is_primary_key: false,
        is_nullable: false,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "password_hash",
        column: "password_hash",
        type: "String",
        is_primary_key: false,
        is_nullable: false,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "display_name",
        column: "display_name",
        type: "String",
        is_primary_key: false,
        is_nullable: true,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "is_active",
        column: "is_active",
        type: "Bool",
        is_primary_key: false,
        is_nullable: true,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "created_at",
        column: "created_at",
        type: "DateTime",
        is_primary_key: false,
        is_nullable: false,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "updated_at",
        column: "updated_at",
        type: "DateTime",
        is_primary_key: false,
        is_nullable: true,
        is_auto_increment: false,
      },
    ],
  }
}

// 字段访问器
pub fn get_id(user : User) -> Int {
  user.id
}

pub fn get_id_column() -> String {
  "id"
}

pub fn get_username(user : User) -> String {
  user.username
}

pub fn get_username_column() -> String {
  "username"
}

pub fn get_email(user : User) -> String {
  user.email
}

pub fn get_email_column() -> String {
  "email_address"
}

// ... 其他字段访问器 ...

// CRUD 操作
pub fn insert_user(user : User) -> String {
  let columns = ["id", "username", "email_address", "password_hash", "display_name", "is_active", "created_at", "updated_at"]
  let placeholders = columns.map(fn(_) { "?" }).join(", ")
  "INSERT INTO users (" + columns.join(", ") + ") VALUES (" + placeholders + ")"
}

pub fn select_user_by_id(id : Int) -> String {
  "SELECT * FROM users WHERE id = ?"
}

pub fn update_user(user : User) -> String {
  let sets = ["username = ?", "email_address = ?", "password_hash = ?", "display_name = ?", "is_active = ?", "updated_at = ?"]
  "UPDATE users SET " + sets.join(", ") + " WHERE id = ?"
}

pub fn delete_user(id : Int) -> String {
  "DELETE FROM users WHERE id = ?"
}

// 查询方法
pub fn find_all_users() -> String {
  "SELECT * FROM users"
}

pub fn find_user_by_username(username : String) -> String {
  "SELECT * FROM users WHERE username = ?"
}

pub fn find_user_by_email(email : String) -> String {
  "SELECT * FROM users WHERE email_address = ?"
}

pub fn count_users() -> String {
  "SELECT COUNT(*) FROM users"
}

pub fn exists_user(id : Int) -> String {
  "SELECT EXISTS(SELECT 1 FROM users WHERE id = ?)"
}

// 验证方法
pub fn validate_user(user : User) -> Array[String] {
  let mut errors : Array[String] = []
  
  // 验证 username 非空
  match user.username {
    "" => errors.push("username 不能为空"),
    _ => {}
  }
  
  // 验证 username 最大长度
  if user.username.length > 50 {
    errors.push("username 长度不能超过 50")
  }
  
  // 验证 email 非空
  match user.email {
    "" => errors.push("email 不能为空"),
    _ => {}
  }
  
  // 验证 email 格式
  if !(user.email =~ re"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$") {
    errors.push("email 格式不正确")
  }
  
  // 验证 password_hash 非空
  match user.password_hash {
    "" => errors.push("password_hash 不能为空"),
    _ => {}
  }
  
  // 验证 password_hash 最大长度
  if user.password_hash.length > 255 {
    errors.push("password_hash 长度不能超过 255")
  }
  
  // 验证 display_name 最大长度
  if user.display_name.length > 100 {
    errors.push("display_name 长度不能超过 100")
  }
  
  errors
}

// ============================================
// Role 实体生成代码
// ============================================

pub struct RoleTableInfo {
  table_name : String,
  schema : String,
  fields : Array[FieldInfo],
}

pub fn role_table_info() -> RoleTableInfo {
  RoleTableInfo::{
    table_name: "roles",
    schema: "public",
    fields: [
      FieldInfo::{
        name: "id",
        column: "id",
        type: "Int",
        is_primary_key: true,
        is_nullable: false,
        is_auto_increment: true,
      },
      FieldInfo::{
        name: "name",
        column: "name",
        type: "String",
        is_primary_key: false,
        is_nullable: false,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "description",
        column: "description",
        type: "String",
        is_primary_key: false,
        is_nullable: true,
        is_auto_increment: false,
      },
      FieldInfo::{
        name: "is_system",
        column: "is_system",
        type: "Bool",
        is_primary_key: false,
        is_nullable: true,
        is_auto_increment: false,
      },
    ],
  }
}

pub fn insert_role(role : Role) -> String {
  "INSERT INTO roles (id, name, description, is_system) VALUES (?, ?, ?, ?)"
}

pub fn select_role_by_id(id : Int) -> String {
  "SELECT * FROM roles WHERE id = ?"
}

pub fn update_role(role : Role) -> String {
  "UPDATE roles SET name = ?, description = ?, is_system = ? WHERE id = ?"
}

pub fn delete_role(id : Int) -> String {
  "DELETE FROM roles WHERE id = ?"
}

pub fn find_all_roles() -> String {
  "SELECT * FROM roles"
}

pub fn find_role_by_name(name : String) -> String {
  "SELECT * FROM roles WHERE name = ?"
}

pub fn count_roles() -> String {
  "SELECT COUNT(*) FROM roles"
}

pub fn validate_role(role : Role) -> Array[String] {
  let mut errors : Array[String] = []
  
  // 验证 name 非空
  match role.name {
    "" => errors.push("name 不能为空"),
    _ => {}
  }
  
  // 验证 name 最大长度
  if role.name.length > 50 {
    errors.push("name 长度不能超过 50")
  }
  
  // 验证 description 最大长度
  if role.description.length > 200 {
    errors.push("description 长度不能超过 200")
  }
  
  errors
}

// ============================================
// Post 实体生成代码（包含关联）
// ============================================

pub struct PostTableInfo {
  table_name : String,
  schema : String,
  fields : Array[FieldInfo],
  relations : Array[RelationInfo],
}

pub fn post_table_info() -> PostTableInfo {
  PostTableInfo::{
    table_name: "posts",
    schema: "content",
    fields: [
      FieldInfo::{
        name: "id",
        column: "id",
        type: "Int",
        is_primary_key: true,
        is_nullable: false,
        is_auto_increment: true,
      },
      FieldInfo::{
        name: "author_id",
        column: "author_id",
        type: "Int",
        is_primary_key: false,
        is_nullable: false,
        is_auto_increment: false,
      },
      // ... 其他字段 ...
    ],
    relations: [
      RelationInfo::{
        relation_type: ManyToOne,
        field_name: "author",
        target_entity: "User",
        target_field: "id",
        foreign_key_column: "author_id",
      },
      RelationInfo::{
        relation_type: ManyToOne,
        field_name: "updater",
        target_entity: "User",
        target_field: "id",
        foreign_key_column: "updater_id",
      },
    ],
  }
}

// 关联查询方法
pub fn find_post_with_author(post_id : Int) -> String {
  "SELECT p.*, u.username as author_username, u.display_name as author_display_name " +
  "FROM posts p LEFT JOIN users u ON p.author_id = u.id WHERE p.id = ?"
}

pub fn find_posts_by_author(author_id : Int) -> String {
  "SELECT * FROM posts WHERE author_id = ? ORDER BY created_at DESC"
}

// ... 其他 Post 相关方法 ...

// ============================================
// 辅助函数
// ============================================

struct FieldInfo {
  name : String,
  column : String,
  type : String,
  is_primary_key : Bool,
  is_nullable : Bool,
  is_auto_increment : Bool,
}

struct RelationInfo {
  relation_type : RelationType,
  field_name : String,
  target_entity : String,
  target_field : String,
  foreign_key_column : String,
}

enum RelationType {
  OneToOne
  OneToMany
  ManyToOne
  ManyToMany
}

pub fn get_all_tables() -> Array[String] {
  ["users", "roles", "posts", "comments", "tags", "post_tags"]
}

pub fn get_table_entities() -> Array[String] {
  ["User", "Role", "Post", "Comment", "Tag", "PostTag"]
}
```

---

## 资源索引

### 官方资源
- MoonBit 文档：https://docs.moonbitlang.com/zh-cn/stable/
- MoonBit 教程：https://docs.moonbitlang.com/zh-cn/latest/tutorial/tour.html
- Mooncakes 包仓库：https://mooncakes.io
- MoonBit 更新日志：https://www.moonbitlang.com/weekly-updates

### 第三方库
- **LunarTUI** (TUI 框架)：`moon add FrozenLemonTee/LunarTUI`
- **moonbit-qt-gui** (Qt GUI)：`moon add WilliamZ1008/qtgui`
- **moonbit-webview** (WebView GUI)：`moon add justjavac/moonbit-webview`

### v0.9 新特性参考
- Debug trait 替代 derive(Show)
- 正则表达式匹配 `s =~ re"..."`
- 反向管道语法 `<|`
- 形式化验证支持 `proof_ensure`
- Int64/UInt64 在 JS 后端编译为 BigInt

## 注意事项
- MoonBit 当前处于 beta-preview 阶段，API 可能变动
- 不同后端（wasm/js/native）支持的功能有差异
- FFI 调用需要了解目标平台的类型映射
- 使用 `moon mod tidy` 自动整理依赖
- 生产环境建议锁定依赖版本