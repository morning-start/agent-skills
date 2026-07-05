# 六层架构详细说明

## 目录
1. [架构概览](#架构概览)
2. [前端 UI 层](#前端-ui-层vue-3--tailwind)
3. [前端服务层](#前端服务层pinia-store)
4. [前端 API 层](#前端-api-层axios--typescript)
5. [后端 API 层](#后端-api-层fastapi--pydantic)
6. [后端服务层](#后端服务层service-类)
7. [数据层](#数据层sqlalchemy--postgresql)
8. [跨层数据流](#跨层数据流)

## 架构概览

### 分层原则
每层只负责自己的职责，通过明确定义的接口与其他层交互：
- **前端**：负责用户交互和数据展示
- **后端**：负责业务逻辑和数据处理
- **数据库**：负责数据持久化

### 技术栈
- **前端**：Vue 3 + TypeScript + Tailwind CSS + Pinia + Axios
- **后端**：FastAPI + Python 3.9+ + Pydantic + SQLAlchemy
- **数据库**：PostgreSQL 14+（或 MongoDB）

### 通信协议
- **前后端通信**：RESTful API + JSON
- **身份认证**：JWT（JSON Web Token）
- **文件上传**：multipart/form-data

---

## 前端 UI 层（Vue 3 + Tailwind）

### 职责
- 用户界面渲染和交互
- 表单输入和数据收集
- 用户反馈显示（加载状态、错误提示、成功提示）

### 核心约束
- 使用 `<script setup>` 语法和组合式 API
- 样式使用 Tailwind CSS 类名
- 不包含业务逻辑，只负责 UI 交互
- 通过调用前端服务层或 API 层获取数据

### 常见模式

#### 表单组件模板
```vue
<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4">标题</h2>
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-sm font-medium mb-1">字段名称</label>
        <input 
          v-model="formData.fieldName"
          type="text" 
          class="w-full px-3 py-2 border rounded"
          required
        />
      </div>
      <button 
        type="submit" 
        :disabled="loading"
        class="px-4 py-2 bg-blue-500 text-white rounded"
      >
        提交
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const loading = ref(false)
const formData = ref({
  fieldName: ''
})

const handleSubmit = async () => {
  // 调用 API 层
}
</script>
```

#### 文件上传组件模板
```vue
<template>
  <div>
    <input 
      type="file" 
      @change="handleFileChange"
      accept="image/*"
    />
    <img v-if="previewUrl" :src="previewUrl" class="w-32 h-32 rounded" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const previewUrl = ref('')
const selectedFile = ref<File | null>(null)

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    selectedFile.value = file
    previewUrl.value = URL.createObjectURL(file)
  }
}
</script>
```

---

## 前端服务层（Pinia Store）

### 职责
- 状态管理（应用全局状态）
- 业务逻辑封装
- 数据缓存和持久化
- 与 API 层交互

### 核心约束
- 使用 `defineStore` 定义 store
- 根据需求决定是否持久化（`usePersist` 插件）
- 不直接操作 DOM，只管理数据和逻辑
- 通过 actions 调用 API 层

### 常见模式

#### 基础 Store 模板
```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface UserState {
  currentUser: User | null
  token: string
}

export const useUserStore = defineStore('user', () => {
  // State
  const currentUser = ref<User | null>(null)
  const token = ref('')

  // Actions
  async function login(email: string, password: string) {
    const response = await loginApi(email, password)
    currentUser.value = response.data.user
    token.value = response.data.token
    localStorage.setItem('token', token.value)
  }

  // Getters
  const isAuthenticated = computed(() => !!token.value)

  return {
    currentUser,
    token,
    login,
    isAuthenticated
  }
}, {
  persist: true  // 持久化到 localStorage
})
```

---

## 前端 API 层（Axios + TypeScript）

### 职责
- 封装 HTTP 请求
- 定义 TypeScript 接口
- 统一错误处理
- Token 管理

### 核心约束
- 使用 axios 发送 HTTP 请求
- 定义明确的 TypeScript 接口
- 统一响应格式处理
- 自动添加 Authorization header

### 常见模式

#### API 函数模板
```typescript
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

// 接口定义
export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  user: User
  token: string
}

// API 函数
export async function login(data: LoginRequest): Promise<LoginResponse> {
  const response = await axios.post(`${API_BASE_URL}/auth/login`, data)
  return response.data
}

export async function uploadAvatar(file: File): Promise<{ avatar_url: string }> {
  const formData = new FormData()
  formData.append('avatarFile', file)
  
  const response = await axios.post(`${API_BASE_URL}/users/avatar`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return response.data
}
```

---

## 后端 API 层（FastAPI + Pydantic）

### 职责
- 定义 API 路由
- 请求参数验证
- 响应格式标准化
- 身份认证中间件

### 核心约束
- 使用 FastAPI 路由装饰器
- 使用 Pydantic 模型定义请求/响应
- 统一响应格式：`{ code, data, message }`
- 使用 `Depends` 处理依赖注入（如当前用户）

### 常见模式

#### 路由模板
```python
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

class UpdateAvatarResponse(BaseModel):
    code: int
    data: dict
    message: str

@router.post("/avatar", response_model=UpdateAvatarResponse)
async def update_avatar(
    avatarFile: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """更新用户头像"""
    try:
        # 调用服务层
        avatar_url = await user_service.update_avatar(current_user.id, avatarFile)
        
        return UpdateAvatarResponse(
            code=200,
            data={"avatar_url": avatar_url},
            message="头像更新成功"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

## 后端服务层（Service 类）

### 职责
- 核心业务逻辑
- 数据验证和处理
- 调用数据层
- 返回业务结果

### 核心约束
- 不包含 HTTP 相关逻辑（由 API 层处理）
- 处理业务规则和验证
- 调用 Repository 或 Model
- 抛出业务异常（由 API 层捕获）

### 常见模式

#### Service 类模板
```python
class UserService:
    def __init__(self, db_session):
        self.db = db_session
        self.user_repository = UserRepository(db_session)
    
    async def update_avatar(self, user_id: int, file: UploadFile) -> str:
        """更新用户头像"""
        # 验证用户存在
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")
        
        # 验证文件类型
        allowed_types = ['image/jpeg', 'image/png']
        if file.content_type not in allowed_types:
            raise ValueError(f"不支持的文件类型: {file.content_type}")
        
        # 保存文件
        filename = self._generate_unique_filename(file.filename)
        file_path = f"uploads/avatars/{filename}"
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        # 更新数据库
        avatar_url = f"/uploads/avatars/{filename}"
        user.avatar_url = avatar_url
        self.db.commit()
        
        return avatar_url
```

---

## 数据层（SQLAlchemy + PostgreSQL）

### 职责
- 数据持久化
- 数据模型定义
- 查询和 CRUD 操作
- 数据库迁移

### 核心约束
- 使用 SQLAlchemy ORM
- 使用 Alembic 管理迁移
- 字段类型与数据库一致
- 定义索引和约束

### 常见模式

#### Model 模板
```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    avatar_url = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### Repository 模式
```python
class UserRepository:
    def __init__(self, db_session):
        self.db = db_session
    
    def get_by_id(self, id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, **kwargs) -> User:
        user = User(**kwargs)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user
```

---

## 前后端类型映射规则

### 类型对应关系表

| TypeScript 类型 | Pydantic 类型 | 数据库类型 | 说明 |
|----------------|---------------|-----------|------|
| `string` | `str` | `VARCHAR` / `TEXT` | 字符串 |
| `number` | `int` / `float` | `INTEGER` / `NUMERIC` | 数字 |
| `boolean` | `bool` | `BOOLEAN` | 布尔值 |
| `Date` | `datetime` | `TIMESTAMP` | 日期时间 |
| `string` (Email) | `EmailStr` | `VARCHAR(255)` | 邮箱地址 |
| `string` (URL) | `HttpUrl` | `VARCHAR(500)` | URL 地址 |
| `string` (UUID) | `UUID4` | `UUID` / `CHAR(36)` | UUID |
| `Array<T>` | `List[T]` | `JSONB` / `ARRAY` | 数组/列表 |
| `T \| null` | `Optional[T]` | `NULL` | 可选类型 |
| `T \| U \| V` | `Union[T, U, V]` | - | 联合类型 |
| `Enum<T>` | `Enum` | `VARCHAR` / `ENUM` | 枚举类型 |

### 字段命名规则

**最佳实践：前后端统一使用蛇形命名（snake_case）**

```typescript
// ❌ 不推荐：前端使用驼峰命名
interface User {
  firstName: string
  lastName: string
  avatarUrl: string
}

// ✅ 推荐：前后端统一使用蛇形命名
interface User {
  first_name: string
  last_name: string
  avatar_url: string
}
```

```python
# 后端 Pydantic
class UserResponse(BaseModel):
    first_name: str
    last_name: str
    avatar_url: Optional[str] = None

# 后端 SQLAlchemy
class User(Base):
    first_name = Column(String(100))
    last_name = Column(String(100))
    avatar_url = Column(String(256), nullable=True)
```

### 空值处理

```typescript
// 前端 TypeScript
interface User {
  id: number
  email: string
  avatar_url: string | null  // 可选，可为 null
  bio?: string  // 可选，可为 undefined
}

// 使用可选链访问
const avatar = user?.avatar_url ?? '/default-avatar.png'
```

```python
# 后端 Pydantic
from typing import Optional

class UserResponse(BaseModel):
    id: int
    email: str
    avatar_url: Optional[str] = None  # 对应前端 string | null
    bio: Optional[str] = None  # 对应前端 string | undefined
```

### 日期时间格式

**前端 → 后端**：
- 前端发送：ISO 8601 格式字符串
- 示例：`2024-01-01T00:00:00Z` 或 `2024-01-01T08:00:00+08:00`

```typescript
// 前端发送日期
const createPostRequest = {
  title: 'Hello World',
  published_at: new Date().toISOString()  // ISO 8601 格式
}
```

**后端 → 前端**：
- 后端返回：JSON 序列化为 ISO 8601 格式
- 前端接收：`new Date()` 解析

```typescript
// 前端接收日期
interface Post {
  title: string
  published_at: string  // ISO 8601 格式字符串
}

// 格式化显示
const formattedDate = new Date(post.published_at).toLocaleDateString('zh-CN')
```

```python
# 后端 Pydantic
from datetime import datetime

class PostResponse(BaseModel):
    title: str
    published_at: datetime  # 自动序列化为 ISO 8601 格式
```

### 枚举类型同步

```typescript
// 前端 TypeScript
export enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  GUEST = 'guest'
}

export enum PostStatus {
  DRAFT = 'draft',
  PUBLISHED = 'published',
  ARCHIVED = 'archived'
}
```

```python
# 后端 Pydantic
from enum import Enum

class UserRole(str, Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'

class PostStatus(str, Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'

class UserResponse(BaseModel):
    id: int
    email: str
    role: UserRole  # 枚举类型

class PostResponse(BaseModel):
    id: int
    title: str
    status: PostStatus  # 枚举类型
```

```python
# 后端 SQLAlchemy
from sqlalchemy import Column, String, Enum as SQLEnum

class User(Base):
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
```

### 验证规则同步

**字符串长度验证**：
```typescript
// 前端 HTML 表单
<input 
  v-model="formData.username"
  type="text"
  minlength="3"
  maxlength="50"
  required
/>
```

```python
# 后端 Pydantic
from pydantic import BaseModel, Field

class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
```

**邮箱验证**：
```typescript
// 前端
<input 
  v-model="formData.email"
  type="email"
  required
/>
```

```python
# 后端 Pydantic
from pydantic import BaseModel, EmailStr

class CreateUserRequest(BaseModel):
    email: EmailStr  # 自动验证邮箱格式
```

**自定义验证**：
```typescript
// 前端自定义验证
const validatePassword = (password: string): boolean => {
  return password.length >= 8 && /[A-Z]/.test(password) && /[0-9]/.test(password)
}
```

```python
# 后端 Pydantic 自定义验证
from pydantic import BaseModel, validator

class CreateUserRequest(BaseModel):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('密码长度至少 8 位')
        if not any(c.isupper() for c in v):
            raise ValueError('密码必须包含大写字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含数字')
        return v
```

### 复杂类型嵌套

```typescript
// 前端 TypeScript
interface User {
  id: number
  email: string
  posts: Post[]  // 嵌套数组
  metadata: {
    last_login_at: string
    login_count: number
  }
}

interface Post {
  id: number
  title: string
  status: PostStatus
  comments: Comment[]
}

interface Comment {
  id: number
  content: string
  author: {
    id: number
    username: string
  }
}
```

```python
# 后端 Pydantic
from typing import List, Dict

class CommentAuthor(BaseModel):
    id: int
    username: str

class CommentResponse(BaseModel):
    id: int
    content: str
    author: CommentAuthor

class PostResponse(BaseModel):
    id: int
    title: str
    status: PostStatus
    comments: List[CommentResponse]

class UserMetadata(BaseModel):
    last_login_at: datetime
    login_count: int

class UserResponse(BaseModel):
    id: int
    email: str
    posts: List[PostResponse]
    metadata: UserMetadata
```

### 类型同步检查清单

- [ ] 前端 TypeScript 接口与后端 Pydantic 模型字段名完全一致
- [ ] 字段类型对应关系正确（参考类型映射表）
- [ ] 可选字段使用 `Optional[T]` / `T | null` 标记
- [ ] 日期时间使用 ISO 8601 格式
- [ ] 枚举类型值完全一致
- [ ] 验证规则（长度、格式）前后端一致
- [ ] 嵌套对象和数组类型结构一致
- [ ] 字段命名统一使用 snake_case 或 camel_case（推荐 snake_case）
                                                         ↓
后端 API 层                后端服务层              数据层
avatarFile: UploadFile  →  验证 + 保存文件    →   user.avatar_url = url
                                                      ↓
响应: { code, data, message }                ←   commit()
                                                         ↓
                                                      HTTP 200
                                                         ↓
前端 API 层                前端服务层              UI 层
响应.data.avatar_url     →   currentUser.avatarUrl →   <img :src="currentUser.avatarUrl" />
```

### 字段名映射规则
- 前端：驼峰命名（camelCase）→ `avatarFile`, `firstName`
- 后端：蛇形命名（snake_case）→ `avatar_file`, `first_name`
- 数据库：蛇形命名（snake_case）→ `avatar_url`, `first_name`

### 类型映射规则
| 前端 TypeScript | 后端 Pydantic | 数据库 |
|----------------|---------------|--------|
| string | str | VARCHAR / TEXT |
| number | int / float | INTEGER / NUMERIC |
| boolean | bool | BOOLEAN |
| Date | datetime | TIMESTAMP |
| File | UploadFile | TEXT (存储 URL) |
| Array<T> | List[T] | JSONB / ARRAY |
