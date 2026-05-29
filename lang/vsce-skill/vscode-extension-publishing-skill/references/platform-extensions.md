# Platform Extensions

## 目录
- [概览](#概览)
- [支持平台](#支持平台)
- [打包发布](#打包发布)

## 概览
发布针对特定平台的扩展包，包含原生依赖或二进制文件。

## 支持平台
- win32-x64
- win32-arm64
- linux-x64
- linux-arm64
- linux-armhf
- alpine-x64
- alpine-arm64
- darwin-x64
- darwin-arm64
- web

## 打包发布
```bash
# 打包单个平台
vsce package --target win32-x64

# 打包多个平台
vsce package --target win32-x64 win32-arm64 linux-x64

# 发布所有平台
vsce publish --target win32-x64 win32-arm64 linux-x64
```
