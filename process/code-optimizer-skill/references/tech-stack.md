# 技术栈感知推荐

## 概览

根据不同技术栈，推荐相应的工具链、最佳实践和检测规则。

---

## Python

### 工具链推荐

| 类别 | 工具 | 用途 | 安装命令 |
|------|------|------|----------|
| **类型检查** | mypy | 静态类型检查 | `pip install mypy` |
| **代码质量** | pylint | 代码规范检查 | `pip install pylint` |
| **代码风格** | black | 代码格式化 | `pip install black` |
| **导入排序** | isort | 自动排序 imports | `pip install isort` |
| **安全扫描** | bandit | 安全漏洞检测 | `pip install bandit` |
| **依赖检查** | safety | 依赖漏洞扫描 | `pip install safety` |
| **测试框架** | pytest | 单元测试 | `pip install pytest` |
| **测试覆盖** | coverage.py | 覆盖率统计 | `pip install coverage` |
| **性能分析** | cProfile | 性能剖析 | 内置 |
| **性能分析** | py-spy | 采样分析器 | `pip install py-spy` |

### 最佳实践

#### 1. 类型注解

```python
# ✅ 推荐：完整的类型注解
from typing import List, Optional, Dict

def process_users(
    users: List[Dict[str, any]],
    filter_by: Optional[str] = None
) -> List[Dict[str, any]]:
    """处理用户数据"""
    if filter_by:
        return [u for u in users if u.get('name') == filter_by]
    return users

# ❌ 避免：缺少类型注解
def process_users(users, filter_by=None):
    return users
```

#### 2. 文档字符串

```python
# ✅ 推荐：Google Style Docstring
def calculate_price(
    base_price: float,
    discount: float,
    tax_rate: float
) -> float:
    """
    计算商品最终价格
    
    Args:
        base_price: 基础价格
        discount: 折扣率（0-1）
        tax_rate: 税率（0-1）
    
    Returns:
        最终价格
    
    Raises:
        ValueError: 当折扣率或税率超出范围时
    """
    if not 0 <= discount <= 1:
        raise ValueError("折扣率必须在 0-1 之间")
    
    discounted = base_price * (1 - discount)
    return discounted * (1 + tax_rate)
```

#### 3. 资源管理

```python
# ✅ 推荐：使用上下文管理器
def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# ❌ 避免：忘记关闭文件
def read_file_bad(path: str) -> str:
    f = open(path, 'r')
    content = f.read()
    return content  # 文件未关闭！
```

#### 4. 异常处理

```python
# ✅ 推荐：精确捕获异常
def get_user_data(user_id: int) -> dict:
    try:
        return db.query("SELECT * FROM users WHERE id = ?", user_id)
    except DatabaseError as e:
        logger.error(f"数据库错误：{e}")
        raise
    except ValueError as e:
        logger.error(f"参数错误：{e}")
        raise

# ❌ 避免：过度宽泛的异常
def get_user_data_bad(user_id: int) -> dict:
    try:
        return db.query("...", user_id)
    except:  # 捕获所有异常，包括 KeyboardInterrupt
        pass  # 吞掉异常
```

### 检测规则

| 规则 | 工具 | 配置 |
|------|------|------|
| 类型注解完整 | mypy | `--strict` |
| 函数长度 < 50 行 | pylint | `max-lines=50` |
| 圈复杂度 < 10 | pylint | `max-complexity=10` |
| 文档字符串 | pylint | `missing-docstring` |
| 安全扫描 | bandit | `-r .` |

### 配置文件示例

**pyproject.toml**:

```toml
[tool.black]
line-length = 100
target-version = ['py39']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pylint.messages_control]
disable = "C0114,C0115,C0116"  # 模块/类/函数文档
max-line-length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src"
```

---

## Java

### 工具链推荐

