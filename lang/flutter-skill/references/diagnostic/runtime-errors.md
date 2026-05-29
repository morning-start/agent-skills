# Flutter Runtime Errors 诊断指南

## 目录
- [常见运行时错误](#常见运行时错误)
- [空指针异常](#空指针异常)
- [状态管理错误](#状态管理错误)
- [网络错误](#网络错误)
- [布局错误](#布局错误)

## 概览
本指南提供 Flutter 应用运行时错误的系统性诊断和解决方案。

## 常见运行时错误

### 1. setState called after dispose

**错误信息**：
```
setState() called after dispose(): ...
```

**诊断步骤**：
1. 检查是否在 dispose 后调用 setState
2. 检查异步操作是否在 dispose 后完成

**解决方案**：
```dart
class MyWidget extends StatefulWidget {
  @override
  _MyWidgetState createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  bool _disposed = false;

  @override
  void dispose() {
    _disposed = true;
    super.dispose();
  }

  Future<void> _loadData() async {
    final data = await fetchSomeData();

    if (!_disposed) {
      setState(() {
        // 更新状态
      });
    }
  }
}
```

**最佳实践**：
```dart
// 使用 mounted 属性
if (mounted) {
  setState(() {
    // 更新状态
  });
}
```

### 2. Null check operator used on a null value

**错误信息**：
```
Null check operator used on a null value
```

**诊断步骤**：
1. 定位错误代码位置
2. 检查可能为 null 的变量
3. 使用调试器查看变量值

**解决方案**：
```dart
// ❌ 错误
final user = userProvider.user!;
print(user.name);

// ✅ 正确
final user = userProvider.user;
if (user != null) {
  print(user.name);
}

// 或使用 ?.
print(userProvider.user?.name);

// 或使用 ??
print(userProvider.user?.name ?? 'Unknown');
```

### 3. RangeError (index)

**错误信息**：
```
RangeError (index): Invalid value: Valid value range is empty: 0
```

**诊断步骤**：
1. 检查列表是否为空
2. 检查索引是否超出范围

**解决方案**：
```dart
// ❌ 错误
final item = list[0];

// ✅ 正确
if (list.isNotEmpty) {
  final item = list[0];
}

// 或使用 elementAt
final item = list.elementAtOrNull(0);
```

### 4. Failed assertion

**错误信息**：
```
'package:flutter/src/widgets/framework.dart': Failed assertion: line xxxx pos xx: 'mounted must not be null'
```

**诊断步骤**：
1. 找到断言失败的代码
2. 检查前置条件是否满足

**解决方案**：
```dart
// 添加防御性检查
if (context.mounted) {
  Navigator.of(context).push(...);
}

// 或使用 try-catch
try {
  Navigator.of(context).push(...);
} catch (e) {
  debugPrint('Navigation error: $e');
}
```

## 空指针异常

### 1. Future 返回 null

**错误信息**：
```
NoSuchMethodError: The getter 'name' was called on null.
```

**诊断步骤**：
1. 检查 Future 是否可能返回 null
2. 使用正确的 null 处理方式

**解决方案**：
```dart
// ❌ 错误
Future<User> getUser() async {
  final data = await fetchUser();
  return data; // 可能返回 null
}

// ✅ 正确
Future<User?> getUser() async {
  final data = await fetchUser();
  return data;
}

// 使用时
final user = await getUser();
if (user != null) {
  print(user.name);
}
```

### 2. 可选参数未提供

**错误信息**：
```
NoSuchMethodError: The method 'call' was called on null.
```

**解决方案**：
```dart
// ❌ 错误
class MyWidget extends StatelessWidget {
  final Future<User?> Function()? fetchUser;

  const MyWidget({this.fetchUser});

  @override
  Widget build(BuildContext context) {
    // fetchUser 可能为 null
    return FutureBuilder(
      future: fetchUser!(), // 可能抛出异常
      builder: (context, snapshot) => Container(),
    );
  }
}

// ✅ 正确
@override
Widget build(BuildContext context) {
  if (fetchUser == null) {
    return Text('fetchUser not provided');
  }

  return FutureBuilder(
    future: fetchUser!(),
    builder: (context, snapshot) => Container(),
  );
}
```

## 状态管理错误

### 1. BLoC 未提供

**错误信息**：
```
BlocProvider.of() called with a context that does not contain a Bloc of type AuthBloc.
```

**诊断步骤**：
1. 检查是否在 Widget 树中提供了 BLoC
2. 检查 context 是否在正确的位置

**解决方案**：
```dart
// ❌ 错误
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // context 没有 BLoC
    final bloc = BlocProvider.of<AuthBloc>(context);
    return Container();
  }
}

// ✅ 正确
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => AuthBloc(),
      child: MaterialApp(
        home: MyWidget(),
      ),
    );
  }
}

// 或使用 Builder
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Builder(
      builder: (context) {
        final bloc = BlocProvider.of<AuthBloc>(context);
        return Container();
      },
    );
  }
}
```

### 2. Stream 订阅未取消

**错误信息**：
```
Bad state: Stream has already been listened to.
```

**诊断步骤**：
1. 检查 Stream 是否被多次订阅
2. 检查 dispose 时是否取消了订阅

**解决方案**：
```dart
class MyWidget extends StatefulWidget {
  @override
  _MyWidgetState createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  StreamSubscription? _subscription;

  @override
  void initState() {
    super.initState();
    _subscription = someStream.listen((data) {
      setState(() {
        // 更新状态
      });
    });
  }

  @override
  void dispose() {
    _subscription?.cancel();
    super.dispose();
  }
}
```

## 网络错误

### 1. 超时错误

**错误信息**：
```
DioError [DioErrorType.connectTimeout]: HttpException: Connection timed out
```

**诊断步骤**：
1. 检查网络连接
2. 检查超时配置

**解决方案**：
```dart
final dio = Dio(BaseOptions(
  baseUrl: 'https://api.example.com',
  connectTimeout: const Duration(seconds: 10),
  receiveTimeout: const Duration(seconds: 10),
  sendTimeout: const Duration(seconds: 10),
));
```

### 2. SSL 错误

**错误信息**：
```
HandshakeException: Handshake error in client
```

**诊断步骤**：
1. 检查证书是否有效
2. 检查 HTTPS 配置

**解决方案**：
```dart
// 仅用于开发环境
final dio = Dio();
(dio.httpClientAdapter as IOHttpClientAdapter).onHttpClientCreate = (client) {
  client.badCertificateCallback = (cert, host, port) => true;
  return client;
};
```

## 布局错误

### 1. RenderFlex overflow

**错误信息**：
```
RenderFlex children overflowed by ... pixels.
```

**诊断步骤**：
1. 使用调试工具查看布局
2. 识别溢出的 Widget

**解决方案**：
```dart
// ❌ 错误
Row(
  children: [
    Text('Very long text that might overflow'),
    Text('Another text'),
  ],
)

// ✅ 正确 - 使用 Expanded
Row(
  children: [
    Expanded(
      child: Text('Very long text that might overflow'),
    ),
    Text('Another text'),
  ],
)

// ✅ 正确 - 使用 Flexible
Row(
  children: [
    Flexible(
      child: Text('Very long text that might overflow'),
    ),
    Text('Another text'),
  ],
)

// ✅ 正确 - 使用 Wrap
Wrap(
  children: [
    Text('Very long text'),
    Text('Another text'),
  ],
)
```

### 2. BoxConstraints 错误

**错误信息**：
```
BoxConstraints forces an infinite width
```

**诊断步骤**：
1. 检查是否在无限约束空间中使用需要固定尺寸的 Widget
2. 检查 Expanded/Flexible 的使用

**解决方案**：
```dart
// ❌ 错误
Row(
  children: [
    Container(
      width: 100, // 在 Row 中使用固定宽度可能导致问题
      child: Text('Hello'),
    ),
  ],
)

// ✅ 正确
Row(
  children: [
    SizedBox(
      width: 100,
      child: Text('Hello'),
    ),
  ],
)
```

## 诊断工具

### 1. 使用 Flutter DevTools

```bash
# 启动 DevTools
flutter pub global activate devtools
flutter pub global run devtools
```

### 2. 使用日志

```dart
import 'package:logging/logging.dart';

final logger = Logger('MyApp');

try {
  // 可能出错的代码
} catch (e, stackTrace) {
  logger.severe('Error occurred', e, stackTrace);
}
```

### 3. 使用断点调试

在 IDE 中设置断点，使用调试器查看变量值和调用栈。

## 预防措施

1. **空安全**
   - 始终使用正确的 null 处理
   - 使用 ? 和 ?? 操作符

2. **防御性编程**
   - 添加边界检查
   - 使用 try-catch 处理异常

3. **单元测试**
   - 覆盖边界情况
   - 测试错误处理

4. **日志记录**
   - 记录关键操作
   - 记录错误信息

## 快速参考

```dart
// 常用错误处理模式

// 1. 空值检查
final value = nullableValue ?? defaultValue;

// 2. 安全导航
final name = user?.name ?? 'Unknown';

// 3. 防御性 setState
if (mounted) {
  setState(() {});
}

// 4. 异步错误处理
try {
  await someAsyncOperation();
} catch (e) {
  debugPrint('Error: $e');
}

// 5. 列表安全访问
final item = list.isNotEmpty ? list[0] : null;
```
