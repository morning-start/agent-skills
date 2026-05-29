# Performance Tips

## 目录
1. 性能分析工具
2. 内存优化
3. 计算优化
4. I/O 优化
5. 并发和并行
6. 缓存策略
7. 算法优化
8. 数据结构选择

## 概览
本章介绍 Python 性能优化的技巧和最佳实践，帮助开发者编写高效的 Python 代码。

## 1. 性能分析工具

### 1.1 使用 timeit 测量性能
```python
import timeit

# 测量函数执行时间
def test_function():
    return sum(range(1000))

# 基本用法
time_taken = timeit.timeit(test_function, number=1000)
print(f'Average time: {time_taken / 1000:.6f} seconds')

# 使用字符串
time_taken = timeit.timeit('sum(range(1000))', number=1000)
print(f'Average time: {time_taken / 1000:.6f} seconds')
```

### 1.2 使用 cProfile 分析性能
```python
import cProfile

def slow_function():
    total = 0
    for i in range(100000):
        total += i ** 2
    return total

# 分析函数
cProfile.run('slow_function()')

# 保存到文件
cProfile.run('slow_function()', filename='profile.stats')
```

### 1.3 使用 memory_profiler 分析内存
```python
# 需要安装: pip install memory_profiler

@profile
def memory_intensive_function():
    large_list = [i for i in range(1000000)]
    return sum(large_list)

# 运行: python -m memory_profiler script.py
```

### 1.4 使用 line_profiler 分析行级性能
```python
# 需要安装: pip install line_profiler

@profile
def line_by_line_profile():
    total = 0
    for i in range(100000):
        total += i
    return total

# 运行: kernprof -l -v script.py
```

## 2. 内存优化

### 2.1 使用生成器替代列表
```python
# 低内存使用
def generate_numbers(n):
    """生成数字."""
    for i in range(n):
        yield i

# 高内存使用
def list_numbers(n):
    """列表数字."""
    return [i for i in range(n)]

# 使用生成器
total = sum(generate_numbers(1000000))  # 节省内存
```

### 2.2 使用 __slots__ 减少内存
```python
# 不使用 __slots__
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 使用 __slots__
class UserOptimized:
    __slots__ = ['name', 'age']
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

import sys
user1 = User('Alice', 25)
user2 = UserOptimized('Alice', 25)
print(sys.getsizeof(user1.__dict__))  # 较大
print(sys.getsizeof(user2))  # 较小
```

### 2.3 使用更小的数据类型
```python
import array
import numpy as np

# Python 列表（高内存）
list_data = [1, 2, 3, 4, 5]

# Array（低内存）
array_data = array.array('i', [1, 2, 3, 4, 5])

# NumPy 数组（最低内存）
numpy_data = np.array([1, 2, 3, 4, 5], dtype=np.int8)
```

### 2.4 及时释放内存
```python
def process_large_data():
    large_data = create_large_dataset()
    result = process(large_data)
    # 显式删除大对象
    del large_data
    # 手动触发垃圾回收
    import gc
    gc.collect()
    return result
```

## 3. 计算优化

### 3.1 使用内置函数
```python
# 慢
def sum_slow(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

# 快
def sum_fast(numbers):
    return sum(numbers)
```

### 3.2 使用列表推导
```python
# 慢
def squares_slow(numbers):
    squares = []
    for num in numbers:
        squares.append(num ** 2)
    return squares

# 快
def squares_fast(numbers):
    return [num ** 2 for num in numbers]
```

### 3.3 使用 map 和 filter
```python
# 慢
def transform_slow(numbers):
    result = []
    for num in numbers:
        result.append(num * 2)
    return result

# 快
def transform_fast(numbers):
    return list(map(lambda x: x * 2, numbers))
```

### 3.4 使用集合进行快速查找
```python
# 慢
def check_in_list(items, target):
    return target in items

# 快
def check_in_set(items, target):
    return target in set(items)
```

## 4. I/O 优化

### 4.1 批量写入
```python
# 慢
def write_slow(lines):
    with open('output.txt', 'w') as f:
        for line in lines:
            f.write(line)

# 快
def write_fast(lines):
    with open('output.txt', 'w') as f:
        f.writelines(lines)
```

### 4.2 使用缓冲
```python
# 小缓冲区
def read_small_buffer(filename):
    with open(filename, 'r', buffering=1024) as f:
        return f.read()

# 大缓冲区
def read_large_buffer(filename):
    with open(filename, 'r', buffering=8192) as f:
        return f.read()
```

### 4.3 使用 mmap 处理大文件
```python
import mmap

def read_large_file(filename):
    """使用 mmap 读取大文件."""
    with open(filename, 'r+b') as f:
        mm = mmap.mmap(f.fileno(), 0)
        content = mm.read()
        mm.close()
        return content
```

### 4.4 异步 I/O
```python
import aiofiles
import asyncio

async def read_file_async(filename):
    """异步读取文件."""
    async with aiofiles.open(filename, 'r') as f:
        return await f.read()

async def main():
    content = await read_file_async('large_file.txt')
    process(content)

asyncio.run(main())
```

