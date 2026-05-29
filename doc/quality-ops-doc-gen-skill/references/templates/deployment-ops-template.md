# 部署与运维手册

> **文档版本**: 1.0.0
> **创建日期**: {{creation_date}}
> **最后更新**: {{last_updated_date}}
> **项目名称**: {{project_name}}
> **负责人**: {{ops_lead}}

---

## 1. 文档概述

### 1.1 文档目的

本部署与运维手册定义了 {{project_name}} 项目的部署流程、运维规范和故障处理方法，确保系统稳定、高效、可维护地运行。

### 1.2 适用范围

**适用环境**:
- {{environment_1}}
- {{environment_2}}
- {{environment_3}}

**适用角色**:
- DevOps 工程师
- SRE（站点可靠性工程师）
- 后端开发工程师
- 运维工程师

### 1.3 部署架构

```
{{deployment_diagram}}
```

**架构说明**:
{{architecture_description}}

---

## 2. 系统架构与环境

### 2.1 系统架构

**架构类型**: {{architecture_type}}（单体/微服务/Serverless）

**技术栈**:
| 组件 | 技术 | 版本 | 用途 |
|------|------|------|------|
| 前端 | {{frontend_tech}} | {{frontend_version}} | 用户界面 |
| 后端 | {{backend_tech}} | {{backend_version}} | 业务逻辑 |
| 数据库 | {{database_tech}} | {{database_version}} | 数据存储 |
| 缓存 | {{cache_tech}} | {{cache_version}} | 缓存加速 |
| 消息队列 | {{mq_tech}} | {{mq_version}} | 异步处理 |

### 2.2 环境配置

#### 开发环境

**配置文件**: `config/development.yaml`

**关键配置**:
```yaml
{{dev_config}}
```

**访问地址**: {{dev_env_url}}

**数据库**: {{dev_database_url}}

#### 测试环境

**配置文件**: `config/testing.yaml`

**关键配置**:
```yaml
{{test_config}}
```

**访问地址**: {{test_env_url}}

**数据库**: {{test_database_url}}

#### 预发环境

**配置文件**: `config/staging.yaml`

**关键配置**:
```yaml
{{staging_config}}
```

**访问地址**: {{staging_env_url}}

**数据库**: {{staging_database_url}}

#### 生产环境

**配置文件**: `config/production.yaml`

**关键配置**:
```yaml
{{prod_config}}
```

**访问地址**: {{prod_env_url}}

**数据库**: {{prod_database_url}}

---

## 3. CI/CD 流程

### 3.1 CI/CD 架构

**工具链**:
- 代码仓库: {{git_repo}}
- CI/CD平台: {{cicd_platform}}
- 构建工具: {{build_tool}}
- 部署工具: {{deploy_tool}}

### 3.2 CI 流程

**触发条件**:
- 代码推送到 {{branch_name}} 分支
- 创建/更新 Pull Request
- 手动触发

**CI 流程**:
```
{{ci_pipeline_diagram}}
```

**CI 配置文件**: `.{{cicd_config_file}}`

```{{cicd_config_language}}
{{ci_config_content}}
```

**CI 阶段**:
| 阶段 | 任务 | 超时时间 | 失败处理 |
|------|------|----------|----------|
| 代码检查 | Lint、格式检查 | {{lint_timeout}} | 阻止合并 |
| 单元测试 | 运行单元测试 | {{unit_test_timeout}} | 阻止合并 |
| 构建 | 构建应用 | {{build_timeout}} | 阻止合并 |
| 集成测试 | 运行集成测试 | {{integration_test_timeout}} | 阻止合并 |
| 安全扫描 | 依赖安全扫描 | {{security_scan_timeout}} | 警告 |

### 3.3 CD 流程

**触发条件**:
- 代码合并到 {{main_branch}} 分支
- 创建 Git Tag
- 手动触发

**CD 流程**:
```
{{cd_pipeline_diagram}}
```

**CD 配置文件**: `.{{cd_config_file}}`

```{{cd_config_language}}
{{cd_config_content}}
```

