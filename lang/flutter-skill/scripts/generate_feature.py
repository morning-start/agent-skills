#!/usr/bin/env python3
"""
Generate Flutter Feature Script

This script generates a complete Clean Architecture feature structure with domain, data, and presentation layers.

Usage:
    python generate_feature.py --feature-name <feature_name>
    python generate_feature.py -n <feature_name>

Example:
    python generate_feature.py --feature-name auth
    python generate_feature.py -n user_profile
"""

import argparse
import os
import sys
from pathlib import Path


def to_pascal_case(snake_str: str) -> str:
    """Convert snake_case to PascalCase."""
    return ''.join(x.capitalize() for x in snake_str.lower().split('_'))


def to_camel_case(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    components = snake_str.lower().split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])


def generate_entity(feature_name: str) -> str:
    """Generate domain entity file content."""
    pascal_name = to_pascal_case(feature_name)
    return f'''import 'package:equatable/equatable.dart';

class {pascal_name} extends Equatable {{
  final String id;

  const {pascal_name}({{required this.id}});

  @override
  List<Object?> get props => [id];

  {pascal_name} copyWith({{String? id}}) {{
    return {pascal_name}(id: id ?? this.id);
  }}
}}
'''


def generate_repository_interface(feature_name: str) -> str:
    """Generate repository interface file content."""
    pascal_name = to_pascal_case(feature_name)
    camel_name = to_camel_case(feature_name)
    return f'''import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/{feature_name}.dart';

abstract class {pascal_name}Repository {{
  Future<Either<Failure, List<{pascal_name}>>> getAll();
  Future<Either<Failure, {pascal_name}>> getById(String id);
  Future<Either<Failure, {pascal_name}>> create({pascal_name} item);
  Future<Either<Failure, {pascal_name}>> update({pascal_name} item);
  Future<Either<Failure, void>> delete(String id);
}}
'''


def generate_usecase(feature_name: str) -> str:
    """Generate use case file content."""
    pascal_name = to_pascal_case(feature_name)
    camel_name = to_camel_case(feature_name)
    return f'''import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/{feature_name}.dart';
import '../repositories/{feature_name}_repository.dart';

class Get{pascal_name}s implements UseCase<List<{pascal_name}>, NoParams> {{
  final {pascal_name}Repository repository;

  Get{pascal_name}s(this.repository);

  @override
  Future<Either<Failure, List<{pascal_name}>>> call(NoParams params) {{
    return repository.getAll();
  }}
}}

class Get{pascal_name}ById implements UseCase<{pascal_name}, String> {{
  final {pascal_name}Repository repository;

  Get{pascal_name}ById(this.repository);

  @override
  Future<Either<Failure, {pascal_name}>> call(String id) {{
    return repository.getById(id);
  }}
}}
'''


def generate_model(feature_name: str) -> str:
    """Generate data model file content."""
    pascal_name = to_pascal_case(feature_name)
    return f'''import 'package:freezed_annotation/freezed_annotation.dart';
import '../../domain/entities/{feature_name}.dart';

part '{feature_name}_model.freezed.dart';
part '{feature_name}_model.g.dart';

@freezed
class {pascal_name}Model with _${{pascal_name}}Model {{
  const {pascal_name}Model._();

  const factory {pascal_name}Model({{
    required String id,
  }}) = _{pascal_name}Model;

  factory {pascal_name}Model.fromJson(Map<String, dynamic> json) =>
      _${{pascal_name}}ModelFromJson(json);

  {pascal_name} toEntity() => {pascal_name}(id: id);

  factory {pascal_name}Model.fromEntity({pascal_name} entity) =>
      {pascal_name}Model(id: entity.id);
}}
'''


