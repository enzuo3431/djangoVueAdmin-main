from django.db import models
from apps.core.models import BaseModel


class ArchivePhoneData(BaseModel):
    """归档数据（手机号）"""
    phone = models.BigIntegerField('手机号', unique=True, db_index=True)
    is_filtered = models.BooleanField('是否命中过滤', default=False, db_index=True)
    status = models.SmallIntegerField('状态(1正常 0禁用)', default=1, db_index=True)
    source = models.CharField('数据来源', max_length=32, default='manual', db_index=True)
    register_flags = models.PositiveIntegerField('平台注册标识(bitmask)', default=0)
    platforms = models.CharField('平台注册平台(逗号分隔)', max_length=64, default='', db_index=True)
    remark = models.CharField('备注', max_length=255, blank=True, default='', db_index=True)
    extra = models.JSONField('扩展字段', default=dict, blank=True)

    class Meta:
        db_table = 'data_archive_phone'
        verbose_name = '归档数据'
        verbose_name_plural = '归档数据'

    def __str__(self):
        return str(self.phone)
