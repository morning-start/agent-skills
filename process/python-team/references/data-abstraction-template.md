# 数据层抽象设计文档

## 文档信息
- **项目名称**：<项目名称>
- **文档版本**：v1.0.0
- **Python 版本**：3.11+
- **包管理工具**：UV

---

## 设计目标
- **抽象目标**：提供统一的数据访问接口，屏蔽底层数据库差异
- **灵活切换**：支持在不同数据库之间切换（如 SQLite → PostgreSQL）
- **易于测试**：便于在测试环境中使用内存数据库
- **类型安全**：使用类型注解确保类型安全
- **技能复用**：数据访问逻辑可作为技能模块复用

---

## 架构设计

### 分层架构
```
┌─────────────────────────────────────┐
│   Application Layer (业务逻辑)      │
│   - 使用 Repository 接口            │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│   Repository Layer (数据访问层)      │
│   - Repository 接口定义              │
│   - 具体实现（SQLAlchemy、MongoDB）  │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│   Database Layer (数据库)            │
│   - PostgreSQL / SQLite / MongoDB   │
└─────────────────────────────────────┘
```

---

## 接口定义

### 基础接口：`BaseRepository`

```python
"""
数据访问层基础接口

定义通用的 CRUD 操作，所有实体 Repository 必须继承此接口
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, Sequence
from dataclasses import dataclass

# 类型变量
ModelType = TypeVar("ModelType")
IDType = TypeVar("IDType", int, str)

@dataclass
class PaginationParams:
    """分页参数"""
    page: int = 1
    page_size: int = 10

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

@dataclass
class PaginationResult(Generic[ModelType]):
    """分页结果"""
    items: Sequence[ModelType]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def create(
        cls,
        items: Sequence[ModelType],
        total: int,
        params: PaginationParams
    ) -> "PaginationResult[ModelType]":
        total_pages = (total + params.page_size - 1) // params.page_size
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages
        )

class BaseRepository(ABC, Generic[ModelType, IDType]):
    """
    数据访问层基础接口

    提供通用的 CRUD 操作，所有实体 Repository 必须实现此接口
    """

    @abstractmethod
    def get_by_id(self, id: IDType) -> ModelType | None:
        """
        根据 ID 获取实体

        Args:
            id: 实体 ID

        Returns:
            实体对象，不存在则返回 None
        """
        pass

    @abstractmethod
    def get_all(
        self,
        pagination: PaginationParams | None = None
    ) -> Sequence[ModelType] | PaginationResult[ModelType]:
        """
        获取所有实体

        Args:
            pagination: 分页参数，不传则返回全部

        Returns:
            实体列表或分页结果
        """
        pass

    @abstractmethod
    def create(self, entity: ModelType) -> ModelType:
        """
        创建实体

        Args:
            entity: 实体对象

        Returns:
            创建后的实体（包含 ID）
        """
        pass

    @abstractmethod
    def create_many(self, entities: Sequence[ModelType]) -> Sequence[ModelType]:
        """
        批量创建实体

        Args:
            entities: 实体列表

        Returns:
            创建后的实体列表
        """
        pass

    @abstractmethod
    def update(
        self,
        id: IDType,
        data: dict[str, Any]
    ) -> ModelType | None:
        """
        更新实体

        Args:
            id: 实体 ID
            data: 更新数据

        Returns:
            更新后的实体，不存在则返回 None
        """
        pass

    @abstractmethod
    def delete(self, id: IDType) -> bool:
        """
        删除实体

        Args:
            id: 实体 ID

        Returns:
            是否删除成功
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """
        统计实体数量

        Returns:
            实体总数
        """
        pass

    @abstractmethod
    def exists(self, id: IDType) -> bool:
        """
        检查实体是否存在

        Args:
            id: 实体 ID

        Returns:
            是否存在
        """
        pass
```

---

## SQLAlchemy 实现

### 基础实现：`SQLAlchemyBaseRepository`

