# Tips on Numbers and Strings

## 目录
1. 数字操作最佳实践
2. 字符串处理技巧
3. 格式化字符串
4. 正则表达式
5. 类型转换
6. 数值精度处理

## 概览
Python 提供了丰富的数字和字符串处理功能。正确使用这些功能可以让代码更简洁、更高效。本章基于《One Python Craftsman》第3章内容。

## 1. 数字操作最佳实践

### 1.1 使用 math 模块
**反模式**：
```python
import math

def calculate_circle(radius):
    pi = 3.14159265359
    return 2 * pi * radius
```

**Pythonic**：
```python
import math

def calculate_circle(radius):
    return 2 * math.pi * radius
```

### 1.2 使用 round() 函数
```python
# 四舍五入
round(3.14159, 2)  # 3.14
round(3.14159, 3)  # 3.142

# 处理浮点数精度
round(0.1 + 0.2, 1)  # 0.3
```

### 1.3 使用 Decimal 处理金融数据
**反模式**：
```python
# 浮点数精度问题
price = 0.1
total = price * 3  # 0.30000000000000004
```

**Pythonic**：
```python
from decimal import Decimal, getcontext

getcontext().prec = 6  # 设置精度

price = Decimal('0.1')
total = price * 3  # Decimal('0.3')
```

### 1.4 使用 fractions 处理分数
```python
from fractions import Fraction

# 创建分数
f1 = Fraction(1, 3)  # 1/3
f2 = Fraction(2, 6)  # 2/6 = 1/3

# 运算
result = f1 + f2  # 2/3
print(result)  # 2/3
print(float(result))  # 0.6666666666666666
```

### 1.5 使用 complex 处理复数
```python
# 创建复数
z = 3 + 4j

# 获取实部和虚部
print(z.real)  # 3.0
print(z.imag)  # 4.0

# 计算模
abs(z)  # 5.0

# 复数运算
z2 = 1 + 2j
print(z + z2)  # (4+6j)
```

## 2. 字符串处理技巧

### 2.1 使用 str.join() 连接字符串
**反模式**：
```python
result = ''
for item in items:
    result += item + ','
```

**Pythonic**：
```python
result = ','.join(items)
```

### 2.2 使用 f-string 格式化（Python 3.6+）
**反模式**：
```python
name = 'Alice'
age = 25
message = 'Hello, ' + name + '. You are ' + str(age) + ' years old.'
```

**Pythonic**：
```python
name = 'Alice'
age = 25
message = f'Hello, {name}. You are {age} years old.'
```

### 2.3 使用字符串方法
**反模式**：
```python
text = '  Hello World  '

# 去除空格
cleaned = text.strip()

# 检查开始/结束
starts_with_hello = cleaned.startswith('Hello')
ends_with_world = cleaned.endswith('World')

# 大小写转换
upper = cleaned.upper()
lower = cleaned.lower()
title = cleaned.title()
```

**Pythonic**：
```python
text = '  Hello World  '

# 链式调用
cleaned = text.strip().lower()

# 条件判断
if cleaned.startswith('hello'):
    print('Starts with hello')
```

### 2.4 使用 split() 分割字符串
```python
# 基本分割
text = 'hello,world,python'
parts = text.split(',')  # ['hello', 'world', 'python']

# 限制分割次数
text = 'hello,world,python,awesome'
parts = text.split(',', 2)  # ['hello', 'world', 'python,awesome']

# 按空白字符分割
text = 'hello world python'
words = text.split()  # ['hello', 'world', 'python']
```

### 2.5 使用 replace() 替换字符串
```python
text = 'hello world'
replaced = text.replace('world', 'python')  # 'hello python'

# 多次替换
text = 'aaa'
replaced = text.replace('a', 'b', 2)  # 'bba'（只替换前2个）
```

### 2.6 使用 find() 和 index()
```python
text = 'hello world'

# find(): 未找到返回 -1
pos = text.find('world')  # 6
pos = text.find('python')  # -1

# index(): 未找到抛出异常
try:
    pos = text.index('python')
except ValueError:
    print('Not found')
```

### 2.7 使用 count() 统计
```python
text = 'hello world hello'

# 统计子串出现次数
count = text.count('hello')  # 2

# 统计字符出现次数
count = text.count('l')  # 5
```

## 3. 格式化字符串

### 3.1 f-string 高级用法
```python
# 表达式计算
x = 10
y = 20
result = f'{x + y}'  # '30'

# 调用方法
name = 'alice'
formatted = f'{name.capitalize()}'  # 'Alice'

# 格式化数字
pi = 3.14159
formatted = f'{pi:.2f}'  # '3.14'

# 格式化百分比
ratio = 0.75
formatted = f'{ratio:.2%}'  # '75.00%'

# 对齐
name = 'Alice'
left = f'{name:<10}'  # 'Alice     '
center = f'{name:^10}'  # '  Alice   '
right = f'{name:>10}'  # '     Alice'
```

