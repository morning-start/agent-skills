# 内容质量工具使用指南

> **版本**: v1.0.0 | **最后更新**: 2026-05-31
> **所属技能**: tutorial-writer-content | **角色**: data-layer

## 1. 工具概述

内容质量工具是一套用于自动化检测和提升教程内容质量的实用程序集合。这些工具围绕 content 技能的核心职责设计，帮助维护数据的完整性、一致性和规范性。

### 1.1 工具分类

```
质量工具体系
├── 验证类 (Validation)
│   ├── Frontmatter 验证
│   ├── Schema 合规检查
│   └── 命名规范检查
│
├── 检测类 (Detection)
│   ├── 断链检测
│   ├── 图片路径检查
│   └── 孤立文件检测
│
├── 统计类 (Statistics)
│   ├── 内容统计
│   ├── 进度追踪
│   └── 质量评分
│
└── 修复类 (Repair)
    ├── 自动修复（安全操作）
    └── 修复建议（人工确认）
```

### 1.2 设计原则

- **快速失败**: 尽早发现问题，避免错误传播
- **零误报**: 减少干扰，提高信任度
- **可配置**: 适应不同项目的需求差异
- **可扩展**: 易于添加新的检查规则

## 2. Frontmatter 验证工具

### 2.1 工具功能

自动验证所有章节文件的 Frontmatter 是否符合 Schema 定义。

**核心能力**:
- ✅ 必填字段完整性检查
- ✅ 字段类型验证
- ✅ 枚举值范围校验
- ✅ 自定义业务规则验证
- ✅ 详细的错误报告

### 2.2 使用方式

#### 手动执行

```bash
node scripts/validate-frontmatter.mjs
```

#### npm script

```json
{
  "scripts": {
    "validate:frontmatter": "node scripts/validate-frontmatter.mjs",
    "validate": "npm run validate:frontmatter && npm run validate:links"
  }
}
```

```bash
npm run validate:frontmatter
```

#### Git Hooks (husky)

```bash
npx husky add .pre-commit "npm run validate:frontmatter"
```

#### GitHub Actions

```yaml
# .github/workflows/validate.yml
name: Validate Content

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run validate:frontmatter
```

### 2.3 完整实现