def generate_remote_datasource(feature_name: str) -> str:
    """Generate remote datasource file content."""
    pascal_name = to_pascal_case(feature_name)
    return f'''import 'package:dio/dio.dart';
import '../../../../core/error/exceptions.dart';
import '../models/{feature_name}_model.dart';

abstract class {pascal_name}RemoteDataSource {{
  Future<List<{pascal_name}Model>> getAll();
  Future<{pascal_name}Model> getById(String id);
  Future<{pascal_name}Model> create(Map<String, dynamic> data);
  Future<{pascal_name}Model> update(String id, Map<String, dynamic> data);
  Future<void> delete(String id);
}}

class {pascal_name}RemoteDataSourceImpl implements {pascal_name}RemoteDataSource {{
  final Dio client;

  {pascal_name}RemoteDataSourceImpl({{required this.client}});

  @override
  Future<List<{pascal_name}Model>> getAll() async {{
    try {{
      final response = await client.get('/{feature_name}s');
      return (response.data as List)
          .map((json) => {pascal_name}Model.fromJson(json))
          .toList();
    }} on DioException catch (e) {{
      throw ServerException(message: e.message ?? 'Server error');
    }}
  }}

  @override
  Future<{pascal_name}Model> getById(String id) async {{
    try {{
      final response = await client.get('/{feature_name}s/$id');
      return {pascal_name}Model.fromJson(response.data);
    }} on DioException catch (e) {{
      throw ServerException(message: e.message ?? 'Server error');
    }}
  }}

  @override
  Future<{pascal_name}Model> create(Map<String, dynamic> data) async {{
    try {{
      final response = await client.post('/{feature_name}s', data: data);
      return {pascal_name}Model.fromJson(response.data);
    }} on DioException catch (e) {{
      throw ServerException(message: e.message ?? 'Server error');
    }}
  }}

  @override
  Future<{pascal_name}Model> update(String id, Map<String, dynamic> data) async {{
    try {{
      final response = await client.put('/{feature_name}s/$id', data: data);
      return {pascal_name}Model.fromJson(response.data);
    }} on DioException catch (e) {{
      throw ServerException(message: e.message ?? 'Server error');
    }}
  }}

  @override
  Future<void> delete(String id) async {{
    try {{
      await client.delete('/{feature_name}s/$id');
    }} on DioException catch (e) {{
      throw ServerException(message: e.message ?? 'Server error');
    }}
  }}
}}
'''


def generate_repository_implementation(feature_name: str) -> str:
    """Generate repository implementation file content."""
    pascal_name = to_pascal_case(feature_name)
    return f'''import 'package:dartz/dartz.dart';
import '../../../../core/error/exceptions.dart';
import '../../../../core/error/failures.dart';
import '../../../../core/network/network_info.dart';
import '../../domain/entities/{feature_name}.dart';
import '../../domain/repositories/{feature_name}_repository.dart';
import '../datasources/{feature_name}_remote_datasource.dart';
import '../models/{feature_name}_model.dart';

class {pascal_name}RepositoryImpl implements {pascal_name}Repository {{
  final {pascal_name}RemoteDataSource remoteDataSource;
  final NetworkInfo networkInfo;

  {pascal_name}RepositoryImpl({{
    required this.remoteDataSource,
    required this.networkInfo,
  }});

  @override
  Future<Either<Failure, List<{pascal_name}>>> getAll() async {{
    if (await networkInfo.isConnected) {{
      try {{
        final remoteModels = await remoteDataSource.getAll();
        return Right(remoteModels.map((model) => model.toEntity()).toList());
      }} on ServerException catch (e) {{
        return Left(ServerFailure(e.message));
      }}
    }} else {{
      return const Left(NetworkFailure('No internet connection'));
    }}
  }}

  @override
  Future<Either<Failure, {pascal_name}>> getById(String id) async {{
    if (await networkInfo.isConnected) {{
      try {{
        final remoteModel = await remoteDataSource.getById(id);
        return Right(remoteModel.toEntity());
      }} on ServerException catch (e) {{
        return Left(ServerFailure(e.message));
      }}
    }} else {{
      return const Left(NetworkFailure('No internet connection'));
    }}
  }}

  @override
  Future<Either<Failure, {pascal_name}>> create({pascal_name} item) async {{
    if (await networkInfo.isConnected) {{
      try {{
        final model = {pascal_name}Model.fromEntity(item);
        final remoteModel = await remoteDataSource.create(model.toJson());
        return Right(remoteModel.toEntity());
      }} on ServerException catch (e) {{
        return Left(ServerFailure(e.message));
      }}
    }} else {{
      return const Left(NetworkFailure('No internet connection'));
    }}
  }}

  @override
  Future<Either<Failure, {pascal_name}>> update({pascal_name} item) async {{
    if (await networkInfo.isConnected) {{
      try {{
        final model = {pascal_name}Model.fromEntity(item);
        final remoteModel = await remoteDataSource.update(item.id, model.toJson());
        return Right(remoteModel.toEntity());
      }} on ServerException catch (e) {{
        return Left(ServerFailure(e.message));
      }}
    }} else {{
      return const Left(NetworkFailure('No internet connection'));
    }}
  }}

  @override
  Future<Either<Failure, void>> delete(String id) async {{
    if (await networkInfo.isConnected) {{
      try {{
        await remoteDataSource.delete(id);
        return const Right(null);
      }} on ServerException catch (e) {{
        return Left(ServerFailure(e.message));
      }}
    }} else {{
      return const Left(NetworkFailure('No internet connection'));
    }}
  }}
}}
'''


