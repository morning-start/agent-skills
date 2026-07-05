# 常见代码模式

## 目录
1. [表单处理](#表单处理)
2. [文件上传](#文件上传)
3. [分页查询](#分页查询)
4. [错误处理](#错误处理)
5. [身份认证](#身份认证)

---

## 表单处理

### 前端表单模板
```vue
<template>
  <form @submit.prevent="handleSubmit">
    <input v-model="formData.field" type="text" />
    <button type="submit">提交</button>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const formData = reactive({
  field: ''
})

const handleSubmit = async () => {
  const response = await api.createResource(formData)
  console.log(response)
}
</script>
```

### 后端表单验证
```python
from pydantic import BaseModel, EmailStr, validator

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('密码长度至少 8 位')
        return v
```

---

## 文件上传

### 前端文件上传
```typescript
const handleFileUpload = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await uploadFile(formData)
  return response.data.url
}
```

### 后端文件处理
```python
import os
import uuid
from fastapi import UploadFile, HTTPException

async def save_upload_file(file: UploadFile, upload_dir: str) -> str:
    # 生成唯一文件名
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(upload_dir, filename)
    
    # 保存文件
    with open(filepath, 'wb') as f:
        content = await file.read()
        f.write(content)
    
    return f"/uploads/{filename}"
```

---

## 分页查询

### 前端分页请求
```typescript
interface PaginationParams {
  page: number
  page_size: number
}

const fetchUsers = async (params: PaginationParams) => {
  const response = await api.getUsers(params)
  return response.data
}
```

### 后端分页响应
```python
from fastapi import Query
from typing import List

@app.get("/users")
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    skip = (page - 1) * page_size
    users = db.query(User).offset(skip).limit(page_size).all()
    total = db.query(User).count()
    
    return {
        "items": users,
        "total": total,
        "page": page,
        "page_size": page_size
    }
```

---

## 错误处理

### 前端统一错误处理
```typescript
import axios from 'axios'

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token 过期，跳转登录
      window.location.href = '/login'
    } else if (error.response?.status === 403) {
      // 权限不足
      alert('权限不足')
    }
    return Promise.reject(error)
  }
)
```

### 后端统一错误响应
```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "data": None,
            "message": exc.detail
        }
    )
```

---

## 身份认证

### JWT Token 存储（前端）
```typescript
export const useAuthStore = defineStore('auth', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  
  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }
  
  function clearToken() {
    token.value = ''
    localStorage.removeItem('token')
  }
  
  return { token, setToken, clearToken }
})
```

### JWT Token 验证（后端）
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```
---

## 类型同步

### 前后端类型定义对照

#### 基础类型
```typescript
// 前端 TypeScript
interface User {
  id: number
  email: string
  username: string
  avatar_url: string | null
  is_active: boolean
  created_at: string  // ISO 8601
  role: UserRole
}
```

```python
# 后端 Pydantic
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    ADMIN = 'admin'
    USER = 'user'

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    avatar_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    role: UserRole
```

#### 复杂嵌套类型
```typescript
// 前端 TypeScript
interface Post {
  id: number
  title: string
  content: string
  author: User
  tags: string[]
  comments: Comment[]
  metadata: {
    views: number
    likes: number
  }
}

interface Comment {
  id: number
  content: string
  author: User
  created_at: string
}
```

```python
# 后端 Pydantic
from typing import List

class PostMetadata(BaseModel):
    views: int
    likes: int

class CommentResponse(BaseModel):
    id: int
    content: str
    author: UserResponse
    created_at: datetime

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: UserResponse
    tags: List[str]
    comments: List[CommentResponse]
    metadata: PostMetadata
```

#### 分页响应类型
```typescript
// 前端 TypeScript
interface PaginationResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  has_next: boolean
}

interface UserListResponse extends PaginationResponse<User> {
  items: User[]
}
```

```python
# 后端 Pydantic
from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field

T = TypeVar('T')

class PaginationResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int = Field(..., ge=0)
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1, le=100)
    has_next: bool

class UserListResponse(PaginationResponse[UserResponse]):
    items: List[UserResponse]
```

#### 文件上传类型
```typescript
// 前端 TypeScript
interface UploadResponse {
  file_url: string
  file_name: string
  file_size: number
  mime_type: string
}

interface UpdateAvatarRequest {
  avatar_file: File  // 原始 File 对象
}

interface UpdateAvatarResponse {
  avatar_url: string
}
```

```python
# 后端 Pydantic
from fastapi import UploadFile

class UploadResponse(BaseModel):
    file_url: str
    file_name: str
    file_size: int
    mime_type: str

class UpdateAvatarResponse(BaseModel):
    avatar_url: str
```

```python
# 后端 FastAPI 路由
@router.post("/avatar", response_model=UpdateAvatarResponse)
async def update_avatar(
    avatar_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
) -> UpdateAvatarResponse:
    # ... 业务逻辑
    return UpdateAvatarResponse(avatar_url=avatar_url)
```

#### 联合类型和枚举
```typescript
// 前端 TypeScript
export enum ContentType {
  TEXT = 'text',
  IMAGE = 'image',
  VIDEO = 'video',
  DOCUMENT = 'document'
}

interface ContentItem {
  id: number
  type: ContentType
  data: TextContent | ImageContent | VideoContent | DocumentContent
}

interface TextContent {
  text: string
}

interface ImageContent {
  url: string
  alt_text?: string
}

interface VideoContent {
  url: string
  duration: number
  thumbnail_url: string
}
```

```python
# 后端 Pydantic
from enum import Enum
from typing import Union
from pydantic import BaseModel

class ContentType(str, Enum):
    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'
    DOCUMENT = 'document'

class TextContent(BaseModel):
    text: str

class ImageContent(BaseModel):
    url: str
    alt_text: Optional[str] = None

class VideoContent(BaseModel):
    url: str
    duration: int
    thumbnail_url: str

class DocumentContent(BaseModel):
    url: str
    file_name: str
    file_size: int

ContentData = Union[TextContent, ImageContent, VideoContent, DocumentContent]

class ContentItemResponse(BaseModel):
    id: int
    type: ContentType
    data: ContentData
```

### 类型验证工具

#### 前端类型守卫
```typescript
// 前端 TypeScript
function isUser(obj: any): obj is User {
  return (
    typeof obj === 'object' &&
    typeof obj.id === 'number' &&
    typeof obj.email === 'string' &&
    typeof obj.username === 'string'
  )
}

function isPostStatus(value: any): value is PostStatus {
  return ['draft', 'published', 'archived'].includes(value)
}

// 使用示例
const data = await api.fetchUser()
if (isUser(data)) {
  console.log(data.email)  // TypeScript 知道这是 User 类型
}
```

#### 后端 Pydantic 验证器
```python
# 后端 Pydantic
from pydantic import BaseModel, validator, HttpUrl

class CreateUserRequest(BaseModel):
    email: str
    username: str
    avatar_url: Optional[str] = None
    
    @validator('email')
    def email_must_contain_at_sign(cls, v):
        if '@' not in v:
            raise ValueError('邮箱必须包含 @ 符号')
        return v
    
    @validator('avatar_url')
    def avatar_url_must_be_valid(cls, v):
        if v is not None and not v.startswith(('http://', 'https://')):
            raise ValueError('头像 URL 必须以 http:// 或 https:// 开头')
        return v
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('用户名只能包含字母和数字')
        return v
```

### 类型转换示例

#### 前端发送数据
```typescript
// 前端 TypeScript
const createPostData = {
  title: 'Hello World',
  content: 'This is a post',
  tags: ['tech', 'programming'],
  is_published: true,
  published_at: new Date().toISOString(),  // Date → ISO 8601 string
  author_id: 123
}

await api.createPost(createPostData)
```

```python
# 后端 Pydantic 接收
class CreatePostRequest(BaseModel):
    title: str
    content: str
    tags: List[str]
    is_published: bool
    published_at: datetime  # 自动解析 ISO 8601 string
    author_id: int
```

#### 后端返回数据
```python
# 后端 Pydantic 返回
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: List[str]
    is_published: bool
    published_at: datetime  # 自动序列化为 ISO 8601 string
    created_at: datetime
    updated_at: datetime
```

```typescript
// 前端 TypeScript 接收
interface Post {
  id: number
  title: string
  content: string
  tags: string[]
  is_published: boolean
  published_at: string  // ISO 8601 string
  created_at: string
  updated_at: string
}

// 格式化显示
const formatDate = (isoString: string): string => {
  return new Date(isoString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
```

### 类型同步检查脚本

#### 前端类型检查（使用 tsc）
```bash
# 检查 TypeScript 类型错误
npm run type-check
# 或
npx tsc --noEmit
```

#### 后端类型检查（使用 Pydantic）
```python
# 后端：Pydantic 自动验证类型
try:
    user = UserResponse(**data)
except ValidationError as e:
    print(f"类型验证失败: {e}")
```
