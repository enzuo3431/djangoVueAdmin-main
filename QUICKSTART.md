# Django Vue Admin 快速启动指南

## 前置要求

在开始之前，请确保您的系统已安装以下软件：

- Python 3.8 或更高版本
- Node.js 14 或更高版本
- npm 6 或更高版本（或 yarn）
- MySQL 5.7+（可选，默认使用 SQLite）

## 第一次运行

### 步骤 1: 安装 Python 依赖

打开命令行工具，执行以下命令：

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r ../requirements.txt
```

### 步骤 2: 初始化数据库

```bash
# 确保虚拟环境已激活
# 执行数据库迁移
python manage.py migrate

# 创建超级管理员（可选）
python manage.py createsuperuser
```

### 步骤 3: 安装前端依赖

打开一个新的命令行窗口：

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

## 日常使用

### 方式一：使用启动脚本（推荐）

**Windows:**
```bash
# 双击运行
scripts\start.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/start.sh
./scripts/start.sh
```

### 方式二：手动启动

**启动后端:**
```bash
cd backend
# 激活虚拟环境
venv\Scripts\activate  # Windows
# 或
source venv/bin/activate  # Linux/Mac

# 启动服务
python manage.py runserver 8000
```

**启动前端:**
```bash
cd frontend
npm run dev
```

## 访问系统

服务启动成功后，在浏览器中访问：

- **前端管理系统**: http://localhost:9528
- **后端 API**: http://localhost:8000/api/
- **健康检查**: http://localhost:8000/api/health/
- **Django Admin**: http://localhost:8000/admin/

## 常见问题

### Q: 提示端口被占用怎么办？

A: 修改项目根目录的 `.env` 文件，更改端口配置：
```bash
DJANGO_PORT=8001  # Django 后端端口
VUE_PORT=9529     # Vue 前端端口
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

### Q: 数据库连接失败？

A: 系统默认使用 SQLite，无需配置 MySQL。如需使用 MySQL：
1. 确保MySQL服务已启动
2. 修改 `.env` 文件中的数据库配置
3. 确保数据库用户有足够的权限

## 开发提示

1. **热重载**: 前后端都支持代码修改后自动重载
2. **API 文档**: 访问后端根地址可查看可用接口
3. **调试工具**: 推荐使用 Chrome DevTools 和 Django Debug Toolbar

## 项目结构说明

```
django-vue-admin/
├── backend/           # Django 后端
│   ├── api/          # API 接口
│   ├── core/         # 核心功能
│   └── config/       # 配置文件
├── frontend/         # Vue 前端
│   ├── src/
│   │   ├── api/      # API 调用
│   │   ├── views/    # 页面组件
│   │   └── router/   # 路由配置
│   └── package.json
└── scripts/          # 启动脚本
```

## 下一步

启动成功后，您可以：

1. 浏览系统的各个功能模块
2. 查看前端页面和组件实现
3. 测试后端 API 接口
4. 开始开发自己的功能

## 技术支持

如有问题，请参考：
- 项目 README.md
- 代码中的注释
- Django 和 Vue 官方文档

祝您使用愉快！
