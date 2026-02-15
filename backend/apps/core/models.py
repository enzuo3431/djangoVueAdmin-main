"""核心业务模型定义。"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    """基础模型类"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    """用户模型"""
    avatar = models.CharField(max_length=255, blank=True, null=True, verbose_name='头像')
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name='昵称')
    phone = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号')
    gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女')),
                              blank=True, null=True, verbose_name='性别')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='users', verbose_name='部门')
    roles = models.ManyToManyField('Role', through='UserRole', verbose_name='角色')

    class Meta:
        db_table = 'sys_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username

    def get_permissions(self):
        """
        获取用户所有权限代码列表

        Returns:
            list: 权限代码列表
        """
        if self.is_superuser:
            return ['*:*:*']  # 超级管理员拥有所有权限

        # 角色权限集合
        permissions = set()
        for role in self.roles.filter(is_deleted=False):
            for perm in role.permissions.filter(is_deleted=False):
                if perm.code:
                    permissions.add(perm.code)
        return list(permissions)

    def has_permission(self, permission_code: str) -> bool:
        """
        检查用户是否具有指定权限

        Args:
            permission_code: 权限代码，支持通配符匹配

        Returns:
            bool: 是否具有权限
        """
        if self.is_superuser:
            return True

        # 当前用户权限列表
        permissions = self.get_permissions()

        # 直接匹配
        if permission_code in permissions:
            return True

        # 通配符匹配
        import re
        for perm in permissions:
            if '*' in perm:
                pattern = perm.replace('*', '.*')
                if re.match(f'^{pattern}$', permission_code):
                    return True

        return False

    def has_any_permission(self, *permission_codes: str) -> bool:
        """
        检查用户是否具有任一指定权限

        Args:
            *permission_codes: 一个或多个权限代码

        Returns:
            bool: 是否具有任一权限
        """
        return any(self.has_permission(code) for code in permission_codes)

    def has_all_permissions(self, *permission_codes: str) -> bool:
        """
        检查用户是否具有所有指定权限

        Args:
            *permission_codes: 一个或多个权限代码

        Returns:
            bool: 是否具有所有权限
        """
        return all(self.has_permission(code) for code in permission_codes)


class Role(BaseModel):
    """角色模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='角色代码')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    data_scope = models.CharField(
        max_length=20,
        choices=(
            ('all', '全部数据权限'),
            ('dept', '本部门数据权限'),
            ('dept_and_child', '本部门及下级数据权限'),
            ('self', '仅本人数据权限'),
            ('custom', '自定义数据权限')
        ),
        default='all',
        verbose_name='数据权限范围'
    )
    departments = models.ManyToManyField('Department', through='RoleDepartment', blank=True, verbose_name='自定义部门权限')
    permissions = models.ManyToManyField('Permission', through='RolePermission', verbose_name='权限')

    class Meta:
        db_table = 'sys_role'
        verbose_name = '角色'
        verbose_name_plural = '角色'

    def __str__(self):
        return self.name


class Permission(BaseModel):
    """权限模型"""
    name = models.CharField(max_length=50, verbose_name='权限名称')
    code = models.CharField(max_length=100, unique=True, verbose_name='权限代码')
    type = models.CharField(max_length=20, choices=(('menu', '菜单'), ('button', '按钮'), ('api', '接口')),
                         verbose_name='权限类型')
    path = models.CharField(max_length=255, blank=True, null=True, verbose_name='路由路径')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                              related_name='children', verbose_name='父权限')
    # 菜单相关字段
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='菜单图标')
    sort_order = models.IntegerField(default=0, verbose_name='排序顺序')
    is_visible = models.BooleanField(default=True, verbose_name='是否显示')
    component = models.CharField(max_length=255, blank=True, null=True, verbose_name='前端组件路径')
    redirect = models.CharField(max_length=255, blank=True, null=True, verbose_name='重定向路径')

    class Meta:
        db_table = 'sys_permission'
        verbose_name = '权限'
        verbose_name_plural = '权限'

    def __str__(self):
        return self.name


class Department(BaseModel):
    """部门模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='部门名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='children', verbose_name='上级部门')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')

    class Meta:
        db_table = 'sys_department'
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def __str__(self):
        return self.name


class UserRole(BaseModel):
    """用户角色关联表"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')

    class Meta:
        db_table = 'sys_user_role'
        verbose_name = '用户角色关联'
        verbose_name_plural = '用户角色关联'
        unique_together = ['user', 'role']


