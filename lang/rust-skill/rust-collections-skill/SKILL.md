---
name: rust-collections
description: Rust 集合类型技能，掌握 Vec、String、HashMap、HashSet 等常用集合的创建、操作和性能特点
version: 1.0.0
---

# Rust 集合类型

## 任务目标

- 本 Skill 用于：使用 Rust 标准库集合类型存储和操作数据
- 能力包含：Vec 向量、String 字符串、HashMap 哈希表、HashSet、队列等
- 触发条件：需要存储多个值、字符串处理、键值对映射

## 前置准备

- 完成 rust-core-skill 基础语法
- 理解 Rust 所有权的特殊性

## Vec<T> 向量

### 创建

```rust
let v: Vec<i32> = Vec::new();
let v = vec![1, 2, 3];
let v: Vec<i32> = (0..5).collect();

// 预分配容量
let mut v = Vec::with_capacity(10);
v.push(1);
```

### 添加元素

```rust
let mut v = Vec::new();
v.push(1);
v.push(2);
v.push(3);

// 使用 push 插入
v.insert(0, 0);  // 在索引 0 插入
v.push(4);

// extend 添加多个
v.extend([5, 6, 7]);
v.extend_from_slice(&[8, 9]);
```

### 读取元素

```rust
let v = vec![1, 2, 3, 4, 5];

// 索引访问（越界 panic）
let third = v[2];

// get 方法（返回 Option）
let third = v.get(2);
match third {
    Some(value) => println!("{}", value),
    None => println!("No third element"),
}

// get_or_insert
let fifth = v.get(4).copied().unwrap_or(0);

// 安全的边界访问
let tenth = v.get(9).copied().unwrap_or(0);
```

### 修改元素

```rust
let mut v = vec![1, 2, 3];
v[0] = 10;
v.push(4);

// 修改引用
if let Some(elem) = v.get_mut(1) {
    *elem *= 2;
}
```

### 删除元素

```rust
let mut v = vec![1, 2, 3, 4, 5];

v.pop();         // 移除最后一个：Some(5)
v.remove(1);    // 移除索引 1：3

// 保留满足条件的
v.retain(|x| x % 2 == 0);

// 清空
v.clear();
```

### 遍历

```rust
let v = vec![1, 2, 3];

// 不可变遍历
for i in &v {
    println!("{}", i);
}

// 可变遍历
let mut v = vec![1, 2, 3];
for i in &mut v {
    *i *= 2;
}

// 枚举遍历
for (index, value) in v.iter().enumerate() {
    println!("{}: {}", index, value);
}
```

### 切片

```rust
let v = vec![1, 2, 3, 4, 5];
let slice = &v[1..4];  // [2, 3, 4]
```

### 常用方法

```rust
let v = vec![3, 1, 4, 1, 5, 9, 2, 6];

v.len();           // 长度：8
v.is_empty();      // 是否为空：false
v.contains(&5);    // 是否包含：true
v.first();         // 第一个：Some(&3)
v.last();          // 最后一个：Some(&6)
v.first_mut();     // 可变第一个
v.sort();          // 排序
v.reverse();       // 反转
v.sort_unstable(); // 不稳定排序（更快）
v.dedup();         // 去重相邻元素
```

### VecDeque<T>

```rust
use std::collections::VecDeque;

let mut deque = VecDeque::new();
deque.push_back(1);
deque.push_front(0);  // 从前面插入

deque.pop_front();    // Some(0)
deque.pop_back();    // Some(1)
```

## String 字符串

### 创建

```rust
let s = String::new();
let s = "initial".to_string();
let s = String::from("initial");
let s: String = "hello".chars().collect();

// 从其他类型转换
let n = 42;
let s = n.to_string();
let s = format!("{}", n);
```

### 修改

```rust
let mut s = String::from("hello");

s.push('.');           // 添加字符
s.push_str(" world");  // 添加字符串

// 替换
let s = s.replace("world", "Rust");

// 插入
s.insert(5, ',');

// 移除
s.pop();                    // 移除最后一个字符
if let Some(c) = s.pop() { println!("{}", c); }
```

### 拼接

```rust
let s1 = String::from("Hello, ");
let s2 = String::from("world!");
let s3 = s1 + &s2;  // s1 被移动
println!("{}", s3);

// 多个拼接
let s1 = String::from("tic");
let s2 = String::from("tac");
let s3 = String::from("toe");
let s = format!("{}-{}-{}", s1, s2, s3);
```

### 读取

```rust
let s = String::from("hello world");

// 按字符
for c in s.chars() {
    println!("{}", c);
}

// 按字节
for b in s.bytes() {
    println!("{}", b);
}

// 按单词
for word in s.split_whitespace() {
    println!("{}", word);
}

// split
let fields: Vec<&str> = s.split(',').collect();

// lines
let multiline = "line1\nline2\nline3";
for line in multiline.lines() {
    println!("{}", line);
}

// trim
let s = "  hello  ";
assert_eq!(s.trim(), "hello");

// 获取子串
let s = "hello";
let sub = &s[0..2];  // "he"
let sub = &s[1..4];  // "ell"
```

### 字符串转换

```rust
let n = "42".parse::<i32>().unwrap();
let n: i32 = "42".parse().unwrap();

let s = 42.to_string();
let s = String::from("42");

// 与 str 转换
let s: &str = &string;
let string: String = s.to_string();
```

### 常用方法

