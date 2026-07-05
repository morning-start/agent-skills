# Friendly Python 设计模式

## 目录
- [核心理念](#核心理念)
- [用户友好模式](#用户友好模式)
- [维护友好模式](#维护友好模式)
- [构建模式](#构建模式)
- [生态扩展模式](#生态扩展模式)
- [明确性原则](#明确性原则)
- [常见场景示例](#常见场景示例)

## 概览

本文档基于 [Frost Ming](https://frostming.com) 的 "Friendly Python" 系列，提供用户友好和维护友好的 Python 设计模式和最佳实践。

## 核心理念

Friendly Python = **用户友好** + **维护友好**

```
┌──────────────────────────────────────────────────────────┐
│           FRIENDLY PYTHON = User-Friendly Python         │
├────────────────────────────────┬─────────────────────────┤
│   User-Friendly               │   Maintainer-Friendly     │
│   ─────────────────           │   ─────────────────      │
│   • Sensible defaults         │   • Single change point  │
│   • Minimal required params   │   • Registry over if-else│
│   • Hidden resource mgmt      │   • Explicit over magic  │
│   • Simple → complex path     │   • Readable & debuggable│
└────────────────────────────────┴─────────────────────────┘
```

## 用户友好模式

### 1. 提供合理默认值

**❌ Bad: 需要用户配置所有参数**

```python
class Database:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

# 使用时必须提供所有参数
db = Database("localhost", 5432, "user", "pass", "mydb")
```

**✅ Good: 提供默认值，快速启动**

```python
class Database:
    def __init__(
        self,
        host="localhost",
        port=5432,
        user=None,
        password=None,
        database=None
    ):
        self.host = host
        self.port = port
        self.user = user or os.getenv("DB_USER")
        self.password = password or os.getenv("DB_PASSWORD")
        self.database = database or os.getenv("DB_NAME")

# 可以快速启动，使用环境变量或默认值
db = Database()
```

### 2. 最少必需参数

**❌ Bad: 暴露复杂的对象组装**

```python
class APIClient:
    def __init__(self, session, retry_strategy, timeout):
        self.session = session
        self.retry_strategy = retry_strategy
        self.timeout = timeout

# 使用者需要手动组装所有对象
session = requests.Session()
retry = Retry(total=3)
client = APIClient(session, retry, 30)
```

**✅ Good: 隐藏复杂组装，提供简化接口**

```python
class APIClient:
    def __init__(self, retry_times=3, timeout=30):
        self.session = requests.Session()
        self.session.mount('http', HTTPAdapter(max_retries=Retry(total=retry_times)))
        self.timeout = timeout

# 使用者只需关心关键参数
client = APIClient(retry_times=5, timeout=60)
```

### 3. 透明的资源管理

**❌ Bad: 需要手动管理资源**

```python
class FileProcessor:
    def __init__(self, filename):
        self.file = open(filename)

    def process(self):
        # 处理文件
        pass

    def close(self):
        self.file.close()

# 容易忘记关闭文件
processor = FileProcessor("data.txt")
processor.process()
processor.close()
```

**✅ Good: 使用上下文管理器**

```python
class FileProcessor:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename)
        return self

    def process(self):
        # 处理文件
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

# 自动管理资源
with FileProcessor("data.txt") as processor:
    processor.process()
```

### 4. 简单到复杂

**❌ Bad: 所有场景都需要复杂配置**

```python
class DataProcessor:
    def __init__(self, config_dict):
        # 需要阅读文档才能知道如何配置
        self.transformers = []
        if "normalize" in config_dict:
            self.transformers.append(NormalizeTransformer(config_dict["normalize"]))
        if "scale" in config_dict:
            self.transformers.append(ScaleTransformer(config_dict["scale"]))
        # ...

# 简单场景也需要复杂配置
processor = DataProcessor({"normalize": {"method": "min-max"}})
```

**✅ Good: 简单场景用默认值，复杂场景显式配置**

```python
class DataProcessor:
    def __init__(self, normalize=True, scale=None):
        self.transformers = []
        if normalize:
            self.transformers.append(NormalizeTransformer())
        if scale:
            self.transformers.append(ScaleTransformer(scale))

    def add_transformer(self, transformer):
        self.transformers.append(transformer)

# 简单场景
processor = DataProcessor()

# 复杂场景
processor = DataProcessor(normalize=False)
processor.add_transformer(CustomTransformer())
```

## 维护友好模式

### 1. 注册表替代 if-else

**❌ Bad: 添加新策略需要修改多处**

```python
class DataParser:
    def parse(self, data, format_type):
        if format_type == "json":
            return self._parse_json(data)
        elif format_type == "xml":
            return self._parse_xml(data)
        elif format_type == "yaml":
            return self._parse_yaml(data)
        # 添加新格式需要修改这里的条件链
        else:
            raise ValueError(f"Unsupported format: {format_type}")

    def _parse_json(self, data):
        return json.loads(data)

    def _parse_xml(self, data):
        return xmltodict.parse(data)

    def _parse_yaml(self, data):
        return yaml.safe_load(data)
```

**✅ Good: 使用注册表，添加新策略只需注册**

```python
class DataParser:
    def __init__(self):
        self._parsers = {}

    def register(self, format_type):
        def decorator(parser_func):
            self._parsers[format_type] = parser_func
            return parser_func
        return decorator

    def parse(self, data, format_type):
        if format_type not in self._parsers:
            raise ValueError(f"Unsupported format: {format_type}")
        return self._parsers[format_type](data)

parser = DataParser()

@parser.register("json")
def parse_json(data):
    return json.loads(data)

@parser.register("xml")
def parse_xml(data):
    return xmltodict.parse(data)

@parser.register("yaml")
def parse_yaml(data):
    return yaml.safe_load(data)

# 添加新格式只需注册，无需修改核心代码
@parser.register("csv")
def parse_csv(data):
    return pandas.read_csv(io.StringIO(data))
```

### 2. 谨慎使用魔法

**❌ Bad: 自动扫描降低可读性**

```python
class CommandRegistry:
    def __init__(self):
        self.commands = {}
        self._auto_discover_commands()

    def _auto_discover_commands(self):
        # 自动扫描模块，难以理解和调试
        import pkgutil
        import commands
        for importer, modname, ispkg in pkgutil.iter_modules(commands.__path__):
            module = __import__(f"commands.{modname}", fromlist=["__name__"])
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if hasattr(attr, "is_command"):
                    self.commands[attr.name] = attr
```

**✅ Good: 显式注册，清晰可读**

```python
class CommandRegistry:
    def __init__(self):
        self.commands = {}

    def register(self, command):
        self.commands[command.name] = command
        return command

registry = CommandRegistry()

@registry.register
class ListCommand:
    name = "list"
    def execute(self, args):
        # 实现
        pass

@registry.register
class CreateCommand:
    name = "create"
    def execute(self, args):
        # 实现
        pass
```

## 构建模式

### 1. 避免半成品对象

**❌ Bad: 需要额外步骤才能使用**

```python
class Config:
    def __init__(self, config_file=None):
        self.data = {}
        if config_file:
            self.load(config_file)
        # 如果不传 config_file，对象是半成品，无法使用

    def load(self, config_file):
        with open(config_file) as f:
            self.data = json.load(f)

    def get(self, key):
        return self.data.get(key)

# 容易创建不可用的对象
config = Config()  # 半成品！
# ... 后来才想起来要加载
config.load("config.json")
value = config.get("key")
```

**✅ Good: 使用 classmethod 构建，保证对象完整**

```python
class Config:
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_file(cls, config_file):
        with open(config_file) as f:
            data = json.load(f)
        return cls(data)

    @classmethod
    def from_dict(cls, config_dict):
        return cls(config_dict)

    @classmethod
    def from_env(cls):
        return cls(dict(os.environ))

    def get(self, key):
        return self.data.get(key)

# 对象创建即完整
config = Config.from_file("config.json")
value = config.get("key")
```

### 2. 多源多入口

**❌ Bad: 用标志控制不同来源**

```python
class DataSource:
    def __init__(self, source_type, source_info):
        self.source_type = source_type
        self.source_info = source_info

        if source_type == "file":
            self._load_from_file(source_info)
        elif source_type == "url":
            self._load_from_url(source_info)
        elif source_type == "env":
            self._load_from_env(source_info)
        # 互斥参数混在一起

# 使用时参数不清晰
data = DataSource("file", "data.json")
```

**✅ Good: 不同的入口，参数清晰**

```python
class DataSource:
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_file(cls, filepath):
        with open(filepath) as f:
            data = json.load(f)
        return cls(data)

    @classmethod
    def from_url(cls, url):
        response = requests.get(url)
        return cls(response.json())

    @classmethod
    def from_env(cls, prefix=""):
        data = {
            k[len(prefix):]: v
            for k, v in os.environ.items()
            if k.startswith(prefix)
        }
        return cls(data)

# 使用时参数清晰，自解释
data = DataSource.from_file("data.json")
data = DataSource.from_url("https://api.example.com/data")
data = DataSource.from_env(prefix="APP_")
```

## 生态扩展模式

### 1. 使用官方扩展点

**❌ Bad: 猴子补丁**

```python
# 修改第三方库的行为
import requests
original_get = requests.get

def patched_get(*args, **kwargs):
    print(f"Requesting: {args[0]}")
    return original_get(*args, **kwargs)

requests.get = patched_get  # 危险！影响全局
```

**✅ Good: 使用官方扩展点**

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# 正确使用 requests 的扩展点
response = session.get("https://api.example.com/data")
```

### 2. 包装而非重写

**❌ Bad: 覆盖第三方库全部接口**

```python
class MyDatabase:
    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)

    def execute(self, query, params=None):
        return self.conn.cursor().execute(query, params)

    def fetchall(self):
        return self.conn.cursor().fetchall()

    # 需要复制 psycopg2 的所有方法...
    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
    # ... 很多重复代码
```

**✅ Good: 组合扩展，添加特定功能**

```python
class Database:
    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)

    def __getattr__(self, name):
        # 委托到原始连接
        return getattr(self.conn, name)

    def query(self, query, params=None):
        """扩展功能：自动处理查询和结果获取"""
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_in_transaction(self, operations):
        """扩展功能：事务管理"""
        try:
            for op in operations:
                op(self.conn)
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

# 使用原有接口 + 新接口
db = Database("postgresql://...")
data = db.query("SELECT * FROM users")
db.execute_in_transaction([
    lambda conn: conn.execute("INSERT INTO users VALUES (1)"),
    lambda conn: conn.execute("UPDATE users SET name='Alice'")
])
```

## 明确性原则

### 1. 避免 `__getattr__` 回退

**❌ Bad: 使用 `__getattr__` 隐藏实际属性**

```python
class DynamicObject:
    def __init__(self):
        self._data = {}

    def __getattr__(self, name):
        # 隐藏实际的数据访问
        if name.startswith("_"):
            return super().__getattr__(name)
        return self._data.get(name)

obj = DynamicObject()
obj.name = "Alice"  # 实际调用 __setattr__
print(obj.name)     # 实际调用 __getattr__
# IDE 无法提示，类型检查失效
```

**✅ Good: 使用描述符或显式属性**

```python
class DataField:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, owner):
        if obj is None:
            return self
        return obj._data.get(self.name)

    def __set__(self, obj, value):
        obj._data[self.name] = value

class User:
    name = DataField()
    age = DataField()

    def __init__(self):
        self._data = {}

user = User()
user.name = "Alice"  # IDE 可以提示，类型检查有效
print(user.name)
```

### 2. 谨慎使用元类

**❌ Bad: 元类过度使用**

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        print("Creating database instance")

# 增加理解成本
db1 = Database()
db2 = Database()  # 隐式的单例行为
```

**✅ Good: 使用更简单的模式**

```python
# 方案 1: 模块级单例（推荐）
# database.py
class _Database:
    def __init__(self):
        print("Creating database instance")

db = _Database()

# 使用
from database import db

# 方案 2: 显式单例（如果必须）
class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("Creating database instance")
        return cls._instance

# 行为更明确
db1 = Database()
db2 = Database()
```

## 常见场景示例

### 场景 1: 多种命令实现

```python
class CommandRegistry:
    def __init__(self):
        self._commands = {}

    def register(self, name):
        def decorator(command_cls):
            self._commands[name] = command_cls
            return command_cls
        return decorator

    def get_command(self, name):
        return self._commands.get(name)

registry = CommandRegistry()

@registry.register("list")
class ListCommand:
    def execute(self, args):
        print("Listing items...")

@registry.register("create")
class CreateCommand:
    def execute(self, args):
        print("Creating item...")

# 使用
command = registry.get_command("list")
command.execute(args)
```

### 场景 2: 资源管理

```python
class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.conn = None

    def __enter__(self):
        self.conn = psycopg2.connect(self.connection_string)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        return False

# 使用
with DatabaseConnection("postgresql://...") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
```

### 场景 3: 配置管理

```python
class Config:
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_file(cls, filepath):
        with open(filepath) as f:
            data = yaml.safe_load(f)
        return cls(data)

    @classmethod
    def from_dict(cls, config_dict):
        return cls(config_dict)

    @classmethod
    def from_env(cls, prefix=""):
        data = {
            k[len(prefix):]: v
            for k, v in os.environ.items()
            if k.startswith(prefix)
        }
        return cls(data)

    def get(self, key, default=None):
        return self.data.get(key, default)

# 使用
config = Config.from_file("config.yaml")
db_url = config.get("database.url")
```

### 场景 4: 插件系统

```python
class PluginManager:
    def __init__(self):
        self.plugins = {}

    def register(self, plugin_name):
        def decorator(plugin_cls):
            self.plugins[plugin_name] = plugin_cls
            return plugin_cls
        return decorator

    def load_plugin(self, plugin_name, **kwargs):
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin {plugin_name} not found")
        return self.plugins[plugin_name](**kwargs)

plugins = PluginManager()

@plugins.register("authentication")
class AuthenticationPlugin:
    def __init__(self, api_key):
        self.api_key = api_key

    def authenticate(self, request):
        # 实现认证逻辑
        pass

# 使用
auth_plugin = plugins.load_plugin("authentication", api_key="xxx")
auth_plugin.authenticate(request)
```

## 参考

- [Friendly Python 1](https://frostming.com/posts/2021/07-07/friendly-python-1/)
- [Friendly Python 2](https://frostming.com/posts/2021/07-23/friendly-python-2/)
- [Friendly Python OOP](https://frostming.com/posts/2022/friendly-python-oop/)
- [Friendly Python Reuse](https://frostming.com/posts/2024/friendly-python-reuse/)
- [Friendly Python Port](https://frostming.com/posts/2025/friendly-python-port/)
