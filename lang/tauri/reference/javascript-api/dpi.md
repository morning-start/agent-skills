# dpi 命名空间

`dpi` 命名空间提供 DPI（每英寸点数）和缩放相关的功能。

## 导入

```typescript
import { dpi } from '@tauri-apps/api';
```

## 函数

### getCurrent()

获取当前显示器的 DPI 信息。

```typescript
async function getCurrent(): Promise<number>
```

**示例：**
```typescript
const currentDpi = await dpi.getCurrent();
console.log(currentDpi); // 96
```

### getScaleFactor()

获取当前窗口的缩放因子。

```typescript
async function getScaleFactor(): Promise<number>
```

**示例：**
```typescript
import { getCurrentWindow } from '@tauri-apps/api/window';

const win = getCurrentWindow();
const scaleFactor = await win.scaleFactor();
console.log(scaleFactor); // 1.5
```

### getDefault()

获取系统默认 DPI。

```typescript
async function getDefault(): Promise<number>
```

## 相关概念

### 物理像素 vs 逻辑像素

- **物理像素**：显示器的实际像素数量
- **逻辑像素**：CSS 和 JavaScript 中使用的像素单位

Tauri 自动处理物理像素和逻辑像素之间的转换。

### 缩放因子

常见的缩放因子：
- 1.0 = 100% (96 DPI)
- 1.25 = 125% (120 DPI)
- 1.5 = 150% (144 DPI)
- 2.0 = 200% (192 DPI)

### 在 CSS 中使用

```css
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  /* High DPI 屏幕样式 */
}
```
