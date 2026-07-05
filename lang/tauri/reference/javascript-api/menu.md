# menu 命名空间

`menu` 命名空间提供应用菜单和上下文菜单的创建与管理功能。

## 导入

```typescript
import { Menu, MenuItem, Submenu, MenuItemKind } from '@tauri-apps/api/menu';
```

## 函数

### newMenu(items: MenuItem[]): Promise<Menu>

创建新菜单。

```typescript
async function newMenu(items: MenuItem[]): Promise<Menu>
```

**示例：**
```typescript
import { Menu, MenuItem } from '@tauri-apps/api/menu';

const menu = await Menu.new({
  items: [
    {
      item: 'MenuItem',
      id: 'open',
      text: '打开文件',
      accelerator: 'CmdOrCtrl+O',
    },
    {
      item: 'MenuItem',
      id: 'quit',
      text: '退出',
      accelerator: 'CmdOrCtrl+Q',
    }
  ]
});
```

### setAsAppMenu(menu: Menu): Promise<void>

将菜单设置为应用菜单。

```typescript
await menu.setAsAppMenu();
```

### setAsContextMenu(menu: Menu): Promise<void>

将菜单设置为上下文菜单。

```typescript
await menu.setAsContextMenu();
```

## MenuItem 类型

### 普通菜单项

```typescript
{
  item: 'MenuItem',
  id: 'save',
  text: '保存',
  accelerator: 'CmdOrCtrl+S',
  enabled: true,
  selected: false
}
```

### 子菜单

```typescript
{
  item: 'Submenu',
  id: 'edit',
  text: '编辑',
  items: [
    { item: 'MenuItem', id: 'copy', text: '复制' },
    { item: 'MenuItem', id: 'paste', text: '粘贴' }
  ]
}
```

### 分隔线

```typescript
{
  item: 'Separator'
}
```

### 复选框

```typescript
{
  item: 'CheckMenuItem',
  id: 'auto-save',
  text: '自动保存',
  checked: true
}
```

### 单选按钮

```typescript
{
  item: 'RadioMenuItem',
  id: 'option-a',
  text: '选项 A',
  checked: true
}
```

## 事件处理

```typescript
import { onMenuItemClick } from '@tauri-apps/api/menu';

await onMenuItemClick('save', async () => {
  console.log('Save clicked!');
  // 执行保存逻辑
});
```

## 完整示例

```typescript
import { Menu, MenuItem, Submenu } from '@tauri-apps/api/menu';

const menu = await Menu.new({
  items: [
    {
      item: 'Submenu',
      id: 'file',
      text: '文件',
      items: [
        { item: 'MenuItem', id: 'new', text: '新建', accelerator: 'CmdOrCtrl+N' },
        { item: 'MenuItem', id: 'open', text: '打开', accelerator: 'CmdOrCtrl+O' },
        { item: 'Separator' },
        { item: 'MenuItem', id: 'save', text: '保存', accelerator: 'CmdOrCtrl+S' },
        { item: 'MenuItem', id: 'save-as', text: '另存为', accelerator: 'CmdOrCtrl+Shift+S' },
        { item: 'Separator' },
        { item: 'MenuItem', id: 'quit', text: '退出', accelerator: 'CmdOrCtrl+Q' }
      ]
    },
    {
      item: 'Submenu',
      id: 'edit',
      text: '编辑',
      items: [
        { item: 'MenuItem', id: 'undo', text: '撤销', accelerator: 'CmdOrCtrl+Z' },
        { item: 'MenuItem', id: 'redo', text: '重做', accelerator: 'CmdOrCtrl+Shift+Z' },
        { item: 'Separator' },
        { item: 'MenuItem', id: 'cut', text: '剪切', accelerator: 'CmdOrCtrl+X' },
        { item: 'MenuItem', id: 'copy', text: '复制', accelerator: 'CmdOrCtrl+C' },
        { item: 'MenuItem', id: 'paste', text: '粘贴', accelerator: 'CmdOrCtrl+V' }
      ]
    }
  ]
});

await menu.setAsAppMenu();
```
