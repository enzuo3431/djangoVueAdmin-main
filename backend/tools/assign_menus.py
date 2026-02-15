"""角色菜单分配脚本。"""
import os
import sys
import django

# 将 backend 目录加入路径，便于加载配置与应用
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import Role, Permission, RolePermission

def assign_menus_to_roles():
    """将菜单分配给角色"""

    # 获取所有菜单
    menus = Permission.objects.filter(type='menu', is_deleted=False)
    print(f'找到 {menus.count()} 个菜单')

    # 为管理员角色分配所有菜单
    admin_role = Role.objects.get(code='admin')
    manager_role = Role.objects.get(code='manager')

    for role in [admin_role, manager_role]:
        # 清除旧的菜单关联
        RolePermission.objects.filter(role=role, permission__type='menu').delete()

        # 添加菜单
        for menu in menus:
            RolePermission.objects.create(role=role, permission=menu)

        print(f'✓ 为角色 {role.name} 分配了 {menus.count()} 个菜单')

    # 为操作员分配部分菜单（不包括菜单管理）
    operator_role = Role.objects.get(code='operator')
    operator_menus = menus.exclude(code='system:menu')
    RolePermission.objects.filter(role=operator_role, permission__type='menu').delete()
    for menu in operator_menus:
        RolePermission.objects.create(role=operator_role, permission=menu)
    print(f'✓ 为角色 {operator_role.name} 分配了 {operator_menus.count()} 个菜单')

    # 为访客分配查看菜单（仪表盘和个人中心）
    viewer_role = Role.objects.get(code='viewer')
    viewer_menus = menus.filter(code__in=['dashboard:view', 'user:profile'])
    RolePermission.objects.filter(role=viewer_role, permission__type='menu').delete()
    for menu in viewer_menus:
        RolePermission.objects.create(role=viewer_role, permission=menu)
    print(f'✓ 为角色 {viewer_role.name} 分配了 {viewer_menus.count()} 个菜单')

    print('\n✅ 菜单分配完成！')

if __name__ == '__main__':
    # 脚本入口
    assign_menus_to_roles()
