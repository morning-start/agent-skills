---
name: export-manager
version: 0.1.0
description: 支持文档多格式导出（Markdown/PDF/HTML/ZIP）
---

# Export Manager

## 职责

- 支持 Markdown 格式打包
- 支持 HTML 格式导出
- 支持 PDF 格式导出
- 支持 ZIP 压缩包导出

## 输入

- 文档集路径
- 导出格式选择

## 输出

- 导出文件（.md / .html / .pdf / .zip）

## 导出格式

### Markdown（默认）

- 保持原始 Markdown 文件
- 包含目录结构
- 适用于 Git 仓库

### HTML

- 转换为带样式的 HTML 文件
- 包含侧边栏导航
- 支持搜索功能
- 配色：亮色主题

### PDF

- 转换为 PDF 文件
- 包含目录页
- 分页控制
- 打印优化

### ZIP

- 打包所有文档
- 包含目录结构
- 可包含图片和附件

## 使用场景

| 场景 | 推荐格式 |
|------|---------|
| 代码仓库 | Markdown |
| 内部分享 | HTML |
| 正式交付 | PDF |
| 离线存档 | ZIP |

## 注意事项

- Markdown 导出保持原始格式，不做转换
- HTML 导出需要包含完整样式
- PDF 导出需要处理分页和目录
- ZIP 导出需要包含完整目录结构
- 导出文件命名规范：`{project-name}-docs-{version}.{ext}`
