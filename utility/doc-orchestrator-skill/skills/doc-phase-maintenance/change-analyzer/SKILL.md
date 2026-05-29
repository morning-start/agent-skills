---
name: change-analyzer
version: 0.1.0
description: 分析需求变更对文档链路的影响范围
---

# Change Analyzer

## 职责

- 分析变更内容
- 追溯受影响的文档链路
- 评估影响程度
- 输出变更影响报告

## 输入

- 变更描述
- 现有文档集

## 输出

```yaml
change_impact_report:
  change_type: modify
  change_description: "登录方式改为支持手机号验证码"
  affected_docs:
    - id: "REQ-001"
      type: "requirement/srs"
      impact: "modify"
      sections: ["3.功能需求 - 用户认证"]
      reason: "需求描述变更"
    - id: "REQ-002"
      type: "requirement/prd"
      impact: "modify"
      sections: ["4.功能清单"]
      reason: "功能清单变更"
    - id: "ARCH-001"
      type: "architecture/sad"
      impact: "modify"
      sections: ["5.模块设计 - 认证服务"]
      reason: "认证模块需增加短信服务依赖"
    - id: "API-001"
      type: "api"
      impact: "modify"
      sections: ["6.1 认证模块"]
      reason: "新增 /api/v1/auth/sms-login 接口"
    - id: "TEST-001"
      type: "quality/test"
      impact: "modify"
      sections: ["2.测试类型"]
      reason: "需增加短信验证码相关测试用例"
  impact_summary:
    total_affected: 5
    require: 2
    architecture: 1
    api: 1
    quality: 1
  risk_assessment: low
```

## 追溯规则

从变更点出发，沿追溯链分析影响：

```
变更 → REQ → ARCH → API/DATA → TEST
              ↓
            OPS/SEC
```

## 影响程度评估

| 程度 | 条件 | 处理 |
|------|------|------|
| low | 仅修改描述，不影响结构 | 标注 minor 变更 |
| medium | 新增/修改接口或模块 | 需要同步更新 |
| high | 架构变更，影响多个文档 | 需要重新规划 |
| critical | 核心需求变更 | 需要重新生成 |

## 注意事项

- 追溯链必须完整，不能遗漏
- 风险评估基于影响程度和变更范围
- 输出报告必须包含具体的变更章节
- 分析结果作为 doc-syncer 的输入
