---
name: naming
version: v1.0.0
author: skill-manager
parent_skill: software-design
description: 命名与注释规范子技能，提供变量命名、函数命名、类命名、注释技巧、文档规范等代码可读性提升策略
tags: [naming, comments, documentation, readability, semantic, conventions]
network_search: optional
---

# 命名与注释规范

## 任务目标

本子技能帮助开发者掌握命名艺术和注释技巧，提升代码的可读性和可维护性。

### 核心能力

- **变量命名**: 语义化、上下文清晰、避免歧义
- **函数命名**: 动词开头、描述行为、一致性
- **类命名**: 名词、大驼峰、职责清晰
- **注释技巧**: 解释为什么、避免冗余、TODO 管理
- **文档规范**: JSDoc、README、API 文档

---

## 命名原则

### 1. 名副其实

```javascript
// ✗ 无意义命名
let d = 10;  // d 是什么？
const x = true;  // x 表示什么？

// ✓ 有意义命名
let daysUntilExpiration = 10;
const isLoggedIn = true;
```

---

### 2. 避免歧义

```javascript
// ✗ 容易混淆
function getUserData() { /* 返回什么数据？ */ }
const list = [];  // list 包含什么？

// ✓ 清晰明确
function getActiveUserProfiles() { /* 清晰 */ }
const pendingOrderIds = [];  // 明确是订单 ID 列表
```

---

### 3. 使用领域术语

```javascript
// ✗ 通用命名
function calculate(a, b) { /* ... */ }

// ✓ 领域术语
function calculateMonthlyPayment(principal, interestRate, months) {
  // ...
}

// ✗ 技术术语
function processEntity(entity) { /* ... */ }

// ✓ 业务术语
function processCustomerOrder(order) {
  // ...
}
```

---

## 变量命名规范

### 1. 类型相关

```javascript
// 布尔值使用 is/has/should/can
const isValid = true;
const hasPermission = false;
const shouldUpdate = true;
const canEdit = false;

// 数组使用复数名词
const users = [];
const orderItems = [];
const productIds = [];

// 集合使用 Set/Map
const uniqueUserIds = new Set();
const userCache = new Map();

// 流/ Observable 使用$后缀
const click$ = new Subject();
const dataStream$ = observable;
```

---

### 2. 上下文相关

```javascript
// ✗ 丢失上下文
let count;  // 什么的 count？
let data;   // 什么 data？

// ✓ 完整上下文
let activeUserCount;
let customerOrderData;
let productInventoryList;

// 适度缩写（团队内公认）
const config = {};      // configuration
const params = {};      // parameters
const props = {};       // properties
const ctx = {};         // context
```

---

### 3. 避免魔法数字

```javascript
// ✗ 魔法数字
if (user.status === 1) { /* ... */ }
setTimeout(callback, 3000);
const price = item.price * 1.08;

// ✓ 使用命名常量
const USER_STATUS = {
  ACTIVE: 1,
  INACTIVE: 0,
  BANNED: -1
};

const REQUEST_TIMEOUT = 3000;
const TAX_RATE = 1.08;

if (user.status === USER_STATUS.ACTIVE) { /* ... */ }
setTimeout(callback, REQUEST_TIMEOUT);
const price = item.price * TAX_RATE;
```

---

## 函数命名规范

### 1. 动词开头

```javascript
// 获取数据
function getUser() { /* ... */ }
function fetchOrders() { /* ... */ }
function loadConfiguration() { /* ... */ }

// 创建数据
function createUser() { /* ... */ }
function generateReport() { /* ... */ }
function buildQueryString() { /* ... */ }

// 更新数据
function updateUser() { /* ... */ }
function modifySettings() { /* ... */ }
function updateConfiguration() { /* ... */ }

// 删除数据
function deleteUser() { /* ... */ }
function removeItem() { /* ... */ }
function clearCache() { /* ... */ }

// 检查验证
function isValid() { /* ... */ }
function hasPermission() { /* ... */ }
function canAccess() { /* ... */ }
function shouldUpdate() { /* ... */ }
```

---

### 2. 描述行为结果

```javascript
// ✗ 模糊
function handleData() { /* ... */ }
function doStuff() { /* ... */ }

// ✓ 清晰
function validateAndTransformUserData() { /* ... */ }
function processPaymentAndSendNotification() { /* ... */ }

// ✗ 不完整
function get() { /* ... */ }
function process() { /* ... */ }

// ✓ 完整
function getUserById() { /* ... */ }
function processOrderRefund() { /* ... */ }
```

---

### 3. 同步/异步命名

```javascript
// 同步函数
function getUser() { /* 立即返回 */ }

// 异步函数（返回 Promise）
async function getUserAsync() { /* ... */ }
async function fetchUser() { /* ... */ }

// 回调风格
function getUser(callback) { /* ... */ }
function loadUserData(done) { /* ... */ }

// Observable
function getUserStream() { /* 返回 Observable */ }
```

---

## 类命名规范

### 1. 大驼峰命名

```javascript
// ✓ 使用名词
class User { /* ... */ }
class Order { /* ... */ }
class Product { /* ... */ }

// ✓ 描述职责
class UserService { /* ... */ }
class OrderProcessor { /* ... */ }
class PaymentGateway { /* ... */ }

// ✓ 设计模式命名
class UserFactory { /* ... */ }
class OrderStrategy { /* ... */ }
class PaymentObserver { /* ... */ }
```

