---
name: error-handling
version: v1.0.0
author: skill-manager
parent_skill: software-design
description: 错误处理机制设计子技能，提供异常捕获、错误码设计、错误传播、优雅降级等错误处理策略和最佳实践
tags: [error-handling, exception, error-codes, try-catch, graceful-degradation]
network_search: optional
---

# 错误处理机制设计

## 任务目标

本子技能帮助开发者设计健壮的错误处理机制，涵盖异常捕获、错误码设计、错误传播、用户友好的错误提示等核心内容。

### 核心能力

- **异常捕获**: try-catch-finally、多层级捕获
- **错误码设计**: 统一错误码、错误分类
- **错误传播**: 错误冒泡、错误转换
- **优雅降级**: 故障恢复、降级策略
- **错误日志**: 日志记录、错误追踪
- **用户提示**: 友好的错误消息

---

## 错误处理策略

### 1. try-catch-finally

```javascript
// ✓ 基本用法
try {
  const data = await fetchData();
  processData(data);
} catch (error) {
  console.error('Failed to fetch data:', error);
  showErrorMessage('数据加载失败');
} finally {
  hideLoading();
}

// ✓ 多层级捕获
try {
  try {
    const user = await getUser(id);
  } catch (error) {
    if (error instanceof NotFoundError) {
      throw new CustomError('用户不存在', 'USER_NOT_FOUND');
    }
    throw error;
  }
} catch (error) {
  handleGlobalError(error);
}
```

---

### 2. 错误码设计

```javascript
// 错误码枚举
const ErrorCodes = {
  // 通用错误 (1000-1999)
  UNKNOWN_ERROR: 1000,
  VALIDATION_ERROR: 1001,
  
  // 用户相关 (2000-2999)
  USER_NOT_FOUND: 2000,
  USER_ALREADY_EXISTS: 2001,
  INVALID_PASSWORD: 2002,
  
  // 订单相关 (3000-3999)
  ORDER_NOT_FOUND: 3000,
  ORDER_INVALID_STATUS: 3001,
  
  // 系统相关 (4000-4999)
  DATABASE_ERROR: 4000,
  NETWORK_ERROR: 4001
};

// 自定义错误类
class AppError extends Error {
  constructor(message, code, statusCode = 400) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.statusCode = statusCode;
    this.timestamp = new Date();
  }
}

// 使用
throw new AppError('用户不存在', ErrorCodes.USER_NOT_FOUND, 404);
```

---

### 3. 错误传播与转换

```javascript
// ✓ 错误冒泡
async function processOrder(orderId) {
  try {
    const order = await orderRepository.findById(orderId);
    if (!order) {
      throw new AppError('订单不存在', ErrorCodes.ORDER_NOT_FOUND, 404);
    }
    return order;
  } catch (error) {
    // 记录日志
    logger.error('Order processing failed', { orderId, error });
    // 继续向上抛出
    throw error;
  }
}

// ✓ 错误转换
async function handleRequest(req, res, next) {
  try {
    await next();
  } catch (error) {
    if (error instanceof AppError) {
      res.status(error.statusCode).json({
        code: error.code,
        message: error.message
      });
    } else if (error instanceof ValidationError) {
      res.status(400).json({
        code: ErrorCodes.VALIDATION_ERROR,
        message: '数据验证失败',
        details: error.details
      });
    } else {
      // 未知错误
      logger.error('Unhandled error', error);
      res.status(500).json({
        code: ErrorCodes.UNKNOWN_ERROR,
        message: '服务器内部错误'
      });
    }
  }
}
```

---

### 4. 优雅降级

```javascript
// ✓ 降级策略
async function getUserProfile(userId) {
  try {
    return await fetchUserProfile(userId);
  } catch (error) {
    logger.warn('Failed to fetch profile, using cache', error);
    // 降级：使用缓存数据
    return getCachedProfile(userId);
  }
}

// ✓ 重试机制
async function fetchWithRetry(url, options = {}) {
  const { retries = 3, delay = 1000 } = options;
  
  for (let i = 0; i < retries; i++) {
    try {
      return await fetch(url);
    } catch (error) {
      if (i === retries - 1) throw error;
      
      logger.warn(`Request failed, retrying (${i + 1}/${retries})`, error);
      await sleep(delay * Math.pow(2, i));  // 指数退避
    }
  }
}

// ✓ 熔断器模式
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.failureCount = 0;
    this.threshold = threshold;
    this.timeout = timeout;
    this.state = 'CLOSED';
    this.nextAttempt = Date.now();
  }
  
  async call(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit breaker is OPEN');
      }
      this.state = 'HALF_OPEN';
    }
    
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }
  
  onFailure() {
    this.failureCount++;
    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.timeout;
    }
  }
}
```

---

## 错误日志记录

```javascript
// ✓ 结构化日志
class Logger {
  error(message, context = {}) {
    console.error(JSON.stringify({
      level: 'error',
      message,
      timestamp: new Date().toISOString(),
      ...context,
      stack: context.error?.stack
    }));
  }
  
  warn(message, context = {}) {
    console.warn(JSON.stringify({
      level: 'warn',
      message,
      timestamp: new Date().toISOString(),
      ...context
    }));
  }
}

// 使用
logger.error('Database connection failed', {
  database: 'users',
  error: error,
  userId: currentUser?.id
});
```

---

## 用户友好的错误提示

```javascript
// ✓ 错误消息映射
const errorMessages = {
  [ErrorCodes.USER_NOT_FOUND]: '用户不存在，请检查账号是否正确',
  [ErrorCodes.INVALID_PASSWORD]: '密码错误，请重新输入',
  [ErrorCodes.ORDER_NOT_FOUND]: '订单不存在，可能已被删除',
  [ErrorCodes.NETWORK_ERROR]: '网络连接失败，请检查网络后重试',
  [ErrorCodes.UNKNOWN_ERROR]: '系统繁忙，请稍后再试'
};

function getUserFriendlyMessage(error) {
  if (error.code && errorMessages[error.code]) {
    return errorMessages[error.code];
  }
  return '发生未知错误，请联系技术支持';
}

// 使用
catch (error) {
  const message = getUserFriendlyMessage(error);
  showToast(message, 'error');
}
```

---

## 注意事项

- **不要吞掉错误**: 捕获后要处理或重新抛出
- **记录足够的上下文**: 便于问题排查
- **区分错误类型**: 不同错误不同处理
- **用户友好**: 错误消息要清晰、友好
- **安全性**: 不要泄露敏感信息

---

## 版本历史

- **v1.0.0** (2025-01-XX): 初始版本
  - 创建错误处理子技能
  - 涵盖错误处理策略
  - 提供最佳实践示例
