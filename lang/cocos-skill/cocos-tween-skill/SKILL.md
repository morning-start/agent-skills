---
name: cocos-tween-skill
description: Cocos Creator 3.8 缓动系统，补间动画、属性动画
dependency:
  - cocos-intro-skill
  - cocos-scene-skill
---

# Cocos Creator 3.8 缓动系统

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator 缓动系统实现动画
- 能力包含：缓动动画、链式调用、队列控制、属性变化
- 触发条件：制作 UI 动画、过渡效果、补间动画

## 概述

缓动系统被广泛的应用于游戏开发中，其主要目的是解决离线动画无法满足需求时的动态动画问题。在 Cocos Creator 中，缓动除了可以用于变换位置、旋转、缩放和颜色等常规动画信息，还支持延迟、队列、并行等动作行为。

## 基础用法

### 创建 Tween
```typescript
import { tween, Node, Vec3 } from 'cc';

const tw = tween(this.node)
    .to(1, { position: new Vec3(100, 0, 0) })
    .start();
```

### 链式调用
```typescript
tween(this.node)
    .to(0.5, { position: new Vec3(100, 0, 0) })
    .by(0.5, { position: new Vec3(100, 0, 0) })
    .to(0.5, { position: new Vec3(200, 0, 0) })
    .start();
```

## 常用缓动

### 位置
```typescript
// 移动到目标位置
tween(node)
    .to(1, { position: new Vec3(100, 0, 0) })
    .start();

// 相对移动
tween(node)
    .by(1, { position: new Vec3(100, 0, 0) })
    .start();
```

### 旋转
```typescript
tween(node)
    .to(1, { rotation: 360 })
    .start();
```

### 缩放
```typescript
tween(node)
    .to(0.3, { scale: new Vec3(1.2, 1.2, 1) })
    .to(0.3, { scale: new Vec3(1, 1, 1) })
    .start();
```

### 透明度
```typescript
tween(node)
    .to(0.5, { opacity: 0 })
    .start();
```

### 颜色
```typescript
tween(node)
    .to(0.5, { color: new Color(255, 0, 0, 255) })
    .start();
```

## 缓动函数

### 内置缓动
```typescript
import { tween,.easing } from 'cc';

// 使用内置缓动函数
tween(node)
    .to(1, { position: new Vec3(100, 0, 0) }, { easing: easing.sineInOut })
    .start();

// 常用缓动函数
// - linear
// - sineIn / sineOut / sineInOut
// - quadIn / quadOut / quadInOut
// - cubicIn / cubicOut / cubicInOut
// - elasticIn / elasticOut / elasticInOut
// - bounceIn / bounceOut / bounceInOut
// - backIn / backOut / backInOut
```

## 动作组合

### 并行执行
```typescript
tween(node)
    .parallel(
        tween().to(1, { position: new Vec3(100, 0, 0) }),
        tween().to(1, { scale: new Vec3(0.5, 0.5, 1) })
    )
    .start();
```

### 顺序执行
```typescript
tween(node)
    .sequence(
        tween().to(0.5, { position: new Vec3(100, 0, 0) }),
        tween().to(0.5, { scale: new Vec3(0.5, 0.5, 1) })
    )
    .start();
```

### 重复执行
```typescript
// 重复 3 次
tween(node)
    .to(0.5, { position: new Vec3(100, 0, 0) })
    .repeat(3)
    .start();

// 永久循环
tween(node)
    .to(0.5, { position: new Vec3(100, 0, 0) })
    .repeatForever()
    .start();
```

### 延迟
```typescript
tween(node)
    .delay(0.5)
    .to(1, { position: new Vec3(100, 0, 0) })
    .start();
```

### 回调
```typescript
tween(node)
    .to(1, { position: new Vec3(100, 0, 0) })
    .call(() => {
        console.log('Animation complete!');
    })
    .start();
```

## Tween 实例方法

### 停止
```typescript
const tw = tween(node).to(1, { position: new Vec3(100, 0, 0) });
tw.start();

// 停止
tw.stop();
```

### 目标设置
```typescript
const tw = tween(node);
tw.target(new Vec3(200, 0, 0)).to(1, { position: new Vec3(100, 0, 0) });
```

## 实用示例

### UI 弹窗
```typescript
tween(this.popupNode)
    .set({ scale: new Vec3(0, 0, 1) })
    .to(0.3, { scale: new Vec3(1.1, 1.1, 1) }, { easing: easing.backOut })
    .to(0.1, { scale: new Vec3(1, 1, 1) })
    .start();
```

### 闪烁效果
```typescript
tween(this.node)
    .to(0.5, { opacity: 0 })
    .to(0.5, { opacity: 255 })
    .repeatForever()
    .start();
```

## 资源索引

### 必要参考
- [缓动系统](https://docs.cocos.com/creator/3.8/manual/zh/tween/)
- [缓动接口](https://docs.cocos.com/creator/3.8/manual/zh/tween/tween-api.html)
- [缓动函数](https://docs.cocos.com/creator/3.8/manual/zh/tween/easing.html)

## 注意事项

### 性能优化
- 避免同时创建过多 Tween
- 及时停止不需要的 Tween
- 使用对象池管理重复 Tween

### 最佳实践
- 链式调用便于阅读
- 善用回调处理完成逻辑
- 合理使用缓动函数增强效果