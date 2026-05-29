---
name: rust-domain-design-skill
description: Rust Layer 2 技能 - 领域设计，核心问题：这个概念在领域中扮演什么角色？掌握 DDD、Entity、Value Object 等领域建模概念
version: 1.0.0
layer: 2
trigger: DDD, entity, value object, aggregate, domain model, bounded context
---

# Rust Domain Design - Layer 2

## 核心问题

这个概念在领域中扮演什么角色？

## 元认知追溯

```
问题 → Layer 2: 设计模式
        ↓
识别领域概念 → Layer 3: 领域专家知识
        ↓
Rust 类型实现 → Layer 1: 语言机制
```

## 领域驱动设计概念

### Entity - 有唯一标识

```rust
// 实体：身份最重要
#[derive(Debug, Clone)]
struct User {
    id: UserId,       // 唯一标识
    email: Email,
    created_at: DateTime<Utc>,
}

// 身份比较
impl PartialEq for User {
    fn eq(&self, other: &Self) -> bool {
        self.id == other.id
    }
}
```

### Value Object - 无身份，仅属性

```rust
// 值对象：属性组合
#[derive(Debug, Clone, PartialEq)]
struct Money {
    amount: Decimal,
    currency: Currency,
}

// 无身份，通过属性判断相等
let m1 = Money::new(100, USD);
let m2 = Money::new(100, USD);
assert_eq!(m1, m2);
```

### Aggregate - 边界内一致性

```rust
// 聚合根：外部访问的入口
struct Order {
    id: OrderId,
    customer_id: CustomerId,
    items: Vec<OrderItem>,
    status: OrderStatus,
}

impl Order {
    fn add_item(&mut self, item: OrderItem) -> Result<(), OrderError> {
        if self.status != OrderStatus::Draft {
            return Err(OrderError::CannotModify);
        }
        self.items.push(item);
        Ok(())
    }
}

// 外部代码只能通过 Order 操作
```

### Domain Service - 无状态操作

```rust
// 领域服务：跨多个聚合的操作
struct PricingService;

impl PricingService {
    fn calculate_total(
        &self,
        items: &[OrderItem],
        discount: Discount,
    ) -> Money {
        let subtotal = items.iter().map(|i| i.subtotal()).sum();
        discount.apply(subtotal)
    }
}
```

## Rust 实现模式

### 防止无效状态

```rust
// 编译时防止无效状态
struct Percentage(u8);

impl Percentage {
    fn new(value: u8) -> Option<Self> {
        if value <= 100 {
            Some(Percentage(value))
        } else {
            None
        }
    }
}

// Percentage::new(150) // 返回 None
```

### 命令与查询分离

```rust
// 命令：修改状态
struct CreateUserCommand {
    email: String,
    name: String,
}

// 查询：只读操作
trait UserRepository {
    fn find_by_id(&self, id: UserId) -> Option<User>;
    fn find_by_email(&self, email: &Email) -> Option<User>;
}
```

## 与其他技能关联

- rust-type-driven-skill: 类型编码领域规则
- rust-error-handling-skill: 领域错误处理
- rust-lifecycle-skill: 领域对象生命周期

## 资源索引

- [DDD in Rust](https://alexn.org/blog/rust/ddd/)
- [Rust Domain Modeling](https://www.amazon.com/Domain-Modeling-Made-Functional-Domain-Driven/dp/1680502539)

## 注意事项

- 区分 Entity 和 Value Object：身份 vs 属性
- 聚合边界内的对象保持一致性
- 使用类型防止无效状态，而非运行时检查