| 类别 | 工具 | 用途 | 依赖坐标 |
|------|------|------|----------|
| **静态检查** | SpotBugs | Bug 检测 | `com.github.spotbugs` |
| **代码质量** | PMD | 代码规范 | `net.sourceforge.pmd` |
| **代码风格** | Checkstyle | 编码规范 | `com.puppycrawl.tools` |
| **代码质量** | SonarQube | 综合质量平台 | SaaS/本地 |
| **性能分析** | VisualVM | JVM 监控 | JDK 自带 |
| **性能分析** | JProfiler | 商业 profiler | 商业软件 |
| **依赖检查** | OWASP Dependency-Check | 依赖漏洞 | `org.owasp` |
| **测试框架** | JUnit 5 | 单元测试 | `org.junit.jupiter` |
| **Mock 框架** | Mockito | Mock 对象 | `org.mockito` |
| **代码覆盖** | JaCoCo | 覆盖率统计 | Maven/Gradle 插件 |

### 最佳实践

#### 1. 空值处理

```java
// ✅ 推荐：使用 Optional
public Optional<User> findUserById(Long id) {
    return Optional.ofNullable(userRepository.findById(id));
}

// 使用
findUserById(1L)
    .map(User::getName)
    .orElse("Unknown");

// ❌ 避免：返回 null
public User findUserById(Long id) {
    return userRepository.findById(id);  // 可能返回 null
}
```

#### 2. 资源管理

```java
// ✅ 推荐：try-with-resources
public String readFile(Path path) throws IOException {
    try (BufferedReader reader = Files.newBufferedReader(path)) {
        return reader.readLine();
    }
}

// ❌ 避免：手动关闭
public String readFileBad(Path path) throws IOException {
    BufferedReader reader = new BufferedReader(
        Files.newBufferedReader(path)
    );
    String line = reader.readLine();
    reader.close();  // 如果 readLine 抛出异常，不会执行
    return line;
}
```

#### 3. 异常处理

```java
// ✅ 推荐：精确异常
public User getUser(Long id) throws UserNotFoundException {
    return userRepository.findById(id)
        .orElseThrow(() -> new UserNotFoundException(id));
}

// ❌ 避免：过度宽泛
public User getUserBad(Long id) throws Exception {
    // 抛出 Exception，调用方难以处理
}
```

#### 4. 集合处理

```java
// ✅ 推荐：使用 Stream API
List<String> names = users.stream()
    .filter(u -> u.getAge() >= 18)
    .map(User::getName)
    .collect(Collectors.toList());

// ✅ 推荐：使用 computeIfAbsent
Map<String, List<User>> usersByCity = new HashMap<>();
users.forEach(user -> 
    usersByCity.computeIfAbsent(
        user.getCity(), 
        k -> new ArrayList<>()
    ).add(user)
);

// ❌ 避免：手动检查
if (!map.containsKey(key)) {
    map.put(key, new ArrayList<>());
}
map.get(key).add(item);
```

### 检测规则

| 规则 | 工具 | 配置 |
|------|------|------|
| Bug 检测 | SpotBugs | Maven/Gradle 插件 |
| 代码规范 | PMD | rulesets/java/bestpractices.xml |
| 代码风格 | Checkstyle | Google/Sun 规范 |
| 代码质量 | SonarQube | Quality Gate |
| 依赖漏洞 | OWASP DC | 定期扫描 |

### 配置文件示例

**pom.xml**:

```xml
<build>
    <plugins>
        <!-- SpotBugs -->
        <plugin>
            <groupId>com.github.spotbugs</groupId>
            <artifactId>spotbugs-maven-plugin</artifactId>
            <version>4.7.3.0</version>
        </plugin>
        
        <!-- PMD -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-pmd-plugin</artifactId>
            <version>3.19.0</version>
        </plugin>
        
        <!-- Checkstyle -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-checkstyle-plugin</artifactId>
            <version>3.2.0</version>
            <configuration>
                <configLocation>google_checks.xml</configLocation>
            </configuration>
        </plugin>
        
        <!-- JaCoCo -->
        <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.8</version>
        </plugin>
    </plugins>
</build>
```

---

## JavaScript/TypeScript

### 工具链推荐

| 类别 | 工具 | 用途 | 安装命令 |
|------|------|------|----------|
| **Linting** | ESLint | 代码规范 | `npm i -D eslint` |
| **格式化** | Prettier | 代码格式化 | `npm i -D prettier` |
| **类型检查** | TypeScript | 静态类型 | `npm i -D typescript` |
| **性能分析** | Chrome DevTools | 浏览器性能 | 浏览器内置 |
| **性能分析** | Lighthouse | Web 性能 | `npm i -g lighthouse` |
| **安全扫描** | npm audit | 依赖漏洞 | npm 内置 |
| **安全扫描** | Snyk | 综合安全 | `npm i -g snyk` |
| **测试框架** | Jest | 单元测试 | `npm i -D jest` |
| **测试框架** | Vitest | Vite 测试 | `npm i -D vitest` |
| **E2E 测试** | Playwright | 端到端测试 | `npm i -D playwright` |

