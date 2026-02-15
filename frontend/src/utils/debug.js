export function debugRouter(store, router) {
  console.group('🔍 路由调试信息')

  // 检查 store 状态
  console.log('📦 Store 状态:')
  console.log('  - token:', store.getters.token)
  console.log('  - permissions:', store.getters.permissions)
  console.log('  - menus:', store.getters.menus)
  console.log('  - addRoutes:', store.getters.addRoutes)

  // 检查路由
  console.log('\n🛣️ 路由信息:')
  console.log('  - constantRoutes 数量:', router.options.routes.length)
  console.log('  - 所有路由:', router.options.routes)

  // 检查动态添加的路由
  const hasDynamicRoutes = router.options.routes.some(r => r.path === '/system')
  console.log('  - 是否有动态路由:', hasDynamicRoutes)

  console.groupEnd()

  // 返回调试信息
  return {
    hasMenus: store.getters.menus && store.getters.menus.length > 0,
    hasDynamicRoutes,
    routesCount: router.options.routes.length,
    menus: store.getters.menus
  }
}
