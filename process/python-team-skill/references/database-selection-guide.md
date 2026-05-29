# 数据库选型指南

## 文档信息
- **项目名称**：<项目名称>
- **文档版本**：v1.0.0
- **Python 版本**：3.11+
- **包管理工具**：UV

---

## 数据库分类与推荐

### 关系型数据库（RDBMS）
适合结构化数据存储，支持 SQL 查询。

#### SQLite
**特点**：
- 轻量级、文件型、零配置、嵌入式
- 非常适合本地开发、移动端、小型应用
- 支持基本 SQL，但不支持并发写入（写锁整个 DB）

**适用场景**：
- 本地开发环境
- 移动端应用
- 小型应用（< 10万条记录）
- 单用户或低并发场景
- 原型验证

**Python 集成**：
```toml
# pyproject.toml
dependencies = [
    "sqlalchemy>=2.0.0",
]
```

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite 连接
engine = create_engine("sqlite:///./data.db")
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
```

#### PostgreSQL
**特点**：
- 功能强大的开源关系数据库，可轻量部署（Docker、本地单机）
- 支持 JSON、全文搜索、地理空间（PostGIS）
- **支持向量搜索**：通过 pgvector 插件
- **支持图查询**：通过 AGE 插件（Cypher 查询）
- 可作为"多模态"数据库使用，适合统一架构

**适用场景**：
- 需要多模态数据存储（关系+向量+图）
- 需要复杂查询和事务支持
- 需要扩展性和高可用性
- 已有 PostgreSQL 基础设施

**Python 集成**：
```toml
# pyproject.toml
dependencies = [
    "psycopg2-binary>=2.9.0",
    "sqlalchemy>=2.0.0",
]

# 向量搜索支持
# dependencies = [
#     "pgvector-python>=0.2.0",
# ]
```

```python
from sqlalchemy import create_engine, Column, Integer, String, JSON, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

# PostgreSQL 连接
engine = create_engine("postgresql+psycopg2://user:password@localhost/dbname")

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    metadata = Column(JSONB)  # JSON 字段
    tags = Column(ARRAY(String))  # 数组字段
    # 向量字段（需 pgvector 插件）
    # embedding = Column(Vector(1536))
```

**插件扩展**：
- **pgvector**：向量存储和相似性搜索
  ```sql
  CREATE EXTENSION vector;
  ```
- **Apache AGE**：图查询支持（Cypher）
  ```sql
  CREATE EXTENSION age;
  ```
- **PostGIS**：地理空间数据
  ```sql
  CREATE EXTENSION postgis;
  ```

---

### 文档型 / NoSQL
适合灵活 schema、JSON 文档存储。

#### MongoDB
**特点**：
- 最流行的文档数据库，以 BSON（二进制 JSON）格式存储
- 支持复杂查询、索引、聚合管道
- 社区版免费，可轻量部署（MongoDB Community Server 或 mongodb-memory-server）

**适用场景**：
- 需要灵活 schema
- 文档型数据（日志、配置、内容）
- 快速迭代开发
- 需要 JSON 原生支持

**Python 集成**：
```toml
# pyproject.toml
dependencies = [
    "pymongo>=4.0.0",
    "motor>=3.0.0",  # 异步驱动
]
```

```python
from pymongo import MongoClient
from typing import Any

# MongoDB 连接
client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["documents"]

# 插入文档
document: dict[str, Any] = {
    "title": "文档标题",
    "content": "文档内容",
    "tags": ["tag1", "tag2"],
    "metadata": {"author": "user1"}
}
collection.insert_one(document)

# 查询
results = collection.find({"tags": "tag1"})
```

---

### 向量数据库
用于 AI / Embedding 相似性搜索。

#### pgvector（PostgreSQL 插件）
**特点**：
- 在 PostgreSQL 中直接支持向量存储和 ANN（近似最近邻）搜索
- 轻量、无需额外服务，适合已有 PG 架构的项目
- 支持多种距离度量（L2、内积、余弦）

**适用场景**：
- 已使用 PostgreSQL 的项目
- 需要向量搜索但不想引入新服务
- 中小规模向量数据（< 1000万向量）

**Python 集成**：
```toml
# pyproject.toml
dependencies = [
    "pgvector-python>=0.2.0",
]
```

```python
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

