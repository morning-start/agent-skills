---
name: error-handling
description: Either/Result pattern and Failure classes for error handling. Use when implementing error handling, creating failure types, or when user asks about "error handling", "Either", "failures", or "exceptions".
---

# Error Handling

## Overview

Clean Architecture uses the Either pattern to handle errors functionally. Exceptions occur in the data layer and are converted to Failures in the domain layer.

## Mandatory Pattern

### Exception Classes (Data Layer)

```dart
// lib/core/error/exceptions.dart

/// Base exception for all app exceptions
abstract class AppException implements Exception {
  final String message;
  final int? statusCode;

  const AppException({
    required this.message,
    this.statusCode,
  });

  @override
  String toString() => message;
}

/// Thrown when server returns an error
class ServerException extends AppException {
  const ServerException({
    super.message = 'Server error occurred',
    super.statusCode,
  });
}

/// Thrown when cache operation fails
class CacheException extends AppException {
  const CacheException({
    super.message = 'Cache error occurred',
  });
}

/// Thrown when authentication fails
class AuthException extends AppException {
  const AuthException({
    super.message = 'Authentication failed',
    super.statusCode,
  });
}

/// Thrown when resource is not found
class NotFoundException extends AppException {
  const NotFoundException({
    super.message = 'Resource not found',
    super.statusCode = 404,
  });
}

/// Thrown when request times out
class TimeoutException extends AppException {
  const TimeoutException({
    super.message = 'Request timed out',
  });
}

/// Thrown when input validation fails
class ValidationException extends AppException {
  final Map<String, String>? fieldErrors;

  const ValidationException({
    super.message = 'Validation failed',
    this.fieldErrors,
  });
}
```

### Failure Classes (Domain Layer)

```dart
// lib/core/error/failures.dart
import 'package:equatable/equatable.dart';

/// Base class for all failures
abstract class Failure extends Equatable {
  final String message;
  final int? code;

  const Failure({
    required this.message,
    this.code,
  });

  @override
  List<Object?> get props => [message, code];

  @override
  String toString() => message;
}

/// Server/API failures
class ServerFailure extends Failure {
  const ServerFailure([String message = 'Server error occurred', int? code])
      : super(message: message, code: code);
}

/// Network connectivity failures
class NetworkFailure extends Failure {
  const NetworkFailure([String message = 'No internet connection'])
      : super(message: message);
}

/// Cache/storage failures
class CacheFailure extends Failure {
  const CacheFailure([String message = 'Cache error occurred'])
      : super(message: message);
}

/// Authentication failures
class AuthFailure extends Failure {
  const AuthFailure([String message = 'Authentication failed', int? code])
      : super(message: message, code: code);
}

/// Validation failures
class ValidationFailure extends Failure {
  final Map<String, String>? fieldErrors;

  const ValidationFailure({
    String message = 'Validation failed',
    this.fieldErrors,
  }) : super(message: message);

  @override
  List<Object?> get props => [message, code, fieldErrors];
}

/// Resource not found failures
class NotFoundFailure extends Failure {
  const NotFoundFailure([String message = 'Resource not found'])
      : super(message: message, code: 404);
}

/// Unknown/unexpected failures
class UnknownFailure extends Failure {
  const UnknownFailure([String message = 'An unexpected error occurred'])
      : super(message: message);
}
```

## Using Either Pattern

### Setup with dartz

```yaml
# pubspec.yaml
dependencies:
  dartz: ^0.10.1
```

```dart
import 'package:dartz/dartz.dart';
```

### Repository Interface

```dart
// lib/features/auth/domain/repositories/auth_repository.dart
import 'package:dartz/dartz.dart';

abstract class AuthRepository {
  /// Returns [Right(User)] on success, [Left(Failure)] on error
  Future<Either<Failure, User>> login(String email, String password);

  /// Returns [Right(void)] on success, [Left(Failure)] on error
  Future<Either<Failure, void>> logout();

  /// Returns [Right(User?)] - null if not logged in
  Future<Either<Failure, User?>> getCurrentUser();
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
    if (!await networkInfo.isConnected) {
      return const Left(NetworkFailure());
    }

    try {
      final userModel = await remoteDataSource.login(email, password);
      await localDataSource.cacheUser(userModel);
      return Right(userModel.toEntity());
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message, e.statusCode));
    } on AuthException catch (e) {
      return Left(AuthFailure(e.message, e.statusCode));
    } on TimeoutException {
      return const Left(ServerFailure('Request timed out'));
    } catch (e) {
      return Left(UnknownFailure(e.toString()));
    }
  }
}
```

### Use Case

