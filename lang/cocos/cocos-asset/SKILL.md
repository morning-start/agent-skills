---
name: cocos-asset
description: Cocos Creator 3.8 资源系统，图像、音频、模型等资源类型与管理
dependency:
  - cocos-intro
---

# Cocos Creator 3.8 资源系统

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator 的资源管理、各种资源类型的使用
- 能力包含：资源导入、资源类型、资源工作流、常见资源格式
- 触发条件：导入资源、管理项目资源、处理各类游戏资源

## 概述

资源是游戏中的重要组成部分，Cocos Creator 支持导入不同类型的资源，并允许开发者将资源运用在游戏中。

## 资源管理器

### 功能
- 访问和管理项目中的所有资源
- 以树状结构显示文件夹
- 自动同步操作系统中的资源修改
- 支持拖拽导入资源

### 资源目录
- **assets**：项目资源根目录
- **resources**：需要动态加载的资源目录
- **imported**：导入后的资源缓存

## 常见资源类型

### 图像资源
- 纹理贴图（Texture）
- 精灵帧（SpriteFrame）
- 图集（Atlas）
- 立方体贴图（CubeMap）

### 场景资源
- 场景文件（.scene）

### 预制资源
- 预制件（Prefab）

### 脚本资源
- JavaScript 脚本（.js）
- TypeScript 脚本（.ts）

### 字体资源
- 动态字体（TTF）
- 位图字体（BMFont）

### 音频资源
- 支持 MP3、WAV、OGG 等格式

### 模型资源
- 支持 glTF、FBX 等格式
- 动画资源

### 骨骼动画资源
- Spine 骨骼动画
- DragonBones 骨骼动画

### 瓦片地图资源
- TiledMap（TMX 格式）

### 材质资源
- 材质定义

## 资源工作流

### 导入资源
1. 将资源文件拖入 assets 目录
2. 或使用资源管理器的导入功能
3. 引擎自动处理资源转换

### 使用资源
1. 在属性检查器中拖拽资源到对应属性
2. 或通过脚本动态加载

### 动态加载
```javascript
import { resources } from 'cc';

// 加载资源（路径不含扩展名）
resources.load('textures/myImage', SpriteFrame, (err, spriteFrame) => {
    if (!err) {
        this.sprite.spriteFrame = spriteFrame;
    }
});
```

## 资源索引

### 必要参考
- [资源系统](https://docs.cocos.com/creator/3.8/manual/zh/asset/)
- [Asset Manager](https://docs.cocos.com/creator/3.8/manual/zh/asset/manager.html)

## 注意事项

### 路径规范
- 动态加载路径不能包含扩展名
- resources 目录下的资源才能动态加载

### 内存管理
- 及时释放不需要的资源
- 合理使用资源缓存