---
name: requirement-parser
version: 0.1.0
description: 将用户描述的需求解析为结构化数据，支持交互补充和信息提取
---

# Requirement Parser

## 职责

- 从自然语言描述中提取需求信息
- 按功能/非功能/约束分类
- 识别需求模糊点并交互补充
- 输出结构化的需求摘要

## 输入

- 用户的项目描述文本
- 可选：需求文档路径

## 输出

```yaml
requirements:
  core_features:
    - name: 用户管理
      priority: must
      description: 支持注册、登录、密码重置
      acceptance_criteria: [...]
  non_functional:
    performance: "API响应 < 200ms"
    availability: "99.9% uptime"
    security: "JWT认证、HTTPS"
  constraints:
    - "数据必须存储在中国境内"
    - "支持 Chrome/Safari/Firefox 最新版"
  assumptions:
    - "用户量初期 < 1000 DAU"
```

## 解析维度

### 功能需求

- 核心业务流程
- 用户角色与权限
- 数据实体与关系
- 接口需求

### 非功能需求

- 性能指标
- 安全要求
- 可用性要求
- 兼容性要求
- 合规性要求

### 约束条件

- 技术约束
- 业务约束
- 时间/资源约束

## 交互补充规则

当检测到以下模糊描述时，主动询问用户：

| 模糊描述 | 应补充 |
|----------|--------|
| "性能要好" | 具体指标（响应时间、QPS） |
| "安全可靠" | 具体措施（加密、认证、备份） |
| "支持多端" | 具体平台（Web/iOS/Android） |
| "用户量会很大" | 具体预期（DAU/MAU） |

## 优先级分类

- **Must**: 核心功能，必须实现
- **Should**: 重要功能，应该实现
- **Could**: 锦上添花，可以实现
- **Won't**: 暂不实现

## 注意事项

- 保持交互节奏，一次最多问 3 个问题
- 用户未明确时，使用合理的默认值并标注 assumption
- 非功能需求是常见遗漏点，需主动识别
