import base64
import json
import os
import random
import re
import tempfile
import zipfile
from datetime import date, timedelta
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache

from apps.core.decorators import permission_required
from apps.core.permissions import HasPermission
from apps.core.response import success_response, error_response
from .models import ToolIdCardRecord
from .serializers import ToolIdCardRecordSerializer
from .nickname_vocab import (
    FEMALE_SURNAMES,
    FEMALE_GIVEN_DOUBLE,
    FEMALE_GIVEN_DOUBLE_HOT,
    FEMALE_GIVEN_SINGLE,
    NICK_PREFIX,
    NICK_SUFFIX,
    NET_ADJ,
    NET_NOUN,
    NET_SYMBOL,
    STYLE_WORDS,
    ANCIENT_GIVEN_DOUBLE,
    BAD_SUBSTRINGS,
    REGION_WORDS
)
from .benefits_service import (
    analyze_benefits_files,
    get_benefits_cache_key,
    CACHE_TTL_BENEFITS
)


IDCARD_PATTERN = re.compile(r'([\u4e00-\u9fa5]{2,4}).*?(\d{17}[\dXx])')
ENTRY_PATTERN = re.compile(r'第\[\d+\]条，数据来源：.*?(?=第\[\d+\]条|$)', re.S)
ALLOWED_NICK_CHARS = re.compile(r'^[\u4e00-\u9fa5A-Za-z0-9_.\-·]+$')

def _pick_style_words(style):
    if style in STYLE_WORDS:
        return STYLE_WORDS[style]
    return None


def _weighted_pick(default_pool, hot_pool=None, hot_prob=0.62):
    if hot_pool and random.random() < hot_prob:
        return random.choice(hot_pool)
    return random.choice(default_pool)


def _normalize_for_dedup(text):
    return re.sub(r'[^A-Za-z0-9\u4e00-\u9fa5]', '', (text or '').lower())


def _has_bad_repeat(text):
    # 3连字视为低质量
    return re.search(r'(.)\1\1', text) is not None


def _is_valid_candidate(name, category, blacklist_words):
    if not name:
        return False
    if any(word in name.lower() for word in blacklist_words):
        return False
    if _has_bad_repeat(name):
        return False
    if not ALLOWED_NICK_CHARS.match(name):
        return False

    length = len(name)
    if category == 'female_name':
        # 姓名强约束：2~4字，且全中文
        if length < 2 or length > 4:
            return False
        if not re.match(r'^[\u4e00-\u9fa5]+$', name):
            return False
    elif category == 'female_nickname':
        if length < 2 or length > 12:
            return False
    elif category == 'female_netname':
        if length < 3 or length > 16:
            return False
    return True


def _style_hot_prob(intensity):
    # 风格强度影响高频/风格词命中概率
    if intensity == 'weak':
        return 0.45
    if intensity == 'strong':
        return 0.82
    return 0.62


def _gen_female_name(style='default', intensity='medium'):
    hot_prob = _style_hot_prob(intensity)
    # 古风姓名单独走古风字库
    if style == 'ancient':
        return random.choice(FEMALE_SURNAMES) + random.choice(ANCIENT_GIVEN_DOUBLE)
    if random.random() < 0.65:
        return random.choice(FEMALE_SURNAMES) + _weighted_pick(FEMALE_GIVEN_DOUBLE, FEMALE_GIVEN_DOUBLE_HOT, hot_prob)
    return random.choice(FEMALE_SURNAMES) + random.choice(FEMALE_GIVEN_SINGLE) + random.choice(FEMALE_GIVEN_SINGLE)


