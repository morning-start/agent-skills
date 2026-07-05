---
description: Generate test file for any source file
argument-hint: <source-file-path>
allowed-tools: Bash, Write, Read
---

# /generate-test Command

Generate a test file with boilerplate for any source file.

## Instructions

When the user runs `/generate-test <source-file-path>`:

1. **Read Source File**
   - Parse the source file to understand:
     - Class name and type (UseCase, Repository, BLoC, Widget, etc.)
     - Dependencies (constructor parameters)
     - Public methods to test
     - Return types

2. **Determine Test File Path**
   ```
   lib/features/auth/domain/usecases/login_user.dart
   → test/features/auth/domain/usecases/login_user_test.dart

   lib/features/auth/presentation/bloc/auth_bloc.dart
   → test/features/auth/presentation/bloc/auth_bloc_test.dart
   ```

3. **Generate Test Based on Type**

### For UseCase:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dartz/dartz.dart';

import 'package:your_app/features/auth/domain/usecases/login_user.dart';
import 'package:your_app/features/auth/domain/repositories/auth_repository.dart';
import 'package:your_app/features/auth/domain/entities/user.dart';
import 'package:your_app/core/error/failures.dart';

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

  // Test fixtures
  final tUser = User(id: '1', name: 'Test', email: 'test@test.com');

  group('LoginUser', () {
    test('should return User when login is successful', () async {
      // Arrange
      when(() => mockRepository.login(any(), any()))
          .thenAnswer((_) async => Right(tUser));

      // Act
      final result = await usecase(LoginParams(
        email: 'test@test.com',
        password: 'password',
      ));

      // Assert
      expect(result, Right(tUser));
      verify(() => mockRepository.login('test@test.com', 'password')).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return Failure when login fails', () async {
      // Arrange
      when(() => mockRepository.login(any(), any()))
          .thenAnswer((_) async => Left(ServerFailure('Invalid credentials')));

      // Act
      final result = await usecase(LoginParams(
        email: 'test@test.com',
        password: 'wrong',
      ));

      // Assert
      expect(result.isLeft(), true);
    });
  });
}
```

### For BLoC:

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dartz/dartz.dart';

import 'package:your_app/features/auth/presentation/bloc/auth_bloc.dart';
import 'package:your_app/features/auth/domain/usecases/login_user.dart';
import 'package:your_app/features/auth/domain/entities/user.dart';
import 'package:your_app/core/error/failures.dart';

class MockLoginUser extends Mock implements LoginUser {}

class FakeLoginParams extends Fake implements LoginParams {}

void main() {
  late AuthBloc bloc;
  late MockLoginUser mockLoginUser;

  setUp(() {
    mockLoginUser = MockLoginUser();
    bloc = AuthBloc(loginUser: mockLoginUser);
  });

  setUpAll(() {
    registerFallbackValue(FakeLoginParams());
  });

  tearDown(() {
    bloc.close();
  });

  final tUser = User(id: '1', name: 'Test', email: 'test@test.com');

  test('initial state should be AuthInitial', () {
    expect(bloc.state, AuthInitial());
  });

  group('LoginRequested', () {
    blocTest<AuthBloc, AuthState>(
      'emits [AuthLoading, AuthAuthenticated] when login succeeds',
      build: () {
        when(() => mockLoginUser(any()))
            .thenAnswer((_) async => Right(tUser));
        return AuthBloc(loginUser: mockLoginUser);
      },
      act: (bloc) => bloc.add(LoginRequested(
        email: 'test@test.com',
        password: 'password',
      )),
      expect: () => [
        AuthLoading(),
        AuthAuthenticated(tUser),
      ],
    );

    blocTest<AuthBloc, AuthState>(
      'emits [AuthLoading, AuthError] when login fails',
      build: () {
        when(() => mockLoginUser(any()))
            .thenAnswer((_) async => Left(ServerFailure('error')));
        return AuthBloc(loginUser: mockLoginUser);
      },
      act: (bloc) => bloc.add(LoginRequested(
        email: 'test@test.com',
        password: 'password',
      )),
      expect: () => [
        AuthLoading(),
        AuthError('error'),
      ],
    );
  });
}
```

