---
name: bloc-testing
description: BLoC state transition testing with bloc_test package. Use when testing BLoCs, Cubits, or state management logic. Covers blocTest, state verification, and mock setup.
---

# BLoC Testing

## Overview

BLoC testing verifies state transitions in response to events. The `bloc_test` package provides `blocTest` for declarative testing of BLoC behavior.

## Mandatory Setup

### Dependencies

```yaml
# pubspec.yaml
dev_dependencies:
  bloc_test: ^9.1.0
  mocktail: ^1.0.0
  flutter_test:
    sdk: flutter
```

### Test File Structure

```dart
// test/features/auth/presentation/bloc/auth_bloc_test.dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dartz/dartz.dart';

import 'package:your_app/features/auth/presentation/bloc/auth_bloc.dart';
import 'package:your_app/features/auth/domain/usecases/login_user.dart';
import 'package:your_app/features/auth/domain/entities/user.dart';
import 'package:your_app/core/error/failures.dart';

// Mock classes
class MockLoginUser extends Mock implements LoginUser {}
class MockLogoutUser extends Mock implements LogoutUser {}

// Fake classes for fallback values
class FakeLoginParams extends Fake implements LoginParams {}

void main() {
  late AuthBloc bloc;
  late MockLoginUser mockLoginUser;
  late MockLogoutUser mockLogoutUser;

  setUp(() {
    mockLoginUser = MockLoginUser();
    mockLogoutUser = MockLogoutUser();
    bloc = AuthBloc(
      loginUser: mockLoginUser,
      logoutUser: mockLogoutUser,
    );
  });

  setUpAll(() {
    registerFallbackValue(FakeLoginParams());
  });

  tearDown(() {
    bloc.close();
  });

  // Tests here
}
```

## blocTest Patterns

### Basic State Transition Test

```dart
blocTest<AuthBloc, AuthState>(
  'emits [AuthLoading, AuthAuthenticated] when LoginRequested succeeds',
  build: () {
    when(() => mockLoginUser(any()))
        .thenAnswer((_) async => Right(tUser));
    return AuthBloc(loginUser: mockLoginUser, logoutUser: mockLogoutUser);
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

### Testing Error States

```dart
blocTest<AuthBloc, AuthState>(
  'emits [AuthLoading, AuthError] when LoginRequested fails',
  build: () {
    when(() => mockLoginUser(any()))
        .thenAnswer((_) async => Left(ServerFailure('Invalid credentials')));
    return AuthBloc(loginUser: mockLoginUser, logoutUser: mockLogoutUser);
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

### Testing Initial State

```dart
test('initial state should be AuthInitial', () {
  expect(bloc.state, AuthInitial());
});

// Or with blocTest
blocTest<AuthBloc, AuthState>(
  'initial state is AuthInitial',
  build: () => AuthBloc(loginUser: mockLoginUser, logoutUser: mockLogoutUser),
  verify: (bloc) => expect(bloc.state, AuthInitial()),
);
```

### Testing with Seed State

```dart
blocTest<AuthBloc, AuthState>(
  'emits [AuthUnauthenticated] when LogoutRequested from authenticated state',
  build: () {
    when(() => mockLogoutUser(any()))
        .thenAnswer((_) async => const Right(null));
    return AuthBloc(loginUser: mockLoginUser, logoutUser: mockLogoutUser);
  },
  seed: () => AuthAuthenticated(tUser), // Start from authenticated state
  act: (bloc) => bloc.add(LogoutRequested()),
  expect: () => [
    AuthLoading(),
    AuthUnauthenticated(),
  ],
);
```

### Testing Multiple Events

```dart
blocTest<CounterBloc, int>(
  'emits [1, 2, 3] when Increment is added three times',
  build: () => CounterBloc(),
  act: (bloc) {
    bloc.add(Increment());
    bloc.add(Increment());
    bloc.add(Increment());
  },
  expect: () => [1, 2, 3],
);

// With delays between events
blocTest<SearchBloc, SearchState>(
  'emits states correctly with delayed events',
  build: () => SearchBloc(),
  act: (bloc) async {
    bloc.add(SearchQueryChanged('a'));
    await Future.delayed(const Duration(milliseconds: 100));
    bloc.add(SearchQueryChanged('ab'));
    await Future.delayed(const Duration(milliseconds: 100));
    bloc.add(SearchQueryChanged('abc'));
  },
  wait: const Duration(milliseconds: 500), // Wait for debounce
  expect: () => [
    SearchLoading(),
    SearchResults(['abc results']),
  ],
);
```

### Verifying Mock Calls

```dart
blocTest<AuthBloc, AuthState>(
  'calls loginUser with correct parameters',
  build: () {
    when(() => mockLoginUser(any()))
        .thenAnswer((_) async => Right(tUser));
    return AuthBloc(loginUser: mockLoginUser, logoutUser: mockLogoutUser);
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

### Testing with wait Parameter

```dart
blocTest<SearchBloc, SearchState>(
  'emits results after debounce period',
  build: () {
    when(() => mockSearch(any()))
        .thenAnswer((_) async => Right(['result']));
    return SearchBloc(search: mockSearch);
  },
  act: (bloc) => bloc.add(SearchQueryChanged('test')),
  wait: const Duration(milliseconds: 350), // Wait for debounce
  expect: () => [
    SearchLoading(),
    SearchResults(['result']),
  ],
);
```

### Testing Skip Initial States

```dart
blocTest<AuthBloc, AuthState>(
  'emits [AuthAuthenticated] skipping loading state',
  build: () {
    when(() => mockLoginUser(any()))
        .thenAnswer((_) async => Right(tUser));
    return AuthBloc(loginUser: mockLoginUser, logoutUser: mockLogoutUser);
  },
  act: (bloc) => bloc.add(LoginRequested(
    email: 'test@test.com',
    password: 'password',
  )),
  skip: 1, // Skip AuthLoading
  expect: () => [
    AuthAuthenticated(tUser),
  ],
);
```

## Testing Cubit

```dart
// Cubit is simpler - no events, just methods
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);

  void increment() => emit(state + 1);
  void decrement() => emit(state - 1);
}

