# 使用示例

## 概览

本章节提供多场景的完整代码优化示例，展示三层分析漏斗的实际应用。

---

## 示例 1: Python 代码优化

### 场景描述

**代码类型**: 订单处理函数  
**场景**: 电商订单折扣计算  
**性能要求**: 中等（批处理）  
**安全性要求**: 一般（内部逻辑）

### 原始代码

```python
def process_orders(orders):
    results = []
    for order in orders:
        if order.status == 1:
            # 处理待支付订单
            if order.amount > 1000:
                if order.user.is_vip:
                    discount = 0.9
                else:
                    discount = 0.95
            else:
                discount = 1.0
            final_price = order.amount * discount
            results.append(final_price)
    return results
```

### AI 分析报告

```markdown
## 🛡️ 代码优化分析报告

### 1. 总体评估

- **代码质量评分**: 6/10
- **复杂度**: 中 (Cyclomatic Complexity: 8)
- **可维护性**: 中等
- **主要风险**: 
  - 🟡 魔法数字（1, 1000, 0.9, 0.95）
  - 🟡 嵌套过深（4 层 if 嵌套）
  - 🟡 硬编码状态码（status == 1）
- **技术债务**: 2-3 小时

### 2. 问题汇总

| 优先级 | 问题类型 | 数量 | 影响范围 |
|--------|----------|------|----------|
| P2 | 可维护性 | 3 | 订单处理逻辑 |
| P3 | 优化建议 | 2 | 代码风格 |

### 3. 关键问题与重构方案

#### 🟡 问题 1: 魔法数字

- **位置**: 第 4、6、7、9 行
- **描述**: 使用了多个无语义的数字字面量
  - `1`: 订单状态
  - `1000`: 金额阈值
  - `0.9`: VIP 折扣率
  - `0.95`: 非 VIP 折扣率
- **影响**: 代码难以理解和维护，修改时需要多处查找
- **建议**: 定义为常量或枚举

#### 🟡 问题 2: 嵌套过深

- **位置**: 第 3-12 行
- **描述**: if 语句嵌套达到 4 层
  ```
  for
    └─ if (status)
         └─ if (amount)
              └─ if (is_vip)
  ```
- **影响**: 可读性差，容易出错，难以测试
- **建议**: 使用提前返回 (Early Return) 或卫语句

#### 🟡 问题 3: 硬编码状态码

- **位置**: 第 3 行
- **描述**: `order.status == 1` 缺乏语义
- **影响**: 不理解业务的人不知道 1 代表什么
- **建议**: 使用枚举 `OrderStatus.PENDING_PAYMENT`

### 4. 重构代码

```python
from enum import Enum
from typing import List

class OrderStatus(Enum):
    """订单状态枚举"""
    PENDING_PAYMENT = 1
    PAID = 2
    SHIPPED = 3
    CANCELLED = 4

# 折扣常量
VIP_HIGH_AMOUNT_DISCOUNT = 0.9
NON_VIP_HIGH_AMOUNT_DISCOUNT = 0.95
LOW_AMOUNT_DISCOUNT = 1.0
HIGH_AMOUNT_THRESHOLD = 1000

def process_orders(orders: List['Order']) -> List[float]:
    """
    处理订单并计算最终价格
    
    Args:
        orders: 订单列表
    
    Returns:
        计算后的订单价格列表
    """
    results = []
    
    for order in orders:
        if order.status != OrderStatus.PENDING_PAYMENT:
            continue
        
        discount = get_order_discount(order)
        final_price = order.amount * discount
        results.append(final_price)
    
    return results

def get_order_discount(order: 'Order') -> float:
    """
    根据订单和用户属性计算折扣
    
    Args:
        order: 订单对象
    
    Returns:
        折扣率（0-1 之间）
    """
    if order.amount > HIGH_AMOUNT_THRESHOLD:
        return (
            VIP_HIGH_AMOUNT_DISCOUNT 
            if order.user.is_vip 
            else NON_VIP_HIGH_AMOUNT_DISCOUNT
        )
    return LOW_AMOUNT_DISCOUNT
