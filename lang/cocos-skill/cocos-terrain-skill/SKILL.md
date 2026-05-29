---
name: cocos-terrain-skill
description: Cocos Creator 3.8 地形系统，山川地貌、地形编辑
dependency:
  - cocos-intro-skill
---

# Cocos Creator 3.8 地形系统

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator 地形系统创建游戏场景
- 能力包含：地形创建、地形编辑、地形材质、地形渲染
- 触发条件：创建大型户外场景、山地地形、开放世界

## 概述

地形系统以一种高效的方式来展示大自然的山川地貌。开发者可以很方便的使用画刷来雕刻出盆地、山脉、峡谷、平原等地貌。

## 地形组件

### 创建地形
1. 在层级管理器中右键选择"创建"
2. 选择"3D Object" -> "Terrain"
3. 或使用代码创建

### Terrain 组件属性
- **alignToGrid**：对齐网格
- **autoBuild**：自动构建
- **brushGround**：画刷工具

## 地形编辑

### 画刷工具
- **Raise/Lower**：升降地形
- **Smooth**：平滑地形
- **Flatten**：平整地形
- **Slope**：坡度调整
- **Roughness**：粗糙度

### 高度图
```typescript
import { Terrain, TerrainBlock } from 'cc';

const terrain = this.node.getComponent(Terrain);

// 设置高度
terrain.setHeight(x, y, height);

// 获取高度
const height = terrain.getHeight(x, y);

// 设置法线
terrain.setNormal(x, y, normal);
```

## 地形材质

### Layer 系统
- 创建地形 Layer
- 设置物理碰撞
- 配置材质

### 纹理层
```typescript
import { TerrainLayer } from 'cc';

const layer = new TerrainLayer();
layer.tileSize = 1;
layer.detailMap = detailTexture;
terrain.addLayer(layer);
```

### 混合纹理
- 多层纹理混合
- 根据高度和坡度自动混合

## 性能优化

### LOD 系统
- 设置地形 LOD 距离
- 根据相机距离切换细节级别

### 遮挡剔除
- 启用地形遮挡
- 优化远距离渲染

### 视锥剔除
- 只渲染可见区域
- 减少不必要的绘制

## 实用技巧

### 地形碰撞
```typescript
import { RigidBody, ColliderBox } from 'cc';

const rigidBody = terrainNode.addComponent(RigidBody);
rigidBody.type = RigidBody.Type.Static;

const collider = terrainNode.addComponent(TerrainCollider);
collider.terrain = terrain;
```

### 地形寻路
- 结合导航系统
- 自动生成导航网格

## 资源索引

### 必要参考
- [地形系统](https://docs.cocos.com/creator/3.8/manual/zh/terrain/)
- [Terrain API](https://docs.cocos.com/creator/3.8/api/zh/classes/Terrain.html)

## 注意事项

### 性能优化
- 合理设置地形大小
- 使用合适的网格分辨率
- 启用视锥剔除

### 最佳实践
- 制作地形预设
- 分区块管理大地形
- 合理使用纹理层数