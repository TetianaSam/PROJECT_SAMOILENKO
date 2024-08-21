from django.urls import path
from . import views

urlpatterns = [
    path('', views.protocol_list, name='protocol_list'),

]
