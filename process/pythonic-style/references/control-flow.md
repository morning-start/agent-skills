# Control Flow and If-Else Block Secrets

## 目录
1. if-else 语句优化
2. 卫语句（Guard Clauses）
3. 提前返回（Early Return）
4. 条件表达式
5. 海象运算符（Walrus Operator）
6. 循环优化
7. match-case 结构
8. 避免深层嵌套

## 概览
良好的控制流结构能让代码更清晰、更易读。Python 提供了多种方式来优化条件判断和循环结构。本章基于《One Python Craftsman》第2、7、16章内容。

## 1. if-else 语句优化

### 1.1 使用提前返回
**反模式**：
```python
def process_user(user):
    if user is not None:
        if user.is_active:
            if user.has_permission:
                return process_data(user.data)
            else:
                return 'No permission'
        else:
            return 'User inactive'
    else:
        return 'No user'
```

**Pythonic**：
```python
def process_user(user):
    if user is None:
        return 'No user'
    
    if not user.is_active:
        return 'User inactive'
    
    if not user.has_permission:
        return 'No permission'
    
    return process_data(user.data)
```

### 1.2 使用字典替代多重 if-else
**反模式**：
```python
def get_role_name(role_id):
    if role_id == 1:
        return 'Admin'
    elif role_id == 2:
        return 'User'
    elif role_id == 3:
        return 'Guest'
    else:
        return 'Unknown'
```

**Pythonic**：
```python
def get_role_name(role_id):
    role_names = {
        1: 'Admin',
        2: 'User',
        3: 'Guest'
    }
    return role_names.get(role_id, 'Unknown')
```

### 1.3 使用 any() 和 all()
**反模式**：
```python
def has_positive_numbers(numbers):
    found = False
    for num in numbers:
        if num > 0:
            found = True
            break
    return found

def all_positive(numbers):
    for num in numbers:
        if num <= 0:
            return False
    return True
```

**Pythonic**：
```python
def has_positive_numbers(numbers):
    return any(num > 0 for num in numbers)

def all_positive(numbers):
    return all(num > 0 for num in numbers)
```

## 2. 卫语句（Guard Clauses）

### 2.1 卫语句原则
卫语句用于在函数开始处检查边界条件，使主逻辑更清晰。

**反模式**：
```python
def process_user(user):
    if user is not None:
        if user.is_active:
            if user.has_permission:
                # 主逻辑
                return do_something(user)
            else:
                return 'No permission'
        else:
            return 'User inactive'
    else:
        return 'No user'
```

**Pythonic（使用卫语句）**：
```python
def process_user(user):
    # 卫语句：处理边界条件
    if user is None:
        return 'No user'
    
    if not user.is_active:
        return 'User inactive'
    
    if not user.has_permission:
        return 'No permission'
    
    # 主逻辑：正常流程
    return do_something(user)
```

### 2.2 卫语句的优势
- 减少嵌套层级
- 提高代码可读性
- 突出主逻辑
- 使边界条件一目了然

### 2.3 卫语句示例

#### 示例 1：参数验证
```python
# 反模式
def calculate_discount(price, customer_type):
    if price is not None:
        if price > 0:
            if customer_type in ['vip', 'regular']:
                if customer_type == 'vip':
                    return price * 0.8
                else:
                    return price * 0.9
    return None

# Pythonic
def calculate_discount(price, customer_type):
    # 卫语句
    if price is None or price <= 0:
        return None
    
    if customer_type not in ['vip', 'regular']:
        return None
    
    # 主逻辑
    return price * 0.8 if customer_type == 'vip' else price * 0.9
```

#### 示例 2：数据处理
```python
# 反模式
def process_data(data):
    if data is not None:
        if isinstance(data, list):
            if len(data) > 0:
                # 主逻辑
                return [item * 2 for item in data]
            else:
                return []
        else:
            return None
    else:
        return None

# Pythonic
def process_data(data):
    # 卫语句
    if data is None:
        return None
    
    if not isinstance(data, list):
        return None
    
    if not data:
        return []
    
    # 主逻辑
    return [item * 2 for item in data]
```

## 3. 提前返回（Early Return）

### 3.1 提前返回原则
在发现异常或不符合条件时立即返回，避免继续执行不必要的逻辑。

**反模式**：
```python
def validate_user(user):
    result = False
    
    if user is not None:
        if user.name:
            if user.email:
                if user.age >= 18:
                    result = True
    
    return result
```

**Pythonic**：
```python
def validate_user(user):
    if user is None:
        return False
    
    if not user.name:
        return False
    
    if not user.email:
        return False
    
    if user.age < 18:
        return False
    
    return True
```

### 3.2 提前返回 vs 卫语句
- **卫语句**：在函数开始处处理边界条件
- **提前返回**：可以在函数任何地方返回

