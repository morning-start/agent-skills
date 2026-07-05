# Cyclic Imports

## 目录
1. 循环导入的定义
2. 循环导入的原因
3. 循环导入的后果
4. 解决循环导入的方法
5. 最佳实践

## 概览
循环导入是 Python 开发中常见的问题，会导致模块无法正常加载。了解循环导入的原因和解决方法对于编写可维护的代码至关重要。本章基于《One Python Craftsman》第9章内容。

## 1. 循环导入的定义

### 1.1 什么是循环导入
循环导入是指两个或多个模块相互导入，形成循环依赖关系。

```python
# module_a.py
import module_b

def func_a():
    module_b.func_b()

# module_b.py
import module_a

def func_b():
    module_a.func_a()
```

### 1.2 循环导入的类型
- **直接循环**：A → B → A
- **间接循环**：A → B → C → A
- **多重循环**：A → B, A → C, B → C

## 2. 循环导入的原因

### 2.1 模块职责不清
**反模式**：
```python
# user.py
from order import Order

class User:
    def __init__(self, name):
        self.name = name
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

# order.py
from user import User

class Order:
    def __init__(self, total):
        self.total = total
        self.user = None

    def set_user(self, user):
        self.user = user
```

**问题分析**：
- `user.py` 导入 `order.py`
- `order.py` 导入 `user.py`
- 形成循环依赖

### 2.2 过度耦合
模块之间耦合度过高，彼此相互依赖。

## 3. 循环导入的后果

### 3.1 ImportError
```python
>>> import module_a
ImportError: cannot import name 'func_b' from partially initialized module 'module_b'
(most likely due to a circular import) (/path/to/module_b.py)
```

### 3.2 AttributeError
```python
>>> import module_a
AttributeError: module 'module_b' has no attribute 'func_b'
```

### 3.3 模块无法正常初始化
循环导入会导致模块处于部分初始化状态，无法访问模块中的所有属性。

## 4. 解决循环导入的方法

### 4.1 方法 1：延迟导入（在函数内部导入）

**反模式**：
```python
# module_a.py
import module_b

def func_a():
    module_b.func_b()

# module_b.py
import module_a

def func_b():
    module_a.func_a()
```

**Pythonic（在函数内部导入）**：
```python
# module_a.py

def func_a():
    import module_b  # 延迟导入
    module_b.func_b()

# module_b.py

def func_b():
    import module_a  # 延迟导入
    module_a.func_a()
```

**优点**：
- 简单直接
- 不需要重构代码

**缺点**：
- 每次调用函数都会重新导入
- 性能略差
- 可能导致代码难以维护

### 4.2 方法 2：重构为单向依赖

**反模式**（双向依赖）：
```python
# user.py
from order import Order

class User:
    def __init__(self, name):
        self.name = name
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

# order.py
from user import User

class Order:
    def __init__(self, total):
        self.total = total
        self.user = None

    def set_user(self, user):
        self.user = user
```

**Pythonic（单向依赖 - Order 依赖 User）**：
```python
# user.py
class User:
    def __init__(self, name):
        self.name = name
        self.orders = []

    def add_order(self, order):
        """添加订单（Order 对象传入即可）."""
        self.orders.append(order)

# order.py
from user import User

class Order:
    def __init__(self, total, user=None):
        self.total = total
        self.user = user

    def set_user(self, user):
        """设置用户."""
        self.user = user

# 使用
user = User('Alice')
order = Order(100.0, user)
# 或者
user.add_order(order)
```

### 4.3 方法 3：提取公共模块

**反模式**：
```python
# user.py
from order import Order

class User:
    def __init__(self, name):
        self.name = name

# order.py
from user import User

class Order:
    def __init__(self, total):
        self.total = total
```

**Pythonic（提取公共模块）**：
```python
# models/base.py
class BaseModel:
    """基础模型."""
    pass

# models/user.py
from models.base import BaseModel

class User(BaseModel):
    def __init__(self, name):
        self.name = name

# models/order.py
from models.base import BaseModel

class Order(BaseModel):
    def __init__(self, total):
        self.total = total
```

### 4.4 方法 4：使用依赖注入

**反模式**：
```python
# user.py
from order import Order

class User:
    def create_order(self, total):
        return Order(total, self)

# order.py
from user import User

class Order:
    def __init__(self, total, user):
        self.total = total
        self.user = user
```

**Pythonic（依赖注入）**：
```python
# user.py

class User:
    def __init__(self, name, order_factory=None):
        self.name = name
        self.order_factory = order_factory

    def create_order(self, total):
        """创建订单."""
        if self.order_factory:
            return self.order_factory(total, self)
        raise ValueError("Order factory not provided")

# order.py

class Order:
    def __init__(self, total, user):
        self.total = total
        self.user = user

# 使用
def create_order_factory():
    def factory(total, user):
        return Order(total, user)
    return factory

user = User('Alice', create_order_factory())
order = user.create_order(100.0)
```

