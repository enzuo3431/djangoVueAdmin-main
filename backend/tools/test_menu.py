"""菜单数据结构测试脚本。"""
import os
import sys
import django
import json

# 将 backend 目录加入路径，便于加载配置与应用
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import User, Permission

def test_menu_data():
    """测试菜单数据结构"""

    # 获取超级管理员用户
    try:
        user = User.objects.get(username='admin')
    except User.DoesNotExist:
        print('找不到admin用户')
        return

    # 模拟 get_user_menus 函数
    if user.is_superuser:
        menu_permissions = Permission.objects.filter(type='menu', is_deleted=False)
    else:
        menu_permissions = Permission.objects.filter(
            type='menu',
            is_deleted=False,
            role__in=user.roles.filter(is_deleted=False)
        ).distinct()

    # 打印菜单权限
    print(f'找到 {menu_permissions.count()} 个菜单权限:')
    for p in menu_permissions:
        print(f'  - {p.name}: path={p.path}, component={p.component}, icon={p.icon}, parent_id={p.parent_id}')

    # 构建菜单树
    def build_tree(permissions, parent_id=None):
        # 递归构建菜单树
        result = []
        for p in sorted(permissions, key=lambda x: getattr(x, 'sort_order', 0)):
            if p.parent_id == parent_id and getattr(p, 'is_visible', True):
                menu_item = {
                    'id': p.id,
                    'title': p.name,
                    'icon': getattr(p, 'icon', ''),
                    'path': p.path or '',
                    'component': getattr(p, 'component', ''),
                    'redirect': getattr(p, 'redirect', ''),
                    'sort_order': getattr(p, 'sort_order', 0),
                    'code': p.code,
                    'children': build_tree(permissions, p.id)
                }
                result.append(menu_item)
        result.sort(key=lambda x: x['sort_order'])
        return result

    menu_tree = build_tree(menu_permissions)

    print('\n菜单树结构:')
    print(json.dumps(menu_tree, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    # 脚本入口
    test_menu_data()
