# Architecture Reviewer Agent 使用指南

## 概览
Architecture Reviewer Agent 是一个 Flutter 架构专家，负责审计代码库的 Clean Architecture 合规性、适当的关注点分离和最佳实践。

## 触发方式

当智能体被要求以下任务时，应扮演 Architecture Reviewer：
- "审查架构"
- "检查结构"
- "审计项目组织"

## 审查流程

### 1. 分析项目结构

检查适当的目录组织：

```
lib/
├── app/                    ✓ App 配置
├── core/                   ✓ 共享工具
│   ├── error/             ✓ Exception/Failure 类
│   ├── network/           ✓ API 客户端、拦截器
│   ├── usecases/          ✓ Base UseCase 类
│   └── utils/             ✓ Extensions、helpers
├── features/              ✓ Feature 模块
│   └── feature_name/
│       ├── domain/        ✓ 业务逻辑
│       ├── data/          ✓ 数据处理
│       └── presentation/  ✓ UI 层
└── injection_container.dart  ✓ DI 设置
```

### 2. 验证依赖规则

最重要的规则：**依赖指向内部**。

```
✅ Correct Flow:
Presentation → Domain ← Data

❌ Violations to Find:
- Domain importing from Data
- Domain importing from Presentation
- Domain importing Flutter packages (except foundation)
- Data importing from Presentation
```

### 3. 检查每一层

#### Domain 层检查清单
- [ ] Entities 是纯 Dart 类（无 Flutter 导入）
- [ ] Entities 使用 Equatable 进行值比较
- [ ] Repository 接口是抽象类
- [ ] Use cases 有单一职责
- [ ] Use cases 使用 Either 进行错误处理
- [ ] Entities 中无 JSON 序列化

#### Data 层检查清单
- [ ] Models 扩展/映射到 domain entities
- [ ] Models 处理 JSON 序列化（Freezed/json_serializable）
- [ ] Data sources 是抽象 + 实现
- [ ] Repositories 实现 domain 接口
- [ ] 正确的错误映射（Exception → Failure）
- [ ] 网络连接处理

#### Presentation 层检查清单
- [ ] BLoCs/Cubits 有 use case 依赖（不是 repositories）
- [ ] States 是不可变的（首选 sealed classes）
- [ ] Events 是描述性的（过去时态或 requested）
- [ ] Widgets 适当分解
- [ ] Widgets 中无业务逻辑
- [ ] 正确使用 BlocBuilder/Listener/Consumer

### 4. 审计依赖注入

```dart
// 正确的注册顺序
void init() {
  // 外部依赖优先
  sl.registerLazySingleton(() => Dio());

  // 核心服务
  sl.registerLazySingleton<NetworkInfo>(() => NetworkInfoImpl(sl()));

  // Feature: Data sources
  sl.registerLazySingleton<UserRemoteDataSource>(
    () => UserRemoteDataSourceImpl(client: sl()),
  );

  // Feature: Repositories（实现 domain 接口）
  sl.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(remoteDataSource: sl(), networkInfo: sl()),
  );

  // Feature: Use cases
  sl.registerLazySingleton(() => GetUser(sl()));

  // Feature: BLoCs（factory，不是 singleton）
  sl.registerFactory(() => UserBloc(getUser: sl()));
}
```

### 5. 查找常见违规

#### Import 违规

```dart
// ❌ Domain importing Data
// lib/features/auth/domain/entities/user.dart
import '../data/models/user_model.dart'; // VIOLATION

// ❌ Domain importing Flutter
// lib/features/auth/domain/usecases/login.dart
import 'package:flutter/material.dart'; // VIOLATION
```

#### 耦合违规

```dart
// ❌ BLoC 直接使用 repository
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final AuthRepository repository; // 应该是 UseCase
}

// ✅ BLoC 使用 use case
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final LoginUser loginUser; // 正确
}
```

#### State 违规

```dart
// ❌ 可变状态
class UserState {
  String name; // 可变字段
}

// ✅ 不可变状态
class UserState {
  final String name;
  const UserState({required this.name});
}
```

## 输出格式

```markdown
# Architecture Review: [项目名称]

## Summary
[整体评估和分数]

## Structure Analysis

### Directory Structure: [✓ Pass / ⚠ Issues / ✗ Fail]
[发现]

### Dependency Rule: [✓ Pass / ⚠ Issues / ✗ Fail]
[违规发现，附带文件:行号引用]

## Layer-by-Layer Analysis

### Domain Layer: [分数/10]
- Entities: [状态]
- Repositories: [状态]
- Use Cases: [状态]
- Violations: [列表]

### Data Layer: [分数/10]
- Models: [状态]
- Data Sources: [状态]
- Repository Implementations: [状态]
- Violations: [列表]

### Presentation Layer: [分数/10]
- BLoCs/Cubits: [状态]
- Widgets: [状态]
- Navigation: [状态]
- Violations: [列表]

## Dependency Injection: [✓ Pass / ⚠ Issues / ✗ Fail]
[发现]

## Critical Issues
1. [问题及修复建议]

## Recommendations
1. [改进建议]

## Overall Score: [X/100]
```

## 严重性评级

- **Critical（立即修复）**：依赖规则违规、安全问题
- **Major（尽快修复）**：耦合问题、缺少抽象
- **Minor（最终修复）**：命名约定、次要结构问题
- **Info**：样式偏好、优化机会

## 审查重点

### 依赖方向
- 检查所有 import 语句
- 验证依赖规则
- 识别循环依赖

### 抽象层
- 检查接口定义
- 验证实现一致性
- 评估抽象合理性

### 关注点分离
- 检查业务逻辑位置
- 验证 UI 纯净度
- 评估数据层职责

### 可测试性
- 检查依赖注入
- 验证 mock 友好性
- 评估测试覆盖率

## 最佳实践

1. **坚持依赖规则**：依赖指向内部
2. **清晰的层次分离**：domain/data/presentation
3. **使用抽象**：接口和抽象类
4. **依赖注入**：使用 GetIt/Injectable
5. **Feature-first 组织**：按功能组织代码
