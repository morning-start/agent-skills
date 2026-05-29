---
name: function-design
version: v1.0.0
author: skill-manager
parent_skill: software-design
description: 函数设计与拆分子技能，提供单一职责、纯函数、副作用管理、方法封装、高内聚低耦合等函数设计原则和最佳实践
tags: [function-design, pure-function, SRP, encapsulation, cohesion, coupling]
network_search: optional
---

# 函数设计与拆分

## 任务目标

本子技能帮助开发者编写高质量、可维护的函数，涵盖函数设计原则、拆分策略、命名规范、参数设计等核心内容。

### 核心能力

- **单一职责原则**: 一个函数只做一件事
- **纯函数设计**: 无副作用、确定性输出
- **副作用管理**: 隔离和控制副作用
- **函数拆分**: 复杂函数的分解策略
- **参数设计**: 参数数量、类型、默认值
- **函数组合**: 高阶函数、函数管道

---

## 三步流程框架

```
┌─────────────────────────────────────────────────────────────┐
│  第一步：查阅信息 (Research)                                  │
│  ├── 分析函数的职责和复杂度                                  │
│  ├── 识别函数设计问题                                        │
│  └── 确定改进方向和原则                                      │
├─────────────────────────────────────────────────────────────┤
│  第二步：执行操作 (Execute)                                   │
│  ├── 应用函数设计原则                                        │
│  ├── 拆分复杂函数                                            │
│  ├── 优化参数和返回值                                        │
│  └── 改进命名和文档                                          │
├─────────────────────────────────────────────────────────────┤
│  第三步：检查验收 (Validate)                                  │
│  ├── 验证函数是否符合单一职责                                │
│  ├── 检查函数的可测试性                                      │
│  └── 评估可读性和可维护性                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心设计原则

### 1. 单一职责原则（SRP）

**原则**: 一个函数应该只有一个改变的理由

```javascript
// ✗ 违反 SRP - 一个函数做多件事
function processUser(userData) {
  // 验证
  if (!userData.email) throw new Error('Email required');
  
  // 格式化
  userData.email = userData.email.toLowerCase();
  userData.name = userData.name.trim();
  
  // 保存到数据库
  const user = db.save(userData);
  
  // 发送邮件
  emailService.send(user.email, 'Welcome!');
  
  // 记录日志
  logger.log(`User ${user.id} created`);
  
  return user;
}

// ✓ 遵循 SRP - 拆分为多个函数
function validateUser(userData) {
  if (!userData.email) {
    throw new Error('Email required');
  }
}

function formatUserData(userData) {
  return {
    ...userData,
    email: userData.email.toLowerCase(),
    name: userData.name.trim()
  };
}

function saveUser(userData) {
  return db.save(userData);
}

function sendWelcomeEmail(user) {
  emailService.send(user.email, 'Welcome!');
}

function logUserCreation(user) {
  logger.log(`User ${user.id} created`);
}

// 主函数 - 协调各步骤
function processUser(userData) {
  validateUser(userData);
  const formatted = formatUserData(userData);
  const user = saveUser(formatted);
  sendWelcomeEmail(user);
  logUserCreation(user);
  return user;
}
```

---

### 2. 纯函数（Pure Function）

**特征**:
- 相同的输入总是产生相同的输出
- 没有副作用（不修改外部状态）

```javascript
// ✗ 非纯函数 - 依赖外部状态
let taxRate = 0.1;

function calculateTotal(price) {
  return price * (1 + taxRate);  // 依赖外部变量
}

// ✓ 纯函数 - 只依赖参数
function calculateTotal(price, taxRate) {
  return price * (1 + taxRate);
}

// ✗ 非纯函数 - 有副作用
function addToCart(cart, item) {
  cart.push(item);  // 修改了传入参数
  return cart;
}

// ✓ 纯函数 - 无副作用
function addToCart(cart, item) {
  return [...cart, item];  // 返回新数组
}
```

**纯函数的优势**:
- ✅ 可测试性强
- ✅ 可缓存（记忆化）
- ✅ 可并行执行
- ✅ 易于推理和理解

---

### 3. 副作用管理

**常见副作用**:
- 修改外部变量
- DOM 操作
- 网络请求
- 文件 I/O
- 控制台输出

**策略**: 隔离副作用

```javascript
// ✗ 副作用混入业务逻辑
async function registerUser(userData) {
  // 验证（纯逻辑）
  if (!userData.email) throw new Error('Email required');
  
  // 副作用：网络请求
  const user = await api.post('/users', userData);
  
  // 副作用：DOM 操作
  document.getElementById('message').innerText = 'Registration successful!';
  
  // 副作用：LocalStorage
  localStorage.setItem('user', JSON.stringify(user));
  
  return user;
}

