# DOCS

本文件是当前项目的详细开发文档，覆盖环境配置、权限菜单、核心模块、主题机制与常见问题。

## 1. 技术栈与模块

### 1.1 后端

- Django 4.2
- Django REST Framework
- JWT (`djangorestframework-simplejwt`)
- MySQL（推荐）
- Redis（缓存）

后端应用目录：

- `backend/apps/authentication`：登录、个人信息、密码等认证能力
- `backend/apps/core`：用户/角色/菜单/部门/日志/权限核心能力
- `backend/apps/script`：脚本配置与脚本数据
- `backend/apps/data_management`：数据管理（归档数据）
- `backend/apps/tools_management`：工具管理（活动福利、六扇门ID、昵称、文件拆分）

### 1.2 前端

- Vue2 + Element UI
- 动态菜单路由
- 黑金主题全局覆盖

主要页面目录：

- `frontend/src/views/system`
- `frontend/src/views/script`
- `frontend/src/views/data-management`
- `frontend/src/views/tools`

## 2. 环境变量与配置

项目根目录 `.env` 常用字段：

```bash
# Django
DJANGO_SECRET_KEY=replace-with-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# DB
DJANGO_USE_SQLITE=False
DJANGO_DB_NAME=django_vue_admin
DJANGO_DB_USER=root
DJANGO_DB_PASSWORD=your_password
DJANGO_DB_HOST=127.0.0.1
DJANGO_DB_PORT=3306

# Redis
REDIS_URL=redis://127.0.0.1:6379/0

# CORS
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=

# 认证会话限制（0=不限制）
AUTH_MAX_SESSIONS=1
```

说明：

- 数据库推荐 `MySQL 8`。
- Redis 缓存默认通过 `CACHES.default` 启用。
- 当 `DJANGO_USE_SQLITE=True` 时自动使用 `sqlite3`。

## 3. 初始化与运行

```bash
pip install -r requirements.txt
python backend/manage.py migrate
python backend/manage.py init_data
python backend/manage.py runserver 0.0.0.0:8000
```

前端：

```bash
cd frontend
npm install
npm run dev
```

## 4. 认证与权限

认证接口（节选）：

- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/user/info/`
- `POST /api/auth/user/profile/`
- `POST /api/auth/user/password/`
- `POST /api/auth/user/avatar/`

JWT：

- Access Token：2 小时
- Refresh Token：7 天
- Header：`Authorization: Bearer <token>`

## 5. 菜单与权限配置

唯一配置源：`backend/config/permissions.json`

同步命令：

```bash
python backend/manage.py init_data
```

规则：

- `type`: `menu` / `api` / `button`
- `parent_code`: 父级权限 code
- `sort_order`: 数值越小越靠前

建议：

- 一级菜单按 100 间隔：100, 200, 300...
- 二级菜单按 10 间隔：210, 220...
- 同级细分使用个位：251, 252...

## 6. 数据管理模块（归档数据）

后端路由：`backend/apps/data_management/urls.py`

接口：

- `GET /api/data-management/archive/`：列表
- `GET /api/data-management/archive/platform-meta/`：平台元数据
- `POST /api/data-management/archive/create/`：新增
- `PUT|PATCH /api/data-management/archive/<id>/update/`：编辑
- `DELETE /api/data-management/archive/<id>/delete/`：删除
- `POST /api/data-management/archive/import/`：批量导入
- `GET /api/data-management/archive/import/template/`：下载模板
- `POST /api/data-management/archive/sync/`：队列同步（前端当前为“未开启”提示）

### 6.1 批量导入规则（强校验）

- 仅支持 `.xlsx`
- 列名必须完全一致：
  - `phone`
  - `source`
  - `remark`
  - `platforms`
  - `is_filtered`
- 类型/格式不符合直接拒绝导入
- 导入策略为“只追加，不覆盖”
  - 文件内重复：跳过
  - 数据库已有：跳过

## 7. 工具管理模块

后端路由：`backend/apps/tools_management/urls.py`

接口：

- `GET /api/tools/nickname/generate/`：批量生成昵称
- `GET /api/tools/benefits/stats/`：活动福利单日统计
- `GET /api/tools/benefits/aggregate/`：活动福利区间累计
- `POST /api/tools/benefits/upload/`：活动福利上传（支持指定日期，不填则当天；同日期覆盖）
- `POST /api/tools/liushan/add/`：六扇门解析并入库
- `POST /api/tools/liushan/preview/`：六扇门预解析
- `POST /api/tools/liushan/commit/`：六扇门确认入库
- `GET /api/tools/liushan/list/`：六扇门列表
- `POST /api/tools/liushan/update-status/`：状态变更
- `POST /api/tools/file-split/run/`：文件拆分

### 7.1 六扇门解析规则

- 解析起点：必须从“同户人：”之后开始匹配
- 支持从大段文本中提取 `姓名 + 身份证`
- 重复规则：
  - 同一批内容内去重
  - 与数据库重复不入库

## 8. 黑金风格（全站）

### 8.1 全局策略

- 黑金模式开启后，通过全局入口统一覆盖样式。
- 颜色、边框、纹理、hover、弹窗、下拉、分页、表格线条均统一到黑金规范。
- 避免每页重复写局部 dark 样式，新增页面默认继承黑金风格。

关键文件：

- `frontend/src/store/index.js`：主题状态与切换
- `frontend/src/main.js`：初始化主题挂载
- `frontend/src/styles/index.scss`：黑金主题全局样式覆盖

### 8.2 黑金特效（仅黑金模式）

- 组件：`frontend/src/components/BlackGoldAmbient/index.vue`
- 挂载：`frontend/src/layout/index.vue`
- 当前参数：
  - 元宝数量：7
  - 闪点数量：20
- 仅黑金模式启用，其他主题默认不启用。

## 9. 常见问题

### 9.1 菜单或权限显示异常

执行：

```bash
python backend/manage.py init_data
```

并确认 `permissions.json` 配置正确、角色已绑定权限。

### 9.2 暗黑模式出现白色闪烁/白色 hover

优先检查：

- 是否有页面 scoped 样式覆盖了全局黑金变量
- 是否有 Element 默认样式优先级高于主题覆盖
- 是否有弹窗/下拉挂载到 `body` 后未被主题选择器命中

### 9.3 导入失败

按顺序排查：

1. 文件后缀必须是 `.xlsx`
2. 列名必须完全匹配模板
3. 手机号必须是 11 位合法号段

## 10. 开发约定

- 一级业务模块应拆分为独立 app（后端）和独立 views 目录（前端）。
- 新功能菜单必须同步维护到 `backend/config/permissions.json`。
- 黑金主题作为全局主题能力，默认覆盖全站；个别页面如需增强效果可单独扩展。
