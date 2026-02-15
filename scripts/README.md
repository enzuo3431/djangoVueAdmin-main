# Django Vue Admin 启动说明

## 快速启动

### Windows 用户

双击运行 `scripts/start.bat` 脚本，按照提示选择：

- 选项 1: 仅启动 Django 后端服务
- 选项 2: 仅启动 Vue 前端服务
- 选项 3: 同时启动前后端服务（推荐）

### Linux/Mac 用户

```bash
# 给启动脚本添加执行权限
chmod +x scripts/start.sh

# 运行启动脚本
./scripts/start.sh
```

## 创建页面

根据菜单组件路径生成 Vue 页面文件（位于 `frontend/src/views`）。

```bash
node scripts/create-page.js script/santiao/index "三条配置"
```

## 手动启动

### 启动后端 (Django)

```bash
# 进入后端目录
cd backend

# 激活虚拟环境（如果已创建）
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖（首次运行）
pip install -r ../requirements.txt

# 执行数据库迁移（首次运行）
python manage.py migrate

# 启动服务
python manage.py runserver 8000
```

后端服务将在 http://localhost:8000 启动

### 启动前端 (Vue)

```bash
# 进入前端目录
cd frontend

# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:9528 启动

## 环境要求

### 后端
- Python 3.8+
- Django 4.2.11
- MySQL 5.7+ (可选，默认使用 SQLite)

### 前端
- Node.js 14+
- npm 6+ 或 yarn

## 访问地址

服务启动后，可以通过以下地址访问：

- **前端系统**: http://localhost:9528
- **后端 API**: http://localhost:8000/api
- **API 健康检查**: http://localhost:8000/api/health/
- **Django Admin**: http://localhost:8000/admin

## 默认账号

目前系统使用模拟数据，无需登录即可访问所有功能。

## 故障排除

### 端口冲突

如果端口被占用，请修改项目根目录的 `.env` 文件：

```bash
DJANGO_PORT=8001      # 修改 Django 端口
VUE_PORT=9529         # 修改 Vue 端口
```

### 依赖安装失败

**Python 依赖安装失败：**
```bash
# 使用清华镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**npm 依赖安装失败：**
```bash
# 使用淘宝镜像源
npm install --registry=https://registry.npmmirror.com
```

### 数据库连接失败

如果 MySQL 连接失败，系统会自动使用 SQLite 数据库。如需使用 MySQL，请确保：

1. MySQL 服务已启动
2. `.env` 文件中数据库配置正确
3. 已创建对应的数据库

## 开发模式

在开发模式下，前端会自动代理 API 请求到后端，无需额外配置跨域。

## 生产部署

生产环境部署时，请：

1. 修改 `.env` 文件中的配置
2. 设置 `DJANGO_DEBUG=False`
3. 构建前端资源：`npm run build:prod`
4. 配置 Nginx 或其他 Web 服务器
5. 使用 Gunicorn 或 uWSGI 运行 Django

## 技术支持

如有问题，请查看项目 README.md 或提交 Issue。
