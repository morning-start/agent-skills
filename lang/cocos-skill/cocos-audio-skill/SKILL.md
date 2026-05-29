---
name: cocos-audio-skill
description: Cocos Creator 3.8 音频系统，背景音乐、音效播放、音频管理
dependency:
  - cocos-intro-skill
---

# Cocos Creator 3.8 声音系统

## 任务目标
- 本 Skill 用于：掌握 Cocos Creator 音频系统实现游戏音效
- 能力包含：音频播放、背景音乐、音效管理、音量控制
- 触发条件：添加游戏音效、背景音乐、语音播放

## 概述

音频是游戏中不可或缺的一部分，好的音乐能让游戏更加真实、富有沉浸感。Cocos Creator 的音频系统支持导入并播放大多数常见的音频文件格式。

## 音频组件

### AudioSource 组件
```typescript
import { AudioSource } from 'cc';

const audioSource = node.getComponent(AudioSource);
audioSource.clip = audioClip;
audioSource.volume = 0.5;
audioSource.loop = true;
audioSource.playOnLoad = true;
```

### 属性说明
- **clip**：音频资源
- **volume**：音量（0-1）
- **loop**：是否循环
- **playOnLoad**：加载后自动播放
- **mute**：静音

## 脚本控制

### 播放控制
```typescript
// 播放
audioSource.play();

// 暂停
audioSource.pause();

// 停止
audioSource.stop();

// 恢复
audioSource.resume();
```

### 播放状态
```typescript
if (audioSource.state === AudioSource.State.PLAYING) {
    console.log('Audio is playing');
}
```

## 动态加载播放

### 加载音频
```typescript
import { resources } from 'cc';

resources.load('audio/bgm_main', AudioClip, (err, audioClip) => {
    if (!err) {
        const audioSource = this.node.addComponent(AudioSource);
        audioSource.clip = audioClip;
        audioSource.loop = true;
        audioSource.play();
    }
});
```

### 短音效播放
```typescript
import { resources } from 'cc';

resources.load('audio/sfx_click', AudioClip, (err, clip) => {
    if (!err) {
        const audioSource = this.node.addComponent(AudioSource);
        audioSource.clip = clip;
        audioSource.play();
    }
});
```

## 音频管理

### 背景音乐管理
```typescript
class AudioManager {
    private bgmSource: AudioSource | null = null;

    playBGM(clip: AudioClip, volume: number = 1) {
        if (!this.bgmSource) {
            this.bgmSource = new AudioSource();
        }
        this.bgmSource.clip = clip;
        this.bgmSource.volume = volume;
        this.bgmSource.loop = true;
        this.bgmSource.play();
    }

    stopBGM() {
        if (this.bgmSource) {
            this.bgmSource.stop();
        }
    }

    setBGMVolume(volume: number) {
        if (this.bgmSource) {
            this.bgmSource.volume = volume;
        }
    }
}
```

### 音效池管理
```typescript
class SFXManager {
    private sfxPool: AudioSource[] = [];
    private sfxClips: Map<string, AudioClip> = new Map();

    playSFX(name: string, volume: number = 1) {
        const clip = this.sfxClips.get(name);
        if (!clip) return;

        const source = this.getFreeSource();
        if (source) {
            source.clip = clip;
            source.volume = volume;
            source.play();
        }
    }

    private getFreeSource(): AudioSource | null {
        for (const source of this.sfxPool) {
            if (source.state !== AudioSource.State.PLAYING) {
                return source;
            }
        }
        return null;
    }
}
```

## 加载模式

### Web Audio
- 兼容性更好
- 问题较少
- 占用内存较多

### DOM Audio
- 每次播放需要用户操作
- 同时只能播放一个音频
- 适合背景音乐

## 资源索引

### 必要参考
- [音频系统](https://docs.cocos.com/creator/3.8/manual/zh/audio/)
- [AudioSource API](https://docs.cocos.com/creator/3.8/api/zh/classes/AudioSource.html)

## 注意事项

### 性能优化
- 合理控制同音效数量
- 使用短音效不循环
- 善用静音控制

### 最佳实践
- 背景音乐与音效分离管理
- 预加载常用音效
- 提供音量设置选项