### 3.2 使用 format() 方法
```python
# 基本用法
name = 'Alice'
age = 25
message = 'Hello, {}. You are {} years old.'.format(name, age)

# 使用索引
message = 'Hello, {0}. You are {1} years old. {0}!'.format(name, age)

# 使用关键字
message = 'Hello, {name}. You are {age} years old.'.format(name=name, age=age)
```

### 3.3 格式化数字
```python
# 整数格式化
number = 1234567890
formatted = f'{number:,}'  # '1,234,567,890'

# 浮点数精度
pi = 3.14159
formatted = f'{pi:.2f}'  # '3.14'

# 百分比
ratio = 0.75
formatted = f'{ratio:.2%}'  # '75.00%'

# 科学计数法
large = 1234567890
formatted = f'{large:.2e}'  # '1.23e+09'

# 二进制、八进制、十六进制
number = 255
binary = f'{number:b}'  # '11111111'
octal = f'{number:o}'  # '377'
hexadecimal = f'{number:x}'  # 'ff'
```

## 4. 正则表达式

### 4.1 基本用法
```python
import re

# 匹配模式
pattern = r'\d+'
text = '123 abc 456'

# 查找所有匹配
matches = re.findall(pattern, text)  # ['123', '456']

# 查找第一个匹配
match = re.search(pattern, text)
if match:
    print(match.group())  # '123'

# 替换
result = re.sub(pattern, 'XXX', text)  # 'XXX abc XXX'
```

### 4.2 常用正则表达式
```python
import re

# 验证邮箱
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
email = 'user@example.com'
is_valid = re.match(email_pattern, email) is not None

# 验证手机号（简单示例）
phone_pattern = r'^\d{11}$'
phone = '13812345678'
is_valid = re.match(phone_pattern, phone) is not None

# 提取URL
url_pattern = r'https?://[^\s]+'
text = 'Visit https://example.com for more info'
urls = re.findall(url_pattern, text)

# 提取数字
number_pattern = r'\d+'
text = 'Price: $123.45, Quantity: 10'
numbers = re.findall(number_pattern, text)  # ['123', '45', '10']
```

### 4.3 预编译正则表达式
```python
import re

# 预编译（性能更好）
pattern = re.compile(r'\d+')

# 使用预编译的模式
matches = pattern.findall('123 abc 456')  # ['123', '456']
match = pattern.search('123 abc 456')
if match:
    print(match.group())  # '123'
```

### 4.4 正则表达式修饰符
```python
import re

# 忽略大小写
pattern = re.compile(r'python', re.IGNORECASE)
matches = pattern.findall('Python PYTHON python')  # ['Python', 'PYTHON', 'python']

# 多行模式
text = '''Line 1: hello
Line 2: world
Line 3: hello'''
matches = re.findall(r'^hello', text, re.MULTILINE)  # ['hello', 'hello']

# 点号匹配换行符
text = 'hello\nworld'
match = re.search(r'hello.*world', text, re.DOTALL)  # 匹配成功
```

## 5. 类型转换

### 5.1 字符串转数字
```python
# 转整数
int('123')  # 123
int('123.45')  # ValueError

# 转浮点数
float('123.45')  # 123.45
float('123')  # 123.0

# 安全转换
def safe_int(s, default=0):
    try:
        return int(s)
    except (ValueError, TypeError):
        return default

def safe_float(s, default=0.0):
    try:
        return float(s)
    except (ValueError, TypeError):
        return default
```

### 5.2 数字转字符串
```python
# 基本转换
str(123)  # '123'
str(123.45)  # '123.45'

# 格式化转换
format(123, '05d')  # '00123'
format(123.456, '.2f')  # '123.46'
```

### 5.3 布尔值转换
```python
# 转布尔
bool('')  # False
bool('hello')  # True
bool(0)  # False
bool(1)  # True
bool([])  # False
bool([1, 2])  # True

# 字符串转布尔（更宽松）
def str_to_bool(s):
    if isinstance(s, str):
        return s.lower() in ('true', '1', 'yes', 'on')
    return bool(s)
```

## 6. 数值精度处理

### 6.1 处理浮点数精度问题
```python
# 问题：浮点数精度
print(0.1 + 0.2)  # 0.30000000000000004

# 解决方案 1：使用 round()
print(round(0.1 + 0.2, 1))  # 0.3

# 解决方案 2：使用 Decimal
from decimal import Decimal
print(Decimal('0.1') + Decimal('0.2'))  # 0.3
```

### 6.2 比较浮点数
```python
import math

# 不精确比较
a = 0.1 + 0.2
b = 0.3
print(a == b)  # False

# 精确比较
def is_close(a, b, rel_tol=1e-9):
    return math.isclose(a, b, rel_tol=rel_tol)

print(is_close(a, b))  # True
```

### 6.3 金融计算使用 Decimal
```python
from decimal import Decimal, getcontext, ROUND_HALF_UP

# 设置精度
getcontext().prec = 4

# 金融计算
price = Decimal('10.99')
quantity = Decimal('3')
tax_rate = Decimal('0.08')

subtotal = price * quantity  # 32.97
tax = subtotal * tax_rate  # 2.6376
total = subtotal + tax  # 35.6076

# 四舍五入到分
total_rounded = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
print(total_rounded)  # 35.61
```

