from django.urls import path
from . import views

urlpatterns = [
    path('script/configs/', views.script_config_list_view, name='script_config_list'),
    path('script/configs/create/', views.script_config_create_view, name='script_config_create'),
    path('script/configs/<int:config_id>/', views.script_config_detail_view, name='script_config_detail'),
    path('script/configs/<int:config_id>/update/', views.script_config_update_view, name='script_config_update'),
    path('script/configs/<int:config_id>/delete/', views.script_config_delete_view, name='script_config_delete'),
]
