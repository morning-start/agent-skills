---
name: cocos-physics
description: Cocos Creator 3.8 物理系统，刚体、碰撞、触发器、物理材质
dependency:
  - cocos-intro
  - cocos-scene
---

# Cocos Creator 3.8 物理系统

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator 物理系统模拟现实物理
- 能力包含：刚体、碰撞体、触发事件、物理材质、射线检测
- 触发条件：实现物理碰撞、角色控制、物体运动

## 概述

物理系统用于让游戏世界的物体按照现实世界进行基于物理的模拟与更新，这对于提升游戏的真实感极为重要。Cocos Creator 内置了 2D 物理系统和 3D 物理系统。

## 物理配置

### 开启物理系统
- 菜单：项目 -> 项目设置 -> 功能裁剪
- 启用 2D 或 3D 物理系统

### 物理世界设置
```typescript
import { PhysicsSystem } from 'cc';

// 获取物理系统实例
const physicsSystem = PhysicsSystem.instance;

// 重力设置
physicsSystem.gravity = new Vec3(0, -9.8, 0);

// 开启调试绘制
physicsSystem.enable = true;
```

## 2D 物理系统

### 刚体类型
- **Dynamic**：动态刚体，受重力影响，可被推动
- **Kinematic**：运动学刚体，可设置速度，不受重力影响
- **Static**：静态刚体，不移动，用于地面和墙壁
- **Animated**：动画刚体，用于动画控制的物体

### 碰撞组件
- **BoxCollider2D**：盒形碰撞器
- **CircleCollider2D**：圆形碰撞器
- **PolygonCollider2D**：多边形碰撞器
- **CapsuleCollider2D**：胶囊碰撞器

### 属性配置
```typescript
import { RigidBody2D, Physics2DManager } from 'cc';

const rigidBody = node.addComponent(RigidBody2D);
rigidBody.type = RigidBody2D.Type.Dynamic;
rigidBody.gravityScale = 1;
rigidBody.linearDamping = 0.3;
rigidBody.angularDamping = 0.3;
```

## 3D 物理系统

### 碰撞组件
- **BoxCollider**：盒形碰撞器
- **SphereCollider**：球形碰撞器
- **CylinderCollider**：圆柱碰撞器
- **CapsuleCollider**：胶囊碰撞器
- **MeshCollider**：网格碰撞器

### 刚体组件
```typescript
import { RigidBody } from 'cc';

const rigidBody = node.addComponent(RigidBody);
rigidBody.mass = 10;
rigidBody.linearDamping = 0.1;
rigidBody.angularDamping = 0.1;
rigidBody.type = RigidBody.Type.Dynamic;
```

## 碰撞与触发

### 碰撞事件
```typescript
import { Component, ICollisionEvent } from 'cc';

export class MyScript extends Component {
    onEnable() {
        const collider = this.getComponent(BoxCollider);
        collider.on('onCollisionEnter', this.onCollisionEnter, this);
    }

    onDisable() {
        const collider = this.getComponent(BoxCollider);
        collider.off('onCollisionEnter', this.onCollisionEnter, this);
    }

    onCollisionEnter(event: ICollisionEvent) {
        console.log('Collision enter with:', event.otherCollider.node.name);
    }
}
```

### 触发事件
```typescript
collider.on('onTriggerEnter', this.onTriggerEnter, this);
collider.on('onTriggerStay', this.onTriggerStay, this);
collider.on('onTriggerExit', this.onTriggerExit, this);
```

## 射线检测

### 2D 射线检测
```typescript
import { Physics2DSystem, Vec2 } from 'cc';

const results = Physics2DSystem.instance.raycast(
    new Vec2(0, 0),
    new Vec2(1, 0),
    Physics2DEnums.Raycast2DType.Closest
);

if (results.length > 0) {
    console.log('Hit:', results[0].collider.node.name);
}
```

### 3D 射线检测
```typescript
import { PhysicsSystem, ray } from 'cc';

const results = PhysicsSystem.instance.raycast(
    new Vec3(0, 0, 0),
    new Vec3(1, 0, 0),
    100
);
```

## 物理材质

### 创建物理材质
1. 资源管理器中创建物理材质资源
2. 设置摩擦系数和弹性系数
3. 应用到碰撞器

### 属性
- **Friction**：摩擦系数
- **Restitution**：弹性系数（恢复系数）

## 资源索引

### 必要参考
- [物理系统](https://docs.cocos.com/creator/3.8/manual/zh/physics/)
- [2D 物理系统](https://docs.cocos.com/creator/3.8/manual/zh/2d-physics/)

## 注意事项

### 性能优化
- 合理使用碰撞体数量
- 避免过密的碰撞网格
- 使用碰撞分组过滤

### 最佳实践
- 使用简单碰撞体代替复杂网格碰撞体
- 合理设置碰撞矩阵
- 及时销毁不需要的刚体