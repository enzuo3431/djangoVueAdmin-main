from django.urls import path
from . import views

urlpatterns = [
    path('data-management/archive/', views.archive_data_list_view, name='archive_data_list'),
    path('data-management/archive/platform-meta/', views.archive_data_platform_meta_view, name='archive_data_platform_meta'),
    path('data-management/archive/create/', views.archive_data_create_view, name='archive_data_create'),
    path('data-management/archive/<int:data_id>/update/', views.archive_data_update_view, name='archive_data_update'),
    path('data-management/archive/<int:data_id>/delete/', views.archive_data_delete_view, name='archive_data_delete'),
    path('data-management/archive/import/', views.archive_data_import_view, name='archive_data_import'),
    path('data-management/archive/import/template/', views.archive_data_import_template_view, name='archive_data_import_template'),
    path('data-management/archive/sync/', views.archive_data_sync_view, name='archive_data_sync'),
]
