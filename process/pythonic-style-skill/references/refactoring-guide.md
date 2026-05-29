# Refactoring Guide

## 目录
1. 重构原则
2. 代码异味检测
3. 重构技巧
4. 重构模式
5. 重构流程
6. 重构工具
7. 重构实践
8. 重构示例

## 概览
本章介绍代码重构的原则、技巧和实践，帮助开发者改进代码质量、可读性和可维护性。

## 1. 重构原则

### 1.1 小步重构
```python
# 重构前
def process(data):
    result = []
    for item in data:
        if item:
            result.append(item.upper())
    return result

# 第一步：提取变量
def process(data):
    result = []
    for item in data:
        if is_valid(item):
            result.append(transform(item))
    return result

def is_valid(item):
    return bool(item)

def transform(item):
    return item.upper()
```

### 1.2 保持测试通过
```python
# 重构前必须确保测试覆盖
def test_process():
    data = ['a', 'b', 'c']
    result = process(data)
    assert result == ['A', 'B', 'C']

# 重构后再运行测试
def process(data):
    return [item.upper() for item in data if item]

test_process()  # 确保仍然通过
```

### 1.3 一次只做一件事
```python
# 重构前：做太多事情
def complex_function(data):
    # 验证
    if not data:
        return []
    
    # 转换
    result = []
    for item in data:
        if item:
            result.append(item.upper())
    
    # 排序
    return sorted(result)

# 重构后：每个函数做一件事
def validate_data(data):
    if not data:
        raise ValueError('Data cannot be empty')
    return data

def transform_items(items):
    return [item.upper() for item in items if item]

def sort_items(items):
    return sorted(items)

def complex_function(data):
    validated = validate_data(data)
    transformed = transform_items(validated)
    return sort_items(transformed)
```

## 2. 代码异味检测

### 2.1 长方法
```python
# 代码异味：长方法
def process_user_order(user_id, order_id):
    # 50+ 行代码...
    pass

# 重构：分解为小方法
def process_user_order(user_id, order_id):
    user = get_user(user_id)
    order = get_order(order_id)
    validate_user_order(user, order)
    calculate_total(order)
    send_confirmation(user, order)
    return order
```

### 2.2 重复代码
```python
# 代码异味：重复代码
def process_users(users):
    results = []
    for user in users:
        if user.is_active:
            results.append(user.name.upper())
    return results

def process_admins(admins):
    results = []
    for admin in admins:
        if admin.is_active:
            results.append(admin.name.upper())
    return results

# 重构：提取通用方法
def process_active_people(people):
    return [person.name.upper() for person in people if person.is_active]
```

### 2.3 过长参数列表
```python
# 代码异味：过长参数列表
def create_user(name, email, age, city, country, phone, address):
    pass

# 重构：使用数据类
from dataclasses import dataclass

@dataclass
class UserData:
    name: str
    email: str
    age: int
    city: str
    country: str
    phone: str
    address: str

def create_user(user_data: UserData):
    pass
```

### 2.4 全局变量
```python
# 代码异味：全局变量
current_user = None

def set_user(user):
    global current_user
    current_user = user

def get_user():
    return current_user

# 重构：使用类或依赖注入
class UserContext:
    def __init__(self):
        self.current_user = None
    
    def set_user(self, user):
        self.current_user = user
    
    def get_user(self):
        return self.current_user
```

## 3. 重构技巧

### 3.1 提取方法
```python
# 重构前
def calculate_total(items):
    total = 0
    for item in items:
        price = item.price
        quantity = item.quantity
        discount = item.discount
        subtotal = price * quantity * (1 - discount)
        total += subtotal
    return total

# 重构后
def calculate_total(items):
    return sum(calculate_item_total(item) for item in items)

def calculate_item_total(item):
    price = item.price
    quantity = item.quantity
    discount = item.discount
    return price * quantity * (1 - discount)
```

### 3.2 内联方法
```python
# 重构前
def get_price(item):
    return item.price

def process_item(item):
    price = get_price(item)
    return price * 2

# 重构后
def process_item(item):
    return item.price * 2
```

### 3.3 提取变量
```python
# 重构前
def calculate_discount(price, tax_rate, discount_rate):
    return price * (1 - discount_rate) * (1 + tax_rate)

# 重构后
def calculate_discount(price, tax_rate, discount_rate):
    discounted_price = price * (1 - discount_rate)
    final_price = discounted_price * (1 + tax_rate)
    return final_price
```