**CD 阶段**:
| 阶段 | 任务 | 环境 | 超时时间 |
|------|------|------|----------|
| 预发部署 | 部署到预发环境 | Staging | {{staging_deploy_timeout}} |
| 预发测试 | 运行预发测试 | Staging | {{staging_test_timeout}} |
| 生产部署 | 部署到生产环境 | Production | {{prod_deploy_timeout}} |
| 生产验证 | 运行生产验证 | Production | {{prod_verify_timeout}} |

### 3.4 发布策略

**发布方式**: {{release_strategy}}（蓝绿部署/金丝雀发布/滚动更新）

**蓝绿部署**:
```
{{blue_green_deployment_diagram}}
```

**金丝雀发布**:
```
{{canary_deployment_diagram}}
```

**发布流程**:
1. {{release_step_1}}
2. {{release_step_2}}
3. {{release_step_3}}
4. {{release_step_4}}

**回滚流程**:
1. {{rollback_step_1}}
2. {{rollback_step_2}}
3. {{rollback_step_3}}

---

## 4. 容器化配置

### 4.1 Docker 配置

**Dockerfile**:

```dockerfile
{{dockerfile_content}}
```

**多阶段构建**:
```dockerfile
{{multi_stage_dockerfile}}
```

**最佳实践**:
- 使用非 root 用户运行
- 多阶段构建减小镜像体积
- 使用 .dockerignore 排除不必要文件
- 使用具体版本号而非 latest 标签

**构建命令**:
```bash
docker build -t {{image_name}}:{{version}} .
docker tag {{image_name}}:{{version}} {{registry_url}}/{{image_name}}:{{version}}
docker push {{registry_url}}/{{image_name}}:{{version}}
```

### 4.2 Kubernetes 配置

**Deployment 配置**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{app_name}}
  namespace: {{namespace}}
spec:
  replicas: {{replicas}}
  selector:
    matchLabels:
      app: {{app_name}}
  template:
    metadata:
      labels:
        app: {{app_name}}
    spec:
      containers:
      - name: {{container_name}}
        image: {{image_name}}:{{version}}
        ports:
        - containerPort: {{container_port}}
        env:
        - name: {{env_var_1}}
          valueFrom:
            secretKeyRef:
              name: {{secret_name}}
              key: {{secret_key}}
        resources:
          requests:
            memory: "{{memory_request}}"
            cpu: "{{cpu_request}}"
          limits:
            memory: "{{memory_limit}}"
            cpu: "{{cpu_limit}}"
        livenessProbe:
          httpGet:
            path: {{health_check_path}}
            port: {{health_check_port}}
          initialDelaySeconds: {{liveness_initial_delay}}
          periodSeconds: {{liveness_period}}
        readinessProbe:
          httpGet:
            path: {{readiness_check_path}}
            port: {{readiness_check_port}}
          initialDelaySeconds: {{readiness_initial_delay}}
          periodSeconds: {{readiness_period}}
```

**Service 配置**:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{service_name}}
  namespace: {{namespace}}
spec:
  type: {{service_type}}
  selector:
    app: {{app_name}}
  ports:
  - port: {{service_port}}
    targetPort: {{container_port}}
    protocol: TCP
```

**ConfigMap 配置**:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{configmap_name}}
  namespace: {{namespace}}
data:
  {{config_file}}: |
    {{config_content}}
```

**Secret 配置**:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{secret_name}}
  namespace: {{namespace}}
type: Opaque
data:
  {{secret_key_1}}: {{secret_value_1_base64}}
  {{secret_key_2}}: {{secret_value_2_base64}}
```

**Helm Chart 目录结构**:

```
helm-chart/
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-staging.yaml
├── values-prod.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── configmap.yaml
    ├── secret.yaml
    └── ingress.yaml
```

**部署命令**:
```bash
helm upgrade --install {{release_name}} ./helm-chart \
  --namespace {{namespace}} \
  --values values-{{env}}.yaml \
  --set image.tag={{version}}
```

---

## 5. 部署步骤与验证

### 5.1 首次部署

#### 前置准备

**环境检查**:
- [ ] {{check_1}}
- [ ] {{check_2}}
- [ ] {{check_3}}

**依赖服务**:
- [ ] {{dependency_1}} 已启动
- [ ] {{dependency_2}} 已启动
- [ ] {{dependency_3}} 已启动

#### 部署步骤

**步骤 1: 准备配置文件**
```bash
cp config/production.example.yaml config/production.yaml
vi config/production.yaml
```

