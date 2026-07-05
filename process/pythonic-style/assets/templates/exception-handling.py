"""
Exception Handling Templates

Common Pythonic patterns for exception handling.
"""

# Template 1: Basic Try-Except
def divide(a, b):
    """基本异常处理."""
    try:
        return a / b
    except ZeroDivisionError:
        return None

# Template 2: Multiple Exception Types
def process_data(data):
    """多个异常类型."""
    try:
        result = validate_and_process(data)
        return result
    except ValueError as e:
        logger.error(f'Validation error: {e}')
    except TypeError as e:
        logger.error(f'Type error: {e}')
    except Exception as e:
        logger.exception('Unexpected error')
        raise

# Template 3: Try-Except-Else-Finally
def read_file(filename):
    """完整的异常处理."""
    try:
        with open(filename) as f:
            content = f.read()
    except FileNotFoundError:
        logger.error(f'File not found: {filename}')
        return None
    else:
        return content.strip()
    finally:
        logger.info('File operation completed')

# Template 4: Custom Exception
class ValidationError(Exception):
    """验证错误."""
    pass

class AuthenticationError(Exception):
    """认证错误."""
    pass

def validate_user_data(data):
    """自定义异常."""
    if not data.get('name'):
        raise ValidationError('Name is required')
    if not data.get('email'):
        raise ValidationError('Email is required')

# Template 5: Exception with Context
def process_with_context(data):
    """异常上下文."""
    try:
        result = process(data)
    except ValueError as e:
        raise ProcessingError('Failed to process data') from e

# Template 6: Re-raising Exceptions
def handle_exception():
    """重新抛出异常."""
    try:
        risky_operation()
    except Exception as e:
        logger.error(f'Error occurred: {e}')
        raise  # 重新抛出原始异常

# Template 7: Exception Logging
def safe_operation():
    """异常日志记录."""
    try:
        result = operation()
        return result
    except Exception as e:
        logger.exception('Operation failed')
        raise

# Template 8: Silent Fail with Warning
def optional_operation():
    """静默失败并警告."""
    try:
        return operation()
    except Exception as e:
        logger.warning(f'Optional operation failed: {e}')
        return None

# Template 9: Retry Logic
def retry_operation(max_attempts=3, delay=1):
    """重试逻辑."""
    import time
    
    for attempt in range(max_attempts):
        try:
            return operation()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            time.sleep(delay)
    return None

# Template 10: Context Manager for Resources
class Resource:
    """资源上下文管理器."""
    
    def __enter__(self):
        self.resource = acquire_resource()
        return self.resource
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.resource.rollback()
        else:
            self.resource.commit()
        self.resource.close()
        return False

with Resource() as resource:
    process(resource)

# Template 11: Exception Chaining
def chain_exceptions():
    """异常链."""
    try:
        risky_operation()
    except ValueError as e:
        raise CustomError('Custom error message') from e

# Template 12: Catching Base Exception
def handle_all_exceptions():
    """捕获所有异常（谨慎使用）."""
    try:
        operation()
    except Exception as e:
        logger.exception('Caught exception')
        # 处理异常
    finally:
        cleanup()

# Template 13: Specific Error Messages
def calculate_discount(price, discount_rate):
    """具体的错误消息."""
    if price is None:
        raise ValueError('Price cannot be None')
    if price < 0:
        raise ValueError(f'Price cannot be negative: {price}')
    if not 0 <= discount_rate <= 1:
        raise ValueError(
            f'Discount rate must be between 0 and 1: {discount_rate}'
        )
    return price * (1 - discount_rate)

# Template 14: Exception with Attributes
class InsufficientFundsError(Exception):
    """余额不足错误."""
    
    def __init__(self, required, available):
        self.required = required
        self.available = available
        super().__init__(
            f'Insufficient funds: required {required}, available {available}'
        )

# Template 15: Assert for Debugging
def debug_assertion(value, condition):
    """断言（仅用于调试）."""
    assert condition, f'Assertion failed: {value}'
    return value

# Template 16: Graceful Degradation
def get_user_info(user_id):
    """优雅降级."""
    try:
        return fetch_user_from_api(user_id)
    except APIError:
        logger.warning('API error, using cache')
        return fetch_user_from_cache(user_id)
    except Exception as e:
        logger.error(f'Failed to get user info: {e}')
        return {'id': user_id, 'name': 'Unknown'}

# Template 17: Validation Pattern
def validate_input(data, schema):
    """验证模式."""
    errors = []
    
    for field, validators in schema.items():
        value = data.get(field)
        
        for validator in validators:
            try:
                if not validator(value):
                    errors.append(f'Invalid {field}')
            except Exception as e:
                errors.append(f'{field}: {e}')
    
    if errors:
        raise ValidationError('; '.join(errors))
    
    return data

