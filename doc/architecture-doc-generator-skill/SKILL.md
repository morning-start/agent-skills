---
name: architecture-doc-generator
version: 1.0.1
author: skill-manager
description: "⚠️ DEPRECATED: 此技能已废弃，请使用 doc-orchestrator 代替。根据SRS/PRD生成SAD/TDD/平台架构文档"
tags: [architecture, documentation, SAD, TDD, design, deprecated]
deprecated: true
deprecation_notice: "此技能已废弃，请使用 doc-orchestrator 代替。新技能提供五阶段文档生命周期管理、双轨格式协议、智能绘图、质量门禁。"
deprecation_date: "2026-05-02"
replacement: "doc-orchestrator"
---

> ⚠️ **此技能已废弃**
> 
> 请使用 [doc-orchestrator](../doc-orchestrator/SKILL.md) 代替。

# 架构设计文档生成器

## 任务目标

- 本 Skill 用于：根据 SRS（软件需求规格说明）和 PRD（产品需求文档）生成专业的架构与设计类文档
- 能力包含：
  - 生成系统架构设计文档（SAD）：描述系统整体结构、技术选型、多端协同策略
  - 生成技术方案设计文档（TDD）：定义模块边界、接口契约、数据流转逻辑
  - 生成平台专项架构文档：针对前端、移动端、桌面端、游戏等平台的专项架构设计
- 触发条件：用户需要生成架构设计文档、分析现有文档、或进行需求变更分析时使用

## 操作步骤

### 标准流程

1. **输入/准备**
   - 用户提供 SRS 或 PRD 文档路径
   - 读取并分析需求文档，提取关键信息（业务目标、功能需求、非功能性需求、技术约束）
   - 识别文档类型，确定需要生成的架构文档类型

2. **执行/处理**
   - 根据需求类型选择合适的文档模板（SAD/TDD/平台专项）
   - 收集并补充技术栈信息（必要时使用 web_search 搜索相关技术选型和最佳实践）
   - 与用户交互澄清不明确的需求或技术偏好
   - 根据选定的模板结构，结合需求文档内容生成完整文档
   - 确保包含所有核心章节：架构概述、技术选型、模块设计、数据模型、安全设计等
   - 生成架构图、时序图、ER图等可视化描述（使用 Mermaid 语法或文字描述）

3. **输出/校验**
   - 检查文档完整性和一致性
   - 确保技术选型的合理性（性能、可维护性、团队熟悉度）
   - 根据用户反馈进行迭代优化
   - 输出最终文档

## 资源索引

- 系统架构设计文档模板：见 [references/sad-template.md](references/sad-template.md)（何时读取：生成系统整体架构设计文档时）
- 技术方案设计文档模板：见 [references/tdd-template.md](references/tdd-template.md)（何时读取：生成具体功能模块的技术方案时）
- 前端架构设计文档：见 [references/web-platform.md](references/web-platform.md)（何时读取：生成前端架构设计时）
- 移动端架构设计文档：见 [references/mobile-platform.md](references/mobile-platform.md)（何时读取：生成移动端架构设计时）
- 桌面端架构设计文档：见 [references/desktop-platform.md](references/desktop-platform.md)（何时读取：生成桌面端架构设计时）
- 游戏架构设计文档：见 [references/game-platform.md](references/game-platform.md)（何时读取：生成游戏架构设计时）

## 注意事项

- 确保生成的文档包含所有必需章节，避免遗漏关键设计点
- 技术选型应基于实际需求，避免过度设计或技术栈过于复杂
- 架构设计应与需求文档保持一致，关键设计决策应说明依据
- 优先选择团队熟悉、生态成熟的技术方案
- 特别关注认证授权、数据加密、防攻击等安全设计
- 遵循行业标准和规范，使用统一的文档格式和术语
- 架构图、时序图等应清晰易懂，标注关键组件和数据流向
- 使用 web_search 补充技术栈信息时，确保信息的时效性和准确性

## 使用示例

### 示例 1：生成系统架构设计文档

**输入**：用户提供电商系统的 PRD 文档，包含用户管理、商品管理、订单管理、支付等核心功能

**执行**：
1. 读取并分析 PRD 文档，提取关键信息（业务目标、功能需求、非功能性需求）
2. 识别为复杂系统，选择生成 SAD 文档
3. 参考 [references/sad-template.md](references/sad-template.md) 模板结构
4. 设计微服务架构模式，规划服务拆分（用户服务、商品服务、订单服务、支付服务）
5. 选择技术栈（Spring Boot、MySQL、Redis、Kafka）
6. 设计多端协同策略（BFF 层、API Gateway）
7. 生成架构图和时序图

**输出**：完整的系统架构设计文档，包含系统拓扑图、技术选型说明、服务划分、接口定义、数据模型、安全设计等章节

### 示例 2：生成技术方案设计文档

**输入**：用户提供用户认证模块的功能需求，包括注册、登录、密码重置、权限管理

**执行**：
1. 读取并分析功能需求
2. 识别为具体功能模块，选择生成 TDD 文档
3. 参考 [references/tdd-template.md](references/tdd-template.md) 模板结构
4. 定义模块边界和职责（认证服务、授权服务）
5. 设计 RESTful API 接口（/api/auth/login、/api/auth/register、/api/auth/reset-password）
6. 设计数据模型（User、Role、Permission 表）
7. 设计安全方案（JWT 认证、RBAC 授权、密码加密）
8. 生成 ER 图和时序图

**输出**：完整的技术方案设计文档，包含模块划分、接口定义、数据模型、安全策略、异常处理等章节

### 示例 3：生成移动端架构设计文档

**输入**：用户提供跨平台移动应用的需求，包含 iOS 和 Android 双端支持

**执行**：
1. 读取并分析移动应用需求
2. 识别为移动端项目，选择生成移动端架构设计文档
3. 参考 [references/mobile-platform.md](references/mobile-platform.md) 模板结构
4. 选择开发模式（Flutter，理由：一次开发双端运行，性能接近原生）
5. 设计推送服务集成方案（APNs for iOS、FCM for Android、厂商通道）
6. 设计权限管理策略（动态申请、隐私合规）
7. 规划包体积优化方案（资源压缩、动态下发）
8. 设计离线缓存和数据同步策略

**输出**：完整的移动端架构设计文档，包含开发模式选择、推送服务、权限管理、性能优化、安全设计等章节
