import request from '@/utils/request'

export function getUserMenus() {
  return request({
    url: '/menus/user/',
    method: 'get'
  })
}

export function getMenus() {
  return request({
    url: '/menus/',
    method: 'get'
  })
}

export function createMenu(data) {
  return request({
    url: '/menus/create/',
    method: 'post',
    data
  })
}

export function updateMenu(id, data) {
  return request({
    url: `/menus/${id}/update/`,
    method: 'put',
    data
  })
}

export function deleteMenu(id) {
  return request({
    url: `/menus/${id}/delete/`,
    method: 'delete'
  })
}
