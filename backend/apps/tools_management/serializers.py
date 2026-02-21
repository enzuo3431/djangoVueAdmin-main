from rest_framework import serializers
from .models import ToolIdCardRecord


class ToolIdCardRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolIdCardRecord
        fields = ['id', 'name', 'idcard', 'status', 'created_at', 'updated_at']
