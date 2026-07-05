# Using Variables Well

## 目录
1. 命名基本原则
2. 布尔变量命名
3. 避免信息丢失的类型命名
4. 减少中间变量
5. 循环变量命名
6. 临时变量和下划线

## 概览
良好的变量命名是编写 Pythonic 代码的基础。清晰、准确的命名能让代码自解释，提高可读性和维护性。本章基于《One Python Craftsman》第1章内容。

## 1. 命名基本原则

### 1.1 使用有意义的名称
**反模式**：
```python
a = 5
b = 10
c = a + b
```

**Pythonic**：
```python
base_price = 5
tax = 10
total_price = base_price + tax
```

### 1.2 使用 snake_case 命名变量和函数
```python
user_name = 'Alice'
get_user_info()
calculate_total()
```

### 1.3 使用 PascalCase 命名类
```python
class UserProfile:
    pass

class DatabaseConnection:
    pass
```

### 1.4 使用 UPPER_CASE 命名常量
```python
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30
API_BASE_URL = 'https://api.example.com'
```

### 1.5 使用动词或动词短语命名函数
**反模式**：
```python
def user(data):
    pass

def calculation(x, y):
    pass
```

**Pythonic**：
```python
def create_user(data):
    pass

def calculate_sum(x, y):
    pass
```

## 2. 布尔变量命名

### 2.1 使用 is/has/can/should 前缀
**反模式**：
```python
active = True
permission = True
available = False
```

**Pythonic**：
```python
is_active = True
has_permission = True
can_edit = True
should_retry = False
```

### 2.2 避免否定形式的布尔变量
**反模式**：
```python
not_active = True
not_logged_in = False
```

**Pythonic**：
```python
is_active = False
is_logged_in = True
```

### 2.3 布尔函数命名
```python
def is_valid_email(email):
    """验证邮箱格式."""
    pass

def has_permission(user, resource):
    """检查用户权限."""
    pass

def can_execute(task):
    """检查任务是否可执行."""
    pass

def should_retry(attempt, max_attempts):
    """判断是否应该重试."""
    pass
```

## 3. 避免信息丢失的类型命名

### 3.1 不使用类型前缀（匈牙利命名法）
**反模式**：
```python
str_name = 'Alice'
int_age = 25
lst_items = [1, 2, 3]
dict_config = {}
```

**Pythonic**：
```python
name = 'Alice'
age = 25
items = [1, 2, 3]
config = {}
```

### 3.2 使用描述性名称替代类型信息
**反模式**：
```python
# 使用列表命名，但内容可能包含其他类型
user_list = get_users()

# 使用字典命名，但值可能不是配置
user_dict = {'name': 'Alice', 'age': 25}
```

**Pythonic**：
```python
# 根据实际用途命名
users = get_users()
user_data = {'name': 'Alice', 'age': 25}
user_info = {'name': 'Alice', 'age': 25}
```

### 3.3 集合类型命名建议
```python
# 单数名称：单个元素
user = get_user()

# 复数名称：集合
users = get_all_users()

# 描述性名称：特定用途的集合
active_users = get_active_users()
admin_accounts = get_admin_accounts()

# 使用集合类型名称
user_set = set(users)
user_dict = {user.id: user for user in users}
user_map = {user.id: user for user in users}
```

## 4. 减少中间变量

### 4.1 避免不必要的临时变量
**反模式**：
```python
def calculate_price(quantity, price_per_unit):
    temp1 = quantity * price_per_unit
    temp2 = temp1 * 1.1  # 加税
    temp3 = temp2 + 5    # 运费
    return temp3
```

**Pythonic**：
```python
def calculate_price(quantity, price_per_unit):
    subtotal = quantity * price_per_unit
    total = subtotal * 1.1 + 5
    return total
```

### 4.2 使用链式调用替代中间变量
**反模式**：
```python
def process_text(text):
    temp1 = text.lower()
    temp2 = temp1.strip()
    temp3 = temp2.replace(' ', '_')
    return temp3
```

**Pythonic**：
```python
def process_text(text):
    return text.lower().strip().replace(' ', '_')
```

### 4.3 避免无意义的中间变量
**反模式**：
```python
def get_user(user_id):
    result = db.query('SELECT * FROM users WHERE id = ?', (user_id,))
    return result

def validate_data(data):
    is_valid = validate_email(data['email']) and validate_phone(data['phone'])
    return is_valid
```

**Pythonic**：
```python
def get_user(user_id):
    return db.query('SELECT * FROM users WHERE id = ?', (user_id,))

def validate_data(data):
    return validate_email(data['email']) and validate_phone(data['phone'])
```

## 5. 循环变量命名

### 5.1 使用描述性的循环变量
**反模式**：
```python
for i in users:
    print(i.name)
    print(i.email)
```

**Pythonic**：
```python
for user in users:
    print(user.name)
    print(user.email)
```

### 5.2 使用有意义的索引变量
**反模式**：
```python
for i in range(len(items)):
    print(f"Item {i}: {items[i]}")
```

**Pythonic**：
```python
for index, item in enumerate(items):
    print(f"Item {index}: {item}")
```

### 5.3 解包循环变量
**反模式**：
```python
for item in items:
    key = item[0]
    value = item[1]
    print(f"{key}: {value}")
```

