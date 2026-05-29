---
description: Run build_runner for code generation (Freezed, JSON, Injectable)
argument-hint: [--watch] [--delete]
allowed-tools: Bash
---

# /build-runner Command

Run Dart build_runner for code generation.

## Instructions

When the user runs `/build-runner`:

1. **Default Build**

```bash
dart run build_runner build --delete-conflicting-outputs
```

2. **Watch Mode (if --watch)**

```bash
dart run build_runner watch --delete-conflicting-outputs
```

3. **Clean Build (if issues)**

```bash
# Clean generated files first
dart run build_runner clean

# Then rebuild
dart run build_runner build --delete-conflicting-outputs
```

4. **Output Format**

### Success:
```
Code generation completed successfully!

Generated files:
- lib/features/auth/data/models/user_model.freezed.dart
- lib/features/auth/data/models/user_model.g.dart
- lib/injection_container.config.dart
- [... more files]

Total: 15 files generated
```

### Errors:
```
Code generation failed!

Errors:
1. lib/features/auth/data/models/user_model.dart:12:3
   Error: The class 'UserModel' doesn't have a unnamed constructor.
   Fix: Add factory constructor for Freezed

2. lib/features/orders/data/models/order_model.dart:8:1
   Error: Couldn't find constructor or factory for 'OrderModel'.
   Fix: Ensure @freezed annotation is present

Suggestions:
- Check that all Freezed classes have proper annotations
- Ensure part directives are correct
- Verify package imports
```

5. **Common Patterns**

### Freezed Model Template:
```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_model.freezed.dart';
part 'user_model.g.dart';

@freezed
class UserModel with _$UserModel {
  const factory UserModel({
    required String id,
    required String name,
    String? email,
    @Default(false) bool isActive,
  }) = _UserModel;

  factory UserModel.fromJson(Map<String, dynamic> json) =>
      _$UserModelFromJson(json);
}
```

### Injectable Registration:
```dart
import 'package:injectable/injectable.dart';

@lazySingleton
class AuthRepository {
  // ...
}

@injectable
class LoginUseCase {
  final AuthRepository _repository;

  LoginUseCase(this._repository);
}
```

6. **Troubleshooting**

### Stale Generated Files:
```bash
# Remove all generated files
find . -name "*.g.dart" -delete
find . -name "*.freezed.dart" -delete
find . -name "*.config.dart" -delete

# Regenerate
dart run build_runner build --delete-conflicting-outputs
```

### Conflicting Outputs:
```bash
# The --delete-conflicting-outputs flag handles this
# If still having issues:
flutter clean
flutter pub get
dart run build_runner build --delete-conflicting-outputs
```

### Missing Part Directive:
```
If error says "Could not find file '*.g.dart'":

Ensure the source file has:
part 'filename.g.dart';
part 'filename.freezed.dart';
```

## Performance Tips

```bash
# Build specific files only (faster)
dart run build_runner build --build-filter="lib/features/auth/**"

# Verbose output for debugging
dart run build_runner build --verbose
```
