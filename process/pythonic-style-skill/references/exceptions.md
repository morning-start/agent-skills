# Three Rituals of Exceptions Handling

## 目录
1. 异常处理三大仪式
2. 捕获特定异常
3. 异常处理原则
4. 异常链
5. 自定义异常
6. 上下文管理器
7. 最佳实践

## 概览
异常处理是 Python 编程中的重要组成部分。遵循"三大仪式"可以让代码更健壮、更易维护。本章基于《One Python Craftsman》第6章内容。

## 1. 异常处理三大仪式

### 1.1 仪式一：不要吞掉异常
**反模式**：
```python
def process_data(data):
    try:
        result = perform_calculation(data)
    except:
        pass  # 吞掉所有异常
    return result
```

**Pythonic**：
```python
def process_data(data):
    try:
        result = perform_calculation(data)
    except ValueError as e:
        logger.error(f'Invalid data: {e}')
        raise  # 重新抛出或处理
    return result
```

### 1.2 仪式二：捕获特定异常
**反模式**：
```python
def read_config(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except Exception as e:  # 太宽泛
        print(f'Error: {e}')
        return None
```

**Pythonic**：
```python
def read_config(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f'Config file not found: {filename}')
        return None
    except json.JSONDecodeError as e:
        logger.error(f'Invalid JSON in config file: {e}')
        return None
```

### 1.3 仪式三：提供有用的错误信息
**反模式**：
```python
def divide(a, b):
    try:
        return a / b
    except Exception:
        raise Exception('Error')  # 无用的错误信息
```

**Pythonic**：
```python
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError(f'Cannot divide {a} by zero')
```

## 2. 捕获特定异常

### 2.1 基本捕获
```python
try:
    result = risky_operation()
except ValueError:
    logger.error('Invalid value')
except KeyError:
    logger.error('Key not found')
except Exception as e:
    logger.error(f'Unexpected error: {e}')
```

### 2.2 捕获多个异常
```python
# 方式 1：元组
try:
    result = risky_operation()
except (ValueError, TypeError) as e:
    logger.error(f'Error: {e}')

# 方式 2：as 语法
try:
    result = risky_operation()
except (ValueError, TypeError) as e:
    logger.error(f'Error type: {type(e).__name__}')
    logger.error(f'Error message: {e}')
```

### 2.3 避免捕获所有异常
**反模式**：
```python
try:
    result = risky_operation()
except:  # 裸 except
    pass
```

**Pythonic**：
```python
try:
    result = risky_operation()
except Exception as e:  # 至少捕获 Exception
    logger.error(f'Error: {e}')
    raise  # 重新抛出
```

### 2.4 finally 子句
```python
def process_file(filename):
    f = None
    try:
        f = open(filename, 'r')
        return f.read()
    except FileNotFoundError:
        logger.error(f'File not found: {filename}')
        return None
    finally:
        if f is not None:
            f.close()  # 确保文件关闭
```

### 2.5 else 子句
```python
try:
    result = risky_operation()
except ValueError:
    logger.error('Invalid value')
    result = None
else:  # 没有异常时执行
    logger.info('Operation succeeded')
    return result
```

## 3. 异常处理原则

### 3.1 EAFP 原则（Easier to Ask for Forgiveness than Permission）
**反模式（LBYL）**：
```python
if 'key' in data:
    value = data['key']
else:
    value = None
```

**Pythonic（EAFP）**：
```python
try:
    value = data['key']
except KeyError:
    value = None
```

### 3.2 何时使用 EAFP vs LBYL

**使用 EAFP 的场景**：
- 异常是预期的、常见的
- 正常路径比异常路径更频繁
- 代码可读性更重要

**使用 LBYL 的场景**：
- 异常处理开销大
- 异常是罕见的
- 性能关键代码

### 3.3 异常处理的粒度
**反模式**：
```python
def process_data(data):
    try:
        # 100 行代码
        result1 = step1(data)
        result2 = step2(result1)
        result3 = step3(result2)
        return result3
    except Exception as e:
        logger.error(f'Error: {e}')
        return None
```

**Pythonic**：
```python
def process_data(data):
    try:
        result1 = step1(data)
    except ValueError as e:
        logger.error(f'Step 1 failed: {e}')
        return None
    
    try:
        result2 = step2(result1)
    except ValueError as e:
        logger.error(f'Step 2 failed: {e}')
        return None
    
    try:
        result3 = step3(result2)
    except ValueError as e:
        logger.error(f'Step 3 failed: {e}')
        return None
    
    return result3
```