```python
"""
SQLAlchemy 数据访问层基础实现

基于 SQLAlchemy ORM 实现 BaseRepository 接口
"""

from typing import Any, Sequence, Type
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from .base import BaseRepository, ModelType, IDType, PaginationParams, PaginationResult

class SQLAlchemyBaseRepository(BaseRepository[ModelType, IDType]):
    """
    SQLAlchemy 数据访问层基础实现

    提供 CRUD 操作的通用实现，子类只需指定模型类型
    """

    def __init__(self, model: Type[ModelType], session: Session):
        """
        初始化 Repository

        Args:
            model: SQLAlchemy 模型类
            session: 数据库会话
        """
        self._model = model
        self._session = session

    def get_by_id(self, id: IDType) -> ModelType | None:
        stmt = select(self._model).where(self._model.id == id)
        return self._session.execute(stmt).scalar_one_or_none()

    def get_all(
        self,
        pagination: PaginationParams | None = None
    ) -> Sequence[ModelType] | PaginationResult[ModelType]:
        stmt = select(self._model)

        if pagination:
            # 获取总数
            count_stmt = select(func.count()).select_from(self._model)
            total = self._session.execute(count_stmt).scalar()

            # 获取分页数据
            stmt = stmt.offset(pagination.offset).limit(pagination.page_size)
            items = self._session.execute(stmt).scalars().all()

            return PaginationResult.create(items, total, pagination)

        # 返回全部数据
        return self._session.execute(stmt).scalars().all()

    def create(self, entity: ModelType) -> ModelType:
        self._session.add(entity)
        self._session.commit()
        self._session.refresh(entity)
        return entity

    def create_many(self, entities: Sequence[ModelType]) -> Sequence[ModelType]:
        self._session.add_all(entities)
        self._session.commit()
        for entity in entities:
            self._session.refresh(entity)
        return entities

    def update(
        self,
        id: IDType,
        data: dict[str, Any]
    ) -> ModelType | None:
        entity = self.get_by_id(id)
        if entity:
            for key, value in data.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            self._session.commit()
            self._session.refresh(entity)
        return entity

    def delete(self, id: IDType) -> bool:
        entity = self.get_by_id(id)
        if entity:
            self._session.delete(entity)
            self._session.commit()
            return True
        return False

    def count(self) -> int:
        stmt = select(func.count()).select_from(self._model)
        return self._session.execute(stmt).scalar()

    def exists(self, id: IDType) -> bool:
        stmt = select(func.count()).select_from(self._model).where(self._model.id == id)
        return self._session.execute(stmt).scalar() > 0
```

### 具体实现：`UserRepository`

```python
"""
用户数据访问层实现

具体实体的 Repository 实现
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Sequence
from .sqlalchemy_base import SQLAlchemyBaseRepository
from .models import User
from .base import PaginationParams

class UserRepository(SQLAlchemyBaseRepository[User, int]):
    """
    用户数据访问层实现

    继承 SQLAlchemyBaseRepository，提供用户特定的数据访问方法
    """

    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_email(self, email: str) -> User | None:
        """根据邮箱获取用户"""
        stmt = select(User).where(User.email == email)
        return self._session.execute(stmt).scalar_one_or_none()

    def get_by_name(self, name: str) -> Sequence[User]:
        """根据姓名搜索用户（模糊匹配）"""
        stmt = select(User).where(User.name.ilike(f"%{name}%"))
        return self._session.execute(stmt).scalars().all()

    def get_active_users(
        self,
        pagination: PaginationParams | None = None
    ) -> Sequence[User]:
        """获取活跃用户"""
        stmt = select(User).where(User.is_active == True)
        if pagination:
            stmt = stmt.offset(pagination.offset).limit(pagination.page_size)
        return self._session.execute(stmt).scalars().all()
```

---

## MongoDB 实现

### 基础实现：`MongoDBBaseRepository`

