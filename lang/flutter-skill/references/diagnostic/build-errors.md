# Flutter Build Errors 诊断指南

## 目录
- [常见构建错误](#常见构建错误)
- [Gradle 错误](#gradle-错误)
- [iOS 构建错误](#ios-构建错误)
- [依赖冲突](#依赖冲突)
- [代码生成错误](#代码生成错误)

## 概览
本指南提供 Flutter 构建过程中常见错误的系统性诊断和解决方案。

## 常见构建错误

### 1. 缺少生成代码

**错误信息**：
```
The method 'fromJson' isn't defined for the type 'UserModel'
```

**诊断步骤**：
1. 检查是否运行了 build_runner
2. 检查 part 指令是否正确
3. 检查 Freezed 注解是否正确

**解决方案**：
```bash
# 清理并重新生成
dart run build_runner clean
dart run build_runner build --delete-conflicting-outputs
```

**验证**：
```bash
# 检查生成文件是否存在
ls -la lib/features/auth/data/models/user_model.g.dart
ls -la lib/features/auth/data/models/user_model.freezed.dart
```

### 2. 类型不匹配

**错误信息**：
```
A value of type 'UserModel' can't be assigned to a variable of type 'User'
```

**诊断步骤**：
1. 检查是否调用了 toEntity() 方法
2. 检查 Entity 和 Model 的字段是否匹配

**解决方案**：
```dart
// ❌ 错误
final user = userRepository.getUser(userModel);

// ✅ 正确
final user = userRepository.getUser(userModel.toEntity());
```

### 3. 缺少依赖

**错误信息**：
```
Error: Could not resolve the package 'http' in 'package:your_app/...'
```

**诊断步骤**：
1. 检查 pubspec.yaml 中的依赖声明
2. 运行 flutter pub get

**解决方案**：
```bash
flutter pub get
```

### 4. 版本冲突

**错误信息**：
```
Because every version of flutter_test from sdk depends on ...
version solving failed.
```

**诊断步骤**：
```bash
flutter pub deps
```

**解决方案**：
```bash
# 查看过时的依赖
flutter pub outdated

# 升级依赖
flutter pub upgrade
```

## Gradle 错误

### 1. Gradle 版本不兼容

**错误信息**：
```
Could not resolve com.android.tools.build:gradle:x.x.x
```

**诊断步骤**：
```bash
cd android
./gradlew --version
```

**解决方案**：
编辑 `android/build.gradle`：
```gradle
buildscript {
    ext.kotlin_version = '1.9.0'
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.1.0'
    }
}
```

### 2. SDK 版本不匹配

**错误信息**：
```
Failed to find target with hash string 'android-33'
```

**诊断步骤**：
```bash
flutter doctor
flutter doctor --android-licenses
```

**解决方案**：
1. 打开 Android Studio
2. SDK Manager → 安装缺失的 SDK 版本
3. 更新 `android/app/build.gradle` 中的 compileSdkVersion

### 3. OutOfMemory 错误

**错误信息**：
```
java.lang.OutOfMemoryError: Java heap space
```

**解决方案**：
编辑 `android/gradle.properties`：
```properties
org.gradle.jvmargs=-Xmx4G -XX:MaxMetaspaceSize=512m
```

## iOS 构建错误

### 1. Pod 安装失败

**错误信息**：
```
Error running pod install
```

**诊断步骤**：
```bash
cd ios
pod install --verbose
```

**解决方案**：
```bash
# 清理 pods
cd ios
rm -rf Pods Podfile.lock
pod install

# 如果仍有问题，更新 CocoaPods
sudo gem install cocoapods
```

### 2. 证书问题

**错误信息**：
```
Code signing is required for product type 'Application' in SDK 'iOS'
```

**诊断步骤**：
1. 打开 Xcode
2. Project Settings → Signing & Capabilities

**解决方案**：
1. 配置正确的开发团队
2. 确保 Bundle Identifier 唯一

### 3. 架构问题

**错误信息**：
```
Building for iOS Simulator, but the linked and embedded framework 'xxx.framework' was built for iOS + iOS Simulator
```

**解决方案**：
```bash
cd ios
pod install
```

编辑 `ios/Podfile`：
```ruby
post_install do |installer|
  installer.pods_project.targets.each do |target|
    target.build_configurations.each do |config|
      config.build_settings['ONLY_ACTIVE_ARCH'] = 'NO'
    end
  end
end
```

## 依赖冲突

### 1. 传递依赖冲突

**诊断步骤**：
```bash
flutter pub deps
```

**解决方案**：
使用 dependency_overrides：
```yaml
dependency_overrides:
  http: ^1.2.0
  analyzer: ^6.0.0
```

### 2. 插件版本不兼容

**错误信息**：
```
Plugin project :path not found. Please update settings.gradle
```

**解决方案**：
```bash
flutter clean
flutter pub get
cd android
./gradlew clean
```

## 代码生成错误

### 1. Part 指令错误

**错误信息**：
```
Could not find file 'xxx.g.dart'
```

**诊断步骤**：
检查源文件是否包含正确的 part 指令。

**解决方案**：
```dart
// 确保文件顶部有
part 'user_model.g.dart';
part 'user_model.freezed.dart';
```

### 2. Freezed 配置错误

**错误信息**：
```
Could not find constructor or factory for 'UserModel'
```

**解决方案**：
```dart
@freezed
class UserModel with _$UserModel {
  const UserModel._();

  const factory UserModel({
    required String id,
  }) = _UserModel;
}
```

### 3. Injectable 错误

**错误信息**：
```
Could not resolve 'Injectable' annotation
```

**解决方案**：
```dart
import 'package:injectable/injectable.dart';

@lazySingleton
class MyService {
  // ...
}
```

## 诊断流程

### 系统性诊断步骤

1. **环境检查**
   ```bash
   flutter doctor -v
   ```

2. **依赖检查**
   ```bash
   flutter pub deps
   ```

3. **清理构建**
   ```bash
   flutter clean
   cd android
   ./gradlew clean
   cd ../ios
   rm -rf Pods Podfile.lock
   cd ..
   flutter pub get
   ```

4. **代码生成**
   ```bash
   dart run build_runner build --delete-conflicting-outputs
   ```

5. **重新构建**
   ```bash
   flutter build apk --debug
   ```

## 预防措施

1. **定期更新依赖**
   ```bash
   flutter pub outdated
   flutter pub upgrade
   ```

2. **使用固定版本**
   ```yaml
   dependencies:
     dio: ^5.3.0  # 使用 caret 版本
     # 或
     dio: 5.3.0   # 使用精确版本
   ```

3. **CI/CD 集成**
   - 在 CI 中运行完整构建流程
   - 及时发现构建错误

4. **文档化依赖**
   - 记录关键依赖的版本要求
   - 维护 CHANGELOG

## 快速参考

```bash
# 完整清理和重建流程
flutter clean
flutter pub get
dart run build_runner clean
dart run build_runner build --delete-conflicting-outputs
flutter build apk --debug

# Android 清理
cd android
./gradlew clean
cd ..

# iOS 清理
cd ios
rm -rf Pods Podfile.lock
pod install
cd ..
```
