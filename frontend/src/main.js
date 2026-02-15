import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import '@/styles/index.scss'
import directive from './directive' // 指令
import '@/permission' // 权限控制
import { formatDateTime } from '@/utils/date'

Vue.config.productionTip = false

// 全局错误处理，禁止 Element UI 弹出 MessageBox
Vue.config.errorHandler = (err, vm, info) => {
  console.error('Vue error:', err, info)
  // 阻止 Vue 默认的错误处理
  return false
}

// 完全禁止 Element UI 的 MessageBox.alert
const { MessageBox } = ElementUI
if (MessageBox && MessageBox.alert) {
  const originalAlert = MessageBox.alert
  MessageBox.alert = function(options) {
    console.warn('MessageBox.alert 被拦截:', options)
    // 转换为 Message.error
    ElementUI.Message.error(typeof options === 'string' ? options : (options.message || options))
  }
}

// 防止 Element UI 的全局错误处理
Vue.use(ElementUI, {
  // 禁止 Element UI 在错误时弹出 MessageBox
  size: 'small'
})

Vue.use(directive)

Vue.filter('datetime', formatDateTime)

// 初始化主题与暗黑模式
document.body.setAttribute('data-theme', store.state.app.theme || 'default')
if (store.state.app.darkMode) {
  document.body.classList.add('theme-dark')
}

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