```

### 5. 改进总结

✅ **提取常量，消除魔法数字**
- 所有数字都有明确语义
- 修改折扣率只需改常量定义

✅ **使用枚举，提升状态码语义**
- `OrderStatus.PENDING_PAYMENT` 一目了然
- IDE 提供自动补全

✅ **拆分函数，降低嵌套深度**
- 从 4 层嵌套降低到 2 层
- 使用提前返回 (continue)

✅ **添加类型注解和文档字符串**
- IDE 提供更好的提示
- 便于自动生成文档

### 6. 推荐测试用例

```python
def test_process_empty_list():
    """测试空订单列表"""
    assert process_orders([]) == []

def test_process_pending_payment():
    """测试待支付订单"""
    order = Order(
        status=OrderStatus.PENDING_PAYMENT,
        amount=1000,
        user=User(is_vip=False)
    )
    assert process_orders([order]) == [950.0]

def test_skip_non_pending():
    """测试跳过非待支付订单"""
    order = Order(
        status=OrderStatus.PAID,
        amount=1000
    )
    assert process_orders([order]) == []

def test_vip_discount():
    """测试 VIP 折扣"""
    order = Order(
        status=OrderStatus.PENDING_PAYMENT,
        amount=2000,
        user=User(is_vip=True)
    )
    assert process_orders([order]) == [1800.0]
```
```

---

## 示例 2: JavaScript 性能优化

### 场景描述

**代码类型**: 数据查询函数  
**场景**: 批量获取用户及其订单数据  
**性能要求**: 高（API 接口）  
**安全性要求**: 高（公开 API）

### 原始代码

```javascript
async function getUserData(userIds) {
    const results = [];
    for (const userId of userIds) {
        const user = await db.query(
            `SELECT * FROM users WHERE id = ${userId}`
        );
        const orders = await db.query(
            `SELECT * FROM orders WHERE user_id = ${userId}`
        );
        results.push({ user, orders });
    }
    return results;
}
```

### AI 分析报告

```markdown
## 🛡️ 代码优化分析报告

### 1. 总体评估

- **代码质量评分**: 4/10
- **主要风险**: 
  - 🔴 SQL 注入漏洞（严重）
  - 🔴 N+1 查询问题（性能）
- **性能影响**: 严重（2n 次数据库查询）
- **技术债务**: 4-6 小时

### 2. 问题汇总

| 优先级 | 问题类型 | 数量 | 影响范围 |
|--------|----------|------|----------|
| P0 | 安全漏洞 | 1 | 用户数据接口 |
| P1 | 性能瓶颈 | 1 | 批量查询场景 |

### 3. 关键问题与重构方案

#### 🔴 P0: SQL 注入漏洞

- **位置**: 第 4、7 行
- **描述**: 直接使用模板字符串拼接 SQL
  ```javascript
  // 危险代码
  `SELECT * FROM users WHERE id = ${userId}`
  ```
- **影响**: 
  - 🔴 严重安全风险
  - 可能导致数据泄露、数据篡改
  - 攻击者可构造恶意 userId
- **建议**: 立即使用参数化查询

#### 🔴 P1: N+1 查询问题

- **位置**: 第 3-8 行
- **描述**: 循环内执行数据库查询
  - userIds 长度为 100 时 → 执行 200 次查询
  - userIds 长度为 1000 时 → 执行 2000 次查询
- **影响**: 
  - 性能极差
  - 数据库连接池可能耗尽
  - 响应时间随用户数线性增长
- **建议**: 改为批量查询

### 4. 重构代码

```javascript
async function getUserData(userIds: number[]) {
    if (userIds.length === 0) {
        return [];
    }
    
    // ✅ 批量查询用户（1 次查询）
    const users = await db.query(
        'SELECT * FROM users WHERE id IN (?)',
        [userIds]
    );
    
    // ✅ 批量查询订单（1 次查询）
    const orders = await db.query(
        'SELECT * FROM orders WHERE user_id IN (?)',
        [userIds]
    );
    
    // ✅ 内存中组装数据
    const userMap = new Map(
        users.map(u => [u.id, u])
    );
    
    const ordersByUserId = new Map();
    for (const order of orders) {
        if (!ordersByUserId.has(order.user_id)) {
            ordersByUserId.set(order.user_id, []);
        }
        ordersByUserId.get(order.user_id).push(order);
    }
    
    return userIds.map(userId => ({
        user: userMap.get(userId),
        orders: ordersByUserId.get(userId) || []
    }));
}
```

### 5. 性能对比

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| **查询次数** | 2n | 2 | 99%+ (n=100) |
| **执行时间** | ~5000ms | ~100ms | 98% |
| **连接池占用** | 2n 个连接 | 2 个连接 | 99%+ |
| **安全性** | 🔴 高危 | ✅ 安全 | - |

### 6. 安全性检查清单

- [x] SQL 注入（已使用参数化查询）
- [ ] 输入验证（建议添加 userId 格式验证）
- [ ] 权限检查（建议验证当前用户是否有权访问）
- [ ] 数据脱敏（建议隐藏敏感字段）

### 7. 推荐测试用例

```javascript
test('getUserData returns empty array for empty input', async () => {
    const result = await getUserData([]);
    expect(result).toEqual([]);
});