```dart
// lib/features/auth/domain/usecases/login_user.dart
class LoginUser implements UseCase<User, LoginParams> {
  final AuthRepository repository;

  LoginUser(this.repository);

  @override
  Future<Either<Failure, User>> call(LoginParams params) {
    return repository.login(params.email, params.password);
  }
}
```

### BLoC Handling

```dart
// lib/features/auth/presentation/bloc/auth_bloc.dart
Future<void> _onLoginRequested(
  LoginRequested event,
  Emitter<AuthState> emit,
) async {
  emit(AuthLoading());

  final result = await loginUser(LoginParams(
    email: event.email,
    password: event.password,
  ));

  // fold handles both cases
  result.fold(
    (failure) => emit(AuthError(_mapFailureToMessage(failure))),
    (user) => emit(AuthAuthenticated(user)),
  );
}

String _mapFailureToMessage(Failure failure) {
  return switch (failure) {
    NetworkFailure() => 'Please check your internet connection',
    AuthFailure() => 'Invalid email or password',
    ServerFailure(:final message) => message,
    _ => 'An unexpected error occurred',
  };
}
```

## Either Operations

### Basic fold

```dart
final result = await repository.getUser(id);

result.fold(
  (failure) => print('Error: ${failure.message}'),
  (user) => print('User: ${user.name}'),
);
```

### getOrElse

```dart
final user = result.getOrElse(() => User.empty());
```

### map and flatMap

```dart
// Transform success value
final nameResult = result.map((user) => user.name);

// Chain operations
final addressResult = result.flatMap((user) =>
  repository.getAddress(user.addressId)
);
```

### isLeft / isRight

```dart
if (result.isRight()) {
  // Handle success
}

if (result.isLeft()) {
  // Handle failure
}
```

### Combine Multiple Results

```dart
Future<Either<Failure, UserWithPosts>> getUserWithPosts(String userId) async {
  final userResult = await userRepository.getUser(userId);

  return userResult.fold(
    (failure) => Left(failure),
    (user) async {
      final postsResult = await postRepository.getUserPosts(userId);
      return postsResult.fold(
        (failure) => Left(failure),
        (posts) => Right(UserWithPosts(user: user, posts: posts)),
      );
    },
  );
}
```

## Error Mapping Utility

```dart
// lib/core/utils/error_mapper.dart
class ErrorMapper {
  static Failure mapExceptionToFailure(Object exception) {
    return switch (exception) {
      ServerException e => ServerFailure(e.message, e.statusCode),
      AuthException e => AuthFailure(e.message, e.statusCode),
      CacheException e => CacheFailure(e.message),
      NotFoundException e => NotFoundFailure(e.message),
      TimeoutException _ => const ServerFailure('Request timed out'),
      DioException e => _mapDioException(e),
      _ => UnknownFailure(exception.toString()),
    };
  }

  static Failure _mapDioException(DioException e) {
    return switch (e.type) {
      DioExceptionType.connectionTimeout ||
      DioExceptionType.sendTimeout ||
      DioExceptionType.receiveTimeout =>
        const ServerFailure('Request timed out'),
      DioExceptionType.connectionError => const NetworkFailure(),
      DioExceptionType.badResponse => _mapStatusCode(e.response?.statusCode),
      _ => ServerFailure(e.message ?? 'Network error'),
    };
  }

  static Failure _mapStatusCode(int? statusCode) {
    return switch (statusCode) {
      401 => const AuthFailure('Session expired'),
      403 => const AuthFailure('Access denied'),
      404 => const NotFoundFailure(),
      422 => const ValidationFailure(),
      >= 500 => const ServerFailure('Server error'),
      _ => const ServerFailure(),
    };
  }
}
```

## Anti-Patterns

### ❌ Throwing Exceptions from Domain Layer

```dart
// BAD: Domain should not throw
class LoginUser {
  Future<User> call(params) async {
    throw AuthFailure(); // Don't do this
  }
}
```

### ✅ Return Either

```dart
// GOOD: Return Either
class LoginUser {
  Future<Either<Failure, User>> call(params) async {
    return Left(AuthFailure()); // Correct
  }
}
```

### ❌ Catching Generic Exception

```dart
// BAD: Too broad
try {
  // ...
} catch (e) {
  return Left(UnknownFailure()); // Loses information
}
```

### ✅ Catch Specific Exceptions

```dart
// GOOD: Specific handling
try {
  // ...
} on ServerException catch (e) {
  return Left(ServerFailure(e.message));
} on AuthException catch (e) {
  return Left(AuthFailure(e.message));
} catch (e) {
  return Left(UnknownFailure(e.toString())); // Last resort
}
```

## References

- See `repository-pattern` skill for repository implementation
- See `bloc-architecture` skill for BLoC error handling
- See `api-layer` skill for HTTP error handling
