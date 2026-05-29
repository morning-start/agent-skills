---
name: cocos-2d-render-skill
description: Cocos Creator 3.8 2D 渲染系统，精灵、图集、2D 骨骼动画
dependency:
  - cocos-intro-skill
---

# Cocos Creator 3.8 2D 渲染

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator 2D 渲染组件和技术
- 能力包含：精灵渲染、2D 物理、2D 粒子、骨骼动画
- 触发条件：开发 2D 游戏、2D 特效、2D UI

## 概述

Cocos Creator 提供了完整的 2D 渲染系统，包括 Sprite、Label、2D 物理、2D 粒子、骨骼动画等组件，适用于 2D 游戏开发。

## 精灵渲染

### Sprite 组件
- **Simple**：普通渲染
- **Sliced**：九宫格渲染（适合 UI）
- **Tiled**：平铺渲染
- **Filled**：填充渲染（进度条）

### 九宫格
```typescript
import { Sprite } from 'cc';

const sprite = this.getComponent(Sprite);
sprite.type = Sprite.Type.SLICED;
sprite.sizeMode = Sprite.SizeMode.CUSTOM;
```

### 顶点颜色修改
```typescript
sprite.color = new Color(255, 0, 0, 255);
sprite.node.opacity = 128;
```

## 图集系统

### 图集资源
- 将多个小图打包成大图
- 减少 DrawCall
- 使用 Atlas 组件管理

### 制作图集
1. 使用 TexturePacker 等工具打包
2. 导入 .png 和 .atlas 文件
3. 使用 SpriteFrame 引用

### 使用图集
```typescript
import { SpriteFrame } from 'cc';

const atlas = resources.get('atlas/game', Atlas);
const frame = atlas.getSpriteFrame('icon_1');
sprite.spriteFrame = frame;
```

## 2D 骨骼动画

### Spine 支持
```typescript
import { sp } from 'cc';

const skeleton = node.getComponent(sp.Skeleton);
skeleton.skeletonData = skeletonData;
skeleton.setAnimation(0, 'idle', true);
```

### DragonBones 支持
```typescript
import { dragonBones } from 'cc';

const armature = node.getComponent(dragonBones.ArmatureDisplay);
armature.armatureData = armatureData;
armature.playAnimation('idle', 0);
```

## 2D 粒子系统

### 2D 粒子组件
```typescript
import { Particle2D } from 'cc';

const particle = node.addComponent(Particle2D);
particle.file = particleAsset;
particle.autoRemoveOnFinish = true;
```

## 2D 渲染组件

### Graphics
- 2D 绘图组件
- 绘制几何形状

### Mask
- 2D 裁剪遮罩
- 支持矩形和椭圆

### MotionStreak
- 拖尾效果
- 适合运动轨迹显示

## 资源索引

### 必要参考
- [2D 渲染系统](https://docs.cocos.com/creator/3.8/manual/zh/2d-engine/)
- [Spine 骨骼动画](https://docs.cocos.com/creator/3.8/manual/zh/editor/publish/spine.html)

## 注意事项

### 性能优化
- 使用图集合并 DrawCall
- 合理设置 Sprite 的 Batch 策略
- 避免过大的纹理

### 最佳实践
- 图集大小控制在 2048x2048 以内
- 合理使用九宫格减少内存占用
- 使用对象池管理动态精灵