---
name: rust-cli-project
description: Rust CLI 项目开发技能，掌握命令行参数解析、文件操作、环境变量、错误处理和项目组织
version: 1.0.0
---

# Rust CLI 项目开发

## 任务目标

- 本 Skill 用于：构建命令行工具和应用
- 能力包含：参数解析、文件操作、环境变量、错误处理、子命令、进度显示
- 触发条件：需要构建 CLI 工具、处理命令行输入、文件批处理

## 前置准备

- 完成 rust-core-skill, rust-error-handling-skill, rust-cargo-skill
- 安装 clap：`cargo add clap --features derive`

## 参数解析

### 使用 clap (推荐)

```rust
use clap::Parser;

#[derive(Parser, Debug)]
#[command(name = "myapp")]
#[command(about = "A simple CLI application", long_about = None)]
struct Args {
    /// Input file to process
    #[arg(short, long)]
    input: String,

    /// Output file
    #[arg(short, long, default_value = "output.txt")]
    output: String,

    /// Enable verbose mode
    #[arg(short, long, action = clap::ArgAction::SetTrue)]
    verbose: bool,

    /// Number of iterations
    #[arg(short, long, default_value_t = 1)]
    count: u32,
}

fn main() {
    let args = Args::parse();
    println!("{:?}", args);
}
```

### 子命令

```rust
use clap::{Parser, Subcommand};

#[derive(Parser, Debug)]
#[command(name = "git")]
#[command(subcommandvalue_name = "COMMAND")]
#[command(arg_required_else_help = true)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Clone a repository
    Clone {
        /// Repository URL
        #[arg(value_name = "REPO")]
        repo: String,
    },
    /// Add files
    Add {
        /// Files to add
        #[arg(required = true)]
        files: Vec<String>,
    },
    /// Commit changes
    Commit {
        /// Commit message
        #[arg(short, long)]
        message: String,
    },
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Clone { repo } => {
            println!("Cloning {}", repo);
        }
        Commands::Add { files } => {
            println!("Adding {:?}", files);
        }
        Commands::Commit { message } => {
            println!("Committing: {}", message);
        }
    }
}
```

### 位置参数

```rust
use clap::Parser;

#[derive(Parser, Debug)]
struct Args {
    /// Files to process
    #[arg(required = true)]
    files: Vec<PathBuf>,

    /// Output directory
    #[arg(value_name = "DIR")]
    output: Option<PathBuf>,
}
```

### 枚举值

```rust
use clap::Parser;

#[derive(Parser, Debug)]
#[command]
struct Args {
    /// Output format
    #[arg(value_enum, short, long, default_value = "text")]
    format: OutputFormat,
}

#[derive(Debug, Clone, ValueEnum)]
enum OutputFormat {
    Json,
    Xml,
    Text,
}
```

### 必选参数

```rust
use clap::Parser;

#[derive(Parser, Debug)]
struct Args {
    /// Required argument
    #[arg(required = true)]
    name: String,

    /// Optional argument
    #[arg(required = false)]
    value: Option<i32>,
}
```

## 文件操作

### 读取文件

```rust
use std::fs;
use std::io;
use std::path::Path;

fn read_file(path: &Path) -> io::Result<String> {
    fs::read_to_string(path)
}

fn main() -> io::Result<()> {
    let content = read_file(Path::new("file.txt"))?;
    println!("{}", content);
    Ok(())
}
```

### 写入文件

```rust
use std::fs::File;
use std::io::{self, Write};
use std::path::Path;

fn write_file(path: &Path, content: &str) -> io::Result<()> {
    let mut file = File::create(path)?;
    file.write_all(content.as_bytes())?;
    Ok(())
}

fn main() -> io::Result<()> {
    write_file(Path::new("output.txt"), "Hello, world!")?;
    Ok(())
}
```

### 遍历目录

```rust
use std::fs;
use std::path::Path;

fn list_files(dir: &Path) -> io::Result<Vec<fs::DirEntry>> {
    let mut entries = Vec::new();
    for entry in fs::read_dir(dir)? {
        let entry = entry?;
        entries.push(entry);
    }
    Ok(entries)
}

fn main() -> io::Result<()> {
    for entry in list_files(Path::new("."))? {
        let path = entry.path();
        if path.is_file() {
            println!("File: {:?}", path);
        } else if path.is_dir() {
            println!("Dir: {:?}", path);
        }
    }
    Ok(())
}
```

### glob 模式匹配

```rust
// Cargo.toml
// glob = "0.3"

use glob::glob;

fn main() {
    for entry in glob("src/**/*.rs").unwrap() {
        println!("{:?}", entry);
    }
}
```

