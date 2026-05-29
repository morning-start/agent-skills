# 进阶功能

## 概览

本章节介绍代码优化专家技能的高级功能，包括交互式重构、测试用例生成和技术债务量化。

---

## 1. 交互式重构

### 理念

不要一次性输出所有修改，而是采用对话式交互，让用户选择优先关注的问题。

### 工作流程

```
1. 初步扫描
   └─ 检测到 N 个主要问题
        ↓
2. 问题列表
   └─ 展示优先级和简要描述
        ↓
3. 用户选择
   └─ "您想先看哪个问题？"
        ↓
4. 详细分析
   └─ 针对选定问题深入分析
        ↓
5. 重构方案
   └─ 提供具体代码和验证方法
        ↓
6. 循环迭代
   └─ "还需要查看其他问题吗？"
```

### 示例对话

**AI**:
```
🛡️ 代码扫描完成

检测到 3 个主要问题：

1. 🔴 SQL 注入漏洞 (P0 - 严重)
   - 位置：第 34 行
   - 风险：可能导致数据泄露
   - 建议：立即修复

2. 🟠 N+1 查询问题 (P1 - 性能)
   - 位置：第 23-28 行
   - 影响：查询次数爆炸（2n 次）
   - 建议：改为批量查询

3. 🟡 缺少类型注解 (P2 - 可维护性)
   - 位置：函数签名
   - 影响：IDE 提示不准确
   - 建议：添加 TypeScript 类型

您想先看哪个问题的详细分析和重构方案？
（回复数字 1、2 或 3）
```

**用户**: `1`

**AI**:
```
好的，我们先看 **SQL 注入漏洞** 的详细分析：

### 🔴 问题 1: SQL 注入漏洞

**位置**: 第 34 行

**问题代码**:
```python
def get_user(username: str) -> Optional[User]:
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)
```

**风险分析**:
- 🔴 严重安全漏洞
- 攻击者可构造恶意 username: `admin' OR '1'='1`
- 导致绕过认证、数据泄露

**重构方案**:
```python
def get_user(username: str) -> Optional[User]:
    query = "SELECT * FROM users WHERE username = ?"
    params = [username]
    return db.execute(query, params)
```

**验证方法**:
1. 运行安全测试：`pytest tests/test_security.py`
2. 尝试注入：`username = "admin' OR '1'='1"`
3. 验证无法注入

---

接下来您想看哪个问题？
- 回复 `2`: N+1 查询问题
- 回复 `3`: 缺少类型注解
- 回复 `done`: 完成
```

### 实现策略

#### System Prompt 设计

```
你是一位代码优化专家，采用交互式重构策略。

当检测到多个问题时：
1. 先列出所有问题的摘要（优先级 + 简要描述）
2. 询问用户想先看哪个问题
3. 针对用户选择的问题提供详细分析
4. 完成后询问是否继续查看其他问题

原则：
- 一次只深入分析一个问题
- 保持对话友好、专业
- 提供可执行的代码示例
- 量化影响和风险
```

#### 上下文管理

```python
# 伪代码示例
class InteractiveRefactoring:
    def __init__(self, code: str):
        self.code = code
        self.issues = []
        self.current_issue = None
    
    def scan(self) -> List[Issue]:
        """初步扫描，返回问题摘要"""
        self.issues = self._detect_issues()
        return [issue.summary() for issue in self.issues]
    
    def analyze(self, issue_index: int) -> DetailedAnalysis:
        """深入分析指定问题"""
        self.current_issue = self.issues[issue_index]
        return self.current_issue.detailed_analysis()
    
    def next_issue(self) -> Optional[int]:
        """返回下一个未查看的问题索引"""
        for i, issue in enumerate(self.issues):
            if not issue.viewed:
                return i
        return None
```

---

## 2. 测试用例生成

### 理念

在优化代码的同时，自动生成对应的单元测试，确保重构没有破坏原有逻辑。

### 测试覆盖策略

#### 1. 边界条件测试

