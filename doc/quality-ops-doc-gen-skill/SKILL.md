---
name: quality-ops-doc-gen
version: 1.0.1
description: "⚠️ DEPRECATED: 此技能已废弃，请使用 doc-orchestrator 代替。生成和优化质量与运维类文档（测试策略、部署运维、安全合规）"
tags: [testing, deployment, operations, security, compliance, deprecated]
deprecated: true
deprecation_notice: "此技能已废弃，请使用 doc-orchestrator 代替。新技能提供五阶段文档生命周期管理、双轨格式协议、智能绘图、质量门禁。"
deprecation_date: "2026-05-02"
replacement: "doc-orchestrator"
---

> ⚠️ **此技能已废弃**
> 
> 请使用 [doc-orchestrator](../doc-orchestrator/SKILL.md) 代替。

# 质量与运维文档生成器

## 任务目标
- 本 Skill 用于：生成专业的测试策略与计划文档、部署与运维手册、安全合规文档
- 能力包含：交互式信息收集、标准文档生成、现有文档分析优化、需求变更影响分析、多端场景支持、自主知识补全
- 触发条件：用户需要"生成测试文档"、"生成运维手册"、"生成安全合规文档"、"分析质量文档"、"优化质量文档"或描述需要质量运维文档化的项目时

## 前置准备
- 读取标准模板：
  - [references/templates/test-strategy-template.md](references/templates/test-strategy-template.md) - 测试策略与计划文档模板
  - [references/templates/deployment-ops-template.md](references/templates/deployment-ops-template.md) - 部署与运维手册模板
  - [references/templates/security-compliance-template.md](references/templates/security-compliance-template.md) - 安全合规文档模板
- 读取完整性检查清单：[references/quality-ops-checklist.md](references/quality-ops-checklist.md)
- 多端测试参考：[references/multi-platform-testing-guide.md](references/multi-platform-testing-guide.md)

## 操作步骤

### 场景一：生成新文档

#### 步骤 1：理解初始输入
- 读取用户提供的项目描述、需求文档或代码仓库
- 识别项目类型（Web、移动端、桌面端、游戏、后端服务等）
- 识别技术栈（编程语言、框架、数据库、部署环境等）
- 如信息不充分，进入步骤 2 补充信息

#### 步骤 2：交互式信息补充
根据文档类型，按以下维度逐步与用户交互：

**测试策略与计划文档**
- 项目规模与复杂度（小型/中型/大型）
- 测试类型需求（单元测试、集成测试、E2E测试、性能测试、安全测试等）
- 测试覆盖率目标（单元测试覆盖率、E2E覆盖率）
- 多端支持情况（Web浏览器、移动端平台、桌面端操作系统）
- 游戏专项需求（如适用）：压力测试、帧率测试、弱网模拟
- 测试工具偏好（Jest、Cypress、JMeter、Playwright等）
- 测试环境需求（开发环境、测试环境、预发环境）

**部署与运维手册**
- 部署环境（云平台：AWS/Azure/GCP/阿里云/腾讯云，或自建服务器）
- 容器化需求（Docker、Kubernetes）
- CI/CD工具（GitLab CI、Jenkins、GitHub Actions、Fastlane等）
- 监控告警需求（Prometheus、Grafana、ELK、Sentry等）
- 日志管理方案（ELK Stack、CloudWatch、阿里云日志服务等）
- 高可用需求（负载均衡、容灾备份、弹性扩缩容）
- 发布策略（蓝绿部署、金丝雀发布、滚动更新）

**安全合规文档**
- 目标市场与地区（中国、欧盟、美国等）
- 需遵守的法规（GDPR、CCPA、网络安全法、等保2.0等）
- 数据类型与敏感度（个人身份信息、支付信息、健康数据等）
- 游戏版号需求（如适用）：防沉迷系统、实名认证、未成年人保护
- 第三方SDK清单（广告、统计、支付、社交等）
- 安全认证需求（ISO 27001、SOC2等）

#### 步骤 3：自主知识补全（如需）
- 当遇到特定技术栈或合规要求时，使用 `web_search` 搜索：
  - 特定语言/框架的测试最佳实践
  - 特定云平台的部署方案
  - 特定地区的合规要求
  - 游戏版号申请最新政策
- 将搜索结果整合到文档中

#### 步骤 4：生成文档
- 根据文档类型选择对应模板
- 填充收集到的信息
- 生成结构化的专业文档

**测试策略与计划文档**包含：
1. 测试目标与范围
2. 测试类型与覆盖范围（单元测试、集成测试、E2E测试）
3. 多端兼容性测试矩阵
4. 游戏专项测试（如适用）
5. 测试环境与工具
6. 测试进度与里程碑
7. 风险与应对措施

