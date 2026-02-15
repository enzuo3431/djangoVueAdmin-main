#!/bin/bash

echo "========================================"
echo "Django Vue Admin System 启动脚本"
echo "========================================"
echo ""

echo "[1] 启动后端服务 (Django)"
echo "[2] 启动前端服务 (Vue)"
echo "[3] 同时启动前后端服务"
echo "[4] 退出"
echo ""

read -p "请选择操作 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "正在启动 Django 后端服务..."
        echo ""
        cd backend
        python manage.py runserver 8000
        ;;
    2)
        echo ""
        echo "正在启动 Vue 前端服务..."
        echo ""
        cd frontend
        npm run dev
        ;;
    3)
        echo ""
        echo "正在同时启动前后端服务..."
        echo ""
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"'/backend && python manage.py runserver 8000"'
        sleep 3
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"'/frontend && npm run dev"'
        echo ""
        echo "前后端服务已启动！"
        echo "后端地址: http://localhost:8000"
        echo "前端地址: http://localhost:9528"
        echo ""
        ;;
    4)
        echo "退出脚本"
        exit 0
        ;;
    *)
        echo "无效的选择，请重新运行脚本"
        exit 1
        ;;
esac
