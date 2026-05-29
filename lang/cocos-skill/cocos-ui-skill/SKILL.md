---
name: cocos-ui-skill
description: Cocos Creator 3.8 UI 系统，布局、组件、适配多分辨率屏幕
dependency:
  - cocos-intro-skill
  - cocos-scene-skill
---

# Cocos Creator 3.8 UI 系统

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator UI 系统制作游戏界面
- 能力包含：UI 组件、布局系统、多分辨率适配、渲染层级
- 触发条件：制作游戏界面、UI 交互、菜单系统

## 概述

Cocos Creator 提供了强大而灵活的 UI 系统，通过组合不同 UI 组件来生产能够适配多种分辨率屏幕的、通过数据动态生成和更新显示内容的，以及支持多种排版布局方式的 UI 界面。

## UI 组件

### 基础组件

#### Sprite（精灵）
- 显示图片
- 支持九宫格（Sliced）
- 类型：Simple、Sliced、Tiled、Filled

#### Label（文本）
- 显示文本
- 字体设置
- 排版：Horizontal（水平）/ Vertical（垂直）
- Overflow：CLAMP、SHRINK、RESIZE_HEIGHT

#### Button（按钮）
- 交互按钮
- 状态：Normal、Pressed、Hover、Disabled
- 过渡效果：Color、Sprite、Scale

#### Toggle（开关）
- 单选/复选框
- ToggleGroup 组件管理组

#### Slider（滑动条）
- 进度条/音量条
- 范围和方向设置

#### ProgressBar（进度条）
- 显示进度
- 方向设置
- 填充模式

### 容器组件

#### Widget（对齐组件）
- 相对于父节点的边距对齐
- 左/右/上/下/中/垂直对齐
- 同级对齐

#### Layout（布局组件）
- 布局类型：Horizontal（水平）/ Vertical（垂直）/ GRID（网格）
- 间距、排列方式
- 自动调整大小

#### ScrollView（滚动视图）
- 可滚动区域
- 方向：水平/垂直
- 视口裁剪

#### PageView（页面视图）
- 多页面切换
- 指示器

#### Canvas（画布）
- UI 根节点
- 设计分辨率适配

## 多分辨率适配

### 适配策略
- **Match Width/Height**：根据宽或高适配
- **Exact Fit**：拉伸适应
- **No Border**：无黑边裁剪
- **Show All**：全部显示可能有黑边

### 设置方法
1. 在 Canvas 组件设置设计分辨率
2. 使用 Widget 组件对齐
3. 使用 Layout 组件自动布局

## 渲染层级

### 优先级
- 同一 Canvas 下，节点层级决定渲染顺序
- 子节点在上层
- 兄弟节点后添加的在上层

### 独立 Canvas
- 创建独立 Canvas 隔离渲染
- 解决 UI 和 3D 场景穿插问题

## 常用技巧

### 文字描边
```typescript
const label = this.getComponent(Label);
label.spacingX = 2;
```

### 点击穿透
```typescript
this.node._uiProps.uiComps = this.node._uiProps.uiComps || {};
// 设置为透明不拦截点击
```

## 资源索引

### 必要参考
- [UI 系统](https://docs.cocos.com/creator/3.8/manual/zh/ui-system/)
- [UI 组件参考](https://docs.cocos.com/creator/3.8/api/zh/classes/Layer.html)

## 注意事项

### 性能优化
- 合理使用 UI 组件数量
- 避免频繁修改 UI 属性
- 使用对象池管理动态 UI

### 最佳实践
- 分离 UI 层级
- 预制常用 UI 模块
- 使用 Atlas 减少 DrawCall