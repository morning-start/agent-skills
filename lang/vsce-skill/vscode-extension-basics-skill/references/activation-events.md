# Activation Events

## 目录
- [概览](#概览)
- [事件类型](#事件类型)
- [onCommand](#oncommand)
- [onView](#onview)
- [onLanguage](#onlanguage)
- [onStartupFinished](#onstartupfinished)
- [自动激活](#自动激活)

## 概览
激活事件决定扩展何时被加载和激活。合理的激活事件可以优化 VSCode 启动性能。

## 事件类型

### onCommand
当命令被调用时激活：
```json
{
  "activationEvents": [
    "onCommand:extension.helloWorld"
  ]
}
```

### onView
当指定视图被打开时激活：
```json
{
  "activationEvents": [
    "onView:nodeDependencies"
  ]
}
```

### onLanguage
当特定语言文件打开时激活：
```json
{
  "activationEvents": [
    "onLanguage:python",
    "onLanguage:javascript"
  ]
}
```

### onStartupFinished
VSCode 启动完成后激活（不阻塞启动）：
```json
{
  "activationEvents": [
    "onStartupFinished"
  ]
}
```

## 自动激活
VSCode 1.74+ 版本，commands 贡献会自动生成 onCommand 激活事件，无需手动声明。

## 推荐实践
- 优先使用具体事件而非 onStartupFinished
- 避免使用 * 通配符
- 按需激活减少资源占用
