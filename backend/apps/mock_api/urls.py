"""示例 API 路由。"""
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
]
