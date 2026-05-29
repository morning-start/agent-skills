---
description: Scaffold a new clean architecture feature with domain, data, and presentation layers
argument-hint: <feature-name>
allowed-tools: Bash, Write, Read
---

# /generate-feature Command

Generate a complete clean architecture feature structure.

## Instructions

When the user runs `/generate-feature <feature-name>`:

1. **Validate Input**
   - Feature name should be snake_case (e.g., `user_profile`, `order_history`)
   - Convert to snake_case if needed

2. **Create Directory Structure**

```bash
mkdir -p lib/features/<feature_name>/domain/{entities,repositories,usecases}
mkdir -p lib/features/<feature_name>/data/{models,datasources,repositories}
mkdir -p lib/features/<feature_name>/presentation/{bloc,pages,widgets}
```

3. **Generate Domain Layer Files**

Create entity (lib/features/<feature_name>/domain/entities/<feature_name>.dart):
```dart
import 'package:equatable/equatable.dart';

class <FeatureName> extends Equatable {
  final String id;
  // Add properties based on feature

  const <FeatureName>({
    required this.id,
  });

  @override
  List<Object?> get props => [id];
}
```

Create repository interface (lib/features/<feature_name>/domain/repositories/<feature_name>_repository.dart):
```dart
import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/<feature_name>.dart';

abstract class <FeatureName>Repository {
  Future<Either<Failure, List<<FeatureName>>>> getAll();
  Future<Either<Failure, <FeatureName>>> getById(String id);
  Future<Either<Failure, <FeatureName>>> create(<FeatureName> item);
  Future<Either<Failure, <FeatureName>>> update(<FeatureName> item);
  Future<Either<Failure, void>> delete(String id);
}
```

Create use case (lib/features/<feature_name>/domain/usecases/get_<feature_name>s.dart):
```dart
import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/<feature_name>.dart';
import '../repositories/<feature_name>_repository.dart';

class Get<FeatureName>s implements UseCase<List<<FeatureName>>, NoParams> {
  final <FeatureName>Repository repository;

  Get<FeatureName>s(this.repository);

  @override
  Future<Either<Failure, List<<FeatureName>>>> call(NoParams params) {
    return repository.getAll();
  }
}
```

4. **Generate Data Layer Files**

Create model (lib/features/<feature_name>/data/models/<feature_name>_model.dart):
```dart
import 'package:freezed_annotation/freezed_annotation.dart';
import '../../domain/entities/<feature_name>.dart';

part '<feature_name>_model.freezed.dart';
part '<feature_name>_model.g.dart';

@freezed
class <FeatureName>Model with _$<FeatureName>Model {
  const <FeatureName>Model._();

  const factory <FeatureName>Model({
    required String id,
    // Add fields matching entity
  }) = _<FeatureName>Model;

  factory <FeatureName>Model.fromJson(Map<String, dynamic> json) =>
      _$<FeatureName>ModelFromJson(json);

  <FeatureName> toEntity() => <FeatureName>(
    id: id,
  );

  factory <FeatureName>Model.fromEntity(<FeatureName> entity) =>
      <FeatureName>Model(
        id: entity.id,
      );
}
```

Create remote data source (lib/features/<feature_name>/data/datasources/<feature_name>_remote_datasource.dart):
```dart
import 'package:dio/dio.dart';
import '../../../../core/error/exceptions.dart';
import '../models/<feature_name>_model.dart';

abstract class <FeatureName>RemoteDataSource {
  Future<List<<FeatureName>Model>> getAll();
  Future<<FeatureName>Model> getById(String id);
  Future<<FeatureName>Model> create(Map<String, dynamic> data);
  Future<<FeatureName>Model> update(String id, Map<String, dynamic> data);
  Future<void> delete(String id);
}

class <FeatureName>RemoteDataSourceImpl implements <FeatureName>RemoteDataSource {
  final Dio client;

  <FeatureName>RemoteDataSourceImpl({required this.client});

  @override
  Future<List<<FeatureName>Model>> getAll() async {
    try {
      final response = await client.get('/<feature_name>s');
      return (response.data as List)
          .map((json) => <FeatureName>Model.fromJson(json))
          .toList();
    } on DioException catch (e) {
      throw ServerException(message: e.message ?? 'Server error');
    }
  }

  @override
  Future<<FeatureName>Model> getById(String id) async {
    try {
      final response = await client.get('/<feature_name>s/$id');
      return <FeatureName>Model.fromJson(response.data);
    } on DioException catch (e) {
      throw ServerException(message: e.message ?? 'Server error');
    }
  }

  @override
  Future<<FeatureName>Model> create(Map<String, dynamic> data) async {
    try {
      final response = await client.post('/<feature_name>s', data: data);
      return <FeatureName>Model.fromJson(response.data);
    } on DioException catch (e) {
      throw ServerException(message: e.message ?? 'Server error');
    }
  }

  @override
  Future<<FeatureName>Model> update(String id, Map<String, dynamic> data) async {
    try {
      final response = await client.put('/<feature_name>s/$id', data: data);
      return <FeatureName>Model.fromJson(response.data);
    } on DioException catch (e) {
      throw ServerException(message: e.message ?? 'Server error');
    }
  }

  @override
  Future<void> delete(String id) async {
    try {
      await client.delete('/<feature_name>s/$id');
    } on DioException catch (e) {
      throw ServerException(message: e.message ?? 'Server error');
    }
  }
}
```

