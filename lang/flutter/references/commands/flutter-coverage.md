---
description: Generate and analyze test coverage report
argument-hint: [--threshold 80] [--html]
allowed-tools: Bash, Read
---

# /flutter-coverage Command

Generate test coverage report and analyze results.

## Instructions

When the user runs `/flutter-coverage`:

1. **Run Tests with Coverage**

```bash
flutter test --coverage
```

2. **Analyze Coverage**

```bash
# Check if lcov is available
which lcov

# If available, generate summary
lcov --summary coverage/lcov.info

# Generate HTML report
genhtml coverage/lcov.info -o coverage/html --no-function-coverage
```

3. **Parse Results**

Read coverage/lcov.info and calculate:
- Total lines
- Covered lines
- Coverage percentage
- Files with low coverage

4. **Output Format**

### Summary Output:
```
Test Coverage Report
====================

Overall Coverage: 82.5%

By Layer:
- Domain (usecases):     95.2% ✓
- Domain (entities):     100.0% ✓
- Data (repositories):   78.4% ⚠
- Data (models):         100.0% ✓
- Data (datasources):    72.1% ⚠
- Presentation (bloc):   88.9% ✓
- Presentation (pages):  65.3% ⚠

Low Coverage Files (< 70%):
1. lib/features/auth/data/datasources/auth_remote_datasource.dart - 62.5%
2. lib/features/orders/presentation/pages/order_details_page.dart - 58.3%
3. lib/core/network/api_client.dart - 45.0%

Recommendations:
- Add tests for auth_remote_datasource.dart (missing error handling tests)
- Add widget tests for order_details_page.dart
- Mock network layer for api_client tests

Coverage report: coverage/html/index.html
```

5. **Threshold Check**

If `--threshold` is specified:
```
Coverage Check
==============
Threshold: 80%
Actual:    82.5%
Status:    PASSED ✓
```

Or if failing:
```
Coverage Check
==============
Threshold: 80%
Actual:    72.3%
Status:    FAILED ✗

Action Required:
- Increase coverage by 7.7% to meet threshold
- Focus on files with < 50% coverage first
```

## Flags

### --threshold <percentage>
Check if coverage meets minimum threshold:
```bash
/flutter-coverage --threshold 80
```

### --html
Generate and open HTML report:
```bash
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html  # macOS
# or
xdg-open coverage/html/index.html  # Linux
```

### --by-feature
Show coverage by feature module:
```
Feature Coverage:
- auth:     85.2%
- orders:   72.4%
- profile:  91.0%
- settings: 68.5%
```

## Coverage Best Practices

### Recommended Thresholds
```
Domain Layer:      90%
Data Layer:        80%
Presentation Layer: 75%
Overall:           80%
```

### Files to Exclude
Add to coverage ignore in pubspec.yaml or test configuration:
```yaml
# Files to exclude from coverage
# - Generated files (*.g.dart, *.freezed.dart)
# - Main entry points
# - Configuration files
```

### Improving Coverage

1. **Identify Untested Code**
   ```bash
   lcov --list coverage/lcov.info | grep -E "^[^ ].*\s+0\.0%"
   ```

2. **Add Missing Tests**
   - Focus on business logic first (domain layer)
   - Then data layer (repositories, data sources)
   - Finally presentation (BLoC, widgets)

3. **Test Edge Cases**
   - Error handling paths
   - Empty/null inputs
   - Boundary conditions
