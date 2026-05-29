# Three Tips on Writing File Related Codes

## 目录
1. 使用 pathlib
2. 上下文管理器
3. 文件编码处理
4. 文件路径操作
5. 文件读写最佳实践
6. 临时文件处理
7. 目录操作

## 概览
正确处理文件操作是编写健壮 Python 代码的重要部分。Python 提供了丰富的文件操作功能，应该合理使用。本章基于《One Python Craftsman》第11章内容。

## 1. 使用 pathlib

### 1.1 基本用法
**反模式**：
```python
import os

# 拼接路径
path = os.path.join('folder', 'subfolder', 'file.txt')

# 获取扩展名
ext = os.path.splitext('file.txt')[1]

# 获取文件名
name = os.path.basename('/path/to/file.txt')
```

**Pythonic**：
```python
from pathlib import Path

# 创建路径
path = Path('folder') / 'subfolder' / 'file.txt'

# 获取扩展名
ext = Path('file.txt').suffix  # '.txt'

# 获取文件名
name = Path('/path/to/file.txt').name  # 'file.txt'

# 获取父目录
parent = Path('/path/to/file.txt').parent  # Path('/path/to')
```

### 1.2 路径操作
```python
from pathlib import Path

# 创建路径
path = Path('folder') / 'file.txt'

# 绝对路径
absolute = path.absolute()

# 解析路径
resolved = path.resolve()  # 解析符号链接

# 检查路径
print(path.exists())  # 是否存在
print(path.is_file())  # 是否是文件
print(path.is_dir())  # 是否是目录
```

### 1.3 读写文件
```python
from pathlib import Path

# 读取文件
path = Path('file.txt')
content = path.read_text()  # 读取文本
data = path.read_bytes()  # 读取字节

# 写入文件
path.write_text('Hello, World!')
path.write_bytes(b'Hello, World!')
```

### 1.4 遍历目录
```python
from pathlib import Path

# 遍历目录
path = Path('folder')
for item in path.iterdir():
    if item.is_file():
        print(f'File: {item.name}')
    elif item.is_dir():
        print(f'Directory: {item.name}')

# 递归遍历
for item in path.rglob('*.py'):
    print(f'Python file: {item}')

# 使用 glob
for item in path.glob('*.txt'):
    print(f'Text file: {item}')
```

## 2. 上下文管理器

### 2.1 使用 with 语句
**反模式**：
```python
f = open('file.txt', 'r')
try:
    content = f.read()
finally:
    f.close()
```

**Pythonic**：
```python
with open('file.txt', 'r') as f:
    content = f.read()
```

### 2.2 自动关闭资源
```python
# 文件操作
with open('file.txt', 'r') as f:
    content = f.read()
# 文件自动关闭

# 锁操作
with lock:
    critical_section()

# 数据库连接
with connection.cursor() as cursor:
    cursor.execute('SELECT * FROM users')
    results = cursor.fetchall()
```

### 2.3 自定义上下文管理器
```python
from contextlib import contextmanager

@contextmanager
def file_writer(filename):
    """文件写入器上下文管理器."""
    f = open(filename, 'w')
    try:
        yield f
    finally:
        f.close()

# 使用
with file_writer('output.txt') as f:
    f.write('Hello, World!')
```

## 3. 文件编码处理

### 3.1 明确指定编码
**反模式**：
```python
with open('file.txt', 'r') as f:
    content = f.read()  # 使用系统默认编码
```

**Pythonic**：
```python
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
```

### 3.2 处理编码错误
```python
# 忽略错误
with open('file.txt', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 替换错误
with open('file.txt', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 使用特定编码
with open('file.txt', 'r', encoding='gbk') as f:
    content = f.read()
```

### 3.3 检测编码
```python
import chardet

def detect_encoding(filename):
    """检测文件编码."""
    with open(filename, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

encoding = detect_encoding('file.txt')
with open('file.txt', 'r', encoding=encoding) as f:
    content = f.read()
```

## 4. 文件路径操作

### 4.1 路径拼接
**反模式**：
```python
import os
path = os.path.join('folder', 'subfolder', 'file.txt')
```

**Pythonic**：
```python
from pathlib import Path
path = Path('folder') / 'subfolder' / 'file.txt'
```

### 4.2 路径信息
```python
from pathlib import Path

path = Path('/home/user/documents/file.txt')

print(path.name)  # 'file.txt'
print(path.stem)  # 'file'
print(path.suffix)  # '.txt'
print(path.parent)  # '/home/user/documents'
print(path.parent.name)  # 'documents'
```

### 4.3 路径检查
```python
from pathlib import Path

path = Path('file.txt')

print(path.exists())  # 是否存在
print(path.is_file())  # 是否是文件
print(path.is_dir())  # 是否是目录
print(path.is_absolute())  # 是否是绝对路径
```

### 4.4 创建和删除
```python
from pathlib import Path

# 创建目录
Path('folder').mkdir(exist_ok=True)
Path('folder/subfolder').mkdir(parents=True, exist_ok=True)

# 创建文件
Path('file.txt').touch()

# 删除文件
Path('file.txt').unlink()

# 删除空目录
Path('folder').rmdir()

# 删除非空目录
import shutil
shutil.rmtree('folder')
```

