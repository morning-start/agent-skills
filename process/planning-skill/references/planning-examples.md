# 项目规划真实案例

> 本文档通过 3 个不同规模和类型的项目规划案例（个人项目、小团队产品、企业级系统），展示如何在实际场景中应用 OKR/SMART/Roadmap/TODO 等方法论，帮助用户理解理论到实践的转化。

---

## 案例总览

| # | 项目 | 类型 | 规模 | 核心方法论 | ROADMAP 行数 | TODO 行数 |
|---|------|------|------|-----------|-------------|----------|
| 1 | **个人技能学习计划** | 个人成长 | 1人 | SMART + Eisenhower | ~40行 | ~60行 |
| 2 | **SaaS 产品 v2.0 规划** | 产品开发 | 5人团队 | OKR + MoSCoW + 敏捷Roadmap | ~90行 | ~100行 |
| 3 | **企业平台技术迁移** | 技术架构 | 20人+ | OKR + 技术Roadmap + RICE | ~130行 | ~120行 |

---

## 案例一：个人技能学习计划

### 背景
- **角色**: 全栈开发者
- **目标**: 在 6 个月内掌握 Rust 和 WebAssembly 开发
- **约束**: 工作日晚上 2 小时 + 周末 4 小时

### ROADMAP.md (简化版)

```markdown
# Rust & WASM 学习路线图 (2026 H1 - H2)

## 🎯 目标
成为能独立使用 Rust 编写 Wasm 应用的开发者，
并能贡献于 {specific-project} 的 Wasm 模块。

## 📅 Phase 1: Rust 基础 (3月)

### O1: 掌握 Rust 核心语法和编程范式
- KR1: 完成 "The Rust Programming Language" 前 15 章 (0→15)
- KR2: 完成 50+ Exercises (0→50)
- KR3: 能独立实现小型 CLI 工具 (0→3个)

#### 里程碑
- **M1 (2月底)**: 完成所有权/借用/生命周期理解
- **M2 (3月中)**: 完成 trait/generic/错误处理练习
- **M3 (3月底)**: 通过自测：编写一个 CLI 文件搜索工具

## 📅 Phase 2: 进阶与实战 (4-5月)

### O2: 掌握异步编程和网络开发
- KR1: 完成 async/.await/tokio 练习 (0→20个练习)
- KR2: 实现 1 个 TCP 服务端 (0→1)
- KR3: 实现 1 个 HTTP API (axum/actix) (0→1)

## 📅 Phase 3: Wasm 集成 (6月)

### O3: 能将 Rust 编译为 Wasm 并集成
- KR1: 成功编译 Rust → Wasm (0→✅)
- KR2: 与 JS 互操作调用成功 (0→3个场景)
- KR3: 贡献 {project} 的 Wasm 模块 PR (0→1个merged)

## ⚠️ 风险
- 时间不足 → 减少练习数量，聚焦核心路径
- 学习曲线陡峭 → 寻找社区/Mentor 支持
```

### TODO.md (当前月度)

```markdown
# Rust 学习待办 (2026年3月)

## 🎯 本月重点
完成 Phase 1 O1: 掌握 Rust 核心语法

## 🚀 P0 - 必须完成

- [ ] **阅读**: TRPL 第 8-11 章 (所有权/结构体/枚举)
  - 负责: @me | 截止: 3/10 | 预估: 8h
- [ ] **练习**: Exercises 8-12 (5题)
  - 负责: @me | 截止: 3/14 | 预估: 4h
- [ ] **实践**: 重写之前的 Python CLI 工具的解析模块
  - 负责: @me | 截止: 3/18 | 预估: 10h

## ⭐ P1 - 应该完成

- [ ] **阅读**: TRPL 第 12-15 章 (泛型/Trait/测试)
  - 负责: @me | 截止: 3/25 | 预估: 6h
- [ ] **输出**: 写 3 篇学习笔记到博客
  - 负责: @me | 截止: 3/31 | 预估: 4h

## 💡 Eisenhower 分类

| 任务 | 象限 | 处理方式 |
|------|------|---------|
| 核心章节学习 | I (重要紧急) | 每晚 9-11pm |
| 练习题 | II (重要不紧急) | 周末下午 |
| 博客写作 | III (委托/可延后) | 有灵感时写 |
| 刷技术视频 | IV (删除) | 本月不看 |

## 📈 进度
- 总任务: 7
- 已完成: 0
- 进行中: 2 (TRPL Ch8-11, Exercises 8-12)
- 未开始: 5
```

