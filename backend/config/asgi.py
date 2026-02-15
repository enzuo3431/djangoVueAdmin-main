"""
ASGI config for django-vue-admin project.
"""
import os
from django.core.asgi import get_asgi_application

# 设置默认配置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# ASGI 应用入口
application = get_asgi_application()
