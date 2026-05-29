---
description: Run Flutter analyzer and apply automatic fixes
argument-hint: [--fix] [path]
allowed-tools: Bash, Read
---

# /flutter-lint Command

Run Flutter static analysis and optionally apply fixes.

## Instructions

When the user runs `/flutter-lint`:

1. **Run Analysis**

```bash
flutter analyze
```

2. **Parse Results**

Categorize issues by severity:
- **Errors**: Must be fixed, will break compilation
- **Warnings**: Should be fixed, potential bugs
- **Info**: Style suggestions, can be deferred

3. **Output Format**

### Clean Output:
```
Analysis completed successfully!

No issues found.
```

### Issues Found:
```
Analysis completed with issues.

Errors (2):
1. lib/features/auth/data/models/user_model.dart:15:3
   error: The method 'fromJson' isn't defined for the type 'UserModel'
   Fix: Run build_runner to generate code

2. lib/features/auth/presentation/bloc/auth_bloc.dart:28:5
   error: The name 'AuthFailure' is defined in the libraries
   Fix: Remove duplicate import or use 'as' prefix

Warnings (3):
1. lib/core/utils/extensions.dart:10:1
   warning: Unused import: 'dart:async'
   Fix: Remove unused import

2. lib/features/auth/presentation/pages/login_page.dart:45:7
   warning: The value of the local variable 'result' isn't used
   Fix: Use the variable or remove it

3. lib/features/auth/domain/usecases/login_user.dart:22:3
   warning: Missing return type on function
   Fix: Add return type annotation

Info (5):
1. lib/main.dart:8:1
   info: Prefer const constructors
   ...

Summary:
- Errors: 2
- Warnings: 3
- Info: 5

Run '/flutter-lint --fix' to apply automatic fixes.
```

4. **Apply Fixes (if --fix flag)**

```bash
dart fix --apply
```

Then re-run analysis to verify:
```bash
flutter analyze
```

5. **Handle Common Issues**

### Missing Generated Code:
```
If errors mention missing .g.dart or .freezed.dart files:

Run: dart run build_runner build --delete-conflicting-outputs
```

### Import Conflicts:
```
If errors mention duplicate definitions:

Use import prefixes:
import 'package:app/core/error/failures.dart' as core;
import 'package:app/features/auth/domain/failures.dart' as auth;
```

### Deprecated APIs:
```
If warnings mention deprecated:

Check Flutter migration guides for replacement APIs.
```

6. **Strict Mode Check**

For stricter analysis, check analysis_options.yaml:

```yaml
# Recommended strict settings
analyzer:
  errors:
    missing_return: error
    must_be_immutable: error
    sort_unnamed_constructors_first: ignore
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true

linter:
  rules:
    - always_declare_return_types
    - avoid_dynamic_calls
    - avoid_print
    - avoid_type_to_string
    - cancel_subscriptions
    - close_sinks
    - prefer_const_constructors
    - prefer_final_fields
    - prefer_final_locals
    - require_trailing_commas
    - unawaited_futures
```

## Quick Fix Commands

```bash
# Apply all safe fixes
dart fix --apply

# Preview fixes without applying
dart fix --dry-run

# Fix specific directory
dart fix --apply lib/features/auth/

# Format code after fixing
dart format .
```

## Integration with CI

Suggest adding to CI pipeline:
```yaml
# .github/workflows/analyze.yml
- name: Analyze
  run: |
    flutter analyze --fatal-warnings --fatal-infos
```
