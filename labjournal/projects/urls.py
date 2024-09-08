from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('project/<int:pk>/', views.view_project, name='project_detail'),
    path('project/create/', views.create_project, name='create_project'),
    path('project/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('project/<int:pk>/access/', views.manage_project_access, name='manage_project_access'),  # Управління доступом
    path('project/<int:project_id>/remove_access/<int:user_id>/', views.remove_project_access, name='remove_project_access'),  # Видалення доступу
]
