# Git 命令速查表

## 目录
- [仓库操作](#仓库操作)
- [基础快照](#基础快照)
- [分支管理](#分支管理)
- [远程协作](#远程协作)
- [历史查看](#历史查看)
- [撤销与恢复](#撤销与恢复)
- [高级操作](#高级操作)

## 仓库操作

### 初始化与克隆
```bash
git init                      # 初始化本地仓库
git clone <url>               # 克隆远程仓库
git clone <url> <目录名>      # 克隆到指定目录
git clone --depth 1 <url>     # 浅克隆（只含最新提交）
```

### 远程仓库
```bash
git remote -v                # 查看远程仓库
git remote add <名称> <url>   # 添加远程仓库
git remote remove <名称>      # 删除远程仓库
git remote rename <旧名> <新名> # 重命名远程仓库
```

## 基础快照

### 暂存与提交
```bash
git add <文件>                # 暂存单个文件
git add .                     # 暂存所有更改
git add -p                    # 交互式暂存（部分暂存）
git commit -m "消息"          # 提交暂存区
git commit -am "消息"         # 直接提交所有跟踪文件的更改
git commit --amend           # 修改最后一次提交
```

### 查看状态
```bash
git status                    # 查看完整状态
git status -s                 # 简洁状态输出
git diff                      # 查看未暂存的更改
git diff --staged            # 查看已暂存的更改
git diff HEAD                # 查看所有更改（已/未暂存）
```

## 分支管理

### 创建与切换
```bash
git branch                    # 列出本地分支
git branch -a                 # 列出所有分支（含远程）
git branch <名称>             # 创建新分支
git checkout <分支>           # 切换分支
git checkout -b <分支>        # 创建并切换
git switch <分支>             # 切换分支（现代语法）
git switch -c <分支>          # 创建并切换
```

### 合并分支
```bash
git merge <分支>              # 合并指定分支到当前分支
git merge --no-ff <分支>      # 合并（禁用快进合并）
git merge --squash <分支>     # 压缩合并
```

### 删除分支
```bash
git branch -d <分支>          # 删除已合并的分支
git branch -D <分支>          # 强制删除分支
git push origin --delete <分支> # 删除远程分支
```

## 远程协作

### 获取与拉取
```bash
git fetch                     # 获取远程更新（不合并）
git pull                      # 拉取并合并
git pull --rebase            # 拉取并变基
```

### 推送
```bash
git push                      # 推送到默认远程
git push origin <分支>        # 推送到指定分支
git push -u origin <分支>     # 推送并设置上游
git push --force             # 强制推送（慎用）
git push --force-with-lease  # 安全的强制推送
```

## 历史查看

### 提交历史
```bash
git log                       # 查看完整提交历史
git log --oneline            # 简洁视图
git log --graph              # 图形化视图
git log -n <数量>             # 查看最近N条
git log --author=<作者>       # 按作者过滤
git log --since=<日期>        # 按时间过滤
```

### 文件历史
```bash
git show <commit>            # 查看某次提交
git blame <文件>             # 查看文件每行最后修改者
git log -p <文件>            # 查看文件变更历史
```

### 差异对比
```bash
git diff <分支1> <分支2>      # 比较两个分支
git diff <commit1> <commit2>  # 比较两次提交
git diff HEAD~3 HEAD          # 比较3个提交前后的差异
```

## 撤销与恢复

### 工作区恢复
```bash
git checkout -- <文件>        # 丢弃工作区更改（危险）
git restore <文件>            # 丢弃工作区更改（新语法）
git restore --staged <文件>   # 取消暂存
```

### 重置提交
```bash
git reset --soft HEAD~1      # 撤销提交，保留更改在暂存区
git reset --mixed HEAD~1      # 撤销提交，保留更改在工作区（默认）
git reset --hard HEAD~1      # 撤销提交，丢弃所有更改（危险）
```

### 回退与反转
```bash
git revert <commit>          # 创建新提交反转指定提交
git checkout <commit>        # 查看历史提交（分离头指针）
```

## 高级操作

### 储藏
```bash
git stash                     # 储藏当前更改
git stash pop                # 应用并删除最新储藏
git stash apply              # 应用储藏（保留储藏）
git stash list               # 查看储藏列表
git stash drop               # 删除储藏
```

### 变基
```bash
git rebase <分支>            # 变基到指定分支
git rebase -i HEAD~3         # 交互式变基（修改最近3个提交）
git rebase --onto <新基> <旧基> # 变基到新基础
```

### 标签
```bash
git tag                      # 列出标签
git tag <名称>               # 创建轻量标签
git tag -a <名称> -m "消息"   # 创建附注标签
git tag -d <名称>            # 删除标签
git push origin <标签>       # 推送标签
git push origin --tags       # 推送所有标签
```

### 子模块
```bash
git submodule add <url> <路径> # 添加子模块
git submodule update --init   # 初始化子模块
git submodule update --remote # 更新子模块
```

### 其他
```bash
git cherry-pick <commit>      # 挑拣提交
git bisect start             # 开始二分查找
git bisect bad               # 标记当前为坏提交
git bisect good <commit>     # 标记为好提交
git reflog                   # 查看操作历史
git gc                       # 垃圾回收和优化
git fsck                     # 检查仓库完整性
```