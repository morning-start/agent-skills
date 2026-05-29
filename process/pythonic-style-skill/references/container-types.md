# Mastering Container Types

## 目录
1. 列表（List）最佳实践
2. 字典（Dict）最佳实践
3. 集合（Set）最佳实践
4. 元组（Tuple）最佳实践
5. 容器推导式
6. 容器操作技巧
7. collections 模块
8. 容器性能考虑

## 概览
Python 提供了多种容器类型，每种类型都有其适用场景。掌握这些容器的最佳实践，能让代码更高效、更 Pythonic。本章基于《One Python Craftsman》第4章内容。

## 1. 列表（List）最佳实践

### 1.1 使用列表推导
**反模式**：
```python
squares = []
for i in range(10):
    squares.append(i ** 2)
```

**Pythonic**：
```python
squares = [i ** 2 for i in range(10)]
```

### 1.2 使用切片操作
```python
# 基本切片
items = [0, 1, 2, 3, 4, 5]
first_three = items[:3]  # [0, 1, 2]
last_three = items[-3:]  # [3, 4, 5]
middle = items[1:4]  # [1, 2, 3]

# 步长切片
every_other = items[::2]  # [0, 2, 4]
reversed_list = items[::-1]  # [5, 4, 3, 2, 1, 0]

# 修改切片
items[1:3] = [10, 20]  # [0, 10, 20, 3, 4, 5]
```

### 1.3 使用列表方法
```python
items = [1, 2, 3, 4, 5]

# 添加元素
items.append(6)  # [1, 2, 3, 4, 5, 6]
items.extend([7, 8])  # [1, 2, 3, 4, 5, 6, 7, 8]
items.insert(0, 0)  # [0, 1, 2, 3, 4, 5, 6, 7, 8]

# 删除元素
items.remove(8)  # [0, 1, 2, 3, 4, 5, 6, 7]
popped = items.pop()  # 7, 列表变为 [0, 1, 2, 3, 4, 5, 6]
items.clear()  # []

# 查找元素
items = [1, 2, 3, 4, 5]
index = items.index(3)  # 2
count = items.count(3)  # 1
```

### 1.4 排序和反转
```python
items = [3, 1, 4, 1, 5, 9, 2, 6]

# 排序（返回新列表）
sorted_items = sorted(items)  # [1, 1, 2, 3, 4, 5, 6, 9]

# 原地排序
items.sort()  # [1, 1, 2, 3, 4, 5, 6, 9]

# 反向排序
items.sort(reverse=True)  # [9, 6, 5, 4, 3, 2, 1, 1]

# 自定义排序
items.sort(key=lambda x: -x)  # [9, 6, 5, 4, 3, 2, 1, 1]

# 反转
items = [1, 2, 3, 4, 5]
items.reverse()  # [5, 4, 3, 2, 1]
reversed_items = items[::-1]  # [1, 2, 3, 4, 5]
```

## 2. 字典（Dict）最佳实践

### 2.1 使用字典推导
**反模式**：
```python
price_map = {}
for item in items:
    price_map[item.id] = item.price
```

**Pythonic**：
```python
price_map = {item.id: item.price for item in items}
```

### 2.2 使用 get() 方法
**反模式**：
```python
try:
    value = data['key']
except KeyError:
    value = None
```

**Pythonic**：
```python
value = data.get('key')
value = data.get('key', default_value)
```

### 2.3 使用 setdefault()
**反模式**：
```python
if 'key' not in data:
    data['key'] = []
data['key'].append(value)
```

**Pythonic**：
```python
data.setdefault('key', []).append(value)
```

### 2.4 使用 update() 方法
```python
# 合并字典
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}

dict1.update(dict2)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# 添加多个键值
dict1.update({'e': 5, 'f': 6})
```

### 2.5 字典解包（Python 3.5+）
```python
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}

# 合并字典
merged = {**dict1, **dict2}  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# 覆盖值
merged = {**dict1, 'a': 10}  # {'a': 10, 'b': 2}
```

