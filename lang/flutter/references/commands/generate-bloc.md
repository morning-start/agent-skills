---
description: Scaffold a BLoC with events, states, and test file
argument-hint: <bloc-name>
allowed-tools: Bash, Write, Read
---

# /generate-bloc Command

Generate a complete BLoC with events, states, and test file.

## Instructions

When the user runs `/generate-bloc <bloc-name>`:

1. **Parse Arguments**
   - Extract bloc name (e.g., `auth`, `login`, `user_profile`)
   - Convert to proper naming: `auth` → `AuthBloc`, `auth_event.dart`, etc.

2. **Determine Location**
   - Ask user for feature name if not obvious
   - Default path: `lib/features/<feature>/presentation/bloc/`

3. **Generate BLoC Event File**

Create `lib/features/<feature>/presentation/bloc/<name>_event.dart`:
```dart
part of '<name>_bloc.dart';

/// Base class for all <Name>Bloc events.
sealed class <Name>Event {}

/// Event to load initial data.
class Load<Name> extends <Name>Event {}

/// Event to refresh data.
class Refresh<Name> extends <Name>Event {}

// Add more events as needed:
// class Submit<Name> extends <Name>Event {
//   final <Type> data;
//   Submit<Name>(this.data);
// }
```

4. **Generate BLoC State File**

Create `lib/features/<feature>/presentation/bloc/<name>_state.dart`:
```dart
part of '<name>_bloc.dart';

/// Base class for all <Name>Bloc states.
sealed class <Name>State {}

/// Initial state before any action.
class <Name>Initial extends <Name>State {}

/// Loading state while fetching data.
class <Name>Loading extends <Name>State {}

/// Success state with loaded data.
class <Name>Success extends <Name>State {
  final dynamic data; // Replace with actual type
  <Name>Success(this.data);
}

/// Error state with failure message.
class <Name>Error extends <Name>State {
  final String message;
  <Name>Error(this.message);
}
```

5. **Generate BLoC File**

Create `lib/features/<feature>/presentation/bloc/<name>_bloc.dart`:
```dart
import 'package:flutter_bloc/flutter_bloc.dart';
// Import use cases
// import '../../domain/usecases/<usecase>.dart';

part '<name>_event.dart';
part '<name>_state.dart';

class <Name>Bloc extends Bloc<<Name>Event, <Name>State> {
  // final <UseCase> useCase;

  <Name>Bloc({
    // required this.useCase,
  }) : super(<Name>Initial()) {
    on<Load<Name>>(_onLoad);
    on<Refresh<Name>>(_onRefresh);
  }

  Future<void> _onLoad(
    Load<Name> event,
    Emitter<<Name>State> emit,
  ) async {
    emit(<Name>Loading());

    // TODO: Call use case and handle result
    // final result = await useCase(params);
    // result.fold(
    //   (failure) => emit(<Name>Error(failure.message)),
    //   (data) => emit(<Name>Success(data)),
    // );

    // Placeholder success
    await Future.delayed(const Duration(seconds: 1));
    emit(<Name>Success('data'));
  }

  Future<void> _onRefresh(
    Refresh<Name> event,
    Emitter<<Name>State> emit,
  ) async {
    // TODO: Implement refresh logic
    // Unlike Load, don't emit Loading to preserve current data
    // final result = await useCase(params);
    // result.fold(
    //   (failure) => emit(<Name>Error(failure.message)),
    //   (data) => emit(<Name>Success(data)),
    // );
  }
}
```

6. **Generate BLoC Test File**

Create `test/features/<feature>/presentation/bloc/<name>_bloc_test.dart`:
```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dartz/dartz.dart';

// Import bloc and dependencies
// import 'package:your_app/features/<feature>/presentation/bloc/<name>_bloc.dart';
// import 'package:your_app/features/<feature>/domain/usecases/<usecase>.dart';

// class Mock<UseCase> extends Mock implements <UseCase> {}

void main() {
  // late <Name>Bloc bloc;
  // late Mock<UseCase> mockUseCase;

  // setUp(() {
  //   mockUseCase = Mock<UseCase>();
  //   bloc = <Name>Bloc(useCase: mockUseCase);
  // });

  // tearDown(() {
  //   bloc.close();
  // });

  group('<Name>Bloc', () {
    test('initial state should be <Name>Initial', () {
      // expect(bloc.state, <Name>Initial());
    });

    // blocTest<<Name>Bloc, <Name>State>(
    //   'emits [<Name>Loading, <Name>Success] when Load<Name> is added',
    //   build: () {
    //     when(() => mockUseCase(any()))
    //         .thenAnswer((_) async => const Right('data'));
    //     return bloc;
    //   },
    //   act: (bloc) => bloc.add(Load<Name>()),
    //   expect: () => [
    //     <Name>Loading(),
    //     <Name>Success('data'),
    //   ],
    // );

    // blocTest<<Name>Bloc, <Name>State>(
    //   'emits [<Name>Loading, <Name>Error] when Load<Name> fails',
    //   build: () {
    //     when(() => mockUseCase(any()))
    //         .thenAnswer((_) async => Left(ServerFailure('error')));
    //     return bloc;
    //   },
    //   act: (bloc) => bloc.add(Load<Name>()),
    //   expect: () => [
    //     <Name>Loading(),
    //     <Name>Error('error'),
    //   ],
    // );
  });
}
```

7. **Output Summary**

```
BLoC '<name>' created successfully!

Files created:
- lib/features/<feature>/presentation/bloc/<name>_bloc.dart
- lib/features/<feature>/presentation/bloc/<name>_event.dart
- lib/features/<feature>/presentation/bloc/<name>_state.dart
- test/features/<feature>/presentation/bloc/<name>_bloc_test.dart

Next steps:
1. Add use case dependencies to the BLoC constructor
2. Implement event handlers with actual use case calls
3. Register BLoC in injection_container.dart:

   sl.registerFactory(
     () => <Name>Bloc(useCase: sl()),
   );

4. Provide BLoC in your widget tree:

   BlocProvider(
     create: (_) => sl<<Name>Bloc>()..add(Load<Name>()),
     child: const <Name>Page(),
   )
```

## Advanced Options

### With Specific Events

If user specifies events (e.g., `/generate-bloc auth --events login,logout,register`):

Generate corresponding events:
```dart
sealed class AuthEvent {}
class LoginRequested extends AuthEvent {
  final String email;
  final String password;
  LoginRequested({required this.email, required this.password});
}
class LogoutRequested extends AuthEvent {}
class RegisterRequested extends AuthEvent {
  final String email;
  final String password;
  final String name;
  RegisterRequested({required this.email, required this.password, required this.name});
}
```

### With Specific States

If user specifies custom states:
```dart
sealed class AuthState {}
class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthAuthenticated extends AuthState {
  final User user;
  AuthAuthenticated(this.user);
}
class AuthUnauthenticated extends AuthState {}
class AuthError extends AuthState {
  final String message;
  AuthError(this.message);
}
```

## Naming Convention

- Input: `login` or `Login` or `login_form`
- Bloc class: `LoginBloc`
- Event file: `login_event.dart`
- State file: `login_state.dart`
- Test file: `login_bloc_test.dart`
