---
name: feature-structure
description: Feature-first folder organization for Flutter projects. Use when creating new features, reorganizing code, or when user asks about "folder structure", "feature modules", or "project organization".
---

# Feature Structure

## Overview

Feature-first organization groups code by business feature rather than technical layer. Each feature is a self-contained module with its own domain, data, and presentation layers.

## Mandatory Structure

### Root Project Layout

```
lib/
├── app/                            # App configuration
│   ├── app.dart                    # MaterialApp setup
│   ├── router.dart                 # GoRouter configuration
│   └── theme.dart                  # ThemeData
│
├── core/                           # Shared utilities
│   ├── constants/
│   │   ├── api_constants.dart
│   │   └── app_constants.dart
│   ├── error/
│   │   ├── exceptions.dart
│   │   └── failures.dart
│   ├── network/
│   │   ├── api_client.dart
│   │   ├── interceptors/
│   │   │   ├── auth_interceptor.dart
│   │   │   └── logging_interceptor.dart
│   │   └── network_info.dart
│   ├── usecases/
│   │   └── usecase.dart
│   ├── utils/
│   │   ├── extensions/
│   │   │   ├── context_extensions.dart
│   │   │   └── string_extensions.dart
│   │   └── helpers/
│   │       └── date_helper.dart
│   └── widgets/                    # Shared widgets
│       ├── loading_widget.dart
│       └── error_widget.dart
│
├── features/                       # Feature modules
│   ├── auth/
│   ├── home/
│   ├── profile/
│   └── settings/
│
├── injection_container.dart        # GetIt setup
└── main.dart                       # Entry point
```

### Feature Module Layout

```
features/
└── auth/
    ├── domain/
    │   ├── entities/
    │   │   └── user.dart
    │   ├── repositories/
    │   │   └── auth_repository.dart
    │   └── usecases/
    │       ├── login_user.dart
    │       ├── register_user.dart
    │       ├── logout_user.dart
    │       └── get_current_user.dart
    │
    ├── data/
    │   ├── models/
    │   │   └── user_model.dart
    │   ├── datasources/
    │   │   ├── auth_remote_datasource.dart
    │   │   └── auth_local_datasource.dart
    │   └── repositories/
    │       └── auth_repository_impl.dart
    │
    └── presentation/
        ├── bloc/
        │   ├── auth_bloc.dart
        │   ├── auth_event.dart
        │   └── auth_state.dart
        ├── pages/
        │   ├── login_page.dart
        │   ├── register_page.dart
        │   └── forgot_password_page.dart
        └── widgets/
            ├── login_form.dart
            ├── register_form.dart
            └── social_login_buttons.dart
```

## Naming Conventions

### Files

```
# Use snake_case for file names
user_model.dart          ✅
UserModel.dart           ❌

# Suffix by type
login_page.dart          # Page
login_form.dart          # Widget
auth_bloc.dart           # BLoC
auth_repository.dart     # Repository
user_model.dart          # Model
user.dart                # Entity
login_user.dart          # UseCase
```

### Classes

```dart
// Entities: Simple name
class User {}

// Models: Name + Model suffix
class UserModel {}

// Use Cases: Verb + Noun
class LoginUser {}
class GetCurrentUser {}
class UpdateUserProfile {}

// Repositories: Name + Repository
abstract class AuthRepository {}
class AuthRepositoryImpl implements AuthRepository {}

// Data Sources: Name + DataSource
abstract class AuthRemoteDataSource {}
class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {}

// BLoC: Feature + Bloc
class AuthBloc {}

// Events: Feature + Event + Action
class LoginRequested extends AuthEvent {}
class LogoutRequested extends AuthEvent {}

// States: Feature + State (sealed class pattern)
sealed class AuthState {}
class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthAuthenticated extends AuthState {}
class AuthFailure extends AuthState {}

// Pages: Feature/Action + Page
class LoginPage extends StatelessWidget {}
class ProfilePage extends StatelessWidget {}
```

## Creating a New Feature

