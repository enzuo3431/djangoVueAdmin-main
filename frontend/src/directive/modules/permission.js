/**
 * 权限指令 v-permission
 * 用于控制页面元素的显示/隐藏
 *
 * 用法:
 * <el-button v-permission="'user:add'">添加用户</el-button>
 * <el-button v-permission="['user:edit', 'user:delete']">编辑/删除</el-button>
 *
 * 逻辑: 拥有任一权限即显示
 */
import store from '@/store'

function checkPermission(el, binding) {
  const { value } = binding
  const permissions = store.getters.permissions || []

  // 如果用户没有任何权限，隐藏所有需要权限的元素
  if (!permissions || permissions.length === 0) {
    el.parentNode && el.parentNode.removeChild(el)
    return
  }

  if (value) {
    let requiredPermissions = []

    if (typeof value === 'string') {
      requiredPermissions = [value]
    } else if (Array.isArray(value)) {
      requiredPermissions = value
    } else {
      throw new Error('v-permission 指令需要字符串或数组作为值')
    }

    const hasPermission = requiredPermissions.some(permission => {
      // 检查是否有通配符权限 *:*:*
      if (permissions.includes('*:*:*')) {
        return true
      }

      // 检查完全匹配
      if (permissions.includes(permission)) {
        return true
      }

      // 检查通配符匹配
      // 例如: user:* 可以匹配 user:add, user:edit 等
      return permissions.some(p => {
        if (p.includes('*')) {
          const pattern = p.replace(/\*/g, '.*')
          const regex = new RegExp(`^${pattern}$`)
          return regex.test(permission)
        }
        return false
      })
    })

    if (!hasPermission) {
      // 没有权限，移除元素
      el.parentNode && el.parentNode.removeChild(el)
    }
  } else {
    throw new Error('v-permission 指令需要指定权限代码')
  }
}

export default {
  inserted(el, binding) {
    checkPermission(el, binding)
  },
  update(el, binding) {
    checkPermission(el, binding)
  }
}
