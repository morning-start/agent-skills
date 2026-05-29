---
name: state-management
version: v1.0.0
author: skill-manager
parent_skill: software-design
description: 状态管理方案设计子技能，提供局部状态、全局状态、共享状态、不可变状态、单向数据流等状态管理策略和最佳实践
tags: [state-management, immutable-state, data-flow, redux, state-design]
network_search: optional
---

# 状态管理方案设计

## 任务目标

本子技能帮助开发者设计和实现高效的状态管理系统，涵盖状态存储、更新、共享和优化的完整解决方案。适用于从简单应用到复杂大型项目的各种场景。

### 核心能力

- **状态分类设计**: 局部状态 / 全局状态 / 共享状态 / 持久化状态
- **状态更新策略**: 直接修改 / 不可变更新 / 响应式更新
- **数据流设计**: 单向数据流 / 双向绑定 / 事件驱动
- **状态管理库应用**: Redux、Vuex、Zustand、Jotai 等
- **性能优化**: 状态切片、懒加载、缓存策略
- **状态持久化**: LocalStorage、IndexedDB、服务端同步

---

## 三步流程框架

```
┌─────────────────────────────────────────────────────────────┐
│  第一步：查阅信息 (Research)                                  │
│  ├── 分析应用场景和需求                                      │
│  ├── 识别状态类型和复杂度                                    │
│  └── 调研合适的状态管理方案                                  │
├─────────────────────────────────────────────────────────────┤
│  第二步：执行操作 (Execute)                                   │
│  ├── 设计状态结构和组织方式                                  │
│  ├── 实现状态更新逻辑                                        │
│  ├── 配置状态管理工具（如需要）                              │
│  └── 优化状态访问和更新性能                                  │
├─────────────────────────────────────────────────────────────┤
│  第三步：检查验收 (Validate)                                  │
│  ├── 验证状态设计的合理性                                    │
│  ├── 检查状态更新的可预测性                                  │
│  └── 评估性能和可维护性                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 状态分类与选择

### 1. 局部状态（Local State）

**适用场景**: 仅单个组件使用的状态

```javascript
// React 示例
function Counter() {
  const [count, setCount] = useState(0);  // 局部状态
  
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

**特点**:
- ✅ 封装性好，不影响其他组件
- ✅ 性能开销小
- ✅ 易于维护和测试
- ❌ 无法跨组件共享

---

### 2. 全局状态（Global State）

**适用场景**: 多个组件需要访问的共享状态

```javascript
// Redux 示例
const initialState = {
  user: null,
  theme: 'light',
  notifications: []
};

function rootReducer(state = initialState, action) {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'SET_THEME':
      return { ...state, theme: action.payload };
    default:
      return state;
  }
}
```

**特点**:
- ✅ 全局可访问
- ✅ 状态集中管理
- ✅ 便于调试和追踪
- ❌ 可能导致不必要的重渲染
- ❌ 过度使用会增加复杂度

---

### 3. 共享状态（Shared State）

**适用场景**: 特定模块或功能区域内的状态共享

```javascript
// Context API 示例
const ThemeContext = createContext();

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  
  const value = useMemo(() => ({
    theme,
    setTheme,
    toggleTheme: () => setTheme(t => t === 'light' ? 'dark' : 'light')
  }), [theme]);
  
  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

// 使用
function ThemedComponent() {
  const { theme, toggleTheme } = useContext(ThemeContext);
  return <div className={theme}>...</div>;
}
```

**特点**:
- ✅ 按需共享，避免全局污染
- ✅ 作用域清晰
- ✅ 灵活性高
- ❌ 多层嵌套可能复杂

---

### 4. 不可变状态（Immutable State）

**核心原则**: 状态不可直接修改，只能通过创建新对象来更新

```javascript
// ✗ 错误做法（直接修改）
state.user.name = 'New Name';

// ✓ 正确做法（不可变更新）
const newState = {
  ...state,
  user: {
    ...state.user,
    name: 'New Name'
  }
};

// 使用 Immer 简化
import produce from 'immer';

const newState = produce(state, draft => {
  draft.user.name = 'New Name';
});
```

**优势**:
- ✅ 可预测的状态变更
- ✅ 便于时间旅行调试
- ✅ 性能优化（引用比较）
- ✅ 避免副作用

---

## 数据流模式

### 1. 单向数据流（推荐）

**流程**: State → View → Action → State

```javascript
// Redux 单向数据流
// 1. 组件 dispatch action
dispatch({ type: 'ADD_TODO', payload: todo });

// 2. Reducer 处理 action
function todos(state = [], action) {
  switch (action.type) {
    case 'ADD_TODO':
      return [...state, action.payload];
    default:
      return state;
  }
}

// 3. Store 更新
// 4. 组件重新渲染
```

**优势**:
- ✅ 数据流向清晰
- ✅ 易于调试和追踪
- ✅ 可预测性强
- ✅ 适合大型应用

---

### 2. 双向绑定

**典型应用**: Vue、Angular

```vue
<!-- Vue 示例 -->
<template>
  <input v-model="message" />
  <p>{{ message }}</p>
</template>

<script>
export default {
  data() {
    return {
      message: ''  // 双向绑定
    }
  }
}
</script>
```

**特点**:
- ✅ 开发效率高
- ✅ 代码简洁
- ❌ 数据流向不清晰
- ❌ 难以追踪状态变化

---

### 3. 响应式状态

**典型应用**: MobX、Vue Reactivity

```javascript
// MobX 示例
import { makeAutoObservable } from 'mobx';

class TodoStore {
  todos = [];
  
  constructor() {
    makeAutoObservable(this);
  }
  
  addTodo(text) {
    this.todos.push({ text, done: false });
  }
  
  get completedTodos() {
    return this.todos.filter(t => t.done);
  }
}

// 自动追踪依赖，响应式更新
```

**特点**:
- ✅ 自动依赖追踪
- ✅ 细粒度更新
- ✅ 代码自然直观
- ❌ 魔法行为，调试困难

---

## 状态管理方案选型指南

### 小型项目（< 10 个组件）

**推荐方案**: 局部状态 + Context

```javascript
// 简单应用架构
function App() {
  const [user, setUser] = useState(null);      // 全局状态
  const [theme, setTheme] = useState('light');  // 全局状态
  
  return (
    <UserContext.Provider value={{ user, setUser }}>
      <ThemeContext.Provider value={{ theme, setTheme }}>
        <MainLayout />
      </ThemeContext.Provider>
    </UserContext.Provider>
  );
}
```

---

### 中型项目（10-50 个组件）

**推荐方案**: Zustand / Jotai / Context + Reducer

```javascript
// Zustand 示例
import create from 'zustand';

const useStore = create((set) => ({
  // 状态
  todos: [],
  filter: 'all',
  
  // 动作
  addTodo: (text) => set((state) => ({
    todos: [...state.todos, { text, done: false }]
  })),
  
  toggleTodo: (index) => set((state) => ({
    todos: state.todos.map((todo, i) =>
      i === index ? { ...todo, done: !todo.done } : todo
    )
  })),
  
  setFilter: (filter) => set({ filter })
}));
```

---

### 大型项目（> 50 个组件）

**推荐方案**: Redux Toolkit / Redux + RTK Query

```javascript
// Redux Toolkit 示例
import { createSlice, configureStore } from '@reduxjs/toolkit';

const todosSlice = createSlice({
  name: 'todos',
  initialState: [],
  reducers: {
    addTodo: (state, action) => {
      state.push({ text: action.payload, done: false });
    },
    toggleTodo: (state, action) => {
      state[action.index].done = !state[action.index].done;
    }
  }
});

const store = configureStore({
  reducer: {
    todos: todosSlice.reducer,
    // 其他 slices...
  }
});
```

---

## 状态设计最佳实践

### 1. 状态最小化原则

```javascript
// ✗ 状态冗余
const [todos, setTodos] = useState([]);
const [todoCount, setTodoCount] = useState(0);  // 可从 todos 推导
const [completedCount, setCompletedCount] = useState(0);  // 可计算

// ✓ 状态最小化
const [todos, setTodos] = useState([]);
const todoCount = todos.length;  // 计算值
const completedCount = todos.filter(t => t.done).length;  // 计算值
```

---

### 2. 状态规范化

```javascript
// ✗ 嵌套过深
const state = {
  users: {
    1: {
      profile: {
        settings: {
          preferences: {
            theme: 'dark'
          }
        }
      }
    }
  }
};

// ✓ 扁平化结构
const state = {
  users: {
    1: {
      profileId: 101,
      settingsId: 201
    }
  },
  profiles: {
    101: { settingsId: 201 }
  },
  settings: {
    201: { theme: 'dark' }
  }
};
```

---

### 3. 派生状态计算

```javascript
// ✗ 存储派生状态
const [todos, setTodos] = useState([]);
const [completedTodos, setCompletedTodos] = useState([]);  // 冗余
const [pendingTodos, setPendingTodos] = useState([]);      // 冗余

// ✓ 计算派生状态
const [todos, setTodos] = useState([]);
const completedTodos = useMemo(
  () => todos.filter(t => t.done),
  [todos]
);
const pendingTodos = useMemo(
  () => todos.filter(t => !t.done),
  [todos]
);
```

---

### 4. 状态更新批处理

```javascript
// ✗ 多次独立更新
setState1(value1);
setState2(value2);
setState3(value3);
// 触发 3 次重渲染

// ✓ 批处理更新
import { unstable_batchedUpdates } from 'react-dom';

unstable_batchedUpdates(() => {
  setState1(value1);
  setState2(value2);
  setState3(value3);
});
// 只触发 1 次重渲染
```

---

## 状态持久化

### LocalStorage 方案

```javascript
// 自定义 Hook
function usePersistentState(key, initialValue) {
  const [state, setState] = useState(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });
  
  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(state));
  }, [key, state]);
  
  return [state, setState];
}

// 使用
const [theme, setTheme] = usePersistentState('theme', 'light');
```

### Redux Persist

```javascript
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['user', 'settings']  // 只持久化这些 slices
};

const persistedReducer = persistReducer(persistConfig, rootReducer);
const store = persistStore(configureStore({ reducer: persistedReducer }));
```

---

## 性能优化策略

### 1. 状态切片（State Slicing）

```javascript
// ✗ 大状态对象
const [state, setState] = useState({
  user: null,
  todos: [],
  theme: 'light',
  notifications: [],
  // ... 更多状态
});

// ✓ 状态切片
const [user, setUser] = useState(null);
const [todos, setTodos] = useState([]);
const [theme, setTheme] = useState('light');
const [notifications, setNotifications] = useState([]);
```

---

### 2. 选择器优化

```javascript
// Redux Reselect 示例
import { createSelector } from 'reselect';

const selectTodos = state => state.todos;

// 记忆化选择器，仅当 todos 变化时重新计算
const selectCompletedTodos = createSelector(
  [selectTodos],
  todos => todos.filter(t => t.done)
);

const selectPendingTodos = createSelector(
  [selectTodos],
  todos => todos.filter(t => !t.done)
);
```

---

### 3. 懒加载状态

```javascript
// 按需加载状态模块
const useFeatureState = () => {
  const [state, setState] = useState(null);
  
  useEffect(() => {
    // 仅在需要时加载
    import('./featureModule').then(module => {
      setState(module.initialState);
    });
  }, []);
  
  return state;
};
```

---

## 网络搜索配置

### 搜索触发条件

- 查询最新状态管理库对比
- 了解特定框架的状态管理最佳实践
- 搜索性能优化方案
- 验证设计模式的当前使用情况

### 搜索关键词示例

- "state management comparison 2025"
- "Redux vs Zustand vs Jotai performance"
- "React state management best practices"
- "immutable state patterns"

---

## 使用示例

### 示例 1: 选择状态管理方案

**用户**: "我的应用有 30 个组件，需要共享用户状态和主题，该用什么方案？"

**输出**:
1. 分析应用规模和需求
2. 推荐 Zustand 或 Context + Reducer
3. 提供实现示例
4. 说明优缺点和注意事项

### 示例 2: 状态结构设计

**用户**: "这个状态结构怎么设计比较好？"

**输出**:
1. 分析业务需求
2. 设计规范化状态结构
3. 区分存储状态和派生状态
4. 提供代码实现

### 示例 3: 性能优化

**用户**: "我的应用重渲染太频繁了，怎么优化？"

**输出**:
1. 分析状态更新模式
2. 识别不必要的重渲染
3. 提供优化方案（记忆化、状态切片等）
4. 给出代码示例

---

## 学习建议

### 🌱 新手阶段

**重点掌握**:
- useState 基础用法
- 局部状态 vs 全局状态
- 状态提升（Lifting State Up）

**练习题目**:
1. 使用 useState 实现计数器
2. 实现父子组件状态共享
3. 使用 Context 传递全局状态

### 🚀 进阶阶段

**重点掌握**:
- 不可变状态更新
- 单向数据流
- 状态管理库应用

**练习题目**:
1. 使用 Redux/Zustand 实现 TODO 应用
2. 实现状态持久化
3. 优化状态更新性能

### 🏗️ 架构师阶段

**重点掌握**:
- 状态管理架构设计
- 高级性能优化
- 自定义状态管理方案

**练习题目**:
1. 设计大型应用的状态架构
2. 实现自定义状态管理库
3. 状态更新追踪和调试工具

---

## 注意事项

- **避免过度设计**: 从小处开始，按需扩展
- **保持状态最小化**: 只存储必要的状态
- **使用不可变更新**: 确保状态可预测
- **性能监控**: 使用 DevTools 监控重渲染
- **类型安全**: 使用 TypeScript 定义状态类型

---

## 相关概念关联

- **状态管理** → **单向数据流** → **Redux 模式**
- **不可变状态** → **纯函数** → **函数式设计**
- **响应式** → **依赖追踪** → **自动更新**
- **状态持久化** → **离线优先** → **同步策略**

---

## 版本历史

- **v1.0.0** (2025-01-XX): 初始版本
  - 创建状态管理子技能
  - 涵盖主流状态管理方案
  - 提供性能优化策略
  - 配置网络搜索能力