Create repository implementation (lib/features/<feature_name>/data/repositories/<feature_name>_repository_impl.dart):
```dart
import 'package:dartz/dartz.dart';
import '../../../../core/error/exceptions.dart';
import '../../../../core/error/failures.dart';
import '../../../../core/network/network_info.dart';
import '../../domain/entities/<feature_name>.dart';
import '../../domain/repositories/<feature_name>_repository.dart';
import '../datasources/<feature_name>_remote_datasource.dart';

class <FeatureName>RepositoryImpl implements <FeatureName>Repository {
  final <FeatureName>RemoteDataSource remoteDataSource;
  final NetworkInfo networkInfo;

  <FeatureName>RepositoryImpl({
    required this.remoteDataSource,
    required this.networkInfo,
  });

  @override
  Future<Either<Failure, List<<FeatureName>>>> getAll() async {
    if (await networkInfo.isConnected) {
      try {
        final models = await remoteDataSource.getAll();
        return Right(models.map((m) => m.toEntity()).toList());
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    }
    return const Left(NetworkFailure('No internet connection'));
  }

  @override
  Future<Either<Failure, <FeatureName>>> getById(String id) async {
    if (await networkInfo.isConnected) {
      try {
        final model = await remoteDataSource.getById(id);
        return Right(model.toEntity());
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    }
    return const Left(NetworkFailure('No internet connection'));
  }

  @override
  Future<Either<Failure, <FeatureName>>> create(<FeatureName> item) async {
    if (await networkInfo.isConnected) {
      try {
        final model = await remoteDataSource.create({
          'id': item.id,
          // Add other fields
        });
        return Right(model.toEntity());
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    }
    return const Left(NetworkFailure('No internet connection'));
  }

  @override
  Future<Either<Failure, <FeatureName>>> update(<FeatureName> item) async {
    if (await networkInfo.isConnected) {
      try {
        final model = await remoteDataSource.update(item.id, {
          // Add fields to update
        });
        return Right(model.toEntity());
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    }
    return const Left(NetworkFailure('No internet connection'));
  }

  @override
  Future<Either<Failure, void>> delete(String id) async {
    if (await networkInfo.isConnected) {
      try {
        await remoteDataSource.delete(id);
        return const Right(null);
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    }
    return const Left(NetworkFailure('No internet connection'));
  }
}
```

5. **Generate Presentation Layer Files**

Create BLoC event (lib/features/<feature_name>/presentation/bloc/<feature_name>_event.dart):
```dart
part of '<feature_name>_bloc.dart';

sealed class <FeatureName>Event {}

class Load<FeatureName>s extends <FeatureName>Event {}

class Refresh<FeatureName>s extends <FeatureName>Event {}

class Delete<FeatureName> extends <FeatureName>Event {
  final String id;
  Delete<FeatureName>(this.id);
}
```

Create BLoC state (lib/features/<feature_name>/presentation/bloc/<feature_name>_state.dart):
```dart
part of '<feature_name>_bloc.dart';

sealed class <FeatureName>State {}

class <FeatureName>Initial extends <FeatureName>State {}

class <FeatureName>Loading extends <FeatureName>State {}

class <FeatureName>Loaded extends <FeatureName>State {
  final List<<FeatureName>> items;
  <FeatureName>Loaded(this.items);
}

class <FeatureName>Error extends <FeatureName>State {
  final String message;
  <FeatureName>Error(this.message);
}
```