### 关键学习点
- ✅ 使用 **SMART** 定义每个 KR（如"完成 50+ Exercises"）
- ✅ 使用 **Eisenhower** 分配每日时间（黄金时间给第 I 象限）
- ✅ 使用 **Pomodoro** 进行专注学习（25分钟学习 + 5分钟休息）
- ✅ **每月复盘**一次 ROADMAP（根据实际进度调整下月目标）

---

## 案例二：SaaS 产品 v2.0 规划

### 背景
- **产品**: AI 辅助代码审查 SaaS 平台
- **阶段**: 从 v1.0 (MVP) 迭代到 v2.0 (PMF)
- **团队**: 5 人（1 PM / 1 设计 / 2 后端 / 1 前端）
- **周期**: Q2 2026 (4月-6月)

### ROADMAP.md (功能型)

```markdown
# CodeReview AI v2.0 产品路线图 (Q2 2026)

## 🎯 季度主题
从"能用"到"好用"，提升用户留存率和 NPS。

## ✅ Now (v2.0 - Must Have)

### 发布目标: 2026-05-15

| # | 功能 | MoSCoW | RICE分 | Owner | Status |
|---|------|--------|--------|-------|--------|
| F1 | 多语言支持 (Python/Go/Java) | Must | 80 | @backend-A | 🔄 Dev |
| F2 | IDE 插件 (VSCode/JetBrains) | Must | 75 | @frontend | ⏳ Plan |
| F3 | 团队协作模式 (Org Review) | Must | 70 | @pm | ⬜ Backlog |
| F4 | 性能优化 (< 2s/文件) | Must | 65 | @backend-B | ⬜ |

**Done 标准**: 所有 Must 功能上线 + P0 Bug 清零

## 🔮 Next (v2.1 - Should Have)

### 计划发布: 2026-06-30

| # | 功能 | MoSCoW | RICE分 | 用户需求 |
|---|------|--------|--------|---------|
| N1 | 自定义规则引擎 | Should | 55 | 企业用户 |
| N2 | GitHub/GitLab 深度集成 | Should | 50 | DevOps用户 |
| N3 | 代码度量仪表盘 | Could | 40 | Tech Lead |

## 🌅 Later (v3.0)

- AI 自动修复建议
- 私有化部署 (On-premise)
- 企业 SSO / SAML 集成

## 📍 版本时间轴

```
Apr ──────── May (v2.0) ──── Jun (v2.1) ──── Jul
│            │                  │                │
├─ Sprint 1 ├─ Sprint 2 ├─ Sprint 3 ├─ Sprint 4
│  (F1部分)   │  (F1+F2)    │  (N1+N2)     │
│            │                  │                │
🔧 Alpha     🚀 Beta        📦 RC          🎉 Release
```

## ⚠️ Top 风险
| # | 风险 | 影响 | 概率 | 应对 |
|---|------|------|------|------|
| R1 | IDE API 变更导致插件失效 | 🔴高 | 🟠中 | 提前与厂商沟通 |
| R2 | 多语言支持性能不达标 | 🟠中 | 🟡低 | 先支持 Top 3 语言 |
```

### TODO.md (当前 Sprint)

