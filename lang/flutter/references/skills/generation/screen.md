---
name: screen
description: Генерация и рефакторинг Flutter экранов для Beeline v4 с Clean Architecture + BLoC + Design System
---

# 🚀 Beeline Screen Generator

## Когда использовать

✅ **Использовать:**
- "Создай экран/скрин..."
- "Нужен раздел..."
- "Отрефактори..."
- "Разбей на виджеты..."

❌ **НЕ использовать:**
- Pixel-perfect UI без архитектуры → `figma-integration`
- Простые виджеты без state → создать напрямую
- Мелкие UI правки → редактировать файл
- Баг-фиксы → дебажить конкретную проблему

---

## Workflow

### Этап 1: Анализ задачи

**Определить тип:**
- 🆕 Новый feature module
- 🔄 Рефакторинг существующего кода
- ✂️ Разбиение большого экрана

**Действия:**
```bash
# Проверить существующие файлы
ls packages/feature_*/lib/presentation/screens/
```

**✅ Checklist:**
- [ ] Тип задачи определен
- [ ] Существующие файлы проверены
- [ ] Понятно что создавать/менять

---

### Этап 2: Структура файлов

**Для нового feature module:**
```
feature_name/lib/
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── usecases/
├── data/
│   ├── datasources/
│   ├── models/
│   └── repositories/
├── presentation/
│   ├── bloc/
│   ├── screens/
│   └── widgets/
└── di/
```

**Определить виджеты для выделения:**
- Секция > 50 строк → отдельный файл
- Повторяющийся элемент → reusable widget

**✅ Checklist:**
- [ ] Структура папок создана/проверена
- [ ] Список виджетов для выделения готов

---

### Этап 3: Domain слой

**Entity** (`domain/entities/`):
```dart
class Payment extends Equatable {
  final String id;
  final double amount;

  const Payment({required this.id, required this.amount});

  @override
  List<Object?> get props => [id, amount];
}
```

**Repository interface** (`domain/repositories/`):
```dart
abstract class PaymentRepository {
  FutureResult<Payment> getPayment(String id);
  FutureResult<void> createPayment(Payment payment);
}
```

**UseCase** (`domain/usecases/`):
```dart
class GetPaymentUseCase {
  final PaymentRepository repository;

  GetPaymentUseCase(this.repository);

  FutureResult<Payment> call(String id) {
    return repository.getPayment(id);
  }
}
```

**✅ Checklist:**
- [ ] Entity с Equatable
- [ ] Repository interface с `FutureResult<T>`
- [ ] UseCase на каждое действие

---

### Этап 4: Data слой

**Model** (`data/models/`):
```dart
class PaymentModel {
  final String id;
  final double amount;

  PaymentModel({required this.id, required this.amount});

  factory PaymentModel.fromJson(Map<String, dynamic> json) => PaymentModel(
    id: json['id'] as String,
    amount: (json['amount'] as num).toDouble(),
  );

  Payment toEntity() => Payment(id: id, amount: amount);
}
```

**DataSource** (`data/datasources/`):
```dart
abstract class PaymentRemoteDataSource {
  Future<PaymentModel> getPayment(String id);
}

class PaymentRemoteDataSourceImpl implements PaymentRemoteDataSource {
  final HttpClient client;

  @override
  Future<PaymentModel> getPayment(String id) async {
    final response = await client.get('/payments/$id');
    return PaymentModel.fromJson(response.data);
  }
}
```

**Repository impl** (`data/repositories/`):
```dart
class PaymentRepositoryImpl implements PaymentRepository {
  final PaymentRemoteDataSource dataSource;

  @override
  FutureResult<Payment> getPayment(String id) async {
    try {
      final model = await dataSource.getPayment(id);
      return Right(model.toEntity());
    } catch (e) {
      return Left(Failure.fromException(e));
    }
  }
}
```

**✅ Checklist:**
- [ ] Model с fromJson/toEntity
- [ ] DataSource (mock или remote)
- [ ] Repository impl с try-catch → Failure

---

### Этап 5: Presentation слой

**BLoC Events** (`presentation/bloc/`):
```dart
sealed class PaymentEvent extends Equatable {
  const PaymentEvent();
}

class LoadPaymentEvent extends PaymentEvent {
  final String id;
  const LoadPaymentEvent(this.id);

  @override
  List<Object?> get props => [id];
}

class SubmitPaymentEvent extends PaymentEvent {
  final double amount;
  const SubmitPaymentEvent(this.amount);

  @override
  List<Object?> get props => [amount];
}
```

