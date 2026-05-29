# Protobuf 使用指南

## 概览
Protocol Buffers（简称 Protobuf）是 Google 开发的一种语言无关、平台无关的序列化协议，用于结构化数据的序列化和反序列化。相比 JSON/XML，Protobuf 具有更小的体积和更快的解析速度。

---

## 基本语法

### 文件结构
```protobuf
syntax = "proto3";  // 指定 proto 版本

package com.example.protocol;  // 包名（防止命名冲突）

// 导入其他 proto 文件
import "common.proto";

// 选项
option java_package = "com.example.protocol";
option java_outer_classname = "UserProtos";
```

### 消息定义
```protobuf
message User {
  int32 user_id = 1;        // 字段编号、类型、名称
  string username = 2;
  string email = 3;
  bool is_active = 4;
}
```

### 枚举定义
```protobuf
enum UserStatus {
  UNKNOWN = 0;    // 第一个值必须为 0（默认值）
  ACTIVE = 1;
  INACTIVE = 2;
  DELETED = 3;
}
```

### 嵌套消息
```protobuf
message User {
  int32 id = 1;
  string name = 2;
  Address address = 3;  // 嵌套消息
}

message Address {
  string city = 1;
  string street = 2;
}
```

---

## 数据类型

| Protobuf 类型 | 说明 | Java 类型 | Python 类型 | Go 类型 |
|---------------|------|-----------|-------------|---------|
| double | 双精度浮点数 | double | float | float64 |
| float | 单精度浮点数 | float | float | float32 |
| int32 | 32 位整数 | int | int | int32 |
| int64 | 64 位整数 | long | int/long | int64 |
| uint32 | 无符号 32 位整数 | int | int | uint32 |
| uint64 | 无符号 64 位整数 | long | int/long | uint64 |
| bool | 布尔值 | boolean | bool | bool |
| string | 字符串 | String | str | string |
| bytes | 字节序列 | ByteString | bytes | []byte |

---

## 字段规则

### 必填 / 可选（proto3 默认）
```protobuf
message User {
  int32 id = 1;           // 可选（默认值：0）
  string name = 2;        // 可选（默认值：""）
  bool active = 3;        // 可选（默认值：false）
}
```

### 重复字段（数组）
```protobuf
message User {
  repeated string tags = 1;  // 字符串数组
  repeated int32 scores = 2; // 整数数组
}
```

### Map 类型
```protobuf
message User {
  map<string, string> metadata = 1;  // 字符串到字符串的映射
  map<int32, int32> scores = 2;     // 整数到整数的映射
}
```

---

## 字段编号规则

### 编号范围
| 编号范围 | 编码方式 | 说明 |
|----------|----------|------|
| 1-15 | 1 字节 | 常用字段（推荐优先使用） |
| 16-2047 | 2 字节 | 不常用字段 |
| 19000-1999 | 保留 | 禁止使用 |

### 编号示例
```protobuf
message User {
  int32 id = 1;           // 常用字段（1 字节）
  string name = 2;        // 常用字段（1 字节）
  string email = 3;       // 常用字段（1 字节）
  // ... 其他字段
  string nickname = 16;   // 不常用字段（2 字节）
}
```

### 删除字段
```protobuf
message User {
  int32 id = 1;
  string name = 2;
  reserved 3;            // 保留字段编号 3（不能被其他字段使用）
  string email = 4;      // 新字段使用编号 4
}
```

---

## 向前/向后兼容

### 添加字段（向前兼容）
```protobuf
// 版本 1
message User {
  int32 id = 1;
  string name = 2;
}

// 版本 2（添加新字段）
message User {
  int32 id = 1;
  string name = 2;
  string email = 3;  // 新增字段，旧版本忽略
}
```

### 删除字段（向后兼容）
```protobuf
// 版本 1
message User {
  int32 id = 1;
  string name = 2;
  string email = 3;
}

// 版本 2（删除字段）
message User {
  int32 id = 1;
  string name = 2;
  reserved 3;           // 保留字段编号
  reserved "email";     // 保留字段名
}
```