## 5. 并发和并行

### 5.1 使用多线程处理 I/O 密集型任务
```python
from concurrent.futures import ThreadPoolExecutor
import time

def io_task(url):
    """I/O 密集型任务."""
    time.sleep(1)  # 模拟 I/O
    return f'Data from {url}'

urls = ['url1', 'url2', 'url3']

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(io_task, urls))

print(results)
```

### 5.2 使用多进程处理 CPU 密集型任务
```python
from multiprocessing import Pool

def cpu_task(n):
    """CPU 密集型任务."""
    return sum(i ** 2 for i in range(n))

numbers = [100000, 200000, 300000]

with Pool(3) as p:
    results = p.map(cpu_task, numbers)

print(results)
```

### 5.3 使用 asyncio 处理并发任务
```python
import asyncio

async def task(name, delay):
    """异步任务."""
    await asyncio.sleep(delay)
    return f'Task {name} completed'

async def main():
    tasks = [
        asyncio.create_task(task('A', 1)),
        asyncio.create_task(task('B', 2)),
        asyncio.create_task(task('C', 3)),
    ]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

## 6. 缓存策略

### 6.1 使用 functools.lru_cache
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    """带缓存的斐波那契."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))  # 快速计算
```

### 6.2 手动实现缓存
```python
class LRUCache:
    """LRU 缓存."""
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = []
    
    def get(self, key):
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)
```

### 6.3 使用装饰器缓存
```python
def cache_decorator(func):
    """缓存装饰器."""
    cache = {}
    
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    return wrapper

@cache_decorator
def expensive_computation(x):
    """昂贵计算."""
    return x ** 2
```

## 7. 算法优化

### 7.1 选择合适的算法
```python
# 慢：O(n)
def search_slow(items, target):
    for item in items:
        if item == target:
            return True
    return False

# 快：O(1) (如果使用集合)
def search_fast(items, target):
    return target in set(items)
```

### 7.2 避免重复计算
```python
# 慢：重复计算
def compute_slow(n):
    result = 0
    for i in range(n):
        for j in range(n):
            result += i * j
    return result

# 快：一次计算
def compute_fast(n):
    total_i = sum(i for i in range(n))
    total_j = sum(j for j in range(n))
    return total_i * total_j
```

### 7.3 使用更高效的数据结构
```python
# 慢：列表查找
def find_in_list(items, target):
    return target in items

# 快：字典查找
def find_in_dict(mapping, target):
    return target in mapping
```

## 8. 数据结构选择

### 8.1 列表 vs 元组
```python
# 列表：可变，用于需要修改的数据
mutable_data = [1, 2, 3]
mutable_data.append(4)

# 元组：不可变，用于固定数据，更快
immutable_data = (1, 2, 3)
```

### 8.2 集合 vs 列表
```python
# 列表：有序，可重复
list_data = [1, 2, 3, 2, 1]

# 集合：无序，唯一，快速查找
set_data = {1, 2, 3}
```

### 8.3 字典 vs 自定义类
```python
# 字典：快速，灵活
user_dict = {'name': 'Alice', 'age': 25}

# 命名元组：更快，类型安全
from collections import namedtuple
User = namedtuple('User', ['name', 'age'])
user_tuple = User('Alice', 25)

# 数据类：最灵活，带方法
from dataclasses import dataclass

@dataclass
class UserClass:
    name: str
    age: int

user_class = UserClass('Alice', 25)
```

## 示例

### 示例 1：优化循环
```python
# 慢
def process_slow(items):
    results = []
    for i in range(len(items)):
        item = items[i]
        if item % 2 == 0:
            results.append(item ** 2)
    return results

# 快
def process_fast(items):
    return [item ** 2 for item in items if item % 2 == 0]
```

### 示例 2：优化字符串操作
```python
# 慢
def concat_slow(strings):
    result = ''
    for s in strings:
        result += s
    return result

# 快
def concat_fast(strings):
    return ''.join(strings)
```

### 示例 3：优化数据库查询
```python
# 慢：N+1 查询
def get_users_slow(user_ids):
    users = []
    for user_id in user_ids:
        user = db.query('SELECT * FROM users WHERE id = ?', (user_id,))
        users.append(user)
    return users

# 快：批量查询
def get_users_fast(user_ids):
    placeholders = ','.join('?' * len(user_ids))
    query = f'SELECT * FROM users WHERE id IN ({placeholders})'
    return db.query(query, user_ids)
```

### 示例 4：使用 Cython 加速
```python
# mymodule.pyx
def cython_sum(n):
    cdef int i
    cdef int total = 0
    for i in range(n):
        total += i
    return total

# 编译：python setup.py build_ext --inplace
```

### 示例 5：使用 NumPy 加速数值计算
```python
import numpy as np

# 慢：纯 Python
def python_sum(n):
    return sum(i ** 2 for i in range(n))

# 快：NumPy
def numpy_sum(n):
    return np.sum(np.arange(n) ** 2)
```
