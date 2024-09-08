from django.urls import path
from . import views

urlpatterns = [
    path('', views.protocol_list, name='protocol_list'),
    path('view/<int:pk>/', views.view_protocol, name='view_protocol'),
    path('protocol/create/', views.create_protocol, name='create_protocol'),
    path('protocol/<int:pk>/edit/', views.edit_protocol, name='edit_protocol'),
    path('protocol/<int:pk>/delete/', views.delete_protocol, name='delete_protocol'),
    path('protocol/<int:pk>/download/', views.download_protocol, name='download_protocol'),
    path('protocol/<int:pk>/', views.view_protocol, name='view_protocol'),
]