test('getUserData fetches users with orders', async () => {
    const userIds = [1, 2, 3];
    const result = await getUserData(userIds);
    
    expect(result).toHaveLength(3);
    expect(result[0]).toHaveProperty('user');
    expect(result[0]).toHaveProperty('orders');
});

test('getUserData handles users without orders', async () => {
    const result = await getUserData([999]);
    expect(result[0].user).toBeDefined();
    expect(result[0].orders).toEqual([]);
});
```
```

---

## 示例 3: Java 重构

### 场景描述

**代码类型**: 业务逻辑类  
**场景**: 支付处理服务  
**性能要求**: 高（核心业务）  
**可维护性要求**: 高（多人协作）

### 原始代码

```java
public class PaymentService {
    public void processPayment(Order order) {
        if (order.getType().equals("alipay")) {
            if (order.getAmount() < 1000) {
                // 小额直接支付
                alipay.pay(order.getAmount());
            } else {
                // 大额需要验证
                if (order.getUser().isVerified()) {
                    alipay.pay(order.getAmount());
                } else {
                    throw new RuntimeException("用户未验证");
                }
            }
        } else if (order.getType().equals("wechat")) {
            if (order.getAmount() < 1000) {
                wechatPay.pay(order.getAmount());
            } else {
                if (order.getUser().isVerified()) {
                    wechatPay.pay(order.getAmount());
                } else {
                    throw new RuntimeException("用户未验证");
                }
            }
        } else if (order.getType().equals("credit_card")) {
            creditCard.pay(order.getAmount());
        }
    }
}
```

### AI 分析报告

```markdown
## 🛡️ 代码优化分析报告

### 1. 总体评估

- **代码质量评分**: 5/10
- **复杂度**: 高 (Cyclomatic Complexity: 12)
- **可维护性**: 低
- **主要风险**: 
  - 🟠 严重代码重复（支付宝和微信逻辑几乎相同）
  - 🟠 违反开闭原则（添加新支付方式需要修改代码）
  - 🟡 魔法字符串（"alipay", "wechat"）
- **技术债务**: 6-8 小时

### 2. 问题汇总

| 优先级 | 问题类型 | 数量 | 影响范围 |
|--------|----------|------|----------|
| P1 | 代码重复 | 2 | 支付逻辑 |
| P1 | 设计问题 | 1 | 架构扩展性 |
| P2 | 魔法字符串 | 2 | 支付类型 |

### 3. 关键问题与重构方案

#### 🟠 问题 1: 严重代码重复

- **位置**: 第 4-11 行 与 第 12-19 行
- **描述**: 支付宝和微信支付的逻辑几乎完全相同
  ```java
  // 支付宝
  if (order.getAmount() < 1000) {
      alipay.pay(order.getAmount());
  } else {
      if (order.getUser().isVerified()) {
          alipay.pay(order.getAmount());
      } else {
          throw new RuntimeException("用户未验证");
      }
  }
  
  // 微信支付（几乎一样）
  if (order.getAmount() < 1000) {
      wechatPay.pay(order.getAmount());
  } else {
      if (order.getUser().isVerified()) {
          wechatPay.pay(order.getAmount());
      } else {
          throw new RuntimeException("用户未验证");
      }
  }
  ```
- **影响**: 维护成本高，修改逻辑需要改多处
- **建议**: 提取公共逻辑，使用策略模式

#### 🟠 问题 2: 违反开闭原则

- **描述**: 添加新支付方式需要修改 processPayment 方法
- **影响**: 违反开闭原则，增加测试成本
- **建议**: 使用策略模式 + 工厂模式

### 4. 重构代码

```java
// 定义支付策略接口
public interface PaymentStrategy {
    void pay(Order order);
}

