#!/usr/bin/env python3
"""
Generate Flutter Test Script

This script generates a test file with boilerplate for any source file.

Usage:
    python generate_test.py --source <source_file_path>
    python generate_test.py -s <source_file_path>

Example:
    python generate_test.py --source lib/features/auth/domain/usecases/login_user.dart
    python generate_test.py -s lib/features/auth/presentation/bloc/auth_bloc.dart
"""

import argparse
import re
import sys
from pathlib import Path


def to_pascal_case(snake_str: str) -> str:
    """Convert snake_case to PascalCase."""
    return ''.join(x.capitalize() for x in snake_str.lower().split('_'))


def to_snake_case(pascal_str: str) -> str:
    """Convert PascalCase to snake_case."""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', pascal_str).lower()


def detect_class_type(content: str) -> str:
    """Detect the type of class in the source file."""
    if 'implements UseCase' in content:
        return 'usecase'
    elif 'implements ' in content and 'Bloc' in content:
        return 'bloc'
    elif 'StatelessWidget' in content or 'StatefulWidget' in content:
        return 'widget'
    elif 'implements ' in content and 'Repository' in content:
        return 'repository'
    else:
        return 'class'


def extract_class_info(content: str, class_type: str) -> dict:
    """Extract class name and dependencies from source content."""
    info = {'name': '', 'dependencies': []}

    # Find class name
    class_match = re.search(r'class\s+(\w+)', content)
    if class_match:
        info['name'] = class_match.group(1)

    # Find constructor dependencies
    constructor_match = re.search(r'\((.*?)\)', content)
    if constructor_match:
        params = constructor_match.group(1)
        # Extract field declarations
        deps = re.findall(r'final\s+(\w+(?:<[^>]+>)?)\s+(\w+)', params)
        info['dependencies'] = deps

    return info


def generate_usecase_test(source_path: Path, class_info: dict) -> str:
    """Generate test file for UseCase."""
    class_name = class_info['name']
    class_name_snake = to_snake_case(class_name)
    module_path = str(source_path.parent.parent.parent.relative_to(Path('lib')))
    feature_name = source_path.parts[source_path.parts.index('features') + 1] if 'features' in source_path.parts else ''

    return f'''import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dartz/dartz.dart';

import 'package:your_app/{source_path.parent.relative_to(Path("lib")).as_posix()}/{class_name_snake}.dart';
import 'package:your_app/{source_path.parent.parent.relative_to(Path("lib")).as_posix()}/repositories/{feature_name}_repository.dart';
import 'package:your_app/{source_path.parent.parent.parent.relative_to(Path("lib")).as_posix()}/entities/{feature_name[:-1]}.dart';
import 'package:your_app/core/error/failures.dart';

// TODO: Create mock repository if needed
// class Mock{class_info['dependencies'][0][0].replace('<', '').replace('>', '')} extends Mock implements {class_info['dependencies'][0][0].replace('<', '').replace('>', '')} {{}}

void main() {{
  late {class_name} usecase;
  // TODO: Initialize mocks
  // late MockRepository mockRepository;

  setUp(() {{
    // TODO: Setup mocks
    // mockRepository = MockRepository();
    // usecase = {class_name}(mockRepository);
  }});

  // TODO: Register fallback values if needed
  // setUpAll(() {{
  //   registerFallbackValue(Params());
  // }});

  group('{class_name}', () {{
    test('should return result when successful', () async {{
      // Arrange
      // when(() => mockRepository.method(any()))
      //     .thenAnswer((_) async => Right(result));

      // Act
      // final result = await usecase(Params());

      // Assert
      // expect(result, Right(result));
      // verify(() => mockRepository.method(any())).called(1);
      // verifyNoMoreInteractions(mockRepository);
    }});

    test('should return Failure when fails', () async {{
      // Arrange
      // when(() => mockRepository.method(any()))
      //     .thenAnswer((_) async => Left(ServerFailure('error')));

      // Act
      // final result = await usecase(Params());

      // Assert
      // expect(result.isLeft(), true);
    }});
  }});
}}
'''