### 3.3 提前返回示例

#### 示例 1：搜索功能
```python
def find_user(users, user_id):
    for user in users:
        if user.id == user_id:
            return user  # 找到后立即返回
    return None  # 未找到
```

#### 示例 2：条件处理
```python
def process_request(request):
    # 快速路径：简单请求
    if request.method == 'GET' and request.path == '/health':
        return {'status': 'ok'}
    
    # 正常路径
    return handle_request(request)
```

## 4. 条件表达式

### 4.1 三元运算符
**反模式**：
```python
def get_greeting(name):
    if name:
        return f'Hello, {name}'
    else:
        return 'Hello, Stranger'
```

**Pythonic**：
```python
def get_greeting(name):
    return f'Hello, {name}' if name else 'Hello, Stranger'
```

### 4.2 链式条件表达式
```python
def get_grade(score):
    return (
        'A' if score >= 90 else
        'B' if score >= 80 else
        'C' if score >= 70 else
        'D' if score >= 60 else
        'F'
    )
```

### 4.3 条件表达式最佳实践
- 只用于简单条件
- 避免嵌套过深
- 考虑使用字典映射

**反模式**：
```python
result = (
    'A' if condition1 else
    'B' if condition2 else
    'C' if condition3 else
    'D' if condition4 else
    'E' if condition5 else
    'F'
)
```

**Pythonic**：
```python
def get_result(condition):
    mapping = {
        cond1: 'A',
        cond2: 'B',
        cond3: 'C',
        cond4: 'D',
        cond5: 'E'
    }
    return mapping.get(condition, 'F')
```

## 5. 海象运算符（Walrus Operator）

### 5.1 基本用法
海象运算符（:=）可以在表达式内部进行赋值。

**反模式**：
```python
data = fetch_data()
if data:
    process(data)
```

**Pythonic（Python 3.8+）**：
```python
if data := fetch_data():
    process(data)
```

### 5.2 避免重复计算
**反模式**：
```python
while True:
    line = read_line()
    if not line:
        break
    process(line)
```

**Pythonic**：
```python
while line := read_line():
    process(line)
```

### 5.3 列表推导式中的赋值
**反模式**：
```python
results = []
for item in items:
    value = calculate(item)
    if value > 10:
        results.append(value)
```

**Pythonic**：
```python
results = [value for item in items if (value := calculate(item)) > 10]
```

### 5.4 复杂条件中的赋值
```python
# 检查用户权限并获取角色
if (user := get_user(user_id)) and (role := get_role(user.role_id)):
    process_with_role(user, role)

# 多重赋值和验证
if (
    (data := fetch_data()) and
    (validated := validate(data)) and
    (result := process(validated))
):
    return result
```

### 5.5 海象运算符最佳实践
- 避免在复杂表达式中过度使用
- 保持代码可读性
- 考虑是否值得使用

**反模式**：
```python
# 过度使用，难以理解
if (a := get_a()) and (b := get_b(a)) and (c := get_c(b)) and (d := get_d(c)):
    process(d)
```

**Pythonic**：
```python
# 分步骤，更清晰
a = get_a()
if not a:
    return

b = get_b(a)
if not b:
    return

c = get_c(b)
if not c:
    return

d = get_d(c)
if d:
    process(d)
```

## 6. 循环优化

### 6.1 使用列表推导替代循环
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

### 6.2 使用生成器表达式
**反模式**：
```python
# 处理大数据时，列表推导消耗大量内存
total = 0
for i in range(1000000):
    total += i ** 2
```

**Pythonic**：
```python
# 生成器表达式惰性求值
total = sum(i ** 2 for i in range(1000000))
```

### 6.3 使用 enumerate 获取索引
**反模式**：
```python
for i in range(len(items)):
    print(i, items[i])
```

**Pythonic**：
```python
for index, item in enumerate(items):
    print(index, item)
```

### 6.4 使用 zip 遍历多个序列
**反模式**：
```python
for i in range(len(names)):
    print(names[i], ages[i])
```

**Pythonic**：
```python
for name, age in zip(names, ages):
    print(name, age)
```

### 6.5 使用字典推导
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

### 6.6 使用 set 去重
**反模式**：
```python
unique_items = []
for item in items:
    if item not in unique_items:
        unique_items.append(item)
```

**Pythonic**：
```python
unique_items = list(set(items))
```

## 7. match-case 结构（Python 3.10+）

### 7.1 基本用法
```python
def handle_command(command):
    match command:
        case 'start':
            print('Starting...')
        case 'stop':
            print('Stopping...')
        case 'restart':
            print('Restarting...')
        case _:
            print('Unknown command')
```

### 7.2 模式匹配
```python
def process_data(data):
    match data:
        case {'type': 'user', 'id': user_id, 'name': name}:
            return f"User {name} (ID: {user_id})"
        case {'type': 'product', 'id': product_id}:
            return f"Product (ID: {product_id})"
        case _:
            return "Unknown data type"
```

