# Advanced Pythonic Patterns

## 目录
1. 元类编程
2. 描述符协议
3. 迭代器协议
4. 上下文管理器高级用法
5. 属性访问控制
6. 动态编程
7. 函数式编程高级模式
8. 并发编程模式
9. 装饰器高级模式
10. 魔术方法

## 概览
本章介绍 Python 的高级 Pythonic 模式，这些模式能够充分利用 Python 的动态特性和强大的元编程能力。

## 1. 元类编程

### 1.1 元类基础
```python
class MetaClass(type):
    """自定义元类."""
    def __new__(cls, name, bases, namespace):
        # 在类创建时修改类
        if 'version' not in namespace:
            namespace['version'] = '1.0'
        
        # 自动添加类方法
        def get_version(cls):
            return cls.version
        
        namespace['get_version'] = classmethod(get_version)
        
        return super().__new__(cls, name, bases, namespace)

class MyClass(metaclass=MetaClass):
    """使用元类的类."""
    name = 'MyClass'

print(MyClass.version)  # 1.0
print(MyClass.get_version())  # 1.0
```

### 1.2 单例元类
```python
class SingletonMeta(type):
    """单例元类."""
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    """单例数据库连接."""
    def __init__(self):
        self.connection = None

db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

### 1.3 抽象基类强制实现
```python
from abc import ABC, abstractmethod

class AbstractShape(ABC):
    """抽象形状类."""
    
    @abstractmethod
    def area(self):
        """计算面积."""
        pass
    
    @abstractmethod
    def perimeter(self):
        """计算周长."""
        pass

class Rectangle(AbstractShape):
    """矩形."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
```

## 2. 描述符协议

### 2.1 描述符基础
```python
class PositiveNumber:
    """正数描述符."""
    
    def __init__(self, name=None):
        self.name = name
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, owner):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if value < 0:
            raise ValueError(f'{self.name} must be positive')
        obj.__dict__[self.name] = value

class Product:
    """产品类."""
    price = PositiveNumber()
    quantity = PositiveNumber()
    
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity

product = Product(10, 5)
product.price = 20  # OK
# product.price = -5  # ValueError
```

### 2.2 延迟加载描述符
```python
class LazyProperty:
    """延迟加载属性."""
    
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    
    def __get__(self, obj, owner):
        if obj is None:
            return self
        
        value = self.func(obj)
        setattr(obj, self.name, value)
        return value

class DatabaseConnection:
    """数据库连接."""
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
    
    @LazyProperty
    def connection(self):
        """延迟创建连接."""
        print('Creating connection...')
        return create_connection(self.connection_string)
```

## 3. 迭代器协议

### 3.1 自定义迭代器
```python
class CountDown:
    """倒计时迭代器."""
    
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start <= 0:
            raise StopIteration
        self.start -= 1
        return self.start + 1

for i in CountDown(5):
    print(i)  # 5, 4, 3, 2, 1
```

### 3.2 生成器模式
```python
def fibonacci_generator():
    """斐波那契数列生成器."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci_generator()
print(next(fib))  # 0
print(next(fib))  # 1
print(next(fib))  # 1

# 使用生成器表达式
squares = (x ** 2 for x in range(10))
total = sum(squares)
```

### 3.3 无限迭代器
```python
from itertools import count, cycle, repeat

# 无限计数
for i in count(start=10, step=2):
    if i > 20:
        break
    print(i)

# 循环迭代
colors = ['red', 'green', 'blue']
for color in cycle(colors):
    print(color)

# 重复元素
for item in repeat('hello', 3):
    print(item)
```

## 4. 上下文管理器高级用法

### 4.1 嵌套上下文管理器
```python
from contextlib import ExitStack

def process_multiple_files(*filenames):
    """处理多个文件."""
    with ExitStack() as stack:
        files = [stack.enter_context(open(fname)) for fname in filenames]
        for f in files:
            process_file(f)
```

### 4.2 上下文管理器装饰器
```python
from contextlib import contextmanager

@contextmanager
def timer(name):
    """计时器上下文管理器."""
    import time
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f'{name} took {elapsed:.4f}s')

