# Scrapling 安装配置

## 环境要求

- Python 3.10 或更高版本

## 基本安装

### 使用 pip 安装

```bash
pip install scrapling
```

这是最小化安装，仅包含解析引擎及其依赖，不包含获取器（fetchers）或命令行工具。

### 使用 uv 安装

```bash
uv pip install scrapling
```

### 使用 bunx 安装（仅用于 CLI）

```bash
bunx scrapling --help
```

## 可选依赖

Scrapling 提供多个可选功能，根据需要安装。

### 获取器（Fetchers）

如果需要使用任何获取器类（`Fetcher`、`StealthyFetcher`、`DynamicFetcher` 等），需要安装：

```bash
pip install "scrapling[fetchers]"
```

安装后还需要下载浏览器依赖：

```bash
scrapling install           # 正常安装
scrapling install --force  # 强制重新安装
```

或者通过代码安装：

```python
from scrapling.cli import install

install([], standalone_mode=False)          # 正常安装
install(["--force"], standalone_mode=False) # 强制重新安装
```

### MCP 服务器

安装 MCP 服务器功能（用于 AI 辅助网页抓取）：

```bash
pip install "scrapling[ai]"
```

### Shell 功能

安装交互式网页抓取 Shell 和提取命令：

```bash
pip install "scrapling[shell]"
```

Shell 功能包括：
- Scrapling 集成的 IPython Shell
- 快捷方式
- 将 curl 请求转换为 Scrapling 请求的工具
- 在浏览器中查看请求结果

### 安装全部功能

```bash
pip install "scrapling[all]"
```

这将安装所有可选依赖。

## Docker 安装

### 从 DockerHub 拉取

```bash
docker pull pyd4vinci/scrapling
```

### 从 GitHub Registry 拉取

```bash
docker pull ghcr.io/d4vinci/scrapling:latest
```

Docker 镜像包含所有 extras 和浏览器，方便快速开始。

## 验证安装

### 验证基本安装

```python
from scrapling import ParselResponse

html = "<html><body><h1>Hello</h1></body></html>"
response = ParselResponse(html)
print(response.css('h1::text').get())  # 输出: Hello
```

### 验证 Fetchers 安装

```python
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher
print("Fetchers 导入成功")
```

### 验证浏览器安装

```bash
scrapling --version
```

## 常见问题

### Q1: 浏览器依赖下载失败

检查网络连接，或使用代理：

```bash
scrapling install --proxy http://your-proxy:port
```

### Q2: 导入错误

确保已正确安装：

```bash
pip install --upgrade scrapling
```

### Q3: 缺少浏览器

首次使用 DynamicFetcher 时会自动下载浏览器，如需手动触发：

```bash
scrapling install
```

### Q4: 内存占用高

使用 Docker 镜像或仅安装核心解析引擎：

```bash
pip install scrapling  # 仅核心解析
```

### Q5: 与其他库冲突

建议使用虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate    # Windows

pip install scrapling[all]
```

## 卸载

```bash
pip uninstall scrapling
```

如需完全清理（包括缓存）：

```bash
rm -rf ~/.scrapling_cache
```

## 版本信息

查看当前版本：

```bash
pip show scrapling
```

或通过 Python：

```python
import scrapling
print(scrapling.__version__)
```