def _gen_female_nickname(style='default', intensity='medium'):
    hot_prob = _style_hot_prob(intensity)
    style_words = _pick_style_words(style)
    prefix_pool = style_words['prefix'] if style_words else NICK_PREFIX
    suffix_pool = style_words['suffix'] if style_words else NICK_SUFFIX
    pattern = random.randint(1, 5)
    if pattern == 1:
        return random.choice(prefix_pool) + _weighted_pick(FEMALE_GIVEN_DOUBLE, FEMALE_GIVEN_DOUBLE_HOT, hot_prob)
    if pattern == 2:
        return _weighted_pick(FEMALE_GIVEN_DOUBLE, FEMALE_GIVEN_DOUBLE_HOT, hot_prob) + random.choice(suffix_pool)
    if pattern == 3:
        base = random.choice(FEMALE_GIVEN_SINGLE)
        return base + base + random.choice(["酱", "呀", "喵", "宝", "崽"])
    if pattern == 4:
        return random.choice(prefix_pool) + random.choice(["小丸子", "奶团子", "软糯糯", "云朵朵", "桃气包", "小甜豆"])
    return random.choice(prefix_pool) + random.choice(FEMALE_GIVEN_SINGLE) + random.choice(suffix_pool)


def _apply_region(adj_pool, noun_pool, region):
    if region in REGION_WORDS:
        adj_pool = list(set(adj_pool + REGION_WORDS[region]['adj']))
        noun_pool = list(set(noun_pool + REGION_WORDS[region]['noun']))
    return adj_pool, noun_pool


def _gen_female_netname(style='default', intensity='medium', region='default'):
    hot_prob = _style_hot_prob(intensity)
    style_words = _pick_style_words(style)
    adj_pool = NET_ADJ
    noun_pool = NET_NOUN
    if style_words:
        adj_pool = list(set(NET_ADJ + style_words['prefix']))
        noun_pool = list(set(NET_NOUN + style_words['suffix']))
    adj_pool, noun_pool = _apply_region(adj_pool, noun_pool, region)

    pattern = random.randint(1, 5)
    if pattern == 1:
        return random.choice(adj_pool) + random.choice(noun_pool)
    if pattern == 2:
        return f"{random.choice(adj_pool)}{random.choice(NET_SYMBOL)}{random.choice(noun_pool)}"
    if pattern == 3:
        return _weighted_pick(FEMALE_GIVEN_DOUBLE, FEMALE_GIVEN_DOUBLE_HOT, hot_prob) + random.choice(["未眠", "日记", "来信", "物语", "手札"])
    if pattern == 4:
        return random.choice(["偷一口", "奔赴", "收藏", "路过"]) + random.choice(adj_pool)
    return random.choice(adj_pool) + random.choice(["07", "23", "99", "314", "520"])


