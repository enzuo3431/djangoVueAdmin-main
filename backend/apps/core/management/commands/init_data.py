"""初始化系统基础数据的管理命令。"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import Role, Permission, UserRole, RolePermission, DataPermissionRule

User = get_user_model()


class Command(BaseCommand):
    help = '初始化系统数据，创建测试用户、角色和权限'

    def handle(self, *args, **options):
        # 命令入口
        self.stdout.write('开始初始化系统数据...')

        # 创建权限
        self.create_permissions()

        # 创建角色并分配权限
        self.create_roles_with_permissions()

        # 创建测试用户并分配角色
        self.create_users()

        # 创建测试数据权限规则
        self.create_data_permission_rules()

        self.stdout.write(self.style.SUCCESS('系统数据初始化完成！'))

    def create_permissions(self):
        """创建权限"""
        # 权限配置清单
        permissions_data = [
            # 仪表盘权限
            {'name': '仪表盘', 'code': 'dashboard:view', 'type': 'menu', 'path': '/dashboard'},
            {'name': '仪表盘统计', 'code': 'dashboard:stats', 'type': 'api', 'path': '/api/dashboard/stats/'},

            # 用户管理权限 (user:*)
            {'name': '用户管理', 'code': 'system:user', 'type': 'menu', 'path': '/system/users'},
            {'name': '用户列表', 'code': 'user:list', 'type': 'api', 'path': '/api/users/'},
            {'name': '用户详情', 'code': 'user:detail', 'type': 'api', 'path': '/api/users/'},
            {'name': '添加用户', 'code': 'user:add', 'type': 'api', 'path': '/api/users/create/'},
            {'name': '编辑用户', 'code': 'user:edit', 'type': 'api', 'path': '/api/users/'},
            {'name': '删除用户', 'code': 'user:delete', 'type': 'api', 'path': '/api/users/'},
            {'name': '分配用户角色', 'code': 'user:assign:role', 'type': 'api', 'path': '/api/users/'},
            {'name': '重置用户密码', 'code': 'user:reset:password', 'type': 'api', 'path': '/api/users/'},
            {'name': '导出用户', 'code': 'user:export', 'type': 'api', 'path': '/api/users/export/'},

            # 角色管理权限 (role:*)
            {'name': '角色管理', 'code': 'system:role', 'type': 'menu', 'path': '/system/roles'},
            {'name': '角色列表', 'code': 'role:list', 'type': 'api', 'path': '/api/roles/'},
            {'name': '角色详情', 'code': 'role:detail', 'type': 'api', 'path': '/api/roles/'},
            {'name': '添加角色', 'code': 'role:add', 'type': 'api', 'path': '/api/roles/create/'},
            {'name': '编辑角色', 'code': 'role:edit', 'type': 'api', 'path': '/api/roles/'},
            {'name': '删除角色', 'code': 'role:delete', 'type': 'api', 'path': '/api/roles/'},
            {'name': '分配角色权限', 'code': 'role:assign:permission', 'type': 'api', 'path': '/api/roles/'},

            # 权限管理权限 (permission:*)
            {'name': '菜单管理', 'code': 'system:menu', 'type': 'menu', 'path': '/system/menus'},
            {'name': '权限列表', 'code': 'permission:list', 'type': 'api', 'path': '/api/permissions/'},
            {'name': '所有权限', 'code': 'permission:all', 'type': 'api', 'path': '/api/permissions/all/'},
            {'name': '添加权限', 'code': 'permission:add', 'type': 'api', 'path': '/api/permissions/create/'},

            # 部门管理权限 (department:*)
            {'name': '部门管理', 'code': 'system:department', 'type': 'menu', 'path': '/system/departments'},
            {'name': '部门列表', 'code': 'department:list', 'type': 'api', 'path': '/api/departments/'},
            {'name': '添加部门', 'code': 'department:add', 'type': 'api', 'path': '/api/departments/create/'},
            {'name': '编辑部门', 'code': 'department:edit', 'type': 'api', 'path': '/api/departments/'},
            {'name': '删除部门', 'code': 'department:delete', 'type': 'api', 'path': '/api/departments/'},

            # 日志管理权限 (log:*)
            {'name': '日志管理', 'code': 'system:log', 'type': 'menu', 'path': '/system/logs'},
            {'name': '登录日志', 'code': 'log:login:list', 'type': 'api', 'path': '/api/logs/login/'},
            {'name': '操作日志', 'code': 'log:operation:list', 'type': 'api', 'path': '/api/logs/operation/'},

            # 数据权限规则
            {'name': '数据权限', 'code': 'system:data-rule', 'type': 'menu', 'path': '/system/data-rules'},
            {'name': '数据权限规则列表', 'code': 'data:rule:list', 'type': 'api', 'path': '/api/data-rules/'},
            {'name': '添加数据权限规则', 'code': 'data:rule:add', 'type': 'api', 'path': '/api/data-rules/create/'},
            {'name': '编辑数据权限规则', 'code': 'data:rule:edit', 'type': 'api', 'path': '/api/data-rules/'},
            {'name': '删除数据权限规则', 'code': 'data:rule:delete', 'type': 'api', 'path': '/api/data-rules/'},

            # 会话管理权限
            {'name': '会话列表', 'code': 'session:list', 'type': 'api', 'path': '/api/sessions/'},

            # 个人中心权限
            {'name': '个人中心', 'code': 'user:profile', 'type': 'menu', 'path': '/profile'},
            {'name': '查看个人信息', 'code': 'user:profile:view', 'type': 'api', 'path': '/api/auth/user/profile/'},
            {'name': '修改个人信息', 'code': 'user:profile:edit', 'type': 'api', 'path': '/api/auth/user/profile/'},
            {'name': '修改密码', 'code': 'user:password:change', 'type': 'api', 'path': '/api/auth/user/password/'},

            # 系统管理员权限（通配符）
            {'name': '系统管理员', 'code': 'system:admin', 'type': 'api', 'path': '/api/system/*'},
        ]

        for perm_data in permissions_data:
            perm, created = Permission.objects.get_or_create(
                code=perm_data['code'],
                defaults=perm_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'创建权限: {perm.name} ({perm.code})'))

    def create_roles_with_permissions(self):
        """创建角色并分配权限"""
        # 角色配置清单
        roles_config = [
            {
                'code': 'admin',
                'name': '超级管理员',
                'description': '系统超级管理员，拥有所有权限',
                'permissions': ['system:admin']  # 拥有系统管理员权限即可
            },
            {
                'code': 'manager',
                'name': '管理员',
                'description': '管理员，可以管理用户、角色和菜单',
                'permissions': [
                    'dashboard:view', 'dashboard:stats',
                    'system:user',
                    'user:list', 'user:detail', 'user:add', 'user:edit', 'user:delete', 'user:assign:role', 'user:reset:password',
                    'system:role',
                    'role:list', 'role:detail', 'role:add', 'role:edit', 'role:delete', 'role:assign:permission',
                    'system:menu',
                    'permission:list', 'permission:all', 'permission:add',
                    'system:department',
                    'department:list', 'department:add', 'department:edit', 'department:delete',
                    'system:log', 'log:login:list', 'log:operation:list',
                    'system:data-rule', 'data:rule:list', 'data:rule:add', 'data:rule:edit', 'data:rule:delete',
                    'session:list',
                    'user:export'
                ]
            },
            {
                'code': 'operator',
                'name': '操作员',
                'description': '操作员，可以查看和管理用户',
                'permissions': [
                    'dashboard:view', 'dashboard:stats',
                    'system:user',
                    'user:list', 'user:detail', 'user:add', 'user:edit',
                    'system:role',
                    'role:list', 'role:detail',
                    'system:menu', 'permission:list',
                    'system:department', 'department:list',
                    'system:log', 'log:login:list',
                    'system:data-rule', 'data:rule:list'
                ]
            },
            {
                'code': 'viewer',
                'name': '访客',
                'description': '访客，只能查看信息',
                'permissions': [
                    'dashboard:view', 'dashboard:stats',
                    'system:user', 'user:list', 'user:detail',
                    'system:role', 'role:list',
                    'system:menu', 'permission:list',
                    'system:log', 'log:login:list',
                    'system:data-rule', 'data:rule:list'
                ]
            },
            {
                'code': 'test',
                'name': '测试角色',
                'description': '测试角色，用于测试用户权限',
                'permissions': [
                    'dashboard:view', 'dashboard:stats',
                    'system:user', 'user:list', 'user:detail',
                    'system:role', 'role:list',
                    'system:menu', 'permission:list',
                    'system:department', 'department:list',
                    'system:data-rule', 'data:rule:list'
                ]
            }
        ]

        for role_config in roles_config:
            # 创建或获取角色
            role, created = Role.objects.get_or_create(
                code=role_config['code'],
                defaults={
                    'name': role_config['name'],
                    'description': role_config['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'创建角色: {role.name}'))

            # 分配权限
            # 角色需要的权限代码
            permission_codes = role_config['permissions']
            for perm_code in permission_codes:
                try:
                    perm = Permission.objects.get(code=perm_code)
                    RolePermission.objects.get_or_create(role=role, permission=perm)

                    # 更新角色的权限多对多关系
                    role.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'权限 {perm_code} 不存在，跳过'))

            # 清理不再需要的权限
            role.permissions.exclude(code__in=permission_codes).delete()

    def create_users(self):
        """创建测试用户并分配角色"""
        # 用户配置清单
        users_config = [
            {
                'username': 'admin',
                'password': 'admin123',
                'email': 'admin@example.com',
                'nickname': '超级管理员',
                'is_superuser': True,
                'is_staff': True,
                'role_code': None  # 超级管理员不需要角色
            },
            {
                'username': 'manager',
                'password': 'manager123',
                'email': 'manager@example.com',
                'nickname': '管理员',
                'is_superuser': False,
                'is_staff': True,
                'role_code': 'manager'
            },
            {
                'username': 'operator',
                'password': 'operator123',
                'email': 'operator@example.com',
                'nickname': '操作员',
                'is_superuser': False,
                'is_staff': True,
                'role_code': 'operator'
            },
            {
                'username': 'viewer',
                'password': 'viewer123',
                'email': 'viewer@example.com',
                'nickname': '访客',
                'is_superuser': False,
                'is_staff': False,
                'role_code': 'viewer'
            },
            {
                'username': 'user',
                'password': 'user123',
                'email': 'user@example.com',
                'nickname': '普通用户',
                'is_superuser': False,
                'is_staff': False,
                'role_code': 'viewer'  # 普通用户默认是访客角色
            },
            {
                'username': 'test',
                'password': 'test123',
                'email': 'test@example.com',
                'nickname': '测试用户',
                'is_superuser': False,
                'is_staff': True,
                'role_code': 'test'
            }
        ]

        for user_config in users_config:
            username = user_config['username']
            role_code = user_config.pop('role_code', None)

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': user_config['email'],
                    'nickname': user_config['nickname'],
                    'is_superuser': user_config['is_superuser'],
                    'is_staff': user_config['is_staff']
                }
            )

            # 更新密码（确保密码正确）
            if created or not user.check_password(user_config['password']):
                user.set_password(user_config['password'])
                user.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'创建用户: {username} ({user_config["password"]})'))
            else:
                self.stdout.write(f'用户 {username} 已存在')

            # 分配角色
            if role_code:
                try:
                    role = Role.objects.get(code=role_code)
                    UserRole.objects.get_or_create(user=user, role=role)
                    self.stdout.write(f'  -> 分配角色: {role.name}')
                except Role.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'  -> 角色 {role_code} 不存在，跳过'))
            else:
                # 清除所有角色
                UserRole.objects.filter(user=user).delete()

    def create_data_permission_rules(self):
        """创建数据权限测试规则"""
        rules = [
            # 管理员：只查看用户名包含 admin 的数据
            ('manager', 'username', 'icontains', 'admin'),
            # 操作员：只查看邮箱为 example.com 的数据
            ('operator', 'email', 'endswith', '@example.com'),
            # 访客：仅查看昵称包含 测试 的数据
            ('viewer', 'nickname', 'icontains', '测试'),
        ]

        for role_code, field, operator, value in rules:
            try:
                role = Role.objects.get(code=role_code)
            except Role.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'角色 {role_code} 不存在，跳过规则 {field}'))
                continue

            rule, created = DataPermissionRule.objects.get_or_create(
                role=role,
                field=field,
                operator=operator,
                value=value,
                defaults={'is_deleted': False}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'创建数据权限规则: {role.name} {field} {operator} {value}'
                ))
