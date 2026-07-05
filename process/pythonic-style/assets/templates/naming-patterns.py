"""
Naming Patterns Templates

Common Pythonic naming patterns and conventions.
"""

# Template 1: Variable Naming
# 使用有意义的变量名
user_name = 'Alice'
user_age = 25
is_active = True

# Template 2: Function Naming
# 使用动词或动词短语
def get_user(user_id):
    """获取用户."""
    pass

def create_user(user_data):
    """创建用户."""
    pass

def update_user(user_id, data):
    """更新用户."""
    pass

def delete_user(user_id):
    """删除用户."""
    pass

# Template 3: Class Naming
# 使用名词，PascalCase
class UserProfile:
    """用户资料."""
    pass

class DatabaseConnection:
    """数据库连接."""
    pass

class EmailService:
    """邮件服务."""
    pass

# Template 4: Constant Naming
# 使用 UPPER_CASE
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30
API_BASE_URL = 'https://api.example.com'
CACHE_EXPIRATION_TIME = 3600

# Template 5: Private Variable Naming
# 使用 _ 前缀表示内部使用
class MyClass:
    def __init__(self):
        self._internal_data = None
        self.__private_data = None
    
    @property
    def data(self):
        return self._internal_data

# Template 6: Boolean Variable Naming
# 使用 is/has/should/can 前缀
is_active = True
has_permission = True
should_retry = True
can_edit = True

# Template 7: Iterator Naming
# 使用 _ 表示不使用的变量
for _ in range(10):
    pass

for index, _ in enumerate(items):
    pass

# Template 8: Enum Naming
from enum import Enum

class UserStatus(Enum):
    """用户状态."""
    ACTIVE = 1
    INACTIVE = 2
    PENDING = 3

# Template 9: Exception Naming
# 使用 Error 后缀
class ValidationError(Exception):
    """验证错误."""
    pass

class AuthenticationError(Exception):
    """认证错误."""
    pass

# Template 10: Module Naming
# 使用小写字母和下划线
# user_profile.py
# database_connection.py
# email_service.py

# Template 11: Package Naming
# 使用小写字母和下划线
# my_package/
# user_management/
# data_processing/

# Template 12: Context Manager Naming
# 使用描述性名称
from contextlib import contextmanager

@contextmanager
def database_transaction(connection):
    """数据库事务."""
    pass

@contextmanager
def temporary_directory():
    """临时目录."""
    pass

# Template 13: Decorator Naming
# 使用描述性名称，通常以动词开头
def retry(max_attempts=3):
    """重试装饰器."""
    pass

def cache(ttl=60):
    """缓存装饰器."""
    pass

def log_call(level='INFO'):
    """日志装饰器."""
    pass

# Template 14: Test Naming
# 使用 test_ 前缀，描述测试内容
def test_user_creation():
    """测试用户创建."""
    pass

def test_user_validation():
    """测试用户验证."""
    pass

def test_user_deletion():
    """测试用户删除."""
    pass

# Template 15: Data Class Naming
from dataclasses import dataclass

@dataclass
class UserInfo:
    """用户信息."""
    name: str
    email: str
    age: int

# Template 16: Type Alias Naming
from typing import List, Dict, Optional

UserId = int
UserName = str
UserData = Dict[str, Any]
UserList = List[UserData]

# Template 17: Protocol Naming
from typing import Protocol

class Drawable(Protocol):
    """可绘制的."""
    def draw(self) -> None:
        pass

class Serializable(Protocol):
    """可序列化的."""
    def serialize(self) -> str:
        pass

# Template 18: Generator Naming
# 使用描述性名称，通常以 generate 开头
def generate_user_ids(count):
    """生成用户 ID."""
    for i in range(count):
        yield i

def generate_random_numbers(count):
    """生成随机数."""
    import random
    for _ in range(count):
        yield random.random()

# Template 19: Callback Naming
# 使用描述性名称，通常以 on_ 开头
def on_success(result):
    """成功回调."""
    pass

def on_error(error):
    """错误回调."""
    pass

def on_complete():
    """完成回调."""
    pass

# Template 20: Configuration Naming
# 使用描述性名称，通常以 config 结尾
class DatabaseConfig:
    """数据库配置."""
    HOST = 'localhost'
    PORT = 5432
    NAME = 'mydb'

class AppConfig:
    """应用配置."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your-secret-key'
