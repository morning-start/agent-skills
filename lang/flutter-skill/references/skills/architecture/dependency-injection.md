---
name: dependency-injection
description: GetIt and Injectable setup for dependency injection. Use when setting up DI, registering dependencies, or when user asks about "dependency injection", "GetIt", "Injectable", or "service locator".
---

# Dependency Injection

## Overview

Dependency Injection (DI) decouples object creation from usage, enabling testability and flexibility. GetIt is the recommended service locator for Flutter, optionally with Injectable for code generation.

## GetIt Setup (Manual)

### Installation

```yaml
# pubspec.yaml
dependencies:
  get_it: ^7.6.0
```

### Service Locator Setup

```dart
// lib/injection_container.dart
import 'package:get_it/get_it.dart';
import 'package:dio/dio.dart';

final sl = GetIt.instance;

Future<void> init() async {
  //============================
  // External Dependencies
  //============================
  sl.registerLazySingleton(() => Dio()..options = BaseOptions(
    baseUrl: 'https://api.example.com',
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 30),
  ));

  //============================
  // Core
  //============================
  sl.registerLazySingleton<NetworkInfo>(
    () => NetworkInfoImpl(Connectivity()),
  );

  //============================
  // Features
  //============================
  await _initAuth();
  await _initUser();
  // Add more features
}

Future<void> _initAuth() async {
  // BLoCs - Factory (new instance each time)
  sl.registerFactory(
    () => AuthBloc(
      loginUser: sl(),
      logoutUser: sl(),
      getCurrentUser: sl(),
    ),
  );

  // Use Cases - Lazy Singleton
  sl.registerLazySingleton(() => LoginUser(sl()));
  sl.registerLazySingleton(() => LogoutUser(sl()));
  sl.registerLazySingleton(() => GetCurrentUser(sl()));

  // Repository - Lazy Singleton
  sl.registerLazySingleton<AuthRepository>(
    () => AuthRepositoryImpl(
      remoteDataSource: sl(),
      localDataSource: sl(),
      networkInfo: sl(),
    ),
  );

  // Data Sources - Lazy Singleton
  sl.registerLazySingleton<AuthRemoteDataSource>(
    () => AuthRemoteDataSourceImpl(client: sl()),
  );
  sl.registerLazySingleton<AuthLocalDataSource>(
    () => AuthLocalDataSourceImpl(storage: sl()),
  );
}
```

### Registration Types

```dart
// Singleton - Same instance always
sl.registerSingleton(MySingleton());

// Lazy Singleton - Created on first access
sl.registerLazySingleton(() => MyLazySingleton());

// Factory - New instance each time
sl.registerFactory(() => MyFactory());

// Factory with parameters
sl.registerFactoryParam<MyService, String, int>(
  (param1, param2) => MyService(param1, param2),
);

// Async singleton
sl.registerSingletonAsync<Database>(() async {
  final db = Database();
  await db.init();
  return db;
});
```

### Initialize in main.dart

```dart
// lib/main.dart
import 'injection_container.dart' as di;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await di.init();

  runApp(const MyApp());
}
```

### Using Dependencies

```dart
// In widgets
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => sl<AuthBloc>()..add(AuthCheckRequested()),
      child: const AuthView(),
    );
  }
}

// In other classes
class MyService {
  final UserRepository _userRepo = sl<UserRepository>();

  Future<User> getUser() => _userRepo.getUser();
}
```

## Injectable Setup (Code Generation)

### Installation

```yaml
# pubspec.yaml
dependencies:
  get_it: ^7.6.0
  injectable: ^2.3.0

dev_dependencies:
  injectable_generator: ^2.4.0
  build_runner: ^2.4.0
```

### Configure Injectable

```dart
// lib/injection_container.dart
import 'package:get_it/get_it.dart';
import 'package:injectable/injectable.dart';

import 'injection_container.config.dart';

final sl = GetIt.instance;

@InjectableInit()
Future<void> configureDependencies() async => sl.init();
```

### Annotate Classes

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

// Register as interface
@LazySingleton(as: AuthRepository)
class AuthRepositoryImpl implements AuthRepository {
  // ...
}

// Named registration
@Named('prod')
@lazySingleton
class ProductionApiClient implements ApiClient {}

