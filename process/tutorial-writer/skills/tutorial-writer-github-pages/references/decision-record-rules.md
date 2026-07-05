# Publish 阶段决策细则

## 本阶段涉及的决策项

| ID | 决策问题 | 影响 |
|----|---------|------|
| `project_delivery_format` | 交付物格式？ | 决定是否执行网页发布流程 |
| `project_web_ssg` | SSG 选型？ | 决定 mkdocs.yml 主题和插件配置 |
| `project_web_diagram` | 图解方案？ | 决定使用 Mermaid 还是自定义 SVG |
| `project_web_interactive` | 需要交互组件？ | 决定是否需要额外 JS 工作 |
| `project_web_deploy` | 部署方式？ | 决定使用 GitHub Actions 还是手动 |

## 操作指引

1. 执行网页发布前检查 `project_delivery_format` 是否包含 `web`
2. 如不包含，跳过网页发布流程，仅做 Markdown 交付
3. 根据 `project_web_ssg` 和 `project_web_diagram` 配置站点
4. 根据 `project_web_interactive` 决定是否需要开发交互组件
