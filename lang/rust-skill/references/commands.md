# Rust Skills 命令系统

## 内置命令

### 路由命令

| 命令 | 描述 |
|------|------|
| /rust-router | 主路由器，引导到正确技能 |

### 信息命令

| 命令 | 描述 |
|------|------|
| /rust-features [version] | 获取 Rust 版本特性 |
| /crate-info \<crate> | 获取 crate 信息 |
| /docs \<crate> [item] | 获取 API 文档 |

### 动态技能命令

| 命令 | 描述 |
|------|------|
| /sync-crate-skills | 从 Cargo.toml 同步技能 |
| /update-crate-skill \<crate> | 更新特定 crate 技能 |
| /clean-crate-skills | 清理本地 crate 技能 |

## 使用示例

### 获取 Rust 版本特性

```
/rust-features 1.70
```

### 获取 Crate 信息

```
/crate-info tokio
/crate-info serde
```

### 获取 API 文档

```
/docs tokio spawn
/docs std::vec Vec::push
```

### 同步项目依赖技能

```bash
# 进入 Rust 项目
cd my-rust-project

# 同步所有依赖
/sync-crate-skills

# 技能创建在 ~/.claude/skills/{crate}/
```

## 动态技能生成

### 工作原理

```
用户问题
     │
     ▼
┌─────────────────────────────────────────┐
│         Hook Layer                       │
│  解析 Cargo.toml 依赖                    │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│       动态技能生成器                       │
│  从 crate 元数据创建技能                   │
└─────────────────────────────────────────┘
     │
     ▼
项目特定的技能 (如 tokio-skill, serde-skill)
```

### 特性

- **按需生成**: 从 Cargo.toml 依赖创建
- **本地存储**: ~/.claude/skills/
- **版本追踪**: 每个技能记录 crate 版本
- **工作区支持**: 解析所有工作区成员

### 配置文件

```toml
# Skills.toml
[project]
name = "my-rust-project"

[skills.install]
rust-skills = "actionbook/rust-skills"

[security]
trusted_authors = ["ZhangHanDong"]
```
