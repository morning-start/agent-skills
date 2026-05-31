# 命名规范详解

> **版本**: v1.0.0 | **最后更新**: 2026-05-31
> **所属技能**: tutorial-writer-content | **角色**: data-layer

## 1. 概述

本文档详细说明 Tutorial Writer 项目中所有内容文件的命名规范。统一的命名约定是确保项目可维护性、可读性和跨平台兼容性的基础。

## 2. 核心原则

### 2.1 设计理念

```
好的命名 = 见名知意 + 机器友好 + 人类可读
```

**三大目标**:

1. **语义清晰**: 文件名能直接表达内容主题
2. **URL 友好**: 生成的链接简洁、专业、易分享
3. **跨平台一致**: Windows/Linux/macOS 行为完全相同

### 2.2 为什么选择英文 slug？

| 因素 | 中文文件名 | 英文 Slug |
|------|-----------|----------|
| URL 编码 | `%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B` (冗长) | `getting-started` (简洁) |
| Git 兼容 | 大小写敏感问题（Windows vs Linux） | 无问题 |
| SEO 优化 | URL 可读性差 | URL 即关键词 |
| 终端操作 | 需要切换输入法 | 直接输入 |

**结论**: 使用英文 slug 作为文件名，中文标题存储在 Frontmatter 的 `title` 字段中。

## 3. 文件命名规则详解

### 3.1 基本格式

```regex
^{[a-z0-9]}([a-z0-9-]*[a-z0-9])?\.md$
```

**组成部分**:

```
{primary-keyword}-{secondary-keyword}.md
 ↑                    ↑                ↑
 │                    │                └── 扩展名（固定 .md）
 │                    └── 可选的修饰词
 └── 必需的核心关键词（小写字母开头）
```

### 3.2 字符集限制

**允许的字符**:
- ✅ 小写字母: `a-z`
- ✅ 数字: `0-9`
- ✅ 连字符: `-` (作为单词分隔符)

**禁止的字符**:
- ❌ 大写字母: `A-Z`
- ❌ 下划线: `_`
- ❌ 空格: ` `
- ❌ 特殊字符: `!@#$%^&*()+=[]{}|;:'",.<>?/~\``
- ❌ 中文/日文/韩文等非 ASCII 字符
- ❌ 连续连字符: `--`

### 3.3 单词分隔符

**统一使用连字符 `-`**，不使用其他形式：

```bash
✅ 正确:
getting-started.md
api-reference-guide.md
installation-and-setup.md

❌ 错误:
getting_started.md        # 下划线（Python 风格）
GettingStarted.md         # 驼峰命名
getting.starting.md       # 点号
GETTING-STARTED.md        # 全大写
```

**原因**:
- 连字符是 URL 的标准单词分隔符
- 更易读（比下划线更清晰）
- 避免 URL 编码问题（下划线在某些场景需要编码）

## 4. 命名模式库

### 4.1 动作导向型

适用于教程、指南类章节：

| 模式 | 示例 | 适用场景 |
|------|------|---------|
| `{verb}-ing-{noun}` | `getting-started`, `setting-up` | 入门、配置 |
| `{verb}-ing-{adjective}` | `building-production` | 实战、进阶 |
| `{verb}-ing-from-{noun}` | `migrating-from-v1` | 迁移指南 |

**常用动词列表**:
- getting, setting, building, creating, deploying, configuring
- installing, integrating, optimizing, debugging, testing

### 4.2 概念解释型

适用于原理、概念类章节：

| 模式 | 示例 | 适用场景 |
|------|------|---------|
| `{noun}` | `introduction`, `overview` | 简介、概览 |
| `{adjective}-{noun}` | `core-concepts`, `advanced-patterns` | 概念讲解 |
| `{noun}-{noun}` | `architecture-design`, `data-model` | 架构、设计 |

**常用名词列表**:
- concepts, principles, patterns, architecture, design
- fundamentals, basics, essentials, overview, introduction

### 4.3 参考文档型

适用于 API、配置参考：

