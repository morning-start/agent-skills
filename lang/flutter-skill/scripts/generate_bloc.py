#!/usr/bin/env python3
"""
Generate Flutter BLoC Script

This script generates a complete BLoC with events, states, and test file.

Usage:
    python generate_bloc.py --bloc-name <bloc_name> [--feature <feature_name>]
    python generate_bloc.py -b <bloc_name> -f <feature_name>

Example:
    python generate_bloc.py --bloc-name auth
    python generate_bloc.py -b login -f auth
"""

import argparse
import sys
from pathlib import Path


def to_pascal_case(snake_str: str) -> str:
    """Convert snake_case to PascalCase."""
    return ''.join(x.capitalize() for x in snake_str.lower().split('_'))


def to_camel_case(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    components = snake_str.lower().split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])


def generate_bloc_event(bloc_name: str) -> str:
    """Generate BLoC event file content."""
    pascal_name = to_pascal_case(bloc_name)
    return f'''part of '{bloc_name}_bloc.dart';

/// Base class for all {pascal_name}Bloc events.
sealed class {pascal_name}Event {{}}

/// Event to load initial data.
class Load{pascal_name} extends {pascal_name}Event {{}}

/// Event to refresh data.
class Refresh{pascal_name} extends {pascal_name}Event {{}}

// Add more events as needed:
// class Submit{pascal_name} extends {pascal_name}Event {{
//   final dynamic data;
//   Submit{pascal_name}(this.data);
// }}
'''


def generate_bloc_state(bloc_name: str) -> str:
    """Generate BLoC state file content."""
    pascal_name = to_pascal_case(bloc_name)
    return f'''part of '{bloc_name}_bloc.dart';

/// Base class for all {pascal_name}Bloc states.
sealed class {pascal_name}State {{}}

/// Initial state before any action.
class {pascal_name}Initial extends {pascal_name}State {{}}

/// Loading state while fetching data.
class {pascal_name}Loading extends {pascal_name}State {{}}

/// Success state with loaded data.
class {pascal_name}Success extends {pascal_name}State {{
  final dynamic data; // Replace with actual type
  {pascal_name}Success(this.data);
}}

/// Error state with failure message.
class {pascal_name}Error extends {pascal_name}State {{
  final String message;
  {pascal_name}Error(this.message);
}}
'''


def generate_bloc(bloc_name: str) -> str:
    """Generate BLoC file content."""
    pascal_name = to_pascal_case(bloc_name)
    return f'''import 'package:flutter_bloc/flutter_bloc.dart';
// Import use cases
// import '../../domain/usecases/<usecase>.dart';

part '{bloc_name}_event.dart';
part '{bloc_name}_state.dart';

class {pascal_name}Bloc extends Bloc<{pascal_name}Event, {pascal_name}State> {{
  // final <UseCase> useCase;

  {pascal_name}Bloc({{
    // required this.useCase,
  }}) : super({pascal_name}Initial()) {{
    on<Load{pascal_name}>(_onLoad);
    on<Refresh{pascal_name}>(_onRefresh);
  }}

  Future<void> _onLoad(
    Load{pascal_name} event,
    Emitter<{pascal_name}State> emit,
  ) async {{
    emit({pascal_name}Loading());

    // TODO: Call use case and handle result
    // final result = await useCase(params);
    // result.fold(
    //   (failure) => emit({pascal_name}Error(failure.message)),
    //   (data) => emit({pascal_name}Success(data)),
    // );

    // Placeholder success
    await Future.delayed(const Duration(seconds: 1));
    emit({pascal_name}Success('data'));
  }}

  Future<void> _onRefresh(
    Refresh{pascal_name} event,
    Emitter<{pascal_name}State> emit,
  ) async {{
    // TODO: Implement refresh logic
    // Unlike Load, don't emit Loading to preserve current data
    // final result = await useCase(params);
    // result.fold(
    //   (failure) => emit({pascal_name}Error(failure.message)),
    //   (data) => emit({pascal_name}Success(data)),
    // );
  }}
}}
'''