### 3.4 替换魔法数字
```python
# 重构前
def check_age(age):
    if age < 18:
        return 'minor'
    elif age < 65:
        return 'adult'
    else:
        return 'senior'

# 重构后
MIN_ADULT_AGE = 18
SENIOR_AGE = 65

def check_age(age):
    if age < MIN_ADULT_AGE:
        return 'minor'
    elif age < SENIOR_AGE:
        return 'adult'
    else:
        return 'senior'
```

## 4. 重构模式

### 4.1 提取类
```python
# 重构前
class Order:
    def __init__(self, customer_name, customer_email, customer_address):
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_address = customer_address
        self.items = []
    
    def send_email(self, subject, body):
        # 发送邮件逻辑
        pass

# 重构后
class Customer:
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address

class Order:
    def __init__(self, customer):
        self.customer = customer
        self.items = []
```

### 4.2 提取接口
```python
# 重构前
class FileStorage:
    def save(self, data):
        with open('data.txt', 'w') as f:
            f.write(data)

class DatabaseStorage:
    def save(self, data):
        # 保存到数据库
        pass

# 重构后
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save(self, data):
        pass

class FileStorage(Storage):
    def save(self, data):
        with open('data.txt', 'w') as f:
            f.write(data)

class DatabaseStorage(Storage):
    def save(self, data):
        # 保存到数据库
        pass
```

### 4.3 组合方法
```python
# 重构前
def validate_user(user):
    if not user.name:
        return False
    if not user.email:
        return False
    if not user.age:
        return False
    if user.age < 18:
        return False
    return True

# 重构后
def validate_user(user):
    return all([
        has_name(user),
        has_email(user),
        has_age(user),
        is_adult(user)
    ])

def has_name(user):
    return bool(user.name)

def has_email(user):
    return bool(user.email)

def has_age(user):
    return bool(user.age)

def is_adult(user):
    return user.age >= 18 if user.age else False
```

### 4.4 参数对象
```python
# 重构前
def create_report(title, author, date, content, format):
    pass

# 重构后
from dataclasses import dataclass

@dataclass
class ReportSpec:
    title: str
    author: str
    date: str
    content: str
    format: str

def create_report(spec: ReportSpec):
    pass
```

## 5. 重构流程

### 5.1 识别代码异味
```python
# 使用工具检测
# pylint: 检测代码异味
# flake8: 检测代码风格问题
# mypy: 类型检查

# 运行工具
# pylint your_code.py
# flake8 your_code.py
# mypy your_code.py
```

### 5.2 编写测试
```python
import unittest

class TestOrderProcessing(unittest.TestCase):
    def test_calculate_total(self):
        order = create_test_order()
        total = calculate_total(order)
        self.assertEqual(total, 100.0)
    
    def test_process_empty_order(self):
        order = Order()
        result = process_order(order)
        self.assertEqual(result.total, 0)
```

### 5.3 小步重构
```python
# 第一步：提取变量
def calculate_total(order):
    subtotal = calculate_subtotal(order)
    tax = calculate_tax(subtotal, order.tax_rate)
    return subtotal + tax

# 第二步：提取方法
def calculate_total(order):
    return add_tax(calculate_subtotal(order), order.tax_rate)

# 第三步：简化逻辑
def calculate_total(order):
    return calculate_subtotal(order) * (1 + order.tax_rate)
```

### 5.4 验证重构
```python
# 运行测试
python -m pytest tests/

# 运行代码检查
pylint refactored_code.py
flake8 refactored_code.py

# 性能测试
python -m cProfile -s time refactored_code.py
```

## 6. 重构工具

### 6.1 使用 IDE 重构功能
```python
# PyCharm / VS Code:
# - 重命名变量/函数/类
# - 提取方法
# - 内联方法
# - 移动代码
# - 提取变量
```

### 6.2 使用命令行工具
```python
# autopep8: 自动格式化代码
# autopep8 --in-place --aggressive your_code.py

# black: 代码格式化
# black your_code.py

# isort: 排序导入
# isort your_code.py
```

### 6.3 使用静态分析工具
```python
# pylint: 代码分析
# pylint your_code.py

# mypy: 类型检查
# mypy your_code.py

# bandit: 安全检查
# bandit -r your_project/
```

## 7. 重构实践

### 7.1 重命名
```python
# 重构前
def calc(x, y):
    return x + y

# 重构后
def calculate_sum(first_number, second_number):
    return first_number + second_number
```

