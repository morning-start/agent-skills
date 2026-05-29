---
name: performance
version: v1.0.0
author: skill-manager
parent_skill: software-design
description: 性能优化子技能，提供性能分析、内存管理、资源优化、渲染优化、网络优化等性能提升策略和最佳实践
tags: [performance, optimization, memory-management, rendering, network, profiling]
network_search: optional
---

# 性能优化

## 任务目标

本子技能帮助开发者识别和解决性能瓶颈，涵盖性能分析、内存管理、渲染优化、网络优化等核心内容。

### 核心能力

- **性能分析**: 性能测试、瓶颈识别、性能监控
- **内存管理**: 内存泄漏检测、垃圾回收优化
- **渲染优化**: 减少重绘重排、虚拟列表、懒加载
- **网络优化**: 请求合并、缓存策略、CDN 加速
- **代码优化**: 算法优化、数据结构选择、防抖节流

---

## 性能分析方法

### 1. 性能测试工具

```javascript
// ✓ 使用 Performance API
const start = performance.now();
// 执行代码
const end = performance.now();
console.log(`Execution time: ${end - start}ms`);

// ✓ 使用 console.time
console.time('fetchData');
const data = await fetchData();
console.timeEnd('fetchData');

// ✓ 性能监控
class PerformanceMonitor {
  static measure(label) {
    const start = performance.now();
    return {
      end: () => {
        const duration = performance.now() - start;
        console.log(`${label}: ${duration.toFixed(2)}ms`);
        return duration;
      }
    };
  }
}

// 使用
const measure = PerformanceMonitor.measure('Process Data');
processData();
measure.end();
```

---

### 2. 内存泄漏检测

```javascript
// ✓ 检测内存泄漏
function detectMemoryLeak() {
  let leakArray = [];
  
  function grow() {
    for (let i = 0; i < 1000; i++) {
      leakArray.push(new Array(1000).fill('data'));
    }
    console.log(`Memory: ${performance.memory?.usedJSHeapSize}`);
  }
  
  setInterval(grow, 1000);
}

// ✓ 避免常见泄漏
class Component {
  constructor() {
    // ✗ 泄漏：未清理的定时器
    this.interval = setInterval(() => {
      this.doSomething();
    }, 1000);
    
    // ✗ 泄漏：未清理的事件监听
    window.addEventListener('resize', this.handleResize);
  }
  
  destroy() {
    // ✓ 清理资源
    clearInterval(this.interval);
    window.removeEventListener('resize', this.handleResize);
  }
}
```

---

## 渲染优化

### 1. 虚拟列表

```javascript
// ✓ 虚拟滚动
function VirtualList({ items, itemHeight, containerHeight }) {
  const [scrollTop, setScrollTop] = useState(0);
  
  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(
    startIndex + Math.ceil(containerHeight / itemHeight),
    items.length
  );
  
  const visibleItems = items.slice(startIndex, endIndex);
  const offsetY = startIndex * itemHeight;
  
  return (
    <div 
      style={{ height: containerHeight, overflow: 'auto' }}
      onScroll={e => setScrollTop(e.target.scrollTop)}
    >
      <div style={{ height: items.length * itemHeight, position: 'relative' }}>
        <div style={{ position: 'absolute', top: offsetY }}>
          {visibleItems.map(item => (
            <div key={item.id} style={{ height: itemHeight }}>
              {item.name}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

---

### 2. 防抖与节流

```javascript
// ✓ 防抖（debounce）
function debounce(fn, delay) {
  let timer = null;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

// 使用：搜索输入
const handleSearch = debounce((query) => {
  searchAPI(query);
}, 300);

// ✓ 节流（throttle）
function throttle(fn, limit) {
  let lastCall = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastCall >= limit) {
      lastCall = now;
      fn.apply(this, args);
    }
  };
}

// 使用：滚动事件
const handleScroll = throttle(() => {
  loadMoreContent();
}, 200);
```

---

### 3. 懒加载

```javascript
// ✓ 图片懒加载
function LazyImage({ src, alt }) {
  const [loaded, setLoaded] = useState(false);
  const [ref, setRef] = useState(null);
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setLoaded(true);
          observer.disconnect();
        }
      },
      { rootMargin: '100px' }
    );
    
    if (ref) observer.observe(ref);
    return () => observer.disconnect();
  }, [ref]);
  
  return (
    <img
      ref={setRef}
      src={loaded ? src : 'placeholder.jpg'}
      alt={alt}
      loading="lazy"
    />
  );
}