@contextmanager
def suppressed(*exceptions):
    """抑制异常."""
    try:
        yield
    except exceptions:
        pass

with suppressed(FileNotFoundError):
    with open('nonexistent.txt') as f:
        content = f.read()
```

### 4.3 资源管理
```python
class ResourceManager:
    """资源管理器."""
    
    def __init__(self):
        self.resources = []
    
    def add_resource(self, resource):
        """添加资源."""
        self.resources.append(resource)
        return resource
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        for resource in reversed(self.resources):
            resource.cleanup()
        return False

with ResourceManager() as manager:
    db = manager.add_resource(Database())
    cache = manager.add_resource(Cache())
```

## 5. 属性访问控制

### 5.1 __getattr__ 和 __getattribute__
```python
class DynamicObject:
    """动态对象."""
    
    def __init__(self, **kwargs):
        self._data = kwargs
    
    def __getattr__(self, name):
        """访问不存在的属性."""
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        """设置属性."""
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value

obj = DynamicObject(name='Alice', age=25)
print(obj.name)  # Alice
print(obj.age)  # 25
```

### 5.2 属性代理
```python
class Proxy:
    """属性代理."""
    
    def __init__(self, obj):
        self._obj = obj
    
    def __getattr__(self, name):
        return getattr(self._obj, name)
    
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            setattr(self._obj, name, value)
```

## 6. 动态编程

### 6.1 动态创建类
```python
def create_class(class_name, base_classes, class_dict):
    """动态创建类."""
    return type(class_name, base_classes, class_dict)

# 动态创建 Person 类
Person = create_class(
    'Person',
    (object,),
    {
        '__init__': lambda self, name, age: (setattr(self, 'name', name), setattr(self, 'age', age)),
        'greet': lambda self: print(f'Hello, I am {self.name}')
    }
)

person = Person('Alice', 25)
person.greet()
```

### 6.2 动态方法添加
```python
class MyClass:
    """示例类."""
    pass

def new_method(self):
    """新方法."""
    return f'Hello from {self.__class__.__name__}'

# 动态添加方法
MyClass.new_method = new_method

obj = MyClass()
print(obj.new_method())  # Hello from MyClass
```

### 6.3 动态属性访问
```python
class DynamicDict:
    """动态字典访问."""
    
    def __init__(self, data):
        self._data = data
    
    def __getitem__(self, key):
        return self._data.get(key)
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __contains__(self, key):
        return key in self._data

dd = DynamicDict({'name': 'Alice'})
print(dd['name'])  # Alice
dd['age'] = 25
print('age' in dd)  # True
```

## 7. 函数式编程高级模式

### 7.1 高阶函数
```python
from functools import partial, reduce

# 偏函数
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))  # 125

# 组合函数
def compose(*functions):
    """函数组合."""
    def inner(data):
        for func in reversed(functions):
            data = func(data)
        return data
    return inner

def add(x):
    return x + 10

def multiply(x):
    return x * 2

combined = compose(add, multiply)
print(combined(5))  # 20
```

### 7.2 柯里化
```python
def curry(func):
    """柯里化装饰器."""
    def curried(*args):
        if len(args) >= func.__code__.co_argcount:
            return func(*args)
        return lambda *more: curried(*(args + more))
    return curried

@curry
def add(a, b, c):
    return a + b + c

add_5 = add(5)
add_5_3 = add_5(3)
print(add_5_3(2))  # 10
```

### 7.3 惰性求值
```python
def lazy_list(func, *args):
    """惰性列表."""
    return func(*args)

def generate_numbers(n):
    """生成数字."""
    return list(range(n))

# 延迟执行
numbers = lazy_list(generate_numbers, 10)
# numbers 在这里才真正创建
```

## 8. 并发编程模式

### 8.1 线程池
```python
from concurrent.futures import ThreadPoolExecutor

def process_item(item):
    """处理项目."""
    return item * 2

items = [1, 2, 3, 4, 5]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(process_item, items))

print(results)  # [2, 4, 6, 8, 10]
```

### 8.2 异步编程
```python
import asyncio

async def fetch_data(url):
    """异步获取数据."""
    await asyncio.sleep(1)
    return f'Data from {url}'

