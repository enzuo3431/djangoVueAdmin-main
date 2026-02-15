"""清空 RBAC 相关数据的管理命令。"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import Role, Permission, UserRole, RolePermission

User = get_user_model()


class Command(BaseCommand):
    help = '清空所有系统数据（用户、角色、权限及其关联表）'

    def handle(self, *args, **options):
        # 命令入口
        self.stdout.write('开始清空系统数据...')

        # 清空用户-角色关联表
        # 统计并清空用户-角色关联
        user_role_count = UserRole.objects.count()
        UserRole.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'清空用户-角色关联表: {user_role_count} 条记录'))

        # 清空角色-权限关联表
        # 统计并清空角色-权限关联
        role_permission_count = RolePermission.objects.count()
        RolePermission.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'清空角色-权限关联表: {role_permission_count} 条记录'))

        # 清空用户表（保留超级管理员或清空所有）
        # 统计并清空用户
        user_count = User.objects.count()
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'清空用户表: {user_count} 个用户'))

        # 清空角色表
        # 统计并清空角色
        role_count = Role.objects.count()
        Role.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'清空角色表: {role_count} 个角色'))

        # 清空权限表
        # 统计并清空权限
        permission_count = Permission.objects.count()
        Permission.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'清空权限表: {permission_count} 个权限'))

        self.stdout.write(self.style.SUCCESS('数据库清空完成！'))
