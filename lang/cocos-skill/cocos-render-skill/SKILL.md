---
name: cocos-render-skill
description: Cocos Creator 3.8 图形渲染系统，渲染管线、光照、后处理
dependency:
  - cocos-intro-skill
---

# Cocos Creator 3.8 图形渲染

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator 渲染系统
- 能力包含：渲染管线、光照、后处理、材质、着色器
- 触发条件：渲染效果开发、光照设置、后期处理

## 概述

RenderPipeline 用于控制场景的渲染流程，包括光照管理、物体剔除、渲染物体排序、渲染目标切换等。可定制化的渲染管线用于对渲染场景中的每个阶段进行更灵活的控制。

## 渲染管线

### Built-in 渲染管线
- 内置渲染管线
- 适合简单项目

### Forward 渲染管线
- 前向渲染
- 支持多光源
- 适合移动平台

### Deferred 渲染管线
- 延迟渲染
- 适合多光源场景
- 更高渲染效率

## 光照系统

### 光源类型
- **Directional Light**：方向光（太阳）
- **Sphere Light**：球形光
- **Spot Light**：聚光灯
- **Point Light**：点光源

### 光照属性
```typescript
import { DirectionalLight } from 'cc';

const light = node.getComponent(DirectionalLight);
light.intensity = 1.5;
light.color = new Color(1, 1, 1, 1);
light.shadowEnabled = true;
```

### 环境光
```typescript
import { scene } from 'cc';

scene.globals.ambientLightIntensity = 0.5;
scene.globals.ambientSkyColor = new Color(0.5, 0.5, 0.5);
```

## 材质系统

### 材质属性
- Base Color
- Metallic
- Roughness
- Normal Map
- Occlusion
- Emission

### 使用材质
```typescript
import { Material } from 'cc';

const material = new Material();
material.initialize({
    effectName: 'standard',
    defines: {
        USE_BATCHING: true
    }
});

const renderer = this.getComponent(MeshRenderer);
renderer.setMaterial(0, material);
```

## 后处理

### 设置后处理
1. 创建后处理相机
2. 添加后处理效果
3. 配置效果参数

### 内置效果
- Bloom（泛光）
- Depth of Field（景深）
- Motion Blur（运动模糊）
- Color Grading（颜色分级）

## 阴影系统

### 阴影类型
- **None**：无阴影
- **ShadowMap**：阴影图
- **Shadow Volume**：阴影体

### 阴影配置
```typescript
import { shadows } from 'cc';

shadows.type = Shadows.ShadowType.ShadowMap;
shadows.maxReceived = 2048;
shadows.size = new Vec2(2048, 2048);
```

## 资源索引

### 必要参考
- [渲染系统](https://docs.cocos.com/creator/3.8/manual/zh/render/)
- [渲染管线](https://docs.cocos.com/creator/3.8/manual/zh/render/render-pipeline/)

## 注意事项

### 性能优化
- 合理控制光源数量
- 使用合适的阴影分辨率
- 优化后处理效果

### 最佳实践
- 选择合适的渲染管线
- 合理使用材质变体
- 做好光照烘焙