"""
Performance Patterns Templates
基于《One Python Craftsman》性能优化概念的代码模板
"""

# ============================================================================
# 缓存模式
# ============================================================================

from functools import lru_cache
import time
import hashlib


@lru_cache(maxsize=128)
def cached_function(x):
    """带缓存的函数模板."""
    time.sleep(1)  # 模拟耗时操作
    return x * 2


class Cache:
    """通用缓存模板."""
    
    def __init__(self, max_size=1000, ttl=3600):
        self.max_size = max_size
        self.ttl = ttl
        self._cache = {}
        self._timestamps = {}
    
    def get(self, key):
        """获取缓存."""
        if key in self._cache:
            # 检查是否过期
            if time.time() - self._timestamps[key] < self.ttl:
                return self._cache[key]
            else:
                del self._cache[key]
                del self._timestamps[key]
        return None
    
    def set(self, key, value):
        """设置缓存."""
        # 如果缓存已满，删除最旧的项
        if len(self._cache) >= self.max_size:
            oldest_key = min(self._timestamps, key=self._timestamps.get)
            del self._cache[oldest_key]
            del self._timestamps[oldest_key]
        
        self._cache[key] = value
        self._timestamps[key] = time.time()
    
    def clear(self):
        """清空缓存."""
        self._cache.clear()
        self._timestamps.clear()


# ============================================================================
# 批处理模式
# ============================================================================