// ✓ 组件懒加载
const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

---

## 网络优化

### 1. 请求合并

```javascript
// ✓ 批量请求
class BatchFetcher {
  constructor(batchDelay = 100) {
    this.queue = [];
    this.batchDelay = batchDelay;
    this.timer = null;
  }
  
  fetch(endpoint, params) {
    return new Promise((resolve, reject) => {
      this.queue.push({ endpoint, params, resolve, reject });
      
      if (!this.timer) {
        this.timer = setTimeout(() => this.flush(), this.batchDelay);
      }
    });
  }
  
  async flush() {
    const batch = this.queue.splice(0);
    this.timer = null;
    
    try {
      const results = await fetch('/api/batch', {
        method: 'POST',
        body: JSON.stringify(batch)
      });
      
      batch.forEach((item, index) => {
        item.resolve(results[index]);
      });
    } catch (error) {
      batch.forEach(item => item.reject(error));
    }
  }
}
```

---

### 2. 缓存策略

```javascript
// ✓ 多级缓存
class CacheManager {
  constructor() {
    this.memoryCache = new Map();
    this.storageCache = localStorage;
  }
  
  async get(key, ttl = 5 * 60 * 1000) {
    // 内存缓存
    const memData = this.memoryCache.get(key);
    if (memData && Date.now() - memData.timestamp < ttl) {
      return memData.data;
    }
    
    // 本地存储缓存
    const storageData = this.storageCache.getItem(key);
    if (storageData) {
      const parsed = JSON.parse(storageData);
      if (Date.now() - parsed.timestamp < ttl) {
        this.memoryCache.set(key, parsed);
        return parsed.data;
      }
    }
    
    return null;
  }
  
  set(key, data) {
    const item = { data, timestamp: Date.now() };
    this.memoryCache.set(key, item);
    try {
      this.storageCache.setItem(key, JSON.stringify(item));
    } catch (e) {
      // localStorage 满了
    }
  }
}
```

---

## 代码优化

### 1. 算法优化

```javascript
// ✗ O(n²)
function findDuplicates(arr) {
  const duplicates = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j] && !duplicates.includes(arr[i])) {
        duplicates.push(arr[i]);
      }
    }
  }
  return duplicates;
}

// ✓ O(n)
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();
  
  for (const item of arr) {
    if (seen.has(item)) {
      duplicates.add(item);
    } else {
      seen.add(item);
    }
  }
  
  return Array.from(duplicates);
}
```

---

### 2. 数据结构选择

```javascript
// ✓ 使用 Map 替代对象查找
// ✗ O(n)
const user = users.find(u => u.id === targetId);

// ✓ O(1)
const userMap = new Map(users.map(u => [u.id, u]));
const user = userMap.get(targetId);

// ✓ 使用 Set 进行成员检查
// ✗ O(n)
if (array.includes(item)) { /* ... */ }

// ✓ O(1)
const set = new Set(array);
if (set.has(item)) { /* ... */ }
```

---

## 性能优化清单

### 加载性能

- [ ] 代码分割（Code Splitting）
- [ ] 懒加载（Lazy Loading）
- [ ] 预加载关键资源
- [ ] 使用 CDN
- [ ] 压缩资源（Gzip/Brotli）
- [ ] 优化图片大小
- [ ] 减少 HTTP 请求

### 运行时性能

- [ ] 使用虚拟列表
- [ ] 实现防抖节流
- [ ] 避免内存泄漏
- [ ] 优化循环和递归
- [ ] 使用合适的数据结构
- [ ] 减少 DOM 操作
- [ ] 使用 requestAnimationFrame

### 网络性能

- [ ] 启用缓存
- [ ] 请求合并
- [ ] 使用 HTTP/2
- [ ] 减少 payload 大小
- [ ] 实现重试机制
- [ ] 使用 WebSocket 实时通信

---

## 注意事项

- **先测量后优化**: 不要盲目优化
- **关注关键路径**: 优先优化用户感知明显的部分
- **平衡可读性**: 不要为了性能牺牲可维护性
- **持续监控**: 建立性能监控体系
- **A/B 测试**: 验证优化效果

---

## 版本历史

- **v1.0.0** (2025-01-XX): 初始版本
  - 创建性能优化子技能
  - 涵盖性能分析方法
  - 提供优化策略和最佳实践
