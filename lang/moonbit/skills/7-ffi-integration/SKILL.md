---
name: ffi-integration
version: 10.0.0
description: >
  FFI 与跨语言集成。C FFI 绑定、JS extern 声明、
  类型映射、所有权处理、条件编译。
  Use when integrating C libraries, calling JavaScript APIs,
  declaring extern functions, or building cross-language bridges.
trigger:
  - "FFI" / "ffi" / "extern" / "C 函数" / "JS 调用"
  - "绑定" / "binding" / "interop" / "互操作"
  - "native" / "c 语言" / "javascript bridge"
tags: [ffi, c-ffi, js-extern, interop, binding, cross-language]
---

# FFI 与跨语言集成

## 触发条件
用户需要**与 C/JS 代码交互**时激活。

## 决策树

```
FFI 目标？
├── JavaScript (JS 后端)
│   ├── 调用 JS API → extern "js" fn name(...) = "...";
│   ├── 异步操作 → extern "js" fn fetch(...) -> JsPromise;
│   └── 对象操作 → extern "js" fn new_map() -> JsMap;
├── C Native (Native 后端)
│   ├── 调用 C 函数 → extern "c" fn c_func(...);
│   ├── 类型映射 → CString/String/Opaque/Ptr
│   └── 内存管理 → RAII / defer 释放
└── 双后端都需要
    └── 条件编译 → #if[target="js"] ... #else ... #endif
```

## 执行步骤

### Step 1: 确定 FFI 目标和后端
- 当前项目的 target 是什么？(`moon.pkg` 中的 target 声明)
- 需要与哪种语言交互？

### Step 2: 声明 extern 函数
**JS 示例**:
```moonbit
extern "js" fn console_log(msg : String) -> Unit = "(msg) => console.log(msg)"
extern "js" fn json_parse(text : String) -> Dynamic = "(text) => JSON.parse(text)"
extern "js" fn now_ms() -> Int = "() => Date.now()"
pub async fn http_get(url : String) -> Result[String, String] {
  try {
    let response = await fetch(url)
    if response.ok { Ok(await response.text()) }
    else { Err("HTTP " + response.status.to_string()) }
  } catch e : Error { Err(e.message()) }
}
```

**C 示例**:
```moonbit
type OpaqueDb = Opaque
extern "c" fn sqlite3_open(filename : CString, out : Ptr[OpaqueDb]) -> Int
extern "c" fn sqlite3_close(db : OpaqueDb) -> Int
extern "c" fn sqlite3_exec(db : OpaqueDb, sql : CString, ...) -> Int
```

### Step 3: 包装为类型安全 API
- 用 struct 包装 opaque 指针
- 将 C 错误码转为 MoonBit Result
- 提供 RAII 式资源管理

### Step 4: 条件编译（如需双后端）
```moonbit
#if(target="js")
  extern "js" fn platform_specific() -> String = "() => 'js'"
#elseif(target="native")
  extern "c" fn platform_specific() -> String
#endif
```

### Step 5: 测试
- 分别在各目标后端下测试 FFI 调用
- 验证类型映射正确性
- 检查内存泄漏（C FFI）

## FFI 最佳实践
1. **最小化 FFI 边界** — 只在边界转换，内部保持纯 MoonBit
2. **类型安全包装** — 用 struct 包装 opaque，不暴露裸指针
3. **RAII 资源管理** — defer/guard 确保释放
4. **错误码翻译** → C 错误码转 Result
5. **字符串处理** — CString/String 双向转换

## 详细知识
🔗 `references/` 中 ffi 技能迁移的完整内容
🔗 `references/library-design.md` Part 13 FFI 互操作实战
🔗 `references/multi-backend.md` 条件编译章节