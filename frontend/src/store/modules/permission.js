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
  'system/logs/operation': () => import('@/views/system/logs/operation'),
  'system/data-permissions/index': () => import('@/views/system/data-permissions')
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
      if (componentMap[menu.component]) {
        route.component = componentMap[menu.component]
      } else {
        route.component = () => import(`@/views/${menu.component}.vue`)
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
