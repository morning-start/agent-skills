---
name: cocos-i18n
description: Cocos Creator 3.8 本地化系统，多语言支持
dependency:
  - cocos-intro
---

# Cocos Creator 3.8 本地化

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator 本地化实现多语言
- 能力包含：多语言配置、动态切换、本地化资源
- 触发条件：开发多语言游戏、支持国际化和地区化

## 概述

Cocos Creator 提供了本地化（i18n）支持，帮助开发者实现游戏的多语言切换，让游戏能够适应不同地区和语言的用户。

## 本地化配置

### 安装插件
1. 打开 Cocos Creator
2. 扩展 -> 扩展商店
3. 搜索 i18n 插件并安装

### 配置语言
```typescript
import { i18n } from 'cc';

// 设置默认语言
i18n.init({
    locale: 'zh-CN'
});

// 切换语言
i18n.setLanguage('en-US');
```

## 多语言文件

### JSON 格式配置
```json
{
    "zh-CN": {
        "game_title": "我的游戏",
        "start_btn": "开始游戏",
        "score": "得分：{score}"
    },
    "en-US": {
        "game_title": "My Game",
        "start_btn": "Start Game",
        "score": "Score: {score}"
    }
}
```

### 加载语言包
```typescript
import { i18n } from 'cc';

i18n.loadScene('i18n/menu', (err, result) => {
    if (!err) {
        console.log('Language loaded');
    }
});
```

## 使用本地化

### 获取文本
```typescript
// 获取本地化文本
const title = i18n.t('game_title');
const scoreText = i18n.t('score', { score: 100 });
```

### 动态更新 Label
```typescript
import { Label } from 'cc';

const label = this.getComponent(Label);
i18n.updateLabel(label, 'game_title');
```

### 自动更新组件
```typescript
import { I18n } from 'cc';

const i18nComponent = this.node.addComponent(I18n);
i18nComponent.dataID = 'game_title';
```

## 语言切换

### 监听语言变化
```typescript
i18n.on('language-changed', () => {
    console.log('Language changed to:', i18n.currentLanguage);
    // 刷新界面文本
    this.refreshUI();
});
```

### 持久化语言设置
```typescript
import { sys } from 'cc';

// 保存语言设置
sys.localStorage.setItem('language', i18n.currentLanguage);

// 加载语言设置
const savedLang = sys.localStorage.getItem('language');
if (savedLang) {
    i18n.setLanguage(savedLang);
}
```

## 格式化

### 参数替换
```typescript
// {0}, {1} 占位符
i18n.t('items_count', { 0: items.length });

// 命名参数
i18n.t('player_level', { level: player.lv, name: player.name });
```

### 复数形式
```typescript
i18n.t('apple_count', { count: appleNum });
// zh-CN: 1个苹果 / 2个苹果
// en-US: 1 apple / 2 apples
```

## 资源索引

### 必要参考
- [本地化](https://docs.cocos.com/creator/3.8/manual/zh/i18n/)
- [i18n API](https://docs.cocos.com/creator/3.8/api/zh/modules/i18n.html)

## 注意事项

### 性能优化
- 避免频繁切换语言
- 缓存已加载的语言包
- 延迟加载非当前语言资源

### 最佳实践
- 使用键值对而非硬编码文本
- 做好文本长度适配
- 注意 RTL（从右到左）语言支持