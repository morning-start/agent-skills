#!/usr/bin/env python3
"""
Generate Flutter Model Script

This script generates a Freezed model with JSON serialization and corresponding domain entity.

Usage:
    python generate_model.py --model-name <model_name> [--fields <field_spec>]
    python generate_model.py -m <model_name> -f <field_spec>

Field format:
    field_name:field_type[:default_value]
    - field_name: snake_case identifier
    - field_type: String, int, double, bool, DateTime, List<String>, etc.
    - default_value (optional): value for nullable fields or defaults

Examples:
    python generate_model.py --model-name user
    python generate_model.py -m user -f id:String,name:String,email:String?
    python generate_model.py -m product -f id:String,name:String,price:double,isActive:bool=false
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


def parse_field(field_spec: str) -> dict:
    """Parse a field specification string."""
    parts = field_spec.split(':')

    if len(parts) < 2:
        raise ValueError(f"Invalid field specification: {field_spec}")

    field_name = parts[0]
    field_type = parts[1]
    default_value = parts[2] if len(parts) > 2 else None

    return {
        'name': field_name,
        'type': field_type,
        'default': default_value,
        'is_nullable': field_type.endswith('?'),
        'base_type': field_type.rstrip('?')
    }


def generate_model(model_name: str, fields: list) -> str:
    """Generate Freezed model file content."""
    pascal_name = to_pascal_case(model_name)

    # Build field definitions
    field_lines = []
    json_keys = []

    for field in fields:
        field_name = field['name']
        field_type = field['base_type']
        is_nullable = field['is_nullable']
        default_value = field['default']

        if field_type == 'String':
            dart_type = 'String'
        elif field_type in ['int', 'double', 'bool', 'DateTime']:
            dart_type = field_type
        elif field_type.startswith('List<'):
            dart_type = field_type
        else:
            dart_type = field_type

        # Generate field line
        if default_value is not None:
            if default_value.lower() == 'false':
                field_lines.append(f'    @Default(false) bool {field_name},')
            elif default_value.lower() == 'true':
                field_lines.append(f'    @Default(true) bool {field_name},')
            elif default_value == '[]':
                field_lines.append(f'    @Default([]) List<String> {field_name},')
            elif default_value.startswith('"') or default_value.startswith("'"):
                field_lines.append(f"    @Default({default_value}) String {field_name},")
            else:
                field_lines.append(f'    @Default({default_value}) {dart_type} {field_name},')
        elif is_nullable:
            field_lines.append(f'    {dart_type}? {field_name},')
        else:
            field_lines.append(f'    required {dart_type} {field_name},')

        # Add to entity conversion list
        json_keys.append(field_name)

    # Generate entity conversion
    entity_params = ',\n    '.join([f"{field['name']}: {field['name']}" for field in fields])
    model_params = ',\n    '.join([f"{field['name']}: entity.{field['name']}" for field in fields])

    return f'''import 'package:freezed_annotation/freezed_annotation.dart';
import '../../domain/entities/{model_name}.dart';

part '{model_name}_model.freezed.dart';
part '{model_name}_model.g.dart';

@freezed
class {pascal_name}Model with _${{pascal_name}}Model {{
  const {pascal_name}Model._();

  const factory {pascal_name}Model({{
    required String id,
{chr(10).join(field_lines)}
  }}) = _{pascal_name}Model;

  factory {pascal_name}Model.fromJson(Map<String, dynamic> json) =>
      _${{pascal_name}}ModelFromJson(json);

  {pascal_name} toEntity() => {pascal_name}(
    id: id,
    {',\n    '.join([f"{field['name']}: {field['name']}" for field in fields])}
  );

  factory {pascal_name}Model.fromEntity({pascal_name} entity) => {pascal_name}Model(
    id: entity.id,
    {',\n    '.join([f"{field['name']}: entity.{field['name']}" for field in fields])}
  );
}}
'''


def generate_entity(model_name: str, fields: list) -> str:
    """Generate domain entity file content."""
    pascal_name = to_pascal_case(model_name)

    # Build field definitions
    field_lines = []
    props = ['id']

    for field in fields:
        field_name = field['name']
        field_type = field['base_type']
        is_nullable = field['is_nullable']

        if field_type == 'String':
            dart_type = 'String'
        elif field_type in ['int', 'double', 'bool', 'DateTime']:
            dart_type = field_type
        elif field_type.startswith('List<'):
            dart_type = field_type
        else:
            dart_type = field_type

        nullable_suffix = '?' if is_nullable else ''
        field_lines.append(f'  final {dart_type}{nullable_suffix} {field_name};')
        props.append(field_name)

    # Build copyWith parameters
    copywith_params = []
    for field in fields:
        field_name = field['name']
        copywith_params.append(f'    {field["type"]}? {field_name},')

    # Build copyWith body
    copywith_body = []
    copywith_body.append(f'    id: id ?? this.id,')
    for field in fields:
        field_name = field['name']
        copywith_body.append(f'    {field_name}: {field_name} ?? this.{field_name},')

    return f'''import 'package:equatable/equatable.dart';

class {pascal_name} extends Equatable {{
  final String id;
{chr(10).join(field_lines)}

  const {pascal_name}({{
    required this.id,
{',\n    '.join([f"    required this.{field['name']}," if not field['is_nullable'] and field['default'] is None else f"    this.{field['name']}," for field in fields])}
  }});

  @override
  List<Object?> get props => [{', '.join(props)}];

  {pascal_name} copyWith({{
    String? id,
{chr(10).join(copywith_params)}
  }}) {{
    return {pascal_name}(
{chr(10).join(copywith_body)}
    );
  }}
}}
'''


def create_model_files(base_path: Path, model_name: str, feature_name: str, fields: list):
    """Create model and entity files."""
    # Determine paths
    if feature_name:
        model_path = base_path / feature_name / 'data' / 'models' / f'{model_name}_model.dart'
        entity_path = base_path / feature_name / 'domain' / 'entities' / f'{model_name}.dart'
    else:
        model_path = base_path / 'data' / 'models' / f'{model_name}_model.dart'
        entity_path = base_path / 'domain' / 'entities' / f'{model_name}.dart'

    # Create directories
    model_path.parent.mkdir(parents=True, exist_ok=True)
    entity_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate and write files
    with open(model_path, 'w', encoding='utf-8') as f:
        f.write(generate_model(model_name, fields))

    with open(entity_path, 'w', encoding='utf-8') as f:
        f.write(generate_entity(model_name, fields))

    return [(model_path, 'model'), (entity_path, 'entity')]


def main():
    parser = argparse.ArgumentParser(
        description='Generate a Freezed model with JSON serialization for Flutter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python generate_model.py --model-name user
  python generate_model.py -m user -f id:String,name:String,email:String?
  python generate_model.py -m product -f id:String,name:String,price:double,isActive:bool=false
  python generate_model.py -m order_item -f id:String,productId:String,quantity:int,price:double

Field types:
  - String: text data
  - int: integer numbers
  - double: floating-point numbers
  - bool: boolean values
  - DateTime: date and time
  - List<Type>: list of items (e.g., List<String>)

Default values:
  - Append "?": nullable field (e.g., String?)
  - Append ":false": default boolean (e.g., isActive:bool=false)
  - Append ":[]": default empty list (e.g., tags:List<String>=[])
  - Append ':"value"': default string (e.g., status:String="active")
        '''
    )

    parser.add_argument(
        '-m', '--model-name',
        required=True,
        help='Model name in snake_case (e.g., user, product, order_item)'
    )

    parser.add_argument(
        '-f', '--fields',
        default='',
        help='Comma-separated field specifications (e.g., id:String,name:String,email:String?)'
    )

    parser.add_argument(
        '-o', '--output',
        default='lib/features',
        help='Output directory for the model (default: lib/features)'
    )

    parser.add_argument(
        '--feature',
        default='',
        help='Feature name if model belongs to a feature (e.g., auth, user)'
    )

    args = parser.parse_args()

    # Validate model name
    if not args.model_name.replace('_', '').isalnum():
        print('Error: Model name must contain only alphanumeric characters and underscores')
        sys.exit(1)

    # Parse fields
    fields = []
    if args.fields:
        for field_spec in args.fields.split(','):
            field_spec = field_spec.strip()
            if field_spec:
                try:
                    fields.append(parse_field(field_spec))
                except ValueError as e:
                    print(f'Error parsing field "{field_spec}": {e}')
                    sys.exit(1)
    else:
        # Add default id field if no fields specified
        fields.append({
            'name': 'id',
            'type': 'String',
            'default': None,
            'is_nullable': False,
            'base_type': 'String'
        })

    # Create model files
    base_path = Path(args.output)
    try:
        created_files = create_model_files(base_path, args.model_name, args.feature, fields)

        pascal_name = to_pascal_case(args.model_name)

        print(f'\\n✓ Model "{pascal_name}" created successfully!')
        print(f'\\nGenerated files:')
        for file_path, file_type in created_files:
            rel_path = file_path.relative_to(Path.cwd())
            print(f'  - {rel_path} ({file_type})')

        print(f'\\nNext steps:')
        print(f'  1. Review and customize the generated model')
        print(f'  2. Add the model to your repository if needed')
        print(f'  3. Run: dart run build_runner build --delete-conflicting-outputs')

        if args.fields:
            print(f'\\nGenerated fields:')
            for field in fields:
                nullable_str = '?' if field['is_nullable'] else ''
                default_str = f' (default: {field["default"]})' if field['default'] else ''
                print(f'  - {field["name"]}: {field["base_type"]}{nullable_str}{default_str}')

    except Exception as e:
        print(f'Error creating model: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