// 支付宝策略
public class AlipayStrategy implements PaymentStrategy {
    private static final BigDecimal HIGH_AMOUNT_THRESHOLD = new BigDecimal("1000");
    
    @Override
    public void pay(Order order) {
        if (order.getAmount().compareTo(HIGH_AMOUNT_THRESHOLD) < 0) {
            AlipayClient.pay(order.getAmount());
        } else {
            verifyUser(order.getUser());
            AlipayClient.pay(order.getAmount());
        }
    }
    
    private void verifyUser(User user) {
        if (!user.isVerified()) {
            throw new PaymentException("大额支付需要用户验证");
        }
    }
}

// 微信支付策略
public class WechatPayStrategy implements PaymentStrategy {
    private static final BigDecimal HIGH_AMOUNT_THRESHOLD = new BigDecimal("1000");
    
    @Override
    public void pay(Order order) {
        if (order.getAmount().compareTo(HIGH_AMOUNT_THRESHOLD) < 0) {
            WechatPayClient.pay(order.getAmount());
        } else {
            verifyUser(order.getUser());
            WechatPayClient.pay(order.getAmount());
        }
    }
    
    private void verifyUser(User user) {
        if (!user.isVerified()) {
            throw new PaymentException("大额支付需要用户验证");
        }
    }
}

// 支付工厂
public class PaymentFactory {
    private static final Map<String, PaymentStrategy> strategies = new HashMap<>();
    
    static {
        strategies.put("alipay", new AlipayStrategy());
        strategies.put("wechat", new WechatPayStrategy());
        strategies.put("credit_card", new CreditCardStrategy());
    }
    
    public static PaymentStrategy getStrategy(String type) {
        PaymentStrategy strategy = strategies.get(type);
        if (strategy == null) {
            throw new IllegalArgumentException("不支持的支付类型：" + type);
        }
        return strategy;
    }
}

// 重构后的服务类
public class PaymentService {
    public void processPayment(Order order) {
        PaymentStrategy strategy = PaymentFactory.getStrategy(order.getType());
        strategy.pay(order);
    }
}
```

### 5. 改进总结

✅ **消除代码重复**
- 使用策略模式，每个支付策略独立实现
- 公共逻辑提取到抽象基类（可选）

✅ **符合开闭原则**
- 添加新支付方式只需实现 PaymentStrategy 接口
- 无需修改现有代码

✅ **使用常量替代魔法字符串**
- 支付类型定义为常量或枚举
- 金额阈值定义为常量

✅ **异常处理规范化**
- 使用自定义异常 PaymentException
- 提供清晰的错误信息

### 6. 扩展性示例

添加银联支付：

```java
public class UnionPayStrategy implements PaymentStrategy {
    @Override
    public void pay(Order order) {
        // 银联支付逻辑（可能不需要大额验证）
        UnionPayClient.pay(order.getAmount());
    }
}

// 注册到工厂（无需修改其他代码）
static {
    strategies.put("unionpay", new UnionPayStrategy());
}
```

### 7. 推荐测试用例

```java
@Test
void testAlipaySmallAmount() {
    Order order = new Order("alipay", new BigDecimal("500"), mockUser);
    paymentService.processPayment(order);
    verify(alipayClient).pay(any());
}

@Test
void testAlipayLargeAmountVerifiedUser() {
    Order order = new Order("alipay", new BigDecimal("2000"), verifiedUser);
    paymentService.processPayment(order);
    verify(alipayClient).pay(any());
}

@Test
void testAlipayLargeAmountUnverifiedUser() {
    Order order = new Order("alipay", new BigDecimal("2000"), unverifiedUser);
    assertThrows(PaymentException.class, () -> 
        paymentService.processPayment(order)
    );
}

