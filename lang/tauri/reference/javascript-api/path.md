# path 命名空间

`path` 命名空间提供跨平台路径操作功能。

## 导入

```typescript
import { path } from '@tauri-apps/api';
```

## 函数

### appDataDir()

获取应用数据目录。

```typescript
async function appDataDir(): Promise<string>
```

**示例：**
```typescript
const dataDir = await path.appDataDir();
// Windows: C:\Users\<user>\AppData\Roaming\com.myapp.app
```

### appConfigDir()

获取应用配置目录。

```typescript
async function appConfigDir(): Promise<string>
```

### appLocalDataDir()

获取应用本地数据目录。

```typescript
async function appLocalDataDir(): Promise<string>
```

### appCacheDir()

获取应用缓存目录。

```typescript
async function appCacheDir(): Promise<string>
```

### appLogDir()

获取应用日志目录。

```typescript
async function appLogDir(): Promise<string>
```

### homeDir()

获取用户主目录。

```typescript
async function homeDir(): Promise<string>
```

**示例：**
```typescript
const home = await path.homeDir();
// Windows: C:\Users\<user>
// Linux/Mac: /home/<user>
```

### desktopDir()

获取桌面目录。

```typescript
async function desktopDir(): Promise<string>
```

### documentDir()

获取文档目录。

```typescript
async function documentDir(): Promise<string>
```

### downloadDir()

获取下载目录。

```typescript
async function downloadDir(): Promise<string>
```

### pictureDir()

获取图片目录。

```typescript
async function pictureDir(): Promise<string>
```

### videoDir()

获取视频目录。

```typescript
async function videoDir(): Promise<string>
```

### audioDir()

获取音频目录。

```typescript
async function audioDir(): Promise<string>
```

### resourceDir()

获取资源目录（应用内置资源）。

```typescript
async function resourceDir(): Promise<string>
```

### tempDir()

获取临时目录。

```typescript
async function tempDir(): Promise<string>
```

### join(...paths: string[]): Promise<string>

拼接路径。

```typescript
const fullPath = await path.join(await path.homeDir(), 'documents', 'file.txt');
```

### normalize(path: string): Promise<string>

标准化路径。

```typescript
const normalized = await path.normalize('./foo/bar/../baz');
```

### resolve(path: string): Promise<string>

解析为绝对路径。

```typescript
const absolute = await path.resolve('relative/path');
```

### isAbsolute(path: string): Promise<boolean>

判断是否为绝对路径。

```typescript
const isAbs = await path.isAbsolute('/home/user/file');
```
