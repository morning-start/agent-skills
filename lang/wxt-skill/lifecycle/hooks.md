# 钩子函数详解

本文档详细说明 WXT 构建生命周期的所有钩子函数，包括参数、返回值和使用示例。

## 官方导航链接

- [Hooks](https://wxt.dev/guide/essentials/config/hooks.html) - 构建与运行时钩子函数完整指南

---

## 钩子概览

WXT 提供两类钩子：

| 类型 | 说明 | 钩子数量 |
|------|------|----------|
| 构建钩子 | 构建过程中的钩子 | 8 个 |
| 开发钩子 | 开发服务器钩子 | 4 个 |

## 一、构建钩子

### 1.1 prepare:build

**触发时机：** 构建准备阶段开始时

**参数：**

```typescript
interface PrepareContext {
  config: UserConfig;
  env: BuildEnv;
  version: string;
}

interface BuildEnv {
  command: 'build' | 'serve';
  mode: 'development' | 'production';
  browser?: BrowserType;
}
```

**返回值：** void | Promise\<void\>

**使用示例：**

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  hooks: {
    'prepare:build': async (ctx) => {
      console.log('开始构建');
      console.log('环境:', ctx.env);
      console.log('版本:', ctx.version);

      // 自定义准备逻辑
      await prepareBuildEnvironment();
    },
  },
});
```

**使用场景：**
- 验证构建环境
- 初始化工具链
- 设置环境变量
- 创建临时目录

---

### 1.2 resolve:entrypoints

**触发时机：** 解析入口点后

**参数：**

```typescript
interface ResolveContext {
  entrypoints: Entrypoint[];
  manifest: Manifest;
  config: ResolvedConfig;
}

interface Entrypoint {
  type: EntrypointType;
  name: string;
  input: string;
  output: string;
  options?: any;
}

type EntrypointType =
  | 'background'
  | 'content-script'
  | 'popup'
  | 'options'
  | 'devtools'
  | 'sidebar';
```

**返回值：** void | Promise\<void\>

**使用示例：**

```typescript
export default defineConfig({
  hooks: {
    'resolve:entrypoints': async (ctx) => {
      console.log('解析到的入口点:', ctx.entrypoints);

      // 可以添加、修改或删除入口点
      ctx.entrypoints.forEach(entry => {
        console.log(`入口点: ${entry.name} (${entry.type})`);
      });

      // 添加自定义入口点
      ctx.entrypoints.push({
        type: 'content-script',
        name: 'custom-content',
        input: './entrypoints/custom-content.ts',
        output: 'custom-content.js',
      });
    },
  },
});
```

**使用场景：**
- 动态添加入口点
- 修改入口点配置
- 过滤入口点
- 验证入口点配置

---

### 1.3 analyze:modules

**触发时机：** 分析模块依赖后

**参数：**

```typescript
interface AnalyzeContext {
  modules: ModuleInfo[];
  graph: DependencyGraph;
  config: ResolvedConfig;
}

interface ModuleInfo {
  id: string;
  importedIds: string[];
  importedBy: string[];
  isEntry: boolean;
  isExternal: boolean;
  size: number;
}

interface DependencyGraph {
  nodes: Map<string, ModuleInfo>;
  edges: Map<string, string[]>;
}
```

**返回值：** void | Promise\<void\>

**使用示例：**

```typescript
export default defineConfig({
  hooks: {
    'analyze:modules': async (ctx) => {
      console.log('分析到的模块数量:', ctx.modules.length);

      // 统计模块大小
      const totalSize = ctx.modules.reduce((sum, m) => sum + m.size, 0);
      console.log('总大小:', totalSize, 'bytes');

      // 查找最大的模块
      const largestModule = ctx.modules.reduce((max, m) =>
        m.size > max.size ? m : max
      );
      console.log('最大的模块:', largestModule.id);

      // 检测循环依赖
      const cycles = detectCycles(ctx.graph);
      if (cycles.length > 0) {
        console.warn('检测到循环依赖:', cycles);
      }
    },
  },
});
```

**使用场景：**
- 检测循环依赖
- 统计模块大小
- 分析模块依赖
- 优化打包策略

---

### 1.4 transform:code

**触发时机：** 转换代码时

**参数：**

```typescript
interface TransformContext {
  code: string;
  id: string;
  map: string | null;
  config: ResolvedConfig;
}
```

**返回值：** string | { code: string; map?: string } | null

**使用示例：**

```typescript
export default defineConfig({
  hooks: {
    'transform:code': async (ctx) => {
      console.log('转换代码:', ctx.id);

      // 替换环境变量
      let code = ctx.code;
      code = code.replace(
        /__API_URL__/g,
        process.env.API_URL || 'https://api.example.com'
      );

      // 添加版本号
      code = code.replace(
        /__VERSION__/g,
        process.env.npm_package_version || '1.0.0'
      );

      // 添加调试信息（开发模式）
      if (ctx.config.mode === 'development') {
        code = `console.log('[DEBUG] ${ctx.id} loaded');\n${code}`;
      }

      return code;
    },
  },
});
```

**使用场景：**
- 替换环境变量
- 注入调试代码
- 转换代码风格
- 添加元数据

---

### 1.5 build:module

**触发时机：** 构建模块时

**参数：**

```typescript
interface BuildContext {
  module: BuildModule;
  config: ResolvedConfig;
}

