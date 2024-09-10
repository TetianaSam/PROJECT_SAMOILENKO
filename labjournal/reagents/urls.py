from django.urls import path
from . import views

urlpatterns = [

    path('reagents/', views.reagents_list, name='reagents_list'),
    path('reagents/create/', views.create_reagent, name='create_reagent'),
    path('reagents/<int:pk>/', views.view_reagent, name='view_reagent'),
    path('reagents/<int:pk>/edit/', views.edit_reagent, name='edit_reagent'),
    path('reagents/<int:pk>/delete/', views.delete_reagent, name='delete_reagent'),
    path('reagents/<int:pk>/access/', views.manage_reagent_access, name='manage_reagent_access'),
    path('reagents/<int:reagent_id>/access/remove/<int:user_id>/', views.remove_reagent_access,
         name='remove_reagent_access'),


    path('consumables/', views.consumables_list, name='consumables_list'),
    path('consumables/create/', views.create_consumable, name='create_consumable'),
    path('consumables/<int:pk>/', views.view_consumable, name='view_consumable'),
    path('consumables/<int:pk>/edit/', views.edit_consumable, name='edit_consumable'),
    path('consumables/<int:pk>/delete/', views.delete_consumable, name='delete_consumable'),
    path('consumables/<int:pk>/access/', views.manage_consumable_access, name='manage_consumable_access'),
    path('consumables/<int:consumable_id>/access/remove/<int:user_id>/', views.remove_consumable_access,
         name='remove_consumable_access'),
]