```python
"""
MongoDB 数据访问层基础实现

基于 PyMongo 实现 BaseRepository 接口
"""

from typing import Any, Sequence, Optional
from pymongo import MongoClient, Collection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from .base import BaseRepository, ModelType, IDType, PaginationParams, PaginationResult
from pydantic import BaseModel

class MongoDBBaseRepository(BaseRepository[BaseModel, str]):
    """
    MongoDB 数据访问层基础实现

    提供 CRUD 操作的通用实现，子类只需指定集合名称
    """

    def __init__(self, client: MongoClient, database_name: str, collection_name: str):
        """
        初始化 Repository

        Args:
            client: MongoDB 客户端
            database_name: 数据库名称
            collection_name: 集合名称
        """
        self._client = client
        self._collection: Collection = client[database_name][collection_name]

    def _to_model(self, data: dict[str, Any], model_class: type[BaseModel]) -> BaseModel:
        """将字典转换为模型对象"""
        return model_class(**data)

    def _to_dict(self, model: BaseModel) -> dict[str, Any]:
        """将模型对象转换为字典"""
        data = model.model_dump(exclude_unset=True)
        # 移除 _id 字段（如果模型中有），让 MongoDB 自动生成
        data.pop("_id", None)
        return data

    def get_by_id(self, id: str) -> BaseModel | None:
        data = self._collection.find_one({"_id": id})
        if data:
            return self._to_model(data, self._model_class)
        return None

    def get_all(
        self,
        pagination: PaginationParams | None = None
    ) -> Sequence[BaseModel] | PaginationResult[BaseModel]:
        if pagination:
            total = self._collection.count_documents({})
            skip = pagination.offset
            limit = pagination.page_size

            cursor = self._collection.find({}).skip(skip).limit(limit)
            items = [
                self._to_model(doc, self._model_class)
                for doc in cursor
            ]

            return PaginationResult.create(items, total, pagination)

        cursor = self._collection.find({})
        return [
            self._to_model(doc, self._model_class)
            for doc in cursor
        ]

    def create(self, entity: BaseModel) -> BaseModel:
        data = self._to_dict(entity)
        result: InsertOneResult = self._collection.insert_one(data)

        # 重新查询获取完整对象（包含 _id）
        created = self.get_by_id(result.inserted_id)
        return created

    def create_many(self, entities: Sequence[BaseModel]) -> Sequence[BaseModel]:
        data_list = [self._to_model(entity) for entity in entities]
        result = self._collection.insert_many(data_list)

        # 批量查询获取完整对象
        created_entities = self._collection.find({"_id": {"$in": result.inserted_ids}})
        return [self._to_model(doc, self._model_class) for doc in created_entities]

    def update(
        self,
        id: str,
        data: dict[str, Any]
    ) -> BaseModel | None:
        result: UpdateResult = self._collection.update_one(
            {"_id": id},
            {"$set": data}
        )

        if result.modified_count > 0:
            return self.get_by_id(id)
        return None

    def delete(self, id: str) -> bool:
        result: DeleteResult = self._collection.delete_one({"_id": id})
        return result.deleted_count > 0

    def count(self) -> int:
        return self._collection.count_documents({})

    def exists(self, id: str) -> bool:
        return self._collection.count_documents({"_id": id}) > 0

    def find(self, query: dict[str, Any]) -> Sequence[BaseModel]:
        """自定义查询"""
        cursor = self._collection.find(query)
        return [self._to_model(doc, self._model_class) for doc in cursor]

    def aggregate(self, pipeline: list[dict[str, Any]]) -> Sequence[dict[str, Any]]:
        """聚合查询"""
        return list(self._collection.aggregate(pipeline))
```

### 具体实现：`UserRepository`

```python
"""
用户数据访问层实现（MongoDB 版本）

具体实体的 Repository 实现
"""

from pymongo import MongoClient
from typing import Sequence
from .mongodb_base import MongoDBBaseRepository
from .models import User
from .base import PaginationParams

class UserRepository(MongoDBBaseRepository[User]):
    """
    用户数据访问层实现（MongoDB 版本）

    继承 MongoDBBaseRepository，提供用户特定的数据访问方法
    """

    def __init__(self, client: MongoClient, database_name: str = "mydb"):
        super().__init__(client, database_name, "users")

    def get_by_email(self, email: str) -> User | None:
        """根据邮箱获取用户"""
        result = list(self._collection.find({"email": email}).limit(1))
        if result:
            return self._to_model(result[0], User)
        return None

    def get_by_name(self, name: str) -> Sequence[User]:
        """根据姓名搜索用户（模糊匹配）"""
        cursor = self._collection.find({"name": {"$regex": name, "$options": "i"}})
        return [self._to_model(doc, User) for doc in cursor]

    def get_active_users(
        self,
        pagination: PaginationParams | None = None
    ) -> Sequence[User]:
        """获取活跃用户"""
        cursor = self._collection.find({"is_active": True})
        if pagination:
            cursor = cursor.skip(pagination.offset).limit(pagination.page_size)
        return [self._to_model(doc, User) for doc in cursor]
```

