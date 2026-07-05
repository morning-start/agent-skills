# Python Rules and Best Practices

## 目录
1. Python 之禅
2. PEP 8 代码风格
3. 类型提示
4. 文档字符串
5. 测试原则
6. 性能优化
7. 安全最佳实践

## 概览
遵循 Python 的规则和最佳实践是编写高质量代码的基础。本文档总结了 Python 开发中的核心规则和建议。

## 1. Python 之禅

### 1.1 核心原则
```
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
```

### 1.2 实际应用
```python
# Beautiful: 优雅优于丑陋
# 反模式
data=[]
for i in range(10):
    data.append(i*2)

# Pythonic
data = [i * 2 for i in range(10)]

# Explicit: 明了优于隐晦
# 反模式
def process(d):
    if d:
        return [x.upper() for x in d if x]
    return []

# Pythonic
def process_documents(documents):
    if not documents:
        return []
    return [doc.upper() for doc in documents if doc]

# Simple: 简洁胜于复杂
# 反模式
def find_max(numbers):
    max_num = numbers[0]
    for i in range(1, len(numbers)):
        if numbers[i] > max_num:
            max_num = numbers[i]
    return max_num

# Pythonic
def find_max(numbers):
    return max(numbers)
```

## 2. PEP 8 代码风格

### 2.1 命名约定
```python
# 函数和变量：snake_case
def calculate_total_price():
    pass

user_name = 'Alice'

# 类：PascalCase
class UserProfile:
    pass

# 常量：UPPER_CASE
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30

# 私有变量：_prefix
_internal_variable = None

# 避免使用：camelCase
# userName = 'Alice'  # 不推荐
```

### 2.2 缩进和空格
```python
# 使用 4 个空格缩进
def function():
    if condition:
        do_something()

# 运算符周围使用空格
x = 1 + 2
result = (a + b) * (c - d)

# 逗号后使用空格
items = [1, 2, 3, 4, 5]

# 函数参数中的逗号后使用空格
def function(arg1, arg2, arg3):
    pass

# 不要在括号内添加空格
# recommended: (a, b)
# not recommended: ( a, b )
```

### 2.3 行长度
```python
# 每行不超过 79 个字符
# 反模式
very_long_variable_name = some_function_with_very_long_name(argument1, argument2, argument3)

# Pythonic: 使用括号
very_long_variable_name = some_function_with_very_long_name(
    argument1,
    argument2,
    argument3
)
```

### 2.4 导入顺序
```python
# 1. 标准库导入
import os
import sys

# 2. 第三方库导入
import requests
import numpy as np

# 3. 本地应用/库导入
from myapp import models
from myapp.utils import helper

# 每组之间用空行分隔
```

## 3. 类型提示

### 3.1 基本类型提示
```python
from typing import List, Dict, Tuple, Optional, Union, Any

def greet(name: str) -> str:
    return f'Hello, {name}!'

def process_numbers(numbers: List[int]) -> List[int]:
    return [x * 2 for x in numbers]

def get_user_info(user_id: int) -> Optional[Dict[str, Any]]:
    if user_id == 0:
        return None
    return {'name': 'Alice', 'age': 25}

def combine(value: Union[int, str]) -> str:
    return str(value)
```

### 3.2 使用 TypeVar
```python
from typing import TypeVar, List

T = TypeVar('T')

def get_first(items: List[T]) -> Optional[T]:
    if items:
        return items[0]
    return None

# 使用
numbers = [1, 2, 3]
first_number = get_first(numbers)

strings = ['a', 'b', 'c']
first_string = get_first(strings)
```

### 3.3 使用 Protocol
```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None:
        ...

def render(obj: Drawable) -> None:
    obj.draw()

class Circle:
    def draw(self) -> None:
        print('Drawing circle')

class Rectangle:
    def draw(self) -> None:
        print('Drawing rectangle')

render(Circle())
render(Rectangle())
```

## 4. 文档字符串

