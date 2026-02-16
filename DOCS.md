# DOCS

本文件为项目的详细说明，包含认证、权限/菜单配置、初始化流程与常见问题。

## 认证与权限

### 认证接口

- 登录: `POST /api/auth/login/`
- 获取用户信息: `GET /api/auth/user/info/`
- 退出登录: `POST /api/auth/logout/`
- 更新个人信息: `POST /api/auth/user/profile/`
- 上传头像: `POST /api/auth/user/avatar/`（`multipart/form-data`，字段 `file`）
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

## 脚本配置（三条/支付宝）

### 获取当前用户单条配置

- 接口：`GET /api/script/configs/`
- 参数：`config_type`（必填，示例：`santiao`）
- 返回：`data` 为单条对象；无配置时 `data: null`

### 公共查询（无鉴权）

用于外部脚本拉取配置：

- 接口：`GET /api/script/configs/public/`
- 参数：`user_id`、`config_type`
- 返回：`data` 为单条对象；无配置时 `data: null`

### 备注

- 后端按 `userId + configType` 作为单条配置维度
- 前端“三条配置”页面进入后若无配置会自动创建默认值

## 脚本数据（队列）

### Redis 配置

在 `.env` 中设置：

```
REDIS_URL=redis://:yourpassword@192.168.0.22:6379/0
```

### 队列结构

- Redis List：`queue:{name}`（手机号队列，左进左出）
- 数据表：`script_queue`（名称、备注、数量、创建时间）

### 队列接口

- 列表：`GET /api/script/queues/`
- 创建：`POST /api/script/queues/create/`
  - 参数：`name`（英文/下划线）、`remark`（可选）
- 清空：`POST /api/script/queues/{id}/clear/`
- 删除：`DELETE /api/script/queues/{id}/delete/`
- 上传：`POST /api/script/queues/{id}/upload/`
  - 文件：TXT（UTF-8），一行一个手机号
  - `mode`：`append`（追加）或 `overwrite`（覆盖）
  - 校验：仅 11 位中国手机号；**只对当前文件去重**

### 说明

- 删除队列为软删除，名称可复用
- `count` 由 Redis 当前长度回写

## 前端页面与菜单入口

### 页面路径（views）

- 仪表盘：`frontend/src/views/dashboard/index.vue`
- 个人中心：`frontend/src/views/profile/index.vue`
- 系统管理：
  - 用户管理：`frontend/src/views/system/users.vue`
  - 角色管理：`frontend/src/views/system/roles.vue`
  - 菜单管理：`frontend/src/views/system/menus.vue`
  - 部门管理：`frontend/src/views/system/departments.vue`
  - 登录日志：`frontend/src/views/system/logs/login.vue`
  - 操作日志：`frontend/src/views/system/logs/operation.vue`
  - 数据权限：`frontend/src/views/system/data-permissions.vue`
- 脚本管理：
  - 三条配置：`frontend/src/views/script/santiao/index.vue`
  - 支付宝配置：`frontend/src/views/script/zhifubao/index.vue`
  - 脚本数据：`frontend/src/views/script/data/index.vue`

### 菜单配置入口

菜单来源：`backend/config/permissions.json`  
运行 `python backend/manage.py init_data` 同步到数据库。

关键菜单（节选）：

- 脚本管理父级：`/script`（`component: Layout`）
- 三条配置：`/script/santiao` → `script/santiao/index`
- 支付宝配置：`/script/zhifubao` → `script/zhifubao/index`
- 脚本数据：`/script/data` → `script/data/index`

### 权限码（节选）

- `script:config:list` / `script:config:add` / `script:config:edit` / `script:config:delete`
- `script:queue:list` / `script:queue:add` / `script:queue:clear` / `script:queue:delete` / `script:queue:upload`

## 迁移与依赖

### 迁移

脚本模块新增迁移：

- `backend/apps/script/migrations/0002_remove_script_name_unique.py`
- `backend/apps/script/migrations/0003_allow_blank_reply_and_content.py`
- `backend/apps/script/migrations/0004_scriptqueue.py`

执行：

```bash
python backend/manage.py migrate
```

### 依赖

新增 Redis 客户端依赖：

```text
redis==5.0.7
```

安装：

```bash
pip install -r requirements.txt
```

## 接口示例（请求/响应）

### 脚本配置（当前用户单条）

请求：

```http
GET /api/script/configs/?config_type=santiao
Authorization: Bearer <token>
```

响应：

```json
{
  "success": true,
  "message": "success",
  "code": 200,
  "data": {
    "id": 1,
    "userId": 2,
    "name": "DDPP",
    "ipAddress": "127.0.0.1",
    "configType": "santiao",
    "addNumber": 1,
    "delayTime": 1,
    "timeIntervalAdd": 10,
    "startTime": "00:00",
    "endTime": "23:59"
  }
}
```

### 公共获取（无鉴权）

请求：

```http
GET /api/script/configs/public/?user_id=2&config_type=santiao
```

响应：

```json
{
  "success": true,
  "message": "success",
  "code": 200,
  "data": { "...": "单条配置" }
}
```

### 队列创建

请求：

```http
POST /api/script/queues/create/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "queue_test",
  "remark": "测试队列"
}
```

响应：

```json
{
  "success": true,
  "message": "创建成功",
  "code": 201,
  "data": {
    "id": 1,
    "name": "queue_test",
    "remark": "测试队列",
    "count": 0
  }
}
```

### 队列上传

请求：

```http
POST /api/script/queues/1/upload/
Authorization: Bearer <token>
Content-Type: multipart/form-data

file=<TXT文件>&mode=append
```

响应：

```json
{
  "success": true,
  "message": "上传成功",
  "code": 200,
  "data": {
    "count": 120,
    "added": 120,
    "mode": "append"
  }
}
```

### 队列清空

请求：

```http
POST /api/script/queues/1/clear/
Authorization: Bearer <token>
```

响应：

```json
{
  "success": true,
  "message": "清空成功",
  "code": 200,
  "data": null
}
```

### 队列删除

请求：

```http
DELETE /api/script/queues/1/delete/
Authorization: Bearer <token>
```

响应：

```json
{
  "success": true,
  "message": "删除成功",
  "code": 200,
  "data": null
}
```

## 前端路由映射说明

动态菜单路由通过 `frontend/src/store/modules/permission.js` 的 `componentMap` 映射到具体页面。

常用映射（节选）：

```js
const componentMap = {
  'system/logs/login': () => import('@/views/system/logs/login'),
  'system/logs/operation': () => import('@/views/system/logs/operation'),
  'script/santiao/index': () => import('@/views/script/santiao/index'),
  'script/zhifubao/index': () => import('@/views/script/zhifubao/index'),
  'script/data/index': () => import('@/views/script/data/index')
}
```

## 启动与部署

### 后端启动（本地）

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py init_data
python manage.py runserver 0.0.0.0:8000
```

### 前端启动（本地）

```bash
cd frontend
npm install
npm run dev
```

### 常用环境变量（.env）

```
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_USE_SQLITE=False
DJANGO_DB_NAME=django_vue_admin
DJANGO_DB_USER=root
DJANGO_DB_PASSWORD=yourpassword
DJANGO_DB_HOST=localhost
DJANGO_DB_PORT=3306
REDIS_URL=redis://:yourpassword@192.168.0.22:6379/0
```

### 部署建议（简要）

- 后端：Gunicorn / uWSGI + Nginx
- 前端：`npm run build` 后静态部署
- Redis：保证网络可达并配置 `REDIS_URL`


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
