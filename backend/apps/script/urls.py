from django.urls import path
from . import views

urlpatterns = [
    path('script/queues/', views.script_queue_list_view, name='script_queue_list'),
    path('script/queues/create/', views.script_queue_create_view, name='script_queue_create'),
    path('script/queues/<int:queue_id>/clear/', views.script_queue_clear_view, name='script_queue_clear'),
    path('script/queues/<int:queue_id>/delete/', views.script_queue_delete_view, name='script_queue_delete'),
    path('script/queues/<int:queue_id>/upload/', views.script_queue_upload_view, name='script_queue_upload'),
    path('script/configs/public/', views.script_config_public_view, name='script_config_public'),
    path('script/configs/', views.script_config_list_view, name='script_config_list'),
    path('script/configs/create/', views.script_config_create_view, name='script_config_create'),
    path('script/configs/<int:config_id>/', views.script_config_detail_view, name='script_config_detail'),
    path('script/configs/<int:config_id>/update/', views.script_config_update_view, name='script_config_update'),
    path('script/configs/<int:config_id>/delete/', views.script_config_delete_view, name='script_config_delete'),
]
