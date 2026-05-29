# DrissionPage 技能文档目录

本文档列出 DrissionPage 技能包的所有文档。

---

## 主技能文件

| 文件 | 说明 |
|------|------|
| [SKILL.md](./SKILL.md) | 主技能文件，包含完整使用指南 |

---

## 脚本文件

scripts/ 目录下包含实用脚本：

| 文件 | 说明 |
|------|------|
| [quick_demo.py](./scripts/quick_demo.py) | 快速演示脚本 |
| [baidu_search.py](./scripts/baidu_search.py) | 百度搜索示例 |
| [data_collector.py](./scripts/data_collector.py) | 数据采集脚本 |
| [login_automation.py](./scripts/login_automation.py) | 登录自动化脚本 |
| [batch_crawler.py](./scripts/batch_crawler.py) | 批量爬取脚本 |
| [network_listener.py](./scripts/network_listener.py) | 网络监听脚本 |
| [action_chains.py](./scripts/action_chains.py) | 动作链脚本 |
| [batch_create.py](./scripts/batch_create.py) | 批量创建脚本 |

---

## 参考文档

references/ 目录下包含完整 API 参考：

### 核心类

| 文件 | 说明 |
|------|------|
| [api_reference.md](./references/api_reference.md) | 核心类完整 API 参考 |
| [browser_object.md](./references/browser_object.md) | 浏览器对象 API |
| [browser_options.md](./references/browser_options.md) | 浏览器启动配置 |

### 元素操作

| 文件 | 说明 |
|------|------|
| [locator_syntax.md](./references/locator_syntax.md) | 元素定位语法 |
| [element_info.md](./references/element_info.md) | 元素信息获取 |
| [actions.md](./references/actions.md) | 动作链 |

### 等待和监听

| 文件 | 说明 |
|------|------|
| [waiting.md](./references/waiting.md) | 等待机制 |
| [network_listener.md](./references/network_listener.md) | 网络监听（见 SKILL.md） |

### SessionPage

| 文件 | 说明 |
|------|------|
| [session_page.md](./references/session_page.md) | SessionPage 无浏览器模式 |

### 高级功能

| 文件 | 说明 |
|------|------|
| [download.md](./references/download.md) | 下载功能 |
| [screenshot.md](./references/screenshot.md) | 截图和录像 |
| [console.md](./references/console.md) | 控制台信息 |

### 配置和错误

| 文件 | 说明 |
|------|------|
| [settings.md](./references/settings.md) | 全局设置 |
| [errors.md](./references/errors.md) | 异常类 |

---

## 功能覆盖

| 官方文档章节 | 本技能文档 |
|------------|-----------|
| 浏览器控制 - 概述 | SKILL.md |
| 浏览器控制 - 连接浏览器 | SKILL.md + browser_options.md |
| 浏览器控制 - 浏览器启动设置 | browser_options.md |
| 浏览器控制 - 浏览器对象 | browser_object.md |
| 浏览器控制 - 标签页管理 | SKILL.md |
| 浏览器控制 - 访问网页 | SKILL.md |
| 浏览器控制 - 页面交互 | SKILL.md |
| 浏览器控制 - 获取网页信息 | SKILL.md |
| 浏览器控制 - 查找元素 | locator_syntax.md |
| 浏览器控制 - 元素交互 | SKILL.md |
| 浏览器控制 - 获取元素信息 | element_info.md |
| 浏览器控制 - iframe 操作 | SKILL.md |
| 浏览器控制 - 动作链 | actions.md |
| 浏览器控制 - 模式切换 | SKILL.md |
| 浏览器控制 - 等待 | waiting.md |
| 浏览器控制 - 监听网络数据 | SKILL.md |
| 浏览器控制 - 获取控制台信息 | console.md |
| 浏览器控制 - 截图和录像 | screenshot.md |
| 浏览器控制 - 上传文件 | SKILL.md |
| SessionPage | session_page.md |
| 进阶使用 - 加速 | SKILL.md |
| 进阶使用 - 命令行 | SKILL.md |
| 进阶使用 - 对接 | SKILL.md |
| 进阶使用 - 错误处理 | errors.md |
| 进阶使用 - ini 配置 | SKILL.md |
| 进阶使用 - 封装 | SKILL.md |
| 进阶使用 - 设置 | settings.md |
| 进阶使用 - 工具 | SKILL.md |
| 下载 | download.md |

---

## 快速导航

### 新手入门
1. 阅读 [SKILL.md](./SKILL.md) 快速开始
2. 运行 [quick_demo.py](./scripts/quick_demo.py) 验证环境
3. 参考 [baidu_search.py](./scripts/baidu_search.py) 编写第一个脚本

### 进阶使用
1. [locator_syntax.md](./references/locator_syntax.md) - 元素定位
2. [actions.md](./references/actions.md) - 动作链
3. [waiting.md](./references/waiting.md) - 等待机制

### 完整 API
1. [api_reference.md](./references/api_reference.md) - 核心 API
2. [browser_options.md](./references/browser_options.md) - 浏览器配置
3. [element_info.md](./references/element_info.md) - 元素信息

---

## 更新日志

- 2024-xx-xx: 初始版本，包含完整文档覆盖
