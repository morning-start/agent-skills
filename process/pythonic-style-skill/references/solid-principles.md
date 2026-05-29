# SOLID Principles

## 目录
1. 单一职责原则 (SRP)
2. 开闭原则 (OCP)
3. 里氏替换原则 (LSP)
4. 接口隔离原则 (ISP)
5. 依赖倒置原则 (DIP)

## 概览
SOLID 原则是面向对象设计的五个基本原则，帮助开发者编写可维护、可扩展的代码。

## 1. 单一职责原则 (Single Responsibility Principle - SRP)

### 1.1 原则说明
一个类应该只有一个引起它变化的原因。

### 1.2 反模式
```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def save_to_database(self):
        # 保存到数据库的逻辑
        pass
    
    def send_email(self, subject, body):
        # 发送邮件的逻辑
        pass
    
    def validate_email(self):
        # 验证邮箱的逻辑
        pass
```

### 1.3 Pythonic 实现
```python
class User:
    """用户数据模型."""
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    """用户数据访问."""
    def save(self, user):
        # 保存到数据库
        pass

class EmailService:
    """邮件服务."""
    def send_email(self, to, subject, body):
        # 发送邮件
        pass

class EmailValidator:
    """邮箱验证器."""
    def is_valid(self, email):
        # 验证邮箱
        pass
```

### 1.4 函数级别的 SRP
```python
# 反模式
def process_user_data(user_data):
    # 验证
    if not user_data.get('name'):
        raise ValueError('Name is required')
    
    # 格式化
    formatted = {
        'name': user_data['name'].strip().title(),
        'email': user_data['email'].lower().strip()
    }
    
    # 保存
    database.insert(formatted)
    
    # 发送邮件
    email_service.send(formatted['email'], 'Welcome', 'Content')

# Pythonic
def validate_user_data(user_data):
    if not user_data.get('name'):
        raise ValueError('Name is required')

def format_user_data(user_data):
    return {
        'name': user_data['name'].strip().title(),
        'email': user_data['email'].lower().strip()
    }

def save_user(user_data):
    database.insert(user_data)

def send_welcome_email(user_data):
    email_service.send(user_data['email'], 'Welcome', 'Content')

def process_user_data(user_data):
    validate_user_data(user_data)
    formatted = format_user_data(user_data)
    save_user(formatted)
    send_welcome_email(formatted)
```

## 2. 开闭原则 (Open/Closed Principle - OCP)

### 2.1 原则说明
软件实体应该对扩展开放，对修改关闭。

### 2.2 反模式
```python
class PaymentProcessor:
    def process_payment(self, payment_type, amount):
        if payment_type == 'credit_card':
            # 信用卡处理逻辑
            pass
        elif payment_type == 'paypal':
            # PayPal 处理逻辑
            pass
        elif payment_type == 'bank_transfer':
            # 银行转账处理逻辑
            pass
        # 每次新增支付方式都需要修改这个类
```

### 2.3 Pythonic 实现
```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    """支付方式抽象类."""
    @abstractmethod
    def process(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def process(self, amount):
        # 信用卡处理逻辑
        pass

class PayPalPayment(PaymentMethod):
    def process(self, amount):
        # PayPal 处理逻辑
        pass

class BankTransferPayment(PaymentMethod):
    def process(self, amount):
        # 银行转账处理逻辑
        pass

class PaymentProcessor:
    def process_payment(self, payment_method: PaymentMethod, amount):
        payment_method.process(amount)

# 使用
processor = PaymentProcessor()
credit_card = CreditCardPayment()
processor.process_payment(credit_card, 100)
```

## 3. 里氏替换原则 (Liskov Substitution Principle - LSP)

### 3.1 原则说明
子类应该能够替换父类，而不会破坏程序的正确性。

### 3.2 反模式
```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def set_width(self, width):
        self.width = width
    
    def set_height(self, height):
        self.height = height
    
    def area(self):
        return self.width * self.height

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
    
    def set_width(self, width):
        self.width = width
        self.height = width  # 强制宽高相等
    
    def set_height(self, height):
        self.width = height  # 强制宽高相等
        self.height = height

# 问题：Square 不能正确替换 Rectangle
rect = Rectangle(2, 3)
rect.set_width(4)
print(rect.area())  # 12 (4 * 3)

square = Square(2)
square.set_width(4)
print(square.area())  # 16 (4 * 4)，破坏了预期的行为
```

### 3.3 Pythonic 实现
```python
class Shape:
    """形状基类."""
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def area(self):
        return self.side ** 2

# 正确的使用方式
shapes = [Rectangle(2, 3), Square(2)]
for shape in shapes:
    print(shape.area())
```

## 4. 接口隔离原则 (Interface Segregation Principle - ISP)

### 4.1 原则说明
客户端不应该依赖它不需要的接口。

### 4.2 反模式
```python
class Worker(ABC):
    @abstractmethod
    def work(self):
        pass
    
    @abstractmethod
    def eat(self):
        pass

class Human(Worker):
    def work(self):
        pass
    
    def eat(self):
        pass

class Robot(Worker):
    def work(self):
        pass
    
    def eat(self):
        # 机器人不需要吃饭，但必须实现这个方法
        raise NotImplementedError('Robots do not eat')
```

