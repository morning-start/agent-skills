# 三层分析漏斗架构

## 概览

本架构采用分层分析策略，从基础到高级逐层扫描代码，避免"过度优化"或"无效建议"。

```
┌─────────────────────────────────────────────────────────────┐
│  L1: 静态合规层 (Static Compliance)                           │
│  目标：确保代码符合语言规范和最佳实践                           │
├─────────────────────────────────────────────────────────────┤
│  L2: 逻辑与结构层 (Logic & Structure)                         │
│  目标：解决重复、抽象不足、可读性差的问题                        │
├─────────────────────────────────────────────────────────────┤
│  L3: 性能与安全层 (Performance & Security)                    │
│  目标：提升运行效率和安全性                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## L1: 静态合规层 (Static Compliance)

### 目标

确保代码符合语言规范和最佳实践，识别基础的代码质量问题。

### 检测点

| 检测项 | 描述 | 工具参考 | 风险等级 |
|--------|------|----------|----------|
| **命名规范** | 变量/函数/类命名是否符合约定 | ESLint, Pylint | 🟡 中 |
| **注释完整性** | 关键逻辑是否有注释说明 | JSDoc, Docstring | 🟡 中 |
| **未使用代码** | 声明但未使用的变量/函数 | TSLint, Flake8 | 🟢 低 |
| **死代码** | 永远无法执行的代码路径 | SonarQube | 🟡 中 |
| **语法风险** | 潜在的语法错误 | Language Server | 🟠 高 |

### 检测规则示例

#### 命名规范

```python
# ❌ 不规范
def myfunc(a, b):  # 函数名无语义，参数名无意义
    return a + b

# ✅ 规范
def calculate_total_price(unit_price: float, quantity: int) -> float:
    """计算商品总价"""
    return unit_price * quantity
```

#### 注释完整性

```python
# ❌ 缺少注释
def process(data):
    result = []
    for item in data:
        if item > 100:
            result.append(item * 0.9)
    return result

# ✅ 完整注释
def apply_bulk_discount(prices: list[float], threshold: float = 100) -> list[float]:
    """
    为超过阈值的价格应用批量折扣
    
    Args:
        prices: 原始价格列表
        threshold: 享受折扣的价格阈值，默认 100
    
    Returns:
        应用折扣后的价格列表
    """
    return [price * 0.9 if price > threshold else price for price in prices]
```

### 输出示例

```
🔴 L1-001: 未使用的变量
- 位置：第 15 行
- 代码：let unusedVar = calculateData();
- 建议：删除未使用的变量，或添加使用逻辑
- 影响：代码冗余，可能导致内存浪费

🟡 L1-002: 命名不规范
- 位置：第 23 行
- 代码：function abc(x, y) { ... }
- 建议：使用描述性函数名，如 calculateDistance(x, y)
- 影响：降低代码可读性
```

---

## L2: 逻辑与结构层 (Logic & Structure)

### 目标

解决代码重复、抽象不足、可读性差的问题，提升代码可维护性。

### 检测点

| 检测项 | 阈值/标准 | 优化手段 | 风险等级 |
|--------|-----------|----------|----------|
| **函数长度** | > 50 行 | 拆分函数 | 🟠 高 |
| **类长度** | > 300 行 | 提取类 | 🟠 高 |
| **循环嵌套** | > 3 层 | 提取方法/使用流式 API | 🟡 中 |
| **重复代码** | 相似度 > 80% | 提取公共函数 | 🟠 高 |
| **魔法数字** | 无意义字面量 | 定义为常量/枚举 | 🟡 中 |
| **圈复杂度** | > 15 | 拆分/使用策略模式 | 🟠 高 |

### 检测规则示例

#### DRY 原则（重复代码）

```python
# ❌ 重复代码
def process_order_vip(order):
    if order.status == 'pending':
        if order.amount > 1000:
            return order.amount * 0.9
    return order.amount

def process_order_regular(order):
    if order.status == 'pending':
        if order.amount > 500:
            return order.amount * 0.95
    return order.amount

# ✅ 提取公共逻辑
def process_order(order: Order, threshold: float, discount: float) -> float:
    """处理订单折扣逻辑"""
    if order.status != 'pending':
        return order.amount
    if order.amount > threshold:
        return order.amount * discount
    return order.amount
```

#### 单一职责原则

```python
# ❌ 一个函数承担过多职责
def process_user_data(user_id):
    # 查询用户
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    # 验证数据
    if not user:
        return None
    if user.age < 18:
        return None
    # 计算积分
    points = user.purchase_amount * 0.01
    # 更新数据库
    db.execute("UPDATE users SET points = ? WHERE id = ?", points, user_id)
    # 发送通知
    send_email(user.email, "积分更新通知")
    return points

# ✅ 拆分函数
def get_eligible_user(user_id: int) -> Optional[User]:
    """获取符合条件的用户"""
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    if not user or user.age < 18:
        return None
    return user

def calculate_points(purchase_amount: float) -> float:
    """计算积分"""
    return purchase_amount * 0.01

def notify_user(user: User, message: str):
    """通知用户"""
    send_email(user.email, message)
```

### 输出示例

```
🔴 L2-003: 重复代码 (DRY Violation)
- 位置：第 45-60 行 与 第 80-95 行
- 相似度：92%
- 描述：两处逻辑几乎完全相同，仅参数不同
- 建议：提取为通用函数 processOrder(type, config)
- 重构代码：
  ```python
  def process_order(order_type: str, config: dict) -> OrderResult:
      # 合并后的通用逻辑
      validate_config(config)
      return execute_order(order_type, config)
  ```

