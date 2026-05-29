---
name: debug-errors
version: 10.0.0
description: >
  诊断修复 MoonBit 编译错误和运行时问题。错误码速查、陷阱识别、修复验证。
  Use when encountering compilation errors, warnings, or runtime issues,
  error codes like E0015/E0029/E3002/E4036 etc.
trigger:
  - "报错" / "编译失败" / "Error" / "Exxxx"
  - "警告" / "warning" / "unused"
  - "类型错误" / "type mismatch"
  - "怎么修" / "why error"
tags: [debug, error-fix, error-codes, diagnostics, troubleshooting]
---

# 诊断修复 MoonBit 错误

## 触发条件
用户遇到**编译错误、警告或运行时异常**时激活。

## Top 10 常见错误速查

| 错误码 | 含义 | 最常见原因 | 修复 |
|--------|------|-----------|------|
| **E0015** | unused_mut | 声明了 mut 但未重新赋值绑定 | 改为 `let` |
| **E0029** | unused_package | 存在其他编译错误导致 import 看似未使用 | 修复底层错误 |
| **E3002** | Parse error | 语法格式错误（mut self/for 解构/match 逗号）| 检查具体语法 |
| **E4021** | unbound variable | Trait 方法内未限定的标识符 | 用 `Trait::method()` |
| **E4036** | read-only type | 外部包无法构造 `pub struct` | 改为 `pub(all)` |
| **E4051** | unused_mut (warn) | 同 E0015 | 改为 `let` |
| **E4087** | immutable field | 字段缺少 `mut` 声明 | 添加 `mut` |
| **E4145** | sealed trait | 无法实现 `pub trait` | 改为 `pub(open)trait` |
| **E4014** | type mismatch | 类型不匹配 | 检查解构/返回类型 |
| **Wxxx** | Warning | 各种警告 | 对照具体 warning 处理 |

## 执行步骤

### Step 1: 获取完整错误列表
```bash
moon check      # 获取所有编译错误
moon fmt         # 自动修复格式问题
```

### Step 2: 定位第一个真正错误
- **总是从第一个真正的错误开始修复**
- 后续错误可能是级联产生的伪错误
- 区分 Error vs Warning（Warning 不阻断编译但不应忽略）

### Step 3: 查询错误码
- 对照上表匹配错误码
- 详细信息见 `references/error-codes.md`
- 无匹配错误码？→ 可能是新版本新增，搜索官方文档

### Step 4: 应用修复方案
按错误码对应的修复方式操作：
- **mut 相关 (E0015/E4051/E4087)**: 检查是否真的需要 `let mut`
- **可见性相关 (E4036/E4145)**: 检查 pub vs pub(all), trait vs pub(open)trait
- **语法相关 (E3002)**: 检查 mut self / for 解构 / match 分支格式
- **作用域相关 (E4021)**: Trait 方法内用完全限定名

### Step 5: 重新验证
```bash
moon check      # 确认错误消除
moon test       # 确保测试仍通过
```

循环 Step 2-5 直到 Exit code 0。

## 八大陷阱快速修复

| # | 陷阱 | ❌ 错误 | ✅ 修复 |
|---|------|---------|---------|
| 1 | mut self | `fn method(mut self)` | 内部 `let s = self` |
| 2 | for 元组解构 | `for (a,b) in arr` | `for p in arr { match p { (a,b) => ... }}` |
| 3 | Match 逗号分支 | `A => f(); B => g(),` | `A => { f() } B => { g() }` |
| 4 | 构造只读类型 | 直接构造 pub struct | 改 pub(all) struct |
| 5 | 实现密封 Trait | 实现 pub trait | 改 pub(open)trait |
| 6 | Trait unbound | `other_method(self)` | `@pkg::Trait::other_method(self)` |
| 7 | Option 冗余通配 | `match o { Some(x)=>x; None=>(); _=>() }` | 删除 `_` 分支 |
| 8 | 变量名混淆 | `(f, w) => use w.0` | `(nid, _) => use nid.0` |

## 详细知识
🔗 `references/error-codes.md` — 完整错误码速查与诊断工作流
🔗 `references/pitfalls.md` — 常见陷阱深度解析
🔗 `references/type-system.md` — 可见性系统详解
🔗 `references/generics-traits-methods.md` — Part 4.5 可变性语义
