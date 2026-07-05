# TreeView Basics

## 目录
- [概览](#概览)
- [TreeDataProvider](#treedataprovider)
- [TreeItem](#treeitem)
- [注册Provider](#注册provider)

## 概览
TreeView API 用于在 VSCode 侧边栏显示层次结构数据。

## TreeDataProvider
```typescript
export class MyProvider implements vscode.TreeDataProvider<MyItem> {
  getTreeItem(element: MyItem): vscode.TreeItem {
    return element;
  }

  getChildren(element?: MyItem): Thenable<MyItem[]> {
    if (!element) {
      return this.getRoot();
    }
    return this.getChildrenOf(element);
  }
}
```

## TreeItem
```typescript
class MyItem extends vscode.TreeItem {
  constructor(
    public readonly label: string,
    public readonly collapsibleState: vscode.TreeItemCollapsibleState
  ) {
    super(label, collapsibleState);
  }
}
```

## 注册Provider
```typescript
vscode.window.registerTreeDataProvider('myView', new MyProvider());
```
