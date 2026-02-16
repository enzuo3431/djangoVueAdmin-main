"""认证相关路由注册。"""
from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/info/', views.user_info_view, name='user_info'),
    path('user/profile/', views.update_profile_view, name='update_profile'),
    path('user/avatar/', views.upload_avatar_view, name='upload_avatar'),
    path('user/password/', views.change_password_view, name='change_password'),
    path('password/reset/request/', views.password_reset_request_view, name='password_reset_request'),
    path('password/reset/confirm/', views.password_reset_confirm_view, name='password_reset_confirm'),
]