### 7.2 移动代码
```python
# 重构前
class Order:
    def process(self):
        # 验证逻辑
        if not self.items:
            raise ValueError('No items')
        
        # 计算逻辑
        total = sum(item.price for item in self.items)
        
        # 保存逻辑
        self.save_to_db()

# 重构后
class OrderValidator:
    @staticmethod
    def validate(order):
        if not order.items:
            raise ValueError('No items')

class OrderCalculator:
    @staticmethod
    def calculate_total(order):
        return sum(item.price for item in order.items)

class OrderRepository:
    @staticmethod
    def save(order):
        order.save_to_db()

class Order:
    def process(self):
        OrderValidator.validate(self)
        self.total = OrderCalculator.calculate_total(self)
        OrderRepository.save(self)
```

### 7.3 简化条件
```python
# 重构前
def get_status(user):
    if user is not None:
        if user.is_active:
            if user.has_permission:
                return 'active'
            else:
                return 'no_permission'
        else:
            return 'inactive'
    else:
        return 'not_found'

# 重构后
def get_status(user):
    if user is None:
        return 'not_found'
    
    if not user.is_active:
        return 'inactive'
    
    if not user.has_permission:
        return 'no_permission'
    
    return 'active'
```

## 8. 重构示例

### 示例 1：重构长方法
```python
# 重构前
def process_order(order):
    if not order:
        return {'status': 'error', 'message': 'No order'}
    
    if not order.items:
        return {'status': 'error', 'message': 'No items'}
    
    total = 0
    for item in order.items:
        if not item.price:
            return {'status': 'error', 'message': 'Invalid price'}
        total += item.price * item.quantity
    
    if order.discount:
        total *= (1 - order.discount)
    
    if order.tax:
        total *= (1 + order.tax)
    
    # 保存到数据库
    db.save(order)
    
    # 发送邮件
    send_email(order.user.email, f'Order processed: {total}')
    
    return {'status': 'success', 'total': total}

# 重构后
def process_order(order):
    validate_order(order)
    total = calculate_order_total(order)
    save_order(order)
    notify_user(order, total)
    return {'status': 'success', 'total': total}

def validate_order(order):
    if not order:
        raise ValueError('No order')
    if not order.items:
        raise ValueError('No items')

def calculate_order_total(order):
    total = sum(item.price * item.quantity for item in order.items)
    total = apply_discount(total, order.discount)
    total = apply_tax(total, order.tax)
    return total

def save_order(order):
    db.save(order)

def notify_user(order, total):
    send_email(order.user.email, f'Order processed: {total}')
```

### 示例 2：重构重复代码
```python
# 重构前
def process_csv(filename):
    with open(filename) as f:
        lines = f.readlines()
    
    data = []
    for line in lines:
        if line.strip():
            parts = line.split(',')
            data.append({
                'name': parts[0],
                'age': int(parts[1])
            })
    
    return data

def process_txt(filename):
    with open(filename) as f:
        lines = f.readlines()
    
    data = []
    for line in lines:
        if line.strip():
            parts = line.split('|')
            data.append({
                'name': parts[0],
                'age': int(parts[1])
            })
    
    return data

# 重构后
def process_file(filename, delimiter):
    """处理文件."""
    lines = read_lines(filename)
    return parse_lines(lines, delimiter)

def read_lines(filename):
    """读取文件行."""
    with open(filename) as f:
        return f.readlines()

def parse_lines(lines, delimiter):
    """解析行."""
    data = []
    for line in lines:
        if line.strip():
            data.append(parse_line(line, delimiter))
    return data

def parse_line(line, delimiter):
    """解析单行."""
    parts = line.split(delimiter)
    return {
        'name': parts[0],
        'age': int(parts[1])
    }
```

### 示例 3：重构条件表达式
```python
# 重构前
def calculate_grade(score):
    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    elif score >= 60:
        grade = 'D'
    else:
        grade = 'F'
    
    if score >= 60:
        passed = True
    else:
        passed = False
    
    if score >= 90:
        honors = True
    else:
        honors = False
    
    return {
        'grade': grade,
        'passed': passed,
        'honors': honors
    }

# 重构后
def calculate_grade(score):
    return {
        'grade': get_letter_grade(score),
        'passed': is_passing(score),
        'honors': is_honors(score)
    }

def get_letter_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    return 'F'

def is_passing(score):
    return score >= 60

def is_honors(score):
    return score >= 90
```
