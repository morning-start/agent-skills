# 类型别名文档

本文档详细说明 WXT 的核心类型别名，包括类型用途、定义说明和使用示例。

## 官方导航链接

- [ContentScriptDefinition](https://wxt.dev/api/reference/wxt/type-aliases/ContentScriptDefinition.html) - 内容脚本定义
- [Entrypoint](https://wxt.dev/api/reference/wxt/type-aliases/Entrypoint.html) - 扩展入口类型
- [EntrypointGroup](https://wxt.dev/api/reference/wxt/type-aliases/EntrypointGroup.html) - 入口组类型
- [UserConfig](https://wxt.dev/api/reference/wxt/type-aliases/UserConfig.html) - 用户配置类型
- [UserManifest](https://wxt.dev/api/reference/wxt/type-aliases/UserManifest.html) - 用户清单类型
- [TargetBrowser](https://wxt.dev/api/reference/wxt/type-aliases/TargetBrowser.html) - 目标浏览器类型
- [TargetManifestVersion](https://wxt.dev/api/reference/wxt/type-aliases/TargetManifestVersion.html) - 目标清单版本类型
- [WxtPlugin](https://wxt.dev/api/reference/wxt/type-aliases/WxtPlugin.html) - WXT 插件类型

---

## 一、配置类型

### 1.1 UserConfig

用户配置的类型别名，定义用户可自定义的项目配置结构类型。

```typescript
type UserConfig = {
  root?: string;
  srcDir?: string;
  publicDir?: string;
  outDir?: string;
  entrypointsDir?: string;
  mode?: 'development' | 'production';
  browser?: TargetBrowser;
  manifest?: UserManifest | UserManifestFn;
  modules?: WxtModuleOptions[];
  hooks?: WxtHooks;
  vite?: InlineConfig;
  build?: WxtBuildConfig;
  dev?: WxtDevConfig;
};
```

**使用示例：**

```typescript
import { defineConfig } from 'wxt';

const config: UserConfig = {
  root: process.cwd(),
  mode: 'production',
  browser: 'chrome',
};

export default defineConfig(config);
```

### 1.2 UserManifest

用户清单的类型别名，定义用户可自定义的扩展清单文件结构类型。

```typescript
type UserManifest = {
  name: string;
  version: string;
  manifest_version?: 2 | 3;
  description?: string;
  permissions?: string[];
  host_permissions?: string[];
  icons?: Record<string, string>;
  action?: {
    default_icon?: Record<string, string>;
    default_popup?: string;
  };
  background?: {
    service_worker?: string;
    scripts?: string[];
  };
  content_scripts?: Array<{
    matches: string[];
    js?: string[];
    css?: string[];
  }>;
  // ... 其他 manifest 字段
};
```

**使用示例：**

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: 'My Extension',
    version: '1.0.0',
    description: 'A sample extension',
    manifest_version: 3,
    permissions: ['storage', 'tabs'],
    icons: {
      16: '/icons/icon-16.png',
      48: '/icons/icon-48.png',
      128: '/icons/icon-128.png',
    },
  },
});
```

### 1.3 UserManifestFn

用户清单函数的类型别名，定义返回用户清单配置的函数结构类型。

```typescript
type UserManifestFn = (env: ConfigEnv) => UserManifest;
```

**使用示例：**

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: (env) => ({
    name: 'My Extension',
    version: '1.0.0',
    // 根据环境配置不同内容
    description: env.mode === 'production'
      ? 'Production extension'
      : 'Development extension',
  }),
});
```

---

## 二、入口点类型

### 2.1 Entrypoint

扩展入口的类型别名，涵盖所有类型的入口接口，提供统一的类型引用方式。

```typescript
type Entrypoint =
  | BackgroundEntrypoint
  | ContentScriptEntrypoint
  | PopupEntrypoint
  | OptionsEntrypoint
  | DevtoolsEntrypoint
  | SidepanelEntrypoint;
```

### 2.2 EntrypointGroup

入口组的类型别名，定义一组相关入口的集合类型，便于批量管理多个入口。

```typescript
type EntrypointGroup = {
  name: string;
  entrypoints: EntrypointInfo[];
};
```

**使用示例：**

```typescript
// 获取所有内容脚本入口
const contentScripts: Entrypoint[] = entrypoints.filter(
  (e) => e.type === 'content-script'
);
```

### 2.3 ContentScriptDefinition

内容脚本定义的类型别名，整合内容脚本的各类配置结构，简化类型引用。

```typescript
type ContentScriptDefinition =
  | IsolatedWorldContentScriptDefinition
  | MainWorldContentScriptDefinition;
```

---

## 三、浏览器类型

### 3.1 TargetBrowser

目标浏览器的类型别名，定义支持的浏览器枚举类型，用于指定扩展适配的浏览器。

```typescript
type TargetBrowser =
  | 'chrome'
  | 'firefox'
  | 'edge'
  | 'safari'
  | 'opera'
  | 'brave';
```

**使用示例：**

```typescript
import { defineConfig } from 'wxt';

const browser: TargetBrowser = 'chrome';

export default defineConfig({
  browser,
});
```

### 3.2 PerBrowserOption

按浏览器配置的选项类型别名，定义支持多浏览器差异化配置的选项类型。

```typescript
type PerBrowserOption<T> = T | {
  [K in TargetBrowser]?: T;
};
```

**使用示例：**

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    // Chrome 特定配置
    chrome: {
      permissions: ['sidePanel'],
    },
    // Firefox 特定配置
    firefox: {
      permissions: ['menus'],
    },
  },
});
```

### 3.3 ResolvedPerBrowserOptions

解析后的按浏览器配置选项类型别名，定义多浏览器差异化配置解析后的最终类型。

```typescript
type ResolvedPerBrowserOption<T> = {
  [K in TargetBrowser]: T;
};
```

---

## 四、清单版本类型

### 4.1 TargetManifestVersion

目标清单版本的类型别名，定义扩展清单文件支持的版本枚举类型。

```typescript
type TargetManifestVersion = 2 | 3;
```

**使用示例：**

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    manifest_version: 3,
  },
});
```

---

## 五、构建类型

### 5.1 HookResult

钩子函数返回值的类型别名，定义钩子函数执行后的返回结果类型。

```typescript
type HookResult = void | Promise<void> | any;
```

### 5.2 OutputFile

输出文件的类型别名，涵盖输出资源与代码块的统一类型，简化文件操作的类型引用。

```typescript
type OutputFile = OutputAsset | OutputChunk;
```

**使用示例：**

```typescript
hooks: {
  'build:done': async (ctx) => {
    const files: OutputFile[] = [
      ...ctx.output.assets,
      ...ctx.output.chunks,
    ];

    files.forEach((file) => {
      console.log(`${file.fileName}: ${file.size} bytes`);
    });
  },
}
```

### 5.3 WxtCommand

WXT 命令的类型别名，定义 WXT 支持的 CLI 命令枚举类型。

```typescript
type WxtCommand =
  | 'build'
  | 'dev'
  | 'zip'
  | 'prepare'
  | 'clean'
  | 'init'
  | 'submit';
```

---

## 六、模块类型

### 6.1 WxtModuleOptions

WXT 模块配置的类型别名，定义模块注册时的配置参数类型。

```typescript
type WxtModuleOptions = string | WxtModule | (() => Promise<WxtModule>);
```

**使用示例：**

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  modules: [
    // 字符串：自动加载
    '@wxt-dev/module-example',

    // 直接引用模块
    myCustomModule,

    // 异步加载
    () => import('./my-module'),
  ],
});
```

### 6.2 WxtModuleSetup

WXT 模块初始化的类型别名，定义模块初始化函数的结构类型。

```typescript
type WxtModuleSetup = (wxt: Wxt) => void | Promise<void>;
```

**使用示例：**

```typescript
const myModule = {
  name: 'my-module',
  setup: (wxt: Wxt) => {
    wxt.logger.info('Module initialized');
  },
};
```

### 6.3 WxtPlugin

WXT 插件的类型别名，定义插件的结构、钩子函数等核心属性类型。

```typescript
type WxtPlugin = {
  name: string;
  config?: (env: ConfigEnv) => InlineConfig;
  hooks?: WxtHooks;
};
```

**使用示例：**

```typescript
const myPlugin: WxtPlugin = {
  name: 'my-plugin',
  hooks: {
    'prepare:build': async (ctx) => {
      console.log('Custom hook from plugin');
    },
  },
};