## 4. 异常链

### 4.1 使用 raise from
```python
def load_config(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise ConfigError(f'Config file not found: {filename}') from e
    except json.JSONDecodeError as e:
        raise ConfigError(f'Invalid JSON in config file: {filename}') from e
```

### 4.2 抑制异常链
```python
try:
    result = risky_operation()
except ValueError:
    raise CustomError('Something went wrong') from None  # 抑制原始异常
```

### 4.3 访问原始异常
```python
try:
    result = risky_operation()
except Exception as e:
    if e.__cause__:
        logger.error(f'Original error: {e.__cause__}')
    if e.__context__:
        logger.error(f'Context: {e.__context__}')
    raise
```

## 5. 自定义异常

### 5.1 基本自定义异常
```python
class CustomError(Exception):
    """自定义异常基类."""
    pass

class ConfigError(CustomError):
    """配置错误."""
    pass

class DataError(CustomError):
    """数据错误."""
    pass
```

### 5.2 带参数的自定义异常
```python
class ValidationError(Exception):
    """验证错误."""
    
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f'{field}: {message}')

# 使用
raise ValidationError('email', 'Invalid email format')
```

### 5.3 异常层次结构
```python
class ApplicationError(Exception):
    """应用程序错误基类."""
    pass

class NetworkError(ApplicationError):
    """网络错误."""
    pass

class DatabaseError(ApplicationError):
    """数据库错误."""
    pass

class ConnectionError(NetworkError):
    """连接错误."""
    pass

class TimeoutError(NetworkError):
    """超时错误."""
    pass
```

## 6. 上下文管理器

### 6.1 使用 with 语句管理资源
```python
# 文件操作
with open('file.txt', 'r') as f:
    content = f.read()

# 锁操作
with lock:
    critical_section()

# 数据库连接
with connection.cursor() as cursor:
    cursor.execute('SELECT * FROM users')
    results = cursor.fetchall()
```

### 6.2 自定义上下文管理器
```python
class Timer:
    """计时器上下文管理器."""
    
    def __init__(self, name):
        self.name = name
        self.start = None
        self.elapsed = None
    
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start
        print(f'{self.name} took {self.elapsed:.4f} seconds')
        return False  # 不抑制异常

# 使用
with Timer('process_data'):
    process_data()
```

### 6.3 使用 contextmanager 装饰器
```python
from contextlib import contextmanager

@contextmanager
def database_connection():
    """数据库连接上下文管理器."""
    conn = create_connection()
    try:
        yield conn
    finally:
        conn.close()

# 使用
with database_connection() as conn:
    results = conn.query('SELECT * FROM users')
```

### 6.4 抑制异常
```python
from contextlib import suppress

with suppress(FileNotFoundError):
    # 文件不存在时不会抛出异常
    os.remove('temp_file.txt')
```

## 7. 最佳实践

### 7.1 不要在 finally 中抛出异常
**反模式**：
```python
try:
    result = risky_operation()
except Exception as e:
    logger.error(f'Error: {e}')
finally:
    if cleanup_failed:
        raise RuntimeError('Cleanup failed')  # 可能覆盖原始异常
```

**Pythonic**：
```python
try:
    result = risky_operation()
except Exception as e:
    logger.error(f'Error: {e}')
    raise
finally:
    try:
        cleanup()
    except Exception as cleanup_error:
        logger.error(f'Cleanup failed: {cleanup_error}')
```

### 7.2 使用日志记录异常
```python
import logging

logger = logging.getLogger(__name__)

def process_data(data):
    try:
        result = risky_operation(data)
    except ValueError as e:
        logger.exception('Failed to process data')  # 记录完整堆栈
        raise
    return result
```

### 7.3 在适当的层级处理异常
```反模式**：
```python
def calculate_total(items):
    try:
        total = sum(item.price for item in items)
    except AttributeError:
        return 0  # 在底层吞掉异常
    return total
```

**Pythonic**：
```python
def calculate_total(items):
    """计算总价，假设 items 已经验证."""
    return sum(item.price for item in items)