// Test
blocTest<CounterCubit, int>(
  'emits [1] when increment is called',
  build: () => CounterCubit(),
  act: (cubit) => cubit.increment(),
  expect: () => [1],
);

blocTest<CounterCubit, int>(
  'emits [1, 2, 3] when increment is called three times',
  build: () => CounterCubit(),
  act: (cubit) {
    cubit.increment();
    cubit.increment();
    cubit.increment();
  },
  expect: () => [1, 2, 3],
);
```

## Testing State Equality

### With Equatable

```dart
// State with Equatable (recommended)
class AuthAuthenticated extends AuthState with EquatableMixin {
  final User user;
  AuthAuthenticated(this.user);

  @override
  List<Object?> get props => [user];
}

// Test works with value equality
expect: () => [
  AuthLoading(),
  AuthAuthenticated(User(id: '1', name: 'Test')), // Matches by value
],
```

### Without Equatable

```dart
// Without Equatable, use matchers
blocTest<AuthBloc, AuthState>(
  'emits loading then authenticated',
  build: () => bloc,
  act: (bloc) => bloc.add(LoginRequested(...)),
  expect: () => [
    isA<AuthLoading>(),
    isA<AuthAuthenticated>().having(
      (s) => s.user.id,
      'user id',
      '1',
    ),
  ],
);
```

## Testing Error Handling

```dart
blocTest<DataBloc, DataState>(
  'emits [Error] when exception is thrown',
  build: () {
    when(() => mockUseCase(any()))
        .thenThrow(Exception('Unexpected error'));
    return DataBloc(useCase: mockUseCase);
  },
  act: (bloc) => bloc.add(LoadData()),
  expect: () => [
    DataLoading(),
    isA<DataError>(),
  ],
  errors: () => [isA<Exception>()], // Verify errors were thrown
);
```

## Testing Transformers

```dart
blocTest<SearchBloc, SearchState>(
  'debounces search queries',
  build: () {
    when(() => mockSearch(any()))
        .thenAnswer((_) async => Right(['result']));
    return SearchBloc(search: mockSearch);
  },
  act: (bloc) async {
    // Rapid fire events
    bloc.add(SearchQueryChanged('a'));
    bloc.add(SearchQueryChanged('ab'));
    bloc.add(SearchQueryChanged('abc'));
  },
  wait: const Duration(milliseconds: 350),
  expect: () => [
    SearchLoading(),
    SearchResults(['result']), // Only one result due to debounce
  ],
  verify: (_) {
    // Should only call search once with final query
    verify(() => mockSearch('abc')).called(1);
    verifyNever(() => mockSearch('a'));
    verifyNever(() => mockSearch('ab'));
  },
);
```

## Testing BLoC with Stream Dependencies

```dart
blocTest<UserBloc, UserState>(
  'updates when auth state changes',
  build: () {
    final authStateController = StreamController<AuthState>();
    when(() => mockAuthBloc.stream)
        .thenAnswer((_) => authStateController.stream);
    when(() => mockAuthBloc.state).thenReturn(AuthInitial());

    return UserBloc(authBloc: mockAuthBloc);
  },
  act: (bloc) async {
    // Simulate auth state change
    // This would typically be done through the mock
  },
  expect: () => [...],
);
```

## Anti-Patterns

### ❌ Testing Implementation Details

```dart
// BAD: Testing internal state
blocTest<AuthBloc, AuthState>(
  'sets internal flag',
  verify: (bloc) {
    expect(bloc._isLoading, true); // Don't test private state
  },
);
```

### ✅ Test Observable Behavior

```dart
// GOOD: Test emitted states
blocTest<AuthBloc, AuthState>(
  'emits loading state',
  expect: () => [
    isA<AuthLoading>(), // Test public state
  ],
);
```

### ❌ Not Closing BLoC

```dart
// BAD: Memory leak
void main() {
  late AuthBloc bloc;

  setUp(() {
    bloc = AuthBloc(); // Created but never closed
  });
}
```

### ✅ Always Close BLoC

```dart
// GOOD: Proper cleanup
void main() {
  late AuthBloc bloc;

  setUp(() {
    bloc = AuthBloc();
  });

  tearDown(() {
    bloc.close(); // Always close
  });
}
```

## Running BLoC Tests

```bash
# Run all bloc tests
flutter test test/features/*/presentation/bloc/

# Run specific bloc test
flutter test test/features/auth/presentation/bloc/auth_bloc_test.dart

# Run with coverage
flutter test --coverage test/features/*/presentation/bloc/
```

## References

- See `unit-testing` skill for general test patterns
- See `mocking-patterns` skill for mock setup
- See `bloc-architecture` skill for BLoC implementation
