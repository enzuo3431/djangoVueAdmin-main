const state = {
  visitedViews: []
}

const mutations = {
  ADD_VISITED_VIEW(state, view) {
    if (state.visitedViews.some(v => v.path === view.path)) return
    state.visitedViews.push({
      name: view.name,
      path: view.path,
      title: view.meta && view.meta.title ? view.meta.title : 'no-name'
    })
  },
  DEL_VISITED_VIEW(state, view) {
    state.visitedViews = state.visitedViews.filter(v => v.path !== view.path)
  },
  DEL_OTHERS_VIEWS(state, view) {
    state.visitedViews = state.visitedViews.filter(v => v.path === view.path)
  },
  DEL_ALL_VIEWS(state) {
    state.visitedViews = []
  }
}

const actions = {
  addView({ commit }, view) {
    commit('ADD_VISITED_VIEW', view)
  },
  delView({ commit }, view) {
    commit('DEL_VISITED_VIEW', view)
  },
  delOthersViews({ commit }, view) {
    commit('DEL_OTHERS_VIEWS', view)
  },
  delAllViews({ commit }) {
    commit('DEL_ALL_VIEWS')
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
