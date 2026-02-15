import request from '@/utils/request'

export function getLoginLogs(params) {
  return request({
    url: '/logs/login/',
    method: 'get',
    params
  })
}

export function getOperationLogs(params) {
  return request({
    url: '/logs/operation/',
    method: 'get',
    params
  })
}