def generate_bloc_test(source_path: Path, class_info: dict) -> str:
    """Generate test file for BLoC."""
    class_name = class_info['name']
    return f'''import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dartz/dartz.dart';

import 'package:your_app/{source_path.parent.relative_to(Path("lib")).as_posix()}/{class_name.lower()}.dart';

// TODO: Create mock use cases
// class MockUseCase extends Mock implements UseCase {{}}

void main() {{
  // late {class_name} bloc;
  // TODO: Initialize mocks
  // late MockUseCase mockUseCase;

  setUp(() {{
    // TODO: Setup mocks
    // mockUseCase = MockUseCase();
    // bloc = {class_name}(useCase: mockUseCase);
  }});

  // TODO: Register fallback values if needed
  // setUpAll(() {{
  //   registerFallbackValue(FakeParams());
  // }});

  tearDown(() {{
    bloc.close();
  }});

  test('initial state should be Initial', () {{
    expect(bloc.state, Initial());
  }});

  // TODO: Add blocTest cases
  // blocTest<{class_name}, State>(
  //   'emits [Loading, Success] when Event is added',
  //   build: () {{
  //     when(() => mockUseCase(any()))
  //         .thenAnswer((_) async => Right(data));
  //     return bloc;
  //   }},
  //   act: (bloc) => bloc.add(Event()),
  //   expect: () => [Loading(), Success(data)],
  // );
}});
'''


def generate_widget_test(source_path: Path, class_info: dict) -> str:
    """Generate test file for Widget."""
    class_name = class_info['name']
    return f'''import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'package:your_app/{source_path.parent.relative_to(Path("lib")).as_posix()}/{to_snake_case(class_name)}.dart';

// TODO: Create mock bloc if needed
// class MockBloc extends MockBloc<Event, State> implements Bloc<Event, State> {{}}

void main() {{
  // TODO: Initialize mocks
  // late MockBloc mockBloc;

  setUp(() {{
    // mockBloc = MockBloc();
  }});

  Widget createWidget() {{
    return MaterialApp(
      home: {class_name}(),
    );
  }}

  group('{class_name}', () {{
    testWidgets('should render correctly', (tester) async {{
      // Arrange
      // when(() => mockBloc.state).thenReturn(State());

      // Act
      await tester.pumpWidget(createWidget());

      // Assert
      // expect(find.byType(SomeWidget), findsOneWidget);
    }});

    // TODO: Add more widget tests
    // testWidgets('should handle user interaction', (tester) async {{
    //   await tester.pumpWidget(createWidget());
    //
    //   await tester.tap(find.byKey(Key('button')));
    //   await tester.pump();
    //
    //   verify(() => mockBloc.add(Event())).called(1);
    // }});
  }});
}}
'''


def generate_test_file(source_path: Path):
    """Generate test file based on source file type."""
    # Read source file
    if not source_path.exists():
        raise FileNotFoundError(f'Source file not found: {source_path}')

    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Detect class type
    class_type = detect_class_type(content)

    # Extract class info
    class_info = extract_class_info(content, class_type)

    # Determine test file path
    lib_index = source_path.parts.index('lib') if 'lib' in source_path.parts else -1
    if lib_index >= 0:
        test_path = Path('test') / source_path.parts[lib_index + 1:]
        test_path = test_path.with_suffix('_test.dart')
    else:
        raise ValueError('Source file must be in lib directory')

    # Generate test content
    if class_type == 'usecase':
        test_content = generate_usecase_test(source_path, class_info)
    elif class_type == 'bloc':
        test_content = generate_bloc_test(source_path, class_info)
    elif class_type == 'widget':
        test_content = generate_widget_test(source_path, class_info)
    else:
        test_content = generate_widget_test(source_path, class_info)

    # Create test file
    test_path.parent.mkdir(parents=True, exist_ok=True)
    with open(test_path, 'w', encoding='utf-8') as f:
        f.write(test_content)

    return test_path


def main():
    parser = argparse.ArgumentParser(
        description='Generate a test file with boilerplate for any source file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python generate_test.py --source lib/features/auth/domain/usecases/login_user.dart
  python generate_test.py -s lib/features/auth/presentation/bloc/auth_bloc.dart
  python generate_test.py -s lib/features/auth/presentation/pages/login_page.dart
        '''
    )

    parser.add_argument(
        '-s', '--source',
        required=True,
        help='Path to source file (e.g., lib/features/auth/domain/usecases/login_user.dart)'
    )

    args = parser.parse_args()

    # Generate test file
    try:
        test_path = generate_test_file(Path(args.source))

        print(f'\\n✓ Test file created successfully!')
        print(f'\\nGenerated file:')
        print(f'  - {test_path}')

        print(f'\\nNext steps:')
        print(f'  1. Uncomment and implement mock classes')
        print(f'  2. Update imports to match your project structure')
        print(f'  3. Implement test cases')
        print(f'  4. Run tests: flutter test {test_path}')

    except FileNotFoundError as e:
        print(f'Error: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'Error generating test: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
