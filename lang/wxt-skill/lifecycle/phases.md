# 构建阶段详解

WXT 构建过程分为 8 个阶段，每个阶段都有特定的任务和目的。本文档详细说明每个阶段的工作和可用的钩子。

## 官方导航链接

- [Hooks](https://wxt.dev/guide/essentials/config/hooks.html) - 构建与运行时钩子函数
- [Vite](https://wxt.dev/guide/essentials/config/vite.html) - Vite 构建工具集成
- [Build Mode](https://wxt.dev/guide/essentials/config/build-mode.html) - 构建模式配置

---

## 构建阶段概览

| 阶段 | 名称 | 说明 |
|------|------|------|
| 1 | 准备阶段 | 初始化构建环境 |
| 2 | 解析阶段 | 解析项目配置和入口点 |
| 3 | 分析阶段 | 分析依赖和模块 |
| 4 | 转换阶段 | 转换代码和资源 |
| 5 | 构建阶段 | 构建模块和打包 |
| 6 | 生成阶段 | 生成 manifest 和资源 |
| 7 | 优化阶段 | 优化输出和压缩 |
| 8 | 完成阶段 | 清理和完成构建 |

## 一、准备阶段（Phase 1: Prepare）

### 阶段目标

初始化构建环境，准备必要的配置和工具。

### 执行内容

1. 加载 `wxt.config.ts` 配置文件
2. 初始化构建工具链（Vite、Rollup 等）
3. 验证 Node.js 和 Bun 版本
4. 检查项目依赖
5. 初始化工作目录

### 可用钩子

```typescript
// wxt.config.ts
import { defineConfig } from 'wxt';

export default defineConfig({
  hooks: {
    'prepare:build': async (ctx) => {
      console.log('构建准备开始');
      // 执行自定义逻辑
    },
  },
});
```

### 钩子参数

```typescript
interface PrepareContext {
  config: UserConfig;
  env: BuildEnv;
  version: string;
}
```

## 二、解析阶段（Phase 2: Resolve）

### 阶段目标

解析项目配置和入口点，确定需要构建的内容。

### 执行内容

1. 扫描 `entrypoints/` 目录
2. 解析入口点文件（background.ts、content.ts、popup.html 等）
3. 解析 `manifest.json` 配置
4. 解析 TypeScript 配置
5. 解析框架配置（Vue、React、Svelte、Solid）

### 可用钩子

```typescript
export default defineConfig({
  hooks: {
    'resolve:entrypoints': async (ctx) => {
      console.log('解析入口点');
      console.log(ctx.entrypoints);
      // 可以添加、修改或删除入口点
    },
  },
});
```

### 钩子参数

```typescript
interface ResolveContext {
  entrypoints: Entrypoint[];
  manifest: Manifest;
  config: ResolvedConfig;
}

interface Entrypoint {
  type: string; // 'background' | 'content' | 'popup' | 'options' 等
  name: string;
  input: string;
  output: string;
}
```

## 三、分析阶段（Phase 3: Analyze）

### 阶段目标

分析代码依赖，构建依赖树。

### 执行内容

1. 分析入口点的 import 语句
2. 构建模块依赖图
3. 检测循环依赖
4. 分析 TypeScript 类型
5. 分析框架组件（Vue SFC、Svelte 组件等）

### 可用钩子

```typescript
export default defineConfig({
  hooks: {
    'analyze:modules': async (ctx) => {
      console.log('分析模块依赖');
      console.log(ctx.modules);
      // 可以添加、修改或删除模块
    },
  },
});
```

### 钩子参数

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
}
```

## 四、转换阶段（Phase 4: Transform）

### 阶段目标

转换代码和资源，使其符合构建目标。

### 执行内容

1. 转换 TypeScript 代码到 JavaScript
2. 转换框架组件（Vue SFC → JS，Svelte → JS 等）
3. 转换 CSS 和样式文件
4. 处理静态资源（图片、字体等）
5. 应用代码分割

### 可用钩子

```typescript
export default defineConfig({
  hooks: {
    'transform:code': async (ctx) => {
      console.log('转换代码');
      console.log(ctx.code);
      // 可以添加、修改或删除代码
    },
  },
});
```

### 钩子参数

```typescript
interface TransformContext {
  code: string;
  id: string;
  map: string | null;
  config: ResolvedConfig;
}
```

## 五、构建阶段（Phase 5: Build）

### 阶段目标

构建模块并打包输出。

### 执行内容

1. 使用 Rollup 打包模块
2. 生成 chunks
3. 应用代码分割策略
4. 生成 sourcemap（如果启用）
5. 优化模块加载顺序

### 可用钩子

```typescript
export default defineConfig({
  hooks: {
    'build:module': async (ctx) => {
      console.log('构建模块');
      console.log(ctx.module);
      // 可以添加、修改或删除模块
    },
  },
});
```

### 钩子参数

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

## 六、生成阶段（Phase 6: Generate）

### 阶段目标

生成 manifest 和资源文件。

### 执行内容

1. 生成 `manifest.json` 文件
2. 复制公共资源（icons、_locales 等）
3. 生成 HTML 文件（popup.html、options.html 等）
4. 生成浏览器特定配置（Firefox 的 `browser_specific_settings` 等）
5. 生成类型定义文件（如果启用）

### 可用钩子

```typescript
export default defineConfig({
  hooks: {
    'generate:manifest': async (ctx) => {
      console.log('生成 manifest');
      console.log(ctx.manifest);
      // 可以添加、修改或删除 manifest 字段
    },
  },
});
```

### 钩子参数

```typescript
interface GenerateContext {
  manifest: Manifest;
  config: ResolvedConfig;
  browser: BrowserType;
}
```

## 七、优化阶段（Phase 7: Optimize）

### 阶段目标

优化输出文件并压缩。

### 执行内容

1. 压缩 JavaScript 代码
2. 压缩 CSS 代码
3. 优化图片资源
4. 移除未使用的代码（Tree Shaking）
5. 应用命名混淆（如果启用）

### 可用钩子

```typescript
export default defineConfig({
  hooks: {
    'optimize:output': async (ctx) => {
      console.log('优化输出');
      console.log(ctx.output);
      // 可以添加、修改或删除输出文件
    },
  },
});
```

### 钩子参数

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

## 八、完成阶段（Phase 8: Complete）

### 阶段目标

清理临时文件并完成构建。

### 执行内容

1. 清理临时文件
2. 移动输出文件到最终目录
3. 生成构建报告
4. 清理缓存
5. 完成构建

### 可用钩子

```typescript
export default defineConfig({
  hooks: {
    'build:done': async (ctx) => {
      console.log('构建完成');
      console.log(ctx.outputDir);
      console.log(ctx.duration);
      // 可以执行后续操作
    },
  },
});
```

### 钩子参数

```typescript
interface CompleteContext {
  outputDir: string;
  duration: number;
  config: ResolvedConfig;
}
```

## 完整钩子列表

### 构建钩子

| 钩子名 | 阶段 | 参数 | 说明 |
|--------|------|------|------|
| `prepare:build` | 准备 | PrepareContext | 构建准备时触发 |
| `resolve:entrypoints` | 解析 | ResolveContext | 解析入口点后触发 |
| `analyze:modules` | 分析 | AnalyzeContext | 分析模块后触发 |
| `transform:code` | 转换 | TransformContext | 转换代码时触发 |
| `build:module` | 构建 | BuildContext | 构建模块时触发 |
| `generate:manifest` | 生成 | GenerateContext | 生成 manifest 后触发 |
| `optimize:output` | 优化 | OptimizeContext | 优化输出时触发 |
| `build:done` | 完成 | CompleteContext | 构建完成时触发 |

### 开发钩子

| 钩子名 | 阶段 | 参数 | 说明 |
|--------|------|------|------|
| `dev:server:start` | 启动 | DevServerContext | 开发服务器启动时触发 |
| `dev:server:restart` | 重启 | DevServerContext | 开发服务器重启时触发 |
| `dev:file:change` | 变化 | FileChangeContext | 文件变化时触发 |
| `dev:server:close` | 关闭 | DevServerContext | 开发服务器关闭时触发 |

## 钩子示例

### 示例 1：修改 manifest

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  hooks: {
    'generate:manifest': async (ctx) => {
      // 添加自定义字段
      ctx.manifest.custom_field = 'custom_value';

      // 根据浏览器添加特定配置
      if (ctx.browser === 'firefox') {
        ctx.manifest.browser_specific_settings = {
          gecko: {
            id: 'my-extension@example.com',
          },
        };
      }
    },
  },
});
```

### 示例 2：添加自定义转换

```typescript
export default defineConfig({
  hooks: {
    'transform:code': async (ctx) => {
      // 替换环境变量
      ctx.code = ctx.code.replace(
        /__API_URL__/g,
        process.env.API_URL || 'https://api.example.com'
      );

      // 添加版本号
      ctx.code = ctx.code.replace(
        /__VERSION__/g,
        process.env.npm_package_version || '1.0.0'
      );
    },
  },
});
```

### 示例 3：生成构建报告

```typescript
import { writeFileSync } from 'fs';

export default defineConfig({
  hooks: {
    'build:done': async (ctx) => {
      const report = {
        outputDir: ctx.outputDir,
        duration: ctx.duration,
        timestamp: new Date().toISOString(),
      };

      writeFileSync(
        'build-report.json',
        JSON.stringify(report, null, 2)
      );

      console.log(`构建完成，耗时 ${ctx.duration}ms`);
      console.log(`输出目录: ${ctx.outputDir}`);
    },
  },
});
```

## 构建流程图

```
┌─────────────────┐
│  准备阶段（1）   │
│  初始化环境      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  解析阶段（2）   │
│  解析配置和入口点│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  分析阶段（3）   │
│  分析依赖和模块  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  转换阶段（4）   │
│  转换代码和资源  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  构建阶段（5）   │
│  构建和打包模块  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  生成阶段（6）   │
│  生成 manifest  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  优化阶段（7）   │
│  优化和压缩输出  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  完成阶段（8）   │
│  清理和完成构建  │
└─────────────────┘
```

## 常见问题

### Q1: 如何调试构建问题？

**启用详细日志：**

```bash
bun run build --debug
```

**使用钩子记录信息：**

```typescript
export default defineConfig({
  hooks: {
    'build:module': async (ctx) => {
      console.log('构建模块:', ctx.module.id);
      console.log('依赖:', ctx.module.dependencies);
    },
  },
});
```

### Q2: 如何添加自定义构建步骤？

**使用钩子添加自定义逻辑：**

```typescript
export default defineConfig({
  hooks: {
    'build:done': async (ctx) => {
      // 添加自定义构建步骤
      console.log('执行自定义构建步骤');

      // 例如：复制文件、生成文档、运行测试等
      await runCustomBuildSteps();
    },
  },
});
```

### Q3: 如何优化构建速度？

**启用缓存：**

```typescript
export default defineConfig({
  build: {
    rollupOptions: {
      cache: true,
    },
  },
});
```

**使用并行构建：**

```typescript
export default defineConfig({
  build: {
    parallel: true,
  },
});
```

**减少构建内容：**

```typescript
export default defineConfig({
  build: {
    sourcemap: false,
    minify: false,
  },
});
```

### Q4: 如何处理构建错误？

**使用钩子捕获错误：**

```typescript
export default defineConfig({
  hooks: {
    'build:module': async (ctx) => {
      try {
        // 构建模块
      } catch (error) {
        console.error('构建模块失败:', error);
        throw error;
      }
    },
  },
});
```

### Q5: 如何生成自定义输出？

**使用钩子生成自定义输出：**

```typescript
export default defineConfig({
  hooks: {
    'generate:manifest': async (ctx) => {
      // 生成自定义 manifest
      const customManifest = {
        ...ctx.manifest,
        custom_field: 'custom_value',
      };

      // 写入文件
      writeFileSync(
        path.join(ctx.config.outDir, 'custom-manifest.json'),
        JSON.stringify(customManifest, null, 2)
      );
    },
  },
});
```

## 下一步

- [钩子函数详解](./hooks.md)：详细说明所有钩子函数
- [完整流程图](./flow.md)：可视化的完整构建流程
- [命令参考](../cli/commands.md)：掌握开发和构建命令
- [入门指南](../guides/getting-started.md)：快速上手 WXT