### 2.6 遍历字典
```python
data = {'a': 1, 'b': 2, 'c': 3}

# 遍历键
for key in data:
    print(key)

# 遍历值
for value in data.values():
    print(value)

# 遍历键值对
for key, value in data.items():
    print(f'{key}: {value}')
```

### 2.7 字典视图
```python
data = {'a': 1, 'b': 2, 'c': 3}

# 获取键、值、项的视图
keys_view = data.keys()
values_view = data.values()
items_view = data.items()

# 视图是动态的
data['d'] = 4
print('d' in keys_view)  # True
```

## 3. 集合（Set）最佳实践

### 3.1 创建集合
```python
# 直接创建
s = {1, 2, 3, 4, 5}

# 从列表创建
s = set([1, 2, 3, 4, 5])

# 空集合（注意：不是 {}）
s = set()
```

### 3.2 集合操作
```python
s1 = {1, 2, 3, 4}
s2 = {3, 4, 5, 6}

# 并集
union = s1 | s2  # {1, 2, 3, 4, 5, 6}
union = s1.union(s2)

# 交集
intersection = s1 & s2  # {3, 4}
intersection = s1.intersection(s2)

# 差集
difference = s1 - s2  # {1, 2}
difference = s1.difference(s2)

# 对称差集
symmetric_diff = s1 ^ s2  # {1, 2, 5, 6}
symmetric_diff = s1.symmetric_difference(s2)
```

### 3.3 集合方法
```python
s = {1, 2, 3}

# 添加和删除
s.add(4)  # {1, 2, 3, 4}
s.remove(1)  # {2, 3, 4}（元素不存在会抛出异常）
s.discard(5)  # 不存在的元素不会抛出异常
s.pop()  # 随机删除并返回一个元素

# 批量操作
s.update({5, 6, 7})  # {2, 3, 4, 5, 6, 7}
s.clear()  # 清空集合
```

### 3.4 集合判断
```python
s1 = {1, 2, 3}
s2 = {1, 2, 3, 4, 5}

# 子集
print(s1.issubset(s2))  # True
print(s1 <= s2)  # True

# 真子集
print(s1 < s2)  # True

# 超集
print(s2.issuperset(s1))  # True
print(s2 >= s1)  # True

# 不相交
s3 = {4, 5, 6}
print(s1.isdisjoint(s3))  # True
```

### 3.5 去重
```python
# 使用集合去重
items = [1, 2, 2, 3, 4, 4, 5]
unique = list(set(items))  # [1, 2, 3, 4, 5]（顺序可能改变）

# 保持顺序去重
from collections import OrderedDict
unique = list(OrderedDict.fromkeys(items))

# Python 3.7+（字典保持顺序）
unique = list(dict.fromkeys(items))
```

## 4. 元组（Tuple）最佳实践

### 4.1 创建元组
```python
# 直接创建
t = (1, 2, 3)

# 单元素元组
t = (1,)  # 注意逗号

# 不使用括号
t = 1, 2, 3

# 从其他容器创建
t = tuple([1, 2, 3])
```

### 4.2 元组解包
```python
# 基本解包
t = (1, 2, 3)
a, b, c = t  # a=1, b=2, c=3

# 嵌套解包
t = (1, (2, 3))
a, (b, c) = t  # a=1, b=2, c=3

# 使用 * 忽略某些值
t = (1, 2, 3, 4, 5)
a, b, *rest = t  # a=1, b=2, rest=[3, 4, 5]
*rest, last = t  # rest=[1, 2, 3, 4], last=5
first, *middle, last = t  # first=1, middle=[2, 3, 4], last=5
```

### 4.3 命名元组
```python
from collections import namedtuple

# 创建命名元组
Point = namedtuple('Point', ['x', 'y'])

# 使用
p = Point(1, 2)
print(p.x)  # 1
print(p.y)  # 2
print(p[0])  # 1

# 转换为字典
print(p._asdict())  # {'x': 1, 'y': 2}
```

### 4.4 元组 vs 列表
```python
# 使用元组：不可变的数据
coordinates = (10.5, 20.3)
rgb_color = (255, 128, 0)

# 使用列表：可变的数据
items = []
for _ in range(10):
    items.append(get_item())
```