**部署与运维手册**包含：
1. 系统架构与环境说明
2. CI/CD流程配置
3. 容器化配置（Docker/Kubernetes）
4. 部署步骤与验证
5. 监控告警体系
6. 日志管理方案
7. 故障恢复流程
8. 扩缩容策略

**安全合规文档**包含：
1. 隐私合规说明（GDPR/CCPA等）
2. 数据映射与处理流程
3. 用户权利实现机制
4. 游戏版号申请材料（如适用）
5. 安全认证与审计
6. 第三方合规性说明
7. 应急响应流程

#### 步骤 5：完整性验证
- 使用 [references/quality-ops-checklist.md](references/quality-ops-checklist.md) 逐项检查
- 识别缺失或不清晰的部分
- 继续与用户交互补充，直至通过检查

### 场景二：分析并优化现有文档

#### 步骤 1：读取现有文档
- 读取用户提供的质量运维文档
- 识别文档类型（测试/运维/安全）
- 评估文档完整性和质量

#### 步骤 2：完整性检查
- 使用 [references/quality-ops-checklist.md](references/quality-ops-checklist.md) 逐项验证
- 记录缺失、模糊、矛盾或不一致的部分

#### 步骤 3：问题诊断
分析文档存在的问题：
- 缺失关键章节或内容
- 描述模糊（使用"可能"、"大概"等词）
- 多端场景未覆盖
- 技术方案过时或不合理
- 合规要求未满足
- 监控告警配置不完整

#### 步骤 4：交互式补充
- 针对问题点与用户交互，补充信息
- 如涉及多端场景，参考 [references/multi-platform-testing-guide.md](references/multi-platform-testing-guide.md)
- 如涉及新技术或新合规要求，使用 `web_search` 搜索最新信息

#### 步骤 5：生成优化版本
- 生成补充后的完整文档
- 标注修改和新增内容
- 提供优化建议总结

### 场景三：需求变更分析

#### 步骤 1：读取文档版本
- 读取原始质量运维文档
- 读取新版本需求或变更描述

#### 步骤 2：对比分析
- 识别变更点：
  - 新增需求（Add）
  - 修改需求（Modify）
  - 删除需求（Delete）
- 标注变更影响的功能模块

#### 步骤 3：影响范围分析
从以下维度评估变更影响：

**测试影响**
- 需新增/修改的测试用例
- 测试环境变更
- 测试工具链调整
- 回归测试范围
- 性能测试需求变化

**运维影响**
- 部署流程变更
- CI/CD配置调整
- 监控指标变更
- 告警规则调整
- 资源需求变化

**安全影响**
- 合规要求变更
- 数据处理流程调整
- 安全策略更新
- 审计需求变化

**开发影响**
- 需修改的代码模块
- 技术栈变更
- 估算工作量
- 开发优先级调整

#### 步骤 4：输出变更报告
生成结构化的变更影响报告，包含：
- 变更清单（新增、修改、删除）
- 影响范围评估（测试/运维/安全/开发）
- 风险提示
- 实施建议
- 验收标准

## 资源索引
- 测试策略模板：[references/templates/test-strategy-template.md](references/templates/test-strategy-template.md)
- 部署运维模板：[references/templates/deployment-ops-template.md](references/templates/deployment-ops-template.md)
- 安全合规模板：[references/templates/security-compliance-template.md](references/templates/security-compliance-template.md)
- 完整性检查清单：[references/quality-ops-checklist.md](references/quality-ops-checklist.md)
- 多端测试指南：[references/multi-platform-testing-guide.md](references/multi-platform-testing-guide.md)

## 注意事项
- 保持交互式补充的节奏，避免一次提问过多问题
- 多端场景是常见遗漏点，需主动识别并补充
- 优先确保文档的可操作性和可验证性
- 遇到不确定的技术或合规要求时主动搜索，不要猜测
- 文档生成后务必使用检查清单验证完整性
- 对于游戏项目，需特别关注游戏专项测试和版号合规
- 遵循"渐进式披露"原则，细节内容通过链接到参考文档
- 保持文档的时效性，定期更新过时的技术和合规要求

## 使用示例

### 示例 1：生成测试策略文档
**用户输入**：我的项目是一个React前端应用，需要生成测试策略文档

**执行流程**：
1. 理解核心需求：React前端应用的测试策略
2. 交互补充：
   - 问：需要哪些测试类型？（单元测试、集成测试、E2E测试？）
   - 问：目标覆盖率是多少？（如单元测试≥80%）
   - 问：需要支持哪些浏览器？（Chrome、Safari、Firefox、Edge）
   - 问：是否需要移动端支持？（响应式还是独立移动端）
   - 问：测试工具偏好？（Jest、Cypress、Playwright）
