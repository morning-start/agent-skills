# Git 提交规范指南

## 目录
- [何时提交](#何时提交)
- [提交原则](#提交原则)
- [提交标准](#提交标准)
- [提交信息格式](#提交信息格式)
- [团队协作实践](#团队协作实践)
- [实际工作流](#实际工作流)
- [常见问题](#常见问题)

## 何时提交

### 应该提交的场景

| 场景         | 说明                     | 示例                   |
| ------------ | ------------------------ | ---------------------- |
| 完成一个功能 | 完成一个独立的功能点     | 添加用户登录功能       |
| 修复一个 bug | 解决一个具体问题         | 修复登录页面白屏问题   |
| 重构代码     | 改进代码结构但不改变行为 | 提取重复代码为工具函数 |
| 添加测试     | 新增或修改测试用例       | 添加单元测试覆盖       |
| 更新文档     | 完善或修正文档内容       | 更新 API 文档          |
| 配置文件变更 | 修改项目配置             | 更新 ESLint 规则       |

### 不应该提交的场景

| 场景                      | 原因               | 处理方式                    |
| ------------------------- | ------------------ | --------------------------- |
| 调试代码                  | 临时调试代码       | 删除后再提交                |
| 未完成的 work-in-progress | 破坏构建完整性     | 使用 `git stash` 或单独分支 |
| 生成文件                  | 可以从源码重新生成 | 添加到 `.gitignore`         |
| 敏感信息                  | 安全风险           | 使用环境变量或配置模板      |
| 无关的修改                | 污染提交历史       | 拆分独立提交                |

## 提交原则

### 原子性原则
**每次提交只做一件事**

✅ 好的做法：
```
commit 1: feat: 添加用户注册功能
commit 2: test: 添加用户注册单元测试
commit 3: docs: 更新用户注册文档
```

❌ 不好的做法：
```
commit 1: feat: 添加用户功能、修复样式问题、更新文档
```

### 小步快跑原则
**将大的功能拆分成小的、可验证的步骤，并频繁提交**

- 方便备份和与团队同步
- 降低合并冲突的风险
- 便于精准回滚

### 易于审查原则
**原子化的提交让代码审查者能轻松理解变更意图**

- 如果出现问题，可以安全、精准地回滚单个提交
- 不会影响其他无关的修改

### 顺序原则
**确定多提交时的先后顺序**

#### 按逻辑依赖排序
如果 A 依赖 B，先提交 B：
```
先: refactor(auth): 提取 Token 工具函数
后: fix(order): 使用新 Token 工具修复回调问题
```

#### 按影响范围排序
小范围 → 大范围：
```
先: fix(ui): 修复按钮样式
后: feat(order): 添加订单导出功能
```

#### 按层次排序
底层 → 上层：
```
先: chore: 升级核心依赖
先: refactor(core): 重构核心模块
后: feat(order): 添加订单功能
```

#### 按类型排序
代码 → 测试 → 文档：
```
1. feat(order): 添加订单导出功能
2. test(order): 添加订单导出测试
3. docs(order): 更新订单功能文档
```

## 提交标准

### Conventional Commits 规范

格式：
```
<type>(<scope>): <subject>
```

| 部分      | 说明             | 必填 |
| --------- | ---------------- | ---- |
| `type`    | 提交类型         | ✅    |
| `scope`   | 影响范围（可选） | ❌    |
| `subject` | 简短描述         | ✅    |

### Type 类型

| Type       | 说明                            | 示例                          |
| ---------- | ------------------------------- | ----------------------------- |
| `feat`     | 新功能                          | `feat: 添加用户登录功能`      |
| `fix`      | Bug 修复                        | `fix: 修复登录超时问题`       |
| `docs`     | 仅文档变更                      | `docs: 更新 API 文档`         |
| `style`    | 不影响代码逻辑的格式调整        | `style: 格式化代码`           |
| `refactor` | 代码重构（非新功能非 Bug 修复） | `refactor: 拆分 UserService`  |
| `perf`     | 性能优化                        | `perf: 优化图片加载速度`      |
| `test`     | 增加或修改测试                  | `test: 添加单元测试`          |
| `build`    | 构建、依赖或辅助工具变动        | `build: 升级 webpack`         |
| `ci`       | CI 配置变更                     | `ci: 添加 GitHub Actions`     |
| `chore`    | 其他杂项                        | `chore: 更新依赖版本`         |
| `revert`   | 回退提交                        | `revert: 回退 feat: 添加登录` |

### Scope 范围

用于指明本次提交影响的模块，帮助快速定位变更区域：

| Scope       | 说明     | 示例                          |
| ----------- | -------- | ----------------------------- |
| `(auth)`    | 认证模块 | `feat(auth): 添加第三方登录`  |
| `(user)`    | 用户模块 | `fix(user): 修复头像上传`     |
| `(api)`     | API 接口 | `refactor(api): 重构用户接口` |
| `(order)`   | 订单模块 | `feat(order): 新增订单导出`   |
| `(payment)` | 支付模块 | `fix(payment): 修复支付回调`  |
| `(ui)`      | 界面相关 | `style(ui): 调整按钮样式`     |

### Description 描述

对本次变更的简短描述：

- 使用**祈使句、现在时**（用 "add" 而不是 "added"）
- 首字母**不大写**
- 结尾**不加句号**
- 长度建议在 **50 个字符以内**

### 优秀示例对比

| 不好的示例 | 好的示例                                    |
| ---------- | ------------------------------------------- |
| `fix`      | `fix(auth): 修复 token 过期后未自动刷新`    |
| `update`   | `feat(order): 新增订单列表分页功能`         |
| `wip`      | `refactor(user): 拆分 UserService 鉴权逻辑` |
| `改了一下` | `chore: 升级 webpack 到 v5`                 |

## 提交信息格式

### 简短格式
```
type: 简短描述
```
示例：`feat: 添加用户积分功能`

### 完整格式
```
type: 简短描述（不超过50字符）

详细说明（可选，超过50字符应换行）
可以多行描述

关联的 Issue 或其他信息
Closes #123
```

### 完整示例

```
feat: 添加用户积分功能

用户可以通过积分系统获得奖励
积分可以兑换商品或折扣

Closes #45
Related to #30
```

```
refactor(user): 提取 HTTP 请求工具函数

将分散在各组件中的 HTTP 请求提取为独立函数
统一错误处理和请求拦截逻辑

BREAKING CHANGE: 需要更新所有调用处
```

## 如何实现原子性提交

使用 `git add -p` 命令逐块（hunk）显示修改，让你选择性暂存：

```bash
git add -p
```

交互式选项：
| 选项 | 说明       |
| ---- | ---------- |
| `y`  | 暂存此块   |
| `n`  | 不暂存此块 |
| `s`  | 拆分当前块 |
| `q`  | 退出       |

## 团队协作实践

### 代码审查 (Code Review)
- PR/MR 是代码质量的守门员
- 提交规范是高效审查的前提
- 审查者可以基于清晰的提交历史，聚焦于代码逻辑和安全性

### 自动化检查
使用工具在提交前自动检查格式：

| 工具         | 说明                                 |
| ------------ | ------------------------------------ |
| `commitlint` | 检查提交信息格式                     |
| `husky`      | Git hooks 工具，在 commit 时触发检查 |

配置示例：
```bash
# 安装
npm install --save-dev @commitlint/cli @commitlint/config-conventional husky

# commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional']
};
```

### 自动生成变更日志
坚持使用规范的 `type`（feat、fix 等），可使用工具自动生成 CHANGELOG：

| 工具               | 说明                           |
| ------------------ | ------------------------------ |
| `standard-version` | 基于提交历史自动生成 CHANGELOG |
| `release-it`       | 自动化版本发布工具             |

```bash
npm install --save-dev standard-version
npx standard-version --dry-run  # 预览
npx standard-version            # 执行
```

## 实际工作流

### 工作流程 1：完成功能后提交
```
1. 完成功能代码
2. git status                    # 查看修改
3. git add src/feature/          # 暂存相关文件
4. git commit -m "feat(order): 添加订单导出功能"
5. git push                       # 推送
```

### 工作流程 2：修复 Bug 后提交
```
1. 复现并定位 Bug
2. 编写测试验证 Bug 存在（可选）
3. 修复 Bug
4. git add <修复的文件>
5. git commit -m "fix(auth): 修复 token 过期后未自动刷新"
6. 运行测试确认修复
7. git push
```

### 工作流程 3：多文件修改分类提交
```
1. 修改了代码、测试和文档
2. git status                    # 查看所有修改

3. git add src/                  # 先提交代码
4. git commit -m "feat(order): 添加订单导出功能"

5. git add tests/                # 再提交测试
6. git commit -m "test(order): 添加订单导出测试"

7. git add docs/                  # 最后提交文档
8. git commit -m "docs(order): 更新订单功能文档"

9. git push                       # 统一推送
```

### 工作流程 4：使用 git add -p 实现原子性提交
```
1. 修改了多个不相关的内容
2. git add -p                     # 交互式暂存

# 对每个块选择：
# y - 暂存此块
# n - 不暂存此块

3. git diff --staged              # 确认暂存内容
4. git commit -m "fix(ui): 修复按钮样式"
5. git add -p                     # 继续暂存下一块
6. git commit -m "refactor(api): 简化接口调用"
```

### 工作流程 5：WIP（进行中）提交
```
1. 功能还未完成，但需要切换分支
2. git add <已完成的部分>
3. git commit -m "feat(user): 用户模块 WIP"
4. git push                       # 推送到远程备份
5. git checkout other-branch
```

### 工作流程 6：合并提交
```
1. git rebase -i HEAD~3          # 交互式变基
2. 将后面的提交 squash 或 fixup
3. 保存退出
4. 更新提交信息
```

### 工作流程 7：回退提交
```
1. git log --oneline              # 找到要回退的提交
2. git revert <commit-hash>      # 创建反向提交
3. 输入回退原因
4. git push                       # 推送回退
```

## 常见问题

### Q: 提交信息写错了怎么办
```bash
git commit --amend                 # 修改最后一次提交
```

### Q: 提交到了错误的分支
```bash
# 撤销提交，保留更改
git reset --soft HEAD~
# 切换正确分支
git checkout correct-branch
# 重新提交
git commit -m "feat: xxx"
```

### Q: 漏提交了文件怎么办
```bash
# 追加到上一个提交
git add <漏掉的文件>
git commit --amend
```

### Q: 提交信息格式不规范想统一修改
```bash
git rebase -i HEAD~10            # 修改最近10个提交
# 将需要修改的 pick 改为 reword
```

### Q: 如何查看提交历史
```bash
git log                           # 完整历史
git log --oneline                 # 简洁历史
git log --graph                   # 图形化历史
git log --author="name"          # 按作者过滤
git log --since="2024-01-01"     # 按时间过滤
```