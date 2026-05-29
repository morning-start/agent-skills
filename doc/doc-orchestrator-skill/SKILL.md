---
name: doc-orchestrator
version: 0.1.0
author: doc-orchestrator
description: 文档编排操盘手，全生命周期管理软件开发文档。从需求分析、文档生成、质量校验到变更维护，支持全规模项目自适应、双轨格式（Agent结构化+人类可读）、智能绘图（TXT/Mermaid自适应）
tags: [documentation, orchestration, lifecycle, quality, automation]
---

# DocOrchestrator - 文档编排操盘手

## 任务目标

- 本 Skill 用于：全生命周期管理软件开发项目的各类文档
- 能力包含：项目分析、文档规划、文档生成、质量校验、变更维护、格式转换、智能绘图、版本管理
- 触发条件：用户需要"创建项目文档"、"生成需求文档"、"画架构图"、"检查文档一致性"、"需求变更分析"、"文档版本管理"等

## 前置准备

### 依赖说明

本 Skill 使用 Python 3.8+ 标准库，核心依赖：
- yaml (PyYAML) - 双轨格式处理
- json - 结构化数据
- pathlib - 路径管理

### 目录结构

```
doc-orchestrator/
├── skills/                    # 阶段协调器 + 执行者
├── references/                # 全局参考
├── templates/                 # 统一模板库
└── scripts/                   # 自动化脚本
```

## 操作步骤

### 标准流程

1. **分析阶段**
   - 调用 `doc-phase-analysis` 分析项目类型、规模、技术栈
   - 输出: `project-profile.yaml`

2. **规划阶段**
   - 调用 `doc-phase-planning` 根据分析结果规划文档清单
   - 输出: `doc-plan.yaml`

3. **生产阶段**
   - 调用 `doc-phase-production` 按规划生成文档族
   - 输出: 完整文档集

4. **质量阶段**
   - 调用 `doc-phase-quality` 进行一致性、完整性检查
   - 输出: `quality-report.yaml`

5. **维护阶段**
   - 调用 `doc-phase-maintenance` 管理版本、变更、同步
   - 输出: 更新后的文档集 + `CHANGELOG.md`

### 快捷路径

- **小项目**: analysis → production → quality（跳过 planning）
- **已有项目**: analysis (scan) → maintenance (sync) → quality
- **仅绘图**: production (diagram-producer)
- **仅校验**: quality

## 资源索引

### 阶段协调器

| 协调器 | 职责 | 路径 |
|--------|------|------|
| doc-phase-analysis | 项目/需求/现状分析 | [查看](skills/doc-phase-analysis/SKILL.md) |
| doc-phase-planning | 文档规划/模板选择 | [查看](skills/doc-phase-planning/SKILL.md) |
| doc-phase-production | 文档生成/绘图 | [查看](skills/doc-phase-production/SKILL.md) |
| doc-phase-quality | 一致性/完整性/评分 | [查看](skills/doc-phase-quality/SKILL.md) |
| doc-phase-maintenance | 版本/变更/同步/导出 | [查看](skills/doc-phase-maintenance/SKILL.md) |

### 全局参考

| 参考文档 | 用途 | 路径 |
|----------|------|------|
| 文档类型目录 | 查看所有支持的文档类型 | [查看](references/doc-types-catalog.md) |
| 双轨格式协议 | Agent与人类格式定义 | [查看](references/dual-track-protocol.md) |
| 智能绘图策略 | TXT/Mermaid选择规则 | [查看](references/diagram-strategy.md) |
| 文档SOLID原则 | 设计原则指南 | [查看](references/solid-doc-principles.md) |
| 模板变量系统 | 模板变量定义 | [查看](references/template-variable-system.md) |
| 质量指标定义 | 评分规则 | [查看](references/quality-metrics.md) |

## 注意事项

- 严格遵循三层架构（根→协调器→执行者），层级深度 ≤ 3
- 所有文档必须包含 YAML front matter（双轨格式）
- 绘图默认智能选择 TXT/Mermaid，根据复杂度自适应
- 变更维护时必须更新追溯链（traceability 字段）
- 质量评分低于阈值时需标注 warning
- 小项目自动裁剪非必要文档

## 使用示例

### 示例 1: 新项目从零生成文档

**输入**: "我有一个电商项目，用 React + Node.js + PostgreSQL，需要完整文档"

**流程**:
1. analysis: 识别为全栈项目，中等规模
2. planning: 规划文档清单（SRS、SAD、API、DB设计、测试策略）
3. production: 按清单生成文档，智能添加图示
4. quality: 校验一致性，输出质量报告
5. maintenance: 建立追溯链，初始化版本

**输出**: 完整文档集 + quality-report.yaml

### 示例 2: 需求变更影响分析

**输入**: "原来的登录改为支持手机号验证码登录，分析影响"

**流程**:
1. maintenance/change-analyzer: 追溯受影响的文档（SRS→SAD→API→测试）
2. maintenance/doc-syncer: 同步更新相关文档
3. quality: 重新校验一致性
4. maintenance/version-manager: 更新版本号

### 示例 3: 快速生成架构图

**输入**: "画一个微服务架构图"

**流程**:
1. analysis/project-analyzer: 确认架构类型
2. production/diagram-producer: 智能选择 Mermaid 生成架构图

## 支持的文档类型

### 需求类
- SRS（软件需求规格说明）
- PRD（产品需求文档）
- 功能需求文档
- 非功能需求文档

### 架构类
- SAD（系统架构设计）
- TDD（技术方案设计）
- 平台专项架构（Web/移动/桌面/游戏）
- 数据流图

### 接口数据类
- API 接口文档
- 数据库设计文档
- 通信协议文档（WebSocket/gRPC/Protobuf）

### 质量运维类
- 测试策略与计划
- 部署运维手册
- 安全合规文档

### 基础类
- README
- CHANGELOG
- CONTRIBUTING

## 质量门禁

| 检查项 | 阈值 |
|--------|------|
| 文档完整性 | ≥ 90% |
| 术语一致性 | 100% |
| 追溯完整性 | 100% 有来源/去向 |
| 双轨格式 | 100% 包含 YAML front matter |
| 图示覆盖率 | ≥ 80%（复杂文档） |
