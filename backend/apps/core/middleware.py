"""自定义中间件：认证、权限、操作日志。"""
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import logging
import json
import time

logger = logging.getLogger(__name__)


class AuthenticationMiddleware(MiddlewareMixin):
    """JWT 认证中间件"""

    def process_request(self, request):
        """处理请求，验证 JWT token"""
        # 排除不需要认证的路径
        excluded_paths = [
            '/api/health/',
            '/api/info/',
            '/api/auth/login/',
            '/api/test/',
            '/admin/',
            '/static/',
            '/media/',
        ]

        # 检查是否在排除列表中
        for path in excluded_paths:
            if request.path.startswith(path):
                return None

        try:
            # 尝试从 header 中获取 token
            jwt_auth = JWTAuthentication()
            # Authorization 头中的 token
            header = self.get_header(request)

            if header is None:
                return self.unauthorized_response('未提供认证令牌')

            # 验证 token
            # 校验 token 并获取用户
            validated_token = jwt_auth.get_validated_token(header)
            request.user = jwt_auth.get_user(validated_token)
            request.auth = validated_token

            # 检查用户是否激活
            if not request.user.is_active:
                return self.forbidden_response('账户已被禁用')

        except (InvalidToken, TokenError) as e:
            logger.warning(f"Invalid token: {e}")
            return self.unauthorized_response('认证令牌无效或已过期')
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return self.server_error_response('认证失败')

    def get_header(self, request):
        """从请求中获取 Authorization header"""
        # 标准 Authorization: Bearer <token>
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header:
            return None

        parts = auth_header.split()

        if parts[0].lower() != 'bearer':
            return None

        if len(parts) == 1:
            return None

        return parts[1]

    def unauthorized_response(self, message):
        """返回 401 响应"""
        return JsonResponse({
            'success': False,
            'message': message,
            'code': 401
        }, status=401)

    def forbidden_response(self, message):
        """返回 403 响应"""
        return JsonResponse({
            'success': False,
            'message': message,
            'code': 403
        }, status=403)

    def server_error_response(self, message):
        """返回 500 响应"""
        return JsonResponse({
            'success': False,
            'message': message,
            'code': 500
        }, status=500)


class PermissionMiddleware(MiddlewareMixin):
    """权限校验中间件"""

    def process_request(self, request):
        """处理请求，校验用户权限"""
        # 排除不需要权限校验的路径
        excluded_paths = [
            '/api/health/',
            '/api/info/',
            '/api/auth/login/',
            '/api/auth/logout/',
            '/api/auth/user/',
            '/api/test/',
            '/admin/',
            '/static/',
            '/media/',
        ]

        # 检查是否在排除列表中
        for path in excluded_paths:
            if request.path.startswith(path):
                return None

        # 超级管理员拥有所有权限
        if hasattr(request, 'user') and request.user.is_superuser:
            return None

        # TODO: 实现基于 RBAC 的权限校验
        # 这里可以根据请求路径和方法，校验用户是否有对应权限
        # 示例：检查用户是否有访问该 API 的权限

        return None


class OperationLogMiddleware(MiddlewareMixin):
    """操作日志中间件"""

    def process_request(self, request):
        # 记录请求开始时间
        request._oplog_start = time.time()

    def process_response(self, request, response):
        # 不记录的路径
        excluded_paths = [
            '/api/health/',
            '/api/info/',
            '/api/schema/',
            '/api/docs/',
            '/admin/',
            '/static/',
            '/media/',
        ]

        for path in excluded_paths:
            if request.path.startswith(path):
                return response

        try:
            from .models import OperationLog
            # 计算耗时（毫秒）
            duration_ms = int((time.time() - getattr(request, '_oplog_start', time.time())) * 1000)

            # 请求参数
            params = None
            if request.method in ['POST', 'PUT', 'PATCH']:
                try:
                    params = json.loads(request.body.decode('utf-8')) if request.body else None
                except Exception:
                    params = request.POST.dict() if hasattr(request, 'POST') else None
            else:
                params = request.GET.dict()

            # 响应内容
            response_content = None
            try:
                content = getattr(response, 'content', None)
                if content:
                    response_content = content.decode('utf-8')
                    if len(response_content) > 2000:
                        response_content = response_content[:2000] + '...'
            except Exception:
                response_content = None

            # 当前用户（可能为空）
            user = getattr(request, 'user', None)
            # 写入操作日志
            OperationLog.objects.create(
                user=user if user and user.is_authenticated else None,
                username=getattr(user, 'username', None) if user and user.is_authenticated else None,
                method=request.method,
                path=request.path,
                params=json.dumps(params, ensure_ascii=False) if params is not None else None,
                response=response_content,
                status_code=getattr(response, 'status_code', 200),
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                duration_ms=duration_ms
            )
        except Exception as e:
            logger.warning(f"OperationLog error: {e}")

        return response