interface BuildModule {
  id: string;
  code: string;
  map: string | null;
  dependencies: string[];
}
```

**返回值：** void | Promise\<void\>

**使用示例：**

```typescript
export default defineConfig({
  hooks: {
    'build:module': async (ctx) => {
      console.log('构建模块:', ctx.module.id);
      console.log('依赖数量:', ctx.module.dependencies.length);

      // 可以添加、修改或删除模块代码
      if (ctx.module.id.includes('secret')) {
        console.warn('检测到敏感模块:', ctx.module.id);
      }

      // 记录构建时间
      const startTime = Date.now();
      // ... 构建逻辑
      const duration = Date.now() - startTime;
      console.log(`构建模块 ${ctx.module.id} 耗时 ${duration}ms`);
    },
  },
});
```

**使用场景：**
- 记录构建信息
- 验证模块代码
- 添加构建统计
- 自定义构建逻辑

---

### 1.6 generate:manifest

**触发时机：** 生成 manifest 后

**参数：**

```typescript
interface GenerateContext {
  manifest: Manifest;
  config: ResolvedConfig;
  browser: BrowserType;
}

type BrowserType = 'chrome' | 'firefox' | 'edge' | 'safari';

interface Manifest {
  name: string;
  version: string;
  description?: string;
  permissions?: string[];
  host_permissions?: string[];
  // ... 更多字段
}
```

**返回值：** void | Promise\<void\>

**使用示例：**

```typescript
export default defineConfig({
  hooks: {
    'generate:manifest': async (ctx) => {
      console.log('生成 manifest:', ctx.manifest.name);

      // 添加自定义字段
      ctx.manifest.custom_field = 'custom_value';

      // 根据浏览器添加特定配置
      if (ctx.browser === 'firefox') {
        ctx.manifest.browser_specific_settings = {
          gecko: {
            id: 'my-extension@example.com',
            strict_min_version: '102.0',
          },
        };
      }

      // 根据环境添加权限
      if (ctx.config.mode === 'development') {
        ctx.manifest.permissions?.push('debugger');
      }
    },
  },
});
```

**使用场景：**
- 添加自定义 manifest 字段
- 根据浏览器添加特定配置
- 根据环境修改权限
- 验证 manifest 配置

---

### 1.7 optimize:output

**触发时机：** 优化输出时

**参数：**

```typescript
interface OptimizeContext {
  output: OutputFile[];
  config: ResolvedConfig;
}

interface OutputFile {
  type: 'chunk' | 'asset';
  fileName: string;
  size: number;
  code?: string;
  source?: string;
}
```

**返回值：** void | Promise\<void\>

**使用示例：**

```typescript
export default defineConfig({
  hooks: {
    'optimize:output': async (ctx) => {
      console.log('优化输出文件数量:', ctx.output.length);

      // 统计总大小
      const totalSize = ctx.output.reduce((sum, f) => sum + f.size, 0);
      console.log('总大小:', totalSize, 'bytes');

      // 查找最大的文件
      const largestFile = ctx.output.reduce((max, f) =>
        f.size > max.size ? f : max
      );
      console.log('最大的文件:', largestFile.fileName);

      // 查找超过 100KB 的文件
      const largeFiles = ctx.output.filter(f => f.size > 100 * 1024);
      if (largeFiles.length > 0) {
        console.warn('大文件列表:', largeFiles.map(f => f.fileName));
      }
    },
  },
});
```

**使用场景：**
- 统计输出文件大小
- 查找大文件
- 优化输出策略
- 生成构建报告

---

### 1.8 build:done

**触发时机：** 构建完成时

**参数：**

```typescript
interface CompleteContext {
  outputDir: string;
  duration: number;
  config: ResolvedConfig;
}
```

**返回值：** void | Promise\<void\>

**使用示例：**

```typescript
import { writeFileSync, readFileSync } from 'fs';
import path from 'path';