def generate_bloc_event(feature_name: str) -> str:
    """Generate BLoC event file content."""
    pascal_name = to_pascal_case(feature_name)
    camel_name = to_camel_case(feature_name)
    return f'''part of '{feature_name}_bloc.dart';

sealed class {pascal_name}Event {{}}

class Load{pascal_name}s extends {pascal_name}Event {{}}

class Get{pascal_name}ById extends {pascal_name}Event {{
  final String id;
  Get{pascal_name}ById(this.id);
}}

class Add{pascal_name} extends {pascal_name}Event {{
  final {pascal_name} {camel_name};
  Add{pascal_name}(this.{camel_name});
}}

class Update{pascal_name} extends {pascal_name}Event {{
  final {pascal_name} {camel_name};
  Update{pascal_name}(this.{camel_name});
}}

class Delete{pascal_name} extends {pascal_name}Event {{
  final String id;
  Delete{pascal_name}(this.id);
}}
'''


def generate_bloc_state(feature_name: str) -> str:
    """Generate BLoC state file content."""
    pascal_name = to_pascal_case(feature_name)
    camel_name = to_camel_case(feature_name)
    return f'''part of '{feature_name}_bloc.dart';

sealed class {pascal_name}State {{}}

class {pascal_name}Initial extends {pascal_name}State {{}}

class {pascal_name}Loading extends {pascal_name}State {{}}

class {pascal_name}sLoaded extends {pascal_name}State {{
  final List<{pascal_name}> {camel_name}s;
  {pascal_name}sLoaded(this.{camel_name}s);
}}

class {pascal_name}Loaded extends {pascal_name}State {{
  final {pascal_name} {camel_name};
  {pascal_name}Loaded(this.{camel_name});
}}

class {pascal_name}Error extends {pascal_name}State {{
  final String message;
  {pascal_name}Error(this.message);
}}
'''


def generate_bloc(feature_name: str) -> str:
    """Generate BLoC file content."""
    pascal_name = to_pascal_case(feature_name)
    camel_name = to_camel_case(feature_name)
    return f'''import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/usecases/get_{feature_name}s.dart';
import '../../domain/usecases/get_{feature_name}_by_id.dart';
import '../../domain/repositories/{feature_name}_repository.dart';
import '../../domain/entities/{feature_name}.dart';

part '{feature_name}_event.dart';
part '{feature_name}_state.dart';

class {pascal_name}Bloc extends Bloc<{pascal_name}Event, {pascal_name}State> {{
  final Get{pascal_name}s get{pascal_name}s;
  final Get{pascal_name}ById get{pascal_name}ById;

  {pascal_name}Bloc({{
    required this.get{pascal_name}s,
    required this.get{pascal_name}ById,
  }}) : super({pascal_name}Initial()) {{
    on<Load{pascal_name}s>(_onLoad{pascal_name}s);
    on<Get{pascal_name}ById>(_onGet{pascal_name}ById);
    on<Add{pascal_name}>(_onAdd{pascal_name});
    on<Update{pascal_name}>(_onUpdate{pascal_name});
    on<Delete{pascal_name}>(_onDelete{pascal_name});
  }}

  Future<void> _onLoad{pascal_name}s(
    Load{pascal_name}s event,
    Emitter<{pascal_name}State> emit,
  ) async {{
    emit({pascal_name}Loading());
    final result = await get{pascal_name}s(NoParams());
    result.fold(
      (failure) => emit({pascal_name}Error(failure.message)),
      ({camel_name}s) => emit({pascal_name}sLoaded({camel_name}s)),
    );
  }}

  Future<void> _onGet{pascal_name}ById(
    Get{pascal_name}ById event,
    Emitter<{pascal_name}State> emit,
  ) async {{
    emit({pascal_name}Loading());
    final result = await get{pascal_name}ById(event.id);
    result.fold(
      (failure) => emit({pascal_name}Error(failure.message)),
      ({camel_name}) => emit({pascal_name}Loaded({camel_name})),
    );
  }}

  Future<void> _onAdd{pascal_name}(
    Add{pascal_name} event,
    Emitter<{pascal_name}State> emit,
  ) async {{
    emit({pascal_name}Loading());
    // TODO: Implement create use case
    emit({pascal_name}Initial());
  }}

  Future<void> _onUpdate{pascal_name}(
    Update{pascal_name} event,
    Emitter<{pascal_name}State> emit,
  ) async {{
    emit({pascal_name}Loading());
    // TODO: Implement update use case
    emit({pascal_name}Initial());
  }}

  Future<void> _onDelete{pascal_name}(
    Delete{pascal_name} event,
    Emitter<{pascal_name}State> emit,
  ) async {{
    emit({pascal_name}Loading());
    // TODO: Implement delete use case
    emit({pascal_name}Initial());
  }}
}}
'''


