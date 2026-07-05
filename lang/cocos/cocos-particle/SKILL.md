---
name: cocos-particle
description: Cocos Creator 3.8 粒子系统，2D/3D 粒子特效制作
dependency:
  - cocos-intro
---

# Cocos Creator 3.8 粒子系统

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator 粒子系统制作特效
- 能力包含：2D 粒子、3D 粒子、粒子编辑器、特效制作
- 触发条件：制作火焰、烟雾、爆炸等游戏特效

## 概述

粒子系统是游戏引擎特效表现的基础，它可以用于模拟火、烟、水、云、雪、落叶等自然现象，也可用于模拟发光轨迹、速度线等抽象视觉效果。Cocos Creator 支持 2D 和 3D 粒子系统。

## 粒子组件

### ParticleSystem2D（2D 粒子）
```typescript
import { ParticleSystem2D } from 'cc';

const particle = node.addComponent(ParticleSystem2D);
particle.file = particleAsset; // Plist 格式
particle.emitRate = 100;
particle.duration = -1; // 持续发射
particle.autoRemoveOnFinish = false;
```

### ParticleSystem（3D 粒子）
```typescript
import { ParticleSystem } from 'cc';

const particle = node.addComponent(ParticleSystem);
particle.mesh = meshAsset; // 可选，自定义形状
particle.particleCount = 200;
particle.startSize = 0.5;
particle.startSpeed = 5;
```

## 粒子属性

### 发射属性
- **duration**：持续时间（-1 永久）
- **emissionRate**：发射速率
- **loop**：是否循环
- **playOnLoad**：加载时播放

### 生命周期
- **startLifetime**：初始生命周期
- **startDelay**：启动延迟

### 空间属性
- **startPosition**：初始位置
- **startRotation**：初始旋转
- **startSize**：初始大小

### 运动属性
- **startSpeed**：初始速度
- **velocityModifier**：速度修饰器
- **gravityModifier**：重力修饰器

### 外观属性
- **startColor**：初始颜色
- **endColor**：结束颜色
- **startOpacity**：初始透明度
- **endOpacity**：结束透明度
- **startScale**：初始缩放
- **endScale**：结束缩放

### 颜色渐变
```typescript
const colorOverLifetime = particle.colorOverLifetime;
colorOverLifetime.enabled = true;
colorOverLifetime.color = new Gradient();

const gradient = new Gradient();
gradient.addColorStop(0, new Color(255, 255, 255, 255));
gradient.addColorStop(1, new Color(255, 255, 255, 0));
colorOverLifetime.color.colorKeyframes = [
    { time: 0, value: new Color(255, 255, 255, 255) },
    { time: 1, value: new Color(255, 255, 255, 0) }
];
```

## 形状模块

### Sphere/半球形状
```typescript
import { ShapeModule } from 'cc';

const shapeModule = particle.shape;
shapeModule.enabled = true;
shapeModule.shapeType = ShapeModule.Type.Sphere;
shapeModule.radius = 2;
shapeModule.arcSpeed = 30;
```

### 锥形发射
```typescript
shapeModule.shapeType = ShapeModule.Type.Cone;
shapeModule.angle = 30;
shapeModule.emitFrom = ShapeModule.EmitLocation.Base;
```

## 发射器模块

### 曲线编辑
```typescript
import { CurveRange } from 'cc';

particle.startSize.mode = CurveRange.Mode.Curve;
particle.startSize.curve = new Curve();
particle.startSize.curve.addKey(0, 1);
particle.startSize.curve.addKey(0.5, 2);
particle.startSize.curve.addKey(1, 0.5);
```

## 脚本控制

### 播放控制
```typescript
// 播放
particle.play();

// 暂停
particle.pause();

// 停止
particle.stop();

// 清除
particle.clear();
```

### 动态修改
```typescript
// 修改发射速率
particle.emissionRate = 50;

// 修改速度
particle.startSpeed = 10;

// 修改颜色
particle.startColor = new Color(255, 0, 0, 255);
```

## 资源索引

### 必要参考
- [粒子系统](https://docs.cocos.com/creator/3.8/manual/zh/particle-system/)
- [2D 粒子](https://docs.cocos.com/creator/3.8/manual/zh/particle-system/2d-particle.html)
- [3D 粒子](https://docs.cocos.com/creator/3.8/manual/zh/particle-system/particle-system.md)

## 注意事项

### 性能优化
- 合理控制粒子数量
- 避免过长的生命周期
- 使用 LOD 控制

### 最佳实践
- 制作粒子预设
- 使用粒子编辑器可视化编辑
- 善用对象池管理