---
name: sales-readme
description: |
  推销员式 README 写作。当你需要写新的 README、改写/优化现有 README、或把技术文档风格的项目介绍转为产品页面风格时，请使用本 skill。
  触发场景包括：用户说"帮我写个 README"、"优化一下 README"、"把我的项目介绍写得更有吸引力"、"重写 README"、"给 README 加点营销感"、"让 README 更像 landing page"、"写 GitHub 项目介绍"。
  即使对方只说了"写个项目说明"或"整理一下项目文档"，如果这是一个需要推广的开源项目，也值得使用本 skill。
  注意：本 skill 专攻 README 文案和布局，不负责技术文档的 API 参考编写（那是 doc-writer 的领域）。
---

# 推销员式 README 写作

## 核心心法

你的读者会在 **30 秒内** 决定是否继续读下去。在这 30 秒里，他们要找到三个问题的答案：

| 优先级 | 问题 | 对应内容 |
|--------|------|----------|
| 1 | 这东西能帮我干什么？ | 功能 + 场景 |
| 2 | 它凭什么比别的好？ | 定位 + 差异化 |
| 3 | 我怎么开始用？ | 快速上手 + 一行命令 |

**黄金法则：** 如果一个信息不回答上面三个问题之一，删掉它或移到独立文档里。

---

## 门禁（Guardrails）：动手前必须完成三步

### 门禁一：项目理解检查

写之前必须搞清楚：

1. **这个项目解决谁的什么问题？** —— 目标用户是谁，核心痛点是什么
2. **和竞品的核心差异是什么？** —— 为什么用户不选别家选你
3. **项目的健康度数据** —— 有没有 GitHub Stars、下载量、CI 状态、版本号、许可证？
4. **项目的技术栈** —— 用什么语言、框架、包管理器？

> 如果用户给的信息不够，你必须主动提问，不要自己编造。

### 门禁二：证据链检查

README 里每一句价值主张，都必须有真实代码/功能支撑：

- "支持实时协作" → 必须有对应代码示例
- "开箱即用" → 必须有对应安装/初始化命令
- "性能优异" → 必须有基准测试数据或用户报告
- "被大型项目使用" → 必须有真实的用户列表或引用

**禁用语（除非有充分证据）：** "blazing fast"、"industry-leading"、"best-in-class"、"most popular"

### 门禁三：输出前自查

写完 README 后检查：
- [ ] 前 3 段用完了吗？如果还没有出现"这东西具体能做什么"，重写标题区
- [ ] 每一句价值主张都有证据吗？
- [ ] 有没有用技术术语代替功能描述？（"支持 GraphQL" → "用一套查询搞定前后端数据"）
- [ ] 有没有教人原理而不是在卖产品？（删掉）
- [ ] 快速开始是不是最短路径？是不是 copy-paste 就能跑？
- [ ] 有没有包含编造的内容？（必须 100% 真实）

---

## 工作流（Writing Workflow）

### 第 1 步：收集信息

用门禁一的四个问题向用户提问，同时收集：
- 项目名称、Logo（如果有）
- 一行描述（tagline）
- 3-5 个核心功能点
- 安装方式（npm/pip/go install/cargo install 等）
- 一段最典型的使用代码
- 竞品名称，如果有
- GitHub 地址、文档地址、社区链接
- 许可证

### 第 2 步：确定场景类别

识别项目类型，选择对应的模板结构（见"场景化模板"章节）。

### 第 3 步：起草

按照"场景化模板"章节的结构逐段撰写。每一段写完问自己：这是一个功能描述还是一个推销员话术？

### 第 4 步：视觉增强

在必要位置插入：
- 徽章行（版本、构建状态、许可证、下载量）
- HTML 居中对齐布局
- 暗色/亮色模式 logo
- Star History 图（GitHub 项目）
- 演示截图或 GIF

### 第 5 步：门禁自查

跑门禁三的输出前自查清单。

---

## 场景化模板

根据项目类型选择最合适的 README 结构。

### 场景 A：开源库 / CLI 工具（如 Zustand、tRPC）

**特点：** 开发者对开发者，需要快速展示 API、安装方式和最小示例。

