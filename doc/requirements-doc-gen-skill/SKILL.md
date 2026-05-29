---
name: requirements-doc-gen
version: 1.0.1
description: "⚠️ DEPRECATED: 此技能已废弃，请使用 doc-orchestrator 代替。将粗糙业务描述转化为标准SRS/PRD文档，支持需求变更分析、多端需求管理"
tags: [requirement, documentation, SRS, PRD, deprecated]
deprecated: true
deprecation_notice: "此技能已废弃，请使用 doc-orchestrator 代替。新技能提供五阶段文档生命周期管理、双轨格式协议、智能绘图、质量门禁、变更追溯链。"
deprecation_date: "2026-05-02"
replacement: "doc-orchestrator"
---

> ⚠️ **此技能已废弃**
> 
> 请使用 [doc-orchestrator](../doc-orchestrator/SKILL.md) 代替。

# 需求文档生成器

## 任务目标
- 本 Skill 用于：将粗糙的业务描述转化为专业的需求规格说明书（SRS）和产品需求文档（PRD）
- 能力包含：交互式需求收集、标准文档生成、现有文档分析优化、需求变更影响分析、多端需求管理
- 触发条件：用户需要"生成需求文档"、"分析需求文档"、"优化需求文档"、"需求变更分析"或描述一个需要文档化的项目时

## 前置准备
- 读取标准模板：[references/srs-template.md](references/srs-template.md) 和 [references/prd-template.md](references/prd-template.md)
- 读取完整性检查清单：[references/requirements-checklist.md](references/requirements-checklist.md)
- 多端开发参考：[references/multi-platform-guide.md](references/multi-platform-guide.md)

## 操作步骤

### 场景一：生成新文档

#### 步骤 1：理解初始输入
- 读取用户提供的粗糙描述（文本或文档）
- 识别核心业务场景和目标
- 如信息不充分，进入步骤 2 补充信息

#### 步骤 2：交互式需求补充
按以下维度逐步与用户交互，补充关键信息：

**基础信息**
- 项目背景与业务目标
- 目标用户画像（User Persona）
- 核心用户场景（User Journey）
- 项目范围与边界

**功能需求**
- 使用 MoSCoW 法则梳理功能清单：
  - Must-have（必须实现）
  - Should-have（应该实现）
  - Could-have（可以实现）
  - Won't-have（暂不实现）
- 核心功能点说明（输入、处理逻辑、输出、异常）

**非功能需求**
- 性能指标（响应时间、并发量、可用性）
- 安全要求（数据加密、权限控制、合规性）
- 兼容性要求（浏览器版本、操作系统版本）

**多端策略**
- 支持的终端类型（Web、移动端、桌面端、游戏端）
- 各端功能差异说明
- UI/UX 适配策略（响应式 vs 原生）

#### 步骤 3：生成 SRS 文档
- 基于 [references/srs-template.md](references/srs-template.md) 模板
- 填充技术性需求细节：
  - 系统架构说明
  - 接口需求（API/SDK）
  - 数据模型
  - 技术约束
  - 测试要求

#### 步骤 4：生成 PRD 文档
- 基于 [references/prd-template.md](references/prd-template.md) 模板
- 填充业务性需求细节：
  - 用户旅程图
  - 交互流程说明
  - 原型描述
  - 数据埋点需求

#### 步骤 5：完整性验证
- 使用 [references/requirements-checklist.md](references/requirements-checklist.md) 逐项检查
- 识别缺失或不清晰的部分
- 继续与用户交互补充，直至通过检查

#### 步骤 6：自主知识补全（如需）
- 当遇到特定领域知识不足时（如 GDPR 合规、游戏引擎限制等）
- 使用 `web_search` 搜索相关规范和最佳实践
- 将搜索结果整合到文档中

### 场景二：分析并优化现有文档

#### 步骤 1：读取现有文档
- 读取用户提供的 SRS 或 PRD 文档
- 识别文档类型和完整性

#### 步骤 2：完整性检查
- 使用 [references/requirements-checklist.md](references/requirements-checklist.md) 逐项验证
- 记录缺失、模糊、矛盾或不一致的部分

