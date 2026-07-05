# 架构设计文档

## 系统概述
- **系统名称**：<系统名称>
- **架构类型**：<如：单体应用、分层架构等>
- **设计目标**：<设计目标概述>
- **文档版本**：v1.0.0
- **Python 版本要求**：3.11+
- **包管理工具**：UV
- **项目规模**：<小项目/大项目>

## 项目规模与组织方式

### 规模评估
- **项目规模**：<小项目/中型项目/大项目>
- **功能点数量**：<数量>
- **预期代码行数**：<行数>
- **复杂度评估**：<低/中/高>

### 组织方式选择

#### 小项目（< 5 个功能点）
```
project/
├── main.py                 # 主程序（所有代码）
├── pyproject.toml         # UV 配置
├── uv.lock                # 依赖锁定
├── README.md              # 项目说明（根目录）
└── docs/                  # 文档文件夹
    ├── requirements.md
    ├── architecture.md
    └── background.md
```

#### 大项目（> 5 个功能点）
```
project/
├── README.md              # 项目说明（根目录）
├── pyproject.toml         # UV 配置
├── uv.lock                # 依赖锁定
├── src/                   # 源代码
│   ├── __init__.py
│   ├── main.py           # 主入口
│   ├── api/              # API 模块
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models/           # 数据模型
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── services/         # 业务逻辑
│   │   ├── __init__.py
│   │   └── weather.py
│   ├── repositories/     # 数据访问层（Repository）
│   │   ├── __init__.py
│   │   ├── base.py       # 基础接口
│   │   ├── user_repo.py  # 具体实现
│   │   └── factory.py    # 工厂
│   └── utils/            # 工具函数
│       ├── __init__.py
│       └── helpers.py
├── tests/                 # 测试
│   ├── __init__.py
│   └── test_main.py
└── docs/                  # 文档
    ├── requirements.md
    ├── architecture.md
    ├── background.md
    ├── database-design.md    # 数据库设计
    └── data-abstraction.md   # 数据层抽象
```

### 当前选择
**本项目采用**：<小项目/大项目>架构

**选择理由**：<基于功能点数量、复杂度、未来扩展性>

---

## 版本控制策略
- **版本规范**：使用语义化版本（Semantic Versioning，vX.Y.Z）
  - X：主版本号（不兼容的 API 修改）
  - Y：次版本号（向下兼容的功能性新增）
  - Z：修订号（向下兼容的问题修正）
- **依赖版本锁定**：使用 UV 的 uv.lock 文件
  - 锁定所有依赖的精确版本
  - 确保环境可复现性
  - 自动生成，不可手动编辑
- **版本更新策略**：
  - 主版本更新：必须经过充分测试和审查
  - 次版本更新：向下兼容，可以使用 `uv lock --upgrade`
  - 修订版本更新：通常可以自动更新

---

## 技术选型
### 核心技术栈
- **编程语言**：Python 3.11+ - 选择理由：<性能、类型注解、现代语法特性>
- **框架/库**：<框架名称及版本> - 选择理由：<详细理由>
- **数据库**：<数据库类型及版本> - 选择理由：<理由>
- **包管理**：UV - 选择理由：快速、可靠、现代化
- **其他工具**：<工具列表>

### 技术选型理由（详细对比）
#### 选型对比表
| 维度 | 方案A | 方案B | 最终选择 |
|------|-------|-------|----------|
| 性能 | <评估> | <评估> | <方案> |
| 学习曲线 | <简单/复杂> | <简单/复杂> | <方案> |
| 生态系统 | <丰富/有限> | <丰富/有限> | <方案> |
| 文档质量 | <评估> | <评估> | <方案> |
| 社区支持 | <活跃/一般> | <活跃/一般> | <方案> |
| Python 3.11+ 支持 | ✅/⚠️/❌ | ✅/⚠️/❌ | <方案> |
| 长期维护性 | <活跃/停滞> | <活跃/停滞> | <方案> |
| 类型注解支持 | <完整/部分/不支持> | <完整/部分/不支持> | <方案> |
| UV 兼容性 | ✅/⚠️/❌ | ✅/⚠️/❌ | <方案> |

#### 选型权衡分析
- **最终选择**：<方案名称>
- **选择理由**：
  1. <理由1，引用对比数据>
  2. <理由2，引用对比数据>
  3. <理由3，引用对比数据>
