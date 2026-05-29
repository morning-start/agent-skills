# 文档一致性规则

## 概述

本文档汇总了文档一致性检查的常见规则、问题模式和解决方案，为自动化检查和人工评审提供依据。

---

## 一、常见不一致问题及解决方案

### 1.1 版本号不一致

**问题模式**：
```
SKILL.md: version: 5.0.0
CHANGELOG.md: ## [4.0.0] - 2024-01-15
Git Tag: v4.5.0
```

**影响**：版本管理混乱，用户无法确定当前版本

**解决方案**：
1. 建立版本发布检查清单
2. 使用自动化脚本检查版本号
3. 版本发布时按顺序更新：
   - 更新 SKILL.md 版本号
   - 提交并创建 Git Tag
   - 更新 CHANGELOG.md
   - 更新 ROADMAP.md

**自动化检查脚本**：
```bash
#!/bin/bash
# check-version.sh

SKILL_VERSION=$(grep "^version:" SKILL.md | awk '{print $2}')
CHANGELOG_VERSION=$(grep "^## \[" CHANGELOG.md | head -1 | sed 's/## \[\(.*\)\].*/\1/')
GIT_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "none")

echo "SKILL.md version: $SKILL_VERSION"
echo "CHANGELOG version: $CHANGELOG_VERSION"
echo "Git Tag: $GIT_TAG"

if [ "$SKILL_VERSION" != "$CHANGELOG_VERSION" ]; then
    echo "❌ Version mismatch between SKILL.md and CHANGELOG.md"
    exit 1
fi

if [ "v$SKILL_VERSION" != "$GIT_TAG" ]; then
    echo "⚠️ Git tag does not match SKILL.md version"
fi

echo "✅ Version check passed"
```

---

### 1.2 日期格式不一致

**问题模式**：
```markdown
# 正确
## [1.0.0] - 2024-01-15

# 错误
## [1.0.0] - 2024/01/15
## [1.0.0] - 01/15/2024
## [1.0.0] - Jan 15, 2024
```

**影响**：日期解析错误，国际化问题

**解决方案**：
1. 统一使用 ISO 8601 格式：YYYY-MM-DD
2. 使用正则表达式验证日期格式
3. 在 CI/CD 中加入日期格式检查

**验证正则**：
```regex
^\d{4}-\d{2}-\d{2}$
```

---

### 1.3 术语混用

**问题模式**：
```
文档 A: "微服务架构"
文档 B: "微服务架构风格"
文档 C: "微服务架构模式"
文档 D: "Microservices Architecture"
```

**影响**：理解困难，专业度降低

**解决方案**：
1. 建立术语表（Glossary）
2. 首次出现时定义术语
3. 使用文本搜索工具检查术语使用

**术语表模板**：
```markdown
| 术语 | 英文 | 定义 | 使用场景 |
|------|------|------|---------|
| 微服务架构 | Microservices Architecture | 将应用程序构建为一组小型服务的架构风格 | 系统设计 |
| 模块 | Module | 代码组织的基本单元 | 代码设计 |
| 组件 | Component | 可独立部署的功能单元 | 系统架构 |
```

---

### 1.4 命名不一致

**问题模式**：
```
ER 图：user_table
数据字典：users
代码 ORM: User
API 文档：user
```

**影响**：开发混淆，集成困难

**解决方案**：
1. 制定命名规范文档
2. 使用代码生成工具保持同步
3. 定期审查命名一致性

**命名规范示例**：
```markdown
## 数据库命名
- 表名：复数名词，下划线分隔（users, order_items）
- 字段名：单数名词，下划线分隔（user_name, email）

## 代码命名
- 类名：PascalCase（User, Order）
- 方法名：camelCase（getUser, createOrder）
- 变量名：camelCase（userName, orderId）

## API 命名
- URL: 复数名词，kebab-case（/api/users, /api/order-items）
- 字段：camelCase（userName, orderId）
```

---

### 1.5 模板占位符未替换

**问题模式**：
```markdown
# 项目名称
{{project_description}}  # 忘记替换

## 版本
[VERSION] - YYYY-MM-DD  # 忘记替换
```

**影响**：文档不专业，信息缺失

**解决方案**：
1. 使用占位符检查脚本
2. 建立文档发布检查清单
3. 同行评审时重点检查

