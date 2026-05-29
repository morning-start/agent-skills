# Function Returning Tips

## 目录
1. 函数设计原则
2. 函数参数设计
3. 返回值设计
4. 函数文档
5. 类型提示
6. 高阶函数
7. 装饰器

## 概览
良好的函数设计是编写可维护、可测试代码的基础。函数应该短小、专注、职责单一。本章基于《One Python Craftsman》第5章内容。

## 1. 函数设计原则

### 1.1 单一职责原则
**反模式**：
```python
def process_user_data(user_data):
    # 验证数据
    if not user_data.get('name'):
        raise ValueError('Name is required')
    
    # 格式化数据
    formatted_data = {
        'name': user_data['name'].strip().title(),
        'email': user_data['email'].lower().strip(),
    }
    
    # 保存到数据库
    db.insert(formatted_data)
    
    # 发送邮件
    send_email(formatted_data['email'])
    
    # 记录日志
    log.info(f'User created: {formatted_data["name"]}')
```

**Pythonic**：
```python
def validate_user_data(user_data):
    """验证用户数据."""
    if not user_data.get('name'):
        raise ValueError('Name is required')

def format_user_data(user_data):
    """格式化用户数据."""
    return {
        'name': user_data['name'].strip().title(),
        'email': user_data['email'].lower().strip(),
    }

def save_user_to_db(user_data):
    """保存用户到数据库."""
    db.insert(user_data)

def send_welcome_email(user_data):
    """发送欢迎邮件."""
    send_email(user_data['email'])

def log_user_creation(user_data):
    """记录用户创建日志."""
    log.info(f'User created: {user_data["name"]}')

def process_user_data(user_data):
    """处理用户数据（协调函数）."""
    validate_user_data(user_data)
    formatted_data = format_user_data(user_data)
    save_user_to_db(formatted_data)
    send_welcome_email(formatted_data)
    log_user_creation(formatted_data)
```

### 1.2 保持函数简短
**反模式**：
```python
def complex_function(data):
    # 100+ 行代码
    # 做了很多事情
    pass
```

**Pythonic**：
```python
def complex_function(data):
    """复杂函数的入口点."""
    validated = validate_data(data)
    processed = process_data(validated)
    result = format_result(processed)
    return result

def validate_data(data):
    """验证数据."""
    pass

def process_data(data):
    """处理数据."""
    pass

def format_result(data):
    """格式化结果."""
    pass
```

## 2. 函数参数设计

### 2.1 使用关键字参数提高可读性
**反模式**：
```python
def send_email(to, subject, body, priority, cc, bcc):
    pass

# 难以理解参数的含义
send_email('user@example.com', 'Hello', 'Content', 1, 'cc@example.com', 'bcc@example.com')
```

**Pythonic**：
```python
def send_email(to, subject, body, *, priority=1, cc=None, bcc=None):
    pass

# 清晰明了
send_email(
    to='user@example.com',
    subject='Hello',
    body='Content',
    priority=1,
    cc='cc@example.com',
    bcc='bcc@example.com'
)
```

### 2.2 避免过多的参数
**反模式**：
```python
def create_user(name, email, age, city, country, phone, address, postal_code):
    pass
```

**Pythonic**：
```python
from dataclasses import dataclass

@dataclass
class UserData:
    name: str
    email: str
    age: int
    city: str
    country: str
    phone: str
    address: str
    postal_code: str

def create_user(user_data: UserData):
    pass

# 使用
user_data = UserData(
    name='Alice',
    email='alice@example.com',
    age=25,
    city='New York',
    country='USA',
    phone='123-456-7890',
    address='123 Main St',
    postal_code='10001'
)
create_user(user_data)
```

### 2.3 使用默认参数
```python
def connect_to_database(
    host='localhost',
    port=5432,
    database='mydb',
    username='user',
    password='password'
):
    pass

# 使用默认值
connect_to_database()

# 覆盖部分参数
connect_to_database(host='production.db')
```

### 2.4 使用 *args 和 **kwargs
```python
def log_message(message, *args, **kwargs):
    """记录消息，支持额外的参数."""
    timestamp = kwargs.get('timestamp', datetime.now())
    level = kwargs.get('level', 'INFO')
    print(f'[{timestamp}] {level}: {message}')

log_message('Hello')
log_message('Hello', timestamp=datetime.now(), level='WARNING')
```

## 3. 返回值设计

### 3.1 返回一致性
**反模式**：
```python
def get_user(user_id):
    if user_id == 1:
        return {'name': 'Alice', 'age': 25}
    elif user_id == 2:
        return None
    else:
        return {'error': 'User not found'}
```

**Pythonic**：
```python
def get_user(user_id):
    """获取用户，返回用户对象或 None."""
    if user_id == 1:
        return {'name': 'Alice', 'age': 25}
    return None
```

