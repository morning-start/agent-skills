# core 命名空间

`core` 命名空间是 Tauri 的核心功能模块，提供与 Rust 后端通信的基础能力。

## 导入

```typescript
import { invoke } from '@tauri-apps/api/core';
```

## 函数

### invoke<T>(cmd: string, args?: object): Promise<T>

调用 Rust 后端命令。

**参数：**
- `cmd`: 命令名称（Rust 函数名）
- `args`: 传递给命令的参数对象

**返回：**
- `Promise<T>`: 命令的返回结果

**示例：**

```typescript
// 调用 Rust 命令
const result = await invoke<string>('greet', { name: 'World' });
console.log(result); // "Hello, World!"

// 调用返回 JSON 对象的命令
const user = await invoke<{ id: number; name: string }>('get_user', { id: 1 });
console.log(user.name); // "John"
```

### invokePlugin(plugin: string, cmd: string, args?: object): Promise<T>

调用插件命令。

**示例：**
```typescript
const file = await invokePlugin('dialog', 'open', {
  multiple: false,
  filters: [{ name: 'Images', extensions: ['png', 'jpg'] }]
});
```

## 创建自定义命令（Rust）

在 `src-tauri/src/main.rs` 中定义命令：

```rust
use tauri::command;

#[derive(Serialize)]
struct User {
    id: u32,
    name: String,
}

#[command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

#[command]
fn get_user(id: u32) -> Result<User, String> {
    Ok(User { id, name: "John".to_string() })
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, get_user])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## 错误处理

```typescript
import { invoke } from '@tauri-apps/api/core';

try {
  const result = await invoke('my_command');
} catch (error) {
  console.error('Error:', error);
}
```

## 泛型类型

使用泛型指定返回类型：

```typescript
// 字符串
const str: string = await invoke<string>('get_string');

// 数字
const num: number = await invoke<number>('get_number');

// 数组
const arr: string[] = await invoke<string[]>('get_array');

// 对象
interface User { id: number; name: string; email: string }
const user: User = await invoke<User>('get_user');
```
