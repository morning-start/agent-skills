# MoonBit 项目布局与规范

> **来源**: `moonbit-project-layout` SKILL.md v8.0.0
> **实践经验来源**: mbtgraph（MoonBit 图算法库）生产实践总结

---

## 一、标准项目结构

### 基础项目布局

```
hello-moonbit/
├── moon.mod.json              # 模块元数据（必填）
├── moon.pkg.json              # 包配置（根包）
├── src/                       # 库代码目录
│   └── lib.mbt               # 库源文件
├── cmd/                       # 可执行命令目录
│   └── main/
│       ├── main.mbt          # 主程序入口
│       └── moon.pkg          # 主包配置
└── tests/                     # 测试代码目录
    └── lib_test.mbt          # 测试文件
```

### 大型项目布局

```
my-large-project/
├── moon.mod.json
├── moon.workspace.json        # 工作区配置（可选）
├── src/
│   ├── core/                 # 核心模块
│   │   ├── moon.pkg.json
│   │   ├── types.mbt
│   │   └── operations.mbt
│   ├── utils/                # 工具模块
│   │   ├── moon.pkg.json
│   │   └── helpers.mbt
│   └── api/                  # API 层
│       ├── moon.pkg.json
│       └── handlers.mbt
├── cmd/
│   ├── server/
│   │   ├── main.mbt
│   │   └── moon.pkg.json
│   └── cli/
│       ├── main.mbt
│       └── moon.pkg.json
└── tests/
    ├── core_test.mbt
    ├── utils_test.mbt
    └── integration_test.mbt
```

---

## 二、配置文件详解

### moon.mod.json（模块配置）

定义模块的元数据，是发布的单元：

```json
{
  "name": "username/my-project",
  "version": "0.1.0",
  "license": "Apache-2.0",
  "description": "A MoonBit library",
  "keywords": ["moonbit", "utility"],
  "repository": "https://github.com/username/my-project",
  "homepage": "https://github.com/username/my-project",
  "readme": "README.mbt.md",
  "preferred-target": "wasm"
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | ✅ 是 | 模块全名，格式 `username/name` |
| `version` | ✅ 是 | 语义化版本号（SemVer） |
| `license` | 否 | 开源许可证（推荐填写） |
| `description` | 否 | 模块描述 |
| `keywords` | 否 | 关键词数组（用于搜索） |
| `repository` | 否 | 代码仓库地址 |
| `homepage` | 否 | 主页地址 |
| `readme` | 否 | 说明文件路径 |
| `preferred-target` | 否 | 首选编译目标（wasm/js/native） |

### moon.pkg / moon.pkg.json（包配置）

定义包的编译和依赖关系，是编译的基本单元。MoonBit 支持**两种包配置格式**：

#### 格式概览

| 特性 | 旧格式 (moon.pkg.json) | 新格式 (moon.pkg) |
|------|----------------------|-------------------|
| 文件名 | `moon.pkg.json` | `moon.pkg` |
| 语法 | JSON | TOML-like DSL |
| 注释支持 | ❌ 不支持 | ✅ 支持 `//...` |
| 可读性 | 一般 | ✅ 更简洁直观 |
| 官方推荐 | 仍兼容 | ✅ **推荐使用** |

#### 旧格式 (moon.pkg.json) - JSON 风格

```json
{
  "is-main": false,
  "import": [
    {
      "path": "moonbitlang/core",
      "alias": "core"
    },
    {
      "path": "username/other-lib",
      "alias": "other"
    }
  ],
  "test-import": [
    {
      "path": "moonbitlang/core",
      "alias": "core"
    }
  ]
}
```

#### 新格式 (moon.pkg) - DSL 风格（官方推荐）

```toml
import {
  "moonbitlang/core/builtin",
  "myorg/some-lib" @alias,
}

import {
  "path/to/package1",
} for "test"

options(
  "is-main": true,
  "supported-targets": "js",
  targets: {
    "only_js.mbt": ["js"],
    "only_wasm.mbt": ["wasm"],
  },
)
```

**关键要点**：

- 使用 `import { ... }` 声明依赖，支持 `@alias` 别名
- 使用 `for "test"` 和 `for "wbtest"` 分别声明测试导入和白盒测试导入
- 所有其他字段放入 `options(...)` 块
- 支持 `//...` 行内注释
- 通过 `moon fmt -C <module_dir>` 从旧格式自动转换

