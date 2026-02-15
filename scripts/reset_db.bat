@echo off
echo 正在清理数据库...

cd backend

echo 1. 删除所有迁移文件
for /d /r .\migrations %%i in (
    rmdir /s /q core\migrations
    rmdir /s /q api\migrations
    rmdir /s /q authentication\migrations
)

echo 2. 重新创建迁移目录
mkdir core\migrations
mkdir api\migrations
mkdir authentication\migrations
echo. > core\migrations\__init__.py
echo. > api\migrations\__init__.py
echo. > authentication\migrations\__init__.py

echo 3. 执行数据库迁移
python manage.py makemigrations
python manage.py migrate

echo 4. 初始化测试数据
python manage.py init_data

echo 数据库重置完成！
pause
