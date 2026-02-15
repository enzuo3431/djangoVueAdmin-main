import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import user from './modules/user'
import permission from './modules/permission'
import tagsView from './modules/tagsView'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    user,
    permission,
    tagsView,
    app: {
      namespaced: true,
      state: {
        sidebar: {
          opened: localStorage.getItem('sidebarStatus') ? !!+localStorage.getItem('sidebarStatus') : true,
          withoutAnimation: false
        },
        device: 'desktop',
        theme: localStorage.getItem('theme') || 'default',
        darkMode: localStorage.getItem('darkMode') === '1'
      },
      mutations: {
        TOGGLE_SIDEBAR: state => {
          state.sidebar.opened = !state.sidebar.opened
          state.sidebar.withoutAnimation = false
          if (state.sidebar.opened) {
            localStorage.setItem('sidebarStatus', '1')
          } else {
            localStorage.setItem('sidebarStatus', '0')
          }
        },
        CLOSE_SIDEBAR: (state, withoutAnimation) => {
          localStorage.setItem('sidebarStatus', '0')
          state.sidebar.opened = false
          state.sidebar.withoutAnimation = withoutAnimation
        },
        TOGGLE_DEVICE: (state, device) => {
          state.device = device
        },
        SET_THEME: (state, theme) => {
          state.theme = theme
        },
        TOGGLE_DARK: state => {
          state.darkMode = !state.darkMode
        }
      },
      actions: {
        toggleSideBar({ commit }) {
          commit('TOGGLE_SIDEBAR')
        },
        closeSideBar({ commit }, { withoutAnimation }) {
          commit('CLOSE_SIDEBAR', withoutAnimation)
        },
        toggleDevice({ commit }, device) {
          commit('TOGGLE_DEVICE', device)
        },
        setTheme({ commit }, theme) {
          commit('SET_THEME', theme)
          localStorage.setItem('theme', theme)
          document.body.setAttribute('data-theme', theme)
        },
        toggleDarkMode({ commit, state }) {
          commit('TOGGLE_DARK')
          localStorage.setItem('darkMode', state.darkMode ? '1' : '0')
          document.body.classList.toggle('theme-dark', state.darkMode)
        }
      }
    }
  },
  getters
})

export default store