## 7. 字符串高级操作

### 7.1 使用 pathlib 处理路径
```python
from pathlib import Path

# 创建路径
path = Path('/home/user/documents/file.txt')

# 获取信息
print(path.name)  # 'file.txt'
print(path.stem)  # 'file'
print(path.suffix)  # '.txt'
print(path.parent)  # '/home/user/documents'

# 路径操作
new_path = path.with_name('new_file.txt')
print(new_path)  # '/home/user/documents/new_file.txt'

# 检查路径
print(path.exists())  # 检查是否存在
print(path.is_file())  # 是否是文件
print(path.is_dir())  # 是否是目录
```

### 7.2 使用 textwrap 格式化文本
```python
import textwrap

# 自动换行
text = "This is a long text that needs to be wrapped to fit within a certain width."
wrapped = textwrap.fill(text, width=40)
print(wrapped)

# 缩进
indented = textwrap.indent(text, prefix="  ")
print(indented)

# 去除缩进
dedented = textwrap.dedent(indented)
print(dedented)
```

### 7.3 使用 unicodedata 处理 Unicode
```python
import unicodedata

# 标准化 Unicode
text = 'café'
normalized = unicodedata.normalize('NFC', text)
print(normalized)

# 检查字符类型
char = '中'
print(unicodedata.category(char))  # 'Lo' (Letter, other)
print(unicodedata.name(char))  # 'CJK UNIFIED IDEOGRAPH-4E2D'
```

## 示例

### 示例 1：完整的字符串处理
```python
def process_user_input(input_text):
    """处理用户输入."""
    # 去除首尾空格
    cleaned = input_text.strip()
    
    # 检查是否为空
    if not cleaned:
        return None
    
    # 转为小写
    cleaned = cleaned.lower()
    
    # 去除多余空格
    cleaned = ' '.join(cleaned.split())
    
    # 首字母大写
    cleaned = cleaned.capitalize()
    
    return cleaned

# 使用
input_text = "  hello   world  "
result = process_user_input(input_text)
print(result)  # "Hello world"
```

### 示例 2：数字格式化
```python
def format_number(value, precision=2):
    """格式化数字."""
    if value is None:
        return 'N/A'
    
    # 整数
    if isinstance(value, int) or value.is_integer():
        return f'{int(value):,}'
    
    # 浮点数
    return f'{value:,.{precision}f}'

# 使用
print(format_number(1234567))  # "1,234,567"
print(format_number(1234567.89123))  # "1,234,567.89"
print(format_number(None))  # "N/A"
```

### 示例 3：价格计算（使用 Decimal）
```python
from decimal import Decimal, getcontext, ROUND_HALF_UP

def calculate_total_price(items, tax_rate=0.08):
    """计算总价（使用 Decimal 保证精度）."""
    getcontext().prec = 6
    tax_rate = Decimal(str(tax_rate))
    
    subtotal = Decimal('0')
    for item in items:
        price = Decimal(str(item['price']))
        quantity = Decimal(str(item['quantity']))
        subtotal += price * quantity
    
    tax = subtotal * tax_rate
    total = subtotal + tax
    
    # 四舍五入到分
    return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

# 使用
items = [
    {'price': 10.99, 'quantity': 2},
    {'price': 5.50, 'quantity': 3},
]
total = calculate_total_price(items)
print(total)  # Decimal('39.12')
```

### 示例 4：正则表达式验证
```python
import re

class Validator:
    """验证器."""
    
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PHONE_PATTERN = re.compile(r'^\d{11}$')
    URL_PATTERN = re.compile(r'^https?://[^\s]+$')
    
    @classmethod
    def is_valid_email(cls, email):
        """验证邮箱."""
        return bool(cls.EMAIL_PATTERN.match(email))
    
    @classmethod
    def is_valid_phone(cls, phone):
        """验证手机号."""
        return bool(cls.PHONE_PATTERN.match(phone))
    
    @classmethod
    def is_valid_url(cls, url):
        """验证 URL."""
        return bool(cls.URL_PATTERN.match(url))

# 使用
print(Validator.is_valid_email('user@example.com'))  # True
print(Validator.is_valid_phone('13812345678'))  # True
print(Validator.is_valid_url('https://example.com'))  # True
```

### 示例 5：文本搜索
```python
import re

def search_text(text, keywords, case_sensitive=False):
    """在文本中搜索关键词."""
    flags = 0 if case_sensitive else re.IGNORECASE
    
    # 构建正则表达式
    pattern = r'\b(?:' + '|'.join(map(re.escape, keywords)) + r')\b'
    compiled_pattern = re.compile(pattern, flags)
    
    # 查找所有匹配
    matches = compiled_pattern.findall(text)
    
    return matches

# 使用
text = "Python is awesome. I love python programming."
keywords = ['python', 'awesome']
matches = search_text(text, keywords)
print(matches)  # ['Python', 'awesome', 'python']
```
