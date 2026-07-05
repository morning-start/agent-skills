# Test Writer Agent 使用指南

## 概览
Test Writer Agent 是一个测试编写专家，为 Flutter 应用生成全面、结构良好的测试。测试遵循 TDD 原则和最佳实践。

## 触发方式

当智能体被要求以下任务时，应扮演 Test Writer：
- "编写测试"
- "添加测试覆盖"
- "为文件或功能生成测试"

## 测试编写流程

### 1. 分析源代码

当给定要测试的代码时：
- 识别类型（UseCase、Repository、BLoC、Widget 等）
- 列出所有公共方法/行为
- 识别需要 mock 的依赖
- 注意边界情况和错误条件

### 2. 确定测试策略

| 代码类型 | 测试类型 | 关键关注点 |
|---------|---------|-----------|
| Entity | Unit | 相等性、copyWith、序列化 |
| UseCase | Unit | 调用 repository、返回正确结果 |
| Repository | Unit | 数据源调用、错误映射 |
| DataSource | Unit | API 调用、JSON 解析 |
| BLoC | blocTest | 状态转换、事件处理 |
| Widget | Widget | 渲染、交互、状态显示 |

### 3. 生成测试结构

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:bloc_test/bloc_test.dart'; // 如果是 BLoC
import 'package:dartz/dartz.dart';

// 源代码的导入
// 依赖的导入

// Mock 类
class MockDependency extends Mock implements Dependency {}

// Fallback 值的 Fake 类
class FakeParams extends Fake implements Params {}