class Embedding(Base):
    __tablename__ = "embeddings"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    vector = Column(Vector(1536))  # 1536 维向量
    # 相似性搜索
    # results = session.query(Embedding).order_by(
    #     Embedding.vector.l2_distance(query_vector)
    # ).limit(10).all()
```

#### ChromaDB
**特点**：
- 轻量级开源向量数据库，专为 LLM 应用设计
- 支持 Python/JS
- 可嵌入（in-memory）或持久化到本地

**适用场景**：
- LLM 应用（RAG、文档问答）
- 快速原型开发
- 本地开发环境

**Python 集成**：
```toml
# pyproject.toml
dependencies = [
    "chromadb>=0.4.0",
]
```

```python
import chromadb
from chromadb.utils import embedding_functions

# ChromaDB 连接
client = chromadb.Client()
collection = client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_functions.DefaultEmbeddingFunction()
)

# 添加文档
collection.add(
    documents=["文档1", "文档2"],
    metadatas=[{"source": "file1"}, {"source": "file2"}],
    ids=["doc1", "doc2"]
)

# 相似性搜索
results = collection.query(
    query_texts=["查询文本"],
    n_results=5
)
```

#### Faiss
**特点**：
- 由 Meta 开发的高效向量相似性搜索库（C++/Python）
- 本身不是完整数据库，是一个索引+搜索库
- 通常需配合其他存储（如 SQLite、HDF5、内存）使用
- 适合离线批处理或嵌入到应用中

**适用场景**：
- 离线批处理
- 需要高性能向量索引
- 已有其他存储方案

**Python 集成**：
```toml
# pyproject.toml
dependencies = [
    "faiss-cpu>=1.7.0",  # CPU 版本
    # "faiss-gpu>=1.7.0",  # GPU 版本
]
```

```python
import faiss
import numpy as np
from typing import Any

# 创建索引
dimension = 1536
index = faiss.IndexFlatL2(dimension)

# 添加向量
vectors = np.random.random((1000, dimension)).astype('float32')
index.add(vectors)

# 搜索
query_vector = np.random.random((1, dimension)).astype('float32')
distances, indices = index.search(query_vector, k=10)
```

---

### 图数据库
适合关系网络、知识图谱等场景。

#### Neo4j
**特点**：
- 最主流的图数据库，支持 Cypher 查询语言
- 社区版免费，可本地运行（单机）
- 资源占用相对较高（需 JVM）

**适用场景**：
- 关系网络分析
- 知识图谱
- 社交网络
- 推荐系统

**Python 集成**：
```toml
# pyproject.toml
dependencies = [
    "neo4j>=5.0.0",
]
```

```python
from neo4j import GraphDatabase
from typing import Any

class Neo4jConnection:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> None:
        self.driver.close()

    def query(self, cypher: str, parameters: dict[str, Any] | None = None) -> Any:
        with self.driver.session() as session:
            result = session.run(cypher, parameters)
            return [record.data() for record in result]

# 使用
conn = Neo4jConnection("bolt://localhost:7687", "neo4j", "password")
results = conn.query(
    "MATCH (n:Person) RETURN n LIMIT 10"
)
conn.close()
```

#### Apache AGE（PostgreSQL 插件）
**特点**：
- PostgreSQL 的官方图扩展
- 让你在 PG 中直接使用 Cypher 查询图数据
- 无需额外部署 Neo4j，复用 PG 的生态和运维
- 适合"以 PG 为中心"的多模架构

**适用场景**：
- 已使用 PostgreSQL 的项目
- 需要图查询但不想要新服务
- 需要关系+图混合查询

**Python 集成**：
```toml
# pyproject.toml
dependencies = [
    "age>=0.8.0",
]
```

```python
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

