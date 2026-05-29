# Edge Cases

## 目录
1. 空值处理
2. 边界值处理
3. 类型检查
4. 异常情况
5. 并发问题
6. 性能边界

## 概览
处理边界情况是编写健壮代码的关键。良好的代码应该能够优雅地处理各种异常和边界情况。

## 1. 空值处理

### 1.1 检查 None
**反模式**：
```python
def process_user(user):
    if user is None or user == '':
        return None
    return user.upper()
```

**Pythonic**：
```python
def process_user(user):
    if not user:
        return None
    return user.upper()
```

### 1.2 提供默认值
```python
# 使用 get 方法
user_data = {'name': 'Alice', 'age': 25}
email = user_data.get('email', 'default@example.com')

# 使用 or 运算符
email = user_email or 'default@example.com'

# 使用 walrus operator (Python 3.8+)
if (email := user_email) and '@' in email:
    process_email(email)
```

### 1.3 处理空容器
```python
# 检查空列表
items = []
if not items:
    print('No items')

# 检查空字典
data = {}
if not data:
    print('No data')

# 检查空字符串
text = ''
if not text:
    print('Empty text')
```

## 2. 边界值处理

### 2.1 数值边界
```python
def validate_age(age):
    """验证年龄."""
    if age is None:
        raise ValueError('Age cannot be None')
    
    if not isinstance(age, (int, float)):
        raise TypeError('Age must be a number')
    
    if age < 0:
        raise ValueError(f'Age cannot be negative: {age}')
    
    if age > 150:
        raise ValueError(f'Age seems unrealistic: {age}')
    
    return age

def calculate_discount(price, discount_rate):
    """计算折扣."""
    if price is None or discount_rate is None:
        raise ValueError('Price and discount rate cannot be None')
    
    if price < 0:
        raise ValueError(f'Price cannot be negative: {price}')
    
    if not 0 <= discount_rate <= 1:
        raise ValueError(f'Discount rate must be between 0 and 1: {discount_rate}')
    
    return price * (1 - discount_rate)
```

### 2.2 索引边界
```python
def get_item(items, index, default=None):
    """安全获取列表项."""
    if not isinstance(index, int):
        raise TypeError('Index must be an integer')
    
    if 0 <= index < len(items):
        return items[index]
    
    return default

# 或者使用 try-except
def get_item_v2(items, index):
    """使用异常处理获取列表项."""
    try:
        return items[index]
    except (IndexError, TypeError):
        return None
```

### 2.3 分页边界
```python
def paginate(items, page=1, page_size=10):
    """分页处理."""
    if not items:
        return {
            'items': [],
            'total': 0,
            'page': page,
            'page_size': page_size,
            'total_pages': 0
        }
    
    if page < 1:
        raise ValueError('Page must be at least 1')
    
    if page_size < 1:
        raise ValueError('Page size must be at least 1')
    
    total = len(items)
    total_pages = (total + page_size - 1) // page_size
    
    if page > total_pages:
        return {
            'items': [],
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages
        }
    
    start = (page - 1) * page_size
    end = start + page_size
    
    return {
        'items': items[start:end],
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages
    }
```

## 3. 类型检查

### 3.1 基本类型检查
```python
def process_number(number):
    """处理数字."""
    if number is None:
        raise ValueError('Number cannot be None')
    
    if not isinstance(number, (int, float)):
        raise TypeError(f'Expected number, got {type(number)}')
    
    if isinstance(number, bool):
        raise TypeError('Boolean is not a valid number')
    
    return number * 2
```

### 3.2 使用 typing 进行类型提示
```python
from typing import List, Dict, Optional, Union

def process_items(items: List[str]) -> Dict[str, int]:
    """处理项目列表."""
    if not isinstance(items, list):
        raise TypeError(f'Expected list, got {type(items)}')
    
    return {item: len(item) for item in items}

def get_value(data: Dict[str, int], key: str) -> Optional[int]:
    """获取字典值."""
    if not isinstance(data, dict):
        raise TypeError(f'Expected dict, got {type(data)}')
    
    return data.get(key)
```

### 3.3 使用 TypeGuard (Python 3.10+)
```python
from typing import TypeGuard

def is_string(value: Any) -> TypeGuard[str]:
    """类型守卫."""
    return isinstance(value, str)

def process_value(value: Any):
    """处理值."""
    if is_string(value):
        return value.upper()
    elif isinstance(value, (int, float)):
        return value * 2
    else:
        raise TypeError(f'Unsupported type: {type(value)}')
```

## 4. 异常情况