```markdown
# v2.0 Sprint 2 待办 (4/13 - 4/26)

## 🎯 Sprint Goal
完成多语言支持的 MVP（Python + Go 解析器），并通过内部测试。

## 🚀 P0 - Commit (23pts)

### Backend
- [ ] **S-1**: Python AST 解析器 (@backend-A, 8p, 4/20)
  - DoD: 能解析 Python 3.10+ 语法树，覆盖 95%+ 常用语法
  - Blocker: S-3 (需要 Go parser 先定义接口)

- [ ] **S-2**: Go AST 解析器 (@backend-B, 8p, 4/22)
  - DoD: 能解析 Go 1.21+ 语法树，通过官方 test suite

### Frontend
- [ ] **S-3**: 多语言切换 UI (@frontend, 5p, 4/19)
  - DoD: 支持在 Python/Go/JS 间一键切换视图

### Infra
- [ ] **S-4**: CI 流水线适配多语言 (@devops, 2p, 4/25)
  - DoD: 新增语言的构建/测试步骤

## 🌟 P1 - Stretch (16pts)

- [ ] **S-5**: 语法高亮主题扩展 (@design, 5p)
- [ ] **S-6**: 性能基准测试脚本 (@backend-A, 8p)
- [ ] **S-7**: 文档更新 (API/用户指南) (@pm, 3p)

## 🚧 Blockers
| Task | Blocked By | Resolution |
|------|------------|------------|
| S-1 | S-3 (需要UI展示) | 先做核心逻辑，UI 用 mock 数据 |
| S-3 | Design finalization (4/17) | 推进至 4/18 完成设计 |

## 📊 Burn-down
Total: 39pts | Done: 0 | Remaining: 39 | Days left: 13
Velocity: 35pts/sprint (last sprint) | Forecast: ✅ 可完成
```

### 关键学习点
- ✅ **MoSCoW** 明确区分 Must/Should/Could/Won't
- ✅ **RICE** 在 Should/Could 内部排序（Reach × Impact × Confidence / Effort）
- ✅ **敏捷 Roadmap** 采用 Now-Next-Later 结构
- ✅ **看板 + WIP 限制** (Doing 列 ≤ 3 tasks)
- ✅ **燃尽图** 预测能否按期完成

---

## 案例三：企业平台技术迁移

### 背景
- **系统**: 大型电商订单管理系统（5年老系统）
- **迁移**: Monolith → 微服务架构 (Kubernetes)
- **团队**: 20 人（跨 4 个子团队）
- **周期**: 2026 Q2 - Q3 (6个月)

### ROADMAP.md (技术型，精简版)

```markdown
# OrderSystem 技术迁移路线图 (2026 Q2-Q3)

## 📍 当前状态
• 单体 Java 应用 (Spring Boot)
• MySQL 主库 + Redis 缓存
• 部署在 VM (on-premise)
• 团队: 20 人 (4 sub-teams)

## 🎯 目标状态
• 5 个微服务 (Order/Payment/User/Inventory/Notification)
• PostgreSQL + Redis Cluster
• Kubernetes (AWS EKS)
• 团队: 22 人 (+2 SRE)

## 🗺️ 迁移阶段

### Stage 0: 准备 (3月,已完成 ✅)
- [x] 技术选型 (K8s + Istio + gRPC)
- [x] PoC: 订单服务容器化验证
- [x] 团队 K8s 培训 (100% 完成)

### Stage 1: 基础服务拆分 (4月-5月)
**O1**: 完成订单服务和用户服务的微服务化

| KR | 指标 | 当前 | 目标 | 状态 |
|----|------|------|------|------|
| KR1 | Order Service 容器化率 | 0% | 100% | 🟡 75% |
| KR2 | User Service 容器化率 | 0% | 100% | 🟢 90% |
| KR3 | P99 延迟 < 200ms (vs monolith 800ms) | - | 测量中 |
| KR4 | 可用性 99.9% (SLA) | - | 验证中 |

**里程碑**:
- M1 (4/30): Order Service 生产流量 10%
- M2 (5/15): User Service 生产流量 10%
- M3 (5/31): 双服务并行运行稳定

### Stage 2: 核心服务拆分 (5月-6月)
**O2**: 完成支付、库存、通知服务的微服务化

(类似结构...)

### Stage 3: 收尾与优化 (6月-7月)
**O3**: 完成全量切换和旧系统下线

(类似结构...)

## 🔗 依赖关系
```
[Order Service] ←── 依赖 ──→ [Payment Service] (Stage 2)
       ↑                           ↓
[User Service] ←── 依赖 ──→ [Inventory Service]
                                  ↓
                          [Notification Service]
