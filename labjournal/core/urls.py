from django.urls import path
from .views import *
from .views import privacy_policy

urlpatterns = [
    path("", home_page_view, name="home"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),
    path("my-protocols", my_protocols, name="my_protocols"),
    path("my-literature", my_literature, name="my_literature"),
    path("reagents_and_consumables", my_reagents_and_consumables, name="reagents_and_consumables"),
    path("my-projects", my_projects, name="my_projects"),
    path("my-results", my_results, name="my_results"),
    path("my-trainings", my_trainings, name="my_trainings"),
    path("useful-resources", useful_resources, name="useful_resources"),
    path("about", about_page_view, name="about"),
    path("my-lab-journal", my_lab_journal, name="my_lab_journals"),

    ]