# Monorepo 快速参考 (Tutorial Writer 特有)

> **定位**: Tutorial Writer 架构专用的补充指南
> **非目标**: 不重复 Turborepo/Astro 官方文档
> **适用版本**: v1.0.0 (Plan D: Official Tools)
> **最后更新**: 2026-05-31

---

## 目录

- [1. Tutorial Writer 三包架构](#1-tutorial-writer-三包架构)
- [2. Workspace 依赖规则](#2-workspace-依赖规则)
- [3. 日常工作流速查](#3-工作流速查)
- [4. 常见问题 (TW 特有)](#4-常见问题-tw-特有)
- [5. 相关资源链接](#5-相关资源链接)

---

## 1. Tutorial Writer 三包架构

### 1.1 核心设计理念

```
内容是唯一真相源 → 格式是可扩展的表示层 → 部署是最终输出目标
```

| 原则 | 说明 |
|------|------|
| **单一职责** | 每个子技能只回答一个问题 |
| **依赖方向正确** | content ← 被 web/book 依赖，禁止反向 |
| **官方工具优先** | 项目创建使用 create-turbo / turbo gen / create-astro |

### 1.2 包职责定义

| 包 | 位置 | 职责 | 技术栈 | 说明 |
|----|------|------|--------|------|
| **web** | `apps/web/` | 展示层：网站渲染 | Astro + Starlight | 消费 content |
| **content** | `packages/content/` | 数据层：内容 + Schema | Astro Content Collections | 唯一真相源 |
| **book** | `packages/book/` | 格式层：PDF/ePub | Pandoc + XeLaTeX | 消费 content |

### 1.3 推荐的 turbo.json 配置

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "dev": {
      "cache": false,
      "persistent": true
    },
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", "*.pdf"]
    }
  }
}
```

**关键点**:
- `^build` 表示先构建所有上游依赖（即 content）
- outputs 声明缓存命中时可复用的产物

---

## 2. Workspace 依赖规则

### 2.1 正确的依赖声明

```json
// apps/web/package.json
{
  "name": "@repo/web",
  "dependencies": {
    "@repo/content": "workspace:*"
  }
}

// packages/book/package.json
{
  "name": "@repo/book",
  "dependencies": {
    "@repo/content": "workspace:*"
  }
}
```

### 2.2 禁止的反向依赖

| 反向依赖 | 状态 | 原因 |
|---------|------|------|
| ❌ content → tutorial | 禁止 | 数据层不应依赖展示层 |
| ❌ content → book | 禁止 | 数据层不应依赖格式层 |
| ❌ tutorial ↔ book | 禁止 | 两个输出格式应独立 |
| ✅ tutorial → content | 允许 | 展示层数据来源 |
| ✅ book → content | 允许 | 格式层数据来源 |

### 2.3 pnpm-workspace.yaml 示例

标准 Turbo 项目包含 apps/ 和 packages/ 两级目录：

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

这会自动发现 `apps/` 和 `packages/` 下所有含 `package.json` 的目录。

---

## 3. 日常工作流速查

### 3.1 命令速查表

| 操作 | 命令 | 说明 |
|------|------|------|
| **启动开发** | `bun run dev` | 所有包并行启动（调用 turbo）|
| **仅启动 web** | `bun run --filter @repo/web dev` | 单独开发教程网站 |
| **全量构建** | `bun run build` | 先 build content，再并行 web + book |
| **仅构建 PDF** | `bun run --filter @repo/book build:pdf` | 只生成电子书 |
| **添加新包** | `bunx turbo gen workspace --name ... --type package` | 官方命令 |
| **查看包图** | `bunx turbo run devtools` | 浏览器可视化依赖图 |

### 3.2 内容创作流程

1. 在 `packages/content/src/chapters/` 创建 `.md` 文件
2. 按照 [/content](../skills/tutorial-writer-content/SKILL.md) 的 Schema 编写 Frontmatter
3. 运行 `bun run dev` 预览效果
4. 内容变更后 web 和 book 自动热重载

### 3.3 并行构建优势

```
# 传统方式: 串行构建
build content (5s) → build web (30s) → build book (20s) = 55s 总计

# Turborepo 方式: 并行构建
build content (5s) → [build web (30s) || build book (20s)] = 35s 总计
# 节省: 36% (假设双核 CPU)
```

---

## 4. 常见问题 (TW 特有)

### Q1: content 包的章节如何被 web 和 book 共享？

A: 通过 Astro Content Collections。web 应用在 `astro.config.mjs` 中通过 `contentDir` 引用 content 包路径。book 包通过 Pandoc 直接读取 Markdown 文件。两者消费同一数据源但互不影响。

### Q2: 如何只更新一个包而不重建全部？

A: Turborepo 自动检测变更，只重建受影响的包及其下游依赖。例如：
- 只改了 content → 重建 content + web + book
- 只改了 web → 仅重建 web
- 只改了 book → 仅重建 book

### Q3: 添加第四种格式（如 EPUB）？

A:
1. `turbo gen workspace --name @repo/epub --type package`
2. 在新包中实现转换逻辑
3. 更新 turbo.json 的 build 任务（如有需要）
4. （可选）创建对应的子技能

详见根路由器 SKILL.md 的"项目初始化"章节 Step 4 变体。

### Q4: Windows 兼容性？

A: 官方工具 (`create-turbo`, `turbo gen`) 原生支持 Windows。无需 Git Bash 或 WSL。`create-astro` 同样支持 Windows PowerShell。

### Q5: 与旧版 (v6.x) 的主要区别？

A:
- v6.x: 自定义 init 脚本 + 硬编码模板
- v1.0.0 (Plan D): 官方 CLI 工具链 + AI 编排命令序列
- 详见 [.trae/tutorial-writer-rebuild/MIGRATION-v6-to-v1.md](../../../.trae/tutorial-writer-rebuild/MIGRATION-v6-to-v1.md)

---

## 5. 相关资源链接

### 官方文档

| 工具 | 文档地址 | 用途 |
|------|---------|------|
| **Turborepo** | https://turborepo.org/docs | 任务编排、缓存、远程构建 |
| **create-turbo** | https://turborepo.org/docs/getting-started/installation | 快速开始 |
| **turbo gen** | https://turborepo.org/docs/guides/generating-code | 代码生成 |
| **Astro** | https://docs.astro.build | 静态站点框架 |
| **Starlight** | https://starlight.astro.build | 文档主题 |
| **npm workspaces** | https://docs.npmjs.com/cli/v11/using-npm/workspaces | 工作区配置 |

### Skill 内部文档

| 文档 | 路径 | 内容 |
|------|------|------|
| 根路由器 | `SKILL.md` | 8-Sub 路由 + 初始化流程 |
| Content 技能 | `skills/tutorial-writer-content/SKILL.md` | Schema、命名规范 |
| Web 技能 | `skills/tutorial-writer-web/SKILL.md` | Astro + Starlight 配置 |
| Book 技能 | `skills/tutorial-writer-book/SKILL.md` | PDF/ePub 生成 |
| GitHub Pages | `skills/tutorial-writer-github-pages/SKILL.md` | 部署配置 |

---

*本指南仅覆盖 Tutorial Writer 特有的 Monorepo 约定和最佳实践。*
*通用的 Turborepo/Astro/bun 使用请参考上方官方文档。*