class BatchProcessor:
    """批处理器模板."""
    
    def __init__(self, batch_size=100, process_func=None):
        self.batch_size = batch_size
        self.process_func = process_func
    
    def process(self, items):
        """批量处理."""
        results = []
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            if self.process_func:
                batch_result = self.process_func(batch)
                results.extend(batch_result)
        return results
    
    def process_in_chunks(self, items, callback):
        """分块处理并回调."""
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            callback(batch, i // self.batch_size + 1)


# ============================================================================
# 惰性求值
# ============================================================================

class LazySequence:
    """惰性序列模板."""
    
    def __init__(self, data_source, transform=None, filter_func=None):
        self.data_source = data_source
        self.transform = transform
        self.filter_func = filter_func
        self._cache = []
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        while self._index < len(self._cache) or self._has_more():
            if self._index >= len(self._cache):
                self._load_next()
            
            item = self._cache[self._index]
            self._index += 1
            return item
        
        raise StopIteration
    
    def _has_more(self):
        return self._index < len(self._cache) or hasattr(self.data_source, '__next__')
    
    def _load_next(self):
        try:
            item = next(self.data_source)
            
            if self.filter_func and not self.filter_func(item):
                return
            
            if self.transform:
                item = self.transform(item)
            
            self._cache.append(item)
        except StopIteration:
            pass


def lazy_map(sequence, func):
    """惰性映射模板."""
    for item in sequence:
        yield func(item)


def lazy_filter(sequence, predicate):
    """惰性过滤模板."""
    for item in sequence:
        if predicate(item):
            yield item


# ============================================================================
# 连接池
# ============================================================================

import queue
import threading


class ConnectionPool:
    """连接池模板."""
    
    def __init__(self, factory, pool_size=10):
        self.factory = factory
        self.pool_size = pool_size
        self._pool = queue.Queue(maxsize=pool_size)
        self._lock = threading.Lock()
        self._created = 0
    
    def get(self):
        """获取连接."""
        try:
            return self._pool.get_nowait()
        except queue.Empty:
            with self._lock:
                if self._created < self.pool_size:
                    connection = self.factory()
                    self._created += 1
                    return connection
            return self._pool.get()
    
    def put(self, connection):
        """归还连接."""
        self._pool.put(connection)
    
    def close(self):
        """关闭所有连接."""
        while not self._pool.empty():
            connection = self._pool.get()
            connection.close()


# ============================================================================
# 内存优化
# ============================================================================

import array
import sys


class MemoryEfficientList:
    """内存高效列表模板."""
    
    def __init__(self, items=None, dtype='i'):
        self.dtype = dtype
        self._array = array.array(dtype, items or [])
    
    def append(self, item):
        self._array.append(item)
    
    def extend(self, items):
        self._array.extend(items)
    
    def __getitem__(self, index):
        return self._array[index]
    
    def __setitem__(self, index, value):
        self._array[index] = value
    
    def __len__(self):
        return len(self._array)
    
    def __iter__(self):
        return iter(self._array)
    
    def memory_usage(self):
        return sys.getsizeof(self._array)


# ============================================================================
# 并行处理
# ============================================================================

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


def parallel_map(func, items, max_workers=None, use_processes=False):
    """并行映射模板."""
    executor_class = ProcessPoolExecutor if use_processes else ThreadPoolExecutor
    
    with executor_class(max_workers=max_workers) as executor:
        futures = [executor.submit(func, item) for item in items]
        results = []
        for future in as_completed(futures):
            results.append(future.result())
    
    return results


def parallel_map_ordered(func, items, max_workers=None):
    """有序并行映射模板."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(func, items))
    
    return results


class ParallelBatchProcessor:
    """并行批处理器模板."""
    
    def __init__(self, func, batch_size=100, max_workers=None):
        self.func = func
        self.batch_size = batch_size
        self.max_workers = max_workers
    
    def process(self, items):
        """并行处理."""
        batches = [items[i:i + self.batch_size] 
                   for i in range(0, len(items), self.batch_size)]
        
        return parallel_map_ordered(self.func, batches, self.max_workers)


# ============================================================================
# 异步优化
# ============================================================================

import asyncio


class AsyncBatchExecutor:
    """异步批执行器模板."""
    
    def __init__(self, batch_size=100, delay=0.1):
        self.batch_size = batch_size
        self.delay = delay
        self._queue = []
        self._task = None
    
    async def add(self, item, process_func):
        """添加项目到批处理."""
        self._queue.append((item, process_func))
        
        if len(self._queue) >= self.batch_size:
            await self._flush()
    
    async def _flush(self):
        """刷新队列."""
        if not self._queue:
            return
        
        batch = self._queue[:]
        self._queue.clear()
        
        tasks = [func(item) for item, func in batch]
        await asyncio.gather(*tasks)
        
        await asyncio.sleep(self.delay)
    
    async def finalize(self):
        """完成所有处理."""
        await self._flush()


# ============================================================================
# 字符串优化
# ============================================================================

class StringBuilder:
    """字符串构建器模板."""
    
    def __init__(self):
        self._parts = []
    
    def append(self, part):
        """添加部分."""
        self._parts.append(str(part))
        return self
    
    def append_line(self, part=''):
        """添加一行."""
        self._parts.append(str(part))
        self._parts.append('\n')
        return self
    
    def build(self):
        """构建字符串."""
        return ''.join(self._parts)
    
    def clear(self):
        """清空."""
        self._parts.clear()


# ============================================================================
# 数据库优化
# ============================================================================

class QueryOptimizer:
    """查询优化器模板."""
    
    def __init__(self):
        self._queries = {}
    
    def prepare(self, name, query):
        """准备查询."""
        self._queries[name] = query
    
    def execute(self, name, params=None, batch_params=None):
        """执行查询."""
        query = self._queries[name]
        
        if batch_params:
            return self._execute_batch(query, batch_params)
        else:
            return self._execute_single(query, params)
    
    def _execute_single(self, query, params):
        """执行单个查询."""
        # 实现单条查询逻辑
        pass
    
    def _execute_batch(self, query, params_list):
        """执行批量查询."""
        # 实现批量查询逻辑
        pass


class BulkInsert:
    """批量插入模板."""
    
    def __init__(self, table, batch_size=1000):
        self.table = table
        self.batch_size = batch_size
        self._buffer = []
    
    def add(self, record):
        """添加记录."""
        self._buffer.append(record)
        
        if len(self._buffer) >= self.batch_size:
            self.flush()
    
    def flush(self):
        """刷新缓冲区."""
        if not self._buffer:
            return
        
        # 执行批量插入
        self._bulk_insert(self._buffer)
        self._buffer.clear()
    
    def _bulk_insert(self, records):
        """批量插入实现."""
        # 实现批量插入逻辑
        pass


# ============================================================================
# 文件优化
# ============================================================================

import os
from pathlib import Path


class FileChunkReader:
    """文件分块读取器模板."""
    
    def __init__(self, filename, chunk_size=8192):
        self.filename = filename
        self.chunk_size = chunk_size
    
    def read_chunks(self):
        """读取文件块."""
        with open(self.filename, 'rb') as f:
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk:
                    break
                yield chunk
    
    def process_chunks(self, processor):
        """处理文件块."""
        for chunk in self.read_chunks():
            processor(chunk)


class ParallelFileProcessor:
    """并行文件处理器模板."""
    
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
    
    def process_files(self, file_paths, process_func):
        """并行处理多个文件."""
        return parallel_map(
            lambda path: self._process_single_file(path, process_func),
            file_paths,
            max_workers=self.max_workers
        )
    
    def _process_single_file(self, file_path, process_func):
        """处理单个文件."""
        return process_func(file_path)


# ============================================================================
# 性能监控
# ============================================================================

import time
from contextlib import contextmanager


class PerformanceMonitor:
    """性能监控器模板."""
    
    def __init__(self):
        self._metrics = {}
    
    @contextmanager
    def measure(self, name):
        """测量性能."""
        start_time = time.time()
        start_memory = self._get_memory_usage()
        
        try:
            yield
        finally:
            elapsed = time.time() - start_time
            memory_delta = self._get_memory_usage() - start_memory
            
            if name not in self._metrics:
                self._metrics[name] = []
            
            self._metrics[name].append({
                'time': elapsed,
                'memory': memory_delta
            })
    
    def get_metrics(self, name=None):
        """获取指标."""
        if name:
            return self._metrics.get(name, [])
        return self._metrics
    
    def get_average(self, name):
        """获取平均值."""
        metrics = self._metrics.get(name, [])
        if not metrics:
            return None
        
        avg_time = sum(m['time'] for m in metrics) / len(metrics)
        avg_memory = sum(m['memory'] for m in metrics) / len(metrics)
        
        return {'time': avg_time, 'memory': avg_memory}
    
    def _get_memory_usage(self):
        """获取内存使用量."""
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # MB


@contextmanager
def profile(func):
    """性能分析装饰器模板."""
    start_time = time.time()
    
    try:
        yield
    finally:
        elapsed = time.time() - start_time
        print(f'{func.__name__} took {elapsed:.4f} seconds')


# ============================================================================
# 数据结构优化
# ============================================================================

from collections import defaultdict, deque


class FastLookup:
    """快速查找模板."""
    
    def __init__(self):
        self._dict = {}
        self._index = defaultdict(list)
    
    def add(self, key, value):
        """添加项目."""
        if key not in self._dict:
            self._dict[key] = []
        
        item = {'key': key, 'value': value}
        self._dict[key].append(item)
        self._index[key].append(item)
    
    def get(self, key):
        """获取项目."""
        return self._dict.get(key, [])
    
    def find_all(self, keys):
        """查找多个键."""
        results = []
        for key in keys:
            results.extend(self.get(key))
        return results


class CircularBuffer:
    """环形缓冲区模板."""
    
    def __init__(self, size):
        self.size = size
        self.buffer = [None] * size
        self.head = 0
        self.tail = 0
        self.count = 0
    
    def append(self, item):
        """添加项目."""
        self.buffer[self.tail] = item
        self.tail = (self.tail + 1) % self.size
        
        if self.count == self.size:
            self.head = (self.head + 1) % self.size
        else:
            self.count += 1
    
    def pop(self):
        """弹出项目."""
        if self.count == 0:
            return None
        
        item = self.buffer[self.head]
        self.head = (self.head + 1) % self.size
        self.count -= 1
        
        return item
    
    def __len__(self):
        return self.count
    
    def __iter__(self):
        for i in range(self.count):
            yield self.buffer[(self.head + i) % self.size]


# ============================================================================
# 示例用法
# ============================================================================

if __name__ == '__main__':
    # 缓存示例
    @lru_cache(maxsize=128)
    def expensive_calculation(n):
        time.sleep(0.1)
        return n * n
    
    start = time.time()
    print(expensive_calculation(10))  # 第一次调用，耗时
    print(expensive_calculation(10))  # 第二次调用，使用缓存
    print(f'Time taken: {time.time() - start:.2f}s')
    
    # 批处理示例
    def process_batch(items):
        return [x * 2 for x in items]
    
    processor = BatchProcessor(batch_size=3)
    items = [1, 2, 3, 4, 5, 6, 7]
    results = processor.process(items)
    print(f'Batch processing results: {results}')
    
    # 惰性求值示例
    numbers = range(1000000)
    lazy_numbers = lazy_map(numbers, lambda x: x * 2)
    lazy_numbers = lazy_filter(lazy_numbers, lambda x: x > 10)
    
    # 只计算需要的值
    result = next(lazy_numbers)
    print(f'First lazy result: {result}')
    
    # 并行处理示例
    def square(x):
        return x * x
    
    numbers = list(range(10))
    results = parallel_map(square, numbers, max_workers=4)
    print(f'Parallel map results: {results}')
    
    # 字符串构建示例
    builder = StringBuilder()
    builder.append('Hello').append(' ').append('World').append_line('!')
    result = builder.build()
    print(f'String builder result: {result}')
    
    # 性能监控示例
    monitor = PerformanceMonitor()
    
    with monitor.measure('test_operation'):
        time.sleep(0.1)
    
    print(f'Performance metrics: {monitor.get_average("test_operation")}')