### 4.1 函数文档字符串
```python
def calculate_discount(price: float, discount_rate: float) -> float:
    """计算折扣后的价格.
    
    Args:
        price: 原价
        discount_rate: 折扣率（0-1之间）
        
    Returns:
        折扣后的价格
        
    Raises:
        ValueError: 如果折扣率不在有效范围内
        
    Example:
        >>> calculate_discount(100, 0.2)
        80.0
    """
    if not 0 <= discount_rate <= 1:
        raise ValueError('Discount rate must be between 0 and 1')
    return price * (1 - discount_rate)
```

### 4.2 类文档字符串
```python
class UserProfile:
    """用户资料类.
    
    这个类用于管理用户的个人信息，包括姓名、邮箱和年龄。
    
    Attributes:
        name: 用户名
        email: 用户邮箱
        age: 用户年龄
    """
    
    def __init__(self, name: str, email: str, age: int):
        """初始化用户资料.
        
        Args:
            name: 用户名
            email: 用户邮箱
            age: 用户年龄
        """
        self.name = name
        self.email = email
        self.age = age
```

### 4.3 模块文档字符串
```python
"""
用户管理模块.

这个模块提供了用户管理相关的功能，包括用户创建、验证和查询。
"""

from typing import Dict, List

def create_user(user_data: Dict) -> None:
    """创建用户."""
    pass

def get_users() -> List[Dict]:
    """获取所有用户."""
    pass
```

## 5. 测试原则

### 5.1 单元测试
```python
import unittest

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()
    
    def test_addition(self):
        result = self.calculator.add(2, 3)
        self.assertEqual(result, 5)
    
    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calculator.divide(10, 0)

if __name__ == '__main__':
    unittest.main()
```

### 5.2 使用 pytest
```python
import pytest

def test_addition():
    result = add(2, 3)
    assert result == 5

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

@pytest.mark.parametrize('a, b, expected', [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_addition_various_cases(a, b, expected):
    assert add(a, b) == expected
```

### 5.3 测试覆盖率
```python
# 运行测试并生成覆盖率报告
# pytest --cov=myapp --cov-report=html

# 目标：保持 80% 以上的测试覆盖率
```

## 6. 性能优化

### 6.1 使用生成器
```python
# 反模式：返回列表（占用大量内存）
def read_all_lines(filename):
    with open(filename) as f:
        return [line.strip() for line in f]

# Pythonic：使用生成器（节省内存）
def read_lines(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()
```

### 6.2 使用内置函数
```python
# 反模式：手动实现
def find_max(numbers):
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

# Pythonic：使用内置函数
def find_max(numbers):
    return max(numbers)
```

### 6.3 避免过早优化
```python
# 反模式：过度优化
def process_data(data):
    # 复杂的优化代码
    pass

# Pythonic：先保证正确性，再考虑性能
def process_data(data):
    # 简单、清晰的代码
    pass

# 只有在性能测试发现问题后才优化
```

## 7. 安全最佳实践

### 7.1 避免使用 eval
```python
# 反模式：危险
user_input = '__import__("os").system("rm -rf /")'
eval(user_input)  # 危险！

# Pythonic：使用 ast.literal_eval
import ast

user_input = '{"key": "value"}'
data = ast.literal_eval(user_input)  # 安全
```

### 7.2 处理用户输入
```python
# 反模式：直接拼接 SQL
query = f"SELECT * FROM users WHERE name = '{user_name}'"

# Pythonic：使用参数化查询
cursor.execute('SELECT * FROM users WHERE name = ?', (user_name,))
```

### 7.3 敏感信息处理
```python
import os
from dotenv import load_dotenv

# 反模式：硬编码敏感信息
api_key = 'my-secret-key'

# Pythonic：使用环境变量
load_dotenv()
api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError('API_KEY not found in environment variables')
```

## 示例

