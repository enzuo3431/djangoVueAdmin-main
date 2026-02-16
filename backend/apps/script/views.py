from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from apps.core.decorators import permission_required
from apps.core.permissions import HasPermission
from apps.core.response import success_response, error_response
from .models import ScriptTable
from .serializers import ScriptTableSerializer


# ============================================================================
# 脚本配置管理
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('script:config:list')
def script_config_list_view(request):
    """脚本配置列表"""
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    keyword = request.GET.get('keyword', '')
    config_type = request.GET.get('config_type')

    queryset = ScriptTable.objects.filter(is_deleted=False)
    if config_type:
        queryset = queryset.filter(configType=config_type)
    if keyword:
        search_q = Q(name__icontains=keyword) | Q(ipAddress__icontains=keyword)
        if keyword.isdigit():
            search_q = search_q | Q(userId=int(keyword))
        queryset = queryset.filter(search_q)

    queryset = queryset.order_by('-updated_at', '-id')
    start = (page - 1) * page_size
    end = start + page_size
    configs = queryset[start:end]
    total = queryset.count()

    serializer = ScriptTableSerializer(configs, many=True)
    return success_response({
        'list': serializer.data,
        'total': total,
        'page': page,
        'page_size': page_size
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('script:config:add')
def script_config_create_view(request):
    """创建脚本配置"""
    data = request.data.copy()
    if not data.get('createBy'):
        data['createBy'] = request.user.username
    if not data.get('updateBy'):
        data['updateBy'] = request.user.username
    serializer = ScriptTableSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success_response(serializer.data, message='创建成功', code=201, http_status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('script:config:list')
def script_config_detail_view(request, config_id):
    """脚本配置详情"""
    try:
        config = ScriptTable.objects.get(id=config_id, is_deleted=False)
    except ScriptTable.DoesNotExist:
        return error_response('配置不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)
    serializer = ScriptTableSerializer(config)
    return success_response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('script:config:edit')
def script_config_update_view(request, config_id):
    """更新脚本配置"""
    try:
        config = ScriptTable.objects.get(id=config_id, is_deleted=False)
    except ScriptTable.DoesNotExist:
        return error_response('配置不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['updateBy'] = request.user.username
    serializer = ScriptTableSerializer(config, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success_response(serializer.data, message='更新成功')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('script:config:delete')
def script_config_delete_view(request, config_id):
    """删除脚本配置"""
    try:
        config = ScriptTable.objects.get(id=config_id, is_deleted=False)
    except ScriptTable.DoesNotExist:
        return error_response('配置不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)
    config.is_deleted = True
    config.save()
    return success_response(message='删除成功')