### 修改字段类型（不兼容）
```protobuf
// ❌ 错误：修改字段类型会导致不兼容
message User {
  int32 id = 1;
  string name = 2;      // 从 int32 改为 string（不兼容）
}
```

---

## 常用选项

### Java 选项
```protobuf
option java_package = "com.example.protocol";         // Java 包名
option java_outer_classname = "UserProtos";            // Java 外部类名
option java_multiple_files = true;                     // 每个消息一个文件
```

### Go 选项
```protobuf
option go_package = "github.com/example/protocol";     // Go 包路径
```

### 消息选项
```protobuf
message User {
  option message_set_wire_format = true;               // MessageSet 格式
  option no_standard_descriptor_accessor = false;      // 禁用描述符访问器
}
```

---

## 代码生成

### 安装 protoc
```bash
# macOS
brew install protobuf

# Ubuntu/Debian
apt-get install protobuf-compiler

# Windows
# 下载：https://github.com/protocolbuffers/protobuf/releases
```

### 安装语言插件
```bash
# Go 插件
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest

# Python 插件
pip install grpcio-tools

# Java 插件（内置，无需额外安装）
```

### 生成代码
```bash
# 生成 Go 代码
protoc --go_out=. --go_opt=paths=source_relative \
       user.proto

# 生成 Python 代码
protoc --python_out=. user.proto

# 生成 Java 代码
protoc --java_out=. user.proto

# 生成 C++ 代码
protoc --cpp_out=. user.proto
```

---

## 使用示例

### Java
```java
// 创建消息
User user = User.newBuilder()
    .setId(1001)
    .setName("张三")
    .setEmail("test@example.com")
    .build();

// 序列化为字节
byte[] data = user.toByteArray();

// 反序列化
User parsedUser = User.parseFrom(data);
System.out.println(parsedUser.getName());
```

### Python
```python
# 创建消息
user = user_pb2.User()
user.id = 1001
user.name = "张三"
user.email = "test@example.com"

# 序列化为字节
data = user.SerializeToString()

# 反序列化
parsed_user = user_pb2.User()
parsed_user.ParseFromString(data)
print(parsed_user.name)
```

### Go
```go
// 创建消息
user := &User{
    Id:    1001,
    Name:  "张三",
    Email: "test@example.com",
}

// 序列化为字节
data, err := proto.Marshal(user)
if err != nil {
    log.Fatal(err)
}

// 反序列化
parsedUser := &User{}
err = proto.Unmarshal(data, parsedUser)
if err != nil {
    log.Fatal(err)
}
fmt.Println(parsedUser.Name)
```

---

## 最佳实践

1. **字段编号分配**：1-15 留给最常用的字段
2. **预留字段编号**：为未来扩展预留部分编号
3. **删除字段**：使用 `reserved` 保留字段编号和名称
4. **枚举默认值**：第一个枚举值必须为 0
5. **包名规范**：使用反向域名（如 com.example.protocol）
6. **文件命名**：使用小写字母和下划线（如 user.proto）
7. **版本控制**：使用 Git 管理 .proto 文件

---

## 常见问题

### Q: 如何处理可空字段？
A: 使用 optional 关键字（proto3 新增）：
```protobuf
syntax = "proto3";
message User {
  optional string email = 3;  // 可为 null
}
```

### Q: 如何定义重复字段？
A: 使用 `repeated` 关键字：
```protobuf
message User {
  repeated string tags = 1;  // 字符串数组
}
```

### Q: 如何嵌套消息？
A: 直接定义嵌套消息或引用其他消息：
```protobuf
message User {
  int32 id = 1;
  Address address = 2;  // 嵌套消息
}

message Address {
  string city = 1;
  string street = 2;
}
```

### Q: 如何处理枚举？
A: 使用 `enum` 定义，第一个值必须为 0：
```protobuf
enum UserStatus {
  UNKNOWN = 0;  // 默认值
  ACTIVE = 1;
  INACTIVE = 2;
}
```