## 5. 文件读写最佳实践

### 5.1 使用 pathlib
```python
from pathlib import Path

# 读取文本
content = Path('file.txt').read_text(encoding='utf-8')

# 写入文本
Path('file.txt').write_text('Hello, World!', encoding='utf-8')

# 读取字节
data = Path('file.bin').read_bytes()

# 写入字节
Path('file.bin').write_bytes(b'Hello, World!')
```

### 5.2 逐行读取大文件
```python
from pathlib import Path

# 方式 1：直接迭代
with Path('large_file.txt').open('r', encoding='utf-8') as f:
    for line in f:
        process(line)

# 方式 2：使用 readlines()（不推荐大文件）
with Path('file.txt').open('r', encoding='utf-8') as f:
    lines = f.readlines()  # 读取所有行到内存
```

### 5.3 写入文件
```python
from pathlib import Path

# 写入文本
with Path('file.txt').open('w', encoding='utf-8') as f:
    f.write('Hello, World!')

# 追加文本
with Path('file.txt').open('a', encoding='utf-8') as f:
    f.write('New line')

# 写入多行
lines = ['Line 1', 'Line 2', 'Line 3']
with Path('file.txt').open('w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
```

### 5.4 使用 csv 模块
```python
import csv
from pathlib import Path

# 读取 CSV
with Path('data.csv').open('r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# 写入 CSV
data = [
    ['Name', 'Age', 'City'],
    ['Alice', 25, 'NYC'],
    ['Bob', 30, 'LA']
]

with Path('output.csv').open('w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)
```

### 5.5 使用 json 模块
```python
import json
from pathlib import Path

# 读取 JSON
with Path('data.json').open('r', encoding='utf-8') as f:
    data = json.load(f)

# 写入 JSON
data = {'name': 'Alice', 'age': 25}
with Path('data.json').open('w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

## 6. 临时文件处理

### 6.1 使用临时文件
```python
import tempfile
from pathlib import Path

# 创建临时文件
with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
    f.write('Temporary content')
    temp_path = Path(f.name)

# 使用临时文件
process_file(temp_path)

# 删除临时文件
temp_path.unlink()
```

### 6.2 使用临时目录
```python
import tempfile
from pathlib import Path

# 创建临时目录
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)
    
    # 在临时目录中操作
    (temp_path / 'file.txt').write_text('Content')
    
    # 临时目录会自动删除
```

### 6.3 使用 shutil 处理文件
```python
import shutil
from pathlib import Path

# 复制文件
shutil.copy('source.txt', 'destination.txt')

# 复制目录
shutil.copytree('source_dir', 'destination_dir')

# 移动文件
shutil.move('old_location.txt', 'new_location.txt')

# 删除目录
shutil.rmtree('directory')
```

## 7. 目录操作

### 7.1 创建目录
```python
from pathlib import Path

# 创建单个目录
Path('folder').mkdir()

# 创建多级目录
Path('folder/subfolder').mkdir(parents=True)

# 忽略已存在的目录
Path('folder').mkdir(exist_ok=True)
```

### 7.2 遍历目录
```python
from pathlib import Path

# 列出目录内容
path = Path('folder')
for item in path.iterdir():
    print(item.name)

# 递归遍历
for item in path.rglob('*'):
    print(item)

# 匹配模式
for item in path.glob('*.txt'):
    print(item)
```

### 7.3 查找文件
```python
from pathlib import Path

# 查找所有 Python 文件
for py_file in Path('.').rglob('*.py'):
    print(py_file)

# 查找特定文件
found = Path('.').rglob('config.py')
for file in found:
    print(file)
```

## 8. 最佳实践

### 8.1 总是使用上下文管理器
```python
# ✅ 好的做法
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# ❌ 不好的做法
f = open('file.txt', 'r', encoding='utf-8')
content = f.read()
f.close()
```

### 8.2 明确指定编码
```python
# ✅ 好的做法
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# ❌ 不好的做法
with open('file.txt', 'r') as f:
    content = f.read()
```

### 8.3 使用 pathlib
```python
# ✅ 好的做法
from pathlib import Path
path = Path('folder') / 'file.txt'

# ❌ 不好的做法
import os
path = os.path.join('folder', 'file.txt')
```

### 8.4 处理文件不存在的情况
```python
from pathlib import Path

path = Path('file.txt')

if path.exists():
    content = path.read_text(encoding='utf-8')
else:
    content = ''
```

### 8.5 异常处理
```python
from pathlib import Path

try:
    with Path('file.txt').open('r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print('File not found')
except PermissionError:
    print('Permission denied')
except UnicodeDecodeError:
    print('Encoding error')
```

## 示例

### 示例 1：完整的文件处理
```python
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

def load_config(config_path: str) -> dict:
    """
    加载配置文件.
    
    Args:
        config_path: 配置文件路径
    
    Returns:
        配置字典
    """
    path = Path(config_path)
    
    # 检查文件是否存在
    if not path.exists():
        logger.error(f'Config file not found: {config_path}')
        return {}
    
    # 检查文件类型
    if path.suffix == '.json':
        try:
            with path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f'Invalid JSON: {e}')
            return {}
    else:
        logger.error(f'Unsupported config file format: {path.suffix}')
        return {}

