---
name: cocos-publish-skill
description: Cocos Creator 3.8 跨平台游戏发布，Web、iOS、Android 等平台构建
dependency:
  - cocos-intro-skill
---

# Cocos Creator 3.8 发布跨平台游戏

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator 多平台发布流程
- 能力包含：平台构建配置、Web 发布、原生平台发布
- 触发条件：发布游戏到各平台

## 概述

Cocos Creator 支持发布到多种平台，包括 Web（HTML5）、iOS、Android、微信小游戏、抖音小游戏等。

## 发布流程

### 通用步骤
1. 菜单栏选择"项目"->"构建发布"
2. 选择目标平台
3. 配置构建参数
4. 执行构建
5. 运行或上传

### Web 发布

#### 构建配置
- **横竖屏**：横屏/竖屏/自动
- **分辨率**：设计分辨率
- **调试模式**：是否开启调试

#### 构建
```bash
# 命令行构建
npm run build
```

#### 输出
- web-mobile 目录
- 包含 index.html 和游戏资源

### iOS 发布

#### 构建配置
- **App ID**：Apple Developer ID
- **签名证书**：开发/发布证书
- **目标设备**：iPhone/iPad/通用

#### 构建步骤
1. Xcode 打开构建后的项目
2. 配置签名证书
3. 选择目标设备
4. Archive 并导出

### Android 发布

#### 构建配置
- **包名**：Bundle Identifier
- **版本信息**：versionCode/versionName
- **屏幕方向**：横屏/竖屏

#### 构建输出
- APK（Debug/Release）
- AAB（Android App Bundle）

### 小游戏平台

#### 微信小游戏
- 配置 AppID
- 启用微信开发者工具
- 上传审核

#### 抖音小游戏
- 配置抖音开发者参数
- 使用抖音开发者工具

## 构建配置

### 项目设置
- 功能裁剪：选择需要的模块
- 分组管理：碰撞分组
- 自定义引擎：如有需要

### 渲染配置
- 2D/3D 模式
- 渲染后端：GLES3/GLES2/WebGL2/WebGL1

## 资源索引

### 必要参考
- [发布跨平台](https://docs.cocos.com/creator/3.8/manual/zh/publish/)
- [构建选项](https://docs.cocos.com/creator/3.8/manual/zh/publish/publish-options.html)

## 注意事项

### 平台差异
- 不同平台 API 差异
- 注意权限申请
- 平台特定功能

### 性能优化
- 针对目标平台优化
- 合理设置分辨率
- 压缩资源