```javascript
#!/usr/bin/env node
/**
 * @file Frontmatter 验证脚本
 * @description 验证所有章节的 Frontmatter 符合 Schema 定义
 */

import { readFileSync, readdirSync } from 'fs';
import { join, extname } from 'path';
import yaml from 'yaml';
import { z } from 'zod';

const CHAPTERS_DIR = 'packages/content/src/chapters';

const chapterSchema = z.object({
  title: z.string()
    .min(2, "标题至少 2 个字符")
    .max(100, "标题不超过 100 字符"),
    
  description: z.string()
    .max(500, "描述不超过 500 字符")
    .optional(),
    
  draft: z.boolean().default(false),
  
  date: z.string()
    .datetime("日期格式无效")
    .optional(),
    
  tags: z.array(z.string())
    .max(10, "标签最多 10 个")
    .default([]),
    
  difficulty: z.enum(['beginner', 'intermediate', 'advanced'])
    .optional(),
    
  readingTime: z.number()
    .min(1, "阅读时间至少 1 分钟")
    .max(300, "阅读时间不超过 300 分钟")
    .optional(),
    
  prerequisites: z.array(z.string())
    .max(10, "前置知识最多 10 项")
    .default([]),
    
  hasInteractive: z.boolean().default(false),
  hasMermaid: z.boolean().default(false),
  hasMath: z.boolean().default(false),
});

function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  
  if (!match) {
    return { raw: null, parsed: null, error: 'Missing frontmatter' };
  }
  
  try {
    const parsed = yaml.parse(match[1]);
    return { raw: match[1], parsed, error: null };
  } catch (error) {
    return { raw: match[1], parsed: null, error: error.message };
  }
}

function validateFile(filePath) {
  const content = readFileSync(filePath, 'utf-8');
  const fileName = basename(filePath);
  
  if (extname(fileName) !== '.md') {
    return { file: fileName, status: 'skipped', reason: 'Not a markdown file' };
  }
  
  const { raw, parsed, error: parseError } = parseFrontmatter(content);
  
  if (parseError) {
    return {
      file: fileName,
      status: 'error',
      errors: [{ field: '_parser', message: parseError }]
    };
  }
  
  if (!parsed) {
    return {
      file: fileName,
      status: 'error',
      errors: [{ field: '_structure', message: '无法解析 Frontmatter' }]
    };
  }
  
  const result = chapterSchema.safeParse(parsed);
  
  if (!result.success) {
    const errors = result.error.errors.map(err => ({
      field: err.path.join('.'),
      message: err.message,
      code: err.code,
    }));
    
    return { file: fileName, status: 'error', errors };
  }
  
  return { file: fileName, status: 'valid', data: result.data };
}

function main() {
  console.log('\n📋 Frontmatter 验证工具\n');
  console.log(`📂 目录: ${CHAPTERS_DIR}\n`);
  
  let validCount = 0;
  let errorCount = 0;
  let skipCount = 0;
  const allErrors = [];
  
  const files = readdirSync(CHAPTERS_DIR)
    .filter(f => !f.startsWith('.'));
  
  for (const file of files) {
    const filePath = join(CHAPTERS_DIR, file);
    const result = validateFile(filePath);
    
    switch (result.status) {
      case 'valid':
        console.log(`✅ ${result.file}`);
        validCount++;
        break;
        
      case 'error':
        console.log(`❌ ${result.file}`);
        result.errors.forEach(err => {
          console.log(`   • ${err.field}: ${err.message}`);
          allErrors.push({ file: result.file, ...err });
        });
        errorCount++;
        break;
        
      case 'skipped':
        console.log(`⏭️  ${result.file} (${result.reason})`);
        skipCount++;
        break;
    }
  }
  
  console.log('\n' + '═'.repeat(50));
  console.log(`📊 验证结果:`);
  console.log(`   ✅ 通过: ${validCount} 个文件`);
  console.log(`   ❌ 错误: ${errorCount} 个文件`);
  console.log(`   ⏭️  跳过: ${skipCount} 个文件`);
  
  if (allErrors.length > 0) {
    console.log('\n📝 错误详情:');
    console.table(allErrors);
  }
  
  console.log('\n');
  
  process.exit(errorCount > 0 ? 1 : 0);
}

main();
```

### 2.4 输出示例

```
📋 Frontmatter 验证工具

📂 目录: packages/content/src/chapters

✅ introduction.md
✅ getting-started.md
❌ core-concepts.md
   • title: 标题至少 2 个字符
   • difficulty: Invalid enum value
✅ api-reference.md
⏭️  .gitkeep (Not a markdown file)

═══════════════════════════════════════
📊 验证结果:
   ✅ 通过: 3 个文件
   ❌ 错误: 1 个文件
   ⏭️  跳过: 1 个文件

📝 错误详情:
┌─────────┬───────────┬─────────────────────────┬──────────┐
│ (index) │   file    │        field          │ message  │
├─────────┼───────────┼─────────────────────────┼──────────┤
│    0    │ 'core-...' │ 'title'                │ '标题...' │
│    1    │ 'core-...' │ 'difficulty'           │ 'Invalid...│
└─────────┴───────────┴─────────────────────────┴──────────┘
```

## 3. 断链检测工具

### 3.1 功能说明

检测 Markdown 文件中的内部链接是否指向存在的章节。

**检测范围**:
- 内部章节链接: `/chapters/{slug}`
- 锚点链接: `/chapters/{slug}#section`
- 相对路径链接: `./other-chapter`

### 3.2 实现思路

