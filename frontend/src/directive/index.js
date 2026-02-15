import waves from './waves'
import permission from './modules/permission'

export default {
  install(Vue) {
    Vue.directive('waves', waves)
    Vue.directive('permission', permission)
  }
}