**步骤 2: 构建镜像**
```bash
docker build -t {{image_name}}:{{version}} .
docker tag {{image_name}}:{{version}} {{registry_url}}/{{image_name}}:{{version}}
docker push {{registry_url}}/{{image_name}}:{{version}}
```

**步骤 3: 部署应用**
```bash
kubectl apply -f k8s/
kubectl rollout status deployment/{{app_name}} -n {{namespace}}
```

**步骤 4: 验证部署**
```bash
kubectl get pods -n {{namespace}}
kubectl logs -f deployment/{{app_name}} -n {{namespace}}
```

### 5.2 日常部署

**部署流程**:
```bash
# 1. 拉取最新代码
git pull origin {{main_branch}}

# 2. 更新版本号
vi package.json  # 或其他版本文件

# 3. 构建并推送镜像
docker build -t {{image_name}}:{{new_version}} .
docker push {{registry_url}}/{{image_name}}:{{new_version}}

# 4. 更新部署
kubectl set image deployment/{{app_name}} \
  {{container_name}}={{registry_url}}/{{image_name}}:{{new_version}} \
  -n {{namespace}}

# 5. 等待部署完成
kubectl rollout status deployment/{{app_name}} -n {{namespace}}
```

**验证清单**:
- [ ] Pod 状态为 Running
- [ ] 健康检查通过
- [ ] 日志无错误
- [ ] API 响应正常
- [ ] 监控指标正常

### 5.3 紧急回滚

**回滚到上一个版本**:
```bash
kubectl rollout undo deployment/{{app_name}} -n {{namespace}}
```

**回滚到指定版本**:
```bash
kubectl rollout undo deployment/{{app_name}} --to-revision={{revision}} -n {{namespace}}
```

**验证回滚**:
```bash
kubectl get pods -n {{namespace}}
kubectl logs -f deployment/{{app_name}} -n {{namespace}}
```

---

## 6. 监控告警体系

### 6.1 监控架构

**监控工具**:
- 指标采集: {{metrics_tool}}（Prometheus/CloudWatch）
- 可视化: {{visualization_tool}}（Grafana）
- 日志收集: {{log_tool}}（ELK Stack/CloudWatch Logs）
- 链路追踪: {{tracing_tool}}（Jaeger/Zipkin）

### 6.2 关键指标

**系统指标**:
| 指标 | 阈值 | 告警级别 | 通知方式 |
|------|------|----------|----------|
| CPU 使用率 | {{cpu_threshold}} | {{cpu_alert_level}} | {{cpu_notification}} |
| 内存使用率 | {{memory_threshold}} | {{memory_alert_level}} | {{memory_notification}} |
| 磁盘使用率 | {{disk_threshold}} | {{disk_alert_level}} | {{disk_notification}} |
| 网络流量 | {{network_threshold}} | {{network_alert_level}} | {{network_notification}} |

**应用指标**:
| 指标 | 阈值 | 告警级别 | 通知方式 |
|------|------|----------|----------|
| 请求响应时间 | {{response_time_threshold}} | {{response_time_alert_level}} | {{response_time_notification}} |
| 错误率 | {{error_rate_threshold}} | {{error_rate_alert_level}} | {{error_rate_notification}} |
| QPS | {{qps_threshold}} | {{qps_alert_level}} | {{qps_notification}} |
| 并发连接数 | {{connection_threshold}} | {{connection_alert_level}} | {{connection_notification}} |

**业务指标**:
| 指标 | 阈值 | 告警级别 | 通知方式 |
|------|------|----------|----------|
| {{business_metric_1}} | {{business_threshold_1}} | {{business_alert_level_1}} | {{business_notification_1}} |
| {{business_metric_2}} | {{business_threshold_2}} | {{business_alert_level_2}} | {{business_notification_2}} |

### 6.3 Prometheus 配置

**Prometheus 配置文件**: `prometheus.yml`

```yaml
global:
  scrape_interval: {{scrape_interval}}
  evaluation_interval: {{evaluation_interval}}

scrape_configs:
  - job_name: '{{job_name}}'
    static_configs:
      - targets: ['{{target_1}}', '{{target_2}}']
    metrics_path: {{metrics_path}}
    scrape_interval: {{scrape_interval}}

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['{{alertmanager_target}}']

rule_files:
  - '{{rule_file}}'
```