```python
# 原始函数
def calculate_discount(amount: float, is_vip: bool) -> float:
    if amount > 1000:
        return 0.9 if is_vip else 0.95
    return 1.0

# 生成的测试用例
def test_calculate_discount_boundary():
    """测试边界条件"""
    # 刚好低于阈值
    assert calculate_discount(1000, False) == 1.0
    assert calculate_discount(1000, True) == 1.0
    
    # 刚好超过阈值
    assert calculate_discount(1000.01, False) == 0.95
    assert calculate_discount(1000.01, True) == 0.9
    
    # 零值
    assert calculate_discount(0, False) == 1.0
    
    # 极大值
    assert calculate_discount(1_000_000, True) == 0.9
```

#### 2. 正常流程测试

```python
def test_calculate_discount_normal_cases():
    """测试正常流程"""
    # 普通用户，小额
    assert calculate_discount(500, False) == 1.0
    
    # 普通用户，大额
    assert calculate_discount(2000, False) == 0.95
    
    # VIP 用户，小额
    assert calculate_discount(500, True) == 1.0
    
    # VIP 用户，大额
    assert calculate_discount(2000, True) == 0.9
```

#### 3. 异常流程测试

```python
def test_calculate_discount_edge_cases():
    """测试异常流程"""
    # 负数金额（应该抛出异常或特殊处理）
    with pytest.raises(ValueError):
        calculate_discount(-100, False)
    
    # NaN（应该抛出异常）
    with pytest.raises(ValueError):
        calculate_discount(float('nan'), False)
    
    # 无穷大
    assert calculate_discount(float('inf'), True) == 0.9
```

#### 4. 属性基测试 (Property-Based Testing)

```python
from hypothesis import given, strategies as st

@given(
    amount=st.floats(min_value=0, max_value=1_000_000),
    is_vip=st.booleans()
)
def test_calculate_discount_properties(amount, is_vip):
    """属性基测试"""
    discount = calculate_discount(amount, is_vip)
    
    # 折扣率必须在 0-1 之间
    assert 0 <= discount <= 1
    
    # VIP 的折扣不会比普通用户差
    if is_vip:
        assert discount <= calculate_discount(amount, False)
    
    # 金额超过阈值一定有折扣
    if amount > 1000:
        assert discount < 1.0
```

### 测试生成模板

```markdown
### 5. 推荐测试用例

#### 单元测试

```python
# 测试空输入
def test_empty_input():
    assert process_orders([]) == []

# 测试正常流程
def test_normal_flow():
    order = Order(
        status=OrderStatus.PENDING_PAYMENT,
        amount=1000,
        user=User(is_vip=False)
    )
    result = process_orders([order])
    assert result == [950.0]

# 测试边界条件
def test_boundary_conditions():
    # 刚好等于阈值
    order = Order(amount=1000, is_vip=False)
    assert calculate_discount(order) == 1.0
    
    # 超过阈值 0.01
    order = Order(amount=1000.01, is_vip=False)
    assert calculate_discount(order) == 0.95

# 测试异常处理
def test_exception_handling():
    with pytest.raises(ValueError):
        process_orders(None)
    
    with pytest.raises(ValueError):
        process_orders([Order(amount=-100)])
```

#### 集成测试

```python
def test_integration_with_database():
    """测试与数据库的集成"""
    # 创建测试数据
    order = create_order_in_db(amount=2000, is_vip=True)
    
    # 处理订单
    result = process_orders_from_db(order.id)
    
    # 验证结果
    assert result.final_price == 1800.0
    assert result.status == 'processed'
```

#### 性能测试

```python
import pytest

@pytest.mark.performance
def test_performance_with_large_dataset():
    """测试大数据集性能"""
    orders = [Order(amount=1000) for _ in range(10_000)]
    
    import time
    start = time.time()
    process_orders(orders)
    elapsed = time.time() - start
    
    # 要求 1 秒内完成
    assert elapsed < 1.0
```
```

### 测试覆盖率目标