export default defineConfig({
  plugins: [myPlugin],
});
```

---

## 七、目录类型

### 7.1 WxtDirEntry

WXT 目录条目的类型别名，涵盖目录下文件与类型引用条目的统一类型。

```typescript
type WxtDirEntry = WxtDirFileEntry | WxtDirTypeReferenceEntry;
```

### 7.2 WxtDirFileEntry

定义 WXT 目录下文件条目的接口，描述文件的路径、名称、类型、属性等相关信息。

```typescript
interface WxtDirFileEntry {
  name: string;
  path: string;
  type: 'file';
  content?: string;
}
```

### 7.3 WxtDirTypeReferenceEntry

定义 WXT 目录下类型引用条目的接口，描述类型引用的路径、关联类型、引用规则等。

```typescript
interface WxtDirTypeReferenceEntry {
  name: string;
  path: string;
  type: 'type-reference';
  target: string;
}
```

---

## 八、公共文件类型

### 8.1 ResolvedPublicFile

解析后的公共文件类型别名，整合解析后的公共文件各类属性，简化类型引用。

```typescript
type ResolvedPublicFile = ResolvedBasePublicFile | CopiedPublicFile | GeneratedPublicFile;
```

### 8.2 CopiedPublicFile

定义公共文件复制后的相关信息，包含源路径、目标路径、复制状态及文件属性等。

```typescript
interface CopiedPublicFile {
  type: 'copied';
  src: string;
  dest: string;
}
```

### 8.3 GeneratedPublicFile

定义自动生成的公共文件相关信息，包含文件内容、生成规则、输出路径及文件属性等。

```typescript
interface GeneratedPublicFile {
  type: 'generated';
  fileName: string;
  content: string;
}
```

---

## 九、其他类型

### 9.1 ExtensionRunnerConfig

扩展运行器配置的类型别名，整合运行器的各类配置参数，简化配置类型引用。

```typescript
type ExtensionRunnerConfig = {
  browser: TargetBrowser;
  port?: number;
  open?: boolean;
};
```

### 9.2 EslintGlobalsPropValue

ESLint 全局变量属性值的类型别名，定义全局变量的校验规则类型。

```typescript
type EslintGlobalsPropValue = boolean | 'readonly' | 'writable' | 'off';
```

### 9.3 OnContentScriptStopped

内容脚本停止回调函数的类型别名，定义脚本停止后触发的回调函数结构。

```typescript
type OnContentScriptStopped = (error?: Error) => void;
```

### 9.4 ReloadContentScriptPayload

定义重新加载内容脚本的请求参数结构，包含脚本标识、加载选项等相关信息。

```typescript
interface ReloadContentScriptPayload {
  entrypoint: string;
  options?: any;
}
```

---

## 十、完整示例

### 10.1 使用多个类型

```typescript
// types.ts
import type {
  UserConfig,
  TargetBrowser,
  UserManifest,
  Entrypoint,
  OutputFile,
} from 'wxt';