# 在调用方处理异常
def process_order(order):
    try:
        total = calculate_total(order.items)
    except AttributeError as e:
        logger.error(f'Invalid order items: {e}')
        raise ValidationError('Invalid order items')
```

### 7.4 异常处理 vs 返回错误码
**反模式**：
```python
def divide(a, b):
    if b == 0:
        return None, 'Division by zero'
    return a / b, ''

# 使用
result, error = divide(10, 0)
if error:
    print(error)
else:
    print(result)
```

**Pythonic**：
```python
def divide(a, b):
    if b == 0:
        raise ValueError('Division by zero')
    return a / b

# 使用
try:
    result = divide(10, 0)
except ValueError as e:
    print(e)
else:
    print(result)
```

### 7.5 使用断言检查不变量
```python
def process_list(items):
    """处理列表，假设输入不为空."""
    assert items, 'Items cannot be empty'  # 断言
    return [item * 2 for item in items]

# 在测试中使用
assert process_list([1, 2]) == [2, 4]
```

## 8. 常见异常类型

### 8.1 内置异常
```python
# ValueError: 值错误
int('abc')  # ValueError

# TypeError: 类型错误
1 + '2'  # TypeError

# KeyError: 键错误
data = {'a': 1}
data['b']  # KeyError

# IndexError: 索引错误
items = [1, 2, 3]
items[10]  # IndexError

# AttributeError: 属性错误
'hello'.len()  # AttributeError

# FileNotFoundError: 文件未找到
open('nonexistent.txt')  # FileNotFoundError

# PermissionError: 权限错误
open('/root/file.txt', 'w')  # PermissionError
```

### 8.2 选择合适的异常类型
```python
# 输入验证：ValueError
def set_age(age):
    if age < 0 or age > 150:
        raise ValueError('Age must be between 0 and 150')