```rust
let s = String::from("Hello, world!");

s.len();                    // 字节长度：13
s.is_empty();               // 是否为空：false
s.contains("world");       // 是否包含子串：true
s.starts_with("Hello");    // 是否以某前缀开始：true
s.ends_with("!");          // 是否以某后缀结束：true
s.to_uppercase();          // 转大写
s.to_lowercase();          // 转小写
s.to_ascii_lowercase();    // ASCII 转小写
s.to_ascii_uppercase();    // ASCII 转大写
s.repeat(3);               // 重复
s.chars().count();         // 字符数量：12
```

## HashMap<K, V>

### 创建

```rust
use std::collections::HashMap;

let mut map = HashMap::new();
let mut map: HashMap<&str, i32> = HashMap::new();

// from 数组
let scores = HashMap::from([
    ("Blue", 10),
    ("Yellow", 50),
]);
```

### 添加元素

```rust
let mut map = HashMap::new();

map.insert("Blue", 10);
map.insert("Yellow", 50);

// or_insert：键不存在时插入
map.entry("Green").or_insert(30);

// or_insert_with：键不存在时计算插入
map.entry("Red").or_insert_with(|| {
    println!("Creating Red");
    100
});
```

### 读取元素

```rust
let mut map = HashMap::new();
map.insert("Blue", 10);

// get 返回 Option
match map.get("Blue") {
    Some(value) => println!("{}", value),
    None => println!("Not found"),
}

// get_with 读取或插入默认值
let value = map.get(&"Blue").copied().unwrap_or(0);

// contains_key
if map.contains_key("Blue") {
    println!("Blue exists");
}
```

### 修改元素

```rust
let mut map = HashMap::new();
map.insert("Apple", 3);

// 替换
map.insert("Apple", 5);  // 替换旧值

// 只在键不存在时插入
map.entry("Apple").or_insert(10);  // 不替换

// 修改现有值
if let Some(v) = map.get_mut("Apple") {
    *v += 1;
}

// 使用 entry 修改
*map.entry("Apple").or_insert(0) += 1;
```

### 删除元素

```rust
let mut map = HashMap::new();
map.insert("Blue", 10);

// remove 返回 Option
if let Some(removed) = map.remove("Blue") {
    println!("Removed: {}", removed);
}

// 保留满足条件的
map.retain(|k, v| k.starts_with("B"));
```

### 遍历

```rust
let mut map = HashMap::new();
map.insert("Blue", 10);
map.insert("Yellow", 50);

// 遍历键值对
for (key, value) in &map {
    println!("{}: {}", key, value);
}

// 遍历键
for key in map.keys() {
    println!("{}", key);
}

// 遍历值
for value in map.values() {
    println!("{}", value);
}

// 可变遍历
for value in map.values_mut() {
    *value *= 2;
}
```

### 其他方法

```rust
let map: HashMap<&str, i32> = HashMap::new();

map.len();           // 键值对数量
map.is_empty();      // 是否为空
map.clear();         // 清空
map.capacity();      // 容量
map.contains_key(&"Blue");  // 是否包含键
```

### 自定义哈希函数

```rust
use std::collections::HashMap;
use std::hash::BuildHasherDefault;
use rustc_hash::FxHasher;

let mut map = HashMap::with_hasher(BuildHasherDefault::<FxHasher>::default());
map.insert("Blue", 10);
```

## HashSet<T>

```rust
use std::collections::HashSet;

let mut set = HashSet::new();
set.insert(1);
set.insert(2);
set.insert(3);

set.contains(&1);     // true
set.remove(&2);       // true

// 集合运算
let a: HashSet<i32> = vec![1, 2, 3].into_iter().collect();
let b: HashSet<i32> = vec![2, 3, 4].into_iter().collect();

let union: HashSet<_> = a.union(&b).collect();    // {1, 2, 3, 4}
let intersection: HashSet<_> = a.intersection(&b).collect();  // {2, 3}
let difference: HashSet<_> = a.difference(&b).collect();    // {1}
```

## 其他集合

### BTreeMap 和 BTreeSet

```rust
use std::collections::{BTreeMap, BTreeSet};

// 有序 Map
let mut map = BTreeMap::new();
map.insert("a", 1);
map.insert("b", 2);

// 有序 Set
let mut set = BTreeSet::new();
set.insert(3);
set.insert(1);
set.insert(2);
for elem in &set {
    println!("{}", elem);  // 1, 2, 3
}
```

### BinaryHeap

```rust
use std::collections::BinaryHeap;

let mut heap = BinaryHeap::new();
heap.push(3);
heap.push(1);
heap.push(5);

while let Some(top) = heap.pop() {
    println!("{}", top);  // 5, 3, 1 (最大堆)
}
```

### LinkedList

```rust
use std::collections::LinkedList;

let mut list = LinkedList::new();
list.push_back(1);
list.push_front(0);
list.push_back(2);

println!("{:?}", list);  // [0, 1, 2]
```

## 资源索引

- 集合：https://doc.rust-lang.org/book/ch08-00-common-collections.html
- Vec：https://doc.rust-lang.org/std/vec/struct.Vec.html
- String：https://doc.rust-lang.org/std/string/struct.String.html
- HashMap：https://doc.rust-lang.org/std/collections/struct.HashMap.html

## 注意事项

- String 是 UTF-8 编码，索引操作可能不是字符边界
- 使用 `chars()` 按字符遍历， `bytes()` 按字节遍历
- HashMap 的键需要实现 Hash 和 Eq trait
- 基本类型已实现这些 trait，自定义类型需要 derive
- Vec::new() 推断类型， vec![] 方便创建
