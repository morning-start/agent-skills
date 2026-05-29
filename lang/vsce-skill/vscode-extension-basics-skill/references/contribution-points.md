# Contribution Points

## 目录
- [概览](#概览)
- [commands](#commands)
- [menus](#menus)
- [configuration](#configuration)
- [views](#views)
- [keybindings](#keybindings)

## 概览
贡献点允许扩展声明式地扩展 VSCode 功能，无需编写代码即可集成到 VSCode UI。

## commands
注册命令到命令面板：
```json
{
  "contributes": {
    "commands": [
      {
        "command": "extension.helloWorld",
        "title": "Hello World",
        "category": "My Extension"
      }
    ]
  }
}
```

## menus
自定义菜单项：
```json
{
  "contributes": {
    "menus": {
      "commandPalette": [
        {
          "command": "extension.helloWorld",
          "when": "editorLangId == markdown"
        }
      ]
    }
  }
}
```

## configuration
添加配置项：
```json
{
  "contributes": {
    "configuration": {
      "title": "My Extension",
      "properties": {
        "myExtension.enable": {
          "type": "boolean",
          "default": true,
          "description": "Enable extension"
        }
      }
    }
  }
}
```

## views
贡献视图到侧边栏：
```json
{
  "contributes": {
    "views": {
      "explorer": [
        {
          "id": "myView",
          "name": "My View"
        }
      ]
    }
  }
}
```

## keybindings
定义快捷键：
```json
{
  "contributes": {
    "keybindings": [
      {
        "command": "extension.helloWorld",
        "key": "ctrl+shift+h",
        "mac": "cmd+shift+h"
      }
    ]
  }
}
```
