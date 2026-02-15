"""
Core应用序列化器
"""
from rest_framework import serializers
from .models import (
    User, Role, Permission, UserRole, RolePermission,
    Department, LoginLog, OperationLog, UserSession, DataPermissionRule
)


class DepartmentSerializer(serializers.ModelSerializer):
    """部门序列化器"""
    parent_name = serializers.CharField(source='parent.name', read_only=True, allow_null=True)
    parent_id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Department
        fields = ['id', 'name', 'parent', 'parent_id', 'parent_name', 'sort_order', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器"""
    parent_name = serializers.CharField(source='parent.name', read_only=True, allow_null=True)
    parent_id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Permission
        fields = ['id', 'name', 'code', 'type', 'path', 'parent', 'parent_name', 'parent_id',
                  'icon', 'sort_order', 'is_visible', 'component', 'redirect']
        read_only_fields = ['id']


class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器"""
    permissions = PermissionSerializer(many=True, read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    department_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Role
        fields = [
            'id', 'name', 'code', 'description', 'data_scope',
            'permissions', 'permission_ids', 'departments', 'department_ids', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        # 解析关联数据
        permission_ids = validated_data.pop('permission_ids', [])
        department_ids = validated_data.pop('department_ids', [])
        # 创建角色
        role = Role.objects.create(**validated_data)
        if permission_ids:
            role.permissions.set(permission_ids)
        if department_ids:
            role.departments.set(department_ids)
        return role

    def update(self, instance, validated_data):
        # 解析关联数据
        permission_ids = validated_data.pop('permission_ids', None)
        department_ids = validated_data.pop('department_ids', None)
        # 更新基础字段
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if permission_ids is not None:
            instance.permissions.set(permission_ids)
        if department_ids is not None:
            instance.departments.set(department_ids)
        return instance


class UserRoleSerializer(serializers.ModelSerializer):
    """用户角色关联序列化器"""
    role_name = serializers.CharField(source='role.name', read_only=True)
    role_code = serializers.CharField(source='role.code', read_only=True)

    class Meta:
        model = UserRole
        fields = ['id', 'role', 'role_name', 'role_code', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserListSerializer(serializers.ModelSerializer):
    """用户列表序列化器（用于列表展示）"""
    roles = serializers.SerializerMethodField()
    role_names = serializers.SerializerMethodField()
    department_name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
    department_id = serializers.IntegerField(source='department.id', read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'nickname', 'phone', 'gender',
            'is_active', 'roles', 'role_names', 'department_id', 'department_name', 'date_joined'
        ]

    def get_roles(self, obj):
        # 返回角色简要信息
        return [{'id': r.id, 'name': r.name, 'code': r.code} for r in obj.roles.all()]

    def get_role_names(self, obj):
        # 返回角色名称列表
        return [r.name for r in obj.roles.all()]


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""
    roles = serializers.SerializerMethodField()
    user_roles = UserRoleSerializer(source='userrole_set', many=True, read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
    department_id = serializers.IntegerField(source='department.id', read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'avatar', 'phone', 'gender',
                  'is_active', 'is_staff', 'is_superuser', 'roles', 'user_roles',
                  'department_id', 'department_name',
                  'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']

    def get_roles(self, obj):
        # 返回角色 ID 列表
        return [r.id for r in obj.roles.all()]


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""
    password = serializers.CharField(write_only=True, min_length=6)
    role_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    department_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'nickname', 'phone', 'gender', 'role_ids', 'department_id']

    def create(self, validated_data):
        # 解析关联字段
        role_ids = validated_data.pop('role_ids', [])
        department_id = validated_data.pop('department_id', None)
        password = validated_data.pop('password')
        # 创建用户并设置密码
        user = User(**validated_data)
        if department_id:
            user.department_id = department_id
        user.set_password(password)
        user.save()
        if role_ids:
            # 关联角色
            for role_id in role_ids:
                UserRole.objects.create(user=user, role_id=role_id)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""
    role_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    department_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['email', 'nickname', 'phone', 'gender', 'is_active', 'role_ids', 'department_id']

    def update(self, instance, validated_data):
        # 解析关联字段
        role_ids = validated_data.pop('role_ids', None)
        department_id = validated_data.pop('department_id', None)
        # 更新基础字段
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if department_id is not None:
            instance.department_id = department_id
        instance.save()
        if role_ids is not None:
            # 删除旧角色关联
            UserRole.objects.filter(user=instance).delete()
            # 添加新角色关联
            for role_id in role_ids:
                UserRole.objects.create(user=instance, role_id=role_id)
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=6)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        # 校验两次新密码一致
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError('两次输入的密码不一致')
        return attrs


class LoginLogSerializer(serializers.ModelSerializer):
    """登录日志序列化器"""
    class Meta:
        model = LoginLog
        fields = ['id', 'username', 'status', 'ip_address', 'user_agent', 'message', 'login_time']


class OperationLogSerializer(serializers.ModelSerializer):
    """操作日志序列化器"""
    class Meta:
        model = OperationLog
        fields = [
            'id', 'username', 'method', 'path', 'params', 'response',
            'status_code', 'ip_address', 'user_agent', 'duration_ms', 'created_at'
        ]


class UserSessionSerializer(serializers.ModelSerializer):
    """用户会话序列化器"""
    class Meta:
        model = UserSession
        fields = ['id', 'jti', 'token_type', 'ip_address', 'user_agent', 'last_activity', 'is_active', 'created_at']


class DataPermissionRuleSerializer(serializers.ModelSerializer):
    """数据权限规则序列化器"""
    role_name = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = DataPermissionRule
        fields = ['id', 'role', 'role_name', 'field', 'operator', 'value', 'created_at']
        read_only_fields = ['id', 'created_at', 'role_name']
