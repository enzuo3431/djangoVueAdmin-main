"""数据权限范围过滤与自定义规则处理。"""
from typing import Iterable, Set

from django.db.models import QuerySet

import json
from django.db.models import Q
from .models import Department, DataPermissionRule


DATA_SCOPE_PRIORITY = {
    # 权限范围优先级，数值越大权限越高
    'all': 5,
    'custom': 4,
    'dept_and_child': 3,
    'dept': 2,
    'self': 1,
}


def _get_department_descendants(dept_ids: Iterable[int]) -> Set[int]:
    """获取部门及其所有子部门 ID"""
    # 使用 BFS 找到所有子部门
    all_ids = set(dept_ids)
    queue = list(dept_ids)
    while queue:
        current_id = queue.pop(0)
        child_ids = list(Department.objects.filter(parent_id=current_id, is_deleted=False).values_list('id', flat=True))
        for child_id in child_ids:
            if child_id not in all_ids:
                all_ids.add(child_id)
                queue.append(child_id)
    return all_ids


def filter_queryset_by_data_scope(user, queryset: QuerySet, dept_field: str = 'department_id', user_field: str = 'id'):
    """
    根据角色数据权限范围过滤查询集

    规则优先级: all > custom > dept_and_child > dept > self
    """
    # 超级管理员不做限制
    if user.is_superuser:
        return queryset

    # 获取用户角色，并预取角色关联部门
    roles = user.roles.filter(is_deleted=False).prefetch_related('departments')
    if not roles.exists():
        # 无角色时仅能看到自己的数据
        return queryset.filter(**{user_field: user.id})

    # 找到最高权限范围
    best_scope = 'self'
    for role in roles:
        # role.data_scope 为空时按 self 处理
        scope = role.data_scope or 'self'
        if DATA_SCOPE_PRIORITY.get(scope, 1) > DATA_SCOPE_PRIORITY.get(best_scope, 1):
            best_scope = scope

    if best_scope == 'all':
        return queryset

    if best_scope == 'custom':
        # 自定义部门权限：汇总角色绑定的部门
        dept_ids = set()
        for role in roles:
            if role.data_scope == 'custom':
                dept_ids.update(role.departments.values_list('id', flat=True))
        base_queryset = queryset.filter(**{f"{dept_field}__in": list(dept_ids)}) if dept_ids else queryset.none()
        return _apply_custom_rules(base_queryset, roles)

    if best_scope == 'dept_and_child':
        # 本部门及子部门
        dept_id = getattr(user, 'department_id', None)
        if not dept_id:
            return queryset.filter(**{user_field: user.id})
        dept_ids = _get_department_descendants([dept_id])
        base_queryset = queryset.filter(**{f"{dept_field}__in": list(dept_ids)})
        return _apply_custom_rules(base_queryset, roles)

    if best_scope == 'dept':
        # 本部门
        dept_id = getattr(user, 'department_id', None)
        if not dept_id:
            return queryset.filter(**{user_field: user.id})
        base_queryset = queryset.filter(**{dept_field: dept_id})
        return _apply_custom_rules(base_queryset, roles)

    # 仅本人
    base_queryset = queryset.filter(**{user_field: user.id})
    return _apply_custom_rules(base_queryset, roles)


def _apply_custom_rules(queryset: QuerySet, roles):
    """
    应用自定义条件规则（大众化标准格式）
    规则字段示例:
      - field: "username"
      - operator: "icontains"
      - value: "admin"
    """
    # 取出角色对应的自定义规则
    rules = DataPermissionRule.objects.filter(role__in=roles, is_deleted=False)
    if not rules.exists():
        return queryset

    # 组合查询条件
    q = Q()
    for rule in rules:
        # 规则字段
        field = rule.field
        # 运算符
        op = rule.operator
        # 比对值
        value = rule.value

        if op == 'isnull':
            q &= Q(**{f"{field}__isnull": True})
            continue

        if op == 'in':
            try:
                parsed = json.loads(value) if value else []
                if not isinstance(parsed, list):
                    parsed = [parsed]
            except Exception:
                parsed = [v.strip() for v in value.split(',')] if value else []
            q &= Q(**{f"{field}__in": parsed})
            continue

        # 运算符映射到 Django ORM lookup
        lookup = {
            'eq': '',
            'ne': '',
            'lt': 'lt',
            'lte': 'lte',
            'gt': 'gt',
            'gte': 'gte',
            'contains': 'contains',
            'icontains': 'icontains',
            'startswith': 'startswith',
            'endswith': 'endswith'
        }.get(op)

        if lookup is None:
            continue

        if op == 'ne':
            # 不等于
            q &= ~Q(**{field: value})
        elif lookup == '':
            # 等于
            q &= Q(**{field: value})
        else:
            # 其他比较
            q &= Q(**{f"{field}__{lookup}": value})

    return queryset.filter(q)