| 模式 | 示例 | 适用场景 |
|------|------|---------|
| `{noun}-reference` | `api-reference`, `config-reference` | API 文档 |
| `{noun}-guide` | `installation-guide`, `usage-guide` | 操作指南 |
| `{noun}-examples` | `code-examples`, `use-cases` | 示例集合 |

### 4.4 问题解决型

适用于 FAQ、故障排查：

| 模式 | 示例 |适用场景 |
|------|------|---------|
| `{noun}` | `faq`, `troubleshooting` | 常见问题 |
| `{verb}-ing-{common-issue}` | `fixing-common-errors` | 问题修复 |
| `{noun}-{solution}` | `performance-tuning` | 优化方案 |

## 5. 最佳实践示例

### 5.1 技术教程常见场景

#### 场景 1: RAG 教程

```bash
# 推荐的章节命名
introduction.md              # 教程简介
getting-started.md           # 快速开始
core-concepts.md             # 核心概念（向量检索、LLM 等）
installation-guide.md        # 安装指南
building-basic-rag.md        # 构建 RAG 应用
advanced-retrieval.md        # 高级检索策略
optimizing-performance.md    # 性能优化
production-deployment.md     # 生产部署
api-reference.md             # API 参考
troubleshooting.md           # 故障排查
faq.md                       # 常见问题
```

#### 场景 2: React 入门

```bash
introduction.md              # React 是什么
getting-started.md           # 环境搭建
jsx-fundamentals.md          # JSX 基础
components-basics.md         # 组件入门
hooks-introduction.md        # Hooks 介绍
state-management.md          # 状态管理
routing-with-react-router.md # 路由配置
testing-react-apps.md        # 测试策略
building-real-project.md     # 实战项目
deployment-guide.md          # 部署上线
```

### 5.2 从中文标题生成 slug 的算法

#### 步骤 1: 提取关键词

```
输入: "快速开始搭建 RAG 应用"
输出关键词: [快速, 开始, 搭建, RAG, 应用]
```

#### 步骤 2: 翻译为英文

```
快速 → getting / quick
开始 → start / begin
搭建 → build / setup
RAG → rag (保留专有名词)
应用 → app / application
```

#### 步骤 3: 组合并规范化

```
候选方案:
1. getting-started-building-rag-app      # 太长
2. getting-started-rag                   # ✅ 推荐
3. quick-start-rag                       # 也可以
4. setup-rag-application                 # 不够直观
```

#### 步骤 4: 长度检查

```javascript
function validateSlug(slug) {
  if (slug.length < 5) {
    return { valid: false, reason: '太短，可能不够具体' };
  }
  
  if (slug.length > 40) {
    return { valid: false, reason: '太长，建议精简' };
  }
  
  if (!/^[a-z0-9][a-z0-9-]*[a-z0-9]$/.test(slug)) {
    return { valid: false, reason: '格式不符合规范' };
  }
  
  return { valid: true };
}
```

**推荐长度**: 10-30 个字符

## 6. 特殊情况处理

### 6.1 包含数字的情况

```bash
# 版本号
migrating-to-v2.md            # ✅ 小写 v + 数字
react18-new-features.md       # ✅ 数字与字母直接连接
python3-vs-python2.md         # ✅ 对比场景

# 序号（避免使用，除非必要）
chapter-1-introduction.md     # ⚠️ 不推荐，用 sidebar 配置代替
step-1-installation.md        # ⚠️ 仅在步骤指南中使用
```

### 6.2 包含缩略词的情况

```bash
# 通用缩略词（小写）
rag-tutorial.md               # RAG → rag
api-reference.md              # API → api
faq.md                        # FAQ → faq
url-routing.md                # URL → url
ui-components.md              # UI → ui

# 专有名词（保持原样)
docker-integration.md         # Docker → docker
kubernetes-deployment.md      # Kubernetes → kubernetes (或 k8s)
postgresql-optimization.md    # PostgreSQL → postgresql
```

**原则**: 
- 广为人知的缩略词 → 全小写
- 专有名词 → 全小写（除非品牌要求大写）

### 6.3 避免歧义的命名