@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('tools:nickname:generate')
def generate_nickname_view(request):
    count = int(request.GET.get('count', 100) or 100)
    count = max(1, min(count, 100))
    category = (request.GET.get('category') or 'mixed').strip()
    style = (request.GET.get('style') or 'default').strip()
    intensity = (request.GET.get('intensity') or 'medium').strip()
    region = (request.GET.get('region') or 'default').strip()
    if category not in ['female_name', 'female_nickname', 'female_netname', 'mixed']:
        return error_response('category 不支持', code=400, http_status=status.HTTP_400_BAD_REQUEST)
    if style not in ['default', 'cute', 'cool', 'literary', 'ancient', 'sweet', 'mixed']:
        return error_response('style 不支持', code=400, http_status=status.HTTP_400_BAD_REQUEST)
    if intensity not in ['weak', 'medium', 'strong']:
        return error_response('intensity 不支持', code=400, http_status=status.HTTP_400_BAD_REQUEST)
    if region not in ['default', 'jiangnan', 'beifang', 'modern', 'mixed']:
        return error_response('region 不支持', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    result = []
    seen = set()
    seen_normalized = set()
    max_try = count * 40
    tries = 0
    blacklist_words = [item.lower() for item in BAD_SUBSTRINGS]

    while len(result) < count and tries < max_try:
        tries += 1
        current_style = random.choice(['cute', 'cool', 'literary', 'ancient', 'sweet']) if style == 'mixed' else style
        current_region = random.choice(['jiangnan', 'beifang', 'modern']) if region == 'mixed' else region

        current_category = category
        if category == 'female_name':
            name = _gen_female_name(current_style, intensity)
        elif category == 'female_nickname':
            name = _gen_female_nickname(current_style, intensity)
        elif category == 'female_netname':
            name = _gen_female_netname(current_style, intensity, current_region)
        else:
            pick = random.choice(['female_name', 'female_nickname', 'female_netname'])
            current_category = pick
            if pick == 'female_name':
                name = _gen_female_name(current_style, intensity)
            elif pick == 'female_nickname':
                name = _gen_female_nickname(current_style, intensity)
            else:
                name = _gen_female_netname(current_style, intensity, current_region)

        if not _is_valid_candidate(name, current_category, blacklist_words):
            continue

        normalized = _normalize_for_dedup(name)
        if name in seen or normalized in seen_normalized:
            continue
        seen.add(name)
        seen_normalized.add(normalized)
        result.append(name)

    return success_response({
        'items': result,
        'category': category,
        'style': style,
        'intensity': intensity,
        'region': region,
        'vocab_file': 'backend/apps/tools_management/nickname_vocab.py',
        'quality': {
            'requested': count,
            'generated': len(result),
            'tries': tries,
            'blacklist_count': len(blacklist_words)
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('tools:liushan:add')
def liushan_parse_add_view(request):
    content = (request.data.get('liushan_content') or '').strip()
    try:
        parsed, batch_duplicate = _parse_liushan_entries(content)
    except ValueError as exc:
        return error_response(str(exc), code=400, http_status=status.HTTP_400_BAD_REQUEST)
    if not parsed:
        return success_response([], message='未解析到有效数据')

    created, db_duplicate = _commit_liushan_entries(parsed)
    return success_response({
        'parsed': len(parsed),
        'created': created,
        'batch_duplicate': batch_duplicate,
        'db_duplicate': db_duplicate
    }, message=f'解析完成，共{len(parsed)}条，新增{created}条')


def _parse_liushan_entries(content):
    if len(content) < 20:
        raise ValueError('数据太少，最低不少于20字符')

    parsed = []
    seen = set()
    batch_duplicate = 0
    for entry in ENTRY_PATTERN.findall(content):
        if '同户人：' not in entry:
            continue
        segment = entry.split('同户人：', 1)[1]
        for name, idcard in IDCARD_PATTERN.findall(segment):
            if name == '身份证':
                continue
            key = (name, idcard.upper())
            if key in seen:
                batch_duplicate += 1
                continue
            seen.add(key)
            parsed.append({'name': name, 'idcard': idcard.upper()})
    return parsed, batch_duplicate


def _commit_liushan_entries(parsed):
    created = 0
    db_duplicate = 0
    for item in parsed:
        exists = ToolIdCardRecord.objects.filter(
            is_deleted=False,
            name=item['name'],
            idcard=item['idcard']
        ).exists()
        if exists:
            db_duplicate += 1
            continue

        _, is_created = ToolIdCardRecord.objects.get_or_create(
            idcard=item['idcard'],
            defaults={'name': item['name'], 'status': 0}
        )
        if is_created:
            created += 1
        else:
            db_duplicate += 1
    return created, db_duplicate


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('tools:liushan:add')
def liushan_preview_view(request):
    content = (request.data.get('liushan_content') or '').strip()
    try:
        parsed, batch_duplicate = _parse_liushan_entries(content)
    except ValueError as exc:
        return error_response(str(exc), code=400, http_status=status.HTTP_400_BAD_REQUEST)

    preview_items = []
    db_duplicate = 0
    for item in parsed:
        exists = ToolIdCardRecord.objects.filter(
            is_deleted=False,
            name=item['name'],
            idcard=item['idcard']
        ).exists()
        if exists:
            db_duplicate += 1
            continue
        preview_items.append(item)

    return success_response({
        'parsed': len(parsed),
        'batch_duplicate': batch_duplicate,
        'db_duplicate': db_duplicate,
        'to_insert': len(preview_items),
        'items': preview_items
    }, message='预览完成')


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('tools:liushan:add')
def liushan_commit_view(request):
    items = request.data.get('items') or []
    if not isinstance(items, list) or len(items) == 0:
        return error_response('缺少待入库数据', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    parsed = []
    for item in items:
        name = (item.get('name') or '').strip()
        idcard = (item.get('idcard') or '').strip().upper()
        if not name or not re.match(r'^\d{17}[\dX]$', idcard):
            continue
        parsed.append({'name': name, 'idcard': idcard})

    if not parsed:
        return error_response('无有效数据可入库', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    created, db_duplicate = _commit_liushan_entries(parsed)
    return success_response({
        'submitted': len(parsed),
        'created': created,
        'db_duplicate': db_duplicate
    }, message=f'入库完成，新增{created}条')


@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('tools:liushan:list')
def liushan_list_view(request):
    page = int(request.GET.get('page', 1) or 1)
    limit = int(request.GET.get('limit', 15) or 15)
    page = max(page, 1)
    limit = max(1, min(limit, 100))
    status_val = request.GET.get('status')
    idcard = (request.GET.get('idcard') or '').strip()

    queryset = ToolIdCardRecord.objects.filter(is_deleted=False).order_by('-id')
    if status_val in ['0', '1']:
        queryset = queryset.filter(status=int(status_val))
    if idcard:
        queryset = queryset.filter(idcard__icontains=idcard)

    total = queryset.count()
    start = (page - 1) * limit
    rows = queryset[start:start + limit]
    return success_response({
        'items': ToolIdCardRecordSerializer(rows, many=True).data,
        'total': total,
        'page': page,
        'limit': limit
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('tools:liushan:update')
def liushan_update_status_view(request):
    card_id = request.data.get('id')
    status_val = request.data.get('status')
    if card_id is None or status_val is None:
        return error_response('参数不完整', code=400, http_status=status.HTTP_400_BAD_REQUEST)
    try:
        item = ToolIdCardRecord.objects.get(id=int(card_id), is_deleted=False)
    except ToolIdCardRecord.DoesNotExist:
        return error_response('记录不存在', code=404, http_status=status.HTTP_404_NOT_FOUND)
    item.status = 1 if str(status_val) == '1' else 0
    item.save(update_fields=['status'])
    return success_response(message='更新成功')


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('tools:file-split:run')
def file_split_view(request):
    uploaded_file = request.FILES.get('file')
    mode = request.POST.get('mode')
    split_count = request.POST.get('split_count')
    lines_per_file = request.POST.get('lines_per_file')

    if not uploaded_file:
        return error_response('未上传文件', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    try:
        content = uploaded_file.read().decode('utf-8')
    except UnicodeDecodeError:
        return error_response('仅支持 UTF-8 文本文件', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    lines = content.splitlines()
    total = len(lines)
    if total == 0:
        return error_response('文件内容为空', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    if mode == 'count':
        if not split_count or not str(split_count).isdigit():
            return error_response('缺少或非法 split_count', code=400, http_status=status.HTTP_400_BAD_REQUEST)
        split_count = int(split_count)
        per_file = (total + split_count - 1) // split_count
    elif mode == 'lines':
        if not lines_per_file or not str(lines_per_file).isdigit():
            return error_response('缺少或非法 lines_per_file', code=400, http_status=status.HTTP_400_BAD_REQUEST)
        per_file = int(lines_per_file)
    else:
        return error_response('非法拆分模式', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    with tempfile.TemporaryDirectory() as tmpdir:
        parts = []
        for i in range(0, total, per_file):
            part_lines = lines[i:i + per_file]
            index = i // per_file + 1
            filename = f'part_{index}.txt'
            filepath = os.path.join(tmpdir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(part_lines))
            parts.append(filepath)

        zip_path = os.path.join(tmpdir, 'split_result.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for part in parts:
                zf.write(part, arcname=os.path.basename(part))

        with open(zip_path, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')

        return success_response({
            'filename': 'split_result.zip',
            'mime_type': 'application/zip',
            'content_base64': encoded,
            'parts': len(parts),
            'total_lines': total
        }, message='拆分完成')


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('tools:benefits:upload')
def benefits_upload_view(request):
    files = request.FILES.getlist('files')
    if not files:
        return error_response('未检测到上传文件', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    query_date = (request.data.get('query_date') or '').strip()
    if query_date:
        try:
            target_date = date.fromisoformat(query_date)
        except ValueError:
            return error_response('query_date 格式错误，需为 YYYY-MM-DD', code=400, http_status=status.HTTP_400_BAD_REQUEST)
    else:
        target_date = date.today()

    try:
        result = analyze_benefits_files(files)
    except ValueError as exc:
        return error_response(str(exc), code=400, http_status=status.HTTP_400_BAD_REQUEST)
    except Exception as exc:
        return error_response(f'解析失败: {exc}', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    target_date_str = target_date.isoformat()
    cache_key = get_benefits_cache_key(target_date_str)
    cache.set(cache_key, json.dumps(result, ensure_ascii=False), timeout=CACHE_TTL_BENEFITS)

    return success_response(
        {
            'date': target_date_str,
            'items': result
        },
        message=f'成功上传 {len(files)} 个文件，已写入 {target_date_str}'
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('tools:benefits:stats')
def benefits_stats_view(request):
    query_date = (request.GET.get('query_date') or '').strip()
    cache_key = get_benefits_cache_key(query_date)
    data_json = cache.get(cache_key)
    if not data_json:
        return success_response({}, message='暂无数据')

    if isinstance(data_json, str):
        try:
            return success_response(json.loads(data_json), message='获取数据成功')
        except Exception:
            return success_response({}, message='暂无数据')
    return success_response(data_json, message='获取数据成功')


@api_view(['GET'])
@permission_classes([IsAuthenticated, HasPermission])
@permission_required('tools:benefits:stats')
def benefits_aggregate_view(request):
    start_date_raw = (request.GET.get('start_date') or '').strip()
    end_date_raw = (request.GET.get('end_date') or '').strip()
    if not start_date_raw or not end_date_raw:
        return error_response('请提供 start_date 和 end_date', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    try:
        start_date = date.fromisoformat(start_date_raw)
        end_date = date.fromisoformat(end_date_raw)
    except ValueError:
        return error_response('日期格式错误，需为 YYYY-MM-DD', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    if start_date > end_date:
        return error_response('开始日期不能大于结束日期', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    if (end_date - start_date).days > 366:
        return error_response('区间过大，最多支持 367 天', code=400, http_status=status.HTTP_400_BAD_REQUEST)

    merged_players = {}
    has_data = False
    cur = start_date
    while cur <= end_date:
        cache_key = get_benefits_cache_key(cur.isoformat())
        day_data = cache.get(cache_key)
        if isinstance(day_data, str):
            try:
                day_data = json.loads(day_data)
            except Exception:
                day_data = {}
        if isinstance(day_data, dict) and day_data:
            has_data = True
            for _, players in day_data.items():
                if not isinstance(players, dict):
                    continue
                for player_name, metrics in players.items():
                    if player_name not in merged_players:
                        merged_players[player_name] = {}
                    target = merged_players[player_name]
                    if not isinstance(metrics, dict):
                        continue
                    for metric_key, metric_val in metrics.items():
                        try:
                            num_val = float(metric_val)
                        except Exception:
                            num_val = 0.0
                        target[metric_key] = round(float(target.get(metric_key, 0.0)) + num_val, 2)
        cur += timedelta(days=1)

    if not has_data:
        return success_response({}, message='区间内暂无数据')

    # 复用前端现有结构：俱乐部 -> 玩家 -> 指标，这里放一个虚拟分组
    result = {
        f'区间合计({start_date_raw}~{end_date_raw})': merged_players
    }
    return success_response(result, message='区间合计完成')
