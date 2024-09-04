from django.urls import path
from . import views

urlpatterns = [

        path('reagents/', views.reagents_list, name='reagents_list'),
        path('reagents/create/', views.create_reagent, name='create_reagent'),
        path('reagents/edit/<int:pk>/', views.edit_reagent, name='edit_reagent'),
        path('reagents/delete/<int:pk>/', views.delete_reagent, name='delete_reagent'),
        path('reagents/view/<int:pk>/', views.view_reagent, name='view_reagent'),
        path('reagents/<int:pk>/manage_access/', views.manage_reagent_access, name='manage_reagent_access'),
        path('consumables/', views.consumables_list, name='consumables_list'),
        path('consumables/create/', views.create_consumable, name='create_consumable'),
        path('consumables/edit/<int:pk>/', views.edit_consumable, name='edit_consumable'),
        path('consumables/delete/<int:pk>/', views.delete_consumable, name='delete_consumable'),
        path('consumables/view/<int:pk>/', views.view_consumable, name='view_consumable'),
        path('consumables/<int:pk>/manage_access/', views.manage_consumable_access, name='manage_consumable_access')
        ]

