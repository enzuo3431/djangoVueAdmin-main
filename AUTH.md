# 认证模块使用说明

## 功能概述

已实现的认证功能：
1. ✅ 登录接口 - `/api/auth/login/`
2. ✅ 获取用户信息接口 - `/api/auth/user/info/`
3. ✅ 退出登录接口 - `/api/auth/logout/`
4. ✅ 更新个人信息接口 - `/api/auth/user/profile/`
5. ✅ 修改密码接口 - `/api/auth/user/password/`
6. ✅ JWT 认证
7. ✅ 权限模型（用户、角色、权限）
8. ✅ 前端登录页面
9. ✅ 前端个人中心页面
10. ✅ Token 拦截器
11. ✅ 401 自动跳转登录

## 后端使用说明

### 1. 安装依赖

```bash
cd backend
pip install -r ../requirements.txt
```

### 2. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 创建测试数据

```bash
python manage.py init_data
```

这会创建以下测试用户：
- **管理员**: username: `admin`, password: `admin123`
- **普通用户**: username: `user`, password: `user123`

### 4. 创建超级管理员（可选）

```bash
python manage.py createsuperuser
```

### 5. 启动服务

```bash
python manage.py runserver 8000
```

## 前端使用说明

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

### 3. 访问系统

- **登录页面**: http://localhost:9528/login
- **系统首页**: http://localhost:9528/
- **个人中心**: http://localhost:9528/profile

## API 接口说明

### 1. 登录接口

**URL**: `POST /api/auth/login/`

**请求参数**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**响应**:
```json
{
  "success": true,
  "message": "登录成功",
  "code": 200,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "nickname": "超级管理员",
      "avatar": "",
      "roles": [{"id": 0, "name": "超级管理员", "code": "admin"}]
    }
  }
}
```

### 2. 获取用户信息

**URL**: `GET /api/auth/user/info/`

**请求头**:
```
Authorization: Bearer {token}
```

**响应**:
```json
{
  "success": true,
  "message": "获取用户信息成功",
  "code": 200,
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "nickname": "超级管理员",
      "avatar": "",
      "roles": [{"id": 0, "name": "超级管理员", "code": "admin"}]
    },
    "permissions": ["dashboard:view", "system:user:view", ...]
  }
}
```

### 3. 退出登录

**URL**: `POST /api/auth/logout/`

**请求头**:
```
Authorization: Bearer {token}
```

**请求参数**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## 前端状态管理

### Store 模块

- **user**: 用户信息模块
  - `state.token`: JWT Token
  - `state.name`: 用户名
  - `state.avatar`: 头像
  - `state.roles`: 角色列表
  - `state.permissions`: 权限列表

### 主要 Actions

- `user/login`: 用户登录
- `user/getInfo`: 获取用户信息
- `user/logout`: 退出登录
- `user/resetToken`: 重置 Token

## 权限模型

### 用户模型

- `username`: 用户名（唯一）
- `password`: 密码（加密存储）
- `email`: 邮箱
- `nickname`: 昵称
- `avatar`: 头像URL
- `phone`: 手机号
- `gender`: 性别

### 角色模型

- `name`: 角色名称
- `code`: 角色代码（唯一）
- `description`: 描述
- `permissions`: 关联的权限列表

### 权限模型

- `name`: 权限名称
- `code`: 权限代码（唯一）
- `type`: 权限类型（menu/button/api）
- `path`: 路由路径

## Token 管理

### Access Token

- 有效期：2小时
- 用于API请求认证

### Refresh Token

- 有效期：7天
- 用于刷新 Access Token

## 下一步开发

1. **权限校验中间件**: 使用 `authentication.AuthenticationMiddleware`
2. **装饰器权限**: 使用 `@permission_classes([IsAuthenticated])`
3. **角色权限**: 在业务逻辑中校验用户角色和权限
4. **Remember Me**: 实现"记住我"功能
5. **第三方登录**: 集成第三方登录（如微信、GitHub）