```javascript
// scripts/check-links.mjs
import { glob } from 'fs/promises';
import { readFileSync } from 'fs';
import { join, dirname } from 'path';

const CHAPTERS_DIR = 'packages/content/src/chapters';

async function checkInternalLinks() {
  const files = await glob('**/*.md', { cwd: CHAPTERS_DIR });
  
  const validSlugs = new Set(
    files.map(f => f.replace(/\.md$/, '').replace(/\\/g, '/'))
  );
  
  console.log(`\n🔗 断链检测工具`);
  console.log(`📂 有效章节: ${validSlugs.size} 个\n`);
  
  const linkPatterns = [
    { regex: /\]\(\/chapters\/([^)]*?)\)/g, type: 'absolute' },
    { regex: /\]\(\.\/([^)]*?)\)/g, type: 'relative' },
  ];
  
  let brokenLinks = [];
  let totalLinks = 0;
  
  for (const file of files) {
    const filePath = join(CHAPTERS_DIR, file);
    const content = readFileSync(filePath, 'utf-8');
    
    for (const pattern of linkPatterns) {
      let match;
      
      while ((match = pattern.regex.exec(content)) !== null) {
        totalLinks++;
        const target = match[1].split('#')[0].replace(/\/$/, '');
        
        if (pattern.type === 'absolute' && !validSlugs.has(target)) {
          brokenLinks.push({
            source: file,
            target: `/chapters/${target}`,
            type: pattern.type,
          });
        }
      }
    }
  }
  
  if (brokenLinks.length === 0) {
    console.log(`✅ 所有 ${totalLinks} 个内部链接有效\n`);
  } else {
    console.log(`❌ 发现 ${brokenLinks.length} 个断链:\n`);
    brokenLinks.forEach(link => {
      console.log(`   ${link.source} → ${link.target}`);
    });
  }
  
  return brokenLinks.length === 0 ? 0 : 1;
}

checkInternalLinks().then(exitCode => process.exit(exitCode));
```

### 3.3 外部链接检测（可选）

对于外部链接，可使用第三方工具：

```bash
npm install -D broken-link-checker

blc https://your-tutorial.com \
  --recursive \
  --exclude-external \
  --ordered \
  --get-level 3
```

## 4. 图片路径检查工具

### 4.1 检查规则

1. **存在性检查**: 引用的图片文件必须存在
2. **路径格式检查**: 不允许绝对路径（CDN 除外）
3. **格式检查**: 仅允许指定格式
4. **大小检查**: 可选，警告过大图片

### 4.2 实现示例

```javascript
// scripts/check-images.mjs
import { existsSync, statSync } from 'fs';
import { join, dirname, extname } from 'path';

const ALLOWED_FORMATS = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'];
const MAX_IMAGE_SIZE_MB = 5;

const imageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;

function checkImagePaths(content, sourceFilePath) {
  const issues = [];
  let match;
  
  while ((match = imageRegex.exec(content)) !== null) {
    const altText = match[1];
    const imagePath = match[2];
    
    if (imagePath.startsWith('http')) continue; // CDN 图片跳过
    
    const absolutePath = join(dirname(sourceFilePath), imagePath);
    
    if (!existsSync(absolutePath)) {
      issues.push({
        type: 'not_found',
        path: imagePath,
        message: `图片不存在: ${imagePath}`,
      });
      continue;
    }
    
    const ext = extname(imagePath).toLowerCase();
    if (!ALLOWED_FORMATS.includes(ext)) {
      issues.push({
        type: 'invalid_format',
        path: imagePath,
        message: `不支持的图片格式: ${ext}`,
      });
    }
    
    try {
      const stats = statSync(absolutePath);
      const sizeMB = stats.size / (1024 * 1024);
      
      if (sizeMB > MAX_IMAGE_SIZE_MB) {
        issues.push({
          type: 'too_large',
          path: imagePath,
          message: `图片过大 (${sizeMB.toFixed(2)}MB)，建议压缩`,
        });
      }
    } catch (error) {
      issues.push({
        type: 'access_error',
        path: imagePath,
        message: `无法读取图片: ${error.message}`,
      });
    }
  }
  
  return issues;
}
```

## 5. 内容统计工具

### 5.1 统计指标