### For Widget:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:bloc_test/bloc_test.dart';

import 'package:your_app/features/auth/presentation/pages/login_page.dart';
import 'package:your_app/features/auth/presentation/bloc/auth_bloc.dart';

class MockAuthBloc extends MockBloc<AuthEvent, AuthState> implements AuthBloc {}

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
    testWidgets('shows loading indicator when loading', (tester) async {
      when(() => mockBloc.state).thenReturn(AuthLoading());

      await tester.pumpWidget(createWidget());

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('shows form when initial', (tester) async {
      when(() => mockBloc.state).thenReturn(AuthInitial());

      await tester.pumpWidget(createWidget());

      expect(find.byType(TextField), findsWidgets);
      expect(find.byType(ElevatedButton), findsOneWidget);
    });

    testWidgets('dispatches LoginRequested on button tap', (tester) async {
      when(() => mockBloc.state).thenReturn(AuthInitial());

      await tester.pumpWidget(createWidget());

      await tester.enterText(find.byKey(Key('email_field')), 'test@test.com');
      await tester.enterText(find.byKey(Key('password_field')), 'password');
      await tester.tap(find.byType(ElevatedButton));

      verify(() => mockBloc.add(any(that: isA<LoginRequested>()))).called(1);
    });
  });
}
```

### For Repository:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dartz/dartz.dart';

import 'package:your_app/features/auth/data/repositories/auth_repository_impl.dart';
import 'package:your_app/features/auth/data/datasources/auth_remote_datasource.dart';
import 'package:your_app/features/auth/data/models/user_model.dart';
import 'package:your_app/core/network/network_info.dart';
import 'package:your_app/core/error/exceptions.dart';
import 'package:your_app/core/error/failures.dart';

class MockAuthRemoteDataSource extends Mock implements AuthRemoteDataSource {}
class MockNetworkInfo extends Mock implements NetworkInfo {}

void main() {
  late AuthRepositoryImpl repository;
  late MockAuthRemoteDataSource mockRemoteDataSource;
  late MockNetworkInfo mockNetworkInfo;

  setUp(() {
    mockRemoteDataSource = MockAuthRemoteDataSource();
    mockNetworkInfo = MockNetworkInfo();
    repository = AuthRepositoryImpl(
      remoteDataSource: mockRemoteDataSource,
      networkInfo: mockNetworkInfo,
    );
  });

  final tUserModel = UserModel(id: '1', name: 'Test', email: 'test@test.com');
  final tUser = tUserModel.toEntity();

  group('login', () {
    group('device is online', () {
      setUp(() {
        when(() => mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      });

      test('should return user when call is successful', () async {
        when(() => mockRemoteDataSource.login(any(), any()))
            .thenAnswer((_) async => tUserModel);

        final result = await repository.login('email', 'password');

        expect(result, Right(tUser));
      });

      test('should return ServerFailure when call fails', () async {
        when(() => mockRemoteDataSource.login(any(), any()))
            .thenThrow(ServerException(message: 'error'));

        final result = await repository.login('email', 'password');

        expect(result, Left(ServerFailure('error')));
      });
    });

    group('device is offline', () {
      test('should return NetworkFailure', () async {
        when(() => mockNetworkInfo.isConnected).thenAnswer((_) async => false);

        final result = await repository.login('email', 'password');

        expect(result, Left(NetworkFailure('No internet connection')));
      });
    });
  });
}
```

4. **Output Summary**

```
Test file created: test/features/<feature>/.../<file>_test.dart

Structure:
- Imports configured
- Mock classes generated
- setUp/tearDown configured
- Test fixtures added
- Test cases for:
  - Success scenarios
  - Failure scenarios
  - Edge cases (if applicable)

Run tests:
flutter test test/features/<feature>/.../<file>_test.dart
```
