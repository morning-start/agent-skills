# 数据库设计文档

## 文档信息
- **项目名称**：<项目名称>
- **文档版本**：v1.0.0
- **Python 版本**：3.11+
- **包管理工具**：UV

---

## 数据库选型

### 选择数据库
- **选择的数据库**：<SQLite / PostgreSQL / MongoDB / ChromaDB / Neo4j 等>
- **选择理由**：
  1. <理由1，引用 database-selection-guide.md 中的对比>
  2. <理由2>
  3. <理由3>
- **部署方式**：<Docker / 本地安装 / 云服务>

### 数据库配置
- **连接字符串**：<连接配置>
- **连接池配置**：<连接池大小、超时等>
- **索引策略**：<哪些字段需要索引>

**SQLite 配置示例**：
```python
DATABASE_URL = "sqlite:///./data.db"
# 启用 WAL 模式以提高并发
PRAGMA journal_mode = WAL
```

**PostgreSQL 配置示例**：
```python
DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/dbname"
# 连接池配置
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

**MongoDB 配置示例**：
```python
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "mydb"
```

---

## 数据模型设计

### 实体关系图（ER图）
```
<描述实体间的关系>
例如：User --< Order >-- Product
```

### 数据表/集合设计

#### 表/集合1：<名称>
- **描述**：<表/集合的用途>
- **字段列表**：

| 字段名 | 类型 | 是否主键 | 可空 | 索引 | 描述 | Python 类型 |
|--------|------|----------|------|------|------|------------|
| id | INTEGER | 是 | 否 | 是 | 主键 | int |
| name | VARCHAR(100) | 否 | 否 | 是 | 名称 | str |
| email | VARCHAR(255) | 否 | 否 | 是 | 邮箱 | str |
| created_at | TIMESTAMP | 否 | 否 | 否 | 创建时间 | datetime |

**SQLAlchemy 模型**：
```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Table1(Base):
    __tablename__ = "table1"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Table1(id={self.id}, name={self.name})>"
```

**MongoDB Schema**：
```python
from typing import Any
from pydantic import BaseModel, Field
from datetime import datetime

class Collection1(BaseModel):
    id: str | None = None  # MongoDB 自动生成
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "示例名称",
                "email": "user@example.com",
                "metadata": {"key": "value"}
            }
        }
```

#### 表/集合2：<名称>
- **描述**：<表/集合的用途>
- **字段列表**：

| 字段名 | 类型 | 是否主键 | 可空 | 索引 | 描述 | Python 类型 |
|--------|------|----------|------|------|------|------------|
| id | INTEGER | 是 | 否 | 是 | 主键 | int |
| user_id | INTEGER | 否 | 否 | 是 | 外键（用户ID） | int |
| content | TEXT | 否 | 否 | 否 | 内容 | str |

**SQLAlchemy 模型（含外键关系）**：
```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Table2(Base):
    __tablename__ = "table2"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("table1.id"), nullable=False, index=True)
    content = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系定义
    user = relationship("Table1", back_populates="table2s")

# 在 Table1 中添加反向关系
# Table1.table2s = relationship("Table2", back_populates="user")
```

---

## 向量存储设计（如适用）

### 向量表设计
- **表名**：<表名>
- **向量维度**：<如 1536（OpenAI embedding）>
- **索引类型**：<如 ivfflat、hnsw>

**PostgreSQL + pgvector 表设计**：
```python
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String, Text

class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    text = Column(Text)
    embedding = Column(Vector(1536))  # 1536 维向量
    created_at = Column(DateTime, default=datetime.utcnow)

    # 创建向量索引
    # CREATE INDEX ON document_embeddings USING ivfflat (embedding vector_cosine_ops)
```

**ChromaDB 集合设计**：
```python
import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}  # 相似度度量：cosine, l2, ip
)
```

---

## 图数据设计（如适用）

### 节点类型
- **节点类型1**：<如 Person>
  - 属性：<列表>
- **节点类型2**：<如 Document>
  - 属性：<列表>

### 边类型
- **边类型1**：<如 KNOWS>
  - 属性：<列表>
- **边类型2**：<如 CONTAINS>
  - 属性：<列表>

**Neo4j Schema**：
```python
# 节点示例
# CREATE (p:Person {name: "Alice", age: 30})
# CREATE (d:Document {title: "文档1", content: "..."})

# 边示例
# MATCH (p:Person), (d:Document)
# CREATE (p)-[:WROTE {timestamp: datetime()}]->(d)
```

**PostgreSQL + AGE Schema**：
```sql
-- 创建图
SELECT create_graph('my_graph');