```

## ⚠️ Top 风险矩阵
| # | 风险 | 类型 | 影响 | 概率 | 缓解方案 |
|---|------|------|------|------|---------|
| R1 | 数据一致性 | 🔴数据 | 🔴高 | 🟠中 | Saga 模式 + 最终一致性 |
| R2 | 团队学习曲线 | 👥人员 | 🟠中 | 🔴高 | 外部顾问 + Pair Programming |
| R3 | 性能回退 | ⚡性能 | 🟡中 | 🟢低 | 金丝雀发布 + 回滚机制 |
| R4 | 网络分区容忍 | 🔗网络 | 🔴高 | 🟡中 | 多可用区部署 |

## 📈 阶段性 OKR 对齐

| 层级 | O | KR | Stage |
|-----|---|-----|-------|
| 公司 | "打造弹性云原生架构" | KR: 云成本降低 30% | All |
| 技术部 | "完成订单域微服务化" | KR: 3个服务上线 | Stage 1-2 |
| 订单组 | "交付高可用订单服务" | KR: 可用性 99.9% | Stage 1-3 |
```

### TODO.md (当前月度 - 精简版)

```markdown
# 迁移项目待办 (2026年5月)

## 🎯 本月重点
完成 Stage 1: Order/User 服务生产流量达到 10%

## 🚀 P0 - 必须完成

### Order Team
- [ ] **T-1**: Order Service K8s Deployment 配置 (@lead-A)
- [ ] **T-2**: Database Migration Script (@DBA)
- [ ] **T-3**: Integration Test Suite (@QA-lead)

### Platform Team (SRE)
- [ ] **T-4**: EKS Cluster Production Setup (@sre-1)
- [ ] **T-5**: Monitoring Stack (Prometheus+Grafana) (@sre-2)
- [ ] **T-6**: CI/CD Pipeline for Microservices (@devops)

### Cross-cutting
- [ ] **T-7**: gRPC Protocol Definition (@architect)
- [ ] **T-8**: Service Mesh (Istio) Config (@network-team)

## 📊 里程碑追踪
| M | 目标 | 计划 | 实际 | 偏差 | 状态 |
|---|------|------|------|------|------|
| M1 | Order 10%流量 | 5/1 | - | - | ⏳ |
| M2 | User 10%流量 | 5/15 | - | - | ⬜ |
| M3 | 双服务稳定运行 | 5/31 | - | - | ⬜ |

## 🚧 关键依赖与阻塞
- T-1 依赖: T-7 (Protocol Definition)
- T-2 依赖: T-4 (Cluster Ready)
- 外部依赖: AWS Support Case #12345 (待响应)

## 📈 健康度仪表盘
| 维度 | 当前 | 目标 | 状态 |
|------|------|------|------|
| 进度 | Stage 1: 25% | 50% by 5/31 | 🟡 |
| 质量 | Unit Test Pass: 92% | > 85% | 🟢 |
| 人员 | Availability: 95% | > 90% | 🟢 |
| 风险 | Open: 2 (R1/R2) | < 3 | 🟡 |
```

### 关键学习点
- ✅ **完整 OKR 三层对齐** (公司→技术部→团队)
- ✅ **技术型 Roadmap** 包含架构依赖图和风险矩阵
- ✅ **跨团队协作** (Order/Platform/QA/Arch 四组协同)
- ✅ **里程碑驱动** (每个 Stage 有明确的 M1/M2/M3)
- ✅ **健康度仪表盘** (5 维度综合评估)

---

## 案例对比总结

| 维度 | 案例1 (个人) | 案例2 (SaaS) | 案例3 (企业) |
|------|-------------|-------------|-------------|
| **方法论** | SMART + Eisenhower | OKR + MoSCoW + 敏捷 | OKR + 技术 Roadmap |
| **ROADMAP** | ~40行 (轻量) | ~90行 (功能型) | ~130行 (技术型) |
| **TODO** | ~60行 (月度) | ~100行 (Sprint) | ~120行 (月度) |
| **跟踪方法** | 手动打勾 | 看板+燃尽图 | 里程碑+仪表盘 |
| **更新频率** | 周 | Sprint (2周) | 月 |
| **复杂度** | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

**文档版本**: v1.0.0  
**最后更新**: 2026-05-17  
**案例来源**: 基于真实项目经验总结（已脱敏处理）
