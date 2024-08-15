from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_protocol, name='upload_protocol'),
    path('files/', views.protocol_list, name='protocol_list'),
]
