---
description: Full clean and rebuild of the Flutter project
argument-hint: [--ios] [--android] [--all]
allowed-tools: Bash
---

# /clean-rebuild Command

Perform a full clean and rebuild of the Flutter project.

## Instructions

When the user runs `/clean-rebuild`:

1. **Standard Clean**

```bash
# Flutter clean
flutter clean

# Remove iOS pods (if on macOS)
cd ios && rm -rf Pods Podfile.lock && cd ..

# Remove Android build artifacts
cd android && ./gradlew clean && cd ..

# Get dependencies
flutter pub get

# iOS pod install (if on macOS)
cd ios && pod install && cd ..
```

2. **Regenerate Code**

```bash
# Run build_runner
dart run build_runner build --delete-conflicting-outputs
```

3. **Verify Build**

```bash
# Check for issues
flutter analyze

# Verify build compiles
flutter build apk --debug --target-platform=android-arm64
# Or for iOS
flutter build ios --debug --no-codesign
```

4. **Output Status**

```
Clean rebuild completed!

Steps performed:
✓ Flutter clean
✓ iOS Pods removed and reinstalled
✓ Android build cleaned
✓ Dependencies refreshed (pub get)
✓ Code generation complete (build_runner)
✓ Analysis passed
✓ Build verified

Project is ready for development.
```

## Flags

### --ios
Focus on iOS-specific cleaning:
```bash
cd ios
rm -rf Pods Podfile.lock .symlinks
rm -rf ~/Library/Developer/Xcode/DerivedData/*YourApp*
pod cache clean --all
pod install --repo-update
cd ..
```

### --android
Focus on Android-specific cleaning:
```bash
cd android
./gradlew clean
./gradlew --stop
rm -rf .gradle build app/build
cd ..
flutter pub get
```

### --all
Deep clean everything:
```bash
flutter clean
rm -rf .dart_tool
rm -rf .packages
rm -rf build
rm -rf ios/Pods ios/Podfile.lock ios/.symlinks
rm -rf android/.gradle android/build android/app/build
flutter pub get
cd ios && pod install && cd ..
dart run build_runner build --delete-conflicting-outputs
```

## Common Issues Resolved

### Gradle Issues
```
If Gradle fails:
./gradlew --stop
rm -rf ~/.gradle/caches
flutter clean && flutter pub get
```

### CocoaPods Issues
```
If pods fail:
pod cache clean --all
pod repo update
cd ios && pod install --repo-update
```

### Dart Tool Issues
```
If .dart_tool is corrupted:
rm -rf .dart_tool
flutter pub get
```

### Build Runner Issues
```
If generated files are stale:
find . -name "*.g.dart" -delete
find . -name "*.freezed.dart" -delete
dart run build_runner build --delete-conflicting-outputs
```
