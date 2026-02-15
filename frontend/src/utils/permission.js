/**
 * 权限工具函数
 */

import store from '@/store'

/**
 * 检查用户是否具有指定权限
 * @param {string|Array} permission 权限代码或权限代码数组
 * @param {string} logical 逻辑关系 'or' 或 'and'，默认 'or'
 * @returns {boolean}
 */
export function hasPermission(permission, logical = 'or') {
  const permissions = store.getters.permissions || []

  // 超级管理员拥有所有权限
  if (permissions.includes('*:*:*')) {
    return true
  }

  const checkList = Array.isArray(permission) ? permission : [permission]

  if (logical === 'and') {
    // 需要所有权限
    return checkList.every(perm => {
      if (permissions.includes(perm)) {
        return true
      }
      // 通配符匹配
      return permissions.some(p => {
        if (p.includes('*')) {
          const pattern = p.replace(/\*/g, '.*')
          const regex = new RegExp(`^${pattern}$`)
          return regex.test(perm)
        }
        return false
      })
    })
  } else {
    // 需要任一权限（默认）
    return checkList.some(perm => {
      if (permissions.includes(perm)) {
        return true
      }
      // 通配符匹配
      return permissions.some(p => {
        if (p.includes('*')) {
          const pattern = p.replace(/\*/g, '.*')
          const regex = new RegExp(`^${pattern}$`)
          return regex.test(perm)
        }
        return false
      })
    })
  }
}

/**
 * 检查用户是否具有所有指定权限
 * @param {...string} permissions 权限代码列表
 * @returns {boolean}
 */
export function hasAllPermissions(...permissions) {
  return hasPermission(permissions, 'and')
}

/**
 * 检查用户是否具有任一指定权限
 * @param {...string} permissions 权限代码列表
 * @returns {boolean}
 */
export function hasAnyPermission(...permissions) {
  return hasPermission(permissions, 'or')
}

/**
 * 获取用户所有权限
 * @returns {Array}
 */
export function getPermissions() {
  return store.getters.permissions || []
}

/**
 * 权限过滤函数 - 用于过滤数组
 * @param {Array} list 要过滤的列表
 * @param {string} permissionKey 权限字段名
 * @param {string} logical 逻辑关系 'or' 或 'and'
 * @returns {Array}
 */
export function filterByPermission(list, permissionKey, logical = 'or') {
  const permissions = getPermissions()

  // 超级管理员返回所有
  if (permissions.includes('*:*:*')) {
    return list
  }

  return list.filter(item => {
    const itemPermissions = item[permissionKey]
    if (!itemPermissions || !itemPermissions.length) {
      return false
    }

    return hasPermission(itemPermissions, logical)
  })
}

/**
 * 路由权限检查
 * @param {Object} route 路由对象
 * @returns {boolean}
 */
export function hasRoutePermission(route) {
  // 如果路由没有设置 meta.permission，默认允许访问
  if (!route.meta || !route.meta.permission) {
    return true
  }

  const permissions = getPermissions()

  // 超级管理员拥有所有权限
  if (permissions.includes('*:*:*')) {
    return true
  }

  const routePermissions = Array.isArray(route.meta.permission)
    ? route.meta.permission
    : [route.meta.permission]

  // 检查是否具有路由所需权限
  return routePermissions.some(perm => {
    if (permissions.includes(perm)) {
      return true
    }
    // 通配符匹配
    return permissions.some(p => {
      if (p.includes('*')) {
        const pattern = p.replace(/\*/g, '.*')
        const regex = new RegExp(`^${pattern}$`)
        return regex.test(perm)
      }
      return false
    })
  })
}