// 配置类型
const config: UserConfig = {
  browser: 'chrome',
  mode: 'production',
};

// 浏览器类型
const browser: TargetBrowser = 'chrome';

// 清单类型
const manifest: UserManifest = {
  name: 'My Extension',
  version: '1.0.0',
};

// 入口点类型
const entrypoint: Entrypoint = {
  type: 'background',
  name: 'background',
  // ...
};

// 输出文件类型
const file: OutputFile = {
  name: 'background.js',
  fileName: 'background.js',
  size: 1024,
  type: 'asset',
};
```

### 10.2 类型守卫

```typescript
// guards.ts
import type { Entrypoint } from 'wxt';

function isBackgroundEntrypoint(entry: Entrypoint): entry is BackgroundEntrypoint {
  return entry.type === 'background';
}

function isContentScriptEntrypoint(entry: Entrypoint): entry is ContentScriptEntrypoint {
  return entry.type === 'content-script';
}

// 使用示例
entrypoints.forEach((entry) => {
  if (isBackgroundEntrypoint(entry)) {
    console.log('Background script:', entry.name);
  } else if (isContentScriptEntrypoint(entry)) {
    console.log('Content script:', entry.name);
  }
});
```

### 10.3 泛型工具函数

```typescript
// utils.ts
import type { PerBrowserOption, TargetBrowser } from 'wxt';

function getBrowserOption<T>(
  options: PerBrowserOption<T>,
  browser: TargetBrowser
): T {
  if (typeof options === 'object' && !Array.isArray(options)) {
    return options[browser] ?? Object.values(options)[0];
  }
  return options;
}

// 使用示例
const browserOptions: PerBrowserOption<string> = {
  chrome: 'chrome-specific',
  firefox: 'firefox-specific',
};

const currentBrowser: TargetBrowser = 'chrome';
const value = getBrowserOption(browserOptions, currentBrowser);
console.log(value); // 'chrome-specific'
```

### 10.4 类型推断

```typescript
// inference.ts
import type { UserConfig, UserManifestFn } from 'wxt';

// 类型推断
function defineMyConfig(config: UserConfig) {
  return config;
}

// 自动推断 manifest 函数类型
const config = defineMyConfig({
  manifest: (env) => ({
    name: 'My Extension',
    // env 的类型自动推断为 ConfigEnv
    mode: env.mode,
  }),
});

export default config;
```
