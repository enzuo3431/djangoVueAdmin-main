"""Core 应用路由注册。"""
from django.urls import path
from . import views

urlpatterns = [
    # 通用接口
    path('health/', views.health_check, name='health_check'),
    path('info/', views.api_info, name='api_info'),

    # 用户管理接口
    path('users/', views.user_list_view, name='user_list'),
    path('users/create/', views.user_create_view, name='user_create'),
    path('users/<int:user_id>/', views.user_detail_view, name='user_detail'),
    path('users/<int:user_id>/update/', views.user_update_view, name='user_update'),
    path('users/<int:user_id>/delete/', views.user_delete_view, name='user_delete'),
    path('users/<int:user_id>/assign-roles/', views.assign_role_view, name='assign_roles'),
    path('users/<int:user_id>/reset-password/', views.user_reset_password_view, name='user_reset_password'),

    # 角色管理接口
    path('roles/', views.role_list_view, name='role_list'),
    path('roles/create/', views.role_create_view, name='role_create'),
    path('roles/<int:role_id>/', views.role_detail_view, name='role_detail'),
    path('roles/<int:role_id>/update/', views.role_update_view, name='role_update'),
    path('roles/<int:role_id>/delete/', views.role_delete_view, name='role_delete'),
    path('roles/<int:role_id>/assign-permissions/', views.assign_permission_view, name='assign_permissions'),

    # 权限管理接口
    path('permissions/', views.permission_list_view, name='permission_list'),
    path('permissions/all/', views.permission_all_view, name='permission_all'),
    path('permissions/<int:permission_id>/', views.permission_detail_view, name='permission_detail'),
    path('permissions/create/', views.permission_create_view, name='permission_create'),
    path('permissions/<int:permission_id>/update/', views.permission_update_view, name='permission_update'),
    path('permissions/<int:permission_id>/delete/', views.permission_delete_view, name='permission_delete'),

    # 菜单管理接口
    path('menus/user/', views.user_menu_view, name='user_menu'),
    path('menus/', views.menu_list_view, name='menu_list'),
    path('menus/create/', views.menu_create_view, name='menu_create'),
    path('menus/<int:menu_id>/update/', views.menu_update_view, name='menu_update'),
    path('menus/<int:menu_id>/delete/', views.menu_delete_view, name='menu_delete'),

    # 部门管理
    path('departments/', views.department_list_view, name='department_list'),
    path('departments/create/', views.department_create_view, name='department_create'),
    path('departments/<int:department_id>/update/', views.department_update_view, name='department_update'),
    path('departments/<int:department_id>/delete/', views.department_delete_view, name='department_delete'),

    # 日志管理
    path('logs/login/', views.login_log_list_view, name='login_log_list'),
    path('logs/operation/', views.operation_log_list_view, name='operation_log_list'),

    # 会话管理
    path('sessions/', views.user_session_list_view, name='user_session_list'),

    # 数据权限规则
    path('data-rules/', views.data_permission_rule_list_view, name='data_rule_list'),
    path('data-rules/create/', views.data_permission_rule_create_view, name='data_rule_create'),
    path('data-rules/<int:rule_id>/update/', views.data_permission_rule_update_view, name='data_rule_update'),
    path('data-rules/<int:rule_id>/delete/', views.data_permission_rule_delete_view, name='data_rule_delete'),
]
