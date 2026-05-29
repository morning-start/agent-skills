# 文档 SOLID 原则

本文档将 SOLID 设计原则应用于文档体系设计，确保文档结构清晰、可维护、可扩展。

## S - 单一职责原则 (Single Responsibility)

### 原则

每份文档只负责一个维度的描述，每个子技能只处理一类文档。

### 在文档中的应用

| 文档 | 职责 | 不包含 |
|------|------|--------|
| SRS | 技术需求 | 产品设计、UI 描述 |
| PRD | 产品需求 | 技术实现细节 |
| SAD | 系统架构 | 代码实现细节 |
| TDD | 技术方案 | 系统整体架构 |
| API | 接口定义 | 业务逻辑说明 |

### 在技能中的应用

| 子技能 | 职责 | 不处理 |
|--------|------|--------|
| requirements-producer | 需求文档 | API、架构文档 |
| architecture-producer | 架构文档 | 测试、运维文档 |
| api-producer | API 文档 | 需求、数据文档 |
| consistency-checker | 一致性检查 | 完整性检查 |
| completeness-checker | 完整性检查 | 一致性检查 |

### 违反示例

```
❌ 错误：在 API 文档中包含业务需求描述
✅ 正确：API 文档只描述接口定义，业务需求在 PRD 中
```

## O - 开闭原则 (Open-Closed)

### 原则

文档体系对扩展开放（新增文档类型），对修改封闭（不改变现有文档结构）。

### 在文档中的应用

- 新增文档类型：在 doc-types-catalog 中添加新类型，不修改现有文档
- 新增平台专项：添加新的平台架构文档，不改变通用架构文档
- 新增模板：在 templates/ 中添加新模板，不修改现有模板

### 在技能中的应用

```
新增 security-gen 子技能：
  ✅ 添加 skills/doc-phase-production/security-producer/
  ❌ 修改 architecture-producer 包含安全内容
```

## L - 里氏替换原则 (Liskov Substitution)

### 原则

同类文档的子类型可以互相替换，不改变文档体系的行为。

### 在文档中的应用

所有文档遵循统一的双轨格式协议：
- SRS 和 PRD 都是 requirement 类型，使用相同的 YAML front matter
- RESTful API 和 GraphQL API 都是 api 类型，遵循相同的文档结构
- 任何 requirement 子类型可被 requirement 类型的消费者处理

### 示例

```yaml
# SRS 文档
doc:
  id: "REQ-001"
  type: "requirement"
  subtype: "srs"

# PRD 文档
doc:
  id: "REQ-002"
  type: "requirement"
  subtype: "prd"

# architecture-producer 可以处理任意 requirement 子类型
depends_on: ["REQ-001"]  # 或 ["REQ-002"]
```

## I - 接口隔离原则 (Interface Segregation)

### 原则

文档消费者不需要依赖不需要的文档字段。

### 在文档中的应用

YAML front matter 分为：
- 必填字段：所有文档必须包含
- 可选字段：按需使用

### 字段分组

| 分组 | 字段 | 使用者 |
|------|------|--------|
| 核心 | id, type, version, status | 所有消费者 |
| 追溯 | traceability | consistency-checker, change-analyzer |
| 质量 | quality | quality-scorer |
| 元数据 | metadata | doc-planner, template-selector |

### 违反示例

```
❌ 错误：api-producer 依赖 quality 字段
✅ 正确：api-producer 只依赖核心字段和 metadata
```

## D - 依赖倒置原则 (Dependency Inversion)

### 原则

高层模块（路由引擎）不依赖低层模块（具体文档生成器），两者都依赖抽象（文档类型定义）。

### 在文档中的应用

```
路由引擎 → 文档类型抽象 ← 具体生成器
   │                          │
   └── 不直接调用 ──────────────┘
```

### 抽象定义

```yaml
# 文档类型抽象（doc-types-catalog.md）
document_type:
  id_prefix: string
  required_sections: string[]
  depends_on_types: string[]
  feeds_into_types: string[]
```

### 具体实现

```yaml
# 具体文档类型
requirement/srs:
  id_prefix: "REQ"
  required_sections: ["功能需求", "非功能需求"]
  depends_on_types: []
  feeds_into_types: ["architecture"]
```

### 优势

- 新增文档类型只需在目录中添加，不修改路由引擎
- 更换生成器实现不影响上层逻辑
- 文档体系可独立演进

## 检查清单

在新增或修改文档/技能时，检查是否遵循 SOLID 原则：

- [ ] **S**: 文档/技能是否只负责一个职责？
- [ ] **O**: 是否可以扩展而不需要修改现有内容？
- [ ] **L**: 同类文档/技能是否可以互相替换？
- [ ] **I**: 是否避免了不必要的依赖？
- [ ] **D**: 是否依赖抽象而非具体实现？