**检查脚本**：
```bash
#!/bin/bash
# check-placeholders.sh

PLACEHOLDERS=("{{" "}}" "[TODO]" "[待填写]" "TODO" "FIXME")

for file in $(find . -name "*.md"); do
    for placeholder in "${PLACEHOLDERS[@]}"; do
        if grep -q "$placeholder" "$file"; then
            echo "⚠️ Found placeholder in $file: $placeholder"
        fi
    done
done
```

---

## 二、一致性检查自动化建议

### 2.1 可自动化的检查项

| 检查项 | 自动化难度 | 建议工具 | 检查频率 |
|--------|-----------|---------|---------|
| 版本号一致性 | 高 | 自定义脚本 | 每次提交 |
| 日期格式 | 高 | 正则表达式 | 每次提交 |
| 文档命名 | 高 | Shell 脚本 | 每次提交 |
| Markdown 语法 | 高 | markdownlint | 每次提交 |
| 链接有效性 | 中 | markdown-link-check | 每天 |
| Mermaid 语法 | 中 | mermaid-cli | 每次提交 |
| 占位符检查 | 高 | Shell 脚本 | 每次提交 |
| 术语频率 | 低 | 文本分析工具 | 每周 |

### 2.2 半自动化的检查项

| 检查项 | 自动化部分 | 人工部分 | 建议流程 |
|--------|-----------|---------|---------|
| 需求 - 设计对齐 | 提取关键词 | 判断语义一致性 | 工具提取 + 人工评审 |
| 设计 - 实现对齐 | 代码覆盖率 | 判断实现质量 | 覆盖率报告 + 代码审查 |
| 术语一致性 | 术语频率统计 | 判断是否合理 | 工具统计 + 人工判断 |
| 图表 - 文字一致 | 提取组件名 | 判断逻辑一致性 | 工具提取 + 人工对比 |

### 2.3 需要人工的检查项

| 检查项 | 原因 | 建议方法 |
|--------|------|---------|
| 内容逻辑一致性 | 需要理解业务语义 | 文档评审会议 |
| 角色权限一致性 | 涉及安全策略 | 安全专家评审 |
| 时间进度一致性 | 需要项目管理信息 | 项目状态会议 |
| 变更影响分析 | 需要综合判断 | 变更控制委员会 |

---

## 三、自动化检查工具集

### 3.1 Markdown 格式检查

**工具**：markdownlint

**安装**：
```bash
npm install -g markdownlint-cli
```

**配置**（.markdownlintrc）：
```json
{
  "default": true,
  "MD001": {"level": 2},  // 标题层级
  "MD004": {"style": "dash"},  // 列表符号
  "MD007": {"indent": 2},  // 列表缩进
  "MD013": false,  // 禁用行长度检查
  "MD024": false,  // 允许重复标题
  "MD033": false   // 允许 HTML
}
```

**使用**：
```bash
markdownlint **/*.md
```

---

### 3.2 链接检查

**工具**：markdown-link-check

**安装**：
```bash
npm install -g markdown-link-check
```

**使用**：
```bash
# 检查单个文件
markdown-link-check README.md

# 批量检查
find . -name "*.md" -exec markdown-link-check {} \;
```

---

### 3.3 Mermaid 图表验证

**工具**：mermaid-cli

**安装**：
```bash
npm install -g @mermaid-js/mermaid-cli
```

**使用**：
```bash
# 渲染验证
mmdc -i diagram.mmd -o diagram.png
```

---

### 3.4 综合检查脚本

**脚本**：check-consistency.sh

