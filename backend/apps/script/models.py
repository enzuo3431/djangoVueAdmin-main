from django.db import models
from apps.core.models import BaseModel


class ScriptTable(BaseModel):
    """脚本配置表"""
    id = models.AutoField(primary_key=True)  # id
    createBy = models.CharField('创建人', max_length=50, default='admin')
    updateBy = models.CharField('更新人', max_length=50, default='admin')
    remark = models.CharField('评论', max_length=50, default='remark')
    ipAddress = models.CharField('ip地址', max_length=50)
    userId = models.IntegerField('用户id', default=0, unique=True)  # 绑定的用户id值，唯一
    name = models.CharField('设备类型', max_length=50)  # 设备类型名称
    isOpenAddFriend = models.BooleanField('是否开启添加好友', default=False)
    isOpenSearchAddFriend = models.BooleanField('是否开启搜索好友', default=False)
    isOpenBookAddFriend = models.BooleanField('是否开启通讯录加好友', default=False)
    isOpenSendFile = models.BooleanField('是否开启发送文件', default=False)
    addNumber = models.IntegerField('添加好友数量', default=1)
    openSendFileIndex = models.IntegerField('发送文件的索引默认第一个', default=1)
    delayTime = models.IntegerField('发消息间隔延迟时间/s', default=1)
    timeIntervalAdd = models.IntegerField('添加好友间隔延迟时间/s', default=5)
    replyContent = models.CharField('加好友话术', max_length=255, default='', blank=True)
    configType = models.CharField('配置类型', max_length=50, default='')
    addPeopleContent = models.TextField('发消息内容', default='', blank=True)
    startTime = models.CharField('定时启动时间', max_length=25, default='')
    endTime = models.CharField('定时结束时间', max_length=25, default='')
    isOpenMsgReply = models.BooleanField('是否开启消息回复', default=False)
    status = models.BooleanField('脚本配置状态 是否开启此脚本', default=False)

    class Meta:
        db_table = 'script_table'
        verbose_name = '脚本配置'
        verbose_name_plural = '脚本配置'

    def __str__(self):
        return f"{self.name}({self.userId})"


class ScriptQueue(BaseModel):
    """脚本数据队列"""
    name = models.CharField('队列名称', max_length=50, unique=True)
    remark = models.CharField('备注', max_length=255, default='', blank=True)
    count = models.IntegerField('数据数量', default=0)
    created_by = models.CharField('创建人', max_length=50, default='')

    class Meta:
        db_table = 'script_queue'
        verbose_name = '脚本队列'
        verbose_name_plural = '脚本队列'

    def __str__(self):
        return self.name