### 最佳实践

#### 1. 类型安全

```typescript
// ✅ 推荐：严格的类型定义
interface User {
    id: number;
    name: string;
    email: string;
    age?: number;  // 可选属性
}

function greetUser(user: User): string {
    return `Hello, ${user.name}!`;
}

// ✅ 推荐：使用类型守卫
function isUser(data: unknown): data is User {
    return (
        typeof data === 'object' &&
        data !== null &&
        'id' in data &&
        'name' in data
    );
}

// ❌ 避免：使用 any
function greetUserBad(user: any): string {
    return `Hello, ${user.name}!`;  // 类型不安全
}
```

#### 2. 异步处理

```typescript
// ✅ 推荐：async/await + 错误处理
async function fetchUserData(userId: number): Promise<User> {
    try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('获取用户失败:', error);
        throw error;
    }
}

// ✅ 推荐：Promise.all 并发请求
async function fetchMultipleUsers(ids: number[]): Promise<User[]> {
    const promises = ids.map(id => fetchUserData(id));
    return await Promise.all(promises);
}

// ❌ 避免：串行请求
async function fetchMultipleUsersBad(ids: number[]): Promise<User[]> {
    const results: User[] = [];
    for (const id of ids) {
        const user = await fetchUserData(id);  // 串行
        results.push(user);
    }
    return results;
}
```

#### 3. 空值处理

```typescript
// ✅ 推荐：可选链 + 空值合并
const userName = user?.profile?.name ?? 'Anonymous';

// ✅ 推荐：类型断言
if (user && 'profile' in user) {
    const name = user.profile.name;
}

// ❌ 避免：多重检查
let userName: string;
if (user !== null && user !== undefined) {
    if (user.profile !== null && user.profile !== undefined) {
        userName = user.profile.name;
    } else {
        userName = 'Anonymous';
    }
} else {
    userName = 'Anonymous';
}
```

#### 4. 不可变性

```typescript
// ✅ 推荐：使用 const
const MAX_RETRIES = 3;
const config = { timeout: 5000 };

// ✅ 推荐：不可变更新
const updatedUser = { ...user, name: 'New Name' };
const filteredItems = items.filter(item => item.active);

// ❌ 避免：直接修改
let maxRetries = 3;  // 可能被修改
config.timeout = 10000;  // 直接修改
items.push(newItem);  // 直接修改数组
```

### 检测规则

| 规则 | 工具 | 配置 |
|------|------|------|
| 代码规范 | ESLint | eslint-config-airbnb |
| TypeScript | ESLint | @typescript-eslint/recommended |
| 格式化 | Prettier | .prettierrc |
| 类型严格 | TypeScript | tsconfig.json strict: true |
| 安全扫描 | npm audit | `npm audit` |

### 配置文件示例

**.eslintrc.js**:

```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
  ],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  rules: {
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/explicit-function-return-type': 'error',
    'no-console': 'warn',
  },
};
```

**tsconfig.json**:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

---

## Go

### 工具链推荐

| 类别 | 工具 | 用途 | 安装命令 |
|------|------|------|----------|
| **代码质量** | golangci-lint | 综合 lint 工具 | `go install golangci-lint` |
| **代码格式** | gofmt | 代码格式化 | Go 内置 |
| **导入排序** | goimports | 自动整理 imports | `go install golang.org/x/tools/cmd/goimports` |
| **安全扫描** | gosec | 安全漏洞检测 | `go install github.com/securego/gosec` |
| **漏洞检查** | govulncheck | 依赖漏洞扫描 | `go install golang.org/x/vuln/cmd/govulncheck` |
| **性能分析** | pprof | 性能剖析 | Go 内置 |
| **性能分析** | trace | 执行追踪 | Go 内置 |
| **测试框架** | testing | 单元测试 | Go 内置 |
| **Mock 框架** | gomock | Mock 生成 | `go install github.com/golang/mock/mockgen` |
| **基准测试** | testing | 性能测试 | Go 内置 |