### 3.2 返回元组替代多个返回值
**反模式**：
```python
def get_stats():
    return 10, 20, 30

count = get_stats()[0]
avg = get_stats()[1]
total = get_stats()[2]
```

**Pythonic**：
```python
def get_stats():
    """返回统计信息."""
    count, avg, total = 10, 20, 30
    return count, avg, total

# 解包
count, avg, total = get_stats()

# 忽略某些值
count, _, total = get_stats()
```

### 3.3 返回命名元组
```python
from collections import namedtuple

# 传统方式
def get_position():
    return 10, 20, 30
x, y, z = get_position()

# 命名元组
Position = namedtuple('Position', ['x', 'y', 'z'])

def get_position():
    """返回位置."""
    return Position(10, 20, 30)

pos = get_position()
print(pos.x)  # 10
print(pos.y)  # 20
print(pos.z)  # 30
```

### 3.4 返回数据类
```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    age: int

def get_user(user_id):
    """获取用户."""
    if user_id == 1:
        return User(name='Alice', email='alice@example.com', age=25)
    return None

user = get_user(1)
if user:
    print(user.name)  # Alice
    print(user.email)  # alice@example.com
```

### 3.5 返回字典的替代方案
**反模式**：
```python
def process_data(data):
    result = {}
    result['success'] = True
    result['data'] = data
    result['message'] = 'Processed successfully'
    return result
```

**Pythonic**：
```python
from dataclasses import dataclass

@dataclass
class ProcessResult:
    success: bool
    data: any
    message: str

def process_data(data):
    """处理数据."""
    return ProcessResult(
        success=True,
        data=data,
        message='Processed successfully'
    )
```

### 3.6 返回生成器
**反模式**：
```python
def get_all_users():
    users = []
    for user_id in range(1000):
        user = fetch_user(user_id)
        users.append(user)
    return users
```

**Pythonic**：
```python
def get_all_users():
    """生成用户."""
    for user_id in range(1000):
        user = fetch_user(user_id)
        yield user

# 使用
for user in get_all_users():
    process(user)
```

## 4. 函数文档

### 4.1 使用 docstring
```python
def calculate_distance(point1, point2):
    """
    计算两点之间的距离.
    
    Args:
        point1 (tuple): 第一个点的坐标 (x, y)
        point2 (tuple): 第二个点的坐标 (x, y)
    
    Returns:
        float: 两点之间的距离
    
    Examples:
        >>> calculate_distance((0, 0), (3, 4))
        5.0
    """
    x1, y1 = point1
    x2, y2 = point2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
```

### 4.2 Google 风格
```python
def send_email(to, subject, body, cc=None, bcc=None):
    """发送邮件.
    
    Args:
        to (str): 收件人邮箱
        subject (str): 邮件主题
        body (str): 邮件正文
        cc (str, optional): 抄送邮箱. Defaults to None.
        bcc (str, optional): 密送邮箱. Defaults to None.
    
    Returns:
        bool: 是否发送成功
    
    Raises:
        ValueError: 邮箱格式不正确
    
    Examples:
        >>> send_email('user@example.com', 'Hello', 'Content')
        True
    """
    pass
```

## 5. 类型提示

### 5.1 基本类型提示
```python
def add(a: int, b: int) -> int:
    """添加两个整数."""
    return a + b

def greet(name: str) -> str:
    """问候."""
    return f'Hello, {name}'

def process_items(items: list[str]) -> dict[str, int]:
    """处理项目."""
    return {item: len(item) for item in items}
```

### 5.2 可选类型
```python
from typing import Optional

def get_user(user_id: int) -> Optional[dict]:
    """获取用户."""
    if user_id == 1:
        return {'name': 'Alice'}
    return None
```

### 5.3 联合类型
```python
from typing import Union

def process(value: Union[int, str]) -> str:
    """处理值."""
    return str(value)

# Python 3.10+
def process(value: int | str) -> str:
    """处理值."""
    return str(value)
```

### 5.4 类型别名
```python
from typing import Dict, List, Tuple

UserInfo = Dict[str, any]
Coordinates = Tuple[float, float]

def process_users(users: List[UserInfo]) -> List[Coordinates]:
    """处理用户."""
    return [(user['x'], user['y']) for user in users]
```

### 5.5 泛型
```python
from typing import TypeVar, List

T = TypeVar('T')

def first(items: List[T]) -> Optional[T]:
    """获取第一个元素."""
    return items[0] if items else None

# 使用
first_int = first([1, 2, 3])  # Optional[int]
first_str = first(['a', 'b', 'c'])  # Optional[str]
```

## 6. 高阶函数

