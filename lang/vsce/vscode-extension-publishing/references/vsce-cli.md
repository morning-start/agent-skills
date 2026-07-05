# vsce CLI

## 目录
- [概览](#概览)
- [publish](#publish)
- [package](#package)
- [login](#login)

## 概览
vsce (Visual Studio Code Extensions) 是扩展管理的命令行工具。

## publish
发布扩展到 Marketplace：
```bash
vsce publish                  # 发布
vsce publish minor           # 自动增加 minor 版本
vsce publish 1.2.0          # 指定版本
vsce publish --pre-release  # 预发布
```

## package
打包扩展为 .vsix：
```bash
vsce package                  # 打包
vsce package --pre-release   # 预发布打包
vsce package --target win32-x64  # 特定平台
```

## login
登录发布者账号：
```bash
vsce login <publisher-id>
```

## 其他命令
```bash
vsce --help           # 显示帮助
vsce --version        # 显示版本
vsce list             # 列出已发布的扩展
vsce unpublish <id>   # 下架扩展
```
