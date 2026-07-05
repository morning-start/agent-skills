---
name: widget-testing
description: Widget tree testing with pump, find, and interaction simulation. Use when testing UI components, screens, user interactions, or widget behavior. Covers tester, finders, and matchers.
---

# Widget Testing

## Overview

Widget tests verify Flutter widgets render correctly and respond to user interactions. They run faster than integration tests while testing more than unit tests.

## Mandatory Workflow

### Step 1: Set Up Test File

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'package:your_app/features/auth/presentation/pages/login_page.dart';
import 'package:your_app/features/auth/presentation/bloc/auth_bloc.dart';

class MockAuthBloc extends MockBloc<AuthEvent, AuthState> implements AuthBloc {}

void main() {
  late MockAuthBloc mockAuthBloc;

  setUp(() {
    mockAuthBloc = MockAuthBloc();
  });
}
```

### Step 2: Create Widget Test Helper

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

### Step 3: Write Tests Using testWidgets

```dart
testWidgets('should display email and password fields', (tester) async {
  // Arrange
  when(() => mockAuthBloc.state).thenReturn(AuthInitial());

  // Act
  await tester.pumpWidget(createWidgetUnderTest());

  // Assert
  expect(find.byType(TextField), findsNWidgets(2));
  expect(find.text('Email'), findsOneWidget);
  expect(find.text('Password'), findsOneWidget);
});
```

## Widget Test Lifecycle

### pump vs pumpWidget vs pumpAndSettle

```dart
testWidgets('understanding pump methods', (tester) async {
  // pumpWidget: Builds widget tree for the first time
  await tester.pumpWidget(const MyApp());

  // pump: Triggers a frame, processes microtasks
  await tester.pump(); // Single frame
  await tester.pump(const Duration(milliseconds: 100)); // Wait then frame

  // pumpAndSettle: Pumps until no more frames scheduled
  // Good for animations, bad for infinite animations
  await tester.pumpAndSettle();

  // For infinite animations or streams, use pump with duration
  await tester.pump(const Duration(seconds: 1));
});
```

## Finder Patterns

### Finding by Type

```dart
find.byType(ElevatedButton);       // Find by widget type
find.byType(TextField);            // All TextFields
find.byType(Text);                 // All Text widgets
```

### Finding by Text

```dart
find.text('Login');                // Exact match
find.textContaining('Log');        // Contains substring
find.byTooltip('Submit');          // By tooltip
```

### Finding by Key

```dart
// In widget
ElevatedButton(
  key: const Key('login_button'),
  onPressed: () {},
  child: const Text('Login'),
)

// In test
find.byKey(const Key('login_button'));
```

### Finding by Widget

```dart
find.byWidget(mySpecificWidget);   // Exact widget instance
find.widgetWithText(ElevatedButton, 'Login'); // Button with text
find.widgetWithIcon(IconButton, Icons.close); // Icon button
```

### Finding by Semantics

```dart
find.bySemanticsLabel('Login button');
find.bySemanticsLabel(RegExp('Login.*'));
```

### Combining Finders

```dart
find.descendant(
  of: find.byType(Form),
  matching: find.byType(TextField),
);

find.ancestor(
  of: find.text('Submit'),
  matching: find.byType(ElevatedButton),
);
```

## Interaction Patterns

### Tapping

```dart
testWidgets('should call login when button tapped', (tester) async {
  when(() => mockAuthBloc.state).thenReturn(AuthInitial());

  await tester.pumpWidget(createWidgetUnderTest());

  // Tap the login button
  await tester.tap(find.byKey(const Key('login_button')));
  await tester.pump();

  // Verify bloc event was added
  verify(() => mockAuthBloc.add(any(that: isA<LoginRequested>()))).called(1);
});
```

### Text Input

```dart
testWidgets('should update email field', (tester) async {
  when(() => mockAuthBloc.state).thenReturn(AuthInitial());

  await tester.pumpWidget(createWidgetUnderTest());

  // Enter text
  await tester.enterText(
    find.byKey(const Key('email_field')),
    'test@example.com',
  );
  await tester.pump();

  // Verify text is displayed
  expect(find.text('test@example.com'), findsOneWidget);
});
```

### Scrolling

```dart
testWidgets('should scroll to item', (tester) async {
  await tester.pumpWidget(createWidgetUnderTest());

  // Scroll down
  await tester.drag(
    find.byType(ListView),
    const Offset(0, -300),
  );
  await tester.pump();

  // Or scroll until visible
  await tester.scrollUntilVisible(
    find.text('Item 50'),
    500.0,
    scrollable: find.byType(Scrollable),
  );
});
```

### Gestures

```dart
testWidgets('should handle long press', (tester) async {
  await tester.pumpWidget(createWidgetUnderTest());

  await tester.longPress(find.byKey(const Key('item')));
  await tester.pump();

  expect(find.byType(BottomSheet), findsOneWidget);
});