# Cypher 查询（通过 AGE）
cypher_query = """
SELECT * FROM cypher('graph_name', $$
    MATCH (n:Person)-[r:KNOWS]->(m:Person)
    RETURN n.name, m.name
$$) as (n_name agtype, m_name agtype);
"""

result = session.execute(text(cypher_query))
```

---

## 推荐组合方案

### 方案1：轻量级统一架构（PostgreSQL 为主）
**组合**：PostgreSQL + pgvector + Apache AGE
**优势**：
- 单一数据库，统一管理
- 支持关系、向量、图三种数据类型
- 轻量部署（Docker 或本地）
- 生态成熟

**适用场景**：
- 中小规模项目
- 需要多模态数据支持
- 追求架构简洁

**依赖配置**：
```toml
# pyproject.toml
dependencies = [
    "psycopg2-binary>=2.9.0",
    "sqlalchemy>=2.0.0",
    "pgvector-python>=0.2.0",
]
```

### 方案2：分离架构（功能专一）
**组合**：SQLite + MongoDB + ChromaDB
**优势**：
- 各数据库专注自己的领域
- 开发体验好
- 灵活组合

**适用场景**：
- 大规模项目
- 需要高可扩展性
- 各数据类型独立

**依赖配置**：
```toml
# pyproject.toml
dependencies = [
    "sqlalchemy>=2.0.0",
    "pymongo>=4.0.0",
    "chromadb>=0.4.0",
]
```

### 方案3：嵌入式架构（最小依赖）
**组合**：SQLite + Faiss
**优势**：
- 零配置，单文件
- 最小依赖
- 适合边缘设备

**适用场景**：
- 本地工具
- 移动端应用
- 单用户场景

**依赖配置**：
```toml
# pyproject.toml
dependencies = [
    "sqlalchemy>=2.0.0",
    "faiss-cpu>=1.7.0",
]
```

---

## 选型决策矩阵

| 数据库类型 | 数据规模 | 并发需求 | 查询复杂度 | 部署复杂度 | 推荐指数 |
|------------|----------|----------|------------|------------|----------|
| SQLite | 小 (<10万) | 低 | 低 | 最低 | ⭐⭐⭐⭐⭐ |
| PostgreSQL | 中 (<1亿) | 中-高 | 高 | 中 | ⭐⭐⭐⭐⭐ |
| MongoDB | 中-大 | 中 | 中 | 中 | ⭐⭐⭐⭐ |
| pgvector | 中 (<1000万向量) | 中 | 高 | 中 | ⭐⭐⭐⭐⭐ |
| ChromaDB | 中-大 | 中 | 高 | 低 | ⭐⭐⭐⭐ |
| Faiss | 大 (>1亿向量) | 低 | 高 | 低 | ⭐⭐⭐ |
| Neo4j | 中 (<1000万节点) | 中 | 高 | 高 | ⭐⭐⭐ |
| Apache AGE | 中 (<1000万节点) | 中 | 高 | 中 | ⭐⭐⭐⭐ |

---

## 选型建议

### 根据项目规模选择
- **小项目**（< 5万条记录）：SQLite
- **中型项目**（5万-1000万条）：PostgreSQL（含插件）
- **大型项目**（> 1000万条）：分离架构（PostgreSQL + MongoDB + 专用向量DB）

### 根据数据类型选择
- **纯关系型数据**：SQLite 或 PostgreSQL
- **文档型数据**：MongoDB
- **向量搜索**：pgvector（已有PG）或 ChromaDB（独立）
- **图关系**：Apache AGE（已有PG）或 Neo4j（独立）

### 根据部署环境选择
- **本地开发**：SQLite、ChromaDB（in-memory）
- **云服务**：PostgreSQL（云数据库）、MongoDB Atlas
- **边缘设备**：SQLite、Faiss
