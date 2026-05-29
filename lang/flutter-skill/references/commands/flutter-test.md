---
description: Run Flutter tests with coverage and optional filters
argument-hint: [test-path] [--coverage] [--name pattern]
allowed-tools: Bash, Read
---

# /flutter-test Command

Run Flutter tests with coverage reporting and filtering options.

## Instructions

When the user runs `/flutter-test`:

1. **Parse Arguments**
   - `[test-path]` - Optional path to specific test file or directory
   - `--coverage` or `-c` - Generate coverage report (default: true)
   - `--name <pattern>` or `-n <pattern>` - Run only tests matching pattern
   - `--update-goldens` - Update golden files
   - `--no-coverage` - Skip coverage generation

2. **Run Tests**

### Default (all tests with coverage):
```bash
flutter test --coverage
```

### Specific test file:
```bash
flutter test test/features/auth/domain/usecases/login_user_test.dart --coverage
```

### Specific directory:
```bash
flutter test test/features/auth/ --coverage
```

### With name filter:
```bash
flutter test --name "should return user" --coverage
```

### Update golden files:
```bash
flutter test --update-goldens
```

3. **Analyze Results**

After tests complete, analyze the output:

- **All tests passed**: Report success with count
- **Some tests failed**: List failed tests with file:line references
- **Coverage generated**: Show coverage summary

4. **Coverage Report**

If coverage was generated:

```bash
# Check if lcov is available
which lcov

# Generate HTML report if lcov is available
genhtml coverage/lcov.info -o coverage/html

# Or show summary
lcov --summary coverage/lcov.info
```

If lcov is not available, read and summarize the lcov.info file:
```bash
# Count covered/total lines
grep -c "DA:" coverage/lcov.info
```

5. **Output Format**

### Success Output:
```
Tests completed successfully!

Summary:
- Total tests: 42
- Passed: 42
- Failed: 0
- Skipped: 0

Coverage:
- Lines: 85.3% (1024/1200)
- Files: 45

Coverage report generated at: coverage/lcov.info
To view HTML report: open coverage/html/index.html
```

### Failure Output:
```
Tests failed!

Failed tests:
1. test/features/auth/domain/usecases/login_user_test.dart:25
   "should return user when login succeeds"
   Expected: Right(User(...))
   Actual: Left(ServerFailure(...))

2. test/features/auth/presentation/bloc/auth_bloc_test.dart:48
   "should emit [Loading, Error] when login fails"
   Expected: [AuthLoading(), AuthError(...)]
   Actual: [AuthLoading()]

Summary:
- Total tests: 42
- Passed: 40
- Failed: 2
- Skipped: 0

Fix the failing tests and run again.
```

6. **Common Issues**

### Missing dependencies:
```
If tests fail due to missing mocks, suggest:
- Add missing mock classes
- Register fallback values for mocktail
- Check import paths
```

### Timeout issues:
```bash
# Run with increased timeout
flutter test --timeout 60s
```

### Integration tests:
```bash
# For integration tests, use flutter drive or integration_test
flutter test integration_test/
```

## Test Filtering Examples

```bash
# Run only unit tests
flutter test test/features/*/domain/

# Run only widget tests
flutter test test/features/*/presentation/

# Run only bloc tests
flutter test --name "Bloc"

# Run tests for specific feature
flutter test test/features/auth/

# Skip slow tests
flutter test --exclude-tags slow
```

## Coverage Thresholds

After running, check if coverage meets thresholds:

```dart
Recommended minimums:
- Domain layer (usecases): 90%
- Data layer (repositories): 80%
- Presentation layer (bloc): 85%
- Widgets: 70%
- Overall: 80%
```

If coverage is below threshold, identify uncovered files:
```bash
# List files with low coverage
grep -B1 "LF:" coverage/lcov.info | grep "SF:" | head -20
```
