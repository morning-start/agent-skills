---
name: rust-iterators
version: 1.0.0
author: book-skills
description: Rust 迭代器与闭包技能，掌握迭代器惰性求值、适配器模式、闭包定义和捕获方式
tags: [rust, iterators, iterator-adapters, collect, closures]
layer: Layer 1 - Language Mechanics
trigger: iterator, closure, adapter, collect, lazy evaluation
---

# Rust 迭代器与闭包

## 任务目标

- 本 Skill 用于：使用迭代器和闭包实现函数式编程风格
- 能力包含：迭代器创建、迭代器适配器、闭包定义、闭包捕获、enumerate、zip
- 触发条件：需要处理集合转换、函数式编程、惰性求值

## 前置准备

- 完成 rust-core-skill 和 rust-collections-skill
- 理解 Rust 所有权的特殊性

## 迭代器基础

### 创建迭代器

```rust
let v = vec![1, 2, 3];

// iter() - 不可变引用
for val in v.iter() {
    println!("{}", val);
}

// iter_mut() - 可变引用
let mut v = vec![1, 2, 3];
for val in v.iter_mut() {
    *val *= 2;
}

// into_iter() - 获取所有权
let v = vec![1, 2, 3];
for val in v.into_iter() {
    println!("{}", val);
}
// v 已无效
```

### Iterator Trait

```rust
pub trait Iterator {
    type Item;  // 关联类型

    fn next(&mut self) -> Option<Self::Item>;

    // 默认实现的方法...
}
```

### 直接使用迭代器

```rust
let v = vec![1, 2, 3];
let mut iter = v.iter();

assert_eq!(iter.next(), Some(&1));
assert_eq!(iter.next(), Some(&2));
assert_eq!(iter.next(), Some(&3));
assert_eq!(iter.next(), None);
```

### IntoIterator

```rust
// 数组
let arr = [1, 2, 3];
for i in arr {
    println!("{}", i);
}

// Range
for i in 0..5 {
    println!("{}", i);
}

for i in 0..=5 {  // 包含 5
    println!("{}", i);
}

// 字符串
let s = "hello";
for c in s.chars() {
    println!("{}", c);
}

// HashMap
use std::collections::HashMap;
let mut map = HashMap::new();
map.insert("a", 1);
for (k, v) in map {
    println!("{}: {}", k, v);
}
```

## 迭代器适配器

### map

```rust
let v = vec![1, 2, 3];

let doubled: Vec<_> = v.iter().map(|x| x * 2).collect();
println!("{:?}", doubled);  // [2, 4, 6]

// 惰性求值
let _ = v.iter().map(|x| {
    println!("processing {}", x);
    x * 2
});
// 上面不会打印任何东西，因为是惰性的
```

### filter

```rust
let v = vec![1, 2, 3, 4, 5, 6];

let evens: Vec<_> = v.iter().filter(|x| *x % 2 == 0).collect();
println!("{:?}", evens);  // [2, 4, 6]

// filter_map - 同时转换和过滤
let strings = vec!["1", "two", "3", "four"];
let numbers: Vec<_> = strings.iter()
    .filter_map(|s| s.parse::<i32>().ok())
    .collect();
println!("{:?}", numbers);  // [1, 3]
```

### filter_map 和 flat_map

```rust
let words = vec!["hello", "world", "rust"];

// filter_map
let first_chars: Vec<_> = words.iter()
    .filter_map(|w| w.chars().next())
    .collect();

// flat_map（展平）
let chars: Vec<_> = words.iter().flat_map(|w| w.chars()).collect();
println!("{:?}", chars);  // ['h', 'e', 'l', 'l', 'o', 'w', 'o', 'r', 'l', 'd', 'r', 'u', 's', 't']
```

### take 和 skip

```rust
let v = vec![1, 2, 3, 4, 5];

let taken: Vec<_> = v.iter().take(3).collect();     // [1, 2, 3]
let skipped: Vec<_> = v.iter().skip(2).collect();  // [3, 4, 5]

// 组合使用
let middle: Vec<_> = v.iter().skip(1).take(3).collect();  // [2, 3, 4]
```

### take_while 和 skip_while

```rust
let v = vec![1, 2, 3, 4, 5];

let taken: Vec<_> = v.iter().take_while(|x| **x < 4).collect();  // [1, 2, 3]
let skipped: Vec<_> = v.iter().skip_while(|x| **x < 3).collect();  // [3, 4, 5]
```

