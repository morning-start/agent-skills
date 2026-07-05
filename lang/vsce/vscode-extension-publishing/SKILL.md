---
name: vscode-extension-publishing
description: 掌握VSCode扩展发布流程，使用vsce工具打包发布扩展到Marketplace，管理版本和平台特定扩展
---

# VSCode Extension Publishing

## 任务目标
- 本 Skill 用于：将 VSCode 扩展发布到官方 Marketplace
- 能力包含：vsce 工具使用、发布流程、平台特定扩展、预发布版本管理
- 触发条件：当用户需要发布或分发 VSCode 扩展时

## 前置准备
- 环境要求：Node.js 18+、npm
- 账号要求：Azure DevOps 账号、Marketplace 发布者账号
- 工具安装：
  ```bash
  npm install -g @vscode/vsce
  ```

## 操作步骤

### 标准流程

#### 1. 准备扩展元数据
确保 package.json 包含：
```json
{
  "name": "my-extension",
  "displayName": "My Extension",
  "publisher": "my-publisher-id",
  "version": "0.0.1",
  "engines": {
    "vscode": "^1.74.0"
  },
  "description": "Extension description"
}
```

#### 2. 创建 Personal Access Token
1. 访问 Azure DevOps → 用户设置 → Personal access tokens
2. 创建新 Token，Organization 设置为 "All accessible organizations"
3.  scopes 选择 Marketplace > Manage

#### 3. 创建 Publisher
1. 访问 https://marketplace.visualstudio.com/manage
2. 登录 Microsoft 账号
3. 创建 Publisher，填写 ID 和 Name
4. 使用 vsce 验证：
   ```bash
   vsce login <publisher-id>
   ```

#### 4. 打包扩展
```bash
# 打包为 .vsix 文件
vsce package

# 打包并指定版本
vsce package --pre-release
```

#### 5. 发布扩展
```bash
# 发布到 Marketplace
vsce publish

# 指定版本号发布
vsce publish minor  # 1.0.0 -> 1.1.0
vsce publish 2.0.0  # 指定具体版本
```

### 可选分支

#### 当需要发布预发布版本时
```bash
vsce package --pre-release
vsce publish --pre-release
```

#### 当需要平台特定扩展时
```bash
# 为特定平台打包
vsce package --target win32-x64
vsce package --target linux-x64
vsce package --target darwin-arm64

# 发布所有平台
vsce publish --target win32-x64 win32-arm64 linux-x64
```

#### 当需要自动化发布时
在 package.json 添加脚本：
```json
{
  "scripts": {
    "vscode:prepublish": "npm run compile"
  }
}
```

## 资源索引

### 领域参考
- [references/vsce-cli.md](references/vsce-cli.md)
  - 何时读取：需要了解 vsce 详细命令时
  - 内容：所有 vsce 子命令、选项、用法

- [references/publisher-setup.md](references/publisher-setup.md)
  - 何时读取：需要设置发布者账号时
  - 内容：Publisher 创建、PAT 配置、账号验证

- [references/platform-extensions.md](references/platform-extensions.md)
  - 何时读取：需要发布平台特定扩展时
  - 内容：平台支持、VSIX 构建、多平台发布

## 注意事项

### 发布限制
- 扩展名称全局唯一
- SVG 图片需转换为 PNG/JPG
- 禁止使用不受信任的 SVG badge

### 版本管理
- 遵循 SemVer 规范
- 预发布版本使用奇数 patch（如 1.0.1, 1.0.3）
- 发布版本使用偶数 patch（如 1.0.0, 1.0.2）

### Marketplace 展示
- 添加 README.md 说明
- 包含 CHANGELOG.md
- 设置有意义的 icon（128x128 PNG）
