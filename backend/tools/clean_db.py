"""
数据库清理脚本
用于删除所有表并重新创建
"""
import os
import sys
import django

# 设置 Django 环境
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

from django.db import connection

def drop_all_tables():
    """删除所有表"""
    with connection.cursor() as cursor:
        # 获取所有表名
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        # 禁用外键检查
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        # 删除所有表
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"删除表: {table_name}")

        # 恢复外键检查
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    print("所有表已删除")

if __name__ == '__main__':
    # 脚本入口
    print("开始清理数据库...")
    drop_all_tables()
    print("数据库清理完成！现在可以运行迁移了：")
    print("python manage.py makemigrations")
    print("python manage.py migrate")
