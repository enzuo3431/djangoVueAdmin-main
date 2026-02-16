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

export function getScriptQueues() {
  return request({
    url: '/script/queues/',
    method: 'get'
  })
}

export function createScriptQueue(data) {
  return request({
    url: '/script/queues/create/',
    method: 'post',
    data
  })
}

export function clearScriptQueue(id) {
  return request({
    url: `/script/queues/${id}/clear/`,
    method: 'post'
  })
}

export function deleteScriptQueue(id) {
  return request({
    url: `/script/queues/${id}/delete/`,
    method: 'delete'
  })
}

export function uploadScriptQueue(id, data) {
  return request({
    url: `/script/queues/${id}/upload/`,
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
