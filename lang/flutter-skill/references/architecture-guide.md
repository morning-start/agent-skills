# Flutter Architecture Guide

## 目录
- [Clean Architecture](#clean-architecture)
- [Feature Structure](#feature-structure)
- [BLoC Pattern](#bloc-pattern)
- [Error Handling](#error-handling)
- [Dependency Rule](#dependency-rule)

## 概览
本指南提供现代 Flutter 项目的完整架构规范，涵盖 Clean Architecture、Feature-First 组织方式、BLoC 状态管理和错误处理模式。

## Clean Architecture

### 核心原则
Clean Architecture 将代码分为三层，每层有明确的职责和依赖方向：

```
┌─────────────────────────────────────────┐
│              Presentation               │
│  (BLoC, Pages, Widgets)                 │
│                  │                      │
│                  ▼                      │
├─────────────────────────────────────────┤
│               Domain                    │
│  (Entities, Use Cases, Repositories)   │
│                  ▲                      │
│                  │                      │
├─────────────────────────────────────────┤
│                Data                     │
│  (Models, Data Sources, Repo Impl)     │
└─────────────────────────────────────────┘
```

### 依赖规则
1. **Domain** 层无依赖：纯 Dart 代码，不依赖其他层
2. **Data** 层实现 Domain 接口：通过抽象契约连接
3. **Presentation** 层依赖 Domain：不直接依赖 Data

### 项目结构

```
lib/
├── core/                           # 共享核心功能
│   ├── error/                      # 错误处理
│   │   ├── exceptions.dart         # 异常类
│   │   └── failures.dart           # 失败类
│   ├── network/                    # 网络层
│   │   ├── api_client.dart         # Dio 配置
│   │   └── network_info.dart       # 网络状态
│   ├── usecases/                   # 基础 UseCase
│   │   └── usecase.dart
│   └── utils/                      # 工具类
│       └── extensions.dart
│
├── features/                       # 功能模块
│   └── auth/                       # 示例功能
│       ├── domain/                 # 领域层
│       │   ├── entities/           # 实体
│       │   ├── repositories/       # 仓储接口
│       │   └── usecases/           # 用例
│       ├── data/                   # 数据层
│       │   ├── models/             # 数据模型
│       │   ├── datasources/        # 数据源
│       │   └── repositories/       # 仓储实现
│       └── presentation/           # 表现层
│           ├── bloc/               # BLoC
│           ├── pages/              # 页面
│           └── widgets/            # 组件
│
└── injection_container.dart        # 依赖注入
```

## Feature Structure

### Feature 模块布局

```
features/
└── auth/
    ├── domain/
    │   ├── entities/
    │   │   └── user.dart
    │   ├── repositories/
    │   │   └── auth_repository.dart
    │   └── usecases/
    │       ├── login_user.dart
    │       ├── logout_user.dart
    │       └── get_current_user.dart
    │
    ├── data/
    │   ├── models/
    │   │   └── user_model.dart
    │   ├── datasources/
    │   │   ├── auth_remote_datasource.dart
    │   │   └── auth_local_datasource.dart
    │   └── repositories/
    │       └── auth_repository_impl.dart
    │
    └── presentation/
        ├── bloc/
        │   ├── auth_bloc.dart
        │   ├── auth_event.dart
        │   └── auth_state.dart
        ├── pages/
        │   ├── login_page.dart
        │   └── register_page.dart
        └── widgets/
            └── login_form.dart
```

### 命名规范

**文件命名**（snake_case）：
- `user_model.dart` ✅
- `UserModel.dart` ❌

**类命名**（PascalCase）：
- Entity: `User`
- Model: `UserModel`
- UseCase: `LoginUser`, `GetCurrentUser`
- Repository: `AuthRepository`, `AuthRepositoryImpl`
- BLoC: `AuthBloc`
- Event: `LoginRequested`, `LogoutRequested`
- State: `AuthInitial`, `AuthLoading`, `AuthAuthenticated`
- Page: `LoginPage`, `ProfilePage`

## BLoC Pattern

### Events（输入）

使用 sealed class 定义事件，支持模式匹配：

```dart
sealed class AuthEvent {}

class LoginRequested extends AuthEvent {
  final String email;
  final String password;

  LoginRequested({required this.email, required this.password});
}

class LogoutRequested extends AuthEvent {}

class AuthCheckRequested extends AuthEvent {}
```

### States（输出）

使用 sealed class 定义状态：

```dart
sealed class AuthState {}

class AuthInitial extends AuthState {}

class AuthLoading extends AuthState {}

class AuthAuthenticated extends AuthState {
  final User user;
  AuthAuthenticated(this.user);
}

class AuthUnauthenticated extends AuthState {}

class AuthError extends AuthState {
  final String message;
  AuthError(this.message);
}
```

### BLoC 实现

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

part 'auth_event.dart';
part 'auth_state.dart';

class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final LoginUser loginUser;
  final LogoutUser logoutUser;

  AuthBloc({
    required this.loginUser,
    required this.logoutUser,
  }) : super(AuthInitial()) {
    on<LoginRequested>(_onLoginRequested);
    on<LogoutRequested>(_onLogoutRequested);
  }

  Future<void> _onLoginRequested(
    LoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());

    final result = await loginUser(
      LoginParams(email: event.email, password: event.password),
    );

    result.fold(
      (failure) => emit(AuthError(failure.message)),
      (user) => emit(AuthAuthenticated(user)),
    );
  }

  Future<void> _onLogoutRequested(
    LogoutRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());

    final result = await logoutUser(NoParams());

    result.fold(
      (failure) => emit(AuthError(failure.message)),
      (_) => emit(AuthUnauthenticated()),
    );
  }
}
```

### 在 Widget 中使用

```dart
BlocProvider(
  create: (context) => sl<AuthBloc>()..add(AuthCheckRequested()),
  child: const LoginPage(),
)

BlocBuilder<AuthBloc, AuthState>(
  builder: (context, state) => switch (state) {
    AuthInitial() => const SizedBox(),
    AuthLoading() => const CircularProgressIndicator(),
    AuthAuthenticated(:final user) => Text('Welcome, ${user.name}'),
    AuthUnauthenticated() => const LoginForm(),
    AuthError(:final message) => Text('Error: $message'),
  },
)
```

## Error Handling

### Exception 类（Data 层）

```dart
abstract class AppException implements Exception {
  final String message;
  final int? statusCode;

  const AppException({required this.message, this.statusCode});
}

class ServerException extends AppException {
  const ServerException({super.message = 'Server error occurred', super.statusCode});
}

class CacheException extends AppException {
  const CacheException({super.message = 'Cache error occurred'});
}
```

### Failure 类（Domain 层）

```dart
abstract class Failure extends Equatable {
  final String message;
  final int? code;

  const Failure({required this.message, this.code});

  @override
  List<Object?> get props => [message, code];
}

class ServerFailure extends Failure {
  const ServerFailure([String message = 'Server error occurred', int? code])
      : super(message: message, code: code);
}

class NetworkFailure extends Failure {
  const NetworkFailure([String message = 'No internet connection'])
      : super(message: message);
}

class CacheFailure extends Failure {
  const CacheFailure([String message = 'Cache error occurred'])
      : super(message: message);
}
```

### Either 模式使用

```dart
import 'package:dartz/dartz.dart';

abstract class AuthRepository {
  Future<Either<Failure, User>> login(String email, String password);
}

class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;

  AuthRepositoryImpl({required this.remoteDataSource});

  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    try {
      final userModel = await remoteDataSource.login(email, password);
      return Right(userModel.toEntity());
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message, e.statusCode));
    } catch (e) {
      return Left(const UnknownFailure());
    }
  }
}
```

## Dependency Rule

### 依赖方向
```
Presentation → Domain ← Data
     ↓           ↑        ↓
   BLoC ──→ UseCase ←── Repository