### 6.1 函数作为参数
```python
def apply_function(items, func):
    """对每个项目应用函数."""
    return [func(item) for item in items]

# 使用
numbers = [1, 2, 3, 4, 5]
squared = apply_function(numbers, lambda x: x ** 2)
```

### 6.2 函数作为返回值
```python
def create_multiplier(factor):
    """创建乘法器."""
    def multiplier(x):
        return x * factor
    return multiplier

times_three = create_multiplier(3)
print(times_three(5))  # 15
```

### 6.3 装饰器
```python
def timer(func):
    """计时装饰器."""
    import time
    
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} took {end - start:.4f} seconds')
        return result
    return wrapper

@timer
def slow_function():
    """慢函数."""
    import time
    time.sleep(1)

slow_function()
```

### 6.4 使用 functools
```python
from functools import partial, reduce, lru_cache

# partial（偏函数）
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))  # 125

# reduce（归约）
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda x, y: x + y, numbers)  # 15

# lru_cache（缓存）
@lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

## 7. 函数式编程

### 7.1 map
```python
# 使用 map 映射函数
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))  # [1, 4, 9, 16, 25]

# 使用内置函数
upper = list(map(str.upper, ['hello', 'world']))  # ['HELLO', 'WORLD']
```

### 7.2 filter
```python
# 使用 filter 过滤
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4, 6]

# 过滤 None
values = [1, None, 2, None, 3]
filtered = list(filter(None, values))  # [1, 2, 3]
```

### 7.3 lambda 函数
```python
# 简单的 lambda
add = lambda x, y: x + y
print(add(3, 5))  # 8

# 使用 lambda 进行排序
users = [
    {'name': 'Alice', 'age': 25},
    {'name': 'Bob', 'age': 30},
    {'name': 'Charlie', 'age': 20}
]
sorted_users = sorted(users, key=lambda x: x['age'])
```

## 示例

### 示例 1：返回值最佳实践
```python
from dataclasses import dataclass

@dataclass
class CalculationResult:
    """计算结果."""
    success: bool
    value: float
    error: str

def divide(a: float, b: float) -> CalculationResult:
    """除法运算."""
    if b == 0:
        return CalculationResult(
            success=False,
            value=0.0,
            error='Division by zero'
        )
    
    return CalculationResult(
        success=True,
        value=a / b,
        error=''
    )

# 使用
result = divide(10, 2)
if result.success:
    print(f'Result: {result.value}')
else:
    print(f'Error: {result.error}')
```

### 示例 2：函数参数设计
```python
def process_data(
    data: list[dict],
    *,
    validate: bool = True,
    transform: bool = True,
    save: bool = False
) -> list[dict]:
    """
    处理数据.
    
    Args:
        data: 要处理的数据
        validate: 是否验证数据
        transform: 是否转换数据
        save: 是否保存数据
    """
    if validate:
        data = [validate_item(item) for item in data]
    
    if transform:
        data = [transform_item(item) for item in data]
    
    if save:
        save_to_database(data)
    
    return data

# 使用
data = [{'name': 'Alice'}, {'name': 'Bob'}]
result = process_data(data, validate=True, save=True)
```

### 示例 3：高阶函数
```python
from typing import Callable, List

def filter_and_map(
    items: List[any],
    predicate: Callable[[any], bool],
    transformer: Callable[[any], any]
) -> List[any]:
    """
    过滤并映射数据.
    
    Args:
        items: 要处理的项目
        predicate: 过滤条件函数
        transformer: 转换函数
    """
    filtered = filter(predicate, items)
    return list(map(transformer, filtered))

# 使用
numbers = [1, 2, 3, 4, 5, 6]
result = filter_and_map(
    numbers,
    predicate=lambda x: x % 2 == 0,
    transformer=lambda x: x ** 2
)
# [4, 16, 36]
```

### 示例 4：类型提示
```python
from typing import List, Dict, Optional, Union

UserInfo = Dict[str, Union[str, int]]

def validate_user(user: UserInfo) -> bool:
    """验证用户数据."""
    required_fields = ['name', 'email', 'age']
    return all(field in user for field in required_fields)

def process_users(users: List[UserInfo]) -> List[str]:
    """处理用户列表."""
    valid_users = [user for user in users if validate_user(user)]
    return [user['name'] for user in valid_users]

# 使用
users = [
    {'name': 'Alice', 'email': 'alice@example.com', 'age': 25},
    {'name': 'Bob', 'email': 'bob@example.com', 'age': 30}
]
names = process_users(users)
```

### 示例 5：装饰器
```python
from functools import wraps
import time

def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    重试装饰器.
    
    Args:
        max_attempts: 最大尝试次数
        delay: 重试延迟（秒）
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2.0)
def fetch_data():
    """获取数据."""
    # 可能失败的操作
    pass
```
