const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  userId: state => state.user.userId,
  avatar: state => state.user.avatar,
  name: state => state.user.name,
  nickname: state => state.user.nickname,
  email: state => state.user.email,
  phone: state => state.user.phone,
  gender: state => state.user.gender,
  roles: state => state.user.roles,
  permissions: state => state.user.permissions,
  menus: state => state.user.menus,
  permission_routes: state => state.permission.routes,
  addRoutes: state => state.permission.addRoutes,
  visitedViews: state => state.tagsView.visitedViews
}
export default getters
