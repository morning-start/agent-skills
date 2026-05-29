---
name: cocos-animation-skill
description: Cocos Creator 3.8 动画系统，关键帧动画、骨骼动画、程序化动画
dependency:
  - cocos-intro-skill
  - cocos-scene-skill
---

# Cocos Creator 3.8 动画系统

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator 动画系统制作游戏动画
- 能力包含：关键帧动画、骨骼动画、动画状态机、程序化动画
- 触发条件：制作角色动画、UI 动画、场景动画

## 概述

Cocos Creator 内置了通用的动画系统用以实现基于关键帧的动画。除了支持标准的位移、旋转、缩放动画和帧动画之外，还支持任意组件属性和用户自定义属性的驱动。

## 核心概念

### 动画剪辑（Animation Clip）
- 包含动画数据的资源
- 可复用
- 通过动画编辑器创建

### 动画组件（Animation Component）
- 附加到节点上
- 管理动画状态
- 控制动画播放

### 动画状态（Animation State）
- 动画剪辑的状态对象
- 控制播放、暂停、停止、切换
- 支持变速、循环模式设置

## 动画编辑器

### 打开方式
- 菜单：窗口 -> 动画编辑器
- 快捷键：Ctrl/Cmd + 6

### 编辑流程
1. 选中节点
2. 在动画编辑器中创建动画剪辑
3. 添加属性轨道
4. 添加关键帧
5. 预览动画

### 关键帧操作
- **添加**：在时间轴上选中帧，右键选择"添加关键帧"
- **移动**：拖拽关键帧
- **复制粘贴**：支持复制关键帧到其他位置
- **曲线编辑**：调整缓动曲线

## 骨骼动画

### Spine 骨骼动画
- 使用 Spine Skeleton 组件
- 支持 Spine 官方工具导出的数据格式
- 资源类型：.json/.skel

### DragonBones 骨骼动画
- 使用 ArmatureDisplay 组件
- 支持 DragonBones 工具导出
- 资源类型：.json

## 骨骼动画组件

### Spine Skeleton
```typescript
import { sp } from 'cc';

const skeleton = this.getComponent(sp.Skeleton);
skeleton.setAnimation(0, 'run', true); // 播放名为 run 的动画
```

### ArmatureDisplay
```typescript
import { dragonBones } from 'cc';

const armature = this.getComponent(dragonBones.ArmatureDisplay);
armature.playAnimation('run', 0); // 播放动画
```

## Marionette 动画系统

### 概述
- v3.4 新增
- 实现由状态机控制的自动化且可复用的骨骼动画流程
- 适合角色动画状态管理

### 状态机概念
- 状态（State）
- 过渡（Transition）
- 条件（Condition）

## 程序化动画

### 概述
- v3.8 新增
- 通过不同的动画节点对动画的采样过程进行程序化控制
- 适合需要动态调整的动画

### 常用节点
- Sample Spine
- Sample DragonBones
- 3D Model Sample

## 脚本控制

### 基本操作
```typescript
import { Animation } from 'cc';

const anim = this.getComponent(Animation);

// 播放
anim.play('animName');

// 暂停
anim.pause('animName');

// 停止
anim.stop();

// 跨动画混合
anim.setAnimationState('anim1', 0.5);
```

### 动画状态控制
```typescript
const state = anim.getState('animName');
state.speed = 1.5; // 播放速度
state.wrapMode = WrapMode.Loop; // 循环模式
state.weight = 0.5; // 混合权重
```

## 资源索引

### 必要参考
- [动画系统](https://docs.cocos.com/creator/3.8/manual/zh/animation/)
- [Marionette 动画系统](https://docs.cocos.com/creator/3.8/manual/zh/animation/marionette/)
- [程序化动画](https://docs.cocos.com/creator/3.8/manual/zh/animation/procedural-animation/)

## 注意事项

### 性能优化
- 控制同屏动画数量
- 合理使用动画曲线
- 及时停止不需要的动画

### 最佳实践
- 分离角色动画和场景动画
- 使用预制管理动画状态
- 做好动画命名规范