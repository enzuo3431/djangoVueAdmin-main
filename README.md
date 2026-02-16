# Django Vue Admin

一个基于 Django + Vue2 + Element UI 的后台管理系统模板，包含 RBAC 权限、动态菜单、脚本配置等模块。

本项目仅保留两份文档：
- `README.md`（快速上手）
- `DOCS.md`（详细说明与配置规范）

## 环境要求

- Python 3.8+
- Node.js 14+
- npm 6+（或 yarn）
- MySQL 5.7+（可选，默认 SQLite）

## 快速开始

### 后端

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r ../requirements.txt

python manage.py migrate
python manage.py init_data
python manage.py runserver 8000
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 访问地址

- 前端管理系统: http://localhost:9528
- 后端 API: http://localhost:8000/api/
- 健康检查: http://localhost:8000/api/health/
- Django Admin: http://localhost:8000/admin/

## 环境变量

项目根目录 `.env` 示例：

```bash
DJANGO_SECRET_KEY=your-secret-key-change-this-in-production
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_PORT=8000

VUE_PORT=9528
VUE_API_BASE_URL=http://localhost:8000/api
VUE_APP_TITLE=Django Vue Admin System
```

## 项目结构

```
django-vue-admin/
├── .env
├── requirements.txt
├── backend/
│   ├── manage.py
│   ├── config/
│   ├── apps/
│   │   ├── core/
│   │   ├── authentication/
│   │   ├── script/
│   │   └── mock_api/
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
└── scripts/
```

## 常见问题

### 端口被占用

修改 `.env` 中端口配置：

```bash
DJANGO_PORT=8001
VUE_PORT=9529
```

### 依赖安装慢

```bash
npm install --registry=https://registry.npmmirror.com
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 下一步

- 菜单/权限配置与 RBAC 说明请查看 `DOCS.md`
- 新增应用功能建议按 app 拆分（如 `apps/xxx`）