---

## 数据库切换策略

### 配置管理
```python
"""
数据库配置管理

支持通过环境变量配置不同数据库
"""

from dataclasses import dataclass
from enum import Enum
import os

class DatabaseType(str, Enum):
    """数据库类型枚举"""
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"
    MONGODB_IN_MEMORY = "mongodb_memory"

@dataclass
class DatabaseConfig:
    """数据库配置"""
    database_type: DatabaseType

    # PostgreSQL / SQLite
    connection_string: str | None = None

    # MongoDB
    mongo_uri: str | None = None
    mongo_database: str | None = None

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """从环境变量加载配置"""
        db_type = DatabaseType(os.getenv("DATABASE_TYPE", "sqlite"))

        if db_type == DatabaseType.SQLITE:
            return cls(
                database_type=db_type,
                connection_string=os.getenv(
                    "SQLITE_DATABASE_URL",
                    "sqlite:///./data.db"
                )
            )

        elif db_type == DatabaseType.POSTGRESQL:
            return cls(
                database_type=db_type,
                connection_string=os.getenv(
                    "POSTGRESQL_DATABASE_URL",
                    "postgresql+psycopg2://user:password@localhost:5432/dbname"
                )
            )

        elif db_type in [DatabaseType.MONGODB, DatabaseType.MONGODB_IN_MEMORY]:
            return cls(
                database_type=db_type,
                mongo_uri=os.getenv(
                    "MONGO_URI",
                    "mongodb://localhost:27017/"
                ),
                mongo_database=os.getenv("MONGO_DATABASE", "mydb")
            )

        raise ValueError(f"Unsupported database type: {db_type}")
```

### Repository 工厂
```python
"""
Repository 工厂

根据配置创建对应数据库的 Repository 实例
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pymongo import MongoClient
from .config import DatabaseConfig, DatabaseType
from .repositories import UserRepository, DocumentRepository
from typing import Any

class RepositoryFactory:
    """
    Repository 工厂

    根据数据库配置创建对应的 Repository 实例
    """

    def __init__(self, config: DatabaseConfig):
        self._config = config
        self._session: Session | None = None
        self._mongo_client: MongoClient | None = None

    def create_session(self) -> Session:
        """创建 SQLAlchemy 会话"""
        if not self._session:
            engine = create_engine(self._config.connection_string)
            SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
            self._session = SessionLocal()
        return self._session

    def create_mongo_client(self) -> MongoClient:
        """创建 MongoDB 客户端"""
        if not self._mongo_client:
            self._mongo_client = MongoClient(self._config.mongo_uri)
        return self._mongo_client

    def create_user_repository(self) -> Any:
        """创建用户 Repository"""
        if self._config.database_type in [DatabaseType.SQLITE, DatabaseType.POSTGRESQL]:
            session = self.create_session()
            return UserRepository(session)
        elif self._config.database_type in [DatabaseType.MONGODB, DatabaseType.MONGODB_IN_MEMORY]:
            client = self.create_mongo_client()
            return UserRepository(client, self._config.mongo_database)
        else:
            raise ValueError(f"Unsupported database type: {self._config.database_type}")

    def create_document_repository(self) -> Any:
        """创建文档 Repository"""
        if self._config.database_type in [DatabaseType.SQLITE, DatabaseType.POSTGRESQL]:
            session = self.create_session()
            return DocumentRepository(session)
        elif self._config.database_type in [DatabaseType.MONGODB, DatabaseType.MONGODB_IN_MEMORY]:
            client = self.create_mongo_client()
            return DocumentRepository(client, self._config.mongo_database)
        else:
            raise ValueError(f"Unsupported database type: {self._config.database_type}")

    def close(self) -> None:
        """关闭所有连接"""
        if self._session:
            self._session.close()
            self._session = None
        if self._mongo_client:
            self._mongo_client.close()
            self._mongo_client = None
```

---

## 使用示例