#### 步骤 3：问题诊断
- 分析文档存在的问题：
  - 缺失关键章节
  - 描述模糊（使用"可能"、"大概"等词）
  - 多端需求未明确
  - 非功能需求缺失
  - 功能需求不可验证

#### 步骤 4：交互式补充
- 针对问题点与用户交互，补充信息
- 如涉及多端需求，参考 [references/multi-platform-guide.md](references/multi-platform-guide.md)

#### 步骤 5：生成优化版本
- 生成补充后的完整文档
- 标注修改和新增内容
- 提供优化建议总结

### 场景三：需求变更分析

#### 步骤 1：读取文档版本
- 读取原始需求文档
- 读取新版本需求文档

#### 步骤 2：对比分析
- 识别变更点：
  - 新增需求（Add）
  - 修改需求（Modify）
  - 删除需求（Delete）
- 标注变更影响的功能模块

#### 步骤 3：影响范围分析
从以下维度评估变更影响：

**技术影响**
- 架构设计变更
- 接口修改（API 参数增减、返回值变化）
- 数据模型调整
- 技术依赖变更

**开发影响**
- 需修改的代码模块
- 估算工作量
- 开发优先级调整

**测试影响**
- 需新增/修改的测试用例
- 回归测试范围
- 性能测试需求

**用户体验影响**
- 界面交互变更
- 操作流程调整
- 用户习惯迁移成本

#### 步骤 4：输出变更报告
生成结构化的变更影响报告，包含：
- 变更清单（新增、修改、删除）
- 影响范围评估
- 风险提示
- 实施建议

## 资源索引
- SRS 模板：[references/srs-template.md](references/srs-template.md)
- PRD 模板：[references/prd-template.md](references/prd-template.md)
- 完整性检查清单：[references/requirements-checklist.md](references/requirements-checklist.md)
- 多端开发指南：[references/multi-platform-guide.md](references/multi-platform-guide.md)

## 注意事项
- 保持交互式补充的节奏，避免一次提问过多问题
- 多端需求是常见遗漏点，需主动识别并补充
- 优先确保需求的可验证性和无歧义性
- 遇到不确定的领域知识时主动搜索，不要猜测
- 文档生成后务必使用检查清单验证完整性
- 遵循"渐进式披露"原则，细节内容通过链接到参考文档

## 使用示例

### 示例 1：从粗糙描述生成需求文档
**用户输入**：我要做一个在线考试系统，支持学生考试、老师出题、管理员管理

**执行流程**：
1. 理解核心需求：在线考试系统，角色为学生、老师、管理员
2. 交互补充：
   - 问：支持哪些题型？（单选、多选、判断、填空、编程等）
   - 问：考试模式？（限时/不限时、单次/多次、随机抽题等）
   - 问：多端需求？（Web 端、移动端？）
   - 问：性能要求？（最大并发用户数？）
3. 生成 SRS 和 PRD 文档
4. 使用检查清单验证
5. 输出完整文档

### 示例 2：分析优化现有文档
**用户输入**：这是我的 PRD 文档，请帮我看看有什么问题 [上传文档]

**执行流程**：
1. 读取并分析文档
2. 使用检查清单逐项验证：
   - ✓ 功能清单完整
   - ✗ 非功能需求缺失
   - ✗ 多端差异未明确
   - ✓ 用户旅程清晰
3. 交互补充缺失信息
4. 生成优化版本，标注新增内容

### 示例 3：需求变更分析
**用户输入**：原来的需求是 Web 端应用，现在要增加移动端支持，请分析影响

**执行流程**：
1. 对比原文档（仅 Web）和新需求（Web + 移动端）
2. 识别变更：
   - 新增：移动端适配需求
   - 修改：接口需支持多端调用
   - 新增：响应式布局要求
3. 分析影响：
   - 技术：前端架构需调整，API 需适配多端
   - 开发：增加移动端开发工作
   - 测试：需新增移动端测试环境
   - 用户体验：需考虑多端一致性
4. 输出变更影响报告
