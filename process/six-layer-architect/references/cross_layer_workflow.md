# 六层架构贯穿式修改工作流

## 目录

1. [工作流概述](#工作流概述)
2. [入口层识别指南](#入口层识别指南)
3. [修改影响推导](#修改影响推导)
4. [贯穿式修改模式](#贯穿式修改模式)
5. [跨层一致性校验](#跨层一致性校验)
6. [完整示例](#完整示例)

---

## 工作流概述

### 什么是贯穿式修改

贯穿式修改是指：当用户从六层架构的任意一层提出修改需求时，自动推导并协调其他五层进行配合修改，确保整个架构的一致性和完整性。

### 核心思想

```
用户提出修改
    ↓
识别入口层（从哪层开始）
    ↓
推导影响范围（影响哪些层）
    ↓
执行贯穿修改（逐层配合）
    ↓
一致性校验（确保对齐）
```

### 适用场景

- **新增字段**：如"添加用户手机号"
- **修改字段**：如"用户名字段从可选改为必填"
- **添加功能**：如"支持文章标签功能"
- **修改逻辑**：如"订单创建时检查库存"
- **接口变更**：如"API 增加分页参数"

---

## 入口层识别指南

### 关键词映射表

| 关键词类别 | 具体关键词 | 识别为入口层 |
|-----------|-----------|-------------|
| **界面相关** | 页面、界面、显示、展示、看到、输入框、按钮、表单、列表 | **UI 层** |
| **状态相关** | Store、状态、缓存、持久化、登录态、全局数据 | **前端服务层** |
| **前端调用** | 前端调用、API 接口、请求、获取数据、发送数据 | **前端 API 层** |
| **后端接口** | 后端接口、API 返回、路由、Endpoint、Controller | **后端 API 层** |
| **业务逻辑** | 业务逻辑、数据处理、验证、计算、检查 | **后端服务层** |
| **数据存储** | 数据库、表结构、字段、模型、Model、迁移 | **数据层** |

### 识别示例

| 用户原话 | 关键词分析 | 入口层 |
|---------|-----------|--------|
| "用户详情页要显示注册时间" | 页面、显示 | UI 层 |
| "登录状态需要在刷新后保持" | 状态、持久化 | 前端服务层 |
| "前端需要调用获取订单列表接口" | 前端调用、接口 | 前端 API 层 |
| "用户列表接口需要支持分页" | 接口、分页 | 后端 API 层 |
| "订单创建时要检查库存" | 业务逻辑、检查 | 后端服务层 |
| "用户表需要添加手机号字段" | 表、字段 | 数据层 |

---

## 修改影响推导

### 六层数据流图

```
┌─────────────────────────────────────────────────────────────┐
│                         数据流向                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   前端三层（Frontend）                                       │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│   │  UI 层   │───▶│ 前端服务 │───▶│ 前端 API │              │
│   │(Vue3)    │    │(Pinia)   │    │(Axios)   │              │
│   └──────────┘    └──────────┘    └────┬─────┘             │
│                                        │                    │
│                              HTTP Request                   │
│                                        │                    │
│                              HTTP Response                  │
│                                        │                    │
│                                        ▼                    │
│   后端三层（Backend）                                        │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│   │ 后端 API │───▶│ 后端服务 │───▶│  数据层  │              │
│   │(FastAPI) │    │(Service) │    │(SQLAlch) │              │
│   └──────────┘    └──────────┘    └──────────┘             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 修改影响推导矩阵

| 入口层 | 向前推导（→ UI） | 向后推导（→ DB） |
|--------|-----------------|-----------------|
| **UI 层** | 无（最前端） | UI → 前端服务 → 前端 API → 后端 API → 后端服务 → 数据层 |
| **前端服务层** | ← UI | → 前端 API → 后端 API → 后端服务 → 数据层 |
| **前端 API 层** | ← 前端服务 ← UI | → 后端 API → 后端服务 → 数据层 |
| **后端 API 层** | ← 前端 API ← 前端服务 ← UI | → 后端服务 → 数据层 |
| **后端服务层** | ← 后端 API ← 前端 API ← 前端服务 ← UI | → 数据层 |
| **数据层** | ← 后端服务 ← 后端 API ← 前端 API ← 前端服务 ← UI | 无（最后端） |

### 推导原则

1. **向前推导**：某层修改后，前面的层需要配合调整以使用新功能
2. **向后推导**：某层修改后，后面的层需要提供支持以实现该功能
3. **双向推导**：中间层修改时，需要同时向前和向后推导

---

## 贯穿式修改模式

### 模式 A：从 UI 层开始（向前无依赖，向后全推导）

**场景**：用户从界面角度提出需求

**执行流程**：

```
用户："页面上要显示用户的注册时间"
    ↓
[UI 层] 添加注册时间显示
    ↓
[前端服务层] 添加注册时间状态
    ↓
[前端 API 层] 确保获取注册时间
    ↓
[后端 API 层] 返回注册时间
    ↓
[后端服务层] 处理注册时间逻辑
    ↓
[数据层] 确保表中有注册时间字段
```

**每层具体工作**：

| 层级 | 工作 | 示例 |
|------|------|------|
| UI 层 | 添加显示字段 | `<div>注册时间: {{ user.registrationTime }}</div>` |
| 前端服务层 | 添加状态 | `registrationTime: string` |
| 前端 API 层 | 更新接口 | `registration_time: string` |
| 后端 API 层 | 返回字段 | `registration_time: datetime` |
| 后端服务层 | 查询字段 | `user.registration_time` |
| 数据层 | 添加字段 | `registration_time = Column(DateTime)` |

### 模式 B：从数据层开始（向后无依赖，向前全推导）

**场景**：用户从数据库角度提出需求

**执行流程**：

```
用户："用户表需要添加手机号字段"
    ↓
[数据层] 添加 phone_number 字段
    ↓
[后端服务层] 更新模型和逻辑
    ↓
[后端 API 层] 支持手机号参数
    ↓
[前端 API 层] 更新 TypeScript 接口
    ↓
[前端服务层] 添加手机号状态
    ↓
[UI 层] 添加手机号输入/显示
```

**每层具体工作**：

| 层级 | 工作 | 示例 |
|------|------|------|
| 数据层 | 添加字段 | `phone_number = Column(String(20))` |
| 后端服务层 | 验证逻辑 | 手机号格式验证 |
| 后端 API 层 | 参数支持 | `phone_number: str` |
| 前端 API 层 | 接口更新 | `phone_number: string` |
| 前端服务层 | 状态管理 | `phoneNumber: string` |
| UI 层 | 输入组件 | `<input v-model="phoneNumber" />` |

### 模式 C：从中间层开始（双向推导）

**场景**：用户从 API 或业务逻辑角度提出需求

**执行流程**：

```
用户："后端 API 需要增加按状态筛选订单"
    ↓
[后端 API 层] 添加 status 查询参数
    ↓
    ├── 向后推导 ───────────────────────────┐
    │                                       ↓
    │                          [后端服务层] 实现筛选逻辑
    │                                       ↓
    │                              [数据层] 确保索引
    │
    └── 向前推导 ───────────────────────────┐
                                            ↓
                              [前端 API 层] 添加参数
                                            ↓
                                [前端服务层] 添加状态
                                            ↓
                                      [UI 层] 添加筛选组件
```

**每层具体工作**：

| 层级 | 工作 | 示例 |
|------|------|------|
| 后端 API 层 | 添加参数 | `status: Optional[OrderStatus] = None` |
| 后端服务层 | 筛选逻辑 | `if status: query = query.filter(Order.status == status)` |
| 数据层 | 确保索引 | `status = Column(String, index=True)` |
| 前端 API 层 | 调用更新 | `getOrders(status?: OrderStatus)` |
| 前端服务层 | 筛选状态 | `filterStatus: OrderStatus \| null` |
| UI 层 | 筛选组件 | `<select v-model="filterStatus">` |

---

## 跨层一致性校验

### 字段名一致性

**命名规范**：

| 层级 | 命名风格 | 示例 |
|------|---------|------|
| UI 层 | 驼峰命名 (camelCase) | `registrationTime` |
| 前端服务层 | 驼峰命名 (camelCase) | `registrationTime` |
| 前端 API 层 | 蛇形命名 (snake_case) | `registration_time` |
| 后端 API 层 | 蛇形命名 (snake_case) | `registration_time` |
| 后端服务层 | 蛇形命名 (snake_case) | `registration_time` |
| 数据层 | 蛇形命名 (snake_case) | `registration_time` |

**一致性检查表**：

| 字段含义 | UI 层 | 前端服务层 | 前端 API 层 | 后端 API 层 | 后端服务层 | 数据层 |
|---------|-------|-----------|------------|------------|-----------|--------|
| 注册时间 | `registrationTime` | `registrationTime` | `registration_time` | `registration_time` | `registration_time` | `registration_time` |
| 手机号 | `phoneNumber` | `phoneNumber` | `phone_number` | `phone_number` | `phone_number` | `phone_number` |
| 订单状态 | `orderStatus` | `orderStatus` | `order_status` | `order_status` | `order_status` | `order_status` |

### 类型一致性

**类型映射表**：

| 数据类型 | UI 层 (TS) | 前端服务层 (TS) | 前端 API 层 (TS) | 后端 API 层 (Pydantic) | 后端服务层 (Python) | 数据层 (SQLAlchemy) |
|---------|-----------|----------------|-----------------|----------------------|-------------------|-------------------|
| 字符串 | `string` | `string` | `string` | `str` | `str` | `String` |
| 整数 | `number` | `number` | `number` | `int` | `int` | `Integer` |
| 浮点数 | `number` | `number` | `number` | `float` | `float` | `Float` |
| 布尔值 | `boolean` | `boolean` | `boolean` | `bool` | `bool` | `Boolean` |
| 日期时间 | `string` | `string` | `string` | `datetime` | `datetime` | `DateTime` |
| 可选类型 | `T \| null` | `T \| null` | `T \| null` | `Optional[T]` | `Optional[T]` | `nullable=True` |
| 枚举 | `Enum` | `Enum` | `Enum` | `Enum` | `Enum` | `Enum` |

### 接口契约检查

**请求契约**：

```typescript
// 前端 API 层请求
interface GetOrdersRequest {
  page: number
  page_size: number
  status?: OrderStatus  // 可选参数
}
```

```python
# 后端 API 层接收
class GetOrdersRequest(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    status: Optional[OrderStatus] = None  # 可选参数
```

**响应契约**：

```python
# 后端 API 层响应
class OrderResponse(BaseModel):
    id: int
    status: OrderStatus
    created_at: datetime
```

```typescript
// 前端 API 层接收
interface Order {
  id: number
  status: OrderStatus
  created_at: string  // ISO 8601 格式
}
```

---

## 完整示例

### 示例：添加订单备注功能

**用户需求**："订单需要支持添加备注，方便客服记录"

#### 步骤 1：识别入口层

- 关键词："订单"、"添加"、"备注"
- 分析：这是一个新功能，涉及数据存储和业务逻辑
- 入口层：**数据层**（需要新增字段存储备注）

#### 步骤 2：推导影响范围

从数据层开始，向前推导：
- 数据层添加字段 → 后端服务层需要处理 → 后端 API 层需要暴露 → 前端 API 层需要调用 → 前端服务层需要管理 → UI 层需要界面

#### 步骤 3：执行贯穿修改

**数据层修改**：

```python
# models/order.py
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    # ... 其他字段
    remark = Column(Text, nullable=True)  # 新增备注字段
```

**后端服务层修改**：

```python
# services/order_service.py
class OrderService:
    def update_remark(self, order_id: int, remark: str) -> Order:
        order = self.get_order(order_id)
        order.remark = remark
        self.db.commit()
        return order
```

**后端 API 层修改**：

```python
# api/routes/orders.py
class UpdateRemarkRequest(BaseModel):
    remark: Optional[str] = Field(None, max_length=1000)

@router.put("/orders/{order_id}/remark")
async def update_order_remark(
    order_id: int,
    request: UpdateRemarkRequest,
    current_user: User = Depends(get_current_user)
):
    order = order_service.update_remark(order_id, request.remark)
    return {"code": 200, "data": order}
```

**前端 API 层修改**：

```typescript
// api/order.ts
interface UpdateRemarkRequest {
  remark?: string
}

export async function updateOrderRemark(
  orderId: number, 
  data: UpdateRemarkRequest
): Promise<Order> {
  const response = await axios.put(`/orders/${orderId}/remark`, data)
  return response.data.data
}
```

**前端服务层修改**：

```typescript
// stores/order.ts
export const useOrderStore = defineStore('order', () => {
  // ... 其他状态
  
  async function updateRemark(orderId: number, remark: string) {
    const updatedOrder = await updateOrderRemark(orderId, { remark })
    // 更新本地状态
    const index = orders.value.findIndex(o => o.id === orderId)
    if (index !== -1) {
      orders.value[index] = updatedOrder
    }
  }
  
  return {
    // ...
    updateRemark
  }
})
```

**UI 层修改**：

```vue
<!-- components/OrderRemark.vue -->
<template>
  <div class="order-remark">
    <textarea 
      v-model="remarkText"
      placeholder="添加订单备注..."
      maxlength="1000"
    />
    <button @click="saveRemark">保存备注</button>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ orderId: number }>()
const orderStore = useOrderStore()

const remarkText = ref('')

async function saveRemark() {
  await orderStore.updateRemark(props.orderId, remarkText.value)
  Swal.fire('保存成功')
}
</script>
```

#### 步骤 4：一致性校验

| 检查项 | 结果 |
|--------|------|
| 字段名一致性 | ✅ `remark` 在各层一致 |
| 类型匹配 | ✅ 前端 `string` ↔ 后端 `str` ↔ 数据库 `Text` |
| 接口契约 | ✅ 请求/响应格式匹配 |
| 长度限制 | ✅ 前后端都有 `max_length=1000` |

#### 步骤 5：数据库迁移

```bash
alembic revision --autogenerate -m "Add remark to orders"
alembic upgrade head
```

---

## 快速参考

### 入口层识别速查

```
界面/显示/页面 → UI 层
状态/Store/缓存 → 前端服务层
前端调用/请求 → 前端 API 层
后端接口/路由 → 后端 API 层
业务逻辑/验证 → 后端服务层
数据库/表/字段 → 数据层
```

### 修改推导速查

```
UI 层修改 → 向后推导全部五层
数据层修改 → 向前推导全部五层
中间层修改 → 双向推导
```

### 一致性检查速查

```
字段名：前端驼峰，后端蛇形
类型：TS 类型 ↔ Pydantic 类型 ↔ SQLAlchemy 类型
接口：请求参数 ↔ 响应格式
约束：长度/必填/验证前后端一致
```
