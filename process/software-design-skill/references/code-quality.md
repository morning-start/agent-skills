---
name: code-quality
version: v1.0.0
author: skill-manager
parent_skill: software-design
description: 代码质量优化子技能，提供代码可读性、可维护性、可扩展性、可测试性、重构技巧等质量提升策略和最佳实践
tags: [code-quality, readability, maintainability, testability, refactoring, clean-code]
network_search: optional
---

# 代码质量优化

## 任务目标

本子技能帮助开发者编写高质量、可维护的代码，涵盖代码可读性、命名规范、注释技巧、重构方法、测试策略等核心内容。

### 核心能力

- **代码可读性**: 清晰命名、简洁结构、一致风格
- **可维护性**: 模块化、解耦、文档化
- **可扩展性**: 设计模式、开放封闭原则
- **可测试性**: 依赖注入、纯函数、测试覆盖
- **重构技巧**: 代码异味识别、重构方法

---

## 代码可读性

### 1. 语义化命名

```javascript
// ✗ 无意义命名
function calc(a, b, c) {
  return a * b * c;
}

// ✓ 语义化命名
function calculateVolume(length, width, height) {
  return length * width * height;
}

// ✗ 模糊命名
const data = fetchData();
const temp = process(data);

// ✓ 清晰命名
const userData = fetchUserData();
const validatedUser = validateUser(userData);
```

---

### 2. 函数长度控制

```javascript
// ✗ 过长函数（> 50 行）
function processOrder(order) {
  // 20 行验证逻辑
  // 30 行价格计算
  // 20 行库存检查
  // 20 行订单创建
  // 10 行邮件通知
  // ... 总共 100+ 行
}

// ✓ 拆分为小函数
function processOrder(order) {
  validateOrder(order);
  const total = calculateTotal(order);
  checkInventory(order.items);
  const orderRecord = createOrder(order, total);
  sendConfirmation(order);
  return orderRecord;
}

// 每个函数职责单一，易于理解和测试
```

---

### 3. 注释最佳实践

```javascript
// ✗ 冗余注释（代码已经说明）
// 设置计数器为 0
let count = 0;

// ✓ 解释为什么（而不是 what）
// 使用快速排序而非冒泡排序，因为数据量可能很大
function sortData(data) {
  return data.sort((a, b) => a - b);
}

// ✓ 警告和注意事项
// ⚠️ 注意：此函数有副作用，会修改全局状态
function updateGlobalCache(key, value) {
  globalCache[key] = value;
}

// ✓ TODO 注释
// TODO: 需要优化此算法，当前时间复杂度为 O(n²)
// FIXME: 处理边界情况时的 bug
// HACK: 临时解决方案，等待 API 更新后移除
```

---

## 代码一致性

### 1. 代码风格统一

```javascript
// ✓ 统一的代码风格
// 使用 2 个空格缩进
// 函数名使用驼峰命名
// 类名使用大驼峰
// 常量使用大写 + 下划线
// 文件使用小写 + 连字符

// .eslintrc.js 配置
module.exports = {
  rules: {
    indent: ['error', 2],
    'func-names': ['error', 'as-needed'],
    'camelcase': 'error',
    'no-const-assign': 'error'
  }
};
```

---

### 2. 错误处理一致性

```javascript
// ✓ 统一的错误处理模式
async function handleRequest(req, res, next) {
  try {
    await next();
  } catch (error) {
    if (error instanceof AppError) {
      handleAppError(error, res);
    } else if (error instanceof ValidationError) {
      handleValidationError(error, res);
    } else {
      handleUnexpectedError(error, res);
    }
  }
}
```

---

## 可维护性

### 1. 减少代码重复（DRY 原则）

```javascript
// ✗ 重复代码
function getUsers() {
  return fetch('/api/users').then(res => res.json());
}

function getProducts() {
  return fetch('/api/products').then(res => res.json());
}

function getOrders() {
  return fetch('/api/orders').then(res => res.json());
}

// ✓ 提取公共逻辑
async function fetchAPI(endpoint) {
  const response = await fetch(`/api/${endpoint}`);
  return response.json();
}

const getUsers = () => fetchAPI('users');
const getProducts = () => fetchAPI('products');
const getOrders = () => fetchAPI('orders');
```

---

### 2. 配置外部化

```javascript
// ✗ 硬编码
function connect() {
  return mongoose.connect('mongodb://localhost:27017/mydb');
}

function sendEmail(to) {
  return nodemailer.createTransport({
    host: 'smtp.example.com',
    port: 587
  });
}

// ✓ 配置外部化
const config = {
  database: process.env.DB_URI || 'mongodb://localhost:27017/mydb',
  email: {
    host: process.env.SMTP_HOST || 'smtp.example.com',
    port: parseInt(process.env.SMTP_PORT) || 587
  }
};

function connect() {
  return mongoose.connect(config.database);
}

function sendEmail(to) {
  return nodemailer.createTransport(config.email);
}
```

---

## 可测试性

### 1. 依赖注入