🟡 L2-004: 魔法数字
- 位置：第 12 行
- 代码：if count > 10:
- 描述：数字 10 缺乏语义说明
- 建议：定义为常量 MAX_RETRY_COUNT = 10
```

---

## L3: 性能与安全层 (Performance & Security)

### 目标

识别并修复性能瓶颈和安全漏洞，确保代码高效、安全运行。

### 检测点

| 检测项 | 风险等级 | 优化手段 | 影响范围 |
|--------|----------|----------|----------|
| **O(n²) 算法** | 高 | 改为 O(n log n) | 性能 |
| **循环内查询** | 高 | 批量查询/缓存 | 性能 |
| **SQL 拼接** | 严重 | 参数化查询 | 安全 |
| **资源未关闭** | 高 | 使用 with/try-finally | 稳定性 |
| **硬编码密钥** | 严重 | 环境变量/密钥管理 | 安全 |
| **竞态条件** | 高 | 加锁/原子操作 | 安全性 |

### 检测规则示例

#### N+1 查询问题

```python
# ❌ N+1 查询
def get_user_orders(user_ids: list[int]) -> list[Order]:
    all_orders = []
    for user_id in user_ids:
        orders = db.query(
            "SELECT * FROM orders WHERE user_id = ?", 
            user_id
        )
        all_orders.extend(orders)
    return all_orders

# ✅ 批量查询
def get_user_orders(user_ids: list[int]) -> list[Order]:
    if not user_ids:
        return []
    placeholders = ','.join(['?' for _ in user_ids])
    return db.query(
        f"SELECT * FROM orders WHERE user_id IN ({placeholders})",
        user_ids
    )
```

#### SQL 注入风险

```python
# ❌ SQL 注入风险
def get_user(username: str) -> Optional[User]:
    return db.query(
        f"SELECT * FROM users WHERE username = '{username}'"
    )

# ✅ 参数化查询
def get_user(username: str) -> Optional[User]:
    return db.query(
        "SELECT * FROM users WHERE username = ?",
        [username]
    )
```

#### 资源泄漏

```python
# ❌ 资源未关闭
def read_file(path: str) -> str:
    f = open(path, 'r')
    content = f.read()
    # 忘记关闭文件
    return content

# ✅ 使用上下文管理器
def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()
```

### 输出示例

```
🔴 L3-002: 性能瓶颈 - N+1 查询
- 位置：第 23-28 行
- 描述：在 for 循环中执行数据库查询，导致 N+1 问题
- 当前复杂度：O(n) 次查询
- 建议：改为批量查询，单次获取所有数据
- 预期提升：99%+ (n=100 时)
- 重构代码：
  ```python
  # ❌ 优化前
  for user_id in user_ids:
      user = db.query("SELECT * FROM users WHERE id = ?", user_id)
  
  # ✅ 优化后
  users = db.query("SELECT * FROM users WHERE id IN ?", user_ids)
  ```

🔴 L3-005: 安全漏洞 - SQL 注入
- 位置：第 34 行
- 描述：直接使用字符串拼接 SQL 查询
- 风险：可能导致数据泄露、数据篡改
- 建议：立即使用参数化查询
- 修复代码：
  ```python
  # ❌ 风险代码
  query = f"SELECT * FROM users WHERE id = {user_id}"
  
  # ✅ 安全代码
  query = "SELECT * FROM users WHERE id = ?"
  params = [user_id]
  ```
```

---

## 三层协作流程

```
1. 接收代码输入
        ↓
2. L1 静态合规扫描
   ├── 命名规范检查
   ├── 注释完整性检查
   ├── 未使用代码检测
   └── 语法风险识别
        ↓
3. L2 逻辑与结构分析
   ├── 重复代码识别
   ├── 函数/类长度分析
   ├── 魔法数字检测
   └── 圈复杂度计算
        ↓
4. L3 性能与安全检测
   ├── 算法复杂度分析
   ├── 资源泄漏检测
   ├── 安全漏洞扫描
   └── 并发问题识别
        ↓
5. 生成综合报告
   ├── 问题汇总（按优先级）
   ├── 重构方案（含代码对比）
   └── 优化建议（量化影响）
```

---

## 优先级判定规则

| 层级 | 问题类型 | 优先级 | 响应时间 |
|------|----------|--------|----------|
| L3 | 安全漏洞（SQL 注入、硬编码密钥） | P0 | 立即 |
| L3 | 严重性能问题（N+1 查询、O(n²)） | P1 | 24 小时 |
| L2 | 严重重复代码、函数过长 | P1 | 24 小时 |
| L2 | 魔法数字、嵌套过深 | P2 | 下次迭代 |
| L1 | 命名不规范、注释缺失 | P2 | 下次迭代 |
| L1 | 未使用变量、死代码 | P3 | 技术债务 |

---

## 架构优势

### 1. 分层递进

- 从基础到高级，逐层深入
- 避免跳过基础问题直接优化性能
- 确保每层问题都得到适当关注

### 2. 可解释性强

- 每层有明确的目标和检测点
- 问题定位精准（行号、代码片段）
- 优化建议有明确的理论依据

### 3. 避免过度优化

- L1/L2 问题解决后再考虑 L3
- 根据代码场景调整优化重点
- 不为了"完美"而强行引入复杂模式

### 4. 技术栈无关

- 架构适用于各种编程语言
- 具体检测规则可适配不同技术栈
- 工具推荐因技术栈而异

---

## 参考资源

- **代码整洁之道** - Robert C. Martin（L2 层理论依据）
- **重构：改善既有代码的设计** - Martin Fowler（L2 层实践指南）
- **Effective Software Maintenance**（L3 层性能优化）
- **OWASP Top 10**（L3 层安全检测标准）
- **SonarQube Rules**（三层规则参考）