testWidgets('should handle swipe', (tester) async {
  await tester.pumpWidget(createWidgetUnderTest());

  // Swipe right to dismiss
  await tester.drag(
    find.byKey(const Key('dismissible_item')),
    const Offset(500, 0),
  );
  await tester.pumpAndSettle();
});
```

## Testing with BLoC

### Mocking BLoC States

```dart
testWidgets('should show loading indicator', (tester) async {
  // Arrange: Set loading state
  when(() => mockAuthBloc.state).thenReturn(AuthLoading());

  // Act
  await tester.pumpWidget(createWidgetUnderTest());

  // Assert
  expect(find.byType(CircularProgressIndicator), findsOneWidget);
});

testWidgets('should show error message', (tester) async {
  when(() => mockAuthBloc.state)
      .thenReturn(AuthFailure('Invalid credentials'));

  await tester.pumpWidget(createWidgetUnderTest());

  expect(find.text('Invalid credentials'), findsOneWidget);
});

testWidgets('should show user data on success', (tester) async {
  final user = User(id: '1', name: 'John', email: 'john@test.com');
  when(() => mockAuthBloc.state).thenReturn(AuthSuccess(user));

  await tester.pumpWidget(createWidgetUnderTest());

  expect(find.text('Welcome, John'), findsOneWidget);
});
```

### Testing State Changes

```dart
testWidgets('should react to state changes', (tester) async {
  final stateController = StreamController<AuthState>();
  when(() => mockAuthBloc.state).thenReturn(AuthInitial());
  when(() => mockAuthBloc.stream).thenAnswer((_) => stateController.stream);

  await tester.pumpWidget(createWidgetUnderTest());

  // Initial state
  expect(find.byType(CircularProgressIndicator), findsNothing);

  // Emit loading state
  stateController.add(AuthLoading());
  await tester.pump();

  expect(find.byType(CircularProgressIndicator), findsOneWidget);

  // Clean up
  await stateController.close();
});
```

## Testing Navigation

```dart
testWidgets('should navigate to home on success', (tester) async {
  when(() => mockAuthBloc.state).thenReturn(AuthSuccess(tUser));

  await tester.pumpWidget(
    MaterialApp(
      home: BlocProvider.value(
        value: mockAuthBloc,
        child: const LoginPage(),
      ),
      routes: {
        '/home': (_) => const HomePage(),
      },
    ),
  );

  await tester.pumpAndSettle();

  expect(find.byType(HomePage), findsOneWidget);
});
```

## Testing Forms

```dart
testWidgets('should show validation errors', (tester) async {
  when(() => mockAuthBloc.state).thenReturn(AuthInitial());

  await tester.pumpWidget(createWidgetUnderTest());

  // Submit empty form
  await tester.tap(find.byKey(const Key('submit_button')));
  await tester.pump();

  // Check validation messages
  expect(find.text('Email is required'), findsOneWidget);
  expect(find.text('Password is required'), findsOneWidget);
});

testWidgets('should enable button when form is valid', (tester) async {
  when(() => mockAuthBloc.state).thenReturn(AuthInitial());

  await tester.pumpWidget(createWidgetUnderTest());

  // Fill form
  await tester.enterText(
    find.byKey(const Key('email_field')),
    'test@example.com',
  );
  await tester.enterText(
    find.byKey(const Key('password_field')),
    'password123',
  );
  await tester.pump();

  // Verify button is enabled
  final button = tester.widget<ElevatedButton>(
    find.byKey(const Key('submit_button')),
  );
  expect(button.onPressed, isNotNull);
});
```

## Matcher Patterns

### Widget Matchers

```dart
expect(find.byType(Text), findsOneWidget);
expect(find.byType(Text), findsNWidgets(3));
expect(find.byType(Text), findsAtLeast(1));
expect(find.byType(Text), findsWidgets); // At least one
expect(find.byType(Missing), findsNothing);
```

### Custom Matchers

```dart
testWidgets('button should have correct color', (tester) async {
  await tester.pumpWidget(createWidgetUnderTest());

  final button = tester.widget<ElevatedButton>(
    find.byKey(const Key('primary_button')),
  );

  expect(
    button.style?.backgroundColor?.resolve({}),
    Colors.blue,
  );
});
```

## Anti-Patterns

### ❌ Using pumpAndSettle with Infinite Animations

```dart
// BAD: Will timeout if widget has infinite animation
await tester.pumpAndSettle();
```

### ✅ Use pump with Duration

```dart
// GOOD: Control timing explicitly
await tester.pump(const Duration(milliseconds: 500));
```

### ❌ Not Wrapping in MaterialApp

```dart
// BAD: Missing MaterialApp ancestor
await tester.pumpWidget(const MyWidget()); // May fail
```

### ✅ Always Wrap in MaterialApp

```dart
// GOOD: Proper widget tree
await tester.pumpWidget(
  const MaterialApp(
    home: MyWidget(),
  ),
);
```

### ❌ Finding by Text in Large Apps

```dart
// BAD: Fragile, may find unexpected widgets
find.text('Submit');
```

### ✅ Use Keys for Test Targets

```dart
// GOOD: Explicit test target
find.byKey(const Key('submit_button'));
```

## References

- See [references/patterns.md](references/patterns.md) for more patterns
- See `golden-testing` skill for visual regression
- See `integration-testing` skill for full app tests