```javascript
// ✗ 难以测试
class UserService {
  constructor() {
    this.db = new Database();  // 硬编码依赖
  }
  
  async getUser(id) {
    return this.db.query('SELECT * FROM users WHERE id = ?', [id]);
  }
}

// ✓ 依赖注入
class UserService {
  constructor(database) {
    this.db = database;
  }
  
  async getUser(id) {
    return this.db.query('SELECT * FROM users WHERE id = ?', [id]);
  }
}

// 测试时使用 mock
const mockDb = {
  query: jest.fn().mockResolvedValue({ id: 1, name: 'Test' })
};
const service = new UserService(mockDb);
```

---

### 2. 纯函数优先

```javascript
// ✓ 纯函数易于测试
function calculateDiscount(price, discountRate) {
  return price * (1 - discountRate);
}

// 测试
test('calculate 10% discount', () => {
  expect(calculateDiscount(100, 0.1)).toBe(90);
});

// ✗ 非纯函数难以测试
let discountRate = 0.1;
function calculateDiscount(price) {
  return price * (1 - discountRate);  // 依赖外部状态
}
```

---

## 重构技巧

### 1. 识别代码异味

```javascript
// 🚩 过长的函数
function processOrder() { /* 200 行代码 */ }

// 🚩 过大的类
class GodClass { /* 管理所有业务逻辑 */ }

// 🚩 重复代码
// 在多个地方看到相同的代码块

// 🚩 过深的嵌套
if (condition1) {
  if (condition2) {
    if (condition3) {
      // ...
    }
  }
}

// 🚩 过多的参数
function createUser(name, email, age, phone, address, city, country, zip) {
  // ...
}
```

---

### 2. 重构方法

```javascript
// 方法 1: 提取函数
// Before
function printInvoice(order) {
  // 计算总价
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }
  // 打印
  console.log('Total:', total);
}

// After
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function printInvoice(order) {
  const total = calculateTotal(order.items);
  console.log('Total:', total);
}

// 方法 2: 提前返回
// Before
function processUser(user) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission) {
        // 处理逻辑
      }
    }
  }
}

// After
function processUser(user) {
  if (!user) return;
  if (!user.isActive) return;
  if (!user.hasPermission) return;
  
  // 处理逻辑
}

// 方法 3: 替换临时变量
// Before
function getFullName(user) {
  const firstName = user.firstName;
  const lastName = user.lastName;
  const fullName = `${firstName} ${lastName}`;
  return fullName;
}

// After
function getFullName(user) {
  return `${user.firstName} ${user.lastName}`;
}
```

---

## SOLID 原则应用

### 1. 单一职责（SRP）

```javascript
// ✗ 违反 SRP
class User {
  save() { /* 保存到数据库 */ }
  validate() { /* 验证数据 */ }
  sendEmail() { /* 发送邮件 */ }
}

// ✓ 遵循 SRP
class User { /* 数据模型 */ }
class UserRepository { save() { /* ... */ } }
class UserValidator { validate() { /* ... */ } }
class EmailService { sendEmail() { /* ... */ } }
```

---

### 2. 开放封闭（OCP）

```javascript
// ✗ 违反 OCP
function calculateDiscount(user, type) {
  if (type === 'vip') {
    return user.price * 0.7;
  } else if (type === 'premium') {
    return user.price * 0.8;
  } else if (type === 'regular') {
    return user.price * 0.9;
  }
  // 新增类型需要修改此函数
}

// ✓ 遵循 OCP
class DiscountStrategy {
  calculate(price) { /* ... */ }
}

class VIPDiscount extends DiscountStrategy {
  calculate(price) { return price * 0.7; }
}

class PremiumDiscount extends DiscountStrategy {
  calculate(price) { return price * 0.8; }
}

// 新增类型只需添加新类，无需修改现有代码
```

---

## 代码审查清单

### 可读性

- [ ] 命名清晰且有意义
- [ ] 函数长度合理（< 50 行）
- [ ] 注释解释了"为什么"
- [ ] 代码格式一致

### 可维护性

- [ ] 没有重复代码（DRY）
- [ ] 职责分离清晰（SRP）
- [ ] 配置外部化
- [ ] 错误处理完善

### 可测试性

- [ ] 依赖可注入
- [ ] 纯函数优先
- [ ] 边界条件考虑
- [ ] 测试覆盖率高

### 性能

- [ ] 没有明显的性能问题
- [ ] 使用了合适的数据结构
- [ ] 避免了不必要的计算
- [ ] 资源正确释放

---

## 注意事项

- **渐进式改进**: 不要一次性重构所有代码
- **测试保护**: 重构前确保有测试覆盖
- **小步快跑**: 每次重构只做一件事
- **代码审查**: 通过 review 保证质量
- **工具辅助**: 使用 Linter、Formatter 等工具

---

## 版本历史

- **v1.0.0** (2025-01-XX): 初始版本
  - 创建代码质量子技能
  - 涵盖代码质量维度
  - 提供重构技巧和最佳实践