export default defineConfig({
  hooks: {
    'build:done': async (ctx) => {
      console.log('构建完成!');
      console.log(`耗时: ${ctx.duration}ms`);
      console.log(`输出目录: ${ctx.outputDir}`);

      // 生成构建报告
      const report = {
        outputDir: ctx.outputDir,
        duration: ctx.duration,
        mode: ctx.config.mode,
        browser: ctx.config.browser,
        timestamp: new Date().toISOString(),
      };

      writeFileSync(
        path.join(ctx.outputDir, 'build-report.json'),
        JSON.stringify(report, null, 2)
      );

      // 读取并打印 manifest
      const manifestPath = path.join(ctx.outputDir, 'manifest.json');
      const manifest = JSON.parse(readFileSync(manifestPath, 'utf-8'));
      console.log('扩展名称:', manifest.name);
      console.log('扩展版本:', manifest.version);
    },
  },
});
```

**使用场景：**
- 生成构建报告
- 清理临时文件
- 执行后续操作
- 通知外部系统

---

## 二、开发钩子

### 2.1 dev:server:start

**触发时机：** 开发服务器启动时

**参数：**

```typescript
interface DevServerContext {
  server: DevServer;
  config: ResolvedConfig;
}

interface DevServer {
  port: number;
  host: string;
  url: string;
  restart(): Promise<void>;
  close(): Promise<void>;
}
```

**返回值：** void | Promise\<void\>

**使用示例：**

```typescript
export default defineConfig({
  hooks: {
    'dev:server:start': async (ctx) => {
      console.log('开发服务器已启动');
      console.log(`地址: ${ctx.server.url}`);
      console.log(`端口: ${ctx.server.port}`);

      // 自动打开浏览器（可选）
      // await open(ctx.server.url);

      // 通知外部系统
      await notifyServerStarted(ctx.server.url);
    },
  },
});
```

**使用场景：**
- 记录服务器信息
- 自动打开浏览器
- 通知外部系统
- 初始化开发工具

---

### 2.2 dev:server:restart

**触发时机：** 开发服务器重启时

**参数：** 同 `dev:server:start`

**返回值：** void | Promise\<void\>

**使用示例：**

```typescript
export default defineConfig({
  hooks: {
    'dev:server:restart': async (ctx) => {
      console.log('开发服务器已重启');
      console.log(`地址: ${ctx.server.url}`);
    },
  },
});
```

**使用场景：**
- 记录重启信息
- 重置开发状态
- 清理缓存
- 通知用户

---

### 2.3 dev:file:change

**触发时机：** 文件变化时

**参数：**

```typescript
interface FileChangeContext {
  file: string;
  event: 'create' | 'update' | 'delete';
  config: ResolvedConfig;
}
```

**返回值：** void | Promise\<void\>

**使用示例：**

```typescript
export default defineConfig({
  hooks: {
    'dev:file:change': async (ctx) => {
      console.log('文件变化:', ctx.file);
      console.log('事件类型:', ctx.event);

      // 根据文件类型执行不同操作
      if (ctx.file.endsWith('.ts')) {
        console.log('TypeScript 文件变化');
      } else if (ctx.file.endsWith('.svelte')) {
        console.log('Svelte 组件变化');
      } else if (ctx.file.endsWith('.css')) {
        console.log('样式文件变化');
      }

      // 通知外部系统
      await notifyFileChanged(ctx.file, ctx.event);
    },
  },
});
```

**使用场景：**
- 记录文件变化
- 执行特定操作
- 通知外部系统
- 自定义热重载逻辑

---

### 2.4 dev:server:close

**触发时机：** 开发服务器关闭时

**参数：** 同 `dev:server:start`

**返回值：** void | Promise\<void\>

**使用示例：**

```typescript
export default defineConfig({
  hooks: {
    'dev:server:close': async (ctx) => {
      console.log('开发服务器已关闭');

      // 清理临时文件
      await cleanupTempFiles();

      // 通知外部系统
      await notifyServerStopped(ctx.server.url);

      // 保存开发状态
      await saveDevState();
    },
  },
});
```

**使用场景：**
- 清理临时文件
- 保存开发状态
- 通知外部系统
- 释放资源

---

## 三、高级用法

### 3.1 组合多个钩子

```typescript
export default defineConfig({
  hooks: {
    'prepare:build': async (ctx) => {
      console.log('开始构建');
    },
    'resolve:entrypoints': async (ctx) => {
      console.log('解析入口点');
    },
    'build:done': async (ctx) => {
      console.log('构建完成');
    },
  },
});
```

### 3.2 条件执行钩子

```typescript
export default defineConfig({
  hooks: {
    'build:done': async (ctx) => {
      // 仅在生产环境执行
      if (ctx.config.mode === 'production') {
        console.log('生产环境构建完成');
        await uploadToCDN(ctx.outputDir);
      }

      // 仅在特定浏览器执行
      if (ctx.config.browser === 'chrome') {
        console.log('Chrome 构建完成');
        await notifyChromeStore();
      }
    },
  },
});
```

### 3.3 异步钩子

```typescript
export default defineConfig({
  hooks: {
    'build:done': async (ctx) => {
      // 并行执行多个异步操作
      await Promise.all([
        generateReport(ctx.outputDir),
        cleanupTempFiles(),
        notifyTeam(ctx.outputDir),
      ]);

      // 串行执行多个异步操作
      await step1();
      await step2();
      await step3();
    },
  },
});
```

### 3.4 错误处理

```typescript
export default defineConfig({
  hooks: {
    'build:done': async (ctx) => {
      try {
        await someAsyncOperation();
      } catch (error) {
        console.error('操作失败:', error);
        // 不要中断构建流程
        // 可以记录错误或通知用户
      }
    },
  },
});
```

## 常见问题

### Q1: 如何调试钩子？

**方法一：使用 console.log**

```typescript
export default defineConfig({
  hooks: {
    'build:done': async (ctx) => {
      console.log('构建完成钩子触发');
      console.log('上下文:', ctx);
    },
  },
});
```

**方法二：使用调试器**

```typescript
export default defineConfig({
  hooks: {
    'build:done': async (ctx) => {
      debugger; // 设置断点
      console.log('构建完成');
    },
  },
});
```

### Q2: 钩子执行顺序是什么？

**构建钩子执行顺序：**

1. `prepare:build`
2. `resolve:entrypoints`
3. `analyze:modules`
4. `transform:code`（每个模块一次）
5. `build:module`（每个模块一次）
6. `generate:manifest`
7. `optimize:output`
8. `build:done`

**开发钩子执行顺序：**

1. `dev:server:start`
2. `dev:file:change`（每次文件变化）
3. `dev:server:restart`（服务器重启）
4. `dev:server:close`

### Q3: 钩子会影响性能吗？

**性能影响：**

- 钩子会延长构建时间
- 建议钩子逻辑尽量简单
- 避免在钩子中执行耗时操作
- 可以使用缓存优化

**优化建议：**

```typescript
export default defineConfig({
  hooks: {
    'build:done': async (ctx) => {
      // 避免重复执行
      const cacheKey = ctx.outputDir;
      if (hasCache(cacheKey)) {
        return;
      }

      // 执行耗时操作
      await expensiveOperation();

      // 保存缓存
      saveCache(cacheKey);
    },
  },
});
```

### Q4: 如何在钩子之间共享数据？

**使用全局变量：**

```typescript
let sharedData: any;

export default defineConfig({
  hooks: {
    'prepare:build': async (ctx) => {
      sharedData = { startTime: Date.now() };
    },
    'build:done': async (ctx) => {
      const duration = Date.now() - sharedData.startTime;
      console.log('构建耗时:', duration);
    },
  },
});
```

### Q5: 如何禁用某个钩子？

**方法一：不注册钩子**

```typescript
export default defineConfig({
  hooks: {
    // 不注册需要禁用的钩子
  },
});
```

**方法二：使用条件判断**

```typescript
export default defineConfig({
  hooks: {
    'build:done': async (ctx) => {
      if (process.env.DISABLE_HOOK === 'true') {
        return;
      }

      console.log('构建完成');
    },
  },
});
```

## 下一步

- [构建阶段详解](./phases.md)：了解构建的 8 个阶段
- [完整流程图](./flow.md)：可视化的完整构建流程
- [命令参考](../cli/commands.md)：掌握开发和构建命令
- [入门指南](../guides/getting-started.md)：快速上手 WXT
