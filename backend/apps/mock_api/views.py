"""示例 API 视图。"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.core.response import success_response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """仪表盘统计数据"""
    # 返回模拟统计数据
    return success_response({
        'total_users': 1256,
        'active_users': 856,
        'total_orders': 3420,
        'total_revenue': 125680,
        'chart_data': {
            'visits': [120, 132, 101, 134, 90, 230, 210],
            'sales': [220, 182, 191, 234, 290, 330, 310],
            'dates': ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        }
    })


