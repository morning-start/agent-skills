---
name: moonbit
version: 11.1.0
description: >
  Use when the user asks about MoonBit project setup, writing or refactoring code,
  debugging compiler errors, tests, publishing, optimization, FFI, or architecture decisions.
  Keywords: MoonBit, .mbt, .pkg, moon new, moon build, moon test, moon check.
tags: [moonbit, language-skill, task-router, code-generation, debugging, testing, publishing, ffi, architecture]
trigger:
  - "MoonBit"
  - ".mbt"
  - ".pkg"
  - "moon new"
  - "moon build"
  - "moon test"
  - "moon check"
category: language-skill
meta:
  complexity: intermediate
  standalone: true
  version_policy: "Prefer the installed MoonBit toolchain and references over hard-coded version claims."
---

# MoonBit Action Handbook

> This is the fast entry point for MoonBit work.
>
> Use this file for common tasks, then jump to `skills/` or `references/` only when the task needs more depth.

## Start Here

Use these commands to validate the local toolchain and start a project:

```bash
moon --version
moon new my-app
moon check
moon test
moon build
moon fmt
```

If the user asked for a specific target, verify the target in the relevant sub-skill before choosing build flags.

## Minimal Code Shapes

### Function

```moonbit
fn greet(name: String) -> String {
  "Hello, \{name}!"
}
```

### Main

```moonbit
fn main {
  println(greet("MoonBit"))
}
```

### Struct and enum

```moonbit
struct Point {
  x: Int
  y: Int
}

enum Color {
  Red
  Green
  Blue
}
```

### Trait and impl

```moonbit
pub(open) trait Show {
  fn to_string(self) -> String
}

impl Show for Point with to_string(self) -> String {
  "Point(\{self.x}, \{self.y})"
}
```

### Error handling

```moonbit
suberror NotFound

fn lookup(id: Int) -> String raise NotFound {
  if id <= 0 {
    raise NotFound
  }
  "ok"
}
```

## Task Router

| User intent | Go to | Use when |
|---|---|---|
| Create a new project | `skills/1-create-project/SKILL.md` | New app, library, CLI, or template selection |
| Write or refactor code | `skills/2-write-code/SKILL.md` | Functions, traits, generics, match, visibility, mutation |
| Debug errors | `skills/3-debug-errors/SKILL.md` | Parse errors, type errors, compiler diagnostics, bad migrations |
| Write tests | `skills/4-write-tests/SKILL.md` | Test layout, assertions, test helpers, coverage |
| Optimize performance | `skills/5-optimize/SKILL.md` | Runtime speed, binary size, backend choice, benchmarking |
| Publish a library | `skills/6-publish-lib/SKILL.md` | mooncakes release, package prep, validation, versioning |
| Integrate FFI | `skills/7-ffi-integration/SKILL.md` | C/JS interop, extern bindings, wrapper design |
| Make architecture decisions | `skills/8-architecture-decisions/SKILL.md` | API shape, module boundaries, design tradeoffs |

## Reference Map

| File | Best use |
|---|---|
| `references/syntax.md` | Quick syntax lookup |
| `references/type-system.md` | Types, options, results, refs, and data modeling |
| `references/generics-traits-methods.md` | Generics, traits, methods, and implementation patterns |
| `references/pattern-matching.md` | Match expressions and advanced branching |
| `references/error-codes.md` | Compiler errors and fix strategies |
| `references/project-layout.md` | Module and package layout |
| `references/app-templates.md` | Project templates and scaffolding patterns |
| `references/library-design.md` | Public API and library design |
| `references/multi-backend.md` | Wasm, JS, and native backend strategy |
| `references/real-world-examples.md` | Case studies from real projects |
| `references/pitfalls.md` | Common mistakes and how to avoid them |
| `references/async.md` | Experimental async support |
| `references/verification.md` | Experimental verification material |
| `references/decision-matrices.md` | Tradeoff tables for choosing an approach |
| `references/architecture.md` | How this skill is organized |

## Execution Checklist

Use this checklist before handing work back:

1. Run `moon check`.
2. Run `moon test`.
3. Run `moon fmt`.
4. Build the target the user cares about.
5. If the task touches public API, verify the route to `skills/8-architecture-decisions/`.

## Guidance

- Prefer the sub-skill when the task is focused and specific.
- Prefer `references/` when you need deeper detail or a second example.
- Avoid hard-coded claims about exact MoonBit syntax or release dates unless they are verified against the installed toolchain.
- Keep examples minimal in this file; put specialized patterns in the child skills and references.

## Notes

- This skill is a router and handbook, not a full tutorial.
- If a user reports a compiler error, route to `skills/3-debug-errors/` first and then confirm with `references/error-codes.md` if needed.
- If a user asks for performance advice, route to `skills/5-optimize/` and measure before changing code.
- If a user asks for a new project, route to `skills/1-create-project/` and choose the template before writing code.

