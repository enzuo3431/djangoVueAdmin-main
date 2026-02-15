"""认证与用户自助接口。"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import logging
import secrets
from django.utils import timezone
from django.conf import settings

from .serializers import (
    LoginSerializer, RegisterSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from apps.core.models import UserSession, LoginLog, PasswordResetToken
from apps.core.response import success_response, error_response
from apps.core.authentication import extract_access_jti

logger = logging.getLogger(__name__)
User = get_user_model()


def get_tokens_for_user(user):
    """获取用户的 JWT token"""
    # 生成 refresh/access 对
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_client_ip(request):
    """获取客户端 IP（优先代理头）。"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def get_user_agent(request):
    """获取 User-Agent。"""
    return request.META.get('HTTP_USER_AGENT', '')


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """用户登录接口"""
    # 校验登录参数
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    # 先查找用户，检查用户状态
    try:
        user = User.objects.get(username=username, is_deleted=False)
    except User.DoesNotExist:
        LoginLog.objects.create(
            username=username,
            status='failed',
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
            message='用户名不存在'
        )
        return error_response('用户名或密码错误', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    # 检查用户是否激活
    if not user.is_active:
        LoginLog.objects.create(
            user=user,
            username=username,
            status='failed',
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
            message='用户已封禁'
        )
        return error_response('用户已封禁', code=403, http_status=status.HTTP_403_FORBIDDEN)

    # 验证密码
    if not user.check_password(password):
        LoginLog.objects.create(
            user=user,
            username=username,
            status='failed',
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
            message='密码错误'
        )
        return error_response('用户名或密码错误', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    # 认证用户
    # 认证用户
    user = authenticate(request, username=username, password=password)

    # 使用 JWT 认证时不强制依赖 Session
    if hasattr(request, 'session'):
        login(request, user)

    # 生成 token
    tokens = get_tokens_for_user(user)
    # 当前 access token 的 jti
    access_jti = extract_access_jti(tokens['access'])

    # 多端登录控制
    # 最大会话数限制
    max_sessions = getattr(settings, 'AUTH_MAX_SESSIONS', 1)
    if max_sessions and max_sessions > 0:
        active_sessions = UserSession.objects.filter(user=user, is_active=True).order_by('created_at')
        overflow = active_sessions.count() - max_sessions + 1
        if overflow > 0:
            stale_ids = list(active_sessions.values_list('id', flat=True)[:overflow])
            if stale_ids:
                UserSession.objects.filter(id__in=stale_ids).update(is_active=False)

    UserSession.objects.create(
        user=user,
        jti=access_jti,
        token_type='access',
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )

    # 获取用户信息
    from .serializers import UserSerializer
    user_serializer = UserSerializer(user)

    # 获取用户权限列表
    # 权限列表
    permissions = []
    if user.is_superuser:
        permissions = ['*:*:*']
    else:
        # 通过角色获取权限
        user_roles = user.roles.filter(is_deleted=False)
        for role in user_roles:
            role_permissions = role.permissions.filter(is_deleted=False)
            for perm in role_permissions:
                if perm.code:
                    permissions.append(perm.code)

    # 获取用户菜单
    from apps.core.views import get_user_menus
    # 菜单树
    menus = get_user_menus(user)

    LoginLog.objects.create(
        user=user,
        username=username,
        status='success',
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request),
        message='登录成功'
    )

    return success_response({
        'token': tokens['access'],
        'refresh_token': tokens['refresh'],
        'user': user_serializer.data,
        'permissions': permissions,
        'menus': menus
    }, message='登录成功', code=200, http_status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """用户退出接口"""
    try:
        # 获取 refresh token 并加入黑名单
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except (InvalidToken, TokenError) as e:
                logger.warning(f"Invalid token during logout: {e}")

        # Django logout（如果存在 session）
        if hasattr(request, 'session'):
            logout(request)

        # 关闭当前 access token 会话
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.lower().startswith('bearer '):
            access_token = auth_header.split(' ', 1)[1].strip()
            try:
                access_jti = extract_access_jti(access_token)
                UserSession.objects.filter(jti=access_jti).update(is_active=False)
            except Exception:
                pass

        return success_response(message='退出成功', code=200, http_status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return error_response('退出失败', code=500, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info_view(request):
    """获取当前用户信息接口"""
    try:
        from .serializers import UserSerializer
        user_serializer = UserSerializer(request.user)

        # 获取用户权限列表
        permissions = []
        if request.user.is_superuser:
            permissions = ['*:*:*']
        else:
            # 通过角色获取权限
            user_roles = request.user.roles.filter(is_deleted=False)
            for role in user_roles:
                role_permissions = role.permissions.filter(is_deleted=False)
                for perm in role_permissions:
                    if perm.code:
                        permissions.append(perm.code)

        # 获取用户菜单
        from apps.core.views import get_user_menus
        # 用户菜单树
        menus = get_user_menus(request.user)

        return success_response({
            'user': user_serializer.data,
            'permissions': permissions,
            'menus': menus
        }, message='获取用户信息成功', code=200, http_status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Get user info error: {e}")
        return error_response('获取用户信息失败', code=500, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """更新用户信息接口"""
    try:
        # 当前用户
        user = request.user
        data = request.data

        # 允许更新的字段
        allowed_fields = ['nickname', 'avatar', 'phone', 'gender', 'email']
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])

        user.save()

        from .serializers import UserSerializer
        user_serializer = UserSerializer(user)

        return success_response(user_serializer.data, message='更新成功', code=200, http_status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Update profile error: {e}")
        return error_response('更新失败', code=500, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """修改密码接口"""
    try:
        # 读取参数
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return error_response('请输入旧密码和新密码', code=400, http_status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 6:
            return error_response('新密码不能少于6位', code=400, http_status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.check_password(old_password):
            return error_response('旧密码错误', code=400, http_status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return success_response(message='修改密码成功', code=200, http_status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Change password error: {e}")
        return error_response('修改密码失败', code=500, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request_view(request):
    """密码重置请求"""
    # 校验输入
    serializer = PasswordResetRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')

    user = None
    if username:
        user = User.objects.filter(username=username, is_deleted=False).first()
    if user is None and email:
        user = User.objects.filter(email=email, is_deleted=False).first()

    if not user:
        return success_response(message='如果用户存在，将发送重置指引', code=200, http_status=status.HTTP_200_OK)

    # 生成重置令牌
    token = secrets.token_urlsafe(24)
    # 有效期 1 小时
    expires_at = timezone.now() + timezone.timedelta(hours=1)
    PasswordResetToken.objects.create(user=user, token=token, expires_at=expires_at)

    return success_response({
        'reset_token': token,
        'expires_at': expires_at
    }, message='重置令牌已生成', code=200, http_status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm_view(request):
    """密码重置确认"""
    # 校验输入
    serializer = PasswordResetConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    token = serializer.validated_data['token']
    new_password = serializer.validated_data['new_password']

    record = PasswordResetToken.objects.filter(token=token, used_at__isnull=True).first()
    if not record:
        return error_response('重置令牌无效', code=400, http_status=status.HTTP_400_BAD_REQUEST)
    if record.expires_at < timezone.now():
        return error_response('重置令牌已过期', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    user = record.user
    user.set_password(new_password)
    user.save()
    record.used_at = timezone.now()
    record.save()

    return success_response(message='密码重置成功', code=200, http_status=status.HTTP_200_OK)