class RoleDepartment(BaseModel):
    """角色-部门关联表（自定义数据权限）"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='部门')

    class Meta:
        db_table = 'sys_role_department'
        verbose_name = '角色-部门关联'
        verbose_name_plural = '角色-部门关联'
        unique_together = ['role', 'department']


class RolePermission(BaseModel):
    """角色权限关联表"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='权限')

    class Meta:
        db_table = 'sys_role_permission'
        verbose_name = '角色权限关联'
        verbose_name_plural = '角色权限关联'
        unique_together = ['role', 'permission']


class SystemConfig(BaseModel):
    """系统配置模型"""
    key = models.CharField(max_length=100, unique=True, verbose_name='配置键')
    value = models.TextField(verbose_name='配置值')
    description = models.CharField(max_length=255, blank=True, verbose_name='描述')

    class Meta:
        db_table = 'system_config'
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置'

    def __str__(self):
        return self.key


class UserSession(BaseModel):
    """用户会话（多端登录控制）"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    jti = models.CharField(max_length=64, unique=True, verbose_name='JWT ID')
    token_type = models.CharField(max_length=10, default='access', verbose_name='令牌类型')
    ip_address = models.CharField(max_length=64, blank=True, null=True, verbose_name='IP地址')
    user_agent = models.TextField(blank=True, null=True, verbose_name='User-Agent')
    last_activity = models.DateTimeField(auto_now=True, verbose_name='最后活跃时间')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        db_table = 'sys_user_session'
        verbose_name = '用户会话'
        verbose_name_plural = '用户会话'

    def __str__(self):
        return f"{self.user_id}:{self.jti}"


class LoginLog(BaseModel):
    """登录日志"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='用户')
    username = models.CharField(max_length=150, blank=True, null=True, verbose_name='用户名')
    status = models.CharField(max_length=10, choices=(('success', '成功'), ('failed', '失败')), verbose_name='状态')
    ip_address = models.CharField(max_length=64, blank=True, null=True, verbose_name='IP地址')
    user_agent = models.TextField(blank=True, null=True, verbose_name='User-Agent')
    message = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')

    class Meta:
        db_table = 'sys_login_log'
        verbose_name = '登录日志'
        verbose_name_plural = '登录日志'

    def __str__(self):
        return f"{self.username or self.user_id} - {self.status}"


class OperationLog(BaseModel):
    """操作日志"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='用户')
    username = models.CharField(max_length=150, blank=True, null=True, verbose_name='用户名')
    method = models.CharField(max_length=10, verbose_name='请求方法')
    path = models.CharField(max_length=255, verbose_name='请求路径')
    params = models.TextField(blank=True, null=True, verbose_name='请求参数')
    response = models.TextField(blank=True, null=True, verbose_name='响应结果')
    status_code = models.IntegerField(default=200, verbose_name='响应状态码')
    ip_address = models.CharField(max_length=64, blank=True, null=True, verbose_name='IP地址')
    user_agent = models.TextField(blank=True, null=True, verbose_name='User-Agent')
    duration_ms = models.IntegerField(default=0, verbose_name='耗时(毫秒)')

    class Meta:
        db_table = 'sys_operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = '操作日志'

    def __str__(self):
        return f"{self.username or self.user_id} {self.method} {self.path}"


class PasswordResetToken(BaseModel):
    """密码重置令牌"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    token = models.CharField(max_length=64, unique=True, verbose_name='重置令牌')
    expires_at = models.DateTimeField(verbose_name='过期时间')
    used_at = models.DateTimeField(null=True, blank=True, verbose_name='使用时间')

    class Meta:
        db_table = 'sys_password_reset_token'
        verbose_name = '密码重置令牌'
        verbose_name_plural = '密码重置令牌'

    def __str__(self):
        return f"{self.user_id}:{self.token}"


class DataPermissionRule(BaseModel):
    """数据权限规则（自定义条件）"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='data_rules', verbose_name='角色')
    field = models.CharField(max_length=100, verbose_name='字段名')
    operator = models.CharField(
        max_length=20,
        choices=(
            ('eq', '等于'),
            ('ne', '不等于'),
            ('lt', '小于'),
            ('lte', '小于等于'),
            ('gt', '大于'),
            ('gte', '大于等于'),
            ('in', '包含'),
            ('contains', '包含文本'),
            ('icontains', '包含文本(忽略大小写)'),
            ('startswith', '前缀匹配'),
            ('endswith', '后缀匹配'),
            ('isnull', '为空')
        ),
        verbose_name='操作符'
    )
    value = models.TextField(blank=True, null=True, verbose_name='值')

    class Meta:
        db_table = 'sys_data_permission_rule'
        verbose_name = '数据权限规则'
        verbose_name_plural = '数据权限规则'

    def __str__(self):
        return f"{self.role_id}:{self.field} {self.operator}"
