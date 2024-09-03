from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/<int:pk>/edit/', views.edit_note, name='edit_note'),
    path('notes/<int:pk>/view/', views.view_note, name='view_note'),
    path('notes/<int:pk>/delete/', views.delete_note, name='delete_note'),
    path('notes/<int:pk>/manage-access/', views.manage_note_access, name='manage_note_access'),
    path('notes/<int:note_id>/remove-access/<int:user_id>/', views.remove_note_access, name='remove_note_access'),
]
