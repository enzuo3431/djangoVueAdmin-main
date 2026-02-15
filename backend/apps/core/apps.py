"""Core 应用配置。"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = '核心应用'

    def ready(self):
        # 注册信号
        import apps.core.signals  # noqa: F401
