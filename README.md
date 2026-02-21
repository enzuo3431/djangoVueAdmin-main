# Django Vue Admin

基于 `Django 4 + DRF + Vue2 + Element UI` 的后台系统，支持 JWT 认证、RBAC 权限、动态菜单，以及业务化工具模块。

当前版本已包含：
- 系统管理（用户、角色、菜单、部门、日志、数据权限）
- 脚本管理（三条配置、脚本数据）
- 数据管理（归档数据，支持 XLSX 模板导入）
- 工具管理（活动福利、六扇门ID提取、批量生成昵称、文件拆分）
- 全站黑金风格主题（含全局样式覆盖和特效）

## 环境要求

- Python 3.8+
- Node.js 14+
- npm 6+
- MySQL 8.0+（推荐）
- Redis 6+（缓存与部分业务能力）

## 快速启动

### 1) 安装依赖

```bash
pip install -r requirements.txt
cd frontend
npm install
```

### 2) 配置 `.env`

在项目根目录创建 `.env`，最少建议包含：

```bash
# Django
DJANGO_SECRET_KEY=replace-with-your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# 数据库
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
```

### 3) 初始化数据库

```bash
python backend/manage.py migrate
python backend/manage.py init_data
```

### 4) 启动服务

```bash
# 后端
python backend/manage.py runserver 0.0.0.0:8000

# 前端（新开终端）
cd frontend
npm run dev
```

## 访问地址

- 前端：`http://localhost:9528`
- 后端 API：`http://localhost:8000/api/`
- 接口文档：`http://localhost:8000/api/docs/`
- Django Admin：`http://localhost:8000/admin/`

## 默认账号

- `admin / admin123`
- `manager / manager123`
- `operator / operator123`
- `viewer / viewer123`

## 项目结构

```text
backend/
  apps/
    authentication/
    core/
    script/
    data_management/
    tools_management/
frontend/
  src/
    views/
      system/
      script/
      data-management/
      tools/
```

## 黑金模式说明

- 黑金模式通过主题切换开启。
- 开启后走全局样式覆盖，统一输入框、下拉、表格、按钮、分页、弹窗等视觉规范。
- 黑金专属特效（元宝/闪点）仅在黑金模式生效，其他主题不生效。

## 文档

- 快速使用：`README.md`
- 详细接口与规范：`DOCS.md`
