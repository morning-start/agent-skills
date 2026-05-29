# 数据库设计文档模板

## 文档概述
- **项目名称**：[项目名称]
- **数据库类型**：MySQL 8.0 / PostgreSQL 14 / Oracle 19c
- **字符集**：utf8mb4
- **存储引擎**：InnoDB
- **文档版本**：v1.0.0

---

## 1. 数据库概览

### 1.1 表清单
| 表名 | 中文名 | 所属模块 | 说明 |
|------|--------|----------|------|
| tb_user | 用户表 | 用户模块 | 存储用户基本信息 |
| tb_order | 订单表 | 订单模块 | 存储订单信息 |
| tb_order_item | 订单明细表 | 订单模块 | 存储订单商品明细 |
| tb_product | 商品表 | 商品模块 | 存储商品信息 |

### 1.2 ER 关系图
```
tb_user (1) ----< (n) tb_order
tb_order (1) ----< (n) tb_order_item
tb_product (1) ----< (n) tb_order_item
```

---

## 2. 表结构详情

### 2.1 tb_user（用户表）

#### 2.1.1 表信息
- **表名**：`tb_user`
- **中文注释**：用户基本信息表
- **所属模块**：用户模块
- **存储引擎**：InnoDB
- **字符集**：utf8mb4

#### 2.1.2 字段列表
| 字段名 | 类型 | 必填 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|------|------|
| id | BIGINT | 是 | - | 用户 ID（主键） | PK |
| username | VARCHAR(32) | 是 | - | 用户名（唯一） | UK |
| password | VARCHAR(64) | 是 | - | 密码（加密） | - |
| email | VARCHAR(64) | 是 | - | 邮箱地址（唯一） | UK |
| phone | VARCHAR(20) | 否 | - | 手机号（唯一） | UK |
| avatar | VARCHAR(255) | 否 | - | 头像 URL | - |
| status | TINYINT | 是 | 1 | 状态（0-禁用, 1-正常, 2-锁定） | IDX |
| created_at | DATETIME | 是 | NOW() | 创建时间 | IDX |
| updated_at | DATETIME | 是 | NOW() | 更新时间 | - |

#### 2.1.3 数据字典

**status（用户状态）**：
| 值 | 说明 |
|----|------|
| 0 | 禁用（无法登录） |
| 1 | 正常 |
| 2 | 锁定（异常登录，需解锁） |

#### 2.1.4 索引说明
- **主键索引**：`id`
- **唯一索引**：`username`, `email`, `phone`
- **普通索引**：`status`, `created_at`
- **联合索引**：(username, status) - 用于按用户名和状态查询

