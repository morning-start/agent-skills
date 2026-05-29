# Changelog 规范指南

## 目录

1. [概述](#概述)
2. [标准命名](#标准命名)
3. [格式规范](#格式规范)
4. [版本号规范](#版本号规范)
5. [变更类型](#变更类型)
6. [Changelog 模板](#changelog-模板)
7. [最佳实践](#最佳实践)

---

## 概述

Changelog（变更日志）是记录项目所有重要变更的文件。它帮助开发者和用户了解项目的演变历史、新功能、问题修复和破坏性变更。

### 为什么要使用 Changelog

✅ **透明度**：清晰记录每个版本的变化
✅ **可追溯性**：快速定位问题和功能
✅ **沟通工具**：向用户传达重要变更
✅ **自动化**：支持自动生成发布说明

### 标准

本规范基于 [Keep a Changelog](https://keepachangelog.com/) 标准，并遵循 [Semantic Versioning](https://semver.org/spec/v2.0.0.html) 版本号规范。

---

## 标准命名

⚠️ **重要**：变更日志文件必须命名为 `CHANGELOG.md`（全大写），位于项目根目录。

**标准路径**：`/CHANGELOG.md`

**错误示例**：
- `changelog.md`（小写）
- `CHANGELOG.markdown`（扩展名错误）
- `wiki/changelog.md`（位置错误）
- `CHANGELOG.txt`（格式错误）

**正确示例**：
- `CHANGELOG.md`（标准）

---

## 格式规范

### 基本结构

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2024-01-15

### Added
- 新功能 1
- 新功能 2

### Changed
- 变更 1
- 变更 2

### Deprecated
- 废弃功能

### Removed
- 移除功能

### Fixed
- 修复问题

### Security
- 安全更新

[Unreleased]: https://github.com/user/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/user/repo/compare/v0.9.0...v1.0.0
```

### 版本条目格式

每个版本条目包含以下部分：

| 部分 | 必选 | 说明 |
|------|------|------|
| 版本号 | ✅ | 遵循 Semantic Versioning |
| 日期 | ✅ | YYYY-MM-DD 格式 |
| 变更类型 | ⭕ | Added/Changed/Deprecated/Removed/Fixed/Security |
| 变更内容 | ⭕ | 简洁描述变更内容 |

### Unreleased 部分

```markdown
## [Unreleased]
```

用于记录尚未发布的变更。发布时，将此部分替换为新的版本号。

---

## 版本号规范

### Semantic Versioning (SemVer)

格式：`MAJOR.MINOR.PATCH`

- **MAJOR**（主版本号）：不兼容的 API 修改
- **MINOR**（次版本号）：向下兼容的功能性新增
- **PATCH**（修订号）：向下兼容的问题修正

### 版本号示例

| 版本号 | 说明 |
|--------|------|
| 1.0.0 | 第一个稳定版本 |
| 1.1.0 | 新增功能，向下兼容 |
| 1.1.1 | 问题修复，向下兼容 |
| 2.0.0 | 破坏性变更，不兼容 |

### 何时升级版本号

| 升级类型 | 触发条件 | 示例 |
|----------|----------|------|
| PATCH | 向下兼容的问题修复 | 修复 bug、性能优化 |
| MINOR | 向下兼容的功能新增 | 新增 API、新功能 |
| MAJOR | 不兼容的 API 修改 | 删除 API、参数变更 |

---

## 变更类型

### Added（新增）

添加了新的功能。

**示例**：
```
### Added
- 添加用户认证功能
- 新增 API 端点 `/api/users`
- 支持多语言切换
```

### Changed（变更）

对现有功能的变更。

**示例**：
```
### Changed
- 修改 API 响应格式
- 更新默认配置参数
- 优化查询性能
```

### Deprecated（废弃）

即将移除的功能。

**示例**：
```
### Deprecated
- API v1 已废弃，请使用 v2
- `old_method()` 已废弃，请使用 `new_method()`
```

### Removed（移除）

已移除的功能。

**示例**：
```
### Removed
- 移除旧的 API 版本
- 删除已废弃的方法
```

### Fixed（修复）

问题修复。

**示例**：
```
### Fixed
- 修复登录失败的问题
- 修复内存泄漏
- 修复数据导出格式错误
```

### Security（安全）

安全相关的更新。

**示例**：
```
### Security
- 修复 SQL 注入漏洞
- 更新依赖包以修复安全漏洞
- 加强密码加密强度
```

---

## Changelog 模板

### 完整模板

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2024-01-15

### Added
- 初始版本发布
- 实现核心功能
- 添加文档

### Changed
- 无

### Deprecated
- 无

### Removed
- 无

### Fixed
- 无

### Security
- 无

[Unreleased]: https://github.com/user/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/user/repo/compare/v0.9.0...v1.0.0
```

### 版本条目模板

```markdown
## [VERSION] - YYYY-MM-DD

### Added
- [变更描述]

### Changed
- [变更描述]

### Deprecated
- [变更描述]

### Removed
- [变更描述]

### Fixed
- [变更描述]

### Security
- [变更描述]
```

---

## 最佳实践

### 1. 保持简洁

✅ 使用简洁、清晰的语言描述变更
✅ 每条变更一行，以 `-` 开头
✅ 避免过于详细的技术细节

❌ 不要写：
```
### Added
- 添加了用户认证功能，使用 JWT 令牌，包含注册、登录、登出、令牌刷新等功能，支持多种登录方式...
```

✅ 应该写：
```
### Added
- 添加用户认证功能（JWT）
- 支持注册、登录、登出
- 支持令牌刷新
```

### 2. 按类型分类

✅ 将变更按类型分类（Added/Changed/Fixed 等）
✅ 每个类型下的变更按重要性排序
✅ 相关变更放在一起

### 3. 及时更新

✅ 每次提交代码时，将变更记录到 Unreleased 部分
✅ 发布新版本时，将 Unreleased 替换为新版本号
✅ 定期检查和更新 Changelog

### 4. 提供链接

✅ 为每个版本号添加 Git 链接
✅ 为重要的变更添加 Issue 或 PR 链接
✅ 方便用户追溯变更来源

### 5. 保持格式一致

✅ 使用统一的格式和命名
✅ 遵循 Keep a Changelog 标准
✅ 保持语言风格一致

### 6. 自动化

✅ 使用脚本自动生成 Changelog
✅ 从 Git log 提取变更记录
✅ 集成到 CI/CD 流程

---

## 自动化工具

### 脚本生成

使用 `scripts/generate_changelog.py` 自动生成 Changelog：

```bash
# 生成新的版本条目
python3 scripts/generate_changelog.py --path ./your-project --version 1.0.0 --type minor

# 从 git log 生成变更记录
python3 scripts/generate_changelog.py --path ./your-project --from-git
```

### Git Commit 规范

为了更好地从 Git log 生成 Changelog，建议遵循以下 Commit 规范：

```
feat: 添加新功能
fix: 修复问题
docs: 更新文档
style: 代码格式调整
refactor: 代码重构
perf: 性能优化
test: 添加测试
chore: 构建/工具链变更
```

---

## 参考资源

- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)