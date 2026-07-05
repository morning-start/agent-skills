# UV 锁定文件模板

## 文件说明
- **文件名**：`uv.lock`
- **生成方式**：由 UV 自动生成，不可手动编辑
- **作用**：锁定所有依赖的精确版本，确保可复现性
- **版本信息**：包含 Python 版本、平台信息、依赖哈希

## 模板结构

```text
version = 1

[[package]]
name = "package-name"
version = "1.2.3"
source = { registry = "https://pypi.org/simple" }
checksum = "sha256:..."

[package.dependencies]
dependency1 = ">=1.0.0"
dependency2 = "~=2.0.0"

[[package]]
name = "another-package"
version = "4.5.6"
source = { registry = "https://pypi.org/simple" }
checksum = "sha256:..."

[package.extras]
extra-feature = ["extra-dependency1", "extra-dependency2"]

[[package]]
name = "development-package"
version = "0.1.0"
source = { registry = "https://pypi.org/simple" }
checksum = "sha256:..."

[package.dependencies]
dependency3 = ">=3.0.0"

[metadata]
python-version = "3.11"
content-hash = "sha256:..."
lock-version = "2.0"
```

## 使用说明

### 生成锁定文件
```bash
# 初始化项目
uv init

# 添加依赖（自动生成 uv.lock）
uv add requests

# 添加开发依赖
uv add --dev pytest
```

### 更新锁定文件
```bash
# 更新所有依赖
uv lock --upgrade

# 更新特定依赖
uv lock --upgrade-package requests

# 同步环境
uv sync
```

### 使用锁定文件
```bash
# 根据锁定文件创建虚拟环境
uv sync

# 运行脚本
uv run python main.py
```

## 注意事项

- **不要手动编辑**：`uv.lock` 由 UV 自动生成和管理
- **提交到版本控制**：确保团队使用相同版本的依赖
- **定期更新**：保持依赖安全和性能
- **检查哈希**：确保包的完整性和安全性

## 版本兼容性

- **UV 版本**：0.1.0+
- **Python 版本**：3.8+
- **锁定格式**：UV lock version 2.0

## 示例

### 小项目示例
```text
version = 1

[[package]]
name = "requests"
version = "2.31.0"
source = { registry = "https://pypi.org/simple" }
checksum = "sha256:abc123..."

[package.dependencies]
certifi = ">=2023.7.22.0"
charset-normalizer = ">=2,<4"
idna = ">=2.5,<4"
urllib3 = ">=1.21.1,<3"

[[package]]
name = "certifi"
version = "2023.7.22.0"
source = { registry = "https://pypi.org/simple" }
checksum = "sha256:def456..."

[metadata]
python-version = "3.11"
content-hash = "sha256:ghi789..."
lock-version = "2.0"
```

### 大项目示例
```text
version = 1

[[package]]
name = "fastapi"
version = "0.104.1"
source = { registry = "https://pypi.org/simple" }
checksum = "sha256:jkl012..."

[package.dependencies]
pydantic = ">=2.0.0,<3.0.0"
starlette = ">=0.27.0,<0.28.0"
typing-extensions = ">=4.8.0"

[package.extras]
all = ["email-validator", "httpx", "itsdangerous", "jinja2", "orjson", "python-multipart", "pyyaml", "ujson"]

[[package]]
name = "pydantic"
version = "2.5.0"
source = { registry = "https://pypi.org/simple" }
checksum = "sha256:mno345..."

[package.dependencies]
annotated-types = ">=0.4.0"
pydantic-core = ">=2.14.5,<2.15.0"

[[package]]
name = "uvicorn"
version = "0.24.0"
source = { registry = "https://pypi.org/simple" }
checksum = "sha256:pqr678..."

[package.dependencies]
h11 = ">=0.14.0"

[metadata]
python-version = "3.11"
content-hash = "sha256:stu901..."
lock-version = "2.0"
```
