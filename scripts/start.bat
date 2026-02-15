@echo off
echo ========================================
echo Django Vue Admin System 启动脚本
echo ========================================
echo.

echo [1] 启动后端服务 (Django)
echo [2] 启动前端服务 (Vue)
echo [3] 同时启动前后端服务
echo [4] 退出
echo.

set /p choice=请选择操作 (1-4):

if "%choice%"=="1" goto start_backend
if "%choice%"=="2" goto start_frontend
if "%choice%"=="3" goto start_all
if "%choice%"=="4" goto end
echo 无效的选择，请重新运行脚本
pause
goto end

:start_backend
echo.
echo 正在启动 Django 后端服务...
echo.
cd backend
python manage.py runserver 8000
pause
goto end

:start_frontend
echo.
echo 正在启动 Vue 前端服务...
echo.
cd frontend
npm run dev
pause
goto end

:start_all
echo.
echo 正在同时启动前后端服务...
echo.
start "Django Backend" cmd /k "cd backend && python manage.py runserver 8000"
timeout /t 3 /nobreak >nul
start "Vue Frontend" cmd /k "cd frontend && npm run dev"
echo.
echo 前后端服务已启动！
echo 后端地址: http://localhost:8000
echo 前端地址: http://localhost:9528
echo.
pause
goto end

:end