#### 完整字段对照表（新旧格式）

| 功能 | 旧格式 (moon.pkg.json) | 新格式 (moon.pkg) |
|------|----------------------|-------------------|
| 导入依赖 | `"import": [...]` | `import { ... }` |
| 测试导入 | `"test-import": {...}` | `import { ... } for "test"` |
| 白盒测试导入 | `"wbtest-import": {...}` | `import { ... } for "wbtest"` |
| 主包标记 | `"is-main": true` | `options("is-main": true)` |
| 条件编译 | `"targets": {...}` | `options(targets: { ... })` |
| 支持目标 | `"supported-targets": [...]` | `options("supported-targets": ...)` |
| 链接选项 | `"link": {...}` | `options(link: { ... })` |
| 格式化忽略 | `"formatter": {"ignore": [...]}` | `options(formatter: { ignore: [...] })` |
| 最大并发测试 | `"max-concurrent-tests": N` | `options("max-concurrent-tests": N)` |
| 虚拟包 | `"virtual": {...}` | `options("virtual": { ... })` |

#### 从旧格式迁移到新格式

```bash
# 自动转换整个模块的所有 moon.pkg.json → moon.pkg
moon fmt -C <module_dir>

# 或手动创建 moon.pkg 文件并删除 moon.pkg.json
# 确保同一目录下只存在一种格式
```

**注意：** 同一目录下不能同时存在 `moon.pkg` 和 `moon.pkg.json`，否则会报错。

### 条件编译

MoonBit 支持根据目标后端和优化模式进行条件编译，让你可以为不同平台编写特定代码。

#### 基本语法

```toml
# 新格式 (moon.pkg)
options(
  targets: {
    "only_js.mbt": ["js"],           # 仅 JS 后端
    "only_wasm.mbt": ["wasm"],       # 仅 Wasm 后端
    "all_wasm.mbt": ["wasm", "wasm-gc"], # 所有 Wasm 后端
    "not_js.mbt": ["not", "js"],     # 非 JS 后端
    "only_debug.mbt": ["debug"],      # 仅 debug 模式
    "js_and_release.mbt": ["and", ["js"], ["release"]],  # JS 且 release
  }
)
```

#### 支持的条件运算符

| 运算符 | 语法 | 说明 |
|--------|------|------|
| **无** | `["js"]` | 匹配指定后端/模式 |
| **not** | `["not", "js"]` | 排除指定后端/模式 |
| **and** | `["and", [...], [...]]` | 同时满足多个条件 |
| **or** | `["or", [...], [...]]` | 满足任一条件 |

#### 支持的分类

**后端条件：**

| 值 | 说明 |
|----|------|
| `"wasm"` | WebAssembly 后端 |
| `"wasm-gc"` | WebAssembly GC 后端 |
| `"js"` | JavaScript 后端 |

**优化层次：**

| 值 | 说明 |
|----|------|
| `"debug"` | 调试模式（默认） |
| `"release"` | 发布模式（启用优化） |

#### 实际应用示例

```toml
# 平台特定实现
options(
  targets: {
    "platform_js.mbt": ["js"],
    "platform_wasm.mbt": ["wasm"],
  }
)

# 仅在 release 模式下包含的性能优化代码
options(
  targets: {
    "perf_opt.mbt": ["release"],
  }
)

# 复杂组合：Wasm 或 JS 的 debug 模式
options(
  targets: {
    "debug_common.mbt": ["and", [["or", ["wasm"], ["js"]]], ["debug"]],
  }
)
```

### supported-targets vs targets 区别

这两个字段容易混淆，但它们有不同的用途：

| 特性 | `supported-targets` | `targets` |
|------|---------------------|-----------|
| **作用域** | 包级元数据 | 文件级条件编译规则 |
| **用途** | 声明该包**打算支持哪些后端** | 为不同后端**包含或排除单独文件** |
| **影响** | 影响包的发布和依赖解析 | 影响哪些文件参与编译 |
| **位置** | `moon.mod.json` 或 `moon.pkg` | 仅在 `moon.pkg` / `moon.pkg.json` 中 |

#### 使用场景对比

