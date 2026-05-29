# 完整流程图

本文档使用 Mermaid 流程图展示 WXT 构建和开发的完整流程。

## 官方导航链接

- [Remote Code](https://wxt.dev/guide/essentials/remote-code.html) - 远程代码加载与安全策略
- [WXT Modules](https://wxt.dev/guide/essentials/wxt-modules.html) - WXT 模块开发与使用
- [Hooks](https://wxt.dev/guide/essentials/config/hooks.html) - 构建与运行时钩子函数

---

## 构建流程

### 构建生命周期

```mermaid
graph TB
    A[开始构建] --> B[准备阶段 Phase 1]
    B --> C[解析阶段 Phase 2]
    C --> D[分析阶段 Phase 3]
    D --> E[转换阶段 Phase 4]
    E --> F[构建阶段 Phase 5]
    F --> G[生成阶段 Phase 6]
    G --> H[优化阶段 Phase 7]
    H --> I[完成阶段 Phase 8]
    I --> J[构建完成]

    B --> B1[prepare:build 钩子]
    C --> C1[resolve:entrypoints 钩子]
    D --> D1[analyze:modules 钩子]
    E --> E1[transform:code 钩子]
    F --> F1[build:module 钩子]
    G --> G1[generate:manifest 钩子]
    H --> H1[optimize:output 钩子]
    I --> I1[build:done 钩子]
```

### 详细构建流程

```mermaid
graph LR
    A[命令: bun run build] --> B[加载 wxt.config.ts]
    B --> C[加载 package.json]
    C --> D[验证环境]
    D --> E[准备构建环境]

    E --> F[扫描 entrypoints/]
    F --> G[解析入口点]
    G --> H[解析 manifest.json]
    H --> I[解析 TypeScript 配置]
    I --> J[解析框架配置]

    J --> K[分析 import 语句]
    K --> L[构建依赖图]
    L --> M[检测循环依赖]
    M --> N[分析 TypeScript 类型]

    N --> O[转换 TS → JS]
    O --> P[转换框架组件]
    P --> Q[转换 CSS/样式]
    Q --> R[处理静态资源]

    R --> S[Rollup 打包]
    S --> T[生成 chunks]
    T --> U[代码分割]
    U --> V[生成 sourcemap]

    V --> W[生成 manifest.json]
    W --> X[复制公共资源]
    X --> Y[生成 HTML 文件]
    Y --> Z[生成浏览器配置]

    Z --> AA[压缩 JS/CSS]
    AA --> AB[优化图片]
    AB --> AC[Tree Shaking]
    AC --> AD[命名混淆]

    AD --> AE[清理临时文件]
    AE --> AF[移动输出文件]
    AF --> AG[生成构建报告]
    AG --> AH[构建完成]
```

## 开发流程

### 开发服务器生命周期

```mermaid
graph TB
    A[命令: bun run dev] --> B[启动开发服务器]
    B --> C[dev:server:start 钩子]
    C --> D[监听文件变化]

    D --> E{文件变化?}
    E -->|是| F[dev:file:change 钩子]
    F --> G[增量构建]
    G --> H[热重载]
    H --> I[更新浏览器]

    E -->|否| J[继续监听]
    I --> J

    J --> K{用户退出?}
    K -->|否| E
    K -->|是| L[关闭开发服务器]
    L --> M[dev:server:close 钩子]
    M --> N[清理资源]
    N --> O[开发结束]
```

### 详细开发流程

```mermaid
graph LR
    A[启动开发服务器] --> B[初始化 Vite 服务器]
    B --> C[扫描 entrypoints/]
    C --> D[解析入口点]
    D --> E[初始构建]
    E --> F[生成 manifest.json]
    F --> G[加载浏览器扩展]

    G --> H[监听文件系统]
    H --> I{文件变化?}

    I -->|创建| J[dev:file:change 钩子]
    J --> K[添加新文件到构建]
    K --> L[热重载]
    L --> M[更新浏览器]

    I -->|更新| N[dev:file:change 钩子]
    N --> O[重新构建变化文件]
    O --> P[热重载]
    P --> M

    I -->|删除| Q[dev:file:change 钩子]
    Q --> R[从构建中移除文件]
    R --> S[热重载]
    S --> M

    M --> T[继续监听]
    T --> I

    I -->|配置变化| U[dev:server:restart 钩子]
    U --> V[重启服务器]
    V --> H

    T --> W{用户退出?}
    W -->|否| I
    W -->|是| X[停止监听]
    X --> Y[关闭服务器]
    Y --> Z[dev:server:close 钩子]
    Z --> AA[清理临时文件]
    AA --> AB[开发结束]
```

## 入口点处理流程

### Background Script

```mermaid
graph TB
    A[background.ts] --> B[defineBackground]
    B --> C[解析入口点配置]
    C --> D[分析依赖]
    D --> E[转换代码]
    E --> F[打包]
    F --> G[生成 background.js]
    G --> H[更新 manifest.json]
    H --> I[加载到浏览器]
```

### Content Script

```mermaid
graph TB
    A[content.ts] --> B[defineContentScript]
    B --> C[解析入口点配置]
    C --> D[分析依赖]
    D --> E[转换代码]
    E --> F[打包]
    F --> G[生成 content.js]
    G --> H[更新 manifest.json]
    H --> I[加载到浏览器]
```

### Popup

```mermaid
graph TB
    A[popup.html] --> B[解析 HTML]
    B --> C[popup.ts]
    C --> D[转换代码]
    D --> E[打包]
    E --> F[生成 popup.html]
    F --> G[更新 manifest.json]
    G --> H[加载到浏览器]

    A --> I[App.svelte]
    I --> J[转换组件]
    J --> E
```

### Options

```mermaid
graph TB
    A[options.html] --> B[解析 HTML]
    B --> C[options.ts]
    C --> D[转换代码]
    D --> E[打包]
    E --> F[生成 options.html]
    F --> G[更新 manifest.json]
    G --> H[加载到浏览器]

    A --> I[App.svelte]
    I --> J[转换组件]
    J --> E
```

## 多浏览器构建流程

```mermaid
graph TB
    A[构建命令] --> B{指定浏览器?}

    B -->|是| C[构建指定浏览器]
    B -->|否| D[构建所有浏览器]

    C --> E[加载浏览器特定配置]
    D --> F[遍历支持浏览器]

    E --> G[Chrome 构建]
    F --> G
    F --> H[Firefox 构建]
    F --> I[Edge 构建]
    F --> J[Safari 构建]

    G --> K[生成 Chrome manifest]
    H --> L[生成 Firefox manifest]
    I --> M[生成 Edge manifest]
    J --> N[生成 Safari manifest]

    K --> O[.output/chrome/]
    L --> P[.output/firefox/]
    M --> Q[.output/edge/]
    N --> R[.output/safari/]

    O --> S[打包 Chrome]
    P --> T[打包 Firefox]
    Q --> U[打包 Edge]
    R --> V[打包 Safari]

    S --> W[chrome-1.0.0.zip]
    T --> X[firefox-1.0.0.zip]
    U --> Y[edge-1.0.0.zip]
    V --> Z[safari-1.0.0.zip]

    W --> AA[构建完成]
    X --> AA
    Y --> AA
    Z --> AA
```

## 钩子执行顺序

### 构建钩子执行顺序

```mermaid
graph TB
    A[开始构建] --> B[prepare:build]
    B --> C[解析入口点]
    C --> D[resolve:entrypoints]
    D --> E[分析模块]
    E --> F[analyze:modules]
    F --> G[转换代码]
    G --> H[transform:code × N]
    H --> I[构建模块]
    I --> J[build:module × N]
    J --> K[生成 manifest]
    K --> L[generate:manifest]
    L --> M[优化输出]
    M --> N[optimize:output]
    N --> O[build:done]
    O --> P[构建完成]
```

### 开发钩子执行顺序

```mermaid
graph TB
    A[启动开发服务器] --> B[dev:server:start]
    B --> C[监听文件]

    C --> D[文件变化]
    D --> E[dev:file:change]
    E --> F[热重载]

    F --> G{配置变化?}
    G -->|是| H[dev:server:restart]
    H --> I[重启服务器]
    I --> C

    G -->|否| J{继续监听?}
    J -->|是| D
    J -->|否| K[关闭服务器]
    K --> L[dev:server:close]
    L --> M[开发结束]
```

## 框架特定流程

### Svelte 项目构建

```mermaid
graph TB
    A[App.svelte] --> B[解析 SFC]
    B --> C[提取 script]
    B --> D[提取 template]
    B --> E[提取 style]

    C --> F[转换 script TS]
    D --> G[编译 template JS]
    E --> H[编译 style CSS]

    F --> I[合并组件代码]
    G --> I
    H --> I

    I --> J[打包]
    J --> K[生成输出]
```

### Vue 项目构建

```mermaid
graph TB
    A[App.vue] --> B[解析 SFC]
    B --> C[提取 script setup]
    B --> D[提取 template]
    B --> E[提取 style scoped]

    C --> F[转换 script TS]
    D --> G[编译 template 渲染函数]
    E --> H[编译 style CSS]

    F --> I[合并组件代码]
    G --> I
    H --> I

    I --> J[打包]
    J --> K[生成输出]
```

### React 项目构建

```mermaid
graph TB
    A[App.tsx] --> B[解析 JSX]
    B --> C[转换 TS]
    C --> D[编译 JSX → JS]
    D --> E[打包]
    E --> F[生成输出]
```

## 错误处理流程

```mermaid
graph TB
    A[执行操作] --> B{成功?}
    B -->|是| C[继续下一步]
    B -->|否| D[捕获错误]

    D --> E[记录错误日志]
    E --> F[分析错误类型]

    F --> G{可恢复?}
    G -->|是| H[执行恢复逻辑]
    H --> I[继续执行]
    G -->|否| J[终止构建]

    J --> K[显示错误信息]
    K --> L[退出流程]
```

## 部署流程

```mermaid
graph TB
    A[构建完成] --> B[打包扩展]
    B --> C{浏览器?}

    C -->|Chrome| D[Chrome Web Store]
    C -->|Firefox| E[Firefox Add-ons]
    C -->|Edge| F[Microsoft Edge Add-ons]
    C -->|Safari| G[Safari App Store]

    D --> H[登录开发者账户]
    E --> H
    F --> H
    G --> I[登录 Apple 开发者账户]

    H --> J[上传 ZIP 文件]
    I --> J

    J --> K[填写商店信息]
    K --> L[提交审核]
    L --> M{审核通过?}

    M -->|是| N[发布扩展]
    M -->|否| O[审核失败]
    O --> P[修正问题]
    P --> J

    N --> Q[发布成功]
```

## 性能优化流程

```mermaid
graph TB
    A[分析构建输出] --> B[检测大文件]
    A --> C[检测重复依赖]
    A --> D[检测未使用代码]

    B --> E{超过阈值?}
    E -->|是| F[代码分割]
    E -->|否| G[跳过优化]

    C --> H{重复依赖?}
    H -->|是| I[去重依赖]
    H -->|否| G

    D --> J{未使用代码?}
    J -->|是| K[Tree Shaking]
    J -->|否| G

    F --> L[重新构建]
    I --> L
    K --> L

    L --> M[验证优化效果]
    M --> N{满意?}
    N -->|否| A
    N -->|是| O[优化完成]
```

## 完整工作流程

### 从开发到部署的完整流程

```mermaid
graph TB
    A[创建项目] --> B[选择框架]
    B --> C[配置项目]
    C --> D[开发功能]

    D --> E[本地测试]
    E --> F{测试通过?}
    F -->|否| G[修复问题]
    G --> D

    F -->|是| H[构建扩展]
    H --> I[打包扩展]
    I --> J[多浏览器测试]

    J --> K{测试通过?}
    K -->|否| G
    K -->|是| L[提交审核]

    L --> M{审核通过?}
    M -->|否| N[审核失败]
    N --> O[修正问题]
    O --> H

    M -->|是| P[发布扩展]
    P --> Q[发布成功]

    Q --> R[收集用户反馈]
    R --> S{新功能?}
    S -->|是| T[规划新版本]
    T --> D

    S -->|否| U[维护现有版本]
    U --> V[修复 Bug]
    V --> H
```

## 使用说明

### 如何查看流程图

1. **Markdown 编辑器**：支持 Mermaid 的编辑器可以渲染流程图
   - VS Code + Mermaid 插件
   - Typora
   - Obsidian
   - GitHub README（自动渲染）

2. **在线工具**：使用在线 Mermaid 编辑器
   - https://mermaid.live
   - https://mermaid-js.github.io/mermaid-live-editor

3. **导出图片**：将流程图导出为 PNG 或 SVG

### 自定义流程图

您可以根据项目需求修改流程图：

```mermaid
graph TB
    A[开始] --> B[步骤1]
    B --> C[步骤2]
    C --> D[结束]
```

## 更多资源

- [构建阶段详解](./phases.md)：8 个构建阶段的详细说明
- [钩子函数详解](./hooks.md)：所有钩子函数的详细文档
- [命令参考](../cli/commands.md)：掌握开发和构建命令
- [入门指南](../guides/getting-started.md)：快速上手 WXT
