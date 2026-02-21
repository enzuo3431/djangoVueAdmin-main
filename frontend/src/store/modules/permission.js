import { getUserMenus } from '@/api/menu'
import { constantRoutes } from '@/router'
import Layout from '@/layout'
import EmptyLayout from '@/layout/EmptyLayout'

const componentMap = {
  'dashboard/index': () => import('@/views/dashboard/index'),
  'profile/index': () => import('@/views/profile/index'),
  'system/users/index': () => import('@/views/system/users'),
  'system/roles/index': () => import('@/views/system/roles'),
  'system/menus/index': () => import('@/views/system/menus'),
  'system/departments/index': () => import('@/views/system/departments'),
  'system/logs/login': () => import('@/views/system/logs/login'),
  'system/logs/login/index': () => import('@/views/system/logs/login'),
  'system/logs/operation': () => import('@/views/system/logs/operation'),
  'system/logs/operation/index': () => import('@/views/system/logs/operation'),
  'system/data-permissions/index': () => import('@/views/system/data-permissions'),
  'script/data/index': () => import('@/views/script/data/index'),
  'data/archive/index': () => import('@/views/data-management/archive/index'),
  'tools/benefits/index': () => import('@/views/tools/benefits/index'),
  'tools/liushan/index': () => import('@/views/tools/liushan/index'),
  'tools/nickname/index': () => import('@/views/tools/nickname/index'),
  'tools/file-split/index': () => import('@/views/tools/file-split/index')
}

export function menusToRoutes(menus, parentPath = '') {
  const routes = []
  menus.forEach(menu => {
    let routePath = menu.path
    if (parentPath && menu.path.startsWith(parentPath + '/')) {
      routePath = menu.path.substring(parentPath.length + 1)
    }
    const route = {
      path: routePath,
      name: menu.code,
      meta: { title: menu.title, icon: menu.icon || '' }
    }
    if (menu.component === 'Layout') {
      route.component = parentPath ? EmptyLayout : Layout
    } else if (menu.component) {
      const viewComponent = componentMap[menu.component]
        ? componentMap[menu.component]
        : () => import(`@/views/${menu.component}.vue`)

      // 顶层叶子路由需要包一层 Layout，保证侧边栏与导航栏显示
      if (!parentPath && (!menu.children || menu.children.length === 0)) {
        route.component = Layout
        route.name = `${menu.code || routePath}-layout`
        route.children = [
          {
            path: '',
            name: menu.code,
            component: viewComponent,
            meta: { title: menu.title, icon: menu.icon || '' }
          }
        ]
      } else {
        route.component = viewComponent
      }
    } else {
      route.component = parentPath ? EmptyLayout : Layout
      route.redirect = menu.redirect || 'noRedirect'
    }
    if (menu.redirect) {
      route.redirect = menu.redirect
    }
    if (menu.children && menu.children.length > 0) {
      route.children = menusToRoutes(menu.children, menu.path)
    }
    routes.push(route)
  })
  return routes
}

const state = {
  routes: [],
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = constantRoutes.concat(routes)
  }
}

const actions = {
  async generateRoutes({ commit }) {
    const { data } = await getUserMenus()
    const accessedRoutes = menusToRoutes(data)
    accessedRoutes.push({ path: '*', redirect: '/404', hidden: true })
    commit('SET_ROUTES', accessedRoutes)
    return accessedRoutes
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