```bash
# 有歧义
base.md                       # ❌ 太模糊
setup.md                      # ❌ 可能指代多种设置
utils.md                      # ❌ 范围不清

# 更明确
project-structure.md          # ✅ 明确是项目结构
environment-setup.md          # ✅ 明确是环境配置
utility-functions.md          # ✅ 明确是工具函数
```

## 7. 目录结构中的命名一致性

### 7.1 章节文件 vs 资源文件

```
packages/content/src/
├── chapters/
│   ├── getting-started.md           # 章节文件
│   └── api-reference.md
│
└── assets/                          # （如果需要在 content 包中存放资源）
    ├── images/
    │   ├── getting-started-         # 与章节同名的前缀
    │   │   ├── diagram.png
    │   │   └── screenshot.png
    │   └── api-reference-
    │       ├── flowchart.svg
    │       └── example.png
    └── code-samples/
        ├── getting-started-demo.py
        └── api-example.js
```

**关联规则**: 资源文件名以所属章节 slug 为前缀

### 7.2 多语言版本的命名

```
chapters/
├── en/                            # 英文版本
│   ├── introduction.md
│   └── getting-started.md
├── zh/                            # 中文版本
│   ├── introduction.md            # 相同的 slug
│   └── getting-started.md
└── ja/                            # 日文版本（未来）
    ├── introduction.md
    └── getting-started.md
```

**关键**: 不同语言的同一章节使用 **相同的 slug**

## 8. 自动化工具

### 8.1 命名验证脚本

```javascript
// scripts/validate-filename.mjs
const NAMING_REGEX = /^[a-z0-9]([a-z0-9-]*[a-z0-9])?\.md$/;

function validateFilename(filename) {
  if (!NAMING_REGEX.test(filename)) {
    throw new Error(`Invalid filename: ${filename}`);
  }
  
  if (filename.length > 40) {
    console.warn(`Warning: Filename too long (${filename.length} chars): ${filename}`);
  }
  
  if (filename.includes('--')) {
    throw new Error(`Consecutive hyphens in: ${filename}`);
  }
  
  return true;
}
```

### 8.2 Git Hook 集成

在 `.pre-commit-config.yaml` 中添加:

```yaml
repos:
  - repo: local
    hooks:
      - id: check-filename-convention
        name: Check filename convention
        entry: node scripts/validate-filename.mjs
        language: node
        files: '^packages/content/src/chapters/.*\.md$'
```

## 9. 常见错误案例

### 错误案例 1: 使用中文

```bash
❌ 第一章-快速开始.md
✅ getting-started.md
```

**修正方法**: 提取核心含义，翻译为英文 slug

### 错误案例 2: 使用驼峰

```bash
❌ GettingStarted.md
✅ getting-started.md
```

**原因**: 
- macOS 文件系统默认不区分大小写（`GettingStarted.md` == `gettingstarted.md`）
- Linux 区分大小写，导致跨平台不一致
- URL 中大小写混合影响可读性和 SEO

### 错误案例 3: 过度缩写

```bash
❌ gs.md (getting-started)
❌ inst.md (installation)
✅ getting-started.md
✅ installation-guide.md
```

**原则**: 宁可稍长，不要牺牲可读性

### 错误案例 4: 无意义的名称

```bash
❌ chapter1.md
❌ part-one.md
❌ temp.md
❌ new-chapter.md
✅ introduction.md
✅ getting-started.md
✅ core-concepts.md
```

## 10. 检查清单

创建新章节时，请确认：

- [ ] 文件名全小写
- [ ] 只包含 `[a-z0-9-]` 字符
- [ ] 使用连字符 `-` 分隔单词
- [ ] 不以下划线开头或结尾
- [ ] 没有连续连字符 `--`
- [ ] 长度在 10-30 个字符之间
- [ ] 见名知意（能表达章节主题）
- [ ] 与现有文件命名风格一致
- [ ] Frontmatter 中的 `title` 字段包含中文标题

---

**相关文档**:
- [SKILL.md 主文档](../SKILL.md) — 内容管理总览
- [frontmatter-schema.md](./frontmatter-schema.md) — Schema 定义参考
