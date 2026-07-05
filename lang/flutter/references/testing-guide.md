# Flutter Testing Guide

## 目录
- [TDD Workflow](#tdd-workflow)
- [Unit Testing](#unit-testing)
- [Widget Testing](#widget-testing)
- [BLoC Testing](#bloc-testing)
- [Test Organization](#test-organization)

## 概览
本指南提供完整的 Flutter 测试流程和模式，涵盖 TDD 工作流、单元测试、Widget 测试和 BLoC 测试。

## TDD Workflow

### Red/Green/Refactor 循环

TDD 的核心是三个步骤的循环：

#### 1. RED - 编写失败的测试
在编写任何生产代码之前，先编写一个描述预期行为的测试：

```dart
test('should return User when login is successful', () async {
  // Arrange
  final tEmail = 'test@example.com';
  final tPassword = 'password123';
  final tUser = User(id: '1', email: tEmail, name: 'Test User');

  when(() => mockRepository.login(tEmail, tPassword))
      .thenAnswer((_) async => Right(tUser));

  // Act
  final result = await usecase(
    LoginParams(email: tEmail, password: tPassword),
  );

  // Assert
  expect(result, Right(tUser));
  verify(() => mockRepository.login(tEmail, tPassword)).called(1);
});
```

**运行测试 - 必须失败**：
```bash
flutter test test/features/auth/domain/usecases/login_user_test.dart
```

#### 2. GREEN - 编写最小代码通过测试
编写最简单的代码使测试通过：

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

**运行测试 - 必须通过**：
```bash
flutter test test/features/auth/domain/usecases/login_user_test.dart
```

#### 3. REFACTOR - 改进代码质量
在保持测试通过的前提下改进代码：

```dart
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

**运行测试 - 确保仍然通过**：
```bash
flutter test
```

### 测试结构：Arrange-Act-Assert (AAA)

每个测试遵循 AAA 模式：

```dart
test('description of expected behavior', () async {
  // Arrange - 准备测试数据和 mocks
  final tInput = 'test input';
  when(() => mockDependency.method(any()))
      .thenReturn(expectedValue);

  // Act - 执行被测试的代码
  final result = await systemUnderTest.method(tInput);

  // Assert - 验证结果
  expect(result, expectedValue);
  verify(() => mockDependency.method(tInput)).called(1);
});
```

### 测试命名规范

使用描述性名称说明：
1. 测试什么
2. 在什么条件下
3. 预期结果

```dart
test('should return cached data when cache is valid', () {});
test('should throw CacheException when cache is empty', () {});
test('should call remote data source when cache is expired', () {});
```

## Unit Testing

### 测试文件结构

镜像源文件结构：

```
lib/features/auth/domain/usecases/login_user.dart
test/features/auth/domain/usecases/login_user_test.dart
```

### 测试设置

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dartz/dartz.dart';

class MockAuthRepository extends Mock implements AuthRepository {}

void main() {
  late LoginUser usecase;
  late MockAuthRepository mockRepository;

  setUp(() {
    mockRepository = MockAuthRepository();
    usecase = LoginUser(mockRepository);
  });

  setUpAll(() {
    registerFallbackValue(LoginParams(email: '', password: ''));
  });
}
```

### 测试函数

```dart
test('should validate email correctly', () {
  expect(Validators.isValidEmail('test@example.com'), true);
  expect(Validators.isValidEmail('invalid-email'), false);
});
```

### 测试异步代码

```dart
test('should complete with data', () async {
  when(() => mockService.fetchData())
      .thenAnswer((_) async => 'data');

  final result = await service.getData();

  expect(result, 'data');
});

test('should throw exception on error', () async {
  when(() => mockService.fetchData())
      .thenThrow(ServerException());

  expect(
    () => service.getData(),
    throwsA(isA<ServerException>()),
  );
});
```

## Widget Testing

### 测试设置

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mocktail/mocktail.dart';

class MockAuthBloc extends MockBloc<AuthEvent, AuthState>
    implements AuthBloc {}

void main() {
  late MockAuthBloc mockAuthBloc;

  setUp(() {
    mockAuthBloc = MockAuthBloc();
  });
}
```

### 创建 Widget 测试助手

```dart
Widget createWidgetUnderTest() {
  return MaterialApp(
    home: BlocProvider<AuthBloc>.value(
      value: mockAuthBloc,
      child: const LoginPage(),
    ),
  );
}
```

### Widget 测试

```dart
testWidgets('should display email and password fields', (tester) async {
  when(() => mockAuthBloc.state).thenReturn(AuthInitial());

  await tester.pumpWidget(createWidgetUnderTest());

  expect(find.byType(TextField), findsNWidgets(2));
  expect(find.text('Email'), findsOneWidget);
  expect(find.text('Password'), findsOneWidget);
});
```

### pump 方法说明

```dart
// pumpWidget: 首次构建 widget 树
await tester.pumpWidget(const MyApp());

// pump: 触发一帧，处理微任务
await tester.pump();
await tester.pump(const Duration(milliseconds: 100));

// pumpAndSettle: 泵送直到没有更多帧被调度
await tester.pumpAndSettle();

// 对于无限动画，使用 pump 加上 duration
await tester.pump(const Duration(seconds: 1));
```

### Finder 模式

```dart
// 按类型查找
find.byType(ElevatedButton);
find.byType(TextField);

// 按文本查找
find.text('Login');
find.textContaining('Log');

// 按 Key 查找
find.byKey(const Key('login_button'));

// 按语义查找
find.bySemanticsLabel('Login button');

// 组合查找器
find.descendant(
  of: find.byType(Form),
  matching: find.byType(TextField),
);
```

### 交互模式

```dart
testWidgets('should call login when button tapped', (tester) async {
  when(() => mockAuthBloc.state).thenReturn(AuthInitial());

  await tester.pumpWidget(createWidgetUnderTest());

  await tester.tap(find.byKey(const Key('login_button')));
  await tester.pump();

  verify(() => mockAuthBloc.add(any(that: isA<LoginRequested>()))).called(1);
});

testWidgets('should update email field', (tester) async {
  when(() => mockAuthBloc.state).thenReturn(AuthInitial());

  await tester.pumpWidget(createWidgetUnderTest());

  await tester.enterText(
    find.byKey(const Key('email_field')),
    'test@example.com',
  );
  await tester.pump();

  expect(find.text('test@example.com'), findsOneWidget);
});
```

## BLoC Testing

### 依赖设置

```yaml
dev_dependencies:
  bloc_test: ^9.1.0
  mocktail: ^1.0.0
```

### 测试设置

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockLoginUser extends Mock implements LoginUser {}

void main() {
  late AuthBloc bloc;
  late MockLoginUser mockLoginUser;

  setUp(() {
    mockLoginUser = MockLoginUser();
    bloc = AuthBloc(loginUser: mockLoginUser);
  });

  tearDown(() {
    bloc.close();
  });
}
```

### blocTest 模式

#### 基本状态转换测试

```dart
blocTest<AuthBloc, AuthState>(
  'emits [AuthLoading, AuthAuthenticated] when LoginRequested succeeds',
  build: () {
    when(() => mockLoginUser(any()))
        .thenAnswer((_) async => Right(tUser));
    return AuthBloc(loginUser: mockLoginUser);
  },
  act: (bloc) => bloc.add(LoginRequested(
    email: 'test@test.com',
    password: 'password123',
  )),
  expect: () => [
    AuthLoading(),
    AuthAuthenticated(tUser),
  ],
);
```

#### 测试错误状态

```dart
blocTest<AuthBloc, AuthState>(
  'emits [AuthLoading, AuthError] when LoginRequested fails',
  build: () {
    when(() => mockLoginUser(any()))
        .thenAnswer((_) async => Left(ServerFailure('Invalid credentials')));
    return AuthBloc(loginUser: mockLoginUser);
  },
  act: (bloc) => bloc.add(LoginRequested(
    email: 'test@test.com',
    password: 'wrong',
  )),
  expect: () => [
    AuthLoading(),
    AuthError('Invalid credentials'),
  ],
);
```

#### 使用 Seed 状态

```dart
blocTest<AuthBloc, AuthState>(
  'emits [AuthUnauthenticated] when LogoutRequested from authenticated state',
  build: () {
    when(() => mockLogoutUser(any()))
        .thenAnswer((_) async => const Right(null));
    return AuthBloc(loginUser: mockLoginUser, logoutUser: mockLogoutUser);
  },
  seed: () => AuthAuthenticated(tUser),
  act: (bloc) => bloc.add(LogoutRequested()),
  expect: () => [
    AuthLoading(),
    AuthUnauthenticated(),
  ],
);
```

#### 验证 Mock 调用

```dart
blocTest<AuthBloc, AuthState>(
  'calls loginUser with correct parameters',
  build: () {
    when(() => mockLoginUser(any()))
        .thenAnswer((_) async => Right(tUser));
    return AuthBloc(loginUser: mockLoginUser);
  },
  act: (bloc) => bloc.add(LoginRequested(
    email: 'test@test.com',
    password: 'password123',
  )),
  verify: (_) {
    verify(() => mockLoginUser(LoginParams(
      email: 'test@test.com',
      password: 'password123',
    ))).called(1);
  },
);
```

## Test Organization

### 使用 group 组织测试

```dart
void main() {
  group('LoginUser', () {
    group('successful login', () {
      test('should return User when credentials are valid', () async {});
      test('should call repository with correct parameters', () async {});
    });

    group('failed login', () {
      test('should return ServerFailure when server error occurs', () async {});
      test('should return InvalidCredentialsFailure when wrong', () async {});
    });
  });
}
```

### 测试覆盖率

生成覆盖率报告：

```bash
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
```

## 最佳实践

1. **测试命名**：使用描述性名称说明测试目的
2. **AAA 模式**：Arrange-Act-Assert 结构清晰
3. **单一职责**：每个测试只验证一个行为
4. **独立性**：测试之间相互独立，不依赖执行顺序
5. **快速反馈**：单元测试应该在毫秒级完成
6. **Mock 使用**：适当使用 mock 隔离依赖


## Mocking Patterns

### 概览
Mocking 通过用可控的替代品替换依赖项来隔离被测单元。Mocktail（推荐）和 Mockito 是 Flutter 的主要模拟库。

### Mocktail（推荐）

#### 为什么选择 Mocktail？
- 无需代码生成
- 原生支持 Null Safety
- API 比 Mockito 更简洁
- 更好的错误消息

#### 设置
```yaml
dev_dependencies:
  mocktail: ^1.0.0
```

#### 创建 Mock
```dart
import 'package:mocktail/mocktail.dart';

// Mock 一个类
class MockUserRepository extends Mock implements UserRepository {}

// Mock 一个抽象类
class MockAuthService extends Mock implements AuthService {}

// Mock 泛型
class MockBloc extends MockBloc<AuthEvent, AuthState> implements AuthBloc {}
```

#### 注册 Fallback 值
对于使用 `any()` 匹配器的自定义类型需要注册：

```dart
void main() {
  setUpAll(() {
    registerFallbackValue(LoginParams(email: '', password: ''));
    registerFallbackValue(User(id: '', name: '', email: ''));
  });
}

// 复杂类型的 Fake 类
class FakeUri extends Fake implements Uri {}
```

### Stubbing 方法

#### 基本 Stubbing
```dart
// 同步返回
when(() => mockRepository.getUser()).thenReturn(user);

// 异步返回
when(() => mockRepository.fetchUser())
    .thenAnswer((_) async => user);

// 抛出异常
when(() => mockRepository.fetchUser())
    .thenThrow(ServerException());

// 异步抛出异常
when(() => mockRepository.fetchUser())
    .thenAnswer((_) async => throw ServerException());
```

#### 带参数的 Stubbing
```dart
// 任意参数
when(() => mockRepository.getUserById(any()))
    .thenAnswer((_) async => user);

// 特定参数
when(() => mockRepository.getUserById('123'))
    .thenAnswer((_) async => user);

// 参数匹配
when(() => mockRepository.getUserById(any(that: startsWith('user_'))))
    .thenAnswer((_) async => user);

// 多个参数
when(() => mockRepository.login(any(), any()))
    .thenAnswer((_) async => user);

// 命名参数
when(() => mockRepository.search(query: any(named: 'query')))
    .thenAnswer((_) async => []);
```

#### 条件返回
```dart
// 根据输入返回不同值
when(() => mockRepository.getUserById(any())).thenAnswer((invocation) async {
  final id = invocation.positionalArguments[0] as String;
  if (id == '1') return user1;
  if (id == '2') return user2;
  throw NotFoundException();
});
```

#### Stubbing Getters 和 Setters
```dart
// Stub getter
when(() => mockService.isConnected).thenReturn(true);

// Stub stream getter
when(() => mockBloc.stream).thenAnswer((_) => Stream.value(state));

// Stub state getter (BLoC)
when(() => mockBloc.state).thenReturn(AuthInitial());
```

### 参数匹配器

#### 基本匹配器
```dart
// 任意值
any()

// 带类型约束的任意值
any<String>()

// 匹配条件的任意值
any(that: isA<User>())
any(that: equals(expectedUser))
any(that: startsWith('test'))

// 命名参数
any(named: 'userId')
```

#### 自定义匹配器
```dart
// 特定条件的匹配器
any(that: predicate<User>((user) => user.age > 18))

// 组合匹配器
any(that: allOf([
  isA<LoginParams>(),
  predicate<LoginParams>((p) => p.email.contains('@')),
]))
```

#### 捕获参数
```dart
// 捕获以供后续断言
final captured = verify(() => mockRepository.saveUser(captureAny())).captured;
expect(captured.first, isA<User>());

// 多次捕获
verify(() => mockRepository.log(captureAny())).captured;
// captured 是所有捕获值的列表
```

### 验证

#### 基本验证
```dart
// 验证被调用
verify(() => mockRepository.getUser()).called(1);

// 验证被调用多次
verify(() => mockRepository.log(any())).called(3);

// 验证从未被调用
verifyNever(() => mockRepository.deleteUser(any()));

// 验证没有其他交互
verifyNoMoreInteractions(mockRepository);
```

#### 验证顺序
```dart
// 按顺序验证
verifyInOrder([
  () => mockRepository.load(),
  () => mockRepository.save(any()),
  () => mockRepository.clear(),
]);
```

### Mockito（备选）

#### 设置
```yaml
dev_dependencies:
  mockito: ^5.4.0
  build_runner: ^2.4.0
```

#### 创建 Mock
```dart
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

@GenerateMocks([UserRepository])
import 'user_repository_test.mocks.dart';

void main() {
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
  });
}
```

### Mocking 最佳实践

1. **优先使用 Mocktail**：无需代码生成，更现代
2. **注册 Fallback 值**：为自定义类型注册避免错误
3. **精确验证**：验证具体的调用次数和参数
4. **避免过度 Mock**：只 mock 外部依赖，不要 mock 被测代码
5. **清晰命名**：Mock 类使用 `Mock` + 原类名
