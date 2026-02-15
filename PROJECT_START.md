# Django Vue Admin 项目启动说明

## 项目已创建完成！

恭喜！您的 Django + Vue Element Admin 管理系统框架已经搭建完成。

## 项目结构

```
django-vue-admin/
├── .env                      # 全局环境变量配置
├── requirements.txt          # Python 依赖
├── backend/                  # Django 后端
│   ├── manage.py            # Django 管理脚本
│   ├── config/              # 配置文件
│   ├── api/                 # API 接口
│   └── core/                # 核心功能
├── frontend/                 # Vue 前端
│   ├── package.json         # NPM 依赖
│   ├── vue.config.js        # Vue 配置
│   ├── public/              # 静态资源
│   └── src/                 # 源代码
└── scripts/                  # 启动脚本
    ├── start.bat            # Windows 启动脚本
    └── start.sh             # Linux/Mac 启动脚本
```

## 第一次启动

### 1. 安装后端依赖

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r ../requirements.txt

# 执行数据库迁移
python manage.py migrate
```

### 2. 安装前端依赖

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

### 3. 启动服务

#### 方式一：使用启动脚本（推荐）

**Windows:**
```bash
# 双击运行
scripts\start.bat
# 或在命令行中
scripts\start.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/start.sh
./scripts/start.sh
```

#### 方式二：手动启动

**启动后端（在 backend 目录下）:**
```bash
python manage.py runserver 8000
```

**启动前端（在 frontend 目录下）:**
```bash
npm run dev
```

## 访问系统

服务启动后，在浏览器中访问：

- **前端管理系统**: http://localhost:9528
- **后端 API**: http://localhost:8000/api/
- **健康检查**: http://localhost:8000/api/health/
- **Django Admin**: http://localhost:8000/admin/

## 功能特性

### 后端功能
- ✅ Django REST Framework API
- ✅ CORS 跨域支持
- ✅ 环境变量配置（从 .env 读取）
- ✅ 模块化应用结构
- ✅ 健康检查接口 `/api/health/`
- ✅ 测试数据接口 `/api/test/data/`
- ✅ 仪表盘统计接口 `/api/dashboard/stats/`
- ✅ 菜单列表接口 `/api/menu/list/`

### 前端功能
- ✅ Vue 2 + Vue Router + Vuex
- ✅ Element UI 组件库
- ✅ 响应式侧边栏布局
- ✅ 面包屑导航
- ✅ 仪表盘页面（带统计图表）
- ✅ 用户管理页面
- ✅ 角色管理页面
- ✅ 菜单管理页面
- ✅ 表格示例页面
- ✅ 表单示例页面
- ✅ 图表示例页面
- ✅ 登录页面
- ✅ 404 错误页面

## 技术栈

### 后端
- Django 4.2.11
- Django REST Framework 3.14.0
- django-cors-headers 4.3.1
- python-dotenv 1.0.1
- PyMySQL 1.1.0

### 前端
- Vue 2.7.16
- Vue Router 3.6.5
- Vuex 3.6.2
- Element UI 2.15.14
- Axios 1.6.7

## 环境变量配置

配置文件位于项目根目录的 `.env` 文件：

```bash
# Django 后端配置
DJANGO_SECRET_KEY=your-secret-key-change-this-in-production
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_PORT=8000

# Vue 前端配置
VUE_PORT=9528
VUE_API_BASE_URL=http://localhost:8000/api
VUE_APP_TITLE=Django Vue Admin System
```

## 常见问题

### Q: 端口被占用怎么办？

A: 修改 `.env` 文件中的端口配置：
```bash
DJANGO_PORT=8001  # 修改 Django 端口
VUE_PORT=9529     # 修改 Vue 端口
```

### Q: npm install 速度慢或失败？

A: 使用国内镜像源：
```bash
npm install --registry=https://registry.npmmirror.com
```

### Q: pip install 速度慢或失败？

A: 使用国内镜像源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 前端无法连接后端 API？

A: 检查以下几点：
1. 确保后端服务已启动
2. 检查 `frontend/.env.development` 中的 API 地址配置
3. 检查 `backend/config/settings.py` 中的 CORS 配置

## 下一步开发建议

1. **添加认证功能**
   - 实现用户登录/注册
   - JWT Token 认证
   - 权限管理

2. **完善业务模块**
   - 在 `backend/api/` 中添加新的 API 接口
   - 在 `frontend/src/views/` 中添加新的页面

3. **数据库设计**
   - 在 `backend/core/models.py` 中定义数据模型
   - 执行 `python manage.py makemigrations` 和 `python manage.py migrate`

4. **前后端联调**
   - 前端 API 调用位于 `frontend/src/api/`
   - 后端接口定义位于 `backend/api/views.py`

## 项目文件说明

### 后端主要文件

| 文件 | 说明 |
|------|------|
| `backend/manage.py` | Django 管理脚本 |
| `backend/config/settings.py` | Django 配置文件 |
| `backend/config/urls.py` | URL 路由配置 |
| `backend/api/views.py` | API 接口定义 |
| `backend/core/models.py` | 数据模型定义 |

### 前端主要文件

| 文件 | 说明 |
|------|------|
| `frontend/src/main.js` | 应用入口 |
| `frontend/src/router/index.js` | 路由配置 |
| `frontend/src/store/index.js` | Vuex 状态管理 |
| `frontend/src/api/` | API 接口封装 |
| `frontend/src/views/` | 页面组件 |
| `frontend/src/layout/` | 布局组件 |

## 开发技巧

1. **热重载**：前后端都支持代码修改后自动重载，无需手动重启
2. **API 调试**：可以直接访问 http://localhost:8000/api/ 查看可用接口
3. **Vue DevTools**：推荐安装 Vue DevTools 浏览器扩展进行调试
4. **代码格式化**：建议使用 ESLint 和 Prettier 保持代码风格一致

## 生产部署

生产环境部署时需要注意：

1. 设置 `DJANGO_DEBUG=False`
2. 修改 `ALLOWED_HOSTS` 配置
3. 构建前端：`npm run build:prod`
4. 使用 Gunicorn 或 uWSGI 运行 Django
5. 配置 Nginx 作为反向代理

## 技术支持

如有问题，请参考：
- 项目 README.md
- QUICKSTART.md 快速启动指南
- Django 官方文档：https://docs.djangoproject.com/
- Vue 官方文档：https://vuejs.org/
- Element UI 文档：https://element.eleme.io/

---

**祝您开发愉快！**
