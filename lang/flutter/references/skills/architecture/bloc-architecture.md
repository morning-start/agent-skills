---
name: bloc-architecture
description: BLoC pattern implementation with events, states, and best practices. Use when implementing state management with BLoC, creating new BLoCs, or when user asks about "BLoC", "events", "states", or "flutter_bloc".
---

# BLoC Architecture

## Overview

BLoC (Business Logic Component) separates business logic from UI using streams of events and states. It provides predictable state management with clear data flow.

## Mandatory Pattern

### BLoC Structure

```
presentation/
└── bloc/
    ├── auth_bloc.dart      # Main BLoC class
    ├── auth_event.dart     # Events (inputs)
    └── auth_state.dart     # States (outputs)
```

### Events (Inputs)

Events represent user actions or system triggers:

```dart
// lib/features/auth/presentation/bloc/auth_event.dart
part of 'auth_bloc.dart';

/// Base class for all auth events.
/// Use sealed class for exhaustive pattern matching.
sealed class AuthEvent {}

/// Triggered when user submits login form.
class LoginRequested extends AuthEvent {
  final String email;
  final String password;

  LoginRequested({
    required this.email,
    required this.password,
  });
}

/// Triggered when user taps logout button.
class LogoutRequested extends AuthEvent {}

/// Triggered on app start to check auth status.
class AuthCheckRequested extends AuthEvent {}

/// Triggered when auth token is refreshed.
class TokenRefreshed extends AuthEvent {
  final String token;
  TokenRefreshed(this.token);
}
```

### States (Outputs)

States represent UI conditions:

```dart
// lib/features/auth/presentation/bloc/auth_state.dart
part of 'auth_bloc.dart';

/// Base class for all auth states.
/// Use sealed class for exhaustive pattern matching.
sealed class AuthState {}

/// Initial state before any auth check.
class AuthInitial extends AuthState {}

/// Loading state during auth operations.
class AuthLoading extends AuthState {}

/// Authenticated state with user data.
class AuthAuthenticated extends AuthState {
  final User user;
  AuthAuthenticated(this.user);
}

/// Unauthenticated state (logged out or session expired).
class AuthUnauthenticated extends AuthState {}

/// Error state with failure message.
class AuthError extends AuthState {
  final String message;
  AuthError(this.message);
}
```

### BLoC Implementation

```dart
// lib/features/auth/presentation/bloc/auth_bloc.dart
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/usecases/login_user.dart';
import '../../domain/usecases/logout_user.dart';
import '../../domain/usecases/get_current_user.dart';

part 'auth_event.dart';
part 'auth_state.dart';

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
      (failure) => emit(AuthError(failure.message)),
      (user) => emit(AuthAuthenticated(user)),
    );
  }

  Future<void> _onLogoutRequested(
    LogoutRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());

    final result = await logoutUser(NoParams());

    result.fold(
      (failure) => emit(AuthError(failure.message)),
      (_) => emit(AuthUnauthenticated()),
    );
  }

  Future<void> _onAuthCheckRequested(
    AuthCheckRequested event,
    Emitter<AuthState> emit,
  ) async {
    final result = await getCurrentUser(NoParams());

    result.fold(
      (failure) => emit(AuthUnauthenticated()),
      (user) => user != null
          ? emit(AuthAuthenticated(user))
          : emit(AuthUnauthenticated()),
    );
  }
}
```

## Using BLoC in Widgets

### Providing BLoC

```dart
// At route level (recommended)
BlocProvider(
  create: (context) => sl<AuthBloc>()..add(AuthCheckRequested()),
  child: const LoginPage(),
)

// Multiple BLoCs
MultiBlocProvider(
  providers: [
    BlocProvider(create: (_) => sl<AuthBloc>()),
    BlocProvider(create: (_) => sl<ThemeBloc>()),
  ],
  child: const MyApp(),
)
```

### Consuming BLoC State

```dart
// BlocBuilder - Rebuilds on state change
BlocBuilder<AuthBloc, AuthState>(
  builder: (context, state) => switch (state) {
    AuthInitial() => const SizedBox(),
    AuthLoading() => const CircularProgressIndicator(),
    AuthAuthenticated(:final user) => Text('Welcome, ${user.name}'),
    AuthUnauthenticated() => const LoginForm(),
    AuthError(:final message) => Text('Error: $message'),
  },
)

// BlocListener - Side effects only (no rebuild)
BlocListener<AuthBloc, AuthState>(
  listener: (context, state) {
    if (state is AuthAuthenticated) {
      context.go('/home');
    }
    if (state is AuthError) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.message)),
      );
    }
  },
  child: const LoginForm(),
)

// BlocConsumer - Both builder and listener
BlocConsumer<AuthBloc, AuthState>(
  listener: (context, state) {
    if (state is AuthAuthenticated) {
      context.go('/home');
    }
  },
  builder: (context, state) => switch (state) {
    AuthLoading() => const CircularProgressIndicator(),
    _ => const LoginForm(),
  },
)
```

### Dispatching Events

