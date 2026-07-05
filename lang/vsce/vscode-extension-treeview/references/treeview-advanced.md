# TreeView Advanced

## 目录
- [概览](#概览)
- [View Container](#view-container)
- [View Actions](#view-actions)
- [Welcome Content](#welcome-content)

## 概览
高级 TreeView 功能，包括自定义视图容器、视图操作和欢迎内容。

## View Container
在 Activity Bar 创建自定义容器：
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

## View Actions
添加视图标题栏按钮：
```json
{
  "contributes": {
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

## Welcome Content
视图为空时显示的内容：
```json
{
  "contributes": {
    "viewsWelcome": [{
      "view": "myView",
      "contents": "No items found. [Add Item](command:myView.add)"
    }]
  }
}
```
