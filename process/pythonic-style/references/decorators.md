# Tips on Decorators

## 目录
1. 装饰器基础
2. 函数装饰器
3. 类装饰器
4. 带参数的装饰器
5. 装饰器链
6. 装饰器最佳实践
7. 常用装饰器模式

## 概览
装饰器是 Python 的强大特性，可以在不修改函数代码的情况下添加功能。理解装饰器的工作原理和最佳实践很重要。本章基于《One Python Craftsman》第8章内容。

## 1. 装饰器基础

### 1.1 理解装饰器
装饰器是一个函数，它接受一个函数作为参数，返回一个新的函数。

```python
def my_decorator(func):
    """简单装饰器."""
    def wrapper():
        print('Before function call')
        func()
        print('After function call')
    return wrapper

@my_decorator
def say_hello():
    print('Hello!')

# 等价于
# say_hello = my_decorator(say_hello)

say_hello()
# 输出:
# Before function call
# Hello!
# After function call
```

### 1.2 装饰器的本质
```python
def decorator(func):
    print(f'Decorating {func.__name__}')
    return func

@decorator
def my_function():
    pass

# 输出: Decorating my_function
```

### 1.3 使用 functools.wraps
```python
import functools

def my_decorator(func):
    @functools.wraps(func)  # 保留原函数的元数据
    def wrapper(*args, **kwargs):
        """Wrapper 函数."""
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def add(a, b):
    """添加两个数字."""
    return a + b

print(add.__name__)  # 'add' (而不是 'wrapper')
print(add.__doc__)   # '添加两个数字。'
```

## 2. 函数装饰器

### 2.1 基本函数装饰器
```python
import time
import functools

def timer(func):
    """计时装饰器."""
    @functools.wraps(func)
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
    time.sleep(1)

slow_function()
```

### 2.2 带返回值的装饰器
```python
def uppercase(func):
    """返回值转大写的装饰器."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, str):
            return result.upper()
        return result
    return wrapper

@uppercase
def greet(name):
    """问候."""
    return f'Hello, {name}'

print(greet('Alice'))  # 'HELLO, ALICE'
```

### 2.3 带参数的装饰器
```python
def repeat(times):
    """重复执行装饰器工厂."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def say_hello():
    """打招呼."""
    print('Hello!')

say_hello()
# 输出:
# Hello!
# Hello!
# Hello!
```

### 2.4 可选参数的装饰器
```python
import functools

def smart_decorator(arg=None):
    """智能装饰器，支持带参数和不带参数."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f'Decorating {func.__name__} with arg={arg}')
            return func(*args, **kwargs)
        return wrapper
    
    # 如果 arg 是可调用的，说明是直接装饰函数
    if callable(arg):
        func = arg
        arg = None
        return decorator(func)
    
    return decorator

@smart_decorator
def func1():
    pass

@smart_decorator(arg='custom')
def func2():
    pass

func1()  # Decorating func1 with arg=None
func2()  # Decorating func2 with arg=custom
```

## 3. 类装饰器

### 3.1 基本类装饰器
```python
class CountCalls:
    """计数装饰器类."""
    
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f'Call #{self.count}')
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    """打招呼."""
    print('Hello!')

say_hello()  # Call #1
say_hello()  # Call #2
say_hello()  # Call #3
```

### 3.2 带参数的类装饰器
```python
class Repeat:
    """重复执行装饰器类."""
    
    def __init__(self, times):
        self.times = times
    
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(self.times):
                result = func(*args, **kwargs)
            return result
        return wrapper

@Repeat(times=3)
def say_hello():
    """打招呼."""
    print('Hello!')

say_hello()
```

## 4. 带参数的装饰器

### 4.1 装饰器工厂
```python
def logged(level='INFO', name=None, message=None):
    """日志装饰器工厂."""
    def decorate(func):
        logname = name if name else func.__module__
        logmsg = message if message else func.__name__
        
        import logging
        logger = logging.getLogger(logname)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.log(level, logmsg)
            return func(*args, **kwargs)
        
        return wrapper
    return decorate

@logged(level='DEBUG')
def add(x, y):
    """添加两个数字."""
    return x + y
```

### 4.2 带状态的装饰器
```python
def cache(func):
    """缓存装饰器."""
    cache_dict = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache_dict:
            cache_dict[args] = func(*args)
        return cache_dict[args]
    
    return wrapper

@cache
def fibonacci(n):
    """斐波那契数列."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

## 5. 装饰器链

### 5.1 多个装饰器
```python
def make_bold(func):
    """加粗装饰器."""
    @functools.wraps(func)
    def wrapper():
        return f'<b>{func()}</b>'
    return wrapper