```toml
# 场景 1：声明包支持的目标（影响发布）
options(
  "supported-targets": ["wasm", "js"]  # 这个包支持 wasm 和 js
)

# 场景 2：按目标包含不同文件（影响编译）
options(
  targets: {
    "js_runtime.mbt": ["js"],
    "wasm_runtime.mbt": ["wasm"],
  }
)

# 场景 3：组合使用
options(
  "supported-targets": ["wasm", "js"],
  targets: {
    "platform_specific.mbt": ["js"],
  }
)
```

---

## 三、包管理核心概念

### 模块与包的关系

```
模块 (Module)          包 (Package)
┌─────────────┐       ┌─────────────┐
│ moon.mod.json│ 1  : N│ moon.pkg.json│
│             │──────>│             │
│ 发布单元     │       │ 编译单元     │
└─────────────┘       └─────────────┘
```

- **模块 (Module)**：由 `moon.mod.json` 定义，是发布到 mooncakes 的单元
- **包 (Package)**：由 `moon.pkg.json` 定义，是编译的基本单元
- 一个模块可以包含多个包

### Mooncakes 包仓库

Mooncakes 是 MoonBit 的官方包仓库（类似 npm、crates.io）：

```bash
# 搜索包
mooncakes search <keyword>

# 或访问网站
# https://mooncakes.io
```

**常用官方包**：

| 包名 | 说明 | 路径 |
|------|------|------|
| core | 标准库 | `moonbitlang/core` |
| json | JSON 处理 | `moonbitlang/json` |
| x | 扩展库 | `moonbitlang/x` |

---

## 四、依赖管理

### 添加依赖

```bash
# 从 mooncakes 添加依赖
moon add moonbitlang/core

# 添加特定版本
moon add username/package@1.0.0
```

### 手动配置依赖

在 `moon.pkg.json` 中添加：

```json
{
  "import": [
    {
      "path": "moonbitlang/core",
      "alias": "core"
    }
  ]
}
```

在代码中使用别名引用：

```moonbit
fn main {
  @core.println("Using core package")
}
```

### 更新和移除依赖

```bash
# 更新所有依赖
moon update

# 更新特定依赖
moon update username/package

# 移除依赖
moon remove username/package
```

---

## 五、工作区（Workspace）

大型项目可以使用工作区管理多个模块：

### 工作区结构

```
my-workspace/
├── moon.workspace.json         # 工作区配置
├── module-a/                   # 子模块 A
│   ├── moon.mod.json
│   └── src/
├── module-b/                   # 子模块 B
│   ├── moon.mod.json
│   └── src/
└── shared/                     # 共享库
    ├── moon.mod.json
    └── src/
```

### 工作区配置

```json
// moon.workspace.json
{
  "modules": [
    "module-a",
    "module-b",
    "shared"
  ]
}
```

### 工作区优势

- **统一依赖管理**：所有子模块共享依赖版本
- **本地开发**：子模块间可以直接引用，无需发布
- **原子提交**：跨模块的改动可以一起提交
- **CI/CD 简化**：可以一次性构建和测试所有模块

---

## 六、发布流程

### 发布准备

```bash
# 1. 确保测试通过
moon test

# 2. 格式化代码
moon fmt

# 3. 检查模块配置
moon check
```

### 版本管理（SemVer）

| 版本变更 | 说明 | 示例 |
|----------|------|------|
| **major** | 破坏性 API 变更 | 1.0.0 → 2.0.0 |
| **minor** | 新增功能（向后兼容） | 1.0.0 → 1.1.0 |
| **patch** | Bug 修复（向后兼容） | 1.0.0 → 1.0.1 |

### 发布执行

```bash
# 登录 mooncakes（首次）
moon login

# 发布模块
moon publish
```

---

## 七、最佳实践

### 命名规范

- **模块名**：使用 `username/project-name` 格式
- **包别名**：简短且有语义（`core`, `http`, `db`）
- **文件名**：使用 snake_case（`my_module.mbt`）

### 目录组织原则

1. **按功能分组**：相关功能放在同一包中
2. **保持扁平**：避免过深的目录嵌套
3. **分离关注点**：库代码（src/）和可执行代码（cmd/）分开
4. **测试就近**：测试文件放在对应的 tests/ 目录

### 依赖管理建议

1. **最小化依赖**：只引入必要的包
2. **固定版本**：生产环境锁定依赖版本
3. **定期更新**：保持依赖的安全性和性能
4. **避免循环依赖**：模块间依赖应该是单向的