**BLoC States** - определяются по потребностям экрана:
```dart
sealed class PaymentState extends Equatable {
  const PaymentState();
}

// Состояния определяй исходя из UI:
// - Нужен loading? → добавь LoadingState
// - Нужен error? → добавь ErrorState
// - Какие данные показывать? → добавь соответствующие Loaded states

class PaymentLoadedState extends PaymentState {
  final Payment payment;
  const PaymentLoadedState(this.payment);

  @override
  List<Object?> get props => [payment];
}

class PaymentSubmittingState extends PaymentState {
  final Payment payment; // сохраняем данные во время отправки
  const PaymentSubmittingState(this.payment);

  @override
  List<Object?> get props => [payment];
}

class PaymentSuccessState extends PaymentState {
  final String transactionId;
  const PaymentSuccessState(this.transactionId);

  @override
  List<Object?> get props => [transactionId];
}
```

**BLoC**:
```dart
class PaymentBloc extends Bloc<PaymentEvent, PaymentState> {
  final GetPaymentUseCase getPayment;

  PaymentBloc(this.getPayment) : super(PaymentLoadedState(Payment.empty())) {
    on<LoadPaymentEvent>(_onLoad);
    on<SubmitPaymentEvent>(_onSubmit);
  }

  Future<void> _onLoad(LoadPaymentEvent event, Emitter<PaymentState> emit) async {
    final result = await getPayment(event.id);
    result.fold(
      (failure) => emit(PaymentErrorState(failure.message)),
      (payment) => emit(PaymentLoadedState(payment)),
    );
  }
}
```

**Screen** (`presentation/screens/`) - **MAX 200 строк!**

Выбор BlocBuilder vs BlocConsumer:
- **BlocBuilder** → только UI меняется от state
- **BlocConsumer** → UI + side effects (navigation, snackbar)

```dart
class PaymentScreen extends StatelessWidget {
  const PaymentScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => GetIt.instance<PaymentBloc>()..add(const LoadPaymentEvent('1')),
      child: Scaffold(
        appBar: BeelineAppBar.primary(title: context.l10n.payment),
        body: BlocConsumer<PaymentBloc, PaymentState>(
          listener: (context, state) {
            if (state is PaymentSuccessState) {
              context.push('/payment/success/${state.transactionId}');
            } else if (state is PaymentErrorState) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text(state.message)),
              );
            }
          },
          builder: (context, state) {
            if (state is PaymentLoadedState) {
              return PaymentContent(payment: state.payment);
            } else if (state is PaymentSubmittingState) {
              return PaymentContent(
                payment: state.payment,
                isSubmitting: true,
              );
            } else if (state is PaymentErrorState) {
              return AppErrorStateVariants.networkError(
                onRetry: () => context.read<PaymentBloc>().add(const LoadPaymentEvent('1')),
              );
            }
            // Fallback - не должен срабатывать при правильной логике
            return AppErrorStateVariants.loadingError(
              onRetry: () => context.read<PaymentBloc>().add(const LoadPaymentEvent('1')),
            );
          },
        ),
      ),
    );
  }
}
```

**✅ Checklist:**
- [ ] States определены по потребностям UI (не шаблонно)
- [ ] BlocBuilder или BlocConsumer выбран осознанно
- [ ] Все states обработаны через if/else if
- [ ] Fallback показывает error state (не пустой экран)
- [ ] Screen < 200 строк
- [ ] Секции выделены в widgets/

---

### Этап 6: Правила качества

**Применить ВСЕ правила:**

| # | Правило | Что делать | Проверка |
|---|---------|------------|----------|
| 1 | **< 200 строк** | Разбить на виджеты | `wc -l file.dart` |
| 2 | **Inline vs функция** | Inline если: <3 строк, 1 место. Функция если: много мест, >3-4 строк, нужно имя для читаемости | `grep "Widget _build"` |
| 3 | **Нет event chains** | Логика в UseCase/BLoC | Нет `add()` в handler |
| 4 | **< 100 символов** | Перенос строк | IDE warning |
| 5 | **BLoC vs StatefulWidget** | BLoC для API, Stateful для UI | — |
| 6 | **ScreenUtil везде** | `.w .h .sp .r` | `grep "fontSize: [0-9]"` |
| 7 | **Абсолютные импорты** | `package:feature_*` | Нет `../` |
| 8 | **const для static** | `const Text()`, `const SizedBox()` | — |
| 9 | **Виджеты сразу** | Определить структуру до кода | — |
| 10 | **Failure.fromException** | Единый класс ошибок | `grep "ServerFailure"` |
| 11 | **Design System** | AppColors.current, AppTextStyles | `grep "Color(0x"` |
| 12 | **Удалить unused** | Find Usages → Delete | `grep "WidgetName"` |
| 14 | **Нет дубликатов** | Extract shared widgets/utils | См. ниже |
| 13 | **Локализация** | `context.l10n.*` | `grep "Text('.*')"` |

**Детали каждого правила:** См. `references/rules_quick_ref.md`

---

### Этап 7: Финальная проверка

```bash
cd packages/feature_name
dart analyze --fatal-infos
```

