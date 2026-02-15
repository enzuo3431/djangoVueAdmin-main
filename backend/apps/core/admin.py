"""后台管理站点注册。"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Role, Permission, SystemConfig, UserRole, RolePermission,
    Department, RoleDepartment, LoginLog, OperationLog, UserSession, PasswordResetToken, DataPermissionRule
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """自定义用户管理展示。"""
    list_display = ['username', 'email', 'nickname', 'phone', 'gender', 'is_active', 'date_joined']
    list_filter = ['is_active', 'gender', 'date_joined']
    search_fields = ['username', 'email', 'nickname', 'phone']
    list_editable = ['nickname', 'phone', 'gender']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """角色管理展示。"""
    list_display = ['name', 'code', 'description', 'created_at']
    search_fields = ['name', 'code', 'description']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """权限管理展示。"""
    list_display = ['name', 'code', 'type', 'path', 'parent', 'created_at']
    search_fields = ['name', 'code']
    list_filter = ['type']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """用户-角色关联展示。"""
    list_display = ['user', 'role', 'created_at']
    list_filter = ['created_at']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    """角色-权限关联展示。"""
    list_display = ['role', 'permission', 'created_at']
    list_filter = ['created_at']


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    """系统配置展示。"""
    list_display = ['key', 'value', 'description', 'created_at', 'updated_at']
    search_fields = ['key', 'description']
    list_filter = ['created_at', 'updated_at']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """部门管理展示。"""
    list_display = ['name', 'parent', 'sort_order', 'is_active', 'created_at']
    search_fields = ['name']
    list_filter = ['is_active']


@admin.register(RoleDepartment)
class RoleDepartmentAdmin(admin.ModelAdmin):
    """角色-部门关联展示。"""
    list_display = ['role', 'department', 'created_at']
    list_filter = ['created_at']


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    """登录日志展示。"""
    list_display = ['username', 'status', 'ip_address', 'login_time']
    list_filter = ['status', 'login_time']
    search_fields = ['username', 'ip_address']


@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):
    """操作日志展示。"""
    list_display = ['username', 'method', 'path', 'status_code', 'created_at']
    list_filter = ['method', 'status_code', 'created_at']
    search_fields = ['username', 'path', 'ip_address']


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """会话管理展示。"""
    list_display = ['user', 'jti', 'ip_address', 'is_active', 'last_activity']
    list_filter = ['is_active', 'last_activity']
    search_fields = ['user__username', 'jti', 'ip_address']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """密码重置令牌展示。"""
    list_display = ['user', 'token', 'expires_at', 'used_at', 'created_at']
    list_filter = ['expires_at', 'used_at']
    search_fields = ['user__username', 'token']


@admin.register(DataPermissionRule)
class DataPermissionRuleAdmin(admin.ModelAdmin):
    """数据权限规则展示。"""
    list_display = ['role', 'field', 'operator', 'value', 'created_at']
    list_filter = ['operator', 'created_at']
    search_fields = ['role__name', 'field', 'value']