void main() {
  // 声明 late 变量
  late SystemUnderTest sut;
  late MockDependency mockDependency;

  // 测试固件
  final tInput = 'test input';
  final tOutput = TestOutput(id: '1');

  setUp(() {
    mockDependency = MockDependency();
    sut = SystemUnderTest(dependency: mockDependency);
  });

  setUpAll(() {
    registerFallbackValue(FakeParams());
  });

  group('SystemUnderTest', () {
    group('methodName', () {
      test('should do X when Y', () async {
        // Arrange
        when(() => mockDependency.method(any()))
            .thenAnswer((_) async => result);

        // Act
        final result = await sut.method(input);

        // Assert
        expect(result, expected);
        verify(() => mockDependency.method(input)).called(1);
      });
    });
  });
}
```

### 4. 包含的测试类别

#### 正常路径测试
```dart
test('should return data when operation succeeds', () async {
  // 测试正常成功操作
});
```

#### 错误/失败测试
```dart
test('should return failure when operation fails', () async {
  // 测试错误处理
});
```

#### 边界情况测试
```dart
test('should handle empty list', () async {});
test('should handle null value', () async {});
test('should handle maximum value', () async {});
```

#### 验证测试
```dart
test('should call dependency with correct parameters', () async {
  // 验证 mock 交互
});
```

## 测试模板

### UseCase 测试

```dart
void main() {
  late GetUser usecase;
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
    usecase = GetUser(mockRepository);
  });

  final tUserId = '123';
  final tUser = User(id: tUserId, name: 'Test', email: 'test@test.com');

  group('GetUser', () {
    test('should return User from repository', () async {
      // Arrange
      when(() => mockRepository.getUser(any()))
          .thenAnswer((_) async => Right(tUser));

      // Act
      final result = await usecase(GetUserParams(id: tUserId));

      // Assert
      expect(result, Right(tUser));
      verify(() => mockRepository.getUser(tUserId)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return ServerFailure when repository fails', () async {
      // Arrange
      when(() => mockRepository.getUser(any()))
          .thenAnswer((_) async => Left(ServerFailure('error')));

      // Act
      final result = await usecase(GetUserParams(id: tUserId));

      // Assert
      expect(result, Left(ServerFailure('error')));
    });
  });
}
```

### Repository 测试

```dart
void main() {
  late UserRepositoryImpl repository;
  late MockUserRemoteDataSource mockRemoteDataSource;
  late MockUserLocalDataSource mockLocalDataSource;
  late MockNetworkInfo mockNetworkInfo;

  setUp(() {
    mockRemoteDataSource = MockUserRemoteDataSource();
    mockLocalDataSource = MockUserLocalDataSource();
    mockNetworkInfo = MockNetworkInfo();
    repository = UserRepositoryImpl(
      remoteDataSource: mockRemoteDataSource,
      localDataSource: mockLocalDataSource,
      networkInfo: mockNetworkInfo,
    );
  });

  group('getUser', () {
    final tUserModel = UserModel(id: '1', name: 'Test', email: 'test@test.com');
    final tUser = tUserModel.toEntity();

    group('device is online', () {
      setUp(() {
        when(() => mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      });

      test('should return remote data when call is successful', () async {
        when(() => mockRemoteDataSource.getUser(any()))
            .thenAnswer((_) async => tUserModel);

        final result = await repository.getUser('1');

        expect(result, Right(tUser));
        verify(() => mockRemoteDataSource.getUser('1')).called(1);
      });

      test('should cache remote data after successful call', () async {
        when(() => mockRemoteDataSource.getUser(any()))
            .thenAnswer((_) async => tUserModel);

        await repository.getUser('1');

        verify(() => mockLocalDataSource.cacheUser(tUserModel)).called(1);
      });
    });

    group('device is offline', () {
      setUp(() {
        when(() => mockNetworkInfo.isConnected).thenAnswer((_) async => false);
      });

      test('should return cached data when available', () async {
        when(() => mockLocalDataSource.getUser(any()))
            .thenAnswer((_) async => tUserModel);

        final result = await repository.getUser('1');

        expect(result, Right(tUser));
        verify(() => mockLocalDataSource.getUser('1')).called(1);
        verifyNever(() => mockRemoteDataSource.getUser(any()));
      });
    });
  });
}
```

### Widget 测试

```dart
void main() {
  late MockAuthBloc mockBloc;

  setUp(() {
    mockBloc = MockAuthBloc();
  });

  Widget createWidget() {
    return MaterialApp(
      home: BlocProvider<AuthBloc>.value(
        value: mockBloc,
        child: const LoginPage(),
      ),
    );
  }

  group('LoginPage', () {
    testWidgets('should render email and password fields', (tester) async {
      when(() => mockBloc.state).thenReturn(AuthInitial());

      await tester.pumpWidget(createWidget());

      expect(find.byType(TextField), findsNWidgets(2));
      expect(find.text('Email'), findsOneWidget);
      expect(find.text('Password'), findsOneWidget);
    });

    testWidgets('should call login when button tapped', (tester) async {
      when(() => mockBloc.state).thenReturn(AuthInitial());
      when(() => mockBloc.stream).thenAnswer((_) => Stream.value(AuthInitial()));

      await tester.pumpWidget(createWidget());

      await tester.enterText(find.byKey(const Key('email_field')), 'test@test.com');
      await tester.enterText(find.byKey(const Key('password_field')), 'password123');

      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      verify(() => mockBloc.add(any(that: isA<LoginRequested>()))).called(1);
    });

    testWidgets('should show error message when login fails', (tester) async {
      when(() => mockBloc.state).thenReturn(AuthError('Invalid credentials'));
      when(() => mockBloc.stream).thenAnswer((_) => Stream.value(AuthError('Invalid credentials')));

      await tester.pumpWidget(createWidget());

      expect(find.text('Invalid credentials'), findsOneWidget);
    });
  });
}
```

## 测试最佳实践

1. **AAA 模式**：Arrange-Act-Assert 结构清晰
2. **描述性命名**：测试名称说明测试内容
3. **独立测试**：每个测试独立运行
4. **快速执行**：测试应该在毫秒级完成
5. **覆盖边界**：测试正常和异常情况
6. **验证交互**：验证 mock 调用
7. **清理资源**：使用 tearDown 释放资源

## 测试覆盖率目标

- **单元测试**：> 80%
- **Widget 测试**：> 70%
- **集成测试**：> 50%
- **整体覆盖率**：> 70%

## 快速参考

```bash
# 运行所有测试
flutter test

# 运行特定测试文件
flutter test test/features/auth/domain/usecases/login_user_test.dart

# 运行特定测试
flutter test --name "should return User"

# 生成覆盖率报告
flutter test --coverage

# 查看覆盖率
genhtml coverage/lcov.info -o coverage/html
```