## 5. 容器推导式

### 5.1 列表推导
```python
# 基本用法
squares = [x ** 2 for x in range(10)]

# 带条件
evens = [x for x in range(20) if x % 2 == 0]

# 嵌套推导
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
# [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
```

### 5.2 字典推导
```python
# 基本用法
squares = {x: x ** 2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 带条件
even_squares = {x: x ** 2 for x in range(10) if x % 2 == 0}

# 字典转换
data = {'a': 1, 'b': 2, 'c': 3}
upper_keys = {k.upper(): v for k, v in data.items()}
```

### 5.3 集合推导
```python
# 基本用法
squares = {x ** 2 for x in range(6)}
# {0, 1, 4, 9, 16, 25}

# 带条件
even_squares = {x ** 2 for x in range(10) if x % 2 == 0}
```

### 5.4 生成器表达式
```python
# 基本用法
squares = (x ** 2 for x in range(10))

# 用于函数
total = sum(x ** 2 for x in range(10))

# 创建列表
squares_list = list(x ** 2 for x in range(10))
```

## 6. 容器操作技巧

### 6.1 使用 enumerate
```python
items = ['a', 'b', 'c']

# 带索引遍历
for index, item in enumerate(items):
    print(index, item)

# 指定起始索引
for index, item in enumerate(items, start=1):
    print(index, item)
```

### 6.2 使用 zip
```python
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]

# 并行遍历
for name, age in zip(names, ages):
    print(f'{name}: {age}')

# 创建字典
user_dict = dict(zip(names, ages))

# 解包
zipped = list(zip(names, ages))  # [('Alice', 25), ('Bob', 30), ('Charlie', 35)]
names, ages = zip(*zipped)  # ('Alice', 'Bob', 'Charlie'), (25, 30, 35)
```

### 6.3 使用 sorted
```python
# 基本排序
items = [3, 1, 4, 1, 5]
sorted_items = sorted(items)  # [1, 1, 3, 4, 5]

# 反向排序
sorted_items = sorted(items, reverse=True)  # [5, 4, 3, 1, 1]

# 自定义排序
users = [
    {'name': 'Alice', 'age': 25},
    {'name': 'Bob', 'age': 30},
    {'name': 'Charlie', 'age': 20}
]
sorted_users = sorted(users, key=lambda x: x['age'])
```

### 6.4 使用 filter 和 map
```python
# filter
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4, 6]

# map
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))  # [1, 4, 9, 16, 25]

# 链式操作
result = list(
    map(lambda x: x ** 2,
        filter(lambda x: x % 2 == 0,
               range(10)))
)
# [0, 4, 16, 36, 64]
```

## 7. collections 模块

### 7.1 defaultdict
```python
from collections import defaultdict

# 计数
words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
word_count = defaultdict(int)
for word in words:
    word_count[word] += 1

# 分组
from collections import defaultdict
data = [('a', 1), ('b', 2), ('a', 3), ('b', 4)]
grouped = defaultdict(list)
for key, value in data:
    grouped[key].append(value)
```

### 7.2 Counter
```python
from collections import Counter

# 计数
words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
word_count = Counter(words)
# Counter({'apple': 3, 'banana': 2, 'orange': 1})

# 最常见的元素
most_common = word_count.most_common(2)
# [('apple', 3), ('banana', 2)]

# 更新
word_count.update(['apple', 'pear'])
```

### 7.3 OrderedDict
```python
from collections import OrderedDict

# 创建有序字典（Python 3.7+ 普通字典也保持顺序）
od = OrderedDict()
od['a'] = 1
od['b'] = 2
od['c'] = 3

# 按插入顺序遍历
for key, value in od.items():
    print(key, value)
```

