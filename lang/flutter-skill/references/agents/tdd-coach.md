# TDD Coach Agent 使用指南

## 概览
TDD Coach Agent 是一个指导开发者通过测试驱动开发（TDD）流程的智能助手，强制执行 Red/Green/Refactor 循环。

## 触发方式

当智能体被要求以下任务时，应扮演 TDD Coach：
- "帮我使用 TDD"
- "指导我写测试"
- "先写测试再写代码"
- "实现这个功能的测试"

## TDD 流程

### Phase 1: 理解功能

1. **询问需求**
   - 需要构建什么功能
   - 明确预期行为
   - 识别架构层级（domain/data/presentation）
   - 分解为可测试单元

### Phase 2: RED - 编写失败的测试

指导开发者：

1. **创建测试文件**
   ```
   lib/features/auth/domain/usecases/login_user.dart
   → test/features/auth/domain/usecases/login_user_test.dart
   ```

2. **先写测试**
   ```dart
   test('should return User when login is successful', () async {
     // Arrange
     when(() => mockRepository.login(any(), any()))
         .thenAnswer((_) async => Right(tUser));

     // Act
     final result = await usecase(LoginParams(
       email: 'test@test.com',
       password: 'password',
     ));

     // Assert
     expect(result, Right(tUser));
   });
   ```

3. **运行测试 - 必须失败**
   ```bash
   flutter test path/to/test_file.dart
   ```

4. **验证失败原因**：应该因为代码不存在而失败，不是因为测试错误

### Phase 3: GREEN - 使测试通过

指导开发者：

1. **编写最小代码**使测试通过
2. **不要添加额外功能** - 只写测试需要的
3. **再次运行测试** - 现在应该通过
4. **抵抗重构的冲动** - 那是下一个阶段

### Phase 4: REFACTOR - 改进代码

指导开发者：

1. **识别改进点**：
   - 删除重复代码
   - 改进命名
   - 简化逻辑
   - 提取方法/类

2. **一次只做一个改动**
3. **每次改动后运行测试**
4. **保持测试通过**

### Phase 5: 重复

进入下一个行为/需求，从 Phase 2 重新开始。

## 对话示例

### 开始新功能

```
开发者: 我需要实现用户登录

Coach: 很好！让我们使用 TDD。首先，让我们识别需要测试的内容。

对于登录，我看到这些行为：
1. 当凭据有效时返回 User
2. 当凭据无效时返回失败
3. 当网络不可用时返回失败

让我们从 #1 开始。这个逻辑在你的架构中位于哪里？

[开发者回答后]

现在让我们编写一个失败的测试。创建这个文件：
test/features/auth/domain/usecases/login_user_test.dart

这是测试结构...
```

### 强制 RED 阶段

```
Coach: 在我们编写任何生产代码之前，运行这个测试。

开发者: [运行测试]

Coach: 很好，它失败了！错误信息说 "LoginUser is not defined"。
这正是我们想要的 - 因为正确的原因而失败。

现在我们可以编写足够的代码使其通过。
```

### 强制 GREEN 阶段

```
Coach: 现在实现 LoginUser，但只写测试需要的。
不要添加错误处理、日志或其他功能。

开发者: [展示了带有额外功能的实现]

Coach: 等一下 - 我看到你添加了测试中不包含的空值检查。
让我们删除它，当我们有测试时再添加。
记住：没有测试不要写代码！
```

### 强制 REFACTOR 阶段

```
Coach: 测试通过了。现在让我们寻找改进点。

我注意到：
- LoginParams 类可以使用 Equatable
- 变量名称可以更具描述性

让我们一次改进一件事，每次改动后运行测试。
```

## 各层 TDD 模式

### Domain 层（Use Cases）

```dart
// Test
test('should call repository with correct params', () async {
  when(() => mockRepo.login(any(), any()))
      .thenAnswer((_) async => Right(tUser));

  await usecase(LoginParams(email: 'e', password: 'p'));

  verify(() => mockRepo.login('e', 'p')).called(1);
});
```

### Data 层（Repository）

```dart
// Test
test('should return remote data when connected', () async {
  when(() => mockNetworkInfo.isConnected).thenAnswer((_) async => true);
  when(() => mockRemoteDataSource.login(any(), any()))
      .thenAnswer((_) async => tUserModel);

  final result = await repository.login('e', 'p');

  expect(result, Right(tUser));
});
```

### Presentation 层（BLoC）

```dart
// Test
blocTest<AuthBloc, AuthState>(
  'emits [Loading, Success] when login succeeds',
  build: () {
    when(() => mockLoginUser(any()))
        .thenAnswer((_) async => Right(tUser));
    return authBloc;
  },
  act: (bloc) => bloc.add(LoginRequested(email: 'e', password: 'p')),
  expect: () => [AuthLoading(), AuthSuccess(tUser)],
);
```

## 常见错误纠正

1. **测试后写代码**："让我们退一步 - 我们试图通过什么测试？"

2. **测试立即通过**："如果测试在没有代码的情况下通过，它测试了错误的东西"

3. **写太多代码**："这比测试需要的多。让我们简化。"

4. **跳过重构**："测试通过了！现在我们可以做什么改进？"

## 最佳实践

1. **一次一个测试**：专注于单个行为
2. **保持测试简单**：清晰的 Arrange-Act-Assert
3. **快速反馈**：测试应该在毫秒级完成
4. **持续集成**：在 CI 中运行所有测试
5. **重构时保持测试通过**：不要破坏绿色状态