---

## 八、Monorepo 项目布局模板

> 当项目规模增长到需要多个包协同时，采用 Monorepo 布局

### 什么时候该用 Monorepo？

| 指标 | 单包项目 | Monorepo |
|------|---------|----------|
| 代码量 | < 5000 行 | > 5000 行 |
| 包数量 | 1 个 | 2-10 个 |
| 发布形式 | 单一产物 | 多产物（库+CLI+绑定）|
| 团队规模 | 1-2 人 | 3+ 人 |
| 示例 | CLI 工具、简单库 | moon-lottie、morm |

### 模板 A：库 + 工具链 Monorepo（来自 moon-lottie）

适用于需要同时发布核心库、命令行工具、语言绑定和演示应用的项目：

```
library-monorepo/
├── moon.mod.json                    # 根模块配置
├── moon.workspace.json              # 工作区声明
│
├── src/                             # 🔧 核心库代码（发布到 mooncakes）
│   ├── core/                        #    纯算法，无平台依赖
│   │   ├── moon.pkg
│   │   ├── types.mbt
│   │   └── algorithms.mbt
│   ├── parser/                      #    解析/序列化
│   │   ├── moon.pkg
│   │   └── parser.mbt
│   └── renderer/                    #    抽象渲染接口
│       ├── moon.pkg
│       └── interface.mbt
│
├── cmd/                             # 🚀 可执行程序（不发布）
│   ├── player/                      #    Wasm/JS 运行时
│   │   ├── moon.pkg
│   │   └── main.mbt
│   └── export_cli/                  #    导出工具
│       ├── moon.pkg
│       └── main.mbt
│
├── packages/                        # 📦 语言绑定（npm 发布）
│   ├── js-binding/
│   │   ├── package.json
│   │   └── index.js
│   └── web-component/
│       ├── package.json
│       └── component.ts
│
├── demo/                            # 🎮 Playground（不发布）
│   └── app/
│       ├── moon.pkg
│       └── main.mbt
│
├── pnpm-workspace.yaml              # npm workspace 配置
├── package.json                     # 根 package.json（脚本）
├── scripts/
│   ├── build.sh                     # 全量构建
│   ├── build-wasm.sh                # Wasm 构建
│   ├── build-js.sh                  # JS 构建
│   └── test-all.sh                  # 全量测试
│
├── README.md                        # 用户文档
├── README.mbt.md                    # MoonBit 专用文档
└── LICENSE
```

**moon.mod.json 配置**:

```json
{
  "name": "username/my-library-monorepo",
  "version": "0.1.0",
  "readme": "README.md",
  "license": "MIT",
  "description": "A monorepo library with multiple targets"
}
```

**moon.workspace.json 配置**:

```json
{
  "-src": ["src/core", "src/parser", "src/renderer"]
}
```

**pnpm-workspace.yaml**:

```yaml
packages:
  - 'packages/*'
```

**根 package.json**:

```json
{
  "name": "my-library-monorepo-root",
  "private": true,
  "scripts": {
    "build:wasm": "bash scripts/build-wasm.sh",
    "build:js": "bash scripts/build-js.sh",
    "build:all": "bash scripts/build.sh",
    "test": "moon test",
    "demo": "moon run demo/app"
  },
  "devDependencies": {
    "pnpm": "^8.0.0"
  }
}
```

### 模板 B：属性驱动框架 Monorepo（来自 morm）

适用于使用宏/属性驱动的框架项目，如 ORM、Web 框架等：

