import { defineBackground } from 'wxt/sandbox';

export default defineBackground(() => {
  console.log('Background script started');

  // 监听扩展安装
  browser.runtime.onInstalled.addListener(() => {
    console.log('Extension installed');

    // 初始化默认设置
    browser.storage.sync.set({
      theme: 'light',
      enabled: true,
      count: 0,
    });
  });

  // 监听消息
  browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'GET_STORAGE') {
      browser.storage.sync.get().then((data) => {
        sendResponse({ success: true, data });
      });
      return true; // 异步响应
    }

    if (message.type === 'SET_STORAGE') {
      browser.storage.sync.set(message.data).then(() => {
        sendResponse({ success: true });
      });
      return true;
    }

    if (message.type === 'INCREMENT_COUNT') {
      browser.storage.sync.get(['count']).then(({ count }) => {
        const newCount = (count || 0) + 1;
        browser.storage.sync.set({ count: newCount }).then(() => {
          sendResponse({ success: true, count: newCount });
        });
      });
      return true;
    }
  });
});