| 代码类型 | 覆盖率目标 | 说明 |
|----------|------------|------|
| **核心业务逻辑** | > 95% | 支付、订单等 |
| **公共 API** | > 90% | 对外接口 |
| **工具函数** | > 80% | 辅助函数 |
| **前端组件** | > 70% | UI 组件 |

---

## 3. 技术债务量化

### 理念

将抽象的"代码质量问题"量化为具体的"小时数"，便于优先级排序和资源分配。

### 债务评估模型

#### 债务构成

```
技术债务 = 重复代码 + 缺少测试 + 文档缺失 + 架构问题 + 安全漏洞

各项权重：
- 安全漏洞：5x（立即修复）
- 架构问题：3x（高优先级）
- 重复代码：2x（中等优先级）
- 缺少测试：2x（中等优先级）
- 文档缺失：1x（低优先级）
```

#### 估算方法

| 问题类型 | 单位 | 估算时间 | 复杂度系数 |
|----------|------|----------|------------|
| 修复安全漏洞 | 个 | 1-2 小时 | 2.0 |
| 重构重复代码 | 处 | 1-2 小时 | 1.5 |
| 拆分大函数 | 个 | 1-2 小时 | 1.5 |
| 补充单元测试 | 函数 | 30 分钟 -1 小时 | 1.0 |
| 添加文档注释 | 函数 | 15-30 分钟 | 0.5 |
| 优化性能瓶颈 | 个 | 2-4 小时 | 2.0 |

### 评估报告模板

```markdown
### 技术债务评估

**当前债务**: 12.5 小时

**债务构成**:
```
安全漏洞：    ████░░░░░░  2.0 小时 (16%)
重复代码：    ██████░░░░  3.0 小时 (24%)
缺少测试：    ████████░░  4.0 小时 (32%)
文档缺失：    ██░░░░░░░░  1.0 小时 (8%)
架构问题：    ███░░░░░░░  2.5 小时 (20%)
```

**债务分布**:
- 支付模块：6.0 小时
- 用户模块：3.5 小时
- 订单模块：2.0 小时
- 工具函数：1.0 小时

**债务趋势**:
- 本月新增：+3.5 小时
- 本月偿还：-1.0 小时
- 净增长：+2.5 小时/月

**建议优先级**:
1. 🔴 修复 P0 安全漏洞（立即，2 小时）
2. 🟠 优化支付模块性能（本周，3 小时）
3. 🟡 补充核心逻辑测试（下周，4 小时）
4. 🟢 清理重复代码（技术债务，3.5 小时）

**偿还计划**:
- 每周安排 2 小时技术债务清理
- 预计 6-8 周还清当前债务
- 建议设立"技术债务日"（每月最后一天）
```

### 债务跟踪工具

#### 代码注释标记

```python
# TODO[TECH-DEBT]: 提取重复的折扣计算逻辑
# 估算：1 小时
# 优先级：P2
# 创建日期：2024-01-15

# FIXME[SECURITY]: 此处存在 SQL 注入风险
# 估算：2 小时
# 优先级：P0
# 创建日期：2024-01-10

# HACK[PERF]: 临时性能优化，需要更好的方案
# 估算：4 小时
# 优先级：P1
# 创建日期：2024-01-12
```

#### 债务跟踪表

| ID | 模块 | 问题描述 | 类型 | 估算 | 优先级 | 创建日期 | 状态 |
|----|------|----------|------|------|--------|----------|------|
| TD-001 | 支付 | SQL 注入风险 | 安全 | 2h | P0 | 2024-01-10 | Open |
| TD-002 | 订单 | 重复代码 | 重复 | 1.5h | P2 | 2024-01-12 | Open |
| TD-003 | 用户 | 缺少测试 | 测试 | 3h | P1 | 2024-01-15 | In Progress |

### 债务可视化

#### 债务燃尽图

