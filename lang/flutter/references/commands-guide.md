# Flutter 常用命令指南

## 目录
- [Flutter Lint](#flutter-lint)
- [Build Runner](#build-runner)
- [Flutter Test](#flutter-test)
- [其他常用命令](#其他常用命令)

## 概览
本指南提供 Flutter 开发中的常用命令，包括代码分析、代码生成、测试运行等操作。

## Flutter Lint

### 运行代码分析

```bash
# 基本分析
flutter analyze

# 自动修复问题
dart fix --apply

# 修复特定目录
dart fix --apply lib/features/

# 预览修复（不应用）
dart fix --dry-run
```

### 分析输出格式

#### 无问题
```
Analysis completed successfully!

No issues found.
```

#### 发现问题
```
Analysis completed with issues.

Errors (2):
1. lib/features/auth/data/models/user_model.dart:15:3
   error: The method 'fromJson' isn't defined
   Fix: Run build_runner to generate code

2. lib/features/auth/presentation/bloc/auth_bloc.dart:28:5
   error: The name 'AuthFailure' is defined in the libraries
   Fix: Remove duplicate import or use 'as' prefix

Warnings (3):
1. lib/core/utils/extensions.dart:10:1
   warning: Unused import: 'dart:async'
   Fix: Remove unused import

Summary:
- Errors: 2
- Warnings: 3
- Info: 5
```

### 常见问题处理

#### 缺少生成代码
```bash
dart run build_runner build --delete-conflicting-outputs
```

#### 导入冲突
```dart
// 使用前缀避免冲突
import 'package:app/core/error/failures.dart' as core;
import 'package:app/features/auth/domain/failures.dart' as auth;
```

#### 弃用 API
检查 Flutter 迁移指南，使用新的 API 替换。

### 严格模式配置

在 `analysis_options.yaml` 中配置严格分析：

```yaml
analyzer:
  errors:
    missing_return: error
    must_be_immutable: error
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true

linter:
  rules:
    - always_declare_return_types
    - avoid_dynamic_calls
    - avoid_print
    - prefer_const_constructors
    - prefer_final_fields
    - require_trailing_commas
    - unawaited_futures
```

## Build Runner

### 基本使用

```bash
# 默认构建
dart run build_runner build --delete-conflicting-outputs

# 监听模式（自动重新生成）
dart run build_runner watch --delete-conflicting-outputs

# 清理构建
dart run build_runner clean
```

### Freezed 模板

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

### Injectable 注册

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

### 故障排除

#### 过时的生成文件
```bash
find . -name "*.g.dart" -delete
find . -name "*.freezed.dart" -delete
find . -name "*.config.dart" -delete

dart run build_runner build --delete-conflicting-outputs
```

#### 冲突输出
```bash
flutter clean
flutter pub get
dart run build_runner build --delete-conflicting-outputs
```

#### 缺少 Part 指令
确保源文件包含：
```dart
part 'filename.g.dart';
part 'filename.freezed.dart';
```

### 性能优化

```bash
# 只构建特定文件
dart run build_runner build --build-filter="lib/features/auth/**"

# 详细输出用于调试
dart run build_runner build --verbose
```

## Flutter Test

### 运行测试

```bash
# 运行所有测试
flutter test

# 运行特定测试文件
flutter test test/features/auth/domain/usecases/login_user_test.dart

# 运行特定测试组
flutter test --name "should return User"

# 运行特定目录的测试
flutter test test/features/auth/
```

### 测试覆盖率

```bash
# 生成覆盖率报告
flutter test --coverage

# 生成 HTML 报告
genhtml coverage/lcov.info -o coverage/html

# 查看覆盖率
open coverage/html/index.html
```

### 并行测试

```bash
# 启用并行测试
flutter test --concurrency=4
```

### 测试报告

```bash
# 生成 JSON 报告
flutter test --reporter json > test_report.json

# 生成机器可读报告
flutter test --reporter compact
```

## 其他常用命令

### 项目清理

```bash
# 完整清理
flutter clean

# 重新获取依赖
flutter pub get

# 升级依赖
flutter pub upgrade
```

### 构建应用

```bash
# Debug 构建
flutter build apk --debug

# Release 构建
flutter build apk --release

# Web 构建
flutter build web

# iOS 构建
flutter build ios
```

### 格式化代码

```bash
# 格式化所有文件
dart format .

# 格式化特定目录
dart format lib/features/

# 检查格式（不修改）
dart format --output=none --set-exit-if-changed .
```

### 依赖管理

```bash
# 检查过时的依赖
flutter pub outdated

# 升级所有依赖
flutter pub upgrade

# 升级特定依赖
flutter pub upgrade package_name
```

### 调试和性能

```bash
# 运行应用
flutter run

# 运行并打开 DevTools
flutter run --devtools

# 性能分析
flutter run --profile

# 分析应用大小
flutter build apk --analyze-size
```

## CI/CD 集成

### GitHub Actions 示例

```yaml
name: Flutter CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'

      - name: Install dependencies
        run: flutter pub get

      - name: Generate code
        run: dart run build_runner build --delete-conflicting-outputs

      - name: Analyze
        run: flutter analyze --fatal-warnings

      - name: Test
        run: flutter test --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v2
        with:
          files: coverage/lcov.info
```

## 最佳实践

1. **定期运行分析**：在提交代码前运行 `flutter analyze`
2. **自动修复**：优先使用 `dart fix --apply` 自动修复问题
3. **测试覆盖率**：保持 70% 以上的测试覆盖率
4. **代码生成**：使用 `build_runner watch` 模式提高开发效率
5. **持续集成**：在 CI 流程中集成分析和测试
