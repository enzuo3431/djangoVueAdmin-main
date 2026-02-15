"""
RBAC权限系统 - 自定义权限类
"""
from django.core.cache import cache
from rest_framework import permissions
from rest_framework.request import Request
from typing import List, Set


class HasPermission(permissions.BasePermission):
    """
    基于权限代码的权限检查

    用法:
        @permission_classes([HasPermission])
        def my_view(request):
            # 需要请求具有 request.permission_code 中定义的权限
            ...

        或指定权限代码:
        @permission_classes([HasPermission])
        def my_view(request):
            permission_required = ['user:add', 'user:edit']
            ...
    """

    def has_permission(self, request: Request, view):
        # 超级管理员拥有所有权限
        if request.user and request.user.is_superuser:
            return True

        # 检查是否已认证
        if not request.user or not request.user.is_authenticated:
            return False

        # 获取视图所需的权限代码
        # 从视图读取权限代码元数据
        permission_codes = getattr(view, 'permission_codes', None)

        # 如果视图没有指定权限代码，则检查是否有 permission_code 属性
        if not permission_codes:
            # 兼容单个 permission_code 属性
            permission_code = getattr(view, 'permission_code', None)
            if permission_code:
                permission_codes = [permission_code]

        # 如果没有指定权限要求，默认允许已认证用户访问
        if permission_codes is None:
            return True

        # 如果指定了空列表，表示不需要任何权限（除了登录）
        if not permission_codes:
            return True

        # 检查用户是否具有所需权限
        # 权限检查结果
        has_perm = self.check_user_permissions(request.user, permission_codes)

        # 权限不足时返回友好提示，而不是抛出错误
        if not has_perm:
            return False

    def check_user_permissions(self, user, permission_codes: List[str]) -> bool:
        """
        检查用户是否具有指定的权限

        Args:
            user: 用户实例
            permission_codes: 权限代码列表，支持通配符 *

        Returns:
            bool: 是否具有权限
        """
        # 获取用户的所有权限代码
        # 用户权限集合
        user_permissions = self.get_user_permissions(user)

        # 检查每个需要的权限
        for code in permission_codes:
            if self.has_permission_code(user_permissions, code):
                return True

        return False

    def has_permission_code(self, user_permissions: Set[str], required_code: str) -> bool:
        """
        检查用户权限集合中是否包含所需权限（支持通配符匹配）

        Args:
            user_permissions: 用户的权限代码集合
            required_code: 需要的权限代码

        Returns:
            bool: 是否具有权限
        """
        # 直接匹配
        if required_code in user_permissions:
            return True

        # 通配符匹配
        # 例如: user:* 可以匹配 user:add, user:edit, user:delete 等
        for user_perm in user_permissions:
            if '*' in user_perm:
                # 将通配符转换为正则表达式
                pattern = user_perm.replace('*', '.*')
                import re
                if re.match(f'^{pattern}$', required_code):
                    return True

        return False

    def get_user_permissions(self, user) -> Set[str]:
        """
        获取用户的所有权限代码

        Args:
            user: 用户实例

        Returns:
            Set[str]: 权限代码集合
        """
        if not user or not user.is_authenticated:
            return set()

        # 缓存 key
        cache_key = f"user_permissions:{user.id}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        # 获取用户通过角色关联的权限
        # 角色权限集合
        permissions = set()
        for role in user.roles.filter(is_deleted=False).prefetch_related('permissions'):
            for perm in role.permissions.filter(is_deleted=False):
                if perm.code:
                    permissions.add(perm.code)

        cache.set(cache_key, permissions, timeout=300)
        return permissions


class HasPermissionCode(permissions.BasePermission):
    """
    简化版权限检查 - 通过装饰器参数指定权限

    用法:
        @permission_classes([HasPermissionCode(['user:add', 'user:edit'])])
        def my_view(request):
            ...

        或使用装饰器:
        @require_permissions(['user:add', 'user:edit'])
        def my_view(request):
            ...
    """

    def __init__(self, permission_codes=None):
        super().__init__()
        # 需要的权限代码
        self.permission_codes = permission_codes or []

    def has_permission(self, request: Request, view):
        # 超级管理员拥有所有权限
        if request.user and request.user.is_superuser:
            return True

        # 检查是否已认证
        if not request.user or not request.user.is_authenticated:
            return False

        # 如果没有指定权限要求，默认允许
        if not self.permission_codes:
            return True

        # 获取视图级别的权限要求并合并
        # 视图级权限代码
        view_permissions = getattr(view, 'permission_codes', [])
        # 合并并去重
        all_permissions = list(set(self.permission_codes + view_permissions))

        if not all_permissions:
            return True

        # 检查用户权限
        # 复用 HasPermission 检查逻辑
        checker = HasPermission()
        return checker.check_user_permissions(request.user, all_permissions)


def require_permissions(*permission_codes):
    """
    权限装饰器工厂函数

    用法:
        @require_permissions('user:add', 'user:edit')
        def my_view(request):
            ...

        @require_permissions('system:config')
        @api_view(['POST'])
        def update_config(request):
            ...
    """
    from functools import wraps

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # 设置权限代码到视图函数
            wrapped_view.permission_codes = list(permission_codes)
            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator


class IsOwnerOrHasPermission(permissions.BasePermission):
    """
    对象级权限检查：资源所有者或具有特定权限的用户可以访问

    用法:
        class MyModelViewSet(ModelViewSet):
            permission_classes = [IsOwnerOrHasPermission]
            permission_codes = ['data:edit']  # 非所有者需要的权限

            def get_queryset(self):
                # 只返回用户有权限访问的对象
                return Model.objects.filter(...)
    """

    def has_object_permission(self, request: Request, view, obj):
        # 超级管理员拥有所有权限
        if request.user and request.user.is_superuser:
            return True

        # 检查是否是资源所有者
        # 资源所有者判断
        if hasattr(obj, 'owner') and obj.owner == request.user:
            return True

        if hasattr(obj, 'user') and obj.user == request.user:
            return True

        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True

        # 检查是否具有所需权限
        permission_codes = getattr(view, 'permission_codes', [])
        if permission_codes:
            # 使用通用权限检查器
            checker = HasPermission()
            return checker.check_user_permissions(request.user, permission_codes)

        return False
