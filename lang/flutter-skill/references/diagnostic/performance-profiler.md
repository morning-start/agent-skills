# Flutter Performance Profiling 指南

## 目录
- [性能分析工具](#性能分析工具)
- [常见性能问题](#常见性能问题)
- [优化技巧](#优化技巧)
- [性能监控](#性能监控)

## 概览
本指南提供 Flutter 应用性能分析和优化的系统性方法。

## 性能分析工具

### 1. Flutter DevTools

**安装和启动**：
```bash
flutter pub global activate devtools
flutter pub global run devtools
```

**主要功能**：
- Performance：帧率分析
- Memory：内存使用分析
- Network：网络请求跟踪
- Timeline：时间线分析

### 2. Flutter Inspector

在 Android Studio 或 VS Code 中打开 Flutter Inspector，查看：
- Widget 树
- 渲染性能
- 布局边界

### 3. Performance Overlay

启用性能覆盖层：

```dart
MaterialApp(
  showPerformanceOverlay: true, // 显示性能覆盖层
  home: MyApp(),
);
```

覆盖层显示：
- GPU 线程帧率
- UI 线程帧率
- 内存使用

## 常见性能问题

### 1. Jank（掉帧）

**症状**：动画不流畅，UI 响应慢

**诊断步骤**：
1. 使用 DevTools Performance 面板
2. 查找超过 16ms 的帧（60fps 标准）
3. 识别瓶颈

**常见原因**：
- UI 线程上有繁重计算
- 大量 Widget 重建
- 复杂的布局计算
- 同步 I/O 操作

**解决方案**：

#### 移除计算到 isolate
```dart
// ❌ 错误 - 在 UI 线程计算
void heavyComputation() {
  final result = complexCalculation();
  setState(() {
    // 更新 UI
  });
}

// ✅ 正确 - 使用 isolate
void heavyComputation() async {
  final result = await compute(complexCalculation, data);
  setState(() {
    // 更新 UI
  });
}
```

#### 优化 Widget 重建
```dart
// ❌ 错误 - 整个列表重建
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ExpensiveWidget(items[index]);
  },
)

// ✅ 正确 - 使用 const 和优化
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return const ExpensiveWidgetWrapper(item: items[index]);
  },
)
```

### 2. 内存泄漏

**症状**：应用内存持续增长，最终崩溃

**诊断步骤**：
1. 使用 DevTools Memory 面板
2. 执行内存快照
3. 对比快照查找增长对象

**常见原因**：
- Stream 订阅未取消
- AnimationController 未释放
- 闭包持有 Context 引用
- 全局缓存未清理

**解决方案**：

#### 取消 Stream 订阅
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
      setState(() {});
    });
  }

  @override
  void dispose() {
    _subscription?.cancel(); // 取消订阅
    super.dispose();
  }
}
```

#### 释放 AnimationController
```dart
class MyWidget extends StatefulWidget {
  @override
  _MyWidgetState createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 1),
      vsync: this,
    );
  }

  @override
  void dispose() {
    _controller.dispose(); // 释放控制器
    super.dispose();
  }
}
```

### 3. 启动慢

**症状**：应用启动时间长

**诊断步骤**：
1. 使用 DevTools Timeline 面板
2. 分析启动帧
3. 识别耗时操作

**解决方案**：

#### 延迟初始化
```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // ❌ 错误 - 在 main 中同步初始化
  await Firebase.initializeApp();
  await SharedPreferences.getInstance();

  runApp(MyApp());
}

// ✅ 正确 - 延迟初始化
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  void initState() {
    super.initState();
    _initializeServices();
  }

  Future<void> _initializeServices() async {
    await Firebase.initializeApp();
    await SharedPreferences.getInstance();
    // 其他初始化
  }
}
```

### 4. 列表滚动性能差

**症状**：长列表滚动卡顿

**解决方案**：

#### 使用 ListView.builder
```dart
// ❌ 错误 - 一次性创建所有子项
ListView(
  children: items.map((item) => ItemWidget(item)).toList(),
)

// ✅ 正确 - 按需创建
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ItemWidget(items[index]);
  },
)
```

#### 使用 AutomaticKeepAliveClientMixin
```dart
class ItemWidget extends StatefulWidget {
  final Item item;

