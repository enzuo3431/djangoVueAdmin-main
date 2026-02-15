"""API 应用配置。"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.mock_api'
    verbose_name = '示例接口'
