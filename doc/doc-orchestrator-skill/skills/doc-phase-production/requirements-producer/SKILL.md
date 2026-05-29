---
name: requirements-producer
version: 0.1.0
description: 生成需求类文档（SRS、PRD、功能需求、非功能需求）
---

# Requirements Producer

## 职责

- 根据模板生成 SRS 文档
- 根据模板生成 PRD 文档
- 生成功能需求说明文档
- 生成非功能需求说明文档
- 为文档添加追溯关系

## 输入

- 模板路径（templates/requirements/）
- 项目 profile
- 需求解析结果

## 输出

- SRS 文档
- PRD 文档
- 需求追溯矩阵

## SRS 文档结构

```markdown
---
doc:
  id: "REQ-001"
  type: "requirement"
  subtype: "srs"
  version: "1.0.0"
  status: "draft"
  traceability:
    depends_on: []
    feeds_into: ["ARCH-001"]
---

# 软件需求规格说明书

## 1. 引言
- 目的、范围、定义、参考资料

## 2. 系统概述
- 系统背景、目标、约束

## 3. 功能需求
- 按模块列出功能需求
- 每个功能：输入、处理、输出、异常

## 4. 非功能需求
- 性能、安全、可用性、兼容性

## 5. 接口需求
- 外部接口、内部接口

## 6. 数据需求
- 数据存储、传输、格式

## 7. 约束与假设
- 技术约束、业务约束、假设条件

## 8. 附录
- 术语表、参考文档
```

## PRD 文档结构

```markdown
---
doc:
  id: "REQ-002"
  type: "requirement"
  subtype: "prd"
  version: "1.0.0"
  status: "draft"
  traceability:
    depends_on: []
    feeds_into: ["ARCH-001"]
---

# 产品需求文档

## 1. 产品概述
- 产品定位、目标用户、核心价值

## 2. 用户画像
- 角色定义、特征、痛点

## 3. 用户旅程
- 关键场景、流程、触点

## 4. 功能清单
- 按优先级排序的功能列表
- MoSCoW 分类

## 5. 交互设计
- 信息架构、页面流程、组件说明

## 6. 数据埋点
- 关键指标、埋点位置

## 7. 成功指标
- 业务指标、技术指标
```

## 注意事项

- SRS 侧重技术视角，PRD 侧重业务视角
- 功能需求必须包含验收标准
- 非功能需求必须可量化
- 追溯关系 feeds_into 指向架构文档
