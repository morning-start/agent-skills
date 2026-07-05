---
description: Create a Freezed model with JSON serialization
argument-hint: <model-name> [--fields field1:type,field2:type]
allowed-tools: Bash, Write, Read
---

# /generate-model Command

Generate a Freezed model class with JSON serialization.

## Instructions

When the user runs `/generate-model <model-name>`:

1. **Parse Arguments**
   - Model name (e.g., `user`, `UserModel`, `order_item`)
   - Optional fields: `--fields id:String,name:String,email:String?`

2. **Determine Location**
   - Ask for feature name if not clear
   - Default path: `lib/features/<feature>/data/models/`

3. **Generate Model File**

Create `lib/features/<feature>/data/models/<model_name>_model.dart`:

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part '<model_name>_model.freezed.dart';
part '<model_name>_model.g.dart';

@freezed
class <ModelName>Model with _$<ModelName>Model {
  const <ModelName>Model._();

  const factory <ModelName>Model({
    required String id,
    // Add fields from arguments or placeholders
    @JsonKey(name: 'field_name') required String fieldName,
    String? optionalField,
    @Default(false) bool hasDefault,
    @Default([]) List<String> listField,
  }) = _<ModelName>Model;

  factory <ModelName>Model.fromJson(Map<String, dynamic> json) =>
      _$<ModelName>ModelFromJson(json);

  // Convert to domain entity
  <ModelName> toEntity() => <ModelName>(
    id: id,
    // Map all fields
  );

  // Create from domain entity
  factory <ModelName>Model.fromEntity(<ModelName> entity) => <ModelName>Model(
    id: entity.id,
    // Map all fields
  );
}
```

4. **Generate Corresponding Entity** (if doesn't exist)

Create `lib/features/<feature>/domain/entities/<model_name>.dart`:

```dart
import 'package:equatable/equatable.dart';

class <ModelName> extends Equatable {
  final String id;
  // Add fields

  const <ModelName>({
    required this.id,
  });

  @override
  List<Object?> get props => [id];

  <ModelName> copyWith({
    String? id,
  }) {
    return <ModelName>(
      id: id ?? this.id,
    );
  }
}
```

5. **Common Field Types**

```dart
// String
required String name,

// Nullable
String? middleName,

// With default
@Default('') String description,

// Boolean with default
@Default(false) bool isActive,

// DateTime
required DateTime createdAt,

// JSON key mapping
@JsonKey(name: 'created_at') required DateTime createdAt,

// Enum
required UserStatus status,

// List
@Default([]) List<String> tags,

// Nested object
required AddressModel address,

// List of objects
@Default([]) List<OrderItemModel> items,
```

6. **Enum Generation** (if needed)

```dart
enum UserStatus {
  @JsonValue('active')
  active,
  @JsonValue('inactive')
  inactive,
  @JsonValue('pending')
  pending,
}
```

7. **Output Summary**

```
Model '<ModelName>Model' created successfully!

Files created:
- lib/features/<feature>/data/models/<model_name>_model.dart
- lib/features/<feature>/domain/entities/<model_name>.dart (if new)

Run code generation:
dart run build_runner build --delete-conflicting-outputs

This will generate:
- <model_name>_model.freezed.dart
- <model_name>_model.g.dart
```

## Field Syntax

```bash
# Basic fields
/generate-model user --fields id:String,name:String,email:String

# With optional fields (append ?)
/generate-model user --fields id:String,name:String,email:String?

# With defaults
/generate-model user --fields id:String,isActive:bool=false

# With JSON key mapping
/generate-model user --fields id:String,created_at:DateTime
```

## Examples

```bash
# Simple model
/generate-model product

# With fields
/generate-model order_item --fields id:String,productId:String,quantity:int,price:double

# Complex model
/generate-model user_profile --fields id:String,firstName:String,lastName:String,email:String,avatar:String?,isVerified:bool=false
```
