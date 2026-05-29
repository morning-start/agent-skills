# 双存储方案

> 本文档定义了决策记录系统的双存储架构：JSON 文件作为持久化主存储，Memory 机制作为运行时缓存。

## 方案对比与选择理由

| 维度 | 方案 A: JSON 文件 | 方案 B: Memory 机制 | 推荐 |
|------|---------------|------------------|------|
| **持久性** | ✅ 永久保存 | ❌ 会话结束丢失 | **JSON 胜** |
| **可读性** | ✅ 人可直接编辑 | ⚠️ 需工具解析 | **JSON 胜** |
| **版本控制** | ✅ Git 天然支持 | ❌ 无版本历史 | **JSON 胜** |
| **访问速度** | ⚠️ 需要文件 I/O | ✅ 内存直接访问 | **Memory 胜** |
| **跨会话** | ✅ 多会话共享 | ❌ 单会话隔离 | **JSON 胜** |
| **实时性** | ⚠️ 需显式保存 | ✅ 自动同步 | **Memory 胜** |

**最终推荐：双轨制（JSON 主 + Memory 辅）**

```
┌─────────────────────────────────────────┐
│           双存储架构                     │
│                                         │
│  ┌─────────────┐    ┌─────────────┐    │
│  │ JSON 文件    │◄──►│ Memory 缓存  │   │
│  │ (持久化存储) │    │ (运行时缓存) │   │
│  └──────┬──────┘    └──────┬──────┘    │
│         │                  │           │
│    主存储(SoT)         运行时镜像       │
│                                         │
│  同步策略：                                │
│  - 启动时：JSON → Memory（加载）          │
│  - 运行中：Memory 实时更新                │
│  - 保存时：Memory → JSON（持久化）        │
│  - 定期：自动保存（每 5 分钟或每次状态变更）  │
└─────────────────────────────────────────┘
```

## JSON 文件规范

**文件位置**：
```
{项目根目录}/decision-record.json
```

**文件结构**（详见 `../../assets/decision-record-template.json`）：

```json
{
  "metadata": {
    "project_name": "《RAG 从入门到生产实践》",
    "version": "v1.0.0",
    "created_at": "2026-05-25T00:00:00+08:00",
    "last_updated": "2026-05-25T12:00:00+08:00",
    "statistics": { ... }
  },
  "decisions": {
    "basic_lang_primary": { ... },
    "tech_primary_language": { ... }
    // 共 20 个预定义决策项
  },
  "discussion_sessions": [ ... ],
  "version_history": [ ... ]
}
```

**Schema 校验**：
- 使用 `../../assets/decision-record-schema.json` 进行校验
- 每次读写后验证数据完整性

## Memory 机制集成

**Memory 键命名规范**：

```
decision:{decision_id}:{field}

示例：
  decision:basic_lang_primary:current_value  → "zh-CN"
  decision:basic_lang_primary:status         → "confirmed"
  decision:tech_framework_preference:current_value → ["langchain", "llamaindex"]
```

**Memory 操作原语**：

```python
# 伪代码 - Agent 实际调用方式

def load_decision(decision_id):
    """从 Memory 加载单个决策"""
    return memory.get(f"decision:{decision_id}")

def save_decision(decision_id, data):
    """保存决策到 Memory"""
    memory.set(f"decision:{decision_id}", data)
    schedule_persist()

def get_all_decisions():
    """获取所有决策的摘要"""
    decisions = memory.search("decision:*")
    return format_summary(decisions)

def persist_to_json():
    """将 Memory 中的决策同步到 JSON 文件"""
    all_data = collect_from_memory()
    validate_schema(all_data)
    write_file("decision-record.json", all_data)
    update_version_history()
```

## 同步与一致性保证

**同步时机**：

| 触发事件 | 操作 | 说明 |
|---------|------|------|
| 会话启动 | JSON → Memory | 加载已有决策到内存 |
| 决策确认 | Memory 更新 + 标记 dirty | 用户确认选择后 |
| 决策修改 | Memory 更新 + 标记 dirty | 变更请求处理后 |
| 讨论结束 | Memory 更新 + 立即持久化 | 讨论会话关闭时 |
| 定时器(5min) | dirty 检查 → 持久化 | 自动保存机制 |
| 会话结束 | 强制持久化 | 确保不丢失数据 |

**冲突解决策略**：

```
检测到 JSON 与 Memory 不一致时：

  1. 比较时间戳
     ├─ JSON 更新 → 以 JSON 为准，覆盖 Memory（可能其他会话修改）
     └─ Memory 更新 → 以 Memory 为准，覆盖 JSON（当前会话的最新操作）

  2. 若时间戳相同（罕见）
     → 提示用户手动选择
     → 记录冲突日志

  3. 持久化成功后清除 dirty 标记
```

---

**最后更新**: 2026-05-25
**版本**: v1.0.0
**作者**: RAG 教程项目组 + Skill Factory 优化
