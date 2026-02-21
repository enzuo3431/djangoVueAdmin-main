from django.db import models
from apps.core.models import BaseModel


class ToolIdCardRecord(BaseModel):
    """六扇门身份证记录"""
    name = models.CharField('姓名', max_length=20, default='')
    idcard = models.CharField('身份证号', max_length=18, unique=True, db_index=True)
    status = models.SmallIntegerField('状态(0未使用 1已使用)', default=0, db_index=True)

    class Meta:
        db_table = 'tools_idcard_record'
        verbose_name = '身份证记录'
        verbose_name_plural = '身份证记录'

    def __str__(self):
        return f'{self.name}-{self.idcard}'
