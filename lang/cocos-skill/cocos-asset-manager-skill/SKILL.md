---
name: cocos-asset-manager-skill
description: Cocos Creator 3.8 Asset Manager 运行时资源管理，加载、缓存、释放
dependency:
  - cocos-intro-skill
  - cocos-asset-skill
---

# Cocos Creator 3.8 Asset Manager 资源管理

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator 运行时资源管理
- 能力包含：资源加载、资源缓存、资源释放、Asset Bundle
- 触发条件：动态加载资源、管理游戏资源、释放内存

## 概述

Asset Manager 是 Cocos Creator 提供的资源管理模块，用于帮助开发者管理资源的使用，大大提升开发效率和使用体验。相比之前的 loader，拥有更好的性能、更易用的 API，以及更强的扩展性。

## 核心功能

### 资源加载
```typescript
import { resources } from 'cc';

// 加载单个资源
resources.load('textures/gameBg', SpriteFrame, (err, spriteFrame) => {
    if (!err) {
        this.background.spriteFrame = spriteFrame;
    }
});

// 批量加载
resources.load(['textures/btn', 'textures/icon'], (completedCount, totalCount) => {
    const progress = completedCount / totalCount;
    console.log(`Loading: ${progress * 100}%`);
}, (err, assets) => {
    if (!err) {
        console.log('All assets loaded');
    }
});
```

### 资源查找
```typescript
import { resources } from 'cc';

// 查找资源（不加载）
const info = resources.getInfoById('textures/gameBg');
const info = resources.getInfoByUuid('xxx');

// 获取已加载的资源
const asset = resources.get('textures/gameBg');
```

### 资源释放
```typescript
import { resources } from 'cc';

// 释放单个资源
resources.release('textures/gameBg', SpriteFrame);

// 释放多个资源
resources.release(['textures/btn', 'textures/icon']);

// 释放指定资源及其依赖
resources.releaseUnusedAssets();

// 释放所有资源（慎用）
resources.releaseAll();
```

## Asset Bundle

### 概念
- 将资源打包成独立的 bundle
- 支持热更新
- 按需加载

### 配置
在 assets 目录下创建 bundle 配置：
```json
{
    "name": "levels",
    "path": "resources/levels",
    "compressionType": "zip"
}
```

### 加载 Bundle
```typescript
import { assetManager } from 'cc';

assetManager.loadBundle('levels', (err, bundle) => {
    if (!err) {
        bundle.load('level1', Prefab, (err, prefab) => {
            if (!err) {
                instantiate(prefab);
            }
        });
    }
});
```

### Bundle 管理
```typescript
// 获取已加载的 Bundle
const bundle = assetManager.getBundle('levels');

// 预加载 Bundle
assetManager.preloadBundle('levels', (progress, completedCount, totalCount) => {
    console.log(`Preloading: ${completedCount}/${totalCount}`);
}, (err) => {
    console.log('Preload complete');
});

// 卸载 Bundle
assetManager.removeBundle(bundle);
```

## 远程资源

### 加载远程资源
```typescript
import { remote } from 'cc';

remote.loadImage('https://example.com/image.png', (err, spriteFrame) => {
    if (!err) {
        this.image.spriteFrame = spriteFrame;
    }
});
```

### 远程包
```typescript
remote.loadRemoteBundle('https://example.com/bundle', (err, bundle) => {
    if (!err) {
        bundle.load('prefab');
    }
});
```

## 资源变化监听

### 监听资源变化
```typescript
import { AssetManager } from 'cc';

AssetManager.AssetLibrary.loadAssetInfoInRuntime('uuid-of-asset', (err, assetInfo) => {
    if (!err) {
        console.log('Asset info:', assetInfo);
    }
});
```

## 扩展资源管理器

### 自定义下载器
```typescript
import { assetManager } from 'cc';

assetManager.downloader.appendRegister({
    exts: ['.myformat'],
    downloader: (url, options, onComplete) => {
        // 自定义下载逻辑
        fetch(url)
            .then(res => res.arrayBuffer())
            .then(data => onComplete(null, data))
            .catch(err => onComplete(err));
    }
});
```

## 资源索引

### 必要参考
- [Asset Manager 概述](https://docs.cocos.com/creator/3.8/manual/zh/asset/manager.html)
- [资源加载升级指南](https://docs.cocos.com/creator/3.8/manual/zh/asset/asset-manager-upgrade-guide.html)

## 注意事项

### 内存管理
- 及时释放不需要的资源
- 使用 releaseUnusedAssets 清理缓存
- 注意循环引用

### 路径规范
- 动态加载路径相对于 resources 目录
- 不包含文件扩展名
- 使用 uuid 或相对路径

### 性能优化
- 善用预加载
- 批量加载减少请求
- 合理使用缓存策略