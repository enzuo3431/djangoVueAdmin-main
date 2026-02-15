"""自定义 JWT 认证与会话控制。"""
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken

from .models import UserSession


class SessionJWTAuthentication(JWTAuthentication):
    """
    JWT 认证 + 会话控制（多端登录控制）
    """

    def get_validated_token(self, raw_token):
        """校验 token 并检查会话是否仍有效。"""
        token = super().get_validated_token(raw_token)
        try:
            # jti 用于标识会话
            jti = token['jti']
        except KeyError as exc:
            raise InvalidToken('Token missing jti') from exc

        if not UserSession.objects.filter(jti=jti, is_active=True).exists():
            raise InvalidToken('Token is not active')

        return token

    def authenticate(self, request):
        """认证通过后更新用户会话最后活跃时间。"""
        result = super().authenticate(request)
        if result is None:
            return None

        # 解构认证结果
        user, validated_token = result
        jti = validated_token.get('jti')
        if jti:
            # 刷新会话最后活动时间
            UserSession.objects.filter(jti=jti, is_active=True).update(last_activity=timezone.now())
        return user, validated_token


def extract_access_jti(access_token_str: str) -> str:
    """从 access token 字符串解析 jti。"""
    token = AccessToken(access_token_str)
    return token.get('jti')
