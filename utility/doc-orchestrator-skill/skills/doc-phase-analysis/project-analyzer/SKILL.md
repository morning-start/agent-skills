---
name: project-analyzer
version: 0.1.0
description: 分析项目类型、规模和技术栈，为文档规划提供基础数据
---

# Project Analyzer

## 职责

- 识别项目类型（前端/后端/全栈/移动/桌面/游戏/CLI）
- 估算项目规模（小/中/大）
- 识别技术栈和依赖
- 识别目标平台

## 输入

- 项目描述文本
- 可选：代码仓库路径、package.json、pom.xml 等配置文件

## 输出

```yaml
analysis_result:
  project_type: fullstack
  scale: medium
  scale_factors:
    feature_count: 15
    estimated_modules: 8
    team_size: 3
  tech_stack:
    frontend: [react, typescript, tailwind]
    backend: [nodejs, express]
    database: [postgresql]
    infrastructure: [docker, aws]
  platforms: [web]
  complexity_level: moderate
```

## 分析规则

### 项目类型识别

| 检测特征 | 项目类型 |
|----------|---------|
| 包含前端框架 + 后端框架 | fullstack |
| 仅前端框架 | frontend |
| 仅后端框架 | backend |
| iOS/Android/React Native/Flutter | mobile |
| Electron/Tauri/WPF | desktop |
| Unity/Unreal/Godot | game |
| 无界面，纯命令行 | cli |

### 规模估算

| 维度 | 小 | 中 | 大 |
|------|-----|-----|-----|
| 功能数量 | <10 | 10-30 | >30 |
| 模块数量 | <5 | 5-15 | >15 |
| 团队规模 | 1-2 | 3-10 | >10 |

### 技术栈识别优先级

1. 从配置文件中提取（package.json、pom.xml、go.mod）
2. 从代码导入语句中识别
3. 从项目描述中关键词匹配
4. 用户补充确认

## 注意事项

- 不确定时主动询问用户，不要猜测
- 规模估算仅作为文档裁剪参考，不强制
- 技术栈识别需记录置信度
