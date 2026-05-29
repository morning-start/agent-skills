# 浏览器启动配置参考

本文档详细介绍 ChromiumOptions 浏览器启动配置。

## 创建对象

```python
from DrissionPage import ChromiumOptions

# 默认从 ini 文件读取
co = ChromiumOptions()

# 不读取 ini 文件
co = ChromiumOptions(read_file=False)

# 指定 ini 文件
co = ChromiumOptions(ini_path='./config.ini')
```

---

## 命令行参数

### set_argument()

设置启动参数。

```python
co.set_argument('--start-maximized')
co.set_argument('--window-size', '800,600')
co.set_argument('--guest')
```

### remove_argument()

删除启动参数。

```python
co.remove_argument('--start-maximized')
```

### clear_arguments()

清空所有参数。

```python
co.clear_arguments()
```

---

## 浏览器路径和端口

### set_browser_path()

设置浏览器可执行文件路径。

```python
co.set_browser_path(r'D:\chrome.exe')
```

### set_local_port()

设置本地端口。

```python
co.set_local_port(9333)
```

### set_address()

设置浏览器地址（支持 ws:// 连接）。

```python
co.set_address('127.0.0.1:9333')
co.set_address('ws://127.0.0.1:9333')
```

### auto_port()

自动分配端口和临时用户目录。

```python
co.auto_port(True)              # 启用
co.auto_port(True, scope=(9600, 9700))  # 指定端口范围
```

### set_user_data_path()

设置用户数据目录。

```python
co.set_user_data_path(r'D:\ChromeData')
```

### set_tmp_path()

设置临时文件目录。

```python
co.set_tmp_path(r'D:\tmp')
```

### set_cache_path()

设置缓存目录。

```python
co.set_cache_path(r'D:\cache')
```

### use_system_user_path()

使用系统浏览器用户目录。

```python
co.use_system_user_path(True)
```

### existing_only()

仅使用已启动的浏览器。

```python
co.existing_only(True)
```

---

## 浏览器选项

### headless()

无头模式。

```python
co.headless(True)
```

### incognito()

无痕模式。

```python
co.incognito(True)
```

### mute()

静音。

```python
co.mute(True)
```

### no_imgs()

不加载图片。

```python
co.no_imgs(True)
```

### no_js()

禁用 JavaScript。

```python
co.no_js(True)
```

### new_env()

全新环境。

```python
co.new_env(True)
```

### ignore_certificate_errors()

忽略证书错误。

```python
co.ignore_certificate_errors(True)
```

### set_user_agent()

设置 User-Agent。

```python
co.set_user_agent('Mozilla/5.0...')
```

---

## 代理和下载

### set_proxy()

设置代理。

```python
co.set_proxy('http://localhost:1080')
co.set_proxy('socks5://127.0.0.1:1080')
```

### set_download_path()

设置下载路径。

```python
co.set_download_path(r'D:\downloads')
```

---

## 超时和重试

### set_timeouts()

设置超时时间。

```python
co.set_timeouts(base=10, page_load=30, script=30)
```

### set_retry()

设置重试次数和间隔。

```python
co.set_retry(times=3, interval=1)
```

### set_load_mode()

设置加载模式。

```python
co.set_load_mode('normal')   # 等待所有资源
co.set_load_mode('eager')   # DOM 就绪停止
co.set_load_mode('none')    # 连接成功停止
```

---

## 用户配置

### set_user()

设置用户配置文件夹。

```python
co.set_user('Profile 1')
```

### set_pref()

设置用户首选项。

```python
co.set_pref('profile.default_content_settings.popups', '0')
co.set_pref('credentials_enable_service', False)
```

### remove_pref()

删除用户首选项。

```python
co.remove_pref('profile.default_content_settings.popups')
```

### clear_prefs()

清空所有首选项。

```python
co.clear_prefs()
```

---

## 插件

### add_extension()

添加插件。

```python
co.add_extension(r'D:\SwitchyOmega')
```

### remove_extensions()

移除所有插件。

```python
co.remove_extensions()
```

---

## 实验项

### set_flag()

设置 chrome://flags 实验项。

```python
co.set_flag('temporary-unexpire-flags-m118', '1')
co.set_flag('disable-accelerated-2d-canvas')
```

### clear_flags()

清空实验项。

```python
co.clear_flags()
```

---

## 保存配置

### save()

保存到指定文件。

```python
co.save()
co.save(r'D:\config.ini')
```

### save_to_default()

保存到默认文件。

```python
co.save_to_default()
```

---

## 属性

| 属性 | 说明 |
|------|------|
| `address` | 浏览器地址 |
| `browser_path` | 浏览器路径 |
| `user_data_path` | 用户数据目录 |
| `tmp_path` | 临时目录 |
| `download_path` | 下载路径 |
| `user` | 用户配置 |
| `load_mode` | 加载模式 |
| `timeouts` | 超时设置 |
| `retry_times` | 重试次数 |
| `proxy` | 代理设置 |
| `arguments` | 启动参数列表 |
| `extensions` | 插件列表 |
| `preferences` | 用户首选项 |
| `is_headless` | 是否无头 |
| `is_auto_port` | 是否自动端口 |
| `is_existing_only` | 是否仅使用已启动 |

---

## 常用配置示例

### 基础无头配置

```python
co = ChromiumOptions()
co.headless(True).mute(True)
browser = Chromium(co)
```

### 代理配置

```python
co = ChromiumOptions()
co.set_proxy('http://127.0.0.1:1080')
co.ignore_certificate_errors(True)
```

### 自动端口配置

```python
co = ChromiumOptions()
co.auto_port(True)
co.set_download_path('./downloads')
```

### 自定义用户目录

```python
co = ChromiumOptions()
co.set_user_data_path(r'D:\ChromeData')
co.set_user('Profile 2')
```
