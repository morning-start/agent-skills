---
name: modularization
version: v1.0.0
author: skill-manager
parent_skill: software-design
description: 模块化与架构设计子技能，提供分层架构、目录规范、代码组织、高内聚低耦合等架构设计原则和最佳实践
tags: [modularization, architecture, layering, directory-structure, cohesion, coupling]
network_search: optional
---

# 模块化与架构设计

## 任务目标

本子技能帮助开发者设计清晰、可维护的代码架构，涵盖模块化设计、分层架构、目录组织、依赖管理等核心内容。

### 核心能力

- **模块化设计**: 高内聚、低耦合、单一职责
- **分层架构**: Controller / Service / DAO / Utils
- **目录规范**: 按功能/按类型组织代码
- **依赖管理**: 模块间通信、依赖注入
- **代码组织**: 文件结构、导出策略
- **架构模式**: MVC、MVVM、Clean Architecture

---

## 三步流程框架

```
┌─────────────────────────────────────────────────────────────┐
│  第一步：查阅信息 (Research)                                  │
│  ├── 分析项目规模和需求                                      │
│  ├── 识别架构痛点和挑战                                      │
│  └── 选择合适的架构模式                                      │
├─────────────────────────────────────────────────────────────┤
│  第二步：执行操作 (Execute)                                   │
│  ├── 设计模块化架构                                          │
│  ├── 组织目录结构                                            │
│  ├── 定义模块边界和接口                                      │
│  └── 实现依赖管理                                            │
├─────────────────────────────────────────────────────────────┤
│  第三步：检查验收 (Validate)                                  │
│  ├── 验证模块独立性                                          │
│  ├── 检查依赖关系合理性                                      │
│  └── 评估可扩展性和可维护性                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 模块化设计原则

### 1. 高内聚（High Cohesion）

**原则**: 相关的代码应该组织在一起

```javascript
// ✗ 低内聚 - 功能分散
// utils.js
function validateUser() { /* ... */ }
function calculatePrice() { /* ... */ }
function sendEmail() { /* ... */ }

// services.js
function createUser() { /* ... */ }
function applyDiscount() { /* ... */ }

// ✓ 高内聚 - 按功能组织
// user/
//   - user.validation.js
//   - user.service.js
//   - user.email.js

// order/
//   - order.pricing.js
//   - order.discount.js
//   - order.service.js
```

---

### 2. 低耦合（Low Coupling）

**原则**: 模块间依赖应该最小化

```javascript
// ✗ 高耦合 - 直接依赖具体实现
class OrderService {
  constructor() {
    this.database = new MySQLDatabase();  // 紧耦合
    this.email = new SMTPEmailService();  // 紧耦合
  }
}

// ✓ 低耦合 - 依赖抽象
class OrderService {
  constructor(database, emailService) {
    this.database = database;      // 依赖接口
    this.email = emailService;     // 依赖接口
  }
}

// 使用时注入依赖
const orderService = new OrderService(
  new MySQLDatabase(),
  new SMTPEmailService()
);
```

---

## 分层架构模式

### 经典三层架构

```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│         (Controller / View)         │
│    - 处理用户输入                   │
│    - 展示数据                       │
├─────────────────────────────────────┤
│         Business Logic Layer        │
│           (Service)                 │
│    - 业务规则                       │
│    - 业务逻辑                       │
├─────────────────────────────────────┤
│         Data Access Layer           │
│            (DAO / Repository)       │
│    - 数据持久化                     │
│    - 数据库操作                     │
└─────────────────────────────────────┘
```

### 代码示例

```javascript
// ============ Data Access Layer ============
// repositories/user.repository.js
class UserRepository {
  async findById(id) {
    return db.query('SELECT * FROM users WHERE id = ?', [id]);
  }
  
  async save(user) {
    return db.query('INSERT INTO users VALUES (?)', [user]);
  }
}

// ============ Business Logic Layer ============
// services/user.service.js
class UserService {
  constructor(userRepository, emailService) {
    this.userRepository = userRepository;
    this.emailService = emailService;
  }
  
  async register(userData) {
    // 业务验证
    this.validateUserData(userData);
    
    // 密码加密
    const hashedPassword = await this.hashPassword(userData.password);
    
    // 保存用户
    const user = await this.userRepository.save({
      ...userData,
      password: hashedPassword
    });
    
    // 发送欢迎邮件
    await this.emailService.sendWelcome(user.email);
    
    return user;
  }
  
  validateUserData(userData) {
    if (!userData.email) {
      throw new Error('Email required');
    }
  }
  
  async hashPassword(password) {
    // 密码加密逻辑
  }
}

// ============ Presentation Layer ============
// controllers/user.controller.js
class UserController {
  constructor(userService) {
    this.userService = userService;
  }
  
