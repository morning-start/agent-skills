# 架构概览

## 目录
- [概览](#概览)
- [三层架构](#三层架构)
- [层依赖关系](#层依赖关系)
- [sitecustomize.py 机制](#sitecustomizepy-机制)

## 概览
venvstacks 使用三层虚拟环境架构，实现 Python 依赖的分解、单独部署和更新。

## 三层架构

### Runtime 层
- 包含特定版本 Python 解释器
- 是其他所有层的基础
- 预装常用包（如 numpy）

```toml
[[runtimes]]
name = "cpython@3.11"
fully_versioned_name = "cpython@3.11.10"
requirements = [
    "numpy",
]
```

### Framework 层
- 包含关键 Python 框架
- 可被多个应用层共享
- 依赖一个 Runtime 层

```toml
[[frameworks]]
name = "pytorch"
runtime = "cpython@3.11"
requirements = [
    "torch",
]
```

### Application 层
- 包含可直接启动的组件
- 可依赖多个 Framework 层
- 定义启动模块

```toml
[[applications]]
name = "ml-inference"
launch_module = "inference_server"
frameworks = ["pytorch"]
requirements = [
    "transformers",
]
```

## 层依赖关系
```
Runtime (cpython@3.11)
    └── Framework (pytorch)
            └── Application (ml-inference)
```

## sitecustomize.py 机制
sitecustomize.py 注入到层的 site-packages 目录，允许代码从构建环境导入依赖层的包，实现层间链接。
