"""统一 API 响应封装。"""
from rest_framework.response import Response


def success_response(data=None, message='success', code=200, http_status=200):
    """返回成功响应结构。"""
    return Response({
        'success': True,
        'message': message,
        'code': code,
        'data': data
    }, status=http_status)


def error_response(message='error', code=400, http_status=400, errors=None):
    """返回错误响应结构，可附带错误详情。"""
    payload = {
        'success': False,
        'message': message,
        'code': code
    }
    if errors is not None:
        # 仅在传入错误详情时追加
        payload['errors'] = errors
    return Response(payload, status=http_status)
