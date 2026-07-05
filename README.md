# Agent Skills

AI Agent 技能集合 — 为 AI 编程助手设计的专业技能库。

## 分类

### lang/ — 语言与框架（8）
教你掌握特定编程语言或开发框架。

| 技能 | 说明 |
|------|------|
| [flutter](lang/flutter/) | Flutter 开发：Clean Architecture、TDD、BLoC |
| [rust](lang/rust/) | Rust 全栈开发指导 |
| [moonbit](lang/moonbit/) | MoonBit AI 原生编程语言 |
| [svelte](lang/svelte/) | Svelte 5 核心概念、Runes 系统 |
| [tauri](lang/tauri/) | Tauri v2 桌面应用开发 |
| [wxt](lang/wxt/) | WXT 浏览器扩展开发框架 |
| [cocos](lang/cocos/) | Cocos Creator 3.8 游戏引擎开发 |
| [vsce](lang/vsce/) | VSCode 扩展开发完整指南 |

### tool/ — 工具（8）
教你使用特定开发工具或库。

| 技能 | 说明 |
|------|------|
| [git](tool/git/) | Git 版本控制全流程 |
| [agent](tool/agent/) | Hermes Agent 配置系统 |
| [drissonpage](tool/drissonpage/) | DrissionPage 网页自动化 |
| [scrapling](tool/scrapling/) | Scrapling 自适应网页爬取框架 |
| [venvstacks](tool/venvstacks/) | 分层 Python 虚拟环境栈 |
| [plotnine](tool/plotnine/) | Plotnine 数据可视化 |
| [echart](tool/echart/) | Apache ECharts 图表可视化 |
| [dashboard](tool/dashboard/) | Streamlit 数据看板构建 |

### process/ — 流程与方法论（10）
教你系统化的开发流程、架构方法论和编码规范。

| 技能 | 说明 |
|------|------|
| [project-management](process/project-management/) | 全流程项目管理母技能（含 ROADMAP/TODO/OKR 规划子技能） |
| [six-layer-architect](process/six-layer-architect/) | 六层架构全栈生成器 |
| [software-design](process/software-design/) | 软件设计与编码规范（含代码优化 + 设计模式子技能） |
| [python-team](process/python-team/) | Python 四角色团队协同开发 |
| [pythonic-style](process/pythonic-style/) | Python 代码风格与惯用法 |
| [agents-writer](process/agents-writer/) | AGENTS.md 写作专家 |
| [data-analytics](process/data-analytics/) | 数据分析完整技能体系 |
| [tutorial-writer](process/tutorial-writer/) | 教程写作 5-Sub Router |
| [personal-software-dev-exploration](process/personal-software-dev-exploration/) | 个人软件开发探索方法论 |
| [doc-orchestrator](process/doc-orchestrator/) | 文档编排操盘手（全生命周期管理软件开发文档） |

### utility/ — 辅助工具（4）
跨界工具和辅助决策技能。

| 技能 | 说明 |
|------|------|
| [tech-comparison](utility/tech-comparison/) | 技术选型对比助手 |
| [side-hustle-evaluator](utility/side-hustle-evaluator/) | 副业评估决策工具 |
| [recruitment-processor](utility/recruitment-processor/) | 招聘信息处理 |
| [copyright-assist](utility/copyright-assist/) | 软著申请辅助（中国版权保护中心全流程） |

## 快速开始

每个技能目录下有独立的 `SKILL.md`，包含完整的使用说明。

```bash
# 列出所有技能
Get-ChildItem -Recurse -Filter "SKILL.md" -Depth 2 | ForEach-Object { $_.Directory.Name }

# 查看技能分类统计
Get-ChildItem -Directory | ForEach-Object { "$($_.Name): $(@(Get-ChildItem $_.FullName -Directory).Count)" }

## 目录分类规则

新技能加入时，按以下规则归类：

| 目录 | 条件 | 示例 |
|------|------|------|
| `lang/` | 教学内容是某编程语言或完整开发框架 | Flutter, Rust, Svelte, Tauri |
| `tool/` | 教学内容是某具体工具或库 | Git, DrissionPage, ECharts |
| `process/` | 教学内容是开发流程、架构方法或编码规范 | TDD, Clean Architecture, 项目管理 |
| `utility/` | 不属于以上任何类别的通用辅助技能 | 技术选型, 副业评估, 软著申请 |

## 命名规范

- 所有技能目录统一命名为 `{name}`（全小写，连字符分隔）
- 技能文件统一使用 `SKILL.md`
- 仓库根目录不放置任何技能文件，只放元数据文件

## 质量门禁

- [ ] 技能目录在正确的分类下
- [ ] 目录名符合 `{name}` 格式
- [ ] 包含 `SKILL.md` 主文档
- [ ] SKILL.md 包含 name/version/description/tags 元数据
- [ ] 无跨仓重复（旧仓库已废弃）

## 旧仓库

以下旧仓库已废弃，请使用本仓库：

| 旧仓库 | 状态 |
|--------|------|
| morning-start/book-skills | ❌ 废弃 |
| morning-start/coze-skills | ❌ 废弃 |
| morning-start/wiki-skills | ❌ 废弃 |
| morning-start/dev-skills | ❌ 废弃 |
