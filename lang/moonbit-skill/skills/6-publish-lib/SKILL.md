---
name: publish-lib
version: 10.0.0
description: >
  发布 MoonBit 库到 mooncakes。API 设计审查、版本管理、
  构建发布流程、文档规范。
  Use when preparing to publish a MoonBit library to mooncakes,
  versioning releases, or ensuring publish-ready quality.
trigger:
  - "发布" / "publish" / "mooncakes"
  - "开源" / "共享" / "package"
  - "版本号" / "version" / "semver"
  - "API 设计" / "public interface"
tags: [publish, mooncakes, api-design, versioning, semver, release]
---

# 发布 MoonBit 库

## 触发条件
用户准备**将 MoonBit 库发布到 mooncakes** 时激活。

## 发布前 Checklist

### API 质量
- [ ] 公开 API 最小化原则（只暴露必要的）
- [ ] 命名遵循规范（snake_case 函数 / CamelCase 类型）
- [ ] 所有公开类型有文档注释
- [ ] 无 pub(all) 滥用（只在确实需要外部构造时使用）
- [ ] Trait 设计合理（pub(open)trait 用于需要外部实现的接口）

### 配置完整性
- [ ] `moon.mod.json` name/version/readme/license 正确
- [ ] `moon.pkg` export/import 配置正确
- [ ] 支持 target 兼容性声明（如需）
- [ ] README.md 包含安装和使用示例

### 测试覆盖
- [ ] 所有公开函数有测试
- [ ] 测试通过 (`moon test`)
- [ ] 无编译警告

### 版本号
- [ ] 遵循语义化版本 (semver)
- [ ] breaking change → major
- [ ] 新功能 → minor
- [ ] bug fix → patch

## 执行步骤

### Step 1: API 审查
运行 `moon info` 检查公开接口：
```bash
moon info
git diff -- "*.mbti"   # 检查 API 变更
```
对照 `references/library-design.md` Parts 1-5 检查 API 设计质量。

### Step 2: 构建 Release
```bash
moon build --release
# 或指定后端
moon build --target wasm-gc --release
moon build --target js --release
```

### Step 3: 本地验证
```bash
# 创建临时测试项目验证安装
moon new test-consumer
# 在 test-consumer 中 import 你的库
# 确认可以正常使用
```

### Step 4: 发布
```bash
moon publish  # 发布到 mooncakes
# 或手动上传
```

### Step 5: 发布后
- 更新 CHANGELOG.md
- 打 git tag: `git tag -a vx.y.z`
- 更新 README 版本 badge

## 库设计核心原则速查
1. **最小 API**: 只暴露必要的东西
2. **正确可见性**: pub(只读) > pub(all)(完全公开)
3. **Trait 密封**: 默认 pub trait，需要外部实现才用 pub(open)trait
4. **语义化版本**: 不 breaking change 不升 major
5. **文档完备**: 公开 API 必须有注释

## 详细知识
🔗 `references/library-design.md` — 完整库设计指南（Parts 1-11）
🔗 `references/real-world-examples.md` — 成功发布的库案例
🔗 `references/app-templates.md` — 库项目模板