---
name: tdd-workflow
description: Master TDD red/green/refactor cycle for Flutter development. Use when writing new features, fixing bugs, or when user mentions "TDD", "test-driven", or "write tests first". Enforces disciplined testing approach.
---

# TDD Workflow

## Overview

Test-Driven Development (TDD) is a software development approach where tests are written before the production code. This skill enforces the **Red/Green/Refactor** cycle for all Flutter development.

## Mandatory Workflow

### Step 1: RED — Write a Failing Test First

Before writing any production code, write a test that:
- Describes the expected behavior
- Fails because the code doesn't exist yet
- Is specific and focused on one behavior

```dart
// test/features/auth/domain/usecases/login_user_test.dart
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

  group('LoginUser', () {
    final tEmail = 'test@example.com';
    final tPassword = 'password123';
    final tUser = User(id: '1', email: tEmail, name: 'Test User');

    test('should return User when login is successful', () async {
      // Arrange
      when(() => mockRepository.login(tEmail, tPassword))
          .thenAnswer((_) async => Right(tUser));

      // Act
      final result = await usecase(
        LoginParams(email: tEmail, password: tPassword),
      );

      // Assert
      expect(result, Right(tUser));
      verify(() => mockRepository.login(tEmail, tPassword)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return ServerFailure when login fails', () async {
      // Arrange
      when(() => mockRepository.login(tEmail, tPassword))
          .thenAnswer((_) async => Left(ServerFailure()));

      // Act
      final result = await usecase(
        LoginParams(email: tEmail, password: tPassword),
      );

      // Assert
      expect(result, Left(ServerFailure()));
    });
  });
}
```

**Run the test — it MUST fail:**

```bash
flutter test test/features/auth/domain/usecases/login_user_test.dart
```

### Step 2: GREEN — Write Minimum Code to Pass

Write the simplest code that makes the test pass. Do not:
- Add extra features
- Optimize prematurely
- Handle edge cases not covered by tests

```dart
// lib/features/auth/domain/usecases/login_user.dart
import 'package:dartz/dartz.dart';

class LoginUser implements UseCase<User, LoginParams> {
  final AuthRepository repository;

  LoginUser(this.repository);

  @override
  Future<Either<Failure, User>> call(LoginParams params) {
    return repository.login(params.email, params.password);
  }
}

class LoginParams {
  final String email;
  final String password;

  LoginParams({required this.email, required this.password});
}
```

**Run the test — it MUST pass:**

```bash
flutter test test/features/auth/domain/usecases/login_user_test.dart
```

### Step 3: REFACTOR — Improve While Tests Pass

Now improve the code quality:
- Extract duplications
- Improve naming
- Simplify logic
- Add documentation if needed

**Critical Rule:** Tests must stay green throughout refactoring.

```dart
// Refactored with Equatable for value comparison
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

Run tests after every refactoring change:

```bash
flutter test
```

## The TDD Cycle Checklist

For every piece of functionality:

- [ ] **RED**: Write test describing expected behavior
- [ ] **RED**: Run test — verify it fails
- [ ] **GREEN**: Write minimum code to pass
- [ ] **GREEN**: Run test — verify it passes
- [ ] **REFACTOR**: Improve code quality
- [ ] **REFACTOR**: Run tests — verify still passing
- [ ] Repeat for next behavior

## Test Structure: Arrange-Act-Assert (AAA)

Every test should follow this pattern:

```dart
test('description of expected behavior', () async {
  // Arrange — Set up test data and mocks
  final tInput = 'test input';
  when(() => mockDependency.method(any()))
      .thenReturn(expectedValue);

  // Act — Execute the code under test
  final result = await systemUnderTest.method(tInput);

  // Assert — Verify the results
  expect(result, expectedValue);
  verify(() => mockDependency.method(tInput)).called(1);
});
```

## Test Naming Convention

Use descriptive names that explain:
1. What is being tested
2. Under what conditions
3. Expected outcome

```dart
// Good
test('should return cached data when cache is valid', () {});
test('should throw CacheException when cache is empty', () {});
test('should call remote data source when cache is expired', () {});

// Bad
test('test1', () {});
test('login test', () {});
test('it works', () {});
```

## TDD for Different Layers

### Domain Layer (Use Cases)
```dart
// Test use case calls repository correctly
test('should get user from repository', () async {
  when(() => mockRepository.getUser(any()))
      .thenAnswer((_) async => Right(tUser));

  final result = await usecase(Params(id: '1'));

  expect(result, Right(tUser));
  verify(() => mockRepository.getUser('1')).called(1);
});
```

### Data Layer (Repositories)
```dart
// Test repository calls correct data source
test('should return remote data when online', () async {
  when(() => mockNetworkInfo.isConnected).thenAnswer((_) async => true);
  when(() => mockRemoteDataSource.getUser(any()))
      .thenAnswer((_) async => tUserModel);

  final result = await repository.getUser('1');

  expect(result, Right(tUser));
  verify(() => mockRemoteDataSource.getUser('1')).called(1);
});
```

### Presentation Layer (BLoC)
```dart
// Test state transitions
blocTest<UserBloc, UserState>(
  'emits [Loading, Loaded] when GetUser is successful',
  build: () {
    when(() => mockGetUser(any()))
        .thenAnswer((_) async => Right(tUser));
    return UserBloc(getUser: mockGetUser);
  },
  act: (bloc) => bloc.add(GetUserEvent(id: '1')),
  expect: () => [
    UserLoading(),
    UserLoaded(tUser),
  ],
);
```

## Anti-Patterns

### ❌ Writing Tests After Code
```dart
// BAD: Code exists before test
class Calculator {
  int add(int a, int b) => a + b;
}

// Test written after — misses TDD benefits
test('add works', () {
  expect(Calculator().add(1, 2), 3);
});
```

### ✅ Writing Tests Before Code
```dart
// GOOD: Test first
test('should return sum of two numbers', () {
  final calculator = Calculator();
  expect(calculator.add(1, 2), 3);
});

// Then implement
class Calculator {
  int add(int a, int b) => a + b;
}
```

### ❌ Testing Implementation Details
```dart
// BAD: Testing private methods or internal state
test('internal list has 3 items', () {
  expect(service._internalList.length, 3); // Don't do this
});
```

### ✅ Testing Behavior
```dart
// GOOD: Testing observable behavior
test('should return 3 items', () {
  expect(service.getItems().length, 3);
});
```

### ❌ Skipping the RED Phase
```dart
// BAD: Never saw the test fail
test('should work', () {
  expect(true, true); // Always passes — useless
});
```

## When NOT to Use TDD

- Spike/prototype code (throw away)
- UI layout exploration
- Learning new APIs

**But:** Convert spikes to TDD code before production.

## References

- See [references/red-green-refactor.md](references/red-green-refactor.md) for detailed cycle explanation
- See `unit-testing` skill for unit test patterns
- See `widget-testing` skill for widget test patterns
- See `bloc-testing` skill for BLoC test patterns