### 业务层使用
```python
"""
业务层使用示例

业务层通过 Repository 接口访问数据，不直接依赖具体数据库实现
"""

from .repositories import UserRepository
from .models import User
from loguru import logger

class UserService:
    """
    用户服务

    业务逻辑层，使用 Repository 接口访问数据
    """

    def __init__(self, user_repository: UserRepository):
        self._user_repo = user_repository

    def create_user(self, name: str, email: str) -> User:
        """创建用户"""
        # 检查邮箱是否已存在
        existing = self._user_repo.get_by_email(email)
        if existing:
            raise ValueError(f"Email {email} already exists")

        # 创建用户
        user = User(name=name, email=email)
        created = self._user_repo.create(user)

        logger.info(f"User created: {created.id}")
        return created

    def get_user(self, user_id: int) -> User | None:
        """获取用户"""
        return self._user_repo.get_by_id(user_id)

    def search_users(self, name: str) -> list[User]:
        """搜索用户"""
        return list(self._user_repo.get_by_name(name))

    def list_users(self, page: int = 1, page_size: int = 10) -> dict[str, Any]:
        """列出用户（分页）"""
        from .base import PaginationParams

        params = PaginationParams(page=page, page_size=page_size)
        result = self._user_repo.get_all(pagination=params)

        return {
            "items": result.items,
            "total": result.total,
            "page": result.page,
            "page_size": result.page_size,
            "total_pages": result.total_pages
        }
```

### 初始化与使用
```python
"""
应用初始化示例
"""

from loguru import logger
from .config import DatabaseConfig
from .factory import RepositoryFactory
from .services import UserService

# 加载配置
config = DatabaseConfig.from_env()

# 创建 Repository 工厂
factory = RepositoryFactory(config)

# 创建 Repository
user_repo = factory.create_user_repository()

# 创建服务
user_service = UserService(user_repo)

# 使用服务
user = user_service.create_user("Alice", "alice@example.com")
logger.info(f"Created user: {user}")

# 清理
factory.close()
```

---

## 测试策略

### 使用内存数据库测试
```python
"""
使用内存数据库进行测试

在测试环境中使用内存数据库，提高测试速度和隔离性
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pymongo import MongoClient
from mongomock import MongoClient as MockMongoClient

# SQLite 内存数据库
@pytest.fixture
def sqlite_session() -> Session:
    """SQLite 内存数据库会话"""
    engine = create_engine("sqlite:///:memory:")
    # 创建表
    from .models import Base
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

# MongoDB 内存数据库
@pytest.fixture
def mongodb_client() -> MockMongoClient:
    """MongoDB 内存数据库客户端"""
    client = MockMongoClient()
    yield client
    client.close()

# 测试用例
def test_create_user(sqlite_session: Session):
    """测试创建用户"""
    from .repositories import UserRepository
    from .models import User

    repo = UserRepository(sqlite_session)
    user = User(name="Test", email="test@example.com")
    created = repo.create(user)

    assert created.id is not None
    assert created.name == "Test"
    assert created.email == "test@example.com"
```

---

## 技能复用

### 识别为技能的数据访问模块
1. **BaseRepository 接口**：可复用的通用 CRUD 接口
2. **SQLAlchemyBaseRepository**：关系型数据库的通用实现
3. **MongoDBBaseRepository**：MongoDB 的通用实现
4. **RepositoryFactory**：数据库切换工厂

### 技能接口
```python
"""
数据访问技能模块接口

定义数据访问层的技能接口，便于在其他项目中复用
"""

from typing import Any, Sequence, Generic, TypeVar
from abc import ABC, abstractmethod

ModelType = TypeVar("ModelType")

class DataAccessSkill(ABC, Generic[ModelType]):
    """
    数据访问技能接口

    提供标准化的数据访问能力，可在不同项目中复用
    """

    @abstractmethod
    def query(self, filters: dict[str, Any]) -> Sequence[ModelType]:
        """查询数据"""
        pass

    @abstractmethod
    def insert(self, data: ModelType) -> ModelType:
        """插入数据"""
        pass

    @abstractmethod
    def update(self, id: Any, data: dict[str, Any]) -> bool:
        """更新数据"""
        pass

    @abstractmethod
    def delete(self, id: Any) -> bool:
        """删除数据"""
        pass
```