// ✓ 副作用隔离
// 纯函数：验证
function validateUser(userData) {
  if (!userData.email) {
    throw new Error('Email required');
  }
}

// 副作用层：处理所有副作用
async function registerUser(userData) {
  validateUser(userData);  // 纯函数调用
  
  try {
    const user = await api.post('/users', userData);
    updateUI('Registration successful!');
    persistUser(user);
    return user;
  } catch (error) {
    handleError(error);
  }
}

// 副作用函数
function updateUI(message) {
  document.getElementById('message').innerText = message;
}

function persistUser(user) {
  localStorage.setItem('user', JSON.stringify(user));
}

function handleError(error) {
  console.error(error);
  showErrorMessage(error.message);
}
```

---

## 函数拆分策略

### 策略 1: 按步骤拆分

```javascript
// ✗ 复杂函数
function processOrder(order) {
  // 验证订单
  if (!order.items || order.items.length === 0) {
    throw new Error('Empty order');
  }
  
  // 计算总价
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }
  
  // 应用折扣
  if (order.couponCode) {
    const discount = getDiscount(order.couponCode);
    total = total * (1 - discount);
  }
  
  // 计算税费
  const tax = total * 0.08;
  total += tax;
  
  // 检查库存
  for (const item of order.items) {
    if (!checkStock(item.id)) {
      throw new Error(`Item ${item.id} out of stock`);
    }
  }
  
  // 创建订单记录
  const orderRecord = {
    id: generateId(),
    items: order.items,
    total,
    status: 'pending'
  };
  
  // 保存到数据库
  db.save('orders', orderRecord);
  
  // 扣减库存
  for (const item of order.items) {
    reduceStock(item.id, item.quantity);
  }
  
  return orderRecord;
}

// ✓ 按步骤拆分
function validateOrder(order) {
  if (!order.items || order.items.length === 0) {
    throw new Error('Empty order');
  }
}

function calculateSubtotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function applyDiscount(total, couponCode) {
  if (!couponCode) return total;
  const discount = getDiscount(couponCode);
  return total * (1 - discount);
}

function calculateTax(amount) {
  return amount * 0.08;
}

function checkInventory(items) {
  for (const item of items) {
    if (!checkStock(item.id)) {
      throw new Error(`Item ${item.id} out of stock`);
    }
  }
}

function createOrderRecord(items, total) {
  return {
    id: generateId(),
    items,
    total,
    status: 'pending'
  };
}

function updateInventory(items) {
  for (const item of items) {
    reduceStock(item.id, item.quantity);
  }
}

// 主函数 - 清晰易读
function processOrder(order) {
  validateOrder(order);
  const subtotal = calculateSubtotal(order.items);
  const afterDiscount = applyDiscount(subtotal, order.couponCode);
  const total = afterDiscount + calculateTax(afterDiscount);
  checkInventory(order.items);
  const orderRecord = createOrderRecord(order.items, total);
  db.save('orders', orderRecord);
  updateInventory(order.items);
  return orderRecord;
}
```

---

### 策略 2: 按职责拆分

```javascript
// ✗ 混合多个职责
function handleFormSubmit(formData) {
  // UI 验证
  if (!formData.email.includes('@')) {
    alert('Invalid email');
    return;
  }
  
  // 业务验证
  if (formData.password.length < 8) {
    throw new Error('Password too short');
  }
  
  // 数据转换
  const userData = {
    email: formData.email.toLowerCase(),
    password: hash(formData.password),
    createdAt: new Date()
  };
  
  // API 调用
  fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify(userData)
  });
  
  // UI 更新
  document.getElementById('form').reset();
  showSuccessMessage('Registration successful!');
}

// ✓ 按职责拆分
// UI 层
function handleFormSubmit(formData) {
  try {
    const uiValidation = validateUI(formData);
    if (!uiValidation.valid) {
      showValidationError(uiValidation.message);
      return;
    }
    
    const userData = transformFormData(formData);
    await submitToServer(userData);
    
    resetForm();
    showSuccessMessage('Registration successful!');
  } catch (error) {
    handleSubmissionError(error);
  }
}

// 验证层
function validateUI(formData) {
  if (!formData.email.includes('@')) {
    return { valid: false, message: 'Invalid email' };
  }
  return { valid: true };
}

function validateBusiness(userData) {
  if (userData.password.length < 8) {
    throw new Error('Password too short');
  }
}

// 转换层
function transformFormData(formData) {
  return {
    email: formData.email.toLowerCase(),
    password: hash(formData.password),
    createdAt: new Date()
  };
}

// 数据层
async function submitToServer(userData) {
  validateBusiness(userData);
  const response = await fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify(userData)
  });
  return response.json();
}

