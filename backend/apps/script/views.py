from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.core.decorators import permission_required
from apps.core.permissions import HasPermission
from apps.core.response import success_response, error_response
from .models import ScriptTable, ScriptQueue
from .serializers import ScriptTableSerializer, ScriptQueueSerializer
from .redis_client import get_redis
import re


# ============================================================================
# 脚本配置管理
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('script:config:list')
def script_config_list_view(request):
    """脚本配置（仅返回当前用户单条）"""
    config_type = request.GET.get('config_type')
    if not config_type:
        return error_response('缺少 config_type 参数', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    config = ScriptTable.objects.filter(
        is_deleted=False,
        userId=request.user.id,
        configType=config_type
    ).order_by('-updated_at', '-id').first()

    if not config:
        return success_response(None)

    serializer = ScriptTableSerializer(config)
    return success_response(serializer.data)


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
    # 如果当前用户已有配置（含软删除），则直接更新/恢复
    user_id = data.get('userId')
    config_type = data.get('configType', '')
    if user_id:
        existing = ScriptTable.objects.filter(userId=user_id, configType=config_type).first()
        if existing:
            data['updateBy'] = request.user.username
            data['is_deleted'] = False
            serializer = ScriptTableSerializer(existing, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(serializer.data, message='创建成功', code=200, http_status=status.HTTP_200_OK)

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


# ============================================================================
# 公共接口：按用户ID获取单条配置（无鉴权）
# ============================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def script_config_public_view(request):
    """根据 userId + configType 获取配置（公开接口）"""
    user_id = request.GET.get('user_id')
    config_type = request.GET.get('config_type')
    if not user_id or not str(user_id).isdigit():
        return error_response('缺少或无效的 user_id 参数', code=400, http_status=status.HTTP_400_BAD_REQUEST)
    if not config_type:
        return error_response('缺少 config_type 参数', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    config = ScriptTable.objects.filter(
        is_deleted=False,
        userId=int(user_id),
        configType=config_type
    ).order_by('-updated_at', '-id').first()

    if not config:
        return success_response(None)

    serializer = ScriptTableSerializer(config)
    return success_response(serializer.data)


# ============================================================================
# 脚本数据队列管理
# ============================================================================

QUEUE_NAME_PATTERN = re.compile(r'^[A-Za-z_]+$')
PHONE_PATTERN = re.compile(r'^1[3-9]\d{9}$')


def _queue_key(name: str) -> str:
    return f"queue:{name}"


@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('script:queue:list')
def script_queue_list_view(request):
    queues = ScriptQueue.objects.filter(is_deleted=False).order_by('-updated_at', '-id')
    serializer = ScriptQueueSerializer(queues, many=True)
    return success_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('script:queue:add')
def script_queue_create_view(request):
    name = (request.data.get('name') or '').strip()
    remark = (request.data.get('remark') or '').strip()
    if not name or not QUEUE_NAME_PATTERN.match(name):
        return error_response('队列名称仅支持英文和下划线', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    existing = ScriptQueue.objects.filter(name=name).order_by('-id').first()
    if existing:
        if not existing.is_deleted:
            return error_response('队列名称已存在', code=400, http_status=status.HTTP_400_BAD_REQUEST)
        # 复用已删除的队列名称
        existing.is_deleted = False
        existing.remark = remark
        existing.count = 0
        existing.created_by = request.user.username
        existing.save(update_fields=['is_deleted', 'remark', 'count', 'created_by'])
        r = get_redis()
        r.delete(_queue_key(existing.name))
        return success_response(ScriptQueueSerializer(existing).data, message='创建成功', code=200, http_status=status.HTTP_200_OK)

    queue = ScriptQueue.objects.create(
        name=name,
        remark=remark,
        count=0,
        created_by=request.user.username
    )
    return success_response(ScriptQueueSerializer(queue).data, message='创建成功', code=201, http_status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('script:queue:clear')
def script_queue_clear_view(request, queue_id):
    try:
        queue = ScriptQueue.objects.get(id=queue_id, is_deleted=False)
    except ScriptQueue.DoesNotExist:
        return error_response('队列不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    r = get_redis()
    r.delete(_queue_key(queue.name))
    queue.count = 0
    queue.save(update_fields=['count'])
    return success_response(message='清空成功')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('script:queue:delete')
def script_queue_delete_view(request, queue_id):
    try:
        queue = ScriptQueue.objects.get(id=queue_id, is_deleted=False)
    except ScriptQueue.DoesNotExist:
        return error_response('队列不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    r = get_redis()
    r.delete(_queue_key(queue.name))
    queue.is_deleted = True
    queue.save(update_fields=['is_deleted'])
    return success_response(message='删除成功')


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('script:queue:upload')
def script_queue_upload_view(request, queue_id):
    try:
        queue = ScriptQueue.objects.get(id=queue_id, is_deleted=False)
    except ScriptQueue.DoesNotExist:
        return error_response('队列不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)

    file = request.FILES.get('file')
    if not file:
        return error_response('请上传TXT文件', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    mode = (request.data.get('mode') or 'append').lower()
    if mode not in ['append', 'overwrite']:
        return error_response('mode 仅支持 append 或 overwrite', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    try:
        content = file.read().decode('utf-8')
    except Exception:
        return error_response('文件解析失败，请使用UTF-8编码的TXT', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    invalid = []
    seen = set()
    phones = []
    for line in lines:
        if not PHONE_PATTERN.match(line):
            if len(invalid) < 20:
                invalid.append(line)
            continue
        if line in seen:
            continue
        seen.add(line)
        phones.append(line)

    if invalid:
        return error_response(
            message='手机号格式不正确',
            code=400,
            http_status=status.HTTP_400_BAD_REQUEST,
            errors={'invalid_samples': invalid}
        )

    r = get_redis()
    key = _queue_key(queue.name)
    if mode == 'overwrite':
        r.delete(key)

    if phones:
        r.rpush(key, *phones)

    queue.count = r.llen(key)
    queue.save(update_fields=['count'])

    return success_response({
        'count': queue.count,
        'added': len(phones),
        'mode': mode
    }, message='上传成功')