**告警规则文件**: `alerts.yml`

```yaml
groups:
  - name: {{alert_group_name}}
    rules:
      - alert: {{alert_name}}
        expr: {{alert_expression}}
        for: {{alert_for_duration}}
        labels:
          severity: {{alert_severity}}
        annotations:
          summary: "{{alert_summary}}"
          description: "{{alert_description}}"
```

### 6.4 Grafana 仪表盘

**仪表盘配置**: `grafana-dashboard.json`

```json
{{grafana_dashboard_config}}
```

**关键仪表盘**:
- 系统概览仪表盘
- 应用性能仪表盘
- 业务指标仪表盘
- 错误分析仪表盘

### 6.5 告警通知

**通知渠道**:
- 邮件: {{email_notification}}
- 企业微信: {{wechat_notification}}
- 钉钉: {{dingtalk_notification}}
- Slack: {{slack_notification}}
- 短信: {{sms_notification}}

**告警级别**:
- P0（严重）: 立即通知所有相关人员
- P1（高）: 通知值班人员
- P2（中）: 记录日志，定时汇总
- P3（低）: 仅记录日志

**值班表**:
| 日期 | 值班人 | 联系方式 | 备用联系人 |
|------|--------|----------|------------|
| {{date_1}} | {{on_call_1}} | {{contact_1}} | {{backup_1}} |
| {{date_2}} | {{on_call_2}} | {{contact_2}} | {{backup_2}} |

---

## 7. 日志管理方案

### 7.1 日志收集架构

**日志收集工具**: {{log_collection_tool}}

**日志流程**:
```
{{log_flow_diagram}}
```

### 7.2 日志规范

**日志格式**:
```json
{
  "timestamp": "{{timestamp}}",
  "level": "{{log_level}}",
  "service": "{{service_name}}",
  "trace_id": "{{trace_id}}",
  "message": "{{log_message}}",
  "context": {
    "{{context_key_1}}": "{{context_value_1}}",
    "{{context_key_2}}": "{{context_value_2}}"
  }
}
```

**日志级别**:
- ERROR: 错误日志，需要立即处理
- WARN: 警告日志，需要关注
- INFO: 信息日志，记录关键操作
- DEBUG: 调试日志，开发调试使用

**日志保留策略**:
- ERROR 日志: 保留 {{error_log_retention}}
- WARN 日志: 保留 {{warn_log_retention}}
- INFO 日志: 保留 {{info_log_retention}}
- DEBUG 日志: 保留 {{debug_log_retention}}

### 7.3 ELK Stack 配置

**Logstash 配置**: `logstash.conf`

```conf
input {
  {{input_config}}
}

filter {
  {{filter_config}}
}

output {
  {{output_config}}
}
```

**Elasticsearch 索引策略**:
```json
{{elasticsearch_index_config}}
```

**Kibana 仪表盘**:
- 系统日志仪表盘
- 应用日志仪表盘
- 错误日志仪表盘
- 审计日志仪表盘

### 7.4 日志查询

**常用查询**:
```json
{{common_log_queries}}
```

**日志分析**:
- 错误趋势分析
- 性能瓶颈分析
- 用户行为分析
- 安全事件分析

---

## 8. 故障恢复流程

### 8.1 故障分级

| 级别 | 定义 | 响应时间 | 解决时间 |
|------|------|----------|----------|
| P0 | 系统完全不可用 | {{p0_response_time}} | {{p0_resolution_time}} |
| P1 | 核心功能不可用 | {{p1_response_time}} | {{p1_resolution_time}} |
| P2 | 部分功能受影响 | {{p2_response_time}} | {{p2_resolution_time}} |
| P3 | 轻微影响 | {{p3_response_time}} | {{p3_resolution_time}} |

### 8.2 故障处理流程

**故障发现**:
- 监控告警
- 用户反馈
- 主动巡检

**故障响应**:
1. 确认故障级别
2. 通知相关人员
3. 创建故障工单
4. 启动应急响应

**故障排查**:
1. 查看监控指标
2. 检查日志
3. 复现问题
4. 定位根因

**故障修复**:
1. 实施临时方案
2. 验证修复效果
3. 实施永久方案
4. 验证系统稳定

