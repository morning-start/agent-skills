# image 命名空间

`image` 命名空间提供图像处理功能，用于加载、操作和转换图像数据。

## 导入

```typescript
import { image } from '@tauri-apps/api';
```

## 函数

### fromUrl(url: string): Promise<Image>

从 URL 加载图像。

```typescript
async function fromUrl(url: string): Promise<Image>
```

**示例：**
```typescript
import { fromUrl } from '@tauri-apps/api/image';

const img = await fromUrl('https://example.com/logo.png');
console.log(img.width, img.height);
```

### fromPath(path: string): Promise<Image>

从文件路径加载图像。

```typescript
async function fromPath(path: string): Promise<Image>
```

**示例：**
```typescript
import { fromPath } from '@tauri-apps/api/image';

const img = await fromPath('/path/to/image.png');
```

### fromBytes(bytes: number[] | Uint8Array): Promise<Image>

从字节数组创建图像。

```typescript
async function fromBytes(bytes: number[] | Uint8Array): Promise<Image>
```

**示例：**
```typescript
const bytes = await fetch('image.png').then(r => r.arrayBuffer());
const img = await fromBytes(new Uint8Array(bytes));
```

### toBase64(image: Image, format: string): Promise<string>

将图像转换为 Base64 字符串。

**参数：**
- `image`: Image 对象
- `format`: 图像格式 ('png', 'jpg', 'ico')

**示例：**
```typescript
import { toBase64 } from '@tauri-apps/api/image';

const base64 = await toBase64(img, 'png');
```

## Image 类

### 属性

```typescript
interface Image {
  width: number;
  height: number;
  rgba: Uint8Array;  // RGBA 像素数据
}
```

### 方法

```typescript
const img = await fromPath('icon.png');

console.log(img.width);   // 宽度
console.log(img.height);  // 高度
console.log(img.rgba);    // RGBA 像素数组
```

## 使用场景

### 应用图标

```typescript
import { app } from '@tauri-apps/api';

const icon = await app.getAppIcon();
```

### 动态图像

```typescript
import { fromBytes, toBase64 } from '@tauri-apps/api/image';

// 加载图像并转换
const img = await fromPath('assets/photo.jpg');
const base64 = await toBase64(img, 'jpg');

// 在 HTML 中使用
document.querySelector('img').src = `data:image/jpeg;base64,${base64}`;
```
