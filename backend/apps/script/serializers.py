from rest_framework import serializers
from .models import ScriptTable, ScriptQueue


class ScriptTableSerializer(serializers.ModelSerializer):
    """脚本配置序列化器"""
    class Meta:
        model = ScriptTable
        fields = [
            'id', 'createBy', 'updateBy', 'remark', 'ipAddress', 'userId', 'name',
            'isOpenAddFriend', 'isOpenSearchAddFriend', 'isOpenBookAddFriend',
            'isOpenSendFile', 'addNumber', 'openSendFileIndex', 'delayTime',
            'timeIntervalAdd', 'replyContent', 'configType', 'addPeopleContent',
            'startTime', 'endTime', 'isOpenMsgReply', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ScriptQueueSerializer(serializers.ModelSerializer):
    """脚本队列序列化器"""
    class Meta:
        model = ScriptQueue
        fields = ['id', 'name', 'remark', 'count', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'count', 'created_by', 'created_at', 'updated_at']
