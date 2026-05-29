---
name: optimize
version: 10.0.0
description: >
  MoonBit 性能优化与多后端适配。Wasm 体积优化、JS gzip 压缩、
  Native 性能调优、双目标构建策略。
  Use when optimizing performance, reducing binary size,
  choosing compilation targets, or cross-backend development.
trigger:
  - "优化" / "性能" / "慢" / "太慢了"
  - "体积太大" / "wasm 大小" / "gzip"
  - "多后端" / "wasm/js/native" / "cross compile"
  - "benchmark" / "基准测试" / "性能对比"
tags: [optimize, performance, wasm, js, native, benchmark, cross-backend]
---

# 性能优化与多后端适配

## 触发条件
用户关注**性能、体积或多后端支持**时激活。

## 决策树

```
优化目标？
├── 减小 Wasm 体积
│   ├── release 模式 → moon build --target wasm-gc --release
│   ├── tree-shaking → 最小化 pub 导出
│   └── 内联标记 → #[inline] 热点函数
├── 减小 JS 输出体积
│   ├── 最小化导出 → priv 标记内部函数
│   ├── 惰性初始化 → 延迟加载重型数据
│   └── 避免泛型膨胀 → 特化关键路径
├── 提升运行时性能
│   ├── 算法优化 → 先分析复杂度
│   ├── 内存分配 → 减少不必要的拷贝
│   └── 基准测试定位瓶颈 → moon bench
├── 多后端支持
│   ├── Wasm-GC + JS 双目标 → 平台抽象 Trait
│   └── Native 特定功能 → 条件编译 target("native")
└── 发布 npm 包
    └── JS 后端 + package.json + TypeScript 声明
```

## 执行步骤

### Step 1: 基准测试（定位瓶颈）
```bash
moon bench              # 运行基准测试
# 分析输出：哪些函数耗时最长
```

### Step 2: 选择优化策略
| 场景 | 策略 | 预期效果 |
|------|------|---------|
| Wasm 体积大 | `--release` + 最小导出 | -30%~50% |
| JS 体积大 | priv 标记 + 惰性初始化 | 类似 MoonBash 434KB gzip |
| 运行时慢 | 算法优化 + 减少拷贝 | 取决于瓶颈 |
| 需要多平台 | 双目标 + 平台抽象 Trait | 一次编写多端运行 |

### Step 3: 后端特定优化
- **Wasm-GC**: 参考 `references/multi-backend.md` Chapter 7-8
- **JS**: 参考 MoonBash 的 434KB gzip 成果（`references/real-world-examples.md`）
- **Native**: link-options + LTO

### Step 4: 验证优化效果
```bash
# 对比优化前后
moon build --target <后端> --release
ls -la target/*/release/
# Wasm: 看 .wasm 文件大小
# JS: 看 .mjs gzip 大小
```

### Step 5: 回归测试
```bash
moon test      # 确保优化未破坏功能
moon bench      # 确认性能确实提升
```

## 经验数据（来自真实项目）

| 项目 | 优化策略 | 结果 |
|------|---------|------|
| MoonBash | priv 导出 + 惰性初始化 + 内联 | **434 KB** gzip (原 ~1.8MB) |
| moon-lottie | Wasm-GC + JS 双目标 | 同一套代码两个产物 |
| mbtgraph | 半存储优化（无向图 O(V+E)） | 空间节省 ~50% |

## 详细知识
🔗 `references/multi-backend.md` — 多后端开发完整指南
🔗 `references/real-world-examples.md` — 真实项目优化案例
🔗 `references/library-design.md` — Builder/Converter 模式（影响性能的设计决策）