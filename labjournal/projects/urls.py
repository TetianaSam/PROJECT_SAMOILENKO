from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),           # Головна сторінка зі списком проектів
    path('project/<int:pk>/', views.view_project, name='project_detail'), # Перегляд деталей проекту
    path('project/create/', views.create_project, name='create_project'), # Створення нового проекту
    path('project/<int:pk>/edit/', views.edit_project, name='edit_project'), # Редагування проекту
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'), # Видалення проекту
]
