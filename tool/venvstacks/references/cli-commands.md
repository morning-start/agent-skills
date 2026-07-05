# CLI 命令详解

## 目录
- [lock](#lock)
- [build](#build)
- [local-export](#local-export)
- [publish](#publish)

## lock
锁定层依赖：
```bash
venvstacks lock <stack.toml>
```

输出：
- requirements/ 文件夹（锁定文件）
- *.lock.toml 元数据
- *_summary.txt 包摘要

## build
构建层环境：
```bash
venvstacks build <stack.toml>

# 指定目标平台
venvstacks build --target linux-x64 <stack.toml>

# 完整流水线（锁定+构建+发布）
venvstacks build --publish --tag-outputs --output-dir artifacts <stack.toml>
```

## local-export
本地导出（快速测试）：
```bash
venvstacks local-export --output-dir <dir> <stack.toml>
```

用途：
- 迭代层定义时快速测试
- 跳过归档打包/解压步骤

## publish
发布归档：
```bash
venvstacks publish --tag-outputs --output-dir <dir> <stack.toml>
```

输出：
- *.tar.zst 归档文件
- __venvstacks__/ 元数据文件夹

## 命令执行顺序
```bash
# 完整发布流程
venvstacks lock stack.toml          # 1. 锁定依赖
venvstacks build stack.toml          # 2. 构建环境
venvstacks publish stack.toml        # 3. 发布归档
```

## 常用选项
| 选项 | 说明 |
|------|------|
| --target | 指定目标平台 |
| --tag-outputs | 自动添加平台标签 |
| --output-dir | 输出目录 |
| --publish | 包含发布步骤 |