**故障复盘**:
1. 编写故障报告
2. 分析根因
3. 制定改进措施
4. 更新文档和流程

### 8.3 常见故障处理

**数据库故障**:
```bash
# 检查数据库状态
kubectl get pods -n {{namespace}} | grep {{database_name}}

# 查看数据库日志
kubectl logs -f {{database_pod_name}} -n {{namespace}}

# 重启数据库
kubectl rollout restart deployment/{{database_deployment_name}} -n {{namespace}}
```

**应用故障**:
```bash
# 检查应用状态
kubectl get pods -n {{namespace}} | grep {{app_name}}

# 查看应用日志
kubectl logs -f {{app_pod_name}} -n {{namespace}}

# 重启应用
kubectl rollout restart deployment/{{app_name}} -n {{namespace}}
```

**网络故障**:
```bash
# 检查网络连接
kubectl exec -it {{pod_name}} -n {{namespace}} -- ping {{target_host}}

# 检查 DNS 解析
kubectl exec -it {{pod_name}} -n {{namespace}} -- nslookup {{target_host}}

# 检查 Service
kubectl get svc -n {{namespace}}
kubectl describe svc {{service_name}} -n {{namespace}}
```

---

## 9. 扩缩容策略

### 9.1 自动扩缩容

**HPA 配置**:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{hpa_name}}
  namespace: {{namespace}}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{app_name}}
  minReplicas: {{min_replicas}}
  maxReplicas: {{max_replicas}}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: {{cpu_target_utilization}}
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: {{memory_target_utilization}}
```

**扩缩容策略**:
| 指标 | 触发条件 | 扩容动作 | 缩容动作 |
|------|----------|----------|----------|
| CPU 使用率 | > {{cpu_scale_up_threshold}}% | +{{cpu_scale_up_replicas}} | -{{cpu_scale_down_replicas}} |
| 内存使用率 | > {{memory_scale_up_threshold}}% | +{{memory_scale_up_replicas}} | -{{memory_scale_down_replicas}} |
| QPS | > {{qps_scale_up_threshold}} | +{{qps_scale_up_replicas}} | -{{qps_scale_down_replicas}} |

### 9.2 手动扩缩容

**扩容命令**:
```bash
kubectl scale deployment/{{app_name}} --replicas={{new_replicas}} -n {{namespace}}
```

**缩容命令**:
```bash
kubectl scale deployment/{{app_name}} --replicas={{new_replicas}} -n {{namespace}}
```

### 9.3 预案扩缩容

**高峰期预案**:
- 时间: {{peak_time}}
- 预期流量: {{expected_traffic}}
- 扩容策略: {{scale_up_strategy}}

**低峰期预案**:
- 时间: {{off_peak_time}}
- 预期流量: {{expected_traffic}}
- 缩容策略: {{scale_down_strategy}}

---

## 10. 备份与恢复

### 10.1 备份策略

**备份类型**:
- 全量备份: {{full_backup_schedule}}
- 增量备份: {{incremental_backup_schedule}}
- 差异备份: {{differential_backup_schedule}}

**备份对象**:
- 数据库: {{database_backup}}
- 配置文件: {{config_backup}}
- 日志文件: {{log_backup}}
- 代码仓库: {{code_backup}}

**备份保留**:
- 每日备份: 保留 {{daily_retention}}
- 每周备份: 保留 {{weekly_retention}}
- 每月备份: 保留 {{monthly_retention}}

### 10.2 备份执行

**数据库备份**:
```bash
# 备份数据库
kubectl exec -it {{database_pod_name}} -n {{namespace}} -- \
  mysqldump -u {{username}} -p{{password}} {{database_name}} > backup_{{date}}.sql

# 上传到对象存储
aws s3 cp backup_{{date}}.sql s3://{{bucket_name}}/backups/
```

**配置备份**:
```bash
# 备份配置
kubectl get configmap -n {{namespace}} -o yaml > configmap_backup_{{date}}.yaml
kubectl get secret -n {{namespace}} -o yaml > secret_backup_{{date}}.yaml

# 上传到对象存储
aws s3 cp configmap_backup_{{date}}.yaml s3://{{bucket_name}}/backups/
aws s3 cp secret_backup_{{date}}.yaml s3://{{bucket_name}}/backups/
```

### 10.3 恢复流程

**数据库恢复**:
```bash
# 下载备份文件
aws s3 cp s3://{{bucket_name}}/backups/backup_{{date}}.sql .

