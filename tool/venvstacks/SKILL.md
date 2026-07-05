---
name: venvstacks
description: 掌握venvstacks分层Python虚拟环境栈工具，实现Python应用的独立打包、环境锁定和可重现发布
dependency:
  python:
    - venvstacks>=0.8.0
    - uv>=0.5.0
---

# venvstacks

## 任务目标
- 本 Skill 用于：掌握 venvstacks 分层 Python 虚拟环境打包和发布技术
- 能力包含：三层环境架构定义、依赖锁定、环境构建、本地导出、归档发布
- 触发条件：当用户需要打包 Python ML/AI 应用并独立分发运行时环境时

## 前置准备
- 环境安装：
  ```bash
  pipx install venvstacks
  # 或
  pip install --user venvstacks
  ```
- 依赖要求：uv>=0.5.0

## 操作步骤

### 标准流程

#### 1. 定义环境栈 (venvstacks.toml)
```toml
[[runtimes]]
name = "cpython@3.11"
fully_versioned_name = "cpython@3.11.10"
requirements = [
    "numpy",
]

[[frameworks]]
name = "sklearn"
runtime = "cpython@3.11"
requirements = [
    "scikit-learn",
]

[[applications]]
name = "classification-demo"
launch_module = "launch_modules/sklearn_classification.py"
frameworks = ["sklearn"]
requirements = [
    "scikit-learn",
]
```

#### 2. 锁定层依赖
```bash
venvstacks lock sklearn_demo/venvstacks.toml
```
- 生成 requirements 文件夹
- 使用 pylock.toml 格式存储锁定的依赖
- 生成层锁定元数据文件

#### 3. 构建环境栈
```bash
venvstacks build sklearn_demo/venvstacks.toml
```
- 创建 venv 环境
- 安装指定包
- 注入 sitecustomize.py 实现层链接
- 注入 postinstall.py 环境配置脚本

#### 4. 本地导出（快速测试）
```bash
venvstacks local-export --output-dir demo_export sklearn_demo/venvstacks.toml
```
- 复制环境到指定目录
- 执行 postinstall.py

#### 5. 发布归档
```bash
venvstacks publish --tag-outputs --output-dir demo_artifacts sklearn_demo/venvstacks.toml
```
- 生成可重现二进制归档
- 生成元数据文件

### 可选分支

#### 当需要完整流水线时
```bash
# 一步完成锁定、构建、发布
venvstacks build --publish --tag-outputs --output-dir artifacts stack.toml
```

#### 当需要多平台支持时
```bash
# 锁定（跨平台）
venvstacks lock stack.toml

# 分平台构建
venvstacks build --target linux-x64 stack.toml
venvstacks build --target win32-x64 stack.toml
venvstacks build --target darwin-arm64 stack.toml

# 发布
venvstacks publish --tag-outputs --output-dir artifacts stack.toml
```

## 资源索引

### 必要脚本
无（CLI 工具为主）

### 领域参考
- [references/architecture.md](references/architecture.md)
  - 何时读取：需要理解三层架构时
  - 内容：Runtime、Framework、Application 层详解

- [references/stack-definition.md](references/stack-definition.md)
  - 何时读取：需要编写 venvstacks.toml 时
  - 内容：TOML 配置格式、层定义规范

- [references/cli-commands.md](references/cli-commands.md)
  - 何时读取：需要了解 CLI 用法时
  - 内容：lock、build、publish、local-export 详解

## 注意事项

### 三层架构
- **Runtime**：Python 解释器环境
- **Framework**：共享框架（如 PyTorch、scikit-learn）
- **Application**：独立应用组件

### 依赖锁定
- 使用 uv 进行联合依赖解析
- 跨平台锁定（pylock.toml 格式）
- 仅允许从二进制包安装

### sitecustomize.py
- 实现层间依赖共享
- 允许代码导入下层包的模块

### 可重现构建
- 相同输入产生字节级相同的归档
- 记录完整的输入哈希和输出哈希