### 最佳实践

#### 1. 错误处理

```go
// ✅ 推荐：显式错误处理
func getUser(id int) (*User, error) {
    if id <= 0 {
        return nil, fmt.Errorf("invalid id: %d", id)
    }
    
    user, err := db.Query(id)
    if err != nil {
        return nil, fmt.Errorf("query user: %w", err)
    }
    
    return user, nil
}

// 使用
user, err := getUser(1)
if err != nil {
    log.Printf("获取用户失败：%v", err)
    return
}

// ❌ 避免：忽略错误
func getUserBad(id int) *User {
    user, _ := db.Query(id)  // 忽略错误
    return user
}
```

#### 2. 资源管理

```go
// ✅ 推荐：defer 关闭
func readFile(path string) (string, error) {
    file, err := os.Open(path)
    if err != nil {
        return "", err
    }
    defer file.Close()  // 确保关闭
    
    return io.ReadAll(file)
}

// ✅ 推荐：HTTP 请求
func fetchData(url string) ([]byte, error) {
    resp, err := http.Get(url)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    return io.ReadAll(resp.Body)
}
```

#### 3. 并发模式

```go
// ✅ 推荐：带超时的并发
func fetchAll(ctx context.Context, urls []string) ([]string, error) {
    var (
        wg  sync.WaitGroup
        mu sync.Mutex
        results []string
        errChan = make(chan error, len(urls))
    )
    
    for _, url := range urls {
        wg.Add(1)
        go func(url string) {
            defer wg.Done()
            
            ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
            defer cancel()
            
            resp, err := http.GetContext(ctx, url)
            if err != nil {
                errChan <- err
                return
            }
            defer resp.Body.Close()
            
            data, _ := io.ReadAll(resp.Body)
            mu.Lock()
            results = append(results, string(data))
            mu.Unlock()
        }(url)
    }
    
    wg.Wait()
    close(errChan)
    
    // 返回第一个错误
    if err := <-errChan; err != nil {
        return nil, err
    }
    
    return results, nil
}
```

#### 4. 接口设计

```go
// ✅ 推荐：小接口
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// ✅ 推荐：接收者命名一致
func (u *User) Validate() error {
    // ...
}

func (u *User) Save() error {
    // ...
}

// ❌ 避免：大接口
type BadInterface interface {
    Method1()
    Method2()
    Method3()
    // ... 20 个方法
}
```

### 检测规则

| 规则 | 工具 | 配置 |
|------|------|------|
| 综合 lint | golangci-lint | `.golangci.yml` |
| 安全扫描 | gosec | `-exclude-dir=vendor` |
| 漏洞检查 | govulncheck | `./...` |
| 代码格式 | gofmt | `gofmt -w .` |

### 配置文件示例

**.golangci.yml**:

```yaml
run:
  timeout: 5m
  tests: true

linters:
  enable:
    - govet
    - errcheck
    - staticcheck
    - unused
    - gosimple
    - structcheck
    - varcheck
    - ineffassign
    - deadcode
    - typecheck
  disable-all: true

linters-settings:
  errcheck:
    check-blank: true
  govet:
    check-shadowing: true

issues:
  exclude-use-default: false
  exclude-rules:
    - path: _test\.go
      linters:
        - errcheck
```

---

## 跨语言通用建议

### 1. 版本控制

- 使用语义化版本（Semantic Versioning）
- 提交信息规范化（Conventional Commits）
- 分支策略（Git Flow / GitHub Flow）

### 2. 文档

- README 必备（项目说明、快速开始）
- API 文档（OpenAPI/Swagger）
- 变更日志（CHANGELOG.md）

### 3. CI/CD

- 自动化测试（每次提交）
- 代码质量检查（PR 门禁）
- 自动化部署（CD 流水线）

### 4. 监控

- 日志记录（结构化日志）
- 指标监控（Prometheus/Grafana）
- 链路追踪（Jaeger/Zipkin）

---

## 参考资源

- **Python**: The Python Guide, Real Python
- **Java**: Effective Java, Oracle Java Docs
- **JavaScript**: You Don't Know JS, MDN Web Docs
- **Go**: Effective Go, Go Blog
- **通用**: Clean Code, The Pragmatic Programmer
