import request from '@/utils/request'

export function getScriptConfigs(params) {
  return request({
    url: '/script/configs/',
    method: 'get',
    params
  })
}

export function getScriptConfigDetail(id) {
  return request({
    url: `/script/configs/${id}/`,
    method: 'get'
  })
}

export function createScriptConfig(data) {
  return request({
    url: '/script/configs/create/',
    method: 'post',
    data
  })
}

export function updateScriptConfig(id, data) {
  return request({
    url: `/script/configs/${id}/update/`,
    method: 'put',
    data
  })
}

export function deleteScriptConfig(id) {
  return request({
    url: `/script/configs/${id}/delete/`,
    method: 'delete'
  })
}
