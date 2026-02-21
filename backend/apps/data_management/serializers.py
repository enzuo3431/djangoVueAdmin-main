from rest_framework import serializers
from .models import ArchivePhoneData


class ArchivePhoneDataSerializer(serializers.ModelSerializer):
    platforms_list = serializers.SerializerMethodField()

    class Meta:
        model = ArchivePhoneData
        fields = [
            'id', 'phone', 'is_filtered', 'status', 'source', 'register_flags',
            'platforms', 'platforms_list', 'remark', 'extra', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'register_flags', 'created_at', 'updated_at']

    def get_platforms_list(self, obj):
        if not obj.platforms:
            return []
        return [item for item in obj.platforms.split(',') if item]