```

### 关键原则
- Domain 层不依赖任何其他层
- Data 层实现 Domain 定义的接口
- Presentation 层只依赖 Domain 层
- 使用依赖注入（GetIt）管理依赖关系

## 示例

### 创建实体

```dart
class User extends Equatable {
  final String id;
  final String email;
  final String name;

  const User({
    required this.id,
    required this.email,
    required this.name,
  });

  @override
  List<Object?> get props => [id, email, name];
}
```

### 创建 Repository 接口

```dart
abstract class AuthRepository {
  Future<Either<Failure, User>> login(String email, String password);
  Future<Either<Failure, void>> logout();
  Future<Either<Failure, User?>> getCurrentUser();
}
```

### 创建 UseCase

```dart
class LoginUser implements UseCase<User, LoginParams> {
  final AuthRepository repository;

  LoginUser(this.repository);

  @override
  Future<Either<Failure, User>> call(LoginParams params) {
    return repository.login(params.email, params.password);
  }
}
```


## Dependency Injection

### 概览
依赖注入（Dependency Injection）将对象创建与使用解耦，提高可测试性和灵活性。GetIt 是 Flutter 推荐的服务定位器，可选择使用 Injectable 进行代码生成。

### GetIt 设置（手动方式）

#### 安装
```yaml
dependencies:
  get_it: ^7.6.0