```
# [项目名]

<!-- 标题区：Logo + 徽章行 -->
<!-- 用 HTML 实现暗色/亮色模式支持 -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="logo-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="logo-light.png">
  <img alt="logo" src="logo-light.png" height="60">
</picture>

<p align="center">
  <a href="..."><img src="...version.svg" alt="npm version"></a>
  <a href="..."><img src="...build.svg" alt="build status"></a>
  <a href="..."><img src="...license.svg" alt="license"></a>
  <a href="..."><img src="...downloads.svg" alt="downloads"></a>
  <a href="..."><img src="...discord.svg" alt="discord"></a>
</p>

<!-- 钩子 —— 一句话说清帮谁解决什么问题 -->
> [一行描述] —— [一个具体场景下能做什么]

## 功能亮点（每个点 = 做了什么 + 用在什么场景 + 对用户的好处）

- **⚡️ [功能名]** —— [场景描述]。一两句话说清楚。
- **🔌 [功能名]** —— ...
- **🛠 [功能名]** —— ...

## 快速开始（一个代码块，copy-paste 就能跑）

```bash
npm install [包名]
# or
pnpm add [包名]
```

```ts
// 最简使用示例 —— 让读者 10 秒理解怎么用
import { create } from '[包名]'
// ...
```

## 为什么选 [项目名] 而不是 [竞品]？

| 场景 | 竞品 | [项目名] |
|------|------|----------|
| [具体场景 1] | [竞品的问题] | [你的优势] |
| [具体场景 2] | [竞品的问题] | [你的优势] |

## 进阶用法

<!-- 技术内容：这里可以放详细的 API、中间件、配置说明 -->
<!-- 保持技术准确性，不编造不存在的功能 -->

### [功能 A]

```ts
// 代码示例
```

### [功能 B]

...

## 社区

- 📖 [文档](链接)
- 💬 [Discord](链接)
- 🐦 [Twitter](链接)
- ⭐ [Star History](https://star-history.com/#user/repo)

---

## 许可证

[许可证类型] — 查看 [LICENSE](链接)
```

**真实案例参考：** Zustand（极简、功能展示清晰、对比直接）、tRPC（Star History 图、社区链接、赞助商）

---

### 场景 B：SaaS / 企业级产品（如 Prisma）

**特点：** 需要建立信任感、展示生态、体现专业度。

```
<div align="center">
  <img src="logo.png" alt="logo" width="200" />
  <h1>[项目名]</h1>
  <p align="center">
    <a href="链接">Quickstart</a>
    <span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
    <a href="链接">Website</a>
    <span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
    <a href="链接">Docs</a>
    <span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
    <a href="链接">Examples</a>
    <span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
    <a href="链接">Blog</a>
  </p>
  <hr />
</div>

## [项目名] 是什么？

[一句话定义] —— 由以下几个部分组成：

- **[组件 A]**：[一句话+链接]
- **[组件 B]**：[一句话+链接]
- **[组件 C]**：[一句话+链接]

## 快速开始（5 分钟）

### 前置条件

- [依赖 1]（附版本要求）
- [依赖 2]

### 安装

```bash
[npm/pip/... 安装命令]
```

### 配置

```ts
// 配置示例 ————必须确保能实际运行
```

### 第一个查询

```ts
// 能让读者立刻产生"我做出来了"感觉的最小示例
```

## 核心概念

<!-- 技术内容：需要解释核心架构但只说必要部分 -->

### [概念 1]

[解释 + 代码]

### [概念 2]

[解释 + 代码]

## 谁在用？

> 列出真实用户（如果有）、GitHub Stars、下载量。**不能编造。**

## 社区 & 支持

- [Discord](链接)
- [Bug 报告](链接)
- [Feature 请求](链接)

## 许可证

[类型]
```

**真实案例参考：** Prisma（导航行、结构化核心概念、清晰的分层）

---

### 场景 C：前端组件库 / UI 工具（如 Vite）

**特点：** 视觉优先，演示动画/截图在第一屏，徽章展示生态健康度。

```
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="...">
    <source media="(prefers-color-scheme: light)" srcset="...">
    <img alt="logo" src="..." height="60">
  </picture>
</p>

<p align="center">
  <a href="..."><img src="..." alt="npm version"></a>
  <a href="..."><img src="..." alt="build status"></a>
  <a href="..."><img src="..." alt="license"></a>
</p>

> [一句朗朗上口的 tagline]

- 💡 [功能 1：一句话]
- ⚡️ [功能 2：一句话]
- 🛠 [功能 3：一句话]
- 📦 [功能 4：一句话]
- 🔩 [功能 5：一句话]
- 🔑 [功能 6：一句话]

<!-- 放一张演示截图或动画 GIF -->

## 快速开始

```bash
npm create [模板名]@latest
```

[如果你用 Vite 这样的工具，加上模板信息]

## 对比

| 特性 | [项目名] | [竞品 A] | [竞品 B] |
|------|---------|---------|---------|
| [维度 1] | ✅ | ❌ | ⚠️ |
| [维度 2] | ✅ | ✅ | ❌ |

## 参与贡献

[贡献指南链接]

## 赞助商

<p align="center">
  <img src="..." alt="sponsors" />
</p>

## 许可证

[MIT]
```

**真实案例参考：** Vite（简短功能列表 + 徽章）、Shadcn/ui（视频演示 + CLI）

---

### 场景 D：轻量工具库 / 单一功能库

**特点：** README 要非常短，100-200 行足矣。聚焦在安装 + 一行代码示例 + API 签名。

```
# [项目名]

> [一行描述]

[3 个徽章：版本、大小、许可证]

```bash
npm install [包名]
```

```js
import { [函数名] } from '[包名]'