```
framework-monorepo/
├── moon.mod.json
├── moon.workspace.json
│
├── src/                             # 🔧 框架核心
│   ├── attributes/                  #    属性定义
│   │   ├── moon.pkg
│   │   └── attrs.mbt
│   ├── generator/                   #    代码生成器
│   │   ├── moon.pkg
│   │   └── generator.mbt
│   ├── engine/                      #    核心引擎
│   │   ├── moon.pkg
│   │   └── engine.mbt
│   ├── dialect/                     #    方言适配
│   │   ├── moon.pkg
│   │   └── dialect.mbt
│   └── main/                        #    公开 API
│       ├── moon.pkg
│       └── api.mbt
│
├── cmd/                             # 🚀 CLI 工具
│   └── generator/
│       ├── moon.pkg
│       └── main.mbt                 # `moon run generator`
│
├── lib/                             # 🔗 FFI 绑定
│   └── native_lib/
│       ├── moon.pkg
│       ├── ffi.mbt                  # FFI 声明
│       └── stub.c                   # Native 存根
│
├── test/                            # 🧪 测试套件
│   ├── unit_test.mbt
│   ├── integration_test.mbt
│   └── e2e_test.mbt
│
├── example/                         # 📖 用户示例
│   ├── models.mbt                   #    实体定义
│   └── models.g.mbt                 #    生成代码（git ignore）
│
├── docs/                            # 📚 文档
│   ├── getting-started.md
│   ├── api-reference.md
│   └── ffi-guide.md
│
└── README.md
```

**各目录职责说明**:

| 目录 | 职责 | 是否发布 | 是否为独立包 |
|------|------|---------|------------|
| `src/*` | 框架核心实现 | ✅ 是（作为库） | ✅ 各自独立 `moon.pkg` |
| `cmd/*` | CLI 入口点 | ❌ 否 | ✅ 独立 `moon.pkg` |
| `lib/*` | C FFI 绑定 | ✅ 随主库发布 | ✅ 独立 `moon.pkg` |
| `test/*` | 测试代码 | ❌ 否 | 同所属包 |
| `example/*` | 示例代码 | ❌ 否 | 独立 `moon.pkg` |
| `docs/*` | 文档 | ❌ 否 | 不计入 |

### 模板 C：解释器/编译器 Monorepo（来自 MoonBash）

适用于语言工具链项目，如解释器、编译器、REPL 等：

```
interpreter-monorepo/
├── moon.mod.json
├── moon.workspace.json
│
├── src/
│   ├── frontend/                    # 📖 前端（源码→AST）
│   │   ├── lexer/
│   │   │   ├── moon.pkg
│   │   │   ├── token.mbt           # Token ADT
│   │   │   └── lexer.mbt           # 词法分析
│   │   ├── parser/
│   │   │   ├── moon.pkg
│   │   │   ├── ast.mbt             # AST ADT
│   │   │   └── parser.mbt          # 语法分析
│   │   └── semantic/
│   │       ├── moon.pkg
│   │       └── analyzer.mbt        # 语义分析
│   │
│   ├── runtime/                     # ⚙️ 运行时（AST执行）
│   │   ├── evaluator/
│   │   │   ├── moon.pkg
│   │   │   └── eval.mbt            # 求值器
│   │   ├── builtin/
│   │   │   ├── moon.pkg
│   │   │   ├── registry.mbt        # 命令注册表
│   │   │   └── commands.mbt         # 内置命令
│   │   └── env/
│   │       ├── moon.pkg
│   │       └── environment.mbt     # 环境管理
│   │
│   ├── vm/                          # 🤖 子组件 VM
│   │   ├── moon.pkg
│   │   ├── regex_vm.mbt            # 正则 VM
│   │   └── opcodes.mbt             # 操作码定义
│   │
│   └── api/                         # 🌐 公开 API
│       ├── moon.pkg
│       ├── types.mbt
│       └── session.mbt
│
├── cmd/
│   └── repl/
│       ├── moon.pkg
│       └── main.mbt                # REPL 循环
│
├── bindings/                        # 🔗 外部绑定
│   └── typescript/
│       ├── src/
│       │   └── index.ts            # TS API
│       └── package.json
│
└── tests/
    ├── lexer_test.mbt
    ├── parser_test.mbt
    ├── eval_test.mbt
    └── e2e_test.mbt
```

### Monorepo 最佳实践清单

| # | 实践 | 说明 | 来源 |
|---|------|------|------|
| 1 | **清晰分层** | lib(核心)/cmd(入口)/packages(绑定)/demo(示例) 四层分离 | moon-lottie |
| 2 | **workspace 声明** | 使用 `moon.workspace.json` 声明内部包 | MoonBit 规范 |
| 3 | **独立 pkg** | 每个子目录是独立的 `moon.pkg` 单元 | 所有三个项目 |
| 4 | **双目标构建** | 同时支持 wasm-gc 和 js，各自有入口 | moon-lottie |
| 5 | **npm workspace** | 用 pnpm/yarn workspace 管理 JS 子包 | moon-lottie |
| 6 | **文档分离** | README.md(用户) + README.mbt.md(MoonBit开发者) | moon-lottie |
| 7 | **FFI 隔离** | C FFI 绑定放在 `lib/` 或 `ffi/` 独立目录 | morm |
| 8 | **生成代码管理** | `.g.mbt` 文件加入 `.gitignore` 或单独跟踪 | morm |
| 9 | **构建脚本化** | 复杂构建逻辑写入 `scripts/` 目录 | moon-lottie |
| 10 | **示例完整** | `example/` 提供可直接运行的示例 | morm |

