"""初始化系统基础数据的管理命令。"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import Role, Permission, UserRole, RolePermission, DataPermissionRule
from pathlib import Path
import json

User = get_user_model()


class Command(BaseCommand):
    help = '初始化系统数据，创建测试用户、角色和权限'

    def handle(self, *args, **options):
        # 命令入口
        self.stdout.write('开始初始化系统数据...')

        config = self.load_config()
        if not config:
            self.stdout.write(self.style.ERROR('未加载到配置文件，初始化终止'))
            return

        # 创建权限
        self.create_permissions(config.get('permissions', []))

        # 创建角色并分配权限
        self.create_roles_with_permissions(config.get('roles', []))

        # 创建测试用户并分配角色
        self.create_users(config.get('users', []))

        # 创建测试数据权限规则
        self.create_data_permission_rules(config.get('data_permission_rules', []))

        self.stdout.write(self.style.SUCCESS('系统数据初始化完成！'))

    def load_config(self):
        config_path = Path(__file__).resolve().parents[4] / 'config' / 'permissions.json'
        if not config_path.exists():
            self.stdout.write(self.style.ERROR(f'配置文件不存在: {config_path}'))
            return None
        try:
            return json.loads(config_path.read_text(encoding='utf-8'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'读取配置失败: {exc}'))
            return None

    def create_permissions(self, permissions_data):
        """创建权限"""
        for perm_data in permissions_data:
            if not perm_data or 'code' not in perm_data:
                continue
            parent_code = perm_data.pop('parent_code', None)
            perm, created = Permission.objects.get_or_create(
                code=perm_data['code'],
                defaults=perm_data
            )
            changed_fields = []
            for key, value in perm_data.items():
                if hasattr(perm, key) and getattr(perm, key) != value:
                    setattr(perm, key, value)
                    changed_fields.append(key)
            if parent_code:
                try:
                    parent = Permission.objects.get(code=parent_code)
                    if perm.parent_id != parent.id:
                        perm.parent = parent
                        changed_fields.append('parent')
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'父权限 {parent_code} 不存在，跳过设置父级'))
            if changed_fields:
                perm.save(update_fields=list(set(changed_fields)))
            if created:
                self.stdout.write(self.style.SUCCESS(f'创建权限: {perm.name} ({perm.code})'))

    def create_roles_with_permissions(self, roles_config):
        """创建角色并分配权限"""
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

    def create_users(self, users_config):
        """创建测试用户并分配角色"""
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

    def create_data_permission_rules(self, rules):
        """创建数据权限测试规则"""
        for rule in rules:
            role_code = rule.get('role_code')
            field = rule.get('field')
            operator = rule.get('operator')
            value = rule.get('value')
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
