---
name: vscode-extension-treeview
description: 掌握VSCode TreeView开发，在侧边栏创建自定义视图，实现数据提供者和视图操作
---

# VSCode Extension TreeView

## 任务目标
- 本 Skill 用于：在 VSCode 侧边栏创建自定义树形视图展示数据
- 能力包含：TreeDataProvider、View Container、View Actions、视图刷新
- 触发条件：当用户需要展示层次结构数据或创建自定义视图时

## 前置准备
- 环境要求：已完成 vscode-extension-basics 学习
- 前置知识：TypeScript 基础

## 操作步骤

### 标准流程

#### 1. 声明 TreeView 贡献点
```json
{
  "contributes": {
    "views": {
      "explorer": [
        {
          "id": "nodeDependencies",
          "name": "Node Dependencies"
        }
      ]
    }
  }
}
```

#### 2. 实现 TreeDataProvider
```typescript
export class MyTreeDataProvider implements vscode.TreeDataProvider<MyTreeItem> {
  getTreeItem(element: MyTreeItem): vscode.TreeItem {
    return element;
  }

  getChildren(element?: MyTreeItem): Thenable<MyTreeItem[]> {
    if (!element) {
      return Promise.resolve(this.getRootItems());
    }
    return Promise.resolve(this.getChildItems(element));
  }
}
```

#### 3. 注册 TreeDataProvider
```typescript
const provider = new MyTreeDataProvider();
vscode.window.registerTreeDataProvider('myView', provider);

// 或创建 TreeView 以获取更多控制
const treeView = vscode.window.createTreeView('myView', {
  treeDataProvider: provider
});
```

#### 4. 创建 TreeItem
```typescript
class MyTreeItem extends vscode.TreeItem {
  constructor(
    public readonly label: string,
    public readonly collapsibleState: vscode.TreeItemCollapsibleState
  ) {
    super(label, collapsibleState);
    this.tooltip = `${label} - description`;
    this.description = 'version 1.0';
  }
}
```

#### 5. 添加视图刷新功能
```typescript
class MyTreeDataProvider implements vscode.TreeDataProvider<MyTreeItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<MyTreeItem>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }
}

// 添加刷新命令
vscode.commands.registerCommand('myView.refresh', () => {
  provider.refresh();
});
```

### 可选分支

#### 当需要添加视图操作按钮时
```json
{
  "contributes": {
    "commands": [{
      "command": "myView.refresh",
      "title": "Refresh",
      "icon": "media/refresh.svg"
    }],
    "menus": {
      "view/title": [{
        "command": "myView.refresh",
        "when": "view == myView",
        "group": "navigation"
      }]
    }
  }
}
```

#### 当需要创建 View Container 时
```json
{
  "contributes": {
    "viewsContainers": {
      "activitybar": [{
        "id": "myContainer",
        "title": "My Container",
        "icon": "media/icon.svg"
      }]
    },
    "views": {
      "myContainer": [{
        "id": "myView",
        "name": "My View"
      }]
    }
  }
}
```

## 资源索引

### 领域参考
- [references/treeview-basics.md](references/treeview-basics.md)
  - 何时读取：需要创建基本树视图时
  - 内容：TreeDataProvider 实现、TreeItem 创建

- [references/treeview-advanced.md](references/treeview-advanced.md)
  - 何时读取：需要高级视图功能时
  - 内容：View Container、View Actions、Welcome Content

## 注意事项

### 性能优化
- 懒加载子节点
- 实现 onDidChangeTreeData 事件支持刷新
- 避免一次性加载大量数据

### 用户体验
- 提供有意义的图标和描述
- 支持键盘导航
- 在视图中显示 Welcome Content 当空时
