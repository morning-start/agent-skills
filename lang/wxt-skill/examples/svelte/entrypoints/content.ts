import { defineContentScript } from 'wxt/sandbox';

export default defineContentScript({
  matches: ['<all_urls>'],
  runAt: 'document_idle',
  main() {
    console.log('Svelte content script injected');

    // 创建浮动按钮
    const button = document.createElement('button');
    button.textContent = '🎨';
    button.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 2147483647;
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      cursor: pointer;
      font-size: 24px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      transition: transform 0.2s, box-shadow 0.2s;
    `;

    button.addEventListener('mouseenter', () => {
      button.style.transform = 'scale(1.1)';
      button.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.2)';
    });

    button.addEventListener('mouseleave', () => {
      button.style.transform = 'scale(1)';
      button.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
    });

    button.addEventListener('click', async () => {
      // 发送消息到 background
      const response = await browser.runtime.sendMessage({
        type: 'INCREMENT_COUNT',
      });

      console.log('Count updated:', response.count);

      // 显示通知
      const notification = document.createElement('div');
      notification.textContent = `Count: ${response.count}`;
      notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: #333;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        z-index: 2147483647;
        animation: slideIn 0.3s ease-out;
      `;

      // 添加动画
      const style = document.createElement('style');
      style.textContent = `
        @keyframes slideIn {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
      `;
      document.head.appendChild(style);

      document.body.appendChild(notification);

      // 3 秒后移除
      setTimeout(() => {
        notification.style.transition = 'opacity 0.3s ease-out';
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
      }, 3000);
    });

    document.body.appendChild(button);
  },
});