```dart
// Using context.read (recommended for event dispatch)
ElevatedButton(
  onPressed: () {
    context.read<AuthBloc>().add(LoginRequested(
      email: _emailController.text,
      password: _passwordController.text,
    ));
  },
  child: const Text('Login'),
)

// Never use context.watch in callbacks
// ❌ BAD: context.watch<AuthBloc>().add(...)
// ✅ GOOD: context.read<AuthBloc>().add(...)
```

### Selective Rebuilds

```dart
// buildWhen - Control when to rebuild
BlocBuilder<AuthBloc, AuthState>(
  buildWhen: (previous, current) {
    // Only rebuild when state type changes
    return previous.runtimeType != current.runtimeType;
  },
  builder: (context, state) => ...,
)

// listenWhen - Control when to trigger listener
BlocListener<AuthBloc, AuthState>(
  listenWhen: (previous, current) {
    // Only listen to error states
    return current is AuthError;
  },
  listener: (context, state) => ...,
  child: ...,
)

// BlocSelector - Select specific data
BlocSelector<AuthBloc, AuthState, String?>(
  selector: (state) {
    if (state is AuthAuthenticated) {
      return state.user.name;
    }
    return null;
  },
  builder: (context, userName) {
    return Text(userName ?? 'Guest');
  },
)
```

## Advanced Patterns

### Event Transformers

```dart
class SearchBloc extends Bloc<SearchEvent, SearchState> {
  SearchBloc() : super(SearchInitial()) {
    // Debounce search queries
    on<SearchQueryChanged>(
      _onSearchQueryChanged,
      transformer: debounce(const Duration(milliseconds: 300)),
    );
  }
}

// Debounce transformer
EventTransformer<E> debounce<E>(Duration duration) {
  return (events, mapper) {
    return events.debounceTime(duration).flatMap(mapper);
  };
}
```

### Concurrent vs Sequential Events

```dart
class DataBloc extends Bloc<DataEvent, DataState> {
  DataBloc() : super(DataInitial()) {
    // Sequential (default) - waits for previous to complete
    on<LoadData>(_onLoadData);

    // Concurrent - processes simultaneously
    on<RefreshData>(
      _onRefreshData,
      transformer: concurrent(),
    );

    // Droppable - ignores new events while processing
    on<SubmitForm>(
      _onSubmitForm,
      transformer: droppable(),
    );

    // Restartable - cancels previous, starts new
    on<SearchQuery>(
      _onSearchQuery,
      transformer: restartable(),
    );
  }
}
```

### BLoC Communication

```dart
// Using BlocListener to react to another BLoC
BlocListener<AuthBloc, AuthState>(
  listener: (context, state) {
    if (state is AuthUnauthenticated) {
      // Clear user data when logged out
      context.read<UserDataBloc>().add(ClearUserData());
    }
  },
  child: ...,
)

// Or in BLoC constructor with stream subscription
class UserDataBloc extends Bloc<UserDataEvent, UserDataState> {
  final AuthBloc authBloc;
  late StreamSubscription authSubscription;

  UserDataBloc({required this.authBloc}) : super(UserDataInitial()) {
    authSubscription = authBloc.stream.listen((authState) {
      if (authState is AuthUnauthenticated) {
        add(ClearUserData());
      }
    });
  }

  @override
  Future<void> close() {
    authSubscription.cancel();
    return super.close();
  }
}
```

## Anti-Patterns

### ❌ Business Logic in UI

```dart
// BAD: Logic in widget
onPressed: () async {
  final result = await repository.login(email, password);
  if (result.isRight) {
    context.go('/home');
  }
}
```

### ✅ Business Logic in BLoC

```dart
// GOOD: UI only dispatches events
onPressed: () {
  context.read<AuthBloc>().add(LoginRequested(
    email: email,
    password: password,
  ));
}
```

### ❌ Mutable State

```dart
// BAD: Mutating state
class CounterState {
  int count = 0; // Mutable!
}

// In bloc
state.count++; // Mutating existing state
emit(state);
```

### ✅ Immutable State

```dart
// GOOD: Immutable state
class CounterState {
  final int count;
  const CounterState(this.count);
}

// In bloc
emit(CounterState(state.count + 1)); // New state object
```

### ❌ Using context.watch in Callbacks

```dart
// BAD: Can cause issues
onPressed: () {
  context.watch<AuthBloc>().add(...); // Don't do this!
}
```

### ✅ Using context.read in Callbacks

```dart
// GOOD: Safe for callbacks
onPressed: () {
  context.read<AuthBloc>().add(...);
}
```

## Testing

See `bloc-testing` skill for comprehensive testing patterns.

```dart
blocTest<AuthBloc, AuthState>(
  'emits [Loading, Authenticated] when login succeeds',
  build: () {
    when(() => mockLoginUser(any()))
        .thenAnswer((_) async => Right(tUser));
    return AuthBloc(loginUser: mockLoginUser, ...);
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
```

## References

- See `bloc-testing` skill for testing patterns
- See `clean-architecture` skill for layer integration
- See `dependency-injection` skill for BLoC registration
