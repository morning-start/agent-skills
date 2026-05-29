---
name: "tech-design"
description: "技术设计与UI细化工具。用于开发前的架构设计和接口约定，包括数据库设计、API定义、技术选型。适用于开发前的最后准备阶段。"
---

# 技术设计与UI细化

开发前的"最后准备"，确保地基稳固。

## 核心模块

```
UI/UX设计 → 技术架构设计 → 接口文档编写
```

---

## 1. UI/UX 设计细化

### 设计输出物清单

| 输出物 | 说明 | 接收方 |
|--------|------|--------|
| 高保真设计稿 | 标注颜色、字体、间距 | 前端开发 |
| 切图资源 | 按分辨率/设备分类 | 前端开发 |
| 交互说明 | 动画、转场、状态变化 | 前端开发 |
| 原型图 | 流程和页面跳转 | 全团队 |

### 设计评审checklist

- [ ] 关键页面是否覆盖所有状态（默认、hover、disabled、loading、空数据）
- [ ] 移动端适配是否考虑
- [ ] 交互反馈是否明确

---

## 2. 技术架构设计

### 数据库设计（ER图）

```
实体命名规范：
- 表名：t_模块名（英文下划线分隔）
- 字段：f_字段名
- 主键：id
- 外键：fk_关联表名

示例：
t_order (订单表)
├── id (主键)
├── f_order_no (订单号)
├── f_user_id (用户ID，外键)
├── f_total_amount (总价)
├── f_status (状态)
└── f_created_at (创建时间)
```

### 技术选型决策表

| 层级 | 选项 | 选型 | 理由 |
|------|------|------|------|
| 前端框架 | React/Vue/Angular | Vue | 学习成本低生态好 |
| 后端框架 | SpringBoot/Express | SpringBoot | 团队熟悉 |
| 数据库 | MySQL/PostgreSQL | MySQL | 轻量易维护 |
| 缓存 | Redis/Memcached | Redis | 支持持久化 |

---

## 3. API 接口文档

### RESTful API规范

```
命名规范：
- GET    /users        获取用户列表
- GET    /users/:id    获取单个用户
- POST   /users        创建用户
- PUT    /users/:id    更新用户
- DELETE /users/:id    删除用户
```

### 接口文档模板

```json
{
  "apiName": "创建订单",
  "url": "/api/orders",
  "method": "POST",
  "request": {
    "userId": "string (必填) 用户ID",
    "items": "array (必填) 订单商品列表",
    "remark": "string (可选) 备注"
  },
  "response": {
    "code": "200 表示成功",
    "data": {
      "orderId": "string 订单ID",
      "totalAmount": "number 总价"
    }
  }
}
```

---

## 使用场景

- 开发启动前的技术评审
- 前后端并行开发前的接口约定
- 技术方案选型讨论

## 关键产出

1. 数据库ER图/表结构文档
2. 技术选型决策表
3. API接口文档
4. UI设计稿评审记录
