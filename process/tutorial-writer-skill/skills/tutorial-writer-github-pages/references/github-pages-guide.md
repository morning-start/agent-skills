# GitHub Pages 高级部署指南

> **来源**: [../SKILL.md](../SKILL.md) → 高级部署参考
> **用途**: 多环境部署、自动化策略、回滚机制、性能监控、安全加固等高级主题
> **何时读取**: 需要 staging/production 环境分离、自动回滚、部署通知、CI/CD 进阶配置时

---

## 1. 多环境部署策略

### 分支策略

```
main          → Production（正式站点）
staging       → Staging（预发布测试）
develop       → 开发环境（日常验证）
feature/*     → 功能分支（不部署）
```

### GitHub Actions 多环境工作流

**`.github/workflows/deploy-staging.yml`**：

```yaml
name: Deploy to Staging

on:
  push:
    branches: ['staging']

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages-staging
      url: ${{ steps.deploy.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: withastro/action@v3
```

⚠️ **限制**: GitHub 免费版仅支持 **1 个 Pages 环境**。Staging 和 Production 共享 URL。完全隔离需用 Cloudflare Pages 或 Vercel。

---

## 2. 自动回滚机制

### 基于健康检查的回滚

在 deploy job 后添加 health-check job：

```yaml
  health-check:
    runs-on: ubuntu-latest
    needs: build-and-deploy
    if: always()
    steps:
      - name: Wait + Check
        id: health
        run: |
          sleep 30
          STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${{ needs.build-and-deploy.outputs.page_url }}")
          if [ "$STATUS" != "200" ]; then
            echo "rollback_needed=true" >> $GITHUB_OUTPUT
            exit 1
          fi
          echo "rollback_needed=false" >> $GITHUB_OUTPUT

      - name: Create Rollback Issue
        if: failure()
        run: |
          gh issue create \
            --title "🚨 部署失败 - 需要回滚" \
            --body "部署未通过健康检查。\n\n建议操作:\n1. \`git revert HEAD\`\n2. 推送到 main" \
            --repo ${{ github.repository }}
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 手动回滚流程

1. 找到最后一个健康的 commit：`git log --oneline -20`
2. 创建回滚分支：`git checkout -b rollback/<date> <healthy-commit>`
3. 触发重新部署
4. 验证后清理分支

---

## 3. 部署通知与监控

### Slack / Discord 通知

```yaml
      - name: Notify Success
        if: success()
        run: |
          curl -X POST -H 'Content-type: application/json' \
          --data "{\"text\": \"✅ 教程站点部署成功!\\n提交: ${{ github.sha }}\"}" \
          ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Uptime 监控（免费方案）

| 服务 | 特点 | 价格 |
|------|------|------|
| **UptimeRobot** | 每 5 分钟检查 | 免费 |
| **Better Uptime** | 包含状态页面 | 免费基础版 |

**配置示例**：
- 监控 URL: `https://username.github.io/repo/`
- 关键词检测: `<title>` 标签中的站点名称

### Core Web Vitals 监控

在布局组件中添加（可选）：

```astro
<script>
  import { onCLS, onFID, onINP, onLCP } from 'web-vitals';

  function sendToAnalytics(metric) {
    navigator.sendBeacon('/api/vitals', JSON.stringify(metric));
  }

  onCLS(sendToAnalytics);
  onFID(sendToAnalytics);
  onINP(sendToAnalytics);
  onLCP(sendToAnalytics);
</script>
```

---

## 4. 安全最佳实践

### 依赖安全扫描

**`.github/dependabot.yml`**：

```yaml
version: 2
updates:
  - package-ecosystem: 'npm'
    directory: '/'
    schedule:
      interval: 'weekly'
    labels:
      - 'dependencies'
      - 'security'
```

### CSP 配置（生产环境强制执行）

```javascript
csp: {
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'strict-dynamic'", "'nonce-<random>'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", 'data:', 'https:'],
    frameSrc: ["'none'"],
    objectSrc: ["'none'"],
  },
  reportOnly: false,
}
```

### 敏感信息管理

❌ **禁止**：
- 硬编码 API Key / 密码
- 提交 `.env` 文件到 Git

✅ **正确做法**：
- 使用 GitHub Secrets：`${{ secrets.SECRET_NAME }}`
- 环境变量：`process.env.PUBLIC_VAR`
- `.env.example` 提供模板（不含真实值）

---

## 5. 性能优化专项

### 利用 GitHub Pages 缓存

GitHub Pages 自动设置缓存头：

| 资源类型 | Cache-Control |
|----------|---------------|
| HTML | `no-cache`（始终验证）|
| CSS/JS | 公开缓存 1 小时 |
| 图片/字体 | 公开缓存 1 年（需 hash 文件名）|

Astro 默认为 `_astro/` 目录下的文件添加 hash，无需额外配置。

### 减少构建产物大小

**分析工具**：

```bash
npm install -D rollup-plugin-visualizer
```

**优化策略**：

1. Tree-shaking 未使用的代码
2. 使用轻量替代库（lodash-es, date-fns）
3. 压缩图片（WebP/AVIF）
4. 启用 Queued Rendering（大型站点）

---

## 6. 国际化部署 (i18n)

### 配置多语言站点

```javascript
i18n: {
  defaultLocale: 'zh-CN',
  locales: ['zh-CN', 'en', 'ja'],
  routing: {
    prefixDefaultLocale: false,
  },
},
```

### SEO 优化

```astro
---
// 在 BaseLayout 中
---

<link rel="alternate" hreflang={locale} href={url} />
<link rel="canonical" href={canonicalUrl} />
```

---

## 7. 故障排查速查表

| HTTP 状态码 | 含义 | 可能原因 | 解决方案 |
|-------------|------|---------|---------|
| **404** | 未找到 | base/trailingSlash 配置错误 | 检查 `astro.config.mjs` |
| **403** | 禁止访问 | Jekyll 处理问题 | 添加 `.nojekyll` |
| **500** | 服务器错误 | 构建失败 | 查看 Actions 日志 |
| **502/503** | 网关超时 | GitHub Pages 临时故障 | 几分钟后重试 |
| **504** | 网关超时 | 构建时间过长 | 优化性能或增加 Node 内存 |

### Actions 日志排查重点

- 展开 failed 的 step 查看详细输出
- 关注红色错误信息
- 检查 Node.js 版本兼容性
- 验证权限配置（pages: write, id-token: write）

---

## 8. 迁移指南

### 从其他平台迁移到 GitHub Pages

**主要差异对比**：

| 特性 | Netlify/Vercel | GitHub Pages |
|------|---------------|--------------|
| SSR 支持 | ✅ | ❌ 仅静态 |
| Serverless Functions | ✅ 原生 | ❌ 需外部服务 |
| Form Handling | ✅ 内置 | ❌ 需第三方 |
| 部署预览 | ✅ PR 自动部署 | ⚠️ 需配置 Actions |
| 多环境 | ✅ 原生 | ⚠️ 受限 |

**迁移步骤**：

1. 更新 `astro.config.mjs`（site/base/trailingSlash）
2. 替换表单处理为 Formspree/Netlify Forms
3. 迁移 Functions 到 Cloudflare Workers/Vercel Functions
4. 更新 DNS 指向 GitHub Pages
5. 设置 GitHub Actions 工作流

---

## 相关资源

- [GitHub Pages 官方文档](https://docs.github.com/en/pages)
- [Astro 官方部署指南](https://docs.astro.build/guides/deploy/github/)
- [withastro/action 仓库](https://github.com/withastro/action)
- [Dependabot 文档](https://docs.github.com/en/code-security/dependabot)
