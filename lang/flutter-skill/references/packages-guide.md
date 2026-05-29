# Flutter 常用库分类指南

## 目录
- [状态管理](#状态管理)
- [路由与导航](#路由与导航)
- [网络请求与数据解析](#网络请求与数据解析)
- [本地存储与缓存](#本地存储与缓存)
- [依赖注入](#依赖注入)
- [UI 增强与组件库](#ui-增强与组件库)
- [表单验证](#表单验证)
- [国际化与本地化](#国际化与本地化)
- [工具与辅助](#工具与辅助)
- [测试相关](#测试相关)
- [性能与调试](#性能与调试)

## 概览
本指南提供现代 Flutter 开发中常用的高质量第三方库分类说明，帮助开发者选择合适的技术栈。基于 Flutter 3.24 + Dart 3.5 版本。

## 状态管理（State Management）

### Riverpod
- **功能**：比 Provider 更强大、更灵活的状态管理方案，支持异步、依赖注入、测试友好
- **优势**：编译时安全、无上下文依赖、支持 Provider 范式但更现代化
- **适用场景**：中小型项目、需要依赖注入的场景
- **最新版本**：^2.4.0

```yaml
dependencies:
  flutter_riverpod: ^2.4.0
```

```dart
// 定义 Provider
final counterProvider = StateProvider<int>((ref) => 0);

// 使用
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return ElevatedButton(
      onPressed: () => ref.read(counterProvider.notifier).state++,
      child: Text('Count: $count'),
    );
  }
}
```

### Bloc / Cubit (flutter_bloc)
- **功能**：基于 BLoC（Business Logic Component）模式，将 UI 与业务逻辑分离
- **适用场景**：中大型项目，强调可测试性和可维护性
- **优势**：清晰的事件流、状态可预测、易于测试
- **最新版本**：^9.1.1

```yaml
dependencies:
  flutter_bloc: ^9.1.1
  equatable: ^2.0.5
```

```dart
// 定义 Event
abstract class CounterEvent {}
class CounterIncrementPressed extends CounterEvent {}

// 定义 State
class CounterState extends Equatable {
  final int count;
  const CounterState({this.count = 0});

  @override
  List<Object> get props => [count];
}

// 定义 Bloc
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  CounterBloc() : super(CounterState()) {
    on<CounterIncrementPressed>((event, emit) {
      emit(state.copyWith(count: state.count + 1));
    });
  }
}
```

## 路由与导航（Routing & Navigation）

### go_router（官方推荐）
- **功能**：声明式路由，支持深度链接、嵌套路由、参数传递、重定向等
- **优势**：与 Web 兼容性好，适合多平台（Web、移动端）
- **适用场景**：需要深度链接支持的项目
- **最新版本**：^13.0.0

```yaml
dependencies:
  go_router: ^13.0.0
```

```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/user/:id',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return UserScreen(userId: id);
      },
    ),
  ],
);

MaterialApp.router(
  routerConfig: router,
);
```

### auto_route
- **功能**：基于注解生成类型安全的路由代码，减少样板代码
- **特点**：编译时生成路由表，错误更早暴露
- **适用场景**：大型项目，强调类型安全
- **最新版本**：^8.0.0

```yaml
dependencies:
  auto_route: ^8.0.0

dev_dependencies:
  auto_route_generator: ^8.0.0
  build_runner: ^2.4.0
```

```dart
@RoutePage()
class UserScreen extends StatelessWidget {
  const UserScreen({@PathParam('id') required this.id});
  final String id;
}

@AutoRouterConfig()
class AppRouter extends $AppRouter {
  @override
  List<AutoRoute> get routes => [
    AutoRoute(page: HomeRoute.page, initial: true),
    AutoRoute(page: UserRoute.page),
  ];
}
```

## 网络请求与数据解析

### Dio
- **功能**：强大的 HTTP 客户端，支持拦截器、超时、文件上传/下载、Cookie 管理等
- **替代**：原生 http 包，适用于复杂网络需求
- **优势**：功能全面、插件生态丰富
- **最新版本**：^5.4.0

```yaml
dependencies:
  dio: ^5.4.0
```

```dart
final dio = Dio(BaseOptions(
  baseUrl: 'https://api.example.com',
  connectTimeout: Duration(seconds: 5),
));

// 添加拦截器
dio.interceptors.add(InterceptorsWrapper(
  onRequest: (options, handler) {
    options.headers['Authorization'] = 'Bearer $token';
    handler.next(options);
  },
  onError: (error, handler) {
    // 错误处理
    handler.next(error);
  },
));

// 发起请求
final response = await dio.get('/users');
final data = response.data;
```

### Retrofit.dart（配合 Dio）
- **功能**：通过注解自动生成 API 调用代码，类似 Java 的 Retrofit
- **优势**：提升 API 层的整洁性和可维护性
- **适用场景**：RESTful API 项目
- **最新版本**：^4.0.0

```yaml
dependencies:
  dio: ^5.4.0
  retrofit: ^4.0.0
  json_annotation: ^4.8.0

dev_dependencies:
  build_runner: ^2.4.0
  retrofit_generator: ^8.0.0
  json_serializable: ^6.7.0
```

```dart
@RestApi(baseUrl: "https://api.example.com")
abstract class UserApi {
  factory UserApi(Dio dio) = _UserApi;

  @GET("/users/{id}")
  Future<User> getUser(@Path("id") String id);

  @POST("/users")
  Future<User> createUser(@Body() User user);

  @DELETE("/users/{id}")
  Future<void> deleteUser(@Path("id") String id);
}
```

### json_serializable + json_annotation
- **功能**：自动生成 JSON 序列化/反序列化代码，避免手写 fromJson/toJson
- **配置**：配合 build_runner 使用
- **优势**：类型安全、性能优化
- **最新版本**：^6.7.0

```yaml
dependencies:
  json_annotation: ^4.8.0

dev_dependencies:
  json_serializable: ^6.7.0
  build_runner: ^2.4.0
```

```dart
import 'package:json_annotation/json_annotation.dart';

part 'user.g.dart';

@JsonSerializable()
class User {
  final String id;
  final String name;
  final String email;

  User({required this.id, required this.name, required this.email});

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

## 本地存储与缓存

### Isar（推荐）
- **功能**：专为 Flutter 打造的超高速 NoSQL 数据库
- **优势**：比 Hive 更快、支持全文检索、ACID 语义、类型安全
- **适用场景**：中大型应用，需要高性能数据存储
- **最新版本**：^3.1.8（从社区源安装）

```yaml
dependencies:
  isar:
    version: 3.1.8
    hosted: https://pub.isar-community.dev/
  isar_flutter_libs:
    version: 3.1.8
    hosted: https://pub.isar-community.dev/

dev_dependencies:
  isar_generator:
    version: 3.1.8
    hosted: https://pub.isar-community.dev/
  build_runner: ^2.4.0
```

```dart
// 定义数据模型
import 'package:isar/isar.dart';

part 'user.g.dart';

@collection
class User {
  @Id()
  int? id;

  @Index()
  late String name;

  late String email;

  List<String>? tags;
}

// 打开数据库
final dir = await getApplicationDocumentsDirectory();
final isar = await Isar.open([UserSchema], directory: dir.path);

// 写入数据
final user = User()
  ..name = 'John'
  ..email = 'john@example.com';

await isar.writeTxn(() async {
  await isar.users.put(user);
});

// 查询数据
final users = await isar.users
  .where()
  .nameContains('John')
  .findAll();

// 监听数据变化
isar.users.where().watchLazy().listen((_) {
  print('Data changed!');
});
```

### Hive
- **功能**：轻量、快速的 NoSQL 本地数据库，支持对象存储、加密、跨平台
- **优势**：无需原生桥接，性能优于 shared_preferences（尤其在大量数据时）
- **适用场景**：复杂数据存储、需要高性能的场景
- **最新版本**：^2.2.3

```yaml
dependencies:
  hive: ^2.2.3
  hive_flutter: ^1.1.0

dev_dependencies:
  hive_generator: ^2.0.0
  build_runner: ^2.4.0
```

```dart
// 定义模型
import 'package:hive/hive.dart';

part 'user.g.dart';

@HiveType(typeId: 0)
class User extends HiveObject {
  @HiveField(0)
  String name;

  @HiveField(1)
  String email;
}

// 打开数据库
await Hive.initFlutter();
final box = await Hive.openBox<User>('users');

// 写入数据
final user = User()
  ..name = 'John'
  ..email = 'john@example.com';
box.add(user);

// 读取数据
final users = box.values.toList();
```

### shared_preferences
- **功能**：存储简单的键值对（如用户设置、token），适合小量数据
- **适用场景**：配置项、用户偏好设置
- **最新版本**：^2.2.0

```yaml
dependencies:
  shared_preferences: ^2.2.0
```

```dart
final prefs = await SharedPreferences.getInstance();

// 保存数据
await prefs.setString('token', 'your_token_here');
await prefs.setBool('isLoggedIn', true);
await prefs.setInt('userId', 123);

// 读取数据
final token = prefs.getString('token');
final isLoggedIn = prefs.getBool('isLoggedIn') ?? false;
final userId = prefs.getInt('userId') ?? 0;
```

### flutter_secure_storage
- **功能**：安全存储敏感信息（如 token、密码），使用系统级安全存储（Keychain/Keystore）
- **适用场景**：存储认证信息、敏感数据
- **最新版本**：^9.0.0

```yaml
dependencies:
  flutter_secure_storage: ^9.0.0
```

```dart
final storage = FlutterSecureStorage();

// 存储敏感数据
await storage.write(key: 'jwt_token', value: 'your_jwt_token');
await storage.write(key: 'api_key', value: 'your_api_key');

// 读取数据
final token = await storage.read(key: 'jwt_token');

// 删除数据
await storage.delete(key: 'jwt_token');

// 删除所有数据
await storage.deleteAll();

// 检查是否存在
final containsToken = await storage.containsKey(key: 'jwt_token');
```

## 依赖注入

### GetIt + Injectable
- **功能**：轻量级服务定位器，配合 Injectable 实现编译时依赖注入
- **优势**：性能优秀、易于测试、减少样板代码
- **适用场景**：中大型项目，需要依赖注入管理
- **最新版本**：GetIt ^7.6.0, Injectable ^2.3.0

```yaml
dependencies:
  get_it: ^7.6.0
  injectable: ^2.3.0

dev_dependencies:
  injectable_generator: ^2.4.0
  build_runner: ^2.4.0
```

```dart
// 定义依赖
import 'package:injectable/injectable.dart';

@module
abstract class AppModule {
  @lazySingleton
  Dio provideDio() => Dio();

  @lazySingleton
  UserRepository provideUserRepository(Dio dio) =>
      UserRepositoryImpl(dio: dio);
}

@injectable
class UserRepositoryImpl implements UserRepository {
  final Dio dio;

  UserRepositoryImpl({required this.dio});
}

// 初始化依赖容器
final getIt = GetIt.instance;

@InjectableInit()
void configureDependencies() {
  getIt.init();
}

void main() {
  configureDependencies();
  runApp(MyApp());
}

// 使用依赖
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final userRepository = getIt<UserRepository>();
    return ...
  }
}
```

## UI 增强与组件库

### flutter_svg
- **功能**：渲染 SVG 图像，解决原生不支持 SVG 的问题
- **适用场景**：需要高质量矢量图标的场景
- **最新版本**：^2.0.0

```yaml
dependencies:
  flutter_svg: ^2.0.0
```

```dart
import 'package:flutter_svg/flutter_svg.dart';

SvgPicture.asset(
  'assets/icons/logo.svg',
  width: 100,
  height: 100,
  color: Colors.blue,
)

// 从网络加载
SvgPicture.network(
  'https://example.com/icon.svg',
)
```

### cached_network_image
- **功能**：加载并缓存网络图片，支持占位图、错误图、内存/磁盘缓存
- **适用场景**：图片密集型应用
- **最新版本**：^3.3.0

```yaml
dependencies:
  cached_network_image: ^3.3.0
```

```dart
CachedNetworkImage(
  imageUrl: 'https://example.com/image.jpg',
  placeholder: (context, url) => CircularProgressIndicator(),
  errorWidget: (context, url, error) => Icon(Icons.error),
  fadeInDuration: Duration(milliseconds: 500),
)
```

### animations（官方）
- **功能**：提供 Material Design 风格的预置动画组件（如 OpenContainer）
- **适用场景**：Material Design 应用
- **最新版本**：^2.0.0

```yaml
dependencies:
  animations: ^2.0.0
```

```dart
import 'package:animations/animations.dart';

OpenContainer(
  closedColor: Colors.blue,
  openColor: Colors.blue,
  closedBuilder: (context, openContainer) {
    return ElevatedButton(
      onPressed: openContainer,
      child: Text('Open Details'),
    );
  },
  openBuilder: (context, closeContainer) {
    return DetailsPage();
  },
)
```

### shimmer
- **功能**：实现加载骨架屏（Skeleton Loading）效果
- **适用场景**：优化加载体验
- **最新版本**：^3.0.0

```yaml
dependencies:
  shimmer: ^3.0.0
```

```dart
Shimmer.fromColors(
  baseColor: Colors.grey[300]!,
  highlightColor: Colors.grey[100]!,
  child: Container(
    width: 100,
    height: 100,
    decoration: BoxDecoration(
      color: Colors.grey,
      borderRadius: BorderRadius.circular(10),
    ),
  ),
)
```

## 表单验证

### reactive_forms
- **功能**：响应式表单验证，类似 Angular Reactive Forms
- **优势**：类型安全、强大的验证规则、易于测试
- **适用场景**：复杂表单验证场景
- **最新版本**：^16.0.0

```yaml
dependencies:
  reactive_forms: ^16.0.0
```

```dart
import 'package:reactive_forms/reactive_forms.dart';

class LoginForm extends StatelessWidget {
  final form = FormGroup({
    'email': FormControl<String>(
      validators: [Validators.required, Validators.email],
    ),
    'password': FormControl<String>(
      validators: [
        Validators.required,
        Validators.minLength(6),
      ],
    ),
  });

  @override
  Widget build(BuildContext context) {
    return ReactiveForm(
      formGroup: form,
      child: Column(
        children: [
          ReactiveTextField<String>(
            formControlName: 'email',
            validationMessages: {
              ValidationMessage.required: (_) => 'Email is required',
              ValidationMessage.email: (_) => 'Invalid email',
            },
            decoration: InputDecoration(
              labelText: 'Email',
            ),
          ),
          ReactiveTextField<String>(
            formControlName: 'password',
            validationMessages: {
              ValidationMessage.required: (_) => 'Password is required',
              ValidationMessage.minLength: (_) => 'Password too short',
            },
            decoration: InputDecoration(
              labelText: 'Password',
            ),
            obscureText: true,
          ),
          ReactiveFormConsumer(
            builder: (context, form, child) {
              return ElevatedButton(
                onPressed: form.valid ? () => _submit() : null,
                child: Text('Login'),
              );
            },
          ),
        ],
      ),
    );
  }

  void _submit() {
    print(form.value);
  }
}
```

## 国际化与本地化（i18n）

### flutter_localizations（官方） + intl
- **功能**：支持多语言切换，配合 ARB 文件管理翻译文本
- **适用场景**：需要国际化的项目
- **最新版本**：intl ^0.19.0

```yaml
dependencies:
  flutter_localizations:
    sdk: flutter
  intl: ^0.19.0

flutter:
  generate: true
```

```dart
// lib/l10n/app_en.arb
{
  "@@locale": "en",
  "hello": "Hello",
  "welcome": "Welcome, {name}!",
  "@welcome": {
    "description": "A welcome message",
    "placeholders": {
      "name": {
        "type": "String",
        "example": "John"
      }
    }
  }
}

// lib/l10n/app_zh.arb
{
  "@@locale": "zh",
  "hello": "你好",
  "welcome": "欢迎，{name}！",
  "@welcome": {
    "description": "欢迎消息",
    "placeholders": {
      "name": {
        "type": "String",
        "example": "张三"
      }
    }
  }
}

// 在代码中使用
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

MaterialApp(
  localizationsDelegates: AppLocalizations.localizationsDelegates,
  supportedLocales: AppLocalizations.supportedLocales,
  home: MyWidget(),
)

class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    return Text(l10n.hello);
  }
}
```

### easy_localization
- **功能**：简化国际化流程，支持从 JSON 或 CSV 加载语言资源，自动检测系统语言
- **优势**：配置简单、支持多格式
- **最新版本**：^3.0.0

```yaml
dependencies:
  easy_localization: ^3.0.0
```

```dart
// assets/i18n/en-US.json
{
  "hello": "Hello",
  "welcome": "Welcome"
}

// assets/i18n/zh-CN.json
{
  "hello": "你好",
  "welcome": "欢迎"
}

// 在代码中使用
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await EasyLocalization.ensureInitialized();
  runApp(
    EasyLocalization(
      supportedLocales: [Locale('en', 'US'), Locale('zh', 'CN')],
      path: 'assets/i18n',
      fallbackLocale: Locale('en', 'US'),
      child: MyApp(),
    ),
  );
}

Text('hello'.tr())
```

## 工具与辅助

### freezed
- **功能**：生成不可变类（immutable）、联合类型（sealed classes）、copyWith、== 重写等
- **优势**：减少样板代码、提高代码质量
- **搭配**：常与 json_serializable 搭配使用
- **最新版本**：^2.4.0

```yaml
dependencies:
  freezed_annotation: ^2.4.0

dev_dependencies:
  freezed: ^2.4.0
  build_runner: ^2.4.0
```

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    String? email,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

// 使用
final user1 = User(id: '1', name: 'John');
final user2 = user1.copyWith(name: 'Jane');

if (user1 == user2) {
  print('Users are equal');
}
```

### dartz
- **功能**：提供函数式编程工具，如 Either，用于错误处理
- **适用场景**：Clean Architecture 项目
- **最新版本**：^0.10.1

```yaml
dependencies:
  dartz: ^0.10.1
```

```dart
import 'package:dartz/dartz.dart';

Either<Failure, User> getUser(String id) {
  try {
    final user = userRepository.getUser(id);
    return Right(user);
  } catch (e) {
    return Left(Failure('Failed to get user'));
  }
}

// 使用
final result = getUser('123');
result.fold(
  (failure) => print('Error: ${failure.message}'),
  (user) => print('User: ${user.name}'),
);
```

### equatable
- **功能**：简化对象相等性比较（替代手写 == 和 hashCode）
- **适用场景**：需要值类型比较的场景
- **最新版本**：^2.0.5

```yaml
dependencies:
  equatable: ^2.0.5
```

```dart
import 'package:equatable/equatable.dart';

class User extends Equatable {
  final String id;
  final String name;

  const User({required this.id, required this.name});

  @override
  List<Object> get props => [id, name];
}

// 使用
final user1 = User(id: '1', name: 'John');
final user2 = User(id: '1', name: 'John');

if (user1 == user2) {
  print('Users are equal');
}
```

## 测试相关

### mocktail
- **功能**：单元测试中的 Mock 工具，无需代码生成
- **优势**：更适配 Dart 新特性（null safety）
- **推荐**：优先使用 mocktail 替代 mockito
- **最新版本**：^1.0.0

```yaml
dev_dependencies:
  mocktail: ^1.0.0
  flutter_test:
    sdk: flutter
```

```dart
import 'package:mocktail/mocktail.dart';
import 'package:flutter_test/flutter_test.dart';

class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late MockUserRepository mockRepository;
  late GetUser usecase;

  setUp(() {
    mockRepository = MockUserRepository();
    usecase = GetUser(mockRepository);
  });

  test('should get user from repository', () async {
    // Arrange
    const tUser = User(id: '1', name: 'John');
    when(() => mockRepository.getUser(any()))
        .thenAnswer((_) async => tUser);

    // Act
    final result = await usecase(Params(id: '1'));

    // Assert
    expect(result, tUser);
    verify(() => mockRepository.getUser('1')).called(1);
  });
}
```

### integration_test
- **功能**：集成测试，测试完整的用户流程
- **适用场景**：端到端测试
- **最新版本**：随 Flutter SDK

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('login flow', (tester) async {
    app.main();
    await tester.pumpAndSettle();

    await tester.enterText(find.byKey(Key('email_field')), 'test@test.com');
    await tester.enterText(find.byKey(Key('password_field')), 'password');
    await tester.tap(find.text('Login'));
    await tester.pumpAndSettle();

    expect(find.text('Welcome'), findsOneWidget);
  });
}
```

## 性能与调试

### flutter_performance_monitoring
- **功能**：监控应用性能指标（如帧率、HTTP 请求耗时）
- **适用场景**：需要性能监控的生产环境
- **替代方案**：Firebase Performance Monitoring

### devtools（官方）
- **功能**：调试内存、CPU、网络、Widget 树等
- **适用场景**：开发和调试阶段
- **启动方式**：flutter pub global run devtools

```bash
# 启动 DevTools
flutter pub global activate devtools
flutter pub global run devtools

# 或通过 VS Code
# Ctrl+Shift+P -> Flutter: Open DevTools
```

## 技术栈推荐

### 小型项目（MVP、原型）
```yaml
dependencies:
  # 状态管理
  flutter_riverpod: ^2.4.0

  # 网络请求
  dio: ^5.4.0

  # 本地存储
  hive: ^2.2.3
  hive_flutter: ^1.1.0

  # 图片加载
  cached_network_image: ^3.3.0
```

**特点**：快速启动、学习曲线平缓、功能完备

### 中大型项目（企业级应用）
```yaml
dependencies:
  # 状态管理
  flutter_bloc: ^9.1.1
  equatable: ^2.0.5

  # 路由
  go_router: ^13.0.0

  # 网络请求
  dio: ^5.4.0
  retrofit: ^4.0.0

  # 数据模型
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.0

  # 本地存储
  isar:
    version: 3.1.8
    hosted: https://pub.isar-community.dev/
  isar_flutter_libs:
    version: 3.1.8
    hosted: https://pub.isar-community.dev/

  # 错误处理
  dartz: ^0.10.1

  # 依赖注入
  get_it: ^7.6.0
  injectable: ^2.3.0

  # 测试
  mocktail: ^1.0.0
  bloc_test: ^9.1.0

dev_dependencies:
  build_runner: ^2.4.0
  freezed: ^2.4.0
  json_serializable: ^6.7.0
  retrofit_generator: ^8.0.0
  injectable_generator: ^2.4.0
```

**特点**：类型安全、可测试性强、可维护性高

### 强调类型安全与可维护性
优先选择代码生成类库：
- **模型**：freezed、json_serializable
- **路由**：auto_route
- **依赖注入**：injectable
- **数据模型**：freezed + isar

## 完整 pubspec.yaml 示例

```yaml
name: flutter_app
description: A modern Flutter application
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter

  # 状态管理
  flutter_bloc: ^9.1.1
  equatable: ^2.0.5

  # 路由
  go_router: ^13.0.0

  # 网络请求
  dio: ^5.4.0
  retrofit: ^4.0.0

  # 数据模型
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.0

  # 本地存储
  isar:
    version: 3.1.8
    hosted: https://pub.isar-community.dev/
  isar_flutter_libs:
    version: 3.1.8
    hosted: https://pub.isar-community.dev/
  shared_preferences: ^2.2.0
  flutter_secure_storage: ^9.0.0

  # 工具库
  dartz: ^0.10.1
  get_it: ^7.6.0
  injectable: ^2.3.0

  # UI 组件
  flutter_svg: ^2.0.0
  cached_network_image: ^3.3.0
  shimmer: ^3.0.0

  # 表单验证
  reactive_forms: ^16.0.0

  # 国际化
  flutter_localizations:
    sdk: flutter
  intl: ^0.19.0

  cupertino_icons: ^1.0.2

dev_dependencies:
  flutter_test:
    sdk: flutter

  # 代码生成
  build_runner: ^2.4.0
  freezed: ^2.4.0
  json_serializable: ^6.7.0
  retrofit_generator: ^8.0.0
  injectable_generator: ^2.4.0

  # 测试
  mocktail: ^1.0.0
  bloc_test: ^9.1.0

  # Linting
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
  generate: true

  assets:
    - assets/images/
    - assets/icons/
```

## 最佳实践

1. **依赖管理**
   - 定期更新依赖：`flutter pub upgrade`
   - 检查过期依赖：`flutter pub outdated`
   - 使用版本范围，但不要过于宽松

2. **代码生成**
   - 在使用代码生成库后运行：`dart run build_runner build --delete-conflicting-outputs`
   - 持续监听模式：`dart run build_runner watch --delete-conflicting-outputs`

3. **性能优化**
   - 优先使用 const 构造函数
   - 避免不必要的 rebuild
   - 使用 ListView.builder 处理长列表

4. **测试**
   - 保持高测试覆盖率（>70%）
   - 使用 mocktail 进行单元测试
   - 编写集成测试验证关键流程

5. **文档**
   - 为公共 API 编写文档注释
   - 使用示例代码
   - 维护 README 和 CHANGELOG