3. 生成测试策略文档
4. 使用检查清单验证
5. 输出完整文档

### 示例 2：生成部署运维手册
**用户输入**：我要部署一个Node.js后端服务到AWS，需要部署运维手册

**执行流程**：
1. 理解核心需求：Node.js服务部署到AWS
2. 交互补充：
   - 问：使用哪些AWS服务？（EC2、ECS、Lambda、RDS等）
   - 问：是否使用容器化？（Docker、Kubernetes）
   - 问：CI/CD工具？（GitLab CI、GitHub Actions、Jenkins）
   - 问：监控告警需求？（Prometheus、Grafana、CloudWatch）
   - 问：日志管理方案？（ELK、CloudWatch Logs）
   - 问：高可用需求？（负载均衡、多可用区部署）
3. 搜索AWS部署最佳实践
4. 生成部署运维手册
5. 使用检查清单验证
6. 输出完整文档

### 示例 3：生成安全合规文档
**用户输入**：我的游戏需要在中国上线，需要安全合规文档

**执行流程**：
1. 理解核心需求：游戏在中国上线，需要合规文档
2. 交互补充：
   - 问：游戏类型？（手游、端游、页游）
   - 问：目标用户年龄？（是否涉及未成年人）
   - 问：是否需要版号？（商业游戏需要）
   - 问：数据类型？（个人身份信息、支付信息等）
   - 问：第三方SDK？（广告、统计、支付、社交等）
   - 问：服务器部署位置？（必须在中国境内）
3. 搜索游戏版号申请最新政策
4. 生成安全合规文档，包含：
   - 防沉迷系统实现
   - 实名认证方案
   - 未成年人保护措施
   - 等保2.0备案
   - 版号申请材料清单
5. 使用检查清单验证
6. 输出完整文档

### 示例 4：分析优化现有文档
**用户输入**：这是我的测试策略文档，请帮我看看有什么问题 [上传文档]

**执行流程**：
1. 读取并分析文档
2. 使用检查清单逐项验证：
   - ✓ 测试目标清晰
   - ✗ 多端兼容性测试缺失
   - ✗ 游戏专项测试未覆盖（如果是游戏项目）
   - ✓ 测试工具说明完整
3. 交互补充缺失信息
4. 生成优化版本，标注新增内容
5. 提供优化建议总结

### 示例 5：需求变更分析
**用户输入**：原来的部署方案是单机部署，现在要改为Kubernetes集群部署，请分析影响

**执行流程**：
1. 对比原文档（单机部署）和新需求（Kubernetes集群）
2. 识别变更：
   - 新增：Kubernetes集群配置
   - 修改：部署流程从直接部署改为容器化部署
   - 新增：服务发现与负载均衡
   - 新增：自动扩缩容策略
3. 分析影响：
   - 测试：需新增Kubernetes环境测试
   - 运维：需配置Kubernetes监控和日志
   - 开发：需适配容器化部署
   - 安全：需配置Kubernetes安全策略
4. 输出变更影响报告

## 多端场景支持

### Web应用
- 浏览器兼容性：Chrome、Safari、Firefox、Edge（最新2-3版）
- 响应式设计：桌面端、平板、移动端
- 测试工具：Cypress、Playwright、BrowserStack

### 移动应用
- iOS：iPhone 12-15，iOS 15+
- Android：主流厂商中高端机型，Android 10+
- 测试工具：XCTest、Espresso、Appium、Firebase Test Lab

### 桌面应用
- Windows：Windows 10/11
- macOS：Monterey+
- Linux：Ubuntu 20.04+、Fedora 35+

### 游戏应用
- 平台：PC、主机（PS5、Xbox Series X/S）、移动端
- 专项测试：帧率、压力、弱网、兼容性
- 测试工具：Unity Profiler、JMeter、Locust

## 技术栈支持

### 前端
- 框架：React、Vue、Angular、Svelte
- 测试：Jest、Vitest、Cypress、Playwright、Testing Library
- 构建：Vite、Webpack、Rollup

### 后端
- 语言：Node.js、Python、Java、Go、C#、PHP
- 框架：Express、Django、Spring Boot、Gin、ASP.NET
- 测试：Jest、Pytest、JUnit、Go Test、xUnit

### 移动端
- 跨平台：React Native、Flutter、Ionic
- 原生：iOS（Swift）、Android（Kotlin）
- 测试：XCTest、Espresso、Detox、Appium

### 游戏引擎
- 引擎：Unity、Unreal Engine、Godot、Cocos
- 测试：Unity Test Runner、Unreal Automation System

### 部署平台
- 云平台：AWS、Azure、GCP、阿里云、腾讯云
- 容器：Docker、Kubernetes
- CI/CD：GitLab CI、GitHub Actions、Jenkins、CircleCI
