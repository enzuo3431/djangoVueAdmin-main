# DOCS

本文件为项目的详细说明，包含认证、权限/菜单配置、初始化流程与常见问题。

## 认证与权限

### 认证接口

- 登录: `POST /api/auth/login/`
- 获取用户信息: `GET /api/auth/user/info/`
- 退出登录: `POST /api/auth/logout/`
- 更新个人信息: `POST /api/auth/user/profile/`
- 修改密码: `POST /api/auth/user/password/`

### Token

- Access Token 有效期：2小时
- Refresh Token 有效期：7天
- 前端请求头：`Authorization: Bearer {token}`

## 菜单/权限配置（配置文件为准）

菜单与权限以 `backend/config/permissions.json` 为唯一来源，运行时会写入数据库。

### 基本规则

- `type`:
  - `menu`：菜单
  - `api`：接口权限
  - `button`：按钮权限
- `parent_code`：子菜单指向父菜单的 `code`
- `sort_order`：排序，数值越小越靠前

### 排序规则（当前约定）

- 顶级菜单 `sort_order` 从 `100` 开始，每个顶级菜单递增 `100`
- 子菜单按顶级菜单的数值递增 `10`（如 210、220、230）
- 同级子菜单细分：个位递增（如 251、252）

### 示例（节选）

```json
{
  "name": "系统管理",
  "code": "system:root",
  "type": "menu",
  "path": "/system",
  "component": "Layout",
  "icon": "el-icon-setting",
  "redirect": "/system/users",
  "sort_order": 200
},
{
  "name": "用户管理",
  "code": "system:user",
  "type": "menu",
  "path": "/system/users",
  "component": "system/users/index",
  "parent_code": "system:root",
  "sort_order": 210
}
```

## 初始化与同步

### 初始化命令

```bash
python backend/manage.py init_data
```

该命令会：
- 读取 `backend/config/permissions.json`
- 同步权限/菜单到 `sys_permission`
- 同步角色到 `sys_role` 并绑定权限
- 初始化测试用户
- 初始化数据权限规则

### 数据库与菜单表

菜单与权限写入 `sys_permission` 表（`type=menu` 表示菜单）。

### 说明

`init_data` 只做新增/更新，不会自动删除数据库中已存在的菜单记录。

## 测试账号

- 管理员: `admin / admin123`
- 管理员: `manager / manager123`
- 操作员: `operator / operator123`
- 访客: `viewer / viewer123`

## 常见问题

### 页面 404 或菜单丢失

通常是菜单未同步或权限为空：

```bash
python backend/manage.py init_data
```

### 前端无法访问后端

检查：
- `frontend/.env.development`
- `backend/config/settings.py` 的 CORS 配置

## 开发约定

- 新功能建议单独建立 app（`apps/xxx`）
- 前端页面组件放到 `frontend/src/views/xxx`
- 菜单配置统一在 `backend/config/permissions.json` 中维护
