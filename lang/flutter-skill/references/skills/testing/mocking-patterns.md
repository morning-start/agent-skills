---
name: mocking-patterns
description: Mocktail and Mockito patterns for Flutter testing. Use when setting up mocks, stubs, or verifying interactions. Covers mock creation, argument matchers, and verification.
---

# Mocking Patterns

## Overview

Mocking isolates units under test by replacing dependencies with controlled substitutes. Mocktail (recommended) and Mockito are the primary mocking libraries for Flutter.

## Mocktail (Recommended)

### Why Mocktail?

- No code generation required
- Null-safe from the start
- Simpler API than Mockito
- Better error messages

### Setup

```yaml
# pubspec.yaml
dev_dependencies:
  mocktail: ^1.0.0
```

### Creating Mocks

```dart
import 'package:mocktail/mocktail.dart';

// Mock a class
class MockUserRepository extends Mock implements UserRepository {}

// Mock an abstract class
class MockAuthService extends Mock implements AuthService {}

// Mock with generics
class MockBloc extends MockBloc<AuthEvent, AuthState> implements AuthBloc {}
```

### Registering Fallback Values

Required for `any()` matcher with custom types:

```dart
void main() {
  setUpAll(() {
    // Register before tests run
    registerFallbackValue(LoginParams(email: '', password: ''));
    registerFallbackValue(User(id: '', name: '', email: ''));
    registerFallbackValue(FakeUri());
  });
}

// Fake class for complex types
class FakeUri extends Fake implements Uri {}
```

## Stubbing Methods

### Basic Stubbing

```dart
// Synchronous return
when(() => mockRepository.getUser()).thenReturn(user);

// Async return
when(() => mockRepository.fetchUser())
    .thenAnswer((_) async => user);

// Return Future directly
when(() => mockRepository.fetchUser())
    .thenAnswer((_) => Future.value(user));

// Throw exception
when(() => mockRepository.fetchUser())
    .thenThrow(ServerException());

// Async throw
when(() => mockRepository.fetchUser())
    .thenAnswer((_) async => throw ServerException());
```

### Stubbing with Arguments

```dart
// Any argument
when(() => mockRepository.getUserById(any()))
    .thenAnswer((_) async => user);

// Specific argument
when(() => mockRepository.getUserById('123'))
    .thenAnswer((_) async => user);

// Argument matching
when(() => mockRepository.getUserById(any(that: startsWith('user_'))))
    .thenAnswer((_) async => user);

// Multiple arguments
when(() => mockRepository.login(any(), any()))
    .thenAnswer((_) async => user);

// Named arguments
when(() => mockRepository.search(query: any(named: 'query')))
    .thenAnswer((_) async => []);
```

### Conditional Returns

```dart
// Different returns based on input
when(() => mockRepository.getUserById(any())).thenAnswer((invocation) async {
  final id = invocation.positionalArguments[0] as String;
  if (id == '1') return user1;
  if (id == '2') return user2;
  throw NotFoundException();
});

// Sequential returns
var callCount = 0;
when(() => mockRepository.fetchData()).thenAnswer((_) async {
  callCount++;
  if (callCount == 1) return 'first';
  return 'subsequent';
});
```

### Stubbing Getters and Setters

```dart
// Stub getter
when(() => mockService.isConnected).thenReturn(true);

// Stub stream getter
when(() => mockBloc.stream).thenAnswer((_) => Stream.value(state));

// Stub state getter (BLoC)
when(() => mockBloc.state).thenReturn(AuthInitial());
```

## Argument Matchers

### Basic Matchers

```dart
// Any value
any()

// Any value with type constraint
any<String>()

// Any value matching condition
any(that: isA<User>())
any(that: equals(expectedUser))
any(that: startsWith('test'))

// Named parameter
any(named: 'userId')
```

### Custom Matchers

```dart
// Matcher for specific conditions
any(that: predicate<User>((user) => user.age > 18))

// Combining matchers
any(that: allOf([
  isA<LoginParams>(),
  predicate<LoginParams>((p) => p.email.contains('@')),
]))
```

### Capturing Arguments

```dart
// Capture for later assertion
final captured = verify(() => mockRepository.saveUser(captureAny())).captured;
expect(captured.first, isA<User>());
expect((captured.first as User).name, 'Test');

// Multiple captures
verify(() => mockRepository.log(captureAny())).captured;
// captured is a List of all captured values
```

## Verification

### Basic Verification

```dart
// Verify called
verify(() => mockRepository.getUser()).called(1);

// Verify called multiple times
verify(() => mockRepository.log(any())).called(3);

// Verify never called
verifyNever(() => mockRepository.deleteUser(any()));

// Verify no more interactions
verifyNoMoreInteractions(mockRepository);
```

