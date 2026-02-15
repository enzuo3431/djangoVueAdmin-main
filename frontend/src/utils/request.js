import axios from 'axios'
import { Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'
import router from '@/router'

const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API || 'http://localhost:8000/api',
  timeout: 10000
})

// 防止重复跳转到登录页
let isRefreshing = false
let requests = []

// Request interceptor
service.interceptors.request.use(
  config => {
    const token = getToken()
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token
    }
    return config
  },
  error => {
    console.log('Request error:', error)
    return Promise.resolve({
      __error: true,
      message: error.response?.data?.message || error.message
    })
  }
)

// Response interceptor
service.interceptors.response.use(
  response => {
    const res = response.data

    // 如果返回的数据有 success 字段且为 false，视为错误
    if (res.success === false) {
      Message({
        message: res.message || 'Error',
        type: 'error',
        duration: 5 * 1000
      })
      // 标记错误已被处理，避免在 error 拦截器中重复处理
      const error = new Error(res.message || 'Error')
      error.isHandled = true
      return Promise.resolve({
        __error: true,
        message: error.response?.data?.message || error.message
      })
    }

    return res
  },
  error => {
    console.log('Response error:', error)

    // 如果错误已经被处理过，不再显示消息
    if (error.isHandled) {
      return Promise.resolve({
        __error: true,
        message: error.response?.data?.message || error.message
      })
    }

    if (error.response) {
      const { status, data } = error.response

      // 统一处理 403 - 权限不足
      if (status === 403 || (data && data.code === 403)) {
        Message.warning({
          message: data?.message || '您没有权限访问该资源',
          showClose: true
        })
        // 标记为已处理
        Object.defineProperty(error, 'isHandled', {
          value: true,
          writable: false,
          enumerable: true
        })
        return Promise.resolve({
          __error: true,
          message: error.response?.data?.message || error.message
        })
      }

      if (status === 401) {
        // Token 过期或无效
        if (!isRefreshing) {
          isRefreshing = true
          // 清除 token
          store.dispatch('user/resetToken')
          // 使用 router.replace 跳转，避免重定向循环
          if (router.currentRoute.path !== '/login') {
            router.replace('/login')
          }
          // 2秒后重置标志，允许下次跳转
          setTimeout(() => {
            isRefreshing = false
          }, 2000)
        }
        // 标记为已处理
        Object.defineProperty(error, 'isHandled', {
          value: true,
          writable: false,
          enumerable: true
        })
        return Promise.resolve({
          __error: true,
          message: error.response?.data?.message || error.message
        })
      }

      if (status === 404) {
        Message({
          message: '请求的资源不存在',
          type: 'error',
          duration: 5 * 1000
        })
        Object.defineProperty(error, 'isHandled', {
          value: true,
          writable: false,
          enumerable: true
        })
        return Promise.resolve({
          __error: true,
          message: error.response?.data?.message || error.message
        })
      }

      if (status === 500) {
        Message({
          message: '服务器错误',
          type: 'error',
          duration: 5 * 1000
        })
        Object.defineProperty(error, 'isHandled', {
          value: true,
          writable: false,
          enumerable: true
        })
        return Promise.resolve({
          __error: true,
          message: error.response?.data?.message || error.message
        })
      }

      Message({
        message: error.response?.data?.message || error.message || '请求失败',
        type: 'error',
        duration: 5 * 1000
      })
      Object.defineProperty(error, 'isHandled', {
        value: true,
        writable: false,
        enumerable: true
      })
      return Promise.resolve({
        __error: true,
        message: error.response?.data?.message || error.message
      })
    } else if (error.code === 'ECONNABORTED') {
      Message({
        message: '请求超时',
        type: 'error',
        duration: 5 * 1000
      })
      Object.defineProperty(error, 'isHandled', {
        value: true,
        writable: false,
        enumerable: true
      })
      return Promise.resolve({
        __error: true,
        message: error.response?.data?.message || error.message
      })
    } else {
      Message({
        message: '网络错误',
        type: 'error',
        duration: 5 * 1000
      })
      Object.defineProperty(error, 'isHandled', {
        value: true,
        writable: false,
        enumerable: true
      })
      return Promise.resolve({
        __error: true,
        message: error.response?.data?.message || error.message
      })
    }
  }
)

export default service