### peekable

```rust
let v = vec![1, 2, 3];
let mut iter = v.iter().peekable();

assert_eq!(iter.peek(), Some(&&1));
assert_eq!(iter.peek(), Some(&&1));
assert_eq!(iter.next(), Some(&1));
```

### enumerate

```rust
let v = vec!["a", "b", "c"];

for (index, value) in v.iter().enumerate() {
    println!("{}: {}", index, value);
}
// 0: a
// 1: b
// 2: c
```

### zip

```rust
let a = vec![1, 2, 3];
let b = vec!['a', 'b', 'c'];

for pair in a.iter().zip(b.iter()) {
    println!("{:?}", pair);
}
// (1, 'a')
// (2, 'b')
// (3, 'c')

// unzip
let pairs = vec![(1, 'a'), (2, 'b'), (3, 'c')];
let (nums, chars): (Vec<_>, Vec<_>) = pairs.into_iter().unzip();
```

### chain

```rust
let a = vec![1, 2];
let b = vec![3, 4];

let combined: Vec<_> = a.iter().chain(b.iter()).collect();
// [1, 2, 3, 4]
```

### cycle

```rust
let v = vec![1, 2];
let mut iter = v.iter().cycle();

println!("{:?}", iter.take(5).collect::<Vec<_>>());
// [1, 2, 1, 2, 1]
```

### rev

```rust
let v = vec![1, 2, 3];

for i in v.iter().rev() {
    println!("{}", i);
}
// 3
// 2
// 1
```

### step_by

```rust
let v = vec![1, 2, 3, 4, 5, 6];

let stepped: Vec<_> = v.iter().step_by(2).collect();  // [1, 3, 5]
```

### flatten

```rust
let nested = vec![vec![1, 2], vec![3, 4], vec![5]];
let flat: Vec<_> = nested.iter().flatten().collect();
// [1, 2, 3, 4, 5]

let strings = vec![Some("hello"), None, Some("world")];
let non_empty: Vec<_> = strings.iter().flatten().collect();
// ["hello", "world"]
```

## 消费者（Consumer）

### collect

```rust
let v = vec![1, 2, 3];

// 收集到 Vec
let vec: Vec<_> = v.iter().map(|x| x * 2).collect();

// 收集到 HashMap
use std::collections::HashMap;
let names = vec!["Alice", "Bob", "Charlie"];
let scores = vec![90, 85, 92];
let map: HashMap<_, _> = names.iter().zip(scores.iter()).collect();
```

### fold 和 reduce

```rust
let v = vec![1, 2, 3, 4, 5];

// fold - 初始值
let sum = v.iter().fold(0, |acc, x| acc + x);
println!("{}", sum);  // 15

let product = v.iter().fold(1, |acc, x| acc * x);
println!("{}", product);  // 120

// reduce - 无初始值
let sum = v.iter().copied().reduce(|acc, x| acc + x);
println!("{:?}", sum);  // Some(15)

// 使用 fold 实现其他操作
let max = v.iter().copied().fold(i32::MIN, |acc, x| acc.max(x));
```

### sum 和 product

```rust
let v = vec![1, 2, 3, 4, 5];

let sum: i32 = v.iter().sum();       // 15
let product: i32 = v.iter().product(); // 120
```

### any 和 all

```rust
let v = vec![1, 2, 3, 4, 5];

let has_even = v.iter().any(|x| x % 2 == 0);  // true
let all_positive = v.iter().all(|x| x > &0); // true
```

### find 和 position

```rust
let v = vec![1, 2, 3, 4, 5];

let first_even = v.iter().find(|x| *x % 2 == 0);  // Some(&2)
let first_neg = v.iter().find(|x| *x < &0);       // None

let pos = v.iter().position(|x| *x == 3);        // Some(2)
let pos = v.iter().position(|x| *x == 10);      // None
```

### max 和 min

```rust
let v = vec![3, 1, 4, 1, 5, 9, 2, 6];

let max = v.iter().max();     // Some(&9)
let min = v.iter().min();     // Some(&1)

// 带 key
let words = vec!["hello", "hi", "hey"];
let longest = words.iter().max_by_key(|w| w.len());  // Some(&"hello")
```

### count

