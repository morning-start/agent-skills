---
name: clean-architecture
description: Domain/Data/Presentation layers with dependency rule enforcement. Use when structuring new features, organizing code, or when user asks about "clean architecture", "layers", or "separation of concerns".
---

# Clean Architecture

## Overview

Clean Architecture separates code into layers with strict dependency rules. The domain layer is the core, containing business logic with no external dependencies. Data and presentation layers depend on domain, never vice versa.

## Mandatory Structure

### Layer Organization

```
lib/
├── core/                           # Shared across features
│   ├── error/
│   │   ├── exceptions.dart         # Exception classes
│   │   └── failures.dart           # Failure classes
│   ├── network/
│   │   ├── api_client.dart         # Dio setup
│   │   └── network_info.dart       # Connectivity
│   ├── usecases/
│   │   └── usecase.dart            # Base UseCase
│   └── utils/
│       └── extensions.dart         # Dart extensions
│
├── features/
│   └── auth/                       # Feature module
│       ├── domain/                 # Business logic (pure Dart)
│       │   ├── entities/
│       │   │   └── user.dart
│       │   ├── repositories/
│       │   │   └── auth_repository.dart  # Abstract
│       │   └── usecases/
│       │       ├── login_user.dart
│       │       └── register_user.dart
│       │
│       ├── data/                   # Data handling
│       │   ├── models/
│       │   │   └── user_model.dart # With JSON
│       │   ├── datasources/
│       │   │   ├── auth_remote_datasource.dart
│       │   │   └── auth_local_datasource.dart
│       │   └── repositories/
│       │       └── auth_repository_impl.dart
│       │
│       └── presentation/           # UI layer
│           ├── bloc/
│           │   ├── auth_bloc.dart
│           │   ├── auth_event.dart
│           │   └── auth_state.dart
│           ├── pages/
│           │   ├── login_page.dart
│           │   └── register_page.dart
│           └── widgets/
│               └── auth_form.dart
│
└── injection_container.dart        # Dependency injection
```

## The Dependency Rule

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

**Rules:**
1. Domain has NO dependencies on other layers
2. Data implements domain interfaces
3. Presentation depends only on domain
4. Inner layers never know about outer layers

## Domain Layer

### Entities

Pure Dart classes representing core business objects:

```dart
// lib/features/auth/domain/entities/user.dart
import 'package:equatable/equatable.dart';

class User extends Equatable {
  final String id;
  final String email;
  final String name;
  final DateTime createdAt;

  const User({
    required this.id,
    required this.email,
    required this.name,
    required this.createdAt,
  });

  @override
  List<Object?> get props => [id, email, name, createdAt];
}
```

### Repository Interfaces

Abstract contracts for data operations:

```dart
// lib/features/auth/domain/repositories/auth_repository.dart
import 'package:dartz/dartz.dart';

abstract class AuthRepository {
  Future<Either<Failure, User>> login(String email, String password);
  Future<Either<Failure, User>> register(String email, String password, String name);
  Future<Either<Failure, void>> logout();
  Future<Either<Failure, User?>> getCurrentUser();
}
```

### Use Cases

Single-purpose business operations:

```dart
// lib/features/auth/domain/usecases/login_user.dart
import 'package:dartz/dartz.dart';
import 'package:equatable/equatable.dart';

class LoginUser implements UseCase<User, LoginParams> {
  final AuthRepository repository;

  LoginUser(this.repository);

  @override
  Future<Either<Failure, User>> call(LoginParams params) {
    return repository.login(params.email, params.password);
  }
}

class LoginParams extends Equatable {
  final String email;
  final String password;

  const LoginParams({
    required this.email,
    required this.password,
  });

  @override
  List<Object?> get props => [email, password];
}
```

### Base UseCase

```dart
// lib/core/usecases/usecase.dart
import 'package:dartz/dartz.dart';

abstract class UseCase<Type, Params> {
  Future<Either<Failure, Type>> call(Params params);
}

class NoParams extends Equatable {
  @override
  List<Object?> get props => [];
}
```

## Data Layer

### Models

DTOs that extend entities with serialization:

```dart
// lib/features/auth/data/models/user_model.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_model.freezed.dart';
part 'user_model.g.dart';

@freezed
class UserModel with _$UserModel {
  const UserModel._();

  const factory UserModel({
    required String id,
    required String email,
    required String name,
    @JsonKey(name: 'created_at') required DateTime createdAt,
  }) = _UserModel;

  factory UserModel.fromJson(Map<String, dynamic> json) =>
      _$UserModelFromJson(json);

  // Convert to domain entity
  User toEntity() => User(
    id: id,
    email: email,
    name: name,
    createdAt: createdAt,
  );

  // Create from domain entity
  factory UserModel.fromEntity(User user) => UserModel(
    id: user.id,
    email: user.email,
    name: user.name,
    createdAt: user.createdAt,
  );
}
```

### Data Sources

```dart
// lib/features/auth/data/datasources/auth_remote_datasource.dart
abstract class AuthRemoteDataSource {
  Future<UserModel> login(String email, String password);
  Future<UserModel> register(String email, String password, String name);
  Future<void> logout();
}

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final Dio client;

  AuthRemoteDataSourceImpl({required this.client});

  @override
  Future<UserModel> login(String email, String password) async {
    try {
      final response = await client.post(
        '/auth/login',
        data: {'email': email, 'password': password},
      );
      return UserModel.fromJson(response.data['user']);
    } on DioException catch (e) {
      throw ServerException(message: e.message ?? 'Server error');
    }
  }

  // ... other methods
}
```

