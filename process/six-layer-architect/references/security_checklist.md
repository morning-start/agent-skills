# 安全检查清单

## 目录
1. [身份认证与授权](#身份认证与授权)
2. [文件上传安全](#文件上传安全)
3. [输入验证](#输入验证)
4. [数据保护](#数据保护)
5. [API 安全](#api-安全)

---

## 身份认证与授权

### ✅ 必须检查项
- [ ] 所有需要身份认证的 API 端点都添加了 `@Depends(get_current_user)`
- [ ] JWT Token 过期时间设置合理（建议 1-7 天）
- [ ] 用户只能修改自己的资源（如头像、个人信息）
- [ ] 敏感操作（删除、修改）需要额外的权限检查
- [ ] Token 存储在 `localStorage` 或 `HttpOnly Cookie` 中

### 💡 实现建议
```python
# 后端：检查资源所有权
@app.put("/users/{user_id}/avatar")
async def update_avatar(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="无权修改他人资源")
    # ... 业务逻辑
```

---

## 文件上传安全

### ✅ 必须检查项
- [ ] 限制文件 MIME 类型（如只允许 `image/jpeg`, `image/png`）
- [ ] 限制文件大小（建议 5MB 以下）
- [ ] 文件名随机化（UUID + 时间戳），防止路径遍历攻击
- [ ] 使用 `os.path.basename()` 提取原始文件名
- [ ] 文件存储在非 Web 可访问目录或云存储

### ⚠️ 安全风险
- 未限制文件类型 → 可能上传恶意脚本（`.php`, `.js`）
- 文件名未随机化 → 可能被猜测和覆盖
- 文件大小未限制 → 可能导致服务器磁盘耗尽
- 文件存储在 Web 根目录 → 可能直接被访问执行

### 💡 实现建议
```python
# 后端：文件上传安全检查
ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/gif']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_upload_file(file: UploadFile):
    # 检查 MIME 类型
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"不支持的文件类型: {file.content_type}"
        )
    
    # 检查文件大小
    content = file.file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过 5MB")
    
    file.file.seek(0)  # 重置文件指针
    return content

def generate_safe_filename(original_filename: str) -> str:
    """生成安全的文件名"""
    ext = os.path.splitext(original_filename)[1]
    return f"{uuid.uuid4()}{ext}"
```

---

## 输入验证

### ✅ 必须检查项
- [ ] 所有用户输入都经过验证（前端 + 后端）
- [ ] 使用 Pydantic 模型进行类型验证
- [ ] 防止 SQL 注入（使用参数化查询）
- [ ] 防止 XSS 攻击（使用白名单或转义）
- [ ] 密码使用 bcrypt 哈希存储

### 💡 实现建议
```python
# 后端：使用 Pydantic 验证
from pydantic import BaseModel, EmailStr, validator, constr

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)
    username: constr(min_length=3, max_length=50)
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('用户名只能包含字母和数字')
        return v
```

---

## 数据保护

### ✅ 必须检查项
- [ ] 敏感信息（密码、Token）不在响应中返回
- [ ] 密码使用 bcrypt 哈希存储（salt + round >= 12）
- [ ] API 响应不包含调试信息（如 SQL 错误、堆栈跟踪）
- [ ] HTTPS 加密传输（生产环境）
- [ ] 数据库连接使用环境变量存储

### 💡 实现建议
```python
# 后端：密码哈希
import bcrypt

def hash_password(password: str) -> str:
    """哈希密码"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """验证密码"""
    return bcrypt.checkpw(
        password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

# 后端：不返回敏感信息
class UserResponse(BaseModel):
    id: int
    email: str
    avatar_url: Optional[str] = None
    # ❌ 不返回 password_hash, token 等敏感字段
```

---

## API 安全

### ✅ 必须检查项
- [ ] 使用 HTTPS（生产环境）
- [ ] API 限流（Rate Limiting）防止 DDoS
- [ ] CORS 配置正确（只允许信任的域名）
- [ ] 统一错误处理，不暴露服务器信息
- [ ] 敏感 API 使用 POST 而非 GET

### 💡 实现建议
```python
# 后端：CORS 配置
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # 允许的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 后端：API 限流
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/login")
@limiter.limit("5/minute")  # 每分钟最多 5 次请求
async def login(request: Request, credentials: LoginRequest):
    # ... 登录逻辑
```

---

## 常见安全问题与解决方案

| 问题 | 风险 | 解决方案 |
|------|------|---------|
| 未验证文件类型 | 上传恶意脚本 | 使用白名单限制 MIME 类型 |
| 文件名未随机化 | 路径遍历攻击 | UUID + 时间戳生成文件名 |
| 明文存储密码 | 数据泄露后账户被盗 | bcrypt 哈希存储 |
| 未验证用户权限 | 修改他人资源 | 检查 `current_user.id == resource.owner_id` |
| 暴露调试信息 | 泄露服务器结构 | 统一错误处理，不返回堆栈跟踪 |
| 无请求限流 | DDoS 攻击 | 使用 `slowapi` 限制请求频率 |
