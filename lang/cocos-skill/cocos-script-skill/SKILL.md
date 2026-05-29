---
name: cocos-script-skill
description: Cocos Creator 3.8 脚本指南与事件系统，JavaScript/TypeScript 组件编写
dependency:
  - cocos-intro-skill
  - cocos-scene-skill
---

# Cocos Creator 3.8 脚本指南与事件系统

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator 脚本编写、组件系统与事件机制
- 能力包含：脚本基础、组件生命周期、事件系统、自定义属性
- 触发条件：编写游戏逻辑、处理用户交互、组件通信

## 概述

Cocos Creator 脚本用于实现用户定义的（游戏）行为，支持 JavaScript 和 TypeScript 两种编程语言。通过编写脚本组件，并挂载到场景节点中来驱动场景中的物体。

## 编程语言

### JavaScript vs TypeScript
- **JavaScript**：传统选择，灵活简洁
- **TypeScript**：推荐选择，类型安全

## 脚本基础

### 创建脚本
1. 在资源管理器中创建脚本文件
2. 继承 `Component` 类
3. 挂载到节点上

### 基础示例
```typescript
import { _decorator, Component, Node } from 'cc';

const { ccclass, property } = _decorator;

@ccclass('MyScript')
export class MyScript extends Component {
    @property
    speed: number = 100;

    start() {
        // 初始化逻辑
    }

    update(deltaTime: number) {
        // 每帧更新
    }
}
```

## 组件生命周期

### 常用回调
- `onLoad()`：组件加载时调用
- `start()`：首次 update 前调用
- `update(dt)`：每帧调用
- `lateUpdate(dt)`：所有 update 后调用
- `onDestroy()`：组件销毁时调用

## 属性声明

### 常用装饰器
```typescript
@property
myValue: number = 10;

@property(Node)
targetNode: Node | null = null;

@property({
    type: SpriteFrame
})
spriteFrame: SpriteFrame | null = null;
```

### 属性类型
- 基本类型（number、string、boolean）
- 节点引用（Node）
- 资源引用（SpriteFrame、Prefab 等）
- 数组类型

## 事件系统

### 节点事件
```typescript
import { Node, Event } from 'cc';

this.node.on(Node.EventType.TOUCH_START, (event: Event.EventTouch) => {
    console.log('Touch started');
}, this);

this.node.on('custom-event', (data: any) => {
    console.log('Custom event:', data);
}, this);
```

### 系统事件
```typescript
import { systemEvent, SystemEventType, EventKeyboard } from 'cc';

systemEvent.on(SystemEventType.KEY_DOWN, (event: EventKeyboard) => {
    console.log('Key down:', event.keyCode);
}, this);
```

### 事件发射与监听
```typescript
// 发射事件
this.node.emit('my-event', { data: 123 });

// 监听事件
this.node.on('my-event', (eventData) => {
    console.log(eventData.data);
});
```

## 组件通信

### 获取其他组件
```typescript
// 获取同级组件
const sprite = this.node.getComponent(Sprite);

// 获取子节点组件
const label = this.node.getChildByName('Label')!.getComponent(Label);

// 获取父节点组件
const parentScript = this.node.parent!.getComponent(MyScript);
```

## 资源索引

### 必要参考
- [脚本指南](https://docs.cocos.com/creator/3.8/manual/zh/scripting/)
- [事件系统](https://docs.cocos.com/creator/3.8/manual/zh/scripting/events/)
- [Node API](https://docs.cocos.com/creator/3.8/api/zh/classes/Node.html)

## 注意事项

### 编码规范
- 使用有意义的变量名
- 合理组织代码结构
- 添加必要的注释

### 性能注意
- 避免在 update 中创建对象
- 善用对象池
- 及时注销事件监听