- **权衡说明**：
  - 性能 vs 易用性：选择 <方案> 是因为 <理由>
  - 功能 vs 复杂度：选择 <方案> 是因为 <理由>
  - 生态系统 vs 创新性：选择 <方案> 是因为 <理由>
- **已知不足**：<选择方案的局限性或不足>
- **不推荐场景**：<何种情况下不适用此方案>

### UV 依赖管理
#### pyproject.toml 配置
```toml
[project]
name = "project-name"
version = "1.0.0"
description = "项目描述"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
    # 数据库依赖
    "sqlalchemy>=2.0.0",  # PostgreSQL/SQLite
    "psycopg2-binary>=2.9.0",  # PostgreSQL 驱动
    # "pymongo>=4.0.0",  # MongoDB
    # "chromadb>=0.4.0",  # ChromaDB
    # "pgvector-python>=0.2.0",  # pgvector
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
    "alembic>=1.12.0",  # 数据库迁移
    "mongomock>=4.0.0",  # MongoDB Mock
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
]
```

#### 依赖管理策略
- **核心依赖**：锁定版本，使用 `uv add package`
- **开发依赖**：使用 `uv add --dev package`
- **更新策略**：定期运行 `uv lock --upgrade`
- **兼容性检查**：使用 `uv check` 验证依赖兼容性

---

## 系统架构
### 模块划分
```
系统结构图或模块关系图
```

#### 模块1：<模块名称>
- **职责**：<模块功能描述>
- **接口**：
  - 函数/类名：`<函数名>(<参数>) -> <返回类型>`  # 必须包含类型注解
  - 描述：<功能说明>
  - Python 3.11+ 特性：<如有>

#### 模块2：<模块名称>
- **职责**：<模块功能描述>
- **接口**：
  - 函数/类名：`<函数名>(<参数>) -> <返回类型>`  # 必须包含类型注解
  - 描述：<功能说明>
  - Python 3.11+ 特性：<如有>

### 数据流设计
```
数据流图或流程描述
```

1. **输入处理**：<描述数据如何进入系统>
2. **处理流程**：<描述数据处理步骤>
3. **输出生成**：<描述结果如何输出>

---

## 接口定义
### 外部接口
- **API接口**：<如调用第三方API>
  - 端点：<URL>
  - 请求方式：<GET/POST/PUT/DELETE>
  - 参数：<参数列表>
  - 响应格式：<响应结构>

### 内部接口
#### 接口1
- **函数签名**：`def function_name(param1: type, param2: type) -> return_type:`
  - 必须使用 PEP 585 内置泛型类型（如 `list[int]` 而非 `List[int]`）
- **参数说明**：
  - `param1`：<描述>
  - `param2`：<描述>
- **返回值**：<描述>

---

## 数据层设计

### 数据库选择
- **选择的数据库**：<SQLite / PostgreSQL / MongoDB / ChromaDB / Neo4j 等>
- **选择理由**：
  1. <理由1，引用 database-selection-guide.md>
  2. <理由2>
  3. <理由3>
- **部署方式**：<Docker / 本地安装 / 云服务 / 嵌入式>

### 数据库配置
- **连接字符串**：<连接配置>
- **连接池配置**：<连接池大小、超时等>

### 数据模型设计

#### 模型1：<实体名称>
- **描述**：<实体用途>
- **字段定义**：

| 字段名 | 类型 | 是否主键 | 可空 | 索引 | 描述 | Python 类型 |
|--------|------|----------|------|------|------|------------|
| id | INTEGER | 是 | 否 | 是 | 主键 | int |
| name | VARCHAR(100) | 否 | 否 | 是 | 名称 | str |
| email | VARCHAR(255) | 否 | 否 | 是 | 邮箱 | str |
| created_at | TIMESTAMP | 否 | 否 | 否 | 创建时间 | datetime |