def generate_page(feature_name: str) -> str:
    """Generate page file content."""
    pascal_name = to_pascal_case(feature_name)
    return f'''import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/{feature_name}_bloc.dart';

class {pascal_name}Page extends StatefulWidget {{
  const {pascal_name}Page({{super.key}});

  @override
  State<{pascal_name}Page> createState() => _{pascal_name}PageState();
}}

class _{pascal_name}PageState extends State<{pascal_name}Page> {{
  @override
  void initState() {{
    super.initState();
    // TODO: Load initial data
    // context.read<{pascal_name}Bloc>().add(Load{pascal_name}s());
  }}

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: Text('{pascal_name}'),
      ),
      body: BlocBuilder<{pascal_name}Bloc, {pascal_name}State>(
        builder: (context, state) {{
          if (state is {pascal_name}Loading) {{
            return const Center(child: CircularProgressIndicator());
          }} else if (state is {pascal_name}Error) {{
            return Center(child: Text('Error: ${{state.message}}'));
          }} else if (state is {pascal_name}sLoaded) {{
            return ListView.builder(
              itemCount: state.{to_camel_case(feature_name)}s.length,
              itemBuilder: (context, index) {{
                final item = state.{to_camel_case(feature_name)}s[index];
                return ListTile(
                  title: Text(item.id),
                  onTap: () {{
                    // TODO: Handle item tap
                  }},
                );
              }},
            );
          }}
          return const Center(child: Text('No data'));
        }},
      ),
    );
  }}
}}
'''


def create_feature_structure(base_path: Path, feature_name: str):
    """Create the complete feature structure."""
    feature_path = base_path / feature_name

    # Create directory structure
    dirs = [
        feature_path / 'domain' / 'entities',
        feature_path / 'domain' / 'repositories',
        feature_path / 'domain' / 'usecases',
        feature_path / 'data' / 'models',
        feature_path / 'data' / 'datasources',
        feature_path / 'data' / 'repositories',
        feature_path / 'presentation' / 'bloc',
        feature_path / 'presentation' / 'pages',
        feature_path / 'presentation' / 'widgets',
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

    # Generate files
    files = [
        (feature_path / 'domain' / 'entities' / f'{feature_name}.dart', generate_entity(feature_name)),
        (feature_path / 'domain' / 'repositories' / f'{feature_name}_repository.dart', generate_repository_interface(feature_name)),
        (feature_path / 'domain' / 'usecases' / f'get_{feature_name}s.dart', generate_usecase(feature_name)),
        (feature_path / 'data' / 'models' / f'{feature_name}_model.dart', generate_model(feature_name)),
        (feature_path / 'data' / 'datasources' / f'{feature_name}_remote_datasource.dart', generate_remote_datasource(feature_name)),
        (feature_path / 'data' / 'repositories' / f'{feature_name}_repository_impl.dart', generate_repository_implementation(feature_name)),
        (feature_path / 'presentation' / 'bloc' / f'{feature_name}_event.dart', generate_bloc_event(feature_name)),
        (feature_path / 'presentation' / 'bloc' / f'{feature_name}_state.dart', generate_bloc_state(feature_name)),
        (feature_path / 'presentation' / 'bloc' / f'{feature_name}_bloc.dart', generate_bloc(feature_name)),
        (feature_path / 'presentation' / 'pages' / f'{feature_name}_page.dart', generate_page(feature_name)),
    ]

    for file_path, content in files:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    return files


def main():
    parser = argparse.ArgumentParser(
        description='Generate a complete Clean Architecture feature structure for Flutter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python generate_feature.py --feature-name auth
  python generate_feature.py -n user_profile
        '''
    )

    parser.add_argument(
        '-n', '--feature-name',
        required=True,
        help='Feature name in snake_case (e.g., auth, user_profile, order_history)'
    )

    parser.add_argument(
        '-o', '--output',
        default='lib/features',
        help='Output directory for the feature (default: lib/features)'
    )

    args = parser.parse_args()

    # Validate feature name
    if not args.feature_name.replace('_', '').isalnum():
        print('Error: Feature name must contain only alphanumeric characters and underscores')
        sys.exit(1)

    # Create feature structure
    base_path = Path(args.output)
    try:
        created_files = create_feature_structure(base_path, args.feature_name)

        print(f'\\n✓ Feature "{args.feature_name}" created successfully!')
        print(f'\\nGenerated files:')
        for file_path, _ in created_files:
            rel_path = file_path.relative_to(Path.cwd())
            print(f'  - {rel_path}')

        print(f'\\nNext steps:')
        print(f'  1. Review and customize the generated code')
        print(f'  2. Add dependencies to pubspec.yaml if needed')
        print(f'  3. Run: dart run build_runner build --delete-conflicting-outputs')

    except Exception as e:
        print(f'Error creating feature: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
