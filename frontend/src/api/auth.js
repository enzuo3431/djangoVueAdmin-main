import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/auth/login/',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/auth/user/info/',
    method: 'get'
  })
}

export function logout(data) {
  return request({
    url: '/auth/logout/',
    method: 'post',
    data
  })
}

export function updateProfile(data) {
  return request({
    url: '/auth/user/profile/',
    method: 'post',
    data
  })
}

export function changePassword(data) {
  return request({
    url: '/auth/user/password/',
    method: 'post',
    data
  })
}

export function uploadAvatar(data) {
  return request({
    url: '/auth/user/avatar/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export function requestPasswordReset(data) {
  return request({
    url: '/auth/password/reset/request/',
    method: 'post',
    data
  })
}

export function confirmPasswordReset(data) {
  return request({
    url: '/auth/password/reset/confirm/',
    method: 'post',
    data
  })
}