```

#### 服务定位器配置
```dart
// lib/injection_container.dart
import 'package:get_it/get_it.dart';
import 'package:dio/dio.dart';

final sl = GetIt.instance;

Future<void> init() async {
  //============================
  // 外部依赖
  //============================
  sl.registerLazySingleton(() => Dio()..options = BaseOptions(
    baseUrl: 'https://api.example.com',
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 30),
  ));

  //============================
  // 核心层
  //============================
  sl.registerLazySingleton<NetworkInfo>(
    () => NetworkInfoImpl(Connectivity()),
  );

  //============================
  // 功能层
  //============================
  await _initAuth();
  await _initUser();
}

Future<void> _initAuth() async {
  // BLoC - Factory（每次创建新实例）
  sl.registerFactory(
    () => AuthBloc(
      loginUser: sl(),
      logoutUser: sl(),
      getCurrentUser: sl(),
    ),
  );

  // Use Case - Lazy Singleton
  sl.registerLazySingleton(() => LoginUser(sl()));
  sl.registerLazySingleton(() => LogoutUser(sl()));

  // Repository - Lazy Singleton
  sl.registerLazySingleton<AuthRepository>(
    () => AuthRepositoryImpl(
      remoteDataSource: sl(),
      localDataSource: sl(),
      networkInfo: sl(),
    ),
  );

  // Data Source - Lazy Singleton
  sl.registerLazySingleton<AuthRemoteDataSource>(
    () => AuthRemoteDataSourceImpl(client: sl()),
  );
}
```

#### 注册类型

```dart
// Singleton - 始终返回同一实例
sl.registerSingleton(MySingleton());

// Lazy Singleton - 首次访问时创建
sl.registerLazySingleton(() => MyLazySingleton());

// Factory - 每次创建新实例
sl.registerFactory(() => MyFactory());

// 带参数的 Factory
sl.registerFactoryParam<MyService, String, int>(
  (param1, param2) => MyService(param1, param2),
);

// 异步 Singleton
sl.registerSingletonAsync<Database>(() async {
  final db = Database();
  await db.init();
  return db;
});
```

#### 在 main.dart 中初始化
```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await di.init();

  runApp(const MyApp());
}
```

#### 使用依赖
```dart
// 在 Widget 中
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => sl<AuthBloc>()..add(AuthCheckRequested()),
      child: const AuthView(),
    );
  }
}

// 在其他类中
class MyService {
  final UserRepository _userRepo = sl<UserRepository>();

  Future<User> getUser() => _userRepo.getUser();
}
```

### Injectable 设置（代码生成）

#### 安装
```yaml
dependencies:
  get_it: ^7.6.0
  injectable: ^2.3.0

dev_dependencies:
  injectable_generator: ^2.4.0
  build_runner: ^2.4.0
```

#### 配置 Injectable
```dart
// lib/injection_container.dart
import 'package:get_it/get_it.dart';
import 'package:injectable/injectable.dart';

import 'injection_container.config.dart';

final sl = GetIt.instance;

@InjectableInit()
Future<void> configureDependencies() async => sl.init();
```

#### 注解类
```dart
// Singleton
@lazySingleton
class UserRepository {
  final ApiClient _client;

  UserRepository(this._client);
}

// Factory
@injectable
class UserBloc extends Bloc<UserEvent, UserState> {
  final GetUser _getUser;

  UserBloc(this._getUser) : super(UserInitial());
}
```

### 依赖注入最佳实践

1. **使用 GetIt 手动注册**：适合小型项目，灵活控制
2. **使用 Injectable 代码生成**：适合中大型项目，减少样板代码
3. **分层注册**：按照 Core、Features 分组注册
4. **单例 vs Factory**：
   - Repository、UseCase 用 Lazy Singleton
   - BLoC 用 Factory（每次创建新实例）
5. **异步依赖**：使用 registerSingletonAsync 处理异步初始化
