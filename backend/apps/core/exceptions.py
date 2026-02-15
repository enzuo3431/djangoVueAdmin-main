"""DRF 异常统一处理。"""
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    """将 DRF 异常转为统一响应结构。"""
    response = drf_exception_handler(exc, context)

    if response is None:
        # 未被 DRF 捕获的异常，视为服务端错误
        return Response({
            'success': False,
            'message': '服务器内部错误',
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 默认错误提示
    message = '请求错误'
    if isinstance(exc, ValidationError):
        message = '参数校验失败'
    elif isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        message = '未认证或认证失败'
    elif isinstance(exc, PermissionDenied):
        message = '权限不足'

    # 统一错误响应结构
    return Response({
        'success': False,
        'message': message,
        'code': response.status_code,
        'errors': response.data
    }, status=response.status_code)
