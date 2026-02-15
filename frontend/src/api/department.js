import request from '@/utils/request'

export function getDepartments(params) {
  return request({
    url: '/departments/',
    method: 'get',
    params
  })
}

export function createDepartment(data) {
  return request({
    url: '/departments/create/',
    method: 'post',
    data
  })
}

export function updateDepartment(id, data) {
  return request({
    url: `/departments/${id}/update/`,
    method: 'put',
    data
  })
}

export function deleteDepartment(id) {
  return request({
    url: `/departments/${id}/delete/`,
    method: 'delete'
  })
}
