from django.urls import path
from . import views

urlpatterns = [
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/add/', views.add_resource, name='add_resource'),
    path('resources/edit/<int:pk>/', views.edit_resource, name='edit_resource'),
    path('resources/delete/<int:pk>/', views.delete_resource, name='delete_resource'),
    path('suggestions/', views.suggestion_list, name='suggestion_list'),
    path('suggestions/add/', views.add_suggestion, name='add_suggestion'),
    path('suggestions/review/<int:pk>/', views.review_suggestion, name='review_suggestion'),
]
