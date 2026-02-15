"""初始化默认菜单脚本。"""
import os
import sys
import django

# 将 backend 目录加入路径，便于加载配置与应用
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import Permission

def create_default_menus():
    """创建默认菜单数据"""

    # 首先更新仪表盘菜单
    dashboard, _ = Permission.objects.get_or_create(
        code='dashboard:view',
        defaults={
            'name': '仪表盘',
            'type': 'menu',
            'path': '/dashboard',
            'component': 'dashboard/index',
            'icon': 'el-icon-s-data',
            'sort_order': 0,
            'is_visible': True
        }
    )
    # 更新字段
    dashboard.type = 'menu'
    dashboard.path = '/dashboard'
    dashboard.component = 'dashboard/index'
    dashboard.icon = 'el-icon-s-data'
    dashboard.sort_order = 0
    dashboard.is_visible = True
    dashboard.save()
    print(f'✓ 创建/更新仪表盘菜单: {dashboard.name}')

    # 创建系统管理父菜单
    # 系统管理父菜单
    system_menu, created = Permission.objects.get_or_create(
        code='system',
        defaults={
            'name': '系统管理',
            'type': 'menu',
            'path': '/system',
            'component': 'Layout',
            'icon': 'el-icon-setting',
            'sort_order': 100,
            'is_visible': True
        }
    )
    if created:
        print(f'✓ 创建系统管理父菜单: {system_menu.name}')
    else:
        system_menu.name = '系统管理'
        system_menu.type = 'menu'
        system_menu.path = '/system'
        system_menu.component = 'Layout'
        system_menu.icon = 'el-icon-setting'
        system_menu.sort_order = 100
        system_menu.is_visible = True
        system_menu.save()
        print(f'✓ 更新系统管理父菜单: {system_menu.name}')

    # ========== 用户管理菜单 ==========
    # 用户管理菜单
    user_menu, created = Permission.objects.get_or_create(
        code='system:user',
        defaults={
            'name': '用户管理',
            'type': 'menu',
            'path': '/system/users',
            'component': 'system/users/index',
            'icon': 'el-icon-user',
            'sort_order': 1,
            'is_visible': True,
            'parent': system_menu
        }
    )
    if created:
        print(f'✓ 创建用户管理菜单: {user_menu.name}')
    else:
        user_menu.name = '用户管理'
        user_menu.type = 'menu'
        user_menu.path = '/system/users'
        user_menu.component = 'system/users/index'
        user_menu.icon = 'el-icon-user'
        user_menu.sort_order = 1
        user_menu.is_visible = True
        user_menu.parent = system_menu
        user_menu.save()
        print(f'✓ 更新用户管理菜单: {user_menu.name}')

    # 用户管理子权限（按钮）
    # 用户管理按钮权限
    user_permissions = [
        ('user:list', '用户列表'),
        ('user:add', '添加用户'),
        ('user:edit', '编辑用户'),
        ('user:delete', '删除用户'),
        ('user:assign:role', '分配角色'),
        ('user:reset:password', '重置密码'),
    ]
    for code, name in user_permissions:
        perm, created = Permission.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'type': 'button',
                'sort_order': 1,
                'is_visible': False,
                'parent': user_menu
            }
        )
        if not created:
            perm.type = 'button'
            perm.is_visible = False
            perm.parent = user_menu
            perm.save()

    # ========== 角色管理菜单 ==========
    # 角色管理菜单
    role_menu, created = Permission.objects.get_or_create(
        code='system:role',
        defaults={
            'name': '角色管理',
            'type': 'menu',
            'path': '/system/roles',
            'component': 'system/roles/index',
            'icon': 'el-icon-s-custom',
            'sort_order': 2,
            'is_visible': True,
            'parent': system_menu
        }
    )
    if created:
        print(f'✓ 创建角色管理菜单: {role_menu.name}')
    else:
        role_menu.name = '角色管理'
        role_menu.type = 'menu'
        role_menu.path = '/system/roles'
        role_menu.component = 'system/roles/index'
        role_menu.icon = 'el-icon-s-custom'
        role_menu.sort_order = 2
        role_menu.is_visible = True
        role_menu.parent = system_menu
        role_menu.save()
        print(f'✓ 更新角色管理菜单: {role_menu.name}')

    # 角色管理子权限（按钮）
    # 角色管理按钮权限
    role_permissions = [
        ('role:list', '角色列表'),
        ('role:add', '添加角色'),
        ('role:edit', '编辑角色'),
        ('role:delete', '删除角色'),
        ('role:assign:permission', '分配权限'),
    ]
    for code, name in role_permissions:
        perm, created = Permission.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'type': 'button',
                'sort_order': 1,
                'is_visible': False,
                'parent': role_menu
            }
        )
        if not created:
            perm.type = 'button'
            perm.is_visible = False
            perm.parent = role_menu
            perm.save()

    # ========== 菜单管理菜单 ==========
    # 菜单管理菜单
    menu_menu, created = Permission.objects.get_or_create(
        code='system:menu',
        defaults={
            'name': '菜单管理',
            'type': 'menu',
            'path': '/system/menus',
            'component': 'system/menus/index',
            'icon': 'el-icon-menu',
            'sort_order': 3,
            'is_visible': True,
            'parent': system_menu
        }
    )
    if created:
        print(f'✓ 创建菜单管理菜单: {menu_menu.name}')
    else:
        menu_menu.name = '菜单管理'
        menu_menu.type = 'menu'
        menu_menu.path = '/system/menus'
        menu_menu.component = 'system/menus/index'
        menu_menu.icon = 'el-icon-menu'
        menu_menu.sort_order = 3
        menu_menu.is_visible = True
        menu_menu.parent = system_menu
        menu_menu.save()
        print(f'✓ 更新菜单管理菜单: {menu_menu.name}')

    # 菜单管理子权限（按钮）
    # 菜单管理按钮权限
    menu_permissions = [
        ('system:menu:list', '菜单列表'),
        ('system:menu:add', '添加菜单'),
        ('system:menu:edit', '编辑菜单'),
        ('system:menu:delete', '删除菜单'),
    ]
    for code, name in menu_permissions:
        perm, created = Permission.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'type': 'button',
                'sort_order': 1,
                'is_visible': False,
                'parent': menu_menu
            }
        )
        if not created:
            perm.type = 'button'
            perm.is_visible = False
            perm.parent = menu_menu
            perm.save()

    # ========== 部门管理菜单 ==========
    # 部门管理菜单
    dept_menu, created = Permission.objects.get_or_create(
        code='system:department',
        defaults={
            'name': '部门管理',
            'type': 'menu',
            'path': '/system/departments',
            'component': 'system/departments/index',
            'icon': 'el-icon-office-building',
            'sort_order': 4,
            'is_visible': True,
            'parent': system_menu
        }
    )
    if created:
        print(f'✓ 创建部门管理菜单: {dept_menu.name}')
    else:
        dept_menu.name = '部门管理'
        dept_menu.type = 'menu'
        dept_menu.path = '/system/departments'
        dept_menu.component = 'system/departments/index'
        dept_menu.icon = 'el-icon-office-building'
        dept_menu.sort_order = 4
        dept_menu.is_visible = True
        dept_menu.parent = system_menu
        dept_menu.save()
        print(f'✓ 更新部门管理菜单: {dept_menu.name}')

    # 部门管理按钮权限
    dept_permissions = [
        ('department:list', '部门列表'),
        ('department:add', '添加部门'),
        ('department:edit', '编辑部门'),
        ('department:delete', '删除部门'),
    ]
    for code, name in dept_permissions:
        perm, created = Permission.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'type': 'button',
                'sort_order': 1,
                'is_visible': False,
                'parent': dept_menu
            }
        )
        if not created:
            perm.type = 'button'
            perm.is_visible = False
            perm.parent = dept_menu
            perm.save()

    # ========== 日志管理菜单 ==========
    # 日志管理父菜单
    log_root_menu, created = Permission.objects.get_or_create(
        code='system:log',
        defaults={
            'name': '日志管理',
            'type': 'menu',
            'path': '/system/logs',
            'component': 'Layout',
            'icon': 'el-icon-document',
            'sort_order': 5,
            'is_visible': True,
            'parent': system_menu
        }
    )
    if created:
        print(f'✓ 创建日志管理菜单: {log_root_menu.name}')
    else:
        log_root_menu.name = '日志管理'
        log_root_menu.type = 'menu'
        log_root_menu.path = '/system/logs'
        log_root_menu.component = 'Layout'
        log_root_menu.icon = 'el-icon-document'
        log_root_menu.sort_order = 5
        log_root_menu.is_visible = True
        log_root_menu.parent = system_menu
        log_root_menu.save()
        print(f'✓ 更新日志管理菜单: {log_root_menu.name}')

    # 登录日志子菜单
    login_log_menu, created = Permission.objects.get_or_create(
        code='system:log:login',
        defaults={
            'name': '登录日志',
            'type': 'menu',
            'path': '/system/logs/login',
            'component': 'system/logs/login',
            'icon': 'el-icon-s-check',
            'sort_order': 1,
            'is_visible': True,
            'parent': log_root_menu
        }
    )
    if not created:
        login_log_menu.name = '登录日志'
        login_log_menu.type = 'menu'
        login_log_menu.path = '/system/logs/login'
        login_log_menu.component = 'system/logs/login'
        login_log_menu.icon = 'el-icon-s-check'
        login_log_menu.sort_order = 1
        login_log_menu.is_visible = True
        login_log_menu.parent = log_root_menu
        login_log_menu.save()

    # 操作日志子菜单
    operation_log_menu, created = Permission.objects.get_or_create(
        code='system:log:operation',
        defaults={
            'name': '操作日志',
            'type': 'menu',
            'path': '/system/logs/operation',
            'component': 'system/logs/operation',
            'icon': 'el-icon-s-operation',
            'sort_order': 2,
            'is_visible': True,
            'parent': log_root_menu
        }
    )
    if not created:
        operation_log_menu.name = '操作日志'
        operation_log_menu.type = 'menu'
        operation_log_menu.path = '/system/logs/operation'
        operation_log_menu.component = 'system/logs/operation'
        operation_log_menu.icon = 'el-icon-s-operation'
        operation_log_menu.sort_order = 2
        operation_log_menu.is_visible = True
        operation_log_menu.parent = log_root_menu
        operation_log_menu.save()

    # 日志按钮权限
    log_permissions = [
        ('log:login:list', '登录日志列表'),
        ('log:operation:list', '操作日志列表'),
    ]
    for code, name in log_permissions:
        perm, created = Permission.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'type': 'button',
                'sort_order': 1,
                'is_visible': False,
                'parent': log_root_menu
            }
        )
        if not created:
            perm.type = 'button'
            perm.is_visible = False
            perm.parent = log_root_menu
            perm.save()

    # ========== 数据权限规则 ==========
    # 数据权限菜单
    data_rule_menu, created = Permission.objects.get_or_create(
        code='system:data-rule',
        defaults={
            'name': '数据权限',
            'type': 'menu',
            'path': '/system/data-rules',
            'component': 'system/data-permissions/index',
            'icon': 'el-icon-s-tools',
            'sort_order': 6,
            'is_visible': True,
            'parent': system_menu
        }
    )
    if not created:
        data_rule_menu.name = '数据权限'
        data_rule_menu.type = 'menu'
        data_rule_menu.path = '/system/data-rules'
        data_rule_menu.component = 'system/data-permissions/index'
        data_rule_menu.icon = 'el-icon-s-tools'
        data_rule_menu.sort_order = 6
        data_rule_menu.is_visible = True
        data_rule_menu.parent = system_menu
        data_rule_menu.save()

    # 数据权限按钮权限
    data_rule_permissions = [
        ('data:rule:list', '数据权限规则列表'),
        ('data:rule:add', '添加数据权限规则'),
        ('data:rule:edit', '编辑数据权限规则'),
        ('data:rule:delete', '删除数据权限规则'),
    ]
    for code, name in data_rule_permissions:
        perm, created = Permission.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'type': 'button',
                'sort_order': 1,
                'is_visible': False,
                'parent': data_rule_menu
            }
        )
        if not created:
            perm.type = 'button'
            perm.is_visible = False
            perm.parent = data_rule_menu
            perm.save()

    # ========== 个人中心菜单 ==========
    # 个人中心菜单
    profile_menu, created = Permission.objects.get_or_create(
        code='user:profile',
        defaults={
            'name': '个人中心',
            'type': 'menu',
            'path': '/profile',
            'component': 'profile/index',
            'icon': 'el-icon-user',
            'sort_order': 200,
            'is_visible': True
        }
    )
    if created:
        print(f'✓ 创建个人中心菜单: {profile_menu.name}')
    else:
        profile_menu.name = '个人中心'
        profile_menu.type = 'menu'
        profile_menu.path = '/profile'
        profile_menu.component = 'profile/index'
        profile_menu.icon = 'el-icon-user'
        profile_menu.sort_order = 200
        profile_menu.is_visible = True
        profile_menu.save()
        print(f'✓ 更新个人中心菜单: {profile_menu.name}')

    print('\n✅ 默认菜单创建完成！')
    print(f'\n菜单层级结构：')
    print(f'- {dashboard.name}')
    print(f'- {system_menu.name}')
    print(f'  - {user_menu.name}')
    print(f'  - {role_menu.name}')
    print(f'  - {menu_menu.name}')
    print(f'  - {dept_menu.name}')
    print(f'  - {log_root_menu.name}')
    print(f'  - {data_rule_menu.name}')
    print(f'- {profile_menu.name}')

if __name__ == '__main__':
    # 脚本入口
    create_default_menus()
