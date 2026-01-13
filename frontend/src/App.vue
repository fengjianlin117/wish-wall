<template>
  <div id="app" class="app-container">
    <header class="app-header">
      <h1>许愿墙 (Wish Wall)</h1>
      <p>分享你的梦想，实现你的愿望</p>
    </header>
    
    <main class="app-main">
      <section class="welcome">
        <h2>欢迎来到许愿墙</h2>
        <p>这是一个充满梦想和希望的地方。在这里，你可以分享你的愿望，浏览他人的梦想，互相鼓励和支持。</p>
      </section>
    </main>
    
    <footer class="app-footer">
      <p>&copy; 2026 Wish Wall. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
// Vue 3 Composition API setup
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem 1rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.app-header h1 {
  margin: 0;
  font-size: 2rem;
}

.app-header p {
  margin: 0.5rem 0 0 0;
  opacity: 0.9;
}

.app-main {
  flex: 1;
  padding: 2rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.welcome {
  text-align: center;
}

.welcome h2 {
  color: #333;
  margin-top: 0;
}

.welcome p {
  color: #666;
  line-height: 1.6;
}

.app-footer {
  background-color: #f5f5f5;
  text-align: center;
  padding: 2rem 1rem;
  color: #666;
  border-top: 1px solid #ddd;
}

.app-footer p {
  margin: 0;
}
</style>