### Step 1: Create Directory Structure

```bash
mkdir -p lib/features/orders/{domain/{entities,repositories,usecases},data/{models,datasources,repositories},presentation/{bloc,pages,widgets}}
```

### Step 2: Create Domain Layer

```dart
// 1. Entity
// lib/features/orders/domain/entities/order.dart
class Order extends Equatable {
  final String id;
  final List<OrderItem> items;
  final double total;
  final OrderStatus status;
  final DateTime createdAt;

  const Order({
    required this.id,
    required this.items,
    required this.total,
    required this.status,
    required this.createdAt,
  });

  @override
  List<Object?> get props => [id, items, total, status, createdAt];
}

// 2. Repository Interface
// lib/features/orders/domain/repositories/order_repository.dart
abstract class OrderRepository {
  Future<Either<Failure, List<Order>>> getOrders();
  Future<Either<Failure, Order>> getOrderById(String id);
  Future<Either<Failure, Order>> createOrder(CreateOrderParams params);
  Future<Either<Failure, void>> cancelOrder(String id);
}

// 3. Use Cases
// lib/features/orders/domain/usecases/get_orders.dart
class GetOrders implements UseCase<List<Order>, NoParams> {
  final OrderRepository repository;
  GetOrders(this.repository);

  @override
  Future<Either<Failure, List<Order>>> call(NoParams params) {
    return repository.getOrders();
  }
}
```

### Step 3: Create Data Layer

```dart
// 1. Model
// lib/features/orders/data/models/order_model.dart
@freezed
class OrderModel with _$OrderModel {
  const OrderModel._();

  const factory OrderModel({
    required String id,
    required List<OrderItemModel> items,
    required double total,
    required String status,
    @JsonKey(name: 'created_at') required DateTime createdAt,
  }) = _OrderModel;

  factory OrderModel.fromJson(Map<String, dynamic> json) =>
      _$OrderModelFromJson(json);

  Order toEntity() => Order(
    id: id,
    items: items.map((i) => i.toEntity()).toList(),
    total: total,
    status: OrderStatus.values.byName(status),
    createdAt: createdAt,
  );
}

// 2. Data Source
// lib/features/orders/data/datasources/order_remote_datasource.dart
abstract class OrderRemoteDataSource {
  Future<List<OrderModel>> getOrders();
  Future<OrderModel> getOrderById(String id);
  Future<OrderModel> createOrder(Map<String, dynamic> data);
  Future<void> cancelOrder(String id);
}

class OrderRemoteDataSourceImpl implements OrderRemoteDataSource {
  final Dio client;
  OrderRemoteDataSourceImpl({required this.client});

  @override
  Future<List<OrderModel>> getOrders() async {
    final response = await client.get('/orders');
    return (response.data['orders'] as List)
        .map((json) => OrderModel.fromJson(json))
        .toList();
  }
  // ... other methods
}

// 3. Repository Implementation
// lib/features/orders/data/repositories/order_repository_impl.dart
class OrderRepositoryImpl implements OrderRepository {
  final OrderRemoteDataSource remoteDataSource;
  final NetworkInfo networkInfo;

  OrderRepositoryImpl({
    required this.remoteDataSource,
    required this.networkInfo,
  });

  @override
  Future<Either<Failure, List<Order>>> getOrders() async {
    if (await networkInfo.isConnected) {
      try {
        final models = await remoteDataSource.getOrders();
        return Right(models.map((m) => m.toEntity()).toList());
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    }
    return const Left(NetworkFailure('No internet connection'));
  }
  // ... other methods
}
```

### Step 4: Create Presentation Layer

