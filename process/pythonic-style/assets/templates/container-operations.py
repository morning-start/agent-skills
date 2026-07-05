"""
Container Operations Templates

Common Pythonic patterns for container operations.
"""

# Template 1: List Comprehension
squares = [x ** 2 for x in range(10)]
even_numbers = [x for x in range(20) if x % 2 == 0]

# Template 2: Dictionary Comprehension
squares_dict = {x: x ** 2 for x in range(10)}
filtered_dict = {k: v for k, v in my_dict.items() if v > 0}

# Template 3: Set Comprehension
unique_chars = {char for char in text if char.isalpha()}

# Template 4: Generator Expression
sum_squares = sum(x ** 2 for x in range(100))

# Template 5: List Operations
def reverse_list(items):
    """反转列表."""
    return items[::-1]

def flatten_list(nested_list):
    """展平嵌套列表."""
    return [item for sublist in nested_list for item in sublist]

def remove_duplicates(items):
    """移除重复项（保持顺序）."""
    seen = set()
    return [x for x in items if not (x in seen or seen.add(x))]

# Template 6: Dictionary Operations
def merge_dicts(*dicts):
    """合并字典."""
    result = {}
    for d in dicts:
        result.update(d)
    return result

def get_nested_value(data, keys, default=None):
    """获取嵌套字典的值."""
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return default
    return data

# Template 7: Set Operations
def union_sets(*sets):
    """集合并集."""
    result = set()
    for s in sets:
        result.update(s)
    return result

def intersection_sets(*sets):
    """集合交集."""
    if not sets:
        return set()
    result = sets[0].copy()
    for s in sets[1:]:
        result.intersection_update(s)
    return result

# Template 8: Tuple Operations
def convert_to_tuple(items):
    """转换为元组."""
    return tuple(items)

def tuple_to_dict(items):
    """元组转字典."""
    return dict(items)

# Template 9: deque Operations
from collections import deque

def rotate_list(items, n):
    """旋转列表."""
    d = deque(items)
    d.rotate(n)
    return list(d)

# Template 10: defaultdict Usage
from collections import defaultdict

def group_by_key(items, key_func):
    """按键分组."""
    result = defaultdict(list)
    for item in items:
        result[key_func(item)].append(item)
    return dict(result)

# Template 11: Counter Usage
from collections import Counter

def count_occurrences(items):
    """统计出现次数."""
    return Counter(items)

def most_common(items, n=5):
    """最常见的项."""
    counter = Counter(items)
    return counter.most_common(n)

# Template 12: namedtuple Usage
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

def create_point(x, y):
    """创建点."""
    return Point(x, y)

# Template 13: Sorting Operations
def sort_by_key(items, key):
    """按键排序."""
    return sorted(items, key=lambda x: x[key])

def sort_multiple_keys(items, keys):
    """多键排序."""
    return sorted(items, key=lambda x: tuple(x[k] for k in keys))

# Template 14: Filtering Operations
def filter_by_condition(items, condition):
    """按条件过滤."""
    return [item for item in items if condition(item)]

def filter_unique(items, key_func=None):
    """过滤唯一项."""
    seen = set()
    result = []
    for item in items:
        key = key_func(item) if key_func else item
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result

# Template 15: Mapping Operations
def map_values(items, transform):
    """映射值."""
    return [transform(item) for item in items]

def map_dict_values(data, transform):
    """映射字典值."""
    return {k: transform(v) for k, v in data.items()}

# Template 16: Reducing Operations
from functools import reduce

def multiply_list(numbers):
    """列表乘积."""
    return reduce(lambda x, y: x * y, numbers, 1)

def concatenate_lists(*lists):
    """连接列表."""
    return reduce(lambda x, y: x + y, lists, [])

# Template 17: Partitioning
def partition(items, condition):
    """分区."""
    true_items = []
    false_items = []
    for item in items:
        if condition(item):
            true_items.append(item)
        else:
            false_items.append(item)
    return true_items, false_items

# Template 18: Chunking
def chunk_list(items, chunk_size):
    """分块."""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

# Template 19: Searching
def binary_search(items, value):
    """二分查找."""
    left, right = 0, len(items) - 1
    while left <= right:
        mid = (left + right) // 2
        if items[mid] == value:
            return mid
        elif items[mid] < value:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Template 20: Set Operations on Lists
def list_difference(list1, list2):
    """列表差集."""
    return [item for item in list1 if item not in list2]

def list_intersection(list1, list2):
    """列表交集."""
    return [item for item in list1 if item in list2]

# Template 21: Dictionary Transformations
def invert_dict(data):
    """反转字典."""
    return {v: k for k, v in data.items()}

def filter_dict(data, condition):
    """过滤字典."""
    return {k: v for k, v in data.items() if condition(k, v)}

# Template 22: List Accumulation
def accumulate_pairs(items):
    """累积对."""
    return [(items[i], items[i+1]) for i in range(len(items) - 1)]

# Template 23: Nested Container Operations
def flatten_dict(data, parent_key='', sep='.'):
    """展平嵌套字典."""
    items = []
    for k, v in data.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Template 24: Container Validation
def is_sequence(obj):
    """检查是否为序列."""
    return isinstance(obj, (list, tuple, str))

def is_mapping(obj):
    """检查是否为映射."""
    return isinstance(obj, dict)

# Template 25: Container Conversion
def to_list(obj):
    """转换为列表."""
    if isinstance(obj, list):
        return obj
    elif isinstance(obj, (tuple, set)):
        return list(obj)
    elif isinstance(obj, dict):
        return list(obj.items())
    else:
        return [obj]

def to_dict(pairs):
    """转换为字典."""
    if isinstance(pairs, dict):
        return pairs
    elif isinstance(pairs, list):
        return dict(pairs)
    else:
        raise ValueError('Cannot convert to dict')

# Template 26: Advanced Dictionary Operations
def get_or_create(data, key, default_factory):
    """获取或创建."""
    if key not in data:
        data[key] = default_factory()
    return data[key]

def deep_update(original, update):
    """深度更新字典."""
    for key, value in update.items():
        if isinstance(value, dict) and key in original and isinstance(original[key], dict):
            deep_update(original[key], value)
        else:
            original[key] = value
    return original

# Template 27: List Statistics
def list_statistics(items):
    """列表统计."""
    if not items:
        return {}
    
    return {
        'count': len(items),
        'unique': len(set(items)),
        'most_common': most_common(items, 1),
        'sum': sum(items) if all(isinstance(x, (int, float)) for x in items) else None
    }

# Template 28: Container Comparison
def containers_equal(container1, container2):
    """容器比较."""
    if isinstance(container1, dict) and isinstance(container2, dict):
        return container1 == container2
    elif isinstance(container1, (list, tuple, set)) and isinstance(container2, (list, tuple, set)):
        return set(container1) == set(container2)
    return False

# Template 29: Container Transformation
def transform_container(container, transform):
    """转换容器."""
    if isinstance(container, dict):
        return {k: transform(v) for k, v in container.items()}
    elif isinstance(container, (list, tuple, set)):
        return type(container)(transform(x) for x in container)
    else:
        return transform(container)

# Template 30: Zip and Enumerate Combinations
def zip_with_index(items):
    """带索引的 zip."""
    return list(enumerate(items))

def zip_multiple(*iterables):
    """多个可迭代对象的 zip."""
    return list(zip(*iterables))
