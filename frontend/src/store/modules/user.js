import { login, logout, getInfo } from '@/api/auth'
import { getToken, setToken, removeToken } from '@/utils/auth'

const state = {
  token: getToken(),
  userId: null,
  name: '',
  avatar: '',
  nickname: '',
  email: '',
  phone: '',
  gender: '',
  roles: [],
  permissions: [],
  menus: []
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_USER_ID: (state, userId) => {
    state.userId = userId
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_NICKNAME: (state, nickname) => {
    state.nickname = nickname
  },
  SET_EMAIL: (state, email) => {
    state.email = email
  },
  SET_PHONE: (state, phone) => {
    state.phone = phone
  },
  SET_GENDER: (state, gender) => {
    state.gender = gender
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  },
  SET_PERMISSIONS: (state, permissions) => {
    state.permissions = permissions
  },
  SET_MENUS: (state, menus) => {
    state.menus = menus
  }
}

const actions = {
  // 用户登录
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        const { data } = response
        commit('SET_TOKEN', data.token)
        commit('SET_USER_ID', data.user.id)
        commit('SET_NAME', data.user.username)
        commit('SET_AVATAR', data.user.avatar || '')
        commit('SET_NICKNAME', data.user.nickname || '')
        commit('SET_EMAIL', data.user.email || '')
        commit('SET_PHONE', data.user.phone || '')
        commit('SET_GENDER', data.user.gender || '')
        commit('SET_ROLES', data.user.roles || [])
        commit('SET_PERMISSIONS', data.permissions || [])
        commit('SET_MENUS', data.menus || [])
        setToken(data.token)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // 获取用户信息
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo().then(response => {
        const { data } = response

        if (!data) {
          reject('验证失败，请重新登录。')
        }

        const { user, permissions, menus } = data

        commit('SET_NAME', user.username)
        commit('SET_USER_ID', user.id)
        commit('SET_AVATAR', user.avatar || '')
        commit('SET_NICKNAME', user.nickname || '')
        commit('SET_EMAIL', user.email || '')
        commit('SET_PHONE', user.phone || '')
        commit('SET_GENDER', user.gender || '')
        commit('SET_ROLES', user.roles || [])
        commit('SET_PERMISSIONS', permissions || [])
        commit('SET_MENUS', menus || [])

        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // 退出登录
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout().then(() => {
        commit('SET_TOKEN', '')
        commit('SET_USER_ID', null)
        commit('SET_NAME', '')
        commit('SET_AVATAR', '')
        commit('SET_NICKNAME', '')
        commit('SET_EMAIL', '')
        commit('SET_PHONE', '')
        commit('SET_GENDER', '')
        commit('SET_ROLES', [])
        commit('SET_PERMISSIONS', [])
        commit('SET_MENUS', [])
        removeToken()
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // 重置 token
  resetToken({ commit }) {
    return new Promise(resolve => {
      commit('SET_TOKEN', '')
      commit('SET_USER_ID', null)
      commit('SET_NAME', '')
      commit('SET_AVATAR', '')
      commit('SET_NICKNAME', '')
      commit('SET_EMAIL', '')
      commit('SET_PHONE', '')
      commit('SET_GENDER', '')
      commit('SET_ROLES', [])
      commit('SET_PERMISSIONS', [])
      commit('SET_MENUS', [])
      removeToken()
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