### 4.1 文件操作
```python
from pathlib import Path

def read_file_safe(filename):
    """安全读取文件."""
    path = Path(filename)
    
    if not path.exists():
        raise FileNotFoundError(f'File not found: {filename}')
    
    if not path.is_file():
        raise ValueError(f'Not a file: {filename}')
    
    try:
        return path.read_text(encoding='utf-8')
    except PermissionError:
        raise PermissionError(f'Permission denied: {filename}')
    except UnicodeDecodeError as e:
        raise ValueError(f'Encoding error: {e}')
```

### 4.2 网络请求
```python
import requests
from requests.exceptions import RequestException

def fetch_url(url, timeout=30):
    """获取 URL 内容."""
    if not url:
        raise ValueError('URL cannot be empty')
    
    if not url.startswith(('http://', 'https://')):
        raise ValueError('Invalid URL format')
    
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        raise TimeoutError(f'Request timeout: {url}')
    except requests.ConnectionError:
        raise ConnectionError(f'Connection error: {url}')
    except requests.HTTPError as e:
        raise RuntimeError(f'HTTP error {e.response.status_code}: {url}')
    except requests.RequestException as e:
        raise RuntimeError(f'Request failed: {e}')
```

### 4.3 数据库操作
```python
def execute_query(query, params=None):
    """执行数据库查询."""
    if not query:
        raise ValueError('Query cannot be empty')
    
    if params is None:
        params = {}
    
    if not isinstance(params, dict):
        raise TypeError('Params must be a dictionary')
    
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except OperationalError as e:
        raise RuntimeError(f'Database error: {e}')
    except DatabaseError as e:
        raise RuntimeError(f'Database error: {e}')
```

## 5. 并发问题

### 5.1 竞态条件
```python
import threading

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    def increment(self):
        """线程安全的增量."""
        with self.lock:
            self.value += 1
    
    def get(self):
        """线程安全的获取."""
        with self.lock:
            return self.value

counter = Counter()

def worker():
    for _ in range(1000):
        counter.increment()

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(counter.get())  # 10000
```

### 5.2 资源竞争
```python
from contextlib import contextmanager
import threading

class ResourceManager:
    def __init__(self):
        self.resources = {}
        self.lock = threading.Lock()
    
    @contextmanager
    def acquire(self, resource_id):
        """获取资源."""
        while True:
            with self.lock:
                if resource_id not in self.resources:
                    self.resources[resource_id] = True
                    break
            
            # 等待资源释放
            import time
            time.sleep(0.1)
        
        try:
            yield resource_id
        finally:
            with self.lock:
                del self.resources[resource_id]
```

## 6. 性能边界

### 6.1 内存限制
```python
def process_large_file(filename, chunk_size=1024):
    """处理大文件，避免内存溢出."""
    with open(filename, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            process_chunk(chunk)

def process_large_list(items, batch_size=1000):
    """批量处理大列表."""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        process_batch(batch)
```

### 6.2 时间限制
```python
import signal
from contextlib import contextmanager

class TimeoutError(Exception):
    pass

@contextmanager
def time_limit(seconds):
    """时间限制上下文管理器."""
    def signal_handler(signum, frame):
        raise TimeoutError(f'Timeout after {seconds} seconds')
    
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    
    try:
        yield
    finally:
        signal.alarm(0)

def long_running_task():
    try:
        with time_limit(5):
            # 可能耗时很长的任务
            pass
    except TimeoutError:
        print('Task timed out')
```

## 示例

### 示例 1：用户注册
```python
from dataclasses import dataclass
from typing import Optional
import re

@dataclass
class User:
    name: str
    email: str
    age: int

class UserValidator:
    """用户验证器."""
    
    @staticmethod
    def validate_name(name: Optional[str]) -> str:
        """验证用户名."""
        if not name:
            raise ValueError('Name is required')
        
        if not isinstance(name, str):
            raise TypeError('Name must be a string')
        
        if len(name) < 2:
            raise ValueError('Name must be at least 2 characters')
        
        if len(name) > 100:
            raise ValueError('Name must be at most 100 characters')
        
        if not name.isalpha():
            raise ValueError('Name must contain only letters')
        
        return name.strip().title()
    
    @staticmethod
    def validate_email(email: Optional[str]) -> str:
        """验证邮箱."""
        if not email:
            raise ValueError('Email is required')
        
        if not isinstance(email, str):
            raise TypeError('Email must be a string')
        
        email = email.strip().lower()
        
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise ValueError(f'Invalid email format: {email}')
        
        return email
    
    @staticmethod
    def validate_age(age: Optional[int]) -> int:
        """验证年龄."""
        if age is None:
            raise ValueError('Age is required')
        
        if not isinstance(age, int):
            raise TypeError('Age must be an integer')
        
        if age < 13:
            raise ValueError(f'Age must be at least 13: {age}')
        
        if age > 150:
            raise ValueError(f'Age seems unrealistic: {age}')
        
        return age
    
    @classmethod
    def validate_user_data(cls, name, email, age) -> User:
        """验证用户数据."""
        validated_name = cls.validate_name(name)
        validated_email = cls.validate_email(email)
        validated_age = cls.validate_age(age)
        
        return User(
            name=validated_name,
            email=validated_email,
            age=validated_age
        )

# 使用
validator = UserValidator()
try:
    user = validator.validate_user_data('Alice', 'alice@example.com', 25)
    print(f'Valid user: {user}')
except (ValueError, TypeError) as e:
    print(f'Validation error: {e}')
```

