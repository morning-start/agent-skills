# Flutter State Debugging 指南

## 目录
- [BLoC 状态调试](#bloc-状态调试)
- [Riverpod 状态调试](#riverpod-状态调试)
- [状态观察技巧](#状态观察技巧)
- [常见状态问题](#常见状态问题)

## 概览
本指南提供 Flutter 应用中状态管理的系统性调试方法和工具。

## BLoC 状态调试

### 1. 使用 BlocObserver

创建自定义 BlocObserver 来监控所有 BLoC 的状态变化：

```dart
class AppBlocObserver extends BlocObserver {
  @override
  void onCreate(BlocBase bloc) {
    super.onCreate(bloc);
    debugPrint('onCreate -- ${bloc.runtimeType}');
  }

  @override
  void onEvent(Bloc bloc, Object? event) {
    super.onEvent(bloc, event);
    debugPrint('onEvent -- ${bloc.runtimeType} $event');
  }

  @override
  void onChange(BlocBase bloc, Change change) {
    super.onChange(bloc, change);
    debugPrint('onChange -- ${bloc.runtimeType} $change');
  }

  @override
  void onError(BlocBase bloc, Object error, StackTrace stackTrace) {
    super.onError(bloc, error, stackTrace);
    debugPrint('onError -- ${bloc.runtimeType} $error');
  }

  @override
  void onClose(BlocBase bloc) {
    super.onClose(bloc);
    debugPrint('onClose -- ${bloc.runtimeType}');
  }
}

// 在 main.dart 中
void main() {
  Bloc.observer = AppBlocObserver();
  runApp(MyApp());
}
```

### 2. 使用 Flutter DevTools 观察 BLoC

1. 启动 DevTools：
```bash
flutter pub global run devtools
```

2. 在应用运行时，打开 DevTools 的 BLoC 面板

3. 查看实时状态变化、事件流和转换

### 3. 手动日志记录

在关键位置添加日志：

```dart
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  AuthBloc(this.loginUser) : super(AuthInitial()) {
    on<LoginRequested>(_onLoginRequested);
  }

  Future<void> _onLoginRequested(
    LoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    debugPrint('AuthBloc: LoginRequested received');
    emit(AuthLoading());
    debugPrint('AuthBloc: Emitting AuthLoading');

    final result = await loginUser(event.email, event.password);
    debugPrint('AuthBloc: Login result: $result');

    result.fold(
      (failure) {
        debugPrint('AuthBloc: Emitting AuthError - ${failure.message}');
        emit(AuthError(failure.message));
      },
      (user) {
        debugPrint('AuthBloc: Emitting AuthSuccess - ${user.name}');
        emit(AuthSuccess(user));
      },
    );
  }
}
```

### 4. 测试 BLoC 行为

使用 blocTest 验证状态转换：

```dart
blocTest<AuthBloc, AuthState>(
  'emits [AuthLoading, AuthSuccess] when login succeeds',
  build: () {
    when(() => mockLoginUser(any()))
        .thenAnswer((_) async => Right(tUser));
    return AuthBloc(mockLoginUser);
  },
  act: (bloc) => bloc.add(LoginRequested(
    email: 'test@test.com',
    password: 'password',
  )),
  expect: () => [
    AuthLoading(),
    AuthSuccess(tUser),
  ],
  verify: (_) {
    verify(() => mockLoginUser(any())).called(1);
  },
);
```

## Riverpod 状态调试

### 1. 使用 ProviderObserver

创建自定义 ProviderObserver：

```dart
class AppProviderObserver extends ProviderObserver {
  @override
  void didAddProvider(
    ProviderBase<Object?> provider,
    Object? value,
    ProviderContainer container,
  ) {
    debugPrint('Provider added: ${provider.name ?? provider.runtimeType}');
  }

  @override
  void didDisposeProvider(
    ProviderBase<Object?> provider,
    ProviderContainer container,
  ) {
    debugPrint('Provider disposed: ${provider.name ?? provider.runtimeType}');
  }

  @override
  void providerDidFail(
    ProviderBase<Object?> provider,
    Object error,
    StackTrace stackTrace,
    ProviderContainer container,
  ) {
    debugPrint('Provider failed: ${provider.name ?? provider.runtimeType}');
    debugPrint('Error: $error');
  }

  @override
  void didUpdateProvider(
    ProviderBase<Object?> provider,
    Object? previousValue,
    Object? newValue,
    ProviderContainer container,
  ) {
    debugPrint('Provider updated: ${provider.name ?? provider.runtimeType}');
    debugPrint('Previous: $previousValue');
    debugPrint('New: $newValue');
  }
}

// 在 main.dart 中
void main() {
  runApp(
    ProviderScope(
      observers: [AppProviderObserver()],
      child: MyApp(),
    ),
  );
}
```

### 2. 使用 ref.listen 调试

在 Widget 中监听 provider 变化：

```dart
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final counter = ref.watch(counterProvider);

    useEffect(() {
      final listener = ref.listen<int>(counterProvider, (previous, next) {
        debugPrint('Counter changed from $previous to $next');
      });

      return listener.close;
    }, []);

    return Text('$counter');
  }
}
```

### 3. 使用 ref.read 调试

在事件处理中读取当前状态：

```dart
ElevatedButton(
  onPressed: () {
    final currentValue = ref.read(counterProvider);
    debugPrint('Current counter value: $currentValue');
    ref.read(counterProvider.notifier).state++;
  },
  child: Text('Increment'),
)
```

### 4. 使用 ref.invalidate 调试

强制刷新 provider：

```dart
ref.invalidate(userProvider);
```

## 状态观察技巧

### 1. 使用 BlocBuilder 显示状态

```dart
BlocBuilder<AuthBloc, AuthState>(
  builder: (context, state) {
    debugPrint('Building widget with state: $state');
    return switch (state) {
      AuthInitial() => const Text('Initial'),
      AuthLoading() => const CircularProgressIndicator(),
      AuthSuccess(:final user) => Text('Welcome, ${user.name}'),
      AuthError(:final message) => Text('Error: $message'),
    };
  },
)
```

### 2. 使用 BlocListener 监听状态

```dart
BlocListener<AuthBloc, AuthState>(
  listener: (context, state) {
    debugPrint('State changed to: $state');
    if (state is AuthSuccess) {
      Navigator.of(context).pushReplacementNamed('/home');
    } else if (state is AuthError) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.message)),
      );
    }
  },
  child: Container(),
)
```

### 3. 使用 BlocConsumer 组合

```dart
BlocConsumer<AuthBloc, AuthState>(
  listener: (context, state) {
    // 监听状态变化
    debugPrint('Listener: State changed to $state');
  },
  builder: (context, state) {
    // 构建 UI
    debugPrint('Builder: Building with $state');
    return Container();
  },
)
```

## 常见状态问题

### 1. 状态未更新

**症状**：调用事件后，UI 没有变化

**诊断步骤**：
1. 检查事件是否正确添加
2. 检查 BLoC 是否正确提供
3. 检查是否使用了正确的 context

**解决方案**：
```dart
// ❌ 错误 - 在错误的 context 中
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: () {
        // context 没有 BLoC
        context.read<AuthBloc>().add(LoginRequested());
      },
      child: Text('Login'),
    );
  }
}

// ✅ 正确
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => AuthBloc(),
      child: Builder(
        builder: (context) {
          return ElevatedButton(
            onPressed: () {
              context.read<AuthBloc>().add(LoginRequested());
            },
            child: Text('Login'),
          );
        },
      ),
    );
  }
}
```

### 2. 状态更新但 UI 不刷新

**症状**：状态已改变，但 Widget 没有重建

**诊断步骤**：
1. 检查是否使用了 BlocBuilder
2. 检查状态是否实现了 ==
3. 检查是否使用了 const 构造函数

**解决方案**：
```dart
// 确保状态使用 Equatable
class AuthState extends Equatable {
  @override
  List<Object?> get props => [];
}

// 或使用 sealed class（Dart 3+）
sealed class AuthState {}
class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthSuccess extends AuthState {
  final User user;
  AuthSuccess(this.user);
}
```

### 3. 状态循环

**症状**：状态不断变化，导致无限循环

**诊断步骤**：
1. 检查 BlocObserver 日志
2. 检查事件处理逻辑
3. 检查是否在 build 方法中触发事件

**解决方案**：
```dart
// ❌ 错误 - 在 build 中触发事件
@override
Widget build(BuildContext context) {
  context.read<CounterBloc>().add(Increment());
  return Text('Count');
}

// ✅ 正确 - 使用 useCallback 或 initState
@override
void initState() {
  super.initState();
  WidgetsBinding.instance.addPostFrameCallback((_) {
    context.read<CounterBloc>().add(Increment());
  });
}
```

## 调试工具

### 1. Flutter DevTools

```bash
# 安装 DevTools
flutter pub global activate devtools

# 启动 DevTools
flutter pub global run devtools
```

DevTools 提供的功能：
- 实时查看 BLoC/Riverpod 状态
- 时间轴视图
- 性能分析
- 网络请求跟踪

### 2. 日志插件

使用 `logger` 包美化日志：

```yaml
dependencies:
  logger: ^2.0.0
```

```dart
import 'package:logger/logger.dart';

final logger = Logger();

logger.i('Info message');
logger.w('Warning message');
logger.e('Error message');
logger.d('Debug message');
```

### 3. 状态快照

保存和恢复状态用于调试：

```dart
class DebugBlocObserver extends BlocObserver {
  final Map<Type, dynamic> _snapshots = {};

  @override
  void onChange(BlocBase bloc, Change change) {
    super.onChange(bloc, change);
    _snapshots[bloc.runtimeType] = change.nextState;
  }

  dynamic getSnapshot(Type blocType) => _snapshots[blocType];
}
```

## 最佳实践

1. **使用 BlocObserver**：全局监控所有 BLoC
2. **添加日志**：在关键位置添加调试日志
3. **编写测试**：验证状态转换逻辑
4. **使用 DevTools**：实时查看状态变化
5. **保持状态简单**：避免过度复杂的状态结构

## 快速参考

```dart
// 快速调试代码片段

// 1. 打印所有状态变化
Bloc.observer = SimpleBlocObserver(
  onChange: (bloc, change) => print('$bloc: $change'),
);

// 2. 监听特定 provider
ref.listen(provider, (previous, next) {
  print('Changed from $previous to $next');
});

// 3. 手动触发事件并查看结果
final bloc = context.read<AuthBloc>();
bloc.add(LoginRequested());
print('State: ${bloc.state}');
```