  async register(req, res) {
    try {
      const userData = req.body;
      const user = await this.userService.register(userData);
      res.status(201).json(user);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }
}
```

---

## 目录组织结构

### 方案 1: 按类型组织（适合小型项目）

```
src/
├── controllers/
│   ├── user.controller.js
│   └── order.controller.js
├── services/
│   ├── user.service.js
│   └── order.service.js
├── repositories/
│   ├── user.repository.js
│   └── order.repository.js
├── models/
│   ├── user.model.js
│   └── order.model.js
├── utils/
│   ├── logger.js
│   └── validator.js
└── index.js
```

**优点**:
- ✅ 结构清晰，易于理解
- ✅ 同类型代码集中
- ✅ 适合小型项目

**缺点**:
- ❌ 功能分散，查找困难
- ❌ 新增功能需修改多个目录

---

### 方案 2: 按功能组织（推荐）

```
src/
├── user/
│   ├── user.controller.js
│   ├── user.service.js
│   ├── user.repository.js
│   ├── user.model.js
│   └── user.routes.js
├── order/
│   ├── order.controller.js
│   ├── order.service.js
│   ├── order.repository.js
│   ├── order.model.js
│   └── order.routes.js
├── shared/
│   ├── middleware/
│   ├── utils/
│   └── constants/
└── index.js
```

**优点**:
- ✅ 功能内聚，易于维护
- ✅ 新增功能只需添加模块
- ✅ 适合中大型项目

**缺点**:
- ❌ 可能有代码重复
- ❌ 需要良好的模块边界

---

### 方案 3: 混合组织（大型项目）

```
src/
├── modules/
│   ├── user/
│   │   ├── application/      # 应用层
│   │   │   └── user.service.js
│   │   ├── domain/           # 领域层
│   │   │   ├── user.model.js
│   │   │   └── user.repository.interface.js
│   │   └── infrastructure/   # 基础设施层
│   │       ├── user.repository.impl.js
│   │       └── user.controller.js
│   └── order/
│       └── ...
├── shared/
│   ├── kernel/               # 核心抽象
│   ├── middleware/
│   └── utils/
└── index.js
```

**优点**:
- ✅ 清晰的职责分离
- ✅ 高度可维护
- ✅ 适合大型团队

**缺点**:
- ❌ 结构复杂
- ❌ 学习曲线陡峭

---

## 模块导出策略

### 1. 统一导出（推荐）

```javascript
// user/index.js
export { default as UserController } from './user.controller.js';
export { default as UserService } from './user.service.js';
export { default as UserRepository } from './user.repository.js';
export { default as User } from './user.model.js';

// 使用
import { UserController, UserService } from '@/user';
```

---

### 2. 命名导出

```javascript
// user/user.service.js
export class UserService { /* ... */ }
export function validateUser() { /* ... */ }
export const USER_ROLES = { /* ... */ };

// 使用
import { UserService, validateUser, USER_ROLES } from './user.service.js';
```

---

### 3. 默认导出（谨慎使用）

```javascript
// user/user.service.js
export default class UserService { /* ... */ }

// 使用
import UserService from './user.service.js';
```

---

## 依赖管理

### 依赖注入模式

```javascript
// 容器模式
class Container {
  constructor() {
    this.services = new Map();
  }
  
  register(name, service) {
    this.services.set(name, service);
  }
  
  get(name) {
    return this.services.get(name);
  }
}

// 注册服务
const container = new Container();
container.register('database', new MySQLDatabase());
container.register('email', new SMTPEmailService());
container.register('userRepository', new UserRepository(
  container.get('database')
));
container.register('userService', new UserService(
  container.get('userRepository'),
  container.get('email')
));

// 使用
const userService = container.get('userService');
```

---

## 代码组织最佳实践

### 1. 文件命名规范

```javascript
// ✓ 使用小写和连字符
user.service.js
user.controller.js
user.model.js

// ✓ 使用描述性名称
email.validator.js
password.hasher.js
order.processor.js
```

---

### 2. 文件大小控制

```javascript
// ✓ 单个文件不超过 300 行
// 如果超过，考虑拆分

// ✗ user.service.js (800 行)
// 包含太多职责

// ✓ 拆分
user.service.js          // 主服务 (150 行)
user.validation.service.js   // 验证逻辑 (100 行)
user.email.service.js        // 邮件逻辑 (120 行)
user.password.service.js     // 密码逻辑 (100 行)
```

---

### 3. 导入组织

```javascript
// ✓ 按类型分组导入
// 1. 第三方库
import express from 'express';
import _ from 'lodash';

// 2. 内部模块
import { UserService } from '@/user';
import { OrderService } from '@/order';

// 3. 相对路径
import { helper } from './utils/helper';
import { constants } from '../constants';

// 4. 样式文件
import './styles.scss';
```

---

## 架构模式对比

### MVC（Model-View-Controller）

**适用**: Web 应用、前后端分离

```
User Action → Controller → Model → View → User
```

---

### MVVM（Model-View-ViewModel）

**适用**: 前端框架（Vue、Angular）

```
View ↔ ViewModel ↔ Model
```

---

### Clean Architecture

**适用**: 大型复杂系统

```
Entities → Use Cases → Interface Adapters → Frameworks & Drivers
```

---

## 学习建议

### 🌱 新手阶段

**重点掌握**:
- 基础目录结构
- 简单的模块化
- 文件组织规范

**练习题目**:
1. 按功能组织代码
2. 实现简单的分层
3. 使用统一的导出方式

### 🚀 进阶阶段

**重点掌握**:
- 依赖注入
- 模块边界设计
- 架构模式应用

**练习题目**:
1. 实现三层架构
2. 应用依赖注入
3. 设计模块接口

### 🏗️ 架构师阶段

**重点掌握**:
- Clean Architecture
- 微服务架构
- 领域驱动设计

**练习题目**:
1. 设计大型系统架构
2. 实现领域驱动设计
3. 制定架构规范

---

## 注意事项

- **避免过度设计**: 根据项目规模选择合适的架构
- **保持一致性**: 整个项目使用统一的组织方式
- **文档化**: 记录架构决策和模块职责
- **逐步演进**: 架构应该随项目发展而演进
- **测试友好**: 架构应该便于单元测试

---

## 版本历史

- **v1.0.0** (2025-01-XX): 初始版本
  - 创建模块化与架构子技能
  - 涵盖主流架构模式
  - 提供目录组织方案
  - 配置网络搜索能力
