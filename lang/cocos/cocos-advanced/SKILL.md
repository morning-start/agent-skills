---
name: cocos-advanced
description: Cocos Creator 3.8 进阶主题，性能优化、架构设计、高级特性
dependency:
  - cocos-intro
  - cocos-scene
  - cocos-script
  - cocos-render
---

# Cocos Creator 3.8 进阶主题

## 任务目标
- 本 Skill 用于：深入掌握 Cocos Creator 高级特性和最佳实践
- 能力包含：性能优化、架构设计、自定义引擎、底层 API
- 触发条件：优化游戏性能、大型项目架构、深度定制

## 性能优化

### 渲染优化

#### DrawCall 优化
- 使用合批（Batching）
- 图集合并
- 减少材质切换
- 静态合批和动态合批

```typescript
import { renderer } from 'cc';

// 启用自动合批
renderer.pipeline.enableAutoBatching = true;
```

#### 帧率优化
- 减少每帧计算
- 善用对象池
- 优化物理引擎更新频率
- 延迟非必要更新

#### 内存优化
- 合理使用资源缓存
- 及时释放资源
- 使用压缩纹理
- 控制资源大小

### CPU 优化
```typescript
import { Game } from 'cc';

// 降低更新频率
Game.I.on(Game.EVENT_HIDE, () => {
    Game.I.targetFrameRate = 30;
});

Game.I.on(Game.EVENT_SHOW, () => {
    Game.I.targetFrameRate = 60;
});
```

### GPU 优化
- 减少 Overdraw
- 使用 LOD
- 简化着色器
- 减少纹理采样

## 架构设计

### 模块化设计
- UI 模块
- 战斗模块
- 资源模块
- 网络模块
- 数据模块

### MVC 架构
```typescript
// Model - 数据
class GameModel {
    score: number = 0;
    level: number = 1;
}

// View - 视图
class GameView extends Component {
    updateScore(score: number) {
        this.scoreLabel.string = score.toString();
    }
}

// Controller - 控制器
class GameController {
    private model: GameModel;
    private view: GameView;

    addScore(amount: number) {
        this.model.score += amount;
        this.view.updateScore(this.model.score);
    }
}
```

### 状态机模式
```typescript
import { StateMachine } from 'cc';

class PlayerStateMachine extends StateMachine {
    states = {
        idle: new IdleState(),
        run: new RunState(),
        jump: new JumpState(),
        attack: new AttackState()
    };
}
```

## 底层 API

### 渲染管线定制
```typescript
import { RenderPipeline, ForwardPipeline } from 'cc';

class CustomPipeline extends ForwardPipeline {
    setupPipeline() {
        // 自定义渲染流程
    }
}
```

### 自定义着色器
```glsl
// myShader.effect
CCEffect %{
    technique {
        pass {
            vert: vert
            frag: frag
        }
    }
}%

Properties {
    _MainTex (Texture2D) {}
    _Color (Color) {}
}
```

### 原生接口调用
```typescript
import {native} from 'cc';

if (sys.platform === sys.Platform.IOS) {
    native.callStaticMethod('NativeBridge', 'showAlert', 'Title', 'Message');
}
```

## 热更新

### 配置热更新
```typescript
import { hotUpdate } from 'cc';

hotUpdate.checkUpdate((err, checking) => {
    if (!err) {
        if (checking) {
            console.log('Update available');
        }
    }
});
```

### 资源热更新
```typescript
hotUpdate.beginUpdate((progress) => {
    console.log('Update progress:', progress);
}, (err, assets) => {
    if (!err) {
        console.log('Update complete');
        hotUpdate.reload();
    }
});
```

## 网络通信

### HTTP 请求
```typescript
import { http } from 'cc';

http.get('https://api.example.com/data', (err, response) => {
    if (!err) {
        const data = JSON.parse(response);
        console.log(data);
    }
});
```

### WebSocket
```typescript
import { WebSocket } from 'cc';

const ws = new WebSocket('wss://game.example.com');
ws.onOpen = () => {
    ws.send('Hello');
};
ws.onMessage = (data) => {
    console.log('Received:', data);
};
```

## 测试

### 单元测试
```typescript
import { test } from 'cc';

@test.suite('GameModel')
class GameModelTest {
    @test.skip('Score should increase')
    testAddScore() {
        const model = new GameModel();
        model.addScore(10);
        assert.equal(model.score, 10);
    }
}
```

## 资源索引

### 必要参考
- [进阶主题](https://docs.cocos.com/creator/3.8/manual/zh/advanced-topics/)
- [性能优化](https://docs.cocos.com/creator/3.8/manual/zh/advanced-topics/optimize-jit.html)
- [HotUpdate](https://docs.cocos.com/creator/3.8/manual/zh/advanced-topics/hot-update/)

## 注意事项

### 大型项目
- 做好代码架构
- 使用模块化开发
- 善用工具链

### 持续优化
- 性能分析优先
- 量化优化效果
- 做好性能监控