# 类型错误：TypeError
def add(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError('Both arguments must be numbers')
    return a + b

# 状态错误：RuntimeError
def process():
    if not initialized:
        raise RuntimeError('Not initialized')
```

## 示例

### 示例 1：完整的异常处理
```python
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigError(Exception):
    """配置错误."""
    pass

def load_config(filename: str) -> dict:
    """
    加载配置文件.
    
    Args:
        filename: 配置文件路径
    
    Returns:
        配置字典
    
    Raises:
        ConfigError: 配置文件不存在或格式错误
    """
    path = Path(filename)
    
    # 检查文件是否存在
    if not path.exists():
        raise ConfigError(f'Config file not found: {filename}')
    
    # 检查文件扩展名
    if path.suffix not in ('.json', '.yaml'):
        raise ConfigError(f'Unsupported config file format: {path.suffix}')
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            if path.suffix == '.json':
                import json
                return json.load(f)
            else:
                import yaml
                return yaml.safe_load(f)
    
    except json.JSONDecodeError as e:
        raise ConfigError(f'Invalid JSON in config file: {e}') from e
    except yaml.YAMLError as e:
        raise ConfigError(f'Invalid YAML in config file: {e}') from e
    except Exception as e:
        logger.exception(f'Unexpected error loading config: {filename}')
        raise ConfigError(f'Failed to load config file: {filename}') from e

# 使用
try:
    config = load_config('config.json')
    print(f'Loaded config: {config}')
except ConfigError as e:
    logger.error(f'Configuration error: {e}')
    # 使用默认配置或退出
    config = get_default_config()
```

### 示例 2：数据库操作异常处理
```python
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """数据库错误."""
    pass

@contextmanager
def database_transaction(connection):
    """数据库事务上下文管理器."""
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception as e:
        connection.rollback()
        logger.exception('Database transaction failed')
        raise DatabaseError('Transaction failed') from e
    finally:
        cursor.close()

def update_user(user_id, data):
    """更新用户信息."""
    try:
        with database_transaction(connection) as cursor:
            cursor.execute(
                'UPDATE users SET name = ?, email = ? WHERE id = ?',
                (data['name'], data['email'], user_id)
            )
            if cursor.rowcount == 0:
                raise ValueError(f'User not found: {user_id}')
    except ValueError as e:
        logger.error(f'Validation error: {e}')
        raise
    except DatabaseError:
        raise
    except Exception as e:
        logger.exception(f'Unexpected error updating user: {user_id}')
        raise DatabaseError(f'Failed to update user: {user_id}') from e

# 使用
try:
    update_user(1, {'name': 'Alice', 'email': 'alice@example.com'})
except DatabaseError as e:
    print(f'Database error: {e}')
except ValueError as e:
    print(f'Validation error: {e}')
```

### 示例 3：API 调用异常处理
```python
import requests
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class APIError(Exception):
    """API 错误."""
    pass

class APIConnectionError(APIError):
    """API 连接错误."""
    pass

class APITimeoutError(APIConnectionError):
    """API 超时错误."""
    pass

class APIResponseError(APIError):
    """API 响应错误."""
    pass

def call_api(url: str, method: str = 'GET', **kwargs) -> Dict[str, Any]:
    """
    调用 API.
    
    Args:
        url: API URL
        method: HTTP 方法
        **kwargs: 其他请求参数
    
    Returns:
        API 响应数据
    
    Raises:
        APIConnectionError: 连接失败
        APITimeoutError: 请求超时
        APIResponseError: 响应错误
    """
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.Timeout as e:
        raise APITimeoutError(f'API request timeout: {url}') from e
    except requests.exceptions.ConnectionError as e:
        raise APIConnectionError(f'Failed to connect to API: {url}') from e
    except requests.exceptions.HTTPError as e:
        raise APIResponseError(f'API returned error: {e.response.status_code}') from e
    except requests.exceptions.RequestException as e:
        raise APIConnectionError(f'API request failed: {e}') from e
    except ValueError as e:
        raise APIResponseError(f'Invalid JSON response: {e}') from e

# 使用
try:
    result = call_api('https://api.example.com/users', params={'page': 1})
    print(f'Got {len(result)} users')
except APITimeoutError as e:
    logger.error(f'API timeout: {e}')
    # 重试或使用缓存
except APIConnectionError as e:
    logger.error(f'Connection error: {e}')
    # 使用缓存数据
except APIResponseError as e:
    logger.error(f'API response error: {e}')
    # 显示错误信息
except APIError as e:
    logger.error(f'API error: {e}')
```

### 示例 4：数据处理流水线
```python
import logging
from typing import List, Any

logger = logging.getLogger(__name__)

class ProcessingError(Exception):
    """处理错误."""
    pass

class ValidationError(ProcessingError):
    """验证错误."""
    pass

class TransformationError(ProcessingError):
    """转换错误."""
    pass

def process_data_pipeline(data: List[Any]) -> List[Any]:
    """
    数据处理流水线.
    
    步骤:
    1. 验证数据
    2. 转换数据
    3. 保存数据
    """
    # 步骤 1: 验证
    try:
        validated = validate_data(data)
    except ValidationError as e:
        logger.error(f'Validation failed: {e}')
        raise ProcessingError('Data validation failed') from e
    
    # 步骤 2: 转换
    try:
        transformed = transform_data(validated)
    except TransformationError as e:
        logger.error(f'Transformation failed: {e}')
        raise ProcessingError('Data transformation failed') from e
    
    # 步骤 3: 保存
    try:
        save_data(transformed)
    except Exception as e:
        logger.error(f'Save failed: {e}')
        raise ProcessingError('Failed to save data') from e
    
    return transformed

def validate_data(data: List[Any]) -> List[Any]:
    """验证数据."""
    if not data:
        raise ValidationError('Data cannot be empty')
    
    validated = []
    for item in data:
        if not isinstance(item, dict):
            raise ValidationError(f'Invalid item type: {type(item)}')
        
        if 'id' not in item:
            raise ValidationError('Item missing id field')
        
        validated.append(item)
    
    return validated

def transform_data(data: List[dict]) -> List[dict]:
    """转换数据."""
    transformed = []
    for item in data:
        try:
            transformed_item = {
                'id': item['id'],
                'name': item['name'].upper(),
                'value': float(item['value'])
            }
            transformed.append(transformed_item)
        except (KeyError, ValueError, TypeError) as e:
            raise TransformationError(f'Failed to transform item {item}: {e}') from e
    
    return transformed

def save_data(data: List[dict]):
    """保存数据."""
    # 实现保存逻辑
    pass

# 使用
try:
    raw_data = [{'id': 1, 'name': 'Alice', 'value': '100'}]
    processed_data = process_data_pipeline(raw_data)
    print(f'Processed {len(processed_data)} items')
except ProcessingError as e:
    logger.error(f'Processing failed: {e}')
    # 显示错误给用户
```
