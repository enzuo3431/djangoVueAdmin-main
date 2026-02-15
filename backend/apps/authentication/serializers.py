"""认证相关序列化器。"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.core.models import Role

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    roles = serializers.SerializerMethodField()
    department_name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
    department_id = serializers.IntegerField(source='department.id', read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'avatar', 'phone', 'gender',
                  'roles', 'department_id', 'department_name', 'date_joined', 'last_login']
        read_only_fields = ['date_joined', 'last_login']

    def get_roles(self, obj):
        """获取用户角色列表"""
        # 超级管理员返回固定角色信息
        if obj.is_superuser:
            return [{'id': 0, 'name': '超级管理员', 'code': 'admin'}]
        # 过滤未删除角色
        roles = obj.roles.filter(is_deleted=False)
        return [{'id': role.id, 'name': role.name, 'code': role.code} for role in roles]


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField(required=True, error_messages={'required': '用户名不能为空'})
    password = serializers.CharField(required=True, error_messages={'required': '密码不能为空'},
                                    write_only=True)


class RegisterSerializer(serializers.ModelSerializer):
    """注册序列化器"""
    password = serializers.CharField(required=True, write_only=True, min_length=6,
                                     error_messages={'min_length': '密码不能少于6位'})
    password_confirm = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email', 'phone']

    def validate(self, attrs):
        # 校验两次密码一致
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '两次密码不一致'})
        return attrs

    def create(self, validated_data):
        # 移除确认密码字段
        validated_data.pop('password_confirm')
        # 取出原始密码
        password = validated_data.pop('password')
        # 创建用户
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    """密码重置请求序列化器"""
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    def validate(self, attrs):
        # 至少提供用户名或邮箱
        if not attrs.get('username') and not attrs.get('email'):
            raise serializers.ValidationError('请输入用户名或邮箱')
        return attrs


class PasswordResetConfirmSerializer(serializers.Serializer):
    """密码重置确认序列化器"""
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    confirm_password = serializers.CharField(required=True, min_length=6)

    def validate(self, attrs):
        # 校验两次新密码一致
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError('两次输入的密码不一致')
        return attrs
