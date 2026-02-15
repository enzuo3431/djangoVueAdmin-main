"""
RBAC权限系统 - 权限装饰器
"""
from functools import wraps
from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import HasPermission, HasPermissionCode


def permission_required(*permission_codes, logical='or'):
    """
    权限装饰器 - 检查用户是否具有指定权限

    Args:
        *permission_codes: 权限代码列表
        logical: 逻辑关系，'or' 表示拥有任一权限即可，'and' 表示需要拥有所有权限

    用法:
        @permission_required('user:add')
        def create_user(request):
            ...

        @permission_required('user:edit', 'user:delete', logical='or')
        def modify_user(request):
            ...

        @permission_required('system:config', logical='and')
        def update_config(request):
            ...
    """
    # 延迟导入，避免循环依赖
    from rest_framework.views import APIView

    def decorator(view_func):
        # 保存权限代码到视图函数
        if not hasattr(view_func, 'permission_codes'):
            view_func.permission_codes = []

        if logical == 'and':
            # 需要 'and' 逻辑，保存完整列表
            view_func.permission_codes = list(permission_codes)
            view_func.permission_logical = 'and'
        else:
            # 默认 'or' 逻辑
            view_func.permission_codes.extend(permission_codes)

        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # 检查是否已认证
            if not request.user or not request.user.is_authenticated:
                return JsonResponse({
                    'success': False,
                    'message': '请先登录',
                    'code': 401
                }, status=401)

            # 超级管理员跳过检查
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # 检查权限
            if logical == 'and':
                # 需要所有权限
                # 是否具备全部权限
                has_all = request.user.has_all_permissions(*permission_codes)
                if not has_all:
                    return JsonResponse({
                        'success': False,
                        'message': '权限不足，需要所有权限: ' + ', '.join(permission_codes),
                        'code': 403
                    }, status=403)
            else:
                # 需要任一权限
                # 是否具备任一权限
                has_any = request.user.has_any_permission(*permission_codes)
                if not has_any:
                    return JsonResponse({
                        'success': False,
                        'message': '权限不足，需要以下权限之一: ' + ', '.join(permission_codes),
                        'code': 403
                    }, status=403)

            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator


def api_permission_required(*permission_codes, logical='or'):
    """
    API权限装饰器 - 用于DRF API视图

    用法:
        @api_view(['POST'])
        @api_permission_required('user:add')
        def create_user(request):
            ...
    """
    def decorator(view_func):
        # 添加DRF权限类
        view_func = permission_classes([IsAuthenticated, HasPermission])(view_func)
        # 记录权限元数据
        view_func.permission_codes = list(permission_codes)
        view_func.permission_logical = logical
        return view_func

    return decorator


class PermissionViewMeta:
    """
    视图元数据类 - 用于声明视图权限

    用法:
        class UserListView(APIView):
            permission_codes = ['user:list']
            ...
    """
    def __init__(self, codes=None, logical='or'):
        # 权限代码列表
        self.codes = codes or []
        # 权限逻辑关系
        self.logical = logical


def permission_view(codes=None, logical='or'):
    """
    视图权限声明装饰器 - 用于类视图

    用法:
        @permission_view(codes=['user:list'])
        class UserListView(APIView):
            ...
    """
    def decorator(cls):
        cls.permission_codes = codes or []
        cls.permission_logical = logical
        return cls

    return decorator