## 环境变量

### 读取环境变量

```rust
use std::env;

fn main() {
    // 读取单个变量
    let home = env::var("HOME").unwrap_or_else(|_| {
        println!("HOME not set, using /tmp");
        "/tmp".to_string()
    });

    // 检查变量是否存在
    if env::var("DEBUG").is_ok() {
        println!("Debug mode enabled");
    }

    // 设置默认值
    let port = env::var("PORT").unwrap_or_else(|_| "8080".to_string());

    // 解析为数字
    let timeout: u64 = env::var("TIMEOUT")
        .unwrap_or_else(|_| "30".to_string())
        .parse()
        .unwrap_or(30);

    println!("Home: {}", home);
    println!("Port: {}", port);
    println!("Timeout: {}", timeout);
}
```

### 设置环境变量

```rust
use std::env;

fn main() {
    env::set_var("MY_VAR", "value");
    println!("{}", env::var("MY_VAR").unwrap());
}
```

### 环境变量作为配置

```rust
use serde::{Deserialize};
use std::env;

#[derive(Debug, Deserialize)]
struct Config {
    database_url: String,
    port: u16,
    debug: bool,
}

impl Config {
    fn from_env() -> Result<Self, env::VarError> {
        Ok(Config {
            database_url: env::var("DATABASE_URL")?,
            port: env::var("PORT")?.parse().unwrap_or(8080),
            debug: env::var("DEBUG").unwrap_or_default() == "1",
        })
    }
}
```

## 标准错误输出

```rust
use std::io::{self, Write};

fn main() {
    // 标准输出
    println!("This is stdout");

    // 标准错误
    eprintln!("This is stderr");

    // 写入 stderr
    writeln!(io::stderr(), "Error: something went wrong").unwrap();
}
```

## 进度显示

### 简单进度

```rust
use std::io::{self, Write};

fn process_items(items: &[i32]) {
    let len = items.len();
    for (i, item) in items.iter().enumerate() {
        print!("\rProcessing {}/{}: {}", i + 1, len, item);
        io::stdout().flush().unwrap();
        std::thread::sleep(std::time::Duration::from_millis(100));
    }
    println!();  // 换行
}

fn main() {
    process_items(&vec![1, 2, 3, 4, 5]);
}
```

### 进度条库

```rust
// Cargo.toml
//indicatif = "0.17"

use std::time::Duration;
use std::thread::sleep;

fn main() {
    let pb = indicatif::ProgressBar::new(100);
    pb.set_style(
        indicatif::ProgressStyle::default_bar()
            .template("[{elapsed_precise}] {bar:40} {pos}/{len} ({eta})")
            .unwrap()
            .progress_chars("##-"),
    );

    for _ in 0..100 {
        pb.inc(1);
        sleep(Duration::from_millis(50));
    }

    pb.finish_with_message("Done!");
}
```

## 结构化输出

### JSON 输出

```rust
// Cargo.toml
//serde_json = "1.0"

use serde::{Serialize};
use std::io;

#[derive(Serialize)]
struct Output {
    status: String,
    count: usize,
    items: Vec<String>,
}

fn main() -> io::Result<()> {
    let output = Output {
        status: "success".to_string(),
        count: 3,
        items: vec!["a".to_string(), "b".to_string(), "c".to_string()],
    };

    let json = serde_json::to_string_pretty(&output).unwrap();
    println!("{}", json);
    Ok(())
}
```

### 输出格式切换

```rust
use clap::Parser;
use serde::{Deserialize, Serialize};

#[derive(Parser, Debug)]
struct Args {
    #[arg(short, long, default_value = "text")]
    format: OutputFormat,
}

#[derive(Debug, Clone, ValueEnum)]
enum OutputFormat {
    Text,
    Json,
    Csv,
}

#[derive(Serialize)]
struct Result {
    name: String,
    value: i32,
}

fn main() {
    let args = Args::parse();

    let results = vec![
        Result { name: "a".to_string(), value: 1 },
        Result { name: "b".to_string(), value: 2 },
    ];

    match args.format {
        OutputFormat::Json => {
            println!("{}", serde_json::to_string_pretty(&results).unwrap());
        }
        OutputFormat::Csv => {
            for r in &results {
                println!("{},{}", r.name, r.value);
            }
        }
        OutputFormat::Text => {
            for r in &results {
                println!("{}: {}", r.name, r.value);
            }
        }
    }
}
```

## 错误处理

### 自定义错误类型

