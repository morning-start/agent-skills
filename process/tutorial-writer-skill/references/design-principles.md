# 设计原则 — Tutorial Writer v3

> 全局共享设计原则，所有 5 个子技能通用。

## 三大铁律

```
① 层级 ≤3 层 (references/assets 不算子技能层级)
② NO SKILL WITHOUT USE CASE IN AGENTS
③ description 只写触发条件 (CSO 格式)
```

## 子技能命名规范

```
tutorial-writer-{role}/

{role} 取值:
  research  调研与规划
  writing   撰写执行
  review    质量校验
  publish   网页发布
  decision  决策贯穿
```

## 子技能自含原则

每个子技能必须包含：

| 组件 | 是否必须 | 说明 |
|------|---------|------|
| SKILL.md | ✅ | 独立 description，Agent 可直接触发 |
| references/ | ✅ | 至少包含一个阶段性决策细则 |
| 阶段映射 | ✅ | 明确本子技能在 PRWRD+D 中的位置 |

## 引用规则

- 子技能间不允许相互引用（避免循环依赖）
- 全局 references/ 可被所有子技能引用
- 子技能内部 references/ 仅本技能使用

## CSO 描述规范

```
Use when {触发场景}
```

- 必须包含 "Use when" 或 "Use when..."
- 描述本技能解决的**用户问题**而非技术实现
- max 1024 字符
