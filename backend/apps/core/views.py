"""
用户管理API - 展示RBAC权限系统的使用
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Role, Permission, UserRole, RolePermission, Department, LoginLog, OperationLog, UserSession, DataPermissionRule
from .serializers import (
    UserListSerializer, UserDetailSerializer,
    UserCreateSerializer, UserUpdateSerializer,
    RoleSerializer, PermissionSerializer,
    DepartmentSerializer, LoginLogSerializer, OperationLogSerializer, UserSessionSerializer,
    DataPermissionRuleSerializer
)
from .permissions import HasPermission
from .decorators import permission_required, api_permission_required
from .response import success_response, error_response
from .data_scope import filter_queryset_by_data_scope
import logging
User = get_user_model()


# ============================================================================
# 通用接口
# ============================================================================

@api_view(['GET'])
def health_check(request):
    """健康检查接口"""
    return success_response({
        'status': 'success',
        'message': 'Django Vue Admin 后端服务运行正常',
        'version': '1.0.0',
        'framework': 'Django REST Framework'
    }, message='OK', code=200)


@api_view(['GET'])
def api_info(request):
    """API 信息接口"""
    return success_response({
        'project': 'Django Vue Admin',
        'version': '1.0.0',
        'description': '基于 Django + Vue Element Admin 的后台管理系统',
        'endpoints': {
            'health': '/api/health/',
            'info': '/api/info/',
        }
    }, message='OK', code=200)


# ============================================================================
# 用户管理接口 - 展示权限控制
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('user:list')  # 方式1: 使用装饰器
def user_list_view(request):
    """
    获取用户列表
    权限要求: user:list
    """
    # 获取查询参数
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    keyword = request.GET.get('keyword', '')

    # 构建查询
    queryset = User.objects.filter(is_deleted=False)

    # 关键词搜索
    if keyword:
        queryset = queryset.filter(
            username__icontains=keyword
        ) | queryset.filter(
            nickname__icontains=keyword
        ) | queryset.filter(
            email__icontains=keyword
        )

    # 数据权限过滤
    queryset = filter_queryset_by_data_scope(request.user, queryset, dept_field='department_id', user_field='id')

    # 分页
    start = (page - 1) * page_size
    end = start + page_size
    users = queryset[start:end]
    total = queryset.count()

    # 序列化
    serializer = UserListSerializer(users, many=True)

    return success_response({
        'list': serializer.data,
        'total': total,
        'page': page,
        'page_size': page_size
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
# 方式2: 通过视图属性声明权限
def user_create_view(request):
    """
    创建用户
    权限要求: user:add
    """
    user_create_view.permission_codes = ['user:add']

    # 使用创建序列化器校验并保存
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return success_response(
        UserListSerializer(user).data,
        message='创建成功',
        code=201,
        http_status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@api_permission_required('user:detail')  # 方式3: 使用DRF专用装饰器
def user_detail_view(request, user_id):
    """
    获取用户详情
    权限要求: user:detail
    """
    try:
        user = User.objects.get(id=user_id, is_deleted=False)
    except User.DoesNotExist:
        return error_response('用户不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    # 序列化详情
    serializer = UserDetailSerializer(user)
    return success_response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('user:edit')
def user_update_view(request, user_id):
    """
    更新用户信息
    权限要求: user:edit

    安全检查: 防止水平越权
    - 不能修改超级管理员（除非自己也是超级管理员）
    - 不能将普通用户提升为超级管理员
    """
    try:
        user = User.objects.get(id=user_id, is_deleted=False)
    except User.DoesNotExist:
        return error_response('用户不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    # 安全检查：防止修改超级管理员
    if user.is_superuser and not request.user.is_superuser:
        return error_response('无权修改超级管理员', code=403, http_status=status.HTTP_403_FORBIDDEN)

    # 安全检查：防止提升为超级管理员
    if 'is_superuser' in request.data and not request.user.is_superuser:
        return error_response('无权设置超级管理员', code=403, http_status=status.HTTP_403_FORBIDDEN)

    # 部分更新
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return success_response(UserListSerializer(user).data, message='更新成功')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('user:delete')
def user_delete_view(request, user_id):
    """
    删除用户
    权限要求: user:delete

    安全检查:
    - 不能删除超级管理员
    - 不能删除自己
    """
    try:
        user = User.objects.get(id=user_id, is_deleted=False)
    except User.DoesNotExist:
        return error_response('用户不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    # 安全检查：不能删除超级管理员
    if user.is_superuser:
        return error_response('不能删除超级管理员', code=403, http_status=status.HTTP_403_FORBIDDEN)

    # 安全检查：不能删除自己
    if user.id == request.user.id:
        return error_response('不能删除自己', code=403, http_status=status.HTTP_403_FORBIDDEN)

    # 软删除
    user.is_deleted = True
    user.save()

    return success_response(message='删除成功')


# ============================================================================
# 角色管理接口
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('role:list')
def role_list_view(request):
    """
    获取角色列表
    权限要求: role:list
    """
    # 角色列表
    roles = Role.objects.filter(is_deleted=False)
    serializer = RoleSerializer(roles, many=True)

    return success_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('role:detail')
def role_detail_view(request, role_id):
    """
    获取角色详情
    权限要求: role:detail
    """
    try:
        role = Role.objects.get(id=role_id, is_deleted=False)
    except Role.DoesNotExist:
        return error_response('角色不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    serializer = RoleSerializer(role)
    return success_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('role:add')
def role_create_view(request):
    """
    创建角色
    权限要求: role:add
    """
    # 校验并创建
    serializer = RoleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return success_response(serializer.data, message='创建成功', code=201, http_status=status.HTTP_201_CREATED)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('role:edit')
def role_update_view(request, role_id):
    """
    更新角色
    权限要求: role:edit
    """
    try:
        role = Role.objects.get(id=role_id, is_deleted=False)
    except Role.DoesNotExist:
        return error_response('角色不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    # 部分更新
    serializer = RoleSerializer(role, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return success_response(serializer.data, message='更新成功')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('role:delete')
def role_delete_view(request, role_id):
    """
    删除角色
    权限要求: role:delete

    级联操作：
    - 删除用户与角色的关联关系（UserRole）
    - 删除角色与权限的关联关系（RolePermission）
    - 软删除角色本身
    """
    try:
        role = Role.objects.get(id=role_id, is_deleted=False)
    except Role.DoesNotExist:
        return error_response('角色不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    # 删除用户与角色的关联关系
    UserRole.objects.filter(role=role).delete()

    # 删除角色与权限的关联关系
    RolePermission.objects.filter(role=role).delete()

    # 软删除角色
    role.is_deleted = True
    role.save()

    return success_response(message='删除成功')


# ============================================================================
# 权限管理接口
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('permission:list')
def permission_list_view(request):
    """
    获取权限列表（树形结构）
    权限要求: permission:list
    """
    # 仅取根节点，前端组装树
    permissions = Permission.objects.filter(is_deleted=False, parent__isnull=True)
    serializer = PermissionSerializer(permissions, many=True)

    return success_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def permission_all_view(request):
    """
    获取所有权限列表（扁平结构，用于分配权限时选择）
    权限要求: 已登录即可
    """
    # 全量权限
    permissions = Permission.objects.filter(is_deleted=False)
    serializer = PermissionSerializer(permissions, many=True)

    return success_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('permission:all')
def permission_detail_view(request, permission_id):
    """
    获取权限详情
    权限要求: permission:all
    """
    try:
        permission = Permission.objects.get(id=permission_id, is_deleted=False)
    except Permission.DoesNotExist:
        return error_response('权限不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    serializer = PermissionSerializer(permission)
    return success_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('permission:add')
def permission_create_view(request):
    """
    创建权限
    权限要求: permission:add
    """
    # 校验并创建
    serializer = PermissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return success_response(serializer.data, message='创建成功', code=201, http_status=status.HTTP_201_CREATED)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('permission:all')
def permission_update_view(request, permission_id):
    """
    更新权限
    权限要求: permission:all
    """
    try:
        permission = Permission.objects.get(id=permission_id, is_deleted=False)
    except Permission.DoesNotExist:
        return error_response('权限不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    # 部分更新
    serializer = PermissionSerializer(permission, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return success_response(serializer.data, message='更新成功')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('permission:all')
def permission_delete_view(request, permission_id):
    """
    删除权限
    权限要求: permission:all
    """
    try:
        permission = Permission.objects.get(id=permission_id, is_deleted=False)
    except Permission.DoesNotExist:
        return error_response('权限不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    # 软删除
    permission.is_deleted = True
    permission.save()

    return success_response(message='删除成功')


# ============================================================================
# 分配角色/权限接口
# ============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('user:assign:role')
def assign_role_view(request, user_id):
    """
    为用户分配角色
    权限要求: user:assign:role

    Body:
    {
        "role_ids": [1, 2, 3]
    }
    """
    try:
        user = User.objects.get(id=user_id, is_deleted=False)
    except User.DoesNotExist:
        return error_response('用户不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    # 目标角色 ID 列表
    role_ids = request.data.get('role_ids', [])

    # 删除旧角色
    UserRole.objects.filter(user=user).delete()

    # 分配新角色
    for role_id in role_ids:
        try:
            UserRole.objects.create(user=user, role_id=role_id)
        except:
            pass

    return success_response(message='分配成功')


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('role:assign:permission')
def assign_permission_view(request, role_id):
    """
    为角色分配权限
    权限要求: role:assign:permission

    Body:
    {
        "permission_ids": [1, 2, 3]
    }
    """
    try:
        role = Role.objects.get(id=role_id, is_deleted=False)
    except Role.DoesNotExist:
        return error_response('角色不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    # 目标权限 ID 列表
    permission_ids = request.data.get('permission_ids', [])
    role.permissions.set(permission_ids)

    return success_response(message='分配成功')


# ============================================================================
# 菜单管理接口
# ============================================================================

def build_menu_tree(permissions, parent_id=None):
    """
    递归构建菜单树

    Args:
        permissions: 权限查询集
        parent_id: 父级ID

    Returns:
        list: 菜单树列表
    """
    # 获取所有权限并预加载父级关系
    # 扁平权限列表，便于递归查找
    permissions_list = list(permissions)

    def get_children(parent_id=None):
        children = []
        for p in permissions_list:
            # 检查是否为当前父级的子项
            # 当前权限的父级 ID
            actual_parent_id = getattr(p, 'parent_id', None)
            if actual_parent_id == parent_id:
                # 检查是否可见
                is_visible = getattr(p, 'is_visible', True)
                if is_visible:
                    menu_item = {
                        'id': p.id,
                        'title': p.name,
                        'icon': getattr(p, 'icon', ''),
                        'path': p.path or '',
                        'component': getattr(p, 'component', ''),
                        'redirect': getattr(p, 'redirect', ''),
                        'sort_order': getattr(p, 'sort_order', 0),
                        'code': p.code,
                        'children': get_children(p.id)
                    }
                    children.append(menu_item)
        # 按排序字段排序
        children.sort(key=lambda x: x['sort_order'])
        return children

    return get_children(parent_id)


def get_user_menus(user):
    """
    获取用户菜单

    Args:
        user: 用户对象

    Returns:
        list: 菜单树列表
    """
    from .models import Permission

    if user.is_superuser:
        # 超级管理员获取所有菜单
        menu_permissions = Permission.objects.filter(type='menu', is_deleted=False)
    else:
        # 普通用户获取角色关联的菜单
        menu_permissions = Permission.objects.filter(
            type='menu',
            is_deleted=False,
            role__in=user.roles.filter(is_deleted=False)
        ).distinct()

    return build_menu_tree(menu_permissions)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_menu_view(request):
    """
    获取当前用户菜单树
    权限要求: 已登录即可
    """
    menus = get_user_menus(request.user)
    return success_response(menus)


@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
def menu_list_view(request):
    """
    获取所有菜单列表（管理页面用）
    权限要求: system:menu:list
    """
    menu_list_view.permission_codes = ['system:menu:list']

    # 菜单权限列表
    menus = Permission.objects.filter(type='menu', is_deleted=False)
    serializer = PermissionSerializer(menus, many=True)

    return success_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
def menu_create_view(request):
    """
    创建菜单
    权限要求: system:menu:add
    """
    menu_create_view.permission_codes = ['system:menu:add']

    # 校验并创建
    serializer = PermissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # 确保类型为 menu
    # 强制类型为 menu
    validated_data = serializer.validated_data
    if 'type' not in validated_data:
        validated_data['type'] = 'menu'

    serializer.save()

    return success_response(serializer.data, message='创建成功', code=201, http_status=status.HTTP_201_CREATED)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, HasPermission])
def menu_update_view(request, menu_id):
    """
    更新菜单
    权限要求: system:menu:edit
    """
    menu_update_view.permission_codes = ['system:menu:edit']

    try:
        menu = Permission.objects.get(id=menu_id, is_deleted=False, type='menu')
    except Permission.DoesNotExist:
        return error_response('菜单不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    # 部分更新
    serializer = PermissionSerializer(menu, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return success_response(serializer.data, message='更新成功')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, HasPermission])
def menu_delete_view(request, menu_id):
    """
    删除菜单
    权限要求: system:menu:delete
    """
    menu_delete_view.permission_codes = ['system:menu:delete']

    try:
        menu = Permission.objects.get(id=menu_id, is_deleted=False, type='menu')
    except Permission.DoesNotExist:
        return error_response('菜单不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    # 软删除
    menu.is_deleted = True
    menu.save()

    return success_response(message='删除成功')


# ============================================================================
# 部门管理接口（数据权限）
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('department:list')
def department_list_view(request):
    """部门列表"""
    # 按排序与 ID 排序
    departments = Department.objects.filter(is_deleted=False).order_by('sort_order', 'id')
    serializer = DepartmentSerializer(departments, many=True)
    return success_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('department:add')
def department_create_view(request):
    """创建部门"""
    # 校验并创建
    serializer = DepartmentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success_response(serializer.data, message='创建成功', code=201, http_status=status.HTTP_201_CREATED)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('department:edit')
def department_update_view(request, department_id):
    """更新部门"""
    try:
        department = Department.objects.get(id=department_id, is_deleted=False)
    except Department.DoesNotExist:
        return error_response('部门不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)
    # 部分更新
    serializer = DepartmentSerializer(department, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success_response(serializer.data, message='更新成功')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('department:delete')
def department_delete_view(request, department_id):
    """删除部门"""
    try:
        department = Department.objects.get(id=department_id, is_deleted=False)
    except Department.DoesNotExist:
        return error_response('部门不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)
    department.is_deleted = True
    department.save()
    return success_response(message='删除成功')


# ============================================================================
# 登录日志 / 操作日志
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('log:login:list')
def login_log_list_view(request):
    """登录日志列表"""
    # 分页与筛选参数
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    keyword = request.GET.get('keyword', '')
    status_filter = request.GET.get('status')

    # 按时间倒序
    queryset = LoginLog.objects.all().order_by('-login_time')
    if keyword:
        queryset = queryset.filter(username__icontains=keyword)
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    # 分页切片
    start = (page - 1) * page_size
    end = start + page_size
    logs = queryset[start:end]
    total = queryset.count()
    serializer = LoginLogSerializer(logs, many=True)

    return success_response({
        'list': serializer.data,
        'total': total,
        'page': page,
        'page_size': page_size
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('log:operation:list')
def operation_log_list_view(request):
    """操作日志列表"""
    # 分页与筛选参数
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    keyword = request.GET.get('keyword', '')
    method = request.GET.get('method')
    status_code = request.GET.get('status_code')

    # 按时间倒序
    queryset = OperationLog.objects.all().order_by('-created_at')
    if keyword:
        queryset = queryset.filter(path__icontains=keyword)
    if method:
        queryset = queryset.filter(method=method.upper())
    if status_code:
        queryset = queryset.filter(status_code=status_code)

    # 分页切片
    start = (page - 1) * page_size
    end = start + page_size
    logs = queryset[start:end]
    total = queryset.count()
    serializer = OperationLogSerializer(logs, many=True)

    return success_response({
        'list': serializer.data,
        'total': total,
        'page': page,
        'page_size': page_size
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('session:list')
def user_session_list_view(request):
    """用户会话列表"""
    # 分页与筛选参数
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    keyword = request.GET.get('keyword', '')

    # 仅返回有效会话
    queryset = UserSession.objects.filter(is_active=True).order_by('-last_activity')
    if keyword:
        queryset = queryset.filter(user__username__icontains=keyword)

    # 分页切片
    start = (page - 1) * page_size
    end = start + page_size
    sessions = queryset[start:end]
    total = queryset.count()
    serializer = UserSessionSerializer(sessions, many=True)

    return success_response({
        'list': serializer.data,
        'total': total,
        'page': page,
        'page_size': page_size
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('user:reset:password')
def user_reset_password_view(request, user_id):
    """管理员重置用户密码"""
    try:
        user = User.objects.get(id=user_id, is_deleted=False)
    except User.DoesNotExist:
        return error_response('用户不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    # 新密码（可为空）
    new_password = request.data.get('new_password')
    if not new_password:
        new_password = f"Pwd{timezone.now().strftime('%m%d%H%M')}"

    if len(new_password) < 6:
        return error_response('密码长度至少6位', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    # 写入新密码
    user.set_password(new_password)
    user.save()

    return success_response({
        'new_password': new_password
    }, message='重置成功')


# ============================================================================
# 数据权限规则（自定义条件）
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('data:rule:list')
def data_permission_rule_list_view(request):
    """数据权限规则列表"""
    # 可选角色筛选
    role_id = request.GET.get('role_id')
    queryset = DataPermissionRule.objects.filter(is_deleted=False)
    if role_id:
        queryset = queryset.filter(role_id=role_id)
    serializer = DataPermissionRuleSerializer(queryset, many=True)
    return success_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('data:rule:add')
def data_permission_rule_create_view(request):
    """创建数据权限规则"""
    serializer = DataPermissionRuleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success_response(serializer.data, message='创建成功', code=201, http_status=status.HTTP_201_CREATED)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('data:rule:edit')
def data_permission_rule_update_view(request, rule_id):
    """更新数据权限规则"""
    try:
        rule = DataPermissionRule.objects.get(id=rule_id, is_deleted=False)
    except DataPermissionRule.DoesNotExist:
        return error_response('规则不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)
    serializer = DataPermissionRuleSerializer(rule, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success_response(serializer.data, message='更新成功')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('data:rule:delete')
def data_permission_rule_delete_view(request, rule_id):
    """删除数据权限规则"""
    try:
        rule = DataPermissionRule.objects.get(id=rule_id, is_deleted=False)
    except DataPermissionRule.DoesNotExist:
        return error_response('规则不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)
    rule.is_deleted = True
    rule.save()
    return success_response(message='删除成功')

