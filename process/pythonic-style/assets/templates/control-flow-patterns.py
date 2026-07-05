"""
Control Flow Patterns Templates

Common Pythonic control flow patterns.
"""

# Template 1: Early Return
def process_user(user):
    """提前返回."""
    if user is None:
        return 'No user'
    
    if not user.is_active:
        return 'User inactive'
    
    if not user.has_permission:
        return 'No permission'
    
    return process_data(user.data)

# Template 2: Guard Clauses
def validate_user(user):
    """卫语句."""
    if not user:
        raise ValueError('User cannot be None')
    
    if not user.name:
        raise ValueError('Name is required')
    
    if not user.email:
        raise ValueError('Email is required')
    
    return user

# Template 3: Dictionary Lookup
def get_role_name(role_id):
    """字典查找."""
    role_names = {
        1: 'Admin',
        2: 'User',
        3: 'Guest'
    }
    return role_names.get(role_id, 'Unknown')

# Template 4: List Comprehension with Condition
def filter_even_numbers(numbers):
    """过滤偶数."""
    return [num for num in numbers if num % 2 == 0]

# Template 5: Dictionary Comprehension
def create_squares(numbers):
    """创建平方字典."""
    return {num: num ** 2 for num in numbers}

# Template 6: enumerate Usage
def process_with_index(items):
    """带索引处理."""
    for index, item in enumerate(items):
        print(f'{index}: {item}')

# Template 7: zip Usage
def combine_lists(names, ages):
    """组合列表."""
    result = []
    for name, age in zip(names, ages):
        result.append({'name': name, 'age': age})
    return result

# Template 8: any/all Usage
def has_positive(numbers):
    """是否有正数."""
    return any(num > 0 for num in numbers)

def all_positive(numbers):
    """是否全部为正数."""
    return all(num > 0 for num in numbers)

# Template 9: Conditional Expression
def get_status(age):
    """条件表达式."""
    return 'adult' if age >= 18 else 'minor'

# Template 10: Chained Comparison
def in_range(value, min_val, max_val):
    """链式比较."""
    return min_val <= value <= max_val

# Template 11: Walrus Operator (Python 3.8+)
def find_first_match(patterns, text):
    """海象运算符."""
    import re
    for pattern in patterns:
        if match := re.search(pattern, text):
            return match.group(1)
    return None

# Template 12: Multiple Returns
def calculate_grade(score):
    """多个返回."""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

# Template 13: Default Arguments
def connect(host='localhost', port=5432, database='mydb'):
    """默认参数."""
    connection_string = f'{host}:{port}/{database}'
    return connection_string

# Template 14: Keyword-Only Arguments
def send_email(to, subject, *, priority=1, cc=None, bcc=None):
    """仅关键字参数."""
    pass

# Template 15: *args and **kwargs
def log_message(message, *args, **kwargs):
    """可变参数."""
    timestamp = kwargs.get('timestamp', datetime.now())
    level = kwargs.get('level', 'INFO')
    print(f'[{timestamp}] {level}: {message}')

# Template 16: try-except-else-finally
def process_file(filename):
    """完整的异常处理."""
    try:
        with open(filename) as f:
            content = f.read()
    except FileNotFoundError:
        return None
    else:
        return content.strip()
    finally:
        pass

# Template 17: Context Manager
with open('file.txt', 'r') as f:
    content = f.read()

# Template 18: Nested Context Managers
with open('input.txt', 'r') as infile, open('output.txt', 'w') as outfile:
    outfile.write(infile.read())

# Template 19: Generator Function
def read_large_file(filename):
    """生成器函数."""
    with open(filename) as f:
        for line in f:
            yield line.strip()

# Template 20: For-Else Loop
def find_prime(numbers):
    """for-else 循环."""
    for num in numbers:
        if is_prime(num):
            print(f'Found prime: {num}')
            break
    else:
        print('No prime found')

# Template 21: While with Condition
def wait_for_condition(condition_func, timeout=30):
    """等待条件."""
    import time
    start = time.time()
    while time.time() - start < timeout:
        if condition_func():
            return True
        time.sleep(0.1)
    return False

# Template 22: Multiple Assignments
def swap_values(a, b):
    """多重赋值."""
    a, b = b, a
    return a, b

# Template 23: Tuple Unpacking
def process_user_data(user_data):
    """元组解包."""
    name, email, age = user_data
    return {
        'name': name,
        'email': email,
        'age': age
    }

# Template 24: Extended Iterable Unpacking
def split_list(items):
    """扩展迭代解包."""
    first, *middle, last = items
    return first, middle, last

# Template 25: Set Operations
def unique_items(items):
    """集合操作."""
    return list(set(items))

def common_items(list1, list2):
    """共同元素."""
    return list(set(list1) & set(list2))

# Template 26: Slice Operations
def reverse_list(items):
    """切片反转."""
    return items[::-1]

def every_nth(items, n):
    """每 n 个元素."""
    return items[::n]

# Template 27: Sorting with Key
def sort_users_by_age(users):
    """按键排序."""
    return sorted(users, key=lambda user: user['age'])

# Template 28: Custom Exception Handling
def custom_exception_handling():
    """自定义异常处理."""
    try:
        risky_operation()
    except ValueError as e:
        logger.error(f'Validation error: {e}')
    except TypeError as e:
        logger.error(f'Type error: {e}')
    except Exception as e:
        logger.exception('Unexpected error')
        raise

# Template 29: Multiple Exception Types
def handle_multiple_exceptions():
    """处理多个异常类型."""
    try:
        operation()
    except (ValueError, TypeError) as e:
        logger.error(f'Error: {e}')
    except Exception as e:
        logger.exception('Unexpected error')
        raise

# Template 30: Exception Chaining
def chain_exceptions():
    """异常链."""
    try:
        risky_operation()
    except Exception as e:
        raise CustomError('Operation failed') from e