---

## 九、moon.pkg DSL 实践经验

> 来自 mbtgraph（MoonBit 图算法库）的生产实践总结

### 三种引用风格对比

```moonbit
// 方式 1: 完全限定名（推荐用于大型项目）
@core.NodeId
@core.GraphReadable::neighbors(g, id)

// 方式 2: use 别名（旧方式，已弃用）
use @core.{NodeId, Node, Edge}
NodeId(...)   // 直接使用

// 方式 3: using 统一导入（v0.6.29+）
using @core
NodeId(...)   // 直接使用
```

**引用风格决策表**：

| 风格 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| **`@alias.` 完全限定名** | 大型项目、多人协作 | 无歧义、IDE 跳转可靠、自文档化 | 稍冗长 |
| `use @alias.{...}` | 小型项目、少量导入 | 简洁 | 作用域规则复杂 |
| `using @alias` | 中型项目、统一导入 | 最简洁 | 可能命名冲突 |

**mbtgraph 的选择**：完全限定名 `@core.` — 决策理由：
- 无歧义，任何位置都能立即识别来源包
- 不依赖 use/using 的作用域规则
- IDE 跳转更可靠
- 多人协作时代码更自文档化

### 同包内函数调用规则

同一 `moon.pkg` 目录下的 `.mbt` 文件属于**同一个包**，函数直接调用，**不需要模块前缀**：

```moonbit
// shared_helpers.mbt 中定义
pub fn has_node(nodes : Array[Node?], idx : Int) -> Bool { ... }

// directed_adj_list.mbt 中使用（同包，无需前缀）
has_node(self.nodes, idx)        // ✅ 正确
shared_helpers::has_node(...)     // ❌ 错误：同包不需要前缀
```

### Block 风格组织（///| 分隔符）

MoonBit 支持块式组织代码，每个块用 `///|` 分隔：

```moonbit
///|
/// 这是第一个块的文档注释
fn foo() -> Int { 0 }

///|
/// 这是第二个块，独立于上面的块
fn bar() -> Int { 1 }
```

**特点**：
- 块之间顺序无关，重构时可以自由移动
- 每个块可以独立包含类型、函数、impl 等
- 废弃的代码放入 `deprecated.mbt`
- 每个块可以有独立的文档注释

### .mbti 接口文件

`.mbti` 是包的公开接口描述文件。

**生成与更新**：
```bash
moon info    # 生成/更新 .mbti 接口文件
```

**.mbti 的意义**：
- 如果修改代码后 `.mbti` 不变 → 改动是内部实现细节，不影响外部使用者
- 如果 `.mbti` 变更 → 公开 API 发生变化，需要评估影响

**检查接口变更**：
```bash
git diff -- "*.mbti"
```

### 常见错误：E0029 unused_package

```
Error: unused_package: @core is imported but unused
```

**原因**：不是真的未使用，而是文件中存在其他编译错误导致 import 看起来"未被消费"。修复底层错误后自动消失。

---

## 十、注意事项

- 模块名全局唯一，必须使用 `username/name` 格式
- 发布前确保所有测试通过且代码已格式化
- 注意版本兼容性，避免破坏性变更（需升级 major 版本）
- 使用 `moon fmt` 保持团队代码风格一致
- 工作区适合 monorepo 风格的大型项目
- **moon.pkg 和 moon.pkg.json 不能共存于同一目录**
- 推荐使用新格式 `moon.pkg`，支持注释且更易读
- 条件编译可以帮助你编写平台特定代码，但要注意维护成本

---

*文档版本: v8.0.0 (from moonbit-project-layout SKILL.md)*
*技能状态: ✅ 稳定版*
*最后更新: 2026-05*
*适用范围: MoonBit ≥ 0.1.0*