@Named('dev')
@lazySingleton
class DevelopmentApiClient implements ApiClient {}

// Environment-specific
@Environment('prod')
@lazySingleton
class ProductionService implements MyService {}

@Environment('dev')
@lazySingleton
class DevelopmentService implements MyService {}
```

### External Dependencies

```dart
// lib/injection/external_module.dart
import 'package:injectable/injectable.dart';
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

@module
abstract class ExternalModule {
  @lazySingleton
  Dio get dio => Dio()..options = BaseOptions(
    baseUrl: 'https://api.example.com',
  );

  @preResolve
  Future<SharedPreferences> get prefs => SharedPreferences.getInstance();
}
```

### Generate Code

```bash
dart run build_runner build --delete-conflicting-outputs
```

## Best Practices

### Registration Order

```dart
// 1. External dependencies (Dio, SharedPreferences, etc.)
// 2. Core services (NetworkInfo, Logger, etc.)
// 3. Data sources (Remote, Local)
// 4. Repositories
// 5. Use cases
// 6. BLoCs/Cubits (always last)
```

### BLoCs Should Be Factories

```dart
// ✅ Correct: Factory - new instance each time
sl.registerFactory(() => AuthBloc(loginUser: sl()));

// ❌ Wrong: Singleton - shared state issues
sl.registerSingleton(AuthBloc(loginUser: sl())); // Don't do this
```

### Use Interfaces for Abstraction

```dart
// Register implementation against interface
sl.registerLazySingleton<UserRepository>(
  () => UserRepositoryImpl(
    remoteDataSource: sl(),
    localDataSource: sl(),
  ),
);

// Depend on interface, not implementation
class GetUser {
  final UserRepository repository; // Interface type
  GetUser(this.repository);
}
```

### Organize by Feature

```dart
Future<void> init() async {
  await _initCore();
  await _initAuth();
  await _initUser();
  await _initOrders();
}

Future<void> _initAuth() async {
  // All auth-related registrations
}

Future<void> _initUser() async {
  // All user-related registrations
}
```

## Testing with DI

### Override for Tests

```dart
void main() {
  late MockUserRepository mockUserRepository;

  setUp(() {
    mockUserRepository = MockUserRepository();

    // Override registration for testing
    sl.registerLazySingleton<UserRepository>(() => mockUserRepository);
  });

  tearDown(() {
    sl.reset(); // Clear all registrations
  });

  test('should use mock repository', () {
    final usecase = GetUser(sl());
    // usecase now uses mockUserRepository
  });
}
```

### Dedicated Test Setup

```dart
// test/helpers/injection_helper.dart
Future<void> initTestDependencies() async {
  // Reset GetIt
  await sl.reset();

  // Register test doubles
  sl.registerLazySingleton<UserRepository>(() => MockUserRepository());
  sl.registerLazySingleton<NetworkInfo>(() => MockNetworkInfo());
}
```

## Anti-Patterns

### ❌ Using sl in Domain Layer

```dart
// BAD: Domain layer using service locator
class LoginUser {
  Future<Either<Failure, User>> call(params) {
    final repo = sl<AuthRepository>(); // Don't do this
    return repo.login(params.email, params.password);
  }
}
```

### ✅ Inject Through Constructor

```dart
// GOOD: Constructor injection
class LoginUser {
  final AuthRepository repository;
  LoginUser(this.repository); // Inject dependency

  Future<Either<Failure, User>> call(params) {
    return repository.login(params.email, params.password);
  }
}
```

### ❌ Circular Dependencies

```dart
// BAD: A depends on B, B depends on A
class ServiceA {
  ServiceA(ServiceB b);
}
class ServiceB {
  ServiceB(ServiceA a); // Circular!
}
```

### ✅ Break Cycle with Interface

```dart
// GOOD: Use interface to break cycle
abstract class IServiceA {}
class ServiceA implements IServiceA {
  ServiceA(ServiceB b);
}
class ServiceB {
  ServiceB(IServiceA a); // Depends on interface
}
```

## References

- See `clean-architecture` skill for layer organization
- See `bloc-architecture` skill for BLoC registration
- See `repository-pattern` skill for repository setup
