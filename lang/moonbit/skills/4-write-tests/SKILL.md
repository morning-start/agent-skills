---
name: write-tests
version: 10.0.0
description: >
  编写 MoonBit 单元测试和集成测试。expect test、assert、覆盖率。
  Use when writing tests, adding test cases, verifying correctness,
  or setting up test infrastructure for MoonBit projects.
trigger:
  - "写测试" / "test" / "单测" / "验证"
  - "覆盖率" / "coverage" / "assert"
  - "expect test" / "快照测试"
tags: [testing, unit-test, expect-test, coverage, verification]
---

# 编写 MoonBit 测试

## 触发条件
用户需要**编写或添加测试**时激活。

## 决策树

```
测试需求？
├── 验证单个函数行为
│   └── 单元测试 → *_test.mbt + assert!/expect
├── 验证输出不变（回归保护）
│   └── Expect Test → @expect_val + moon test --update
├── 验证类型/属性关系
│   └── 属性测试 → 检查 Trait 实现一致性
├── 验证多组件交互
│   └── 集成测试 → 测试公共 API 边界
└── 性能基准对比
    └── 基准测试 → @bench + moon bench
```

## 执行步骤

### Step 1: 确定测试策略
- 单元测试：每个公开函数至少一个 happy path + 边界 case
- Expect Test：输出格式敏感的函数（序列化/渲染/格式化）
- 集成测试：跨包交互的关键路径

### Step 2: 创建测试文件
```moonbit
// lib/my_module_test.mbt
test "my_function works correctly" {
  let result = my_function(input)
  assert_eq(result, expected)?
}
```

### Step 3: 配置 moon.pkg
```toml
// 在被测包的 moon.pkg 中
import {
  "moonbitlang/core/builtin" @lib,
}
// 测试文件自动被 moon test 发现（*_test.mbt 后缀）
```

### Step 4: 编写测试用例
**必测场景**：
- 正常输入（happy path）
- 边界值（空/零/最大/最小）
- 错误输入（Result::Err 分支）
- Option::None 分支
- 枚举所有变体（ADT 穷尽性）

### Step 5: 运行并维护
```bash
moon test                    # 运行所有测试
moon test --update          # 更新 expect test 快照
moon test filter="keyword"  # 运行匹配的测试
```

## Expect Test 最佳实践

```moonbit
test "pretty_print output" {
  let result = pretty_print(data)
  @expect_val(result, "expected output here")
  // 首次运行: moon test --update 生成快照
  // 后续运行: 自动比对，不一致则失败
}
```

**适合场景**：格式化输出、序列化结果、错误消息文本

## 测试 checklist
- [ ] 每个公开函数有对应测试
- [ ] 覆盖 Result 的 Ok 和 Err 分支
- [ ] 覆盖 Option 的 Some 和 None
- [ ] ADT 枚举所有变体
- [ ] 边界条件已测试
- [ ] 测试命名清晰描述场景
- [ ] 无硬编码外部依赖

## 详细知识
🔗 `references/` 中 devtools 迁移的测试部分（原 Part 1 测试系统）
