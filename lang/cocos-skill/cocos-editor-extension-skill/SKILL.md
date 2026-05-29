---
name: cocos-editor-extension-skill
description: Cocos Creator 3.8 扩展编辑器，自定义面板、菜单、工具
dependency:
  - cocos-intro-skill
---

# Cocos Creator 3.8 扩展编辑器

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator 扩展开发自定义编辑器功能
- 能力包含：自定义面板、菜单、Inspector、快捷键
- 触发条件：开发团队工具、定制工作流、扩展编辑器功能

## 概述

Cocos Creator 提供了强大的扩展系统，开发者可以自定义面板、菜单、Inspector 属性、快捷键等，来扩展编辑器的功能，提高开发效率。

## 扩展项目结构

### 基本目录结构
```
extensions/
  my-extension/
    package.json       # 扩展配置
    src/               # 源码
    panel/             # 面板
    static/            # 静态资源
```

### package.json 配置
```json
{
    "name": "my-extension",
    "version": "1.0.0",
    "main": "./dist/index.js",
    "panels": {
        "my-panel": {
            "title": "My Panel",
            "main": "./panel/index.js"
        }
    },
    "menu": [
        {
            "label": "My Tools",
            "submenu": [
                {
                    "label": "Open My Panel",
                    "command": "my-extension:open-panel"
                }
            ]
        }
    ]
}
```

## 面板开发

### 创建面板
```typescript
import { Panel } from 'cc.EDITOR';

// 面板类
@Panel.title('my-panel')
@Panel.type(Panel.ResourceTree)
class MyPanel extends Panel {
    constructor() {
        super();
    }

    ready() {
        // 面板准备就绪
        this.$header.innerHTML = '<h3>My Panel</h3>';
    }

    refresh() {
        // 刷新面板
    }
}

module.exports = MyPanel;
```

### 面板通信
```typescript
// 发送消息到编辑器
Editor.Scene.callSceneScript('my-extension', 'my-method', data);

// 监听消息
Editor.Ipc.on('my-extension:message', (event, data) => {
    console.log('Received:', data);
});
```

## 自定义 Inspector

### 创建属性装饰器
```typescript
import { decorator } from 'cc.EDITOR';

@decorator.Componentmenu('My Components/CustomComponent')
@decorator.requireComponent(RigidBody)
@ccclass('CustomComponent')
export class CustomComponent extends Component {
    @decorator.tooltip('自定义数值')
    @decorator.range([0, 100])
    @property
    customValue: number = 50;
}
```

### 自定义 Inspector 面板
```typescript
Editor.Ipc.add('custom-inspector:verify', (payload) => {
    return {
        valid: payload.value > 0,
        error: payload.value <= 0 ? 'Value must be greater than 0' : ''
    };
});
```

## 菜单扩展

### 注册菜单
```json
{
    "menu": [
        {
            "label": "My Menu",
            "submenu": [
                {
                    "label": "Action 1",
                    "accelerator": "CmdOrCtrl+Shift+A",
                    "command": "my-extension:action-1"
                }
            ]
        }
    ]
}
```

### 菜单命令处理
```typescript
Editor.Ipc.handle('my-extension:action-1', () => {
    console.log('Menu action triggered');
    // 执行操作
});
```

## 快捷键

### 注册快捷键
```json
{
    "shortcuts": [
        {
            "key": "CmdOrCtrl+Shift+G",
            "message": "my-extension:grab-something"
        }
    ]
}
```

## 资源索引

### 必要参考
- [扩展编辑器](https://docs.cocos.com/creator/3.8/manual/zh/editor/)
- [扩展开发文档](https://docs.cocos.com/creator/3.8/manual/zh/editor/extension/)

## 注意事项

### 性能优化
- 避免频繁刷新面板
- 善用缓存
- 懒加载非必要资源

### 最佳实践
- 遵循扩展命名规范
- 提供友好的错误提示
- 做好版本兼容性