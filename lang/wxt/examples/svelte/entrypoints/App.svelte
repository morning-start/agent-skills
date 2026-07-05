<script lang="ts">
  import { onMount } from 'svelte';

  // 状态管理
  let storageData = {
    theme: 'light',
    enabled: true,
    count: 0,
  };

  let loading = true;
  let message = '';

  // 加载存储数据
  onMount(async () => {
    await loadStorage();
  });

  async function loadStorage() {
    try {
      const response = await browser.runtime.sendMessage({ type: 'GET_STORAGE' });
      storageData = response.data;
    } catch (error) {
      console.error('Failed to load storage:', error);
      showMessage('Failed to load data', 'error');
    } finally {
      loading = false;
    }
  }

  async function updateStorage(key: string, value: any) {
    try {
      const response = await browser.runtime.sendMessage({
        type: 'SET_STORAGE',
        data: { [key]: value },
      });

      if (response.success) {
        storageData[key] = value;
        showMessage('Settings saved', 'success');
      }
    } catch (error) {
      console.error('Failed to update storage:', error);
      showMessage('Failed to save', 'error');
    }
  }

  async function incrementCount() {
    try {
      const response = await browser.runtime.sendMessage({
        type: 'INCREMENT_COUNT',
      });

      if (response.success) {
        storageData.count = response.count;
        showMessage(`Count: ${response.count}`, 'success');
      }
    } catch (error) {
      console.error('Failed to increment count:', error);
      showMessage('Failed to increment', 'error');
    }
  }

  function showMessage(text: string, type: 'success' | 'error') {
    message = text;
    setTimeout(() => {
      message = '';
    }, 2000);
  }

  function getThemeStyles() {
    return storageData.theme === 'dark'
      ? 'background: #1a1a1a; color: #ffffff;'
      : 'background: #ffffff; color: #1a1a1a;';
  }
</script>

<div class="container" style:style={getThemeStyles()}>
  <header class="header">
    <h1 class="title">Svelte Extension</h1>
    <p class="subtitle">Built with WXT + Svelte</p>
  </header>

  {#if loading}
    <div class="loading">Loading...</div>
  {:else}
    <main class="main">
      <!-- 计数器 -->
      <section class="section">
        <h2 class="section-title">Counter</h2>
        <div class="counter-container">
          <button class="counter-btn" on:click={incrementCount}>
            Increment
          </button>
          <div class="counter-value">{storageData.count}</div>
        </div>
      </section>

      <!-- 设置 -->
      <section class="section">
        <h2 class="section-title">Settings</h2>

        <div class="setting">
          <label class="setting-label">
            <input
              type="checkbox"
              bind:checked={storageData.enabled}
              on:change={() => updateStorage('enabled', storageData.enabled)}
            />
            Enable Extension
          </label>
        </div>

        <div class="setting">
          <label class="setting-label">Theme</label>
          <select
            class="select"
            bind:value={storageData.theme}
            on:change={() => updateStorage('theme', storageData.theme)}
          >
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </div>
      </section>

      <!-- 消息提示 -->
      {#if message}
        <div class="message message-{message === 'Failed to save' || message === 'Failed to load data' || message === 'Failed to increment' ? 'error' : 'success'}">
          {message}
        </div>
      {/if}
    </main>
  {/if}
</div>

<style>
  .container {
    width: 350px;
    min-height: 400px;
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell,
      sans-serif;
    transition: background 0.3s, color 0.3s;
  }

  .header {
    margin-bottom: 24px;
    text-align: center;
  }

  .title {
    font-size: 24px;
    font-weight: 700;
    margin: 0 0 8px 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .subtitle {
    font-size: 14px;
    color: #666;
    margin: 0;
  }

  .loading {
    text-align: center;
    padding: 40px 20px;
    color: #999;
  }

  .main {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .section {
    background: #f5f5f5;
    padding: 16px;
    border-radius: 12px;
  }

  .section-title {
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 16px 0;
  }

  .counter-container {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .counter-btn {
    flex: 1;
    padding: 12px 24px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .counter-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }

  .counter-btn:active {
    transform: translateY(0);
  }

  .counter-value {
    font-size: 32px;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .setting {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
  }

  .setting:not(:last-child) {
    border-bottom: 1px solid #e0e0e0;
  }

  .setting-label {
    font-size: 14px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .setting-label input[type='checkbox'] {
    width: 18px;
    height: 18px;
    cursor: pointer;
  }

  .select {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    background: white;
  }

  .message {
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    text-align: center;
    animation: slideIn 0.3s ease-out;
  }

  .message-success {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
  }

  .message-error {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }

  @keyframes slideIn {
    from {
      transform: translateY(-10px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
</style>