Create BLoC (lib/features/<feature_name>/presentation/bloc/<feature_name>_bloc.dart):
```dart
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/usecases/usecase.dart';
import '../../domain/entities/<feature_name>.dart';
import '../../domain/usecases/get_<feature_name>s.dart';

part '<feature_name>_event.dart';
part '<feature_name>_state.dart';

class <FeatureName>Bloc extends Bloc<<FeatureName>Event, <FeatureName>State> {
  final Get<FeatureName>s get<FeatureName>s;

  <FeatureName>Bloc({
    required this.get<FeatureName>s,
  }) : super(<FeatureName>Initial()) {
    on<Load<FeatureName>s>(_onLoad<FeatureName>s);
    on<Refresh<FeatureName>s>(_onRefresh<FeatureName>s);
  }

  Future<void> _onLoad<FeatureName>s(
    Load<FeatureName>s event,
    Emitter<<FeatureName>State> emit,
  ) async {
    emit(<FeatureName>Loading());
    final result = await get<FeatureName>s(NoParams());
    result.fold(
      (failure) => emit(<FeatureName>Error(failure.message)),
      (items) => emit(<FeatureName>Loaded(items)),
    );
  }

  Future<void> _onRefresh<FeatureName>s(
    Refresh<FeatureName>s event,
    Emitter<<FeatureName>State> emit,
  ) async {
    final result = await get<FeatureName>s(NoParams());
    result.fold(
      (failure) => emit(<FeatureName>Error(failure.message)),
      (items) => emit(<FeatureName>Loaded(items)),
    );
  }
}
```

Create page (lib/features/<feature_name>/presentation/pages/<feature_name>_page.dart):
```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/<feature_name>_bloc.dart';

class <FeatureName>Page extends StatelessWidget {
  const <FeatureName>Page({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('<Feature Name>'),
      ),
      body: BlocBuilder<<FeatureName>Bloc, <FeatureName>State>(
        builder: (context, state) => switch (state) {
          <FeatureName>Initial() => const SizedBox(),
          <FeatureName>Loading() => const Center(
              child: CircularProgressIndicator(),
            ),
          <FeatureName>Loaded(:final items) => ListView.builder(
              itemCount: items.length,
              itemBuilder: (context, index) {
                final item = items[index];
                return ListTile(
                  title: Text(item.id),
                  // Customize display
                );
              },
            ),
          <FeatureName>Error(:final message) => Center(
              child: Text(message),
            ),
        },
      ),
    );
  }
}
```

6. **Create Test Files**

Create use case test (test/features/<feature_name>/domain/usecases/get_<feature_name>s_test.dart):
```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dartz/dartz.dart';

// Import necessary files

class Mock<FeatureName>Repository extends Mock implements <FeatureName>Repository {}

void main() {
  late Get<FeatureName>s usecase;
  late Mock<FeatureName>Repository mockRepository;

  setUp(() {
    mockRepository = Mock<FeatureName>Repository();
    usecase = Get<FeatureName>s(mockRepository);
  });

  test('should get list of <feature_name>s from repository', () async {
    // Arrange
    final tItems = [<FeatureName>(id: '1')];
    when(() => mockRepository.getAll())
        .thenAnswer((_) async => Right(tItems));

    // Act
    final result = await usecase(NoParams());

    // Assert
    expect(result, Right(tItems));
    verify(() => mockRepository.getAll()).called(1);
  });
}
```

7. **Output Summary**

After generation, output:
```
Feature '<feature_name>' created successfully!

Structure:
lib/features/<feature_name>/
├── domain/
│   ├── entities/<feature_name>.dart
│   ├── repositories/<feature_name>_repository.dart
│   └── usecases/get_<feature_name>s.dart
├── data/
│   ├── models/<feature_name>_model.dart
│   ├── datasources/<feature_name>_remote_datasource.dart
│   └── repositories/<feature_name>_repository_impl.dart
└── presentation/
    ├── bloc/
    │   ├── <feature_name>_bloc.dart
    │   ├── <feature_name>_event.dart
    │   └── <feature_name>_state.dart
    └── pages/<feature_name>_page.dart

Next steps:
1. Run 'dart run build_runner build' for code generation
2. Add dependency injection in injection_container.dart
3. Add routing in router.dart
4. Customize entity properties and model fields
```

## Naming Convention

- Input: `userProfile` or `user_profile` or `UserProfile`
- Directory: `user_profile`
- Class: `UserProfile`
- File: `user_profile.dart`
