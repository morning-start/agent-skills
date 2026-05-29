# Git 故障排除指南

## 目录
- [基础问题](#基础问题)
- [提交问题](#提交问题)
- [分支问题](#分支问题)
- [合并与冲突](#合并与冲突)
- [远程仓库问题](#远程仓库问题)
- [数据恢复](#数据恢复)

## 基础问题

### Q: 提示 "fatal: not a git repository"
**原因**：当前目录不是 Git 仓库
**解决**：
```bash
git init                      # 如果是本地项目
git clone <url>               # 如果要连接远程仓库
```

### Q: 提示 "nothing to commit, working tree clean"
**原因**：没有未提交的更改
**解决**：
- 检查是否在正确分支 `git branch`
- 查看提交历史 `git log --oneline`
- 检查远程状态 `git status`

### Q: 提示 "Please tell me who you are"
**原因**：未配置用户信息
**解决**：
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

## 提交问题

### Q: 提交信息写错了
**解决**：
```bash
git commit --amend           # 修改最后一次提交
# 在编辑器中修改提交信息
```

### Q: 忘记添加文件了
**解决**：
```bash
git add <遗漏的文件>
git commit --amend           # 将新添加的文件合并到上次提交
```

### Q: 提交到了错误的分支
**解决**：
```bash
# 撤销提交，保留更改
git reset --soft HEAD~1
# 切换到正确分支
git checkout correct-branch
# 重新提交
git add .
git commit -m "message"
```

### Q: 提交信息格式不规范
**解决**：使用交互式 rebase 修改
```bash
git rebase -i HEAD~3         # 修改最近3个提交
# 将 pick 改为 reword 来修改提交信息
```

## 分支问题

### Q: 分支名写错了
**解决**：
```bash
# 重命名本地分支
git branch -m old-name new-name
# 重命名当前分支
git branch -m new-name
```

### Q: 远程分支和本地分支不同步
**解决**：
```bash
git fetch --all              # 获取所有远程分支
git fetch origin              # 只获取 origin
```

### Q: 删除了远程分支，本地还能看到
**解决**：
```bash
git fetch --prune            # 清除已删除的远程分支引用
# 或
git remote prune origin
```

### Q: 切换分支时提示 "please commit your changes or stash them"
**原因**：有未提交的更改，无法切换分支
**解决**：
```bash
git stash                     # 储藏更改
git checkout other-branch
# ... 在新分支工作
git checkout original-branch
git stash pop                # 恢复储藏
```

## 合并与冲突

### Q: 合并冲突了
**解决步骤**：
1. 查看冲突文件 `git status`
2. 编辑冲突文件，删除冲突标记 `<<<<<<< ==== >>>>>>`
3. 保留正确内容
4. `git add <文件>` 标记已解决
5. `git commit` 完成合并

### Q: 冲突标记怎么用
**冲突标记格式**：
```
<<<<<<< HEAD
当前分支的内容
=======
要合并的分支的内容
>>>>>>> feature/xxx
```
**解决方式**：
- 保留 `HEAD`（当前分支）的内容
- 保留 `feature/xxx` 的内容
- 或者手动合并两边内容

### Q: 不想解决冲突了，能取消合并吗
**解决**：
```bash
git merge --abort            # 取消合并
git rebase --abort           # 取消变基
```

### Q: 合并后想撤销
**解决**：
```bash
git reset --hard ORIG_HEAD   # 撤销合并
git log -1 --format="%H" -g  # 找到合并前的提交
```

## 远程仓库问题

### Q: 推送被拒绝
**原因**：远程分支有新的提交
**解决**：
```bash
git fetch origin
git rebase origin/main       # 变基到最新
# 或
git merge origin/main         # 合并远程更改
git push
```

### Q: 强制推送后想恢复
**原因**：强制推送覆盖了远程历史
**解决**：
```bash
git reflog                    # 查看本地操作历史
git push --force origin <之前正确的commit>
```

### Q: 远程地址改变了
**解决**：
```bash
git remote set-url origin <新URL>
git remote -v                 # 确认修改
```

### Q: 想切换到 SSH 协议
**解决**：
```bash
git remote set-url origin git@github.com:user/repo.git
```

## 数据恢复

### Q: 误删了文件怎么恢复
**解决**：
```bash
git checkout -- <文件>        # 从 HEAD 恢复
git restore <文件>            # 新语法
# 如果已提交
git log --oneline -- <文件>   # 找到包含文件的提交
git checkout <提交>^ -- <文件> # 恢复该提交时的文件
```

### Q: 误删了分支怎么恢复
**解决**：
```bash
git reflog                    # 查看分支删除记录
git checkout -b <分支名> <commit-hash>  # 恢复分支
```

### Q: reset --hard 后想恢复
**解决**：
```bash
git reflog                    # 找到 reset 前的 commit
git reset --hard <commit-hash> # 恢复到那个提交
```

### Q: 提交被 squash 后想找回
**解决**：
```bash
git reflog                    # 找到 squash 前的提交
git show <commit-hash>       # 查看提交内容
```

### Q: commit 消息丢了
**解决**：
```bash
git log -1 --format="%B" <commit-hash>
git reflog                    # 找 commit hash
```

## 警告信息处理

### "detached HEAD" 警告
**原因**：当前处于游离的 HEAD 状态
**解决**：
```bash
git checkout <分支名>         # 切换到分支
# 如果想保留当前更改
git checkout -b new-branch    # 创建新分支保存
```

### "working tree clean" 但知道有更改
**原因**：.gitignore 忽略了这些文件
**解决**：
```bash
git status --ignored         # 查看忽略的文件
```

### "untracked files" 警告
**原因**：有未跟踪的新文件
**解决**：
```bash
git add .                     # 添加所有文件
# 或创建 .gitignore 忽略
```

### "Changes not staged for commit"
**原因**：文件有更改但未暂存
**解决**：
```bash
git add <文件>                # 暂存更改
git diff                      # 查看更改内容
```

## 高级恢复

### 从 dangling commit 恢复
```bash
git fsck --unreachable --no-reflogs
# 找到 dangling commit hash
git show <hash>
git branch recover <hash>
```

### 恢复特定文件的所有版本
```bash
git log --oneline -- <文件>   # 查看文件历史
git show <commit>:<文件> > recovered-<文件>  # 恢复特定版本
```

### 恢复误删的 stash
```bash
git fsck --unreachable | grep commit
git log --all --grep="WIP" --oneline
```