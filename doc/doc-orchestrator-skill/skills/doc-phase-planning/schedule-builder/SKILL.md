---
name: schedule-builder
version: 0.1.0
description: 根据文档依赖关系生成执行计划
---

# Schedule Builder

## 职责

- 分析文档间的依赖关系
- 生成有向无环图（DAG）执行顺序
- 输出可并行化的执行计划
- 支持分阶段执行

## 输入

- 文档清单（含依赖关系）

## 输出

```yaml
execution_schedule:
  phases:
    - phase: 1
      parallel: [REQ-001, REQ-002]
      description: "需求文档可并行生成"
    - phase: 2
      parallel: [ARCH-001]
      depends_on: [REQ-001, REQ-002]
      description: "架构文档依赖需求文档"
    - phase: 3
      parallel: [API-001, DATA-001]
      depends_on: [ARCH-001]
      description: "API和数据文档可并行"
  total_phases: 3
  estimated_parallelism: 2
```

## 算法

1. 构建依赖图（邻接表）
2. 拓扑排序得到执行顺序
3. 按拓扑层级分组可并行任务
4. 检测循环依赖并报错

## 注意事项

- 循环依赖必须报错，不能继续执行
- 同一 phase 内的文档无依赖关系，可并行
- phase 数应最小化，充分利用并行度
