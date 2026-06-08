---
name: doc-syncer
version: 0.1.1
description: Use when the user needs to synchronize related documents after a change and preserve traceability.
tags: [sync, traceability, documentation]
---

# Doc Syncer

## 职责

- 根据变更影响报告更新文档
- 更新 YAML front matter 中的版本号
- 更新追溯关系
- 确保变更后的文档一致性

## 输入

- change_impact_report
- 现有文档集

## 输出

- 更新后的文档集
- sync_report.yaml

## 同步规则

### 需求变更

1. 更新需求文档中的功能描述
2. 更新架构文档中的对应模块
3. 更新 API 文档中的接口定义
4. 更新测试文档中的测试用例

### 架构变更

1. 更新架构文档
2. 更新 API 文档中的模块结构
3. 更新数据文档中的存储策略
4. 更新运维文档中的部署配置

### API 变更

1. 更新 API 文档
2. 更新测试文档中的接口测试
3. 更新架构文档中的接口说明（如有）

## 同步流程

1. 读取 change_impact_report
2. 按影响文档列表逐个更新
3. 更新 YAML front matter 版本号
4. 更新追溯关系
5. 输出 sync_report.yaml

## 注意事项

- 同步更新不能改变文档整体结构
- 版本号必须与 version-manager 输出一致
- 追溯关系变更后需重新运行一致性检查
- 更新内容需标注变更标记（如 `<!-- CHANGED: ... -->`）