  const ItemWidget(this.item);

  @override
  _ItemWidgetState createState() => _ItemWidgetState();
}

class _ItemWidgetState extends State<ItemWidget>
    with AutomaticKeepAliveClientMixin {
  @override
  bool get wantKeepAlive => true;

  @override
  Widget build(BuildContext context) {
    super.build(context);
    return Text(widget.item.name);
  }
}
```

## 优化技巧

### 1. 使用 const 构造函数

```dart
// ❌ 错误
Container(
  padding: const EdgeInsets.all(8.0),
  child: const Text('Hello'),
)

// ✅ 正确
const Padding(
  padding: EdgeInsets.all(8.0),
  child: Text('Hello'),
)
```

### 2. 拆分 Widget

```dart
// ❌ 错误 - 过大的 Widget
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          Header(),
          Body(), // 复杂的 Body
          Footer(),
        ],
      ),
    );
  }
}

// ✅ 正确 - 拆分为小 Widget
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: const [
          Header(),
          BodyWidget(),
          Footer(),
        ],
      ),
    );
  }
}
```

### 3. 使用 RepaintBoundary

隔离重绘区域：

```dart
RepaintBoundary(
  child: ExpensiveWidget(),
)
```

### 4. 使用 Image 缓存

```dart
CachedNetworkImage(
  imageUrl: 'https://example.com/image.jpg',
  placeholder: (context, url) => CircularProgressIndicator(),
  errorWidget: (context, url, error) => Icon(Icons.error),
)
```

### 5. 使用 ListView.separated

```dart
ListView.separated(
  itemCount: items.length,
  separatorBuilder: (context, index) => Divider(),
  itemBuilder: (context, index) {
    return ItemWidget(items[index]);
  },
)
```

## 性能监控

### 1. 帧率监控

```dart
class PerformanceMonitor extends StatefulWidget {
  @override
  _PerformanceMonitorState createState() => _PerformanceMonitorState();
}

class _PerformanceMonitorState extends State<PerformanceMonitor> {
  int _frameCount = 0;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      setState(() {
        _frameCount = 0;
      });
    });

    SchedulerBinding.instance.addTimingsCallback((timings) {
      for (final frame in timings) {
        if (frame.timestamp.inMilliseconds % 16 == 0) {
          _frameCount++;
        }
      }
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Text('FPS: $_frameCount');
  }
}
```

### 2. 内存监控

```dart
void printMemoryUsage() {
  final info = ProcessInfo.currentRss;
  final memoryMB = info / 1024 / 1024;
  print('Memory usage: $memoryMB MB');
}
```

### 3. 网络监控

```dart
Dio dio = Dio();

dio.interceptors.add(InterceptorsWrapper(
  onRequest: (options, handler) {
    final startTime = DateTime.now();
    options.extra['startTime'] = startTime;
    return handler.next(options);
  },
  onResponse: (response, handler) {
    final startTime = response.requestOptions.extra['startTime'] as DateTime;
    final duration = DateTime.now().difference(startTime);
    print('Request to ${response.requestOptions.uri} took ${duration.inMilliseconds}ms');
    return handler.next(response);
  },
));
```

## 性能基准

### 目标指标

- **帧率**：60fps（移动端）
- **启动时间**：< 3秒
- **内存使用**：< 150MB（应用运行时）
- **首屏渲染**：< 1秒

### 性能测试

```dart
void testPerformance() {
  final stopwatch = Stopwatch()..start();

  // 执行操作
  performOperation();

  stopwatch.stop();
  print('Operation took ${stopwatch.elapsedMilliseconds}ms');
}
```

## 最佳实践

1. **避免在 build 中进行计算**
2. **使用 const 构造函数**
3. **合理使用缓存**
4. **优化列表渲染**
5. **及时释放资源**
6. **使用 DevTools 定期分析**

## 快速参考

```bash
# 性能分析命令

# 运行性能分析
flutter run --profile

# 生成性能报告
flutter build apk --profile
flutter build apk --analyze-size

# 查看 APK 大小
flutter build apk --split-per-abi
```