**Pythonic**：
```python
for key, value in items:
    print(f"{key}: {value}")
```

### 5.4 使用 _ 表示忽略的值
```python
# 忽略索引
for _ in range(10):
    do_something()

# 忽略某些值
for _, value in items:
    process(value)

# 忽略多个值
for user_id, _, _, email in user_data:
    print(email)
```

## 6. 临时变量和下划线

### 6.1 使用 _ 表示临时结果
```python
# 使用 _ 接受不需要的返回值
length, _ = get_file_size('data.txt')
_, extension = os.path.splitext('file.txt')

# 使用 _ 表示未使用的变量（临时）
def calculate(a, b, c):
    result = a + b
    _ = c  # 临时计算但不使用
    return result
```

### 6.2 使用 __ 表示私有变量
```python
class MyClass:
    def __init__(self):
        self.__private_data = None  # 名字重整，真正私有
    
    def _internal_method(self):
        """内部方法，约定私有."""
        pass
```

### 6.3 使用 __dunder__ 表示魔术方法
```python
class MyClass:
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f"MyClass({self.value})"
    
    def __repr__(self):
        return f"MyClass({self.value!r})"
```

## 7. 常见命名错误

### 7.1 使用数字后缀
**反模式**：
```python
data1 = 'Alice'
data2 = 'Bob'
data3 = 'Charlie'
```

**Pythonic**：
```python
user_names = ['Alice', 'Bob', 'Charlie']
# 或者
alice_name = 'Alice'
bob_name = 'Bob'
charlie_name = 'Charlie'
```

### 7.2 使用无意义的后缀
**反模式**：
```python
temp = calculate_result()
temp2 = process_data(temp)
result = final_step(temp2)
```

**Pythonic**：
```python
raw_result = calculate_result()
processed_result = process_data(raw_result)
final_result = final_step(processed_result)
```

### 7.3 使用误导性的名称
**反模式**：
```python
# 实际返回的是列表，不是单个用户
def get_user():
    return [user1, user2, user3]
```

**Pythonic**：
```python
def get_users():
    return [user1, user2, user3]
```

### 7.4 过度缩写
**反模式**：
```python
usr_nm = 'Alice'
usr_age = 25
usr_phn = '123456'
```

**Pythonic**：
```python
user_name = 'Alice'
user_age = 25
user_phone = '123456'
```

## 8. 命名最佳实践总结

### 8.1 命名检查清单
- [ ] 名称是否有意义？
- [ ] 名称是否准确描述用途？
- [ ] 是否遵循命名约定（snake_case、PascalCase、UPPER_CASE）？
- [ ] 布尔变量是否使用 is/has/can/should 前缀？
- [ ] 是否避免了类型前缀（匈牙利命名法）？
- [ ] 是否避免了不必要的中间变量？
- [ ] 循环变量是否有意义？
- [ ] 是否避免了数字后缀？
- [ ] 常量是否使用 UPPER_CASE？

### 8.2 命名示例对比

#### 示例 1：用户处理
```python
# 反模式
def proc(u):
    if u.act:
        return u.n
    return None

# Pythonic
def process_user(user):
    if user.is_active:
        return user.name
    return None
```

#### 示例 2：数据验证
```python
# 反模式
def chk(d):
    if d['nm'] and d['ag'] > 18:
        return True
    return False

# Pythonic
def validate_user_data(data):
    return bool(data['name']) and data['age'] > 18
```

#### 示例 3：配置管理
```python
# 反模式
CFG = {
    'url': 'http://example.com',
    'tm': 30
}

# Pythonic
CONFIG = {
    'base_url': 'http://example.com',
    'timeout': 30
}
```

## 9. 特殊命名场景

### 9.1 异常处理变量
```python
try:
    process_data()
except ValueError as e:  # e 是常见的异常变量命名
    logger.error(f"Processing failed: {e}")
except Exception as exc:  # 更明确的异常变量名
    logger.error(f"Unexpected error: {exc}")
```

### 9.2 Lambda 函数参数
```python
# 短 lambda 可以使用简单参数名
items.sort(key=lambda x: x.value)

# 复杂 lambda 使用描述性参数名
items.sort(key=lambda item: item.calculate_score())
```

### 9.3 生成器和迭代器
```python
def user_generator(users):
    """生成器函数."""
    for user in users:
        if user.is_active:
            yield user

def active_users(users):
    """返回活动用户的迭代器."""
    return (user for user in users if user.is_active)
```

## 示例

### 示例 1：完整的命名改进
```python
# 反模式
def proc(d):
    res = []
    for i in d['itms']:
        if i['prc'] > 0:
            res.append(i)
    return res

# Pythonic
def process_active_items(data):
    """处理活动项目."""
    active_items = []
    for item in data['items']:
        if item['price'] > 0:
            active_items.append(item)
    return active_items
```

### 示例 2：布尔命名优化
```python
# 反模式
if not user.inactive:
    process(user)

if not result.error:
    return result

# Pythonic
if user.is_active:
    process(user)

if result.is_success:
    return result
```

### 示例 3：循环变量优化
```python
# 反模式
for i in range(len(items)):
    for j in range(len(items[i])):
        print(items[i][j])

# Pythonic
for row_index, row in enumerate(items):
    for col_index, value in enumerate(row):
        print(f"Row {row_index}, Column {col_index}: {value}")
```
