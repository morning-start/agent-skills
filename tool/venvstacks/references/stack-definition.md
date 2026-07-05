# 栈定义规范

## 目录
- [概览](#概览)
- [Runtime 定义](#runtime-定义)
- [Framework 定义](#framework-定义)
- [Application 定义](#application-定义)
- [完整示例](#完整示例)

## 概览
venvstacks.toml 是栈规范文件，定义所有层的配置。

## Runtime 定义
```toml
[[runtimes]]
name = "cpython@3.11"
fully_versioned_name = "cpython@3.11.10"
requirements = [
    "numpy>=1.24",
]
```

| 字段 | 说明 |
|------|------|
| name | 层名称（格式：runtime名@版本） |
| fully_versioned_name | 完全版本化名称 |
| requirements | 预装包列表 |

## Framework 定义
```toml
[[frameworks]]
name = "sklearn"
runtime = "cpython@3.11"
requirements = [
    "scikit-learn>=1.3",
]
```

| 字段 | 说明 |
|------|------|
| name | 框架名称 |
| runtime | 依赖的 Runtime 层名 |
| requirements | 框架包列表 |

## Application 定义
```toml
[[applications]]
name = "classification-demo"
launch_module = "launch_modules/sklearn_classification.py"
frameworks = ["sklearn"]
requirements = [
    "scikit-learn",
]
```

| 字段 | 说明 |
|------|------|
| name | 应用名称 |
| launch_module | 启动模块名 |
| frameworks | 依赖的 Framework 层列表 |
| requirements | 应用专属包列表 |

## 完整示例
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