@Test
void testUnsupportedPaymentType() {
    Order order = new Order("unknown", new BigDecimal("100"), mockUser);
    assertThrows(IllegalArgumentException.class, () -> 
        paymentService.processPayment(order)
    );
}
```
```

---

## 示例 4: TypeScript 类型安全优化

### 场景描述

**代码类型**: 数据处理函数  
**场景**: API 响应处理  
**类型安全要求**: 高（大型项目）

### 原始代码

```typescript
function handleResponse(data) {
    if (data.status === 'success') {
        return data.result;
    } else {
        throw new Error(data.message);
    }
}

function calculateTotal(items) {
    let total = 0;
    for (let item of items) {
        total += item.price * item.quantity;
    }
    return total;
}
```

### AI 分析报告

```markdown
## 🛡️ 代码优化分析报告

### 1. 总体评估

- **代码质量评分**: 6/10
- **类型安全性**: 低（缺少类型注解）
- **主要风险**: 
  - 🟡 缺少类型注解（任何类型错误只能在运行时发现）
  - 🟡 缺少空值检查
  - 🟡 魔法字符串（'success'）
- **技术债务**: 2-3 小时

### 2. 重构代码

```typescript
// 定义类型
interface ApiResponse<T> {
    status: 'success' | 'error';
    result?: T;
    message?: string;
}

interface CartItem {
    price: number;
    quantity: number;
}

// 定义常量
const API_STATUS = {
    SUCCESS: 'success' as const,
    ERROR: 'error' as const
} as const;

// 优化后的代码
function handleResponse<T>(data: ApiResponse<T>): T {
    if (data.status === API_STATUS.SUCCESS) {
        if (data.result === undefined) {
            throw new Error('Success response but no result');
        }
        return data.result;
    } else {
        const message = data.message ?? 'Unknown error';
        throw new Error(message);
    }
}

function calculateTotal(items: CartItem[]): number {
    if (!items || items.length === 0) {
        return 0;
    }
    
    return items.reduce(
        (total, item) => total + item.price * item.quantity, 
        0
    );
}
```

### 3. 改进总结

✅ **添加类型注解**
- 函数参数和返回值都有明确类型
- 使用泛型处理不同的响应结果

✅ **定义接口**
- ApiResponse<T> 描述 API 响应结构
- CartItem 描述购物车项目

✅ **使用常量替代魔法字符串**
- API_STATUS 定义状态常量
- 使用 `as const` 确保类型安全

✅ **添加空值检查**
- 检查 result 是否存在
- 使用空值合并运算符 `??`

✅ **使用数组方法**
- 使用 reduce 替代 for 循环
- 更函数式、更简洁

### 4. 类型安全保障

优化后的类型检查：

```typescript
// ✅ 类型安全
const result = handleResponse<UserData>(response);
console.log(result.name); // IDE 提供自动补全

// ✅ 编译时错误检测
calculateTotal("invalid"); // 编译错误：参数类型不匹配

// ✅ 类型推导
const total = calculateTotal(cartItems); // total 类型为 number
```
```

---

## 示例 5: Go 并发优化

### 场景描述

**代码类型**: 数据处理服务  
**场景**: 批量处理 HTTP 请求  
**性能要求**: 极高（高并发）

### 原始代码

```go
func FetchAllData(urls []string) ([]Data, error) {
    var results []Data
    for _, url := range urls {
        resp, err := http.Get(url)
        if err != nil {
            return nil, err
        }
        defer resp.Body.Close()
        
        var data Data
        json.NewDecoder(resp.Body).Decode(&data)
        results = append(results, data)
    }
    return results, nil
}
```

### AI 分析报告

