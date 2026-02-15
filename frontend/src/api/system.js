import request from '@/utils/request'

export function getDashboardStats() {
  return request({
    url: '/dashboard/stats/',
    method: 'get'
  })
}

export function healthCheck() {
  return request({
    url: '/health/',
    method: 'get'
  })
}
