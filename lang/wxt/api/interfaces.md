# 核心接口文档

本文档详细说明 WXT 的核心接口定义，包括接口用途、属性说明和使用示例。

## 官方导航链接

- [BackgroundDefinition](https://wxt.dev/api/reference/wxt/interfaces/BackgroundDefinition.html) - 后台脚本定义
- [BackgroundEntrypoint](https://wxt.dev/api/reference/wxt/interfaces/BackgroundEntrypoint.html) - 后台脚本入口
- [ContentScriptEntrypoint](https://wxt.dev/api/reference/wxt/interfaces/ContentScriptEntrypoint.html) - 内容脚本入口
- [PopupEntrypoint](https://wxt.dev/api/reference/wxt/interfaces/PopupEntrypoint.html) - 弹出页面入口
- [OptionsEntrypoint](https://wxt.dev/api/reference/wxt/interfaces/OptionsEntrypoint.html) - 选项页面入口
- [Wxt](https://wxt.dev/api/reference/wxt/interfaces/Wxt.html) - WXT 核心接口
- [WxtBuilder](https://wxt.dev/api/reference/wxt/interfaces/WxtBuilder.html) - WXT 构建器
- [WxtDevServer](https://wxt.dev/api/reference/wxt/interfaces/WxtDevServer.html) - WXT 开发服务器

---

## 一、入口点接口

### 1.1 BackgroundDefinition

后台脚本定义接口，描述后台脚本的基础结构、运行规则及关联配置。

```typescript
interface BackgroundDefinition {
  main: () => void | Promise<void>;
  type?: 'module';
}
```

**使用示例：**

```typescript
import { defineBackground } from 'wxt/sandbox';

export default defineBackground(() => {
  console.log('Background script started');

  browser.runtime.onInstalled.addListener(() => {
    console.log('Extension installed');
  });
});
```

### 1.2 BackgroundEntrypoint

后台脚本入口接口，描述后台脚本的入口信息、执行上下文及关联依赖说明。

```typescript
interface BackgroundEntrypoint extends BaseEntrypoint {
  type: 'background';
  options: BackgroundEntrypointOptions;
  content?: string;
}
```

### 1.3 ContentScriptEntrypoint

内容脚本入口接口，描述内容脚本的入口结构、执行上下文及与页面的交互规则。

```typescript
interface ContentScriptEntrypoint extends BaseEntrypoint {
  type: 'content-script';
  options: ContentScriptEntrypointOptions;
  content?: string;
  css?: string[];
}
```

**使用示例：**

```typescript
import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],
  main() {
    console.log('Content script loaded');
  },
});
```

### 1.4 PopupEntrypoint

扩展弹窗页面入口接口，定义弹窗的结构、加载规则、显示逻辑及与扩展核心的交互方式。

```typescript
interface PopupEntrypoint extends BaseEntrypoint {
  type: 'popup';
  options: PopupEntrypointOptions;
  content?: string;
}
```

**使用示例：**

```typescript
// entrypoints/popup.html
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
</head>
<body>
  <div id="app"></div>
  <script type="module" src="./main.ts"></script>
</body>
</html>
```

### 1.5 OptionsEntrypoint

扩展选项页面入口接口，定义选项页面的结构、加载规则及与扩展核心的交互方式。

```typescript
interface OptionsEntrypoint extends BaseEntrypoint {
  type: 'options';
  options: OptionsEntrypointOptions;
  content?: string;
}
```

### 1.6 BaseEntrypoint

所有扩展入口的基础接口，定义入口的通用属性、生命周期方法及基础运行规则。

```typescript
interface BaseEntrypoint {
  type: string;
  name: string;
  inputPath: string;
  outputPath: string;
  options: BaseEntrypointOptions;
}
```

---

## 二、配置接口

### 2.1 UserConfig

用户配置接口，定义用户可自定义的项目配置结构类型。

```typescript
interface UserConfig {
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
}
```

**使用示例：**

```typescript
// wxt.config.ts
import { defineConfig } from 'wxt';

export default defineConfig({
  root: process.cwd(),
  srcDir: 'src',
  publicDir: 'public',
  outDir: '.output',
  entrypointsDir: 'entrypoints',

  mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
  browser: 'chrome',

  manifest: {
    name: 'My Extension',
    version: '1.0.0',
  },

  modules: [],

  hooks: {
    'build:done': () => {
      console.log('Build complete');
    },
  },
});
```

### 2.2 InlineConfig

内联配置接口，定义可直接嵌入代码中的配置结构，支持临时覆盖默认配置。

```typescript
interface InlineConfig {
  config?: UserConfig;
  env?: Record<string, string>;
}
```

### 2.3 ResolvedConfig

解析后的项目完整配置，包含合并默认配置与用户配置后的所有参数信息。

```typescript
interface ResolvedConfig extends UserConfig {
  root: string;
  srcDir: string;
  publicDir: string;
  outDir: string;
  entrypointsDir: string;
  mode: 'development' | 'production';
  browser: TargetBrowser;
  manifest: ResolvedManifest;
  modules: WxtModule[];
  hooks: WxtHooks;
  vite: ResolvedViteConfig;
}
```

---

## 三、构建接口

### 3.1 BuildOutput

定义项目构建输出的相关信息，包含构建产物路径、产物类型、构建状态及错误信息等。

```typescript
interface BuildOutput {
  manifest: string;
  public: ResolvedPublicFile[];
  background?: string;
  contentScripts: string[];
  popup?: string;
  options?: string;
  assets: OutputAsset[];
  chunks: OutputChunk[];
}
```

### 3.2 BuildStepOutput

定义构建流程中单个步骤的输出信息，包含步骤执行结果、产物、日志及错误详情。

```typescript
interface BuildStepOutput {
  step: string;
  status: 'pending' | 'running' | 'success' | 'failed';
  output?: any;
  logs: string[];
  errors: Error[];
}
```

### 3.3 WxtBuilder

WXT 构建器接口，定义项目构建的相关方法，负责执行构建流程、生成构建产物。

```typescript
interface WxtBuilder {
  build(): Promise<BuildOutput>;
  watch(): Promise<() => Promise<void>>;
  clean(): Promise<void>;
}
```

### 3.4 WxtBuilderServer

WXT 构建服务器接口，整合构建功能与开发服务器，支持边构建边调试的开发模式。

```typescript
interface WxtBuilderServer extends WxtBuilder {
  startServer(): Promise<ServerInfo>;
  stopServer(): Promise<void>;
}
```

---

## 四、开发服务器接口

### 4.1 WxtDevServer

WXT 开发服务器接口，定义开发环境下的服务器启动、热更新、调试等相关功能。

```typescript
interface WxtDevServer {
  start(): Promise<ServerInfo>;
  stop(): Promise<void>;
  reload(): Promise<void>;
  getServer(): ServerInfo;
}
```

**使用示例：**

```typescript
import { createWxtDevServer } from 'wxt/server';

const server = await createWxtDevServer({
  browser: 'chrome',
  mode: 'development',
});

await server.start();

// 停止服务器
await server.stop();
```

### 4.2 ServerInfo

定义开发服务器的相关信息，包含服务器地址、端口、运行状态、配置参数等。

```typescript
interface ServerInfo {
  url: string;
  port: number;
  hostname: string;
  status: 'running' | 'stopped' | 'error';
  browser?: TargetBrowser;
}
```

---

## 五、核心接口

### 5.1 Wxt

WXT 核心接口，定义 WXT 框架的核心属性、方法，统筹项目构建、运行、调试等全流程。

```typescript
interface Wxt {
  config: ResolvedConfig;
  builder: WxtBuilder;
  devServer: WxtDevServer;
  packageManager: WxtPackageManager;
  logger: Logger;
  fsCache: FsCache;
}
```

### 5.2 WxtHooks

定义 WXT 的钩子函数接口，包含构建、运行、打包等全流程的钩子，支持自定义扩展流程。

```typescript
interface WxtHooks {
  'prepare:build'?: (ctx: PrepareContext) => HookResult;
  'resolve:entrypoints'?: (ctx: ResolveContext) => HookResult;
  'analyze:modules'?: (ctx: AnalyzeContext) => HookResult;
  'transform:code'?: (ctx: TransformContext) => HookResult;
  'build:module'?: (ctx: BuildModuleContext) => HookResult;
  'generate:manifest'?: (ctx: GenerateContext) => HookResult;
  'optimize:output'?: (ctx: OptimizeContext) => HookResult;
  'build:done'?: (ctx: DoneContext) => HookResult;
}
```

**使用示例：**

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  hooks: {
    'prepare:build': async (ctx) => {
      console.log('Build preparing...');
    },
    'build:done': async (ctx) => {
      console.log('Build complete!');
    },
  },
});
```

### 5.3 WxtModule

WXT 模块接口，定义模块的结构、注册方法、生命周期及与核心框架的交互规则。

```typescript
interface WxtModule {
  name: string;
  setup: WxtModuleSetup;
  version?: string;
}
```

**使用示例：**

```typescript
// my-wxt-module.ts
export default {
  name: 'my-wxt-module',
  version: '1.0.0',
  setup(wxt) {
    // 模块初始化逻辑
    console.log('Module loaded:', this.name);
  },
};
```

---

## 六、输出接口

### 6.1 OutputAsset

定义构建输出资源文件的相关信息，包含资源路径、大小、哈希值、类型等属性。

```typescript
interface OutputAsset {
  name: string;
  fileName: string;
  size: number;
  source?: string;
  type: 'asset' | 'public';
}
```

### 6.2 OutputChunk

定义构建输出代码块的相关信息，包含代码块路径、依赖、哈希值、打包规则等属性。

```typescript
interface OutputChunk {
  name: string;
  fileName: string;
  size: number;
  modules: Record<string, OutputModule>;
  importedAssets: OutputAsset[];
  importedFiles: string[];
  isEntry?: boolean;
  isDynamicEntry?: boolean;
  facadeModuleId?: string;
}
```

### 6.3 OutputFile

输出文件的类型别名，涵盖输出资源与代码块的统一类型。

```typescript
type OutputFile = OutputAsset | OutputChunk;
```

---

## 七、工具接口

### 7.1 Logger

日志工具接口，定义日志的打印、级别控制、格式配置等相关方法与属性。

```typescript
interface Logger {
  debug(message: string, ...args: any[]): void;
  info(message: string, ...args: any[]): void;
  warn(message: string, ...args: any[]): void;
  error(message: string, ...args: any[]): void;
  success(message: string, ...args: any[]): void;
}
```

**使用示例：**

```typescript
import { logger } from 'wxt';

logger.info('Extension started');
logger.warn('Warning message');
logger.error('Error occurred');
```

### 7.2 FsCache

文件系统缓存接口，定义缓存的创建、读取、更新、删除等操作方法及缓存规则。

```typescript
interface FsCache {
  get(key: string): Promise<any>;
  set(key: string, value: any): Promise<void>;
  delete(key: string): Promise<void>;
  clear(): Promise<void>;
  has(key: string): Promise<boolean>;
}
```

### 7.3 WxtPackageManager

WXT 包管理器接口，定义依赖包的安装、更新、卸载、检测等相关操作方法。

```typescript
interface WxtPackageManager {
  name: string;
  version: string;
  install(deps: string[]): Promise<void>;
  uninstall(deps: string[]): Promise<void>;
  update(deps: string[]): Promise<void>;
  list(): Promise<Dependency[]>;
}
```

---

## 八、类型引用接口

### 8.1 EntrypointInfo

描述扩展入口的详细信息，包含入口类型、配置、依赖及运行状态等汇总信息。

```typescript
interface EntrypointInfo {
  name: string;
  type: string;
  inputPath: string;
  outputPath: string;
  options: any;
  dependencies: Dependency[];
}
```

### 8.2 Dependency

定义项目依赖的相关信息，包含依赖名称、版本、路径、类型及加载规则等。

```typescript
interface Dependency {
  name: string;
  version: string;
  path: string;
  type: 'prod' | 'dev' | 'peer';
}
```

### 8.3 TargetBrowser

目标浏览器的类型定义，定义支持的浏览器枚举类型，用于指定扩展适配的浏览器。

```typescript
type TargetBrowser =
  | 'chrome'
  | 'firefox'
  | 'edge'
  | 'safari'
  | 'opera'
  | 'brave';
```

---

## 九、完整示例

### 9.1 使用多个接口

```typescript
// wxt.config.ts
import { defineConfig } from 'wxt';

export default defineConfig({
  // UserConfig
  root: process.cwd(),
  mode: 'production',
  browser: 'chrome',

  // Hooks
  hooks: {
    'prepare:build': async (ctx) => {
      ctx.logger.info('Build preparing...');
    },

    'build:done': async (ctx) => {
      ctx.logger.success('Build complete!');

      // 处理构建输出
      const output = ctx.output;
      ctx.logger.info(`Assets: ${output.assets.length}`);
      ctx.logger.info(`Chunks: ${output.chunks.length}`);
    },
  },
});
```

### 9.2 自定义模块

```typescript
// modules/my-module.ts
import type { WxtModule } from 'wxt';

const myModule: WxtModule = {
  name: 'my-custom-module',
  version: '1.0.0',

  setup(wxt) {
    // 使用 Wxt 接口
    wxt.logger.info('Module loaded');

    // 添加钩子
    wxt.config.hooks['prepare:build'] = async (ctx) => {
      ctx.logger.info('Custom prepare hook');
    };
  },
};

export default myModule;
```

### 9.3 使用开发服务器

```typescript
// server.ts
import { createWxtDevServer } from 'wxt/server';

async function startDevServer() {
  const server = await createWxtDevServer({
    browser: 'chrome',
    mode: 'development',
  });

  const info = await server.start();
  console.log(`Server running at ${info.url}`);

  // 监听退出信号
  process.on('SIGINT', async () => {
    await server.stop();
    process.exit(0);
  });
}

startDevServer();
```