#### 2.1.5 DDL 语句
```sql
CREATE TABLE `tb_user` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '用户 ID',
  `username` VARCHAR(32) NOT NULL COMMENT '用户名',
  `password` VARCHAR(64) NOT NULL COMMENT '密码',
  `email` VARCHAR(64) NOT NULL COMMENT '邮箱',
  `phone` VARCHAR(20) DEFAULT NULL COMMENT '手机号',
  `avatar` VARCHAR(255) DEFAULT NULL COMMENT '头像 URL',
  `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态（0-禁用, 1-正常, 2-锁定）',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  UNIQUE KEY `uk_email` (`email`),
  UNIQUE KEY `uk_phone` (`phone`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_username_status` (`username`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户基本信息表';
```

---

### 2.2 tb_order（订单表）

#### 2.2.1 表信息
- **表名**：`tb_order`
- **中文注释**：订单信息表
- **所属模块**：订单模块

#### 2.2.2 字段列表
| 字段名 | 类型 | 必填 | 默认值 | 说明 | 索引 |
|--------|------|------|--------|------|------|
| id | BIGINT | 是 | - | 订单 ID（主键） | PK |
| order_no | VARCHAR(32) | 是 | - | 订单号（唯一） | UK |
| user_id | BIGINT | 是 | - | 用户 ID（外键） | IDX |
| total_amount | DECIMAL(10,2) | 是 | 0.00 | 订单总金额 | - |
| status | TINYINT | 是 | 0 | 订单状态 | IDX |
| pay_time | DATETIME | 否 | - | 支付时间 | - |
| created_at | DATETIME | 是 | NOW() | 创建时间 | IDX |

#### 2.2.3 数据字典

**status（订单状态）**：
| 值 | 说明 |
|----|------|
| 0 | 待支付 |
| 1 | 已支付 |
| 2 | 已发货 |
| 3 | 已完成 |
| 4 | 已取消 |
| 5 | 退款中 |
| 6 | 已退款 |

**状态流转规则**：
- 0（待支付）→ 1（已支付）：支付成功
- 0（待支付）→ 4（已取消）：取消订单
- 1（已支付）→ 2（已发货）：发货
- 2（已发货）→ 3（已完成）：确认收货
- 1（已支付）→ 5（退款中）：申请退款
- 5（退款中）→ 6（已退款）：退款成功

#### 2.2.4 索引说明
- **主键索引**：`id`
- **唯一索引**：`order_no`
- **普通索引**：`user_id`, `status`, `created_at`
- **联合索引**：(user_id, created_at) - 用于查询用户订单列表

#### 2.2.5 DDL 语句
```sql
CREATE TABLE `tb_order` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '订单 ID',
  `order_no` VARCHAR(32) NOT NULL COMMENT '订单号',
  `user_id` BIGINT NOT NULL COMMENT '用户 ID',
  `total_amount` DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '订单总金额',
  `status` TINYINT NOT NULL DEFAULT 0 COMMENT '订单状态（0-待支付, 1-已支付, 2-已发货, 3-已完成, 4-已取消, 5-退款中, 6-已退款）',
  `pay_time` DATETIME DEFAULT NULL COMMENT '支付时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_user_created` (`user_id`, `created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单信息表';
```

---

## 3. 分库分表方案（如适用）

### 3.1 分片策略
- **分片表**：`tb_order`, `tb_order_item`
- **分片键**：`user_id`
- **分片算法**：哈希取模（user_id % 4）
- **分片数量**：4 个分库，每个分库 16 张表（共 64 张表）

### 3.2 分片说明
```
db_order_0 (user_id % 4 == 0)
  - tb_order_0000 ~ tb_order_0015
db_order_1 (user_id % 4 == 1)
  - tb_order_0000 ~ tb_order_0015
db_order_2 (user_id % 4 == 2)
  - tb_order_0000 ~ tb_order_0015
db_order_3 (user_id % 4 == 3)
  - tb_order_0000 ~ tb_order_0015
```

### 3.3 跨分片查询限制
- 不支持跨分片的 JOIN 查询
- 不支持跨分片的排序和分页
- 需要在应用层进行数据聚合

---

## 4. 数据迁移与备份

### 4.1 备份策略
- **全量备份**：每天凌晨 2:00 执行
- **增量备份**：每小时执行一次
- **备份保留**：保留最近 30 天的备份

### 4.2 数据迁移
- **迁移工具**：mysqldump / DataX
- **迁移步骤**：
  1. 导出源库数据
  2. 数据清洗和转换
  3. 导入目标库
  4. 数据校验

---

## 5. 注意事项

1. 所有表必须包含 `id`（主键）、`created_at`（创建时间）、`updated_at`（更新时间）
2. 时间字段统一使用 `DATETIME` 类型，存储 UTC+8 时间
3. 金额字段统一使用 `DECIMAL(10,2)` 类型，单位：元
4. 枚举类型字段必须在数据字典中说明
5. 外键关联建议在应用层维护，不使用数据库外键约束
6. 大字段（TEXT/BLOB）尽量拆分到子表，避免影响查询性能
7. 索引数量不宜过多，单表建议不超过 5 个索引
