---
name: unit-testing
description: Pure Dart function and class testing patterns. Use when testing domain logic, use cases, utilities, or any non-widget code. Covers mocktail, test organization, and assertions.
---

# Unit Testing

## Overview

Unit tests verify individual units of code (functions, classes, methods) in isolation. They are fast, reliable, and form the foundation of your test pyramid.

## Mandatory Workflow

### Step 1: Set Up Test File Structure

Mirror your source file structure:

```
lib/features/auth/domain/usecases/login_user.dart
test/features/auth/domain/usecases/login_user_test.dart
```

### Step 2: Create Test File with Proper Imports

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dartz/dartz.dart';

import 'package:your_app/features/auth/domain/usecases/login_user.dart';
import 'package:your_app/features/auth/domain/repositories/auth_repository.dart';
import 'package:your_app/core/error/failures.dart';

// Mock classes
class MockAuthRepository extends Mock implements AuthRepository {}

void main() {
  // Test implementation here
}
```

### Step 3: Use setUp for Common Initialization

```dart
void main() {
  late LoginUser usecase;
  late MockAuthRepository mockRepository;

  setUp(() {
    mockRepository = MockAuthRepository();
    usecase = LoginUser(mockRepository);
  });

  // Register fallback values for any() matchers
  setUpAll(() {
    registerFallbackValue(LoginParams(email: '', password: ''));
  });
}
```

### Step 4: Organize Tests with group()

```dart
void main() {
  // ... setUp

  group('LoginUser', () {
    group('successful login', () {
      test('should return User when credentials are valid', () async {
        // test implementation
      });

      test('should call repository with correct parameters', () async {
        // test implementation
      });
    });

    group('failed login', () {
      test('should return ServerFailure when server error occurs', () async {
        // test implementation
      });

      test('should return InvalidCredentialsFailure when credentials wrong', () async {
        // test implementation
      });
    });
  });
}
```

## Testing Patterns

### Pattern 1: Testing Functions

```dart
// Source: lib/core/utils/validators.dart
class Validators {
  static bool isValidEmail(String email) {
    return RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(email);
  }
}

// Test: test/core/utils/validators_test.dart
void main() {
  group('Validators', () {
    group('isValidEmail', () {
      test('should return true for valid email', () {
        expect(Validators.isValidEmail('test@example.com'), true);
      });

      test('should return false for invalid email', () {
        expect(Validators.isValidEmail('invalid-email'), false);
      });

      test('should return false for empty string', () {
        expect(Validators.isValidEmail(''), false);
      });
    });
  });
}
```

### Pattern 2: Testing Classes with Dependencies

```dart
// Source
class GetUser implements UseCase<User, String> {
  final UserRepository repository;
  GetUser(this.repository);

  @override
  Future<Either<Failure, User>> call(String userId) {
    return repository.getUser(userId);
  }
}

// Test
class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late GetUser usecase;
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
    usecase = GetUser(mockRepository);
  });

  final tUserId = '123';
  final tUser = User(id: tUserId, name: 'Test', email: 'test@test.com');

  test('should return user from repository', () async {
    // Arrange
    when(() => mockRepository.getUser(tUserId))
        .thenAnswer((_) async => Right(tUser));

    // Act
    final result = await usecase(tUserId);

    // Assert
    expect(result, Right(tUser));
    verify(() => mockRepository.getUser(tUserId)).called(1);
    verifyNoMoreInteractions(mockRepository);
  });
}
```

### Pattern 3: Testing Async Code

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

### Pattern 4: Testing Streams

```dart
test('should emit values in order', () {
  final stream = service.dataStream;

  expect(
    stream,
    emitsInOrder([
      'loading',
      'data',
      emitsDone,
    ]),
  );
});

test('should emit error', () {
  when(() => mockService.dataStream)
      .thenAnswer((_) => Stream.error(Exception('error')));

  expect(
    service.dataStream,
    emitsError(isA<Exception>()),
  );
});
```

### Pattern 5: Testing with Either (dartz/fpdart)

```dart
test('should return Right with data on success', () async {
  when(() => mockRepository.getData())
      .thenAnswer((_) async => const Right('data'));

  final result = await usecase();

  expect(result.isRight(), true);
  expect(result.getOrElse(() => ''), 'data');
});

