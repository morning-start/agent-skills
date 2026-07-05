# Scrapling 技能文档目录

本文档列出 Scrapling 技能包的所有文档。

---

## 主技能文件

| 文件 | 说明 |
|------|------|
| [SKILL.md](./SKILL.md) | 主技能文件，包含完整使用指南 |

---

## 技能列表

Scrapling 是一个自适应网页抓取框架，可处理从单个请求到完整爬取的所有任务。其解析器能够学习网站变化，在页面更新时自动重新定位元素。其获取器开箱即用可绕过反机器人系统（如 Cloudflare Turnstile）。其蜘蛛框架可扩展到并发、多会话爬取，支持暂停/恢复和自动代理轮换。

| 技能 | 版本 | 说明 |
|------|------|------|
| [scrapling-core](./scrapling-core/) | 1.0.0 | 核心解析引擎：CSS/XPath 选择器、智能元素追踪、自适应解析 |
| [scrapling-fetchers](./scrapling-fetchers/) | 1.0.0 | 获取器：Fetcher、StealthyFetcher、DynamicFetcher |
| [scrapling-spiders](./scrapling-spiders/) | 1.0.0 | 爬虫框架：并发控制、暂停/恢复、流式输出 |
| [scrapling-adaptive](./scrapling-adaptive/) | 1.0.0 | 自适应解析：SmartElement、相似元素查找、缓存管理 |
| [scrapling-session](./scrapling-session/) | 1.0.0 | 会话管理：Cookie 持久化、代理轮换、域阻断 |

---

## 参考文档

references/ 目录下包含完整参考文档：

### 核心解析

| 文件 | 说明 |
|------|------|
| [basic-usage.md](./scrapling-core/references/basic-usage.md) | 基础使用指南 |
| [installation.md](./scrapling-core/references/installation.md) | 安装配置 |

### 获取器

| 文件 | 说明 |
|------|------|
| [fetcher.md](./scrapling-fetchers/references/fetcher.md) | Fetcher 基础获取器 |
| [stealthy-fetcher.md](./scrapling-fetchers/references/stealthy-fetcher.md) | StealthyFetcher 反检测获取器 |
| [dynamic-fetcher.md](./scrapling-fetchers/references/dynamic-fetcher.md) | DynamicFetcher 动态网站获取器 |

### 爬虫框架

| 文件 | 说明 |
|------|------|
| [spider-basics.md](./scrapling-spiders/references/spider-basics.md) | Spider 基础 |
| [concurrency.md](./scrapling-spiders/references/concurrency.md) | 并发控制 |
| [streaming.md](./scrapling-spiders/references/streaming.md) | 流式输出 |

### 自适应解析

| 文件 | 说明 |
|------|------|
| [adaptive-parsing.md](./scrapling-adaptive/references/adaptive-parsing.md) | 自适应解析 |
| [element-tracking.md](./scrapling-adaptive/references/element-tracking.md) | 智能元素追踪 |
| [similar-elements.md](./scrapling-adaptive/references/similar-elements.md) | 相似元素查找 |

### 会话管理

| 文件 | 说明 |
|------|------|
| [session-management.md](./scrapling-session/references/session-management.md) | 会话管理 |
| [proxy-rotation.md](./scrapling-session/references/proxy-rotation.md) | 代理轮换 |
| [domain-blocking.md](./scrapling-session/references/domain-blocking.md) | 域阻断 |

---

## 功能覆盖

| 官方文档章节 | 本技能文档 |
|------------|-----------|
| 核心解析器 - 概述 | scrapling-core/SKILL.md |
| 核心解析器 - 选择器 | scrapling-core/SKILL.md |
| 核心解析器 - 元素操作 | scrapling-core/SKILL.md |
| 核心解析器 - DOM 导航 | scrapling-core/SKILL.md |
| 核心解析器 - 文本处理 | scrapling-core/SKILL.md |
| 获取器 - Fetcher | scrapling-fetchers/SKILL.md |
| 获取器 - StealthyFetcher | scrapling-fetchers/SKILL.md |
| 获取器 - DynamicFetcher | scrapling-fetchers/SKILL.md |
| 获取器 - 会话管理 | scrapling-fetchers/SKILL.md |
| Spider 框架 - 基础 | scrapling-spiders/SKILL.md |
| Spider 框架 - 并发控制 | scrapling-spiders/SKILL.md |
| Spider 框架 - 暂停/恢复 | scrapling-spiders/SKILL.md |
| Spider 框架 - 流式输出 | scrapling-spiders/SKILL.md |
| 自适应解析 - 概述 | scrapling-adaptive/SKILL.md |
| 自适应解析 - SmartElement | scrapling-adaptive/SKILL.md |
| 自适应解析 - 相似元素 | scrapling-adaptive/SKILL.md |
| 自适应解析 - 缓存管理 | scrapling-adaptive/SKILL.md |
| 会话管理 - Cookie | scrapling-session/SKILL.md |
| 会话管理 - 代理轮换 | scrapling-session/SKILL.md |
| 会话管理 - 域阻断 | scrapling-session/SKILL.md |

---

## 快速导航

### 新手入门
1. 阅读 [scrapling-core/SKILL.md](./scrapling-core/SKILL.md) 快速开始
2. 了解 [scrapling-fetchers](./scrapling-fetchers/) 获取器
3. 学习 [scrapling-spiders](./scrapling-spiders/) 爬虫框架

### 进阶使用
1. [scrapling-adaptive](./scrapling-adaptive/) - 自适应解析，处理网站变化
2. [scrapling-session](./scrapling-session/) - 会话管理，代理轮换
3. [references/](./references/) - 完整 API 参考

### 完整 API
1. [scrapling-core](./scrapling-core/) - 核心解析引擎
2. [scrapling-fetchers](./scrapling-fetchers/) - HTTP 获取器
3. [scrapling-spiders](./scrapling-spiders/) - 爬虫框架
4. [scrapling-adaptive](./scrapling-adaptive/) - 自适应解析
5. [scrapling-session](./scrapling-session/) - 会话管理

---

## 安装说明

```bash
# 安装 Scrapling 核心
pip install scrapling

# 安装获取器依赖（推荐）
pip install "scrapling[fetchers]"

# 下载浏览器依赖（DynamicFetcher 需要）
scrapling install
```

---

## 更新日志

- 2026-03-16: 初始版本
  - 添加 scrapling-core v1.0.0：核心解析引擎
  - 添加 scrapling-fetchers v1.0.0：获取器
  - 添加 scrapling-spiders v1.0.0：爬虫框架
  - 添加 scrapling-adaptive v1.0.0：自适应解析
  - 添加 scrapling-session v1.0.0：会话管理
