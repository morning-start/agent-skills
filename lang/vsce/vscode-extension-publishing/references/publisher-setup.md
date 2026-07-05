# Publisher Setup

## 目录
- [概览](#概览)
- [创建 Azure PAT](#创建-azure-pat)
- [创建 Publisher](#创建-publisher)
- [验证账号](#验证账号)

## 概览
设置 VSCode Marketplace 发布所需的账号和凭证。

## 创建 Azure PAT
1. 访问 Azure DevOps → 用户设置 → Personal access tokens
2. 创建新 Token
3. Organization: All accessible organizations
4. Scopes: Marketplace > Manage

## 创建 Publisher
1. 访问 https://marketplace.visualstudio.com/manage
2. 登录 Microsoft 账号
3. 点击 "Create publisher"
4. 填写 ID（唯一标识）和 Name（显示名）

## 验证账号
```bash
vsce login <publisher-id>
# 输入 PAT token
```