### 4.5 方法 5：使用类型注解的字符串形式（Python 3.7+）

**反模式**：
```python
# user.py
from order import Order

class User:
    def __init__(self, name):
        self.name = name
        self.orders: list[Order] = []

# order.py
from user import User

class Order:
    def __init__(self, total, user: User):
        self.total = total
        self.user = user
```

**Pythonic（使用 TYPE_CHECKING）**：
```python
# user.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from order import Order

class User:
    def __init__(self, name):
        self.name = name
        self.orders: list['Order'] = []  # 使用字符串形式

# order.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from user import User

class Order:
    def __init__(self, total, user: 'User'):
        self.total = total
        self.user = user
```

**说明**：
- `TYPE_CHECKING` 只在类型检查时为 `True`
- 运行时不会导入，避免循环导入
- 类型提示仍然有效

## 5. 最佳实践

### 5.1 避免在模块顶层相互导入

**反模式**：
```python
# module_a.py
import module_b

class A:
    pass

# module_b.py
import module_a

class B:
    pass
```

**Pythonic**：
```python
# module_a.py

class A:
    pass

# module_b.py

class B:
    pass

# 如果需要使用 A，在函数内部导入
def func():
    import module_a
    return module_a.A()
```

### 5.2 明确模块职责

**反模式**：
```python
# models.py（包含所有模型）

class User:
    def __init__(self, name):
        self.orders = []

class Order:
    def __init__(self, total):
        self.user = None
```

**Pythonic（分离模型）**：
```python
# models/user.py

class User:
    def __init__(self, name):
        self.orders = []

# models/order.py

class Order:
    def __init__(self, total):
        self.user = None
```

### 5.3 使用工厂模式

**Pythonic**：
```python
# factories.py

class OrderFactory:
    """订单工厂."""
    
    def __init__(self):
        self._user_class = None
    
    def set_user_class(self, user_class):
        """设置用户类."""
        self._user_class = user_class
    
    def create_order(self, total, user):
        """创建订单."""
        from models.order import Order
        return Order(total, user)

# 使用
factory = OrderFactory()
factory.set_user_class(User)
order = factory.create_order(100.0, user)
```

### 5.4 使用事件系统

**Pythonic**：
```python
# events.py

class EventBus:
    """事件总线."""
    
    def __init__(self):
        self._handlers = {}
    
    def on(self, event, handler):
        """注册事件处理器."""
        if event not in self._handlers:
            self._handlers[event] = []
        self._handlers[event].append(handler)
    
    def emit(self, event, *args, **kwargs):
        """触发事件."""
        if event in self._handlers:
            for handler in self._handlers[event]:
                handler(*args, **kwargs)

# 使用
event_bus = EventBus()

# user.py
def handle_user_created(user):
    from order import Order
    Order.create_for_user(user)

event_bus.on('user_created', handle_user_created)

# order.py
class Order:
    @staticmethod
    def create_for_user(user):
        """为用户创建订单."""
        return Order(0.0, user)
```

## 6. 常见场景和解决方案

### 6.1 场景 1：模型关联

**反模式**：
```python
# models/user.py
from models.order import Order

class User:
    def __init__(self, name):
        self.name = name
        self.orders: list[Order] = []

# models/order.py
from models.user import User

class Order:
    def __init__(self, total, user: User):
        self.total = total
        self.user = user
```

**Pythonic（使用延迟导入和类型注解）**：
```python
# models/user.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.order import Order

class User:
    def __init__(self, name):
        self.name = name
        self.orders: list['Order'] = []
    
    def add_order(self, order: 'Order'):
        """添加订单."""
        self.orders.append(order)

# models/order.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User

class Order:
    def __init__(self, total, user: 'User'):
        self.total = total
        self.user = user
```

### 6.2 场景 2：服务层相互调用

**反模式**：
```python
# services/user_service.py
from services.order_service import OrderService

class UserService:
    def __init__(self):
        self.order_service = OrderService()

# services/order_service.py
from services.user_service import UserService

class OrderService:
    def __init__(self):
        self.user_service = UserService()
```

**Pythonic（依赖注入）**：
```python
# services/user_service.py

class UserService:
    def __init__(self, order_service=None):
        self.order_service = order_service

# services/order_service.py

class OrderService:
    def __init__(self, user_service=None):
        self.user_service = user_service

# 使用
order_service = OrderService()
user_service = UserService(order_service)
order_service.user_service = user_service
```

### 6.3 场景 3：配置相互引用

**反模式**：
```python
# config/dev.py
from config.common import DATABASE

DATABASE = {
    **DATABASE,
    'name': 'dev_db'
}

# config/common.py
from config.dev import DATABASE

DATABASE = {
    'host': 'localhost',
    'port': 5432
}
```

**Pythonic（配置继承）**：
```python
# config/base.py

BASE_CONFIG = {
    'host': 'localhost',
    'port': 5432
}

# config/dev.py

from config.base import BASE_CONFIG

DATABASE = {
    **BASE_CONFIG,
    'name': 'dev_db'
}
```