**SQLAlchemy 模型示例**：
```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Model1(Base):
    __tablename__ = "model1"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### 模型2：<实体名称>
- **描述**：<实体用途>
- **字段定义**：<同上>

### 索引策略
| 字段 | 索引类型 | 理由 |
|------|----------|------|
| user_id | B-Tree | 外键，频繁查询 |
| email | B-Tree + UNIQUE | 唯一性约束 |
| created_at | B-Tree | 时间范围查询 |

---

## 数据访问层（Repository）

### Repository 架构
```
┌─────────────────────────────────────┐
│   业务层 (Service Layer)            │
│   - 使用 Repository 接口            │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│   Repository 抽象层                  │
│   - BaseRepository 接口              │
│   - 定义通用 CRUD 操作               │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│   Repository 实现层                  │
│   - SQLAlchemyBaseRepository       │
│   - MongoDBBaseRepository          │
│   - 具体实体 Repository             │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│   数据库层                           │
│   - PostgreSQL / SQLite / MongoDB   │
└─────────────────────────────────────┘
```

### BaseRepository 接口
```python
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, Sequence

ModelType = TypeVar("ModelType")
IDType = TypeVar("IDType", int, str)

class BaseRepository(ABC, Generic[ModelType, IDType]):
    """数据访问层基础接口"""

    @abstractmethod
    def get_by_id(self, id: IDType) -> ModelType | None:
        """根据 ID 获取实体"""
        pass

    @abstractmethod
    def get_all(self) -> Sequence[ModelType]:
        """获取所有实体"""
        pass

    @abstractmethod
    def create(self, entity: ModelType) -> ModelType:
        """创建实体"""
        pass

    @abstractmethod
    def update(self, id: IDType, data: dict[str, Any]) -> ModelType | None:
        """更新实体"""
        pass

    @abstractmethod
    def delete(self, id: IDType) -> bool:
        """删除实体"""
        pass

    @abstractmethod
    def count(self) -> int:
        """统计实体数量"""
        pass
```

### 具体 Repository 实现

#### UserRepository
- **功能**：用户数据访问
- **继承**：SQLAlchemyBaseRepository / MongoDBBaseRepository
- **额外方法**：
  - `get_by_email(email: str) -> User | None`
  - `get_by_name(name: str) -> list[User]`

#### DocumentRepository
- **功能**：文档数据访问
- **继承**：SQLAlchemyBaseRepository / MongoDBBaseRepository
- **额外方法**：
  - `search_by_keyword(keyword: str) -> list[Document]`
  - `get_by_category(category: str) -> list[Document]`

### Repository 工厂
```python
class RepositoryFactory:
    """Repository 工厂，根据配置创建对应数据库的 Repository"""

    def __init__(self, config: DatabaseConfig):
        self._config = config

    def create_user_repository(self) -> UserRepository:
        """创建用户 Repository"""
        if self._config.database_type == DatabaseType.POSTGRESQL:
            return SQLAlchemyUserRepository(self._session)
        elif self._config.database_type == DatabaseType.MONGODB:
            return MongoDBUserRepository(self._mongo_client)
        else:
            raise ValueError(f"Unsupported database type: {self._config.database_type}")

    def create_document_repository(self) -> DocumentRepository:
        """创建文档 Repository"""
        # 类似实现
        pass
```

### 数据库切换策略
- 通过环境变量配置数据库类型
- Repository 工厂根据配置创建对应的实现
- 业务层通过接口访问，无需关心底层实现

---

## 数据库迁移

### SQLAlchemy + Alembic
```bash
# 安装
uv add alembic

# 初始化
alembic init migrations

# 生成迁移脚本
alembic revision --autogenerate -m "initial migration"

# 执行迁移
alembic upgrade head
```

### MongoDB 迁移
- 使用自定义脚本或 pymongo-migrate
- 记录迁移版本和执行时间

---

## 数据库备份与恢复

### 备份策略
- **备份频率**：<如每天一次>
- **备份方式**：<如 pg_dump、mongodump>
- **备份存储**：<如云存储 S3、本地>

### PostgreSQL 备份示例
```bash
# 备份
pg_dump -U user -d dbname > backup.sql

# 恢复
psql -U user -d dbname < backup.sql
```

### MongoDB 备份示例
```bash
# 备份
mongodump --uri="mongodb://localhost:27017/" --out=./backup