```dart
// 1. BLoC Events
// lib/features/orders/presentation/bloc/orders_event.dart
sealed class OrdersEvent {}
class LoadOrders extends OrdersEvent {}
class RefreshOrders extends OrdersEvent {}
class CancelOrder extends OrdersEvent {
  final String orderId;
  CancelOrder(this.orderId);
}

// 2. BLoC States
// lib/features/orders/presentation/bloc/orders_state.dart
sealed class OrdersState {}
class OrdersInitial extends OrdersState {}
class OrdersLoading extends OrdersState {}
class OrdersLoaded extends OrdersState {
  final List<Order> orders;
  OrdersLoaded(this.orders);
}
class OrdersError extends OrdersState {
  final String message;
  OrdersError(this.message);
}

// 3. BLoC
// lib/features/orders/presentation/bloc/orders_bloc.dart
class OrdersBloc extends Bloc<OrdersEvent, OrdersState> {
  final GetOrders getOrders;
  final CancelOrderUseCase cancelOrder;

  OrdersBloc({
    required this.getOrders,
    required this.cancelOrder,
  }) : super(OrdersInitial()) {
    on<LoadOrders>(_onLoadOrders);
    on<CancelOrder>(_onCancelOrder);
  }

  Future<void> _onLoadOrders(
    LoadOrders event,
    Emitter<OrdersState> emit,
  ) async {
    emit(OrdersLoading());
    final result = await getOrders(NoParams());
    result.fold(
      (failure) => emit(OrdersError(failure.message)),
      (orders) => emit(OrdersLoaded(orders)),
    );
  }
  // ... other handlers
}

// 4. Page
// lib/features/orders/presentation/pages/orders_page.dart
class OrdersPage extends StatelessWidget {
  const OrdersPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Orders')),
      body: BlocBuilder<OrdersBloc, OrdersState>(
        builder: (context, state) => switch (state) {
          OrdersInitial() => const SizedBox(),
          OrdersLoading() => const LoadingWidget(),
          OrdersLoaded(:final orders) => OrdersList(orders: orders),
          OrdersError(:final message) => ErrorWidget(message: message),
        },
      ),
    );
  }
}
```

### Step 5: Register Dependencies

```dart
// lib/injection_container.dart
void _initOrders() {
  // BLoC
  sl.registerFactory(
    () => OrdersBloc(getOrders: sl(), cancelOrder: sl()),
  );

  // Use Cases
  sl.registerLazySingleton(() => GetOrders(sl()));
  sl.registerLazySingleton(() => CancelOrderUseCase(sl()));

  // Repository
  sl.registerLazySingleton<OrderRepository>(
    () => OrderRepositoryImpl(
      remoteDataSource: sl(),
      networkInfo: sl(),
    ),
  );

  // Data Source
  sl.registerLazySingleton<OrderRemoteDataSource>(
    () => OrderRemoteDataSourceImpl(client: sl()),
  );
}
```

## Feature Communication

### Cross-Feature Navigation

```dart
// Use GoRouter for navigation between features
context.go('/orders/${order.id}');
context.push('/profile');
```

### Shared State

```dart
// For shared state, create a separate feature or use core
// lib/core/auth/auth_state_provider.dart
class AuthStateProvider {
  final GetCurrentUser getCurrentUser;
  // Provides auth state to multiple features
}
```

### Shared Widgets

```dart
// Place truly shared widgets in core
// lib/core/widgets/avatar_widget.dart
class AvatarWidget extends StatelessWidget {
  final String? imageUrl;
  final String name;
  // Used across multiple features
}
```

## Anti-Patterns

### ❌ Feature Depending on Another Feature's Data Layer

```dart
// BAD: Orders feature imports auth's data layer
import 'package:app/features/auth/data/models/user_model.dart';
```

### ✅ Depend Only on Domain

```dart
// GOOD: Orders feature imports auth's domain layer
import 'package:app/features/auth/domain/entities/user.dart';
```

### ❌ God Features

```dart
// BAD: One feature doing everything
features/
└── main/
    └── (500+ files)
```

### ✅ Small, Focused Features

```dart
// GOOD: Split by business domain
features/
├── auth/
├── orders/
├── products/
├── cart/
└── profile/
```

## References

- See [references/conventions.md](references/conventions.md) for naming conventions
- See `clean-architecture` skill for layer details
- See `dependency-injection` skill for DI setup
