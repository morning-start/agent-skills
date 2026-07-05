# tray 命名空间

`tray` 命名空间提供系统托盘功能，用于创建和管理托盘图标、菜单和事件。

## 导入

```typescript
import { tray, TrayIcon, TrayIconEvent, MouseButton, MouseButtonState } from '@tauri-apps/api/tray';
```

## 函数

### newTrayIcon(options: TrayIconOptions): Promise<TrayIcon>

创建新的托盘图标。

```typescript
async function newTrayIcon(options: TrayIconOptions): Promise<TrayIcon>
```

**示例：**
```typescript
import { newTrayIcon } from '@tauri-apps/api/tray';

const tray = await newTrayIcon({
  id: 'my-tray',
  icon: 'icons/icon.png',
  menu: await createTrayMenu(),
  tooltip: 'My App',
  onClick: (event) => {
    console.log('Tray clicked!');
  }
});
```

### getTrayIcon(id: string): Promise<TrayIcon>

根据 ID 获取托盘图标。

```typescript
async function getTrayIcon(id: string): Promise<TrayIcon>
```

### removeTrayIcon(id: string): Promise<void>

移除托盘图标。

```typescript
await removeTrayIcon('my-tray');
```

## TrayIcon 类

### 属性

```typescript
interface TrayIcon {
  id: string;
  icon: string;
  menu?: Menu;
  tooltip?: string;
}
```

### 方法

```typescript
const tray = await getTrayIcon('my-tray');

// 设置图标
await tray.setIcon('icons/new-icon.png');

// 设置工具提示
await tray.setTooltip('New tooltip');

// 设置菜单
await tray.setMenu(menu);

// 设置点击事件
tray.onClick((event) => { /* ... */ });

// 设置右键菜单
tray.onMenuItemClick((event) => { /* ... */ });
```

## TrayIconOptions

```typescript
interface TrayIconOptions {
  id: string;
  icon: string;
  menu?: Menu;
  tooltip?: string;
  iconAsTemplate?: boolean;
  menuOnLeftClick?: boolean;
  onClick?: (event: TrayIconEvent) => void;
  onDoubleClick?: (event: TrayIconEvent) => void;
  onMenuItemClick?: (event: MenuItemEvent) => void;
}
```

## 托盘菜单

```typescript
import { Menu, MenuItem } from '@tauri-apps/api/menu';

const menu = await Menu.new({
  items: [
    { item: 'MenuItem', id: 'show', text: '显示窗口' },
    { item: 'MenuItem', id: 'hide', text: '隐藏窗口' },
    { item: 'Separator' },
    { item: 'MenuItem', id: 'quit', text: '退出' }
  ]
});
```

## 完整示例

```typescript
import { newTrayIcon, TrayIconEvent } from '@tauri-apps/api/tray';
import { Menu, MenuItem } from '@tauri-apps/api/menu';
import { getCurrentWindow } from '@tauri-apps/api/window';

async function createTray() {
  const menu = await Menu.new({
    items: [
      { item: 'MenuItem', id: 'show', text: '显示' },
      { item: 'MenuItem', id: 'hide', text: '隐藏' },
      { item: 'Separator' },
      { item: 'MenuItem', id: 'quit', text: '退出' }
    ]
  });

  const tray = await newTrayIcon({
    id: 'main-tray',
    icon: 'icons/icon.png',
    tooltip: 'My App',
    menu,
    onClick: async (event: TrayIconEvent) => {
      if (event.button === 'Left') {
        const win = getCurrentWindow();
        await win.show();
        await win.setFocus();
      }
    }
  });

  return tray;
}
```