```bash
#!/bin/bash
# 文档一致性综合检查脚本

echo "=== 文档一致性检查 ==="
echo ""

# 1. 版本号检查
echo "1. 检查版本号一致性..."
SKILL_VERSION=$(grep "^version:" SKILL.md | awk '{print $2}')
CHANGELOG_VERSION=$(grep "^## \[" CHANGELOG.md | head -1 | sed 's/## \[\(.*\)\].*/\1/')

if [ "$SKILL_VERSION" = "$CHANGELOG_VERSION" ]; then
    echo "   ✅ 版本号一致：$SKILL_VERSION"
else
    echo "   ❌ 版本号不一致：SKILL.md($SKILL_VERSION) vs CHANGELOG.md($CHANGELOG_VERSION)"
fi

# 2. 日期格式检查
echo ""
echo "2. 检查日期格式..."
INVALID_DATES=$(grep -E "^\d{4}[\/\.]\d{2}[\/\.]\d{2}" CHANGELOG.md || true)
if [ -z "$INVALID_DATES" ]; then
    echo "   ✅ 日期格式正确"
else
    echo "   ❌ 发现错误日期格式："
    echo "$INVALID_DATES"
fi

# 3. 占位符检查
echo ""
echo "3. 检查占位符..."
PLACEHOLDERS=$(grep -rE "\{\{.*\}\}|\[TODO\]|\[待填写\]" --include="*.md" . || true)
if [ -z "$PLACEHOLDERS" ]; then
    echo "   ✅ 无占位符"
else
    echo "   ⚠️ 发现未替换占位符："
    echo "$PLACEHOLDERS" | head -10
fi

# 4. Markdown 语法检查
echo ""
echo "4. 检查 Markdown 语法..."
if command -v markdownlint &> /dev/null; then
    MD_ERRORS=$(markdownlint **/*.md 2>&1 | grep -v "^$" || true)
    if [ -z "$MD_ERRORS" ]; then
        echo "   ✅ Markdown 格式正确"
    else
        echo "   ⚠️ Markdown 格式问题（前 10 条）："
        echo "$MD_ERRORS" | head -10
    fi
else
    echo "   ⚠️ markdownlint 未安装，跳过"
fi

# 5. 文档存在性检查
echo ""
echo "5. 检查核心文档..."
CORE_DOCS=("README.md" "CHANGELOG.md" "ROADMAP.md" "ARCHITECTURE.md" "SKILL.md")
for doc in "${CORE_DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo "   ✅ $doc 存在"
    else
        echo "   ❌ $doc 缺失"
    fi
done

echo ""
echo "=== 检查完成 ==="
```

---

## 四、CI/CD 集成

### 4.1 GitHub Actions 工作流

**文件**：.github/workflows/consistency-check.yml

```yaml
name: Document Consistency Check

on:
  push:
    paths:
      - '**/*.md'
      - 'SKILL.md'
  pull_request:
    paths:
      - '**/*.md'
      - 'SKILL.md'

jobs:
  consistency:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install tools
        run: |
          npm install -g markdownlint-cli
          npm install -g markdown-link-check
      
      - name: Check version consistency
        run: |
          SKILL_VERSION=$(grep "^version:" SKILL.md | awk '{print $2}')
          CHANGELOG_VERSION=$(grep "^## \[" CHANGELOG.md | head -1 | sed 's/## \[\(.*\)\].*/\1/')
          if [ "$SKILL_VERSION" != "$CHANGELOG_VERSION" ]; then
            echo "Version mismatch: SKILL.md($SKILL_VERSION) vs CHANGELOG.md($CHANGELOG_VERSION)"
            exit 1
          fi
      
      - name: Check Markdown files
        run: markdownlint **/*.md
      
      - name: Check links
        run: |
          find . -name "*.md" -exec markdown-link-check {} \; || true
      
      - name: Check placeholders
        run: |
          if grep -rE "\{\{.*\}\}|\[TODO\]|\[待填写\]" --include="*.md" .; then
            echo "Found unreplaced placeholders"
            exit 1
          fi
      
      - name: Generate report
        run: |
          echo "# Consistency Check Report" > report.md
          echo "" >> report.md
          echo "Date: $(date -u)" >> report.md
          echo "Status: ✅ Passed" >> report.md
```

---

## 五、最佳实践总结

### 5.1 预防不一致

1. **使用模板**：所有文档从模板开始
2. **定义规范**：明确的命名规范、格式规范
3. **自动化检查**：在 CI/CD 中集成检查
4. **同行评审**：文档发布前必须评审

### 5.2 发现不一致

1. **定期检查**：每周/每月运行检查脚本
2. **工具辅助**：使用自动化工具发现问题
3. **度量指标**：跟踪一致性指标（如通过率）

### 5.3 修复不一致

1. **优先级排序**：先修复高优先级问题
2. **跟踪进度**：使用问题跟踪系统
3. **验证修复**：修复后重新运行检查

---

## 参考资料

- [文档一致性检查指南](../../guides/document/consistency-check-guide.md)
- [一致性检查清单模板](../templates/consistency-checklist-template.md)
- [基础文档清单](../../guides/document/basic-docs-checklist.md)
