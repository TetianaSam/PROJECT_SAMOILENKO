from django.urls import path
from .views import *
from .views import privacy_policy

urlpatterns = [
    path("", home_page_view, name="home"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),
    path("my_projects", my_projects, name="my_projects"),
    path("about", about_page_view, name="about"),
    path("mylabjournal", my_lab_journal, name="my_lab_journals"),

    ]