### Verification Order

```dart
// Verify calls happened in order
verifyInOrder([
  () => mockRepository.startTransaction(),
  () => mockRepository.saveUser(any()),
  () => mockRepository.commitTransaction(),
]);
```

### Verification with Matchers

```dart
// Verify with specific argument
verify(() => mockRepository.getUserById('123')).called(1);

// Verify with matcher
verify(() => mockRepository.getUserById(any(that: startsWith('user_')))).called(1);

// Verify and capture
final captured = verify(() => mockRepository.saveUser(captureAny())).captured;
expect(captured.single.email, 'test@test.com');
```

## Mocking Streams

```dart
// Mock stream
when(() => mockBloc.stream).thenAnswer(
  (_) => Stream.fromIterable([
    AuthLoading(),
    AuthAuthenticated(user),
  ]),
);

// Mock StreamController for more control
final controller = StreamController<AuthState>();
when(() => mockBloc.stream).thenAnswer((_) => controller.stream);

// Emit states
controller.add(AuthLoading());
controller.add(AuthAuthenticated(user));

// Clean up
await controller.close();
```

## Mocking HTTP Client

```dart
class MockDio extends Mock implements Dio {}

void main() {
  late MockDio mockDio;
  late UserRemoteDataSource dataSource;

  setUp(() {
    mockDio = MockDio();
    dataSource = UserRemoteDataSourceImpl(client: mockDio);
  });

  test('should return user on successful response', () async {
    // Arrange
    when(() => mockDio.get(any())).thenAnswer(
      (_) async => Response(
        data: {'id': '1', 'name': 'Test'},
        statusCode: 200,
        requestOptions: RequestOptions(path: '/user'),
      ),
    );

    // Act
    final result = await dataSource.getUser();

    // Assert
    expect(result.name, 'Test');
  });

  test('should throw on error response', () async {
    // Arrange
    when(() => mockDio.get(any())).thenThrow(
      DioException(
        type: DioExceptionType.badResponse,
        response: Response(
          statusCode: 404,
          requestOptions: RequestOptions(path: '/user'),
        ),
        requestOptions: RequestOptions(path: '/user'),
      ),
    );

    // Act & Assert
    expect(
      () => dataSource.getUser(),
      throwsA(isA<ServerException>()),
    );
  });
}
```

## Mocking BLoC for Widget Tests

```dart
import 'package:bloc_test/bloc_test.dart';

class MockAuthBloc extends MockBloc<AuthEvent, AuthState> implements AuthBloc {}

void main() {
  late MockAuthBloc mockBloc;

  setUp(() {
    mockBloc = MockAuthBloc();
  });

  testWidgets('shows loading indicator', (tester) async {
    // Stub state
    when(() => mockBloc.state).thenReturn(AuthLoading());

    await tester.pumpWidget(
      MaterialApp(
        home: BlocProvider<AuthBloc>.value(
          value: mockBloc,
          child: const LoginPage(),
        ),
      ),
    );

    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });

  testWidgets('dispatches event on button tap', (tester) async {
    when(() => mockBloc.state).thenReturn(AuthInitial());

    await tester.pumpWidget(
      MaterialApp(
        home: BlocProvider<AuthBloc>.value(
          value: mockBloc,
          child: const LoginPage(),
        ),
      ),
    );

    await tester.tap(find.byKey(Key('login_button')));

    verify(() => mockBloc.add(any(that: isA<LoginRequested>()))).called(1);
  });
}
```

## Anti-Patterns

### ❌ Over-mocking

```dart
// BAD: Mocking value objects
class MockUser extends Mock implements User {} // Don't do this

// GOOD: Use real value objects
final user = User(id: '1', name: 'Test', email: 'test@test.com');
```

### ✅ Mock Boundaries Only

```dart
// GOOD: Mock at architectural boundaries
class MockUserRepository extends Mock implements UserRepository {}
class MockHttpClient extends Mock implements Dio {}
```

### ❌ Forgetting Fallback Values

```dart
// BAD: Will fail with custom types
when(() => mock.method(any())).thenReturn(result);
// Error: type 'Null' is not a subtype of type 'LoginParams'
```

### ✅ Register Fallbacks

```dart
// GOOD: Register before using any()
setUpAll(() {
  registerFallbackValue(LoginParams(email: '', password: ''));
});

when(() => mock.method(any())).thenReturn(result); // Now works
```

## References

- See `unit-testing` skill for test structure
- See `bloc-testing` skill for BLoC mocks
- See `widget-testing` skill for widget test mocks
