---
name: doc-phase-maintenance
version: 0.1.0
description: 维护阶段协调器，负责变更分析、文档同步、版本管理和导出管理
---

# Maintenance Phase Coordinator

## 职责

- 分析变更影响范围
- 同步更新相关文档
- 管理版本号和变更日志
- 支持多格式导出

## 子技能

| 执行者 | 职责 | 路径 |
|--------|------|------|
| change-analyzer | 变更影响分析 | [查看](change-analyzer/SKILL.md) |
| doc-syncer | 文档同步更新 | [查看](doc-syncer/SKILL.md) |
| version-manager | 版本管理 | [查看](version-manager/SKILL.md) |
| export-manager | 导出管理 | [查看](export-manager/SKILL.md) |

## 输入

- 变更描述或新版本文档
- 现有文档集

## 输出

- 更新后的文档集
- CHANGELOG.md
- 可选：导出文件（PDF/HTML/ZIP）

## 工作流程

1. 读取变更描述
2. 调用 change-analyzer 分析影响范围
3. 调用 doc-syncer 同步更新受影响文档
4. 调用 version-manager 更新版本号
5. 可选：调用 export-manager 导出
6. 输出更新后的文档集

## 变更分析维度

| 维度 | 内容 |
|------|------|
| 需求影响 | 功能增减、优先级变化 |
| 架构影响 | 模块变更、技术栈调整 |
| API 影响 | 接口新增/修改/删除 |
| 数据影响 | 表结构变更、协议变更 |
| 测试影响 | 测试用例新增/修改 |
| 运维影响 | 部署流程、监控配置 |

## 版本管理规则

### 语义化版本

```
主版本号.次版本号.修订号
MAJOR.MINOR.PATCH
```

| 变更类型 | 版本变更 | 示例 |
|----------|---------|------|
| 新增文档 | MINOR +1 | 1.0.0 → 1.1.0 |
| 修改文档内容 | PATCH +1 | 1.0.0 → 1.0.1 |
| 删除文档 | MAJOR +1 | 1.0.0 → 2.0.0 |
| 初始版本 | - | 1.0.0 |

## 注意事项

- 变更分析必须追溯完整链路
- 同步更新必须保持追溯关系一致
- 版本号必须在所有文档的 YAML front matter 中同步
- CHANGELOG 必须包含日期、变更类型、描述