```rust
let v = vec![1, 2, 3, 4, 5];
let count = v.iter().filter(|x| *x % 2 == 0).count();  // 2
```

## 闭包

### 基本语法

```rust
// 完整语法
let add = |a: i32, b: i32| -> i32 { a + b };

// 类型推导
let add = |a, b| a + b;

// 无参数
let get_five = || 5;

// 无返回值
let print = || println!("Hello");

// 块体
let calculate = |x| {
    let doubled = x * 2;
    let tripled = x * 3;
    doubled + tripled
};
```

### 捕获环境

```rust
let x = 4;

// 不可变借用
let equal_to_x = |z| z == x;

// 可变借用
let mut y = 5;
let mut add_to_y = || y += x;
add_to_y();
println!("{}", y);  // 9

// 获取所有权（move）
let z = 10;
let move_closure = move || x + z;  // x 和 z 被移动到闭包
```

### move 闭包

```rust
let s = String::from("hello");

// 不使用 move：闭包借用 s 的引用
let borrow = || println!("{}", s);
// println!("{}", s);  // 仍然有效

// 使用 move：闭包获取 s 的所有权
let take = move || println!("{}", s);
// println!("{}", s);  // 错误：s 已移动
```

### 闭包作为参数

```rust
fn apply<F>(f: F) where F: Fn() {
    f();
}

fn apply_with_return<F, T>(f: F) -> T where F: Fn() -> T {
    f()
}

fn apply_to<T, F>(value: T, f: F) -> T where F: FnOnce(T) -> T {
    f(value)
}
```

### Fn, FnMut, FnOnce

| Trait | 说明 | 要求 |
|-------|------|------|
| FnOnce | 可以调用一次 | 消耗捕获的变量 |
| FnMut | 可变调用 | 修改捕获的变量 |
| Fn | 不可变调用 | 只读访问捕获的变量 |

```rust
fn call<F>(f: F) where F: Fn() {
    f();
}

fn call_mut<F>(mut f: F) where F: FnMut() {
    f();
}

fn call_once<F>(f: F) where F: FnOnce() {
    f();
}
```

### 闭包实现Trait

```rust
struct Container {
    value: Option<i32>,
}

impl Container {
    fn update<F>(&mut self, f: F) where F: FnOnce(i32) -> i32 {
        if let Some(v) = self.value.take() {
            self.value = Some(f(v));
        }
    }
}
```

## 迭代器实战

### 链式调用

```rust
let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

let result = numbers
    .iter()
    .filter(|x| *x % 2 == 0)      // 过滤偶数
    .map(|x| x * x)               // 平方
    .fold(0, |acc, x| acc + x);  // 求和

println!("{}", result);  // 220 (4 + 16 + 36 + 64 + 100)
```

### 搜索和分组

```rust
use std::collections::HashMap;

let words = vec!["apple", "banana", "apricot", "blueberry", "cherry"];

let grouped: HashMap<_, Vec<_>> = words
    .iter()
    .fold(HashMap::new(), |mut acc, word| {
        let first = word.chars().next().unwrap();
        acc.entry(first).or_insert_with(Vec::new).push(word);
        acc
    });

println!("{:?}", grouped);
// {'a': ["apple", "apricot"], 'b': ["banana", "blueberry"], 'c': ["cherry"]}
```

### 生成器模式

```rust
struct Counter {
    count: u32,
    max: u32,
}

impl Counter {
    fn new(max: u32) -> Counter {
        Counter { count: 0, max }
    }
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        if self.count < self.max {
            self.count += 1;
            Some(self.count)
        } else {
            None
        }
    }
}

let counter = Counter::new(5);
let sum: u32 = counter.collect();
println!("{}", sum);  // 15
```

## 资源索引

- 迭代器：https://doc.rust-lang.org/book/ch13-02-iterators.html
- 闭包：https://doc.rust-lang.org/book/ch13-01-closures.html
- Iterator trait：https://doc.rust-lang.org/std/iter/trait.Iterator.html

## 注意事项

- 迭代器是惰性的，需要消费者触发求值
- `for` 循环会自动调用 `into_iter()`
- 闭包默认使用最小捕获原则
- `move` 闭包会获取捕获变量的所有权
- 迭代器适配器返回新迭代器，不消耗原迭代器
- 消费者方法消耗迭代器并产生结果
