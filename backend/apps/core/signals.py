"""权限相关缓存清理信号。"""
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save, m2m_changed
from django.dispatch import receiver

from .models import UserRole, RolePermission, Role


def _clear_user_permissions(user_id):
    """清理指定用户的权限缓存。"""
    cache.delete(f"user_permissions:{user_id}")


@receiver(post_save, sender=UserRole)
@receiver(post_delete, sender=UserRole)
def clear_user_role_cache(sender, instance, **kwargs):
    """用户角色变更后清理缓存。"""
    _clear_user_permissions(instance.user_id)


@receiver(post_save, sender=RolePermission)
@receiver(post_delete, sender=RolePermission)
def clear_role_permission_cache(sender, instance, **kwargs):
    """角色权限变更后清理所有关联用户缓存。"""
    role = instance.role
    for user in role.user_set.all():
        _clear_user_permissions(user.id)


@receiver(m2m_changed, sender=Role.permissions.through)
def clear_role_permission_m2m_cache(sender, instance, action, **kwargs):
    """多对多权限变更时清理缓存。"""
    if action in {'post_add', 'post_remove', 'post_clear'}:
        for user in instance.user_set.all():
            _clear_user_permissions(user.id)
