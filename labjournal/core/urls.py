from django.urls import path
from .views import *
from .views import privacy_policy

urlpatterns = [
    path("", home_page_view, name="home"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),
    path("my-protocols", my_protocols, name="my_protocols"),
    path("my-literature", my_literature, name="my_literature"),
    path("my-plastic", my_plastic, name="my_plastic"),
    path("my-chemicals", my_chemicals, name="my_chemicals"),
    path("my-projects", my_projects, name="my_projects"),
    path("my-trainings", my_trainings, name="my_trainings"),
    path("about", about_page_view, name="about"),
    path("mylabjournal", my_lab_journal, name="my_lab_journals"),

    ]