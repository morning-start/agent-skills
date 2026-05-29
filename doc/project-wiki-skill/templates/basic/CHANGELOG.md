# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 待添加的新功能

### Changed
- 待变更的功能

### Deprecated
- 待废弃的功能

### Removed
- 待移除的功能

### Fixed
- 待修复的问题

### Security
- 待修复的安全问题

---

## [2.0.0] - 2024-06-01

### Added
- 多租户支持
- 高级分析功能
- API 网关集成
- 实时协作功能

### Changed
- 迁移到新框架
- 优化数据库性能
- 增强安全性
- 改进用户界面

### Deprecated
- 旧版 API（v1）将在 v3.0.0 中移除

### Removed
- 移除了已废弃的 Python 2.7 支持
- 移除了旧的数据库驱动

### Fixed
- 修复了内存泄漏问题
- 修复了并发竞争条件
- 修复了 XSS 漏洞

### Security
- 升级了依赖包到最新安全版本
- 增强了 CSRF 保护
- 添加了速率限制

---

## [1.0.0] - 2024-01-15

### Added
- 初始版本发布
- 用户认证系统（JWT + OAuth 2.0）
- 基础 CRUD 接口
- 数据可视化功能
- 报告生成功能
- API 文档（Swagger/OpenAPI）
- 单元测试（覆盖率 60%）

### Changed
- 无

### Deprecated
- 无

### Removed
- 无

### Fixed
- 修复了 #123 号问题
- 修复了登录页面在 iOS Safari 上的显示异常
- 修复了数据库查询性能问题（从 500ms 优化到 200ms）

### Security
- 实现了 JWT 认证
- 实现了 RBAC 权限模型
- 实现了 API 限流

---

[Unreleased]: https://github.com/user/repo/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/user/repo/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/user/repo/compare/v0.0.0...v1.0.0
