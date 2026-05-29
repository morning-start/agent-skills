"""
Advanced Pythonic Patterns Templates
基于《One Python Craftsman》高级概念的代码模板
"""

# ============================================================================
# 元类编程
# ============================================================================

class SingletonMeta(type):
    """单例元类模板."""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """单例类模板."""
    pass


# ============================================================================
# 描述符协议
# ============================================================================

class ValidatedAttribute:
    """验证属性描述符模板."""
    
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


class LazyProperty:
    """延迟加载属性模板."""
    
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    
    def __get__(self, obj, owner):
        if obj is None:
            return self
        value = self.func(obj)
        setattr(obj, self.name, value)
        return value


# ============================================================================
# 迭代器协议
# ============================================================================

class SequenceIterator:
    """序列迭代器模板."""
    
    def __init__(self, sequence):
        self.sequence = sequence
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.sequence):
            raise StopIteration
        result = self.sequence[self.index]
        self.index += 1
        return result


# ============================================================================
# 上下文管理器
# ============================================================================

from contextlib import contextmanager


@contextmanager
def resource_manager(resource):
    """资源管理器模板."""
    try:
        yield resource
    finally:
        resource.cleanup()


@contextmanager
def timer(name):
    """计时器模板."""
    import time
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f'{name} took {elapsed:.4f}s')


# ============================================================================
# 属性访问控制
# ============================================================================

class DynamicObject:
    """动态对象模板."""
    
    def __init__(self, **kwargs):
        self._data = kwargs
    
    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value


# ============================================================================
# 函数式编程
# ============================================================================

from functools import partial, reduce


def compose(*functions):
    """函数组合模板."""
    def composed(data):
        for func in reversed(functions):
            data = func(data)
        return data
    return composed


def pipe(data, *functions):
    """管道函数模板."""
    for func in functions:
        data = func(data)
    return data


# ============================================================================
# 装饰器高级模式
# ============================================================================

def count_calls(func):
    """计数装饰器模板."""
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


def memoize(func):
    """记忆化装饰器模板."""
    cache = {}
    
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


def singleton(cls):
    """单例装饰器模板."""
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


def retry(max_attempts=3, delay=1):
    """重试装饰器模板."""
    import time
    
    def decorator(func):
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


# ============================================================================
# 魔术方法
# ============================================================================

class Comparable:
    """可比较对象模板."""
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __lt__(self, other):
        return self.__dict__ < other.__dict__
    
    def __le__(self, other):
        return self < other or self == other
    
    def __gt__(self, other):
        return not self <= other
    
    def __ge__(self, other):
        return not self < other


class Container:
    """容器对象模板."""
    
    def __init__(self, items):
        self._items = list(items)
    
    def __len__(self):
        return len(self._items)
    
    def __getitem__(self, index):
        return self._items[index]
    
    def __setitem__(self, index, value):
        self._items[index] = value
    
    def __delitem__(self, index):
        del self._items[index]
    
    def __contains__(self, item):
        return item in self._items
    
    def __iter__(self):
        return iter(self._items)
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self._items})'


class Callable:
    """可调用对象模板."""
    
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


# ============================================================================
# 并发模式
# ============================================================================

import threading
import queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


class ThreadPool:
    """线程池模板."""
    
    def __init__(self, max_workers=None):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def submit(self, func, *args, **kwargs):
        return self.executor.submit(func, *args, **kwargs)
    
    def map(self, func, iterable):
        return list(self.executor.map(func, iterable))
    
    def shutdown(self):
        self.executor.shutdown(wait=True)


class ProducerConsumer:
    """生产者-消费者模板."""
    
    def __init__(self, queue_size=10):
        self.queue = queue.Queue(maxsize=queue_size)
    
    def produce(self, item):
        self.queue.put(item)
    
    def consume(self):
        return self.queue.get()
    
    def task_done(self):
        self.queue.task_done()
    
    def join(self):
        self.queue.join()


# ============================================================================
# 异步模式
# ============================================================================

import asyncio


class AsyncTask:
    """异步任务模板."""
    
    @staticmethod
    async def run(tasks):
        """运行多个异步任务."""
        return await asyncio.gather(*tasks)
    
    @staticmethod
    async def run_with_timeout(task, timeout):
        """带超时的异步任务."""
        return await asyncio.wait_for(task, timeout)
    
    @staticmethod
    async def batch_execute(tasks, batch_size=10):
        """批量执行任务."""
        results = []
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            batch_results = await asyncio.gather(*batch)
            results.extend(batch_results)
        return results


# ============================================================================
# 缓存模式
# ============================================================================

from functools import lru_cache


class LRUCache:
    """LRU 缓存模板."""
    
    def __init__(self, capacity=128):
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
    
    def clear(self):
        self.cache.clear()
        self.order.clear()


# ============================================================================
# 验证模式
# ============================================================================

class Validator:
    """验证器模板."""
    
    @staticmethod
    def validate_email(email):
        """验证邮箱."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_url(url):
        """验证 URL."""
        import re
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return re.match(pattern, url) is not None
    
    @staticmethod
    def validate_positive_number(value):
        """验证正数."""
        return isinstance(value, (int, float)) and value > 0
    
    @staticmethod
    def validate_required(value):
        """验证必填."""
        return value is not None and value != ''


# ============================================================================
# 建造者模式
# ============================================================================

class Builder:
    """建造者模板."""
    
    def __init__(self):
        self._data = {}
    
    def add(self, key, value):
        self._data[key] = value
        return self
    
    def remove(self, key):
        if key in self._data:
            del self._data[key]
        return self
    
    def update(self, data):
        self._data.update(data)
        return self
    
    def build(self):
        return self._data.copy()


# ============================================================================
# 查询构建器
# ============================================================================

class QueryBuilder:
    """查询构建器模板."""
    
    def __init__(self):
        self._query = []
        self._where = []
        self._order_by = []
        self._limit = None
    
    def select(self, *columns):
        self._query.append(f"SELECT {', '.join(columns)}")
        return self
    
    def from_table(self, table):
        self._query.append(f"FROM {table}")
        return self
    
    def where(self, condition):
        self._where.append(condition)
        return self
    
    def order_by(self, *columns):
        self._order_by.extend(columns)
        return self
    
    def limit(self, n):
        self._limit = n
        return self
    
    def build(self):
        query = ' '.join(self._query)
        
        if self._where:
            query += ' WHERE ' + ' AND '.join(self._where)
        
        if self._order_by:
            query += ' ORDER BY ' + ', '.join(self._order_by)
        
        if self._limit:
            query += f' LIMIT {self._limit}'
        
        return query


# ============================================================================
# 示例用法
# ============================================================================

if __name__ == '__main__':
    # 单例示例
    s1 = Singleton()
    s2 = Singleton()
    assert s1 is s2
    
    # 验证属性示例
    class Product:
        price = ValidatedAttribute(validator=Validator.validate_positive_number)
    
    p = Product()
    p.price = 10  # OK
    # p.price = -5  # ValueError
    
    # 迭代器示例
    seq = [1, 2, 3]
    it = SequenceIterator(seq)
    assert list(it) == [1, 2, 3]
    
    # 装饰器示例
    @count_calls
    def test_func():
        return 'test'
    
    test_func()
    test_func()
    assert test_func.calls == 2
    
    # 查询构建器示例
    query = (QueryBuilder()
             .select('*')
             .from_table('users')
             .where('age > 18')
             .order_by('name')
             .limit(10)
             .build())
    
    assert query == "SELECT * FROM users WHERE age > 18 ORDER BY name LIMIT 10"