test('should return Left with failure on error', () async {
  when(() => mockRepository.getData())
      .thenAnswer((_) async => Left(ServerFailure()));

  final result = await usecase();

  expect(result.isLeft(), true);
  result.fold(
    (failure) => expect(failure, isA<ServerFailure>()),
    (_) => fail('Should be Left'),
  );
});
```

## Mocktail Patterns

### Basic Mocking

```dart
// Stub a method
when(() => mock.method(any())).thenReturn(value);
when(() => mock.asyncMethod(any())).thenAnswer((_) async => value);

// Verify calls
verify(() => mock.method('param')).called(1);
verifyNever(() => mock.method(any()));
verifyNoMoreInteractions(mock);
```

### Argument Matchers

```dart
// Any argument
when(() => mock.method(any())).thenReturn(value);

// Specific type
when(() => mock.method(any(that: isA<String>()))).thenReturn(value);

// Custom matcher
when(() => mock.method(any(that: startsWith('test')))).thenReturn(value);

// Capture arguments
final captured = verify(() => mock.method(captureAny())).captured;
expect(captured.first, 'expected');
```

### Throwing Exceptions

```dart
when(() => mock.method()).thenThrow(Exception('error'));

// For async methods
when(() => mock.asyncMethod())
    .thenAnswer((_) async => throw Exception('error'));
```

### Sequential Returns

```dart
var callCount = 0;
when(() => mock.method()).thenAnswer((_) {
  callCount++;
  if (callCount == 1) return 'first';
  return 'second';
});
```

## Assertion Patterns

### Basic Assertions

```dart
expect(actual, expected);
expect(actual, equals(expected));
expect(actual, isNull);
expect(actual, isNotNull);
expect(actual, isTrue);
expect(actual, isFalse);
```

### Collection Assertions

```dart
expect(list, isEmpty);
expect(list, isNotEmpty);
expect(list, hasLength(3));
expect(list, contains('item'));
expect(list, containsAll(['a', 'b']));
expect(list, orderedEquals(['a', 'b', 'c']));
```

### Type Assertions

```dart
expect(value, isA<String>());
expect(value, isA<User>());
expect(error, isA<ServerFailure>());
```

### Exception Assertions

```dart
expect(() => function(), throwsException);
expect(() => function(), throwsA(isA<CustomException>()));
expect(() => function(), throwsArgumentError);

// Async exceptions
expect(() async => await asyncFunction(), throwsA(isA<ServerException>()));
```

## Test Data Fixtures

### Creating Test Fixtures

```dart
// test/fixtures/user_fixtures.dart
class UserFixtures {
  static User get validUser => User(
    id: '1',
    name: 'Test User',
    email: 'test@example.com',
  );

  static User userWithId(String id) => User(
    id: id,
    name: 'Test User',
    email: 'test@example.com',
  );

  static List<User> get userList => [
    User(id: '1', name: 'User 1', email: 'user1@test.com'),
    User(id: '2', name: 'User 2', email: 'user2@test.com'),
  ];
}

// Usage in tests
final tUser = UserFixtures.validUser;
```

### Loading JSON Fixtures

```dart
// test/fixtures/reader.dart
String fixture(String name) => File('test/fixtures/$name').readAsStringSync();

// Usage
final json = fixture('user.json');
final userModel = UserModel.fromJson(jsonDecode(json));
```

## Anti-Patterns

### ❌ Testing Multiple Things

```dart
// BAD
test('user operations', () {
  expect(service.createUser(user), isNotNull);
  expect(service.getUser('1'), user);
  expect(service.deleteUser('1'), true);
});
```

### ✅ One Assert Per Test

```dart
// GOOD
test('should create user', () {
  expect(service.createUser(user), isNotNull);
});

test('should get user by id', () {
  expect(service.getUser('1'), user);
});

test('should delete user', () {
  expect(service.deleteUser('1'), true);
});
```

### ❌ No Arrange Phase

```dart
// BAD
test('should work', () {
  expect(SomeClass().method(), 'result'); // No setup
});
```

### ✅ Clear Arrange-Act-Assert

```dart
// GOOD
test('should return formatted name', () {
  // Arrange
  final user = User(firstName: 'John', lastName: 'Doe');

  // Act
  final result = user.fullName;

  // Assert
  expect(result, 'John Doe');
});
```

## Running Tests

```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/features/auth/domain/usecases/login_user_test.dart

# Run tests matching name
flutter test --name "should return user"

# Run with coverage
flutter test --coverage

# Run in verbose mode
flutter test --reporter expanded
```

## References

- See [references/patterns.md](references/patterns.md) for more patterns
- See `mocking-patterns` skill for advanced mocking
- See `test-fixtures` skill for fixture management
