from django.urls import path
from . import views

urlpatterns = [
    # Reagents URLs

    # Список реагентів
        path('reagents/', views.reagents_list, name='reagents_list'),

        # Створення нового реагента
        path('reagents/create/', views.create_reagent, name='create_reagent'),

        # Редагування реагента
        path('reagents/edit/<int:pk>/', views.edit_reagent, name='edit_reagent'),

        # Видалення реагента
        path('reagents/delete/<int:pk>/', views.delete_reagent, name='delete_reagent'),

        # Перегляд деталей реагента
        path('reagents/view/<int:pk>/', views.view_reagent, name='view_reagent'),

        # Управління доступом до реагента
        path('reagents/<int:pk>/manage_access/', views.manage_reagent_access, name='manage_reagent_access'),



        # Список витратних мreagent'),атеріалів
        path('consumables/', views.consumables_list, name='consumables_list'),

        # Створення нового витратного матеріалу
        path('consumables/create/', views.create_consumable, name='create_consumable'),

        # Редагування витратного матеріалу
        path('consumables/edit/<int:pk>/', views.edit_consumable, name='edit_consumable'),

        # Видалення витратного матеріалу
        path('consumables/delete/<int:pk>/', views.delete_consumable, name='delete_consumable'),

        # Перегляд деталей витратного матеріалу
        path('consumables/view/<int:pk>/', views.view_consumable, name='view_consumable'),

        # Управління доступом до витратного матеріалу
        path('consumables/<int:pk>/manage_access/', views.manage_consumable_access, name='manage_consumable_access')
        ]