def save_config(config: dict, config_path: str) -> bool:
    """
    保存配置文件.
    
    Args:
        config: 配置字典
        config_path: 配置文件路径
    
    Returns:
        是否成功
    """
    path = Path(config_path)
    
    try:
        # 确保目录存在
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # 写入文件
        with path.open('w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        logger.error(f'Failed to save config: {e}')
        return False
```

### 示例 2：日志轮转
```python
from pathlib import Path
import gzip
import shutil
import logging

logger = logging.getLogger(__name__)

def rotate_log_file(log_path: str, max_size: int = 10 * 1024 * 1024, max_files: int = 5):
    """
    轮转日志文件.
    
    Args:
        log_path: 日志文件路径
        max_size: 最大文件大小（字节）
        max_files: 最大文件数
    """
    path = Path(log_path)
    
    # 检查文件大小
    if path.exists() and path.stat().st_size >= max_size:
        # 删除最旧的日志
        old_log = path.parent / f'{path.name}.{max_files}'
        if old_log.exists():
            old_log.unlink()
        
        # 轮转日志文件
        for i in range(max_files - 1, 0, -1):
            old_log = path.parent / f'{path.name}.{i}'
            new_log = path.parent / f'{path.name}.{i + 1}'
            if old_log.exists():
                old_log.rename(new_log)
        
        # 压缩当前日志
        compressed = path.parent / f'{path.name}.1'
        with path.open('rb') as f_in:
            with gzip.open(compressed, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # 创建新的日志文件
        path.touch()
```

### 示例 3：批量文件处理
```python
from pathlib import Path
from typing import Callable
import logging

logger = logging.getLogger(__name__)

def process_files(
    directory: str,
    pattern: str,
    processor: Callable[[Path], None]
) -> int:
    """
    批量处理文件.
    
    Args:
        directory: 目录路径
        pattern: 文件匹配模式
        processor: 处理函数
    
    Returns:
        处理的文件数
    """
    path = Path(directory)
    
    if not path.exists():
        logger.error(f'Directory not found: {directory}')
        return 0
    
    count = 0
    for file_path in path.glob(pattern):
        try:
            logger.info(f'Processing: {file_path}')
            processor(file_path)
            count += 1
        except Exception as e:
            logger.error(f'Failed to process {file_path}: {e}')
    
    return count

# 使用
def uppercase_content(file_path: Path):
    """将文件内容转为大写."""
    content = file_path.read_text(encoding='utf-8')
    file_path.write_text(content.upper(), encoding='utf-8')

count = process_files('data', '*.txt', uppercase_content)
print(f'Processed {count} files')
```

### 示例 4：文件监控
```python
from pathlib import Path
import time
import logging

logger = logging.getLogger(__name__)

class FileWatcher:
    """文件监控器."""
    
    def __init__(self, path: str, callback: Callable[[Path], None]):
        self.path = Path(path)
        self.callback = callback
        self.last_mod = 0
    
    def check(self):
        """检查文件变化."""
        if not self.path.exists():
            return
        
        current_mod = self.path.stat().st_mtime
        
        if current_mod != self.last_mod:
            logger.info(f'File changed: {self.path}')
            self.callback(self.path)
            self.last_mod = current_mod
    
    def watch(self, interval: float = 1.0):
        """监控文件."""
        try:
            while True:
                self.check()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info('Stopped watching')

# 使用
def on_file_changed(file_path: Path):
    """文件变化回调."""
    print(f'File {file_path} changed!')
    content = file_path.read_text(encoding='utf-8')
    print(f'Content: {content}')

watcher = FileWatcher('config.json', on_file_changed)
watcher.watch()
```

### 示例 5：安全的文件操作
```python
from pathlib import Path
import tempfile
import shutil
import logging

logger = logging.getLogger(__name__)

def atomic_write(file_path: str, content: str, encoding: str = 'utf-8'):
    """
    原子写入文件.
    
    使用临时文件确保写入的原子性.
    
    Args:
        file_path: 文件路径
        content: 文件内容
        encoding: 文件编码
    """
    path = Path(file_path)
    
    try:
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            encoding=encoding,
            delete=False,
            dir=path.parent
        )
        
        # 写入内容
        temp_file.write(content)
        temp_file.close()
        
        # 原子性替换
        Path(temp_file.name).replace(path)
        
        logger.info(f'Successfully wrote: {file_path}')
    
    except Exception as e:
        # 清理临时文件
        temp_path = Path(temp_file.name)
        if temp_path.exists():
            temp_path.unlink()
        logger.error(f'Failed to write file: {e}')
        raise

def safe_copy(source: str, destination: str):
    """
    安全复制文件.
    
    Args:
        source: 源文件路径
        destination: 目标文件路径
    """
    src_path = Path(source)
    dst_path = Path(destination)
    
    # 确保目标目录存在
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 复制文件
    shutil.copy2(src_path, dst_path)
    
    logger.info(f'Copied {source} to {destination}')
```