// 一个示例展示核心用法
```

## API

### `[函数签名]`

[参数说明、返回值]

## License

MIT
```

---

## 视觉资产模式（从顶级开源项目提取）

### 1. 徽章行（Badge Row）

从 shields.io 生成，放在标题下方。建议包含：

| 徽章 | 示例 URL | 必要程度 |
|------|---------|---------|
| npm/pypi 版本 | `https://img.shields.io/npm/v/包名` | ✅ 推荐 |
| 构建状态 | GitHub Actions 链接 | ✅ 推荐 |
| 许可证 | `https://img.shields.io/badge/license-MIT-blue` | ✅ 推荐 |
| 月下载量 | `https://img.shields.io/npm/dm/包名` | 可选 |
| Discord/社区 | `https://img.shields.io/discord/频道ID` | 可选 |

**注意：** 只有真正存在的链接才放。没有 Discord 服务器就不要用 Discord badge。

### 2. HTML 布局技巧

在 GitHub README 中可以直接使用 HTML 标签。GitHub 支持以下常用标签：

- `<p align="center">` —— 居中段落
- `<div align="center">` —— 居中容器
- `<picture>` + `<source media="(prefers-color-scheme: ...)">` —— 暗色/亮色模式适配
- `<img>` —— 图片、Logo、徽章
- `<h1>` ~ `<h6>` —— 标题（与 Markdown 等价）
- `<table>` / `<tr>` / `<td>` —— 表格布局（用于核心团队照片墙、Sponsors）
- `<br>` —— 换行
- `<hr>` —— 分隔线
- `<details>` / `<summary>` —— 折叠区块
- `<kbd>` —— 快捷键标记

### 3. Star History 图

对 GitHub 项目非常有说服力，放在 Feature 或 Community 区：

```markdown
[![Star History](https://api.star-history.com/svg?repos=user/repo&type=Date)](https://star-history.com/#user/repo)
```

### 4. logos 的暗色/亮色模式

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="logo-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="logo-light.png">
  <img alt="logo" src="logo-light.png" height="60">
</picture>
```

### 5. 导航链接行

```markdown
<p align="center">
  <a href="链接">Quickstart</a>
  <span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
  <a href="链接">Docs</a>
  <span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
  <a href="链接">Examples</a>
  <span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
  <a href="链接">Community</a>
</p>
```

---

## 反编造规则

> **这是红线。不能越界。**

### ❌ 绝对不能做的事

1. **不能编造 GitHub Stars、下载量、用户数、月活跃用户** —— 除非用户明确提供
2. **不能编造用户案例 / 推荐语 / 客户证言** —— 除非用户明确提供真实案例
3. **不能编造竞品对比数据** —— 除非用户提供真实来源
4. **不能编造不存在的功能** —— 每个功能必须有真实代码支撑
5. **不能编造性能数据** —— 除非用户提供基准测试结果
6. **不能编造版本号** —— 使用真实的 npm/pypi/crates 版本

### ✅ 可以做的事

1. **假设场景** —— "如果你在做 SaaS 产品，需要实时协作……" 这类场景化描述，只要明确标注为假设场景就可以
2. **通用行业常识** —— "Vim 用户可能需要学习模式切换"这类常识性描述
3. **项目本身的真实信息** —— 用户告诉你的功能、定位、技术栈
4. **引用已知的竞品名称和官网** —— 竞品是公开信息

### 怀疑时的处理原则

如果不确定某个信息的真实性，执行以下操作：
1. 在 README 里加上 `[TODO: 确认 XXX]` 标记
2. 向用户提问："关于 XXX，你能提供具体数据吗？"
3. 在用户确认之前绝不发布

---

## 推销员自查清单

最终输出前逐项检查：

- [ ] 第一部分说没说出"这东西能帮我解决什么问题"？
- [ ] 有没有用技术术语代替功能描述？
- [ ] 有没有教人原理而不是在卖产品？
- [ ] 快速开始是不是最短 copy-paste 路径？
- [ ] 读者看完前三段能说出"这是做什么的"吗？
- [ ] 每一个 claim 都有证据支撑吗？
- [ ] 前 30 秒内回答了"这是什么、为什么选它、怎么开始用"三个问题吗？
- [ ] 有没有编造任何内容？
- [ ] 徽章和链接都是真实可用的吗？
- [ ] 代码示例编译/运行无误吗？

---

## 写作风格指南

- **优先用"你"而不是"用户"** —— "你的 API 密钥"而不是"用户的 API 密钥"
- **每句话回答"所以呢"** —— 功能是子弹，场景是靶子，方案是枪
- **用短句、短段、短句** —— 每段不超过 3 行
- **代码示例永远可运行** —— 不要用伪代码
- **解释 why 而不是 what** —— 说明为什么这样设计，而不是只描述做了什么
- **对比不要贬低竞品** —— 客观说差异即可
