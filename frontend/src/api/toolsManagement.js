import request from '@/utils/request'

export function getBenefitsStats(params) {
  return request({
    url: '/tools/benefits/stats/',
    method: 'get',
    params
  })
}

export function getBenefitsAggregate(params) {
  return request({
    url: '/tools/benefits/aggregate/',
    method: 'get',
    params
  })
}

export function uploadBenefitsFiles(data) {
  return request({
    url: '/tools/benefits/upload/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export function generateNicknames(params) {
  return request({
    url: '/tools/nickname/generate/',
    method: 'get',
    params
  })
}

export function addLiushanText(data) {
  return request({
    url: '/tools/liushan/add/',
    method: 'post',
    data
  })
}

export function previewLiushanText(data) {
  return request({
    url: '/tools/liushan/preview/',
    method: 'post',
    data
  })
}

export function commitLiushanItems(data) {
  return request({
    url: '/tools/liushan/commit/',
    method: 'post',
    data
  })
}

export function getLiushanList(params) {
  return request({
    url: '/tools/liushan/list/',
    method: 'get',
    params
  })
}

export function updateLiushanStatus(data) {
  return request({
    url: '/tools/liushan/update-status/',
    method: 'post',
    data
  })
}

export function runFileSplit(data) {
  return request({
    url: '/tools/file-split/run/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