| 指标 | 计算方式 | 用途 |
|------|---------|------|
| 总章节数 | `.md` 文件数 | 进度追踪 |
| 总字数 | 中文字数 + 英文词数 | 工作量评估 |
| 平均阅读时间 | ΣreadingTime / n | 课程时长 |
| 草稿比例 | draft:true 数量占比 | 发布就绪度 |
| 标签覆盖率 | 有 tags 的章节占比 | 元数据完整性 |
| 交互组件比例 | hasInteractive:true 占比 | 丰富度评估 |
| Mermaid 使用率 | hasMermaid:true 占比 | 可视化程度 |
| 数学公式使用率 | hasMath:true 占比 | 技术深度 |

### 5.2 实现示例

```javascript
// scripts/content-stats.mjs
import { glob } from 'fs/promises';
import { readFileSync } from 'fs';
import yaml from 'yaml';

function extractFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  return match ? yaml.parse(match[1]) : {};
}

function countWords(content) {
  const text = content
    .replace(/^---\n[\s\S]*?\n---/, '')
    .replace(/```[\s\S]*?```/g, '')
    .replace(/!\[.*?\]\(.*?\)/g, '')
    .replace(/\[[^\]]+\]\([^)]+\)/g, '')
    .replace(/[#*_~`]/g, '')
    .trim();
  
  const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
  const englishWords = text.split(/\s+/).filter(w => /[a-zA-Z]+/.test(w)).length;
  
  return { chineseChars, englishWords, total: chineseChars + englishWords };
}

async function generateStats() {
  const files = await glob('packages/content/src/chapters/**/*.md');
  
  const stats = {
    totalChapters: files.length,
    totalChineseChars: 0,
    totalEnglishWords: 0,
    totalReadingTime: 0,
    draftCount: 0,
    withTagsCount: 0,
    withDifficultyCount: 0,
    withPrereqsCount: 0,
    interactiveCount: 0,
    mermaidCount: 0,
    mathCount: 0,
    withDateCount: 0,
    withDescriptionCount: 0,
  };
  
  for (const file of files) {
    const content = readFileSync(file, 'utf-8');
    const fm = extractFrontmatter(content);
    const words = countWords(content);
    
    stats.totalChineseChars += words.chineseChars;
    stats.totalEnglishWords += words.englishWords;
    stats.totalReadingTime += fm.readingTime || 0;
    
    if (fm.draft) stats.draftCount++;
    if (fm.tags?.length > 0) stats.withTagsCount++;
    if (fm.difficulty) stats.withDifficultyCount++;
    if (fm.prerequisites?.length > 0) stats.withPrereqsCount++;
    if (fm.hasInteractive) stats.interactiveCount++;
    if (fm.hasMermaid) stats.mermaidCount++;
    if (fm.hasMath) stats.mathCount++;
    if (fm.date) stats.withDateCount++;
    if (fm.description) stats.withDescriptionCount++;
  }
  
  const n = stats.totalChapters || 1;
  
  return {
    ...stats,
    avgReadingTime: Math.round(stats.totalReadingTime / n),
    draftPercentage: Math.round((stats.draftCount / n) * 100),
    tagsCoverage: Math.round((stats.withTagsCount / n) * 100),
    difficultyCoverage: Math.round((stats.withDifficultyCount / n) * 100),
    prereqsCoverage: Math.round((stats.withPrereqsCount / n) * 100),
    interactivePercentage: Math.round((stats.interactiveCount / n) * 100),
    mermaidPercentage: Math.round((stats.mermaidCount / n) * 100),
    mathPercentage: Math.round((stats.mathCount / n) * 100),
    dateCoverage: Math.round((stats.withDateCount / n) * 100),
    descriptionCoverage: Math.round((stats.withDescriptionCount / n) * 100),
    estimatedReadingMinutes: Math.ceil(stats.totalChineseChars / 400 + stats.totalEnglishWords / 200),
  };
}