def make_italic(func):
    """斜体装饰器."""
    @functools.wraps(func)
    def wrapper():
        return f'<i>{func()}</i>'
    return wrapper

@make_bold
@make_italic
def say_hello():
    """打招呼."""
    return 'Hello'

print(say_hello())  # <b><i>Hello</i></b>

# 等价于
# say_hello = make_bold(make_italic(say_hello))
```

### 5.2 装饰器执行顺序
```python
def decorator1(func):
    print('Decorator 1')
    def wrapper(*args, **kwargs):
        print('Wrapper 1 start')
        result = func(*args, **kwargs)
        print('Wrapper 1 end')
        return result
    return wrapper

def decorator2(func):
    print('Decorator 2')
    def wrapper(*args, **kwargs):
        print('Wrapper 2 start')
        result = func(*args, **kwargs)
        print('Wrapper 2 end')
        return result
    return wrapper

@decorator1
@decorator2
def my_function():
    print('Function')

# 输出:
# Decorator 2
# Decorator 1

my_function()
# 输出:
# Wrapper 1 start
# Wrapper 2 start
# Function
# Wrapper 2 end
# Wrapper 1 end
```

## 6. 装饰器最佳实践

### 6.1 使用 functools.wraps
```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 6.2 处理异常
```python
import functools
import logging

logger = logging.getLogger(__name__)

def handle_errors(func):
    """错误处理装饰器."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f'Error in {func.__name__}')
            raise
    return wrapper
```

### 6.3 验证参数
```python
import functools

def validate_positive(*param_names):
    """验证参数为正数."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 验证位置参数
            for i, param_name in enumerate(param_names):
                if i < len(args) and args[i] <= 0:
                    raise ValueError(f'{param_name} must be positive')
            
            # 验证关键字参数
            for param_name in param_names:
                if param_name in kwargs and kwargs[param_name] <= 0:
                    raise ValueError(f'{param_name} must be positive')
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_positive('a', 'b')
def add_positive(a, b):
    """添加两个正数."""
    return a + b
```

### 6.4 性能监控
```python
import functools
import time

def profile(func):
    """性能分析装饰器."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} executed in {end - start:.4f}s')
        return result
    return wrapper
```

### 6.5 访问和修改参数
```python
import functools

def convert_args_to_int(func):
    """转换参数为整数."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        new_args = [int(arg) for arg in args]
        new_kwargs = {k: int(v) for k, v in kwargs.items()}
        return func(*new_args, **new_kwargs)
    return wrapper

@convert_args_to_int
def add(a, b):
    """添加两个数字."""
    return a + b

print(add('3', '5'))  # 8
```

## 7. 常用装饰器模式

### 7.1 单例模式
```python
def singleton(cls):
    """单例装饰器."""
    instances = {}
    
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Database:
    """数据库连接."""
    pass

db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

### 7.2 权限检查
```python
import functools

def require_permission(permission):
    """权限检查装饰器."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not has_permission(permission):
                raise PermissionError(f'Missing permission: {permission}')
            return func(*args, **kwargs)
        return wrapper
    return decorator

def has_permission(permission):
    """检查权限."""
    return permission in ['read', 'write']

@require_permission('write')
def update_data():
    """更新数据."""
    print('Data updated')
```

### 7.3 缓存
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(x):
    """昂贵计算."""
    print(f'Computing {x}...')
    return x * x

print(expensive_computation(5))  # Computing 5...
print(expensive_computation(5))  # 使用缓存
```

### 7.4 重试机制
```python
import functools
import time

def retry(max_attempts=3, delay=1):
    """重试装饰器."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def unreliable_function():
    """不可靠的函数."""
    import random
    if random.random() < 0.7:
        raise ValueError('Random error')
    return 'Success'
```

### 7.5 超时控制
```python
import functools
import signal
from contextlib import contextmanager

@contextmanager
def timeout(seconds):
    """超时上下文."""
    def timeout_handler(signum, frame):
        raise TimeoutError(f'Timeout after {seconds} seconds')
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def timed_out(seconds):
    """超时装饰器."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with timeout(seconds):
                return func(*args, **kwargs)
        return wrapper
    return decorator

@tim_out(seconds=2)
def long_running_function():
    """长时间运行的函数."""
    time.sleep(5)
```

## 8. 装饰器高级用法

### 8.1 装饰类方法
```python
def class_method_decorator(func):
    """类方法装饰器."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f'Calling {func.__name__} on {self.__class__.__name__}')
        return func(self, *args, **kwargs)
    return wrapper