### 7.3 模式解包
```python
def analyze_point(point):
    match point:
        case (0, 0):
            return "Origin"
        case (x, 0):
            return f"X-axis at {x}"
        case (0, y):
            return f"Y-axis at {y}"
        case (x, y) if x == y:
            return f"Diagonal at ({x}, {y})"
        case (x, y):
            return f"Point at ({x}, {y})"
```

### 7.4 带条件的模式匹配
```python
def classify_number(n):
    match n:
        case x if x < 0:
            return "Negative"
        case 0:
            return "Zero"
        case x if x % 2 == 0:
            return "Positive even"
        case _:
            return "Positive odd"
```

## 8. 避免深层嵌套

### 8.1 使用提前返回减少嵌套
**反模式**：
```python
def process_order(order):
    if order:
        if order.items:
            if order.user:
                if order.user.is_active:
                    # 深层嵌套
                    process(order)
```

**Pythonic**：
```python
def process_order(order):
    if not order:
        return
    
    if not order.items:
        return
    
    if not order.user:
        return
    
    if not order.user.is_active:
        return
    
    process(order)
```

### 8.2 使用辅助函数减少嵌套
**反模式**：
```python
def process_data(data):
    if data:
        if isinstance(data, list):
            for item in data:
                if item:
                    if isinstance(item, dict):
                        if 'value' in item:
                            process_item(item)
```

**Pythonic**：
```python
def process_data(data):
    if not data:
        return
    
    if not isinstance(data, list):
        return
    
    for item in data:
        process_item_if_valid(item)

def process_item_if_valid(item):
    if not item:
        return
    
    if not isinstance(item, dict):
        return
    
    if 'value' not in item:
        return
    
    process_item(item)
```

## 9. 控制流最佳实践

### 9.1 优先使用内置函数
- 使用 `any()` 和 `all()` 替代循环判断
- 使用 `max()` 和 `min()` 替代循环查找
- 使用 `sum()` 替代循环求和
- 使用 `filter()` 和 `map()` 函数式处理

### 9.2 保持控制流简单
- 每个函数只做一件事
- 减少嵌套层级
- 使用有意义的变量名
- 添加必要的注释

### 9.3 避免过长的条件
**反模式**：
```python
if condition1 and condition2 and condition3 and condition4 and condition5:
    do_something()
```

**Pythonic**：
```python
conditions_met = (
    condition1 and
    condition2 and
    condition3 and
    condition4 and
    condition5
)

if conditions_met:
    do_something()
```

## 示例

### 示例 1：综合控制流优化
```python
# 反模式
def process_user(user):
    if user is not None:
        if user.is_active:
            if user.age >= 18:
                if user.has_permission:
                    if user.email:
                        # 主逻辑
                        return send_email(user.email, 'Welcome!')
                    else:
                        return 'No email'
                else:
                    return 'No permission'
            else:
                return 'Too young'
        else:
            return 'Inactive'
    else:
        return 'No user'

# Pythonic
def process_user(user):
    """处理用户，使用卫语句."""
    # 卫语句
    if not user:
        return 'No user'
    
    if not user.is_active:
        return 'Inactive'
    
    if user.age < 18:
        return 'Too young'
    
    if not user.has_permission:
        return 'No permission'
    
    if not user.email:
        return 'No email'
    
    # 主逻辑
    return send_email(user.email, 'Welcome!')
```

### 示例 2：使用海象运算符优化
```python
# 反模式
def find_first_positive(numbers):
    for num in numbers:
        if num > 0:
            # 重复计算
            result = num ** 2
            if result > 100:
                return result
    return None

# Pythonic
def find_first_positive(numbers):
    for num in numbers:
        if num > 0 and (result := num ** 2) > 100:
            return result
    return None
```

### 示例 3：match-case 使用
```python
def handle_response(response):
    """处理 HTTP 响应."""
    match response.status_code:
        case 200:
            return response.json()
        case 201:
            return response.json()
        case 400:
            raise ValueError("Bad request")
        case 401:
            raise PermissionError("Unauthorized")
        case 404:
            raise ValueError("Not found")
        case 500:
            raise RuntimeError("Server error")
        case _:
            raise ValueError(f"Unknown status: {response.status_code}")
```

### 示例 4：循环优化
```python
# 反模式
def process_items(items):
    result = []
    for item in items:
        if item is not None:
            if isinstance(item, dict):
                if 'value' in item:
                    if item['value'] > 0:
                        result.append(item['value'] * 2)
    return result

# Pythonic
def process_items(items):
    return [
        item['value'] * 2
        for item in items
        if item and isinstance(item, dict) and 'value' in item and item['value'] > 0
    ]
```