-- 节点
SELECT * FROM cypher('my_graph', $$
    CREATE (p:Person {name: 'Alice', age: 30})
$$) as (p agtype);

-- 边
SELECT * FROM cypher('my_graph', $$
    MATCH (p:Person), (d:Document)
    CREATE (p)-[:WROTE {timestamp: datetime()}]->(d)
$$) as (result agtype);
```

---

## 索引策略

### 关系型数据库索引
| 字段 | 索引类型 | 理由 |
|------|----------|------|
| user_id | B-Tree | 外键，频繁查询 |
| email | B-Tree + UNIQUE | 唯一性约束，登录查询 |
| created_at | B-Tree | 时间范围查询 |
| embedding | ivfflat / hnsw | 向量相似性搜索 |

**创建索引的 SQL**：
```sql
-- B-Tree 索引
CREATE INDEX idx_user_id ON table2(user_id);

-- 唯一索引
CREATE UNIQUE INDEX idx_email ON table1(email);

-- 向量索引（pgvector）
CREATE INDEX idx_embedding ON document_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

### MongoDB 索引
| 字段 | 索引类型 | 理由 |
|------|----------|------|
| email | Unique | 唯一性约束 |
| user_id | Single | 外键，频繁查询 |
| created_at | Single | 时间范围查询 |
| tags | Multikey | 标签查询 |

```python
# 创建索引
collection.create_index([("email", 1)], unique=True)
collection.create_index([("user_id", 1)])
collection.create_index([("tags", 1)])  # Multikey 索引
```

---

## 数据访问接口定义

### Repository 模式接口
为每个实体定义数据访问接口，统一数据层抽象。

#### Repository1：`<EntityName>Repository`
- **功能**：<描述>
- **接口方法**：
  - `def get_by_id(id: int) -> EntityType | None`
  - `def get_all(limit: int = 100, offset: int = 0) -> list[EntityType]`
  - `def create(entity: EntityType) -> EntityType`
  - `def update(id: int, data: dict[str, Any]) -> EntityType | None`
  - `def delete(id: int) -> bool`

**SQLAlchemy 实现**：
```python
from typing import Any, Generic, TypeVar, Type
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    def get_by_id(self, id: int) -> ModelType | None:
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self, limit: int = 100, offset: int = 0) -> list[ModelType]:
        return self.session.query(self.model).offset(offset).limit(limit).all()

    def create(self, entity: ModelType) -> ModelType:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, id: int, data: dict[str, Any]) -> ModelType | None:
        entity = self.get_by_id(id)
        if entity:
            for key, value in data.items():
                setattr(entity, key, value)
            self.session.commit()
            self.session.refresh(entity)
        return entity

    def delete(self, id: int) -> bool:
        entity = self.get_by_id(id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return True
        return False

# 具体实现
class UserRepository(BaseRepository[Table1]):
    def __init__(self, session: Session):
        super().__init__(Table1, session)

    def get_by_email(self, email: str) -> Table1 | None:
        return self.session.query(Table1).filter(Table1.email == email).first()
```

---

## 数据迁移策略

### SQLAlchemy + Alembic（PostgreSQL / SQLite）
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
```python
# 使用 pymongo-migrate 或自定义脚本
from pymongo import MongoClient

def migrate():
    client = MongoClient()
    db = client["mydb"]

    # 示例：添加新字段
    db.users.update_many(
        {"new_field": {"$exists": False}},
        {"$set": {"new_field": "default_value"}}
    )
```

---

## 数据备份与恢复

### 备份策略
- **备份频率**：<如每天一次>
- **备份方式**：<如 pg_dump、mongodump>
- **备份存储**：<如云存储 S3、本地>

**PostgreSQL 备份**：
```bash
# 备份
pg_dump -U user -d dbname > backup.sql

# 恢复
psql -U user -d dbname < backup.sql
```

**MongoDB 备份**：
```bash
# 备份
mongodump --uri="mongodb://localhost:27017/" --out=./backup

# 恢复
mongorestore --uri="mongodb://localhost:27017/" ./backup
```

**SQLite 备份**：
```bash
# 直接复制文件
cp data.db data.db.backup
```

---

## 性能优化建议

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

## 安全考虑

### 访问控制
- 数据库用户权限最小化
- 使用环境变量存储敏感信息
- 连接加密（SSL/TLS）

### 数据加密
- 传输加密：SSL/TLS
- 存储加密：字段级加密（敏感数据）

### SQL 注入防护
- 使用参数化查询（SQLAlchemy 自动处理）
- 输入验证和清理
- ORM 提供的防护机制