```markdown
## 🛡️ 代码优化分析报告

### 1. 总体评估

- **代码质量评分**: 5/10
- **性能**: 低（串行请求）
- **主要风险**: 
  - 🔴 资源泄漏（defer 在循环中使用）
  - 🟠 性能问题（串行 HTTP 请求）
  - 🟡 缺少错误处理
- **技术债务**: 4-6 小时

### 2. 关键问题与重构方案

#### 🔴 问题 1: 资源泄漏

- **位置**: 第 6 行
- **描述**: defer 在循环中使用，所有响应体要等到函数返回才关闭
- **影响**: 连接池耗尽，内存泄漏
- **建议**: 使用函数闭包或手动关闭

#### 🟠 问题 2: 串行请求

- **描述**: 顺序执行 HTTP 请求
  - 10 个 URL → 10 * 100ms = 1000ms
- **影响**: 响应时间随 URL 数量线性增长
- **建议**: 使用 goroutine 并发请求

### 3. 重构代码

```go
func FetchAllData(ctx context.Context, urls []string) ([]Data, error) {
    var (
        mu      sync.Mutex
        results []Data
        wg      sync.WaitGroup
        errChan = make(chan error, len(urls))
    )
    
    // 限制并发数
    sem := make(chan struct{}, 10)
    
    for _, url := range urls {
        wg.Add(1)
        go func(url string) {
            defer wg.Done()
            
            // 获取信号量
            select {
            case sem <- struct{}{}:
            case <-ctx.Done():
                errChan <- ctx.Err()
                return
            }
            defer func() { <-sem }()
            
            // 创建带超时的请求
            reqCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
            defer cancel()
            
            req, err := http.NewRequestWithContext(reqCtx, "GET", url, nil)
            if err != nil {
                errChan <- err
                return
            }
            
            resp, err := http.DefaultClient.Do(req)
            if err != nil {
                errChan <- err
                return
            }
            defer resp.Body.Close() // ✅ 在 goroutine 内关闭
            
            var data Data
            if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
                errChan <- err
                return
            }
            
            mu.Lock()
            results = append(results, data)
            mu.Unlock()
        }(url)
    }
    
    // 等待所有 goroutine 完成
    go func() {
        wg.Wait()
        close(errChan)
    }()
    
    // 收集错误
    var firstErr error
    for err := range errChan {
        if err != nil && firstErr == nil {
            firstErr = err
        }
    }
    
    return results, firstErr
}
```

### 4. 性能对比

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| **10 个 URL** | ~1000ms | ~150ms | 85% |
| **100 个 URL** | ~10000ms | ~1500ms | 85% |
| **并发连接** | 1 个 | 最多 10 个 | - |
| **资源泄漏** | 🔴 有 | ✅ 无 | - |

### 5. 改进总结

✅ **修复资源泄漏**
- defer resp.Body.Close() 在 goroutine 内执行
- 每个响应体及时处理

✅ **并发请求**
- 使用 goroutine 并发执行
- 响应时间从 O(n) 降为 O(1)

✅ **限制并发数**
- 使用信号量限制最大并发数（10）
- 避免连接池耗尽

✅ **上下文控制**
- 支持取消操作
- 超时控制（5 秒）

✅ **错误处理**
- 收集所有错误
- 返回第一个错误

### 6. 推荐测试

```go
func TestFetchAllData_Success(t *testing.T) {
    urls := []string{
        "http://api.example.com/data/1",
        "http://api.example.com/data/2",
    }
    
    ctx := context.Background()
    results, err := FetchAllData(ctx, urls)
    
    assert.NoError(t, err)
    assert.Len(t, results, 2)
}

func TestFetchAllData_Timeout(t *testing.T) {
    urls := []string{"http://slow-api.example.com/data"}
    
    ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
    defer cancel()
    
    _, err := FetchAllData(ctx, urls)
    
    assert.Error(t, err)
    assert.Contains(t, err.Error(), "timeout")
}
```
```

---

## 使用指南

### 如何选择示例

- **Python 项目**: 参考示例 1
- **Node.js/前端**: 参考示例 2 和 4
- **Java 项目**: 参考示例 3
- **Go 项目**: 参考示例 5

### 学习路径

1. **理解问题**: 先自己分析代码问题
2. **对比报告**: 查看 AI 的分析报告
3. **学习重构**: 理解重构方案和原因
4. **实践应用**: 应用到自己的代码中

---

## 参考资源

- **重构示例**: Martin Fowler, Refactoring Catalog
- **代码异味**: Code Smells (Wikipedia)
- **设计模式**: Gang of Four, Design Patterns
- **性能优化**: Brendan Gregg, Systems Performance
