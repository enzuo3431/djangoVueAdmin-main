import router from './router'
import { getToken } from '@/utils/auth'
import store from './store'

const whiteList = ['/login', '/404']

router.beforeEach(async(to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - Django Vue Admin` : 'Django Vue Admin'

  const hasToken = getToken()

  if (hasToken) {
    if (to.path === '/login') {
      next({ path: '/' })
    } else {
      const permissions = store.getters.permissions
      const hasMenus = store.getters.menus && store.getters.menus.length > 0
      const hasRoutes = store.getters.addRoutes && store.getters.addRoutes.length > 0

      if (hasMenus && hasRoutes) {
        next()
      } else {
        try {
          // 获取用户信息
          if (!hasMenus) {
            await store.dispatch('user/getInfo')
          }

          // 生成动态路由
          const accessRoutes = await store.dispatch('permission/generateRoutes')

          // 添加动态路由
          accessRoutes.forEach(route => {
            router.addRoute(route)
          })

          // 确保路由添加完成后重新进入
          next({ ...to, replace: true })
        } catch (error) {
          console.error('路由加载失败:', error)
          await store.dispatch('user/resetToken')
          next(`/login?redirect=${to.path}`)
        }
      }
    }
  } else {
    if (whiteList.indexOf(to.path) !== -1) {
      next()
    } else {
      next(`/login?redirect=${to.path}`)
    }
  }
})