## 7. 检测循环导入

### 7.1 使用工具检测

```bash
# 使用 pylint
pylint your_project/

# 使用 pyflakes
pyflakes your_project/

# 使用 importchecker
pip install importchecker
importchecker your_project/
```

### 7.2 手动检测

```python
# test_circular_imports.py
import sys

def test_imports():
    """测试所有模块是否能正常导入."""
    modules_to_test = [
        'models.user',
        'models.order',
        'services.user_service',
        'services.order_service',
    ]
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f'{module_name}: OK')
        except ImportError as e:
            print(f'{module_name}: FAILED - {e}')

if __name__ == '__main__':
    test_imports()
```

## 8. 总结

### 8.1 避免循环导入的原则
1. **明确模块职责**：每个模块应该有清晰的职责
2. **单向依赖**：尽量保持依赖关系的单向性
3. **延迟导入**：在函数内部导入，而非模块顶层
4. **依赖注入**：使用依赖注入降低耦合
5. **类型注解**：使用字符串形式的类型注解和 TYPE_CHECKING

### 8.2 选择解决方案的决策树
- 是否可以重构为单向依赖？ → 是 → 重构
- 是否可以使用依赖注入？ → 是 → 使用依赖注入
- 是否只需要类型注解？ → 是 → 使用 TYPE_CHECKING
- 是否需要立即修复？ → 是 → 使用延迟导入

## 示例

### 示例 1：完整的电商系统（避免循环导入）

```python
# models/base.py
class BaseModel:
    """基础模型."""
    pass

# models/user.py
from typing import TYPE_CHECKING, List
from models.base import BaseModel

if TYPE_CHECKING:
    from models.order import Order

class User(BaseModel):
    def __init__(self, name: str):
        self.name = name
        self.orders: List['Order'] = []
    
    def add_order(self, order: 'Order') -> None:
        """添加订单."""
        self.orders.append(order)
    
    def get_total_spent(self) -> float:
        """获取总消费."""
        return sum(order.total for order in self.orders)

# models/order.py
from typing import TYPE_CHECKING
from models.base import BaseModel

if TYPE_CHECKING:
    from models.user import User

class Order(BaseModel):
    def __init__(self, total: float, user: 'User' = None):
        self.total = total
        self.user = user
        if user:
            user.add_order(self)
    
    def set_user(self, user: 'User') -> None:
        """设置用户."""
        self.user = user
        user.add_order(self)

# 使用
from models.user import User
from models.order import Order

user = User('Alice')
order1 = Order(100.0, user)
order2 = Order(200.0, user)

print(f'Total spent: {user.get_total_spent()}')  # 300.0
```

### 示例 2：服务层依赖注入

```python
# services/base.py
class BaseService:
    """基础服务."""
    pass

# services/user_service.py
from typing import TYPE_CHECKING, Optional
from services.base import BaseService

if TYPE_CHECKING:
    from services.order_service import OrderService

class UserService(BaseService):
    def __init__(self, order_service: Optional['OrderService'] = None):
        self.order_service = order_service
    
    def create_user_with_order(self, name: str, total: float):
        """创建用户并创建订单."""
        user = User(name)
        if self.order_service:
            order = self.order_service.create_order(total, user)
        return user, order

# services/order_service.py
from typing import TYPE_CHECKING, Optional
from services.base import BaseService

if TYPE_CHECKING:
    from services.user_service import UserService

class OrderService(BaseService):
    def __init__(self, user_service: Optional['UserService'] = None):
        self.user_service = user_service
    
    def create_order(self, total: float, user):
        """创建订单."""
        return Order(total, user)

# 使用
from services.user_service import UserService
from services.order_service import OrderService

# 创建服务实例
order_service = OrderService()
user_service = UserService(order_service)
order_service.user_service = user_service

# 使用服务
user, order = user_service.create_user_with_order('Alice', 100.0)
```

### 示例 3：配置管理

```python
# config/base.py

class BaseConfig:
    """基础配置."""
    DEBUG = False
    TESTING = False
    DATABASE = {
        'host': 'localhost',
        'port': 5432,
    }

# config/development.py

from config.base import BaseConfig

class DevelopmentConfig(BaseConfig):
    """开发环境配置."""
    DEBUG = True
    DATABASE = {
        **BaseConfig.DATABASE,
        'name': 'dev_db',
    }

# config/production.py

from config.base import BaseConfig

class ProductionConfig(BaseConfig):
    """生产环境配置."""
    DEBUG = False
    DATABASE = {
        **BaseConfig.DATABASE,
        'name': 'prod_db',
    }

# config/__init__.py

def get_config(env: str = 'development'):
    """获取配置."""
    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
    }
    return configs.get(env, DevelopmentConfig)()

# 使用
config = get_config('development')
print(config.DEBUG)  # True
print(config.DATABASE['name'])  # 'dev_db'
```