def generate_bloc_test(bloc_name: str, feature_name: str) -> str:
    """Generate BLoC test file content."""
    pascal_name = to_pascal_case(bloc_name)
    feature_path = f'{feature_name}/' if feature_name else ''

    return f'''import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dartz/dartz.dart';

// Import bloc and dependencies
// import 'package:your_app/features/{feature_path}presentation/bloc/{bloc_name}_bloc.dart';
// import 'package:your_app/features/{feature_path}domain/usecases/<usecase>.dart';

// class Mock<UseCase> extends Mock implements <UseCase> {{}}

void main() {{
  // late {pascal_name}Bloc bloc;
  // late Mock<UseCase> mockUseCase;

  // setUp(() {{
  //   mockUseCase = Mock<UseCase>();
  //   bloc = {pascal_name}Bloc(useCase: mockUseCase);
  // }});

  // tearDown(() {{
  //   bloc.close();
  // }});

  group('{pascal_name}Bloc', () {{
    test('initial state should be {pascal_name}Initial', () {{
      // expect(bloc.state, {pascal_name}Initial());
    }});

    // blocTest<{pascal_name}Bloc, {pascal_name}State>(
    //   'emits [{pascal_name}Loading, {pascal_name}Success] when Load{pascal_name} is added',
    //   build: () {{
    //     when(() => mockUseCase(any()))
    //         .thenAnswer((_) async => const Right('data'));
    //     return bloc;
    //   }},
    //   act: (bloc) => bloc.add(Load{pascal_name}()),
    //   expect: () => [
    //     {pascal_name}Loading(),
    //     {pascal_name}Success('data'),
    //   ],
    // );

    // blocTest<{pascal_name}Bloc, {pascal_name}State>(
    //   'emits [{pascal_name}Loading, {pascal_name}Error] when Load{pascal_name} fails',
    //   build: () {{
    //     when(() => mockUseCase(any()))
    //         .thenAnswer((_) async => Left(ServerFailure('error')));
    //     return bloc;
    //   }},
    //   act: (bloc) => bloc.add(Load{pascal_name}()),
    //   expect: () => [
    //     {pascal_name}Loading(),
    //     {pascal_name}Error('error'),
    //   ],
    // );
  }});
}}
'''


def create_bloc_files(base_path: Path, bloc_name: str, feature_name: str):
    """Create BLoC files and test."""
    # Determine paths
    if feature_name:
        bloc_path = base_path / feature_name / 'presentation' / 'bloc'
        test_path = Path('test') / 'features' / feature_name / 'presentation' / 'bloc'
    else:
        bloc_path = base_path / 'presentation' / 'bloc'
        test_path = Path('test') / 'presentation' / 'bloc'

    # Create directories
    bloc_path.mkdir(parents=True, exist_ok=True)
    test_path.mkdir(parents=True, exist_ok=True)

    # Generate and write files
    files = [
        (bloc_path / f'{bloc_name}_event.dart', generate_bloc_event(bloc_name)),
        (bloc_path / f'{bloc_name}_state.dart', generate_bloc_state(bloc_name)),
        (bloc_path / f'{bloc_name}_bloc.dart', generate_bloc(bloc_name)),
        (test_path / f'{bloc_name}_bloc_test.dart', generate_bloc_test(bloc_name, feature_name)),
    ]

    for file_path, content in files:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    return files


def main():
    parser = argparse.ArgumentParser(
        description='Generate a complete BLoC with events, states, and test file for Flutter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python generate_bloc.py --bloc-name auth
  python generate_bloc.py -b login -f auth
  python generate_bloc.py -b product -f catalog
        '''
    )

    parser.add_argument(
        '-b', '--bloc-name',
        required=True,
        help='BLoC name in snake_case (e.g., auth, login, user_profile)'
    )

    parser.add_argument(
        '-f', '--feature',
        default='',
        help='Feature name if BLoC belongs to a feature (e.g., auth, user)'
    )

    parser.add_argument(
        '-o', '--output',
        default='lib/features',
        help='Output directory for the BLoC (default: lib/features)'
    )

    args = parser.parse_args()

    # Validate bloc name
    if not args.bloc_name.replace('_', '').isalnum():
        print('Error: BLoC name must contain only alphanumeric characters and underscores')
        sys.exit(1)

    # Create BLoC files
    base_path = Path(args.output)
    try:
        created_files = create_bloc_files(base_path, args.bloc_name, args.feature)

        pascal_name = to_pascal_case(args.bloc_name)

        print(f'\\n✓ BLoC "{pascal_name}" created successfully!')
        print(f'\\nGenerated files:')
        for file_path, _ in created_files:
            rel_path = file_path.relative_to(Path.cwd())
            print(f'  - {rel_path}')

        print(f'\\nNext steps:')
        print(f'  1. Import use cases in the BLoC')
        print(f'  2. Implement event handlers')
        print(f'  3. Add actual types to State (replace "dynamic")')
        print(f'  4. Uncomment and implement test cases')
        print(f'  5. Run tests: flutter test')

    except Exception as e:
        print(f'Error creating BLoC: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