# Template 18: Exception Handling in Loops
def process_items(items):
    """循环中的异常处理."""
    results = []
    errors = []
    
    for item in items:
        try:
            result = process_item(item)
            results.append(result)
        except Exception as e:
            errors.append({
                'item': item,
                'error': str(e)
            })
            logger.error(f'Failed to process {item}: {e}')
    
    return {'results': results, 'errors': errors}

# Template 19: Timeout Handler
def with_timeout(func, timeout=30):
    """超时处理."""
    import signal
    
    def handler(signum, frame):
        raise TimeoutError(f'Function timed out after {timeout} seconds')
    
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    
    try:
        result = func()
    finally:
        signal.alarm(0)
    
    return result

# Template 20: Resource Cleanup Pattern
def process_with_cleanup():
    """资源清理模式."""
    resource1 = None
    resource2 = None
    
    try:
        resource1 = acquire_resource1()
        resource2 = acquire_resource2()
        
        result = process_resources(resource1, resource2)
        return result
    
    except Exception as e:
        logger.error(f'Processing failed: {e}')
        raise
    
    finally:
        if resource2:
            resource2.close()
        if resource1:
            resource1.close()

# Template 21: Context Manager from Generator
from contextlib import contextmanager

@contextmanager
def temp_file(content):
    """临时文件上下文管理器."""
    import tempfile
    fd, path = tempfile.mkstemp()
    
    try:
        with open(path, 'w') as f:
            f.write(content)
        yield path
    finally:
        import os
        os.close(fd)
        os.unlink(path)

# Template 22: Exception Wrapper
def handle_errors(func):
    """异常处理装饰器."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.error(f'Value error in {func.__name__}: {e}')
            raise
        except Exception as e:
            logger.exception(f'Unexpected error in {func.__name__}')
            raise RuntimeError(f'Operation failed: {e}')
    
    return wrapper

# Template 23: Batch Processing with Error Handling
def process_batch(items, batch_size=10):
    """批量处理."""
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        
        try:
            batch_result = process_batch_items(batch)
            results.extend(batch_result)
        except Exception as e:
            logger.error(f'Failed to process batch {i//batch_size}: {e}')
            results.extend([None] * len(batch))
    
    return results

# Template 24: Fallback Strategy
def get_config(key, fallback=None):
    """回退策略."""
    # 尝试从环境变量获取
    value = os.getenv(key.upper())
    if value:
        return value
    
    # 尝试从配置文件获取
    try:
        with open('config.json') as f:
            config = json.load(f)
            return config.get(key)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    
    # 使用回退值
    if fallback is not None:
        return fallback
    
    raise ValueError(f'Configuration key not found: {key}')

# Template 25: Exception with Recovery
def operation_with_recovery():
    """可恢复的异常处理."""
    try:
        return primary_operation()
    except PrimaryError:
        logger.info('Primary operation failed, trying fallback')
        try:
            return fallback_operation()
        except Exception as e:
            logger.error('Fallback also failed')
            raise

# Template 26: Validation with Custom Exceptions
class TooYoungError(Exception):
    """年龄太小错误."""
    pass

class TooOldError(Exception):
    """年龄太大错误."""
    pass

def validate_age(age):
    """年龄验证."""
    if age < 13:
        raise TooYoungError(f'Age too young: {age}')
    if age > 150:
        raise TooOldError(f'Age too old: {age}')
    return age

# Template 27: Safe Dictionary Access
def safe_dict_get(data, key, default=None):
    """安全的字典访问."""
    try:
        return data[key]
    except (KeyError, TypeError):
        return default

# Template 28: Exception Aggregation
def aggregate_errors(errors):
    """聚合错误."""
    if not errors:
        return None
    
    error_messages = [str(e) for e in errors]
    combined_message = '; '.join(error_messages)
    
    raise AggregateError(
        f'{len(errors)} errors occurred: {combined_message}',
        errors=errors
    )

# Template 29: Retry with Exponential Backoff
def retry_with_backoff(func, max_retries=3, base_delay=1):
    """指数退避重试."""
    import time
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            delay = base_delay * (2 ** attempt)
            logger.warning(f'Retry {attempt + 1}/{max_retries} after {delay}s')
            time.sleep(delay)
    
    return None

# Template 30: Exception Hierarchy
class APIError(Exception):
    """API 错误基类."""
    pass

class AuthenticationError(APIError):
    """认证错误."""
    pass

class RateLimitError(APIError):
    """速率限制错误."""
    pass

class ServerError(APIError):
    """服务器错误."""
    pass

def call_api(endpoint):
    """调用 API."""
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        if e.response.status_code == 401:
            raise AuthenticationError('Authentication failed')
        elif e.response.status_code == 429:
            raise RateLimitError('Rate limit exceeded')
        else:
            raise ServerError(f'Server error: {e.response.status_code}')
    except requests.RequestException as e:
        raise APIError(f'Network error: {e}')
