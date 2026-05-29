import App from './App.svelte';
import { mount } from 'svelte';

const app = new App({
  target: document.getElementById('app')!,
});

export default app;
