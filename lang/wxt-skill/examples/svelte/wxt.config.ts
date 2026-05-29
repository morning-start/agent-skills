import { defineConfig } from 'wxt';

// See https://wxt.dev/guide/configuration.html
export default defineConfig({
  manifest: {
    name: 'Svelte Extension',
    version: '1.0.0',
    description: 'A browser extension built with WXT and Svelte',
    permissions: ['storage'],
  },

  // 启用 Svelte 模块
  modules: ['@wxt-dev/module-svelte'],

  // Svelte 配置
  svelte: {
    preprocess: [], // Svelte 预处理器
  },

  // 开发服务器配置
  devServer: {
    port: 3000,
  },
});