### 示例 1：完整的 Pythonic 函数
```python
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

def filter_and_sort_users(
    users: List[dict],
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    sort_by: str = 'name'
) -> List[dict]:
    """过滤和排序用户列表.
    
    Args:
        users: 用户列表
        min_age: 最小年龄（可选）
        max_age: 最大年龄（可选）
        sort_by: 排序字段（name 或 age）
        
    Returns:
        过滤和排序后的用户列表
        
    Raises:
        ValueError: 如果 sort_by 不是有效的排序字段
    """
    if not users:
        logger.info('Empty user list provided')
        return []
    
    # 验证排序字段
    valid_sort_fields = ['name', 'age']
    if sort_by not in valid_sort_fields:
        raise ValueError(
            f'Invalid sort_by: {sort_by}. '
            f'Must be one of {valid_sort_fields}'
        )
    
    # 过滤用户
    filtered_users = users.copy()
    
    if min_age is not None:
        filtered_users = [
            user for user in filtered_users
            if user.get('age', 0) >= min_age
        ]
    
    if max_age is not None:
        filtered_users = [
            user for user in filtered_users
            if user.get('age', 0) <= max_age
        ]
    
    # 排序用户
    sorted_users = sorted(
        filtered_users,
        key=lambda user: user.get(sort_by, '')
    )
    
    logger.info(f'Filtered {len(users)} users to {len(sorted_users)}')
    
    return sorted_users
```

### 示例 2：Pythonic 类设计
```python
from dataclasses import dataclass
from typing import List
from enum import Enum

class UserStatus(Enum):
    """用户状态枚举."""
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'

@dataclass
class User:
    """用户数据类."""
    name: str
    email: str
    age: int
    status: UserStatus = UserStatus.PENDING
    
    def __post_init__(self):
        """初始化后验证."""
        if not self.name:
            raise ValueError('Name cannot be empty')
        
        if '@' not in self.email:
            raise ValueError('Invalid email format')
        
        if self.age < 0:
            raise ValueError('Age cannot be negative')
    
    @property
    def is_adult(self) -> bool:
        """是否成年."""
        return self.age >= 18
    
    def activate(self) -> None:
        """激活用户."""
        self.status = UserStatus.ACTIVE
    
    def deactivate(self) -> None:
        """停用用户."""
        self.status = UserStatus.INACTIVE
    
    def __repr__(self) -> str:
        """字符串表示."""
        return f'User(name={self.name!r}, email={self.email!r}, status={self.status.value})'

# 使用
user = User(
    name='Alice',
    email='alice@example.com',
    age=25
)
print(user)
print(f'Is adult: {user.is_adult}')
```

### 示例 3：Pythonic 模块结构
```python
"""
用户管理模块.

提供用户创建、查询、更新和删除功能。
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class User:
    """用户数据模型."""
    id: int
    name: str
    email: str
    age: int

class UserRepository:
    """用户数据访问层."""
    
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id = 1
    
    def create(self, user_data: Dict) -> User:
        """创建用户."""
        user = User(
            id=self._next_id,
            name=user_data['name'],
            email=user_data['email'],
            age=user_data['age']
        )
        self._users[user.id] = user
        self._next_id += 1
        logger.info(f'Created user: {user.id}')
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """根据 ID 获取用户."""
        return self._users.get(user_id)
    
    def get_all(self) -> List[User]:
        """获取所有用户."""
        return list(self._users.values())
    
    def update(self, user_id: int, user_data: Dict) -> Optional[User]:
        """更新用户."""
        user = self._users.get(user_id)
        if not user:
            return None
        
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        logger.info(f'Updated user: {user_id}')
        return user
    
    def delete(self, user_id: int) -> bool:
        """删除用户."""
        if user_id in self._users:
            del self._users[user_id]
            logger.info(f'Deleted user: {user_id}')
            return True
        return False

class UserService:
    """用户服务层."""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def register_user(self, user_data: Dict) -> User:
        """注册新用户."""
        # 验证用户数据
        if not user_data.get('name'):
            raise ValueError('Name is required')
        
        if not user_data.get('email'):
            raise ValueError('Email is required')
        
        # 创建用户
        return self.repository.create(user_data)
    
    def get_user(self, user_id: int) -> Optional[User]:
        """获取用户."""
        return self.repository.get_by_id(user_id)
```