```dart
// lib/features/auth/data/datasources/auth_local_datasource.dart
abstract class AuthLocalDataSource {
  Future<UserModel?> getCachedUser();
  Future<void> cacheUser(UserModel user);
  Future<void> clearCache();
}

class AuthLocalDataSourceImpl implements AuthLocalDataSource {
  final Box<String> userBox;

  AuthLocalDataSourceImpl({required this.userBox});

  @override
  Future<UserModel?> getCachedUser() async {
    final json = userBox.get('current_user');
    if (json == null) return null;
    return UserModel.fromJson(jsonDecode(json));
  }

  @override
  Future<void> cacheUser(UserModel user) async {
    await userBox.put('current_user', jsonEncode(user.toJson()));
  }

  @override
  Future<void> clearCache() async {
    await userBox.delete('current_user');
  }
}
```

### Repository Implementation

```dart
// lib/features/auth/data/repositories/auth_repository_impl.dart
class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;
  final AuthLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  AuthRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.networkInfo,
  });

  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    if (await networkInfo.isConnected) {
      try {
        final userModel = await remoteDataSource.login(email, password);
        await localDataSource.cacheUser(userModel);
        return Right(userModel.toEntity());
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    } else {
      return const Left(NetworkFailure('No internet connection'));
    }
  }

  @override
  Future<Either<Failure, User?>> getCurrentUser() async {
    try {
      final cachedUser = await localDataSource.getCachedUser();
      return Right(cachedUser?.toEntity());
    } on CacheException catch (e) {
      return Left(CacheFailure(e.message));
    }
  }

  // ... other methods
}
```

## Presentation Layer

### BLoC

```dart
// lib/features/auth/presentation/bloc/auth_bloc.dart
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final LoginUser loginUser;
  final LogoutUser logoutUser;
  final GetCurrentUser getCurrentUser;

  AuthBloc({
    required this.loginUser,
    required this.logoutUser,
    required this.getCurrentUser,
  }) : super(AuthInitial()) {
    on<LoginRequested>(_onLoginRequested);
    on<LogoutRequested>(_onLogoutRequested);
    on<AuthCheckRequested>(_onAuthCheckRequested);
  }

  Future<void> _onLoginRequested(
    LoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());

    final result = await loginUser(LoginParams(
      email: event.email,
      password: event.password,
    ));

    result.fold(
      (failure) => emit(AuthFailure(failure.message)),
      (user) => emit(AuthAuthenticated(user)),
    );
  }

  // ... other handlers
}
```

### Pages

```dart
// lib/features/auth/presentation/pages/login_page.dart
class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: BlocConsumer<AuthBloc, AuthState>(
        listener: (context, state) {
          if (state is AuthAuthenticated) {
            context.go('/home');
          }
          if (state is AuthFailure) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(state.message)),
            );
          }
        },
        builder: (context, state) {
          if (state is AuthLoading) {
            return const Center(child: CircularProgressIndicator());
          }
          return const LoginForm();
        },
      ),
    );
  }
}
```

## Dependency Injection

```dart
// lib/injection_container.dart
final sl = GetIt.instance;

Future<void> init() async {
  // Features - Auth
  // BLoC
  sl.registerFactory(
    () => AuthBloc(
      loginUser: sl(),
      logoutUser: sl(),
      getCurrentUser: sl(),
    ),
  );

  // Use Cases
  sl.registerLazySingleton(() => LoginUser(sl()));
  sl.registerLazySingleton(() => LogoutUser(sl()));
  sl.registerLazySingleton(() => GetCurrentUser(sl()));

  // Repository
  sl.registerLazySingleton<AuthRepository>(
    () => AuthRepositoryImpl(
      remoteDataSource: sl(),
      localDataSource: sl(),
      networkInfo: sl(),
    ),
  );

  // Data Sources
  sl.registerLazySingleton<AuthRemoteDataSource>(
    () => AuthRemoteDataSourceImpl(client: sl()),
  );
  sl.registerLazySingleton<AuthLocalDataSource>(
    () => AuthLocalDataSourceImpl(userBox: sl()),
  );

  // Core
  sl.registerLazySingleton<NetworkInfo>(() => NetworkInfoImpl(sl()));
  sl.registerLazySingleton(() => Dio()..options.baseUrl = ApiConstants.baseUrl);
}
```

## Anti-Patterns

### ❌ Domain Depending on Data

```dart
// BAD: Entity knows about JSON
class User {
  factory User.fromJson(Map<String, dynamic> json) => ... // Don't do this
}
```

### ✅ Keep Domain Pure

```dart
// GOOD: Entity is pure Dart
class User {
  final String id;
  final String name;
  const User({required this.id, required this.name});
}

// Model handles serialization
class UserModel {
  factory UserModel.fromJson(Map<String, dynamic> json) => ...
  User toEntity() => User(id: id, name: name);
}
```

### ❌ BLoC Calling Data Source Directly

```dart
// BAD: Presentation depends on Data
class AuthBloc {
  final AuthRemoteDataSource dataSource; // Wrong!
}
```

### ✅ BLoC Uses Only Use Cases

```dart
// GOOD: Presentation depends on Domain
class AuthBloc {
  final LoginUser loginUser; // Correct!
}
```

## References

- See [references/layers.md](references/layers.md) for detailed layer docs
- See [references/dependencies.md](references/dependencies.md) for DI patterns
- See `feature-structure` skill for feature organization
- See `dependency-injection` skill for GetIt setup