# 恢复数据库
kubectl exec -i {{database_pod_name}} -n {{namespace}} -- \
  mysql -u {{username}} -p{{password}} {{database_name}} < backup_{{date}}.sql
```

**配置恢复**:
```bash
# 下载备份文件
aws s3 cp s3://{{bucket_name}}/backups/configmap_backup_{{date}}.yaml .
aws s3 cp s3://{{bucket_name}}/backups/secret_backup_{{date}}.yaml .

# 恢复配置
kubectl apply -f configmap_backup_{{date}}.yaml
kubectl apply -f secret_backup_{{date}}.yaml
```

---

## 11. 安全策略

### 11.1 访问控制

**RBAC 配置**:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: {{role_name}}
  namespace: {{namespace}}
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
```

**权限矩阵**:
| 角色 | 权限 | 范围 |
|------|------|------|
| {{role_1}} | {{permission_1}} | {{scope_1}} |
| {{role_2}} | {{permission_2}} | {{scope_2}} |

### 11.2 网络安全

**Network Policy 配置**:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {{network_policy_name}}
  namespace: {{namespace}}
spec:
  podSelector:
    matchLabels:
      app: {{app_name}}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: {{allowed_namespace}}
    ports:
    - protocol: TCP
      port: {{allowed_port}}
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: {{allowed_namespace}}
    ports:
    - protocol: TCP
      port: {{allowed_port}}
```

### 11.3 镜像安全

**镜像扫描**:
```bash
# 扫描镜像漏洞
trivy image {{image_name}}:{{version}}

# 扫描报告
trivy image --format json --output scan_report.json {{image_name}}:{{version}}
```

**镜像签名**:
```bash
# 签名镜像
cosign sign {{registry_url}}/{{image_name}}:{{version}}

# 验证签名
cosign verify {{registry_url}}/{{image_name}}:{{version}}
```

---

## 12. 附录

### 12.1 常用命令

**Pod 操作**:
```bash
# 查看 Pod
kubectl get pods -n {{namespace}}

# 查看 Pod 详情
kubectl describe pod {{pod_name}} -n {{namespace}}

# 查看 Pod 日志
kubectl logs {{pod_name}} -n {{namespace}}

# 进入 Pod
kubectl exec -it {{pod_name}} -n {{namespace}} -- /bin/bash

# 删除 Pod
kubectl delete pod {{pod_name}} -n {{namespace}}
```

**Service 操作**:
```bash
# 查看 Service
kubectl get svc -n {{namespace}}

# 查看 Service 详情
kubectl describe svc {{service_name}} -n {{namespace}}

# 删除 Service
kubectl delete svc {{service_name}} -n {{namespace}}
```

**Deployment 操作**:
```bash
# 查看 Deployment
kubectl get deployment -n {{namespace}}

# 查看 Deployment 详情
kubectl describe deployment {{deployment_name}} -n {{namespace}}

# 扩容
kubectl scale deployment {{deployment_name}} --replicas={{replicas}} -n {{namespace}}

# 重启
kubectl rollout restart deployment {{deployment_name}} -n {{namespace}}

# 回滚
kubectl rollout undo deployment {{deployment_name}} -n {{namespace}}
```

### 12.2 联系方式

| 角色 | 姓名 | 联系方式 | 负责范围 |
|------|------|----------|----------|
| DevOps 负责人 | {{devops_lead}} | {{devops_contact}} | 整体运维 |
| SRE 工程师 | {{sre_engineer}} | {{sre_contact}} | 系统稳定性 |
| 后端负责人 | {{backend_lead}} | {{backend_contact}} | 应用部署 |
| DBA | {{dba}} | {{dba_contact}} | 数据库运维 |

### 12.3 相关文档

- [系统架构文档]({{architecture_doc_link}})
- [API 文档]({{api_doc_link}})
- [测试策略文档]({{test_strategy_doc_link}})
- [安全合规文档]({{security_doc_link}})

---

**文档变更历史**:

| 版本 | 日期 | 变更内容 | 变更人 |
|------|------|----------|--------|
| 1.0.0 | {{creation_date}} | 初始版本 | {{author}} |
