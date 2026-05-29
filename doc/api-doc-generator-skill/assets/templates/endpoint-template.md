# {{ENDPOINT_NAME}}

## 基本信息

- **方法**：{{METHOD}}
- **路径**：`{{PATH}}`
- **描述**：{{DESCRIPTION}}
- **功能**：{{FUNCTION}}

## 请求

### 请求头

```
Content-Type: application/json
Authorization: Bearer {{API_KEY}}
```

### 路径参数

{{#if PATH_PARAMS}}
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
{{PATH_PARAMS_TABLE}}
{{else}}
无
{{/if}}

### 查询参数

{{#if QUERY_PARAMS}}
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
{{QUERY_PARAMS_TABLE}}
{{else}}
无
{{/if}}

### 请求体

{{#if BODY_PARAMS}}
```json
{
{{BODY_PARAMS_JSON}}
}
```

**请求体参数说明**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
{{BODY_PARAMS_TABLE}}
{{else}}
无
{{/if}}

---

## 前端组件文档

### 组件名称

{{COMPONENT_NAME}}

### 组件描述

{{COMPONENT_DESCRIPTION}}

### Props

| Prop | Type | Default | Required | Description |
| ----- | ------ | ------- | -------- | ----------------- |
{{PROPS_TABLE}}

### Events

| Event | Payload | Description |
|-------|---------|-------------|
{{EVENTS_TABLE}}

### Slots

| Slot | Description |
|------|-------------|
{{SLOTS_TABLE}}

### 使用示例

#### 基础用法

```jsx
import { {{COMPONENT_NAME}} } from '{{PROJECT_NAME}}';

function Example() {
  return (
    <{{COMPONENT_NAME}}
      {{#if PROPS_EXAMPLE}}
      {{PROPS_EXAMPLE}}
      {{/if}}
    >
      {{#if DEFAULT_CHILDREN}}
      {{DEFAULT_CHILDREN}}
      {{/if}}
    </{{COMPONENT_NAME}}>
  );
}
```

#### 高级用法

```jsx
import { {{COMPONENT_NAME}} } from '{{PROJECT_NAME}}';

function AdvancedExample() {
  const [value, setValue] = useState('');

  return (
    <{{COMPONENT_NAME}}
      {{#if PROPS_EXAMPLE}}
      {{PROPS_EXAMPLE}}
      {{/if}}
      {{#if EVENTS_EXAMPLE}}
      {{EVENTS_EXAMPLE}}
      {{/if}}
    >
      {{#if DEFAULT_CHILDREN}}
      {{DEFAULT_CHILDREN}}
      {{/if}}
    </{{COMPONENT_NAME}}>
  );
}
```

### TypeScript 类型定义

```typescript
interface {{COMPONENT_NAME}}Props {
  {{#if TYPESCRIPT_TYPES}}
  {{TYPESCRIPT_TYPES}}
  {{/if}}
}

declare const {{COMPONENT_NAME}}: React.FC<{{COMPONENT_NAME}}Props>;
```

---

## 请求示例

### cURL

```bash
curl -X {{METHOD}} {{BASE_URL}}{{PATH}} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
{{#if BODY_PARAMS}}
  -d '{
{{REQUEST_BODY_EXAMPLE}}
  }'
{{else}}
{{/if}}
```

### JavaScript (Fetch)

```javascript
fetch('{{BASE_URL}}{{PATH}}', {
  method: '{{METHOD}}',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  }{{#if BODY_PARAMS}},
  body: JSON.stringify({
{{REQUEST_BODY_EXAMPLE}}
  })
{{/if}}
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Python (Requests)

```python
import requests

url = '{{BASE_URL}}{{PATH}}'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
}
{{#if BODY_PARAMS}}
data = {
{{REQUEST_BODY_EXAMPLE}}
}
response = requests.{{METHOD.lower()}}(url, headers=headers, json=data)
{{else}}
response = requests.{{METHOD.lower()}}(url, headers=headers)
{{/if}}
result = response.json()
print(result)
```

## 响应

### 成功响应

**状态码**：200 OK

```json
{
{{SUCCESS_RESPONSE}}
}
```

### 错误响应

**状态码**：400 Bad Request

```json
{
  "error": {
    "code": "{{ERROR_CODE}}",
    "message": "{{ERROR_MESSAGE}}",
    "details": {}
  }
}
```

## 响应参数说明

| 参数名 | 类型 | 说明 |
|--------|------|------|
{{RESPONSE_PARAMS_TABLE}}

## 状态码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 注意事项

1. {{NOTE_1}}
2. {{NOTE_2}}
3. {{NOTE_3}}

## 相关端点

- {{RELATED_ENDPOINT_1}}
- {{RELATED_ENDPOINT_2}}