async def main():
    """主函数."""
    urls = ['url1', 'url2', 'url3']
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

### 8.3 生产者-消费者模式
```python
import queue
import threading

def producer(queue):
    """生产者."""
    for i in range(5):
        queue.put(i)
        print(f'Produced: {i}')

def consumer(queue):
    """消费者."""
    while True:
        item = queue.get()
        if item is None:
            break
        print(f'Consumed: {item}')
        queue.task_done()

q = queue.Queue()
producer_thread = threading.Thread(target=producer, args=(q,))
consumer_thread = threading.Thread(target=consumer, args=(q,))

producer_thread.start()
consumer_thread.start()

producer_thread.join()
q.put(None)
consumer_thread.join()
```

## 9. 装饰器高级模式

### 9.1 带状态的装饰器
```python
class CountCalls:
    """带状态的装饰器."""
    
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f'Call #{self.count}')
        return self.func(*args, **kwargs)

@CountCalls
def greet():
    print('Hello!')

greet()
greet()
greet()
```

### 9.2 类装饰器
```python
class Singleton:
    """单例装饰器."""
    
    _instances = {}
    
    def __call__(cls, wrapped_class):
        def wrapper(*args, **kwargs):
            if wrapped_class not in cls._instances:
                cls._instances[wrapped_class] = wrapped_class(*args, **kwargs)
            return cls._instances[wrapped_class]
        return wrapper

@Singleton()
class Database:
    pass

db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

### 9.3 参数化装饰器工厂
```python
def repeat(times):
    """重复执行装饰器."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet():
    print('Hello!')

greet()
```

## 10. 魔术方法

### 10.1 比较运算符
```python
class Vector:
    """向量类."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return self.length() < other.length()
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return f'Vector({self.x}, {self.y})'
    
    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)  # Vector(4, 6)
print(v1 < v2)  # True
```

### 10.2 容器方法
```python
class CustomList:
    """自定义列表."""
    
    def __init__(self, items):
        self._items = items
    
    def __len__(self):
        return len(self._items)
    
    def __getitem__(self, index):
        return self._items[index]
    
    def __setitem__(self, index, value):
        self._items[index] = value
    
    def __contains__(self, item):
        return item in self._items
    
    def __iter__(self):
        return iter(self._items)

lst = CustomList([1, 2, 3])
print(len(lst))  # 3
print(lst[0])  # 1
print(2 in lst)  # True
for item in lst:
    print(item)
```

### 10.3 可调用对象
```python
class Multiplier:
    """可调用对象."""
    
    def __init__(self, factor):
        self.factor = factor
    
    def __call__(self, value):
        return value * self.factor

times_three = Multiplier(3)
print(times_three(5))  # 15
```

## 示例

### 示例 1：构建领域特定语言（DSL）
```python
class QueryBuilder:
    """查询构建器."""
    
    def __init__(self):
        self._query = ''
    
    def select(self, *columns):
        self._query += f'SELECT {", ".join(columns)} '
        return self
    
    def from_table(self, table):
        self._query += f'FROM {table} '
        return self
    
    def where(self, condition):
        self._query += f'WHERE {condition} '
        return self
    
    def build(self):
        return self._query.strip()

query = QueryBuilder()
sql = query.select('*').from_table('users').where('age > 18').build()
print(sql)  # SELECT * FROM users WHERE age > 18
```

### 示例 2：属性验证系统
```python
class ValidatedProperty:
    """验证属性."""
    
    def __init__(self, validator=None, default=None):
        self.validator = validator
        self.default = default
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, owner):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, self.default)
    
    def __set__(self, obj, value):
        if self.validator and not self.validator(value):
            raise ValueError(f'Invalid value for {self.name}')
        obj.__dict__[self.name] = value

class User:
    """用户类."""
    
    @staticmethod
    def validate_email(email):
        return '@' in email and '.' in email
    
    @staticmethod
    def validate_age(age):
        return isinstance(age, int) and 0 <= age <= 150
    
    email = ValidatedProperty(validator=validate_email)
    age = ValidatedProperty(validator=validate_age)

user = User()
user.email = 'user@example.com'  # OK
# user.email = 'invalid'  # ValueError
```
