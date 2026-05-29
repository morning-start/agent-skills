# Git 工作流指南

## 目录
- [工作流概述](#工作流概述)
- [集中式工作流](#集中式工作流)
- [功能分支工作流](#功能分支工作流)
- [Gitflow 工作流](#gitflow-工作流)
- [Forking 工作流](#forking-工作流)
- [选择建议](#选择建议)

## 工作流概述

Git 工作流是团队使用 Git 进行协作的实践方式。选择合适的工作流取决于团队规模、项目类型和发布周期。

## 集中式工作流

### 适用场景
- 小型团队（2-5人）
- 快速迭代项目
- 无需长期维护多版本

### 分支策略
```
只有一个分支：main/master
所有成员直接提交到这个分支
```

### 操作流程
1. 克隆中央仓库
2. 在 main 分支开发
3. 提交更改
4. 推送前先拉取最新代码
5. 解决冲突（如有）
6. 推送到中央仓库

### 优点
- 简单直观
- 适合小型团队
- 易于管理

### 缺点
- 无法隔离功能开发
- 大型项目难以管理
- 无法追踪功能历史

## 功能分支工作流

### 适用场景
- 中型团队（5-15人）
- 需要并行开发多个功能
- 有代码审查需求

### 分支策略
```
main: 主分支，只接受合并
feature/xxx: 功能分支
bugfix/xxx: 修复分支
```

### 操作流程
1. 从 main 创建功能分支
2. 在功能分支开发
3. 提交到本地仓库
4. 推送分支到远程
5. 创建 Pull Request
6. 代码审查
7. 合并到 main
8. 删除功能分支

### 优点
- 隔离功能开发
- 支持代码审查
- 便于并行工作

### 缺点
- 需要团队熟悉分支操作
- 分支管理较复杂

## Gitflow 工作流

### 适用场景
- 大型团队（15人以上）
- 需要维护多个版本
- 有明确的发布周期

### 分支策略
```
main: 主分支，始终与发布版本同步
develop: 开发分支，集成所有功能
feature/xxx: 功能分支
release/xxx: 发布分支
hotfix/xxx: 热修复分支
```

### 分支生命周期

#### 功能分支
1. 从 develop 创建
2. 开发完成后合并到 develop
3. 删除分支

#### 发布分支
1. 从 develop 创建
2. 进行发布准备（修复小问题）
3. 合并到 main 并打标签
4. 合并回 develop
5. 删除分支

#### 热修复分支
1. 从 main 创建
2. 修复完成后合并到 main 和 develop
3. 为 main 打上新标签
4. 删除分支

### 操作流程

#### 开发新功能
1. `git checkout -b feature/xxx develop`
2. 开发并提交
3. `git checkout develop`
4. `git merge --no-ff feature/xxx`
5. `git branch -d feature/xxx`
6. `git push origin develop`

#### 创建发布
1. `git checkout -b release/1.0.0 develop`
2. 修复小问题
3. `git checkout main`
4. `git merge --no-ff release/1.0.0`
5. `git tag -a 1.0.0 -m "Release 1.0.0"`
6. `git push origin main --tags`
7. `git checkout develop`
8. `git merge --no-ff release/1.0.0`
9. `git branch -d release/1.0.0`

#### 热修复
1. `git checkout -b hotfix/1.0.1 main`
2. 修复问题
3. `git checkout main`
4. `git merge --no-ff hotfix/1.0.1`
5. `git tag -a 1.0.1 -m "Hotfix 1.0.1"`
6. `git push origin main --tags`
7. `git checkout develop`
8. `git merge --no-ff hotfix/1.0.1`
9. `git branch -d hotfix/1.0.1`

### 优点
- 适合复杂项目
- 明确的版本维护策略
- 支持多版本并行

### 缺点
- 较为复杂
- 分支较多
- 需要团队高度配合

## Forking 工作流

### 适用场景
- 开源项目
- 大型分布式团队
- 需要贡献者隔离

### 分支策略
```
上游仓库（官方）
  └── fork 克隆
        └── 个人仓库
              └── 本地克隆
                    └── feature 分支
```

### 操作流程
1. Fork 官方仓库到个人账户
2. Clone 个人仓库到本地
3. 添加上游仓库链接
4. 创建功能分支
5. 提交并推送到个人仓库
6. 创建 Pull Request 到官方仓库
7. 等待维护者审查和合并

### 优点
- 完全隔离贡献者
- 适合开源项目
- 易于管理权限

### 缺点
- 需要贡献者熟悉 Git
- 流程相对复杂
- 需要维护多个远程

## 选择建议

### 按团队规模选择
| 团队规模 | 推荐工作流 |
|---------|-----------|
| 1-5人 | 集中式工作流 |
| 5-15人 | 功能分支工作流 |
| 15人以上 | Gitflow 工作流 |
| 开源项目 | Forking 工作流 |

### 按项目类型选择
| 项目类型 | 推荐工作流 |
|---------|-----------|
| MVP/原型 | 集中式工作流 |
| SaaS 应用 | 功能分支/Gitflow |
| 库/框架 | Forking + 功能分支 |
| 多版本产品 | Gitflow |

### 按发布周期选择
| 发布周期 | 推荐工作流 |
|---------|-----------|
| 持续发布 | 集中式/功能分支 |
| 定期发布 | 功能分支/Gitflow |
| 多版本并行 | Gitflow |

### 混合策略
可以根据实际情况组合使用：
- 小团队可以用简化版 Gitflow
- 大型项目可以用 Gitflow + Forking
- 内部项目可以用功能分支 + 代码审查