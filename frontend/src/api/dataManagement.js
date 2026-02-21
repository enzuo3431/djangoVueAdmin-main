import request from '@/utils/request'

export function getArchiveDataList(params) {
  return request({
    url: '/data-management/archive/',
    method: 'get',
    params
  })
}

export function getArchivePlatformMeta() {
  return request({
    url: '/data-management/archive/platform-meta/',
    method: 'get'
  })
}

export function createArchiveData(data) {
  return request({
    url: '/data-management/archive/create/',
    method: 'post',
    data
  })
}

export function updateArchiveData(id, data) {
  return request({
    url: `/data-management/archive/${id}/update/`,
    method: 'put',
    data
  })
}

export function deleteArchiveData(id) {
  return request({
    url: `/data-management/archive/${id}/delete/`,
    method: 'delete'
  })
}

export function importArchiveData(data) {
  return request({
    url: '/data-management/archive/import/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export function syncArchiveData(data) {
  return request({
    url: '/data-management/archive/sync/',
    method: 'post',
    data
  })
}

export function getArchiveImportTemplate() {
  return request({
    url: '/data-management/archive/import/template/',
    method: 'get'
  })
}