```rust
use std::fmt;
use std::io;

#[derive(Debug)]
enum CliError {
    Io(io::Error),
    Parse(std::num::ParseIntError),
    InvalidInput(String),
}

impl fmt::Display for CliError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            CliError::Io(e) => write!(f, "IO error: {}", e),
            CliError::Parse(e) => write!(f, "Parse error: {}", e),
            CliError::InvalidInput(msg) => write!(f, "Invalid input: {}", msg),
        }
    }
}

impl From<io::Error> for CliError {
    fn from(e: io::Error) -> Self {
        CliError::Io(e)
    }
}

impl From<std::num::ParseIntError> for CliError {
    fn from(e: std::num::ParseIntError) -> Self {
        CliError::Parse(e)
    }
}
```

### 错误处理策略

```rust
use std::fs;
use std::io;
use std::path::Path;

type Result<T> = std::result::Result<T, CliError>;

fn process_file(path: &Path) -> Result<String> {
    if !path.exists() {
        return Err(CliError::InvalidInput(format!("{:?} not found", path)));
    }

    let content = fs::read_to_string(path)?;
    Ok(content)
}

fn main() {
    match process_file(Path::new("nonexistent.txt")) {
        Ok(content) => println!("{}", content),
        Err(e) => {
            eprintln!("Error: {}", e);
            std::process::exit(1);
        }
    }
}
```

## 子命令模式

### 独立子命令程序

```rust
// src/main.rs
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "tool")]
#[command(subcommand)]
enum Command {
    Init(InitArgs),
    Build(BuildArgs),
    Run(RunArgs),
}

#[derive(Parser)]
struct InitArgs {
    #[arg(default_value = ".")]
    path: std::path::PathBuf,
}

#[derive(Parser)]
struct BuildArgs {
    #[arg(short, long)]
    release: bool,
}

#[derive(Parser)]
struct RunArgs {
    #[arg(short, long)]
    debug: bool,
}

fn main() {
    let cmd = Command::parse();

    match cmd {
        Command::Init(args) => {
            println!("Initializing at {:?}", args.path);
        }
        Command::Build(args) => {
            println!("Building (release: {})", args.release);
        }
        Command::Run(args) => {
            println!("Running (debug: {})", args.debug);
        }
    }
}
```

## 项目组织

### 典型 CLI 项目结构

```
my-cli/
├── src/
│   ├── main.rs        # 入口
│   ├── cli.rs         # CLI 参数解析
│   ├── commands/      # 子命令
│   │   ├── mod.rs
│   │   ├── init.rs
│   │   ├── build.rs
│   │   └── run.rs
│   ├── config.rs      # 配置
│   └── error.rs       # 错误类型
├── Cargo.toml
└── README.md
```

### 模块化示例

```rust
// src/main.rs
mod cli;
mod commands;
mod config;
mod error;

use clap::Parser;

fn main() {
    let cli = cli::Cli::parse();

    if let Err(e) = run(cli) {
        eprintln!("Error: {}", e);
        std::process::exit(1);
    }
}

fn run(cli: cli::Cli) -> Result<(), error::Error> {
    match cli.command {
        cli::Commands::Init(args) => commands::init::execute(args),
        cli::Commands::Build(args) => commands::build::execute(args),
        cli::Commands::Run(args) => commands::run::execute(args),
    }
}
```

## 日志

### 简单日志

```rust
use std::env;

fn log(level: &str, msg: &str) {
    if env::var("RUST_LOG").ok().map(|s| s.as_str()) == Some(level) {
        eprintln!("[{}] {}", level.to_uppercase(), msg);
    }
}

fn main() {
    env::set_var("RUST_LOG", "info");
    log("info", "Starting application");
    log("debug", "Debug info");
}
```

### 第三方日志库

```rust
// Cargo.toml
//env_logger = "0.10"
//log = "0.4"

use log::{info, error, warn};

fn main() {
    env_logger::Builder::from_env(env_logger::Env::default().default_filter_or("info")).init();

    info!("Starting application");
    warn!("This is a warning");
    error!("This is an error");
}
```

## 资源索引

- clap 文档：https://docs.rs/clap
- 常用 CLI 库：https://github.com/clap-rs/clap
- 错误处理：https://doc.rust-lang.org/book/ch09-00-error-handling.html
- 环境变量：https://doc.rust-lang.org/book/ch12-05-working-with-environment-variables.html

## 注意事项

- 使用 clap derive 简化参数解析
- 区分标准输出和标准错误
- 提供清晰的错误消息
- 支持配置文件和环境变量
- 提供 `--help` 和 `--version`
- 使用结构化输出便于脚本处理
- 处理 Ctrl+C 中断
- 返回适当的退出码
