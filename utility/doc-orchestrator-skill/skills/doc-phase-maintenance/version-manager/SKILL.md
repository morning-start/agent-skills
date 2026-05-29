---
name: version-manager
version: 0.1.0
description: 管理文档版本号，语义化版本控制，生成 CHANGELOG
---

# Version Manager

## 职责

- 根据变更类型自动计算新版本号
- 更新所有文档的 YAML front matter 版本号
- 生成 CHANGELOG 条目
- 维护版本历史

## 输入

- 变更类型（新增/修改/删除）
- 现有版本号

## 输出

```yaml
version_update:
  previous_version: "1.0.0"
  new_version: "1.1.0"
  change_type: minor
  changelog_entry: |
    ## [1.1.0] - 2026-05-02
    ### Added
    - 新增手机号验证码登录功能
    - 新增短信验证码接口
    
    ### Changed
    - 更新用户认证流程说明
```

## 版本计算规则

| 变更类型 | 规则 | 示例 |
|----------|------|------|
| 新增文档 | MINOR +1 | 1.0.0 → 1.1.0 |
| 修改文档内容 | PATCH +1 | 1.0.0 → 1.0.1 |
| 删除文档 | MAJOR +1 | 1.0.0 → 2.0.0 |
| 架构重大变更 | MAJOR +1 | 1.0.0 → 2.0.0 |

## CHANGELOG 格式

```markdown
# 变更日志

## [1.1.0] - 2026-05-02

### Added
- 新增手机号验证码登录功能

### Changed
- 更新用户认证流程说明

### Fixed
- 修复认证文档中的错误码描述

### Removed
- 移除废弃的密码登录方式说明
```

## 注意事项

- 版本号必须在所有文档中一致
- CHANGELOG 按时间倒序排列
- 变更类型分类：Added/Changed/Fixed/Removed/Deprecated/Security
- 日期格式：YYYY-MM-DD