### 示例 2：API 响应处理
```python
from typing import Dict, Any, Optional
import requests

class APIResponse:
    """API 响应处理器."""
    
    @staticmethod
    def validate_response(response: requests.Response) -> Dict[str, Any]:
        """验证 API 响应."""
        if response is None:
            raise ValueError('Response cannot be None')
        
        if not isinstance(response, requests.Response):
            raise TypeError('Invalid response type')
        
        if response.status_code >= 400:
            raise RuntimeError(
                f'API error: {response.status_code} - {response.text}'
            )
        
        try:
            return response.json()
        except ValueError as e:
            raise ValueError(f'Invalid JSON response: {e}')
    
    @staticmethod
    def get_field(data: Dict[str, Any], field: str, 
                  required: bool = True, 
                  default: Any = None) -> Any:
        """安全获取字段."""
        if not isinstance(data, dict):
            raise TypeError('Data must be a dictionary')
        
        if field not in data:
            if required:
                raise ValueError(f'Required field missing: {field}')
            return default
        
        return data[field]
    
    @classmethod
    def process_user_response(cls, response: requests.Response) -> Dict[str, Any]:
        """处理用户响应."""
        data = cls.validate_response(response)
        
        return {
            'id': cls.get_field(data, 'id', required=True),
            'name': cls.get_field(data, 'name', required=True),
            'email': cls.get_field(data, 'email', required=True),
            'age': cls.get_field(data, 'age', required=False),
        }

# 使用
try:
    response = requests.get('https://api.example.com/users/1')
    user_data = APIResponse.process_user_response(response)
    print(f'User: {user_data}')
except (ValueError, TypeError, RuntimeError) as e:
    print(f'Error: {e}')
```

### 示例 3：配置加载
```python
from pathlib import Path
from typing import Dict, Any
import json

class ConfigLoader:
    """配置加载器."""
    
    REQUIRED_FIELDS = ['database', 'api']
    
    @classmethod
    def load_config(cls, filename: str) -> Dict[str, Any]:
        """加载配置文件."""
        config_path = Path(filename)
        
        if not config_path.exists():
            raise FileNotFoundError(f'Config file not found: {filename}')
        
        if not config_path.is_file():
            raise ValueError(f'Not a file: {filename}')
        
        try:
            config = json.loads(config_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            raise ValueError(f'Invalid JSON: {e}')
        except UnicodeDecodeError as e:
            raise ValueError(f'Encoding error: {e}')
        
        cls.validate_config(config)
        
        return config
    
    @classmethod
    def validate_config(cls, config: Dict[str, Any]) -> None:
        """验证配置."""
        if not isinstance(config, dict):
            raise TypeError('Config must be a dictionary')
        
        for field in cls.REQUIRED_FIELDS:
            if field not in config:
                raise ValueError(f'Required field missing: {field}')
        
        # 验证数据库配置
        db_config = config['database']
        if not isinstance(db_config, dict):
            raise TypeError('Database config must be a dictionary')
        
        for field in ['host', 'port', 'name', 'user', 'password']:
            if field not in db_config:
                raise ValueError(f'Missing database field: {field}')
        
        # 验证 API 配置
        api_config = config['api']
        if not isinstance(api_config, dict):
            raise TypeError('API config must be a dictionary')
        
        if 'base_url' not in api_config:
            raise ValueError('Missing API base_url')

# 使用
try:
    config = ConfigLoader.load_config('config.json')
    print('Config loaded successfully')
except (FileNotFoundError, ValueError, TypeError) as e:
    print(f'Config error: {e}')
```
