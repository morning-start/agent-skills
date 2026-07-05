---
name: create-project
version: 10.0.0
description: >
  创建/初始化 MoonBit 项目。选模板、配置 moon.pkg、验证构建。
  Use when creating new MoonBit project, CLI tool, library, or application.
trigger:
  - "创建项目" / "新建" / "new project" / "moon new"
  - "初始化" / "init" / "从头开始"
  - "脚手架" / "scaffold" / "模板"
tags: [create, project-init, template, scaffold]
---

# 创建 MoonBit 项目

## 触发条件
用户要**从零开始**一个 MoonBit 项目时激活。

## 决策树

```
用户想创建什么？
├── CLI 命令行工具
│   └── → 参考 references/app-templates.md 模板一
├── 算法/计算库
│   └── → 参考 references/app-templates.md 模板二/三
├── GUI/TUI 应用
│   └── → 参考 references/app-templates.md 模板四/五/六
├── Web 服务
│   └── → 参考 references/app-templates.md 模板七
├── Monorepo 多包项目
│   └── → 参考 references/project-layout.md Monorepo 模板
├── 解释器/编译器
│   └── → 参考 references/app-templates.md 模板十
└── 属性驱动框架（ORM/代码生成）
    └── → 参考 references/app-templates.md 模板十一
```

## 执行步骤

### Step 1: 确认需求
- [ ] 应用类型？（CLI/lib/GUI/Web/Monorepo）
- [ ] 目标后端？（wasm-gc / js / native）
- [ ] 是否需要发布到 mooncakes？

### Step 2: 初始化项目
```bash
# 方式 A：使用 moon new（简单项目）
moon new my-project && cd my-project

# 方式 B：手动创建（复杂项目，参考 project-layout.md 模板）
mkdir -p my-project/src/lib/core my-project/cmd/main
```

### Step 3: 配置 moon.pkg
根据目标后端配置：
- Wasm-GC: `target("wasm-gc")`
- JS: `target("js")`
- 双目标: 不设 target 或用条件编译
- 参考 `references/project-layout.md` 完整配置字段表

### Step 4: 验证
```bash
moon check      # 类型检查
moon run        # 运行（如有 main）
moon build --target <后端>  # 构建
```

### Step 5: 初始化 Git
```bash
git init
echo "/_build/" >> .gitignore
git add -A && git commit -m "init: 项目初始化"
```

## 常见问题
- Q: 不知道选什么模板？A: 从最简单的 CLI 开始，参考 app-templates.md
- Q: 需要多后端支持？A: 参考 multi-backend.md 双运行时模式
- Q: 要发布到 mooncakes？A: 完成开发后调用 6-publish-lib 子技能

## 详细知识
🔗 `references/project-layout.md` — 项目结构与配置详解
🔗 `references/app-templates.md` — 10 种应用模板完整代码
🔗 `references/syntax.md` — 基础语法速查
