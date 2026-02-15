<template>
  <div class="debug-container">
    <h1>路由调试信息</h1>

    <div class="section">
      <h2>Store 状态</h2>
      <pre>{{ storeState }}</pre>
    </div>

    <div class="section">
      <h2>Menus 数据 ({{ menus.length }} 个)</h2>
      <pre>{{ JSON.stringify(menus, null, 2) }}</pre>
    </div>

    <div class="section">
      <h2>Routes 数据 ({{ routes.length }} 个)</h2>
      <pre>{{ JSON.stringify(routes, null, 2) }}</pre>
    </div>

    <div class="section">
      <h2>动态添加的路由 ({{ dynamicRoutes.length }} 个)</h2>
      <pre>{{ JSON.stringify(dynamicRoutes, null, 2) }}</pre>
    </div>

    <div class="section">
      <h2>完整路由配置</h2>
      <pre>{{ JSON.stringify(allRoutes, null, 2) }}</pre>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RouterDebug',
  data() {
    return {
      allRoutes: []
    }
  },
  computed: {
    storeState() {
      return this.$store.state
    },
    menus() {
      return this.$store.getters.menus || []
    },
    routes() {
      return this.$store.getters.permission_routes || []
    },
    dynamicRoutes() {
      return this.$store.getters.addRoutes || []
    }
  },
  mounted() {
    // 获取路由器中的所有路由
    this.allRoutes = this.$router.options.routes || []
    console.log('===== 调试信息 =====')
    console.log('Menus:', this.menus)
    console.log('Permission Routes:', this.routes)
    console.log('Dynamic Routes:', this.dynamicRoutes)
    console.log('All Router Options:', this.$router.options)
    console.log('=====================')
  }
}
</script>

<style scoped>
.debug-container {
  padding: 20px;
}
.section {
  margin-bottom: 30px;
  border: 1px solid #eee;
  padding: 15px;
  border-radius: 4px;
}
.section h2 {
  margin-top: 0;
  color: #409EFF;
}
pre {
  background: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  overflow: auto;
  max-height: 400px;
}
</style>