### 4.3 Pythonic 实现
```python
class Workable(ABC):
    """可工作的接口."""
    @abstractmethod
    def work(self):
        pass

class Eatable(ABC):
    """可进食的接口."""
    @abstractmethod
    def eat(self):
        pass

class Human(Workable, Eatable):
    def work(self):
        pass
    
    def eat(self):
        pass

class Robot(Workable):
    def work(self):
        pass

# 正确的使用方式
human = Human()
human.work()
human.eat()

robot = Robot()
robot.work()
# robot 不需要实现 eat 方法
```

## 5. 依赖倒置原则 (Dependency Inversion Principle - DIP)

### 5.1 原则说明
高层模块不应该依赖低层模块，两者都应该依赖抽象。抽象不应该依赖细节，细节应该依赖抽象。

### 5.2 反模式
```python
class Switch:
    def __init__(self):
        self.bulb = LightBulb()
    
    def turn_on(self):
        self.bulb.on()
    
    def turn_off(self):
        self.bulb.off()

class LightBulb:
    def on(self):
        print('Bulb is on')
    
    def off(self):
        print('Bulb is off')

# 问题：Switch 直接依赖具体的 LightBulb，难以扩展
```

### 5.3 Pythonic 实现
```python
from abc import ABC, abstractmethod

class Switchable(ABC):
    """可开关的设备抽象."""
    @abstractmethod
    def on(self):
        pass
    
    @abstractmethod
    def off(self):
        pass

class LightBulb(Switchable):
    def on(self):
        print('Bulb is on')
    
    def off(self):
        print('Bulb is off')

class Fan(Switchable):
    def on(self):
        print('Fan is on')
    
    def off(self):
        print('Fan is off')

class Switch:
    def __init__(self, device: Switchable):
        self.device = device
    
    def turn_on(self):
        self.device.on()
    
    def turn_off(self):
        self.device.off()

# 使用
bulb = LightBulb()
switch = Switch(bulb)
switch.turn_on()

fan = Fan()
switch = Switch(fan)
switch.turn_on()
```

## 示例

### 示例 1：订单处理系统
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

# SRP: 每个类只有一个职责
@dataclass
class Order:
    id: int
    items: List[str]
    total: float

class OrderRepository:
    """订单数据访问."""
    def save(self, order: Order):
        # 保存订单
        pass
    
    def find_by_id(self, order_id: int):
        # 查找订单
        pass

class PaymentService(ABC):
    """支付服务抽象."""
    @abstractmethod
    def process(self, amount: float):
        pass

class CreditCardPayment(PaymentService):
    def process(self, amount: float):
        # 信用卡支付逻辑
        pass

class PayPalPayment(PaymentService):
    def process(self, amount: float):
        # PayPal 支付逻辑
        pass

class EmailService:
    """邮件服务."""
    def send_confirmation(self, order: Order):
        # 发送确认邮件
        pass

class OrderProcessor:
    """订单处理器（依赖倒置）."""
    def __init__(
        self,
        repository: OrderRepository,
        payment_service: PaymentService,
        email_service: EmailService
    ):
        self.repository = repository
        self.payment_service = payment_service
        self.email_service = email_service
    
    def process_order(self, order: Order):
        # 处理订单
        self.repository.save(order)
        self.payment_service.process(order.total)
        self.email_service.send_confirmation(order)
```

### 示例 2：日志系统
```python
from abc import ABC, abstractmethod
from enum import Enum

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

class Logger(ABC):
    """日志器抽象."""
    @abstractmethod
    def log(self, level: LogLevel, message: str):
        pass

class FileLogger(Logger):
    def log(self, level: LogLevel, message: str):
        # 文件日志逻辑
        pass

class ConsoleLogger(Logger):
    def log(self, level: LogLevel, message: str):
        # 控制台日志逻辑
        pass

class DatabaseLogger(Logger):
    def log(self, level: LogLevel, message: str):
        # 数据库日志逻辑
        pass

class Application:
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def run(self):
        self.logger.log(LogLevel.INFO, 'Application started')
        # 应用逻辑
        self.logger.log(LogLevel.INFO, 'Application finished')

# 使用不同的日志器
app1 = Application(FileLogger())
app1.run()

app2 = Application(ConsoleLogger())
app2.run()
```

### 示例 3：数据验证器
```python
from abc import ABC, abstractmethod
from typing import List, Any

class Validator(ABC):
    """验证器抽象."""
    @abstractmethod
    def validate(self, value: Any) -> bool:
        pass

class EmailValidator(Validator):
    def validate(self, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        return '@' in value and '.' in value

class AgeValidator(Validator):
    def validate(self, value: Any) -> bool:
        if not isinstance(value, int):
            return False
        return 0 <= value <= 150

class NameValidator(Validator):
    def validate(self, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        return len(value) >= 2 and value.isalpha()

class ValidationService:
    """验证服务."""
    def __init__(self, validators: List[Validator]):
        self.validators = validators
    
    def validate_all(self, data: dict) -> dict:
        """验证所有数据."""
        results = {}
        for field, value in data.items():
            for validator in self.validators:
                field_name = validator.__class__.__name__.replace('Validator', '').lower()
                if field_name in field:
                    results[field] = validator.validate(value)
        return results

# 使用
validators = [
    EmailValidator(),
    AgeValidator(),
    NameValidator()
]

service = ValidationService(validators)
data = {
    'email': 'user@example.com',
    'age': 25,
    'name': 'Alice'
}

results = service.validate_all(data)
print(results)
```