### 7.4 deque
```python
from collections import deque

# 创建双端队列
d = deque([1, 2, 3])

# 两端操作
d.append(4)  # [1, 2, 3, 4]
d.appendleft(0)  # [0, 1, 2, 3, 4]
d.pop()  # 4, [0, 1, 2, 3]
d.popleft()  # 0, [1, 2, 3]

# 旋转
d.rotate(1)  # [3, 1, 2]
d.rotate(-1)  # [1, 2, 3]
```

## 8. 容器性能考虑

### 8.1 时间复杂度
- 列表：O(n) 查找，O(1) 索引访问
- 字典：O(1) 平均查找，O(n) 最坏
- 集合：O(1) 平均查找，O(n) 最坏
- 元组：O(n) 查找，O(1) 索引访问

### 8.2 选择合适的数据结构
```python
# 需要快速查找：使用集合或字典
items = set(large_list)
if item in items:  # O(1)
    process(item)

# 需要保持顺序：使用列表
items = []
items.append(item)

# 需要键值对：使用字典
data = {}
data[key] = value

# 需要不可变的数据：使用元组
coordinates = (10.5, 20.3)
```

### 8.3 内存优化
```python
# 使用 __slots__ 减少内存
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 使用 array 替代列表存储数值
import array
numbers = array.array('i', [1, 2, 3, 4, 5])
```

## 示例

### 示例 1：数据分组
```python
from collections import defaultdict

def group_by_key(items, key_func):
    """按键分组."""
    grouped = defaultdict(list)
    for item in items:
        key = key_func(item)
        grouped[key].append(item)
    return dict(grouped)

# 使用
users = [
    {'name': 'Alice', 'age': 25, 'city': 'NYC'},
    {'name': 'Bob', 'age': 30, 'city': 'LA'},
    {'name': 'Charlie', 'age': 25, 'city': 'NYC'},
]

grouped = group_by_key(users, lambda x: x['age'])
# {25: [{'name': 'Alice', ...}, {'name': 'Charlie', ...}],
#  30: [{'name': 'Bob', ...}]}
```

### 示例 2：数据转换
```python
def transform_data(data):
    """转换数据格式."""
    # 列表转字典
    item_dict = {item['id']: item for item in data}
    
    # 提取特定字段
    names = [item['name'] for item in data]
    
    # 筛选数据
    active_items = [item for item in data if item.get('active')]
    
    # 计算统计
    total = sum(item['value'] for item in data)
    average = total / len(data) if data else 0
    
    return {
        'item_dict': item_dict,
        'names': names,
        'active_items': active_items,
        'total': total,
        'average': average
    }
```

### 示例 3：合并字典
```python
def merge_configs(*configs):
    """合并多个配置字典."""
    merged = {}
    for config in configs:
        merged.update(config)
    return merged

# 使用
default_config = {'timeout': 30, 'retries': 3}
user_config = {'timeout': 60}
env_config = {'debug': True}

final_config = merge_configs(default_config, user_config, env_config)
# {'timeout': 60, 'retries': 3, 'debug': True}
```

### 示例 4：使用 Counter 统计
```python
from collections import Counter

def analyze_text(text):
    """分析文本."""
    # 统计词频
    words = text.lower().split()
    word_count = Counter(words)
    
    # 最常见的词
    top_words = word_count.most_common(10)
    
    # 总词数
    total_words = len(words)
    
    # 唯一词数
    unique_words = len(word_count)
    
    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'top_words': top_words,
        'word_count': dict(word_count)
    }

# 使用
text = "Python is awesome. Python is great. I love Python."
result = analyze_text(text)
print(result)
```

### 示例 5：使用 deque 实现队列
```python
from collections import deque

class Queue:
    """队列实现."""
    
    def __init__(self):
        self._items = deque()
    
    def enqueue(self, item):
        """入队."""
        self._items.append(item)
    
    def dequeue(self):
        """出队."""
        if not self.is_empty():
            return self._items.popleft()
        return None
    
    def is_empty(self):
        """判断是否为空."""
        return len(self._items) == 0
    
    def size(self):
        """队列大小."""
        return len(self._items)

# 使用
queue = Queue()
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
print(queue.dequeue())  # 1
print(queue.dequeue())  # 2
print(queue.size())  # 1
```