class MyClass:
    @class_method_decorator
    def method(self):
        """方法."""
        pass
```

### 8.2 装饰器访问类
```python
def add_method(cls):
    """添加方法的装饰器."""
    def new_method(self):
        return 'New method'
    
    cls.new_method = new_method
    return cls

@add_method
class MyClass:
    pass

obj = MyClass()
print(obj.new_method())  # 'New method'
```

### 8.3 装饰器属性
```python
def property_decorator(func):
    """属性装饰器."""
    @property
    @functools.wraps(func)
    def wrapper(self):
        return func(self)
    return wrapper

class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property_decorator
    def area(self):
        """面积."""
        return 3.14 * self._radius ** 2
```

## 示例

### 示例 1：日志装饰器
```python
import functools
import logging

logger = logging.getLogger(__name__)

def log(level=logging.INFO):
    """日志装饰器."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.log(level, f'Calling {func.__name__} with args={args}, kwargs={kwargs}')
            try:
                result = func(*args, **kwargs)
                logger.log(level, f'{func.__name__} returned {result}')
                return result
            except Exception as e:
                logger.log(level, f'{func.__name__} raised {e}')
                raise
        return wrapper
    return decorator

@log(level=logging.DEBUG)
def calculate(x, y):
    """计算."""
    return x + y
```

### 示例 2：验证装饰器
```python
import functools
from typing import get_type_hints

def validate_types(func):
    """类型验证装饰器."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        hints = get_type_hints(func)
        
        # 验证参数
        for param_name, param_type in hints.items():
            if param_name in kwargs:
                if not isinstance(kwargs[param_name], param_type):
                    raise TypeError(f'Parameter {param_name} must be {param_type}')
        
        return func(*args, **kwargs)
    return wrapper

@validate_types
def process_data(data: list, count: int):
    """处理数据."""
    return len(data) * count
```

### 示例 3：性能监控装饰器
```python
import functools
import time
import statistics

class PerformanceMonitor:
    """性能监控."""
    
    def __init__(self):
        self.timings = {}
    
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            elapsed = end - start
            
            if func.__name__ not in self.timings:
                self.timings[func.__name__] = []
            self.timings[func.__name__].append(elapsed)
            
            return result
        return wrapper
    
    def get_stats(self, func_name):
        """获取统计信息."""
        timings = self.timings.get(func_name, [])
        if not timings:
            return None
        
        return {
            'count': len(timings),
            'min': min(timings),
            'max': max(timings),
            'avg': statistics.mean(timings),
            'stdev': statistics.stdev(timings) if len(timings) > 1 else 0
        }

monitor = PerformanceMonitor()

@monitor
def slow_function():
    """慢函数."""
    time.sleep(0.1)

for _ in range(10):
    slow_function()

print(monitor.get_stats('slow_function'))
```

### 示例 4：缓存装饰器
```python
import functools
import hashlib
import pickle

def disk_cache(maxsize=128, cache_dir='.cache'):
    """磁盘缓存装饰器."""
    import os
    os.makedirs(cache_dir, exist_ok=True)
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            key = hashlib.md5(pickle.dumps((args, kwargs))).hexdigest()
            cache_file = os.path.join(cache_dir, f'{func.__name__}_{key}')
            
            # 检查缓存
            if os.path.exists(cache_file):
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            
            # 计算结果
            result = func(*args, **kwargs)
            
            # 保存到缓存
            with open(cache_file, 'wb') as f:
                pickle.dump(result, f)
            
            return result
        return wrapper
    return decorator

@disk_cache()
def expensive_computation(x):
    """昂贵计算."""
    print(f'Computing {x}...')
    return x ** 2
```

### 示例 5：装饰器链示例
```python
import functools
import time
import logging

logger = logging.getLogger(__name__)

def logged(func):
    """日志装饰器."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f'Calling {func.__name__}')
        return func(*args, **kwargs)
    return wrapper

def timed(func):
    """计时装饰器."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f'{func.__name__} took {elapsed:.4f}s')
        return result
    return wrapper

def cached(func):
    """缓存装饰器."""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

@logged
@timed
@cached
def fibonacci(n):
    """斐波那契数列."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 使用
print(fibonacci(10))
```
