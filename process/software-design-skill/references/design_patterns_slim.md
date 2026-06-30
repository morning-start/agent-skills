# 设计模式精简速查表 (Top 10)

> 基于 GoF 23 种经典设计模式归纳，按意图分为三类。每个模式包含一句话定义、适用场景和简单伪代码。

---

## 创建型模式 (Creational)

### 1. 工厂方法 (Factory Method)

**定义**: 定义一个创建对象的接口，让子类决定实例化哪个类。

**适用场景**:
- 一个类无法预知它需要创建哪个类的对象
- 将创建逻辑委托给子类

```python
# 伪代码
interface Creator { factoryMethod(): Product }
class ConcreteCreatorA implements Creator {
    factoryMethod(): Product { return new ConcreteProductA() }
}
```

---

### 2. 建造者模式 (Builder)

**定义**: 将一个复杂对象的构建与它的表示分离，使同样的构建过程可以创建不同的表示。

**适用场景**:
- 创建对象需要大量可选参数
- 创建步骤固定但具体实现可变

```python
# 伪代码
class PizzaBuilder {
    setSize(size)     → self
    addCheese(flag)   → self
    addPepperoni(flag)→ self
    build()           → Pizza
}
# 使用: PizzaBuilder().setSize("large").addCheese(true).build()
```

---

### 3. 单例模式 (Singleton)

**定义**: 确保一个类只有一个实例，并提供全局访问点。

**适用场景**:
- 需要全局唯一的对象（配置管理器、连接池）
- ⚠️ 注意：持有可变状态时慎用，建议用依赖注入替代

```python
# 伪代码
class Singleton {
    private static instance
    static getInstance(): Singleton {
        if instance == null: instance = new Singleton()
        return instance
    }
}
```

---

## 结构型模式 (Structural)

### 4. 适配器模式 (Adapter)

**定义**: 将一个类的接口转换成客户期望的另一个接口。

**适用场景**:
- 需要使用一个现有类但其接口不符合需求
- 集成第三方库或遗留系统

```python
# 伪代码
interface Target { request(): void }
class Adaptee { specificRequest(): void }
class Adapter implements Target {
    adaptee = new Adaptee()
    request(): void { adaptee.specificRequest() }
}
```

---

### 5. 装饰器模式 (Decorator)

**定义**: 动态地给对象添加额外的职责，比生成子类更灵活。

**适用场景**:
- 需要给对象动态添加功能，且不希望影响其他对象
- 功能组合多变，用继承会导致类爆炸

```python
# 伪代码
interface DataSource { write(data): void }
class FileDataSource implements DataSource { ... }
class EncryptionDecorator implements DataSource {
    wrappee: DataSource
    write(data): void { wrappee.write(encrypt(data)) }
}
```

---

### 6. 代理模式 (Proxy)

**定义**: 为另一个对象提供一个替身以控制对它的访问。

**适用场景**:
- 延迟加载（虚拟代理）
- 访问控制（保护代理）
- 日志记录（日志代理）
- 远程调用（远程代理）

```python
# 伪代码
interface Image { display(): void }
class RealImage implements Image { ... }
class ProxyImage implements Image {
    realImage: RealImage
    display(): void {
        if realImage == null: realImage = new RealImage()
        realImage.display()
    }
}
```

---

## 行为型模式 (Behavioral)

### 7. 策略模式 (Strategy)

**定义**: 定义一系列算法，把它们封装起来，并使它们可以互相替换。

**适用场景**:
- 多个条件分支对应不同行为
- 算法族需要独立于使用它的客户端变化

```python
# 伪代码
interface PaymentStrategy { pay(amount): Result }
class AlipayStrategy implements PaymentStrategy { ... }
class WechatPayStrategy implements PaymentStrategy { ... }
class PaymentContext {
    strategy: PaymentStrategy
    executePay(amount): Result { return strategy.pay(amount) }
}
```

---

### 8. 观察者模式 (Observer)

**定义**: 定义一对多的依赖关系，当一个对象状态变化时，所有依赖者自动收到通知。

**适用场景**:
- 事件处理系统
- 状态变化需要通知多个模块
- 发布-订阅场景

```python
# 伪代码
interface Observer { update(event): void }
class Subject {
    observers: List<Observer>
    attach(observer): void { observers.add(observer) }
    notify(event): void { for obs in observers: obs.update(event) }
}
```

---

### 9. 模板方法模式 (Template Method)

**定义**: 定义一个操作中的算法骨架，将一些步骤延迟到子类中实现。

**适用场景**:
- 多个类有相似的算法结构，但某些步骤不同
- 需要控制子类扩展点

```python
# 伪代码
abstract class DataProcessor {
    process(): void {         # 模板方法
        read()
        transform()
        save()
    }
    abstract transform(): void
}
class JsonProcessor extends DataProcessor {
    transform(): void { ... }
}
```

---

### 10. 命令模式 (Command)

**定义**: 将请求封装为对象，从而使你可以用不同的请求参数化客户端、队列请求、或记录请求日志。

**适用场景**:
- 需要将操作参数化
- 需要支持撤销/重做
- 需要记录操作日志

```python
# 伪代码
interface Command { execute(): void; undo(): void }
class PlaceOrderCommand implements Command {
    order: Order
    execute(): void { orderService.place(order) }
    undo(): void { orderService.cancel(order) }
}
```

---

## 模式选择口诀

> **创建对象用工厂，复杂构建找建造**
> **接口不匹配适配器，功能增强装饰器**
> **访问控制用代理，算法切换策略妙**
> **状态通知观察者，骨架固定模板套**
> **请求封装命令好，单一实例单例保**

---

## 参考

> 本速查表由 `E:\Workplace\Agent\agent-skills\process\standards-design-skill\skills\design-pattern-advisor\references` 中的 23 种 GoF 完整模式库精简而来。
> 如需完整模式库，请参考原目录。
