from django.urls import path
from . import views

urlpatterns = [
    path('tools/nickname/generate/', views.generate_nickname_view, name='tools_generate_nickname'),
    path('tools/benefits/stats/', views.benefits_stats_view, name='tools_benefits_stats'),
    path('tools/benefits/aggregate/', views.benefits_aggregate_view, name='tools_benefits_aggregate'),
    path('tools/benefits/upload/', views.benefits_upload_view, name='tools_benefits_upload'),
    path('tools/liushan/add/', views.liushan_parse_add_view, name='tools_liushan_add'),
    path('tools/liushan/preview/', views.liushan_preview_view, name='tools_liushan_preview'),
    path('tools/liushan/commit/', views.liushan_commit_view, name='tools_liushan_commit'),
    path('tools/liushan/list/', views.liushan_list_view, name='tools_liushan_list'),
    path('tools/liushan/update-status/', views.liushan_update_status_view, name='tools_liushan_update_status'),
    path('tools/file-split/run/', views.file_split_view, name='tools_file_split_run'),
]
