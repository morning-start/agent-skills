"""
String and Number Operations Templates

Common Pythonic patterns for string and number operations.
"""

# Template 1: String Formatting with f-strings
name = 'Alice'
age = 25
message = f'Hello, {name}. You are {age} years old.'

# Template 2: String Methods
def normalize_string(text):
    """规范化字符串."""
    return text.strip().lower()

def capitalize_words(text):
    """首字母大写."""
    return text.title()

# Template 3: String Joining
words = ['Hello', 'World', 'Python']
sentence = ' '.join(words)

# Template 4: String Splitting
text = 'apple,banana,cherry'
items = text.split(',')

# Template 5: String Replacement
text = 'Hello World'
new_text = text.replace('World', 'Python')

# Template 6: String Checking
def is_valid_email(email):
    """检查邮箱格式."""
    return '@' in email and '.' in email

# Template 7: String Padding
def pad_string(text, length=10, char=' '):
    """填充字符串."""
    return text.ljust(length, char)

# Template 8: Number Formatting
def format_price(price):
    """格式化价格."""
    return f'${price:.2f}'

def format_percentage(value):
    """格式化百分比."""
    return f'{value:.2%}'

# Template 9: Number Operations
def calculate_average(numbers):
    """计算平均值."""
    return sum(numbers) / len(numbers) if numbers else 0

def calculate_median(numbers):
    """计算中位数."""
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    if n == 0:
        return 0
    if n % 2 == 0:
        return (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
    return sorted_numbers[n//2]

# Template 10: Rounding
def round_number(value, precision=2):
    """四舍五入."""
    return round(value, precision)

# Template 11: Number Validation
def is_valid_age(age):
    """验证年龄."""
    return isinstance(age, int) and 0 <= age <= 150

def is_valid_percentage(value):
    """验证百分比."""
    return isinstance(value, (int, float)) and 0 <= value <= 100

# Template 12: Decimal Operations
from decimal import Decimal, getcontext

def calculate_price_tax(price, tax_rate):
    """精确计算价格和税."""
    getcontext().prec = 4
    price = Decimal(str(price))
    tax_rate = Decimal(str(tax_rate))
    return price * (1 + tax_rate)

# Template 13: Fraction Operations
from fractions import Fraction

def add_fractions(a, b):
    """分数相加."""
    return Fraction(a) + Fraction(b)

# Template 14: String to Number Conversion
def safe_int_conversion(value, default=0):
    """安全的整数转换."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float_conversion(value, default=0.0):
    """安全的浮点数转换."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

# Template 15: Number to String Conversion
def format_number_with_commas(number):
    """格式化数字（千位分隔符）."""
    return f'{number:,}'

def format_bytes(size):
    """格式化字节数."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f'{size:.2f} {unit}'
        size /= 1024.0
    return f'{size:.2f} PB'

# Template 16: String Cleaning
def clean_string(text):
    """清理字符串."""
    # 移除多余空白
    text = ' '.join(text.split())
    # 移除特殊字符
    import re
    text = re.sub(r'[^\w\s-]', '', text)
    return text

# Template 17: String Truncation
def truncate_string(text, max_length=50, suffix='...'):
    """截断字符串."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

# Template 18: Number Ranges
def is_in_range(value, min_val, max_val):
    """检查数字是否在范围内."""
    return min_val <= value <= max_val

def clamp(value, min_val, max_val):
    """限制数值范围."""
    return max(min_val, min(value, max_val))

# Template 19: String Validation
def is_valid_string(text, min_length=1, max_length=100):
    """验证字符串."""
    if not isinstance(text, str):
        return False
    if not text.strip():
        return False
    return min_length <= len(text) <= max_length

# Template 20: Math Operations
import math

def calculate_circle_area(radius):
    """计算圆面积."""
    return math.pi * radius ** 2

def calculate_distance(x1, y1, x2, y2):
    """计算两点距离."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Template 21: String Comparison
def are_strings_equal_case_insensitive(str1, str2):
    """不区分大小写比较字符串."""
    return str1.lower() == str2.lower()

def contains_substring_case_insensitive(text, substring):
    """不区分大小写检查子字符串."""
    return substring.lower() in text.lower()

# Template 22: Number Statistics
def calculate_statistics(numbers):
    """计算统计信息."""
    if not numbers:
        return {}
    
    return {
        'count': len(numbers),
        'sum': sum(numbers),
        'mean': sum(numbers) / len(numbers),
        'min': min(numbers),
        'max': max(numbers),
        'median': calculate_median(numbers)
    }

# Template 23: String Encoding/Decoding
def encode_base64(text):
    """Base64 编码."""
    import base64
    return base64.b64encode(text.encode()).decode()

def decode_base64(encoded_text):
    """Base64 解码."""
    import base64
    return base64.b64decode(encoded_text.encode()).decode()

# Template 24: Number Formatting for Display
def format_duration(seconds):
    """格式化持续时间."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f'{hours}h {minutes}m {secs}s'
    elif minutes > 0:
        return f'{minutes}m {secs}s'
    else:
        return f'{secs}s'

# Template 25: String Tokenization
def tokenize_text(text):
    """文本分词."""
    import re
    return re.findall(r'\w+', text.lower())

# Template 26: Percentage Calculation
def calculate_percentage(value, total):
    """计算百分比."""
    if total == 0:
        return 0
    return (value / total) * 100

# Template 27: String Masking
def mask_email(email):
    """掩码邮箱."""
    if '@' not in email:
        return email
    
    local, domain = email.split('@', 1)
    if len(local) > 2:
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
    else:
        masked_local = local
    
    return f'{masked_local}@{domain}'

def mask_phone_number(phone):
    """掩码电话号码."""
    if len(phone) > 4:
        return phone[:-4] + '*' * 4
    return phone

# Template 28: Number Conversion
def celsius_to_fahrenheit(celsius):
    """摄氏度转华氏度."""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """华氏度转摄氏度."""
    return (fahrenheit - 32) * 5/9

# Template 29: String Parsing
def parse_config_line(line):
    """解析配置行."""
    if '=' not in line:
        return None
    
    key, value = line.split('=', 1)
    return {
        'key': key.strip(),
        'value': value.strip()
    }

# Template 30: Advanced Number Operations
def calculate_compound_interest(principal, rate, time):
    """计算复利."""
    return principal * (1 + rate) ** time

def calculate_simple_interest(principal, rate, time):
    """计算单利."""
    return principal * rate * time