async function main() {
  console.log('\n📊 内容统计报告\n');
  console.log('═'.repeat(60));
  
  const stats = await generateStats();
  
  console.table(stats);
  
  console.log('\n📈 质量评分:');
  
  const scores = [
    { metric: '元数据完整性', score: calculateMetadataScore(stats), weight: 0.3 },
    { metric: '发布就绪度', score: 100 - stats.draftPercentage, weight: 0.3 },
    { metric: '内容丰富度', score: calculateRichnessScore(stats), weight: 0.2 },
    { metric: '格式规范度', score: calculateFormatScore(stats), weight: 0.2 },
  ];
  
  const weightedScore = Math.round(
    scores.reduce((sum, s) => sum + s.score * s.weight, 0)
  );
  
  console.log(`   综合评分: ${weightedScore}/100\n`);
  
  if (weightedScore >= 80) console.log('🎉 优秀！');
  else if (weightedScore >= 60) console.log('👍 良好');
  else console.log('⚠️ 需要改进');
}

function calculateMetadataScore(s) {
  return Math.round((
    s.tagsCoverage +
    s.difficultyCoverage +
    s.prereqsCoverage +
    s.dateCoverage +
    s.descriptionCoverage
  ) / 5);
}

function calculateRichnessScore(s) {
  return Math.round((
    s.interactivePercentage +
    s.mermaidPercentage +
    s.mathPercentage
  ) / 3);
}

function calculateFormatScore(s) {
  return 100; // 如果通过验证就是满分
}

main().catch(console.error);
```

### 5.3 输出示例

```
📊 内容统计报告

══════════════════════════════════════════════════════
┌─────────────────────────┬──────────┐
│ 指标                    │ 值       │
├─────────────────────────┼──────────┤
│ totalChapters           │ 12       │
│ totalChineseChars        │ 45680    │
│ totalEnglishWords        │ 3200     │
│ totalReadingTime        │ 180      │
│ draftCount              │ 3        │
│ withTagsCount           │ 11       │
│ withDifficultyCount     │ 10       │
│ ...                     │ ...      │
│ estimatedReadingMinutes │ 118      │
└─────────────────────────┴──────────┘

📈 质量评分:
   综合评分: 85/100

🎉 优秀！
```

## 6. 工具集成方案

### 6.1 统一入口脚本

```json
{
  "scripts": {
    "quality:validate": "node scripts/validate-frontmatter.mjs",
    "quality:links": "node scripts/check-links.mjs",
    "quality:images": "node scripts/check-images.mjs",
    "quality:stats": "node scripts/content-stats.mjs",
    "quality:all": "npm run quality:validate && npm run quality:links && npm run quality:stats",
    "quality:ci": "npm run quality:all"
  }
}
```

### 6.2 Turborepo 集成

```json
{
  "tasks": {
    "quality": {
      "cache": false,
      "dependsOn": []
    }
  }
}
```

```bash
bunx turbo run quality
```

### 6.3 VS Code 集成

在 `.vscode/tasks.json` 中添加:

```json
{
  "label": "Validate Frontmatter",
  "type": "shell",
  "command": "npm run quality:validate",
  "group": "build",
  "problemMatcher": "$tsc"
}
```

## 7. 最佳实践

### 7.1 CI/CD 中的质量门禁

```yaml
# .github/workflows/quality.yml
name: Quality Gates

on:
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'pnpm'
      
      - name: Install dependencies
        run: bun install
        
      - name: Run validation
        run: bun run quality:ci
        
      - name: Generate report
        run: bun run quality:stats
        if: always()
        
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: quality-report
          path: reports/
        if: always()
```

### 7.2 本地开发工作流

1. **提交前**: `npm run quality:validate`
2. **Push 前**: `npm run quality:all`
3. **定期**: `npm run quality:stats` 查看进度
4. **发布前**: 完整的质量检查报告

### 7.3 团队协作建议

- **统一配置**: 共享 `.qualityrc.json` 配置文件
- **阈值设定**: 定义最低质量标准（如覆盖率 > 80%）
- **持续改进**: 定期审查和调整检查规则
- **文档同步**: 新增字段时更新验证规则

---

**相关文档**:
- [SKILL.md 主文档](../SKILL.md) — 质量工具概述
- [frontmatter-schema.md](./frontmatter-schema.md) — Schema 定义（验证依据）
- [naming-conventions.md](./naming-conventions.md) — 命名规范（检查规则）
- [enhancement-pipeline.md](./enhancement-pipeline.md) — 增强管道（预处理）