# 恢复
mongorestore --uri="mongodb://localhost:27017/" ./backup
```

---

## 性能优化

### 查询优化
- 使用索引加速查询
- 避免 N+1 查询
- 使用 eager loading（SQLAlchemy 的 joinedload）
- 限制返回字段（projection）

### 连接池优化
- 合理设置连接池大小
- 使用连接池预检查（pool_pre_ping）
- 设置连接超时

### 缓存策略
- 使用 Redis 缓存热点数据
- 使用查询结果缓存
- 使用物化视图（PostgreSQL）

---

## 技能识别和管理

### 可提取为技能的模块
识别项目中可复用的功能模块，将其定义为"技能"以便后续复用。

#### 技能列表
- **技能1**：`<函数/类名>` - `<功能描述>` - 位置：<文件路径>
- **技能2**：`<函数/类名>` - `<功能描述>` - 位置：<文件路径>
- **技能3**：`<函数/类名>` - `<功能描述>` - 位置：<文件路径>

### 技能接口定义
为每个可复用技能定义清晰的接口，包含类型注解。

#### 技能1：`<技能名称>`
- **功能**：<技能功能描述>
- **位置**：<文件路径>
- **函数签名**：
  ```python
  def skill_function(data: list[dict[str, Any]]) -> dict[str, Any]:
      """技能功能的实现"""
      pass
  ```
- **输入参数**：
  - `data`：<参数描述>
- **返回值**：<返回值描述>
- **依赖**：<依赖的其他技能或库>
- **复用场景**：<适用的复用场景>

#### 技能2：`<技能名称>`
- **功能**：<技能功能描述>
- **位置**：<文件路径>
- **函数签名**：
  ```python
  def skill_function(param1: str, param2: int) -> bool:
      """技能功能的实现"""
      pass
  ```
- **输入参数**：
  - `param1`：<参数描述>
  - `param2`：<参数描述>
- **返回值**：<返回值描述>
- **依赖**：<依赖的其他技能或库>
- **复用场景**：<适用的复用场景>

### 技能复用指南
说明如何在新功能实现中调用已有技能。

#### 调用方式
1. **直接调用**：
   ```python
   from src.utils.helpers import skill_function

   result = skill_function(data)
   ```

2. **组合调用**：
   ```python
   from src.utils.helpers import skill1, skill2

   result = skill2(skill1(data))
   ```

3. **适配器模式**：
   ```python
   def adapt_skill_for_new_feature(data: list[Any]) -> dict[str, Any]:
       """适配器函数，将新功能的输入转换为技能需要的格式"""
       adapted_data = transform_data(data)
       return existing_skill(adapted_data)
   ```

#### 复用原则
- 优先使用已有技能，避免重复开发
- 确保技能的接口稳定，避免频繁修改
- 技能应具有单一职责，功能清晰
- 技能应包含完整的类型注解和文档

### 数据访问技能
以下数据访问层模块可作为技能复用：

#### 数据访问技能1：BaseRepository 接口
- **功能**：提供通用的 CRUD 操作接口
- **位置**：`src/repositories/base.py`
- **接口**：
  ```python
  class BaseRepository(ABC, Generic[ModelType, IDType]):
      def get_by_id(self, id: IDType) -> ModelType | None
      def get_all(self) -> Sequence[ModelType]
      def create(self, entity: ModelType) -> ModelType
      def update(self, id: IDType, data: dict[str, Any]) -> ModelType | None
      def delete(self, id: IDType) -> bool
      def count(self) -> int
  ```
- **复用场景**：所有需要数据访问的项目

#### 数据访问技能2：SQLAlchemyBaseRepository
- **功能**：SQLAlchemy 的通用实现
- **位置**：`src/repositories/sqlalchemy_base.py`
- **接口**：继承 BaseRepository
- **复用场景**：使用 SQLAlchemy 的关系型数据库项目

#### 数据访问技能3：MongoDBBaseRepository
- **功能**：MongoDB 的通用实现
- **位置**：`src/repositories/mongodb_base.py`
- **接口**：继承 BaseRepository
- **复用场景**：使用 MongoDB 的项目

#### 数据访问技能4：RepositoryFactory
- **功能**：根据配置创建对应的 Repository
- **位置**：`src/repositories/factory.py`
- **接口**：
  ```python
  class RepositoryFactory:
      def create_user_repository(self) -> UserRepository
      def create_document_repository(self) -> DocumentRepository
  ```
- **复用场景**：需要数据库切换的项目
