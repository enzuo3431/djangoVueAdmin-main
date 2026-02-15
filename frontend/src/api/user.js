import request from '@/utils/request'

/**
 * 获取用户列表
 */
export function getUsers(params) {
  return request({
    url: '/users/',
    method: 'get',
    params
  })
}

/**
 * 获取用户详情
 */
export function getUserDetail(id) {
  return request({
    url: `/users/${id}/`,
    method: 'get'
  })
}

/**
 * 创建用户
 */
export function createUser(data) {
  return request({
    url: '/users/create/',
    method: 'post',
    data
  })
}

/**
 * 更新用户
 */
export function updateUser(id, data) {
  return request({
    url: `/users/${id}/update/`,
    method: 'put',
    data
  })
}

/**
 * 删除用户
 */
export function deleteUser(id) {
  return request({
    url: `/users/${id}/delete/`,
    method: 'delete'
  })
}

/**
 * 分配角色
 */
export function assignRoles(id, data) {
  return request({
    url: `/users/${id}/assign-roles/`,
    method: 'post',
    data
  })
}

export function resetUserPassword(id, data) {
  return request({
    url: `/users/${id}/reset-password/`,
    method: 'post',
    data
  })
}

/**
 * 获取角色列表
 */
export function getRoles() {
  return request({
    url: '/roles/',
    method: 'get'
  })
}

/**
 * 创建角色
 */
export function createRole(data) {
  return request({
    url: '/roles/create/',
    method: 'post',
    data
  })
}

/**
 * 更新角色
 */
export function updateRole(id, data) {
  return request({
    url: `/roles/${id}/update/`,
    method: 'put',
    data
  })
}

/**
 * 删除角色
 */
export function deleteRole(id) {
  return request({
    url: `/roles/${id}/delete/`,
    method: 'delete'
  })
}

/**
 * 获取权限列表
 */
export function getPermissions() {
  return request({
    url: '/permissions/',
    method: 'get'
  })
}

/**
 * 获取所有权限（扁平结构）
 */
export function getAllPermissions() {
  return request({
    url: '/permissions/all/',
    method: 'get'
  })
}

/**
 * 创建权限
 */
export function createPermission(data) {
  return request({
    url: '/permissions/create/',
    method: 'post',
    data
  })
}

/**
 * 获取权限详情
 */
export function getPermissionDetail(id) {
  return request({
    url: `/permissions/${id}/`,
    method: 'get'
  })
}

/**
 * 更新权限
 */
export function updatePermission(id, data) {
  return request({
    url: `/permissions/${id}/update/`,
    method: 'put',
    data
  })
}

/**
 * 删除权限
 */
export function deletePermission(id) {
  return request({
    url: `/permissions/${id}/delete/`,
    method: 'delete'
  })
}

/**
 * 为角色分配权限
 */
export function assignPermissions(roleId, data) {
  return request({
    url: `/roles/${roleId}/assign-permissions/`,
    method: 'post',
    data
  })
}