---

### 2. 避免冗余

```javascript
// ✗ 冗余
class UserClass { /* ... */ }
class UserManagerService { /* ... */ }

// ✓ 简洁
class User { /* ... */ }
class UserService { /* ... */ }
```

---

## 注释最佳实践

### 1. 解释为什么，而不是什么

```javascript
// ✗ 冗余注释
// 设置初始值为 0
let count = 0;

// 增加 count
count++;

// ✓ 解释原因
// 使用位运算提高性能，因为此函数会被频繁调用
const result = value << 2;

// 临时解决方案，等待 API 版本升级后移除
// TODO: 升级到 v2 API 后删除此兼容代码
if (apiVersion === 'v1') {
  // ...
}
```

---

### 2. 函数注释

```javascript
/**
 * 计算订单总价
 * 
 * @param {Order} order - 订单对象
 * @param {Object} options - 可选参数
 * @param {boolean} options.includeTax - 是否包含税费，默认 true
 * @param {boolean} options.applyDiscount - 是否应用折扣，默认 true
 * @returns {number} 订单总价（保留两位小数）
 * @throws {ValidationError} 当订单数据无效时
 * @throws {NotFoundError} 当商品不存在时
 * 
 * @example
 * const total = calculateOrderTotal(order, { includeTax: true });
 * 
 * @since 1.0.0
 * @author John Doe
 */
function calculateOrderTotal(order, options = {}) {
  // ...
}
```

---

### 3. 复杂逻辑注释

```javascript
// ✓ 解释算法思路
// 使用快速排序，因为数据量可能很大
// 时间复杂度：O(n log n)
function sortLargeDataset(data) {
  // ...
}

// ✓ 解释业务规则
// 根据会员等级应用不同折扣：
// - VIP: 7 折
// - Premium: 8 折
// - Regular: 9 折
// - Guest: 无折扣
function applyMembershipDiscount(price, membershipLevel) {
  // ...
}

// ✓ 解释边界情况
// 特殊处理：当用户 ID 为 0 时，表示系统管理员
if (userId === 0) {
  return grantAllPermissions();
}
```

---

### 4. TODO 注释管理

```javascript
// TODO: [优先级] [负责人] [截止日期] 描述

// TODO: [HIGH] [@John] [2025-02-01] 优化此算法，当前性能为 O(n²)
function findDuplicates(data) {
  // ...
}

// FIXME: [CRITICAL] [@Jane] 处理内存泄漏问题
function setupEventListeners() {
  // ...
}

// HACK: [LOW] [@All] 临时解决方案，等待第三方库更新
function workaround() {
  // ...
}

// NOTE: [INFO] [@All] 重要说明：此函数有副作用
function updateGlobalState() {
  // ...
}
```

---

## 文档规范

### 1. README 结构

```markdown
# 项目名称

简短描述（一句话）

## 功能特性

- 特性 1
- 特性 2
- 特性 3

## 快速开始

### 安装

```bash
npm install package-name
```

### 使用

```javascript
// 代码示例
import { feature } from 'package-name';
feature();
```

## API 文档

### 方法名

描述

**参数:**
- `param1` (类型) - 描述

**返回:**
类型 - 描述

**示例:**
```javascript
// 代码示例
```

## 开发指南

### 本地开发

```bash
git clone
npm install
npm run dev
```

### 测试

```bash
npm test
```

## 贡献指南

...

## 许可证

MIT
```

---

### 2. 代码示例文档

```javascript
/**
 * @file 用户管理模块
 * @description 提供用户 CRUD 操作、权限管理等功能
 * @module user
 * @requires axios
 * @requires lodash
 * 
 * @example
 * // 导入模块
 * import { UserService } from './user';
 * 
 * // 创建用户
 * const user = await UserService.create({
 *   name: 'John',
 *   email: 'john@example.com'
 * });
 * 
 * // 获取用户
 * const user = await UserService.getById(1);
 * 
 * // 更新用户
 * await UserService.update(1, { name: 'Jane' });
 * 
 * // 删除用户
 * await UserService.delete(1);
 */
```

---

## 命名检查清单

### 基础检查

- [ ] 名称是否清晰表达了意图？
- [ ] 是否有歧义或误导？
- [ ] 是否使用了领域术语？
- [ ] 是否符合团队规范？

### 变量命名

- [ ] 类型是否清晰（布尔值、数组等）？
- [ ] 上下文是否完整？
- [ ] 是否避免了魔法数字？

### 函数命名

- [ ] 是否以动词开头？
- [ ] 是否描述了行为？
- [ ] 同步/异步是否区分？

### 类命名

- [ ] 是否使用大驼峰？
- [ ] 是否是名词？
- [ ] 是否避免了冗余？

---

## 注意事项

- **一致性优先**: 团队内部保持一致最重要
- **适度缩写**: 使用公认的缩写，避免过度
- **重构命名**: 发现不好的命名及时重构
- **文档更新**: 代码变更后及时更新文档
- **工具辅助**: 使用 Linter 检查命名规范

---

## 版本历史

- **v1.0.0** (2025-01-XX): 初始版本
  - 创建命名与注释子技能
  - 涵盖命名规范和注释技巧
  - 提供文档编写指南