```
技术债务燃尽图

15 │
   │●
12 │  ●
   │    ●
10 │      ●
   │        ●
 8 │          ●
   │            ●
 6 │              ●
   │                ●
 4 │                  ●
   │                    ●
 2 │                      ●
   │                        ●
 0 └─────────────────────────
   1  2  3  4  5  6  7  8  周
   
目标线 ──  实际线 ●
```

#### 债务分布饼图

```
技术债务分布

        安全漏洞 16%
      ┌───────────┐
    ╱│              │╲
   │ │  缺少测试    │ │
   │ │    32%       │ │
   │ │              │ │
   │ │   重复代码    │ │
    ╲│    24%      ╱│
      └───────────┘
        架构问题 20%
        文档缺失 8%
```

---

## 4. 性能基准测试

### 理念

优化前后都应该有性能数据支撑，避免"感觉变快了"。

### 基准测试模板

```python
import timeit
from contextlib import contextmanager

@contextmanager
def benchmark(name: str, iterations: int = 1000):
    """性能测试上下文管理器"""
    start = timeit.default_timer()
    try:
        yield
    finally:
        elapsed = timeit.default_timer() - start
        avg_ms = (elapsed / iterations) * 1000
        print(f"{name}: {avg_ms:.3f} ms/op ({iterations} 次)")

# 使用示例
def test_performance():
    data = list(range(1000))
    
    with benchmark("优化前", iterations=1000):
        result = process_before(data)
    
    with benchmark("优化后", iterations=1000):
        result = process_after(data)
```

### 性能对比报告

```markdown
### 性能测试结果

**测试环境**:
- CPU: Intel i7-10700K
- 内存：32GB DDR4
- Python: 3.9.7

**测试场景**: 处理 10,000 条订单

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| **执行时间** | 5,230ms | 120ms | 97.7% |
| **内存占用** | 450MB | 85MB | 81.1% |
| **CPU 使用** | 85% | 25% | 70.6% |
| **GC 次数** | 15 | 3 | 80.0% |

**详细分析**:

```
优化前：████████████████████████████████████████ 5,230ms
优化后：█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  120ms
提升：    ████████████████████████████████████ 97.7%
```

**瓶颈分析**:
- 优化前：N+1 查询（占 85% 时间）
- 优化后：JSON 序列化（占 60% 时间）

**下一步优化方向**:
1. 使用更快的 JSON 库（orjson）
2. 批量序列化
3. 考虑使用 Protobuf
```

---

## 5. 自动化集成

### CI/CD 集成

```yaml
# GitHub Actions 示例
name: Code Quality

on: [push, pull_request]

jobs:
  code-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Linter
        run: |
          pip install pylint flake8 black
          pylint src/
          flake8 src/
          black --check src/
      
      - name: Run Security Scan
        run: |
          pip install bandit
          bandit -r src/
      
      - name: Run Tests
        run: |
          pip install pytest pytest-cov
          pytest --cov=src tests/
      
      - name: Code Coverage
        run: |
          pytest --cov=src --cov-report=xml
          bash <(curl -s https://codecov.io/bash)
      
      - name: Performance Test
        run: |
          pytest tests/perf/ -v
```

### 自动化报告生成

```python
# 自动生成代码优化报告
def generate_optimization_report(code_path: str) -> str:
    """生成完整的代码优化报告"""
    issues = scan_code(code_path)
    report = MarkdownReport()
    
    report.add_header("代码优化分析报告")
    report.add_summary(issues)
    
    for issue in issues.by_priority():
        report.add_issue(issue)
        report.add_refactoring_suggestion(issue)
        report.add_test_cases(issue)
    
    report.add_technical_debt_assessment(issues)
    report.add_performance_benchmarks()
    
    return report.render()
```

---

## 参考资源

- **交互式重构**: JetBrains, "The Art of Refactoring"
- **测试生成**: Test-Driven Development, Kent Beck
- **技术债务**: Martin Fowler, Technical Debt Quadrant
- **性能基准**: Brendan Gregg, Performance Analysis Methodology
- **CI/CD**: Continuous Delivery, Jez Humble