**Быстрые проверки:**
```bash
# Файлы > 200 строк
find lib/presentation -name "*.dart" -exec wc -l {} + | awk '$1 > 200'

# Hardcoded colors
grep -rE "Color\(0x[0-9A-F]{8}\)" lib/presentation/

# Hardcoded text
grep -rE "Text\s*\(\s*['\"]" lib/presentation/

# Old static colors
grep -rE "AppColors\.(primary|textPrimary)" lib/ | grep -v "AppColors.current"

# _build functions
grep -r "Widget _build" lib/presentation/

# Дублирующиеся виджеты
grep -rh "class.*extends.*Widget" lib/ | sed 's/class \([^ ]*\).*/\1/' | sort | uniq -d

# Дублирующиеся классы (entities, models, blocs)
grep -rh "^class " lib/ | sed 's/class \([^ ]*\).*/\1/' | sort | uniq -d

# Похожие методы - проверить вручную:
# - Одинаковые названия в разных файлах
# - Похожая логика (копипаст)
grep -rh "void \|Future<\|Widget " lib/ | sed 's/.*\(void\|Future\|Widget\) \([a-zA-Z_]*\).*/\2/' | sort | uniq -c | sort -rn | head -20
```

**✅ Final Checklist:**
- [ ] `dart analyze` = 0 errors
- [ ] Все файлы < 200 строк
- [ ] Нет hardcoded colors/text
- [ ] Все импорты абсолютные
- [ ] Validators из core_utils

---

## Quick Reference

### Colors (Instance-Based!)

```dart
// ✅ С BuildContext (предпочтительно)
final colors = context.colors;
color: colors.primary

// ✅ Без BuildContext (BLoC, validators)
color: AppColors.current.primary

// ❌ FORBIDDEN
AppColors.primary  // Статический доступ удален!
const TextStyle(color: colors.primary)  // const + instance = ошибка!
```

**Детали:** См. `references/design_system.md`

### BLoC Patterns

```dart
// UI changes → BlocBuilder
BlocBuilder<Bloc, State>(builder: (context, state) => ...)

// Side effects (navigation, snackbar) → BlocListener
BlocListener<Bloc, State>(listener: (context, state) {
  if (state is SuccessState) context.push('/success');
})

// Both → BlocConsumer
BlocConsumer<Bloc, State>(listener: ..., builder: ...)
```

**Детали:** См. `references/bloc_patterns.md`

### Navigation

```dart
context.push('/path/$id');           // Add to stack
context.go('/home');                 // Replace stack
context.pop();                       // Go back
context.push('/path', extra: data);  // Pass data
```

### Forms

```dart
class _FormScreenState extends State<FormScreen> {
  final _formKey = GlobalKey<FormState>();
  final _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _submit() {
    if (_formKey.currentState!.validate()) {
      context.read<Bloc>().add(SubmitEvent(_controller.text));
    }
  }
}
```

### DI Registration

```dart
// di/feature_injection.dart
gh.factory<PaymentRemoteDataSource>(() => PaymentRemoteDataSourceImpl(gh()));
gh.lazySingleton<PaymentRepository>(() => PaymentRepositoryImpl(gh()));
gh.lazySingleton<GetPaymentUseCase>(() => GetPaymentUseCase(gh()));
gh.factory<PaymentBloc>(() => PaymentBloc(gh()));
```

---

## Integration with figma-integration

| Skill | Фокус | Результат |
|-------|-------|-----------|
| **figma-integration** | Pixel-perfect UI | Только presentation (виджеты) |
| **screen** | Clean Architecture | Domain + Data + Presentation |

**Совместный workflow:**
1. `figma-integration` → pixel-perfect виджеты с комментариями
2. `screen` → рефакторинг в Clean Architecture (сохраняя комментарии)

---

## Common Mistakes

| Ошибка | Решение |
|--------|---------|
| `fontSize: 16` | `fontSize: 16.sp` |
| `Color(0xFFFFCD00)` | `colors.primary` |
| `Text('Payments')` | `Text(context.l10n.payments)` |
| `Widget _buildContent()` | Inline или Widget class |
| `void _onTap() { bloc.add(...) }` | Inline: `onTap: () => bloc.add(...)` |
| `AppColors.primary` | `AppColors.current.primary` |
| `const TextStyle(color: colors.*)` | Убрать `const` |
| `BorderRadius.circular()` для bottom sheet | `BorderRadius.only(top*)` |
| `ServerFailure` | `Failure.fromException(e)` |
| `return SizedBox.shrink()` в builder | Fallback на error state |
| `if` без `else if` в BlocBuilder | Использовать `else if` для states |
| Нет fallback в конце условий | Всегда `else` или финальный `return` с подходящим state |

---

## Reference Files

- **`references/rules_quick_ref.md`** - Детали всех 13 правил с bash-командами
- **`references/architecture.md`** - Clean Architecture patterns
- **`references/design_system.md`** - Colors, TextStyles, компоненты
- **`references/bloc_patterns.md`** - Примеры BLoC из проекта
- **`references/localization.md`** - ARB файлы, placeholders, keys
- **`references/icons_guide.md`** - BeelineIcons, SVG colors

---

🚀 **Ready to generate screens for Beeline v4!**