// UI 辅助函数
function showValidationError(message) { /* ... */ }
function showSuccessMessage(message) { /* ... */ }
function resetForm() { /* ... */ }
function handleSubmissionError(error) { /* ... */ }
```

---

### 策略 3: 提取通用逻辑

```javascript
// ✗ 重复代码
function fetchUsers() {
  setLoading(true);
  try {
    const users = await api.get('/users');
    setUsers(users);
    setError(null);
  } catch (error) {
    setError(error.message);
  } finally {
    setLoading(false);
  }
}

function fetchProducts() {
  setLoading(true);
  try {
    const products = await api.get('/products');
    setProducts(products);
    setError(null);
  } catch (error) {
    setError(error.message);
  } finally {
    setLoading(false);
  }
}

// ✓ 提取通用逻辑
async function fetchData(endpoint, setter) {
  setLoading(true);
  try {
    const data = await api.get(endpoint);
    setter(data);
    setError(null);
  } catch (error) {
    setError(error.message);
  } finally {
    setLoading(false);
  }
}

// 使用
function fetchUsers() {
  return fetchData('/users', setUsers);
}

function fetchProducts() {
  return fetchData('/products', setProducts);
}
```

---

## 参数设计

### 参数数量原则

**规则**: 参数不超过 3 个

```javascript
// ✗ 参数过多
function createUser(email, password, name, age, phone, address, city, country) {
  // ...
}

// ✓ 使用对象参数
function createUser({
  email,
  password,
  name,
  age,
  phone,
  address: {
    street,
    city,
    country
  }
}) {
  // ...
}
```

### 默认参数

```javascript
// ✓ 使用默认参数
function createOrder({
  items,
  currency = 'USD',
  taxRate = 0.08,
  discount = 0
}) {
  // ...
}
```

### 参数验证

```javascript
// ✓ 参数验证
function createUser({ email, password, name }) {
  if (!email || !password) {
    throw new Error('Email and password are required');
  }
  
  if (password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }
  
  // ...
}
```

---

## 函数组合

### 高阶函数

```javascript
// 函数作为参数
function withLogging(fn) {
  return function(...args) {
    console.log(`Calling ${fn.name} with`, args);
    const result = fn(...args);
    console.log(`Returned`, result);
    return result;
  };
}

// 使用
const loggedAdd = withLogging(function add(a, b) {
  return a + b;
});

loggedAdd(2, 3);
// Calling add with [2, 3]
// Returned 5
```

### 函数管道

```javascript
// 工具函数
const pipe = (...fns) => (x) => fns.reduce((v, f) => f(v), x);

// 纯函数
const trim = str => str.trim();
const toLowerCase = str => str.toLowerCase();
const validateEmail = email => email.includes('@');

// 组合使用
const processEmail = pipe(
  trim,
  toLowerCase,
  validateEmail
);

const result = processEmail('  USER@EXAMPLE.COM  ');
// true
```

---

## 命名规范

### 函数命名规则

```javascript
// ✓ 动词开头，描述行为
function getUser() { /* ... */ }
function calculateTotal() { /* ... */ }
function validateInput() { /* ... */ }
function handleSubmit() { /* ... */ }

// ✓ 布尔函数使用 is/has/should/can
function isValid() { /* ... */ }
function hasPermission() { /* ... */ }
function shouldUpdate() { /* ... */ }
function canEdit() { /* ... */ }

// ✓ 转换函数使用 to/as 前缀
function toUpperCase() { /* ... */ }
function asJSON() { /* ... */ }
```

---

## 学习建议

### 🌱 新手阶段

**重点掌握**:
- 函数的基本概念
- 参数和返回值
- 简单函数编写

**练习题目**:
1. 编写单一功能的函数
2. 练习参数验证
3. 使用有意义的命名

### 🚀 进阶阶段

**重点掌握**:
- 单一职责原则
- 纯函数设计
- 函数拆分技巧

**练习题目**:
1. 重构复杂函数
2. 将非纯函数改为纯函数
3. 实践函数组合

### 🏗️ 架构师阶段

**重点掌握**:
- 高阶函数
- 函数式编程模式
- 架构级函数设计

**练习题目**:
1. 设计函数库
2. 实现函数组合工具
3. 制定团队函数规范

---

## 注意事项

- **保持函数小巧**: 一个函数最好不超过 20 行
- **避免副作用**: 或明确隔离副作用
- **命名要清晰**: 函数名应该说明做什么
- **单一职责**: 一个函数只做一件事
- **可测试性**: 函数应该易于单元测试

---

## 版本历史

- **v1.0.0** (2025-01-XX): 初始版本
  - 创建函数设计子技能
  - 涵盖核心设计原则
  - 提供拆分策略和示例
  - 配置网络搜索能力
