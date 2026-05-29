---
name: write-code
version: 10.0.0
description: >
  编写/改造 MoonBit 源代码。涵盖泛型、Trait、模式匹配、可变性等核心语言特性。
  Use when writing or modifying MoonBit source code, implementing traits,
  writing generic functions, using pattern matching, or refactoring.
trigger:
  - "帮我写" / "实现" / "改" / "加功能"
  - "泛型" / "generic" / "trait" / "接口"
  - "模式匹配" / "match" / "enum" / "ADT"
  - "重构函数" / "抽取方法"
tags: [write-code, generic, trait, pattern-match, mutation, refactor]
---

# 编写/改造 MoonBit 代码

## 触发条件
用户需要**编写或修改** MoonBit 源代码时激活。

## 决策树

```
代码任务类型？
├── 定义数据类型
│   ├── 简单数据 → struct { fields }
│   ├── 带变体 → enum { A(...) B(...) }
│   └── 需外部构造 → pub(all) struct/enum
├── 需要泛型
│   ├── 函数级 → fn[T] func_name(...)
│   └── 类型级 → struct[T] Name { ... }
├── 需要多态行为
│   ├── 接口抽象 → pub(open) trait { fn method(...) }
│   └── 类型枚举 → match expr { :TypeA => ... }
├── 需要模式匹配
│   ├── 数据解构 → match value { Pattern => ... }
│   └── 类型分支 → match value { :TypeName => ... }
├── 需要可变操作
│   ├── 只改字段 → let x = self; x.field = v （无需 mut）
│   └── 重新赋值 → let mut x = self; x = new_x （需 mut）
└── 需要方法/运算符
    └── impl Type with method(self, ...) { ... }  // 注意：不支持 mut self
```

## 执行步骤

### Step 1: 分析现有代码
- 读取目标 `.mbt` 文件
- 识别现有类型、函数、import
- 检查是否有编译错误需先修复（调用 3-debug-errors）

### Step 2: 选择代码模式
根据决策树选择合适的模式，参考：
- 数据类型 → `references/syntax.md`, `references/type-system.md`
- 泛型/Trait → `references/generics-traits-methods.md`
- 模式匹配 → `references/pattern-matching.md`

### Step 3: 编写代码（遵循规范）
⚠️ **MoonBit v0.9+ 关键规则**：
1. **不支持 `mut self` 参数** — 用内部绑定替代
2. **For 循环不支持元组解构** — 先绑定再 match
3. **Match 分支多语句必须 `{}` 包裹** — 不要用逗号分隔
4. **Option 匹配不需要 `_` 通支** — Some/None 已穷尽
5. **泛型语法**: `fn[T] func_name(...)` 不是 `fn func_name[T](...)`

### Step 4: 验证
```bash
moon check      # 类型检查
moon fmt && git diff --check  # 格式化检查
```

### Step 5: 质量检查
- [ ] 无 E0015 unused_mut 警告
- [ ] 无 E4021 unbound variable 错误
- [ ] 无 E3002 parse error
- [ ] pub/pub(all) 可见性正确

## 代码风格要点
- 使用 `@alias.` 完全限定名引用跨包类型（mbtgraph 最佳实践）
- 同包内直接调用函数，无需模块前缀
- Block 用 `///|` 分隔组织相关代码
- 复杂逻辑拆分为私有辅助函数

## 详细知识
🔗 `references/syntax.md` — 基础语法速查
🔗 `references/type-system.md` — 类型系统详解
🔗 `references/generics-traits-methods.md` — 泛型/Trait/方法完整指南
🔗 `references/pattern-matching.md` — 模式匹配详解与陷阱
🔗 `references/pitfalls.md` — 常见陷阱合集
